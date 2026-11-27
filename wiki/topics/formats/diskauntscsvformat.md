---
id: "format-diskauntscsvformat"
title: "Как выгрузить товары на маркетплейс Diskaunts?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/diskauntscsvformat
confidence: "measured"
updated: "2026-11-27"
---

# Как выгрузить товары на маркетплейс Diskaunts?

**Category:** `cms` · **Target:** маркетплейс Diskaunts
**Source:** https://q-parser.ru/howto/format/diskauntscsvformat

Список товаров на Diskaunts выгружается в формате CSV. Файл уже подготовлен для импорта на платформу Diskaunts, дополнительных
манипуляций не требуется.

Рекомендуем импортировать за один раз не более 10 000 товаров.

**Важно.** Категории товаров необходимо создавать вручную до импорта файла.

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары в Diskaunts - Шаг 1](/static/howto/export-1.png)

### 2. Задайте настройки формата

В появившемся окне выберите формат "Diskaunts CSV (diskaunts.net)", задайте необходимые настройки и сформируйте файл для импорта
товаров.

### 3. Перейдите в раздел [Массовая загрузка товаров](https://diskaunts.net/vendor/products/import)

В панели управления вашего магазина Diskaunts перейдите в раздел **Массовая загрузка товаров**.

Загрузите файл или укажите ссылку на него и нажмите кнопку Начать импорт. Далее следуйте инструкциям на экране.

![Как выгрузить товары в Diskaunts - Шаг 3](/_app/immutable/assets/export-diskaunts-2.DR5k3Kp1.png)

## Специальные характеристики

Часть колонок заполняется значением характеристики с фиксированным названием. Если у товара такой характеристики нет, колонка
останется пустой. Эти характеристики не дублируются в колонках характеристик: туда попадают остальные.

**color** — характеристика «Цвет».

Название должно совпадать точно. Переименовать характеристику можно в [редактировании товаров](/howto/mods/cols-rename).

## Extracted settings

- color
- Важно.
- Массовая загрузка товаров

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
