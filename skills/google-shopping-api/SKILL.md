---
name: google-shopping-api
description: "Google Shopping product and price data as structured JSON: search products with min/max price, on-sale, free-shipping and price-sort filters returning title, price, seller, rating and reviews, open a full product page with specs and variants, then page every store selling it. 3 endpoints, 1 credit each."
version: 1.0.0
tags: google-shopping, google-shopping-api, product-search, price-comparison, merchant-offers, product-prices, ecommerce, retail, shopping-results, agents, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F6CD"
    homepage: https://scavio.dev/docs/google-shopping?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-shopping-api
---

# Google Shopping API - Product Search, Merchant Offers, Prices

Search Google Shopping for products, open a full product detail page, and page through every store selling it — all as structured JSON. Three endpoints, each 1 credit.

## When to trigger

Use this skill when the user asks to:
- Find products across retailers with price or sale filters
- Compare prices for a product across many stores
- Get specs, ratings, variants, or seller options for a product
- Build a price-comparison or shopping-research workflow

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-shopping-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

## Endpoints

| Endpoint | Credits | Description |
|---|---|---|
| `POST https://api.scavio.dev/api/v2/google/shopping` | 1 | Search products, returns `shopping_results[]` |
| `POST https://api.scavio.dev/api/v2/google/shopping/product` | 1 | Full product detail page |
| `POST https://api.scavio.dev/api/v2/google/shopping/product/stores` | 1 | Page through all stores selling a product |

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Workflow

1. **Search:** call `/shopping` with a `query`. Filter with `min_price`, `max_price`, `on_sale`, `free_shipping`, or `sort_by`. Each result carries a `catalog_id` (durable) or `product_id`.
2. **Product page:** call `/shopping/product` with a `catalog_id` (pass the same `query`) for full specs, variants, and top stores in `product_results`.
3. **All stores:** if the product lists more sellers than returned, call `/shopping/product/stores` with the `catalog_id` and the `next_page_token` from the previous response to page through every store.

## Shopping Search Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search query (1-500 chars) |
| `device` | string | -- | `desktop` or `mobile` |
| `start` | number | -- | Result offset (follow `pagination.next`) |
| `min_price` | number | -- | Minimum price filter |
| `max_price` | number | -- | Maximum price filter |
| `sort_by` | number | `0` | `0` relevance, `1` price ascending, `2` price descending |
| `free_shipping` | boolean | -- | Only free-shipping offers |
| `on_sale` | boolean | -- | Only on-sale offers |
| `shoprs` | string | -- | Opaque filter token from `filters[]` / `carousel_filters[]` |
| `hl` | string | -- | UI language |
| `gl` | string | -- | Geo country |
| `google_domain` | string | `google.com` | Regional Google domain |
| `location` | string | -- | Canonical location name (auto-UULE) |
| `uule` | string | -- | Pre-encoded UULE |

## Product Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `catalog_id` | string | -- | Durable catalog id (pass with `query`) |
| `query` | string | -- | Required when `catalog_id` is set |
| `product_id` | string | -- | Product id alternative |
| `immersive_product_page_token` | string | -- | Page token from a listing |
| `page_token` | string | -- | Alias for `immersive_product_page_token` |
| `device` | string | -- | `desktop`, `mobile`, or `tablet` |
| `sort_by` | string | -- | Seller sort: `base_price`, `total_price`, `promotion`, `seller_rating` |
| `load_all_stores` | boolean | -- | Load all stores inline |
| `more_stores` | boolean | -- | Include additional stores |
| `hl` | string | -- | UI language |
| `gl` | string | -- | Geo country |
| `google_domain` | string | `google.com` | Regional Google domain |
| `location` | string | -- | Canonical location name |
| `uule` | string | -- | Pre-encoded UULE |

## Product Stores Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `catalog_id` | string | required | Same `catalog_id` used on the product call |
| `next_page_token` | string | required | Continuation cursor from a prior response |

## Example

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-shopping-api. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search products, cheapest first, under $1500
search = requests.post(f"{BASE}/api/v2/google/shopping", headers=HEADERS,
    json={"query": "16 inch laptop", "sort_by": 1, "max_price": 1500}).json()

item = search["shopping_results"][0]
print(item["title"], item.get("price"), item.get("source"))

# 2. Full product page (catalog_id needs the query alongside it)
product = requests.post(f"{BASE}/api/v2/google/shopping/product", headers=HEADERS,
    json={"catalog_id": item["catalog_id"], "query": "16 inch laptop"}).json()

# 3. Page through every store selling it
token = product["product_results"].get("stores_pagination", {}).get("next_page_token")
if token:
    stores = requests.post(f"{BASE}/api/v2/google/shopping/product/stores", headers=HEADERS,
        json={"catalog_id": item["catalog_id"], "next_page_token": token}).json()
    for s in stores["product_results"]["stores"]:
        print(s.get("name"), s.get("total_price"))
```

## Responses

Search returns `shopping_results[]` (plus `filters` and `pagination`); product returns `product_results`; stores returns `product_results.stores[]`. Each also includes `response_time`, `credits_used`, `credits_remaining`, and `cached`.

```json
{
  "shopping_results": [
    {
      "position": 1,
      "title": "Example 16\" Laptop",
      "price": "$1,299.00",
      "extracted_price": 1299,
      "source": "Example Store",
      "rating": 4.5,
      "reviews": 210,
      "catalog_id": "1234567890"
    }
  ],
  "response_time": 1420,
  "credits_used": 1,
  "credits_remaining": 997,
  "cached": false
}
```

## Guardrails

- Each call costs 1 credit. Inform the user before paginating through many stores.
- Never fabricate product titles, prices, sellers, or ratings. Only return API data.
- The product call needs `catalog_id` + `query` together; the stores call needs `catalog_id` + `next_page_token` — always run `/shopping` first to obtain the `catalog_id`.
- Prices are strings as displayed; use `extracted_price` when present for numeric comparisons.

## Failure handling

- `400` means an invalid parameter (e.g. `catalog_id` without `query`) — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-shopping-api.
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If search returns no results, loosen the price filters or broaden the query.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
