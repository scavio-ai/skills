# Staples API - Ink Prices, Office Supplies, Store Stock

Read Staples (staples.com, the US office supply retailer; Staples Canada at staples.ca): keyword, model-number and item-number search, class listings and deals, one product in full with Staples' price, Regular price, price per unit, page yield, promotions and coupon codes, the units of one item at the Staples stores near a US ZIP, reviews and customer questions, Staples' public coupons, the stores near a ZIP or a city, one store, the department tree and trending searches. www.staples.com (USD, English) for all 12 endpoints; www.staples.ca (Staples Canada, CAD, English or French) for product and search. Every endpoint returns structured JSON at 1 credit per call.

**The job this skill is for: Staples ink prices.** What a cartridge costs at staples.com today, standard against XL, per page at the yield Staples states, and how many the stores near a ZIP have. On 2026-11-24 the HP 64XL Black High Yield Ink Cartridge (item `2724258`, model `N9J92AN#140`, "Prints Up to 600 Pages") read $62.89 with `page_yield` 600 and Staples' own `price_per_unit` 0.1 "Cost Per Page" ($62.89 / 600 = $0.105). `/store-stock` near ZIP 60540 listed 7 stores with 63 units, 12 at store 1633 (Naperville, IL) and 12 at 1895 (Glen Ellyn, IL), each "Ready in 30 mins". HP 67XL Black (`24430099`, 240 pages) read $35.89 with no cost per page from Staples ($35.89 / 240 = $0.15 a page) and HP 67 Black (`24430098`, 120 pages) $22.89 ($0.19). The second job is copy paper per ream: Hammermill Copy Plus, 10 reams (`122374`), read $49.99 against Staples' "Regular price" $83.19, Staples' own $5.00/Ream, "Offer Expires on 11/28/2026", "Limit 5 at promotional price." Pair it with `amazon-product-data`, `walmart-product-data`, `target-product-data` and `best-buy-product-data` for the same cartridge (same model number): Staples' own price match policy names Amazon.com, Walmart, Target, Best Buy and Office Depot/OfficeMax.

Nine limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Prices are national: the ZIP and the store never change the price.** Measured 2026-11-24: a Staples office chair (`24588453`) read $59.99 at 7 ZIP codes in 7 states including Alaska, the Hammermill carton $49.99 at 4 ZIP codes, and a Hyken chair (`990119`) $125.99 online and for pickup at 3 stores (1574 New York, NY; 1633 Naperville, IL; 0874 Greenfield, MA). The ZIP changes delivery availability and dates; the store changes pickup units. Never write that Staples prices differ by store or by ZIP.
- **`was_price` is Staples' own "Regular price".** It is given only when it is above the price. `discount_percent` is Scavio's arithmetic from the two; `savings` carries Staples' "Instant Savings" amount as given. `promotions` are Staples' own texts and `offer_expires` its expiry date; `coupon_codes` are the codes Staples applies to that price, with its per-order limit.
- **Price per unit and page yield are Staples' own.** `price_per_unit` with `price_per_unit_unit` ("Ream", "Cost Per Page", ...) and `price_per_unit_text` ("$5.00/Ream") appear only where Staples shows them. `page_yield` is the yield Staples states for a cartridge. Where Staples gives no cost per page, divide the price by `page_yield` and show the division; yields are stated, not measured.
- **Store stock lists only stores WITH stock.** `/store-stock` returns the nearest Staples stores that have the item for pickup today (7 to 10 per answer seen), each with `units` as Staples reports them, `pickup_text` ("Ready in 30 mins") and this week's hours. An empty `stores` list means no store within `radius` has it, or the item is not offered for store pickup: the product's `pickup_eligible` says which (HP 67 and 67XL read `false`, and their store list was empty near 10001). Staples returns a `threshold` value (50 in every capture) beside the units; it is reported as given. Never claim the units are capped at it.
- **The item number is the input.** `items[].item_id` (the number after `product_` in a staples.com link) is the input of product, store-stock, reviews and questions. A search for an item number answers with that product (`redirect` {`type`: `product`}). Every pack size is its own item: a product's `variants[]` give the 1-ream, 3-ream, 5-ream, 8-ream, 10-ream and pallet item numbers.
- **No UPC on staples.com.** `model` is the manufacturer's part number as Staples gives it (`N9J92AN#140`, `105007CT/27061`); match other retailers on it. Staples Canada products carry a `barcode` (a UPC for branded items).
- **Staples Canada: product and top matches only.** `country` `ca` reads www.staples.ca (Staples Canada, a separate company) in CAD; `language` `fr` reads www.staples.ca/fr with French names. `/search` gives the top matches Staples Canada's search box shows (about 5), with no paging, sort or filters; `/product` takes a `handle`, a staples.ca link or an `item_id`. The same item number can be on both sites at different prices: HP 67 Black (`24430098`) read $22.89 on staples.com and $34.99 CAD on staples.ca on 2026-11-24. Report each in its own currency; never convert or call one cheaper. Canadian store stock, delivery dates and reviews are not served, and every other endpoint is US only.
- **No history, no member prices.** Guest prices only: no Easy Rewards, Staples Business Advantage contract, teacher or AutoRestock prices. Nothing is cached or kept: poll and store your own series.

Staples has no public API for reading its catalog, prices or store stock. Publishers can join its affiliate programme (a links programme, not a price API); business customers connect their purchasing systems through Staples Business Advantage, which says it is integrated with 170+ eProcurement systems (punchout to the buyer's own contract catalog); suppliers trade EDI. API directory profiles carrying a "Staples Product Catalog API" name are third-party listings, not Staples documents. Prices and store availability are shown on staples.com for the ZIP and store you pick, and this skill reads those public pages with one Scavio key.

Staples says it has 900+ stores in the United States (Staples About Us page). Staples, Inc. is privately held, owned by Sycamore Partners since 2017; Staples Canada is run separately. Quote these with their source, never from the samples.

See also: for the same cartridge or paper at Amazon use `amazon-product-data`; at Walmart `walmart-product-data`; at Target `target-product-data`; at Best Buy `best-buy-product-data`; prices across retailers `google-shopping-api`; per-store stock at other retailers `micro-center-api`, `home-depot-product-data`, `michaels-craft-prices-api`.

## When to trigger

Use this skill when the user asks to:
- Price an HP, Canon or Epson ink cartridge or a toner at Staples, standard against XL, per page at the stated yield, with Staples' own cost per page where it shows one
- Price copy paper at Staples per ream across pack sizes (1, 3, 5, 8, 10 reams, carton, pallet), with Staples' Regular price, promotion text and offer expiry
- Check how many units of one Staples item the stores near a US ZIP have for pickup today
- Search staples.com by keyword, model number or Staples item number, sorted by price, rating or newest, or filtered by brand, price, number of reams, sheet size, brightness or any facet
- List a Staples class (Copy & Printer Paper, laptops, office chairs) or the On Promotion or Clearance products for a keyword or a class
- Read one Staples product in full: specifications, page yield, promotions with expiry, coupon codes, rating breakdown, every pack size, delivery dates for a ZIP and one store's pickup units
- Read the reviews of a Staples item (up to 100 per page, by stars, newest or most helpful) or its customer questions and answers
- List Staples' public coupons with codes and end dates, the trending searches, or the department tree
- Find the Staples stores near a ZIP or a city, or one store's hours and services (print, shredding, UPS, Amazon Lockers, passport services)
- Read one item on Staples Canada (staples.ca) in English or French, in CAD
- Compare one cartridge at Staples, Amazon, Walmart, Target and Best Buy (with `amazon-product-data`, `walmart-product-data`, `target-product-data` and `best-buy-product-data`)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, store-stock, stores, store, questions and trending took under 1 second, search, deals, reviews and categories 2-4, a US product about 5, and a Staples Canada search or product 2-22. Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Markets | Credits |
|---|---|---|---|
| `POST /api/v1/staples/search` | Keywords, a model number or an item number: 40 per page with total, facets, price per unit, Regular price and delivery; Canada: the top matches (about 5) | us, ca | 1 |
| `POST /api/v1/staples/product` | One product by item number or link: price, Regular price, price per unit, page yield, reams and sheets, promotions with expiry, coupon codes, specifications, rating breakdown, Staples' review summary, every pack size, delivery dates for a ZIP, one store's pickup units; Canada: price in CAD, barcode, variants | us, ca | 1 |
| `POST /api/v1/staples/store-stock` | Units of one item at the nearest Staples stores that have it for pickup today near a US ZIP, with the threshold value, pickup text and hours | us | 1 |
| `POST /api/v1/staples/category` | One class listing (CL id or staples.com category link), sorted, filtered and paged like search | us | 1 |
| `POST /api/v1/staples/deals` | Staples' On Promotion or Clearance products for keywords or a class | us | 1 |
| `POST /api/v1/staples/reviews` | Reviews of one item, up to 100 per page, sorted and filtered by stars or photos, with the rating breakdown | us | 1 |
| `POST /api/v1/staples/questions` | Customer questions on one item with answers, 10 per page | us | 1 |
| `POST /api/v1/staples/coupons` | The coupons on Staples' public coupons page: code, headline, details, end date, channel | us | 1 |
| `POST /api/v1/staples/stores` | The Staples stores near a US ZIP or city: address, phone, distance, this week's hours, services | us | 1 |
| `POST /api/v1/staples/store` | One store by number: address, phone, fax, hours, services | us | 1 |
| `POST /api/v1/staples/categories` | Staples' top-level departments, or one department's sub-departments and classes | us | 1 |
| `POST /api/v1/staples/trending` | The trending searches Staples shows in its search box | us | 1 |

`country` is `us` (default, www.staples.com, USD) or `ca` (www.staples.ca, Staples Canada, CAD: search and product only); `language` is `en` (default) or `fr` (with `ca` only). An endpoint asked for a market it does not serve is a `400`, not charged.

## Prices: Regular price, price per unit, page yield, promotions

Every priced US item carries:

| Field | Meaning |
|---|---|
| `price`, `price_text` | The price as Staples shows it, and its text ("$49.99") |
| `was_price`, `was_price_label` | Staples' own "Regular price", given only when above the price; `null` otherwise |
| `discount_percent` | Computed by Scavio from `price` and `was_price`; `null` without a `was_price` |
| `savings` | List items: [{`type`, `text`}] as Staples gives them ("Instant Savings", "$33.20"); product: the amount |
| `price_per_unit`, `price_per_unit_unit`, `price_per_unit_text` | Staples' own unit price where it shows one: 5 "Ream" ("$5.00/Ream"), 0.1 "Cost Per Page"; `null` otherwise |
| `pack_size` | As Staples gives it ("5000/Carton", "2/Pack", "Each") |
| `page_yield` | Product: the page yield Staples states for a cartridge (600 on HP 64XL); `null` on other items |
| `number_of_reams`, `sheets_per_ream`, `total_sheets` | Product: Staples' paper specifications as given ("10-Ream"; Staples' "Sheets Per Ream or Pack" value, 5000 on the carton) |
| `promotions`, `offer_expires` | Product: [{`type`, `name`, `text`}] Staples' own promotion texts ("Special Buy", "Offer Expires on 11/28/2026") and the expiry date (2026-11-28) |
| `coupon_codes` | Product: [{`code`, `limit`}] the codes Staples applies to this price and its limit per order at the promotional price |

- **National:** one price per item on staples.com. Report "$49.99 at staples.com on 2026-11-24", with the date; never per store or per ZIP.
- **Per ream:** quote Staples' `price_per_unit_text` where it is given (`122374` "$5.00/Ream" = $49.99 / 10 reams). The `variants[]` of a paper product list every pack size with its own item number and price: Hammermill Copy Plus 1-Ream (`122408`) $6.99, 3-Ream (`24422900`) $30.09, 5-Ream (`1181122`) $33.99, 8-Ream (`24422901`) $78.79, 400-Ream pallet (`24579853`) $3,305.49 on 2026-11-24 (the selected item's own variant row has no price there: read `price`). Open each variant with `/product` for its current Regular price and promotion.
- **Per page:** quote Staples' "Cost Per Page" where it is given. Otherwise divide `price` by `page_yield` and show the arithmetic ($35.89 / 240 = $0.15). Only where `page_yield` or the name states the yield; never infer one.
- **Canada:** `price` in CAD with `was_price` (Staples Canada's compare-at price, given only when above the price) and `discount_percent`; no price per unit or page yield.
- Report the labels and the arithmetic. Never judge a Regular price, a discount or an offer's expiry, never describe how often an item is on sale, and never compute a price after a coupon.

## Workflow

1. **Find the item.** `/search` with `q` (keywords such as `hp 64xl`, a model number, or a Staples item number), or `/category` (a class id from `/categories` or from `items[].category.id`) or `/deals`. Each item's `item_id` is the input of product, store-stock, reviews and questions. Case does not matter: the API handles it.
2. **Read it in full.** `/product` with `item_id` (or the item's `url`): price, Regular price, price per unit, page yield, promotions with expiry, coupon codes, specifications, every pack size. Add `zip` for delivery dates to that ZIP and `store` for that store's pickup units.
3. **Per page or per ream.** Quote `price_per_unit_text`; otherwise divide by `page_yield` or the reams in the pack, and show the division.
4. **Units near a ZIP.** `/store-stock` with `item_id` and `zip` (a 5-digit US ZIP) and `radius` (miles, default 100). Read `units` per store and `total_units`. An empty list: check `pickup_eligible` on the product.
5. **Pick a store.** `/stores` with `zip` or `city` (`Chicago, IL`) gives store numbers, hours and services; `/store` gives one store. `/store-stock` takes a ZIP, not a city: take the ZIP from `/stores`.
6. **Narrow a list.** `sort`, `brand` (up to 5), `min_price` / `max_price`, `deal` (`on_promotion` or `clearance`) and facet `filters` (up to 10 `facets[].values[].filter` strings, sent exactly as given, such as `Number of Reams_3A_2210-Ream_22`); `page` (1-250, 40 per page).
7. **Reviews and questions.** `/reviews` with `item_id`, `limit` (1-100), `page`, `sort`, `rating` (1-5) or `photos_only`; `/questions` with `item_id`, `page` and `sort`.
8. **Canada.** Send `country` `ca` (and `language` `fr` for French) on search and product only. A Canadian search answers the top matches; read each with `/product` by its `handle` or `item_id`.
9. **Watching prices:** there is no history. Poll the same items on a schedule and store each answer with its `fetched_at` and market; that stored series is the history.

## Parameters

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string or integer | one of | A Staples item number (`122374`, `2724258`) |
| `url` | string | one of | A staples.com product link (`items[].url`), or with `country` `ca` a staples.ca product link |
| `handle` | string | one of (ca) | With `country` `ca`: a Staples Canada product handle (`items[].handle` of a Canadian search) |
| `zip` | string or integer | none | A US ZIP: delivery availability and dates for it (the price does not change with it) |
| `store` | string or integer | none | A Staples store number (`stores[].store_number`): that store's pickup units |
| `country`, `language` | string | `us`, `en` | `us` or `ca`; `en` or `fr` (Canada). `zip` and `store` are US only |

### Store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string or integer | required | A Staples item number |
| `zip` | string or integer | required | A 5-digit US ZIP (`60540`). Not a city: `/stores` gives the ZIP of the stores near a city |
| `radius` | integer | 100 | Miles around the ZIP (1-100) |

### Search (`/search`), category (`/category`), deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | search: required | Keywords, a model number or a Staples item number (an item number answers with that product); 1-200 chars. Deals: `q` or `category` |
| `category` | string | category: required | A class id (`CL140691`) or a staples.com category link (`/<name>/cat_CL<id>`). Deals: `q` or `category`, not both |
| `type` | string | `on_promotion` | Deals: `on_promotion` or `clearance` |
| `deal` | string | none | Search and category: `on_promotion` or `clearance` only |
| `sort` | string | `best_match` | `best_match`, `price_low`, `price_high`, `rating`, `newest` |
| `brand` | string or array | none | 1-5 brands as Staples names them (the Brand facet's values: `Hammermill`, `HP`) |
| `filters` | array | none | 1-10 facet values exactly as an earlier answer gives them in `facets[].values[].filter`; several are combined |
| `min_price`, `max_price` | number | none | Price range (USD) |
| `page` | integer | 1 | 1-250; 40 products per page |
| `country`, `language` | string | `us`, `en` | Search: `us` or `ca` (`ca`: `q` only, top matches); category and deals: `us` |

### Reviews (`/reviews`) and questions (`/questions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string or integer | required | A Staples item number |
| `limit` | integer | 10 | Reviews: per page, 1-100 (questions: 10 per page) |
| `page` | integer | 1 | Page (1-based) |
| `sort` | string | `most_relevant` / `newest` | Reviews: `most_relevant`, `newest`, `oldest`, `highest_rating`, `lowest_rating`, `most_helpful`. Questions: `newest`, `most_answered` |
| `rating` | integer | none | Reviews: only this many stars (1-5) |
| `photos_only` | boolean | false | Reviews: only reviews with photos |

### Stores (`/stores`), store (`/store`), categories (`/categories`), coupons (`/coupons`), trending (`/trending`)

`/stores` takes `zip` or `city` (`"Chicago, IL"`, not both) and `radius` (1-100, default 25). `/store` takes `store` (required). `/categories` takes an optional `category` (a department id: `SC`, `CG` or `DP`, such as `SC1676`) for its sub-departments and classes; without it, the top-level departments. `/coupons` takes an optional `category` as Staples names it (`Printers`, `Ink & Toner`). `/trending` takes nothing. All are US only.

## Examples

### One product with its Regular price, price per ream, offer expiry and pickup units

```bash
curl -X POST https://api.scavio.dev/api/v1/staples/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "122374", "zip": "60540", "store": "1633"}'
```

Captured `data` (2026-11-24; `images`, `description`, `bullets`, `review_summary`, `breadcrumbs` and `hierarchy` dropped, `specifications` cut to 4 of 28, `variants` to 2 of 9, `notes` to 3 of 7):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "locale": "en-US" },
  "requested_item_id": "122374",
  "found_requested_item_id": true,
  "item_id": "122374",
  "name": "Hammermill Copy Plus 8.5\" x 11\" Copy Paper, 20 lbs., 92 Brightness, 5000 Sheets/Carton (105007)",
  "brand": "Hammermill",
  "manufacturer": "Hammermill",
  "model": "105007CT/27061",
  "url": "https://www.staples.com/hammermill-copy-plus-8-5-x-11-copy-paper-20-lbs-92-brightness-5000-sheets-carton-105007/product_122374",
  "image": "https://www.staples-3p.com/s7/is/image/Staples/0A9DEFAA-5A39-42C6-938F42EAB5C0ACCF_sc7",
  "price": 49.99,
  "was_price": 83.19,
  "was_price_label": "Regular price",
  "discount_percent": 40,
  "savings": 33.2,
  "on_promotion": true,
  "price_per_unit": 5,
  "price_per_unit_unit": "Ream",
  "pack_size": "5000/Carton",
  "promotions": [
    { "type": "terms_and_conditions", "name": "Special Buy", "text": "**While supplies last. May not be valid in combination with other offers. Offer subject to change." },
    { "type": "promo_headliner", "name": "Special Buy", "text": "Limit 5 at promotional price." },
    { "type": "promo_offer_expiration", "name": "Special Buy", "text": "Offer Expires on 11/28/2026" }
  ],
  "offer_expires": "2026-11-28",
  "coupon_codes": [{ "code": "89875", "limit": 5 }],
  "page_yield": null,
  "sheets_per_ream": 5000,
  "number_of_reams": "10-Ream",
  "total_sheets": 5000,
  "specifications": [
    { "name": "Paper Weight (lbs.)", "value": "20", "group": "Size & Weight" },
    { "name": "Total Number of Sheets", "value": "5000", "group": "Quantity" },
    { "name": "Brightness", "value": "92", "group": "Features" },
    { "name": "Number of Reams", "value": "10-Ream", "group": "Quantity" }
  ],
  "rating": 4.63,
  "review_count": 39887,
  "question_count": 83,
  "rating_breakdown": [
    { "stars": 1, "count": 930, "percent": 2 },
    { "stars": 2, "count": 495, "percent": 1 },
    { "stars": 3, "count": 1381, "percent": 3 },
    { "stars": 4, "count": 6799, "percent": 17 },
    { "stars": 5, "count": 30282, "percent": 76 }
  ],
  "category": { "id": "CL140691", "name": "Copy & Printer Paper" },
  "pickup_eligible": true,
  "ship_to_store_eligible": false,
  "free_shipping": true,
  "free_returns": true,
  "in_store_only": false,
  "back_order": false,
  "coming_soon": false,
  "clearance": false,
  "instant_savings": true,
  "restriction": null,
  "supplier_type": "Stock",
  "availability": {
    "zip": "60540",
    "store": "1633",
    "out_of_stock": false,
    "options": [
      { "mode": "pickup", "method": "pickup", "units": 42, "earliest_date": "2026-11-24", "latest_date": "2026-11-24", "date_text": "Tue, Nov 24", "order_within": null, "back_order": false },
      { "mode": "standard", "method": "delivery", "units": 1677, "earliest_date": "2026-11-30", "latest_date": "2026-11-30", "date_text": "Mon, Nov 30", "order_within": null, "back_order": false }
    ],
    "pickup": { "store_number": "1633", "units": 42, "in_stock": true }
  },
  "variant_group": { "id": "SS101841976", "name": "Hammermill Copy Plus Copy Paper, 20 lbs., 92 Brightness" },
  "variants": [
    {
      "item_id": "122374",
      "name": "Hammermill Copy Plus 8.5\" x 11\" Copy Paper, 20 lbs., 92 Brightness, 5000 Sheets/Carton (105007)",
      "url": "https://www.staples.com/hammermill-copy-plus-8-5-x-11-copy-paper-20-lbs-92-brightness-5000-sheets-carton-105007/product_122374",
      "price": null,
      "options": [{ "name": "Sheet Dimension", "value": "8.5\" x 11\" (US letter)" }, { "name": "Number of Reams", "value": "10-Ream" }],
      "image": "https://www.staples-3p.com/s7/is/image/Staples/0A9DEFAA-5A39-42C6-938F42EAB5C0ACCF_sc7",
      "selected": true
    },
    {
      "item_id": "122408",
      "name": "Hammermill Copy Plus 8.5\" x 11\" Copy Paper, 20 lbs., 92 Brightness, 500 Sheets/Ream (105007)",
      "url": "https://www.staples.com/hammermill-copy-plus-8-5-x-11-copy-paper-20-lbs-92-brightness-500-sheets-ream-105007/product_122408",
      "price": 6.99,
      "options": [{ "name": "Sheet Dimension", "value": "8.5\" x 11\" (US letter)" }, { "name": "Number of Reams", "value": "1-Ream" }],
      "image": "https://www.staples-3p.com/s7/is/image/Staples/sp167072084_sc7",
      "selected": false
    }
  ],
  "currency": "USD",
  "notes": [
    "price and was_price are as Staples shows them: was_price is Staples' Regular price, given only when it is above the price, and discount_percent is computed by Scavio from the two. staples.com prices are national (USD): the ZIP and the store change availability, not the price.",
    "staples.com publishes no UPC or GTIN for its items; model is the manufacturer's part number as Staples gives it.",
    "promotions and offer_expires are Staples' own promotion texts and expiry date as given; coupon_codes are the codes Staples applies to this price (limit: Staples' limit per order at the promotional price)."
  ]
}
```

$49.99 / 10 reams = $5.00 a ream, as Staples' own `price_per_unit` says; at the Regular price $83.19 / 10 = $8.32. Store 1633 (Naperville, IL) had 42 cartons for pickup the same day; delivery to 60540 read Mon, Nov 30. The ink cartridge `{"item_id": "2724258"}` read HP 64XL Black High Yield at $62.89 with `page_yield` 600, `price_per_unit` 0.1 and `price_per_unit_unit` "Cost Per Page", no Regular price. An unknown item is a charged `404`.

### Units of one item near a ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/staples/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "2724258", "zip": "60540"}'
```

Captured `data` (2026-11-24; 2 of 7 stores shown):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "locale": "en-US" },
  "item_id": "2724258",
  "name": "HP 64XL Black High Yield Ink Cartridge, Prints Up to 600 Pages (N9J92AN#140)",
  "image": "https://www.staples-3p.com/s7/is/image/Staples/5C3CA16E-D33D-4E06-BC12B567ADC71242_sc7?$std$",
  "location": "60540",
  "radius_miles": 100,
  "count": 7,
  "total_units": 63,
  "stores": [
    {
      "position": 1,
      "store_number": "1633",
      "address": { "line1": "1552 South Route 59", "city": "Naperville", "state": "IL", "zip": "60564" },
      "phone": "6303050253",
      "distance_miles": 3.38,
      "units": 12,
      "threshold": 50,
      "in_stock": true,
      "pickup_type": "ISP",
      "pickup_text": "Ready in 30 mins",
      "your_store": false,
      "hours": [
        { "day": "Monday", "open": "08:00", "close": "20:00", "closed": false },
        { "day": "Tuesday", "open": "08:00", "close": "20:00", "closed": false },
        { "day": "Wednesday", "open": "08:00", "close": "20:00", "closed": false },
        { "day": "Thursday", "open": null, "close": null, "closed": true },
        { "day": "Friday", "open": "09:00", "close": "20:00", "closed": false },
        { "day": "Saturday", "open": "09:00", "close": "18:00", "closed": false },
        { "day": "Sunday", "open": "10:00", "close": "18:00", "closed": false }
      ]
    },
    {
      "position": 2,
      "store_number": "1895",
      "address": { "line1": "539 W Roosevelt Rd", "city": "Glen Ellyn", "state": "IL", "zip": "60137" },
      "phone": "6307900989",
      "distance_miles": 7.98,
      "units": 12,
      "threshold": 50,
      "in_stock": true,
      "pickup_type": "ISP",
      "pickup_text": "Ready in 30 mins",
      "your_store": false,
      "hours": [
        { "day": "Monday", "open": "08:00", "close": "20:00", "closed": false },
        { "day": "Tuesday", "open": "08:00", "close": "20:00", "closed": false },
        { "day": "Wednesday", "open": "08:00", "close": "20:00", "closed": false },
        { "day": "Thursday", "open": null, "close": null, "closed": true },
        { "day": "Friday", "open": "09:00", "close": "20:00", "closed": false },
        { "day": "Saturday", "open": "09:00", "close": "20:00", "closed": false },
        { "day": "Sunday", "open": "10:00", "close": "18:00", "closed": false }
      ]
    }
  ],
  "notes": [
    "Staples lists only the stores that have the item for pickup today, nearest first (7 to 10 stores seen per answer): a store that is not listed either has none or is farther away.",
    "units are the available units as Staples reports them for each store; threshold is the value Staples returns beside them, as given (whether Staples caps units at it is not verified). Stock is as Staples reports it; Scavio makes no promise of its accuracy."
  ]
}
```

The other five stores: 1767 Willowbrook 9, 1615 Shorewood 7, 1657 Oak Lawn 8, 1634 Rolling Meadows 7 and 1788 Norridge 8 units, all within 22 miles. `hours` are this week's, holiday closures included (Thursday, Thanksgiving, closed). `{"item_id": "24430099", "zip": "10001"}` (HP 67XL, `pickup_eligible` `false`) answered `count` 0, an empty `stores` list and the note "No store within 100 miles lists this item for pickup today: no nearby store has it, or Staples does not offer it for store pickup (the product endpoint's pickup_eligible says which)."

### Reviews with full paging

```bash
curl -X POST https://api.scavio.dev/api/v1/staples/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "24430099"}'
```

Captured `data` (2026-11-24; `rating_breakdown` dropped, 1 of 10 reviews shown, `notes` cut to 2 of 4):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "locale": "en-US" },
  "item_id": "24430099",
  "name": "HP 67XL Black High Yield Ink Cartridge, Prints Up to 240 Pages (3YM57AN#140)",
  "rating": 4.45,
  "review_count": 18098,
  "sort": "most_relevant",
  "rating_filter": null,
  "photos_only": false,
  "page": 1,
  "limit": 10,
  "total": 6829,
  "total_pages": 683,
  "count": 10,
  "reviews": [
    {
      "id": "421434640",
      "rating": 5,
      "title": "INK",
      "text": "It works like ink is supposed to do.",
      "date": "2026-11-21T01:22:11.000+00:00",
      "locale": "en_US",
      "verified_purchase": true,
      "incentivized": false,
      "helpful_votes": 0,
      "unhelpful_votes": 0,
      "photos": [],
      "product": {
        "item_id": "24430101",
        "name": "HP 67XL Tri-Color High Yield Ink Cartridge (3YM58AN#140)",
        "url": "https://www.staples.com/hp-67xl-tri-color-high-yield-ink-cartridge-3ym58an-140-print-up-to-200-pages/product_24430101"
      },
      "syndicated_from": null,
      "responses": []
    }
  ],
  "notes": [
    "Reviews are pooled across the sizes and packs Staples groups with this item: product names the variant each review is about.",
    "No reviewer names: reviewers' display names are left out, and the customer's name in a reply's greeting (and the replying agent's initials) are removed."
  ]
}
```

Page with `total` and `total_pages` (6,829 reviews here; `review_count` 18,098 is Staples' own count on the product): `{"item_id": "24430099", "limit": 100, "page": 2}` reads the next 100. Reviews are pooled across the items Staples groups together, so `product` names the cartridge each review is about. `review_summary` is Staples' own AI-generated summary: quote it as Staples', never as Scavio's finding.

### Search, category, deals, questions, coupons, stores, store, categories, trending and Canada

- `/search` `{"q": "copy paper"}`: `total` 11,147, 40 per page, 250 pages (Staples serves listings to page 250); Hammermill Copy Plus 10 reams (`122374`) $49.99 / Regular price $83.19 ("$5.00/Ream") first, Staples Multiuse (`1149611`, 4000/Carton) $42.99 / $71.59 ("$5.37/Ream"), TRU RED 10 reams (`135848`) $62.79 ("$6.28/Ream"), each with `pack_size`, `savings` and `highlights`. 25 facets, including Brand, Number of Reams, Sheet Dimension, Brightness and Deals. `{"q": "hp 67 ink", "sort": "price_low"}` read 48 results, HP 67 Black (`24430098`) $22.89 first. `{"q": "122374"}` answered `redirect` {`type`: `product`, `item_id`: `122374`} with that product.
- `/category` `{"category": "CL140691"}`: Copy & Printer Paper, `total` 891, 23 pages; sponsored placements are kept with `sponsored: true` and `organic_position` null. An unknown class is a charged `404`.
- `/deals` `{"q": "laptop"}` (On Promotion): `total` 178, such as an HP 17.3" laptop (`24631637`) $399.99 / Regular price $899.99 with "Instant Savings" $500.00. `deals` needs `q` or `category`.
- `/questions` `{"item_id": "990119"}` (Hyken chair): `total` 201, 10 per page, each question with its first answer and `answer_count`; Staples staff answers carry `staff: true` and `badge` "Staff". No asker or answerer names.
- `/coupons`: 15 coupons in 6 categories (Pack & Ship, Printers, PC's, Tech Other, Ink & Toner, Office Supplies), such as code `12943` "Get $15 off the HP Envy Photo 7975 Printer" "when you buy an HP 64 Black/Tri-Color Standard Yield Ink Cartridge.", `ends` 2026-12-31, `channel` Online. Scavio does not check whether a code applies to an order.
- `/stores` `{"city": "Chicago, IL"}`: 10 stores within 25 miles, store 1611 The Garland Building, 111 North Wabash Ave., at 0.42 miles first, each with phone, fax, `utc_offset`, 7 `hours` entries and `services` (Print and Marketing Services, Shredding Services, Recycling Services, Amazon Lockers, UPS Shipping & Drop-off, Passport Services, Online Notary, ...).
- `/store` `{"store": "1574"}`: 500 Eighth Avenue Front 3, New York, NY 10018, phone 2122442681, the same `services`. An unknown store number is a charged `404`.
- `/categories` `{"category": "SC1676"}`: Paper, 19 sub-departments and classes, each {`id`, `type` (`SC`, `CG`, `DP`, `CL`), `name`, `url`}, such as `CL140691` Copy & Printer Paper. A `CL` id is the input of category and deals; any other id goes back to categories.
- `/trending`: 10 terms in Staples' order (needoh, office chairs, office chair, printer, ipad, paper, laptop, copy paper, smart watches, pens).
- Canada: `/search` `{"q": "hp 67", "country": "ca"}` read 4 top matches in CAD, HP 67 Black (`24430098`) $34.99 and HP 67 Tri-Colour (`24430103`) $36.99, with `suggested_queries`; `/product` `{"item_id": "24430098", "country": "ca"}` read $34.99 CAD, `barcode` 193015522398, `model` 3YM56AN#140, rating 4.38 from 5,132 reviews. With `"language": "fr"`, `{"q": "papier"}` read French names ("Papier LUX, 8-1/2 po x 14 po, écume de mer, paquet de 500") and the product `15332` read "Staples - Papier copie, 20 lb, 8,5 po l x 11 po H, blanc, 500 feuilles" at $8.49 CAD. English and French are separate products with the same item number, each with its own `handle`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def staples(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/staples/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Cartridges for a printer, lowest price first (1 credit)
hits = staples("search", {"q": "hp 64xl ink", "sort": "price_low"})["data"]
for i in hits["items"][:5]:
    print(i["item_id"], i["name"], i["price_text"], i["price_per_unit_text"])

# 2. One cartridge with its stated yield and Staples' own cost per page (1 credit)
p = staples("product", {"item_id": "2724258"})["data"]
print(p["name"], p["price"], p["was_price"], p["page_yield"], p["price_per_unit"], p["price_per_unit_unit"])
if p["page_yield"]:
    # Only where Staples states the yield; show the arithmetic.
    print("per page", round(p["price"] / p["page_yield"], 3))

# 3. Units at the stores near a ZIP (1 credit)
stock = staples("store-stock", {"item_id": "2724258", "zip": "60540"})["data"]
if not stock["stores"]:
    print("no nearby store lists it for pickup today; pickup_eligible:", p["pickup_eligible"])
for s in stock["stores"]:
    print(s["store_number"], s["address"]["city"], s["address"]["state"], s["distance_miles"], s["units"], s["pickup_text"])
print("total", stock["total_units"])

# Prices and units can change between calls. Store each answer with fetched_at
# and run this on a schedule: that stored series is your history (Staples shows
# only the current price and the current units).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` {`country`, `language`, `currency`, `locale`} (`USD` or `CAD`) and `notes`.

- **item** (search, category, deals; US) - `position`, `organic_position`, `sponsored`, `item_id`, `name`, `url`, `image`, `brand`, `manufacturer`, `model`, `price`, `price_text`, `was_price`, `was_price_label`, `discount_percent`, `savings[]` {`type`, `text`}, `price_per_unit`, `price_per_unit_unit`, `price_per_unit_text`, `pack_size`, `rating`, `review_count`, `category` {`id`, `name`}, `department`, `supercategory`, `delivery` {`text`, `date`, `type`}, `in_stock_for_delivery`, `out_of_stock`, `pickup_eligible`, `pickup_message`, `ship_to_store_eligible`, `in_store_only`, `restriction`, `badges`, `highlights[]` {`name`, `value`}, `supplier_type`.
- **lists** (US) - `title`, `page`, `page_size`, `total`, `total_pages`, `count`, `sponsored_count`, `sort`, `filters_applied[]` {`group`, `filter`, `name`}, `min_price`, `max_price`, `corrected_query`, `items[]`, `facets[]` {`name`, `values[]` {`filter`, `name`, `count`, `selected`}} (send `filter` back in `filters`). Search adds `query` and `redirect` {`type` (`product`, `category`, `page`), `item_id`, `category_id`, `url`}; category `category` {`id`, `name`}; deals `type`, `query` or `category`, `redirect`.
- **search, Canada** - `query`, `count`, `items[]` {`position`, `item_id`, `handle`, `language`, `name`, `brand`, `url`, `image`, `price`, `was_price`, `discount_percent`, `currency`, `available`}, `suggested_queries`.
- **product** (US) - `requested_item_id`, `found_requested_item_id`, `item_id`, `name`, `brand`, `manufacturer`, `model`, `url`, `image`, `images`, the price fields above, `on_promotion`, `promotions[]`, `offer_expires`, `coupon_codes[]`, `page_yield`, `sheets_per_ream`, `number_of_reams`, `total_sheets`, `specifications[]` {`name`, `value`, `group`}, `description`, `bullets`, `rating`, `review_count`, `question_count`, `rating_breakdown[]` {`stars`, `count`, `percent`}, `review_summary`, `category`, `hierarchy`, `breadcrumbs[]` {`name`, `id`, `url`}, `pickup_eligible`, `ship_to_store_eligible`, `free_shipping`, `free_returns`, `in_store_only`, `back_order`, `coming_soon`, `clearance`, `instant_savings`, `restriction`, `supplier_type`, `availability` {`zip`, `store`, `out_of_stock`, `options[]` {`mode`, `method`, `units`, `earliest_date`, `latest_date`, `date_text`, `order_within`, `back_order`}, `pickup` {`store_number`, `units`, `in_stock`}}, `variant_group` {`id`, `name`}, `variants[]` {`item_id`, `name`, `url`, `price`, `options[]` {`name`, `value`}, `image`, `selected`}, `currency`.
- **product, Canada** - `requested_item_id`, `item_id`, `handle`, `language`, `name`, `brand`, `url`, `image`, `images`, `price`, `was_price`, `discount_percent`, `currency`, `available`, `barcode`, `rating`, `review_count`, `pickup_eligible`, `clearance`, `model`, `breadcrumbs` (names), `description`, `variants[]` {`sku`, `name`, `options[]` {`name`, `value`}, `price`, `was_price`, `discount_percent`, `available`, `barcode`}.
- **store-stock** - `item_id`, `name`, `image`, `location`, `radius_miles`, `count`, `total_units`, `stores[]` {`position`, `store_number`, `address` {`line1`, `city`, `state`, `zip`}, `phone`, `distance_miles`, `units`, `threshold`, `in_stock`, `pickup_type`, `pickup_text`, `your_store`, `hours[]` {`day`, `open`, `close`, `closed`}}.
- **reviews** - `item_id`, `name`, `rating`, `review_count`, `rating_breakdown[]`, `review_summary`, `sort`, `rating_filter`, `photos_only`, `page`, `limit`, `total`, `total_pages`, `count`, `reviews[]` {`id`, `rating`, `title`, `text`, `date`, `locale`, `verified_purchase`, `incentivized`, `helpful_votes`, `unhelpful_votes`, `photos[]` {`url`, `thumbnail_url`}, `product` {`item_id`, `name`, `url`}, `syndicated_from`, `responses[]` {`text`, `date`}}.
- **questions** - `item_id`, `sort`, `page`, `total`, `total_pages`, `count`, `questions[]` {`id`, `text`, `date`, `locale`, `helpful_votes`, `answer_count`, `answers[]` {`id`, `text`, `date`, `helpful_votes`, `staff`, `badge`, `reply_count`}}.
- **coupons** - `category`, `count`, `categories`, `coupons[]` {`position`, `code`, `headline`, `details`, `ends` (ISO date), `ends_text` (as given), `channel` (`Online` or `omni`), `category`, `url`, `image`}.
- **stores** - `location`, `radius_miles`, `count`, `stores[]` {`position`, `store_number`, `name`, `address` {`line1`, `city`, `state`, `zip`, `country`}, `phone`, `fax`, `latitude`, `longitude`, `distance_miles`, `utc_offset`, `hours[]`, `services`}.
- **store** - `store_number`, `name`, `address`, `phone`, `fax`, `latitude`, `longitude`, `utc_offset`, `hours[]`, `services`.
- **categories** - `category` {`id`, `name`, `url`}, `parents[]` {`id`, `type`, `name`, `url`}, `count`, `categories[]` {`id`, `type`, `name`, `url`}.
- **trending** - `count`, `terms`.

## Guardrails

- Name it "Staples (staples.com, the US office supply retailer; Staples Canada at staples.ca)" on first mention. Staples Easy Rewards and Staples Business Advantage accounts are not read.
- Prices: quote `price` and `was_price` with Staples' own label ("Regular price"), the site (staples.com or staples.ca) and the `fetched_at` date. Prices are national: never call a price a store's or a ZIP's price, and never carry a US price to Canada or the reverse.
- Report Staples' labels (Regular price, the promotion text, `offer_expires`, coupon end dates) and the arithmetic only. Never judge a Regular price, a discount, an ink price or an offer deadline, never describe how often an item is on sale, and never compute a price after a coupon.
- Per page and per ream: show the price, the yield or reams as stated and the division, or quote Staples' own `price_per_unit_text`. Never infer a yield the product does not state, and say that yields are stated, not measured.
- Comparing Staples with Amazon, Walmart, Target or Best Buy: compare only the same item (same model number), each with its date, and label marketplace sellers as such. Staples' own brands (Staples, TRU RED) have no same item elsewhere: compare them per page or per ream, labelled as different products. Never call one retailer cheaper beyond the numbers shown.
- Stock: `units` as Staples reported them at the moment of the call; Scavio makes no promise of their accuracy. Report `threshold` as the value Staples returns, without claiming what it caps. Never promise pickup or delivery.
- Reviews: no reviewer names are returned. Quote `review_summary` as Staples' own AI-generated summary.
- Not available: UPC on staples.com, the weekly ad, search suggestions, print, copy and tech service prices, ink recycling rewards, Easy Rewards member prices, price match requests, Staples Business Advantage contract prices, price history (poll and store), checkout, cart or ordering; Staples Canada full search, reviews, store stock and delivery dates. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not collect or store Staples data: each call fetches the public Staples page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Staples' terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Staples product photos or logos; link products by `url` instead.
- Never fabricate prices, units, item numbers, store numbers, hours, dates, promotions, coupon codes or ratings. Only return what the API returned, with the `fetched_at` time, the market and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` other than `us` or `ca`; a `language` other than `en` or `fr`, or `fr` with `us`; any endpoint but search and product with `ca`; `sort`, `page`, `brand`, `filters`, prices or `deal` on a Canadian search; `zip` or `store` with `ca`; an `item_id` that is not a Staples item number; a `url` that is not a staples.com (or with `ca` a staples.ca) product link, or a `url` and `item_id` naming different items; a `handle` without `ca`; a `zip` that is not a 5-digit US ZIP, or a city on store-stock; both `zip` and `city` on stores, or neither; a `category` that is not a Staples class id or category link; deals without `q` or `category`, with both, or with `deal` instead of `type`; a `page` outside 1-250; more than 5 brands or 10 filters, or a filter not taken from `facets[].values[].filter`; a `radius` outside 1-100 or a review `limit` outside 1-100; an unknown `sort` or `type`; `min_price` above `max_price`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Staples has no item <item_id>.", "Staples has no such store.", "Staples has no department <id>.", "Staples Canada has no item <item_id>.", "Not found on Staples Canada.", "Staples serves no page <page> for this search.". Take item numbers, store numbers, class ids and filters from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api).
- `502` means Staples data was temporarily unavailable ("Staples is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Staples is busy ("Staples is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.83.0
npm install scavio@0.84.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: ink } = await scavio.staples.product({ item_id: "2724258" });
const { data: near } = await scavio.staples.storeStock({ item_id: "2724258", zip: "60540" });
const { data: paper } = await scavio.staples.search({ q: "copy paper", sort: "price_low" });
const { data: canada } = await scavio.staples.search({ q: "hp 67", country: "ca" });
const { data: cls } = await scavio.staples.category({ category: "CL140691" });
const { data: deals } = await scavio.staples.deals({ q: "laptop", type: "on_promotion" });
const { data: coupons } = await scavio.staples.coupons();
const { data: reviews } = await scavio.staples.reviews({ item_id: "24430099", limit: 100 });
const { data: questions } = await scavio.staples.questions({ item_id: "990119" });
const { data: stores } = await scavio.staples.stores({ city: "Chicago, IL" });
const { data: store } = await scavio.staples.store({ store: "1574" });
const { data: tree } = await scavio.staples.categories({ category: "SC1676" });
const { data: trending } = await scavio.staples.trending();
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.staples.search(...)`, `product`, `store_stock`, `category`, `categories`, `deals`, `coupons`, `stores`, `store`, `reviews`, `questions` and `trending`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 12 endpoints as tools: `search_staples`, `get_staples_product`, `get_staples_store_stock`, `get_staples_category`, `get_staples_categories`, `get_staples_deals`, `get_staples_coupons`, `get_staples_stores`, `get_staples_store`, `get_staples_reviews`, `get_staples_questions` and `get_staples_trending`. Staples is opt-in: add `staples` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.83.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,staples"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/staples-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api), [product](https://scavio.dev/docs/staples-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api), [store stock](https://scavio.dev/docs/staples-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api), [category](https://scavio.dev/docs/staples-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api), [categories](https://scavio.dev/docs/staples-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api), [deals](https://scavio.dev/docs/staples-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api), [coupons](https://scavio.dev/docs/staples-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api), [stores](https://scavio.dev/docs/staples-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api), [store](https://scavio.dev/docs/staples-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api), [reviews](https://scavio.dev/docs/staples-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api), [questions](https://scavio.dev/docs/staples-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api), [trending](https://scavio.dev/docs/staples-trending?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api). Overview: [Staples API](https://scavio.dev/staples-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api).
