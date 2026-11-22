# Corpus coverage — Q-Parser

Generated: 2026-11-22T07:22:06+00:00

| Metric | Value |
|---|---|
| Canonical URLs in inventory | 128 |
| Present and HTTP 200 | 128 |
| Missing | 0 |
| Thin / non-200 | 0 |
| Total extracted characters | 442,579 |

## Missing

- none

## Thin / non-200 pages

- none

## Method

- Canonical documentation URLs only. The sitemap's `/catalog/<city>/<category>` permutations are excluded by design.
- Each page is stored twice: raw HTML (`raw/`) and cleaned Markdown (`pages/`) with source frontmatter.
- The manifest records HTTP status, byte size, SHA-256, title and fetch timestamp for every URL.

## Rebuild

```bash
python tools/fetch_corpus.py            # incremental
python tools/fetch_corpus.py --force    # full refetch
python tools/extract_qparser.py
python tools/build_knowledge.py
python tools/verify_coverage.py
```
