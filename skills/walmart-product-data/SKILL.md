---
name: walmart-product-data
description: "Walmart product data API: keyword search, full product detail by item id, customer reviews with the rating breakdown, category listings, the buy-box offer on an item, and marketplace seller storefronts and their catalogs, as structured JSON. 7 endpoints; 1 credit, or 2 when search or category targets walmart.com.mx."
version: 3.0.0
tags: walmart, walmart-product-data, walmart-api, ecommerce, retail, product-search, product-data, pricing, price-monitoring, reviews, buy-box, marketplace-sellers, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F3EA"
    homepage: https://scavio.dev/docs/walmart-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data
---

# Walmart Product Data API - Search, Detail, Reviews, Offers

Search Walmart, read a product in full, page its customer reviews, list a category, look up the buy-box offer on an item, and read a marketplace seller's storefront and catalog. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Search Walmart for products by keyword, price band or sort order
- Look up a Walmart item by its item id (usItemId)
- Read customer reviews and the rating breakdown for a Walmart product
- List the products inside a Walmart category
- Check who holds the buy box on a Walmart listing and at what price
- Look up a Walmart marketplace seller: rating, review count, Pro Seller badge
- See what a Walmart marketplace seller lists
- Compare Walmart pricing against another retailer (pair with scavio-amazon, scavio-ebay or scavio-target)
- Search the Canadian (walmart.ca) or Mexican (walmart.com.mx) marketplace

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=walmart-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Endpoints in this skill cost 1 credit each unless the table below says otherwise.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`.

| Endpoint | Credits | Description |
|---|---|---|
| `POST /api/v1/walmart/search` | 1, or 2 when `domain` is `com.mx` | Keyword search: `products[]`, `products_count`, `location` |
| `POST /api/v1/walmart/product` | 1 | Full product detail by item id |
| `POST /api/v1/walmart/reviews` | 1 | Customer reviews plus the rating breakdown |
| `POST /api/v1/walmart/category` | 1, or 2 when `domain` is `com.mx` | Products in a category, same shape as search |
| `POST /api/v1/walmart/offers` | 1 | The buy-box seller for an item |
| `POST /api/v1/walmart/seller` | 1 | Marketplace seller storefront |
| `POST /api/v1/walmart/seller-products` | 1 | A seller's catalog (path is hyphenated) |

### Cost rule

Cost is a function of the request body, not a constant. `domain` is the only price-bearing parameter:

- `domain: "com"` (US, the default) costs 1 credit
- `domain: "ca"` (Canada) costs 1 credit
- `domain: "com.mx"` (Mexico) costs 2 credits

Only `/search` and `/category` accept `domain`, so only those two can ever cost 2. The other five endpoints are always 1 credit. Never quote a flat price for search or category without stating the domain rule.

## Workflow

1. **Find items:** call `/walmart/search` with `query`. The item id is `id` on each row of `data.products[]` — that is the value the other endpoints take as `product_id`.
2. **Read an item:** call `/walmart/product` with `product_id`.
3. **Reviews:** call `/walmart/reviews` with the same `product_id`, paging with `page` (10 reviews per page).
4. **Browse a category:** call `/walmart/category` with `category_id`.
5. **Buy box:** call `/walmart/offers` with `product_id` to see who currently wins the buy box and at what price.
6. **Sellers:** a product, search or offers response carries `seller_catalog_id`. Pass that numeric id as `seller_id` to `/walmart/seller` for the storefront and to `/walmart/seller-products` for the catalog.

`search`, `reviews` and `category` paginate with `page` (1-based). `product`, `offers`, `seller` and `seller-products` do not paginate at all — there is no page or cursor parameter on them.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search query (1-500 chars) |
| `page` | integer >= 1 | -- | Results page, 1-based |
| `start_page` | integer >= 1 | -- | Deprecated alias for `page`. Prefer `page` |
| `sort_by` | string | `best_match` | `best_match`, `price_low`, `price_high`, `best_seller`, `rating_high`, `new` |
| `min_price` | number | -- | Minimum price filter |
| `max_price` | number | -- | Maximum price filter |
| `fulfillment_speed` | string | -- | `today` or `tomorrow` only |
| `fulfillment_type` | string | -- | `in_store` for in-store pickup |
| `domain` | string | `com` | `com` (1 credit), `ca` (1 credit), `com.mx` (2 credits) |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | Walmart item id (usItemId), e.g. `13544111159` |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | Walmart item id (usItemId) |
| `page` | integer >= 1 | -- | Reviews page, 1-based. 10 reviews per page |
| `sort` | string | -- | `relevancy`, `submission-desc`, `submission-asc`, `rating-desc`, `rating-asc`, `helpful-desc` |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | required | Leaf id (`1095191`) or full underscore path (`3944_133251_1095191`) |
| `limit` | integer >= 1 | -- | Trims the returned products. Applied after fetching, so it does NOT reduce cost |
| `page` | integer >= 1 | -- | Results page, 1-based |
| `sort_by` | string | `best_match` | Same six values as search |
| `min_price` | number | -- | Minimum price filter |
| `max_price` | number | -- | Maximum price filter |
| `fulfillment_speed` | string | -- | `today` or `tomorrow` only |
| `domain` | string | `com` | `com` (1 credit), `ca` (1 credit), `com.mx` (2 credits) |

### Offers (`/offers`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | Walmart item id (usItemId), e.g. `2979510112` |

### Seller (`/seller`) and seller products (`/seller-products`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `seller_id` | string | required | NUMERIC catalog seller id, as returned in `seller_catalog_id`. Example `101480084` |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search (1 credit on the default com domain)
results = requests.post(f"{BASE}/api/v1/walmart/search", headers=HEADERS,
    json={"query": "wireless headphones", "sort_by": "price_low", "max_price": 100}).json()

product_id = results["data"]["products"][0]["id"]   # search rows carry `id`, not `product_id`

# 2. Full product detail
product = requests.post(f"{BASE}/api/v1/walmart/product", headers=HEADERS,
    json={"product_id": product_id}).json()

# 3. Reviews, page 2 (10 per page)
reviews = requests.post(f"{BASE}/api/v1/walmart/reviews", headers=HEADERS,
    json={"product_id": product_id, "page": 2, "sort": "rating-desc"}).json()

# 4. Buy box for an item
offers = requests.post(f"{BASE}/api/v1/walmart/offers", headers=HEADERS,
    json={"product_id": "2979510112"}).json()

# 5. Seller storefront, then their catalog (numeric seller_catalog_id)
seller = requests.post(f"{BASE}/api/v1/walmart/seller", headers=HEADERS,
    json={"seller_id": "101480084"}).json()
catalog = requests.post(f"{BASE}/api/v1/walmart/seller-products", headers=HEADERS,
    json={"seller_id": "101480084"}).json()

# 6. Mexican marketplace search: this call costs 2 credits, not 1
mx = requests.post(f"{BASE}/api/v1/walmart/search", headers=HEADERS,
    json={"query": "audifonos", "domain": "com.mx"}).json()
```

## Response

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`, plus an optional `warnings[]` array of strings that Walmart adds when the request used a retired parameter.

- **search** puts the rows in `data.products[]` with `data.products_count`, and reports the Walmart store the results were served against in `data.location`. **category** returns the same product shape as search.
- **product** returns price, rating, images, specifications, availability and seller.
- **reviews** returns the review bodies with ratings, text, author and date, plus the rating breakdown.
- **offers** returns price, seller, condition and the buy-box flag.
- **seller** returns store name, rating, review count, Pro Seller badge and business details.
- **seller-products** returns the seller's catalog with `total_count`.

Read `credits_used` on the response rather than assuming a cost, since search and category are body-priced.

## Changed in 3.0.0

If you have an older version of this skill installed, stop sending these. They were tested against the live site before removal, and the API now answers them with a `warnings[]` entry rather than an error, which means a request that looks successful was silently unfiltered:

- **`device`** is gone. Desktop, mobile and tablet return identical page data, so the response would not change.
- **`delivery_zip`** is gone. Walmart mints its location cookies server-side and ignores any sent to it, so results always come back against its default store. The store actually used is reported in `data.location`.
- **`store_id`** is gone, for the same reason as `delivery_zip`. The store used is reported in `data.location`.
- **`fulfillment_speed: "2_days"`** is gone. It leaked items 3-4 days out.
- **`fulfillment_speed: "anytime"`** is gone. It was a no-op. To mean "anytime", omit the parameter entirely.

`domain` is NOT retired. It is live, it is the price-bearing parameter, and it is the only way to reach walmart.ca and walmart.com.mx.

New since 2.x: `/reviews`, `/category`, `/offers`, `/seller` and `/seller-products`. `sort_by` gained `rating_high` and `new`. `search` and `product` both changed response shape.

## Guardrails

- Never fabricate product names, prices, item ids, ratings or availability. Only return data the API returned.
- `/offers` returns the BUY-BOX SELLER ONLY. It is not the full offer list, and must never be described as one. If the user wants every seller on an item, say that this API cannot enumerate them.
- `/seller-products` returns roughly the first 40 items, server-rendered. There is no pagination on it. `total_count` reports the seller's real catalog size, so the two numbers will disagree and that is expected. Do not invent a `page` parameter.
- `seller_id` must be the NUMERIC catalog seller id from `seller_catalog_id`. The GUID form of `seller_id` returns 404.
- `domain` is accepted on `/search` and `/category` only. walmart.ca product pages could not be fetched at all in testing, so the id-keyed endpoints are US-only.
- `limit` on `/category` trims the response after fetching. It does not reduce the credit cost.
- `category_id` accepts either the leaf id or the full underscore-joined path.
- `sort_by`, `fulfillment_speed`, `fulfillment_type` and `domain` are closed enums - a value outside them is a `400`. Send only the values listed above; in particular `fulfillment_speed` no longer accepts `2_days` or `anytime`, and to mean "anytime" you omit the parameter.
- Always include the product URL so the user can verify and complete the purchase.

## Failure handling

- `400` means an invalid or missing parameter. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` on `/seller` or `/seller-products` almost always means a GUID was sent instead of the numeric `seller_catalog_id`.
- `429` means a rate or usage limit was exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data).
- `502` / `503` mean the upstream is temporarily unavailable. Transient 502s happen on Walmart; wait a few seconds and retry once before reporting failure.
- If a response carries `warnings[]`, surface it to the user. It means part of their request was ignored.
- If search returns nothing, relax the filters (drop `fulfillment_speed`, widen `min_price`/`max_price`) and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Docs

- [Walmart search](https://scavio.dev/docs/walmart-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)
- [Walmart product](https://scavio.dev/docs/walmart-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)
- [Walmart reviews](https://scavio.dev/docs/walmart-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)
- [Walmart category](https://scavio.dev/docs/walmart-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)
- [Walmart offers](https://scavio.dev/docs/walmart-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)
- [Walmart seller](https://scavio.dev/docs/walmart-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)
- [Walmart seller products](https://scavio.dev/docs/walmart-seller-products?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)
