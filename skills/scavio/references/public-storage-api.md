# Public Storage API - Storage Unit Prices, Facilities, Reviews

Read Public Storage (publicstorage.com, the US self-storage operator, also in Canada): facility search near a ZIP or postal code, a city or an address; one facility in full with every unit and its price; and every customer review a US facility shows. Every answer is what Public Storage's public pages show a visitor without an account at the moment of the call, in USD on the US site and CAD on the Canadian one. All 3 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Public Storage shows to any visitor and returns them as JSON for analysis. It uses no Public Storage account, no reservation, no rental, no lease and no payment flow.

**The job this skill is for: what a storage unit costs at a given facility, by size, as Public Storage prices it.** `/facility` returns every unit the facility page lists with its In-Store Rent, its Online price, the first and second month after the promotion, the move-in cost, the admin fee, the lock charge and the promotion as Public Storage words it. Captured 2026-11-26 (1 credit per call):

| Facility (`store_id`) | Unit | In-Store Rent | Online price | Promotion (as given) | Move-in cost |
|---|---|---|---|---|---|
| Public Storage - Dallas, TX (2044) | Small 5'x5' | 66 USD | 39.60 USD | 40% off For 4 Month | 68.60 USD |
| Public Storage - Dallas, TX (2044) | Medium 10'x10' | 135 USD | 67.50 USD | 50% off First 4 Months | 96.50 USD |
| Public Storage - Dallas, TX (2044) | Large 10'x20' | 208 USD | 124.80 USD | 40% off For 4 Month | 153.80 USD |
| Public Storage - Dorval, QC (7785, `market: "ca"`, `language: "fr"`) | Petit 5'x5' | 64 CAD | 32 CAD | 50 % de rabais sur les 4 premiers mois | 61 CAD |
| Public Storage - Dorval, QC (7785) | Moyen 10'x10' | 179 CAD | 89.50 CAD | 50 % de rabais sur les 4 premiers mois | 118.50 CAD |

The Dallas facility listed 20 units (`units_count`), carried a 4.7 rating from 422 reviews and a "One Time $29 Admin Fee Applies" note; the Dorval page listed 16 units and no reviews (Canadian pages show none). A search near ZIP 75201 sorted by price listed 10 facilities on page 1 of 2, the nearest 0.5 miles away with units starting from 32 USD; a search for "Toronto, ON" with `market: "ca"` listed 18 facilities in km and CAD. Quote each price with its label (In-Store Rent or Online price), the unit size, the facility and the `fetched_at` date. For other storage operators near the same place use `extra-space-storage-api`, matched on city or ZIP and unit size.

Nine limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Prices as the page gives them.** `in_store_rent` is the In-Store Rent and `online_price` the Online price; `first_month_rent`, `first_month_after_promotion`, `second_month_after_promotion`, `move_in_cost`, `admin_fee` and `lock_charge` are the page's own figures per unit. Promotions are Public Storage's as given and can vary between visits, so store each answer with its `fetched_at`.
- **No occupancy.** Public Storage does not publish how many units are free. `units_left` is set only where the page itself says so ("Limited availability - 1 unit left!"), otherwise `null`; `availability` is the page's own label when it shows one.
- **Search pages shallowly.** 9 to 19 facilities a page. A ZIP search pages through its search slug (`location.slug` with `page`, up to 20); a city or a Canadian search lists every facility on page 1. `pages` and `has_more` say what is left.
- **Search filters apply to the page.** The facility filters (climate control, drive-up, 24/7, business, vehicle, RV, boat storage, unit size) are applied to the facilities on the page by their own features; `listed` is what the page had and `count` what matched, and a note says so.
- **Search cards show some units.** `starting_from` is the card's "Units starting from" price, and `units` are the units the card shows (some cards show none). `/facility` lists every unit.
- **Reviews: US only, newest first, no names.** `/reviews` returns every review Public Storage shows for a US facility in one answer (819 five-star reviews for store 2223 in one call), newest first, its only order. Each has the rating, date, `source` as the page gives it (Google on every review seen) and text, which can be empty. No reviewer name is returned. Canadian facility pages show no reviews.
- **US and Canada.** `market: "us"` (default, USD, miles, English) or `"ca"` (CAD, km, `language` `en` or `fr`). French is Public Storage Canada's French site: unit names, hours, features and promotion text come in French.
- **Slow search pages.** In the captures search answered in 5 to 7 seconds, a facility in 2.5 to 3 and reviews in 0.5 to 1; the build measured search pages up to 155 seconds. Set a client timeout of at least 240 seconds and send one request at a time.

Public Storage publishes no public developer API. This skill reads Public Storage's public pages with one Scavio key.

See also: `extra-space-storage-api` (Extra Space Storage facilities, unit prices and reviews), `google-maps-api` (storage businesses and their Google reviews near a place). Same facility or same area only: match on address or ZIP and unit size, name the operator and date with every number.

## When to trigger

Use this skill when the user asks to:
- Price a storage unit at a Public Storage facility by size (5x5, 10x10, 10x20 ...), with the In-Store Rent, the Online price, the promotion and the move-in cost
- Find Public Storage facilities near a ZIP or postal code, a US city, a Canadian city or an address, sorted by distance or price, with climate-controlled, drive-up, 24/7, vehicle, RV, boat or business storage
- Compare unit prices across nearby Public Storage facilities, or track a facility's prices and promotions over time
- Read a Public Storage facility's office, access and rental support hours, amenities and payment methods
- Read the customer reviews a Public Storage facility shows, all of them or one star rating
- Read Public Storage Canada facilities and prices in English or French

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=public-storage-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=public-storage-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example 16 facilities priced: one search and 15 facility pages, with 34 credits left).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, reviews answered in 0.5-1 seconds, facility 2.5-3 and search 5-7; search pages were measured up to 155 seconds. Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/publicstorage/search` | Facilities near a ZIP or postal code, a city or an address: 9-19 a page, 3 sorts, facility filters, `listed` and `count`, paging by search slug; each facility with store id, address, phone, distance, today's hours, starting price, features, unit sizes and the units its card shows | 1 |
| `POST /api/v1/publicstorage/facility` | One facility by store id or link: address, phone, market area, rating and review count (US), office, access and rental support hours, amenities, images, payment methods, admin fee note, and every unit with its prices and promotion | 1 |
| `POST /api/v1/publicstorage/reviews` | Every customer review a US facility shows, newest first, optionally one star rating: rating, date, source and text (no names) | 1 |

## Market

| `market` | Site | Currency | Distance | `language` |
|---|---|---|---|---|
| `us` (default) | publicstorage.com | USD | miles | `en` only |
| `ca` | Public Storage Canada | CAD | km | `en` (default) or `fr` |

`language: "fr"` with `market: "us"` is a `400`. `/reviews` is US only. A facility `url` carries its own market and language; a `market` or `language` that contradicts it is a `400`.

## Unit and facility fields

| Field | Meaning |
|---|---|
| `units[].name`, `size_class`, `size`, `dimension` | The page's unit name ("Small 5'x5'"), its class (Small, Medium, Large; Petit, Moyen, Grand in French), the size as printed and the normalized dimension (`5x5`) |
| `units[].vehicle`, `features` | Whether it is a vehicle or parking space, and the page's feature list ("Climate Controlled", "Inside Unit, Swing Door", "Ground Floor", "Elevator access") |
| `units[].in_store_rent`, `online_price` | The In-Store Rent and the Online price, in the market's currency |
| `units[].first_month_rent`, `first_month_after_promotion`, `second_month_after_promotion` | The page's first-month rent, first month after the promotion and second month after it |
| `units[].move_in_cost`, `admin_fee`, `lock_charge` | The page's move-in cost, the one-time admin fee and the lock charge |
| `units[].promotion` | {`id`, `name`, `label`, `reward_type`, `amount`, `length_months`, `promotion_months_label`, `in_store_months_label`}: Public Storage's promotion as given ("50% off First 4 Months", Percent Off, 50, 4, "Month 1-4", "Months 5-12") |
| `units[].availability`, `units_left` | The page's own availability label and unit count where it shows one; otherwise `null` |
| `starting_from` (search) | The facility card's "Units starting from" price |
| `features` (search) | {`climate_controlled`, `drive_up`, `access_24_7`, `business_storage`, `vehicle_storage`, `rv_storage`, `boat_storage`, `manager_on_site`, `electronic_gate`, `instant_booking`} as the facility's card marks them |
| `rating`, `review_count` (facility) | The page's own rating and review count (US); `null` on Canadian pages |

- **Two price labels.** Quote `in_store_rent` as "In-Store Rent" and `online_price` as "Online price"; never present either as a final quote or a lease price.
- **Promotion months.** `promotion_months_label` ("Month 1-4") is when the promotion applies and `in_store_months_label` ("Months 5-12") when the In-Store Rent applies, as the page states them.

## Workflow

1. **Facilities near a place.** `/search` with `location` (a ZIP `"75201"`, `"Austin, TX"`, `"Toronto, ON"` with `market: "ca"`, or an address). Add `sort` and filters. Note `location.slug`, `pages` and each facility's `store_id`.
2. **More pages.** For a ZIP search with `has_more: true`, send `slug` (from `location.slug`) with `page: 2` and up.
3. **One facility.** `/facility` with `store_id` (and `market: "ca"` for Canada) or the facility `url`. Read every unit and its prices.
4. **Reviews.** `/reviews` with the US `store_id`, optionally `stars`.
5. **Report.** Each price with its label, unit size, facility, currency and `fetched_at` date; promotions as Public Storage words them; no verdict on a facility.
6. **Over time:** store each answer with its `fetched_at`; prices and promotions change as Public Storage updates them, and that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | one of | 2-120 characters: a ZIP or postal code (`75201`), a city with its state or province (`Austin, TX`; `Toronto, ON`) or a street address. Not latitude / longitude |
| `slug` | string | one of | Or the search slug an earlier answer gave (`location.slug`, e.g. `dallas-tx-75201`): needed for page 2 and later. Send `location` or `slug`, not both |
| `market` | string | `us` | `us` or `ca` (Public Storage Canada) |
| `language` | string | `en` | `en` or `fr` (`fr` with `market: "ca"` only) |
| `sort` | string | `recommended` | `recommended` (Public Storage's default order), `distance` or `price_low` |
| `page` | integer | 1 | 1-20; a page past 1 needs `slug` |
| `climate_controlled`, `drive_up`, `access_24_7`, `business_storage`, `vehicle_storage`, `rv_storage`, `boat_storage` | boolean | false | Only facilities with that feature |
| `unit_size` | string | none | Only facilities with this unit size: `5x5`, `5x10`, `5x15`, `10x10`, `10x15`, `10x20`, `10x25`, `10x30` |

### Facility (`/facility`) and reviews (`/reviews`)

| Endpoint | Parameters |
|---|---|
| `/facility` | one of `store_id` (digits, `2044`; `facilities[].store_id`) or `url` (the facility link, `facilities[].url`); `market` `us` (default) or `ca` (read from `url` when sent); `language` `en` or `fr` |
| `/reviews` | `store_id` (required, a US facility); `stars` (1-5, only that rating); `site_number` (optional, the facility's site number, `facilities[].site_number`); `market` `us` only. There is no sort |

## Examples

### Every unit and its price at one facility

```bash
curl -X POST https://api.scavio.dev/api/v1/publicstorage/facility \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "2044"}'
```

Captured `data` (2026-11-26; `office_hours`, `access_hours` and `rental_support_hours` cut to 1 of 7 days, `units` to 2 of 20, `images` and `notes` dropped):

```json
{
  "market": "us",
  "language": "en",
  "store_id": "2044",
  "site_number": "08489",
  "name": "Public Storage - Dallas",
  "country": "US",
  "currency": "USD",
  "phone": "972-763-5455",
  "address": {"street": "2420 N Haskell Ave", "city": "Dallas", "state": "TX", "postal_code": "75204", "country": "US"},
  "latitude": 32.80534,
  "longitude": -96.78863,
  "market_area": "Dallas-Ft. Worth",
  "rating": 4.7,
  "review_count": 422,
  "office_hours": [{"day": "Monday", "hours": "6:00 AM – 10:00 PM"}],
  "access_hours": [{"day": "Monday", "hours": "6:00 AM – 10:00 PM"}],
  "rental_support_hours": [{"day": "Monday", "hours": "7:00 AM – 12:00 AM"}],
  "hours_labels": ["Rental Support", "Access Hours", "Office Hours"],
  "amenities": ["Climate-Controlled Storage"],
  "payment_accepted": ["Visa", "Mastercard", "American Express", "Discover"],
  "admin_fee_note": "One Time $29 Admin Fee Applies",
  "units_count": 20,
  "units": [
    {
      "id": "V_1453935",
      "name": "Small 5'x5'",
      "size_class": "Small",
      "size": "5'x5'",
      "dimension": "5x5",
      "vehicle": false,
      "features": ["Elevator access", "Climate Controlled", "Inside Unit, Swing Door", "Near Door or Elevator"],
      "currency": "USD",
      "in_store_rent": 66,
      "online_price": 39.6,
      "first_month_rent": 66,
      "first_month_after_promotion": 39.6,
      "second_month_after_promotion": 66,
      "move_in_cost": 68.6,
      "admin_fee": 29,
      "lock_charge": 21.99,
      "promotion": {"id": "833", "name": "40% off For 4 Month", "label": "40% OFF", "reward_type": "Percent Off", "amount": 40, "length_months": 4, "promotion_months_label": "Month 1-4", "in_store_months_label": "Months 5-12"},
      "availability": null,
      "units_left": null
    },
    {
      "id": "V_1453937",
      "name": "Medium 10'x10'",
      "size_class": "Medium",
      "size": "10'x10'",
      "dimension": "10x10",
      "vehicle": false,
      "features": ["Elevator access", "Climate Controlled", "Inside Unit, Rollup Door", "Near Door or Elevator"],
      "currency": "USD",
      "in_store_rent": 135,
      "online_price": 67.5,
      "first_month_rent": 135,
      "first_month_after_promotion": 67.5,
      "second_month_after_promotion": 135,
      "move_in_cost": 96.5,
      "admin_fee": 29,
      "lock_charge": 21.99,
      "promotion": {"id": "865", "name": "50% off First 4 Months", "label": "50% off", "reward_type": "Percent Off", "amount": 50, "length_months": 4, "promotion_months_label": "Month 1-4", "in_store_months_label": "Months 5-12"},
      "availability": null,
      "units_left": null
    }
  ]
}
```

### Facilities near a ZIP, by price

```bash
curl -X POST https://api.scavio.dev/api/v1/publicstorage/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": "75201", "sort": "price_low"}'
```

Captured `data` (2026-11-26; `facilities` cut to 1 of 10, its `units` to 1 of 30, `filters` and `notes` dropped):

```json
{
  "market": "us",
  "language": "en",
  "currency": "USD",
  "distance_unit": "miles",
  "location": {"query": "75201", "slug": "dallas-tx-75201", "heading": "Find a Storage Unit Near You In 75201"},
  "sort": "price_low",
  "page": 1,
  "pages": 2,
  "has_more": true,
  "listed": 10,
  "count": 10,
  "facilities": [
    {
      "rank": 1,
      "store_id": "817",
      "site_number": "25508",
      "name": "Dallas/ Swiss Ave - Deep Ellum",
      "address": "2439 Swiss Ave",
      "city": "Dallas",
      "state": "TX",
      "postal_code": "75204",
      "country": "US",
      "phone": "972-763-5465",
      "latitude": 32.78561,
      "longitude": -96.79058,
      "distance": 0.5,
      "distance_unit": "miles",
      "today_hours": {"opens": "6:00 AM", "closes": "10:00 PM"},
      "starting_from": 32,
      "currency": "USD",
      "features": {"climate_controlled": true, "drive_up": true, "access_24_7": false, "business_storage": true, "vehicle_storage": false, "rv_storage": false, "boat_storage": false, "manager_on_site": true, "electronic_gate": true, "instant_booking": true},
      "unit_sizes": ["5x5", "5x10", "5x15", "10x10", "10x15", "10x20", "10x30"],
      "units_shown": 30,
      "units": [
        {"id": "V_106611", "name": "Small 5'x5'", "size_class": "Small", "size": "5'x5'", "dimension": "5x5", "vehicle": false, "features": ["Elevator access", "Climate Controlled", "Inside Unit, Swing Door"], "currency": "USD", "in_store_rent": 32, "online_price": 16, "first_month_rent": 32, "first_month_after_promotion": 16, "second_month_after_promotion": 32, "move_in_cost": 45, "admin_fee": 29, "lock_charge": 21.99, "promotion": {"id": "865", "name": "50% off First 4 Months", "label": "50% off", "reward_type": "Percent Off", "amount": 50, "length_months": 4, "promotion_months_label": "Month 1-4", "in_store_months_label": "Months 5-12"}, "availability": null, "units_left": null}
      ]
    }
  ]
}
```

Page 2 of this search: `{"slug": "dallas-tx-75201", "page": 2}`.

### Canada, in French, and reviews

- `/search` `{"location": "Toronto, ON", "market": "ca"}`: 18 facilities on 1 page, distances in km, prices in CAD; the first, Toronto/Jefferson Avenue (store 7771), 3.3 km away with units starting from 106 CAD.
- `/facility` `{"store_id": "7785", "market": "ca", "language": "fr"}`: Public Storage - Dorval, QC (Montreal market area), 16 units from a Petit 5'x5' at 64 CAD In-Store Rent and 32 CAD online to a Grand 10'x30' at 507 CAD, promotion "50 % de rabais sur les 4 premiers mois", hours in French, `rating` and `review_count` `null`.
- `/reviews` `{"store_id": "2044", "stars": 4}`: 12 four-star reviews, newest first, each like `{"rating": 4, "date": "December 3, 2023", "date_iso": "2023-12-03", "source": "Google", "text": "Good customer service"}`; some have `text: null`. `{"store_id": "2223", "stars": 5}` returned 819 five-star reviews in one answer.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def ps(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/publicstorage/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# Facilities near a ZIP (1 credit)
s = ps("search", {"location": "75201", "sort": "distance"})["data"]
print(s["location"]["slug"], "page", s["page"], "of", s["pages"])

# Every 10x10 at the 3 nearest facilities (1 credit each)
for f in s["facilities"][:3]:
    fac = ps("facility", {"store_id": f["store_id"]})["data"]
    for u in fac["units"]:
        if u["dimension"] == "10x10":
            promo = (u["promotion"] or {}).get("name")
            print(fac["name"], u["name"], "In-Store Rent", u["in_store_rent"], "Online price", u["online_price"], promo)

# Store each answer with fetched_at: that stored set is your record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every answer carries `notes`.

- **unit** (search `units[]`, facility `units[]`) - `id`, `name`, `size_class`, `size`, `dimension`, `vehicle`, `features`, `currency`, `in_store_rent`, `online_price`, `first_month_rent`, `first_month_after_promotion`, `second_month_after_promotion`, `move_in_cost`, `admin_fee`, `lock_charge`, `promotion` {`id`, `name`, `label`, `reward_type`, `amount`, `length_months`, `promotion_months_label`, `in_store_months_label`}, `availability`, `units_left`.
- **search** - `market`, `language`, `currency`, `distance_unit`, `location` {`query`, `slug`, `heading`}, `sort`, `filters`, `page`, `pages`, `has_more`, `listed`, `count`, `facilities[]` {`rank`, `store_id`, `site_number`, `name`, `url`, `address`, `city`, `state`, `postal_code`, `country`, `phone`, `latitude`, `longitude`, `distance`, `distance_unit`, `today_hours` {`opens`, `closes`}, `starting_from`, `currency`, `features`, `unit_sizes`, `units_shown`, `units[]`}, `notes`.
- **facility** - `market`, `language`, `store_id`, `site_number`, `name`, `url`, `country`, `currency`, `phone`, `address` {`street`, `city`, `state`, `postal_code`, `country`}, `latitude`, `longitude`, `market_area`, `rating`, `review_count`, `office_hours`, `access_hours`, `rental_support_hours` [{`day`, `hours`}], `hours_labels`, `amenities`, `images`, `payment_accepted`, `admin_fee_note`, `units_count`, `units[]`, `notes`.
- **reviews** - `store_id`, `stars`, `count`, `reviews[]` {`rating`, `date`, `date_iso`, `source`, `text`}, `notes`.

## Guardrails

- Name it "Public Storage (publicstorage.com)" on first mention, "Public Storage" after that; say "Public Storage Canada" for `market: "ca"`.
- Prices: always with the label ("In-Store Rent" or "Online price"), the unit size, the facility name or store id, the currency and the `fetched_at` date ("10'x10' at Public Storage - Dallas, store 2044: In-Store Rent 135 USD, Online price 67.50 USD with 50% off First 4 Months, fetched Nov 26, 2026"). Never present a price as a quote, a lease term or what a unit will cost later; promotions are as given and can change between visits.
- Availability: never infer how full a facility is. Quote `units_left` only where the page states it.
- Reviews: no reviewer is named or identified. Review text sometimes names facility staff; do not repeat those names. Quote review text with its rating, date and source, and say how many reviews `count` covers.
- Descriptive only: no commentary on Public Storage's business, pricing practices or policies, and no ranking of facilities from the data.
- Do not republish Public Storage photos or review text in bulk. Write publicstorage.com as plain text and cite store ids and capture dates rather than linking Public Storage pages.
- Terms: Scavio keeps no copy: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no reservation, rental or payment flow. Public Storage's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, promotions, store ids, ratings or reviews. Only return what the API returned, with the `fetched_at` time.
- Not available: occupancy or vacancy figures, price history (store answers over time), reservations, rentals or payments, reviews on Canadian facilities, Public Storage's European affiliates.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without a place ("location is required: a ZIP or postal code, a city with its state or province (Austin, TX) or a street address."), with both ("Send location or slug, not both."), or by coordinates ("location must be a ZIP or postal code, a city (Austin, TX) or an address: Public Storage does not search by latitude / longitude."); a page past 1 without a slug ("A page past 1 needs the search slug: send slug (location.slug from page 1) with page. Searches by a city or a Canadian place list every facility on page 1."); a bad slug ("slug must be a Public Storage search slug as an earlier search answer gives it (location.slug, e.g. dallas-tx-75201)."); French on the US site ("language fr is Public Storage Canada's French site: send market ca (the US site is English only)."); a `market` or `language` that contradicts the link; `/facility` without a store id ("store_id (or url) is required.") or with a link that is not a facility ("url must be a Public Storage facility link ..."); a `store_id` that does not match the link; `/reviews` on Canada ("reviews covers US facilities only: Public Storage Canada's facility pages show no reviews.") or with a sort ("Public Storage lists reviews newest first only: there is no sort."); a `sort` or `unit_size` outside its list; `stars` outside 1-5.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Public Storage has no facilities for this place. Send a ZIP or postal code, a city with its state or province (Austin, TX) or a street address; Canadian places need market ca.", "Public Storage has no facility <store_id> on its US site (facilities[].store_id from search; a Canadian facility needs market ca).", "Public Storage Canada has no facility <store_id> (facilities[].store_id from a market ca search).", "No reviews for this store id.". Take store ids and slugs from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=public-storage-api).
- `502` means Public Storage data was temporarily unavailable ("Public Storage is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Public Storage is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.98.0
npm install scavio@0.99.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.publicstorage.search({ location: "75201", sort: "price_low" });
const { data: facility } = await scavio.publicstorage.facility({ store_id: "2044" });
const { data: dorval } = await scavio.publicstorage.facility({ store_id: "7785", market: "ca", language: "fr" });
const { data: reviews } = await scavio.publicstorage.reviews({ store_id: "2044", stars: 4 });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.publicstorage.search(...)`, `facility` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 3 endpoints as tools: `search_publicstorage`, `get_publicstorage_facility` and `get_publicstorage_reviews`. Public Storage is opt-in: add `publicstorage` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.98.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,publicstorage"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/publicstorage-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=public-storage-api), [facility](https://scavio.dev/docs/publicstorage-facility?utm_source=agent-skills&utm_medium=skill&utm_campaign=public-storage-api), [reviews](https://scavio.dev/docs/publicstorage-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=public-storage-api). Overview: [Public Storage API](https://scavio.dev/publicstorage-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=public-storage-api).
