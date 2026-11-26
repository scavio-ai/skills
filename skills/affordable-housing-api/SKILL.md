---
name: affordable-housing-api
description: AffordableHousing.com API for AffordableHousing.com (affordablehousing.com, the US affordable and Section 8 rental site run by Affordable Housing Network, formerly GoSection8) - which Section 8 and public housing waiting lists are open now, and which housing authority runs each one (the national page listed 753 open waiting lists, 625 of them Section 8 Housing Choice Voucher lists and 88 Project-Based Voucher lists, 137 taking online applications) with the program, the opened-on date and the agency; one housing authority with its public office address, phone, fax and website, waitlist status, voucher count, programs, the counties it serves and its waiting lists with how applicants are selected (Somerville Housing Authority, MA, open, 1,193 vouchers, 12 waiting lists); a state's housing authorities; affordable and Section 8 rental search by state, city, county or ZIP code with beds, baths, property type, rent range, pet friendly, Section 8, utilities included, senior (age restricted) and accessibility filters, 9 sorts, 42 a page, each listing with rent range, beds, baths, size, year built, the Section 8 badge, income-restricted, trusted-owner and tier flags; one listing in full with floor plans and their rents, units, move-in and monthly fees, the tenant and owner utilities split, amenities, accessibility features, pet policy and age restriction; place suggestions. 6 endpoints, search and suggestions 2 credits per call, listing, waiting lists and housing authority pages 1 credit. US only, USD. Private landlords are never named; no payment standard or fair market rent numbers, no applications.
version: 1.0.0
tags: affordablehousing, affordablehousing-com, affordable-housing, affordable-housing-api, affordable-housing-search, affordable-housing-listings, section-8, section-8-housing, section-8-rentals, section-8-waiting-list, section-8-waiting-lists, housing-choice-voucher, hcv, project-based-voucher, public-housing, public-housing-waiting-list, housing-authority, housing-authorities, public-housing-agency, pha, low-income-housing, income-restricted-housing, senior-housing, accessible-housing, gosection8, rental-listings, rent-prices, floor-plans, rental-fees, utilities, real-estate, real-estate-data, us-real-estate, usd, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/affordablehousing-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=affordable-housing-api
---

# AffordableHousing.com API - Section 8 Rentals, Waiting Lists, Housing Authorities

Read AffordableHousing.com (affordablehousing.com, the US affordable and Section 8 rental site run by Affordable Housing Network, founded in 2003 as GoSection8): the Section 8 and public housing waiting lists that are open now, nationwide or for one state; one housing authority (public housing agency) with its public office contact, programs, the counties it serves and its waiting lists; a state's housing authorities; affordable and Section 8 rental search; one listing in full; and place suggestions. Every answer is what AffordableHousing.com's public pages show a visitor without an account at the moment of the call, in USD. All 6 endpoints return structured JSON: search and suggestions at 2 credits per call, the other 4 at 1.

**Read-only data.** This skill reads the public pages AffordableHousing.com shows to any visitor and returns them as JSON for analysis. It uses no AffordableHousing.com account, no tenant or landlord login, no application, no contact form and no voucher calculator.

**The job this skill is for: which waiting lists are open, who runs them, and what affordable rentals are listed in a place.** `/waiting-lists` returns every open Section 8 and public housing waiting list AffordableHousing.com lists, with its program, opened-on date and agency; `/housing-authority` returns one agency's public office contact, voucher count, programs, jurisdiction and lists; `/search` returns listings with the Section 8 badge and rent. Captured 2026-11-26:

| Request | What AffordableHousing.com showed | Credits |
|---|---|---|
| `/waiting-lists` (nationwide) | 753 open waiting lists; by program 625 Section 8 (HCV), 88 Project-Based Voucher, 11 Project Based Section 8 Housing, 5 Public Housing; 137 with an online application; most in VT (96), NY (56) and TX (50); 0 opening soon | 1 |
| `/waiting-lists` `{"state": "TX"}` | 50 open lists, e.g. the Abilene Housing Authority Section 8 Waiting List, open since 10/31/2022 | 1 |
| `/housing-authority` Somerville Housing Authority, MA (id 674) | waitlist Open, 1,193 vouchers, programs Section 8 (HCV) and Other, 12 waiting lists (Somerville Primary: Section 8 (HCV), First in, First out, centralized), public office 30 Memorial Road, phone 617-625-1152 | 1 |
| `/housing-authorities` `{"state": "CA"}` | total 103 housing authorities in California, first 14 listed (TX 346, NY 164) | 1 |
| `/search` Los Angeles, CA, 1 or 2 beds, `section8: true` | total 3,279 (79 pages of 42); page 1 rents $990 to $3,190 a month; 3 spotlight listings first, then 39 premium | 2 |
| `/search` Houston, TX, `sort: "price_asc"` | total 1,553 (37 pages); page 1 rents $450 to $824 a month, all 42 premium tier, 36 with the Section 8 badge | 2 |
| `/listing` The Reserve At Westwood, Houston (766073) | $810 to $1,480 a month over 7 floor plans, Section 8 badge, application fee $50, pet rent $30, one-time pet fee $400, tenant pays 9 utilities, owner pays lawn care | 1 |

Quote each figure with AffordableHousing.com, the place, the program and the `fetched_at` date. A waiting list's `status` and `opened_on` are as the site gives them; check with the housing authority before acting on one. For other rentals in the same area use `rent-com-api`, `rentcafe-api` or `zillow-property-data`, matched on city and beds.

Ten limits shape every answer, so say them plainly:
- **2 credits for search and suggestions, 1 for the rest.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **42 listings a page, tiers first.** Search returns 42 a page to page 500; `pages` says how many exist. Premium and spotlight listings are placed first by AffordableHousing.com and the sort applies within each tier, so a `price_asc` page is sorted inside its tier, not across the whole result.
- **The Section 8 badge is the owner's.** `section8_accepted` (and the `section8` filter) is the listing's badge for an owner with experience with the Section 8 / Housing Choice Voucher program; it is not a promise that a voucher will be accepted for a given unit.
- **A ZIP code is searched within its city.** Send `zip` with its `city` and `state`; a ZIP alone is refused. Send `city` or `county`, not both; leave both out to search the whole state.
- **Rents as the site shows them.** USD per month; `rent_min` and `rent_max` are `null` where a listing states no rent. Income-based rents show as the listing states them ("Income Based Rent" in a title).
- **Housing authorities: public office contact only.** `phone`, `fax`, `website` and the address are the agency's public office details. No staff names or staff email addresses are returned. `housing-authorities` lists the first 14 agencies of a state's page; `total` is the site's count for the state.
- **Waiting list dates.** `opened_on` is MM/DD/YYYY as the site gives it; a housing authority's own `waiting_lists` carry no open or close dates (its `waitlist_status`, `waitlist_open_date` and `waitlist_close_date` are the agency's).
- **No landlord personal data.** `listed_by` is given only when AffordableHousing.com marks the owner as a business (a property manager); private landlords' names and contact details are never returned, and phone numbers and email addresses are cut out of titles and descriptions.
- **No payment standards.** AffordableHousing.com explains payment standards and utility allowances in text only; no payment standard or fair market rent numbers are returned.
- **What is not there.** No applications or eligibility checks, no voucher calculator, no landlord contact, no listings past page 500, no history of when a list opened or closed beyond what the page states. In the captures search answered in 1.2 to 5.7 seconds (19.6 under parallel load), suggestions in 1.1 to 2.8, a listing in 2.1 to 4.0, waiting lists in 2.0 to 4.0 and a housing authority in 2.1 to 10.3; set a client timeout of at least 240 seconds and send one request at a time.

AffordableHousing.com publishes no public developer API. This skill reads AffordableHousing.com's public pages with one Scavio key.

See also: `rent-com-api` and `rentcafe-api` (US rental listings and floor plans), `zillow-property-data`, `trulia-api` (neighborhood survey and market snapshot). Same place only: match on city and beds, name the site and date with every number.

## When to trigger

Use this skill when the user asks to:
- Find which Section 8, Housing Choice Voucher, Project-Based Voucher or public housing waiting lists are open now, nationwide or in one US state
- Read one housing authority (public housing agency) on AffordableHousing.com: its public office address, phone and website, waitlist status, voucher count, programs, the counties it serves and its waiting lists
- List a state's housing authorities with their waitlist status and programs
- Search affordable and Section 8 rentals by state, city, county or ZIP code with beds, baths, property type, rent range, pet friendly, Section 8, utilities included, senior or accessibility filters
- Read one AffordableHousing.com listing in full: floor plans and their rents, units, fees, the utilities split, amenities, accessibility features, pets and age restriction
- Look up the place names AffordableHousing.com searches (cities, counties, ZIP codes)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=affordable-housing-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=affordable-housing-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Search and suggestions cost 2 credits, the other endpoints 1, so 50 credits cover for example 10 cities (one search and one listing each, 30 credits) plus 20 waiting list or housing authority reads.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures every endpoint answered in 1.1 to 10.3 seconds (search up to 19.6 under parallel load). Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/affordablehousing/search` | Affordable and Section 8 rentals in a state, city, county or ZIP code: 42 a page, 9 sorts, filters; each listing with rent range, beds, baths, size, year built, unit count, Section 8 badge, trusted-owner, income-restricted and government flags, tier, availability and photo | 2 |
| `POST /api/v1/affordablehousing/suggestions` | Place suggestions (cities, counties, ZIP codes) with population and the `search` input of search | 2 |
| `POST /api/v1/affordablehousing/listing` | One listing by link or id: address, rent range, beds, baths, size, Section 8 badge, pets, age restriction, description, floor plans with units and rents, fees, utilities split, amenities, accessibility, photos and the business owner name where the site marks one | 1 |
| `POST /api/v1/affordablehousing/waiting-lists` | Open Section 8 and public housing waiting lists, nationwide or for one state: name, program, agency, online application, status, opened-on date; and the lists opening soon | 1 |
| `POST /api/v1/affordablehousing/housing-authority` | One housing authority by link or id and state: public office address, phone, fax, website, HCV page, participant code, waitlist status and dates, voucher count, programs, jurisdiction, waiting lists | 1 |
| `POST /api/v1/affordablehousing/housing-authorities` | A state's housing authorities as its page lists them (first 14): name, address, waitlist status, programs, jurisdiction, link; and the state's total | 1 |

## Market

US only, English, USD. There is no `country`, `language` or `currency` input. `state` takes a 2-letter code (TX, CA, DC) or the state's name.

## Listing and agency fields

| Field | Meaning |
|---|---|
| `section8_accepted` | The listing's badge for an owner with experience with the Section 8 / Housing Choice Voucher program |
| `income_restricted`, `government_listing`, `trusted_owner`, `special_offer`, `room_for_rent` | The listing's flags as the site sets them |
| `tier` | `premium`, `spotlight` or `standard`: premium and spotlight listings are placed first in every sort |
| `models[]` | Each floor plan: {`id`, `name`, `beds`, `full_baths`, `half_baths`, `sqft`, `rent`, `rent_text`, `deposit`, `deposit_negotiable`, `year_built`, `property_type`, `available_date`, `accepting_applications`, `subsidized_units`, `description`, `units[]` {`unit`, `rent`, `available_date`, `accepting_applications`}} |
| `fees` | {`move_in_total`, `move_out_total`, `estimated_monthly_total`, `estimated_one_time_total` (each {`min`, `max`, `text`}), `application_fee`, `pet_rent`, `pet_deposit`, `pet_fee_one_time`} |
| `utilities` | {`tenant_pays`, `owner_pays`}: the listing's split of who pays which utility |
| `listed_by` | The owner's name where the site marks the owner as a business; `null` otherwise |
| `waitlist_status`, `voucher_count`, `section8_inventory` | A housing authority's waitlist status and voucher figures as the site gives them |
| `waiting_lists[]` (housing authority) | {`id`, `name`, `program`, `selected_by` ("First in, First out" ...), `centralized`} |
| `open[]` (waiting lists) | {`waitlist_id`, `name`, `program`, `agency_id`, `agency_name`, `agency_url`, `state`, `online_application`, `status`, `opened_on`} |

- **Use the utilities split, not a utilities badge.** `utilities.tenant_pays` and `owner_pays` are what the listing states; the `utilities_included` search filter is the site's own filter.

## Workflow

1. **Open lists.** `/waiting-lists` (nationwide, or `{"state": "TX"}`): note `program`, `status`, `opened_on` and `online_application`.
2. **The agency.** `/housing-authority` with `url` = `agency_url` (or `id` = `agency_id` with `state`): public office contact, programs, jurisdiction, its waiting lists. `/housing-authorities` lists a state's agencies.
3. **Place names.** `/suggestions` (`{"text": "Houston"}`): `places[].search` is the location input of search (state with city or county).
4. **Rentals.** `/search` with `state` and `city` or `county` (or `zip` with its city), plus filters. Check `total`, `pages`, `tier` and the notes.
5. **One listing.** `/listing` with `id` or `url` from `listings[]`: floor plans, fees, utilities split.
6. **Report.** Each list with its program, agency, status and `opened_on`; each rent with AffordableHousing.com, the place and the `fetched_at` date; point people to the housing authority itself to apply.
7. **Over time:** store each answer with its `fetched_at`; waiting lists open and close as agencies update them, and that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `state` | string | required | A US state: 2-letter code (`TX`, `CA`, `DC`) or its name |
| `city` | string | none | A city in the state (`suggestions` `places[].search.city`), 2-80 characters |
| `county` | string | none | Or a county in the state (`Harris`). Leave out city and county to search the whole state |
| `zip` | string | none | A 5-digit ZIP code, sent with its `city` and `state` |
| `beds` | integer or list | none | 0 (studio) to 4, or 5 for 5+; one number or a list (`[2, 3]`, up to 10) |
| `baths_min` | integer | none | At least this many bathrooms, 1-5 |
| `property_type` | string or list | none | `apartment`, `condo`, `townhouse` or `house` (single family house) |
| `price_min`, `price_max` | integer | none | Lowest (0-100,000) and highest (1-100,000) monthly rent, USD |
| `sort` | string | `default` | `default` (the site's own order), `price_asc`, `price_desc`, `newest` (last updated), `beds_asc`, `beds_desc`, `sqft_asc`, `sqft_desc` or `affordability`. Premium and spotlight listings come first in every sort |
| `page` | integer | 1 | 1-500, 42 listings a page |
| `pet_friendly` | boolean | false | Pet-friendly listings |
| `section8` | boolean | false | Listings whose owner has experience with the Section 8 / Housing Choice Voucher program |
| `utilities_included` | boolean | false | The site's utilities-included filter |
| `age_restricted` | boolean | false | Age-restricted (senior) housing |
| `accessibility` | string or list | none | `physical` (ramps, grab bars, roll-in showers) and / or `visual_hearing` (visual alarms and doorbells) |

### Listing, suggestions, waiting lists and housing authorities

| Endpoint | Parameters |
|---|---|
| `/listing` | one of `id` (`listings[].id`, `766073`) or `url` (`listings[].url`, an affordablehousing.com `/<city>-<st>/<name>-<id>/` link), 20-400 characters |
| `/suggestions` | `text` (2-80 characters: the start of a city, county or ZIP code); `limit` (1-100, default 25) |
| `/waiting-lists` | `state` (optional: a code or name; leave out for every open list nationwide) |
| `/housing-authority` | one of `url` (`agency_url` from waiting lists, `agencies[].url`) or `id` (`agency_id`, `agencies[].id`, e.g. `674`) with `state` (`MA`) |
| `/housing-authorities` | `state` (required) |

## Examples

### Open waiting lists in a state

```bash
curl -X POST https://api.scavio.dev/api/v1/affordablehousing/waiting-lists \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"state": "TX"}'
```

Captured `data` (2026-11-26; `open` cut to 2 of 50, `agency_url` dropped, `notes` dropped):

```json
{
  "state": "TX",
  "title": "Section 8 Waiting Lists in Texas",
  "count": 50,
  "open": [
    {"waitlist_id": null, "name": "Abilene Housing Authority Section 8 Waiting List", "program": "Section 8 (HCV)", "agency_id": "593", "agency_name": "Abilene Housing Authority", "state": "TX", "online_application": false, "status": "Open", "opened_on": "10/31/2022"},
    {"waitlist_id": null, "name": "Alice Housing Authority Section 8 Waiting List", "program": "Section 8 (HCV)", "agency_id": "3566", "agency_name": "Alice Housing Authority", "state": "TX", "online_application": false, "status": "Open", "opened_on": "07/01/2021"}
  ],
  "opening_soon_count": 0,
  "opening_soon": []
}
```

### One housing authority

```bash
curl -X POST https://api.scavio.dev/api/v1/affordablehousing/housing-authority \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "674", "state": "MA"}'
```

Captured `data` (2026-11-26; `jurisdiction` cut to 3 of 14, `waiting_lists` to 2 of 12, `url` and `notes` dropped):

```json
{
  "id": "674",
  "name": "Somerville Housing Authority",
  "address": "30 Memorial Road",
  "address2": null,
  "city": "Somerville",
  "county": "Middlesex",
  "state": "MA",
  "zip": "02145",
  "phone": "617-625-1152",
  "fax": "617-628-7057",
  "website": "http://sha-web.org/",
  "hcv_url": "http://sha-web.org/section8.aspx",
  "latitude": 42.39599,
  "longitude": -71.09231,
  "participant_code": "MA031",
  "waitlist_status": "Open",
  "waitlist_open_date": null,
  "waitlist_close_date": null,
  "voucher_count": 1193,
  "section8_inventory": 1193,
  "programs": ["Section 8 (HCV)", "Other"],
  "jurisdiction": [
    {"county": "Middlesex", "full_county": false},
    {"county": "Essex", "full_county": true},
    {"county": "Suffolk", "full_county": true}
  ],
  "waiting_lists": [
    {"id": "78", "name": "Somerville Primary", "program": "Section 8 (HCV)", "selected_by": "First in, First out", "centralized": true},
    {"id": "946", "name": "Capen Court", "program": "Project Based Section 8 Housing", "selected_by": "First in, First out", "centralized": false}
  ]
}
```

A state's agencies (`{"state": "CA"}`, captured): `{"state": "CA", "total": 103, "count": 14, "agencies": [{"id": "1136", "name": "Housing Authority Of Fresno County", "address": "1331 Fulton Street, Fresno CA,93721", "waitlist_status": "Closed", "programs": ["Section 8 (HCV)"], "jurisdiction": "Serving all of Fresno County"}, ...]}`.

### Section 8 rentals in a city

```bash
curl -X POST https://api.scavio.dev/api/v1/affordablehousing/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"state": "CA", "city": "Los Angeles", "beds": [1, 2], "section8": true}'
```

Captured `data` (2026-11-26; `listings` cut to 1 of 42, its `title` shortened and its `url` and `photo` dropped; `notes` dropped):

```json
{
  "state": "CA",
  "city": "Los Angeles",
  "county": null,
  "zip": null,
  "currency": "USD",
  "filters": {"beds": [1, 2], "baths_min": null, "property_type": [], "price_min": null, "price_max": null, "pet_friendly": false, "section8": true, "utilities_included": false, "age_restricted": false, "accessibility": []},
  "sort": "default",
  "title": "Rental Properties in Los Angeles, CA",
  "total": 3279,
  "page": 1,
  "page_size": 42,
  "pages": 79,
  "has_more": true,
  "count": 42,
  "listings": [
    {
      "id": "836310",
      "title": "Introducing Haven On Orange, a brand new, affordable housing solution ...",
      "address": "2900 S Orange Dr Los Angeles CA 90016",
      "unit": "102",
      "city": "Los Angeles",
      "county": "Los Angeles",
      "state": "CA",
      "zip": "90016",
      "latitude": 34.0273819,
      "longitude": -118.3550139,
      "property_type": "Apartments",
      "rent_min": 1999,
      "rent_max": 1999,
      "currency": "USD",
      "beds_min": 2,
      "beds_max": 2,
      "baths_min": 1,
      "baths_max": 1,
      "sqft_min": 569,
      "sqft_max": 569,
      "year_built": 2025,
      "unit_count": 12,
      "section8_accepted": true,
      "trusted_owner": true,
      "income_restricted": true,
      "government_listing": false,
      "special_offer": false,
      "room_for_rent": false,
      "tier": "spotlight",
      "availability": "Available Now",
      "is_new": false,
      "just_updated": false
    }
  ]
}
```

The search notes say: "Premium and spotlight listings (tier) are placed first by AffordableHousing.com; the sort applies within each tier." and "section8_accepted is the listing's badge for an owner with experience with the Section 8 / Housing Choice Voucher program. listings[].url (or listings[].id) is the input of listing."

### One listing

```bash
curl -X POST https://api.scavio.dev/api/v1/affordablehousing/listing \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "766073"}'
```

Captured `data` (2026-11-26; `models` cut to 2 of 7 and their `description` dropped; `url`, `description`, `photos` and `notes` dropped):

```json
{
  "id": "766073",
  "name": "The Reserve At Westwood 10225 Bissonnet St in Houston, TX 77036",
  "title": "Houston Complex With Move In Specials and Great Apartments With Tons Of Space",
  "listing_status": "active",
  "date_posted": "2026-01-09",
  "address": {"street": "10225 Bissonnet St", "city": "Houston", "county": "Harris", "state": "TX", "zip": "77036", "country": "US"},
  "property_type": "apartment",
  "currency": "USD",
  "rent_min": 810,
  "rent_max": 1480,
  "rent_text": "$810 - $1,480",
  "beds": "1, 2",
  "sqft_min": 653,
  "sqft_max": 1332,
  "section8_accepted": true,
  "pets_allowed": true,
  "pets_max": 2,
  "age_restriction": "No",
  "age_restricted": false,
  "models": [
    {"id": "3428803", "name": "2 Beds 2 Baths 976 Sq. Ft.", "beds": 2, "full_baths": 2, "half_baths": 0, "sqft": 976, "rent": 1265, "rent_text": "$1,265", "deposit": 0, "deposit_negotiable": true, "year_built": null, "property_type": "apartment", "available_date": "2026-05-11", "accepting_applications": true, "subsidized_units": null, "units": []},
    {"id": "3428804", "name": "1 Bed 1 Bath 653 Sq. Ft.", "beds": 1, "full_baths": 1, "half_baths": 0, "sqft": 653, "rent": 810, "rent_text": "$810", "deposit": 0, "deposit_negotiable": true, "year_built": null, "property_type": "apartment", "available_date": "2026-05-11", "accepting_applications": true, "subsidized_units": null, "units": []}
  ],
  "fees": {"move_in_total": {"min": 0, "max": 0, "text": "$0"}, "move_out_total": {"min": 0, "max": 0, "text": "$0"}, "estimated_monthly_total": null, "estimated_one_time_total": {"min": 0, "max": 0, "text": "$0"}, "application_fee": 50, "pet_rent": 30, "pet_deposit": 0, "pet_fee_one_time": 400},
  "utilities": {"tenant_pays": ["Electric", "Cooking Fuel (Electric)", "Water (City Water)", "Cooling (Central)", "Sewer (Public Sewer)", "Heating (Electric)", "Hot Water (Electric)", "Trash pickup", "Pest control"], "owner_pays": ["Lawn care/Snow removal"]},
  "amenities": {"community_amenities": ["Additional Storage", "Bicycle Storage", "On-Site Management", "Online Payment", "On-Site Laundry", "Gym/Fitness Center", "Barbeque Area", "Playground"], "security_features": ["Gated Community", "Controlled Access"]},
  "accessibility": {},
  "listed_by": "Reserve at Westwood"
}
```

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/affordablehousing/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Houston"}'
```

Captured: `total` 18, places such as `{"label": "Houston County, TX", "type": "county", "state": "TX", "county": "Houston", "city": null, "zip": null, "population": 22911, "search": {"state": "TX", "county": "Houston"}}`. A ZIP code suggestion carries no city or state (`"search": null`): search a ZIP code with its city and state.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def ah(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/affordablehousing/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# Open waiting lists in a state (1 credit)
wl = ah("waiting-lists", {"state": "TX"})["data"]
print(wl["count"], "open lists in", wl["state"])
for w in wl["open"][:5]:
    print(" ", w["agency_name"], "|", w["program"], "| opened", w["opened_on"], "| online", w["online_application"])

# The agency behind the first list (1 credit)
ha = ah("housing-authority", {"url": wl["open"][0]["agency_url"]})["data"]
print(ha["name"], ha["phone"], ha["website"], "vouchers", ha["voucher_count"], "status", ha["waitlist_status"])

# Section 8 rentals in a city (2 credits)
s = ah("search", {"state": "TX", "city": "Houston", "section8": True, "sort": "price_asc"})["data"]
print(s["total"], "listings,", s["pages"], "pages")
for l in s["listings"][:5]:
    print(" ", l["id"], l["rent_min"], l["rent_max"], l["beds_min"], l["tier"], l["address"])

# Store each answer with fetched_at: that stored set is your record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every answer carries `notes`.

- **search** - `state`, `city`, `county`, `zip`, `currency`, `filters`, `sort`, `title`, `total`, `page`, `page_size` (42), `pages`, `has_more`, `count`, `listings[]` {`id` (the input of listing), `title`, `address`, `unit`, `city`, `county`, `state`, `zip`, `latitude`, `longitude`, `property_type`, `rent_min`, `rent_max`, `currency`, `beds_min`, `beds_max`, `baths_min`, `baths_max`, `sqft_min`, `sqft_max`, `year_built`, `unit_count`, `section8_accepted`, `trusted_owner`, `income_restricted`, `government_listing`, `special_offer`, `room_for_rent`, `tier`, `availability`, `is_new`, `just_updated`, `url`, `photo`, `photo_count`}, `notes`.
- **listing** - `id`, `url`, `name`, `title`, `listing_status`, `date_posted`, `address` {`street`, `city`, `county`, `state`, `zip`, `country`}, `latitude`, `longitude`, `property_type`, `currency`, `rent_min`, `rent_max`, `rent_text`, `beds`, `baths`, `sqft_min`, `sqft_max`, `section8_accepted`, `pets_allowed`, `pets_max`, `age_restriction`, `age_restricted`, `description`, `models[]`, `fees`, `utilities` {`tenant_pays`, `owner_pays`}, `amenities` and `accessibility` (by the listing's groups), `photos`, `listed_by`, `notes`.
- **suggestions** - `text`, `total`, `count`, `places[]` {`label`, `type` (city, county or zip), `state`, `county`, `city`, `zip`, `population`, `search`}, `notes`.
- **waiting lists** - `state`, `title`, `count`, `open[]`, `opening_soon_count`, `opening_soon[]`, `notes`.
- **housing authority** - `id`, `name`, `address`, `address2`, `city`, `county`, `state`, `zip`, `phone`, `fax`, `website`, `hcv_url`, `latitude`, `longitude`, `participant_code`, `waitlist_status`, `waitlist_open_date`, `waitlist_close_date`, `voucher_count`, `section8_inventory`, `programs`, `jurisdiction[]` {`county`, `full_county`}, `waiting_lists[]`, `url`, `notes`.
- **housing authorities** - `state`, `total`, `count`, `agencies[]` {`id`, `name`, `address`, `waitlist_status` (Open or Closed), `programs`, `jurisdiction`, `url`}, `notes`.

## Guardrails

- Name it "AffordableHousing.com (affordablehousing.com, the US affordable and Section 8 rental site)" on first mention, "AffordableHousing.com" after that.
- Waiting lists: quote each with its agency, program, `status` and `opened_on` as AffordableHousing.com lists it, with the `fetched_at` date, and say that the housing authority itself decides who can apply and when; never tell someone they qualify or will get a voucher.
- Section 8 badge: describe `section8_accepted` as "the listing's badge for an owner with experience with the Section 8 program", never as a guarantee that a voucher is accepted.
- Rents: USD per month with AffordableHousing.com, the place and the `fetched_at` date; say when a page is sorted within tiers.
- No landlord personal data: never try to identify or contact a private landlord. Name an owner only where `listed_by` gives a business name. A housing authority's public office phone, fax, address and website are public agency details; no staff contact details are returned or should be looked up.
- Fair Housing: describe listings with the data as AffordableHousing.com gives it; do not characterize an area by who lives there, do not steer anyone toward or away from an area, and do not filter or rank people by any protected characteristic. Age-restricted (senior) and accessibility filters describe the housing, not the applicant.
- Descriptive only: no commentary on AffordableHousing.com's business, its listing tiers or any housing authority's practices.
- Do not republish listing photos or descriptions in bulk. Write affordablehousing.com as plain text and cite listing ids, agency ids and capture dates rather than linking its pages.
- Terms: Scavio keeps no copy: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no application, contact or login flow. AffordableHousing.com's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate rents, waiting list dates, voucher counts, listing ids or agency ids. Return what the API returned, with the `fetched_at` time.
- Not available: applications or eligibility checks, payment standard or fair market rent numbers, private landlord names or contacts, agency staff contacts, listings past page 500, a voucher calculator.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `state`, or a state that is not one ("state must be a US state: a 2-letter code (TX, CA, DC) or its name. AffordableHousing.com is US only."); a ZIP code without its city ("zip needs its city too (AffordableHousing.com searches a ZIP code within a city and state), e.g. zip 10001 with city New York and state NY.") or one that is not 5 digits; both city and county ("send city (optionally with zip) or county, not both."); "price_min must not be above price_max."; a `sort`, `property_type` or `accessibility` value outside its list; `/listing` without exactly one of `url` or `id` ("send one of url or id.") or with a link that is not a listing; `/housing-authority` with both ("send url, or id with state, not both.") or neither ("send url or id (with state): ..."); suggestions under 2 characters. A value the request schema rejects (a type, range or list) answers with `error` and a `details` array naming each invalid field.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "AffordableHousing.com has no listing with this id (it may have been taken down). Use a url or id from search listings[].", "AffordableHousing.com has no housing authority with this id in this state. Use an agency_url from waiting-lists or housing-authorities.", "AffordableHousing.com has no waiting list page for this state.", "AffordableHousing.com has no housing authority page for this state.", "AffordableHousing.com has no search for this place.". A search that matches nothing answers `200` with `total` 0 and a note: "No listings matched. Use suggestions for the place names AffordableHousing.com searches (a ZIP code is searched within its city and state)."
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=affordable-housing-api).
- `502` means AffordableHousing.com data was temporarily unavailable ("AffordableHousing.com is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("AffordableHousing.com is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.98.0
npm install scavio@0.99.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: lists } = await scavio.affordablehousing.waitingLists({ state: "TX" });
const { data: agency } = await scavio.affordablehousing.housingAuthority({ id: "674", state: "MA" });
const { data: agencies } = await scavio.affordablehousing.housingAuthorities({ state: "CA" });
const { data: rentals } = await scavio.affordablehousing.search({ state: "CA", city: "Los Angeles", beds: [1, 2], section8: true });
const { data: listing } = await scavio.affordablehousing.listing({ id: "766073" });
const { data: places } = await scavio.affordablehousing.suggestions({ text: "Houston" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.affordablehousing.search(...)`, `listing`, `suggestions`, `waiting_lists`, `housing_authority` and `housing_authorities`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 6 endpoints as tools: `search_affordablehousing`, `get_affordablehousing_listing`, `get_affordablehousing_suggestions`, `get_affordablehousing_waiting_lists`, `get_affordablehousing_housing_authority` and `get_affordablehousing_housing_authorities`. AffordableHousing.com is opt-in: add `affordablehousing` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.98.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,affordablehousing"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/affordablehousing-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=affordable-housing-api), [listing](https://scavio.dev/docs/affordablehousing-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=affordable-housing-api), [suggestions](https://scavio.dev/docs/affordablehousing-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=affordable-housing-api), [waiting lists](https://scavio.dev/docs/affordablehousing-waiting-lists?utm_source=agent-skills&utm_medium=skill&utm_campaign=affordable-housing-api), [housing authority](https://scavio.dev/docs/affordablehousing-housing-authority?utm_source=agent-skills&utm_medium=skill&utm_campaign=affordable-housing-api), [housing authorities](https://scavio.dev/docs/affordablehousing-housing-authorities?utm_source=agent-skills&utm_medium=skill&utm_campaign=affordable-housing-api). Overview: [AffordableHousing.com API](https://scavio.dev/affordablehousing-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=affordable-housing-api).
