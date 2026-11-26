---
name: streeteasy-api
description: StreetEasy API for StreetEasy (streeteasy.com, Zillow Group's New York City real estate site covering NYC's five boroughs and North New Jersey) - what NYC rentals ask and what they net after free months, next to the monthly market data StreetEasy publishes for the same neighborhood (a one-bedroom at 482 Kent Avenue in Williamsburg asked 5,295 a month, 4,766 net effective with 1.5 months free on a 15-month lease, while StreetEasy's published median asking rent for Williamsburg one-bedrooms was 4,695 in October 2026); search for sale, for rent or sold in a borough, neighborhood, New Jersey city or all of NYC by price, bedrooms, bathrooms, size, home type, sale type, year built, 24 amenity filters, pets, ZIP, by owner and in contract, 7 sorts, each card with its asking price, net effective rent, months free and lease term, size, building type, status, brokerage and its placement (organic, featured or sponsored); one listing in full by link or by id with listing_type, with price changes, monthly maintenance, taxes and common charges, move-in fees, the unit's past listings and their events, and StreetEasy's recent-listing prices for that bedroom count in the area; one building with its year, floors, units, amenities, policies, developer and architect, NYC building class and evacuation zone, available and past listing counts and price ranges per bedroom count, its units on the market, transit and similar buildings; the building directory of an area; StreetEasy's monthly market data for NYC neighborhoods, boroughs and the city from 2010 (median sale price, median asking price and rent, inventory, sale-to-list ratio, recorded sales, days on market, share of price and rent cuts, price and rental indexes). 5 endpoints, 1 credit per call. NYC and North NJ, USD; market data for New York City only. No agent or landlord names or contacts, no no-fee filter, no reviews.
version: 1.0.0
tags: streeteasy, streeteasy-com, streeteasy-api, streeteasy-rentals, streeteasy-sales, streeteasy-sold, streeteasy-search, streeteasy-listing, streeteasy-building, streeteasy-buildings, streeteasy-market-data, nyc-real-estate, nyc-rentals, nyc-apartments, nyc-condos, nyc-co-ops, manhattan-rentals, brooklyn-rentals, queens-real-estate, jersey-city-rentals, hoboken, net-effective-rent, months-free, rent-concessions, median-asking-rent, median-sale-price, sale-to-list-ratio, rental-inventory, price-cuts, building-data, new-development, real-estate, real-estate-data, rental-market, usd, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/streeteasy-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=streeteasy-api
---

# StreetEasy API - NYC Rentals, Sales, Buildings, Market Data

Read StreetEasy (streeteasy.com, Zillow Group's New York City real estate site covering NYC's five boroughs and North New Jersey): search for sale, for rent and sold, one listing in full, one building, an area's building directory, and the monthly market data StreetEasy publishes for New York City. Every answer is what StreetEasy's public pages and published data files show a visitor without an account at the moment of the call, in USD. All 5 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages StreetEasy shows to any visitor, and the market data it publishes, and returns them as JSON for analysis. It uses no StreetEasy account, no saved searches, no application, no tour or contact request.

**The job this skill is for: what NYC rentals ask, what they net after free months, and how that sits against StreetEasy's own numbers.** `/search` returns each rental's asking rent with StreetEasy's `net_effective_rent`, `months_free` and `lease_term_months`; `/market` returns the median asking rent StreetEasy publishes for the neighborhood by bedroom count; `/listing` adds `area_price_stats`, StreetEasy's recent-listing prices for that bedroom count in the listing's area (including New Jersey, which has no published market series). Captured 2026-11-26 (1 credit per call):

| Area | Listing (`beds`) | Asking (`price`) | `net_effective_rent` (`months_free`, `lease_term_months`) | StreetEasy's figure for the same bedroom count |
|---|---|---|---|---|
| Williamsburg | 482 Kent Avenue #PHC (1) | 5,295 | 4,766 (1.5, 15) | Median asking rent, one bedroom, Williamsburg, 2026-10: 4,695 (`/market`) |
| Williamsburg | 265 Lorimer Street #704 (1) | 4,075 | none | Same: 4,695 |
| Waterfront, Jersey City | 99 Provost Street #4315 (1) | 4,730 | 4,336 (2, 24) | `area_price_stats.rental` for 1 bed: median 3,865 across 381 listings (min 2,300, max 6,750); NJ has no `/market` series |
| Bedford-Stuyvesant | 12 Halsey Street #828 (0, studio) | 3,225 | none | `area_price_stats.rental` for studios: median 2,795 across 34 listings |

The Williamsburg cards came from `{"mode": "rent", "area": "Williamsburg", "amenities": ["elevator", "gym"], "pets_allowed": true}` (98 rentals); the market median covers every one-bedroom StreetEasy counts in the neighborhood, so name the filters beside each comparison. Put asking rent, net effective rent and the median side by side with their labels and months, and leave the gap uninterpreted: a median is not what any one unit should rent for. For the same address on other sites use `zillow-property-data`, `trulia-api` or `rent-com-api`, matched on address, unit and bedroom count.

Ten limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Paid placements come first.** StreetEasy puts featured and sponsored cards ahead of the organic results, and the sort orders the organic ones only. `placement` (`organic`, `featured`, `sponsored`) is on every card: a Manhattan sale page held 6 featured, 29 organic and 3 sponsored; a rent page 2 featured, 11 organic and 1 sponsored. Leave paid cards out of a price ranking, or label them.
- **Asking rent vs net effective rent.** `price` is the asking rent per month; `net_effective_rent` is StreetEasy's figure after `months_free` over `lease_term_months`. On rentals StreetEasy applies the price filter to the net effective rent where a listing has one, so `price` can be above `price_max` (a note says so).
- **Sold prices live on the listing.** On a sold search the card `price` is the last asking price; `/listing` returns `sold_price` where StreetEasy shows it. Sold searches default to `newest` (StreetEasy's own default order starts with 2006-2008 sales).
- **Paging is capped.** Up to 100 pages; a sale page holds about 38 cards and a rent page 14, and StreetEasy stops sale results at 37 pages (Brooklyn sold: `total` 137,793, `pages` 37). Narrow the area or filters to reach the rest.
- **A listing id needs its type.** `/listing` takes `url` (a card's `url`), or `id` with `listing_type` (`sale` for sale and sold listings, `rent`); the wrong type is a charged `404` ("StreetEasy has no listing 5151221 (check listing_type: sale or rent).").
- **Market data is New York City only.** `/market` is StreetEasy's published monthly series, from 2010-01 to 2026-10 in the captures, for 182 areas (176 neighborhoods, the 5 boroughs and NYC); `price_index` and `rental_index` run from 2005 and 2007 for Brooklyn, Manhattan, Queens and NYC. A New Jersey area is a `400`; an area StreetEasy publishes no series for is a charged `404`. Ratios and shares are fractions (0.974 = 97.4%).
- **No agent or landlord personal data.** No agent or private landlord names, emails, phones or photos. `brokerage` is the company as StreetEasy shows it, with its license type and license address; a by-owner listing has `listed_by_owner: true` and no name.
- **Slow pages.** In the captures search answered in 3 to 38 seconds (an NYC-wide ZIP search in 13), a listing in 2 to 27, a building in 2 to 5, the building directory in 3 to 5 and market data in 1 to 5. Set a client timeout of at least 240 seconds and send one request at a time.
- **What is not there.** No no-fee filter, no transit or school filter on search, no agent profiles, no reviews, no place suggestions (send area names, slugs or ids), no market data for New Jersey, no application, tour or contact.

StreetEasy publishes no public API for its listings; it publishes its market data as monthly data files, which `/market` reads. This skill reads StreetEasy's public pages and those files with one Scavio key.

See also: `zillow-property-data` (Zillow search and property pages across the US), `trulia-api` (US neighborhood surveys, reviews and market snapshots), `rent-com-api` and `rentcafe-api` (US rental listings), `realtor-com-property-data` and `redfin-property-data`. Same unit or same area only: match on address, unit and bedroom count, and name the site and month with every number.

## When to trigger

Use this skill when the user asks to:
- Compare NYC asking rents and net effective rents (months free, lease term) with StreetEasy's published median asking rent for a neighborhood
- Search StreetEasy for sale, for rent or sold in a borough, neighborhood or North New Jersey city, by price, bedrooms, bathrooms, size, home type, sale type, year built, amenities, pets, ZIP, by owner or in contract
- Read one StreetEasy listing in full: price changes, maintenance, taxes and common charges, move-in fees, the unit's past listings, StreetEasy's area prices for that bedroom count
- Read one NYC or North NJ building: year built, floors, units, amenities, policies, developer, architect, NYC building class, available and past listings per bedroom count, units on the market
- List the buildings StreetEasy has in an area (condo, co-op or rental)
- Pull StreetEasy's monthly market data for NYC neighborhoods, boroughs or the city: median sale price, median asking price or rent, inventory, sale-to-list ratio, recorded sales, days on market, price and rent cuts, price and rental indexes

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=streeteasy-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=streeteasy-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example 25 neighborhoods: one rental search and one market series each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, market data answered in 1-5 seconds, building 2-5, buildings 3-5, listing 2-27 and search 3-38. Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/streeteasy/search` | For sale, for rent or sold in an area: StreetEasy's criteria as read, total, pages, `has_more`; each card with placement, address, unit, area, price, net effective rent, months free, lease term, beds, baths, size, building type, sale type, status, dates, brokerage, open house | 1 |
| `POST /api/v1/streeteasy/listing` | One listing by link or by id with `listing_type`: status changes, rooms, amenities, features, views, pricing (price changes, maintenance, taxes, common charges, payment estimate, net effective rent, move-in and monthly fees), the unit's past listings, open houses, media, `area_price_stats`, brokerage and license | 1 |
| `POST /api/v1/streeteasy/building` | One building by slug or link: year, floors, units, amenities, policies, details (developer, architect, manager, deed owner when a business, leasing office), NYC facts, inventory per bedroom count, units on the market, schools, transit, nearby places, similar buildings | 1 |
| `POST /api/v1/streeteasy/buildings` | An area's building directory, about 11 a page: name, slug, address, active sales and rentals, units, floors, year built, status, type | 1 |
| `POST /api/v1/streeteasy/market` | StreetEasy's monthly market data for NYC: one metric and filter, every published area or one, `months` with `values` aligned to them and the latest value per area | 1 |

## Market

New York City's five boroughs and North New Jersey (Jersey City, Hoboken and their neighborhoods), USD. There is no `country` or `currency` input. `area` takes a StreetEasy area by name, slug or id: a borough (`Manhattan` 100, `Brooklyn` 300, `Queens` 400, `Bronx`, `Staten Island`), a neighborhood (`Williamsburg` 302, `Upper West Side`), a New Jersey city (`Jersey City` 1001000, `Hoboken` 1004000), or `nyc` for all of NYC and NJ. Market data covers New York City only.

## Prices and market fields

| Field | Meaning |
|---|---|
| `price` | Asking price, or asking rent per month on rentals, USD; on a sold card the last asking price |
| `net_effective_rent`, `months_free`, `lease_term_months` | StreetEasy's net effective rent and the concession it is computed from (4,730 asking, 2 months free on 24 months, 4,336 net) |
| `total_monthly_price` | The monthly total where StreetEasy shows one |
| `placement` | `organic`, `featured` or `sponsored`: the last two are StreetEasy's paid placements |
| `pricing.sold_price`, `pricing.rented_price` | The recorded sale or rent where StreetEasy shows it (listing) |
| `pricing.price_changes[]` | {`price`, `at`}: the listing's price changes |
| `pricing.monthly_maintenance`, `monthly_taxes`, `monthly_common_charges`, `estimated_monthly_payment` | Co-op and condo carrying costs and StreetEasy's payment estimate, as StreetEasy gives them |
| `pricing.move_in_fees[]` | {`type`, `label`, `amount`, `refundable`, `required`, `timing`} (application fee, security deposit) |
| `property_history[]` | The unit's past listings, each {`listing_id`, `brokerage`, `listed_by_owner`, `sold_date`, `off_market_date`, `events[]` {`date`, `price`, `status`, `price_change_percent`}} |
| `area_price_stats` | {`beds`, `sale` {`min`, `median`, `max`, `listings`}, `rental` {...}}: StreetEasy's recent-listing prices for that bedroom count in the listing's area |
| `inventory.sales[]`, `inventory.rentals[]` (building) | Per bedroom count: `available_count`, `available_min_price`, `available_max_price`, `past_count`, `past_min_price`, `past_max_price` |
| `areas[].values` (market) | One value per entry of `months`, `null` where StreetEasy publishes none; `latest` is the last non-null month |

- **Percent or dollar change:** compute it from two values and label it computed (Williamsburg one-bedroom median asking rent 3,994 in 2024-01 to 4,695 in 2026-10 is 701 higher, computed).
- **Ids:** a card's `id` with `listing_type`, or its `url`, opens `/listing`; a listing's `building.slug` opens `/building`; a directory row's `slug` too.

## Workflow

1. **The area.** Send a borough, neighborhood or NJ city name (`Williamsburg`), its slug or its id; every answer returns `area` with its id.
2. **Listings.** `/search` with `mode`, `area` and filters. Separate `placement` `organic` from the paid cards; note `price`, `net_effective_rent`, `months_free` and `lease_term_months`.
3. **StreetEasy's numbers.** `/market` with `type`, `metric`, `filter` (bedrooms or home type) and the same `area` for the published series; for New Jersey, or a bedroom-level area figure, read `area_price_stats` from `/listing`.
4. **One listing.** `/listing` with the card's `url` (or `id` + `listing_type`) for price changes, fees, carrying costs and the unit's past listings.
5. **The building.** `/building` with `building.slug` for its inventory per bedroom count and units on the market; `/buildings` lists an area's buildings.
6. **Report.** Each price with StreetEasy, the address and unit, bedroom count, placement and the `fetched_at` date; each market value with its metric label, filter label, area and month; no verdict.
7. **Over time:** `/market` is already monthly history. For listings, store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `area` | string or integer | required | A StreetEasy area by name, slug or id (see Market); `nyc` for all of NYC and NJ |
| `mode` | string | `sale` | `sale` (for sale), `rent` (rentals) or `sold` (past sales) |
| `price_min`, `price_max` | integer | none | USD (rent per month on `rent`) |
| `beds_min`, `beds_max` | integer | none | 0-10 (0 = studio); `beds_min` = `beds_max` asks for exactly that many |
| `baths_min` | integer | none | 1-10 |
| `sqft_min` | integer | none | Smallest size in square feet (listings without a size are left out) |
| `home_types` | list | none | `sale` and `sold` only: `condo`, `coop`, `house`, `multifamily` |
| `sale_types` | list | none | `sale` and `sold` only: `sponsor` (a sponsor unit, sold by the developer), `resale`, `foreclosure`, `restricted` |
| `year_built_min`, `year_built_max` | integer | none | 1700 to five years ahead |
| `amenities` | list | none | All required: `washer_dryer`, `dishwasher`, `elevator`, `doorman`, `laundry`, `gym`, `parking`, `pool`, `storage`, `private_outdoor_space`, `public_outdoor_space`, `central_ac`, `furnished`, `fireplace`, `loft`, `city_view`, `garden_view`, `park_view`, `skyline_view`, `waterview`, `guarantor_ok`, `pied_a_terre`, `childrens_playroom`, `smoke_free` |
| `pets_allowed` | boolean | false | Only listings that allow pets |
| `zip` | string | none | Only listings in this ZIP code (with `area` `nyc` to search every borough) |
| `by_owner` | boolean | false | `rent` only: listings posted by the owner (no broker) |
| `status` | string | `active` | `sale` only: `active` or `in_contract` (StreetEasy's pending) |
| `sort` | string | `recommended` (`newest` on `sold`) | `recommended`, `newest`, `recently_updated`, `price_desc`, `price_asc`, `sqft_desc`, `sqft_asc`; orders the organic results |
| `page` | integer | 1 | 1-100; `pages` and `has_more` say how deep the results go |

### Listing (`/listing`), building (`/building`), buildings (`/buildings`)

| Endpoint | Parameters |
|---|---|
| `/listing` | one of `url` (a StreetEasy listing link or path, `listings[].url`: `/building/<building>/<unit>` or `/sale/<id>`) or `id` (digits, `listings[].id`) with `listing_type` (`sale` for sale and sold listings, `rent`) |
| `/building` | one of `slug` (`building.slug`, e.g. `eastlight-condominium`) or `url` (the building's link; a listing link in it works too) |
| `/buildings` | `area` (required, as in search); `building_type` `condo`, `coop` or `rental` (default every type); `page` 1-1000 (about 11 buildings a page) |

### Market data (`/market`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `sales` | `sales` or `rentals` |
| `metric` | string | `median_sale_price` / `median_asking_rent` | sales: `price_index`, `inventory`, `sale_to_list_ratio`, `recorded_sales`, `median_sale_price`, `median_asking_price`, `median_days_on_market`, `share_of_price_cuts`. rentals: `rental_index`, `inventory`, `median_asking_rent`, `share_of_rent_cuts` |
| `filter` | string | `all` | sales by home type: `all`, `condo`, `coop`, `single_family`. rentals by bedrooms: `all`, `studio`, `one_bedroom`, `two_bedrooms`, `three_plus_bedrooms`. `price_index` and `rental_index` are published for `all` only |
| `area` | string or integer | every published area | One NYC neighborhood, borough or `NYC` by name, slug or id |
| `start_month`, `end_month` | string | the full series | `YYYY-MM` (`2024-01`) |

## Examples

### StreetEasy's median asking rent for one-bedrooms in a neighborhood

```bash
curl -X POST https://api.scavio.dev/api/v1/streeteasy/market \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "rentals", "metric": "median_asking_rent", "filter": "one_bedroom", "area": "Williamsburg", "start_month": "2024-01"}'
```

Captured `data` (2026-11-26; `months` and `values` cut to the first 3 and the last 3 of 34):

```json
{
  "type": "rentals",
  "metric": "median_asking_rent",
  "metric_label": "Median Asking Rent",
  "filter": "one_bedroom",
  "filter_label": "One Bedroom",
  "first_month": "2024-01",
  "last_month": "2026-10",
  "months": ["2024-01", "2024-02", "2024-03", "2026-08", "2026-09", "2026-10"],
  "count": 1,
  "areas": [
    {
      "area": "Williamsburg",
      "area_id": 302,
      "area_slug": "williamsburg",
      "borough": "Brooklyn",
      "area_type": "neighborhood",
      "latest": {"month": "2026-10", "value": 4695},
      "values": [3994, 4150, 4000, 4800, 4680, 4695]
    }
  ],
  "notes": ["Monthly values as StreetEasy publishes them in its market data (New York City; values[i] is for months[i], null where StreetEasy publishes none). Prices in USD; ratios and shares as fractions."]
}
```

`{"type": "sales", "metric": "median_sale_price", "area": "Williamsburg", "start_month": "2024-01"}` read 1,450,000 for 2026-10. `{"type": "sales", "metric": "sale_to_list_ratio", "area": "Brooklyn", "start_month": "2026-01"}` read 0.9739 for 2026-10. `{"type": "sales", "metric": "inventory", "filter": "condo", "area": "Manhattan", "start_month": "2025-06"}` read 4,127 condos in 2026-10. `{"type": "rentals", "metric": "rental_index", "area": "NYC"}` returned the series from 2007-01, latest 4,014. `{"type": "sales", "metric": "share_of_price_cuts"}` without an area returned all 182 areas (Astoria 0.151 in 2026-10).

### Rentals in a borough under a price

```bash
curl -X POST https://api.scavio.dev/api/v1/streeteasy/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mode": "rent", "area": "Brooklyn", "price_max": 4000}'
```

Captured `data` (2026-11-26; `listings` cut to the 2nd, 3rd and 4th of 14 cards, each shortened to the fields shown; `notes` dropped):

```json
{
  "mode": "rent",
  "area": {"id": 300, "name": "Brooklyn", "slug": "brooklyn", "borough": "Brooklyn"},
  "criteria": "area:300|price:-4000|status:open",
  "sort": "recommended",
  "page": 1,
  "total": 1559,
  "pages": 100,
  "has_more": true,
  "count": 14,
  "listings": [
    {"id": "5202889", "placement": "featured", "address": "1634 Flatbush Avenue", "unit": "#1261", "area": "East Flatbush", "area_id": 358, "zip": "11210", "price": 3203, "currency": "USD", "net_effective_rent": 3070, "months_free": 0.5, "lease_term_months": 12, "beds": 2, "full_baths": 1, "building_type": "rental", "status": "active", "available_date": "2026-11-12", "source_type": "partner", "brokerage": "Rentopia"},
    {"id": "5209805", "placement": "organic", "address": "20 Rockwell Place", "unit": "#1731Q", "area": "Fort Greene", "area_id": 304, "zip": "11201", "price": 3557, "currency": "USD", "beds": null, "full_baths": 1, "building_type": "rental", "status": "active", "available_date": "2026-11-24", "source_type": "partner", "brokerage": "Bushburg"},
    {"id": "5167226", "placement": "organic", "address": "1057 Atlantic Avenue", "unit": "#1520", "area": "Bedford-Stuyvesant", "area_id": 310, "zip": "11238", "price": 4605, "currency": "USD", "net_effective_rent": 3838, "months_free": 2.5, "lease_term_months": 15, "beds": 1, "full_baths": 1, "building_type": "rental", "status": "active", "available_date": "2026-09-24", "is_new_development": true, "has_3d_tour": true, "source_type": "partner", "brokerage": "MNS"}
  ]
}
```

The third card shown asks 4,605, above `price_max` 4,000: its net effective rent is 3,838, and the note reads "On rentals StreetEasy applies the price filter to the net effective rent when a listing has one (net_effective_rent), so price can be above price_max." Other captures: Manhattan for sale (`{"area": "Manhattan"}`) 6,303 listings in 37 pages, 38 cards a page; in contract (`"status": "in_contract"`) 2,643; Brooklyn sold (`{"mode": "sold", "area": "Brooklyn"}`) 137,793 with `off_market_date` per card (365 Clinton Avenue #5D, 895,000 last asking, 2026-11-23); Jersey City rentals 2,927; Hoboken for sale built 2000 or later (`year_built_min` 2000) 23; by-owner rentals in ZIP 11211 across NYC (`{"mode": "rent", "area": "nyc", "zip": "11211", "by_owner": true}`) 3, each `listed_by_owner: true` with no brokerage (plus one sponsored card from a brokerage).

### One listing in full

```bash
curl -X POST https://api.scavio.dev/api/v1/streeteasy/listing \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://streeteasy.com/building/everton/4315"}'
```

Captured `data` (2026-11-26; a subset of the fields shown: `description`, the amenity and feature lists, `media`, `status_changes`, the null pricing fields and the building's `amenities` and `area` dropped):

```json
{
  "id": "5184968",
  "url": "https://streeteasy.com/building/everton/4315",
  "listing_type": "rent",
  "status": "active",
  "address": {"street": "99 Provost Street", "unit": "#4315", "city": "JERSEY CITY", "state": "NJ", "zip": "07302", "full": "99 Provost Street #4315"},
  "area": {"id": 1001250, "name": "Waterfront", "slug": "waterfront", "borough": "New Jersey"},
  "building": {"id": "7003769", "name": "Everton", "slug": "everton", "type": "Rental unit", "status": "new_development", "year_built": 2026, "floors": 60, "units": 802, "policies": ["smoke_free", "guarantors_accepted", "pets_allowed"]},
  "days_on_market": 40,
  "listed_date": "2026-10-17",
  "available_date": "2026-10-01",
  "rooms": 3,
  "beds": 1,
  "full_baths": 1,
  "pricing": {
    "price": 4730,
    "currency": "USD",
    "price_changes": [{"price": 4730, "at": "2026-10-17T19:00:20.000-04:00"}],
    "net_effective_rent": 4336,
    "months_free": 2,
    "lease_term_months": 24,
    "move_in_fees": [],
    "monthly_fees": []
  },
  "property_history": [
    {"listing_id": "5184968", "brokerage": "LyvWell Apartments NJ", "listed_by_owner": false, "sold_date": null, "off_market_date": null, "events": [{"date": "2026-10-17", "price": 4730, "status": "active", "price_change_percent": null}]}
  ],
  "area_price_stats": {
    "beds": 1,
    "sale": {"min": 521000, "median": 645000, "max": 1200000, "listings": 33},
    "rental": {"min": 2300, "median": 3865, "max": 6750, "listings": 381}
  },
  "source_type": "feed",
  "listed_by_owner": false,
  "brokerage": {"name": "LyvWell Apartments NJ", "listed_as": "LyvWell Apartments NJ", "license_type": null, "license_address": null},
  "agent_brokerages": []
}
```

By id: `{"id": "5151221", "listing_type": "rent"}` returned a Bedford-Stuyvesant studio at 3,225 with `move_in_fees` [{"label": "Application fee", "amount": 20, ...}, {"label": "Security deposit", "amount": 3225, "refundable": true, ...}], 78 days on market and `brokerage.name` "Triumph Property Group Ltd" with license type "Corporate Broker"; the same id with `listing_type: "sale"` was a charged `404`. A by-owner Williamsburg townhouse rental (`/building/143-north-3rd-street-brooklyn/th5`, 15,000, 3 beds, 2,000 sqft) had `listed_by_owner: true`, no brokerage, and a `property_history` showing the unit rented at 15,500 in July 2025 through a brokerage. A sold Bedford-Stuyvesant listing (`/sale/1854253`, 5 beds, 3,484 sqft) read `status` sold, `off_market_date` 2026-11-13, last asking 2,999,999.

### One building and an area's buildings

```bash
curl -X POST https://api.scavio.dev/api/v1/streeteasy/building \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "455-fdr-drive-new_york"}'
```

Captured (2026-11-26): 455 Fdr Drive, Lower East Side, Manhattan, `type` "Co-op building", `nyc` {"building_class": "D4", "building_class_description": "Elevator Cooperative", "hurricane_evacuation_zone": 3, "has_abatements": false}, transit (Essex St, F J M Z, 0.58 miles ...) and nearby parks (East River Park, under 500 feet). `inventory.sales` per bedroom count:

| `beds` | `available_count` | Available price range | `past_count` | Past price range |
|---|---|---|---|---|
| 1 bed | 5 | 425,000-639,000 | 93 | 465,000-625,000 |
| 2 beds | 6 | 765,000-849,000 | 74 | 715,000-2,100,000 |
| 3 beds | 1 | 1,100,000 | 21 | 999,000 |

`sales` listed its 12 units on the market (#B406, in contract, 550,000, 1 bed ...) and `similar_buildings` 3 co-ops nearby with their active sales and price ranges. The new Everton building in Jersey City (`{"url": "https://streeteasy.com/building/everton"}`) read 60 floors, 802 units, year 2026, `details.developer` "BGRE and G&S Investors", `details.architect` "Beyer Blinder Belle", and `inventory.rentals` 1 bed: 5 available at 4,300-5,200, 10 past at 3,895-4,900.

- `/buildings` `{"area": "Williamsburg"}`: `total` 5,775 in 525 pages, 11 a page, first One Domino Square - Condos (`one-domino-square-condos`, 8 South 4th Street, 160 units, 45 floors, 2024, 13 active sales) and 420 Kent Avenue (605 units, 22 floors, 13 active rentals). `{"area": "Upper West Side", "building_type": "coop"}`: 783 co-ops, first Lincoln Towers (432 units, 1962). `{"area": "Manhattan", "building_type": "rental"}`: 14,853 buildings.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def streeteasy(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/streeteasy/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# StreetEasy's published median asking rent for one-bedrooms (1 credit)
m = streeteasy("market", {"type": "rentals", "metric": "median_asking_rent",
                          "filter": "one_bedroom", "area": "Williamsburg", "start_month": "2026-01"})["data"]
latest = m["areas"][0]["latest"]
print(m["metric_label"], m["filter_label"], m["areas"][0]["area"], latest["month"], latest["value"])

# One-bedroom rentals in the same neighborhood, organic results only (1 credit)
s = streeteasy("search", {"mode": "rent", "area": "Williamsburg", "beds_min": 1, "beds_max": 1})["data"]
for c in s["listings"]:
    if c["placement"] != "organic":
        continue
    print(c["address"], c["unit"], "asking", c["price"], "net", c["net_effective_rent"],
          "free", c["months_free"], "lease", c["lease_term_months"])

# Store each answer with fetched_at: that stored set is your record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Search and market answers carry `notes`.

- **card** (search) - `id`, `url`, `placement`, `address`, `unit`, `area`, `area_id`, `zip`, `state`, `latitude`, `longitude`, `price`, `currency`, `sold_price`, `net_effective_rent`, `months_free`, `lease_term_months`, `total_monthly_price`, `price_change`, `beds`, `full_baths`, `half_baths`, `sqft`, `building_type`, `sale_type`, `status`, `available_date`, `off_market_date`, `is_new_development`, `furnished`, `has_videos`, `has_3d_tour`, `source_type`, `listed_by_owner`, `brokerage`, `open_house` {`start`, `end`, `appointment_only`}, `photo`, `photos`.
- **search** - `mode`, `area` {`id`, `name`, `slug`, `borough`}, `criteria` (StreetEasy's search criteria as it read them), `sort`, `page`, `total`, `pages`, `has_more`, `count`, `listings[]`, `notes`.
- **listing** - `id`, `url`, `listing_type`, `status`, `address` {`street`, `unit`, `city`, `state`, `zip`, `full`}, `area`, `building` {`id`, `name`, `slug`, `url`, `type`, `status`, `year_built`, `floors`, `units`, `area`, `latitude`, `longitude`, `amenities`, `policies`}, `sale_type`, `description`, `days_on_market`, `listed_date`, `available_date`, `off_market_date`, `sold_date`, `updated_at`, `status_changes[]` {`status`, `at`}, `rooms`, `beds`, `full_baths`, `half_baths`, `sqft`, `lot_sqft`, `amenities`, `doorman`, `parking`, `shared_outdoor_space`, `storage`, `features`, `fireplaces`, `private_outdoor_space`, `views`, `pricing` {`price`, `currency`, `sold_price`, `rented_price`, `price_changes`, `monthly_maintenance`, `monthly_taxes`, `monthly_common_charges`, `estimated_monthly_payment`, `max_financing_percent`, `tax_deduction_percent`, `net_effective_rent`, `months_free`, `lease_term_months`, `total_monthly_price`, `furnished_rent`, `security_deposit`, `due_up_front`, `move_in_fees`, `monthly_fees`, `additional_fees`}, `property_history[]`, `open_houses[]`, `media` {`photos`, `floor_plans`, `video_count`, `has_3d_tour`}, `area_price_stats`, `source_type`, `listed_by_owner`, `mls_number`, `brokerage` {`name`, `listed_as`, `license_type`, `license_address`}, `agent_brokerages[]` {`brokerage`, `license_type`, `license_address`}.
- **building** - `id`, `name`, `slug`, `url`, `address`, `area`, `neighborhood`, `type`, `unit_type`, `status`, `year_built`, `floors`, `units`, `latitude`, `longitude`, `description`, `amenities`, `doorman`, `parking`, `shared_outdoor_space`, `storage`, `policies`, `pets`, `is_land_lease`, `is_waterfront`, `is_green`, `details` {`developer`, `architect`, `interiors`, `landscape_design`, `construction`, `manager`, `marketing_team`, `owner`, `sales_start_date`, `leasing_start_date`, `sales_office`, `leasing_office`, `website`}, `nyc` {`building_class`, `building_class_description`, `community_district`, `council_district`, `police_precinct`, `hurricane_evacuation_zone`, `has_abatements`, `abatement_type`, `abatement_expiration`}, `inventory` {`sales`, `rentals`, `active_sale_ids`, `active_rental_ids`}, `sales[]` and `rentals[]` {`id`, `url`, `unit`, `status`, `price`, `currency`, `price_changed_at`, `price_change`, `beds`, `full_baths`, `half_baths`, `sqft`, `sale_type`, `months_free`, `lease_term_months`, `available_date`, `furnished`, `brokerage`, `open_house`, `photo`, `floor_plan`}, `schools`, `transit[]` {`name`, `routes`, `distance`}, `nearby` {`parks`, `colleges`, `museums`}, `similar_buildings[]` {`id`, `name`, `url`, `address`, `type`, `year_built`, `active_sales`, `active_rentals`, `sale_price_min`, `sale_price_max`, `rent_min`, `rent_max`, `photo`}, `photo_count`, `photos`.
- **buildings** - `area`, `building_type`, `page`, `total`, `pages`, `has_more`, `count`, `buildings[]` {`id`, `name`, `slug`, `url`, `address`, `active_sales`, `active_rentals`, `units`, `floors`, `year_built`, `status`, `buildings_in_complex`, `type`, `neighborhood`, `latitude`, `longitude`, `photo`}.
- **market** - `type`, `metric`, `metric_label`, `filter`, `filter_label`, `first_month`, `last_month`, `months`, `count`, `areas[]` {`area`, `area_id`, `area_slug`, `borough`, `area_type` (neighborhood, borough or city), `latest` {`month`, `value`}, `values`}, `notes`.

## Guardrails

- Name it "StreetEasy (streeteasy.com, Zillow Group's New York City real estate site)" on first mention, "StreetEasy" after that.
- Prices: quote each with USD, StreetEasy, the address and unit, bedroom count, `placement` and the `fetched_at` date ("asking 4,730 a month, 4,336 net effective with 2 months free on a 24-month lease, 99 Provost Street #4315, Jersey City, on streeteasy.com Nov 26, 2026"). Keep asking rent and net effective rent apart, with their labels.
- Paid placements: say when a card is `featured` or `sponsored`, and keep paid cards out of any ranking of organic results.
- Market data: quote `metric_label`, `filter_label`, the area and the month with every value, as "StreetEasy's published market data"; ratios and shares are fractions, so convert them and say so. Never present a median as what one unit should cost.
- Comparisons: the same bedroom count and area, the filters named, the month or date beside each number. No verdict on whether a listing is a good deal beyond the numbers shown.
- No agent or landlord personal data: name the brokerage company only, and do not try to identify an agent or a private landlord. A brokerage name can be a person's trade name: quote it only where the brokerage matters.
- Fair housing: describe listings and areas with the data as StreetEasy gives it; do not characterize an area by who lives there, and do not steer anyone toward or away from one.
- Descriptive only: no commentary on StreetEasy's business, pricing practices or policies.
- Do not republish StreetEasy photos or descriptions. Write streeteasy.com as plain text and cite listing ids, building slugs, area ids and capture dates rather than linking StreetEasy pages.
- Terms: Scavio does not collect or store StreetEasy data: each call fetches the public page or published data file at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no application, tour or contact flow. StreetEasy's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, rents, concessions, listing ids, building slugs or market values. Only return what the API returned, with the `fetched_at` time.
- Not available: agent or landlord names and contacts, a no-fee filter, transit or school search filters, reviews, place suggestions, New Jersey market data, application, tour or contact.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search or buildings without `area`, or an area StreetEasy does not list ("area: ... is not a StreetEasy area. Send a borough (Manhattan, Brooklyn, Queens, Bronx, Staten Island), a neighborhood (Williamsburg, Upper West Side), a New Jersey city (Jersey City, Hoboken), nyc for all of NYC and NJ, or a StreetEasy area id (100 Manhattan, 300 Brooklyn, 1001000 Jersey City)."); a filter outside its mode ("by_owner applies to mode rent only.", "home_types applies to mode sale and sold only.", "status applies to mode sale only."); a minimum above its maximum ("beds: the minimum is above the maximum."); a ZIP that is not 5 digits; a `sort`, `amenities` or type value outside its list; `page` past 100; `/listing` without exactly one of `url` or `id` ("send one of url or id."), `id` without `listing_type` ("listing_type is required with id: sale (sale and sold listings) or rent."), or a link that is not a StreetEasy listing; `/building` without exactly one of `slug` or `url`; market data for New Jersey ("StreetEasy publishes market data for New York City only (its five boroughs and their neighborhoods), not New Jersey."), a metric with a filter it is not published for ("metric price_index is published for filter all only (sales)."), a month not written `YYYY-MM`, or `start_month` after `end_month`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "StreetEasy has no listing 5151221 (check listing_type: sale or rent).", "StreetEasy has no listing at /building/<building>/<unit>." (a removed listing), "StreetEasy has no building <slug>.", "StreetEasy has no building directory for <area>.", "StreetEasy has no <mode> search for area <area>.", "StreetEasy publishes no <metric> series for <area>." (an area name with no published series). Take ids, links and slugs from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=streeteasy-api).
- `502` means StreetEasy data was temporarily unavailable ("StreetEasy is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds (a rental index call that answered `502` succeeded on the next try in the captures).
- `503` with a `Retry-After` header means the service is busy ("StreetEasy is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.97.0
npm install scavio@0.98.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: rents } = await scavio.streeteasy.search({ mode: "rent", area: "Brooklyn", price_max: 4000 });
const { data: unit } = await scavio.streeteasy.listing({ url: "https://streeteasy.com/building/everton/4315" });
const { data: building } = await scavio.streeteasy.building({ slug: "455-fdr-drive-new_york" });
const { data: buildings } = await scavio.streeteasy.buildings({ area: "Williamsburg" });
const { data: market } = await scavio.streeteasy.market({ type: "rentals", metric: "median_asking_rent", filter: "one_bedroom", area: "Williamsburg" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.streeteasy.search(...)`, `listing`, `building`, `buildings` and `market`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 5 endpoints as tools: `search_streeteasy`, `get_streeteasy_listing`, `get_streeteasy_building`, `get_streeteasy_buildings` and `get_streeteasy_market`. StreetEasy is opt-in: add `streeteasy` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.97.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,streeteasy"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/streeteasy-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=streeteasy-api), [listing](https://scavio.dev/docs/streeteasy-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=streeteasy-api), [building](https://scavio.dev/docs/streeteasy-building?utm_source=agent-skills&utm_medium=skill&utm_campaign=streeteasy-api), [buildings](https://scavio.dev/docs/streeteasy-buildings?utm_source=agent-skills&utm_medium=skill&utm_campaign=streeteasy-api), [market data](https://scavio.dev/docs/streeteasy-market?utm_source=agent-skills&utm_medium=skill&utm_campaign=streeteasy-api). Overview: [StreetEasy API](https://scavio.dev/streeteasy-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=streeteasy-api).
