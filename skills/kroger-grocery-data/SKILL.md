---
name: kroger-grocery-data
description: "Kroger grocery data API: product search with price, unit price, rating and availability, and full item detail with nutrition facts and ingredients across Kroger, Ralphs, Fred Meyer, Harris Teeter, King Soopers and Fry's. 2 endpoints, 2 credits each."
version: 1.0.0
tags: kroger, kroger-api, kroger-grocery-data, grocery, grocery-prices, ralphs, fred-meyer, harris-teeter, king-soopers, frys, product-data, product-search, retail, nutrition, price-monitoring, catalog-enrichment, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/kroger-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data
---

# Kroger Grocery Data API - Search, Product Detail, Multi-Banner

Search Kroger products and read full item detail with pricing and nutrition. Covers all Kroger-owned banners: Kroger, Ralphs, Fred Meyer, Harris Teeter, King Soopers and Fry's. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find products on kroger.com by keyword, brand or category
- Look up a Kroger product by URL or UPC barcode
- Compare grocery prices at Kroger, Ralphs, Fred Meyer, Harris Teeter, King Soopers or Fry's
- Get nutrition facts, ingredients or specifications for a Kroger product
- Monitor Kroger pricing or enrich a catalog with Kroger product data
- Search any Kroger-family banner (Ralphs, Fred Meyer, Harris Teeter, King Soopers, Fry's)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. All Kroger endpoints cost **2 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/kroger/search` | 2 | Product search results: name, brand, price, unit price, size, rating, image, availability and promotions |
| `POST /api/v1/kroger/product` | 2 | Full product detail: description, nutrition facts, ingredients, specifications, images, pricing and availability |

## Workflow

1. **Search for products:** call `/kroger/search` with `query`. Results include price, unit price, rating and availability across all Kroger banners.
2. **Product detail:** call `/kroger/product` with a `product_url` from search results, or with a `upc` barcode.

### Pagination

- **Search:** `page` (1-based). The response carries `total_results` and `total_pages`. Each page is 2 credits.
- **Product:** no pagination.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords, brand or product name (1-200 chars) |
| `page` | integer | 1 | 1-based page number |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_url` | string | one of | A kroger.com product URL (or any Kroger-family banner URL) |
| `upc` | string | one of | UPC barcode (GTIN-13 or UPC-A) |
| `slug` | string | -- | Optional product slug, used with `upc` for disambiguation |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/kroger/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "organic eggs"}'
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def kroger(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/kroger/{endpoint}", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]

# 1. Search for products
found = kroger("search", {"query": "organic eggs"})
for row in found["results"]:
    print(row["name"], row["brand"], row["price"], row["size"])

# 2. Full product detail by URL
product = kroger("product", {"product_url": found["results"][0]["url"]})
print(product["name"], product["price"], product["nutrition"])

# 3. Look up by UPC barcode
product = kroger("product", {"upc": "0011110838490"})
print(product["name"], product["price"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. `fetched_at` is the ISO time the data was retrieved; nothing is cached, so it is the age of the data. Key `data` fields:

- **search** - `query`, `total_results`, `page`, `total_pages`, `count`, `results[]`. A row: `product_id`, `upc`, `name`, `brand`, `slug`, `url`, `image`, `price`, `original_price`, `unit_price`, `unit_of_measure`, `size`, `rating`, `reviews_count`, `in_stock`, `on_sale`, `promotions[]`, `categories`, `banner`.
- **product** - `product_id`, `upc`, `name`, `brand`, `slug`, `url`, `images[]`, `description`, `price`, `original_price`, `unit_price`, `unit_of_measure`, `size`, `rating`, `reviews_count`, `in_stock`, `on_sale`, `promotions[]`, `nutrition` {`serving_size`, `calories`, `nutrients[]`}, `ingredients`, `specifications[]` {`name`, `value`}, `categories`, `banner`.

## Guardrails

- Kroger operates under multiple banners. The `banner` field identifies which storefront the data comes from (Kroger, Ralphs, Fred Meyer, Harris Teeter, King Soopers, Fry's).
- Product URLs from any Kroger-family banner site work with the product endpoint.
- Unit prices (`unit_price` + `unit_of_measure`) are the best way to compare products of different sizes.
- Never fabricate prices, nutrition facts or UPCs. Only return what the API returned, and surface the product `url` so the user can verify.
- `on_sale` and `promotions` reflect the current online state; in-store prices may differ by location.
- UPC lookup returns the product across any Kroger banner that carries it.

## Failure handling

- `400` means an invalid or missing parameter - fix the body and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means the product was not found - check the URL or UPC.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data).
- `502` / `503` mean Kroger data is temporarily unavailable - wait a few seconds and retry.
- If search returns nothing, try broader keywords or check spelling.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.18.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.kroger.search("organic eggs")
product = client.kroger.product(product_url="https://www.kroger.com/p/...")
product = client.kroger.product(upc="0011110838490")
```

```bash
npm install scavio@0.18.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const found = await scavio.kroger.search({ query: "organic eggs" });
const product = await scavio.kroger.product({ product_url: "https://www.kroger.com/p/..." });
const product2 = await scavio.kroger.product({ upc: "0011110838490" });
```

MCP: the Scavio MCP server exposes both Kroger endpoints as tools (`search_kroger`, `get_kroger_product`). Kroger is opt-in: add `kroger` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.16.1"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,kroger"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [Kroger search](https://scavio.dev/docs/kroger-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data), [product](https://scavio.dev/docs/kroger-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data). Overview: [Kroger API](https://scavio.dev/kroger-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data).
