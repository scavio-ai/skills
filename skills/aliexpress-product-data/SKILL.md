---
name: aliexpress-product-data
description: Search AliExpress, browse a category, pull one product with every SKU variant, read translated buyer reviews, and open a seller's storefront and catalogue. 6 endpoints, 1 credit each, structured JSON.
version: 1.0.0
tags: aliexpress, product-data, ecommerce, price-tracking, product-search, sku-variants, product-reviews, seller-data, dropshipping, market-research, price-comparison, catalog, listings, agents, structured-data, json, ai-agents, scraping-api
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F6D2"
    homepage: https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=aliexpress-product-data
---

# AliExpress Product Data API - Search, Category, Reviews, Seller

Search AliExpress products, browse a category, pull one product in full with all its SKU variants, read translated customer reviews, and open a seller's storefront and catalogue. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Search AliExpress for a product with price, rating, units-sold and free-shipping filters
- Browse a whole AliExpress category and sort by best sellers (units ordered)
- Pull one product in full - current and original price, discount, every SKU variant group, the full image gallery, and the seller
- Read translated buyer reviews with star rating, buyer country, per-SKU variant and photos
- Open a seller's profile (followers, rating, catalogue size) and page through their catalogue
- Do price comparison, dropshipping research, or product-market research on AliExpress

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=aliexpress-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every AliExpress endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/aliexpress/search` | 1 | Products for a query: price with discounts, rating, units sold, delivery estimate, ship-from country, images, plus related search terms |
| `POST /api/v1/aliexpress/category` | 1 | Products within a category id, same product shape and filters as search. Sort by `orders` for the category's best sellers |
| `POST /api/v1/aliexpress/reviews` | 1 | Customer reviews: text with English translation, star rating, buyer country, per-SKU variant, photos, votes, and the product's full rating breakdown. Up to 50 per call |
| `POST /api/v1/aliexpress/product` | 1 | One product in full: title, current/original price, discount, rating, review count, every SKU variant group with options, full image gallery, free-shipping flag, seller (store name, id, positive-feedback rate, followers). Typically responds in 20-60 seconds |
| `POST /api/v1/aliexpress/seller` | 1 | A storefront profile: name, store id, follower count, plus rating, opening date and catalogue size when published. Typically responds in 20-60 seconds |
| `POST /api/v1/aliexpress/seller-products` | 1 | A seller's catalogue, 30 items per page, with `total_products` reporting the full size. Typically responds in 20-60 seconds |

## Two facts that decide how you call this

**`search` and `category` share one product shape.** The same filters (`sort_by`, `min_price`, `max_price`, `ship_from`, `free_shipping`, `ship_to`, `currency`) apply to both. Use `search` for a keyword, `category` for a category id.

**`ship_to` changes what appears, not just prices.** The 2-letter destination country changes prices, VAT and delivery estimates - and which items appear at all, because AliExpress filters by shippability. Send it explicitly for a stable result.

**When you set `min_price`/`max_price`, `total_results` comes back `null`.** AliExpress reports a broadened match count under a price filter, so the total is suppressed rather than shown wrong. The `products` array is still correct.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search terms (1-500 chars) |
| `category_id` | string | -- | Restrict the search to one category id |
| `page` | integer | -- | 1-based, 60 items per full page |
| `sort_by` | string | `best_match` | `best_match`, `orders` (units sold), `price_low`, `price_high` |
| `min_price` / `max_price` | number | -- | Price filter, in the selected currency |
| `ship_from` | string | -- | Only items shipped from this 2-letter country (e.g. `US`, `CN`) |
| `free_shipping` | boolean | -- | Only items with free shipping |
| `ship_to` | string | `US` | 2-letter ISO destination country |
| `currency` | string | `USD` | 3-letter ISO currency |

### Category (`/category`)

Same fields as search, but `category_id` is **required** and there is no `query`.

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | Product id or product URL. Both id spaces are accepted (canonical `1005...`, or the `3256...` alias search pages emit) |
| `page` | integer | -- | 1-based reviews page |
| `page_size` | integer | `20` | Reviews per page, 1-50 |
| `filter` | string | `all` | `all`, `image` (with photos), `local` (buyer's country), `additional` (follow-up reviews), `with_personal` |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | Product id or product URL |
| `ship_to` | string | `US` | 2-letter ISO destination country |
| `currency` | string | `USD` | 3-letter ISO currency |

### Seller (`/seller`) and Seller Products (`/seller-products`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string | required | Store id, or any storefront URL containing `/store/<id>`. Every product response returns its seller's `store_id` |
| `page` | integer | -- | (`seller-products` only) 1-based, 30 items per page |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search, best sellers first, shipped to the UK, priced in GBP
found = requests.post(f"{BASE}/api/v1/aliexpress/search", headers=HEADERS,
    json={"query": "usb c hub", "sort_by": "orders", "max_price": 40,
          "free_shipping": True, "ship_to": "GB", "currency": "GBP"}).json()

row = found["data"]["products"][0]
product_id = row["product_id"]

# 2. One product in full - price, every SKU variant group, the seller
product = requests.post(f"{BASE}/api/v1/aliexpress/product", headers=HEADERS,
    json={"product_id": product_id, "ship_to": "GB", "currency": "GBP"}).json()
store_id = product["data"]["seller"]["store_id"]

# 3. Reviews with photos only
reviews = requests.post(f"{BASE}/api/v1/aliexpress/reviews", headers=HEADERS,
    json={"product_id": product_id, "filter": "image", "page_size": 50}).json()

# 4. The seller's catalogue
catalogue = requests.post(f"{BASE}/api/v1/aliexpress/seller-products", headers=HEADERS,
    json={"store_id": store_id, "page": 1}).json()
```

curl:

```bash
curl -s https://api.scavio.dev/api/v1/aliexpress/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"mechanical keyboard","sort_by":"orders","ship_to":"US","currency":"USD"}'
```

## Response shape

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. `data` carries the product/review/seller payload described in the table above (`products[]`, `products_count`, `total_results`, `reviews[]`, `seller`, and so on).

## Guardrails

- Every call is **1 credit**, including one that comes back empty.
- Send `ship_to` and `currency` explicitly - they change prices, delivery estimates and which items appear at all.
- Under a `min_price`/`max_price` filter, `total_results` is `null` by design; use the `products` array, not the total.
- The `product`, `seller` and `seller-products` endpoints typically take 20-60 seconds. Size your client timeout accordingly (120s is safe).
- Never invent a `sort_by` or `filter` value; unrecognised values are rejected before the request runs.
- Never fabricate prices, ratings, seller details or review text. Only return what the API returned.
- Review text is written by real buyers. Summarise; do not build profiles of individuals.

## Failure handling

- `400` means an invalid or missing parameter. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the product, seller or category could not be resolved.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=aliexpress-product-data).
- `502` / `503` mean the source is temporarily unavailable - wait a few seconds and retry, up to a few times.
- An empty result set is usually the filters - widen the price range, drop `free_shipping`, or change `ship_from`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
