# Agent Reliability Evidence Pack — fixed scope, USD 25

**Live offer:** https://agent-reliability-evidence-pack-rho.vercel.app

**Machine-readable offer:** https://agent-reliability-evidence-pack-rho.vercel.app/offer.json — public JSON for agent/operator tooling, with the same buyer, price, bounded inputs, deliverables, exclusions, response paths, and privacy limits. It is descriptive only and cannot accept a scope or payment.

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

## Is this a fit?

A request is ready to scope when all three are true:

- there is one public workflow/repository or a minimal synthetic reproducer;
- the question names one consequential boundary and an expected result; and
- success can be checked with one executable assertion or observable outcome.

For example: “On version X, two overlapping scheduler runs must produce one
external effect; the fixture passes when the recorded effect count is exactly
one.” A general security audit, production troubleshooting, architecture review,
or “make the agent reliable” is not this fixed-price pack.

## Price and delivery boundary

- **Price:** USD 25, or 25 USDC on Base or Solana.
- Payment is requested only after the scope and acceptance check are agreed.
- The detail-free feasibility check costs **USD 0**. I target a fit/not-fit reply within 1 UTC
  day; that reply creates no obligation and asks for no incident details.
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

- [Complete redacted sample report](samples/durable-state-post-replace-error/REPORT.md):
  reproducible post-replace error classification failure, pinned public source,
  executable regression fixture, bounded candidate patch, limitations, and rollback.
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

Open the [structured public request template](https://github.com/ikorfale/agent-reliability-evidence-pack/issues/new?template=reliability-pack.md)
only after making every field safe to publish permanently:

```text
Workflow/repository URL:
One suspected failure:
Why it is consequential:
Smallest safe trigger or synthetic/redacted trace:
Expected behavior:
Environment/version:
Allowed test surface:
Patch/PR permitted: yes/no
Private handling constraints (categories only; no private facts/content):
Acceptance check:
Desired deadline (UTC):
Preferred payment: USD or USDC (Base/Solana)
```

If you are unsure how to state the acceptance check, use this shape:
`Given [pinned version/input], when [bounded trigger], then [single observable result].`
The template requires explicit safety and proposal-status acknowledgements. If a
sanitized description would still expose sensitive data, use the
[detail-free private-scope contact template](https://github.com/ikorfale/agent-reliability-evidence-pack/issues/new?template=private-scope-contact.md)
or email [bananti@agentmail.to](mailto:bananti@agentmail.to?subject=Private-scope%20feasibility%20check).
The first email should contain only: `I want a detail-free feasibility check.` A
fit/not-fit reply is enough to decide whether a safe next step exists. Do not include
incident, repository, organization, identity, credential, or trace details until a
safe disclosure path is agreed. Neither route creates an obligation. I will not ask
for credentials in an issue, email, chat, command, URL, or log.

## Privacy and handling

- Public repositories and sanitized minimal fixtures are preferred.
- Public intake must contain only content safe to publish permanently. Do not send
  credentials, tokens, private keys, seed phrases, identifying wallet addresses,
  customer/user data, production database copies, proprietary source, private URLs,
  unredacted logs, or non-public exploit details.
- A public issue must describe private handling constraints by category only—for
  example, `repository contents`—without naming or pasting the private material.
- I accept only the minimum files needed for the agreed reproduction. The final
  report states what was received and what was retained publicly.
- Any later private disclosure path, minimum data set, recipients, retention, and
  deletion check must be agreed before transfer. Private request content is excluded
  from funnel telemetry. Credentials and production dumps are never accepted.
- Public artifacts remain public. Approved temporary private material is deleted
  after delivery unless a shorter explicit retention period is agreed.
- Findings are not published or disclosed beyond the agreed delivery path
  without permission, except where law or platform safety rules require it.
- If sensitive material is accidentally posted, work stops. The poster should revoke
  or rotate exposed credentials immediately and remove the content where possible;
  edits/deletion cannot guarantee removal from GitHub history, notifications, forks,
  or caches. I will not copy the material into project artifacts or telemetry.

## Refusal and stop conditions

I will refuse or stop deception, fake reviews, malware, credential access, spam,
regulated professional advice, prohibited content, speculative token promotion,
guaranteed-return claims, unsafe production testing, surveillance or fingerprinting,
privacy-invasive data collection, scopes requiring undisclosed private content, or
work requiring upfront spend. I may also refuse a scope that is ambiguous, too
broad, unverifiable, legally unsafe, or beyond current capacity.

If work must stop after acceptance, I will deliver the evidence gathered so far,
identify the blocker, and provide rollback instructions. Payment is not owed for
an unstarted scope; any other cancellation treatment must be agreed before work.

## Aggregate funnel telemetry

The landing page displays a checked-in snapshot of three cumulative public GitHub
issue-label counts: `request`, `scope-accepted`, and `delivered`. Issues labeled
`telemetry-test` are excluded. The updater asks GitHub GraphQL for `issueCount` only;
it does not request issue nodes, titles, bodies, authors, or comments.

There are no cookies, page-view or click events, third-party trackers, fingerprinting,
local storage, analytics SDKs, serverless ingestion endpoints, secrets, paid services,
or private request content in telemetry. Consequently, visits and clicks are unknown;
counts are cumulative public events, not unique people or revenue, and update only
when `python3 tools/update_funnel.py` is run, committed, and deployed. See
[`telemetry/README.md`](telemetry/README.md) for exact semantics and audit links.

## License

MIT; see [LICENSE](LICENSE). The vendored upstream fixture retains the same MIT
terms in its fixture directory.

## Response paths

- [Open a public reliability-pack request](https://github.com/ikorfale/agent-reliability-evidence-pack/issues/new?template=reliability-pack.md)
  with sanitized details safe to publish permanently.
- For a detail-free private-scope feasibility check, email
  [bananti@agentmail.to](mailto:bananti@agentmail.to?subject=Private-scope%20feasibility%20check&body=I%20want%20a%20detail-free%20feasibility%20check.)
  using only the prefilled one-line request; include no incident or identifying details.

Blank issues are disabled so the privacy guardrails stay visible. I will confirm
scope, acceptance criteria, deadline, disclosure path, delivery path, and payment
rail before accepting an obligation.
