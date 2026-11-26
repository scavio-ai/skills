---
name: carvana-api
description: Carvana API for Carvana (carvana.com, the US online used-car retailer) - Carvana's listed price next to the Kelley Blue Book value Carvana shows for the same vehicle, the MSRP and market_adjustment (Carvana's price minus that MSRP), the previous price and when it changed, and Carvana's own labels such as Great Deal (Carvana's text - priced at least $1,500 below its Kelley Blue Book Suggested Retail Value) and New Price (a 2019 Ford F-150 XLT with 93,232 miles read 21,990 USD, previously 22,590, next to a KBB value of 23,600 on Nov 26, 2026); used-car search by make and model as Carvana writes them, 24 a page, six sorts, filters for model year, price, maximum mileage, trims, drive types, colours, body styles, fuel types, Carvana's tags and free shipping, with facet counts on request, inventory national and the location set by Carvana's own city pages (new-york-ny, los-angeles-ca) or by the visit - shipping cost and delivery flags change with it; one vehicle in full by id with powertrain, dimensions, factory warranty left, prior use, recalls, highlights with the history-report basis text Carvana gives, Carvana's inspection report, imperfections, features, packages and the hub holding it; Carvana's model-year guide (what changed, specs by trim, trims in stock, owner rating and star counts, owner reviews without names, FAQ), trim guide and make lineup, and every make with its in-stock count. 6 endpoints, 1 credit per call. US only, USD. No ZIP targeting, no keyword search, no VIN, no monthly payments, taxes, fees, delivery quotes or price history.
version: 1.0.0
tags: carvana, carvana-api, carvana-prices, carvana-used-cars, carvana-inventory, carvana-search, carvana-vehicle, carvana-kbb, carvana-great-deal, carvana-price-drop, carvana-inspection, carvana-model-guide, carvana-trims, carvana-makes, used-cars, used-car-prices, used-car-listings, used-car-inventory, online-car-retailer, kelley-blue-book, kbb-value, msrp, car-prices, model-year, trim-guide, owner-ratings, shipping-cost, automotive, us-retail, usd, price-monitoring, price-comparison, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/carvana-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=carvana-api
---

# Carvana API - Used Car Prices, KBB Value, Vehicle Details

Read Carvana (carvana.com, the US online used-car retailer): used-car search by make and model, one vehicle in full, Carvana's model-year guide, trim guide and make lineup, and every make with its in-stock count. Every answer is what Carvana's public pages show a visitor without an account at the moment of the call, in USD. All 6 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Carvana shows to any visitor and returns them as JSON for analysis. It uses no Carvana account, no financing pre-qualification, no trade-in or sell-my-car offer, no reservation and no checkout.

**The job this skill is for: Carvana's listed price next to the Kelley Blue Book value Carvana shows for the same vehicle.** Every search item and vehicle carries `price`, `kbb_value` (the KBB value Carvana shows next to the price), `msrp`, `market_adjustment` (Carvana's price minus that MSRP), `previous_price` with `price_updated_at`, and Carvana's `tags`. Captured 2026-11-26 (1 credit per call):

| Vehicle (`vehicle_id`) | Miles | `price` | `previous_price` | `kbb_value` | `msrp` / `market_adjustment` | `tags` |
|---|---|---|---|---|---|---|
| 2019 Ford F-150 XLT SuperCab 6 1/2 ft (4832946) | 93,232 | 21,990 | 22,590 (changed Nov 20) | 23,600 | 43,280 / -21,290 | New Price, Great Deal |
| 2025 Ford F-150 XLT SuperCrew 5 1/2 ft (4947600) | 33,481 | 32,990 | none | 40,007 | 56,850 / -23,860 | Recently Added, Great Deal |
| 2019 Toyota RAV4 XLE (4918779) | 53,856 | 26,590 | 26,990 (changed Nov 24) | 24,390 | 29,970 / -3,380 | New Price |
| 2019 Honda Civic LX sedan (4763258) | 80,257 | 17,790 | 17,990 | 16,630 | 21,305 / -3,515 | none |
| 2026 Toyota RAV4 LE hybrid (4886803) | 1,810 | 38,990 | none | 38,440 | 34,750 / +4,240 | none |

Carvana's own text for its Great Deal label, as the vehicle page gives it: "This car is priced at least $1,500 below its Kelley Blue Book® Suggested Retail Value." Quote the price, the KBB value and the label as Carvana shows them, with the mileage and date; compute any difference yourself and label it computed (21,990 against 23,600 is 1,610 below, computed). Never call the KBB value a valuation of the user's car. For another retailer's price on the same model-year use `carmax-api` (CarMax's listed prices and its recent instant offers for the model-year), `cargurus-api`, `autotrader-api` or `cars-com-api`, matched on year, make, model, trim and mileage band.

Ten limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **No ZIP targeting; location comes from a city page or the visit.** Carvana sets the location from the visit or from its own city pages. Pass `city` (`new-york-ny`, `los-angeles-ca`, or `"New York, NY"`) to use Carvana's city page; without it the location is the one Carvana set for that visit, which is not chosen by the request: send `city` whenever the location matters. `location.source` says which (`city_page` or `visit`). A `zip` or `postal_code` is a `400`.
- **City works only without filters or sort.** Carvana keeps the location only on an unfiltered city page: `city` with any filter or a sort other than `most_popular` is a `400`. Send `city` with `make`, `model` and `page` only, or filters and sorts without `city`.
- **Inventory is national; shipping changes with the location.** Every listed vehicle can be bought from anywhere; the location changes `shipping_cost` (0 = free), the delivery flags (`delivery_available`, `out_of_market`, `earliest_delivery_date`) and the counts slightly, not which vehicles exist. The same 2013 RAV4 Limited (4831499) read `shipping_cost` 0 at one location and 1,990 at another. Report shipping with the location it was shown for.
- **Totals move with the location and the visit.** Toyota RAV4 read 1,366, 1,266 and 1,101 vehicles in three captures, and `/makes` read 83,988, 87,667 and 90,664 vehicles in stock. Report a total with its `fetched_at` and location.
- **Most popular is not stable between pages.** Carvana recomputes its default order per visit: to page through results, send a fixed sort (`lowest_price`, `highest_price`, `lowest_mileage`, `newest_year`, `newest_listed`).
- **Names as Carvana writes them, and no keyword search.** `make` and `model` are Carvana's names (case ignored, hyphens count: `F-150`, `CR-V`); `/makes` and `/make` list them, and an unknown name is a charged `404` that lists Carvana's names. `query` and `keyword` are a `400`.
- **Used vehicles only.** Carvana's listings hold used vehicles; each item's `offering` says so, and `offering` as an input is a `400`. The mileage filter takes a maximum only (`mileage_min` is a `400`).
- **No VIN, no payment or fee figures.** No endpoint returns a VIN. Monthly payments, shipping to an address, taxes, fees and delivery dates for an address are not included (Carvana computes them per visitor). `price` is before taxes, title, registration and fees.
- **What is not there.** No ZIP targeting, keyword search, search suggestions, dealers (Carvana is the seller), owner-review paging beyond what a research page shows, price trends or price history (store your own answers with `fetched_at`), trade-in or sell-my-car offers, checkout.

Carvana publishes no public developer API or inventory feed; its affiliate program for publishers offers links, not data. This skill reads Carvana's public pages with one Scavio key.

See also: `carmax-api` (CarMax's no-haggle prices by ZIP and its recent instant offers for a model-year), `cars-com-api`, `autotrader-api` and `cargurus-api` (dealer and private listings across the US), and `offerup-api` (local private-party cars by ZIP). Same model-year only: match year, make, model and trim, keep the mileage beside each price, and name the retailer and date with every number.

## When to trigger

Use this skill when the user asks to:
- Read Carvana's price for used vehicles next to the Kelley Blue Book value Carvana shows, the MSRP and the last price change
- Search Carvana's used cars by make and model, sorted by price, mileage, model year or newest listed, filtered by year, price, maximum mileage, trims, drive type, colour, body style, fuel type, Carvana's tags (Great Deal, New Price, No Reported Accidents, Single Owner, Recently Added, Low Miles Per Year) or free shipping
- See what a vehicle's shipping cost and delivery flags read for one of Carvana's city pages
- Read one Carvana vehicle in full: powertrain, dimensions, warranty left, prior use, recalls, highlights, the inspection report and imperfections
- Read Carvana's model-year guide (what changed that year, specs by trim, owner rating), its trim guide for a model, a make's lineup, or every make's in-stock count

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=carvana-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=carvana-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (50 search pages of 24 vehicles, or 50 vehicles in full).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, search answered in 4-12 seconds, vehicle 3-7, model guide 3-5, trims 3-4, make 2-5 and makes 4-10. Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/carvana/search` | Used vehicles by make and model, 24 a page: price, KBB value, MSRP, market adjustment, previous price, shipping cost, tags, warranty left; total, pages, filters applied, the location used, facets with counts on request | 1 |
| `POST /api/v1/carvana/vehicle` | One vehicle by id: price, previous price, KBB value, MSRP, powertrain, dimensions, warranty, prior use, recalls, highlights, inspection, imperfections, features, packages, options, Carvana's AI-written summary (labelled), hub | 1 |
| `POST /api/v1/carvana/model-guide` | Carvana's guide to one model year: summary, generation, what changed, specs by trim, trims in stock, owner rating and star counts, owner reviews (no names), FAQ, sources | 1 |
| `POST /api/v1/carvana/trims` | Carvana's trim guide for one model: trim groups with descriptions, best-for text, highlights, attributes and in-stock counts, FAQ | 1 |
| `POST /api/v1/carvana/make` | One make's model lineup: model names (the input of search), taglines, in-stock counts, body types | 1 |
| `POST /api/v1/carvana/makes` | Every make with its in-stock count, the total in stock and the location used | 1 |

## Market

US only, USD: every answer carries `market` {`country` "us", `currency` "USD", `language` "en"}. There is no `country` or `zip` input; see the location limit above.

## Prices, labels and location

| Field | Meaning |
|---|---|
| `price` | Carvana's listed price, USD, before taxes, title, registration and fees |
| `kbb_value` | The Kelley Blue Book value Carvana shows next to the price (`fair_market_value` on `/vehicle` reads the same value in the captures) |
| `msrp`, `market_adjustment` | The MSRP Carvana shows and Carvana's price minus it (negative = below MSRP) |
| `previous_price`, `price_updated_at` | Carvana's last price change, as given; `null` without one |
| `tags` (search) | Carvana's labels: Great Deal, New Price, No Reported Accidents, Single Owner, Recently Added, Low Miles Per Year |
| `highlights` (vehicle) | {`key`, `name`, `description`}: Carvana's labels with the CARFAX / AutoCheck basis text exactly as Carvana gives it |
| `shipping_cost` (search) | The shipping Carvana shows to the location the page used (0 = free) |
| `purchase_pending`, `purchase_type`, `sale_status` | Carvana's own availability flags |
| `remaining_warranty_months`, `remaining_warranty_miles` | Factory warranty left, as Carvana shows it |
| `location` (search, makes) | {`source` (`city_page` or `visit`), `city`, `state`, `zip`, `delivery_available`, `pickup_available`, `out_of_market`, `miles_to_pickup`, `earliest_delivery_date`, `pickup_city`, `pickup_state`} |
| `hub` (vehicle) | The Carvana location holding the vehicle {`city`, `state`, `zip`} |
| `ai_summary` (vehicle) | Carvana's AI-written text about the vehicle, labelled as such in `source`; quote it as Carvana's, never as a fact Scavio checked |

- **Vehicle ids:** `vehicle_id` (from `items[].vehicle_id`) is the input of `/vehicle`; `stock_number` is Carvana's stock number. A sold or removed vehicle leaves Carvana's site: a charged `404`.

## Workflow

1. **Names.** `/makes` for the makes, `/make` with `make` for its models (the names search takes, hyphens included).
2. **Search.** `/search` with `make`, `model`, a fixed `sort` and filters (`year_min`, `price_max`, `mileage_max`, `tags`, `include_facets: true` on the first call for trims and counts). Note each `vehicle_id`, `price`, `kbb_value`, `mileage`, `tags` and `shipping_cost`.
3. **Location, if shipping matters.** `/search` with `make`, `model` and `city` (no filters, no sort) for one of Carvana's city pages; report `location` with the shipping figures.
4. **One vehicle.** `/vehicle` with `vehicle_id` for the previous price, highlights, inspection, imperfections, warranty and hub.
5. **Context for the model-year.** `/model-guide` with `year`, `make`, `model` for what changed and the owner rating; `/trims` for Carvana's trim groups.
6. **Compare.** The same model-year at CarMax (`carmax-api`) or another retailer, matched on year, make, model, trim and mileage band.
7. **Report.** Each price with Carvana, the vehicle's year, make, model, trim and mileage, the KBB value Carvana shows, Carvana's tags, the location for shipping and the `fetched_at` date; any difference labelled computed.
8. **Price series:** there is no history beyond the last change. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `make` | string | none | A make as Carvana writes it (`Toyota`, `Ford`, `Mercedes-Benz`; case ignored) |
| `model` | string | none | Needs `make`. A model as Carvana writes it (`RAV4`, `F-150`, `CR-V`; hyphens count) |
| `city` | string | none | One of Carvana's city pages (`new-york-ny`, `los-angeles-ca`, or `"New York, NY"`). Only with `make`, `model` and `page`: a filter or a sort with `city` is a `400` |
| `page` | integer | 1 | Page, 24 vehicles each; `total_pages` says how many |
| `sort` | string | `most_popular` | `most_popular` (not stable between pages), `lowest_price`, `highest_price`, `lowest_mileage`, `newest_year`, `newest_listed` |
| `year_min`, `year_max` | integer | none | Model year range |
| `price_min`, `price_max` | integer | none | Price range, USD |
| `mileage_max` | integer | none | Mileage up to (no minimum) |
| `trims` | list or string | none | Needs `make` and `model`: up to 10 trim names as Carvana writes them (`["XLE"]`; `include_facets` lists them) |
| `drive_types` | list or string | none | Any of `4wd`, `awd`, `fwd`, `rwd` |
| `colors` | list or string | none | Any of `beige`, `black`, `blue`, `brown`, `gold`, `gray`, `green`, `orange`, `pink`, `purple`, `red`, `silver`, `white`, `yellow` |
| `body_styles` | list or string | none | Any of `suv`, `sedan`, `truck`, `coupe`, `minivan`, `convertible`, `wagon`, `hatchback` |
| `fuel_types` | list or string | none | Any of `gas`, `diesel`, `electric`, `hybrid`, `plug_in_hybrid` |
| `tags` | list or string | none | Any of `great_deal`, `new_price`, `no_reported_accidents`, `single_owner`, `recently_added`, `low_miles_per_year` (Carvana's labels) |
| `free_shipping` | boolean | false | Only vehicles Carvana ships free to the location the page uses |
| `include_facets` | boolean | false | Counts per filter value, the year, price and mileage ranges, the makes, and the make's models with their trims |

Refused with a `400` that explains why: `zip`, `postal_code`, `query` / `keyword`, `offering`, `mileage_min`, and sorts Carvana ignores (`oldest_year`, `highest_mileage`, `newest`, `oldest`).

### Vehicle, model guide, trims, make, makes

| Endpoint | Parameters |
|---|---|
| `/vehicle` | `vehicle_id` (`4832946`, from `items[].vehicle_id`), or `url`: a carvana.com vehicle page address, as `items[].url` gives it |
| `/model-guide` | `year` (`2021`), `make` (`Toyota`), `model` (`RAV4`), all required |
| `/trims` | `make`, `model`, both required |
| `/make` | `make` (required) |
| `/makes` | none (`{}`) |

## Examples

### Search with filters, lowest price first

```bash
curl -X POST https://api.scavio.dev/api/v1/carvana/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "Ford", "model": "F-150", "year_min": 2019, "tags": ["great_deal"], "sort": "lowest_price", "include_facets": true}'
```

Captured `data` (2026-11-26; `items` cut to 2 of 24, `url`, `image`, `facets` and `notes` dropped):

```json
{
  "make": "Ford",
  "model": "F-150",
  "city": null,
  "sort": "lowest_price",
  "page": 1,
  "page_size": 24,
  "total": 578,
  "total_pages": 25,
  "has_more": true,
  "count": 24,
  "filters_applied": {"year_min": 2019, "tags": ["great_deal"]},
  "items": [
    {"vehicle_id": 4832946, "stock_number": "3006784065", "year": 2019, "make": "Ford", "model": "F-150", "model_variant": "F150 Super Cab", "trim": "XLT 6 1/2 ft", "kbb_trim": "XLT Pickup 4D 6 1/2 ft", "exterior_color": "Black", "interior_color": "Black", "body_style": "Pickup", "mileage": 93232, "mpg": 19, "fuel_type": "Gas", "seats": 5, "horsepower": 250, "price": 21990, "kbb_value": 23600, "msrp": 43280, "market_adjustment": -21290, "previous_price": 22590, "price_updated_at": "2026-11-20T14:38:26.967Z", "shipping_cost": 1590, "tags": ["New Price", "Great Deal"], "purchase_pending": false, "purchase_type": "Purchasable", "offering": "Used", "remaining_warranty_months": 0, "remaining_warranty_miles": 0, "currency": "USD"},
    {"vehicle_id": 4820438, "stock_number": "3006808304", "year": 2020, "make": "Ford", "model": "F-150", "model_variant": "F150 Super Cab", "trim": "XLT 6 1/2 ft", "kbb_trim": "XLT Pickup 4D 6 1/2 ft", "exterior_color": "Gray", "interior_color": "Black", "body_style": "Pickup", "mileage": 101499, "mpg": 18, "fuel_type": "Gas", "seats": 5, "horsepower": 325, "price": 21990, "kbb_value": 23725, "msrp": 43980, "market_adjustment": -21990, "previous_price": 22590, "price_updated_at": "2026-11-20T14:39:15.02Z", "shipping_cost": 1590, "tags": ["New Price", "Great Deal"], "purchase_pending": false, "purchase_type": "Purchasable", "offering": "Used", "remaining_warranty_months": 0, "remaining_warranty_miles": 0, "currency": "USD"}
  ],
  "location": {"source": "visit", "city": "Christiansted", "state": "VI", "zip": "00821", "delivery_available": false, "pickup_available": true, "out_of_market": true, "miles_to_pickup": 1148, "earliest_delivery_date": null, "pickup_city": "Miami", "pickup_state": "FL"},
  "market": {"country": "us", "currency": "USD", "language": "en"}
}
```

The location was the one Carvana set for the visit (Christiansted, VI, `out_of_market` true), so the 1,590 shipping costs are for that location. The `facets` held `body_styles`, `colors` (white 210, gray 99, black 97 ...), `drive_types` (4WD 475, RWD 103), `fuel_types`, `tags` (New Price 232, Low Miles Per Year 84 ...), `offerings` (Used 578), the `year` (2013-2026), `price` (19,590-113,990) and `mileage` ranges, `makes` and `models`, each value with its `count` and `applied`.

### A city page

```bash
curl -X POST https://api.scavio.dev/api/v1/carvana/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "Honda", "model": "Civic", "city": "los-angeles-ca"}'
```

Captured (2026-11-26): `total` 488 over 21 pages, `location` {`source` "city_page", `city` "Venice", `state` "CA", `zip` "90291", `delivery_available` true, `out_of_market` false, `miles_to_pickup` 36, `earliest_delivery_date` "2026-11-27T16:45:00Z", `pickup_city` "Westminster"}; first a 2019 Civic LX sedan (4763258) at 17,790 with 80,257 miles, KBB value 16,630, `shipping_cost` 0. `new-york-ny` (Toyota RAV4, page 2) used Brooklyn, NY 11229 with delivery available and listed 1,101 RAV4s.

### One vehicle

```bash
curl -X POST https://api.scavio.dev/api/v1/carvana/vehicle \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"vehicle_id": "4832946"}'
```

Captured `data` (2026-11-26; `dimensions`, `inspection` (cut), `imperfections` to 1, `features`, `packages`, `options`, `ai_summary`, `url`, `image`, `images` and `notes` dropped):

```json
{
  "vehicle_id": 4832946,
  "stock_number": "3006784065",
  "year": 2019,
  "make": "Ford",
  "model": "F-150",
  "model_variant": "F150 Super Cab",
  "trim": "XLT Pickup 4D 6 1/2 ft",
  "body_type": "Truck",
  "exterior_color": "Black",
  "exterior_color_oem": "Agate Black Metallic",
  "mileage": 93232,
  "price": 21990,
  "previous_price": 22590,
  "price_updated_at": "2026-11-20T14:38:26.965Z",
  "kbb_value": 23600,
  "fair_market_value": 23600,
  "msrp": 43280,
  "market_adjustment": -21290,
  "market_value_date": "2026-11-21T10:02:58.000Z",
  "currency": "USD",
  "powertrain": {"engine": "EcoBoost 2.7L V-6 DOHC", "transmission": "10-speed automatic", "automatic": true, "drivetrain": "4WD", "fuel": "Gas", "horsepower": 325, "mpg_city": 19, "mpg_highway": 24, "mpg_combined": 21},
  "warranty": {"basic_miles": 36000, "basic_months": 36, "drivetrain_miles": 60000, "drivetrain_months": 60, "remaining_basic_miles": 0, "remaining_basic_months": 0, "remaining_drivetrain_miles": 0, "remaining_drivetrain_months": 0},
  "in_service_date": "2019-05-06T04:00:00.000Z",
  "keys": 1,
  "prior_use": ["Lease"],
  "recalls": [],
  "autocheck_accident_reported": false,
  "highlights": [
    {"key": "AccidentFree", "name": "No Reported Accidents", "description": "This vehicle has no reported accidents, fire, flood, or frame damage according to CARFAX™ and AutoCheck®."},
    {"key": "RecentPriceDrop", "name": "New Price", "description": "New Price"},
    {"key": "KeepMovingPrice", "name": "Great Deal", "description": "This car is priced at least $1,500 below its Kelley Blue Book® Suggested Retail Value."}
  ],
  "inspection": {"inspected_on": "2026-10-13T00:00:00.000Z", "categories": [{"name": "Under the hood", "points": [{"name": "Engine condition (visual verification of oil change maintenance)", "status": "FixedOrReplaced"}, {"name": "Battery (condition, fluid level, load test)", "status": "Passed"}]}]},
  "imperfections": [{"title": "Worn or Faded", "description": "Discoloration or fading of material, usually due to UV exposure or use.", "zone": "Steering Wheel", "location": "interior"}],
  "hub": {"city": "Heath", "state": "OH", "zip": "43056"},
  "sale_status": "Available",
  "purchase_type": "Purchasable",
  "offering": "Used",
  "market": {"country": "us", "currency": "USD", "language": "en"}
}
```

The 2019 Civic LX (4763258) read 17,790, previous 17,990, KBB value 16,630, prior use Lease, 7 imperfections, hub San Diego, CA. The 2026 RAV4 LE hybrid (4886803) read 38,990 against an MSRP of 34,750 (`market_adjustment` +4,240) with the labels No Reported Accidents, Low Miles Per Year and Single Owner. No vehicle carries a VIN, a monthly payment, taxes or fees.

### Model-year guide, trims, make, makes

- `/model-guide` `{"year": 2021, "make": "Toyota", "model": "RAV4"}`: "2021 Toyota RAV4", `in_stock` 149, `rating` 4.3 from 1,404 owner ratings (`star_counts` 5: 652, 4: 521, 3: 194, 2: 33, 1: 4), `changes` (Powertrain: the first RAV4 Prime plug-in hybrid; Structural: a TRD Off-Road skid plate), engine and transmission by trim, `trims_in_stock` (XLE 50, LE 35, XLE Premium 21 ... TRD Off-Road 0), owner reviews as the page shows them (text, rating, date, vehicle; no names), `faq`, `sources` (Toyota press pages) and `next_year` 2022. The notes say Carvana's owner ratings come from Strategic Vision owner surveys one to six months after purchase. 2019 Ford F-150: rating 4.1 from 306, 251 in stock.
- `/trims` `{"make": "Ford", "model": "F-150"}`: 7 groups: Work Truck (XL, 445 in stock), Essential Value (STX, 55), Mid-Level (FX2, FX4, XLT, 858), Luxury Features (Lariat, Tremor, 235), Hybrid (18), Premium Luxury (Harley-Davidson, King Ranch, Lariat Limited, Limited, Platinum, 145), High Performance (Raptor, Raptor R, SVT Raptor, 56), each with Carvana's description, best-for text, highlights and attributes.
- `/make` `{"make": "Honda"}`: 17 models with in-stock counts (Accord 871, Civic 1,180, CR-V 1,242 ...). Ford: 32 models.
- `/makes` `{}`: 40 makes, `total_in_stock` 90,664 (Chevrolet 8,811, Ford 8,122, Jeep 7,824, Honda 5,441 ...); two more captures read 83,988 and 87,667 at other visit locations.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def carvana(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/carvana/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# Price next to the KBB value Carvana shows (1 credit per page)
s = carvana("search", {"make": "Toyota", "model": "RAV4", "year_min": 2019, "year_max": 2019,
                       "sort": "lowest_price"})["data"]
print("location:", s["location"]["source"], s["location"]["city"], s["location"]["state"])
for v in s["items"]:
    diff = v["price"] - v["kbb_value"] if v["kbb_value"] else None  # computed, label it so
    print(v["vehicle_id"], v["trim"], v["mileage"], v["price"], v["kbb_value"], diff, v["tags"])

# One vehicle in full (1 credit)
d = carvana("vehicle", {"vehicle_id": "4832946"})["data"]
print(d["price"], d["previous_price"], d["price_updated_at"], [h["name"] for h in d["highlights"]])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` and `notes`.

- **item** (search) - `vehicle_id`, `stock_number`, `url`, `year`, `make`, `model`, `model_variant`, `trim`, `kbb_trim`, `exterior_color`, `interior_color`, `body_style`, `mileage`, `mpg`, `fuel_type`, `seats`, `horsepower`, `price`, `kbb_value`, `msrp`, `market_adjustment`, `previous_price`, `price_updated_at`, `shipping_cost`, `tags`, `purchase_pending`, `purchase_type`, `offering`, `remaining_warranty_months`, `remaining_warranty_miles`, `image`, `currency`.
- **search** - `make`, `model`, `city`, `sort`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `filters_applied`, `items[]`, `location` {`source`, `city`, `state`, `zip`, `delivery_available`, `pickup_available`, `out_of_market`, `miles_to_pickup`, `earliest_delivery_date`, `pickup_city`, `pickup_state`}, `facets` (with `include_facets`: `body_styles`, `colors`, `drive_types`, `fuel_types`, `tags`, `offerings` [{`value`, `name`, `count`, `applied`}], `year`, `price`, `mileage` {`min`, `max`}, `makes`, `models` [{`name`, `count`, `applied`}] with trims), `market`, `notes`.
- **vehicle** - `vehicle_id`, `stock_number`, `url`, `year`, `make`, `model`, `model_variant`, `trim`, `body_type`, `doors`, `exterior_color`, `exterior_color_oem`, `interior_color`, `mileage`, `seats`, `price`, `previous_price`, `price_updated_at`, `kbb_value`, `fair_market_value`, `msrp`, `market_adjustment`, `market_value_date`, `currency`, `powertrain` {`engine`, `transmission`, `automatic`, `drivetrain`, `fuel`, `horsepower`, `mpg_city`, `mpg_highway`, `mpg_combined`}, `dimensions`, `warranty`, `in_service_date`, `in_service_miles`, `keys`, `prior_use`, `recalls`, `autocheck_accident_reported`, `highlights[]` {`key`, `name`, `description`}, `inspection` {`inspected_on`, `categories[]` {`name`, `points[]` {`name`, `status`}}}, `imperfections[]` {`title`, `description`, `zone`, `location`, `image`}, `features[]` {`category`, `name`, `tier`, `description`}, `packages[]`, `options[]` {`name`, `description`, `msrp`}, `ai_summary` {`source`, `summary`, `points`}, `hub` {`city`, `state`, `zip`}, `sale_status`, `purchase_type`, `offering`, `image`, `images`, `market`, `notes`.
- **model guide** - `year`, `make`, `model`, `name`, `url`, `summary`, `generation`, `in_stock`, `rating`, `rating_count`, `star_counts` {5..1}, `changes[]` {`area`, `text`}, `engine_by_trim`, `transmission_by_trim`, `drivetrain_by_trim` [{`trim`, `values`}], `other_specs[]` {`name`, `value`}, `trims_in_stock[]` {`trim`, `in_stock`}, `owner_reviews[]` {`text`, `rating`, `date`, `vehicle`}, `next_year` {`name`, `url`}, `faq[]` {`question`, `answer`}, `sources[]` {`name`, `url`}, `market`, `notes`.
- **trims** - `make`, `model`, `name`, `url`, `summary`, `count`, `groups[]` {`group`, `name`, `trims`, `description`, `best_for`, `highlights`, `attributes[]` {`name`, `value`}, `in_stock`, `image`}, `faq[]`, `sources`, `market`, `notes`.
- **make** - `make`, `name`, `url`, `summary`, `count`, `models[]` {`model`, `make`, `slug`, `url`, `tagline`, `in_stock`, `body_types`, `image`}, `market`, `notes`.
- **makes** - `count`, `total_in_stock`, `makes[]` {`make`, `in_stock`}, `location`, `market`, `notes`.

## Guardrails

- Name it "Carvana (carvana.com, the US online used-car retailer)" on first mention, "Carvana" after that.
- Links: write carvana.com as plain text only. Never put a link to Carvana in an answer, a table or a report, and do not pass on the `url`, `image` or `images` values as links; cite the vehicle's year, make, model, trim, `vehicle_id` and the capture date instead.
- Prices: quote each with USD, the vehicle's year, make, model, trim and mileage, the `fetched_at` date and "before taxes, title, registration and fees"; put shipping with the `location` it was shown for. Never compute an out-the-door price or a monthly payment.
- KBB value: say "the Kelley Blue Book value Carvana shows", never a valuation of the user's car. A difference between price and KBB value is computed by you: label it so.
- Labels and history: Great Deal, New Price and the other tags, highlights, the inspection and imperfections are Carvana's own; attribute them to Carvana (highlights cite CARFAX and AutoCheck as Carvana gives it). Quote `ai_summary` only as Carvana's AI-written text.
- Comparisons: the same model-year (and trim where given), mileage beside every number, named retailer and date. No verdict on which vehicle or retailer is cheaper beyond the numbers shown.
- Reviews: owner reviews carry no names; quote them as the page shows them, with the rating and date. Owner ratings are Carvana's figures from Strategic Vision owner surveys, as Carvana states.
- Descriptive only: no commentary on Carvana's business, pricing practices or policies.
- Do not republish Carvana photos or descriptions.
- Terms: Scavio does not collect or store Carvana data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no purchase, financing or trade-in flow. Carvana's terms of use cover how its site and content may be used, including linking to it; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, KBB values, vehicle ids, labels, locations or review text. Only return what the API returned, with the `fetched_at` time.
- Not available: ZIP targeting, keyword search, VIN, monthly payments, taxes, fees, delivery quotes for an address, search suggestions, dealers, price trends or history, trade-in offers, checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: `zip` or `postal_code` ("zip is not supported: Carvana sets the location from the visit and cannot be pointed at a ZIP. Use city ..."); `query` or `keyword` ("Keyword search is not offered: search by make and model ..."); `offering`; `mileage_min` ("Carvana's mileage filter takes a maximum only (mileage_max)"); `city` with a filter or a sort ("city works only without filters or sort ..."); a `city` that is not city-state (`new-york-ny`); `model` without `make`; `trims` without `make` and `model`, or more than 10 values in a list; a list value outside its set; a `sort` Carvana ignores or one not listed; a `_min` above its `_max`; `/vehicle` without `vehicle_id` or a valid carvana.com vehicle page address; `/model-guide` without `year`; `/trims` or `/make` without `make` (or `model`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: an unknown make ("Carvana lists no make named ... Makes: ...") or model ("Carvana lists no Ford model named ... Ford models: ...", with Carvana's names to retry with); "Carvana has no city page for ... in <city>. Check the make and model names (make endpoint) and the city ..., or search without city."; "Carvana has no vehicle <id> (a sold or removed vehicle leaves Carvana's site)."; "Carvana has no model-year guide for the ...", "Carvana has no trims guide for the ...", "Carvana has no model lineup for a make named ...". Take names and ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=carvana-api).
- `502` means Carvana data was temporarily unavailable ("Carvana is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy: wait the `Retry-After` seconds and send it again. Not charged.
- A search with `count` 0 is a `200`: no vehicle matches the filters at that moment. Loosen a filter rather than retrying the same call.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.96.0
npm install scavio@0.97.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: trucks } = await scavio.carvana.search({ make: "Ford", model: "F-150", year_min: 2019, tags: ["great_deal"], sort: "lowest_price" });
const { data: la } = await scavio.carvana.search({ make: "Honda", model: "Civic", city: "los-angeles-ca" });
const { data: vehicle } = await scavio.carvana.vehicle({ vehicle_id: "4832946" });
const { data: guide } = await scavio.carvana.modelGuide({ year: 2021, make: "Toyota", model: "RAV4" });
const { data: trims } = await scavio.carvana.trims({ make: "Ford", model: "F-150" });
const { data: makes } = await scavio.carvana.makes();
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.carvana.search(...)`, `vehicle`, `model_guide`, `trims`, `make` and `makes`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 6 endpoints as tools: `search_carvana`, `get_carvana_vehicle`, `get_carvana_model_guide`, `get_carvana_trims`, `get_carvana_make` and `get_carvana_makes`. Carvana is opt-in: add `carvana` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,carvana"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/carvana-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=carvana-api), [vehicle](https://scavio.dev/docs/carvana-vehicle?utm_source=agent-skills&utm_medium=skill&utm_campaign=carvana-api), [model guide](https://scavio.dev/docs/carvana-model-guide?utm_source=agent-skills&utm_medium=skill&utm_campaign=carvana-api), [trims](https://scavio.dev/docs/carvana-trims?utm_source=agent-skills&utm_medium=skill&utm_campaign=carvana-api), [make](https://scavio.dev/docs/carvana-make?utm_source=agent-skills&utm_medium=skill&utm_campaign=carvana-api), [makes](https://scavio.dev/docs/carvana-makes?utm_source=agent-skills&utm_medium=skill&utm_campaign=carvana-api). Overview: [Carvana API](https://scavio.dev/carvana-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=carvana-api).
