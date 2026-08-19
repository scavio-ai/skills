---
name: google-maps-api
description: "Google Maps local business and place data as structured JSON: search places by query and map center, fetch full place detail with address, phone, hours, rating and GPS coordinates, and page reviews with sort. 3 endpoints, 1 credit per request, v2 engine."
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

# Google Maps API - Local Business Search, Place Detail, Reviews

Search Google Maps for places, fetch enriched details for a single place, and read its reviews — all as structured JSON. Three endpoints, each 1 credit.

## When to trigger

Use this skill when the user asks to:
- Find local businesses or places ("coffee shops near downtown Austin")
- Get a place's address, phone, hours, rating, or coordinates
- Read reviews for a business or place
- Build a local lead list or enrich places with map data

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

## Example

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-maps-api. Load it from your environment or secret
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
```

## Responses

Search returns `local_results[]`; place returns `place_results`; reviews returns `place_info`, `topics[]`, `reviews[]`, and `pagination`. Each also includes `response_time`, `credits_used`, `credits_remaining`, and `cached`.

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

- Each call costs 1 credit. Inform the user before paginating through many pages.
- Never fabricate place names, ratings, addresses, or review text. Only return API data.
- Maps localizes by `ll` (map center), not `gl`. To search a specific city, pass its center.
- `place` needs a `place_id`/`data_cid` and `reviews` needs a `data_id`/`place_id` — always run `/maps/search` first to obtain them.

## Failure handling

- `400` means an invalid parameter (e.g. missing place identifier) — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-maps-api.
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If search returns no results, suggest a broader query or a different `ll`/`gl`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
