---
id: "api"
title: "Q-Parser REST API"
tags:
  - qparser
  - api
  - rest
sources:
  - https://q-parser.ru/howto/api
confidence: "measured"
updated: "2026-11-22"
---

# Q-Parser REST API

Base URL `https://q-parser.ru/api/v1`. Auth: `Authorization: Bearer <key>` or `X-Api-Key: <key>`.
Errors: `{ "error": { "code": "...", "message": "..." } }`; dates are unix milliseconds.
Source: [[sources]] · `https://q-parser.ru/howto/api`.

| # | Method | Path | Purpose |
|---|---|---|---|
| 1 | `GET` | `/api/v1/catalog` | Каталог сайтов, доступных для парсинга: поиск по названию, описанию и домену. |
| 2 | `POST` | `/api/v1/categories` | Запускает сбор категорий сайта. Если список уже есть в кэше, сразу возвращается `completed` без повторного сбора. |
| 3 | `GET` | `/api/v1/categories/:id` | Статус и результат сбора категорий. |
| 4 | `GET` | `/api/v1/credentials` | Список сохранённых логинов для сайтов, где нужна авторизация. Пароли не возвращаются. |
| 5 | `POST` | `/api/v1/credentials` | Добавляет логин и пароль. Если такая пара уже есть, пароль обновляется, `id` остаётся прежним. |
| 6 | `POST` | `/api/v1/export` | Запускает выгрузку товаров парсинга в выбранный формат. |
| 7 | `GET` | `/api/v1/export/:id` | Статус выгрузки: очередь, прогресс, файлы или ссылки результата. |
| 8 | `GET` | `/api/v1/format` | Список форматов выгрузки: идентификаторы, названия и схема опций. |
| 9 | `GET` | `/api/v1/me` | Текущий пользователь: тариф, баланс и AI Points. |
| 10 | `POST` | `/api/v1/parser` | Запускает парсинг товаров. Полноценный парсинг платного сайта — только с действующим тарифом. Пробный парсинг — с `trial: true`, доступен без тарифа. Если `categories` не передан или пустой, список категорий будет загружен автоматически |
| 11 | `GET` | `/api/v1/parser/:id` | Статус парсинга: очередь, прогресс, ошибка. |
| 12 | `GET` | `/api/v1/parser/:id/goods` | Список товаров парсинга с постраничной выдачей. |
| 13 | `POST` | `/api/v1/parser/:id/resume` | Возобновляет вручную остановленный парсинг — то же, что кнопка «Возобновить». Парсинг должен быть в статусе `canceled` и не в архиве. Успешно завершенный, завершенный с ошибкой, еще идущий или архивный парсинг возобновить нельзя: |
| 14 | `POST` | `/api/v1/parser/:id/stop` | Останавливает незавершенный парсинг — то же, что кнопка «Остановить» в интерфейсе. Парсинг в очереди или в работе переходит в статус `canceled`. Уже завершенный или уже остановленный парсинг остановить нельзя: ответ `unprocessable`. |
| 15 | `GET` | `/api/v1/parser/list` | История парсингов. |
| 16 | `GET` | `/api/v1/website/:domain` | Схема настроек парсера для сайта: нужна ли авторизация, ручные категории и какие опции передавать при запуске. |

## GET /api/v1/catalog

Каталог сайтов, доступных для парсинга: поиск по названию, описанию и домену.

**Request**

- `q` — поисковый запрос (необязательно). Можно передать домен или URL
- `free=1` — только сайты с бесплатным парсингом
- `limit` — размер страницы, по умолчанию 100, максимум 1000
- `offset` — смещение, по умолчанию 0

**Response**

- `total` — всего сайтов по фильтру
- `limit`, `offset` — фактическая пагинация
- `list` — массив: `domain`, `title`, `slug` (страница в каталоге), `private`, `free_until` (unix ms), `categories` и `cities` — массивы `{ title, slug }`

В выдачу также попадают приватные сайты, доступные текущему пользователю. Домен из `list` передают в `GET /api/v1/website/:domain` и при запуске парсинга.

## POST /api/v1/categories

Запускает сбор категорий сайта. Если список уже есть в кэше, сразу возвращается `completed` без повторного сбора.

**Response**

- `id` — идентификатор задачи, его передают в `GET /api/v1/categories/:id`
- `status` — `running` или `completed`

## GET /api/v1/categories/:id

Статус и результат сбора категорий.

**Request**

`id` задачи из `POST /api/v1/categories`.

**Response**

- `id` — идентификатор задачи
- `status` — `running`, `completed` или `error`
- `updated` — время обновления кэша (unix ms) или `null`
- `categories` — массив `{ title, url }` или `null`, пока статус `running`

## GET /api/v1/credentials

Список сохранённых логинов для сайтов, где нужна авторизация. Пароли не возвращаются.

**Request**

необязательный query-параметр `domain` — фильтр по сайту.

**Response**

объект `credentials` — массив записей:

- `id` — идентификатор записи (UUID), его передают в `credentials_id`
- `domain` — домен сайта
- `login` — логин
- `last_login` — время последней успешной авторизации (unix ms) или `null`

## POST /api/v1/credentials

Добавляет логин и пароль. Если такая пара уже есть, пароль обновляется, `id` остаётся прежним.

**Response**

`id`, `login`, `domain`.

## POST /api/v1/export

Запускает выгрузку товаров парсинга в выбранный формат.

**Response**

`id` выгрузки (UUID).

## GET /api/v1/export/:id

Статус выгрузки: очередь, прогресс, файлы или ссылки результата.

**Request**

`id` в пути — UUID выгрузки из `POST /api/v1/export`.

**Response**

- `id` — идентификатор выгрузки
- `status` — `queued`, `running`, `completed`, `canceled` или `error`
- `parser_id` — id парсинга
- `format` — id формата
- `goods_exported` — сколько товаров уже обработано
- `created` — время создания (unix ms)
- `finished` — время завершения (unix ms) или `null`
- `error` — текст ошибки или `null`
- `message` — сообщение результата или `null`
- `files` — массив ссылок на файлы выгрузки (может быть пустым)
- `links` — массив `{ title, url }` (может быть пустым)
- `progress` — `{ current, max, message }` во время работы или `null`

## GET /api/v1/format

Список форматов выгрузки: идентификаторы, названия и схема опций.

**Response**

объект `formats` — массив записей:

- `id` — идентификатор формата, его передают в `POST /api/v1/export`
- `title` — название формата
- `options` — объект опций (может быть пустым). Ключ опции передаётся в `options` при запуске выгрузки.
  Каждая опция: `title`, `type`, `values` — массив `{ key, label }`. Для выбора обычно берут `key` первого элемента `values`

## GET /api/v1/me

Текущий пользователь: тариф, баланс и AI Points.

**Response**

- `email` — email пользователя
- `tariff_id` — идентификатор тарифа
- `tariff_until` — срок действия тарифа (unix ms)
- `balance` — баланс в рублях
- `ai_points` — баланс AI Points

## POST /api/v1/parser

Запускает парсинг товаров. Полноценный парсинг платного сайта — только с действующим тарифом. Пробный парсинг — с `trial: true`, доступен без тарифа. Если `categories` не передан или пустой, список категорий будет загружен автоматически

**Response**

`id` парсинга в виде `id1234567`.

## GET /api/v1/parser/:id

Статус парсинга: очередь, прогресс, ошибка.

**Request**

`id` в пути — полный id парсинга, например `id1234567`.

**Response**

- `id` — идентификатор парсинга
- `status` — `queued`, `running`, `completed`, `canceled` или `error`
- `domain` — домен сайта
- `goods_processed` — сколько товаров уже спарсено
- `goods_limited` — лимит товаров по тарифу или `null`
- `categories_total` — всего категорий в задании
- `categories_processed` — сколько категорий уже обработано
- `created` — время создания (unix ms)
- `finished` — время завершения (unix ms) или `null`
- `archive` — архивный парсинг
- `error` — текст ошибки или `null`

## GET /api/v1/parser/:id/goods

Список товаров парсинга с постраничной выдачей.

**Request**

- `id` в пути — полный id парсинга, например `id1234567`
- `limit` — размер страницы, по умолчанию 100, максимум 1000
- `offset` — смещение, по умолчанию 0

**Response**

- `total` — всего товаров
- `limit`, `offset` — фактическая пагинация
- `goods` — массив товаров: `title`, `article`, `url`, `price`, `old_price`, `currency`, `brand`, `quantity`, `publish` (наличие, `true` / `false` / `null`), `images`, `file_links`, `video_links` (массивы ссылок), `category_title`, `category_url`, `description`, `short_description`, `data` — дополнительные характеристики с человекочитаемыми ключами

## POST /api/v1/parser/:id/resume

Возобновляет вручную остановленный парсинг — то же, что кнопка «Возобновить». Парсинг должен быть в статусе `canceled` и не в архиве. Успешно завершенный, завершенный с ошибкой, еще идущий или архивный парсинг возобновить нельзя:

**Request**

`id` в пути — полный id парсинга, например `id1234567`. Тело запроса не нужно.

**Response**

тот же объект, что у `GET /api/v1/parser/:id`. После возобновления `status` — `queued` или `running`.

## POST /api/v1/parser/:id/stop

Останавливает незавершенный парсинг — то же, что кнопка «Остановить» в интерфейсе. Парсинг в очереди или в работе переходит в статус `canceled`. Уже завершенный или уже остановленный парсинг остановить нельзя: ответ `unprocessable`.

**Request**

`id` в пути — полный id парсинга, например `id1234567`. Тело запроса не нужно.

**Response**

тот же объект, что у `GET /api/v1/parser/:id`. После остановки `status` — `canceled`.

## GET /api/v1/parser/list

История парсингов.

**Request**

- `limit` — размер страницы, по умолчанию 100, максимум 1000
- `offset` — смещение, по умолчанию 0

**Response**

- `total` — всего парсингов
- `limit`, `offset` — фактическая пагинация
- `list` — массив: `id`, `domain`, `status` (`queued`, `running`, `completed`, `canceled`, `error`), `goods_processed`, `goods_limited`, `categories_total`, `categories_processed`, `created`, `finished` (unix ms, `finished` может быть `null`), `archive`

## GET /api/v1/website/:domain

Схема настроек парсера для сайта: нужна ли авторизация, ручные категории и какие опции передавать при запуске.

**Request**

`domain` в пути (например `example.com`).

**Response**

- `domain` — канонический домен
- `protocol` — `http` или `https`
- `auth_required` — нужна ли авторизация на сайте
- `manual_categories` — нужно ли передавать категории вручную
- `options` — объект опций (может быть пустым). Ключ опции передаётся в `options` при запуске парсинга
  категорий или товаров. Типы: `select`, `input`, `file`, `text`, `html`, `vkcom`, `okru`
