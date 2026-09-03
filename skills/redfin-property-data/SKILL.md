---
name: redfin-property-data
description: Redfin listing search for sale, sold or for rent with filters for price, beds, baths, square footage and property type; one property in full with the Redfin Estimate, price and tax history, schools and comparable sales; plus housing-market stats for a city, ZIP or neighborhood. 3 endpoints, 1 credit each.
version: 1.0.0
tags: redfin, redfin-api, property-data, real-estate, mls-listings, home-prices, sold-homes, rentals, price-history, redfin-estimate, housing-market, comparable-sales, langchain, crewai, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F3E0"
    homepage: https://scavio.dev/docs/redfin-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=redfin-property-data
---

# Redfin Property Data API - For Sale, Sold, Rentals, Price History

Search Redfin listings for sale, sold or for rent with the full filter set, open any one of them for the complete MLS fact sheet plus the Redfin Estimate, and pull housing-market statistics for a whole region. All three endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find homes for sale, recently sold homes, or rentals in a specific area
- Filter listings by price, beds, baths, square footage, lot size, year built, HOA, property type or pool
- Pull one property in full: Redfin Estimate, price and tax history, agents, schools, climate risk, comparable sales
- Get housing-market statistics for a city, ZIP, neighborhood or county
- Build real-estate lead lists, comp analyses or market-trend datasets

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=redfin-property-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=redfin-property-data) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/redfin`. Every endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/redfin/search` | 1 | Listings, up to 350 per page, page-paginated |
| `POST /api/v1/redfin/property` | 1 | One listing in full, with the Redfin Estimate and comps |
| `POST /api/v1/redfin/market` | 1 | Housing-market statistics for a region |

`/property` and `/market` read the property or region **page**, whose inlined request cache replaces the roughly 40 internal calls that page made - which is why they cost the same as a search.

## How to name a location

This is the one thing that trips callers up.

**City names are not accepted on `location`.** Redfin's own name-lookup path is the single route its edge blocks. Give the endpoint either of these instead:

1. A **redfin.com region URL** - `/city/`, `/neighborhood/`, `/county/` or `/zipcode/` - or a bare 5-digit ZIP code, in `location`; or
2. `region_id` **and** `region_type` together.

`region_id` is **not** a ZIP code. They are different number spaces, and a ZIP passed as `region_id` resolves to some other city rather than failing, so a wrong answer looks like a right one. `region_id` and `region_type` must be sent as a pair - with only one of them, the transport falls back to `location`.

`region_type` values: `1` neighborhood, `2` ZIP, `5` county, `6` city.

## Workflow

1. **Search:** call `/redfin/search` with a region URL or ZIP in `location` (or `region_id` + `region_type`), plus filters. Set `listing_status` to `for_sale`, `sold` or `for_rent`.
2. **Open a listing:** call `/redfin/property` with a `property_id` or any redfin.com listing URL.
3. **Market context:** call `/redfin/market` with the same region reference to get medians, sale-to-list ratio, compete score and live inventory.

### Pagination

`/redfin/search` pages with `page` (1-based) and `limit` (1-350, default 100). `/property` and `/market` return a single object and take no paging parameter.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | one of | A redfin.com region URL (`/city/`, `/neighborhood/`, `/county/`, `/zipcode/`) or a bare 5-digit ZIP (1-500 chars). **City names are not accepted.** |
| `region_id` | integer | one of | Redfin region id. Not a ZIP code. Must be sent with `region_type`. |
| `region_type` | integer | one of | `1` neighborhood, `2` ZIP, `5` county, `6` city |
| `listing_status` | string | `for_sale` | `for_sale`, `sold`, `for_rent` |
| `sold_within_days` | integer | `90` | **Only valid with `listing_status: sold`** - rejected otherwise |
| `page` | integer | -- | 1-based |
| `limit` | integer | `100` | 1-350 |
| `sort` | string | `recommended` | `recommended`, `price_low`, `price_high`, `newest`, `oldest`, `sqft_low`, `sqft_high`, `price_per_sqft_low`, `price_per_sqft_high` |
| `min_price` | number | -- | Monthly rent when `listing_status: for_rent` |
| `max_price` | number | -- | |
| `beds_min` / `beds_max` | integer | -- | |
| `baths_min` | integer | -- | **Whole baths only** |
| `sqft_min` / `sqft_max` | integer | -- | |
| `lot_size_min` | integer | -- | |
| `year_built_min` / `year_built_max` | integer | -- | |
| `max_hoa` | number | -- | |
| `property_type` | string | -- | `house`, `condo`, `townhouse`, `multi_family`, `land`, `other`, `co_op` |
| `has_pool` | boolean | -- | |
| `max_days_on_market` | integer | -- | Mutually exclusive with `min_days_on_market` |
| `min_days_on_market` | integer | -- | Mutually exclusive with `max_days_on_market` |

Rules the endpoint enforces:

- `location` **or** (`region_id` **and** `region_type`).
- `sold_within_days` requires `listing_status: sold`. It only ever widens what `listing_status` already chose, so it is rejected elsewhere rather than silently ignored.
- `max_days_on_market` and `min_days_on_market` **cannot be combined**. Redfin expresses both through a single upstream parameter, so sending both would send the max and quietly drop the min.
- Every numeric filter is truncated into the underlying query, so **fractional bounds are rejected** - `1.5` baths would have silently become `1`.

### Property (`/property`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `property_id` | string | required | Redfin property id, or any redfin.com listing URL carrying one (1-500 chars) |

### Market (`/market`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | one of | Region URL or ZIP, same rules as search |
| `region_id` | integer | one of | Must be sent with `region_type` |
| `region_type` | integer | one of | `1`, `2`, `5`, `6` |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. For-sale search by region URL. A city NAME would not work here.
listings = requests.post(f"{BASE}/api/v1/redfin/search", headers=HEADERS,
    json={"location": "https://www.redfin.com/city/30749/TX/Austin",
          "listing_status": "for_sale", "min_price": 400000, "max_price": 800000,
          "beds_min": 3, "property_type": "house", "sort": "newest", "limit": 350}).json()

# 2. Same thing by ZIP
by_zip = requests.post(f"{BASE}/api/v1/redfin/search", headers=HEADERS,
    json={"location": "78704", "listing_status": "for_sale"}).json()

# 3. Recent sales - sold_within_days is valid ONLY with listing_status=sold
sold = requests.post(f"{BASE}/api/v1/redfin/search", headers=HEADERS,
    json={"location": "78704", "listing_status": "sold", "sold_within_days": 30}).json()

# 4. Rentals - min_price/max_price are MONTHLY RENT here
rentals = requests.post(f"{BASE}/api/v1/redfin/search", headers=HEADERS,
    json={"location": "78704", "listing_status": "for_rent", "max_price": 3000}).json()

# 5. One listing in full
prop = requests.post(f"{BASE}/api/v1/redfin/property", headers=HEADERS,
    json={"property_id": "https://www.redfin.com/TX/Austin/..."}).json()

# 6. Market stats for the same region
market = requests.post(f"{BASE}/api/v1/redfin/market", headers=HEADERS,
    json={"region_id": 30749, "region_type": 6}).json()
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **search** - price, price per sqft, beds, baths, living area, lot size, year built, coordinates, listing remarks and full photo galleries, up to 350 rows per page.
- **property** - price, Redfin Estimate and rental estimate, the complete MLS fact sheet, price and tax history, listing agents, open houses, schools, climate risk, walkability and location scores, sun exposure, monthly weather, permits, zoning, comparable sales and photos.
- **market** - median list and sale price, price per sqft, sale-to-list ratio, average offers and days on market, year-over-year movement, Redfin's 0-100 compete score, live inventory by property type, median price and active listings per bedroom count, and Redfin agent presence with an aggregate rating.

**`days_on_market` is always `null` on `/search`.** The upstream payload has no such key. Do not report it as populated, do not infer it from a listing date, and if the user needs time-on-market, use `/market` (which publishes an average for the region) or `min_days_on_market` / `max_days_on_market` as filters.

## Guardrails

- Every call is 1 credit, including a 350-row page. Prefer one wide page over several narrow ones.
- **Never pass a city name as `location`.** If the user says "Austin", resolve it to a redfin.com region URL or a ZIP first, or ask them for one - a name will not work and there is no name-lookup endpoint here.
- Never treat a ZIP as a `region_id`. It will resolve to a different city and return plausible-looking data for the wrong place.
- `sold_within_days` only makes sense with `listing_status: sold`. Do not send it with a for-sale or rental search.
- Do not combine `max_days_on_market` with `min_days_on_market` - pick one.
- Fractional filters are rejected on purpose. If the user wants 1.5 baths, say the filter is whole-baths only rather than rounding for them.
- `min_price` / `max_price` mean **monthly rent** on a `for_rent` search and sale price everywhere else. Label the number in your answer.
- `property_type` deliberately omits one Redfin code whose meaning could not be confirmed. If a listing class seems missing from results, do not guess a code - search without the filter.
- Never fabricate addresses, prices, estimates, agents or comps. Only return API data, and include the listing URL so the user can verify.
- Listing data moves fast. Say when the data was fetched, and never present an estimate as an appraisal.

## Failure handling

- `400` means an invalid or missing parameter - a city name in `location`, a lone `region_id` without `region_type`, `sold_within_days` on a non-sold search, both day-on-market bounds at once, or a fractional numeric filter. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the property or region does not resolve. Re-check the id or URL.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=redfin-property-data).
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry.
- If a search returns nothing, relax the price, bed or property-type filters before assuming the region is empty.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Python SDK

`langchain-scavio` has no Redfin tool - use the Scavio SDK directly:

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

listings = client.redfin.search(location="78704", listing_status="for_sale",
                                beds_min=3, max_price=800000, limit=350)
prop = client.redfin.property("https://www.redfin.com/TX/Austin/...")
market = client.redfin.market(region_id=30749, region_type=6)
```

JavaScript / TypeScript:

```bash
npm install scavio@0.15.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const listings = await scavio.redfin.search({ location: "78704", listing_status: "sold",
                                              sold_within_days: 30 });
```
