---
id: "format-opencartcsvpriceproformat"
title: "Как выгрузить товары для OpenCart в формате CSV Price Pro?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/opencartcsvpriceproformat
confidence: "measured"
updated: "2026-11-22"
---

# Как выгрузить товары для OpenCart в формате CSV Price Pro?

**Category:** `cms` · **Target:** OpenCart в формате CSV Price Pro
**Source:** https://q-parser.ru/howto/format/opencartcsvpriceproformat

Список товаров для OpenCart в формате CSV Price Pro выгружается в формате CSV. Файл уже подготовлен для импорта на платформу
OpenCart, дополнительных манипуляций не требуется.

Для использования данного формата импорта у вас должно быть установлено расширение CSV Price Pro import/export.

**Важно.** Для того, что бы скачать изображения по ссылке, нужно включить настройку **Докачка изображений**.

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары в CSV Price Pro - Шаг 1](/static/howto/export-1.png)

### 2. Задайте настройки формата

В появившемся окне выберите формат "OpenCart CSV Price Pro", задайте необходимые настройки и сформируйте файл для импорта товаров.

### 3. Импортируйте товары

В панели управления вашего магазина перейдите в раздел **Товары > Импорт** расширения CSV Price Pro.

Загрузите файл, выберите ключевое поле **\_SKU\_**, задайте необходимые настройки и запустите импорт. Далее следуйте инструкциям на
экране.

## Специальные характеристики

Часть колонок заполняется значением характеристики с фиксированным названием. Если у товара такой характеристики нет, колонка
останется пустой. Эти характеристики не дублируются в **\_ATTRIBUTES\_**: туда попадают остальные.

**\_MANUFACTURER\_** — характеристика «Бренд».

**\_MODEL\_** — характеристика «Модель».

**\_WEIGHT\_** — характеристика «Вес».

**\_LENGTH\_** — характеристика «Длина».

**\_WIDTH\_** — характеристика «Ширина».

**\_HEIGHT\_** — характеристика «Высота».

**\_ISBN\_** — характеристика «ISBN».

Название должно совпадать точно. Переименовать характеристику можно в [редактировании товаров](/howto/mods/cols-rename).

## Extracted settings

- \_ATTRIBUTES\_
- \_HEIGHT\_
- \_ISBN\_
- \_LENGTH\_
- \_MANUFACTURER\_
- \_MODEL\_
- \_SKU\_
- \_WEIGHT\_
- \_WIDTH\_
- Важно.
- Докачка изображений
- Товары > Импорт

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
