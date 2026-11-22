---
url: https://q-parser.ru/howto/format/opencartcsvliteformat
path: /howto/format/opencartcsvliteformat
title: "Как выгрузить товары в OpenCart модулем CSV Export/Import Light?"
fetched_at: 2026-11-22T06:35:09+00:00
http_status: 200
sha256: 89050f7081f689c024c8752dff0591a1fb1d962a417a5c32ab742f345b0b7a5e
links: ["/howto/mods/cols-rename"]
---

Выгрузка товаров производится в формате OpenCart для модуля [CSV Export/Import Light](https://shop.opencart-russia.ru/csv-export-import-light).

Модуль работает только с основными данными: товары, категории, производители, изображения, опции и атрибуты.

Архив с изображениями (images.zip) необходимо распаковать и загрузить содержимое архива в вашу папку с картинками OpenCart (обычно
"image").

Подробную информацию о модуле вы можете получить на странице модуля в магазине OpenCart или связавшись с разработчиком.

![Как выгрузить товары в OpenCart](/_app/immutable/assets/export-opencartcsvliteformat-1.Ceq2ndJW.png)

## Специальные характеристики

Часть колонок заполняется значением характеристики с фиксированным названием. Если у товара такой характеристики нет, колонка
останется пустой. Эти характеристики не дублируются в атрибутах: туда попадают остальные.

**manufacturer** — характеристика «Бренд».

Название должно совпадать точно. Переименовать характеристику можно в [редактировании товаров](/howto/mods/cols-rename).
