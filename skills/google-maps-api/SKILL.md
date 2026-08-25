---
name: google-maps-api
description: "Google Maps local business and place data as structured JSON: search places by query and map center, fetch full place detail with address, phone, hours, rating and GPS coordinates, page reviews with sort, and run a local-SEO geo-grid to track where a business ranks across an NxN lattice of points. 4 endpoints on the v2 engine; search, place and reviews are 1 credit, geo-grid bills per point."
version: 1.0.0
tags: google-maps, google-maps-api, local-business-search, places, place-details, google-reviews, local-seo, business-listings, lead-generation, geocoding, agents, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F5FA"
    homepage: https://scavio.dev/docs/google-maps?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-maps-api
---

# Google Maps API - Local Search, Place Detail, Reviews, Rank Tracking

Search Google Maps for places, fetch enriched details for a single place, read its reviews, and track where a business ranks across a geographic grid of points — all as structured JSON. Four endpoints on the v2 engine.

## When to trigger

Use this skill when the user asks to:
- Find local businesses or places ("coffee shops near downtown Austin")
- Get a place's address, phone, hours, rating, or coordinates
- Read reviews for a business or place
- Build a local lead list or enrich places with map data
- Track where a business ranks in Google Maps local results across an area (a local-SEO geo-grid)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-maps-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

## Endpoints

| Endpoint | Credits | Description |
|---|---|---|
| `POST https://api.scavio.dev/api/v2/google/maps/search` | 1 | Search places, returns a paginated list |
| `POST https://api.scavio.dev/api/v2/google/maps/place` | 1 | Full details for one place |
| `POST https://api.scavio.dev/api/v2/google/maps/reviews` | 1 | Paginated reviews for a place |
| `POST https://api.scavio.dev/api/v2/google/maps/geo-grid` | N² | Local-pack rank of one business across an N×N grid of points |

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Workflow

1. **Search:** call `/maps/search` with a `query`. Results are in `local_results[]`, each with a `place_id`, `data_id`, `title`, `rating`, `address`, and `gps_coordinates`.
2. **Localize:** Maps uses `ll` (map center `@lat,lng,zoomz`), NOT `gl`, to decide where results come from. Pass a city center (e.g. `@30.2672,-97.7431,12z`) to focus a city. If you only have a country, pass `gl` and the API defaults `ll` to that country's center.
3. **Place details:** take a `place_id` (or `data_cid`) from search and call `/maps/place` for full info in `place_results`.
4. **Reviews:** take a `data_id` (or `place_id`) and call `/maps/reviews`. Page with `next_page_token`.

## Maps Search Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search query (1-500 chars) |
| `ll` | string | -- | Map center `@lat,lng,zoomz`. Controls result location. Defaults to `gl` country center if omitted |
| `start` | number | `0` | Result offset, multiple of 20 (0, 20, 40, ...; max 100) |
| `gl` | string | -- | Geo country, ISO 3166-1 alpha-2 |
| `hl` | string | -- | UI language, ISO 639-1 |
| `google_domain` | string | `google.com` | Regional Google domain |

## Place Details Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `place_id` | string | -- | Place ID (`ChIJ...`). One of `place_id` or `data_cid` required |
| `data_cid` | string | -- | Numeric CID. One of `place_id` or `data_cid` required |

## Reviews Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data_id` | string | -- | Data ID (`0xHEX:0xHEX`). One of `data_id` or `place_id` required |
| `place_id` | string | -- | Place ID (`ChIJ...`). One of `data_id` or `place_id` required |
| `num` | number | -- | Reviews per page (1-20) |
| `sort_by` | string | -- | `relevance`, `newest`, `highest_rating`, `lowest_rating` |
| `next_page_token` | string | -- | Pagination cursor from a prior response |
| `hl` | string | -- | UI language |
| `gl` | string | -- | Geo country |
| `google_domain` | string | `google.com` | Regional Google domain |

## Geo-Grid Rank Tracking Parameters

`/maps/geo-grid` tracks where one business ranks in the Google Maps local pack across an N×N lattice of points around a center — the classic local-SEO geo-grid. It searches `query` at every point and reports the target business's rank there, plus an aggregate summary (average, best, worst rank and coverage). Provide `target_place_id` and/or `target_name`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | The search term to measure the business's local ranking for |
| `target_place_id` | string | -- | Place ID of the business to track (exact match, preferred). One of `target_place_id`/`target_name` required |
| `target_name` | string | -- | Business name to track (case-insensitive substring match). Used when no `target_place_id` |
| `center` | object | required | Geographic center of the grid: `{ "lat": <num>, "lng": <num> }` |
| `grid_size` | number | `5` | Grid dimension N for an N×N lattice of points (`3`, `5`, or `7`) |
| `radius_km` | number | `2` | Half-extent of the grid from the center, in kilometers (max 100) |
| `zoom` | number | `13` | Map zoom level applied at every grid point (1-21) |
| `gl` | string | -- | Geo country, ISO 3166-1 alpha-2 |
| `hl` | string | -- | UI language, ISO 639-1 |
| `google_domain` | string | `google.com` | Regional Google domain |

**Credits: billed per grid point** — an N×N grid costs **N² credits** (9 for `grid_size=3`, 25 for `5`, 49 for `7`). Any point that returns no data is not charged.

## Example

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search places, focused on Austin
search = requests.post(f"{BASE}/api/v2/google/maps/search", headers=HEADERS,
    json={"query": "coffee shops", "ll": "@30.2672,-97.7431,12z"}).json()

place = search["local_results"][0]
print(place["title"], place.get("rating"), place.get("address"))

# 2. Full details for that place
detail = requests.post(f"{BASE}/api/v2/google/maps/place", headers=HEADERS,
    json={"place_id": place["place_id"]}).json()
print(detail["place_results"].get("phone"), detail["place_results"].get("hours"))

# 3. Newest reviews
reviews = requests.post(f"{BASE}/api/v2/google/maps/reviews", headers=HEADERS,
    json={"data_id": place["data_id"], "sort_by": "newest", "num": 10}).json()
for r in reviews["reviews"]:
    print(r.get("rating"), r.get("snippet"))

# 4. Geo-grid: where does a business rank across a 3x3 grid? (9 credits)
grid = requests.post(f"{BASE}/api/v2/google/maps/geo-grid", headers=HEADERS,
    json={
        "query": "coffee shop",
        "target_name": "Starbucks",
        "center": {"lat": 40.7128, "lng": -74.006},
        "grid_size": 3,
        "radius_km": 2,
    }).json()
s = grid["data"]["summary"]
print(s["points_found"], "of", s["points_total"], "points rank; avg rank", s["avg_rank"])
for point in grid["data"]["grid"]:
    print(point["lat"], point["lng"], point["rank"])
```

## Responses

Search returns `local_results[]`; place returns `place_results`; reviews returns `place_info`, `topics[]`, `reviews[]`, and `pagination`. Each also includes `response_time`, `credits_used`, `credits_remaining`, and `cached`. Geo-grid wraps its payload in `data`: `data.grid[]` (each point with `lat`, `lng`, `rank`, `found`) and `data.summary` (`points_total`, `points_found`, `avg_rank`, `best_rank`, `worst_rank`, `found_share`).

```json
{
  "local_results": [
    {
      "position": 1,
      "title": "Example Coffee",
      "place_id": "ChIJLSsVbGBZwokRR0LlGBSvMOI",
      "data_id": "0x89c259606c152b2d:0xe230af1b18e542a7",
      "rating": 4.6,
      "reviews": 1284,
      "address": "123 Main St, Austin, TX",
      "gps_coordinates": { "latitude": 30.27, "longitude": -97.74 }
    }
  ],
  "response_time": 1103,
  "credits_used": 1,
  "credits_remaining": 998,
  "cached": false
}
```

## Guardrails

- Search, place and reviews each cost 1 credit; geo-grid costs N² credits for an N×N grid (9 / 25 / 49). Inform the user before paginating through many pages or running a large grid.
- Never fabricate place names, ratings, addresses, or review text. Only return API data.
- Maps localizes by `ll` (map center), not `gl`. To search a specific city, pass its center.
- `place` needs a `place_id`/`data_cid` and `reviews` needs a `data_id`/`place_id` — always run `/maps/search` first to obtain them.

## Failure handling

- `400` means an invalid parameter (e.g. missing place identifier) — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-maps-api).
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If search returns no results, suggest a broader query or a different `ll`/`gl`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
