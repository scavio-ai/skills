---
name: rona-api
description: RONA API for RONA (rona.ca, the Canadian home improvement retailer - RONA+ and RONA stores, about 425 corporate and affiliated dealer stores per RONA inc.) - RONA store prices in Canadian dollars to set next to Home Depot Canada for the same item (the same grade and length, or the same model) in the same city, at named stores on one date, with units; up to 60 article numbers priced at one RONA store in one call with price, regular price, rebate, on-sale flag, exact store units (null means RONA shows no count, not zero), distribution-centre and parcel units, aisle, UPC and model (lumber and panels can be priced differently by store - a 2-in x 4-in x 8-ft SPF Select board read 4.35 CAD at a Quebec store, 4.22 in Ontario and 4.19 in Alberta on Nov 26, 2026); keyword search, any category and RONA's weekly deals or clearance, 24, 48 or 96 a page with total and pages, six sorts on search and category, RONA's filters (brand, price band, rating, on sale, clearance, Buy in Bulk, in-store or online-only products) with counts, priced at the store_id you send or at the store RONA's site picks for the visit; one product with specifications, UPC, the sale end as RONA shows it ("until Dec 10th, 2026") plus an ISO date when unambiguous, the store's units and aisle, rating and review count; the 403 stores on RONA's store locator filtered by province, city and banner (RONA+ or RONA) or nearest a latitude and longitude; one store with hours, special hours and departments; the units at the RONA stores near a store or point for one article; the department tree. English or French. 9 endpoints, 1-3 credits per call (prices, categories, stores and store 1; search and deals 2, 3 with store_id, search 2 more when RONA redirects the term; category 2-3, or 1 by family_id at a store; product and stock 3). Not available - review text, search suggestions, postal-code store lookup, the flyer, price history, cart or checkout.
version: 1.0.0
tags: rona, rona-ca, rona-api, rona-plus, rona-prices, rona-store-prices, rona-lumber-prices, rona-stock, rona-deals, rona-clearance, rona-stores, rona-product-data, rona-categories, home-depot-canada, canadian-tire, canada, canadian-retail, quebec, french, cad, cad-prices, home-improvement, hardware, lumber-prices, building-materials, store-prices, store-inventory, in-store-stock, aisle-location, price-comparison, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/rona-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api
---

# RONA API - Store Prices, Lumber, Stock, Deals

Read RONA (rona.ca, the Canadian home improvement retailer: RONA+ and RONA stores, about 425 corporate and affiliated dealer stores per RONA inc.): prices and exact units for up to 60 articles at one store, keyword search, any category, the weekly deals and clearance listings, one product in full, the stores on RONA's store locator, one store's hours, the units at the stores near a store for one article, and the department tree. Every answer is what RONA's public pages show a visitor without an account at the moment of the call, in Canadian dollars, in English or French. All 9 endpoints return structured JSON at 1 to 3 credits per call.

**Read-only data.** This skill reads the public pages RONA shows to any visitor and returns them as JSON for analysis. It uses no RONA account, no loyalty login, no cart and no checkout.

**The job this skill is for: RONA store prices next to Home Depot Canada for the same item in the same city.** The same board (the same grade and length) or the same model, at named stores, on one date, with the units each store shows. Captured 2026-11-26 with `/prices` (one call per store, 1 credit each), the same four article numbers at three RONA+ stores:

| Article | RONA+ Brossard Dix/30 (41460, QC) | RONA+ Toronto Stockyards (55130, ON) | RONA+ Calgary NE (62860, AB) |
|---|---|---|---|
| 0971073 2-in x 4-in x 8-ft SPF Select Lumber | 4.35 (units null) | 4.22 (541 units) | 4.19 (938 units) |
| 0938002 Spruce Plywood Sheet 3/8-in x 4-ft x 8-ft | 28.82 (118) | 29.82 (128) | 30.88 (null, "Not available at the selected store") |
| 0938042 7/16-in x 4-ft x 8-ft OSB Panel | 17.33 (111) | 18.11 (88) | 16.33 (378) |
| 00277649 DEWALT DCD793D1 drill/driver kit | 118, regular 219 (28) | 118, regular 219 (12) | 118, regular 219 (21) |

Lumber and panels differed by store; the promoted DEWALT kit had one price at every store sampled. Then read the same item at the nearest Home Depot Canada store with `home-depot-product-data` (`country: "ca"` and a `store_id`). Match on the model number (RONA returns `model` and `upc`; DEWALT DCD793D1 is DCD793D1 at both) or, for lumber, on the grade words and the length in both names. Never pair different grades: an SPF Select board is not a premium stud. Put each price with its retailer, the store's name and number, the units and the date.

Ten limits shape every answer, so say them plainly:
- **Credits depend on the endpoint.** prices, categories, stores and store 1; search and deals 2, or 3 with `store_id`, and search 2 more when RONA sends the term to another page (`redirected_to`); category 2 (3 with `store_id`), or 1 when read by `family_id` at a store; product 3; stock 3. `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **prices is the per-store endpoint.** `/prices` takes 1 to 60 article numbers and a required `store_id` and returns each one's price, regular price, rebate, on-sale flag, exact units, aisle, UPC and model at that store, for 1 credit. It is the cheapest way to compare stores: one call per store, the same list each time.
- **Prices are per store.** Without `store_id`, search, category, deals and product are priced at the store RONA's site picks for the visit (`store.requested` false); with `store_id`, every price and unit count is that store's (`store.requested` true). Always send `store_id` when the store matters, and report the store with every price.
- **units null means unknown, not zero.** `units` is the exact count RONA shows for the store; `null` means RONA shows no count there (RONA can hide a count of 1 or 2). Never report `null` as out of stock or as 0. `dc_units`, `parcel_units` and `parcel_units_on_hand` are RONA's distribution-centre and parcel figures, kept apart from the store's units.
- **Sale end dates as RONA shows them.** On `/product`, `sale_ends_text` is RONA's own wording ("until Dec 10th, 2026") and `sale_ends` the ISO date only when it reads unambiguously, else `null`. Lists (search, category, deals) carry no end date: read it on `/product`. Quote it; never compute when a price will change.
- **Redirects cost more.** RONA sends some search terms to a category or a filtered search; that page is read and `redirected_to` says where, for 2 more credits (in the French capture, `perceuse` went to the cordless drills category).
- **stock can come back empty.** `/stock` lists the RONA stores near a store or a point that RONA shows for one article, with units. RONA offers no such list for some articles (lumber), and the list is occasionally empty for an article that has one: retry once before reporting no stores.
- **No postal-code lookup.** Neither `/stores` nor `/stock` takes a postal code (a `postal_code` is a `400`, not charged). Pass `latitude` and `longitude`, a `city` or a `province`, or a `store_id` from `/stores`.
- **Ratings, not reviews.** `rating` and `review_count` are RONA's; review text is not offered.
- **What is not there.** No review text, no search suggestions, no postal-code store lookup, no printed flyer, no price history (store your own answers with `fetched_at`), no cart or checkout. The in-stock filter is not offered (RONA applies it to the visit's store, not to `store_id`): read each item's `units` with `store_id` instead.

RONA publishes no public API for its catalog, prices or store stock; its supplier portal is for vendors exchanging orders and invoices, not a product data feed. This skill reads RONA's public pages with one Scavio key. Other vendors offer RONA data tools; this skill reads RONA's own public pages.

RONA+ is the banner RONA inc. introduced in 2023 for the Lowe's stores it converted (RONA inc. release, June 22, 2023); RONA+ stores are corporate stores. rona.ca's store locator listed 403 stores on November 26, 2026 (302 shown as RONA, 101 as RONA+); write "about 425 per RONA inc." for the network and "403 in rona.ca's store locator" for what `/stores` returns.

See also: `home-depot-product-data` (Home Depot Canada with `country: "ca"`, per-store prices and exact units), `canadian-tire-api` (Canadian Tire store prices and stock), `walmart-product-data` (Walmart.ca with `domain: "ca"`) and `amazon-product-data` (Amazon.ca with `country: "ca"`). Same item only: match the model number, or the grade and length for lumber, show each price with its retailer, store and date, and flag marketplace sellers on Amazon.ca and Walmart.ca rather than treating them as Amazon or Walmart.

## When to trigger

Use this skill when the user asks to:
- Read RONA prices and exact units at a named RONA or RONA+ store, for one article or up to 60
- Put a RONA store price next to Home Depot Canada (or Canadian Tire) for the same item in the same city
- Compare one RONA article's price across stores or provinces (lumber, plywood, OSB)
- Search RONA or browse a category priced at one store, sorted and filtered by brand, price, rating, on sale or clearance
- List RONA's weekly deals or clearance with sale and regular prices at a store
- Read one RONA product with specifications, UPC, aisle, the sale end date and the store's units
- Find RONA+ and RONA stores by province, city, banner or nearest a point, read one store's hours, or see which nearby stores have an article

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Calls in this skill cost 1 to 3 credits, so 50 credits cover 50 `/prices` calls (up to 60 articles each) or about 16 product calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, prices answered in about 1 second, categories 2, store 3, search 4-10, category 5, stock 6, stores 7, product 9 and deals 13. Allow up to about a minute for an answer, set a client timeout of at least 120 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/rona/prices` | 1-60 articles at one store: price, regular price, rebate, on sale, exact units, DC and parcel units, aisle, UPC, model, availability; `not_found` | 1 |
| `POST /api/v1/rona/search` | Products for keywords: price, regular price, on sale, unit, rating, review count, units; total, pages, sorts, filters, facets with counts on request | 2; 3 with `store_id`; +2 when redirected |
| `POST /api/v1/rona/category` | One category by path with paging, sorts, filters and facets; or by `family_id` at a store | 2; 3 with `store_id`; 1 by `family_id` |
| `POST /api/v1/rona/deals` | RONA's weekly deals or clearance listing, sale and regular prices, paged and filtered (RONA's own order) | 2; 3 with `store_id` |
| `POST /api/v1/rona/product` | One product by article number or link: specifications, UPC, model, images, breadcrumb, rating, review count, price, regular price, rebate, sale end, the store's units and aisle, DC and parcel units, nearby stores | 3 |
| `POST /api/v1/rona/stock` | The RONA stores near a store or a point that have one article, nearest first, with exact units | 3 |
| `POST /api/v1/rona/stores` | The stores on RONA's store locator: banner, format, relationship, address, coordinates, services; filtered or nearest a point | 1 |
| `POST /api/v1/rona/store` | One store: address, phone, coordinates, weekly hours, special hours, departments with their own hours, services | 1 |
| `POST /api/v1/rona/categories` | RONA's department tree with `path` for `/category` | 1 |

## Market

Canada only, CAD: every answer carries `market` {`country` "ca", `currency` "CAD", `language`}. `language` is `en` (default) or `fr` on every endpoint: French names, links and labels, with the same article numbers and CAD prices. There is no `country` input.

## Prices, units and stores

| Field | Meaning |
|---|---|
| `price` | RONA's price at the store, CAD, before tax. `null` on a list when RONA does not price the item at that store |
| `regular_price` | RONA's regular price next to a sale price (equal to `price` when there is no sale) |
| `rebate` | The amount off as RONA gives it (`regular_price` minus `price`), `null` without a sale |
| `on_sale` | Whether RONA marks the item on sale |
| `sale_ends_text`, `sale_ends` (product) | RONA's sale end as shown ("until Dec 10th, 2026") and the ISO date when it reads unambiguously ("2026-12-10"), else `null` |
| `units` | The exact count RONA shows for the store; `null` = RONA shows no count (unknown, not zero) |
| `dc_units`, `parcel_units`, `parcel_units_on_hand` | RONA's distribution-centre and parcel figures as given, not store stock |
| `aisle` | RONA's aisle and section code for the store (`F50D2`), `null` where RONA gives none |
| `sold_at_store` (prices) | `false` when RONA gives no price or stock for the article at that store (not carried there) |
| `store` | {`store_id`, `name`, `requested`}: the store the answer is priced at; `requested` false means RONA's site picked it for the visit |
| `price_shown` | Whether RONA shows a price for the item |

- **Percent off:** compute it from `price` and `regular_price` as shown and label it computed (118 against 219 is 46.1% off, computed).
- **Store choice:** `store_id` is a 5-digit RONA store number from `/stores` (`55130` RONA+ Toronto Stockyards, `41460` RONA+ Brossard Dix/30, `62860` RONA+ Calgary NE). Send it as a string.
- **Article numbers:** `sku` is RONA's Article # and the id everywhere. Send it as a string: leading zeros count (`"00277649"`, `"0971073"`). `item_number` on `/product` differs by language; do not use it as the id.

## Workflow

1. **Pick the stores.** `/stores` with `city` or `province` (and `banner`), or `latitude` and `longitude` for the nearest ones. Note each `store_id`, `name` and `banner`.
2. **Find the articles.** `/search` with `query` and `store_id` (and `include_facets: true` on the first call), or `/category` with `category` set to a `path` from `/categories`. Note each `sku`, `name` and `model`.
3. **Price them per store.** `/prices` with up to 60 `skus` and one `store_id`, once per store (1 credit each). Read `price`, `regular_price`, `on_sale`, `units` (null = unknown) and `aisle`.
4. **Sale end dates.** `/product` with `sku` and `store_id` for each item on sale: `sale_ends_text` as RONA shows it.
5. **Match elsewhere.** `home-depot-product-data` with `country: "ca"` and the nearest Home Depot Canada `store_id`, matched on model number, or on grade and length for lumber. Skip any row that does not match.
6. **Report.** Each price with its retailer, store name and number, CAD, the units, the capture date and "before tax"; a percent off labelled computed; the sale end as RONA shows it.
7. **Which stores have it.** `/stock` with `sku` and `store_id`: the stores nearby with units. If the list is empty, retry once; RONA has no list for some articles (lumber).
8. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Prices (`/prices`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `skus` | list or string | required | 1-60 article numbers, a list or comma-separated (`["0971073", "0938002", "00277649"]`) |
| `store_id` | string | required | A RONA store number (5 digits, from `/stores`) |
| `language` | string | `en` | `en` or `fr` |

### Search (`/search`), category (`/category`) and deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required (search) | Keywords, up to 200 chars |
| `category` | string | one of (category) | A category path from `/categories` (`/en/tools/power-tools-158001/cordless-drills-and-drivers-158003`); its `/en` or `/fr` is the answer's language |
| `family_id` | string | one of (category) | A category answer's `family_id`: with `store_id` and no sort, filters or facets, the category's products at 1 credit (page size 1-100) |
| `type` | string | `weekly` | Deals only: `weekly` (RONA's weekly deals) or `clearance` |
| `page` | integer | 1 | Page number; `total_pages` says how many |
| `page_size` | integer | 48 | 24, 48 or 96 |
| `sort` | string | `relevance` | Search and category: `relevance`, `price_low_to_high`, `price_high_to_low`, `highest_rated`, `newest`, `best_sellers`. Deals have no sort (a sort is a `400`) |
| `filters` | list | none | Up to 10 values from `facets[].values[].value` (`"1000337236"` for $1 - $5, `"promotion"`, `"clearance"`) |
| `on_sale` | boolean | false | Only products on sale |
| `clearance` | boolean | false | Only clearance products |
| `include_facets` | boolean | false | Also return RONA's filters with counts (brand, price range, rating, offers, availability, departments) |
| `store_id` | string | none | Price every item at this store |
| `language` | string | `en` | `en` or `fr` |

### Product (`/product`), stock (`/stock`), stores (`/stores`), store (`/store`), categories (`/categories`)

| Endpoint | Parameters |
|---|---|
| `/product` | `sku` (an article number) or `url` (a rona.ca product link, as `items[].url` gives it), `store_id`, `language` |
| `/stock` | `sku` (required), and `store_id` (the stores near that store) or `latitude` + `longitude`; `language` |
| `/stores` | `province` (code or name: `qc`, `on`, `ab`, `bc` ...), `city` (contains, accents and case ignored), `banner` (`rona` or `rona_plus`), or `latitude` + `longitude` for the nearest; `limit` 1-403 (default 20 near a point, else all); `language` |
| `/store` | `store_id` or `url` (a rona.ca store link, as `stores[].url` gives it); `language` |
| `/categories` | `depth` 1-3 (default 3: departments, categories, sub-categories); `language` |

## Examples

### Prices for four articles at one store

```bash
curl -X POST https://api.scavio.dev/api/v1/rona/prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"skus": ["0971073", "0938002", "0938042", "00277649"], "store_id": "62860"}'
```

Captured `data` (2026-11-26; `items` cut to 2 of 4, `url`, `image` and `notes` dropped):

```json
{
  "store": {"store_id": "62860", "requested": true},
  "language": "en",
  "requested": 4,
  "count": 4,
  "items": [
    {"sku": "0971073", "found": true, "sold_at_store": true, "name": "2-in x 4-in x 8-ft SPF Select Lumber", "brand": null, "model": "034-02013", "upc": "689236240185", "format": "2\"x4\"x8'", "unit": "Each", "price": 4.19, "regular_price": 4.19, "rebate": null, "on_sale": false, "units": 938, "dc_units": null, "parcel_units": null, "parcel_units_on_hand": null, "aisle": null, "availability": "FREE pick-up in store", "price_shown": true, "buyable": true, "rating": 3.1, "review_count": 23},
    {"sku": "00277649", "found": true, "sold_at_store": true, "name": "DEWALT 20 V MAX Brushless Compact Drill/Driver Kit with Battery/Charger", "brand": "DEWALT", "model": "DCD793D1", "upc": "885911904919", "format": "20V 1/2\"", "unit": "Each", "price": 118, "regular_price": 219, "rebate": 101, "on_sale": true, "units": 21, "dc_units": 64, "parcel_units": 349, "parcel_units_on_hand": 54, "aisle": "F50D2", "availability": "FREE pick-up in store", "price_shown": true, "buyable": true, "rating": 4.6, "review_count": 50}
  ],
  "not_found": [],
  "market": {"country": "ca", "currency": "CAD", "language": "en"}
}
```

The same call with `store_id` `41460` (RONA+ Brossard Dix/30, QC) read the 2x4 at 4.35 with `units` null, and with `55130` (RONA+ Toronto Stockyards, ON) at 4.22 with 541 units. At 62860 the plywood sheet 0938002 read 30.88 with `units` null and "Not available at the selected store".

### Search at a store with facets

```bash
curl -X POST https://api.scavio.dev/api/v1/rona/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "2x4", "store_id": "41460", "page_size": 24, "include_facets": true}'
```

Captured `data` (2026-11-26; `items` cut to 2 of 24, `facets` to 1 of 7, `url`, `image` and `notes` dropped):

```json
{
  "query": "2x4",
  "language": "en",
  "redirected_to": null,
  "page": 1,
  "page_size": 24,
  "sort": "relevance",
  "filters_applied": [],
  "total": 2440,
  "total_pages": 102,
  "has_more": true,
  "count": 24,
  "items": [
    {"sku": "0971073", "name": "2-in x 4-in x 8-ft SPF Select Lumber", "brand": null, "model": "034-02013", "price": 4.35, "regular_price": 4.35, "on_sale": false, "unit": "Each", "rating": 3.1, "review_count": 23, "units": null, "availability": "Available for order in store", "price_shown": true},
    {"sku": "84895021", "name": "Pressure Treated Wood Deck Board 2 x 4-in x 8-ft - Brown", "brand": null, "model": "761-62389", "price": 7.39, "regular_price": 7.39, "on_sale": false, "unit": "Each", "rating": 3.1, "review_count": 7, "units": 503, "availability": "FREE pick-up in store", "price_shown": true}
  ],
  "store": {"store_id": "41460", "name": null, "requested": true},
  "facets": [
    {"facet": "offer", "name": "Our special offers", "values": [{"value": "promotion", "name": "On Sale", "count": 180}, {"value": "clearance", "name": "Clearance", "count": 55}, {"value": "1000338402", "name": "Buy in Bulk", "count": 48}, {"value": "1000458176", "name": "Pro Pick", "count": 5}]}
  ],
  "market": {"country": "ca", "currency": "CAD", "language": "en"}
}
```

15 of the 24 items read `units` null at this store: unknown, not zero. The 7 facets were Our special offers, Price Range, Product availability, More ways to shop, Rating, Brand (254 values) and Shop by departments. This call cost 3 credits (`store_id`).

### One product with the sale end

```bash
curl -X POST https://api.scavio.dev/api/v1/rona/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "00277649", "store_id": "55130"}'
```

Captured `data` (2026-11-26; `description`, `bullets`, `specs` (26 rows), `images`, `breadcrumb`, `url` and `notes` dropped):

```json
{
  "sku": "00277649",
  "item_number": "000314341",
  "name": "DEWALT 20 V MAX Brushless Compact Drill/Driver Kit with Battery/Charger",
  "brand": "DEWALT",
  "model": "DCD793D1",
  "upc": "885911904919",
  "format": "20V 1/2\"",
  "unit": "Each",
  "rating": 4.6,
  "review_count": 50,
  "price": 118,
  "regular_price": 219,
  "rebate": 101,
  "on_sale": true,
  "sale_ends_text": "until Dec 10th, 2026",
  "sale_ends": "2026-12-10",
  "price_shown": true,
  "store": {"store_id": "55130", "name": null, "requested": true},
  "units": 12,
  "availability": "FREE pick-up in store",
  "aisle": "F20T1",
  "dc_units": null,
  "parcel_units": 349,
  "parcel_units_on_hand": 54,
  "back_in_stock": null,
  "pickup_message": null,
  "nearby_stores": [],
  "buyable": true,
  "market": {"country": "ca", "currency": "CAD", "language": "en"}
}
```

Quote the end as RONA shows it ("until Dec 10th, 2026"). The aisle is per store: F20T1 at 55130, F50D2 at 62860.

### Stock near a store

```bash
curl -X POST https://api.scavio.dev/api/v1/rona/stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "00277649", "store_id": "62860"}'
```

Captured (2026-11-26): `count` 12, `in_stock_count` 10, nearest first from `center` 62860: RONA+ Calgary NE (32nd St) 21 units at 0 km, RONA+ Sunridge Way NE 6 at 1.11 km, RONA Calgary (Forest Lawn) 9 at 5.21 km, RONA+ Calgary (MacLeod) 25 at 13.34 km ... RONA Black Diamond and RONA OLDS `units` null with "Not in stock in this store". Each row carries `store_id`, `name`, `distance_km`, `address`, `city`, `province`, `postal_code`, `units`, `in_stock`, `stock_message`, `pickup_message`, `latitude`, `longitude`. Prices are not on this list: price the stores with `/prices`.

### Stores, store, category, deals, categories

- `/stores` `{"latitude": 43.6426, "longitude": -79.3871, "limit": 10}`: `total` 403, the 10 nearest, first RONA+ Toronto Stockyards (55130, `banner` RONA+, `format` big_box, `relationship` corporate) at 7.29 km, then RONA+ York 8.78 km and RONA+ Golden Mile 12.07 km; `address`, `postal_code` and `phone` are filled for the stores nearest the point (null for the others: read `/store`).
- `/store` `{"store_id": "55130"}`: RONA+ Toronto Stockyards, 110 West Toronto Street, Toronto, ON M6N 5B7, `hours` Monday-Friday 06:00-21:00, Saturday 07:00-20:00, Sunday 08:00-20:00 (local time), `departments` Garden Center, `relationship` corporate, `services` click_and_collect, installation, truck_delivery, parcel_shipping, appliances all true.
- `/category` `{"category": "/en/tools/power-tools-158001/cordless-drills-and-drivers-158003", "store_id": "55130", "page_size": 24}`: Cordless Drills and Drivers, `category_id` 158003, `family_id` 318485, `source` page, `total` 233 over 10 pages; first a Bosch GDX18V-285B12 at 119 (regular 249, 3 units). The next pages by `family_id` 318485 with `store_id` cost 1 credit each.
- `/deals` `{"type": "weekly", "store_id": "55130", "page_size": 24}`: first the DEWALT 20 V MAX Impact Driver Kit DCF840D1 at 118 (regular 219, 16 units), then the Bosch GDX18V-285B12 at 119 (regular 249, 3 units) and a RONA Gas Snow Blower 24-in at 599 (regular 799, 2 units). End dates are on `/product`.
- `/categories` `{"depth": 2}`: 22 departments (Outdoor, Building Supplies and Materials, Appliances, Bathroom, Hardware, Kitchen, Flooring and Ceramic Tile, Tools ...) and 232 entries in all, each with `path` for `/category`.
- French: `/search` `{"query": "perceuse", "language": "fr", "store_id": "41460", "page_size": 24}` was redirected to the French cordless drills category (`redirected_to` set, 2 more credits), 233 products with French names and the same CAD prices.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def rona(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/rona/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()

# The same four articles at three stores (1 credit per store)
skus = ["0971073", "0938002", "0938042", "00277649"]
for store_id in ["41460", "55130", "62860"]:
    d = rona("prices", {"skus": skus, "store_id": store_id})["data"]
    for i in d["items"]:
        units = "unknown" if i["units"] is None else i["units"]  # null is not zero
        print(store_id, i["sku"], i["name"], i["price"], i["regular_price"], units)

# The sale end as RONA shows it (3 credits)
p = rona("product", {"sku": "00277649", "store_id": "55130"})["data"]
print(p["price"], p["regular_price"], p["sale_ends_text"], p["sale_ends"], p["aisle"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` and `notes`.

- **item** (search, category, deals) - `sku`, `name`, `brand`, `model`, `url`, `image`, `price`, `regular_price`, `on_sale`, `unit`, `rating`, `review_count`, `units`, `availability`, `price_shown`.
- **search** - `query`, `language`, `redirected_to`, `page`, `page_size`, `sort`, `filters_applied`, `total`, `total_pages`, `has_more`, `count`, `items[]`, `store` {`store_id`, `name`, `requested`}, `facets[]` (with `include_facets`: {`facet`, `name`, `values[]` {`value`, `name`, `count`}}).
- **category** - `category` {`path`, `name`, `category_id`, `family_id`, `url`}, `language`, `source` (`page` or `family`), then as search from `page`.
- **deals** - `type`, `language`, then as search from `page`.
- **prices** - `store` {`store_id`, `requested`}, `language`, `requested`, `count`, `items[]` {`sku`, `found`, `sold_at_store`, `name`, `brand`, `model`, `upc`, `format`, `unit`, `price`, `regular_price`, `rebate`, `on_sale`, `units`, `dc_units`, `parcel_units`, `parcel_units_on_hand`, `aisle`, `availability`, `price_shown`, `buyable`, `rating`, `review_count`, `url`, `image`}, `not_found`.
- **product** - `sku`, `item_number`, `name`, `brand`, `model`, `upc`, `format`, `unit`, `url`, `images`, `description`, `bullets`, `specs[]` {`name`, `value`}, `breadcrumb[]` {`name`, `url`}, `rating`, `review_count`, `price`, `regular_price`, `rebate`, `on_sale`, `sale_ends_text`, `sale_ends`, `price_shown`, `store`, `units`, `availability`, `aisle`, `dc_units`, `parcel_units`, `parcel_units_on_hand`, `back_in_stock`, `pickup_message`, `nearby_stores[]` {`store_id`, `name`, `distance_km`, `units`}, `buyable`.
- **stock** - `sku`, `name`, `model`, `center` {`store_id`, `latitude`, `longitude`}, `count`, `in_stock_count`, `stores[]` {`store_id`, `name`, `distance_km`, `address`, `city`, `province`, `postal_code`, `units`, `in_stock`, `stock_message`, `pickup_message`, `latitude`, `longitude`, `url`}.
- **stores** - `language`, `location`, `filters_applied` {`province`, `city`, `banner`}, `total`, `count`, `stores[]` {`store_id`, `name`, `banner` (RONA+ or RONA), `format` (big_box or proximity), `relationship` (corporate, dealer or franchisee, `null` where RONA's store file gives none), `city`, `province`, `address`, `postal_code`, `phone`, `latitude`, `longitude`, `distance_km`, `services`, `url`}.
- **store** - `store_id`, `name`, `banner`, `address` {`street`, `city`, `province`, `postal_code`, `country`}, `phone`, `latitude`, `longitude`, `hours[]` {`day`, `opens`, `closes`}, `special_hours`, `departments[]` {`name`, `hours`}, `url`, `relationship`, `services` {`click_and_collect`, `installation`, `truck_delivery`, `parcel_shipping`, `appliances`}.
- **categories** - `language`, `depth`, `count`, `total`, `departments[]` {`name`, `path`, `url`, `category_id`, `children[]`}.

## Guardrails

- Name it "RONA (rona.ca, the Canadian home improvement retailer: RONA+ and RONA stores, about 425 corporate and affiliated dealer stores per RONA inc.)" on first mention, "RONA" after that.
- Prices: quote each with CAD, the store's name and number, the `fetched_at` date and "before tax" ("listed on rona.ca for RONA+ Toronto Stockyards (55130) on Nov 26, 2026, before tax"). Prices can differ by store and province; never present one store's price as RONA's price everywhere.
- Units: report `units` with the store it belongs to; `null` is unknown, never 0 or out of stock.
- Comparisons: the same model number, or the same grade and length for lumber, at named stores on one date. Never pair different grades. No price-match advice and no verdict on which retailer is cheaper beyond the numbers shown.
- Store types: RONA+ stores are corporate stores. Report `relationship` as RONA's store file gives it; never call RONA+ stores affiliates.
- Reviews: `rating` and `review_count` only; review text is not offered.
- Descriptive only: no commentary on RONA's business, ownership, pricing practices or policies. Quote RONA inc. figures only with their source and date.
- Do not republish RONA product photos, descriptions or logos. Write rona.ca as plain text and cite product names, article numbers, store numbers and capture dates rather than linking RONA pages.
- Terms: Scavio does not collect or store RONA data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account, no cart and no checkout. RONA's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, regular prices, sale dates, article numbers, stores, units or aisles. Only return what the API returned, with the `fetched_at` time.
- Not available: review text, search suggestions, postal-code store lookup, the printed flyer, price history (store your own), the in-stock filter, cart or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `query`; prices without `skus` or `store_id`, or more than 60 article numbers; an article number sent as a number or not 5-10 digits ("article numbers keep their leading zeros"); a `store_id` that is not a store number; `page_size` other than 24, 48 or 96; more than 10 `filters`, or a value not taken from `facets[].values[].value`; the in-stock filter; a `sort` on deals ("RONA's deals listing has no sort (its own order only): leave sort out."); category without `category` or `family_id`, `family_id` without `store_id`, or sort, filters or facets with `family_id` alone; a `language` that does not match the category path; product without `sku` or `url`, or the two naming different articles; stock without `sku`, or without `store_id` or `latitude` + `longitude`; `latitude` without `longitude`; a `province` that is not a Canadian province; any `postal_code` ("Postal code lookup is not supported; pass latitude and longitude, or a city / province.").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "RONA has no article <sku>.", "RONA has none of these article numbers.", "RONA has no store <id>.", "RONA has no such page.", "RONA has no category family <id>.". Take article numbers, store numbers and paths from a previous answer rather than guessing them. On `/prices`, unknown article numbers among known ones are listed in `not_found` in a `200`. A search with no matches is a `200` with `count` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api).
- `502` means RONA data was temporarily unavailable ("RONA is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("RONA is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- `/stock` with `count` 0 is a `200`: RONA has no nearby-store list for some articles (lumber), and the list is occasionally empty for one that has it. Retry once before reporting no stores.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.94.0
npm install scavio@0.95.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: prices } = await scavio.rona.prices({ skus: ["0971073", "0938002", "00277649"], store_id: "55130" });
const { data: lumber } = await scavio.rona.search({ query: "2x4", store_id: "41460", include_facets: true });
const { data: product } = await scavio.rona.product({ sku: "00277649", store_id: "55130" });
const { data: nearby } = await scavio.rona.stock({ sku: "00277649", store_id: "62860" });
const { data: stores } = await scavio.rona.stores({ city: "Calgary", banner: "rona_plus" });
const { data: deals } = await scavio.rona.deals({ type: "weekly", store_id: "55130" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.rona.search(...)`, `product`, `prices`, `category`, `categories`, `stores`, `store`, `stock` and `deals`, with the same parameter names as keyword arguments. Give the client a timeout of at least 120 seconds for these calls.

## MCP

The Scavio MCP server exposes all 9 endpoints as tools: `search_rona`, `get_rona_product`, `get_rona_prices`, `get_rona_category`, `get_rona_categories`, `get_rona_stores`, `get_rona_store`, `get_rona_stock` and `get_rona_deals`. RONA is opt-in: add `rona` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.94.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,rona"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/rona-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api), [product](https://scavio.dev/docs/rona-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api), [prices](https://scavio.dev/docs/rona-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api), [category](https://scavio.dev/docs/rona-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api), [categories](https://scavio.dev/docs/rona-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api), [stores](https://scavio.dev/docs/rona-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api), [store](https://scavio.dev/docs/rona-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api), [stock](https://scavio.dev/docs/rona-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api), [deals](https://scavio.dev/docs/rona-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api). Overview: [RONA API](https://scavio.dev/rona-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rona-api).
