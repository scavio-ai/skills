---
name: sephora-product-data
description: "Sephora product data API: search sephora.com and list any category with price, list and sale price, rating, review count and bestseller, new and exclusive flags, then read one product with every shade or size, stock per shade, ingredients, and Sephora's review summary with pro and con sentiment counts. 3 endpoints, 1 credit each."
version: 1.0.0
tags: sephora, sephora-api, sephora-product-data, beauty, cosmetics, makeup, skincare, fragrance, shades, beauty-prices, product-search, product-data, category-listing, review-summary, review-sentiment, ingredients, retail, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/sephora-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data
---

# Sephora Product Data API - Search, Shades, Prices, Reviews Summary

Search Sephora (sephora.com, US) and list any category: price, list and sale price, value price for sets, rating, review count, extra colors and bestseller, new, exclusive and limited-edition flags, 60 products per page. Read one product with every shade or size it offers, each with its own price, stock and ingredients, plus a summary of what reviews say and pro and con sentiment counts. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find makeup, skincare, hair care or fragrance at Sephora by keyword
- List the products in a Sephora category (lipstick, face serum, foundation) with prices and ratings
- Check a Sephora product's price, sale price, and which shades or sizes are in stock
- Compare shades of one product: shade name, description, size, price, swatch
- Summarize what Sephora reviewers like and dislike about a product
- Read a product's ingredients or suggested usage
- Find what is on sale, new or Sephora-exclusive in a search or category
- Compare Sephora prices with other retailers, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All Sephora endpoints cost **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/sephora/search` | 1 | 60 products per page: product id, sku id, brand, name, URL, image, price, list and sale price, value price for sets, price range, rating, review count, extra colors, sale scope, bestseller, new, exclusive, online-only, limited-edition and sponsored flags. With `zip`, same-day delivery eligibility. Plus category facets and related searches |
| `POST /api/v1/sephora/category` | 1 | 60 products per page of one category in the same shape as search, plus the category id, name and URL, total products, parent category, subcategories with product counts and breadcrumbs |
| `POST /api/v1/sephora/product` | 1 | One product: name, brand, rating, review count, loves count, price range, description, suggested usage, category, breadcrumbs, a review summary with pro and con sentiment counts, and every shade or size the page offers with sku id, shade, size, price, list and sale price, in stock, only-few-left, ingredients, images, swatch, pickup and same-day eligibility |

## Workflow

1. **Find products:** call `/sephora/search` with `query`, or `/sephora/category` with a category name such as `lipstick`. Each row has a `url` and a `product_id`.
2. **One product in full:** call `/sephora/product` with the row's `url` (faster) or its `product_id`.
3. **Shades and stock:** read `skus[]` on the product answer. Each shade or size has its own `price`, `in_stock` and `only_few_left`.
4. **What reviewers say:** read `review_summary` and `review_sentiments[]` on the same answer. There is no review text endpoint.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars) |
| `page` | integer | 1 | 1-based page (1-100), 60 products per page |
| `sort` | string | `relevance` | `relevance`, `best_selling`, `rating`, `price_low`, `price_high` or `newest` |
| `zip` | string | - | US ZIP code. When set, each product carries `same_day_eligible` for same-day delivery to that ZIP |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category` | string | required | The name in a sephora.com/shop/ URL (`lipstick`, `face-serum`, `makeup-cosmetics`), or the full `https://www.sephora.com/shop/...` URL |
| `page` | integer | 1 | 1-based page (1-100), 60 products per page |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | sephora.com product URL, the `url` of a search or category row. Preferred: it answers faster |
| `product_id` | string | one of | Sephora product id like `P510799`, used when `url` is not given |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/sephora/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.sephora.com/product/mac-cosmetics-m-a-cximal-silky-matte-lipstick-P510799"}'
```

Captured response (MAC lipstick; description, breadcrumbs and 31 `skus[]` trimmed, `current_sku` without images and ingredients):

```json
{
  "data": {
    "product_id": "P510799",
    "name": "M·A·Cximal Silky Matte 12HR Wear Lipstick",
    "brand": "MAC Cosmetics",
    "url": "https://www.sephora.com/product/mac-cosmetics-m-a-cximal-silky-matte-lipstick-P510799",
    "rating": 4.5879,
    "review_count": 774,
    "loves_count": 316704,
    "price_min": 16,
    "price_max": 25,
    "review_summary": "Reviews generally reflect favorable impressions of the pigment, texture, and finish, with these features often mentioned positively. Some customers note mild concerns about dryness, transfer, and formula change, though these are less frequently discussed.",
    "review_sentiments": [
      { "sentiment": "Dryness", "type": "cons", "count": 21 },
      { "sentiment": "Finish", "type": "pros", "count": 34 },
      { "sentiment": "Formula Change", "type": "cons", "count": 11 },
      { "sentiment": "Pigment", "type": "pros", "count": 88 },
      { "sentiment": "Texture", "type": "pros", "count": 54 },
      { "sentiment": "Transfer", "type": "cons", "count": 12 }
    ],
    "variation_type": "Color",
    "current_sku": {
      "sku_id": "2764421",
      "variation_type": "Color",
      "variation_value": "Honeylove",
      "variation_description": "light beige toned rose",
      "size": "0.12 oz",
      "price": 25,
      "list_price": 25,
      "sale_price": null,
      "on_sale": false,
      "in_stock": true,
      "only_few_left": false,
      "is_new": false,
      "is_limited_edition": false,
      "is_sephora_exclusive": false,
      "is_online_only": false,
      "pickup_eligible": true,
      "same_day_eligible": true,
      "max_purchase_quantity": 10,
      "highlights": ["Matte Finish"],
      "swatch": "https://www.sephora.com/productimages/sku/s2764421+sw.jpg",
      "url": "https://www.sephora.com/product/mac-cosmetics-m-a-cximal-silky-matte-lipstick-P510799?skuId=2764421"
    },
    "sku_count": 31
  },
  "response_time": 3465,
  "credits_used": 1
}
```

A captured `/search` row for `{"query": "lipstick", "zip": "10001"}`, a product on sale (image trimmed):

```json
{
  "position": 30,
  "product_id": "P501583",
  "sku_id": "2599041",
  "brand": "NARS",
  "name": "Powermatte Long-Lasting Lipstick",
  "url": "https://www.sephora.com/product/nars-powermatte-lipstick-P501583?skuId=2599041",
  "price": 18,
  "list_price": 36,
  "sale_price": 18,
  "value_price": null,
  "price_range": null,
  "price_text": "$36.00",
  "rating": 4.3106,
  "review_count": 367,
  "more_colors": 7,
  "on_sale": true,
  "sale_scope": "full",
  "is_bestseller": false,
  "is_new": false,
  "is_sephora_exclusive": true,
  "is_online_only": false,
  "is_limited_edition": false,
  "sponsored": false,
  "same_day_eligible": true
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def sephora(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/sephora/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. What is on sale in a category
cat = sephora("category", {"category": "lipstick"})
for p in cat["products"]:
    if p["on_sale"]:
        print(p["brand"], p["name"][:40], p["price"], "was", p["list_price"])

# 2. One product: shades in stock and what reviewers say
item = sephora("product", {"url": cat["products"][0]["url"]})
print(item["name"], item["rating"], item["review_count"], "reviews")
print(item["review_summary"])
for s in item["review_sentiments"]:
    print(s["type"], s["sentiment"], s["count"])
print([s["variation_value"] for s in item["skus"] if s["in_stock"]])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Sephora answered.

- **search** - `query`, `page`, `sort`, `zip`, `total_results`, `total_pages`, `count`, `products[]` (`position`, `product_id`, `sku_id`, `brand`, `name`, `url`, `image`, `price`, `list_price`, `sale_price`, `value_price`, `price_range` {`min`, `max`}, `price_text`, `rating`, `review_count`, `more_colors`, `on_sale`, `sale_scope`, `is_bestseller`, `is_new`, `is_sephora_exclusive`, `is_online_only`, `is_limited_edition`, `sponsored`, `same_day_eligible`), `categories[]` {`category_id`, `name`, `product_count`}, `related_searches[]`.
- **category** - `category` {`category_id`, `name`, `seo_name`, `url`, `page_type`}, `page`, `total_results`, `total_pages`, `count`, `parent_category` {`category_id`, `name`, `url`}, `subcategories[]` {`category_id`, `name`, `url`, `product_count`}, `breadcrumbs[]` {`name`, `url`}, `products[]` (the search product shape).
- **product** - `product_id`, `name`, `brand`, `brand_url`, `url`, `rating`, `review_count`, `loves_count`, `price_min`, `price_max`, `description`, `suggested_usage`, `category` {`category_id`, `name`, `url`}, `breadcrumbs[]`, `review_summary`, `review_sentiments[]` {`sentiment`, `type` (`pros` or `cons`), `count`}, `variation_type`, `current_sku`, `sku_count`, `skus[]` (`sku_id`, `variation_type`, `variation_value`, `variation_description`, `size`, `price`, `list_price`, `sale_price`, `on_sale`, `in_stock`, `only_few_left`, `is_new`, `is_limited_edition`, `is_sephora_exclusive`, `is_online_only`, `pickup_eligible`, `same_day_eligible`, `max_purchase_quantity`, `highlights[]`, `ingredients`, `image`, `images[]`, `swatch`, `url`).

## Guardrails

- Prices are in dollars: `25` is $25.00. `price` is what the shopper pays now: the sale price when there is one, else the list price.
- On a listing row whose sizes are priced differently, `price` and `list_price` are the low end; `price_range` holds both ends and `price_text` the range as shown ("$16.00 - $25.00"). Quote the range, or read the exact shade's price from `/product`.
- `value_price` is the stated value of a set's contents, not a price anyone pays.
- `sale_scope` is `full` (every shade on sale) or `partial` (some shades). On a partial sale the product page can leave the sale shades out, so `skus[]` is what the page offers, not necessarily every shade; `more_colors` on the listing row is the site's own count.
- `same_day_eligible` on listings is only set when a `zip` was sent; it is `null` otherwise and always `null` on `/category`.
- `review_summary` and `review_sentiments` are Sephora's own summary of its reviews. There is no review text endpoint; do not quote individual reviews.
- Prices are sephora.com's. Store-level stock is not available; `pickup_eligible` only says the shade can be picked up somewhere.
- Never fabricate prices, shades or stock. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, an unknown `sort`, a ZIP that is not 5 digits, a `category` that is not a sephora.com/shop/ name, or a `product_id` not like `P510799`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/category` means no such category; use the name from a sephora.com/shop/ URL. `404` on `/product` means no such product; re-run the search for a fresh `url`. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data).
- `502` means Sephora is temporarily unavailable. It is not charged; retry after a few seconds.
- A nonsense query is not empty: Sephora falls back to loosely related products, so check that results match before answering.

## SDKs

```bash
pip install scavio==0.32.0
npm install scavio@0.32.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.sephora.search({ query: "lipstick", sort: "best_selling", zip: "10001" });
const lips = await scavio.sephora.category({ category: "lipstick", page: 2 });
const item = await scavio.sephora.product({ url: found.products[0].url });
```

MCP: the Scavio MCP server exposes all 3 endpoints as tools (`search_sephora`, `get_sephora_category`, `get_sephora_product`). Sephora is opt-in: add `sephora` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.30.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,sephora"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/sephora-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data), [category](https://scavio.dev/docs/sephora-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data), [product](https://scavio.dev/docs/sephora-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data). Overview: [Sephora API](https://scavio.dev/sephora-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data).
