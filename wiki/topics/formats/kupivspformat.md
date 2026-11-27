---
id: "format-kupivspformat"
title: "Как выгрузить товары на сайт Kupivsp.ru?"
tags:
  - qparser
  - format
  - sp
sources:
  - https://q-parser.ru/howto/format/kupivspformat
confidence: "measured"
updated: "2026-11-27"
---

# Как выгрузить товары на сайт Kupivsp.ru?

**Category:** `sp` · **Target:** сайт Kupivsp.ru
**Source:** https://q-parser.ru/howto/format/kupivspformat

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары на сайт Kupivsp.ru - Шаг 1](/static/howto/export-1.png)

### 2. Перейдите в организаторскую

Зайдите на сайт Kupivsp.ru под своим логином организатора и на панели меню выберите пункт "Организаторская"

![Как выгрузить товары на сайт Kupivsp.ru - Шаг 2](/_app/immutable/assets/kupivsp-1.CBLuDxIB.png)

### 3. Загрузите файл

В списке своих каталогов найдите каталог, который хотите обновить. В поле "Обновить каталог из файла" выберите файл с товарами и
нажмите кнопку "Загрузить".

![Как выгрузить товары на сайт Kupivsp.ru - Шаг 3](/_app/immutable/assets/kupivsp-2.BlhX09OZ.png)

### 4. Настройте поля

В появившейся форме настройте колонки так, как вам необходимо импортировать товары и нажмите кнопку "Обновить". Товары импортируются
в ваш каталог.

![Как выгрузить товары на сайт Kupivsp.ru - Шаг 4](/_app/immutable/assets/kupivsp-3.CeiPHTGV.png)

### Особенности формата

Данный формат выгрузки поддерживает только следующие характеристики:

- Размер/Цвет
- Размер
- Цвет

Если характеристика называется именно так, она выгружается в отдельную колонку. Иначе - добавляется в описание товара.

## Extracted settings

- (no bold settings detected)

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
