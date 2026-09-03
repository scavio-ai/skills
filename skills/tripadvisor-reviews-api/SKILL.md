---
name: tripadvisor-reviews-api
description: "Tripadvisor reviews API: resolve any place or business name to Tripadvisor ids, list ranked restaurants, hotels and attractions in a geo, read a location in full (rating histogram, sub-ratings, city ranking, price band, amenities, contact), and page reviews with trip date, trip type and management response. 4 endpoints, 2 credits each."
version: 1.0.0
tags: tripadvisor, tripadvisor-reviews, tripadvisor-api, hotels, restaurants, attractions, reviews, ratings, travel, hospitality, local-business, review-mining, reputation-monitoring, agents, structured-data, json, ai-agents, scraping-api
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F989"
    homepage: https://scavio.dev/docs/tripadvisor-locations?utm_source=agent-skills&utm_medium=skill&utm_campaign=tripadvisor-reviews-api
---

# Tripadvisor Reviews API - Hotels, Restaurants, Attractions

Resolve a place or business name to Tripadvisor's own ids, list ranked restaurants, hotels and attractions in a geo, read one location in full, and page through its reviews. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find the top-rated restaurants, hotels or attractions in a city or area
- Look up one venue's Tripadvisor rating, ranking, price band, cuisines, amenities, hours and contact details
- Read Tripadvisor review bodies with trip dates, trip types and management responses
- Compare a venue against its local competitive set
- Monitor a venue's reputation and review flow
- Turn a place NAME into the ids Tripadvisor's own URLs use

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=tripadvisor-reviews-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=tripadvisor-reviews-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Every Tripadvisor endpoint costs **2 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/tripadvisor/locations` | 2 | **START HERE.** Resolves a place or business NAME to `geo_id` / `location_id` |
| `POST /api/v1/tripadvisor/search` | 2 | Restaurants / hotels / attractions in a geo, Tripadvisor-ranked; each row carries the `location_id` + `geo_id` pair |
| `POST /api/v1/tripadvisor/location` | 2 | One location in full: rating histogram, sub-ratings, city ranking, price band, cuisines, amenities, contact, photos, **and the first page of reviews** |
| `POST /api/v1/tripadvisor/reviews` | 2 | A page of reviews: rating, trip date and type, reviewer home town and contribution count, management response |

## Workflow

**Start at `/locations`.** Every other endpoint is keyed by ids that exist only inside Tripadvisor's own URLs, so a caller holding a place name has no other entry point.

1. **Resolve the name:** call `/tripadvisor/locations` with `query`. Each result carries `type`, `geo_id` and `location_id`.
   - A **GEO** row (a city or region) answers `geo_id` for `/search`. Its `location_id` is `null`.
   - A **business** row answers the `geo_id` + `location_id` pair that `/location` and `/reviews` take.
2. **List a geo:** call `/tripadvisor/search` with `geo_id` and a `category` (`restaurants`, `hotels`, `attractions`). Or paste a full Tripadvisor listing URL as `url` instead.
3. **One venue:** call `/tripadvisor/location` with `location_id` (+ `geo_id`) or a full `_Review` URL. **Page 1 of the reviews already rides along here.**
4. **More reviews:** call `/tripadvisor/reviews` only to page *past* the first page.

### Pagination

- **`/search`** renders **30 locations per page**. A page beyond the last is a **404**, not an empty result.
- **`/reviews`** page size depends on the family - **15 for restaurants, 10 for hotels and attractions** - so `category` must match the location's own type on any page past the first, or you will page in the wrong stride.
- Consecutive review pages can **repeat one review at the boundary**. De-duplicate on `review_id` when concatenating.
- **`/locations`** and **`/location`** do not page. On `/locations`, `limit` only sizes the single response (1-20, default 12); it is not a page parameter.

## Parameters

### Locations lookup (`/locations`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Place or business name (1-120 chars) |
| `limit` | integer | `12` | 1-20. Sizes this response only; not pagination |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `geo_id` | string | one of | Accepts `30196`, `g30196`, or a URL carrying one |
| `url` | string | one of | Full tripadvisor.com listing URL (country sites and subdomains accepted) |
| `category` | string | `restaurants` | `restaurants`, `hotels`, `attractions` |
| `page` | integer | -- | 1-based, 30 locations per page |

`geo_id` or `url` is required.

### Location (`/location`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location_id` | string | one of | Accepts `1899234`, `d1899234`, or a full `_Review` URL |
| `url` | string | one of | Full Tripadvisor location URL |
| `geo_id` | string | -- | Required alongside a bare `d`-id |
| `category` | string | `restaurants` | `restaurants`, `hotels`, `attractions` |

`location_id` or `url` is required; a bare `d`-id additionally needs a geo.

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location_id` | string | one of | Location id, or send `url` instead |
| `url` | string | one of | Full Tripadvisor location URL |
| `geo_id` | string | -- | Geo the location belongs to |
| `category` | string | `restaurants` | Must match the location's own type - it sets the page stride |
| `page` | integer | -- | 1-based. 15/page restaurants, 10/page hotels and attractions. Past the last page is a 404 |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. ALWAYS START HERE - a name is not an id
places = requests.post(f"{BASE}/api/v1/tripadvisor/locations", headers=HEADERS,
    json={"query": "Austin, Texas"}).json()

geo = next(r for r in places["data"]["results"] if r["type"] == "GEO")

# 2. Ranked restaurants in that geo
listing = requests.post(f"{BASE}/api/v1/tripadvisor/search", headers=HEADERS,
    json={"geo_id": geo["geo_id"], "category": "restaurants"}).json()

row = listing["data"]["results"][0]

# 3. One venue in full - page 1 of its reviews comes along for free
venue = requests.post(f"{BASE}/api/v1/tripadvisor/location", headers=HEADERS,
    json={"location_id": row["location_id"], "geo_id": row["geo_id"],
          "category": "restaurants"}).json()

# 4. Page PAST that first page - keep category in step with the venue type
more = requests.post(f"{BASE}/api/v1/tripadvisor/reviews", headers=HEADERS,
    json={"location_id": row["location_id"], "geo_id": row["geo_id"],
          "category": "restaurants", "page": 2}).json()
```

Concatenating review pages, de-duplicated on `review_id`:

```python
def review_pages(location_id, geo_id, category="restaurants", pages=(2, 3, 4)):
    """2 credits per page. Page 1 already came with /location."""
    seen, out = set(), []
    for page in pages:
        data = requests.post(f"{BASE}/api/v1/tripadvisor/reviews", headers=HEADERS,
                             json={"location_id": location_id, "geo_id": geo_id,
                                   "category": category, "page": page}).json()["data"]
        for r in data["reviews"]:
            if r["review_id"] not in seen:      # pages overlap at the boundary
                seen.add(r["review_id"])
                out.append(r)
    return out
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **locations** — `query`, `count`, `results[]` (`pos`, `type` (`GEO` or a business type), `name`, `geo_id`, `location_id` (`null` on a GEO row), `url`, `latitude`, `longitude`, `category`).
- **search** — `geo_id`, `category`, `location`, `url`, `page`, `count`, `breadcrumbs`, `results[]` (`pos`, `location_id`, `geo_id`, `type`, `name`, `rank`, `url`, `image`, `rating`, `review_count`, `price_range`, `price`, `cuisines`, `street_address`, `city`, `region`, `postal_code`, `country`, `address`, `latitude`, `longitude`, `phone`, `hours`, `menu_url`, `accepts_reservations`, `description`, `ranking`, `review_snippet`, `travelers_choice`, `sponsored`).
- **location** — `location_id`, `geo_id`, `type`, `url`, `name`, `description`, `rating`, `review_count`, `rating_distribution`, `subratings`, `ranking`, `ranking_position`, `ranking_total`, `ranking_category`, `price_range`, `cuisines`, `meal_types`, `special_diets`, `street_address`, `city`, `region`, `postal_code`, `country`, `address`, `latitude`, `longitude`, `phone`, `website`, `menu_url`, `hours`, `hours_text`, `open_now`, `amenities`, `features`, `image`, `images`, `photo_count`, `travelers_choice`, `breadcrumbs`, `reviews[]` (page 1).
- **reviews** — `location_id`, `geo_id`, `type`, `url`, `name`, `rating`, `review_count`, `rating_distribution`, `offset`, `count`, `reviews[]` (`pos`, `review_id`, `url`, `title`, `text`, `rating`, `published_date`, `trip_date`, `trip_type`, `author`, `author_url`, `author_location`, `author_contributions`, `helpful_votes`, `owner_response`, `owner_response_date`, `owner_response_from`).

```json
{
  "data": {
    "query": "Austin, Texas",
    "count": 10,
    "results": [
      {
        "pos": 1,
        "type": "GEO",
        "name": "Austin, Texas, United States",
        "geo_id": "30196",
        "location_id": null,
        "url": "https://www.tripadvisor.com/Tourism-g30196-Austin_Texas-Vacations.html",
        "latitude": 30.267223,
        "longitude": -97.742546,
        "category": "Destinations"
      }
    ]
  },
  "credits_used": 2,
  "credits_remaining": 998
}
```

## Guardrails

- Every call is **2 credits**, including one that comes back empty. A name-to-reviews walk is four calls and 8 credits before any paging - say so before starting.
- **Never guess a `geo_id` or `location_id`.** Resolve the name with `/locations` first; ids only exist inside Tripadvisor's URLs.
- Do not call `/reviews` with `page: 1` after `/location` - you already have that page, and the repeat costs another 2 credits.
- Keep `category` matched to the venue's own type when paging reviews. A restaurant pages in 15s and a hotel in 10s; a mismatch silently skips or repeats reviews.
- De-duplicate on `review_id` when you concatenate pages - the boundary review can repeat.
- Do not ask for a page beyond the last; it is a billed 404, not an empty list.
- A rating and a city ranking are Tripadvisor's, computed from reviews Tripadvisor chose to display. Attribute them.
- Never fabricate venue names, ratings, rankings or review text. Only return what the API returned.

## Failure handling

- `400` means an invalid or missing parameter - neither `geo_id` nor `url` on search, neither `location_id` nor `url` on location/reviews, a bare `d`-id with no geo, or a `category` outside the enum. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the id does not exist or the page is past the last one. Tripadvisor answers an unknown location id with a **billed** `200` city listing that the API restates as a 404 - re-resolve the name with `/locations` rather than retrying the id.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=tripadvisor-reviews-api).
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry, up to a few times.
- If `/locations` returns nothing useful, try the fuller place name ("Austin, Texas" rather than "Austin").
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

places = client.tripadvisor.locations("Austin, Texas")
geo = next(r for r in places["data"]["results"] if r["type"] == "GEO")

listing = client.tripadvisor.search(geo_id=geo["geo_id"], category="restaurants")
row = listing["data"]["results"][0]

venue = client.tripadvisor.location(location_id=row["location_id"], geo_id=row["geo_id"])
more = client.tripadvisor.reviews(location_id=row["location_id"], geo_id=row["geo_id"], page=2)
```

```bash
npm install scavio@0.15.0
```

```javascript
import { Scavio } from "scavio";

const client = new Scavio(); // reads SCAVIO_API_KEY
const places = await client.tripadvisor.locations({ query: "Austin, Texas" });
const listing = await client.tripadvisor.search({ geo_id: "30196", category: "restaurants" });
```
