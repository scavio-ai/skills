# QVC + HSN API - Today's Special Value, On-Air Items, Program Guide, Reviews

Read QVC (qvc.com, plus QVC UK, Germany, Italy and Japan) and HSN (hsn.com), the video shopping networks of QVC Group: keyword search, one product in full with every variant, up to 20 QVC items in one call, today's special on each network, the item on air now on every QVC channel, the TV program guide, the items HSN presented in one show hour, a qvc.com category or collection grid, QVC search suggestions and the first page of reviews. `site` picks `qvc` (default) or `hsn`; `market` picks the QVC storefront. Every endpoint returns structured JSON at 1 credit per call.

**The job this skill is for: what QVC and HSN are selling right now, and at what price.** Today's deal, the item on air on each channel, and the price, everyday price, special price window and instalment plan behind each. On 2026-11-27 `/todays-special` on QVC returned the Diamonique Set of 5 Boxed Jewelry Gifts (`J463591`) at $49.98 against a `qvc_price` of $67.00 and a `retail_value` of $124.24 ("If Purchased Separately"), 5 Easy Payments of $10.00, free standard shipping, 3 color variants all `in_stock`, and the Today's Special Value window from 2026-11-25T20:50:00Z to 2026-12-05T06:10:00Z. On HSN it returned a ROTOflash set of 2 rechargeable flashlights (`23926884`) at $39.99, original price $59.99, 5 FlexPay payments of $8.00, with HSN's countdown "01:43:54". `/on-air` listed the item on air on all 4 QVC channels (QVC, QVC2, QVC3, QVC Home), each with its price summary. The second job is the catalog: `/search` for "blender" on QVC US read 102 results, the first the Ninja Professional Plus Duo Blender with Auto IQ (`K82223`) at $99.98 against a QVC price of $159.99 (code SPB, "Black Friday Sale"), 4.67 stars from 950 reviews and 120 added to cart last week. Pair it with `amazon-product-data`, `walmart-product-data` and `google-shopping-api` to see the same brand item elsewhere (QVC returns no UPC: match on brand and model name).

Eight limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit, reviews and today's special included. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Not every endpoint serves every site and market.** search and product: QVC us, uk, de, it, jp and HSN. products (batch): QVC us and it. todays-special, program-guide, reviews: QVC us and HSN. on-air and category: QVC us only. suggestions: QVC us, uk, de. recently-aired: HSN only. Anything else is an unbilled `400` that names what is available.
- **Reviews are the first page only.** QVC shows the 8 newest, HSN the 12 highest rated, as the product page shows them. There is no paging, sort or star filter. A reviews call takes 20-60 seconds.
- **Price labels are QVC's and HSN's own.** On QVC `price` is the current selling price, `qvc_price` QVC's everyday price, `retail_value` the value QVC states with its reason, and `special_price.code` QVC's price code as given (TSV Today's Special Value, SPB Black Friday Sale, SPR Sale, CPQ Final Sale). On HSN `price` is the current price, `original_price` HSN's struck price and `percent_off` the percent off. Report them as labels; never judge a discount.
- **Stock is a flag, never a unit count on QVC.** QVC variants are `in_stock`, `sold_out` or `waitlist`. HSN variants are `available`, `low_inventory` or `sold_out`, and `units_left` is set only when HSN itself shows a low-inventory count.
- **No host or guest names.** Program guide shows carry the show name as the guide lists it; on-air presenter and guest names are not returned, and a QVC show description that names one is null.
- **HSN categories and HSN suggestions are not served.** HSN search with `department` covers HSN's departments.
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series of today's specials or prices.

QVC and HSN publish no public API for their catalog, prices, program guide or reviews. HSN runs an affiliate programme through a third-party affiliate network (a links programme, not a price or catalog API). This skill reads the public QVC and HSN pages with one Scavio key.

QVC Group, Inc. (formerly Qurate Retail) describes its brands as reaching "more than 200 million homes worldwide via 15 television networks" (QVC Group). Quote this with its source, never from the samples.

See also: the same brand item at Amazon `amazon-product-data`, at Walmart `walmart-product-data`, at Target `target-product-data`; prices across retailers `google-shopping-api`; TikTok Shop live-commerce products `tiktok-shop-api`.

## When to trigger

Use this skill when the user asks to:
- Get today's QVC Today's Special Value or HSN Today's Special with its price, everyday price, window or countdown and instalments
- See what is on air right now on QVC, QVC2, QVC3 and QVC Home, with each item's price
- Read the QVC or HSN TV program guide for a day (QVC in Eastern, Central, Mountain or Pacific time; HSN or HSN2)
- List the items HSN presented in one show hour
- Search QVC US, QVC UK, QVC Germany, QVC Italy, QVC Japan or HSN by keyword, sorted or filtered by brand, price band, rating or department
- Read one QVC or HSN product in full: description, every color and size variant with its stock flag, Easy Pay or FlexPay options, shipping and protection plans
- Price up to 20 QVC item numbers in one call
- List a qvc.com category or collection (Clearance, deals) 96 per page
- Get QVC's search-box suggestions for a partial query
- Read the first page of QVC or HSN reviews with the star distribution, recommend counts and questions

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Calls usually take 2-20 seconds (in the captures: search 3-4, product 3-7, products 3, today's special 7, on-air 8, category 12); reviews take 20-60. Allow a client timeout of at least 90 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Sites and markets | Credits |
|---|---|---|---|
| `POST /api/v1/qvc/search` | Keywords: items with price, QVC price, special price, Easy Pay or FlexPay, stock, rating; total, pages, facets (qvc) or departments (hsn) | qvc us, uk, de, it, jp; hsn | 1 |
| `POST /api/v1/qvc/product` | One product by item number or link: description, bullets, retail value, shipping, variants with stock flags, promotions, protection plans (qvc); FlexPay options, countdown, variants with stock and units left (hsn) | qvc us, uk, de, it, jp; hsn | 1 |
| `POST /api/v1/qvc/products` | Up to 20 QVC item numbers in one call: a price summary per item, in the order asked, and `not_found` | qvc us, it | 1 |
| `POST /api/v1/qvc/todays-special` | QVC's Today's Special Value with its window and the full product; HSN's Today's Special with its countdown, the full product and the Today's Specials list | qvc us; hsn | 1 |
| `POST /api/v1/qvc/on-air` | The item on air now on QVC, QVC2, QVC3 and QVC Home, with its price summary | qvc us | 1 |
| `POST /api/v1/qvc/program-guide` | One day of shows: QVC per channel in 4 time zones; HSN or HSN2 hourly, each hour linked to its items | qvc us; hsn | 1 |
| `POST /api/v1/qvc/recently-aired` | The items HSN presented in one show hour, and the day's other hours | hsn | 1 |
| `POST /api/v1/qvc/category` | A qvc.com category or collection grid, 96 per page, with total and pages | qvc us | 1 |
| `POST /api/v1/qvc/suggestions` | QVC's search-box suggestions and suggested products for a partial query | qvc us, uk, de | 1 |
| `POST /api/v1/qvc/reviews` | The first page of reviews (QVC 8 newest, HSN 12 highest rated), star distribution, recommend counts, questions | qvc us; hsn | 1 |

Markets (`market`, QVC only, default `us`): `us` (qvc.com, USD, en-US), `uk` (qvcuk.com, GBP, en-GB), `de` (qvc.de, EUR, de-DE), `it` (qvc.it, EUR, it-IT) and `jp` (qvc.jp, JPY, ja-JP; QVC Japan is a joint venture). HSN is US only (USD): with `site` `hsn`, `market` must be `us` or left out. Data comes in each storefront's language and currency, and every answer carries `site`, `market`, `language` and `currency`.

## Prices: QVC price, special price, retail value, Easy Pay and FlexPay

QVC items carry:

| Field | Meaning |
|---|---|
| `price`, `price_max` | The current selling price, and the top of the range when variants differ |
| `qvc_price`, `qvc_price_max` | QVC's own everyday price ($159.99 on `K82223`, selling at $99.98) |
| `special_price` | {`code`, `description`, `badge`, `starts_at`, `ends_at`}: QVC's price code as given (TSV Today's Special Value, SPB Black Friday Sale, SPR Sale, CPQ Final Sale) with its window when QVC gives one |
| `retail_value`, `retail_value_reason` | Product: the value QVC states, with its reason as given ("If Purchased Separately") |
| `easy_pay[]` | {`code`, `installments`, `installment_amount`, `text`}: Easy Pay plans as given ("Available for 5 Easy Payments", 5 x $10.00) |
| `shipping_charge`, `shipping_text` | The shipping and handling charge ($0 with "Free Standard S&H") |
| `price_with_shipping`, `qvc_price_with_shipping` | QVC UK, as given |
| `comparison_price` | QVC Italy, as given |
| `price_excluding_tax`, `tax` | QVC Japan product, as given |
| `added_to_cart_last_week`, `sold_last_30_days` | QVC's own counts, as given (120 added to cart last week on `K82223`; 6,482 sold in the last 30 days on `K341654`) |

On a category or collection grid an item carries `price`, `was_price` (the struck price when shown), `price_code` and `easy_pay_count` instead.

HSN items carry `price` (current), `original_price` (HSN's struck price), `percent_off`, `flexpay` {`payments`, `amount`} (the FlexPay plan HSN headlines), `flexpay_options[]` on a product ("2 Payments of $20.00"), `shipping_charge`, `note` ("Free Shipping"), `flag` and `badge` (Customer Pick, Black Friday Deal, Today's Special, Clearance) and `sale_time_remaining`, HSN's countdown as given (days.hours:minutes:seconds, "11.01:45:11").

- Quote "$99.98 at qvc.com on 2026-11-27 (Black Friday Sale; QVC price $159.99; 4 Easy Payments of $25.00)", with the date.
- Quote a special price's window from `special_price.starts_at` and `ends_at` (UTC) when given; QVC can extend TSV pricing past the TV day.
- Report the labels, the window and the arithmetic only. Never judge a QVC price, a retail value or a discount, and never describe how often an item is on special.

## Workflow

1. **Today's deal.** `/todays-special` with `{}` (QVC) or `{"site": "hsn"}`. QVC answers `headline`, `item_number`, `window` and `item` (the full product); HSN answers `current`, `item` and the Today's Specials list `items` (each flagged `today`, `presale` or `post_sale`); `list_complete` false means the list could not be read that time.
2. **On air now.** `/on-air` with `{}`: one entry per QVC channel with `item_number` and the `item` price summary.
3. **The schedule.** `/program-guide` with `date` (YYYY-MM-DD, US Eastern day) and, on QVC, `time_zone` and `channel`; on HSN, `network` (`hsn` or `hsn2`). Each HSN show carries `items_aired` {`date`, `hour`, `network`}: pass it to `/recently-aired` for that hour's items.
4. **Find a product.** `/search` with `query` (in the market's language), or `/category` with a qvc.com `url` or `path`. Each item's `item_number` is the input of product, products and reviews.
5. **Read it in full.** `/product` with `item_number` (QVC US `K341654`; QVC UK, DE, IT, JP digits such as `833632`; HSN `23550176`) or a product `url`. Pick the variant by `color` and `size` and read its `stock`.
6. **Watch a list of items.** `/products` with up to 20 `item_numbers` (QVC us or it): one call prices them all; `not_found` lists the ones that do not exist.
7. **Narrow a QVC search.** `sort`, `page`, `page_size` (1-96) and `filters`: tokens exactly as an earlier answer gives them in `facets[].values[].filter` (`8c::1z139k3` is the Ninja brand; `category::lglv` Kitchen & Food), up to 10, on us, uk and de. On HSN use `department` (a `departments[].code`: `j` Jewelry, `ho` Home, `qc` Kitchen & Food).
8. **Reviews.** `/reviews` with `item_number` or `url`: the first page only, plus totals and questions.
9. **Watching deals or prices:** there is no history. Call `/todays-special`, `/on-air` or `/products` on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Common

| Parameter | Type | Default | Description |
|---|---|---|---|
| `site` | string | `qvc` | `qvc` or `hsn`; a parameter of the other site is refused (`department is not used on site qvc.`) |
| `market` | string | `us` | QVC storefront: `us`, `uk`, `de`, `it`, `jp` (per endpoint, see the table above); HSN serves `us` |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords, 1-200 chars, in the market's language |
| `sort` | string | qvc `relevance`, hsn `featured` | qvc: `relevance`, `newest`, `top_sellers`, `rating`, `recently_on_air`, `price_desc`, `price_asc` (QVC Japan has no `recently_on_air`). hsn: `featured`, `best_selling`, `rating`, `newest`, `price_desc`, `price_asc` |
| `filters` | array or string | none | qvc us, uk, de: facet tokens from `facets[].values[].filter`, up to 10 (a comma-separated string also works); one `category::` token at most |
| `department` | string | none | hsn: a department code from `departments[].code` |
| `page` | integer | 1 | 1-100; `total_pages` reports the last one |
| `page_size` | integer | qvc 24 | qvc: 1-96. hsn: 60 (fixed) |

### Product (`/product`) and reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_number` | string | one of | `items[].item_number`: QVC US a letter and digits (`K341654`), QVC UK, DE, IT, JP digits (`833632`), HSN a product id (`23550176`) |
| `url` | string | one of | A product link (qvc.com /p/<name>/<item>, qvcuk.com, qvc.de, qvc.it, qvc.jp, or hsn.com /products/<name>/<id>), instead of `item_number` (not both) |

### Products (`/products`)

`item_numbers` (required): up to 20 QVC item numbers, as an array or a comma-separated string; duplicates are dropped. `site` is `qvc`; `market` `us` or `it`.

### Program guide (`/program-guide`) and recently aired (`/recently-aired`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `date` | string | today | YYYY-MM-DD, the US Eastern day. qvc: 14 days back to 17 days ahead, as QVC's guide offers |
| `time_zone` | string | `eastern` | qvc guide: `eastern`, `central`, `mountain`, `pacific` |
| `channel` | string | all | qvc guide: one channel by code or name (`QVC`, `2CH` / `QVC2`, `STA` / `QVC3`, `ONQ` / `QVC Home`, ...) |
| `network` | string or integer | `hsn` | hsn: `hsn` (or `1`) or `hsn2` (or `4`) |
| `hour` | integer | latest show | recently-aired: 0-23 (Eastern), with `date`: a guide row's `items_aired.hour` |

`/recently-aired` requires `site` `hsn`.

### Category (`/category`) and suggestions (`/suggestions`)

`/category` (qvc us) takes a qvc.com `url` or its `path` (not both): a category `/c/<name>/-/<group>/c.html` or a collection `/collections/<name>.html` (`/collections/deals-clearance.html`), plus `sort` (the QVC sorts above) and `page` (1-100, 96 per page). `/suggestions` takes `query` (1-100 chars) on qvc us, uk or de.

## Examples

### QVC's Today's Special Value

```bash
curl -X POST https://api.scavio.dev/api/v1/qvc/todays-special \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (2026-11-27; `item` cut to its price, stock and variant fields; `description`, `bullets`, `images`, `categories` and 1 of 3 variants dropped):

```json
{
  "site": "qvc",
  "market": "us",
  "language": "en-US",
  "currency": "USD",
  "headline": "Diamonique® Set of 5 Jewelry Gifts",
  "subline": "Under $50 & Ships Free | Choice of Metal Color",
  "item_number": "J463591",
  "window": { "code": "TSV", "description": "Today's Special Value", "starts_at": "2026-11-25T20:50:00Z", "ends_at": "2026-12-05T06:10:00Z" },
  "item": {
    "item_number": "J463591",
    "title": "Diamonique Set of 5 Boxed Jewelry Gifts",
    "brand": "Diamonique",
    "currency": "USD",
    "price": 49.98,
    "qvc_price": 67,
    "special_price": { "code": "TSV", "description": "Today's Special Value", "badge": null, "starts_at": "2026-11-25T20:50:00Z", "ends_at": "2026-12-05T06:10:00Z" },
    "easy_pay": [
      { "code": "C5", "installments": 5, "installment_amount": 10, "installment_amount_max": null, "text": "Available for 5 Easy Payments", "starts_at": null, "ends_at": null }
    ],
    "shipping_charge": 0,
    "stock": "in_stock",
    "last_on_air": "2026-11-26T20:35:29Z",
    "retail_value": 124.24,
    "retail_value_reason": "If Purchased Separately",
    "shipping_text": "Free Standard S&H",
    "first_available": "2026-11-19T00:00:00Z",
    "sold_last_30_days": 9,
    "max_order_quantity": 5,
    "variant_count": 3,
    "variants": [
      { "color_code": "563", "color": "Goldplate", "size_code": "6XV", "size": "1 pc", "stock": "in_stock", "buyable": true, "price": 49.98, "qvc_price": null, "retail_value": 124.24, "price_with_shipping": null, "delivery_days": null },
      { "color_code": "680", "color": "Silvertone", "size_code": "6XV", "size": "1 pc", "stock": "in_stock", "buyable": true, "price": 49.98, "qvc_price": null, "retail_value": 124.24, "price_with_shipping": null, "delivery_days": null }
    ],
    "promotions": [{ "text": "Free Shipping on Everything! Exclusions Apply. Discount Reflected at Checkout." }],
    "protection_plans": [{ "title": "Allstate 3-Year Contract: Jewelry $25-$50", "price": 9, "years": 3 }]
  }
}
```

`{"site": "hsn"}` answered `current` {`item_number` "23926884", "ROTOflash Set of 2 Rechargeable Flashlight with 4,000mAh Power Bank", `price` 39.99, `original_price` 59.99, `flexpay` {5, 8}, `sale_time_remaining` "01:43:54"} and `item` the full product (6 variants, all `available`, `flag` "Today's Special", `on_air_today` true). In that capture `list_complete` was false and `items` empty: the Today's Specials list could not be read that time, and the current item still came back.

### One QVC search result

```bash
curl -X POST https://api.scavio.dev/api/v1/qvc/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "blender"}'
```

Captured `data.items[0]` (2026-11-27; `total` 102, 5 pages of 24, 26 facet groups):

```json
{
  "position": 1,
  "item_number": "K82223",
  "title": "Ninja Professional Plus Duo Blender with Auto IQ",
  "brand": null,
  "url": "https://www.qvc.com/.product.K82223.html",
  "image": "https://qvc.scene7.com/is/image/QVC/k/23/k82223_012.102",
  "currency": "USD",
  "price": 99.98,
  "price_max": null,
  "qvc_price": 159.99,
  "qvc_price_max": null,
  "price_with_shipping": null,
  "qvc_price_with_shipping": null,
  "special_price": { "code": "SPB", "description": "Black Friday Sale", "badge": "Black Friday Sale Price", "starts_at": null, "ends_at": null },
  "comparison_price": null,
  "easy_pay": [
    { "code": "C4", "installments": 4, "installment_amount": 25, "installment_amount_max": null, "text": "Available for 4 Easy Payments", "starts_at": null, "ends_at": null }
  ],
  "shipping_charge": 0,
  "rating": 4.67,
  "review_count": 950,
  "added_to_cart_last_week": 120,
  "stock": "in_stock",
  "promo_text": ["Free Standard S&H"],
  "colors": ["Black"],
  "last_on_air": null
}
```

The facets held Category (Kitchen & Food 96, filter `category::lglv`), Brand (Ninja 18 `8c::1z139k3`, Vitamix 17 `8c::1z13ejs`, ...), Product Type, Rating, Price and 21 more groups. `{"site": "hsn", "query": "ring"}` answered 687 results over 12 pages of 60 and 10 departments (Jewelry `j` 631, Mens `mn` 16, Home `ho` 13, ...); the first item read $61.96, original price $68, 8% off, 5 FlexPay payments of $12.39, "Free Shipping". HSN search items carry no star rating; product has it.

### Product, products, on-air, program guide, recently aired, category, suggestions and reviews

- `/product` `{"item_number": "K341654"}`: GE Profile Opal Mini Pro Nugget Ice Maker w/ Side Tank at $279.98, `qvc_price` $379, special price TSV from 2026-11-23T06:10Z to 2026-12-01T06:10Z, 5 Easy Payments of $56, free standard S&H, 4.43 stars from 46 reviews, `sold_last_30_days` 6,482, `max_order_quantity` 5, 1 variant `in_stock`, an Allstate 3-year protection plan at $44.99. `{"site": "hsn", "item_number": "20315209"}`: a legging at $22.96, original price $27, `flag` "Customer Pick", 6 FlexPay options from a single payment of $22.96 to 6 payments of $3.83 (`flexpay` 5 x $4.59 as HSN headlines it), `sale_time_remaining` "11.01:45:11", 4.2 stars from 41 reviews, 31 color and size variants each with its own HSN item number and `stock` (`available`, `low_inventory` or `sold_out`). An unknown item is a charged `404`.
- `/products` `{"item_numbers": ["K341654", "K82223"]}`: both found, in the order asked; the Ninja Professional Plus Duo Blender at $99.98 (QVC price $159.99, SPB Black Friday Sale ending 2026-12-06T06:10:00Z, 4 Easy Payments of $25).
- `/on-air` `{}`: 4 channels; on QVC (`QVC`) a Fire Light Lab Grown Diamonds 3.00 ctw Station Bracelet (`J468559`) at $599.98 (QVC price $744, SPR Sale to 2026-12-21T06:10Z); on QVC3 (`STA`) a Bolsetta pouch at $24.98 (SPB Black Friday Sale); on QVC Home (`ONQ`) a Takker 73-piece hanging kit at $13.99 (QVC price $28, CPQ Final Sale).
- `/program-guide` `{"date": "2026-11-26", "channel": "QVC"}`: 14 shows on the QVC channel in Eastern time, the first from 00:00 to 01:00 "Diamonique(R) Jewelry Gifts - All Sale Prices - All New" (show code `DQG`). `{"site": "hsn", "date": "2026-11-26"}`: 24 hourly shows on HSN, "Black Friday Deals" at midnight, each with `items_aired` {`date`, `hour`, `network`}.
- `/recently-aired` `{"site": "hsn"}`: the latest show hour (9:00 PM - 10:00 PM Eastern on 2026-11-26) with 2 items: a Brookstone Neck & Shoulder Massager at $49.99 (original $59.99, 16% off, `flag` "Black Friday Deal") and the ROTOflash flashlight set at $39.99 (`flag` "Today's Special"); `shows` held the day's 24 hours.
- `/category` `{"path": "/collections/deals-clearance.html"}`: "QVC Clearance Sale", `total` 8,551, 90 pages of 96; the first item, a Kringle Express Oversized 60x80 Holiday Printed Throw (`H500429`), at $11.99, `price_code` CPQ, 2 Easy Payments, 4.7 stars from 33 reviews, 1,782 added to cart last week. An unknown link is a charged `404`: "No QVC category or collection at this link."
- `/suggestions` `{"query": "blen"}`: blender, blenders on sale, blendjet portable blender, blendtec, vitamix blender, ... (7), and 4 suggested products with the search item fields.
- `/reviews` `{"item_number": "K82223"}`: the 8 newest of 918 written reviews (`review_count` 950 with rating-only reviews), average 4.67, distribution {5: 795, 4: 77, 3: 27, 2: 18, 1: 33}, 606 recommend and 47 do not; the first, 5 stars, "Must-have for smoothies!", was `syndicated` from influenster.com. No reviewer names, nicknames or locations.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def qvc(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/qvc/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Today's deal on both networks (1 credit each)
tsv = qvc("todays-special", {})["data"]
print(tsv["item_number"], tsv["item"]["title"], tsv["item"]["price"], tsv["item"]["qvc_price"], tsv["window"])
hsn = qvc("todays-special", {"site": "hsn"})["data"]["current"]
print(hsn["item_number"], hsn["title"], hsn["price"], hsn["original_price"], hsn["sale_time_remaining"])

# 2. What is on air on each QVC channel (1 credit)
for c in qvc("on-air", {})["data"]["channels"]:
    item = c["item"] or {}
    print(c["channel"], c["item_number"], item.get("price"), (item.get("special_price") or {}).get("description"))

# 3. Price a watch list of QVC items in one call (1 credit)
batch = qvc("products", {"item_numbers": ["K341654", "K82223"]})["data"]
for i in batch["items"]:
    print(i["item_number"], i["price"], i["qvc_price"], i["special_price"])

# Prices and specials change between calls. Store each answer with
# fetched_at and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it; nothing is cached. Every `data` carries `site`, `market`, `language`, `currency` and `notes`.

- **qvc item** (search, suggestions products) - `position`, `item_number`, `title`, `brand`, `url`, `image`, `currency`, `price`, `price_max`, `qvc_price`, `qvc_price_max`, `price_with_shipping`, `qvc_price_with_shipping`, `special_price` {`code`, `description`, `badge`, `starts_at`, `ends_at`}, `comparison_price`, `easy_pay[]` {`code`, `installments`, `installment_amount`, `installment_amount_max`, `text`, `starts_at`, `ends_at`}, `shipping_charge`, `rating`, `review_count`, `added_to_cart_last_week`, `stock`, `promo_text`, `colors`, `last_on_air`.
- **hsn item** (search, today's specials list, recently aired) - `position`, `item_number`, `sku`, `title`, `brand`, `url`, `image`, `currency`, `price`, `original_price`, `percent_off`, `flexpay` {`payments`, `amount`}, `shipping_charge`, `note`, `flag`, `todays_special` {`today`, `presale`, `post_sale`}, `badge`, `on_air_today`, `available`, `categories[]` {`id`, `name`}.
- **search** - `query`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `sort`, `items[]`; qvc adds `filters_applied` and `facets[]` {`id`, `name`, `multi_select`, `values[]` {`name`, `count`, `filter`, `selected`}}; hsn adds `department` and `departments[]` {`code`, `name`, `count`}.
- **qvc product** - the qvc item fields plus `brand_id`, `description`, `bullets`, `retail_value`, `retail_value_max`, `retail_value_reason`, `price_excluding_tax`, `tax`, `shipping_text`, `two_man_handling`, `auto_delivery` {`text`}, `first_available`, `sold_last_30_days`, `max_order_quantity`, `categories[]` {`id`, `name`}, `images`, `variant_count`, `variants[]` {`color_code`, `color`, `size_code`, `size`, `stock`, `buyable`, `price`, `qvc_price`, `retail_value`, `price_with_shipping`, `delivery_days`}, `promotions[]` {`text`}, `protection_plans[]` {`title`, `price`, `years`}.
- **hsn product** - `item_number`, `sku`, `item_code`, `title`, `brand`, `url`, `image`, `price`, `original_price`, `shipping_charge`, `flexpay`, `flexpay_options[]` {`text`, `payments`, `amount`, `card_only`}, `flag`, `todays_special`, `sale_time_remaining`, `on_air_today`, `rating`, `review_count`, `has_warranty`, `primary_category` {`id`, `name`}, `description`, `images`, `low_inventory_level`, `variant_count`, `variants[]` {`item_number`, `sku`, `color_code`, `color`, `size_code`, `size`, `plus_size`, `stock`, `units_left`}.
- **products** - `requested`, `count`, `items[]` {`item_number`, `title`, `brand`, `url`, `image`, `currency`, `price`, `price_max`, `qvc_price`, `retail_value`, `special_price`, `easy_pay`, `rating`, `review_count`, `stock`}, `not_found`.
- **todays-special** - qvc: `headline`, `subline`, `item_number`, `window` {`code`, `description`, `starts_at`, `ends_at`}, `item` (qvc product). hsn: `current` {`item_number`, `title`, `price`, `original_price`, `flexpay`, `sale_time_remaining`, `url`, `image`}, `item` (hsn product), `count`, `items[]` (hsn items), `list_complete`.
- **on-air** - `count`, `channels[]` {`channel_code`, `channel`, `item_number`, `item` (the products summary, or null)}.
- **program-guide** - qvc: `date`, `time_zone`, `channel_count`, `show_count`, `channels[]` {`channel_code`, `channel`, `shows[]` {`start`, `end`, `duration_hours`, `show_name`, `show_code`, `source_code`, `description`}}. hsn: `date`, `network`, `time_zone`, `show_count`, `shows[]` {`time`, `start`, `hour`, `show_name`, `network`, `items_aired` {`date`, `hour`, `network`}}.
- **recently-aired** - `date`, `hour`, `network`, `show` {`time`, `start`, `hour`, `show_name`, `selected`}, `count`, `items[]` (hsn items), `shows[]`.
- **category** - `path`, `url`, `title`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `sort`, `items[]` {`position`, `item_number`, `title`, `url`, `image`, `currency`, `price`, `was_price`, `price_code`, `easy_pay_count`, `promo_text`, `rating`, `review_count`, `added_to_cart_last_week`, `colors_available`}.
- **suggestions** - `query`, `count`, `suggestions` (terms), `products[]` (qvc items).
- **reviews** - `item_number`, `page` (always 1), `order` (`newest` on qvc, `highest_rated` on hsn), `count`, `total`, `average_rating`, `review_count`, `ratings_only_count`, `rating_distribution`, `recommended_count`, `not_recommended_count`, `reviews[]` {`review_id`, `rating`, `title`, `text`, `submitted_at`, `recommended`, `syndicated`, `syndicated_from`, `helpful_votes`, `unhelpful_votes`, `pros`, `cons`, `verified_purchaser`, `badges`, `secondary_ratings`, `language`, `photo_count`}, `questions[]` {`question`, `submitted_at`, `answer_count`, `answers[]` {`answer`, `submitted_at`, `is_brand_answer`}}, `questions_total`.

## Guardrails

- Name them "QVC (qvc.com)" and "HSN (hsn.com), the video shopping networks of QVC Group" on first mention, and name the QVC storefront (QVC UK, QVC Germany, QVC Italy, QVC Japan) when the market is not `us`. Shopper accounts are not read.
- Prices: quote `price` with QVC's `qvc_price` and `special_price` (or HSN's `original_price` and `percent_off`), the instalment plan as given, and the `fetched_at` date. Prices are in the storefront's own currency; never convert them without saying so.
- `retail_value` is the value QVC states with its reason; quote it with `retail_value_reason`, never as a price anyone paid.
- Stock: report QVC's `stock` flag and HSN's `stock` and `units_left` exactly as given, at the moment of the call. Never state or estimate a QVC unit count, and never promise availability.
- People: never name on-air hosts, guests or presenters. Some show names as the guide lists them include a presenter's first name: refer to those shows by time and `show_code` instead of repeating the name. No reviewer names are returned.
- Reviews: say it is the first page only (QVC 8 newest, HSN 12 highest rated) and quote `total`, `review_count` and `rating_distribution` for the whole picture. Syndicated reviews were written elsewhere (`syndicated_from`); say so when quoting one.
- Report QVC's and HSN's labels (price codes, badges, flags, countdowns, windows) and the arithmetic only. Never judge a deal, a retail value or a countdown, and never describe how often an item is on special.
- Comparing QVC or HSN with other retailers: compare only the same item (same brand and model), each with its date; label QVC-exclusive and HSN-exclusive lines as different products.
- Not available: review paging, sort or star filters, HSN categories, HSN suggestions, QVC recently aired, on-air host or guest names, QVC unit counts, price history (poll and store), cart, Easy Pay or FlexPay sign-up and checkout. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not store QVC or HSN data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. QVC's and HSN's terms of use cover how their sites and content may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish QVC or HSN product photos, logos or video; link products by `url` instead.
- Never fabricate prices, item numbers, windows, countdowns, show times, stock flags, dates or ratings. Only return what the API returned, with the `fetched_at` time and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "item_number or url is required", "Pass item_number or url, not both.", "url or path is required", "item_numbers is required", "item_numbers takes at most 20 item numbers."; an item number of the wrong form ("item_number must be a QVC item number (items[].item_number, e.g. K341654).", "item_number must be a QVC UK item number (items[].item_number, digits, e.g. 833632).", "item_number must be an HSN product id (items[].item_number, e.g. 23550176)."); a link of the wrong site ("url must be an hsn.com product link.", "url must be a qvc.com category (/c/<name>/-/<group>/c.html) or collection (/collections/<name>.html) link."); an endpoint asked for a site or market it does not serve ("on-air is available on site qvc (not hsn).", "suggestions on site qvc is available for market us, uk, de.", "HSN serves market us."); a parameter of the other site ("filters is not used on site hsn."); "filters work on QVC us, uk and de.", "filters must be facet tokens from facets[].values[].filter, e.g. \"8c::1z139k3\".", "filters takes one category token."; a sort not offered ("sort on site hsn must be one of featured, best_selling, rating, newest, price_desc, price_asc.", "sort recently_on_air is not offered on QVC Japan (...)"); "page_size on site hsn is 60 (HSN's page size)."; a guide date outside QVC's window ("date must be within 14 days back and 17 days ahead of today (US Eastern), as QVC's guide offers."); an unknown `channel` (the message lists the channels); "network must be hsn (1) or hsn2 (4)."; "hour goes with date."; a `page` or `hour` outside its range.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No QVC US product with item number <item_number>.", "No HSN product with id <item_number>.", "None of these item numbers exist.", "No QVC category or collection at this link.", "No Today's Special Value is shown right now.", "Nothing is on air right now.", "No guide for this date.", "No shows for this date.", "No results.", "No suggestions.". Take item numbers and links from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api).
- `502` means QVC or HSN data was temporarily unavailable ("QVC is temporarily unavailable. Please try again.", "HSN is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the sites are busy ("QVC and HSN are busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.100.0
npm install scavio@0.101.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: tsv } = await scavio.qvc.todaysSpecial({});
const { data: hsnDeal } = await scavio.qvc.todaysSpecial({ site: "hsn" });
const { data: live } = await scavio.qvc.onAir({});
const { data: hits } = await scavio.qvc.search({ query: "blender", filters: ["8c::1z139k3"] });
const { data: rings } = await scavio.qvc.search({ site: "hsn", query: "ring", department: "j" });
const { data: item } = await scavio.qvc.product({ item_number: "K341654" });
const { data: watch } = await scavio.qvc.products({ item_numbers: ["K341654", "K82223"] });
const { data: guide } = await scavio.qvc.programGuide({ date: "2026-11-26", channel: "QVC" });
const { data: aired } = await scavio.qvc.recentlyAired({ site: "hsn", date: "2026-11-26", hour: 20 });
const { data: clearance } = await scavio.qvc.category({ path: "/collections/deals-clearance.html" });
const { data: typed } = await scavio.qvc.suggestions({ query: "blen" });
const { data: reviews } = await scavio.qvc.reviews({ item_number: "K82223" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.qvc.search(...)`, `product`, `products`, `todays_special`, `on_air`, `program_guide`, `recently_aired`, `category`, `suggestions` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 10 endpoints as tools: `search_qvc`, `get_qvc_product`, `get_qvc_products`, `get_qvc_todays_special`, `get_qvc_on_air`, `get_qvc_program_guide`, `get_qvc_recently_aired`, `get_qvc_category`, `get_qvc_suggestions` and `get_qvc_reviews`. QVC + HSN is opt-in: add `qvc` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.100.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,qvc"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/qvc-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api), [product](https://scavio.dev/docs/qvc-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api), [products](https://scavio.dev/docs/qvc-products?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api), [today's special](https://scavio.dev/docs/qvc-todays-special?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api), [on air](https://scavio.dev/docs/qvc-on-air?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api), [program guide](https://scavio.dev/docs/qvc-program-guide?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api), [recently aired](https://scavio.dev/docs/qvc-recently-aired?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api), [category](https://scavio.dev/docs/qvc-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api), [suggestions](https://scavio.dev/docs/qvc-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api), [reviews](https://scavio.dev/docs/qvc-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api). Overview: [QVC + HSN API](https://scavio.dev/qvc-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=qvc-hsn-api).
