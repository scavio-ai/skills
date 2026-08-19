---
name: yelp-business-data
description: "Yelp business data API: search businesses in a metro, pull one business in full with hours, amenities and health inspections, and page through reviews. Returns rating, review count, price band, categories, address, contact details, photos, and review text with owner responses. 3 endpoints, 2 credits each, structured JSON."
version: 1.0.0
tags: yelp, yelp-api, yelp-reviews, business-data, local-business, business-listings, ratings, review-mining, business-hours, local-seo, lead-generation, reputation-management, restaurants, langchain, crewai, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\u2B50"
    homepage: https://scavio.dev/docs/yelp-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=yelp-business-data
---

# Yelp Business Data API - Search, Business Detail, Reviews

Search Yelp businesses in a metro, read one business in full, and page through its reviews. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find local businesses by term and location, in Yelp's ranked order
- Filter by price band, open-now, or Yelp's own attribute aliases
- Pull one business in full - rating histogram, price band, categories, address and coordinates, phone, website and menu links, hours and holidays, amenities, photos, popular items, health inspections, Q&A, licences, claim status
- Read review bodies with author expertise, attached photos, reaction counts and the owner's response
- Build local-lead lists, reputation monitors or competitor comp sets

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=yelp-business-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every Yelp endpoint costs **2 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/yelp/search` | 2 | Businesses in Yelp's ranked order: rating, review count, price band, categories, address, contact rails, hours, photos, review snippet; each row carries `business_id` **and** `alias` |
| `POST /api/v1/yelp/business` | 2 | One business in full - **plus the first page of reviews at no extra cost** |
| `POST /api/v1/yelp/reviews` | 2 | A page of reviews: rating, full text, language, author profile and expertise counts, attached photos, reaction counts, owner response |

## Workflow

1. **Find businesses:** call `/yelp/search` with `term` **and** `location` (or a full `yelp.com/search` URL as `url`). Read `businesses[].business_id` or `alias`.
2. **One business:** call `/yelp/business` with that `business_id` - an alias like `desnudo-coffee-austin-2`, the opaque encid, or a `yelp.com/biz` URL all work. **This already includes page 1 of the reviews.**
3. **More reviews:** call `/yelp/reviews` starting at **`page: 2`**.

### The two ways to waste 2 credits

- **`/yelp/reviews` with `page: 1` re-fetches the document `/business` already returned.** It is the same content for another 2 credits. Always start review paging at page 2.
- **A search without `location`** is answered off the proxy exit, so the same request reports on a different metro from one run to the next. `location` is effectively required even though the schema allows a `url` instead.

### Pagination

Yelp fixes the page size at **10** for both search and reviews.

- **`/search`** takes a 1-based `page`. `count` is the 10-row page, `total_results` is Yelp's headline count, `results_per_page` and `start` are echoed back.
- **`/reviews`** takes a 1-based `page` and carries `has_next_page`. A page past the last review is a **404**, not an empty result - stop on `has_next_page: false`.
- **`/business`** takes no paging parameter.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `term` | string | with `location` | What to look for (1-200 chars) |
| `location` | string | with `term` | Metro, neighbourhood or address (1-200 chars) |
| `url` | string | alternative | Full `yelp.com/search` URL instead of term + location (1-1000 chars) |
| `page` | integer | -- | 1-based, page size fixed at 10 |
| `sort` | string | `recommended` | `recommended`, `rating`, `review_count` |
| `price` | integer[] | -- | Any of `1`, `2`, `3`, `4` (1-4 items) |
| `open_now` | boolean | -- | Open at request time |
| `attributes` | string[] | -- | Raw Yelp filter aliases, max 20 (`RestaurantsDelivery`, `GoodForKids`, `WheelchairAccessible`) |

`(term AND location)` or `url` is required.

`sort` is closed - Yelp **ignores** an unrecognised sort and serves default ranking under a `200`, so an invented value buys a premium scrape of a sort that never ran. `attributes` is the opposite: a deliberate passthrough, because Yelp's vocabulary runs to roughly 117 aliases per vertical. An alias Yelp does not know is ignored upstream and the results come back unfiltered - so check that the filter you asked for is reflected in the results before reporting it as applied.

### Business (`/business`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `business_id` | string | one of | Alias (`desnudo-coffee-austin-2`), opaque encid, or a `yelp.com/biz` URL |
| `url` | string | one of | Full `yelp.com/biz` URL |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `business_id` | string | one of | Alias, encid, or biz URL |
| `url` | string | one of | Full `yelp.com/biz` URL |
| `page` | integer | -- | **Start at 2** - page 1 is what `/business` already returned |
| `sort` | string | `relevance` | `relevance`, `newest`, `oldest`, `rating_high`, `rating_low`, `elites` |
| `rating` | integer | -- | `1`-`5`. Changes `filtered_review_count`, not `review_count` |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Always send location - a location-less search follows the proxy exit
found = requests.post(f"{BASE}/api/v1/yelp/search", headers=HEADERS,
    json={"term": "coffee", "location": "Austin, TX",
          "sort": "review_count", "price": [1, 2], "open_now": True}).json()

row = found["data"]["businesses"][0]

# 2. Full business record - page 1 of the reviews rides along free
biz = requests.post(f"{BASE}/api/v1/yelp/business", headers=HEADERS,
    json={"business_id": row["alias"]}).json()["data"]

print(biz["rating"], biz["review_count"], biz["not_recommended_review_count"])
first_page_reviews = biz["reviews"]

# 3. Page PAST it. Never ask for page 1 here - it is the same 2 credits twice.
more = requests.post(f"{BASE}/api/v1/yelp/reviews", headers=HEADERS,
    json={"business_id": row["alias"], "page": 2, "sort": "newest"}).json()["data"]

# 4. One-star reviews only: filtered_review_count is the count that matches
one_star = requests.post(f"{BASE}/api/v1/yelp/reviews", headers=HEADERS,
    json={"business_id": row["alias"], "rating": 1, "page": 2}).json()["data"]
print(one_star["filtered_review_count"], "of", one_star["review_count"])
```

Paging reviews, stopping on the signal Yelp actually gives:

```python
def review_pages(business_id, start=2, max_pages=4, **body):
    """10 per page, 2 credits per page. Page 1 came free with /business."""
    out = []
    for page in range(start, start + max_pages):
        data = requests.post(f"{BASE}/api/v1/yelp/reviews", headers=HEADERS,
                             json={"business_id": business_id, "page": page, **body}).json()["data"]
        out += data["reviews"]
        if not data["has_next_page"]:      # past the last page is a billed 404
            break
    return out
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **search** — `term`, `location`, `url`, `location_display`, `city`, `state`, `country`, `latitude`, `longitude`, `bounds`, `categories`, `vertical`, `sort`, `attributes`, `open_now`, `breadcrumbs`, `total_results`, `results_per_page`, `page`, `start`, `related_searches`, `count`, `businesses[]` (`pos`, `business_id`, `alias`, `name`, `url`, `rank`, `is_ad`, `rating`, `review_count`, `price_range`, `categories`, `address`, `street_address`, `city`, `state`, `postal_code`, `country`, `neighborhoods`, `timezone`, `hours`, `image`, `images`, `photos`, `snippet`, `tags`, `actions`, `highlights`, `is_yelp_guaranteed`, `has_verified_license`, `is_service_area_business`).
- **business** — `business_id`, `alias`, `name`, `url`, `summary`, `specialties`, `history`, `year_established`, `rating`, `review_count`, `rating_distribution`, `not_recommended_review_count`, `review_counts_by_language`, `price_range`, `categories`, `phone`, `website`, `menu_url`, `address`, `city`, `state`, `postal_code`, `country`, `neighborhoods`, `timezone`, `latitude`, `longitude`, `service_areas`, `hours[]`, `hours_today`, `is_open_now`, `is_closed`, `holidays`, `attributes`, `amenities`, `popular_items[]`, `popular_items_omitted`, `review_highlights`, `health_inspections`, `question_count`, `questions`, `is_claimed`, `is_advertiser`, `verified_licenses`, `messaging_response_time`, `filtered_review_count`, `reviews[]` (page 1).
- **reviews** — `business_id`, `alias`, `name`, `url`, `rating`, `review_count`, `rating_distribution`, `filtered_review_count`, `sort`, `rating_filter`, `start`, `page`, `has_next_page`, `count`, `reviews[]` (`pos`, `review_id`, `url`, `rating`, `text`, `language`, `published_date`, `experience_date`, `author`, `author_url`, `author_photo`, `author_expertise`, `author_expertise_count`, `photos`, `videos`, `reactions`, `is_first_review`, `previous_review_count`, `owner_response`, `owner_response_date`, `owner_response_from`, `appreciated_by_owner`).

```json
{
  "data": {
    "term": "coffee",
    "location": "Austin, TX",
    "page": 1,
    "start": 0,
    "results_per_page": 10,
    "total_results": 240,
    "count": 10,
    "businesses": [
      {
        "pos": 1,
        "business_id": "kQ7pCn2m0Vx9",
        "alias": "desnudo-coffee-austin-2",
        "name": "Desnudo Coffee",
        "rating": 4.5,
        "review_count": 2153,
        "price_range": "$",
        "categories": ["Coffee & Tea"],
        "city": "Austin",
        "state": "TX",
        "url": "https://www.yelp.com/biz/desnudo-coffee-austin-2"
      }
    ]
  },
  "credits_used": 2,
  "credits_remaining": 998
}
```

## Guardrails

- Every call is **2 credits**, including one that comes back empty. Yelp is on the premium proxy table - budget before paging.
- **Never call `/reviews` with `page: 1`.** `/business` already returned that page; the repeat is 2 credits for a duplicate.
- **Always send `location`.** Without it the answer is about wherever the request exited, and it can differ between two identical runs.
- Never invent a `sort` value. An unrecognised sort is ignored and you pay for default ranking.
- `attributes` is a passthrough, so an alias Yelp does not recognise silently disappears. Verify the filter took effect before telling the user it was applied.
- `rating` on `/reviews` changes `filtered_review_count`, not `review_count`. Quote the right one.
- Yelp's recommendation software hides some reviews entirely. Those are never returned and are counted in `not_recommended_review_count` - so the reviews you can read are not the whole picture, and an average you compute yourself will not match Yelp's.
- `popular_items` can arrive as stub shells; those rows are dropped and `popular_items_omitted` flags it. If that flag is `true`, do not claim the item list is complete.
- Never fabricate business names, ratings, addresses, hours or review text. Only return what the API returned.
- Always include the business `url` so the user can verify.

## Failure handling

- `400` means an invalid or missing parameter - `term` without `location` and no `url`, a `sort` outside its enum, or more than 20 attributes. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the business does not exist, or the review page is past the last one. Stop on `has_next_page: false` rather than discovering the end with a billed 404.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=yelp-business-data).
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry, up to a few times.
- An empty search is usually the filters: drop `open_now`, widen `price`, or use a broader `term`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.yelp.search(term="coffee", location="Austin, TX", sort="review_count")
alias = found["data"]["businesses"][0]["alias"]

biz = client.yelp.business(business_id=alias)          # includes page 1 of reviews
more = client.yelp.reviews(business_id=alias, page=2)  # start at 2, never 1
```

```bash
npm install scavio@0.15.0
```

```javascript
import { Scavio } from "scavio";

const client = new Scavio(); // reads SCAVIO_API_KEY
const found = await client.yelp.search({ term: "coffee", location: "Austin, TX" });
const more = await client.yelp.reviews({ business_id: found.data.businesses[0].alias, page: 2 });
```
