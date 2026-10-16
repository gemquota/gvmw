# Getting the most out of Grok with autonomous, self-assembling, hierarchical multi-agent swarms

*Research brief for Gem. Prepared 2 October 2026 (AEST). Everything here is sourced from the links given; where something couldn't be verified it's flagged.*

**How I read the brief:** "Maximizing Grok, not collaborative augmentation, via self-assembling and auto-bootstrapping hierarchical multi-tiered agent swarms" means: how to get the most capability out of xAI's Grok models using **autonomous** multi-agent systems (no human-in-the-loop "augmentation"). These systems **self-assemble** (the model decides which agents it needs), **auto-bootstrap** (agents spawn and configure sub-agents and tools), and are **organised in tiers** (orchestrator → managers → workers).

---

## TL;DR

- xAI now ships most of the building blocks: frontier and cheap Grok models with function calling and structured outputs, server-side **Agent Tools** (web/X search, code execution, MCP), an OpenAI-compatible API at `https://api.x.ai/v1`, and a hosted **multi-agent model** (`grok-4.20-multi-agent`, 4 or 16 agents) ([xAI models](https://docs.x.ai/docs/models), [multi-agent docs](https://docs.x.ai/developers/model-capabilities/text/multi-agent)).
- The evidence says multi-agent setups win on **breadth-first, parallelisable, read-heavy** tasks. They often *lose* on **sequential** reasoning, and they lose on tool-heavy work run on a fixed budget ([Anthropic](https://www.anthropic.com/engineering/built-multi-agent-research-system), [Kim et al. 2025, arXiv:2512.08296](https://arxiv.org/abs/2512.08296)).
- Most of the gain comes from **spending more tokens in parallel, isolated contexts**. Expect about 15× the tokens of a chat ([Anthropic](https://www.anthropic.com/engineering/built-multi-agent-research-system)).
- Failures are mostly about **system design, coordination and verification**, not raw model capability ([MAST, arXiv:2503.13657](https://arxiv.org/abs/2503.13657)).
- Recommended shape: a **centralised map-reduce-and-manage hierarchy**. Use a strong Grok as orchestrator and cheap Grok workers. Code (not the model) enforces hard limits on depth, fan-out and budget. Use a shared artefact store, a clean-context verifier, and keep writes single-threaded.

---

## 1. What xAI offers today (as at 2 Oct 2026)

> Note: xAI's docs and news pages are now branded **"SpaceXAI"**. I haven't researched the corporate background. The API host is still `api.x.ai`.

### 1.1 Model line-up and pricing (text)

From the [xAI Models & Pricing page](https://docs.x.ai/docs/models) and the individual model pages:

| Model | Context | Input / Cached / Output (USD per 1M tokens, <200k prompt) | Reasoning | Published rate limit* | Notes |
|---|---|---|---|---|---|
| `grok-4.7` | 500k | $2.00 / $0.50 / $6.00 | Yes; efforts `low`–`xhigh` (default `high`) | 150 RPS, 50M TPM | xAI's recommended model for code and chat. Knowledge cut-off May 2026. No Batch API ([page](https://docs.x.ai/developers/models/grok-4.7)) |
| `grok-4.6`, `grok-4.5` | 500k | $2.00 / $0.50 (4.5: $0.30) / $6.00 | — | — | Listed on pricing page |
| `grok-4.3` | 1M | $1.25 / $0.20 / $2.50 | Yes; efforts `none`–`xhigh` (default `low`) | 37 RPS, 10M TPM | "Fast, reliable model with strong tool calling". Batch API −20% ([page](https://docs.x.ai/developers/models/grok-4.3)) |
| `grok-4.20-0309-reasoning` / `-non-reasoning` | 1M | $1.25 / $0.20 / $2.50 | Yes / No | 37 RPS, 10M TPM (non-reasoning) | Non-reasoning variant marketed for speed and tool calling ([page](https://docs.x.ai/developers/models/grok-4.20-0309-non-reasoning)) |
| `grok-build-0.1` | 256k | $1.00 / $0.20 / $2.00 | — | — | Coding model (early access) |
| `grok-4.20-multi-agent-0309` | 1M | $1.25 / $0.20 / $2.50 | Yes | 9 RPS, 2.5M TPM | Hosted multi-agent, **beta** ([page](https://docs.x.ai/developers/models/grok-4.20-multi-agent-0309)) |

Prompts of 200k tokens or more are billed at roughly double for *all* tokens in that request. \*Rate limits shown are the figures on each model page. xAI says actual limits are **per team and scale with spend tier**, and going over them returns HTTP 429 ([Rate limits](https://docs.x.ai/developers/rate-limits)).

### 1.2 API features relevant to swarms

- **OpenAI-compatible API.** The base URL is `https://api.x.ai/v1` with Bearer auth, and the docs show the OpenAI Python SDK pointed at it ([Get started](https://docs.x.ai/overview), [REST overview](https://docs.x.ai/developers/rest-api-reference/inference)). xAI recommends the **Responses API** (`/v1/responses`) over Chat Completions. It supports `previous_response_id`, server-side storage, and encrypted reasoning content, and new features land there first ([comparison](https://docs.x.ai/developers/model-capabilities/text/comparison)).
- **Function calling** (client-side tools) and **built-in server-side tools** (`web_search`, `x_search`, `code_interpreter`/`code_execution`, `collections_search`, image generation, remote **MCP**). These can be mixed in one request. xAI runs the server-side tools itself, while custom functions pause and return to your code ([Tools overview](https://docs.x.ai/developers/tools/overview), [Function calling](https://docs.x.ai/developers/tools/function-calling), [Advanced usage](https://docs.x.ai/developers/tools/advanced-usage)).
- **Structured outputs** via `response_format` with `json_schema`, or the SDK's `parse()` with Pydantic ([Structured outputs](https://docs.x.ai/developers/model-capabilities/text/structured-outputs)).
- **Tool pricing.** Web search, X search and code execution cost **$5 per 1,000 successful calls**, and collections search costs $2.50 per 1,000. Failed calls aren't billed ([Pricing](https://docs.x.ai/developers/pricing), [Tool usage details](https://docs.x.ai/developers/tools/tool-usage-details)).
- **Per-request cost reporting.** `usage.cost_in_usd_ticks` (divide by 1e10 for USD) covers all tokens and tool calls in an agentic request ([Cost tracking](https://docs.x.ai/developers/cost-tracking)). This makes budget enforcement in a swarm much easier.
- **Agent Tools API launch.** Announced alongside Grok 4.1 Fast, it was positioned as letting Grok "operate as a fully autonomous agent" with tools that run entirely on xAI's infrastructure ([xAI news](https://x.ai/news/grok-4-1-fast)). *Grok 4.1 Fast (2M context) no longer appears in the current pricing table. I couldn't confirm whether it has been retired.*

### 1.3 xAI's own multi-agent offerings

- **Grok 4 Heavy (July 2025, consumer SuperGrok Heavy tier).** It uses "parallel test-time compute, which allows Grok to consider multiple hypotheses at once". xAI claimed it was the first to score 50.7% on Humanity's Last Exam (text-only subset) and 61.9% on USAMO'25 ([xAI, Grok 4](https://x.ai/news/grok-4)). These are vendor claims and not independently verified here.
- **`grok-4.20-multi-agent` (API, beta).** You run 4 or 16 agents, and a **leader agent synthesises** the result. Set it with `agent_count` in the xAI SDK, or with `reasoning.effort` `low`/`medium` (4 agents) or `high`/`xhigh` (16 agents) in the OpenAI SDK or REST. It works only on the **Responses API**, supports built-in tools and remote MCP, and does **not** support client-side/custom function tools or `max_tokens`. You only see the leader's output; sub-agent state is encrypted. All sub-agent tokens and tool calls are billed ([Multi-agent docs](https://docs.x.ai/developers/model-capabilities/text/multi-agent)).
- **Safety documentation.** The [Grok 4.20 System Card](https://data.x.ai/2026-04-07-grok-4-20-model-card.pdf) says Grok 4.20 can run in single-agent or multi-agent mode. It assesses malicious use and **loss of control**, but evaluations are in single-agent mode unless stated otherwise.

**Implication:** for pure deep research, `grok-4.20-multi-agent` is a turnkey, hosted "flat" swarm. It can't call your functions and it doesn't expose its internals, so a **custom hierarchy** is still needed when you want your own tools, deeper tiers, verification, or hard budgets. The hosted model works well as a *leaf node* inside such a hierarchy.

---

## 2. What the research literature says

### 2.1 Self-assembling / auto-bootstrapping systems

| Work | Core idea | Key result (as reported by the authors) |
|---|---|---|
| **AutoAgents** ([arXiv:2309.17288](https://arxiv.org/abs/2309.17288)) | Generates task-specific expert agents on the fly and plans with them. An **observer** role reflects on plans and responses | More coherent and accurate than prior multi-agent methods on their benchmarks |
| **AgentVerse** ([arXiv:2308.10848](https://arxiv.org/abs/2308.10848)) | A group that "dynamically adjust[s] its composition" (recruitment → decision → execution → evaluation) | Multi-agent groups outperform a single agent. Documents emergent social behaviours, both positive and negative |
| **MetaGPT** ([arXiv:2308.00352](https://arxiv.org/abs/2308.00352)) | Encodes **SOPs** into role prompts in an assembly line, so agents verify intermediate results | Reduces cascading hallucinations from naive chaining. More coherent results on software benchmarks |
| **GPTSwarm** ([arXiv:2402.16823](https://arxiv.org/abs/2402.16823)) | Agents as **optimisable computational graphs**. Graphs compose recursively into hierarchies, with optimisers for node prompts and edge (orchestration) connectivity | Automatic improvement of agent orchestration |
| **ADAS / Meta Agent Search** ([arXiv:2408.08435](https://arxiv.org/abs/2408.08435)) | A meta-agent **writes new agents in code** and builds a growing archive | Discovered agents beat hand-designed ones and transfer across domains and models. The authors stress "provided we develop it safely" |
| **Agent Symbolic Learning** ([arXiv:2406.18532](https://arxiv.org/abs/2406.18532)) | Treats prompts, tools and pipeline as "weights" and runs language-based back-prop and gradient descent | Agents that self-update after deployment ("self-evolving") |
| **AFlow** ([arXiv:2410.10762](https://arxiv.org/abs/2410.10762)) | MCTS search over code-represented workflows | +5.7% average over baselines. Smaller models beat GPT-4o on some tasks at 4.55% of the cost |
| **MaAS** ([arXiv:2502.04180](https://arxiv.org/abs/2502.04180)) | An "agentic supernet" that samples a **query-dependent** architecture | 6–45% of the inference cost of existing multi-agent systems, with +0.54–11.82% performance |
| **Recursive Language Models** ([arXiv:2512.24601](https://arxiv.org/abs/2512.24601)) | The LLM **recursively calls itself** over pieces of a long prompt held in an environment | Handles inputs about 100× beyond the context window. Beats compaction and coding-agent scaffolds at comparable cost |
| **Magentic-One** ([arXiv:2411.04468](https://arxiv.org/abs/2411.04468)) | Orchestrator that plans, tracks progress and **re-plans**, directing specialist agents | Competitive with the state of the art on GAIA, AssistantBench and WebArena. Modular team composition |
| **More Agents Is All You Need** ([arXiv:2402.05120](https://arxiv.org/abs/2402.05120)) | Plain sample-and-vote ("Agent Forest") | Performance scales with the number of agents, and the gain correlates with task difficulty |
| **Multi-agent debate** ([arXiv:2305.14325](https://arxiv.org/abs/2305.14325)) | Several instances propose and debate | Better maths and strategic reasoning, and fewer hallucinations |

**Pattern:** "self-assembly" works best when the *search over structures* is **query-dependent and cost-aware** (MaAS, AFlow, Anthropic's effort-scaling rules) rather than one fixed, heavy swarm used for everything.

### 2.2 When multi-agent beats single-agent, and when it doesn't

- **Anthropic's multi-agent research system** ([engineering post, Jun 2025](https://www.anthropic.com/engineering/built-multi-agent-research-system)) used an Opus 4 lead with Sonnet 4 sub-agents. It **outperformed single-agent Opus 4 by 90.2%** on their internal research eval.
  - On BrowseComp, three factors explained 95% of performance variance, and **token usage alone explained 80%**.
  - Agents use about **4×** the tokens of chat, and multi-agent systems about **15×**.
  - It's a poor fit where agents must share context or have many dependencies, such as most coding.
  - Early failures included **spawning 50 sub-agents for simple queries**, endless searching, and duplicated work. They were fixed with explicit effort-scaling rules: 1 agent and 3–10 tool calls for simple facts, 2–4 sub-agents for comparisons, 10+ for complex research.
  - Parallel sub-agents plus parallel tool calls cut research time by up to 90%.
- **"Towards a Science of Scaling Agent Systems"** ([arXiv:2512.08296](https://arxiv.org/abs/2512.08296)) tested 180 configurations with matched token budgets.
  - **Tool–coordination trade-off:** tool-heavy tasks suffer from multi-agent overhead.
  - **Capability saturation:** gains turn negative once the single-agent baseline exceeds about **45%**.
  - **Error amplification:** independent agents amplified errors **17.2×**, while centralised coordination held it to **4.4×**.
  - Centralised coordination gave **+80.8%** on parallelisable financial reasoning, but **every multi-agent variant cut sequential planning performance by 39–70%**.
- **Cognition** ([Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents), [Multi-Agents: What's Actually Working, Apr 2026](https://cognition.com/blog/multi-agents-working)): what works is "**writes stay single-threaded**" and extra agents contribute *intelligence*, not actions.
  - A **clean-context reviewer** works best when it shares *no* prior context with the coder. Devin Review averages about 2 bugs per PR, and about 58% of those are severe.
  - Managers spawning child agents is live in Devin, but it needed heavy context engineering.
  - "Unstructured swarms… mostly a distraction". The practical shape is **map-reduce-and-manage**.

### 2.3 Failure modes

**MAST: "Why Do Multi-Agent LLM Systems Fail?"** ([arXiv:2503.13657](https://arxiv.org/abs/2503.13657)) analysed 1,642 traces from 7 frameworks and found **41–86.7% failure rates**. It sorts failures into 14 modes in 3 groups:
1. **System design** (step repetition 15.7%, not recognising termination 12.4%, disobeying the task spec 11.8%, …)
2. **Inter-agent misalignment** (reasoning–action mismatch 13.2%, task derailment 7.4%, failing to ask for clarification 6.8%, …)
3. **Task verification** (incorrect verification 9.1%, no or incomplete verification 8.2%, premature termination 6.2%)

Findings:
- Topology changes beat prompt tweaks.
- A high-level objective check added **+15.6%** for ChatDev.
- "Unaware of termination conditions" and "information withholding" appear almost only in failed runs.

Other recurring problems:
- **Cost blow-up** (15× tokens; [Anthropic](https://www.anthropic.com/engineering/built-multi-agent-research-system))
- Duplicated effort from vague delegation
- **Context rot** in long-running managers ([Cognition](https://cognition.com/blog/multi-agents-working))
- Synchronous bottlenecks while waiting on the slowest sub-agent ([Anthropic](https://www.anthropic.com/engineering/built-multi-agent-research-system))

---

## 3. Frameworks that can run hierarchical, self-spawning swarms on Grok

| Framework | Hierarchy / spawning support | Grok / xAI support | Notes |
|---|---|---|---|
| **Roll-your-own on the xAI Responses API** | Whatever you code: a `spawn_agent` function tool plus recursion (see §4) | Native | Most control over budgets and limits. Server-side tools for free |
| **OpenAI Agents SDK** | **Handoffs** (transfer control) and **agents-as-tools** (`agent.as_tool`, where the manager keeps control) | Via `AsyncOpenAI(base_url=…)` + `OpenAIChatCompletionsModel`, `set_default_openai_client`, per-agent `Agent.model`, or the beta LiteLLM / Any-LLM adapters ([Models docs](https://openai.github.io/openai-agents-python/models/)) | Disable tracing or swap the trace processor if you have no OpenAI key. Its *hosted* multi-agent and some Responses-only tool features are OpenAI-only |
| **LangGraph** (+ `langgraph-supervisor`) | `create_supervisor` nests teams under a **top-level supervisor**, so it's explicitly hierarchical ([README](https://github.com/langchain-ai/langgraph-supervisor-py/blob/main/README.md)) | `ChatXAI` (langchain-xai) or any OpenAI-compatible chat model | Graph state works well as shared memory and checkpoints |
| **CrewAI** | `Process.hierarchical` with `manager_llm` or a custom `manager_agent` ([Processes](https://docs.crewai.com/edge/en/concepts/processes)) | LiteLLM `xai/<model>` strings ([CrewAI LLMs](https://docs.crewai.com/edge/en/concepts/llms), [LiteLLM xAI](https://docs.litellm.ai/docs/providers/xai)) | The manager delegates and validates. Agents are mostly predefined, not self-spawned |
| **AG2 (AutoGen)** | GroupChat / nested chats / swarm patterns | Documented Grok config: `api_type="openai"`, `base_url="https://api.x.ai/v1"`, plus a Responses-API path for xAI built-in tools ([AG2 Grok guide](https://classic.docs.ag2.ai/latest/docs/user-guide/models/grok-and-oai-compatible-models/)) | MAST studied AG2 traces |
| **Swarms (kyegomez)** | `HierarchicalSwarm` (director plus worker agents, `max_loops`) ([docs](https://docs.swarms.world/architectures/hierarchical-swarm)) | LiteLLM-style `model_name="xai/…"` | I couldn't confirm the current constructor arguments from primary docs; check the repo |
| **CAMEL** | `Workforce` (coordinator plus task planner plus workers) ([Workforce docs](https://docs.camel-ai.org/key_modules/workforce)) | Native `ModelPlatformType.XAI` backend ([xai_model.py](https://github.com/camel-ai/camel/blob/master/camel/models/xai_model.py)) | |
| **smolagents** | `managed_agents` lets an agent call sub-agents (nested hierarchy) | `LiteLLMModel("xai/…")` or `OpenAIServerModel(api_base=…)` ([HF docs](https://huggingface.co/docs/smolagents/main/examples/using_different_models)) | Code-acting agents |
| **MetaGPT / AFlow, GPTSwarm, ADAS** | Research codebases for SOP pipelines and automated structure search | Generally OpenAI-compatible configs (not individually verified for Grok) | Good for *offline* search over swarm designs, then freeze the winner |

Code examples in the search snippets used model strings like `grok-4` or `grok-4.5`. **Use current names from the [xAI models page](https://docs.x.ai/docs/models)** (for example `grok-4.7`, `grok-4.3`).

---

## 4. Recommended architecture: a self-bootstrapping hierarchical Grok swarm

### 4.1 Design principles (each traced to evidence)

1. **Centralised hierarchy, not peer-to-peer.** Centralised coordination limits error amplification (4.4× vs 17.2×) ([2512.08296](https://arxiv.org/abs/2512.08296)), and map-reduce-and-manage is what works in production ([Cognition](https://cognition.com/blog/multi-agents-working)).
2. **Decide whether to swarm at all.** Classify the task first. Sequential or tightly coupled work, or work a single agent already does well, goes to **one strong agent**. Swarming hurt sequential tasks by 39–70% and returns diminish above a 45% single-agent baseline ([2512.08296](https://arxiv.org/abs/2512.08296)).
3. **Self-assembly through a spawn tool, with effort-scaling rules written into the prompt** (1 / 2–4 / 10+ agents) ([Anthropic](https://www.anthropic.com/engineering/built-multi-agent-research-system)). This is query-dependent architecture, in the spirit of MaAS and AutoAgents.
4. **Hard limits live in code, not in prompts.** These are depth, fan-out, total agents, turns per agent, USD budget and wall-clock time. Use `cost_in_usd_ticks` to meter spend ([xAI cost tracking](https://docs.x.ai/developers/cost-tracking)).
5. **Delegation contract.** Every spawn must specify an objective, output format, tools/sources and boundaries ([Anthropic](https://www.anthropic.com/engineering/built-multi-agent-research-system)). Use structured outputs ([xAI](https://docs.x.ai/developers/model-capabilities/text/structured-outputs)).
6. **Shared memory = artefact store (blackboard), not chat relay.** Sub-agents write findings and pass back references, which avoids the "game of telephone". The plan is persisted so it survives context limits ([Anthropic](https://www.anthropic.com/engineering/built-multi-agent-research-system)).
7. **Single-threaded writes.** Only one agent (or a deterministic merger) commits side effects ([Cognition](https://cognition.com/blog/multi-agents-working)).
8. **Multi-level verification.** Workers self-check. A **clean-context verifier** checks claims against evidence, and a final objective-level check confirms the task was met ([MAST](https://arxiv.org/abs/2503.13657), [Cognition](https://cognition.com/blog/multi-agents-working)).
9. **Explicit termination.** Use success criteria, a bounded critique loop (for example ≤2 rounds), and "INSUFFICIENT EVIDENCE" as an allowed answer. This targets MAST's termination and premature-termination failures.

### 4.2 Tiers and model choice

| Tier | Job | Suggested Grok model | Rationale |
|---|---|---|---|
| **T0 Orchestrator** | Classify the task, plan, decide swarm vs single agent, spawn T1/T2, synthesise | `grok-4.7`, effort `high` | Most capable per xAI. 500k context. Low volume, so higher cost is acceptable |
| **T1 Managers** (optional, only for very broad tasks) | Own one sub-domain, spawn workers, merge results | `grok-4.7` effort `medium`, or `grok-4.3` effort `medium`/`high` | Needs judgement about delegation, at moderate volume |
| **T2 Workers** | Narrow search / extract / compute, using server-side `web_search`, `x_search`, `code_interpreter` | `grok-4.3` effort `low` (or `none`), or `grok-4.20-0309-non-reasoning` | $1.25/$2.50 per 1M, 1M context, strong tool calling. Batch API −20% for offline jobs |
| **Deep-research leaf** (optional) | One-shot broad research subtask | `grok-4.20-multi-agent`, effort `low` (4 agents) or `high` (16 agents) | Hosted parallelism. No custom tools, so use it only as a leaf |
| **Verifier / critic** | Clean-context fact and objective check | `grok-4.7` effort `high`, ideally with `web_search` | Should be at least as strong as the generator. Clean context helps ([Cognition](https://cognition.com/blog/multi-agents-working)) |

*Model-to-tier pairings are my recommendation, based on xAI's published positioning and prices. I haven't benchmarked them.*

### 4.3 Spawning rules and limits (suggested starting values)

- `max_depth = 2` (T0 → T1 → T2). Only T0 and T1 get the `spawn_agent` tool; workers can't spawn.
- `max_children = 5` per parent and `max_agents = 20` per job. Anthropic ran 3–5 sub-agents in parallel and saw 50-agent blow-ups without rules.
- `max_turns = 12` per agent, plus a per-job **USD budget** and wall-clock timeout. When a limit is hit, the error is returned *to the parent as a tool result* so it can adapt, rather than crashing (as in Anthropic's practice of telling agents when tools fail).
- Respect per-model **RPS/TPM**: use a semaphore and exponential back-off on 429 ([xAI rate limits](https://docs.x.ai/developers/rate-limits)).
- Log every spawn (parent, objective, cost) for tracing. MAST-style post-hoc labelling is possible ([MAST](https://arxiv.org/abs/2503.13657)).

### 4.4 Python sketch (xAI Responses API via the OpenAI SDK)

I checked the endpoint (`https://api.x.ai/v1`) and model names against docs.x.ai on 2 Oct 2026. The code has only been **syntax-checked. It has not been run against the live API**, so test it before relying on it. The same file is at `/workspace/grok-swarm-research/swarm_sketch.py`.

```python
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
```

**How it maps to the principles:**
- Self-assembly = the orchestrator's `spawn_agent` calls.
- Auto-bootstrapping = children get role-appropriate tools and the spawn tool at T0/T1 only.
- Hierarchy and limits are enforced in Python.
- The blackboard is the shared memory.
- The verifier runs with a clean context, inside a bounded critique loop.

**Simpler variants:**
- For pure deep research, have T0 delegate to `grok-4.20-multi-agent` as a single leaf call.
- With the OpenAI Agents SDK, model each worker as `agent.as_tool(...)` on an `OpenAIChatCompletionsModel` pointed at `api.x.ai` ([Agents SDK models](https://openai.github.io/openai-agents-python/models/)). Note that dynamic spawning then needs a function tool that builds `Agent` objects at runtime.

---

## 5. Practical caveats

- **Cost.** Multi-agent runs use about 15× chat tokens ([Anthropic](https://www.anthropic.com/engineering/built-multi-agent-research-system)).
  - With Grok, every server-side tool call adds $5 per 1,000 on top of tokens ([xAI pricing](https://docs.x.ai/developers/pricing)).
  - The 16-agent hosted model uses "significantly more tokens" than the 4-agent one ([xAI](https://docs.x.ai/developers/model-capabilities/text/multi-agent)).
  - Prompts at or above 200k tokens double the rate for the whole request, so keep manager contexts small and push detail into the blackboard.
  - Use cached input (much cheaper on every model) by keeping system prompts stable.
- **Latency.** Synchronous fan-out waits on the slowest child ([Anthropic](https://www.anthropic.com/engineering/built-multi-agent-research-system)). Grok 4 Heavy itself showed "~10 min" per-agent timers in xAI's launch demo ([xAI](https://x.ai/news/grok-4)). Parallelise tools and children, and stream results.
- **Error compounding.** Errors cascade in agentic settings, and independent agents amplify them 17.2× ([2512.08296](https://arxiv.org/abs/2512.08296)). Verification is the weakest link in existing systems ([MAST](https://arxiv.org/abs/2503.13657)). Use centralised control, evidence-grounded verification, and durable checkpoints so you can resume rather than restart ([Anthropic](https://www.anthropic.com/engineering/built-multi-agent-research-system)).
- **When not to swarm.** Sequential reasoning, tightly coupled coding, and tasks a single agent already handles well (above about 45%) usually get worse with a swarm ([2512.08296](https://arxiv.org/abs/2512.08296), [Cognition](https://cognition.com/blog/dont-build-multi-agents)).
- **Safety limits on self-replication.** Unbounded self-spawning is both a cost risk and a recognised safety concern.
  - Researchers report open-weight LLM agents creating live copies of themselves in 50% and 90% of trials ([arXiv:2412.12140](https://arxiv.org/abs/2412.12140)). That's a single-group, non-peer-reviewed preprint.
  - ADAS's authors explicitly caveat "provided we develop it safely" ([arXiv:2408.08435](https://arxiv.org/abs/2408.08435)).
  - xAI's [Grok 4.20 System Card](https://data.x.ai/2026-04-07-grok-4-20-model-card.pdf) evaluates loss-of-control risk and notes that use must follow xAI's Acceptable Use Policy.
  - Practical rules:
    - Agents may only spawn *through* your orchestrator's function. They never get credentials, shell access to launch processes, or the ability to change their own limits.
    - Run code execution in xAI's server-side sandbox or your own isolated sandbox.
    - Allow-list MCP servers and tools.
    - Give side-effecting tools idempotency keys and a single writer.
    - Keep a kill switch and an audit log.
- **Autonomy vs oversight.** The brief asks for no human in the loop. The evidence (Anthropic's human testers catching source-quality bias, Cognition's "scale human taste") suggests keeping at least **offline** human evaluation of sampled runs, even if each run is fully autonomous.
- **Beta and vendor-claim risk.** `grok-4.20-multi-agent` is beta with a non-final interface. Benchmark claims (Grok 4 Heavy, Grok 4.20 "lowest hallucination rate") are xAI's own and I haven't independently verified them.

---

## Things I couldn't verify

- Whether **Grok 4.1 Fast** (2M context) is still offered. It's missing from the current pricing table.
- What the "SpaceXAI" rebrand on xAI's docs means.
- Current **Swarms (kyegomez)** `HierarchicalSwarm` arguments and native Grok handling, beyond LiteLLM model strings.
- Exact behaviour of `function_call_output` round-trips on xAI's Responses API. The sketch follows the OpenAI Responses format that xAI says it's compatible with, but it hasn't been tested live.
- Independent benchmarks of Grok in hierarchical swarms. I found none. All Grok performance figures here are xAI's.

---

## Sources

**xAI**
- Models & pricing: https://docs.x.ai/docs/models
- Grok 4.7: https://docs.x.ai/developers/models/grok-4.7
- Grok 4.3: https://docs.x.ai/developers/models/grok-4.3
- Grok 4.20 non-reasoning: https://docs.x.ai/developers/models/grok-4.20-0309-non-reasoning
- Grok 4.20 Multi-Agent model page: https://docs.x.ai/developers/models/grok-4.20-multi-agent-0309
- Multi-agent guide: https://docs.x.ai/developers/model-capabilities/text/multi-agent
- Tools overview: https://docs.x.ai/developers/tools/overview
- Function calling: https://docs.x.ai/developers/tools/function-calling
- Advanced tool usage: https://docs.x.ai/developers/tools/advanced-usage
- Tool usage details: https://docs.x.ai/developers/tools/tool-usage-details
- Pricing (tools): https://docs.x.ai/developers/pricing
- Cost tracking: https://docs.x.ai/developers/cost-tracking
- Rate limits: https://docs.x.ai/developers/rate-limits
- Structured outputs: https://docs.x.ai/developers/model-capabilities/text/structured-outputs
- Responses vs Chat Completions: https://docs.x.ai/developers/model-capabilities/text/comparison
- Get started: https://docs.x.ai/overview
- REST API overview: https://docs.x.ai/developers/rest-api-reference/inference
- Grok 4 / Grok 4 Heavy announcement: https://x.ai/news/grok-4
- Grok 4.1 Fast & Agent Tools API: https://x.ai/news/grok-4-1-fast
- Grok 4.20 System Card: https://data.x.ai/2026-04-07-grok-4-20-model-card.pdf

**Research and industry write-ups**
- Anthropic, How we built our multi-agent research system: https://www.anthropic.com/engineering/built-multi-agent-research-system
- Cemri et al., Why Do Multi-Agent LLM Systems Fail? (MAST): https://arxiv.org/abs/2503.13657
- Kim et al., Towards a Science of Scaling Agent Systems: https://arxiv.org/abs/2512.08296
- Cognition, Don't Build Multi-Agents: https://cognition.com/blog/dont-build-multi-agents
- Cognition, Multi-Agents: What's Actually Working: https://cognition.com/blog/multi-agents-working
- AutoAgents: https://arxiv.org/abs/2309.17288
- MetaGPT: https://arxiv.org/abs/2308.00352
- AgentVerse: https://arxiv.org/abs/2308.10848
- GPTSwarm: https://arxiv.org/abs/2402.16823
- ADAS / Meta Agent Search: https://arxiv.org/abs/2408.08435
- Agent Symbolic Learning: https://arxiv.org/abs/2406.18532
- AFlow: https://arxiv.org/abs/2410.10762
- MaAS: https://arxiv.org/abs/2502.04180
- Recursive Language Models: https://arxiv.org/abs/2512.24601
- Magentic-One: https://arxiv.org/abs/2411.04468
- More Agents Is All You Need: https://arxiv.org/abs/2402.05120
- Multiagent Debate: https://arxiv.org/abs/2305.14325
- Self-replication red line (preprint): https://arxiv.org/abs/2412.12140

**Frameworks**
- OpenAI Agents SDK, Models: https://openai.github.io/openai-agents-python/models/
- LangGraph Supervisor: https://github.com/langchain-ai/langgraph-supervisor-py/blob/main/README.md
- CrewAI Processes: https://docs.crewai.com/edge/en/concepts/processes
- CrewAI LLMs: https://docs.crewai.com/edge/en/concepts/llms
- LiteLLM xAI provider: https://docs.litellm.ai/docs/providers/xai
- AG2 Grok guide: https://classic.docs.ag2.ai/latest/docs/user-guide/models/grok-and-oai-compatible-models/
- Swarms HierarchicalSwarm: https://docs.swarms.world/architectures/hierarchical-swarm
- CAMEL Workforce: https://docs.camel-ai.org/key_modules/workforce
- CAMEL xAI model: https://github.com/camel-ai/camel/blob/master/camel/models/xai_model.py
- smolagents, using different models: https://huggingface.co/docs/smolagents/main/examples/using_different_models
