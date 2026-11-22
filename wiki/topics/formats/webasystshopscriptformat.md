---
id: "format-webasystshopscriptformat"
title: "Как выгрузить товары в Webasyst Shop-Script?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/webasystshopscriptformat
confidence: "measured"
updated: "2026-11-22"
---

# Как выгрузить товары в Webasyst Shop-Script?

**Category:** `cms` · **Target:** Webasyst Shop-Script
**Source:** https://q-parser.ru/howto/format/webasystshopscriptformat

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары в Webasyst Shop-Script - Шаг 1](/static/howto/export-1.png)

### 2. Задайте настройки формата

В появившемся окне выберите формат "Webasyst Shop-Script". Там же можно выбрать дополнительные настройки, например, кодировку файла.

### 3. Загрузите файл в Webasyst

Перейдите в панель управления вашим магазином в Webasyst, затем в разделе "Магазин" выберите "Импорт/Экспорт".

Настройки кодировки файла и разделителей CSV можно оставить по умолчанию, Q-Parser выгружает товары для Webasyst сразу в нужном
формате.

Щелкните на поле для файла и выберите CSV-файл с товарами, либо перетащите его на поле загрузки.

![Как выгрузить товары в Webasyst Shop-Script - Шаг 3](/_app/immutable/assets/export-webasystss-2.B1g8qmev.png)

### 4. Настройте колонки и запустите импорт

После выбора файла и его загрузки появится таблица, в которой необходимо выбрать соответствие колонок файла характеристикам товаров.
Webasyst по умолчанию выбирает подходящие колонки, но если требуется вы можете настроить их вручную.

Настройте колонки и другие параметры импорта, затем запустите проверку импорта и появится кнопка старта импорта.

![Как выгрузить товары в Webasyst Shop-Script - Шаг 4](/_app/immutable/assets/export-webasystss-3.D7bGey11.png)

### 5. Дождитесь окончания импорта

После запуска необходимо дождаться окончания импорта. Вкладку браузера нельзя закрывать, пока импорт не закончится.

Подробное описание формата и его настроек доступно в [документации Webasyst](https://support.webasyst.ru/shop-script/26/import-products-from-csv-file/).

![Как выгрузить товары в Webasyst Shop-Script - Шаг 5](/_app/immutable/assets/export-webasystss-4.BVljG_2T.png)

## Extracted settings

- (no bold settings detected)

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
