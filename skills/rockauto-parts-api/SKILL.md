---
name: rockauto-parts-api
description: RockAuto API for RockAuto (rockauto.com, the online auto parts catalog based in Madison, Wisconsin) - auto parts prices by vehicle across every brand RockAuto lists for a part type, each listing with brand, part number, RockAuto's tier label (Economy, Daily Driver, Premium, High Performance, Heavy Duty), RockAuto's fitment notes (front or rear, trim, material), price, core charge, pack options, closeout, out-of-stock, remaining and non-stock labels, RockAuto's popular mark and the OE / interchange numbers it replaces (brake pads for a 2010 Honda Accord 2.4L L4 read 114 listings from 10.23 to 59.79 USD on Nov 26, 2026); part number and interchange search across brands (an OE, FRAM or Bosch number finds the listings RockAuto maps to it); one brand's parts of one part type (RockAuto lists up to 50); one part's detail with specifications, OE numbers, warranty and the manufacturer's text; the vehicle chain (makes, years, models, engines with RockAuto's carcode) and a vehicle's categories and part types; search box suggestions and free text read as a vehicle; the tools and universal parts catalog; the promotions and manufacturer rebates page with printed expiry dates; the 568-brand list and 5,463 part types. One US catalog shown in 15 display currencies (BOSCH BP1084 read 29.79 USD, 22.74 GBP and 583.71 MXN) and in English, Spanish, French or German (part detail in English). 11 endpoints, 1 credit per call. No reviews, stores, shipping cost, price history, sort or paging.
version: 1.0.0
tags: rockauto, rockauto-com, rockauto-api, rockauto-parts, rockauto-parts-api, rockauto-prices, rockauto-catalog, rockauto-part-number, rockauto-interchange, rockauto-closeout, rockauto-rebates, rockauto-promotions, rockauto-carcode, rockauto-brands, auto-parts, auto-parts-api, car-parts-api, auto-parts-prices, parts-by-vehicle, vehicle-fitment, part-number-search, oe-numbers, interchange, cross-reference, aftermarket-parts, brake-pads, spark-plugs, oil-filters, tools, price-comparison, price-monitoring, usd, cad, eur, gbp, mxn, multi-currency, spanish, french, german, ai-agents, structured-data, json, mcp
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/rockauto-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api
---

# RockAuto API - Auto Parts Prices by Vehicle, Part Number Search, Brands

Read RockAuto (rockauto.com, the online auto parts catalog based in Madison, Wisconsin): the vehicle chain from make to engine, a vehicle's categories and part types, every brand's listing for one part type on one vehicle, part number and interchange search, one brand's parts of a part type, one part's detail page, RockAuto's brand list, search box suggestions, free text read as a vehicle, the tools and universal parts catalog and the promotions and rebates page. All 11 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public catalog pages RockAuto shows to any visitor and returns them as JSON for analysis. It uses no RockAuto account, no cart and no checkout.

**The job this skill is for: RockAuto's price ladder for one part on one vehicle, every brand and tier, next to the store retailers.** RockAuto lists many brands for one part type and groups them by its own tier labels. Captured 2026-11-26 with `/parts` (1 credit), brake pads (`part_type_id` 1684) for a 2010 Honda Accord 2.4L L4 (`carcode` 1444945) returned 114 listings, front and rear together:

| RockAuto tier | Listings | Lowest (brand, part number, axle) | Highest |
|---|---|---|---|
| Economy | 29 | FMG PSG787, front, 10.23 USD (closeout) | ACDELCO 14D1506CHF1, 33.79 |
| Daily Driver | 59 | CENTRIC 30109140, front, 12.65 | BREMBO P28035X, 57.79 |
| Heavy Duty (Long Life, Truck & Tow) | 3 | CENTRIC 10613360, rear, 13.01 | POWER STOP Z36914, 35.99 |
| Premium | 15 | BOSCH BC1451, rear, 23.79 | POWER STOP Z23787, 55.79 |
| High Performance | 8 | DYNAMIC FRICTION 1115145100, rear, 31.89 | DYNAMIC FRICTION 1115150601, 59.79 |

Front and rear pads sit in one list: the axle is in each listing's `notes` ("Front; ..." or "Rear"), so split on `notes` before comparing. Then read the same brand and part number at AutoZone (`autozone-api`, priced for one store) or O'Reilly (`oreilly-auto-parts-api`) and put each price with its retailer and date. RockAuto prices exclude shipping, which RockAuto prices per warehouse in the cart and this skill does not read; say so next to every RockAuto price.

Ten limits shape every answer, so say them plainly:
- **1 credit per call.** A not-found (an unknown make, year, model, category, part type or part keys) is a `404` and is charged. A refused input (`400`), including a carcode that answers another vehicle, and an upstream failure (`502`, `503`) are not charged.
- **carcode decides the vehicle.** `/categories` and `/parts` need `make`, `year`, `model`, `engine` and `carcode` sent together exactly as `/vehicles` answers them for an engine (or a `/suggestions` vehicle with its `carcode`). A carcode that answers another vehicle is a `400`, not charged ("carcode 1503315 is a 2012 SUBARU OUTBACK 3.6L H6 on RockAuto, not the 2012 BMW 328I 2.0L L4 TURBOCHARGED you sent").
- **No sort and no paging.** `/parts`, `/search`, `/brand` and the `/tools` listing come back whole in RockAuto's own order (grouped by tier on `/parts`); `count` is the list. Sort and filter the items yourself.
- **Brand browse stops at 50.** `/brand` returns at most 50 of a brand's parts for one part type, with `limited` true and RockAuto's notice ("Results may be limited due to size of query..."). For a full list use `/parts` for a vehicle or `/search` by part number.
- **One US catalog, 15 display currencies.** `currency` (USD default, AUD, BRL, GBP, CAD, CLP, EUR, HUF, JPY, MXN, NZD, NOK, PLN, SEK, CHF) changes how RockAuto prints the price, converted by RockAuto; it is the same US catalog, not a local store. BOSCH BP1084 read 29.79 USD, 22.74 GBP and 583.71 MXN on Nov 26, 2026. Promotions are always in USD.
- **Four languages, part detail in English.** `language` `en`, `es`, `fr` or `de` translates names, tiers, notes and labels (`Économique`, `Preiswert`); part numbers and prices do not change. `/part` is in English in every language.
- **Labels as RockAuto prints them.** `closeout_text` ("Wholesaler Closeout -- 30 Day Warranty"), `remaining_text` ("Only 1 Remaining"), `non_stock_text` ("Non-stock item--shipping delayed up to 1 business days") and `tier` are RockAuto's wording. Quote them; never turn "Only 1 Remaining" into a stock count beyond what it says.
- **A price can be null.** An item RockAuto prints no price for reads `price` null (part number 0986494104 did in a GBP / Spanish search). Report it as no price shown, not as zero.
- **Slow on big part types.** `/parts` answered brake pads in about 7 seconds in the capture, but RockAuto can take 80-100 seconds on a large part type. Set a client timeout of 240 seconds.
- **What is not there.** No reviews (RockAuto has none), no stores or store stock (RockAuto has no stores), no buyer's guide, no shipping cost (needs a cart), no coupon codes (RockAuto publishes none), no price history (store your own answers with `fetched_at`), no cart or checkout.

RockAuto publishes no public API for its catalog or prices, and no affiliate product feed was found. This skill reads RockAuto's public catalog pages with one Scavio key.

RockAuto, LLC (Madison, Wisconsin) describes itself on rockauto.com as an online-only family business founded in 1999. Quote that with its source, never as a Scavio figure.

See also: `autozone-api` (AutoZone prices by vehicle, priced for one store, with core charge and pickup), `oreilly-auto-parts-api` (O'Reilly cross-reference, prices and store stock) and `discount-tire-prices-api` (tire prices by store and vehicle fitment). Same part only: match the brand and part number (or an OE / interchange number both list), keep front and rear apart, and show each price with its retailer, store where there is one, and date.

## When to trigger

Use this skill when the user asks to:
- List every brand RockAuto carries for one part on one vehicle (brake pads, rotors, spark plugs, oil filters, struts), with prices and RockAuto's tiers
- Put a RockAuto price next to AutoZone or O'Reilly for the same brand and part number
- Look up a part number or an OE / interchange number on RockAuto and see which brands' listings it maps to
- Read one RockAuto part in full: specifications, OE numbers, warranty, the manufacturer's description
- Walk RockAuto's vehicle catalog: makes, years, models, engines and the carcode, then the vehicle's categories and part types
- Turn free text ("2010 honda accord brake pads") into a RockAuto vehicle, or read RockAuto's search suggestions
- Browse RockAuto's tools and universal parts, or one brand's parts of a part type
- Read RockAuto prices in another display currency (CAD, EUR, GBP, MXN ...) or with Spanish, French or German labels
- List RockAuto's current promotions and manufacturer rebates with their printed expiry dates

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls: about a dozen vehicles walked from make to a part type's full listing.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, vehicles, resolve and tools answered in about 1 second, categories, brands, brand and part in about 2, search 2-6, parts 7, promotions 1-16 and suggestions 3-18 (the list of every make took 17). Large part types can take 80-100 seconds: set a client timeout of 240 seconds and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/rockauto/vehicles` | The vehicle chain one level at a time: makes, a make's years, a year's models, a model's engines with `carcode` | 1 |
| `POST /api/v1/rockauto/categories` | One vehicle's part categories, or one category's part types with `part_type_id` | 1 |
| `POST /api/v1/rockauto/parts` | Every brand's listing for one part type on one vehicle: price, tier, notes, core charge, closeout and stock labels, OE / interchange numbers | 1 |
| `POST /api/v1/rockauto/search` | Part number and interchange search across brands, optionally narrowed by brand or part type | 1 |
| `POST /api/v1/rockauto/brand` | One brand's parts of one part type (at most 50) | 1 |
| `POST /api/v1/rockauto/brands` | RockAuto's 568 brands and 26 part groups; with `include_part_types`, the 5,463 part type ids | 1 |
| `POST /api/v1/rockauto/part` | One part's detail: price, specifications, OE numbers, warranty, disclaimer, manufacturer text, images | 1 |
| `POST /api/v1/rockauto/suggestions` | RockAuto's search box suggestions: vehicles with carcode, part types, tools, help articles | 1 |
| `POST /api/v1/rockauto/resolve` | Free text read the way RockAuto's search box reads it: vehicle, part type, the words it did not interpret | 1 |
| `POST /api/v1/rockauto/tools` | Tools and universal parts: categories, subcategories, part types, then a part type's listing | 1 |
| `POST /api/v1/rockauto/promotions` | RockAuto's promotions and manufacturer rebates with printed expiry dates, and its recently expired list | 1 |

## Markets

RockAuto runs one US catalog. `markets` on a vehicle (`us`, `ca`, `mx`) are the vehicle markets RockAuto lists the vehicle for, and `fits_markets` on a listing the markets the part is listed as fitting. There is no `country` input.

- `currency`: USD (default), AUD, BRL, GBP, CAD, CLP, EUR, HUF, JPY, MXN, NZD, NOK, PLN, SEK or CHF, on parts, search, brand, part and tools. Echoed in every answer and on every item. RockAuto converts for display; the catalog and part numbers are the same.
- `language`: `en` (default), `es`, `fr` or `de`, on every endpoint except part, suggestions and resolve. `category` keeps its English input value (`category` "Engine", `category_name` "Moteur").

## Listings and prices

| Field | Meaning |
|---|---|
| `price`, `price_text` | RockAuto's price in the requested currency, and the price as printed (`$10.23`, `(€4.79/Each)`, `Mex$583.71`); `null` when RockAuto prints none |
| `price_per`, `pack_size`, `total`, `pack_options[]` | Per-unit wording (`Each`), the pack size, the pack total and RockAuto's pack choices {`pack_size`, `price_each`, `total`, `selected`} |
| `core_charge` | The core charge RockAuto adds, `0` when none |
| `tier` | RockAuto's tier label on `/parts` and `/tools` (Economy, Daily Driver, Premium, High Performance, Heavy Duty (Long Life, Truck & Tow); for spark plugs, Iridium / Platinum / Copper / Nickel). `null` on search and brand |
| `notes[]` | RockAuto's fitment notes: axle, trim, material, emissions ("Front; Ceramic; Includes Pad Installation Hardware; EX or EX-L") |
| `closeout`, `closeout_text` | RockAuto's closeout mark and its wording ("Wholesaler Closeout -- 30 Day Warranty") |
| `out_of_stock`, `remaining`, `remaining_text`, `non_stock_text`, `shipping_delay_days` | RockAuto's stock labels as printed ("Only 1 Remaining", "Non-stock item--shipping delayed up to 2 business days" with `shipping_delay_days` 2) |
| `popular` | RockAuto's most-popular mark |
| `alternate_numbers[]` | OE and alternate numbers the listing replaces (NGK 97390 listed 20, among them `12290R40A01`) |
| `part` {`part_key`, `carcode`, `part_type_id`} | The input of `/part` (`carcode` "0" from search, brand and tools) |
| `info_url`, `image` | RockAuto's detail link and image |

- **Prices exclude shipping.** RockAuto prices shipping per warehouse in the cart; it is not read. Write "before shipping" next to every RockAuto price.
- **Front and rear.** One brake list mixes axles; read the axle from `notes` and compare front with front.
- **Tiers are RockAuto's.** Report `tier` as RockAuto's label, not as a quality rating of the brand.

## Workflow

1. **Find the vehicle.** `/suggestions` with `"2015 ford f-150"` returns each engine with `carcode` (four F-150 engines, `5.0l v8` carcode 3308775), or walk `/vehicles`: no input, then `make`, then `make` + `year`, then `make` + `year` + `model` for the engines. Use the engine row's `make`, `year`, `model`, `engine` and `carcode` exactly as given (`/vehicles` answers upper case, HONDA / ACCORD; suggestions answer lower case).
2. **Find the part type.** `/categories` with the vehicle for its categories, then with `category` ("Brake & Wheel Hub") for its part types (Brake Pad 1684 among 30).
3. **Read the listing.** `/parts` with the vehicle, `category` and `part_type_id`. Split by axle from `notes`; group by `tier`; read `price`, `core_charge`, `closeout_text` and `remaining_text`.
4. **Check a part number.** `/search` with `part_number` (and `brand` or `part_type_id` to narrow): RockAuto matches its brands' numbers and the OE / interchange numbers it maps (PH7317, a FRAM number, found one listing, VARIOUS MFR PG4612, in a French / CAD search).
5. **Read the part.** `/part` with the item's `part` keys for specifications, OE numbers, warranty and the disclaimer ("Brake Pads are sold as a set. Quantity of one (1) is for both wheels").
6. **Match elsewhere.** `autozone-api` or `oreilly-auto-parts-api` with the same brand and part number, or a shared OE number. Skip rows that do not match exactly.
7. **Report.** Each price with RockAuto, the vehicle, the axle, the currency, "before shipping" and the `fetched_at` date.
8. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Vehicle inputs (`/categories`, `/parts`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `make` | string | required | As `/vehicles` answers it (`engines[].make`, e.g. `HONDA`) |
| `year` | integer | required | Model year, 1900-2100 |
| `model` | string | required | As `/vehicles` answers it (`ACCORD`) |
| `engine` | string | required | As `/vehicles` answers it (`2.4L L4`) |
| `carcode` | string or integer | required | RockAuto's vehicle code (`1444945`); decides the vehicle |
| `category` | string | optional on categories, required on parts | `categories[].category` (`Brake & Wheel Hub`) |
| `part_type_id` | string or integer | required on parts | `part_types[].part_type_id` (`1684` = Brake Pad) |
| `part_type` | string | none | Optional part type name; RockAuto reads the id |
| `language` | string | `en` | `en`, `es`, `fr` or `de` |
| `currency` | string | `USD` | Parts only: one of the 15 currencies |

### The other endpoints

| Endpoint | Parameters |
|---|---|
| `/vehicles` | none (makes), `make` (years), `make` + `year` (models), `make` + `year` + `model` (engines with carcode); `language` |
| `/search` | `part_number` (required, up to 60 chars: letters, digits, `- . / #`), `brand` (a `/brands` name), `part_type_id`, `language`, `currency` |
| `/brand` | `brand` (required, a `/brands` name such as `BOSCH`), `part_type_id` (required), `language`, `currency` |
| `/brands` | `include_part_types` (true adds about 5,500 part type ids and names), `language` |
| `/part` | `part_key` and `part_type_id` (required, from `items[].part`), `carcode` (`items[].part.carcode`, `0` from search, brand and tools), `currency` |
| `/suggestions` | `query` (required, 2-100 chars: a vehicle, a part type or a tool) |
| `/resolve` | `query` (required, 3-150 chars: free text naming a vehicle and optionally a part) |
| `/tools` | none (categories), `category` (subcategories), `category` + `subcategory` (part types), or `part_type_id` (that part type's listing); `language`, `currency` |
| `/promotions` | `language` |

## Examples

### Every brand's brake pads for one vehicle

```bash
curl -X POST https://api.scavio.dev/api/v1/rockauto/parts \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "HONDA", "year": 2010, "model": "ACCORD", "engine": "2.4L L4", "carcode": "1444945", "category": "Brake & Wheel Hub", "part_type_id": "1684"}'
```

Captured `data` (2026-11-26; `items` cut to 2 of 114, `image`, `info_url` and `notes` dropped at the end):

```json
{
  "language": "en",
  "currency": "USD",
  "vehicle": {"make": "HONDA", "year": 2010, "model": "ACCORD", "engine": "2.4L L4", "carcode": "1444945"},
  "category": "Brake & Wheel Hub",
  "category_name": "Brake & Wheel Hub",
  "part_type": {"part_type_id": "1684", "name": "Brake Pad"},
  "count": 114,
  "items": [
    {"position": 1, "brand": "FMG", "part_number": "PSG787", "description": null, "part_type": null, "part_type_id": "1684", "notes": ["Front; Housing: YES; Includes: Hardware Kit, Grease Pack; Service Grade; Material: Ceramic; EX; EX-L"], "tier": "Economy", "price": 10.23, "price_text": "$10.23", "price_per": null, "core_charge": 0, "pack_size": 1, "total": 10.23, "pack_options": [], "currency": "USD", "out_of_stock": false, "closeout": true, "closeout_text": "Wholesaler Closeout -- 30 Day Warranty", "non_stock_text": null, "shipping_delay_days": null, "remaining": null, "remaining_text": null, "popular": false, "fits_markets": ["us", "ca"], "alternate_numbers": [], "part": {"part_key": "18572429", "carcode": "1444945", "part_type_id": "1684"}},
    {"position": 2, "brand": "PRO LINE", "part_number": "PS787C", "description": null, "part_type": null, "part_type_id": "1684", "notes": ["Front; Ceramic; Includes Pad Installation Hardware; EX or EX-L"], "tier": "Economy", "price": 10.87, "price_text": "$10.87", "price_per": null, "core_charge": 0, "pack_size": 1, "total": 10.87, "pack_options": [], "currency": "USD", "out_of_stock": false, "closeout": true, "closeout_text": "Wholesaler Closeout -- 30 Day Warranty", "non_stock_text": null, "shipping_delay_days": null, "remaining": null, "remaining_text": null, "popular": false, "fits_markets": ["us", "ca"], "alternate_numbers": []}
  ]
}
```

Of the 114 listings, 59 were Daily Driver, 29 Economy, 15 Premium, 8 High Performance and 3 Heavy Duty; 4 were closeouts, 6 carried RockAuto's popular mark (DURAGO BP1336C at 12.28, AKEBONO ACT1336A at 40.79 ...), four read "Only 1 Remaining" and three were non-stock items with a 1 or 2 business day delay. The same call with `"currency": "EUR"` and part type 7212 (Spark Plug, category Ignition) returned 12 listings from NGK 97390 at €4.79 each.

### Part number search

```bash
curl -X POST https://api.scavio.dev/api/v1/rockauto/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"part_number": "BP1084"}'
```

Captured `data` (2026-11-26; `image`, `info_url` and `notes` dropped):

```json
{
  "language": "en",
  "currency": "USD",
  "part_number": "BP1084",
  "brand": null,
  "part_type_id": null,
  "search_label": "Search for Part Number='BP1084'",
  "limited": false,
  "limited_notice": null,
  "count": 1,
  "items": [
    {"position": 1, "brand": "BOSCH", "part_number": "BP1084", "description": null, "part_type": "Brake Pad", "part_type_id": "1684", "notes": [], "tier": null, "price": 29.79, "price_text": "$29.79", "core_charge": 0, "pack_size": 1, "total": 29.79, "currency": "USD", "out_of_stock": false, "closeout": false, "popular": false, "alternate_numbers": [], "part": {"part_key": "6129207", "carcode": "0", "part_type_id": "1684"}}
  ]
}
```

With `"language": "es", "currency": "MXN"` the same part read `Mex$583.71` (`part_type` "Pastilla de Freno"). Part number `41-110` in German / EUR matched 5 listings across part types (a PA CARGO clutch disc at €5.01, an ACDELCO 41110 spark plug at €5.33, a GATES water pump at €39.04 ...): RockAuto matches numbers across brands, so check `part_type` and `brand` before using a match. A number with no match returns `count` 0 in a `200`.

### One part's detail

```bash
curl -X POST https://api.scavio.dev/api/v1/rockauto/part \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"part_key": "6129207", "part_type_id": "1684", "carcode": "0"}'
```

Captured `data` (2026-11-26; `specifications` cut to 3 of 14, `more_information`, `images` and `notes` dropped):

```json
{
  "language": "en",
  "requested": {"part_key": "6129207", "carcode": "0", "part_type_id": "1684"},
  "brand": "BOSCH",
  "part_number": "BP1084",
  "title": "More Information for BOSCH BP1084",
  "part": {"part_key": "6129207", "carcode": "0", "part_type_id": "1684"},
  "price": 29.79,
  "price_text": "$29.79",
  "price_per": null,
  "core_charge": 0,
  "pack_size": 1,
  "total": 29.79,
  "pack_options": [],
  "currency": "USD",
  "out_of_stock": false,
  "description": "QuietCast Semi-Metallic",
  "specifications": [
    {"name": "Friction Material Composition", "value": "Semi-Metallic"},
    {"name": "Pad Quantity", "value": "4"},
    {"name": "Slotted", "value": "Yes"}
  ],
  "oe_numbers": [],
  "alternate_numbers": [],
  "warranty": ["12 Months"],
  "warranty_url": null,
  "disclaimer": "Brake Pads are sold as a set. Quantity of one (1) is for both wheels"
}
```

With `"currency": "GBP"` the same part read £22.74. An NGK 4912 spark plug in JPY read `(¥1,480.25/Each)` with `oe_numbers` 19185438, 9091901253 and 9091901275 and `warranty` "2 Months".

### Vehicles, categories, suggestions, resolve, brand, brands, tools, promotions

- `/vehicles` `{"make": "HONDA", "year": 2010, "model": "ACCORD"}`: `level` engines, 2 engines, `2.4L L4` carcode 1444945 and `3.5L V6` carcode 1444944, each with `markets` us, ca, mx.
- `/categories` with that vehicle and `"category": "Brake & Wheel Hub"`: `level` part_types, 30 part types (ABS Wheel Speed Sensor 1912, Brake Bleeder Screw 1676, Brake Fluid 11389, Brake Hose 1792, Brake Pad 1684, Caliper 1704 ...).
- `/suggestions` `{"query": "2015 ford f-150"}`: 4 vehicles, each with `carcode`: 2.7l v6 turbocharged 3308772, 3.5l v6 3308774, 3.5l v6 turbocharged 3308773, 5.0l v8 3308775.
- `/resolve` `{"query": "2010 honda accord brake pads"}`: 2 matches, the 2010 accord and the 2010 accord crosstour, both without engine or carcode and with `leftover` "brake pads": take the engines from `/vehicles`.
- `/brand` `{"brand": "BOSCH", "part_type_id": "1684"}`: 50 items (the cap), `limited` true, from BOSCH BE905AH at 12.99 to 24.79.
- `/brands`: `count` 568 brands (3D, 3M, 555, A-1 CLUTCH COMPANY, ...), 26 `part_groups` (Brake & Wheel Hub, Engine, Ignition, Suspension ...), `part_type_count` 5463.
- `/tools` `{"category": "Brake & Wheel Hub", "subcategory": "Tool"}`: 28 part types (Air Brake Bolt Wrench 1002188, Brake Bleeder Kit 1000608 ...). `{"part_type_id": "1000891", "language": "es", "currency": "MXN"}` listed 24 tools, the first PERFORMANCE TOOL W80621 at Mex$99.93.
- `/promotions`: `read_date` 2026-11-26, 8 promotions: Wholesaler Closeout Parts, AutoMeter "Get Up To $150 CASH BACK!" (`expires_text` "Offer expires 12/31/26", `expires` 2026-12-31, with its rebate form link), Power Stop instant 10% (expires 2026-12-07), Valvoline "Get $5 CASH BACK!" (expires 2027-07-31); three instant rebates whose printed dates had passed read `shown` false. `recently_expired`: Advics Brakes (exp. 10/31), Sylvania Bulbs (exp. 10/31).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def rockauto(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/rockauto/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. The engines (with carcode) for a year, make and model
engines = rockauto("vehicles", {"make": "HONDA", "year": 2010, "model": "ACCORD"})["data"]["engines"]
v = next(e for e in engines if e["engine"] == "2.4L L4")
vehicle = {k: v[k] for k in ("make", "year", "model", "engine", "carcode")}

# 2. Every brand's brake pads, grouped by RockAuto's tier, front only
d = rockauto("parts", {**vehicle, "category": "Brake & Wheel Hub", "part_type_id": "1684"})["data"]
front = [i for i in d["items"] if any(n.lower().startswith("front") for n in i["notes"])]
by_tier = {}
for i in front:
    if i["price"] is not None:
        by_tier.setdefault(i["tier"], []).append(i)
for tier, items in by_tier.items():
    low = min(items, key=lambda i: i["price"])
    print(tier, len(items), low["brand"], low["part_number"], low["price"], d["currency"], "before shipping")

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `notes`.

- **item** (parts, search, brand, tools listing) - `position`, `brand`, `part_number`, `description`, `part_type` (search, brand), `part_type_id`, `notes`, `tier`, `price`, `price_text`, `price_per`, `core_charge`, `pack_size`, `total`, `pack_options[]` {`pack_size`, `price_each`, `total`, `selected`}, `currency`, `out_of_stock`, `closeout`, `closeout_text`, `non_stock_text`, `shipping_delay_days`, `remaining`, `remaining_text`, `popular`, `fits_markets`, `alternate_numbers`, `image`, `info_url`, `part` {`part_key`, `carcode`, `part_type_id`}.
- **vehicles** - `level` (makes, years, models, engines), `language`, `make`, `year`, `model`, `count`, and `makes[]` {`make`, `name`, `markets`, `url`}, `years[]` {`year`, `markets`, `url`}, `models[]` {`model`, `markets`, `url`} or `engines[]` {`make`, `year`, `model`, `engine`, `carcode`, `markets`, `url`}.
- **categories** - `level` (categories or part_types), `language`, `vehicle` {`make`, `year`, `model`, `engine`, `carcode`}, `count`, `categories[]` {`category`, `name`, `url`} or `category`, `category_name`, `part_types[]` {`part_type_id`, `name`, `category`, `url`}.
- **parts** - `language`, `currency`, `vehicle`, `category`, `category_name`, `part_type` {`part_type_id`, `name`}, `count`, `items[]`.
- **search** - `language`, `currency`, `part_number`, `brand`, `part_type_id`, `search_label`, `limited`, `limited_notice`, `count`, `items[]`.
- **brand** - `language`, `currency`, `brand`, `part_type_id`, `search_label`, `limited`, `limited_notice`, `count`, `items[]`.
- **brands** - `language`, `count`, `brands[]`, `part_groups[]`, `part_type_count`, `part_types[]` {`part_type_id`, `name`} (with `include_part_types`).
- **part** - `language`, `requested`, `brand`, `part_number`, `title`, `part`, `price`, `price_text`, `price_per`, `core_charge`, `pack_size`, `total`, `pack_options`, `currency`, `out_of_stock`, `description`, `specifications[]` {`name`, `value`}, `oe_numbers`, `alternate_numbers`, `warranty[]`, `warranty_url`, `disclaimer`, `more_information`, `images`.
- **suggestions** - `query`, `count`, `vehicles[]` {`year`, `make`, `model`, `engine`, `carcode`, `markets`, `part_type_id`, `part_type`, `category`, `text`}, `part_types[]` {`part_type_id`, `name`, `category`}, `tools[]` {`part_type_id`, `name`, `category`, `subcategory`}, `help[]` {`question`, `answer_preview`, `url`}.
- **resolve** - `query`, `count`, `matches[]` {`year`, `make`, `model`, `engine`, `carcode`, `markets`, `part_type_id`, `part_type`, `category`, `text`, `leftover`}.
- **tools** - `level`, `language`, `currency`, `count`, and `categories[]`, `subcategories[]` {`category`, `subcategory`, `name`, `url`}, `part_types[]` {`part_type_id`, `name`, `url`} or `category`, `subcategory`, `part_type`, `items[]`.
- **promotions** - `language`, `currency` (USD), `read_date`, `count`, `promotions[]` {`name`, `badge`, `title`, `offer`, `expires_text`, `expires`, `shown`, `link_text`, `link_url`}, `recently_expired[]`.

## Guardrails

- Name it "RockAuto (rockauto.com, the online auto parts catalog based in Madison, Wisconsin)" on first mention, "RockAuto" after that.
- Prices: quote each with the currency, "before shipping", the vehicle and axle where it applies, and the `fetched_at` date ("listed on rockauto.com at 23.79 USD before shipping, rear pads for a 2010 Honda Accord 2.4L L4, Nov 26, 2026"). A converted currency is RockAuto's display conversion of the US catalog: never present a GBP or EUR price as a UK or European retailer's price.
- Comparisons: same brand and part number (or an OE / interchange number both list), front with front, at named retailers on one date. No verdict on which retailer is cheaper beyond the numbers shown, and no "best brand" call: tiers are RockAuto's labels.
- Fitment: report RockAuto's `notes` as given. Never claim a part fits a vehicle beyond what RockAuto lists for that carcode, and tell the user to confirm fitment before buying.
- Stock labels: quote `remaining_text`, `non_stock_text` and `closeout_text` as printed; never infer quantities or warehouse locations.
- Promotions: quote `offer` and `expires_text` as printed with `read_date`; an offer whose printed date has passed may still be on the page.
- Descriptive only: no commentary on RockAuto's business, pricing or policies. Quote RockAuto's own description of itself only with its source.
- Do not republish RockAuto images, manufacturer descriptions or logos. Write rockauto.com as plain text and cite brands, part numbers, carcodes and capture dates rather than linking RockAuto pages.
- Terms: Scavio does not collect or store RockAuto data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account, no cart and no checkout. RockAuto's site terms and notices cover how its site may be used; read them for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, part numbers, carcodes, part type ids, tiers or fitment notes. Only return what the API returned, with the `fetched_at` time.
- Not available: reviews, stores or store stock, the buyer's guide, shipping cost, coupon codes, price history (store your own), sort or paging, cart or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: the vehicle inputs not sent together ("<the missing ones> is required: send make, year, model, engine and carcode exactly as vehicles answers them for the engine (carcode decides the vehicle on RockAuto)."), a carcode that answers another vehicle ("carcode 1503315 is a 2012 SUBARU OUTBACK 3.6L H6 on RockAuto, not the 2012 BMW 328I 2.0L L4 TURBOCHARGED you sent. Take make, year, model, engine and carcode together from vehicles ..."), `year` without `make` or `model` without `make` and `year` on `/vehicles`, an id that is not digits ("must be a RockAuto number (digits), as RockAuto's answers give it"), a part number with other characters, a brand not written as `/brands` lists it, a `query` under 2 characters (suggestions) or 3 (resolve), `subcategory` without `category` on `/tools`, a `language` or `currency` outside the lists.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "RockAuto lists no make \"NOSUCHMAKE\". Take make from vehicles (no inputs).", "RockAuto lists no <year> <make>. Take make and year from vehicles.", "RockAuto lists no category \"<category>\" for this vehicle. Take category from categories.", "RockAuto lists no part type <id> in \"<category>\" for this vehicle. Take part_type_id from categories with category.", "RockAuto has no part for these keys. Take part (part_key, carcode, part_type_id) from parts, search, brand or tools items.", "RockAuto has no such page.". Take every input from a previous answer rather than guessing it. A part number with no match is a `200` with `count` 0, not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api).
- `502` means RockAuto data was temporarily unavailable ("RockAuto is temporarily unavailable. Please try again.", or "RockAuto answered in another currency than the one requested. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("RockAuto is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- A timeout on `/parts` for a large part type: RockAuto can take 80-100 seconds. Keep the client timeout at 240 seconds and retry once.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.96.0
npm install scavio@0.97.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const vehicle = { make: "HONDA", year: 2010, model: "ACCORD", engine: "2.4L L4", carcode: "1444945" };
const { data: engines } = await scavio.rockauto.vehicles({ make: "HONDA", year: 2010, model: "ACCORD" });
const { data: types } = await scavio.rockauto.categories({ ...vehicle, category: "Brake & Wheel Hub" });
const { data: pads } = await scavio.rockauto.parts({ ...vehicle, category: "Brake & Wheel Hub", part_type_id: "1684" });
const { data: found } = await scavio.rockauto.search({ part_number: "BP1084", currency: "CAD" });
const { data: part } = await scavio.rockauto.part({ part_key: "6129207", part_type_id: "1684", carcode: "0" });
const { data: suggest } = await scavio.rockauto.suggestions({ query: "2015 ford f-150" });
const { data: promos } = await scavio.rockauto.promotions();
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.rockauto.vehicles(...)`, `categories`, `parts`, `search`, `brand`, `brands`, `part`, `suggestions`, `resolve`, `tools` and `promotions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `get_rockauto_vehicles`, `get_rockauto_categories`, `get_rockauto_parts`, `search_rockauto`, `get_rockauto_brand`, `get_rockauto_brands`, `get_rockauto_part`, `get_rockauto_suggestions`, `get_rockauto_resolve`, `get_rockauto_tools` and `get_rockauto_promotions`. RockAuto is opt-in: add `rockauto` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,rockauto"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [vehicles](https://scavio.dev/docs/rockauto-vehicles?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api), [categories](https://scavio.dev/docs/rockauto-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api), [parts](https://scavio.dev/docs/rockauto-parts?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api), [search](https://scavio.dev/docs/rockauto-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api), [brand](https://scavio.dev/docs/rockauto-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api), [brands](https://scavio.dev/docs/rockauto-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api), [part](https://scavio.dev/docs/rockauto-part?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api), [suggestions](https://scavio.dev/docs/rockauto-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api), [resolve](https://scavio.dev/docs/rockauto-resolve?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api), [tools](https://scavio.dev/docs/rockauto-tools?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api), [promotions](https://scavio.dev/docs/rockauto-promotions?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api). Overview: [RockAuto API](https://scavio.dev/rockauto-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rockauto-parts-api).
