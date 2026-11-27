---
id: "format-xmlformat"
title: "Как выгрузить товары в XML?"
tags:
  - qparser
  - format
  - file
sources:
  - https://q-parser.ru/howto/format/xmlformat
confidence: "measured"
updated: "2026-11-27"
---

# Как выгрузить товары в XML?

**Category:** `file` · **Target:** XML
**Source:** https://q-parser.ru/howto/format/xmlformat

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары в XML - Шаг 1](/static/howto/export-1.png)

### 2. Задайте настройки файла

В появившемся окне выберите формат "XML" и задайте настройки формата.

Обратите внимание, что для выгрузки в Яндекс.Маркет используется [отдельный формат](/howto/format/ymlformat).

Подробное описание каждой настройки вы можете найти ниже на этой странице.

### 3. Выгрузка запущена

Появится индикатор выгрузки товаров. Если не хотите ждать, вы можете выключить компьютер или закрыть браузер — выгрузка
продолжится независимо от вас.

По окончании выгрузки вы увидите ссылку на скачивание файла XML. Если будет сформировано несколько файлов, появится список ссылок.

### Обратите внимание

Выгрузка в XML - это не то же самое, что выгрузка в YML. Это разные форматы, они не совместимы между собой.

## Extracted settings

- (no bold settings detected)

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
