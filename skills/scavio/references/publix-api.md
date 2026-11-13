# Publix API - Weekly Ad, BOGO Deals, Store Prices, Pub Subs

Read Publix (publix.com) data store by store: the weekly ad with its BOGO list, Extra Savings, digital coupons, product search and category listings, product cards with nutrition facts, the deli and bakery order-ahead menu (Pub Subs, platters, cakes), the category tree, store locations and search suggestions. Publix is the employee-owned Southeast grocer with roughly 1,440 supermarkets in eight states: Florida, Georgia, Alabama, South Carolina, North Carolina, Tennessee, Virginia and Kentucky. All 11 endpoints return structured JSON and cost 1 credit each.

**The one fact to get right: publix.com does not show regular shelf prices.** Publix's own product catalog FAQ says pricing "is only displayed for items currently on sale and those available for purchase through In-Store Pickup". So search, category and product return `price` only when the site shows one (an item on promotion, or an order-ahead deli or bakery item) and `null` otherwise: in the captured "chicken" search at store 1614, 38 of 48 items had `price: null`. Never present a null as zero, and never claim a shelf price for an item that has none. Publix's delivery and curbside shopping runs on a separate Instacart storefront whose pricing policy says those prices "are higher than item prices in physical store locations"; this skill returns publix.com's own store-level promotion and order-ahead prices, not delivery-app prices.

**Prices differ by store.** Every price endpoint takes a `store_id` (a Publix store number from the stores endpoint). Measured 2026-11-13: the Publix Chicken Tender Sub was $12.09 at store 1614 (Miami, FL) and $11.99 at 1825 (Atlanta, GA) and 1453 (Charlotte, NC); the weekly-ad 24-pack of Michelob Ultra was $25.99, $28.49 and $23.49 at the same three stores; across the three weekly ads, 15 of 590 shared items had different prices. Always say which store a price came from.

Publix does not publish a public developer API. Its business-partner pages cover suppliers and real estate, not product or weekly-ad data.

See also: for other US grocery store prices use `kroger-grocery-data`, `heb-grocery-data`, `aldi-grocery-data`, `whole-foods-grocery-data` or `costco-product-data`; for the cross-retailer view use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Get the Publix weekly ad or this week's Publix BOGO (Buy 1 Get 1 Free) list for a store, city or ZIP code
- Compare a Publix deal or a Pub Sub price across stores, or across Florida and Georgia ads
- List Publix Extra Savings or a store's Publix digital coupons
- Find which Publix deals and coupons match a keyword ("coffee", "chicken") at one store
- Search Publix products or browse a Publix category at a store, with aisle, sale price and promotion
- Read the Publix deli and bakery order-ahead menu (Pub Subs, platters, cakes) with the store's prices
- Read nutrition facts for a Publix product or a Pub Sub
- Find Publix stores near a ZIP code or in a city, with hours, services, pharmacy hours and the day the weekly ad starts
- Build a BOGO newsletter, a deal alert or a promotion tracker for Southeast grocery stores

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint here costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Most calls answered in 2 to 17 seconds in testing; a product call took 22 seconds. Allow a client timeout of at least 60 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/publix/stores` | 1 | Stores near a ZIP or in a city + state (up to 30), or one store by `store_id`: address, phone, 7 days of hours, departments, services, pharmacy phone and hours, liquor store, coordinates, distance, `weekly_ad_break_day` |
| `POST /api/v1/publix/weekly-ad` | 1 | The store's current weekly ad (about 700 items) with `ad.start_date` / `ad.end_date`, deal type, sale price, multi-buy, BOGO, valid dates; filter by department, BOGO only or text |
| `POST /api/v1/publix/extra-savings` | 1 | The store's Extra Savings (temporary price reductions, several hundred items) with the reduced `final_price` and the current `period` |
| `POST /api/v1/publix/coupons` | 1 | The store's digital coupons (about 100-130) with value, limits, valid dates and terms. Listed only, never clipped |
| `POST /api/v1/publix/savings-search` | 1 | One keyword across the store's weekly ad, Extra Savings and digital coupons; each item tagged with `saving_type` |
| `POST /api/v1/publix/search` | 1 | Product search at one store, 48 per page, with sorts, on-sale / BOGO / brand filters, aisle, promo and facets |
| `POST /api/v1/publix/category` | 1 | One category's products at one store, by category link or id, in the search shape |
| `POST /api/v1/publix/categories` | 1 | The category tree (16 departments, 382 nodes in the capture) with ids for the category endpoint |
| `POST /api/v1/publix/product` | 1 | One product by Publix item code at one store: the product card plus nutrition facts |
| `POST /api/v1/publix/order-ahead` | 1 | The store's deli and bakery order-ahead menu with its prices: Pub Subs (default) or the whole catalog, 60 per page |
| `POST /api/v1/publix/suggestions` | 1 | Up to 10 search-box suggestions and, with `store_id`, up to 4 products |

## Workflow

1. **Find the store:** `/publix/stores` with the shopper's `zip` (or `city` + `state`). Use `stores[].store_id` as `store_id` everywhere else. Store numbers are 1 to 5 digits (`54`, `1614`); send them as a string or a number.
2. **This week's deals:** `/publix/weekly-ad` with `store_id`; add `bogo_only: true` for the BOGO list, `department` for one department, or `query` for text. Read `ad.start_date` and `ad.end_date`.
3. **More savings:** `/publix/extra-savings` and `/publix/coupons` with the same `store_id`, or `/publix/savings-search` to find one keyword across the weekly ad, Extra Savings and coupons in a single call.
4. **Products:** `/publix/search` with `query`, or `/publix/categories` then `/publix/category` with a `category_id`. Use `on_sale: true` or `bogo: true` to keep only items on promotion, the ones that carry a price (or a multi-buy `bundle`).
5. **One product in full:** `/publix/product` with the `item_code` from search, category, order-ahead, suggestions or a weekly-ad item, plus `store_id`.
6. **Deli and bakery:** `/publix/order-ahead` for Pub Sub prices (`section: "subs"`, the default) or the whole order-ahead catalog (`section: "all"`).
7. **Compare stores:** call the same endpoint once per `store_id` and compare. Name each store (`store.id`, `store.name`) next to its prices.
8. **Monitoring:** poll the weekly ad once per ad cycle per store (it changes on `weekly_ad_break_day`), store the answer with the time, and compare runs yourself. There is no price history.

### Weekly ad cycles by state

Weekly ads start on different days by state. In the 2026-11-13 captures, Florida store 1614 (Miami) ran Thursday 2026-11-12 to Wednesday 2026-11-18, and stores 1825 (Atlanta, GA) and 1453 (Charlotte, NC) ran Wednesday 2026-11-11 to Tuesday 2026-11-17. Do not hard-code a day per state: read `weekly_ad_break_day` from `/publix/stores` (it is `"Thursday"` for every Miami store in the capture) and `ad.start_date` / `ad.end_date` from the weekly ad itself. The ad is the English ad.

### Pagination and sort

- **search and category:** 48 products per page, `page` 1-100; `total`, `total_pages` and `count` describe the result. A page past the last answers an empty list. `sort` is `relevance` (default), `featured`, `name_asc`, `name_desc`, `popularity`, `savings_amount` (biggest promo savings first) or `most_viewed`.
- **order-ahead:** 60 items per page, `page` 1-50. In the capture the Pub Sub section had 66 items over 2 pages.
- **weekly-ad, extra-savings, coupons and savings-search:** one call returns the whole list (691 weekly-ad items and 678 Extra Savings items at store 1614). A full weekly ad is a large answer: filter with `department`, `bogo_only` or `query` when you need part of it.
- **stores:** `limit` 1-30 (default 10), `radius_miles` 1-100 (default 50), no paging.

## Parameters

### Stores (`/stores`)

Send `zip`, or `city` and `state`, or `store_id`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | A 5-digit US ZIP code: the stores nearest to it |
| `city` | string | one of | A city name, with `state` |
| `state` | string | with city | A 2-letter state code (Publix operates in FL, GA, AL, SC, NC, TN, VA and KY) |
| `store_id` | string or integer | one of | One store by number |
| `limit` | integer | 10 | Stores to return, 1-30 |
| `radius_miles` | integer | 50 | Search radius in miles, 1-100 |

### Weekly ad (`/weekly-ad`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string or integer | required | A Publix store number |
| `department` | string | - | Only items of this department (from the answer's `departments`, e.g. `Meat`, `Produce`, `Deli`) |
| `bogo_only` | boolean | false | Only Buy 1 Get 1 Free and Buy 2 Get 1 Free items |
| `query` | string | - | Only items whose title, description or brand contains this text |

### Extra Savings (`/extra-savings`) and Coupons (`/coupons`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string or integer | required | A Publix store number |

### Savings search (`/savings-search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | A keyword to find in the store's weekly ad, Extra Savings and digital coupons (1-100 chars) |
| `store_id` | string or integer | required | A Publix store number |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-100 chars) |
| `store_id` | string or integer | required | A Publix store number |
| `page` | integer | 1 | 1-100, 48 products per page |
| `sort` | string | `relevance` | `relevance`, `featured`, `name_asc`, `name_desc`, `popularity`, `savings_amount` or `most_viewed` |
| `on_sale` | boolean | false | Only items on sale at the store (weekly ad, BOGO, multi-buy or Extra Savings) |
| `bogo` | boolean | false | Only Buy One Get One Free items at the store |
| `brand` | string | - | Only this brand, as the site lists it (the `Brand` facet's values) |

### Category (`/category`)

Send `category_url` or `category_id`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_url` | string | one of | A publix.com category link (`/c/<name>/<id>`) |
| `category_id` | string | one of | A category id (`categories[].id` of the categories endpoint, a 36-character id) |
| `store_id` | string or integer | required | A Publix store number |
| `page`, `sort`, `on_sale`, `bogo`, `brand` | | | As on search |

### Categories (`/categories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `parent_id` | string | - | Return only this department's or category's subtree |
| `store_id` | string or integer | - | Optional |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_code` | string or integer | required | A Publix item code (`items[].item_code` of search, category, order-ahead, suggestions or the weekly ad). Not a UPC |
| `store_id` | string or integer | required | A Publix store number |

### Order ahead (`/order-ahead`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string or integer | required | A Publix store number |
| `section` | string | `subs` | `subs` (the Pub Sub menu) or `all` (the whole deli and bakery order-ahead catalog: subs, platters, cakes, meals) |
| `page` | integer | 1 | 1-50, 60 items per page |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars) |
| `store_id` | string or integer | - | Optional: with a store the answer also carries up to 4 products |

## Examples

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/publix/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "33101"}'
```

Captured `data` (9 of 10 stores trimmed; 5 of 7 days of store and pharmacy hours and the image trimmed):

```json
{
  "zip": "33101",
  "radius_miles": 50,
  "count": 10,
  "stores": [
    {
      "store_id": 1614,
      "name": "3 Miami Central",
      "short_name": "3 MiamiCentral",
      "type": "supermarket",
      "address": { "street": "601 NW 2nd Ave", "city": "Miami", "state": "FL", "zip": "33136" },
      "phone": "305-374-6806",
      "hours": [
        { "date": "2026-11-13", "open": "07:00", "close": "22:00", "is_closed": false, "is_open_24_hours": false, "note": null },
        { "date": "2026-11-14", "open": "07:00", "close": "22:00", "is_closed": false, "is_open_24_hours": false, "note": null }
      ],
      "time_zone": "EST",
      "departments": ["Floral", "Meat", "Produce", "Publix Bakery", "Publix Deli", "Seafood"],
      "services": ["Check Cashing", "Pharmacy", "In-Store Pickup", "Wine & Beer", "Sushi", "Order Bakery Cakes Online", "Instacart", "Curbside"],
      "pharmacy": {
        "phone": "305-341-9629",
        "hours": [
          { "date": "2026-11-13", "open": "09:00", "close": "21:00", "is_closed": false, "is_open_24_hours": false, "note": null },
          { "date": "2026-11-14", "open": "09:00", "close": "19:00", "is_closed": false, "is_open_24_hours": false, "note": null }
        ]
      },
      "liquor_store": null,
      "latitude": 25.780117,
      "longitude": -80.197358,
      "distance_miles": 0.09,
      "weekly_ad_break_day": "Thursday",
      "opening_date": "2021-08-19",
      "closing_date": null
    }
  ]
}
```

`store_id` is the value every other endpoint takes. `weekly_ad_break_day` is the day the store's weekly ad starts. `services` was shortened here (the store lists 14). `liquor_store` is null or the attached Publix Liquors store's `phone`, `address` and `hours`.

### Weekly ad

```bash
curl -X POST https://api.scavio.dev/api/v1/publix/weekly-ad \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "1614"}'
```

Captured `data` (687 of 691 items and 83 of 88 departments trimmed; `image` trimmed from each item):

```json
{
  "store": { "id": 1614, "name": "3 Miami Central" },
  "ad": { "start_date": "2026-11-12", "end_date": "2026-11-18" },
  "total": 691,
  "count": 691,
  "applied_filters": {},
  "departments": ["Bakery", "Cold Beer", "Deli", "Meat", "Produce"],
  "items": [
    {
      "id": "97ff6748-dfff-45dc-a04e-f5ba0f7bec33",
      "item_code": null,
      "base_product_id": null,
      "title": "Lean Ground Beef 7% Fat",
      "description": "3 lbs or More pkg.",
      "brand": "Publix",
      "department": "Meat",
      "categories": ["meat"],
      "savings_text": "$6.89 lb",
      "additional_savings": null,
      "save_up_to": null,
      "deal_type": "price",
      "price": 6.89,
      "price_unit": "lb",
      "bundle": null,
      "min_quantity": null,
      "fine_print": null,
      "stacked_with_coupon": false,
      "promotion": "Weekly Ad",
      "valid_from": "2026-11-12",
      "valid_to": "2026-11-18"
    },
    {
      "id": "102b439e-bb86-41ce-bbdc-f7597a770d4c",
      "item_code": null,
      "base_product_id": null,
      "title": "Fresh Express Chopped Kit",
      "description": "Free item of equal or lesser price.\nOr Salad Kit or Blends, 5 to 13.3-oz pkg.",
      "brand": "Fresh Express",
      "department": "Produce",
      "categories": ["produce", "bogo"],
      "savings_text": "Buy 1 Get 1 FREE",
      "additional_savings": null,
      "save_up_to": "SAVE UP TO $5.65",
      "deal_type": "bogo",
      "price": null,
      "price_unit": null,
      "bundle": null,
      "min_quantity": null,
      "fine_print": null,
      "stacked_with_coupon": false,
      "promotion": "Weekly Ad",
      "valid_from": "2026-11-12",
      "valid_to": "2026-11-18"
    },
    {
      "id": "405abffb-7d59-408b-b366-5f772b29def4",
      "item_code": null,
      "base_product_id": null,
      "title": "Kraft Stove Top Stuffing Mix",
      "description": "6-oz box",
      "brand": "Kraft",
      "department": "Stuffing/Potatoes",
      "categories": ["grocery"],
      "savings_text": "2 for $4.00",
      "additional_savings": null,
      "save_up_to": "SAVE UP TO $2.90 ON 2",
      "deal_type": "multi",
      "price": null,
      "price_unit": null,
      "bundle": { "quantity": 2, "price": 4 },
      "min_quantity": null,
      "fine_print": null,
      "stacked_with_coupon": false,
      "promotion": "Weekly Ad",
      "valid_from": "2026-11-12",
      "valid_to": "2026-11-18"
    },
    {
      "id": "9358ea78-de55-4126-9c56-bac7c6ef7c41",
      "item_code": 93933,
      "base_product_id": "BMO-DSB-100004",
      "title": "Boar's Head® Italian Whole Sub",
      "description": "Tavern Ham, Genoa Salami, Capicola, Provolone, and Choice of Toppings",
      "brand": "Boar's Head",
      "department": "Deli",
      "categories": ["deli", "fiber", "protein", "order-now"],
      "savings_text": "$9.49 each",
      "additional_savings": null,
      "save_up_to": "SAVE UP TO $2.00",
      "deal_type": "price",
      "price": 9.49,
      "price_unit": "each",
      "bundle": null,
      "min_quantity": null,
      "fine_print": null,
      "stacked_with_coupon": false,
      "promotion": "Weekly Ad",
      "valid_from": "2026-11-12",
      "valid_to": "2026-11-18"
    }
  ]
}
```

How to read a weekly-ad item:

- `deal_type` is `bogo` (Buy 1 Get 1 Free), `b2g1` (Buy 2 Get 1 Free), `multi` ("2 for $4.00"), `price` (a plain sale price), `percent_off` ("25% Off") or `other` (anything else, e.g. "Buy 2 Get 2 FREE"). In this capture: 316 price, 229 bogo, 86 multi, 35 other, 20 b2g1 and 5 percent_off.
- `price` is a number only when `savings_text` is a plain price (`$6.89 lb` -> `price: 6.89`, `price_unit: "lb"`). For BOGO and B2G1 items it is null and the item carries `save_up_to` ("SAVE UP TO $5.65") instead. Quote that text and do not compute a BOGO unit price; for one product's price at the store, `/publix/search` with `bogo: true` returns cards with `price`.
- A multi-buy keeps `price: null` and carries `bundle {quantity, price}`: "2 for $4.00" is `{ "quantity": 2, "price": 4 }`. Quote it as a multi-buy, not as one item's price.
- `additional_savings`, `stacked_with_coupon` and `min_quantity` mark a deal that stacks with a coupon (e.g. a BOGO plus "Save $1.00", `min_quantity: 2`).
- `promotion` is the flyer the item came from: `Weekly Ad`, `Extra Savings` or a seasonal flyer (`2026 Fall Wine` in the capture), each with its own `valid_from` / `valid_to`. The same product can appear under two promotions (the 24-pack Michelob Ultra is listed under both `Weekly Ad` and `2026 Fall Wine` at $25.99): dedupe by title and `savings_text` before counting deals.
- `item_code` is set on 266 of the 691 items here (mostly meat, deli and produce) and null on the rest; pass it to `/publix/product` when present.
- `title` can be null (1 item in this capture); fall back to `description`.

### Extra Savings

```bash
curl -X POST https://api.scavio.dev/api/v1/publix/extra-savings \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "1614"}'
```

Captured `data` (676 of 678 items trimmed; image shortened):

```json
{
  "store": { "id": 1614, "name": "3 Miami Central" },
  "period": { "start_date": "2026-11-05", "end_date": "2026-11-18" },
  "count": 678,
  "items": [
    {
      "id": "bda9e682-b70a-4056-897b-629ad355d050",
      "base_product_id": "RIO-PCI-151435",
      "title": "Alessi Breadsticks, Thin",
      "size": "3 oz (85 g)",
      "brand": "Alessi",
      "categories": ["grocery"],
      "savings_text": "$0.89",
      "savings": 0.89,
      "additional_savings": null,
      "final_price": 4.19,
      "min_quantity": 2,
      "image": "https://images.publixcdn.com/pct/images/products/400000/402397-600x600-A.jpg",
      "url": "https://www.publix.com/pd/alessi-breadsticks-thin/RIO-PCI-151435"
    },
    {
      "id": "41225731-0b72-4892-aeaa-949e12047de4",
      "base_product_id": "RIO-PCI-622725",
      "title": "I and Love and You Top That Dog Food Topper, Tummy, Chicken Recipe in Gravy",
      "size": "3 oz (85 g)",
      "brand": "I and love and you",
      "categories": ["pet"],
      "savings_text": "$0.75",
      "savings": 0.75,
      "additional_savings": null,
      "final_price": 5,
      "min_quantity": 5,
      "image": "https://images.publixcdn.com/pct/images/products/320000/322038-600x600-A.jpg",
      "url": "https://www.publix.com/pd/i-and-love-and-you-top-that-dog-food-topper-tummy-chicken-recipe-in-gravy/RIO-PCI-622725"
    }
  ]
}
```

`savings` is the amount saved and `final_price` the reduced price, both as the site lists them. When `min_quantity` is above 1 (`final_price: 5`, `min_quantity: 5` above), `final_price` may be the price for that quantity rather than one unit: quote it with the quantity and do not divide it. Extra Savings items carry `base_product_id` and `url` but no `item_code`. `period` is the current Extra Savings period; Florida stores showed 11/05-11/18 and Georgia and North Carolina 11/04-11/17.

### Coupons

```bash
curl -X POST https://api.scavio.dev/api/v1/publix/coupons \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "1614"}'
```

Captured `data` (102 of 103 coupons trimmed; terms shortened; image trimmed):

```json
{
  "store": { "id": 1614, "name": "3 Miami Central" },
  "count": 103,
  "items": [
    {
      "id": 9128853,
      "title": "Save $2.00 on any ONE (1) ARM & HAMMER™ Black Box or Hardball Cat Litter",
      "description": "Save $2.00 on any ONE (1) ARM & HAMMER™ Black Box or Hardball Cat Litter",
      "brand": "Arm & Hammer Cat Litter",
      "savings_text": "Save $2.00",
      "value": 2,
      "min_quantity": 1,
      "limit_per_transaction": 1,
      "categories": ["pet"],
      "valid_from": "2026-11-01",
      "valid_to": "2026-12-12",
      "terms": "Valid only for product, size stated. Limit one coupon per purchase. ..."
    }
  ]
}
```

`value` is the dollar amount when the coupon states one and null otherwise (4 of 103 here, e.g. "Free with purchase"). Coupons are listed exactly as any visitor sees them: nothing is clipped and no shopper account is used, so the shopper still has to clip a coupon for it to apply.

### Savings search

```bash
curl -X POST https://api.scavio.dev/api/v1/publix/savings-search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "coffee", "store_id": "1614"}'
```

The captured answer has `query`, `store`, `count: 18` and `items[]`: 11 `weekly_ad`, 6 `extra_savings` and 1 `coupon`. Each item carries `saving_type` and then that feed's own fields (the weekly-ad, Extra Savings or coupon shape above). One trimmed example of each type:

```json
[
  {
    "saving_type": "weekly_ad",
    "id": "d82a242f-3e27-414e-a6e0-0dc549ff3f46",
    "title": "Dunkin' Iced Coffee",
    "brand": "Dunkin",
    "department": "Coffee & Tea",
    "savings_text": "Buy 1 Get 1 FREE",
    "save_up_to": "SAVE UP TO $4.15",
    "deal_type": "bogo",
    "price": null,
    "valid_from": "2026-11-05",
    "valid_to": "2026-11-18"
  },
  {
    "saving_type": "extra_savings",
    "id": "0c5664c1-1c34-4db3-baf8-d01ce9fc5187",
    "title": "Colcafe Instant Coffee, Classic",
    "size": "3 oz (85 g)",
    "savings": 0.8,
    "final_price": 4.55,
    "min_quantity": 1
  },
  {
    "saving_type": "coupon",
    "id": 8982886,
    "title": "Buy any ONE (1) La Colombe Multi-Serve and Get ONE (1) Single Serve 11oz Can FREE",
    "savings_text": "Free with purchase",
    "value": null,
    "valid_from": "2026-11-04",
    "valid_to": "2026-12-01"
  }
]
```

Branch on `saving_type` before reading fields: the three shapes differ.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/publix/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "chicken", "store_id": "1614"}'
```

Captured `data` (45 of 48 items and the facets trimmed):

```json
{
  "query": "chicken",
  "corrected_query": null,
  "store": { "id": 1614, "name": "3 Miami Central" },
  "total": 249,
  "page": 1,
  "page_size": 48,
  "total_pages": 6,
  "count": 48,
  "sort": "relevance",
  "applied_filters": {},
  "items": [
    {
      "item_code": 96215,
      "base_product_id": "RIO-PCI-119468",
      "title": "Publix Boneless Skinless Chicken Breast, USDA Grade a, 97% Fat Free Less Than 4 Lbs.",
      "brand": "Publix",
      "size": null,
      "description": null,
      "image": "https://images.publixcdn.com/pct/images/products/95000/096215-600x600-A.jpg",
      "url": "https://www.publix.com/pd/publix-boneless-skinless-chicken-breast-usda-grade-a-97-fat-free-less-than-4-lbs/RIO-PCI-119468",
      "category_path": ["Meat/Chicken"],
      "aisle": "Meat",
      "on_sale": false,
      "price": null,
      "price_unit": null,
      "bundle": null,
      "starting_price": null,
      "regular_price": null,
      "price_text": null,
      "regular_price_text": null,
      "promo": null,
      "has_coupon": false,
      "is_order_ahead": false
    },
    {
      "item_code": 99649,
      "base_product_id": "RIO-PCI-120474",
      "title": "Publix Chicken Breast Tenderloins,boneless Skinless, 99% Fat Free,usda Grade a",
      "brand": "Publix",
      "size": null,
      "description": null,
      "image": "https://images.publixcdn.com/pct/images/products/95000/099649-600x600-A.jpg",
      "url": "https://www.publix.com/pd/publix-chicken-breast-tenderloinsboneless-skinless-99-fat-freeusda-grade-a/RIO-PCI-120474",
      "category_path": ["Meat/Chicken"],
      "aisle": "Meat",
      "on_sale": true,
      "price": 5.49,
      "price_unit": "lb",
      "bundle": null,
      "starting_price": null,
      "regular_price": 7.29,
      "price_text": "$5.49/lb",
      "regular_price_text": "$7.29/lb",
      "promo": {
        "type": "single",
        "message": "Save $1.80/lb",
        "conditions": null,
        "savings": 1.8,
        "valid_from": "2026-11-12",
        "valid_through": "2026-11-18"
      },
      "has_coupon": false,
      "is_order_ahead": false
    },
    {
      "item_code": 257412,
      "base_product_id": "RIO-PCI-571896",
      "title": "Just Bare® Boneless Skinless Chicken Breast Fillets",
      "brand": "Just Bare®",
      "size": "18oz",
      "description": null,
      "image": "https://images.publixcdn.com/pct/images/products/255000/257412-600x600-A.jpg",
      "url": "https://www.publix.com/pd/just-bare-boneless-skinless-chicken-breast-fillets/RIO-PCI-571896",
      "category_path": ["Meat/Chicken"],
      "aisle": "Meat",
      "on_sale": true,
      "price": 8.79,
      "price_unit": null,
      "bundle": null,
      "starting_price": null,
      "regular_price": null,
      "price_text": "$8.79",
      "regular_price_text": null,
      "promo": {
        "type": "bogo",
        "message": "Buy 1 Get 1 Free",
        "conditions": "of equal or lesser price",
        "savings": 8.79,
        "valid_from": "2026-11-12",
        "valid_through": "2026-11-18"
      },
      "has_coupon": false,
      "is_order_ahead": false
    }
  ],
  "redirected_to": null
}
```

How to read a search, category or order-ahead item:

- `price` is null when Publix shows no price (the first item: not on sale, not order-ahead). That is the normal case for regular grocery items, not an error and not zero.
- `price_text` is the price as shown; `price` is a number only for a plain price line (`$5.49/lb` -> `5.49` with `price_unit: "lb"`; `price_unit` is `lb` or `each` or null). `regular_price` is the crossed-out price when the site shows one.
- `promo.type` is `single`, `bogo` or `multi`, with `message`, `conditions`, `savings`, `valid_from` and `valid_through`. On the BOGO card above `price` and `promo.savings` are both $8.79.
- A multi-buy card carries `bundle {quantity, price}` with `price: null`; an order-ahead item priced "Starts at" carries `starting_price` with `price: null`.
- `aisle` is where the item sits in that store (e.g. `"Meat"`, or `"Aisle 1 - Milk"`).
- `facets[]` (`name`, `label`, `values[]` with `value`, `label`, `count`) covers deals, BOGO, weekly ad, brand, type, diet and nutrition ranges. Use a `Brand` value as `brand`.
- Some keywords make the site open a category instead of a search: those are answered with the category's products. Keywords that lead to an order-ahead page (e.g. "cake") set `redirected_to` and can return no items; use `/publix/order-ahead` for those.
- To keep only items on promotion (the ones with a `price` or a `bundle`), send `on_sale: true` or `bogo: true`.

### Category and categories

```bash
curl -X POST https://api.scavio.dev/api/v1/publix/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category_url": "https://www.publix.com/c/chicken/6772da29-55bf-4051-83d5-104d73ae9a96", "store_id": "1825"}'
```

The captured answer opens with (then `items[]` and `facets[]` in the search shape; 39 of the 48 items have `price: null`):

```json
{
  "category": { "id": "6772da29-55bf-4051-83d5-104d73ae9a96", "name": "Chicken", "path": "Meat/Chicken" },
  "store": { "id": 1825, "name": "Publix at Summerhill" },
  "total": 117,
  "page": 1,
  "page_size": 48,
  "total_pages": 3,
  "count": 48,
  "sort": "relevance",
  "applied_filters": {}
}
```

`/publix/categories` with `{}` returned 16 top-level departments (Baby, Bakery, Beauty and Personal Care, Beer and Wine, Dairy, Deli, Floral, Frozen Food, Grocery, Health and Nutrition, Home and Outdoors, Liquor, Meat, Pet, Produce, Seafood), `count: 382` nodes in all. Each node has `id`, `name`, `url`, `parent_id`, `level` and `children[]`, e.g. `{ "id": "78e5beda-3150-479b-ad86-8d41b82aa0fb", "name": "Baby Food", "url": "https://www.publix.com/c/baby-food/78e5beda-3150-479b-ad86-8d41b82aa0fb", "level": 2 }`. Department urls use `/d/`, lower levels `/c/`. Pass any `id` to `/publix/category` as `category_id`.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/publix/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_code": "90355", "store_id": "1825"}'
```

Captured `data` (122 of 123 nutrition labels trimmed; 6 of 11 nutrients trimmed):

```json
{
  "item_code": 90355,
  "base_product_id": "BMO-DSB-100011",
  "title": "Publix Chicken Tender Sub",
  "brand": "Publix",
  "size": null,
  "description": "Our famous hand-breaded chicken tenders, with provolone, lettuce, and tomato.",
  "image": "https://images.publixcdn.com/pct/images/products/90000/090355-600x600-A.jpg",
  "url": "https://www.publix.com/pd/publix-chicken-tender-sub/BMO-DSB-100011",
  "category_path": ["Deli/Deli Subs", "In Store Pickup/Subs Flatbreads/Subs"],
  "aisle": "Deli",
  "on_sale": false,
  "price": 11.99,
  "price_unit": null,
  "bundle": null,
  "starting_price": null,
  "regular_price": null,
  "price_text": "$11.99",
  "regular_price_text": null,
  "promo": null,
  "has_coupon": false,
  "is_order_ahead": true,
  "short_description": "Hot Chicken Tenders and Choice of Cheese",
  "lead_time": "Ready as soon as 30 minutes",
  "serves": null,
  "calories": "450 Cal - 1955 Cal/Sub",
  "nutrition": [
    {
      "title": "Chicken Tenders",
      "size": "Half",
      "serving_size": "2 tenders (188g )",
      "includes": null,
      "group": "Deli Sub Recipe Included",
      "serving_size_value": null,
      "serving_size_unit": null,
      "household_serving_size": null,
      "household_serving_unit": null,
      "servings_per_container": null,
      "nutrients": [
        { "name": "Calories", "amount": 470, "unit": null, "value": "470", "daily_value_percent": null },
        { "name": "Total Fat (g)", "amount": 20, "unit": "g", "value": "20", "daily_value_percent": null },
        { "name": "Sodium (mg)", "amount": 880, "unit": "mg", "value": "880", "daily_value_percent": null },
        { "name": "Sugars (g)", "amount": null, "unit": "g", "value": "< 1 g", "daily_value_percent": null },
        { "name": "Protein (g)", "amount": 46, "unit": "g", "value": "46", "daily_value_percent": null }
      ]
    }
  ],
  "store": { "id": 1825, "name": "Publix at Summerhill" }
}
```

The product is the item's card (the search fields, plus `short_description`, `lead_time`, `serves` and `calories` for order-ahead items) and its nutrition facts. A deli sub has one nutrition label per component and size (`Half`, `Whole`; 123 labels for this sub, 87 with nutrients); `nutrition` is null when Publix has none. `amount` is null when the label gives a range or a bound (`"< 1 g"`): read `value`. Ingredients, allergens, UPC and reviews are not published by Publix online, so they are not returned. The same sub was $12.09 at store 1614 in the order-ahead capture below.

### Order-ahead menu

```bash
curl -X POST https://api.scavio.dev/api/v1/publix/order-ahead \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "1614"}'
```

Captured `data` (59 of 60 items trimmed):

```json
{
  "section": "subs",
  "store": { "id": 1614, "name": "3 Miami Central" },
  "total": 66,
  "page": 1,
  "page_size": 60,
  "total_pages": 2,
  "count": 60,
  "items": [
    {
      "item_code": 90355,
      "base_product_id": "BMO-DSB-100011",
      "title": "Publix Chicken Tender Sub",
      "brand": "Publix",
      "size": null,
      "description": "Our famous hand-breaded chicken tenders, with provolone, lettuce, and tomato.",
      "image": "https://images.publixcdn.com/pct/images/products/90000/090355-600x600-A.jpg",
      "url": "https://www.publix.com/pd/publix-chicken-tender-sub/BMO-DSB-100011",
      "category_path": ["Deli/Deli Subs", "In Store Pickup/Subs Flatbreads/Subs"],
      "aisle": "Deli",
      "on_sale": false,
      "price": 12.09,
      "price_unit": null,
      "bundle": null,
      "starting_price": null,
      "regular_price": null,
      "price_text": "$12.09",
      "regular_price_text": null,
      "promo": null,
      "has_coupon": false,
      "is_order_ahead": true,
      "short_description": "Hot Chicken Tenders and Choice of Cheese",
      "lead_time": "Ready as soon as 30 minutes",
      "serves": null,
      "calories": "450 Cal - 1955 Cal/Sub",
      "pay_online": true
    }
  ]
}
```

Every order-ahead item has a price (`price`, or `starting_price` for "Starts at" items), which makes this the endpoint for Pub Sub prices by store. Subs on promotion carry `on_sale: true` and a `promo` such as `{ "type": "single", "message": "Save $2.10 on Whole", "savings": 2.1 }`. `section: "all"` is the whole order-ahead catalog (about 1,150 items over 60-item pages).

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/publix/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "chick", "store_id": "1614"}'
```

Captured `data` (7 of 10 suggestions and 3 of 4 products trimmed):

```json
{
  "query": "chick",
  "store_id": 1614,
  "count": 10,
  "suggestions": [
    { "text": "chicken wings", "type": "query" },
    { "text": "chicken tenders", "type": "query" },
    { "text": "chicken tender sub", "type": "query" }
  ],
  "products": [
    {
      "item_code": 13690,
      "base_product_id": "RIO-HC1-104724",
      "title": "Publix Deli Fried Chicken Wings 20-Piece Hot & Spicy Non-Breaded",
      "description": "Hot",
      "saving_text": null,
      "image": "https://images.publixcdn.com/pct/images/products/10000/013690-600x600-A.jpg",
      "url": "https://www.publix.com/pd/publix-deli-fried-chicken-wings-20-piece-hot-and-spicy-non-breaded/RIO-HC1-104724"
    }
  ]
}
```

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def publix(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/publix/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Publix stores near a ZIP (1 credit)
stores = publix("stores", {"zip": "33101", "limit": 3})["stores"]

for s in stores:
    sid = s["store_id"]
    # 2. This week's BOGO list at each store (1 credit per store)
    ad = publix("weekly-ad", {"store_id": sid, "bogo_only": True})
    print(s["name"], ad["ad"]["start_date"], "to", ad["ad"]["end_date"], ad["count"], "BOGO items")
    for item in ad["items"][:5]:
        print("  ", item["title"], "|", item["savings_text"], "|", item["save_up_to"])

    # 3. Pub Sub prices at the same store (1 credit per store)
    subs = publix("order-ahead", {"store_id": sid})
    for sub in subs["items"][:3]:
        print("  ", sub["title"], sub["price"] if sub["price"] is not None else sub["starting_price"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. `fetched_at` is the ISO time the data was retrieved; nothing is cached, so it is the age of the data. Store-scoped answers echo `store` {`id`, `name`}. Key `data` fields:

- **grid item (search, category, order-ahead)** - `item_code`, `base_product_id`, `title`, `brand`, `size`, `description`, `image`, `url`, `category_path[]`, `aisle`, `on_sale`, `price`, `price_unit`, `bundle` {`quantity`, `price`}, `starting_price`, `regular_price`, `price_text`, `regular_price_text`, `promo` {`type`, `message`, `conditions`, `savings`, `valid_from`, `valid_through`}, `has_coupon`, `is_order_ahead`; order-ahead items add `short_description`, `lead_time`, `serves`, `calories`, `pay_online`.
- **search** - `query`, `corrected_query`, `store`, `total`, `page`, `page_size`, `total_pages`, `count`, `sort`, `applied_filters`, `items[]`, `facets[]` {`name`, `label`, `values[]` {`name`, `value`, `label`, `count`}}, `redirected_to`.
- **category** - `category` {`id`, `name`, `path`}, then the search fields from `store` on.
- **categories** - `parent_id`, `store_id`, `count`, `categories[]` {`id`, `name`, `url`, `parent_id`, `level`, `children[]`}; with `parent_id` also `category`.
- **product** - the grid item plus `short_description`, `lead_time`, `serves`, `calories`, `nutrition[]` {`title`, `size`, `serving_size`, `includes`, `group`, `serving_size_value`, `serving_size_unit`, `household_serving_size`, `household_serving_unit`, `servings_per_container`, `nutrients[]` {`name`, `amount`, `unit`, `value`, `daily_value_percent`}}, `store`.
- **weekly-ad** - `store`, `ad` {`start_date`, `end_date`}, `total`, `count`, `applied_filters`, `departments[]`, `items[]` {`id`, `item_code`, `base_product_id`, `title`, `description`, `brand`, `department`, `categories[]`, `savings_text`, `additional_savings`, `save_up_to`, `deal_type`, `price`, `price_unit`, `bundle`, `min_quantity`, `fine_print`, `stacked_with_coupon`, `promotion`, `valid_from`, `valid_to`, `image`}.
- **extra-savings** - `store`, `period` {`start_date`, `end_date`}, `count`, `items[]` {`id`, `base_product_id`, `title`, `size`, `brand`, `categories[]`, `savings_text`, `savings`, `additional_savings`, `final_price`, `min_quantity`, `image`, `url`}.
- **coupons** - `store`, `count`, `items[]` {`id`, `title`, `description`, `brand`, `savings_text`, `value`, `min_quantity`, `limit_per_transaction`, `categories[]`, `valid_from`, `valid_to`, `terms`, `image`}.
- **savings-search** - `query`, `store`, `count`, `items[]`: `saving_type` (`weekly_ad`, `extra_savings` or `coupon`) plus that feed's item fields.
- **order-ahead** - `section`, `store`, `total`, `page`, `page_size`, `total_pages`, `count`, `items[]` (grid items with the order-ahead fields).
- **stores** - `zip`, `radius_miles`, `count`, `stores[]` {`store_id`, `name`, `short_name`, `type`, `address` {`street`, `city`, `state`, `zip`}, `phone`, `hours[]` {`date`, `open`, `close`, `is_closed`, `is_open_24_hours`, `note`}, `time_zone`, `departments[]`, `services[]`, `pharmacy` {`phone`, `hours[]`}, `liquor_store`, `latitude`, `longitude`, `distance_miles`, `weekly_ad_break_day`, `opening_date`, `closing_date`, `image`}.
- **suggestions** - `query`, `store_id`, `count`, `suggestions[]` {`text`, `type`}, `products[]` {`item_code`, `base_product_id`, `title`, `description`, `saving_text`, `image`, `url`}.

## Guardrails

- Shelf prices: publix.com shows prices only for items on promotion and for order-ahead (deli and bakery) items. A null `price` means Publix shows no price for that item at that store; never fill it in, estimate it, or present it as zero. Never call a promotion price the item's regular price.
- Store scope: every price is one store's. Always name the store (`store.id` and `store.name`) next to a price, and never call one store's number "the Publix price".
- Deals: quote BOGO and B2G1 items with `savings_text` and `save_up_to`; quote multi-buys with `bundle` ("2 for $4.00"); quote Extra Savings `final_price` with its `min_quantity`. Respect `valid_from` / `valid_to` and the ad dates.
- Item codes: `item_code` is Publix's own item code, not a UPC. Publix does not publish UPCs online, so this skill cannot match items by UPC or barcode.
- Coupons are listed, never clipped; the shopper has to clip them on publix.com or in the Publix app for them to apply.
- Delivery prices: delivery and curbside prices on Publix's Instacart storefront are not returned; Publix's own pricing policy says they are higher than in-store prices. Do not present these results as delivery prices or vice versa.
- Not covered: regular shelf prices for items not on promotion, ratings and reviews (Publix shows none), ingredients and allergens, UPCs, the Spanish weekly ad, coupon clipping, cart, ordering and checkout, pharmacy data beyond the pharmacy's phone and hours, and price history.
- Publix's Terms of Use (last updated 6/30/2025) license its websites and apps "for your personal, noncommercial use only" and say users agree not to "access or use the Services by means of any automated program, expert system, electronic agent or 'bot' except for general purpose search engines" or to "scrape, copy, republish, license, or sell the information or Materials on the Services". This is not legal advice; the user is responsible for checking the current terms for their use case.
- Never fabricate prices, item codes, store numbers, deals, coupons or nutrition. Only return what the API returned, with the store it came from.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a missing `store_id` on a price endpoint; a `store_id` that is not 1 to 5 digits; category without `category_url` or `category_id`; stores without `zip`, `city` + `state` or `store_id`; `page`, `limit` or `radius_miles` out of range; an unknown `sort` or `section`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means an unknown store number ("No Publix store 99991.") or an unknown item code on product. Not-founds are charged 1 credit: take store numbers and item codes from a previous answer rather than guessing them. A search with no match is not a 404: it answers 200 with an empty `items` list.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api).
- `502` means Publix data was temporarily unavailable ("Publix is temporarily unavailable. Please try again."). Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Publix is busy: wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.55.0
npm install scavio@0.56.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: stores } = await scavio.publix.stores({ zip: "33101" });
const { data: ad } = await scavio.publix.weeklyAd({ store_id: "1614", bogo_only: true });
const { data: extra } = await scavio.publix.extraSavings({ store_id: "1614" });
const { data: coupons } = await scavio.publix.coupons({ store_id: "1614" });
const { data: coffee } = await scavio.publix.savingsSearch({ query: "coffee", store_id: "1614" });
const { data: found } = await scavio.publix.search({ query: "chicken", store_id: "1614", on_sale: true });
const { data: chicken } = await scavio.publix.category({ category_id: "6772da29-55bf-4051-83d5-104d73ae9a96", store_id: "1825" });
const { data: tree } = await scavio.publix.categories({});
const { data: sub } = await scavio.publix.product({ item_code: "90355", store_id: "1825" });
const { data: subs } = await scavio.publix.orderAhead({ store_id: "1614" });
const { data: hints } = await scavio.publix.suggestions({ query: "chick", store_id: "1614" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.publix.stores(...)`, `client.publix.weekly_ad(...)`, `client.publix.extra_savings(...)`, `client.publix.coupons(...)`, `client.publix.savings_search(...)`, `client.publix.search(...)`, `client.publix.category(...)`, `client.publix.categories(...)`, `client.publix.product(...)`, `client.publix.order_ahead(...)` and `client.publix.suggestions(...)`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all eleven endpoints as tools: `find_publix_stores`, `get_publix_weekly_ad`, `get_publix_extra_savings`, `get_publix_coupons`, `search_publix_savings`, `search_publix`, `get_publix_category`, `get_publix_categories`, `get_publix_product`, `get_publix_order_ahead` and `get_publix_suggestions`. Publix is opt-in: add `publix` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.53.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,publix"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [stores](https://scavio.dev/docs/publix-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api), [weekly ad](https://scavio.dev/docs/publix-weekly-ad?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api), [extra savings](https://scavio.dev/docs/publix-extra-savings?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api), [coupons](https://scavio.dev/docs/publix-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api), [savings search](https://scavio.dev/docs/publix-savings-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api), [search](https://scavio.dev/docs/publix-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api), [category](https://scavio.dev/docs/publix-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api), [categories](https://scavio.dev/docs/publix-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api), [product](https://scavio.dev/docs/publix-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api), [order ahead](https://scavio.dev/docs/publix-order-ahead?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api), [suggestions](https://scavio.dev/docs/publix-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api). Overview: [Publix API](https://scavio.dev/publix-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api).
