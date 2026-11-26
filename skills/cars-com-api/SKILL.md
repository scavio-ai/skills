---
name: cars-com-api
description: Cars.com API for Cars.com (cars.com, the US car marketplace run by Cars Commerce) - new, used and certified car listings around a US ZIP code with a radius, by make, model and trim, 24 a page with Cars.com's total, Cars.com's 11 sorts and filters by year, price, mileage, drivetrain, color, body style, Cars.com deal rating, seller type (dealer or private) and keyword, with facet counts on request; each listing's asking price, MSRP on new cars, mileage, price drop, Cars.com's deal and demand badges with Cars.com's own explanation (a used 2018 Toyota RAV4 XLE near New York read 21,170 USD with "Great Deal ... $863 below the average market price of similar vehicles in the same geographic area at $22,033" on Nov 26, 2026), sponsored placements flagged; one listing with the price breakdown (vehicle price, listed fees, all-in price), Cars.com's deal rating and good-deal range, the seller's price history, features, the vehicle history summary, the certified program terms and the dealer; a dealer's public profile, its inventory and its customer reviews; owner reviews of one model year with category ratings and recommend percent; dealers near a ZIP by make, rating and name; research pages for a make, model, model year (average listing price or starting price, MPG, NHTSA score, the good and the bad) and trims. Reviews without names, no VINs. US only, USD. 8 endpoints, 1 credit per call. No search suggestions, sold prices, VIN lookup or price history across listings.
version: 1.0.0
tags: cars-com, carscom, cars-com-api, cars-com-listings, cars-com-prices, cars-com-used-cars, cars-com-new-cars, cars-com-dealers, cars-com-dealer-reviews, cars-com-reviews, cars-com-research, cars-commerce, used-car-prices, used-car-listings, new-car-prices, car-listings-api, car-dealers, dealer-inventory, dealer-reviews, car-reviews, owner-reviews, deal-rating, good-deal-range, price-history, price-drop, certified-pre-owned, cpo, msrp, car-research, trims, automotive, us-cars, usd, price-monitoring, market-research, ai-agents, structured-data, json, mcp
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/carscom-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api
---

# Cars.com API - Used Car Listings, Deal Ratings, Dealers, Reviews

Read Cars.com (cars.com, the US car marketplace run by Cars Commerce): car listings around a ZIP code, one listing in full, a dealer's profile, inventory and customer reviews, owner reviews of a model year, dealers near a ZIP, and Cars.com's research pages for makes, models, model years and trims. All 8 endpoints return structured JSON at 1 credit per call, US only, prices in USD.

**Read-only data.** This skill reads the public pages Cars.com shows to any visitor and returns them as JSON for analysis. It uses no Cars.com account, sends no lead or message to a seller and returns no VINs, stock numbers, private-seller names or contact details, reviewer names or towns, or dealer employee names.

**The job this skill is for: used car asking prices near a ZIP, with Cars.com's own deal labels and good-deal range.** Each card carries the asking price, the mileage and the badge Cars.com gives it, with Cars.com's explanation (which often names the average market price it compared against); the listing endpoint adds the good-deal range and the seller's price history. Captured 2026-11-26 with `/search` (`zip` 10001, used Toyota RAV4, 50-mile radius: `total` 700 over 30 pages):

| Card | Mileage | Asking price | Cars.com badge (as stated) | Seller, distance |
|---|---|---|---|---|
| 2018 RAV4 XLE | 49,684 | 21,170 | Great Deal: "$863 below the average market price ... at $22,033"; High Demand | Lia Toyota of Rockland, 23 mi (sponsored) |
| 2019 RAV4 XLE Premium | 87,775 | 21,989 | Great Deal: "$505 below ... at $22,494" | Queens Auto Mall of Jamaica, 11 mi (sponsored) |
| 2018 RAV4 XLE | 48,538 | 21,799 (price drop $400) | Good Deal | BMW of Ramsey, 23 mi |
| 2024 RAV4 XLE (certified) | 29,023 | 31,287 (price drop $1.8K) | Great Deal | Glen Toyota, 16 mi |
| 2013 RAV4 LE | 153,150 | 9,580 | none | Tijara Auto Sales, 20 mi (sponsored) |

The certified 2024 XLE's `/listing` (1 credit) then read: vehicle price 30,488 plus a 799 Doc Fee = all-in 31,287 (taxes and registration not included); `deal` "At $31,287, this vehicle is a great deal. The good deal range for this vehicle is between $32,858 and $36,547."; `price_history` listed at 33,793 on 2026-09-29, five changes, 31,287 on 2026-11-25 ("$2,506 below original listed price"). Quote these as Cars.com states them; Scavio does not rate deals.

Ten limits shape every answer, so say them plainly:
- **1 credit per call.** A not-found (a listing that is no longer available, an unknown dealer, a model year without a consumer reviews page, an unknown research page) is a `404` and is charged. A refused input (`400`) and an upstream failure (`502`, `503`) are not charged.
- **Asking prices, not sale prices.** `price` is what the seller lists. `price_breakdown` on a listing shows the listed fees and the all-in price as given; taxes, registration and government charges are not included. Cars.com shows no sold prices.
- **Deal labels are Cars.com's.** `badges` (Great Deal, Good Deal, Fair Deal, High Demand, award finalist) carry Cars.com's explanation as `description`, and `deal` on a listing is Cars.com's price analysis (rating, good-deal range, market position). Report them as Cars.com's; never present them as Scavio's valuation.
- **24 a page, total stops at 10,000.** `total` is Cars.com's count; at 10,000 `total_capped` is true (the site shows "10K+") and pages stop at 417: narrow the search (ZIP and radius, year, price, trim) to see everything.
- **A ZIP is required.** `/search` and `/dealers` need a 5-digit US ZIP. A malformed ZIP is a `400`; a ZIP Cars.com cannot place comes back searched nationwide with a note ("New Kia for sale nationwide", `total` 0 for ZIP 99999): read `notes` and `search_title`.
- **Unknown values are dropped, not refused.** Cars.com ignores a model, trim or filter value it does not list; `filters_not_applied` names it and the results are without it (model "Notamodel" came back in `filters_not_applied`). Check it before trusting a filtered count; `include_facets` shows the values Cars.com lists.
- **Sponsored and partial matches are mixed in.** Paid placements stay in the results with `sponsored` true and their `placement`; after a small search's own results Cars.com adds wider-area cards marked `partial_match` true, not counted in `total` (a private-seller Civic search near Los Angeles read `total` 8 and returned 20 cards). Filter both before summarizing.
- **Reviews have no star filter.** Dealer reviews page 10-40 at a time and model reviews 10-200, sorted `most_recent`, `lowest_rated`, `most_helpful` or `highest_rated`; sort instead of filtering. Reviewer names and towns are not returned, and phone numbers, emails and VIN-like codes inside review texts and seller notes read "[removed]".
- **Slow pages happen.** Most answers took 2-15 seconds in the captures; one faceted search took 157 seconds and one dealer reviews page 105. Set a client timeout of 240 seconds and send one request at a time.
- **What is not there.** No search suggestions, no VIN lookup or VIN search, no sold prices, no price history beyond a listing's own (store your own answers with `fetched_at`), no messaging, lead forms, financing or checkout.

Cars.com publishes no public API for reading listings; Cars Commerce sells dealer-side products (inventory and marketing tools for dealers), not a listing data feed. This skill reads Cars.com's public pages with one Scavio key.

Cars.com is run by Cars Commerce (Chicago; NYSE: CARS). Quote any Cars Commerce figure only with its source and date, never as a Scavio figure.

See also: `autotrader-api` (Autotrader listings with the KBB fair price range as given), `cargurus-api` (CarGurus deal ratings and expected price), `carmax-api` (CarMax inventory and recent offers as shown), `carvana-api` (Carvana inventory by city) and `offerup-api` (local private-party asking prices by city). Same vehicle only: match year, make, model, trim and a mileage band, and show each price with its marketplace, area and date.

## When to trigger

Use this skill when the user asks to:
- Find new, used or certified cars for sale near a US ZIP code by make, model, trim, year, price or mileage, with asking prices and mileage
- Read Cars.com's deal rating for a car, its good-deal range and the average market price Cars.com states
- Read one Cars.com listing in full: price breakdown and fees, price history, features, vehicle history summary, certified program terms, the dealer
- Compare asking prices for one model across ZIP codes or against Autotrader, CarGurus, CarMax or Carvana
- List a car dealer's inventory on Cars.com, or read its profile (address, phone, hours, rating, awards)
- Read a dealer's customer reviews, or owner reviews of one model year with category ratings and recommend percent
- Find car dealers near a ZIP by make, minimum rating or name
- Read Cars.com research for a make, a model's generations and model years, a model year's average listing price or starting price, MPG, NHTSA score and trims

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls: 50 pages of 24 listings, or a search plus a few dozen listings read in full.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, model reviews answered in 2-14 seconds, dealer 3-7, listing 3-8, research 5-15, search 4-14, dealers 5-12, dealer inventory 6-10 and dealer reviews 3-6; one faceted search took 157 seconds and one dealer reviews page 105. Set a client timeout of 240 seconds and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/carscom/search` | Listings around a ZIP: asking price, MSRP (new), mileage, trim, badges, price drop, seller, sponsored flag; total, pages, filters applied and not applied, facets on request | 1 |
| `POST /api/v1/carscom/listing` | One listing: price breakdown, deal rating and good-deal range, price history, features, vehicle history summary, certified terms, seller notes, dealer | 1 |
| `POST /api/v1/carscom/dealer` | A dealer's public profile: address, phone, website, coordinates, sales and service hours, rating, review count, awards, inventory count | 1 |
| `POST /api/v1/carscom/dealer-inventory` | A dealer's vehicles for sale, 24 a page, with price, mileage and deal badge | 1 |
| `POST /api/v1/carscom/dealer-reviews` | A dealer's customer reviews, 10-40 a page, four sorts, no names | 1 |
| `POST /api/v1/carscom/model-reviews` | Owner reviews of one model year, 10-200 a page, rating, recommend percent, category ratings, no names | 1 |
| `POST /api/v1/carscom/dealers` | Dealers near a ZIP by make, minimum rating and name, sorted by rating, name or distance | 1 |
| `POST /api/v1/carscom/research` | Research for a make, a model, a model year or its trims | 1 |

## Market

US only, USD: every answer carries `market` {`country` "us", `currency` "USD"}. There is no `country` input; distances are miles.

## Listing fields

| Field | Meaning |
|---|---|
| `price` | The seller's asking price, USD |
| `msrp` | MSRP on new vehicles only (`null` on used) |
| `stock_type`, `certified` | New or Used, and whether the listing is certified pre-owned |
| `price_drop` (search) | The drop the card shows, rounded as printed (`$400`, `$1.8K`); the exact changes are in `price_history` on `/listing` |
| `badges[]` {`label`, `description`} | Cars.com's labels with Cars.com's explanation |
| `price_stack` | `fees_disclosed` or `no_fees_disclosed`: whether the seller lists its fees |
| `price_breakdown` (listing) | {`disclosed`, `vehicle_price`, `fees[]` {`label`, `amount`}, `all_in_price`}: as the seller lists it, before taxes and registration |
| `deal` (listing) | {`rating`, `summary`, `good_deal_range_low`, `good_deal_range_high`, `market_position`}: Cars.com's price analysis as stated |
| `price_history` (listing) | {`summary`, `entries[]` {`date`, `change` (listed, drop, increase), `change_amount`, `price`}} |
| `history` (listing, used) | The vehicle history summary as the page reports it, with its `source` (e.g. Experian AutoCheck): title, accidents, owners, prior use, recalls and flags |
| `seller` (search) | {`seller_type`, `name` (dealers only), `city`, `state`, `zip`, `rating`, `distance_miles`} |
| `sponsored`, `placement`, `position` | Paid placement flag, Cars.com's placement (`listing_1_priority`, `inventory_ad`, `standard` ...) and the card's position |
| `partial_match` | A wider-area card Cars.com adds after a small search's own results; not counted in `total` |

- **Private sellers:** `seller_type` private returns no name, contact or address (`dealer` null on the listing; the card keeps city and state).
- **No VINs:** no VIN, stock number or license plate is returned in any field.

## Workflow

1. **Search an area.** `/search` with `zip`, `stock_type`, `make`, `model` (and `radius`, `year_min`, `mileage_max`, `trims`). Add `include_facets: true` on the first call to see the trims and values Cars.com lists. Check `filters_not_applied` and `total_capped`.
2. **Clean the set.** Drop or flag `sponsored` and `partial_match` cards before counting; keep the same trim and a mileage band.
3. **Summarize.** Report count, low, high and median asking price per ZIP and radius, with the pages read and the `fetched_at` date.
4. **Read the deal context.** `/listing` for the cars that matter: `price_breakdown`, `deal` (good-deal range) and `price_history`, quoted as Cars.com states them.
5. **Check the dealer.** `/dealer` (profile, rating, hours), `/dealer-reviews` with `sort` `lowest_rated` to read complaints, `/dealer-inventory` for the rest of its stock.
6. **Model background.** `/research` with `make`, `model`, `year` for the model year's average listing price or starting price, MPG and trims; `/model-reviews` for owner reviews.
7. **Compare elsewhere.** The same year, make, model, trim and mileage band on `autotrader-api`, `cargurus-api`, `carmax-api` or `carvana-api`, each price with its marketplace, area and date.
8. **Price series:** there is no history across listings. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | A 5-digit US ZIP code |
| `stock_type` | string | `all` | `all` (new, used and certified), `new`, `used`, `cpo`, `new_cpo` |
| `make` | string | none | A make as Cars.com lists it (`Toyota`, `Land Rover`, `Mercedes-Benz`) or its slug (`land_rover`) |
| `model` | string | none | A model of `make`: name (`RAV4`, `F-150`, `CR-V`) or slug (`rav4`, `f_150`, `cr_v`); needs `make` |
| `radius` | integer | 50 | Miles: 10, 20, 30, 40, 50, 75, 100, 150, 200, 250, 500, 750, 1000 |
| `page` | integer | 1 | 24 listings a page, up to 417 |
| `sort` | string | `best_match` | `best_match`, `price_low`, `price_high`, `mileage_low`, `mileage_high`, `distance`, `best_deal`, `year_newest`, `year_oldest`, `listed_newest`, `listed_oldest` |
| `year_min`, `year_max` | integer | none | Model year range |
| `price_min`, `price_max` | integer | none | List price range, whole USD |
| `mileage_max` | integer | none | One of 10000, 20000, ... 100000, 150000, 200000, 250000 |
| `trims` | list or string | none | Trim names or slugs (`["XLE", "XLE Premium"]`); needs `make` and `model` |
| `drivetrain` | list or string | none | `all_wheel_drive`, `four_wheel_drive`, `front_wheel_drive`, `rear_wheel_drive` (or `awd`, `4wd`, `fwd`, `rwd`) |
| `exterior_color` | list or string | none | `black`, `white`, `gray`, `silver`, `blue`, `red` ... |
| `deal_rating` | list or string | none | `great`, `good`, `fair` |
| `body_style` | list or string | none | `suv`, `sedan`, `truck`, `coupe`, `hatchback`, `minivan`, `wagon`, `convertible` ... |
| `seller_type` | string | none | `dealership` or `private` |
| `keyword` | string | none | Cars.com's keyword filter (words in the listing, up to 100 chars) |
| `include_facets` | boolean | false | Also return Cars.com's filter options with counts |

### The other endpoints

| Endpoint | Parameters |
|---|---|
| `/listing` | `listing_id` (`items[].listing_id`, e.g. `2eb8d15b-b308-4bb3-99b3-f5b04e0ff4cd`) or `url` (a cars.com/vehicledetail/<id>/ link) |
| `/dealer` | `dealer_id` (digits, from `seller`, a listing's `dealer` or `/dealers`) or `url` (a cars.com/dealers/<id>/ link) |
| `/dealer-inventory` | `dealer_id` or `url`; `page` (24 a page, up to 500) |
| `/dealer-reviews` | `dealer_id` or `url`; `page`; `page_size` 10, 20 (default), 30 or 40; `sort` `most_recent` (default), `lowest_rated`, `most_helpful`, `highest_rated` |
| `/model-reviews` | `make`, `model`, `year` (all required); `page`; `page_size` 10, 20 (default), 30, 50, 100 or 200; `sort` as dealer reviews |
| `/dealers` | `zip` (required); `radius` 10-500 (default 30); `make`; `min_rating` 1-4 (& up); `sort` `rating` (default), `name`, `distance`; `dealer_name` (words in the name); `page` (about 20 a page) |
| `/research` | `make` (required), `model`, `year`; `level` `make`, `model`, `model_year` or `trims` (default: make without model, model without year, model_year with year) |

## Examples

### Used cars near a ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/carscom/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "10001", "stock_type": "used", "make": "Toyota", "model": "RAV4"}'
```

Captured `data` (2026-11-26; `items` cut to 2 of 24, `url`, `image` and `notes` dropped, badge text shortened with "..."):

```json
{
  "search_title": "Used Toyota RAV4 for sale near New York, NY",
  "location": {"zip": "10001", "radius_miles": 50},
  "stock_type": "used",
  "sort": "best_match",
  "page": 1,
  "page_size": 24,
  "total": 700,
  "total_capped": false,
  "total_pages": 30,
  "has_more": true,
  "filters_applied": [{"filter": "stock_type", "value": "used", "label": "Used"}, {"filter": "makes", "value": "toyota", "label": "Toyota"}, {"filter": "models", "value": "toyota-rav4", "label": "RAV4"}],
  "filters_not_applied": [],
  "count": 24,
  "items": [
    {"listing_id": "e960badf-299d-4b80-9e8a-06f5a7ac7c39", "title": "Used 2018 Toyota RAV4 XLE", "year": 2018, "make": "Toyota", "model": "RAV4", "trim": "XLE", "stock_type": "Used", "certified": false, "dealer_verified_condition": false, "price": 21170, "msrp": null, "mileage": 49684, "body_style": "SUV", "drivetrain": "All-wheel Drive", "exterior_color": "white", "fuel_type": "Gasoline", "price_stack": "fees_disclosed", "price_drop": null, "photo_count": 48, "badges": [{"label": "Great Deal", "description": "Based on the dealership's total vehicle list price, this vehicle may present a great buying opportunity at $863 below the average market price of similar vehicles in the same geographic area at $22,033. ..."}, {"label": "High Demand", "description": "This vehicle is currently in high demand given its competitive price, desirable features, and overall condition, and may have a higher chance of selling quickly."}], "delivery": null, "seller": {"seller_type": "dealership", "name": "Lia Toyota of Rockland", "city": "Blauvelt", "state": "NY", "zip": "10913", "rating": 4.9, "distance_miles": 23}, "sponsored": true, "placement": "listing_1_priority", "position": 1},
    {"listing_id": "85b17ec2-ae3a-49e0-ae99-76faba86ae55", "title": "Used 2018 Toyota RAV4 XLE", "year": 2018, "make": "Toyota", "model": "RAV4", "trim": "XLE", "stock_type": "Used", "certified": false, "dealer_verified_condition": false, "price": 21799, "msrp": null, "mileage": 48538, "body_style": "SUV", "drivetrain": "Front-wheel Drive", "exterior_color": "blue", "fuel_type": "Gasoline", "price_stack": "fees_disclosed", "price_drop": "$400", "photo_count": 29, "badges": [{"label": "Good Deal", "description": "Based on the dealership's total vehicle list price, this vehicle may present a good buying opportunity in comparison to similar vehicles in the same geographic area. ..."}], "delivery": null, "seller": {"seller_type": "dealership", "name": "BMW of Ramsey", "city": "Ramsey", "state": "NJ", "zip": "07446", "rating": 4.2, "distance_miles": 23}, "sponsored": false, "placement": "standard", "position": 4}
  ],
  "market": {"country": "us", "currency": "USD"}
}
```

On this page 6 of 24 cards were sponsored; the badges were Good Deal 17, Great Deal 5, High Demand 4 and one 2026 Award Finalist. Asking prices ran from 9,580 (2013 LE, 153,150 miles) to 40,991 (2026 LE, 3,114 miles). With `"trims": ["XLE", "XLE Premium"]`, `"sort": "mileage_low"`, `zip` 98101 and `include_facets: true`, Cars.com applied both trims (`filters_applied` toyota-rav4-xle and toyota-rav4-xle_premium), counted 109 and returned 27 facets (mileage_max, stock_type, deal_ratings, trims, drivetrain_slugs, seller_type ...), each option with its count.

### One listing with the deal range and price history

```bash
curl -X POST https://api.scavio.dev/api/v1/carscom/listing \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"listing_id": "2eb8d15b-b308-4bb3-99b3-f5b04e0ff4cd"}'
```

Captured `data` (2026-11-26; `features`, `cpo.terms`, `seller_notes`, `dealer.hours`, `badges`, `url` and `notes` dropped):

```json
{
  "listing_id": "2eb8d15b-b308-4bb3-99b3-f5b04e0ff4cd",
  "title": "Certified 2024 Toyota RAV4 XLE",
  "year": 2024,
  "make": "Toyota",
  "model": "RAV4",
  "trim": "XLE",
  "stock_type": "Used",
  "certified": true,
  "price": 31287,
  "msrp": null,
  "mileage": 29023,
  "body_style": "SUV",
  "exterior_color": "Midnight Black Metallic",
  "drivetrain": "All-wheel Drive",
  "transmission": "8-Speed Automatic w/Sequential Shift Mode",
  "mpg": "27-33.00 mpg",
  "price_stack": "fees_disclosed",
  "price_breakdown": {"disclosed": true, "vehicle_price": 30488, "fees": [{"label": "Doc Fee", "amount": 799}], "all_in_price": 31287, "note": "All-in price as the seller lists it (vehicle price plus the listed fees); taxes, registration and government charges are not included."},
  "deal": {"rating": "great deal", "summary": "At $31,287, this vehicle is a great deal. The good deal range for this vehicle is between $32,858 and $36,547.", "good_deal_range_low": 32858, "good_deal_range_high": 36547, "market_position": "This vehicle is below the current average market range."},
  "price_history": {"summary": "$2,506 below original listed price", "entries": [
    {"date": "2026-11-25", "change": "drop", "change_amount": 506, "price": 31287},
    {"date": "2026-11-19", "change": "drop", "change_amount": 1294, "price": 31793},
    {"date": "2026-11-04", "change": "drop", "change_amount": 706, "price": 33087},
    {"date": "2026-10-07", "change": "increase", "change_amount": 706, "price": 33793},
    {"date": "2026-10-02", "change": "drop", "change_amount": 706, "price": 33087},
    {"date": "2026-09-29", "change": "listed", "change_amount": null, "price": 33793}
  ]},
  "history": {"source": "Experian AutoCheck", "title": "Clean title", "accidents": "Accidents or damage reported", "owners": "1 owner", "prior_use": "Non-personal use reported", "recalls": "No open recalls reported", "clean_title": true, "no_accidents": false, "single_owner": true, "personal_use_only": false, "open_recall": false},
  "cpo": {"package": "Toyota", "program": "Toyota Certified Used Vehicles", "certified_by": "Certified by the manufacturer"},
  "seller_type": "dealership",
  "dealer": {"dealer_id": "4614", "name": "Glen Toyota", "rating": 4.5, "review_count": 4195, "address": {"street": "23-07 Maple Ave", "city": "Fair Lawn", "state": "NJ", "zip": "07410"}, "website": "https://www.glentoyota.com/"},
  "market": {"country": "us", "currency": "USD"}
}
```

The card's Great Deal badge read "$1,736 below the average market price of similar vehicles in the same geographic area at $33,529". A new 2027 Kia Telluride X-Pro SX-Prestige read `price` 60,744 against `msrp` 60,569 (a 175 Document prep fee in `price_breakdown`). A private seller's 2016 Civic EX listed at 15,000 returned `seller_type` private and `dealer` null.

### Owner reviews of a model year

```bash
curl -X POST https://api.scavio.dev/api/v1/carscom/model-reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"make": "Toyota", "model": "RAV4", "year": 2019}'
```

Captured `data` (2026-11-26; `reviews` cut to 1 of 20, `notes` dropped):

```json
{
  "vehicle": "2019 Toyota RAV4",
  "msrp_range": {"low": 25650, "high": 27050},
  "rating": 4.4,
  "total": 458,
  "recommend_percent": 82,
  "category_ratings": {"comfort": 4.6, "interior": 4.6, "performance": 4.4, "value": 4.4, "exterior": 4.7, "reliability": 4.5},
  "model_slug": "toyota-rav4-2019",
  "sort": "most_recent",
  "page": 1,
  "page_size": 20,
  "total_pages": 23,
  "has_more": true,
  "count": 20,
  "reviews": [
    {"rating": 5, "title": "I just bought this car and am happy with my experience", "date": "2025-12-30", "text": "I just bought this car and am happy with my experience purchasing it! Great place. Can't go wrong with a Toyota! I'm loving everything about it", "category_ratings": {"comfort": 5, "interior": 5, "performance": 5, "value": 5, "exterior": 5, "reliability": 5}, "recommends": true, "purchased": "used", "used_for": "Commuting", "owns_this_car": true, "helpful_votes": 1, "total_votes": 1}
  ],
  "market": {"country": "us", "currency": "USD"}
}
```

The 2020 Honda Civic read 4.8 over 173 reviews with 97% recommending; the 2021 Ford F-150 4.5 over 90 with 84%.

### Dealer, inventory, reviews, dealers, research

- `/dealer` `{"dealer_id": "97701"}`: Queens Auto Mall of Jamaica, 134-01 Atlantic Avenue, Richmond Hill, NY 11418, phone (833) 802-5886, `rating` 3.6 over 2,145 reviews, `inventory_count` 150, sales hours Monday-Saturday 10:00am-7:00pm and Sunday 11:00am-6:00pm, a service center with its own hours, `awards` 2019 and 2017 consumer dealer award, `on_cars_com_since` "July 2026".
- `/dealer-inventory` `{"dealer_id": "97701"}`: `total` 150 over 7 pages; the first a used 2021 Land Rover Range Rover P525 Westminster at 32,988 with 94,780 miles, `deal_badge` Good Deal.
- `/dealer-reviews` `{"dealer_id": "188776", "sort": "lowest_rated", "page_size": 40}`: Mercedes-Benz of Edison, `rating` 5 over 7,089 reviews, 178 pages; each review with `rating`, `title`, `date`, `text`, `category_ratings` (customer service, buying process, quality of repair, overall facilities, overall experience; `null` where the reviewer gave none), `recommends`, `shopped_for`, `made_purchase` and helpful votes, no names.
- `/dealers` `{"zip": "60601", "make": "Toyota", "min_rating": 4, "radius": 20, "sort": "distance"}`: `total` 9, Toyota of Downtown Chicago (4.4, 3 miles, 148 vehicles), Victory Toyota of Midtown (4.6, 8 miles, 244), Serra Toyota Lincolnwood (4.4, 11 miles, 165) ..., each with address and its new, used and service `phones`. `{"zip": "90012"}` read `total` 734.
- `/research` `{"make": "Toyota", "model": "RAV4", "year": 2022}`: `level` model_year, `price` 26,704 with `price_kind` avg_listing_price ("The 2022 Toyota RAV4 has an average listing price of $26,704."), `mpg` 27 city / 35 highway, `rating` 4.3 over 12, `safety_rating_nhtsa` 5, `the_good` (fuel economy, especially RAV4 Hybrid ...), `the_bad` (road and engine noise ...), `warranty` basic 3 years and powertrain 5, and every trim with its price (LE FWD 24,037, XLE 26,496, XLE Premium 29,043 ...). A new model year reads `price_kind` starting_price (2026 Mercedes-Benz C-Class: 49,650). `{"make": "Ford", "model": "F-150", "year": 2025, "level": "trims"}`: 9 trims from 37,450 to 79,005 starting MSRP (Raptor 79,005, 450 hp, 16 mpg combined). `{"make": "Toyota", "model": "RAV4"}`: generations 2026-2027 back to 1996-2000, competitors (toyota-rav4_hybrid, honda-cr_v, toyota-rav4_prime, honda-cr_v_hybrid), model years with price ranges.

### Python

```python
import statistics
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def carscom(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/carscom/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# Used RAV4 XLE asking prices around two ZIPs (1 credit per page)
for zip_code in ["10001", "60601"]:
    d = carscom("search", {"zip": zip_code, "stock_type": "used", "make": "Toyota", "model": "RAV4",
                           "trims": ["XLE"], "year_min": 2019, "year_max": 2021})["data"]
    if d["filters_not_applied"]:
        print("not applied:", d["filters_not_applied"])
    cars = [i for i in d["items"] if not i["sponsored"] and not i.get("partial_match")]
    prices = [i["price"] for i in cars if i["price"]]
    if prices:
        print(zip_code, d["total"], len(prices), min(prices), statistics.median(prices), max(prices), "USD asking")

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` and `notes`.

- **search** - `search_title`, `location` {`zip`, `radius_miles`}, `stock_type`, `sort`, `page`, `page_size`, `total`, `total_capped`, `total_pages`, `has_more`, `filters_applied[]` {`filter`, `value`, `label`}, `filters_not_applied[]`, `count`, `items[]` {`listing_id`, `url`, `title`, `year`, `make`, `model`, `trim`, `stock_type`, `certified`, `dealer_verified_condition`, `price`, `msrp`, `mileage`, `body_style`, `drivetrain`, `exterior_color`, `fuel_type`, `price_stack`, `price_drop`, `photo_count`, `image`, `badges[]`, `delivery`, `seller`, `sponsored`, `placement`, `position`, `partial_match`}, `facets[]` {`key`, `title`, `options[]` {`name`, `value`, `count`, `selected`}} (with `include_facets`).
- **listing** - `listing_id`, `url`, `title`, `year`, `make`, `model`, `trim`, `stock_type`, `certified`, `dealer_verified_condition`, `price`, `msrp`, `mileage`, `body_style`, `category`, `exterior_color`, `interior_color`, `fuel_type`, `drivetrain`, `engine`, `transmission`, `mpg`, `photo_count`, `badges[]`, `price_stack`, `price_breakdown`, `deal`, `price_history`, `features[]` {`group`, `items`}, `history`, `cpo` {`package`, `program`, `certified_by`, `terms`}, `seller_notes`, `seller_type`, `dealer` {`dealer_id`, `name`, `rating`, `review_count`, `address`, `website`, `hours[]`, `url`}.
- **dealer** - `dealer_id`, `name`, `url`, `rating`, `review_count`, `phone`, `website`, `address` {`street`, `city`, `state`, `zip`, `country`}, `latitude`, `longitude`, `description`, `opening_hours[]` {`days`, `opens`, `closes`}, `hours[]` {`day`, `sales`, `service`}, `service` {`name`, `phone`, `opening_hours`}, `inventory_count`, `awards`, `award_count`, `on_cars_com_since`, `image`.
- **dealer-inventory** - `dealer` {`dealer_id`, `name`, `url`, `rating`, `review_count`}, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`listing_id`, `url`, `year`, `make`, `model`, `trim`, `stock_type`, `certified`, `price`, `msrp`, `mileage`, `body_style`, `drivetrain`, `exterior_color`, `interior_color`, `fuel_type`, `photo_count`, `deal_badge`, `cpo_package`, `sponsored`}.
- **dealer-reviews** - `dealer`, `rating`, `total`, `sort`, `page`, `page_size`, `total_pages`, `has_more`, `count`, `reviews[]` {`rating`, `title`, `date`, `text`, `category_ratings`, `recommends`, `shopped_for`, `made_purchase`, `helpful_votes`, `total_votes`}.
- **model-reviews** - `vehicle`, `msrp_range` {`low`, `high`}, `rating`, `total`, `recommend_percent`, `category_ratings`, `model_slug`, `sort`, `page`, `page_size`, `total_pages`, `has_more`, `count`, `reviews[]` {`rating`, `title`, `date`, `text`, `category_ratings`, `recommends`, `owns_this_car`, `purchased`, `used_for`, `helpful_votes`, `total_votes`}.
- **dealers** - `location` {`zip`, `radius_miles`}, `filters` {`make`, `min_rating`, `dealer_name`}, `sort`, `page`, `total`, `has_more`, `count`, `items[]` {`dealer_id`, `name`, `url`, `rating`, `review_count`, `address`, `distance_miles`, `inventory_count`, `phones[]` {`label`, `number`}}.
- **research** - `level`, `slug`, then per level: make {`make`, `description`, `lineup[]` {`name`, `slug`, `url`, `price`}, `models[]`}; model {`name`, `make`, `description`, `generations`, `competitors`, `model_years[]` {`year`, `name`, `url`, `body_style`, `price_low`, `price_high`, `rating`, `review_count`}}; model_year {`name`, `make`, `model`, `description`, `price`, `price_kind`, `mpg`, `rating`, `review_count`, `category_ratings`, `safety_rating_nhtsa`, `notable_features`, `the_good`, `the_bad`, `warranty[]`, `trims[]`, `trim_price_kind`, `image`}; trims {`description`, `trims[]` {`name`, `trim`, `starting_msrp`, `mpg_combined`, `engine`, `drivetrain`, `transmission`, `seating_capacity`}}.

## Guardrails

- Name it "Cars.com (cars.com, the US car marketplace run by Cars Commerce)" on first mention, "Cars.com" after that.
- Prices: every Cars.com number is an asking price. Quote it with USD, the ZIP and radius, the dealer where there is one and the `fetched_at` date ("asked on Cars.com by Glen Toyota, Fair Lawn, NJ, Nov 26, 2026"). Never write "sold for", "worth" or "market value" from Cars.com data, and never drop the fees the seller lists when quoting an all-in price.
- Deal ratings: report `badges`, `deal` and the good-deal range as Cars.com's analysis, in Cars.com's words. Scavio does not rate deals; add no "underpriced", "overpriced" or "buy now" verdict of your own.
- Summaries: count, low, high and median per area, with sponsored and partial-match cards flagged or removed and the pages read. Same trim and mileage band only.
- Private sellers: never name, describe or try to identify a private seller; city and state only, as returned. Dealer business name, address, phone, website and hours are public business details and may be quoted.
- Reviews: quote ratings, titles and short excerpts without names; none are returned. Do not attempt to identify a reviewer or a dealer employee from review text.
- Vehicles: no VINs, stock numbers or license plates (none are returned); do not ask the user for one to look up.
- Descriptive only: no commentary on Cars.com's business, ranking or policies, and no verdict on a dealer beyond its ratings and reviews as shown. Quote Cars Commerce figures only with their source.
- Do not republish Cars.com photos, seller notes or review texts at length. Write cars.com as plain text and cite listing titles, dealer names, ids and capture dates rather than linking Cars.com pages.
- Terms: Scavio does not collect or store Cars.com data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and sends nothing to sellers. Cars.com's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, mileages, deal ratings, listing ids, dealers or review counts. Only return what the API returned, with the `fetched_at` time.
- Not available: search suggestions, VIN lookup, sold prices, price history across listings (store your own), messaging, lead forms, financing or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: `zip` missing or not a 5-digit US ZIP code ("zip is required: a 5-digit US ZIP code (Cars.com searches around it)", "zip 00000 is not a US ZIP code"); a make Cars.com does not list ("make must be a make Cars.com lists, e.g. Toyota, Ford, Land Rover, Mercedes-Benz"); `model` without `make` ("model needs make (the site's model keys are per make)"); `trims` without make and model; a `radius`, `mileage_max`, `sort`, `page_size` or `min_rating` outside its list ("must be one of ..."); a listing id that is not a Cars.com id ("must be a Cars.com listing id (items[].listing_id, e.g. 90e3df05-5f5e-4f4d-a474-79eb2077c99a) or a cars.com/vehicledetail/<id>/ link"); a dealer id that is not digits.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Cars.com has no listing <id> (it is no longer available).", "Cars.com has no dealer <id>.", "Cars.com has no consumer reviews page for <year> <make> <model>.", "Cars.com has no research page for <slug>.", "Cars.com has no such search.". Listings sell and disappear: take ids from a fresh search rather than an old one.
- A `200` can still need a second look: `filters_not_applied` lists a model, trim or value Cars.com ignored; a note says when a ZIP was not placed and the search ran nationwide; `total_capped` true means the count stopped at 10,000.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api).
- `502` means Cars.com data was temporarily unavailable ("Cars.com is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Cars.com is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.96.0
npm install scavio@0.97.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: cars } = await scavio.carscom.search({ zip: "10001", stock_type: "used", make: "Toyota", model: "RAV4" });
const { data: listing } = await scavio.carscom.listing({ listing_id: "2eb8d15b-b308-4bb3-99b3-f5b04e0ff4cd" });
const { data: dealer } = await scavio.carscom.dealer({ dealer_id: "4614" });
const { data: stock } = await scavio.carscom.dealerInventory({ dealer_id: "4614" });
const { data: reviews } = await scavio.carscom.dealerReviews({ dealer_id: "4614", sort: "lowest_rated" });
const { data: owners } = await scavio.carscom.modelReviews({ make: "Toyota", model: "RAV4", year: 2019 });
const { data: dealers } = await scavio.carscom.dealers({ zip: "60601", make: "Toyota", min_rating: 4 });
const { data: research } = await scavio.carscom.research({ make: "Toyota", model: "RAV4", year: 2022 });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.carscom.search(...)`, `listing`, `dealer`, `dealer_inventory`, `dealer_reviews`, `model_reviews`, `dealers` and `research`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 8 endpoints as tools: `search_carscom`, `get_carscom_listing`, `get_carscom_dealer`, `get_carscom_dealer_inventory`, `get_carscom_dealer_reviews`, `get_carscom_model_reviews`, `get_carscom_dealers` and `get_carscom_research`. Cars.com is opt-in: add `carscom` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,carscom"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/carscom-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api), [listing](https://scavio.dev/docs/carscom-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api), [dealer](https://scavio.dev/docs/carscom-dealer?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api), [dealer inventory](https://scavio.dev/docs/carscom-dealer-inventory?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api), [dealer reviews](https://scavio.dev/docs/carscom-dealer-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api), [model reviews](https://scavio.dev/docs/carscom-model-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api), [dealers](https://scavio.dev/docs/carscom-dealers?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api), [research](https://scavio.dev/docs/carscom-research?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api). Overview: [Cars.com API](https://scavio.dev/carscom-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=cars-com-api).
