# AutoZone API - Parts by Vehicle, Prices, Core Charges, Reviews

Read AutoZone (autozone.com, the US auto parts retailer): the parts of a part type that fit a vehicle, keyword and part-number search, brand and clearance lists, one product in full, customer reviews, the vehicle selector, mail-in rebates, the category menu and the store directory, plus AutoZone Brazil (autozone.com.br) search, product and store stock and the AutoZone Mexico (autozone.com.mx) store directory, vehicles and categories. All 12 endpoints return structured JSON at 1 credit per call (2 on Brazil search, product and store stock).

This is the retail site autozone.com. It is not AutoZonePro (autozonepro.com, AutoZone's commercial login site for repair shops and fleets): commercial pricing is not read.

**The job this skill is for: AutoZone parts prices by vehicle.** What fits a year / make / model, at what price at an AutoZone store, with the core charge, the warranty and pickup. Batteries first, then brake pads: on 2026-11-22 AutoZone listed 307 batteries unfiltered and 47 for a 2015 Honda Civic (10 vehicle-specific; the other 37 are universal batteries AutoZone lists for every vehicle and marks MAY_NOT_FIT) - filter `universal_or_specific_fit_s: VEHICLE_SPECIFIC` for only the vehicle-specific ones; the first, a Duralast Gold 51R (`51R-DLG`), read $219.99 plus a $22 core charge with "3 Year Warranty" and 6 for pickup, priced for AutoZone store 6229 in Phoenix, AZ.

Nine limits shape every answer, so say them plainly:
- **1 credit per call; 2 on Brazil search, product and store stock.** A not-found (an unknown item id, an unknown vehicle, an unknown brand, state, city or store) is a `404` and is charged. A refused input (`400`) and an upstream failure (`502`, `503`) are not charged.
- **Every price is for one store, the one AutoZone assigns to the request.** `priced_for` {`store_number`, `address`, `city`, `state`, `zip`} names it. AutoZone prices differ by store (core charges too), so the same item can cost more or less at another store, and two calls can be priced for different stores. There is no store or ZIP input on us. Report "$219.99 at AutoZone store 6229 (Phoenix, AZ) on 2026-11-22", never a national price.
- **Lists show the first 24 results only.** search, category, brand and clearance return AutoZone's first 24 with AutoZone's `total`; `page` is 1 only (a page above 1 is a `400`, not charged). Narrow instead: a vehicle, one facet, `min_price` / `max_price` or a price sort. Never call 24 items "all".
- **One facet at a time.** `filters` takes one facet (`brand` counts as one), plus a price range. AutoZone's pages apply one at a time.
- **Vehicle fit is year / make / model.** `vehicle` in `/category` takes the names `/vehicles` lists (`{"year": 2018, "make": "Ford", "model": "F-150"}`). Items AutoZone ties to an engine read `fitment.vehicle_fit` `NEEDS_BASE_VEHICLE`: they fit some engine of that model, and AutoZone's engine step is not applied. Engine-level fitment and VIN lookup are not offered; the product page has no per-vehicle fit list.
- **Part numbers cross-reference.** search takes AutoZone part numbers and other brands' or OEM numbers: `PH3614` (a FRAM oil filter) answered `part_number_search` true, `match_type` "We ID match" and 16 parts, the FRAM filter itself plus parts that carry `oem_part_number` "PH3614", `oem_brand` "Fram".
- **Three markets, different scope.** `country` `us` (default) serves all 12 endpoints except store stock; `br` serves search, product, store-stock, vehicles, stores, store and categories; `mx` serves vehicles, stores, store and categories only (Mexico search and product are a `400`: AutoZone Mexico prices only for a Mexican store it does not reliably assign).
- **Store stock at a chosen store is Brazil only.** `/store-stock` reads one autozone.com.br product at a Brazilian store you pick, with its quantity. US and Mexico stock at a chosen store is not offered: on us, `availability.store_pickup` is the assigned store's pickup quantity only.
- **No stores near a ZIP.** `/stores` is AutoZone's directory, state, then city, then stores; `/store` is one store. There is no search by ZIP, address or coordinates.

AutoZone has no public developer API. Commercial accounts order through AutoZonePro and their shop software, and suppliers connect over EDI. Retail prices, fitment and store pickup are shown on autozone.com; this skill reads those public pages with one Scavio key.

AutoZone, Inc. ran 8,031 stores at the end of August 2026 (6,863 in the US, 1,001 in Mexico, 167 in Brazil) and reported $20.3 billion in net sales for fiscal 2026 (AutoZone 10-K). Quote these with their source, never from the samples.

See also: for Harbor Freight tools and its clearance use `harbor-freight-api`; for the same battery at Walmart use `walmart-product-data`; for parts on Amazon use `amazon-product-data`; for Mercado Livre in Brazil use `mercadolibre-product-data`; for prices across retailers use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Find the AutoZone parts that fit a vehicle (year, make, model) in a part type, with prices: batteries, brake pads, rotors, oil filters, spark plugs, wiper blades
- Read an AutoZone price with its core charge, warranty, deal price and pickup or delivery options
- Look up a part number at AutoZone, or cross-reference another brand's or an OEM part number to the parts AutoZone matches to it
- Compare AutoZone's brand ladder for one part (Duralast, Duralast Gold, Duralast Elite, other brands) by price and warranty
- Read one AutoZone product in full: specifications, features, safety data sheets, rating distribution
- Read AutoZone customer reviews, with AutoZone's review summary and the reviewer's vehicle
- List AutoZone's vehicle years, makes, models, submodels or engines
- List AutoZone's clearance items or current mail-in rebates
- Find AutoZone stores in a state or city with opening hours and holiday hours (US, Brazil, Mexico)
- Check an AutoZone Brazil product's quantity at a Brazilian store, or search autozone.com.br in BRL

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 1 credit; Brazil search, product and store stock cost 2.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, vehicles took 1-12 seconds, reviews 2-14, stores, store and categories 4-21, search, category and product 7-26, brand 11-26, clearance and rebates 5-25, and Brazil store stock 5-19. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Markets | Credits |
|---|---|---|---|
| `POST /api/v1/autozone/search` | Keywords or a part number (cross-reference included): the first 24 results with total, facets and `priced_for` | us, br | 1; br 2 |
| `POST /api/v1/autozone/product` | One product by item id or link: price, was / deal price, core charge, warranty, deal, availability per fulfilment option, specifications, features, safety data sheets, rating distribution | us, br | 1; br 2 |
| `POST /api/v1/autozone/category` | One part type's products, optionally only those that fit a vehicle (year / make / model); first 24 with total and facets | us | 1 |
| `POST /api/v1/autozone/brand` | One brand's products, optionally within one part type; first 24 with total | us | 1 |
| `POST /api/v1/autozone/vehicles` | The vehicle selector one level at a time: years, makes, models, submodels, engines | us; br, mx (years, makes, models) | 1 |
| `POST /api/v1/autozone/reviews` | One product's reviews, 10 a page at full depth, sorted, filtered by stars, with AutoZone's review summary on page 1 | us | 1 |
| `POST /api/v1/autozone/stores` | The store directory: states, then cities of a state, then the stores of a city with hours and holiday hours | us, br, mx | 1 |
| `POST /api/v1/autozone/store` | One store by slug or link: address, phone, coordinates, hours, holiday hours | us, br, mx | 1 |
| `POST /api/v1/autozone/categories` | The category menu (23 departments on us, br and mx) with part type paths and AutoZone's popular part types | us, br, mx | 1 |
| `POST /api/v1/autozone/clearance` | AutoZone's clearance list; first 24 with total | us | 1 |
| `POST /api/v1/autozone/rebates` | Current mail-in rebates with end date, postmark date and the form link | us | 1 |
| `POST /api/v1/autozone/store-stock` | One autozone.com.br product at a Brazilian store you choose: price, core charge and in-store quantity | br only | 2 |

## Markets

| `country` | Site | Language, currency | Endpoints |
|---|---|---|---|
| `us` (default) | autozone.com | English, USD | all but `/store-stock` |
| `br` | autozone.com.br | Portuguese, BRL | `/search`, `/product`, `/store-stock` (its default), `/vehicles` (years, makes, models), `/stores`, `/store`, `/categories` |
| `mx` | autozone.com.mx | Spanish | `/vehicles` (years, makes, models), `/stores`, `/store`, `/categories` |

- Every answer echoes `country`, `language` and `currency`. Any other market, or a market an endpoint does not serve, is a `400`, not charged.
- Brazil prices are for AutoZone store 7602, São Paulo (Interlagos), unless `/store-stock` asks for another store; `priced_for` says which store priced the answer. Names, part types, locations and facet labels come back in Portuguese as AutoZone writes them (`Pastilha de Freio`, `Traseiro` = rear): translate them for the user, never alter the values.
- A product or store link carries its own market: send it alone, or with a `country` that agrees with it.
- AutoZone's Brazilian and Mexican sites show no reviews, so `/reviews` is us only. `/category`, `/brand`, `/clearance` and `/rebates` are us only.

## Prices, core charges and warranty

Every priced item (search, category, brand, clearance, product, store stock) carries:

| Field | Meaning |
|---|---|
| `price` | AutoZone's price at the `priced_for` store |
| `was_price` | AutoZone's struck-through price, as shown, or `null` |
| `deal_price` | AutoZone's deal price, or `null`. On product, `deal` {`available`, `price`, `label` (e.g. "Bundle and Save"), `quantity`} |
| `discount_percent` | Computed by Scavio from `was_price`; `null` without one |
| `core_charge` | The refundable core deposit; `0` when there is none |
| `warranty` | AutoZone's warranty text, as given ("3 Year Warranty", "Limited-Lifetime Warranty", "1 Year Warranty") |
| `clearance` | Whether AutoZone marks the item clearance |
| `availability` | `store_pickup` {`available`, `quantity`} at the `priced_for` store, `ship_to_home` {`available`, `quantity`, `estimated_delivery`}, `next_day` {`available`, `quantity`, `order_cutoff`, `estimated_delivery`}, `same_day` {`available`, `quantity`}, `sister_stores_available`, `sister_store_count` |

- **Core charge.** AutoZone adds a core charge on parts such as batteries until the old part (the core) is returned. AutoZone's 10-K: customers are not charged for the core if a used core is returned when the new part is bought; otherwise AutoZone charges a specified amount for it and refunds that same amount when a used core is returned to the store later. Quote `core_charge` as a refundable deposit on top of `price`, at that store. Captured 2026-11-22: car batteries read $22 (Duralast Gold 51R at $219.99 in Phoenix; Duralast 35 `35-DL` at $184.99 in Lombard, IL); Duralast Gold AGM powersport batteries read $10; a Moura battery on autozone.com.br read BRL 150 on BRL 3,478. Never state an amount that is not in the answer.
- **Warranty.** Quote `warranty` as AutoZone gives it. AutoZone's Battery Limited Warranty (United States only, autozone.com terms) sets these free-replacement periods: Duralast Platinum Elite 5 years, Duralast Platinum AGM 4 years, Duralast Platinum EFB 3 years, Duralast Gold 3 years, Duralast 2 years, TotalPro 1 year, Econocraft 90 days, Optima Yellow / Red Top 3 years, Odyssey Extreme 4 years; "This warranty expires when you sell or transfer your vehicle." Cite it as AutoZone's terms; read the item's own `warranty` first (powersport batteries read "6 Month Warranty").
- **Stock** is as AutoZone reports it for that store, at the moment of the call; Scavio makes no promise of its accuracy.
- List items carry no rating; `/product` has `rating`.
- Prices differ by store: describe differences between two answers from their `priced_for` stores and numbers, never why, and never call a discount real or fake.

## Workflow

1. **Vehicle:** `/vehicles` with `level` `years`, then `makes` (`year`), then `models` (`year` + `make_id`); keep the make and model `name`s. `submodels` and `engines` (`year` + `make_id` + `model_id`, us) tell the user which engines exist; they do not filter category.
2. **Part type:** a path from `/categories` (`children[].path` where `has_products` is true, or `popular[].path`: Battery `/batteries-starting-and-charging/battery`, Brake Pads `/brakes-and-traction-control/brake-pads`), from a product's `breadcrumbs` (`page_type` `PartGroup`), or the AutoZone link. A grouping page answers `list_type` `group` with no items: pick a part type under it.
3. **Parts that fit:** `/category` with `category` and `vehicle` {`year`, `make`, `model`}. Compare `total` against the same call without `vehicle`.
4. **Narrow the 24:** one facet from `facets[]` (`{"position_name_s": "Front"}`, `{"sub_brand_name_display_s": "Duralast Gold"}`, `{"padbattr_facet_3_s": "Ceramic"}`), `min_price` / `max_price`, or `sort` `price_asc` / `price_desc`. One narrowing per call; several calls for several cuts (1 credit each).
5. **Part number:** `/search` with the number (`DG1210`, `PH3614`, `FL-820S`); `oem_part_number` / `oem_brand` show the number a result was matched to.
6. **Detail:** `/product` with `id` (`items[].id`) for specifications, features, safety data sheets, the deal and `rating`.
7. **Reviews:** `/reviews` with `id`; page 1 adds AutoZone's review summary.
8. **Stores:** `/stores` (states), `/stores` with `state` (cities), `/stores` with `state` + `city` (stores), then `/store` with a `slug` for phone and coordinates.
9. **Brazil store stock:** `/search` with `country` `br`, `/stores` with `country` `br` for a `store_number`, then `/store-stock` with `id` and `store_number`.
10. **Watching prices:** there is no history. Poll the same items on a schedule and store each answer with its `fetched_at` and `priced_for`; that stored series is the history. Compare only answers priced for the same store.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords, an AutoZone part number (`DG1210`) or another brand's / OEM part number (`PH3614`, `FL-820S`); 1-200 chars. Brazil: Portuguese keywords (`pastilha de freio`) |
| `country` | string | `us` | `us` or `br` (2 credits); `mx` is a `400` |
| `sort` | string | `relevance` | `relevance` (AutoZone's own order), `price_asc`, `price_desc` |
| `brand` | string | none | A brand as `facets` lists it (`Duralast Gold`); the same as `filters.sub_brand_name_display_s`. Counts as the one facet |
| `filters` | object | none | One facet: `{"<facets[].facet>": "<facets[].values[].value>"}` |
| `min_price` / `max_price` | number | none | Price band in the market's currency (USD; BRL on br) |
| `page` | integer | 1 | Only 1 |

`ranking_variant` names the search ranking AutoZone served: AutoZone runs ranking tests, so `total` and order can differ between two identical calls. A search AutoZone sends straight to one product page answers `redirected_to` and `redirect_product_id` with no items: send that id to `/product`. `corrected_query` shows a spelling AutoZone corrected.

### Category (`/category`), brand (`/brand`), clearance (`/clearance`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category` | string | category: required; brand: optional | A part type path (`/brakes-and-traction-control/brake-pads`) or its AutoZone link. On `/brand`, narrows the brand to that part type (`/brakes-and-traction-control/brake-rotor`) |
| `vehicle` | object | none | Category only: `{"year": 2018, "make": "Ford", "model": "F-150"}`, names as `/vehicles` lists them. An unknown make or model for that year is a charged `404` |
| `brand` | string | brand: required | A brand slug (`duralast`, `duralast-gold`, `mobil-1`) or its AutoZone link |
| `sort` / `filters` / `min_price` / `max_price` | | | Category: as in search |
| `page` | integer | 1 | Only 1 |

Clearance takes no input besides `country` (us). Category and brand serve us only.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `id` | string or integer | one of | AutoZone item id (`items[].id`, the number at the end of the product link: `1399158`) |
| `url` | string | one of | A product link (`https://www.autozone.com/p/<name>/<id>`, or autozone.com.br); the market comes from the link. Send exactly one of `id`, `url` |
| `country` | string | `us` | `us` or `br` (2 credits) with `id` |

### Vehicles (`/vehicles`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `level` | string | `years` | `years`, `makes` (needs `year`), `models` (`year` + `make_id`), `submodels` and `engines` (`year` + `make_id` + `model_id`; us only) |
| `year` | integer | none | From `years` |
| `make_id` | integer | none | `makes[].make_id` (54 = Ford on us) |
| `model_id` | integer | none | `models[].model_id` (666 = F-150) |
| `country` | string | `us` | `us`, `br` or `mx` (years, makes, models) |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `id` / `url` | | one of | The product's item id or link |
| `page` | integer | 1 | 10 reviews a page; `total_pages` says how deep they go |
| `sort` | string | `default` | `default` (AutoZone's order), `most_recent`, `most_helpful` |
| `stars` | array | none | Only these star ratings (`[1, 2]`) |

### Stores (`/stores`), store (`/store`), categories (`/categories`), rebates (`/rebates`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `us` | Stores, store, categories: `us`, `br` or `mx`. Rebates: us |
| `state` | string | none | Stores: a state from the states list (`states[].state`: `tx`, `vt`, `sao-paulo`, `nuevo-leon`): lists its cities |
| `city` | string | none | Stores, with `state`: a city slug (`cities[].city_slug`: `houston`): lists its stores |
| `slug` / `url` | string | one of | Store: a store slug (`stores[].slug`: `vt/barre/18-overlook-dr.html`) or the store page link. A store number alone is not an input |

### Store stock (`/store-stock`, Brazil)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `id` / `url` | | one of | An AutoZone Brazil item id (`items[].id` from a br search: `100123563`) or the autozone.com.br product link |
| `store_number` | string or integer | required | A Brazilian store number (`stores[].store_number` with `country` `br`: `7602`) |
| `country` | string | `br` | `br` only; `us` / `mx` are a `400` |

## Examples

### Parts that fit a vehicle

```bash
curl -X POST https://api.scavio.dev/api/v1/autozone/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category": "/brakes-and-traction-control/brake-pads", "vehicle": {"year": 2018, "make": "Ford", "model": "F-150"}}'
```

Captured `data` (2026-11-22, 1 credit; 2 of 24 items and 3 of 7 facets shown, `image` dropped, the Brand facet cut to 3 values):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "category": "/brakes-and-traction-control/brake-pads",
  "filters": {},
  "min_price": null,
  "max_price": null,
  "sort": "relevance",
  "requested_vehicle": { "year": 2018, "make": "Ford", "model": "F-150" },
  "priced_for": { "store_number": "1528", "address": "2125 ROCHELLE RD", "city": "IRVING", "state": "TX", "zip": "75062" },
  "list_type": "products",
  "page_type": "ProductShelf",
  "title": "Brake Pads",
  "vehicle": { "year": 2018, "make": "Ford", "model": "F-150" },
  "total": 59,
  "count": 24,
  "page_size": 24,
  "items": [
    {
      "position": 1,
      "id": "1115999",
      "part_number": "D2087",
      "name": "Duralast Ceramic Brake Pads D2087",
      "brand": "Duralast",
      "sub_brand": "Duralast",
      "part_type": "Brake Pads",
      "url": "https://www.autozone.com/p/duralast-disc-brake-pad-set-d2087/1115999",
      "location": "Front",
      "fitment": { "type": "VEHICLE_SPECIFIC", "vehicle_fit": "NEEDS_BASE_VEHICLE" },
      "oem_part_number": null,
      "oem_brand": null,
      "attributes": { "Mounting Hardware Included": "No", "Pad Type": "Ceramic" },
      "sponsored": false,
      "price": 52.99,
      "was_price": null,
      "deal_price": null,
      "discount_percent": null,
      "core_charge": 0,
      "currency": "USD",
      "warranty": "Limited-Lifetime Warranty",
      "clearance": false,
      "availability": {
        "store_pickup": { "available": true, "quantity": 2 },
        "ship_to_home": { "available": true, "quantity": 306, "estimated_delivery": "Nov. 24" },
        "next_day": { "available": true, "quantity": 1, "order_cutoff": "2026-11-23T20:00:00-06:00", "estimated_delivery": "2026-11-24T12:10:15.099-06:00" },
        "same_day": { "available": true, "quantity": 2 },
        "sister_stores_available": false,
        "sister_store_count": 0
      }
    },
    {
      "position": 2,
      "id": "749413",
      "part_number": "MKD1790",
      "name": "Duralast Ceramic Brake Pads MKD1790",
      "brand": "Duralast",
      "sub_brand": "Duralast",
      "part_type": "Brake Pads",
      "url": "https://www.autozone.com/p/duralast-disc-brake-pad-set-mkd1790/749413",
      "location": "Rear",
      "fitment": { "type": "VEHICLE_SPECIFIC", "vehicle_fit": "NEEDS_BASE_VEHICLE" },
      "oem_part_number": null,
      "oem_brand": null,
      "attributes": { "Mounting Hardware Included": "No", "Pad Type": "Ceramic" },
      "sponsored": false,
      "price": 44.99,
      "was_price": null,
      "deal_price": null,
      "discount_percent": null,
      "core_charge": 0,
      "currency": "USD",
      "warranty": "Limited-Lifetime Warranty",
      "clearance": false,
      "availability": {
        "store_pickup": { "available": true, "quantity": 2 },
        "ship_to_home": { "available": true, "quantity": 369, "estimated_delivery": "Nov. 24" },
        "next_day": { "available": true, "quantity": 2, "order_cutoff": "2026-11-23T20:00:00-06:00", "estimated_delivery": "2026-11-24T12:10:15.103-06:00" },
        "same_day": { "available": true, "quantity": 2 },
        "sister_stores_available": false,
        "sister_store_count": 0
      }
    }
  ],
  "facets": [
    { "facet": "available_stores_ss", "name": "Pick Up Today", "values": [{ "value": "1528", "label": "Pick Up In Store", "count": 9, "selected": false }] },
    { "facet": "sub_brand_name_display_s", "name": "Brand", "values": [{ "value": "Duralast", "label": "Duralast", "count": 3, "selected": false }, { "value": "Duralast Gold", "label": "Duralast Gold", "count": 3, "selected": false }, { "value": "Duralast Elite", "label": "Duralast Elite", "count": 3, "selected": false }] },
    { "facet": "position_name_s", "name": "Location", "values": [{ "value": "Rear", "label": "Rear", "count": 39, "selected": false }, { "value": "Front", "label": "Front", "count": 20, "selected": false }] }
  ],
  "notes": [
    "Vehicle fit is at year / make / model level: items AutoZone ties to an engine read fitment.vehicle_fit NEEDS_BASE_VEHICLE, as AutoZone gives it.",
    "AutoZone's page lists the first 24 of 59 products. Narrow with a vehicle, filters, min_price / max_price or sort."
  ]
}
```

The same part type without `vehicle` read `total` 19,853 (priced for a Dallas store); for the 2018 F-150 it read 59, of which `Location` splits 39 rear and 20 front. The 24 items shown ranged from $29.49 to $99.99 at Irving store 1528. The `Pick Up Today` facet's value is the assigned store's number: send it as the one facet to keep items that store can hand over today. `NEEDS_BASE_VEHICLE` means AutoZone ties the pad to an engine of that model: tell the user to confirm the engine on AutoZone before buying.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/autozone/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "1399158"}'
```

Captured `data` (2026-11-22, 1 credit; `description`, `images` and 6 of 9 `specifications` dropped, `features` cut to 3):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "requested_id": "1399158",
  "priced_for": { "store_number": "5267", "address": "745 SECAUCUS RD", "city": "JERSEY CITY", "state": "NJ", "zip": "07307" },
  "id": "1399158",
  "part_number": "D3THJ",
  "name": "Duralast 3 Ton Hybrid Floor Jack",
  "brand": "Duralast",
  "sub_brand": "Duralast",
  "part_type": "Floor Jack",
  "url": "https://www.autozone.com/p/duralast-floor-jack-d3thj/1399158",
  "brand_path": "/brands/duralast",
  "features": ["Light Weight Aluminum Design - engineered 25% lighter", "Double Pump Piston design reaches lift point 75% faster", "Lift Range: 4\" - 18.5\""],
  "specifications": [{ "name": "Maximum Extended Height", "value": "18.5 in" }, { "name": "Weight Capacity", "value": "3 T" }, { "name": "Collapsed Height", "value": "4 in" }],
  "breadcrumbs": [
    { "name": "Tools & Garage Equipment", "path": "/tools-and-equipment", "page_type": "TopLevel" },
    { "name": "Jacks & Jack Stands", "path": "/tools-and-equipment/jacks-jack-stands", "page_type": "LeafCategory" },
    { "name": "Floor Jack", "path": "/engine-and-vehicle-lift/jack", "page_type": "PartGroup" }
  ],
  "safety_data_sheets": ["https://contentassets.autozone.com/safety_data_sheet/USA/1399158.pdf"],
  "fitment": { "type": "UNIVERSAL", "vehicle_fit": "FITS" },
  "location": null,
  "price": 219.99,
  "was_price": null,
  "deal_price": 199.99,
  "discount_percent": null,
  "core_charge": 0,
  "warranty": "1 Year Warranty",
  "clearance": false,
  "deal": { "available": true, "price": 199.99, "label": null, "quantity": 1 },
  "availability": {
    "store_pickup": { "available": true, "quantity": 1 },
    "ship_to_home": { "available": true, "quantity": 6, "estimated_delivery": "Nov. 24" },
    "next_day": { "available": true, "quantity": 1, "order_cutoff": "2026-11-23T18:00:00-06:00", "estimated_delivery": "2026-11-24T12:09:53.242-06:00" },
    "same_day": { "available": false, "quantity": 0 },
    "sister_stores_available": false,
    "sister_store_count": 0
  },
  "rating": {
    "average": 4.48,
    "count": 106,
    "with_text": 45,
    "ratings_only": 61,
    "recommended_percent": 83,
    "distribution": [
      { "stars": 5, "count": 84, "percent": 79 },
      { "stars": 4, "count": 9, "percent": 8 },
      { "stars": 3, "count": 2, "percent": 1 },
      { "stars": 2, "count": 2, "percent": 1 },
      { "stars": 1, "count": 9, "percent": 8 }
    ]
  }
}
```

$219.99 with a deal price of $199.99 at Jersey City store 5267. A battery answers the same shape with its core charge: item `4474` (Duralast 35 `35-DL`) read $184.99, `core_charge` 22, "2 Year Warranty" and 11 for pickup at Lombard, IL store 2563. An unknown id answers `404` ("AutoZone has no product 99999917 on autozone.com (or the id does not exist)."), charged.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/autozone/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "1399158"}'
```

Captured `data` (2026-11-22, 1 credit; 1 of 10 reviews shown, the summary text and features cut):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "id": "1399158",
  "sort": "default",
  "stars": [],
  "page": 1,
  "page_size": 10,
  "total_reviews": 105,
  "total_matching": 105,
  "total_pages": 11,
  "has_more": true,
  "average_rating": 4.5,
  "rating_distribution": [
    { "stars": 5, "count": 84, "percent": 80 },
    { "stars": 4, "count": 8, "percent": 8 },
    { "stars": 3, "count": 2, "percent": 2 },
    { "stars": 2, "count": 2, "percent": 2 },
    { "stars": 1, "count": 9, "percent": 8 }
  ],
  "summary": {
    "text": "Customers overwhelmingly praise this floor jack for its reliability, ease of use, and sturdy construction. ...",
    "features": [{ "name": "price", "mentions": 6, "positive": 4, "negative": 1 }, { "name": "ease of use", "mentions": 5, "positive": 5, "negative": 0 }]
  },
  "count": 10,
  "reviews": [
    {
      "review_id": "409274590",
      "rating": 4,
      "title": null,
      "text": "Works as it should.",
      "verified_purchase": true,
      "vehicle": "2012 Dodge Challenger",
      "helpful_votes": 0,
      "not_helpful_votes": 0,
      "images": []
    }
  ]
}
```

(Review fields `recommends`, `incentivized`, `syndicated`, `syndicated_from` and `submitted_at` dropped in this excerpt.) `summary` is AutoZone's own review summary, on page 1 without a star filter (`null` if AutoZone shows none); say it is AutoZone's. `vehicle` is the reviewer's vehicle as they wrote it, not a verified fitment. Reviews go to full depth: the Duralast 35 battery had 5,765 reviews in 577 pages. `stars` `[1, 2]` keeps the low ratings and `total_matching` counts them.

### Brazil store stock

```bash
curl -X POST https://api.scavio.dev/api/v1/autozone/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "100112748", "store_number": "9403"}'
```

Captured `data` (2026-11-22, 2 credits):

```json
{
  "country": "br",
  "language": "pt",
  "currency": "BRL",
  "requested_id": "100112748",
  "store_number": "9403",
  "priced_for": { "store_number": "9403", "address": "AVENIDA RIO DAS PEDRAS, 1488", "city": "São Paulo", "state": "SP", "zip": "03452-100" },
  "id": "100112748",
  "part_number": "31045065",
  "name": "Óleo de Motor 5W30 Sintetico SQ Havoline 4L",
  "brand": "Havoline",
  "url": "https://www.autozone.com.br/p/havoline-oleo-do-motor-31045065/100112748",
  "price": 193.99,
  "was_price": null,
  "deal_price": null,
  "core_charge": 0,
  "in_store": { "available": true, "quantity": 2 },
  "availability": {
    "store_pickup": { "available": true, "quantity": 2 },
    "ship_to_home": { "available": false, "quantity": 0, "estimated_delivery": null },
    "next_day": { "available": null, "quantity": 0, "order_cutoff": null, "estimated_delivery": null },
    "same_day": { "available": false, "quantity": 0 },
    "sister_stores_available": false,
    "sister_store_count": 0
  }
}
```

A 4-litre Havoline 5W30 synthetic motor oil, BRL 193.99 with 2 in store at store 9403 in São Paulo. Report it as "AutoZone reported 2 at store 9403 at the time of the call". If AutoZone does not apply the store asked for, the call fails with an unbilled `502` rather than answering for another store.

### Search, brand, clearance, vehicles, stores, store, categories and rebates

- `/search` with `{"query": "brake pads"}`: `total` 20,622, 24 items, priced for Ashburn, VA store 5180; `{"query": "PH3614"}`: 16 parts (`match_type` "We ID match"), FRAM PH3614 at $14.99 and Beck/Arnley filters with `oem_part_number` "PH3614"; `{"query": "pastilha de freio", "country": "br"}`: 2,174 results in BRL priced for store 7602, the first a SYL rear pad set (`Traseiro`) at BRL 299.99.
- `/brand` with `{"brand": "duralast"}`: 134,086 products (add `category` to narrow to one part type).
- `/clearance`: 805 items; the 24 shown include items with `was_price` (a Dorman exhaust bolt kit at $5 against $10.99, `discount_percent` 55). Three calls were priced for three different stores.
- `/vehicles` with `{"level": "models", "year": 2018, "make_id": 54}`: 32 Ford models, `F-150` `model_id` 666 (`vehicle_type` "Truck", `popular` true); `level` `engines` with `model_id` 666: 5 engines ("6 Cylinders 2.7L Turbo EcoBoost", `drive_type`, `region`).
- `/stores` without `state`: 53 states with `store_count` (`total_stores` 6,890 in the directory on 2026-11-22); `{"state": "vt"}`: 2 cities; `{"state": "tx", "city": "houston"}`: 50 of 84 stores (a city answer lists up to 50, `total` says how many). Stores carry `store_number`, `slug`, `address`, `timezone`, `hours` and `holiday_hours` (on 2026-11-22 the Barre, VT store showed Thanksgiving 2026-11-26 closed and 2026-11-27 06:00-20:00).
- `/store` with `{"slug": "vt/barre/18-overlook-dr.html"}`: Barre #3470 with `phone`, `toll_free_phone`, `latitude`, `longitude`, hours and holiday hours. A Brazilian or Mexican store link works the same way.
- `/categories`: 23 departments (Batteries & Chargers, Brakes, ... Tools & Garage Equipment) with `children[].path` and `has_products`, and `popular[]` (Brake Pads, Motor Oil, Brake Rotor, Oil Filter, Battery, ...).
- `/rebates`: 3 rebates, e.g. "$3.00 back on BlueDEF Platinum (DEG002) after mail in rebate", `end_date` 2026-12-01 (last purchase day), `postmark_date` 2026-12-31 (last day to mail the form), `form_url` (the PDF form).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def autozone(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/autozone/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Batteries that fit a 2015 Honda Civic, lowest price first, with core charge and warranty (1 credit)
res = autozone("category", {
    "category": "/batteries-starting-and-charging/battery",
    "vehicle": {"year": 2015, "make": "Honda", "model": "Civic"},
    "sort": "price_asc",
})
d = res["data"]
store = d["priced_for"]
print(res["fetched_at"], "priced for store", store["store_number"], store["city"], store["state"], "-", d["count"], "of", d["total"])
for it in d["items"]:
    print(it["part_number"], it["name"], it["price"], "+ core", it["core_charge"], it["warranty"],
          "pickup", it["availability"]["store_pickup"]["quantity"], it["fitment"]["vehicle_fit"])

# 2. Cross-reference another brand's part number (1 credit)
hits = autozone("search", {"query": "PH3614"})["data"]
for it in hits["items"]:
    print(it["brand"], it["part_number"], it["price"], it["oem_brand"], it["oem_part_number"])

# Prices are for the store AutoZone assigned (priced_for), and can differ by store and
# between calls. Store each answer with fetched_at and priced_for and run this on a
# schedule: that stored series is your price history (AutoZone shows only the current price).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `country`, `language` and `currency`.

- **item** (search, category, brand, clearance) - `position`, `id` (the input of product and reviews), `part_number`, `name`, `brand`, `sub_brand`, `part_type`, `url`, `image`, `location` (e.g. Front, Rear), `fitment` {`type` (`UNIVERSAL` or `VEHICLE_SPECIFIC`), `vehicle_fit` (as AutoZone gives it, e.g. `NEEDS_BASE_VEHICLE`)}, `oem_part_number`, `oem_brand` (the cross-referenced number and brand), `attributes`, `sponsored`, `price`, `was_price`, `deal_price`, `discount_percent`, `core_charge`, `currency`, `warranty`, `clearance`, `availability`. No rating.
- **lists** - `priced_for`, `title`, `total` (as AutoZone reports it), `count`, `page_size` (24), `items[]`, `facets[]` {`facet` (the key to send in `filters`), `name`, `values[]` {`value` (the value to send), `label`, `count`, `selected`}}, `notes`. Search adds `query`, `sort`, `filters`, `min_price`, `max_price`, `ranking_variant`, `part_number_search`, `match_type`, `corrected_query`, `oem_part_number`, `oem_brand`, `redirected_to`, `redirect_product_id`, `list_source`. Category adds `category`, `requested_vehicle`, `vehicle` (as AutoZone applied it), `list_type` (`products` or `group`), `page_type`. Brand adds `brand`, `category`, `path`; clearance `path`.
- **product** - `requested_id`, `priced_for`, `id`, `part_number`, `name`, `brand`, `sub_brand`, `part_type`, `url`, `brand_path`, `description`, `features`, `specifications[]` {`name`, `value`}, `breadcrumbs[]` {`name`, `path`, `page_type`}, `images`, `safety_data_sheets` (PDF links), `fitment`, `location`, `price`, `was_price`, `deal_price`, `discount_percent`, `core_charge`, `warranty`, `clearance`, `deal` {`available`, `price`, `label`, `quantity`}, `availability`, `rating` {`average`, `count`, `with_text`, `ratings_only`, `recommended_percent`, `distribution[]` {`stars`, `count`, `percent`}}.
- **reviews** - `id`, `sort`, `stars`, `page`, `page_size`, `total_reviews`, `total_matching`, `total_pages`, `has_more`, `average_rating`, `rating_distribution[]`, `summary` {`text`, `features[]` {`name`, `mentions`, `positive`, `negative`}} or `null`, `count`, `reviews[]` {`review_id`, `rating`, `title`, `text`, `recommends`, `verified_purchase`, `incentivized`, `syndicated`, `syndicated_from`, `submitted_at`, `vehicle`, `helpful_votes`, `not_helpful_votes`, `images[]` {`url`, `thumbnail_url`, `caption`}}.
- **vehicles** - `level`, `year`, `make_id`, `model_id`, `count` and `years`, `makes[]` {`make_id`, `name`, `popular`}, `models[]` {`model_id`, `name`, `vehicle_type`, `popular`}, `submodels[]` {`submodel_id`, `name`, `drive_type`} or `engines[]` {`engine_id`, `name`, `drive_type`, `region`}.
- **stores** - `level` (`states`, `cities`, `stores`), `state`, `city`, `count`; `states[]` {`state`, `name`, `store_count`, `new_store`} with `total_stores`; `cities[]` {`city`, `city_slug`, `store_count`, `new_store`}; `stores[]` {`store_number`, `name`, `slug`, `url`, `address` {`line1`, `line2`, `city`, `state`, `postal_code`, `country_code`}, `timezone`, `closed`, `hours[]` {`day`, `open`, `close`, `closed`}, `holiday_hours[]` {`date`, `closed`, `open`, `close`}} with `total`.
- **store** - `store_number`, `name`, `label` (e.g. Barre #3470), `slug`, `url`, `address`, `phone`, `toll_free_phone`, `latitude`, `longitude`, `timezone`, `closed`, `hours[]`, `holiday_hours[]`.
- **categories** - `count`, `node_count`, `categories[]` {`name`, `path`, `page_type`, `child_count`, `children[]` {`name`, `path` (the input of category), `page_type`, `has_products`}}, `popular[]` {`name`, `path`}.
- **rebates** - `count`, `rebates[]` {`title`, `end_date`, `postmark_date`, `form_url`}, `notes`.
- **store-stock** - `requested_id`, `store_number`, `priced_for` (the store asked), `id`, `part_number`, `name`, `brand`, `url`, `price`, `was_price`, `deal_price`, `core_charge`, `in_store` {`available`, `quantity`}, `availability`.

## Guardrails

- Name it "AutoZone (autozone.com, the US auto parts retailer)" on first mention. This is the retail site, not AutoZonePro or commercial pricing.
- Prices: quote `price`, `core_charge`, `warranty` and the deal with the `priced_for` store and the `fetched_at` date. Never call a price national or "AutoZone's price" without the store; never carry one store's price to another; compare two answers only when their `priced_for` stores are named.
- Core charge: a refundable deposit on top of the price until the old part is returned, as AutoZone describes it. Never invent an amount.
- Fitment: quote it at year / make / model level. Say `NEEDS_BASE_VEHICLE` means the part is tied to an engine AutoZone's year / make / model filter does not apply; never promise that a part fits a specific engine or VIN.
- Lists: the first 24 with `total`; never call one answer "all parts" or present `total` as what was returned. Narrow with a vehicle, one facet, a price range or a price sort.
- Stock: `store_pickup` and Brazil `in_store` are what AutoZone reported for that store at the moment of the call; Scavio makes no promise of their accuracy. US and Mexico stock at a chosen store is not offered.
- Reviews: `summary` is AutoZone's own; `vehicle` is the reviewer's text. No reviewer names or identities are returned; never try to identify a reviewer.
- Brazil data: translate Portuguese names, part types and labels for the user and keep the original values in quotes and outputs.
- Not available: paging past 24, stores near a ZIP, store stock at a chosen store in the US or Mexico, search suggestions, VIN lookup, engine-level fitment, repair guides, AutoZonePro or commercial pricing, Mexico prices, price history (poll and store), checkout, cart, ordering or reservations. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not collect or store AutoZone data: each call fetches the public AutoZone page at the moment the request asks for it and returns what it shows as JSON, with no response cache. AutoZone's terms cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish AutoZone product photos, logos or reviewer details; link products by `url` instead.
- Never fabricate prices, core charges, warranties, fitment, stock, stores, hours, rebates, reviews or ratings. Only return what the API returned, with the `fetched_at` time, the `priced_for` store and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` outside us, br, mx, or a market the endpoint does not serve (mx on search or product; br on category, brand, reviews, clearance or rebates; us or mx on store-stock); `page` above 1 on a list; more than one facet (or `brand` together with `filters`); `min_price` above `max_price`; an unknown `sort`; both or neither of `id` / `url` (`slug` / `url` on store); a link whose market disagrees with `country`; `city` without `state`; `makes` without `year`, `models` without `make_id`, `submodels` / `engines` without `model_id` or outside us.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "AutoZone has no product <id> on autozone.com (or the id does not exist).", "AutoZone did not apply the vehicle 2018 Ford Notamodel to this category (unknown make or model name for that year): use the names vehicles lists.", "AutoZone has no product list for <path>.", "AutoZone lists no stores in state <state>.", "AutoZone has no store page <slug>.". Take ids, paths, names and slugs from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api).
- `502` means AutoZone data was temporarily unavailable ("AutoZone is temporarily unavailable. Please try again."), or AutoZone Brazil did not apply the store asked for. It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means AutoZone is busy ("AutoZone is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.76.0
npm install scavio@0.77.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: fits } = await scavio.autozone.category({
  category: "/batteries-starting-and-charging/battery",
  vehicle: { year: 2015, make: "Honda", model: "Civic" },
});
const { data: found } = await scavio.autozone.search({ query: "PH3614" });
const { data: product } = await scavio.autozone.product({ id: "4474" });
const { data: duralast } = await scavio.autozone.brand({ brand: "duralast" });
const { data: models } = await scavio.autozone.vehicles({ level: "models", year: 2018, make_id: 54 });
const { data: reviews } = await scavio.autozone.reviews({ id: "1399158", sort: "most_helpful" });
const { data: states } = await scavio.autozone.stores();
const { data: store } = await scavio.autozone.store({ slug: "vt/barre/18-overlook-dr.html" });
const { data: menu } = await scavio.autozone.categories();
const { data: clearance } = await scavio.autozone.clearance();
const { data: rebates } = await scavio.autozone.rebates();
const { data: stock } = await scavio.autozone.storeStock({ id: "100112748", store_number: "9403" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.autozone.search(...)`, `product`, `category`, `brand`, `vehicles`, `reviews`, `stores`, `store`, `categories`, `clearance`, `rebates` and `store_stock`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 12 endpoints as tools: `search_autozone`, `get_autozone_product`, `get_autozone_category`, `get_autozone_brand`, `get_autozone_vehicles`, `get_autozone_reviews`, `get_autozone_stores`, `get_autozone_store`, `get_autozone_categories`, `get_autozone_clearance`, `get_autozone_rebates` and `get_autozone_store_stock`. AutoZone is opt-in: add `autozone` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.76.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,autozone"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/autozone-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api), [product](https://scavio.dev/docs/autozone-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api), [category](https://scavio.dev/docs/autozone-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api), [brand](https://scavio.dev/docs/autozone-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api), [vehicles](https://scavio.dev/docs/autozone-vehicles?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api), [reviews](https://scavio.dev/docs/autozone-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api), [stores](https://scavio.dev/docs/autozone-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api), [store](https://scavio.dev/docs/autozone-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api), [categories](https://scavio.dev/docs/autozone-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api), [clearance](https://scavio.dev/docs/autozone-clearance?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api), [rebates](https://scavio.dev/docs/autozone-rebates?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api), [store stock](https://scavio.dev/docs/autozone-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api). Overview: [AutoZone API](https://scavio.dev/autozone-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api).
