---
name: ulta-beauty-api
description: "Ulta Beauty API: search ulta.com or list a category with list and sale price, discount, promo text, rating and review count, read one product with every shade or size, GTIN, ingredients and the five latest reviews, and check whether one shade is in stock for pickup at the 10 Ulta stores nearest a ZIP. 4 endpoints, 1 credit each."
version: 1.0.0
tags: ulta, ulta-beauty, ulta-api, ulta-beauty-api, beauty, cosmetics, makeup, skincare, hair-care, shades, beauty-prices, store-inventory, in-store-stock, store-pickup, product-search, product-data, category-listing, retail, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/ulta-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api
---

# Ulta Beauty API - Search, Prices, Shades, Store Stock

Search Ulta Beauty and list any category: list and sale price, discount, promo text, rating, review count, badge and shade count, 64 products per page. Read one product for the shade or size you pick, with every variant, GTIN, ingredients, ship, pickup and same-day options and the five most recent reviews. Check whether one shade is in stock for pickup at the 10 Ulta stores nearest a ZIP. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find makeup, skincare, hair care or fragrance at Ulta Beauty by keyword
- List the products in an Ulta category (lipstick, mascara, shampoo) with prices and ratings
- Check an Ulta product's price, sale price and discount, or what is on sale
- List the shades or sizes of a product and which are available
- Find which Ulta stores near a ZIP have a shade in stock for pickup
- Read the latest Ulta reviews, ingredients or usage for a product
- Look up a product's GTIN (UPC)
- Compare Ulta prices with Sephora or other retailers, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All Ulta Beauty endpoints cost **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/ulta/search` | 1 | 64 products per page plus sponsored placements: product id, sku id, brand, name, URL, image, list and sale price (and the range when shades are priced differently), discount, promo text, rating, review count, badge, shade count, limited-stock and sponsored flags |
| `POST /api/v1/ulta/category` | 1 | One category's products in the same shape, with the category title and total results |
| `POST /api/v1/ulta/product` | 1 | One product for the selected shade or size: list and sale price, discount, availability, GTIN, rating, review count, badges, summary, description, usage, ingredients, restrictions, category and breadcrumbs, images, every shade or size variant, ship / pickup / same-day options, and the five most recent reviews |
| `POST /api/v1/ulta/stores` | 1 | In-store pickup stock of one shade at the 10 Ulta stores nearest a ZIP: store id, name, address, distance, open-now label, curbside label, `in_stock` and the availability label |

## Workflow

1. **Find products:** call `/ulta/search` with `query`, or `/ulta/category` with a category path like `/shop/makeup/lips/lipstick`. Each row has a `url`, a `product_id` and a `sku_id`.
2. **One product in full:** call `/ulta/product` with the row's `url`. Add `sku` to pick a shade or size; `variants[]` lists every one with its `sku_id`.
3. **Who has it nearby:** call `/ulta/stores` with the `product_id`, the shade's `sku_id` and the user's `zip`. Stock is per shade, so pass the exact `sku_id` the user wants.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars) |
| `page` | integer | 1 | 1-based page (1-100), 64 products per page plus sponsored placements |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category` | string | required | An ulta.com category that lists products: the full URL, or its path (`/shop/makeup/lips/lipstick` or `makeup/lips/lipstick`) |
| `page` | integer | 1 | 1-based page (1-100), 64 products per page plus sponsored placements |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | required | Ulta product page URL, `/p/<name>-<productId>` (the `url` of a search or category row). The name part is required |
| `sku` | string | URL's `?sku=`, else the default | Shade or size to select, by sku id (a `variants[].sku_id`) |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | Ulta product id, e.g. `pimprod2057119` |
| `sku_id` | string | required | Sku id of the shade or size, a `sku_id` or `variants[].sku_id` |
| `zip` | string | required | US ZIP code to search around |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/ulta/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "pimprod2057119", "sku_id": "2648428", "zip": "10001"}'
```

Captured response (Maybelline Serum Lipstick near Manhattan 10001; trimmed to 3 of 10 stores):

```json
{
  "data": {
    "product_id": "pimprod2057119",
    "sku_id": "2648428",
    "zip": "10001",
    "count": 10,
    "in_stock_count": 7,
    "stores": [
      {
        "store_id": "1638",
        "name": "2 Herald Square",
        "address": "51 West 34th Street, Suite 110, New York, NY 10001",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "distance_miles": 0.17,
        "is_open": true,
        "open_label": "Open until 8:00 pm",
        "curbside_label": null,
        "in_stock": false,
        "availability": "Out of Stock"
      },
      {
        "store_id": "1899",
        "name": "Ulta Beauty",
        "address": "620 Avenue of the Americas, Ste 0105, New York, NY 10011",
        "city": "New York",
        "state": "NY",
        "zip": "10011",
        "distance_miles": 0.63,
        "is_open": true,
        "open_label": "Open until 7:00 pm",
        "curbside_label": null,
        "in_stock": true,
        "availability": "In Stock"
      },
      {
        "store_id": "1402",
        "name": "Upper East Side",
        "address": "188 East 86th Street, New York, NY 10028",
        "city": "New York",
        "state": "NY",
        "zip": "10028",
        "distance_miles": 2.81,
        "is_open": true,
        "open_label": "Open until 7:00 pm",
        "curbside_label": null,
        "in_stock": true,
        "availability": "In Stock"
      }
    ]
  },
  "response_time": 3096,
  "credits_used": 1
}
```

A captured `/product` answer for the same product (summary, description, ingredients, images, breadcrumbs trimmed; 2 of 16 variants, 1 of 5 reviews):

```json
{
  "product_id": "pimprod2057119",
  "sku_id": "2648428",
  "name": "Serum Lipstick",
  "brand": "Maybelline",
  "url": "https://www.ulta.com/p/serum-lipstick-pimprod2057119?sku=2648428",
  "variant_label": "Crop Top (light nude pink)",
  "variant_type": "Color",
  "size": "0.12 oz",
  "list_price": 9.99,
  "list_price_range": null,
  "sale_price": 4.99,
  "sale_price_range": null,
  "discount": 5,
  "currency": "USD",
  "availability": "InStock",
  "gtin": "041554100051",
  "rating": 4.7,
  "review_count": 431,
  "questions_count": 1,
  "badges": ["Sale"],
  "category": "Makeup:Lips:Lipstick",
  "variants": [
    { "sku_id": "2648432", "name": "Avenue A", "shade_description": "deep chocolate brown", "selected": false, "available": true, "out_of_stock_label": null },
    { "sku_id": "2648514", "name": "Blind Date", "shade_description": "midtone bricky mauve", "selected": false, "available": true, "out_of_stock_label": null }
  ],
  "fulfillment": {
    "ship": { "eligibility": "in_stock", "state": "active", "label": "Free standard shipping over $35", "message": "In stock and ready to ship", "stock_status": null, "speed": "Usually ships in 24 hours" },
    "pickup": { "eligibility": "change_store", "state": "unavailable", "label": "Unavailable", "message": null, "stock_status": null, "speed": null },
    "same_day": { "eligibility": "change_address", "state": "active", "label": "Delivered for $6.95", "message": "Check your address to view availability", "stock_status": null, "speed": "Get by 8PM today if ordered before 4PM" }
  },
  "recent_reviews": [
    { "title": "i wouldn't say matte, but its ok", "body": "glides on and king lasting... a little greasy looking. which i personally do not care for.  I layer with lip liners to achieve the look I want. It does stay on! so that's good", "rating": 3, "date": "2026-10-27", "author": "Vanessa", "location": "ai" }
  ]
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def ulta(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/ulta/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Search, organic results only, one row per product
rows = [p for p in ulta("search", {"query": "lipstick"})["products"] if not p["sponsored"]]
top = rows[0]
print(top["brand"], top["name"], top["list_price"], "sale", top["sale_price"])

# 2. The product and its shades
item = ulta("product", {"url": top["url"]})
shade = next(v for v in item["variants"] if v["available"])

# 3. Which nearby stores have that shade for pickup
near = ulta("stores", {"product_id": item["product_id"], "sku_id": shade["sku_id"], "zip": "10001"})
for s in near["stores"]:
    if s["in_stock"]:
        print(shade["name"], "at", s["name"], s["address"], s["distance_miles"], "mi")
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Ulta Beauty answered.

- **search / category** - `query` (search) or `category`, `title`, `url` (category), `page`, `page_size`, `total_results`, `total_pages`, `count`, `sponsored_count`, `has_more`, `products[]` (`position`, `product_id`, `sku_id`, `brand`, `name`, `url`, `image`, `list_price`, `list_price_range`, `sale_price`, `sale_price_range`, `discount`, `promo_text`, `rating`, `review_count`, `badge`, `variant_label`, `is_limited_stock`, `sponsored`).
- **product** - `product_id`, `sku_id`, `name`, `brand`, `url`, `variant_label`, `variant_type`, `size`, `list_price`, `list_price_range`, `sale_price`, `sale_price_range`, `discount`, `currency`, `availability`, `gtin`, `rating`, `review_count`, `questions_count`, `badges[]`, `summary`, `description`, `usage`, `ingredients`, `restrictions`, `category`, `category_path[]`, `breadcrumbs[]` {`label`, `url`}, `images[]`, `variants[]` {`sku_id`, `name`, `shade_description`, `selected`, `available`, `out_of_stock_label`, `image`, `swatch`}, `fulfillment` {`ship`, `pickup`, `same_day`: {`eligibility`, `state`, `label`, `message`, `stock_status`, `speed`}}, `recent_reviews[]` {`title`, `body`, `rating`, `date`, `author`, `location`}.
- **stores** - `product_id`, `sku_id`, `zip`, `count`, `in_stock_count`, `stores[]` (`store_id`, `name`, `address`, `city`, `state`, `zip`, `distance_miles`, `is_open`, `open_label`, `curbside_label`, `in_stock`, `availability`).

## Guardrails

- Prices are in dollars: `9.99` is $9.99. `discount` is a dollar amount off, not a percentage: `5` is $5 off.
- When shades are priced differently, `list_price` / `sale_price` are the low end and `list_price_range` / `sale_price_range` hold the range as shown ("$4.99 - $9.99"). Quote the range, or call `/product` with the shade's `sku` for one exact price.
- `sale_price` is `null` when the item is not on sale; the price paid is then `list_price`.
- Listing pages carry sponsored placements on top of the 64 organic cards (`count` can be 73), and they can repeat products from other pages. Filter on `sponsored` and dedupe by `product_id` when merging pages.
- `/stores` reports In Stock or Out of Stock per store for pickup; Ulta does not publish unit counts. Never quote a quantity.
- Store stock is per shade: a store can have one shade and not another, so always check the exact `sku_id`.
- `recent_reviews` are the five most recent reviews the product page shows; there is no endpoint that pages older reviews.
- Never fabricate prices, shades or stock. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, a `url` or `category` that is not on ulta.com, a non-numeric `sku` or `sku_id`, a `product_id` not like `pimprod2057119`, or an unknown ZIP).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means no such product, or a URL without its name part (`/p/<productId>` alone). `404` on `/category` means a path with no product grid, such as the `/shop/makeup` landing page; use a deeper path. `404` on `/stores` means no Ulta store near that ZIP. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api).
- `502` means Ulta Beauty is temporarily unavailable. It is not charged; retry after a few seconds.

## SDKs

```bash
pip install scavio==0.32.0
npm install scavio@0.32.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.ulta.search({ query: "lipstick" });
const lips = await scavio.ulta.category({ category: "/shop/makeup/lips/lipstick" });
const { data: item } = await scavio.ulta.product({ url: found.products[0].url });
const near = await scavio.ulta.stores({ product_id: item.product_id, sku_id: item.sku_id, zip: "10001" });
```

MCP: the Scavio MCP server exposes all 4 endpoints as tools (`search_ulta`, `get_ulta_category`, `get_ulta_product`, `get_ulta_stores`). Ulta Beauty is opt-in: add `ulta` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.30.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,ulta"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/ulta-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api), [category](https://scavio.dev/docs/ulta-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api), [product](https://scavio.dev/docs/ulta-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api), [stores](https://scavio.dev/docs/ulta-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api). Overview: [Ulta Beauty API](https://scavio.dev/ulta-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api).
