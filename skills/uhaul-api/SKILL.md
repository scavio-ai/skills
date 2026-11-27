---
name: uhaul-api
description: U-Haul API for U-Haul (uhaul.com, the US and Canada truck rental and self-storage company) - U-Haul's own truck rental rates for a move, as its public quote form shows them for a pickup place, an optional drop-off and a date (on 2026-11-27 a one-way Dallas, TX to Austin, TX move on 2026-12-11 read $212 for the 10' Truck, $223 for the 15', $280 for the 20' and $335 for the 26', each including up to 2 days and 229 miles, with the 8' Pickup Truck and 9' Cargo Van "Not available for your move."; an in-town Chicago, IL quote read $19.95 to $49.95 plus $1.59/mile; Toronto, ON to Ottawa, ON read CAD 646 for the 10' Truck, 651 with fees, including 531 kilometers) with every truck's availability, U-Haul's Limited Availability note, inside dimensions and specs, the truck + moving labor estimate and the U-Box starting price; U-Haul locations near a city, ZIP or postal code for truck rentals, trailer rentals, moving supplies or self-storage, 6 per page, with U-Haul's location type (company center or dealer), address, public business phone, rating, review count, distance, hours, holiday hours, services and flags; one location with hours, payment methods and, for Canadian locations, the full CAD rate card (weekday and weekend day and per-km rates, daily, weekly and monthly plans with kilometers included); self-storage facilities near a place, up to 18, sorted by distance, starting rate or rating and filtered by climate control, indoor, drive-up, portable, Rent Now and RV, boat or vehicle storage; one storage facility with every unit's size, floor and climate attributes, monthly rate, Rent Now or reserve-only flag, vacant unit count and reserve window, its promotions and office and access hours (U-Haul Moving & Storage at Greenville Ave, Dallas listed 43 units, 139 vacant, a 5' x 5' indoor unit at $64.95 a month); U-Haul's own customer reviews of a location, filtered by service (trucks, storage, U-Box) and stars, sorted and paged, without reviewer names; place suggestions for pickup, drop-off and search; moving supplies prices in USD or CAD by category or product, with U-Haul's bundle prices. US and Canada, English, Spanish (es.uhaul.com) and French (fr.uhaul.com). 8 endpoints, 1 credit per call. Quotes are U-Haul's rates page only - no pickup location, nothing reserved; no trailer, towing or U-Box quotes, no price history.
version: 1.0.0
tags: u-haul, uhaul, uhaul-com, u-haul-api, uhaul-api, u-haul-quote, uhaul-quote, u-haul-truck-rental, uhaul-truck-rental, u-haul-rates, uhaul-rates, u-haul-prices, uhaul-prices, u-haul-one-way, uhaul-one-way, u-haul-locations, uhaul-locations, u-haul-dealers, u-haul-storage, uhaul-storage, u-haul-self-storage, u-haul-storage-prices, u-haul-reviews, uhaul-reviews, u-haul-moving-supplies, uhaul-moving-boxes, u-haul-canada, truck-rental, truck-rental-quote, moving-truck-rental, one-way-truck-rental, in-town-truck-rental, moving-costs, moving-truck-prices, cargo-van-rental, pickup-truck-rental, trailer-rental, self-storage, self-storage-prices, storage-unit-prices, storage-units, climate-controlled-storage, rv-storage, moving-supplies, moving-boxes, location-search, customer-reviews, price-monitoring, market-research, real-estate, usd, cad, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/uhaul-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api
---

# U-Haul API - Truck Rental Quotes, Locations, Self-Storage Prices, Reviews

Read U-Haul (uhaul.com, the US and Canada truck rental and self-storage company): U-Haul's own truck rental rates for a move (one-way or in-town), U-Haul locations near a place for truck rentals, trailer rentals, moving supplies or self-storage, one location with its hours and (in Canada) its rate card, self-storage facilities near a place, one storage facility with every unit and its monthly rate, U-Haul's own customer reviews of a location, place suggestions, and moving supplies prices. US and Canada (USD or CAD, miles or kilometers), in English, Spanish or French. Every endpoint returns structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages U-Haul shows to any visitor and returns them as JSON. It uses no U-Haul account, opens no reservation and rents nothing: a truck quote stops at U-Haul's rates page.

**The job this skill is for: what a moving truck costs for one move, and what self-storage costs near a place.** On 2026-11-27 `/truck-quote` for Dallas, TX to Austin, TX on 2026-12-11 answered 6 trucks, 4 available: the 10' Truck $212, the 15' Truck $223, the 20' Truck $280 and the 26' Truck $335, each U-Haul's one-way total including "up to 2 days of use and 229 miles", the 8' Pickup Truck and 9' Cargo Van "Not available for your move.", a 26' Truck + 4 hours / 2 Laborers estimate from $568.96 and U-Box from $893.95. The same date in town in Chicago, IL read $19.95 (pickup truck, cargo van, 10' truck), $29.95, $39.95 and $49.95 (26') "plus $1.59/mile". Toronto, ON M5V 2T6 to Ottawa, ON K1P 1J1 on 2026-12-10 read CAD 646 for the 10' Truck and 651 with fees, including 531 kilometers. On the storage side, `/storage-facility` for U-Haul Moving & Storage at Greenville Ave in Dallas (`741065`) listed 43 units with 139 vacant, from a 3' x 3' x 3' locker at $19.95 a month and a 5' x 5' indoor unit at $64.95 to a 10' x 25' drive-up unit at $324.95, with the 1-Year Price Lock and No Deposit Or Admin Fee promotions. Pair it with `extra-space-storage-api` and `public-storage-api` for storage prices at the other operators near the same place.

Eight limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit, the truck quote included. `credits_used` in the response is the truth. A not-found (`404`) is charged (an unknown id, a place U-Haul cannot find, a move U-Haul will not quote); a refused input (`400`) and an upstream failure (`502`, `503`) are not. One `404` is not charged: a place U-Haul read as another one with the same name (see Failure handling).
- **A quote is U-Haul's rates page, never a reservation.** Nothing is reserved, held or rented. U-Haul chooses the pickup location in its reservation step, after a truck is picked; Scavio stops at the rates page, so **no pickup location is returned**. Say the rate is U-Haul's quote for that route and date at the moment of the call.
- **One-way and in-town rates mean different things.** One-way (`rate_kind` `one_way_total`) is U-Haul's total for the truck on that route and date, including the days and distance in `includes`. In-town (`rate_kind` `in_town_base`) is U-Haul's base rate plus `per_distance_rate` per mile or km (`per_distance_text`, "plus $1.59/mile"). Never add mileage to a one-way total, and never present an in-town base rate as the cost of the move.
- **Canada has two prices.** Canadian quotes carry `rate` (without fees) and `rate_with_fees`, both as U-Haul shows them, in CAD. `allowed_miles` is U-Haul's own figure in miles even when the page states kilometers (`includes.distance`, `distance_unit` `km`): quote `includes` for Canada.
- **Trucks only.** Trailer, towing and U-Box quotes are not covered (`ubox_from` is U-Haul's U-Box starting price as the rates page shows it, not a quote). `/locations` with `service` `trailer_rentals` lists where trailers are rented, without prices.
- **Storage rates are U-Haul's one monthly rate per unit.** U-Haul shows no separate web and in-store rate. `vacant_units` is the vacant unit count U-Haul's page carries for that unit; `rent_now` and `reserve_only` are U-Haul's own offer flags. Promotions are U-Haul's text and can change between visits.
- **Location "from" prices are not quotes.** US dealer pages list "from" prices (`listed_from_prices`); they do not match U-Haul's live rates. Use `/truck-quote` for a move's price. Canadian locations carry a real `rate_card` in CAD.
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

U-Haul publishes no public API for truck rates, locations, storage units or reviews, and no affiliate data feed was found. Rates, locations and storage units are shown on uhaul.com for the place and date a visitor enters, and this skill reads those public pages with one Scavio key.

U-Haul Holding Company (NYSE: UHAL, UHAL.B) describes its network as "the most extensive network of rental locations in the U.S. and Canada" and itself as the third largest self-storage operator (investors.uhaul.com); uhaul.com states over 25,000 locations. Quote these with their source, never from the samples.

See also: self-storage unit prices at Extra Space use `extra-space-storage-api`; at Public Storage `public-storage-api`; a business's Google rating and reviews `google-maps-api`; homes at the destination `zillow-property-data`.

## When to trigger

Use this skill when the user asks to:
- Price a U-Haul truck for a one-way move between two cities, ZIPs or postal codes on a date, every truck size side by side with what the rate includes
- Price an in-town U-Haul rental (base rate plus the per-mile or per-km rate) for a city on a date
- Compare U-Haul truck rates for the same route across dates, or a US and a Canadian move, with the date of each quote
- Find U-Haul locations near a place for truck rentals, trailer rentals, moving supplies or self-storage, with type (company center or dealer), hours, holiday hours, rating and services
- Read one U-Haul location: address, public business phone, hours, payment methods, rating, and the CAD rate card of a Canadian location
- List U-Haul self-storage facilities near a place sorted by starting rate, distance or rating, or only those with climate control, drive-up, indoor, Rent Now or RV, boat or vehicle storage
- Read every unit of one U-Haul storage facility with size, attributes, monthly rate, vacant count and promotions
- Read U-Haul's customer reviews of a location, the 1-star truck reviews or the storage reviews only
- Price U-Haul moving boxes and packing supplies in USD or CAD, with bundle prices
- Turn a partial city, ZIP or postal code into the place U-Haul accepts

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Calls usually take 2-30 seconds (in the captures: a truck quote 21-28, locations, storage search and suggestions 4-17, a storage facility or reviews up to about 20). A location page has taken up to 70 seconds. Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/uhaul/truck-quote` | U-Haul's truck rates for a pickup place, an optional drop-off (empty = in-town) and a date: every truck with availability, rate, rate with fees (Canada), rate kind, per-mile or per-km rate, inside dimensions and specs; what a one-way rate includes; the truck + labor estimate; the U-Box starting price | 1 |
| `POST /api/v1/uhaul/locations` | U-Haul locations near a city, ZIP or postal code for truck rentals, trailer rentals, moving supplies or self-storage: id, name, location type, address, phone, rating, review count, distance, hours, holiday hours, services, flags; 6 per page | 1 |
| `POST /api/v1/uhaul/location` | One location by id or link: address, coordinates, phone, hours, payment methods, rating, review count, the Canadian CAD rate card, US listed "from" prices | 1 |
| `POST /api/v1/uhaul/storage-search` | Self-storage facilities near a place, up to 18: id, name, affiliate flag, address, distance, starting rate, rating, review count, price lock, features, today's office and access hours; sorted and filtered by features | 1 |
| `POST /api/v1/uhaul/storage-facility` | One storage facility by id or link: every unit (section, size class, dimensions, use, attributes, monthly rate, Rent Now or reserve-only, vacant units, reserve window), promotions, office, access and holiday hours, features | 1 |
| `POST /api/v1/uhaul/reviews` | U-Haul's own customer reviews of a location or facility, filtered by service and stars, sorted and paged; no reviewer names | 1 |
| `POST /api/v1/uhaul/suggestions` | U-Haul's place suggestions for the start of a city, ZIP or postal code (US and Canada) | 1 |
| `POST /api/v1/uhaul/supplies` | Moving supplies prices in USD or CAD: a category's products with price and As low as flag, or one product with bundle price, availability, rating, dimensions and sizes | 1 |

Market: US or Canada follows the place (`country`, `currency` and `distance_unit` in the answer). `language` (`en`, `es`, `fr`) picks www.uhaul.com, es.uhaul.com or fr.uhaul.com on the quote, locations, location, storage search and storage facility; supplies are English only and take `country` (`us` or `ca`) instead.

## Truck rates: one-way totals, in-town base rates and Canadian fees

Every truck in `trucks[]` carries:

| Field | Meaning |
|---|---|
| `model_code`, `name`, `moving_type` | U-Haul's truck code (`TM`, `DC`, `TT`, `JH`, `BP`, `BE`), name ("10' Truck") and its move size ("Studio to 1 Bedroom Apt.") |
| `available`, `availability_text`, `inventory_note` | Whether U-Haul offers it for this move; U-Haul's text when not ("Not available for your move."); its own note ("Limited Availability") |
| `rate`, `rate_with_fees` | U-Haul's rate; the rate with fees, given on Canadian quotes only; `null` on a truck that is not available |
| `rate_kind` | `one_way_total` (the whole one-way rate, see `includes`) or `in_town_base` (base rate before mileage) |
| `per_distance_rate`, `per_distance_unit`, `per_distance_text` | In-town only: the mileage rate (1.59, `mile`, "plus $1.59/mile") |
| `inside_dimensions`, `specs` | Inside dimensions, door opening, deck height and ramp as U-Haul lists them |

Around the trucks: `move_type` (`one_way` or `in_town`), `includes` {`days`, `distance`, `distance_unit`, `text`} (one-way), `allowed_miles`, `ubox_from`, `count`, `available_count`, and `truck_with_labor` {`model_code`, `truck_rate`, `truck_rate_with_fees`, `labor_from`, `labor_text`, `estimated_total_from`} (U-Haul's truck + moving labor starting prices as given).

- Quote "$280 for U-Haul's 20' Truck, Dallas, TX to Austin, TX on 2026-12-11, including up to 2 days and 229 miles (U-Haul quote fetched 2026-11-27)", with the route, the move date and the fetch date.
- In-town: "$39.95 plus $1.59/mile" - never a total, since the miles driven are unknown.
- Canada: quote both `rate` and `rate_with_fees` as U-Haul shows them, in CAD, and the kilometers from `includes`.
- Report U-Haul's rates and the arithmetic only. Never call a rate a good or bad deal, never predict how rates move with the date, and never present a quote as a booked price.

## Workflow

1. **Get the place right.** `/suggestions` with `term` (`dall`, `M5V`, `8500`) returns U-Haul's own places and postal codes; `value` goes straight into `pickup`, `dropoff` or `near`. In Canada (and for any city name shared across states or provinces) send the postal code too (`Toronto, ON M5V 2T6`).
2. **Quote a move.** `/truck-quote` with `pickup`, `date` (YYYY-MM-DD, today to 330 days ahead) and `dropoff` for one-way (leave it out for in-town). Read `trucks[]` for every size and `includes` for what a one-way rate covers. Check `pickup.state` and `dropoff.state` against what was asked.
3. **Compare dates.** One call per date; store each answer with its `fetched_at`.
4. **Where to rent.** `/locations` with `near` and `service` (`truck_rentals` default, `trailer_rentals`, `moving_supplies`, `self_storage`), `page` while `has_more`. Each `location_id` is the input of `/location` and `/reviews`.
5. **One location.** `/location` with `location_id` (or its `url`) for hours and payment methods; a Canadian location adds its CAD `rate_card`.
6. **Storage near a place.** `/storage-search` with `near`, `sort` (`distance`, `price`, `rating`) and `features`. Each `facility_id` is the input of `/storage-facility` and `/reviews`.
7. **Every unit of one facility.** `/storage-facility` with `facility_id`: match the user's size in `units[]` (`dimensions`, `width_ft`, `length_ft`, `section`, `attributes`) and quote its `monthly_rate`.
8. **Reviews.** `/reviews` with `location_id` (or a `facility_id`), `service` (`trucks`, `storage`, `ubox`), `stars`, `sort`, `page`, `page_size`.
9. **Boxes and packing supplies.** `/supplies` with `category` (`Boxes`, `Packing-Supplies`, `Tape`) or a product `url`, and `country` `ca` for CAD.
10. **Watching rates:** there is no history. Poll the same route, date and facilities on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Truck quote (`/truck-quote`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pickup` | string | required | A city with its state or province (`Dallas, TX`, `Toronto, ON`), a US ZIP or a Canadian postal code, 2-80 chars |
| `dropoff` | string | none | Drop-off for a one-way move; leave it out for an in-town quote. Must differ from `pickup` |
| `date` | string | required | Pickup day, `YYYY-MM-DD`: today or later, up to 330 days ahead (U-Haul quotes up to 11 months out) |
| `language` | string | `en` | `en` (www.uhaul.com), `es` (es.uhaul.com) or `fr` (fr.uhaul.com); the market (US or Canada) follows the place |

### Locations (`/locations`) and storage search (`/storage-search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `near` | string | required | A city with its state or province, a ZIP or a postal code. Not a latitude / longitude |
| `service` | string | `truck_rentals` | Locations: `truck_rentals`, `trailer_rentals`, `moving_supplies` or `self_storage` |
| `page` | integer | 1 | Locations: 1-50; 6 per page where U-Haul pages (`layout` `paged`), every location on page 1 where it does not (`layout` `single`) |
| `sort` | string | `distance` | Storage search: `distance`, `price` (starting rate, low to high) or `rating` (high to low) |
| `features` | array | none | Storage search: up to 6 of `climate_control`, `indoor`, `drive_up`, `portable`, `rent_now_online`, `vehicle` (RV/Boat/Vehicle Storage); a facility must have every one |
| `language` | string | `en` | `en`, `es` or `fr` |

### Location (`/location`), storage facility (`/storage-facility`), reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location_id` | string or integer | one of | Location and reviews: a U-Haul location id, 5-7 digits (`741028`: `locations[].location_id`; a `facility_id` also works on reviews) |
| `facility_id` | string or integer | one of | Storage facility: a U-Haul storage facility id (`741065`: `facilities[].facility_id`) |
| `url` | string | one of | The location or facility link from an earlier answer (`locations[].url`, `facilities[].url`) instead of the id |
| `language` | string | `en` | Location and storage facility: `en`, `es` or `fr` (must match the link's site when a `url` is sent) |
| `service` | string | `all` | Reviews: `all`, `trucks`, `storage` or `ubox` |
| `stars` | integer | none | Reviews: only reviews with this many stars, 1-5 |
| `sort` | string | `newest` | Reviews: `newest`, `highest` or `lowest` |
| `page`, `page_size` | integer | 1, 20 | Reviews: page 1-200, 1-100 reviews per page |

### Suggestions (`/suggestions`) and supplies (`/supplies`)

`/suggestions` takes `term` (2-60 chars, the start of a city, a ZIP or a postal code). `/supplies` takes `category` (a moving supplies category as U-Haul's link writes it: `Boxes`, `Packing-Supplies`, `Tape`, `Boxes/Standard-Sized-Moving-Boxes`) or `url` (a www.uhaul.com moving supplies category or product link, `products[].url`), not both, and `country` (`us` default, USD, or `ca`, CAD).

## Examples

### One-way truck quote

```bash
curl -X POST https://api.scavio.dev/api/v1/uhaul/truck-quote \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"pickup": "Dallas, TX", "dropoff": "Austin, TX", "date": "2026-12-11"}'
```

Captured `data` (2026-11-27; 3 of 6 trucks shown, `specs` cut to 1, `notes` cut to 2):

```json
{
  "language": "en",
  "country": "us",
  "currency": "USD",
  "distance_unit": "miles",
  "move_type": "one_way",
  "pickup": { "query": "Dallas, TX", "city": "Dallas", "state": "TX" },
  "dropoff": { "query": "Austin, TX", "city": "Austin", "state": "TX" },
  "date": "2026-12-11",
  "includes": { "days": 2, "distance": 229, "distance_unit": "miles", "text": "Truck Rate includes up to 2 days of use and 229 miles." },
  "allowed_miles": 229,
  "ubox_from": 893.95,
  "count": 6,
  "available_count": 4,
  "trucks": [
    {
      "model_code": "TM",
      "name": "10' Truck",
      "moving_type": "Studio to 1 Bedroom Apt.",
      "available": true,
      "availability_text": null,
      "inventory_note": null,
      "rate": 212,
      "rate_with_fees": null,
      "rate_kind": "one_way_total",
      "per_distance_rate": null,
      "per_distance_unit": null,
      "per_distance_text": null,
      "inside_dimensions": "9'11\" x 6'4\" x 6'2\" (LxWxH)",
      "specs": ["Inside dimensions: 9'11\" x 6'4\" x 6'2\" (LxWxH)"]
    },
    {
      "model_code": "JH",
      "name": "26' Truck",
      "moving_type": "3 Bedroom Home to 4 Bedroom Home",
      "available": true,
      "availability_text": null,
      "inventory_note": null,
      "rate": 335,
      "rate_with_fees": null,
      "rate_kind": "one_way_total",
      "per_distance_rate": null,
      "per_distance_unit": null,
      "per_distance_text": null,
      "inside_dimensions": "26'2\" x 8'2\" x 8'3\" (LxWxH)",
      "specs": ["Inside dimensions: 26'2\" x 8'2\" x 8'3\" (LxWxH)"]
    },
    {
      "model_code": "BP",
      "name": "8' Pickup Truck",
      "moving_type": "Home improvement / Small loads",
      "available": false,
      "availability_text": "Not available for your move.",
      "inventory_note": "Limited Availability",
      "rate": null,
      "rate_with_fees": null,
      "rate_kind": null,
      "per_distance_rate": null,
      "per_distance_unit": null,
      "per_distance_text": null,
      "inside_dimensions": "7'10\" x 5'2\" x 1'9\" (LxWxH)",
      "specs": ["Inside dimensions: 7'10\" x 5'2\" x 1'9\" (LxWxH)"]
    }
  ],
  "truck_with_labor": {
    "model_code": "JH",
    "truck_rate": 335,
    "truck_rate_with_fees": null,
    "labor_from": 233.96,
    "labor_text": "4 hours / 2 Laborers",
    "estimated_total_from": 568.96
  },
  "notes": [
    "One-way rates are U-Haul's total for the truck on this route and date, including the days and distance in includes (rate_kind one_way_total).",
    "The pickup location is chosen in U-Haul's reservation step, after a truck is selected; Scavio stops at the rates page, so no pickup location is returned and nothing is reserved."
  ]
}
```

The other trucks were the 15' Truck at $223, the 20' Truck at $280 and the 9' Cargo Van, not available. `{"pickup": "Chicago, IL", "date": "2026-12-11"}` (in-town) answered all 6 available, `rate_kind` `in_town_base`: $19.95 for the 8' Pickup Truck, 9' Cargo Van and 10' Truck, $29.95, $39.95 and $49.95 for the 15', 20' and 26', each "plus $1.59/mile", and a 26' Truck + 3 hours / 2 Laborers estimate from $238.94. `{"pickup": "Toronto, ON M5V 2T6", "dropoff": "Ottawa, ON K1P 1J1", "date": "2026-12-10"}` answered `currency` CAD, `includes` 2 days and 531 km (`allowed_miles` 330), 10' Truck `rate` 646 and `rate_with_fees` 651, 26' Truck 1023 and 1028. `{"pickup": "85004", "dropoff": "Denver, CO", "date": "2026-12-10", "language": "es"}` answered Phoenix, AZ to Denver, CO with up to 5 days and 1022 miles, 10' Truck $524, and U-Haul's Spanish text ("No disponible para tu mudanza.").

### Every unit of one storage facility

```bash
curl -X POST https://api.scavio.dev/api/v1/uhaul/storage-facility \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"facility_id": "741065"}'
```

Captured `data` (2026-11-27; 2 of 43 units shown; `features`, `amenities`, `office_hours`, `access_hours`, `special_hours` and `notes` dropped):

```json
{
  "language": "en",
  "country": "us",
  "currency": "USD",
  "facility_id": "741065",
  "name": "U-Haul Moving & Storage at Greenville Ave",
  "url": "https://www.uhaul.com/Locations/Self-Storage-near-Dallas-TX-75231/741065/",
  "affiliate": false,
  "address": { "street": "7043 Greenville Ave", "city": "Dallas", "state": "TX", "postal_code": "75231", "country": "US" },
  "latitude": 32.87494514,
  "longitude": -96.76252431,
  "phone": "+12146917311",
  "rating": 5,
  "review_count": 2544,
  "sections": ["Indoor Storage", "Drive Up Storage", "Storage Lockers"],
  "promotions": [
    { "name": "1-Year Price Lock", "text": "Monthly price remains the same for your first 12 months." },
    { "name": "No Deposit Or Admin Fee", "text": "No Deposit Required and $0.00 Admin Fee" }
  ],
  "units_count": 43,
  "vacant_units_total": 139,
  "units": [
    {
      "unit_id": "4adcaa0",
      "section": "Indoor Storage",
      "size_class": "Small",
      "dimensions": "5' x 5' x 10'",
      "width_ft": 5,
      "length_ft": 5,
      "use": "Miscellaneous Storage",
      "attributes": ["Interior", "3rd Floor", "Street Level", "Elevator", "No Climate"],
      "monthly_rate": 64.95,
      "rent_now": true,
      "reserve_only": false,
      "vacant_units": 9,
      "reserve_from": "2026-11-26",
      "reserve_until": "2027-05-25",
      "free_lock_with_rent_now": true
    },
    {
      "unit_id": "fee8235",
      "section": "Indoor Storage",
      "size_class": "Small",
      "dimensions": "5' x 5' x 10'",
      "width_ft": 5,
      "length_ft": 5,
      "use": "Miscellaneous Storage",
      "attributes": ["Interior", "1st Floor", "Street Level", "No Climate"],
      "monthly_rate": 69.95,
      "rent_now": true,
      "reserve_only": false,
      "vacant_units": 7,
      "reserve_from": "2026-11-26",
      "reserve_until": "2027-05-25",
      "free_lock_with_rent_now": true
    }
  ]
}
```

The same size can carry different rates by floor and attributes (5' x 5' x 10' indoor at $64.95, $69.95 and $74.95). Units ran from a 3' x 3' x 3' locker at $19.95 to 10' x 10' x 10' at $169.95-$209.95 and a 10' x 25' x 10' drive-up unit at $324.95. A third promotion read "Ask about our 1 month free self-storage offer with any truck or trailer reservation!". `{"facility_id": "848027", "language": "fr"}` (Toronto) answered CAD rates with U-Haul's French labels ("Entreposage intérieur", a 5 pi x 5 pi x 8 pi unit at 119.95, `reserve_only` true).

### Locations, location, storage search, reviews, suggestions and supplies

- `/locations` `{"near": "75201"}`: "Moving Truck Rentals Near Dallas, TX 75201", `layout` `paged`, 6 per page, `has_more` true; the first five were U-Haul Neighborhood Dealers 1.0-2.2 miles away, the sixth U-Haul Moving & Storage of Lower Greenville (`741028`, `location_type` null = a U-Haul company location, 2.4 miles, 4 stars from 10,582 reviews, special hours 2026-11-26 7:00 am - 3:00 pm and 2026-12-25 Closed, services from Moving Trucks to Plastic Moving Boxes, flags "Free towing inspection" and "24 hour customer return"). `{"near": "Phoenix, AZ 85004", "service": "trailer_rentals"}` read "Trailer & Towing Rentals Near Phoenix, AZ 85004". `{"near": "Toronto, ON", "page": 2}` answered 6 more with `has_more` false. Distances in Canada come in miles as U-Haul gives them (`distance_text`).
- `/location` `{"location_id": "741028"}`: 1616 Greenville Ave, Dallas, TX 75206, phone +12148235830, hours "Mon - Thur: 7 am - 7 pm" to "Sun: 9 am - 5 pm", payment Cash and Credit Card, 4 stars from 10,582 reviews, `rate_card` empty. `{"location_id": "848027"}` (U-Haul Moving & Storage of Stockyards District, Toronto, ON) answered `currency` CAD and a `rate_card` per truck: the Pickup Truck from 19.95, weekday 0.99 and weekend 1.09 per km, plans daily 89 (150 km), weekly 419 (999 km) and monthly 1676 (4000 km), additional $0.30/km, valid until 2026-12-31.
- `/storage-search` `{"near": "Phoenix, AZ 85004", "sort": "price"}`: 18 listed, Star Mini Storage (a U-Haul Self-Storage Affiliate, 7.9 miles) first at $50 Starting at, then U-Haul Moving & Storage at I-17 and McDowell at $64.95 (5 stars, 3,693 reviews, `price_lock` true); two facilities without a starting rate sorted last. `{"near": "Phoenix, AZ", "sort": "rating", "features": ["climate_control", "rent_now_online"]}` kept 12 of 18. `{"near": "Toronto, ON", "language": "fr"}` listed 12 with CAD starting rates (94.95 at Stockyards District).
- `/reviews` `{"location_id": "741028", "page_size": 10}`: `overall_rating` 4, `counts` {all 178, trucks 100, storage 78}, 18 pages, newest first, each review with `rating`, `date`, `review_type` (U-Haul's label: FirstImpressions, OverallExperience, Unknown), `service` and `text` ("Good people and easy to work with.", 5 stars, 2026-11-25; "Could use an elevator.", 3 stars, storage). `{"location_id": "848027", "service": "storage"}` read 720 storage reviews of 820.
- `/suggestions` `{"term": "dall"}`: 15 places, Dallas, TX first, then Dallas, GA, Dallas, NC, ...; `{"term": "M5V"}`: M5V (Toronto, ON) and postal codes M5V0A1, M5V0A2, ... (`kind` `postal_code`); `{"term": "8500"}`: 85001 (Phoenix, AZ), 85002, ...
- `/supplies` `{"category": "Boxes"}`: Moving Boxes, 47 products, the Medium Moving Box (`2793`) "As low as: $1.99" (`as_low_as` true: U-Haul's per-item bundle price), Large $2.78, Small $1.49, Extra-Large $3.78; `{"category": "Boxes", "country": "ca"}`: the same boxes at CAD 3.21, 4.51, 2.21 and 5.61. The product link of `2793` with `country` `ca` read `price` 3.46 CAD single, `bundle` "Bundle of 20: $64.20 ($3.21 each)", `availability` InStock, 4.5 stars from 6,102 reviews, 18 x 18 1/8 x 16 inches, and sizes Small to X-Large with their product ids.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def uhaul(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/uhaul/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. One-way truck rates for a route and date (1 credit). Not a reservation.
q = uhaul("truck-quote", {"pickup": "Dallas, TX", "dropoff": "Austin, TX", "date": "2026-12-11"})["data"]
print(q["includes"]["text"])
for t in q["trucks"]:
    print(t["name"], t["available"], t["rate"], t["rate_kind"], t["availability_text"])

# 2. Storage near the destination, lowest starting rate first (1 credit)
s = uhaul("storage-search", {"near": "Austin, TX", "sort": "price", "features": ["climate_control"]})["data"]
for f in s["facilities"][:5]:
    print(f["facility_id"], f["name"], f["starting_rate"], f["distance_text"], f["rating"])

# 3. Every unit of the first facility (1 credit)
fac = uhaul("storage-facility", {"facility_id": s["facilities"][0]["facility_id"]})["data"]
for u in fac["units"]:
    print(u["dimensions"], u["section"], u["monthly_rate"], u["vacant_units"], u["rent_now"])

# Rates change between calls. Store each answer with fetched_at and run this
# on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `notes`.

- **truck-quote** - `language`, `country`, `currency`, `distance_unit`, `move_type`, `pickup` {`query`, `city`, `state`}, `dropoff` (same, or null in town), `date`, `includes` {`days`, `distance`, `distance_unit`, `text`} (one-way, else null), `allowed_miles`, `ubox_from`, `count`, `available_count`, `trucks[]` {`model_code`, `name`, `moving_type`, `available`, `availability_text`, `inventory_note`, `rate`, `rate_with_fees`, `rate_kind`, `per_distance_rate`, `per_distance_unit`, `per_distance_text`, `inside_dimensions`, `specs`}, `truck_with_labor` {`model_code`, `truck_rate`, `truck_rate_with_fees`, `labor_from`, `labor_text`, `estimated_total_from`}.
- **locations** - `language`, `near`, `service`, `country`, `distance_unit`, `heading`, `layout` (`paged` or `single`), `page`, `per_page`, `has_more`, `count`, `locations[]` {`rank`, `location_id`, `name`, `location_type`, `url`, `address` {`street`, `city`, `state`, `postal_code`, `country`}, `phone` (paged layout), `rating`, `review_count`, `distance`, `distance_text`, `open_today`, `hours[]` {`days`, `hours`}, `special_hours[]` {`date`, `hours`}, `services`, `flags`, `latitude`, `longitude`}.
- **location** - `language`, `country`, `currency`, `location_id`, `name`, `url`, `address`, `latitude`, `longitude`, `phone`, `hours`, `payment_accepted`, `rating`, `review_count`, `image`, `rate_card[]` {`name`, `model_code`, `description`, `from_price`, `currency`, `price_valid_until`, `weekday_day_rate`, `weekday_distance_rate`, `weekend_day_rate`, `weekend_distance_rate`, `distance_unit`, `plans[]` {`period`, `rate`, `distance_included`, `additional_distance_rate`, `additional_distance_text`}, `properties[]` {`name`, `value`}} (Canada), `listed_from_prices` (US dealers).
- **storage-search** - `language`, `near`, `country`, `currency`, `distance_unit`, `sort`, `features`, `listed`, `count`, `facilities[]` {`rank`, `facility_id`, `name`, `url`, `affiliate`, `address`, `distance`, `distance_text`, `starting_rate`, `rating`, `review_count`, `price_lock`, `features`, `feature_keys`, `office_hours_today`, `access_hours_today`, `special_hours`}.
- **storage-facility** - `language`, `country`, `currency`, `facility_id`, `name`, `url`, `affiliate`, `address`, `latitude`, `longitude`, `phone`, `rating`, `review_count`, `units_count`, `vacant_units_total`, `units[]` {`unit_id`, `section`, `size_class`, `dimensions`, `width_ft`, `length_ft`, `use`, `attributes`, `monthly_rate`, `rent_now`, `reserve_only`, `vacant_units`, `reserve_from`, `reserve_until`, `free_lock_with_rent_now`}, `sections`, `promotions[]` {`name`, `text`}, `office_hours`, `access_hours`, `special_hours`, `features`, `amenities`.
- **reviews** - `location_id`, `location_name`, `overall_rating`, `counts` {`all`, `trucks`, `storage`, `ubox`}, `service`, `stars`, `sort`, `total`, `page`, `page_size`, `pages`, `has_more`, `count`, `reviews[]` {`rating`, `date`, `review_type`, `service`, `text`}.
- **suggestions** - `term`, `count`, `suggestions[]` {`label`, `value`, `kind` (`place` or `postal_code`)}.
- **supplies** - category: `country`, `currency`, `kind` `category`, `category`, `name`, `count`, `products[]` {`product_id`, `name`, `url`, `price`, `price_text`, `as_low_as`, `pickup_only`, `free_in_store_pickup`, `next_day_delivery`}; product: `country`, `currency`, `kind` `product`, `product_id`, `name`, `url`, `category`, `description`, `brand`, `image`, `sku`, `price`, `as_low_as_price`, `bundle` {`quantity`, `price`, `unit_price`, `text`}, `availability`, `rating`, `review_count`, `dimensions`, `sizes[]` {`label`, `product_id`, `url`, `selected`}.

## Guardrails

- Name it "U-Haul (uhaul.com, the US and Canada truck rental and self-storage company)" on first mention. No U-Haul account is used.
- Quotes: report U-Haul's rate with the truck, the route, the move date, what `includes` says and the `fetched_at` date. Say plainly that it is U-Haul's quote at the moment of the call, that nothing is reserved and that the pickup location is chosen by U-Haul in its reservation step (none is returned). Never promise a truck will be there or that the rate will hold.
- In-town rates are a base rate plus mileage: never present them as a total. Canadian quotes: give `rate` and `rate_with_fees` as U-Haul shows them, never pick one silently.
- Storage: quote `monthly_rate` per unit with its size, section and attributes, and promotions as U-Haul words them. `vacant_units` is the count U-Haul's page carries: quote it as that, never as a promise a unit is free to rent.
- Report U-Haul's figures and the arithmetic only. Never judge a rate or a promotion, never call one operator cheaper beyond the numbers shown, and compare storage across operators only like for like (same size, same date), each with its date.
- Dealer and center names, addresses and phone numbers are the business's public contact. Reviews carry no reviewer names; never try to identify a reviewer or staff member mentioned in a review.
- Not available: pickup locations on quotes, reservations, trailer, towing and U-Box quotes, storage rentals or move-ins, prices by latitude / longitude, price history (poll and store), cart or checkout. This API cannot reserve, rent or buy.
- Terms: Scavio does not store U-Haul data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON. U-Haul's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish U-Haul photos or logos; link locations and facilities by `url` instead.
- Never fabricate rates, truck availability, unit prices, vacant counts, location ids, hours, ratings or dates. Only return what the API returned, with the `fetched_at` time and the `url` where one is given.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "pickup is required", "date must be YYYY-MM-DD (the pickup day).", "date is not a real calendar day.", "date must be today or later.", "date must be within the next 330 days (U-Haul quotes moves up to 11 months ahead).", "dropoff equals pickup: leave dropoff empty for an in-town quote."; a place that is not a city, ZIP or postal code ("near must be a city with its state or province (Dallas, TX), a ZIP (75201) or a postal code (M5V 2T6)."), coordinates ("... U-Haul does not search by latitude / longitude."); "location_id (or url) is required.", an id that is not 5-7 digits ("location_id must be a U-Haul location id (5-7 digits, e.g. 741028; locations[].location_id or facilities[].facility_id)."), "location_id does not match the link's id.", "language does not match the link's site (fr)."; a link that is not a uhaul.com location link; "features takes at most 6 values."; "term must be the start of a city, a ZIP or a postal code."; supplies "Send category or url, not both.", "category (Boxes, Packing-Supplies, ...) or url is required.", "supplies pages are in English (U-Haul's www site): send language en or none."; an unknown `service`, `sort` or `language`; a `page` or `page_size` outside its range.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "U-Haul has no truck rates for this move. Send pickup (and dropoff) as a city with its state or province (Dallas, TX), a ZIP or a postal code.", "U-Haul could not quote this move: <U-Haul's own message>", "U-Haul lists no truck rentals locations near <place>. ...", "U-Haul lists no self-storage near <place>. ...", "U-Haul has no location <id> (locations[].location_id from locations).", "U-Haul has no storage facility <id> (facilities[].facility_id from storage_search).", "U-Haul has no moving supplies category <category> (Boxes, Packing-Supplies, Tape)." Take ids from a previous answer rather than guessing them.
- One `404` is **not** charged: when U-Haul's form reads a place as another one with the same name (Toronto, ON read as Toronto, OH), the quote is retried and then refused: "U-Haul read pickup Toronto, ON as Toronto, OH. Send the place with its ZIP or postal code (Toronto, ON M5V 2T6) so U-Haul reads the right one. Not charged." Send the postal code and call again.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api).
- `502` or `503` means U-Haul data was temporarily unavailable ("U-Haul is temporarily unavailable. Please try again.") or busy ("U-Haul is busy right now. Please retry in a few seconds.", with a `Retry-After` header): wait and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.100.0
npm install scavio@0.101.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: quote } = await scavio.uhaul.truckQuote({ pickup: "Dallas, TX", dropoff: "Austin, TX", date: "2026-12-11" });
const { data: near } = await scavio.uhaul.locations({ near: "75201", service: "truck_rentals" });
const { data: center } = await scavio.uhaul.location({ location_id: "741028" });
const { data: storage } = await scavio.uhaul.storageSearch({ near: "Phoenix, AZ 85004", sort: "price" });
const { data: facility } = await scavio.uhaul.storageFacility({ facility_id: "741065" });
const { data: critical } = await scavio.uhaul.reviews({ location_id: "741028", stars: 1, service: "trucks" });
const { data: places } = await scavio.uhaul.suggestions({ term: "dall" });
const { data: boxes } = await scavio.uhaul.supplies({ category: "Boxes", country: "ca" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.uhaul.truck_quote(...)`, `locations`, `location`, `storage_search`, `storage_facility`, `reviews`, `suggestions` and `supplies`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 8 endpoints as tools: `get_uhaul_truck_quote`, `search_uhaul_locations`, `get_uhaul_location`, `search_uhaul_storage`, `get_uhaul_storage_facility`, `get_uhaul_reviews`, `get_uhaul_suggestions` and `get_uhaul_supplies`. U-Haul is opt-in: add `uhaul` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.100.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,uhaul"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [truck quote](https://scavio.dev/docs/uhaul-truck-quote?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api), [locations](https://scavio.dev/docs/uhaul-locations?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api), [location](https://scavio.dev/docs/uhaul-location?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api), [storage search](https://scavio.dev/docs/uhaul-storage-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api), [storage facility](https://scavio.dev/docs/uhaul-storage-facility?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api), [reviews](https://scavio.dev/docs/uhaul-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api), [suggestions](https://scavio.dev/docs/uhaul-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api), [supplies](https://scavio.dev/docs/uhaul-supplies?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api). Overview: [U-Haul API](https://scavio.dev/uhaul-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=uhaul-api).
