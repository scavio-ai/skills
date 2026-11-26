# TrueCar API - Car Prices, Market Average vs MSRP, Dealer Inventory

Read TrueCar (truecar.com, the US car-buying marketplace): new and used dealer inventory around a US ZIP, one listing by a VIN you supply, TrueCar's model overview with its per-trim Starting MSRP and Starting Market Average, owner reviews, a dealer's profile and its inventory, TrueCar's search suggestions, and the makes and models it lists. Every answer is what TrueCar's public pages show a visitor without an account at the moment of the call, in USD. All 9 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages TrueCar shows to any visitor and returns them as JSON for analysis. It uses no TrueCar account, sends no lead or price request to a dealer, and returns no VINs, stock numbers, listing links, dealer photos, dealer employees or reviewer names.

**The job this skill is for: what dealers near a ZIP advertise a model at, next to TrueCar's own per-trim figures for it.** `/model` returns TrueCar's Starting MSRP and "Starting Market Average" per trim and its national average listed price per trim (`national_new.trims`), and `/search` returns each dealer's advertised price and MSRP for the same model around a ZIP. Captured 2026-11-26 (1 credit per call):

| Trim | Starting MSRP (`/model`) | Starting Market Average (`/model`) | National average listed price, new (`national_new.trims`) | Advertised near ZIP 75201 (`/search`, new, radius 50, 4WD) |
|---|---|---|---|---|
| 2026 Ford F-150 XLT | 48,490 | 46,102.13 | 60,668 (8,315 listed) | 52,880, MSRP 59,770 (XLT SuperCrew 5.5' Box 4WD, AutoNation Ford Fort Worth, 36.8 mi) |
| 2026 Ford F-150 STX | 45,650 | 42,829.97 | 48,418 (5,104 listed) | 46,025, MSRP 50,865 (STX SuperCrew 5.5' Box 4WD, AutoNation Ford Burleson, 34 mi) |
| 2026 Toyota RAV4 LE | 33,495 | 32,766.12 | 36,553 (1,870 listed) | not searched |

The Starting MSRP and Starting Market Average are for a trim's starting configuration; a listing's `msrp` is that vehicle's own MSRP with its options, and the national average covers every listed vehicle of the trim. Put them side by side with their labels and leave the difference uninterpreted: it is not a dealer's margin and not a price the user can get. For another view of the same model-year use `edmunds-api` (Edmunds Suggested Price next to MSRP and invoice), `kelley-blue-book-api`, `cargurus-api` or `cars-com-api`, matched on year, make, model and trim.

Nine limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`) are not.
- **A ZIP is required for search.** TrueCar searches dealers around `zip`; `radius` defaults to TrueCar's own (75 miles used, 150 new). TrueCar also lists vehicles from dealers far outside the radius, often offered with delivery (a used Civic search near 90012 listed a dealer in Palmetto Bay, FL at 2,330.7 miles with `nationwide_delivery` true): check `distance_miles` on every vehicle.
- **The VIN is input only.** No endpoint returns a VIN, stock number, listing link or dealer photo (TrueCar's listing links and photos carry the VIN). `/listing` takes a VIN you already have or a truecar.com listing link you already have; search results do not carry one, so a search cannot feed `/listing`.
- **Prices are the dealer's advertised prices as TrueCar lists them.** `price` is before taxes, title, registration and the dealer's fees; `/listing` adds `price_summary`, TrueCar's own breakdown (advertised price, the dealer's listed fees, dealer asking price). `price` is `null` when TrueCar shows no advertised price (a 2027 F-150 LARIAT near Dallas showed only an MSRP of 74,260).
- **Price rating and price label are TrueCar's.** `price_rating` (`EXCELLENT`, `GREAT`, `FAIR` ...) and `price_label` (`UPFRONT_PRICE`, `DEALER_DISCOUNT`, "Dealer Discount Available") are TrueCar's own labels as given; TrueCar shows no basis for the rating. New vehicles in the captures carried no `price_rating`.
- **Market Average is per trim, current model years only.** `starting_market_average` is TrueCar's "Starting Market Average" as labelled; the 2022 Honda Civic overview showed none for any trim.
- **Reviews are grouped by generation.** Owner reviews cover every model year of the generation the `year` belongs to (the current one without `year`); `vehicle` says which version the owner reviewed. TrueCar's own order only: no sort.
- **Slow pages.** Search answered in 3 to 9 seconds in the captures (up to 27 in the probe), models up to 39 seconds, makes up to 14. Set a client timeout of at least 240 seconds and send one request at a time.
- **What is not there.** No VIN, no price history (TrueCar shows none), no "what others paid" (TrueCar shows it only after a sign-up), no dealer reviews (TrueCar has none), no dealer search near a ZIP (dealers come from listings), no payment estimates or delivery quotes, no keyword search, no private sellers (TrueCar lists dealer vehicles only). Paging stays within TrueCar's count, which caps at 10,000 (334 pages of 30).

TrueCar publishes no public data API or affiliate data feed for its listings or prices; dealerportal.truecar.com is TrueCar's portal for dealers. This skill reads TrueCar's public pages with one Scavio key.

See also: `edmunds-api` (Edmunds' MSRP, invoice and Suggested Price per trim, and its used-car values), `kelley-blue-book-api` (KBB values), `cargurus-api`, `cars-com-api` and `autotrader-api` (dealer and private listings across the US), and `carmax-api` / `carvana-api` (retailers' own no-haggle prices). Same model-year only: match year, make, model and trim, keep the mileage beside each price, and name the site and date with every number.

## When to trigger

Use this skill when the user asks to:
- Put dealers' advertised prices for a model near a ZIP next to TrueCar's Starting MSRP, Starting Market Average and national average listed price per trim
- Search TrueCar's new or used dealer inventory around a ZIP by make, model, trim or body style, sorted by price, mileage, year, distance, newest listed or best deal, filtered by year, price, maximum mileage, drivetrain, colour, fuel type, accident-free or certified pre-owned
- Read one TrueCar listing in full by a VIN the user supplies: price breakdown with the dealer's listed fees, AutoCheck flags as TrueCar shows them, warranties, specs, features, the dealer's hours
- Read TrueCar's overview of a model or model year: trims, owner rating, pros and cons, specs, model years
- Read TrueCar owner reviews of a model by generation, filtered by stars or by words in the text
- Read a dealer's profile on TrueCar (hours, phone, links, services) or list its new or used vehicles
- Look up TrueCar's suggestions, makes or models and the slugs TrueCar uses

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example 25 models: one model overview and one search each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, search answered in 3-9 seconds (up to 27 in the probe), listing 6-12, model 2-11, reviews 1-5, dealer 3-9, dealer inventory 7-15, suggestions 1-3, makes 6-14 and models 7-39. Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/truecar/search` | New or used dealer vehicles around a ZIP: advertised price, MSRP, price label and rating, mileage, specs, history counts, days on market, distance, dealer; total, paging, TrueCar's echo of the filters it applied, national figures for a make and model | 1 |
| `POST /api/v1/truecar/listing` | One listing by a VIN you supply or a truecar.com listing link: price breakdown with the dealer's listed fees, AutoCheck flags, highlights, specs, features, warranties, certified program, seller notes, dealer with hours | 1 |
| `POST /api/v1/truecar/model` | TrueCar's overview of a model or model year: generation, owner rating, trims with Starting MSRP and Starting Market Average, specs, model years, national new and used figures | 1 |
| `POST /api/v1/truecar/reviews` | Owner reviews of a model's generation: up to 100 a page, star filter, text search, sub-ratings, pros, cons (no names) | 1 |
| `POST /api/v1/truecar/dealer` | One dealer's profile: address, phone, hours, description, links, services | 1 |
| `POST /api/v1/truecar/dealer-inventory` | One dealer's new or used vehicles, 30 a page | 1 |
| `POST /api/v1/truecar/suggestions` | TrueCar's own search suggestions (makes, models, trims, body styles) with slugs | 1 |
| `POST /api/v1/truecar/makes` | Every make with used inventory, with slugs, and TrueCar's national new and used counts | 1 |
| `POST /api/v1/truecar/models` | One make's models with slugs, latest year, body styles, engine types | 1 |

## Market

US only, USD, English. There is no `country` or `currency` input. TrueCar lists dealer vehicles only; `/makes` read 1,099,640 new and 743,848 used vehicles as TrueCar's own national counts on 2026-11-26.

## Prices, ratings and history

| Field | Meaning |
|---|---|
| `price` | The dealer's advertised price in USD as TrueCar lists it, before taxes, title, registration and dealer fees; `null` when TrueCar shows none |
| `msrp`, `base_msrp` (lists) | The vehicle's MSRP with its options and its base MSRP, as TrueCar shows them (new vehicles) |
| `price_label` | TrueCar's own label as given (`UPFRONT_PRICE`, `DEALER_DISCOUNT`; on a listing "Dealer Discount Available") |
| `price_rating` | TrueCar's own price rating as given (`EXCELLENT`, `GREAT`, `FAIR` ...); TrueCar shows no basis for it |
| `no_extra_dealer_fees` | TrueCar's flag as given |
| `price_summary` (listing) | {`advertised_price`, `msrp`, `discount`, `dealer_fees[]` {`label`, `text`, `amount`}, `dealer_asking_price`, `taxes_and_fees`, `advertised_price_disclaimer`}, TrueCar's breakdown as given |
| `history` (lists) | {`accident_count`, `owner_count`, `clean_title`} |
| `history` (listing) | {`source` (AutoCheck), `accident_count`, `owner_count`, `fleet`, `rental`, `lemon`, `salvage`, `theft_recovered`, `report_date`}: the AutoCheck flags TrueCar shows; the report itself is not returned |
| `days_on_market`, `listed_at` | Days since the listing date TrueCar shows, and that date |
| `distance_miles`, `nationwide_delivery` | Miles from the ZIP to the dealer (empty on dealer inventory) and TrueCar's delivery flag |
| `trims[].starting_msrp`, `trims[].starting_market_average` (model) | TrueCar's Starting MSRP and "Starting Market Average" per trim as labelled (market average current model years only) |
| `national`, `national_new`, `national_used` | TrueCar's national figures for the make and model: {`condition`, `price` {`min`, `max`}, `years`, `mileage`, `trims[]` {`trim`, `count`, `average_price`}, `by_year[]` {`year`, `count`, `lowest_price`, `accident_free_count`, `cpo_count`, `under_100k_miles_count`}, `fuel_types[]`, `currency`} |

- **Fees:** the dealer asking price plus the listed fees gives the advertised price; label any sum you make computed (the 2017 RAV4 Hybrid XLE: 13,495 asking + 1,995 pre-delivery inspection + 995 documentation = 16,485 advertised, computed).
- **Seller notes:** `seller_notes` is the dealer's own text with VIN-like codes, stock numbers, emails and phone numbers replaced by "[removed]".

## Workflow

1. **Names.** `/suggestions` (`{"query": "rav4"}`), `/makes` or `/models` (`{"make": "Toyota"}`) for the names and slugs TrueCar uses (F-150 is `f-150`, Land Rover is `land-rover`).
2. **TrueCar's per-trim figures.** `/model` with `make`, `model` (and `year`). Note each trim's `starting_msrp` and `starting_market_average`, and `national_new.trims` / `national_used.trims`.
3. **Advertised prices near a ZIP.** `/search` with `zip`, `condition`, `make`, `model` (and `trim`, `radius`, `year_min` / `year_max`, `sort: "lowest_price"`). Note each vehicle's `trim`, `style`, `mileage`, `price`, `msrp`, `distance_miles` and dealer, and read `filters_applied` to see what TrueCar applied.
4. **One vehicle.** `/listing` with a VIN the user supplies (or a truecar.com listing link they have) for the price breakdown, AutoCheck flags and the dealer's hours.
5. **A dealer.** `/dealer` with `dealer_id` (from `items[].dealer.id`) for its profile, `/dealer-inventory` for its new or used vehicles.
6. **Owners.** `/reviews` with `make`, `model` (and `year`, `stars`, `search`).
7. **Report.** Each price with TrueCar, the dealer, the ZIP and distance, year, trim, style and mileage, and the `fetched_at` date; TrueCar's figures with their labels; no verdict.
8. **Price series:** TrueCar shows no price history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | A 5-digit US ZIP code; TrueCar searches dealers around it |
| `condition` | string | `used` | `used` or `new` |
| `make` | string | none | A make name or slug as TrueCar writes it (`Toyota`, `Mercedes-Benz`, `land-rover`); leave make and model out to search every vehicle |
| `model` | string | none | Needs `make`: a model name or slug (`RAV4`, `F-150`, `CR-V`) |
| `trim` | string | none | Needs `make` and `model`: one trim name or slug (`xlt`, `XLE`) |
| `body_style` | string | none | `convertible`, `coupe`, `hatchback`, `sedan`, `suv`, `truck`, `van`, `wagon` |
| `radius` | integer | TrueCar's (75 used, 150 new) | Miles around the ZIP, 1-500 |
| `year_min`, `year_max` | integer | none | Model year range (1981 to two years ahead) |
| `price_min`, `price_max` | integer | none | Price range, USD |
| `mileage_max` | integer | none | Mileage up to; TrueCar takes a maximum only (`mileage_min` is a 400) |
| `drivetrains` | list or comma-separated | none | Up to 10 of `4wd`, `awd`, `fwd`, `rwd` |
| `colors` | list or comma-separated | none | Up to 10 of `beige`, `black`, `blue`, `brown`, `gold`, `gray`, `green`, `orange`, `purple`, `red`, `silver`, `white`, `yellow` |
| `fuel_types` | list or comma-separated | none | Up to 10 of `gas`, `hybrid`, `electric`, `diesel`, `plug_in_hybrid` |
| `accident_free` | boolean | false | Only vehicles with no reported accident |
| `certified_pre_owned` | boolean | false | Only certified pre-owned vehicles |
| `sort` | string | `best_match` | `best_match`, `best_deal`, `lowest_price`, `highest_price`, `nearest`, `lowest_mileage`, `highest_mileage`, `oldest_year`, `newest_year`, `newest_listed` |
| `page` | integer | 1 | 30 vehicles a page, up to page 334 |

`query`, `keyword`, `mileage_min` and `seller_type` are refused with a `400` that says why.

### Model (`/model`), reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `make` | string | required | A make name or slug (`Toyota`, `Ford`) |
| `model` | string | required | A model name or slug (`RAV4`, `F-150`) |
| `year` | integer | current | Model: one model year (`model_years` lists them). Reviews: that year's generation |
| `stars` | list, integer or comma-separated | none | Reviews only: overall ratings to keep, 1-5 (`[5]`) |
| `search` | string | none | Reviews only: words to match in the review text (up to 80 characters) |
| `page` | integer | 1 | Reviews only: page, up to 500 |
| `page_size` | integer | 20 | Reviews only: 1-100 reviews a page |

`sort` on reviews is refused with a `400`: TrueCar's owner reviews come in its own order only.

### Listing, dealer, dealer inventory, suggestions, makes, models

| Endpoint | Parameters |
|---|---|
| `/listing` | one of `vin` (a 17-character VIN you supply; input only, never returned) or `url` (a truecar.com listing link you already have) |
| `/dealer` | one of `dealer_id` (`414984`, from `items[].dealer.id`) or `url` (a truecar.com dealership link) |
| `/dealer-inventory` | `dealer_id` or `url`; `condition` `used` (default) or `new`; `page` (30 a page) |
| `/suggestions` | `query` (2-80 characters: a make, model, trim or body style; `f-150 2024` works) |
| `/makes` | none (`{}`) |
| `/models` | `make` (a name or slug from `/makes`) |

## Examples

### TrueCar's per-trim figures for a model

```bash
curl -X POST https://api.scavio.dev/api/v1/truecar/model \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "Ford", "model": "F-150"}'
```

Captured `data` (2026-11-26; `trims` cut to 4 of 8, `national_new.trims` to 3 of its list; `overview`, `pros`, `cons`, `whats_new`, `sub_ratings`, specs, `model_years`, `national_used`, `image` and `notes` dropped):

```json
{
  "make": "Ford",
  "make_slug": "ford",
  "model": "F-150",
  "model_slug": "f-150",
  "year": 2026,
  "generation": {"number": 14, "years": {"min": 2021, "max": 2027}},
  "rating": {"value": 4.25, "count": 3737, "stars": {"1": 25, "2": 68, "3": 578, "4": 1315, "5": 1751}},
  "trims": [
    {"trim": "XL", "slug": "xl", "starting_msrp": 40085, "starting_market_average": 38481.75},
    {"trim": "STX", "slug": "stx", "starting_msrp": 45650, "starting_market_average": 42829.97},
    {"trim": "XLT", "slug": "xlt", "starting_msrp": 48490, "starting_market_average": 46102.13},
    {"trim": "LARIAT", "slug": "lariat", "starting_msrp": 62355, "starting_market_average": 57325.79}
  ],
  "horsepower": {"min": 325, "max": 720},
  "combined_mpg": {"min": 12, "max": 24},
  "warranty": {"basic_years": 3, "basic_miles": 36000},
  "has_new_inventory": true,
  "has_used_inventory": true,
  "national_new": {
    "condition": "new",
    "trims": [
      {"trim": "XLT", "count": 8315, "average_price": 60668},
      {"trim": "STX", "count": 5104, "average_price": 48418},
      {"trim": "LARIAT", "count": 3737, "average_price": 71931}
    ],
    "currency": "USD"
  },
  "currency": "USD"
}
```

`national_used.trims` read XLT 32,023 (7,345 listed), XL 26,145 and Lariat 33,300. The 2026 Toyota RAV4 overview read LE 33,495 / 32,766.12 and XLE Premium 37,695 / 37,064.63, rating 4.38 from 5,069; the 2022 Honda Civic overview listed seven trims with Starting MSRP only (`starting_market_average` `null`).

### Search near a ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/truecar/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "75201", "condition": "new", "make": "Ford", "model": "F-150", "sort": "newest_listed", "radius": 50, "drivetrains": ["4wd"]}'
```

Captured `data` (2026-11-26; `items` cut to 2 of 30 with `key_features`, colours, engine and mpg dropped; `national` and `notes` dropped):

```json
{
  "condition": "new",
  "zip": "75201",
  "make": "ford",
  "model": "f-150",
  "sort": "newest_listed",
  "sort_applied": "created_at_desc",
  "page": 1,
  "page_size": 30,
  "total": 984,
  "total_capped": false,
  "total_pages": 33,
  "has_more": true,
  "count": 30,
  "is_fallback": false,
  "filters_applied": {"condition": "new", "zip": "75201", "radius": 50, "make": "ford", "model": "f-150", "drivetrains": ["4wd"]},
  "items": [
    {"year": 2026, "make": "Ford", "model": "F-150", "trim": "XLT", "style": "XLT SuperCrew 5.5' Box 4WD", "condition": "new", "certified_pre_owned": false, "price": 52880, "msrp": 59770, "base_msrp": 51915, "price_label": "UPFRONT_PRICE", "price_rating": null, "no_extra_dealer_fees": false, "mileage": 4, "drivetrain": "4WD", "fuel_type": "Gas", "body_style": "TRUCK", "days_on_market": 0, "distance_miles": 36.8, "nationwide_delivery": false, "dealer": {"id": "12378", "name": "AutoNation Ford Fort Worth", "group": null, "address": "5000 Bryant Irvin Road", "city": "Ft. Worth", "state": "TX", "zip": "76132"}, "currency": "USD"},
    {"year": 2026, "make": "Ford", "model": "F-150", "trim": "STX", "style": "STX SuperCrew 5.5' Box 4WD", "condition": "new", "price": 46025, "msrp": 50865, "base_msrp": 51070, "price_label": "UPFRONT_PRICE", "price_rating": null, "mileage": 6, "days_on_market": 0, "distance_miles": 34, "nationwide_delivery": false, "dealer": {"id": "7832", "name": "AutoNation Ford Burleson", "group": null, "address": "850 N Burleson Blvd", "city": "Burleson", "state": "TX", "zip": "76028"}, "currency": "USD"}
  ]
}
```

A used search (`{"zip": "10001", "make": "Toyota", "model": "RAV4"}`) read `total` 2,440 in 82 pages; its first vehicle was a 2017 RAV4 Hybrid XLE at 16,485 with 125,334 miles, `price_rating` `EXCELLENT`, 3 owners, 0 accidents, 11 days on market, at Metro Honda, Jersey City, NJ, 5.8 miles. `national` on that search read used RAV4 prices 3,190 to 53,442 and per-trim averages XLE 26,814 (3,610 listed), LE 25,292, XLE Premium 33,422.

### One listing

`/listing` takes `{"vin": ...}` with a 17-character VIN the user supplies, or `{"url": ...}` with a truecar.com listing link they already have; search results carry neither, so no request body is shown here. Captured `data` for a used 2017 Toyota RAV4 Hybrid XLE (2026-11-26; `specs`, `features`, `highlights`, `warranties`, the dealer's `hours`, `stock_image` and `notes` dropped, `seller_notes` shortened):

```json
{
  "year": 2017,
  "make": "Toyota",
  "model": "RAV4",
  "trim": "Hybrid XLE",
  "style": "Hybrid XLE AWD",
  "condition": "used",
  "price": 16485,
  "msrp": null,
  "price_label": "Dealer Discount Available",
  "price_rating": "EXCELLENT",
  "price_summary": {
    "advertised_price": {"label": "Advertised price", "text": "$16,485", "amount": 16485},
    "msrp": null,
    "discount": null,
    "dealer_fees": [
      {"label": "Pre Delivery Inspection Fee", "text": "$1,995.00", "amount": 1995},
      {"label": "Documentation Fees", "text": "$995.00", "amount": 995}
    ],
    "dealer_asking_price": {"label": "Dealer asking price", "text": "$13,495.00", "amount": 13495},
    "taxes_and_fees": null,
    "advertised_price_disclaimer": "The advertised price of this vehicle is provided by the dealer or other third parties. TRUECar is not responsible for the accuracy of such information."
  },
  "mileage": 125334,
  "engine": "2.5L Inline-4 Hybrid",
  "mpg": {"city": 34, "highway": 30, "combined": 32},
  "history": {"source": "AutoCheck", "accident_count": 0, "owner_count": 3, "fleet": false, "rental": false, "lemon": false, "salvage": false, "theft_recovered": false, "report_date": "2026-11-15"},
  "seller_notes": "This 2017 Toyota RAV4 Hybrid XLE delivers impressive fuel efficiency and dependable hybrid performance ...",
  "listed_at": "2026-11-15T07:45:00+00:00",
  "days_on_market": 11,
  "photo_count": 32,
  "dealer": {"id": "5892", "name": "Metro Honda", "address": "540 Route 440 North, North", "city": "Jersey City", "state": "NJ", "zip": "07305", "type": "franchise", "phone": "(201) 451-7111", "timezone": "America/New_York"},
  "currency": "USD"
}
```

A new 2027 F-150 Raptor read `price` 81,415 against `msrp` 81,190 with one $225 doc fee and `price_rating` `GREAT`; its AutoCheck fields were all `null`.

### Owner reviews, five stars only

```bash
curl -X POST https://api.scavio.dev/api/v1/truecar/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "Toyota", "model": "RAV4", "year": 2022, "stars": [5], "page": 2}'
```

Captured (2026-11-26): `name` RAV4, `model_year` 2022, `rating` 4.38 from 5,069 (2,831 five-star), `total` 246 five-star reviews in 13 pages of 20. One review: `rating` 5, `sub_ratings` Performance 5, Comfort 5, Fuel Efficiency 5, Safety Technology 4, Features 4, `pros` "Gas mileage and smooth ride", `date` 2022-08-07, `purchase_date` 2022-07-08, `vehicle` "Hybrid XLE Premium AWD". No reviewer name, initials or state is returned. `{"make": "Ford", "model": "F-150", "search": "towing", "page_size": 10}` found 7 reviews mentioning towing.

### Dealer, dealer inventory, suggestions, makes, models

- `/dealer` `{"dealer_id": "414984"}`: Castle Volkswagen Downers Grove, 2020 Ogden Avenue, Downers Grove, IL 60515, 630-964-9500, Monday-Friday 9:00am-8:00pm, Saturday 9:00am-6:00pm, Sunday closed; `links` website, facebook, new inventory, credit application, service appointment; `services` all false. No employees are returned and TrueCar shows no dealer reviews.
- `/dealer-inventory` `{"dealer_id": "414984", "condition": "used"}`: `total` 73 used vehicles in 3 pages, first a 2024 Volkswagen ID.4 Standard at 18,133 with 35,315 miles, `price_rating` `EXCELLENT`. `{"dealer_id": "31117", "condition": "new", "page": 2}`: Upstate Chevrolet, Attica, NY, 89 new vehicles.
- `/suggestions` `{"query": "rav4"}`: RAV4 (`rav4`), RAV4 Plug-In Hybrid (`rav4-plug-in-hybrid`), RAV4 Prime (`rav4-prime`), the Toyota make and the SUV body style, each with the `pages` TrueCar has for it. `{"query": "f-150 2024"}` returned F-150, F-150 Lightning and Silverado 1500 with `year` 2024.
- `/makes` `{}`: 63 makes with slugs (Acura `acura`, Alfa Romeo `alfa-romeo` ...).
- `/models` `{"make": "Toyota"}`: 47 models (4Runner, 86, Avalon ...) with latest `year`, body styles and engine types; `{"make": "Land Rover"}` 14.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def truecar(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/truecar/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# TrueCar's per-trim figures for a model (1 credit)
m = truecar("model", {"make": "Ford", "model": "F-150"})["data"]
for t in m["trims"]:
    print(t["trim"], "Starting MSRP", t["starting_msrp"], "Starting Market Average", t["starting_market_average"])

# Dealers' advertised prices for the same model near a ZIP (1 credit)
s = truecar("search", {"zip": "75201", "condition": "new", "make": "Ford", "model": "F-150",
                       "trim": "xlt", "sort": "lowest_price"})["data"]
for v in s["items"]:
    print(v["year"], v["style"], v["price"], v["msrp"], v["dealer"]["name"], v["distance_miles"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }` (`response_time` in milliseconds). Everything is fetched when the request asks for it; nothing is cached. Every answer carries `market` {`country`, `currency`, `language`} and most carry `notes`.

- **vehicle** (search, dealer inventory) - `year`, `make`, `model`, `trim`, `style`, `condition`, `certified_pre_owned`, `price`, `msrp`, `base_msrp`, `price_label`, `price_rating`, `no_extra_dealer_fees`, `mileage`, `exterior_color`, `exterior_color_generic`, `interior_color`, `drivetrain`, `engine`, `fuel_type`, `transmission`, `body_style`, `mpg` {`city`, `highway`, `combined`}, `electric_range`, `key_features`, `history` {`accident_count`, `owner_count`, `clean_title`}, `listed_at`, `days_on_market`, `distance_miles`, `nationwide_delivery`, `dealer` {`id`, `name`, `group`, `address`, `city`, `state`, `zip`}, `currency`.
- **search** - `condition`, `zip`, `make`, `model`, `sort`, `sort_applied`, `page`, `page_size`, `total`, `total_capped`, `total_pages`, `has_more`, `count`, `is_fallback`, `filters_applied`, `items[]`, `national` (with make and model), `market`, `notes`.
- **listing** - `year`, `make`, `model`, `trim`, `style`, `condition`, `certified_pre_owned`, `price`, `msrp`, `price_label`, `price_rating`, `price_summary`, `no_extra_dealer_fees`, `mileage`, `exterior_color`, `interior_color`, `drivetrain`, `engine`, `fuel_type`, `transmission`, `body_style`, `mpg`, `electric_range`, `key_features`, `highlights` {`technology`, `safety`, `comfort`, `appearance`}, `specs[]` and `features[]` {`group`, `items[]` {`name`, `value`, `units`}}, `warranties[]` {`name`, `years`, `miles`}, `cpo_program`, `history`, `seller_notes`, `listed_at`, `days_on_market`, `photo_count`, `stock_image`, `nationwide_delivery`, `dealer` {`id`, `name`, `group`, `address`, `city`, `state`, `zip`, `type`, `phone`, `timezone`, `hours` {`monday`..`sunday`: {`open`, `close`, `closed`}}}, `currency`, `market`, `notes`.
- **model** - `make`, `make_slug`, `model`, `model_slug`, `year`, `generation` {`number`, `years`}, `overview`, `pros`, `cons`, `whats_new`, `rating` {`value`, `count`, `stars`}, `sub_ratings[]` {`name`, `value`}, `trims[]` {`trim`, `slug`, `starting_msrp`, `starting_market_average`}, `body_styles`, `engine_types`, `transmissions`, `horsepower`, `combined_mpg`, `electric_range`, `seating`, `cargo_cubic_feet`, `max_towing_lbs`, `warranty` {`basic_years`, `basic_miles`}, `segment_ranking` {`position`, `list`}, `has_new_inventory`, `has_used_inventory`, `model_years`, `national_new`, `national_used`, `image`, `currency`, `market`, `notes`.
- **reviews** - `make`, `model`, `name`, `model_year`, `year`, `rating`, `stars`, `search`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `reviews[]` {`rating`, `sub_ratings[]`, `pros`, `cons`, `other_text[]` {`section`, `text`}, `date`, `purchase_date`, `vehicle`}, `market`, `notes`.
- **dealer** - `id`, `name`, `group`, `address`, `city`, `state`, `zip`, `phone`, `hours`, `description`, `links[]` {`type`, `url`}, `services` {`express_checkout`, `delivery`, `free_car_wash_new`, `free_car_wash_used`, `free_oil_change_new`, `free_oil_change_used`, `free_scheduled_maintenance_new`, `free_scheduled_maintenance_used`}, `online_dealer`, `hybrid_dealer`, `dealer_group`, `images`, `market`, `notes`.
- **dealer inventory** - `dealer` {`id`, `name`, `group`, `address`, `city`, `state`, `zip`, `phone`}, `condition`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `items[]`, `market`, `notes`.
- **suggestions** - `query`, `did_you_mean`, `hint`, `count`, `suggestions[]` {`type` (make, model, trim, body_style), `make`, `make_slug`, `model`, `model_slug`, `trim`, `trim_slug`, `body_style`, `body_style_slug`, `year`, `pages`}, `market`, `notes`.
- **makes** - `count`, `makes[]` {`make`, `slug`}, `national_new_count`, `national_used_count`. **models** - `make`, `make_slug`, `count`, `models[]` {`model`, `slug`, `year`, `body_styles`, `engine_types`, `new_inventory`, `used_inventory`, `image`}.

## Guardrails

- Name it "TrueCar (truecar.com, the US car-buying marketplace)" on first mention, "TrueCar" after that.
- Prices: quote each with USD, the year, make, model, trim, style and mileage, the dealer, the ZIP and distance, and the `fetched_at` date ("advertised on truecar.com by AutoNation Ford Fort Worth, 36.8 miles from 75201, on Nov 26, 2026"), and say it is before taxes, title, registration and the dealer's fees. Never compute an out-the-door price.
- TrueCar's figures: always give `starting_msrp`, `starting_market_average` and the national `average_price` with TrueCar's labels ("TrueCar's Starting Market Average"), and never present them as a price the user can get, a fair price or what a car is worth.
- `price_rating` and `price_label` are TrueCar's labels as given, with no basis shown; attribute them to TrueCar.
- Comparisons: the same model-year and trim, mileage beside every number, named site and date. No verdict on which car or dealer is cheaper beyond the numbers shown, and no commentary on dealer margins.
- History: `history` is the AutoCheck summary TrueCar shows; attribute it that way.
- VINs: never print, ask for more of, or guess a VIN; use the one the user supplied only as the `/listing` input.
- Reviews: no reviewer is named or identified; quote review text as TrueCar shows it, with its rating and date.
- Descriptive only: no commentary on TrueCar's business, pricing practices or policies.
- Do not republish TrueCar photos or descriptions. Write truecar.com as plain text and cite dealer ids and capture dates rather than linking TrueCar pages.
- Terms: Scavio does not collect or store TrueCar data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no lead or purchase flow. TrueCar's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, ratings, dealers, mileage or review text. Only return what the API returned, with the `fetched_at` time.
- Not available: VINs or stock numbers in answers, price history, what others paid, dealer reviews, dealers near a ZIP, payment estimates, delivery quotes, keyword search, private sellers.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `zip` ("zip is required (a 5-digit US ZIP code, e.g. 10001): TrueCar searches around a ZIP."); a ZIP that is not 5 digits; `model` without `make` ("model needs make (e.g. make Toyota, model RAV4)."); `trim` without `make` and `model`; a `body_style`, `sort` or list value outside its list, or more than 10 values in a list; a `_min` above its `_max`; `query` or `keyword` ("Keyword search is not offered: search by make and model (names or slugs, from the makes / models / suggestions endpoints) with filters."); `mileage_min` ("mileage_min is not offered: TrueCar's mileage filter takes a maximum only (mileage_max)."); `seller_type` ("seller_type is not offered: TrueCar lists dealer vehicles only (no private sellers)."); `sort` on reviews ("sort is not offered: TrueCar's owner reviews come in TrueCar's own order only."); `/listing` without `vin` or `url` ("vin or url is required (url: a truecar.com listing link)."), a VIN that is not 17 letters and digits, or a link that is not a truecar.com listing link; `/dealer` or `/dealer-inventory` without `dealer_id` or `url`, or an id that is not TrueCar's number; suggestions under 2 characters ("query must be at least 2 characters.").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "TrueCar lists no make "...". Makes (slugs): ..." (the answer lists every slug), "TrueCar has no ... model "...". The models endpoint lists a make's models (names and slugs).", "TrueCar has no listing for this VIN (a sold or removed vehicle leaves TrueCar).", "TrueCar has no overview for ... Check the names (makes / models endpoints) and the year (model_years).", "TrueCar has no dealer ...", "TrueCar has no make "...". The makes endpoint lists them.". Take names, slugs and dealer ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api).
- `502` means TrueCar data was temporarily unavailable ("TrueCar is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds. TrueCar requests retry a busy moment before answering, so a busy moment also ends as this `502`; if a `503` with `Retry-After` ever arrives, wait that many seconds and send it again (not charged).
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.97.0
npm install scavio@0.98.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: model } = await scavio.truecar.model({ make: "Ford", model: "F-150" });
const { data: cars } = await scavio.truecar.search({ zip: "75201", condition: "new", make: "Ford", model: "F-150", sort: "lowest_price" });
const { data: reviews } = await scavio.truecar.reviews({ make: "Toyota", model: "RAV4", year: 2022, stars: [5] });
const { data: dealer } = await scavio.truecar.dealer({ dealer_id: "414984" });
const { data: lot } = await scavio.truecar.dealerInventory({ dealer_id: "414984", condition: "used" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.truecar.search(...)`, `listing`, `model`, `reviews`, `dealer`, `dealer_inventory`, `suggestions`, `makes` and `models`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 9 endpoints as tools: `search_truecar`, `get_truecar_listing`, `get_truecar_model`, `get_truecar_reviews`, `get_truecar_dealer`, `get_truecar_dealer_inventory`, `get_truecar_suggestions`, `get_truecar_makes` and `get_truecar_models`. TrueCar is opt-in: add `truecar` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.97.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,truecar"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/truecar-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api), [listing](https://scavio.dev/docs/truecar-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api), [model](https://scavio.dev/docs/truecar-model?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api), [reviews](https://scavio.dev/docs/truecar-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api), [dealer](https://scavio.dev/docs/truecar-dealer?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api), [dealer inventory](https://scavio.dev/docs/truecar-dealer-inventory?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api), [suggestions](https://scavio.dev/docs/truecar-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api), [makes](https://scavio.dev/docs/truecar-makes?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api), [models](https://scavio.dev/docs/truecar-models?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api). Overview: [TrueCar API](https://scavio.dev/truecar-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=truecar-api).
