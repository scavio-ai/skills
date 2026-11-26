# Bring a Trailer API - BaT Auction Results, Sold Prices, Live Bids

Read Bring a Trailer (bringatrailer.com, the online collector-car auction site owned by Hearst): the completed auction results of any query, one model, a model family or a make with sale prices and sell-through in one call, one listing live or ended with its full bid history and comments, every live auction, the make, model and country pages, and the search suggestions. Every answer is what Bring a Trailer's public pages show a visitor without an account at the moment of the call, with each lot's amount in its own currency. All 8 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Bring a Trailer shows to any visitor and returns them as JSON for analysis. It uses no Bring a Trailer account, places no bid, sets no watchlist and submits no listing.

**The job this skill is for: what a collector car sells for on Bring a Trailer.** The sale prices and reserve-not-met high bids of one model (or a whole model family, or a make) over its history in one call, the same vehicle's earlier results, and what is live now. Captured 2026-11-26 with `/price-history` (1 credit each):

| Filter | Completed | Sold | Reserve not met | Sell-through | USD sold median | USD sold max | Since |
|---|---|---|---|---|---|---|---|
| BMW E30 M3 (`model_id` 1833018) | 490 | 385 | 105 | 0.786 | 56,000 | 256,556 | 2014-07-30 |
| Toyota Land Cruiser FJ40 (`model_id` 1833055) | 1,374 | 927 | 447 | 0.675 | 32,000 | 270,000 | 2014-11-12 |
| Porsche 911 family (118 ids from `/model`), `recency` 1y | 3,726 | 2,951 | 775 | 0.792 | 80,732 | 3,050,000 | 2025-11-26 |
| Porsche (`make`), `recency` 30d | 673 | 486 | 187 | 0.722 | 48,000 | 1,125,000 | 2026-10-27 |

A model page's results include parts and wheels sold for that model: the E30 M3 series carried "Rebuilt BMW S14 Engine and Getrag 5-Speed Gearbox" (sold 19,000), a set of Alpina wheels (sold 3,951) and "No Reserve: BMW M Technic 1 Steering Wheel" (sold 300, the sold minimum). Keeping only titles with a model year left 337 USD sales with a median of 59,501 (computed from the captured `results`). Then read one car: `/listing` for `1988-bmw-m3-272-2` read sold for 80,000 USD on 2026-11-19 after 29 bids, 11,598 views and 1,220 watchers, and its `bat_history` listed the same car's two earlier Bring a Trailer sales, 82,500 USD (2024-06-14) and 87,333 USD (2025-12-31).

Ten limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint costs 1 credit; `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Amounts are in each lot's own currency.** USD for US lots, EUR, GBP and others for lots elsewhere, as Bring a Trailer shows them: read `currency` on every lot. The Germany location results carried both EUR lots and a USD lot; `stats_by_currency` keeps each currency apart (a key `unknown` can appear). Never add or average across currencies.
- **Sale price, high bid, or nothing.** `status` `sold` carries the sale price from Bring a Trailer's "Sold for" result; `reserve_not_met` carries the high bid ("Bid to"); `withdrawn` and older `ended` lots carry no amount. On `/listing`, `sold_price` is the "Sold for" figure (it can differ from the last bid) and `high_bid` the "Bid to" figure. Never call a reserve-not-met high bid a sale.
- **Before the buyer's fee.** Bring a Trailer adds a buyer's fee to the winning bid; every amount here is the bid or sale figure as the site shows it, before that fee. Never compute the fee.
- **10,000 results per query.** `/results` pages through the first 10,000 results of a query (`reachable_pages`; `page` x `page_size` past 10,000 is a `400`). With no keywords the archive read `total` 276,462 and `reachable_pages` 166 at 60 a page. Narrow with `recency`, years, a make or a model to reach older lots. `/price-history` returns at most 10,000 results (the most recent) and says so with `capped`.
- **Model families need their ids.** A family page such as Porsche 911 has no results of its own id: read `/model` for `porsche/911` and pass its `filter_ids` (118 ids, up to 200 per call) as `model_id`. One single model id (from `/suggestions` or `/make` `models[].id`) works directly.
- **Counts live on the listing.** Results carry no view, watcher or comment counts; `/listing` has `views`, `watchers`, `bid_count` and `comment_count`.
- **No people.** No usernames, member profile links, chassis numbers or VINs, or seller ZIP codes are returned. Bids are `amount`, `currency` and `time` only; comments are `time`, `text`, `is_seller` and `likes`; names in comment text read `[member]`, mentions read `@member` or `@seller`, and VIN-shaped codes in text read `[redacted]`.
- **Live is one large page.** `/live` reads every live auction at once (1,073 lots on 2026-11-26), so a call can take 20 seconds to 3 minutes; allow at least 200 seconds. Filters and sort are applied by Scavio over that list; `current_bid` is `null` before any bid (30 of 1,073), and a bid in the final two minutes extends `ends_at`.
- **No history beyond the site.** `/price-history` is the site's completed results; nothing is cached or kept by Scavio. Store each answer with its `fetched_at` for your own record of live bids.

Bring a Trailer publishes no public API, developer programme or data feed for its auctions; this skill reads the public results, listing, live-auction and directory pages with one Scavio key. Other vendors offer Bring a Trailer data tools; this skill reads Bring a Trailer's own public pages.

Bring a Trailer Media, LLC is "part of the Hearst affiliated network of media companies" (Bring a Trailer terms page); Hearst Autos announced its acquisition on June 25, 2020. Bring a Trailer's About page states "over 1,000 listings per week". Quote these with their source, never from the samples.

See also: `nellis-auction-api` (liquidation auction bids and closing prices), `ebay-product-data` (eBay listings and sold items), and for dealer and marketplace asking prices of the same model `cars-com-api` (Cars.com), `autotrader-api` (Autotrader with the KBB fair price range), `cargurus-api` (CarGurus deal ratings and expected price) and `carmax-api` (CarMax). An auction sale price and a dealer asking price are different things: show each with its source, date and currency, never as one figure.

## When to trigger

Use this skill when the user asks to:
- Read what a model, a model family or a make has sold for on Bring a Trailer, with sold count, reserve-not-met count, sell-through and median per currency
- Search Bring a Trailer's completed auctions by keyword, sorted by recently closed, popular, highest bid or oldest, filtered by sold or reserve not met, recency, model years, max bid, category, origin, era, no reserve or Premium
- Read one Bring a Trailer listing by slug or link: the sale price or high bid, bid count, views, watchers, location, seller type, details, the full bid history and the comments
- See the same vehicle's earlier Bring a Trailer results
- List the live Bring a Trailer auctions by make, keyword, country, ending within N hours, no reserve or Premium, sorted by ending time or current bid
- Read a make's model list, a model page or a country's lots with their live auctions and latest results
- Find the page id for a make, model or place to filter on

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=bring-a-trailer-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=bring-a-trailer-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (a whole model's price history is one call).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, results answered in 1-4 seconds, suggestions 1-3, model 1-5, make and location 2-4, listing 2-7, price history 3-15 (a 118-id family) and live 1-12; live can take up to 3 minutes and a make page up to a minute. Set a client timeout of at least 240 seconds and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/bringatrailer/results` | Completed auctions for keywords (or none) with sorts and filters: sale price or high bid, currency, status, end date, flags; total, pages, reachable pages | 1 |
| `POST /api/v1/bringatrailer/price-history` | Every completed result of one model, a list of model ids or a make in one call: counts, sell-through, stats per currency, each result with date and amount | 1 |
| `POST /api/v1/bringatrailer/listing` | One auction live or ended: sale price, high bid or current bid, bid count, views, watchers, location, seller type, details, photos, earlier BaT results, full bid history, paged comments | 1 |
| `POST /api/v1/bringatrailer/live` | Every live auction filtered by keyword, make, country, ending within N hours, no reserve, Premium; sorted by ending time or current bid | 1 |
| `POST /api/v1/bringatrailer/make` | One make page: its models with ids and paths, live lots, completed total, latest results | 1 |
| `POST /api/v1/bringatrailer/model` | One model or model-family page: `filter_ids`, sub-models, live lots, completed total, latest results | 1 |
| `POST /api/v1/bringatrailer/location` | One country's page: `location_id`, live lots, completed total, latest results | 1 |
| `POST /api/v1/bringatrailer/suggestions` | Search-box suggestions for a partial make, model or place, with the page id the filters take | 1 |

## Market

One site, in English, with no country or language input. Lots are located worldwide and each one is shown in its own currency: on 2026-11-26 the 1,073 live lots were 1,063 in USD, 7 in EUR and 3 in GBP (1,041 located in the US, 19 in Canada). `/location` filters by where the lot is, not by a storefront.

## Amounts, status and ids

| Field | Meaning |
|---|---|
| `amount` (results, recent_results, price-history) | The sale price of a sold lot ("Sold for") or the high bid of a lot that ended under its reserve ("Bid to"); `null` for withdrawn and older ended lots |
| `status` | `sold`, `reserve_not_met`, `withdrawn` or `ended` on completed lots; `live` too on `/listing` |
| `sold_price`, `high_bid`, `current_bid` (listing) | The "Sold for" figure; the "Bid to" figure under the reserve; the live bid (`null` before any bid) |
| `currency` | The lot's own currency as shown (USD, EUR, GBP ...) |
| `ended_at`, `ends_at` | When a completed lot ended; when a live lot is scheduled to end (a late bid extends it) |
| `no_reserve`, `premium`, `bat_alumni` | Bring a Trailer's No Reserve and Premium flags; `bat_alumni` marks a vehicle sold on Bring a Trailer before |
| `year` | The model year in the lot title; `null` when the title has none (parts, wheels, memorabilia) |
| `seller_type`, `seller_type_label` (listing) | `private_party` or `dealer`, and the label as shown |
| `bat_history` (listing) | The same vehicle's earlier Bring a Trailer results: `result`, `amount`, `currency`, `date` |
| `sell_through_rate` (price-history) | `sold_count` divided by `total`, as returned |
| `stats_by_currency` (price-history) | Per currency: `sold` and `reserve_not_met` each with `count`, `min`, `max`, `median`, `average` (or `null` when none) |

- **Ids.** `slug` (`1988-bmw-m3-272-2`) is the listing id for `/listing`. `model_id` and `location_id` are Bring a Trailer page ids from `/suggestions`, `/make` (`models[].id`) or `/model` (`filter_ids`), e.g. `1833018` BMW E30 M3, `1833055` Toyota Land Cruiser FJ40, `89009067` Germany. `make` on results and price-history is the make name as `/make` gives it in `filter.make` (`BMW`, `Porsche`, `Land Rover`).
- **Model years on `/make`.** `models[].year_min` and `year_max` are as Bring a Trailer lists them (1895 and 2027 on the BMW models captured); they are not production years.

## Workflow

1. **Find the page id.** `/suggestions` with `q` ("e30 m3" returned BMW E30 M3, id 1833018, path `bmw/e30-m3`), or `/make` for the model list with ids and paths.
2. **For a model family,** `/model` with the family path (`porsche/911`) and keep `filter_ids`.
3. **Price history in one call.** `/price-history` with `model_id` (one id or the list), or `make`, plus `recency` or `year_min` / `year_max`. Read `stats_by_currency` per currency and `sell_through_rate`; check `capped`.
4. **Clean the series.** Drop parts, wheels and memorabilia (titles without a model year) and match the variant in the title (a race car, an engine swap, a Euro car) before comparing. Label anything you compute from the rows "computed".
5. **Browse or narrow.** `/results` with `q` and filters (`status` `sold`, `recency`, years, `max_bid`, `category`, `origin`, `era`, `no_reserve` or `premium`, one `make`, `model_id` or `location_id`) for pages of lots with flags and end dates.
6. **Read the car.** `/listing` with the `slug`: `sold_price` or `high_bid`, `bid_count`, `views`, `watchers`, `location`, `seller_type`, `details`, `bat_history` and `bids`. Page `comments` with `comments_page`.
7. **What is live.** `/live` with `make` or `q`, `ending_within_hours` and `sort`, or `/model` and `/make` for that page's live lots.
8. **Report.** Each amount with its currency, status (sold or reserve not met), end date and the listing link, "before the buyer's fee", and the capture date.

## Parameters

### Results (`/results`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | none | Keywords, up to 200 chars. Omitted: every completed result (filters and sort still apply) |
| `exclude` | string | none | Leave out results matching these words |
| `sort` | string | `recently_closed` | `recently_closed`, `popular`, `highest_bid` or `oldest` |
| `status` | string | `all` | `all`, `sold` or `reserve_not_met` |
| `recency` | string | all time | `7d`, `30d`, `1y`, `2y` or `5y` |
| `year_min`, `year_max` | integer | none | Model-year range, 1885-2027 |
| `max_bid` | integer | none | One of Bring a Trailer's steps: 10000, 25000, 50000, 100000, 250000, 500000, 750000, 1000000 |
| `category` | string or integer | none | A name or id: Aircraft (543), All-Terrain Vehicles (431), Boats (383), Charity & Non-Profit (415), Convertibles (434), Diesels (560), Electric Vehicles (426), Go-Karts (428), Hot Rods (429), Kei Vehicles (556), Military Vehicles (447), Minibikes & Scooters (430), Motorcycles (70), Parts (379), Projects (10), Race Cars (11), Right-Hand Drive (557), RVs & Campers (436), Service Vehicles (479), Side-by-Sides (553), Station Wagons (433), Tractors (432), Trains (544), Truck & 4x4 (21), Vans (418), Wheels (380) |
| `origin` | string or integer | none | American (3), Brazilian (499), British (4), Canadian (498), Czech (542), Dutch (497), French (6), German (7), Italian (8), Japanese (9), Korean (496), Prewar (441), Spanish (82), Swedish (18) |
| `era` | string | none | A decade: 2020, 2010 ... 1900, or `pre-1900` |
| `no_reserve` | boolean | false | Only no-reserve auctions (not together with `premium`) |
| `premium` | boolean | false | Only Premium listings (not together with `no_reserve`) |
| `make` | string | none | A make name (`BMW`, `Porsche`, `Land Rover`). Use one of `make`, `model_id` or `location_id` |
| `model_id` | integer, string or list | none | One model page id, or up to 200 ids (a family's `filter_ids`) |
| `location_id` | integer or string | none | One location page id (`89009067` = Germany) |
| `page` | integer | 1 | Page; `page` x `page_size` at most 10,000 |
| `page_size` | integer | 36 | 1-60 |

### Price history (`/price-history`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `model_id` | integer, string or list | one of | One model page id or up to 200 ids |
| `make` | string | one of | A make name instead of `model_id`: its results, at most the 10,000 most recent |
| `recency` | string | all time | `7d`, `30d`, `1y`, `2y` or `5y` |
| `year_min`, `year_max` | integer | none | Model-year range |

### Listing, live, make, model, location, suggestions

| Endpoint | Parameters |
|---|---|
| `/listing` | `slug` (`lots[].slug`, e.g. `1988-bmw-m3-272-2`) or `url` (a bringatrailer.com/listing/<slug>/ link); `comments_page` (default 1), `comments_page_size` 1-500 (default 100) |
| `/live` | `q` (title or excerpt words), `make` (matched in the title), `country` (`US`, `DE`, `GB` or a country name as listed), `ending_within_hours` 1-336, `no_reserve`, `premium`, `sort` (`ending_soon` default, `ending_latest`, `bid_high`, `bid_low`), `limit` 1-2000 (default 100), `page` |
| `/make` | `make` (required): a slug or name (`bmw`, `porsche`, `land-rover`, `Land Rover`) or its bringatrailer.com link |
| `/model` | `model` (required): a make and model path (`bmw/e30-m3`, `porsche/911`, from `models[].path`) or its link |
| `/location` | `country` (required): a country name or slug (`germany`, `united-kingdom`, `Italy`) or its bringatrailer.com/location/ link |
| `/suggestions` | `q` (required): a partial make, model or place, up to 100 chars |

## Examples

### Price history of one model

```bash
curl -X POST https://api.scavio.dev/api/v1/bringatrailer/price-history \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model_id": 1833018}'
```

Captured `data` (2026-11-26; `results` cut to 3 of 490, `notes` dropped):

```json
{
  "filter": {"model_id": [1833018]},
  "total": 490,
  "sold_count": 385,
  "reserve_not_met_count": 105,
  "sell_through_rate": 0.786,
  "capped": false,
  "first_date": "2014-07-30T20:21:10.000Z",
  "last_date": "2026-11-23T19:36:00.000Z",
  "stats_by_currency": {
    "USD": {
      "sold": {"count": 385, "min": 300, "max": 256556, "median": 56000, "average": 59114},
      "reserve_not_met": {"count": 102, "min": 7500, "max": 191000, "median": 53750, "average": 62805}
    },
    "EUR": {
      "sold": null,
      "reserve_not_met": {"count": 3, "min": 3200, "max": 108000, "median": 80500, "average": 63900}
    }
  },
  "count": 490,
  "results": [
    {"id": 114668085, "title": "1991 BMW M3", "url": "https://bringatrailer.com/listing/1991-bmw-m3-54/", "slug": "1991-bmw-m3-54", "date": "2026-11-23T19:36:00.000Z", "amount": 48640, "currency": "USD", "sold": false, "status": "reserve_not_met"},
    {"id": 127148867, "title": "No Reserve: Rebuilt BMW S14 Engine and Getrag 5-Speed Gearbox", "url": "https://bringatrailer.com/listing/engine-383/", "slug": "engine-383", "date": "2026-11-21T19:36:16.000Z", "amount": 19000, "currency": "USD", "sold": true, "status": "sold"},
    {"id": 126146257, "title": "1988 BMW M3", "url": "https://bringatrailer.com/listing/1988-bmw-m3-272-2/", "slug": "1988-bmw-m3-272-2", "date": "2026-11-19T22:03:00.000Z", "amount": 80000, "currency": "USD", "sold": true, "status": "sold"}
  ]
}
```

The first row is a reserve-not-met high bid, not a sale; the second is an engine, not a car.

### Completed results for a keyword

```bash
curl -X POST https://api.scavio.dev/api/v1/bringatrailer/results \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "bronco"}'
```

Captured `data` (2026-11-26; `lots` cut to 2 of 36, `thumbnail`, `excerpt` and `notes` dropped):

```json
{
  "query": "bronco",
  "sort": "recently_closed",
  "status": "all",
  "filters_applied": {},
  "page": 1,
  "page_size": 36,
  "total": 3460,
  "total_pages": 97,
  "reachable_pages": 97,
  "has_more": true,
  "count": 36,
  "lots": [
    {"id": 126349108, "title": "289-Powered 1973 Ford Bronco 4-Speed", "url": "https://bringatrailer.com/listing/1973-ford-bronco-349/", "slug": "1973-ford-bronco-349", "year": 1973, "status": "reserve_not_met", "sold": false, "amount": 30000, "currency": "USD", "ended_at": "2026-11-25T18:27:00.000Z", "ends_at": null, "no_reserve": false, "premium": false, "bat_alumni": false, "country_code": "US"},
    {"id": 127056848, "title": "1969 Ford Bronco 302", "url": "https://bringatrailer.com/listing/1969-ford-bronco-341/", "slug": "1969-ford-bronco-341", "year": 1969, "status": "sold", "sold": true, "amount": 83500, "currency": "USD", "ended_at": "2026-11-24T22:49:50.000Z", "ends_at": null, "no_reserve": false, "premium": false, "bat_alumni": false, "country_code": "US"}
  ]
}
```

`{"location_id": 89009067, "sort": "highest_bid"}` (Germany) read `total` 250: first a 1959 BMW 507 Series II sold for 1,800,000 EUR, then a 1958 Mercedes-Benz 300SL Roadster sold for 880,000 USD (located in Germany, shown in USD), then a 2005 Porsche Carrera GT `withdrawn` with `amount` null. `{"q": "911", "premium": true}` read `total` 785, first a 1989 Porsche 911 Speedster `reserve_not_met` at 104,911 EUR.

### One listing

```bash
curl -X POST https://api.scavio.dev/api/v1/bringatrailer/listing \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "1988-bmw-m3-272-2"}'
```

Captured `data` (2026-11-26; `details` cut to 4 of 20, `bids` to the first and last of 29, `comments.items` to 1 of 34; `description`, `photos` and `notes` dropped):

```json
{
  "requested_slug": "1988-bmw-m3-272-2",
  "id": 126146257,
  "lot_number": 275292,
  "title": "1988 BMW M3",
  "url": "https://bringatrailer.com/listing/1988-bmw-m3-272-2/",
  "slug": "1988-bmw-m3-272-2",
  "year": 1988,
  "status": "sold",
  "sold": true,
  "reserve_not_met": false,
  "no_reserve": false,
  "premium": false,
  "bat_alumni": true,
  "currency": "USD",
  "current_bid": null,
  "sold_price": 80000,
  "high_bid": null,
  "ends_at": null,
  "ended_at": "2026-11-19T22:03:00.000Z",
  "bid_count": 29,
  "comment_count": 35,
  "views": 11598,
  "watchers": 1220,
  "location": {"text": "Pompano Beach, Florida", "city": "Pompano Beach", "region": "Florida", "country": "United States", "country_code": "US"},
  "seller_type": "dealer",
  "seller_type_label": "Dealer",
  "details": ["83k Miles Shown", "Rebuilt 2.3-Liter S14 Inline-Four", "Five-Speed Manual Transmission", "Diamond Black Metallic Paint"],
  "categories": ["german"],
  "photo_count": 141,
  "bat_history": [
    {"title": "1988 BMW M3", "url": "https://bringatrailer.com/listing/1988-bmw-m3-272/", "slug": "1988-bmw-m3-272", "result": "sold", "amount": 87333, "currency": "USD", "date": "2025-12-31T19:41:55.000Z"},
    {"title": "1988 BMW M3", "url": "https://bringatrailer.com/listing/1988-bmw-m3-227/", "slug": "1988-bmw-m3-227", "result": "sold", "amount": 82500, "currency": "USD", "date": "2024-06-14T18:09:00.000Z"}
  ],
  "bids": [
    {"amount": 30, "currency": "USD", "time": "2026-11-13T01:08:29.000Z"},
    {"amount": 80000, "currency": "USD", "time": "2026-11-18T23:39:12.000Z"}
  ],
  "comments": {
    "page": 1, "page_size": 100, "total": 34, "total_pages": 1, "has_more": false,
    "items": [{"time": "2026-11-20T16:50:33.000Z", "text": "well bought", "is_seller": false, "likes": 3}]
  }
}
```

`comment_count` (35) is the site's own count; `comments.total` (34) counts the comments the page carries. Other captured listings: `1991-bmw-m3-54` ended `reserve_not_met` with `high_bid` 48,640 USD after 17 bids (private party, Floral Park, New York); `1994-bmw-850csi-56` sold for 109,000 EUR (private party, Germany); `1985-ferrari-288-gto-2` (Lot #250,000) sold for 6,825,000 USD with 984 comments, read 100 at a time with `comments_page`.

### Live, make, model, location, suggestions

- `/live` `{"ending_within_hours": 36, "no_reserve": true}`: `total_live` 1,073, `total` 117, `has_more` true; first a Carbon-Fiber-Bodied Shelby Cobra 427 CSX4000R at a `current_bid` of 115,000 USD ending 2026-11-27T18:00:00Z (`premium` true), then a 1990 Toyota Pickup 5-Speed at 6,700 USD.
- `/make` `{"make": "bmw"}`: `filter` {`make` "BMW"}, `model_count` 143, `live_count` 68, `completed_total` 22,576, 24 `recent_results`.
- `/model` `{"model": "bmw/e30-m3"}`: BMW E30 M3, `filter_ids` [1833018], `completed_total` 491, 2 live lots (an Original-Owner 1989 BMW M3 at 79,999 USD and a 1988 BMW M3 Race Car at 36,000 USD). `{"model": "porsche/911"}`: 118 `filter_ids` and `sub_models`, 68 live, 20,860 completed.
- `/location` `{"country": "germany"}`: Located in Germany, `location_id` 89009067, 3 live lots in EUR, 250 completed; first recent result the Euro 1994 BMW 850CSi 6-Speed sold for 109,000 EUR.
- `/suggestions` `{"q": "land cruiser"}`: 10 models, among them Toyota Land Cruiser FJ40 (1833055, `toyota/fj40`) and Toyota Land Cruiser FJ55 (6305781); `{"q": "germany"}`: Located in Germany (89009067, `type` location).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def bat(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/bringatrailer/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# A model family: read its ids, then its last year of results in one call (2 credits)
family = bat("model", {"model": "porsche/911"})["data"]
hist = bat("price-history", {"model_id": family["filter_ids"], "recency": "1y"})["data"]
for currency, s in hist["stats_by_currency"].items():
    if s["sold"]:  # keep currencies apart
        print(currency, s["sold"]["count"], s["sold"]["median"])
print("sell-through", hist["sell_through_rate"], "capped", hist["capped"])

# One car with its earlier Bring a Trailer results (1 credit)
car = bat("listing", {"slug": "1988-bmw-m3-272-2"})["data"]
print(car["status"], car["sold_price"], car["high_bid"], car["currency"], car["bid_count"])
for prior in car["bat_history"]:
    print(prior["date"][:10], prior["result"], prior["amount"], prior["currency"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `notes`.

- **lot** (results, recent_results) - `id`, `title`, `url`, `slug`, `year`, `status`, `sold`, `amount`, `currency`, `ended_at`, `ends_at`, `no_reserve`, `premium`, `bat_alumni`, `country_code`, `thumbnail`, `excerpt`.
- **card** (live lists) - `id`, `title`, `url`, `slug`, `year`, `current_bid`, `currency`, `ends_at`, `no_reserve`, `premium`, `bat_alumni`, `country`, `country_code`, `thumbnail`, `excerpt` (and `era` on `/live`).
- **results** - `query`, `sort`, `status`, `filters_applied`, `page`, `page_size`, `total`, `total_pages`, `reachable_pages`, `has_more`, `count`, `lots[]`.
- **price-history** - `filter`, `total`, `sold_count`, `reserve_not_met_count`, `sell_through_rate`, `capped`, `first_date`, `last_date`, `stats_by_currency` {<currency>: {`sold`, `reserve_not_met`} each {`count`, `min`, `max`, `median`, `average`} or `null`}, `count`, `results[]` {`id`, `title`, `url`, `slug`, `date`, `amount`, `currency`, `sold`, `status`} newest to oldest.
- **listing** - `requested_slug`, `id`, `lot_number`, `title`, `url`, `slug`, `year`, `status`, `sold`, `reserve_not_met`, `no_reserve`, `premium`, `bat_alumni`, `currency`, `current_bid`, `sold_price`, `high_bid`, `ends_at`, `ended_at`, `bid_count`, `comment_count`, `views`, `watchers`, `location` {`text`, `city`, `region`, `country`, `country_code`}, `seller_type`, `seller_type_label`, `details[]`, `categories[]`, `description`, `photo_count`, `photos[]`, `bat_history[]` {`title`, `url`, `slug`, `result`, `amount`, `currency`, `date`}, `bids[]` {`amount`, `currency`, `time`} oldest to newest, `comments` {`page`, `page_size`, `total`, `total_pages`, `has_more`, `items[]` {`time`, `text`, `is_seller`, `likes`}} newest to oldest.
- **live** - `total_live`, `total`, `sort`, `filters_applied`, `page`, `limit`, `has_more`, `count`, `lots[]` (cards).
- **make** - `requested_make`, `make`, `title`, `description`, `url`, `filter` {`make`}, `model_count`, `models[]` {`id`, `title`, `url`, `path`, `year_min`, `year_max`, `image`}, `live_count`, `live[]`, `completed_total`, `recent_results[]`.
- **model** - `requested_model`, `title`, `description`, `url`, `filter_ids[]`, `sub_models[]` {`id`, `title`, `url`, `path`, `year_min`, `year_max`, `image`}, `live_count`, `live[]`, `completed_total`, `recent_results[]`.
- **location** - `requested_country`, `title`, `url`, `location_id`, `live_count`, `live[]`, `completed_total`, `recent_results[]`.
- **suggestions** - `query`, `count`, `suggestions[]` {`id`, `title`, `type` (make, model, location, other), `url`, `path`}.

## Guardrails

- Name it "Bring a Trailer (bringatrailer.com, the online collector-car auction site owned by Hearst)" on first mention, "Bring a Trailer" after that.
- Amounts: quote each with its currency, its status (sold, or reserve not met with the high bid), the end date, the listing link and "before the buyer's fee" ("sold for 80,000 USD on Bring a Trailer on Nov 19, 2026, before the buyer's fee"). Never add, average or compare amounts across currencies without saying so, and never convert them.
- Series: keep parts, wheels and memorabilia out of a vehicle's figures, and match the variant before comparing. Anything you compute from the rows (a median of a subset, a change over time) is labelled computed.
- Valuations: report what lots sold or were bid to, with counts and dates. No valuation of a specific car, no prediction of what a live lot will sell for, and no advice to buy, sell or bid.
- People: no usernames, bidder or seller identities, and no chassis numbers or VINs are returned; never try to identify a bidder, seller or commenter, and never ask for or add a VIN. `seller_type` is the only seller signal.
- Descriptive only: no commentary on Bring a Trailer's business, fees or practices. Quote Bring a Trailer and Hearst figures only with their source and date.
- Do not republish Bring a Trailer photos, descriptions or comments. Write bringatrailer.com as plain text and cite titles, slugs, amounts and capture dates rather than embedding Bring a Trailer pages.
- Terms: Scavio does not collect or store Bring a Trailer data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account, places no bid and sets no watchlist. Bring a Trailer's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate sale prices, bids, dates, slugs, ids or counts. Only return what the API returned, with the `fetched_at` time.
- Not available: bidding, watchlists, member profiles or usernames, VINs, seller ZIP codes, the buyer's fee amount, reserve prices, shipping, the full live bid stream (call again for a newer bid), cart or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: more than one of `make`, `model_id` and `location_id` ("Use one of make, model_id or location_id ..."); more than one `location_id` or more than 200 `model_id`s; ids that are not numbers; `no_reserve` and `premium` together ("Bring a Trailer applies them as either-or"); `page` x `page_size` past 10,000 ("Narrow with filters or recency for older lots"); a `max_bid` that is not one of the steps; an unknown `category`, `origin` or `era`; an unknown `sort`, `status` or `recency`; `year_min` after `year_max`; `/price-history` without `model_id` or `make`; `/listing` without `slug` or `url`, a slug not shaped like `1988-bmw-m3-272-2`, or a link that is not a bringatrailer.com/listing/ link; `/make`, `/model`, `/location` or `/suggestions` without their input.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Bring a Trailer listing was found for "<slug>".", "No Bring a Trailer make page was found for "<path>".", "No Bring a Trailer model page was found for "<path>".", "No Bring a Trailer location page was found for "<country>".", or "<path>" is not a Bring a Trailer make / model / location / listing page. Take slugs, paths and ids from a previous answer rather than guessing them.
- `/price-history` with `total` 0 is a `200`: a family page id has no results of its own. Pass the family's `filter_ids` from `/model`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=bring-a-trailer-api).
- `502` means Bring a Trailer data was temporarily unavailable ("Bring a Trailer did not answer in time. Please try again in a moment." or "Bring a Trailer returned an unexpected page. Please try again in a moment."). It is not charged, so retry after a few seconds.
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
const { data: hits } = await scavio.bringatrailer.suggestions({ q: "e30 m3" });
const { data: history } = await scavio.bringatrailer.priceHistory({ model_id: 1833018 });
const { data: results } = await scavio.bringatrailer.results({ q: "bronco", status: "sold", recency: "1y" });
const { data: car } = await scavio.bringatrailer.listing({ slug: "1988-bmw-m3-272-2" });
const { data: live } = await scavio.bringatrailer.live({ make: "Porsche", sort: "bid_high" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.bringatrailer.results(...)`, `price_history`, `listing`, `live`, `make`, `model`, `location` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 8 endpoints as tools: `get_bringatrailer_results`, `get_bringatrailer_price_history`, `get_bringatrailer_listing`, `get_bringatrailer_live`, `get_bringatrailer_make`, `get_bringatrailer_model`, `get_bringatrailer_location` and `get_bringatrailer_suggestions`. Bring a Trailer is opt-in: add `bringatrailer` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,bringatrailer"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [results](https://scavio.dev/docs/bringatrailer-results?utm_source=agent-skills&utm_medium=skill&utm_campaign=bring-a-trailer-api), [price history](https://scavio.dev/docs/bringatrailer-price-history?utm_source=agent-skills&utm_medium=skill&utm_campaign=bring-a-trailer-api), [listing](https://scavio.dev/docs/bringatrailer-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=bring-a-trailer-api), [live](https://scavio.dev/docs/bringatrailer-live?utm_source=agent-skills&utm_medium=skill&utm_campaign=bring-a-trailer-api), [make](https://scavio.dev/docs/bringatrailer-make?utm_source=agent-skills&utm_medium=skill&utm_campaign=bring-a-trailer-api), [model](https://scavio.dev/docs/bringatrailer-model?utm_source=agent-skills&utm_medium=skill&utm_campaign=bring-a-trailer-api), [location](https://scavio.dev/docs/bringatrailer-location?utm_source=agent-skills&utm_medium=skill&utm_campaign=bring-a-trailer-api), [suggestions](https://scavio.dev/docs/bringatrailer-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=bring-a-trailer-api). Overview: [Bring a Trailer API](https://scavio.dev/bringatrailer-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=bring-a-trailer-api).
