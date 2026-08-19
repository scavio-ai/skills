---
name: airbnb-scraper-api
description: "Airbnb scraper API: search stays for a location and date window with per-night and stay-total price plus the full discount ledger, pull one listing with amenities, host profile, house rules and the rating breakdown, and page real guest review bodies. 3 endpoints, 1 credit each; nightly price is search-only."
version: 1.0.0
tags: airbnb, airbnb-scraper, airbnb-api, short-term-rental, vacation-rental, listings, nightly-rates, guest-reviews, travel, rental-market-research, agents, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F3E1"
    homepage: https://scavio.dev/docs/airbnb-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=airbnb-scraper-api
---

# Airbnb Scraper API - Stay Search, Listing Detail, Reviews

Search Airbnb stays for a location and date window, read one listing in full, and page through its review bodies. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find Airbnb stays in a place for specific dates, with price, rating and capacity filters
- Compare nightly and stay-total prices across listings, including the discount ledger
- Pull one listing in full - description, capacity, the complete grouped amenity list, host profile, house rules, cancellation policy, photo tour
- Read the rating breakdown - six category ratings and the five-bucket star distribution
- Read actual guest review bodies with per-review ratings and dates
- Build short-term-rental market research, comp sets or host analytics

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=airbnb-scraper-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every Airbnb endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/airbnb/search` | 1 | Stays: stay-total and per-night price with the full discount ledger, rating and review count, bedrooms/beds/baths, coordinates, badges, images, `dates_are_defaulted` |
| `POST /api/v1/airbnb/listing` | 1 | One listing in full: description, property and room type, capacity and room counts, the complete grouped amenity list (including what the place does **not** have), host profile and stats, house rules with parsed check-in/out times, cancellation policy, sleeping arrangements, photo tour, every image, and the **rating breakdown**. **No nightly price** |
| `POST /api/v1/airbnb/reviews` | 1 | Review **bodies** with per-review rating, date, and reviewer name/photo/location |

## Two facts that decide how you call this

**Prices are search-only.** The room page carries no nightly rate under any parameters - with or without dates, and even under a rendered fetch. If the user wants a price for a specific listing, you must find it in a `/search` response. `/listing` will never have one.

**The rating breakdown is listing-only.** The six category ratings, the five-bucket star distribution and the synthesised review tags are server-rendered on `/listing` - they are *not* on `/reviews`. `/reviews` gives you the review text.

## Workflow

1. **Search:** call `/airbnb/search` with `location` and, ideally, `check_in` + `check_out`. Read `listings[].listing_id` and `listings[].price`.
2. **One listing:** call `/airbnb/listing` with that `listing_id` or a full `/rooms/` URL. Query parameters on a pasted URL are discarded - they carry somebody else's dates.
3. **Reviews:** call `/airbnb/reviews` with the same `listing_id`, sending an explicit `limit` and stepping `offset`.

### Dates and currency

`check_in` and `check_out` must be sent **together**. A dateless search defaults to roughly +30 days for 5 nights - and Airbnb A/B tests **both the window and the prices** on that shape: the same URL has come back split across two different windows with first-row prices of $680, $802 and $2,238. The response flags this as `dates_are_defaulted`. If it is `true`, do not quote the price as an answer to a dated question.

`currency` defaults to `USD` in the transport. Send one explicitly; without it Airbnb prices off the proxy exit and two identical requests disagree.

### Pagination

- **`/search`** is **18 listings per page** and offers two mutually exclusive controls: a 1-based `page`, or the opaque `next_cursor` from a previous response passed back as `cursor`. **`cursor` wins over `page`, so sending both is rejected.** Pick one. `page_count` is on the response.
- **`/reviews`** pages with `limit` (1-50, default 30) and `offset` (default 0). `count` is the listing's **total** review count; `returned` is how many this page holds.
- **`/listing`** takes no paging parameter.

The `limit` / `offset` names are load-bearing. The underscored `_limit` / `_offset` used elsewhere in Airbnb's API are silently ignored here and pin the response at a fixed 7 rows for every offset - which reads as a paging loop that never advances.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | required | City, region, ZIP, or a pasted `airbnb.com/s/` URL (1-200 chars). Unresolvable is a 404 |
| `check_in` / `check_out` | string | +30d / +5 nights | `YYYY-MM-DD`, sent together and in order |
| `adults` | integer | -- | Adult guests |
| `children` | integer | -- | Ages 2-12 |
| `infants` | integer | -- | Infants |
| `pets` | integer | -- | Pets |
| `min_price` / `max_price` | number | -- | **Whole-stay total**, not per night |
| `room_type` | string | -- | `entire_home`, `private_room`, `shared_room`, `hotel_room` |
| `min_bedrooms` / `min_beds` / `min_bathrooms` | integer | -- | Minimum counts |
| `superhost` | boolean | -- | Superhost listings only |
| `instant_book` | boolean | -- | Instant Book only |
| `guest_favorite` | boolean | -- | Guest Favourite only |
| `free_cancellation` | boolean | -- | Free cancellation only |
| `amenities` | string | -- | Comma-separated: `wifi`, `air_conditioning`, `pool`, `kitchen`, `free_parking`, `washer`, `self_check_in`, `tv` - or raw numeric Airbnb amenity ids |
| `currency` | string | `USD` | ISO 4217 |
| `page` | integer | -- | 1-based, 18 listings per page. **Cannot be combined with `cursor`** |
| `cursor` | string | -- | `next_cursor` from a previous response. Wins over `page` |

`room_type` and the named amenities are validated **before** the scrape, on purpose: an unrecognised value makes Airbnb return the *unfiltered* set under a `200`, so the user would pay for a filter that never ran.

### Listing (`/listing`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `listing_id` | string | required | Listing id or full `/rooms/` URL; query params discarded |
| `check_in` / `check_out` | string | -- | `YYYY-MM-DD`, sent together and in order |
| `adults` / `children` / `infants` / `pets` | integer | -- | Party composition |
| `currency` | string | `USD` | ISO 4217 |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `listing_id` | string | required | Listing id or full `/rooms/` URL |
| `limit` | integer | `30` | 1-50. Send it explicitly - see the paging note |
| `offset` | integer | `0` | Row offset |
| `currency` | string | `USD` | ISO 4217 |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=airbnb-scraper-api. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search a real date window - min_price/max_price are the WHOLE-STAY total
found = requests.post(f"{BASE}/api/v1/airbnb/search", headers=HEADERS,
    json={"location": "Austin, TX", "check_in": "2026-09-08", "check_out": "2026-09-13",
          "adults": 2, "max_price": 1500, "room_type": "entire_home",
          "amenities": "wifi,pool", "currency": "USD"}).json()

assert found["data"]["dates_are_defaulted"] is False   # you sent dates, so this is False

row = found["data"]["listings"][0]
listing_id, stay_price = row["listing_id"], row["price"]

# 2. Listing detail: amenities, host, house rules, rating breakdown - NO price
listing = requests.post(f"{BASE}/api/v1/airbnb/listing", headers=HEADERS,
    json={"listing_id": listing_id}).json()

print(listing["data"]["category_ratings"])   # cleanliness, accuracy, check-in, ...

# 3. Review bodies - always send limit explicitly, then step offset
reviews = requests.post(f"{BASE}/api/v1/airbnb/reviews", headers=HEADERS,
    json={"listing_id": listing_id, "limit": 30, "offset": 0}).json()

print(reviews["data"]["count"], reviews["data"]["returned"])   # total vs this page
```

Paging: cursor **or** page, never both.

```python
def search_pages(location, max_pages=3, **body):
    """18 listings per page, 1 credit per page."""
    out, cursor = [], None
    for _ in range(max_pages):
        payload = {"location": location, **body}
        if cursor:
            payload["cursor"] = cursor          # never alongside "page"
        data = requests.post(f"{BASE}/api/v1/airbnb/search",
                             headers=HEADERS, json=payload).json()["data"]
        out += data["listings"]
        cursor = data["next_cursor"]
        if not cursor:
            break
    return out


def all_reviews(listing_id, max_pages=4, limit=50):
    out = []
    for i in range(max_pages):
        data = requests.post(f"{BASE}/api/v1/airbnb/reviews", headers=HEADERS,
                             json={"listing_id": listing_id,
                                   "limit": limit, "offset": i * limit}).json()["data"]
        out += data["reviews"]
        if data["returned"] < limit or len(out) >= data["count"]:
            break
    return out
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **search** — `url`, `location`, `resolved_location`, `city`, `state`, `country`, `place_precision`, `coordinates`, `map_bounds`, `check_in`, `check_out`, `nights`, `dates_are_defaulted`, `currency`, `guests`, `page`, `page_count`, `next_cursor`, `count`, `listings[]` (`pos`, `listing_id`, `listing_node_id`, `url`, `name`, `title`, `subtitle`, `rating`, `review_count`, `rating_label`, `bedrooms`, `beds`, `baths`, `price`, `badges`, `is_guest_favorite`, `is_superhost`, `coordinates`, `images`).
- **listing** — `listing_id`, `url`, `name`, `headline`, `description`, `description_html`, `summary`, `property_type`, `room_type`, `space_type`, `person_capacity`, `overview`, `bedrooms`, `beds`, `baths`, `rating`, `review_count`, `is_guest_favorite`, `is_new_listing`, `coordinates`, `address`, `neighborhood`, `breadcrumbs`, `host`, `amenities`, `amenity_groups`, `highlights`, `sleeping_arrangements`, `photo_tour`, `images`, `thumbnail`, `house_rules`, `safety_and_property`, `cancellation_policy`, `additional_house_rules`, `check_in_time`, `check_in_end_time`, `check_out_time`, `category_ratings[]` (`category`, `label`, `rating`). **No price field of any kind.**
- **reviews** — `listing_id`, `url`, `count` (the listing's total), `rating`, `returned` (this page), `reviews[]` (`id`, `text`, `rating`, `language`, `created_at`, `date`, `reviewer_id`, `reviewer_name`, `reviewer_photo`).

```json
{
  "data": {
    "location": "Austin, TX",
    "check_in": "2026-09-08",
    "check_out": "2026-09-13",
    "nights": 5,
    "dates_are_defaulted": false,
    "currency": "USD",
    "page": 1,
    "page_count": 15,
    "next_cursor": "eyJzZWN0aW9uX29mZnNldCI6...",
    "count": 18,
    "listings": [
      {
        "pos": 1,
        "listing_id": "1234567890",
        "name": "Sunny East Austin bungalow",
        "rating": 4.92,
        "review_count": 318,
        "bedrooms": 2,
        "beds": 3,
        "baths": 1,
        "is_guest_favorite": true,
        "url": "https://www.airbnb.com/rooms/1234567890"
      }
    ]
  },
  "credits_used": 1,
  "credits_remaining": 999
}
```

## Guardrails

- Every call is **1 credit**, including one that comes back empty.
- **Never quote a nightly rate from `/listing`** - there is none. Prices come from `/search` only.
- Always check `dates_are_defaulted`. If it is `true`, Airbnb chose the window and A/B tested the prices; say so instead of presenting the figure as the user's dates.
- `min_price` / `max_price` are the **whole-stay total**. If the user thinks in nightly terms, convert and tell them which one you filtered on.
- Send `currency` on every call. Two identical requests without it can disagree.
- Send `page` **or** `cursor`, never both - the request is rejected.
- On `/reviews`, always send an explicit `limit`, and use exactly `limit` / `offset`. The underscored variants silently return the same 7 rows forever.
- Never invent a `room_type` or amenity name. Unrecognised values are rejected before the scrape precisely so the user is not billed for a filter Airbnb would have ignored.
- Never fabricate listing names, prices, ratings, host details or review text. Only return what the API returned.
- Review text and host profiles are personal data about real people. Summarise; do not build profiles of individuals.

## Failure handling

- `400` means an invalid or missing parameter - an unpaired or out-of-order date, `min_price` above `max_price`, `page` sent together with `cursor`, or an unrecognised `room_type` / amenity name. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means Airbnb could not resolve the location, or the listing id does not exist.
- `429` means rate or usage limit exceeded. Wait before retrying. See https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=airbnb-scraper-api.
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry, up to a few times. Airbnb occasionally serves a geo domain-switch interstitial; the transport already retries that internally, so a 502 that survives to you is real.
- An empty result set is usually the filters - widen `max_price` (remember it is the stay total), drop `superhost` / `guest_favorite`, or shorten the stay.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.airbnb.search("Austin, TX", check_in="2026-09-08", check_out="2026-09-13",
                             adults=2, max_price=1500, currency="USD")
listing_id = found["data"]["listings"][0]["listing_id"]

listing = client.airbnb.listing(listing_id)          # amenities + rating breakdown, no price
reviews = client.airbnb.reviews(listing_id, limit=50, offset=0)
```

```bash
npm install scavio@0.15.0
```

```javascript
import { Scavio } from "scavio";

const client = new Scavio(); // reads SCAVIO_API_KEY
const found = await client.airbnb.search({
  location: "Austin, TX", check_in: "2026-09-08", check_out: "2026-09-13", currency: "USD",
});
const reviews = await client.airbnb.reviews({ listing_id: "1234567890", limit: 50, offset: 0 });
```
