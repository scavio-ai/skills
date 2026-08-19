---
name: capterra-reviews-api
description: "Capterra reviews API: search B2B software for 20 ranked products, read a full profile with the complete pricing table, rated features, integrations and the 25 most recent reviews included, then page deeper reviews with five per-criterion scores each. 3 endpoints, 2 credits each, no search pagination."
version: 1.0.0
tags: capterra, capterra-reviews, software-reviews, b2b-software, saas, software-pricing, vendor-comparison, review-mining, competitive-intelligence, buyer-research, agents, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F9ED"
    homepage: https://scavio.dev/docs/capterra-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=capterra-reviews-api
---

# Capterra Reviews API - Software Search, Pricing, Reviews

Search Capterra for B2B software, open a product's full profile - complete pricing table, every rated feature and integration, AI-derived pros and cons, and the 25 most recent reviews riding along - and page deeper into reviews with five per-criterion scores each. All three endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find B2B software products in a category on Capterra
- Read a product's Capterra profile: pricing plans, rated features, integrations, buyer profile
- Mine Capterra reviews for pros, cons, advice, and what buyers switched from
- See which alternatives a product's reviewers also considered, with their ratings and starting prices
- Do software-selection research, competitive intelligence, or voice-of-customer analysis

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=capterra-reviews-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/capterra`. Every endpoint costs **2 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/capterra/search` | 2 | 20 ranked products, each row carrying `product_id` and `slug`. No pagination. |
| `POST /api/v1/capterra/product` | 2 | The full profile **plus the 25 most recent reviews** |
| `POST /api/v1/capterra/reviews` | 2 | Deeper review pages, 25 per page |

## Workflow

1. **Find the product:** call `/capterra/search` with `query`. You get 20 rows, each carrying `product_id` and `slug`.
2. **Profile:** call `/capterra/product` with `product_id` - the number in `/p/186596/Notion/`, **as a string** (a JSON number is rejected).
3. **Only then go deeper.** The profile already contains the 25 most recent reviews at no extra cost. Call `/capterra/reviews` only to page **past** them.

Every endpoint also accepts a full `capterra.com` URL as `url` instead of an id or query. The host check covers the international domains too, including `capterra.co.uk` and `capterra.com.br`.

### Pagination

**Search does not paginate.** Capterra fixes the result set at 20 and `?page=2` returns identical rows, so there is deliberately **no `page` parameter** on `/search`. Do not add one, and never claim a second page exists - refine the query instead.

**Reviews page with `page`, 25 per page, capped at page 100.** Past page 100 Capterra answers `200` with **page one** and quietly drops the page from the canonical URL, so an over-run looks like a successful call returning duplicate data rather than an error. Stay inside the cap.

**`/product` does not paginate.**

### `slug` is cosmetic on one endpoint and load-bearing on another

- On **`/product`**, `slug` is cosmetic. `/p/186596/Zzzjunk/` returns Notion's profile byte for byte.
- On **`/reviews`**, `slug` is load-bearing. It is case-sensitive upstream, and a wrong one **silently serves page one** under a billed `200`.

So never hand-write a slug for a review call. Pass back the `slug` or the `reviews_url` that `/search` or `/product` gave you.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Search term (1-200 chars) |
| `url` | string | one of | Full `capterra.com` search URL (1-1000 chars); the host is checked and covers `capterra.co.uk`, `capterra.com.br` |

`query` or `url` is required. A term-less search serves a fixed popular-products list that has nothing to do with the caller, which is why the query is mandatory.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | The number in `/p/186596/Notion/` (1-50 chars). **String only** - a JSON number is rejected. |
| `slug` | string | one of | Cosmetic here (1-200 chars) |
| `url` | string | one of | Full capterra.com product URL |

`product_id` or `url` is required.

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | String only |
| `slug` | string | -- | **Load-bearing here**: case-sensitive, and a wrong one silently serves page one |
| `url` | string | one of | Passing back `reviews_url` from `/product` is the reliable way to page |
| `page` | integer | -- | 1-100, 25 reviews per page |

`product_id` or `url` is required.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search - 20 products, no pagination. Refine the query for different results.
found = requests.post(f"{BASE}/api/v1/capterra/search", headers=HEADERS,
    json={"query": "project management software"}).json()

# 2. Full profile. product_id is a STRING; the 25 most recent reviews ride along free.
profile = requests.post(f"{BASE}/api/v1/capterra/product", headers=HEADERS,
    json={"product_id": "186596"}).json()

# 3. Page PAST those 25. Pass back reviews_url (or the exact slug) - never a hand-typed slug.
more = requests.post(f"{BASE}/api/v1/capterra/reviews", headers=HEADERS,
    json={"url": profile["data"]["reviews_url"], "page": 2}).json()
```

Reviews cap at page 100, and an over-run is a silent repeat of page one rather
than an error:

```python
def review_pages(reviews_url, start=2, pages=5):
    """2 credits per page. Never ask past page 100."""
    out = []
    for page in range(start, min(start + pages, 101)):
        data = requests.post(f"{BASE}/api/v1/capterra/reviews", headers=HEADERS,
                             json={"url": reviews_url, "page": page}).json()["data"]
        if not data:
            break
        out.append(data)
    return out
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **search** - 20 products: name, vendor description, rating, review count, logo and a paid-placement flag, with `product_id` and `slug` on every row.
- **product** - rating with per-star histogram and the four scored criteria, likelihood to recommend, review sentiment and topics, the complete pricing table with every plan and its features, every rated feature, every integration, AI-derived pros and cons each with the quoted review, FAQs, screenshots, badges and awards, competitor comparisons and alternatives, buyer profile by company size / industry / job function, **plus the 25 most recent reviews**.
- **reviews** - overall score plus five per-criterion scores, title, pros, cons, advice, usage duration, incentivized flag, alternatives considered and what the reviewer switched from, reviewer job title / industry / company size, and the vendor response - plus a **richer competitor list than the profile carries**, each alternative with its own rating histogram and starting price.

**`vendor` is `null` on `/product`.** Capterra does not publish it as structured data on the product page - this is verified, not a gap in the parser. The **reviews** name the vendor per review, so that is where to get it.

## Guardrails

- Every call is 2 credits. Search + profile is 4, and each extra review page is another 2.
- **Do not call `/reviews` for page 1.** Those 25 reviews are already inside `/product`, so paying for them again is a wasted call.
- Search returns 20 products and does not paginate. Never offer the user "the next page of results" - narrow the query.
- Never hand-write a `slug` for `/reviews`. It is case-sensitive and a wrong one returns page one under a billed 200, which looks like real data. Use `reviews_url` or the exact `slug` from a prior response.
- Never ask for a review page above 100. Capterra answers with page one and the duplicate rows are easy to mistake for new ones.
- `product_id` must be a string. A JSON number is rejected.
- Report `vendor` as unavailable on the profile rather than guessing it from the product name; take it from a review if the user needs it.
- Never fabricate product names, ratings, prices, plan names or review text. Only return API data.

## Failure handling

- `400` means an invalid or missing parameter - a numeric `product_id`, a missing `query`/`url`, or a page above 100. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the product does not resolve. Re-check the id via `/search`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=capterra-reviews-api).
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry.
- Duplicate review rows across two pages usually mean the slug was wrong or the page number was past 100 - both silently return page one. Re-check the slug and the page rather than retrying blindly.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Python SDK

`langchain-scavio` has no Capterra tool - use the Scavio SDK directly:

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.capterra.search(query="project management software")
profile = client.capterra.product(product_id="186596")     # 25 reviews included
more = client.capterra.reviews(url=profile["data"]["reviews_url"], page=2)
```

JavaScript / TypeScript:

```bash
npm install scavio@0.15.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const profile = await scavio.capterra.product({ product_id: "186596" });
```
