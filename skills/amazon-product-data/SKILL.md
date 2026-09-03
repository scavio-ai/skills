---
name: amazon-product-data
description: "Amazon product data API: keyword search, full product detail by ASIN, and every seller offer on an ASIN with the buy-box winner. Normalized JSON with price, rating, review count, availability, shipping and sellers. 3 endpoints, all 1 credit, 22 marketplaces; no server-side sort."
version: 3.0.1
tags: amazon, amazon-product-data, product-search, asin, price-lookup, offers, buy-box, sellers, ecommerce, retail, competitor-research, agents, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F6D2"
    homepage: https://scavio.dev/docs/amazon-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=amazon-product-data
---

# Amazon Product Data API - Search, ASIN Lookup, Offers

Search Amazon by keyword, pull full product detail for an ASIN, and list every seller offering that ASIN including which one holds the buy box. All three endpoints return clean normalized JSON across 22 Amazon marketplaces.

## When to trigger

Use this skill when the user asks to:
- Find products on Amazon by keyword, with price, rating and review count
- Look up a specific product by ASIN: price, availability, images, specifications, variants, shipping
- Compare sellers on one product, find the cheapest offer, or see who holds the buy box
- Track a price, check stock, or watch a listing over time
- Research a marketplace other than the US (Germany, UK, Japan, ...)
- Mine best sellers rank, sales volume or badges for competitor research

## Three things to read before you call anything

**1. There is no sort. At all.** Amazon accepts every sort value and ignores all of them. Verified by comparing price ordering across `price-asc-rank`, `price-desc-rank`, `review-rank` and `date-desc-rank`: identical, unordered result sets every time. There is therefore no `sort_by` parameter, and sending one gets you a `warnings` entry, not a sorted list. If the user wants "cheapest first", sort the returned `products[]` yourself on `price` — and say that you sorted one page locally, not that Amazon ranked them.

**2. `country` is a two-letter country code, not a domain and not a ZIP.** `us`, `gb`, `de`, `jp`. Two do not match the domain suffix people expect: **amazon.com is `us`** (not `com`) and **amazon.co.uk is `gb`** (not `uk`). The old `domain` parameter (`com`, `co.uk`) still works as a deprecated alias and is translated for you, but write new calls with `country`. A code that is two letters but not a real marketplace does not fail — it quietly returns the **US** storefront, so a typo looks like a successful search of the wrong country. Check the code against the list below before sending it.

**3. `reviews_count` from search can be a rounded display value; from product and offers it is always exact.** Search carries the count as page text: `"(517)"` parses to an exact `517`, but anything Amazon abbreviates — `"(1.3K)"`, `"(92.9K)"` — parses to `1300` and `92900`, which are Amazon's own rounded figures, not real counts. `/product` and `/offers` return the true integer. Never present a large search-derived count as exact, and never diff a search count against a product count and call it a change.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=amazon-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=amazon-product-data) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Every data endpoint costs **1 credit**.

| Endpoint | Credits | Description |
|---|---|---|
| `POST /api/v1/amazon/search` | 1 | Keyword search: product cards, filters, related searches |
| `POST /api/v1/amazon/product` | 1 | Full detail for one ASIN |
| `POST /api/v1/amazon/offers` | 1 | Every seller offer on one ASIN, with the buy-box winner |
| `GET /api/v1/amazon/options` | 0 | The marketplace list. No API key, no credit. |

## Workflow

1. **Find products:** `POST /amazon/search` with `query`. Each card already carries `asin`, `price`, `currency`, `rating`, `reviews_count`, `badge`, `sales_volume` and `delivery` — for a shortlist you are done in one call.
2. **Page through:** pass `page: 2`, `page: 3`. One page per call, 1 credit per call. There is no way to fetch several pages in one request.
3. **Deep-dive:** `POST /amazon/product` with the ASIN for description, features, images, videos, specifications, variants, best sellers rank and structured shipping.
4. **Compare sellers:** `POST /amazon/offers` with the same ASIN when the user cares about price, condition or who is selling. `has_buy_box` and `other_sellers_count` on the product response tell you whether that call is worth 1 credit.
5. **Switch marketplace:** set `country` on any of the three.

`/product` and `/offers` take the ASIN in `query` (the field every Scavio client has always used) or in `asin` — they are the same parameter, so send one.

## Parameters

### Search (`/api/v1/amazon/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keyword (1-500 chars) |
| `country` | string | `us` | Marketplace, ISO 3166-1 alpha-2 (see below) |
| `page` | number | `1` | 1-based results page |
| `domain` | string | -- | Deprecated alias for `country` (`com`, `co.uk`, `de`). Translated for you. |
| `start_page` | number | -- | Deprecated alias for `page` |

No `sort_by`, no `pages`, no `category_id`, no `merchant_id`, no price filter, no `zip_code`, no `device`, no `language`, no `currency`. None of those exist upstream any more, so none are accepted. To narrow a search, use the URLs in `filters[].options[]`, or add the qualifier to `query` ("laptop under 500").

### Product (`/api/v1/amazon/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | The 10-character ASIN, e.g. `B09XS7JWHH`. Alias: `asin`. |
| `country` | string | `us` | Marketplace, ISO 3166-1 alpha-2 |
| `domain` | string | -- | Deprecated alias for `country` |

### Offers (`/api/v1/amazon/offers`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | The 10-character ASIN. Alias: `asin`. |
| `country` | string | `us` | Marketplace, ISO 3166-1 alpha-2 |
| `domain` | string | -- | Deprecated alias for `country` |

**Page 1 only.** The response echoes `page` and `has_more_pages`, but there is no verified upstream parameter to request page 2, so none is exposed. If `has_more_pages` is `true`, say the list is the first page rather than implying it is complete.

### Marketplaces

`us` `gb` `de` `fr` `it` `es` `nl` `be` `se` `pl` `tr` `ca` `mx` `br` `jp` `cn` `sg` `in` `au` `ae` `sa` `eg`

`GET /api/v1/amazon/options` returns the same list with labels, needs no API key and costs nothing. Its body is `{ domains, countries, languages, currencies }`: `countries` holds `{value, label}` pairs for the codes above, `domains` the matching `amazon.<suffix>` aliases, and `languages` / `currencies` are **empty arrays** — they are kept only so old parsers do not break, since neither is a request parameter any more.

`country` must be exactly two letters or the request is a `400`. A two-letter code that is not on the list above does **not** error: it is forwarded to Amazon, which quietly serves the US storefront instead — `country: "zz"` comes back `200` with amazon.com results. The deprecated `domain` alias does the same, so an old caller sending `domain: "uk"` (not a real Amazon suffix — the UK is `co.uk`) also gets the US storefront with no error. Neither case is distinguishable from a real US search once you have the response, so validate the code against `/options` before sending it rather than trusting what comes back.

## Examples

```bash
# 1. Keyword search
curl -s -X POST https://api.scavio.dev/api/v1/amazon/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "wireless headphones"}'

# 2. Page 2 of the German marketplace
curl -s -X POST https://api.scavio.dev/api/v1/amazon/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "kopfhoerer", "country": "de", "page": 2}'

# 3. Product detail by ASIN
curl -s -X POST https://api.scavio.dev/api/v1/amazon/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "B0GRVFY42Q"}'

# 4. Every seller offer on that ASIN
curl -s -X POST https://api.scavio.dev/api/v1/amazon/offers \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asin": "B0GRVFY42Q", "country": "us"}'

# 5. The marketplace list -- free, no key needed
curl -s https://api.scavio.dev/api/v1/amazon/options
```

Search, then price-check the cheapest seller:

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def call(path, body):
    r = requests.post(f"{BASE}/api/v1/amazon/{path}", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()

# 1. Search. Results are in Amazon's default ranking -- there is no sort param.
#    Sort locally if the user wants cheapest first, and say so.
res = call("search", {"query": "wireless headphones", "country": "us"})["data"]

for p in sorted(res["products"], key=lambda p: p["price"] or float("inf")):
    # reviews_count here is rounded when Amazon abbreviated it: "(1.3K)" -> 1300
    print(p["asin"], p["price"], p["currency"], p["rating"], p["reviews_count"], p["title"][:60])

asin = res["products"][0]["asin"]

# 2. Detail. price/list_price are numbers, currency is a separate string.
d = call("product", {"query": asin})["data"]
print(d["title"], d["price"], d["currency"], d["availability"], d["sold_by"])

# 3. Only pay for offers when there are other sellers to compare.
if (d["other_sellers_count"] or 0) > 0:
    offers = call("offers", {"asin": asin})["data"]
    for o in sorted(offers["offers"], key=lambda o: o["price"] or float("inf")):
        tag = "buy box" if o["is_buy_box_winner"] else ""
        print(o["seller_name"], o["condition"], o["price"], o["shipping_price"], tag)
    if offers["has_more_pages"]:
        print("first page of offers only")
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. A `warnings` array is added at the top level only when the request carried a retired parameter — see Failure handling.

Fields mean the same thing on all three endpoints: `title`, `price` (a number), `currency` (a separate string), `rating` (0-5), `reviews_count`, `image`. Any field with no upstream equivalent is absent, never a permanent `null`.

### Search

`data` is `{ query, page, total_results, total_results_text, count, products[], filters[], related_searches[] }`.

```json
{
  "data": {
    "query": "laptop",
    "page": 1,
    "total_results": 100000,
    "total_results_text": "1-16 of over 100,000 results for laptop",
    "count": 16,
    "products": [
      {
        "asin": "B0GRVFY42Q",
        "title": "HP 15.6\" FHD Laptop 2026 Edition, Intel Processor, 8GB RAM, 256GB SSD",
        "url": "https://www.amazon.com/HP-Laptop-Intel-Processor-256GB/dp/B0GRVFY42Q/ref=sr_1_1?dib=...",
        "image": "https://m.media-amazon.com/images/I/71sTXs4lkqL._AC_UY218_.jpg",
        "price": 414.99,
        "currency": "USD",
        "rating": 4.2,
        "reviews_count": 517,
        "is_sponsored": false,
        "position": 3,
        "badge": "Overall Pick",
        "sales_volume": "1K+ bought in past month",
        "delivery": { "is_free": true, "date": "Tomorrow, Aug 1", "fastest_date": "Aug 3 - 4" }
      }
    ],
    "filters": [
      {
        "name": "Popular Shopping Ideas",
        "options": [
          {
            "name": "Thinkpad",
            "url": "https://www.amazon.com/s?k=laptop+thinkpad&ref=sr_nr_p_rag_integrated_qb_0",
            "refinement": null
          }
        ]
      }
    ],
    "related_searches": [
      { "position": 1, "query": "macbook", "url": "https://www.amazon.com/s?k=macbook&ref=rsl_sug_0_0" }
    ]
  },
  "response_time": 4940,
  "credits_used": 1,
  "credits_remaining": 999
}
```

Read these carefully before building on them:

- `total_results` is a **floor** parsed out of the page text: "over 100,000 results" becomes `100000`. `total_results_text` is the sentence it came from. Never divide either by a page size to compute a page count — page until `products[]` comes back short.
- `count` is how many products this page returned, typically 16 and not guaranteed.
- `position` is Amazon's own grid index **including ad and carousel slots**, so it is neither the array index nor contiguous — a live page returned 3, 4, 5, 8, 9, 10, ..., 22. It is passed through untouched. Use the array order for "the Nth result".
- `price` and `rating` can be `null` on a card Amazon rendered without them. Guard before arithmetic.
- `filters[].options[].refinement` is Amazon's refinement token. There is no parameter to send it back to, so use the option `url` instead.
- `is_sponsored` marks paid placements. Exclude them when the user asks for organic results.

### Product

`data` is `{ asin, title, brand, url, description, features[], price, list_price, currency, rating, reviews_count, is_prime, is_sponsored, has_buy_box, availability, max_quantity, sold_by, other_sellers_count, sales_volume, climate_pledge_friendly, image, images[], videos[], best_sellers_rank[], categories[], specifications{}, variants[], shipping{}, reviews[] }`.

```json
{
  "data": {
    "asin": "B0GRVFY42Q",
    "title": "HP 15.6\" FHD Laptop 2026 Edition, Intel Processor, 8GB RAM, 256GB SSD",
    "brand": "HP",
    "url": "https://www.amazon.com/dp/B0GRVFY42Q",
    "description": "Your Reliable Companion for Learning, Work & Everyday Computing...",
    "features": ["Powerful Everyday Performance: Intel N100 processor with 8GB RAM..."],
    "price": 414.99,
    "list_price": 799,
    "currency": "USD",
    "rating": 4.2,
    "reviews_count": 517,
    "is_prime": true,
    "is_sponsored": false,
    "has_buy_box": true,
    "availability": "In Stock",
    "max_quantity": 30,
    "sold_by": "Omnitech Global",
    "other_sellers_count": 0,
    "sales_volume": "1K+ bought in past month",
    "climate_pledge_friendly": true,
    "image": "https://m.media-amazon.com/images/I/71sTXs4lkqL._AC_SY300_SX300_QL70_FMwebp_.jpg",
    "images": ["https://m.media-amazon.com/images/I/71sTXs4lkqL._AC_SL1500_.jpg"],
    "videos": [
      {
        "title": "HP 15.6\\\" FHD Laptop 2026 Edition with Copilot AI",
        "url": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/de91.../default.jobtemplate.hls.m3u8",
        "thumbnail": "https://m.media-amazon.com/images/I/51YqUDn8TkL.SX522_.jpg",
        "duration_seconds": 12,
        "width": 1920,
        "height": 1080
      }
    ],
    "best_sellers_rank": [{ "category": "Computers & Accessories", "rank": 98 }],
    "categories": [
      {
        "name": "Electronics",
        "url": "https://www.amazon.com/electronics-store/b/ref=dp_bc_1?ie=UTF8&node=172282",
        "node": "172282"
      }
    ],
    "specifications": { "CPU Model Number": "Intel Processor N100", "Screen Size": "15.6 inches" },
    "variants": [
      { "asin": "B0GRVFY42Q", "dimensions": { "Color": "Natural Silver" }, "is_selected": true, "is_available": true }
    ],
    "shipping": {
      "is_prime": true,
      "zipcode": "10001",
      "options": [
        {
          "type": "free",
          "price": 0,
          "is_prime": true,
          "delivery_date": "Tomorrow, August 1",
          "order_deadline_hours": 4,
          "order_deadline_minutes": 55
        }
      ]
    },
    "reviews": [
      {
        "id": "R25NUR3YMMFTG1",
        "author": "Domika0717",
        "date": "Reviewed in the United States on June 7, 2026",
        "verified_purchase": true
      }
    ]
  },
  "response_time": 2768,
  "credits_used": 1,
  "credits_remaining": 998
}
```

- `availability` is free text in the marketplace's language ("In Stock", "Nur noch 3 auf Lager"). There is no boolean in-stock flag, because the wording cannot be parsed reliably across 22 storefronts. Quote it; do not derive from it.
- `reviews[]` is **metadata only** — id, author, date, verified flag. Upstream carries no review body and no per-review rating anywhere on the product page. Never claim to have read a review's text.
- `specifications` and `variants[].dimensions` use Amazon's own human labels as keys ("CPU Model Number", "Color"), kept verbatim. They differ by category and by marketplace, so look keys up defensively.
- `video.title` arrives double-escaped from upstream (`HP 15.6\\" FHD ...`). It is passed through as sent rather than "fixed", because un-escaping would corrupt legitimate backslashes.
- `image` is a resized thumbnail; `images[]` holds the full-size set.
- `other_sellers_count` is the cheapest way to decide whether an `/offers` call is worth a credit.

### Offers

`data` is `{ asin, title, image, rating, reviews_count, note, count, total_offers, has_more_pages, page, offers[] }`.

```json
{
  "data": {
    "asin": "B0GRVFY42Q",
    "title": "HP 15.6\" FHD Laptop 2026 Edition, Intel Processor, 8GB RAM, 256GB SSD",
    "image": "https://m.media-amazon.com/images/I/412kavhXHzL.jpg",
    "rating": 4.2,
    "reviews_count": 517,
    "note": "Currently, there are no other sellers matching your location and / or item specification.",
    "count": 1,
    "total_offers": 1,
    "has_more_pages": false,
    "page": 1,
    "offers": [
      {
        "condition": "New",
        "seller_id": "A171014CP909KT",
        "seller_name": "Omnitech Global",
        "ships_from": "Omnitech Global",
        "is_fulfilled_by_amazon": false,
        "is_buy_box_winner": true,
        "is_prime": true,
        "is_national_prime": true,
        "price": 414.99,
        "currency": "USD",
        "list_price": 799,
        "shipping_price": 0,
        "discount_percentage": 48.06,
        "discount_amount": 384.01,
        "price_notice": null,
        "promotion": null,
        "quantity": 30,
        "delivery": { "min_hours": 24, "max_hours": 72, "date": "August 3 - 4", "is_free": true },
        "prime_delivery": { "date": "Tomorrow, August 1", "order_deadline": "Order within 4 hrs 55 mins" }
      }
    ]
  },
  "response_time": 3830,
  "credits_used": 1,
  "credits_remaining": 997
}
```

- `price` is the item price and `shipping_price` is separate. The landed cost is `price + shipping_price`; compute it, do not assume `price` includes delivery.
- `is_buy_box_winner` marks the offer Amazon serves by default. It is not always the cheapest — say which one is which.
- `count` is the offers on this page; `total_offers` is what upstream reported. They agreed in every observed response, but trust `count` for anything you are about to iterate.
- `note` is genuine user-facing text explaining an empty or short list. Surface it instead of reporting "no offers found".
- `price_notice` and `promotion` were `null` in every offer observed so far. Treat a non-null value as a bonus, never a required field.
- `condition` is Amazon's own wording ("New", "Used - Very Good"). Do not normalize it into a grade you invented.

## Guardrails

- Every call to `/search`, `/product` and `/offers` costs **1 credit**, including a search that returns nothing. Tell the user before paginating deeply or looping `/product` over a whole results page. `/options` is free.
- Never fabricate a product title, ASIN, price, rating, review count, seller or availability. Only return API data. If a field is `null`, say it is unavailable.
- **Never claim results are sorted by Amazon.** There is no sort parameter. If you ordered them, say you sorted one page of results locally.
- Prices are numbers in `currency`, which changes with `country`. Never mix currencies in one comparison and never convert between them — you have no exchange rate.
- Search `reviews_count` is rounded whenever Amazon abbreviated it (`1.3K` -> `1300`); product and offers counts are always exact. Do not mix the two in one comparison.
- `position` is Amazon's grid index including ads. Do not present it as "rank 3 of the organic results".
- Always include the product `url` so the user can verify. For a search card that is the ref-tracked link Amazon serves; it is the real result URL and works as-is.
- Prices and delivery estimates are point-in-time and vary by marketplace and location. Say when the data was fetched rather than implying it is stable.
- `/offers` returns page 1 only. If `has_more_pages` is `true`, do not present the list as every seller.
- For a price comparison across two products, run two searches or two product calls — 2 credits — and present both. Never infer the second from the first.

## Failure handling

- `400` — an invalid parameter: an empty or over-500-character `query`, a `country` that is not exactly two letters, or a `/product` or `/offers` call with no ASIN in either `query` or `asin`. Not billed. Fix the request.
- `401` — the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` — rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=amazon-product-data).
- `502` — Amazon data is temporarily unavailable, or the ASIN could not be fetched from that marketplace. **Not billed.** Wait a few seconds and retry once; if it repeats, check the ASIN exists on that `country`'s storefront before retrying again.
- `503` — the upstream fetch never completed (network failure or timeout). **Not billed.** Retry after a short backoff.
- A `200` with a top-level `warnings` array means the request carried a parameter that no longer exists and was ignored. Read it and fix the caller, because the response is not filtered the way the request implied:

  ```json
  {
    "data": { "query": "laptop", "page": 1, "count": 16 },
    "response_time": 4512,
    "credits_used": 1,
    "credits_remaining": 996,
    "warnings": [
      "sort_by is no longer supported: the upstream marketplace ignores every sort value and returns the default ranking. Results are unsorted."
    ]
  }
  ```

  Warned parameters: all nine retired ones — `sort_by`, `pages`, `category_id`, `merchant_id`, `language`, `currency`, `device`, `zip_code`, `autoselect_variant`. The `data` object is unchanged and the call is still billed.

- An empty `products[]` on a `200` means Amazon returned no matches for that keyword in that marketplace. Try a broader keyword or a different `country`; do not retry the same request.
- Results from the wrong storefront mean the marketplace code did not resolve. Both an off-list two-letter `country` and an unrecognised legacy `domain` fall back to `us` silently rather than erroring, so a typo returns plausible US data instead of an error. Check the code against `/api/v1/amazon/options` and prefer `country` over `domain`.
- Calls typically take 3-5 seconds. Set a client timeout of at least 60 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Related

- `scavio-walmart` — the same product-research shape for Walmart.
- `scavio-google-shopping` — cross-retailer price comparison when the user is not tied to Amazon.
- Full API reference: [Amazon API](https://scavio.dev/docs/amazon-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=amazon-product-data) (one page per endpoint: `amazon-api`, `amazon-product`, `amazon-offers`)

## LangChain

```bash
pip install langchain-scavio==4.0.2
```

```python
from langchain_scavio import ScavioAmazonOffers, ScavioAmazonProduct, ScavioAmazonSearch

tools = [ScavioAmazonSearch(), ScavioAmazonProduct(), ScavioAmazonOffers()]
```

All three endpoints have a LangChain tool; each reads `SCAVIO_API_KEY` from the environment.
