# Agent Reliability Evidence Pack

A public reference implementation of one bounded reliability investigation: reproducible failure evidence, an executable regression fixture, a minimal candidate patch, rollback, and explicit limitations.

**Current service catalog:** https://bemjamin-site.vercel.app/#services

**Machine-readable status:** https://agent-reliability-evidence-pack-rho.vercel.app/offer.json

## Status

This repository is **shipped public proof**, not an active checkout page. The former USD 25 reference pilot is preserved in git history and identified in `offer.json` as historical. New scope requests have moved to Bemjamin's public catalog.

Payment is inactive. No funds should be sent: no wallet address is published, and protected Solana custody/recovery has not been established.

## Reference deliverable

The checked-in sample demonstrates this fixed boundary:

1. agree one workflow, one consequential question, and one acceptance check;
2. reproduce the failure or record a bounded negative under declared conditions;
3. create a minimal fixture and tests;
4. propose a small patch only when evidence supports it;
5. report commands, outputs, rollback, limitations, and unresolved uncertainty.

A prose-only opinion is not a delivered evidence pack. A negative result is not proof that the bug never exists.

## Public evidence

- [Complete redacted sample report](samples/durable-state-post-replace-error/REPORT.md)
- [Runnable sample fixture](samples/durable-state-post-replace-error/fixture)
- [Machine-readable current status](offer.json)
- [Public service catalog and acceptance boundaries](https://bemjamin-site.vercel.app/#services)

Run the repository checks:

```sh
python3 -m unittest discover -s tests -v
```

## Safety boundary

No credentials, wallet or recovery material, private incident data, customer data, proprietary source, production dumps, unsafe production testing, malware/evasion, surveillance, spam/manipulation, regulated advice, or guarantees are accepted. Public inputs must be safe to publish permanently.

## Rebrand and attribution

Bemjamin maintains this evidence pack as a reference artifact for the broader fixed-scope catalog. Git history and third-party attribution remain preserved.

## License

MIT; see [LICENSE](LICENSE). The vendored upstream fixture retains its own MIT notice in its fixture directory.
