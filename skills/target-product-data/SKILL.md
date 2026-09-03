---
name: target-product-data
description: "Target.com product data: keyword search, category browsing, product detail by TCIN with price, rating, images, specifications, variants and fulfillment, and reviews with the star breakdown and per-attribute averages. Store-aware pricing via store_id. 4 endpoints, 1 credit each, structured JSON."
version: 1.0.0
tags: target-product-data, target-com, retail, ecommerce, product-search, tcin, product-reviews, price-tracking, store-availability, competitor-research, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    emoji: "\U0001F3AF"
    homepage: https://scavio.dev/docs/target-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data
---

# Target Product Data API - Search, Category, TCIN Detail, Reviews

Search Target.com, the US retailer: browse a category, read a product by its TCIN, and pull reviews with the rating breakdown, per-attribute averages and guest photos. All endpoints return structured JSON and cost 1 credit each.

Target calls are slow. See the latency table below and set your client timeout accordingly.

## When to trigger

Use this skill when the user asks to:
- Search Target.com for products by keyword
- Browse the products in a Target category
- Look up a Target product by TCIN (Target's catalog id)
- Check a Target product's price or availability at a specific store
- Read Target reviews, the star breakdown or per-attribute ratings for a product
- Compare Target pricing against another retailer (pair with scavio-walmart, scavio-amazon or scavio-ebay)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Every endpoint costs **1 credit**.

| Endpoint | Credits | Typical latency | Description |
|---|---|---|---|
| `POST /api/v1/target/search` | 1 | ~9s | Search Target.com: prices, ratings, badges, promotions |
| `POST /api/v1/target/category` | 1 | ~37s | Products in a category, same shape as search plus the breadcrumb |
| `POST /api/v1/target/product` | 1 | ~4s | Product detail by TCIN: price, rating, images, specifications, variants, return policy, fulfillment |
| `POST /api/v1/target/reviews` | 1 | ~40s | Reviews with the rating breakdown, per-attribute averages and guest photos |

Latency, not cost, is the thing to plan around. A `502`-then-retry has been observed taking 105 seconds. Set a client timeout of at least 120 seconds, and prefer async or background execution if the user is waiting on a response.

## Workflow

1. **Find products:** call `/target/search` with `keyword`. Read the TCIN off each row.
2. **Browse a category:** call `/target/category` with `category_id`, which is the segment after `N-` in a target.com `/c/` URL.
3. **Read a product:** call `/target/product` with `tcin`.
4. **Reviews:** call `/target/reviews` with the same `tcin`.
5. **Store-specific prices:** pass `store_id` on any of the four endpoints. It defaults to `3991`. Unlike Walmart, this is a real request parameter here: prices and availability are the caller's choice.

`search` and `category` paginate with `page` plus `count`. `product` and `reviews` do not paginate.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | required | Search query (1-500 chars) |
| `page` | integer >= 1 | -- | Results page, 1-based |
| `count` | integer 1-28 | `24` | Results per page. Target rejects anything above 28 outright |
| `sort` | string | `relevance` | `relevance`, `featured`, `price_low`, `price_high`, `rating_high`, `best_seller`, `newest` |
| `store_id` | string | `3991` | Numeric Target store id. Sets the store prices and availability are read against |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | required | The segment after `N-` in a target.com `/c/` URL, e.g. `5xtg6` |
| `page` | integer >= 1 | -- | Results page, 1-based |
| `count` | integer 1-28 | `24` | Results per page |
| `sort` | string | `relevance` | Same seven values as search |
| `store_id` | string | `3991` | Numeric Target store id |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tcin` | string | required | Target catalog id, e.g. `1010453160` |
| `store_id` | string | `3991` | Numeric Target store id |

A child TCIN is answered by its variation parent, with the child present in `variants`.

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tcin` | string | required | Target catalog id |
| `limit` | integer >= 1 | -- | TRIMS the returned bodies only. There is no paging |
| `store_id` | string | `3991` | Numeric Target store id |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
# Target calls are slow: give the client room.
TIMEOUT = 120

# 1. Search (~9s)
results = requests.post(f"{BASE}/api/v1/target/search", headers=HEADERS, timeout=TIMEOUT,
    json={"keyword": "airpods", "sort": "price_low", "count": 28}).json()

# 2. Category browse (~37s) - category_id is the segment after N- in a /c/ URL
category = requests.post(f"{BASE}/api/v1/target/category", headers=HEADERS, timeout=TIMEOUT,
    json={"category_id": "5xtg6", "page": 1}).json()

# 3. Product detail by TCIN (~4s), priced at a specific store
product = requests.post(f"{BASE}/api/v1/target/product", headers=HEADERS, timeout=TIMEOUT,
    json={"tcin": "1010453160", "store_id": "3991"}).json()

# 4. Reviews (~40s). Returns 8 bodies maximum, whatever review_count says.
reviews = requests.post(f"{BASE}/api/v1/target/reviews", headers=HEADERS, timeout=TIMEOUT,
    json={"tcin": "1010453160"}).json()
```

## Response

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **search** returns the product rows with prices, ratings, badges and promotions.
- **category** returns the same row shape as search, plus the category breadcrumb.
- **product** returns price, rating, images, specifications, variants, return policy and fulfillment.
- **reviews** returns the review bodies with the rating breakdown, per-attribute averages and guest photos.

`seller_id` and `seller_name` are **null for first-party stock, which is most of Target**. Null there means "sold by Target", not missing data. Only Target Plus marketplace rows name a vendor, and how many of those appear varies enormously by query: in testing, 22 of 24 rows for "office chair" carried a vendor and 0 of 24 for "patio furniture" did.

## Guardrails

- Never fabricate product names, prices, TCINs, ratings or review text. Only return data the API returned.
- **Do not overpromise speed.** Product is roughly 4s, search roughly 9s, category roughly 37s and reviews roughly 40s. If the user is building something interactive, tell them to run these in the background.
- **`/reviews` returns 8 review bodies maximum**, regardless of what `review_count` on the product says. `limit` only trims that set further. There is no `page` and no `offset` parameter. Never tell the user they can page through all reviews, and never present 8 bodies as the complete review corpus. The rating breakdown does cover all reviews.
- A null `seller_id` / `seller_name` means the item is sold by Target itself. Do not report it as missing or unknown data.
- `count` is capped at 28. Target rejects anything higher outright.
- Concurrency, not credits, is the real ceiling. Simultaneous requests are capped per plan and shared across Target, eBay, Walmart, Amazon and Google -- 1 on free and pay-as-you-go, up to 50 on Growth -- and a single Target call can hold a slot for 40 seconds. Do not fan out dozens of Target calls in parallel.
- Prices and availability are store-dependent. If the user cares about a specific store, pass `store_id`; if you did not pass one, say the numbers are for the default store.
- Always include the product URL so the user can verify.

## Failure handling

- `400` means an invalid or missing parameter, e.g. a `count` above 28. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the TCIN or category id was not found. Check that `category_id` is the segment after `N-` in the `/c/` URL, not the whole path.
- `429` means a rate or usage limit was exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data).
- `502` / `503` mean the upstream is temporarily unavailable. Retry once after a few seconds; a 502-then-retry has been seen to complete at 105 seconds total, so do not abandon the request too early.
- A client-side timeout is far more likely than an API error here. Raise the timeout before assuming the endpoint is broken.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Docs

- [Target search](https://scavio.dev/docs/target-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data)
- [Target category](https://scavio.dev/docs/target-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data)
- [Target product](https://scavio.dev/docs/target-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data)
- [Target reviews](https://scavio.dev/docs/target-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data)
