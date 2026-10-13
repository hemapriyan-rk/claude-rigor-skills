# Patent search guide

## Databases

| Database | Use it for |
|---|---|
| **Google Patents** | Fast full-text search across major offices, with non-patent literature from Google Scholar mixed in |
| **Espacenet** (EPO) | Worldwide coverage, CPC browsing, patent family and legal status |
| **WIPO PATENTSCOPE** | PCT applications, cross-language search |
| **USPTO Patent Public Search** | Full US text and US-specific detail |
| **InPASS** (Indian Patent Office) | Indian applications and grants |

## Steps

1. **Mechanism keywords.** Describe what the invention *does*, in the field's terms. Write 2–3 phrasings with synonyms.
2. **Find the CPC class.** Open the 2–3 most relevant hits from step 1 and note their CPC classes. Classes find documents that use completely different words.
3. **Search within the class.** Combine the class with 1–2 key terms.
4. **Chain citations.** For the closest hit, check the documents it cites (backward) and the ones that cite it (forward).
5. **Non-patent literature and products.** Run the same mechanism queries on Google Scholar, arXiv, GitHub, and product pages.

## Query syntax

| Database | Example |
|---|---|
| Google Patents | `(drowsiness OR fatigue) (EEG OR electroencephalogram) helmet` |
| Google Patents, class filter | `CPC=A61B5/18 helmet vibration` |
| Google Patents, date filter | `before:priority:20210101` |
| Espacenet Smart Search | `cpc=A61B5/18 and txt="helmet"` |

## Dates

- Prior art counts if it was public **before the claim's priority date**: the earliest filing date the application can rely on.
- The inventor's own public disclosure before filing can count against them. The US has a 1-year grace period for the inventor's own disclosures. Europe generally has none. India has limited grace provisions. Flag any public demo, paper, or repository the inventor has already released.

## Recording the search

Log each database, query, CPC class, and how many results you reviewed. The search log goes in the report so the user can extend it, and a patent attorney can judge how thorough it was.
