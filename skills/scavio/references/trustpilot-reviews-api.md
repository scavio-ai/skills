# Trustpilot Reviews API - Business Search, TrustScore, Reviews, Categories

Search Trustpilot businesses, read a full business profile, page through filtered reviews, browse the category tree and the businesses ranked in a category, and fetch a single review by id. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find businesses on Trustpilot by name, keyword or category in a given country
- Look up a company's TrustScore, star rating, review count or rating distribution by domain or a pasted `trustpilot.com/review/...` URL
- Read Trustpilot reviews for a business, filtered by stars, language, date range, topic, text, verified-only or with-replies
- Measure how many negative reviews a business gets, how often it replies, and how fast
- Monitor a brand's or a competitor's Trustpilot reviews over time, or count reviews in a recent window (review velocity)
- Get the AI review summary and topic breakdown Trustpilot shows for a business
- List the top-rated or most-reviewed businesses in a Trustpilot category, optionally only claimed profiles
- Build a lead list of businesses in a category with their website and published email and phone
- Fetch one Trustpilot review by its id, with the business reply and the business it is about

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 2 credits.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every Trustpilot endpoint costs **2 credits** per call.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/trustpilot/search` | 2 | Businesses matching a keyword in one country, up to 100 per page: name, domain, TrustScore, stars, review count, categories, website, and the email, phone and address the business published |
| `POST /api/v1/trustpilot/business` | 2 | One full profile by domain or Trustpilot URL: rating distribution, review count per language, category path, contact details, claimed and verification status, reply rate and average days to reply on negative reviews, consumer alerts, AI summary and topics, similar businesses, and the 20 newest reviews |
| `POST /api/v1/trustpilot/reviews` | 2 per page | 20 reviews per page, filtered by stars, language, date range, topics, text, verified-only and with-replies, sorted by recency or relevance. Pages 1-10 |
| `POST /api/v1/trustpilot/categories` | 2 | The category tree (22 top-level categories, 189 subcategories), or the categories matching a name |
| `POST /api/v1/trustpilot/category` | 2 per page | Businesses ranked in one category and country, 20 per page, with sort, minimum star rating and claimed-only filters |
| `POST /api/v1/trustpilot/review` | 2 | One review by its 24-character id, with the business reply and the business it is about |

## Workflow

1. **Find the business:** call `/trustpilot/search` with `query` (a name or keyword). Read `businesses[].domain` (e.g. `nordvpn.com`). If the user already gave a domain or a Trustpilot URL, skip this step.
2. **Profile:** call `/trustpilot/business` with `domain` (or `url`). One call returns the TrustScore, the rating distribution, reply behavior, the AI summary and topics, and the 20 newest reviews in `language` (default `en`).
3. **Reviews:** call `/trustpilot/reviews` with the same `domain` plus filters. Topic ids for the `topics` filter come from the profile's `topics[].id` (e.g. `customer_service`).
4. **One review:** call `/trustpilot/review` with a `review_id` from step 2 or 3.

For a category: call `/trustpilot/categories` (with `query` to find one by name, or empty for the tree), take a `category_id` such as `vpn_service`, then call `/trustpilot/category`.

### Pagination

- **Search:** `page` (1-based) and `page_size` (default 20, up to 100). The response carries `total_results` and `total_pages`.
- **Reviews:** `page` 1-10, 20 per page. The response carries `max_page` (how far this filter combination goes), `total_filtered` (every match for the filters) and `total_reviews`. See the 200-review limit under Guardrails.
- **Category:** `page` (1-based), 20 businesses per page. The response carries `total_results` and `total_pages`.
- **Business, categories, review:** no paging.

Every page is 2 credits, so state the budget before looping.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Business name, keyword or category, 1-200 chars (e.g. `vpn`) |
| `country` | string | `US` | 2-letter country code to search in |
| `page` | integer | 1 | Results page, 1-based |
| `page_size` | integer | 20 | Businesses per page, 1-100 |

### Business (`/business`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `domain` | string | one of | The website domain as listed on Trustpilot (e.g. `www.amazon.com`, `nordvpn.com`); search returns it as `domain` |
| `url` | string | one of | A `trustpilot.com/review/<domain>` URL from any Trustpilot country site |
| `language` | string | `en` | 2-letter code. The 20 included reviews are this language's newest, and the AI summary and topics come back in it when Trustpilot has them for that language (null or empty otherwise). The rating distribution and language breakdown always cover every language |

Pass exactly one of `domain` or `url`.

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `domain` / `url` | string | one of | Same as business; pass exactly one |
| `page` | integer | 1 | 1-10, 20 reviews per page |
| `stars` | integer[] | -- | Only these star ratings, 1-5 (e.g. `[1, 2]`) |
| `language` | string | `all` | 2-letter review language code, or `all` |
| `date_range` | string | -- | `last30days`, `last3months`, `last6months`, `last12months` |
| `sort` | string | `recency` | `recency` (newest first) or `relevance` |
| `verified_only` | boolean | -- | Only verified reviews |
| `with_replies` | boolean | -- | Only reviews the business replied to |
| `topics` | string[] | -- | 1-10 topic ids from the business profile's `topics` (e.g. `["customer_service"]`) |
| `search` | string | -- | Only reviews containing this text, 1-100 chars (e.g. `refund`) |

### Categories (`/categories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | -- | Find categories by name (e.g. `insurance`). Omit for the full tree |
| `country` | string | `US` | 2-letter country code for the name lookup |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | required | A `category_id` from `/categories` (e.g. `vpn_service`) |
| `country` | string | `US` | 2-letter country code |
| `sort` | string | `most_relevant` | `most_relevant`, `reviews_count`, `latest_review` |
| `min_trust_score` | number | -- | Minimum star rating: `3`, `4` or `4.5`. Trustpilot rounds TrustScore to stars, so `4` includes TrustScore 3.8 and up |
| `claimed_only` | boolean | -- | Only businesses that claimed their Trustpilot profile |
| `page` | integer | 1 | Results page, 1-based, 20 per page |

### Review (`/review`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `review_id` | string | required | The 24-character `review_id` from a business or reviews response (e.g. `6aca2504b52cc4b518bf4b75`) |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/trustpilot/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "nordvpn.com", "stars": [1, 2], "language": "en"}'
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def trustpilot(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/trustpilot/{endpoint}", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]

# 1. Find businesses by keyword (email/phone only when the business published them)
found = trustpilot("search", {"query": "vpn", "country": "US", "page_size": 10})
for biz in found["businesses"]:
    print(biz["name"], biz["domain"], biz["trust_score"], biz["review_count"], biz["email"])

# 2. One full profile
profile = trustpilot("business", {"domain": "nordvpn.com"})
print(profile["trust_score"], profile["stars"], profile["rating_distribution"])
rb = profile["reply_behavior"]
print(rb["reply_rate"], rb["avg_days_to_reply"], rb["negative_reviews"])
topic_ids = [t["id"] for t in profile["topics"]]        # e.g. "customer_service"

# 3. Negative English reviews, 20 per page, newest first
bad = trustpilot("reviews", {"domain": "nordvpn.com", "stars": [1, 2], "language": "en"})
print(bad["total_filtered"], "matching reviews; this combination goes to page", bad["max_page"])
for review in bad["reviews"]:
    print(review["rating"], review["title"], (review["reply"] or {}).get("text"))

# 4. Ranked businesses in a category, 4 stars and up, claimed profiles only
ranked = trustpilot("category", {"category_id": "vpn_service", "sort": "reviews_count",
                                 "min_trust_score": 4, "claimed_only": True})
for biz in ranked["businesses"]:
    print(biz["name"], biz["trust_score"], biz["stars"], biz["website"])

# 5. One review by id
one = trustpilot("review", {"review_id": "6aca2504b52cc4b518bf4b75"})
print(one["review"]["text"], one["business"]["name"])
```

Review velocity: `total_filtered` counts every match, so the same call with a `date_range` tells you how many reviews arrived in that window without paging.

```python
recent = trustpilot("reviews", {"domain": "nordvpn.com", "date_range": "last30days"})
print(recent["total_filtered"], "reviews in the last 30 days")
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **search** - `query`, `country`, `page`, `page_size`, `total_results`, `total_pages`, `count`, `businesses[]`.
  A row: `business_unit_id`, `name`, `domain`, `profile_url`, `trust_score`, `stars`, `review_count`, `categories[]` {`id`, `name`, `primary`}, `website`, `email`, `phone`, `address` {`street`, `city`, `postcode`, `country_code`, `country`, `lat`, `lng`}, `verified`, `logo_url`.
- **business** - `business_unit_id`, `name`, `domain`, `profile_url`, `language`, `trust_score`, `stars`, `review_count`, `review_count_last_12_months`, `rating_distribution` {`1`..`5`}, `languages[]` {`code`, `review_count`}, `categories[]`, `category_path` {`top`, `mid`, `bottom`}, `website`, `email`, `phone`, `address`, `contact`, `description`, `verified`, `verification` {`identity`, `google`, `payment_method`, `persona`}, `logo_url`, `claimed`, `claimed_at`, `closed`, `temporarily_closed`, `collects_incentivised_reviews`, `reply_behavior` {`reply_rate`, `avg_days_to_reply`, `negative_reviews`, `negative_reviews_replied`, `last_reply_to_negative_at`}, `consumer_alerts[]`, `merged`, `uses_ai_responses`, `ai_summary`, `topics[]` {`id`, `name`, `summary`}, `similar_businesses[]`, `facebook_url`, `reviews_count`, `reviews[]`.
- **reviews** - `business_unit_id`, `name`, `domain`, `profile_url`, `page`, `per_page`, `max_page`, `total_filtered`, `total_pages`, `total_reviews`, `filters` (the filters applied), `count`, `reviews[]`.
  A review: `review_id`, `url`, `rating`, `title`, `text`, `language`, `likes`, `source`, `verified`, `verification_source`, `verification_level`, `published_at`, `experienced_at`, `updated_at`, `consumer` {`consumer_id`, `name`, `country_code`, `review_count`, `verified`, `image_url`}, `reply` {`text`, `published_at`, `updated_at`} or null, `location`, `merged`.
- **categories** - the tree: `query` (null), `count`, `subcategory_count`, `categories[]` {`category_id`, `name`, `subcategories[]` {`category_id`, `name`}}. With `query`, a flat list of matching categories, each with `category_id` and `name`.
- **category** - `category_id`, `name`, `parent_id`, `business_count`, `subcategories`, `country`, `page`, `per_page`, `total_results`, `total_pages`, `filters` {`sort`, `min_trust_score`, `claimed_only`}, `count`, `businesses[]` (search rows plus `recommended`).
- **review** - `review` (a review as above) and `business` {`business_unit_id`, `name`, `domain`, `profile_url`}.

A profile, trimmed (captured, `nordvpn.com`):

```json
{
  "data": {
    "name": "NordVPN",
    "domain": "nordvpn.com",
    "trust_score": 4.2,
    "stars": 4,
    "review_count": 50990,
    "review_count_last_12_months": 6722,
    "rating_distribution": { "1": 6194, "2": 1765, "3": 2150, "4": 4183, "5": 36698 },
    "claimed": true,
    "reply_behavior": {
      "reply_rate": 99.2,
      "avg_days_to_reply": 0.05,
      "negative_reviews": 1206,
      "negative_reviews_replied": 1196,
      "last_reply_to_negative_at": "2026-10-09T17:32:37.000Z"
    },
    "category_path": {
      "top": { "id": "electronics_technology", "name": "Electronics & Technology" },
      "mid": { "id": "internet_software", "name": "Internet & Software" },
      "bottom": { "id": "vpn_service", "name": "VPN Service" }
    },
    "topics": [
      { "id": "customer_service", "name": "Customer service", "summary": "..." }
    ],
    "reviews_count": 20
  }
}
```

A review with a business reply (captured, `nordvpn.com`, `stars: [1, 2]`):

```json
{
  "review_id": "6ac973241a356ec383b96536",
  "url": "https://www.trustpilot.com/reviews/6ac973241a356ec383b96536",
  "rating": 2,
  "title": "i ordered afull subscrtion &not working",
  "language": "en",
  "verified": true,
  "verification_level": "invited",
  "published_at": "2026-10-10T01:05:08.000Z",
  "experienced_at": "2026-10-09T00:00:00.000Z",
  "consumer": { "country_code": "US", "review_count": 5, "verified": false },
  "reply": {
    "text": "Hello! Please accept our apologies for any inconvenience. ...",
    "published_at": "2026-10-10T05:27:03.000Z",
    "updated_at": null
  }
}
```

A search row (captured, "vpn" in the US):

```json
{
  "business_unit_id": "548832a000006400057c1055",
  "name": "CyberGhost VPN",
  "domain": "cyberghostvpn.com",
  "profile_url": "https://www.trustpilot.com/review/cyberghostvpn.com",
  "trust_score": 4,
  "stars": 4,
  "review_count": 24134,
  "categories": [{ "id": "vpn_service", "name": "VPN Service", "primary": true }],
  "website": "https://www.cyberghostvpn.com",
  "email": "support@cyberghost.ro",
  "phone": null,
  "address": { "city": "Bucharest", "country_code": "RO", "country": "Romania" },
  "verified": true
}
```

## Guardrails

- **200 reviews per filter combination.** `/reviews` serves at most 10 pages of 20 for any one set of filters; `max_page` says how far the current combination goes, even when `total_pages` is larger. Never claim to have pulled "all reviews" of a large business, and never loop past page 10. To read more, slice into separate sets - each combination of `stars`, `language` and `date_range` (and `topics` or `search`) is its own set of up to 200:

  ```python
  seen = {}
  for stars in ([1], [2], [3], [4], [5]):
      for date_range in ("last30days", "last3months", "last6months", "last12months"):
          first = trustpilot("reviews", {"domain": "nordvpn.com", "language": "en",
                                         "stars": stars, "date_range": date_range})
          for page in range(1, first["max_page"] + 1):
              data = first if page == 1 else trustpilot("reviews", {
                  "domain": "nordvpn.com", "language": "en", "stars": stars,
                  "date_range": date_range, "page": page})
              for r in data["reviews"]:
                  seen[r["review_id"]] = r          # windows overlap, so dedupe by id
  ```

  That loop can run to 200 calls (400 credits). The date windows nest (30 days sits inside 3 months), so de-duplicate by `review_id`, and quote the credit total before running anything like it.
- `min_trust_score` is a minimum star rating, not a raw TrustScore cut-off. Trustpilot rounds TrustScore to stars, so `4` includes TrustScore 3.8 and up, and a 4.4 can show as 4.5 stars. Filter on `trust_score` yourself when the exact score matters. It is a floor only: to find low-rated businesses, page the listing and filter on `trust_score`.
- `email`, `phone` and `address` appear only when the business published them on Trustpilot; they are null otherwise. Never guess contact details.
- `ai_summary` and `topics` appear only when Trustpilot has them for the requested `language` (null or empty otherwise). The rating distribution and language breakdown always cover every language.
- The profile already includes the 20 newest reviews in its `language`; skip `/reviews` page 1 when that is all the user needs.
- There is no TrustScore history and no reviewer-profile endpoint. To track change over time, store snapshots yourself.
- Results usually take 2-5 seconds per call; batch sequentially rather than firing many calls at once.
- Never fabricate TrustScores, review counts, review text or replies. Only return what the API returned, and surface `profile_url` or the review `url` so the user can verify.

## Failure handling

- `400` means an invalid or missing parameter (both or neither of `domain` and `url`, `page` above 10 on reviews, a `review_id` that is not 24 hex characters, a `min_trust_score` other than 3, 4 or 4.5) - fix the body and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means the business, category or review does not exist on Trustpilot; the error names what was not found, and the call is billed (2 credits). Check the domain spelling - Trustpilot lists some businesses under `www.` and some without.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api).
- `502` / `503` mean Trustpilot data is temporarily unavailable - wait a few seconds and retry, up to a few times. These are not billed.
- If search returns nothing, try a shorter name or the business's domain.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.19.1
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.trustpilot.search("vpn", country="US", page_size=10)
profile = client.trustpilot.business(domain="nordvpn.com")
bad = client.trustpilot.reviews(domain="nordvpn.com", stars=[1, 2], language="en", date_range="last30days")
tree = client.trustpilot.categories()
ranked = client.trustpilot.category("vpn_service", sort="reviews_count", min_trust_score=4, claimed_only=True)
one = client.trustpilot.review("6aca2504b52cc4b518bf4b75")
```

```bash
npm install scavio@0.19.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const found = await scavio.trustpilot.search({ query: "vpn", country: "US", page_size: 10 });
const bad = await scavio.trustpilot.reviews({ domain: "nordvpn.com", stars: [1, 2], language: "en" });
const ranked = await scavio.trustpilot.category({ category_id: "vpn_service", min_trust_score: 4, claimed_only: true });
```

MCP: the Scavio MCP server exposes all 6 endpoints as tools (`search_trustpilot`, `get_trustpilot_business`, `get_trustpilot_reviews`, `get_trustpilot_categories`, `get_trustpilot_category`, `get_trustpilot_review`). Trustpilot is opt-in: add `trustpilot` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.17.1"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,trustpilot"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [Trustpilot search](https://scavio.dev/docs/trustpilot-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api), [business](https://scavio.dev/docs/trustpilot-business?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api), [reviews](https://scavio.dev/docs/trustpilot-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api), [categories](https://scavio.dev/docs/trustpilot-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api), [category](https://scavio.dev/docs/trustpilot-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api), [review](https://scavio.dev/docs/trustpilot-review?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api). Overview: [Trustpilot API](https://scavio.dev/trustpilot-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api).
