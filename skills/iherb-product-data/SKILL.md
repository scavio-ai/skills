---
name: iherb-product-data
description: "iHerb product data API: search iherb.com by keyword or brand with price, list price, discount, rating, review count, stock and recent sales, read one product with UPC, price per serving, supplement facts, ingredients, variants and best-seller rankings, check price and stock for up to 50 products in one call, and read the review summary with the star histogram and top positive and critical review. US store, USD. 4 endpoints, 2 credits each."
version: 1.0.0
tags: iherb, iherb-api, iherb-product-data, supplements, vitamins, health, wellness, sports-nutrition, beauty, supplement-facts, ingredients, product-search, product-data, bulk-prices, review-summary, ratings, upc-lookup, online-retail, retail, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/iherb-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data
---

# iHerb Product Data API - Search, Prices, Supplement Facts, Ratings

Search iHerb (supplements, vitamins, sports nutrition, beauty, grocery) by keyword, optionally narrowed to one brand, with price, list price, discount, rating, review count, stock, badges and recent sales, 48 products per page. Read one product with UPC, part number, price per serving, supplement facts, description, suggested use, ingredients, warnings, every variant and its best-seller rankings. Check price and stock for up to 50 products in one call, and read a product's review summary: average rating, star histogram, review counts per language, and the top positive and top critical review. All endpoints return structured JSON from the US store in US dollars.

## When to trigger

Use this skill when the user asks to:
- Find supplements, vitamins or other products on iHerb by keyword or brand
- Check an iHerb product's price, list price, discount or price per serving
- Read a supplement's facts panel, ingredients, suggested use or warnings
- Look up an iHerb product's UPC, part number, variants or best-seller rank
- Monitor iHerb prices and stock across a list of products
- Summarize what reviewers think of an iHerb product (star histogram, top positive and critical review)
- Compare iHerb prices with Amazon, Walmart or other retailers

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 2 credits.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All iHerb endpoints cost **2 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/iherb/search` | 2 | 48 products per page: product id, part number, name, brand and brand code, URL, image, price, list price, original price and discount percent when discounted, rating, review count, in-stock flag, badges ("Quality Pick", "Best seller", "iHerb Brands", "New"), recent sales ("30K+ sold in 30 days"), category, sponsored flag. Total results, total pages and brand filters (brand code, name, match count) |
| `POST /api/v1/iherb/product` | 2 | One product by id or URL: name, brand, part number, UPC, price, list price, discount, price per serving or unit, stock status, discontinued and coming-soon flags, quantity limit, expiration date, first-available date, package quantity, weight and dimensions, rating, review count, breadcrumbs, best-seller rankings by category, badges, variants (size, potency, flavor) with product ids, supplement facts, description, suggested use, ingredients, warnings, images |
| `POST /api/v1/iherb/prices` | 2 | Price, list price, discount, in-stock flag, rating and review count for up to 50 products in one call, one row per id in request order; unknown ids listed in `not_found` |
| `POST /api/v1/iherb/reviews` | 2 | Review summary for one product: average rating, review count, star histogram (count and percent per star), review counts per language, and the full top positive and top critical review |

## Workflow

1. **Find products:** call `/iherb/search` with `query`. Each row has a `product_id` and a `brand_code`. To stay within one brand, repeat with `brand_code` (from a row or from `brand_filters`).
2. **One product in full:** call `/iherb/product` with the `product_id` (or the iherb.com `url`) for supplement facts, ingredients, variants and rankings. Search and product take 6-20 seconds; give them a 60-second timeout.
3. **Watch many products:** call `/iherb/prices` with up to 50 `product_ids`. One call (2 credits) re-checks price and stock for the whole list, so do not loop `/product` for monitoring.
4. **What reviewers say:** call `/iherb/reviews` with the `product_id` for the star histogram and the top positive and critical review.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars) |
| `page` | integer | 1 | 1-based page (1-500), 48 results per page |
| `sort` | string | iHerb's featured order | `relevance`, `best_selling`, `rating`, `price_asc`, `price_desc`, `newest`, `percent_off` (highest discount first) or `review_count` |
| `brand_code` | string | - | Only this brand, by iHerb brand code (`CGN` for California Gold Nutrition, `NOW` for NOW Foods): a row's `brand_code` or a `brand_filters` entry |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | iHerb product id, the number at the end of an iherb.com `/pr/` URL (`"70316"`) |
| `url` | string | one of | An iherb.com product URL. Data is always the US store's, whatever the URL's country |

### Prices (`/prices`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_ids` | string[] | required | 1-50 iHerb product ids. Duplicates are answered once |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | iHerb product id |
| `url` | string | one of | An iherb.com product URL |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/iherb/prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_ids": ["70316", "77548", "10421", "124745", "10056", "113543", "77549", "101967", "148171"]}'
```

Captured response (nine vitamin D products, two rows shown):

```json
{
  "data": {
    "currency": "USD",
    "count": 9,
    "not_found": [],
    "products": [
      {
        "product_id": "70316",
        "found": true,
        "name": "Vitamin D3, 125 mcg (5,000 IU), 90 Fish Gelatin Softgels",
        "url": "https://www.iherb.com/pr/california-gold-nutrition-vitamin-d3-125-mcg-5-000-iu-90-fish-gelatin-softgels/70316",
        "part_number": "CGN-01065",
        "brand": "California Gold Nutrition",
        "brand_code": "CGN",
        "is_iherb_brand": true,
        "price": 6.07,
        "list_price": 6.07,
        "discount_percent": 0,
        "discount_type": 0,
        "discount_message": null,
        "is_in_cart_discount": false,
        "in_stock": true,
        "is_available_to_purchase": true,
        "status_code": 0,
        "rating": 4.8,
        "review_count": 324874
      },
      {
        "product_id": "10421",
        "found": true,
        "name": "Vitamin D-3, High Potency, 125 mcg (5,000 IU), 120 Softgels",
        "url": "https://www.iherb.com/pr/now-foods-vitamin-d-3-high-potency-125-mcg-5-000-iu-120-softgels/10421",
        "part_number": "NOW-00372",
        "brand": "NOW Foods",
        "brand_code": "NOW",
        "is_iherb_brand": false,
        "price": 5.45,
        "list_price": 5.45,
        "discount_percent": 0,
        "discount_type": 0,
        "discount_message": null,
        "is_in_cart_discount": false,
        "in_stock": true,
        "is_available_to_purchase": true,
        "status_code": 0,
        "rating": 4.9,
        "review_count": 277474
      }
    ]
  },
  "response_time": 1592,
  "credits_used": 2
}
```

A captured `/reviews` response for `{"product_id": "70316"}` (languages trimmed to three; this product has no top critical review):

```json
{
  "product_id": "70316",
  "average_rating": 4.8,
  "review_count": 324874,
  "rating_histogram": {
    "five": { "count": 286910, "percent": 88 },
    "four": { "count": 28200, "percent": 9 },
    "three": { "count": 7470, "percent": 2 },
    "two": { "count": 1319, "percent": 0 },
    "one": { "count": 975, "percent": 0 }
  },
  "languages": [
    { "language_code": "en-US", "language": "English", "count": 54113 },
    { "language_code": "ru-RU", "language": "Russian", "count": 149203 },
    { "language_code": "ko-KR", "language": "Korean", "count": 23618 }
  ],
  "top_positive_review": {
    "review_id": "f5830fcc-de50-4fbe-b645-42751a3ad46c",
    "rating": 5,
    "title": "Excellent!",
    "text": "I'm so glad I found these Vitamin D3 softgels! I was feeling really run down and depleted, but after just a few days of taking these, I feel so much better. ...",
    "author": "iHerb customer",
    "author_country": "Spain",
    "country_code": "ES",
    "language_code": "en-US",
    "posted_at": "2022-08-20T16:08:13.958Z",
    "verified_purchase": true,
    "helpful_yes": 112,
    "helpful_no": 0,
    "images": []
  },
  "top_critical_review": null
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def iherb(endpoint, body):
    # search and product take 6-20 seconds; a generous timeout keeps them from failing early.
    r = requests.post(f"{BASE}/api/v1/iherb/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Best-selling vitamin D from one brand (2 credits)
rows = iherb("search", {"query": "vitamin d", "brand_code": "CGN", "sort": "best_selling"})["products"]
for p in rows[:5]:
    print(p["name"][:60], p["price"], p["rating"], p["review_count"], p["recent_sales"])

# 2. Re-check price and stock for up to 50 ids in one call (2 credits)
ids = [p["product_id"] for p in rows[:50]]
watch = iherb("prices", {"product_ids": ids})
for p in watch["products"]:
    if p["found"]:
        print(p["product_id"], p["price"], "list", p["list_price"], "in stock" if p["in_stock"] else "out of stock")

# 3. One product in full and its review summary (2 credits each)
item = iherb("product", {"product_id": rows[0]["product_id"]})
print(item["upc"], item["price_per_unit"], item["supplement_facts"]["serving_size"])
summary = iherb("reviews", {"product_id": rows[0]["product_id"]})
print(summary["average_rating"], summary["rating_histogram"]["one"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when iHerb answered.

- **search** - `query`, `page`, `sort`, `brand_code`, `total_results`, `total_pages`, `count`, `brand_filters[]` {`brand_code`, `name`, `count`}, `products[]` (`position`, `product_id`, `part_number`, `name`, `brand`, `brand_code`, `url`, `image`, `price`, `list_price`, `original_price`, `discount_percent`, `discount_type`, `rating`, `review_count`, `in_stock`, `inventory_status`, `is_discontinued`, `is_trial`, `sponsored`, `badges[]`, `recent_sales`, `category`).
- **product** - `product_id`, `name`, `brand`, `brand_code`, `brand_url`, `part_number`, `upc`, `url`, `price`, `list_price`, `currency`, `discount_percent`, `discount_amount`, `price_per_unit` {`text`, `amount`, `unit`}, `discounted_price_per_unit` {`text`, `amount`, `unit`}, `availability`, `in_stock`, `stock_status`, `is_available_to_purchase`, `is_discontinued`, `is_coming_soon`, `recent_sales`, `quantity_limit`, `expiration_date`, `first_available`, `package_quantity`, `shipping_weight`, `dimensions`, `weight`, `rating`, `review_count`, `category`, `breadcrumbs[]` {`name`, `url`}, `is_iherb_brand`, `badges[]`, `rankings[]` {`rank`, `category`, `url`}, `variants[]` {`attribute`, `options[]` {`value`, `product_id`, `url`, `price`, `selected`, `in_stock`}}, `supplement_facts` {`serving_size`, `servings_per_container`, `nutrients[]` {`name`, `amount`, `daily_value`}, `notes[]`}, `description`, `suggested_use`, `ingredients`, `warnings`, `images[]`.
- **prices** - `currency`, `count`, `not_found[]`, `products[]` (`product_id`, `found`, `name`, `url`, `part_number`, `brand`, `brand_code`, `is_iherb_brand`, `price`, `list_price`, `discount_percent`, `discount_type`, `discount_message`, `is_in_cart_discount`, `in_stock`, `is_available_to_purchase`, `status_code`, `rating`, `review_count`). An unknown id is `{ product_id, found: false }`.
- **reviews** - `product_id`, `average_rating`, `review_count`, `rating_histogram` {`five`, `four`, `three`, `two`, `one`: {`count`, `percent`}}, `languages[]` {`language_code`, `language`, `count`}, `top_positive_review` and `top_critical_review` (each `null` or {`review_id`, `rating`, `title`, `text`, `author`, `author_country`, `country_code`, `language_code`, `posted_at`, `verified_purchase`, `helpful_yes`, `helpful_no`, `images[]`}).

## Guardrails

- Online only: iHerb has no stores, so there is no store locator, store price or store stock. `in_stock` is the online stock flag.
- Every answer is the US store in US dollars (`6.07` is $6.07), even for a URL from another iHerb country site. Never quote it as another country's price.
- `price` is what the product sells for now and `list_price` the regular price; they are equal when not discounted. `discount_percent` is the site's own figure. `discount_type`, `inventory_status` and `status_code` are iHerb's raw codes whose meaning is not published; do not interpret them.
- `/reviews` is a SUMMARY, not a review list: the star histogram, counts per language, and at most one top positive and one top critical review. Either top review can be `null`. There is no endpoint to page through all reviews; never claim to have read them.
- Histogram `percent` values are whole numbers as iHerb rounds them, so they need not sum to 100.
- `/prices` takes up to 50 ids per call and keeps request order. An unknown id is not an error: its row has `found: false` and it is listed in `not_found`. Use it for monitoring instead of repeated `/product` calls.
- On `/product`, a variant option's `price` can be `null`; get that variant's price from `/prices` with its `product_id`.
- Search rows can be `sponsored: true`; say so when ranking results. A page past the last returns an empty `products` list.
- Never fabricate prices, stock, supplement facts or reviews. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, an unknown `sort`, a `brand_code` that is not 2-10 letters or digits, `page` outside 1-500, neither `product_id` nor `url`, a non-numeric id, or more than 50 `product_ids`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` or `/reviews` means no such product; use the number at the end of an iherb.com `/pr/` URL. `404` on `/search` means no listing for that query and `brand_code`. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data).
- `502` or `503` means iHerb is temporarily unavailable. It is not charged; retry after a few seconds. Search and product are slow (6-20 seconds), so allow a minute per call before treating it as failed.

## SDKs

```bash
pip install scavio==0.33.0
npm install scavio@0.33.0
```

```js
import { Scavio } from "scavio";

// reads SCAVIO_API_KEY; search and product can take 20 seconds, so raise the 30s default timeout
const scavio = new Scavio({ timeout: 60_000 });
const { data: found } = await scavio.iherb.search({ query: "vitamin d", sort: "best_selling" });
const ids = found.products.slice(0, 50).map((p) => p.product_id);
const prices = await scavio.iherb.prices({ product_ids: ids });
const item = await scavio.iherb.product({ product_id: ids[0] });
const summary = await scavio.iherb.reviews({ product_id: ids[0] });
```

MCP: the Scavio MCP server exposes all 4 endpoints as tools (`search_iherb`, `get_iherb_product`, `get_iherb_prices`, `get_iherb_reviews`). iHerb is opt-in: add `iherb` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.31.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,iherb"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/iherb-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data), [product](https://scavio.dev/docs/iherb-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data), [prices](https://scavio.dev/docs/iherb-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data), [reviews](https://scavio.dev/docs/iherb-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data). Overview: [iHerb API](https://scavio.dev/iherb-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data).
