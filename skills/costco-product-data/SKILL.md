---
name: costco-product-data
description: "Costco product data API: search and category listings with per-warehouse shelf price and stock, full item detail for up to 20 items, online vs in-warehouse prices at up to 10 warehouses with promotion dates, warehouse stock status, gas prices, the member coupon book, deal feeds, a clearance finder and reviews. 13 endpoints, mostly 1 credit each."
version: 1.0.0
tags: costco, costco-api, costco-product-data, product-data, product-search, retail, warehouse-club, warehouse-prices, gas-prices, coupons, clearance, pricing, product-reviews, price-monitoring, catalog-enrichment, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/costco-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data
---

# Costco Product Data API - Warehouse Prices, Stock, Gas, Coupons

Search Costco, read items in full, compare the online price with the shelf price at specific warehouses, check warehouse stock, and pull gas prices, the member coupon book, deal feeds and clearance markdowns. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find products on costco.com or costco.ca by keyword, item number, category, brand, price band or rating
- Look up a Costco item by item number, product id or a pasted `costco.com` product URL
- Compare the online price with the in-warehouse price at one or more Costco warehouses
- Check whether a warehouse has an item in stock, or offers pickup or same-day delivery for it
- Find Costco warehouses near a zip code or coordinates, with hours, departments and services
- Get current regular, premium and diesel prices at Costco gas stations
- Read the current Costco member coupon book, or the new, treasure hunt, while-supplies-last and on-sale deal feeds
- Find clearance and manager-markdown items at a specific warehouse
- Read customer reviews for a Costco product with the rating distribution
- Monitor Costco pricing and promotions, or enrich a catalog with Costco item data

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Endpoints in this skill cost 1 credit each unless the table below says otherwise.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Most Costco endpoints cost **1 credit**; US search, category, deals and clearance cost **2**, and the multi-warehouse ones scale with the number of warehouses.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/costco/search` | 2 on `us` (1 on `ca` and the other countries) | Keyword or item-number results: online and original price, rating, member-only and stock flags, promotions, facets. With `warehouse_id`, each row adds that warehouse's shelf price, stock and price code |
| `POST /api/v1/costco/category` | 2 on `us` (1 on `ca`) | Products in a category, same filters and row shape as search |
| `POST /api/v1/costco/categories` | 1 | The department list, or the full subcategory tree under one department |
| `POST /api/v1/costco/product` | 1 (1-20 ids) | Full detail for up to 20 items: description, features, specifications, variants, purchase limits, delivery fee, promotions with start and end dates |
| `POST /api/v1/costco/prices` | 1 for 1-9 warehouses, 2 for 10 | Online price vs in-warehouse price per warehouse: discount, final price, promotion dates, per-order and per-member limits, price code |
| `POST /api/v1/costco/availability` | 1 per 5 warehouses | In-warehouse stock status for one item at up to 10 warehouses, plus pickup and same-day delivery |
| `POST /api/v1/costco/reviews` | 1 per page | Review bodies with the rating distribution and recommend count; sort, star filter, up to 100 per page |
| `POST /api/v1/costco/warehouses` | 1 (2 on costco.ca) | Warehouses near a US zip or coordinates: `warehouse_id`, address, hours, departments, services, gas station hours and prices |
| `POST /api/v1/costco/gas` | 1 by location (2 on costco.ca); by warehouse 1 per 5 (2 per warehouse on costco.ca) | Regular, premium and diesel prices at Costco gas stations |
| `POST /api/v1/costco/coupons` | 1 | The current member coupon book: item number, amount off, final price, warehouse/online scope, limits, valid dates. US only |
| `POST /api/v1/costco/deals` | 2 on `us` (1 on `ca`) | Deal feeds: `new`, `while_supplies_last`, `treasure_hunt`, `member_favorites`, `online_only`, `on_sale` |
| `POST /api/v1/costco/clearance` | 2 on `us`, 1 on `ca` (any `pages` value) | Items at one warehouse whose shelf price carries a markdown code: .97 clearance, .00/.88 manager markdown, .49/.79/.89 special buy on request |
| `POST /api/v1/costco/autocomplete` | 1 | Search suggestions for a partial query, plus matching warehouse locations |

**Countries.** `country` is `us` (costco.com, default) or `ca` (costco.ca) on every endpoint except coupons, which is US only and takes no parameters. Search, product and warehouses also accept `uk`, `au`, `mx`, `jp`, `kr` and `tw` for keyword, sort and paging only - no warehouse prices and no gas outside the US and Canada.

## Workflow

1. **Find a warehouse:** call `/costco/warehouses` with `zip` (US) or `latitude` + `longitude`. Read `warehouses[].warehouse_id` (e.g. `1062`). `/costco/autocomplete` also resolves a town name to warehouses.
2. **Find items:** call `/costco/search` with `query` (or `/costco/category` with a `slug` from `/costco/categories`). Pass `warehouse_id` to get that warehouse's shelf price and stock on every row at no extra cost (2 credits on `us`, 1 on `ca`).
3. **Item detail:** call `/costco/product` with `item_id`, or up to 20 at once with `item_ids`.
4. **Price across warehouses:** call `/costco/prices` with the item and `warehouse_ids` (up to 10). The online price is always included.
5. **Stock:** call `/costco/availability` with `item_number` and `warehouse_ids`.
6. **Reviews:** call `/costco/reviews` with `product_id` - the costco.com page id, not the item number.

**Two ids, not one.** `item_number` is the number on the shelf tag and the receipt; `product_id` is the costco.com page id. Product, prices and availability accept either (or a product URL). Reviews takes `product_id` only.

### Pagination

- **Search, category and deals:** `page` (1-based, up to 500) and `page_size` (default 24, up to 120; up to 100 on uk, au, mx, jp, kr and tw). The response carries `total_results` and `total_pages`. Each page is 2 credits on `us` (1 on `ca` and elsewhere), so state the budget before looping.
- **Reviews:** `page` and `limit` (default 25, up to 100). Stop at `total_pages`.
- **Clearance:** `pages` is how many result pages of 120 to scan (default 3, up to 5); still one call: 2 credits on `us`, 1 on `ca`.
- **Product, prices, availability, warehouses, gas, coupons, categories, autocomplete:** no paging.

## Parameters

### Search (`/search`), Category (`/category`), Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required on search | Keywords, or a Costco item number (1-200 chars) |
| `category` | string | required on category | Category `slug` from `/categories` (e.g. `televisions`), or a costco.com category URL |
| `type` | string | required on deals | `new`, `while_supplies_last`, `treasure_hunt`, `member_favorites`, `online_only`, `on_sale` |
| `country` | string | `us` | `us`, `ca`; search also `uk`, `au`, `mx`, `jp`, `kr`, `tw` |
| `warehouse_id` | string | -- | Adds that warehouse's shelf price, stock status and price code to every row |
| `sort_by` | string | `best_match` | `best_match`, `price_low`, `price_high`, `top_rated`, `newest` |
| `brands` | string[] | -- | Brand names to keep, up to 20 (e.g. `["Kirkland Signature"]`) |
| `min_price` / `max_price` | number | -- | Online price bounds, inclusive |
| `min_rating` | number | -- | Minimum average star rating, 1-5 |
| `on_sale` | boolean | -- | Only items with an active discount |
| `in_stock` | boolean | -- | Hide out-of-stock items |
| `in_warehouse` | boolean | -- | Only items sold and in stock at `warehouse_id` (requires `warehouse_id`) |
| `page` | integer | 1 | 1-500 |
| `page_size` | integer | 24 | 1-120 |

On `uk`, `au`, `mx`, `jp`, `kr` and `tw`, sending `warehouse_id`, `brands`, a price or rating filter, `on_sale`, `in_stock` or `in_warehouse` is a `400`, and so is `sort_by: newest`.

### Categories (`/categories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | -- | Omit for the top-level departments; pass a numeric id (e.g. `30001`) for its full subcategory tree |
| `country` | string | `us` | `us` or `ca` |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string | one of | Item number, product id, or a costco.com product URL |
| `item_ids` | string[] | one of | Up to 20 ids in one call, mixed forms allowed (us and ca only) |
| `country` | string | `us` | `us`, `ca`, `uk`, `au`, `mx`, `jp`, `kr`, `tw`. Outside us/ca, one id per call |

### Prices (`/prices`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` / `item_ids` | string / string[] | one of | Same forms as product, up to 20 ids |
| `warehouse_ids` | string[] | required | 1-10 warehouse numbers. The online price is always included |
| `country` | string | `us` | `us` or `ca` |

### Availability (`/availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_number` | string | required | Item number, product id, or a costco.com product URL |
| `warehouse_ids` | string[] | required | 1-10 warehouse numbers |
| `country` | string | `us` | `us` or `ca` |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | The `product_id` field from search or product (not the item number) |
| `sort_by` | string | `newest` | `newest`, `oldest`, `highest_rating`, `lowest_rating`, `most_helpful` |
| `rating` | integer | -- | Only reviews with this star rating, 1-5 |
| `page` | integer | 1 | 1-based |
| `limit` | integer | 25 | Reviews per page, 1-100 |

### Warehouses (`/warehouses`) and Gas (`/gas`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | -- | US zip code. Outside the US, send coordinates instead |
| `latitude` / `longitude` | number | -- | Search center |
| `warehouse_ids` | string[] | -- | Gas only: 1-10 specific warehouses instead of a location |
| `limit` | integer | 10 | Nearest warehouses or stations to return, 1-50 |
| `country` | string | `us` | `us` or `ca`; warehouses also `uk`, `au`, `mx`, `jp`, `kr`, `tw` |

### Clearance (`/clearance`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `warehouse_id` | string | required | The warehouse whose shelf prices are checked |
| `query` | string | one of | What to scan (e.g. `snacks`) |
| `category` | string | one of | A category slug to scan instead of a query |
| `pages` | integer | 3 | Result pages of 120 to scan, 1-5 |
| `price_codes` | string[] | `["clearance", "manager_markdown"]` | Add `special_buy` for .49/.79/.89 endings, which are common on regular grocery prices |
| `country` | string | `us` | `us` or `ca` |

### Autocomplete (`/autocomplete`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Partial query, 1-100 chars (e.g. `kirk`) |
| `country` | string | `us` | `us` or `ca` |

### Coupons (`/coupons`)

No parameters. Send an empty JSON object: `{}`.

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/costco/prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "1492456", "warehouse_ids": ["1062", "1107"]}'
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def costco(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/costco/{endpoint}", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]

# 1. Nearest warehouses to a zip code
wh = costco("warehouses", {"zip": "10025", "limit": 5})
warehouse_id = wh["warehouses"][0]["warehouse_id"]          # "1062"

# 2. Search with that warehouse's shelf price on every row (2 credits on us)
found = costco("search", {"query": "olive oil", "warehouse_id": warehouse_id, "page_size": 5})
for row in found["results"]:
    shelf = row.get("warehouse") or {}
    print(row["title"], row["price"], shelf.get("price"), shelf.get("price_code"))

# 3. Online vs in-warehouse price at two warehouses (1 credit for up to 9)
prices = costco("prices", {"item_id": "1492456", "warehouse_ids": ["1062", "1107"]})
item = prices["items"][0]
print(item["online"]["final_price"], [(w["warehouse_id"], w["final_price"]) for w in item["warehouses"]])

# 4. Stock at the warehouse (status only, never a unit count)
stock = costco("availability", {"item_number": "1492456", "warehouse_ids": [warehouse_id]})

# 5. Reviews take product_id, not item_number
reviews = costco("reviews", {"product_id": "100334960", "sort_by": "lowest_rating", "limit": 25})
print(reviews["rating"]["average"], reviews["total_pages"])
```

Gas, coupons, deals and clearance:

```python
gas = costco("gas", {"zip": "90001", "limit": 5})
for s in gas["stations"]:
    print(s["name"], s["distance_miles"], s["prices"])          # regular / premium / diesel

book = costco("coupons", {})
print(book["valid_from"], book["valid_to"], book["count"])

deals = costco("deals", {"type": "while_supplies_last", "page_size": 5})

markdowns = costco("clearance", {"warehouse_id": "1062", "query": "snacks", "pages": 2})
for row in markdowns["results"]:
    print(row["title"], row["price"], row["warehouse"]["price"], row["warehouse"]["price_code"]["meaning"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. `fetched_at` is the ISO time the data was retrieved; nothing is cached, so it is the age of the data. Key `data` fields:

- **search / category / deals** - `country`, `query`, `category`, `redirected_to_category`, `corrected_query`, `warehouse_id`, `total_results`, `page`, `page_size`, `total_pages`, `count`, `results[]`, `facets[]` (deals also `type`).
  A row: `position`, `product_id`, `item_number`, `title`, `brand`, `categories`, `url`, `image`, `rating`, `reviews_count`, `price`, `original_price`, `on_sale`, `currency`, `delivery_availability`, `promotions`, `member_only`, `buyable`, `fsa_eligible`, `sold_in_warehouse`, `max_order_quantity`, `program_types`, `first_listed`, `variants_count`, and with `warehouse_id` a `warehouse` object (`warehouse_id`, `price`, `availability`, `price_code` {`ending`, `meaning`}).
- **product** - `country`, `count`, `not_found[]`, `products[]` (`product_id`, `item_number`, `id`, `title`, `url`, `image`, `description`, `features[]`, `specifications[]` {`name`, `value`}, `rating`, `reviews_count`, `price`, `currency`, `delivery_fee`, `promotions[]`, `member_only`, `buyable`, `fsa_eligible`, `limit_one_per_order`, `min_order_quantity`, `max_order_quantity`, `reviews_eligible`, `department`, `program_types`, `first_listed`, `variants[]`).
- **prices** - `country`, `count`, `items[]` (`item_number`, `found`, `online` {`price`, `discount`, `final_price`, `currency`, `promotions[]`}, `warehouses[]` {`warehouse_id`, `available`, `price`, `discount`, `final_price`, `currency`, `promotions[]`, `price_code`}). A promotion: `promotion_id`, `type`, `amount_off`, `start_date`, `end_date`, `order_limit`, `member_limit`, `text`.
- **availability** - `item_number`, `count`, `warehouses[]` (`warehouse_id`, `in_warehouse`, `channels` {`in_warehouse`, `warehouse_pickup`, `same_day_delivery`}, each with `status`). Status values: `in_stock`, `low_stock`, `out_of_stock`, `not_available`, and `no_record` when Costco keeps no stock record for the item at that warehouse (common for warehouse-only items; `channels` is then `{}`).
- **reviews** - `product_id`, `product_title`, `rating` {`average`, `count`, `recommended_count`, `distribution`}, `total_results`, `page`, `limit`, `total_pages`, `count`, `reviews[]` (`review_id`, `rating`, `title`, `text`, `author`, `location`, `submitted_at`, `recommended`, `verified_purchaser`, `helpful_votes`, `not_helpful_votes`, `photos`, `language`, `syndicated`).
- **warehouses** - `country`, `location`, `count`, `warehouses[]` (`warehouse_id`, `name`, `address`, `phone`, `latitude`, `longitude`, `distance_miles`, `opened`, `region`, `hours`, `business_hours`, `pharmacy_hours`, `tire_center_hours`, `gas_station` {`hours`, `prices`} or null, `departments`, `services`, `specialty_departments`, `warehouse_pickup`, `ship_to_warehouse`, `upcoming_holidays`, `currency`).
- **gas** - `country`, `currency`, `location`, `count`, `stations[]` (`warehouse_id`, `name`, `address`, `latitude`, `longitude`, `distance_miles`, `prices` {`regular`, `premium`, `diesel`}, `hours`).
- **coupons** - `country`, `valid_from`, `valid_to`, `count`, `coupons[]` (`title`, `item_number`, `product_id`, `discount` {`amount_off`, `final_price`, `text`}, `applies_to`, `coupon_type`, `limits`, `details`, `terms`, `url`).
- **clearance** - `country`, `warehouse_id`, `query`, `category`, `products_scanned`, `count`, `results[]` (search rows with `warehouse`), `price_code_legend`, `note`.
- **categories** - `parent_category_id`, `count`, `categories[]` (`category_id`, `name`, `slug`).
- **autocomplete** - `query`, `suggestions[]`, `warehouses[]` (`warehouse_id`, `name`, `address`, `city`, `state`, `zip`, `country`).

A prices response (captured, item 1492456 at warehouse 1062):

```json
{
  "data": {
    "country": "us",
    "count": 1,
    "items": [
      {
        "item_number": "1492456",
        "found": true,
        "online": {
          "price": 20.99,
          "discount": 4,
          "final_price": 16.99,
          "currency": "USD",
          "promotions": [
            {
              "amount_off": 4,
              "start_date": "2026-09-28T07:00:00Z",
              "end_date": "2026-10-12T06:59:00Z",
              "order_limit": null,
              "member_limit": 6
            }
          ]
        },
        "warehouses": [
          {
            "warehouse_id": "1062",
            "available": true,
            "price": 17.99,
            "discount": 4,
            "final_price": 13.99,
            "currency": "USD",
            "price_code": { "ending": "99", "meaning": "regular_price" }
          }
        ]
      }
    ]
  }
}
```

A search row with `warehouse_id` (captured, "olive oil" at warehouse 1062):

```json
{
  "position": 1,
  "product_id": "100334841",
  "item_number": "692731",
  "title": "Kirkland Signature, Organic Extra Virgin Olive Oil, 2 L",
  "brand": "Kirkland Signature",
  "rating": 4.8,
  "reviews_count": 6484,
  "price": 20.99,
  "currency": "USD",
  "url": "https://www.costco.com/p/-/kirkland-signature-organic-extra-virgin-olive-oil-2-l/100334841",
  "warehouse": {
    "warehouse_id": "1062",
    "price": 15.59,
    "availability": "in_stock",
    "price_code": { "ending": "59", "meaning": "other" }
  }
}
```

### Price codes

`price_code` reads the cents of the warehouse shelf price: `99` regular_price, `97` clearance, `00` and `88` manager_markdown, `49`/`79`/`89` special_buy, anything else `other`. It is the decode Costco members use for shelf tags; Costco does not publish it, so treat it as a strong hint, not a guarantee. It is computed from the warehouse price only, never the online price.

## Guardrails

- `price` on search rows and `online` on prices is the costco.com (or costco.ca) online price. The warehouse shelf price is `warehouse.price` / `warehouses[].price`, and it is often lower. Never present one as the other.
- Availability is a status per warehouse (`in_stock`, `low_stock`, `out_of_stock`, `not_available`, `no_record`), never a quantity. Do not invent unit counts. `no_record` is not out of stock: say Costco has no stock data for it there, and use `/costco/prices` to check whether that warehouse prices the item.
- Clearance covers only items Costco lists online; warehouse-only items with no costco.com page cannot appear. A clearance item can already be `out_of_stock` at that warehouse - report `warehouse.availability` with it.
- `special_buy` endings are common on regular grocery prices, so they are off by default in clearance. Add them only when the user asks.
- Reviews take `product_id`, which is a different number from the item number. Get it from search or product first.
- Coupons are US only and take no parameters; the whole book is 1 credit.
- Non-default `sort_by` values broaden matching on Costco's side, so results can look less relevant than `best_match`.
- Multi-warehouse calls cost more: prices at 10 warehouses is 2 credits, availability is 1 per 5 warehouses, gas by `warehouse_ids` on costco.ca is 2 per warehouse. State the spend before fanning out.
- Never fabricate item numbers, prices, stock, gas prices or coupon terms. Only return what the API returned, and surface the product `url` so the user can verify.

## Failure handling

- `400` means an invalid or missing parameter (no `query`, `in_warehouse` without `warehouse_id`, more than 10 `warehouse_ids`, a us/ca-only filter on another country, an unknown US zip) - fix the body and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means none of the ids matched anything; that call is billed. When some ids match, the rest are listed in `not_found[]` and the call succeeds.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data).
- `502` / `503` mean Costco data is temporarily unavailable - wait a few seconds and retry, up to a few times.
- If search returns nothing, drop the filters or try broader keywords.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.18.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

wh = client.costco.warehouses(zip="10025", limit=5)
found = client.costco.search("olive oil", warehouse_id="1062", page_size=5)
prices = client.costco.prices(item_id="1492456", warehouse_ids=["1062", "1107"])
gas = client.costco.gas(zip="90001", limit=5)
book = client.costco.coupons()
markdowns = client.costco.clearance(warehouse_id="1062", query="snacks")
```

```bash
npm install scavio@0.18.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const found = await scavio.costco.search({ query: "olive oil", warehouse_id: "1062", page_size: 5 });
const prices = await scavio.costco.prices({ item_id: "1492456", warehouse_ids: ["1062", "1107"] });
const book = await scavio.costco.coupons();
```

MCP: the Scavio MCP server exposes all 13 endpoints as tools (`search_costco`, `get_costco_prices`, `get_costco_availability`, `get_costco_gas_prices`, `get_costco_coupons`, `get_costco_clearance` and the rest). Costco is opt-in: add `costco` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.16.1"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,costco"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [Costco search](https://scavio.dev/docs/costco-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data), [prices](https://scavio.dev/docs/costco-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data), [availability](https://scavio.dev/docs/costco-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data), [gas](https://scavio.dev/docs/costco-gas?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data), [coupons](https://scavio.dev/docs/costco-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data), [clearance](https://scavio.dev/docs/costco-clearance?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data). Overview: [Costco API](https://scavio.dev/costco-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data).
