---
id: "format-advantshopv1format"
title: "Как выгрузить товары в Advantshop 1.0?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/advantshopv1format
confidence: "measured"
updated: "2026-11-27"
---

# Как выгрузить товары в Advantshop 1.0?

**Category:** `cms` · **Target:** Advantshop 1.0
**Source:** https://q-parser.ru/howto/format/advantshopv1format

Список товаров на Advantshop выгружается в формате CSV для версии импорта Advantshop v1.0. Файл уже подготовлен для импорта на
платформу Advantshop, дополнительных манипуляций не требуется.

[Нужна версия 2.0?](/howto/format/advantshopv2format)

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары в Advantshop - Шаг 1](/static/howto/export-1.png)

### 2. Задайте настройки формата

В появившемся окне выберите формат "Advantshop 1.0 (advantshop.net)", задайте необходимые настройки и сформируйте файл для импорта
товаров.

### 3. Перейдите в раздел "Импорт данных" в вашем Advantshop

В панели управления вашего магазина Advantshop перейдите в раздел "Товары", затем "Импорт данных".

![Как выгрузить товары в Advantshop - Шаг 3](/_app/immutable/assets/export-advantshopv1-2.BXTLb4bI.png)

### 4. Задайте настройки импорта

Задайте настройки импорта в соответствии с настройками выгрузки. Обычно требуется только **выбрать версию импорта**, остальные
параметры работают по умолчанию.

В разделе "Csv файл каталога товаров" обязательно укажите формат файла "AdvantShop 1.0".

Может потребоваться указать кодировку файла.

![Как выгрузить товары в Advantshop - Шаг 4](/_app/immutable/assets/export-advantshopv1-3.2hwreoeu.png)

### 5. Загрузите файлы из Q-Parser и запустите импорт

- Загрузите файл с товарами с диска (скачав его).
- Если вы выгружали фото в ZIP-архив, также скачайте архив и загрузите его в панель управления сайтом.
- Нажмите «Импортировать» в правой части панели и дождитесь импорта товаров.

![Как выгрузить товары в Advantshop - Шаг 5](/_app/immutable/assets/export-advantshopv1-4.DKX1cI5r.png)

Актуальную инструкцию по импорту товаров всегда можно найти в [документация Advantshop](https://www.advantshop.net/help/pages/import-csv).

## Специальные характеристики

Часть колонок заполняется значением характеристики с фиксированным названием. Если у товара такой характеристики нет, колонка
останется пустой. Эти характеристики не дублируются в колонке **properties**: туда попадают остальные.

**producer** — характеристика «Бренд».

**weight** — характеристика «Вес».

**barcode** — характеристика «Штрихкод».

**sku:size:color:price:purchaseprice:amount** — характеристики «Размер» и «Цвет» (размер и цвет варианта в одной колонке).

Название должно совпадать точно. Переименовать характеристику можно в [редактировании товаров](/howto/mods/cols-rename).

## Extracted settings

- barcode
- producer
- properties
- sku:size:color:price:purchaseprice:amount
- weight
- выбрать версию импорта

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
