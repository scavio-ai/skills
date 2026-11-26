# Movoto API - Home Listings, Property Details, Market Trends

Read Movoto (movoto.com, the US home search site owned by Lower): a city's or ZIP code's housing market trends, home search for sale, sold or for rent, one home in full, one school and the homes zoned for it, and place suggestions. Every answer is what Movoto's public pages show a visitor without an account at the moment of the call, in USD. All 5 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Movoto shows to any visitor and returns them as JSON for analysis. It uses no Movoto account, no saved homes, no tour or contact request, no lead form and no financing flow.

**The job this skill is for: what a local housing market is doing, next to the homes on it.** `/market-trends` returns Movoto's market figures for a city or a ZIP code at three points (today, one month ago, one year ago), each split into all homes, single-family and condos, plus Movoto's summary sentence and the nearby cities or ZIP codes compared side by side. `/search` returns the same snapshot for the area next to its listings. Captured 2026-11-26 (1 credit per call):

| Place | Median list price today | One year ago (2025-10-31) | Price per sq ft today | Median days on market (today / year ago) | Active listings (today / year ago) |
|---|---|---|---|---|---|
| Los Angeles, CA (city) | $1,049,000 | $1,100,000 | $652 | 72 / 72 | 5,037 / 4,859 |
| New York, NY (city) | $1,299,000 | $1,399,000 | $1,476 | 104 / 130 | 9,541 / 12,180 |
| Austin, TX (city, from `/search`) | $525,000 | $585,000 | $283 | 99 / 91 | 6,472 / 6,323 |
| 78704, Austin, TX (ZIP) | $750,000 | $820,000 | $506 | 79 / 91 | 367 / 425 |
| 90012, Los Angeles, CA (ZIP, no state sent) | $570,000 | $649,000 | $581 | 93 / 106 | 100 / 90 |

These are Movoto's figures for homes listed for sale, as Movoto publishes them; they are not sale prices, an appraisal or Scavio's view of the market. Quote each with the place, the date and Movoto's label, and say whether it is a city or a ZIP code. For the same place on other sites use `zillow-property-data`, `redfin-property-data`, `realtor-com-property-data` or `trulia-api`, matched on the place and the date.

Ten limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent; a ZIP's trends with its daily statistics are still 1 credit. A not-found (`404`) is charged, and so is a page past the last one; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Three points in time, no series.** Market trends give today, one month ago and one year ago (`snapshots`), with `change_1m_percent` and `change_1y_percent` as Movoto rounds them. Movoto publishes no monthly series; to build one, call on a schedule and store each answer with its `fetched_at`.
- **List prices, not sale prices.** Medians and inventory describe homes listed for sale. On rentals, `market_summary` and `market_snapshot` are still the area's for-sale figures (a note says so).
- **No sale prices in non-disclosure states.** `sold_price` is `null` where the sale price is not public: Texas does not publish sale prices and Movoto shows none (22 Austin sold homes in one capture, every `sold_price` null, a note says why). Los Angeles sold homes carry it (a listing at $1,149,000 sold for $1,140,000 on 2026-11-25).
- **Search is 50 homes a page, to page 99.** That is up to 4,950 homes per query; `total` can be higher (Austin for sale: 5,885). A page past the last is empty, charged, and carries a note; narrow by ZIP, neighborhood, price or sold window to reach the rest. A filter Movoto did not apply is listed in `notes`.
- **Movoto's estimate is area-based.** `estimate` is "Movoto's area-based estimate": the area's price per square foot times the home's size, as Movoto shows it, with a range. It is not an appraisal and is `null` on rentals.
- **School data is GreatSchools data.** `rating` (1-10), `state_rating` and test scores are GreatSchools data as Movoto shows them. Parent reviews are not returned.
- **No agent personal data.** No listing-agent names, phones, emails or license numbers. `brokerage` is the company name (`null` where the brokerage label is a person's name). Phone numbers and emails are removed from descriptions.
- **Pages are quick but vary.** In the captures search answered in 1.3 to 9.7 seconds, a home in 1.5 to 7.4, market trends in 1.9 to 5.5, a school in 1.8 to 3.1 and suggestions in 1.0 to 3.3. Set a client timeout of at least 180 seconds and send one request at a time.
- **What is not there.** No agent directory or profiles, no parent reviews, no monthly trend series, no street-address suggestions (places only), no Spanish pages, no tour, contact or financing forms.

Movoto offers no public developer API. This skill reads Movoto's public pages with one Scavio key. Listing data comes from the MLS that supplies each listing (`mls_id`, `mls_name`).

See also: `zillow-property-data`, `redfin-property-data`, `realtor-com-property-data`, `trulia-api` (neighborhood surveys and reviews), `streeteasy-api` (New York City) and `rent-com-api` / `rentcafe-api` (US rentals). Same home or same area only: match on address or place, name the site and date with every number.

## When to trigger

Use this skill when the user asks to:
- Read a US city's or ZIP code's housing market trends on Movoto: median list price, price per square foot, days on market, inventory and home size, today, a month ago and a year ago, for all homes, single-family and condos
- Compare a city with its nearby cities, or a ZIP code with nearby ZIP codes, on Movoto's market figures
- Search Movoto homes for sale, sold (with a sold window) or for rent by city, ZIP code, county, neighborhood or school zone, with property-type, beds, baths, price, size, lot, year-built, HOA, days-on-market, garage, pool, open-house, price-reduced, new-listing, new-construction or foreclosure filters
- Read one Movoto home in full: price history, tax history, features, HOA, Movoto's area-based estimate, schools, local scores and nearby sold, for-sale and rental homes
- Read one school on Movoto with its GreatSchools rating, state rating and test scores, and find the homes zoned for it
- Look up the cities, ZIP codes, neighborhoods, counties and school ids Movoto uses

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=movoto-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=movoto-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example 25 cities: one market-trends call and one search each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, suggestions answered in 1-3.3 seconds, school 1.8-3.1, market trends 1.9-5.5, property 1.5-7.4 and search 1.3-9.7. Set a client timeout of at least 180 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/movoto/search` | Homes for sale, sold or for rent in a city, ZIP code, county, neighborhood or school zone: 50 a page to page 99, 8 sorts, filters, total and paging; each home with price, sold price and date, beds, baths, size, lot, year built, HOA, days on Movoto, price change, open houses, MLS number and brokerage; plus the area's market summary, market snapshot, facet counts, top ZIP codes, top neighborhoods and nearby cities | 1 |
| `POST /api/v1/movoto/property` | One home (for sale, sold or for rent) by link or path: description, features, price history, tax history, Movoto's area-based estimate, key insights, schools with GreatSchools ratings, school districts, area trends (city, ZIP, neighborhood, county), local scores, nearby sold, for-sale, new and rental homes, photos | 1 |
| `POST /api/v1/movoto/market-trends` | A city's or ZIP code's market trends: Movoto's summary, snapshots for today, one month ago and one year ago (all, single-family, condo), stat cards, the nearby cities or ZIP codes compared, an overview of counts and, for a ZIP, Movoto's daily statistics | 1 |
| `POST /api/v1/movoto/suggestions` | Place suggestions (city, ZIP code, neighborhood, county, school) with Movoto's listing count and the `search` input for each place | 1 |
| `POST /api/v1/movoto/school` | One school by link or path: GreatSchools rating, state rating, teacher-student ratio, test scores by grade and subject, district, nearby schools, up to 10 zoned homes and the search input for every home zoned for it | 1 |

## Market

US only, USD. There is no `country`, `currency` or `language` input. Rentals carry the monthly rent in `price`.

## Market trend fields

| Field | Meaning |
|---|---|
| `snapshots.today`, `snapshots.one_month_ago`, `snapshots.one_year_ago` | {`date`, `all`, `single_family`, `condo`}; each type {`median_list_price`, `median_price_per_sqft`, `median_days_on_market`, `median_home_sqft`, `inventory`, `change_1m_percent`, `change_1y_percent`} |
| `change_1m_percent`, `change_1y_percent` | Movoto's rounded percent changes per measure (on `today`): Los Angeles median list price -4 over a year |
| `summary` | Movoto's own sentence ("The median home price in Los Angeles is $1,049,000, down 4.6% year-over-year. ...") |
| `stat_cards[]`, `by_type` | {`id`, `title`, `value`, `change`, `direction`} as Movoto prints them ("$1.05M", "4.6% YoY", "down") |
| `compare` | {`label` (Cities or Zip Codes), `rows[]` {`name`, `current`, `median_price`, `yoy_change_percent`, `price_per_sqft`, `days_on_market`, `active_homes`, `url`}} |
| `overview[]` | {`label`, `count`, `url`}: Active Homes, New Homes (last 7 days), Open Houses, Price Reduced |
| `daily` | ZIP codes only (with `include_daily`, default true): Movoto's daily statistics, same shape as `snapshots` |
| `market_summary` (search) | {`homes_for_sale`, `average_list_price`, `median_price_per_sqft`, `min_list_price`, `max_list_price`, `new_listings`, `open_houses`, `price_reduced`, `new_construction`, `with_pool`, `condos`, `single_family`, `schools`} |

- **Two percents.** `change_1y_percent` is rounded to a whole number (-4); `stat_cards` and `compare` carry Movoto's one-decimal figure (-4.6%). Quote whichever you use with its label.
- **Two counts.** `market_summary.homes_for_sale` (6,009 in Austin), `snapshots.today.all.inventory` (6,472) and the search `total` (5,885) are different Movoto counts; quote each with its label.

## Workflow

1. **Places.** `/suggestions` (`{"query": "Austin"}`): each place carries `search`, the exact input for `/search` (`{"city": "Austin", "state": "TX"}`, `{"neighborhood": "East Austin", "city": "Austin", "state": "TX"}`, `{"county": "Austin County", "state": "TX"}`, `{"school_id": "4825212", "city": "Austin", "state": "TX"}`).
2. **The market.** `/market-trends` with `city` + `state` or `zip`. Note `snapshots`, `compare` and `last_updated`.
3. **Homes in it.** `/search` with the place, `status` and filters. Check `notes` for a filter Movoto did not apply or a place it answered differently.
4. **One home.** `/property` with `path` from `listings[]`. Its `schools[].url` leads to step 5.
5. **Schools.** `/school` with `url`; `zone_search` is the `/search` input for every home zoned for it.
6. **Report.** Each figure with Movoto, the place, USD and the `fetched_at` date; list prices labeled as list prices; `estimate` labeled as Movoto's area-based estimate; no verdict on the market or a home.
7. **Over time:** store each answer with its `fetched_at`; Movoto updates its figures daily, and that stored set is your series.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `city` + `state` | string | one place required | A US city (up to 80 characters) and its two-letter state code (`Austin`, `TX`) |
| `zip` | string | one place required | Or a five-digit ZIP code (`78704`); `state` optional |
| `county` + `state` | string | one place required | Or a county (`Travis` or `Travis County`) with state |
| `neighborhood` + `city` + `state` | string | one place required | Or a neighborhood (suggestions returns the names) |
| `school_id` + `city` + `state` | string or integer | one place required | Or the homes zoned for one school: a Movoto school id (4-10 digits, `4800595`) |
| `status` | string | `for_sale` | `for_sale`, `sold` or `rentals` |
| `sold_within` | string | every sale Movoto lists | `sold` only: `1w`, `1m`, `3m`, `6m`, `1y` or `2y` |
| `hide_pending` | boolean | false | `for_sale` only: leave out pending and contingent homes |
| `property_types` | list | none | Any of `single_family`, `condo`, `multi_family`, `land`, `mobile`, `other` |
| `beds_min`, `beds_max`, `baths_min`, `baths_max` | integer | none | 0-20 |
| `price_min`, `price_max` | integer | none | USD (monthly rent on rentals) |
| `sqft_min`, `sqft_max` | integer | none | Living area, 0-1,000,000 square feet |
| `lot_sqft_min`, `lot_sqft_max` | integer | none | Lot size, square feet |
| `year_built_min`, `year_built_max` | integer | none | 1700 to two years ahead |
| `hoa_min`, `hoa_max` | integer | none | Monthly HOA fee, USD (`for_sale` and `sold` only) |
| `days_on_market_min`, `days_on_market_max` | integer | none | 0-3650 days on Movoto (`for_sale` and `rentals` only) |
| `garage_min` | integer | none | 1-10 garage spaces |
| `pool` | boolean | false | Homes whose listing mentions a pool |
| `open_houses`, `price_reduced`, `new_listings`, `new_construction`, `foreclosed` | boolean | false | `for_sale` only: an open house scheduled, price reduced in the last 30 days, listed in the last 7 days, new construction, foreclosures |
| `sort` | string | `relevant` | `relevant` (Movoto's default), `newest` (list date), `updated`, `price_low`, `price_high`, `sqft_large`, `sqft_small`, `price_per_sqft` (lowest first) |
| `page` | integer | 1 | 1-500, 50 homes a page; Movoto serves up to 99 pages, a page past the last is empty with a note |

### Market trends (`/market-trends`), property (`/property`), school (`/school`), suggestions (`/suggestions`)

| Endpoint | Parameters |
|---|---|
| `/market-trends` | `city` + `state`, or `zip` (`state` optional); `include_daily` (boolean, default true: with `zip`, add Movoto's daily statistics, same 1 credit) |
| `/property` | one of `url` (a movoto.com property link, `listings[].url`) or `path` (`listings[].path`, `austin-tx/12901-sherbourne-st-austin-tx-78729/pid_vgz5rxm5nh/`) |
| `/school` | one of `url` (a movoto.com school link, `schools[].url` on a property) or `path` (`schools/<city-st>/<school>-<id>/`) |
| `/suggestions` | `query` (2-80 characters: the start of a city, ZIP code, neighborhood, county or school name); `types` (any of `city`, `zipcode`, `neighborhood`, `county`, `school`) |

## Examples

### A city's market trends

```bash
curl -X POST https://api.scavio.dev/api/v1/movoto/market-trends \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"city": "Los Angeles", "state": "CA"}'
```

Captured `data` (2026-11-26; `single_family` and `condo` dropped from each snapshot, `one_month_ago` dropped, `stat_cards` cut to 2 of 4, `compare.rows` to 2, `by_type`, `overview`, `url` and the compare `url`s dropped):

```json
{
  "location": {"type": "city", "name": "Los Angeles", "city": "Los Angeles", "state": "CA", "county": "Los Angeles County", "zip": null},
  "last_updated": "November 26, 2026",
  "summary": "The median home price in Los Angeles is $1,049,000, down 4.6% year-over-year. Median price per square foot is down 4.4% at $652/sq. ft. Homes are selling in 72 days on average, the same as last year. As of November 26, 2026, there are 5,037 active listings on the market, with 547 new listings in the last 7 days.",
  "snapshots": {
    "today": {
      "date": "2026-11-26",
      "all": {
        "median_list_price": 1049000, "median_price_per_sqft": 652, "median_days_on_market": 72, "median_home_sqft": 1703, "inventory": 5037,
        "change_1m_percent": {"median_list_price": 0, "median_price_per_sqft": 0, "median_days_on_market": -1, "median_home_sqft": 0, "inventory": 0},
        "change_1y_percent": {"median_list_price": -4, "median_price_per_sqft": -4, "median_days_on_market": 0, "median_home_sqft": -1, "inventory": 3}
      }
    },
    "one_year_ago": {
      "date": "2025-10-31",
      "all": {"median_list_price": 1100000, "median_price_per_sqft": 682, "median_days_on_market": 72, "median_home_sqft": 1729, "inventory": 4859}
    }
  },
  "stat_cards": [
    {"id": "medianprice", "title": "Median home price", "value": "$1.05M", "change": "4.6% YoY", "direction": "down"},
    {"id": "inventory", "title": "Active homes", "value": "5,037", "change": "3.7% YoY", "direction": "up"}
  ],
  "compare": {
    "label": "Cities",
    "rows": [
      {"name": "Los Angeles", "current": true, "median_price": 1049000, "yoy_change_percent": -4.6, "price_per_sqft": 652, "days_on_market": 72, "active_homes": 5037},
      {"name": "East Los Angeles", "current": false, "median_price": 727000, "yoy_change_percent": 11.1, "price_per_sqft": 500, "days_on_market": 82, "active_homes": 7}
    ]
  },
  "notes": ["Medians, inventory and days on market are Movoto's figures for homes listed for sale, as Movoto publishes them: today, one month ago and one year ago (no monthly series). Prices in USD."]
}
```

A ZIP code (`{"zip": "78704"}`) answers the same shape with `compare.label` "Zip Codes" (78701 at $675,000 and -14.4%, 78702 at $650,000 and -6.5% next to 78704 at $750,000 and -8.5%) and `daily`, Movoto's daily statistics for the ZIP.

### Search homes for sale in a city

```bash
curl -X POST https://api.scavio.dev/api/v1/movoto/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"city": "Austin", "state": "TX"}'
```

Captured `data` (2026-11-26; `listings` cut to 1 of 50 and its `url` and `photo` dropped, `market_snapshot`, `facet_counts`, `top_zips`, `top_neighborhoods`, `nearby_cities` and `url` dropped):

```json
{
  "status": "for_sale",
  "sold_within": null,
  "location": {"type": "city", "city": "Austin", "state": "TX", "name": "Austin, TX", "county": "Travis County", "latitude": 30.2986219, "longitude": -97.7541339},
  "sort": "relevant",
  "page": 1,
  "page_size": 50,
  "total": 5885,
  "pages": 99,
  "has_more": true,
  "count": 50,
  "listings": [
    {
      "id": "23ce1aa8-5669-434a-baf7-eb4f25e99049",
      "property_id": "b2112314-bff0-4177-99c6-0a8c5b4c69df",
      "path": "austin-tx/12901-sherbourne-st-austin-tx-78729/pid_vgz5rxm5nh/",
      "status": "Active",
      "status_code": "ACTIVE",
      "is_sold": false,
      "is_rental": false,
      "price": 649029,
      "sold_price": null,
      "currency": "USD",
      "sold_date": null,
      "list_date": "2026-11-06",
      "days_on_movoto": 0,
      "price_change": null,
      "price_changed_date": "2026-11-26",
      "beds": 4,
      "baths": 3,
      "sqft": 2000,
      "lot_sqft": 12702,
      "year_built": 1973,
      "hoa_fee_monthly": 2,
      "garage_spaces": 2,
      "property_type": "SINGLE_FAMILY_HOUSE",
      "property_type_label": "Residential - Single Family",
      "mls_number": "8087683",
      "mls_id": 404,
      "brokerage": "Compass RE Texas, LLC",
      "address": {"street": "12901 Sherbourne St", "unit": null, "city": "Austin", "state": "TX", "zip": "78729", "county": "Williamson County", "neighborhood": "Pond Springs", "full": "12901 Sherbourne St Austin, TX 78729"},
      "latitude": 30.456081,
      "longitude": -97.779183,
      "photo_count": 35,
      "open_houses": [{"date": "2026-11-28", "start_time": "13:00:00", "end_time": "15:00:00"}],
      "has_3d_tour": false,
      "has_video_tour": false
    }
  ],
  "market_summary": {"homes_for_sale": 6009, "average_list_price": 596041, "median_price_per_sqft": 283, "min_list_price": 24000, "max_list_price": 22000000, "new_listings": 270, "open_houses": 261, "price_reduced": 1369, "new_construction": 989, "with_pool": 2158, "condos": 1432, "single_family": 3768, "schools": 380},
  "notes": ["Prices are in USD as Movoto shows them. Listing data comes from the MLS that supplies each listing (mls_id)."]
}
```

Other captured searches: `{"city": "Los Angeles", "state": "CA", "status": "sold", "sold_within": "1m"}` matched 935 homes sold in the last month (19 pages), the first sold at $690,000 on 2026-11-25 with `sold_price` filled; `{"city": "Austin", "state": "TX", "status": "rentals", "beds_min": 2}` matched 3,866 rentals, the first a 3-bed condo at $1,637 a month, with the note that `market_summary` stays the for-sale figures; `{"zip": "10001"}` (no state) answered New York, NY with 114 homes, the first a 3-bed condo at $5,595,000 with an $8,809 monthly HOA fee; `{"school_id": "4800595", "city": "Austin", "state": "TX"}` returned the 33 homes zoned for Davis Elementary School.

### One home

```bash
curl -X POST https://api.scavio.dev/api/v1/movoto/property \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"path": "austin-tx/12901-sherbourne-st-austin-tx-78729/pid_vgz5rxm5nh/"}'
```

Captured `data` (2026-11-26; the card fields shown in search dropped, `price_history` cut to 4 of 7, `tax_history` to 2 of 9, `schools` to 1 of 3; `description`, `features`, `area_trends`, `city_market_snapshot`, `nearby`, `photos` and the URLs dropped):

```json
{
  "price": 649029,
  "on_market_date": "2026-11-06",
  "mls_name": "Unlock MLS",
  "price_history": [
    {"date": "2026-11-06", "event": "Listed", "price": 649029, "change_percent": 52.7, "source": "MLS", "mls_number": "8087683", "is_rental": false},
    {"date": "2026-08-14", "event": "Pending", "price": null, "change_percent": null, "source": "MLS", "mls_number": "6027393", "is_rental": false},
    {"date": "2026-08-06", "event": "Active", "price": null, "change_percent": null, "source": "MLS", "mls_number": "6027393", "is_rental": false},
    {"date": "2026-07-30", "event": "Price Change", "price": 425000, "change_percent": -4.3, "source": "MLS", "mls_number": "6027393", "is_rental": false}
  ],
  "tax_history": [
    {"year": 2023, "tax": 1236.61, "assessed_total": 457811, "assessed_land": 105500, "assessed_improvements": 356692, "tax_rate_percent": 0.27},
    {"year": 2022, "tax": 2625.5, "assessed_total": 445150, "assessed_land": 115000, "assessed_improvements": 330150, "tax_rate_percent": 0.59}
  ],
  "estimate": {"label": "Movoto's area-based estimate", "value": 542780, "currency": "USD", "range_text": "$488K - $598K", "area_price_per_sqft": 271, "area_price_per_sqft_low": 244, "area_price_per_sqft_high": 299, "sqft": 2000, "difference_percent": 16.37, "estimate_above_price": false},
  "schools": [
    {"id": "4805891", "name": "Mcneil High School", "rating": 7, "level": "9-12", "type": "public"}
  ],
  "local_scores": {"food": 80, "pet": 93, "walk": 55, "kid": 71},
  "updated": {"last_updated": "2026-11-26 17:47:27", "last_checked": "2026-11-26 18:49:06"},
  "notes": [
    "Prices are in USD as Movoto shows them. Listing data comes from the MLS that supplies the listing (mls_name).",
    "estimate is Movoto's area-based estimate: the area's price per square foot times this home's size, as Movoto shows it. It is not an appraisal.",
    "School ratings are GreatSchools ratings (1-10) as Movoto shows them."
  ]
}
```

The price history shows the home listed at $649,029 on 2026-11-06 after a $425,000 price change in July (+52.7%, Movoto's figure). A sold Los Angeles home read `price` 1,149,000, `sold_price` 1,140,000 and `sold_date` 2026-11-25 with an estimate of $1,059,647; a rental reads the monthly rent in `price` and `estimate` null.

### School and suggestions

- `/school` `{"path": "schools/austin-tx/davis-elementary-school-480894022775/"}`: Davis Elementary School, PK and K-5, public, Austin Independent School District (122 schools), `rating` 6, `state_rating` {"rating": 6, "year": 2024}, teacher-student ratio 1:12, STAAR test scores by grade and subject, 10 `zone_homes`, 20 nearby schools and `zone_search` {"school_id": "4800595", "city": "Austin", "state": "TX"}.
- `/suggestions` `{"query": "Austin"}`: 16 places: Austin, TX (6,610 listings, `search` {"city": "Austin", "state": "TX"}), Austin, MN (175), Austin, AR (108), Austintown, OH, Austin, CO; the neighborhoods Central Austin (967), East Austin (847) and three more; Austin County, TX (639); and schools with their `school_id`. Street addresses are not suggested.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def movoto(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/movoto/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# The market for a ZIP code (1 credit)
t = movoto("market-trends", {"zip": "78704"})["data"]
now, year = t["snapshots"]["today"], t["snapshots"]["one_year_ago"]
print(t["location"]["name"], now["date"], now["all"]["median_list_price"], "vs", year["date"], year["all"]["median_list_price"])
for row in t["compare"]["rows"][:5]:
    print(" ", row["name"], row["median_price"], row["yoy_change_percent"], row["active_homes"])

# Homes for sale in it, newest first (1 credit)
s = movoto("search", {"zip": "78704", "sort": "newest", "beds_min": 3})["data"]
print("total", s["total"], "pages", s["pages"])
for h in s["listings"][:5]:
    print(h["path"], h["price"], h["beds"], h["baths"], h["sqft"], h["brokerage"])

# One home with its price and tax history (1 credit)
p = movoto("property", {"path": s["listings"][0]["path"]})["data"]
for e in p["price_history"]:
    print(e["date"], e["event"], e["price"])

# Store each answer with fetched_at: that stored set is your series.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every answer carries `notes`.

- **home card** (search `listings[]`, a school's `zone_homes[]`) - `id`, `property_id`, `url`, `path` (the input of property), `status`, `status_code`, `is_sold`, `is_rental`, `price` (USD; monthly rent on rentals), `sold_price` (null in non-disclosure states such as Texas), `currency`, `sold_date`, `list_date`, `days_on_movoto`, `price_change`, `price_changed_date`, `beds`, `baths`, `sqft`, `lot_sqft`, `year_built`, `hoa_fee_monthly`, `garage_spaces`, `property_type`, `property_type_label`, `mls_number`, `mls_id`, `brokerage`, `address` {`street`, `unit`, `city`, `state`, `zip`, `county`, `neighborhood`, `full`}, `latitude`, `longitude`, `photo`, `photo_count`, `open_houses[]` {`date`, `start_time`, `end_time`}, `has_3d_tour`, `has_video_tour`.
- **search** - `status`, `sold_within`, `location` {`type`, `city`, `state`, `zip`, `name`, `county`, `latitude`, `longitude`}, `url`, `sort`, `page`, `page_size`, `total`, `pages`, `has_more`, `count`, `listings[]`, `market_summary`, `market_snapshot` {`today`, `one_month_ago`, `one_year_ago`}, `facet_counts` {`beds`, `baths`, `price_ranges`, `amenities`: [{`filter`, `label`, `count`}]}, `top_zips[]` {`zip`, `city`, `state`, `median_list_price`, `url`}, `top_neighborhoods[]` and `nearby_cities[]` {`name`, `city`, `state`, `median_list_price`, `url`}, `notes`.
- **property** - the card fields plus `on_market_date`, `building_name`, `mls_name`, `neighborhood_url`, `description` (phone numbers and emails removed), `features[]` {`category`, `group`, `name`, `value`}, `price_history[]` {`date`, `event`, `price`, `change_percent`, `source`, `mls_number`, `is_rental`}, `tax_history[]` {`year`, `tax`, `assessed_total`, `assessed_land`, `assessed_improvements`, `tax_rate_percent`}, `estimate` {`label`, `value`, `currency`, `range_text`, `area_price_per_sqft`, `area_price_per_sqft_low`, `area_price_per_sqft_high`, `sqft`, `difference_percent`, `estimate_above_price`} (null on rentals), `key_insights[]` {`title`, `detail`, `text`}, `schools[]` {`id`, `name`, `rating`, `level`, `type`, `url`}, `school_districts[]` {`name`, `nces_id`, `url`}, `area_trends` {`city`, `zip`, `neighborhood`, `county`}, `city_market_snapshot`, `local_scores` {`food`, `pet`, `walk`, `kid`}, `local_highlights`, `nearby` {`sold`, `for_sale`, `new_construction`, `rentals`: {`total`, `homes[]`}}, `photos[]` {`url`, `tag`}, `updated` {`last_updated`, `last_checked`}, `notes`.
- **market trends** - `location` {`type`, `name`, `city`, `state`, `county`, `zip`}, `url`, `last_updated`, `summary`, `snapshots`, `stat_cards[]`, `by_type` {`all`, `single_family`, `condo`}, `compare` {`label`, `rows[]`}, `overview[]` {`label`, `count`, `url`}, `daily` (ZIP codes), `notes`.
- **suggestions** - `query`, `count`, `places[]` {`type` (city, zipcode, neighborhood, county, school), `name`, `full_name`, `city`, `county`, `state`, `zip`, `neighborhood`, `school_id`, `listings`, `geo_id`, `latitude`, `longitude`, `search`}, `notes`.
- **school** - `id`, `nces_id`, `name`, `url`, `level`, `type`, `address`, `latitude`, `longitude`, `district` {`id`, `name`, `nces_id`, `url`, `school_count`}, `rating`, `state_rating` {`rating`, `year`}, `teacher_student_ratio`, `tests[]` {`name`, `abbreviation`, `description`, `grades[]` {`grade`, `subjects[]` {`name`, `scores` {year: percent}}}}, `zone_homes[]`, `zone_search` {`school_id`, `city`, `state`, `url`}, `nearby_schools[]` {`id`, `name`, `rating`, `level`, `type`, `distance_miles`, `url`}, `notes`.

## Guardrails

- Name it "Movoto (movoto.com, the US home search site owned by Lower)" on first mention, "Movoto" after that.
- Market figures: always "Movoto's market trends" with the place, its type (city or ZIP code), the measure, the snapshot date and the `fetched_at` date ("Movoto's median list price for Los Angeles was $1,049,000 on Nov 26, 2026, against $1,100,000 on Oct 31, 2025"). They describe homes listed for sale: never call them sale prices or home values.
- Prices: USD with Movoto, the address or path and the `fetched_at` date. `estimate` is "Movoto's area-based estimate", never an appraisal or what a home is worth. Where `sold_price` is null, say the sale price is not public in that state; do not fill it from the list price.
- Schools: ratings, state ratings and test scores are "GreatSchools data as Movoto shows them".
- Fair housing: describe places with the data as Movoto gives it; do not characterize an area by who lives there, and do not steer anyone toward or away from an area.
- No agent personal data: name the brokerage company only, and do not try to identify a listing agent, a seller or an owner.
- Descriptive only: no commentary on Movoto's business, pricing practices or policies.
- Do not republish Movoto photos or listing descriptions in bulk. Write movoto.com as plain text and cite paths, MLS numbers and capture dates rather than linking Movoto pages.
- Terms: Scavio keeps no copy: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no lead, tour or contact flow. Movoto's terms of use and each MLS's listing terms cover how the site and its data may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, medians, percents, paths, school ids or ratings. Only return what the API returned, with the `fetched_at` time.
- Not available: agent names, phones or profiles, parent reviews, monthly trend series, street-address suggestions, Spanish pages, tours, contact or financing.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: no place ("a place is required: send city + state, zip, county + state, neighborhood + city + state or school_id + city + state."); two places at once ("zip is a place of its own: ...", "county is a place of its own: ...", "send neighborhood or school_id, not both: ..."); a bad state ("state must be a two-letter US state code (e.g. TX).") or ZIP ("zip must be a five-digit US ZIP code (e.g. 78704)."); `sold_within` without `sold` ("sold_within is a sold filter: send it with status sold."); a for-sale filter on another status ("open_houses is a for-sale filter: send it with status for_sale."); `hoa_min` / `hoa_max` on rentals ("hoa_min / hoa_max filter homes for sale and sold homes, not rentals."); `days_on_market` on sold ("days_on_market filters homes on the market: use sold_within with status sold."); a `_min` above its `_max`; a value outside its list; `/property` or `/school` without exactly one of `url` or `path` ("send one of url or path."), or a link that is not Movoto's ("url must be a Movoto property link (https://www.movoto.com/<city-st>/<address>/<id>/), path its path (search listings[].path)."); suggestions under 2 characters.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Movoto has no search page for this place. Check the city / state, ZIP, county or neighborhood (suggestions returns search inputs).", "Movoto has no listing at this link. Use listings[].url or listings[].path from search.", "Movoto publishes no market trends for this place. Send a city + state or a ZIP code.", "Movoto has no school at this link. Use schools[].url from property.", "Movoto does not know ZIP code <zip>." (on a ZIP sent without a state). Take places from `/suggestions` and paths from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=movoto-api).
- `502` means Movoto data was temporarily unavailable ("Movoto is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Movoto is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.98.0
npm install scavio@0.99.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: trends } = await scavio.movoto.marketTrends({ city: "Los Angeles", state: "CA" });
const { data: homes } = await scavio.movoto.search({ city: "Austin", state: "TX", beds_min: 3, price_max: 750000 });
const { data: home } = await scavio.movoto.property({ path: "austin-tx/12901-sherbourne-st-austin-tx-78729/pid_vgz5rxm5nh/" });
const { data: school } = await scavio.movoto.school({ path: "schools/austin-tx/davis-elementary-school-480894022775/" });
const { data: places } = await scavio.movoto.suggestions({ query: "Austin" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.movoto.search(...)`, `property`, `market_trends`, `suggestions` and `school`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 5 endpoints as tools: `search_movoto`, `get_movoto_property`, `get_movoto_market_trends`, `get_movoto_suggestions` and `get_movoto_school`. Movoto is opt-in: add `movoto` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.98.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,movoto"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/movoto-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=movoto-api), [property](https://scavio.dev/docs/movoto-property?utm_source=agent-skills&utm_medium=skill&utm_campaign=movoto-api), [market trends](https://scavio.dev/docs/movoto-market-trends?utm_source=agent-skills&utm_medium=skill&utm_campaign=movoto-api), [suggestions](https://scavio.dev/docs/movoto-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=movoto-api), [school](https://scavio.dev/docs/movoto-school?utm_source=agent-skills&utm_medium=skill&utm_campaign=movoto-api). Overview: [Movoto API](https://scavio.dev/movoto-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=movoto-api).
