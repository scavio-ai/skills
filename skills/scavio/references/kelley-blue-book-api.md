# Kelley Blue Book API - KBB Car Values, Trade-In Values, Cars for Sale

Read Kelley Blue Book (kbb.com, Cox Automotive's car value and research site): a car's KBB values for a trim, mileage, condition and ZIP, one model year with its trims, depreciation and specs, the cars for sale around a US ZIP with KBB's deal ratings, one listing in full, owner reviews of a model year, dealers near a ZIP and one dealer, and KBB's make and model directory. Every answer is what KBB's public pages show a visitor without an account at the moment of the call, in USD. All 8 endpoints return structured JSON, most at 1 credit per call.

**Read-only data.** This skill reads the public pages KBB shows to any visitor and returns them as JSON for analysis. It uses no KBB account, no saved cars, no instant offer request, no dealer contact form and no financing step.

**The job this skill is for: Kelley Blue Book's values for one trim, mileage and condition, and how they move with the ZIP.** `/car-value` returns every price type KBB's value page gives for the car, each with its base value and KBB's region, mileage and option adjustments. Captured 2026-11-26:

| Car (intent, mileage, condition) | KBB's default location (1 credit) | A ZIP you choose |
|---|---|---|
| 2021 Toyota RAV4 LE Sport Utility 4D (`buy_used`, 40,000 mi, good) | ZIP 92620: Fair Purchase Price 25,950 (range 23,750-28,150), Private Party Value Good 24,350, Trade-In Value Good 19,880, Typical Listing Price 26,550 | ZIP 10001 (2 credits): 25,410 (23,210-27,610), 23,820, 19,450, 26,000 |
| 2019 Ford F150 SuperCrew Cab XLT Pickup 4D 5 1/2 ft (`buy_used`, 60,000 mi, very good) | ZIP 98101: Fair Purchase Price 30,790, Private Party Value Very Good 29,690, Trade-In Value Very Good 22,960 | ZIP 75201 (6 credits): 31,320, 30,210, 23,350 |
| 2020 Honda Civic EX Sedan 4D (`trade_in_sell`, 50,000 mi, good) | ZIP 07094: Trade-In Value Good 14,460 (13,410-15,460), Private Party Value Good 17,800, Auction Value Good 14,810 | ZIP 90012 (2 credits): 14,890 (13,840-15,890), 18,360, 15,240 |

Each value is KBB's base value plus its adjustments (RAV4 Fair Purchase Price: 22,900 base + 120 region + 2,930 mileage = 25,950 at 92620; the region adjustment is -420 at 10001, so 25,410). Quote each value with its KBB name, the trim, mileage, condition and the ZIP from `location.valid_text`; leave the differences between price types uninterpreted. For listed prices of the same car use `/search` here (each car carries KBB's deal rating and Fair Purchase Price range), or `carmax-api`, `carvana-api`, `cargurus-api` and `autotrader-api`, matched on year, make, model, trim and mileage band.

Eleven limits shape every answer, so say them plainly:
- **1 credit per call, with two exceptions.** A car value for a ZIP you choose costs 2 credits, or 6 when KBB needs a heavier second attempt to answer for that ZIP (the F-150 at 75201 above). A reviews page beyond 1, another sort or a star filter costs 1 credit, or 5 when that heavier attempt is needed. The balance must cover the most a call can bill (6 for a car value with `zip`, 5 for those reviews calls) for it to start. `credits_used` in every answer says what was spent. A not-found (`404`) is charged what it cost; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Values are for a ZIP, and say which.** Without `zip` the values are for KBB's default location, which can change from call to call (92620, 98101 and 07094 in the captures): `location.zip`, `location.valid_text` ("Valid for ZIP Code 92620 through 11/26/2026") and `chosen_zip` say which. With `zip` (it needs `mileage`) the values are for that ZIP. `zip` is not offered for `buy_new`.
- **The trim is required.** Pass `trim` as a `trim_slug` from `/model` (`le-sport-utility-4d`), a `vehicle_id`, or a name that starts exactly one trim (`LE`). A name several trims share is a `400` that lists them; a trim KBB does not list is a charged `404` that lists the model's trims. Model slugs are KBB's own: `f150-supercrew-cab`, not `f-150`.
- **Every price type, and a headline.** `prices` is every KBB price type the value page gives: 17 for a used car (Lending Value, Typical Listing Price, Trade-In, Private Party and Auction values for Fair, Good, Very Good and Excellent, Typical Listing Price (CPO), Fair Purchase Price, Fair Purchase Price (CPO)); MSRP, Invoice and Fair Purchase Price for a new model year. `headline` picks the ones for the `intent` and `condition`. `range_low` / `range_high` are KBB's range where it gives one (`null` for auction values).
- **KBB's values, not an offer.** These are Kelley Blue Book's figures, exactly as KBB gives them (KBB: the actual price of a vehicle may vary). Never present one as what the user's car will fetch, a dealer's offer or an appraisal.
- **Deal ratings are KBB's.** On cars for sale, `deal_label` (Great, Good ...) is KBB's rating, based on the KBB Fair Purchase Price range in `kbb_fair_purchase_price` {`amount`, `low`, `high`, `delta`}; `delta` is that price minus the listing's displayed price (negative = the car is listed above it). `display_price` can include the dealer fees listed in `dealer_fees` (23,250 + 175 doc fee = 23,425).
- **No VIN, no private-seller identity.** VINs and stock numbers are never returned, and there is no VIN input. A private seller is `{type: private, city, state, distance_miles}` only. Phone numbers, emails, stock numbers and VIN-like codes inside descriptions read "[removed]". Dealer name, address, phone, website and rating are the dealer's public business details.
- **Reviews: 8 a page, up to 10 pages.** Owner reviews come 8 a page, pages 1 to 10 for each sort and star filter, with KBB's averages in `ratings`. A review can be for a neighbouring model year or variant KBB groups with this one (the 2021 RAV4 page carried reviews of a 2020 RAV4 and a 2023 RAV4 Hybrid): read `reviews[].year` and `model`. No reviewer name, nickname or location. `incentivized` and `staff` are KBB's flags.
- **Dealers: at most 50, no paging.** KBB's dealer finder shows at most 50 dealers, nearest first, and does not page: narrow with `radius` or `make`. Dealer reviews are not included (`rating` and `rating_count` only).
- **Slow pages.** A car value answered in 13 to 20 seconds, 36 to 48 with a chosen ZIP and 160 when the heavier attempt was needed; reviews beyond page 1 took 59 to 129. Answers can take up to 4 minutes: set a client timeout of at least 240 seconds and send one request at a time.
- **What is not there.** No VIN lookup, no instant offer, no dealer reviews, no free-text search or suggestions (use `/makes-models` for names and slugs), no `buy_new` value at a chosen ZIP, no monthly payments or taxes, no market outside the US (kbb.ca and kbb.com.br no longer carry KBB data). Search pages stop at page 100.

Kelley Blue Book's own data feed (InfoDriver) is a business contract with KBB, not a self-serve API. This skill reads KBB's public pages with one Scavio key.

See also: `carmax-api` (CarMax's listed prices and recent instant offers for a model-year), `carvana-api` (Carvana's listed prices next to the KBB value Carvana shows), `autotrader-api` and `cargurus-api` (dealer and private listings across the US). Same car only: match year, make, model and trim, keep the mileage beside each number, and name the site and date with every price.

## When to trigger

Use this skill when the user asks to:
- Get Kelley Blue Book's values for a car: Fair Purchase Price, private party, trade-in, auction, typical listing price, CPO, lending value, or MSRP and invoice for a new model year, for a trim, mileage, condition and ZIP
- See how KBB's values for a car change with the ZIP, the mileage or the condition
- Read one model year on KBB: its trims with KBB prices, specs and fuel economy, depreciation history and forecast, rankings and new-car pricing
- Search cars for sale on KBB around a ZIP by make and model, sorted by price, mileage or model year, filtered by year, price, mileage, drivetrain, colour or dealer versus private seller, with KBB's deal rating on each
- Read one KBB listing in full: price history, dealer fees, features, warranties, open recall count, the dealer
- Read KBB owner reviews of a model year, with KBB's average ratings and star distribution
- Find car dealers near a ZIP, or read one dealer's hours, home services and cars for sale
- Look up the makes and models KBB lists, with the slugs the other endpoints take

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=kelley-blue-book-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=kelley-blue-book-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 1 credit, so 50 credits cover about 50 calls (for example 25 cars: one model page for the trim slug and one car value at KBB's default location each). A car value at a ZIP you choose costs 2 credits, or 6.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, dealer answered in 3-10 seconds, listing 5-7, makes and models 4-11, model 6-13, car value 13-20 (36-48 with a chosen ZIP, 160 with the heavier attempt), search 6-33, reviews 7-13 for page 1 (59-129 beyond it, other sorts or a star filter) and dealers 20-46. Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/kbb/car-value` | A car's KBB values by make, model, year, trim, intent, condition, mileage and optional ZIP: every price type with base value, region, mileage and option adjustments and range; the headline values; the location and valid date | 1; with `zip` 2 (6 with the heavier attempt) |
| `POST /api/v1/kbb/model` | One model year: trims with KBB prices and specs, new-car pricing, depreciation history and forecast, specs, rankings, KBB's list placement, model years, other models | 1 |
| `POST /api/v1/kbb/search` | Cars for sale around a ZIP: price, dealer fees, deal rating, KBB Fair Purchase Price range, price history, history flags, seller; total, paging, filters applied and not applied, spotlights, price / mileage / year stats | 1 |
| `POST /api/v1/kbb/listing` | One car for sale by listing id or link: the search fields plus description, images, features, specifications, warranties, open recall count, KBB consumer rating, dealer details | 1 |
| `POST /api/v1/kbb/reviews` | Owner reviews of a model year: 8 a page, 3 sorts, star filter, sub-ratings, pros and cons; KBB's average ratings and distribution; most helpful positive and negative | 1; beyond page 1, other sorts or `stars` 1 (5 with the heavier attempt) |
| `POST /api/v1/kbb/dealers` | Dealers near a ZIP, optionally of one make and within a radius: rating, distance, address, phone, website (at most 50) | 1 |
| `POST /api/v1/kbb/dealer` | One dealer: rating, address, phone, website, hours, home services, cars-for-sale count, price stats, makes, the first page of its cars | 1 |
| `POST /api/v1/kbb/makes-models` | KBB's make and model directory, used (68 makes, about 1,500 models) or new, with the slugs and model years | 1 |

## Market

US only, USD (`market` {"country": "us", "currency": "USD"} on every answer). `country` is optional and takes `us`; any other value, or a kbb.ca / kbb.com.br link, is a `400`: "Kelley Blue Book data is served for the US only (www.kbb.com, USD): kbb.ca now points to AutoTrader.ca and kbb.com.br became Molicar, so neither carries KBB data."

## Values, deal ratings and prices

| Field | Meaning |
|---|---|
| `prices[]` (car value) | {`type_id`, `type` (KBB's name: "Private Party Value Good"), `category`, `condition`, `value`, `base_value`, `region_adjustment`, `mileage_adjustment`, `option_adjustment`, `range_low`, `range_high`} per KBB price type |
| `headline` (car value) | `buy_used`: `fair_purchase_price`, `private_party` (for the condition), `typical_listing_price`, `cpo_fair_purchase_price`; `trade_in_sell`: `trade_in`, `private_party`, `auction`; `buy_new`: `fair_purchase_price`, `msrp`, `invoice`, `typical_listing_price` (null where KBB gives none) |
| `location` (car value) | {`zip`, `chosen_zip` (true when you sent `zip`), `valid_text`, `valid_through`} |
| `mileage`, `typical_mileage` | The miles valued, and the mileage KBB assumes for the car (RAV4 2021: 78,057) |
| `trims[]` (model) | Each trim's `fair_purchase_price`, `trade_in_value`, `private_party_value` at KBB's default location and typical mileage, plus specs |
| `depreciation` (model) | {`three_year_depreciation`, `current_resale_value`, `current_trade_in_value`, `history[]`, `forecast[]` {`year`, `resale_value`, `trade_in_value`, `annual_depreciation`}}: KBB's own history and forecast |
| `deal_label` (cars for sale) | KBB's deal rating as given (Great, Good ...), `null` where KBB gives none |
| `kbb_fair_purchase_price` | {`amount`, `low`, `high`, `delta` (that price minus the displayed price; negative = listed above it)} |
| `price`, `display_price`, `msrp`, `price_label` | The listed price (USD; `null` when the dealer asks you to call: `price_label`), the price KBB displays (can include `dealer_fees`), the MSRP on new cars |
| `dealer_fees` | {`total`, `items[]` {`name`, `amount`}} as the listing states them |
| `price_history[]` | {`date`, `price`, `current`} as KBB shows it |
| `history_preview` | History flags as given (`NO_ACCIDENTS_REPORTED`, `ONE_OWNER`, `ACCIDENTS_REPORTED`, `FREE_REPORT` ...) |

- **Percent or dollar change:** compute it from two values and label it computed (Fair Purchase Price 25,950 at 92620 to 25,410 at 10001 is 540 lower, computed).
- **Ids:** `listing_id` opens with `/listing`, `seller.dealer_id` / `dealers[].dealer_id` with `/dealer`. A sold or removed listing is a charged `404`.

## Workflow

1. **Names and slugs.** `/makes-models` (`{"make": "ford"}`) for the model slugs KBB uses (`f150-supercrew-cab`, `f150-super-cab`, `f150-lightning` ...).
2. **The trim.** `/model` with `make`, `model`, `year`; take the `trim_slug` of the trim (trims can include sibling models such as RAV4 Hybrid and RAV4 Prime: read `trims[].model`).
3. **Values.** `/car-value` with `make`, `model`, `year`, `trim`, `intent`, `condition`, `mileage`, and `zip` for a ZIP of your choice. Note `location.valid_text`, `headline` and the `prices` you need.
4. **Cars for sale.** `/search` with `zip`, `make`, `model`, `year_min` = `year_max` = the year, `sort: "price_asc"`; read each car's `trim`, `mileage`, `price`, `deal_label` and `kbb_fair_purchase_price`. `/listing` for one car in full.
5. **Owners.** `/reviews` for the model year, with `sort` and `stars` as needed.
6. **Dealers.** `/dealers` near the ZIP, `/dealer` for one dealer's hours and cars.
7. **Report.** Each value with its KBB name, trim, mileage, condition, ZIP and `fetched_at` date; each listed price with the car's mileage, the seller and KBB's deal rating as KBB's; no verdict.
8. **Value series:** KBB's depreciation history is on `/model`; for your own record of values or listings, store each answer with its `fetched_at`.

## Parameters

### Car value (`/car-value`), model (`/model`), reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `make` | string | required | A make by name or KBB slug (`Toyota`, `Mercedes-Benz`, `land-rover`; 68 makes) |
| `model` | string | required | KBB's model slug as `/makes-models` gives it (`rav4`, `civic`, `f150-supercrew-cab`, `3-series`) |
| `year` | integer | required | Model year (1981-2028) |
| `trim` | string | required (car value) | A `trim_slug` from `/model` (`le-sport-utility-4d`), its `vehicle_id`, or a name that starts exactly one trim (`LE`) |
| `intent` | string | `buy_used` | Car value only: `buy_used`, `buy_new` (a new model year) or `trade_in_sell`; picks the headline values (every price type the page gives comes back) |
| `condition` | string | `good` | Car value only: `fair`, `good`, `very_good`, `excellent` (for the trade-in, private party and auction headline values) |
| `mileage` | integer | KBB's assumed mileage | Car value only: odometer miles, 0-999,999 (not used for `buy_new`) |
| `zip` | string | KBB's default location | Car value only: a 5-digit US ZIP the values are for (`buy_used` and `trade_in_sell`; needs `mileage`). 2 credits, or 6 |
| `page` | integer | 1 | Reviews only: page of 8 reviews, 1-10 |
| `sort` | string | `recent` | Reviews only: `recent` (most recent first), `rating_desc`, `rating_asc` |
| `stars` | integer | none | Reviews only: only reviews with this overall star rating (1-5) |
| `country` | string | `us` | Optional; `us` is the only market |

### Cars for sale (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | A 5-digit US ZIP code: cars for sale around it (an unknown ZIP is a `400`) |
| `listing_type` | string | `all` | `all`, `used` or `new` |
| `make` | string | none | A make by name or code (`Toyota`, `Ford`, `Mercedes-Benz`, or `TOYOTA`, `MB`) |
| `model` | string | none | With `make`: a model as the listings name it (`RAV4`, `Civic`, `F150`; `F-150` is matched to F150). A model KBB does not list for the make is a charged `404` that lists the make's models; the search is never widened to the whole make |
| `model_code` | string | none | With `make`, instead of `model`: a code as `listings[].model_code` gives it (`F150PICKUP`) |
| `radius` | integer | KBB's default | Miles around the ZIP: 10, 25, 50, 75, 100, 200, 300, 400, 500 or 0 (nationwide); `location.radius_miles` says what was used |
| `page` | integer | 1 | Page, 1-100 |
| `page_size` | integer | 25 | 25 or 100 |
| `sort` | string | `relevance` | `relevance`, `price_asc`, `mileage_asc`, `year_desc` (newest model year) |
| `year_min`, `year_max` | integer | none | Model year range (1981-2028) |
| `price_min`, `price_max` | integer | none | Price range, whole USD |
| `mileage_min`, `mileage_max` | integer | none | Mileage range |
| `drivetrain` | string | none | `AWD4WD` (AWD/4WD), `FWD` (Front Wheel Drive), `RWD` (Rear Wheel Drive) |
| `exterior_color` | string | none | `BEIGE`, `BLACK`, `BLUE`, `BROWN`, `BURGUNDY`, `CHARCOAL`, `GOLD`, `GRAY`, `GREEN`, `OFFWHITE`, `ORANGE`, `PINK`, `PURPLE`, `RED`, `SILVER`, `TAN`, `TURQUOISE`, `WHITE`, `YELLOW` (or the colour name) |
| `seller_type` | string | none | `dealer` or `private` |
| `country` | string | `us` | Optional |

### Listing, dealers, dealer, makes and models

| Endpoint | Parameters |
|---|---|
| `/listing` | one of `listing_id` (`796688649`) or `url` (a kbb.com cars-for-sale vehicle link); `zip` (optional: `seller.distance_miles` is measured from it, `null` without it) |
| `/dealers` | `zip` (required); `make` (only dealers of this make); `radius` 10, 25, 50, 75, 100, 200, 300, 500 or 0 (any; KBB's default 25) |
| `/dealer` | one of `dealer_id` (`87788`) or `url` (a kbb.com dealer link) |
| `/makes-models` | `vehicle_class` `used` (default: every model year KBB values) or `new` (models sold new); `make` (only this make's models) |

## Examples

### A car's KBB values at a ZIP you choose

```bash
curl -X POST https://api.scavio.dev/api/v1/kbb/car-value \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "Toyota", "model": "rav4", "year": 2021, "trim": "LE", "mileage": 40000, "zip": "10001"}'
```

Captured `data` (2026-11-26, 2 credits, 36 seconds; `headline` cut to 2 of 4, `prices` to 5 of 17, `url` and `notes` dropped):

```json
{
  "vehicle": {"make": "Toyota", "make_slug": "toyota", "model": "RAV4", "model_slug": "rav4", "year": 2021, "trim": "LE Sport Utility 4D", "trim_slug": "le-sport-utility-4d", "vehicle_id": 449733, "body_style": "SUV"},
  "intent": "buy_used",
  "condition": "good",
  "mileage": 40000,
  "typical_mileage": 78057,
  "location": {"zip": "10001", "chosen_zip": true, "valid_text": "Valid for ZIP Code 10001 through 11/26/2026", "valid_through": "2026-11-26"},
  "valuation_date": "2026-11-26",
  "headline": {
    "fair_purchase_price": {"type_id": 130, "type": "Fair Purchase Price", "category": "FPP", "condition": null, "value": 25410, "base_value": 22900, "region_adjustment": -420, "mileage_adjustment": 2930, "option_adjustment": 0, "range_low": 23210, "range_high": 27610},
    "private_party": {"type_id": 7, "type": "Private Party Value Good", "category": "Private Party", "condition": "Good", "value": 23820, "base_value": 21300, "region_adjustment": -410, "mileage_adjustment": 2930, "option_adjustment": 0, "range_low": 21720, "range_high": 25920}
  },
  "prices": [
    {"type_id": 1, "type": "Lending Value", "category": "Wholesale", "condition": null, "value": 21450, "range_low": null, "range_high": null},
    {"type_id": 2, "type": "Typical Listing Price", "category": "Retail", "condition": null, "value": 26000, "range_low": 23800, "range_high": 28200},
    {"type_id": 4, "type": "Trade-In Value Good", "category": "Trade-In", "condition": "Good", "value": 19450, "range_low": 17300, "range_high": 21650},
    {"type_id": 76, "type": "Auction Value Good", "category": "Auction", "condition": "Good", "value": 19850, "range_low": null, "range_high": null},
    {"type_id": 131, "type": "Fair Purchase Price (CPO)", "category": "CPO FPP", "condition": null, "value": 26000, "range_low": 23900, "range_high": 28200}
  ],
  "market": {"country": "us", "currency": "USD"}
}
```

`prices` entries above are shortened to their value and range; each one carries `base_value` and the three adjustments too. The same car without `zip` (1 credit, 13 seconds) came back for ZIP 92620 with Fair Purchase Price 25,950 (`region_adjustment` 120). A new 2026 RAV4 LE with `intent: "buy_new"` read MSRP 33,350, Invoice 31,437 and Fair Purchase Price 33,400 (range 33,200-33,500).

### One model year

`/model` `{"make": "Toyota", "model": "rav4", "year": 2021}` (1 credit): `zip` 92620, 13 trims, including RAV4 Hybrid and RAV4 Prime trims (`le-sport-utility-4d` of the RAV4: `fair_purchase_price` 22,900, `trade_in_value` 16,850, `private_party_value` 21,300, `epa_combined` 30, `horsepower` "203 @ 6600 RPM", `drivetrain` AWD, `cargo_capacity_cu_ft` 69.8); `depreciation` {"three_year_depreciation": 1788, "current_resale_value": 21300, "current_trade_in_value": 16850, `history` 2023-2026, `forecast` [{"year": 2027, "resale_value": 18456, "trade_in_value": 14600, "annual_depreciation": 2844}, {"year": 2028, "resale_value": 16070, "trade_in_value": 12712, "annual_depreciation": 2386}]}; `rankings` on Horsepower, MPG Combined and Consumer Ratings; `best_cars` {"list": "Best 2-Row SUVs", "rank": 100, "winner": false}; `years` 1996 to 2027. With `model: "f-150"` KBB answered with its F150 Super Cab page (23 trims across the F150 cabs) and a note naming the model it used: send the slug `/makes-models` gives.

### Cars for sale with KBB's deal rating

```bash
curl -X POST https://api.scavio.dev/api/v1/kbb/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "10001", "make": "Toyota", "model": "RAV4", "listing_type": "used"}'
```

Captured `data` (2026-11-26; `listings` cut to 1 of 25 and its specs shortened; `url`, `image`, `warranties`, `spotlights` (3) and `notes` dropped):

```json
{
  "search": {"zip": "10001", "listing_type": "used", "make": "Toyota", "model": "RAV4"},
  "location": {"zip": "10001", "place": "New York, NY", "radius_miles": 25},
  "filters_applied": {"make": "TOYOTA", "model": "RAV4"},
  "filters_not_applied": [],
  "sort": "relevance",
  "page": 1,
  "page_size": 25,
  "total": 574,
  "total_pages": 23,
  "has_more": true,
  "count": 25,
  "listings": [
    {"listing_id": "796688649", "title": "Used 2020 Toyota RAV4 LE w/ Carpet Mat Package", "year": 2020, "make": "Toyota", "model": "RAV4", "model_code": "RAV4", "trim": "LE", "listing_type": "used", "mileage": 4709, "exterior_color": "Midnight Black Metallic", "drivetrain": "AWD4WD", "engine": "Hybrid", "days_on_site": 6, "newly_listed": true, "reduced_price": false, "price": 27665, "display_price": 27665, "msrp": null, "price_label": null, "deal_label": "Great", "kbb_fair_purchase_price": {"amount": 31443, "low": 30143, "high": 32743, "delta": 3778}, "dealer_fees": {"total": 512, "items": [{"name": "Documentation Fee", "amount": 175}, {"name": "Inspection Fee", "amount": 37}, {"name": "Registration Fee", "amount": 300}]}, "price_history": [], "history_preview": ["NO_SALVAGE_TITLE", "NO_ACCIDENTS_REPORTED", "ONE_OWNER"], "sponsored": false, "seller": {"type": "dealer", "dealer_id": "72770671", "name": "Toyota City", "rating": 5, "rating_count": 2892, "city": "Mamaroneck", "state": "NY", "distance_miles": 20.3}}
  ],
  "stats": {"price": {"min": 2995, "avg": 29294, "max": 51109}, "mileage": {"min": 1, "avg": 49131, "max": 251200}, "year": {"min": 2002, "avg": 2022, "max": 2026}},
  "market": {"country": "us", "currency": "USD"}
}
```

With `{"zip": "75201", "make": "Ford", "model": "F-150", "sort": "price_asc", "year_min": 2018, "price_max": 40000}` KBB read the model as F150 (`filters_applied` {"make": "FORD", "model": "F150PICKUP", "year_min": 2018, "price_max": 40000}, a note says so), 1,190 cars; the first a private seller's 2018 F150 XLT with 224,302 miles at 7,000, `deal_label` "Good", `kbb_fair_purchase_price` {"amount": 6860, "delta": -140}, `seller` {"type": "private", "city": "Keller", "state": "TX", "distance_miles": 29.6}. A 2024 Civic Sport near 10001 showed `price` 23,250, `display_price` 23,425 with a 175 documentation fee, and `price_history` 23,533 (Nov 16), 23,708 (Nov 17), then 23,425.

### One listing

`/listing` `{"listing_id": "796688649", "zip": "10001"}` (1 credit, 7 seconds): the search fields plus `features` by group, `ranked_features`, `specifications` {"drive_type": "All wheel drive", "engine_description": "Hybrid Gas/Electric Engine", "transmission": "Continuously Variable Automatic" ...}, `warranties` (Basic "3 Years/36,000 Miles", `remaining_miles` 31,291 ...), `kbb_consumer_rating` 3.6 from 398 reviews, `kbb_vehicle_id` 446192, `recall_count` 0 with `recall_note` "No recall found based on AutoCheck report.", `price_valid_until` "2027-11-20", and `dealer` (Toyota City, Mamaroneck, NY, with address, phone, website and hours). A private seller's listing returned `dealer` `null` and `seller` with city and state only.

### Owner reviews

`/reviews` `{"make": "Toyota", "model": "rav4", "year": 2021}` (1 credit): `total` 398, `total_pages` 50, `ratings` {"rating": 3.6, "review_count": 398, "value": 3.6, "reliability": 3.9, "performance": 3.8, "styling": 4.3, "comfort": 3.9, "quality": 3.7, "recommendation": 3.4, "distribution": {"five": 171, "four": 66, "three": 56, "two": 56, "one": 49}}, `most_helpful` positive titled "Toyota reliability, but very noisy". A review: `rating` 3, `title` "Multiple issues off the lot", `ratings` {"value": 3, "reliability": 5, "performance": 5 ...}, `ownership` "I own this car", `staff` false, `incentivized` false. No reviewer name or location is returned. `{"make": "Honda", "model": "civic", "year": 2020, "sort": "rating_asc"}` (5 credits, 129 seconds) opened on a 1-star review titled "Overrated"; `{"make": "Ford", "model": "f150-supercrew-cab", "year": 2019, "stars": 5, "page": 2}` (5 credits) counted 230 five-star reviews over 29 pages.

### Dealers, dealer, makes and models

- `/dealers` `{"zip": "75201", "make": "Ford", "radius": 50}`: 50 dealers in Dallas, TX within 50 miles, first Westway Ford (`87788`, rating 4.6 from 5,621, 10 miles, Irving TX), then Planet Ford 635 (Garland) ...; `{"zip": "90012", "make": "Honda"}`: 38 dealers within 25 miles, first New Century Honda (`71080617`, 4.9 from 5,052, Glendale).
- `/dealer` `{"dealer_id": "87788"}`: Westway Ford, 801 West Airport Freeway, Irving, TX 75062, hours Monday 9:30 AM-7:00 PM ..., `home_services` {"buy_online": false, "test_drive": true, "vehicle_delivery": true, "virtual_tour": true}, `inventory_count` 496, `price_stats` {"min": 13054, "avg": 49089, "max": 216535}, `makes` with counts, and `inventory` (25 cars, newest model year first).
- `/makes-models` `{}`: 68 makes, 1,519 models with slugs and model years. `{"make": "ford"}`: 105 Ford models (F150 Regular Cab `f150-regular-cab`, F150 Super Cab `f150-super-cab`, F150 SuperCrew Cab `f150-supercrew-cab`, F150 Lightning ...). `{"vehicle_class": "new", "make": "Toyota"}`: 36 models sold new (bZ, bZ Woodland, bZ4X, C-HR, Camry ...).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def kbb(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/kbb/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# The trim slug for a model year (1 credit)
m = kbb("model", {"make": "Toyota", "model": "rav4", "year": 2021})["data"]
trim = next(t["trim_slug"] for t in m["trims"] if t["model_slug"] == "rav4" and t["name"].startswith("LE"))

# KBB's values for that trim at a ZIP you choose (2 credits, or 6)
res = kbb("car-value", {"make": "Toyota", "model": "rav4", "year": 2021, "trim": trim,
                        "mileage": 40000, "condition": "good", "zip": "10001"})
v = res["data"]
print(v["location"]["valid_text"], res["credits_used"], "credits")
for p in v["prices"]:
    print(p["type"], p["value"], p["range_low"], p["range_high"])

# Cars for sale of the same model year near the ZIP (1 credit)
s = kbb("search", {"zip": "10001", "make": "Toyota", "model": "RAV4", "listing_type": "used",
                   "year_min": 2021, "year_max": 2021, "sort": "price_asc"})["data"]
for c in s["listings"]:
    fpp = c["kbb_fair_purchase_price"] or {}
    print(c["listing_id"], c["trim"], c["mileage"], c["price"], c["deal_label"], fpp.get("amount"))

# Store each answer with fetched_at: that stored set is your record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every answer carries `market` and most carry `notes`.

- **car value** - `vehicle` {`make`, `make_slug`, `model`, `model_slug`, `year`, `trim`, `trim_slug`, `vehicle_id`, `body_style`}, `intent`, `condition`, `mileage`, `typical_mileage`, `location` {`zip`, `chosen_zip`, `valid_text`, `valid_through`}, `valuation_date`, `headline`, `prices[]` {`type_id`, `type`, `category`, `condition`, `value`, `base_value`, `region_adjustment`, `mileage_adjustment`, `option_adjustment`, `range_low`, `range_high`}, `url`, `market`, `notes`.
- **model** - `make_slug`, `model_slug`, `make`, `model`, `year`, `zip`, `categories`, `trims[]` {`vehicle_id`, `name`, `trim_slug`, `model`, `model_slug`, `body_style`, `fair_purchase_price`, `trade_in_value`, `private_party_value`, `combined_mpg`, `epa_city`, `epa_highway`, `epa_combined`, `mpge_combined`, `horsepower`, `torque`, `engine`, `drivetrain`, `seating`, `curb_weight_lbs`, `towing_capacity_lbs`, `cargo_capacity_cu_ft`, `ev_range_miles`, `is_ev`, `url`}, `new_car_pricing[]` {`trim`, `trim_id`, `msrp`, `fair_purchase_price`, `fair_market_range` {`low`, `high`}, `epa_city`, `epa_highway`}, `new_car_summary`, `depreciation`, `specs` {`fuel_economy`, `fuel_type`, `horsepower`, `max_seating`, `cargo_space`, `maximum_towing`, `basic_warranty`, `additional[]` {`category`, `specs[]` {`name`, `value`}}}, `rankings[]` {`metric`, `value`, `top[]`}, `best_cars` {`list`, `rank`, `winner`, `url`}, `years`, `other_models`, `image`, `url`, `market`, `notes`.
- **car for sale** (search, dealer inventory) - `listing_id`, `url`, `title`, `year`, `make`, `make_code`, `model`, `model_code`, `trim`, `trim_code`, `listing_type`, `mileage`, `exterior_color`, `interior_color`, `body_style`, `drivetrain`, `engine`, `fuel`, `transmission`, `mpg_city`, `mpg_highway`, `doors`, `days_on_site`, `newly_listed`, `reduced_price`, `price`, `display_price`, `msrp`, `price_label`, `deal_label`, `kbb_fair_purchase_price` {`amount`, `low`, `high`, `delta`}, `dealer_fees` {`total`, `items[]`}, `price_history[]` {`date`, `price`, `current`}, `history_preview`, `warranties`, `image`, `sponsored`, `seller` ({`type`: dealer, `dealer_id`, `name`, `rating`, `rating_count`, `city`, `state`, `distance_miles`, `url`} or {`type`: private, `city`, `state`, `distance_miles`}).
- **search** - `search` {`zip`, `listing_type`, `make`, `model`}, `location` {`zip`, `place`, `radius_miles`}, `filters_applied`, `filters_not_applied`, `sort`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `listings[]`, `spotlights[]` (paid placements, `sponsored: true`), `stats` {`price`, `mileage`, `year`: {`min`, `avg`, `max`}}, `market`, `notes`.
- **listing** - the car fields plus `description`, `images`, `features` {group: [...]}, `ranked_features`, `specifications`, `warranties[]` {`group`, `type`, `label`, `details`, `years`, `miles`, `unlimited_miles`, `remaining_years`, `remaining_miles`}, `kbb_consumer_rating`, `kbb_consumer_review_count`, `deal_basis`, `dealer` {`dealer_id`, `name`, `rating`, `rating_count`, `address`, `phone`, `website`, `hours[]` {`day`, `open`, `close`}, `home_services`, `is_open`, `url`} or `null`, `kbb_vehicle_id`, `recall_count`, `recall_note`, `price_valid_until`, `zip`, `market`, `notes`.
- **reviews** - `vehicle` {`make`, `make_slug`, `model_slug`, `year`}, `sort`, `stars`, `page`, `per_page`, `total`, `total_pages`, `has_more`, `count`, `reviews[]` {`review_id`, `title`, `text`, `rating`, `ratings` {`value`, `reliability`, `performance`, `styling`, `comfort`, `quality`}, `recommend`, `date`, `ownership`, `year`, `make`, `model`, `pros`, `cons`, `helpful_yes`, `helpful_no`, `photos`, `staff`, `incentivized`}, `ratings` {`rating`, `review_count`, `value`, `reliability`, `performance`, `styling`, `comfort`, `quality`, `recommendation`, `distribution` {`five` ... `one`}}, `most_helpful` {`positive`, `negative`} (page 1), `url`, `market`, `notes`.
- **dealers** - `search` {`zip`, `make`}, `location` {`zip`, `place`, `radius_miles`}, `count`, `dealers[]` {`dealer_id`, `name`, `franchise_name`, `make`, `rating`, `rating_count`, `distance_miles`, `address` {`street`, `street2`, `city`, `state`, `zip`}, `phone`, `website`, `hours`, `home_services`, `is_open`, `url`}, `market`, `notes`.
- **dealer** - as a dealer above plus `hours[]`, `home_services` {`buy_online`, `test_drive`, `vehicle_delivery`, `virtual_tour`}, `is_open`, `inventory_count`, `price_stats` {`min`, `avg`, `max`}, `makes[]` {`make`, `make_code`, `count`}, `inventory_sort`, `inventory[]` (the car fields), `market`, `notes`.
- **makes and models** - `vehicle_class`, `make`, `make_count`, `count`, `makes[]` {`make`, `make_slug`, `model_count`}, `models[]` {`make`, `make_slug`, `model`, `model_slug`, `years`}, `market`, `notes`.

## Guardrails

- Name it "Kelley Blue Book (kbb.com, Cox Automotive's car value and research site)" on first mention, "Kelley Blue Book" or "KBB" after that.
- Values: quote each with KBB's own price-type name, the year, make, model and trim, the mileage and condition, the ZIP from `location.valid_text` and the `fetched_at` date ("KBB Private Party Value Good 23,820 for a 2021 RAV4 LE with 40,000 miles, ZIP 10001, on kbb.com on Nov 26, 2026"). Say "Kelley Blue Book's value, as KBB gives it"; never present it as what the user's car is worth, an offer, an appraisal or a trade-in quote.
- Listed prices: quote each with the car's mileage, the seller (dealer name, or "a private seller in Keller, TX"), the ZIP and radius, and KBB's deal rating as KBB's. Mention `dealer_fees` where `display_price` includes them. Never compute an out-the-door price.
- Comparisons: the same year, make, model and trim, mileage beside every number, named site and date. No verdict on which car or dealer is a better deal beyond KBB's own deal rating and the numbers shown.
- Private sellers and reviewers: no one is named or identified; never try to recover a private seller's identity or a VIN.
- Descriptive only: no commentary on KBB's business, methods, pricing practices or policies, or on any dealer's.
- Do not republish KBB photos or descriptions. Write kbb.com as plain text and cite listing ids, dealer ids, slugs and capture dates rather than linking KBB pages.
- Terms: Scavio does not collect or store Kelley Blue Book data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no offer or purchase flow. Kelley Blue Book's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate values, prices, trims, listing ids, dealers or review text. Only return what the API returned, with the `fetched_at` time.
- Not available: VIN lookup, an instant offer, dealer reviews, free-text search, a `buy_new` value at a chosen ZIP, payments and taxes, markets outside the US.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a missing `make` ("make is required (e.g. Toyota).") or a make KBB does not list; a missing or malformed `model` ("model is required: KBB's model slug, e.g. rav4, civic, f150-supercrew-cab (makes_models lists them)."); a missing `year` ("year is required (a model year, e.g. 2021).") or one outside 1981-2028; a missing `trim` or one several trims share ("trim \"...\" matches N Kelley Blue Book trims of the ...; pass one trim_slug: ..."); `zip` with `buy_new` ("zip is offered for buy_used and trade_in_sell values only; a buy_new value is for Kelley Blue Book's default location (location.zip says which)."); `zip` without `mileage` ("mileage is required with zip (the odometer miles KBB values the car at)."); a ZIP that is not 5 digits ("zip must be a 5-digit US ZIP code.") or not a US ZIP code; search or dealers without `zip`; `model` without `make` ("model needs make (e.g. make Toyota, model RAV4)."); `model` with `model_code` ("pass model or model_code, not both."); a `radius`, `page_size`, `sort`, `drivetrain` or `exterior_color` outside its list; a `_min` above its `_max` ("year_min must not be greater than year_max."); a reviews sort for most helpful ("Most Helpful is not offered"); `/listing` without `listing_id` or `url` ("listing_id or url is required") or a link that is not a KBB listing; `/dealer` without `dealer_id` or `url` ("dealer_id or url is required"); a `country` other than `us`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits, or below what the call can bill (6 for a car value with `zip`, 5 for reviews beyond page 1, other sorts or `stars`). The body carries `billing_url`.
- `404` means not found, and it is charged: "Kelley Blue Book has no page for the <year> <make> <model> (check the model slug with makes_models: KBB writes f150-supercrew-cab, not f-150).", "Kelley Blue Book lists no trim \"...\" for the ... Trims (pass the trim_slug): ...", "Kelley Blue Book has no value page for the ...", "Kelley Blue Book lists no model \"...\" for Toyota near this ZIP. Models listed for Toyota: ...", "Kelley Blue Book has no listing <id> (sold, removed or never listed).", "The <year> <make> <model> has <n> review pages for this sort and rating on Kelley Blue Book (page <page> asked).", "Kelley Blue Book has no consumer reviews page for the ...", "Kelley Blue Book has no dealer ...", "Kelley Blue Book has no dealer results page for this search.". Take slugs, trims, listing ids and dealer ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=kelley-blue-book-api).
- `502` means KBB data was temporarily unavailable ("Kelley Blue Book is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service cannot reach KBB right now (same message): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.97.0
npm install scavio@0.98.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: value } = await scavio.kbb.carValue({ make: "Toyota", model: "rav4", year: 2021, trim: "LE", mileage: 40000, zip: "10001" });
const { data: model } = await scavio.kbb.model({ make: "Toyota", model: "rav4", year: 2021 });
const { data: cars } = await scavio.kbb.search({ zip: "10001", make: "Toyota", model: "RAV4", listing_type: "used" });
const { data: reviews } = await scavio.kbb.reviews({ make: "Toyota", model: "rav4", year: 2021 });
const { data: dir } = await scavio.kbb.makesModels({ make: "ford" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.kbb.car_value(...)`, `model`, `search`, `listing`, `reviews`, `dealers`, `dealer` and `makes_models`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 8 endpoints as tools: `get_kbb_car_value`, `get_kbb_model`, `search_kbb`, `get_kbb_listing`, `get_kbb_reviews`, `get_kbb_dealers`, `get_kbb_dealer` and `get_kbb_makes_models`. Kelley Blue Book is opt-in: add `kbb` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.97.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,kbb"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [car value](https://scavio.dev/docs/kbb-car-value?utm_source=agent-skills&utm_medium=skill&utm_campaign=kelley-blue-book-api), [model](https://scavio.dev/docs/kbb-model?utm_source=agent-skills&utm_medium=skill&utm_campaign=kelley-blue-book-api), [search](https://scavio.dev/docs/kbb-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=kelley-blue-book-api), [listing](https://scavio.dev/docs/kbb-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=kelley-blue-book-api), [reviews](https://scavio.dev/docs/kbb-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=kelley-blue-book-api), [dealers](https://scavio.dev/docs/kbb-dealers?utm_source=agent-skills&utm_medium=skill&utm_campaign=kelley-blue-book-api), [dealer](https://scavio.dev/docs/kbb-dealer?utm_source=agent-skills&utm_medium=skill&utm_campaign=kelley-blue-book-api), [makes and models](https://scavio.dev/docs/kbb-makes-models?utm_source=agent-skills&utm_medium=skill&utm_campaign=kelley-blue-book-api). Overview: [Kelley Blue Book API](https://scavio.dev/kbb-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=kelley-blue-book-api).
