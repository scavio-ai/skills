---
name: dollar-tree-bulk-prices-api
description: Dollar Tree API for Dollar Tree (dollartree.com, the US and Canada discount variety store chain) - Dollar Tree bulk prices and store stock, the case price split into the unit price as Dollar Tree lists them online (9-in. White Paper Plates, 40-ct. read $1.50 a pack and $45.00 for a case of 30, order minimum 5), the order minimum and split-case multiple, the price points Dollar Tree shows ($1.00, $1.25, $1.50, $1.75, $3.00, $5.00, $7.00, $10.00 in Christmas Decor) and MORE CHOICES, its multi-price department; one national online price (the same item read $1.50 and the same $45.00 case at 6 stores in 6 states); the exact units of one item at a Dollar Tree store by store number plus up to about 63 nearby stores (116 packs at store 5126 in East Harlem, New York, 59 of 63 nearby in stock), ship-to-home units with an estimated delivery date and ship-to-store; keyword and item-number search, category, brand, sale, clearance, New Arrivals and MORE CHOICES lists, 48 per page by default (up to 250) to page 200, sorted by relevance, price, newest or rating and filtered by price point, brand, rating, in-store only, price range or any facet; one product in full with UPCs as Dollar Tree gives them, specifications, online stock units, SNAP flag and its categories; the stores near a US ZIP or city with hours, holiday hours, EBT, frozen foods and MORE CHOICES flags; one store page (Dollar Tree Canada store pages too, no prices); the category tree; the newest English reviews (up to about 98 per call) with syndicated reviews flagged and no reviewer names. 10 endpoints, 1 credit per call, stores 5. No UPC search, search suggestions, weekly ad, deal dates, Quick Order, gift cards, Canadian products or prices, price history or checkout.
version: 1.0.0
tags: dollar-tree, dollartree, dollartree-com, dollar-tree-api, dollar-tree-prices, dollar-tree-bulk, dollar-tree-bulk-prices, dollar-tree-bulk-order, dollar-tree-case-price, dollar-tree-case-pack, dollar-tree-unit-price, dollar-tree-price-per-unit, dollar-tree-online, dollar-tree-in-stock, dollar-tree-store-stock, dollar-tree-inventory, dollar-tree-stores, dollar-tree-store-hours, dollar-tree-more-choices, dollar-tree-christmas, dollar-tree-party-supplies, dollar-tree-clearance, dollar-tree-new-arrivals, dollar-tree-reviews, dollar-tree-canada, dollar-store, dollar-store-prices, discount-retail, case-price, unit-price, bulk-prices, party-supplies, store-stock, store-locator, ebt, snap, us-retail, usd, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 300
    throttle: 1
    homepage: https://scavio.dev/dollartree-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api
---

# Dollar Tree API - Bulk Prices, Case Packs, Store Stock

Read Dollar Tree (dollartree.com, the US and Canada discount variety store chain): keyword and item-number search, category, brand and deal lists (sale, clearance, New Arrivals, MORE CHOICES), one product in full with its unit price, case price, case pack, order minimum and split-case rules, the units of one item at a Dollar Tree store and the stores near it, the stores near a US ZIP or city, one store page, the category tree and the newest reviews. www.dollartree.com (USD, English) for all 10 endpoints; Dollar Tree Canada store pages (English, no prices) for `store` only. Every endpoint returns structured JSON at 1 credit per call, except `stores` at 5.

**The job this skill is for: Dollar Tree bulk prices.** What a Dollar Tree item costs on dollartree.com today by the unit and by the case, the order minimum and split-case multiple, the price point Dollar Tree shows, and how many units a store has. On 2026-11-25 (UTC) the 9-in. White Paper Plates, 40-ct. Packs (item `221159`, brand The Home Store) read `price` 1.5 with `case_price` 45 for a `case_pack` of 30 ($1.50 x 30 = $45.00), `minimum_quantity` 5 and `split_case.multiple` 5. `/store-stock` at store 5126 (2182 3rd Avenue, East Harlem, New York, NY) read 116 units on hand (`unit_size` 1: stores sell single packs) and listed 63 nearby stores by number, 59 of them in stock; ship to home read 75,570 units with an estimated delivery of 2026-12-02. A search for `paper plates` read 61 items: Heavy-Duty 10-in Ultra Paper Plates, 10-pc (`380886`) $1.50 a pack, $36.00 for 24; Round Paper Plates - Black, 9 in., 24 ct. (`356742`) $1.25, $22.50 for 18; Serv Heavy Duty 10-in Ultra Paper Plates, 50-pc (`376763`) $5.00, $50.00 for 10. Pair it with `dollar-general-api`, `walmart-product-data`, `target-product-data` and `instacart-api` for the same item (same UPC).

Ten limits shape every answer, so say them plainly:
- **1 credit per call, `stores` 5.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **One national online price.** `price` is Dollar Tree's online unit price from one national online price list: item `221159` read $1.50 and the same $45.00 case at 6 stores in 6 states (5126 NY, 5262 NJ, 2461 IL, 8170 MT, 7796 TX, 5441 CA) on 2026-11-24, and no endpoint takes a ZIP or store for prices. Dollar Tree's own footer says prices and availability may vary between stores and online, and store shelf prices are not published online. Write "the online price at dollartree.com", never a store's shelf price.
- **Case price against unit price.** Online orders go by the case or in split-case multiples. `case_price` is Dollar Tree's price for `case_pack` units (unit price x case pack: $1.50 x 30 = $45.00); `minimum_quantity` is Dollar Tree's order minimum; `split_case` {`available`, `multiple`, `fee`} is Dollar Tree's split-case data as given (`fee` only on the product, `null` in lists). Report them as Dollar Tree gives them and show the arithmetic; stores sell single units.
- **Case pack 0 means no case price.** Where Dollar Tree gives a case pack or case price of 0 (Red Bull Zero, item `403802`, measured 2026-11-24), `case_pack` and `case_price` are `null`. Never compute one.
- **The prices Dollar Tree shows, as given.** Items come at many price points: the Christmas Decor Price facet listed $1.00, $1.25, $1.50, $1.75, $3.00, $5.00, $7.00 and $10.00; `paper plates` listed $1.25, $1.50, $4.00 and $5.00. MORE CHOICES (`deals` `type` `more_choices`) is Dollar Tree's multi-price department. Never write that everything costs $1.25.
- **Store stock needs a store number and is slow.** `/store-stock` takes `item_id` and `store` (a number from `/stores`); a ZIP alone does not pick a store. It returns the store's exact `units`, up to about 63 `nearby_stores` by store number with their units, `ship_to_home` and `ship_to_store`. It is the slowest endpoint: 27 seconds in the capture, 17 to 72 seconds measured. Allow a client timeout of 300 seconds.
- **No UPC search.** Dollar Tree's search does not match UPCs: a UPC finds nothing. Look items up by the Dollar Tree item number (`items[].item_id`, the number at the end of a dollartree.com product link, such as `221159` or `FD1402202`). `upcs` are listed as Dollar Tree gives them, zero-padded to 18 digits, and an assorted item can list several (221159 lists 10).
- **Reviews: the newest only.** `/reviews` returns up to about 98 of the newest English reviews, newest first. No other sort, no star filter, no questions and answers, no reviewer names. Many reviews are syndicated from brand sites: `syndicated` and `syndication_source` say so (95 of 97 on Crest Tartar Protection came from crest.com).
- **Canada: store pages only.** Dollar Tree Canada has no shopping site. `country` `ca` is served by `/store` only (locations.dollartreecanada.com pages, English, no prices, `currency` `null`); every other endpoint is US only.
- **No history, no deal dates.** Dollar Tree publishes no validity dates for sale, clearance or new items and no weekly ad. Nothing is cached or kept: poll and store your own series.

Dollar Tree publishes no public API for its catalog, prices, store stock or stores. Publishers can join its affiliate programme through affiliate networks (a links-and-commission programme, not a price API); suppliers work through Dollar Tree's vendor portal on SAP Ariba and EDI. API directory profiles carrying a Dollar Tree name are third-party listings, not Dollar Tree documentation. Prices are shown on dollartree.com, and this skill reads those public pages with one Scavio key.

Dollar Tree, Inc. reported 9,511 stores across the Dollar Tree U.S. and Dollar Tree Canada banners at the end of Q3 fiscal 2026 (October 31, 2026; 8-K filed 2026-11-24), in 48 contiguous states and seven Canadian provinces, and $19.4 billion in net sales for fiscal 2025. Family Dollar has been a separate company since July 2025. Quote these with their source, never from the samples.

See also: for the same item (same UPC) at Dollar General use `dollar-general-api` (it looks products up by UPC); at Walmart `walmart-product-data`; at Target `target-product-data`; Dollar Tree is also an Instacart retailer, and `instacart-api` reads Instacart's prices for it (label them as Instacart's, never as Dollar Tree's shelf price); per-unit prices at other retailers `staples-ink-prices-api`, `michaels-craft-prices-api`.

## When to trigger

Use this skill when the user asks to:
- Price a Dollar Tree item by the unit and by the case, with the case pack, the order minimum and the split-case multiple, as dollartree.com lists them
- List Dollar Tree items at one price point ($1.25, $1.50, $5.00, ...) or in MORE CHOICES, Dollar Tree's multi-price department
- Check how many units of one item a Dollar Tree store has, with the nearby stores' units and the ship-to-home units and delivery estimate
- Find the Dollar Tree stores near a US ZIP or city with hours, holiday hours and EBT, frozen foods or MORE CHOICES flags, or read one store page (US or Dollar Tree Canada)
- Search dollartree.com by keyword or item number, sorted by price, newest or rating, or filtered by brand, rating, in-store only, price range or any facet
- List a Dollar Tree category (party supplies, Christmas decor, cleaning), one brand's items, or the sale, clearance and New Arrivals items
- Read one Dollar Tree product in full: UPCs, specifications, online stock units, SNAP flag, categories
- Read the newest reviews of a Dollar Tree item with Dollar Tree's rating breakdown and syndication flags
- Compare one item at Dollar Tree, Dollar General, Walmart and Target by UPC (with `dollar-general-api`, `walmart-product-data` and `target-product-data`)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit except `stores` (5), so 50 credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, deals took about 1 second, search, product, category, categories, brand and store 2-4, stores 14, store-stock 27 and reviews 31. Store stock was measured at 17 to 72 seconds. Allow a client timeout of at least 300 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Markets | Credits |
|---|---|---|---|
| `POST /api/v1/dollartree/search` | Keywords or an item number: 48 per page by default (up to 250) with total, facets, unit price, case price, case pack, order minimum and split case | us | 1 |
| `POST /api/v1/dollartree/product` | One item by item number or link: unit price, list price, sale price, case price, case pack, order minimum, split case with fee, UPCs, specifications, online stock units, SNAP flag, categories | us | 1 |
| `POST /api/v1/dollartree/category` | One category listing (`dimension_id` or a dollartree.com category link), sorted, filtered and paged like search | us | 1 |
| `POST /api/v1/dollartree/categories` | Dollar Tree's departments with every sub-category, or one category's sub-categories | us | 1 |
| `POST /api/v1/dollartree/brand` | One brand's items as Dollar Tree writes the brand, with its other spellings | us | 1 |
| `POST /api/v1/dollartree/deals` | Sale, clearance, New Arrivals or MORE CHOICES items, sorted, filtered and paged like search | us | 1 |
| `POST /api/v1/dollartree/store-stock` | Units of one item at a store (by store number) and up to about 63 nearby stores, ship-to-home units with an estimated delivery date, ship-to-store | us | 1 |
| `POST /api/v1/dollartree/stores` | The Dollar Tree stores near a US ZIP or city (20 per answer): address, phone, distance, hours, holiday hours, EBT, frozen foods, MORE CHOICES, pickup and delivery | us | 5 |
| `POST /api/v1/dollartree/store` | One store page by link or slug: hours, holiday hours, amenities and the stores nearby | us, ca | 1 |
| `POST /api/v1/dollartree/reviews` | The newest English reviews of one item (up to about 98), with rating breakdown and syndication flags | us | 1 |

`country` is `us` (default, www.dollartree.com, USD) or `ca` (Dollar Tree Canada store pages: `store` only); `language` is `en` (the default and only value). An endpoint asked for a market it does not serve is a `400`, not charged.

## Prices: unit price, case price, order minimum, split case

Every priced item carries:

| Field | Meaning |
|---|---|
| `price` | Dollar Tree's online unit price (USD), from one national online price list |
| `list_price` | Dollar Tree's list price as given |
| `sale_price` | Product: Dollar Tree's sale price, `null` without one |
| `on_sale` | Dollar Tree's own sale flag, as given |
| `unit_price_text` | The unit price as Dollar Tree writes it ("1.50") |
| `case_price` | Dollar Tree's price for `case_pack` units; `null` where Dollar Tree gives 0 |
| `case_pack` | Units in a case; `null` where Dollar Tree gives 0 |
| `minimum_quantity` | Dollar Tree's order minimum (units) |
| `split_case` | {`available`, `multiple`, `fee`} as Dollar Tree gives them; `fee` on the product only (`null` in lists) |
| `not_for_individual_sale`, `varying_case_packs`, `assortment`, `assortment_details` | Dollar Tree's flags and assortment text (the last three on the product) |
| `upcs` | The UPCs Dollar Tree lists for the item, zero-padded to 18 digits as given |
| `snap_eligible`, `in_store_only`, `clearance`, `new` | Dollar Tree's flags |

- **Per unit:** quote `price` with the date: "$1.50 a pack at dollartree.com on 2026-11-25". Per case: quote `case_price` with `case_pack` and show the division ($45.00 / 30 = $1.50).
- **Order rules:** quote `minimum_quantity` and `split_case` as given. Item `221159` read `minimum_quantity` 5, `split_case` {`available`: false, `multiple`: 5, `fee`: 0}; most listing items read `minimum_quantity` equal to `case_pack` (`380886`: 24 and 24).
- **Price points:** the Price facet (`facets[]` with `key` `price_point`) lists the price points in a listing with counts; send one as `price_point` (`1.25`) or its `id` in `filters`.
- **Matching another retailer:** match on the UPC. The last 12 digits of an 18-digit `upcs` value are the UPC-A, the last 13 an EAN-13. An assortment can carry several UPCs: compare only the one that names the same product.
- Report the labels and the arithmetic. Never call a price a store's shelf price, never describe a price as a rise, a cut or a bargain, and never compute a price Dollar Tree does not show.

## Workflow

1. **Find the item.** `/search` with `q` (keywords such as `paper plates`, or a Dollar Tree item number), or `/category` (a `dimension_id` from `/categories` or from a product's `categories[]`), `/brand` or `/deals`. Each item's `item_id` is the input of product, store-stock and reviews. Never search a UPC: it finds nothing.
2. **Read it in full.** `/product` with `item_id` (or the item's `url`): unit price, case price, case pack, order minimum, split case with fee, UPCs, online stock units.
3. **Per unit and per case.** Quote `price`, then `case_price` for `case_pack` units with the division; quote `minimum_quantity` and `split_case` as given.
4. **Pick a store.** `/stores` with `zip` (a US ZIP) or `city` (`"Naperville, IL"`), 5 credits: 20 stores in Dollar Tree's order with `store_number`, `slug`, address, hours and flags.
5. **Units at the store.** `/store-stock` with `item_id` and `store` (a `store_number`), optionally `zip` and `state` of the store. Read `store.units`, `nearby_stores[]` (store numbers with units) and `nearby_in_stock`. Nearby stores carry no address: `/stores` near the same ZIP and `/store` (its `nearby_stores`) give store numbers with addresses. Expect tens of seconds.
6. **Narrow a list.** `sort`, `price_point`, `brand`, `rating` (1-5, and up), `in_store_only`, `min_price` / `max_price` and facet `filters` (up to 10 `facets[].values[].id` strings, sent exactly as given); `page` (1-200) and `page_size` (1-250, default 48).
7. **Reviews.** `/reviews` with `item_id`: the newest English reviews, with `syndicated` and `syndication_source` on each.
8. **Canada.** `/store` with `country` `ca` and a locations.dollartreecanada.com `url` or its `slug`. Nothing else is served for Canada.
9. **Watching prices:** there is no history. Poll the same items on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Product (`/product`) and reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string or integer | one of | A Dollar Tree item number (`221159`, `FD1402202`; `items[].item_id`). UPCs are not item numbers |
| `url` | string | one of | A dollartree.com product link (`items[].url`) instead of `item_id` |
| `country`, `language` | string | `us`, `en` | `us` only; `en` only |

### Store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` or `url` | string or integer | one required | A Dollar Tree item number or product link |
| `store` | string or integer | required | A Dollar Tree store number (`stores[].store_number`, e.g. `5126`). A ZIP alone does not pick a store |
| `zip` | string or integer | none | Optional: the store's ZIP, sent along with the store |
| `state` | string | none | Optional: the store's two-letter state (`NY`) |

### Search (`/search`), category (`/category`), brand (`/brand`), deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | search: required | Keywords or a Dollar Tree item number (1-200 chars); category, deals: keywords inside the listing |
| `category` | string or integer | category: required | A category `dimension_id` (`3804024826`, Christmas Decor) or a dollartree.com category link. Search and brand: a filter; deals: with `type` `sale` or `clearance` only |
| `brand` | string | brand: required | A brand as Dollar Tree writes it (the Brand facet's labels, `Dixie`); matched case-insensitively. Search, category, deals: a filter |
| `type` | string | `sale` | Deals: `sale`, `clearance`, `new` (New Arrivals, newest first by default) or `more_choices` (MORE CHOICES) |
| `sort` | string | `relevance` | `relevance`, `price_low`, `price_high`, `newest`, `rating` |
| `price_point` | number or string | none | Only items at this price point, as the Price facet lists them (`1.25`, `1.50`, `5.00`) |
| `rating` | integer | none | Only items rated this many stars and up (1-5) |
| `in_store_only` | boolean | false | Only items Dollar Tree sells in stores only |
| `min_price`, `max_price` | number | none | Unit price range (USD); `max_price` must be above 0.05 |
| `filters` | array | none | 1-10 refinement ids exactly as an earlier answer gives them in `facets[].values[].id`; several are combined |
| `page` | integer | 1 | 1-200 |
| `page_size` | integer | 48 | 1-250 (48 is the site's own page size) |

### Stores (`/stores`), store (`/store`), categories (`/categories`)

`/stores` takes `zip` (a US ZIP) or `city` (`"Naperville, IL"`); with both, `zip` is used. `/store` takes `url` (`stores[].url`, a locations.dollartree.com page, or with `country` `ca` a locations.dollartreecanada.com page) or `slug` (`stores[].slug`, `ny/new-york/2182-3rd-avenue`). `/categories` takes an optional `category` (a `dimension_id`, id or category link) for its sub-categories; without it, the departments with every sub-category.

## Examples

### One product with its case price, order minimum and online stock

```bash
curl -X POST https://api.scavio.dev/api/v1/dollartree/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "221159"}'
```

Captured `data` (2026-11-25 UTC; `images`, `long_description` and `notes` dropped, `upcs` cut to 2 of 10, `specifications` to 4 of 12):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "locale": "en-US" },
  "requested_item_id": "221159",
  "item_id": "221159",
  "name": "9-in. White Paper Plates, 40-ct. Packs",
  "brand": "The Home Store",
  "store_brand": "DT",
  "url": "https://www.dollartree.com/the-home-store-9-in-uncoated-white-paper-plates-40-pc-pack/221159",
  "image": "https://www.dollartree.com/ccstore/v1/images/?source=/file/v5770587485520967755/products/221159.jpg",
  "description": "PAPER PLATES 9IN",
  "price": 1.5,
  "list_price": 1.5,
  "sale_price": null,
  "on_sale": false,
  "unit_price_text": "1.50",
  "case_price": 45,
  "case_pack": 30,
  "minimum_quantity": 5,
  "split_case": { "available": false, "multiple": 5, "fee": 0 },
  "not_for_individual_sale": false,
  "varying_case_packs": false,
  "assortment": true,
  "assortment_details": "40-pc Pack The Home Store 9-in Uncoated White Paper Plate",
  "upcs": ["000000639277128775", "000000076955101000"],
  "rating": 3.4444,
  "review_count": 9,
  "in_store_only": false,
  "store_pickup_eligible": true,
  "shippable": true,
  "online_only": false,
  "delivery_options": "2",
  "order_limit": null,
  "clearance": false,
  "new": true,
  "deals": null,
  "snap_eligible": false,
  "gift_card": false,
  "available_since": "2026-03-31",
  "online_stock": { "status": "IN_STOCK", "in_stock": true, "units": 47340, "orderable_units": 47340 },
  "specifications": [
    { "name": "Length", "value": "9 in" },
    { "name": "Width", "value": "9 in" },
    { "name": "Material", "value": "Paper" },
    { "name": "Microwave Safe", "value": "Yes" }
  ],
  "categories": [
    { "id": "574", "name": "Party Supplies", "dimension_id": "4070223595", "url": "https://www.dollartree.com/department/party-supplies" },
    { "id": "511", "name": "Disposable Tableware", "dimension_id": "334265920", "url": "https://www.dollartree.com/party-supplies/disposable-tableware" }
  ],
  "child_skus": [
    { "sku_id": "221159", "color": "Default", "size": "Default", "list_price": 1.5, "sale_price": null, "sale_starts": null, "sale_ends": null, "active": true }
  ],
  "currency": "USD"
}
```

$45.00 / 30 = $1.50 a pack, the same as `price`; the order minimum is 5 packs as Dollar Tree gives it. `online_stock` is the units Dollar Tree can ship from its online inventory, not a store's units. An unknown item is a charged `404`.

### Units at a store and the stores nearby

```bash
curl -X POST https://api.scavio.dev/api/v1/dollartree/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "221159", "store": "5126"}'
```

Captured `data` (2026-11-25 UTC, 27 seconds; 3 of 63 nearby stores shown, `notes` dropped):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "locale": "en-US" },
  "item_id": "221159",
  "item": {
    "name": "9-in. White Paper Plates, 40-ct. Packs",
    "url": "https://www.dollartree.com/the-home-store-9-in-uncoated-white-paper-plates-40-pc-pack/221159",
    "price": 1.5
  },
  "store": { "store_number": "5126", "units": 116, "status": "AVAILABLE", "in_stock": true, "unit_size": 1 },
  "nearby_stores": [
    { "store_number": "5849", "units": 66, "status": "AVAILABLE", "in_stock": true },
    { "store_number": "3789", "units": 170, "status": "AVAILABLE", "in_stock": true },
    { "store_number": "4514", "units": 104, "status": "AVAILABLE", "in_stock": true }
  ],
  "nearby_in_stock": 59,
  "ship_to_home": { "available": true, "units": 75570, "cases": 2374, "case_size": 30, "eta": "2026-12-02", "express_eta": "2026-11-30", "back_order": false },
  "ship_to_store": { "available": false, "units": 0, "cases": 0, "case_size": 30, "eta": "2026-12-05" },
  "split_case_ship_to_home": false
}
```

Store 5126 is 2182 3rd Avenue, New York, NY (East Harlem). 59 of the 63 nearby stores were in stock; 4 read `OUT_OF_STOCK` with 0 units. `unit_size` 1 means the store sells single packs; `ship_to_home` counts whole cases of 30 for delivery. Units are as Dollar Tree reports them at the moment of the call. An unknown item or store number is a charged `404`.

### Stores near a ZIP (5 credits)

```bash
curl -X POST https://api.scavio.dev/api/v1/dollartree/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "60540"}'
```

Captured `data` (2026-11-25 UTC; 1 of 20 stores shown, `hours` cut to 1 of 7, `notes` dropped):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "locale": "en-US" },
  "location": "60540",
  "total": 263,
  "count": 20,
  "stores": [
    {
      "position": 1,
      "store_number": "9207",
      "name": "Dollar Tree",
      "location_note": "Green Trails Shopping Center",
      "address": { "line1": "2709 Maple Avenue", "line2": null, "city": "Lisle", "state": "IL", "zip": "60532-3280", "country": "US" },
      "phone": "+13312511513",
      "latitude": 41.77916091329374,
      "longitude": -88.1048094079519,
      "distance_miles": 2.38,
      "closed": false,
      "timezone": "America/Chicago",
      "hours": [{ "day": "monday", "open": "08:00", "close": "22:00", "closed": false }],
      "holiday_hours": [{ "date": "2026-11-26", "open": "08:00", "close": "17:00", "closed": false }],
      "reopen_date": null,
      "amenities": ["Frozen/Refrigerated Foods", "Snack Zone™", "Greeting Cards: Expressions from Hallmark", "Accepts EBT", "New Items, Great Value"],
      "accepts_ebt": true,
      "frozen_foods": true,
      "more_choices": true,
      "store_pickup": false,
      "pickup_and_delivery": ["In-Store Pickup", "Delivery"],
      "payment_options": ["American Express", "Cash", "MasterCard", "Visa"],
      "slug": "il/lisle/2709-maple-avenue",
      "url": "https://locations.dollartree.com/il/lisle/2709-maple-avenue"
    }
  ]
}
```

`total` is the number of stores Dollar Tree's locator counts around the place (263 here); 20 come back, in its order. `store_number` is the input of store-stock; `slug` and `url` are the input of store. 19 of the 20 read `more_choices` `true` (store 1340, Glen Ellyn, read `false`).

### Newest reviews with syndication flags

```bash
curl -X POST https://api.scavio.dev/api/v1/dollartree/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "206652"}'
```

Captured `data` (2026-11-25 UTC, 31 seconds; 2 of 97 reviews shown, `notes` dropped):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "locale": "en-US" },
  "item_id": "206652",
  "item": { "name": "Crest Tartar Protection Toothpaste, 2.9 oz. Tubes", "url": "https://www.dollartree.com/crest-tartar-protection-toothpaste-29oz-tubes/206652" },
  "rating": 4.3,
  "review_count": 98,
  "rating_breakdown": [
    { "stars": 5, "count": 75, "percent": 76.5 },
    { "stars": 4, "count": 5, "percent": 5.1 },
    { "stars": 3, "count": 3, "percent": 3.1 },
    { "stars": 2, "count": 2, "percent": 2 },
    { "stars": 1, "count": 13, "percent": 13.3 }
  ],
  "recommended_count": 81,
  "not_recommended_count": 13,
  "total": 97,
  "count": 97,
  "sort": "newest",
  "reviews": [
    {
      "id": "249191960",
      "rating": 5,
      "rating_range": 5,
      "title": "Good for teeth",
      "text": "When I started using the tartar control toothpaste (back before all these other EXPENSIVE options were available), my teeth cleanings at the dentist went much better and faster.  So I know this works.  It is so hard to find any more (even on Crest's website it doesn't come up), so I'm happy Dollar Tree still carries it.",
      "date": "2026-04-01T18:23:21.000+00:00",
      "recommended": null,
      "syndicated": false,
      "syndication_source": null,
      "badges": [],
      "secondary_ratings": [],
      "helpful_votes": 0,
      "unhelpful_votes": 0,
      "locale": "en_US",
      "photos": [],
      "responses": []
    },
    {
      "id": "242826608",
      "rating": 5,
      "rating_range": 5,
      "title": "Great product!",
      "text": "I’ve been using this toothpaste for years. It’s exactly what I need, tarter control & cavity prevention with no harsh whitening chemicals. But now I can’t find this anywhere! I’m so upset. Please, please, please bring this back.",
      "date": "2021-02-27T18:35:56.000+00:00",
      "recommended": true,
      "syndicated": true,
      "syndication_source": "crest.com",
      "badges": [],
      "secondary_ratings": [],
      "helpful_votes": 0,
      "unhelpful_votes": 0,
      "locale": "en_US",
      "photos": [],
      "responses": []
    }
  ]
}
```

95 of the 97 reviews were syndicated from crest.com; the oldest read 2010-01-12. `rating`, `review_count` and `rating_breakdown` cover every rating of the item, ratings without text included, so `review_count` (98) can exceed `total` (97). There is no paging past the newest batch, no other sort and no star filter.

### Search, category, brand, deals, categories, store and Canada

- `/search` `{"q": "paper plates"}`: `total` 61, 48 per page, 2 pages; Heavy-Duty 10-in Ultra Paper Plates, 10-pc Pack. (`380886`) $1.50, `case_price` 36 for 24, `minimum_quantity` 24 first. Facets: Category, Product Availability, Average Rating And Up, Price (1.25: 32, 1.50: 26, 4.00: 2, 5.00: 1), Brand, Material Base, Finish Base, Dishwasher Safe, Microwave Safe, BPA Free. An item number as `q` answers with that item.
- `/category` `{"category": "3804024826"}`: Christmas Decor, `total` 153, 4 pages, such as Christmas Theme Car Decor, Assorted Cars (`355419`) $7.00, $84.00 for 12, and Metal Mini Tree Decor (`427551`) $1.00, $36.00 for 36. An unknown category is a charged `404`.
- `/brand` `{"brand": "Dixie"}`: 6 items, all $4.00, such as Dixie Ultra Paper Bowls, 20 oz., 26-ct. (`390704`) $24.00 for 6 and Dixie Ultra Paper Plate, 20-pc Pack (`412887`) $160.00 for 40. Brand names are as Dollar Tree writes them; `other_spellings` lists the same brand under other spellings (send an `id` in `filters`). A brand Dollar Tree does not list is a charged `404`.
- `/deals` `{}` (`type` `sale`): 1 item that day, RUSSELL STOVER Christmas Milk Chocolate Marshmallow Candy Ornament, 1.3 oz. (`405615`) with `price` 1 and `list_price` 1.25, `case_price` 18 for 18, `snap_eligible` true. Dollar Tree publishes no validity dates. `{"type": "more_choices"}` reads MORE CHOICES, `{"type": "new"}` New Arrivals.
- `/categories` `{}`: 16 departments with 520 categories in all, such as Party Supplies (`4070223595`), Holidays (`2264625405`) and MORE CHOICES (`703144065`). The tree includes seasonal categories that can be empty out of season.
- `/store` `{"slug": "ny/new-york/2182-3rd-avenue"}`: store 5126, 3rd Avenue East Harlem, open 08:00-21:00 every day, holiday hours 08:00-17:00 on 2026-11-26, `accepts_ebt` true, `frozen_foods` true, and 4 nearby stores with addresses. An unknown store page is a charged `404`.
- Canada: `/store` `{"slug": "on/toronto/2340-eglinton-ave-west", "country": "ca"}`: store 40144, Westside Mall, Toronto, ON, `currency` `null`, `accepts_ebt` `null`, with nearby Canadian stores. No Canadian products or prices exist on any endpoint.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def dollartree(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/dollartree/{endpoint}", headers=HEADERS, json=body, timeout=300)
    r.raise_for_status()
    return r.json()

# 1. Items for a keyword, lowest unit price first (1 credit)
hits = dollartree("search", {"q": "paper plates", "sort": "price_low"})["data"]
for i in hits["items"][:5]:
    line = f'{i["item_id"]} {i["name"]} ${i["price"]:.2f} a unit'
    if i["case_price"] is not None:
        # Dollar Tree's own case figures; show the division.
        line += f' / ${i["case_price"]:.2f} for {i["case_pack"]} = ${i["case_price"] / i["case_pack"]:.2f}'
    print(line, "min", i["minimum_quantity"])

# 2. Stores near a ZIP (5 credits): store numbers for store-stock
stores = dollartree("stores", {"zip": "60540"})["data"]["stores"]
first = stores[0]
print(first["store_number"], first["address"]["city"], first["distance_miles"])

# 3. Units at that store and the stores nearby (1 credit, tens of seconds)
stock = dollartree("store-stock", {"item_id": "221159", "store": first["store_number"]})["data"]
print("store", stock["store"]["store_number"], stock["store"]["units"], stock["store"]["status"])
print("nearby in stock", stock["nearby_in_stock"], "of", len(stock["nearby_stores"]))

# Prices and units can change between calls. Store each answer with fetched_at
# and run this on a schedule: that stored series is your history (Dollar Tree
# shows only the current price and the current units).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` {`country`, `language`, `currency`, `locale`} (`USD`, or `null` for a Canadian store page) and `notes`.

- **item** (search, category, brand, deals) - `position`, `item_id`, `name`, `brand`, `url`, `image`, `price`, `list_price`, `on_sale`, `unit_price_text`, `case_price`, `case_pack`, `minimum_quantity`, `split_case` {`available`, `multiple`, `fee`}, `not_for_individual_sale`, `rating`, `review_count`, `online_availability`, `in_stock_online`, `in_store_only`, `clearance`, `new`, `snap_eligible`, `upcs`, `store_brand`, `categories` (names).
- **lists** - `page`, `page_size`, `total`, `total_pages`, `count`, `sort`, `filters_applied[]` {`facet`, `label`, `count`}, `resolved_filters[]` {`facet`, `requested`, `id`, `label`, `other_spellings`}, `price_range`, `items[]`, `facets[]` {`key`, `name`, `multi_select`, `values[]` {`id`, `label`, `count`}} (send `id` back in `filters`). Search adds `query`, `corrected_query`, `category`; category `category_id`, `query`, `category` (name); brand `brand`, `brand_id`, `other_spellings[]` {`id`, `label`, `count`}, `category`; deals `type`, `query`, `category`.
- **product** - `requested_item_id`, `item_id`, `name`, `brand`, `store_brand`, `url`, `image`, `images`, `description`, `long_description`, `price`, `list_price`, `sale_price`, `on_sale`, `unit_price_text`, `case_price`, `case_pack`, `minimum_quantity`, `split_case` {`available`, `multiple`, `fee`}, `not_for_individual_sale`, `varying_case_packs`, `assortment`, `assortment_details`, `upcs`, `rating`, `review_count`, `in_store_only`, `store_pickup_eligible`, `shippable`, `online_only`, `delivery_options`, `order_limit`, `clearance`, `new`, `deals`, `snap_eligible`, `gift_card`, `available_since`, `online_stock` {`status`, `in_stock`, `units`, `orderable_units`}, `specifications[]` {`name`, `value`}, `categories[]` {`id`, `name`, `dimension_id`, `url`}, `child_skus[]` {`sku_id`, `color`, `size`, `list_price`, `sale_price`, `sale_starts`, `sale_ends`, `active`}, `currency`.
- **store-stock** - `item_id`, `item` {`name`, `url`, `price`}, `store` {`store_number`, `units`, `status`, `in_stock`, `unit_size`}, `nearby_stores[]` {`store_number`, `units`, `status`, `in_stock`}, `nearby_in_stock`, `ship_to_home` {`available`, `units`, `cases`, `case_size`, `eta`, `express_eta`, `back_order`}, `ship_to_store` {`available`, `units`, `cases`, `case_size`, `eta`}, `split_case_ship_to_home`.
- **stores** - `location`, `total`, `count`, `stores[]` {`position`, `store_number`, `name`, `location_note`, `address` {`line1`, `line2`, `city`, `state`, `zip`, `country`}, `phone`, `latitude`, `longitude`, `distance_miles`, `closed`, `timezone`, `hours[]` {`day`, `open`, `close`, `closed`}, `holiday_hours[]` {`date`, `open`, `close`, `closed`}, `reopen_date`, `amenities`, `accepts_ebt`, `frozen_foods`, `more_choices`, `store_pickup`, `pickup_and_delivery`, `payment_options`, `slug`, `url`}.
- **store** - the store fields above without `position` and `distance_miles`, plus `nearby_stores[]` {`store_number`, `address` {`line1`, `city`, `state`, `zip`}, `closed`, `slug`, `url`}.
- **categories** - `category`, `parents`, `count`, `total_categories`, `categories[]` {`id`, `name`, `dimension_id`, `url`, `route`, `children[]`}.
- **reviews** - `item_id`, `item` {`name`, `url`}, `rating`, `review_count`, `rating_breakdown[]` {`stars`, `count`, `percent`}, `recommended_count`, `not_recommended_count`, `total`, `count`, `sort`, `reviews[]` {`id`, `rating`, `rating_range`, `title`, `text`, `date`, `recommended`, `syndicated`, `syndication_source`, `badges`, `secondary_ratings[]` {`name`, `value`, `range`}, `helpful_votes`, `unhelpful_votes`, `locale`, `photos[]` {`url`, `thumbnail_url`}, `responses[]` {`text`, `date`, `department`}}.

## Guardrails

- Name it "Dollar Tree (dollartree.com, the US and Canada discount variety store chain)" on first mention. Family Dollar is a separate company and is not read.
- Prices: quote `price` as the online unit price at dollartree.com with the `fetched_at` date, and `case_price` with `case_pack`. Prices are one national online price: never call a price a store's or a ZIP's price, and never present it as the store shelf price (Dollar Tree says prices may vary between stores and online).
- Report Dollar Tree's own price, list price, case price, units and flags plus the arithmetic. Never write that everything at Dollar Tree costs $1.25, never describe a price as an increase, a cut or shrinking packs, and never judge an item's quality or value.
- Case and unit: show the case price, the units in the case and the division; quote `minimum_quantity` and `split_case` as given. Never compute a case price where `case_pack` or `case_price` is `null`.
- Comparing Dollar Tree with Dollar General, Walmart, Target or Instacart: compare only the same item (same UPC), each with its date and its source, unit price against unit price. Instacart's prices are Instacart's, never Dollar Tree's shelf price. Never call one retailer cheaper beyond the numbers shown.
- Stock: `units` as Dollar Tree reported them at the moment of the call; Scavio makes no promise of their accuracy. Never promise pickup, shipping or a delivery date.
- Reviews: no reviewer names are returned. Say which reviews are syndicated and from where (`syndication_source`).
- Not available: UPC search (use the item number), search suggestions, the weekly ad, deal validity dates, Quick Order or bulk ordering, gift cards, Canadian products and prices (Dollar Tree Canada has no shopping site), price history (poll and store), checkout, cart or ordering. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not collect or store Dollar Tree data: each call fetches the public Dollar Tree page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Dollar Tree's terms of use cover how its site may be used (personal, non-commercial use); read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Dollar Tree product photos or logos; link products by `url` instead.
- Never fabricate prices, case packs, units, item numbers, store numbers, UPCs, hours, dates or ratings. Only return what the API returned, with the `fetched_at` time and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` other than `us` or `ca`; `ca` on any endpoint but store; a `language` other than `en`; an `item_id` that is not a Dollar Tree item number (digits, or `FD` and digits); a `url` that is not a dollartree.com product link; store-stock without `store`, or a `store` that is not a store number; a `state` that is not two letters; a `zip` that is not a US ZIP; stores without `zip` or `city`, or a city without its state; store without `url` or `slug`, or a US store page with `country` `ca` (or a Canadian page without it); a `category` that is not a `dimension_id` or a dollartree.com category link; deals `category` with `type` `new` or `more_choices`; a `filters` value that is not a refinement id, or more than 10; a `page` outside 1-200 or `page_size` outside 1-250; an unknown `sort` or `type`; a `rating` outside 1-5; a `price_point` of 0 or less; `min_price` above `max_price`, or `max_price` at or below 0.05.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Dollar Tree has no item <item_id> ...", "Dollar Tree has no item <item_id> or no store <store> ...", "Dollar Tree has no category <id>. ...", "Dollar Tree lists no brand named ...", "Dollar Tree has no store page <slug>.", "Dollar Tree found no place called <place>.". Take item numbers, store numbers, category ids and filters from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api).
- `502` means Dollar Tree data was temporarily unavailable ("Dollar Tree is temporarily unavailable. Please try again.", "Dollar Tree store stock is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Dollar Tree is busy ("Dollar Tree is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.84.0
npm install scavio@0.85.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.dollartree.search({ q: "paper plates", sort: "price_low" });
const { data: item } = await scavio.dollartree.product({ item_id: "221159" });
const { data: stores } = await scavio.dollartree.stores({ zip: "60540" });
const { data: stock } = await scavio.dollartree.storeStock({ item_id: "221159", store: "5126" });
const { data: store } = await scavio.dollartree.store({ slug: "ny/new-york/2182-3rd-avenue" });
const { data: canada } = await scavio.dollartree.store({ slug: "on/toronto/2340-eglinton-ave-west", country: "ca" });
const { data: decor } = await scavio.dollartree.category({ category: "3804024826", price_point: 1.25 });
const { data: tree } = await scavio.dollartree.categories();
const { data: dixie } = await scavio.dollartree.brand({ brand: "Dixie" });
const { data: more } = await scavio.dollartree.deals({ type: "more_choices" });
const { data: reviews } = await scavio.dollartree.reviews({ item_id: "206652" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.dollartree.search(...)`, `product`, `category`, `categories`, `brand`, `deals`, `store_stock`, `stores`, `store` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 10 endpoints as tools: `search_dollartree`, `get_dollartree_product`, `get_dollartree_category`, `get_dollartree_categories`, `get_dollartree_brand`, `get_dollartree_deals`, `get_dollartree_store_stock`, `get_dollartree_stores`, `get_dollartree_store` and `get_dollartree_reviews`. Dollar Tree is opt-in: add `dollartree` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.84.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,dollartree"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/dollartree-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api), [product](https://scavio.dev/docs/dollartree-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api), [category](https://scavio.dev/docs/dollartree-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api), [categories](https://scavio.dev/docs/dollartree-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api), [brand](https://scavio.dev/docs/dollartree-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api), [deals](https://scavio.dev/docs/dollartree-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api), [store stock](https://scavio.dev/docs/dollartree-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api), [stores](https://scavio.dev/docs/dollartree-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api), [store](https://scavio.dev/docs/dollartree-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api), [reviews](https://scavio.dev/docs/dollartree-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api). Overview: [Dollar Tree API](https://scavio.dev/dollartree-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-tree-bulk-prices-api).
