---
id: "format-woocommerceformat"
title: "Как выгрузить товары в WooCommerce?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/woocommerceformat
confidence: "measured"
updated: "2026-11-27"
---

# Как выгрузить товары в WooCommerce?

**Category:** `cms` · **Target:** WooCommerce
**Source:** https://q-parser.ru/howto/format/woocommerceformat

Выгрузка товаров производится в формате CSV для модуля [Product CSV Importer and Exporter](https://docs.woocommerce.com/document/product-csv-importer-exporter/).

Подробную информацию о модуле вы можете получить на странице модуля в документации WooCommerce.

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары в WooCommerce - Шаг 1](/static/howto/export-1.png)

### 2. Задайте настройки формата

В появившемся окне выберите формат "WooCommerce (CSV)", задайте необходимые настройки и сформируйте файл для импорта товаров.

### 3. Перейдите в Import WooCommerce

В панели управления перейдите в раздел **WooCommerce > Products**, выберите **Import** в верхнем меню.

![Как выгрузить товары в WooCommerce - Шаг 3](/_app/immutable/assets/export-woocommerce-2.1euMqwZY.png)

### 4. Загрузите файл в импортер

На странице импорта щелкните на поле загрузки файла и выберите выгруженный файл с товарами. Нажмите "Продолжить".

Если требуется обновить уже существующие товары по Артикулу, поставьте соответствующую галочку на этом экране.

![Как выгрузить товары в WooCommerce - Шаг 4](/_app/immutable/assets/export-woocommerce-3.BYLfIaIY.png)

### 5. Запустите импорт

После загрузки файла появится страница сопоставления колонок в файле и колонок импорта. Вы можете изменить соотношение колонок, если
это требуется. Затем нажмите "Продолжить" и запустите импорт. Дождитесь завершения импорта, чтобы убедиться, что все товары
загружены на сайт.

![Как выгрузить товары в WooCommerce - Шаг 5](/_app/immutable/assets/export-woocommerce-4.CB8vmhJR.png)

![Как выгрузить товары в WooCommerce - Шаг 6](/_app/immutable/assets/export-woocommerce-5.DT3E5fPt.png)

![Как выгрузить товары в WooCommerce - Шаг 7](/_app/immutable/assets/export-woocommerce-6.D8nZjex7.png)

## Настройки формата

**Тип атрибутов** — позволяет задать локальный или глобальный тип выгружаемых атрибутов.

**Расположение атрибутов** — расположить атрибуты товаров подряд или каждый в своей колонке (не перемешивая).

**Обрезать имена атрибутов до 28 символов** — по умолчанию включено: названия характеристик в CSV ограничиваются 28 символами,
как ожидает типичный импорт WooCommerce. Если отключить опцию, в файл попадут полные названия (удобно для ручной правки или других сценариев;
учитывайте возможные ограничения импортёра на стороне магазина).

## Специальные характеристики

Часть колонок заполняется значением характеристики с фиксированным названием. Если у товара такой характеристики нет, колонка
останется пустой. Эти характеристики не дублируются в атрибутах: туда попадают остальные.

**tax:product\_brand** — характеристика «Бренд».

**Weight (unit)** — характеристика «Вес».

**Length (unit)** — характеристика «Длина».

**Width (unit)** — характеристика «Ширина».

**Height (unit)** — характеристика «Высота».

Название должно совпадать точно. Переименовать характеристику можно в [редактировании товаров](/howto/mods/cols-rename).

## Extracted settings

- Height (unit)
- Import
- Length (unit)
- Weight (unit)
- Width (unit)
- WooCommerce > Products
- tax:product\_brand
- Обрезать имена атрибутов до 28 символов
- Расположение атрибутов
- Тип атрибутов

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
