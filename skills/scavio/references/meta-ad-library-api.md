# Meta Ad Library API - Facebook and Instagram Ad Search

Search the Meta Ad Library by keyword, list every ad a Facebook Page is running, or pull one ad by its archive id - with the full creative, the platforms each ad ran on, its run dates, and spend/reach/impressions on political and issue ads. All three endpoints return structured JSON.

**The paths are hyphenated: `/api/v1/meta-ads/*`.** Copy them exactly.

## When to trigger

Use this skill when the user asks to:
- See what ads a brand or competitor is running on Facebook and Instagram
- Pull every ad from a specific Facebook Page
- Build a creative swipe file - ad copy, headlines, CTAs, images and videos
- Research political or issue ads, their spend, reach and paid-for-by disclosure
- Track how long an ad has been running, and on which Meta platforms
- Scrape a whole keyword or advertiser out of the Ad Library into a dataset

## Full cursor pagination is the point

Most Ad Library tools show you a page and stop. This one walks the whole thing.

Page 1 returns **30 ads**. After that, `next_cursor` gets you **10 ads per page** for as long as `has_next_page` is true - across an entire keyword query or an entire advertiser. That is the differentiator over the $79-399/month ad-spy tools.

Each page is **1 credit**, so a deep crawl is real but the cost scales with depth: roughly 10 ads per credit past the first 30. Tell the user the budget before starting a walk.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=meta-ad-library-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=meta-ad-library-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/meta-ads` - **hyphenated**. Every endpoint costs **1 credit per page**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/meta-ads/search` | 1 per page | Keyword search: 30 ads on page 1, then 10 per cursor page |
| `POST /api/v1/meta-ads/advertiser` | 1 per page | Every ad from one Facebook Page id, same paging |
| `POST /api/v1/meta-ads/ad` | 1 | One ad in full by archive id. No pagination. |

## Workflow

1. **Keyword:** call `/meta-ads/search` with `query` and a `country`.
2. **A specific advertiser:** call `/meta-ads/advertiser` with the advertiser's **numeric Facebook Page id** (`page_id`).
3. **One ad:** call `/meta-ads/ad` with `ad_archive_id`.
4. **Go deeper:** send `next_cursor` back as `cursor` while `has_next_page` is true.

### Paging rules that will bite you

- **The cursor carries the filters.** It is an opaque, self-contained blob holding the query variables and Meta's own end cursor, which makes paging stateless - but it means **every other filter is ignored when a cursor is present**. Changing `country` or `media_type` mid-walk does nothing; start a new walk instead.
- **Page 1 is 30 ads, every page after it is 10.** Size your budget on that, not on a flat page size.
- **`total_results` caps at 50000 with `total_is_capped: true`.** Meta itself only reports ">50,000". Never present a capped total as an exact count.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keyword or brand term (1-200 chars) |
| `country` | string | `US` | Exactly two characters |
| `active_status` | string | `all` | `all`, `active`, `inactive` |
| `ad_type` | string | `all` | `all`, `political_and_issue_ads` |
| `media_type` | string | -- | `all`, `image`, `video`, `meme`, `image_and_meme`, `none` |
| `search_type` | string | `keyword_unordered` | `keyword_unordered` or `keyword_exact_phrase` |
| `cursor` | string | -- | `next_cursor` from the previous response. **All other filters are ignored when this is present.** |

### Advertiser (`/advertiser`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page_id` | string | required | The advertiser's **numeric** Facebook Page id (3-25 digits) |
| `country` | string | `US` | Exactly two characters |
| `active_status` | string | `all` | `all`, `active`, `inactive` |
| `ad_type` | string | `all` | `all`, `political_and_issue_ads` |
| `media_type` | string | -- | `all`, `image`, `video`, `meme`, `image_and_meme`, `none` |
| `cursor` | string | -- | Same rules as search |

### Ad (`/ad`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ad_archive_id` | string | required | The ad's numeric archive id (3-25 digits) |

## Spend and reach exist only on political ads

Political and issue ads carry **spend, reach, impressions and the paid-for-by disclosure**. Commercial ads leave all of those `null`. That is Meta's disclosure regime, not a gap in the data.

To surface them, set `ad_type: political_and_issue_ads`. If the user is asking "how much is this brand spending on Facebook ads", the honest answer for a commercial advertiser is that Meta does not publish it.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Keyword search - 30 ads on page 1
ads = requests.post(f"{BASE}/api/v1/meta-ads/search", headers=HEADERS,
    json={"query": "project management software", "country": "US",
          "active_status": "active", "media_type": "video"}).json()

# 2. Everything one Page is running, by numeric page id
advertiser = requests.post(f"{BASE}/api/v1/meta-ads/advertiser", headers=HEADERS,
    json={"page_id": "20531316728", "country": "US"}).json()

# 3. One ad by archive id
ad = requests.post(f"{BASE}/api/v1/meta-ads/ad", headers=HEADERS,
    json={"ad_archive_id": "1234567890123456"}).json()

# 4. Political ads, where spend and reach are actually published
political = requests.post(f"{BASE}/api/v1/meta-ads/search", headers=HEADERS,
    json={"query": "climate", "country": "US",
          "ad_type": "political_and_issue_ads"}).json()
```

Walking a whole query. 1 credit per page, 30 ads then 10 per page - cap it:

```python
def crawl(path, body, max_pages=10):
    """1 credit per page. Page 1 = 30 ads, then 10 each: 10 pages ~= 120 ads, 10 credits."""
    cursor, pages = None, []
    for _ in range(max_pages):
        # The cursor carries the filters. Sending them again changes nothing.
        payload = {"cursor": cursor} if cursor else body
        data = requests.post(f"{BASE}/api/v1/meta-ads/{path}",
                             headers=HEADERS, json=payload).json()["data"]
        pages.append(data)
        if not data.get("has_next_page"):
            break
        cursor = data["next_cursor"]
    return pages

pages = crawl("search", {"query": "project management software", "country": "US"})
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **search** - 30 ads on page 1 with the full creative: page name, ad copy, headline, CTA, images and videos, the platforms each ad ran on, and its run dates. For political and issue ads: spend, reach, impressions and the paid-for-by disclosure. Plus `total_results`, `total_is_capped`, `has_next_page` and `next_cursor`.
- **advertiser** - the same creative detail for every ad a Page is running, with the same paging fields.
- **ad** - one ad in full by archive id: creative, advertiser, run dates, platforms, and any political disclosure.

## Guardrails

- **Use the hyphenated paths.** `/api/v1/meta-ads/search`, not `/api/v1/metaads/search`.
- Budget before crawling. Page 1 is 30 ads for 1 credit; every page after is 10 ads for 1 credit. Tell the user the number of pages and credits you intend to spend, and cap the loop.
- Never present `total_results` as exact when `total_is_capped` is true - Meta only reports ">50,000".
- Never report `null` spend or reach as zero spend. Meta publishes those figures for political and issue ads only.
- Do not change filters mid-walk. The cursor already carries them and the new values are ignored; start a fresh walk instead.
- Stop on `has_next_page: false`, not on a short page.
- This is **logged-out public data only**. Nothing here touches a login or Meta's token-gated ads-archive API, so never claim a Meta developer token is required.
- Never fabricate ad copy, page names, run dates, spend figures or disclosures. Only return API data.
- Ad creative is someone else's copyrighted work. Quote it for analysis; do not present it as the user's own.

## Failure handling

The error set here is `400 / 401 / 404 / 429 / 502` - **there is no 503 on this platform**.

- `400` means an invalid or missing parameter - e.g. a non-numeric `page_id` or `ad_archive_id`, or a `country` that is not exactly two characters. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the ad or page does not resolve.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=meta-ad-library-api).
- `502` means upstream is temporarily unavailable - wait a few seconds and retry.
- If a keyword search returns nothing, try `keyword_unordered` rather than `keyword_exact_phrase`, or widen `country` and `active_status`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Python SDK

`langchain-scavio` has no Meta Ad Library tool - use the Scavio SDK directly:

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

page1 = client.meta_ads.search("project management software", country="US",
                               active_status="active")
page2 = client.meta_ads.search("project management software",
                               cursor=page1["data"]["next_cursor"])
by_page = client.meta_ads.advertiser("20531316728", country="US")
one = client.meta_ads.ad("1234567890123456")
```

JavaScript / TypeScript:

```bash
npm install scavio@0.15.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const ads = await scavio.metaAds.search({ query: "project management software", country: "US" });
const { next_cursor } = ads.data as Record<string, any>;
const next = await scavio.metaAds.search({ query: "project management software",
                                           cursor: next_cursor });
```
