---
name: home-depot-product-data
description: "Home Depot product data: keyword search returning price, promotions, brand, model, ratings and per-store pickup and delivery; full item detail with spec table, dimensions, documents and return policy; and paginated review bodies with rating distribution. 3 endpoints, 2 credits each, structured JSON."
version: 1.0.0
tags: home-depot, home-depot-api, home-depot-product-data, product-data, product-search, retail, home-improvement, hardware, pricing, product-reviews, price-monitoring, catalog-enrichment, web-scraping, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F528"
    homepage: https://scavio.dev/docs/home-depot-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=home-depot-product-data
---

# Home Depot Product Data API - Search, Item Detail, Reviews

Search Home Depot by keyword, read one item in full, and page through its review bodies. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find products on homedepot.com by keyword, price band or rating
- Look up a Home Depot item by item id or by a pasted `homedepot.com/p/...` URL
- Pull the spec table, dimensions, documents or return policy for an item
- Read customer reviews for an item, with the rating distribution and per-attribute ratings
- Monitor hardware or home-improvement pricing and promotions
- Enrich a product catalog with brand, model number, UPC and category path

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=home-depot-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every Home Depot endpoint costs **2 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/homedepot/search` | 2 | Keyword results with price, promotions, brand, model, ratings, badges, per-store pickup and delivery |
| `POST /api/v1/homedepot/product` | 2 | One item in full: pricing, images and videos, spec table, dimensions, bullets, documents, return policy |
| `POST /api/v1/homedepot/reviews` | 2 | One page of full review bodies, rating distribution, per-attribute ratings, photos, seller responses |

## Workflow

1. **Find items:** call `/homedepot/search` with `query`. Read `products[].item_id`.
2. **Item detail:** call `/homedepot/product` with that `item_id` (a full `homedepot.com/p/...` URL works too; tracking parameters are discarded).
3. **Reviews:** call `/homedepot/reviews` with the same `item_id`. `/product` carries only a **10-review preview** — `/reviews` is the paginated surface.

### Pagination

- **Search** is fixed at **12 products per page**. There is no page-size parameter and no way to raise it, so paging is the only way to read further. Ten pages is 20 credits — decide the budget before looping.
- **Reviews** are **30 per page**. The response carries `total_pages`; that is the last page that exists, and asking past it is a **404**. Stop at `total_pages`.
- **Product** takes no paging parameter.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keyword (1-500 chars) |
| `page` | integer | -- | 1-based. 12 products per page, fixed |
| `sort_by` | string | `best_match` | `best_match`, `top_sellers`, `top_rated`, `price_low`, `price_high` |
| `min_price` | number | -- | Minimum price, inclusive (0 or greater) |
| `max_price` | number | -- | Maximum price, inclusive (0 or greater) |

`sort_by` is a **closed set**. Home Depot does not fall back on an unknown sort — it answers `200` with an empty page that is still billed. A "newest" sort is deliberately absent: it works on category pages and is rejected on keyword search.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string | required | Item id, or a full `homedepot.com/p/...` URL |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string | required | Item id, or a full `homedepot.com/p/...` URL |
| `page` | integer | -- | 1-based. 30 per page; past `total_pages` is a 404 |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search, cheapest first, under $300
found = requests.post(f"{BASE}/api/v1/homedepot/search", headers=HEADERS,
    json={"query": "cordless drill", "sort_by": "price_low", "max_price": 300}).json()

item_id = found["data"]["products"][0]["item_id"]

# 2. Full item detail (a pasted product URL works just as well)
item = requests.post(f"{BASE}/api/v1/homedepot/product", headers=HEADERS,
    json={"item_id": item_id}).json()

# 3. Reviews, page 2 onward - stop at total_pages, never guess past it
reviews = requests.post(f"{BASE}/api/v1/homedepot/reviews", headers=HEADERS,
    json={"item_id": item_id, "page": 2}).json()

print(reviews["data"]["total_pages"], reviews["data"]["count"])
```

Paging search, capped so it cannot run away with the user's credits:

```python
def search_pages(query, max_pages=3, **filters):
    """12 products per page, 2 credits per page."""
    out = []
    for page in range(1, max_pages + 1):
        data = requests.post(f"{BASE}/api/v1/homedepot/search", headers=HEADERS,
                             json={"query": query, "page": page, **filters}).json()["data"]
        out += data["products"]
        if data["count"] < data["page_size"]:
            break
    return out
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **search** — `query`, `url`, `canonical_url`, `page`, `page_size` (12), `start_index`, `total_results`, `sort`, `sort_order`, `did_you_mean`, `corrected_query`, `category_path`, `count`, `products[]`.
  A product row: `pos`, `item_id`, `parent_id`, `store_sku`, `model_number`, `brand`, `title`, `url`, `product_type`, `image`, `images`, `price`, `original_price`, `currency`, `unit_of_measure`, `discount_amount`, `discount_percent`, `promotion_type`, `promotion_text`, `clearance_price`, `price_hidden`, `rating`, `review_count`, `badges`, `sponsored`, `category_path`, `department`, `returnable`, `quantity_limit`, `availability`, `buyable`, `in_stock`, `stock_quantity`, `pickup`, `delivery`, `key_features`.
- **product** — `item_id`, `parent_id`, `store_sku`, `oms_sku`, `model_number`, `upc`, `gtin13`, `title`, `url`, `brand`, `product_type`, `description`, `price`, `original_price`, `currency`, `unit_of_measure`, `promotion_*`, `clearance_price`, `price_valid_until`, `availability`, `buyable`, `discontinued`, `rating`, `review_count`, `image`, `images[]`, `videos[]`, `badges[]`, `highlights[]`, `bullets[]`, `specifications[]` (`group`, `name`, `value`), `key_features[]`, `depth`, `height`, `width`, `weight`, `category_path[]`, `returnable`, `return_days`, `quantity_limit`, `prop65_warning`, `prop65_message`.
- **reviews** — `item_id`, `product_name`, `url`, `rating`, `total_results`, `recommended_count`, `not_recommended_count`, `total_pages`, `rating_distribution[]`, `page`, `page_size` (30), `count`, `reviews[]` (`id`, `rating`, `title`, `text`, `author`, `location`, `submitted_at`, `verified_purchase`, `recommended`, `helpful_votes`, `unhelpful_votes`, `syndicated`, `pros`, `cons`, `secondary_ratings`, `photos`, `videos`, `responses`).

```json
{
  "data": {
    "query": "cordless drill",
    "page": 1,
    "page_size": 12,
    "total_results": 2148,
    "count": 12,
    "products": [
      {
        "pos": 1,
        "item_id": "325479354",
        "brand": "DEWALT",
        "title": "20V MAX Cordless Drill/Driver Kit",
        "price": 179,
        "currency": "USD",
        "rating": 4.7,
        "review_count": 8230,
        "url": "https://www.homedepot.com/p/325479354"
      }
    ]
  },
  "credits_used": 2,
  "credits_remaining": 998
}
```

## Guardrails

- Every call is **2 credits**, including one that comes back empty. Search paging is 2 credits per 12 products, so state the intended spend before looping.
- Never invent a `sort_by` value. An unrecognised sort returns an empty page and is still billed.
- Do not send a page size — there is none. Search is 12 per page and reviews are 30 per page, both fixed upstream.
- Do not ask for a review page past `total_pages`; it is a billed 404, not an empty list.
- `/product` gives a 10-review preview only. If the user wants review analysis, call `/reviews` — do not present the preview as the full set.
- Never fabricate item ids, prices, model numbers, availability or review text. Only return what the API returned.
- Always surface the product `url` so the user can verify.

## Failure handling

- `400` means an invalid or missing parameter (no `query`, a `sort_by` outside the enum) — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` on `/product` or `/reviews` means the item id does not exist, or the review page is past the last one. Home Depot answers those with a billed `200` shell that the API restates as a 404 — do not retry the same id or page.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=home-depot-product-data).
- `502` / `503` mean upstream is temporarily unavailable — wait a few seconds and retry, up to a few times.
- If search returns nothing, relax the price filters or try broader keywords.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.home_depot.search("cordless drill", sort_by="top_rated", max_price=300)
item = client.home_depot.product(found["data"]["products"][0]["item_id"])
reviews = client.home_depot.reviews(item["data"]["item_id"], page=2)
```

```bash
npm install scavio@0.15.0
```

```javascript
import { Scavio } from "scavio";

const client = new Scavio(); // reads SCAVIO_API_KEY
const found = await client.homeDepot.search({ query: "cordless drill", sort_by: "top_rated" });
```
