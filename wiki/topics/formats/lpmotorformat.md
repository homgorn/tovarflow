---
id: "format-lpmotorformat"
title: "Как выгрузить товары для LPmotor (lpmotor.ru)?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/lpmotorformat
confidence: "measured"
updated: "2026-11-27"
---

# Как выгрузить товары для LPmotor (lpmotor.ru)?

**Category:** `cms` · **Target:** LPmotor (lpmotor.ru)
**Source:** https://q-parser.ru/howto/format/lpmotorformat

### 1. Выгрузите товары

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить". В появившемся окне выберите
формат "LPmotor (CSV)" и задайте нужные настройки формата.

Появится индикатор выгрузки товаров. Если не хотите ждать, вы можете выключить компьютер или закрыть браузер — выгрузка
продолжится независимо от вас.

По окончании выгрузки вы увидите ссылку на скачивание файла. Если будет сформировано несколько файлов, появится список ссылок.

![Как выгрузить товары на LPmotor - Шаг 1](/static/howto/export-1.png)

### 2. Импортируйте файл в LPmotor

Перейдите в панель управления магазина LPmotor, в раздел **Товары**.

В правом меню выберите **Загрузить товары из CSV, YML**.

Загрузите файл и следуйте инструкциям импорта. Подробная инструкция по импорту [доступна по ссылке](https://help.lpmotor.ru/article/4957).

![Как выгрузить товары на LPmotor - Шаг 2](/_app/immutable/assets/export-lpmotor-1.DvPrULpo.png)

![Как выгрузить товары на LPmotor - Шаг 2](/_app/immutable/assets/export-lpmotor-2.C0d1UanQ.png)

## Особенности формата

id товаров в файле формируются на основе Артикула и URL товара.

Вы можете вручную удалить id из файла, если они мешают или пересекаются вам, но в этом случае перестанет работать импорт вариантов
товаров.

## Extracted settings

- Загрузить товары из CSV, YML
- Товары

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
