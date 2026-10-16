# MedB export (format `medb-export/1.0`)

This directory is a complete export of one MedB instance. It is meant to be
read **without MedB software**. Everything needed to interpret it is described
here and in `schema/`. `verify_export.py` is a ~150-line, standard-library-only
reference checker that does not import MedB.

## 1. Model in one paragraph

MedB stores nothing by overwriting. Each kind of record is an append-only
**stream** of events (`events/<stream>.jsonl`). Each event is hash-chained to
the one before it in its stream. Current state is computed by **replaying**
events in `seq` order. A past state ("what did MedB record at time T?") comes
from replaying only the events with `ts <= T`. Corrections, supersessions,
disavowals and deletions are new events (*transitions*), never edits.

## 2. Streams

| stream | what it records | key event kinds |
|---|---|---|
| `gov` | governance log: every action evaluation and execution, escalation, context package issued, claim retrieval, policy change, prohibited attempt, suspension, audit result, integrity check, export | `ACTION_EVALUATED`, `ACTION_EXECUTED`, `ESCALATION_*`, `CONTEXT_PACKAGE_ISSUED`, `CLAIMS_RETRIEVED`, `POLICY_CHANGE`, `PROHIBITED_ATTEMPT`, `STATE_TRANSITION`, ... |
| `claims` | the claim ledger | `ASSERT` (user self-account), `PROPOSE` (inference), `CONFIRM`, `REJECT`, `CORRECT`, `SUPERSEDE`, `DISAVOW`, `DELETE` |
| `permissions` | ingest/infer/model/use grants issued by the user | `GRANT`, `REVOKE` |
| `policy` | versions of delegation policy P-1 and module classification | `VERSION` |
| `suspension` | suspension records (immutable) and their status transitions | `RECORD`, `TRANSITION`, `ADJACENT` |
| `corpus` | immutable corpus items; withdrawal makes an item unusable but keeps its content (F-05) | `INGEST`, `WITHDRAW` |
| `delegation` | delegation grants | `GRANT`, `REVOKE` |
| `normative` | user directives: the positions stated when resolving escalations (F-18); not claims | `DIRECTIVE` |
| `auditlog` | audit-plane reads (Q-1, audit views, export) made while any suspension was active (F-11). Deliberately NOT cross-linked into `gov`, so governance-log evidence is not perturbed by auditing | `AUDIT_READ` |
| `anchors` | optional external RFC 3161 timestamp receipts over a digest of all stream heads (F-13; off by default) | `ANCHOR` |

`gov` events of kind `STATE_TRANSITION` cross-link the governance chain to a
domain event: `{stream, seq, event_hash}`. Every `normative` and `anchors`
event has such a cross-link; no `auditlog` event does.

An `ANCHOR` body holds `heads` (`{stream: {seq, hash}}`, every stream except
`anchors`), `heads_digest` = sha256(canonical(heads)) -- the only value sent to
the timestamping authority -- and `receipt_b64`, the raw RFC 3161
TimeStampResp. `verify_export.py` checks that the heads match the chains and
that the receipt is granted and contains the digest as its message imprint; the
TSA's CMS signature is checked offline, e.g.
`openssl ts -verify -digest <heads_digest> -in receipt.tsr -CAfile tsa-chain.pem`
(after base64-decoding `receipt_b64` into `receipt.tsr`).

## 3. Verifying integrity

For each stream, with `prev = "0"*64`:

```
record = {stream, seq, event_id, ts, kind, actor, body}      # all fields except prev_hash, hash
hash   = sha256( canonical({"prev": prev, "record": record}) )
canonical(x) = JSON, keys sorted, separators (",", ":"), UTF-8, no ASCII escaping
```

`seq` must be 1, 2, 3, ... with no gaps. Each event's `prev_hash` must equal the
previous event's `hash`. `manifest.json` lists the sha256 of every file and the
head of every stream.

## 4. Claims

A claim has `claim_id, subject, predicate, object, source, origin, created_at,
confirmation, temporal_validity, scope, sensitivity`.

* `subject, predicate, object, source, temporal_validity` are **content**. They
  are stored in `content/claim_content.json` under a salted commitment
  `content_ref = "c-" + sha256(salt + canonical(content))`.
* A `DELETE` transition destroys the content of every version of the claim.
  The commitment, the metadata and the fact of deletion stay in the chain. A
  deleted claim's content is absent from `claim_content.json`, and that absence
  is intentional.
* `origin`: `user_stated` (the user's self-account) or `inference` (proposed by
  MedB's inference layer).
* `confirmation`: `user_asserted` | `unconfirmed` | `user_confirmed` |
  `user_rejected`. Only the user can move a claim out of `unconfirmed`.
  Inference can only `PROPOSE`.
* `medb_mediated: true` means the evidence appeared after the user was exposed
  to MedB output (for example, confirming a MedB proposal). Treat it as not
  independent of MedB (Principle 12).
* `derived_from` lists the inputs (claims or corpus items). It is the
  derivation path that permissions must close over.
* Status after replay: `active`, `rejected`, `superseded`, `disavowed`,
  `deleted`.
* Two times: `ts` is transaction time (when MedB recorded it), and
  `temporal_validity.valid_from/valid_to` is valid time (when the claim is
  asserted to hold).

## 5. Permissions

A grant has `operation` (`ingest`, `infer`, `model` or `use`), `scopes`,
`purposes` (for `use`), `sources` (for `ingest`), `sensitivity_max`,
`compose`, and `expires_at`. Sensitivity order is
`low < moderate < high < special`. An operation on an item is permitted only if
**one** active grant covers the item and every ancestor on its derivation
path. Composing several inputs (multi-input inference, multi-scope packages)
requires such a grant with `compose: true`.

## 6. Delegation and P-1

`gov` `ACTION_EVALUATED` holds the proposed action, the decision
(`AUTHORIZED`, `REQUIRES_ESCALATION` or `PROHIBITED`), the governing clause,
and a trace of every clause checked, together with the digests of the policy
and classification versions in force. `ACTION_EXECUTED.authorizing_clause` is
either a P-1 clause id or `USER_APPROVAL<clause>`. The policy text for each
version is in `policy` `VERSION` events.

## 7. Suspensions

`RECORD` bodies are immutable; see `schema/suspension_record.schema.json`. The
current status is the `to` of the record's last `TRANSITION`
(`SUSPENDED`, `RESOLVED_PASS` or `NONCOMPLIANT`). `ADJACENT` events flag
indirect dependents as `SUSPENSION_ADJACENT`.

## 8. Context packages

MedB does not retain packages. `CONTEXT_PACKAGE_ISSUED` logs the package id,
purpose, requester, expiry, the claim versions included (`claim_refs` with
event hashes), the template key used for each claim, the digest of the
rendering configuration, contradictions, unknowns, boundary, and the complete
ranking record (inputs, weights, scores, order). A package can be
reconstructed from the ledger as of `issued_at`, except for content deleted
since then.

## 9. Provenance

`prov/prov.json` is a W3C PROV-JSON view (entities = claims and corpus items,
activities = transitions, agents = actors, `wasDerivedFrom` = derivation).

## 10. What is not in an export

Rendered package text, which is never retained, and the content of deleted
claims, which is destroyed.
