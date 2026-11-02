---
name: whole-foods-grocery-data
description: "Whole Foods grocery data API: search and browse Whole Foods Market at the store you choose with that store's shelf price, sale price and Prime member price with sale dates, list every product on sale at a store, read one product with ingredients, nutrition facts, diets and its in-store and online prices side by side, find stores near a ZIP, read one store, and pull its weekly sales flyer. 7 endpoints, 1 credit each."
version: 1.0.0
tags: whole-foods, whole-foods-market, wholefoods, whole-foods-api, whole-foods-grocery-data, grocery, groceries, supermarket, organic, store-prices, grocery-prices, prime-deals, sale-prices, weekly-ad, sales-flyer, nutrition-facts, ingredients, product-search, product-data, category-listing, store-locator, retail, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/wholefoods-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data
---

# Whole Foods Grocery Data API - Store Prices, Prime Deals, Sales Flyer

Search and browse Whole Foods Market at the store you choose, with that store's shelf prices: regular price, sale price and the Prime member price, with the sale start and end dates, up to 60 products per page. List every product on sale at a store, read one product with ingredients, nutrition facts, diets, SNAP EBT eligibility and its in-store and online prices as two separate blocks, find stores near a ZIP, read one store's details, and pull a store's current weekly sales flyer. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find groceries at Whole Foods by keyword, or list a category such as cheese, produce or dairy
- Check a Whole Foods product's shelf price, sale price or Prime member price at a specific store
- List everything on sale at a Whole Foods store, or the Prime deals in one category
- Read the weekly Whole Foods sales flyer for a store
- Read a product's ingredients, nutrition facts or dietary attributes (vegan, gluten-free, organic)
- Compare a product's in-store price with its online delivery or pickup price
- Find Whole Foods stores near a ZIP code, with hours
- Compare Whole Foods prices across stores or with other grocers, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All Whole Foods endpoints cost **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/wholefoods/search` | 1 | Up to 60 products per page at one store: ASIN, slug, name, brand, image, regular, sale and Prime price with multi-buy quantities, sale start and end dates, price unit, on-sale and local flags, URL. Total results and facets (category tree, featured, diets) with counts |
| `POST /api/v1/wholefoods/category` | 1 | One category at one store, same rows as search, with the category breadcrumb, six sorts and on-sale and diet filters |
| `POST /api/v1/wholefoods/deals` | 1 | Every product on sale at one store, store-wide or in one category, same rows as search |
| `POST /api/v1/wholefoods/product` | 1 | One product by ASIN, URL or slug: name, brand, description, highlights, ingredients, nutrition facts, diets, SNAP EBT eligibility, category, images. With `store_id`: the store's shelf prices (`in_store`) and its online delivery/pickup price, unit price and availability (`online`) |
| `POST /api/v1/wholefoods/stores` | 1 | Stores near a US ZIP, nearest first: store id, name, address, phone, coordinates, distance, time zone, seven days of in-store and pickup hours |
| `POST /api/v1/wholefoods/store` | 1 | One store by id: name, status, Prime eligibility, opening date, address, coordinates, time zone, store page and sales flyer URLs |
| `POST /api/v1/wholefoods/sales-flyer` | 1 | The store's current weekly flyer: per promotion the product name, brand, headline, description, terms, regular, sale and Prime price as printed, start and end dates, image, rank and the ASINs it covers |

## Workflow

Every price is a store's price. Pick the store first; without `store_id`, search, category and deals use store 10145 (Lamar, Austin TX).

1. **Find the store:** call `/wholefoods/stores` with the user's `zip`. Each row has a 5-digit `store_id`.
2. **Search at that store:** call `/wholefoods/search` with `query` and `store_id`. Each row has an `asin` and the store's shelf prices.
3. **Browse or list deals:** call `/wholefoods/category` with a category slug (from the `category` facet of any search), or `/wholefoods/deals` for everything on sale.
4. **One product in full:** call `/wholefoods/product` with the row's `asin` and the same `store_id` for nutrition, ingredients and the in-store vs online prices.
5. **This week's flyer:** call `/wholefoods/sales-flyer` with `store_id`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars) |
| `store_id` | string | `10145` | 5-digit Whole Foods store id from `/stores` |
| `sort` | string | `relevance` | `relevance`, `price_asc` or `price_desc` (search honours no other sort) |
| `on_sale` | boolean | false | Only products on sale at the store |
| `diet` | string | - | `vegan`, `gluten-free`, `organic`, `dairy-free` or `vegetarian` |
| `category` | string | - | Restrict to one category slug, e.g. `milk-cream` |
| `limit` | integer | 60 | Products per page, 1-60 |
| `offset` | integer | 0 | Products to skip, 0-10000 (60 = page 2 at the default limit) |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category` | string | required | Category slug, e.g. `dairy-eggs`, `cheese`, `produce`, `fresh-fruit`; `all-products` lists the whole store. Slugs are in the `category` facet of any search |
| `store_id` | string | `10145` | 5-digit store id |
| `sort` | string | `featured` | `featured`, `popular`, `price_asc`, `price_desc`, `brand_az` or `brand_za` |
| `on_sale` | boolean | false | Only products on sale at the store |
| `diet` | string | - | `vegan`, `gluten-free`, `organic`, `dairy-free` or `vegetarian` |
| `limit` | integer | 60 | Products per page, 1-60 |
| `offset` | integer | 0 | Products to skip, 0-10000 |

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category` | string | `all-products` | Category slug; the default is every sale item at the store |
| `store_id` | string | `10145` | 5-digit store id |
| `sort` | string | `featured` | Same values as `/category` |
| `diet` | string | - | Same values as `/search` |
| `limit` | integer | 60 | Products per page, 1-60 |
| `offset` | integer | 0 | Products to skip, 0-10000 |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `asin` | string | one of | Product ASIN, a search row's `asin` (`"B0BCBNG8LS"`) |
| `url` | string | one of | wholefoodsmarket.com product URL |
| `slug` | string | one of | A search row's `slug` |
| `store_id` | string | - | 5-digit store id. Adds that store's `in_store` and `online` price blocks; without it both are `null` |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | US ZIP code. Searches 15 miles, widening to 50 |

### Store (`/store`) and Sales flyer (`/sales-flyer`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string | required | 5-digit store id from `/stores` |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/wholefoods/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asin": "B078WVT2BC", "store_id": "10160"}'
```

Captured response (Elmhurst hazelnut milk at store 10160, Columbus Circle, New York; description, images and nutrition trimmed):

```json
{
  "data": {
    "asin": "B078WVT2BC",
    "name": "Milk Hazelnut Unsweetened, 32 Fl Oz",
    "short_name": "Unsweetened Hazelnut Milked",
    "brand": "Elmhurst",
    "ingredients": "Filtered Water, Hazelnuts.",
    "diets": ["vegan", "kosher"],
    "nutrition": {
      "calories": "90",
      "serving_size": "8 fl oz (240ml)",
      "servings_per_container": "4.0 servings per container",
      "macronutrients": [
        { "name": "Total Fat", "amount": "9g", "daily_value_percent": "12%", "level": "TOP" },
        { "name": "Protein", "amount": "2g", "daily_value_percent": null, "level": "TOP" }
      ]
    },
    "snap_ebt": "SNAP EBT eligible",
    "category": "Grocery",
    "product_type": "MILK_SUBSTITUTE",
    "store_id": "10160",
    "in_store": {
      "regular_price": 7.29,
      "sale_price": null,
      "sale_quantity": null,
      "prime_price": null,
      "prime_quantity": null,
      "sale_start_date": null,
      "sale_end_date": null,
      "price_unit": null,
      "is_local": true
    },
    "online": {
      "price": 7.49,
      "list_price": null,
      "savings": null,
      "savings_percent": null,
      "prime_price": null,
      "unit_price": 0.23,
      "unit_price_unit": "fluid ounce",
      "currency": "USD",
      "availability": "IN_STOCK",
      "max_order_quantity": 5
    },
    "url": "https://www.wholefoodsmarket.com/grocery/product/elmhurst-unsweetened-hazelnut-milked-32-fz-b078wvt2bc"
  },
  "response_time": 1425,
  "credits_used": 1
}
```

A captured `/deals` row at store 10160, a multi-buy with a Prime price (image trimmed):

```json
{
  "position": 46,
  "asin": "B01DIZT0KO",
  "slug": "boulder-canyon-avocado-oil-sea-salt-potato-chips-525-oz-b01dizt0ko",
  "name": "Avocado Oil Sea Salt Potato Chips, 5.25 OZ",
  "brand": "Boulder Canyon",
  "regular_price": 4.69,
  "sale_price": 12.23,
  "sale_quantity": 3,
  "prime_price": 11.01,
  "prime_quantity": 3,
  "sale_start_date": "2026-10-21T00:00:00Z",
  "sale_end_date": "2026-11-03T23:59:59Z",
  "price_unit": null,
  "on_sale": true,
  "is_local": false,
  "store_id": "10160",
  "url": "https://www.wholefoodsmarket.com/grocery/product/boulder-canyon-avocado-oil-sea-salt-potato-chips-525-oz-b01dizt0ko"
}
```

That row is 3 bags for $12.23, or 3 for $11.01 with Prime, against $4.69 each at regular price.

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def wfm(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/wholefoods/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. The nearest store (1 credit)
store = wfm("stores", {"zip": "10019"})["stores"][0]
STORE = store["store_id"]
print(store["name"], store["address"], store["distance_miles"], "mi")

# 2. Search at that store, cheapest first (1 credit)
for p in wfm("search", {"query": "milk", "store_id": STORE, "sort": "price_asc", "limit": 20})["products"]:
    unit = f"/{p['price_unit']}" if p["price_unit"] else ""
    print(p["name"][:50], p["regular_price"], unit, "sale:", p["sale_price"], "x", p["sale_quantity"], "prime:", p["prime_price"])

# 3. Everything on sale in one category (1 credit)
deals = wfm("deals", {"category": "cheese", "store_id": STORE})
print(deals["total_results"], "cheeses on sale")

# 4. This week's flyer (1 credit)
for promo in wfm("sales-flyer", {"store_id": STORE})["promotions"][:5]:
    print(promo["product_name"], promo["sale_price"], "Prime:", promo["prime_price"], "until", promo["end_date"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Whole Foods answered.

- **search** - `query`, `category`, `store_id`, `sort`, `on_sale`, `diet`, `offset`, `limit`, `total_results`, `count`, `products[]` (`position`, `asin`, `slug`, `name`, `brand`, `image`, `regular_price`, `sale_price`, `sale_quantity`, `prime_price`, `prime_quantity`, `sale_start_date`, `sale_end_date`, `price_unit`, `on_sale`, `is_local`, `store_id`, `url`), `facets[]` {`name` (`category`, `featured`, `diets`), `label`, `options[]` {`slug`, `label`, `count`, `selected`, `children[]`}}.
- **category** and **deals** - `category`, `breadcrumb[]` {`slug`, `label`}, then the same fields as search from `store_id` on.
- **product** - `asin`, `name`, `short_name`, `brand`, `description`, `about[]`, `ingredients`, `diets[]`, `nutrition` {`calories`, `serving_size`, `servings_per_container`, `macronutrients[]`, `vitamins_and_minerals[]`: {`name`, `amount`, `daily_value_percent`, `level`}}, `snap_ebt`, `category`, `product_type`, `images[]`, `store_id`, `in_store` {`regular_price`, `sale_price`, `sale_quantity`, `prime_price`, `prime_quantity`, `sale_start_date`, `sale_end_date`, `price_unit`, `is_local`} or `null`, `online` {`price`, `list_price`, `savings`, `savings_percent`, `prime_price`, `unit_price`, `unit_price_unit`, `currency`, `availability`, `max_order_quantity`} or `null`, `url`.
- **stores** - `zip`, `count`, `stores[]` (`store_id`, `name`, `address`, `city`, `state`, `zip`, `latitude`, `longitude`, `phone`, `distance_miles`, `time_zone`, `in_store_hours[]` and `pickup_hours[]` {`date`, `opens_at`, `closes_at`}, `in_store_shopping_disabled`, `url`).
- **store** - `store_id`, `name`, `status`, `phone`, `prime_eligible`, `opened_at`, `address`, `city`, `state`, `zip`, `country`, `latitude`, `longitude`, `time_zone`, `folder`, `url`, `sales_flyer_url`.
- **sales-flyer** - `store_id`, `store_name`, `prime_eligible`, `count`, `promotions[]` (`promotion_id`, `product_name`, `brand`, `headline`, `description`, `terms`, `package_size`, `regular_price`, `sale_price`, `prime_price`, `start_date`, `end_date`, `image`, `tier`, `rank`, `asins[]`).

## Guardrails

- Prices are per store, in dollars. The same product often costs a different amount at another store, so always name the store when quoting a price. Without `store_id`, search, category and deals use store 10145 (Lamar, Austin TX).
- `regular_price`, `sale_price` and `prime_price` are shelf prices. `prime_price` is the Prime member price and needs a Prime membership; never present it as the price everyone pays.
- A multi-buy is a total: `sale_price` 12.23 with `sale_quantity` 3 is 3 for $12.23, not $12.23 each. The same holds for `prime_price` and `prime_quantity`. Divide before comparing with `regular_price`.
- `price_unit` `"lb"` means the price is per pound; `null` means per item.
- `/product` returns two separate price blocks. `in_store` is the shelf price; `online` is the same store's delivery/pickup price, and the two often differ. Label which one you quote. Both are `null` without `store_id`; `in_store` is `null` when that store does not list the item, `online` when it has no online offer.
- Flyer prices are display text as printed (`"$26.99/lb"`, `"44% off"`, `"$10.49 to $13.49"`), not numbers. Quote them as written.
- Search honours only `relevance`, `price_asc` and `price_desc`. Popularity, featured and brand sorts exist only on `/category` and `/deals`.
- There are no ratings, reviews or UPCs anywhere on Whole Foods; the product id is the ASIN. There is no per-store unit count either: `online.availability` is the online offer's status, not shelf stock.
- An unknown `store_id` on search, category or deals returns an empty list (`total_results` 0) and is charged, not an error. If a listing is empty, check the store id with `/store` before telling the user nothing matches.
- `/store` returns `phone` as digits only (`"2128239600"`); `/stores` returns the same number formatted (`"(212) 823-9600"`).
- Store hours in `/stores` are UTC timestamps; convert with the row's `time_zone` before quoting a local time.
- Never fabricate prices, deals or nutrition. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, a `store_id` that is not 5 digits, an unknown `sort` or `diet`, `limit` above 60, a malformed ZIP, or none of `asin`, `url` or `slug` on `/product`). A product whose slug has no ASIN also answers `400`: its prices are in search and category rows.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means an unknown category slug, store id (on `/store` and `/sales-flyer`) or ASIN. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data).
- `502` or `503` means Whole Foods is temporarily unavailable. It is not charged; retry after a few seconds.

## SDKs

```bash
pip install scavio==0.33.0
npm install scavio@0.33.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: near } = await scavio.wholeFoods.stores({ zip: "10019" });
const store_id = near.stores[0].store_id;
const { data: found } = await scavio.wholeFoods.search({ query: "milk", store_id, sort: "price_asc" });
const item = await scavio.wholeFoods.product({ asin: found.products[0].asin, store_id });
const flyer = await scavio.wholeFoods.salesFlyer({ store_id });
```

MCP: the Scavio MCP server exposes all 7 endpoints as tools (`search_whole_foods`, `get_whole_foods_category`, `get_whole_foods_deals`, `get_whole_foods_product`, `get_whole_foods_stores`, `get_whole_foods_store`, `get_whole_foods_sales_flyer`). Whole Foods is opt-in: add `wholefoods` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.31.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,wholefoods"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/wholefoods-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data), [category](https://scavio.dev/docs/wholefoods-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data), [deals](https://scavio.dev/docs/wholefoods-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data), [product](https://scavio.dev/docs/wholefoods-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data), [stores](https://scavio.dev/docs/wholefoods-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data), [store](https://scavio.dev/docs/wholefoods-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data), [sales flyer](https://scavio.dev/docs/wholefoods-sales-flyer?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data). Overview: [Whole Foods API](https://scavio.dev/wholefoods-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data).
