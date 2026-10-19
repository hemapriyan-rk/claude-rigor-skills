# Demo: `memory-leak-hunter` on a message worker

Run on 2026-10-19 in a fresh, headless Claude Code session (model `claude-sonnet-5-5`, `--setting-sources project,local` so only this skill was installed) in a folder containing only `worker.py`, `simulate.py`, and the skill. [output.md](output.md) is the session's output, unedited.

## Prompt

```text
Use the memory-leak-hunter skill on worker.py. Our message worker's memory climbs steadily until it gets OOM-killed after about a day. simulate.py feeds it fake messages the way the queue consumer does.
```

**Tools allowed:** Skill, Read, Edit, Write, Glob, Grep, `python`. **Cost:** $0.16, 47 seconds.

## Files

- [`worker_before.py`](worker_before.py) is the code the session was given. It has one real leak, and one bounded cache (`lru_cache(maxsize=512)`) that is not a leak.
- [`worker_after.py`](worker_after.py) is what the session wrote: the handler is unsubscribed in a `finally` block.
- [`growth_test.py`](growth_test.py) is the repeatable growth test the session wrote.
- [`simulate.py`](simulate.py) feeds the worker fake messages. It imports `worker`, so copy one of the two versions to `worker.py` first.

## What to look for

- It proved the growth with checkpoints before touching code, and found the exact chain: module-level `bus._handlers["audit"]` → closure → `RequestContext` → the raw message.
- It explained why growth accelerated: every leaked handler also receives every later event.
- It correctly identified the `lru_cache(maxsize=512)` as bounded and left it alone.
- **Checked independently** with its own growth test: before, 322 MB and 8,500 registered handlers after 8,000 messages; after, 0 MB and 0 handlers.

## Run it yourself

```sh
cp worker_before.py worker.py && python growth_test.py   # grows
cp worker_after.py worker.py && python growth_test.py    # flat
```

Model output varies from run to run, so a re-run will be worded differently.
