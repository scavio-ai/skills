---
name: hotpads-api
description: HotPads API for HotPads (hotpads.com, Zillow Group's US rental search site) - what a US rental really costs and how its rent has moved, as HotPads shows it (Lincoln at Bankside in the Bronx listed base rent of $2,680 to $5,160 across 143 units, a monthly total of $2,686.25 to $5,166.25 with the required fees, $33.90 due at move-in, plus electricity and thermal billed as "Varies"; a 6-bed house in Dallas, ZIP 75228, was listed at $2,999 on Nov 14, 2026 and cut 18.3% to $2,450 on Nov 25, with 22 rent events back to 2012) with every move-in, monthly and usage fee the property manager lists, required or optional; rental search for apartments, houses, condos, townhomes, rooms, sublets or for-rent-by-owner listings in a US city, neighborhood, borough or ZIP code, 40 buildings a page, 4 sorts and filters for beds, baths, rent, size, dogs or cats, in-unit laundry, parking or furnished and keywords, with the filters HotPads applied; one listing or building in full with floor plans and units, amenities, pet policies, lease terms, special offers, total-monthly-price notes, HotPads' comparison with the ZIP, city and county average rent, views and inquiries, schools and similar listings; the rent history of a listing (listed, price changed, removed, with percent change and source); location suggestions with the area ids search takes. 5 endpoints, 1 credit per call. US only, USD. No landlord or agent names or contacts, no reviews, no Canada.
version: 1.0.0
tags: hotpads, hotpads-com, hotpads-api, hotpads-search, hotpads-rentals, hotpads-apartments, hotpads-listing, hotpads-fees, hotpads-price-history, hotpads-rent-history, hotpads-rooms, hotpads-sublets, hotpads-for-rent-by-owner, hotpads-suggestions, zillow-group, rental-listings, apartments-for-rent, houses-for-rent, rooms-for-rent, for-rent-by-owner, rent-prices, rental-fees, move-in-costs, total-monthly-price, rent-history, floor-plans, pet-policy, area-average-rent, rental-market, rental-data, real-estate, real-estate-data, us-real-estate, usd, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/hotpads-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=hotpads-api
---

# HotPads API - Rental Listings, Fees, Rent Price History

Read HotPads (hotpads.com, Zillow Group's US rental search site): rental search, one listing or building in full, the costs and fees the property manager lists, the rent history of a listing, and location suggestions. Every answer is what HotPads' public pages show a visitor without an account at the moment of the call, in USD. All 5 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages HotPads shows to any visitor and returns them as JSON for analysis. It uses no HotPads account, no saved searches, no tour or contact request, no rental application and no lead form.

**The job this skill is for: what a rental really costs, and how its rent has moved.** `/fees` returns every cost the property manager lists for a listing (base rent, the required and optional monthly fees, move-in fees, usage fees such as late fees) with HotPads' own move-in and monthly totals; `/price-history` returns the listing's rent events with the percent change and source; `/listing` adds HotPads' comparison with the ZIP, city and county average rent. Captured 2026-11-26 (1 credit per call):

| Listing | Base rent | Monthly total with required fees | Due at move-in | What else the listing shows |
|---|---|---|---|---|
| Lincoln at Bankside, Bronx, NY (building, 143 units in the fee table) | $2,680 - $5,160 | $2,686.25 - $5,166.25 | $33.90 | Thermal admin fee $6.25 a month; electricity and thermal "Varies"; late fee $50; early termination fee $5,360 - $10,320 (optional); up to 4 months free on a 24-month lease (special offer) |
| Ferrante, Los Angeles, CA 90012 (building, 22 units in the fee table) | $1,799 - $3,239 | $1,799 - $3,239 | "Contact" | 27 views and 12 inquiries on HotPads since Nov 26 |
| Room for rent, Dallas, TX 75241 (by owner) | $450 | $450 | $400 security deposit | "Based on a 6-month lease"; $450 against a Dallas city average of $1,154 (-61%, HotPads' comparison) |
| 6-bed house, 11227 Drummond Dr, Dallas, TX 75228 | $2,450 | - | - | Rent history: listed $2,999 on 2026-11-14, cut to $2,450 on 2026-11-25 (-18.3%); 22 events back to 2012; -28% against the ZIP 75228 average of $3,403 |

Totals and comparisons are HotPads' own figures as it shows them; the fees are what the property manager lists, not a quote or a lease. Quote each with the listing, its date and HotPads' label. For the same area on other sites use `zillow-property-data`, `rent-com-api`, `rentcafe-api` or `apartment-list-api`, matched on address, beds and date.

Ten limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Fees are the property manager's listing.** `/fees` returns what the property manager lists on HotPads; an amount HotPads states as text ("Varies", "Contact") is in `amount.text`. `move_in_total`, `monthly_total` and `base_rent` are HotPads' own min and max across the listing's units.
- **Rent history where HotPads publishes it.** `/price-history` takes the listing's `price_history.listing_alias` and `price_history.model_id`; `price_history` is `null` on a listing when HotPads publishes none (a large building such as Lincoln at Bankside had none). Events are `listedForRent`, `priceChanged` and `listingRemoved`, each with `change_pct` and `source` as HotPads gives them; `truncated: true` means HotPads cut the history.
- **Search pages are buildings.** Search returns HotPads' map pins (a building or a single home), 40 a page, each with its listings; `total_units` and `total_buildings` are HotPads' counts. A page past the last is empty with a note (Los Angeles houses: 95 pages).
- **Filters HotPads applied.** `applied_filters` echoes what HotPads applied and a note lists any filter it did not. HotPads takes one pet type and one amenity (parking or furnished) per search.
- **Area comparison is HotPads'.** `area_comparison` is HotPads' comparison of the listing's rent with the neighborhood, ZIP, city and county averages it publishes; on large buildings it can be empty.
- **No landlord or agent personal data.** No landlord, agent or leasing-contact names, phones or emails. `company_name` is the management company on property-managed listings only (`paid_multifamily: true`). Price-history `source` is the listing feed or company HotPads names.
- **US only, USD.** HotPads Canada is not offered: Canadian areas and listings are a `400`, and Canadian results are left out of searches and suggestions with a note.
- **Slow pages.** In the captures search answered in 2.7 to 15.8 seconds, a listing in 4 to 17.7, price history in 1.3 to 6.2, fees in 1.9 to 3.5 and suggestions in 1.1 to 4.2. Set a client timeout of at least 180 seconds and send one request at a time.
- **What is not there.** No reviews (HotPads has no first-party reviews), no rent-trend pages, no Spanish pages, no tours, contact forms or applications, no listings outside the US.

HotPads offers no public data API (its listing feeds are for property managers sending listings in). This skill reads HotPads' public pages with one Scavio key.

See also: `zillow-property-data` (Zillow rentals, sales and property detail), `rent-com-api`, `rentcafe-api`, `apartment-list-api` (rent reports and market rent data), `trulia-api` and `streeteasy-api` (New York City). Same listing or same area only: match on address and beds, name the site and date with every number.

## When to trigger

Use this skill when the user asks to:
- Find what a US rental costs in full on HotPads: base rent, required and optional monthly fees, move-in fees, usage fees and HotPads' move-in and monthly totals
- Read the rent history of a HotPads listing: when it was listed, every price change with its percent, and when it was removed
- Search HotPads apartments, houses, condos, townhomes, rooms, sublets or for-rent-by-owner listings in a city, neighborhood, borough or ZIP code, with beds, baths, rent, size, pets, in-unit laundry, parking, furnished or keyword filters, sorted by price or newest
- Read one HotPads listing or building in full: floor plans with units and rents, amenities, pet policies, lease terms, special offers, total-monthly-price notes, area rent comparison, views and inquiries, schools and similar listings
- Look up the area ids HotPads uses for a city, neighborhood, borough, county, ZIP code, school or address

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=hotpads-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=hotpads-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example 16 listings: one listing, one fees and one price-history call each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, suggestions answered in 1.1-4.2 seconds, fees 1.9-3.5, price history 1.3-6.2, listing 4-17.7 and search 2.7-15.8. Set a client timeout of at least 180 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/hotpads/search` | Rentals in a US city, neighborhood, borough or ZIP code by type (apartments, houses, condos, townhomes, rooms, sublets, by owner): 40 buildings a page with their listings (rent range, beds, baths, size, unit counts, price drops, special offer, tags, room details, photos), totals, minimum rent, filters and the filters HotPads applied | 1 |
| `POST /api/v1/hotpads/listing` | One listing, unit or building by link or id: rents, description, lease terms, office hours, special offers, amenities and highlights, pet policies, floor plans with units, total-monthly-price notes, history, views and inquiries, area rent comparison, schools, similar listings, photos, and the inputs of price history and fees | 1 |
| `POST /api/v1/hotpads/price-history` | The rent history HotPads publishes for one listing: listed, price changed and removed events with rent, rent per square foot, percent change and source | 1 |
| `POST /api/v1/hotpads/fees` | The costs and fees the property manager lists: base rent, move-in and monthly totals, required and optional move-in and monthly fees, usage fees, unit count and the disclaimer | 1 |
| `POST /api/v1/hotpads/suggestions` | Location suggestions: areas (city, neighborhood, borough, county, ZIP code, school) with the `resource_id` search takes, and matching addresses with the `id` listing takes | 1 |

## Market

US only (including DC and Puerto Rico), USD. There is no `country`, `currency` or `language` input. Rents are monthly.

## Fee and rent-history fields

| Field | Meaning |
|---|---|
| `base_rent`, `monthly_total`, `move_in_total` | {`min`, `max`, `text`}: HotPads' own figures across the listing's units (`text` when HotPads states it as text, such as "Contact") |
| `move_in_fees`, `monthly_fees` | {`required`, `optional`}: each fee {`type` (BASE_RENT, ADMINISTRATION, SECURITY_DEPOSIT, ELECTRICITY_FEE, GAS_FEE, RENTERS_INSURANCE_FEE, CUSTOM ...), `name`, `amount` {`min`, `max`, `text`}, `count` {`min`, `max`}, `notes`} |
| `usage_fees[]` | Fees charged when they apply (LATE_FEE, INSUFFICIENT_FUNDS_FEE ...), same shape |
| `disclaimer` | The property manager's pricing disclaimer as HotPads shows it |
| `events[]` (price history) | {`date`, `type` (listedForRent, priceChanged, listingRemoved), `price`, `price_per_sqft`, `change_pct`, `currency`, `source`} newest first |
| `area_comparison[]` (listing) | {`type` (neighborhood, zip, city, county), `name`, `area_average_price`, `listing_price`, `difference`, `vs_area_pct`} |
| `total_monthly_price[]` (listing) | {`id`, `text`}: HotPads' note per unit ("Total price includes the base rent ($2,680) and fixed monthly fees ($7) that the property manager lists as required.") |
| `popularity` (listing) | {`since`, `views`, `inquiries`, `favorites`}: HotPads' counts since the date it states (about 7 days) |

- **Two totals.** A listing's `price_min` / `price_max` (Lincoln at Bankside $2,687 - $5,667) cover every unit HotPads shows; `/fees` totals ($2,686.25 - $5,166.25) cover the units in the property manager's fee table (`unit_count` 143). Quote each with its label.

## Workflow

1. **Area.** `/suggestions` (`{"text": "brooklyn"}`): `areas[].resource_id` (`brooklyn-new-york-ny`) is the `area` of `/search`; an address suggestion carries `listings[].id` for `/listing`.
2. **Search.** `/search` with `area`, `type` and filters. Check `applied_filters` and the notes.
3. **One listing.** `/listing` with `url` from `buildings[].listings[].url` (or `id` from `buildings[].id`). Note `alias` and `price_history`.
4. **Costs.** `/fees` with `listing_alias` = the listing's `alias`.
5. **Rent history.** `/price-history` with `price_history.listing_alias` and `price_history.model_id` (only when `price_history` is not null).
6. **Report.** Each rent with HotPads, the listing, USD and the `fetched_at` date; fees as the property manager lists them; totals and comparisons as HotPads' figures; no verdict on a listing or landlord.
7. **Over time:** store each answer with its `fetched_at`; rents and fees change as listings update, and that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `area` | string | required | A HotPads area: a suggestions `areas[].resource_id` (`brooklyn-new-york-ny`, `austin-tx`, `90012`) or a place such as `Austin, TX` (2-160 characters). US only |
| `type` | string | `apartments` | `apartments`, `houses`, `condos`, `townhomes`, `rooms` (rooms for rent), `sublets` or `by_owner` (for rent by owner) |
| `beds` | integer | none | An exact bedroom count, 0-8 (0 is a studio) |
| `beds_min` | integer | none | Or at least this many bedrooms, 1-8 (not with `beds`) |
| `baths_min` | number | none | At least this many bathrooms: 1, 1.5, 2, 3 or 4 |
| `price_min`, `price_max` | integer | none | Monthly rent, USD (0-100,000) |
| `sqft_min`, `sqft_max` | integer | none | Square feet, 0-50,000 |
| `pets` | string | none | `dogs` or `cats` (one per search) |
| `in_unit_laundry` | boolean | false | Listings with an in-unit washer and dryer |
| `amenity` | string | none | `parking` or `furnished` (one per search) |
| `keywords` | string | none | Keywords HotPads matches in listings (`balcony`), up to 80 characters |
| `sort` | string | `default` | `default` (HotPads' own order), `price_low`, `price_high` or `newest` |
| `page` | integer | 1 | 1-200, 40 buildings a page; `pages` says how many |

### Listing (`/listing`), price history (`/price-history`), fees (`/fees`), suggestions (`/suggestions`)

| Endpoint | Parameters |
|---|---|
| `/listing` | one of `url` (a hotpads.com listing link: `buildings[].listings[].url` or `buildings[].url`, ending `/pad`, `/building` or `/<unit>/pad`) or `id` (a building id, `buildings[].id` or suggestions `listings[].id`, e.g. `skrzz0`) |
| `/price-history` | `listing_alias` (required, 6-20 characters: the listing's `price_history.listing_alias`) and `model_id` (required: `price_history.model_id`, e.g. `738529`) |
| `/fees` | `listing_alias` (required: the listing's `alias` or search `listings[].alias`, e.g. `24ga0pwypzg8y`) |
| `/suggestions` | `text` (3-80 characters: a city, neighborhood, borough, county, ZIP code, school or address); `limit` (1-10, default 6) |

## Examples

### What a rental costs in full

```bash
curl -X POST https://api.scavio.dev/api/v1/hotpads/fees \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"listing_alias": "24ga0pwypzg8y"}'
```

Captured `data` (2026-11-26, Lincoln at Bankside, Bronx; `disclaimer` shortened, the second usage fee dropped):

```json
{
  "listing_alias": "24ga0pwypzg8y",
  "currency": "USD",
  "move_in_total": {"min": 33.9, "max": 33.9, "text": null},
  "monthly_total": {"min": 2686.25, "max": 5166.25, "text": null},
  "base_rent": {"min": 2680, "max": 5160, "text": null},
  "move_in_fees": {
    "required": [
      {"type": "ADMINISTRATION", "name": "Thermal Final Bill Fee", "amount": {"min": 16.95, "max": 16.95, "text": null}, "count": {"min": 1, "max": 1}, "notes": []},
      {"type": "CUSTOM", "name": "Thermal Setup Fee", "amount": {"min": 16.95, "max": 16.95, "text": null}, "count": {"min": 1, "max": 1}, "notes": []}
    ],
    "optional": [
      {"type": "CUSTOM", "name": "Early Termination Fee ($5,360-10,320)", "amount": {"min": 5360, "max": 10320, "text": null}, "count": {"min": 0, "max": 1}, "notes": []}
    ]
  },
  "monthly_fees": {
    "required": [
      {"type": "BASE_RENT", "name": "Monthly base rent", "amount": {"min": 2680, "max": 5160, "text": null}, "count": {"min": 1, "max": 1}, "notes": ["See unit for details"]},
      {"type": "ELECTRICITY_FEE", "name": "Electricity", "amount": {"min": null, "max": null, "text": "Varies"}, "count": {"min": 1, "max": 1}, "notes": []},
      {"type": "GAS_FEE", "name": "Thermal", "amount": {"min": null, "max": null, "text": "Varies"}, "count": {"min": 1, "max": 1}, "notes": []},
      {"type": "ADMINISTRATION", "name": "Thermal Admin Fee", "amount": {"min": 6.25, "max": 6.25, "text": null}, "count": {"min": 1, "max": 1}, "notes": []}
    ],
    "optional": [
      {"type": "RENTERS_INSURANCE_FEE", "name": "Renter's Insurance Charges ($16.75)", "amount": {"min": 16.75, "max": 16.75, "text": null}, "count": {"min": 0, "max": 1}, "notes": []}
    ]
  },
  "usage_fees": [
    {"type": "LATE_FEE", "name": "Late Fee", "amount": {"min": 50, "max": 50, "text": null}, "count": {"min": 1, "max": 1}, "notes": []}
  ],
  "unit_count": 143,
  "disclaimer": "All pricing and fees information is provided by the housing provider. ...",
  "notes": [
    "Costs and fees as the property manager lists them on HotPads (hotpads.com, Zillow Group's rental search site), in USD. An amount HotPads states as text (Varies) is in amount.text.",
    "move_in_total, monthly_total and base_rent are HotPads' own estimates (min and max across the listing's units)."
  ]
}
```

### The rent history of a listing

```bash
curl -X POST https://api.scavio.dev/api/v1/hotpads/price-history \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"listing_alias": "5759ydyqtn49h", "model_id": "738529"}'
```

Captured `data` (2026-11-26, 11227 Drummond Dr, Dallas; `events` cut to the 5 newest of 22, `notes` dropped):

```json
{
  "listing_alias": "5759ydyqtn49h",
  "model_id": "738529",
  "currency": "USD",
  "truncated": false,
  "count": 22,
  "events": [
    {"date": "2026-11-25", "type": "priceChanged", "price": 2450, "price_per_sqft": 1, "change_pct": -18.3, "currency": "USD", "source": "Zillow Rentals"},
    {"date": "2026-11-14", "type": "listedForRent", "price": 2999, "price_per_sqft": 1, "change_pct": 20, "currency": "USD", "source": "Zillow Rentals"},
    {"date": "2025-11-07", "type": "listingRemoved", "price": 2499, "price_per_sqft": 1, "change_pct": 0, "currency": "USD", "source": "Zillow Rentals"},
    {"date": "2025-10-29", "type": "priceChanged", "price": 2499, "price_per_sqft": 1, "change_pct": -16.7, "currency": "USD", "source": "Zillow Rentals"},
    {"date": "2025-07-28", "type": "listedForRent", "price": 2999, "price_per_sqft": 1, "change_pct": 66.6, "currency": "USD", "source": "Zillow Rentals"}
  ]
}
```

The oldest event is a listing at $1,750 on 2012-11-20. A Reseda, Los Angeles listing read 25 events, the newest relisted at $4,400 on 2026-11-26 (-56%) after $10,000 in May 2025.

### Search rentals in an area

```bash
curl -X POST https://api.scavio.dev/api/v1/hotpads/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"area": "brooklyn-new-york-ny", "beds": 1, "sort": "price_low"}'
```

Captured `data` (2026-11-26; `buildings` cut to 1 of 20, its `url` and the listing `url` and `photos` dropped, `filters` and `notes` dropped):

```json
{
  "area": "brooklyn-new-york-ny",
  "type": "apartments",
  "currency": "USD",
  "applied_filters": [
    {"key": "beds", "min": 1, "max": 1},
    {"key": "propertyTypes", "values": ["apartment"]},
    {"key": "additionalOpts", "values": ["requiresPrice"]}
  ],
  "sort": "price_low",
  "applied_sort": "priceAsc",
  "title": "Brooklyn Apartments for Rent",
  "total_units": 198,
  "total_buildings": 20,
  "min_price": 1600,
  "page": 1,
  "page_size": 40,
  "pages": 1,
  "has_more": false,
  "count": 20,
  "listing_count": 20,
  "buildings": [
    {
      "id": "253uvg5",
      "latitude": 40.69819783485631,
      "longitude": -73.9329993724823,
      "listing_count": 1,
      "listings": [
        {
          "alias": "2h6br0aghw3wa",
          "property_type": "large",
          "listing_type": "room",
          "title": "Co-living Brand new modern building in Bushwick",
          "unit": null,
          "address": {"street": "31 Troutman St", "city": "Brooklyn", "state": "NY", "zip": "11206"},
          "beds_min": 1, "beds_max": 1, "baths_min": 1.5, "baths_max": 1.5, "sqft_min": 100, "sqft_max": 200,
          "price_min": 1600, "price_max": 1850, "currency": "USD",
          "unit_count": 3, "new_unit_count": 0, "price_drop_count": 0,
          "special_offer": null, "tags": [], "labels": ["paidMultifamily", "trusted"],
          "total_monthly_price": null,
          "room": {"furnished": false, "private_bath": null, "roommates": null, "room_sqft": null},
          "photo_count": 8,
          "activated": "2025-04-10T21:32:38.390Z",
          "updated": "2026-11-03T07:28:38.487Z"
        }
      ]
    }
  ]
}
```

Other captured searches: `{"area": "austin-tx", "type": "apartments", "beds_min": 2, "price_max": 3000, "pets": "dogs", "in_unit_laundry": true, "amenity": "parking"}` matched 3,323 units in 223 buildings from $782, every filter echoed in `applied_filters`; `{"area": "austin-tx", "type": "rooms"}` matched 100 rooms in 83 buildings from $370 (3 pages; a furnished room with a private bath and 1 roommate at $900); `{"area": "dallas-tx", "type": "by_owner"}` matched 775 units in 600 buildings from $750 (15 pages); `{"area": "90012"}` matched 742 units in 42 buildings from $1,378.

### One listing

```bash
curl -X POST https://api.scavio.dev/api/v1/hotpads/listing \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "23y7mk6"}'
```

Captured `data` (2026-11-26, Lincoln at Bankside; `floorplans` cut to 1 of 54, `total_monthly_price` to 1 of 198, `special_offers` shortened; `description`, `amenities`, `highlights`, `office_hours`, `schools`, `similar_listings`, `photos`, the URLs and `notes` dropped):

```json
{
  "id": "23y7mk6",
  "alias": "24ga0pwypzg8y",
  "title": "Lincoln at Bankside",
  "property_type": "large",
  "listing_type": "rental",
  "is_building": true,
  "address": {"street": "5 Lincoln Ave", "city": "Bronx", "state": "NY", "zip": "10454", "neighborhood": "Mott Haven"},
  "currency": "USD",
  "price_min": 2687,
  "price_max": 5667,
  "price_text": "$2,687 - $5,667",
  "beds_min": 0, "beds_max": 3, "baths_min": 1, "baths_max": 2.5, "sqft_min": 468, "sqft_max": 1395,
  "unit_count": 350,
  "new_unit_count": 143,
  "special_offer": "Special offer",
  "special_offers": ["Up to 4 months free base rent for a 24-month lease on market-rate apartments! ..."],
  "amenity_summary": {"pets": "Cats and Dogs Allowed", "laundry": "In Unit", "parking": true, "airConditioning": false, "gym": true, "pool": true, "security": "Security", "dishwasher": false},
  "floorplans": [
    {"model_id": "5250787", "name": "2BB", "beds": 2, "baths": 2.5, "sqft": 1395, "price_min": 5166.25, "price_max": 5166.25, "price_text": "$5,166", "availability_date": null, "unit_count": 1,
     "units": [{"id": "W-0001E", "name": "W-0001E", "beds": 2, "baths": 2.5, "sqft": 1395, "price_min": 5166.25, "price_max": 5166.25, "price_text": "$5,166", "availability_date": null, "is_new": false, "price_drop": null, "listed": "1 month ago"}]}
  ],
  "total_monthly_price": [{"id": "5250612", "text": "Total price includes the base rent ($2,680) and fixed monthly fees ($7) that the property manager lists as required."}],
  "history": {"created": "2024-10-01T12:32:59.217Z", "activated": "2026-03-06T05:09:03.886Z", "updated": "2026-11-26T13:18:42.613Z"},
  "popularity": {"since": "2026-11-26T14:39:30.646Z", "views": 67, "inquiries": 21, "favorites": 0},
  "area_comparison": [],
  "price_history": null,
  "company_name": "LyvWell Apartments LLC",
  "paid_multifamily": true,
  "trusted": true,
  "rental_application": "undecided",
  "income_restricted": false,
  "senior_housing": false,
  "student_housing": false,
  "military_housing": false
}
```

A single home (`{"id": "skrzz0"}`, 11227 Drummond Dr, Dallas) reads `price_text` "$2,450", 6 beds, 3 baths, 3,240 sq ft, `lease_terms` "We prefer a longer lease than normal. $75 application fee per adult.", dogs allowed, `area_comparison` against ZIP 75228 ($3,403, -28%), Dallas and Dallas County, `company_name` null and `price_history` {"listing_alias": "5759ydyqtn49h", "model_id": "738529"}.

### Suggestions

- `/suggestions` `{"text": "brooklyn"}`: 5 areas: Brooklyn, New York, NY (`borough`, `resource_id` "brooklyn-new-york-ny"), Brooklyn Park, MN, Brooklyn, MI, Brooklyn Center, MN, Brooklyn, OH. `{"text": "90012"}` returned the ZIP and 4 addresses with their listing `id` (`1m2jd5g`, 1053 Figueroa Ter).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def hotpads(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/hotpads/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# Houses for rent in Dallas, newest first (1 credit)
s = hotpads("search", {"area": "dallas-tx", "type": "houses", "beds_min": 3, "sort": "newest"})["data"]
print(s["total_units"], "units,", s["pages"], "pages")
first = s["buildings"][0]["listings"][0]

# The listing in full (1 credit)
l = hotpads("listing", {"url": first["url"]})["data"]
print(l["title"], l["price_text"], l["area_comparison"])

# What it costs in full (1 credit)
f = hotpads("fees", {"listing_alias": l["alias"]})["data"]
print("monthly", f["monthly_total"], "move-in", f["move_in_total"])

# Its rent history, when HotPads publishes one (1 credit)
if l["price_history"]:
    h = hotpads("price-history", l["price_history"])["data"]
    for e in h["events"][:5]:
        print(e["date"], e["type"], e["price"], e["change_pct"])

# Store each answer with fetched_at: that stored set is your record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every answer carries `notes`.

- **search listing** (`buildings[].listings[]`) - `alias` (the `listing_alias` of fees), `url` (the `url` of listing), `property_type`, `listing_type`, `title`, `unit`, `address` {`street`, `city`, `state`, `zip`}, `beds_min`, `beds_max`, `baths_min`, `baths_max`, `sqft_min`, `sqft_max`, `price_min`, `price_max`, `currency`, `unit_count`, `new_unit_count`, `price_drop_count`, `special_offer`, `tags` (New Today, Price Drop, Special Offer ...), `labels` (trusted, specialOffers, paidMultifamily ...), `total_monthly_price`, `room` {`furnished`, `private_bath`, `roommates`, `room_sqft`}, `photo_count`, `photos`, `activated`, `updated`.
- **search** - `area`, `type`, `currency`, `filters`, `applied_filters`, `sort`, `applied_sort`, `title`, `total_units`, `total_buildings`, `min_price`, `page`, `page_size`, `pages`, `has_more`, `count`, `listing_count`, `buildings[]` {`id` (the `id` of listing), `url`, `latitude`, `longitude`, `listing_count`, `listings[]`}, `notes`.
- **listing** - `id`, `alias`, `url`, `building_url`, `title`, `name`, `property_type`, `listing_type`, `is_building`, `unit`, `active`, `address` {`street`, `city`, `state`, `zip`, `neighborhood`}, `latitude`, `longitude`, `currency`, `price_min`, `price_max`, `price_text`, beds / baths / sqft ranges, `unit_count`, `new_unit_count`, `price_drop_count`, `description`, `is_mls`, `mls_disclaimer`, `furnished`, `lease_terms`, `office_hours`, `special_offer`, `special_offers`, `amenities`, `highlights`, `amenity_summary`, `pet_policies` {`cats`, `dogs`: [{`allowed`, `size`, `deposit`, `one_time_fee`, `monthly_fee`, `max_allowed`, `max_weight`, `comment`, `restriction`}]}, `floorplans[]` {`model_id`, `name`, `beds`, `baths`, `sqft`, `price_min`, `price_max`, `price_text`, `availability_date`, `layouts`, `unit_count`, `units[]`}, `total_monthly_price[]` {`id`, `text`}, `history` {`created`, `activated`, `updated`}, `popularity` {`since`, `views`, `inquiries`, `favorites`}, `area_comparison[]`, `schools[]` {`name`, `type`, `grades`, `rating`, `is_private`, `students`, `city`}, `similar_listings`, `photo_count`, `photos`, `price_history` {`listing_alias`, `model_id`} or null, `company_name`, `paid_multifamily`, `trusted`, `rental_application`, `income_restricted`, `senior_housing`, `student_housing`, `military_housing`, `notes`.
- **price history** - `listing_alias`, `model_id`, `currency`, `truncated`, `count`, `events[]` {`date`, `type`, `price`, `price_per_sqft`, `change_pct`, `currency`, `source`}, `notes`.
- **fees** - `listing_alias`, `currency`, `move_in_total`, `monthly_total`, `base_rent` ({`min`, `max`, `text`}), `move_in_fees` and `monthly_fees` {`required`, `optional`: [{`type`, `name`, `amount` {`min`, `max`, `text`}, `count` {`min`, `max`}, `notes`}]}, `usage_fees[]`, `unit_count`, `disclaimer`, `notes`.
- **suggestions** - `text`, `areas[]` {`type` (city, neighborhood, borough, county, zip, school), `label`, `resource_id`, `region_id`, `city`, `county`, `state`}, `listings[]` {`id`, `label`, `city`, `state`}, `count`, `notes`.

## Guardrails

- Name it "HotPads (hotpads.com, Zillow Group's rental search site)" on first mention, "HotPads" after that.
- Rents: USD, monthly, with HotPads, the listing (title or address) and the `fetched_at` date. Say whether a figure is a listing's rent range, a floor plan or unit rent, or a fee-table total.
- Fees: "as the property manager lists them on HotPads", required and optional kept apart; an amount given as text ("Varies", "Contact") is quoted as that text, never filled in. `move_in_total` and `monthly_total` are HotPads' estimates, not a quote or a lease.
- Rent history: quote each event with its date, type, rent, `change_pct` and `source` as HotPads gives them; where `price_history` is null, say HotPads publishes none for that listing.
- `area_comparison` and `popularity` are HotPads' own figures; quote them with their labels and dates.
- Fair housing: describe listings and areas with the data as HotPads gives it; do not characterize an area by who lives there, and do not steer anyone toward or away from an area or a listing.
- No landlord or agent personal data: name the management company only where `company_name` is given, and do not try to identify a landlord, an owner, an agent or a leasing contact.
- Descriptive only: no commentary on HotPads' business, a property manager's pricing practices or policies.
- Do not republish HotPads photos or listing descriptions in bulk. Write hotpads.com as plain text and cite listing ids, aliases and capture dates rather than linking HotPads pages.
- Terms: Scavio keeps no copy: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no lead, tour, contact or application flow. HotPads' terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate rents, fees, totals, events, aliases or ids. Only return what the API returned, with the `fetched_at` time.
- Not available: landlord or agent names, phones or emails, reviews, rent-trend pages, Spanish pages, Canada, tours, contact forms or applications.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: an area that is not a HotPads area ("area must be a HotPads area: a suggestions areas[].resource_id (e.g. brooklyn-new-york-ny, austin-tx, 90012) or a place such as Austin, TX."), a ZIP without 5 digits ("area: a ZIP code has 5 digits."), a Canadian area or listing ("HotPads Canada is not offered (US only, including DC and Puerto Rico)."); `beds` with `beds_min` ("send beds (an exact count; 0 is a studio) or beds_min, not both."); `baths_min` outside its list ("baths_min must be one of 1, 1.5, 2, 3, 4."); a `_min` above its `_max` ("price_min must not be above price_max."); two amenities ("HotPads applies one amenity per search: one of parking, furnished."); a `type`, `sort` or `pets` value outside its list; `/listing` without exactly one of `url` or `id` ("send one of url or id."), or a link that is not a HotPads listing; a malformed alias ("listing_alias must be a HotPads listing alias (listing alias or search listings[].alias, e.g. 5759ydyqtn49h)."); `/price-history` without `model_id` ("model_id is required: send the listing's price_history.listing_alias and price_history.model_id (HotPads gives a price history only to listings whose price_history is set)."); suggestions under 3 characters ("text must be at least 3 characters.").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "HotPads has no search page for this area. Use suggestions to find the area HotPads uses (areas[].resource_id).", "HotPads has no listing at this link (it may have been taken down). Use a url from search listings[].url.", "HotPads has no price history for this listing alias and model id (use the listing's price_history.listing_alias and price_history.model_id).", "HotPads has no costs and fees for this listing alias (use listing alias or search listings[].alias).". Take areas, urls, aliases and model ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=hotpads-api).
- `502` means HotPads data was temporarily unavailable ("HotPads is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("HotPads is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.98.0
npm install scavio@0.99.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: rentals } = await scavio.hotpads.search({ area: "austin-tx", beds_min: 2, price_max: 3000, pets: "dogs" });
const { data: listing } = await scavio.hotpads.listing({ id: "skrzz0" });
const { data: fees } = await scavio.hotpads.fees({ listing_alias: "24ga0pwypzg8y" });
const { data: history } = await scavio.hotpads.priceHistory({ listing_alias: "5759ydyqtn49h", model_id: "738529" });
const { data: places } = await scavio.hotpads.suggestions({ text: "brooklyn" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.hotpads.search(...)`, `listing`, `price_history`, `fees` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 5 endpoints as tools: `search_hotpads`, `get_hotpads_listing`, `get_hotpads_price_history`, `get_hotpads_fees` and `get_hotpads_suggestions`. HotPads is opt-in: add `hotpads` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.98.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,hotpads"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/hotpads-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=hotpads-api), [listing](https://scavio.dev/docs/hotpads-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=hotpads-api), [fees](https://scavio.dev/docs/hotpads-fees?utm_source=agent-skills&utm_medium=skill&utm_campaign=hotpads-api), [price history](https://scavio.dev/docs/hotpads-price-history?utm_source=agent-skills&utm_medium=skill&utm_campaign=hotpads-api), [suggestions](https://scavio.dev/docs/hotpads-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=hotpads-api). Overview: [HotPads API](https://scavio.dev/hotpads-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=hotpads-api).
