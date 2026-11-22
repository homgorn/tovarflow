---
id: "formats"
title: "Export formats"
tags:
  - qparser
  - formats
  - export
sources:
  - https://q-parser.ru/howto/format
confidence: "measured"
updated: "2026-11-22"
---

# Export formats

72 formats are documented. A format is a contract: target platform, file shape,
settings, and field mapping. The storefront pipeline must treat each format as a versioned adapter.

| Category | Count | What it is for |
|---|---|---|
| file | 5 | Universal CSV / XLS / JSON / XML / YML |
| cms | 36 | Direct import into a shop engine |
| social | 8 | VK, OK, Facebook, Google Merchant, showcase |
| marketplace | 5 | YML/XML feeds for marketplaces |
| sp | 16 | Group-buying platforms |
| commerce | 2 | CommerceML / MoySklad |

## File formats

### file

| Format | Target | Source |
|---|---|---|
| [[topics/formats/csvformat\|Как выгрузить товары в CSV?]] | CSV | file |
| [[topics/formats/jsonformat\|Как выгрузить товары в JSON?]] | JSON | file |
| [[topics/formats/xlsformat\|Как выгрузить товары в Excel?]] | Excel | file |
| [[topics/formats/xmlformat\|Как выгрузить товары в XML?]] | XML | file |
| [[topics/formats/ymlformat\|Как выгрузить товары в YML?]] | YML | file |

### marketplace

| Format | Target | Source |
|---|---|---|
| [[topics/formats/epicentrkymlformat\|Как выгрузить товары на Epicentrk (epicentrk.ua) в YML?]] | Epicentrk (epicentrk.ua) в YML | marketplace |
| [[topics/formats/kaspixmlformat\|Как выгрузить цены и наличие товаров на Kaspi.kz?]] | Как выгрузить цены и наличие товаров на Kaspi.kz | marketplace |
| [[topics/formats/megamarketymlformat\|Как выгрузить товары на Мегамаркет?]] | Мегамаркет | marketplace |
| [[topics/formats/promuaymlformat\|Как выгрузить товары на Prom.ua?]] | Prom.ua | marketplace |
| [[topics/formats/rozetkaymlformat\|Как выгрузить товары на Rozetka.com.ua?]] | Rozetka.com.ua | marketplace |

### commerce

| Format | Target | Source |
|---|---|---|
| [[topics/formats/commercemlformat\|Как выгрузить товары в CommerceML (1С)?]] | CommerceML (1С) | commerce |
| [[topics/formats/moyskladformat\|Как выгрузить товары в МойСклад?]] | МойСклад | commerce |

### cms

| Format | Target | Source |
|---|---|---|
| [[topics/formats/advantshopv1format\|Как выгрузить товары в Advantshop 1.0?]] | Advantshop 1.0 | cms |
| [[topics/formats/advantshopv2format\|Как выгрузить товары в Advantshop 2.0?]] | Advantshop 2.0 | cms |
| [[topics/formats/alltradesformat\|Как выгрузить товары на AllTrades?]] | AllTrades | cms |
| [[topics/formats/bitrixcsvformat\|Как выгрузить товары в 1С-Битрикс (Bitrix)?]] | 1С-Битрикс (Bitrix) | cms |
| [[topics/formats/botobotformat\|Как выгрузить товары в Botobot?]] | Botobot | cms |
| [[topics/formats/cmss3format\|Как выгрузить товары для CMS.S3 (Megagroup)?]] | CMS.S3 (Megagroup) | cms |
| [[topics/formats/cscartformat\|Как выгрузить товары на CS-Cart?]] | CS-Cart | cms |
| [[topics/formats/diskauntscsvformat\|Как выгрузить товары на маркетплейс Diskaunts?]] | маркетплейс Diskaunts | cms |
| [[topics/formats/eshoperformat\|Как выгрузить товары в Eshoper?]] | Eshoper | cms |
| [[topics/formats/hostcmsformat\|Как выгрузить товары на HostCMS?]] | HostCMS | cms |
| [[topics/formats/insalescsvformat\|Как выгрузить товары в InSales?]] | InSales | cms |
| [[topics/formats/insalesxlsformat\|Как выгрузить товары в InSales?]] | InSales | cms |
| [[topics/formats/joomlaformat\|Как выгрузить товары в Joomla (Excel2JS)?]] | Joomla (Excel2JS) | cms |
| [[topics/formats/joomshoppingformat\|Как выгрузить товары в JoomShopping?]] | JoomShopping | cms |
| [[topics/formats/lpmotorformat\|Как выгрузить товары для LPmotor (lpmotor.ru)?]] | LPmotor (lpmotor.ru) | cms |
| [[topics/formats/mogutaformat\|Как выгрузить товары в Moguta?]] | Moguta | cms |
| [[topics/formats/okaycmsformat\|Как выгрузить товары на OkayCMS?]] | OkayCMS | cms |
| [[topics/formats/opencartcsvliteformat\|Как выгрузить товары в OpenCart модулем CSV Export/Import Light?]] | OpenCart модулем CSV Export/Import Light | cms |
| [[topics/formats/opencartcsvpriceproformat\|Как выгрузить товары для OpenCart в формате CSV Price Pro?]] | OpenCart в формате CSV Price Pro | cms |
| [[topics/formats/opencartexportimportformat\|Как выгрузить товары в OpenCart?]] | OpenCart | cms |
| [[topics/formats/openmallformat\|Как выгрузить товары на OpenMall?]] | OpenMall | cms |
| [[topics/formats/osclassadimporterformat\|Как выгрузить товары в Osclass?]] | Osclass | cms |
| [[topics/formats/phpshopformat\|Как выгрузить товары в PHPShop?]] | PHPShop | cms |
| [[topics/formats/prestashopformat\|Как выгрузить товары в PrestaShop?]] | PrestaShop | cms |
| [[topics/formats/prestashopmagiconestoremanagerformat\|Как выгрузить товары в PrestaShop MagicOne Store Manager?]] | PrestaShop MagicOne Store Manager | cms |
| [[topics/formats/readyscriptformat\|Как выгрузить товары в ReadyScript?]] | ReadyScript | cms |
| [[topics/formats/shopifyformat\|Как выгрузить товары на Shopify (shopify.com)?]] | Shopify (shopify.com) | cms |
| [[topics/formats/simplacmsformat\|Как выгрузить товары в Simpla CMS?]] | Simpla CMS | cms |
| [[topics/formats/storelandformat\|Как выгрузить товары в Storeland?]] | Storeland | cms |
| [[topics/formats/tildacsvformat\|Как выгрузить товары на Tilda (tilda.cc) в CSV?]] | Tilda (tilda.cc) в CSV | cms |
| [[topics/formats/tildaymlformat\|Как выгрузить товары на Tilda (tilda.cc) в YML?]] | Tilda (tilda.cc) в YML | cms |
| [[topics/formats/uralcmscsvformat\|Как выгрузить товары для Ural CMS (uralcms.ru)?]] | Ural CMS (uralcms.ru) | cms |
| [[topics/formats/ushopymlformat\|Как выгрузить товары на uShop (ucoz.ru)?]] | uShop (ucoz.ru) | cms |
| [[topics/formats/webasystshopscriptformat\|Как выгрузить товары в Webasyst Shop-Script?]] | Webasyst Shop-Script | cms |
| [[topics/formats/wixformat\|Как выгрузить товары в Wix?]] | Wix | cms |
| [[topics/formats/woocommerceformat\|Как выгрузить товары в WooCommerce?]] | WooCommerce | cms |

### social

| Format | Target | Source |
|---|---|---|
| [[topics/formats/facebookcsvformat\|Как выгрузить товары в каталоги Facebook* (CSV)?]] | каталоги Facebook* (CSV) | social |
| [[topics/formats/facebookxmlfeedformat\|Как выгрузить товары в каталоги Facebook*?]] | каталоги Facebook* | social |
| [[topics/formats/googlemerchantformat\|Как выгрузить товары в Google Merchant Center?]] | Google Merchant Center | social |
| [[topics/formats/okalbumsformat\|Как выгрузить товары в альбомы Одноклассники?]] | альбомы Одноклассники | social |
| [[topics/formats/okformat\|Как выгрузить товары в Одноклассники?]] | Одноклассники | social |
| [[topics/formats/showcaseformat\|Витрины товаров]] | Витрины товаров | social |
| [[topics/formats/vkalbumsformat\|Как выгрузить товары в альбомы ВКонтакте?]] | альбомы ВКонтакте | social |
| [[topics/formats/vkformat\|Как выгрузить товары в ВКонтакте?]] | ВКонтакте | social |

### sp

| Format | Target | Source |
|---|---|---|
| [[topics/formats/amadyformat\|Как выгрузить товары на Амади?]] | Амади | sp |
| [[topics/formats/kupivspformat\|Как выгрузить товары на сайт Kupivsp.ru?]] | сайт Kupivsp.ru | sp |
| [[topics/formats/materinstvoshopformat\|Как выгрузить товары на Материнство (materinstvo-shop.ru)?]] | Материнство (materinstvo-shop.ru) | sp |
| [[topics/formats/mikaiformat\|Как выгрузить товары на Mikai?]] | Mikai | sp |
| [[topics/formats/ok24format\|Как выгрузить товары на 24-ok.ru?]] | 24-ok.ru | sp |
| [[topics/formats/pokupki63format\|Как выгрузить товары на 63pokupki.ru?]] | 63pokupki.ru | sp |
| [[topics/formats/pokupkiprostoformat\|Как выгрузить товары на Покупки-просто?]] | Покупки-просто | sp |
| [[topics/formats/samarskieroditeliformat\|Как выгрузить товары на Самарские родители?]] | Самарские родители | sp |
| [[topics/formats/serpokformat\|Как выгрузить товары на Serpok.ru?]] | Serpok.ru | sp |
| [[topics/formats/spkostromaformat\|Как выгрузить товары на СП Кострома?]] | СП Кострома | sp |
| [[topics/formats/spprotonformat\|Как выгрузить товары на сайты СП-Протон?]] | сайты СП-Протон | sp |
| [[topics/formats/stospformat\|Как выгрузить товары на 100 СП?]] | 100 СП | sp |
| [[topics/formats/supermamkiformat\|Как выгрузить товары на Супермамки?]] | Супермамки | sp |
| [[topics/formats/superpuperformat\|Как выгрузить товары на сайт SuperPuper.ru?]] | сайт SuperPuper.ru | sp |
| [[topics/formats/tom70format\|Как выгрузить товары на сайты СП с модулем Tom70?]] | сайты СП с модулем Tom70 | sp |
| [[topics/formats/zaprosto24format\|Как выгрузить товары на Запросто 24?]] | Запросто 24 | sp |
