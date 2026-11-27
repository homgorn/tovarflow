# Answer-First / AEO content contract

> Applies to every textual page we publish: storefront product and category pages, wiki pages,
> reports and documentation. Confidence in the ranking mechanics: 7/10 (mechanics widely reported;
> the owner-supplied +30–40% citation figure is reported, not independently measured here).
> Primary source: https://developers.google.com/search/docs/fundamentals/seo-starter-guide.

## 1. Direct answer

Put a factual answer in the **first 150–300 characters (40–80 words)** immediately under `<h1>` or
`<h2>`. RAG pipelines chunk HTML into 200–500 tokens (~800–2000 characters) and the first chunk is
the one most likely to be read and quoted verbatim.

Template for a product page:

```markdown
# Товар X — бренд, артикул, цена

Товар X (артикул ART-00001, бренд Nord) — 1 590 ₽, в наличии 12 шт на складе Москва,
доставка 2 дня. Категория: Кухня. Совместимость: ... Гарантия 12 месяцев.
```

The first sentence contains: name, SKU, brand, price, currency, availability, units, delivery time,
category and warranty. No adjective like «unforgettable» before the facts.

## 2. Chunking

- Target chunk: 200–500 tokens (~800–2000 characters), split at headings and paragraphs.
- Our existing corpus chunker uses ~1400 characters — compatible.
- Every chunk keeps its heading and source URL. A retrieval result must be traceable.
- Do not bury the answer after a hero image, navigation or a cookie banner in the raw HTML.

## 3. Fact density

Prefer exact, verifiable values:

| Weak | Strong |
|---|---|
| «быстрая доставка» | «доставка 2 дня, склад Москва, выгрузка каждый час» |
| «высокое качество» | «хлопок 100%, 180 г/м², сертификат ОЕКО-ТЕХ 100» |
| «популярный товар» | «1 240 заказов за 90 дней, 4.7/5 по 86 отзывам» |

Every number has a source: supplier card, marketplace analytics, internal ledger. If a value is
unknown, write «неизвестно» and name what was attempted. Never turn unknown into zero.

## 4. Tables and definition lists

LLM parsers extract `<table>` and `<dl>` with high weight. Every product page has:

- a specification table (attribute → value → unit → source);
- a price explanation table (purchase, delivery, commission, tax, margin → final price);
- a `<dl>` for short facts: SKU, GTIN, brand, country, warranty, availability.

Multilingual and marketplace pages reuse the same tables, translated with a reviewed glossary.

## 5. Trust citations

Explicit links to primary sources increase the probability of citation. Link to:

- manufacturer / supplier product page;
- official standard or certificate register;
- official marketplace category rules;
- government registers where relevant.

Mark the link type (`primary`, `mirror`, `internal`) so an answer engine can see that we are a
secondary validator, not the original source.

## 6. Entity disambiguation

An entity is consistent when name, address, phone and coordinates (NAP) match across our site,
Google Business Profile, OpenStreetMap and aggregators. For products: keep SKU, GTIN, brand and
canonical URL identical across storefront, marketplace feeds and WordPress sites. A mismatch
reduces trust, so identity fields come from the canonical catalogue, never retyped per channel.

## 7. Gates

1. `answer_first` — the first 300 characters under H1 contain at least three concrete facts
   (number, currency, date, unit or identifier).
2. `chunk_size` — no content block over 2000 characters without a heading.
3. `tables` — at least one spec table and one `<dl>` on a product page.
4. `citations` — at least one `primary` source link.
5. `entity_consistency` — SKU/GTIN/URL match the canonical catalogue record.
6. `crawler_view` — all of the above present in raw HTML without JavaScript.

## 8. Where it lives in code

- `tools/aeo_lint.py` — static gate for generated wiki pages and sample HTML.
- `specs/003-storefront/spec.md` — product-page acceptance criteria.
- `tools/build_knowledge.py` — generated wiki index carries an Answer-First lead.
