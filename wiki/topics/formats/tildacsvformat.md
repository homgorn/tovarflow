---
id: "format-tildacsvformat"
title: "Как выгрузить товары на Tilda (tilda.cc) в CSV?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/tildacsvformat
confidence: "measured"
updated: "2026-11-22"
---

# Как выгрузить товары на Tilda (tilda.cc) в CSV?

**Category:** `cms` · **Target:** Tilda (tilda.cc) в CSV
**Source:** https://q-parser.ru/howto/format/tildacsvformat

### 1. Выгрузите товары

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить". В появившемся окне выберите
формат "Tilda CSV (tilda.cc)" и задайте нужные настройки формата.

Появится индикатор выгрузки товаров. Если не хотите ждать, вы можете выключить компьютер или закрыть браузер — выгрузка
продолжится независимо от вас.

По окончании выгрузки вы увидите ссылку на скачивание файла. Если будет сформировано несколько файлов, появится список ссылок.

![Как выгрузить товары на Ural CMS - Шаг 1](/static/howto/export-1.png)

### 2. Импортируйте товары в Tilda

Перейдите в панель управления своим магазином Tilda, в раздел **Сайт**, **Каталог** нажмите на "три точки" и выберите импорт из
CSV. Укажите файл и запустите импорт.

![Как выгрузить товары на Tilda - Шаг 2](/_app/immutable/assets/export-tilda-yml-2.CPuskJGi.png)

## Особенности формата

Производится выгрузка категорий только первого уровня, остальные уровни категорий игнорируются.

## Extracted settings

- Каталог
- Сайт

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
