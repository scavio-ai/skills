---
name: ace-hardware-prices-api
description: Ace Hardware API for Ace Hardware (acehardware.com, the US hardware cooperative) - Ace Hardware prices by store, one item priced for the Ace store you pick by its 5-digit store number (Ace stores are independently owned and operated, and the same item can be priced differently at different stores; priced_for names the store and the price list Ace used, the same 40 lb Ace ice melt read $35.99, $21.99 and $18.99 at three stores on one day), the exact units on hand at up to 25 Ace stores or at one store and the 25 stores Ace lists as nearest to it, with the store's shelf location code and the regional distribution centre's units, and a store's weekly ad with its valid dates, items and prices in the ad's words; keyword, item-number and UPC search, category, brand and deals lists, 15 to 200 per page, sorted by price, name or newest and filtered by brand, Ace's Special Offers (sale, Ace Rewards, Buy & Get, Buy More & Save) or any facet, priced as Ace lists them (not a store's price); one product in full with UPC, manufacturer part number, rating and review count, specifications, measurements and assembly options; one store with hours, services, departments, brands, programs, pickup, curbside, delivery and propane flags, price zones and its nearest and same-owner stores; the 25 stores nearest a store with addresses, hours and distance; Ace's departments and categories, the brand index (about 5,700 brands), site-wide promotions with codes and dates, and about 5,300 paint colours (Benjamin Moore, Clark+Kensington, Magnolia Home) with hex and RGB. 11 endpoints, 1 credit per call, search and product 2, store-stock 1 per 5 stores (nearby 6). US only. No ZIP store search, review text, price history, Ace Rewards member prices or checkout.
version: 1.0.0
tags: ace-hardware, acehardware, acehardware-com, ace-hardware-api, ace-hardware-prices, ace-hardware-prices-by-store, ace-hardware-price-by-store, ace-hardware-local-price, ace-hardware-inventory, ace-hardware-inventory-checker, ace-hardware-stock-checker, ace-hardware-store-inventory, ace-hardware-weekly-ad, ace-hardware-local-ad, ace-hardware-black-friday, ace-hardware-deals, ace-hardware-stores, ace-hardware-paint-colors, ace-vs-home-depot, hardware-store, hardware-store-prices, hardware-price-api, home-improvement, store-prices, store-inventory, store-stock, weekly-ad, paint-colors, benjamin-moore, us-retail, price-monitoring, usd, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/acehardware-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api
---

# Ace Hardware Prices API - Price by Store, Inventory, Weekly Ad

Read Ace Hardware (acehardware.com, the US hardware cooperative): one product priced for the Ace store you pick, exact units on hand at a store and its 25 nearest, a store's weekly ad, keyword and item-number search, category, brand and deals lists, one store's details, the stores nearest a store, the category tree, the brand index and Ace's paint colours. All 11 endpoints return structured JSON at 1 credit per call (2 for search and product, and store stock by the number of stores, listed below).

**The job this skill is for: Ace Hardware prices by store.** Ace stores are independently owned and operated, and the same item can be priced differently at different stores, and Ace's own terms say product availability and pricing "vary and are determined by your location". `/product` with a `store` returns the price as Ace shows it for that store. On 2026-11-23 the Ace pet friendly ice melt 40 lb (item `72779`) read $35.99 at store 10665 (New York), $21.99 at store 18250 (Chicago) and $18.99 at store 03085 (Kalona, IA); item `7109754` read $46.99 at 10665 and $25.99 at 03085. Then `/store-stock` gives the units on hand at that store and its 25 nearest, and `/weekly-ad` that store's circular. Pair it with `home-depot-product-data` and `lowes-product-data` for a local hardware price comparison on the same item (same brand and model).

Nine limits shape every answer, so say them plainly:
- **1 credit per call; search and product 2; store stock by stores.** Search is 2 (3 when Ace sends the keywords to a category page and the list options are applied to it again). Product is 2, with or without `store`. Store stock is 1 per 5 stores (1 store 1, 5 stores 1, 25 stores 5, `nearby` = the store and its 25 nearest = 6). Stores is 1, with `details` 1 per 5 lookups (the store plus one per store listed: 25 stores 6). Everything else is 1. An occasional call is billed 2 instead of 1 when Ace is slow to answer: `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Every store price needs a 5-digit Ace store number.** There is no ZIP, city or address store search on Ace. The number is on every Ace store page (`acehardware.com/store-details/<number>`); `/stores` then lists the 25 Ace stores nearest a known store. Leading zeros count: `03085` (a shorter number is padded, so `3085` is `03085`, and every answer carries 5 digits).
- **Product with `store` is that store's price; read `priced_for`.** `priced_for` {`store_id`, `price_list`} names the store and the price list Ace priced the page from: a store number (`10665`, `18250`) is that store's own list, a code such as `Z08010_A` is a price zone, and `CORP` is Ace's online price (what you get without `store`). If Ace priced the page for another store than the one requested, `priced_for` says so and `notes` explains: compare `priced_for.store_id` with `store_requested` before quoting.
- **Listing prices are not a store's price.** Search, category, brand and deals return the price Ace shows in its listing, with `price_list` per item (usually `CORP`, sometimes a store's list). For a store's price, call `/product` with `store`.
- **Store stock is exact units, and 0 can mean unknown.** `/store-stock` returns `units_in_stock`, `soft_units`, `in_stock`, the store's `location_code` and the regional `distribution_center` {`id`, `units`} per store. Ace answers 0 for a store number or product it does not know exactly as for one out of stock, with no not-found: check a store number with `/store` and an item with `/product`.
- **The weekly ad is per store.** `/weekly-ad` reads one store's circular with `valid_from`, `valid_to`, `title` and the items with `price_text` as the ad prints it. Stores read different ads: store 18250 read 7 pages, 10665 and 03085 6, all "Black Friday" valid 2026-11-01 to 2026-11-30.
- **`msrp` is as Ace gives it.** It can sit below a store's price (72779 at 10665: $35.99 with `msrp` $19.99) or above it. Report both numbers as Ace gives them, without judging the gap.
- **Ratings, not reviews.** Items and products carry `rating` and `review_count`. No review text, Q&A or reviewer details.
- **US only, no price history.** `country` is `us` (default); anything else is a `400`, not charged. Ace's stores abroad are run by other companies and are not read. Nothing is cached or kept: poll and store your own series.

Ace Hardware has no public developer API. Publishers can join its affiliate programme on Impact for links and banners, suppliers work through Ace's vendor programme and EDI, and store prices, stock and local ads are shown on acehardware.com for the store you pick; this skill reads those public pages with one Scavio key.

Ace Hardware is a retailer-owned cooperative: 5,307 Ace stores in the US at the end of its third quarter of 2026 (Q3 2026 release, Nov 11, 2026, revenue $2.5 billion for the quarter) and $10.0 billion in revenue for fiscal 2025 (release Feb 18, 2026). Quote these with their source, never from the samples.

See also: for the same item at Home Depot use `home-depot-product-data`; at Lowe's `lowes-product-data`; Menards prices, rebates and store stock `menards-product-data`; Harbor Freight tools and coupons `harbor-freight-api`; prices across retailers `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Check an Ace Hardware item's price at a given Ace store, or compare one item's price across several Ace stores
- Check how many units an Ace store has on hand (and where in the store), or which of the 25 nearest Ace stores have it
- Read an Ace store's weekly ad or local ad (Black Friday ad, valid dates, items and prices)
- Search acehardware.com by keyword, Ace item number or UPC, sorted by price or filtered by brand or Ace's Special Offers
- List an Ace category, a brand's products, or Ace's sales and specials with the current promo codes
- Read one Ace product in full: UPC, manufacturer part number, specifications, measurements, rating and review count
- Look up an Ace store's hours, services, pickup, delivery and propane, or the Ace stores nearest it
- Find a Benjamin Moore, Clark+Kensington or Magnolia Home paint colour at Ace with its hex and RGB
- Compare one item at Ace, Home Depot and Lowe's (with `home-depot-product-data` and `lowes-product-data`)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 1 credit; search and product cost 2, and store stock 1 per 5 stores (a store and its 25 nearest 6).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, store stock took 1-8 seconds (a store and its 25 nearest about 23), store and stores 2-9, product 5-12, search 4-16, and some category, brand and category-tree calls up to 50. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/acehardware/product` | One product by item number or link: price, list price, sale, msrp, UPC, specifications, measurements, rating, review count, options; with `store`, the price as Ace shows it for that store (`priced_for`) | 2 |
| `POST /api/v1/acehardware/store-stock` | Units on hand for one product at 1-25 stores, or at one store and its 25 nearest (`nearby`), with shelf location and distribution centre units | 1 per 5 stores; nearby 6 |
| `POST /api/v1/acehardware/weekly-ad` | One store's weekly ad page by page: title, valid dates, items with price text and item numbers | 1 |
| `POST /api/v1/acehardware/search` | Keywords, an Ace item number or a UPC: 15-200 per page with total, facets and subcategories; `redirected_to` when Ace sends it to a category or a product | 2 (3 when a category redirect is read again with the list options) |
| `POST /api/v1/acehardware/category` | One category's products by link, path or id, sorted, filtered and paged | 1 |
| `POST /api/v1/acehardware/brand` | One brand's products by slug or link; without `brand`, Ace's brand index (about 5,700 brands, 500 a page) | 1 |
| `POST /api/v1/acehardware/deals` | Ace's sales and specials list plus the site-wide promotions with codes and dates | 1 |
| `POST /api/v1/acehardware/store` | One store: address, phone, hours, services, departments, brands, programs, features, price zones, nearest and same-owner stores | 1 |
| `POST /api/v1/acehardware/stores` | Up to 25 stores Ace lists as nearest a store; with `details`, each one's name, address, phone, hours, services and distance | 1; with details 1 per 5 lookups (25 stores 6) |
| `POST /api/v1/acehardware/categories` | Ace's departments and their categories (two levels), or one department's | 1 |
| `POST /api/v1/acehardware/paint-colors` | Ace's paint colours (about 5,300) by name or code, family, brand or collection, with hex and RGB | 1 |

All 11 endpoints serve `country` `us` only (acehardware.com, English, USD).

## Prices: store price, listing price, price list

Every priced item (search, category, brand, deals, product) carries:

| Field | Meaning |
|---|---|
| `price` | What Ace charges now: the sale price when on sale |
| `original_price` | The list price when on sale; `null` otherwise |
| `list_price`, `sale_price`, `on_sale` | The list price and the sale, as Ace gives them |
| `discount_percent` | Computed by Scavio from `list_price` when on sale; `null` otherwise |
| `msrp` | The manufacturer's suggested price as Ace gives it (can be below or above `price`) |
| `price_list` | The price list Ace priced it from: `CORP` is Ace's online price, a store number is that store's list, a code such as `Z08010_A` a price zone |
| `special_offers` | Ace's Special Offers labels: "Sale", "Ace Rewards", "Buy & Get", "Buy More & Save" |
| `in_store_promo` | {`start`, `end`} of an in-store promotion as Ace dates it, or `null` |
| `fulfillment` | {`ship_to_home`, `store_pickup`, `delivery`} as Ace flags them |

- **Store price:** `/product` with `store`. Captured 2026-11-23 for item `72779` (Ace ice melt 40 lb, `msrp` $19.99): store 10665 $35.99 (`price_list` `10665`), store 18250 $21.99 (`18250`), store 03085 $18.99 (`Z08010_A`, a price zone). Item `7109754`: 10665 $46.99, 03085 $25.99 (`msrp` $29.99). Report "$21.99 at Ace store 18250 (Chicago) on 2026-11-23", never "Ace's price".
- **Listing price:** search, category, brand and deals give the price Ace shows in its listing. It is not a store's price, even when an item's `price_list` names one; quote it as "Ace's listed price online" with `price_list`.
- **Ace Rewards** is a label on items in Ace's member offers (`offer` `ace_rewards`). Member-only prices are not read: every price is the guest price.
- Price differences between stores: describe them from the two answers (store, `price_list`, number, date), never why a store prices as it does.

## Workflow

1. **Get a store number.** From the user (it is on their store's page, `acehardware.com/store-details/<number>`), or from `/stores` around a store you know. Confirm it with `/store` (1 credit): an unknown number is a charged `404`.
2. **Find the item.** `/search` with keywords, an Ace item number or a UPC; each item's `product_code` is the input of product and store stock. An item number or UPC usually answers one item with `redirected_to` {`type` `product`}.
3. **Price it at the store.** `/product` with `product_code` and `store` (2 credits). Quote `price` with `priced_for`; check `priced_for.store_id` equals `store_requested`.
4. **Compare stores.** Repeat step 3 per store (2 credits each). Compare only answers for the same `product_code` on the same day.
5. **Units on hand.** `/store-stock` with `product_code` and `stores` (up to 25, 1 credit per 5) or one `store` with `nearby: true` (that store and the 25 Ace lists as nearest, 6 credits). Remember 0 can mean an unknown store or item.
6. **The store's ad.** `/weekly-ad` with `store`: page 1 gives `total_pages` and `ad_group`; send `ad_group` with `page` for the later pages. `item_numbers` on a tile are the Ace item numbers to send to `/product`.
7. **Narrow a list.** `brand` (a brand slug such as `dewalt`), `offer` (`sale`, `ace_rewards`, `buy_and_get`, `buy_more_save`) or `on_sale`, up to 6 facet `filters` in all (`facets[].values[].filter`, e.g. `"price:[100 TO 250]"`), `sort`, `page_size` (15, 30, 50, 100, 200) and `page`.
8. **Watching prices:** there is no history. Poll the same items at the same stores on a schedule and store each answer with its `fetched_at` and `priced_for`; that stored series is the history. Compare only answers priced for the same store.

## Parameters

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_code` | string or integer | one of | An Ace item number (`items[].product_code`: `72779`) |
| `url` | string | one of | An acehardware.com product link (`items[].url`). Send `product_code` or `url`, not both |
| `store` | string or integer | none | An Ace store number (`10665`, `03085`): the price as Ace shows it for that store. Without it, `priced_for` names the price list Ace used (`CORP`) |
| `country` | string | `us` | `us` only |

### Store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_code` | string or integer | required | An Ace item number or product link |
| `store` | string or integer | one of | One Ace store number |
| `stores` | array | one of | 1-25 Ace store numbers (`["18250", "17309"]`). Send `store` or `stores`, not both |
| `nearby` | boolean | `false` | With one `store`: also the 25 stores Ace lists as nearest to it (6 credits) |

### Search (`/search`), category (`/category`), brand (`/brand`), deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Keywords, an Ace item number or a UPC; 1-200 chars. On `/brand` without `brand`: brands whose name contains it |
| `category` | string or integer | category: required | A category link or path (`/departments/tools/power-tools/cordless-drills`, `/c/<id>`) or a category id (`categories[].url`); a wrong path is a charged `404` |
| `brand` | string | brand: optional | On `/brand`, a brand slug (`weber`) or link (`brands[].url`); without it, the brand index. On search, category and deals, the Brand Name facet value (`dewalt`) |
| `offer` | string | none | `sale`, `ace_rewards`, `buy_and_get`, `buy_more_save` (Ace's Special Offers) |
| `on_sale` | boolean | none | Only items on sale (same as `offer` `sale`) |
| `filters` | array | none | Facet filters from an earlier answer (`facets[].values[].filter`: `"tenant~A00317:lithium-ion"`, `"price:[100 TO 250]"`); at most 6 with `brand` and `offer` |
| `sort` | string | `relevance` | `relevance` (Ace's order), `price_asc`, `price_desc`, `name_asc`, `name_desc`, `newest`, `oldest` |
| `page_size` | integer | 30 | 15, 30, 50, 100 or 200 (brand index: 500) |
| `page` | integer | 1 | 1-200, while the first item stays within 10,000 |
| `country` | string | `us` | `us` only |

### Store (`/store`), stores (`/stores`), weekly ad (`/weekly-ad`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store` | string or integer | required | An Ace store number (`18250`, `03085`) |
| `details` | boolean | `false` | Stores: each nearest store's name, address, phone, hours, services and `distance_miles` (1 lookup per store) |
| `limit` | integer | 25 | Stores: how many of the nearest stores (1-25) |
| `page` | integer | 1 | Weekly ad: the ad page (1-40; `total_pages` says how many) |
| `ad_group` | string | none | Weekly ad: `ad_group` from an earlier answer, for page 2+ in one lookup |

### Categories (`/categories`), paint colors (`/paint-colors`)

`/categories` takes an optional `category` (a department or category link, path or id) for its subcategories; without it, every department. `/paint-colors` takes `query` (name or code contains), `family` (`families[].name`: `Blue`), `brand` (`Benjamin Moore`, `Clark+Kensington`, `Magnolia Home`), `collection`, `page` and `page_size` (1-500, default 100).

## Examples

### One item priced for a store

```bash
curl -X POST https://api.scavio.dev/api/v1/acehardware/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_code": "72779", "store": "10665"}'
```

Captured `data` (2026-11-23, 2 credits; `description`, `features`, `image` and `images` dropped, `specifications` cut to 3):

```json
{
  "country": "us",
  "currency": "USD",
  "store_requested": "10665",
  "priced_for": { "store_id": "10665", "price_list": "10665" },
  "product_code": "72779",
  "name": "Ace Magnesium Chloride/MG-104/Sodium Chloride Pet Friendly Granule Ice Melt 40 lb",
  "brand": "Ace",
  "sub_brand": null,
  "url": "https://www.acehardware.com/p/72779",
  "price": 35.99,
  "original_price": null,
  "list_price": 35.99,
  "sale_price": null,
  "on_sale": false,
  "discount_percent": null,
  "msrp": 19.99,
  "price_list": "10665",
  "displayed_price": 35.99,
  "displayed_was_price": null,
  "promotion_text": null,
  "special_offers": [],
  "in_store_promo": null,
  "upc": "082901727798",
  "mfg_part_number": "666902",
  "rating": 4.5,
  "review_count": 263,
  "short_description": "ICE MELT 40LB BAG ACE",
  "specifications": [
    { "name": "Chemical Composition", "value": "Magnesium Chloride/MG-104/Sodium Chloride" },
    { "name": "Container Size", "value": "40 pound" },
    { "name": "Lowest Effective Temperature", "value": "-10 degree Fahrenheit" }
  ],
  "whats_included": null,
  "country_of_origin": "US",
  "product_type": "Ice Melt",
  "family_code": "F049011",
  "measurements": {
    "height": { "value": 20.5, "unit": "in" },
    "width": { "value": 14.5, "unit": "in" },
    "length": { "value": 5, "unit": "in" },
    "weight": { "value": 40.3, "unit": "lbs" }
  },
  "breadcrumbs": [
    { "name": "Lawn and Garden", "url": "https://www.acehardware.com/departments/lawn-and-garden" },
    { "name": "Snow Removal and Equipment", "url": "https://www.acehardware.com/departments/lawn-and-garden/snow-removal-and-equipment" },
    { "name": "Ice Melt", "url": "https://www.acehardware.com/departments/lawn-and-garden/snow-removal-and-equipment/ice-melt" }
  ],
  "options": [],
  "fulfillment": { "ship_to_home": true, "store_pickup": true, "delivery": true },
  "in_stock_online": null,
  "purchasable": true,
  "notes": ["Ace stores are independently owned and operated, and the same item can be priced differently at different stores: prices are as Ace shows them for the store in priced_for."]
}
```

The same call with `"store": "03085"` (Yotty's Ace Discount, Kalona, IA) answered `priced_for` {`store_id` "03085", `price_list` "Z08010_A"} and `price` 18.99; with `"store": "18250"` (Ace Bridgeport, Chicago) `price_list` "18250" and `price` 21.99. Without `store`, `priced_for` is {`store_id` null, `price_list` "CORP"}: Ace's online price. A recteq Backyard Beast 1200 grill (`8114717`) read online $1,049.99 on sale against $1,199.99 list (`discount_percent` 13, `special_offers` ["Sale"]), with `options` for item assembly and haul away. A product Ace does not list is a charged `404`.

### Units on hand at stores

```bash
curl -X POST https://api.scavio.dev/api/v1/acehardware/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_code": "72779", "stores": ["18250", "17309"]}'
```

Captured `data` (2026-11-23, 1 credit):

```json
{
  "country": "us",
  "currency": "USD",
  "product_code": "72779",
  "store_requested": null,
  "nearby": false,
  "count": 2,
  "in_stock_count": 2,
  "total_units": 147,
  "stores": [
    {
      "store_id": "18250",
      "units_in_stock": 135,
      "soft_units": 135,
      "in_stock": true,
      "location_code": "SLT25",
      "distribution_center": { "id": "IL01", "units": 55161 }
    },
    {
      "store_id": "17309",
      "units_in_stock": 12,
      "soft_units": 12,
      "in_stock": true,
      "location_code": null,
      "distribution_center": { "id": "IL01", "units": 55161 }
    }
  ],
  "failed_stores": [],
  "notes": ["units_in_stock is the exact units on hand as Ace reports them for each store; location_code is the store's own shelf location code; distribution_center is the regional distribution centre's stock as Ace reports it."]
}
```

135 bags at store 18250 and 12 at 17309. `location_code` is the store's own code, not an aisle name: quote it as given. With `{"product_code": "8087286", "store": "18250", "nearby": true}` (6 credits) the answer listed 26 stores (18250 first, then the 25 Ace lists as nearest), 6 of them in stock, 15 units in all. A store Ace did not answer for is listed in `failed_stores` (not charged; retry it) rather than as 0.

### A store's weekly ad

```bash
curl -X POST https://api.scavio.dev/api/v1/acehardware/weekly-ad \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store": "18250"}'
```

Captured `data` (2026-11-23, 1 credit; 3 of 11 items shown, `image` dropped):

```json
{
  "country": "us",
  "currency": "USD",
  "store_id": "18250",
  "title": "Black Friday",
  "valid_from": "2026-11-01",
  "valid_to": "2026-11-30",
  "ad_group": "261101_WCAS",
  "zone": "BASE",
  "page": 1,
  "total_pages": 7,
  "count": 11,
  "items": [
    {
      "item_id": "6077446",
      "heading": "IN-STORE ONLY",
      "title": "Great Stuff Wide Spray Cream Polyurethane Foam Insulating Sealant, 36 Oz.",
      "description": null,
      "price_text": "$39.99",
      "details": "1039070",
      "item_numbers": ["1039070"]
    },
    {
      "item_id": "6077448",
      "heading": "IN-STORE ONLY",
      "title": "Rug Doctor by Bissell",
      "description": null,
      "price_text": "RENTAL-TimeToClean",
      "details": null,
      "item_numbers": []
    },
    {
      "item_id": "6077449",
      "heading": "IN-STORE ONLY",
      "title": "Fresh Wave Odor Removing Spray, 8 Oz. Liquid 1 Pk.",
      "description": "Natural, Lavender, or Lemon Scent",
      "price_text": "25%OFF",
      "details": "Limit 4 1339894, 1797935, 1024830",
      "item_numbers": ["1339894", "1797935", "1024830"]
    }
  ],
  "notes": ["Items are as the store's weekly ad lists them (price_text and details in Ace's words; item_numbers are the Ace item numbers the tile names, the input of product). Some tiles are image-only, with no price text."]
}
```

`price_text` is the ad's own wording ("$39.99", "25%OFF", "RENTAL-TimeToClean"): quote it, never parse a number out of a percentage or a rental tile. Store 10665 read its own Black Friday ad (`ad_group` "261101_ACE_CORP", 6 pages); send `ad_group` with `page` for page 2 onward in one lookup.

### Search, category, brand, deals, store, stores, categories and paint colours

- `/search` `{"query": "brass hose nozzle"}` (2 credits): `total` 59, 30 per page, 2 pages, the first an Ace Adjustable Jet Stream Brass Hose Nozzle (`76943`) at $9.99 (`price_list` "CORP"), `rating` 5 from 345. `{"query": "8087286"}` answered one item with `redirected_to` {`type` "product"}; `{"query": "cordless drill", "brand": "dewalt", "on_sale": true, "page_size": 15}` was sent by Ace to its Cordless Drills category (`redirected_to` {`type` "category"}) and read again with the filters: 11 items, 3 credits.
- `/category` `{"category": "/departments/tools/power-tools/cordless-drills"}`: `total` 176, 19 facets, the first a DeWalt 20V MAX compact drill kit (`2385458`, `DCD771C2`) at $159 on sale against $179 list, `special_offers` ["Ace Rewards", "Sale"]. A department page answers `items` [] with its `subcategories`.
- `/brand` `{"brand": "weber"}`: 540 products and 12 subcategories, the first a Weber Genesis II S-435 at $1,049 against $1,299 list. Without `brand`: 5,699 brands, 500 a page, each {`name`, `url`, `category_id`, `product_count`}.
- `/deals`: Ace's Best Sales and Specials, `total` 3,152, and `promotions` such as "15% off for Ace Rewards Members" (`code` "NOV26", `starts` 2026-11-26T05:00:00Z, `ends` 2026-11-27T04:59:00Z) and "50% OFF Under $30 or $15 OFF $30+ for Ace Rewards Members" (`code` "BF26"). `offer` `ace_rewards` narrowed the list to 401. Quote the promotion's own `details`.
- `/store` `{"store": "18250"}`: Ace Bridgeport, 3145 S Ashland Ave, Chicago, IL 60608, seven `hours` rows (Thursday read closed), 29 `services` (Paint Color Matching, Key Cutting, Propane Refill or Exchange, ...), 10 `departments`, 18 `brands`, `programs` (Ace Rewards, Apple Cash Back Program, Ace Handyman Services), `features` (store pickup, curbside, delivery, assembly, propane, Benjamin Moore, Ace Rewards), `max_delivery_radius_miles` 4, `price_zones` ["Z16006_2"], 25 `nearest_stores` and the `same_owner_stores`. No owner or staff names.
- `/stores` `{"store": "03085", "details": true, "limit": 4}` (1 credit): the 4 Ace stores nearest Yotty's Ace Discount in Kalona, IA, the first Ace-N-More in Washington, IA at 13 miles, each with phone, hours, services and features. Without `details`: up to 25 store numbers in Ace's order (store 10665 listed 10).
- `/categories`: 17 departments, 201 nodes, each {`category_id`, `name`, `url` (the input of category), `product_count`, `children`}.
- `/paint-colors` `{"query": "pink"}`: 142 of 5,342 colours (palette dated 2026-09-15), e.g. Benjamin Moore 001 Pink Powderpuff `#FFD5CB`; `brands` Benjamin Moore 3,787, Clark+Kensington 1,390, Magnolia Home 165. `sample_product_code` is an Ace item number, the input of product.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def ace(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/acehardware/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. One item priced at three Ace stores (2 credits each)
for store in ["10665", "18250", "03085"]:
    p = ace("product", {"product_code": "72779", "store": store})["data"]
    pf = p["priced_for"]
    if pf["store_id"] != p["store_requested"]:
        print("Ace priced store", store, "as", pf["store_id"], p["notes"])
    print(store, p["price"], "price list", pf["price_list"], "msrp", p["msrp"])

# 2. Units on hand at one store and the 25 Ace lists as nearest (6 credits)
stock = ace("store-stock", {"product_code": "72779", "store": "18250", "nearby": True})["data"]
for s in stock["stores"]:
    if s["in_stock"]:
        print(s["store_id"], s["units_in_stock"], "units, location", s["location_code"])
# 0 can also mean Ace does not know the store or the item: check with store / product.

# 3. The store's weekly ad, every page (1 credit a page)
ad = ace("weekly-ad", {"store": "18250"})["data"]
print(ad["title"], ad["valid_from"], "to", ad["valid_to"])
for page in range(2, ad["total_pages"] + 1):
    more = ace("weekly-ad", {"store": "18250", "page": page, "ad_group": ad["ad_group"]})["data"]
    for it in more["items"]:
        print(it["title"], it["price_text"], it["item_numbers"])

# Prices are for the store in priced_for and can change between calls. Store each
# answer with fetched_at and priced_for and run this on a schedule: that stored
# series is your price history (Ace shows only the current price).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `country` (`us`) and `currency` (`USD`).

- **item** (search, category, brand, deals) - `position`, `product_code` (the input of product and store-stock), `name`, `brand`, `url`, `image`, `price`, `original_price`, `list_price`, `sale_price`, `on_sale`, `discount_percent`, `msrp`, `currency`, `price_list`, `upc`, `mfg_part_number`, `rating`, `review_count`, `special_offers`, `in_store_promo` {`start`, `end`}, `fulfillment` {`ship_to_home`, `store_pickup`, `delivery`}, `in_stock_online`, `purchasable`, `product_type`.
- **lists** - `title`, `total` (as Ace reports it), `page`, `page_size`, `total_pages`, `count`, `sort`, `sort_applied`, `brand`, `offer`, `filters`, `applied_filters`, `items[]`, `facets[]` {`name`, `field`, `values[]` {`label`, `count`, `filter` (the value to send in `filters`), `applied`, `children`}}, `subcategories[]` {`category_id`, `name`, `url`, `product_count`}, `notes`. Search adds `query`, `redirected_to` {`type` (`category` or `product`), `url`} or `null`; category `category`, `url`, `category_id`; brand `brand_path`, `url`, `category_id`; deals `url`, `promotions[]` {`slot` (`current` or `next`), `title`, `details`, `code`, `starts`, `ends`}.
- **brand index** - `query`, `total_brands`, `total`, `page`, `page_size` (500), `total_pages`, `count`, `brands[]` {`name`, `url`, `category_id`, `product_count`}, `notes`.
- **product** - `store_requested`, `priced_for` {`store_id`, `price_list`}, `product_code`, `name`, `brand`, `sub_brand`, `url`, the price fields, `displayed_price`, `displayed_was_price` (the page's own price pair), `promotion_text`, `special_offers`, `in_store_promo`, `upc`, `mfg_part_number`, `rating`, `review_count`, `short_description`, `description`, `features`, `specifications[]` {`name`, `value`}, `whats_included`, `country_of_origin`, `product_type`, `family_code`, `measurements` {`height`, `width`, `length`, `weight`: {`value`, `unit`}}, `breadcrumbs[]` {`name`, `url`}, `image`, `images`, `options[]` {`option`, `name`, `product_code`, `price_delta`, `required`} (assembly and haul-away add-ons), `fulfillment`, `in_stock_online`, `purchasable`, `notes`.
- **store-stock** - `product_code`, `store_requested`, `nearby`, `count`, `in_stock_count`, `total_units`, `stores[]` {`store_id`, `units_in_stock`, `soft_units`, `in_stock`, `location_code`, `distribution_center` {`id`, `units`}}, `failed_stores`, `notes`.
- **store** - `store_id`, `name`, `display_name`, `url`, `address` {`line1`, `city`, `state`, `zip`}, `phone`, `latitude`, `longitude`, `time_zone`, `hours[]` {`day`, `open`, `close`, `closed`}, `services`, `departments`, `brands[]` {`name`, `url`}, `programs`, `features` {`store_pickup`, `curbside_pickup`, `delivery`, `third_party_delivery`, `assembly`, `propane`, `benjamin_moore`, `ace_rewards`}, `max_delivery_radius_miles`, `price_zones`, `distribution_centers`, `nearest_stores` (25 store numbers), `same_owner_stores[]` {`store_id`, `name`, `address`}.
- **stores** - `store_id`, `name`, `address`, `latitude`, `longitude`, `distribution_centers`, `details`, `count`, `stores[]` {`position`, `store_id`}; with `details`, each also `name`, `display_name`, `url`, `address`, `phone`, `latitude`, `longitude`, `distance_miles` (computed by Scavio), `hours`, `services`, `features`.
- **weekly-ad** - `store_id`, `title`, `valid_from`, `valid_to`, `ad_group`, `zone`, `page`, `total_pages`, `count`, `items[]` {`item_id`, `heading`, `title`, `description`, `price_text`, `details`, `item_numbers`, `image`}, `notes`.
- **categories** - `root` {`category_id`, `name`, `url`}, `count`, `node_count`, `categories[]` {`category_id`, `name`, `url`, `product_count`, `children[]`}, `notes`.
- **paint-colors** - `palette_date`, `total_colors`, `query`, `family`, `brand`, `collection`, `total`, `page`, `page_size`, `total_pages`, `count`, `colors[]` {`code`, `name`, `brand`, `hex`, `rgb` {`r`, `g`, `b`}, `families`, `collections`, `sample_product_code`}, `families[]` {`name`, `count`}, `brands[]` {`name`, `count`}, `notes`.

## Guardrails

- Name it "Ace Hardware (acehardware.com, the US hardware cooperative)" on first mention. Ace Handyman Services, Ace's stores abroad (run by other companies) and Ace Rewards accounts are not read.
- Store prices: quote `price` with the `priced_for` store, its `price_list` and the `fetched_at` date. Never call a price national or "Ace's price" without the store; never carry one store's price to another. Ace stores are locally owned and Ace's terms say pricing varies by location: report the differences between stores as numbers, never explain why a store prices as it does.
- Listing prices (search, category, brand, deals) are what Ace shows in its listing, not a store's price: say so when you quote one, and use `/product` with `store` for a store.
- `msrp` and `list_price` are as Ace gives them. Report them next to the store's price without judging the gap.
- Comparing Ace with Home Depot or Lowe's: compare only the same item (same brand and model or UPC) on each, each with its store and date. Never call one retailer cheaper beyond the numbers shown.
- Stock: `units_in_stock` as Ace reported it at the moment of the call; Scavio makes no promise of its accuracy. A 0 can mean Ace does not know the store or the item; never report "out of stock" at a store number you have not confirmed.
- Weekly ad: quote `price_text`, `details` and the valid dates in the ad's words; some tiles are image-only.
- Reviews: `rating` and `review_count` only. No review text or reviewer details are returned.
- Not available: ZIP, city or address store search (a store number is needed), review and Q&A text, search suggestions, pickup or delivery dates, price history (poll and store), Ace Rewards member prices, Ace Handyman Services, rentals, Ace stores outside the US, checkout, cart or ordering. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not collect or store Ace data: each call fetches the public Ace page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Ace's terms of use cover how its site may be used (they restrict automated access and commercial use); read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Ace product photos or logos; link products by `url` instead.
- Never fabricate prices, units, store numbers, hours, ad items, promotions, ratings or paint colours. Only return what the API returned, with the `fetched_at` time, the `priced_for` store and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` other than `us`; a store number that is not 1-5 digits; a `product_code` that is not an Ace item number or product link; both or neither of `product_code` / `url` on product; both or neither of `store` / `stores` on store stock, more than 25 `stores`, or `nearby` with more than one store; a `page_size` outside 15, 30, 50, 100, 200; a `page` whose first item is past 10,000; more than 6 filters with `brand` and `offer`, or a filter that is not a `facets[].values[].filter`; `on_sale` with an `offer` other than `sale`; an unknown `sort` or `offer`; an `ad_group` that is not one a weekly-ad answer gave.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Ace Hardware does not list this product.", "Ace Hardware has no store <number>.", "Ace Hardware has no weekly ad for store <number>.", "Ace Hardware has no category at this path.", "Ace Hardware has no brand page at this path.". Take store numbers, item numbers, links and filters from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api).
- `502` means Ace data was temporarily unavailable ("Ace Hardware is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Ace is busy ("Ace Hardware is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.79.0
npm install scavio@0.80.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: atStore } = await scavio.acehardware.product({ product_code: "72779", store: "10665" });
const { data: stock } = await scavio.acehardware.storeStock({ product_code: "72779", stores: ["18250", "17309"] });
const { data: nearby } = await scavio.acehardware.storeStock({ product_code: "8087286", store: "18250", nearby: true });
const { data: ad } = await scavio.acehardware.weeklyAd({ store: "18250" });
const { data: results } = await scavio.acehardware.search({ query: "brass hose nozzle" });
const { data: drills } = await scavio.acehardware.category({ category: "/departments/tools/power-tools/cordless-drills" });
const { data: weber } = await scavio.acehardware.brand({ brand: "weber" });
const { data: deals } = await scavio.acehardware.deals();
const { data: store } = await scavio.acehardware.store({ store: "18250" });
const { data: near } = await scavio.acehardware.stores({ store: "03085", details: true, limit: 4 });
const { data: tree } = await scavio.acehardware.categories();
const { data: pinks } = await scavio.acehardware.paintColors({ query: "pink" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.acehardware.search(...)`, `product`, `store_stock`, `store`, `stores`, `category`, `categories`, `brand`, `deals`, `weekly_ad` and `paint_colors`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `search_acehardware`, `get_acehardware_product`, `get_acehardware_store_stock`, `get_acehardware_store`, `get_acehardware_stores`, `get_acehardware_category`, `get_acehardware_categories`, `get_acehardware_brand`, `get_acehardware_deals`, `get_acehardware_weekly_ad` and `get_acehardware_paint_colors`. Ace Hardware is opt-in: add `acehardware` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.79.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,acehardware"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/acehardware-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api), [product](https://scavio.dev/docs/acehardware-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api), [store stock](https://scavio.dev/docs/acehardware-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api), [store](https://scavio.dev/docs/acehardware-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api), [stores](https://scavio.dev/docs/acehardware-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api), [category](https://scavio.dev/docs/acehardware-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api), [categories](https://scavio.dev/docs/acehardware-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api), [brand](https://scavio.dev/docs/acehardware-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api), [deals](https://scavio.dev/docs/acehardware-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api), [weekly ad](https://scavio.dev/docs/acehardware-weekly-ad?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api), [paint colors](https://scavio.dev/docs/acehardware-paint-colors?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api). Overview: [Ace Hardware API](https://scavio.dev/acehardware-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api).
