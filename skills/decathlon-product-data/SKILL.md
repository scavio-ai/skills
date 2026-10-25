---
name: decathlon-product-data
description: "Decathlon product data API: product search with price, rating, availability and images, and full item detail with variants, SKU, GTIN, breadcrumbs and category across 7 country domains (FR, ES, IT, IN, UK, PT, international). 2 endpoints, 2 credits each."
version: 1.0.0
tags: decathlon, decathlon-api, decathlon-product-data, sporting-goods, sports-equipment, product-search, product-data, retail, price-monitoring, catalog-enrichment, europe, france, spain, italy, india, uk, portugal, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/decathlon-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=decathlon-product-data
---

# Decathlon Product Data API - Search, Pricing, 7 Countries

Search Decathlon products and read full item detail with pricing, ratings, images, variants and breadcrumbs. Covers 7 country domains: France, Spain, Italy, India, UK, Portugal and decathlon.net (international). All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find products on decathlon.fr, decathlon.es, decathlon.it, decathlon.in, decathlon.co.uk, decathlon.pt or decathlon.net
- Search Decathlon products by keyword across any supported country
- Look up a Decathlon product by URL or product ID
- Compare sporting goods prices across Decathlon country stores
- Monitor Decathlon pricing or enrich a catalog with Decathlon product data
- Get product details, images, variants or ratings for a Decathlon item

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=decathlon-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=decathlon-product-data) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. All Decathlon endpoints cost **2 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/decathlon/search` | 2 | Product search results: name, brand, price, rating, review count, image, availability and product URL |
| `POST /api/v1/decathlon/product` | 2 | Full product detail: description, images, variants, pricing, SKU, GTIN, color, rating, breadcrumbs and category |

## Country domains

| Code | Domain | Country |
|---|---|---|
| `fr` | decathlon.fr | France |
| `es` | decathlon.es | Spain |
| `it` | decathlon.it | Italy |
| `in` | decathlon.in | India |
| `uk` | decathlon.co.uk | United Kingdom |
| `pt` | decathlon.pt | Portugal |
| `net` | decathlon.net | International |

## Workflow

1. **Search for products:** call `/decathlon/search` with `query` and a `country` code. Results include price in cents, rating and availability across any supported country store.
2. **Product detail:** call `/decathlon/product` with a `product_url` from search results or a `product_id`, plus the `country` code.

### Pagination

- **Search:** `page` (1-based). The response carries `count` (number of products on this page). Each page is 2 credits.
- **Product:** no pagination.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords or product name (1-200 chars) |
| `country` | string | required | Country code: `fr`, `es`, `it`, `in`, `uk`, `pt` or `net` |
| `page` | integer | 1 | 1-based page number (max 50) |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_url` | string | one of | Full or relative Decathlon product URL from any supported domain |
| `product_id` | string | one of | Numeric product ID (the 5+ digit number from the /p/{slug}/{id}/... URL) |
| `country` | string | required | Country code: `fr`, `es`, `it`, `in`, `uk`, `pt` or `net` |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/decathlon/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "running shoes", "country": "fr"}'
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def decathlon(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/decathlon/{endpoint}", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]

# 1. Search for products in France
found = decathlon("search", {"query": "running shoes", "country": "fr"})
for row in found["products"]:
    print(row["name"], row["price"], row["rating"])

# 2. Full product detail by URL
product = decathlon("product", {
    "product_url": found["products"][0]["url"],
    "country": "fr"
})
print(product["name"], product["price"], product["brand"])

# 3. Look up by product ID
product = decathlon("product", {"product_id": "325965", "country": "fr"})
print(product["name"], product["description"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. `fetched_at` is the ISO time the data was retrieved; nothing is cached, so it is the age of the data. Key `data` fields:

- **search** - `query`, `page`, `country`, `count`, `products[]`. A row: `position`, `id`, `name`, `brand`, `url`, `image`, `price` (cents), `currency`, `availability`, `rating`, `review_count`.
- **product** - `id`, `name`, `brand`, `url`, `country`, `description`, `images[]`, `sku`, `gtin`, `mpn`, `color`, `price` (cents), `list_price` (cents, original price before discount), `currency`, `availability`, `offers[]` (when multiple sellers), `rating`, `review_count`, `best_rating`, `category`, `breadcrumbs[]`.

## Guardrails

- Decathlon runs different frontends per country (Svelte in France, Next.js in Spain, custom in India). The API normalizes all of them into one consistent shape.
- Prices are in cents of the local currency. The `currency` field tells you which one (EUR, GBP, INR).
- `list_price` is the original price before any discount. It is null when there is no discount.
- `availability` follows Schema.org values: `InStock`, `OutOfStock`, `PreOrder`, etc.
- Never fabricate prices, ratings or product IDs. Only return what the API returned, and surface the product `url` so the user can verify.
- Product URLs from any country domain work, but the `country` parameter must match the domain (e.g. `country: "fr"` for decathlon.fr URLs).

## Failure handling

- `400` means an invalid or missing parameter - fix the body and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means the product was not found - check the URL or product ID.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=decathlon-product-data).
- `502` / `503` mean Decathlon data is temporarily unavailable - wait a few seconds and retry.
- If search returns nothing, try broader keywords, check spelling or try a different country.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.18.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.decathlon.search("running shoes", country="fr")
product = client.decathlon.product(product_url="/p/mens-running-shoes/325965/...")
product = client.decathlon.product(product_id="325965", country="fr")
```

```bash
npm install scavio@0.18.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const found = await scavio.decathlon.search({ query: "running shoes", country: "fr" });
const product = await scavio.decathlon.product({ product_id: "325965", country: "fr" });
```

MCP: the Scavio MCP server exposes both Decathlon endpoints as tools (`search_decathlon`, `get_decathlon_product`). Decathlon is opt-in: add `decathlon` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.16.1"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,decathlon"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [Decathlon search](https://scavio.dev/docs/decathlon-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=decathlon-product-data), [product](https://scavio.dev/docs/decathlon-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=decathlon-product-data). Overview: [Decathlon API](https://scavio.dev/decathlon-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=decathlon-product-data).
