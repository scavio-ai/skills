# Trulia API - Neighborhood Reviews, Home Listings, Market Data

Read Trulia (trulia.com, Zillow Group's US home and neighborhood site): a neighborhood's What Locals Say survey, safety statements, resident reviews, amenities, schools and market snapshot; home search for sale, for rent or recently sold; one home or one rental building in full; one school; and place suggestions. Every answer is what Trulia's public pages show a visitor without an account at the moment of the call, in USD. All 5 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Trulia shows to any visitor and returns them as JSON for analysis. It uses no Trulia account, no saved homes, no tour or contact request, no lead form and no financing flow.

**The job this skill is for: what locals say about a neighborhood, next to what its market is doing.** `/neighborhood` returns Trulia's What Locals Say survey (16 statements, each the share of respondents who agreed), the safety statements, the resident reviews with their category counts, and Trulia's market snapshot for the neighborhood (or for its city, where Trulia scopes it that way), all in one call. Captured 2026-11-26 (1 credit per call):

| Neighborhood (`location_id`) | Survey `minimum_responses` | "People would walk alone at night" | Resident reviews (`total` / `shown`) | Market snapshot, October 2026 (`scope`: avg sale price, sale-to-list, condition, temperature index) |
|---|---|---|---|---|
| Upper East Side, New York, NY (85381) | 1,480 | 84% | 277 / 40 | neighborhood: $1.47M, 98.2%, NEUTRAL_MARKET, 52 |
| Gravesend, New York, NY (85244) | 969 | 60% | 112 / 40 | city (New York): $822K, 98.2%, NEUTRAL_MARKET, 50 |
| Fremont, Seattle, WA (86943) | 96 | 81% | 26 / 21 | city (Seattle): $835K, 99.6%, BUYERS_MARKET, 36 |
| Brentwood, Austin, TX (86214) | 34 | 80% | 36 / 33 | city (Austin): $567K, 97.4%, BUYERS_MARKET, 34 |
| Boyle Heights, Los Angeles, CA (87374, `language: "es"`) | 519 | 36% ("La gente caminaría sola por la noche") | 84 / 40 | city (Los Angeles): $1M, 99.3%, BUYERS_MARKET, 39 |

The survey figures are Trulia's survey results, the share of respondents who agreed with each statement as Trulia shows it; they are not a crime rate, a safety rating or Scavio's assessment of the neighborhood. Quote each with its statement text, its percent and the response count, and say when the market snapshot is the city's rather than the neighborhood's. For listings in the same area use `/search` (Trulia) or `zillow-property-data`, `redfin-property-data` and `realtor-com-property-data`, matched on location, beds and property type.

Ten limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent; a neighborhood with its market snapshot is still 1 credit. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Survey results, not crime data.** `what_locals_say` and `safety` are Trulia's resident survey (`percent` = share who agreed, `minimum_responses` = the response count Trulia gives). Trulia no longer publishes crime data, and no endpoint returns any.
- **Up to 40 resident reviews.** Trulia's neighborhood page shows up to 40 reviews (`reviews.shown`, in Trulia's order); `reviews.total` and the per-category counts cover all of them. There is no way to page past those 40. No reviewer name is returned, only `reviewer_type` (Resident, Prev. Resident).
- **The market snapshot names its scope.** `market.snapshot.scope` is `neighborhood` or `city`: where Trulia shows a city-wide market for a neighborhood, `area` is the city and a note says so (Gravesend reads New York's). Trulia publishes the snapshot on home pages, so it is read from one home for sale in the neighborhood (`market.read_from`); with no home for sale, or a snapshot for another area, `market` is `null` and a note says why. `include_market_snapshot: false` skips it and answers faster.
- **Search is 40 homes a page, to page 50.** That is up to 2,000 homes per query; `total` can be higher (Austin for sale, 3+ beds, under $600,000: 2,146). Narrow the location or filters to reach the rest. Trulia drops a filter it cannot read: `applied_filters` echoes what Trulia applied and a note lists what it did not.
- **Prices as Trulia shows them.** USD; rentals per month; a rental building has `price_min` / `price_max` and a `price_note` such as "Total price" (base rent plus the monthly fees the owner lists as required). Sold rows carry the sale price Trulia prints. `zestimate` and `rent_zestimate` are Zillow's estimates as Trulia shows them, not appraisals; `payment_estimate` and `price_vs_median` are read from Trulia's own FAQ answers on the page.
- **Spanish where Trulia publishes it.** `language: "es"` works on rental searches (`listing_status: "for_rent"`), rental buildings and neighborhoods; anywhere else it is a `400`. Survey statements and labels come in Spanish; review text stays as residents wrote it, and `reviewer_type` can come as Trulia's raw label ("revisión del vecindario.contexto.residente actual" on the Boyle Heights capture).
- **No agent personal data.** No listing-agent names, phones, emails or license numbers, and no reviewer names. `brokerage` is the company name. Sentences in a listing description that credit the listing to someone or carry contact details are removed.
- **Slow pages.** In the captures search answered in 2.8 to 45 seconds, a home or building page in 2 to 29, a neighborhood in 3 to 14 (with its market snapshot), a school in 2 to 8 and suggestions in 1 to 3. Set a client timeout of at least 240 seconds and send one request at a time.
- **What is not there.** No crime data, no agent directory or agent profiles, no Trulia market-trends pages (they no longer exist on Trulia), no neighborhood reviews past 40, no walk or transit scores, no tour, contact or financing forms.

Trulia's former public developer API is retired and issues no keys. This skill reads Trulia's public pages with one Scavio key.

See also: `zillow-property-data` (Zillow search, property and agent pages; Trulia and Zillow share the same `zpid`), `redfin-property-data`, `realtor-com-property-data`, `streeteasy-api` (New York City listings, buildings and StreetEasy's market data), `rent-com-api` and `rentcafe-api` (US rental listings). Same home or same area only: match on zpid or address, name the site and date with every number.

## When to trigger

Use this skill when the user asks to:
- Read what locals say about a US neighborhood on Trulia: the What Locals Say survey, safety statements and resident reviews by category
- Get a neighborhood's market snapshot on Trulia (average sale price, sale-to-list ratio, price per square foot, active listings, market condition) and its monthly median sale price since 2018
- List a neighborhood's amenities, schools with GreatSchools ratings, commute time, home counts and price ranges, boundary or nearby neighborhoods
- Search Trulia homes for sale, for rent or recently sold by ZIP, city or neighborhood, with beds, baths, price, size, year-built, HOA, property-type, keyword or pet filters
- Read one Trulia home in full (price and tax history, Zestimate and rent estimate as Trulia shows them, features, payment estimate) or one rental building (floor plans, available units, fees, pet policy)
- Read one school on Trulia with its GreatSchools sub-ratings, parent reviews and assigned homes
- Look up the place names, neighborhood ids and school ids Trulia uses

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=trulia-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=trulia-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example 25 neighborhoods: one suggestions lookup and one neighborhood page each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, suggestions answered in 1-3 seconds, school 2-8, neighborhood 3-14 (with its market snapshot), property 2-29 and search 2.8-45. Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/trulia/neighborhood` | One neighborhood by location id or link: What Locals Say survey (16 statements), safety statements, resident reviews (up to 40, category counts, no names), facts (home counts, price ranges, commute), amenities, schools, boundary, nearby neighborhoods, homes for sale, market snapshot and monthly median sale price history | 1 |
| `POST /api/v1/trulia/search` | Homes for sale, for rent or recently sold in a ZIP, city or neighborhood: 40 a page, 7 sorts, filters, `applied_filters`, total and paging; each home with price, beds, baths, size, type, tags, dates and brokerage | 1 |
| `POST /api/v1/trulia/property` | One home by zpid or link (price and tax history, Zestimate and rent estimate as Trulia shows them, home value trend, features, payment estimate, price vs median, neighborhood market) or one rental building by id (floor plans with units, fees, pet policy, special offers, unit counts) | 1 |
| `POST /api/v1/trulia/school` | One school by link or id and state: GreatSchools rating and sub-ratings, ratios, parent reviews (no names), nearby schools, assigned homes for sale and for rent | 1 |
| `POST /api/v1/trulia/suggestions` | Place suggestions (city, neighborhood, ZIP, county, address) with `location_id`, `zpid` and `search_location`, plus matching schools and districts | 1 |

## Market

US only, USD. There is no `country` or `currency` input. `language` is `en` (default) or `es` (Trulia's US Spanish pages), and Spanish exists on rental searches, rental buildings and neighborhoods only.

## Survey, reviews and market fields

| Field | Meaning |
|---|---|
| `what_locals_say.statements[]` | {`type`, `statement`, `percent`}: Trulia's 16 survey statements ("It's walkable to grocery stores", "Parking is easy", "They plan to stay for at least 5 years"), each the share of respondents who agreed |
| `what_locals_say.minimum_responses`, `safety.minimum_responses` | The response count Trulia gives for the survey |
| `safety.statements[]` | The 3 safety statements ("There are sidewalks", "Streets are well-lit", "People would walk alone at night") with their percent |
| `reviews` | {`total`, `shown`, `categories[]` {`id`, `name`, `count`}, `items[]` {`id`, `text`, `category`, `category_name`, `reviewer_type`, `date`, `helpful`}}; categories are General, Community, Dog Owners, Parents, Commute |
| `facts` | {`homes_for_sale`, `homes_for_rent`, `for_sale_price_range`, `for_rent_price_range` {`min`, `max`, `display`}, `commute` {`destination`, `minutes`}} as Trulia states them |
| `market.snapshot` | {`scope`, `area`, `last_updated`, `avg_sale_price`, `sale_to_list_ratio`, `price_per_sqft`, `active_listings` (each {`value`, `display`, `mom_change`, `mom_direction`}), `market_condition`, `market_temperature_index`, `source`} |
| `market.median_sale_price_history` | {`scope`, `area`, `last_updated`, `points[]` {`month`, `median_sale_price`}}: monthly, from Jun 2018 on the captures |
| `market.read_from` | The home for sale (`zpid`, `url`) the snapshot was read from |

- **Two home counts.** `facts.homes_for_sale` is Trulia's neighborhood fact (1,885 on the Upper East Side) and `homes_for_sale.total` the count on its home list (1,238); quote each with its label.
- **Month-over-month:** `mom_change` and `mom_direction` are Trulia's ("$50K", "up"). Any other change you compute, label as computed.

## Workflow

1. **Names and ids.** `/suggestions` (`{"query": "Williamsburg"}`): a `neighborhood` place carries `location_id` (the input of `/neighborhood`) and `search_location` (the input of `/search`); an `address` carries `zpid`; schools carry `school_id`.
2. **The neighborhood.** `/neighborhood` with `location_id`. Note the survey statements and `minimum_responses`, `reviews.total` and the category counts, and `market.snapshot.scope`.
3. **Homes in it.** `/search` with `location` = `"Neighborhood, City, ST"`, a ZIP or `"City, ST"`, plus `listing_status` and filters. Check `applied_filters` and the notes.
4. **One home or building.** `/property` with `zpid` or `building_id` from `listings[]`. `neighborhood.location_id` on a home leads back to step 2.
5. **Schools.** `/school` with `url` from `schools.items[]` (or `school_id` + `state` from suggestions).
6. **Report.** Each survey figure with its statement, percent and response count; each price with Trulia, USD and the `fetched_at` date; the snapshot with its scope and `last_updated` month; no verdict on the neighborhood.
7. **Over time:** store each answer with its `fetched_at`; the survey, reviews and snapshot change as Trulia updates them, and that stored set is your record.

## Parameters

### Neighborhood (`/neighborhood`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location_id` | string or integer | one of | A Trulia neighborhood location id (`85381`): `neighborhood.location_id` on a property, or `location_id` of a neighborhood in suggestions |
| `url` | string | one of | Or the neighborhood's trulia.com link (`/n/<st>/<city>/<neighborhood>/<location id>/`) |
| `include_market_snapshot` | boolean | true | Add `market` (snapshot and monthly median sale price history); same 1 credit. `false` answers faster |
| `language` | string | `en` | `en` or `es` (Trulia's US Spanish neighborhood page) |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | required | A ZIP code (`78701`), `"City, ST"` (`Austin, TX`) or `"Neighborhood, City, ST"` (`Upper East Side, New York, NY`); suggestions returns `search_location` values |
| `listing_status` | string | `for_sale` | `for_sale`, `for_rent` or `sold` (recently sold) |
| `beds_min` | integer | none | 0-10 |
| `baths_min` | integer | none | 1-10 |
| `price_min`, `price_max` | integer | none | USD (monthly rent on `for_rent`) |
| `sqft_min`, `sqft_max` | integer | none | Living area, square feet |
| `year_built_min`, `year_built_max` | integer | none | 1700 to two years ahead |
| `hoa_max` | integer | none | Highest monthly HOA fee, USD (`for_sale` and `sold` only) |
| `property_types` | list | none | Any of `single_family`, `townhouse`, `condo`, `coop`, `apartment`, `multi_family` |
| `keyword` | string | none | A listing keyword Trulia filters on (letters, digits, spaces; `pool`, `hardwood floors`), up to 40 characters |
| `pets` | list | none | Rentals only: `cats`, `small_dogs`, `large_dogs` |
| `sort` | string | `default` | `default` (Trulia's order: newest on for_sale, its own ranking on for_rent, latest sale on sold), `newest`, `price_low`, `price_high`, `sqft` (largest), `beds` (most), `baths` (most) |
| `page` | integer | 1 | 1-50, 40 homes a page; `has_more` says whether another exists |
| `language` | string | `en` | `es` on `for_rent` only |

### Property (`/property`), school (`/school`), suggestions (`/suggestions`)

| Endpoint | Parameters |
|---|---|
| `/property` | one of `zpid` (`339349810`, the id Trulia shares with Zillow; `listings[].zpid`), `building_id` (a rental building's id, `listings[].building_id`) or `url` (a trulia.com `/home/<address>-<zpid>` or `/building/<name>-<id>` link); `language` `en` or `es` (Spanish on building pages only) |
| `/school` | one of `url` (a Trulia school link, `schools.items[].url`) or `school_id` (`279445`, the number at the end of the school link) with `state` (two-letter code, `IL`); `language` `en` only |
| `/suggestions` | `query` (2-80 characters: the start of a city, neighborhood, ZIP, address or school name); `listing_status` `for_sale` (default) or `for_rent`; `include_schools` (default true); `language` `en` only |

## Examples

### What locals say about a neighborhood, with its market

```bash
curl -X POST https://api.scavio.dev/api/v1/trulia/neighborhood \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location_id": "85381"}'
```

Captured `data` (2026-11-26; `statements` cut to 4 of 16, reviews to 2 of 40 and the second review's text shortened, `points` to the last 3 of 100; `url`, `search_urls`, `amenities`, `schools`, `geo`, `nearby_neighborhoods`, `homes_for_sale`, the snapshot's `neighborhood` and `city` and `notes` dropped):

```json
{
  "location_id": 85381,
  "region_id": 270957,
  "name": "Upper East Side",
  "city": "New York",
  "state": "NY",
  "county": "New York County",
  "zip_code": "10128",
  "language": "en",
  "what_locals_say": {
    "title": "What Locals Say about Upper East Side",
    "minimum_responses": 1480,
    "statements": [
      {"type": "WalkableToGroceries", "statement": "It's walkable to grocery stores", "percent": 94},
      {"type": "PeopleWouldWalkAloneAtNight", "statement": "People would walk alone at night", "percent": 84},
      {"type": "EasyParking", "statement": "Parking is easy", "percent": 30},
      {"type": "NeedACar", "statement": "Car is needed", "percent": 16}
    ]
  },
  "safety": {
    "minimum_responses": 1480,
    "statements": [
      {"type": "Sidewalks", "statement": "There are sidewalks", "percent": 93},
      {"type": "WellLitStreets", "statement": "Streets are well-lit", "percent": 87},
      {"type": "PeopleWouldWalkAloneAtNight", "statement": "People would walk alone at night", "percent": 84}
    ]
  },
  "reviews": {
    "total": 277,
    "shown": 40,
    "categories": [
      {"id": "general", "name": "General", "count": 110},
      {"id": "community", "name": "Community", "count": 35},
      {"id": "dogOwners", "name": "Dog Owners", "count": 36},
      {"id": "parents", "name": "Parents", "count": 47},
      {"id": "commute", "name": "Commute", "count": 49}
    ],
    "items": [
      {"id": "1c99d449-5fd9-452e-958a-2ffe7f4b3902", "text": "Nice people/ family orientations- the blend of different cultures", "category": "general", "category_name": "General", "reviewer_type": "Prev. Resident", "date": "2026-11-18T01:08:07+00:00", "helpful": null},
      {"id": "25d4881e-8ffe-48f3-99ef-089fba1c26bd", "text": "It’s quite “suburbs “ of hectic Manhattan. Very low key , kids friendly and neighborhoody. ...", "category": "general", "category_name": "General", "reviewer_type": "Resident", "date": "2024-04-18T01:32:59+00:00", "helpful": 15}
    ]
  },
  "facts": {
    "homes_for_sale": 1885,
    "homes_for_rent": 507,
    "for_sale_price_range": {"min": 199000, "max": 89500000, "display": "$199K - $89.5M"},
    "for_rent_price_range": {"min": 1460, "max": 165000, "display": "$1.46K - $165K"},
    "commute": {"destination": "Downtown New York", "minutes": 22},
    "school_count": null
  },
  "market": {
    "snapshot": {
      "scope": "neighborhood",
      "area": "Upper East Side",
      "last_updated": "October 2026",
      "avg_sale_price": {"value": 1465833.3333333333, "display": "$1.47M", "mom_change": "$50K", "mom_direction": "up"},
      "sale_to_list_ratio": {"value": 0.9818101215762818, "display": "98.2%", "mom_change": "0.3%", "mom_direction": "up"},
      "price_per_sqft": {"value": 1379.4694603266653, "display": "$1.38K", "mom_change": "$33", "mom_direction": "up"},
      "active_listings": {"value": 1130, "display": "1130", "mom_change": "82", "mom_direction": "up"},
      "market_condition": "NEUTRAL_MARKET",
      "market_temperature_index": 52,
      "source": "Sourced by Trulia Market Trends"
    },
    "median_sale_price_history": {
      "scope": "neighborhood",
      "area": "Upper East Side",
      "last_updated": "September 2026",
      "points": [{"month": "Jul 2026", "median_sale_price": 1512500}, {"month": "Aug 2026", "median_sale_price": 1335000}, {"month": "Sep 2026", "median_sale_price": 1550000}]
    },
    "rental_snapshot": null,
    "rent_history": null,
    "read_from": {"zpid": "119917817", "url": "https://www.trulia.com/home/345-e-93rd-st-8f-new-york-ny-10128-119917817"}
  }
}
```

The same page listed 175 amenities in 7 categories (Restaurants, Groceries, Nightlife, Cafes, Shopping, ArtsAndEntertainment, Fitness), 50 schools (Preschool 17, Elementary 34, Middle 29, High 28) with GreatSchools ratings where given, and 10 nearby neighborhoods (Central Park, Roosevelt Island ...). For Gravesend (`85244`) `market.snapshot.scope` was `city` with `area` New York, and the note read "market: Trulia shows New York's city-wide market for this neighborhood (scope city)." With `language: "es"` Boyle Heights (`87374`) came back as "Lo que dicen los locales sobre Boyle Heights" with statements such as "Hay banquetas" 91%.

### Search homes for sale in a city

```bash
curl -X POST https://api.scavio.dev/api/v1/trulia/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": "Austin, TX", "beds_min": 3, "price_max": 600000}'
```

Captured `data` (2026-11-26; `listings` cut to 2 of 40 (the 1st and 3rd), each row shortened to the fields shown; `url`, `neighborhoods` and `notes` dropped):

```json
{
  "listing_status": "for_sale",
  "location": {"city": "Austin", "state": "TX", "zip_code": null, "neighborhood": null, "location_id": 4668},
  "language": "en",
  "total": 2146,
  "page": 1,
  "page_size": 40,
  "total_pages": 54,
  "has_more": true,
  "sort": "default",
  "applied_filters": {"sort": {"type": "DATE", "ascending": false}, "price": {"min": 0, "max": 600000}, "beds": {"min": 3, "max": null}},
  "count": 40,
  "listings": [
    {"id": "29487771_ZPID", "zpid": "29487771", "status": "for_sale", "listing_type": "RESALE", "price": 300000, "price_display": "$300,000", "currency": "USD", "address": "4914 Fort Clark Dr, Austin, TX 78745", "zip_code": "78745", "beds": 3, "baths": 2, "living_area": 1154, "home_type": "SINGLE_FAMILY_HOME", "tags": ["NEW - 19 MIN AGO"], "date_listed": "2026-11-26T15:27:27+00:00", "brokerage": "Berkshire Hathaway TX Realty"},
    {"id": "29414751_ZPID", "zpid": "29414751", "status": "for_sale", "listing_type": "RESALE", "price": 520000, "price_display": "$520,000", "currency": "USD", "address": "1802 Alegria Rd, Austin, TX 78757", "zip_code": "78757", "beds": 3, "baths": 1, "living_area": 1024, "home_type": "SINGLE_FAMILY_HOME", "tags": ["NEW - 16 HRS AGO"], "date_listed": "2026-11-25T23:41:43+00:00", "brokerage": "Kifer Sparks Agency, LLC"}
  ]
}
```

`{"location": "Brooklyn, NY", "listing_status": "for_rent", "pets": ["cats"]}` returned 2,264 rentals, led by rental buildings with a price range ("Sky Three", 532 Neptune Ave, `price_display` "$3,375 - $5,425/mo", 1-3 beds). `{"location": "Seattle, WA", "listing_status": "sold", "sort": "newest"}` returned 7,547 recent sales with `sold_date` per row, and Trulia added `sold_within` 9 to `applied_filters` by itself. `{"location": "98101", "property_types": ["condo"]}` returned 97 condos. In Spanish (`{"location": "Austin, TX", "listing_status": "for_rent", "language": "es"}`) prices read "$1,121 - $1,761/mes" and `price_note` "Precio total".

### One home for sale

```bash
curl -X POST https://api.scavio.dev/api/v1/trulia/property \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zpid": "119917817"}'
```

Captured `data` (2026-11-26; a subset of the fields shown: `features`, `faqs`, `images`, `insights`, `description`, `taxes`, `open_houses`, `seller_net_proceeds`, `median_sale_price_history`, the `market_snapshot` figures, the `*_display` and address-part fields and `notes` dropped, `price_history` details cut):

```json
{
  "id": "119917817_ZPID",
  "zpid": "119917817",
  "status": "for_sale",
  "listing_type": "RESALE",
  "address": "345 E 93rd Street #8F, New York, NY 10128",
  "neighborhood_name": "Upper East Side",
  "price": 610000,
  "price_display": "$610,000",
  "currency": "USD",
  "beds": 1,
  "baths": 1,
  "living_area": 725,
  "home_type": "COOP",
  "date_listed": "2026-11-26T13:33:36+00:00",
  "zestimate": null,
  "rent_zestimate": 4634,
  "rent_zestimate_display": "$4,634/mo",
  "price_history": [
    {"date": "2026-11-26", "event": "Listed For Sale", "price": 610000, "price_display": "$610,000", "source": "OneKey® MLS as distributed by MLS GRID #1077203"},
    {"date": "2013-01-07", "event": "Sold", "price": 368000, "price_display": "$368,000", "source": "N/A"}
  ],
  "last_sold": {"price": 368000, "date": "2013-01-07"},
  "brokerage": "NextHome Residential",
  "payment_estimate": {"monthly_total": 3815, "principal_and_interest": 3282, "property_taxes": 458, "homeowners_insurance": 75, "hoa": null, "down_payment_percent": 20},
  "price_vs_median": {"percent": 58, "direction": "below", "median_display": "$1.47M", "area": "New York"},
  "market_snapshot": {"scope": "neighborhood", "area": "Upper East Side", "last_updated": "October 2026", "market_condition": "NEUTRAL_MARKET", "market_temperature_index": 52},
  "neighborhood": {"location_id": 85381, "region_id": 270957, "url": "https://www.trulia.com/n/ny/new-york/upper-east-side/85381/", "search_url": "https://www.trulia.com/NY/New_York,Upper_East_Side/"},
  "photo_count": 42
}
```

A recently sold Seattle condo (`63337849`) read sold 114,000 on 2026-08-12, `zestimate_display` "$221,200", `home_value.since_last_year` {"value": "$28K", "percent": "-11.1%", "direction": "down"} and a 2025 tax of 2,544 on a 239,000 assessment. A Brooklyn rental (`2077403072`) added `rental_market_snapshot` ("Rental Market Trends in Gravesend", average rent $2.8K) and `rent_history` ("Average rent in Gravesend increased by +5% in the last 10 years"). An id Trulia does not have was a charged `404`.

### One rental building

```bash
curl -X POST https://api.scavio.dev/api/v1/trulia/property \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"building_id": "2775825120"}'
```

Captured (2026-11-26): "The Janis", 3500 E Parmer Ln, Austin, TX 78754, `listing_type` RENTAL_COMMUNITY, `price_display` "$1,524 - $2,310/mo" with `price_note` "Total price" ("The total price includes the base rent ($1,449–$2,235) and any monthly fees ($75) that the property owner lists as required ..."), `units` {"total": 422, "available": 56}, `ideal_income` 54864. `floor_plans.groups` "1 Bedroom (2 Floorplans, 40 Units)" and "2 Bedrooms (5 Floorplans, 16 Units)"; plan "1A" at $1,524 - $1,554, 731 sqft, with units such as {"name": "Unit 1210", "availability": "Available Now", "price_display": "$1,524/mo"}. `fees.monthly_required` starts with {"name": "Monthly base rent", "min": 1449, "max": 2235} and lists each other required fee with its amount or Trulia's text ("Varies", "Contact for details"). `pet_policy.summary` "Cats, small dogs, large dogs allowed", with per-species facts (monthly dog rent $25/mo, dog deposit $250). No property manager contact is returned.

### School and suggestions

- `/school` `{"school_id": "279445", "state": "IL"}`: Dever Elementary School, Chicago Public Schools, PK-8, 728 students, `ratings` {"overall": 4, "max": 10, "test_scores": 4, "equity": 3, "student_growth": 4, "source": "GreatSchools"}, student-teacher ratio 13.2, `parent_rating` 4 from 12 reviews, 5 parent reviews with rating, text and date (no names), 19 nearby schools, `assigned_homes` 10 for sale and 16 for rent.
- `/suggestions` `{"query": "Austin"}`: 7 places (Austin, TX `location_id` 4668 with `search_location` "Austin, TX"; Austinville, VA; Austintown, OH ...) and 3 schools (Austin Independent School District; Jackson Memorial Elementary School `school_id` 1083433 ...). `{"query": "Williamsburg"}` led with Williamsburg, VA; the neighborhood "Williamsburg, New York, NY" came third with `location_id` 85395 and `search_location` "Williamsburg, New York, NY". `{"query": "98101"}` returned the ZIP and addresses with their `zpid`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def trulia(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/trulia/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# Find the neighborhood's id (1 credit)
places = trulia("suggestions", {"query": "Upper East Side"})["data"]["places"]
hood = next(p for p in places if p["type"] == "neighborhood")

# What locals say, the reviews and the market snapshot (1 credit)
n = trulia("neighborhood", {"location_id": hood["location_id"]})["data"]
print(n["name"], n["city"], "responses", n["what_locals_say"]["minimum_responses"])
for s in n["what_locals_say"]["statements"]:
    print(f'  {s["percent"]}% {s["statement"]}')
print("reviews", n["reviews"]["total"], "shown", n["reviews"]["shown"])
snap = (n.get("market") or {}).get("snapshot")
if snap:
    print(snap["scope"], snap["area"], snap["last_updated"], snap["avg_sale_price"]["display"], snap["market_condition"])

# Homes for sale in the same neighborhood (1 credit)
s = trulia("search", {"location": hood["search_location"], "beds_min": 2})["data"]
for h in s["listings"][:5]:
    print(h["zpid"], h["price_display"], h["beds"], h["address"])

# Store each answer with fetched_at: that stored set is your record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Neighborhood, search, property and school answers carry `notes`.

- **home row** (search, a neighborhood's `homes_for_sale`, a school's `assigned_homes`) - `id`, `zpid`, `building_id`, `url`, `status` (for_sale, for_rent, sold, rented, off_market), `listing_type`, `price`, `price_min`, `price_max`, `price_display`, `price_note`, `price_note_details`, `currency`, `price_change_direction`, `address`, `street_address`, `city`, `state`, `zip_code`, `community_name`, `latitude`, `longitude`, `beds`, `beds_min`, `beds_max`, `beds_display`, `baths`, `baths_min`, `baths_max`, `baths_display`, `living_area`, `living_area_min`, `living_area_max`, `living_area_display`, `lot_size_display`, `home_type`, `tags`, `date_listed`, `sold_date`, `open_houses`, `brokerage`, `has_3d_tour`, `has_video`, `image`, `images`.
- **neighborhood** - `location_id`, `region_id`, `name`, `city`, `state`, `county`, `zip_code`, `url`, `language`, `search_urls` {`for_sale`, `for_rent`}, `what_locals_say` {`title`, `minimum_responses`, `statements[]`}, `safety` {`minimum_responses`, `statements[]`}, `reviews` {`total`, `shown`, `categories[]`, `items[]`}, `facts`, `amenities` {`categories`, `count`, `items[]` {`name`, `category`, `subcategory`, `website`, `latitude`, `longitude`}}, `schools` {`levels[]` {`level`, `name`, `count`}, `items[]` {`id`, `name`, `url`, `district`, `type`, `levels`, `grades`, `students`, `rating`, `rating_max`, `parent_rating`, `review_count`, `address`, `latitude`, `longitude`, `greatschools_url`, `reviews[]` {`rating`, `rating_max`, `text`, `type`, `date`}}}, `geo` {`centroid`, `bounding_box`, `encoded_polygon`, `wkt`}, `nearby_neighborhoods[]` {`name`, `location_id`, `url`, `homes_for_sale`, `for_sale_price_range`}, `homes_for_sale` {`total`, `listings[]`}, `market` (unless `include_market_snapshot: false`) {`snapshot`, `median_sale_price_history`, `rental_snapshot`, `rent_history`, `read_from`}, `notes`.
- **search** - `listing_status`, `location` {`city`, `state`, `zip_code`, `neighborhood`, `location_id`}, `url`, `language`, `total`, `page`, `page_size`, `total_pages`, `has_more`, `sort`, `applied_filters`, `neighborhoods[]` {`name`, `id`, `count`}, `count`, `listings[]`, `notes`.
- **property** - `id`, `zpid`, `building_id`, `url`, `language`, `name`, `status`, `status_label`, `listing_type`, `is_foreclosure`, `address`, `street_address`, `city`, `state`, `zip_code`, `county`, `neighborhood_name`, `latitude`, `longitude`, `price`, `price_min`, `price_max`, `price_display`, `price_note`, `price_note_details`, `currency`, `beds`, `beds_display`, `baths`, `baths_display`, `baths_summary`, `living_area` (and `_min`, `_max`, `_display`), `lot_size_display`, `home_type`, `home_type_display`, `available_date`, `date_listed`, `last_modified`, `tags`, `insights`, `description`, `description_updated`, `zestimate`, `zestimate_display`, `rent_zestimate`, `rent_zestimate_display`, `home_value` {`current_display`, `since_last_month`, `since_last_year`, `since_last_sale`, `history`}, `price_change_direction`, `price_history[]` {`date`, `event`, `price`, `price_display`, `source`, `details`}, `last_sold`, `taxes` {`assessment`, `source`, `history[]` {`year`, `tax`, `assessment`}}, `features` {`highlights`, `categories[]` {`name`, `attributes`, `groups`}}, `open_houses[]`, `brokerage`, `mls`, `payment_estimate`, `price_vs_median`, `faqs[]` {`question`, `answer`}, `market_snapshot`, `median_sale_price_history`, `rental_market_snapshot`, `rent_history`, `seller_net_proceeds`, `neighborhood` {`location_id`, `region_id`, `url`, `search_url`, `what_locals_say`}, `schools_summary`, `floor_plans` {`disclaimer`, `groups[]` {`title`, `beds`, `plans[]` {`id`, `name`, `availability`, `beds`, `baths`, `price_min`, `price_max`, `price_display`, `sqft_min`, `sqft_max`, `sqft_display`, `image`, `units[]` {`id`, `name`, `availability`, `available_now`, `available_date`, `price_min`, `price_max`, `price_display`, `sqft_display`}}}}, `fees` {`monthly_required`, `one_time_required`, `monthly_optional`, `one_time_optional` [{`name`, `min`, `max`, `amount`, `amount_text`}], `disclaimer`}, `total_monthly_fee_included`, `pet_policy`, `special_offers`, `ideal_income`, `units` {`total`, `available`}, `photo_count`, `images` (up to 50), `has_3d_tour`, `notes`.
- **school** - `id`, `name`, `url`, `type`, `levels`, `grades`, `students`, `district`, `district_url`, `address` {`street`, `city`, `state`, `zip_code`}, `latitude`, `longitude`, `website`, `greatschools_url`, `ratings` {`overall`, `max`, `test_scores`, `equity`, `academic_progress`, `college_readiness`, `student_growth`, `source`}, `student_teacher_ratio`, `student_counselor_ratio`, `certified_teachers_percent`, `parent_rating`, `review_count`, `reviews[]`, `nearby_schools[]`, `assigned_homes` {`for_sale`, `for_rent`: {`total`, `listings[]`}}, `notes`.
- **suggestions** - `query`, `listing_status`, `count`, `places[]` {`title`, `details`, `type` (city, neighborhood, zipcode, county, address ...), `city`, `state`, `zip_code`, `location_id`, `region_id`, `zpid`, `url`, `search_location`, `latitude`, `longitude`}, `schools[]` {`title`, `subtitle`, `details`, `type` (school or school_district), `school_id`, `city`, `state`, `latitude`, `longitude`}.

## Guardrails

- Name it "Trulia (trulia.com, Zillow Group's home and neighborhood site)" on first mention, "Trulia" after that.
- Survey figures: always "Trulia's What Locals Say survey" with the statement text, the percent and `minimum_responses` ("84% of Trulia survey respondents said people would walk alone at night, Upper East Side, response count 1,480, fetched Nov 26, 2026"). Never present them as crime statistics, a safety rating, a ranking or Scavio's view of the neighborhood, and never rank neighborhoods as safe or unsafe from them.
- Reviews: no reviewer is named or identified; quote review text as Trulia shows it, with its category, `reviewer_type` and date, and say how many of `reviews.total` were shown.
- Market: quote the snapshot with its `scope`, `area` and `last_updated` month, and say when it is the city's market rather than the neighborhood's. Quote `market_condition` as Trulia's label.
- Prices: USD with Trulia, the address or zpid and the `fetched_at` date. `zestimate` and `rent_zestimate` are "Zillow's estimates as Trulia shows them", never an appraisal or what a home is worth; `payment_estimate` is Trulia's own estimate from its FAQ answer, not a loan quote.
- Fair housing: describe places with the data as Trulia gives it; do not characterize a neighborhood by who lives there, and do not steer anyone toward or away from an area.
- No agent personal data: name the brokerage company only, and do not try to identify a listing agent, a reviewer or a property manager.
- Descriptive only: no commentary on Trulia's business, pricing practices or policies.
- Do not republish Trulia photos, descriptions or review text in bulk. Write trulia.com as plain text and cite zpids, location ids and capture dates rather than linking Trulia pages.
- Terms: Scavio does not collect or store Trulia data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no lead, tour or contact flow. Trulia's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate survey percents, reviews, prices, zpids, location ids or school ratings. Only return what the API returned, with the `fetched_at` time.
- Not available: crime data, agent names, phones or profiles, neighborhood reviews past 40, walk or transit scores, Trulia market-trends pages, tours, contact or financing.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `location`, or one that is not a ZIP, "City, ST" or "Neighborhood, City, ST" ("location must be a ZIP code (78701), \"City, ST\" (Austin, TX) or \"Neighborhood, City, ST\" (Upper East Side, New York, NY)."); `pets` without `for_rent` ("pets is a rental filter: send it with listing_status for_rent."); `hoa_max` on `for_rent` ("hoa_max is a for-sale filter: Trulia does not filter rentals by HOA fee."); a `_min` above its `_max`; a `keyword` with other characters; a `sort`, `listing_status`, `property_types` or `pets` value outside its list; `page` past 50; `language: "es"` where Trulia has no Spanish page ("language es is only available where Trulia publishes Spanish pages: rental searches (listing_status for_rent), buildings and neighborhoods. ... is English only."); `/property` without exactly one of `zpid`, `building_id` or `url`; `/neighborhood` without exactly one of `location_id` or `url`; `/school` without exactly one of `url` or `school_id`, or `school_id` without `state` ("state is required with school_id (the two-letter code at the start of the school link, e.g. IL)."); suggestions under 2 characters.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Trulia has no home or building with this id. Check the zpid, building_id or url (search returns them).", "Trulia has no neighborhood page with this location id. Use property neighborhood.location_id or a suggestions neighborhood location_id.", "Trulia has no school with this id in this state. Use schools[].url from neighborhood, or school_id + state from suggestions.", "Trulia does not know this location. Send a ZIP code, \"City, ST\" or \"Neighborhood, City, ST\" (suggestions returns search_location values).". Take zpids, location ids and school ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=trulia-api).
- `502` means Trulia data was temporarily unavailable ("Trulia is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Trulia is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.97.0
npm install scavio@0.98.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hood } = await scavio.trulia.neighborhood({ location_id: "85381" });
const { data: homes } = await scavio.trulia.search({ location: "Austin, TX", beds_min: 3, price_max: 600000 });
const { data: home } = await scavio.trulia.property({ zpid: "119917817" });
const { data: school } = await scavio.trulia.school({ school_id: "279445", state: "IL" });
const { data: places } = await scavio.trulia.suggestions({ query: "Austin" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.trulia.neighborhood(...)`, `search`, `property`, `school` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 5 endpoints as tools: `get_trulia_neighborhood`, `search_trulia`, `get_trulia_property`, `get_trulia_school` and `get_trulia_suggestions`. Trulia is opt-in: add `trulia` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.97.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,trulia"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [neighborhood](https://scavio.dev/docs/trulia-neighborhood?utm_source=agent-skills&utm_medium=skill&utm_campaign=trulia-api), [search](https://scavio.dev/docs/trulia-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=trulia-api), [property](https://scavio.dev/docs/trulia-property?utm_source=agent-skills&utm_medium=skill&utm_campaign=trulia-api), [school](https://scavio.dev/docs/trulia-school?utm_source=agent-skills&utm_medium=skill&utm_campaign=trulia-api), [suggestions](https://scavio.dev/docs/trulia-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=trulia-api). Overview: [Trulia API](https://scavio.dev/trulia-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=trulia-api).
