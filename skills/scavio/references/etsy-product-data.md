# Etsy Product Data API - Listings, Shops, Reviews

Search Etsy listings, pull one listing in full with its variations and reviews, open a shop's profile and catalogue, and page through a shop's reviews. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Search Etsy for a product, with price, on-sale and free-shipping filters, sorted by relevance, price or newest
- Pull one listing in full - description, price, availability, material, category path, ship-from, all images, buyer-selectable variations, aggregate rating and its first page of reviews
- Read a shop's profile: location, year opened, sales and admirer counts, rating, review and listing counts, star-seller flag, announcement and sections
- List a shop's own listings
- Page through a shop's reviews across all its listings
- Do handmade/craft market research, competitor shop analysis or price comparison on Etsy

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=etsy-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=etsy-product-data) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Every Etsy endpoint costs **2 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/etsy/search` | 2 | Listings for a query: title, price with discounts, image, shop, per-listing rating and review count, ad and free-shipping flags. Paginated by `page` |
| `POST /api/v1/etsy/product` | 2 | One listing in full: description, price, availability, material, category path, ship-from, all images, buyer-selectable variations, aggregate rating, first page of reviews, and the shop |
| `POST /api/v1/etsy/shop` | 2 | A shop's profile and stats: headline, location, logo/banner, year opened, sales and admirer counts, rating, review and listing counts, star-seller flag, announcement, about and sections |
| `POST /api/v1/etsy/shop/products` | 2 | A page of a shop's listings, same card shape as search (shop-grid cards carry no per-card rating) |
| `POST /api/v1/etsy/reviews` | 2 | A shop's reviews, paginated across all its listings (~14 per page): rating, author, date, text, reviewer avatar, and the source listing |

## Which endpoint has the reviews

A **listing's** own first-page reviews ride the `product` endpoint. The `reviews` endpoint returns a **shop's** reviews pooled across all its listings. Use `product` for one item, `reviews` for the whole shop.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search terms (1-500 chars) |
| `page` | integer | -- | 1-based results page |
| `sort` | string | `relevance` | `relevance`, `lowest_price`, `highest_price`, `most_recent` |
| `min_price` / `max_price` | number | -- | Price filter, in USD |
| `free_shipping` | boolean | -- | Only listings that offer free shipping |
| `on_sale` | boolean | -- | Only listings currently discounted |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `listing` | string | required | Listing id or a listing URL containing `/listing/<id>/` |

### Shop (`/shop`), Shop Products (`/shop/products`), Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `shop` | string | required | Shop name or a shop URL like `https://www.etsy.com/shop/StonehousePotteryOH` |
| `page` | integer | -- | 1-based page (`shop/products` and `reviews`) |
| `sort` | string | `relevance` | (`shop/products` only) same values as search |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search, newest first, on sale only
found = requests.post(f"{BASE}/api/v1/etsy/search", headers=HEADERS,
    json={"query": "ceramic mug", "sort": "most_recent", "on_sale": True,
          "max_price": 40}).json()

row = found["data"]["items"][0]
listing_id, shop = row["listing_id"], row["shop"]

# 2. One listing in full - variations, aggregate rating, first reviews
listing = requests.post(f"{BASE}/api/v1/etsy/product", headers=HEADERS,
    json={"listing": listing_id}).json()

# 3. The shop's profile, then its reviews
shop_profile = requests.post(f"{BASE}/api/v1/etsy/shop", headers=HEADERS,
    json={"shop": shop}).json()
reviews = requests.post(f"{BASE}/api/v1/etsy/reviews", headers=HEADERS,
    json={"shop": shop, "page": 1}).json()
```

curl:

```bash
curl -s https://api.scavio.dev/api/v1/etsy/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"linen apron","sort":"lowest_price"}'
```

## Response shape

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. `data` carries the listings/shop/reviews payload plus `count` on the paginated endpoints.

## Guardrails

- Every Etsy call is **2 credits**, including one that comes back empty.
- Use `product` for one listing's reviews, `reviews` for the whole shop's reviews.
- Shop-grid cards (`search` and `shop/products`) carry no per-card rating; get the aggregate rating from `product` or `shop`.
- Never invent a `sort` value; unrecognised values are rejected before the request runs.
- Never fabricate prices, ratings, shop details or review text. Only return what the API returned.
- Review text is written by real buyers. Summarise; do not build profiles of individuals.

## Failure handling

- `400` means an invalid or missing parameter. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the listing or shop could not be resolved.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=etsy-product-data).
- `502` / `503` mean the source is temporarily unavailable - wait a few seconds and retry.
- An empty result set is usually the filters - widen the price range or drop `on_sale` / `free_shipping`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
