# Uniqlo API - Prices by Country, Stock by Size, Reviews

Read Uniqlo's own online stores: keyword search, one product in full, one product priced across up to 10 countries, online stock per colour and size, stock per store near a point, Uniqlo stores with opening hours, customer reviews with fit feedback, category lists, the sale and limited-offer lists, new arrivals, the category tree and search suggestions. All 12 endpoints return structured JSON and cost 1 credit per call, except store stock resolved from a product, colour and size (2 credits) and prices (1 credit per market).

**The job this skill is for: Uniqlo prices by country, Japan vs the rest.** One Uniqlo product id priced in each market, in that market's currency. **Product ids are global on uniqlo.com**: `E479000-000` opens the same product in every uniqlo.com market that sells it. Uniqlo's Greater China sites (`tw`, `hk`, `cn`) run their own product codes (`u0000000055478`), valid only there. `/prices` takes one product id and up to 10 countries per call.

Captured on 2026-11-17, product `E479000-000` (barrel jeans) from the prices endpoint with its default 10 markets (10 credits):

| `country` | `title` | `price` | `promo_price` | `currency` | `on_sale` | `tax` |
|---|---|---|---|---|---|---|
| `jp` | バギーバレルレッグジーンズ | 3990 | 3990 | JPY | true (limited offer until 11/19) | inclusive |
| `us` | Barrel Jeans | 39.9 | 39.9 | USD | true (limited offer until 11/18) | exclusive |
| `gb` | Baggy Barrel Leg Jeans | 39.9 | null | GBP | false | inclusive |
| `de` | Baggy Jeans (Barrel Leg) | 49.9 | null | EUR | false | inclusive |
| `fr` | Jean Barrel | 49.9 | null | EUR | false | inclusive |
| `kr` | 배기배럴레그진(다리길이75cm) | 59900 | null | KRW | false | inclusive |
| `au` | Baggy Barrel Leg Jeans \| Regular Length | 59.9 | null | AUD | false | inclusive |
| `ca` | Barrel Jeans | 59.9 | null | CAD | false | exclusive |
| `sg` | (not sold: `available: false`, listed in `not_sold`) | null | null | SGD | null | null |
| `th` | ยีนส์ ขาบาร์เรล (Baggy Barrel) \| ความยาวปกติ 75 cm* | 1290 | null | THB | false | inclusive |

Titles come back in each market's language and prices in its own currency, never converted. To compare countries, convert explicitly and state the rate and its date (for example the ECB reference rates of that day), and keep `tax` in mind: US and Canadian prices exclude sales tax, the others in this table include it. A shopper's tax refund abroad is not in any price.

**The price fields.** `price` is Uniqlo's regular price, `promo_price` its promotional price when it sends one. The two groups of markets show a drop differently:
- On **`us`, `jp`, `kr` and `ca`** (and on some items `sg`, `my` and `in`) Uniqlo marks a drop with **flags only**, so `promo_price` equals `price`; `on_sale`, `limited_offer` {`name`, `start`, `end`} and `price_flags` [{`code`, `name`, `start`, `end`}] carry the flags. The answer carries no earlier price there: never compute or invent a was-price or a discount for these markets. Captured on `ca` the same day: Seamless Down Parka `E470077-000` at `price` 99.9 and `promo_price` 99.9 CAD, flagged `discount` "Sale".
- In **Europe, Australia and most of Southeast Asia** `promo_price` is **below** `price`, with `discount_percent`. Captured on `vn` the same day: `E471601-000` at `price` 489000, `promo_price` 391000 VND, `discount_percent` 20, a limited offer labelled "Ưu đãi có giới hạn từ 13 thg 11 - 19 thg 11 2026".
- **Offer windows.** Only a limited-time offer has a window: quote Uniqlo's own label in `price_flags.name` (e.g. "Limited-Time Offer until 11/18"), not a date read from `end`. A sale flag carries a start but no end, and Select Colors/Sizes Only (`colorSizeLimitedPrice`) carries no dates. Where Uniqlo shows the 30-day lowest price next to a discount (Europe), the product and prices answers add `lowest_price_30d`; the key is absent otherwise.

**Price history.** Uniqlo shows none and none is returned. To build one, call `/prices` (or product) on a schedule and store each reading with its time, country, currency and flags. Only limited-time offers carry a window, under Uniqlo's own label.

**Price groups.** Product and prices default to `price_group` `00`, Uniqlo's regular price list. Search can list the same `product_id` a second time in price group `01`, mostly Uniqlo's Select Colors/Sizes Only sale price for some colours or sizes (`us` `E471601-000`: `00` at 29.9, `01` at 19.9); pass `price_group: "01"` to `/product` to read that price and the colours and sizes it covers. `/prices` compares group `00` unless `price_group` is sent. Store stock needs the price group the variant came from (see Guardrails). Black Friday 2026 is November 27; Uniqlo had announced no Black Friday dates in anything captured as of 2026-11-17.

Uniqlo has no public product data API. Neither Uniqlo nor Fast Retailing publishes developer documentation for catalog, price, stock or review data.

See also: for Zara prices by country use `zara-api`; for H&M prices by country use `hm-api`; for the cross-merchant view of one product use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Compare one Uniqlo item's price across countries, Japan against the US, the UK, Europe or Asia, each in its own currency (one product id, up to 10 countries per call)
- Check whether a Uniqlo item is on a limited-time offer or on sale in a market, and when a limited offer ends (Uniqlo's own label)
- Track Uniqlo prices over time (limited offers, Black Friday, seasonal sales) by polling and storing prices
- Check which colours and sizes of a Uniqlo item are in stock online (US, Japan, Korea)
- Check whether a size is in stock at the Uniqlo stores near a place (US, Japan, Korea)
- Find Uniqlo stores near a point with address, phone and opening hours
- Read Uniqlo customer reviews with fit feedback (runs small or large), purchased size and height, weight and age ranges
- Search Uniqlo's catalogue by keyword, sorted by price, newest or rating, filtered by gender, colour, size, flag or price range
- Read one Uniqlo product in full: description, composition, washing, country of origin, colours, sizes, rating and size chart link
- Browse the category tree, one category's list, the sale or limited-offer list, or the new arrivals
- Get Uniqlo's search suggestions or trending search words

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits: 50 one-credit calls, or five `/prices` calls across 10 markets each.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures most calls took 1 to 8 seconds; `/prices` across 10 markets took about 15 seconds. Set a client timeout of at least 180 seconds and do not fire many calls at once (a busy moment answers `503` with `Retry-After`).

| Endpoint | Markets | Credits | What it returns |
|---|---|---|---|
| `POST /api/v1/uniqlo/search` | us jp kr + tw hk cn | 1 | Items for a keyword with prices, flags, colours, sizes, rating; facets and totals |
| `POST /api/v1/uniqlo/product` | 41 (all) | 1 | One product by `product_id` or link: description, composition, washing, origin, category, prices, flags, colours, sizes, rating with fit, size chart link; variants on us jp kr |
| `POST /api/v1/uniqlo/prices` | 38 (all but tw hk cn) | 1 per market that answered | One product id in up to 10 markets: price, promo price, flags, tax, title, url; `not_sold` lists the markets that do not sell it |
| `POST /api/v1/uniqlo/stock` | us jp kr | 1 | Online stock of every colour x size (x length) variant, with its `l2_id` |
| `POST /api/v1/uniqlo/store-stock` | us jp kr | 1 with `l2_id`; 2 with `product_id` + `color` + `size` | One variant's status (in stock, low, out) in up to 10 stores nearest a point |
| `POST /api/v1/uniqlo/stores` | us jp kr | 1 | Stores nearest a point, or one store: address, phone, opening hours, sections, services |
| `POST /api/v1/uniqlo/reviews` | us jp kr | 1 | Customer reviews with rating, fit, purchased size, height / weight / age ranges; the rating summary |
| `POST /api/v1/uniqlo/suggestions` | us jp kr | 1 | Suggestions, categories and feature pages for a partial query; trending search words with no query |
| `POST /api/v1/uniqlo/category` | us jp kr | 1 | Every product of one category path, paged and sorted |
| `POST /api/v1/uniqlo/deals` | us jp kr | 1 | The sale list (`type: sale`) or the limited-offer list (`type: limited_offer`) |
| `POST /api/v1/uniqlo/new-arrivals` | us jp kr | 1 | Items Uniqlo flags New |
| `POST /api/v1/uniqlo/categories` | us jp kr | 1 | The market's category tree with the paths to pass as `category_path` |

A not-found (`404`) is charged; a failed upstream call is not.

## Markets

Every endpoint except `/prices` takes `country` (lowercase ISO-2, default `us`; `gb` for the United Kingdom, `uk` accepted as an alias) and `language` (default: the first listed below). Titles, descriptions, colour and category names come back in that language and prices in the market's currency, never converted. Answers echo `country` and `language`; list answers also echo `currency`.

| Group | `country` (languages, first is the default) | Currency | Endpoints |
|---|---|---|---|
| Full catalogue | `us` (en), `jp` (ja), `kr` (ko) | USD, JPY, KRW | all 12 |
| Greater China | `tw` (zh-Hant), `hk` (zh-Hant), `cn` (zh-Hans) | TWD, HKD, CNY | search, product (own product codes) |
| Product + prices | `au` (en), `ca` (en, fr), `in` (en), `id` (id, en), `my` (en), `ph` (en), `sg` (en), `th` (th, en), `vn` (vi, en) | AUD, CAD, INR, IDR, MYR, PHP, SGD, THB, VND | product, prices |
| Product + prices | `gb` (en) | GBP | product, prices |
| Product + prices | `de` (de, en), `fr` (fr, en), `es` (es, en), `it` (it, en), `nl` (nl, en), `be` (nl, fr, en) | EUR | product, prices |
| Product + prices | `dk` (en), `se` (en) | DKK, SEK | product, prices |
| Product + prices, Uniqlo's EU store (English, euros) | `at`, `bg`, `cz`, `ee`, `fi`, `gr`, `hr`, `hu`, `ie`, `lt`, `lu`, `lv`, `pl`, `pt`, `ro`, `si`, `sk` | EUR | product, prices |

- 41 markets for product, 38 for prices (not `tw`, `hk`, `cn`: their product codes differ), 6 for search, 3 (`us`, `jp`, `kr`) for everything else.
- The EU store prices in euros in every one of its countries, Poland, Czechia and Hungary included.
- Answering `400` before anything is charged: a market an endpoint does not serve (the message lists the markets it does); `ch`, `no`, `nz`, `mx`, `tr`, `ae`, `il` (no Uniqlo online store) and `ru` (closed); Danish on `dk` and Swedish on `se` (those pages do not carry the product data, use `en`); languages Uniqlo does not offer in a market (`es` on `us`, `en` on `jp` or `kr`, `hi` on `in`, `ms` on `my`).

## Workflow

1. **One item, every country:** take the product id (`items[].product_id` of a search answer, or `E` + the 6-digit code printed on the product page + `-000`). Call `/prices` with `product_id` and up to 10 `countries` (1 credit per market that answered). Each market gives `price`, `promo_price`, `discount_percent`, `on_sale`, `limited_offer`, `price_flags`, `tax`, `title` and the market's own `url`; `not_sold` lists the markets that do not sell it. Store each reading with its time.
2. **Is it on offer:** read `on_sale`, `limited_offer` and `price_flags` (quote the label in `name`). On `us`, `jp`, `kr` and `ca` (and on some items `sg`, `my`, `in`) the flags are the whole story; in Europe, Australia and most of Southeast Asia `promo_price` is below `price`. For a Select Colors/Sizes Only price, read the item's price group `01` with `/product`.
3. **Sizes in stock online (us, jp, kr):** `/stock` with the `product_id` returns every colour x size variant with `status`, `quantity` (capped at 11) and its `l2_id`.
4. **Size in a store (us, jp, kr):** `/store-stock` with that `l2_id` and a `lat` + `lng` (1 credit), or with `product_id` + `color` + `size` (+ `length`) and a point (2 credits); send the `price_group` the variant came from (default `00`). Match `store_code` to `/stores` for the address and hours.
5. **Fit:** `/reviews` with the `product_id`: each review's `fit` (1 tight, 3 true to size, 5 loose) and `purchased_size`; `rating.fit` is the product's average.
6. **Browse:** `/categories` for the tree, then `/category` with a node's `path`. `/deals` (`sale` or `limited_offer`) and `/new-arrivals` for the current lists. `/search` with `query`; read `facets` from the first answer, then filter with those codes in the same market.
7. **Price tracking:** poll `/prices` (or product) on a schedule and store each reading. There is no price history endpoint.

## Parameters

### Shared

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `us` | See Markets (not on prices, which takes `countries`) |
| `language` | string | the market's first | One of the market's languages (`zh-Hant` on `tw`, `hk`; `zh-Hans` on `cn`) |
| `page` | integer | 1 | Results page (search, category, deals, new arrivals) |
| `page_size` | integer | 24 | 1 to 100 (48 on `tw`, `hk`, `cn`); Uniqlo answers up to offset 500 |
| `sort` | string | `featured` | `featured` (Uniqlo's order), `newest`, `price_asc`, `price_desc`, `top_rated` (us jp kr), `best_selling` (tw hk cn) |
| `gender` | string | none | `women`, `men`, `kids`, `baby` (search, deals, new arrivals, categories) |
| `price_group` | string | `00` | `items[].price_group` of a search answer (product, stock, store-stock, prices): `00` is Uniqlo's regular price list, `01` mostly the Select Colors/Sizes Only sale price |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords in the market's language, 1-200 chars (Chinese on `tw`, `hk`, `cn`: English keywords mostly find nothing there) |
| `category_path` | string or array | none | 1 to 4 ids from `/categories` (`22210,23296,23339` is women > bottoms > jeans on `us`) |
| `flag` | string | none | `sale`, `limited_offer`, `new`, `new_color`, `coming_soon`, `online_only` (jp only) |
| `color` | string | none | A colour code from `facets.colors` (`COL09`) or its 2-digit display code (`09`) |
| `size` | string | none | A size code from `facets.sizes` (`SMA004` is M, `INS030` is 30 inch) |
| `price_min` / `price_max` | number | none | Price range in the market's currency |

On `tw`, `hk`, `cn` search takes `query`, `sort`, `page`, `page_size` and the price range only.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | `E479000-000` on uniqlo.com markets; `u` + 13 digits on `tw`, `hk`, `cn` |
| `url` | string | one of | A Uniqlo product link from any market; its market is used unless `country` is sent |

### Prices (`/prices`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | A uniqlo.com product id (`E479000-000`) |
| `countries` | array | `jp`, `us`, `gb`, `de`, `fr`, `kr`, `au`, `ca`, `sg`, `th` | 1 to 10 of the 38 prices markets |
| `language` | string | each market's default | Used for the titles where the market serves it |

### Stock (`/stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | A uniqlo.com product id |

### Store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `l2_id` | string | one of | A variant id, 8 digits (`variants[].l2_id` of stock or product): 1 credit |
| `product_id` + `color` + `size` | string | one of | Product id with `colors[].code` (`COL67`) and `sizes[].code` (`INS028`); add `length` when the product comes in lengths: 2 credits |
| `price_group` | string | `00` | The price group the variant came from (`items[].price_group` of search, or `price_group` of product), with either form. A variant of price group `01` asked as `00` reads out of stock in every store |
| `lat` / `lng` | number | required | A point in the country (40.758, -73.9855 New York; 35.6595, 139.7005 Tokyo; 37.5636, 126.9826 Seoul) |
| `limit` | integer | 10 | Stores, 1 to 10 |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `lat` / `lng` | number | one of | A point in the country, nearest first |
| `store_id` | string | one of | One store (`stores[].store_id`, e.g. `10200154`) |
| `limit` | integer | 10 | Stores per page, 1 to 10 |
| `page` | integer | 1 | 1 to 100 |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | A uniqlo.com product id |
| `page` | integer | 1 | 1 to 1000 |
| `page_size` | integer | 10 | 1 to 25 |
| `sort` | string | `newest` | `newest`, `oldest`, `most_helpful`, `highest`, `lowest` |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | none | What the shopper has typed so far, up to 100 chars. Empty or absent: Uniqlo's trending search words |

### Category (`/category`), deals (`/deals`), new arrivals (`/new-arrivals`), categories (`/categories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_path` | string or array | required (category) | A node's `path` from `/categories`; ids are per market |
| `flag` | string | none | Category only: as on search |
| `type` | string | `sale` | Deals only: `sale` or `limited_offer` |
| `include_subcategories` | boolean | false | Categories only: add level 4 (a much larger answer) |

## Examples

### Prices

```bash
curl -X POST https://api.scavio.dev/api/v1/uniqlo/prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "E479000-000"}'
```

Captured `data` (2026-11-17, the default 10 markets, 10 credits; 3 of 10 markets shown, the rest are in the table above, notes shortened to 1 of 4):

```json
{
  "product_id": "E479000-000",
  "price_group": "00",
  "markets": [
    {
      "country": "jp",
      "language": "ja",
      "currency": "JPY",
      "available": true,
      "title": "バギーバレルレッグジーンズ",
      "product_id": "E479000-000",
      "price": 3990,
      "promo_price": 3990,
      "discount_percent": null,
      "on_sale": true,
      "limited_offer": {
        "name": "11/19まで期間限定価格",
        "start": "2026-11-12T17:00:00.000Z",
        "end": "2026-11-19T17:00:00.000Z"
      },
      "price_flags": [
        {
          "code": "limitedOffer",
          "name": "11/19まで期間限定価格",
          "start": "2026-11-12T17:00:00.000Z",
          "end": "2026-11-19T17:00:00.000Z"
        }
      ],
      "tax": "inclusive",
      "url": "https://www.uniqlo.com/jp/ja/products/E479000-000/00"
    },
    {
      "country": "gb",
      "language": "en",
      "currency": "GBP",
      "available": true,
      "title": "Baggy Barrel Leg Jeans",
      "product_id": "E479000-000",
      "price": 39.9,
      "promo_price": null,
      "discount_percent": null,
      "on_sale": false,
      "limited_offer": null,
      "price_flags": [],
      "tax": "inclusive",
      "url": "https://www.uniqlo.com/uk/en/products/E479000-000/00"
    },
    {
      "country": "sg",
      "language": "en",
      "currency": "SGD",
      "available": false,
      "title": null,
      "product_id": null,
      "price": null,
      "promo_price": null,
      "discount_percent": null,
      "on_sale": null,
      "limited_offer": null,
      "price_flags": [],
      "tax": null,
      "url": null
    }
  ],
  "not_sold": ["sg"],
  "errors": [],
  "count": 10,
  "notes": ["1 credit per market that answered (a market that does not sell the product answers too, and is listed in not_sold); a market that failed is listed in errors and not charged."]
}
```

### Stock (online, per colour and size)

```bash
curl -X POST https://api.scavio.dev/api/v1/uniqlo/stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "E479000-000"}'
```

Captured `data` (US, 2026-11-17; 1 of 55 variants shown):

```json
{
  "product_id": "E479000-000",
  "price_group": "00",
  "title": "Barrel Jeans",
  "variants": [
    {
      "l2_id": "09463522",
      "sku": "487973-04-022-000",
      "color": {"code": "COL04", "display_code": "04", "name": "GRAY"},
      "size": {"code": "INS022", "display_code": "022", "name": "22inch"},
      "length": null,
      "price": 39.9,
      "promo_price": 39.9,
      "on_sale": true,
      "price_flags": [{"code": "limitedOffer", "name": "Limited-Time Offer until 11/18", "start": "2026-11-12T13:00:00.000Z", "end": "2026-11-19T13:00:00.000Z"}],
      "sold_online": true,
      "status": "in_stock",
      "status_raw": "IN_STOCK",
      "quantity": 11,
      "quantity_capped": true,
      "back_in_stock": false,
      "in_transit": false
    }
  ],
  "variants_total": 55,
  "variants_in_stock": 40,
  "country": "us",
  "language": "en",
  "currency": "USD",
  "notes": ["Online stock, not store stock (store-stock answers per store). status is Uniqlo's own: in_stock, low_stock or out_of_stock. Uniqlo caps the quantity it shows at 11 (quantity_capped: true means 11 or more)."]
}
```

### Store stock

```bash
curl -X POST https://api.scavio.dev/api/v1/uniqlo/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"l2_id": "08665900", "lat": 40.758, "lng": -73.9855}'
```

Captured `data` (US, near Times Square, 2026-11-17, 1 credit; 1 of 10 stores shown). `08665900` is the BLUE 29inch variant in price group `00` (the default, so the request does not send it): 10 of the 10 stores nearest the point had it, 5 `in_stock` and 5 `low_stock`. Online stock (`/stock`) and store stock are different answers.

```json
{
  "l2_id": "08665900",
  "price_group": "00",
  "point": {"lat": 40.758, "lng": -73.9855},
  "stores": [
    {
      "store_code": "131876",
      "name": "UNIQLO Bryant Park at 5th Avenue",
      "distance_km": 0.6,
      "status": "in_stock",
      "status_raw": "IN_STOCK",
      "store_status": "open",
      "order_and_pick": true,
      "sections": {"women": true, "men": true, "kids": false, "baby": false, "maternity": false}
    }
  ],
  "count": 10,
  "stores_with_stock": 10,
  "total_stores": 93,
  "country": "us",
  "language": "en",
  "currency": "USD",
  "notes": [
    "Store stock, not online stock: status per store is Uniqlo's own (in_stock, low_stock, out_of_stock); Uniqlo shows no unit counts per store. distance_km from the point. store_code matches stores[].store_code of the stores answer.",
    "price_group is the variant's price group (default 00): a variant of price group 01 asked as 00 reads out of stock in every store, so send the price group the l2_id or product came from.",
    "Uniqlo does not refuse an unknown l2_id (it answers every store out of stock): take l2_id from stock or product."
  ]
}
```

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/uniqlo/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "E479000-000"}'
```

Captured `data` (US, 2026-11-17; 1 of 10 reviews shown):

```json
{
  "product_id": "E479000-000",
  "rating": {
    "average": 4.7,
    "count": 607,
    "fit": 3.17,
    "distribution": {"1": 11, "2": 6, "3": 10, "4": 50, "5": 530}
  },
  "reviews": [
    {
      "review_id": "16993074",
      "rating": 5,
      "title": "Best jeans ever!",
      "text": "I love the fit of the jeans! As a 5’0 woman, I stayed away from barrel jeans because I was afraid that it would look weird. However these barrel jeans have a nice subtle curve to it and it doesn’t look weird — even when you alter them it looks good!",
      "created_at": "2026-11-17T04:56:10.000Z",
      "fit": 3,
      "fit_label": "true_to_size",
      "purchased_size": "25inch",
      "purchased_color": "67 BLUE",
      "height_range": "5'0\" - 5'1\"",
      "weight_range": "130lb - 139lb",
      "age_range": "20 to 24 years",
      "gender": "Female",
      "shoe_size": "US6.5",
      "helpful_count": 0,
      "incentivized": false,
      "syndicated": false
    }
  ],
  "count": 10,
  "total": 607,
  "page": 1,
  "page_size": 10,
  "has_more": true,
  "sort": "newest",
  "country": "us",
  "language": "en",
  "currency": "USD",
  "notes": ["fit is the reviewer's fit rating from 1 (tight) to 5 (loose), 3 true to size; rating.fit is the product's average. Reviewer names and locations are not returned. Dates are ISO."]
}
```

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/uniqlo/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "E471601-000", "country": "gb"}'
```

Captured `data` (UK, 2026-11-17; 1 colour, 1 size and 1 image shown, notes dropped):

```json
{
  "product_id": "E471601-000",
  "price_group": "00",
  "title": "HEATTECH Extra Warm Cashmere Blend Turtleneck T-Shirt (Long Sleeve)",
  "url": "https://www.uniqlo.com/uk/en/products/E471601-000/00",
  "description": "HEATTECH is functional innerwear in which the fabric itself creates warmth by using the moisture that evaporates from the body.\n\n- Subtly sheer fabric can be worn alone or layered. Soft, non-constrictive turtleneck.\n- Absorbs and releases moisture to help keep you feeling fresh.\n- Ultra Stretch fabric conforms to the body for a comfortable fit.\n- Quality care label.",
  "information": "- 03: GRAY / 07: GRAY / 30: NATURAL / 61: BLUE are nuanced shades created by blending colors with varying depths. *The target colors may include colors that are not available.",
  "design_details": null,
  "composition": "57% Acrylic, 28% Viscose, 9% Cashmere, 6% Elastane",
  "washing": "Machine wash up to 40 degrees, gentle cycle, Do not Dry Clean, Not suitable for tumble-drying.",
  "care": null,
  "countries_of_origin": ["BD"],
  "gender": "women",
  "category": {
    "gender": {"id": "37267", "name": "WOMEN"},
    "class": {"id": "105438", "name": "Special Collaborations"},
    "category": {"id": "107393", "name": "UNIQLO : C"},
    "subcategory": {"id": "146200", "name": "Turtle neck"}
  },
  "price": 22.9,
  "promo_price": null,
  "currency": "GBP",
  "discount_percent": null,
  "on_sale": false,
  "limited_offer": null,
  "price_flags": [],
  "tax": "inclusive",
  "flags": [],
  "colors": [{"code": "COL10", "display_code": "10", "name": "PINK", "image": "https://image.uniqlo.com/UQ/ST3/gb/imagesgoods/471601/item/gbgoods_10_471601_3x4.jpg"}],
  "sizes": [{"code": "SMA001", "name": "XXS"}],
  "lengths": [],
  "representative": {"l2_id": "09509184", "sku": "485824-10-001-000", "color_code": "COL10", "size_code": "SMA001"},
  "rating": {
    "average": 4.7,
    "count": 2318,
    "fit": 3.03,
    "distribution": {"1": 32, "2": 23, "3": 43, "4": 181, "5": 2039}
  },
  "review_count": 2318,
  "images": ["https://image.uniqlo.com/UQ/ST3/gb/imagesgoods/471601/item/gbgoods_10_471601_3x4.jpg"],
  "size_chart_url": "https://www.uniqlo.com/uk/en/size/471601_size.html",
  "tags": [{"group": "Material", "name": "HEATTECH"}],
  "best_seller": true,
  "discontinued": false,
  "variants": null,
  "country": "gb",
  "language": "en"
}
```

The same product on `de` the same day: 24.9 EUR, and the same rating count, 2318 (Uniqlo's European markets share one review pool). On `jp` it was 2490 JPY with 15891 ratings, on `kr` 24900 KRW with 1378. `variants` is `null` outside `us`, `jp`, `kr`; there each variant carries `l2_id`, `sku`, colour, size, length, prices, `price_flags` and `sold_online` (stock per size is `/stock`).

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/uniqlo/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "heattech"}'
```

Captured `data` (US, 2026-11-17; 1 of 24 items, 1 of each colour, size and facet list shown, notes dropped):

```json
{
  "query": "heattech",
  "items": [
    {
      "product_id": "E471601-000",
      "price_group": "00",
      "title": "HEATTECH Cashmere Blend T-Shirt | Extra Warm | Turtleneck",
      "url": "https://www.uniqlo.com/us/en/products/E471601-000/00",
      "gender": "women",
      "price": 29.9,
      "promo_price": null,
      "currency": "USD",
      "discount_percent": null,
      "on_sale": false,
      "limited_offer": null,
      "price_flags": [],
      "flags": [],
      "colors": [{"code": "COL38", "display_code": "38", "name": "DARK BROWN"}],
      "sizes": [{"code": "SMA002", "name": "XS"}],
      "lengths": [],
      "rating": 4.6,
      "review_count": 496,
      "image": "https://image.uniqlo.com/UQ/ST3/us/imagesgoods/471601/item/usgoods_38_471601_3x4.jpg",
      "store_only": false
    }
  ],
  "count": 24,
  "total": 107,
  "page": 1,
  "page_size": 24,
  "has_more": true,
  "sort": "featured",
  "filters": {},
  "facets": {
    "colors": [{"code": "COL00", "name": "WHITE", "group": "white"}],
    "sizes": [{"code": "BNC080", "name": "Age12-18M(80)"}],
    "lengths": [{"code": "SLA020", "name": "Regular", "count": 1}],
    "flags": [{"flag": null, "code": "multibuy", "name": "Multibuy", "count": 40}],
    "price_ranges": [{"min": 0, "max": 10, "count": 55}],
    "genders": [{"id": 22210, "name": "Women"}],
    "classes": [{"id": 23295, "name": "T-Shirts, Sweats & Fleece"}],
    "categories": [{"id": 68332, "name": "Tops"}]
  },
  "related_keywords": ["heattech+ultra+warm"],
  "country": "us",
  "language": "en",
  "currency": "USD"
}
```

Greater China search (captured on `tw`, query 牛仔褲, 2026-11-17): 66 results; the first item is `u0000000055478` (`style_code` 490536) "直筒牛仔褲" at `price` 1290, `promo_price` 990 TWD, `discount_percent` 23, `on_sale` true, a limited offer ending 2026-11-19, with `in_stock` and `season`; colours and sizes come as codes only. On `hk` (41 results) and `cn` (79) the first items were also below their regular price.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/uniqlo/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"lat": 40.758, "lng": -73.9855}'
```

Captured `data` (US, 2026-11-17; 1 of 10 stores shown, Monday to Thursday hours dropped):

```json
{
  "point": {"lat": 40.758, "lng": -73.9855},
  "stores": [
    {
      "store_id": "10200154",
      "store_code": "131876",
      "name": "UNIQLO Bryant Park at 5th Avenue",
      "address": "510 5th Avenue, New York, NY 10036",
      "postal_code": "10036",
      "city": "New York",
      "region": "NY",
      "country": "United States",
      "lat": 40.75429020916058,
      "lng": -73.9806914,
      "distance_km": 0.6,
      "phone": "1-855-486-4756",
      "opening_hours": {"fri": {"open": "10:00", "close": "20:00"}, "sat": {"open": "10:00", "close": "20:00"}, "sun": {"open": "11:00", "close": "20:00"}},
      "today": {"open": "10:00", "close": "20:00"},
      "status": "open",
      "store_type": "standard",
      "open_date": "2026-03-06",
      "click_and_collect": true,
      "inventory_shown": true,
      "pickup_location": "1st floor cashier",
      "sections": ["women"],
      "services": [],
      "accessibility": []
    }
  ],
  "count": 10,
  "total": 93,
  "page": 1,
  "limit": 10,
  "has_more": true,
  "country": "us",
  "language": "en",
  "currency": "USD"
}
```

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/uniqlo/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "jea"}'
```

Captured `data` (US, 2026-11-17; 3 of 10 suggestions and 1 of 6 categories shown, notes dropped):

```json
{
  "query": "jea",
  "suggestions": ["jw anderson women jeans", "baggy jeans", "Barrel jeans"],
  "categories": [{"id": 23339, "title": "Jeans", "gender_id": 22210, "gender": "Women", "parent_id": 23296, "parent": "Bottoms"}],
  "features": [{"title": "NY POP ART UT", "url": "https://www.uniqlo.com/us/en/spl/ut/ny-pop-art"}],
  "count": 10,
  "country": "us",
  "language": "en",
  "currency": "USD"
}
```

### Other endpoints (captured 2026-11-17, US)

- `/deals` with `{"type": "limited_offer"}`: 62 items; the first, `E494100-000` "Baggy Barrel Jeans", at `price` 39.9 and `promo_price` 39.9 USD with `limited_offer` "Limited-Time Offer until 11/18". Items have the search item shape.
- `/new-arrivals` with `{"gender": "women"}`: 38 items flagged New (`flags: ["salesStart"]`), the first `E493371-000` "mofusand UT Graphic T-Shirt" at 29.9 USD.
- `/category` with `{"category_path": "22210,23296,23339"}` (women > bottoms > jeans): 30 items, 14 of them flagged Limited-Time Offer in `facets.flags`.
- `/categories`: 254 nodes, each with `id`, `name`, `key`, `level` (1 gender, 2 class, 3 category, 4 subcategory), `gender_id`, `parent_id` and `path` (the ids to pass as `category_path`).

### Python

```python
import time
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def uniqlo(endpoint, body, timeout=180):
    r = requests.post(f"{BASE}/api/v1/uniqlo/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()["data"]

PRODUCT_ID = "E479000-000"  # uniqlo.com ids are the same in every market
MARKETS = ["jp", "us", "gb", "de", "fr", "kr", "au", "ca", "sg", "th"]  # up to 10 per call

captured_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
d = uniqlo("prices", {"product_id": PRODUCT_ID, "countries": MARKETS})  # 1 credit per market
for m in d["markets"]:
    if not m["available"]:
        print(m["country"], "not sold")
        continue
    offer = m["limited_offer"]["name"] if m["limited_offer"] else ""  # Uniqlo's own label
    promo = m["promo_price"] if m["promo_price"] is not None and m["promo_price"] < m["price"] else ""
    print(captured_at, m["country"], m["price"], m["currency"], m["tax"], "promo", promo, "offer", offer)
for e in d["errors"]:
    print(e["country"], "no answer (not charged)")

# Store each row with captured_at and run this on a schedule: that stored series is
# your price history (Uniqlo publishes none). Currencies differ and US / Canada prices
# exclude sales tax: convert explicitly, with the rate and its date, before comparing.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live; nothing is cached. Prices are numbers in the market's currency, never converted. `notes` appears when there is something to say.

- **Grid item** (search, category, deals, new arrivals on us jp kr) - `product_id`, `price_group`, `title`, `url`, `gender`, `price`, `promo_price`, `currency`, `discount_percent`, `on_sale`, `limited_offer`, `price_flags`, `flags` (Uniqlo's raw flag codes), `colors[]` {`code`, `display_code`, `name`}, `sizes[]` {`code`, `name`}, `lengths`, `rating`, `review_count`, `image`, `store_only`.
- **Greater China item** (search on tw hk cn) - `product_id` (u-code), `style_code`, `title`, `url`, `gender`, `price`, `promo_price`, `max_price`, `discount_percent`, `on_sale`, `limited_offer`, `flags`, `currency`, `colors[]` {`code`}, `sizes[]` {`code`}, `rating`, `review_count`, `in_stock`, `season`, `image`.
- **search / category / deals / new arrivals** - `items[]`, `count`, `total`, `page`, `page_size`, `has_more`, `sort`, `facets` {`colors`, `sizes`, `lengths`, `flags`, `price_ranges`, `genders`, `classes`, `categories`}. Search adds `query`, `filters`, `related_keywords`; category adds `category_path`; deals adds `type`, `gender`; new arrivals adds `gender`.
- **product** - `product_id`, `price_group`, `title`, `url`, `description`, `information`, `design_details`, `composition`, `washing`, `care`, `countries_of_origin`, `gender`, `category` {`gender`, `class`, `category`, `subcategory` each {`id`, `name`}}, `price`, `promo_price`, `currency`, `discount_percent`, `on_sale`, `limited_offer`, `price_flags`, `lowest_price_30d` (when Uniqlo shows it), `tax`, `flags`, `colors[]` {`code`, `display_code`, `name`, `image`}, `sizes[]`, `lengths[]`, `representative`, `rating` {`average`, `count`, `fit`, `distribution`}, `review_count`, `images`, `size_chart_url`, `tags[]` {`group`, `name`}, `best_seller`, `discontinued`, `variants` (us jp kr; else `null`).
- **prices** - `product_id`, `price_group`, `markets[]` {`country`, `language`, `currency`, `available`, `title`, `product_id`, `price`, `promo_price`, `discount_percent`, `on_sale`, `limited_offer`, `price_flags`, `lowest_price_30d` (when shown), `tax`, `url`}, `not_sold`, `errors[]`, `count`.
- **stock** - `product_id`, `price_group`, `title`, `variants[]` {`l2_id`, `sku`, `color`, `size`, `length`, `price`, `promo_price`, `on_sale`, `price_flags`, `sold_online`, `status`, `status_raw`, `quantity`, `quantity_capped`, `back_in_stock`, `in_transit`}, `variants_total`, `variants_in_stock`.
- **store-stock** - `l2_id`, `price_group`, `variant` (when resolved from product, colour and size), `point`, `stores[]` {`store_code`, `name`, `distance_km`, `status`, `status_raw`, `store_status`, `order_and_pick`, `sections`}, `count`, `stores_with_stock`, `total_stores`.
- **stores** - `point`, `stores[]` {`store_id`, `store_code`, `name`, `address`, `postal_code`, `city`, `region`, `country`, `lat`, `lng`, `distance_km`, `phone`, `opening_hours` {`mon` .. `sun` {`open`, `close`}}, `today`, `status`, `store_type`, `open_date`, `click_and_collect`, `inventory_shown`, `pickup_location`, `sections`, `services`, `accessibility`}, `count`, `total`, `page`, `limit`, `has_more`.
- **reviews** - `product_id`, `rating` {`average`, `count`, `fit`, `distribution`}, `reviews[]` {`review_id`, `rating`, `title`, `text`, `created_at`, `fit`, `fit_label`, `purchased_size`, `purchased_color`, `height_range`, `weight_range`, `age_range`, `gender`, `shoe_size`, `helpful_count`, `incentivized`, `syndicated`}, `count`, `total`, `page`, `page_size`, `has_more`, `sort`.
- **suggestions** - `query`, `suggestions[]` (strings), `categories[]` {`id`, `title`, `gender_id`, `gender`, `parent_id`, `parent`}, `features[]` {`title`, `url`}, `count`. With no query: `trending[]` {`text`, `type`, `url`}.
- **categories** - `gender`, `include_subcategories`, `nodes[]` {`id`, `name`, `key`, `level`, `gender_id`, `parent_id`, `path`}, `count`.

## Guardrails

- Product ids are global on uniqlo.com: the same `E479000-000` opens the product in every uniqlo.com market that sells it. `tw`, `hk`, `cn` use their own `u` + 13-digit codes: a uniqlo.com id answers `400` there and a u-code answers `400` elsewhere. `/prices` does not cover Greater China.
- The 6-digit code on the product page is not accepted alone: send `E` + the code + `-000` (`479000` -> `E479000-000`).
- On `us`, `jp`, `kr` and `ca` (and on some items `sg`, `my` and `in`) Uniqlo marks a drop with flags only (`on_sale`, `limited_offer`, `price_flags`), so `promo_price` equals `price`. Never compute a discount or invent a was-price there. In Europe, Australia and most of Southeast Asia `promo_price` is below `price`.
- Quote a limited offer's end with Uniqlo's own label (`price_flags.name`, e.g. "Limited-Time Offer until 11/18"), never a date read from `end`. Sale flags carry a start but no end; Select Colors/Sizes Only carries no dates.
- `price_group` `00` is Uniqlo's regular price list (the default). Search can list the same `product_id` again in group `01`, mostly a Select Colors/Sizes Only sale price; read it with `/product` and `price_group: "01"`. `/prices` compares group `00` unless `price_group` is sent. Not every group-`01` item carries a sale flag.
- `tax` says whether a price includes sales tax (`exclusive` on `us` and `ca` in the capture). Say so when comparing countries.
- `/stock` is ONLINE stock; `/store-stock` is per physical store. Never present one as the other. Online `quantity` is capped at 11 (`quantity_capped: true` means 11 or more); stores show a status only, no unit counts.
- On `/store-stock` send the `price_group` the variant came from: a variant of price group `01` asked as `00` reads out of stock in every store. A store `out_of_stock` for the right price group is Uniqlo's answer, not an error.
- Uniqlo answers an unknown `l2_id` with every store out of stock rather than an error: take `l2_id` from `/stock` or `/product`.
- Ratings are per region: the European markets share one review pool (same count on `gb`, `de`, `fr`), so a European rating is not a UK-only or Germany-only figure. Review texts are served on `us`, `jp`, `kr` only.
- `fit` runs 1 (tight) to 5 (loose), 3 true to size; `null` when the reviewer gave none. Reviewer names and locations are not returned; never claim them.
- Search, stock, store stock, stores, reviews, suggestions, category, deals, new arrivals and categories are `us`, `jp`, `kr` only (search also `tw`, `hk`, `cn`). On the other markets only product and prices work: say so per market rather than claiming every endpoint everywhere.
- Category ids are per market (women is `22210` on `us`, `1071` on `jp`, `57892` on `kr`): take them from `/categories` on the same market.
- Not available: price history (poll and store), store-level prices, checkout. GU is a separate brand and not a separate platform here; Uniqlo's own listings can include GU collaboration items (`kr` limited offers did), and they come back as Uniqlo lists them.
- Terms: Scavio fetches the public Uniqlo page when your request asks for it and returns it as JSON (no stored dataset, no response cache). Uniqlo's terms of use cover how its website and content may be used; review them for your use case and get your own advice. This is not legal advice. Do not republish Uniqlo product photos, campaign images or logos; link product pages instead.
- Never fabricate prices, ids, sizes, stock, store details or reviews. Only return what the API returned, with the country, the currency and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` the endpoint does not serve (the message lists the markets it does), a country with no Uniqlo online store (`ch`, `no`, `nz`, `mx`, `tr`, `ae`, `il`, `ru`), a language the market does not serve (`da` on `dk`, `sv` on `se`, `es` on `us`, `en` on `jp` / `kr`); a product id in the wrong form for the market; both or neither of `product_id` and `url`; both or neither of `l2_id` and `product_id` on store-stock, or `product_id` without `color` and `size`; a product with several lengths for that colour and size without `length`; neither `lat` + `lng` nor `store_id` on stores; filters other than query, sort, page and price range on `tw` / `hk` / `cn` search; `flag: online_only` outside `jp`; more than 10 `countries`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Uniqlo does not sell ... on ... (or no such product).", "No Uniqlo store ... on ....", "... has no variant in colour ... and size ... on ....". Take ids from a previous answer rather than guessing them; on `/prices` a market that does not sell the product is in `not_sold`, not a 404.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api).
- `502` means Uniqlo data was temporarily unavailable ("Uniqlo is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds. On `/prices` a market that fails is listed in `errors` and not charged; the other markets still answer.
- `503` with a `Retry-After` header means Uniqlo is busy ("Uniqlo is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.67.0
npm install scavio@0.68.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: prices } = await scavio.uniqlo.prices({ product_id: "E479000-000", countries: ["jp", "us", "gb", "kr"] });
const { data: found } = await scavio.uniqlo.search({ query: "heattech", country: "jp" });
const { data: item } = await scavio.uniqlo.product({ product_id: "E471601-000", country: "gb" });
const { data: online } = await scavio.uniqlo.stock({ product_id: "E479000-000" });
const { data: inStores } = await scavio.uniqlo.storeStock({ l2_id: "08665900", lat: 40.758, lng: -73.9855 });
const { data: stores } = await scavio.uniqlo.stores({ lat: 40.758, lng: -73.9855 });
const { data: reviews } = await scavio.uniqlo.reviews({ product_id: "E479000-000", sort: "most_helpful" });
const { data: typed } = await scavio.uniqlo.suggestions({ query: "jea" });
const { data: jeans } = await scavio.uniqlo.category({ category_path: "22210,23296,23339", sort: "price_asc" });
const { data: offers } = await scavio.uniqlo.deals({ type: "limited_offer" });
const { data: fresh } = await scavio.uniqlo.newArrivals({ gender: "women" });
const { data: tree } = await scavio.uniqlo.categories({ gender: "women" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.uniqlo.search(...)`, `client.uniqlo.product(...)`, `client.uniqlo.prices(...)`, `client.uniqlo.stock(...)`, `client.uniqlo.store_stock(...)`, `client.uniqlo.stores(...)`, `client.uniqlo.reviews(...)`, `client.uniqlo.suggestions(...)`, `client.uniqlo.category(...)`, `client.uniqlo.deals(...)`, `client.uniqlo.new_arrivals(...)` and `client.uniqlo.categories(...)`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all twelve endpoints as tools: `search_uniqlo`, `get_uniqlo_product`, `get_uniqlo_prices`, `get_uniqlo_stock`, `get_uniqlo_store_stock`, `get_uniqlo_stores`, `get_uniqlo_reviews`, `get_uniqlo_suggestions`, `get_uniqlo_category`, `get_uniqlo_deals`, `get_uniqlo_new_arrivals` and `get_uniqlo_categories`. Uniqlo is opt-in: add `uniqlo` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.67.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,uniqlo"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/uniqlo-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api), [product](https://scavio.dev/docs/uniqlo-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api), [prices](https://scavio.dev/docs/uniqlo-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api), [stock](https://scavio.dev/docs/uniqlo-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api), [store stock](https://scavio.dev/docs/uniqlo-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api), [stores](https://scavio.dev/docs/uniqlo-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api), [reviews](https://scavio.dev/docs/uniqlo-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api), [suggestions](https://scavio.dev/docs/uniqlo-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api), [category](https://scavio.dev/docs/uniqlo-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api), [deals](https://scavio.dev/docs/uniqlo-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api), [new arrivals](https://scavio.dev/docs/uniqlo-new-arrivals?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api), [categories](https://scavio.dev/docs/uniqlo-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api). Overview: [Uniqlo API](https://scavio.dev/uniqlo-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=uniqlo-api).
