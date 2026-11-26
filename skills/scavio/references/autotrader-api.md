# Autotrader API - Used Car Listings, KBB Price Range, Dealers

Read Autotrader (autotrader.com, the US car marketplace run by Cox Automotive) around any US ZIP code: search the cars for sale, one listing in full, the dealers near a ZIP, one dealer with its inventory, and one make's models. Every answer is what Autotrader's public pages show a visitor without an account at the moment of the call, in USD. All 5 endpoints return structured JSON at 2 credits per call.

**Read-only data.** This skill reads the public pages Autotrader shows to any visitor and returns them as JSON for analysis. It uses no Autotrader account, no saved searches, no messaging and no dealer contact forms.

**The job this skill is for: asking prices next to the KBB Fair Purchase Price range.** Each Autotrader listing can carry the Kelley Blue Book Fair Purchase Price Autotrader shows for it (`kbb_fair_purchase_price` {`amount`, `low`, `high`, `delta`}) and Autotrader's own deal label (`deal_label`, Great or Good). Report both exactly as given, next to the asking price and the mileage. Captured 2026-11-26 with `/search`:

| Listing (seller, city) | Mileage | Asking (USD) | KBB Fair Purchase Price (low-high) | `delta` | `deal_label` |
|---|---|---|---|---|---|
| Used 2018 Honda Civic LX (dealer, Van Nuys, CA) | 46,077 | 18,881 | 19,440 (18,690-20,140) | 559 | Great |
| Used 2021 Honda Civic Sport (dealer, Alhambra, CA) | 45,699 | 18,777 | 20,990 (19,490-22,490) | 2,128 | Great |
| Used 2022 Toyota RAV4 SE w/ Convenience Package (dealer, Bronx, NY) | 59,009 | 28,999 | 29,089 (27,889-30,389) | -85 | Good |
| Used 2023 Volkswagen Atlas SE (private seller, Chicago, IL) | 19,120 | 28,405 | 28,601 (27,101-30,001) | 196 | Great |
| Used 2015 BMW X5 xDrive35d (private seller, Chicago, IL) | 47,393 | 21,500 | 20,140 (18,690-21,590) | -1,360 | Good |
| Used 2021 Ford F150 XL w/ XL Power Equipment Group (dealer, 23.1 miles from 75201) | 114,605 | 10,000 | 21,460 (20,160-22,860) | 11,460 | null |

The BMW asked more than the KBB amount and was still labelled Good; the F150 asked far below the range and carried no label at all. The label is Autotrader's, not a verdict: quote it as "Autotrader labels it Great", never as "a great deal". Put each row with its listing id, seller type, city, mileage and the capture date.

Ten limits shape every answer, so say them plainly:
- **2 credits per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`: a sold or removed listing, an unknown dealer, a model Autotrader does not list for the make) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **US only, USD, a ZIP is required.** `/search` and `/dealers` need `zip` (a 5-digit US ZIP code). `location.place` is the place Autotrader names for it (90012 Los Angeles, CA; 75201 Dallas, TX; 10001 New York, NY; 60601 Chicago, IL in the captures) and `location.radius_miles` the radius it applied. An unknown ZIP is a `400`, not charged. autotrader.co.uk and autotrader.ca are separate sites and are not served.
- **KBB figures and labels as given.** `kbb_fair_purchase_price` and `deal_label` are Autotrader's, as shown on the listing. `delta` is Autotrader's own figure: it does not always equal `amount` minus `price` (the RAV4 above: 29,089 against 28,999, `delta` -85), so quote it, never recompute it. New cars and some used cars carry no KBB range or label (`null`): say "no KBB range shown", not "no deal".
- **Asking prices, not sold prices.** `price` is the asking price on the listing (`null` with a `price_label` when the dealer asks you to call). `dealer_fees` are the fees the dealer lists, kept apart from the price. `price_history` is the listing's own price changes as Autotrader shows them. Autotrader publishes no sold prices.
- **Private sellers stay private.** A private seller is `{type: "private", city, state, distance_miles}` only: no name, phone or street address. VINs and stock numbers are never returned; phone numbers, emails, stock numbers and VIN-like codes inside descriptions read "[removed]". Dealer names, addresses, phones, websites and hours are the dealer's public business details.
- **Paid placements are flagged.** `spotlights` are Autotrader's paid Spotlight placements shown above the results (`sponsored: true`); `listings` are the results in page order. Count and compare `listings`, not spotlights.
- **Paging.** 25 (default) or 100 listings a page, `page` 1-100. `total` and `total_pages` are Autotrader's counts; `stats` gives the min, average and max price, mileage and model year of the whole result set, not of the page.
- **Filters as applied.** `filters_applied` lists the filters Autotrader applied (in its own codes); `filters_not_applied` lists any you sent that it did not, and the results are without them. A model spelt differently is matched to Autotrader's name and a note says so (`F-150` was read as F150).
- **Dealers are the first 50.** `/dealers` returns the dealer finder's first 50, nearest first as Autotrader orders them; it does not page, so narrow with `radius` or `make`. `/dealer` gives `rating` and `rating_count` only: dealer review text is not offered.
- **Slow pages.** Answers took 5 to 104 seconds in the captures and can take up to 4 minutes. Set a client timeout of at least 240 seconds and send one request at a time.

Autotrader publishes no public API for reading listings, dealers or prices. This skill reads Autotrader's public search, listing, dealer and make pages with one Scavio key. Other vendors offer Autotrader data tools; this skill reads Autotrader's own public pages.

See also: `cargurus-api` (CarGurus' expected price and deal rating for the same model, in the US, Canada and the UK), `cars-com-api` (Cars.com listings and dealers), `carmax-api` (CarMax's own no-haggle prices), `carvana-api` (Carvana's online prices) and `offerup-api` (local used-car asks from private sellers). Same car only: year, make, model, trim and a mileage band must match; show each price with its marketplace, seller type, city and date, and keep each site's own price analysis labelled as that site's.

## When to trigger

Use this skill when the user asks to:
- Read Autotrader asking prices for a make and model around a US ZIP code or city
- Put an asking price next to the Kelley Blue Book Fair Purchase Price range Autotrader shows, with Autotrader's deal label
- Find only the listings Autotrader labels a Good or Great price, or only private sellers, certified cars or one body style
- Read one Autotrader listing in full: specifications, features, warranties, dealer fees, price changes and history flags
- Find the car dealers near a ZIP code (optionally of one make) with address, phone, website and rating
- Read one dealer's hours, home services, inventory count by make and its listings, lowest price first
- List one make's models with model years and the price range by year

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=autotrader-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=autotrader-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 2 credits, so 50 credits cover 25 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, listings answered in 5-11 seconds, makes 6-31, dealers 11-17, dealer 10-21 and search 24-104. Allow up to 4 minutes, set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/autotrader/search` | Cars for sale around a ZIP: asking price, mileage, KBB Fair Purchase Price range, deal label, dealer fees, price history, history flags, seller; total, pages, filters applied, spotlights, price / mileage / year stats | 2 |
| `POST /api/v1/autotrader/listing` | One listing by id or link: the search fields plus description, images, features, specifications, warranties, KBB consumer rating, the dealer's address, phone, website and hours | 2 |
| `POST /api/v1/autotrader/dealers` | The first 50 dealers near a ZIP, nearest first, optionally of one make or with cars in a price or year range | 2 |
| `POST /api/v1/autotrader/dealer` | One dealer by id or link: address, phone, website, hours, home services, inventory count, makes with counts, the first page of its listings | 2 |
| `POST /api/v1/autotrader/makes` | One make's models: model years, price range label by year, MPG by year, body style, the model name to pass to search | 2 |

## Market

US only, USD: every answer carries `market` {`country` "us", `currency` "USD"}. There is no `country` or `market` input. Mileage is in miles, distances in miles from the ZIP.

## Prices, labels and sellers

| Field | Meaning |
|---|---|
| `price` | The asking price on the listing, USD. `null` when the dealer asks you to call (`price_label` says so) |
| `display_price`, `msrp` | The price as displayed, and the MSRP where Autotrader shows one (new cars) |
| `kbb_fair_purchase_price` | {`amount`, `low`, `high`, `delta`}: the Kelley Blue Book Fair Purchase Price and range Autotrader shows for the listing, and Autotrader's own `delta` (as given; negative means the listing is above it). `null` when none is shown |
| `deal_label` | Autotrader's own label (Great, Good) based on that range, as given; `null` when Autotrader shows none. `deal_basis` on `/listing` says what it is based on |
| `dealer_fees` | {`total`, `items` [{`name`, `amount`}]}: the fees the dealer lists (Doc Fee, Emissions Testing Charge ...), not included in `price` |
| `price_history` | [{`date`, `price`, `current`}]: the listing's own price changes as Autotrader shows them |
| `history_preview` | Autotrader's vehicle history flags as given (`NO_ACCIDENTS_REPORTED`, `ACCIDENTS_REPORTED`, `ONE_OWNER`, `NO_SALVAGE_TITLE`, `FREE_REPORT` ...) |
| `days_on_site`, `newly_listed`, `reduced_price` | Autotrader's days-on-site count and flags |
| `seller` | A dealer {`type` "dealer", `dealer_id`, `name`, `rating`, `rating_count`, `city`, `state`, `distance_miles`, `url`} or a private seller {`type` "private", `city`, `state`, `distance_miles`} |
| `sponsored` | `true` on Spotlight placements (`spotlights`) |

- **Ids:** `listing_id` and `dealer_id` are Autotrader's (digits); send them as strings. `trim_code` (`CIVIC|LX`) and `model_code` come from a search answer.
- **Distance:** `distance_miles` is from the ZIP you sent; on `/listing` it is `null` unless you send `zip`.
- **Dealer phones:** quote the phone with the page it came from; the dealer finder and the dealer page can show different numbers for the same dealer.

## Workflow

1. **Pick the model.** `/makes` with `make` for the models and their `search_model` names (or start from `/search` with a make and model name: Autotrader's spelling is matched and a note says so).
2. **Search per area.** `/search` with `zip`, `make`, `model` (and `radius`, `listing_type`, `year_min`, `mileage_max` ...). Note `location.place`, `location.radius_miles`, `total` and `stats`. Send the same filters and `sort` in every area you compare.
3. **Read the KBB columns.** For each listing: `price`, `mileage`, `kbb_fair_purchase_price` (amount, low, high, delta) and `deal_label`, all as given. Skip `spotlights` when you count.
4. **Open the interesting ones.** `/listing` with `listing_id` (and `zip` for the distance): features, warranties, dealer fees, price history, history flags and the dealer's address and hours.
5. **Dealers.** `/dealers` with `zip` (and `make`) for the nearest 50; `/dealer` with `dealer_id` for hours, home services, inventory by make and the first page of its listings.
6. **Report.** Each car with year, make, model, trim, mileage, asking price in USD, the KBB range and label as Autotrader gives them, seller type and city, the listing id and the capture date.
7. **Price series:** there is no history beyond each listing's own `price_history`. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | A 5-digit US ZIP code |
| `make` | string | none | A make by name or Autotrader code (Toyota, Ford, Mercedes-Benz, Land Rover, or MB, ROV; 72 makes) |
| `model` | string | none | A model as Autotrader names it (Civic, F150, RAV4, C-Class) or its `model_code`. Needs `make`. A model Autotrader does not list for the make is a charged `404` that lists the make's models |
| `trim_code` | string | none | A trim as `listings[].trim_code` gives it (`CIVIC|LX`). Needs `make` and `model` |
| `radius` | integer | Autotrader's | Miles: 10, 25, 50, 75, 100, 200, 300, 400, 500, or 0 for nationwide |
| `page` | integer | 1 | 1-100 |
| `page_size` | integer | 25 | 25 or 100 |
| `sort` | string | `relevance` | `relevance`, `price_asc`, `mileage_asc`, `year_desc` (newest model year), `distance_asc` |
| `year_min`, `year_max` | integer | none | Model year range |
| `price_min`, `price_max` | integer | none | Whole USD |
| `mileage_min`, `mileage_max` | integer | none | Miles |
| `body_style` | string | none | Code or label: CONVERT (Convertible), COUPE, HATCH (Hatchback), SEDAN, SUVCROSS (SUV / Crossover), TRUCKS (Truck), VANMV (Van / Minivan), WAGON |
| `drivetrain` | string | none | AWD4WD, FWD, RWD |
| `exterior_color`, `interior_color` | string | none | BLACK, WHITE, GRAY, SILVER, BLUE, RED ... (19 colours) |
| `seller_type` | string | none | `dealer` or `private` |
| `listing_type` | string | none | `new`, `used`, `certified` (manufacturer certified pre-owned), `third_party_certified` |
| `fuel` | string | none | GSL (Gasoline), DSL (Diesel), HYB (Hybrid), ELE (Electric), HYD (Hydrogen), PIH (Plug-in Hybrid) |
| `transmission` | string | none | AUT (Automatic) or MAN (Manual) |
| `history` | string | none | NO_ACCIDENTS, ONE_OWNER, CLEAN_TITLE, NO_FRAME_DAMAGE, FREE_REPORT |
| `deal` | string | none | `good` or `great`: only listings Autotrader labels a Good or Great price |
| `feature` | string | none | One feature, code or label (Apple CarPlay, Android Auto, Backup Camera, 3rd Row Seats, Heated Seats, Sunroof ...; 34 offered) |
| `doors` | string | none | 2, 3, 4, 5 |
| `seating` | string | none | 2-7 or 8+ |

### Listing (`/listing`), dealers (`/dealers`), dealer (`/dealer`), makes (`/makes`)

| Endpoint | Parameters |
|---|---|
| `/listing` | `listing_id` (from `listings[].listing_id`) or `url` (an autotrader.com/cars-for-sale/vehicle/<id> link); optional `zip` for `seller.distance_miles` |
| `/dealers` | `zip` (required), `make`, `radius` (10, 25, 50, 75, 100, 200, 300, 500, or 0 for any), `price_min`, `price_max`, `year_min`, `year_max` |
| `/dealer` | `dealer_id` (from `dealers[].dealer_id` or `listings[].seller.dealer_id`) or `url` (an autotrader.com/car-dealers/<city-st>/<id>/<name> link) |
| `/makes` | `make` (required): name or Autotrader code |

## Examples

### Search a model around a ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/autotrader/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "90012", "make": "Honda", "model": "Civic"}'
```

Captured `data` (2026-11-26; `listings` cut to 1 of 25, `spotlights` (3) and `notes` dropped; `warranties` and `image` dropped from the listing):

```json
{
  "search": {"zip": "90012", "make": "Honda", "model": "Civic"},
  "location": {"zip": "90012", "place": "Los Angeles, CA", "radius_miles": 25},
  "filters_applied": {"make": "HONDA", "model": "CIVIC"},
  "filters_not_applied": [],
  "sort": "relevance",
  "page": 1,
  "page_size": 25,
  "total": 1884,
  "total_pages": 76,
  "has_more": true,
  "count": 25,
  "listings": [
    {"listing_id": "796810802", "url": "https://www.autotrader.com/cars-for-sale/vehicle/796810802", "title": "Used 2018 Honda Civic LX", "year": 2018, "make": "Honda", "make_code": "HONDA", "model": "Civic", "model_code": "CIVIC", "trim": "LX", "trim_code": "CIVIC|LX", "listing_type": "used", "mileage": 46077, "exterior_color": "Rallye Red", "interior_color": "Black/Ivory", "body_style": "Coupe", "drivetrain": "FWD", "engine": "4-Cylinder", "fuel": "Gasoline", "transmission": "Continuously Variable Automatic", "mpg_city": 30, "mpg_highway": 39, "doors": 2, "days_on_site": 5, "newly_listed": true, "reduced_price": false, "price": 18881, "display_price": 18881, "msrp": null, "price_label": null, "deal_label": "Great", "kbb_fair_purchase_price": {"amount": 19440, "low": 18690, "high": 20140, "delta": 559}, "dealer_fees": {"total": 181, "items": [{"name": "Doc Fee", "amount": 85}, {"name": "E - Filling Fee", "amount": 37}, {"name": "Emissions Testing Charge", "amount": 59}]}, "price_history": [], "history_preview": ["NO_SALVAGE_TITLE", "NO_FRAME_DAMAGE", "NO_FLOOD_WATER_DAMAGE", "ACCIDENTS_REPORTED", "NO_ONE_OWNER", "FREE_REPORT"], "sponsored": false, "seller": {"type": "dealer", "dealer_id": "72925383", "name": "Keyes Toyota", "rating": 4.6, "rating_count": 9097, "city": "Van Nuys", "state": "CA", "distance_miles": 14.5, "url": "https://www.autotrader.com/car-dealers/van-nuys-ca/72925383/keyes-toyota"}}
  ],
  "stats": {"price": {"min": 2800, "avg": 28820, "max": 72557}, "mileage": {"min": 0, "avg": 18456, "max": 263613}, "year": {"min": 1999, "avg": 2025, "max": 2027}},
  "market": {"country": "us", "currency": "USD"}
}
```

Other listings on the page carried their own `price_history`, e.g. 19,962 on Nov 14, 19,762 on Nov 18, 18,962 on Nov 19 and 18,862 now (`current` true).

### Private sellers, cheapest first, other filters

- `/search` `{"zip": "60601", "seller_type": "private", "body_style": "SUVCROSS", "drivetrain": "AWD4WD", "radius": 100}`: Chicago, IL, 100 miles, `total` 360 over 15 pages, `filters_applied` {`drivetrain` AWD4WD, `body_style` SUVCROSS, `seller_type` private}; first a Used 2023 Volkswagen Atlas SE, 19,120 miles, 28,405 against a KBB Fair Purchase Price of 28,601 (27,101-30,001), Great, `seller` {`type` private, `city` Chicago, `state` IL, `distance_miles` 8.9}.
- `/search` `{"zip": "75201", "make": "Ford", "model": "F-150", "year_min": 2018, "price_max": 40000, "sort": "price_asc", "radius": 50}`: Dallas, TX, 50 miles, `total` 1194, a note that Autotrader names the model "F150"; first a Used 2018 Ford F150 XLT, 224,302 miles, from a private seller in Keller, TX at 7,000 against 6,860 (5,860-7,810), `delta` -140, Good. `stats.price` read 7,000 to 39,999 and `stats.year` 2018 to 2026.
- `/search` `{"zip": "10001", "make": "Toyota", "model": "RAV4", "listing_type": "used", "radius": 50, "page": 2}`: New York, NY, `total` 882, page 2 of 36.

### One listing in full

```bash
curl -X POST https://api.scavio.dev/api/v1/autotrader/listing \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"listing_id": "795241382", "zip": "75201"}'
```

Captured (2026-11-26; abridged): Used 2016 Ford F150 XLT, 76,887 miles, `price` 22,175, `deal_label` Great, `kbb_fair_purchase_price` {`amount` 23600, `low` 22600, `high` 24650, `delta` 1425}, `dealer_fees` {`total` 225, `items` [Dealer Doc Fee 225]}, `kbb_consumer_rating` 4.4 from 317 reviews (Kelley Blue Book owner ratings for the model), `seller` Mesquite KIA (Mesquite, TX, 10.5 miles), and `dealer` {`address` 1919 Oates Drive, Mesquite, TX 75150, `hours` Monday-Saturday 8:30 AM-8:00 PM, Sunday Closed, `is_open` false}. `features`, `ranked_features`, `specifications`, `warranties` and `images` follow. A private seller's listing (`796854799`, the Atlas above) returns `dealer` `null` and `seller` city and state only.

### Dealers near a ZIP, one dealer

- `/dealers` `{"zip": "75201", "make": "Ford"}`: Dallas, TX, 50 miles, 50 dealers; first Westway Ford (`dealer_id` 87788, Irving, TX, 10 miles, rating 4.6 from 5,621), then Planet Ford 635 (Garland) and Town East Ford (Mesquite), each with address, phone and website.
- `/dealers` `{"zip": "60601", "make": "Toyota", "radius": 50}`: 32 dealers, first Toyota of Downtown Chicago at 2 miles.
- `/dealer` `{"dealer_id": "87788"}`: Westway Ford, 801 West Airport Freeway, Irving, TX 75062, hours Monday-Saturday 9:30 AM-7:00 PM, `home_services` {`buy_online` false, `test_drive` true, `vehicle_delivery` true, `virtual_tour` true}, `inventory_count` 498, `makes` Ford 461, Chevrolet 4, Jeep 4 ... , `inventory_sort` price_asc and 25 listings.

### One make's models

- `/makes` `{"make": "Toyota"}`: 46 models, `popular_models` COROL, RAV4, HIGHLANDER, 4RUN, CAMRY ...; 4Runner {`years` [2025, 2026], `price_by_year` {"2025": "$41,270 - $67,400", "2026": "$42,270 - $68,600"}, `search_model` "4Runner"}. These price labels are Autotrader's new-model price ranges, not used prices.
- `/makes` `{"make": "Ford"}`: 64 models; F150 `price_by_year` {"2025": "$37,450 - $79,005", "2026": "$37,290 - $79,005", "2027": "$38,110 - $75,325"}.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def autotrader(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/autotrader/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# The same model in two metros, asking price next to the KBB range (2 credits each)
for zip_code in ["90012", "75201"]:
    d = autotrader("search", {"zip": zip_code, "make": "Honda", "model": "Civic", "listing_type": "used"})["data"]
    print(d["location"]["place"], d["location"]["radius_miles"], d["total"])
    for car in d["listings"]:  # spotlights are paid placements: left out here
        kbb = car["kbb_fair_purchase_price"] or {}
        print(car["listing_id"], car["title"], car["mileage"], car["price"],
              kbb.get("amount"), kbb.get("low"), kbb.get("high"), car["deal_label"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` and `notes`.

- **listing tile** (search `listings[]` and `spotlights[]`, dealer `inventory[]`) - `listing_id`, `url`, `title`, `year`, `make`, `make_code`, `model`, `model_code`, `trim`, `trim_code`, `listing_type`, `mileage`, `exterior_color`, `interior_color`, `body_style`, `drivetrain`, `engine`, `fuel`, `transmission`, `mpg_city`, `mpg_highway`, `doors`, `days_on_site`, `newly_listed`, `reduced_price`, `price`, `display_price`, `msrp`, `price_label`, `deal_label`, `kbb_fair_purchase_price` {`amount`, `low`, `high`, `delta`}, `dealer_fees` {`total`, `items[]`}, `price_history[]` {`date`, `price`, `current`}, `history_preview[]`, `warranties`, `image`, `sponsored`, `seller`.
- **search** - `search` {`zip`, `make`, `model`}, `location` {`zip`, `place`, `radius_miles`}, `filters_applied`, `filters_not_applied`, `sort`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `listings[]`, `spotlights[]`, `stats` {`price`, `mileage`, `year`: {`min`, `avg`, `max`}}.
- **listing** - the tile plus `description`, `images`, `features` {group: [...]}, `ranked_features`, `specifications` {name: value}, `warranties[]` {`group`, `type`, `label`, `details`, `years`, `miles`, `unlimited_miles`, `remaining_years`, `remaining_miles`}, `kbb_consumer_rating`, `kbb_consumer_review_count`, `deal_basis`, `dealer` {`dealer_id`, `name`, `rating`, `rating_count`, `address` {`street`, `street2`, `city`, `state`, `zip`}, `phone`, `website`, `hours[]` {`day`, `open`, `close`}, `home_services`, `is_open`, `url`} (`null` for a private seller), `zip`.
- **dealers** - `search` {`zip`, `make`}, `location` {`zip`, `place`, `radius_miles`}, `count`, `dealers[]` {`dealer_id`, `name`, `franchise_name`, `make`, `rating`, `rating_count`, `distance_miles`, `address`, `phone`, `website`, `url`}.
- **dealer** - `dealer_id`, `name`, `rating`, `rating_count`, `address`, `phone`, `website`, `hours[]`, `home_services` {`buy_online`, `test_drive`, `vehicle_delivery`, `virtual_tour`}, `is_open`, `url`, `inventory_count`, `makes[]` {`make`, `make_code`, `count`}, `inventory_sort`, `inventory[]` (tiles).
- **makes** - `make` {`code`, `name`}, `years`, `popular_models`, `count`, `models[]` {`code`, `name`, `years`, `price_by_year`, `mpg_by_year` {year: {`city`, `highway`}}, `body_style`, `image`, `search_model`}.

## Guardrails

- Name it "Autotrader (autotrader.com, the US car marketplace run by Cox Automotive)" on first mention, "Autotrader" after that.
- Prices: quote each with USD, year, make, model, trim, mileage, seller type and city, the listing id and the `fetched_at` date ("listed on autotrader.com on Nov 26, 2026"). These are asking prices, never sold prices.
- KBB figures: quote `kbb_fair_purchase_price` and `deal_label` exactly as Autotrader gives them and say they are Autotrader's ("Autotrader shows a KBB Fair Purchase Price of 19,440, range 18,690-20,140, and labels it Great"). Never recompute `delta`, never invent a label where it is `null`, and give no buy or negotiate advice beyond the numbers shown.
- Comparisons: the same year, make, model, trim and a similar mileage band, labelled with each marketplace and date. Keep each site's price analysis (Autotrader's KBB range, CarGurus' expected price) labelled as that site's.
- Private sellers: city and state only. Never ask for, guess or add a private seller's name or contact. Dealer name, address, phone, website and hours are public business details.
- No VINs: none are returned; never add or guess one.
- Descriptive only: no commentary on Autotrader's business, its dealers or its pricing practices.
- Do not republish Autotrader photos or listing descriptions. Write autotrader.com as plain text and cite listing ids, dealer names and capture dates rather than linking Autotrader pages.
- Terms: Scavio does not collect or store Autotrader data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no contact forms. Autotrader's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, KBB figures, labels, mileages, listing ids or dealers. Only return what the API returned, with the `fetched_at` time.
- Not available: VINs, stock numbers, private sellers' names or contact details, dealer review text, sold prices, price history beyond each listing's own `price_history`, autotrader.co.uk or autotrader.ca, more than 100 pages of a search.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: no `zip` ("zip is required (a 5-digit US ZIP code)."), a ZIP that is not a US ZIP code, a make Autotrader does not list ("make must be a make Autotrader lists, e.g. Toyota, Ford, Honda, Mercedes-Benz (72 makes)."), `model` without `make`, `trim_code` without `model`, a `radius`, `page_size` or `sort` outside the lists above, `year_min` above `year_max` (or price / mileage), a filter code not offered, `/listing` or `/dealer` without an id or link.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Autotrader has no listing <id> (sold, removed or never listed).", "Autotrader has no dealer <id>.", "Autotrader lists no model "<model>" for <make>. Models Autotrader lists for <make> near this ZIP: ...". Take ids and model names from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=autotrader-api).
- `502` means Autotrader data was temporarily unavailable ("Autotrader is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy: wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.96.0
npm install scavio@0.97.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: civics } = await scavio.autotrader.search({ zip: "90012", make: "Honda", model: "Civic" });
const { data: listing } = await scavio.autotrader.listing({ listing_id: "795241382", zip: "75201" });
const { data: dealers } = await scavio.autotrader.dealers({ zip: "75201", make: "Ford" });
const { data: dealer } = await scavio.autotrader.dealer({ dealer_id: "87788" });
const { data: toyota } = await scavio.autotrader.makes({ make: "Toyota" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.autotrader.search(...)`, `listing`, `dealers`, `dealer` and `makes`, with the same parameter names as keyword arguments. Set the client timeout to 240 seconds.

## MCP

The Scavio MCP server exposes all 5 endpoints as tools: `search_autotrader`, `get_autotrader_listing`, `get_autotrader_dealers`, `get_autotrader_dealer` and `get_autotrader_makes`. Autotrader is opt-in: add `autotrader` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,autotrader"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/autotrader-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=autotrader-api), [listing](https://scavio.dev/docs/autotrader-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=autotrader-api), [dealers](https://scavio.dev/docs/autotrader-dealers?utm_source=agent-skills&utm_medium=skill&utm_campaign=autotrader-api), [dealer](https://scavio.dev/docs/autotrader-dealer?utm_source=agent-skills&utm_medium=skill&utm_campaign=autotrader-api) and [makes](https://scavio.dev/docs/autotrader-makes?utm_source=agent-skills&utm_medium=skill&utm_campaign=autotrader-api). Platform overview: [Autotrader API](https://scavio.dev/autotrader-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=autotrader-api).
