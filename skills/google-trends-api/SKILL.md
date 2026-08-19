---
name: google-trends-api
description: "Google Trends search-interest data as structured JSON: interest over time, interest by region (country, region, DMA or city), and related or rising queries and topics for a keyword, scoped by geo, date range and Google property, plus real-time trending searches per country. 2 endpoints, 1 credit each."
version: 1.0.0
tags: google-trends, google-trends-api, search-trends, interest-over-time, trending-searches, keyword-research, market-research, demand-signals, seasonality, seo, agents, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F4C8"
    homepage: https://scavio.dev/docs/google-trends?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-trends-api
---

# Google Trends API - Interest Over Time, By Region, Related Queries

Measure search interest for a keyword over time and geography, and pull the real-time trending searches for a country — all as structured JSON. Two endpoints, each 1 credit.

## When to trigger

Use this skill when the user asks to:
- Measure interest in a keyword over time or compare terms
- See where a term is most searched (by region)
- Find related or rising queries for a topic
- Get what's trending right now in a country

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-trends-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

## Endpoints

| Endpoint | Credits | Description |
|---|---|---|
| `POST https://api.scavio.dev/api/v2/google/trends` | 1 | Interest-over-time, by-region, and related data for a keyword |
| `POST https://api.scavio.dev/api/v2/google/trending` | 1 | Real-time trending searches for a country |

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Workflow

1. **Keyword interest:** call `/trends` with `query`. Scope with `geo` and `date` (e.g. `today 12-m`). Pick a `data_type` to get the widget you need (defaults to `TIMESERIES` + `GEO_MAP`).
2. Read `interest_over_time.timeline_data[]` for the time series and `interest_by_region[]` for geography. Use `data_type: RELATED_QUERIES` / `RELATED_TOPICS` for rising terms.
3. **Trending now:** call `/trending` with a required `geo` country code. Filter with `hours`, `cat`, `sort`, and `status`. Read `trends[]`.

## Trends Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keyword (1-500 chars) |
| `geo` | string | -- | Location code (`US`, `GB`, `US-CA`). Worldwide when empty |
| `date` | string | -- | Time range (e.g. `today 12-m`, `now 7-d`) |
| `data_type` | string | `TIMESERIES`+`GEO_MAP` | `TIMESERIES`, `GEO_MAP`, `GEO_MAP_0`, `RELATED_QUERIES`, `RELATED_TOPICS` |
| `cat` | string | -- | Category id (e.g. `71`) |
| `gprop` | string | -- | Google property: `images`, `news`, `youtube`, `froogle` (empty = web) |
| `region` | string | -- | Geo granularity: `COUNTRY`, `REGION`, `DMA`, `CITY` |
| `hl` | string | -- | UI language |
| `tz` | string | -- | Timezone offset in minutes |

## Trending Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `geo` | string | required | Country code (e.g. `US`) |
| `hours` | number | -- | Window: `4`, `24`, `48`, or `168` |
| `cat` | number | -- | Category id (`0` = all, up to 20) |
| `sort` | string | -- | `relevance`, `search_volume`, `recency`, `title` |
| `status` | string | -- | `all` or `active` |
| `hl` | string | -- | UI language |

## Example

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Interest over the last 12 months in the US
trends = requests.post(f"{BASE}/api/v2/google/trends", headers=HEADERS,
    json={"query": "bitcoin", "geo": "US", "date": "today 12-m"}).json()
for point in trends["interest_over_time"]["timeline_data"]:
    print(point["date"], point["values"][0]["value"])

# 2. What's trending in the US right now
trending = requests.post(f"{BASE}/api/v2/google/trending", headers=HEADERS,
    json={"geo": "US", "hours": 24, "sort": "search_volume"}).json()
for t in trending["trends"]:
    print(t.get("query"), t.get("search_volume"))
```

## Responses

`/trends` returns `interest_over_time.timeline_data[]` and/or `interest_by_region[]` (and related queries/topics per `data_type`). `/trending` returns `trends[]`. Each also includes `response_time`, `credits_used`, `credits_remaining`, and `cached`.

```json
{
  "interest_over_time": {
    "timeline_data": [
      { "date": "May 2026", "values": [{ "query": "bitcoin", "value": "72" }] }
    ]
  },
  "interest_by_region": [
    { "location": "El Salvador", "value": "100" }
  ],
  "response_time": 1220,
  "credits_used": 1,
  "credits_remaining": 992,
  "cached": false
}
```

## Guardrails

- Each call costs 1 credit.
- Never fabricate interest values, regions, or trending terms. Only return API data.
- Trends `value` is a relative 0-100 index, not an absolute search count — describe it as relative interest.
- `/trending` requires a `geo` country code.

## Failure handling

- `400` means an invalid parameter (e.g. `/trending` without `geo`) — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-trends-api).
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If a widget is empty, try a different `data_type`, a broader `date`, or drop `geo` for worldwide.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
