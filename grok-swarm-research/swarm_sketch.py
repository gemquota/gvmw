"""
Minimal self-bootstrapping, hierarchical Grok swarm (sketch, not production code).

Tiers:  Orchestrator (grok-4.7, high effort)
          -> spawns Managers / Workers via a `spawn_agent` function tool
        Workers (grok-4.3, low effort, server-side web_search / code_interpreter)
        Verifier (grok-4.7, clean context) checks the final answer.

Hard limits (depth, total agents, fan-out, USD budget, turns) are enforced in
Python, never by the model. Endpoint/model names checked against docs.x.ai on
2 Oct 2026. NOT run against the live API: test before relying on it.
"""
import json, os, threading
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI

client = OpenAI(api_key=os.environ["XAI_API_KEY"], base_url="https://api.x.ai/v1")

MODELS = {"orchestrator": "grok-4.7", "manager": "grok-4.7",
          "worker": "grok-4.3", "verifier": "grok-4.7"}
EFFORT = {"orchestrator": "high", "manager": "medium", "worker": "low", "verifier": "high"}

LIMITS = dict(max_depth=2, max_agents=20, max_children=5, max_turns=12, budget_usd=5.00)

class Ledger:
    """Shared, thread-safe budget + agent counter + blackboard memory."""
    def __init__(self):
        self.lock = threading.Lock()
        self.spent = 0.0
        self.agents = 0
        self.blackboard = {}          # key -> artefact (findings live here, not in chat)

    def charge(self, resp):
        ticks = getattr(getattr(resp, "usage", None), "cost_in_usd_ticks", None)
        with self.lock:
            if ticks:                  # xAI returns cost in 1e-10 USD ticks
                self.spent += ticks / 1e10
            if self.spent > LIMITS["budget_usd"]:
                raise RuntimeError(f"Budget exceeded: ${self.spent:.2f}")

    def new_agent(self):
        with self.lock:
            if self.agents >= LIMITS["max_agents"]:
                raise RuntimeError("Agent cap reached")
            self.agents += 1
            return self.agents

L = Ledger()

SPAWN_TOOL = {
    "type": "function", "name": "spawn_agent",
    "description": ("Create a sub-agent for ONE well-scoped, independent subtask. "
                    "Give objective, output format, tools to use and boundaries. "
                    "Use 1 agent for simple facts, 2-4 for comparisons, more only for broad research."),
    "parameters": {"type": "object", "properties": {
        "role": {"type": "string", "enum": ["manager", "worker"]},
        "objective": {"type": "string"},
        "output_format": {"type": "string"},
        "use_web": {"type": "boolean"}},
        "required": ["role", "objective", "output_format", "use_web"]},
}
WRITE_TOOL = {
    "type": "function", "name": "write_blackboard",
    "description": "Store a finding/artefact in shared memory; return its key instead of pasting long text.",
    "parameters": {"type": "object", "properties": {
        "key": {"type": "string"}, "content": {"type": "string"}},
        "required": ["key", "content"]},
}

def run_agent(role, objective, output_format, depth=0, use_web=False):
    agent_id = L.new_agent()
    tools = [WRITE_TOOL]
    if role in ("orchestrator", "manager") and depth < LIMITS["max_depth"]:
        tools.append(SPAWN_TOOL)                       # only upper tiers may spawn
    if use_web or role == "worker":
        tools += [{"type": "web_search"}, {"type": "code_interpreter"}]  # server-side, run by xAI

    instructions = (f"You are a {role} (agent #{agent_id}, depth {depth}). "
                    f"Objective: {objective}\nReturn: {output_format}\n"
                    "Stop as soon as the objective is met. Say 'INSUFFICIENT EVIDENCE' rather than guess.")
    resp = client.responses.create(model=MODELS[role], instructions=instructions,
                                   input=objective, tools=tools,
                                   reasoning={"effort": EFFORT[role]})
    L.charge(resp)

    for _ in range(LIMITS["max_turns"]):
        calls = [o for o in resp.output if getattr(o, "type", "") == "function_call"]
        if not calls:
            return resp.output_text
        spawns = [c for c in calls if c.name == "spawn_agent"][: LIMITS["max_children"]]
        outputs = []
        # fan out children in parallel (bounded)
        with ThreadPoolExecutor(max_workers=LIMITS["max_children"]) as pool:
            futs = {c.call_id: pool.submit(_child, c, depth) for c in spawns}
        for c in calls:
            if c.name == "write_blackboard":
                a = json.loads(c.arguments)
                L.blackboard[a["key"]] = a["content"]
                out = f"stored:{a['key']}"
            elif c.call_id in futs:
                out = futs[c.call_id].result()
            else:
                out = "ERROR: spawn rejected (fan-out limit)"
            outputs.append({"type": "function_call_output", "call_id": c.call_id, "output": out})
        resp = client.responses.create(model=MODELS[role], previous_response_id=resp.id,
                                       input=outputs, tools=tools,
                                       reasoning={"effort": EFFORT[role]})
        L.charge(resp)
    return "TERMINATED: turn limit reached"

def _child(call, depth):
    a = json.loads(call.arguments)
    try:
        return run_agent(a["role"], a["objective"], a["output_format"], depth + 1, a["use_web"])
    except RuntimeError as e:                        # budget/agent cap: report up, don't crash
        return f"ERROR: {e}"

def verify(task, answer):
    """Clean-context verifier: sees only the task + answer + blackboard, not the swarm's chatter."""
    resp = client.responses.create(
        model=MODELS["verifier"], reasoning={"effort": EFFORT["verifier"]},
        tools=[{"type": "web_search"}],
        input=(f"TASK:\n{task}\n\nCANDIDATE ANSWER:\n{answer}\n\nEVIDENCE:\n"
               f"{json.dumps(L.blackboard)[:50000]}\n\nCheck every claim. Reply JSON: "
               '{"pass": bool, "problems": [str]}'))
    L.charge(resp)
    return resp.output_text

if __name__ == "__main__":
    task = "Compare the three most-cited approaches to X, with sources."
    answer = run_agent("orchestrator", task, "Markdown report with inline source URLs")
    for attempt in range(2):                         # bounded critique loop
        verdict = verify(task, answer)
        try:
            if json.loads(verdict).get("pass"):
                break
        except json.JSONDecodeError:
            pass                                     # treat unparseable verdict as a fail
        answer = run_agent("orchestrator", f"{task}\nFix these problems: {verdict}\nPrevious draft:\n{answer}",
                           "Corrected Markdown report")
    print(answer, f"\n\nAgents: {L.agents}  Spend: ${L.spent:.2f}")
