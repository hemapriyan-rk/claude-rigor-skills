"""Feed the worker fake messages, the way the queue consumer does in production."""

import random
import sys

from worker import handle_message

rng = random.Random(1)


def fake_message(i):
    return {
        "id": f"msg-{i}",
        "customer": f"c{rng.randint(1, 5000)}",
        "country": rng.choice(["IN", "DE", "GB", "US", "JP", "BR"]),
        "quantity": rng.randint(-1, 20),
        "unit_price": round(rng.uniform(1, 500), 2),
        "notes": "x" * rng.randint(200, 2000),
    }


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    for i in range(n):
        handle_message(fake_message(i))
    print(f"processed {n} messages")
