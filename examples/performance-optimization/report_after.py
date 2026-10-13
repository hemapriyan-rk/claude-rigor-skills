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
    return list(dict.fromkeys(s["email"] for s in signups))


def count_by_country(signups, emails):
    first_country = {}
    for s in signups:
        first_country.setdefault(s["email"], s["country"])
    counts = {}
    for email in emails:
        country = first_country.get(email)
        if country is not None:
            counts[country] = counts.get(country, 0) + 1
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
