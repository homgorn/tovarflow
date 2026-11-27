---
id: "format-joomshoppingformat"
title: "Как выгрузить товары в JoomShopping?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/joomshoppingformat
confidence: "measured"
updated: "2026-11-27"
---

# Как выгрузить товары в JoomShopping?

**Category:** `cms` · **Target:** JoomShopping
**Source:** https://q-parser.ru/howto/format/joomshoppingformat

[JoomShopping](https://extensions.joomla.org/extension/joomshopping/) — бесплатный интернет-магазин
для Joomla. Для импорта товаров у вас должен быть установлен и настроен данный модуль.

**Важно.** Для импорта у вас должна быть поддержка импорта в формате Comiel.

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары в JoomShopping - Шаг 1](/static/howto/export-1.png)

### 2. Заходим в раздел Import & Export

В панели администратора Joomla переходим в раздел Components > JoomShopping > Options и выбираем раздел Import & Export

![Как выгрузить товары в JoomShopping - Шаг 2](/_app/immutable/assets/joomshopping-1.CIMhgHK8.png)

### 3. Выбираем формат Comiel

В появившемся списке выбираем формат Comiel

![Как выгрузить товары в JoomShopping - Шаг 3](/_app/immutable/assets/joomshopping-2.Ch_SfIaS.png)

### 4. Загружаем файл

Выбираем вкладку Import, подгружаем наш файл и нажимаем кнопку "Start importing a file"

Обратите внимание на список настроек под полем загрузки файла. Если требуется, выберите интересующие вас настройки.

Для добавления в каталог новых товаров необходимо установить переключатель "Create products?" в положение "Yes".

![Как выгрузить товары в JoomShopping - Шаг 4](/_app/immutable/assets/joomshopping-3.sUEes7EF.png)

### 5. Отчет об импорте

После обработки файла вы увидите отчет об импортированных товарах.

![Как выгрузить товары в JoomShopping - Шаг 5](/_app/immutable/assets/joomshopping-4.DB21Gi4j.png)

## Как импортировать картинки в JoomShopping?

Архив с файлами изображений необходимо распаковать на ваш веб-сервер по пути:

\_ваш\_сайт\_/components/com\_jshopping/files/img\_products

Для формирования превью-изображений мы рекомендуем пользоваться расширением [Расширенный импорт экспорт Товаров из MS Excel (XLS, XLSX), CSV в JoomShopping](https://nevigen.com/ru/import-export/kompleksnyj-import-eksport-tovarov-joomshopping.html)

При импорте, необходимо сначала распаковать изображения на сервер и в настройках импорта включить опцию "Менять размеры фото?",
тогда, при импорте автоматически сгенерируются нужные размеры фото.

## Настройки формата

**Выгрузка файлов** — определяет куда выгружать ссылки на дополнительные файлы к товарам: оставлять в характеристиках или размещать
отдельно в поле files (потребует ручно доработки модуля импорта).

## Специальные характеристики

Часть колонок заполняется значением характеристики с фиксированным названием. Если у товара такой характеристики нет, колонка
останется пустой. Эти характеристики не дублируются в колонке **extra\_fields**: туда попадают остальные.

**manufacturer** — характеристика «Бренд».

**weight** — характеристика «Вес».

Название должно совпадать точно. Переименовать характеристику можно в [редактировании товаров](/howto/mods/cols-rename).

## Extracted settings

- extra\_fields
- manufacturer
- weight
- Важно.
- Выгрузка файлов

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
