---
name: specs-liquor-prices
description: "Spec's liquor prices API: search Spec's Wines, Spirits & Finer Foods in Texas, get a product's price and stock at every Spec's store in one call, and list stores by region. 3 endpoints, 5 credits each."
version: 1.0.1
tags: specs, specs-liquor, specs-api, specs-liquor-prices, liquor, wine, beer, spirits, texas, liquor-prices, store-prices, product-search, product-data, store-locator, retail, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/specs-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=specs-liquor-prices
---

# Spec's Liquor Prices API - Every Texas Store, Search, Store Locator

Search Spec's Wines, Spirits & Finer Foods, the Texas liquor chain, and get a product's price and stock at every Spec's store in one call. A store locator maps store numbers to addresses by region. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find wine, spirits or beer at Spec's by keyword or brand
- Check what a bottle costs at a specific Spec's store, or which store is cheapest
- Compare Spec's prices across stores or against other liquor retailers
- Find Spec's stores in a Texas region (Austin, Corpus Christi, Dallas, El Paso, Fort Worth, Houston, San Antonio)
- Monitor Spec's prices, promotions or stock

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=specs-liquor-prices) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=specs-liquor-prices) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 5 credits.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All Spec's endpoints cost **5 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/specs/search` | 5 | Search results with the online price (cents), case price and quantity, promo and Keyclub flags, stock, size, SKU, UPC and `slug` |
| `POST /api/v1/specs/product` | 5 | One product with `store_prices[]` (every store's price and stock, about 200 stores), the online price, ABV, origin and tasting notes. Optional `store_id` |
| `POST /api/v1/specs/stores` | 5 | Stores in a region: `store_id`, name, status, address, phone, coordinates, hours |

## Workflow

1. **Search:** call `/specs/search` with `query`. Each row has the online price and a `slug`.
2. **Every store's price:** call `/specs/product` with the `slug`. `store_prices[]` has each store's `price` and `in_stock`.
3. **One store on top (optional):** pass `store_id` to `/specs/product`. The top-level `price` and `in_stock` become that store's; `available_at_store` is `false` if it does not list the item.
4. **Map store numbers to places:** call `/specs/stores` with a `region`.

Search returns the online price only. Store prices differ, so use the product call when the store matters.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars) |
| `page` | integer | 1 | 1-based page, 24 results per page |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `slug` | string | one of | `slug` from search, e.g. `titos-texas-vodka-5` |
| `product_url` | string | one of | `https://specsonline.com/shop/<type>/<slug>/` |
| `store_id` | string | - | Store number from `/stores`, e.g. `"169"` |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `region` | string | required | `austin`, `corpus-christi`, `dallas`, `el-paso`, `fort-worth`, `houston` or `san-antonio` |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/specs/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "titos-texas-vodka-5", "store_id": "169"}'
```

Captured response (store 169, Stone Oak; trimmed to 2 of 195 store_prices entries):

```json
{
  "data": {
    "sku": "181081",
    "upc": "061994700003",
    "slug": "titos-texas-vodka-5",
    "name": "Tito's Handmade Vodka",
    "brand": "Tito's",
    "size": "1.75L",
    "abv": "40.00%",
    "origin": "United States",
    "url": "https://specsonline.com/shop/spirits/titos-texas-vodka-5/",
    "store_id": "169",
    "available_at_store": true,
    "price": 3260,
    "case_price": null,
    "case_quantity": null,
    "on_promo": false,
    "keyclub_offer": false,
    "in_stock": true,
    "online": {
      "price": 3155,
      "case_price": null,
      "case_quantity": null,
      "on_promo": false,
      "keyclub_offer": false,
      "in_stock": true
    },
    "store_count": 195,
    "store_prices": [
      {
        "store_id": "1",
        "price": 3155,
        "case_price": null,
        "case_quantity": null,
        "on_promo": false,
        "keyclub_offer": false,
        "in_stock": true
      },
      {
        "store_id": "2",
        "price": 3155,
        "case_price": null,
        "case_quantity": null,
        "on_promo": false,
        "keyclub_offer": false,
        "in_stock": true
      }
    ]
  },
  "response_time": 29059,
  "credits_used": 5
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def specs(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/specs/{endpoint}", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]

# 1. Search (online prices, in cents)
rows = specs("search", {"query": "titos"})["products"]
slug = rows[0]["slug"]

# 2. Every store's price in one call, with store 169 on top
p = specs("product", {"slug": slug, "store_id": "169"})
print(p["name"], "store 169:", p["price"] / 100, "online:", p["online"]["price"] / 100)
cheapest = min((s for s in p["store_prices"] if s["in_stock"]), key=lambda s: s["price"])
print("cheapest in-stock store:", cheapest["store_id"], cheapest["price"] / 100)

# 3. Name the stores
stores = {s["store_id"]: s for s in specs("stores", {"region": "san-antonio"})["stores"]}
print(stores.get(cheapest["store_id"], {}).get("name"))
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Spec's answered.

- **search** - `query`, `page`, `total_results`, `total_pages`, `count`, `products[]` (`position`, `code`, `sku`, `upc`, `slug`, `name`, `title`, `brand`, `size`, `category`, `category_group`, `subcategory`, `url`, `image`, `price`, `case_price`, `case_quantity`, `on_promo`, `keyclub_offer`, `in_stock`).
- **product** - `sku`, `upc`, `slug`, `name`, `title`, `brand`, `size`, `proof`, `abv`, `type`, `varietal`, `origin`, `region`, `vintage`, `tasting_notes`, `description`, `url`, `images[]`, `store_id`, `available_at_store`, `price`, `case_price`, `case_quantity`, `on_promo`, `keyclub_offer`, `in_stock`, `online` {same price fields}, `store_count`, `store_prices[]` {`store_id`, `price`, `case_price`, `case_quantity`, `on_promo`, `keyclub_offer`, `in_stock`}, `rating`, `review_count`.
- **stores** - `region`, `count`, `stores[]` (`store_id`, `name`, `status`, `type`, `address`, `city`, `state`, `zip`, `phone`, `latitude`, `longitude`, `url`, `hours[]` {`day`, `open`, `close`, `closed`}).

## Guardrails

- Prices are integers in cents: `3155` is $31.55.
- Search prices are the online price. When the user asks about a store, use the product call and quote that store's price.
- `on_promo` and `keyclub_offer` say a promotion or Keyclub member offer applies; the amount is not returned, so do not state one.
- A region covers nearby towns too (san-antonio includes Kerrville, Boerne and San Marcos).
- Never fabricate prices or store details. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (a region outside the 7, or a non-numeric `store_id`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means no such product; re-run the search for a fresh `slug`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=specs-liquor-prices).
- `502` means Spec's is temporarily unavailable. It is not charged; retry after a few seconds. Spec's pages are slow, so allow up to a minute per call.

## SDKs

```bash
pip install scavio==0.29.1
npm install scavio@0.29.1
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const found = await scavio.specs.search({ query: "titos" });
const { data: p } = await scavio.specs.product({ slug: found.data.products[0].slug, store_id: "169" });
const stores = await scavio.specs.stores({ region: "san-antonio" });
```

MCP: the Scavio MCP server exposes all 3 endpoints as tools (`search_specs`, `get_specs_product`, `get_specs_stores`). Spec's is opt-in: add `specs` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.27.1"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,specs"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/specs-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=specs-liquor-prices), [product](https://scavio.dev/docs/specs-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=specs-liquor-prices), [stores](https://scavio.dev/docs/specs-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=specs-liquor-prices). Overview: [Spec's API](https://scavio.dev/specs-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=specs-liquor-prices).
