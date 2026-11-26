# Apartment List API - Rental Listings, Rent Report, Market Rent Data

Read Apartment List (apartmentlist.com, the US rental search site): its monthly rent report for a city, average rent and a listings summary for a city, neighborhood or ZIP code, rental search, one listing in full, resident-review summaries for a city, and place suggestions. Every answer is what Apartment List's public pages show a visitor without an account at the moment of the call, in USD. All 6 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Apartment List shows to any visitor and returns them as JSON for analysis. It uses no Apartment List account, no saved listings, no quiz, no tour or contact request and no rental application.

**The job this skill is for: what renting costs in a city, and which way rents are moving.** `/rent-report` returns Apartment List's monthly rent report for a US city: median rents for a 1-bedroom and a 2-bedroom, the month and year growth, the 12-month trend next to the state and the nation, year-to-date growth back to 2019, and the metro table of nearby cities. `/market-summary` adds Apartment List's average rent by bed count for the place and a summary of the listings on it. Captured 2026-11-26 (1 credit per call):

| City | Overall median rent (report text) | Median 1BR / 2BR (rent report) | Month / year growth | Average rent by bed count, studio / 1BR / 2BR / 3BR (market summary, 2026-11-20) |
|---|---|---|---|---|
| Austin, TX | $1,323 | $1,172 / $1,426 | -0.2% / -1.3% | $1,175 / $1,339 / $1,754 / $2,252, trend "even" |
| Chicago, IL | $1,858 | $1,723 / $1,875 | -1.1% / +3.4% | $1,918 / $2,299 / $2,767 / $3,306, trend "down" |
| New York City, NY | $2,593 | $2,475 / $2,609 | -0.35% / +4.3% | $4,184 / $5,148 / $7,141 / $8,374, trend "even" |

These are two different Apartment List figures: the rent report gives Apartment List's own median rent estimates for the city as its monthly report publishes them, and the market summary gives the average rent by bed count it shows for the place. Quote each with its label, the city and the report month or `pricing_date`; never mix them in one number. For listings in the same city use `/search` (Apartment List), `rent-com-api`, `rentcafe-api`, `hotpads-api` or `zillow-property-data`, matched on city, beds and date.

Ten limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Growth is a fraction.** `rent_growth_month`, `rent_growth_year`, `annual_trend` values and `ytd_growth` are fractions as Apartment List publishes them (-0.0133 is -1.33%). `annual_trend` is the cumulative change over the last 12 months; `ytd_growth` the change since January of each year.
- **Rent reports are city-level.** `/rent-report` and `/review-summaries` take a city (`city_slug` such as `/tx/austin`, or `city` with `state`); a city with no rent report is a charged `404`. A metro area or county is not searchable; send one of its cities.
- **A ZIP code reads its city.** Apartment List lists a ZIP code under its city: a ZIP search returns the city's listings inside the ZIP code's bounding box (a few may sit just outside it), and a ZIP code's market summary is the city's figures. A note says so.
- **Search is 20 a page.** Without filters or sort, listings come in Apartment List's own map order and the answer is quick; with any filter or sort (city or ZIP code only, not neighborhoods) Scavio reads Apartment List's filtered results, which can take up to about 2 minutes. `price_min`, `price_max` and `floor_plans` cover every unit a listing shows, not only the units a filter matched.
- **Prices as Apartment List shows them.** USD, monthly; a price Apartment List does not show is `null`. Each unit carries `price`, `base_price`, `total_price` and `required_fees` as Apartment List gives them; specials and fees are Apartment List's text.
- **Reviews without names.** `/listing` returns the resident reviews the listing page shows (not every listing shows them) with their category ratings; `/review-summaries` returns one summary per reviewed listing in a city (217 in Austin, 125 in Chicago, 8 in New York City). No reviewer name is returned.
- **No landlord personal data.** No landlord, agent or leasing-contact names. `phone` and `website_url` are returned for apartment communities only (a business line), never for private landlords.
- **Slow pages.** In the captures suggestions answered in 1.6 to 7 seconds, rent reports in 1.2 to 4, review summaries in 1 to 6.2, market summaries in 2.8 to 6.3, listings in 2 to 11 and searches in 5.3 to 23.6 (filtered searches up to about 2 minutes). Set a client timeout of at least 240 seconds and send one request at a time.
- **What is not there.** No landlord or agent contacts, no reviewer names, no rent history per listing, no Spanish pages, no listings outside the US, no quiz, tour, contact or application flow.

Apartment List offers no public developer API. This skill reads Apartment List's public pages with one Scavio key.

See also: `rent-com-api`, `rentcafe-api`, `hotpads-api` (full fees and rent history per listing), `zillow-property-data`, `trulia-api` and `streeteasy-api` (New York City). Same city or same listing only: match on city, beds and address, name the site and date with every number.

## When to trigger

Use this skill when the user asks to:
- Read Apartment List's monthly rent report for a US city: median 1-bedroom and 2-bedroom rent, month and year rent growth, the 12-month trend against the state and the nation, year-to-date growth, nearby cities and the national lists of fastest rent growth and highest rents
- Get Apartment List's average rent by bed count for a city, neighborhood or ZIP code, with a listings summary (average and median rent, size, unit and property counts, amenity shares, price histogram), optionally for some bed counts or amenities
- Search Apartment List rentals in a city, neighborhood or ZIP code with bed, bath, rent, move-in date, amenity or occupancy-type (affordable, senior, student, military, co-living) filters, sorted by match, newest or rent
- Read one Apartment List listing in full: floor plans with every unit's base price, total price and required fees, specials, fees, pet policies, parking, income requirement, amenities, office hours and resident reviews
- Compare resident-review ratings across a city's listings on Apartment List
- Look up the city, neighborhood and ZIP code slugs Apartment List uses

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=apartment-list-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=apartment-list-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example 25 cities: one rent report and one market summary each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, rent reports answered in 1.2-4 seconds, review summaries 1-6.2, suggestions 1.6-7, market summaries 2.8-6.3, listings 2-11 and searches 5.3-23.6 (filtered searches up to about 2 minutes). Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/apartmentlist/rent-report` | Apartment List's monthly rent report for a city: median 1BR and 2BR rent, month and year growth, 12-month trend (city, state, nation), year-to-date growth by year, metro table, national top rent growth and top rent levels, the report's sections as text | 1 |
| `POST /api/v1/apartmentlist/market-summary` | Average rent by bed count (studio to 3BR, with pricing date and trend) and a listings summary (average and median rent and size, property and unit counts, amenity shares, price histogram) for a city, neighborhood or ZIP code, optionally for some bed counts and amenities | 1 |
| `POST /api/v1/apartmentlist/search` | Rentals in a city, neighborhood or ZIP code, 20 a page: each listing with rent range, rent by bed count, floor plans and units, availability, specials flag, amenities, rating and highlight; totals, paging and the place's market summary | 1 |
| `POST /api/v1/apartmentlist/listing` | One listing by link or slug: address, description, year built, units, floor plans with every unit's prices and fees, specials, fees, pet policies, parking, requirements, lease terms, amenities, office hours, review summary and resident reviews | 1 |
| `POST /api/v1/apartmentlist/review-summaries` | One resident-review summary per reviewed listing in a city, most reviewed first: average ratings, rating count, best and worst rating, a snippet | 1 |
| `POST /api/v1/apartmentlist/suggestions` | Places (city, neighborhood, ZIP code, county, state) with the slug search and market-summary take, population, bounds and parents | 1 |

## Market

US only, USD. There is no `country`, `currency` or `language` input. Rents are monthly.

## Rent report and market fields

| Field | Meaning |
|---|---|
| `at_a_glance` | {`name`, `location_id`, `median_rent_1br`, `median_rent_2br`, `rent_growth_month`, `rent_growth_year`} |
| `annual_trend` | {`city`, `state`, `national`}: each {`name`, `location_id`, `monthly_change[]` {`date` (M/YYYY), `value`}}, the cumulative change over the last 12 months |
| `ytd_growth` | {`year`, `lines[]` {`year`, `months[]` {`month`, `label`, `growth`}}}: change since January of each year, from 2019 |
| `metro_table[]` | {`city`, `slug`, `location_id`, `median_rent_1br`, `median_rent_2br`, `rent_growth_month`, `rent_growth_year`} for the metro's cities |
| `top_rent_growth[]`, `top_rent_levels[]` | {`location_id`, `name`, `value`}: Apartment List's national lists (growth as a fraction; levels as a monthly rent) |
| `sections[]` | {`name`, `text`}: the report's own text ("Currently, the overall median rent in the city stands at $1,323, roughly the same as last month.") |
| `average_rent` (market summary, search `location_summary`) | {`studio`, `one_bedroom`, `two_bedroom`, `three_bedroom`, `pricing_date`, `trend` (up, down or even)} |
| `listings_summary` | {`average_price`, `median_price`, `average_sqft`, `median_sqft`, `property_count`, `unit_count`, `amenity_shares` (share of listings with each amenity), `price_histogram[]` {`price`, `unit_count`, `property_count`}}, for the listings that match the filters |

- **Overall median.** The rent report's overall median rent ($1,323 in Austin) is in `sections[]` text only; `at_a_glance` carries the 1BR and 2BR medians. Quote it as the report's text.

## Workflow

1. **Places.** `/suggestions` (`{"query": "Austin"}`): `places[].slug` is the `location` of `/search` and `/market-summary` (`/tx/austin`, `/il/chicago/neighborhoods/austin`, `/tx/austin/zip-78704`); a city's slug is the `city_slug` of `/rent-report` and `/review-summaries`. `searchable: false` (a county or state) cannot be searched.
2. **The city's rents.** `/rent-report` with `city_slug`. Note the report month in `sections[0].text`.
3. **The place's market.** `/market-summary` with `location` (and `beds` or `amenities` if wanted).
4. **Listings.** `/search` with `location` and filters or `sort`. Check the notes (map order, ZIP code read as its city).
5. **One listing.** `/listing` with `slug` from `listings[]`.
6. **Reviews across the city.** `/review-summaries` with `city_slug`; match `listing_id` to search `listings[].id`.
7. **Report.** Each rent with Apartment List, the place, USD, the report month or `pricing_date` and the `fetched_at` date; growth converted from fractions and labeled; no verdict on a listing or landlord.
8. **Over time:** store each answer with its `fetched_at`; the rent report changes monthly, and that stored set is your series.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | one place required | A place slug from suggestions: a city (`/tx/austin`), a neighborhood (`/tx/austin/neighborhoods/riverside`) or a ZIP code (`/tx/austin/zip-78704`) |
| `city` + `state` | string | one place required | Or a city name (2-80 characters) with its 2-letter state code (`Chicago`, `IL`) |
| `zip` | string | one place required | Or a 5-digit ZIP code (`78704`); `state` optional |
| `beds` | integer, string or list | none | 0 (studio), 1, 2 or 3 (3 or more), or a list of them (`[1, 2]`) |
| `baths` | integer | none | 1, 2 or 3 (or more) |
| `price_min`, `price_max` | integer | none | Monthly rent, USD (0-100,000) |
| `move_in_date` | string | none | `YYYY-MM-DD` |
| `amenities` | string or list | none | Up to 10, all must match: `is_pet_friendly`, `is_dog_friendly`, `is_cat_friendly`, `has_pool`, `has_gym`, `has_in_unit_laundry`, `has_on_site_laundry`, `has_laundry_connections`, `has_garage`, `has_parking`, `has_hardwood_floors`, `has_dishwasher`, `has_air_conditioning`, `has_balcony`, `is_accessible`, `has_bbq`, `has_bathtub`, `has_business_center`, `has_elevator`, `has_doorman`, `has_walk_in_closet`, `has_stainless_steel`, `has_granite_counter`, `has_garbage_disposal`, `has_furnished_option`, `has_fireplace`, `has_hot_tub`, `has_ceiling_fan` |
| `occupancy_types` | string or list | none | Any of `affordable`, `senior`, `student`, `military`, `co-living` |
| `sort` | string | Apartment List's map order | `best_match`, `freshness` (newest), `price_asc` or `price_desc` |
| `page` | integer | 1 | 1-250, 20 listings a page; `pages` says how many |

Filters and `sort` apply to city and ZIP code searches; a neighborhood search lists every listing without them.

### Rent report, market summary, review summaries, listing, suggestions

| Endpoint | Parameters |
|---|---|
| `/rent-report` | `city_slug` (a city slug such as `/tx/austin`) or `city` with `state` |
| `/market-summary` | one of `location`, `city` + `state` or `zip` (as in search); `beds` and `amenities` (as in search) only |
| `/review-summaries` | `city_slug` or `city` with `state` |
| `/listing` | one of `url` (an apartmentlist.com listing link, search `listings[].url`) or `slug` (search `listings[].slug`, e.g. `/tx/austin/the-asher`) |
| `/suggestions` | `query` (2-80 characters: a city, neighborhood, ZIP code, county or state) |

## Examples

### A city's rent report

```bash
curl -X POST https://api.scavio.dev/api/v1/apartmentlist/rent-report \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"city_slug": "/il/chicago"}'
```

Captured `data` (2026-11-26; `annual_trend` cut to the city's last 3 months, `ytd_growth`, `top_rent_growth`, `top_rent_levels`, `url` and `location.bounds` dropped, `metro_table` cut to 3 of 9, `sections` to the first of 8):

```json
{
  "city_slug": "/il/chicago",
  "location": {"id": 705702, "slug": "/il/chicago", "type": "city", "name": "Chicago", "display_name": "Chicago, IL"},
  "currency": "USD",
  "at_a_glance": {"name": "Chicago, IL", "location_id": 705702, "median_rent_1br": 1723, "median_rent_2br": 1875, "rent_growth_month": -0.0112, "rent_growth_year": 0.0337},
  "annual_trend": {
    "city": {"name": "Chicago, IL", "location_id": 705702, "monthly_change": [
      {"date": "8/2026", "value": 0.0556}, {"date": "9/2026", "value": 0.0454}, {"date": "10/2026", "value": 0.0337}
    ]}
  },
  "metro_table": [
    {"city": "Arlington Heights", "slug": "/il/arlington-heights", "location_id": 705513, "median_rent_1br": 1642, "median_rent_2br": 2093, "rent_growth_month": 0.0062, "rent_growth_year": 0.023},
    {"city": "Aurora", "slug": "/il/aurora", "location_id": 705531, "median_rent_1br": 1481, "median_rent_2br": 1951, "rent_growth_month": -0.0012, "rent_growth_year": 0.0199},
    {"city": "Chicago", "slug": "/il/chicago", "location_id": 705702, "median_rent_1br": 1723, "median_rent_2br": 1875, "rent_growth_month": -0.0112, "rent_growth_year": 0.0337}
  ],
  "sections": [
    {"name": "at_a_glance", "text": "Chicago Rent Report: November 2026\nWelcome to the Apartment List November 2026 Rent Report for Chicago, IL. Currently, the overall median rent in the city stands at $1,858, after falling 1.1% last month. Prices remain up 3.4% year-over-year. ..."}
  ],
  "notes": [
    "Figures are Apartment List's own rent estimates as its monthly rent report publishes them: median rents in USD, growth as a fraction (-0.0133 is -1.33%).",
    "annual_trend is the cumulative change over the last 12 months for the city, its state and the nation; ytd_growth is the change since January of each year."
  ]
}
```

In the same report `top_rent_levels` led with San Francisco, CA ($3,842), San Jose, CA and Irvine, CA, and `top_rent_growth` with Detroit, MI (`value` 0.0133).

### Average rent and the listings summary for a place

```bash
curl -X POST https://api.scavio.dev/api/v1/apartmentlist/market-summary \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": "/ny/new-york", "beds": 2}'
```

Captured `data` (2026-11-26; `location.bounds` dropped, `amenity_shares` cut to 4 of 31, `price_histogram` dropped):

```json
{
  "location": {"id": 700607, "slug": "/ny/new-york", "type": "city", "name": "New York City", "display_name": "New York City, NY"},
  "filters": {"beds": [2], "amenities": []},
  "currency": "USD",
  "location_id": 700607,
  "location_name": "New York City",
  "average_rent": {"studio": 4184, "one_bedroom": 5148, "two_bedroom": 7141, "three_bedroom": 8374, "pricing_date": "2026-11-20", "trend": "even"},
  "listings_summary": {
    "average_price": 6940,
    "median_price": 6510,
    "average_sqft": 519,
    "median_sqft": null,
    "property_count": 268,
    "unit_count": 335,
    "amenity_shares": {"has_dishwasher": 0.6, "has_hardwood_floors": 0.5, "has_in_unit_laundry": 0.46, "is_pet_friendly": 0.35}
  },
  "notes": ["average_rent is Apartment List's average rent by bed count for the place (with its trend: up, down or even); listings_summary describes the listings that match the filters, with a price histogram (price buckets with unit and property counts) and amenity_shares (the share of listings with each amenity)."]
}
```

### Search rentals in a city

```bash
curl -X POST https://api.scavio.dev/api/v1/apartmentlist/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"city": "Chicago", "state": "IL", "beds": 1, "price_max": 2000, "sort": "price_asc"}'
```

Captured `data` (2026-11-26; `listings` cut to 1 of 20, its `floor_plans` to 1 of several with 1 unit, `url`, `photos`, `amenities` and the remaining card fields dropped; `location_summary` and `notes` dropped):

```json
{
  "location": {"id": 705702, "slug": "/il/chicago", "type": "city", "name": "Chicago", "display_name": "Chicago, IL"},
  "filters": {"beds": [1], "baths": null, "price_min": null, "price_max": 2000, "move_in_date": null, "amenities": [], "occupancy_types": []},
  "sort": "price_asc",
  "total_listings": 442,
  "total_units": 854,
  "page": 1,
  "page_size": 20,
  "pages": 23,
  "has_more": true,
  "count": 20,
  "listings": [
    {
      "id": "p112618710",
      "name": "Westhaven Park Phase II B - Affordable Housing",
      "slug": "/il/chicago/westhaven-park-phase-ii-b-affordable-housing",
      "address": "110 North Wood Street, Chicago, IL 60612",
      "neighborhood": "West Side",
      "currency": "USD",
      "show_price": true,
      "price_min": 660,
      "price_max": 1454,
      "price_by_beds": [
        {"beds": 1, "price_min": 660, "price_max": 1054},
        {"beds": 2, "price_min": 1260, "price_max": 1260},
        {"beds": 3, "price_min": 1118, "price_max": 1454}
      ],
      "bed_range": [1, 2, 3],
      "floor_plans": [
        {"id": 10343717, "name": "1BDRM T/C", "beds": 1, "baths": 1, "sqft": 682, "sqft_max": 719, "price": 660, "price_max": null, "unit_count": 4,
         "units": [{"unit_id": "p112618710-2-9", "name": "3-0009", "price": 660, "base_price": 660, "total_price": null, "required_fees": null, "sqft": 717, "availability": "available", "available_on": "2026-05-22", "available_now": true, "lease_length_months": 12, "updated_at": "2026-11-26T10:04:31Z"}]}
      ]
    }
  ]
}
```

Other captured searches: `{"location": "/tx/austin"}` (no filters) listed 2,197 listings with 20,223 units in Apartment List's map order (110 pages); `{"zip": "78704"}` listed 156 listings, with the note that Apartment List lists ZIP 78704 under Austin and `location_summary` is the city's.

### One listing

```bash
curl -X POST https://api.scavio.dev/api/v1/apartmentlist/listing \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "/tx/austin/the-asher"}'
```

Captured `data` (2026-11-26; `floor_plans` cut to 1 of 32, the review text and snippet shortened or dropped, `description`, `highlight`, `amenities`, `office_hours`, `photos`, `website_url`, `phone`, `url` and the disclaimers dropped; `notes` dropped):

```json
{
  "id": "p65805790",
  "name": "The Asher",
  "slug": "/tx/austin/the-asher",
  "rental_type": "apartment",
  "address": {"street": "13460 Lyndhurst Street", "city": "Austin", "county": "Austin", "state": "TX", "zip": "78717", "formatted": "13460 Lyndhurst Street, Austin, TX 78717"},
  "meta_neighborhood": "Cedar Park",
  "year_built": 2023,
  "total_units": 377,
  "currency": "USD",
  "price_by_beds": [{"beds": 1, "price_from": 1381}, {"beds": 2, "price_from": 1870}, {"beds": 3, "price_from": 3057}],
  "floor_plan_count": 32,
  "available_unit_count": 40,
  "floor_plans": [
    {"id": 6826819, "name": "A9", "beds": 1, "baths": 1, "sqft": 957, "sqft_max": 957, "price": 1928, "price_max": null, "unit_count": 1,
     "units": [{"unit_id": "p65805790-A.A9-3058", "name": "3058", "price": 1928, "base_price": 1928, "total_price": 1928, "required_fees": 0, "sqft": 957, "availability": "available", "available_on": "2026-11-30", "available_now": false, "lease_length_months": 16, "updated_at": "2026-11-26T10:02:30Z"}]}
  ],
  "specials": [{"text": "Limited Time Offer. Up to 10 Weeks Free!", "type": "auto_parse_opt_out", "monthly_price_discount": 0, "estimated_value": 0, "expires_at": null, "created_at": "2026-11-04T09:44:47.027Z", "updated_at": "2026-11-04T09:44:47.027Z"}],
  "pet_policies": {"allowed": true, "allowed_pets": ["cats", "dogs"], "details": null, "general": null, "cats": null, "dogs": null},
  "requirements": {"income": "Must have 3x the rent in total household income (before taxes)", "income_multiplier": 3, "evictions_allowed": "case_by_case", "evictions_policy": null, "credit_check": null, "criminal_check": null},
  "availability_last_checked_at": "2026-11-26T16:10:51.022Z",
  "review_summary": {"rating": 5, "amenities_rating": 5, "value_rating": 4, "rating_count": 1, "best_rating": 5, "worst_rating": 5, "snippet_rating": 5, "snippet_date": "2025-04-24"},
  "reviews_total": 1,
  "reviews": [{"date": "2025-04-24", "text": "It’s a pretty chill place to stay. ...", "rating": 5, "value": 4, "amenities": 5, "location": 5, "management": 5, "maintenance": 5, "parking": 4, "noise": 5}]
}
```

### Review summaries and suggestions

- `/review-summaries` `{"city_slug": "/tx/austin"}`: 217 summaries, most reviewed first, each with `listing_id` (`p37112`: rating 3.83 from 6 ratings, best 5, worst 3, a snippet and its date). No reviewer names.
- `/suggestions` `{"query": "Austin"}`: 10 places: Austin, TX (`/tx/austin`, population 790,390), the Austin neighborhood of Chicago (`/il/chicago/neighborhoods/austin`), Austintown, OH, Austin County, TX (`searchable: false`), Austin, MN, Austin, IN and neighborhoods in El Paso, Covington, Lynn and Stafford Courthouse.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def apartmentlist(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/apartmentlist/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# Rent reports for a few cities (1 credit each)
for slug in ["/tx/austin", "/il/chicago", "/ny/new-york"]:
    r = apartmentlist("rent-report", {"city_slug": slug})["data"]
    g = r["at_a_glance"]
    print(g["name"], g["median_rent_1br"], g["median_rent_2br"],
          f'{g["rent_growth_month"]:+.2%} month', f'{g["rent_growth_year"]:+.2%} year')

# Average rent by bed count for one place (1 credit)
m = apartmentlist("market-summary", {"location": "/tx/austin"})["data"]
print(m["average_rent"])

# 1-bedrooms under $2,000, lowest rent first (1 credit; filtered searches can take up to ~2 minutes)
s = apartmentlist("search", {"location": "/tx/austin", "beds": 1, "price_max": 2000, "sort": "price_asc"})["data"]
for l in s["listings"][:5]:
    print(l["name"], l["price_min"], l["price_max"], l["units_available"])

# Store each answer with fetched_at: that stored set is your series.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every answer carries `notes`.

- **search listing** (`listings[]`) - `id`, `name`, `slug`, `url` (the input of listing), `address`, `neighborhood`, `latitude`, `longitude`, `currency`, `show_price`, `price_min`, `price_max`, `price_by_beds[]` {`beds`, `price_min`, `price_max`}, `bed_range`, `floor_plans[]` {`id`, `name`, `beds`, `baths`, `sqft`, `sqft_max`, `price`, `price_max`, `photo`, `unit_count`, `units[]` {`unit_id`, `name`, `price`, `base_price`, `total_price`, `required_fees`, `sqft`, `availability`, `available_on`, `available_now`, `lease_length_months`, `updated_at`}}, `units_available`, `soonest_available`, `has_rent_special`, `fee_transparent`, `occupancy_types`, `amenities` {`community`, `unit`}, `amenities_text`, `photos`, `photo_count`, `highlight` {`title`, `text`, `tag`}, `unit_highlights[]` {`unit_id`, `unit`, `unit_type`, `price`, `price_change`, `is_total_price`, `available_now`, `available_on`, `lease_length_months`}, `rating`, `value_rating`, `review_snippet`, `standout_category`, `updated_at`.
- **search** - `location`, `zip` and `city` (for a ZIP code), `filters`, `sort`, `total_listings`, `total_units`, `page`, `page_size`, `pages`, `has_more`, `count`, `listings[]`, `location_summary` {`location_id`, `location_name`, `average_rent`, `listings_summary`}, `notes`.
- **listing** - `id`, `name`, `slug`, `url`, `rental_type`, `address` {`street`, `city`, `county`, `state`, `zip`, `formatted`}, `neighborhood`, `meta_neighborhood`, `latitude`, `longitude`, `description`, `year_built`, `year_remodeled`, `total_units`, `currency`, `show_price`, `price_by_beds[]` {`beds`, `price_from`}, `floor_plan_count`, `available_unit_count`, `floor_plans`, `specials[]` {`text`, `type`, `monthly_price_discount`, `estimated_value`, `expires_at`, `created_at`, `updated_at`}, `fees` {`fee_sheet_url`, `price_shown_plus_fees`, `application_fee`, `deposit`, `move_in_fees`, `additional_fees`, `utilities_included`}, `pet_policies` {`allowed`, `allowed_pets`, `details`, `general`, `cats`, `dogs`}, `parking[]`, `requirements` {`income`, `income_multiplier`, `evictions_allowed`, `evictions_policy`, `credit_check`, `criminal_check`}, `lease_terms`, `occupancy_types`, `amenities` {`top`, `unit`, `community`}, `office_hours[]` {`day`, `opens`, `closes`}, `time_zone`, `website_url`, `phone` (apartment communities only), `source`, `availability_last_checked_at`, `updated_at`, `highlight`, `floor_plan_disclaimers`, `photos`, `photo_count`, `review_summary` {`rating`, `amenities_rating`, `value_rating`, `rating_count`, `best_rating`, `worst_rating`, `snippet`, `snippet_rating`, `snippet_date`}, `reviews_total`, `reviews[]` {`date`, `text`, `rating`, `value`, `amenities`, `location`, `management`, `maintenance`, `parking`, `noise`}, `notes`.
- **rent report** - `city_slug`, `location`, `url`, `currency`, `at_a_glance`, `annual_trend` {`city`, `state`, `national`}, `ytd_growth`, `metro_table[]`, `top_rent_growth[]`, `top_rent_levels[]`, `sections[]` {`name`, `text`}, `notes`.
- **market summary** - `location`, `filters`, `currency`, `location_id`, `location_name`, `average_rent`, `listings_summary`, `notes`.
- **review summaries** - `city_slug`, `count`, `review_summaries[]` {`listing_id`, `rating`, `amenities_rating`, `value_rating`, `rating_count`, `best_rating`, `worst_rating`, `snippet`, `snippet_rating`, `snippet_date`}, `notes`.
- **suggestions** - `query`, `count`, `places[]` {`id`, `slug`, `type` (city, neighborhood, zip_code, county, state), `name`, `display_name`, `long_name`, `metro_id`, `county_id`, `population`, `coordinates`, `bounds` {`ne`, `sw`}, `parents`, `searchable`}, `notes`.

## Guardrails

- Name it "Apartment List (apartmentlist.com, the US rental search site)" on first mention, "Apartment List" after that.
- Rent report figures: always "Apartment List's rent report" with the city and the report month ("Apartment List's November 2026 rent report put Chicago's median 1-bedroom rent at $1,723, up 3.4% over the year"). Convert growth fractions to percents and say so. They are Apartment List's own estimates, not a survey of every lease or Scavio's view of the market.
- Market summary figures: "Apartment List's average rent by bed count" with the place and `pricing_date`; never present them as the rent report's medians, or the other way round.
- Listing rents: USD, monthly, with Apartment List, the listing name or slug and the `fetched_at` date; say whether a figure is a listing's range, a floor plan or a unit's `base_price` or `total_price`. Specials and fees are Apartment List's text as given.
- Reviews: no reviewer is named or identified; quote review text and ratings as Apartment List shows them, with the date and how many reviews the summary covers.
- Fair housing: describe listings and places with the data as Apartment List gives it; do not characterize an area by who lives there, and do not steer anyone toward or away from an area or a listing.
- No landlord personal data: use a community's business `phone` or `website_url` only as Apartment List gives them, and do not try to identify a landlord, an agent, a leasing contact or a reviewer.
- Descriptive only: no commentary on Apartment List's business, a property's pricing practices or policies.
- Do not republish Apartment List photos, descriptions or review text in bulk. Write apartmentlist.com as plain text and cite slugs, listing ids and capture dates rather than linking Apartment List pages.
- Terms: Scavio keeps no copy: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no quiz, tour, contact or application flow. Apartment List's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate rents, growth figures, ratings, slugs or listing ids. Only return what the API returned, with the `fetched_at` time.
- Not available: landlord or agent contacts, reviewer names, rent history per listing, Spanish pages, listings outside the US, quiz, tours, contact or applications.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: no place or two places ("send one of location (a suggestions places[].slug), city (with state) or zip."); `state` with `location` ("state goes with city or zip, not with location."); a bad state ("state must be a 2-letter US state code (e.g. TX). Apartment List covers the US only.") or ZIP ("zip must be a 5-digit US ZIP code (e.g. 78704)."); a metro area or county ("location: a metro area or county is not searchable; send one of its cities (suggestions places[] of type city)."); a `beds` value outside 0-3 ("beds must be 0 (studio), 1, 2 or 3 (3 or more), or a list of them."); an amenity outside the list; `price_min` above `price_max` ("price_min must not be above price_max."); a bad date ("move_in_date must be a date as YYYY-MM-DD."); filters or sort on a neighborhood ("filters and sort apply to city and ZIP code searches: Apartment List's neighborhood pages list every listing. Search the neighborhood without filters, or its city with them."); other inputs on `/market-summary` ("market-summary takes beds and amenities only (not sort)."); `/listing` without exactly one of `url` or `slug` ("send one of url or slug."); `/rent-report` or `/review-summaries` without a city ("send city_slug (e.g. /tx/austin) or city with state."), or with a slug that is not a city ("city_slug must be a city slug such as /tx/austin (suggestions places[].slug of a city)."); suggestions under 2 characters.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Apartment List has no city, neighborhood or ZIP code at this location. Use suggestions to find it (places[].slug).", "Apartment List has no listing at this link (it may have left the site). Use the url from search listings[].url.", "Apartment List publishes no rent report for this city (city and state as Apartment List names them, e.g. Austin, TX; or a suggestions city slug).". Take slugs from `/suggestions` and a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=apartment-list-api).
- `502` means Apartment List data was temporarily unavailable ("Apartment List is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Apartment List is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.98.0
npm install scavio@0.99.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: report } = await scavio.apartmentlist.rentReport({ city_slug: "/il/chicago" });
const { data: market } = await scavio.apartmentlist.marketSummary({ location: "/ny/new-york", beds: 2 });
const { data: rentals } = await scavio.apartmentlist.search({ city: "Chicago", state: "IL", beds: 1, price_max: 2000, sort: "price_asc" });
const { data: listing } = await scavio.apartmentlist.listing({ slug: "/tx/austin/the-asher" });
const { data: reviews } = await scavio.apartmentlist.reviewSummaries({ city_slug: "/tx/austin" });
const { data: places } = await scavio.apartmentlist.suggestions({ query: "Austin" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.apartmentlist.suggestions(...)`, `search`, `listing`, `rent_report`, `market_summary` and `review_summaries`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 6 endpoints as tools: `get_apartmentlist_suggestions`, `search_apartmentlist`, `get_apartmentlist_listing`, `get_apartmentlist_rent_report`, `get_apartmentlist_market_summary` and `get_apartmentlist_review_summaries`. Apartment List is opt-in: add `apartmentlist` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.98.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,apartmentlist"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/apartmentlist-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=apartment-list-api), [listing](https://scavio.dev/docs/apartmentlist-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=apartment-list-api), [suggestions](https://scavio.dev/docs/apartmentlist-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=apartment-list-api), [market summary](https://scavio.dev/docs/apartmentlist-market-summary?utm_source=agent-skills&utm_medium=skill&utm_campaign=apartment-list-api), [rent report](https://scavio.dev/docs/apartmentlist-rent-report?utm_source=agent-skills&utm_medium=skill&utm_campaign=apartment-list-api), [review summaries](https://scavio.dev/docs/apartmentlist-review-summaries?utm_source=agent-skills&utm_medium=skill&utm_campaign=apartment-list-api). Overview: [Apartment List API](https://scavio.dev/apartmentlist-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=apartment-list-api).
