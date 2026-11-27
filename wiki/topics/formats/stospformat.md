---
id: "format-stospformat"
title: "Как выгрузить товары на 100 СП?"
tags:
  - qparser
  - format
  - sp
sources:
  - https://q-parser.ru/howto/format/stospformat
confidence: "measured"
updated: "2026-11-27"
---

# Как выгрузить товары на 100 СП?

**Category:** `sp` · **Target:** 100 СП
**Source:** https://q-parser.ru/howto/format/stospformat

На этой странице

[100sp](http://www.100sp.ru/) — это один из крупнейших сайтов совместных покупок в России,
который работает с 2007 года.

Выгрузка для 100 СП производится в формате CSV, но здесь мы уже все настроили именно под этот сайт так, чтобы максимально
использовать его возможности.

### Общие настройки

**Выгрузка характеристик** — позволяет выгрузить свойства товаров (цвета, размеры и пр.) отдельными полями или добавить их
к описанию.

**Разбить на несколько файлов** — позволяет разбить выгрузку на несколько файлов: по категориям или по брендам.

**Разбить по числу товаров** — максимум товаров в одном файле. Например, при значении 5000 первые 5000 товаров попадут в
первый файл, следующие — во второй (с окончанием --2) и т.д. Работает вместе с разбивкой по категориям и брендам: лимит действует
внутри каждого файла категории или бренда. Пустое значение — без ограничения.

**Файловое хранилище** — позволяет сделать выгрузку файлов в произвольное хранилище на FTP или S3 ([подробнее](/howto/filestorage))

### Нашли ошибку в выгрузке в этот формат?

Если вы обнаружили ошибку в формате выгрузки 100 СП (100sp.ru), пожалуйста, сообщите нам на почту или в чат на сайте. Мы
постараемся исправить выгрузку как можно скорее.

## Связанные материалы

- [Все форматы выгрузки](/howto/format)
- [Выгрузка в CSV](/howto/format/csvformat)
- [Выгрузка в YML](/howto/format/ymlformat)
- [Выгрузка в соцсети](/howto/social)
- [Как выгружать товары](/howto)

- [CSV](/howto/format/csvformat)
- [Excel (XLS/x)](/howto/format/xlsformat)
- [JSON](/howto/format/jsonformat)
- [XML](/howto/format/xmlformat)
- [YML (Яндекс.Маркет)](/howto/format/ymlformat)

- [Facebook\* - Catalog Manager (CSV)](/howto/format/facebookcsvformat)
- [Facebook\* - Catalog Manager (XML)](/howto/format/facebookxmlfeedformat)
- [Google Merchant Center (XML)](/howto/format/googlemerchantformat)
- [Витрина товаров](/howto/format/showcaseformat)
- [ВКонтакте - Альбомы](/howto/format/vkalbumsformat)
- [ВКонтакте - Товары](/howto/format/vkformat)
- [Одноклассники - Альбомы](/howto/format/okalbumsformat)
- [Одноклассники - Товары](/howto/format/okformat)

- [100 СП (100sp.ru)](/howto/format/stospformat)
- [24-OK (24-ok.ru)](/howto/format/ok24format)
- [63покупки (63pokupki.ru)](/howto/format/pokupki63format)
- [Mikai (mikai.org)](/howto/format/mikaiformat)
- [serpok.ru](/howto/format/serpokformat)
- [SuperPuper (superpuper.ru)](/howto/format/superpuperformat)
- [Tom70 (tom70.ru)](/howto/format/tom70format)
- [Амади (amady-sp.ru)](/howto/format/amadyformat)
- [Запросто 24 (zaprosto24.ru)](/howto/format/zaprosto24format)
- [Купим вместе (kupivsp.ru)](/howto/format/kupivspformat)
- [Материнство (materinstvo-shop.ru)](/howto/format/materinstvoshopformat)
- [Покупки-Просто (pokupki-prosto.ru)](/howto/format/pokupkiprostoformat)
- [Самарские родители (sp.samarskie-roditeli.ru)](/howto/format/samarskieroditeliformat)
- [СП Кострома (spkostroma.ru)](/howto/format/spkostromaformat)
- [СП-Протон](/howto/format/spprotonformat)
- [Супермамки (supermamki.ru)](/howto/format/supermamkiformat)

- [Advantshop 1.0 (advantshop.net)](/howto/format/advantshopv1format)
- [Advantshop 2.0 (advantshop.net)](/howto/format/advantshopv2format)
- [AllTrades (alltrades.ru)](/howto/format/alltradesformat)
- [Botobot (botobot.ru)](/howto/format/botobotformat)
- [CMS.S3 (Megagroup)](/howto/format/cmss3format)
- [CommerceML 2 (1С)](/howto/format/commercemlformat)
- [CS-Cart (cs-cart.ru)](/howto/format/cscartformat)
- [Diskaunts CSV (diskaunts.net)](/howto/format/diskauntscsvformat)
- [Epicentrk YML (epicentrk.ua)](/howto/format/epicentrkymlformat)
- [Eshoper (eshoper.ru)](/howto/format/eshoperformat)
- [HostCMS (hostcms.ru)](/howto/format/hostcmsformat)
- [InSales CSV (insales.ru)](/howto/format/insalescsvformat)
- [InSales XLS (insales.ru)](/howto/format/insalesxlsformat)
- [Joomla: Excel2JS (JoomShopping)](/howto/format/joomlaformat)
- [JoomShopping (Comiel)](/howto/format/joomshoppingformat)
- [Kaspi.kz (XML)](/howto/format/kaspixmlformat)
- [LPmotor (CSV)](/howto/format/lpmotorformat)
- [Moguta (moguta.ru)](/howto/format/mogutaformat)
- [Okay CMS (okay-cms.com)](/howto/format/okaycmsformat)
- [OpenCart CSV Export/Import Light](/howto/format/opencartcsvliteformat)
- [OpenCart CSV Price Pro](/howto/format/opencartcsvpriceproformat)
- [OpenCart Export/Import](/howto/format/opencartexportimportformat)
- [OpenMall (openmall.info)](/howto/format/openmallformat)
- [Osclass (Ad Importer)](/howto/format/osclassadimporterformat)
- [PHPShop](/howto/format/phpshopformat)
- [PrestaShop (CSV)](/howto/format/prestashopformat)
- [PrestaShop MagicOne Store Manager](/howto/format/prestashopmagiconestoremanagerformat)
- [Prom.ua (YML)](/howto/format/promuaymlformat)
- [ReadyScript (readyscript.ru)](/howto/format/readyscriptformat)
- [Rozetka (YML)](/howto/format/rozetkaymlformat)
- [Shopify (shopify.com)](/howto/format/shopifyformat)
- [Simpla CMS](/howto/format/simplacmsformat)
- [Storeland](/howto/format/storelandformat)
- [Tilda CSV (tilda.cc)](/howto/format/tildacsvformat)
- [Tilda YML (tilda.cc)](/howto/format/tildaymlformat)
- [Ural CMS (CSV)](/howto/format/uralcmscsvformat)
- [uShop YML (ucoz.ru)](/howto/format/ushopymlformat)
- [Webasyst Shop-Script](/howto/format/webasystshopscriptformat)
- [Wix (wix.com)](/howto/format/wixformat)
- [WooCommerce (CSV)](/howto/format/woocommerceformat)
- [Битрикс (CSV)](/howto/format/bitrixcsvformat)
- [Мегамаркет (YML)](/howto/format/megamarketymlformat)
- [МойСклад (moysklad.ru)](/howto/format/moyskladformat)

- [Общие сведения](/howto/automata)
- [Настройка автовыгрузок](/howto/automata/edit)
- [Webhooks](/howto/automata/webhooks)

- [Общие сведения](/howto/ai)
- [Как запустить AI редактирование](/howto/ai/agent)
- [Генерация и редактирование фото товаров](/howto/ai/images)
- [Удаление водяных знаков](/howto/ai/unwatermark)
- [Веб-поиск](/howto/ai/web-search)
- [Составление запросов к AI](/howto/ai/prompt-writing)
- [AI модели](/howto/ai/models)
- [AI Points](/howto/ai/points)

- [Общие сведения](/howto/mods)
- [Шаблоны и копирование](/howto/mods/copying)
- [Фильтрация товаров](/howto/mods/filter)
- [Сортировка товаров](/howto/mods/sort)
- [Удаление дублей](/howto/mods/deduplication)
- [Изменение цен](/howto/mods/price)
- [Редактирование](/howto/mods/cols)
- [Переименование](/howto/mods/cols-rename)
- [Разделение](/howto/mods/cols-split)
- [Удаление](/howto/mods/cols-remove)
- [Обрезание](/howto/mods/cols-cut)
- [Удаление HTML-тегов](/howto/mods/cols-strip-html)
- [Удаление HTML элементов](/howto/mods/html-remove-children)
- [Сортировка характеристик](/howto/mods/cols-sort)
- [Поиск и замена](/howto/mods/cols-replace)
- [Изменение наличия товаров](/howto/mods/publish)

- [Общие сведения](/howto/mods/images)
- [Изменение формата](/howto/mods/images/format)
- [Ограничение числа фото](/howto/mods/images/count)
- [Изменение размеров](/howto/mods/images/resize)
- [Вписать с обрезкой](/howto/mods/images/embed)
- [Обрезка фото](/howto/mods/images/cut)
- [Наложение текста](/howto/mods/images/text)
- [Наложение watermark](/howto/mods/images/overlay)
- [Сделать цвет прозрачным](/howto/mods/images/transparent)
- [Добавить фон](/howto/mods/images/background)

- [Выгрузка в соцсети](/howto/social)
- [Предложить формат](/howto/format)
- [Реферальная программа](/howto/referral)
- [Кнопка в браузер](/howto/button)
- [Частичная выгрузка](/howto/erange)
- [Ручное добавление категорий](/howto/parser-categories)
- [Выгрузка на FTP, S3](/howto/filestorage)
- [Управление заголовками файлов](/howto/file-headers)
- [Сравнение парсингов](/howto/parser-compare)
- [Парсинг по CSS селекторам](/howto/additional-css-selectors)
- [Скачивание фото товаров](/howto/images-downloader)
- [API разработчикам](/howto/api)

## Extracted settings

- Выгрузка характеристик
- Разбить на несколько файлов
- Разбить по числу товаров
- Файловое хранилище

## Pipeline note

Treat this as an adapter contract, not as a file dump. Required fields, enum values and
media rules must be validated against the target platform before publishing.
