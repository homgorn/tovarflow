---
id: "format-storelandformat"
title: "Как выгрузить товары в Storeland?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/storelandformat
confidence: "measured"
updated: "2026-11-22"
---

# Как выгрузить товары в Storeland?

**Category:** `cms` · **Target:** Storeland
**Source:** https://q-parser.ru/howto/format/storelandformat

Список товаров на Storeland выгружается в формате CSV. Файл уже подготовлен для импорта на платформу Storeland, дополнительных
манипуляций не требуется.

Storeland может загружать файлы не более 20 мегабайт за раз. Если нужно импортировать больше товаров, разбейте выгрузку на более
мелкие с помощью функции [частичной выгрузки](/howto/erange).

Актуальная инструкция всегда доступна в [документации Storeland](https://storeland.ru/about/faq#25).

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары в Storeland - Шаг 1](/static/howto/export-1.png)

### 2. Задайте настройки формата

В появившемся окне выберите формат "Storeland", задайте необходимые настройки и сформируйте файл для импорта товаров.

### 3. Импортируйте файл на Storeland

В панели уплавления Storeland перейдите во вкладку "Товары", выберите категорию "Склад", нажмите иконку "создать категорию" сверху.
После её выбора нажмите на иконку импорта прайсов и следуйте дальнейшим инструкциям системы.

После окончания импорта нажмите иконку сверху "Копировать структуру и товары из указанных категорий склада в категорию на сайте".
После этого товары появятся в категориях на сайте, вся структура категорий будет сохранена, поиск по товарам будет работать

![Как выгрузить товары в Storeland - Шаг 3](/_app/immutable/assets/export-storeland-2.C5bQzUmL.jpg)

![Как выгрузить товары в Storeland - Шаг 4](/_app/immutable/assets/export-storeland-3.Deo-uRJq.jpg)

![Как выгрузить товары в Storeland - Шаг 5](/_app/immutable/assets/export-storeland-4.D4GyvITv.jpg)

## Extracted settings

- (no bold settings detected)

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
