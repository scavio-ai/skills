# RentCafe API - Rental Listings, Floor Plan Units, Rent Trends

Read RentCafe (rentcafe.com, Yardi's US and Canada rental listing site): rental search in a city, ZIP, neighborhood or state, one listing in full with its floor plans, fees and amenities, every unit of a floor plan, resident reviews, location and property suggestions, and RentCafe's rent trends for a US city. Every answer is what RentCafe's public pages show a visitor without an account at the moment of the call, in USD (US) or CAD (Canada), in English or RentCafe's French. All 6 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages RentCafe shows to any visitor and returns them as JSON for analysis. It uses no RentCafe account, no resident or payment portal, no tour request, no contact form and no application.

**The job this skill is for: RentCafe's average rent per bed type for a city, next to the base rents the listings there ask.** `/rent-trends` returns RentCafe's city averages (`average_rent`, its YoY change and `by_bed_type` with the average size) with the date and source RentCafe states; `/search` with `beds` returns the listings with their base rent per bed type (`rent_by_bed`). Captured 2026-11-26 (1 credit per call):

| City and bed type | RentCafe average (`by_bed_type`, last updated October 30, 2026) | Listed base rents, same bed type (`/search`) |
|---|---|---|
| Chicago, IL, 1 bed | 2,464 for 708 sq ft (all rentals 2,531, +3.91% YoY) | Unfiltered, the 1 bd `rent_by_bed` rows: Shoreham And Tides 2,381+, North Harbor Tower 2,660+, The Montrose 2,402+ |
| Chicago, IL, 2 beds | 3,341 for 1,062 sq ft | not captured |
| Chicago, IL, studio | 1,798 for 466 sq ft | not captured |
| Austin, TX, 2 beds | not captured | `beds: 2`, `price_max: 2000`: 4,228 rentals; Sonterra Apartment Homes 1,404+, Ventana Oaks Apartments 1,345+ |

The averages are RentCafe's monthly figures for the city, attributed as RentCafe states them ("RentCafe Market Analysis, Yardi Matrix, U.S. Census Bureau"); the listing rents are base rents RentCafe shows ("+" means from). Put them side by side with the date, bed type and size, and leave any gap uninterpreted. For another site's view of the same city use `rent-com-api` (Rent.com's current averages per bed count and its listings), `zillow-property-data`, `redfin-property-data` or `realtor-com-property-data`, matched on city, bed count and date.

Nine limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged, and so is a search page past the last page (an empty page with a note); a refused input (`400`) and an upstream failure (`502`, `503`) are not. One exception: a rent-trends city for which RentCafe has no page at all is an uncharged `404`.
- **One path filter per search.** RentCafe takes one of `beds`, `rent_specials`, `short_term`, `furnished`, `utilities_included` or `amenity` per search; `price_min`, `price_max`, `pet_friendly` and `sort` combine with any of them. Two path filters are refused with a `400`.
- **RentCafe stops paging at about 15 to 20 pages of 25.** `total` is RentCafe's own count (Austin: 15,217 rentals, but `pages` 15); narrow with filters to reach more of them. A page past the last one comes back empty with a note, is charged, and took 76 seconds in the capture.
- **Base rents, in the market's currency.** Rents are the base rents RentCafe shows: USD in the US, CAD in Canada (read `currency`). A rent RentCafe does not state (call for price) is `null`, and `sort: "rent"` lists those first; in Toronto it opened on listings at 100 to 150 CAD, one of them named as a parking space. Read `rent_by_bed` and the floor plans before quoting a low `rent_min`.
- **Two markets, two languages.** `market` is `us` or `ca`, read from the location's state or province; `language: "fr"` returns RentCafe's French pages (fr-CA labels such as "2 Chambres", "Maintenant") over the same listings, prices unchanged.
- **Rent trends are US only, as RentCafe publishes them.** `/rent-trends` has `last_updated` (October 30, 2026 for Austin, Chicago and Houston) and `source`; RentCafe publishes no Canada rent trends pages, so a Canadian province is refused. There is no rent history per listing: store your own answers with `fetched_at`.
- **Floor plans show 2 units; one more call shows all.** A property's `floorplans[].units` holds the units RentCafe shows inline (up to 2); `/floorplan-units` lists every unit of one plan (Bridge At Indigo's Cobalt plan: 5).
- **Reviews as RentCafe shows them.** 10 a page in RentCafe's order (most recent first in every capture), no sort and no star filter, no reviewer name. `renters_summary` is RentCafe's own summary of its reviews, and `great_deal` is RentCafe's bare "Great deal" badge with no basis stated on the page.
- **Slow pages, and what is not there.** Search answered in 4 to 11 seconds in the captures (the probe saw up to 24), a property in 4 to 6, a rent-trends city RentCafe does not have in 71. Set a client timeout of at least 240 seconds and send one request at a time. No reviewer names, no rent history, no application, tour or contact flow, no Canada rent trends.

RentCafe links no public listing API or affiliate feed from rentcafe.com. This skill reads RentCafe's public pages with one Scavio key.

See also: `rent-com-api` (Rent.com and Apartment Guide rentals, floor plans and Rent.com's city averages), `zillow-property-data`, `redfin-property-data` and `realtor-com-property-data` (rentals next to homes for sale). Same city and bed type only, and name the site, currency and date with every number.

## When to trigger

Use this skill when the user asks to:
- Read RentCafe's average rent for a US city, by bed type with average size, its year-on-year change, rent by neighborhood and compared cities
- Search RentCafe rentals in a US or Canadian city, ZIP, neighborhood or state by property type, beds, rent specials, short-term, furnished, utilities included or an amenity, a rent range or pet-friendly, sorted by rent, rating or newest, in English or French
- Read one RentCafe listing in full: floor plans and units, deposit, application and pet fees, amenities, building details, category ratings, office hours
- List every unit of one floor plan with its rent and move-in date
- Read a listing's resident reviews, its rating and category ratings
- Turn a place or property name into the location or property id RentCafe uses

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=rentcafe-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=rentcafe-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, search answered in 4-11 seconds (the probe saw up to 24; a page past the last one 76), property 4-6, floor plan units 1-3, reviews 1-5, suggestions 1-3 and rent trends 4 (71 for a city RentCafe does not have). Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/rentcafe/search` | Rentals in a city, ZIP, neighborhood or state: rent range and rent per bed type, beds, baths, rating, review count, pets, rent specials, units available, tags, badges, management company; RentCafe's total, paging | 1 |
| `POST /api/v1/rentcafe/property` | One listing by link or slug: rent range, floor plans with up to 2 units each, fees and pet policies, amenities, services, building details, rating and category ratings, renters summary, reviews, office hours, leasing office phone, management company, description | 1 |
| `POST /api/v1/rentcafe/floorplan-units` | Every unit of one floor plan: unit, rent, move-in date, size, specials; the plan's amenities and photos | 1 |
| `POST /api/v1/rentcafe/reviews` | Resident reviews of one listing, 10 a page: rating, resident type, date, text (no names); on page 1 the overall rating, category ratings and renters summary | 1 |
| `POST /api/v1/rentcafe/suggestions` | Location and property suggestions for a city, neighborhood, ZIP or property name, with the `location` input for search and the property id | 1 |
| `POST /api/v1/rentcafe/rent-trends` | RentCafe's rent trends for a US city: average rent, previous year, YoY change, by bed type with average size, budget share, households, neighborhoods, compared cities, last updated date and source | 1 |

## Market

| `market` | Currency | Languages | Locations |
|---|---|---|---|
| `us` | USD | `en`, `fr` (RentCafe's French pages over US listings) | city + 2-letter state, 5-digit ZIP + state, neighborhood or state slug |
| `ca` | CAD | `en`, `fr` (fr-CA, e.g. Montreal) | city + 2-letter province, neighborhood or province slug (no ZIP) |

`market` is read from the location's state or province when left out; a mismatch is refused. Rent trends cover US cities only.

## Rents, fees and listings

| Field | Meaning |
|---|---|
| `rent_min`, `rent_max` | The listing's base rent range as RentCafe shows it, in `currency`; `null` when RentCafe states none |
| `rent_by_bed[]` (search) | {`beds` (RentCafe's label: "Studio", "2 bd", "2 chambre"), `rent`, `rent_text`} - "+" in `rent_text` means from |
| `floorplans[]` (property) | {`id`, `name`, `beds`, `baths`, `size`, `rent`, `rent_text`, `has_units`, `price_drop`, `units_shown`, `units[]` {`id`, `name`, `size`, `rent`, `rent_text`, `availability`}} |
| `units[]` (floor plan units) | {`id`, `name`, `availability` ("Now", "Dec 5"), `available_now`, `beds`, `baths`, `size`, `rent`, `rent_text`, `specials`} |
| `policies[]` | {`name`, `items[]` {`label`, `value`, `amount`}, `text`}: security deposit, application fees, one-time pet fees, monthly pet rent and pet policy text as RentCafe lists them |
| `rent_special`, `badges`, `great_deal`, `price_drop` | RentCafe's special text and badges as shown; `great_deal` has no basis stated |
| `rating`, `rating_label`, `category_ratings[]` | RentCafe's rating (e.g. 4, "Excellent") and per-category ratings (Parking, Amenities, Maintenance, Staff, Value, Location, Noise) |
| `by_bed_type[]` (rent trends) | {`type`, `average_rent`, `average_sqft`}: All Rentals, Studio, 1 Bed, 2 Beds, 3 Beds |
| `management_company`, `phone` | The management company's name and the leasing office's phone as the listing gives them |

- **Percent change:** `yoy_change_pct` is RentCafe's; any change you compute between answers is yours, so label it computed.
- **Ids:** `listings[].id` and `properties[].id` are the `property_id` of `/reviews` and `/floorplan-units`; `floorplans[].id` is the `floorplan_id`; `listings[].url` is the input of `/property`.

## Workflow

1. **Place.** `/suggestions` (`{"query": "Austin"}`, `market` `ca` for Canada) for `places[].location` (`austin-tx`, `downtown-toronto-toronto-on`) or a property's id.
2. **City averages (US).** `/rent-trends` with `city` and `state`. Note `average_rent`, `yoy_change_pct`, `by_bed_type`, `last_updated` and `source`.
3. **Listings.** `/search` with `location` (or `city` + `state`, or `zip` + `state`), one path filter such as `beds`, plus `price_max` or `pet_friendly`. Note `total`, `pages` and each listing's `rent_by_bed`.
4. **One listing.** `/property` with `listings[].url` for floor plans, fees, amenities and ratings; `/floorplan-units` with `property_id` and `floorplans[].id` for every unit of a plan.
5. **Residents.** `/reviews` with `property_id`, page by page.
6. **Report.** Each rent with the listing name, city, bed type, currency, RentCafe and the `fetched_at` date; RentCafe's averages with `last_updated` and `source`; no verdict.
7. **Rent series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | none | A RentCafe location as its links write it (`austin-tx`, `78704-tx`, `downtown-toronto-toronto-on`, a state such as `tx`) or a suggestions `places[].seo_url` (`us/tx/austin`). Send one of `location`, `city` or `zip` |
| `city` | string | none | Or a city name, with `state` (`Chicago`) |
| `zip` | string | none | Or a 5-digit US ZIP, with `state` (`78704`) |
| `state` | string | none | With `city` or `zip`: the 2-letter US state or Canadian province code (`TX`, `ON`, `QC`) |
| `market` | string | from the location | `us` or `ca`; a mismatch with the location is refused |
| `language` | string | `en` | `en` or `fr` (RentCafe's French pages, fr-CA labels over the same listings; prices stay in the market's currency) |
| `property_type` | string | `apartments` | `apartments`, `houses`, `condos` or `townhomes` |
| `beds` | string or integer | none | `studio`, 1, 2, 3 or 4 (0 is studio). A path filter |
| `rent_specials`, `short_term`, `furnished`, `utilities_included` | boolean | false | Only listings with a rent special, short-term leases, furnished, or utilities included. Each is a path filter |
| `amenity` | string | none | One of `washer-dryer`, `pool`, `garage`, `fitness-center`, `balcony`, `air-conditioning`, `dishwasher`, `fireplace`, `hardwood-floors`, `walk-in-closets`, `wheelchair-accessible`, `controlled-access`, `playground`, `public-transportation`, `recent-build`, `tennis-court`, `yard`, `cheap`, `luxury`. A path filter |
| `pet_friendly` | boolean | false | Only pet-friendly listings (combines with any filter) |
| `price_min`, `price_max` | integer | none | Monthly rent range in the market's currency (0-100,000) |
| `sort` | string | `default` | `default` (RentCafe's own order), `rent` (low to high; listings without a stated rent first), `rent_desc`, `rating_desc` or `newest` (listings with new units at the top) |
| `page` | integer | 1 | Page of 25, 1-50; RentCafe pages through about 15-20 pages at most (`pages` says how many) |

### Property, floor plan units, reviews, suggestions, rent trends

| Endpoint | Parameters |
|---|---|
| `/property` | one of `url` (a listing link as `listings[].url` gives it; a `/fr/` link reads French) or `slug` (`tx/austin/bridge-at-indigo`, as in the link; `housing/...` or `single-family/...` for those links); `language` (`en` or `fr`) |
| `/floorplan-units` | `property_id` (`1651075`) and `floorplan_id` (`4746456`, from `floorplans[].id`), both required; `unit_id` (from `floorplans[].units[].id`: `selected_unit` gives its base rent and availability); `url` (the listing link) or `market` (`us` default or `ca`, the currency of the rents) |
| `/reviews` | `property_id` (required); `page` (1-200, 10 reviews a page); `url` (the listing link). No sort or star filter exists |
| `/suggestions` | `query` (2-80 characters: a city, neighborhood, ZIP or property name); `market` (`us` default or `ca`) |
| `/rent-trends` | `city` (a US city) and `state` (its 2-letter code), both required |

## Examples

### RentCafe's rent trends for a city

```bash
curl -X POST https://api.scavio.dev/api/v1/rentcafe/rent-trends \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"city": "Chicago", "state": "IL"}'
```

Captured `data` (Chicago, IL, 2026-11-26; `highlights` cut to 1 of 5, the neighborhood lists to 2 of 3, `rent_by_neighborhood` to 2 of 60, `compared_cities` to 3 of 16, `notes` dropped):

```json
{
  "city": "Chicago",
  "state": "IL",
  "currency": "USD",
  "url": "https://www.rentcafe.com/average-rent-market-trends/us/il/chicago/",
  "title": "Chicago, IL Rental Market Trends",
  "last_updated": "October 30, 2026",
  "source": "RentCafe Market Analysis, Yardi Matrix, U.S. Census Bureau",
  "average_rent": 2531,
  "average_rent_previous_year": 2436,
  "yoy_change_pct": 3.91,
  "highlights": ["The average rent for an apartment in Chicago is $2,531, a 3.91% increase compared to the previous year, when the average rent was $2,436."],
  "by_bed_type": [
    {"type": "All Rentals", "average_rent": 2531, "average_sqft": 745},
    {"type": "Studio", "average_rent": 1798, "average_sqft": 466},
    {"type": "1 Bed", "average_rent": 2464, "average_sqft": 708},
    {"type": "2 Beds", "average_rent": 3341, "average_sqft": 1062},
    {"type": "3 Beds", "average_rent": 3726, "average_sqft": 1355}
  ],
  "budget_share": [{"range": "≤ $1000", "share_pct": 2}, {"range": "$1,001-$1,500", "share_pct": 14}, {"range": "$1,501-$2,000", "share_pct": 18}, {"range": "$2,001-$2,500", "share_pct": 21}, {"range": "$2,501-$3,000", "share_pct": 19}, {"range": "> $3,000", "share_pct": 26}],
  "households": {"renter_occupied": 626193, "renter_pct": 54, "owner_occupied": 534012, "owner_pct": 46},
  "most_affordable_neighborhoods": [{"name": "Austin", "average_rent": 1180, "location": "austin-chicago-il"}, {"name": "Washington Park", "average_rent": 1253, "location": "washington-park-chicago-il"}],
  "most_expensive_neighborhoods": [{"name": "River North", "average_rent": 3419, "location": "river-north-chicago-il"}, {"name": "Wrightwood", "average_rent": 3783, "location": "wrightwood-chicago-cook-county-il"}],
  "rent_by_neighborhood": [{"name": "Sheffield", "average_rent": 4051}, {"name": "Wrightwood", "average_rent": 3783}],
  "compared_cities": [{"name": "Chicago", "average_rent": 2531}, {"name": "Oak Park", "average_rent": 2318}, {"name": "Evanston", "average_rent": 2593}]
}
```

Houston read 1,343 (-1.26%) with one-bedroom 1,192. (Chicago's "Austin" is its West Side neighborhood, `austin-chicago-il`, not Austin, TX.) A neighborhood's `location` is the `location` input of `/search`. `{"city": "Toronto", "state": "ON"}` is refused: "rent-trends covers US cities only: RentCafe publishes no Canada rent trends pages."

### Search a city by bed count and rent cap

```bash
curl -X POST https://api.scavio.dev/api/v1/rentcafe/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": "austin-tx", "beds": 2, "price_max": 2000}'
```

Captured `data` (2026-11-26; `listings` cut to 2 of 25 without `latitude`, `longitude`, `url` and `image`; `notes` dropped):

```json
{
  "market": "us",
  "language": "en",
  "currency": "USD",
  "property_type": "apartments",
  "location": "austin-tx",
  "filters": {"beds": "2", "rent_specials": false, "short_term": false, "furnished": false, "utilities_included": false, "amenity": null, "pet_friendly": false, "price_min": null, "price_max": 2000},
  "sort": "default",
  "title": "2 Bedroom Apartments for Rent in Austin, TX",
  "total": 4228,
  "page": 1,
  "page_size": 25,
  "pages": 9,
  "has_more": true,
  "count": 25,
  "listings": [
    {"id": "137127", "name": "Sonterra Apartment Homes", "address": "8801 FM 620 North", "city": "Austin", "state": "TX", "zip": "78726", "beds": "2 Beds", "baths": "1-2 Baths", "rent_min": 1404, "rent_max": 1831, "currency": "USD", "rent_by_bed": [{"beds": "2 bd", "rent": 1404, "rent_text": "$1,404+"}], "rating": 4.5, "review_count": 28, "pets_allowed": true, "rent_specials": true, "units_available": 9, "tags": ["Apply online", "Pet friendly", "Parking"], "badges": ["Rent specials", "Rewards"], "featured_type": "premier_plus", "management_company": "Bassham Properties", "image_count": 84},
    {"id": "137129", "name": "Ventana Oaks Apartments", "address": "9301 Spectrum Drive", "city": "Austin", "state": "TX", "zip": "78717", "beds": "2 Beds", "baths": "2 Baths", "rent_min": 1345, "rent_max": 2227, "currency": "USD", "rent_by_bed": [{"beds": "2 bd", "rent": 1345, "rent_text": "$1,345+"}], "rating": 4.5, "review_count": 25, "pets_allowed": true, "rent_specials": true, "units_available": 10, "tags": ["Apply online", "Pet friendly", "Parking"], "badges": ["Rent specials", "Rewards"], "featured_type": "premier_plus", "management_company": "Bassham Properties", "image_count": 53}
  ]
}
```

Other captures: Austin with no filter counted 15,217 rentals over 15 pages, and `page` 16 came back empty with "RentCafe has 15 page(s) for this search; page 16 is past the last one. Narrow with filters to see other listings." Chicago with `amenity: "pool"` and `sort: "rating_desc"` counted 1,468. Toronto (`toronto-on`, CAD) counted 8,559; `downtown-toronto-toronto-on` with `furnished: true` 30. Montreal in French (`{"location": "montreal-qc", "language": "fr"}`) counted 1,160 with RentCafe's French labels ("Studio-3 Chambres", "Offres spéciales de location") and rents in CAD. Austin houses (`property_type: "houses"`) counted 83.

### One listing in full

```bash
curl -X POST https://api.scavio.dev/api/v1/rentcafe/property \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.rentcafe.com/apartments/tx/austin/bridge-at-indigo/default.aspx"}'
```

Captured `data` (2026-11-26; `floorplans` cut to 1 of 9, `policies` to 2 of 4, `office_hours` to 2 of 7, `renters_summary` text shortened; `latitude`, `longitude`, `units_available` (null), `images` (41), `amenities`, `services`, `reviews` (39), `phone`, `office_hours_note`, `description` and `notes` dropped):

```json
{
  "id": "1651075",
  "name": "Bridge At Indigo",
  "url": "https://www.rentcafe.com/apartments/tx/austin/bridge-at-indigo/default.aspx",
  "market": "us",
  "language": "en",
  "currency": "USD",
  "address": {"street": "10800 Lakeline Blvd", "city": "Austin", "state": "TX", "zip": "78717", "country": "US"},
  "rent_min": 1130,
  "rent_max": 2880,
  "rent_text": "$1,130+",
  "beds": "1-3 Beds",
  "baths": "1-2",
  "rating": 4,
  "rating_label": "Excellent",
  "review_count": 39,
  "badges": ["Rent specials", "Great deal"],
  "great_deal": true,
  "price_drop": false,
  "rent_special": "Lease today for up to 10 weeks free! Call for details. Offers vary by floor plan.",
  "floorplans": [
    {"id": "4746456", "name": "Cobalt", "beds": "1 Bed", "baths": "1 Bath", "size": "657 Sqft", "rent": 1130, "rent_text": "$1,130+", "has_units": true, "price_drop": false, "units_shown": 2,
     "units": [{"id": "34997017", "name": "12204", "size": "657 Sqft", "rent": 1130, "rent_text": "$1,130+", "availability": "Now"}, {"id": "34996946", "name": "9106", "size": "657 Sqft", "rent": 1305, "rent_text": "$1,305+", "availability": "Now"}]}
  ],
  "policies": [
    {"name": "General", "items": [{"label": "Security deposit", "value": "$500", "amount": 500}, {"label": "Application fees", "value": "$25 - $200", "amount": null}], "text": ["There may be additional unit-specific fees. Please select a unit and move-in date here."]},
    {"name": "Cats", "items": [{"label": "One-time pet fees", "value": "$400", "amount": 400}, {"label": "Monthly pet rent", "value": "$20", "amount": 20}], "text": ["max 2 pets per unit."]}
  ],
  "building_details": ["14 buildings in the community", "325 apartments in the community", "3 stories per building", "Building constructed in 2013"],
  "category_ratings": [{"category": "Parking", "rating": 4.5}, {"category": "Amenities", "rating": 4}, {"category": "Maintenance", "rating": 4}, {"category": "Staff", "rating": 4}, {"category": "Value", "rating": 4}, {"category": "Location", "rating": 4.5}, {"category": "Noise", "rating": 4}],
  "renters_summary": {"text": "Renters at Bridge at Indigo appreciate the property’s prime location, which is conveniently close to shops, schools, and public transport ...", "source": "RentCafe's own summary of resident reviews (What renters are saying)"},
  "office_hours": [{"day": "Monday", "hours": "8:30AM-5:30PM"}, {"day": "Saturday", "hours": "10:00AM-5:00PM"}],
  "management_company": "Apartment Management Professionals"
}
```

In Toronto, 390 Queens Quay West (`636318`) read CAD 2,327 to 3,614, rating 3.5 "Very good", `rent_special` "Receive 1 MONTH RENT-FREE + $500 MOVE-IN BONUS! ...", `management_company` "Briarlane Rental Property Management Inc.". In French, Maddox Dorchester in Montreal (`1715285`, `{"url": ".../fr/apartments/qc/montr%C3%A9al/maddox-dorchester/default.aspx"}`) read CAD 1,390 to 2,400, "Studio-2 Chambres", 16 units available, with floor plan units available "Maintenant".

### Every unit of one floor plan

```bash
curl -X POST https://api.scavio.dev/api/v1/rentcafe/floorplan-units \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"property_id": "1651075", "floorplan_id": "4746456"}'
```

Captured `data` (2026-11-26; `units` cut to 3 of 5, `selected_unit`, `amenities` (18), `photos` and `notes` dropped):

```json
{
  "property_id": "1651075",
  "floorplan_id": "4746456",
  "name": "Cobalt",
  "beds": "1 Bed",
  "baths": "1 Bath",
  "size": "657 Sqft",
  "rent": 1130,
  "rent_text": "$1,130+",
  "currency": "USD",
  "price_drop": false,
  "count": 5,
  "units": [
    {"id": "34996947", "name": "9107", "availability": "Dec 5", "available_now": false, "beds": "1 Bed", "baths": "1 Bath", "size": "657 Sqft", "rent": 1305, "rent_text": "$1,305+", "specials": null},
    {"id": "34996851", "name": "4305", "availability": "Dec 31", "available_now": false, "beds": "1 Bed", "baths": "1 Bath", "size": "657 Sqft", "rent": 1130, "rent_text": "$1,130+", "specials": null},
    {"id": "34996881", "name": "5307", "availability": "Jan 10, 2027", "available_now": false, "beds": "1 Bed", "baths": "1 Bath", "size": "657 Sqft", "rent": 1130, "rent_text": "$1,130+", "specials": null}
  ],
  "specials": null
}
```

The property page showed 2 of these 5 units. Toronto's 390 Queens Quay West plan `2344662` (send `"market": "ca"` or the listing `url` for CAD) listed 6 units from CAD 2,937 to 3,614, two available Dec 1. Without `market` or `url`, the note says "currency assumes a US listing: send market ca (or the listing url) for a Canadian one."

### Reviews and suggestions

- `/reviews` `{"property_id": "1651075"}`: `total` 39, `pages` 4, `rating` 4 "Excellent", the 7 category ratings and the renters summary; first review `rating` 4.2, `resident_type` "Verified Resident", `date` "May 22, 2026", `text` "Ive had a good time living here and the location is great." Page 6 came back empty with "Page 6 is past the last page of reviews (4)." 390 Queens Quay West had 16 reviews over 2 pages; Maddox Dorchester 21, one of the first 10 in French.
- `/suggestions` `{"query": "Austin"}`: places Austin TX (`austin-tx`, `us/tx/austin`), Austin IN, Austin MN, Austin NV, Austintown OH; properties such as Austin Commons in Hayward, CA (`1495152`). `{"query": "Toronto", "market": "ca"}`: Toronto ON, Downtown Toronto (`downtown-toronto-toronto-on`), East End Toronto, Greater Toronto and 3 properties. A property name (`{"query": "Chelsea 29"}`) returned only that property (`582406`, New York).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def rentcafe(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/rentcafe/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# RentCafe's averages for a US city (1 credit)
t = rentcafe("rent-trends", {"city": "Austin", "state": "TX"})["data"]
print(t["average_rent"], t["yoy_change_pct"], t["last_updated"], t["source"])
for b in t["by_bed_type"]:
    print(b["type"], b["average_rent"], b["average_sqft"])

# Two-bedroom listings in the same city under a rent cap (1 credit)
s = rentcafe("search", {"location": "austin-tx", "beds": 2, "price_max": 2000})["data"]
print(s["total"], "rentals,", s["pages"], "pages")
for l in s["listings"]:
    print(l["id"], l["name"], l["currency"], l["rent_by_bed"], l["management_company"])

# Store each answer with fetched_at: that stored set is your rent record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Most answers carry `notes`.

- **search** - `market`, `language`, `currency`, `property_type`, `location`, `filters` {`beds`, `rent_specials`, `short_term`, `furnished`, `utilities_included`, `amenity`, `pet_friendly`, `price_min`, `price_max`}, `sort`, `title`, `total`, `page`, `page_size`, `pages`, `has_more`, `count`, `listings[]` {`id`, `name`, `url`, `address`, `city`, `state`, `zip`, `latitude`, `longitude`, `beds`, `baths`, `rent_min`, `rent_max`, `currency`, `rent_by_bed[]` {`beds`, `rent`, `rent_text`}, `rating`, `review_count`, `pets_allowed`, `rent_specials`, `units_available`, `tags`, `badges`, `featured_type`, `management_company`, `image`, `image_count`}, `notes`.
- **property** - `id`, `name`, `url`, `market`, `language`, `currency`, `address` {`street`, `city`, `state`, `zip`, `country`}, `latitude`, `longitude`, `rent_min`, `rent_max`, `rent_text`, `beds`, `baths`, `rating`, `rating_label`, `review_count`, `badges`, `great_deal`, `price_drop`, `rent_special`, `units_available`, `images`, `floorplans[]` {`id`, `name`, `beds`, `baths`, `size`, `rent`, `rent_text`, `has_units`, `price_drop`, `units_shown`, `units[]` {`id`, `name`, `size`, `rent`, `rent_text`, `availability`}}, `policies[]` {`name`, `items[]` {`label`, `value`, `amount`}, `text`}, `amenities` {`apartment`, `community`}, `services`, `building_details`, `category_ratings[]` {`category`, `rating`}, `renters_summary` {`text`, `source`}, `reviews[]` {`rating`, `date`, `text`}, `office_hours[]` {`day`, `hours`}, `office_hours_note`, `phone`, `management_company`, `description`, `notes`.
- **floor plan units** - `property_id`, `floorplan_id`, `name`, `beds`, `baths`, `size`, `rent`, `rent_text`, `currency`, `price_drop`, `selected_unit` {`id`, `base_rent`, `base_rent_text`, `availability`}, `count`, `units[]` {`id`, `name`, `availability`, `available_now`, `beds`, `baths`, `size`, `rent`, `rent_text`, `specials`}, `amenities`, `photos[]` {`url`, `alt`}, `specials`, `notes`.
- **reviews** - `property_id`, `page`, `page_size`, `total`, `pages`, `has_more`, page 1 also `rating`, `rating_label`, `category_ratings`, `renters_summary`; `count`, `reviews[]` {`rating`, `resident_type`, `date`, `text`}, `notes`.
- **suggestions** - `query`, `market`, `places[]` {`name`, `label`, `seo_url`, `location`}, `properties[]` {`id`, `name`, `address`, `city`, `state`, `zip`, `seo_url`, `location`}, `notes`.
- **rent trends** - `city`, `state`, `currency`, `url`, `title`, `last_updated`, `source`, `average_rent`, `average_rent_previous_year`, `yoy_change_pct`, `highlights`, `by_bed_type[]` {`type`, `average_rent`, `average_sqft`}, `budget_share[]` {`range`, `share_pct`}, `households` {`renter_occupied`, `renter_pct`, `owner_occupied`, `owner_pct`}, `most_affordable_neighborhoods[]` and `most_expensive_neighborhoods[]` {`name`, `average_rent`, `location`}, `rent_by_neighborhood[]` {`name`, `average_rent`}, `compared_cities[]` {`name`, `average_rent`}, `notes`.

## Guardrails

- Name it "RentCafe (rentcafe.com, Yardi's US and Canada rental listing site)" on first mention, "RentCafe" after that.
- Rents: quote each with its currency (USD or CAD), the listing name, city, bed type (and floor plan or unit where given), RentCafe and the `fetched_at` date ("RentCafe listed Cobalt at Bridge At Indigo, Austin, from 1,130 USD a month on Nov 26, 2026"). A "+" rent is a starting rent, not every unit's rent.
- Averages: quote `average_rent` and `by_bed_type` as RentCafe's, with `last_updated` and `source` as RentCafe states them. Never present them as this month's rent for a specific listing.
- Badges: `great_deal` is RentCafe's badge with no basis stated; never explain or rank by it. `renters_summary` is RentCafe's own summary; attribute it that way.
- Reviews: no reviewer is named or identified. Review text can mention staff by first name; do not repeat any personal name that appears in a review. Quote review text as RentCafe shows it, with its rating and date.
- Comparisons: same city, bed type, currency and date; name each site. No verdict on whether a listing is a good deal, no commentary on the rental market beyond the numbers shown.
- Contacts: `phone` is the leasing office's number as the listing shows it and `management_company` a business name; there are no personal contacts.
- Descriptive only: no commentary on RentCafe's or Yardi's business, pricing or practices.
- Do not republish listing photos or descriptions. Write rentcafe.com as plain text and cite property ids, floor plan ids and capture dates rather than linking RentCafe pages.
- Terms: Scavio does not collect or store RentCafe data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account, no portal and no contact, tour or application flow. RentCafe's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate rents, averages, units, move-in dates, fees, ratings or review text. Only return what the API returned, with the `fetched_at` time.
- Not available: reviewer names, rent history, applications, tours, contact forms, Canada rent trends.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without exactly one location ("send one of location, city (with state) or zip (with state)."); `state` with `location` ("state goes with city or zip, not with location."); a ZIP for Canada ("zip is for US searches; for Canada use city with a province (e.g. Toronto, ON)."); a location that does not end in a state or province code; two path filters ("RentCafe filters one of beds, rent_specials, short_term, furnished, utilities_included or amenity at a time (price_min, price_max, pet_friendly and sort combine with any of them)."); a `market` that does not match the location; `price_min` above `price_max`; an amenity outside the list; `page` above 50; `/property` without exactly one of `url` or `slug` ("send one of url or slug."), or a link that is not a RentCafe listing link; a `property_id` or `floorplan_id` that is not digits; rent trends for a Canadian province ("rent-trends covers US cities only: RentCafe publishes no Canada rent trends pages."); suggestions under 2 characters. A body that fails the schema answers "Invalid request: ..." with `details`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "RentCafe has no listings page for this location (it sent the search to a state page). Use suggestions to find the location RentCafe uses (places[].location or places[].seo_url).", "RentCafe has no listing at this link (it sent it to a search page). Use the url from search listings[].url.", "RentCafe has no floor plan with this id for this property (property floorplans[].id).", "RentCafe has no property with this id (listings[].id).". A rent-trends city RentCafe has no page for answers "RentCafe has no rent trends page for this city (city and state as RentCafe names them, e.g. Austin, TX)." and is not charged when RentCafe has no page at that address. Take locations, links and ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=rentcafe-api).
- `502` means RentCafe data was temporarily unavailable ("RentCafe is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("RentCafe is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.97.0
npm install scavio@0.98.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: trends } = await scavio.rentcafe.rentTrends({ city: "Austin", state: "TX" });
const { data: rentals } = await scavio.rentcafe.search({ location: "austin-tx", beds: 2, price_max: 2000 });
const { data: listing } = await scavio.rentcafe.property({ url: "https://www.rentcafe.com/apartments/tx/austin/bridge-at-indigo/default.aspx" });
const { data: units } = await scavio.rentcafe.floorplanUnits({ property_id: "1651075", floorplan_id: "4746456" });
const { data: reviews } = await scavio.rentcafe.reviews({ property_id: "1651075", page: 1 });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.rentcafe.search(...)`, `property`, `floorplan_units`, `reviews`, `suggestions` and `rent_trends`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 6 endpoints as tools: `search_rentcafe`, `get_rentcafe_property`, `get_rentcafe_floorplan_units`, `get_rentcafe_reviews`, `get_rentcafe_suggestions` and `get_rentcafe_rent_trends`. RentCafe is opt-in: add `rentcafe` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.97.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,rentcafe"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/rentcafe-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=rentcafe-api), [property](https://scavio.dev/docs/rentcafe-property?utm_source=agent-skills&utm_medium=skill&utm_campaign=rentcafe-api), [floor plan units](https://scavio.dev/docs/rentcafe-floorplan-units?utm_source=agent-skills&utm_medium=skill&utm_campaign=rentcafe-api), [reviews](https://scavio.dev/docs/rentcafe-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=rentcafe-api), [suggestions](https://scavio.dev/docs/rentcafe-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=rentcafe-api), [rent trends](https://scavio.dev/docs/rentcafe-rent-trends?utm_source=agent-skills&utm_medium=skill&utm_campaign=rentcafe-api). Overview: [RentCafe API](https://scavio.dev/rentcafe-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rentcafe-api).
