---
name: michaels-craft-prices-api
description: Michaels API for Michaels (michaels.com, the US and Canada arts and crafts retailer) - Michaels prices and store stock, one SKU's exact units at the Michaels stores near a US ZIP or a Canadian postal code as Michaels reports them (one colour of Soft Classic yarn by Loops & Threads read 6 skeins at Naperville, IL and 1 at Downers Grove, IL on one day; virtual pop-up stores are flagged and show 0 units), up to 30 SKUs at one store in one call, and prices that are national per country (the store does not change the price; Canada has its own CAD prices, and the same Cricut Explore 5 bundle read $199.00 against Reg. $249.00 in the US and $269.99 against Reg. $349.99 in Canada); keyword, item-number and UPC search, category, brand and deals lists (sale, new, clearance, Great Buy), up to 100 per page, sorted by best match, best sellers, new arrivals, price or rating and filtered by brand, price, rating, store pickup, same-day delivery, seller (Michaels, Marketplace, Michaels Pro) and any facet such as colour, yarn weight or material, Michaels items and Marketplace items together with the seller type; one product in full with every colour or size and its price, Reg. price, UPC and online stock, the Pro bulk-pack unit price, specifications such as skein weight and yardage, rating and review count, and Michaels' own promotion text with its start and end; the stores near a ZIP with hours and services and one store's details; Michaels' departments and search suggestions. Canada in English or French. 11 endpoints, 2 credits per call (a category given as a link or path 4). No review text, weekly ad, coupons, classes, aisle location, Marketplace seller names, price history or checkout.
version: 1.0.0
tags: michaels, michaels-com, michaels-api, michaels-craft-store, michaels-prices, michaels-yarn, michaels-yarn-prices, michaels-inventory, michaels-inventory-checker, michaels-stock-checker, michaels-store-inventory, michaels-in-stock, michaels-stores, michaels-store-hours, michaels-deals, michaels-clearance, michaels-black-friday, michaels-canada, michaels-cricut, loops-and-threads, bernat, lion-brand, caron, cricut, yarn, yarn-prices, price-per-ounce, craft-supplies, craft-store-prices, arts-and-crafts, store-inventory, store-stock, us-retail, canada-retail, usd, cad, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/michaels-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api
---

# Michaels API - Craft Prices, Store Stock, Yarn Inventory

Read Michaels (michaels.com, the US and Canada arts and crafts retailer): the exact units of one SKU at the Michaels stores near a US ZIP or a Canadian postal code, the units of up to 30 SKUs at one store, keyword, item-number and UPC search, category, brand and deals lists, one product in full with every colour or size, the stores near a ZIP, one store's details, the department tree and search suggestions. www.michaels.com (USD, English) and canada.michaels.com (CAD, English or French). All 11 endpoints return structured JSON at 2 credits per call (4 for a category given as a link or path, listed below).

**The job this skill is for: Michaels yarn prices.** What a skein costs at Michaels this week, per ounce, next to Michaels' own "Reg." price and the offer's own dates, and how many skeins of one colour the stores near a ZIP have. On 2026-11-24 Soft Classic Solid Yarn by Loops & Threads (SKU `10228177`, colour Butter, "Skein Weight" 7 oz. / 198 g) read $3.37 against Michaels' "Reg.$4.49" under the promotion "25% Off Online or Buy One Get One 50% off mix & match in stores" (`starts` 2026-11-20T00:00:00, `ends` 2026-11-24T17:59:59): $3.37 / 7 oz = $0.48 an ounce, Reg. $4.49 / 7 oz = $0.64. The 12-skein Pro pack (`MP228177`) read $2.89 each ($0.41 an ounce). `/store-stock` for that colour near ZIP 60540 counted 6 skeins at store 4809 (Naperville, IL) and 1 at store 1278 (Downers Grove, IL); `/store-inventory` counted 85 at store 1191 (NYC-Manhattan-Chelsea). Every colour is its own SKU, so stock is per colour. Pair it with `walmart-product-data`, `amazon-product-data` and `etsy-product-data` for the same item (same brand, line, colour and skein weight, or the same UPC) and `google-shopping-api` across retailers.

Nine limits shape every answer, so say them plainly:
- **2 credits per call; a category link or path 4.** Every endpoint is 2. `category` and `deals` with a `/shop/` link or path are 4 (one more lookup finds its code path); send a code path (`categories[].code_path`) for 2. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not. A request needs the most it can spend available in the balance (2, or 4 with a category link): the charge is still `credits_used`.
- **Prices are national per country, not per store.** Measured 2026-11-24: 39 items read the same price at 6 stores in 6 states. The store matters for stock, never for price; `store` on a list only keeps the products with free store pickup there. Canada has its own prices in CAD: the Cricut Explore 5 in Teal & Essential Bundle (`10816737`, UPC `00093573453045`) read $199.00 / Reg. $249.00 on www.michaels.com and $269.99 / Reg. $349.99 on canada.michaels.com the same day. Report each in its own currency; never convert or call one cheaper.
- **`was_price` is Michaels' own "Reg." label.** `price_text` and `was_price_text` are as Michaels writes them ("$3.37", "Reg.$4.49"); `discount_percent` is Scavio's arithmetic from the two. Promotions carry Michaels' own `text`, `details`, `starts` and `ends` (no timezone, as given). Online and in-store offers can differ inside one promotion text; quote it whole.
- **Store stock is exact units as Michaels reports them.** `/store-stock` returns `units`, `in_stock`, `pickup_text` ("TODAY", "TOMORROW", "AUJOURD'HUI" in French) per store within `radius` miles (default 20, up to 200). `virtual: true` marks a virtual or pop-up event store Michaels lists by that name (store 3492 "CALGARY STAMPEDE-VIRTUAL STORE" in Toronto showed 0 units). A SKU Michaels does not know shows 0 units at every store: confirm a SKU with `/product` first. Michaels' own FAQ calls its online availability "an estimation"; never promise pickup.
- **`online_stock` on a product is not a store's stock.** Product and its variants carry `online_stock` {`units`, `in_stock`}, Michaels' ship-to-home stock. Store units come only from `/store-stock` and `/store-inventory`.
- **The SKU is the input; one colour is one SKU.** `items[].sku` (8 digits for Michaels items, 18 for Marketplace items, `MP...` for Pro packs, `D...` on `dropship` items) is the input of product, store-stock and store-inventory. A list item's `colors` [{`sku`, `name`}] and a product's `variants[]` give each colour's own SKU. A UPC search answers with the product group's lead SKU (the Light Coral UPC `00191518184167` returned `10228177`, the Butter lead): read `variants[]` for the colour you need.
- **Michaels and Marketplace items come mixed.** Lists carry `seller_type` (`michaels`, `marketplace` for MakerPlace sellers, `michaels_pro` for bulk packs, `dropship`); `seller` filters them (US only). A Marketplace product carries `seller_id` as the page gives it; Michaels does not show the seller's name there.
- **Canada in English or French.** `country` `ca` reads canada.michaels.com in CAD; `language` `fr` reads canada.michaels.com/fr with French names and texts ("Laine Blanket Big de Bernat", `price_text` "16,99 $"). `fr` with `us` is a `400`. If the French storefront does not list the requested SKU, product answers the variant it shows with `found_requested_sku` `false` and a note. `stores`, `categories` and `suggestions` are US only; in Canada `/store-stock` lists the stores near a postal code, and `category` / `deals` take a code path from a search's "By category code" facet.
- **Ratings, not reviews; no history.** Items and products carry `rating` and `review_count`, no review or Q&A text. Nothing is cached or kept: poll and store your own series.

Michaels' official API is for approved Marketplace sellers, who use it to manage their own listings, inventory and orders through its Developer Portal. Publishers can join its affiliate programme on CJ for links and a product feed. There is no public Michaels API for reading the catalog, prices, offer dates or store stock; those are shown on michaels.com for the store you pick, and this skill reads those public pages with one Scavio key.

Michaels operated 1,376 Michaels stores in 49 states and Canada as of January 31, 2026 (Michaels press release, Feb 17, 2026). It has been privately held since 2021, when funds affiliated with Apollo acquired it. Quote these with their source, never from the samples.

See also: for the same item at Walmart use `walmart-product-data`; at Amazon `amazon-product-data`; handmade and vintage alternatives on Etsy `etsy-product-data`; prices across retailers `google-shopping-api`; per-store stock at other retailers `home-depot-product-data`, `lowes-product-data`, `tractor-supply-prices-api`.

## When to trigger

Use this skill when the user asks to:
- Price a Michaels yarn (Loops & Threads, Bernat, Lion Brand, Caron, Big Twist) per ounce, with Michaels' sale price next to its "Reg." price and the offer's dates
- Check how many skeins of one colour (or units of any SKU) the Michaels stores near a ZIP or a Canadian postal code have, or one store's units for a list of SKUs
- Search michaels.com or canada.michaels.com by keyword, item number or UPC, sorted by price, rating or best sellers, or filtered by brand, yarn weight, material, colour, store pickup or seller
- List a Michaels category, a brand's products (Cricut, Lion Brand Yarn, Loops and Threads) or the sale, new, clearance or Great Buy items for a keyword or category
- Read one Michaels product in full: every colour or size with price, Reg. price, UPC and online stock, specifications (skein weight, yardage), Pro-pack unit price, rating and review count, promotions with dates
- Compare one item's US and Canadian listing (same SKU or UPC), each in its own currency
- Find the Michaels stores near a ZIP, a city or a point, or one store's hours, services (custom framing, curbside pickup, same-day delivery) and opening date
- Compare one national-brand item at Michaels, Walmart, Amazon or Etsy (with `walmart-product-data`, `amazon-product-data` and `etsy-product-data`)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 2 credits (4 for a category given as a link or path), so 50 credits cover 25 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, store-stock, store-inventory, stores, search and the lists took 1-5 seconds, product 3-17 and store 2-26. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Markets | Credits |
|---|---|---|---|
| `POST /api/v1/michaels/store-stock` | Units of one SKU at the Michaels stores within `radius` of a US ZIP or a Canadian postal code: units, in stock, pickup message, address, phone, distance, hours, virtual flag | us, ca | 2 |
| `POST /api/v1/michaels/store-inventory` | Units of 1-30 SKUs at one store, with `total_units` and `not_reported` | us, ca | 2 |
| `POST /api/v1/michaels/product` | One product by SKU or link: price, Reg. price, UPC, options, every variant with its price, UPC and online stock, specifications, Pro pack, rating, review count, promotions with dates, seller id on Marketplace items | us, ca | 2 |
| `POST /api/v1/michaels/search` | Keywords, an item number or a UPC: up to 100 per page with total, facets, seller type and promotions | us, ca | 2 |
| `POST /api/v1/michaels/category` | One category's products by code path, or by `/shop/` link or path (US), sorted, filtered and paged | us, ca (code path) | 2 (4 with a link or path) |
| `POST /api/v1/michaels/brand` | One brand's products, optionally matching keywords or within a category | us, ca | 2 |
| `POST /api/v1/michaels/deals` | Michaels' Sale, New, Clearance or Great Buy (US) products for a keyword or a category | us, ca | 2 (4 with a link or path) |
| `POST /api/v1/michaels/stores` | The Michaels stores near a ZIP, a city or a point: address, phone, distance, hours, curbside hours, services, virtual flag | us | 2 |
| `POST /api/v1/michaels/store` | One store by number: address, phone, fax, hours, services, opening date, closing dates | us, ca | 2 |
| `POST /api/v1/michaels/categories` | Michaels' departments, or one category's subcategories, each with its `path` and `code_path` | us | 2 |
| `POST /api/v1/michaels/suggestions` | The search suggestions Michaels shows as you type, with categories and brands | us | 2 |

`country` is `us` (default, www.michaels.com, USD) or `ca` (canada.michaels.com, CAD); `language` is `en` (default) or `fr` (with `ca` only). An endpoint asked for a market it does not serve is a `400`, not charged.

## Prices: Reg. price, sale price, variants, Pro packs, per ounce

Every priced item carries:

| Field | Meaning |
|---|---|
| `price`, `price_text` | The price as Michaels shows it, and its text as written ("$3.37"; in French "16,99 $") |
| `was_price`, `was_price_text` | Michaels' own "Reg." price where it shows one ("Reg.$4.49"); `null` otherwise |
| `price_min`, `price_max`, `was_price_min`, `was_price_max` | The range across sizes when Michaels gives one; `null` otherwise |
| `on_sale` | Michaels' flag |
| `discount_percent` | Computed by Scavio from `price` and `was_price`; `null` without a `was_price` |
| `unit_price` | Michaels' own unit price text where it shows one ("$1.30 ea." on a 10-pack of canvases); `null` otherwise |
| `pro_pack` | Product: {`sku`, `units_per_pack`, `unit_price`, `unit_price_text`} for the Michaels Pro bulk pack where Michaels lists one |
| `promotions` | [{`text`, `details`, `rewards_text`, `starts`, `ends`}]: Michaels' own offer text and dates, as given |

- **National per country:** one price per item per storefront. 10228177 read $3.37 / Reg. $4.49 on www.michaels.com on 2026-11-24. Report "$3.37 at michaels.com on 2026-11-24", with the date; never per store.
- **US and Canada:** the same SKU can be listed on both storefronts at different prices and under different promotions. 10816737 read $199.00 / Reg. $249.00 (US) and $269.99 / Reg. $349.99 CAD (Canada). The Canadian yarn search the same day carried "Buy 1 Get 1 50% off - Add 2 items to qualify" (ends 2026-11-24T23:59:59) where the US one carried "25% Off Online or Buy One Get One 50% off mix & match in stores" (ends 2026-11-24T17:59:59).
- **Per ounce:** divide the price by the skein weight only where the name or `specifications` state it ("Skein Weight" "7 oz. / 198 g"), and show the arithmetic: $3.37 / 7 = $0.48 an ounce. Canada: Bernat Blanket Big (`10519836`, "10.5 oz. / 300 g") $16.99 CAD / 10.5 = $1.62 CAD an ounce. List items carry no skein weight: read the product for it.
- **Variants:** `variants[]` lists each colour or size with its own `sku`, `price`, `was_price`, `upc` and `online_stock` (10228177 has 45 colours, all $3.37 / Reg. $4.49 on 2026-11-24).
- **Guest prices only:** no Michaels Rewards, educator, military or coupon prices; coupons are not read or applied.
- Report the labels and the arithmetic. Never judge a Reg. price, a discount or an offer's dates, and never describe how often an item is on sale.

## Workflow

1. **Find the item.** `/search` with `q` (keywords, an item number or a UPC), or `/brand` (`Lion Brand Yarn`, `Cricut`), `/category` (a `code_path` from `/categories` or a search facet) or `/deals`. Each item's `sku` and its `colors[].sku` are the inputs of product, store-stock and store-inventory.
2. **Read it in full.** `/product` with `sku` (or the item's `url`): price, Reg. price, promotions with dates, specifications (skein weight, yardage), every colour's SKU, UPC and online stock, the Pro pack.
3. **Per ounce.** Divide `price` (and `was_price`) by the stated skein weight; show the division.
4. **Skeins near a ZIP.** `/store-stock` with the colour's `sku` and `zip` (a US ZIP, or with `country` `ca` a postal code such as `M5V 2T6`) and `radius` (miles, default 20). Read `units` per store, skip `virtual` stores, and quote `total_units` and `in_stock_count`.
5. **One store, many SKUs.** `/store-inventory` with `store` and up to 30 `skus` (every colour a pattern needs, for example). `not_reported` lists SKUs Michaels gave no units for.
6. **Pick a store.** `/stores` with `zip`, `city` (`San Francisco, CA`) or `latitude` + `longitude` (US), or the store numbers `/store-stock` returns (US and Canada). `/store` gives one store's hours and services; an unknown number is a charged `404`.
7. **Narrow a list.** `sort`, `brand`, `min_price` / `max_price`, `min_rating` (1-4), `store` + `pickup`, `same_day`, `ship_to_me`, `on_sale`, `new`, `clearance`, `great_buy` (US), `seller` (US) and facet `filters` ({`facets[].key`: [`facets[].values[].value`]}, e.g. `{"yarnWeight": ["4 - Medium"]}`), at most 8 in all; `page_size` (1-100, default 40) and `page`.
8. **Canada.** Send `country` `ca` (and `language` `fr` for French) on search, product, store-stock, store-inventory, store, category, brand and deals.
9. **Watching prices:** there is no history. Poll the same SKUs on a schedule and store each answer with its `fetched_at` and market; that stored series is the history.

## Parameters

### Store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string or integer | required | A Michaels SKU (`items[].sku`, one colour or size: `10228177`) |
| `zip` | string | required | A 5-digit US ZIP (`10001`), or with `country` `ca` a Canadian postal code (`M5V 2T6`) |
| `radius` | integer | 20 | Miles around the location (1-200) |
| `country`, `language` | string | `us`, `en` | `us` or `ca`; `en` or `fr` (Canada) |

### Store inventory (`/store-inventory`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store` | string or integer | required | A Michaels store number (`1191`, `4936`) |
| `skus` | array | required | 1-30 Michaels SKUs (`["10228177", "10816737"]`) |
| `country`, `language` | string | `us`, `en` | As above |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string or integer | one of | A Michaels SKU |
| `url` | string | one of | A www.michaels.com or canada.michaels.com product link (`items[].url`); its host must match `country` |
| `country`, `language` | string | `us`, `en` | As above |

### Search (`/search`), category (`/category`), brand (`/brand`), deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | search: required | Keywords, an item number or a UPC; 1-200 chars. On category, brand and deals: only products matching it (deals needs `q` or `category`) |
| `category` | string | category: required | A code path (`categories[].code_path`, or a "By category code" facet value: `root//Categories//809187838`), or in the US a `/shop/` link or path (`/shop/art-supplies/artist-canvas`, 4 credits). On search and brand: a code path only |
| `brand` | string | brand: required | A brand as Michaels names it in the Brand facet (`Cricut`, `Lion Brand Yarn`, `Loops and Threads`). On search, category and deals: only that brand |
| `type` | string | `sale` | Deals: `sale`, `new`, `clearance` or `great_buy` (US) |
| `sort` | string | `best_match` | `best_match`, `best_sellers`, `new_arrivals`, `price_asc`, `price_desc`, `rating` |
| `min_price`, `max_price` | number | none | Price range |
| `min_rating` | integer | none | Only products rated at least this many stars (1-4) |
| `store` | string or integer | none | Only products with free store pickup at that store |
| `pickup` | boolean | none | Free store pickup only (needs `store`) |
| `same_day`, `ship_to_me` | boolean | none | Same-day delivery or ship-to-home only |
| `on_sale`, `new`, `clearance`, `great_buy` | boolean | none | Michaels' More Ways to Shop filters (not on deals: use `type`; `great_buy` US only) |
| `seller` | string | none | `michaels`, `marketplace` or `michaels_pro` (US only) |
| `filters` | object | none | Facet filters from an earlier answer: {`facets[].key`: [`facets[].values[].value`]}, sent exactly as given (`refinementColor`, `size`, `material`, `yarnWeight`); 1-10 values each |
| `page_size` | integer | 40 | 1-100 |
| `page` | integer | 1 | (page - 1) x page_size at most 8000 |
| `country`, `language` | string | `us`, `en` | As above |

### Stores (`/stores`), store (`/store`), categories (`/categories`), suggestions (`/suggestions`)

`/stores` (US) takes `zip`, `city` or `latitude` + `longitude`, and `radius` (1-200, default 20). `/store` takes `store` (required) and `country`. `/categories` (US) takes an optional `path` (a `categories[].path` such as `/shop/art-supplies`) for its subcategories; without it, the departments. `/suggestions` (US) takes `q` (1-100 chars).

## Examples

### One product with its Reg. price, offer dates and colours

```bash
curl -X POST https://api.scavio.dev/api/v1/michaels/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "10228177"}'
```

Captured `data` (2026-11-24; `description`, `image` and `images` dropped, `variants` cut to 2 of 45, `breadcrumbs` to 1, `notes` to 2):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD" },
  "sku": "10228177",
  "requested_sku": "10228177",
  "found_requested_sku": true,
  "master_sku": "M10196925",
  "name": "Soft Classic™ Solid Yarn by Loops & Threads®",
  "brand": "Loops & Threads",
  "url": "https://www.michaels.com/product/soft-classic-solid-yarn-by-loops-threads-10228177",
  "price": 3.37,
  "was_price": 4.49,
  "price_min": null,
  "price_max": null,
  "was_price_min": null,
  "was_price_max": null,
  "price_text": "$3.37",
  "was_price_text": "Reg.$4.49",
  "on_sale": true,
  "discount_percent": 25,
  "unit_price": null,
  "rating": 4.77,
  "review_count": 38343,
  "seller_type": "michaels",
  "channel": "1",
  "seller_id": null,
  "upc": "00195158112504",
  "options": { "Color": "Butter" },
  "details": [],
  "specifications": [
    { "name": "Brand", "value": "Loops & Threads" },
    { "name": "Size", "value": "7 oz" },
    { "name": "Usage and care", "value": "Machine wash cold, gentle cycle. Do not bleach. Tumble dry low. Do not iron." },
    { "name": "Weight", "value": "Medium (4)" },
    { "name": "Contents", "value": "100% acrylic" },
    { "name": "Skein Weight", "value": "7 oz. / 198 g" },
    { "name": "Yardage", "value": "354 yd. / 324 m" }
  ],
  "category": "Value Yarn",
  "breadcrumbs": [
    { "name": "Value Yarn", "url": "https://www.michaels.com/shop/yarn-needlework/shop-all-yarn/value-yarn" }
  ],
  "online_stock": { "units": 10349, "in_stock": true },
  "pro_pack": { "sku": "MP228177", "units_per_pack": 12, "unit_price": 2.89, "unit_price_text": "$2.89 each" },
  "store_pickup": true,
  "store_only": false,
  "online_only": false,
  "badges": ["free_store_pickup", "same_day_delivery"],
  "same_day_delivery_fee": "$9.99",
  "variant_counts": { "Color": 45 },
  "variants": [
    {
      "sku": "10626715",
      "options": { "Color": "Light Coral" },
      "price": 3.37,
      "was_price": 4.49,
      "on_sale": true,
      "discount_percent": 25,
      "upc": "00191518184167",
      "online_stock": { "units": 4886, "in_stock": true },
      "image": "https://imgs.michaels.com/renditions/8ae79d0b-6d41-4a56-bd13-f019c5c5e26b_thumbnail.jpg"
    },
    {
      "sku": "10661801",
      "options": { "Color": "Coffee" },
      "price": 3.37,
      "was_price": 4.49,
      "on_sale": true,
      "discount_percent": 25,
      "upc": "00195158445510",
      "online_stock": { "units": 8423, "in_stock": true },
      "image": "https://imgs.michaels.com/renditions/45f3e620-f31c-4958-b9bc-b24653475fad_thumbnail.jpg"
    }
  ],
  "promotions": [
    {
      "text": "25% Off Online or Buy One Get One 50% off mix & match in stores",
      "details": "25% Discount Available online only. Buy one item at regular price & get the second of equal or lesser value half price available in store. Excludes clearance.",
      "rewards_text": null,
      "starts": "2026-11-20T00:00:00",
      "ends": "2026-11-24T17:59:59"
    }
  ],
  "notes": [
    "price and was_price are as Michaels shows them (was_price is its own Reg. price); discount_percent is computed by Scavio from those two. Michaels prices nationally per country: the store does not change the price.",
    "promotions are the offer texts Michaels lists for the item, with starts and ends exactly as Michaels gives them (no timezone)."
  ]
}
```

$3.37 / 7 oz = $0.48 an ounce (Reg. $4.49 / 7 oz = $0.64; Pro pack $2.89 / 7 oz = $0.41). `online_stock` is the ship-to-home stock, not a store's. `{"sku": "10519836", "country": "ca"}` read Bernat Blanket Big at $16.99 CAD with no Reg. price and the promotion "Buy 1 Get 1 50% off - Add 2 items to qualify"; with `"language": "fr"` its `name` read "Laine Blanket Big de Bernat" and `price_text` "16,99 $". An unknown SKU is a charged `404`.

### Units of one SKU near a ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/michaels/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "10816737", "zip": "10001"}'
```

Captured `data` (2026-11-24; 2 of 21 stores shown):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD" },
  "sku": "10816737",
  "location": "10001",
  "radius_miles": 20,
  "count": 21,
  "in_stock_count": 19,
  "total_units": 58,
  "stores": [
    {
      "store_id": "1191",
      "name": "NYC-Manhattan-Chelsea, NY",
      "address": { "line1": "675 Avenue of the Americas", "line2": "NYC-Manhattan-Chelsea, NY", "city": "New York", "state": "NY", "zip": "10010", "country": "US" },
      "phone": "(646) 259-3911",
      "latitude": 40.74208,
      "longitude": -73.99362,
      "distance_miles": 0.9,
      "units": 8,
      "in_stock": true,
      "pickup": true,
      "pickup_text": "TODAY",
      "same_day_delivery": true,
      "open_now": false,
      "hours": ["09:00 AM - 10:00 PM", "09:00 AM - 10:00 PM", "09:00 AM - 10:00 PM", "CLOSED", "07:00 AM - 10:00 PM", "07:00 AM - 10:00 PM", "09:00 AM - 08:00 PM"],
      "virtual": false
    },
    {
      "store_id": "1283",
      "name": "Mill Creek at Harmon Meadow",
      "address": { "line1": "400 Mill Creek Dr", "line2": "Mill Creek at Harmon Meadow", "city": "Secaucus", "state": "NJ", "zip": "07094", "country": "US" },
      "phone": "(201) 293-0214",
      "latitude": 40.79165,
      "longitude": -74.04738,
      "distance_miles": 3.6,
      "units": 5,
      "in_stock": true,
      "pickup": true,
      "pickup_text": "TODAY",
      "same_day_delivery": true,
      "open_now": false,
      "hours": ["09:00 AM - 10:00 PM", "09:00 AM - 10:00 PM", "09:00 AM - 10:00 PM", "CLOSED", "07:00 AM - 10:00 PM", "07:00 AM - 10:00 PM", "09:00 AM - 08:00 PM"],
      "virtual": false
    }
  ],
  "notes": [
    "units are the store's units as Michaels reports them for pickup; Scavio makes no promise of their accuracy. pickup_text is Michaels's own pickup message (e.g. TODAY, TOMORROW).",
    "Stores are the Michaels stores within radius miles of the location, in Michaels's order, with distance_miles as Michaels gives it. A SKU Michaels does not know shows 0 units at every store."
  ]
}
```

That is the Cricut Explore 5 in Teal bundle: 58 units across 21 stores within 20 miles, 19 of them with stock (Edgewater, NJ and Paramus, NJ at 0). In Canada, `{"sku": "10196926", "zip": "M5V 2T6", "country": "ca"}` (Soft Classic yarn) listed 14 stores and 104 units, 13 at store 4936 (Riocan Hall, Toronto) and 17 at 4931 (Erin Mills Power Centre, Mississauga), with the virtual store 3492 at 0; with `"language": "fr"` near `H2X 1Y4` (Montreal) Bernat Blanket Big (`10519836`) read 41 to 115 units at each of 8 stores, `pickup_text` "AUJOURD'HUI". `hours` are the 7 entries Michaels lists for the current week, in its order, without day names.

### Many SKUs at one store

```bash
curl -X POST https://api.scavio.dev/api/v1/michaels/store-inventory \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store": "1191", "skus": ["10228177", "10816737", "10617442"]}'
```

Captured `data` (2026-11-24):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD" },
  "store_id": "1191",
  "count": 3,
  "in_stock_count": 3,
  "total_units": 113,
  "items": [
    { "sku": "10228177", "units": 85 },
    { "sku": "10816737", "units": 8 },
    { "sku": "10617442", "units": 20 }
  ],
  "not_reported": [],
  "notes": [
    "units are the store's pickup units as Michaels reports them; Scavio makes no promise of their accuracy. not_reported: SKUs Michaels gave no units for.",
    "A store number or SKU Michaels does not know answers 0 units or no units: check the store with store and the SKU with product."
  ]
}
```

### Search, category, brand, deals, stores, store, categories and suggestions

- `/search` `{"q": "yarn"}`: `total` 21,188, 40 per page, 530 pages; the first items Soft Classic by Loops & Threads (`10228177`) $3.37 / Reg. $4.49, Big Twist Value Yarn (`10794639`) $3.74 / Reg. $4.99, Bernat Blanket Big (`10750420`) $10.49 / Reg. $13.99, each with the dated promotion and `colors` [{`sku`, `name`}]. Facets include Brand (Lion Brand Yarn 1,018, Loops and Threads 809), Retailers (Marketplace 16,498, Michaels 4,374, Michaels Pro - Buy in Bulk 316), `yarnWeight` and `material`. With `country` `ca` the same query read `total` 2,614, Soft Classic (`10196926`) $5.49 CAD.
- `/brand` `{"brand": "Cricut"}`: `total` 790, 20 pages; Cricut Explore 5 in Teal (`10816737`) $199.00 / Reg. $249.00 first, with Michaels, Marketplace (an 18-digit SKU) and `dropship` (`D9017715S`) items in one list, each with its `seller_type`.
- `/category` `{"category": "root//Categories//809187942//845162438"}`: `total` 5,684 canvases; Level 3 Gallery Wrapped Heavy Duty Canvas by Artist's Loft (`10472532`) $4.90 / Reg. $13.99 under "65% Off Online or Buy 1 Get 2 Free mix & match in stores" (ends 2026-11-29T17:59:59), and a 10-pack with Michaels' own `unit_price` "$1.30 ea.". The same category as `/shop/art-supplies/artist-canvas` costs 4 credits. A wrong category is a charged `404`.
- `/deals` `{"type": "clearance", "q": "christmas"}`: `total` 32, such as Green Seeded Eucalyptus Pick by Ashland (`10737792`) $3.00 / Reg. $9.79. `deals` needs `q` or `category`.
- `/stores` `{"zip": "60657"}`: 13 stores within 20 miles of Chicago, IL 60657, 1040 The Point at Clark Street at 0.2 miles first, each with phone, 7 `hours` entries, `curbside_pickup_hours` and `services` {`in_store_shopping`, `store_pickup`, `curbside_pickup`, `same_day_delivery`, `custom_framing`, `frame_and_print`, `balloon_inflation`, `birthday_parties`, `fabrics`}.
- `/store` `{"store": "1040"}`: The Point at Clark Street, 3131 N Clark St, Chicago, IL 60657-4413, phone (773) 327-7127, `open_date` 2010-07-16, `time_zone` America/Chicago, the same `services`. No staff names.
- `/categories`: 35 departments (Sale, Christmas, Christmas Trees, Yarn & Needlework, Fabric, Frames, Canvas, Art Supplies, Cricut, Floral, MichaelsPro - Buy In Bulk, Clearance, ...), each {`name`, `path`, `url`, `code_path`, `leaf`, `children`}; Sale and Clearance have no `code_path` (use `/deals`).
- `/suggestions` `{"q": "paint"}`: 5 terms (paint by number, paint, paint brushes, paint by numbers kits for adults, paint markers), each with Michaels' categories and brands (DecoArt, Liquitex, FolkArt).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def michaels(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/michaels/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. One yarn with its Reg. price, offer dates and skein weight (2 credits)
p = michaels("product", {"sku": "10228177"})["data"]
spec = {s["name"]: s["value"] for s in p["specifications"]}
print(p["name"], p["price_text"], p["was_price_text"], spec.get("Skein Weight"))
for promo in p["promotions"]:
    print(promo["text"], promo["starts"], promo["ends"])
# Per ounce only where the skein weight is stated ("7 oz. / 198 g" -> 7)
oz = 7
print("per oz", round(p["price"] / oz, 2), "Reg. per oz", round(p["was_price"] / oz, 2) if p["was_price"] else None)

# 2. Skeins of that colour at the stores near a ZIP (2 credits)
stock = michaels("store-stock", {"sku": "10228177", "zip": "60540"})["data"]
for s in stock["stores"]:
    if s["virtual"]:
        continue
    print(s["store_id"], s["address"]["city"], s["address"]["state"], s["distance_miles"], s["units"])
print("total", stock["total_units"], "in stock at", stock["in_stock_count"])

# 3. Every colour a pattern needs at one store (2 credits, up to 30 SKUs)
inv = michaels("store-inventory", {"store": "1191", "skus": ["10228177", "10626715", "10661801"]})["data"]
print({i["sku"]: i["units"] for i in inv["items"]}, "not reported:", inv["not_reported"])

# Prices and units can change between calls. Store each answer with fetched_at
# and run this on a schedule: that stored series is your history (Michaels shows
# only the current price and the current units).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` {`country`, `language`, `currency`} (`USD` or `CAD`).

- **item** (search, category, brand, deals) - `position`, `sku`, `name`, `url`, `image`, `images`, `category`, `price`, `was_price`, `price_min`, `price_max`, `was_price_min`, `was_price_max`, `price_text`, `was_price_text`, `on_sale`, `discount_percent`, `unit_price`, `rating`, `review_count`, `seller_type` (`michaels`, `marketplace`, `michaels_pro`, `dropship`), `channel`, `sponsored`, `store_pickup`, `same_day_delivery`, `ship_to_me`, `online_only`, `store_only`, `badges`, `gtin`, `variant_counts`, `colors[]` {`sku`, `name`}, `promotions[]` {`text`, `details`, `rewards_text`, `starts`, `ends`}. List items carry no `brand`: read it on the product.
- **lists** - `total`, `page`, `page_size`, `total_pages`, `count`, `sort`, `filters_applied`, `corrected_query`, `items[]`, `facets[]` {`key`, `name`, `values[]` {`value`, `count`, `label`}} (send `key` and `value` in `filters`), `notes`. Search adds `query`, `category`; category `category` {`code_path`, `name`, `path`, `url`}, `query`; brand `brand`, `query`, `category`; deals `type`, `query`, `category`.
- **product** - `sku`, `requested_sku`, `found_requested_sku`, `master_sku`, `name`, `brand`, `url`, `image`, `images`, the price fields above, `rating`, `review_count`, `seller_type`, `channel`, `seller_id` (Marketplace items), `upc`, `options`, `description`, `details`, `specifications[]` {`name`, `value`}, `category`, `breadcrumbs[]` {`name`, `url`}, `online_stock` {`units`, `in_stock`}, `pro_pack` {`sku`, `units_per_pack`, `unit_price`, `unit_price_text`}, `store_pickup`, `store_only`, `online_only`, `badges`, `same_day_delivery_fee`, `variant_counts`, `variants[]` {`sku`, `options`, `price`, `was_price`, `on_sale`, `discount_percent`, `upc`, `online_stock`, `image`}, `promotions[]`, `notes`.
- **store-stock** - `sku`, `location`, `radius_miles`, `count`, `in_stock_count`, `total_units`, `stores[]` {`store_id`, `name`, `address` {`line1`, `line2`, `city`, `state`, `zip`, `country`}, `phone`, `latitude`, `longitude`, `distance_miles`, `units`, `in_stock`, `pickup`, `pickup_text`, `same_day_delivery`, `open_now`, `hours`, `virtual`}, `notes`.
- **store-inventory** - `store_id`, `count`, `in_stock_count`, `total_units`, `items[]` {`sku`, `units`}, `not_reported`, `notes`.
- **stores** - `location` {`query`, `latitude`, `longitude`, `formatted_address`}, `radius_miles`, `count`, `stores[]` {`position`, `store_id`, `name`, `address`, `phone`, `latitude`, `longitude`, `distance_miles`, `time_zone`, `hours`, `hours_text`, `curbside_pickup_hours`, `open_now`, `services`, `virtual`}, `notes`.
- **store** - `store_id`, `name`, `address`, `phone`, `fax`, `latitude`, `longitude`, `time_zone`, `hours`, `hours_text`, `curbside_pickup_hours`, `services`, `virtual`, `open_date`, `closing_dates`, `temporarily_closed_date`, `notes`.
- **categories** - `path`, `name`, `url`, `code_path`, `leaf`, `count`, `categories[]` {`name`, `path` (the input of categories), `url`, `code_path` (the input of category, search, brand and deals), `leaf`, `children`}, `notes`.
- **suggestions** - `query`, `count`, `suggestions[]` {`term`, `categories`, `brands`}, `notes`.

## Guardrails

- Name it "Michaels (michaels.com, the US and Canada arts and crafts retailer)" on first mention. Michaels Rewards accounts, MakerPlace seller pages and Michaels Pro accounts are not read.
- Prices: quote `price` and `was_price_text` as Michaels labels them, with the storefront (www.michaels.com or canada.michaels.com) and the `fetched_at` date. Prices are national per country: never call a price a store's price, and never carry a US price to Canada or the reverse.
- Report Michaels' labels ("Reg.", the promotion text, `starts` and `ends`) and the arithmetic only. Never judge a Reg. price, a discount or an offer deadline, never describe how often an item is on sale, and never compute a price after a coupon.
- Per ounce: show the price, the skein weight as stated and the division. Never infer a weight the name or `specifications` do not state.
- Comparing Michaels with Walmart, Amazon or Etsy: compare only the same item (same brand, line, colour and skein weight, or UPC), each with its date. Michaels' own lines (such as Loops & Threads and Artist's Loft) have no same item elsewhere: compare them per ounce, labelled as different products. Never call one retailer cheaper beyond the numbers shown.
- Stock: `units` as Michaels reported them at the moment of the call; Scavio makes no promise of their accuracy. Skip `virtual` stores when counting. Never promise pickup or same-day delivery.
- Reviews: `rating` and `review_count` only. No review text or reviewer details are returned.
- Not available: review and Q&A text, the weekly ad, coupons, classes and events, aisle location, Marketplace seller names and seller pages, custom framing quotes, Rewards prices, price history (poll and store), Canadian store search by city (use store-stock), Canadian categories and suggestions, checkout, cart or ordering. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not collect or store Michaels data: each call fetches the public Michaels page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Michaels' terms of use cover how its site may be used (they license personal, non-commercial use); read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Michaels product photos or logos; link products by `url` instead.
- Never fabricate prices, units, SKUs, store numbers, hours, dates, promotions or ratings. Only return what the API returned, with the `fetched_at` time, the market and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` other than `us` or `ca`; a `language` other than `en` or `fr`, or `fr` with `us`; stores, categories or suggestions with `ca`; a SKU that is not a Michaels SKU; a `zip` that is not a 5-digit US ZIP (or, with `ca`, a Canadian postal code); a store number that is not a Michaels store number; neither `sku` nor `url` on product, or a `url` whose host does not match `country`; more than 30 `skus`; a `radius` outside 1-200 or a `page_size` outside 1-100; an unknown `sort`, `type` or `seller`; `seller` or `great_buy` with `ca`; `pickup` without `store`; `min_price` above `max_price`; `latitude` without `longitude`; deals without `q` or `category`; a `/shop/` path with `ca` or on search and brand; a Sale or Clearance department as a category (use deals); more than 8 filters in all, or a filter that is not a `facets[].key`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Unknown Michaels product (search lists SKUs).", "Unknown Michaels store in the US (store-stock and stores list store numbers)." ("in Canada" with `ca`), "Unknown Michaels category (categories lists them).", "Unknown Michaels category, or no products in it (categories lists them).", "No Michaels products for this brand (brand values are the facets Brand values of search, e.g. Cricut, Lion Brand Yarn).", "Not found on Michaels.". Take SKUs, store numbers, code paths and filters from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api).
- `502` means Michaels data was temporarily unavailable ("Michaels is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Michaels is busy ("Michaels is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.81.0
npm install scavio@0.82.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: yarn } = await scavio.michaels.product({ sku: "10228177" });
const { data: near } = await scavio.michaels.storeStock({ sku: "10228177", zip: "60540" });
const { data: inv } = await scavio.michaels.storeInventory({ store: "1191", skus: ["10228177", "10816737", "10617442"] });
const { data: results } = await scavio.michaels.search({ q: "yarn" });
const { data: canada } = await scavio.michaels.search({ q: "yarn", country: "ca" });
const { data: canvas } = await scavio.michaels.category({ category: "root//Categories//809187942//845162438" });
const { data: cricut } = await scavio.michaels.brand({ brand: "Cricut" });
const { data: deals } = await scavio.michaels.deals({ type: "clearance", q: "christmas" });
const { data: stores } = await scavio.michaels.stores({ zip: "60657" });
const { data: store } = await scavio.michaels.store({ store: "1040" });
const { data: tree } = await scavio.michaels.categories();
const { data: typed } = await scavio.michaels.suggestions({ q: "paint" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.michaels.search(...)`, `product`, `store_stock`, `store_inventory`, `stores`, `store`, `category`, `categories`, `brand`, `deals` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `search_michaels`, `get_michaels_product`, `get_michaels_store_stock`, `get_michaels_store_inventory`, `get_michaels_stores`, `get_michaels_store`, `get_michaels_category`, `get_michaels_categories`, `get_michaels_brand`, `get_michaels_deals` and `get_michaels_suggestions`. Michaels is opt-in: add `michaels` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.81.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,michaels"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/michaels-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api), [product](https://scavio.dev/docs/michaels-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api), [store stock](https://scavio.dev/docs/michaels-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api), [store inventory](https://scavio.dev/docs/michaels-store-inventory?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api), [stores](https://scavio.dev/docs/michaels-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api), [store](https://scavio.dev/docs/michaels-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api), [category](https://scavio.dev/docs/michaels-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api), [categories](https://scavio.dev/docs/michaels-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api), [brand](https://scavio.dev/docs/michaels-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api), [deals](https://scavio.dev/docs/michaels-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api), [suggestions](https://scavio.dev/docs/michaels-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api). Overview: [Michaels API](https://scavio.dev/michaels-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api).
