---
id: "format-epicentrkymlformat"
title: "Как выгрузить товары на Epicentrk (epicentrk.ua) в YML?"
tags:
  - qparser
  - format
  - marketplace
sources:
  - https://q-parser.ru/howto/format/epicentrkymlformat
confidence: "measured"
updated: "2026-11-22"
---

# Как выгрузить товары на Epicentrk (epicentrk.ua) в YML?

**Category:** `marketplace` · **Target:** Epicentrk (epicentrk.ua) в YML
**Source:** https://q-parser.ru/howto/format/epicentrkymlformat

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары на Epicentrk - Шаг 1](/static/howto/export-1.png)

### 2. Задайте настройки формата

В появившемся окне выберите формат "Epicentrk YML (epicentrk.ua)" и задайте настройки формата: как выгружать характеристики и
разделять свойства.

Подробное описание каждой настройки вы можете найти ниже на этой странице.

### 3. Выгрузка запущена

Появится индикатор выгрузки товаров. Если не хотите ждать, вы можете выключить компьютер или закрыть браузер — выгрузка
продолжится независимо от вас.

По окончании выгрузки вы увидите ссылку на скачивание файла YML. Если будет сформировано несколько файлов, появится список ссылок.

### 4. Импортируйте товары в Epicentrk

Перейдите в панель управления своим магазином Epicentrk и импортируйте файл с товарами согласно актуальной инструкции.

<https://crm.epicentrk.ua/pub/site/18/yak-importuvaty-tovary/>

### Особенности формата

Язык для тегов с поддержкой атрибута lang: ua.

Товары не привязываются к категориям, поскольку категории спарсенных товаров не соответствуют категориям Epicentrk.

Характеристики товаров всегда добавляются в описание, поскольку характеристики товаров в парсинге не соответствуют справочникам
Epicentrk.

## Extracted settings

- (no bold settings detected)

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
