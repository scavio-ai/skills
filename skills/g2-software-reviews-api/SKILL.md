---
name: g2-software-reviews-api
description: "G2 software reviews API for B2B SaaS research: search products with star rating, review count and vendor, read a full profile with pricing editions, features, integrations and alternatives (no review text), and pull reviews with exact per-star counts and company-size, role, industry and region facets. 3 endpoints, 5 credits each."
version: 1.0.0
tags: g2, g2-crowd, software-reviews, b2b-software, saas, competitive-intelligence, review-mining, voice-of-customer, product-research, pricing-research, vendor-comparison, alternatives, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U00002B50"
    homepage: https://scavio.dev/docs/g2-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=g2-software-reviews-api
---

# G2 Software Reviews API - Product Search, Ratings, Reviews

Search G2, the B2B software review site, open any product's full profile with its pricing editions, features and alternatives, and pull reviews with exact per-star counts and company-size / role / industry / region facets. All three endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find B2B software products in a category on G2
- Read a software product's G2 profile: rating histogram, pricing editions, features, integrations, alternatives
- Mine G2 reviews for what enterprise buyers, admins or a specific region actually say
- Compare a product against its listed alternatives and head-to-head comparisons
- Do competitive intelligence, win/loss research, or voice-of-customer analysis on SaaS

## Cost: 5 credits per call

**G2 is 5 credits per request - the most expensive platform on Scavio, and the only one at this tier.** g2.com bills a premium upstream on every single fetch, with no cheap mode available. Three calls is 15 credits.

Plan the run before making it, tell the user the credit cost up front, and never loop over search results calling `/product` on each one.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=g2-software-reviews-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=g2-software-reviews-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/g2`. Every endpoint costs **5 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/g2/search` | 5 | Ranked software products, each row carrying `product_id` and `slug` |
| `POST /api/v1/g2/product` | 5 | The full profile - **but no review text** |
| `POST /api/v1/g2/reviews` | 5 | Reviews plus exact per-star counts and faceted counts |

## Workflow

1. **Find the product:** call `/g2/search` with `query`. Every row carries `product_id` and `slug`.
2. **Profile:** call `/g2/product` with `product_id` (a slug like `notion`, or the numeric G2 id like `82623` as a **string** - both resolve).
3. **Reviews:** call `/g2/reviews` with the same `product_id`.

**`/product` carries no reviews at all.** G2 loads review bodies in a separate frame, so the profile page simply does not contain them. If the user wants what customers said, you must call `/reviews` - there is no way to get it out of `/product`.

Conversely, `/reviews` carries things the profile has no form of: **exact per-star counts**, pros and cons with per-theme counts, and company-size / role / industry / region / category **facets with counts**. For a "how do enterprise buyers rate this" question, `/reviews` is the right call, not `/product`.

Every reference endpoint also accepts a full `g2.com` URL as `url` instead of an id.

### Pagination

- **`/search`** - `page` (1-based) with `limit` (1-100, default 20). The 100 ceiling is ours, to keep a single request inside the request deadline; G2 itself keeps paginating at any size.
- **`/reviews`** - `page`, **fixed at 10 per page**, and it paginates well past the 10 pages G2's own widget links to.
- **`/product`** does not paginate.

At 5 credits a page, a 10-page review pull is 50 credits. Say so before starting.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Search term (1-200 chars) |
| `url` | string | one of | Full `g2.com/search` URL (1-1000 chars); the host is checked |
| `page` | integer | -- | 1-based; page size follows `limit` |
| `limit` | integer | `20` | 1-100 |
| `sort` | string | `relevance` | `relevance`, `popular`, `alphabetical`, `rating` |
| `rating` | integer | -- | `1`-`5`. Products **at or above** this star rating. |

`query` or `url` is required.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | Slug (`notion`) or numeric G2 id as a string (`82623`) - both resolve (1-200 chars) |
| `url` | string | one of | Full g2.com product URL |

`product_id` or `url` is required.

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | Slug or numeric id as a string |
| `url` | string | one of | Full g2.com reviews URL |
| `page` | integer | -- | 10 reviews per page, fixed |
| `sort` | string | `relevance` | `relevance`, `newest`, `most_helpful`, `rating_high`, `rating_low` |
| `rating` | integer | -- | `1`-`5`, **half-star-inclusive**: `1` returns 0, 0.5 and 1-star reviews |
| `company_size` | string | -- | `small_business` (<=50), `mid_market` (51-1000), `enterprise` (>1000) |
| `role` | string | -- | `user`, `administrator`, `executive_sponsor`, `internal_consultant`, `consultant`, `agency`, `industry_analyst` |
| `region` | string | -- | `north_america`, `europe`, `asia`, `latin_america`, `anz`, `middle_east`, `africa` |
| `query` | string | -- | Full-text search **within** the reviews. Narrows the list **and every facet count**. |

`product_id` or `url` is required.

### Why every filter is a closed enum

Two upstream behaviours make free-text filters dangerous here, and both fail silently:

- **An unknown sort is silently accepted.** `order=zzznotasort` answers `200` with a full result set in some unstated ordering. The sort never ran and nothing in the response says so.
- **An unknown filter value matches nothing.** A bogus company-segment value returns "Reviews (0)", which reads exactly like "this product has no enterprise reviews".

So the enums above are the complete set. Do not pass a value outside them, and do not report a zero-result filtered call as a finding without re-checking it unfiltered.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Find products - 5 credits
found = requests.post(f"{BASE}/api/v1/g2/search", headers=HEADERS,
    json={"query": "project management", "limit": 100, "sort": "rating", "rating": 4}).json()

# 2. Full profile - 5 credits. Slug or numeric id, both as strings.
profile = requests.post(f"{BASE}/api/v1/g2/product", headers=HEADERS,
    json={"product_id": "notion"}).json()

# NOTE: profile contains NO review text. For that you must call /reviews.

# 3. What enterprise admins say - 5 credits, 10 reviews, plus every facet count
reviews = requests.post(f"{BASE}/api/v1/g2/reviews", headers=HEADERS,
    json={"product_id": "notion", "company_size": "enterprise",
          "role": "administrator", "sort": "newest", "page": 1}).json()

# 4. Search the review text itself - narrows the list AND the facet counts
mentions = requests.post(f"{BASE}/api/v1/g2/reviews", headers=HEADERS,
    json={"product_id": "notion", "query": "migration", "page": 1}).json()
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **search** - star rating, review count, vendor, categories, seller description and logo, with `product_id` and `slug` on every row. `total_results` is G2's Products-tab headline and **caps at 10000**; `total_by_type` splits the query across products, sellers, categories and discussions.
- **product** - rating and per-star histogram, review count, vendor, description and seller website, pricing editions with parsed amounts, feature groups, categories and breadcrumbs, supported languages, integrations, alternatives, head-to-head comparisons, media, community discussions, and G2's AI-derived pros and cons. **No review text.**
- **reviews** - rating, title, likes and dislikes, problems solved, reviewer job title, industry and company size, validated and incentivized flags - plus exact per-star counts, pros and cons with per-theme counts, and company-size / role / industry / region / category facets with counts.

## Guardrails

- **State the cost.** Every call is 5 credits. Before a multi-page pull, tell the user the total you intend to spend.
- Never loop `/product` over search results. Search already returns rating, review count, vendor and categories for every row.
- Never say "the profile has no reviews so this product has none". `/product` structurally cannot carry review text - call `/reviews` before drawing any conclusion about customer sentiment.
- `total_results` caps at 10000. Do not present it as an exact count of matching products.
- `rating` on `/reviews` is half-star-inclusive: `rating: 1` includes 0 and 0.5-star reviews. Do not describe it as "exactly one star".
- Zero results from a filtered `/reviews` call is ambiguous - it may mean the filter matched nothing rather than the segment having no opinion. Re-check unfiltered before reporting it.
- Never fabricate product names, ratings, review counts, pricing or review text. Only return API data.

## Failure handling

- `400` means an invalid or missing parameter - e.g. neither `query`/`product_id` nor `url`, or a value outside a closed enum. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the product does not resolve. Re-check the slug or id via `/search`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=g2-software-reviews-api).
- `502` means G2 served a bot wall or a hollow shell. **This one is billed** - the upstream charged full price for a page that could not be used, and it arrives as a real HTTP 200 upstream before we classify it. Retries are deliberately conservative for exactly this reason: back off for several seconds and retry **at most once or twice**, then report the failure instead of burning credits.
- `503` means upstream is temporarily unavailable - wait a few seconds and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Python SDK

`langchain-scavio` has no G2 tool - use the Scavio SDK directly:

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.g2.search(query="project management", limit=100, sort="rating", rating=4)
profile = client.g2.product(product_id="notion")          # no review text here
reviews = client.g2.reviews(product_id="notion", company_size="enterprise",
                            role="administrator", sort="newest", page=1)
```

JavaScript / TypeScript:

```bash
npm install scavio@0.15.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const reviews = await scavio.g2.reviews({ product_id: "notion", company_size: "enterprise" });
```
