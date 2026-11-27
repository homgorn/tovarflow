---
id: "format-shopifyformat"
title: "Как выгрузить товары на Shopify (shopify.com)?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/shopifyformat
confidence: "measured"
updated: "2026-11-27"
---

# Как выгрузить товары на Shopify (shopify.com)?

**Category:** `cms` · **Target:** Shopify (shopify.com)
**Source:** https://q-parser.ru/howto/format/shopifyformat

### 1. Выгрузите товары

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить". В появившемся окне выберите
формат "Shopify (shopify.com)" и задайте нужные настройки формата.

Появится индикатор выгрузки товаров. Если не хотите ждать, вы можете выключить компьютер или закрыть браузер — выгрузка
продолжится независимо от вас.

По окончании выгрузки вы увидите ссылку на скачивание файла. Если будет сформировано несколько файлов, появится список ссылок.

![Как выгрузить товары на Shopify - Шаг 1](/static/howto/export-1.png)

### 2. Импортируйте файл в Shopify

Перейдите в панель управления магазина Shopify, в раздел **Products**, затем **All products**, нажмите кнопку **Import**.

Загрузите файл и следуйте инструкциям импорта. Подробная инструкция по импорту [доступна по ссылке](https://help.shopify.com/en/manual/products/import-export/import-products).

Обратите внимание, что после импорта товаров Shopify не отображает результаты. Отчет приходит на почту администратора магазина.

![Как выгрузить товары на Shopify - Шаг 2](/_app/immutable/assets/export-shopify-2.D23pccy_.png)

## Особенности формата

Все вариации товаров будут иметь одинаковые характеристики, цену, наличие, остатки и фото.

Shopify поддерживает импорт ограниченного набора форматов фото (jpg, png, gif). Ссылка на фото должна быть https://

## Специальные характеристики

Часть колонок заполняется значением характеристики с фиксированным названием. Если у товара такой характеристики нет, колонка
останется пустой. Эти характеристики не дублируются в описании.

**Vendor** — характеристика «Бренд».

**Variant Barcode** — характеристика «Штрихкод».

Название должно совпадать точно. Переименовать характеристику можно в [редактировании товаров](/howto/mods/cols-rename).

## Extracted settings

- All products
- Import
- Products
- Variant Barcode
- Vendor

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
