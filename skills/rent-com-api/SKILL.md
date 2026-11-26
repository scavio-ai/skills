---
name: rent-com-api
description: Rent.com API for Rent.com (rent.com, the US rental listing site run by Redfin, and its sister site Apartment Guide, apartmentguide.com, which lists the same rentals) - Rent.com's current average rent per bed count for a US city with its year-on-year change, next to the rents the listings in that city ask, as Rent.com shows them (Austin, TX on Nov 26, 2026 - one-bedroom 1,099 USD a month, -25% year on year, two-bedroom 1,364, -25%, across 4,748 rentals with 23,832 available units), plus the monthly series Rent.com publishes on the page (it ended May 2025 in every capture), the rent distribution and nearby cities and neighborhoods with their averages; rental search by city and state, ZIP or neighborhood for apartments, houses, condos, townhouses or rooms, filtered by beds, baths, rent range, minimum square feet, pets, cheap or luxury, rent specials and up to 8 amenities, 6 sorts, 30 a page (50 on Apartment Guide), each listing with its lowest rent, rent per bed count, bed, bath and square-foot ranges, units available, rent specials, price-drop amounts, pet friendliness, highlighted amenities and the management company for paid listings; one listing in full with every floor plan and unit rent, deposit and availability date, fees, pet policies, parking, amenities, office hours, lease terms, income limits, schools, nearby places, walk, bike and transit scores and similar listings; one building's unit listings; search-box suggestions for places and properties; the cities Rent.com lists for a state. 6 endpoints, 1 credit per call. US only, USD. No phone numbers, emails or agent and landlord names, no reviews, no rent history beyond the series Rent.com publishes.
version: 1.0.0
tags: rent-com, rentcom, rent-com-api, apartment-guide, apartmentguide, rent-com-rentals, rent-com-listings, rent-com-search, rent-com-rent-trends, rent-com-average-rent, apartment-guide-listings, apartments-for-rent, rental-listings, rental-search, rent-prices, average-rent, rent-trends, rental-market, floor-plans, unit-availability, rent-specials, move-in-specials, price-drops, pet-policy, pet-friendly-apartments, apartment-amenities, houses-for-rent, condos-for-rent, rooms-for-rent, property-management-companies, us-rentals, real-estate, usd, rent-monitoring, market-research, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/rentcom-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rent-com-api
---

# Rent.com API - Rental Listings, Average Rent, Floor Plan Prices

Read Rent.com (rent.com, the US rental listing site run by Redfin) and its sister site Apartment Guide (apartmentguide.com, the same rentals): rental search by city, ZIP or neighborhood, one listing in full with its floor plans and unit rents, one building's unit listings, Rent.com's rent trends for a city, search-box suggestions and the cities Rent.com lists for a state. Every answer is what the site's public pages show a visitor without an account at the moment of the call, in USD a month. All 6 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Rent.com and Apartment Guide show to any visitor and returns them as JSON for analysis. It uses no account, no saved search, no tour request, no contact form and no application.

**The job this skill is for: what Rent.com says a city's rentals average per bed count, next to what the listings there ask.** `/rent-trends` returns Rent.com's `current` average rent per bed count with its year-on-year change and the monthly `series` it publishes on the page; `/search` returns the listings with their lowest rent and rent per bed count, plus `total` and `available_units`. Captured 2026-11-26 (1 credit per call):

| City | `current` 1 bed (YoY) | `current` 2 beds (YoY) | Last `series` month (May 2025): 1 bed / 2 beds | `/search` |
|---|---|---|---|---|
| Austin, TX | 1,099 (-25%), as `/search` `average_rent` | 1,364 (-25%), as `/search` `average_rent` | not captured | `beds: 2`: 1,819 rentals, 20,380 available units |
| New York, NY | 5,242 (+4%) | 7,849 (+13%) | 5,242 / 7,849 | 4,168 rentals, 6,861 available units |
| Chicago, IL | 1,275 (-33%) | 1,547 (-38%) | 2,120 / 2,733 | Lincoln Park, `beds: 1`: 646 rentals |
| Los Angeles, CA | 4,950 (+85%) | 6,450 (+71%) | 2,717 / 3,565 | `beds: 2`: 3,219 rentals; Apartment Guide `beds: 1`: 3,955 rentals, 13,546 available units |

The averages are Rent.com's, as it publishes them; the series stops at May 2025 and can sit far from `current` (Chicago one-bedroom: 2,120 in the series, 1,275 now). Quote `current` with its YoY text and the date, the series with its `series_range`, and listing rents as asks; leave any gap between them uninterpreted. For another site's view of the same city use `rentcafe-api` (RentCafe's city averages per bed type and its listings), `zillow-property-data`, `redfin-property-data` or `realtor-com-property-data`, matched on city, bed count and date.

Nine limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged, and so is a search page past the last page (an empty page with a note); a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Two sites, one inventory.** `site: "apartmentguide"` lists the same rentals as Rent.com (Los Angeles, CA, `beds: 1`, captured Nov 26, 2026: 3,955 rentals and 13,546 units), 50 a page instead of 30, and its ids drop Rent.com's `lc` prefix (`5898701` = `lc5898701`; either id works on either site). Apartment Guide takes only city and state (with one `beds` value) or a ZIP, and `page`; send `site: "rent"` for every other filter. `/building`, `/rent-trends` and `/cities` read Rent.com only.
- **Averages are Rent.com's.** `current` (rent trends) and `average_rent` (search, studio to two bedrooms) are Rent.com's published averages with its YoY change. A ZIP or neighborhood search carries the city's averages (ZIP 78704 showed Austin's, Lincoln Park showed Chicago's), and Apartment Guide searches carry none (`null`). A bed count with too few listings has a `null` average.
- **The monthly series is old.** `series` ran 2024-04 to 2025-05 (13 points) in every capture; Rent.com does not update it monthly, so it can end well before today. Report `series_range` with it and never present it as this month's rent.
- **Rent is the lowest listed rent.** `price` is the lowest rent the listing shows; `rent_by_beds` and the floor plans give the rest. Student housing that rents by the bed shows up at low rents (three of the first five Austin two-bedroom cards with `sort: "price_low"` were student housing named "Rent by the Bed", at 587 to 714), and `sort: "price_high"` can put listings priced far above a monthly rent at the top.
- **No contacts.** No phone number, email or agent or landlord name is returned. `management_company` is given only for listings a property manager pays to list; `private_listing: true` marks the others.
- **Price drops, not history.** `has_price_drops`, `price_drops` (USD amounts) and, on a listing, `price_drop_overall` are what the site shows today. There is no rent history per listing: store your own answers with `fetched_at`.
- **Slow pages.** Search answered in about 4 to 13 seconds in the captures (the probe saw up to 31), a listing 3 to 13, rent trends 2 to 10. Set a client timeout of at least 240 seconds and send one request at a time.
- **What is not there.** No reviews (none are published on these sites), no contacts, no application, tour or availability booking, no for-sale homes, no rent history beyond the published series. Fees are often empty: `fees` was all `null` on every listing captured.

Rent.com and Apartment Guide link no public data API or affiliate feed from their sites; their business links are for advertisers listing a property. This skill reads the public pages with one Scavio key.

See also: `rentcafe-api` (RentCafe's US and Canada listings, floor-plan units, resident reviews and city rent trends), `zillow-property-data`, `redfin-property-data` and `realtor-com-property-data` (rentals next to homes for sale). Same city and bed count only, and name the site and date with every number.

## When to trigger

Use this skill when the user asks to:
- Read Rent.com's current average rent per bed count for a US city, its year-on-year change, the published monthly series and the rent distribution
- Search Rent.com or Apartment Guide rentals by city and state, ZIP or neighborhood, by property type, beds, baths, rent range, square feet, pets, cheap or luxury, rent specials or amenities, sorted by price, beds, size or latest update
- Read one rental in full: floor plans and unit rents, deposits and availability dates, fees, pet policies, parking, amenities, office hours, lease terms, income limits, schools, nearby places, walk, bike and transit scores
- List the unit listings in one building on Rent.com
- Turn a place or property name into the city, ZIP or neighborhood Rent.com uses, or list the cities Rent.com has for a state

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=rent-com-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=rent-com-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example 25 cities: one rent trends and one search each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, search answered in 4-13 seconds (the probe saw up to 31), listing 3-13, building 5-6, rent trends 2-10, suggestions 2-5 and cities 2-6. Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/rentcom/search` | Rentals by city and state, ZIP or neighborhood: lowest rent, rent per bed count, bed / bath / square-foot ranges, units available, rent specials, price drops, pets, highlighted amenities, management company; total, available units, paging, the city's average rents | 1 |
| `POST /api/v1/rentcom/listing` | One rental by id or link: floor plans with unit rents, deposits and dates, fees, pet policies, parking, amenities, office hours, deals, lease terms, income limits, schools, nearby places, walk / bike / transit scores, similar listings | 1 |
| `POST /api/v1/rentcom/building` | One building on Rent.com: its separate unit listings at one address, rent range, photos, schools | 1 |
| `POST /api/v1/rentcom/rent-trends` | Rent.com's rent trends for one city: current average rent per bed count with YoY change, listing count, the published monthly series, rent distribution, nearby cities and neighborhoods with their averages | 1 |
| `POST /api/v1/rentcom/suggestions` | The site's search-box suggestions: places (city, ZIP, neighborhood, school, college) and matching rentals | 1 |
| `POST /api/v1/rentcom/cities` | The cities Rent.com links from a state page, A to Z, with the `city` input for search and rent trends | 1 |

## Market

US only, USD a month. There is no `country` or `currency` input. `site` picks the host: `rent` (rent.com, the default) or `apartmentguide` (apartmentguide.com, the same rentals). Locations are a US city with its state (code or name), a 5-digit ZIP, or a neighborhood inside a city.

## Rents, averages and listings

| Field | Meaning |
|---|---|
| `price` | The lowest listed rent, USD a month (`null` on some building unit rows; read `rent_min` there) |
| `price_text`, `rent_min`, `rent_max` | The site's rent text ("$624+") and the listed rent range |
| `rent_by_beds[]` | {`beds`, `rent_min`, `rent_max`, `sqft_min`, `sqft_max`} per bed count, as the search card gives it |
| `floor_plans[]` (listing) | {`id`, `name`, `beds`, `baths`, `sqft`, `rent_min`, `rent_max`, `rent_text`, `available_count`, `availability_text`, `available_date`, `deposit`, `units[]` {`unit_id`, `rent`, `sqft`, `available_date`, `available`, `deposit`, `floor`}} |
| `deals_text`, `deals[]`, `special_terms` | The listing's rent specials as written ("UP TO 6 WEEKS FREE FOR WELL QUALIFIED APPLICANTS!") |
| `has_price_drops`, `price_drops`, `price_drop_overall` | The price drops the site shows, as USD amounts (`[249, 209, 57, 398]`, overall 350) |
| `average_rent` (search), `current` (rent trends) | Rent.com's average rent per bed count {`average_rent`, `yoy_change_pct`, `yoy_change_text`} |
| `series`, `series_range` (rent trends) | The monthly averages Rent.com publishes on the page, and the months they cover |
| `rent_distribution[]` (rent trends) | {`min`, `max`, `count`, `percent`} rent bands for the city |
| `kind` | `listing` or `building` (a building id starts with `b`; send it to `/building`) |
| `private_listing`, `management_company`, `verified` | Unpaid listings (`true`, no company), the paying property manager's name, the site's verified flag |

- **Percent change:** `yoy_change_pct` is Rent.com's; any other change you compute (series month to `current`) is yours, so label it computed.
- **Ids:** listing ids come as search gives them (`lc5898701`, `206824305`, `lv3119690811`, `rf7054291`); a rented or removed listing is a charged `404`.

## Workflow

1. **Place.** `/suggestions` (`{"query": "Austin"}`) for the city, ZIP or neighborhood the site uses, or `/cities` (`{"state": "TX"}`) for a state's cities.
2. **City averages.** `/rent-trends` with `city` and `state`. Note `current` per bed count with `yoy_change_text`, `listing_count` and `series_range`.
3. **Listings.** `/search` with `city` and `state` (or `zip`, or `neighborhood` with both), `beds`, `price_max`, `sort: "price_low"`. Note `total`, `available_units`, each listing's `price`, `rent_by_beds`, deals and price drops.
4. **One rental.** `/listing` with the `id` for every floor plan and unit rent, deposit and date, fees and pet policies. A `kind: "building"` id goes to `/building`, which lists the unit listings at that address.
5. **Report.** Each rent with the listing name, city, bed count, site and `fetched_at` date; Rent.com's averages with their YoY text; the series with its months; no verdict.
6. **Rent series:** the listing pages carry no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `site` | string | `rent` | `rent` (rent.com, 30 a page) or `apartmentguide` (apartmentguide.com, the same rentals, 50 a page; city and state with one `beds` value, or `zip`, and `page` only) |
| `city` | string | none | With `state`: a city name (`Austin`, `New York`, `St. Louis`) or its slug (`new-york`; `/cities` lists them) |
| `state` | string | none | With `city`: a US state, 2-letter code (`TX`) or name (`Texas`) |
| `neighborhood` | string | none | With `city` and `state` (site `rent`): a neighborhood by name or slug (`lincoln-park`, `Downtown Manhattan`) |
| `zip` | string | none | Or a 5-digit US ZIP code (`78704`) instead of city and state; ZIP+4 is cut to 5 |
| `property_type` | string | `apartments` | `apartments`, `houses`, `condos`, `townhouses` or `rooms` (rooms for rent). Site `rent` |
| `beds` | integer, `studio` or list | none | `studio` or 0-4 (4 = 4 or more), or a list of up to 5 (site `rent`). Listings with at least one matching floor plan |
| `baths` | integer | none | 1-4 (4 = 4 or more). Site `rent` |
| `price_min`, `price_max` | integer | none | Monthly rent range, USD (up to 100,000). Site `rent` |
| `sqft_min` | integer | none | Smallest square feet: 100, 200, ... 1600 (steps of 100). Site `rent` |
| `pets` | string | none | `pet_friendly`, `dogs`, `cats` or `no_pets`. Site `rent` |
| `cheap`, `luxury` | boolean | false | The site's cheap or luxury filter, not both. Site `rent` |
| `deals` | boolean | false | Only listings with rent specials. Site `rent` |
| `amenities` | list | none | Up to 8 of: `air-conditioning`, `assisted-living`, `att-fiber`, `available-now`, `cable-ready`, `college`, `controlled-limited-access`, `corporate-billing-available`, `disability-access`, `dishwasher`, `elevator`, `ev-charging`, `extra-storage`, `fitness-center`, `furnished`, `garage`, `gated-access`, `hardwood-floor`, `best`, `high-speed-internet-access`, `income-restricted`, `independent-living`, `laundry-facility`, `loft`, `military`, `new-construction`, `remodeled`, `no-credit-check`, `onsite-personnel`, `oversized-closets`, `patio`, `pool`, `new`, `senior-living`, `short-term-available`, `virtual-tours`, `utilities-included`, `view`, `washer-dryer-connections`, `washer-dryer-in-unit`, `waterfront` (the site's own amenity names). Site `rent` |
| `sort` | string | `best_match` | `best_match`, `price_low`, `price_high`, `beds` (fewest first), `sqft` (smallest first) or `latest` (latest update). Site `rent` |
| `page` | integer | 1 | 1-1000; `pages` and `has_more` say how deep the results go |

### Listing, building, rent trends, suggestions, cities

| Endpoint | Parameters |
|---|---|
| `/listing` | one of `id` (a listing id from search: `lc5898701`, `206824305`, `lv3119690811`) or `url` (the listing's rent.com or apartmentguide.com link; its host sets the site); `site` (`rent` or `apartmentguide`) with `id` |
| `/building` | one of `building_id` (`b147857`, from `listings[].id` where `kind` is `building`) or `url` (a rent.com `/building/` link); `site` `rent` only |
| `/rent-trends` | `city` and `state` (as for search); `site` `rent` only |
| `/suggestions` | `query` (2-80 characters: the start of a city, ZIP, neighborhood, school or property name); `site` |
| `/cities` | `state` (`TX` or `Texas`); `site` `rent` only |

## Examples

### Rent.com's rent trends for a city

```bash
curl -X POST https://api.scavio.dev/api/v1/rentcom/rent-trends \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"city": "Los Angeles", "state": "CA"}'
```

Captured `data` (Los Angeles, CA, 2026-11-26; `series` cut to two of its four bed counts and their end months, `nearby_cities` to 1 of 25 with two bed counts and no `url`, `nearby_neighborhoods` (50) and `notes` dropped):

```json
{
  "site": "rent",
  "location": {"name": "Los Angeles, CA", "city": "Los Angeles", "state": "California", "state_code": "CA", "latitude": 34.0522, "longitude": -118.2428},
  "current": {
    "studio": {"average_rent": 1375, "yoy_change_pct": -37, "yoy_change_text": "-37%"},
    "one_bedroom": {"average_rent": 4950, "yoy_change_pct": 85, "yoy_change_text": "+85%"},
    "two_bedroom": {"average_rent": 6450, "yoy_change_pct": 71, "yoy_change_text": "+71%"},
    "three_bedroom": {"average_rent": 4145, "yoy_change_pct": -16, "yoy_change_text": "-16%"}
  },
  "listing_count": 3275,
  "series": {
    "one_bedroom": [{"month": "2024-04", "label": "Apr 2024", "average_rent": 2695}, {"month": "2025-05", "label": "May 2025", "average_rent": 2717}],
    "two_bedroom": [{"month": "2025-05", "label": "May 2025", "average_rent": 3565}]
  },
  "series_range": {"from": "2024-04", "to": "2025-05", "points": 13},
  "rent_distribution": [
    {"min": 501, "max": 701, "count": 9, "percent": 0},
    {"min": 701, "max": 1001, "count": 74, "percent": 1},
    {"min": 1001, "max": 1501, "count": 669, "percent": 6},
    {"min": 1501, "max": 2101, "count": 2530, "percent": 22},
    {"min": 2101, "max": null, "count": 8173, "percent": 71}
  ],
  "nearby_cities": [{"name": "Pasadena, CA", "listing_count": 899, "averages": {"one_bedroom": {"average_rent": 1700, "yoy_change_pct": -12, "yoy_change_text": "-12%"}, "two_bedroom": {"average_rent": 2000, "yoy_change_pct": -30, "yoy_change_text": "-30%"}}}],
  "url": "https://www.rent.com/california/los-angeles-apartments"
}
```

The notes say it plainly: "It is not updated monthly by Rent.com, so it can end well before today." New York read one-bedroom 5,242 (+4%) and two-bedroom 7,849 (+13%) over 5,497 listings; Chicago 1,275 (-33%) and 1,547 (-38%).

### Search a city, lowest rent first

```bash
curl -X POST https://api.scavio.dev/api/v1/rentcom/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"city": "Austin", "state": "TX", "beds": 2, "sort": "price_low"}'
```

Captured `data` (2026-11-26; `listings` cut to the 3rd and 2nd of 30 with the address parts, bed / bath ranges, `deals`, `highlights`, `image`, `url` and the second card's `deals_text` and `amenities_highlighted` dropped; `query` shortened, `notes` dropped):

```json
{
  "query": {"site": "rent", "city": "Austin", "state": "TX", "zip": null, "property_type": "apartments", "beds": [2], "sort": "price_low", "page": 1},
  "site": "rent",
  "location": {"name": "Austin, TX", "type": "city", "city": "Austin", "state": "Texas", "state_code": "TX", "zip": null, "neighborhood": null, "latitude": 30.2669, "longitude": -97.7428},
  "total": 1819,
  "available_units": 20380,
  "page": 1,
  "page_size": 30,
  "pages": 61,
  "has_more": true,
  "count": 30,
  "average_rent": {
    "studio": {"average_rent": 1499, "yoy_change_pct": 13, "yoy_change_text": "+13%"},
    "one_bedroom": {"average_rent": 1099, "yoy_change_pct": -25, "yoy_change_text": "-25%"},
    "two_bedroom": {"average_rent": 1364, "yoy_change_pct": -25, "yoy_change_text": "-25%"}
  },
  "listings": [
    {"id": "lc6575848", "kind": "listing", "name": "Villas at Mueller", "address_full": "6103 Manor Rd, Austin, TX 78723", "property_type": "APARTMENTS", "price": 665, "price_text": "$665+", "rent_min": 665, "rent_max": 799, "beds_min": 1, "beds_max": 2, "sqft_text": "653–982 Sqft", "rent_by_beds": [{"beds": 1, "rent_min": 699, "rent_max": 699, "sqft_min": null, "sqft_max": null}, {"beds": 2, "rent_min": 665, "rent_max": 665, "sqft_min": null, "sqft_max": null}], "units_available_text": "7 Units Available", "availability": "TODAY", "deals_text": "UP TO 6 WEEKS FREE FOR WELL QUALIFIED APPLICANTS! CONTACT US NOW!", "has_price_drops": true, "price_drops": [134, 134], "pet_friendly": true, "amenities_highlighted": ["Pet Friendly"], "management_company": "Gordon & Bilyeu Property Management", "verified": true, "private_listing": false, "updated_at": "2026-11-26T15:12:31.000Z"},
    {"id": "lc5897975", "kind": "listing", "name": "1883 at Montgomery House (Student Housing - Rent by the Bed)", "address_full": "2700 Nueces St, Austin, TX 78705", "property_type": "APARTMENTS", "price": 587, "price_text": "$587+", "rent_min": 587, "rent_max": 1770, "sqft_text": "529–1442 Sqft", "rent_by_beds": [{"beds": 1, "rent_min": 874, "rent_max": 874, "sqft_min": null, "sqft_max": null}, {"beds": 2, "rent_min": 630, "rent_max": 630, "sqft_min": null, "sqft_max": null}, {"beds": 3, "rent_min": 587, "rent_max": 587, "sqft_min": null, "sqft_max": null}], "units_available_text": "Available Now", "availability": "TODAY", "has_price_drops": false, "price_drops": [], "pet_friendly": true, "management_company": "San Miguel Management", "verified": true, "private_listing": false, "updated_at": "2026-11-26T15:20:40.000Z"}
  ]
}
```

Three of the first five cards on this page were student housing whose names say "Rent by the Bed" (587, 664 and 714); read `rent_by_beds` and the listing's floor plans before treating a low `price` as a unit's rent. With `site: "apartmentguide"` and `{"city": "Los Angeles", "state": "CA", "beds": 1}` the same search shape came back with 3,955 rentals, 13,546 units, 50 a page and `average_rent` `null`. `{"city": "Chicago", "state": "IL", "neighborhood": "lincoln-park", "beds": 1}` returned 646 rentals, the first ones `kind: "building"` (`b39052` ...). A page past the end (`page` 400 of 159) came back empty with the note "page 400 is past the last page (159): Rent.com answered page 1 instead, so this page is empty."

### One rental with floor plans and price drops

```bash
curl -X POST https://api.scavio.dev/api/v1/rentcom/listing \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "lc5918237"}'
```

Captured `data` (2026-11-26; cut to the fields shown: `floor_plans` to 1 of 31 without its `half_baths`, size range, amenities and image, `pet_policies` to 1 of 2; `fees` (all `null`), address parts, ranges, `description`, `amenities`, `parking`, `photos`, `schools`, `nearby`, `vibes`, `similar`, `office_hours` and `notes` among the dropped):

```json
{
  "site": "rent",
  "id": "lc5918237",
  "name": "Avalon Willoughby Square",
  "address_full": "214 Duffield St, Brooklyn, NY 11201",
  "neighborhoods": ["Downtown", "Northwestern Brooklyn", "Downtown Brooklyn"],
  "property_type": "APARTMENTS",
  "total_units": 826,
  "units_available": 12,
  "units_available_text": "10+ Units Available",
  "price": 3687,
  "price_text": "$3,687+",
  "floor_plans": [
    {"id": "lc5918237_NY039A8S772SF_1_1_0", "name": "A8S-772", "beds": 1, "baths": 1, "beds_baths_text": "1 Bd, 1 Ba", "sqft": 772, "rent_min": 5735, "rent_max": 5735, "rent_text": "$5,735/mo", "available_count": 1, "availability_text": "1 Unit Available", "available_date": null, "deposit": 2000,
     "units": [{"unit_id": "58N", "rent": 5735, "rent_text": "$5,735", "sqft": 772, "available_date": null, "available": true, "deposit": 2000, "floor": null}]}
  ],
  "deals_text": "* Save up to $350/mo on select apartments! * Terms and conditions apply.",
  "has_price_drops": true,
  "price_drops": [249, 209, 57, 398],
  "price_drop_overall": 350,
  "pet_policies": [{"type": "CATS_ALLOWED", "label": "Cats Allowed", "comment": null, "initial_fee": null, "additional_rent": null, "deposit": null, "max_pets": null, "weight_limit": null}],
  "walk_score": {"walk": 98, "walk_description": "Walker's Paradise", "bike": 91, "bike_description": "Biker's Paradise", "transit": 100, "transit_description": "Rider's Paradise"},
  "management_company": null,
  "verified": true,
  "updated_at": "2026-11-25T16:50:42.000Z"
}
```

Alcott Village in Houston (`179448193`) read 1,330 for a 968 sq ft two-bedroom with 3 units listed, `management_company` "RPM Living", `special_terms` "Available months 12" and `income_restrictions` (maximum annual income) from $42,480 for 1 occupant to $80,100 for 8. On Apartment Guide, listing `rf7054291` (Los Angeles) carried pet policies with 50 USD monthly pet rent and a 250 deposit per pet. Notes on every listing: "Reviews: none are published on these sites."

### Building, suggestions, cities

- `/building` `{"building_id": "b147857"}`: 8616 60th Ave, Elmhurst, NY 11373, `count` 1 unit listing at 1,188 (1 bed, 788 sq ft, `availability` FUTURE, `private_listing` true), 9 schools. `b1079` (10727 Wilshire Blvd, Los Angeles) held 3 unit listings from 11,950 to 27,436.
- `/suggestions` `{"query": "Austin"}`: 10 places (Austin TX, Austintown OH, Austinville IA ...; each with `type` city, its `id` and `path`) and 10 rentals whose name matches. On Apartment Guide `{"query": "Seattle"}` returned types `city`, `hood`, `school` and `college`.
- `/cities` `{"state": "TX"}`: 600 cities A to Z (Abilene `abilene`, Addison `addison` ...); California 500, New York 450.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def rentcom(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/rentcom/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# Rent.com's current averages for a city (1 credit)
t = rentcom("rent-trends", {"city": "Austin", "state": "TX"})["data"]
for beds, v in t["current"].items():
    print(beds, v["average_rent"], v["yoy_change_text"])
print("series", t["series_range"])

# Two-bedroom listings in the same city, lowest rent first (1 credit)
s = rentcom("search", {"city": "Austin", "state": "TX", "beds": 2, "sort": "price_low"})["data"]
print(s["total"], "rentals,", s["available_units"], "units")
for l in s["listings"]:
    print(l["id"], l["name"], l["price"], l["rent_by_beds"], l["management_company"])

# Store each answer with fetched_at: that stored set is your rent record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Most answers carry `notes`.

- **listing card** (search, building) - `id`, `kind`, `name`, `address`, `address_full`, `city`, `state`, `state_code`, `zip`, `latitude`, `longitude`, `property_type`, `price`, `price_text`, `rent_min`, `rent_max`, `beds_min`, `beds_max`, `baths_min`, `baths_max`, `sqft_min`, `sqft_max`, `bed_text`, `bath_text`, `sqft_text`, `rent_by_beds[]` {`beds`, `rent_min`, `rent_max`, `sqft_min`, `sqft_max`}, `units_available_text`, `availability`, `deals_text`, `deals[]` {`category`, `description`, `expires`}, `special_terms`, `has_price_drops`, `price_drops`, `pet_friendly`, `amenities_highlighted`, `highlights`, `image`, `url`, `management_company`, `verified`, `private_listing`, `updated_at`.
- **search** - `query` (the inputs as read), `site`, `location` {`name`, `type`, `city`, `state`, `state_code`, `zip`, `neighborhood`, `latitude`, `longitude`}, `total`, `available_units`, `page`, `page_size`, `pages`, `has_more`, `count`, `average_rent` {`studio`, `one_bedroom`, `two_bedroom`: {`average_rent`, `yoy_change_pct`, `yoy_change_text`}}, `listings[]`, `notes`.
- **listing** - `site`, `id`, `name`, `url`, `description`, `address`, `address_full`, `city`, `state`, `state_code`, `zip`, `neighborhoods`, `latitude`, `longitude`, `property_type`, `room_for_rent`, `total_units`, `units_available`, `units_available_text`, `availability`, `price`, `price_text`, `rent_min`, `rent_max`, bed / bath / sqft ranges and texts, `floor_plans[]` {`id`, `name`, `beds`, `baths`, `half_baths`, `beds_baths_text`, `sqft`, `sqft_min`, `sqft_max`, `rent_min`, `rent_max`, `rent_text`, `available_count`, `availability_text`, `available_date`, `deposit`, `amenities`, `image`, `units[]` {`unit_id`, `rent`, `rent_text`, `sqft`, `available_date`, `available`, `deposit`, `floor`}}, `fees` {`admin_fee`, `application_fee`, `broker_fee`, `amenity_fee` {`fee`, `type`, `notes`}, `utilities_included`, `utilities_notes`, `tenant_paid_utilities`, `insurance` {`offered_by_property`, `requirement`, `min_liability`, `min_property`, `notes`}, `sales_tax`}, `pet_policies[]` {`type`, `label`, `comment`, `initial_fee`, `additional_rent`, `deposit`, `max_pets`, `weight_limit`}, `pet_friendly`, `parking[]` {`type`, `assigned`, `assigned_fee`, `per_space_fee`, `total_spaces`, `comments`}, `amenities[]` {`name`, `subcategory`, `category`}, `amenities_highlighted`, `highlights`, `office_hours[]` {`day`, `hours[]` {`open`, `close`, `comment`}}, `deals_text`, `deals`, `special_terms`, `has_price_drops`, `price_drops`, `price_drop_overall`, `lease_terms`, `income_restrictions`, `schools[]` {`name`, `type`, `grades`, `rating`, `district`, `distance_miles`, `address`}, `nearby[]` {`category`, `total`, `places[]` {`name`, `type`, `distance_miles`}}, `walk_score` {`walk`, `walk_description`, `bike`, `bike_description`, `transit`, `transit_description`}, `vibes[]` {`category`, `context`}, `photos`, `management_company`, `verified`, `private_listing`, `updated_at`, `similar[]` {`id`, `name`, `address_full`, `price_text`, `rent_min`, `rent_max`, `bed_text`, `url`}, `similar_ids`, `notes`. Fields the site leaves empty are `null` or `[]`.
- **building** - `site`, `id`, `url`, `address`, `address_full`, `city`, `state`, `state_code`, `zip`, `neighborhoods`, `latitude`, `longitude`, `price_text`, `bed_text`, `bath_text`, `sqft_text`, `rent_min`, `rent_max`, `photos`, `count`, `listings[]` (listing cards), `schools`, `notes`.
- **rent trends** - `site`, `location` {`name`, `city`, `state`, `state_code`, `latitude`, `longitude`}, `current` {`studio`, `one_bedroom`, `two_bedroom`, `three_bedroom`: {`average_rent`, `yoy_change_pct`, `yoy_change_text`}}, `listing_count`, `series` {same four keys: [{`month`, `label`, `average_rent`}]}, `series_range` {`from`, `to`, `points`}, `rent_distribution[]` {`min`, `max`, `count`, `percent`}, `nearby_cities[]` and `nearby_neighborhoods[]` {`name`, `url`, `listing_count`, `averages`}, `url`, `notes`.
- **suggestions** - `query`, `site`, `count`, `places[]` {`name`, `type`, `id`, `path`, `url`}, `listings[]` {`id`, `name`, `address`, `address_full`, `city`, `state_code`, `property_type`, `url`}, `notes`.
- **cities** - `state`, `state_code`, `count`, `cities[]` {`name`, `city` (the city input of search and rent trends), `url`}, `notes`.

## Guardrails

- Name it "Rent.com (rent.com, the US rental listing site)" on first mention, "Rent.com" after that; name Apartment Guide when `site` is `apartmentguide`, and say it lists the same rentals.
- Rents: quote each with USD a month, the listing name, city, bed count (and floor plan or unit where given), the site and the `fetched_at` date ("listed on rent.com at 1,330 a month for a two-bedroom, Nov 26, 2026"). `price` is the lowest listed rent, not the rent of every unit.
- Averages: quote `current` and `average_rent` as Rent.com's published averages with `yoy_change_text`; quote `series` only with its `series_range` and never as this month's rent.
- Comparisons: same city, bed count and date; name each site. No verdict on whether a listing is a good deal, no commentary on the rental market beyond the numbers shown.
- No contacts: there are no phone numbers, emails or agent or landlord names, and none should be inferred or looked up. `management_company` is a business name; quote it as given.
- Deals and price drops: quote the listing's own wording and amounts; never compute an effective rent from a special.
- Descriptive only: no commentary on Rent.com's, Apartment Guide's or Redfin's business or listing practices.
- Do not republish listing photos or descriptions. Write rent.com and apartmentguide.com as plain text and cite listing ids, building ids and capture dates rather than linking the sites' pages.
- Terms: Scavio does not collect or store Rent.com data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no contact, tour or application flow. Rent.com's and Apartment Guide's terms of use cover how their sites and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate rents, averages, listing ids, units, dates or fees. Only return what the API returned, with the `fetched_at` time.
- Not available: reviews, phone numbers, emails, agent or landlord names, applications or tours, for-sale homes, rent history beyond the published series.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without a location ("send city and state (e.g. Austin, TX), or zip."); a ZIP with a city ("send zip, or city and state (optionally with neighborhood), not both."); a ZIP that is not 5 digits ("zip must be a 5-digit US ZIP code (e.g. 78704)."); a state that is not a US state ("state must be a US state: a 2-letter code (NY) or a name (New York)."); `price_min` above `price_max`; both `cheap` and `luxury` ("send cheap or luxury, not both."); an amenity outside the list or more than 8; a `sqft_min` outside its steps; a filter Apartment Guide does not take ("site apartmentguide takes city and state (with one beds value) or zip, and page: Apartment Guide's links do not carry ... Send site rent for those filters (Rent.com lists the same rentals)."); `/listing` without exactly one of `id` or `url` ("send one of id or url."), or a building id there ("this is a building id (b...): use the building endpoint."); `/building` without one of `building_id` or `url`; `site: "apartmentguide"` on building, rent trends or cities ("... reads Rent.com's page: send site rent or leave it out (Apartment Guide lists the same rentals)."); suggestions under 2 characters. A body that fails the schema answers "Invalid request: ..." with `details`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Rent.com has no city Notarealcity in Texas (check the spelling; cities lists a state's cities, suggestions finds places).", "Rent.com has no listing lc1000000 (it may have been rented or taken down).", "<site> has no rentals page for ZIP <zip>.", "<site> has no neighborhood <name> in <city>, <ST> (check the spelling; suggestions lists places).", "Rent.com has no building <id>.", "Rent.com has no rent trends for <city>, <ST> (check the spelling; cities lists a state's cities).", "Rent.com has no page for <state>.". Take ids, cities and neighborhoods from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=rent-com-api).
- `502` means Rent.com data was temporarily unavailable ("Rent.com is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Rent.com is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.97.0
npm install scavio@0.98.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: trends } = await scavio.rentcom.rentTrends({ city: "Austin", state: "TX" });
const { data: rentals } = await scavio.rentcom.search({ city: "Austin", state: "TX", beds: 2, sort: "price_low" });
const { data: listing } = await scavio.rentcom.listing({ id: "lc5918237" });
const { data: building } = await scavio.rentcom.building({ building_id: "b147857" });
const { data: cities } = await scavio.rentcom.cities({ state: "TX" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.rentcom.search(...)`, `listing`, `building`, `rent_trends`, `suggestions` and `cities`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 6 endpoints as tools: `search_rentcom`, `get_rentcom_listing`, `get_rentcom_building`, `get_rentcom_rent_trends`, `get_rentcom_suggestions` and `get_rentcom_cities`. Rent.com is opt-in: add `rentcom` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.97.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,rentcom"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/rentcom-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=rent-com-api), [listing](https://scavio.dev/docs/rentcom-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=rent-com-api), [building](https://scavio.dev/docs/rentcom-building?utm_source=agent-skills&utm_medium=skill&utm_campaign=rent-com-api), [rent trends](https://scavio.dev/docs/rentcom-rent-trends?utm_source=agent-skills&utm_medium=skill&utm_campaign=rent-com-api), [suggestions](https://scavio.dev/docs/rentcom-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=rent-com-api), [cities](https://scavio.dev/docs/rentcom-cities?utm_source=agent-skills&utm_medium=skill&utm_campaign=rent-com-api). Overview: [Rent.com API](https://scavio.dev/rentcom-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rent-com-api).
