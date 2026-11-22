---
id: "format-uralcmscsvformat"
title: "Как выгрузить товары для Ural CMS (uralcms.ru)?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/uralcmscsvformat
confidence: "measured"
updated: "2026-11-22"
---

# Как выгрузить товары для Ural CMS (uralcms.ru)?

**Category:** `cms` · **Target:** Ural CMS (uralcms.ru)
**Source:** https://q-parser.ru/howto/format/uralcmscsvformat

### 1. Выгрузите товары

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить". В появившемся окне выберите
формат "Ural CMS (CSV)" и задайте нужные настройки формата.

Появится индикатор выгрузки товаров. Если не хотите ждать, вы можете выключить компьютер или закрыть браузер — выгрузка
продолжится независимо от вас.

По окончании выгрузки вы увидите ссылку на скачивание файла. Если будет сформировано несколько файлов, появится список ссылок.

![Как выгрузить товары на Ural CMS - Шаг 1](/static/howto/export-1.png)

### 2. Импортируйте файл в Ural CMS

Перейдите в панель управления магазина Ural CMS, в раздел **Структура и содержание**, затем **Интернет-магазин**.

В правом меню выберите **Импорт / экспорт позиций** и затем **Импорт из файла CSV**.

Загрузите файл и следуйте инструкциям импорта. Подробная инструкция по импорту [доступна по ссылке](https://uralcms.ru/instruction/structure/shop/settings/csv/#import).

![Как выгрузить товары на Ural CMS - Шаг 2](/_app/immutable/assets/export-uralcmscsv-1.CundlhHm.png)

![Как выгрузить товары на Ural CMS - Шаг 2](/_app/immutable/assets/export-uralcmscsv-2.Df70lxZk.png)

![Как выгрузить товары на Ural CMS - Шаг 2](/_app/immutable/assets/export-uralcmscsv-3.hO-6yCvp.png)

## Особенности формата

По умолчанию Ural CMS импортирует все товары в категорию неразобранных товаров.

Формат импорта Ural CMS поддерживает только основные данные товара. Все характеристики полностью игнорируются.

## Extracted settings

- Импорт / экспорт позиций
- Импорт из файла CSV
- Интернет-магазин
- Структура и содержание

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
