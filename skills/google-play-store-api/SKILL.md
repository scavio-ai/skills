---
name: google-play-store-api
description: "Google Play Store data as structured JSON: search Android apps by keyword, pull a full listing with the real install count, rating histogram, permissions, Data safety table, changelog and 20 reviews, and cursor-page reviews by newest, relevance or rating. 3 endpoints, 2 credits each."
version: 1.0.0
tags: google-play, google-play-api, play-store, android-apps, app-search, install-count, app-reviews, aso, app-store-optimization, data-safety, competitor-research, agents, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F4F2"
    homepage: https://scavio.dev/docs/google-play-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-play-store-api
---

# Google Play Store API - App Search, Install Counts, Reviews

Search Google Play, pull a full Android store listing - including the real install count Play publishes but never renders, the whole permission tree and the Data safety table - and page reviews by cursor. All three endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find Android apps or games matching a keyword
- Pull an app's full Play listing: installs, rating histogram, IAPs, permissions, Data safety, changelog
- Read Google Play reviews for an app, beyond the handful the store page shows
- Compare an Android app against competitors, or check a developer's identity and legal contact
- Do Android ASO research across storefronts and languages
- Track an app's rating distribution or changelog over time

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-play-store-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-play-store-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/googleplay`. Every endpoint costs **2 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/googleplay/search` | 2 | One shelf of ranked apps (~30). No pagination. |
| `POST /api/v1/googleplay/app` | 2 | The complete store listing, plus the 20 server-rendered reviews |
| `POST /api/v1/googleplay/reviews` | 2 | A page of reviews, cursor-paginated |

Google Play is a **premium domain upstream**, which is why it is 2 credits and not 1. Budget accordingly before planning a deep review crawl.

## Workflow

1. **Find an app:** call `/googleplay/search` with `query`. You get one shelf of roughly 30 apps. A branded query also returns Play's hero card as result 1, projected to the same row shape, plus Play's related-query rail.
2. **Read the listing:** call `/googleplay/app` with `app_id` - a package name (`com.notion.id`) or **any** `play.google.com` URL carrying one in its `id` param.
3. **The listing already carries 20 reviews.** Play server-renders them and they ride along at no extra cost. Only call `/googleplay/reviews` when you need to page past those 20 or sort differently.
4. **Page reviews:** call `/googleplay/reviews` with `app_id`, then send `next_cursor` back as `cursor`.

### Pagination

**Search does not paginate.** It is one shelf of about 30 apps. There is no page or cursor parameter - do not invent one. Narrow the query instead.

**`/app` does not paginate.**

**Reviews paginate by cursor, and the cursor is strict.** It is opaque, **single-use**, and it encodes the sort as well as the position. Send it back with the **same `sort`** it came from. A cursor past the last review is a **404**, not an empty page - that is the stop signal.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search term (1-200 chars) |
| `hl` | string | `en` | Interface language (2-20 chars). Changes the storefront, not only the strings. |
| `gl` | string | `us` | Country (2-10 chars) |

### App (`/app`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `app_id` | string | required | Package name, or any `play.google.com` URL carrying one in its `id` param (1-500 chars) |
| `hl` | string | `en` | Interface language |
| `gl` | string | `us` | Country |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `app_id` | string | required | Package name or Play URL (1-500 chars) |
| `sort` | string | `newest` | `relevance`, `newest`, `rating` |
| `count` | integer | `50` | Reviews per page, 1-200. Capped at 200 on our side. |
| `cursor` | string | -- | The previous response's `next_cursor`. Opaque, single-use, sort-encoded. |
| `hl` | string | `en` | Interface language |
| `gl` | string | `us` | Country |

### `hl` moves more than the words

At `hl=pt-BR` the title, the description, the install formatting **and the content rating** all change with it - it selects a storefront, not a translation layer. Play also silently falls back to English/US on any value it does not serve, so an unexpected language in the response means the value was not supported, not that the call failed.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search - one shelf of ~30 apps, no pagination
apps = requests.post(f"{BASE}/api/v1/googleplay/search", headers=HEADERS,
    json={"query": "habit tracker", "hl": "en", "gl": "us"}).json()

# 2. Full listing - package name or any play.google.com URL
app = requests.post(f"{BASE}/api/v1/googleplay/app", headers=HEADERS,
    json={"app_id": "com.spotify.music"}).json()

# The 20 server-rendered reviews are already in there - do not pay again for them.

# 3. Page past them, sorted by rating
reviews = requests.post(f"{BASE}/api/v1/googleplay/reviews", headers=HEADERS,
    json={"app_id": "com.spotify.music", "sort": "rating", "count": 200}).json()
```

Cursor paging, capped so it cannot run away with the user's credits. The cursor
encodes the sort, so the sort must not change between pages, and running past the
end is a `404`:

```python
def paged_reviews(app_id, sort="newest", count=200, max_pages=5):
    """2 credits per page. 5 pages = 10 credits."""
    cursor, pages = None, []
    for _ in range(max_pages):
        body = {"app_id": app_id, "sort": sort, "count": count}
        if cursor:
            body["cursor"] = cursor    # same sort every time: the cursor encodes it
        r = requests.post(f"{BASE}/api/v1/googleplay/reviews", headers=HEADERS, json=body)
        if r.status_code == 404:
            break                      # cursor ran past the last review: this is the end
        data = r.json()["data"]
        pages.append(data)
        cursor = data.get("next_cursor")
        if not cursor:
            break
    return pages
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **search** - ranked apps: package name, title, developer, rating, install count, price and IAP range, content rating, icon, screenshots. A branded query puts the hero card first in the same row shape, and Play's related-query rail comes along.
- **app** - installs (**including the real count Play publishes but never renders on the page**), rating and star histogram, description, developer identity and legal contact, price and IAPs, categories and gameplay tags, screenshots and trailer, version and Android requirement, release and update dates, changelog, the full permission tree, the Data safety table, the 20 server-rendered reviews, and the similar-apps and more-by-developer rails.
- **reviews** - star score, full text, author, thumbs-up count, developer reply, and the **app version** the reviewer was running. Paged via `next_cursor`.

## Guardrails

- Every call is **2 credits**, not 1. Say so before planning a multi-page crawl: a 10-page review pull is 20 credits.
- `/app` already contains 20 reviews. Do not call `/reviews` for the same app unless you need to go deeper or change the sort - that is a second premium call for data you already have.
- Search is one shelf of ~30 apps with **no pagination**. Never tell the user there is a page 2; narrow the query instead.
- Keep `sort` fixed while paging reviews. The cursor carries the sort, and changing it mid-walk invalidates the sequence.
- Do not treat a `404` mid-walk as a failure - a cursor past the last review is how the feed ends.
- Games are folded into the apps vertical and are covered. **Books and films are not** - they use a different card shape entirely.
- Never fabricate package names, install counts, ratings, permissions or review text. Only return API data.

## Failure handling

- `400` means an invalid or missing parameter - fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` on `/reviews` while paging means the cursor ran past the last review. Stop; this is normal.
- A reviews call that answers **200 with an empty payload is a billed 404** - premium price paid to learn the package has no reviews or does not exist. Confirm the package with `/app` before crawling reviews for it.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-play-store-api).
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Python SDK

`langchain-scavio` has no Google Play tool - use the Scavio SDK directly:

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

apps = client.google_play.search("habit tracker", gl="us")
app = client.google_play.app("com.spotify.music")
page1 = client.google_play.reviews("com.spotify.music", sort="rating", count=200)
page2 = client.google_play.reviews("com.spotify.music", sort="rating", count=200,
                                   cursor=page1["data"]["next_cursor"])
```

JavaScript / TypeScript:

```bash
npm install scavio@0.15.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const app = await scavio.googlePlay.app({ app_id: "com.spotify.music" });
```
