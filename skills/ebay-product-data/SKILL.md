---
name: ebay-product-data
description: "eBay product data API: search live or SOLD listings for comps and resale pricing (price, condition, bids, shipping, seller, feedback), read one listing in full with item specifics, shipping, returns and auction state, and pull a seller's feedback score, items sold and location. 3 endpoints, 1 credit each."
version: 1.0.0
tags: ebay, ebay-product-data, sold-listings, price-research, resale, ecommerce, marketplace, product-data, seller-profile, price-monitoring, arbitrage, auctions, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F4E6"
    homepage: https://scavio.dev/docs/ebay-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=ebay-product-data
---

# eBay Product Data API - Live and Sold Listings, Sellers

Search eBay's live listings or its SOLD listings, read a single listing in full, and pull a seller's public profile card. All endpoints return structured JSON and cost 1 credit each.

## When to trigger

Use this skill when the user asks to:
- Find what something actually SOLD for on eBay (comps, resale pricing, market value)
- Search live eBay listings by keyword, price band, condition or buying format
- Filter to auctions, Buy It Now or Best Offer listings
- Read one eBay listing in full: item specifics, shipping, returns, auction state
- List everything a particular eBay seller has for sale
- Look up an eBay seller's feedback score, items sold and location
- Compare eBay resale prices against retail (pair with scavio-amazon, scavio-walmart or scavio-target)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=ebay-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every endpoint costs **1 credit**.

| Endpoint | Credits | Description |
|---|---|---|
| `POST /api/v1/ebay/search` | 1 | Search live or sold listings: price, condition, bids, shipping, seller, feedback |
| `POST /api/v1/ebay/product` | 1 | One listing in full: images, item specifics, shipping, returns, auction state, seller |
| `POST /api/v1/ebay/seller` | 1 | Seller profile card: store name, feedback score and percentage, items sold, followers, location, categories |

## Workflow

1. **Price research:** call `/ebay/search` with `query` and `sold: true`. This is the differentiating call. It searches completed listings that actually sold, which is what a comp is.
2. **Live listings:** call `/ebay/search` with `query` and no `sold` flag.
3. **Read a listing:** call `/ebay/product` with `item_id` (the eBay item number, or a full `ebay.com/itm/...` URL — tracking parameters are discarded).
4. **List a seller's inventory:** call `/ebay/search` with `seller` set and NO `query`. That is the paginated route through a seller's catalogue.
5. **Seller reputation:** call `/ebay/seller` with the username as it appears in `ebay.com/usr/<name>`.

`/search` paginates with `page`. `/product` and `/seller` do not paginate.

## Parameters

### Search (`/search`)

`query` or `seller` is required. At least one must be present.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Search keywords (1-500 chars) |
| `seller` | string | one of | Scope to one seller (1-64 chars). Usable with NO query to page their whole catalogue |
| `page` | integer >= 1 | -- | Results page, 1-based |
| `per_page` | integer | `60` | Accepts ONLY `60`, `120` or `240` |
| `sort_by` | string | `best_match` | `best_match`, `ending_soonest`, `newly_listed`, `price_low`, `price_high` |
| `min_price` | number >= 0 | -- | Minimum price filter |
| `max_price` | number >= 0 | -- | Maximum price filter |
| `condition` | string | -- | `new`, `open_box`, `refurbished`, `used`, `for_parts` |
| `buying_format` | string | -- | `auction`, `buy_it_now`, `best_offer` |
| `free_shipping` | boolean | -- | Only listings with free shipping |
| `sold` | boolean | -- | Search completed listings that actually SOLD |
| `category_id` | string | -- | Numeric eBay category id, e.g. `112529` |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string | required | eBay item number (e.g. `168591664725`) or a full `ebay.com/itm/...` URL |

### Seller (`/seller`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `seller` | string | required | eBay username as in `ebay.com/usr/<name>`, e.g. `red-rock-uk` (1-64 chars) |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. What did it actually sell for? (the price-research call)
sold = requests.post(f"{BASE}/api/v1/ebay/search", headers=HEADERS,
    json={"query": "nintendo switch oled", "sold": True, "condition": "used"}).json()

# 2. Live listings, cheapest first, 120 per page
live = requests.post(f"{BASE}/api/v1/ebay/search", headers=HEADERS,
    json={"query": "nintendo switch oled", "sort_by": "price_low", "per_page": 120}).json()

# 3. One listing in full
item = requests.post(f"{BASE}/api/v1/ebay/product", headers=HEADERS,
    json={"item_id": "168591664725"}).json()

# 4. A seller's whole catalogue: /search with seller and no query
catalogue = requests.post(f"{BASE}/api/v1/ebay/search", headers=HEADERS,
    json={"seller": "red-rock-uk", "page": 1}).json()

# 5. That seller's reputation card
profile = requests.post(f"{BASE}/api/v1/ebay/seller", headers=HEADERS,
    json={"seller": "red-rock-uk"}).json()
```

## Response

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **search** returns the listing rows with price, condition, bids, shipping, seller and feedback, alongside `count` and `total_results`.
- **product** returns price, condition, images, item specifics, shipping, returns, auction state and seller.
- **seller** returns store name, feedback score and percentage, items sold, followers, location and categories.

`total_results` is **null when `sold: true`**. eBay publishes no headline count on the sold view, so a null there means "eBay did not say", not "zero results". Count the returned rows instead.

## Guardrails

- Never fabricate prices, item numbers, sold dates, feedback scores or seller names. Only return data the API returned.
- `/seller` is a PROFILE endpoint. It cannot enumerate a catalogue. If the user wants a seller's items, use `/search` with `seller` set and no keyword.
- `per_page` accepts only `60`, `120` or `240`. eBay silently falls back to 60 for any other value, so a request for 100 quietly returns 60 and looks successful.
- `category_id` must be numeric. An unrecognised category id returns the UNFILTERED result set under a `200`, which looks like a successful filter and is not one. Verify the id before relying on it.
- `condition: "refurbished"` is eBay's parent condition, not one of its three graded refurbished tiers. Do not present it as a specific grade.
- There is no "Distance: nearest first" sort. It ranks against the proxy exit rather than the caller's location, so it is deliberately absent. Never recommend it.
- Sold-listing prices are historical. When quoting them as a market value, say when the sale happened.
- Always include the listing URL so the user can verify.

## Failure handling

- `400` means an invalid or missing parameter, most often neither `query` nor `seller` being supplied. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the item or seller was not found. Check the item number or the `ebay.com/usr/<name>` spelling.
- `429` means a rate or usage limit was exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=ebay-product-data).
- `502` / `503` mean the upstream is temporarily unavailable. Wait a few seconds before retrying.
- If a sold search returns nothing, widen the keywords before concluding the item never sold. Sold-view matching is stricter than the live view.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Docs

- [eBay search](https://scavio.dev/docs/ebay-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=ebay-product-data)
- [eBay product](https://scavio.dev/docs/ebay-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=ebay-product-data)
- [eBay seller](https://scavio.dev/docs/ebay-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=ebay-product-data)
