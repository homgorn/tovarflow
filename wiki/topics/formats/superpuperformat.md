---
id: "format-superpuperformat"
title: "Как выгрузить товары на сайт SuperPuper.ru?"
tags:
  - qparser
  - format
  - sp
sources:
  - https://q-parser.ru/howto/format/superpuperformat
confidence: "measured"
updated: "2026-11-27"
---

# Как выгрузить товары на сайт SuperPuper.ru?

**Category:** `sp` · **Target:** сайт SuperPuper.ru
**Source:** https://q-parser.ru/howto/format/superpuperformat

Формат файла для импорта товаров на [SuperPuper.ru](https://superpuper.ru/).

## Специальные характеристики

Часть колонок заполняется значением характеристики с фиксированным названием. Если у товара такой характеристики нет, колонка
останется пустой. Эти характеристики не дублируются в описании: туда попадают остальные.

**Размер** — характеристика «Размер».

Название должно совпадать точно. Переименовать характеристику можно в [редактировании товаров](/howto/mods/cols-rename).

## Extracted settings

- Размер

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
