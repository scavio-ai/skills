---
name: compass-real-estate-api
description: Compass Real Estate API for Compass (compass.com, the US real estate brokerage whose site also lists Coldwell Banker, Corcoran and Sotheby's International Realty homes) - what a US home is listed at, and what it sold for, as Compass shows it (24 Cousteau Lane in Westlake, Austin was listed at $12,995,000 on Sep 14, 2026, went pending Nov 5 and sold Nov 23 for $12,000,000 after 52 days on market, source MLS ACTRIS) with the listing history (Listed, Price Change, Pending, Contract Signed, Sold, Sold (Public Record)), listed, last asking and sold price, price per square foot, monthly charges, tax and assessed values, key details, amenities, schools with ratings, the building, lease terms on rentals, the listing brand and the source MLS with its disclaimer; home search for sale, for rent or sold in the last 90 days by city, ZIP, neighborhood, county or school area, 41 listings a page through the first 369 results, with highest price, fewest beds, baths and square feet, property type, open house this weekend and coming soon filters and price sorts, each card with price, beds, baths, size, status, sold date, brand, badges and open house times; place, ZIP, school and address suggestions with the area slugs search takes. 3 endpoints, 2 credits per call. US only, USD. No agent names, emails, phones or license numbers, no reviews, no market reports.
version: 1.0.0
tags: compass, compass-com, compass-real-estate, compass-real-estate-api, compass-api, compass-homes, compass-listings, compass-for-sale, compass-rentals, compass-sold, compass-sold-homes, compass-coming-soon, compass-open-house, compass-listing-history, compass-sold-price, coldwell-banker, corcoran, sothebys-international-realty, homes-for-sale, homes-for-rent, recently-sold, sold-prices, listing-history, price-history, coming-soon-listings, open-houses, mls-data, real-estate, real-estate-data, property-data, us-real-estate, usd, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/compass-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=compass-real-estate-api
---

# Compass Real Estate API - Homes For Sale, Rentals, Sold Listings

Read Compass (compass.com, the US real estate brokerage): home search for sale, for rent or sold in the last 90 days in a US area; one listing in full with its price, listing history, sold price, details, schools and building; and the search box suggestions that give the area slugs. Since Compass merged with Anywhere Real Estate in January 2026, compass.com also lists homes under the Coldwell Banker, Corcoran and Sotheby's International Realty brands, and each card says which. Every answer is what Compass's public pages show a visitor without an account at the moment of the call, in USD. All 3 endpoints return structured JSON at 2 credits per call.

**Read-only data.** This skill reads the public pages Compass shows to any visitor and returns them as JSON for analysis. It uses no Compass account, no saved search, no tour or contact request and no agent page.

**The job this skill is for: what a home is listed at, what it sold for, and what else is on the market around it.** `/search` returns 41 listings a page with price, status and the listing brand; `/listing` returns one home's listed, last asking and sold price, every event in its listing history with its date and source MLS, days on market, tax and the monthly charges. Captured 2026-11-26 (2 credits per call):

| Request | What Compass showed |
|---|---|
| `/search` Manhattan (`manhattan-ny`) for sale, 2+ beds, up to $2,000,000 | `total` 1,219 (369 reachable); the 41 cards on page 1 ran from $130,000 to $1,995,000, brands Compass, Corcoran and Sotheby's International Realty |
| `/search` Los Angeles (`Los Angeles, CA`) for rent, 1+ bed, up to $4,000 | `total` 2,550; page 1 rents ran from $1,650 to $4,000 a month, status `active` or `coming_soon`, brands Century 21, Coldwell Banker, Coldwell Banker Realty, Compass and Sotheby's International Realty |
| `/search` Austin (`austin-tx`) sold in the last 90 days, single family, `price_desc` | `total` 1,857; page 1 ran from $2,790,000 to $12,995,000 |
| `/listing` 24 Cousteau Lane, Austin, TX 78746 (Westlake) | listed $12,995,000 on 2026-09-14, Pending 2026-11-05, Active Under Contract 2026-11-13, Sold 2026-11-23; `sold_price` $12,000,000 (`sold_price_verification` "Unverified"), 52 days on market, $1,339.69 per sq ft, 2025 tax $50,041, source MLS ACTRIS |
| `/listing` 77 Bleecker Street, Unit 121, Manhattan, NY 10012 | Co-op listed $1,875,000 on 2026-11-01, 24 days on market, maintenance $3,629 a month, 20% minimum down payment, building Bleecker Court (251 residences, built 1930), 118 schools listed with ratings |

Quote each price with Compass, the address or listing id, the status and the `fetched_at` date. A sold card's `price` is the price Compass prints on the card (the Cousteau Lane card read $12,995,000); the recorded sale price is `pricing.sold_price` on `/listing`, with its `sold_price_verification` label. For the same home or area on other sites use `zillow-property-data`, `redfin-property-data` or `realtor-com-property-data`, matched on address.

Ten limits shape every answer, so say them plainly:
- **2 credits per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **41 listings a page, 9 pages.** Compass pages through the first 369 results of a search, whatever `total` says (Los Angeles rentals: 2,550 counted, 369 reachable). `reachable`, `pages` and `has_more` say what can be read, and a note says so when `total` is higher. Narrow the area or the filters to reach the rest. A page past the end answers with no listings and a note.
- **Sold means the last 90 days.** `mode: "sold"` covers homes sold in Compass's recently sold window (`criteria.sold_within_days: 90`). Sold cards are ordered by Compass's own price field, so with a price sort they run close to, not strictly in, price order.
- **Filters Compass applies, and the ones it does not.** Highest price, fewest beds, baths and square feet, property type, open house and coming soon work. Compass does not apply a minimum price or a maximum bedroom count next to other filters, nor year built or lot size: `price_min`, `beds_max`, `year_built_min`, `year_built_max`, `lot_min` and `lot_size_min` are refused with a `400` instead of being dropped silently. `criteria` echoes the filters as Compass applied them.
- **Prices as Compass shows them.** USD; rentals per month (`price_period: "month"`). `sold_price` is the recorded sale price with Compass's verification label; `last_property_sale_price` and `history` entries marked `public_record` come from public records.
- **Brand, not agent.** `brand` is the listing brand (Compass, Corcoran, Coldwell Banker, Coldwell Banker Realty, Century 21, Sotheby's International Realty) and can be `null` (the Austin sold cards). No agent names, emails, phones, license numbers or photos are returned, and phone numbers and emails are taken out of descriptions.
- **The source MLS and its disclaimer.** `source_mls` names the MLS the listing comes from (ACTRIS, CRMLS, CLAW, or "Manual" for a listing Compass entered itself); `disclaimer` and `mls_disclaimer` are the texts Compass shows with the listing. Carry them when you quote listing data.
- **Undisclosed addresses.** Some suggestions come back as "Undisclosed Address" (two of the three listings for `90012`); quote them as Compass shows them.
- **Slow pages.** In the captures suggestions answered in 1.4 to 2.5 seconds, a listing in 3.8 to 7.3 and a search in 3.6 to 25. Set a client timeout of at least 240 seconds and send one request at a time.
- **What is not there.** No agent directory or agent profiles, no reviews or ratings (Compass publishes none), no market reports or price trends, no building pages, no tours, contact or financing.

Compass publishes no public developer API. This skill reads Compass's public pages with one Scavio key.

See also: `zillow-property-data`, `redfin-property-data`, `realtor-com-property-data`, `trulia-api` (neighborhood survey and market snapshot), `streeteasy-api` (New York City listings and market data). Same home or same area only: match on address, name the site and date with every number.

## When to trigger

Use this skill when the user asks to:
- Search Compass homes for sale, for rent or sold in the last 90 days in a US city, ZIP, neighborhood, county or school area
- Filter Compass listings by highest price, fewest bedrooms, bathrooms or square feet, property type (homes, condos, townhomes, co-ops, multi-family, land), open house this weekend or coming soon
- Read one Compass listing in full: listed, last asking and sold price, listing history, days on market, monthly charges, tax and assessed values, key details, amenities, schools, the building and lease terms
- Find what a home sold for on Compass and how long it was on the market
- See which brand (Compass, Corcoran, Coldwell Banker, Sotheby's International Realty) lists a home, and which MLS the listing comes from
- Look up the area slugs and listing ids Compass uses for a place, ZIP, school or address

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=compass-real-estate-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=compass-real-estate-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 2 credits, so 50 credits cover 25 calls (for example 8 areas: one suggestions lookup, one search and one listing each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures suggestions answered in 1.4-2.5 seconds, listing 3.8-7.3 and search 3.6-25. Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/compass/search` | Homes for sale, for rent or sold in the last 90 days in a US area: 41 a page, up to 9 pages (the first 369 results), filters, price sorts, `total`, `reachable`, `criteria` as Compass applied them; each card with price, beds, baths, size, lot, type, status, sold date, brand, badges, open houses and photos | 2 |
| `POST /api/v1/compass/listing` | One listing by link or id: address, size, description, pricing (listed, last asking, sold price with its verification, price per sq ft, monthly charges, financing), dates, days on market, listing history, key details, amenities, schools, building, rental terms, tax, brand, source MLS and disclaimers | 2 |
| `POST /api/v1/compass/suggestions` | Search box suggestions for a place, ZIP, school or address: areas with the `slug` search takes, and listings with the `id` listing takes | 2 |

## Market

US only, English, USD. There is no `country`, `language` or `currency` input. Prices on `for_rent` are monthly rents.

## Pricing and history fields

| Field | Meaning |
|---|---|
| `pricing.price`, `price_text`, `price_period` | The price Compass shows now (`price_period` "month" on rentals) |
| `pricing.listed_price`, `last_asking_price` | The price the home was listed at, and the last asking price |
| `pricing.sold_price`, `sold_price_verification` | The recorded sale price and Compass's label for it ("Unverified" on the Cousteau Lane capture) |
| `pricing.price_per_sqft` | Compass's price per square foot |
| `pricing.monthly_charges`, `monthly_charges_incl_taxes` | Monthly charges (maintenance, HOA) and the same with taxes, as Compass states them |
| `pricing.max_financing_percent`, `min_down_payment_percent` | Financing terms a co-op or condo listing states (80 and 20 on 77 Bleecker Street) |
| `pricing.last_property_sale_price`, `dates.last_property_sale` | The last recorded sale of the property |
| `dates` | {`listed`, `contract`, `sold`, `available`, `updated`, `last_property_sale`} |
| `days_on_market`, `cumulative_days_on_market` | As Compass gives them |
| `history[]` | {`date`, `event` (Listed (Active), Price Change, Pending, Active Under Contract, Contract Signed, Sold, Sold (Public Record), Expired, Withdrawn / Cancelled), `price`, `source` (the MLS), `public_record`, `record_url`} |
| `tax` | {`tax_year`, `tax`, `monthly_tax`, `assessment_year`, `land_value`, `improvement_value`} |
| `brand`, `source_mls`, `disclaimer`, `mls_disclaimer` | The listing brand, the MLS the listing comes from and the texts Compass shows with it |

- **Two prices on a sold home.** The search card's `price` is the price printed on the card; `pricing.sold_price` on `/listing` is the recorded sale. Quote each with its label.
- **History from more than one MLS.** A home listed in two MLSs shows each event once per source (the North Hollywood rental capture lists "Listed (Active)" from both CLAW and CRMLS on 2026-11-19); say which source each event comes from.

## Workflow

1. **Area slug.** `/suggestions` (`{"q": "Austin, TX"}`): `areas[].slug` is the `area` input of `/search` (`austin-tx`, `los-angeles-ca-90012`, `school-district/austin-independent-school-district-4808940`); `listings[].id` is the `id` input of `/listing`.
2. **Search.** `/search` with `area`, `mode` and filters. Check `total` against `reachable`, `criteria` and the notes.
3. **One listing.** `/listing` with `id` (or `url`) from `listings[]`. Read `pricing`, `history`, `days_on_market`, `source_mls`.
4. **Report.** Each price with Compass, the address, the status, the brand and the `fetched_at` date; a sold price with its verification label; the source MLS and its disclaimer when you quote listing data.
5. **Over time:** store each answer with its `fetched_at`; listings change status and price as Compass updates them, and that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `area` | string | required | A Compass area slug from suggestions (`areas[].slug`): a city (`austin-tx`, `manhattan-ny`), a city and ZIP (`los-angeles-ca-90012`), a neighborhood (`brooklyn-heights-brooklyn-ny`), a county, or a school (`school/<slug>`, `school-district/<slug>`). A place written as `"Austin, TX"` reads as its slug. 2-160 characters. An unknown area is a charged `404` |
| `mode` | string | `for_sale` | `for_sale`, `for_rent` or `sold` (homes sold in the last 90 days) |
| `price_max` | integer | none | Highest price, USD (monthly rent on `for_rent`), 1 to 1,000,000,000 |
| `beds_min` | integer | none | Fewest bedrooms, 1-10 |
| `baths_min` | integer | none | Fewest bathrooms, 1-10 |
| `sqft_min` | integer | none | Smallest size in square feet, 1-100,000 |
| `property_type` | string | none | `homes` (single family), `condos`, `townhomes`, `co_ops`, `multi_family` or `land` |
| `open_house` | boolean | false | `for_sale` only: homes with an open house this weekend |
| `coming_soon` | boolean | false | `for_sale` only: Coming Soon listings. Send one of `open_house` or `coming_soon`, not both |
| `sort` | string | `default` | `default` (Compass's own order), `price_asc` or `price_desc` |
| `page` | integer | 1 | 1-9, 41 listings a page |

### Listing (`/listing`) and suggestions (`/suggestions`)

| Endpoint | Parameters |
|---|---|
| `/listing` | one of `id` (a Compass listing id, `listings[].id`, digits as a string: `2222080658253107193`) or `url` (a compass.com listing link: `listings[].url` or `property_url`, `/homedetails/<address>/<id>_lid/` or `/<code>_pid/`; a suggestions `/listing/<id>/view` link works too), 5-400 characters |
| `/suggestions` | `q` (2-80 characters: a city, neighborhood, ZIP code, school or address) |

## Examples

### Homes for sale in an area

```bash
curl -X POST https://api.scavio.dev/api/v1/compass/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"area": "manhattan-ny", "beds_min": 2, "price_max": 2000000}'
```

Captured `data` (2026-11-26; `listings` cut to 1 of 41, its `url`, `property_url`, `photo` and `thumbnail` dropped; `nearby_areas` cut to 2 of 5):

```json
{
  "mode": "for_sale",
  "area": {"slug": "manhattan-ny", "location_id": 21425},
  "sort": "default",
  "page": 1,
  "per_page": 41,
  "total": 1219,
  "reachable": 369,
  "pages": 9,
  "has_more": true,
  "count": 41,
  "criteria": {"listing_type": "sale", "price_max": 2000000, "beds_min": 2, "baths_min": null, "sqft_min": null, "property_types": [], "open_house": false, "coming_soon": false, "sold_within_days": null},
  "listings": [
    {
      "id": "2222080658253107193",
      "address": "77 Bleecker Street, Unit 121",
      "neighborhood": "Greenwich Village",
      "city": "Manhattan",
      "state": "NY",
      "zip": "10012",
      "latitude": 40.726966,
      "longitude": -73.99609339999999,
      "price": 1875000,
      "price_text": "$1,875,000",
      "price_period": null,
      "currency": "USD",
      "beds": 2,
      "baths": 2,
      "baths_detail": "2 full",
      "sqft": null,
      "lot_size": null,
      "property_types": ["Co-op"],
      "status": "active",
      "status_code": 0,
      "sold_date": null,
      "brand": "Compass",
      "badges": ["Listed By Compass", "Virtual Tour"],
      "open_houses": []
    }
  ],
  "nearby_areas": [
    {"name": "Brooklyn Heights", "slug": "brooklyn-heights-brooklyn-ny"},
    {"name": "Carroll Gardens", "slug": "carroll-gardens-brooklyn-ny"}
  ],
  "notes": ["Compass counts 1219 matches but pages through the first 369 only (9 pages of 41); narrow the area or the filters to reach the rest."]
}
```

### Rentals, and homes sold in the last 90 days

```bash
curl -X POST https://api.scavio.dev/api/v1/compass/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mode": "for_rent", "area": "Los Angeles, CA", "beds_min": 1, "price_max": 4000}'

curl -X POST https://api.scavio.dev/api/v1/compass/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mode": "sold", "area": "austin-tx", "property_type": "homes", "sort": "price_desc"}'
```

A captured rental card (2026-11-26; links and photos dropped): `{"id": "2246212870948107401", "address": "5421 West Slauson Avenue, Los Angeles, CA 90056", "price": 3400, "price_text": "$3,400", "price_period": "month", "beds": 2, "baths": 1.75, "baths_detail": "1 full • 1 three-quarter", "sqft": 1600, "property_types": ["Rental"], "status": "coming_soon", "brand": "Coldwell Banker Realty", "badges": ["See It First", "Coldwell Banker Realty Coming Soon"]}`. A captured sold card: `{"id": "2194420550970771025", "address": "24 Cousteau Lane, Austin, TX 78746", "price": 12995000, "beds": 6, "baths": 7.5, "baths_detail": "6 full • 3 half", "sqft": 9700, "lot_size": "3.97 AC / 172,933 SF", "property_types": ["Single Family"], "status": "sold", "sold_date": "2026-11-23", "brand": null, "badges": ["Closed 11/23/26"]}`. The sold search's notes: "Sold searches cover homes sold in the last 90 days (Compass's recently sold window); listing returns a sold home's recorded sold price (pricing.sold_price) and its history." and "Compass orders sold homes by its own price field, so the card prices run close to, not strictly in, price order."

### One sold home: listed price, sold price and history

```bash
curl -X POST https://api.scavio.dev/api/v1/compass/listing \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "2194420550970771025"}'
```

Captured `data` (2026-11-26, the sold card's listing read by its link; cut to the fields below, `history` to its 4 latest events):

```json
{
  "listing_type": "sale",
  "status": "Closed",
  "mls_number": "4742126",
  "address": {"street": "24 Cousteau Lane", "city": "Austin", "state": "TX", "zip": "78746", "neighborhood": "Westlake", "county": "Travis County", "full": "24 Cousteau Lane, Austin, TX 78746"},
  "beds": 6,
  "baths": 7.5,
  "sqft": 9700,
  "lot_size": "3.97 AC / 172,933 SF",
  "pricing": {"price": 12995000, "price_text": "$12,995,000", "price_period": null, "currency": "USD", "listed_price": 12995000, "last_asking_price": null, "sold_price": 12000000, "sold_price_verification": "Unverified", "price_per_sqft": 1339.69, "monthly_charges": 233.17, "monthly_charges_incl_taxes": 5223.24, "max_financing_percent": null, "min_down_payment_percent": null, "last_property_sale_price": 12000000},
  "dates": {"listed": "2026-09-14T05:00:00.000Z", "contract": "2026-11-13T09:37:44.000Z", "sold": "2026-11-23T06:00:00.000Z", "available": null, "updated": "2026-11-23T17:39:50.557Z", "last_property_sale": "2026-11-23T06:00:00.000Z"},
  "days_on_market": 52,
  "history": [
    {"date": "2026-11-23T06:00:00.000Z", "event": "Sold", "price": null, "source": "ACTRIS", "public_record": false, "record_url": null},
    {"date": "2026-11-13T09:37:44.000Z", "event": "Active Under Contract", "price": null, "source": "ACTRIS", "public_record": false, "record_url": null},
    {"date": "2026-11-05T06:00:00.000Z", "event": "Pending", "price": null, "source": "ACTRIS", "public_record": false, "record_url": null},
    {"date": "2026-09-14T05:00:00.000Z", "event": "Listed (Active)", "price": 12995000, "source": "ACTRIS", "public_record": false, "record_url": null}
  ],
  "tax": {"tax_year": "2025", "tax": "$50,041", "monthly_tax": "$4,170", "assessment_year": "2026", "land_value": 2240000, "improvement_value": 1858434},
  "brand": null,
  "source_mls": "ACTRIS"
}
```

A captured co-op listing (77 Bleecker Street, Unit 121, by `id` `2222080658253107193`) adds the building: `{"id": "281916010771019189", "name": "Bleecker Court", "address": "77 Bleecker St", "floors": 5, "units": 251, "year_built": 1930}`, `key_details` such as `{"key": "Maintenance", "value": "$3,629 / month"}` and `{"key": "Pet Policy", "value": "Allowed"}`, 16 amenities ("Full-Time Doorman", "Elevator", "Washer / Dryer in Unit", ...), and `schools[]` items such as `{"name": "P.S. 3 Charrette School", "distance_miles": 0.65, "types": ["Public"], "grades": "PK-5", "rating": 6}`. A captured rental (by `id` `2242407599514522809`, North Hollywood, $3,395 a month) carries `rental` `{"lease_term": "Lease Length: 1+Year", "lease_term_min_months": null, "lease_term_max_months": null, "broker_fee_percent": null}`.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/compass/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "Austin, TX"}'
```

Captured `data` (2026-11-26; `areas` cut to 3 of 9, `url` dropped):

```json
{
  "q": "Austin, TX",
  "count": 10,
  "areas": [
    {"name": "Austin", "region": "TX", "slug": "austin-tx", "kind": "city", "location_id": 42626},
    {"name": "Austin Heights", "region": "Austin, TX", "slug": "austin-heights-austin-tx", "kind": "neighborhood", "location_id": 131488},
    {"name": "Austin Independent School District", "region": "Travis County, TX", "slug": "school-district/austin-independent-school-district-4808940", "kind": "school_district", "location_id": 197128}
  ],
  "listings": [
    {"id": "25240385865469537", "address": "1017 N Austin St", "region": "Denton, TX"}
  ]
}
```

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def compass(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/compass/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# The area slug (2 credits)
areas = compass("suggestions", {"q": "Austin, TX"})["data"]["areas"]
city = next(a for a in areas if a["kind"] == "city")

# Homes sold in the last 90 days, most expensive first (2 credits)
s = compass("search", {"mode": "sold", "area": city["slug"], "property_type": "homes", "sort": "price_desc"})["data"]
print(s["total"], "counted,", s["reachable"], "reachable")
for h in s["listings"][:5]:
    print(h["id"], h["price_text"], h["sold_date"], h["address"])

# The recorded sale price and history of the first one (2 credits)
L = compass("listing", {"id": s["listings"][0]["id"]})["data"]
p = L["pricing"]
print(L["address"]["full"], "listed", p["listed_price"], "sold", p["sold_price"], p["sold_price_verification"], L["days_on_market"], "days")
for e in L["history"]:
    print(" ", e["date"][:10], e["event"], e["price"], e["source"])

# Store each answer with fetched_at: that stored set is your record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Search answers carry `notes`.

- **search** - `mode`, `area` {`slug`, `location_id`}, `sort`, `page`, `per_page` (41), `total` (Compass's count), `reachable` (at most 369), `pages`, `has_more`, `count`, `criteria` {`listing_type`, `price_max`, `beds_min`, `baths_min`, `sqft_min`, `property_types`, `open_house`, `coming_soon`, `sold_within_days`}, `listings[]`, `nearby_areas[]` {`name`, `slug`}, `notes`.
- **listing card** - `id` (the input of listing), `url`, `property_url`, `address`, `neighborhood`, `city`, `state`, `zip`, `latitude`, `longitude`, `price`, `price_text`, `price_period`, `currency`, `beds`, `baths`, `baths_detail`, `sqft`, `lot_size`, `property_types`, `status` (active, pending, sold, coming_soon), `status_code`, `sold_date`, `brand`, `badges`, `open_houses[]` {`start`, `end`, `by_appointment_only`, `virtual`}, `photo`, `thumbnail`.
- **listing** - `id`, `url`, `property_url`, `property_code`, `mls_number`, `listing_type` (sale or rent), `status`, `mls_status`, `status_code`, `address` {`street`, `city`, `state`, `zip`, `neighborhood`, `county`, `full`}, `latitude`, `longitude`, `timezone`, `beds`, `baths`, `full_baths`, `half_baths`, `total_baths`, `rooms`, `sqft`, `lot_sqft`, `lot_size`, `stories`, `property_types`, `mls_property_type`, `description` (phone numbers and emails taken out), `pricing`, `dates`, `days_on_market`, `cumulative_days_on_market`, `history[]`, `key_details[]` {`key`, `value`}, `regional_details`, `details[]` {`category`, `sections[]` {`name`, `fields[]` {`key`, `values`}}}, `amenities`, `schools[]` {`name`, `distance_miles`, `types`, `grades`, `rating`, `url`}, `school_districts`, `building` {`id`, `name`, `address`, `floors`, `units`, `year_built`, `url`, `key_details`}, `rental` {`lease_term`, `lease_term_min_months`, `lease_term_max_months`, `broker_fee_percent`}, `tax`, `parcel_number`, `badges`, `photos`, `photo_count`, `brand`, `source_mls`, `disclaimer`, `mls_disclaimer`.
- **suggestions** - `q`, `count`, `areas[]` {`name`, `region`, `slug` (the area input of search), `kind` (city, zip, neighborhood, school, school_district or area), `location_id`, `url`}, `listings[]` {`id` (the id input of listing), `address`, `region`, `url`}. Agent suggestions are left out.

## Guardrails

- Name it "Compass (compass.com, the US real estate brokerage)" on first mention, "Compass" after that.
- Prices: USD with Compass, the address or listing id, the status and the `fetched_at` date; rents per month. A sold price is `pricing.sold_price` with its `sold_price_verification` label ("sold for $12,000,000, Unverified, per Compass, fetched Nov 26, 2026"), never the card price.
- Counts: quote `total` as Compass's count and say how many were `reachable`; never present page 1 as the whole market.
- No agent personal data: name the listing brand only, and do not try to identify a listing agent, a buyer, a seller or an owner.
- MLS data: name `source_mls` and carry the `disclaimer` and `mls_disclaimer` texts when you quote listing data.
- Fair housing: describe homes and areas with the data as Compass gives it; do not characterize an area by who lives there, and do not steer anyone toward or away from an area.
- Descriptive only: no commentary on Compass's business, its merger, its litigation or its listing policies.
- Do not republish Compass photos or descriptions in bulk. Write compass.com as plain text and cite listing ids, addresses and capture dates rather than linking Compass pages.
- Terms: Scavio keeps no copy: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no tour, contact or agent flow. Compass's terms of service cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, sold prices, dates, listing ids or area slugs. Return what the API returned, with the `fetched_at` time.
- Not available: agent names, phones, emails, licenses or profiles, reviews or ratings, market reports or trends, results past the first 369 of a search, tours, contact or financing.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `area`, or one that is not a slug or "City, ST" ("area must be a Compass area slug from suggestions (areas[].slug, e.g. austin-tx, manhattan-ny, los-angeles-ca-90012) or a place written as \"City, ST\"."); a filter Compass does not apply ("Compass does not apply a minimum price next to other filters, so price_min is not supported: use price_max and sort price_asc.", "Compass does not apply a maximum bedroom count next to other filters, so beds_max is not supported: use beds_min.", "Compass ignores a year-built filter on its search pages, so year_built_min is not supported.", "Compass ignores a lot-size filter on its search pages, so lot_min is not supported."); `open_house` or `coming_soon` outside `for_sale` ("open_house and coming_soon apply to mode for_sale only."); both at once ("send one of open_house or coming_soon, not both."); a `mode`, `sort` or `property_type` outside its list; a number out of range (`page` past 9, `beds_min` past 10); `/listing` without exactly one of `url` or `id` ("send one of url or id."), an id that is not 6-25 digits, or a link ("url must be a Compass listing link (listings[].url, ...)."); suggestions under 2 characters. A value the request schema rejects (a type, range or list) answers with `error` and a `details` array naming each invalid field.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Compass has no area <slug>. Look the place up with suggestions and send its areas[].slug (e.g. austin-tx, manhattan-ny, los-angeles-ca-90012).", "Compass has no listing <id>.", "Compass has no suggestions for <q>.". Take area slugs and listing ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=compass-real-estate-api).
- `502` means Compass data was temporarily unavailable ("Compass is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Compass is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.98.0
npm install scavio@0.99.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: homes } = await scavio.compass.search({ area: "manhattan-ny", beds_min: 2, price_max: 2000000 });
const { data: sold } = await scavio.compass.search({ mode: "sold", area: "austin-tx", property_type: "homes", sort: "price_desc" });
const { data: home } = await scavio.compass.listing({ id: "2222080658253107193" });
const { data: places } = await scavio.compass.suggestions({ q: "Austin, TX" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.compass.search(...)`, `listing` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 3 endpoints as tools: `search_compass`, `get_compass_listing` and `get_compass_suggestions`. Compass is opt-in: add `compass` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.98.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,compass"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/compass-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=compass-real-estate-api), [listing](https://scavio.dev/docs/compass-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=compass-real-estate-api), [suggestions](https://scavio.dev/docs/compass-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=compass-real-estate-api). Overview: [Compass API](https://scavio.dev/compass-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=compass-real-estate-api).
