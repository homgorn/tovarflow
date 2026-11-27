# ADR 0007 — Project name: TovarFlow

**Status:** accepted · **Date:** 2026-11-27 · **Confidence:** 8/10

## Context

The project needed a name that works in Russian speech, carries SEO keywords, and has an available
domain in `.ru` and ideally `.com`. We generated 65 bases, removed 12 by the reading rule
(`gate`, `way`, `line`, `base` introduce the `й` sound in Russian reading), and checked 53 full
`.ru` domains through WHOIS.

## Decision

Use **TovarFlow** (товар + поток) with primary domain `tovarflow.ru` and `tovarflow.com` for global
expansion.

Evidence:

- WHOIS: both domains `available` on 2026-11-27 (two checks for the finalists).
- Wayback CDX for `tovarflow.ru`: `no_captures` — no snapshots found in the checked index.
- Google exact quoted query `"tovarflow.ru"`: no relevant exact mentions; results were unrelated
  `tovar.kg` listings.
- Yandex exact quoted query: captcha → recorded as `blocked`, not as "no results".

SEO roots in the name and tagline: **товар**, **поток товаров**, **парсинг товаров**, **каталог**,
**витрина**. Confidence 8/10 because availability is measured twice but history coverage is
incomplete (Yandex blocked, 28 Wayback checks errored).

## Alternatives

| Candidate | Why not |
|---|---|
| CatalogFlow | `.com` taken; `.ru` free but weaker brand than "товар" for RU SEO |
| VitrinaFlow | `.com` taken; "витрина" is narrower than the platform scope |
| TovarMost / TovarPotok | Free, but less obvious as a product brand and weaker in English |

## Consequences

Positive: short, dictatable, carries the main RU commercial keyword, both key zones available.

Negative: "flow" is English; requires a stable tagline in Russian to anchor meaning. The name is
not a trademark check; legal review is still required before registration.

## Reopen conditions

- `tovarflow.ru` or `.com` becomes taken before registration.
- A trademark conflict is found.
- The product pivots away from supplier catalogues entirely.
