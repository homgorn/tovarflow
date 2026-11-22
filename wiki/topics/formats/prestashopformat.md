---
id: "format-prestashopformat"
title: "Как выгрузить товары в PrestaShop?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/prestashopformat
confidence: "measured"
updated: "2026-11-22"
---

# Как выгрузить товары в PrestaShop?

**Category:** `cms` · **Target:** PrestaShop
**Source:** https://q-parser.ru/howto/format/prestashopformat

Подробную информацию о процессе импорта вы можете получить в [документации PrestaShop](http://doc.prestashop.com/display/PS17/Import).

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары в PrestaShop - Шаг 1](/static/howto/export-1.png)

### 2. Задайте настройки формата

В появившемся окне выберите формат "PrestaShop (CSV)", задайте необходимые настройки и сформируйте файлы для импорта товаров.

### 3. Перейдите в Импорт PrestaShop

В панели управления PrestaShop перейдите в раздел **Расширенные параметры > Импорт**.

Загрузите файлы в следующей последовательности, выбирая при импорте соответствующий тип данных:

- Категории, файл *categories*;
- Бренды, файл *manufacturers*;
- Товары, файл *без постфикса*;
- Комбинации, файл *combinations*;

**Обратите внимание**, что файлов с брендами и комбинациями может не быть, если в парсинге нет этих данных.

Вы можете задать дополнительные настройки при импорте товаров в PrestaShop при необходимости.

![Как выгрузить товары в PrestaShop - Шаг 3](/_app/immutable/assets/export-prestashop-2.DV9467kF.png)

## Настройки формата

**Формат Feature** — позволяет задать формат вывода колонки Feature. Разные версии PrestaShop поддерживают разные форматы.

## Специальные характеристики

Часть колонок заполняется значением характеристики с фиксированным названием. Если у товара такой характеристики нет, колонка
останется пустой. Эти характеристики не дублируются в колонке **Feature**: туда попадают остальные.

**Manufacturer** — характеристика «Бренд».

**Width** — характеристика «Ширина».

**Height** — характеристика «Высота».

**Depth** — характеристика «Глубина».

**Weight** — характеристика «Вес».

Название должно совпадать точно. Переименовать характеристику можно в [редактировании товаров](/howto/mods/cols-rename).

## Extracted settings

- Depth
- Feature
- Height
- Manufacturer
- Weight
- Width
- Обратите внимание
- Расширенные параметры > Импорт
- Формат Feature

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
