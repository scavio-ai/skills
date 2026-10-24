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

Search HEB products, read full item detail with pricing and nutrition, and find HEB and Central Market stores near a location. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find products on heb.com by keyword, brand, category or department
- Look up an HEB product by URL, slug or product id
- Compare HEB grocery prices or check product availability
- Get nutrition facts, ingredients or specifications for an HEB product
- Find HEB or Central Market stores near a zip code or city in Texas
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
| `POST /api/v1/heb/search` | 2 | Product search results: name, brand, price, unit price, size, rating, image, availability and promotions |
| `POST /api/v1/heb/product` | 2 | Full product detail: description, nutrition facts, ingredients, specifications, images, price history and availability |
| `POST /api/v1/heb/stores` | 2 | HEB and Central Market stores near a location with address, phone, hours, departments, services and distance |

## Workflow

1. **Search for products:** call `/heb/search` with `query`. Results include price, unit price, rating and availability.
2. **Product detail:** call `/heb/product` with a `product_url` from search results, or with `slug` and `product_id`.
3. **Find stores:** call `/heb/stores` with `zip` or `city` to find nearby HEB and Central Market locations.

### Pagination

- **Search:** `page` (1-based) and `page_size` (default 24, up to 60). The response carries `total_results` and `total_pages`. Each page is 2 credits.
- **Product and stores:** no pagination.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords, brand or product name (1-200 chars) |
| `page` | integer | 1 | 1-based page number |
| `page_size` | integer | 24 | Results per page, 1-60 |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_url` | string | one of | An heb.com product URL |
| `slug` | string | one of | Product slug from search results (used with `product_id`) |
| `product_id` | string | one of | Product id from search results (used with `slug`) |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | US zip code (Texas and nearby states) |
| `city` | string | one of | City name (e.g. `Austin`, `San Antonio`) |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/heb/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "organic milk", "page_size": 5}'
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

# 1. Search for products
found = heb("search", {"query": "organic milk", "page_size": 5})
for row in found["results"]:
    print(row["name"], row["price"], row["unit_price"], row["size"])

# 2. Full product detail
product = heb("product", {"product_url": found["results"][0]["url"]})
print(product["name"], product["price"], product["nutrition"])

# 3. Find nearby stores
stores = heb("stores", {"zip": "78701"})
for s in stores["stores"]:
    print(s["name"], s["address"], s["distance_miles"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. `fetched_at` is the ISO time the data was retrieved; nothing is cached, so it is the age of the data. Key `data` fields:

- **search** - `query`, `total_results`, `page`, `page_size`, `total_pages`, `count`, `results[]`. A row: `product_id`, `name`, `brand`, `slug`, `url`, `image`, `price`, `original_price`, `unit_price`, `unit_of_measure`, `size`, `rating`, `reviews_count`, `in_stock`, `on_sale`, `promotions[]`, `categories`.
- **product** - `product_id`, `name`, `brand`, `slug`, `url`, `images[]`, `description`, `price`, `original_price`, `unit_price`, `unit_of_measure`, `size`, `rating`, `reviews_count`, `in_stock`, `on_sale`, `promotions[]`, `nutrition` {`serving_size`, `calories`, `nutrients[]`}, `ingredients`, `specifications[]` {`name`, `value`}, `categories`, `upc`.
- **stores** - `location`, `count`, `stores[]` (`store_id`, `name`, `type`, `address`, `city`, `state`, `zip`, `phone`, `latitude`, `longitude`, `distance_miles`, `hours`, `departments[]`, `services[]`).

## Guardrails

- HEB operates primarily in Texas and parts of northeast Mexico. Store searches outside this area will return few or no results.
- Central Market stores appear alongside HEB stores in the stores endpoint - check the `type` field to distinguish them.
- Unit prices (`unit_price` + `unit_of_measure`) are the best way to compare products of different sizes.
- Never fabricate prices, nutrition facts or store hours. Only return what the API returned, and surface the product `url` so the user can verify.
- `on_sale` and `promotions` reflect the current heb.com state; in-store prices may differ.

## Failure handling

- `400` means an invalid or missing parameter - fix the body and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means the product was not found - check the URL or id.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data).
- `502` / `503` mean HEB data is temporarily unavailable - wait a few seconds and retry.
- If search returns nothing, try broader keywords or check spelling.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.18.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.heb.search("organic milk", page_size=5)
product = client.heb.product(product_url="https://www.heb.com/product-detail/...")
stores = client.heb.stores(zip="78701")
```

```bash
npm install scavio@0.18.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const found = await scavio.heb.search({ query: "organic milk", page_size: 5 });
const product = await scavio.heb.product({ product_url: "https://www.heb.com/product-detail/..." });
const stores = await scavio.heb.stores({ zip: "78701" });
```

MCP: the Scavio MCP server exposes all 3 HEB endpoints as tools (`search_heb`, `get_heb_product`, `get_heb_stores`). HEB is opt-in: add `heb` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.16.1"],
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
