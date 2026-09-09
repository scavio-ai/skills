# TikTok Ad Library API - Search Ads, Top Ads, Ad Detail

Search the ads running on TikTok by keyword and/or industry, pull the top-performing ads with a written performance highlight, and open one ad in full with its objective, engagement, the countries it ran in, its landing page and a playable video. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find TikTok ads for a brand, keyword, product or industry
- See what ads a competitor is running on TikTok and how they perform
- Pull the top-performing TikTok ads in a niche for creative research or swipe files
- Get one ad in full: objective, click-through rate, likes, the countries it ran in, its landing page and the video
- Do paid-social / creative research or ad-intelligence work on TikTok

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-ad-library-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-ad-library-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Every TikTok Ads endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/tiktok/ads/search` | 1 | Ads matching a keyword and/or industry: `ad_id`, title, brand, objective, click-through rate, likes, and a video cover, with pagination |
| `POST /api/v1/tiktok/ads/top` | 1 | The top-performing ads, optionally by industry and country: click-through rate, likes, a written performance highlight, and a video cover |
| `POST /api/v1/tiktok/ads/detail` | 1 | One ad in full: title, brand, objective, click-through rate, likes, comments, shares, the countries it ran in, its landing page, and a playable video URL |

## Parameters

### `ads/search`

Provide a `keyword` or an `industry` (or both).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | -- | Keyword to match ad copy and creative by |
| `industry` | string | -- | Restrict to a single industry key (e.g. `label_22108000000`) |
| `country` | string | `US` | Two-letter country the ad ran in |
| `objective` | string | -- | Restrict to a campaign objective |
| `ad_format` | string | -- | Restrict to a given ad format |
| `period` | number | `180` | Lookback window in days: `7`, `30` or `180` |
| `order_by` | string | -- | Result ordering (e.g. `for_you`) |
| `page` | number | `1` | Page number (1-100) |
| `limit` | number | `20` | Results per page (1-50) |

### `ads/top`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `industry` | string | -- | Restrict to a single industry key |
| `country` | string | -- | Two-letter country the ad ran in |
| `page` | number | `1` | Page number (1-100) |
| `limit` | number | `20` | Results per page (1-50) |

### `ads/detail`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ad_id` | string | required | The ad's numeric id, as carried by every search and top result |

## Scope notes

- `ads/search` **requires a keyword or an industry** - a bare call with neither is rejected.
- `search` and `top` rows carry a `video.cover` image but not a playable file. To get a downloadable MP4, call `ads/detail` with the `ad_id`, which returns `video.url`.
- `video.url` and `video.cover` links are directly usable but signed with a **short expiry** - fetch them promptly rather than storing the URL.
- `top` returns TikTok's curated top performers, so it does not deep-paginate the way `search` does.
- Results are scoped to a `country` (search defaults to `US`) and, for search, a lookback `period`.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search ads for a brand in the last 180 days
search = requests.post(f"{BASE}/api/v1/tiktok/ads/search", headers=HEADERS,
    json={"keyword": "nike", "country": "US", "period": 180, "limit": 20}).json()
for ad in search["data"]["ads"]:
    print(ad["ad_id"], ad["ctr"], ad["title"])

# 2. Top-performing ads in an industry
top = requests.post(f"{BASE}/api/v1/tiktok/ads/top", headers=HEADERS,
    json={"industry": "label_22108000000", "country": "US"}).json()

# 3. One ad in full, including a playable video URL, by an id from search
ad_id = search["data"]["ads"][0]["ad_id"]
detail = requests.post(f"{BASE}/api/v1/tiktok/ads/detail", headers=HEADERS,
    json={"ad_id": ad_id}).json()
d = detail["data"]
print(d["brand"], d["objective"], d["countries"], d["video"]["url"])
```

curl:

```bash
curl -s https://api.scavio.dev/api/v1/tiktok/ads/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword":"nike","country":"US","period":180}'
```

## Response shape

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. On `search` and `top`, `data` carries `ads[]` plus a `pagination` block; on `detail`, `data` is the ad object with a nested `video` (`id`, `duration`, `cover`, and a playable `url`).

## Guardrails

- Every TikTok Ads call is **1 credit**.
- Never fabricate ad copy, brands, click-through rates, likes or landing pages. Only return what the API returned.
- `search` and `top` do not include a playable video - only `detail` returns `video.url`. Do not claim a downloadable video from a search row.
- Video and cover URLs expire quickly - fetch promptly rather than storing the link.

## Failure handling

- `400` means an invalid request - most often `search` called with neither `keyword` nor `industry`. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the ad id was not found.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-ad-library-api).
- `502` / `503` mean the source is temporarily unavailable - wait a few seconds and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
