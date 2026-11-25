# Discount Tire API - Tire Prices by Store, Vehicle Fitment, Stock

Read Discount Tire (discounttire.com, the US tire and wheel retailer, America's Tire in parts of CA, PA, NJ and NY): tires by size, the vehicle selector and the tires that fit a vehicle, one tire or wheel in full, every size of a model, the exact units at the stores near a ZIP, wheels, model lists by category, brand or keyword, the stores near a ZIP, one store, store and tire reviews, the category list, search suggestions and a store's appointment calendar. One US catalog in USD for Discount Tire and America's Tire stores. All 15 endpoints return structured JSON at 1 credit per call.

**The job this skill is for: Discount Tire tire prices.** What a tire costs at a named Discount Tire or America's Tire store today, per tire, with the set-of-four figure shown as arithmetic, the same tire at other stores, the tires that fit a vehicle, and how many units the stores near a ZIP have. On 2026-11-25 (UTC) at store 1009 (Oak Street, 2301 N Scottsdale Rd, Scottsdale, AZ) the Michelin Defender 2 225/65R17 102H (item `108547`, GTIN `086699082183`, manufacturer part number `08218`) read `price` 206 per tire ($206 x 4 = $824 for four, arithmetic, not a Discount Tire field), 25 units at the store and the promotion "$110 OFF a set of 4!" ending `2026-12-04T07:59:00Z` with condition `MYACCOUNT`. A size search for `225/65R17` at the same store read 158 tires, the best seller the Mohave CUV at $79 per tire. `/store-stock` near ZIP 85251 listed 47 stores within 25 miles, the nearest five holding 38, 33, 16, 15 and 32 units. Pair it with `walmart-product-data`, `sams-club-product-data` and `amazon-product-data` for the same tire elsewhere, and `autozone-api` and `oreilly-auto-parts-api` for parts (same GTIN or manufacturer part number only).

Ten limits shape every answer, so say them plainly:
- **1 credit per call.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Every price is one store's price.** search, vehicle-tires, product, model, wheels and browse need `store` (a store code from `/stores`) or `zip` (the nearest store in Discount Tire's store search is used); without one the call is a `400`, not charged. The store used comes back in `store` {`store_code`, `brand`, `name`, `location_name`, `address`, `city`, `state`, `zip`, `phone`, `distance_miles`, `chosen_by`}. Measured: the Michelin Defender 2 225/65R17 read $206 at 9 stores in 8 states and $205 at an America's Tire store in New Jersey; across 45 tires in that size there were 0 price differences in Texas, Florida and Washington, 1 in California, 3 in Michigan and 13 of 32 at the New Jersey store. Write "$206 per tire at Discount Tire store 1009 (Scottsdale, AZ) on 2026-11-25", never one national price and never "every store differs".
- **Per tire only, no set price.** `price` is per tire (or per wheel). Discount Tire publishes no set-of-four price field: 4 x `price` is your arithmetic and must be labelled so. A staggered set is 2 front + 2 rear, each at its own price.
- **Promotions as given, end date only.** `promotions[]` carry Discount Tire's own `title`, `text`, `description`, `ends` (ISO 8601 UTC, converted from `ends_text`), `ends_text` (as given), `group`, `condition` and `url`. There is no start date. Many promotions read `condition` `MYACCOUNT` (group `myAccountPromotionRuleGroup`): they may need a Discount Tire account, so say so. Mail-in rebates read `condition` `OTHER`. Never subtract a promotion from a price, and never add urgency ("ends soon", "last day"): quote the end date exactly as given.
- **A vehicle is three ids.** `/vehicle` walks Discount Tire's selector one step per call: nothing -> years; `year` -> makes; `year` + `make` -> models (`vehicle_id`); `vehicle_id` -> trims (`trim_id`); `vehicle_id` + `trim_id` -> tire size options (`assembly_id`); all three -> the fitment. vehicle-tires and wheels by vehicle take the same three ids. Ids come from a previous answer, never a guess.
- **Staggered vehicles come in pairs.** Where the fitment has different front and rear sizes (`staggered` true), vehicle-tires answers front / rear pairs by default (`position` `set`), each tire with its own per-tire price; `front` or `rear` lists one axle. A size search with `rear_size` does the same by size.
- **OE and Treadwell are Discount Tire's own labels.** `original_equipment` is Discount Tire's flag for the vehicle maker's original-equipment tire. `ranking` `treadwell` adds Discount Tire's Treadwell ranking fields (rank, mileage, miles per dollar, ride ratings, stopping distances): Discount Tire's estimates, never Scavio measurements or a recommendation.
- **Store stock is exact units, plus a date message.** `/store-stock` gives the exact `units` of 1-4 items at the stores near a ZIP, 5 stores per page. `message` is Discount Tire's availability text for the `quantity` asked (default 4): a store with 0 units can still say "Available as soon as <date>" (stock that can be brought in). Quote `message` as given.
- **Read only.** `/appointments` reads the open service-appointment slots a store shows. Scavio never books, holds or cancels anything, and no endpoint adds to a cart or checks out.
- **No fees, no history.** No answer carries installation, disposal, road hazard or certificate prices or fees: never state an amount. Nothing is cached or kept: poll and store your own series for history.

Discount Tire publishes no public API for its catalog, prices, store stock or stores. Publishers can join its affiliate programme through Commission Junction (CJ), a links-and-commission programme, not a price API; fleet customers work through Discount Tire Fleet accounts and fleet-software integrations; suppliers and distributors connect through EDI and industry platforms. Prices are shown on discounttire.com and americastire.com for the store a shopper picks, and this skill reads those public pages with one Scavio key. Other vendors sell tire catalog, fitment or retail data; this skill reads Discount Tire's own public pages.

Discount Tire, a private company founded in 1960 and based in Scottsdale, Arizona, says it serves customers at more than 1,275 stores in 40 states, trading as America's Tire in parts of California, Pennsylvania, New Jersey and New York (Discount Tire release, Nov 17, 2026). Tire Rack is its sister company, a separate site with its own prices, and is not read. Mavis Discount Tire is a different company and is not read. Quote these with their source, never from the samples.

See also: for the same tire at Walmart use `walmart-product-data`, at Sam's Club `sams-club-product-data`, on Amazon `amazon-product-data` (match on GTIN or manufacturer part number with the same size, load index and speed rating); for parts by vehicle `autozone-api` and `oreilly-auto-parts-api`.

## When to trigger

Use this skill when the user asks to:
- Price a tire at a named Discount Tire or America's Tire store (or the store nearest a ZIP), per tire, with the set-of-four figure as labelled arithmetic
- Compare the same tire across Discount Tire and America's Tire stores
- List the tires in one size (225/65R17, LT265/70R17, 35x12.50R20), or a staggered front / rear pair, sorted by price or rating and filtered by brand, category, speed rating, load range, Three-Peak snowflake, run flat, rebates, instant savings, in stock or price
- Find the tires that fit a vehicle (year, make, model, trim, tire size option), with the OE tire flagged and staggered sets, or Discount Tire's Treadwell ranking for it
- Read a vehicle's fitment: front and rear sizes, wheel diameters, staggered flag, lug torque and the optional plus sizes
- Read one tire or wheel in full (UTQG, load index, speed rating, tread depth, max pressure, GTIN, manufacturer part number) or every size of one model with its price
- Check how many units of a tire the Discount Tire stores near a ZIP have
- Find wheels by size (diameter, width, bolt pattern) or that fit a vehicle
- List tire models in a category, of a brand or matching keywords
- Find Discount Tire and America's Tire stores near a ZIP, read one store's dated hours and services, or its reviews
- Read Discount Tire's own reviews of a tire, sorted, filtered by stars and paged in full
- Read the open service-appointment slots at a store (read only)
- Compare one tire at Discount Tire, Walmart, Sam's Club and Amazon by GTIN or manufacturer part number

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, most calls took 1 to 7 seconds; search, vehicle-tires and store-stock 6 to 10. Allow a client timeout of at least 120 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Store or ZIP | Credits |
|---|---|---|---|
| `POST /api/v1/discounttire/search` | Tires in one size (or a staggered front / rear pair), sorted, filtered and paged, with price, promotions and store units | required | 1 |
| `POST /api/v1/discounttire/vehicle` | The vehicle selector, one step per call: years, makes, models, trims, tire size options, fitment | no | 1 |
| `POST /api/v1/discounttire/vehicle-tires` | The tires Discount Tire lists for a vehicle fitment, OE flagged, staggered pairs, optional Treadwell ranking | required | 1 |
| `POST /api/v1/discounttire/product` | One tire or wheel by item number: specs, UTQG, GTIN, manufacturer part number, stock, promotions, FAQs | required | 1 |
| `POST /api/v1/discounttire/model` | Every size of one tire or wheel model with its price, size options and spec ranges | required | 1 |
| `POST /api/v1/discounttire/store-stock` | Exact units of 1-4 items at the stores near a ZIP (5 per page, 10-150 miles) | ZIP required | 1 |
| `POST /api/v1/discounttire/stores` | Discount Tire and America's Tire stores near a ZIP, city or point (10 per page) | no | 1 |
| `POST /api/v1/discounttire/store` | One store: dated hours for the coming week, services, ratings, nearby stores | no | 1 |
| `POST /api/v1/discounttire/reviews` | Discount Tire's own reviews of a tire model or one size, sorted, star-filtered and paged | no | 1 |
| `POST /api/v1/discounttire/store-reviews` | Discount Tire's own reviews of one store (5 per page) | no | 1 |
| `POST /api/v1/discounttire/wheels` | Wheels by size (diameter + width + bolt pattern) or that fit a vehicle | required | 1 |
| `POST /api/v1/discounttire/browse` | Tire models in a category, of a brand or matching keywords, with the price range at the store | required | 1 |
| `POST /api/v1/discounttire/categories` | Discount Tire's tire or wheel categories with their slugs | no | 1 |
| `POST /api/v1/discounttire/suggestions` | What Discount Tire's search box suggests for a few letters (no prices) | no | 1 |
| `POST /api/v1/discounttire/appointments` | One store's service-appointment calendar for a month, read only | no | 1 |

`country` is `us` (the default and only value: www.discounttire.com, USD) and `language` is `en` (the default and only value). Send `store` or `zip` on a price endpoint, not both.

## Prices, promotions and the set of four

Every priced item carries:

| Field | Meaning |
|---|---|
| `price` | Discount Tire's price per tire (or per wheel) at the store in `store`, USD |
| `price_text` | The price as Discount Tire writes it ("$206.00") |
| `price_range` | Model-level items (browse, wheels by size): {`min`, `max`} across the model's sizes at the store; `price` is `null` there |
| `markdown`, `map_price`, `map_display_rule` | As given; `null` when Discount Tire gives none |
| `promotions[]` | {`title`, `text`, `description`, `ends`, `ends_text`, `group`, `condition`, `url`}, as given |
| `stock` | {`store_code`, `units`, `message`, `available_date`, `days_out`} at the store |
| `gtin`, `manufacturer_part_number` | As given (they can be the same number: Mohave CUV `89847` reads `841623130510` for both) |
| `tier` | Discount Tire's Good / Better / Best label, as given (casing differs between endpoints: `Best`, `BEST`, `BETTR`) |
| `original_equipment` | Discount Tire's OE flag for the vehicle in the request |

- **Per tire:** "$206 per tire for the Michelin Defender 2 225/65R17 at Discount Tire store 1009 (Scottsdale, AZ) on 2026-11-25". For four, show the arithmetic: "4 x $206 = $824 (arithmetic; Discount Tire publishes no set price)".
- **Staggered:** "2 x $350 front + 2 x $462 rear = $1,624 (arithmetic)" for the Michelin Pilot Sport All Season 4 on a 2022 Corvette Stingray at store 1009.
- **Promotions:** quote `title` and the end date exactly ("$110 OFF a set of 4!, ends 2026-12-04T07:59:00Z as Discount Tire gives it"), and say when `condition` is `MYACCOUNT` that the offer may need a Discount Tire account. Never compute a price after a promotion or rebate.
- **Across stores:** call the same `item_number` with another `store`. America's Tire stores are the same company and catalog; the price follows the store.
- **Matching another retailer:** same brand, model, size, load index and speed rating, and the same GTIN or manufacturer part number. Each price with its retailer, store and date.
- Report Discount Tire's numbers and the arithmetic. Never call a price a rise, a cut or a bargain, never call one retailer cheaper beyond the numbers shown, and never state an installation, disposal or fee amount.

## Workflow

1. **Pick a store.** `/stores` with `zip` (`85251`), `city` (`"Phoenix, AZ"`) or `latitude` + `longitude`: `store_code` and `brand` (Discount Tire or America's Tire). Or send `zip` on a price endpoint and read `store` in the answer.
2. **Tires by size.** `/search` with `size` (`225/65R17`) or `width` + `aspect_ratio` + `diameter`, plus `store` or `zip`. Add `rear_size` for a staggered pair.
3. **Tires by vehicle.** `/vehicle` step by step (`{}`, `{"year": 2022}`, `{"year": 2022, "make": "Ford"}`, `{"vehicle_id": "17361"}`, `{"vehicle_id": "17361", "trim_id": "52455"}`), then `/vehicle-tires` with the three ids and a store. Send `ranking` `treadwell` for Discount Tire's Treadwell ranking.
4. **One tire.** `/product` with `item_number` (`items[].item_number`, the number after `/p/` in a discounttire.com link) and a store. Every size of the model: `/model` with `model_id` (`michelin-defender-2`).
5. **Units near a ZIP.** `/store-stock` with `item_number` (or up to 4 `item_numbers`, such as a staggered front and rear) and `zip`; `radius` 10, 25 (default), 50, 75 or 150; `sort` `distance` or `availability`; `page` for the next 5 stores; `quantity` 1-8 (default 4); optional `store` for your store's units in `my_store`.
6. **Narrow a list.** `sort`, the named filters (`brand`, `category`, `speed_rating`, `load_range`, `mileage_warranty`, `three_peak`, `run_flat`, `rebates`, `instant_savings`, `in_stock`, `min_price`, `max_price`) and `filters` (up to 10 `facets[].values[].filter` tokens, sent exactly as given); `page` (1-500) and `page_size` (1-100, default 20).
7. **Wheels.** `/wheels` with `diameter` + `width` + `bolt_pattern` (all three), or the vehicle's three ids, plus a store.
8. **Reviews.** `/reviews` with `item_number`: `scope` `model` (every size, default) or `size`, `sort`, `rating`, `page`, `page_size` (1-100, default 10). Store reviews: `/store-reviews` with `store_code`.
9. **Appointments.** `/appointments` with `store_code` and optional `month`: open slots per day, read only.
10. **Watching prices:** there is no history. Poll the same items at the same stores on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Store or ZIP (search, vehicle-tires, product, model, wheels, browse)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store` | string or integer | one of | A Discount Tire / America's Tire store code (`stores[].store_code`, e.g. `1009`) |
| `zip` | string or integer | one of | A US ZIP instead: the nearest store in Discount Tire's store search is used and echoed in `store` |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `size` | string | one of | `225/65R17`, `LT265/70R17`, `35x12.50R20` |
| `width`, `aspect_ratio`, `diameter` | string or number | one of | Instead of `size` (`225`, `65`, `17`) |
| `rear_size` | string | none | Rear size for a staggered pair (`305/30R20`): items become front / rear pairs |
| `sort` | string | `best_seller` | `best_seller`, `price_low`, `price_high`, `rating` |
| `brand`, `category`, `speed_rating`, `mileage_warranty` | string or array | none | As Discount Tire writes them (its facets): `Michelin`, `All-Season Tires` (or its code `allSeasonTires`), `H`, `60,000-70,000`; up to 5 values |
| `load_range` | string | none | `SL`, `XL`, `C`, `D`, `E`, ... |
| `three_peak`, `run_flat`, `rebates`, `instant_savings`, `in_stock` | boolean | false | Discount Tire's own filters |
| `min_price`, `max_price` | number | none | Per tire, USD, at the store |
| `filters` | array | none | 1-10 tokens exactly as `facets[].values[].filter` gives them (`brands:brand-MCH`); several are combined |
| `page`, `page_size` | integer | 1, 20 | Page (1-500) and items per page (1-100) |

### Vehicle (`/vehicle`) and vehicle tires (`/vehicle-tires`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `year` | integer or string | none | Vehicle: the year's makes (with `make`: its models) |
| `make` | string | none | Vehicle: a make as `makes[].make` writes it, with `year` |
| `vehicle_id` | string or integer | none | `models[].vehicle_id` (`17361`, 2022 Ford F-150) |
| `trim_id` | string or integer | none | `trims[].trim_id` (`52455`, XLT Crew Cab 2WD) |
| `assembly_id` | string | none | `assemblies[].assembly_id` (`0000E28B`, 245/70R17) |
| `position` | string | `set` | Vehicle tires, staggered vehicles only: `set` (front / rear pairs), `front` or `rear` |
| `ranking` | string | `all` | Vehicle tires: `all` or `treadwell` (adds `treadwell` to each item; `sort` `treadwell` becomes the default) |
| `sort` | string | `best_seller` | Vehicle tires: `best_seller`, `price_low`, `price_high`, `rating`, and `treadwell` with that ranking |

vehicle-tires needs `vehicle_id`, `trim_id` and `assembly_id` plus a store, and takes the same filters and paging as search.

### Product (`/product`), model (`/model`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_number` | string or integer | product: required | A Discount Tire item number (`108547`) |
| `nearby_stores` | array | none | Product: up to 10 store codes Discount Tire checks for a nearby store with stock (`nearby_store_stock`) |
| `model_id` | string | model: required | `michelin-defender-2`, or a discounttire.com `/buy-tires/` or `/buy-wheels/` link |
| `type` | string | from the link | Model: `tires` or `wheels` |

### Store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_number` or `item_numbers` | string, integer or array | one required | One item, or up to 4 checked together |
| `zip` | string or integer | required | A US ZIP: the stores near it |
| `radius` | integer | 25 | Miles: 10, 25, 50, 75 or 150 |
| `sort` | string | `distance` | `distance` or `availability` |
| `page` | integer | 1 | 5 stores per page (1-100) |
| `quantity` | integer | 4 | 1-8: the `message` text is written for this quantity |
| `store` | string or integer | none | Your store: its units come back in `my_store` |

### Wheels (`/wheels`), browse (`/browse`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `diameter`, `width`, `bolt_pattern` | string or number | wheels by size: all three | `20`, `9`, `6-135` (also `6x139.7` or `5x4.5` in inches) |
| `vehicle_id`, `trim_id`, `assembly_id` | string | wheels by vehicle | The vehicle's three ids; `diameter` picks another diameter than the vehicle's |
| `category`, `color` | string or array | none | Wheels: Discount Tire's Wheel Category and Wheel Color labels (`Chrome Wheels`, `Black`) |
| `special_offers` | boolean | false | Wheels: only wheels with a special offer |
| `sort` | string | `best_seller` | Wheels: `best_seller`, `price_low`, `price_high`; browse also `rating` and `relevance` |
| `category` (browse) | string | one of | A category slug from `/categories` (`all-season-tires`) |
| `brand` (browse) | string | one of | A tire brand (`Michelin`) |
| `q` (browse) | string | one of | Keywords (`michelin defender`) |

Browse lists tires only; for wheels use `/wheels`.

### Stores, store, reviews, store reviews, categories, suggestions, appointments

`/stores` takes one of `zip`, `city` (`"Phoenix, AZ"`) or `latitude` + `longitude`, optional `radius` (1-150 miles) and `page` (10 stores per page). `/store`, `/store-reviews` and `/appointments` take `store_code` (`1009`); store-reviews also `sort`, `rating` and `page` (5 per page); appointments `month` (1-12, default the current month). `/reviews` takes `item_number`, `scope` (`model` or `size`), `sort` (`newest`, `highest`, `lowest`, `most_helpful`), `rating` (1-5), `page` and `page_size`. `/categories` takes `type` (`tires`, default, or `wheels`). `/suggestions` takes `q` (3 characters or more).

## Examples

### One tire at one store

```bash
curl -X POST https://api.scavio.dev/api/v1/discounttire/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_number": "108547", "store": "1009"}'
```

Captured `data` (2026-11-25 UTC; `images`, `long_description` and `notes` dropped, `categories` cut to 2 of 4):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "locale": "en-US" },
  "store": { "store_code": "1009", "brand": "Discount Tire", "name": "Discount Tire Store (AZP 07)", "location_name": "Oak Street", "address": "2301 N SCOTTSDALE RD", "city": "SCOTTSDALE", "state": "AZ", "zip": "85257-2126", "phone": "480-994-5336", "distance_miles": null, "chosen_by": "store" },
  "requested_item_number": "108547",
  "item_number": "108547",
  "type": "tire",
  "model_id": "michelin-defender-2",
  "brand": "Michelin",
  "model": "Defender 2",
  "name": "Michelin Defender 2",
  "description": "225/65R17 102H B MCH DEFEN 2",
  "size": "225/65R17 102H SL BSW",
  "price": 206,
  "price_text": "$206.00",
  "price_range": null,
  "markdown": null,
  "map_price": null,
  "map_display_rule": null,
  "promotions": [
    { "title": "$110 OFF a set of 4!", "text": "$110 OFF a set of 4!", "description": "SAVE NOW: Get $110 off a set of 4!", "ends": "2026-12-04T07:59:00Z", "ends_text": "04-12-2026 07:59 AM", "group": "myAccountPromotionRuleGroup", "condition": "MYACCOUNT", "url": null }
  ],
  "rating": 4.8,
  "review_count": 11578,
  "recommend_count": null,
  "stock": { "store_code": "1009", "units": 25, "message": "20+ in stock at My Store", "available_date": "2026-11-24", "days_out": 0 },
  "gtin": "086699082183",
  "manufacturer_part_number": "08218",
  "mileage_warranty": 80000,
  "tier": "BEST",
  "categories": ["touringTires", "passengerTires"],
  "original_equipment": false,
  "image": "https://cdn.discounttire.com/sys-master/images/h98/h69/9998287110174/mmid2_ang_l.jpg",
  "url": "https://www.discounttire.com/buy-tires/michelin-defender-2/p/108547",
  "category_ratings": null,
  "tire": { "load_index": 102, "load_index_speed": "102H", "speed_rating": "Up to 130 mph", "load_range": "SL", "utqg": { "treadwear": "840", "traction": "B", "temperature": "B" }, "tread_depth": 10, "max_pressure": 51, "overall_diameter": 28.5, "section_width": "225", "aspect_ratio": "65", "rim_diameter": "17", "rim_width_range": "6.0 - 8.0", "sidewall": "Black Side Wall", "run_flat": false },
  "weight": { "net": 27.8, "gross": 27.8 },
  "faqs": [
    { "question": "Does the Michelin Defender 2 225/65R17 have a treadwear warranty?", "answer": "Yes, Michelin lists a 80,000-mile limited treadwear warranty for the Defender 2 when four tires are installed in size 225/65R17.", "type": "WARRANTY" }
  ],
  "nearby_store_stock": null,
  "no_longer_available": false
}
```

$206 is per tire at store 1009; 4 x $206 = $824 is arithmetic, not a Discount Tire field. The promotion's `condition` `MYACCOUNT` means it may need a Discount Tire account. `stock.message` "20+ in stock at My Store" is Discount Tire's text; `units` 25 is the exact count. `speed_rating`, `tread_depth`, `max_pressure`, `overall_diameter` and `weight` are as Discount Tire gives them, with no unit in the answer. An unknown item is a charged `404`.

### Units at the stores near a ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/discounttire/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_number": "108547", "zip": "85251"}'
```

Captured `data` (2026-11-25 UTC; 2 of 5 stores shown, `notes` dropped):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "locale": "en-US" },
  "item_numbers": ["108547"],
  "quantity": 4,
  "zip": "85251",
  "radius_miles": 25,
  "sort": "distance",
  "page": 1,
  "page_size": 5,
  "total": 47,
  "total_pages": 10,
  "count": 5,
  "my_store": null,
  "stores": [
    {
      "store_code": "1022",
      "brand": "Discount Tire",
      "name": "Discount Tire Store (AZP 20)",
      "address": { "line1": "9199 E TALKING STICK WAY", "line2": null, "city": "SCOTTSDALE", "state": "AZ", "zip": "85250-8506", "country": "US" },
      "phone": "480-951-9126",
      "latitude": 33.53841,
      "longitude": -111.883131,
      "distance_miles": 3.81,
      "stock": [{ "item_number": "108547", "units": 38, "message": "20+ in stock at My Store" }]
    },
    {
      "store_code": "1005",
      "brand": "Discount Tire",
      "name": "Discount Tire Store (AZP 03)",
      "address": { "line1": "1929 W MAIN ST", "line2": null, "city": "MESA", "state": "AZ", "zip": "85201-6919", "country": "US" },
      "phone": "480-962-1403",
      "latitude": 33.41466,
      "longitude": -111.873261,
      "distance_miles": 6.06,
      "stock": [{ "item_number": "108547", "units": 16, "message": "7+ in stock at My Store" }]
    }
  ]
}
```

47 stores within 25 miles, 5 per page (10 pages). `units` is the exact count Discount Tire reports per store and item; `message` is its text for the `quantity` asked. In the size search at store 1009, the Falken Pro G5 CSV read `units` 0 with "Available as soon as Wednesday, Nov. 25 at My Store": 0 on hand, stock that can be brought in. Units are as Discount Tire reports them at the moment of the call.

### The vehicle selector, step by step

```bash
curl -X POST https://api.scavio.dev/api/v1/discounttire/vehicle \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"vehicle_id": "17361", "trim_id": "52455"}'
```

Captured `data` (2026-11-25 UTC), the tire size options of a 2022 Ford F-150 XLT Crew Cab 2WD:

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "locale": "en-US" },
  "step": "assemblies",
  "vehicle_id": "17361",
  "trim_id": "52455",
  "count": 3,
  "options": [
    { "assembly_id": "0000E28B", "description": "245 /70 R17 SL", "staggered": false, "front_size": "245/70R17 SL", "rear_size": null },
    { "assembly_id": "0000E28C", "description": "265 /60 R18 SL", "staggered": false, "front_size": "265/60R18 SL", "rear_size": null },
    { "assembly_id": "0000E28D", "description": "275 /60 R20 SL", "staggered": false, "front_size": "275/60R20 SL", "rear_size": null }
  ],
  "next": "Send vehicle_id + trim_id + assembly_id for the fitment (vehicle-tires and wheels take the same three)."
}
```

The steps before it: `{}` read 79 years (2028 back to 1932); `{"year": 2022}` 58 makes; `{"year": 2022, "make": "Ford"}` 32 models, F-150 as `vehicle_id` `17361`; `{"vehicle_id": "17361"}` 30 trims, XLT Crew Cab 2WD as `trim_id` `52455`. With all three ids (`assembly_id` `0000E28B`) the fitment read `front_size` and `rear_size` `245/70-R17`, `staggered` false, wheel diameters 17, `lug_torque` 150 (as given, no unit) and `optional_sizes` for 9 wheel diameters (16 to 24 inches), each size with its `fit` (`match`, `oversize` or `undersize`) as Discount Tire gives it.

### Tires for a staggered vehicle

```bash
curl -X POST https://api.scavio.dev/api/v1/discounttire/vehicle-tires \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"vehicle_id": "16990", "trim_id": "51166", "assembly_id": "0000DI40", "store": "1009"}'
```

Captured `data` (2026-11-25 UTC, a 2022 Chevrolet Corvette Stingray; 1 of 20 pairs shown with fields cut, `store`, `facets` and `notes` dropped):

```json
{
  "vehicle": { "vehicle_id": "16990", "year": "2022", "make": "Chevrolet", "model": "Corvette", "type": "PAS", "trim_id": "51166", "trim": "Stingray", "assembly_id": "0000DI40", "front_size": "245/35-R19", "rear_size": "305/30-R20", "staggered": true, "front_wheel_diameter": "19", "rear_wheel_diameter": "20" },
  "staggered": true,
  "position": "set",
  "ranking": "all",
  "page": 1,
  "page_size": 20,
  "total": 93,
  "total_pages": 5,
  "count": 20,
  "sort": "best_seller",
  "items": [
    {
      "position": 1,
      "pair": "set",
      "front": { "item_number": "102019", "brand": "Michelin", "model": "Pilot Sport All Season 4", "size": "245/35R19 89Y SL BSW GM RF", "price": 350, "stock": { "store_code": "1009", "units": 0, "message": "Available as soon as Wednesday, Nov. 25 at My Store", "available_date": "2026-11-25", "days_out": 1 }, "gtin": "086699253392", "original_equipment": true },
      "rear": { "item_number": "102020", "brand": "Michelin", "model": "Pilot Sport All Season 4", "size": "305/30R20 99Y SL BSW GM RF", "price": 462, "stock": { "store_code": "1009", "units": 0, "message": "Available as soon as Wednesday, Nov. 25 at My Store", "available_date": null, "days_out": null }, "original_equipment": true },
      "url": "https://www.discounttire.com/buy-tires/michelin-pilot-sport-all-season-4/p/102019/rearProduct/102020",
      "price_note": "front.price and rear.price are per tire; a staggered set is 2 front + 2 rear."
    }
  ]
}
```

Discount Tire lists 93 front / rear pairs for it at store 1009. The first pair is the one Discount Tire flags as original equipment on both axles: 2 x $350 + 2 x $462 = $1,624 (arithmetic). `position` `front` or `rear` lists single tires for one axle. For a non-staggered vehicle (the F-150 above) items are single tires with `position_on_vehicle` `all`: 157 tires at store 1009, the Bridgestone Dueler LX 245/70R17 (`101351`) first at $194. `available_date` and `days_out` are Discount Tire's fields as given and can be `null` or disagree with `message` (a front tire read "Available as soon as Saturday, Nov. 28" with `available_date` 2026-11-25): quote `message`.

### Treadwell ranking

`ranking` `treadwell` on vehicle-tires sorts by Discount Tire's Treadwell rank and adds to each item `treadwell` {`rank`, `mileage` {`min`, `median`, `max`, `warranty`}, `miles_per_dollar`, `tire_life` {`years`, `months`}, `ride_ratings` {`comfort`, `handling`, `quiet`, `wet_handling`}, `stopping` {`dry_distance`, `dry_rating`, `wet_distance`, `wet_rating`, `wet_worn_distance`, `winter_rating`, `rolling_resistance_rating`}, `winter` {`snow_brake_distance`, `snow_brake_rating`, `snow_handling_rating`}}. These are Discount Tire's own estimates as given: label them "Discount Tire's Treadwell estimate", never a test result. Treadwell's chat assistant is not read.

### Reviews, stores, store, appointments and the rest

- `/search` `{"size": "225/65R17", "store": "1009"}`: `total` 158, 20 per page, best sellers first: Mohave CUV (`89847`) $79, Michelin Defender 2 (`108547`) $206, Phantom C-Sport (`90935`) $111, Arizonian Silver Edition All Season (`88927`) $127. Facets include Brands (31), Tire Category, Good Better Best, Speed Rating, Load Range, Mileage Warranty, Rebates, Instant Savings, In Stock and Three-Peak Mountain Snowflake. Promotions on that page: "$110 OFF a set of 4!" and "$100 OFF a set of 4!" (`MYACCOUNT`), and Goodyear and Continental mail-in rebates (`OTHER`), each with its own end date.
- `/model` `{"model_id": "michelin-defender-2", "store": "1009"}`: 60 sizes priced $180 to $327 per tire at store 1009 (`price_range`), `items[]` {`item_number`, `price`}, `size_options` and `spec_ranges` as given. Its `review_count` (11,389) can differ from the product's (11,578).
- `/reviews` `{"item_number": "108547"}`: the whole model, newest first, `rating` 4.8, `review_count` 11,578, `total` 10,623 matching, 1,063 pages of 10. Many reviews are rating-only (`text` `null`; 1 of the first 10 had text); each carries `category_ratings` (tread life, wet and dry traction, cornering, ride noise, ride comfort, winter), `pros`, `cons`, `state` and `vehicle` as the reviewer gave them, and no reviewer names or cities.
- `/stores` `{"zip": "85251"}`: `total` 58, 10 per page, nearest first: 1009 Oak Street (1.4 mi), 1022 Pavilions (3.8 mi), 1003 East Thomas (5.3 mi). `brand` names Discount Tire or America's Tire.
- `/store` `{"store_code": "1009"}`: rating 4.8 from 589 reviews, `hours` dated for the coming week (closed 2026-11-26 with note "Thanksgiving Day"), `store_services`, 4 `nearby_stores`. `{"store_code": "1752"}` is an America's Tire store (CAL 35, Glendale, CA). No staff names. An unknown store is a charged `404`.
- `/store-reviews` `{"store_code": "1009"}`: 608 reviews, 5 per page, with cleanliness and knowledge ratings and no reviewer names.
- `/wheels` `{"diameter": "20", "width": "9", "bolt_pattern": "6-135", "store": "1009"}`: 323 wheel models, each `type` `model` with `price_range` at the store, `item_numbers` and `finishes`; `/model` or `/product` gives each wheel's price.
- `/browse` `{"category": "all-season-tires", "store": "1009"}`: 617 tire models with `price_range` at the store (Sentury Touring $49 to $76 first). An unknown category or brand is a charged `404`.
- `/categories` `{}`: 14 tire categories (`all-season-tires`, `winter-tires`, `trailer-tires`, ...); `slug` is browse input, `name` the category filter of search and vehicle-tires.
- `/suggestions` `{"q": "michelin"}`: 3 models (`model_id` for `/model`) and 9 categories with counts. No prices.
- `/appointments` `{"store_code": "1009"}`: November at store 1009, 7 days: "Walkins Welcome" days with no slots, Thanksgiving Day, 8 open slots on 2026-11-27, 24 on 2026-11-28, "Store Closed" on Sunday 2026-11-29, 27 on 2026-11-30. `slots` {`start`, `end`} are as Discount Tire gives them with a `Z` suffix; in the capture they fall inside the store's local opening hours (09:15 to 17:00 on a day Discount Tire lists 8:00 AM to 6:00 PM at an Arizona store), so compare them with `opens` / `closes` before converting time zones. Read only: Scavio never books.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def discounttire(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/discounttire/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()

# 1. Tires in one size at one store, lowest price first (1 credit)
hits = discounttire("search", {"size": "225/65R17", "store": "1009", "sort": "price_low"})["data"]
store = hits["store"]
for i in hits["items"][:5]:
    # price is per tire; 4 x price is arithmetic, not a Discount Tire set price.
    print(i["item_number"], i["brand"], i["model"], f'${i["price"]:.2f} per tire',
          f'(4 x = ${4 * i["price"]:.2f}, arithmetic)', "units", i["stock"]["units"] if i["stock"] else None)
print("store", store["store_code"], store["brand"], store["city"], store["state"])

# 2. The same tire at another store (1 credit each)
for code in ["1009", "1752"]:
    p = discounttire("product", {"item_number": "108547", "store": code})["data"]
    print(code, p["store"]["brand"], p["price"], [x["title"] + " (" + x["condition"] + ")" for x in p["promotions"]])

# 3. Units at the stores near a ZIP (1 credit per page of 5)
stock = discounttire("store-stock", {"item_number": "108547", "zip": "85251"})["data"]
for s in stock["stores"]:
    print(s["store_code"], s["distance_miles"], [(x["units"], x["message"]) for x in s["stock"]])

# Prices and units can change between calls. Store each answer with fetched_at
# and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` {`country`, `language`, `currency`, `locale`} and most carry `notes`.

- **item** (search, vehicle-tires, wheels, browse) - `position`, `item_number`, `type` (`tire`, `wheel`, or `model` with `price_range` and `item_numbers`), `model_id`, `brand`, `model`, `name`, `description`, `size`, `price`, `price_text`, `price_range`, `markdown`, `map_price`, `map_display_rule`, `promotions[]` {`title`, `text`, `description`, `ends`, `ends_text`, `group`, `condition`, `url`}, `rating`, `review_count`, `recommend_count`, `stock` {`store_code`, `units`, `message`, `available_date`, `days_out`}, `gtin`, `manufacturer_part_number`, `mileage_warranty`, `tier`, `categories`, `original_equipment`, `image`, `url`, `category_ratings`; wheels add `wheel` {`diameter`, `width`, `color`, `finish`, `vendor_finish`} and `finishes`; vehicle-tires adds `position_on_vehicle`, or for staggered pairs {`position`, `pair`, `front`, `rear`, `url`, `price_note`}, and with `ranking` `treadwell` a `treadwell` object.
- **lists** - `store`, `page`, `page_size`, `total`, `total_pages`, `count`, `sort`, `filters_applied`, `resolved_filters[]` {`input`, `requested`, `label`, `filter`}, `items[]`, `facets[]` {`key`, `name`, `values[]` {`label`, `count`, `filter`, `selected`}} (send `filter` back in `filters`). Search adds `size`, `rear_size`; vehicle-tires `vehicle`, `staggered`, `position`, `ranking`; wheels `diameter`, `width`, `bolt_pattern`; browse `category`, `brand`, `q`, `product_type`.
- **vehicle** - `step` (`years`, `makes`, `models`, `trims`, `assemblies`, `fitment`), `count`, `options[]` ({`year`}, {`make`}, {`vehicle_id`, `model`}, {`trim_id`, `trim`}, {`assembly_id`, `description`, `staggered`, `front_size`, `rear_size`}), `next`; the fitment step `fitment` {`vehicle` {`vehicle_id`, `year`, `make`, `model`, `type`, `image`}, `trim` {`trim_id`, `name`, `category`}, `assembly_id`, `front_size`, `rear_size`, `staggered`, `front_wheel_diameter`, `rear_wheel_diameter`, `ride_height`, `drive`, `lug_torque`, `optional_sizes[]` {`wheel_diameter`, `axle`, `sizes[]` {`size`, `fit`}}, `optional_staggered_sets`}.
- **product** - the item fields plus `requested_item_number`, `tire` {`load_index`, `load_index_speed`, `speed_rating`, `load_range`, `utqg` {`treadwear`, `traction`, `temperature`}, `tread_depth`, `max_pressure`, `overall_diameter`, `section_width`, `aspect_ratio`, `rim_diameter`, `rim_width_range`, `sidewall`, `run_flat`} or `wheel` {`diameter`, `width`, `bolt_pattern`, `bolts`, `offset`, `hub_bore`, `finish`, `color`, `load_capacity`}, `weight`, `faqs[]` {`question`, `answer`, `type`}, `long_description`, `images`, `nearby_store_stock`, `no_longer_available`.
- **model** - `store`, `requested_model_id`, `product_type`, `model_id`, `brand`, `model`, `name`, `type`, `rating`, `review_count`, `price_range`, `promotions`, `tier`, `categories`, `item_count`, `items[]` {`item_number`, `price`}, `size_options[]` {`key`, `options`}, `spec_ranges[]` {`name`, `range`}, `default_item`, `long_description`, `image`, `url`.
- **store-stock** - `item_numbers`, `quantity`, `zip`, `radius_miles`, `sort`, `page`, `page_size`, `total`, `total_pages`, `count`, `my_store`, `stores[]` {`store_code`, `brand`, `name`, `address` {`line1`, `line2`, `city`, `state`, `zip`, `country`}, `phone`, `latitude`, `longitude`, `distance_miles`, `stock[]` {`item_number`, `units`, `message`}}.
- **stores** - `location`, `radius_miles`, `page`, `page_size`, `total`, `total_pages`, `count`, `stores[]` {`position`, `store_code`, `brand`, `name`, `location_name`, `legacy_code`, `address`, `phone`, `latitude`, `longitude`, `distance_miles`, `rating`, `review_count`, `services`}.
- **store** - the store fields plus `cleanliness_rating`, `knowledge_rating`, `recommended_count`, `recommended_percent`, `rating_breakdown[]` {`stars`, `count`}, `hours[]` {`date`, `open`, `close`, `closed`, `note`, `holiday`}, `store_services`, `features`, `images`, `nearby_stores[]` {`store_code`, `distance_miles`, `address`, `phone`, `rating`, `review_count`}, `current_time`.
- **reviews** - `item_number`, `scope`, `sort`, `rating_filter`, `rating`, `review_count`, `recommend_count`, `rating_breakdown[]` {`stars`, `count`}, `page`, `page_size`, `total`, `total_pages`, `count`, `reviews[]` {`id`, `rating`, `text`, `date`, `recommended`, `helpful_votes`, `unhelpful_votes`, `category_ratings`, `pros`, `cons`, `state`, `vehicle`}.
- **store-reviews** - `store_code`, `sort`, `rating_filter`, `rating_breakdown`, `page`, `page_size`, `total`, `total_pages`, `count`, `reviews[]` {`id`, `rating`, `text`, `date`, `recommended`, `helpful_votes`, `unhelpful_votes`, `category_ratings` {`overall`, `cleanliness`, `knowledge`}}.
- **categories** - `type`, `count`, `categories[]` {`code`, `name`, `slug`, `description`, `groups`, `url`, `image`}.
- **suggestions** - `q`, `products[]` {`model_id`, `item_number`, `brand`, `model`, `description`, `type`, `url`, `image`}, `categories[]` {`code`, `name`, `count`}.
- **appointments** - `store_code`, `month`, `count`, `days[]` {`date`, `day_of_week`, `bookable`, `message`, `holiday`, `opens`, `closes`, `slot_count`, `slots[]` {`start`, `end`}}.

## Guardrails

- Name it "Discount Tire (discounttire.com, the US tire and wheel retailer, America's Tire in parts of CA, PA, NJ and NY)" on first mention. America's Tire is the same company; Tire Rack (a sister company) and Mavis Discount Tire (a different company) are not read.
- Prices: quote `price` as the price per tire at the store in `store`, with the store code, city and the `fetched_at` date. Never present a price as national or as every store's; never claim every store differs.
- Set of four: there is no set price field. Show 4 x `price` (or 2 front + 2 rear for a staggered set) as labelled arithmetic. Never compute a price after a promotion or rebate.
- Promotions: quote Discount Tire's `title` or `text` and the end date exactly as given, say when `condition` is `MYACCOUNT` that a Discount Tire account may be needed, and never add urgency or countdown wording.
- Never state installation, disposal, road hazard, certificate or other fee amounts: no endpoint returns them. Never discuss recalls, lawsuits, safety verdicts or price trends.
- OE and Treadwell: `original_equipment` is Discount Tire's flag; Treadwell fields are Discount Tire's estimates. Never present either as Scavio's recommendation or test.
- Comparing Discount Tire with Walmart, Sam's Club or Amazon: the same tire only (brand, model, size, load index, speed rating, and the GTIN or manufacturer part number), each price with its retailer, store and date. Never call one retailer cheaper beyond the numbers shown.
- Stock: `units` and `message` as Discount Tire reported them at the moment of the call; Scavio makes no promise of their accuracy. Never promise pickup, installation or a date.
- Appointments: read only. Never say a slot is booked or held.
- Reviews: no reviewer names are returned. Do not republish Discount Tire product photos or logos; link products by `url` instead.
- Terms: Scavio does not collect or store Discount Tire data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Discount Tire's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, units, item numbers, store codes, vehicle ids, GTINs, dates or ratings. Only return what the API returned, with the `fetched_at` time and the product `url`.
- Not available: a set-of-four price field, the deals page text, installation and fee amounts, road hazard and certificate prices, financing, Treadwell's chat, fleet accounts, Tire Rack, price history (poll and store), booking, cart or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a price endpoint without `store` or `zip`, or with both; a `country` other than `us` or a `language` other than `en`; search without `size` (or `width` + `aspect_ratio` + `diameter`); `make` without `year`; `assembly_id` without `trim_id` and `vehicle_id`; vehicle-tires without all three ids; store-stock without `zip` or an item, more than 4 `item_numbers`, or a `radius` other than 10, 25, 50, 75 or 150; stores without `zip`, `city` or `latitude` + `longitude`, or a point outside the United States; store, store-reviews or appointments without `store_code`; wheels by size without all of `diameter`, `width` and `bolt_pattern`, or a bolt pattern not written like `6-135`, `6x139.7` or `5x4.5`; browse without one of `category`, `brand` or `q`, or with wheels; suggestions with fewer than 3 characters; `min_price` above `max_price`; an unknown `sort`, `scope`, `position` or `ranking`; more than 10 `nearby_stores`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Discount Tire has no item <item>.", "Discount Tire has no store <code>. stores lists them (stores[].store_code).", "Discount Tire lists no Discount Tire or America's Tire store near <zip>.", "Discount Tire has no fitment for vehicle <id>, trim <id>, assembly <id>. ...", "Discount Tire lists no <make> models for <year>. ...", "Discount Tire has no tire or wheel model <id>. ...", "Discount Tire has no tires category <slug>. categories lists the slugs.", "Discount Tire lists no tire brand \"<brand>\".". A store-stock search with no store in the radius answers 200 with `total` 0 and a note suggesting a larger radius (up to 150). Take item numbers, store codes, vehicle ids, slugs and filters from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api).
- `502` means Discount Tire data was temporarily unavailable ("Discount Tire is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Discount Tire is busy ("Discount Tire is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.85.0
npm install scavio@0.86.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.discounttire.search({ size: "225/65R17", store: "1009" });
const { data: years } = await scavio.discounttire.vehicle({});
const { data: sizes } = await scavio.discounttire.vehicle({ vehicle_id: "17361", trim_id: "52455" });
const { data: fits } = await scavio.discounttire.vehicleTires({ vehicle_id: "17361", trim_id: "52455", assembly_id: "0000E28B", store: "1009" });
const { data: tire } = await scavio.discounttire.product({ item_number: "108547", store: "1009" });
const { data: sizesOfModel } = await scavio.discounttire.model({ model_id: "michelin-defender-2", store: "1009" });
const { data: stock } = await scavio.discounttire.storeStock({ item_number: "108547", zip: "85251" });
const { data: stores } = await scavio.discounttire.stores({ zip: "85251" });
const { data: store } = await scavio.discounttire.store({ store_code: "1009" });
const { data: reviews } = await scavio.discounttire.reviews({ item_number: "108547", sort: "most_helpful" });
const { data: storeReviews } = await scavio.discounttire.storeReviews({ store_code: "1009" });
const { data: wheels } = await scavio.discounttire.wheels({ diameter: "20", width: "9", bolt_pattern: "6-135", store: "1009" });
const { data: allSeason } = await scavio.discounttire.browse({ category: "all-season-tires", store: "1009" });
const { data: cats } = await scavio.discounttire.categories();
const { data: suggest } = await scavio.discounttire.suggestions({ q: "michelin" });
const { data: slots } = await scavio.discounttire.appointments({ store_code: "1009" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.discounttire.search(...)`, `vehicle`, `vehicle_tires`, `product`, `model`, `store_stock`, `stores`, `store`, `reviews`, `store_reviews`, `wheels`, `browse`, `categories`, `suggestions` and `appointments`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 15 endpoints as tools: `search_discounttire`, `get_discounttire_vehicle`, `get_discounttire_vehicle_tires`, `get_discounttire_product`, `get_discounttire_model`, `get_discounttire_store_stock`, `get_discounttire_stores`, `get_discounttire_store`, `get_discounttire_reviews`, `get_discounttire_store_reviews`, `get_discounttire_wheels`, `get_discounttire_browse`, `get_discounttire_categories`, `get_discounttire_suggestions` and `get_discounttire_appointments`. Discount Tire is opt-in: add `discounttire` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.85.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,discounttire"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/discounttire-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [vehicle](https://scavio.dev/docs/discounttire-vehicle?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [vehicle tires](https://scavio.dev/docs/discounttire-vehicle-tires?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [product](https://scavio.dev/docs/discounttire-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [model](https://scavio.dev/docs/discounttire-model?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [store stock](https://scavio.dev/docs/discounttire-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [stores](https://scavio.dev/docs/discounttire-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [store](https://scavio.dev/docs/discounttire-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [reviews](https://scavio.dev/docs/discounttire-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [store reviews](https://scavio.dev/docs/discounttire-store-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [wheels](https://scavio.dev/docs/discounttire-wheels?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [browse](https://scavio.dev/docs/discounttire-browse?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [categories](https://scavio.dev/docs/discounttire-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [suggestions](https://scavio.dev/docs/discounttire-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api), [appointments](https://scavio.dev/docs/discounttire-appointments?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api). Overview: [Discount Tire API](https://scavio.dev/discounttire-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=discount-tire-prices-api).
