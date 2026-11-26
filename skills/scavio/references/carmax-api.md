# CarMax API - Used Car Prices, Car Value Offers, Store Inventory

Read CarMax (carmax.com, the US used-car retailer with no-haggle prices, 263 stores in 42 states as CarMax states it): used-car search around a US ZIP, one car in full, its photos, CarMax's stores and one store's lot, owner reviews of a model-year, make and model lists, and CarMax's recent instant offers for a model-year. Every answer is what CarMax's public pages show a visitor without an account at the moment of the call, in USD. All 12 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages CarMax shows to any visitor and returns them as JSON for analysis. It uses no CarMax account, no saved cars, no financing pre-qualification, no reservation and no offer request for a car.

**The job this skill is for: what CarMax recently offered for a model-year, next to what CarMax lists that model-year at.** `/car-value` returns the recent instant offers CarMax shows on its value page for one model-year (mileage, trim, offer and date per offer), and `/search` returns CarMax's own no-haggle prices for the same model-year around a ZIP. Captured 2026-11-26 (1 credit per call):

| Model-year | Recent CarMax offers (`offer_range`, 10 offers) | Value-page headline (`headline_range`) | CarMax listed prices, same model-year (`/search`) |
|---|---|---|---|
| 2021 Toyota RAV4 | 16,400-22,000 (Oct 12 - Nov 25, 2026) | $18,400-$23,400 | 25,998 (LE, 52,175 mi, Merrillville IN) and 29,998 (XLE, 33,335 mi, Oak Lawn IL), zip 60601, radius 75 |
| 2019 Ford F-150 | 11,000-20,000 (Oct 11 - Nov 25) | $16,400-$25,400 | 27,998 (XL, 14,014 mi, Plano TX), zip 75201, radius 100 |
| 2017 Honda Civic | 6,600-12,400 (Oct 12 - Nov 26) | $9,400-$13,400 | 15,998 (EX, 110,877 mi, Canoga Park CA) and 16,998 (EX, 94,906 mi, Burbank CA), zip 90012, radius 25, `price_min` 15000; 18,998 (EX, 83,386 mi, Town Center GA), zip 30301 |

The offers are for other cars of that model-year, each with its own mileage and trim; the listed prices are for specific cars on CarMax's lots. Put both side by side with their mileage, trim and dates, and leave the difference uninterpreted: it is not CarMax's margin, and an offer range is not what any one car would be offered. For another retailer's price on the same model-year use `carvana-api` (Carvana's price next to the KBB value it shows), `cargurus-api`, `autotrader-api` or `cars-com-api`, matched on year, make, model, trim and mileage band.

Ten limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Car value is recent CarMax offers, not an appraisal.** `/car-value` is what CarMax offered for cars of that model-year as its value page shows them: `offer_range` is CarMax's range across the recent offers listed, `headline_range` the range its page headline states, and they can differ widely (2019 F-150: offers 11,000-20,000, headline $16,400-$25,400). Quote both with their labels. Never present either as a value for the user's car, an instant offer they can get, or a trade-in quote.
- **A ZIP is required for search and store inventory.** CarMax prices each car's shipping fee and dates to `zip`, and `radius` is measured from it (5, 25, 50, 75, 100, 250, 500 or `nationwide`; without `radius`, every CarMax car with the shipping fee to that ZIP). Report the ZIP and radius with every list.
- **Shipping is per ZIP and only on lists.** `shipping.fee` is CarMax's fee to the ZIP (0 = free, `null` when the car is at the nearby store and can be test-driven there); `shipping.text` and `arrival` are CarMax's wording ("Free shipping • Nov 28-Dec 7"). `/listing` carries no shipping: read it from `/search` or `/store-inventory` with a `zip`.
- **Prices are CarMax's no-haggle prices, before what CarMax's state terms exclude.** `/store` returns `fee_disclaimer`, CarMax's price and fee terms for that store's state, and they differ (the Irving, TX store's price excludes taxes, title, registration and tags; the Wayne, NJ store's includes all costs except licensing, registration and taxes). Quote the store's own terms with a price; never compute an out-the-door price.
- **Price drops as CarMax gives them.** Lists carry `original_price` and `price_drop`; `/listing` adds `previous_price`, `price_drop_date`, `price_drop_expires` and `price_drop_text` ("We lowered this price by $1,000 on November 20, 2026 to match current market trends."). There is no longer price history: store your own answers with `fetched_at`.
- **No VIN.** No endpoint returns a VIN. The car's id everywhere is CarMax's `stock_number` (6 to 10 digits).
- **History as CarMax shows it.** `history` (accident and owner counts, prior uses) and the `car_life` callouts are CarMax's, which cites AutoCheck. Report them as CarMax's statement about the car, not as an independent history.
- **Slow pages.** Search answered in 4 to 43 seconds in the captures, a 100-car page can take CarMax about 80 seconds, and car value 20 to 28. Set a client timeout of at least 240 seconds and send one request at a time.
- **What is not there.** No VIN, no appraisal or offer for a specific car, no monthly payments or financing, no taxes, no trim filter (filter by facets, read `trim` per car), no price history beyond the last drop, no reservation, no checkout. Paging stays within the first 10,000 cars of a search.

CarMax publishes no public API or affiliate data feed for its inventory, prices or value pages. This skill reads CarMax's public pages with one Scavio key.

See also: `carvana-api` (Carvana's listed prices next to the KBB value Carvana shows), `cars-com-api`, `autotrader-api` and `cargurus-api` (dealer and private listings across the US), and `offerup-api` (local private-party cars by ZIP). Same model-year only: match year, make, model and trim, keep the mileage beside each price, and name the retailer and date with every number.

## When to trigger

Use this skill when the user asks to:
- Read CarMax's recent instant offers for a model-year (car value) and put them next to CarMax's listed prices for that model-year
- Search CarMax's used cars by make, model, body type or keyword around a ZIP, sorted by price, mileage, year or distance, filtered by price, mileage, year, drivetrain, colour, engine type, features or max shipping fee
- Read one CarMax car in full: price, price drop and its date, mileage, accident and owner counts, warranties, features, specifications, reconditioning
- Get every photo of a CarMax car
- Find CarMax stores near a ZIP or in a state or city, read a store's hours and price terms, or list one store's lot
- Read CarMax owner reviews of a model-year, the star distribution and top likes and dislikes
- Look up the makes and models CarMax lists, or suggestions for the start of a name

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example 25 model-years: one car value and one search each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, listing answered in 3-22 seconds, photos 2-3, stores 3-5, store 5, store inventory 8-10, reviews 3-6, review summary 10-17, suggestions 11-13, makes 13, models 15-19, car value 20-28 and search 4-43. Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/carmax/search` | Used cars by make / model, body type or keyword around a ZIP: price, original price, price drop, mileage, specs, store, distance, shipping fee and dates; total, paging, applied filters, nearest store, facets with counts on request | 1 |
| `POST /api/v1/carmax/listing` | One car by stock number or link: price, price-drop date and text, history, `car_life` callouts, warranties, features, specifications, reconditioning, store, pros and cons | 1 |
| `POST /api/v1/carmax/photos` | Every photo of one car: type (image or 360), category, shot, three sizes | 1 |
| `POST /api/v1/carmax/stores` | Stores near a ZIP (nearest first) or in a state or city: address, phones, coordinates, hours, service and holiday hours | 1 |
| `POST /api/v1/carmax/store` | One store: address, phones, hours, holiday hours, open now, alert, the state's price and fee terms | 1 |
| `POST /api/v1/carmax/store-inventory` | One store's lot with the search filters, sorts and paging; `total` is the lot count | 1 |
| `POST /api/v1/carmax/reviews` | Owner reviews of one model-year: 10 a page, 5 sorts, star filter, distribution, top likes and dislikes (no names) | 1 |
| `POST /api/v1/carmax/review-summary` | The owner-review summary of one model-year: count, average, distribution, top likes and dislikes | 1 |
| `POST /api/v1/carmax/suggestions` | Make and model suggestions for the start of a name, with slugs | 1 |
| `POST /api/v1/carmax/makes` | Every make CarMax lists, with slugs | 1 |
| `POST /api/v1/carmax/models` | One make's models, with slugs | 1 |
| `POST /api/v1/carmax/car-value` | Recent CarMax instant offers for one model-year: offer range, headline range, each offer's mileage, trim and date, ranges per trim, median offer by year | 1 |

## Market

US only, USD. There is no `country` or `currency` input. CarMax states 263 stores in 42 states; `/stores` lists them by ZIP, state or city.

## Prices, offers and shipping

| Field | Meaning |
|---|---|
| `price` | CarMax's no-haggle price, USD, as listed (before what the store's state terms exclude) |
| `original_price`, `price_drop` (lists) | CarMax's earlier price and drop flag as given; `original_price` `null` without a drop |
| `previous_price`, `price_drop_date`, `price_drop_expires`, `price_drop_text` (listing) | CarMax's last price change and its own wording |
| `badge` | CarMax's label as given (`Price drop`, `Popular`) |
| `shipping` | {`fee` (USD to the ZIP; 0 free; `null` for a test drive at the nearby store), `text`, `type` (`test-drive` or `shipping-from`), `transferable`, `arrival`, `min_days`, `max_days`} |
| `distance_miles` | Miles from the ZIP to the car's store |
| `history` (listing) | {`accident_count`, `owner_count`, `prior_uses`} as CarMax shows them (CarMax cites AutoCheck) |
| `offer_range` (car value) | CarMax's range across the recent offers on its value page |
| `headline_range` (car value) | The range CarMax's page headline states {`text`, `low`, `high`}; can differ from `offer_range` |
| `recent_offers[]` (car value) | {`mileage`, `offer`, `offered_at`, `trim`, `trim_code`} per offer, as CarMax lists them |
| `trim_ranges[]`, `median_offer_history[]` | CarMax's offer range per trim (trim names and codes as given, e.g. `LARI`, `K029`) and median offer by year |

- **Percent or dollar change:** compute it from `previous_price` and `price` and label it computed (45,998 to 44,998 is 1,000 lower, computed).
- **Stock numbers:** `stock_number` is the id for `/listing` and `/photos`. Send it as a string or number (`"28466923"`). A sold car leaves CarMax's site: a `404`.

## Workflow

1. **Names.** `/suggestions` (`{"query": "rav"}`), `/makes` or `/models` (`{"make": "ford"}`) for the names and slugs CarMax uses (F-150 is read as F150).
2. **Offers for the model-year.** `/car-value` with `make`, `model`, `year`. Note `offer_range`, `headline_range`, the offer dates, and `trim_ranges`.
3. **Listed prices for the same model-year.** `/search` with `make`, `model`, `zip`, `radius`, and `year_min` = `year_max` = the year (add `sort: "price_asc"`). Note each car's `trim`, `mileage`, `price`, store and `shipping.fee`.
4. **One car.** `/listing` with the `stock_number` for the price drop, history, warranties and reconditioning; `/photos` for its photos.
5. **A store.** `/stores` with `zip` for the nearest, `/store` for its hours and `fee_disclaimer`, `/store-inventory` with `store_id` and `zip` for its lot.
6. **Owners.** `/review-summary`, then `/reviews` with `sort` and `rating` for the model-year.
7. **Report.** Each price or offer with CarMax, the ZIP, store or model-year, mileage, trim and the `fetched_at` date; the offer range and the headline range with their labels; no verdict.
8. **Price series:** there is no history beyond the last drop. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`) and store inventory (`/store-inventory`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | A 5-digit US ZIP code: shipping fees and dates are priced to it, and the radius is measured from it |
| `make` | string | none | A make by name or slug (`Ford`, `land-rover`) |
| `model` | string | none | With `make`: a model by name or slug (`F-150` and `F150` both work, `RAV4`, `CX-5`, `Model 3`) |
| `keyword` | string | none | Search only: free text across every make (`hybrid`); not combined with `make` / `model`. CarMax can map it to filters (`applied` says which: `hybrid` became the Hybrid and Plug-In Hybrid engine types) |
| `body_type` | string | none | A body type as CarMax writes it: `suvs`, `sedans`, `trucks`, `coupes`, `hatchbacks`, `minivans-and-vans`, `convertibles`, `wagons` |
| `filters` | list | none | Up to 8 facet `url_segment` values (`["all-wheel-drive", "black"]`), from `facets[].values[].url_segment` |
| `year_min`, `year_max` | integer | none | Model year range (1980 to next year) |
| `price_min`, `price_max` | integer | none | Price range, USD |
| `mileage_min`, `mileage_max` | integer | none | Mileage range |
| `max_shipping_fee` | integer | none | 0, 99, 199, 299, 399, 499 or 999 (USD; 0 = free to home or store) |
| `radius` | string | every car | Search only: 5, 25, 50, 75, 100, 250, 500 or `nationwide` (miles from `zip`). Not accepted on store inventory |
| `store_id` | string | required (store inventory) | A CarMax store id from `/stores` (`7115`) |
| `sort` | string | `best_match` | `best_match`, `distance`, `price_asc`, `price_desc`, `mileage_asc`, `mileage_desc`, `year_desc`, `year_asc` |
| `page` | integer | 1 | Page; `has_more` says whether another exists |
| `page_size` | integer | 24 | 1-100 (100 cars can take CarMax 80 seconds) |
| `include_facets` | boolean | false | Every filter value with `url_segment` and count (makes carry their models), and the year, price and mileage ranges with counts |

### Car value (`/car-value`), reviews (`/reviews`), review summary (`/review-summary`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `make` | string | required | A make by name or slug (`Ford`, `Toyota`) |
| `model` | string | required | A model by name or slug (`F-150` is read as `f150`, `RAV4`) |
| `year` | integer | required | The model year (`2019`) |
| `page` | integer | 1 | Reviews only: 10 reviews a page; `total_pages` says how deep they go |
| `sort` | string | `most_helpful` | Reviews only: `most_helpful`, `newest`, `oldest`, `highest_rating`, `lowest_rating` |
| `rating` | integer | none | Reviews only: only reviews with exactly this many stars (1-5) |

### Listing, photos, stores, store, suggestions, makes, models

| Endpoint | Parameters |
|---|---|
| `/listing`, `/photos` | one of `stock_number` (`28466923`) or `url` (a carmax.com car link as `cars[].url` gives it) |
| `/stores` | one of `zip`, `state` (`TX` or `Texas`) or `city` (`Atlanta`); `limit` 1-50 (default 25) |
| `/store` | `store_id` (`7115`) |
| `/suggestions` | `query` (2-60 characters, the start of a make or model name) |
| `/makes` | none (`{}`) |
| `/models` | `make` (a name or slug from `/makes`) |

## Examples

### Recent CarMax offers for a model-year

```bash
curl -X POST https://api.scavio.dev/api/v1/carmax/car-value \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "Ford", "model": "F-150", "year": 2019}'
```

Captured `data` (2026-11-26; `recent_offers` cut to 4 of 10, `trim_ranges` to 4 of 7, `other_years`, `url` and `notes` dropped):

```json
{
  "make": "Ford",
  "model": "F150",
  "year": 2019,
  "currency": "USD",
  "offer_range": {"low": 11000, "high": 20000},
  "headline_range": {"text": "$16,400-$25,400", "low": 16400, "high": 25400},
  "aggregate": {"low": 11000, "high": 20000, "offer_count": 10},
  "offers_from": "2026-10-11T20:21:28.2375642Z",
  "offers_to": "2026-11-25T19:56:44.8099557Z",
  "count": 10,
  "recent_offers": [
    {"mileage": 60000, "offer": 18000, "offered_at": "2026-11-25T18:26:56.5137571Z", "trim": "XLT", "trim_code": "XLT"},
    {"mileage": 135000, "offer": 12600, "offered_at": "2026-11-25T18:23:14.7890396Z", "trim": "LARI", "trim_code": "LARI"},
    {"mileage": 34500, "offer": 17400, "offered_at": "2026-11-25T19:04:00.6895693Z", "trim": "XLT", "trim_code": "XLT"},
    {"mileage": 53500, "offer": 19400, "offered_at": "2026-11-25T19:53:29.5184512Z", "trim": "XLT", "trim_code": "XLT"}
  ],
  "trim_ranges": [
    {"trim": "XLT", "trim_code": "XLT", "low": 2400, "high": 30000},
    {"trim": "XL", "trim_code": "XL", "low": 1400, "high": 26000},
    {"trim": "Limited", "trim_code": "LIMI", "low": 8000, "high": 40400},
    {"trim": "RAPT", "trim_code": "RAPT", "low": 9400, "high": 46000}
  ],
  "median_offer_history": [{"year": 2021, "median_offer": 36600}, {"year": 2022, "median_offer": 33800}, {"year": 2023, "median_offer": 29000}, {"year": 2024, "median_offer": 24000}],
  "median_offer_change": 12600
}
```

The notes say it plainly: "Recent CarMax instant offers for this model-year, as CarMax shows them: not an appraisal of any one car." The 2021 Toyota RAV4 read `offer_range` 16,400-22,000 and headline $18,400-$23,400; the 2017 Honda Civic 6,600-12,400 and $9,400-$13,400.

### Search around a ZIP, lowest price first

```bash
curl -X POST https://api.scavio.dev/api/v1/carmax/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "Toyota", "model": "RAV4", "zip": "60601", "radius": "75", "sort": "price_asc"}'
```

Captured `data` (2026-11-26; `cars` cut to 2 of 24 and the second car's specs shortened; `features`, `highlighted_features`, `url`, `photo`, `query` and `notes` dropped):

```json
{
  "total": 62,
  "count": 24,
  "page": 1,
  "page_size": 24,
  "has_more": true,
  "sort": "price_asc",
  "zip": "60601",
  "radius": "75",
  "applied": [{"category": "make", "value": "toyota", "label": "Toyota"}, {"category": "model", "value": "rav4", "label": "RAV4"}],
  "nearest_store": {"id": "7199", "name": "Oak Lawn", "city": "Oak Lawn", "state": "IL", "zip": "60453", "distance_miles": 14},
  "cars": [
    {"stock_number": "70334270", "year": 2015, "make": "Toyota", "model": "RAV4", "trim": "XLE", "body": "4D Sport Utility", "price": 16998, "original_price": null, "price_drop": false, "currency": "USD", "mileage": 118237, "exterior_color": "White", "interior_color": "Black", "transmission": "Automatic", "drivetrain": "Front Wheel Drive", "engine_type": "Gas", "engine_size": "2.5L", "cylinders": 4, "horsepower": 176, "mpg_city": 24, "mpg_highway": 31, "store": {"id": "7128", "name": "Schaumburg", "city": "Schaumburg", "state": "IL"}, "distance_miles": 27.4, "shipping": {"fee": 0, "text": "Test drive today • Schaumburg", "type": "test-drive", "transferable": true, "arrival": "11/27 - 12/1", "min_days": 1, "max_days": 5}, "model_rating": {"average": 4.683333333333334, "count": 60}, "badge": null, "new_arrival": false, "reserved": false, "saleable": true},
    {"stock_number": "70370598", "year": 2015, "make": "Toyota", "model": "RAV4", "trim": "Limited", "body": "4D Sport Utility", "price": 17998, "original_price": null, "price_drop": false, "currency": "USD", "mileage": 119244, "drivetrain": "All Wheel Drive", "store": {"id": "7807", "name": "Kenosha", "city": "Kenosha", "state": "WI"}, "distance_miles": 56.5, "shipping": {"fee": 0, "text": "Free shipping • Nov 28-Dec 7", "type": "shipping-from", "transferable": true, "arrival": "11/28 - 12/7", "min_days": 2, "max_days": 11}, "badge": null, "new_arrival": true, "reserved": false, "saleable": true}
  ]
}
```

The two 2021 RAV4s on this search were 25,998 (LE, 52,175 miles, Merrillville IN, 29.2 miles) and 29,998 (XLE, 33,335 miles, Oak Lawn IL, `shipping.fee` `null` with "Test drive today"). With `include_facets: true` the F-150 search near 75201 returned 20 facets (VehicleType, BedLength, CabStyle, DriveTrainType, Packages such as FX4 Package, Year, Mileage and BasePrice ranges and more), each value with its `url_segment` for `filters`.

### One car with a price drop

```bash
curl -X POST https://api.scavio.dev/api/v1/carmax/listing \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"stock_number": "29242747"}'
```

Captured `data` (2026-11-26; `features`, `oem_standard_features`, `specifications`, `warranties`, `pros`, `cons` and `notes` dropped):

```json
{
  "stock_number": "29242747",
  "year": 2026,
  "make": "Ford",
  "model": "F150",
  "trim": "STX",
  "mileage": 1971,
  "price": 44998,
  "currency": "USD",
  "price_reduced": true,
  "previous_price": 45998,
  "price_drop_date": "2026-11-20T15:38:45.733Z",
  "price_drop_expires": "2026-11-27T15:38:45.733Z",
  "price_drop_text": "We lowered this price by $1,000 on November 20, 2026 to match current market trends.",
  "badge": "Price drop",
  "history": {"accident_count": 0, "owner_count": 1, "prior_uses": ["Loaner", "Personal Use"]},
  "car_life": [
    {"group": "vehicle-summary", "title": "Only 1 owner", "subtitle": "Reported by AutoCheck®"},
    {"group": "vehicle-summary", "title": "Used as loaner vehicle", "subtitle": null},
    {"group": "manufacturer-warranty", "title": "Manufacturer Warranty may apply", "subtitle": "Balance of 3 yrs / 36k miles may still apply"}
  ],
  "save_count": 20,
  "first_made_saleable_at": "2026-10-07T23:13:08.0855635Z",
  "store": {"id": "7207", "name": "Plano", "state": "TX", "remote_lot": false}
}
```

A 2017 Honda Civic EX (`70299919`) read 15,998 with `accident_count` 1, `owner_count` 1 and `reconditioning` [{"type": "Replaced Two Tires", "description": "Replaced to meet our standards."}]. No listing carries a VIN or shipping: read shipping from a search with a `zip`.

### Owner reviews of a model-year

```bash
curl -X POST https://api.scavio.dev/api/v1/carmax/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "Toyota", "model": "RAV4", "year": 2022}'
```

Captured (2026-11-26): `total_reviews` 17, `total_pages` 2, `average_rating` 4.41, `distribution` 12 five-star, 2 four, 1 three, 2 two, 0 one; `top_likes` Fuel Economy, Reliability, Ride and Handling; `top_dislikes` Cabin Noise, Ride and Handling, Braking. One review: `rating` 5, `title` "It is a very nice car.", pros [{"aspect": "Fuel Economy", "comment": "It gets very good mileage."}], cons [{"aspect": "Cabin Noise", "comment": "It is a little noisy on the road."}], `vehicle` {"mileage": 49000, "time_owned": "less than a year"}. No reviewer name or identity is returned. With `sort: "lowest_rating"` the 2020 F-150 (37 reviews, 4 pages) opened on a 1-star review titled "Not happy!!!".

### Stores, store, store inventory, photos, suggestions, makes, models

- `/stores` `{"zip": "75201"}`: 5 stores nearest first: Texas Stadium (Irving) `7115` at 7 miles, then Garland `7109` ...; each with address, phone, toll-free phone, hours, service hours and holiday hours from today (closed 2026-11-26 and 2026-12-25). `{"state": "TX"}` returned 25 (the default `limit`; pass `limit: 50` for more), `{"city": "Atlanta"}` 9 in that market (Athens, Buford, Gainesville, Lithia Springs, Norcross, Peachtree as a car buying center ...). `distance_miles` is only meaningful with `zip`.
- `/store` `{"store_id": "7115"}`: Texas Stadium (Irving), 3100 Spur 482, Irving, TX 75062, market Dallas / Ft. Worth, (972) 721-0500, Monday-Friday 10:00-21:00, Saturday 09:00-21:00, Sunday closed, service Monday-Friday 07:30-18:00, `fee_disclaimer` "Price excludes state and local taxes, title, registration, tags, and any optional products or services. Price assumes that final purchase will be made in the State of TX ...".
- `/store-inventory` `{"store_id": "7115", "make": "toyota", "zip": "75201"}`: `total` 71 Toyotas on that lot, first a 2022 RAV4 Hybrid LE at 29,998 with 29,067 miles. Without a make, the Burbank store `7126` listed 377 cars.
- `/photos` `{"stock_number": "70184244"}`: 27 photos (image, 360-exterior and 360-images; Exterior and Interior), each with a thumbnail, a 1600x1200 and a 16:9 size.
- `/suggestions` `{"query": "rav"}`: RAV4 (`rav4`), RAV4 Prime (`rav4-prime`), Ram (make, `ram`).
- `/makes` `{}`: 60 makes with slugs. `/models` `{"make": "ford"}`: 44 Ford models (Bronco, Bronco Sport, C-Max ...).
- `/search` `{"keyword": "hybrid", "body_type": "suvs", "zip": "30301", "radius": "100"}`: 175 cars; `applied` showed CarMax mapped the keyword to the Hybrid and Plug-In Hybrid engine types.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def carmax(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/carmax/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# Recent CarMax offers for a model-year (1 credit)
v = carmax("car-value", {"make": "Toyota", "model": "RAV4", "year": 2021})["data"]
print("offers", v["offer_range"], "headline", v["headline_range"]["text"], v["offers_from"][:10], v["offers_to"][:10])

# CarMax's listed prices for the same model-year near a ZIP (1 credit)
s = carmax("search", {"make": "Toyota", "model": "RAV4", "zip": "60601", "radius": "75",
                      "year_min": 2021, "year_max": 2021, "sort": "price_asc"})["data"]
for c in s["cars"]:
    print(c["stock_number"], c["trim"], c["mileage"], c["price"], c["store"]["name"], c["shipping"]["fee"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Most answers carry `notes`.

- **car** (search, store inventory) - `stock_number`, `url`, `year`, `make`, `model`, `trim`, `body`, `price`, `original_price`, `price_drop`, `currency`, `mileage`, `exterior_color`, `interior_color`, `transmission`, `drivetrain`, `engine_type`, `engine_size`, `cylinders`, `horsepower`, `mpg_city`, `mpg_highway`, `battery_range_miles`, `vehicle_size`, `vehicle_types`, `features`, `highlighted_features`, `packages`, `feature_score`, `prior_uses`, `store` {`id`, `name`, `city`, `state`}, `distance_miles`, `shipping` {`fee`, `text`, `type`, `transferable`, `arrival`, `min_days`, `max_days`}, `model_rating` {`average`, `count`}, `badge`, `new_arrival`, `coming_soon`, `reserved`, `saleable`, `made_saleable_at`, `photo`.
- **search** - `query` (the filters as read), `total`, `count`, `page`, `page_size`, `has_more`, `sort`, `zip`, `radius`, `applied[]` {`category`, `value`, `label`}, `nearest_store` {`id`, `name`, `city`, `state`, `zip`, `distance_miles`}, `cars[]`, `facets[]` (with `include_facets`: values facets {`name`, `type`, `values[]` {`value`, `url_segment`, `count`, `selected`, `children`}} and range facets {`name`, `label`, `type`, `min`, `max`, `selected_min`, `selected_max`, `buckets[]`}), `notes`.
- **store inventory** - `store_id`, `store_name`, `query`, then as search (no `radius`); `total` is the store's lot count for the filters.
- **listing** - `stock_number`, `url`, `status`, `year`, `make`, `model`, `trim`, `body`, `engine`, `transmission`, `drivetrain`, `fuel_type`, `fuel_capacity_gallons`, `mpg` {`city`, `highway`, `combined`, `equivalent`}, `battery_range_miles`, `mileage`, `exterior_color`, `interior_color`, `passenger_capacity`, `vehicle_types`, `generation`, `price`, `currency`, `price_reduced`, `previous_price`, `price_drop_date`, `price_drop_expires`, `price_drop_text`, `badge`, `history` {`accident_count`, `owner_count`, `prior_uses`}, `car_life[]` {`group`, `title`, `subtitle`}, `highlights[]`, `warranties[]` {`type`, `years`, `miles`}, `feature_score`, `feature_score_description`, `installed_packages`, `features[]` {`name`, `category`, `installed_option`}, `oem_standard_features`, `specifications[]` {`name`, `value`, `category`}, `reconditioning[]` {`type`, `description`}, `store` {`id`, `name`, `state`, `latitude`, `longitude`, `remote_lot`, `url`}, `saleable`, `available_to_transact`, `transferable`, `reserved`, `sold`, `new_arrival`, `coming_soon`, `first_made_saleable_at`, `last_made_saleable_at`, `save_count`, `model_review_summary`, `pros`, `cons`, `new_this_year`, `notes`.
- **photos** - `stock_number`, `count`, `photos[]` {`type`, `name`, `category`, `shot`, `thumbnail_url`, `url`, `url_16x9`}.
- **stores** - `zip` / `state` / `city`, `count`, `stores[]` {`id`, `name`, `url`, `address` {`line1`, `line2`, `city`, `market`, `state`, `zip`}, `phone`, `toll_free_phone`, `latitude`, `longitude`, `distance_miles`, `status`, `is_microstore`, `is_car_buying_center`, `hours[]` {`day`, `open`, `close`, `closed`}, `service_hours[]`, `holiday_hours[]` {`date`, `open`, `close`, `closed`}}.
- **store** - as a store above plus `is_open_now`, `todays_hours_label`, `alert`, `fee_disclaimer`.
- **reviews** - `make`, `model`, `year`, `sort`, `rating`, `page`, `page_size`, `total_reviews`, `total_matching`, `total_pages`, `has_more`, `average_rating`, `distribution[]` {`stars`, `count`}, `top_likes`, `top_dislikes`, `count`, `reviews[]` {`id`, `rating`, `title`, `recommends`, `pros[]` {`aspect`, `comment`}, `cons[]`, `submitted_at`, `helpful_votes`, `not_helpful_votes`, `ratings_only`, `syndicated`, `vehicle` {`year`, `make`, `model`, `mileage`, `time_owned`}}, `notes`.
- **review summary** - `make`, `model`, `year`, `count`, `average`, `rounded_average`, `top_likes`, `top_dislikes`, `distribution[]`.
- **suggestions** - `query`, `count`, `suggestions[]` {`name`, `type` (make or model), `slug`}, `notes`.
- **makes** - `count`, `makes[]` {`name`, `slug`}. **models** - `make`, `make_slug`, `count`, `models[]` {`name`, `slug`}.
- **car value** - `make`, `model`, `year`, `currency`, `offer_range` {`low`, `high`}, `headline_range` {`text`, `low`, `high`}, `aggregate` {`low`, `high`, `offer_count`}, `offers_from`, `offers_to`, `count`, `recent_offers[]` {`mileage`, `offer`, `offered_at`, `trim`, `trim_code`}, `trim_ranges[]` {`trim`, `trim_code`, `low`, `high`}, `median_offer_history[]` {`year`, `median_offer`}, `median_offer_change`, `other_years`, `url`, `notes`.

## Guardrails

- Name it "CarMax (carmax.com, the US used-car retailer)" on first mention, "CarMax" after that. Quote "263 stores in 42 states" as CarMax's own figure.
- Prices: quote each with USD, the car's year, make, model, trim and mileage, the store, the ZIP and the `fetched_at` date ("listed on carmax.com at the Plano, TX store on Nov 26, 2026"), and the store's `fee_disclaimer` when taxes or fees matter. Never compute an out-the-door price.
- Car value: always say "recent CarMax instant offers for the model-year, as CarMax shows them", give `offer_range` and `headline_range` with their labels and the offer dates, and never present them as an appraisal, an offer the user can get, a trade-in quote or what their car is worth.
- Comparisons: the same model-year (and trim where given), mileage beside every number, named retailer and date. No verdict on which car or retailer is cheaper beyond the numbers shown, and no commentary on CarMax's margins.
- History: `history` and `car_life` are CarMax's statements (CarMax cites AutoCheck); attribute them that way.
- Reviews: no reviewer is named or identified; quote review text as CarMax shows it, with its rating and date.
- Descriptive only: no commentary on CarMax's business, pricing practices or policies.
- Do not republish CarMax photos or descriptions. Write carmax.com as plain text and cite stock numbers, store ids and capture dates rather than linking CarMax pages.
- Terms: Scavio does not collect or store CarMax data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no offer or purchase flow. CarMax's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, offers, stock numbers, stores, mileage or review text. Only return what the API returned, with the `fetched_at` time.
- Not available: VIN, an appraisal or offer for one car, monthly payments and financing, taxes, a trim filter, price history beyond the last drop, reservation or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search or store inventory without `zip` ("zip is required: a 5-digit US ZIP code (CarMax prices shipping to it)."); a ZIP that is not 5 digits; `model` without `make`; `keyword` with `make` / `model` ("send keyword or make / model, not both"); more than 8 `filters`, or a value that is not a facet `url_segment`; a `radius`, `max_shipping_fee` or `sort` outside its list; `radius` on store inventory; a `_min` above its `_max`; `page * page_size` past the first 10,000 cars; `/listing` or `/photos` without exactly one of `stock_number` or `url`, or a stock number that is not 6-10 digits; `/stores` without exactly one of `zip`, `state` or `city`, or a state that is not a US state; car value or reviews without `year`; suggestions under 2 characters.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "CarMax has no car with this stock number (it may have sold).", "CarMax has no photos for this stock number.", "CarMax has no store with this id.", "CarMax found no stores for this search.", "CarMax has no owner reviews for this make, model and year (names as makes and models list them, e.g. Toyota RAV4 2022).", "CarMax has no make with this name (use makes[].slug or makes[].name).", "CarMax has no value page for this make, model and year (models lists the model slugs of a make).", "CarMax has no search for these filters (check make, model and filter segments).". Take names, slugs, stock numbers and store ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api).
- `502` means CarMax data was temporarily unavailable ("CarMax is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("CarMax is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.96.0
npm install scavio@0.97.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: value } = await scavio.carmax.carValue({ make: "Ford", model: "F-150", year: 2019 });
const { data: cars } = await scavio.carmax.search({ make: "Toyota", model: "RAV4", zip: "60601", radius: "75", sort: "price_asc" });
const { data: car } = await scavio.carmax.listing({ stock_number: "29242747" });
const { data: lot } = await scavio.carmax.storeInventory({ store_id: "7115", make: "toyota", zip: "75201" });
const { data: reviews } = await scavio.carmax.reviews({ make: "Toyota", model: "RAV4", year: 2022 });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.carmax.search(...)`, `listing`, `photos`, `stores`, `store`, `store_inventory`, `reviews`, `review_summary`, `suggestions`, `makes`, `models` and `car_value`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 12 endpoints as tools: `search_carmax`, `get_carmax_listing`, `get_carmax_photos`, `get_carmax_stores`, `get_carmax_store`, `get_carmax_store_inventory`, `get_carmax_reviews`, `get_carmax_review_summary`, `get_carmax_suggestions`, `get_carmax_makes`, `get_carmax_models` and `get_carmax_car_value`. CarMax is opt-in: add `carmax` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,carmax"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/carmax-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api), [listing](https://scavio.dev/docs/carmax-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api), [photos](https://scavio.dev/docs/carmax-photos?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api), [stores](https://scavio.dev/docs/carmax-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api), [store](https://scavio.dev/docs/carmax-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api), [store inventory](https://scavio.dev/docs/carmax-store-inventory?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api), [reviews](https://scavio.dev/docs/carmax-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api), [review summary](https://scavio.dev/docs/carmax-review-summary?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api), [suggestions](https://scavio.dev/docs/carmax-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api), [makes](https://scavio.dev/docs/carmax-makes?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api), [models](https://scavio.dev/docs/carmax-models?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api), [car value](https://scavio.dev/docs/carmax-car-value?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api). Overview: [CarMax API](https://scavio.dev/carmax-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=carmax-api).
