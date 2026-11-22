# Research tracks

> Each track is a folder with `REPORT.md` (narrative), `data.json` (machine-readable records) and
> sources with observation dates. The research DB loads both; the graph links them.

## Status (2026-11-22)

| Track | Folder | Status | Records |
|---|---|---|---|
| Competitors | `competitors/` | complete | 33 |
| RU marketplaces | `marketplaces/ru/` | complete | 6 |
| CN marketplaces | `marketplaces/cn/` | complete | 11 |
| Global marketplaces | `marketplaces/global/` | complete | 16 |
| Storefront platforms | `platforms/` | complete | 11 |
| Demand and niches | `demand/` | complete | — |
| Inherited assets | `inherited/` | complete | 14 |

## Method

1. Official documentation and pricing pages first.
2. Every fact carries `source_url`, `observed_at`, `confidence`.
3. A blocked page is `not verified`, never guessed.
4. A marketplace is analysed as `supply` or `sales` before API details.
5. Entity requirements and ToS blockers are recorded before endpoints.
6. Long reports end with a Gaps section.

## Output contract

```text
docs/research/<track>/
  REPORT.md     narrative, tables, decisions, gaps
  data.json     { generated_at, method, records: [...] }
  atoms/        optional: one concept/finding/question per file
```

`data.json` is loaded by `tools/build_research_db.py` into `data/research.sqlite` and indexed with
FTS5. The wiki page `wiki/research/<track>.md` is generated from it.

## Known gaps

- Competitor pricing for several RU services is rendered client-side or behind a login.
- Some marketplace docs are login-walled (Rakuten, Cdiscount/Octopia, Zalando partner).
- Chinese domestic platforms require a Chinese entity; the legal path is not resolved.
- Demand data requires paid accounts (MPSTATS, Semrush) for the highest-confidence signals.
