# Edmunds API - Car Listings, Suggested Price, Appraisal Values, Reviews

Read Edmunds (edmunds.com, the US car research and shopping site owned by CarMax): MSRP, invoice and Edmunds Suggested Price per trim, used-car values per style and condition, car listings around a US city, one listing by a VIN you supply, owner reviews of a model year, a dealer's page with its reviews, a model year's research page, and the makes and models Edmunds lists. Every answer is what Edmunds' public pages show a visitor without an account at the moment of the call, in USD. All 8 endpoints return structured JSON at 2 credits per call.

**Read-only data.** This skill reads the public pages Edmunds shows to any visitor and returns them as JSON for analysis. It uses no Edmunds account, sends no lead, offer or appraisal request, and returns no VINs, stock numbers, listing photos, private sellers' details or reviewer names.

**The job this skill is for: Edmunds' own price figures for a model year, with the place Edmunds computed them for.** `/price` returns MSRP, invoice and Edmunds Suggested Price per trim of a new model year, and `/appraisal` returns Edmunds' used-car values per style and condition; both name the place Edmunds used. Captured 2026-11-26 (2 credits per call):

| Model year, trim (`/price`) | MSRP | Invoice | Edmunds Suggested | Place Edmunds used (`suggested_price_near`) |
|---|---|---|---|---|
| 2026 Ford F-150 XLT (most popular) | 50,850 | 47,726 | 48,579 | near Norwalk, CT 06850, sales through November 16th |
| 2025 Toyota RAV4 XLE (most popular) | 32,760 | 30,725 | 30,140 | near Paramus, NJ 07652, sales through November 16th |
| 2026 Honda Civic Sport (most popular) | 27,990 | `null` (N/A) | 26,698 | near Paramus, NJ 07652, sales through November 16th |

| 2020 Toyota RAV4 LE 4dr SUV AWD (`/appraisal`, 72,000 miles assumed, near Paramus, NJ) | Dealer retail | Private party | Trade-in | Auction |
|---|---|---|---|---|
| Clean | 23,946 | 21,638 | 19,036 | 17,986 |
| Rough | 19,465 | 17,589 | 15,474 | 14,620 |

Prices on `/price` are for the most popular style of each trim with typically-equipped options, as `table_note` says. Edmunds picks the place itself and states it, and it changed between calls on the same day (Norwalk, CT and Paramus, NJ; appraisal values near Aurora, CO and Plano, TX): quote the place with every figure. For another view of the same model-year use `truecar-api` (TrueCar's Starting MSRP and Starting Market Average per trim and dealers' advertised prices near a ZIP), `kelley-blue-book-api` or `carmax-api`, matched on year, make, model and trim.

Nine limits shape every answer, so say them plainly:
- **2 credits per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged 2; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Suggested price and values are for the place Edmunds names.** `suggested_price_near` {`city`, `state`, `zip`, `text`} and `values_near` {`city`, `state`} are the place Edmunds computed for, not one you choose; there is no location input on `/price`, `/appraisal` or `/model`. Never present them as the figure for the user's own area.
- **Values are Edmunds' estimates, not an offer.** `/appraisal` values are for the mileage Edmunds assumes (`estimated_mileage`, 72,000 on the 2020 RAV4) with no options; never present them as an appraisal of the user's car, an offer or a trade-in quote.
- **Search is by city and state, not ZIP.** Edmunds places a search by its own city pages: send `city` and `state` (a `zip` is a `400`, not charged). `location` in the answer is the city Edmunds searched around and `radius` the radius it used (default 25). An unknown city is a charged `404`.
- **Deal ratings are Edmunds'.** `deal_rating` {`local`, `national`} is Edmunds' own rating as given (`Great`, `Good`, `Fair`, `Above_market` ...) with Edmunds' `list_price_estimate`, `max_great_price`, `max_good_price`, `max_fair_price`, `savings` and `savings_percent`; local compares with listings near the search place, national nationwide.
- **The VIN is input only.** No endpoint returns a VIN, stock number or listing photo (every Edmunds photo link carries the VIN). `/listing` takes a VIN the user supplies with its make, model and year, or an edmunds.com listing link they already have; search results carry neither, so a search cannot feed `/listing`.
- **Private sellers are city and state only.** Dealer business names, addresses, phones, websites, hours and ratings are kept.
- **Slow pages.** Pages answered in 2 to 15 seconds in the captures (up to 22 in the probe). Set a client timeout of at least 240 seconds and send one request at a time.
- **What is not there.** No VIN, no ZIP search, no dealers near a ZIP and no private-seller search (Edmunds places both by the visitor's own location only), no autocomplete, no market trends, no price history beyond a listing's own `price_history`, no lead forms, financing or checkout.

Edmunds' own API is for partners and dealers only: developer.edmunds.com describes an Edmunds API partner and dealership program that needs a key, with no public signup. This skill reads Edmunds' public pages with one Scavio key.

See also: `truecar-api` (TrueCar's per-trim Starting MSRP and Starting Market Average and dealer prices near a ZIP), `kelley-blue-book-api` (KBB values), `carmax-api` (CarMax's recent instant offers and no-haggle prices), `cargurus-api`, `cars-com-api` and `autotrader-api` (listings across the US). Same model-year only: match year, make, model and trim, keep the mileage beside each price, and name the site, place and date with every number.

## When to trigger

Use this skill when the user asks to:
- Read MSRP, invoice and Edmunds Suggested Price per trim of a model year, with the place Edmunds used
- Read Edmunds' used-car values (dealer retail, private party, trade-in, auction) per style and condition for a model year
- Search Edmunds' car listings around a US city by make and model or every make, used or new, sorted by price, mileage or newest listed, filtered by year, price, mileage, trim, drivetrain, colour, body type, Edmunds deal rating or no accidents
- Read one Edmunds listing in full by a VIN the user supplies: dealer fees, price history, deal rating, history flags, the dealer's hours
- Read Edmunds owner reviews of a model year with category ratings, sorted or filtered by stars
- Read a dealer's page on Edmunds: ratings, inventory counts, hours, reviews
- Read a model year's research page: styles with base MSRP and invoice, specs, Edmunds' expert review, owner rating
- List every make Edmunds lists and one make's models with slugs

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=edmunds-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=edmunds-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 2 credits, so 50 credits cover 25 calls (for example 12 model years: one price and one appraisal each, 48 credits).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, search answered in 6-10 seconds, listing 3-10, reviews 3-4, dealer 2-8, model 3-15, price 4-5, appraisal 2-7 and makes 3-6 (the probe's slowest page took 22). Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/edmunds/search` | Used (with certified) or new listings around a US city: price, price change, MSRP, monthly payment estimate, deal rating, days on Edmunds, estimated days to sell, history summary, seller; total, paging, the city and radius Edmunds used | 2 |
| `POST /api/v1/edmunds/listing` | One listing by a VIN you supply (with make, model, year) or an edmunds.com listing link: advertised price, dealer fees, destination fee, MSRPs, price history, deal rating, history flags, options, seller comments, dealer with hours | 2 |
| `POST /api/v1/edmunds/reviews` | Owner reviews of one model year: 5 a page, 4 sorts, star filter, star counts, topics, seven category ratings (no names) | 2 |
| `POST /api/v1/edmunds/dealer` | A dealer's page: address, phones, hours, sales and service ratings, inventory counts by model, reviews 21 a page (no names) | 2 |
| `POST /api/v1/edmunds/model` | A model year's research page: MSRP range, every style with base MSRP, invoice and specs, Edmunds' expert review, owner rating, listing counts near Edmunds' own location | 2 |
| `POST /api/v1/edmunds/price` | MSRP, invoice and Edmunds Suggested Price per trim, with the place and the sales date Edmunds used | 2 |
| `POST /api/v1/edmunds/appraisal` | Used values per style and condition (dealer retail, private party, trade-in, auction), with the mileage and place Edmunds assumes | 2 |
| `POST /api/v1/edmunds/makes` | Every make Edmunds lists (69) and one make's models with slugs, latest year and submodels | 2 |

## Market

US only, USD, English. There is no `country` or `currency` input. `/makes` lists 69 makes, each flagged `new` (sold new now) and `used`.

## Prices, values and ratings

| Field | Meaning |
|---|---|
| `price` | The listing's price in USD as Edmunds displays it |
| `advertised_price` (listing) | The dealer's advertised price as Edmunds gives it; can differ from `price` by the fees `dealer_fees` lists |
| `price_change` | {`amount`, `changed_at`}: the last price change Edmunds shows (`-500` on Oct 16) |
| `price_history` (listing) | {`total_change`, `entries[]` {`price`, `date`}}: the price changes Edmunds shows for this listing |
| `msrp`, `base_msrp`, `total_msrp`, `destination_fee` (listing) | MSRP figures as Edmunds gives them |
| `dealer_fees[]` (listing) | {`name`, `amount`, `included_in_price`} as listed |
| `estimated_monthly_payment` | Edmunds' loan payment estimate as shown |
| `deal_rating` | {`local`, `national`: {`rating`, `list_price_estimate`, `max_great_price`, `max_good_price`, `max_fair_price`, `savings`, `savings_percent`}}, Edmunds' own |
| `days_on_edmunds`, `estimated_days_to_sell` | Edmunds' figures; a negative `estimated_days_to_sell` means the listing has been up longer than Edmunds estimated |
| `history` | {`owners`, `accidents`, `usage`, `clean_title`, `one_owner`, `personal_use_only`, `salvage_history`, `frame_damage`, `lemon_history`, `theft_history`, `free_history_report`, `provider`} as the history provider Edmunds names gives them (full flags on a listing) |
| `trims[]` (price) | {`trim`, `msrp`, `invoice` (`null` where Edmunds shows N/A), `edmunds_suggested`, `most_popular`} |
| `suggested_price_near`, `sales_through` (price) | The place Edmunds computed its suggested price for and the date of the sales it used |
| `styles[].conditions` (appraisal) | {`outstanding`, `clean`, `average`, `rough`: {`dealer_retail`, `private_party`, `trade_in`, `auction`}} |
| `estimated_mileage`, `values_near` (appraisal) | The mileage Edmunds assumes and the place it computed for |

- **Fees:** `price` plus the fees not included gives `advertised_price` on the captures; label any sum you make computed (a 2019 RAV4 LE near Dallas: 14,793 + 225 doc fee + 499 + 499 + 349 = 16,365 advertised, computed).
- **Seller comments:** `seller_comments` is the dealer's own text with VIN-like codes removed.

## Workflow

1. **Names.** `/makes` (`{"make": "Toyota"}`) for every make and that make's model slugs (F-150 is `f-150`, CR-V is `cr-v`).
2. **New-car figures.** `/price` with `make`, `model`, `year` (and `trim`). Note `msrp`, `invoice`, `edmunds_suggested`, `suggested_price_near.text` and `sales_through`.
3. **Used values.** `/appraisal` with `make`, `model`, `year` (and `trim`). Note each style's values per condition, `estimated_mileage` and `values_near`.
4. **Listings.** `/search` with `city`, `state`, `make`, `model` (and `radius`, `sort: "price_asc"`, `year_min` / `year_max`). Note each listing's `trim`, `style`, `mileage`, `price`, `deal_rating` and seller.
5. **One listing.** `/listing` with a VIN the user supplies plus `make`, `model` and `year` (or an edmunds.com listing link they have) for fees, price history and history flags.
6. **The model year.** `/model` for styles, base MSRP and invoice per style and Edmunds' expert review; `/reviews` for owners.
7. **A dealer.** `/dealer` with `seller.dealer_id` or `seller.url` from a search or listing.
8. **Report.** Each figure with Edmunds, the place Edmunds used (or the search city and radius), year, trim, style, mileage and the `fetched_at` date; Edmunds' labels as given; no verdict. Store each answer with its `fetched_at`: that stored set is your price record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `city` | string | required | A US city (`New York`, `Los Angeles`, `St. Louis`, small towns too) |
| `state` | string | required | The city's state, 2-letter code (`NY`) or name |
| `condition` | string | `used` | `used` (with certified pre-owned) or `new` (needs `make` and `model`) |
| `make` | string | none | A make Edmunds lists, by name or slug (`Toyota`, `land-rover`); with `model`. Leave both out to search every make (used only) |
| `model` | string | none | A model of `make` by name or slug (`RAV4`, `F-150`, `Civic`) |
| `radius` | integer | 25 | 10, 25, 50, 75, 100, 200 or 500 miles |
| `sort` | string | `best_match` | `best_match`, `price_asc`, `price_desc`, `mileage_asc`, `newest_listed` |
| `page` | integer | 1 | 21 listings a page, up to page 500 (and Edmunds' own maximum) |
| `year_min`, `year_max` | integer | none | Model year range (1990-2028) |
| `price_min`, `price_max` | integer | none | Price range, whole USD |
| `mileage_min`, `mileage_max` | integer | none | Mileage range |
| `trim` | string | none | Needs `make` and `model`: a trim as Edmunds names it (`XLE`, `LX`, `Lariat`) |
| `drivetrain` | string | none | `all_wheel_drive`, `four_wheel_drive`, `front_wheel_drive`, `rear_wheel_drive` (or `awd`, `4wd`, `4x4`, `fwd`, `rwd`) |
| `exterior_color` | string | none | `black`, `white`, `gray`, `silver`, `blue`, `red`, `brown`, `green`, `beige`, `gold`, `orange`, `yellow`, `purple` |
| `body_type` | string | none | `suv`, `sedan`, `pickup` (or `truck`), `hatchback`, `coupe`, `convertible`, `minivan`, `wagon` |
| `deal_rating` | string | none | `great`, `good` or `fair` |
| `no_accidents` | boolean | false | Only listings with no reported accidents |

### Price (`/price`), appraisal (`/appraisal`), model (`/model`), reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `make` | string | required | A make Edmunds lists (`Toyota`, `Ford`, `Mercedes-Benz`) or its slug |
| `model` | string | required | A model by name or slug (`RAV4`, `F-150`, `CR-V`) |
| `year` | integer | required (model: current) | The model year (1990-2028); on `/model` it defaults to Edmunds' current model year |
| `trim` | string | none | Price and appraisal only: one trim as Edmunds names it (`XLT`, `Sport`, `LE`); a trim the page does not list is a charged `404` that lists the page's trims |
| `page` | integer | 1 | Reviews only: 5 reviews a page |
| `sort` | string | `most_helpful` | Reviews only: `most_helpful`, `most_recent`, `highest_rated`, `lowest_rated` |
| `stars` | integer | none | Reviews only: only reviews with this many stars (1-5) |

### Listing, dealer, makes

| Endpoint | Parameters |
|---|---|
| `/listing` | `vin` (a 17-character VIN you supply; input only, never returned) with `make`, `model` and `year`, or `url` (an edmunds.com listing link you already have) |
| `/dealer` | one of `dealer_id` (`GermainVolkswagenofColumbus_1908979`, as `seller.dealer_id` gives it) or `url` (an edmunds.com dealer link, `seller.url`); `page` for reviews (21 a page, newest first) |
| `/makes` | `make` (required): its models are returned with every make Edmunds lists |

## Examples

### MSRP, invoice and Edmunds Suggested Price

```bash
curl -X POST https://api.scavio.dev/api/v1/edmunds/price \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "Ford", "model": "F-150", "year": 2026}'
```

Captured `data` (2026-11-26; `trims` cut to 4 of 8, `notes` dropped):

```json
{
  "make": "Ford",
  "model": "f-150",
  "year": 2026,
  "trim": null,
  "count": 8,
  "trims": [
    {"trim": "XL", "msrp": 46730, "invoice": 44753, "edmunds_suggested": 45262, "most_popular": false},
    {"trim": "STX", "msrp": 49985, "invoice": 47862, "edmunds_suggested": 48378, "most_popular": false},
    {"trim": "XLT", "msrp": 50850, "invoice": 47726, "edmunds_suggested": 48579, "most_popular": true},
    {"trim": "Raptor", "msrp": 81800, "invoice": 76665, "edmunds_suggested": 81022, "most_popular": false}
  ],
  "table_note": "Prices shown are for the most popular style of each trim with typically-equipped options.",
  "suggested_price_near": {"city": "Norwalk", "state": "CT", "zip": "06850", "text": "near Norwalk, CT 06850"},
  "sales_through": "November 16th",
  "market": {"country": "us", "language": "en-US", "currency": "USD"}
}
```

With `"trim": "Sport"` the 2026 Honda Civic returned one trim: MSRP 27,990, invoice `null`, Edmunds Suggested 26,698, near Paramus, NJ 07652.

### Used values per condition

```bash
curl -X POST https://api.scavio.dev/api/v1/edmunds/appraisal \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "Toyota", "model": "RAV4", "year": 2020, "trim": "LE"}'
```

Captured `data` (2026-11-26; the second style, `LE 4dr SUV (2.5L 4cyl 8A)`, and `notes` dropped):

```json
{
  "make": "Toyota",
  "model": "rav4",
  "year": 2020,
  "trim": "LE",
  "estimated_mileage": 72000,
  "values_near": {"city": "Paramus", "state": "NJ"},
  "count": 2,
  "styles": [
    {
      "style_id": "401831165",
      "style": "LE 4dr SUV AWD (2.5L 4cyl 8A)",
      "base_msrp": 27350,
      "base_invoice": 25573,
      "values_updated": "2026-11-25",
      "conditions": {
        "outstanding": {"dealer_retail": 25688, "private_party": 23212, "trade_in": 20421, "auction": 19294},
        "clean": {"dealer_retail": 23946, "private_party": 21638, "trade_in": 19036, "auction": 17986},
        "average": {"dealer_retail": 22701, "private_party": 20513, "trade_in": 18046, "auction": 17051},
        "rough": {"dealer_retail": 19465, "private_party": 17589, "trade_in": 15474, "auction": 14620}
      }
    }
  ]
}
```

The 2018 Ford F-150 returned 44 styles at 96,000 miles assumed near Plano, TX (XL 2dr Regular Cab 8 ft. LB clean: dealer retail 15,456, private party 12,771, trade-in 9,210); the 2019 Honda Civic 21 styles at 84,000 miles near Aurora, CO.

### Search around a city

```bash
curl -X POST https://api.scavio.dev/api/v1/edmunds/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"city": "Los Angeles", "state": "CA", "make": "Honda", "model": "Civic", "sort": "price_asc", "year_min": 2019, "no_accidents": true, "radius": 50}'
```

Captured `data` (2026-11-26; `items` cut to 1 of 21 with colours, engine, mpg, `features` and 8 of the 12 `history` flags dropped; `notes` dropped):

```json
{
  "condition": "used",
  "make": "Honda",
  "model": "civic",
  "location": {"city": "Los Angeles", "state": "CA", "zip": "90068"},
  "radius": 50,
  "sort": "price_asc",
  "page": 1,
  "page_size": 21,
  "total": 2469,
  "total_pages": 118,
  "has_more": true,
  "filters_applied": {"year_min": 2019, "no_accidents": true},
  "count": 21,
  "items": [
    {
      "position": 1,
      "condition": "used",
      "year": 2019,
      "make": "Honda",
      "model": "Civic",
      "trim": "LX",
      "style": "LX 4dr Sedan (2.0L 4cyl CVT)",
      "style_id": "401773861",
      "body_type": "Sedan",
      "mileage": 184790,
      "drivetrain": "front wheel drive",
      "photo_count": 5,
      "price": 9000,
      "price_change": {"amount": -500, "changed_at": "2026-10-16T23:47:41.970Z"},
      "msrp": null,
      "estimated_monthly_payment": 155.7,
      "deal_rating": {
        "local": {"rating": "Great", "list_price_estimate": 11377, "max_great_price": 9633, "max_good_price": 10979, "max_fair_price": 12230, "savings": 2377, "savings_percent": 20.9},
        "national": {"rating": "Good", "list_price_estimate": 10756, "max_great_price": 8805, "max_good_price": 10213, "max_fair_price": 11578, "savings": 1756, "savings_percent": 16.3}
      },
      "days_on_edmunds": 76,
      "estimated_days_to_sell": -52,
      "listed_at": "2026-09-11T07:00:00.000Z",
      "history": {"owners": 1, "accidents": 0, "usage": "Personal Use", "clean_title": true},
      "in_transit": false,
      "seller": {"type": "dealer", "dealer_id": "BeisanMotors_1986462", "name": "Beisan Motors", "street": "14726 Ramona Ave UNIT W5", "city": "Chino", "state": "CA", "zip": "91710", "distance_miles": 37.2, "rating": null, "review_count": null, "phone": "909-417-9699", "url": "https://www.edmunds.com/dealerships/all/california/chino/BeisanMotors_1986462/"}
    }
  ]
}
```

The same listing read Great locally and Good nationally: quote both with their labels. `{"city": "New York", "state": "NY", "make": "Toyota", "model": "RAV4"}` read 3,124 used RAV4s around New York (25 miles, 149 pages); `{"city": "Dallas", "state": "TX", "condition": "new", "make": "Ford", "model": "F-150", "page": 2, "sort": "newest_listed"}` 658 new F-150s, a 2026 XLT SuperCrew 4WD at 67,215 (MSRP 67,215) at Planet Ford Dallas Love Field, 4.7 miles; every make with `{"city": "Dallas", "state": "TX", "body_type": "truck", "deal_rating": "great", "mileage_max": 60000}` 867 pickups.

### One listing

`/listing` takes `{"vin": ..., "make": ..., "model": ..., "year": ...}` with a 17-character VIN the user supplies, or `{"url": ...}` with an edmunds.com listing link they already have; search results carry neither, so no request body is shown here. Captured `data` for a used 2019 Toyota RAV4 LE near Dallas (2026-11-26; specs, `features`, `options`, `highlighted_features`, the dealer's `hours`, `rating`, `review_count`, `distance_miles` and `notes` dropped, `seller_comments` shortened):

```json
{
  "condition": "used",
  "year": 2019,
  "make": "Toyota",
  "model": "RAV4",
  "trim": "LE",
  "style": "LE 4dr SUV (2.5L 4cyl 8A)",
  "mileage": 116871,
  "price": 14793,
  "advertised_price": 16365,
  "price_change": null,
  "msrp": null,
  "base_msrp": 25650,
  "total_msrp": 26770,
  "destination_fee": 1120,
  "dealer_fees": [
    {"name": "Doc Fee", "amount": 225, "included_in_price": false},
    {"name": "Pre-Delivery Inspection", "amount": 499, "included_in_price": false},
    {"name": "Vehicle Preparation and Reconditioning", "amount": 499, "included_in_price": false},
    {"name": "Dealer Fee", "amount": 349, "included_in_price": false}
  ],
  "estimated_monthly_payment": 255.9,
  "price_history": null,
  "deal_rating": {
    "local": {"rating": "Great", "list_price_estimate": 19965, "max_great_price": 18086, "max_good_price": 19356, "max_fair_price": 20964, "savings": 3600, "savings_percent": 18},
    "national": {"rating": "Great", "list_price_estimate": 19642, "max_great_price": 17351, "max_good_price": 18942, "max_fair_price": 20611, "savings": 3277, "savings_percent": 16.7}
  },
  "days_on_edmunds": 22,
  "estimated_days_to_sell": 2,
  "selling_slowly": false,
  "listed_at": "2026-11-06T04:14:26.000Z",
  "history": {"owners": 2, "accidents": 0, "usage": "Lease", "clean_title": true, "one_owner": false, "personal_use_only": true, "salvage_history": false, "frame_damage": false, "lemon_history": false, "theft_history": false, "free_history_report": false, "provider": "EXPERIAN"},
  "seller_comments": "2019 Toyota RAV4 LE Sport Utility 4DThis 2019 Toyota RAV4 LE is a versatile compact SUV ...",
  "in_transit": false,
  "seller": {"type": "dealer", "dealer_id": "HappyCarsandCreditCenter_1960920", "name": "Happy Cars and Credit Center", "street": "11450 E Northwest Hwy", "city": "Dallas", "state": "TX", "zip": "75218", "phone": "570-572-0263", "url": "https://www.edmunds.com/dealerships/all/texas/dallas/HappyCarsandCreditCenter_1960920/", "parent_group": null, "franchise_make": null, "websites": ["https://www.happycarsusa.com/"], "verified": true}
}
```

A listing's `distance_miles` is empty: the listing page measures from Edmunds' own location, not a place you chose. A 2022 RAV4 LE read `price` 24,128 with MSRP 26,975 and `selling_slowly` true.

### Owner reviews, one star only

```bash
curl -X POST https://api.scavio.dev/api/v1/edmunds/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "Ford", "model": "F-150", "year": 2021, "stars": 1}'
```

Captured (2026-11-26): `rating` 3.7 from 106 reviews, `star_counts` 56 five-star, 12 four, 10 three, 9 two, 19 one; `total_matching` 19 one-star reviews in 4 pages of 5; `pros` topics fuel efficiency, engine, comfort ...; `cons` reliability & manufacturing quality, technology, interior ...; `styles` lists every style with its review count. Most helpful one-star review: `title` "Electrical problems", `style` "XLT 4dr SuperCab 6.5 ft. SB (3.3L 6cyl 10A)", `created` 2021-07-21, `helpful_votes` 100, `unhelpful_votes` 12. No reviewer name is returned. The 2022 Honda Civic read 3.9 from 101 reviews; the 2025 RAV4 4.1 from 29.

### Dealer, model, makes

- `/dealer` `{"url": "https://www.edmunds.com/dealerships/all/ohio/columbus/GermainVolkswagenofColumbus_1908979/", "page": 2}`: Germain Volkswagen of Columbus, parent group Germain Automotive Partnership, franchise Volkswagen, 1495 Auto Mall Dr, Columbus, OH 43228, `sales_rating` 5 from 272 (17 recommend), `service_rating` 4 from 7, `inventory` 140 (88 new, 43 used, 9 certified; Atlas 38, Tiguan 27, Taos 15), `reviews_total` 279 in 14 pages of 21. Each review has `rating`, `type` (sales or service), `title`, `text`, `recommends_dealer`, `bought_here` and the dealer's replies. Edmunds serves its first review page twice, so our pages skip the repeat: each review appears once.
- `/model` `{"make": "Toyota", "model": "RAV4", "year": 2025}`: MSRP range 29,800-39,505, 8 styles (LE, XLE, XLE Premium, Limited; LE 4dr SUV base MSRP 29,800, base invoice 27,863), `editorial_review` "2025 Toyota RAV4 Review", rating 6.9 of 10 with its category scores and recommended trim, `consumer_rating` 4.1 from 29, `inventory` near Norwalk, CT (Edmunds' own location): 203 used, 68 certified. Without `year` the Honda Civic answered for 2027.
- `/makes` `{"make": "Toyota"}`: 69 makes (Acura `acura`, Alfa Romeo `alfa-romeo`, AM General `am-general` ...) and 31 Toyota models (4Runner `4runner`, latest year 2027, submodels 4Runner Hybrid and 4Runner SUV ...).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def edmunds(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/edmunds/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# MSRP, invoice and Edmunds Suggested Price per trim (2 credits)
p = edmunds("price", {"make": "Ford", "model": "F-150", "year": 2026})["data"]
for t in p["trims"]:
    print(t["trim"], t["msrp"], t["invoice"], t["edmunds_suggested"], p["suggested_price_near"]["text"])

# Used values per condition for an older model year (2 credits)
a = edmunds("appraisal", {"make": "Toyota", "model": "RAV4", "year": 2020, "trim": "LE"})["data"]
for s in a["styles"]:
    print(s["style"], s["conditions"]["clean"], a["estimated_mileage"], a["values_near"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }` (`response_time` in seconds on Edmunds). Everything is fetched when the request asks for it; nothing is cached. Every answer carries `market` {`country`, `language`, `currency`} and `notes`.

- **listing item** (search) - `position`, `condition` (new, used, certified), `year`, `make`, `model`, `trim`, `style`, `style_id`, `body_type`, `vehicle_style`, `mileage`, `exterior_color`, `exterior_color_generic`, `interior_color`, `interior_color_generic`, `drivetrain`, `engine` {`size_liters`, `cylinders`, `type`, `fuel`, `horsepower`}, `transmission`, `mpg` {`city`, `highway`, `combined`}, `seats`, `features`, `photo_count`, `stock_image`, `price`, `price_change`, `msrp`, `estimated_monthly_payment`, `deal_rating`, `days_on_edmunds`, `estimated_days_to_sell`, `listed_at`, `history`, `in_transit`, `seller` (dealer: {`type`, `dealer_id`, `name`, `street`, `city`, `state`, `zip`, `distance_miles`, `rating`, `review_count`, `phone`, `url`}; private: {`type`, `city`, `state`}).
- **search** - `condition`, `make`, `model`, `location` {`city`, `state`, `zip`}, `radius`, `sort`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `filters_applied`, `count`, `items[]`, `market`, `notes`.
- **listing** - the item fields above plus `options`, `advertised_price`, `base_msrp`, `total_msrp`, `destination_fee`, `dealer_fees[]`, `price_history`, `selling_slowly`, `highlighted_features[]` {`name`, `category`}, `seller_comments`, and `seller` with `parent_group`, `franchise_make`, `websites`, `hours[]` {`day`, `open`, `close`, `closed`}, `verified`.
- **reviews** - `make`, `model`, `year`, `rating`, `total_reviews`, `star_counts[]` {`stars`, `count`}, `sort`, `stars`, `total_matching`, `page`, `page_size`, `total_pages`, `has_more`, `pros`, `cons`, `styles[]` {`style_id`, `name`, `review_count`}, `count`, `reviews[]` {`id`, `rating`, `title`, `text`, `style`, `style_id`, `created`, `updated`, `helpful_votes`, `unhelpful_votes`, `ratings` {`safety`, `technology`, `performance`, `interior`, `comfort`, `reliability`, `value`}}.
- **dealer** - `dealer_id`, `name`, `parent_group`, `franchise_make`, `url`, `websites`, `address` {`street`, `city`, `state`, `zip`, `county`}, `latitude`, `longitude`, `phones`, `hours[]`, `verified`, `sales_rating` and `service_rating` {`average`, `count`, `recommended`, `not_recommended`}, `inventory` {`total`, `new`, `used`, `certified`, `models[]` {`make`, `model`, `total`, `new`, `used`, `certified`}}, `reviews_total`, `page`, `page_size`, `total_pages`, `has_more`, `count`, `reviews[]` {`id`, `rating`, `type`, `title`, `text`, `created`, `updated`, `recommends_dealer`, `bought_here`, `dealer_replies[]` {`text`, `date`}}.
- **model** - `make`, `model`, `make_slug`, `model_slug`, `year`, `msrp_range` {`low`, `high`}, `styles[]` {`style_id`, `name`, `trim`, `base_msrp`, `base_invoice`, `seats`, `body_type`, `sold_as`, `exterior_colors`, `specs` {group: [{`name`, `value`}]}}, `editorial_review` {`title`, `published`, `updated`, `rating`, `scale`, `ratings`, `verdict`, `summary`, `pros`, `cons`, `recommended_trim`}, `consumer_rating` {`average`, `count`, `star_counts`}, `inventory` {`near`, `new`, `used`, `certified`, `total`, `used_listings`}.
- **price** - `make`, `model`, `year`, `trim`, `count`, `trims[]`, `table_note`, `suggested_price_near` {`city`, `state`, `zip`, `text`}, `sales_through`.
- **appraisal** - `make`, `model`, `year`, `trim`, `estimated_mileage`, `values_near` {`city`, `state`}, `count`, `styles[]` {`style_id`, `style`, `base_msrp`, `base_invoice`, `values_updated`, `conditions`}.
- **makes** - `make`, `make_slug`, `models_count`, `models[]` {`name`, `slug`, `latest_year`, `vehicle_type`, `new`, `used`, `submodels`}, `makes_count`, `makes[]` {`name`, `slug`, `new`, `used`}.

## Guardrails

- Name it "Edmunds (edmunds.com, the US car research and shopping site)" on first mention, "Edmunds" after that.
- Suggested price and values: always give the place Edmunds names (`suggested_price_near.text`, `values_near`), `sales_through` or `values_updated`, the estimated mileage and the condition, with Edmunds' labels ("Edmunds Suggested Price near Norwalk, CT 06850"). Never present them as a price or value for the user's car or area, an offer, an appraisal of one car or a trade-in quote.
- Listing prices: quote each with USD, the year, make, model, trim, style and mileage, the seller, the search city and radius and the `fetched_at` date, and the fees `dealer_fees` lists as not included. Never compute an out-the-door price.
- Deal ratings, days to sell and payment estimates are Edmunds' as given; attribute them to Edmunds and give local and national with their labels.
- Comparisons: the same model-year and trim, mileage beside every number, named site, place and date. No verdict on which car or dealer is cheaper beyond the numbers shown, and no commentary on dealer margins.
- History: `history` is as the provider Edmunds names gives it; attribute it that way.
- VINs: never print, ask for more of, or guess a VIN; use the one the user supplied only as the `/listing` input.
- Reviews: no reviewer is named or identified. Dealer review text and titles can name dealership staff: do not repeat those names; summarise or quote the parts without them, with the rating and date.
- Descriptive only: no commentary on Edmunds' business, pricing practices or policies.
- Do not republish Edmunds photos, expert review text at length or descriptions. Write edmunds.com as plain text and cite dealer ids, style ids and capture dates rather than linking Edmunds pages.
- Terms: Scavio does not collect or store Edmunds data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no lead, offer or purchase flow. Edmunds' terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, values, ratings, dealers, mileage or review text. Only return what the API returned, with the `fetched_at` time.
- Not available: VINs or stock numbers in answers, listing photos, ZIP search, dealers near a ZIP, private-seller search or details, autocomplete, market trends, lead forms, financing or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `city` or `state`; a `zip` ("zip is not accepted: Edmunds searches around its own city pages, so pass city and state (e.g. city: "New York", state: "NY")."); a city that is not a US city name or a state that is not a US state ("state must be a US state as its 2-letter code (NY, CA, TX ...) or name."); `model` without `make` ("model needs make"); `make` without `model` ("make needs model (Edmunds' city pages are per model; leave both out to search every make, used only)"); `condition` new without make and model ("condition new needs make and model"); `trim` without make and model; a `radius`, `sort`, `drivetrain`, `exterior_color`, `body_type` or `deal_rating` outside its list; a `_min` above its `_max`; a make Edmunds does not list ("make must be a make Edmunds lists, e.g. Toyota, Ford, Honda, Mercedes-Benz (69 makes; the makes endpoint lists them)."); a missing `year`; `/listing` without `vin` or `url` ("vin (with make, model and year) or url is required"), a VIN that is not 17 letters and digits, or a link that is not an edmunds.com listing link; `/dealer` without `dealer_id` or `url` ("dealer_id or url is required"), or an id not in Edmunds' `Name_12345` form (some search results carry a bare id such as `StonebriarChevrolet`, which `/dealer` cannot open).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 2 credits: "Edmunds has no used Toyota rav4 search page for ..., NY (check the city, state and model).", "Edmunds has no listing for this VIN as a ... (sold, removed, or a different make, model or year).", "Edmunds has no consumer reviews page for the ... (check the model and year).", "Edmunds has no dealer ...", "Edmunds has no ... page (check the model and year).", "Edmunds has no MSRP page for the ... (check the model and year).", "Edmunds has no appraisal values for the ... (check the model and year).", and a trim the page does not list ("The 2026 Ford f-150 MSRP page has no trim "..."; its trims: ..." - the answer lists them). Take names, slugs, ids and trims from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=edmunds-api).
- `502` means Edmunds data was temporarily unavailable ("Edmunds is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Search is temporarily unavailable. Please try again in a moment."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.97.0
npm install scavio@0.98.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: price } = await scavio.edmunds.price({ make: "Ford", model: "F-150", year: 2026 });
const { data: values } = await scavio.edmunds.appraisal({ make: "Toyota", model: "RAV4", year: 2020, trim: "LE" });
const { data: cars } = await scavio.edmunds.search({ city: "Los Angeles", state: "CA", make: "Honda", model: "Civic", sort: "price_asc" });
const { data: reviews } = await scavio.edmunds.reviews({ make: "Ford", model: "F-150", year: 2021, stars: 1 });
const { data: dealer } = await scavio.edmunds.dealer({ dealer_id: "GermainVolkswagenofColumbus_1908979" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.edmunds.search(...)`, `listing`, `reviews`, `dealer`, `model`, `price`, `appraisal` and `makes`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 8 endpoints as tools: `search_edmunds`, `get_edmunds_listing`, `get_edmunds_reviews`, `get_edmunds_dealer`, `get_edmunds_model`, `get_edmunds_price`, `get_edmunds_appraisal` and `get_edmunds_makes`. Edmunds is opt-in: add `edmunds` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.97.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,edmunds"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/edmunds-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=edmunds-api), [listing](https://scavio.dev/docs/edmunds-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=edmunds-api), [reviews](https://scavio.dev/docs/edmunds-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=edmunds-api), [dealer](https://scavio.dev/docs/edmunds-dealer?utm_source=agent-skills&utm_medium=skill&utm_campaign=edmunds-api), [model](https://scavio.dev/docs/edmunds-model?utm_source=agent-skills&utm_medium=skill&utm_campaign=edmunds-api), [price](https://scavio.dev/docs/edmunds-price?utm_source=agent-skills&utm_medium=skill&utm_campaign=edmunds-api), [appraisal](https://scavio.dev/docs/edmunds-appraisal?utm_source=agent-skills&utm_medium=skill&utm_campaign=edmunds-api), [makes](https://scavio.dev/docs/edmunds-makes?utm_source=agent-skills&utm_medium=skill&utm_campaign=edmunds-api). Overview: [Edmunds API](https://scavio.dev/edmunds-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=edmunds-api).
