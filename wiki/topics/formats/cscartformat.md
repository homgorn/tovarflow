---
id: "format-cscartformat"
title: "Как выгрузить товары на CS-Cart?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/cscartformat
confidence: "measured"
updated: "2026-11-22"
---

# Как выгрузить товары на CS-Cart?

**Category:** `cms` · **Target:** CS-Cart
**Source:** https://q-parser.ru/howto/format/cscartformat

### 1. Выгрузите товары

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить". В появившемся окне выберите
формат "CS-Cart (cs-cart.ru)" и задайте нужные настройки формата.

Появится индикатор выгрузки товаров. Если не хотите ждать, вы можете выключить компьютер или закрыть браузер — выгрузка
продолжится независимо от вас.

По окончании выгрузки вы увидите ссылку на скачивание файла. Если будет сформировано несколько файлов, появится список ссылок.

![Как выгрузить товары на CS-Cart - Шаг 1](/static/howto/export-1.png)

### 2. Импортируйте файл в CS-Cart

Перейдите в панель управления магазина CS-Cart, в раздел **Администрирование > Импорт данных > Товары**.

Нажмите на кнопку **+** чтобы добавить пресет импорта, выберите CSV файл.

Перейдите на вкладку **Таблица соответствия полей** и укажите как должен обрабатываться файл.

Разделитель категорий — **///**

Разделитель изображений — **///**

В случае импорта изображений в виде файлов необходимо самостоятельно загрузить скачанные фото на сервер и при импорте указать папку
для изображений.

Загрузите файл и следуйте инструкциям импорта. Подробная инструкция по импорту [доступна по ссылке](https://www.cs-cart.ru/docs/4.14.x/user_guide/import_export/).

![Как выгрузить товары на CS-Cart - Шаг 2](/_app/immutable/assets/export-cscart-2.C3feJCd2.jpg)

![Как выгрузить товары на CS-Cart - Шаг 3](/_app/immutable/assets/export-cscart-3.CczUgEXM.jpg)

## Особенности формата

Файл создается для версии CS-Cart 4.14.x (скорее всего, будет работать и в других версиях)

## Настройки формата

**Язык товаров** — задает значение поля [Language](https://www.cs-cart.ru/docs/4.14.x/user_guide/manage_products/import_export/fields_format.html#language).

**Product code** — задает способ формирования поля [Product code](https://www.cs-cart.ru/docs/4.14.x/user_guide/manage_products/import_export/fields_format.html#product-code). Обратите внимание, что код не может быть больше 32 символов и имеет ограничения по набору символов.

## Extracted settings

- 

Разделитель изображений — 
-  и укажите как должен обрабатываться файл.

Разделитель категорий — 
-  чтобы добавить пресет импорта, выберите CSV файл.

Перейдите на вкладку 
- Product code
- Администрирование > Импорт данных > Товары
- Язык товаров

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
