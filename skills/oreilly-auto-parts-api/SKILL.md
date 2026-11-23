---
name: oreilly-auto-parts-api
description: O'Reilly Auto Parts API for O'Reilly Auto Parts (oreillyauto.com, the US auto parts retailer) - part-number cross-reference with prices, another brand's, an AutoZone or an OE part number in (FRAM PH3614, Motorcraft FL820S), the O'Reilly parts O'Reilly lists as its replacements out, each with O'Reilly's price, sale price, the refundable core charge, the warranty, deals and store pickup, all priced for the O'Reilly store O'Reilly assigns to the request (priced_for names it; prices differ by store); keyword and part-number search, category and brand lists, 24 per page up to O'Reilly's 20 pages, sorted by price, best selling or brand and filtered by brand, store pickup or ship to home and attribute facets, optionally only the parts for one vehicle (brake pads 7,578 unfiltered, 42 for a 2015 Ford F-150) with O'Reilly's fit notes; one product in full with UPC, specifications, documents, deals with end dates, rebates, the rating and the 10 most recent reviews (no reviewer names); the vehicle selector down to engine and a 17-character VIN decode; the makes, models, engines and years one part fits; which O'Reilly stores within 50 miles of a ZIP or a point can hand over one part (in store now, pickup time, as availability states, not unit counts); stores near a ZIP with hours, holiday hours and services, the store directory by state and city (US, and the Mexican directory in Spanish); search suggestions, the category tree, mail-in rebates with valid and postmark dates and the coupons and promotions page. 14 endpoints, 2 credits per call, 4 for a product by line code and part number, a ZIP lookup, the brand index and deals, cross-reference 2-6. No unit counts, store choice for prices, reviews past the 10 most recent, Mexico prices, O'Reilly Pro pricing, price history or checkout.
version: 1.0.0
tags: oreilly, oreilly-auto-parts, oreillyauto, oreillyauto-com, oreilly-api, oreilly-auto-parts-api, oreilly-cross-reference, oreilly-part-number, oreilly-part-number-lookup, oreilly-interchange, oreilly-prices, oreilly-core-charge, oreilly-rebates, oreilly-deals, oreilly-store-pickup, oreilly-store-stock, oreilly-stores, oreilly-store-hours, oreilly-battery, oreilly-brake-pads, oreilly-vin-lookup, oreilly-fitment, brakebest, super-start, microgard, auto-parts, auto-parts-api, car-parts-api, auto-parts-cross-reference, part-number-cross-reference, oil-filter-cross-reference, vehicle-fitment, vin-decoder, core-charge, us-retail, price-monitoring, usd, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/oreilly-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api
---

# O'Reilly Auto Parts API - Cross-Reference, Prices, Store Stock

Read O'Reilly Auto Parts (oreillyauto.com, the US auto parts retailer): O'Reilly's own part-number cross-reference, keyword and part-number search, category and brand lists, one product in full, the parts that fit a vehicle, the vehicle selector and a VIN decode, the vehicles one part fits, pickup availability at the stores near a ZIP, stores with hours, the category tree, search suggestions, rebates and deals, plus O'Reilly's Mexican store directory. All 14 endpoints return structured JSON at 2 credits per call (4 or 6 where a call needs more than one O'Reilly step, listed below).

This is the retail site oreillyauto.com. It is not O'Reilly Pro or First Call Online (O'Reilly's commercial login sites for repair shops): commercial pricing is not read. It is also not O'Reilly Media, the technology publisher.

**The job this skill is for: O'Reilly Auto Parts part-number cross-reference with prices.** Another brand's, an AutoZone or an OE part number in, the O'Reilly parts O'Reilly lists as its replacements out, each with price, core charge, deals and rebates, then pickup at the stores near a ZIP. On 2026-11-23 the FRAM oil filter `PH3614` (part type `02269`, Engine Oil Filter) answered 10 O'Reilly parts for 2 credits, the first a MicroGard `MGL51348` at $5.99, then K&N, WIX, ACDelco and aFe filters, priced for O'Reilly store 1058 in Houston, TX. Pair it with `autozone-api` for a two-store parts price comparison on the same part (same brand and part number).

Ten limits shape every answer, so say them plainly:
- **2 credits per call; 4 or 6 where the call needs more steps.** A product by `line_code` + `part_number` is 4 (found through O'Reilly's search first; by link 2). Cross-reference is 2 with `part_type_id` + `manufacturer`, 4 with one of them or when several manufacturers use the number (the answer is then the lists to choose from, no items), 6 with neither when one manufacturer uses it. Store stock and stores by ZIP are 4 (by latitude + longitude, or the directory by state / city, 2). The brand index (brand without input) and deals are 4. A not-found (`404`) is charged, and an empty list is a charged answer. A refused input (`400`) and an upstream failure (`502`, `503`) are not charged.
- **Every price is for one store, the one O'Reilly assigns to the request.** `priced_for` {`store_id`, `address`, `city`, `state`, `zip`} names it. There is no store or ZIP input for prices, and two calls can be priced for different stores (Houston 1058 and Missouri City 5640 in the same session). O'Reilly's own price-match FAQ says "pricing at one O'Reilly Auto Parts location may differ from another or from oreillyauto.com". Report "$5.99 at O'Reilly store 1058 (Houston, TX) on 2026-11-23", never a national price.
- **Lists are 24 per page, up to O'Reilly's 20 pages.** search, category, brand and cross-reference take `page` 1-20 (a page above 20 is a `400`, not charged). O'Reilly serves at most 20 pages (480 items) of any list: "brake pads" read `total` 7,578, `total_pages` 316 and `max_page` 20. Narrow with a vehicle, `brand`, `availability` or `filters` rather than paging; never call 480 items "all".
- **A vehicle is a `base_vehicle_id`.** Resolve it once with `/vehicles` `level` `resolve` (2015 Ford F-150 = `129927`) and send `{"base_vehicle_id": 129927}` as `vehicle` in search, category, brand and product. It pins year, make and model; submodel and engine show only in each item's `fit_notes`.
- **`vehicle_fit.fits` on a product is `true` or `null`, never `false`.** It is `true` when O'Reilly's product page gives the part's application for that vehicle and `null` when the page gives no fit details, which it does for many vehicle selections: `SC1414` is the first item of the 2015 F-150 brake pad list, yet its product page with that vehicle gives no fit details. For "does it fit", use a search or category with `vehicle` (only parts that fit are listed) or `/compatibility`.
- **Cross-reference is O'Reilly's statement of equivalence, not a fit guarantee.** A number can map to no O'Reilly part: the AutoZone Duralast Gold battery `DG1210` (part type `03351`, manufacturer `AutoZone`) answered 0 items, charged 2. A part-number `/search` is O'Reilly's text match, not a cross-reference: use `/cross-reference` for another brand's number.
- **Store stock is availability states, not unit counts.** `/store-stock` answers, per store within 50 miles, `store_pickup`, `in_store_now` and `pickup_time` in O'Reilly's words ("8 AM today", "by 11:25 AM today"). O'Reilly publishes no quantity; never report a number of units.
- **Reviews are the rating and the 10 most recent.** `/product` returns `rating` {`average`, `count`} and the 10 most recent reviews O'Reilly shows (date, title, text, rating). No paging, sort, star filter, Q&A or reviewer identity.
- **US only, except the Mexican store directory.** `country` `us` (default) serves all 14 endpoints. `mx` serves `/stores` and `/store` only, O'Reilly's Mexican store directory in Spanish; O'Reilly's Mexican site shows no prices, so `mx` anywhere else is a `400`, not charged. Canada has no O'Reilly web store.
- **No price history.** Nothing is cached or kept. Poll and store your own series.

O'Reilly Auto Parts has no public developer API. Commercial customers can apply through the O'Reilly Pro Integration Hub for "a direct API or punchout ordering and invoicing integration" (single locations, multi-location shops, National Accounts and shop management systems; shop software such as Mitchell 1 and R.O. Writer connects through it), and suppliers use EDI. Retail prices, rebates and store pickup are shown on oreillyauto.com; this skill reads those public pages with one Scavio key.

O'Reilly Automotive ran 6,758 stores at the end of September 2026 (6,595 in the US and Puerto Rico, 134 in Mexico, 29 in Canada; Q3 2026 10-Q) and reported $17.78 billion in sales for 2025 (FY2025 10-K); Q3 2026 sales were $5.12 billion, up 9% (Q3 2026 release). Quote these with their source, never from the samples.

See also: for the same part at AutoZone use `autozone-api`; for Harbor Freight tools use `harbor-freight-api`; for the same oil or battery at Walmart use `walmart-product-data`; for parts on Amazon use `amazon-product-data`; for prices across retailers use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Cross-reference another brand's, an AutoZone or an OE part number (FRAM, WIX, Motorcraft, Duralast) to the O'Reilly parts O'Reilly lists as replacements, with prices
- Read an O'Reilly price with its sale price, core charge, warranty, deals and mail-in rebate
- Find the O'Reilly parts that fit a vehicle (year, make, model, or a VIN) in a part type: brake pads, batteries, oil filters, wiper blades, alternators
- Check which O'Reilly stores near a ZIP can hand over a part today (in store now, pickup time)
- List the makes, models, engines and years one O'Reilly part fits
- Search oreillyauto.com by keyword or part number, sorted by price or best selling, filtered by brand or attribute
- Read one O'Reilly product in full: UPC, specifications, documents, deals, rebates, rating and recent reviews
- Find O'Reilly stores near a ZIP or in a state and city with hours, holiday hours and services (US; Mexican directory in Spanish)
- List O'Reilly's current mail-in rebates with valid and postmark dates, or its coupons, offers and promotions
- Compare one part's price at O'Reilly and AutoZone (with `autozone-api`)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 2 credits; a product by line code and part number, a ZIP lookup, the brand index and deals cost 4, and an unscoped cross-reference up to 6.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, vehicles, VIN decode, compatibility, store, suggestions, categories, rebates and deals took 2-14 seconds, store stock and stores 2-15, product and cross-reference 2-30, and search and category 5-38. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Markets | Credits |
|---|---|---|---|
| `POST /api/v1/oreilly/search` | Keywords or an O'Reilly part number: 24 per page (pages 1-20) with total, facets and `priced_for`; optionally only parts for a vehicle | us | 2 |
| `POST /api/v1/oreilly/cross-reference` | Another brand's or an OE part number: the O'Reilly parts O'Reilly lists as replacements, or the part types and manufacturers to choose from | us | 2 with `part_type_id` + `manufacturer`; 4 with one, or when several manufacturers match; 6 with neither |
| `POST /api/v1/oreilly/product` | One product: price, sale, core charge, warranty, availability, UPC, specifications, documents, deals, rebates, rating, the 10 most recent reviews; with `vehicle`, `vehicle_fit` | us | 2 by link; 4 by `line_code` + `part_number` |
| `POST /api/v1/oreilly/vehicles` | The vehicle selector one level at a time (types, years, makes, models, submodels, engines), `resolve` to a `base_vehicle_id`, or a VIN decode | us | 2 |
| `POST /api/v1/oreilly/compatibility` | The makes one part fits; with `make`, the models, engines and years | us | 2 |
| `POST /api/v1/oreilly/category` | One category's products by link or path, 24 per page, optionally only parts for a vehicle | us | 2 |
| `POST /api/v1/oreilly/categories` | The category tree (34 departments, 1,334 nodes) or one branch | us | 2 |
| `POST /api/v1/oreilly/brand` | One brand's products, 24 per page; without `brand`, O'Reilly's brand index | us | 2; index 4 |
| `POST /api/v1/oreilly/store-stock` | The stores within 50 miles of a ZIP or a point that can hand over one part: in store now, pickup time | us | 4 by ZIP; 2 by latitude + longitude |
| `POST /api/v1/oreilly/stores` | The 25 nearest stores within 50 miles of a ZIP or a point with hours and services, or the store directory by state (+ city) | us, mx (directory) | 4 by ZIP; 2 by point or directory |
| `POST /api/v1/oreilly/store` | One store: us by `store_id`; us or mx by its directory `url`; mx by `store_number` + `state` + `city` | us, mx | 2 |
| `POST /api/v1/oreilly/suggestions` | O'Reilly's part-type suggestions for typed text, each with the category link | us | 2 |
| `POST /api/v1/oreilly/rebates` | O'Reilly's current rebates with valid dates, postmark-by date, terms and form PDFs | us | 2 |
| `POST /api/v1/oreilly/deals` | The coupons, offers and promotions page (promo codes, validity, details) and the deals menu | us | 4 |

## Markets

| `country` | Site | Language, currency | Endpoints |
|---|---|---|---|
| `us` (default) | oreillyauto.com and O'Reilly's store locator | English, USD | all 14 |
| `mx` | O'Reilly's Mexican store directory | Spanish | `/stores` (by `state`, + `city`), `/store` |

- Every answer echoes `country` and `language` (and `currency` on us). `mx` on any other endpoint, or any other market, is a `400`, not charged.
- Mexican states are the codes O'Reilly lists: `agu`, `bcs`, `col`, `gua`, `jal`, `mic`, `nay`, `sin`, `son`. Store names, addresses and services come back in Spanish as O'Reilly writes them ("Prueba de batería"): translate them for the user, never alter the values.
- US store search near a ZIP or point covers the US and Puerto Rico. There are no prices, catalog or stock for Mexico, and no Canadian web store.

## Prices, core charges, deals and rebates

Every priced item (search, category, brand, cross-reference, product) carries:

| Field | Meaning |
|---|---|
| `price` | O'Reilly's price at the `priced_for` store (the sale price when on sale) |
| `regular_price` | O'Reilly's regular price |
| `sale_price`, `on_sale`, `sale_type` | The sale, as O'Reilly marks it (`sale_type` e.g. "Sale"), or `null` / `false` |
| `discount_percent` | Computed by Scavio from `regular_price` when on sale; `null` otherwise |
| `clearance` | Whether O'Reilly marks the item clearance |
| `core_charge` | The refundable core deposit O'Reilly adds on parts such as batteries and alternators; `0` when there is none |
| `oil_fee`, `oil_deposit` | Fees O'Reilly lists on some oils, or `null` |
| `warranty` | O'Reilly's warranty text, as given ("Limited Lifetime Warranty", "1 Year Limited Warranty") |
| `availability` | `store_pickup`, `in_store_now`, `pickup_time` (O'Reilly's words), `ship_to_home`, `two_day`, `three_day`, `special_order`, `free_shipping`, `ship_to_home_blocked`, `store_pickup_blocked`, `store_restricted`, `air_shipping_restricted`, all for the `priced_for` store |
| `deals` | [{`title`, `description`, `ends`, `terms`}] as O'Reilly writes them |

- **Core charge.** Quote `core_charge` as a refundable deposit shown separately, on top of `price`, at that store; never add it into the price silently. Captured 2026-11-23: Super Start Platinum AGM batteries read $264.99 plus a $22 core charge; an Ultima 175 Amp remanufactured alternator (`ULT` `R113614`) read $355.99 plus a $40 core charge. Never state an amount that is not in the answer.
- **Rebates are mail-in or online claims paid as gift cards or prepaid cards**, with a purchase window and a postmark-by date. Never subtract a rebate from a price; show it next to the price. On product, `rebates` [{`heading`, `title`, `description`}]; `/rebates` lists them all with dates and form PDFs.
- **Deals** are O'Reilly's own text: quote `title`, `ends` and `terms`. "FREE* with Purchase of 2 Rotors" (BrakeBest pads) read `ends` "November 30, 2026"; a Mobil 1 5W-30 5 quart read $44.95 on sale against $46.99 regular with "Get 5 quarts for $44.95" ending November 24, 2026 and a "$10 O'Reilly Gift Card plus a Tyler Reddick Poster" rebate.
- **Stock** is as O'Reilly reports it for that store, at the moment of the call; Scavio makes no promise of its accuracy.
- List items carry no rating; `/product` has `rating`.
- Prices differ by store: describe differences between two answers from their `priced_for` stores and numbers, never why, and never call a discount real or fake.

## Workflow

1. **Cross-reference a number:** `/cross-reference` with `part_number` alone (`FL820S`). If several manufacturers use it, the answer lists `part_types` and `manufacturers` with no items (4 credits): ask the user whose part it is, then call again with `part_type_id` + `manufacturer` (2 credits). When the user already knows the brand, send `manufacturer` from the start.
2. **Price the matches:** each item already carries price, core charge, warranty, deals and availability at the `priced_for` store. For specifications, UPC, rebates and reviews, `/product` with the item's `url` (2 credits).
3. **Pickup near the user:** `/store-stock` with the item's `line_code`, `part_number` and a `zip` (4) or `latitude` + `longitude` (2).
4. **Vehicle:** `/vehicles` `years`, then `makes` (`year`), `models` (`year` + `make_id`), optionally `submodels` (+ `model_id`) and `engines` (+ `submodel_id`), then `resolve` (`year` + `make_id` + `model_id`, optional `submodel_id` / `engine_id`) for the `base_vehicle_id`. Or `level` `vin` with a 17-character VIN, then `resolve` with the ids it returns.
5. **Parts that fit:** `/search` or `/category` with `vehicle` {`base_vehicle_id`}. Compare `total` against the same call without `vehicle`; read `fit_notes` for submodel, engine and position.
6. **Part type:** a category `url` from `/categories`, a `/suggestions` answer, a `Categories` facet value or a product's `breadcrumbs`. A page O'Reilly shows as a landing answers `items` [] with `links` to its product lists.
7. **Narrow the list:** `brand` (a `Brands` facet value), `availability` (`store_pickup` or `home_delivery`), up to 4 attribute `filters` (`{"/attributes/prodAttr_32769": "104088"}` = Brake Pad Material Ceramic), `sort` `price_asc` / `price_desc` / `best_selling` / `brand`, then `page`.
8. **Which vehicles a part fits:** `/compatibility` with `line_code` + `part_number` (makes), then with `make` (models with engine and years).
9. **Stores:** `/stores` with `zip` or a point (nearest 25 within 50 miles, hours with holiday adjustments, services), or `state` then `state` + `city` for the directory; `/store` for one.
10. **Watching prices:** there is no history. Poll the same items on a schedule and store each answer with its `fetched_at` and `priced_for`; that stored series is the history. Compare only answers priced for the same store.

## Parameters

### Search (`/search`), category (`/category`), brand (`/brand`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Keywords or an O'Reilly part number (`brake pads`, `SC1001`); 1-200 chars |
| `category` | string | category: required | A category link or path (`categories[].url`, a suggestion or facet link): `/shop/b/<name>/<12-character hash>`. A wrong hash is a charged `404` |
| `brand` | string | brand: optional | On `/brand`, a brand link or path from the index (`brands[].url`, `/shop/brands/a/<brand>/<code>`); without it, the brand index (4 credits). On search and category, a `Brands` facet value (`Wagner_OEX`) |
| `vehicle` | object | none | `{"base_vehicle_id": 129927}` from `/vehicles` `resolve`; optional `slug` as `/vehicles` returned it |
| `availability` | string | none | `store_pickup` or `home_delivery`, as O'Reilly filters them |
| `filters` | object | none | Up to 4 attribute facets: `{"<facets[].param>": "<facets[].values[].value>"}` |
| `sort` | string | `relevance` | `relevance` (O'Reilly's order), `price_desc`, `price_asc`, `best_selling`, `brand` (A-Z) |
| `page` | integer | 1 | 1-20, 24 items a page; above 20 is a `400` |
| `country` | string | `us` | `us` only (`mx` is a `400`) |

On `/brand` the list inputs (`page`, `sort`, `vehicle`, `filters`, `availability`) apply to one brand: sent without `brand` they are a `400`. A search O'Reilly sends to a category answers `redirected_to` with that category's link.

### Cross-reference (`/cross-reference`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `part_number` | string | required | Another brand's or an OE part number (`PH3614`, `FL820S`, `DG1210`) |
| `part_type_id` | string | none | `part_types[].id` from an earlier answer (`02269` = Engine Oil Filter). Without it, O'Reilly's first-listed part type is used and named in `notes` |
| `manufacturer` | string | none | The brand whose number it is: `manufacturers[].id` from an earlier answer (`FRAM`, `Motorcraft`, `AutoZone`, `OE Part Number`) |
| `page` | integer | 1 | 1-20 |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | An O'Reilly product link (`items[].url`): 2 credits |
| `line_code` + `part_number` | string | one of | As list items give them (`BB` + `SC1001`, `MOB` + `1-5-30-5QT`): 4 credits. Send `url` or the pair, not both |
| `vehicle` | object | none | `{"base_vehicle_id": 129927}`: adds `vehicle_fit` |

### Vehicles (`/vehicles`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `level` | string | `years` | `types`, `years`, `makes` (`year`), `models` (`year` + `make_id`), `submodels` (+ `model_id`), `engines` (+ `submodel_id`), `resolve` (`year` + `make_id` + `model_id`, optional `submodel_id`, `engine_id` with `submodel_id`), `vin` |
| `type_id` | integer | 1 | 1 Automotive, 2 Motorcycle & Scooter, 3 ATV & UTV, 4 Personal Watercraft, 5 Snowmobile |
| `year` / `make_id` / `model_id` / `submodel_id` / `engine_id` | integer | none | Ids from the level before (23076 = Ford, 31549 = F-150) |
| `vin` | string | none | A 17-character VIN (`level` `vin`); an undecodable VIN is a charged `404` |

### Compatibility (`/compatibility`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `line_code` + `part_number` | string | required | The part (`BB` + `SC1001`) |
| `make` | string | none | A make from the first answer's `makes` (`Ford`): its models, engines and years |

### Store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `line_code` + `part_number` | string | required | The part (`SSB` + `48PLT`) |
| `zip` | string | one of | A 5-digit US ZIP (4 credits; an unknown ZIP is a charged `404`) |
| `latitude` + `longitude` | number | one of | A point (2 credits) |
| `quantity` | integer | 1 | Quantity to check, 1-99 |

### Stores (`/stores`), store (`/store`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` / `latitude` + `longitude` | | one of | Stores: the 25 nearest within 50 miles (us; ZIP 4 credits, point 2) |
| `state` | string | one of | Stores: a US state code (`mo`, `tx`, `pr`) or, on mx, a Mexican state code (`jal`): its cities |
| `city` | string | none | Stores, with `state`: a city name or `cities[].city_slug`: its stores |
| `store_id` | string or integer | one of | Store, us: an O'Reilly store number (`stores[].store_id`: `4973`) |
| `url` | string | one of | Store, us or mx: a directory store page link (`stores[].url`) |
| `store_number` + `state` + `city` | | one of | Store, mx: the store number with its state and city |
| `country` | string | `us` | `us` or `mx` (directory only) |

### Categories (`/categories`), suggestions (`/suggestions`), rebates (`/rebates`), deals (`/deals`)

`/categories` takes an optional `root` (`categories[].hash`, 12 hex characters) for one branch; `/suggestions` takes `query` (2-100 chars); `/rebates` and `/deals` take no input besides `country` (us).

## Examples

### Cross-reference a part number

```bash
curl -X POST https://api.scavio.dev/api/v1/oreilly/cross-reference \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"part_number": "PH3614", "part_type_id": "02269", "manufacturer": "FRAM"}'
```

Captured `data` (2026-11-23, 2 credits; 2 of 10 items shown, `image` dropped, `attributes` cut to 2):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "part_number": "PH3614",
  "part_types": null,
  "part_type_id": "02269",
  "manufacturers": null,
  "manufacturer": "FRAM",
  "replacing_brands": ["FRAM"],
  "priced_for": { "store_id": "1058", "address": "9009 Cullen Boulevard", "city": "Houston", "state": "TX", "zip": "77051" },
  "total": 10,
  "page": 1,
  "page_size": 24,
  "total_pages": 1,
  "count": 10,
  "items": [
    {
      "position": 1,
      "product_id": "4444867",
      "line_code": "MGD",
      "part_number": "MGL51348",
      "name": "MicroGard Oil Filter",
      "brand": null,
      "url": "https://www.oreillyauto.com/detail/c/microgard/microgard-oil-filter/mgd3/mgl51348",
      "category": "Engine Oil Filter",
      "price": 5.99,
      "regular_price": 5.99,
      "sale_price": null,
      "on_sale": false,
      "sale_type": null,
      "discount_percent": null,
      "clearance": false,
      "core_charge": 0,
      "oil_fee": null,
      "oil_deposit": null,
      "currency": "USD",
      "unit_of_measure": "Each",
      "warranty": "1 Year Limited Warranty",
      "fit": "UNKNOWN",
      "fit_notes": [],
      "availability": {
        "store_pickup": true,
        "in_store_now": true,
        "pickup_time": null,
        "ship_to_home": true,
        "two_day": false,
        "three_day": false,
        "special_order": false,
        "free_shipping": true,
        "ship_to_home_blocked": false,
        "store_pickup_blocked": false,
        "store_restricted": false,
        "air_shipping_restricted": false
      },
      "deals": [],
      "attributes": [{ "name": "Style", "value": "Spin-On Canister" }, { "name": "Thread Size", "value": "3/4-16 Inch" }]
    },
    {
      "position": 2,
      "product_id": "4395990",
      "line_code": "KAN",
      "part_number": "HP1002",
      "name": "K&N Engineering Performance Gold Oil Filter",
      "brand": null,
      "url": "https://www.oreillyauto.com/detail/c/performance-gold/k-n-engineering-performance-gold-oil-filter/kan1/hp1002",
      "category": "Engine Oil Filter",
      "price": 17.99,
      "regular_price": 17.99,
      "sale_price": null,
      "on_sale": false,
      "sale_type": null,
      "discount_percent": null,
      "clearance": false,
      "core_charge": 0,
      "oil_fee": null,
      "oil_deposit": null,
      "currency": "USD",
      "unit_of_measure": "Each",
      "warranty": "1 Year Limited Warranty",
      "fit": "UNKNOWN",
      "fit_notes": [],
      "availability": {
        "store_pickup": true,
        "in_store_now": true,
        "pickup_time": null,
        "ship_to_home": true,
        "two_day": false,
        "three_day": false,
        "special_order": false,
        "free_shipping": true,
        "ship_to_home_blocked": false,
        "store_pickup_blocked": false,
        "store_restricted": false,
        "air_shipping_restricted": false
      },
      "deals": [],
      "attributes": [{ "name": "Style", "value": "Spin-On Canister" }, { "name": "Thread Size", "value": "3/4-16 Inch" }]
    }
  ],
  "facets": [
    { "name": "Part Types You're Replacing", "param": "partTypeFilter", "values": [{ "label": "Engine Oil Filter", "value": "02269", "url": null }] },
    { "name": "Brands You're Replacing", "param": "manufacturers", "values": [{ "label": "FRAM", "value": "FRAM", "url": null }] }
  ],
  "notes": ["Prices are as O'Reilly shows them for the store it assigns to the request (priced_for); another store can price differently."]
}
```

The other 8 matches were K&N, MicroGard Select, aFe POWER, ACDelco (`PF53` at $14.99) and WIX (`51348XP` at $16.99), all at Houston store 1058. `brand` on list items comes from the page's Brands facet and can be `null`, as here: read the brand from `name`. The same day, other numbers answered:
- `{"part_number": "FL820S"}` alone (4 credits): no items, `part_types` [Engine Oil Filter `02269`] and 10 `manufacturers` that use the number (Bosch, Lincoln Electric, Indmar, Motorcraft, K&N Engineering, Fleetguard, Kalmar, Winnebago, aFe POWER, OE Part Number), with the note to send `manufacturer`.
- `{"part_number": "FL820S", "manufacturer": "Motorcraft"}` (4 credits): 6 O'Reilly parts, K&N `HP2010` $17.99, WIX `51372XP` $16.99 and `51372` $14.99, MicroGard `MGL51372` $7.99 and `MSL51372` $9.99, aFe `44LF008MB` $54.99.
- `{"part_number": "DG1210", "part_type_id": "03351", "manufacturer": "AutoZone"}` (2 credits): 0 items, "O'Reilly lists no replacement for this part number from this manufacturer."

### Parts that fit a vehicle

```bash
curl -X POST https://api.scavio.dev/api/v1/oreilly/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "brake pads", "vehicle": {"base_vehicle_id": 129927}}'
```

Captured `data` (2026-11-23, 2 credits; 1 of 24 items shown, `image` dropped, its 15 `fit_notes` cut to 1, `deals` to 1 and `attributes` to 2; 3 of 12 facets shown with 3 values each):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "query": "brake pads",
  "priced_for": { "store_id": "1058", "address": "9009 Cullen Boulevard", "city": "Houston", "state": "TX", "zip": "77051" },
  "vehicle_requested": { "base_vehicle_id": "129927" },
  "vehicle": { "base_vehicle_id": "129927", "year": 2015, "make": "Ford", "model": "F-150" },
  "title": "2015 Ford F-150 - Brake Pads",
  "total": 42,
  "page": 1,
  "page_size": 24,
  "total_pages": 2,
  "max_page": 2,
  "count": 24,
  "sort": "relevance",
  "sort_applied": null,
  "brand": null,
  "availability": null,
  "filters": {},
  "items": [
    {
      "position": 1,
      "product_id": "7940547",
      "line_code": "BB",
      "part_number": "SC1414",
      "name": "BrakeBest Select Front Ceramic Brake Pads",
      "brand": "BrakeBest Select Brake Pads",
      "url": "https://www.oreillyauto.com/detail/c/brakebest-select-brake-pads/brakes/brake-pads---shoes/brake-pads/a99314144bb6/brakebest-select-front-ceramic-brake-pads/bsg0/sc1414",
      "category": "Brake Pads",
      "price": 76.99,
      "regular_price": 76.99,
      "sale_price": null,
      "on_sale": false,
      "sale_type": null,
      "discount_percent": null,
      "clearance": false,
      "core_charge": 0,
      "oil_fee": null,
      "oil_deposit": null,
      "currency": "USD",
      "unit_of_measure": "per Set",
      "warranty": "Limited Lifetime Warranty",
      "fit": "UNKNOWN",
      "fit_notes": [
        {
          "name": "Brake Pads",
          "description": "Front; Ceramic; This Vehicle May Use An Electronic Parking Brake That Requires A Special Procedure To Complete The Pad Replacement, Please Refer To Vehicle Service Manual; Includes Hardware; OE Pad Material Is Ceramic"
        }
      ],
      "availability": {
        "store_pickup": true,
        "in_store_now": true,
        "pickup_time": null,
        "ship_to_home": true,
        "two_day": false,
        "three_day": false,
        "special_order": false,
        "free_shipping": true,
        "ship_to_home_blocked": false,
        "store_pickup_blocked": false,
        "store_restricted": false,
        "air_shipping_restricted": false
      },
      "deals": [
        {
          "title": "FREE* with Purchase of 2 Rotors",
          "description": "Get a set of BrakeBest Select Pro or Import Direct brake pads when you purchase (2) BrakeBest Select Pro or Import Direct rotors.",
          "ends": "November 30, 2026",
          "terms": "Get a set of BrakeBest Select Pro or Import Direct brake pads when you purchase (2) BrakeBest Select Pro or Import Direct rotors Sales tax not included. Discount applied automatically in Cart once qualifying items are added."
        }
      ],
      "attributes": [{ "name": "Brake Pad Material", "value": "Ceramic" }, { "name": "Installation Hardware Included", "value": "Yes" }]
    }
  ],
  "facets": [
    { "name": "Availability", "param": "Availability", "values": [{ "label": "Ship to Home", "value": "HOME_DELIVERY", "url": null }, { "label": "Pick Up in Store", "value": "STORE_PICKUP", "url": null }] },
    { "name": "Brands", "param": "Brands", "values": [{ "label": "ACDelco", "value": "ACDelco", "url": null }, { "label": "Baer Brakes", "value": "Baer Brakes", "url": null }, { "label": "BrakeBest Brake Pads", "value": "BrakeBest Brake Pads", "url": null }] },
    { "name": "Brake Pad Material", "param": "/attributes/prodAttr_32769", "values": [{ "label": "Ceramic", "value": "104088", "url": null }, { "label": "Low-Metallic", "value": "1352993", "url": null }, { "label": "Organic", "value": "202428", "url": null }] }
  ],
  "notes": ["Prices are as O'Reilly shows them for the store it assigns to the request (priced_for); another store can price differently."],
  "redirected_to": "https://www.oreillyauto.com/shop/b/brakes/brake-pads---shoes/brake-pads/a99314144bb6/v/a/129927/automotive-truck-2015-ford-f-150"
}
```

The same search without `vehicle` read `total` 7,578 (316 pages, 20 served); for the 2015 F-150 it read 42 in 2 pages. `fit` stays `UNKNOWN` without an engine: `fit_notes` are the evidence (position, material, parking brake type, hardware). The facet `param` is the key to send: `Brands` -> `brand`, `Availability` -> `availability`, an `/attributes/...` param -> `filters`. The battery category for the same vehicle (`/shop/b/battery---accessories/batteries/battery---best-fit/ec27e4e51018`) read 70 batteries, the first a Super Start Platinum AGM `47PLT` at $264.99 plus a $22 core charge.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/oreilly/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.oreillyauto.com/detail/c/brakebest-select-brake-pads/brakebest-select-ceramic-brake-pads/bsg0/sc1001"}'
```

Captured `data` (2026-11-23, 2 credits; `description` and `images` dropped, `specifications` cut to 3, `deals` to 1, `reviews` to 2 of 3):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "requested": { "url": "https://www.oreillyauto.com/detail/c/brakebest-select-brake-pads/brakebest-select-ceramic-brake-pads/bsg0/sc1001" },
  "priced_for": { "store_id": "5640", "address": "9829 Hwy 6", "city": "Missouri City", "state": "TX", "zip": "77459" },
  "line_code": "BB",
  "part_number": "SC1001",
  "name": "BrakeBest Select Ceramic Brake Pads",
  "brand": "BrakeBest Select Brake Pads",
  "url": "https://www.oreillyauto.com/detail/c/brakebest-select-brake-pads/brakebest-select-ceramic-brake-pads/bsg0/sc1001",
  "upc": "441769034583",
  "unit_of_measure": "per Set",
  "category": "Brake Pads",
  "part_type_id": null,
  "universal": false,
  "price": 69.99,
  "regular_price": 69.99,
  "sale_price": null,
  "on_sale": false,
  "sale_type": null,
  "discount_percent": null,
  "clearance": false,
  "core_charge": 0,
  "oil_fee": null,
  "oil_deposit": null,
  "warranty": "Limited Lifetime Warranty",
  "availability": {
    "store_pickup": true,
    "in_store_now": true,
    "pickup_time": null,
    "ship_to_home": true,
    "two_day": false,
    "three_day": false,
    "special_order": false,
    "free_shipping": true,
    "ship_to_home_blocked": false,
    "store_pickup_blocked": false,
    "store_restricted": false,
    "air_shipping_restricted": false
  },
  "stock_status": "InStock",
  "deals": [
    {
      "title": "FREE* with Purchase of 2 Rotors",
      "description": "Get a set of BrakeBest Select Pro or Import Direct brake pads when you purchase (2) BrakeBest Select Pro or Import Direct rotors.",
      "ends": "November 30, 2026",
      "terms": "Get a set of BrakeBest Select Pro or Import Direct brake pads when you purchase (2) BrakeBest Select Pro or Import Direct rotors Sales tax not included. Discount applied automatically in Cart once qualifying items are added."
    }
  ],
  "rebates": [],
  "specifications": [
    { "name": "Brake Pad Material", "value": "Ceramic" },
    { "name": "Installation Hardware Included", "value": "No" },
    { "name": "Noise-Reducing Shim Included", "value": "Yes" }
  ],
  "image": "https://images-prod.oreillyauto.com/parts/img/large/obb/orly_sc1001_202_ang_primary.jpg",
  "documents": [],
  "breadcrumbs": [
    { "name": "All Brands", "url": "https://www.oreillyauto.com/shop/AllBrands" },
    { "name": "BrakeBest Select Brake Pads", "url": "https://www.oreillyauto.com/shop/brands/a/brakebest-select-brake-pads/bsg" },
    { "name": "BrakeBest Select Brake Pads", "url": "https://www.oreillyauto.com/shop/brands/a/brakebest-select-brake-pads/brakebest-select-brake-pads/bsg/bsg0" },
    { "name": "BrakeBest Select Ceramic Brake Pads", "url": null }
  ],
  "rating": { "average": 4.3, "count": 3 },
  "reviews": [
    { "date": "2026-06-04T18:02:21.000Z", "title": "Brake pads", "text": "Problems with one side of these brake pads, squealing, and grinding", "rating": 3 },
    { "date": "2025-11-23T12:40:21.000Z", "title": "Break pads", "text": "Great pad work very nice they wear evenly and last long", "rating": 5 }
  ],
  "notes": [
    "O'Reilly applied a vehicle that was not requested; vehicle fit details are left out (send vehicle for them).",
    "Prices are as O'Reilly shows them for the store it assigns to the request (priced_for); another store can price differently.",
    "reviews are the 10 most recent O'Reilly shows on the product page (rating.count says how many there are)."
  ]
}
```

$69.99 at Missouri City store 5640; the same part listed at $69.99 at Houston store 1058 in search. By `line_code` + `part_number` (4 credits), `MOB` + `1-5-30-5QT` answered Mobil 1 Advanced Full Synthetic 5W-30 5 Quart at $44.95 on sale (regular $46.99, `discount_percent` 4) with a rebate, `rating` 4.8 from 177 and the 10 most recent reviews. With `vehicle`, the answer adds `vehicle_requested`, `vehicle` and `vehicle_fit` {`fits` (`true` or `null`), `universal`, `notes` [{`name`, `description`, `per_vehicle_quantity`}], `documents`}. A product O'Reilly does not list is a charged `404`.

### Store stock near a ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/oreilly/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"line_code": "SSB", "part_number": "48PLT", "zip": "60540"}'
```

Captured `data` (2026-11-23, 4 credits; 2 of 23 stores shown):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "line_code": "SSB",
  "part_number": "48PLT",
  "quantity": 1,
  "zip": "60540",
  "latitude": 41.774282,
  "longitude": -88.147187,
  "radius_miles": 50,
  "count": 23,
  "stores": [
    {
      "store_id": "4841",
      "address": { "line1": "543 Frontenac Ct", "city": "Naperville", "state": "IL", "zip": "60563" },
      "latitude": 41.780461,
      "longitude": -88.227411,
      "distance_miles": 4.2,
      "hours_message": "Opens at 7 AM",
      "closed_all_week": false,
      "availability": { "store_pickup": true, "in_store_now": true, "pickup_time": "8 AM today", "message_hidden": false }
    },
    {
      "store_id": "3406",
      "address": { "line1": "440 N Bolingbrook Drive", "city": "Bolingbrook", "state": "IL", "zip": "60440" },
      "latitude": 41.709527,
      "longitude": -88.068009,
      "distance_miles": 6.1,
      "hours_message": "Opens at 7:30 AM",
      "closed_all_week": false,
      "availability": { "store_pickup": true, "in_store_now": true, "pickup_time": "8:30 AM today", "message_hidden": false }
    }
  ],
  "notes": [
    "O'Reilly shows availability states (in store now, available for pickup, pickup time as it words it), not unit counts. Availability is as O'Reilly reports it; Scavio makes no promise of its accuracy.",
    "distance_miles is computed by Scavio from the requested point to the store's coordinates."
  ]
}
```

A Super Start Platinum AGM battery near ZIP 60540 (Naperville, IL): 23 stores within 50 miles, the nearest 4.2 miles away with it in store now and pickup "8 AM today". Report it as "O'Reilly showed it in store at store 4841 at the time of the call", never a count. Near ZIP 10001 (Manhattan) the Mobil 1 5 quart answered 4 stores, the nearest in Greenburgh, NY at 22.4 miles. With `latitude` + `longitude` instead of `zip` the call is 2 credits.

### Vehicles, compatibility, category, brand, categories, stores, store, suggestions, rebates and deals

- `/vehicles` `{"level": "vin", "vin": "1HGCM82633A004352"}`: 2003 Honda Accord (`make_id` 23152, `model_id` 29711) with `submodels` [EX `20882`] and one engine id. `{"level": "resolve", "year": 2015, "make_id": 23076, "model_id": 31549, "submodel_id": 39806, "engine_id": 301350}`: `base_vehicle_id` 129927, `vehicle_id` "129927-39806-301350", F-150 King Ranch, "V6 - 3.5L 3496cc 213ci GAS DI Turbocharged vin G - 4 valve DOHC", `path` `/v/a/129927/automotive-truck-2015-ford-f-150`. `makes` for 2015: 88; `models` for 2018 `make_id` 23514: 20 (4Runner first).
- `/compatibility` `{"line_code": "BB", "part_number": "SC1001"}`: 16 makes; with `"make": "Ford"`: 6 rows such as `{"model": "Mustang Boss 302", "engine": "V8 - 5.0L 4951cc 302ci GAS MFI vin U type 99U - 4 valve DOHC", "years": [2013]}`.
- `/category` with an engine oil filter category link and `sort` `best_selling`: `total` 1,352, `sort_applied` "Best Selling", 57 pages of which 20 are served.
- `/brand` with `/shop/brands/a/super-start-platinum/super-start-platinum/ssb/ssbq`: 21 batteries at $264.99 plus a $22 core charge each, priced for Houston store 1058. `/brand` without input (4 credits): 916 brands with their links, 6 `top_brands` and 17 `featured_brands`.
- `/categories`: 34 departments (Accessories, ... Wipers & Components), `node_count` 1,334, each node {`hash`, `name`, `url` (the input of category), `requires_vehicle`, `children`}, and 8 `featured` (Batteries, Brake Pads & Shoes, ...).
- `/stores` `{"zip": "77002"}` (4 credits): 25 stores, the nearest store 4973 in Houston at 1.3 miles, `open_now`, `pickup_opens` "8:30 AM", seven `hours` rows; on 2026-11-23 Thursday read 7:30 AM to 5 PM with `adjustment` "holiday", and `services` {`hydraulic_hoses`, `paint_mixing`, `machine_shop`}. `{"state": "mo", "city": "springfield"}`: 13 stores with `store_number`, `phone`, `services` and the directory `url`. `{"country": "mx", "state": "jal"}`: 26 cities, `total_stores` 57; with `"city": "guadalajara"`: 13 stores, in Spanish.
- `/store` `{"store_id": "4973"}`: phone, address with county and ZIP+4, coordinates, hours and services. With a directory `url` (us or mx) the answer is {`store_number`, `name`, `url`, `phone`, `address` {`street`, `city`, `region`, `zip`, `country`}, `latitude`, `longitude`, `opening_hours`, `hours`, `services` (as the page lists them)}: Warren, AR store 1820; Ameca, Jalisco store 7730 in Spanish.
- `/suggestions` `{"query": "brake"}`: 8 part types ("brake pads", "brake rotors", ...), each with the category `url` to send to `/category`.
- `/rebates`: 23 rebates, e.g. "Bosch Wiper Blades" valid "October 28 - November 24, 2026", postmarked by December 24, 2026; Bar's Leaks Head Seal "$10 Prepaid Mastercard" valid all of 2026. `valid_from` / `valid_to` are read by Scavio from O'Reilly's text; `form_url` and `terms_url` are the PDFs.
- `/deals` (4 credits): 17 offers, e.g. "15% OFF $75+ WITH PROMO CODE: CLEAR15, Online Only" (`code` "CLEAR15", `validity_text` "11/20/26 – 11/23/26", maximum discount $50, ship to home only), plus the deals menu (`highlights`, `by_category`). Deals vary by store and some are online only: quote the details.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def oreilly(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/oreilly/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Another brand's number -> O'Reilly parts (4 credits without part type; 2 once both are known)
first = oreilly("cross-reference", {"part_number": "FL820S"})["data"]
if not first["items"] and first["manufacturers"]:
    print("manufacturers using it:", [m["id"] for m in first["manufacturers"]])
    first = oreilly("cross-reference", {
        "part_number": "FL820S",
        "part_type_id": first["part_type_id"],
        "manufacturer": "Motorcraft",
    })["data"]
store = first["priced_for"]
print("priced for store", store["store_id"], store["city"], store["state"])
for it in first["items"]:
    print(it["line_code"], it["part_number"], it["name"], it["price"], "+ core", it["core_charge"], it["warranty"])

# 2. Which stores near a ZIP can hand over the first match (4 credits; states, not counts)
if first["items"]:
    top = first["items"][0]
    stock = oreilly("store-stock", {"line_code": top["line_code"], "part_number": top["part_number"], "zip": "60540"})["data"]
    for s in stock["stores"][:5]:
        a = s["availability"]
        print(s["store_id"], s["address"]["city"], s["distance_miles"], "in store now" if a["in_store_now"] else "not in store", a["pickup_time"])

# Prices are for the store O'Reilly assigned (priced_for), and can differ by store and
# between calls. Store each answer with fetched_at and priced_for and run this on a
# schedule: that stored series is your price history (O'Reilly shows only the current price).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `country` and `language` (and `currency` on us).

- **item** (search, category, brand, cross-reference) - `position`, `product_id`, `line_code`, `part_number` (with `line_code`, the input of product, compatibility and store-stock), `name`, `brand` (the Brands facet label the name starts with; `null` when none), `url`, `image`, `category`, `price`, `regular_price`, `sale_price`, `on_sale`, `sale_type`, `discount_percent`, `clearance`, `core_charge`, `oil_fee`, `oil_deposit`, `currency`, `unit_of_measure`, `warranty`, `fit` (as O'Reilly gives it: `UNKNOWN`, `UNIVERSAL`, ...), `fit_notes` [{`name`, `description`}] (for the requested vehicle), `availability`, `deals` [{`title`, `description`, `ends`, `terms`}], `attributes` [{`name`, `value`}]. No rating.
- **lists** - `priced_for`, `vehicle_requested`, `vehicle` {`base_vehicle_id`, `year`, `make`, `model`} (as O'Reilly applied it), `title`, `total` (as O'Reilly reports it), `page`, `page_size` (24), `total_pages`, `max_page` (at most 20), `count`, `sort`, `sort_applied`, `brand`, `availability`, `filters`, `items[]`, `facets[]` {`name`, `param` (the key to send), `values[]` {`label`, `value` (the value to send), `url` (for facets that link to another list)}}, `notes`; a landing adds `links[]` {`name`, `url`}. Search adds `query`, `redirected_to`; category `category`, `url`; brand `brand_path`, `url`.
- **cross-reference** - `part_number`, `part_types[]` {`id`, `name`} and `manufacturers[]` {`id`, `name`} (when they were looked up; `null` when sent), `part_type_id`, `manufacturer`, `replacing_brands`, `priced_for`, `total`, `page`, `page_size`, `total_pages`, `count`, `items[]`, `facets[]`, `notes`.
- **product** - `requested`, `priced_for`, `line_code`, `part_number`, `name`, `brand`, `url`, `upc`, `unit_of_measure`, `category`, `part_type_id`, `universal`, the price fields, `warranty`, `availability`, `stock_status`, `deals[]`, `rebates[]` {`heading`, `title`, `description`}, `description`, `specifications[]` {`name`, `value`}, `image`, `images`, `documents[]` {`name`, `url`}, `breadcrumbs[]` {`name`, `url`}, `rating` {`average`, `count`} or `null`, `reviews[]` {`date`, `title`, `text`, `rating`} (the 10 most recent), `notes`; with `vehicle`, `vehicle_requested`, `vehicle`, `vehicle_fit` {`fits`, `universal`, `notes[]` {`name`, `description`, `per_vehicle_quantity`}, `documents`}.
- **vehicles** - `level`, `type_id`, `year`, `make_id`, `model_id`, `submodel_id`, `count` and `types[]`, `years`, or `makes` / `models` / `submodels` / `engines` [{`id`, `name`}]; `resolve`: `vehicle` {`base_vehicle_id`, `vehicle_id`, `type`, `subtype`, `year`, `make_id`, `make`, `model_id`, `model`, `submodel_id`, `submodel`, `engine_id`, `engine`, `slug`, `path`}; `vin`: `vin`, `vehicle` {`year`, `make_id`, `make`, `model_id`, `model`, `submodels[]`, `engines[]`}.
- **compatibility** - `line_code`, `part_number`, `make`, `count` and `makes[]`, or `models[]` {`model`, `engine`, `years`}.
- **categories** - `root`, `count`, `node_count`, `categories[]` {`hash`, `name`, `url`, `requires_vehicle`, `children[]`}, `featured[]` {`hash`, `name`, `url`}.
- **brand index** - `count`, `brands[]` {`name`, `url`}, `top_brands[]` and `featured_brands[]` {`name`, `url`, `image`}.
- **store-stock** - `line_code`, `part_number`, `quantity`, `zip`, `latitude`, `longitude`, `radius_miles` (50), `count`, `stores[]` {`store_id`, `address` {`line1`, `city`, `state`, `zip`}, `latitude`, `longitude`, `distance_miles`, `hours_message`, `closed_all_week`, `availability` {`store_pickup`, `in_store_now`, `pickup_time`, `message_hidden`}}, `notes`.
- **stores** - near a ZIP or point: `zip`, `latitude`, `longitude`, `radius_miles`, `count`, `stores[]` {`store_id`, `phone`, `address` {`line1`, `line2`, `city`, `county`, `state`, `zip`, `zip4`, `country`}, `latitude`, `longitude`, `distance_miles`, `open_now`, `hours_message`, `closed_all_week`, `pickup_opens`, `hours[]` {`day`, `open`, `close`, `closed`, `adjustment`}, `services` {`hydraulic_hoses`, `paint_mixing`, `machine_shop`}}. Directory: `state`, `city`, `source` (`state` or `city`), `count`, `total_stores` and `cities[]` {`city`, `city_slug`, `store_count`, `store_number` and `url` (cities with one store)}, or `stores[]` {`store_number`, `name`, `address`, `city_state`, `phone`, `services`, `url`}.
- **store** - us by `store_id`: the near-a-ZIP store shape. By `url` or mx: `store_number`, `name`, `url`, `phone`, `address` {`street`, `city`, `region`, `zip`, `country`}, `latitude`, `longitude`, `opening_hours`, `hours[]` {`day`, `open`, `close`}, `services`.
- **suggestions** - `query`, `count`, `suggestions[]` {`name`, `type` (`part_type`), `url`}.
- **rebates** - `count`, `rebates[]` {`title`, `details`, `valid_text`, `valid_from`, `valid_to`, `postmark_by`, `keywords`, `categories`, `terms_url`, `form_url`, `redeem_online_url`}, `notes`.
- **deals** - `count`, `offers[]` {`section`, `title`, `code`, `validity_text`, `details`, `url`, `image`, `image_text`}, `highlights[]` {`title`, `description`, `url`}, `by_category[]` {`title`, `url`}, `notes`.

## Guardrails

- Name it "O'Reilly Auto Parts (oreillyauto.com, the US auto parts retailer)" on first mention. This is the retail site, not O'Reilly Pro, First Call Online or commercial pricing, and not O'Reilly Media.
- Prices: quote `price`, `core_charge`, `warranty`, deals and rebates with the `priced_for` store and the `fetched_at` date. Never call a price national or "O'Reilly's price" without the store; never carry one store's price to another.
- Comparing O'Reilly with AutoZone: compare only the same part (same brand and part number) on both, each with its own `priced_for` store and date. A cross-referenced O'Reilly part is O'Reilly's equivalent, not the same product: say so, and never call one store cheaper than the other beyond the two numbers shown.
- Core charge: a refundable deposit shown separately from the price. Rebates: a mail-in or online claim with a postmark date, shown next to the price, never subtracted from it. Never invent an amount.
- Fitment: a vehicle list (search or category with `vehicle`) is the fit answer, at year / make / model with `fit_notes`. `vehicle_fit.fits` `null` means the product page gave no fit details, not that the part does not fit. Never promise a fit to a specific engine or VIN beyond what `fit_notes` say.
- Lists: 24 per page up to 20 pages; never call one page or 480 items "all parts" or present `total` as what was returned.
- Stock: availability states as O'Reilly reported them at the moment of the call; never a unit count. Scavio makes no promise of their accuracy.
- Reviews: the 10 most recent and the rating. No reviewer names or identities are returned; never try to identify a reviewer.
- Mexico data: translate Spanish store names, addresses and services for the user and keep the original values in quotes and outputs.
- Not available: unit counts in store stock, a chosen store for prices, reviews past the 10 most recent (no paging, sort or star filter), Q&A, Mexico prices or catalog, Canada, license-plate lookup, the weekly / current ad, repair guides and trouble codes, O'Reilly Pro / First Call Online commercial pricing, price history (poll and store), checkout, cart, ordering or reservations. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not collect or store O'Reilly data: each call fetches the public O'Reilly page at the moment the request asks for it and returns what it shows as JSON, with no response cache. O'Reilly's terms cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish O'Reilly product photos, logos or reviewer details; link products by `url` instead.
- Never fabricate prices, core charges, warranties, cross-references, fitment, availability, stores, hours, rebates, deals, reviews or ratings. Only return what the API returned, with the `fetched_at` time, the `priced_for` store and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` outside us, mx, or `mx` on any endpoint but stores and store; `page` above 20; more than 4 `filters` or a filter key that is not a facet `param`; an unknown `sort` or `availability`; both or neither of `url` / `line_code` + `part_number` on product; a malformed line code, part number, `part_type_id`, VIN (17 characters, no I, O or Q), ZIP (5 digits) or category hash; a vehicle level without the ids it needs; `latitude` without `longitude`; `city` without `state`; list inputs on `/brand` without `brand`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "O'Reilly has no product at this link.", "O'Reilly lists no product <line> <part> (line code and part number as items[] give them).", "O'Reilly has no category at this path (check the hash: categories lists them).", "O'Reilly has no brand page at this path (brand without input lists them).", "O'Reilly could not decode this VIN.", "O'Reilly has no vehicle with these ids (take them from the years, makes, models, submodels and engines levels).", "O'Reilly's store finder does not know ZIP <zip>.", "O'Reilly's store directory has no such state.", "O'Reilly has no store <id>.". Take ids, links, codes and slugs from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api).
- `502` means O'Reilly data was temporarily unavailable ("O'Reilly Auto Parts is temporarily unavailable. Please try again."), or O'Reilly answered for a vehicle that was not requested ("O'Reilly answered for a vehicle that was not requested. Please retry."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means O'Reilly is busy ("O'Reilly Auto Parts is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.78.0
npm install scavio@0.79.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: xref } = await scavio.oreilly.crossReference({ part_number: "PH3614", part_type_id: "02269", manufacturer: "FRAM" });
const { data: fits } = await scavio.oreilly.search({ query: "brake pads", vehicle: { base_vehicle_id: 129927 } });
const { data: product } = await scavio.oreilly.product({ line_code: "MOB", part_number: "1-5-30-5QT" });
const { data: stock } = await scavio.oreilly.storeStock({ line_code: "SSB", part_number: "48PLT", zip: "60540" });
const { data: vin } = await scavio.oreilly.vehicles({ level: "vin", vin: "1HGCM82633A004352" });
const { data: models } = await scavio.oreilly.compatibility({ line_code: "BB", part_number: "SC1001", make: "Ford" });
const { data: filters } = await scavio.oreilly.category({ category: "https://www.oreillyauto.com/shop/b/filters/engine-oil-filter/80c2d8dbb188", sort: "best_selling" });
const { data: menu } = await scavio.oreilly.categories();
const { data: brand } = await scavio.oreilly.brand({ brand: "/shop/brands/a/super-start-platinum/super-start-platinum/ssb/ssbq" });
const { data: near } = await scavio.oreilly.stores({ zip: "77002" });
const { data: store } = await scavio.oreilly.store({ store_id: "4973" });
const { data: hints } = await scavio.oreilly.suggestions({ query: "brake" });
const { data: rebates } = await scavio.oreilly.rebates();
const { data: deals } = await scavio.oreilly.deals();
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.oreilly.search(...)`, `cross_reference`, `product`, `vehicles`, `compatibility`, `category`, `categories`, `brand`, `store_stock`, `stores`, `store`, `suggestions`, `rebates` and `deals`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 14 endpoints as tools: `search_oreilly`, `get_oreilly_cross_reference`, `get_oreilly_product`, `get_oreilly_vehicles`, `get_oreilly_compatibility`, `get_oreilly_category`, `get_oreilly_categories`, `get_oreilly_brand`, `get_oreilly_store_stock`, `get_oreilly_stores`, `get_oreilly_store`, `get_oreilly_suggestions`, `get_oreilly_rebates` and `get_oreilly_deals`. O'Reilly is opt-in: add `oreilly` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.78.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,oreilly"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/oreilly-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [cross-reference](https://scavio.dev/docs/oreilly-cross-reference?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [product](https://scavio.dev/docs/oreilly-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [vehicles](https://scavio.dev/docs/oreilly-vehicles?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [compatibility](https://scavio.dev/docs/oreilly-compatibility?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [category](https://scavio.dev/docs/oreilly-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [categories](https://scavio.dev/docs/oreilly-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [brand](https://scavio.dev/docs/oreilly-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [store stock](https://scavio.dev/docs/oreilly-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [stores](https://scavio.dev/docs/oreilly-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [store](https://scavio.dev/docs/oreilly-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [suggestions](https://scavio.dev/docs/oreilly-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [rebates](https://scavio.dev/docs/oreilly-rebates?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api), [deals](https://scavio.dev/docs/oreilly-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api). Overview: [O'Reilly Auto Parts API](https://scavio.dev/oreilly-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api).
