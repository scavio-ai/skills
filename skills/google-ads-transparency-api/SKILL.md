---
name: google-ads-transparency-api
description: "Google Ads Transparency Center data as JSON: resolve a brand or domain to a verified advertiser id, pull every ad it runs across Search, YouTube, Shopping, Maps and Play with first-seen and last-seen dates, then open one creative with its region and impression history. 3 endpoints, 1 credit each."
version: 1.0.0
tags: google-ads-transparency, google-ads, ads-transparency-center, ad-library, competitor-ads, ad-creatives, advertiser-lookup, youtube-ads, ppc-research, paid-search, political-ads, ad-intelligence, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F4E2"
    homepage: https://scavio.dev/docs/google-ads-advertisers?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-ads-transparency-api
---

# Google Ads Transparency API - Advertiser Lookup, Live Ad Creatives

Resolve a brand name or domain to a verified Google advertiser id, pull every ad that advertiser is running across Search, YouTube, Shopping, Maps and Play, and open any single creative for its full per-region history. All three endpoints return structured JSON from Google's Ads Transparency Center.

## When to trigger

Use this skill when the user asks to:
- See what ads a competitor is running on Google, YouTube or Shopping right now
- Find a brand's verified Google advertiser id
- Pull ad creatives with their first-seen and last-seen dates and how long they actually ran
- Break one creative down by region, surface and impression bucket
- Research political or issue ads and their funder disclosures
- Build ad-intelligence, creative-swipe or competitor-monitoring pipelines

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-ads-transparency-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=google-ads-transparency-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/googleads`. Every endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/googleads/advertisers` | 1 | **Start here.** Brand or domain to advertiser id. No pagination. |
| `POST /api/v1/googleads/search` | 1 | Every ad for one advertiser, 100 per cursor page |
| `POST /api/v1/googleads/creative` | 1 | One creative in full, with its region and impression history |

## Workflow

**Look up first.** `/search` and `/creative` are keyed by `advertiser_id`.

1. **Resolve:** call `/googleads/advertisers` with a brand name or a domain. A name query returns two kinds of row - `advertiser` rows with the id, verified name, verification country and total ad count, and `domain` rows carrying a website. A domain-shaped query returns domains only. A full URL is fine - Google reduces it to the registrable host itself. **Pass `region` for any non-US advertiser:** this endpoint defaults to the United States, so a brand that runs no US ads returns an empty list, which reads like "not found" rather than "wrong country".
2. **Pull the ads:** call `/googleads/search` with `advertiser_id` **or** `domain`, plus filters.
3. **Open one creative:** call `/googleads/creative` with the `advertiser_id` **and** `creative_id` **pair**.

### Query by domain when you need the domain back

`domain` is dropped entirely from every row when the query is by `advertiser_id`. Querying by `domain` is the **only** way to get that field back on each row. Choose the query shape based on what you need in the output.

### Pagination

- **`/search` paginates by cursor**: send `cursor` and read `next_cursor` back, 100 rows per page. **Re-send the same filters** alongside the cursor. `next_cursor` is `null` once the set is exhausted.
- **`limit` is capped at 100, and that is a hard upstream ceiling, not our policy.** Google answers a request for more than 100 with **zero rows** rather than an error, so an over-large limit looks like "this advertiser has no ads".
- **`/advertisers` does not paginate** - it is an autocomplete, roughly 20 rows per arm.
- **`/creative` does not paginate.**

## Parameters

### Advertisers (`/advertisers`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Brand name or domain (1-200 chars) |
| `region` | string | `US` | ISO alpha-2 (`US`, `GB`, `DE`) or a Google geo criteria id as a string (2-12 chars). **Defaults to the United States, not worldwide** - the lookup runs against one country index at a time, so an advertiser who runs no US ads comes back as an empty list rather than an error. Set it to a country the advertiser actually advertises in. |
| `limit` | integer | `10` | 1-20, **per arm** - advertisers and domains are capped separately, so a name query can return up to twice this many rows |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `domain` | string | one of | Bare host, www host or full URL (1-253 chars), reduced to the registrable host. The only way to get `domain` back on each row. |
| `advertiser_id` | string | one of | e.g. `AR16735076323512287233` (3-40 chars). The shape is checked before any request, so a typo costs nothing. |
| `region` | string | -- | ISO alpha-2 or a Google geo criteria id. Default: no region filter (worldwide). |
| `format` | string | -- | `text`, `image`, `video`. Default: all formats. |
| `platform` | string | -- | `play`, `maps`, `search`, `shopping`, `youtube`. Default: all surfaces. |
| `topic` | string | `all` | `all` or `political` |
| `limit` | integer | `40` | 1-100. **100 is a hard upstream ceiling** - larger returns zero rows. |
| `cursor` | string | -- | `next_cursor` from the previous response. Re-send the same filters with it. |

`domain` or `advertiser_id` is required.

**The three format sets are disjoint.** An advertiser's text, image and video ads share no creatives, so a `format` filter partitions the library rather than ranking within it. To see everything, omit `format`.

**`region` scopes the deep links on every row**, and the same advertiser can share **zero** creatives between two countries. A region-filtered empty result does not mean the advertiser is inactive.

### Creative (`/creative`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `advertiser_id` | string | required | 3-40 chars |
| `creative_id` | string | required | 3-40 chars. Must belong to the `advertiser_id` sent with it - the lookup is keyed by the **pair**, and a mismatched pair is a `404`. |

## Impressions and reach are EEA-only

`impressions_min`, `impressions_max` and `first_shown` come back **`null` outside the EEA**. Google is compelled to publish reach data by EU law and publishes it **only where law requires**, so a US creative simply has no impression figures. This is not a bug, not a parsing gap, and not something a retry will fix.

If the user wants reach numbers, query an EEA region. If they are looking at a US advertiser, tell them the data does not exist rather than reporting zero.

## Everything Google publishes as a range

Google never publishes an exact ad count. The advertiser's headline total arrives as `total_ads_min` / `total_ads_max`, and impression buckets on `/creative` behave the same way - a row can carry a lower bound, an upper bound, or **one of the two alone**. Report ranges as ranges; never present a bound as a precise figure.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Resolve the brand to a verified advertiser id - always start here
who = requests.post(f"{BASE}/api/v1/googleads/advertisers", headers=HEADERS,
    json={"query": "Notion", "region": "DE", "limit": 20}).json()

# 2. Every ad they run in Germany. EEA region, so impressions are populated.
ads = requests.post(f"{BASE}/api/v1/googleads/search", headers=HEADERS,
    json={"advertiser_id": "AR16735076323512287233", "region": "DE",
          "platform": "youtube", "limit": 100}).json()

# 2b. Query by domain instead when you need `domain` back on each row
by_domain = requests.post(f"{BASE}/api/v1/googleads/search", headers=HEADERS,
    json={"domain": "notion.so", "region": "DE", "limit": 100}).json()

# 3. One creative in full - the advertiser_id + creative_id PAIR
creative = requests.post(f"{BASE}/api/v1/googleads/creative", headers=HEADERS,
    json={"advertiser_id": "AR16735076323512287233", "creative_id": "CR1234567890"}).json()
```

Cursor paging. Re-send the same filters every time, and cap the walk:

```python
def all_ads(body, max_pages=5):
    """1 credit per page, 100 rows per page. Same filters on every call."""
    cursor, pages = None, []
    for _ in range(max_pages):
        payload = {**body, **({"cursor": cursor} if cursor else {})}
        data = requests.post(f"{BASE}/api/v1/googleads/search",
                             headers=HEADERS, json=payload).json()["data"]
        pages.append(data)
        cursor = data.get("next_cursor")
        if not cursor:
            break
    return pages

pages = all_ads({"advertiser_id": "AR16735076323512287233", "region": "DE", "limit": 100})
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **advertisers** - two row kinds in one list. `advertiser` rows carry the id, verified name, verification country and total ad count **as a range**; `domain` rows carry a website.
- **search** - the creative (archived image, rich-media bundle, Google's renderer link, dimensions), advertiser id and name, format, first and last seen dates, how many days it actually ran, plus `total_ads_min` / `total_ads_max` and `next_cursor`. `domain` appears on each row **only** when the query was by domain.
- **creative** - every size variation of the asset, the impression bucket, the per-region breakdown with first and last shown dates and a per-surface impression split inside each region, the format, Google's category label, and the funder disclosure on political ads. This is the **only** endpoint carrying a creative's history.

## Guardrails

- Every call is 1 credit, including a 100-row page. Budget the walk before starting it.
- Never send `limit` above 100. Google returns **zero rows** for an over-large request, which reads as "no ads" and is the single easiest way to report a false negative here.
- Never report `null` impressions as zero impressions. Outside the EEA the figure is not published at all - say so.
- Never convert `total_ads_min` / `total_ads_max` into a single number. Google publishes a range on purpose.
- A `format` filter partitions a disjoint set. Do not describe a video-only pull as "all their ads".
- A region-filtered empty result means nothing about the advertiser globally - the same advertiser can share zero creatives between two countries.
- `/creative` is keyed by the advertiser + creative pair. Do not carry a creative id across advertisers.
- Never fabricate advertiser ids, creative ids, run dates, impression figures or funder names. Only return API data.
- This is public transparency data. When summarising political ads, quote the disclosure rather than characterising the funder.

## Failure handling

- `400` means an invalid or missing parameter - e.g. neither `domain` nor `advertiser_id`. The advertiser id shape is validated before any upstream request, so a typo there costs nothing. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` on `/creative` usually means the `advertiser_id` and `creative_id` do not belong together. Re-pull the creative id from `/search` for that advertiser.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-ads-transparency-api).
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry.
- Zero rows from `/search` with a large `limit` is almost always the 100 ceiling, not an empty advertiser. Drop `limit` to 100 and retry before concluding anything.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Python SDK

`langchain-scavio` has no Google Ads Transparency tool - use the Scavio SDK directly:

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

who = client.google_ads.advertisers("Notion", region="DE", limit=20)
page1 = client.google_ads.search(advertiser_id="AR16735076323512287233",
                                 region="DE", limit=100)
page2 = client.google_ads.search(advertiser_id="AR16735076323512287233",
                                 region="DE", limit=100,
                                 cursor=page1["data"]["next_cursor"])
creative = client.google_ads.creative("AR16735076323512287233", "CR1234567890")
```

JavaScript / TypeScript:

```bash
npm install scavio@0.15.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const ads = await scavio.googleAds.search({ domain: "notion.so", region: "DE", limit: 100 });
```
