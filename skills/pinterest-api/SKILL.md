---
name: pinterest-api
description: Search Pinterest pins, pull one pin with its save/share counts, read a user's profile and boards, page through a board, and look up how often external URLs have been saved. 6 endpoints, structured JSON.
version: 1.0.0
tags: pinterest, pinterest-api, pins, boards, social-media-data, visual-search, image-data, content-research, influencer-data, save-counts, url-stats, trends, agents, structured-data, json, ai-agents, scraping-api
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F4CC"
    homepage: https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=pinterest-api
---

# Pinterest API - Search, Pins, Boards, Profiles

Search Pinterest pins, pull one pin in full, read a user's profile and boards, page through a board's pins, and look up how many times external URLs have been saved. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Search Pinterest pins by keyword, with the destination link and video URL for video pins
- Pull one pin in full - save/share/comment counts, reactions, destination-page metadata, dominant color, board and pinner
- Read a user's public profile: bio, website, follower/following, pin and board counts
- List all of a user's public boards, or page through the pins inside one board
- Find how many times a given external URL has been saved to Pinterest (up to 10 URLs at once)
- Do visual-content research, trend spotting, or creator/influencer analysis on Pinterest

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=pinterest-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=pinterest-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/pinterest/search` | 1 | Pins for a keyword: title, description, image renditions, external destination link, video URL for video pins, board and pinner. Cursor-paginated |
| `POST /api/v1/pinterest/pin` | 1 | One pin in full: save/share/comment counts, reactions, destination-page metadata, video URL, dominant color, board, pinner and original pinner |
| `POST /api/v1/pinterest/profile` | 1 | A user's public profile: bio, website, follower/following, pin and board counts, merchant/partner flags, account creation date |
| `POST /api/v1/pinterest/user/boards` | 1 | All public boards of a user: name, URL, slug, description, pin/follower/section counts, cover image, owner. Cursor-paginated |
| `POST /api/v1/pinterest/board` | 1 | A board's metadata plus a page of its pins. Cursor-paginated |
| `POST /api/v1/pinterest/url-stats` | 1-2 | How many times external URLs have been saved to Pinterest, up to 10 URLs per call. **1 credit for 1-5 URLs, 2 credits for 6-10** |

## Pagination

`search`, `user/boards` and `board` are cursor-paginated. Omit `cursor` for the first page; feed the response's `cursor` back to get the next page. When the response's cursor is `null` the feed is exhausted.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search terms (1-500 chars) |
| `cursor` | string | -- | Opaque cursor from a previous response |

### Pin (`/pin`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pin` | string | required | Pin URL on any Pinterest domain, a bare numeric pin id, or a `pin.it` share link |

### Profile (`/profile`) and User Boards (`/user/boards`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | required | Username (optionally with a leading `@`) or a profile URL like `https://www.pinterest.com/pinterest/` |
| `cursor` | string | -- | (`user/boards` only) cursor from a previous response |

### Board (`/board`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `board` | string | required | Board URL, a `username/slug` pair, or a numeric board id. With a bare id, board metadata is unavailable and the `board` field is `null` |
| `cursor` | string | -- | Cursor from a previous response |
| `page_size` | integer | `25` | Pins per page, 1-50 |

### URL Stats (`/url-stats`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `urls` | string[] | required | 1-10 absolute http(s) URLs. Matching is exact-string (scheme, trailing slash and query variants count separately); counts can be 0 or stale for some domains |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search, then page with the returned cursor
first = requests.post(f"{BASE}/api/v1/pinterest/search", headers=HEADERS,
    json={"query": "home decor ideas"}).json()
cursor = first["data"]["cursor"]
nxt = requests.post(f"{BASE}/api/v1/pinterest/search", headers=HEADERS,
    json={"query": "home decor ideas", "cursor": cursor}).json()

# 2. One pin in full
pin = requests.post(f"{BASE}/api/v1/pinterest/pin", headers=HEADERS,
    json={"pin": "https://www.pinterest.com/pin/104779128829676115/"}).json()

# 3. A creator's profile and boards
profile = requests.post(f"{BASE}/api/v1/pinterest/profile", headers=HEADERS,
    json={"username": "pinterest"}).json()

# 4. Save counts for two external URLs (1 credit for 1-5 URLs)
stats = requests.post(f"{BASE}/api/v1/pinterest/url-stats", headers=HEADERS,
    json={"urls": ["https://www.nytimes.com", "https://www.allrecipes.com"]}).json()
```

curl:

```bash
curl -s https://api.scavio.dev/api/v1/pinterest/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"minimalist kitchen"}'
```

## Response shape

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. `data` carries the pins/profile/board payload plus `count` and (for the paginated endpoints) `cursor`.

## Guardrails

- `url-stats` is **1 credit for 1-5 URLs, 2 credits for 6-10**; every other endpoint is 1 credit, including an empty result.
- Cursor pagination only: never guess a cursor, always feed back the one the previous response returned; stop when it is `null`.
- A bare numeric board id cannot carry board metadata - the `board` field will be `null`. Pass a board URL or `username/slug` if you need it.
- `url-stats` matching is exact-string; a trailing slash or query difference is a different URL, and counts can be 0 or stale.
- Never fabricate pins, counts, profiles or board data. Only return what the API returned.
- Pin descriptions and profiles are written by real people. Summarise; do not build profiles of individuals.

## Failure handling

- `400` means an invalid or missing parameter. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the pin, user or board could not be resolved.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=pinterest-api).
- `502` / `503` mean the source is temporarily unavailable - wait a few seconds and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
