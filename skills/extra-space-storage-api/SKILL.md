---
name: extra-space-storage-api
description: Extra Space Storage API for Extra Space Storage (extraspace.com, the US self-storage REIT) - what a storage unit costs at an Extra Space facility, as its page shows it, with the IN STORE price next to the WEB RATE (the Knoxville - Middlebrook Pike facility listed a 10' x 10' climate-controlled unit at $160 in store and $92 web rate, 10 available, First Month Free) for every unit class available now (or every class), with size, square feet, features, available count and promotions, the facility's Starting at prices by size class and its price figures by size (lowest, average, highest and historical), hours by type, 24-hour access, rating and review count; a city's storage prices as Extra Space's city page states them (105 facilities near Dallas, TX had 5' x 5' units starting at $7 and averaging $24 a month, 141 had 10' x 10' units starting at $30 and averaging $78) with the figures for each size and for climate-controlled, RV, boat and vehicle storage; facility search near a ZIP code, "City, ST", place or point, up to 120 nearest first, filtered by climate control, drive-up, indoor, RV parking, enclosed vehicle storage, 24-hour access and unit size, sorted by distance or Starting at price, each with its highlighted unit prices; the Google reviews shown on a facility page with the star histogram, sorted, star-filtered and paged, with Extra Space's replies (no reviewer names); the 1,700 US cities Extra Space lists. 5 endpoints, 1 credit per call. US only, USD. No reservations, no move-in quotes, no price history beyond the figures the page gives.
version: 1.0.0
tags: extra-space-storage, extraspace, extraspace-com, extra-space-storage-api, extra-space-storage-prices, extra-space-storage-units, extra-space-storage-reviews, extra-space-storage-locations, extra-space-web-rate, self-storage, self-storage-prices, self-storage-api, storage-unit-prices, storage-units, storage-unit-sizes, climate-controlled-storage, drive-up-storage, rv-storage, boat-storage, vehicle-storage, 10x10-storage-unit, storage-price-comparison, storage-market-data, city-storage-prices, storage-facility-reviews, google-reviews, price-monitoring, rate-tracking, self-storage-reit, real-estate, real-estate-data, us-real-estate, usd, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/extraspace-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=extra-space-storage-api
---

# Extra Space Storage API - Storage Unit Prices, Facilities, Reviews

Read Extra Space Storage (extraspace.com, the US self-storage REIT): facility search near a ZIP code, city, place or point; one facility in full with every unit class available now and its IN STORE price and WEB RATE; a city's storage prices as Extra Space's city page states them; the Google reviews shown on a facility page; and the US cities Extra Space lists. Every answer is what Extra Space's public pages show a visitor without an account at the moment of the call, in USD per month. All 5 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Extra Space shows to any visitor and returns them as JSON for analysis. It uses no Extra Space account, no reservation, no rental or move-in flow and no customer login.

**The job this skill is for: what a storage unit costs at a facility, and what storage costs across a city.** `/facility` returns every unit class available now with its IN STORE price and WEB RATE, available count and promotions; `/city-prices` returns the city page's own price sentences and its figures for each size. Captured 2026-11-26 (1 credit per call):

| Request | What Extra Space showed |
|---|---|
| `/facility` 1935 - Knoxville - Middlebrook Pike (`store_id` 1934) | 14 of 43 unit classes available now; 10' x 10' climate-controlled $160 IN STORE / $92 WEB RATE (10 available), 5' x 5' $46 / $26, 10' x 20' $336 / $228 (8 available), all with First Month Free; Starting at $11 small, $72 medium, $228 large; rating 4.9 over 699 ratings, 24-hour access |
| `/city-prices` Dallas, TX | "105 self storage facilities near Dallas, TX have small 5' x 5' units available now, starting at $7 and averaging $24 per month."; 10' x 10': 141 facilities, $30 lowest, $78 average, $392 highest; 10' x 20': 108, $36, $148; climate controlled: 123, $8, $98; 120 facilities listed; rating 4.9 over 76,439 reviews |
| `/search` ZIP 90012 | 120 facilities (the most Extra Space lists), nearest 6109 - Los Angeles - Main St at 0.44 mi (Starting at $69 small, $179 medium, $341 large, Flash Sale), farthest 24.09 mi; Starting at prices from $7 to $224 |
| `/search` point 32.7767, -96.797 (Dallas), climate controlled, `sort: "price"` | 96 of 120 kept; lowest Starting at $5 (0514 - Dallas - Inwood Rd, 9.56 mi) |
| `/reviews` Knoxville - Middlebrook Pike | 485 text reviews (699 ratings), histogram 5 stars 456, 4: 12, 3: 8, 2: 3, 1: 6; `stars: [1]` returns the 6 one-star reviews |

Quote each price with Extra Space, the facility name and `store_id`, the unit size, the label (IN STORE or WEB RATE) and the `fetched_at` date. For other operators near the same place use `public-storage-api`, matched on unit size and features.

Ten limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`: a place with no match, an unknown facility id, a city with no page) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Two prices per unit, as labelled.** `in_store_price` is the page's IN STORE price and `web_rate` its WEB RATE, monthly in USD; a price Extra Space does not give is `null`. Prices can change at any time.
- **Up to 120 facilities, no further pages.** Extra Space lists up to 120 facilities near a place, nearest first. The filters and the price sort are applied by Scavio over that list using each facility card's own flags, so `total` is the list Extra Space gave and `count` what was kept.
- **Available now, unless asked.** `/facility` lists the unit classes available now, as the facility page lists them; `include_unavailable: true` adds every class (`available: false` means none to rent now). `available_count` is Extra Space's count of free units in the class.
- **Price figures without a stated period.** `price_stats` (lowest, average, highest, `historical_*`) are the figures Extra Space's page data gives by size; Extra Space does not state the period behind the historical figures. On a city page, `lowest` is the page's "starting at", `average` its "averaging", and `highest` and `historical_*` are in the page data but not shown on the page.
- **City pages are large.** A city page answered in 4 to 36 seconds in the captures and can take up to about 2 minutes; allow up to 3 minutes for `/city-prices`.
- **Reviews are the Google reviews on the page.** Extra Space sends every text review of a facility at once: sort, star filter, histogram and paging are computed by Scavio over that full set. `rating` and `rating_count` are Extra Space's summary and count star-only ratings too; `review_count` counts the text reviews.
- **No reviewer names.** No reviewer name is returned; in Extra Space's replies the reviewer's name reads `[name]`, and a reply addressing the reviewer by a name that cannot be matched is left out (`null`).
- **Store id, not store number.** `store_id` (the last number of the facility link, `1934`) is the input of facility and reviews; the store number in the facility name (`1935`) is a different number.
- **What is not there.** No reservations or rental flow, no move-in quote with fees or insurance, no customer account, no Spanish facility data, no facilities outside the US. In the captures search answered in 3.2 to 21 seconds, a facility in 2.6 to 16, reviews in 2.2 to 17 and locations in 1 to 1.7; set a client timeout of at least 240 seconds and send one request at a time.

Extra Space publishes no public developer API or data feed. This skill reads Extra Space's public pages with one Scavio key.

See also: `public-storage-api` (Public Storage facilities, unit prices and reviews), `google-maps-api` (storage facilities of every operator near a place), `yelp-business-data`. Same place and same unit size only: name the operator, the facility and the date with every price.

## When to trigger

Use this skill when the user asks to:
- Find Extra Space Storage facilities near a ZIP code, city, place or point, with their Starting at prices, features and hours
- Filter Extra Space facilities by climate control, drive-up, indoor, RV parking, enclosed vehicle storage, 24-hour access or unit size, or sort them by price
- Read what each storage unit costs at one Extra Space facility: IN STORE price, WEB RATE, size, features, available count and promotions
- Get a US city's self-storage prices as Extra Space's city page states them, by unit size and for climate-controlled, RV, boat or vehicle storage
- Read and filter the Google reviews shown on an Extra Space facility page, with the star histogram and Extra Space's replies
- List the US cities Extra Space has city pages for

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=extra-space-storage-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=extra-space-storage-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example 10 ZIP codes: one search and four facility reads each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures locations answered in 1-1.7 seconds, facility 2.6-16, reviews 2.2-17, search 3.2-21 and city prices 4-36 (allow up to 3 minutes). Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/extraspace/search` | Up to 120 facilities near a ZIP code, "City, ST", place or point, nearest first: filters, distance or price sort; each with address, distance, phone, promotion, Starting at prices by size class, rating, hours, features, sizes available and the highlighted unit prices | 1 |
| `POST /api/v1/extraspace/facility` | One facility by id or link: address, phones, hours by type, 24-hour access, rating, promotion, Starting at prices, price figures by size, description, directions, images, unit classes with IN STORE price, WEB RATE, size, features, available count and promotions, nearest facilities | 1 |
| `POST /api/v1/extraspace/reviews` | The Google reviews on a facility page: rating, rating count, histogram, sorted, star-filtered and paged reviews with Extra Space's replies, no reviewer names | 1 |
| `POST /api/v1/extraspace/city-prices` | A US city's storage prices as the city page gives them: the page's price sentences, figures by size or storage type with facility counts, up to 120 facilities, the city's rating | 1 |
| `POST /api/v1/extraspace/locations` | The US cities Extra Space lists (1,700), narrowed by state or by the start of a city name | 1 |

## Market

US only, English, USD per month. There is no `country`, `language` or `currency` input. `state` takes a 2-letter code or the state's name.

## Price fields

| Field | Meaning |
|---|---|
| `units[].in_store_price`, `units[].web_rate` | The page's IN STORE price and WEB RATE for the unit class, monthly USD; `null` where Extra Space gives none |
| `units[]` | {`unit_id`, `size_class` (Small, Medium, Large), `dimensions`, `width`, `depth`, `square_feet`, `exact_size`, `is_parking`, `features`, `available`, `available_count`, `first_come`, `limited`, `promotions`, `in_store_price`, `web_rate`} |
| `starting_at` | {`starting`, `small`, `medium`, `large`, `parking`}: the Starting at price by size class, as the card shows it |
| `best_prices[]` | The units a search card highlights, with both prices |
| `price_stats[]` | {`category` (All, a size such as 10x10, ClimateControlled, RVStorage, RVBoat, CarVehicle), `store_count` (city pages), `lowest`, `average`, `highest`, `historical_lowest`, `historical_average`, `historical_highest`} |
| `price_summary` | The city page's own price sentences, word for word |
| `promotion`, `promotions` | Extra Space's promotion text ("First Month Free", "2nd Month Free", "Flash Sale") |

- **The two prices differ.** On the Knoxville capture every WEB RATE was below the IN STORE price (10' x 10': $92 vs $160). Quote both with their labels; never compute a "discount" without saying it is computed.
- **`store_count` can exceed the facilities listed.** A city's `store_count` for a size counts facilities near the city with that size; `facilities` lists up to 120.

## Workflow

1. **Place.** `/search` with `term` (a ZIP code, "City, ST" or a place) or `latitude` + `longitude`, plus filters. An ambiguous place (`"Springfield"`) answers `did_you_mean`: send one of them as `term`.
2. **One facility.** `/facility` with `store_id` from `facilities[]`. Read `units` (IN STORE and WEB RATE), `starting_at` and `price_stats`.
3. **A city.** `/locations` (`{"state": "TX"}`) for the cities with a page, then `/city-prices` with `city` and `state`.
4. **Reviews.** `/reviews` with `store_id`, `sort`, `stars` and paging.
5. **Report.** Each price with Extra Space, the facility and `store_id`, the size, the label and the `fetched_at` date; city figures with the page's own wording.
6. **Over time:** store each answer with its `fetched_at`; unit prices and availability change as Extra Space updates them, and that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `term` | string | one of | A ZIP code (`90012`), `"City, ST"` (`Denver, CO`) or a place, 2-100 characters |
| `latitude`, `longitude` | number | one of | Or a point (`32.7767`, `-96.797`) |
| `climate_controlled` | boolean | false | Facilities with climate-controlled units |
| `drive_up_access` | boolean | false | Facilities with drive-up units |
| `indoor` | boolean | false | Facilities with indoor units |
| `rv_parking` | boolean | false | Facilities with RV, boat or vehicle parking (covered or uncovered) |
| `enclosed_vehicle_storage` | boolean | false | Facilities with enclosed vehicle storage |
| `all_hour_access` | boolean | false | Facilities with 24-hour access |
| `unit_sizes` | list | none | Facilities with at least one of these sizes available: `5x5`, `5x10`, `5x15`, `10x10`, `10x15`, `10x20`, `10x25`, `10x30` |
| `sort` | string | `distance` | `distance` (nearest first, as Extra Space orders them) or `price` (lowest Starting at price first; facilities without one last) |

### Facility (`/facility`) and reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string or integer | one of | An Extra Space facility id (`facilities[].store_id`; the last number of the facility link, e.g. `1934`) |
| `url` | string | one of | Or the facility's extraspace.com link (`facilities[].url`), 20-400 characters |
| `include_unavailable` | boolean | false | Facility only: also list unit classes with nothing to rent now |
| `sort` | string | `recent` | Reviews only: `recent`, `oldest`, `rating_desc` or `rating_asc` (newest first within a rating) |
| `stars` | list | none | Reviews only: star ratings to keep, e.g. `[1, 2]` |
| `page` | integer | 1 | Reviews only: 1-1000 |
| `page_size` | integer | 20 | Reviews only: 1-100 |

### City prices (`/city-prices`) and locations (`/locations`)

| Endpoint | Parameters |
|---|---|
| `/city-prices` | `city` (required, 2-80 characters: a US city Extra Space has a page for, see locations) and `state` (required: a 2-letter code or the state's name) |
| `/locations` | `state` (optional: code or name) and `query` (optional, 1-80 characters: cities whose name starts with it, `"San"` or `"San Antonio, TX"`) |

## Examples

### What each unit costs at one facility

```bash
curl -X POST https://api.scavio.dev/api/v1/extraspace/facility \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "1934"}'
```

Captured `data` (2026-11-26; `units` cut to 3 of 14, `hours` to 1 of 5, `price_stats` to 3 of 9; `url`, `description`, `directions`, `images`, `google_maps_url`, `nearest_locations` and `notes` dropped):

```json
{
  "store_id": 1934,
  "store_number": 1935,
  "name": "1935 - Knoxville - Middlebrook Pike",
  "address": {"line1": "8627 Middlebrook Pike", "line2": null, "city": "Knoxville", "county": "Knox", "state": "TN", "state_name": "Tennessee", "postal_code": "37923"},
  "latitude": 35.94443302,
  "longitude": -84.07066918,
  "phone": "8658885577",
  "existing_customer_phone": "8653818850",
  "time_zone": "Eastern Standard Time",
  "hours": [
    {"type": "staffing", "monday": "09:30 AM - 06:00 PM", "tuesday": "09:30 AM - 06:00 PM", "wednesday": "09:30 AM - 06:00 PM", "thursday": "09:30 AM - 06:00 PM", "friday": "09:30 AM - 06:00 PM", "saturday": "09:00 AM - 05:30 PM", "sunday": "Closed"}
  ],
  "has_24_hour_access": true,
  "rating": 4.9,
  "review_count": 699,
  "promotion": null,
  "starting_at": {"starting": 11, "small": 11, "medium": 72, "large": 228, "parking": null},
  "price_stats": [
    {"category": "All", "lowest": 26, "average": 105, "highest": 228, "historical_lowest": 26, "historical_average": 134, "historical_highest": 432},
    {"category": "5x5", "lowest": 26, "average": 30, "highest": 33, "historical_lowest": 26, "historical_average": 31, "historical_highest": 33},
    {"category": "10x10", "lowest": 72, "average": 82, "highest": 92, "historical_lowest": 72, "historical_average": 82, "historical_highest": 92}
  ],
  "has_kiosk": true,
  "has_available_inventory": true,
  "is_newly_built": false,
  "is_coming_soon": false,
  "is_grand_opening": false,
  "expected_opening": null,
  "unit_class_count": 43,
  "available_unit_class_count": 14,
  "units": [
    {"unit_id": "2533_1935", "size_class": "Medium", "dimensions": "10' x 15'", "width": 10, "depth": 15, "square_feet": 150, "exact_size": true, "is_parking": false, "features": ["Elevator Access", "Climate Controlled", "Indoor"], "available": true, "available_count": 6, "first_come": false, "limited": false, "promotions": ["First Month Free", "Flash Sale"], "in_store_price": 172, "web_rate": 98},
    {"size_class": "Medium", "dimensions": "10' x 10'", "features": ["Indoor", "Climate Controlled", "1st Floor Access"], "available_count": 10, "promotions": ["First Month Free"], "in_store_price": 160, "web_rate": 92},
    {"size_class": "Small", "dimensions": "5' x 5'", "features": ["Indoor", "Elevator Access", "Climate Controlled"], "available_count": 1, "promotions": ["First Month Free"], "in_store_price": 46, "web_rate": 26}
  ],
  "currency": "USD"
}
```

(The second and third units are cut to their size, features, count, promotions and prices.)

### A city's storage prices

```bash
curl -X POST https://api.scavio.dev/api/v1/extraspace/city-prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"city": "Dallas", "state": "TX"}'
```

Captured `data` (2026-11-26; `price_summary` cut to 2 of 10, `price_stats` to 3 of 13, `facilities` (120) and `notes` dropped, `url` dropped):

```json
{
  "city": "Dallas",
  "state": "TX",
  "state_name": "Texas",
  "currency": "USD",
  "search_center": {"latitude": 32.79657688785047, "longitude": -96.80622894392523},
  "rating": 4.9,
  "review_count": 76439,
  "price_summary": [
    "105 self storage facilities near Dallas, TX have small 5' x 5' units available now, starting at $7 and averaging $24 per month.",
    "141 self storage facilities near Dallas, TX have medium sized 10' x 10' units available starting at $30, with an average price of $78 per month."
  ],
  "price_stats": [
    {"category": "5x5", "store_count": 105, "lowest": 7, "average": 24, "highest": 58, "historical_lowest": 7, "historical_average": 26, "historical_highest": 132},
    {"category": "10x10", "store_count": 141, "lowest": 30, "average": 78, "highest": 392, "historical_lowest": 17, "historical_average": 83, "historical_highest": 392},
    {"category": "ClimateControlled", "store_count": 123, "lowest": 8, "average": 98, "highest": 1044, "historical_lowest": 8, "historical_average": 106, "historical_highest": 1750}
  ],
  "count": 120
}
```

### Facilities near a ZIP code

```bash
curl -X POST https://api.scavio.dev/api/v1/extraspace/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"term": "90012"}'
```

Captured `data` (2026-11-26; `facilities` cut to 1 of 120, its `url`, `hours`, `image` and `google_maps_url` dropped and `best_prices` cut to 2 of 4; `notes` dropped):

```json
{
  "term": "90012",
  "latitude": null,
  "longitude": null,
  "search_center": {"latitude": 34.065549, "longitude": -118.24054},
  "did_you_mean": [],
  "currency": "USD",
  "filters": {"features": [], "unit_sizes": []},
  "sort": "distance",
  "total": 120,
  "count": 120,
  "facilities": [
    {
      "store_id": 6109,
      "store_number": 6109,
      "name": "6109 - Los Angeles - Main St",
      "address": "1000 N Main St",
      "city": "Los Angeles",
      "state": "CA",
      "state_name": "California",
      "postal_code": "90012",
      "latitude": 34.06222011,
      "longitude": -118.2340683,
      "distance_mi": 0.44,
      "phone": "2136692650",
      "promotion": "Flash Sale",
      "starting_at": {"starting": 69, "small": 69, "medium": 179, "large": 341, "parking": 437},
      "rating": 4.8,
      "review_count": 524,
      "features": ["climate_controlled", "drive_up_access", "indoor", "enclosed_vehicle_storage", "video_surveillance"],
      "unit_sizes_available": ["5x5", "5x10", "10x10", "10x15", "10x20", "10x25", "10x30"],
      "is_coming_soon": false,
      "is_grand_opening": false,
      "expected_opening": null,
      "best_prices": [
        {"unit_id": "2562_6109", "type": "size", "size_class": "Medium", "dimensions": "9' x 10'", "width": 9, "depth": 10, "square_feet": 90, "features": ["Elevator Access", "Indoor", "Climate Controlled"], "promotions": ["First Month Free"], "first_come": true, "limited": false, "in_store_price": 282, "web_rate": 179},
        {"unit_id": "2555_6109", "type": "size", "size_class": "Small", "dimensions": "5' x 5'", "width": 5, "depth": 5, "square_feet": 25, "features": ["Climate Controlled", "Indoor", "Elevator Access"], "promotions": ["2nd Month Free"], "first_come": true, "limited": false, "in_store_price": 124, "web_rate": 69}
      ]
    }
  ]
}
```

A filtered, price-sorted search near a point (`{"latitude": 32.7767, "longitude": -96.797, "climate_controlled": true, "sort": "price"}`, captured) kept 96 of 120, lowest first: 0514 - Dallas - Inwood Rd ($5 Starting at, 9.56 mi), 3185 - Dallas - Harry Hines Blvd ($6, 2.91 mi), 7282 - Mesquite - Big Town Blvd ($7, 7.72 mi). An ambiguous term (`"Springfield"`) answered `total` 0 with 10 `did_you_mean` places.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/extraspace/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "1934", "stars": [1]}'
```

Captured `data` (2026-11-26; `reviews` cut to 1 of 6, its `text` shortened; `notes` dropped):

```json
{
  "store_id": 1934,
  "name": "1935 - Knoxville - Middlebrook Pike",
  "rating": 4.9,
  "rating_count": 699,
  "review_count": 485,
  "histogram": {"1": 6, "2": 3, "3": 8, "4": 12, "5": 456},
  "stars": [1],
  "sort": "recent",
  "page": 1,
  "page_size": 20,
  "total": 6,
  "pages": 1,
  "has_more": false,
  "count": 6,
  "reviews": [
    {"review_id": "0a092aad-f39f-4a03-b98b-5303ac8b827e", "rating": 1, "text": "Did not call me about payment not being processed and locked my unit only after it being late 3 days. ...", "date": "2025-10-09T00:00:00", "source": "Google", "reply": "Sorry for any inconvenience with the payment processing and unit access. Please contact us at (865) 888-5577 to resolve this immediately.", "reply_date": "2025-10-10T07:58:00"}
  ]
}
```

A reply that names the reviewer reads `[name]`: "Thank you for the recommendation, [name]! We appreciate your feedback and are glad to hear you experienced great service at Extra Space Storage."

### Locations

`{"state": "TX"}` (captured): `total` 1,700 cities across 44 state codes (DC among them), 125 in Texas, each `{"city": "Addison", "state": "TX", "state_name": "Texas"}`; `city` and `state` are the inputs of city-prices.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def es(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/extraspace/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# Climate-controlled facilities with a 10x10 near a ZIP, nearest first (1 credit)
s = es("search", {"term": "90012", "climate_controlled": True, "unit_sizes": ["10x10"]})["data"]
print(s["count"], "of", s["total"], "kept")

# Every available unit at the three nearest (1 credit each)
for f in s["facilities"][:3]:
    fac = es("facility", {"store_id": f["store_id"]})["data"]
    for u in fac["units"]:
        if u["dimensions"] in ("10' x 10'",):
            print(fac["name"], u["dimensions"], "IN STORE", u["in_store_price"], "WEB RATE", u["web_rate"], u["promotions"])

# Store each answer with fetched_at: that stored set is your record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every answer carries `notes`.

- **facility card** (search, city prices) - `store_id` (the input of facility and reviews), `store_number`, `name`, `url`, `address`, `city`, `state`, `state_name`, `postal_code`, `latitude`, `longitude`, `distance_mi`, `phone`, `promotion`, `starting_at`, `rating`, `review_count`, `hours`, `features`, `unit_sizes_available`, `is_coming_soon`, `is_grand_opening`, `expected_opening`, `best_prices[]` {`unit_id`, `type`, `size_class`, `dimensions`, `width`, `depth`, `square_feet`, `features`, `promotions`, `first_come`, `limited`, `in_store_price`, `web_rate`}, `image`, `google_maps_url`.
- **search** - `term`, `latitude`, `longitude`, `search_center`, `did_you_mean`, `currency`, `filters` {`features`, `unit_sizes`}, `sort`, `total`, `count`, `facilities[]`, `notes`.
- **facility** - `store_id`, `store_number`, `name`, `url`, `address` {`line1`, `line2`, `city`, `county`, `state`, `state_name`, `postal_code`}, `latitude`, `longitude`, `phone`, `existing_customer_phone`, `time_zone`, `hours[]` (by `type`: staffing, business, gate ...), `has_24_hour_access`, `rating`, `review_count`, `promotion`, `starting_at`, `price_stats[]`, `has_kiosk`, `has_available_inventory`, `is_newly_built`, `is_coming_soon`, `is_grand_opening`, `expected_opening`, `description`, `directions`, `google_maps_url`, `images`, `unit_class_count`, `available_unit_class_count`, `units[]`, `nearest_locations[]`, `currency`, `notes`.
- **reviews** - `store_id`, `name`, `rating`, `rating_count`, `review_count`, `histogram`, `stars`, `sort`, `page`, `page_size`, `total`, `pages`, `has_more`, `count`, `reviews[]` {`review_id`, `rating`, `text`, `date`, `source`, `reply`, `reply_date`}, `notes`.
- **city prices** - `city`, `state`, `state_name`, `url`, `currency`, `search_center`, `rating`, `review_count`, `price_summary`, `price_stats[]`, `count`, `facilities[]`, `notes`.
- **locations** - `state`, `query`, `total`, `states`, `count`, `cities[]` {`city`, `state`, `state_name`}, `notes`.

## Guardrails

- Name it "Extra Space Storage (extraspace.com, the US self-storage REIT)" on first mention, "Extra Space" after that.
- Prices: USD per month with Extra Space, the facility name and `store_id`, the unit size, the label (IN STORE or WEB RATE) and the `fetched_at` date. Say that prices can change at any time and are confirmed on the facility page at rental; never present a price as a quote or a reservation.
- Price figures: quote `price_stats` and `price_summary` as Extra Space's figures, and say that Extra Space states no period for the historical figures.
- Reviews: no reviewer is named or identified; quote review text as shown with its rating, date and source (Google), and say how many of `review_count` matched a filter.
- Descriptive only: no commentary on Extra Space's business, pricing practices or policies.
- Do not republish facility photos, descriptions or review text in bulk. Write extraspace.com as plain text and cite store ids, facility names and capture dates rather than linking Extra Space pages.
- Terms: Scavio keeps no copy: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no reservation or rental flow. Extra Space's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, available counts, store ids, ratings or reviews. Return what the API returned, with the `fetched_at` time.
- Not available: reservations, move-in quotes with fees or insurance, customer accounts, reviewer names, facilities outside the US, results past the 120 Extra Space lists near a place.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search with neither or both of `term` and a point ("send one of term (a ZIP code, \"City, ST\" or a place) or latitude with longitude."); a term under 2 characters; a `unit_sizes` or `sort` value outside its list; `/facility` or `/reviews` without exactly one of `store_id` or `url` ("send one of store_id or url."), or a `store_id` that is not digits; a state that is not one ("state must be a US state: a 2-letter code (TX) or its name (Texas)."). A value the request schema rejects (a type, range or list) answers with `error` and a `details` array naming each invalid field.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Extra Space Storage found no place for this search term. Send a ZIP code, \"City, ST\" or latitude and longitude.", "Extra Space Storage has no facility with this id. Use search facilities[].store_id (the facility link ends with it; the store number is a different number).", "Extra Space Storage has no city page for <city>, <state>. Use locations for the cities Extra Space lists.". Take store ids and city names from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=extra-space-storage-api).
- `502` means Extra Space data was temporarily unavailable ("Extra Space Storage is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Extra Space Storage is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.98.0
npm install scavio@0.99.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: near } = await scavio.extraspace.search({ term: "90012", climate_controlled: true });
const { data: facility } = await scavio.extraspace.facility({ store_id: "1934" });
const { data: reviews } = await scavio.extraspace.reviews({ store_id: "1934", stars: [1, 2] });
const { data: city } = await scavio.extraspace.cityPrices({ city: "Dallas", state: "TX" });
const { data: cities } = await scavio.extraspace.locations({ state: "TX" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.extraspace.search(...)`, `facility`, `reviews`, `city_prices` and `locations`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 5 endpoints as tools: `search_extraspace`, `get_extraspace_facility`, `get_extraspace_reviews`, `get_extraspace_city_prices` and `get_extraspace_locations`. Extra Space Storage is opt-in: add `extraspace` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.98.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,extraspace"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/extraspace-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=extra-space-storage-api), [facility](https://scavio.dev/docs/extraspace-facility?utm_source=agent-skills&utm_medium=skill&utm_campaign=extra-space-storage-api), [reviews](https://scavio.dev/docs/extraspace-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=extra-space-storage-api), [city prices](https://scavio.dev/docs/extraspace-city-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=extra-space-storage-api), [locations](https://scavio.dev/docs/extraspace-locations?utm_source=agent-skills&utm_medium=skill&utm_campaign=extra-space-storage-api). Overview: [Extra Space Storage API](https://scavio.dev/extraspace-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=extra-space-storage-api).
