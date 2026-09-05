# Sample evidence report: post-replace error is not an uncommitted write

**Report date:** 2026-09-05 UTC
**Public source:** [`ikorfale/durable-state-write` v0.4.0](https://github.com/ikorfale/durable-state-write/tree/v0.4.0)
**Pinned commit:** [`0dddd546b5b0a8d9018f6ed7d08b6d6e8ddfa045`](https://github.com/ikorfale/durable-state-write/commit/0dddd546b5b0a8d9018f6ed7d08b6d6e8ddfa045)
**Scope:** one local error-classification boundary in `durable_replace()`
**Result:** failure reproduced; bounded patch passes the supplied regression test

## Executive result

In v0.4.0, an exception raised after `os.replace()` escapes with its original,
generic type even though the destination already contains the new generation.
A caller that treats every ordinary exception as “the write did not happen” can
retry a surrounding side effect or state transition incorrectly. This report
does **not** claim that `durable-state-write` itself performs or duplicates an
external side effect; it demonstrates that its post-replace failure is not
machine-distinguishable from a pre-replace failure by exception type.

The supplied patch introduces `ReplacementPublishedError`. It wraps ordinary
Python exceptions raised after the successful namespace replacement while
preserving the original exception as `__cause__`. The patched result tells a
caller that the new file became visible and that post-replace confirmation
failed, so blind retry is unsafe. The patch does not claim power-loss durability.

## Acceptance check

1. The vendored source byte-for-byte matches public v0.4.0 by SHA-256.
2. A deterministic hook raises immediately after `os.replace()`.
3. Baseline v0.4.0 raises the injected ordinary `RuntimeError` while the file
   contains `new\n`.
4. The patch applies cleanly with `git apply --check`.
5. Under the same trigger, the patched source raises
   `ReplacementPublishedError`, chains the original `RuntimeError`, and leaves
   the same published `new\n` generation.

All five conditions are asserted by the executable fixture.

## Reproduce

Requirements: Python 3.10+ and Git. No network access, credentials, services,
wallets, or private data are needed after cloning this repository.

```sh
git clone https://github.com/ikorfale/agent-reliability-evidence-pack.git
cd agent-reliability-evidence-pack
python3 samples/durable-state-post-replace-error/tests/test_sample.py
```

Expected summary:

```text
Ran 3 tests

OK
```

The first test pins the vendored upstream file to SHA-256
`118fe51f71916158eb48bffc6d1d910f44155251950e8a6d6dce9c1e1e27d37e`.
Its provenance is the public command:

```sh
git -C durable-state-write show v0.4.0:durable_state.py | sha256sum
```

## Evidence captured

On Linux 6.8 with Python 3.12.3, the isolated baseline trigger produced:

```text
raised=RuntimeError: injected after replace
destination=b'new\n'
temps=[]
```

The regression suite then applied
[`patches/classify-post-replace-errors.patch`](patches/classify-post-replace-errors.patch)
to a temporary copy and proved that the same trigger raises the new classified
exception with the original error chained. Both baseline and patched runs
observe the complete new generation; the intended change is classification,
not write ordering.

## Cause and bounded patch

Both `durable_replace()` and `durable_replace_stream()` set `replaced = True`
immediately after `os.replace()`. Their subsequent hook, directory open, and
directory `fsync` can still raise. In v0.4.0 those exceptions leave the function
without communicating that replacement already occurred.

The patch wraps only the post-replace confirmation block in both functions. It:

- adds one public `ReplacementPublishedError` type;
- preserves the original exception through exception chaining;
- leaves all pre-replace behavior unchanged;
- leaves hard process exits and power loss outside Python exception handling;
- does not add dependencies, background cleanup, locking, or network behavior.

This is a candidate patch supplied as part of the sample. It has not been merged
into or released from `durable-state-write`; users must not describe v0.4.0 as
fixed.

## Security and privacy

The fixture contains only public MIT-licensed source and synthetic bytes
(`old\n`, `new\n`). It includes no logs, hostnames, account IDs, credentials,
private paths, customer data, endpoints, blockchain interaction, or production
state. The injected hook is an existing test-only interface in the public
artifact. Nothing is retained outside this public repository.

## Limitations

- The fixture proves a deterministic Python exception boundary, not an actual
  disk, controller, kernel, or power-loss fault.
- It demonstrates retry ambiguity; it does not execute or observe a duplicate
  external effect.
- `ReplacementPublishedError` means `os.replace()` returned successfully and
  the new generation became visible in the running namespace. It does not mean
  the containing-directory `fsync` succeeded or that the rename survives power
  loss.
- `BaseException` events such as `KeyboardInterrupt`, `SystemExit`, signals, or
  `os._exit()` are not wrapped.
- The candidate exception type is a small API addition, but downstream callers
  that match exact exception classes still need review.
- NFS, hostile directory mutation, ACLs/xattrs, full disks, and concurrent
  read-modify-write safety remain outside this sample.

## Rollback

This repository deploys only static documentation. Roll back the report/site by
reverting its release commit. To undo the candidate source change in a separate
`durable-state-write` checkout, run:

```sh
git apply -R patches/classify-post-replace-errors.patch
```

from a checkout where the patch was applied (adjust the patch path as needed).
No service restart, database migration, wallet action, or state conversion is
required.
