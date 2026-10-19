"""Growth test: repeat handle_message and record traced heap at checkpoints."""

import gc
import tracemalloc

import simulate
import worker


def run(n, start):
    for i in range(start, start + n):
        worker.handle_message(simulate.fake_message(i))


if __name__ == "__main__":
    run(500, 0)  # warm up
    gc.collect()
    tracemalloc.start(25)
    gc.collect()
    base = tracemalloc.take_snapshot()
    prev = tracemalloc.get_traced_memory()[0]
    done = 500
    total = 0
    for step in (1000, 1000, 2000, 4000):
        run(step, done)
        done += step
        total += step
        gc.collect()
        cur = tracemalloc.get_traced_memory()[0]
        print(f"after {total:5d} msgs: heap={cur/1e6:8.2f} MB  "
              f"delta={(cur-prev)/step:8.0f} B/msg  handlers={len(worker.bus._handlers['audit'])}")
        prev = cur
    for stat in tracemalloc.take_snapshot().compare_to(base, "lineno")[:5]:
        print(stat)
