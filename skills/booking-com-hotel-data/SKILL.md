---
name: booking-com-hotel-data
description: "Booking.com hotel data API: search a destination and stay for live nightly prices, review scores and star ratings, pull one property in full with rooms, rate plans, facilities and policies, and read guest reviews with per-category subscores. 3 endpoints, 1 credit each, structured JSON."
version: 1.0.0
tags: booking-com, booking-com-hotel-data, hotel-prices, hotels, nightly-rates, accommodation, travel, rate-shopping, guest-reviews, ota-data, agents, langchain, crewai, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F3E8"
    homepage: https://scavio.dev/docs/booking-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=booking-com-hotel-data
---

# Booking.com Hotel Data API - Search, Live Prices, Reviews

Search Booking.com for a destination and a stay, read one property in full with its rooms and rate plans, and pull guest reviews with the score breakdown. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find hotels, apartments or hostels in a city for specific dates
- Compare live nightly prices, review scores and star ratings across properties
- Filter by price per night, star rating, review score, property type, free cancellation, no prepayment or breakfast
- Pull one property in full - rooms and rate plans, facilities, house rules, check-in windows, policies, images
- Read guest reviews with the per-category subscores and Booking's own praise and complaint summary
- Build rate-shopping, competitive-set or travel-research pipelines

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=booking-com-hotel-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=booking-com-hotel-data) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Every Booking.com endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/booking/search` | 1 | Properties for a destination and stay: live nightly price, review score, star rating, location, room type, deal badges |
| `POST /api/v1/booking/hotel` | 1 | One property in full: rooms and rate plans, facilities, house rules, check-in windows, policies, images, location, review scores |
| `POST /api/v1/booking/reviews` | 1 | Guest reviews with the score breakdown by category and Booking's own praise/complaint summary |

## Workflow

1. **Search:** call `/booking/search` with `destination` (or a numeric `dest_id`) **and both `checkin` and `checkout`**. Read `properties[].url`.
2. **One property:** call `/booking/hotel` with that `url` as `hotel`. Chaining the URL a search row already returned is always the cheapest and safest path - a bare page slug needs the right `country_code`, and a wrong one is a real, **billed** 404.
3. **Reviews:** call `/booking/reviews` with the same `hotel` value.

Booking prices a **stay**, not a property, so all three endpoints take dates.

### Dates, currency and the two ways to waste a credit

- **`checkin` and `checkout` must be sent together.** Booking ignores a lone `checkin` and prices its own default range, so you get real prices for dates nobody asked for. The API rejects an unpaired or out-of-order date.
- **Omitting dates entirely on `/hotel` or `/reviews`** returns prices for a two-night range Booking chose. The response echoes whichever dates were actually used - read `checkin`, `checkout` and `nights` back before quoting a price.
- **A search with neither `destination` nor `dest_id` would return Booking's homepage** - a credit spent for nothing - so the API rejects it up front.
- **Always send `currency`.** It defaults to `USD` in the transport; without one Booking prices off the proxy exit and two identical requests disagree.

### Pagination

Only `/search` pages, with a 1-based `page` — **25 properties per page**. `count` is what this page returned and `total_results` is Booking's headline count. `/hotel` and `/reviews` return a single response and take **no page parameter**; on reviews, `total_count` is the whole history and `count` is what this response holds.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `destination` | string | one of | Free-text destination (1-200 chars) |
| `dest_id` | string | one of | Numeric Booking destination id |
| `dest_type` | string | -- | `city`, `region`, `country`, `district`, `landmark`, `airport`, `hotel`. **Requires `dest_id`** |
| `page` | integer | -- | 1-based, 25 properties per page |
| `sort_by` | string | `popularity` | `popularity`, `price_low`, `price_high`, `stars_high`, `stars_low`, `stars_and_price`, `distance`, `review_score` |
| `min_price` / `max_price` | number | -- | **Per night**, in `currency` |
| `stars` | integer[] | -- | 1-5 stars, 1-5 items, OR'd |
| `min_review_score` | string | -- | `6`, `7`, `8`, `9` only |
| `property_type` | string or integer | -- | `apartments`, `hostels`, `hotels`, `motels`, `resorts`, `bed_and_breakfasts`, `villas`, `campgrounds`, `vacation_homes`, `lodges`, `homestays`, or a raw numeric Booking accommodation-type id |
| `free_cancellation` | boolean | -- | Free-cancellation rates only |
| `no_prepayment` | boolean | -- | No-prepayment rates only |
| `breakfast_included` | boolean | -- | Breakfast-included rates only |
| `checkin` / `checkout` | string | -- | `YYYY-MM-DD`, sent together and in order |
| `adults` | integer | `2` | Adult guests |
| `children_ages` | integer[] | -- | **Ages** (0-17, max 10 entries), not a count |
| `rooms` | integer | `1` | Rooms requested |
| `currency` | string | `USD` | ISO 4217, 3 letters |

`destination` or `dest_id` is required. `min_review_score` is an enum - an arbitrary threshold such as `8.4` is silently dropped upstream and the results come back unfiltered. `dest_type` on its own is ignored by Booking, so the API rejects it without `dest_id`.

### Hotel (`/hotel`) and reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `hotel` | string | required | Booking.com property URL or the bare page slug (1-500 chars); query params are discarded |
| `country_code` | string | `us` | 2 letters. Only consulted for a **bare slug** |
| `checkin` / `checkout` | string | -- | `YYYY-MM-DD`, sent together and in order |
| `adults` | integer | `2` | Adult guests |
| `children_ages` | integer[] | -- | Ages, max 10 |
| `rooms` | integer | `1` | Rooms requested |
| `currency` | string | `USD` | ISO 4217 |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

STAY = {"checkin": "2026-09-08", "checkout": "2026-09-10", "currency": "USD"}

# 1. Search a destination for a real stay - dates always in pairs
found = requests.post(f"{BASE}/api/v1/booking/search", headers=HEADERS,
    json={"destination": "Austin", "adults": 2, "rooms": 1,
          "sort_by": "review_score", "min_review_score": "8",
          "max_price": 300, **STAY}).json()

row = found["data"]["properties"][0]

# 2. Chain the URL the row already gave you - no country_code guessing
hotel = requests.post(f"{BASE}/api/v1/booking/hotel", headers=HEADERS,
    json={"hotel": row["url"], **STAY}).json()

# The response echoes the dates it actually priced
print(hotel["data"]["checkin"], hotel["data"]["checkout"], hotel["data"]["nights"])

# 3. Guest reviews for the same property
reviews = requests.post(f"{BASE}/api/v1/booking/reviews", headers=HEADERS,
    json={"hotel": row["url"], **STAY}).json()

# 4. A family stay: children_ages are AGES, not a headcount
family = requests.post(f"{BASE}/api/v1/booking/search", headers=HEADERS,
    json={"destination": "Lisbon", "adults": 2, "children_ages": [4, 9],
          "rooms": 1, **STAY}).json()
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **search** — `destination`, `url`, `page`, `checkin`, `checkout`, `nights`, `adults`, `children_ages`, `rooms`, `currency`, `dest_id`, `dest_type`, `destination_name`, `destination_country`, `total_results`, `count`, `properties[]`, `bounding_box`, `sort`, `sort_options`, `applied_filters`, `available_filters`, `breadcrumbs`.
  A property row: `pos`, `hotel_id`, `name`, `page_name`, `url`, `country_code`, `city`, `address`, `latitude`, `longitude`, `display_location`, `district`, `distance_from_center`, `accommodation_type_id`, `star_rating`, `review_score`, `review_score_word`, `review_count`, `image`, `price`, `price_formatted`, `currency`, `price_per_night`, `original_price`, `charges_info`, `discounts`, `deal_badges`, `room_name`, `beds`, `bedrooms`, `bathrooms`, `unit_area`, `free_cancellation`, `free_cancellation_until`, `no_prepayment`, `meal_plan`, `rooms_left_message`, `is_sold_out`, `sponsored`, `preferred`, `genius_rate_available`, `is_sustainable`, `badges`.
- **hotel** — `hotel_id`, `name`, `page_name`, `url`, `description`, `country_code`, `city`, `address`, `postal_code`, `region`, `latitude`, `longitude`, `dest_id`, `accommodation_type`, `star_rating`, `chain_ids`, `brand`, `review_score`, `review_count`, `review_subscores[]`, `languages_spoken`, `currency`, `checkin`, `checkout`, `nights`, `adults`, `children_ages`, `rooms_requested`, `price_from`, `is_sold_out`, `image`, `images`, `facilities[]`, `highlights`, `meals`, `checkin_from`, `checkin_until`, `checkout_from`, `checkout_until`, `min_checkin_age`.
- **reviews** — `hotel_id`, `name`, `page_name`, `url`, `score`, `total_count`, `count`, `subscores[]` (`name`, `label`, `score`, `review_count`), `summary` (`review_count`, `pros`, `cons`), `topics[]`, `reviews[]` (`review_id`, `title`, `positive`, `negative`, `score`, `reviewed_at`, `guest_name`, `guest_country`, `guest_review_count`, `is_anonymous`, `customer_type`, `trip_purpose`, `room_name`, `language`).

```json
{
  "data": {
    "destination": "Austin",
    "dest_type": "CITY",
    "checkin": "2026-09-08",
    "checkout": "2026-09-10",
    "nights": 2,
    "currency": "USD",
    "total_results": 955,
    "page": 1,
    "count": 25,
    "properties": [
      {
        "pos": 1,
        "hotel_id": 1234567,
        "name": "Hotel Example Austin",
        "url": "https://www.booking.com/hotel/us/example-austin.html",
        "star_rating": 4,
        "review_score": 8.5,
        "review_count": 2122,
        "price": 405.76,
        "price_per_night": 202.88,
        "currency": "USD",
        "free_cancellation": true
      }
    ]
  },
  "credits_used": 1,
  "credits_remaining": 999
}
```

## Guardrails

- Every call is **1 credit**, including one that comes back empty.
- Never send `checkin` without `checkout`. If the user gives one date, ask for the other or pick an explicit range and say which one you used.
- If you did not send dates, read `checkin` / `checkout` / `nights` off the response and tell the user which stay the prices refer to. Never present a defaulted range as the dates they asked for.
- Always pass `currency`. A price with no stated currency is not a usable answer.
- `min_price` / `max_price` are **per night**, while a property row also carries the stay total in `price`. Say which figure you are quoting.
- `min_review_score` accepts only `6`, `7`, `8` or `9`. Round the user's threshold to one of those and tell them, rather than sending a value Booking will drop.
- Prices and availability are live and move. Timestamp any quote and always include the property `url` so the user can verify and book.
- Never fabricate property names, prices, review scores or review text. Only return what the API returned.

## Failure handling

- `400` means an invalid or missing parameter - no `destination` and no `dest_id`, `dest_type` without `dest_id`, an unpaired or out-of-order date, or `min_price` above `max_price`. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` on `/hotel` or `/reviews` usually means a bare slug was resolved against the wrong `country_code`. It is a real, **billed** 404 - do not brute-force country codes. Run a search and chain the `url` it returns instead.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=booking-com-hotel-data).
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry, up to a few times.
- A search that returns no properties is usually a filter problem: widen `max_price`, drop `min_review_score`, or loosen `stars`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.booking.search(destination="Austin", checkin="2026-09-08",
                              checkout="2026-09-10", adults=2, currency="USD")
url = found["data"]["properties"][0]["url"]
hotel = client.booking.hotel(url, checkin="2026-09-08", checkout="2026-09-10", currency="USD")
reviews = client.booking.reviews(url, checkin="2026-09-08", checkout="2026-09-10")
```

```bash
npm install scavio@0.15.0
```

```javascript
import { Scavio } from "scavio";

const client = new Scavio(); // reads SCAVIO_API_KEY
const found = await client.booking.search({
  destination: "Austin", checkin: "2026-09-08", checkout: "2026-09-10", currency: "USD",
});
const hotel = await client.booking.hotel({ hotel: found.data.properties[0].url, currency: "USD" });
```
