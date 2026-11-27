---
id: "format-insalesxlsformat"
title: "Как выгрузить товары в InSales?"
tags:
  - qparser
  - format
  - cms
sources:
  - https://q-parser.ru/howto/format/insalesxlsformat
confidence: "measured"
updated: "2026-11-27"
---

# Как выгрузить товары в InSales?

**Category:** `cms` · **Target:** InSales
**Source:** https://q-parser.ru/howto/format/insalesxlsformat

Список товаров на InSales выгружается в формате Excel. Файл уже подготовлен для импорта на платформу InSales, дополнительных
манипуляций не требуется.

InSales может загружать файлы не более 60 мегабайт за раз. Если нужно импортировать больше товаров, разбейте выгрузку на более
мелкие с помощью функции [частичной выгрузки](/howto/erange).

Обратите внимание, что возможен импорт товаров в InSales также из [YML формата](/howto/format/ymlformat) и [CSV формата](/howto/format/insalescsvformat).

### 1. В списке товаров нажмите "Выгрузить"

После загрузки товаров на парсер, находясь на странице со списком товаров, нажмите кнопку "Выгрузить".

![Как выгрузить товары в InSales - Шаг 1](/static/howto/export-1.png)

### 2. Задайте настройки формата

В появившемся окне выберите формат "InSales XLS (insales.ru)", задайте необходимые настройки и сформируйте файл для импорта товаров.

### 3. Перейдите в раздел Импорт в вашем InSales

В панели управления вашего магазина InSales перейдите в раздел «Импорт/Экспорт», выберите пункт «Из XLS» из контекстного меню по
клику «Новый импорт».

![Как выгрузить товары в InSales - Шаг 3](/_app/immutable/assets/export-insalescsv-2.DC0SmiOw.jpg)

### 4. Выберите сопоставление товаров

Вам необходимо определить, как сопоставлять новые товары из файла с теми, что уже есть. Для простоты выбора нужного типа используйте
блок-схему ниже.

В типах 2-4 для дополнительной идентификации используются категории. Тип №5 "Идентифицировать по ID вариантов" только обновляет
существующие товары и не добавляет новые. Подробнее читайте в разделе [«Обновление товаров с помощью импорта из csv»](https://www.insales.ru/collection/doc-import-export/product/obnovlenie-suschestvuyuschih-tovarov-s-pomoschyu-importa-iz-csv-sposoby-identifikatsii-tovarov-pri-importe-iz-csv-i-razlichiya-mezhdu-nimi).

![Как выгрузить товары в InSales - Шаг 4](/_app/immutable/assets/export-insalescsv-3.DOUA_lU5.png)

### 5. Загрузите файл из Q-Parser

- Загрузите файл с диска (скачав его), либо укажите ссылку на файл.
- Можно указать кодировку файла. Обычно подходит автоопределение. На Q-Parser можно выбрать UTF-8 или Windows-1251 (по умолчанию).
- Разделитель столбцов - точка с запятой (;). Обычно подходит автоопределение.
- Укажите язык файла, если он отличается от Русского.
- Нажмите «Загрузить» и дождитесь загрузки файла.

![Как выгрузить товары в InSales - Шаг 5](/_app/immutable/assets/export-insalescsv-4.C4n8xq1Z.jpg)

### 6. Задайте настройки импорта

Сопоставьте все столбцы из файла с атрибутами товаров в InSales. Например, для столбца «Название» выберите атрибут «Название
товара», для столбца «Скорость» создайте параметр «Скорость», для свойства «Цвет» выберите «Свойство: Цвет». Если атрибут уже
существовал (базовый атрибут или ранее созданный вручную или импортом параметр), он автоматически подставится.

После сопоставления атрибутов прокрутите страницу к настройкам. По умолчанию настройки установлены в наиболее востребованный
пользователями режим. Проверьте, подходят ли они вам. Подробнее про настройки вы сможете прочитать в статье [Настройки обновления товаров из csv и их смысл](https://www.insales.ru/collection/doc-import-export/product/obnovlenie-suschestvuyuschih-tovarov-s-pomoschyu-importa-iz-csv-nastroyki-obnovleniya-tovarov-i-ih-smysl).

![Как выгрузить товары в InSales - Шаг 4](/_app/immutable/assets/export-insalescsv-5.CM6HIZsI.jpg)

![Как выгрузить товары в InSales - Шаг 5](/_app/immutable/assets/export-insalescsv-6.BfVmtYC1.jpg)

### 7. Дождитесь окончания импорта

На следующем шаге начинается импорт. Он может продлиться до нескольких часов (особенно если импорт идет с изображениями). Вы можете
закрыть браузер, отчет о завершении импорта придет Вам на электронную почту.

После завершения импорта товары появятся у вас на складе в разделе "Импорт/Экспорт" и вы сможете выставить их на витрину магазина.

![Как выгрузить товары в InSales - Шаг 6](/_app/immutable/assets/export-insalescsv-7.C5MvMFHv.jpg)

## Категории

Каждый уровень категории выгружается в отдельную колонку: «Корневая», «Подкатегория 1», «Подкатегория 2» и далее по числу уровней
категорий товаров.

Актуальную инструкцию по импорту товаров всегда можно найти в [документации InSales](https://www.insales.ru/collection/doc-import-export/product/sozdanie-tovarov-s-pomoschyu-importa-iz-csv-i-xls).

## Extracted settings

- (no bold settings detected)

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
