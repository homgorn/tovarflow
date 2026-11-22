---
id: "format-facebookxmlfeedformat"
title: "Как выгрузить товары в каталоги Facebook*?"
tags:
  - qparser
  - format
  - social
sources:
  - https://q-parser.ru/howto/format/facebookxmlfeedformat
confidence: "measured"
updated: "2026-11-22"
---

# Как выгрузить товары в каталоги Facebook*?

**Category:** `social` · **Target:** каталоги Facebook*
**Source:** https://q-parser.ru/howto/format/facebookxmlfeedformat

Выгрузка формирует ATOM XML файл для загрузки товаров [каталоги в Facebook\*](https://www.facebook.com/business/help/890714097648074). Загрузка производится в [Catalog Manager](https://www.facebook.com/products/),
официальная инструкция по импорту товаров на Facebook\* находится в [документации](https://www.facebook.com/business/help/125074381480892).

### Откройте Catalog Manager и выберите каталог

После формирования файла, скачайте его к себе на компьютер, затем откройте [Catalog Manager](https://www.facebook.com/products/) и выберите (или создайте) ваш каталог с товарами. Выгрузка производится только для каталогов вида **"Электронная коммерция"**.

В левом меню выберите "Источники данных о товарах", затем справа "Добавить товары".

![Как выгрузить товары на Facebook - Шаг 1](/_app/immutable/assets/export-facebookxmlfeedformat-1.ClZDeaFT.png)

В появившемся окне выберите "Использовать массовую загрузку" для загрузки файла с товарами.

![Как выгрузить товары на Facebook - Шаг 2](/_app/immutable/assets/export-facebookxmlfeedformat-2.BBA6-t6K.png)

Затем выберите "Загрузка файла" и загрузите файл. Файл сразу пройдет валидацию, убедитесь, что не появляется сообщений об ошибке.
Запустите импорт товаров и дождитесь результатов импорта.

![Как выгрузить товары на Facebook - Шаг 3](/_app/immutable/assets/export-facebookxmlfeedformat-3.SwS3ndv7.png)

![Как выгрузить товары на Facebook - Шаг 4](/_app/immutable/assets/export-facebookxmlfeedformat-4.CrEq-Iwb.png)

## Вариации

Если у товара есть характеристики с несколькими значениями (например, несколько цветов или размеров), для каждой комбинации значений
выгружается отдельная вариация с общим **g:item\_group\_id** — артикулом товара. Цена, фото и описание у всех вариаций
одинаковые. Цвет, размер, пол, материал и узор попадают в стандартные теги Facebook\*, остальные характеристики с несколькими
значениями — в **g:additional\_variant\_attribute**.

## Артикул товара

Тег **g:id** заполняется артикулом товара. Если артикула нет, используется код, построенный по ссылке на товар. Такой код не
меняется между выгрузками, но если ссылка на товар изменится, Facebook\* примет его за новый товар. Чтобы этого избежать, задайте
артикулы в [редактировании товаров](/howto/mods).

\* Meta признана экстремистской организацией в России.

## Специальные характеристики

Часть тегов заполняется значением характеристики с фиксированным названием. Если у товара такой характеристики нет, тег не
выгружается. Своих тегов для остальных характеристик у Facebook\* нет, поэтому все характеристики товара добавляются к описанию **g:description**.

**g:brand** — характеристика «Бренд».

**g:mpn** — характеристика «MPN», код производителя. Артикул в этот тег не выгружается.

**g:color** — характеристика «Цвет».

**g:size** — характеристика «Размер».

**g:gender** — характеристика «Пол»: значения «Женский», «Мужской», «Унисекс».

**g:material** — характеристика «Материал».

**g:pattern** — характеристика «Узор».

Название должно совпадать точно. Переименовать характеристику можно в [редактировании товаров](/howto/mods/cols-rename).

## Extracted settings

- "Электронная коммерция"
- g:additional\_variant\_attribute
- g:brand
- g:color
- g:description
- g:gender
- g:id
- g:item\_group\_id
- g:material
- g:mpn
- g:pattern
- g:size

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
