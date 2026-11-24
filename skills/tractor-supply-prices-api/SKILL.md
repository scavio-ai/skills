---
name: tractor-supply-prices-api
description: Tractor Supply API for Tractor Supply (tractorsupply.com, the US rural lifestyle retailer) - Tractor Supply prices by store, one item priced for the store you pick by store number or for the nearest store Tractor Supply lists for a US ZIP (priced_for names the store and its price zone; Tractor Supply's terms note that prices may vary in different geographic markets, and the same 50 lb bag of Producer's Pride 16% Layer Pellets read $14.49 at Glendive, MT and $20.19 at Port Orchard, WA on one day), one item's price at up to 25 stores or at the stores nearest a ZIP in one call with the low and the high, the exact units on hand per store with stock in transit and its pickup date, and pickup and delivery options with dates for one store and ZIP; keyword, item-number and UPC search, category, brand and deals (on sale or new) lists, 24 to 200 per page, sorted by price, rating, name or newest and filtered by brand, on sale, pickup, rating or any facet, each item with Tractor Supply's own unit price (per lb on feed); one product in full with UPC, was price, pickup price, the manufacturer's minimum advertised price where Tractor Supply flags it, rating and review count, sizes, fulfillment flags and dated promotions; the stores nearest a ZIP and one store with address, phone, hours, services (propane refill, trailer rental and more), price zone and dated store events; Tractor Supply's departments and categories. 12 endpoints, 1 credit per call, product 2 on a store's first lookup, store-prices 1 per 5 lookups. US only. No review text, weekly ad, search suggestions, price history, Neighbor's Club prices or checkout.
version: 1.0.0
tags: tractor-supply, tractorsupply, tractorsupply-com, tractor-supply-api, tractor-supply-prices, tractor-supply-prices-by-store, tractor-supply-feed-prices, tractor-supply-chicken-feed, tractor-supply-dog-food, tractor-supply-inventory, tractor-supply-inventory-checker, tractor-supply-stock-checker, tractor-supply-store-inventory, tractor-supply-stores, tractor-supply-store-hours, tractor-supply-propane, tractor-supply-deals, tractor-supply-black-friday, tractor-supply-promotions, producers-pride, dumor, purina, nutrena, chicken-feed, layer-feed, feed-prices, price-per-pound, farm-supply, farm-supply-prices, farm-and-ranch, store-prices, store-inventory, store-stock, us-retail, price-monitoring, usd, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/tractorsupply-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api
---

# Tractor Supply API - Store Prices, Feed Prices, Inventory

Read Tractor Supply (tractorsupply.com, the US rural lifestyle retailer): one product priced for the store you pick or the store nearest a ZIP, one item's price at up to 25 stores in one call, the exact units on hand per store with stock in transit, pickup and delivery options with dates, keyword and item-number search, category, brand and deals lists, the stores nearest a ZIP, one store's details, the category tree and an item's dated promotions. All 12 endpoints return structured JSON at 1 credit per call (product 2 on a store's first lookup, and store prices by the number of stores, listed below).

**The job this skill is for: Tractor Supply feed prices by store.** Tractor Supply prices by store, and the same item can be priced differently at different stores: Tractor Supply's own terms say prices "may vary ... due to varying conditions in different geographic markets and areas". `/product` with a `store` (or a `zip`) returns the price as Tractor Supply shows it for that store, and `priced_for` names the store and its price zone. On 2026-11-24 the Producer's Pride 16% Layer Pelleted Chicken Feed, 50 lb. Bag (item `2340147`) read $14.49 at store 1933 (Glendive, MT, zone 81), $20.19 at store 1923 (Port Orchard, WA, zone 92) and $16.99 at store 1600 (Buda, TX, zone 13): $0.29, $0.40 and $0.34 a pound for the 50 lb bag. `/store-prices` reads all three in one call, `/store-stock` gives the units on hand at each store, and `/fulfillment` the pickup and delivery dates. Pair it with `walmart-product-data`, `chewy-product-data` and `petsmart-product-data` for the same national-brand bag (Purina, Nutrena, Blue Buffalo, matched by brand, formula and bag size) and `ace-hardware-prices-api` for the same hardware item at an Ace store.

Nine limits shape every answer, so say them plainly:
- **1 credit per call; product 2 on a store's first lookup; store prices by stores.** Product is 1, and 2 the first time Scavio looks up a store's details (its zone, city and state). Store prices is 1 per 5 lookups: each store's price, each store's details the first time, and the item (3 new stores 2, 25 new stores 11). Store stock is 1 (10 stores per lookup). Everything else is 1. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not. A request needs the most it can spend available in the balance (2 on most endpoints, store prices up to 11): the charge is still `credits_used`.
- **Every price needs a store or a ZIP.** Search, category, brand, deals and product take `store` (a Tractor Supply store number) or `zip` (a 5-digit US ZIP: the nearest store Tractor Supply lists for it is used), not both; without either the answer is a `400`, not charged. There is no default store. Store numbers are 1-5 digits as Tractor Supply gives them (`303`, `1933`, `3047`); `/stores` lists the stores nearest a ZIP with their numbers.
- **Read `priced_for` before quoting a price.** `priced_for` {`store_id`, `zone`, `city`, `state`, `from`, `zip`} names the store the prices are for: `from` is `store` when you sent a store and `nearest_store_to_zip` when you sent a ZIP. `zone` is the store's price zone as Tractor Supply gives it. Report "$20.19 at Tractor Supply store 1923 (Port Orchard, WA) on 2026-11-24", never "Tractor Supply's price".
- **`mapp` is reported as given, not a promise of one price.** Where Tractor Supply flags a manufacturer's minimum advertised price, the item carries `mapp` {`type`, `min`, `max`}. Flagged items can still show different prices at different stores, and a price can sit below `mapp.min` (measured 2026-11-24). Report `mapp` as given, next to the price.
- **The 7-digit item number is the input.** `items[].item_number` (`2340147`) is the size the item's link names and the input of product, store prices, store stock, fulfillment and promotions. `part_number` (`234014799`) is the product's, not an input. Store stock with a `part_number` is a charged `404` ("no stock record"). A product link to a multi-size product answers `type` `product` with `price` to `price_max` across sizes: send a size's item number (`variants[].item_number`, or `item_numbers` on a list item) for one size's price.
- **Store stock is exact units as Tractor Supply reports them.** `/store-stock` returns `units`, `status` ("Available", "Unavailable"), `in_stock` and `in_transit` [{`units`, `pickup_date`, `source`}] per store. A store number Tractor Supply does not know is dropped and listed in `unknown_stores` (not reported as 0); a store that did not answer is in `failed_stores` (retry it). Stock is as Tractor Supply reports it at the moment of the call.
- **Per pound: Tractor Supply's unit price, or the stated bag weight.** List items (search, category, brand, deals) carry `unit_price` {`amount`, `unit`} as Tractor Supply gives it (2340147 at 1933: 0.29 a `lb`). Product and store prices carry no unit price: divide the price by the bag weight only where the name or `options` state it ("50 lb. Bag", `Feed Packaged Weight` "50 lb"), and show the arithmetic.
- **Ratings, not reviews.** Items and products carry `rating` and `review_count`. No review text, Q&A or reviewer details.
- **US only, no price history.** `country` is `us` (default); anything else is a `400`, not charged. Nothing is cached or kept: poll and store your own series.

Tractor Supply has no public developer API. Publishers can join its affiliate programme on Partnerize for links and banners, suppliers connect through Tractor Supply's vendor portal and EDI, and store prices and stock are shown on tractorsupply.com for the ZIP code or store you pick; this skill reads those public pages with one Scavio key.

Tractor Supply Company (NASDAQ: TSCO) describes itself as the largest rural lifestyle retailer in the US: 2,486 Tractor Supply stores in 49 states at September 26, 2026 (Q3 2026 release, Oct 22, 2026) and $15.52 billion in net sales for fiscal 2025 (release Jan 29, 2026). Quote these with their source, never from the samples.

See also: for the same national-brand bag at Walmart use `walmart-product-data`; at Chewy `chewy-product-data`; at PetSmart `petsmart-product-data`; at Petco `petco-product-data`; the same hardware item at an Ace store `ace-hardware-prices-api`; Home Depot `home-depot-product-data`; Lowe's `lowes-product-data`; Tractor Supply as an Instacart retailer `instacart-api`; prices across retailers `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Check a Tractor Supply item's price at a given store or at the store nearest a ZIP, or compare one item's price across several Tractor Supply stores
- Price a bag of chicken, horse, livestock feed or dog food at Tractor Supply per pound, store by store
- Check how many units a Tractor Supply store has on hand, or which stores near a ZIP have it, with stock in transit and its pickup date
- Check pickup, ship-to-store, same-day or standard delivery for an item at a store and ZIP, with dates and order cut-offs
- Search tractorsupply.com by keyword, item number or UPC, sorted by price or rating or filtered by brand, on sale, pickup or a facet such as bag weight
- List a Tractor Supply category, a brand's products (Producer's Pride, DuMOR, Purina, 4health), the items on sale or the new arrivals
- Read one Tractor Supply product in full: UPC, was price, pickup price, sizes, rating and review count, fulfillment flags and promotions with dates
- Find the Tractor Supply stores near a ZIP, or one store's hours, services (propane refill, trailer rental), price zone and events
- Compare one national-brand item at Tractor Supply, Walmart, Chewy or PetSmart (with `walmart-product-data`, `chewy-product-data` and `petsmart-product-data`)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 1 credit; product costs 2 the first time a store is looked up, and store prices 1 per 5 lookups (3 new stores 2).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, search took 3-5 seconds, store and stores 4-6, store stock and fulfillment 7-9, category and deals 8-11, store prices 5-13, promotions 9-19 and product 14-38. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/tractorsupply/product` | One product or size by item number or link, priced for one store (`priced_for`): price, was price, pickup price, price type, `mapp`, UPC, rating, review count, sizes, fulfillment flags, promotions with dates | 1 (2 on a store's first lookup) |
| `POST /api/v1/tractorsupply/store-prices` | One item's price at 1-25 stores or at the stores nearest a ZIP, with zone, was price, pickup price and `mapp` per store and `price_range` {`min`, `max`} | 1 per 5 lookups (3 new stores 2, 25 new stores 11) |
| `POST /api/v1/tractorsupply/store-stock` | Units on hand for one item at 1-25 stores or at the stores nearest a ZIP, with status and stock in transit with its pickup date | 1 |
| `POST /api/v1/tractorsupply/fulfillment` | Pickup units at one store and the delivery options to a ZIP (standard, same day, ship to store) with delivery dates and order cut-offs | 1 |
| `POST /api/v1/tractorsupply/search` | Keywords, an item number or a UPC, priced for one store: 24-200 per page with total, facets and `unit_price`; `redirected_to` when Tractor Supply sends it to a category | 1 |
| `POST /api/v1/tractorsupply/category` | One category's products by link, path, slug or listing id, priced for one store, sorted, filtered and paged | 1 |
| `POST /api/v1/tractorsupply/brand` | One brand's products, optionally matching keywords, priced for one store | 1 |
| `POST /api/v1/tractorsupply/deals` | The products on sale (`type` `sale`) or the new arrivals (`type` `new`), priced for one store | 1 |
| `POST /api/v1/tractorsupply/promotions` | The promotions Tractor Supply lists for one item, with start and end dates | 1 |
| `POST /api/v1/tractorsupply/stores` | Up to 10 stores nearest a ZIP: address, phone, distance, hours, services, price zone, events | 1 |
| `POST /api/v1/tractorsupply/store` | One store: address, phone, hours, services, price zone, pickup, events | 1 |
| `POST /api/v1/tractorsupply/categories` | Tractor Supply's departments, or one department's categories (two levels) | 1 |

All 12 endpoints serve `country` `us` only (tractorsupply.com, English, USD).

## Prices: store price, zone, sizes, MAPP

Every priced item carries:

| Field | Meaning |
|---|---|
| `price` | The price of the size the item's link names, as Tractor Supply shows it for the store in `priced_for` |
| `price_min`, `price_max` | Lists: the lowest and highest price across the product's sizes. Product: `price_max` across sizes when `type` is `product` |
| `was_price` | The was price where one price applies; `null` otherwise |
| `on_sale`, `clearance`, `price_type` | Tractor Supply's flags (`price_type` on product and store prices: `regular`, `sale`, `clearance`) |
| `discount_percent` | Computed by Scavio from `was_price`; `null` otherwise |
| `savings_up_to` | {`amount`, `percent`} as Tractor Supply gives it when sizes differ |
| `pickup_price` | Where Tractor Supply gives a separate pickup price; `null` otherwise |
| `unit_price` | Lists: {`amount`, `unit`} as Tractor Supply gives it (`lb` on feed) |
| `mapp` | {`type`, `min`, `max`}: the manufacturer's minimum advertised price where Tractor Supply flags it; `null` otherwise |
| `badge` | Lists: Tractor Supply's badge ("Exclusive", "SALE") |

- **Store price:** every price is for the store in `priced_for`. Captured 2026-11-24 for item `2340147` (Producer's Pride 16% Layer Pellets, 50 lb): store 1933 Glendive, MT (zone 81) $14.49, store 1923 Port Orchard, WA (zone 92) $20.19, store 1600 Buda, TX (zone 13) $16.99. Report each with its store, zone and date.
- **Per pound:** $14.49 / 50 lb = $0.29, $20.19 / 50 lb = $0.40, $16.99 / 50 lb = $0.34. On list items use `unit_price` as given; on product, divide only by a bag weight the name or `options` state.
- **Sizes:** a list item's `price` is the size its link names; `price_min` / `price_max` span the sizes (DuMOR 16% Layer Pellets `1496729` read $16.99 with `price_min` 9.49 over 2 sizes at 1933).
- **Guest prices:** every price is the price shown without an account. Neighbor's Club member prices are not read; Smart Supply subscription offers appear only as promotion text.
- Price differences between stores: describe them from the answers (store, zone, number, date), never why a store prices as it does.

## Workflow

1. **Pick a store.** From the user (a store number), or `/stores` with their `zip` (up to 10 nearest, each with its `store_id` and `zone`). Confirm a store number with `/store` (1 credit): an unknown number is a charged `404`. Or send `zip` on any priced call and read `priced_for`.
2. **Find the item.** `/search` with `query` and `store` (keywords, an item number or a UPC), or `/category` (`/tsc/catalog/poultry-feed`), `/brand` (`Producer's Pride`) or `/deals`; each item's `item_number` is the input of product, store prices, store stock, fulfillment and promotions.
3. **Price it at the store.** `/product` with `item_number` and `store` (or `zip`). Quote `price` with `priced_for`.
4. **Price it across stores.** `/store-prices` with `item_number` and `stores` (up to 25) or `zip` with `limit` (1-10 nearest, default 5). `price_range` gives the low and high across the stores asked; a store with `price` `null` shows no price for the item (it may not be sold there, or the store did not answer: retry it). Compare only answers for the same `item_number` on the same day.
5. **Per pound.** Divide each store's price by the stated bag weight (or read `unit_price` on a list), and show the arithmetic.
6. **Units on hand.** `/store-stock` with `item_number` and `stores` (up to 25) or `zip` with `limit` (1-10, default 5).
7. **Pickup and delivery.** `/fulfillment` with `item_number`, `store` and `zip` (and `quantity`): pickup units and each delivery option with its `delivery_date` and `order_by` cut-off.
8. **Promotions.** Product carries `promotions` for the item; `/promotions` with `item_number` reads them without a store. Quote `name`, `starts` and `ends` (`null` is open-ended) in Tractor Supply's words.
9. **Narrow a list.** `sort`, `brand`, `on_sale`, `new`, `pickup`, `rating` (1-4 stars and up) and facet `filters` (`facets[].values[].filter`, e.g. a `Feed Packaged Weight` value), at most 6 in all; `page_size` (24, 48, 96, 200) and `page` (1-100).
10. **Watching prices:** there is no history. Poll the same item numbers at the same stores on a schedule and store each answer with its `fetched_at` and `priced_for`; that stored series is the history. Compare only answers priced for the same store.

## Parameters

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_number` | string or integer | one of | A Tractor Supply item number (`items[].item_number`: `2340147`) |
| `url` | string | one of | A tractorsupply.com product link (`items[].url`, `/tsc/product/...`). Send `item_number` or `url`, not both |
| `store` | string or integer | one of | A Tractor Supply store number (`1933`) |
| `zip` | string | one of | A 5-digit US ZIP: the nearest store Tractor Supply lists for it. Send `store` or `zip`, not both |
| `country` | string | `us` | `us` only |

### Store prices (`/store-prices`), store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_number` | string or integer | required | The 7-digit Tractor Supply item number |
| `stores` | array | one of | 1-25 store numbers (`["1933", "1923", "1600"]`) |
| `store` | string or integer | one of | One store number |
| `zip` | string | one of | A US ZIP: the stores Tractor Supply lists nearest it. Send `stores` or `zip`, not both |
| `limit` | integer | 5 | With `zip`: how many of the nearest stores (1-10) |

### Fulfillment (`/fulfillment`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_number` | string or integer | required | The 7-digit item number |
| `store` | string or integer | required | The pickup store number |
| `zip` | string | required | The delivery ZIP |
| `quantity` | integer | 1 | 1-999 |

### Search (`/search`), category (`/category`), brand (`/brand`), deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Keywords, an item number or a UPC; 1-200 chars. On brand and deals, optional: only products matching it |
| `category` | string or integer | category: required | A category link or path (`/tsc/catalog/poultry-feed`), its slug (`poultry-feed`) or a listing category id (`breadcrumbs[].category_id`: `24534`) |
| `brand` | string | brand: required | A brand as Tractor Supply names it (`items[].brand`: `Purina`, `Producer's Pride`, `4health`). On search, category and deals, only that brand |
| `type` | string | `sale` | Deals: `sale` (products on sale) or `new` (new arrivals) |
| `store` / `zip` | string | one required | The store the prices are for (see product) |
| `sort` | string | `popular` | `popular` (Most Popular), `rating`, `name_asc`, `name_desc`, `price_asc`, `price_desc`, `recent`, `new_arrivals` |
| `on_sale`, `new`, `pickup` | boolean | none | Only products on sale, new arrivals, or offered for pickup at the store (not on deals for `on_sale` / `new`: use `type`) |
| `rating` | integer | none | Only products rated at least this many stars (1-4) |
| `filters` | array | none | Facet filters from an earlier answer (`facets[].values[].filter`, sent exactly as given); at most 6 with `brand`, `on_sale`, `new`, `pickup` and `rating` |
| `page_size` | integer | 24 | 24, 48, 96 or 200 |
| `page` | integer | 1 | 1-100 |
| `country` | string | `us` | `us` only |

### Stores (`/stores`), store (`/store`), categories (`/categories`), promotions (`/promotions`)

`/stores` takes `zip` (required) and `limit` (1-10, default 10). `/store` takes `store` (required). `/categories` takes an optional `parent_id` (a `categories[].tree_id`) for its categories, two levels; without it, the departments. Tree ids are not listing ids: send a category's `url` to `/category`. `/promotions` takes `item_number` (required).

## Examples

### One item priced for a store

```bash
curl -X POST https://api.scavio.dev/api/v1/tractorsupply/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_number": "2340147", "store": "1933"}'
```

Captured `data` (2026-11-24; `description` and `image` dropped, `breadcrumbs` and `promotions` cut to 1, `notes` cut to 2):

```json
{
  "country": "us",
  "currency": "USD",
  "store_requested": "1933",
  "zip_requested": null,
  "priced_for": { "store_id": "1933", "zone": "81", "city": "Glendive", "state": "MT", "from": "store", "zip": null },
  "item_number": "2340147",
  "part_number": "234014799",
  "type": "item",
  "name": "Producer's Pride 16% Layer Pelleted Chicken Feed, 50 lb. Bag",
  "brand": "Producer's Pride",
  "url": "https://www.tractorsupply.com/tsc/product/producers-pride-16-layer-pellets-poultry-feed-50-lb-2340147",
  "price": 14.49,
  "price_max": null,
  "was_price": null,
  "was_price_max": null,
  "pickup_price": null,
  "price_type": "regular",
  "on_sale": false,
  "discount_percent": null,
  "savings_up_to": null,
  "mapp": null,
  "rating": 4.4424,
  "review_count": 1824,
  "availability": "Online In Stores",
  "upc": "749394340834",
  "vendor_part_number": "3005205-206",
  "buyable": true,
  "specifications": [],
  "options": [{ "name": "Feed Packaged Weight", "value": "50 lb" }],
  "variants": [],
  "parent": { "part_number": "234014799", "url": "https://www.tractorsupply.com/tsc/product/producers-pride-16-layer-pellets-poultry-feed-50-lb" },
  "breadcrumbs": [
    { "name": "Poultry Feed", "url": "https://www.tractorsupply.com/tsc/catalog/poultry-feed", "category_id": "24534" }
  ],
  "fulfillment": { "store_pickup": true, "standard_delivery": true, "same_day_delivery": true, "truck_delivery": null, "shipping_restricted_states": [] },
  "hazmat": null,
  "country_of_origin": null,
  "attachments": [],
  "promotions": [
    {
      "name": "Bulk Discount Buy 20 Get 5% off Each.",
      "description": "Bulk Discount Buy 20 Get 5% off Each. Add to the cart to see the discount.",
      "type": "CategoryLevelPercentDiscount",
      "kind": "product",
      "site_wide": false,
      "starts": "2025-10-08",
      "ends": null
    }
  ],
  "notes": [
    "Prices are as Tractor Supply shows them for the store in priced_for: Tractor Supply prices by store, and the same item can be priced differently at different stores.",
    "Tractor Supply's terms note that prices \"may vary\" in different geographic markets."
  ]
}
```

The same call with `"store": "1923"` answered `priced_for` {`store_id` "1923", `zone` "92", `city` "Port Orchard", `state` "WA"} and `price` 20.19. A 6 ft. Green Studded T-Post (`3609112`) at store 2304 (Middletown, NJ, zone 63) read $5.39 against a `was_price` of $5.89 (`price_type` "sale", `discount_percent` 8, `availability` "In Stores Only"). A product Tractor Supply does not list is a charged `404`.

### One item at several stores

```bash
curl -X POST https://api.scavio.dev/api/v1/tractorsupply/store-prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_number": "2340147", "stores": ["1933", "1923", "1600"]}'
```

Captured `data` (2026-11-24; 1-2 credits for 3 stores, 2 when Scavio has not looked the stores up yet; the second and third stores cut to their prices):

```json
{
  "country": "us",
  "currency": "USD",
  "item_number": "2340147",
  "name": "Producer's Pride 16% Layer Pelleted Chicken Feed, 50 lb. Bag",
  "url": "https://www.tractorsupply.com/tsc/product/producers-pride-16-layer-pellets-poultry-feed-50-lb-2340147",
  "zip_requested": null,
  "count": 3,
  "priced_count": 3,
  "price_range": { "min": 14.49, "max": 20.19 },
  "stores": [
    {
      "store_id": "1933",
      "name": "GLENDIVE MT",
      "city": "Glendive",
      "state": "MT",
      "zone": "81",
      "distance_miles": null,
      "unknown_store": false,
      "price": 14.49,
      "price_max": null,
      "was_price": null,
      "pickup_price": null,
      "price_type": "regular",
      "on_sale": false,
      "discount_percent": null,
      "mapp": null
    },
    { "store_id": "1923", "name": "PORT ORCHARD WA", "city": "Port Orchard", "state": "WA", "zone": "92", "price": 20.19 },
    { "store_id": "1600", "name": "BUDA TX", "city": "Buda", "state": "TX", "zone": "13", "price": 16.99 }
  ],
  "failed_stores": [],
  "notes": [
    "Prices are as Tractor Supply shows them for the store: Tractor Supply prices by store, and the same item can be priced differently at different stores.",
    "A store with price null shows no price for the item (it may not be sold there, or the store did not answer: retry it)."
  ]
}
```

$14.49 to $20.19 for the same 50 lb bag: a $5.70 spread, $0.29 to $0.40 a pound. With `zip` and `limit` instead of `stores`, the answer lists the stores Tractor Supply gives as nearest that ZIP, each with `distance_miles`.

### Units on hand near a ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/tractorsupply/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_number": "2340147", "zip": "59301", "limit": 5}'
```

Captured `data` (2026-11-24, 1 credit; 3 of 5 stores shown):

```json
{
  "country": "us",
  "currency": "USD",
  "item_number": "2340147",
  "zip_requested": "59301",
  "count": 5,
  "in_stock_count": 4,
  "total_units": 341,
  "in_transit_units": 0,
  "stores": [
    {
      "store_id": "1933",
      "name": "GLENDIVE MT",
      "city": "Glendive",
      "state": "MT",
      "distance_miles": 68.8,
      "units": 71,
      "status": "Available",
      "in_stock": true,
      "in_transit": []
    },
    {
      "store_id": "303",
      "name": "BILLINGS MT",
      "city": "Billings",
      "state": "MT",
      "distance_miles": 133,
      "units": 127,
      "status": "Available",
      "in_stock": true,
      "in_transit": []
    },
    {
      "store_id": "3047",
      "name": "BILLINGS (S) MT",
      "city": "Billings",
      "state": "MT",
      "distance_miles": 141.1,
      "units": 0,
      "status": "Unavailable",
      "in_stock": false,
      "in_transit": []
    }
  ],
  "unknown_stores": [],
  "failed_stores": [],
  "not_reported": [],
  "notes": [
    "units is the exact count Tractor Supply reports for each store; in_transit lists stock on its way with the date Tractor Supply gives for pickup. Stock is as Tractor Supply reports it; Scavio makes no promise of its accuracy.",
    "stores are the store(s) Tractor Supply lists nearest ZIP 59301, in its order."
  ]
}
```

The other two stores: 1796 Sidney, MT 75 units and 1916 Sheridan, WY 68. `in_transit` lists {`units`, `pickup_date`, `source`} for stock on its way, when Tractor Supply gives it.

### Pickup and delivery for a store and ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/tractorsupply/fulfillment \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_number": "2340147", "store": "1933", "zip": "59330"}'
```

Captured `data` (2026-11-24):

```json
{
  "country": "us",
  "currency": "USD",
  "item_number": "2340147",
  "store_id": "1933",
  "store": { "name": "GLENDIVE MT", "city": "Glendive", "state": "MT" },
  "zip": "59330",
  "quantity": 1,
  "pickup": { "units": 71, "status": "Available", "in_transit": [] },
  "delivery_options": [
    {
      "type": "ship_to_store",
      "name": "Ship To Store",
      "delivery_date": "2026-12-01",
      "order_by": "2026-11-25T22:59:59Z",
      "order_by_local": "2:59pm",
      "time_zone": "America/Los_Angeles"
    },
    {
      "type": "standard_delivery",
      "name": "Standard Delivery",
      "delivery_date": "2026-11-30",
      "order_by": "2026-11-25T22:59:59Z",
      "order_by_local": "2:59pm",
      "time_zone": "America/Los_Angeles"
    }
  ],
  "same_day_delivery": false,
  "ship_to_store": true,
  "standard_delivery": true,
  "notes": ["Options and dates are as Tractor Supply gives them for the store and ZIP (delivery_date is the latest date Tractor Supply names; order_by is its order cut-off). pickup.units is the count Tractor Supply reports at the store."]
}
```

`delivery_date` is the latest date Tractor Supply names and `order_by` its cut-off in UTC, with `order_by_local` and `time_zone` as Tractor Supply gives them. Quote the dates, never promise them.

### Search, category, brand, deals, promotions, stores, store and categories

- `/search` `{"query": "layer pellets", "store": "1933"}`: `total` 36, 24 per page, 2 pages, 22 facets, priced for store 1933 with Tractor Supply's `unit_price` per pound: Producer's Pride 16% Layer Pellets 50 lb (`2340147`) $14.49 (0.29 a lb, `badge` "Exclusive"), DuMOR 16% Layer Pellets 50 lb (`1496729`) $16.99 (0.34), Nutrena NatureWise 17% Layer Pellets 50 lb (`2494614`) $21.49 (0.43), Purina Layena Layer Pellets (`2800927`) $24.49 (0.49), Kent Home Fresh Extra Egg Layer 50 lb (`2372716`) $22.99 (0.46). Some searches are sent to a category page: `redirected_to` {`type` "category", `url`, `category_id`} and the list is that category's.
- `/category` `{"category": "/tsc/catalog/poultry-feed", "store": "1933"}`: `total` 155, 7 pages, `breadcrumbs` Poultry > Poultry Feed & Treats > Poultry Feed, the second item Producer's Pride Scratch Grains 50 lb (`2525064`) $12.69 (0.25 a lb). A wrong numeric category id is a charged `404`; an unknown path can answer `502` (not charged).
- `/brand` `{"brand": "Producer's Pride", "store": "1933"}`: 189 products, 8 pages, the first two the 16% Layer Pellets and the 16% Layer Crumbles 50 lb (`2340148`), both $14.49.
- `/deals` `{"type": "sale", "store": "1933"}`: `total` 37,533 products on sale for that store, each with `was_price` and `discount_percent` where one price applies and `savings_up_to` otherwise; `type` `new` lists the new arrivals.
- `/promotions` `{"item_number": "3609112"}`: 2 promotions, "Bulk Discount buy 400 get 5% off each" (`starts` 2025-10-08, `ends` null) and a free standard delivery offer (`kind` "shipping"). Ended promotions are left out; quote `name` and the dates as given.
- `/stores` `{"zip": "59301", "limit": 3}`: 1933 Glendive, MT at 68.8 miles (zone 81), 1796 Sidney, MT at 120.1 (zone 83) and 1916 Sheridan, WY at 125.1 (zone 87), each with address, phone, seven `hours` rows, `services` (such as TRAILER RENTAL and PROPANE TANK REFILL) and dated `events`; `services_nearby` lists the services across them (TSC SUBSCRIPTION PICKUP, TRAILER RENTAL, PROPANE TANK REFILL, FUSION STORE).
- `/store` `{"store": "1933"}`: GLENDIVE MT, 2808 West Towne ST, Glendive, MT 59330, phone 406-365-9665, `zone` "81", seven `hours` rows (Thursday read closed on 2026-11-24, Friday 06:00 AM to 09:00 PM), 3 `services` and 4 `events` such as "Santa Pet Photos Event" on 2026-12-19, 9:00am to 4:00pm. No staff names.
- `/categories`: 23 departments (Christmas, Pet, Lawn & Garden, Livestock, Poultry, Horse, Farm & Ranch, Heating & Cooling, Pet & Animal Pharmacy, ...), each {`tree_id`, `name`, `url`, `children`}; send a `tree_id` as `parent_id` for its categories and a `url` as `category` for its products.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def tsc(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/tractorsupply/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. One 50 lb bag priced at three stores in one call (1 credit per 5 lookups)
sp = tsc("store-prices", {"item_number": "2340147", "stores": ["1933", "1923", "1600"]})["data"]
for s in sp["stores"]:
    if s["price"] is None:
        print(s["store_id"], "no price shown")
        continue
    print(s["store_id"], s["city"], s["state"], "zone", s["zone"], s["price"], "per lb", round(s["price"] / 50, 2))
print("low", sp["price_range"]["min"], "high", sp["price_range"]["max"])

# 2. Units on hand at the 5 stores nearest a ZIP (1 credit)
stock = tsc("store-stock", {"item_number": "2340147", "zip": "59301", "limit": 5})["data"]
for s in stock["stores"]:
    print(s["store_id"], s["city"], s["units"], s["status"], s["in_transit"])

# 3. Layer feeds at one store with Tractor Supply's own unit price (1 credit)
res = tsc("search", {"query": "layer pellets", "store": "1933"})["data"]
for it in res["items"]:
    up = it["unit_price"]
    print(it["item_number"], it["name"], it["price"], f"{up['amount']}/{up['unit']}" if up else "")

# Prices are for the store in priced_for and can change between calls. Store each
# answer with fetched_at and the store and run this on a schedule: that stored
# series is your price history (Tractor Supply shows only the current price).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `country` (`us`) and `currency` (`USD`).

- **item** (search, category, brand, deals) - `position`, `item_number` (the input of product, store-prices, store-stock, fulfillment, promotions), `part_number`, `name`, `brand`, `url`, `image`, `price`, `price_min`, `price_max`, `was_price`, `on_sale`, `clearance`, `discount_percent`, `savings_up_to` {`amount`, `percent`}, `currency`, `unit_price` {`amount`, `unit`}, `badge`, `rating`, `review_count`, `availability` (Online In Stores, Online Only, In Stores Only), `pickup`, `standard_delivery`, `same_day_delivery`, `vendor_part_number`, `variant_count`, `item_numbers`.
- **lists** - `store_requested`, `zip_requested`, `priced_for`, `total`, `page`, `page_size`, `total_pages`, `count`, `sort`, `brand`, `on_sale`, `new`, `pickup`, `rating`, `filters`, `corrected_query`, `relaxed_query`, `breadcrumbs[]` {`name`, `category_id`}, `items[]`, `facets[]` {`name`, `id`, `values[]` {`label`, `count`, `filter` (send it in `filters`)}}, `notes`. Search adds `query`, `redirected_to` {`type`, `url`, `category_id`} or `null`, `category_id`; category `category`, `category_id`; brand `query`; deals `type`, `query`.
- **product** - `store_requested`, `zip_requested`, `priced_for` {`store_id`, `zone`, `city`, `state`, `from`, `zip`}, `item_number`, `part_number`, `type` (`item`: one size; `product`: every size), `name`, `brand`, `url`, `image`, `price`, `price_max`, `was_price`, `was_price_max`, `pickup_price`, `price_type`, `on_sale`, `discount_percent`, `savings_up_to`, `mapp` {`type`, `min`, `max`}, `rating`, `review_count`, `availability`, `upc`, `vendor_part_number`, `buyable`, `description`, `specifications[]` {`name`, `value`}, `options[]` {`name`, `value`}, `variants[]` {`item_number`, `name`, `vendor_part_number`, `buyable`}, `parent` {`part_number`, `url`}, `breadcrumbs[]` {`name`, `url`, `category_id`}, `fulfillment` {`store_pickup`, `standard_delivery`, `same_day_delivery`, `truck_delivery`, `shipping_restricted_states`}, `hazmat`, `country_of_origin`, `attachments`, `promotions[]`, `notes`.
- **store-prices** - `item_number`, `name`, `url`, `zip_requested`, `count`, `priced_count`, `price_range` {`min`, `max`}, `stores[]` {`store_id`, `name`, `city`, `state`, `zone`, `distance_miles`, `unknown_store`, `price`, `price_max`, `was_price`, `pickup_price`, `price_type`, `on_sale`, `discount_percent`, `mapp`}, `failed_stores`, `notes`.
- **store-stock** - `item_number`, `zip_requested`, `count`, `in_stock_count`, `total_units`, `in_transit_units`, `stores[]` {`store_id`, `name`, `city`, `state`, `distance_miles` (with zip), `units`, `status`, `in_stock`, `in_transit[]` {`units`, `pickup_date`, `source`}}, `unknown_stores`, `failed_stores`, `not_reported`, `notes`.
- **fulfillment** - `item_number`, `store_id`, `store` {`name`, `city`, `state`}, `zip`, `quantity`, `pickup` {`units`, `status`, `in_transit`}, `delivery_options[]` {`type` (`standard_delivery`, `same_day_delivery`, `ship_to_store`), `name`, `delivery_date`, `order_by`, `order_by_local`, `time_zone`}, `same_day_delivery`, `ship_to_store`, `standard_delivery`, `notes`.
- **promotions** - `item_number`, `name`, `url`, `count`, `promotions[]` {`name`, `description`, `type`, `kind` (`product`, `shipping`), `site_wide`, `starts`, `ends` (`null`: open-ended)}, `notes`.
- **stores** - `zip`, `count`, `stores[]` {`position`, `store_id`, `name`, `address` {`line1`, `city`, `state`, `zip`}, `phone`, `latitude`, `longitude`, `distance_miles`, `time_zone`, `zone`, `hours[]` {`day`, `open`, `close`, `closed`}, `hours_text`, `services`, `store_pickup`, `aisle_locations`, `events[]` {`title`, `starts`, `ends`, `start_time`, `end_time`}}, `services_nearby`, `notes`.
- **store** - `store_id`, `name`, `address`, `phone`, `latitude`, `longitude`, `zone`, `store_pickup`, `time_zone`, `hours`, `hours_text`, `services`, `aisle_locations`, `events`, `notes`.
- **categories** - `parent_id`, `count`, `node_count`, `categories[]` {`tree_id` (the input of `parent_id`), `name`, `url` (the input of category), `children[]`}, `notes`.

## Guardrails

- Name it "Tractor Supply (tractorsupply.com, the US rural lifestyle retailer)" on first mention. Petsense, Allivet, VIP Petcare and Tractor Supply accounts are not read.
- Store prices: quote `price` with the `priced_for` store, its `zone` and the `fetched_at` date. Never call a price national or "Tractor Supply's price" without the store; never carry one store's price to another. Report the differences between stores as numbers; the only explanation to quote is Tractor Supply's own terms wording ("prices may vary ... due to varying conditions in different geographic markets and areas"), never a reason of your own.
- `mapp`, `was_price` and `savings_up_to` are as Tractor Supply gives them. Report them next to the store's price without judging them.
- Per pound: show the price, the bag weight as stated and the division. Never infer a weight the name or `options` do not state.
- Comparing Tractor Supply with Walmart, Chewy, PetSmart or Ace: compare only the same item (same brand, formula and bag size, or UPC), each with its store or ZIP and date. Tractor Supply's own brands (Producer's Pride, DuMOR, Retriever, 4health) have no same item elsewhere: compare them per pound, labelled as different products. Never call one retailer cheaper beyond the numbers shown.
- Stock: `units` as Tractor Supply reported them at the moment of the call; Scavio makes no promise of their accuracy. Never promise pickup or a delivery date.
- Reviews: `rating` and `review_count` only. No review text or reviewer details are returned.
- Not available: review and Q&A text, search suggestions, the weekly ad or digital flyer, a clearance list (deals has `sale` and `new` only), a price-range facet, price history (poll and store), Neighbor's Club member prices, Smart Supply subscription prices, live chick availability, Petsense, checkout, cart or ordering. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not collect or store Tractor Supply data: each call fetches the public Tractor Supply page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Tractor Supply's terms of use cover how its site may be used (they license personal, non-commercial use); read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Tractor Supply product photos or logos; link products by `url` instead.
- Never fabricate prices, units, store numbers, zones, hours, dates, promotions or ratings. Only return what the API returned, with the `fetched_at` time, the `priced_for` store and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` other than `us`; no `store` or `zip` on search, category, brand, deals or product, or both; a store number that is not 1-5 digits; a ZIP that is not a 5-digit US ZIP; an `item_number` that is not a Tractor Supply item number or a `url` that is not a tractorsupply.com product link; both or neither of `item_number` / `url` on product; neither `stores`, `store` nor `zip` on store prices or store stock, both `stores` and `zip`, or more than 25 `stores`; a `limit` outside 1-10; a `page_size` outside 24, 48, 96, 200 or a `page` outside 1-100; an unknown `sort` or deals `type`; a `rating` outside 1-4; more than 6 filters in all, a filter that is not a `facets[].values[].filter`, the price-range facet, or filters Tractor Supply does not accept; a `parent_id` that is not a tree id; a `quantity` outside 1-999.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Tractor Supply does not list item <number>.", "Tractor Supply does not list this product.", "Tractor Supply has no store <number>.", "Tractor Supply has none of the stores <numbers>.", "Tractor Supply lists no store near ZIP <zip>.", "Tractor Supply has no stock record for item <number> (send the 7-digit item number, items[].item_number).", "Tractor Supply has no category at this path.", "Tractor Supply has no category tree id <id>.", "Tractor Supply lists no promotions for this item.", "Nothing was found on Tractor Supply for this request.". Take store numbers, item numbers, links and filters from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api).
- `502` means Tractor Supply data was temporarily unavailable ("Tractor Supply is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Tractor Supply is busy ("Tractor Supply is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.80.0
npm install scavio@0.81.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: atStore } = await scavio.tractorsupply.product({ item_number: "2340147", store: "1933" });
const { data: prices } = await scavio.tractorsupply.storePrices({ item_number: "2340147", stores: ["1933", "1923", "1600"] });
const { data: stock } = await scavio.tractorsupply.storeStock({ item_number: "2340147", zip: "59301", limit: 5 });
const { data: ship } = await scavio.tractorsupply.fulfillment({ item_number: "2340147", store: "1933", zip: "59330" });
const { data: results } = await scavio.tractorsupply.search({ query: "layer pellets", store: "1933" });
const { data: feed } = await scavio.tractorsupply.category({ category: "/tsc/catalog/poultry-feed", store: "1933" });
const { data: brand } = await scavio.tractorsupply.brand({ brand: "Producer's Pride", store: "1933" });
const { data: deals } = await scavio.tractorsupply.deals({ type: "sale", store: "1933" });
const { data: promos } = await scavio.tractorsupply.promotions({ item_number: "3609112" });
const { data: near } = await scavio.tractorsupply.stores({ zip: "59301", limit: 3 });
const { data: store } = await scavio.tractorsupply.store({ store: "1933" });
const { data: tree } = await scavio.tractorsupply.categories();
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.tractorsupply.search(...)`, `product`, `store_prices`, `store_stock`, `fulfillment`, `stores`, `store`, `category`, `categories`, `brand`, `deals` and `promotions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 12 endpoints as tools: `search_tractorsupply`, `get_tractorsupply_product`, `get_tractorsupply_store_prices`, `get_tractorsupply_store_stock`, `get_tractorsupply_fulfillment`, `get_tractorsupply_stores`, `get_tractorsupply_store`, `get_tractorsupply_category`, `get_tractorsupply_categories`, `get_tractorsupply_brand`, `get_tractorsupply_deals` and `get_tractorsupply_promotions`. Tractor Supply is opt-in: add `tractorsupply` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.80.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,tractorsupply"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/tractorsupply-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api), [product](https://scavio.dev/docs/tractorsupply-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api), [store prices](https://scavio.dev/docs/tractorsupply-store-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api), [store stock](https://scavio.dev/docs/tractorsupply-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api), [fulfillment](https://scavio.dev/docs/tractorsupply-fulfillment?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api), [stores](https://scavio.dev/docs/tractorsupply-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api), [store](https://scavio.dev/docs/tractorsupply-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api), [category](https://scavio.dev/docs/tractorsupply-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api), [categories](https://scavio.dev/docs/tractorsupply-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api), [brand](https://scavio.dev/docs/tractorsupply-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api), [deals](https://scavio.dev/docs/tractorsupply-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api), [promotions](https://scavio.dev/docs/tractorsupply-promotions?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api). Overview: [Tractor Supply API](https://scavio.dev/tractorsupply-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api).
