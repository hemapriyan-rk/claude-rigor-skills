"""Build a daily signup report: unique emails per country and a CSV summary."""

import random
import string


def make_signups(n, seed=7):
    rng = random.Random(seed)
    countries = ["IN", "US", "DE", "BR", "JP", "NG", "FR", "GB"]
    signups = []
    for _ in range(n):
        user = "".join(rng.choices(string.ascii_lowercase, k=5))
        signups.append({"email": f"{user}@example.com", "country": rng.choice(countries)})
    return signups


def unique_emails(signups):
    seen = []
    for s in signups:
        if s["email"] not in seen:
            seen.append(s["email"])
    return seen


def count_by_country(signups, emails):
    counts = {}
    for email in emails:
        for s in signups:
            if s["email"] == email:
                counts[s["country"]] = counts.get(s["country"], 0) + 1
                break
    return counts


def to_csv(counts):
    out = "country,unique_signups\n"
    for country in sorted(counts):
        out += f"{country},{counts[country]}\n"
    return out


if __name__ == "__main__":
    signups = make_signups(12_000)
    emails = unique_emails(signups)
    print(to_csv(count_by_country(signups, emails)))
