---
name: heb-grocery-data
description: "HEB grocery data API: product search with price, unit price, rating and availability, full item detail with nutrition facts and ingredients, and store locator for HEB and Central Market locations. 3 endpoints, 2 credits each."
version: 1.0.0
tags: heb, heb-api, heb-grocery-data, grocery, grocery-prices, texas-grocery, product-data, product-search, retail, store-locator, nutrition, price-monitoring, catalog-enrichment, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/heb-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data
---

# HEB Grocery Data API - Search, Product Detail, Store Locator

Search HEB products, read full item detail with pricing and nutrition, and find HEB stores near a location. Pass a `store_id` to get one store's prices, stock, aisle location and search assortment. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find products on heb.com by keyword, brand, category or department
- Look up an HEB product by URL, slug or product id
- Compare HEB grocery prices or check product availability
- Check the price, stock or aisle location of a product at a specific HEB store
- Get nutrition facts, ingredients or specifications for an HEB product
- Find HEB stores near a zip code or city in Texas
- Monitor HEB pricing or enrich a catalog with HEB product data

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 2 credits.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All HEB endpoints cost **2 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/heb/search` | 2 | Product search results: name, brand, price (cents), sale status, unit price, size, UPC, stock, EBT/SNAP eligibility, aisle location and URL. Optional `store_id` |
| `POST /api/v1/heb/product` | 2 | Full product detail: description, ingredients, nutrition, images, similar products, coupons and aisle location. Optional `store_id` |
| `POST /api/v1/heb/stores` | 2 | HEB stores near a ZIP or city: `store_number`, address, phone, hours, pharmacy, fulfillment channels and distance |

## Workflow

1. **Search for products:** call `/heb/search` with `query`. Results include price, unit price, stock and aisle location.
2. **Product detail:** call `/heb/product` with a `product_url` from search results, or with `slug` and `product_id`.
3. **Find stores:** call `/heb/stores` with `zip` or `city` to find nearby HEB locations.

### Prices at a specific store

Prices, stock and the in-store aisle differ by store. Without `store_id` every call uses HEB's default store.

1. Call `/heb/stores` with the shopper's `zip` (or `city`) and take `store_number` from the nearest store (e.g. `"441"`).
2. Pass it as `store_id` (string `"441"` or number `441`) to `/heb/search` and `/heb/product`. Prices, `in_stock`, `product_location` and the search assortment then come from that store.
3. The response echoes the store used in `data.store`, e.g. `{"store_id": "441", "name": "Uvalde H-E-B"}`. Quote that store name when reporting prices.
4. With `store_id`, `/heb/product` accepts `product_id` alone (no `slug` needed); `product_url` still works.

An unknown store number returns `400` with `store_id 99999 is not an HEB store. Find store numbers with /api/v1/heb/stores.` Store pricing is US (heb.com) only. Credits are unchanged: 2 per call.

### Pagination

- **Search:** `page` (1-based) and `page_size` (default 60, 1-60). The response carries `total_results` and `count`. Each page is 2 credits.
- **Product and stores:** no pagination.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords, brand or product name (1-200 chars) |
| `page` | integer | 1 | 1-based page number |
| `page_size` | integer | 60 | Results per page, 1-60 |
| `store_id` | string or integer | - | HEB store number from `/heb/stores` (`store_number`). Prices, stock, aisle and assortment for that store. US only |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_url` | string | one of | An heb.com product URL |
| `slug` | string | one of | Product slug (the readable part of the product URL), used with `product_id` |
| `product_id` | string | one of | Product id (`id` in search results). Needs `slug`, unless `store_id` is set |
| `store_id` | string or integer | - | HEB store number from `/heb/stores`. Price, stock and aisle for that store. US only |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | 5-digit US ZIP code |
| `city` | string | one of | City name (e.g. `Austin`, `San Antonio`) |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/heb/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "whole milk", "store_id": "441", "page_size": 5}'
```

Captured response (store 441, trimmed to one product):

```json
{
  "data": {
    "query": "whole milk",
    "page": 1,
    "country": "us",
    "count": 2,
    "total_results": 34,
    "products": [
      {
        "id": "314130",
        "name": "H-E-B Whole Milk, 1 gal",
        "brand": "H-E-B",
        "is_own_brand": true,
        "url": "https://www.heb.com/product-detail/h-e-b-whole-milk-1-gal/314130",
        "image": "https://images.heb.com/is/image/HEBGrocery/prd-large/000314130.jpg",
        "price": 398,
        "list_price": null,
        "is_on_sale": false,
        "unit_price": "$0.03/oz",
        "size": "1 gal",
        "upc": "041220753772",
        "in_stock": true,
        "availability": ["IN_STORE", "CURBSIDE_PICKUP", "CURBSIDE_DELIVERY"],
        "is_ebt_snap": true,
        "category": "Dairy & eggs",
        "category_id": "490016",
        "product_location": "In Dairy on the Back Wall"
      }
    ],
    "store": { "store_id": "441", "name": "Uvalde H-E-B" }
  },
  "response_time": 2453,
  "credits_used": 2
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def heb(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/heb/{endpoint}", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]

# 1. Find the shopper's store
stores = heb("stores", {"zip": "78801"})
store = stores["stores"][0]
print(store["store_number"], store["name"], store["distance_miles"])

# 2. Search that store (price is in cents)
found = heb("search", {"query": "whole milk", "store_id": store["store_number"], "page_size": 5})
print("Prices at", found["store"]["name"])
for row in found["products"]:
    print(row["name"], row["price"] / 100, row["unit_price"], row["product_location"])

# 3. Full product detail at the same store - product_id alone is enough with store_id
product = heb("product", {"product_id": found["products"][0]["id"], "store_id": store["store_number"]})
print(product["name"], product["price"], product["in_stock"], product["ingredients"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. `fetched_at` is the ISO time the data was retrieved; nothing is cached, so it is the age of the data. Key `data` fields:

- **search** - `query`, `page`, `country`, `count`, `total_results`, `products[]`, and `store` {`store_id`, `name`} when `store_id` was passed. A row: `id`, `name`, `brand`, `is_own_brand`, `url`, `image`, `price` (cents), `list_price` (cents, set when on sale), `is_on_sale`, `unit_price`, `size`, `upc`, `in_stock`, `availability[]`, `is_ebt_snap`, `category`, `category_id`, `product_location` (aisle).
- **product** - `id`, `name`, `brand`, `is_own_brand`, `url`, `country`, `images[]`, `price`, `list_price`, `is_on_sale`, `unit_price`, `size`, `upc`, `in_stock`, `availability[]`, `is_ebt_snap`, `description`, `ingredients`, `nutrition` {`serving_size`, `calories`, `nutrients[]`} or null, `breadcrumbs[]`, `category`, `category_id`, `product_location`, `similar_products[]`, `coupons[]`, and `store` when `store_id` was passed.
- **stores** - `count`, `total_stores`, `page`, `stores[]` (`store_number`, `name`, `address` {`street`, `city`, `state`, `zip`}, `phone`, `latitude`, `longitude`, `distance_miles`, `store_hours[]`, `has_pharmacy`, `format`, `fulfillments[]`, `url`).

## Guardrails

- HEB operates primarily in Texas. Store searches outside this area return few or no results.
- `price` and `list_price` are integers in cents: `398` is $3.98.
- Prices, stock and aisle are per store. When the user names a town or ZIP, look the store up and pass `store_id`; otherwise say the prices are for HEB's default store. Name the store from `data.store` in the answer.
- Unit prices (`unit_price`) are the best way to compare products of different sizes.
- Never fabricate prices, nutrition facts or store hours. Only return what the API returned, and surface the product `url` so the user can verify.
- `on_sale` and `promotions` reflect the current heb.com state; in-store prices may differ.

## Failure handling

- `400` means an invalid or missing parameter - fix the body and retry. An unknown `store_id` is a `400` too: look the store up again with `/heb/stores`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means the product was not found - check the URL or id.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data).
- `502` / `503` mean HEB data is temporarily unavailable - wait a few seconds and retry.
- If search returns nothing, try broader keywords or check spelling.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

Python: use the `requests` example above.

```bash
npm install scavio@0.28.1
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const stores = await scavio.heb.stores({ zip: "78801" });
const storeId = stores.data.stores[0].store_number;
const found = await scavio.heb.search({ query: "whole milk", store_id: storeId, page_size: 5 });
const product = await scavio.heb.product({ product_id: found.data.products[0].id, store_id: storeId });
```

MCP: the Scavio MCP server exposes all 3 HEB endpoints as tools (`search_heb`, `get_heb_product`, `get_heb_stores`); `search_heb` and `get_heb_product` take `store_id`. HEB is opt-in: add `heb` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.26.4"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,heb"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [HEB search](https://scavio.dev/docs/heb-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data), [product](https://scavio.dev/docs/heb-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data), [stores](https://scavio.dev/docs/heb-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data). Overview: [HEB API](https://scavio.dev/heb-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data).
