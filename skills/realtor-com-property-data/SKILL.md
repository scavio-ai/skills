---
name: realtor-com-property-data
description: "Realtor.com property data API: search listings for sale, pending, for rent or sold with up to 200 rows per 1-credit call and filters for lot size, property type, sold-within days and listing-text keywords, pull one property in full with price and tax history, home value estimates, schools and flood/fire risk, get area market stats, and find agents with every review. 6 endpoints, 1 credit each."
version: 1.0.0
tags: realtor, realtor-com, realtor-api, realtor-com-api, real-estate, property-data, mls-listings, for-sale, for-rent, sold-homes, sold-comps, land-comps, home-prices, home-value-estimate, tax-history, housing-market, real-estate-agents, langchain, crewai, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/realtor-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data
---

# Realtor.com Property Data API - Listings, Sold Comps, Valuations, Agents

Search Realtor.com listings for sale, pending, for rent or sold with the full filter set, read one property in full, pull housing market stats for an area, resolve a place name to a location, and find agents and read a full agent profile with every review. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Search US homes, land or rentals on Realtor.com by city, county, ZIP, neighborhood, a point and radius, or a listing agent
- Pull sold comps: recent sales in an area filtered by property type, lot size, price band and sold-within days
- Watch new listings whose description mentions a keyword (e.g. `workshop`, `live/work`, `storefront`) across several cities
- Look up one property by Realtor.com URL or property id: price history, tax history with assessed and market values, home value estimates, schools, flood and wildfire risk, the listing agent
- Get median listing, sold and rent prices, days on market and year-over-year change for a city, county or ZIP
- Find real estate agents in a city or ZIP, or read one agent's profile, license, sales stats and reviews
- Build a land, rental or new-construction lead list from Realtor.com

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every Realtor.com endpoint costs **1 credit** per call.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/realtor/search` | 1 per page | Listings for sale, pending, for rent or sold, up to 200 per call: list price, sold price and date, beds, baths, sqft, lot size, year built, HOA, flags, address with county and coordinates, MLS id, listing agent and office |
| `POST /api/v1/realtor/property` | 1 | One property in full: description and detail groups, price history, tax history, three home value estimates with ranges plus history and forecast, nearby schools with ratings, flood/wildfire/noise risk, the listing agent and office with contact details, mortgage estimate, photos |
| `POST /api/v1/realtor/locations` | 1 | Location suggestions for a partial name: cities, counties, ZIPs, neighborhoods, schools and addresses, with the `slug_id` for market and the `property_id` for an address |
| `POST /api/v1/realtor/market` | 1 | Market stats for a city, county or ZIP: median listing, sold and rent price, price per sqft, days on market, lot size, listing counts, year-over-year and month-over-month change, breakdown by property type |
| `POST /api/v1/realtor/agents` | 1 per page | Agents by city, ZIP or name: rating, review and recommendation counts, active listings and price range, homes sold last year, broker, office, first year, services |
| `POST /api/v1/realtor/agent` | 1 | One agent's profile with every review: bio, phones, website, license, MLS memberships, languages, specializations, served areas, office, social links, sales stats, and reviews with four sub-ratings and the agent's reply |

## Workflow

1. **Search:** call `/realtor/search` with `location` (e.g. `"Maricopa County, AZ"`, `"Austin, TX"`, a ZIP) plus filters. Each row carries `property_id` and `url`.
2. **Property:** call `/realtor/property` with a `property_id` from step 1, or a pasted `url`.
3. **Market:** call `/realtor/locations` with a place name, take a `slug_id` (e.g. `Austin_TX`, `Travis-County_TX`), then call `/realtor/market` with `location`. `"City, ST"` also works directly.
4. **Agents:** call `/realtor/agents` with `location` (`"Austin, TX"`), `postal_code` or `name`, then `/realtor/agent` with an `agent_id`. A listing's `agent.agent_id` also works, and `/realtor/search` with `agent_id` returns that agent's listings.

### Pagination

- **Search:** `page` (1-based) and `page_size` (default 50, up to 200). The response carries `total`, `count` and `max_page`. `page` x `page_size` may not exceed 10,000 - see Guardrails.
- **Agents:** `page` (1-based) and `page_size` (default 20, up to 50). The response carries `total`.
- **Property, locations, market, agent:** no paging.

Every page is 1 credit, so state the budget before looping.

## Parameters

### Search (`/search`)

Pass one of `location`, `latitude` + `longitude` + `radius_miles`, or `agent_id`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | one of | City (`"Austin, TX"`), county (`"Travis County, TX"`), ZIP code, state or neighborhood |
| `latitude` / `longitude` | number | -- | Center of a radius search |
| `radius_miles` | number | -- | 0.1 to 50 miles around the center |
| `agent_id` | string | -- | Only this agent's listings |
| `listing_status` | string | `for_sale` | `for_sale` (includes pending and contingent, as on the site), `pending`, `for_rent`, `sold` |
| `exclude_pending` | boolean | -- | `for_sale` only: leave out pending and contingent listings |
| `min_price` / `max_price` | number | -- | USD: list price, sold price on `sold`, monthly rent on `for_rent` |
| `beds_min` / `beds_max` | integer | -- | Bedrooms |
| `baths_min` / `baths_max` | number | -- | Bathrooms |
| `sqft_min` / `sqft_max` | integer | -- | Interior square feet |
| `lot_sqft_min` / `lot_sqft_max` | integer | -- | Lot size in square feet (1 acre = 43,560) |
| `year_built_min` / `year_built_max` | integer | -- | Year built, 1700-2100 |
| `garage_min` | integer | -- | Minimum garage spaces |
| `max_hoa` | number | -- | Maximum monthly HOA fee in USD; listings without an HOA fee are kept |
| `property_types` | string[] | -- | `single_family`, `condos`, `townhomes`, `multi_family`, `land`, `mobile`, `farm` |
| `listed_within_days` | integer | -- | Listed in the last N days, 1-3650 |
| `sold_within_days` | integer | -- | `sold` only: sold in the last N days, 1-3650 |
| `price_reduced_within_days` | integer | -- | Price cut in the last N days, 1-3650 |
| `keywords` | string[] | -- | 1-10 keywords matched against the listing text (e.g. `["workshop"]`) |
| `new_construction` | boolean | -- | Only new construction |
| `foreclosure` | boolean | -- | Only foreclosures |
| `has_open_house` | boolean | -- | Only listings with an open house in the next 7 days |
| `sort` | string | `relevance` | `relevance`, `newest`, `price_low`, `price_high` (sold price on `sold`), `sold_newest` (`sold` only), `sqft_high`, `lot_size_high`, `year_built_new`, `recently_updated`, `recently_reduced` |
| `page` | integer | 1 | Results page, 1-based |
| `page_size` | integer | 50 | Listings per page, 1-200 |

### Property (`/property`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `property_id` | string | one of | Numeric property id from search or locations (e.g. `9564057635`) |
| `url` | string | one of | A realtor.com property or rental URL |

Pass exactly one of `property_id` or `url`.

### Locations (`/locations`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | City, county, ZIP, neighborhood, school or street address, 1-200 chars |

### Market (`/market`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | required | A `slug_id` from locations (`Austin_TX`, `Travis-County_TX`) or `"City, ST"` |

### Agents (`/agents`)

Pass exactly one of `location`, `postal_code` or `name`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | one of | City as `"City, ST"` (e.g. `"Austin, TX"`) |
| `postal_code` | string | one of | 5-digit ZIP code |
| `name` | string | one of | Agent name, 2-100 chars |
| `page` | integer | 1 | Results page, 1-1000 |
| `page_size` | integer | 20 | Agents per page, 1-50 |

### Agent (`/agent`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `agent_id` | string | required | Numeric agent id from search rows (`agent.agent_id`) or agents (e.g. `642581`) |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/realtor/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": "Maricopa County, AZ", "listing_status": "sold", "property_types": ["land"], "sold_within_days": 180, "lot_sqft_min": 5000, "page_size": 200}'
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def realtor(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/realtor/{endpoint}", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]

# 1. Sold land comps in one county, up to 200 rows for 1 credit
comps = realtor("search", {"location": "Maricopa County, AZ", "listing_status": "sold",
                           "property_types": ["land"], "sold_within_days": 180,
                           "lot_sqft_min": 5000, "sort": "sold_newest", "page_size": 200})
print(comps["total"], "sales;", comps["max_page"], "pages at this size")
for row in comps["listings"]:
    a = row["address"]
    print(row["sold_price"], row["sold_date"], row["lot_sqft"], a["line"], a["city"], a["postal_code"])

# 2. Keyword watch: new for-sale listings mentioning "workshop"
fresh = realtor("search", {"location": "Austin, TX", "keywords": ["workshop"],
                           "listed_within_days": 7, "sort": "newest"})
for row in fresh["listings"]:
    print(row["list_price"], row["beds"], row["sqft"], row["url"])

# 3. One property in full
home = realtor("property", {"property_id": "9564057635"})
print(home["list_price"], home["price_per_sqft"], home["hoa_fee"], home["risk"]["flood_severity"])
for event in home["property_history"]:
    print(event["date"], event["event"], event["price"])
for school in home["schools"][:3]:
    print(school["name"], school["rating"], school["distance_miles"])

# 4. Market stats for a city
loc = realtor("locations", {"query": "Austin"})["locations"][0]   # slug_id "Austin_TX"
market = realtor("market", {"location": loc["slug_id"]})
print(market["median_listing_price"], market["median_days_on_market"], market["year_over_year_pct"])

# 5. Agents in a city, then one full profile with every review
agents = realtor("agents", {"location": "Austin, TX", "page_size": 10})
top = agents["agents"][0]
profile = realtor("agent", {"agent_id": top["agent_id"]})
print(profile["name"], profile["license"], profile["sold_total"], len(profile["reviews"]))
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **search** - `listing_status`, `total`, `count`, `page`, `page_size`, `max_page`, `listings[]`.
  A row: `property_id`, `listing_id`, `url`, `status`, `list_date`, `list_price`, `list_price_min`, `list_price_max`, `price_per_sqft`, `sold_price`, `sold_date`, `last_status_change_at`, `flags` {`new_listing`, `price_reduced`, `foreclosure`, `new_construction`, `pending`, `contingent`, `coming_soon`}, `property_type`, `sub_type`, `beds`, `baths`, `baths_full`, `baths_half`, `sqft`, `lot_sqft`, `year_built`, `garage`, `stories`, `address` {`line`, `unit`, `city`, `state_code`, `postal_code`, `county`, `county_fips`, `lat`, `lng`}, `hoa_fee`, `photo`, `photo_count`, `open_houses[]`, `tags[]`, `mls` {`id`, `listing_id`}, `agent` {`agent_id`, `name`}, `office` {`office_id`, `name`}, `price_reduced_amount`, `estimate`.
- **property** - the search row fields plus `last_price_change_amount`, `last_price_change_date`, `days_on_market`, `description`, `features`, `neighborhoods[]`, `details[]` {`category`, `parent_category`, `items[]`}, `property_history[]` {`date`, `event`, `price`, `price_per_sqft`, `source`}, `tax_history[]` {`year`, `tax`, `assessed` {`building`, `land`, `total`}, `market` {...}}, `valuations[]` {`source`, `estimate`, `high`, `low`, `date`, `is_best`}, `valuation_history[]` and `valuation_forecast[]` {`source`, `points[]` {`date`, `estimate`}}, `schools[]` {`school_id`, `name`, `rating`, `parent_rating`, `distance_miles`, `levels[]`, `grades[]`, `funding`, `students`, `district`}, `risk` {`flood_factor`, `flood_severity`, `fema_zone`, `fire_factor`, `fire_severity`, `noise_score`}, `popularity[]`, `listing_agent` {`agent_id`, `name`, `email`, `phone`, `license`, `office` {`name`, `email`, `phone`}}, `buyer_agent`, `mortgage_estimate` {`tax_rate`, `insurance_rate`, `monthly_payment`, `loan_amount`, `down_payment`}, `monthly_fees[]`, `photos[]`, `virtual_tours[]`, `parcel` {`apn`}, `mls_disclaimer`.
- **locations** - `query`, `count`, `locations[]` {`text`, `area_type`, `slug_id`, `city`, `state_code`, `postal_code`, `county`, `property_id`, `latitude`, `longitude`}.
- **market** - `location`, `geo_type`, `state_code`, `latitude`, `longitude`, `parents[]` {`geo_type`, `slug_id`, `name`}, `median_listing_price`, `median_sold_price`, `median_rent_price`, `median_price_per_sqft`, `median_days_on_market`, `median_lot_sqft`, `listing_count`, `rental_listing_count`, `year_over_year_pct` {`active_listings`, `days_on_market`, `listing_price`, `price_per_sqft`, `rent`}, `month_over_month_pct`, `by_property_type[]` {`type`, `median_listing_price`, `median_sold_price`, `median_price_per_sqft`, `median_days_on_market`, `median_lot_sqft`}.
- **agents** - `total`, `count`, `page`, `page_size`, `agents[]` {`agent_id`, `name`, `is_realtor`, `broker`, `office`, `photo`, `rating`, `review_count`, `recommendation_count`, `for_sale_count`, `for_sale_price_min`, `for_sale_price_max`, `last_listing_at`, `sold_last_year`, `first_year`, `services` {`buyer[]`, `seller[]`}}.
- **agent** - the agents row plus `bio`, `phones[]` {`type`, `number`}, `website`, `license` {`number`, `state`}, `designations[]`, `languages[]`, `specializations[]`, `served_areas[]` {`name`, `state_code`}, `mls_memberships[]`, `sold_total`, `last_sold_date`, `office_details` {`name`, `website`, `phones[]`, `address`}, `social` {`facebook`, `instagram`, `linkedin`, `x`}, `reviews[]` {`review_id`, `rating`, `responsiveness`, `market_expertise`, `negotiation`, `professionalism`, `comment`, `reviewer`, `reviewer_type`, `location`, `year`, `date`, `reply`}.

A sold land row, trimmed (captured, Maricopa County, AZ, `listing_status: "sold"`, `property_types: ["land"]`):

```json
{
  "property_id": "1795946305",
  "url": "https://www.realtor.com/realestateandhomes-detail/9155-W-Garfield-St_Tolleson_AZ_85353_M17959-46305",
  "status": "sold",
  "sold_price": 135000,
  "sold_date": "2025-06-13",
  "property_type": "land",
  "lot_sqft": 6591,
  "address": {
    "line": "9155 W Garfield St",
    "city": "Tolleson",
    "state_code": "AZ",
    "postal_code": "85353",
    "county": "Maricopa",
    "county_fips": "04013",
    "lat": 33.455652,
    "lng": -112.256709
  }
}
```

A property, trimmed (captured, `9564057635`, Austin, TX):

```json
{
  "data": {
    "property_id": "9564057635",
    "status": "for_sale",
    "list_price": 535900,
    "price_per_sqft": 301,
    "beds": 3,
    "baths": 3,
    "sqft": 1778,
    "lot_sqft": 5066,
    "year_built": 2027,
    "hoa_fee": 75,
    "flags": { "new_listing": true, "new_construction": true },
    "property_history": [
      { "date": "2026-10-10", "event": "Listed", "price": 535900, "source": "UnlockMLS" }
    ],
    "schools": [
      { "name": "Newton Collins Elementary School", "rating": 7, "distance_miles": 1, "funding": "public" }
    ],
    "risk": { "flood_factor": 1, "flood_severity": "minimal", "fema_zone": "X (unshaded)", "fire_factor": 6, "fire_severity": "Major" },
    "listing_agent": { "agent_id": "100431241", "name": "Lee Jones", "phone": "(713) 948-6666", "license": "0439466" },
    "mortgage_estimate": { "monthly_payment": 4218, "loan_amount": 428720, "down_payment": 107180 }
  }
}
```

Market stats, trimmed (captured, `Austin_TX`):

```json
{
  "location": "Austin_TX",
  "geo_type": "city",
  "median_listing_price": 500000,
  "median_sold_price": null,
  "median_rent_price": 1949,
  "median_price_per_sqft": 310,
  "median_days_on_market": 81,
  "listing_count": 7072,
  "rental_listing_count": 7143,
  "year_over_year_pct": { "active_listings": -3.46, "listing_price": -9.09, "rent": -2.31 },
  "by_property_type": [
    { "type": "home", "median_listing_price": 525000, "median_sold_price": 484375, "median_days_on_market": 78 }
  ]
}
```

An agent review (captured, agent `1918615`):

```json
{
  "review_id": "9f45762e-d0b0-4d9e-a28f-1376ff4a4011",
  "rating": 5,
  "responsiveness": 5,
  "market_expertise": 5,
  "negotiation": 5,
  "professionalism": 5,
  "reviewer": "Nick",
  "reviewer_type": "BUYER",
  "location": "Hutto, TX",
  "date": "2026-09-11T03:03:43.157Z",
  "reply": null
}
```

## Guardrails

- **10,000 results per search.** `page` x `page_size` may not exceed 10,000; a request past that is a `400`. To cover a large area, slice it into separate searches by price band, property type, ZIP or radius, and de-duplicate by `property_id`. Never claim a search returned "every listing" when `total` is above 10,000.
- **Sold prices in non-disclosure states.** `sold_price` is null in US sold-price non-disclosure states (Texas, Utah, Wyoming, Alaska, Idaho, Kansas, Louisiana, Mississippi, Montana, New Mexico, North Dakota and parts of Missouri); `sold_date` still comes back. Say so when comps come back unpriced, and never estimate a missing sold price.
- `valuations`, `schools` and `risk` can be null or empty for land and new construction. Some market medians are null at some geography levels (e.g. `median_sold_price` for a city).
- `keywords` matches the listing text, not a structured field; confirm a hit in `description` via `/property` when it matters.
- Public listing data only: no owner names, buyer or seller identities, or mortgage records.
- Results usually take 1-5 seconds per call; batch sequentially rather than firing many calls at once.
- Never fabricate prices, estimates, school ratings or reviews. Only return what the API returned, and surface the listing `url` so the user can verify.

## Failure handling

- `400` means an invalid or missing parameter (no location, point or agent on search; both or neither of `property_id` and `url`; more than one of `location`, `postal_code` and `name` on agents; `page` x `page_size` above 10,000) - fix the body and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means the property, market or agent does not exist on Realtor.com; the error names what was not found, and the call is billed (1 credit).
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data).
- `502` / `503` mean Realtor.com data is temporarily unavailable - wait a few seconds and retry, up to a few times. These are not billed.
- If a `location` string returns nothing, resolve it with `/realtor/locations` first and retry with the suggestion's text or `slug_id`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.20.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

comps = client.realtor.search(location="Maricopa County, AZ", listing_status="sold",
                              property_types=["land"], sold_within_days=180, page_size=200)
home = client.realtor.property(property_id="9564057635")
places = client.realtor.locations("Austin")
market = client.realtor.market("Austin_TX")
agents = client.realtor.agents(location="Austin, TX", page_size=10)
profile = client.realtor.agent("1918615")
```

```bash
npm install scavio@0.20.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const comps = await scavio.realtor.search({ location: "Maricopa County, AZ", listing_status: "sold", property_types: ["land"], page_size: 200 });
const home = await scavio.realtor.property({ property_id: "9564057635" });
const market = await scavio.realtor.market({ location: "Austin_TX" });
```

MCP: the Scavio MCP server exposes all 6 endpoints as tools (`search_realtor`, `get_realtor_property`, `get_realtor_locations`, `get_realtor_market`, `search_realtor_agents`, `get_realtor_agent`). Realtor.com is opt-in: add `realtor` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.18.1"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,realtor"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [Realtor.com search](https://scavio.dev/docs/realtor-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data), [property](https://scavio.dev/docs/realtor-property?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data), [locations](https://scavio.dev/docs/realtor-locations?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data), [market](https://scavio.dev/docs/realtor-market?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data), [agents](https://scavio.dev/docs/realtor-agents?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data), [agent](https://scavio.dev/docs/realtor-agent?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data). Overview: [Realtor.com API](https://scavio.dev/realtor-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data).
