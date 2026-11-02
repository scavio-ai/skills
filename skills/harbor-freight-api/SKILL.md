---
name: harbor-freight-api
description: "Harbor Freight API: search harborfreight.com or list clearance with the national price, sale price and end date, public coupon price, Inside Track member price and competitor compare-at price, read one product with UPC, specs and manuals, batch prices for up to 50 items, find stores near a ZIP, check in-stock, limited or out-of-stock status and aisle for up to 20 items at nearby stores, and page customer reviews. 7 endpoints, 1 credit each."
version: 1.0.0
tags: harbor-freight, harborfreight, harbor-freight-api, tools, power-tools, hand-tools, automotive, coupons, member-prices, inside-track-club, clearance, store-inventory, in-store-stock, aisle-location, product-search, product-data, product-reviews, store-locator, retail, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/harborfreight-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api
---

# Harbor Freight API - Prices, Coupons, Store Stock, Reviews

Search Harbor Freight tools and equipment by keyword, category and brand, or list what is on clearance, with the national price, the sale price and when it ends, the public coupon price, the Inside Track Club member price and the competitor price Harbor Freight compares against. Read one product with UPC, the full specification table, warranty, owner's manuals and variants; get current prices for up to 50 item numbers in one call; find stores near a ZIP or city; check whether up to 20 items are in stock, limited or out of stock, and in which aisle, at chosen or nearby stores; and page customer reviews. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find tools or equipment at Harbor Freight by keyword, category or brand (BAUER, HERCULES, PITTSBURGH, WARRIOR)
- Check a Harbor Freight item's price, sale price and end date, coupon price or Inside Track member price
- List Harbor Freight clearance items and their clearance prices
- Check whether nearby Harbor Freight stores have an item, and which aisle it is in
- Find Harbor Freight stores near a ZIP code, city or coordinates
- Read an item's specifications, warranty, UPC or owner's manual, or its customer reviews
- Watch prices for a list of item numbers, or compare Harbor Freight with Home Depot, Lowe's or other retailers

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All Harbor Freight endpoints cost **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/harborfreight/search` | 1 | Up to 48 products per page by keyword and/or category, with brand and clearance filters and 7 sorts: item number, id, title, brand, URL, image, price, regular price, sale (price, end date, savings), coupon, member deal, compare-at, badges, rating, review count, where it sells, variants. Category, brand, rating, price and attribute facets |
| `POST /api/v1/harborfreight/clearance` | 1 | Clearance items, optionally narrowed by keyword, category or brand. Same row fields as search; the clearance price and end date are in `sale` |
| `POST /api/v1/harborfreight/product` | 1 | One product by item number, id or URL: UPC, every price field, rating, review count, badges, summary, description, highlights, full specification table, warranty, shipping notes, owner's manuals, images and variants |
| `POST /api/v1/harborfreight/prices` | 1 | Current price fields for up to 50 item numbers in one call. Unknown item numbers are listed in `not_found` |
| `POST /api/v1/harborfreight/stores` | 1 | Stores near a ZIP, "City, ST" or coordinates, nearest first: store number, name, address, phone, coordinates, distance, status, opening date and hours |
| `POST /api/v1/harborfreight/availability` | 1 | In-store stock for up to 20 items at up to 20 chosen stores, or at the stores nearest a ZIP or coordinates: per store and item the stock status (in_stock, limited, out_of_stock, not_carried), aisle, and a nearby store that has it |
| `POST /api/v1/harborfreight/reviews` | 1 | Customer reviews for one item, newest first, paged with `limit`/`offset`: title, text, star rating, author, review and purchase dates, incentivized flag, helpful votes and the reviewer's answers. Also the average rating and total review count |

## Workflow

Prices are national: every store charges the same. The store only matters for stock and aisle.

1. **Find the item:** call `/harborfreight/search` with `query` (or `category_id`). Each row has a `sku` (the Harbor Freight item number, like `73216`) and an `id`.
2. **One product in full:** call `/harborfreight/product` with the `sku` for specifications, manuals and variants.
3. **Who has it:** call `/harborfreight/availability` with the `skus` and the user's `zip`. One call returns the nearest stores (10 by default, up to 100) with each item's status and aisle. To watch specific stores, call `/harborfreight/stores` first and pass up to 20 `store_ids`.
4. **Watch prices:** call `/harborfreight/prices` with up to 50 `skus`. This is the cheap way to track a list of items, their sales and coupons.
5. **Markdowns:** call `/harborfreight/clearance`, optionally with `query` or `category_id`.
6. **What buyers say:** call `/harborfreight/reviews` with the `sku`, paging with `offset`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Keywords (1-200 chars). Pass this, `category_id`, or both |
| `category_id` | string | one of | Numeric category id, e.g. `1827` (Drills, Drivers & Drill Presses): the `value` of an option in the `category` facet |
| `brand` | string | - | Only this brand, as listed in the `brand` facet (`BAUER`, `HERCULES`, `PITTSBURGH`). Case-insensitive |
| `clearance` | boolean | false | Only clearance items |
| `sort` | string | `best_match` | `best_match`, `price_low`, `price_high`, `member_price_low`, `member_price_high` (Inside Track Club price), `top_rated` or `newest` |
| `page` | integer | 1 | 1-based page (1-100) |
| `page_size` | integer | 36 | Results per page, 1-48 |

### Clearance (`/clearance`)

Same parameters as search, all optional (`query`, `category_id`, `brand`, `sort`, `page`, `page_size`). With none, it lists all clearance items.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | one of | Harbor Freight item number (3-8 digits), a search row's `sku` |
| `id` | integer | one of | Numeric product id, a search row's `id` |
| `url` | string | one of | harborfreight.com product URL ending in the item number, `https://www.harborfreight.com/<name>-73216.html` |

### Prices (`/prices`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `skus` | string[] | required | 1-50 Harbor Freight item numbers |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | 5-digit US ZIP code or "City, ST" (`"Los Angeles, CA"`) |
| `latitude`, `longitude` | number | one of | Coordinates to search around, instead of `query` |
| `radius` | integer | 50 | Search radius in miles, 1-100 |
| `limit` | integer | 10 | Most stores to return, 1-50 |

### Availability (`/availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `skus` | string[] | required | 1-20 Harbor Freight item numbers |
| `store_ids` | string[] | one of | 1-20 store numbers, the `store_id` values from `/stores` |
| `zip` | string | one of | US ZIP code: stock at the stores nearest to it |
| `latitude`, `longitude` | number | one of | Coordinates: stock at the stores nearest to them |
| `limit` | integer | 10 | Nearest stores to return with `zip` or coordinates, 1-100 |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | required | Harbor Freight item number |
| `limit` | integer | 10 | Reviews per call, 1-50 |
| `offset` | integer | 0 | Reviews to skip, for paging |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/harborfreight/availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"skus": ["73216"], "zip": "90012", "limit": 5}'
```

Captured response (a BAUER 20V drill kit at the five stores nearest downtown Los Angeles; two stores trimmed, the out-of-stock one kept):

```json
{
  "data": {
    "skus": ["73216"],
    "store_ids": null,
    "zip": "90012",
    "latitude": 34.066,
    "longitude": -118.239,
    "inventory_updated_at": "2026-11-01 17:17:07",
    "total_stores": 95,
    "count": 5,
    "stores": [
      {
        "store_id": "3060",
        "name": "Los Angeles, CA",
        "address": "2619 N Figueroa St",
        "city": "Los Angeles",
        "state": "CA",
        "zip": "90065",
        "phone": "747-286-7600",
        "distance_miles": 1.61,
        "status": "OPEN",
        "hours": { "monday_friday": "8:00AM-8:00PM", "saturday": "8:00AM-8:00PM", "sunday": "9:00AM-6:00PM" },
        "items": [
          { "sku": "73216", "stock_status": "in_stock", "stock_code": "IS", "aisle": "Aisle 1", "nearby_store_with_stock": null }
        ]
      },
      {
        "store_id": "3224",
        "name": "Hollywood, CA",
        "address": "5711 Hollywood Blvd",
        "city": "Hollywood",
        "state": "CA",
        "zip": "90028",
        "phone": "213-374-2626",
        "distance_miles": 4.98,
        "status": "OPEN",
        "hours": { "monday_friday": "8:00AM-8:00PM", "saturday": "8:00AM-8:00PM", "sunday": "9:00AM-6:00PM" },
        "items": [
          {
            "sku": "73216",
            "stock_status": "out_of_stock",
            "stock_code": "NS",
            "aisle": "Aisle 1",
            "nearby_store_with_stock": { "store_id": "3654", "stock_status": "in_stock" }
          }
        ]
      }
    ]
  },
  "response_time": 2354,
  "credits_used": 1
}
```

A captured `/prices` row for `{"skus": ["73216", "59716", "64508"]}`, with an Inside Track member deal:

```json
{
  "sku": "59716",
  "id": 30724,
  "title": "9 Amp, 1/2 in. Variable-Speed D-Handle Drill",
  "brand": "BAUER",
  "url": "https://www.harborfreight.com/9-amp-12-in-variable-speed-d-handle-drill-59716.html",
  "price": 59.99,
  "regular_price": 59.99,
  "on_sale": false,
  "clearance": false,
  "sale": null,
  "coupon": null,
  "member_deal": {
    "code": "32457254",
    "price": 42.99,
    "was_price": 59.99,
    "savings": "28%",
    "expires": "2026-12-03",
    "limit": 2,
    "members_only": true
  },
  "compare_at": { "brand": "RIDGID", "model": "R71111", "price": 139, "savings": "$79.01" },
  "badges": [],
  "sold_in": "Store",
  "in_store_only": true,
  "online_only": false
}
```

A captured `/clearance` row for `{"query": "drill"}` (image trimmed):

```json
{
  "position": 1,
  "id": 12112,
  "sku": "63443",
  "title": "7.3 Amp, 1 in. SDS-PLUS Type Variable-Speed Rotary Hammer",
  "brand": "BAUER",
  "category": "Power Tools",
  "url": "https://www.harborfreight.com/73-amp-1-in-sds-plus-type-variable-speed-rotary-hammer-63443.html",
  "price": 39.97,
  "regular_price": 49.97,
  "on_sale": true,
  "clearance": true,
  "sale": { "price": 39.97, "ends_at": "2026-12-03 23:59:59", "savings": "20%", "banner_code": "CLR", "clearance": true },
  "coupon": null,
  "member_deal": null,
  "compare_at": null,
  "badges": [],
  "rating": 4.6,
  "review_count": 1528,
  "sold_in": "Store",
  "in_store_only": true,
  "online_only": false,
  "variants": null
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def hf(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/harborfreight/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Find the item (1 credit). A keyword that maps to a category can come back
#    with no rows and a redirect; retry with a category_id from the facets.
found = hf("search", {"query": "impact wrench", "sort": "top_rated"})
if not found["products"] and found["redirect"]:
    cats = next(f for f in found["facets"] if f["name"] == "category")["options"]
    found = hf("search", {"category_id": cats[0]["value"], "sort": "top_rated"})
row = found["products"][0]
member = row["member_deal"]["price"] if row["member_deal"] else None
print(row["sku"], row["title"], row["price"], "member:", member)

# 2. Status and aisle at the 10 stores nearest a ZIP (1 credit)
stock = hf("availability", {"skus": [row["sku"]], "zip": "60601"})
for s in stock["stores"]:
    it = s["items"][0]
    print(s["name"], s["distance_miles"], "mi:", it["stock_status"], it["aisle"])

# 3. Recent reviews (1 credit)
for rv in hf("reviews", {"sku": row["sku"], "limit": 5})["reviews"]:
    print(rv["rating"], rv["title"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Harbor Freight answered.

Price block (on every search, clearance, prices and product row): `price`, `regular_price`, `on_sale`, `clearance`, `sale` {`price`, `ends_at`, `savings`, `banner_code`, `clearance`} or null, `coupon` {`code`, `price`, `was_price`, `savings`, `expires`, `limit`, `members_only`} or null, `member_deal` (same shape as `coupon`) or null, `compare_at` {`brand`, `model`, `price`, `savings`} or null.

- **search / clearance** - `query`, `category_id`, `brand`, `clearance`, `sort`, `page`, `page_size`, `corrected_query`, `redirect` {`url`, `category_id`, `category_name`} or null, `total_results`, `total_pages`, `count`, `products[]` (`position`, `id`, `sku`, `title`, `brand`, `category`, `url`, `image`, price block, `badges[]`, `rating`, `review_count`, `sold_in`, `in_store_only`, `online_only`, `variants` {`name`, `options[]`, `count`} or null), `facets[]` {`name`, `type`, `options[]` {`label`, `value`, `count`}}.
- **product** - `id`, `sku`, `title`, `brand`, `upc`, `category`, `url`, price block, `badges[]`, `rating`, `review_count`, `sold_in`, `in_store_only`, `online_only`, `online_only_message`, `summary`, `description`, `highlights[]`, `specifications[]` {`label`, `value`}, `warranty`, `shipping_notes[]`, `manuals[]` {`title`, `url`}, `images[]`, `variants` {`options[]`, `items[]` {`id`, `sku`, `url`, `attributes[]`}} or null.
- **prices** - `count`, `not_found[]`, `products[]` (`sku`, `id`, `title`, `brand`, `url`, price block, `badges[]`, `sold_in`, `in_store_only`, `online_only`).
- **stores** - `query`, `latitude`, `longitude`, `radius_miles`, `count`, `stores[]` (`store_id`, `name`, `address`, `city`, `state`, `zip`, `latitude`, `longitude`, `phone`, `distance_miles`, `status`, `opened`, `hours` {`monday_friday`, `saturday`, `sunday`}).
- **availability** - `skus[]`, `store_ids`, `zip`, `latitude`, `longitude`, `inventory_updated_at`, `total_stores`, `count`, `stores[]` (every store field above plus `items[]` {`sku`, `stock_status`, `stock_code`, `aisle`, `nearby_store_with_stock` {`store_id`, `stock_status`} or null}).
- **reviews** - `sku`, `average_rating`, `total_results`, `offset`, `limit`, `count`, `reviews[]` (`id`, `title`, `text`, `rating`, `author`, `date`, `purchase_date`, `incentivized`, `helpful_votes`, `unhelpful_votes`, `answers[]` {`question`, `answers[]`}).

## Guardrails

- Prices are in dollars and national: `59.99` is $59.99 at every store. No endpoint takes a store for price, so never claim a store-specific price.
- `price` is what the shelf charges now (the sale price while a sale runs); `regular_price` is the list price. `sale` carries the sale price, `ends_at` and `savings`; `banner_code` `CLR` means clearance. On many clearance items `regular_price` already equals the clearance price and `sale.savings` is `"0"`.
- `coupon` is the public coupon price with its code, expiry and per-customer `limit`. `member_deal` is the Inside Track Club member price and needs a paid membership; say so when quoting it. Neither is applied to `price`; quote them separately and do not stack them into a final price.
- `compare_at` is the competitor brand, model and price Harbor Freight itself quotes on the page, not a live price from that retailer. `savings` is Harbor Freight's text (`"39%"` or `"$79.01"`).
- Store stock is a status, never a unit count: `in_stock`, `limited`, `out_of_stock` (the site reads "Back In Stock Soon") or `not_carried` (the store does not sell it; an aisle can still appear). Never turn a status into a number.
- Stock comes from a daily snapshot: `inventory_updated_at` is when it was taken. Quote it with the status, and tell the user to confirm with the store for same-day plans.
- `/availability` with `zip` or coordinates returns the nearest stores (`limit`, default 10) out of `total_stores` within about 200 miles. With `store_ids`, unknown store numbers are simply absent from `stores`.
- A keyword that maps to a category page (e.g. "wrench") follows that category: `redirect.category_id` is set and the rows are the category's. If `redirect` is set with `category_id: null`, `products` is empty even though `total_results` is not 0; retry with a `category_id` from the `category` facet or a narrower keyword.
- `sold_in` is where it sells (`Store`, `All`, `DTC`); `in_store_only: true` items cannot be shipped.
- The product's `review_count` and the reviews endpoint's `total_results` can differ by a few reviews; quote the one from the call you made.
- Never fabricate prices, stock, aisles or reviews. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (neither `query` nor `category_id` on search, an item number that is not 3-8 digits, a URL without the item number, an unknown `sort`, `page_size` above 48, more than 50 `skus` on prices or 20 on availability, more than 20 `store_ids`, a ZIP that is not 5 digits, or a stores `query` that is neither a ZIP nor "City, ST").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` or `/reviews` means no such item number; re-run the search for a fresh `sku`. Not charged. On `/prices` unknown item numbers are not an error: they come back in `not_found`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api).
- `502` or `503` means Harbor Freight is temporarily unavailable. It is not charged; retry after a few seconds.

## SDKs

```bash
pip install scavio==0.33.0
npm install scavio@0.33.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.harborFreight.search({ query: "floor jack", sort: "price_low" });
const sku = found.products[0].sku;
const item = await scavio.harborFreight.product({ sku });
const stock = await scavio.harborFreight.availability({ skus: [sku], zip: "60601" });
const prices = await scavio.harborFreight.prices({ skus: found.products.slice(0, 50).map((p) => p.sku) });
```

MCP: the Scavio MCP server exposes all 7 endpoints as tools (`search_harbor_freight`, `get_harbor_freight_clearance`, `get_harbor_freight_product`, `get_harbor_freight_prices`, `get_harbor_freight_stores`, `get_harbor_freight_availability`, `get_harbor_freight_reviews`). Harbor Freight is opt-in: add `harborfreight` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.31.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,harborfreight"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/harborfreight-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api), [clearance](https://scavio.dev/docs/harborfreight-clearance?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api), [product](https://scavio.dev/docs/harborfreight-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api), [prices](https://scavio.dev/docs/harborfreight-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api), [stores](https://scavio.dev/docs/harborfreight-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api), [availability](https://scavio.dev/docs/harborfreight-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api), [reviews](https://scavio.dev/docs/harborfreight-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api). Overview: [Harbor Freight API](https://scavio.dev/harborfreight-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api).
