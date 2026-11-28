# Developer worklog — TovarFlow

Пошаговый журнал разработки для показа клиенту. Каждая запись: что сделано, какая проверка,
источник и уверенность 0–10. Обновляется по чанкам; старые записи не удаляются.

## 2026-11-22 — Фундамент

**MEASURED, 10/10.** Снят полный корпус документации Q-Parser: 128/128 канонических страниц,
442 579 символов, 0 пропусков. Извлечено 16 REST-эндпоинтов, 72 формата, 4 тарифа, 15 фактов с
URL и датой. Построены `data/qparser.sqlite` (826 чанков + FTS5), граф 334/293, вики из 89
страниц. Проверка: `python tools/verify_coverage.py` → 128/128.

Источник: `https://q-parser.ru/howto/api`, `docs/research/qparser/COVERAGE.md`.

## 2026-11-22 — Рисерч

**MEASURED 8/10, INFERRED 7/10.** Шесть параллельных треков: конкуренты (33 вендора), RU (6
платформ), CN (11), global (16), платформы витрин (11), спрос. Позже добавлены WordPress и
админка. Решения: Medusa v2 (81/100), RU-first, CN supply-first, Google Merchant первым из
глобальных, WordPress через отдельные инсталлы + MainWP. Источники: `docs/research/**/REPORT.md`.

## 2026-11-27 — Имя, сайт, публикация

**MEASURED 8/10.** Выбрано имя TovarFlow (`tovarflow.ru`, `tovarflow.com` свободны по WHOIS дважды;
Wayback без снимков; Google точный запрос — без релевантных упоминаний; Яндекс заблокирован
капчей — проверка неполная). Сайт RU/EN на Cloudflare Workers, `llms.txt`, sitemap, `.md`-двойники,
CSP. Репозиторий `https://github.com/homgorn/tovarflow`. Источник: `docs/naming/data.json`, ADR-0007.

## 2026-11-28 — Живой инжест npopt.ru

**MEASURED 10/10.** Ключ из `.env`, эндпоинт `GET /catalog?q=npopt` → `npopt.ru`. Парсинг
`id4048511` завершён: 973 товара, 200 загружено в канонический каталог. Обнаружено 200 товаров без
бренда; в YML подставляется название поставщика с записью `fallback_vendors: 200`. Фид валиден на
300 офферов. Проверка: `python tools/ingest.py --domain npopt.ru --parse-id id4048511`,
`python tools/feed_yml.py`.

## 2026-11-28 — Админка, чанк 1

**MEASURED 10/10.** `tools/admin.py`: дашборд, экран маппинга, очередь ценовых предложений.
Одобрение пишет `approval_event` с `idempotency_key`; повтор не дублирует событие. Проверка:
`python tools/test_admin.py` → PASS.

## 2026-11-29 — Исполнение и сверка

**MEASURED 10/10.** `tools/executor.py`: 2 одобренных предложения исполнены и верифицированы
чтением (2/2 OK), повтор → 2 idempotent-skips. В админке `/executions` и `/reconciliation`.
Находка: 400 сырых записей = 300 уникальных SKU + 100 дублей между запусками; добавлен отдельный
код причины `duplicates`, невязка 0. Коммиты `75f75f8`, `949ec8f`.

## 2026-11-29 — Ozon L2

**MEASURED 10/10.** Создан адаптерный слой `connectors/kernel` (ошибки, capability profile,
HTTP с rate limiter, idempotency и raw capture) и `connectors/ru/ozon` (профиль + адаптер).
Имена эндпоинтов из официальной OpenAPI-спеки Ozon (482 пути) и из `docs/research/marketplaces/ru`.
Контрактный тест `tools/contract_ozon.py` — **8/8**: профиль, health, запись цены и чтение назад,
идемпотентный повтор, локальная валидация, блокировка HTTP при ошибке, 401 → AuthError, rethrow
после 429. `executor --connector ozon` применил 3 новых одобренных предложения через адаптер,
2 уже исполненных пропустил; повторный запуск — 5 skips, 0 дублей.

Источник: `data/ozon_contract_report.json`, `H:/susa ai 500/wb china/ozon-seller-api-openapi.json`.

## Что не проверено

- Реальный аккаунт Ozon: нет продавцовского кабинета, все тесты на эмуляторе (INFERRED 6/10).
- WB: профиль и 13 спецификаций есть, адаптера ещё нет.
- WordPress sync, витрина Medusa, приём заказов и возвраты — не построены.
- Юридическая проверка имени и прав на контент поставщика — не проведена.
