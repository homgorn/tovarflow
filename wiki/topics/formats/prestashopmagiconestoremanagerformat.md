---
id: "format-prestashopmagiconestoremanagerformat"
title: "Как выгрузить товары в PrestaShop MagicOne Store Manager?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/prestashopmagiconestoremanagerformat
confidence: "measured"
updated: "2026-11-22"
---

# Как выгрузить товары в PrestaShop MagicOne Store Manager?

**Category:** `cms` · **Target:** PrestaShop MagicOne Store Manager
**Source:** https://q-parser.ru/howto/format/prestashopmagiconestoremanagerformat

Подробную информацию о процессе импорта вы можете получить на [сайте приложения](https://www.prestashopmanager.com).

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары в PrestaShop MagicOne Store Manager - Шаг 1](/static/howto/export-1.png)

### 2. Задайте настройки формата

В появившемся окне выберите формат "PrestaShop MagicOne Store Manager", задайте необходимые настройки и сформируйте файлы для
импорта товаров.

### 3. Перейдите в приложение PrestaShop MagicOne Store Manager

Импортируйте файлы с товарами согласно настройкам вашего интернет-магазина и потребностям.

## Специальные характеристики

Часть колонок заполняется значением характеристики с фиксированным названием. Если у товара такой характеристики нет, колонка
останется пустой.

**Бренд** и **Производитель** — характеристика «Бренд».

Название должно совпадать точно. Переименовать характеристику можно в [редактировании товаров](/howto/mods/cols-rename).

## Extracted settings

- Бренд
- Производитель

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
