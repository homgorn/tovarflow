# TovarFlow — supplier catalogues to storefronts and marketplaces

TovarFlow turns supplier catalogues into storefronts and marketplace feeds. The platform uses 16 documented Q-Parser API endpoints, knows 72 export formats and publishes to Ozon, Wildberries, Google Merchant and WordPress. The storefront runs on Medusa v2; the core is tenant-scoped with RLS from day one.

| Layer | Input | Output |
|---|---|---|
| Ingestion | Q-Parser API, 1688, supplier feeds | Hashed raw payloads, pagination, polling |
| Normalisation | `goods` fields and free-form `data` keys | product, variant, offer, media, attributes |
| Pricing | purchase, delivery, duty, commission, returns, tax, margin | explained price with floor and `is_complete` |
| Channels | canonical catalogue | Ozon, WB, Yandex Market, Google Merchant, WordPress |

Key numbers: 128 documentation pages, 16 endpoints, 72 formats, 100 concurrent jobs, 1000 records per page, 100 goods in the first slice.

Primary sources: https://q-parser.ru/howto/api, https://docs.ozon.ru/api/seller/, https://dev.wildberries.ru/, https://developers.google.com/merchant/api/.

<!-- aeo-content-type-fix -->
