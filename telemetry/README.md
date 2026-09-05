# Aggregate funnel telemetry

This offer measures only three cumulative public GitHub issue-label counts:

1. **Requests** — issues labeled `request`.
2. **Scopes accepted** — issues labeled `scope-accepted`.
3. **Delivered** — issues labeled `delivered`.

Issues labeled `telemetry-test` are excluded from every count. A private-scope
contact counts as a request because the public contact issue is an explicit funnel
event, but its template forbids request details. Counts never imply unique people,
revenue, quality, or conversion attribution; one person can create multiple issues,
and deleted/transferred issues can reduce a later snapshot.

`funnel.json` is a checked-in snapshot. `tools/update_funnel.py` asks GitHub's
GraphQL search API for `issueCount` only and writes aggregate integers plus the UTC
refresh time. It does not request issue nodes, titles, bodies, authors, comments,
IP addresses, referrers, or private repository data. The landing page fetches that
same-origin JSON and does not send an analytics event.

There are deliberately no page-view or click counters, cookies, local storage,
fingerprinting, analytics SDKs, third-party pixels, serverless ingestion endpoints,
or private-content ledgers. Therefore the funnel starts at explicit public contact;
anonymous visits and clicks are unknowable. A snapshot changes only when this script
is run, committed, and deployed.

Refresh locally with an authenticated `gh` CLI session that can read the public
repository:

```sh
python3 tools/update_funnel.py
```

Audit the underlying public sets through the links on the landing page or GitHub's
label views. The checked-in JSON contains no request content.
