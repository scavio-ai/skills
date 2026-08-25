---
name: linkedin-ad-library-api
description: Search ads running across LinkedIn by keyword and/or advertiser company id, returning each ad's advertiser, ad copy, format, promoted label, thumbnail and a detail link, then open one ad in full with its media, headline, who paid for it and the advertiser's company URL. 2 endpoints, 6 credits each, structured JSON.
version: 1.0.0
tags: linkedin-ads, linkedin-ad-library, ad-library-api, b2b-ads, competitor-ads, ad-creative, ad-intelligence, paid-social, marketing-research, sponsored-content, demand-gen, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F4BC"
    homepage: https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=linkedin-ad-library-api
---

# LinkedIn Ad Library API - Search Ads and Ad Detail

Search the ads running across LinkedIn by keyword and/or advertiser, then open any ad in full with its creative, headline, format, who paid for it and the advertiser's company URL. Both endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find LinkedIn ads for a keyword, topic or advertiser
- See what ads a company is running on LinkedIn and pull the creative
- Build a competitor swipe file of B2B / sponsored-content ads
- Get one ad in full: advertiser, ad copy, headline, format, media and who paid for it
- Do paid-social, demand-gen or ad-intelligence research on LinkedIn

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=linkedin-ad-library-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every LinkedIn Ads endpoint costs **6 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/linkedin/ads/search` | 6 | The ads on the page for a keyword and/or advertiser: `ad_id`, advertiser, ad copy, format, creative type, sponsored flag, headline, thumbnail, advertiser logo, and a detail link |
| `POST /api/v1/linkedin/ads/detail` | 6 | One ad in full: advertiser and company URL, who paid for it, ad copy, headline, format, the media items, and a detail link |

## Parameters

### `ads/search`

Provide a `keyword` or a `company_id` (or both).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | -- | Keyword to search ads by |
| `company_id` | string | -- | The advertiser's numeric LinkedIn company id |
| `countries` | string or string[] | -- | One or more 2-letter country codes to restrict results to |
| `date_option` | string | -- | Restrict to ads seen within a recent time window |

### `ads/detail`

Provide an `ad_id` or a `url` (one is required).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ad_id` | string | -- | The ad's numeric id, as carried by every search result |
| `url` | string | -- | A full ad detail URL (`linkedin.com/ad-library/detail/...`), as an alternative to `ad_id` |

## Scope notes

- `ads/search` **requires a keyword or a company_id** - a bare call with neither is rejected.
- `search` returns the ads on **one page** and a `total_seen` count; it does not deep-paginate the whole library.
- `company_id` is the numeric LinkedIn company id (the digits in a company URL like `linkedin.com/company/1035`), not the vanity handle.
- `detail` carries `impressions` and `demographics` only where LinkedIn publishes them - for most non-political ads these are `null`, and `about.run_dates` may be `null` too.
- The `thumbnail`, `advertiser_logo` and `media[].url` are LinkedIn CDN links - fetch them promptly.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search ads by keyword, restricted to the US
search = requests.post(f"{BASE}/api/v1/linkedin/ads/search", headers=HEADERS,
    json={"keyword": "ai search", "countries": "US"}).json()
print(search["data"]["total_seen"], "ads seen")
for ad in search["data"]["ads"]:
    print(ad["ad_id"], ad["advertiser"], ad["format"])

# 2. Every ad from one advertiser, by numeric company id
by_company = requests.post(f"{BASE}/api/v1/linkedin/ads/search", headers=HEADERS,
    json={"company_id": "1035"}).json()

# 3. One ad in full, by an id from search
ad_id = search["data"]["ads"][0]["ad_id"]
detail = requests.post(f"{BASE}/api/v1/linkedin/ads/detail", headers=HEADERS,
    json={"ad_id": ad_id}).json()
d = detail["data"]
print(d["advertiser"], d["paid_for_by"], d["headline"])
```

curl:

```bash
curl -s https://api.scavio.dev/api/v1/linkedin/ads/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword":"ai search","countries":"US"}'
```

## Response shape

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. On `search`, `data` carries `ads[]` plus a `total_seen` count; on `detail`, `data` is the ad object with a `media[]` array and an `about` block.

## Guardrails

- Every LinkedIn Ads call is **6 credits** - more than the other social endpoints, so paginate deliberately.
- Never fabricate advertisers, ad copy, headlines or media. Only return what the API returned.
- `impressions` and `demographics` are usually `null` - do not invent spend or reach figures when they are not present.
- CDN media links expire - fetch them promptly rather than storing the URL.

## Failure handling

- `400` means an invalid request - most often `search` called with neither `keyword` nor `company_id`, or `detail` with neither `ad_id` nor `url`. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the ad id or URL was not found.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=linkedin-ad-library-api).
- `502` / `503` mean the source is temporarily unavailable - wait a few seconds and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
