---
name: zillow-property-data
description: "Zillow property data API: search listings for sale, for rent or sold, pull one property in full, and read an agent's profile and reviews. Returns price and price history, Zestimate, tax history, beds, baths, living area, days on market, schools, open houses and photos. 3 endpoints, 1 credit each, structured JSON."
version: 1.0.0
tags: zillow, zillow-api, property-data, real-estate, listings, for-sale, for-rent, sold-homes, zestimate, price-history, home-prices, rental-market, market-analysis, langchain, crewai, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F3E0"
    homepage: https://scavio.dev/docs/zillow-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=zillow-property-data
---

# Zillow Property Data API - For Sale, Rent, Sold, Price History

Search Zillow listings in a region with the full filter set, read one property in full, and pull a Zillow agent's profile with their reviews. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find homes for sale, for rent, or recently sold in a city, neighbourhood or ZIP
- Filter listings by price, beds, baths, square footage, lot size, year built, HOA or home type
- Pull one listing in full - price history, Zestimate, tax history, RESO facts, rooms, schools, open houses, photos
- Look up a rental building's floor plans, amenities and unit counts
- Read a real-estate **agent's** profile, ratings and reviews
- Build comparables, rent-vs-buy analysis, or a market monitor

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=zillow-property-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=zillow-property-data) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Every Zillow endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/zillow/search` | 1 | Listings in a region: price, beds, baths, living area, Zestimate, coordinates, images, days on market |
| `POST /api/v1/zillow/property` | 1 | One listing in full: price and price history, Zestimate, tax history, description, RESO facts, rooms, schools, open houses, photos |
| `POST /api/v1/zillow/reviews` | 1 | An **agent** profile and its reviews - not a property |

**`/zillow/reviews` addresses an AGENT, not a home.** It takes a `screen_name` from a `zillow.com/profile/` URL. There is no property-review endpoint; do not present agent reviews as reviews of a house.

## Workflow

1. **Find listings:** call `/zillow/search` with `location` - a Zillow slug, a human place name, a ZIP, or a pasted Zillow search URL. Read `properties[].zpid`.
2. **One property:** call `/zillow/property` with that `zpid`, a `/homedetails/` URL, or - for a rental building - the `zillow.com/apartments/` URL. Rental buildings have **no caller-visible zpid**: search returns coordinates in that slot, so pass the apartments URL instead.
3. **An agent:** call `/zillow/reviews` with the agent's `screen_name` (or full profile URL). Screen names may contain spaces.

### Pagination

Only `/search` pages, with a 1-based `page`. The response carries `count` (what this page returned), `total_results` (Zillow's headline count) and `next_page_url`. `/property` and `/reviews` return a single object and take no paging parameter — the agent endpoint returns the **first five** reviews Zillow server-renders, where `count` is what came back and `total_review_count` is what the agent actually has.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | required | Zillow slug, human place name, ZIP, or a pasted Zillow search URL (1-200 chars) |
| `listing_status` | string | `for_sale` | `for_sale`, `for_rent`, `sold` |
| `page` | integer | -- | 1-based |
| `sort` | string | -- | `relevance`, `recommended`, `newest`, `price_low`, `price_high`, `payment_low`, `payment_high`, `beds`, `baths`, `sqft`, `lot_size`, `zestimate_low`, `zestimate_high`, `recent_change` |
| `min_price` / `max_price` | number | -- | On `for_rent` these mean **monthly rent** |
| `beds_min` / `beds_max` | integer | -- | Bedroom count |
| `baths_min` / `baths_max` | number | -- | Half-baths allowed (`1.5`) |
| `sqft_min` / `sqft_max` | integer | -- | Living area |
| `lot_size_min` / `lot_size_max` | integer | -- | Lot size |
| `year_built_min` / `year_built_max` | integer | -- | Year built |
| `max_hoa` | number | -- | Maximum monthly HOA |
| `home_type` | string | -- | `houses`, `townhomes`, `multi_family`, `condos`, `apartments`, `manufactured`, `lots_land` |
| `days_on_zillow` | string | -- | `1`, `7`, `14`, `30`, `90`, `6m`, `12m`, `24m`, `36m` |
| `keywords` | string | -- | Free-text listing keywords (1-200 chars) |
| `has_pool`, `has_garage`, `has_air_conditioning`, `is_waterfront`, `has_basement`, `is_new_construction`, `has_open_house`, `price_reduced`, `is_3d_tour` | boolean | -- | Feature flags |

Three things Zillow does that the filter table cannot show:

- **A bare ZIP works alone but cannot be combined with a filter or a sort.** On that request shape Zillow resolves the ZIP by geolocation and answers about a different city. Use the city name whenever you are also sending filters or a sort.
- **On `listing_status=for_rent`, `min_price`/`max_price` are monthly rent** - Zillow files rent under its payment filter, not its price filter.
- **`days_on_zillow` is closed.** An unrecognised value returns the *unfiltered* set under a `200`. Sorts that rank against a signed-in profile (saved, featured, personalised) are deliberately absent - this API is never signed in.

### Property (`/property`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zpid` | string | required | zpid, a `/homedetails/` URL, or a `zillow.com/apartments/` building URL |

### Agent reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `screen_name` | string | required | `zillow.com/profile/<name>/` screen name or full profile URL; may contain spaces |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Homes for sale - use the CITY name, not a ZIP, when filtering
listings = requests.post(f"{BASE}/api/v1/zillow/search", headers=HEADERS,
    json={"location": "Austin, TX", "listing_status": "for_sale",
          "min_price": 400000, "max_price": 750000,
          "beds_min": 3, "baths_min": 2, "sort": "newest"}).json()

zpid = listings["data"]["properties"][0]["zpid"]

# 2. Full property record
prop = requests.post(f"{BASE}/api/v1/zillow/property", headers=HEADERS,
    json={"zpid": zpid}).json()

# 3. Rentals: min_price / max_price are MONTHLY RENT here
rentals = requests.post(f"{BASE}/api/v1/zillow/search", headers=HEADERS,
    json={"location": "Austin, TX", "listing_status": "for_rent",
          "max_price": 2500, "beds_min": 2}).json()

# 4. A rental BUILDING has no visible zpid - pass the apartments URL
building = requests.post(f"{BASE}/api/v1/zillow/property", headers=HEADERS,
    json={"zpid": "https://www.zillow.com/apartments/austin-tx/the-quincy/5XjKpQ/"}).json()

# 5. An AGENT's profile and reviews (not a property)
agent = requests.post(f"{BASE}/api/v1/zillow/reviews", headers=HEADERS,
    json={"screen_name": "jane-smith"}).json()
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **search** — `url`, `listing_status`, `sort`, `region` (`id`, `type`, `name`, `display_name`, `bounds`), `title`, `description`, `total_results`, `page`, `next_page_url`, `count`, `properties[]`, `relaxed_count`, `relaxed_properties[]`.
  A property row: `position`, `zpid`, `url`, `is_building`, `building_name`, `status`, `home_status`, `listing_sub_type`, `price`, `price_display`, `currency`, `min_rent`, `max_rent`, `monthly_fees_min`, `monthly_fees_max`, `zestimate`, `rent_zestimate`, `tax_assessed_value`, `price_change`, `price_reduction`, `address`, `street_address`, `unit`, `city`, `state`, `zipcode`, `latitude`, `longitude`, `beds`, `baths`, `living_area`, `lot_area_value`, `home_type`, `days_on_zillow`, `date_sold`, `availability_date`, `available_unit_count`, `units`, `broker_name`, `image`, `images`, `has_3d_model`, `has_video`, `has_open_house`, `open_house_start`, `is_zillow_owned`.
- **property** — `listing_type`, `zpid`, `url`, `home_status`, `home_type`, `property_sub_type`, `price`, `currency`, `price_per_square_foot`, `price_change`, `date_posted`, `date_sold`, `zestimate`, `zestimate_low_percent`, `zestimate_high_percent`, `rent_zestimate`, `tax_assessed_value`, `property_tax_rate`, `monthly_hoa_fee`, `street_address`, `city`, `state`, `zipcode`, `county`, `neighborhood`, `latitude`, `longitude`, `bedrooms`, `bathrooms`, `living_area`, `lot_size`, `year_built`, `description`, `home_insights`, `days_on_zillow`, `page_view_count`, `favorite_count`, `photo_count`, `photos[]`, `virtual_tour_urls[]`. Rental buildings return floor plans, amenities and unit counts instead of a single-home record.
- **reviews** (agent) — `screen_name`, `encoded_zuid`, `url`, `name`, `business_name`, `profile_photo`, `is_top_agent`, `profile_types`, `rating`, `total_review_count`, `count`, `reviews[]` (`review_id`, `rating`, `comment`, `created_at`, `work_description`, `reviewer_screen_name`, `sub_ratings`, `response`), `review_filters[]`, `review_keywords[]`, `agent` (`title`, `description`, `years_in_industry`, `specialties`, `languages`, `website_url`, `business_address`, `phone`, `licenses`, `service_areas`, `past_sales_count`, `for_sale_listing_count`, `for_rent_listing_count`, `team_members`).

```json
{
  "data": {
    "listing_status": "for_sale",
    "region": { "name": "Austin", "type": "city" },
    "total_results": 5806,
    "page": 1,
    "count": 41,
    "properties": [
      {
        "zpid": "29444601",
        "street_address": "1200 Barton Hills Dr",
        "city": "Austin",
        "state": "TX",
        "price": 689000,
        "beds": 3,
        "baths": 2,
        "living_area": 1684,
        "zestimate": 702300,
        "days_on_zillow": 6
      }
    ]
  },
  "credits_used": 1,
  "credits_remaining": 999
}
```

## Guardrails

- Every call is **1 credit**, including one that comes back empty.
- A bare ZIP is only safe on its own. The moment you add a filter or a sort, switch to the city name or Zillow will silently answer about somewhere else.
- On `for_rent`, always describe `min_price`/`max_price` to the user as monthly rent, never as a purchase price.
- Never invent a `days_on_zillow` value. An unrecognised one returns the unfiltered set under a `200`, so the user pays for a filter that never ran.
- A Zestimate is Zillow's estimate, not an appraisal or a sale price. Label it as such and never present it as the listing price.
- `/reviews` is agent reviews. Never describe them as reviews of a property.
- Never fabricate addresses, prices, zpids, agent names or review text. Only return what the API returned.
- This is public listing data. Do not use it to profile the occupants of a home.

## Failure handling

- `400` means an invalid or missing parameter (no `location`, a `sort` or `home_type` outside the enum) — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means Zillow could not resolve the region, the zpid, or the agent screen name. An unresolvable region is a 404, **not** an empty result set — re-check the spelling or fall back to a broader place name rather than retrying.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=zillow-property-data).
- `502` / `503` mean upstream is temporarily unavailable — wait a few seconds and retry, up to a few times.
- A search that returns zero properties with a `200` is a real result: the filters were too tight. Relax them rather than retrying the same body.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

listings = client.zillow.search("Austin, TX", listing_status="for_sale", beds_min=3)
prop = client.zillow.property(listings["data"]["properties"][0]["zpid"])
agent = client.zillow.agent_reviews("jane-smith")
```

```bash
npm install scavio@0.15.0
```

```javascript
import { Scavio } from "scavio";

const client = new Scavio(); // reads SCAVIO_API_KEY
const listings = await client.zillow.search({ location: "Austin, TX", listing_status: "for_rent", max_price: 2500 });
const agent = await client.zillow.agentReviews({ screen_name: "jane-smith" });
```
