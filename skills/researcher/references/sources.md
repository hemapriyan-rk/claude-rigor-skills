# Where to search, and how

## Sources by layer

| Layer | Sources | Notes |
|---|---|---|
| **Academic** | Google Scholar, Semantic Scholar, arXiv, IEEE Xplore, ACM Digital Library, PubMed (biomedical), DBLP (computer science) | Semantic Scholar shows "cited by" and related papers, which is good for citation chaining |
| **Patents** | Google Patents, Espacenet (EPO), WIPO PATENTSCOPE, USPTO Patent Public Search, InPASS (India) | Search by CPC class as well as keywords. See below |
| **Products** | Company docs and changelogs, GitHub, Hacker News ("Show HN"), Product Hunt, app stores, Crunchbase | A shipped product is prior art even without a patent or paper |
| **Standards** | IETF RFCs, ISO, IEC, IEEE Standards, W3C, 3GPP, NIST publications | Standards often settle "is this viable" regardless of novelty |
| **Regulation** | FDA device databases, EU MDR, national regulators | For medical, safety, automotive, telecom |

## Building queries

1. **Describe the mechanism, not the product.** "Phone speaker emits ultrasonic chirp, microphone measures time of flight for room-level location" finds more than "smart indoor locator."
2. **Collect synonyms from the first relevant result.** The vocabulary in the first good paper or patent tells you what the field calls it. Search again with those words.
3. **Search the problem, then the solution.** Papers that tried the same problem another way show what you're competing against.
4. **Chain citations both ways.** Look at what the closest result cites (older work) and what cites it (newer work).
5. **Date-filter for state of the art.** In fast-moving fields, limit to the last 2–3 years for the "current" picture.

## Patent search specifics

- **Find the CPC class** from the best keyword hit's classification, then search within it. Classes catch patents that use completely different wording.
- **Google Patents:** use `CPC=G01S5/18`, `before:priority:20200101`, `assignee:"..."`, and exact phrases in quotes.
- **Espacenet:** use Smart Search with `cpc=...` and `txt=...`.
- **Check dates:** prior art is judged against the priority date of the claim, not the publication date.
- **Check status before calling a patent a threat:** granted, pending, lapsed, or expired matters for freedom to operate, though not for novelty.

## Judging sources

| Weight | Source type |
|---|---|
| **Strong** | Peer-reviewed paper, granted patent, official standard, primary documentation, source code you read |
| **Medium** | Preprint, pending application, reputable technical blog by practitioners, conference talk |
| **Weak** | Vendor marketing, press release, aggregator or listicle, AI-generated summary, undated page |

Load-bearing claims need at least one strong source.
