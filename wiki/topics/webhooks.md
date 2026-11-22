---
id: "webhooks"
title: "Automation webhooks"
tags:
  - qparser
  - webhooks
  - hmac
sources:
  - https://q-parser.ru/howto/automata/webhooks
confidence: "measured"
updated: "2026-11-22"
---

# Automation webhooks


Webhooks позволяют узнать о завершении автовыгрузки программно: например, сразу забрать свежий файл или запустить импорт на своем
сайте.

## Как добавить webhook

- Откройте автовыгрузку на странице [Автоматические выгрузки](/my/parser/automata);
- Перейдите на вкладку **Webhooks**;
- Добавьте адрес, на который нужно отправлять запрос, и нажмите **Сохранить**.

К одной автовыгрузке можно добавить до 5 адресов. После сохранения под каждым адресом появится секрет для проверки подписи.

## Когда отправляется запрос

После каждой завершенной выгрузки мы отправляем на каждый адрес **POST**-запрос с JSON-телом. Если парсинг завершился с ошибкой
или был отменен, выгрузка не запускается и webhooks не вызываются.

Если в автовыгрузке несколько выгрузок, запрос приходит на каждую выгрузку отдельно. Различить их можно по полям `export_id`, `automata_export_id` и `format`.

Ответ вашего сервера должен иметь код **2xx**, тело ответа не важно. Если сервер ответил другим кодом, перенаправил запрос или не
ответил за 10 секунд, мы повторим запрос через 1, 5, 10, 30 и 60 секунд. Если все попытки не удались, ошибка будет показана в
настройках webhook.

## Параметры запроса

```
{
    "event": "automata.finished",
    "status": "success",
    "result": {
        "files": [
            "https://s3.q-parser.ru/a1b2c3d4/example.com.csv"
        ]
    },
    "automata_id": "0b6c1e3a-5f0d-4c6e-9a51-3d2f8f0c7e11",
    "automata_title": "Каталог example.com",
    "automata_export_id": "5a7f3c21-9d4e-4b8a-8f6c-2e1d0b9a7c35",
    "domain": "example.com",
    "format": "csv",
    "parsing_id": 123456,
    "export_id": "7d9e2b14-8a3f-4b6d-b1c2-5e4f3a2d1c0b",
    "goods_processed": 1520,
    "goods_exported": 1498,
    "created_at": 1767225600,
    "finished_at": 1767229200
}
```

- `status` — `success` или `error`, если выгрузка завершилась с ошибкой;
- `result` — результат выгрузки, как он показан в личном кабинете: `files` (ссылки на файлы), `links` (ссылки на отчеты), `message` (например, если выгрузка не запускалась из-за отсутствия изменений)
  и `error` (текст ошибки);
- `parsing_id` — номер парсинга, `export_id` — ID выгрузки;
- `automata_export_id` — ID выгрузки в настройках автовыгрузки: одинаковый при каждом запуске, пока выгрузку не
  удалят. Помогает понять, к какой выгрузке относится запрос, если их несколько; `null`, если выгрузку уже удалили;
- `goods_processed` — товаров обработано при парсинге, `goods_exported` — товаров выгружено;
- `created_at`, `finished_at` — время запуска парсинга и завершения выгрузки (Unix timestamp, секунды).

Заголовки запроса:

- `X-QParser-Delivery` — ID доставки, одинаковый во всех повторах. Помогает не обработать один вызов дважды;
- `X-QParser-Timestamp` — время отправки (Unix timestamp);
- `X-QParser-Signature` — подпись `sha256=<HMAC-SHA256>` от строки `<X-QParser-Timestamp>.<тело запроса>` с секретом webhook.

## Проверка подписи

Секрет у каждого webhook свой, он показан под адресом в настройках. Проверяйте подпись, чтобы убедиться, что запрос отправил
Q-Parser. Если секрет стал известен посторонним, сгенерируйте новый: старый сразу перестанет работать.

Пример проверки на PHP:

```
<?php
$secret = 'секрет webhook из настроек автовыгрузки';
$body = file_get_contents('php://input');
$timestamp = $_SERVER['HTTP_X_QPARSER_TIMESTAMP'] ?? '';
$signature = $_SERVER['HTTP_X_QPARSER_SIGNATURE'] ?? '';

$expected = 'sha256=' . hash_hmac('sha256', $timestamp . '.' . $body, $secret);

if (!hash_equals($expected, $signature) || abs(time() - (int)$timestamp) > 300) {
    http_response_code(403);
    exit;
}

$data = json_decode($body, true);
// ... обработка $data
http_response_code(200);
```

Пример проверки на Node.js:

```
import {createHmac, timingSafeEqual} from 'node:crypto';
import {createServer} from 'node:http';

const secret = 'секрет webhook из настроек автовыгрузки';

createServer((req, res) => {
    const chunks = [];
    req.on('data', chunk => chunks.push(chunk));
    req.on('end', () => {
        const body = Buffer.concat(chunks).toString('utf8');
        const timestamp = req.headers['x-qparser-timestamp'] ?? '';
        const signature = req.headers['x-qparser-signature'] ?? '';

        const expected = 'sha256=' + createHmac('sha256', secret).update(timestamp + '.' + body).digest('hex');
        const valid =
            signature.length === expected.length &&
            timingSafeEqual(Buffer.from(signature), Buffer.from(expected)) &&
            Math.abs(Date.now() / 1000 - Number(timestamp)) <= 300;

        if (!valid) {
            res.writeHead(403).end();
            return;
        }

        const data = JSON.parse(body);
        // ... обработка data
        res.writeHead(200).end();
    });
}).listen(3000);
```

## Связанные материалы

- [Автовыгрузки — общие сведения](/howto/automata)
- [Настройка автовыгрузок](/howto/automata/edit)
- [Форматы выгрузки](/howto/format)
