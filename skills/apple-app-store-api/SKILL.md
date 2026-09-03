---
name: apple-app-store-api
description: "Apple App Store API: search apps by keyword or publisher name, read a full listing by App Store id or bundle id with price, ratings, version, release notes and screenshots, and page user reviews with rating, text, author and app version. 3 endpoints, 1 credit each, any Apple storefront."
version: 1.0.0
tags: app-store, apple-app-store, app-store-api, ios-apps, aso, app-reviews, app-metadata, bundle-id, apple, mobile-apps, competitor-research, agents, langchain, crewai, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F4F1"
    homepage: https://scavio.dev/docs/app-store-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=apple-app-store-api
---

# Apple App Store API - App Search, Listing Detail, Reviews

Search the App Store, pull a full app listing by App Store id or bundle id, and read user reviews with the app version each was written against. All three endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find iOS, iPadOS or macOS apps matching a keyword, category term, or publisher name
- Pull a single app's full listing: price, ratings, version, release notes, screenshots, size, minimum OS
- Read App Store reviews for an app, in one storefront or across several countries
- Compare an app against competitors, or audit a publisher's whole catalogue
- Do App Store Optimization research (title, description, genres, ratings by country)
- Build a bulk app-metadata dataset

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=apple-app-store-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=apple-app-store-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/appstore`. Every endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/appstore/search` | 1 | Up to 200 fully-shaped apps, the same row as `/app`. No pagination. |
| `POST /api/v1/appstore/app` | 1 | One app's complete listing, by App Store id or bundle id |
| `POST /api/v1/appstore/reviews` | 1 | A page of reviews: rating, title, text, author, app version |

This runs on Apple's own iTunes JSON API, so the data is first-party and cheap.

## Workflow

1. **Find an app:** call `/appstore/search` with `term`. Apple matches an app name, a keyword **or a publisher name**, so searching a developer returns their catalogue.
2. **A search is already a bulk metadata fetch.** Every search row is the same complete row `/app` returns, up to 200 at a time. If you searched for it, you do not need to call `/app` for it as well.
3. **Read one app:** call `/appstore/app` with `app_id`. It takes either a numeric App Store id or a bundle id (`notion.id`, `com.burbn.instagram`) and auto-detects which; the payload is identical either way.
4. **Read reviews:** call `/appstore/reviews` with a **numeric** `app_id` and a `page` from 1 to 10.

### Pagination

**Search does not paginate.** `limit` (1-200, default 25) is the only lever on result volume, and every offset spelling is silently ignored. To get more results, raise `limit` - there is no second page.

**Reviews paginate by `page`, 50 per page, and hard-stop at page 10.** 500 reviews per storefront is Apple's anonymous ceiling. To reach further, ask a different `country` - each storefront has its own review pool.

`/app` returns a single object and takes no paging parameter.

### The `country` parameter is not cosmetic

`country` picks the storefront, and the storefront decides the price, the currency, the localised title and description, and whether the app is sold there at all. It must be a **two-letter** code: the transport falls back to `us` for anything else, so `"usa"` silently buys a US result set that looks correct.

On `/search`, `lang` is independent of `country`: the storefront sets the prices, `lang` sets the words.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `term` | string | required | What to search for (1-500 chars). Matches app name, keyword, or publisher name. |
| `limit` | integer | `25` | 1-200. The only lever on result volume - there is no pagination. |
| `country` | string | `us` | Two-letter storefront code. Anything not two letters silently falls back to `us`. |
| `entity` | string | `software` | `software` (iPhone), `ipad_software`, `mac_software` |
| `lang` | string | -- | Five-letter locale, e.g. `en_us`. Independent of `country`. |

### App (`/app`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `app_id` | string | required | App Store id **or** bundle id (1-255 chars, `^[A-Za-z0-9][A-Za-z0-9._-]*$`). A pasted `apps.apple.com` URL is rejected with a free `400` - extract the id first. |
| `country` | string | `us` | Two-letter storefront code |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `app_id` | string | required | **Numeric App Store id only.** The reviews RSS feed has no bundle-id form. |
| `country` | string | `us` | Two-letter storefront code. Each storefront has its own review pool. |
| `page` | integer | `1` | 1-10, 50 reviews each. Apple hard-stops at page 10. |
| `sort` | string | `most_recent` | `most_recent` or `most_helpful` |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search - one call, up to 200 complete app rows. No pagination: raise limit.
apps = requests.post(f"{BASE}/api/v1/appstore/search", headers=HEADERS,
    json={"term": "habit tracker", "limit": 200, "country": "us"}).json()

# 2. A publisher's catalogue - the same search endpoint, a developer name as the term
catalogue = requests.post(f"{BASE}/api/v1/appstore/search", headers=HEADERS,
    json={"term": "Notion Labs", "limit": 50}).json()

# 3. One app, by numeric id or by bundle id - identical payload
app = requests.post(f"{BASE}/api/v1/appstore/app", headers=HEADERS,
    json={"app_id": "1232780281"}).json()

same_app = requests.post(f"{BASE}/api/v1/appstore/app", headers=HEADERS,
    json={"app_id": "notion.id"}).json()

# 4. Reviews - numeric id only, page 1-10, 50 per page
reviews = requests.post(f"{BASE}/api/v1/appstore/reviews", headers=HEADERS,
    json={"app_id": "1232780281", "page": 1, "sort": "most_helpful"}).json()
```

Reviews stop at 500 per storefront. To go wider, ask another country rather than another page:

```python
def reviews_across_storefronts(app_id, countries=("us", "gb", "de"), pages=10):
    """1 credit per call. 10 pages x 3 countries = 30 credits, so cap it."""
    out = []
    for country in countries:
        for page in range(1, pages + 1):          # page 10 is Apple's hard stop
            data = requests.post(f"{BASE}/api/v1/appstore/reviews", headers=HEADERS,
                                 json={"app_id": app_id, "country": country,
                                       "page": page, "sort": "most_recent"}).json()["data"]
            if not data:
                break                              # empty feed, stop this storefront
            out.append({"country": country, "page": page, "data": data})
    return out
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **search** - up to 200 app rows, each the same complete row `/app` returns.
- **app** - title, description, developer and seller identity, price and currency, all-time and current-version ratings, version and release notes, genres, content rating and advisories, icons at three sizes, screenshots, download size, minimum OS, languages, supported devices, Game Center and VPP flags.
- **reviews** - star rating, title, full review text, author, and the **app version** the review was written against.

Two shapes to code for:

- **Mac rows are thinner.** An app fetched with `entity: mac_software` carries no iPad or Apple TV screenshots, no advisories, no features, no supported-device list and no Game Center flag. These come back **empty rather than absent**, so a Mac app is not a broken response.
- **The reviews feed types its entries by cardinality.** Apple's RSS returns an array at two or more reviews, a bare object at exactly one, and nothing at all at zero. Any parser must handle all three; assuming an array will crash on a one-review app.

## Guardrails

- Every call is 1 credit. Search returns up to 200 complete rows for that one credit, so **prefer one large search over a loop of `/app` calls**.
- Never say "page 2 of the search" - there is no pagination on search. Raise `limit`.
- Never promise more than 500 reviews per storefront. Page 10 is Apple's ceiling; more coverage means more countries, not more pages.
- Under `sort: most_recent` the vote fields come back as **zeroes** - those reviews are simply too new to have been voted on. Do not report that as "no one found these helpful". Use `most_helpful` if you need vote data.
- `country` changes the price, the currency, the localised text and the availability. If the user cares about price, name the storefront you queried in your answer.
- Never fabricate app names, ids, bundle ids, prices, ratings or review text. Only return API data.

## Failure handling

- `400` means an invalid or missing parameter - including a pasted `apps.apple.com` URL in `app_id`. Not billed. Extract the numeric id or bundle id and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` on `/app` means Apple could not resolve that id. **This one is billed** - Apple answers with a 200 carrying an empty result list and charges for it. Verify the id before looping over a list of them.
- **`/reviews` cannot 404.** An unknown id and a real app with zero reviews return the same empty feed, so an empty result never proves the app does not exist. Confirm the app with `/app` first.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=apple-app-store-api).
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Python SDK

`langchain-scavio` has no App Store tool - use the Scavio SDK directly (it handles the auth header):

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

apps = client.app_store.search("habit tracker", limit=200, country="us")
app = client.app_store.app("notion.id")
reviews = client.app_store.reviews("1232780281", page=1, sort="most_helpful")
```

JavaScript / TypeScript:

```bash
npm install scavio@0.15.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const apps = await scavio.appStore.search({ term: "habit tracker", limit: 200 });
const reviews = await scavio.appStore.reviews({ app_id: "1232780281", page: 1 });
```
