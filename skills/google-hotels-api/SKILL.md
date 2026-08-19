---
name: google-hotels-api
description: "Google Hotels search for a destination and stay dates as structured JSON: properties with name, nightly rate and rating, then per-property detail with booking-site vendor prices. Filter by price, rating, hotel class, amenities and vacation rentals. 2 endpoints, 1 credit each."
version: 1.0.0
tags: google-hotels, google-hotels-api, hotel-search, hotel-prices, nightly-rates, hotel-ratings, amenities, lodging, vacation-rentals, travel, price-comparison, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F3E8"
    homepage: https://scavio.dev/docs/google-hotels?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-hotels-api
---

# Google Hotels API - Hotel Search, Rates, Ratings, Amenities

Search Google Hotels for a destination and stay dates, then open any property for full details and per-vendor pricing — all as structured JSON. Two endpoints, each 1 credit.

## When to trigger

Use this skill when the user asks to:
- Find hotels or vacation rentals for a destination and dates
- Compare lodging by price, rating, class, or amenities
- Get full details and booking-site prices for a specific property

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-hotels-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

## Endpoints

| Endpoint | Credits | Description |
|---|---|---|
| `POST https://api.scavio.dev/api/v2/google/hotels` | 1 | Search lodging, returns `properties[]` |
| `POST https://api.scavio.dev/api/v2/google/hotels/detail` | 1 | Full property details + vendor prices |

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Workflow

1. **Search:** call `/hotels` with `query` (use the `"<City> hotels"` form), `check_in_date`, and `check_out_date`. Filter with price, rating, class, and amenities.
2. Read `properties[]`; each has a `name`, `rate_per_night`, `overall_rating`, and a `detail_token`.
3. **Details:** call `/hotels/detail` with a property's `detail_token` and the same stay dates to get full info and booking-site prices in `property.booking_sources`.
4. Page more results with `next_page_token` from the search response.

## Hotels Search Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Use the `"<City> hotels"` form (e.g. `Bali hotels`) |
| `check_in_date` | string | required | Check-in `YYYY-MM-DD` |
| `check_out_date` | string | required | Check-out `YYYY-MM-DD` |
| `sort_by` | number | -- | `3` lowest price, `8` highest rating, `13` most reviewed |
| `min_price` | number | -- | Minimum nightly price |
| `max_price` | number | -- | Maximum nightly price |
| `rating` | number | -- | `7` (3.5+), `8` (4.0+), `9` (4.5+) |
| `hotel_class` | string | -- | Comma-separated 2-5 (e.g. `4,5`) |
| `amenities` | string | -- | Amenity filter ids |
| `property_types` | string | -- | `12` = vacation rentals |
| `free_cancellation` | boolean | -- | Only free-cancellation offers |
| `eco_certified` | boolean | -- | Only eco-certified properties |
| `special_offers` | boolean | -- | Only special offers |
| `next_page_token` | string | -- | Pagination cursor from a prior response |
| `limit` | number | -- | Cap properties returned (1-20) |
| `hl` | string | -- | UI language |
| `gl` | string | -- | Geo country |
| `currency` | string | -- | Currency code (e.g. `USD`) |

## Hotels Detail Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `detail_token` | string | required | From a listing property's `detail_token` |
| `check_in_date` | string | required | Check-in `YYYY-MM-DD` |
| `check_out_date` | string | required | Check-out `YYYY-MM-DD` |
| `currency` | string | -- | Currency code |
| `gl` | string | -- | Geo country |
| `hl` | string | -- | UI language |

## Example

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-hotels-api. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
DATES = {"check_in_date": "2026-10-01", "check_out_date": "2026-10-05"}

# 1. Search hotels, highest rated first
search = requests.post(f"{BASE}/api/v2/google/hotels", headers=HEADERS,
    json={"query": "Bali hotels", **DATES, "sort_by": 8, "rating": 8}).json()

prop = search["properties"][0]
print(prop["name"], prop.get("overall_rating"), prop.get("rate_per_night"))

# 2. Full details + vendor prices for that property
detail = requests.post(f"{BASE}/api/v2/google/hotels/detail", headers=HEADERS,
    json={"detail_token": prop["detail_token"], **DATES, "currency": "USD"}).json()
for src in detail["property"]["booking_sources"]:
    print(src.get("source"), src.get("rate_per_night"))
```

## Responses

Search returns `properties[]`; detail returns `property` with `booking_sources[]`. Each also includes `response_time`, `credits_used`, `credits_remaining`, and `cached`.

```json
{
  "properties": [
    {
      "name": "Example Resort",
      "type": "hotel",
      "overall_rating": 4.6,
      "reviews": 3120,
      "hotel_class": 5,
      "rate_per_night": { "lowest": "$180", "extracted_lowest": 180 },
      "detail_token": "CggI...Aw"
    }
  ],
  "response_time": 1760,
  "credits_used": 1,
  "credits_remaining": 993,
  "cached": false
}
```

## Guardrails

- Each call costs 1 credit.
- Never fabricate property names, ratings, prices, or vendors. Only return API data.
- The detail call needs a `detail_token` from a search result plus the same stay dates — always run `/hotels` first.
- Prices reflect the requested `currency`; state the currency and the stay dates when quoting.

## Failure handling

- `400` means an invalid parameter (e.g. missing dates or `detail_token`) — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-hotels-api.
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If no properties are returned, loosen price/rating/class filters or try different dates.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
