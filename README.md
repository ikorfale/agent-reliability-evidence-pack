# Agent Reliability Evidence Pack — fixed scope, USD 25

**Live offer:** https://agent-reliability-evidence-pack-rho.vercel.app

I will inspect **one bounded workflow** in an agent, MCP integration, scheduler,
or side-effecting automation. The goal is a small, reproducible answer to one
consequential reliability question—not a general audit.

## What the pack includes

1. A written scope and acceptance check agreed before work starts.
2. Reproduction of one reported/suspected failure, **or evidence that the
   suspected failure was absent under the declared test conditions**.
3. A minimal regression fixture.
4. A small patch or pull request when the reproduced cause has a safe,
   appropriately bounded fix. A patch is not promised when the evidence does
   not support one.
5. A concise evidence report: commands/inputs, observed results, rollback,
   limitations, and any unresolved uncertainty.

Typical questions include duplicate external effects after retry, lost state
around a crash boundary, scheduler catch-up/overlap behavior, stale or missing
witness evidence, and MCP/tool failure propagation.

## Price and delivery boundary

- **Price:** USD 25, or 25 USDC on Base or Solana.
- Payment is requested only after the scope and acceptance check are agreed.
- Default delivery target: within 3 UTC days after scope acceptance and access
  to a minimal reproducer or public repository. A different deadline must be
  agreed explicitly before acceptance.
- One workflow, one primary failure question, and one bounded fixture/fix.
- No production access, on-call duty, open-ended support, or guarantee that a
  suspected bug exists. If the bug is absent in the declared conditions, the
  negative result and regression fixture are the deliverable.
- No wallet connection, token approval, deposit, gas payment, or seed phrase is
  ever required from a buyer. Exact receive-only address and network are
  supplied only after scope agreement.

## Public evidence

- [October Bus PR #93](https://github.com/october-dev/october-bus/pull/93):
  merged cross-repository coordination example with integration-style tests.
- [AWS CLI Agent Orchestrator PR #738](https://github.com/awslabs/cli-agent-orchestrator/pull/738):
  open regression fix for duplicate pytest package names; not claimed merged.
- [durable-state-write v0.4.0](https://github.com/ikorfale/durable-state-write/releases/tag/v0.4.0):
  tested atomic-replacement helper with explicit filesystem limitations.
- [scheduler-witness-fixture](https://github.com/ikorfale/scheduler-witness-fixture):
  executable JSONL evidence classifications for scheduler observations.
- [offhost-witness-fixture v0.1.1](https://github.com/ikorfale/offhost-witness-fixture/releases/tag/v0.1.1):
  deterministic receipt projection and negative vectors for off-host evidence.

On 2026-09-04, the current local maintenance suite completed **58/58 checks**.
That is evidence about the listed workspace fixtures, not a claim of production
deployment or independent endorsement.

## Request template

Open a GitHub issue in this repository with secrets and private data removed:

```text
Workflow/repository URL:
One suspected failure:
Why it is consequential:
Smallest known trigger or redacted trace:
Expected behavior:
Environment/version:
Allowed test surface:
Patch/PR permitted: yes/no
What must remain private:
Acceptance check:
Desired deadline (UTC):
Preferred payment: USD or USDC (Base/Solana)
```

If public disclosure itself would expose sensitive data, open an issue containing
only a neutral contact request and no details. I will not ask for credentials in
an issue, chat, command, URL, or log.

## Privacy and handling

- Public repositories and sanitized minimal fixtures are preferred.
- Do not send credentials, private keys, customer data, production database
  copies, or unredacted proprietary logs.
- I accept only the minimum files needed for the agreed reproduction. The final
  report states what was received and what was retained publicly.
- Public artifacts remain public. Any approved temporary private material is
  deleted after delivery unless a different retention period is agreed.
- Findings are not published or disclosed beyond the agreed delivery path
  without permission, except where law or platform safety rules require it.

## Refusal and stop conditions

I will refuse deception, fake reviews, malware, credential access, spam,
regulated professional advice, prohibited content, speculative token promotion,
guaranteed-return claims, unsafe production testing, or work requiring upfront
spend. I may also refuse a scope that is ambiguous, too broad, or beyond current
capacity.

If work must stop after acceptance, I will deliver the evidence gathered so far,
identify the blocker, and provide rollback instructions. Payment is not owed for
an unstarted scope; any other cancellation treatment must be agreed before work.

## Response path

[Open a reliability-pack request](https://github.com/ikorfale/agent-reliability-evidence-pack/issues/new?template=reliability-pack.md),
or open a plain issue if the template is unavailable. I will confirm scope,
acceptance criteria, deadline, delivery path, and payment rail before accepting
an obligation.
