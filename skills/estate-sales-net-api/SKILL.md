---
name: estate-sales-net-api
description: EstateSales.net API for EstateSales.net (estatesales.net, the US estate sale directory) - which estate sales, auctions and moving sales are running near a US ZIP code and when, as EstateSales.net lists them (around Dallas ZIP 75201 the site counted 164 sales with 87 in its default list, the 20 nearest from 2.1 miles; around New York ZIP 10001, 17 of the 20 nearest ran tomorrow) with each sale's type, the company running it and its public business contact, the city, state and ZIP, the street address once the site releases it (company-run sales only), every sale day with local and UTC times, the picture count and featured flags, filtered by today, tomorrow or the next 15 days and by 14 sale types, sorted by distance, start, end, newest or most pictures; one sale in full with its terms, description, schedule and pictures; every estate sale company in a metro area (226 in Dallas / Fort Worth / Arlington) with phones, website, address and package; one company's page with its memberships, testimonials (no author names) and current sales; keyword search over sales and marketplace items, 24 a page; one marketplace item with its current bid, starting and minimum bid, buy-now price, reserve flag, shipping and pickup terms (a pair of life-size figures read 635 USD after 4 bids). 6 endpoints, 1 credit per call. US only, USD. Private sellers are never identified (city, state and ZIP only). No sold prices, bidder identities, bidding or checkout.
version: 1.0.0
tags: estatesales, estatesales-net, estate-sales, estate-sales-api, estate-sales-near-me, estate-sale-listings, estate-sale-companies, estate-sale-search, estate-sale-items, estatesales-net-api, estatesales-marketplace, estate-auctions, online-estate-auctions, moving-sales, business-closings, estate-liquidation, estate-sale-calendar, weekend-sales, garage-sales, antiques, vintage, collectibles, furniture, resale, reseller, sourcing, flipping, auction-prices, marketplace-items, local-sales, us-retail, usd, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/estatesales-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=estate-sales-net-api
---

# EstateSales.net API - Estate Sales Near You, Sale Items, Companies

Read EstateSales.net (estatesales.net, the US estate sale directory): the estate sales, auctions and moving sales near a ZIP code or in a city's metro area; one sale in full; every estate sale company in a metro area; one company's page; keyword search over sales and marketplace items; and one marketplace item with its bids and buy-now price. Every answer is what EstateSales.net's public pages show a visitor without an account at the moment of the call, in USD. All 6 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages EstateSales.net shows to any visitor and returns them as JSON for analysis. It uses no EstateSales.net account, no saved sales, no bidding, no buy-now and no checkout.

**The job this skill is for: which sales are on near a place, when, and who runs them.** `/sales` returns the sales EstateSales.net lists around a ZIP (nearest first) with each sale's type, every sale day in local and UTC time, the company running it and its public business contact, the picture count and, for company-run sales, the street address once the site releases it. Captured 2026-11-26 (1 credit per call):

| Request | Site counts (`total_count` / `filtered_count`) | Listed / matched | Nearest sales |
|---|---|---|---|
| `{"zip": "75201"}` (Dallas, TX) | 164 / 87 | 20 / 20 | Moved Offsite to Warehouse by When Pigs Fly Estate, Consignment & Auctions, 2.13 mi, Nov 27-29, 629 pictures; an estate sale by About The House, 3.18 mi, 1,654 pictures; a private estate sale in Dallas 75205, 3.18 mi |
| `{"zip": "10001", "when": "tomorrow"}` (New York, NY) | 382 / 146 | 20 / 17 | Online Only Auctions by Millbrook Country Auctions and Clearing House Estate Sales, 0.64 mi, ending Nov 27 |
| `{"zip": "90012", "type": ["estate_sales"], "sort": "start_date"}` (Los Angeles, CA) | 234 / 129 | 20 / 3 | two private estate sales (Long Beach 90815, Westminster 92683) and one by Grasons Co. Elite Of North Orange County, all starting Nov 27 |

The marketplace answers what single items are going for: `/item` 2038603, a pair of life-size figures sold by Curated Collections in Midland, GA, read a 635 USD current bid after 4 bids, a 100 USD starting bid, a 645 USD minimum next bid and a reserve, local pickup only. `/search` for "lamp" found 1,057 results (24 a page) with items from 5 USD. Quote each sale with its type, the company or "a private seller", the city and ZIP, its dates and the `fetched_at` date. For local resale prices use `offerup-api`, and for liquidation lots `nellis-auction-api`, matched on city and item.

Nine limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **The 20 nearest sales.** EstateSales.net's area page lists the first 20 sales of the ZIP or metro area, nearest first; there is no deeper paging. `total_count` and `filtered_count` are the site's own counts for the area. `when`, `type` and `sort` are applied to those 20 (`listed` is what the page had, `count` what matched), and the note says so.
- **Private sellers are never identified.** A private sale (`seller_type: "private"`) gives its city, state and ZIP only: no name, phone, street address or coordinates. A private sale's own title can mention its area; quote the city and ZIP, not the title's street wording.
- **Company addresses as published.** A company-run sale's street address and coordinates are given once its show-address time has passed (`address_released`; `/sale` gives `address_shown_after_local`). Company phones, websites and addresses are public business contact as the directory shows them.
- **Dates in two clocks.** `*_local` is the sale's own wall-clock time, `*_utc` the instant; `dates[]` holds every sale day.
- **Search is 24 a page, pages 1 to 4.** That is up to 96 results per query; `total` can be higher ("lamp": 1,057). Items (`kind: "item"`) and sales (`kind: "sale"`) come mixed in the site's order. `companies` lists companies whose name matches the query.
- **Marketplace prices as listed.** `current_price` (search) and `prices.current` (item) are the price shown, `current_bid` the high bid and `minimum_bid` the next bid the item takes. These are asking prices and live bids, not sold prices; there is no sold-price history.
- **No bidder or testimonial authors.** No bidder identity is returned, and company testimonials carry text and date only. Testimonial text can name company staff; do not repeat those names.
- **Slow pages.** In the captures sales, sale, companies and item answered in 1.7 to 3.7 seconds, search in 9 to 10 and a company page in 11; the site can take 10 to 50 seconds on search and company pages. Set a client timeout of at least 180 seconds and send one request at a time.

EstateSales.net publishes no public developer API; its API keys are for company accounts and website plugins. This skill reads EstateSales.net's public pages with one Scavio key.

See also: `offerup-api` (OfferUp local listings and asking prices by city), `nellis-auction-api` (liquidation auction lots and closing prices), `ebay-product-data` (sold and active eBay listings for the same item). Same item or same area only: match on city or ZIP and item, and name the site and date with every number.

## When to trigger

Use this skill when the user asks to:
- Find estate sales, auctions, moving sales or business closings near a US ZIP code or in a city's metro area, today, tomorrow or in the next 15 days
- Plan a weekend of estate sales: every sale day with its times, distance, type and company
- Read one estate sale in full: its terms, description, schedule, pictures and the company running it
- List the estate sale companies in a metro area with their phones, websites, addresses and package
- Read an estate sale company's page: memberships, testimonials and the sales it lists now
- Search EstateSales.net by keyword (rolex, mid century modern, lamp) across sales and marketplace items
- Read one EstateSales.net marketplace item with its current bid, starting and minimum bid, buy-now price, reserve flag, shipping and pickup terms

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=estate-sales-net-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=estate-sales-net-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example 10 ZIP codes checked with 4 sales read in full each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, item answered in 1.7 seconds, companies 2.8, sale 2.9, sales 2.9-3.7, search 9.3-9.8 and company 11. Search and company pages can take 10-50 seconds. Set a client timeout of at least 180 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/estatesales/sales` | The 20 nearest sales around a ZIP or in a city's metro area: the site's counts, `when` / `type` / `sort` applied to those 20; each sale with id, title, type, seller type, company and its contact, city, state, ZIP, released address, distance, every sale day, picture count, featured flags | 1 |
| `POST /api/v1/estatesales/sale` | One sale by id or link: status, seller, location with the show-address time, every sale day, length in days, terms, description, featured flags, pictures, auction and video links | 1 |
| `POST /api/v1/estatesales/companies` | Every estate sale company EstateSales.net lists for a metro area: tagline, trusted flag, package, address, phones, website, social links, page, logo, distance | 1 |
| `POST /api/v1/estatesales/company` | One company's page by id or link: profile with description, metro areas, social links and memberships, testimonials (text and date), and the sales it lists | 1 |
| `POST /api/v1/estatesales/search` | Keyword search over sales and marketplace items, 24 a page, pages 1-4: items with price, bid, buy-now, shipping and pickup flags; sales with type, company, city and dates; matching companies | 1 |
| `POST /api/v1/estatesales/item` | One marketplace item by id or link: description, prices (current, current bid, starting, minimum, buy-now, discount), bids, reserve flag, shipping, pickup, payment, terms, categories, dates, status, pictures, the selling company | 1 |

## Market

US only (the 50 states and DC), USD. There is no `country`, `currency` or `language` input. `state` takes a two-letter code (`TX`, `NY`, `CA` ... or `DC`).

## Sale and item fields

| Field | Meaning |
|---|---|
| `type`, `type_name` | The sale type in snake_case and as the site labels it ("Estate Sales", "Online Only Auctions", "Moved Offsite to Warehouse", "By Appointment") |
| `seller_type` | `company` (run by an estate sale company: `company` / `seller` carries its public business contact) or `private` (city, state and ZIP only) |
| `address`, `address_released`, `latitude`, `longitude` | A company-run sale's street address and coordinates as EstateSales.net publishes them, once released; `null` before that and always `null` on private sales |
| `schedule` | The site's own label for when the sale runs ("Today", "Tomorrow") |
| `starts_at_local`, `ends_at_local`, `starts_at_utc`, `ends_at_utc`, `dates[]` | The sale's span and every sale day, in its own wall-clock time and in UTC |
| `featured` | {`local`, `regional`, `national`}: the site's featured placements for the sale |
| `picture_count`, `main_picture` | How many pictures the sale has, and its main picture |
| `status` (sale) | {`message`, `has_started`, `is_over`}: the site's own status text ("starts tomorrow!") |
| `prices` (item) | {`current`, `current_bid`, `starting_bid`, `minimum_bid`, `buy_now`, `base_buy_now`, `discount_percent`} in USD as listed |
| `bids`, `has_reserve`, `allows_bidding`, `allows_buy_now` (item) | Bid count, reserve flag, and whether the item takes bids or a buy-now |
| `shipping`, `pickup` (item) | {`allows_shipping`, `cost`, `days_to_ship`} and {`allows_local_pickup`, `local_pickup_discount`, `details`} |

## Workflow

1. **Sales near a place.** `/sales` with `zip` (or `city` + `state`), optionally `when`, `type` and `sort`. Note `total_count`, `listed` and each `sale_id`.
2. **One sale.** `/sale` with `sale_id` for its terms, description, every day and the pictures.
3. **Companies.** `/companies` with `state` and `metro` (or a city in it); `/company` with `org_id` for one company's page and its current sales.
4. **Items.** `/search` with `query` (pages 1-4), then `/item` with an `item_id` for its bids, reserve and pickup terms.
5. **Report.** Each sale with its type, company or "a private seller", city and ZIP, dates and the `fetched_at` date; each item price with its label (current bid, buy-now) and bid count.
6. **Over time:** store each answer with its `fetched_at`; sales, bids and prices change as EstateSales.net updates them, and that stored set is your record.

## Parameters

### Sales (`/sales`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | A 5-digit US ZIP code (`75201`): the sales around it |
| `city` | string | one of | Or a city (2-80 characters, with `state`): EstateSales.net lists the sales of its metro area |
| `state` | string | with city | A US state code (`TX`) |
| `when` | string | `any` | `any`, `today`, `tomorrow` or `15_days` (starting within 15 days), read as the site's own date filter reads each sale |
| `type` | string or list | none | Sale types to keep: `estate_sales`, `auctions`, `moving_sales`, `business_closings`, `moved_offsite_to_warehouse`, `by_appointment`, `online_only_auctions`, `auction_house`, `moved_offsite_to_store`, `charity_sales`, `outside_sales`, `single_item_type_collections`, `buyouts_or_cleanouts`, `demolition_sales` |
| `sort` | string | `distance` | `distance` (the site's order, nearest first), `start_date`, `end_date`, `newest` (first published) or `most_pictures` |

### Sale, companies, company, search, item

| Endpoint | Parameters |
|---|---|
| `/sale` | one of `sale_id` (`5114622`; `sales[].sale_id`) or `url` (the sale link, `sales[].url`) |
| `/companies` | `state` (required); `metro` (the metro area as EstateSales.net names it, `Dallas-Fort-Worth-Arlington`, `New-York`, or a city in it, `Dallas`); `city` (alias of metro: a city resolves to its metro area) |
| `/company` | one of `org_id` (`14402`; `companies[].org_id`, `sales[].company.org_id`) or `url` (the company link, `companies[].page_url`) |
| `/search` | `query` (required, 2-100 characters: `rolex`, `lamp`, `mid century modern`); `page` 1-4 (24 a page) |
| `/item` | one of `item_id` (`2038603`; search `items[].item_id`) or `url` (the marketplace item link) |

## Examples

### Sales near a ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/estatesales/sales \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "75201"}'
```

Captured `data` (2026-11-26; `sales` cut to 2 of 20 (a company-run and a private sale), `dates` to the first 2 days, `url`, `logo`, `main_picture` and `note` dropped):

```json
{
  "location": {"query": {"zip": "75201", "city": null, "state": null}, "kind": "zip", "state": "TX", "city": "Dallas", "metro": null, "zip": "75201", "heading": "Dallas, TX Estate Sales around 75201", "latitude": 32.787706, "longitude": -96.79985},
  "when": "any",
  "types": [],
  "sort": "distance",
  "total_count": 164,
  "filtered_count": 87,
  "listed": 20,
  "count": 20,
  "sales": [
    {
      "sale_id": 5013480,
      "name": "Black Friday Signature Estate Sale",
      "type": "moved_offsite_to_warehouse",
      "type_name": "Moved Offsite to Warehouse",
      "seller_type": "company",
      "company": {"org_id": 19001, "name": "When Pigs Fly Estate, Consignment & Auctions", "website": "http://www.whenpigsflyestatesales.com", "phones": ["(972) 345-5312", "9405661000"], "package": "Gold"},
      "city": "Dallas",
      "state": "TX",
      "zip": "75207",
      "address": "2223 Monitor St",
      "address_released": true,
      "latitude": 32.79751,
      "longitude": -96.834556,
      "distance_miles": 2.13,
      "schedule": "Tomorrow",
      "starts_at_local": "2026-11-27T09:00:00",
      "ends_at_local": "2026-11-29T15:00:00",
      "starts_at_utc": "2026-11-27T15:00:00Z",
      "ends_at_utc": "2026-11-29T21:00:00Z",
      "dates": [
        {"starts_at_local": "2026-11-27T09:00:00", "ends_at_local": "2026-11-27T15:00:00", "starts_at_utc": "2026-11-27T15:00:00Z", "ends_at_utc": "2026-11-27T21:00:00Z", "show_end_time": true},
        {"starts_at_local": "2026-11-28T09:00:00", "ends_at_local": "2026-11-28T15:00:00", "starts_at_utc": "2026-11-28T15:00:00Z", "ends_at_utc": "2026-11-28T21:00:00Z", "show_end_time": true}
      ],
      "first_published_at": "2026-07-25T16:02:28Z",
      "featured": {"local": false, "regional": false, "national": false},
      "picture_count": 629,
      "auction_url": null,
      "is_marketplace_sale": false
    },
    {
      "sale_id": 5172699,
      "type": "estate_sales",
      "type_name": "Estate Sales",
      "seller_type": "private",
      "company": null,
      "city": "Dallas",
      "state": "TX",
      "zip": "75205",
      "address": null,
      "address_released": false,
      "latitude": null,
      "longitude": null,
      "distance_miles": 3.18,
      "schedule": "Tomorrow",
      "starts_at_local": "2026-11-27T09:00:00",
      "ends_at_local": "2026-11-28T16:00:00",
      "first_published_at": "2026-11-25T19:53:43Z",
      "picture_count": 23,
      "is_marketplace_sale": false
    }
  ]
}
```

The private sale is shortened (its `name`, `dates`, UTC times and `featured` dropped). Tomorrow only near New York: `{"zip": "10001", "when": "tomorrow"}` (382 sales counted, 17 of the 20 listed run tomorrow).

### One marketplace item

```bash
curl -X POST https://api.scavio.dev/api/v1/estatesales/item \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "2038603"}'
```

Captured `data` (2026-11-26; `pickup.details` and `terms` shortened; `url`, `pictures`, the seller's `page_url`, `logo` and `phones` and `note` dropped):

```json
{
  "item_id": 2038603,
  "sale_id": 86098,
  "name": "#414 Life Size Blues Brothers",
  "description": "Dimensions Joilet-65” H x 43” W\nDimensions Elwood-74” H x 32” W\n\nItems are located on the second floor and are larger than life size. Please bring help! Owner paid $1,000 a piece for these originally.",
  "currency": "USD",
  "prices": {"current": 635, "current_bid": 635, "starting_bid": 100, "minimum_bid": 645, "buy_now": null, "base_buy_now": null, "discount_percent": null},
  "bids": 4,
  "has_reserve": true,
  "allows_bidding": true,
  "allows_buy_now": false,
  "shipping": {"allows_shipping": false, "cost": null, "days_to_ship": null},
  "pickup": {"allows_local_pickup": true, "local_pickup_discount": null, "details": "HOLIDAY SPECIAL! NO BUYERS PREMIUM! ..."},
  "payment": {"online": true, "in_person": false, "in_person_details": null},
  "terms": "If the reserve is not met, please contact us. We may be able to sell the pieces outright for a lower price. ...",
  "categories": [{"id": 6, "name": "Home", "parent_id": null}],
  "tags": [],
  "city": "Midland",
  "state": "GA",
  "zip": "31820",
  "published_at": "2026-11-19T20:23:01Z",
  "starts_at_utc": "2026-11-20T23:00:00Z",
  "ends_at_utc": "2026-11-27T23:00:00Z",
  "utc_offset": -5,
  "status": {"has_started": true, "has_ended": false, "is_active": true, "sale_has_ended": false},
  "dimensions": null,
  "picture_count": 10,
  "seller": {"type": "company", "org_id": 136664, "name": "Curated Collections", "website": "http://www.curated-collections.com", "trusted": true}
}
```

### Sale, companies, company, search

- `/sale` `{"sale_id": "5114622"}`: a 3-day estate sale in Garland, TX 75041 run by DFW Estate Liquidators, `status` "starts tomorrow!", address released after 2026-11-26 09:00 local, Nov 27-29 from 09:00, 287 pictures, regionally featured, with the company's terms and description as plain text.
- `/companies` `{"state": "TX", "metro": "Dallas-Fort-Worth-Arlington"}`: 226 companies in Dallas / Fort Worth / Arlington, each like {"org_id": 14402, "name": "DFW Estate Liquidators", "trusted": true, "package": "Gold", "city": "Arlington", "zip": "76017", "phones": ["(682) 239-1746"], "website": "http://www.dfwestateliquidators.com", "distance": {"miles": 25, "display": "< 25 miles"}}.
- `/company` `{"org_id": "14402"}`: the profile with metro areas (Dallas / Fort Worth / Arlington, Wichita Falls), 2 memberships (Appraisers Association of America, American Society of Estate Liquidators), 22 testimonials (text and date) and 19 current and upcoming sales.
- `/search` `{"query": "lamp"}`: 1,057 results, 24 on page 1 (23 items and 1 sale), from "Vtg lamps" in Greeley, CO at 5 USD to an "Industrial Floor Lamp" in Ozark, MO at 250 USD buy-now. `{"query": "rolex", "page": 2}`: 70 results, page 2 all sales (an online-only jewelry auction by Pacific Auction House in Los Angeles ...).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def es(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/estatesales/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# Estate sales starting within 15 days near a ZIP, soonest first (1 credit)
s = es("sales", {"zip": "75201", "when": "15_days", "type": ["estate_sales"], "sort": "start_date"})["data"]
print(s["total_count"], "counted;", s["count"], "of", s["listed"], "listed match")
for sale in s["sales"]:
    who = sale["company"]["name"] if sale["seller_type"] == "company" else "a private seller"
    print(sale["sale_id"], sale["type_name"], who, sale["city"], sale["zip"], sale["starts_at_local"], sale["picture_count"])

# Store each answer with fetched_at: that stored set is your record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every answer carries `note`.

- **sales** - `location` {`query`, `kind` (zip or metro), `state`, `city`, `metro`, `zip`, `heading`, `latitude`, `longitude`}, `when`, `types`, `sort`, `total_count`, `filtered_count`, `listed`, `count`, `sales[]` {`sale_id`, `name`, `type`, `type_name`, `url`, `seller_type`, `company` {`org_id`, `name`, `page_url`, `website`, `phones`, `logo`, `package`}, `city`, `state`, `zip`, `address`, `address_released`, `latitude`, `longitude`, `distance_miles`, `schedule`, `starts_at_local`, `ends_at_local`, `starts_at_utc`, `ends_at_utc`, `dates[]`, `first_published_at`, `featured` {`local`, `regional`, `national`}, `picture_count`, `main_picture` {`url`, `thumbnail_url`, `width`, `height`, `description`}, `auction_url`, `is_marketplace_sale`}, `note`.
- **sale** - `sale_id`, `name`, `type`, `type_name`, `url`, `status` {`message`, `has_started`, `is_over`}, `seller` (company: {`type`, `org_id`, `name`, `phones`, `page_url`, `website`, `logo`, `trusted`}; private: {`type`}), `location` {`address`, `city`, `state`, `zip`, `latitude`, `longitude`, `directions`, `address_released`, `address_shown_after_utc`, `address_shown_after_local`}, `starts_at_local`, `ends_at_local`, `starts_at_utc`, `ends_at_utc`, `dates[]`, `utc_offset`, `length_in_days`, `terms`, `description`, `featured`, `picture_count`, `pictures[]`, `auction_url`, `video_url`, `is_marketplace_sale`, `note`.
- **companies** - `state`, `metro`, `heading`, `count`, `companies[]` {`org_id`, `name`, `tagline`, `trusted`, `package`, `address`, `city`, `state`, `zip`, `latitude`, `longitude`, `phones`, `website`, `social` {`facebook`, `instagram`, `youtube`, `pinterest`, `linkedin`, `twitter`}, `page_url`, `logo`, `has_home_page`, `created_at`, `distance` {`miles`, `display`}}, `note`.
- **company** - `profile` {`org_id`, `name`, `logo`, `phones`, `website`, `description`, `city`, `state`, `zip`, `page_url`, `primary_metro_area`, `metro_areas`, `social`, `memberships[]` {`name`, `description`}, `has_home_page`}, `testimonials[]` {`id`, `text`, `date`}, `sales_count`, `sales[]` {`sale_id`, `name`, `type`, `type_name`, `url`, `address`, `city`, `state`, `zip`, `status`, `has_started`, `starts_at_local`, `ends_at_local`, `picture_count`, `thumbnail_url`, `featured`}, `note`.
- **search** - `query`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `max_page`, `count`, `items[]` (kind item: `item_id`, `name`, `url`, `currency`, `current_price`, `current_bid`, `buy_now_price`, `base_buy_now_price`, `bids`, `accepts_bids`, `buy_now`, `allows_shipping`, `shipping_cost`, `allows_local_pickup`, `city`, `state`, `starts_at_utc`, `ends_at_utc`, `main_picture`; kind sale: `sale_id`, `name`, `type`, `type_name`, `url`, `seller_type`, `company_name`, `address`, `city`, `state`, `zip`, `starts_at_local`, `ends_at_local`, `dates`, `featured`, `main_picture`), `companies[]` {`org_id`, `name`, `city`, `state`, `zip`, `page_url`}, `note`.
- **item** - `item_id`, `sale_id`, `name`, `url`, `description`, `currency`, `prices`, `bids`, `has_reserve`, `allows_bidding`, `allows_buy_now`, `shipping`, `pickup`, `payment` {`online`, `in_person`, `in_person_details`}, `terms`, `categories[]` {`id`, `name`, `parent_id`}, `tags`, `city`, `state`, `zip`, `published_at`, `starts_at_utc`, `ends_at_utc`, `utc_offset`, `status` {`has_started`, `has_ended`, `is_active`, `sale_has_ended`}, `dimensions`, `picture_count`, `pictures[]` {`url`, `thumbnail_url`}, `seller` {`type`, `org_id`, `name`, `page_url`, `website`, `phones`, `logo`, `trusted`}, `note`.

## Guardrails

- Name it "EstateSales.net (estatesales.net)" on first mention, "EstateSales.net" after that.
- Sales: always with the type, the company name or "a private seller", the city, state and ZIP, the dates and the `fetched_at` date ("Estate sale by DFW Estate Liquidators in Garland, TX 75041, Nov 27-29, 2026, fetched Nov 26, 2026").
- Private sellers: never try to identify a private seller, find a private sale's address or guess it from the title, the pictures or the distance. City, state and ZIP are all there is.
- Companies: company phones, websites and addresses are public business contact; use them as such. Testimonials carry no author; do not repeat staff names that appear in testimonial text.
- Items: quote prices with their label ("current bid 635 USD after 4 bids, with a reserve"), never as a sold price or a valuation of the item.
- Descriptive only: no commentary on EstateSales.net's business, its companies or their practices, and no ranking of companies from the data.
- Do not republish EstateSales.net pictures, sale descriptions or item text in bulk. Write estatesales.net as plain text and cite sale ids, org ids, item ids and capture dates rather than linking EstateSales.net pages.
- Terms: Scavio keeps no copy: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no bidding, buy-now or checkout flow. EstateSales.net's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate sales, dates, companies, prices, bids or ids. Only return what the API returned, with the `fetched_at` time.
- Not available: sold prices or price history, sales past the 20 nearest of an area, search past page 4, bidder identities, private seller contact, bidding, buy-now or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: sales without a place ("Send zip (a 5-digit US ZIP code), or city with state (Dallas, TX)."), a city without a state ("state is required with city (a US state code: TX, NY, CA ... or DC)."), a bad ZIP ("zip must be a 5-digit US ZIP code."), a bad state ("state must be a US state code (TX, NY, CA ... or DC)."); `/companies` without a metro ("metro is required: a metro area slug (Dallas-Fort-Worth-Arlington) or a city in it (Dallas)."); `/sale`, `/company` or `/item` without an id ("sale_id (or url) is required.", "org_id (or url) is required.", "item_id (or url) is required."), with a link of the wrong kind ("url must be an EstateSales.net sale link ...") or an id that does not match the link ("sale_id does not match the link's sale id."); a search under 2 characters ("query must be at least 2 characters (a word such as lamp, rolex or mid century modern)."); `page` outside 1-4; a `when`, `type` or `sort` value outside its list.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "EstateSales.net has no page for this ZIP code.", "EstateSales.net has no page for this city: send a ZIP code, or a city and its state as the site lists it (Dallas, TX).", "EstateSales.net has no sale with this id (it may have been removed).", "EstateSales.net has no company directory for this metro area: send its metro slug (Dallas-Fort-Worth-Arlington) or a city in it (Dallas) with the state.", "EstateSales.net has no company with this id.", "EstateSales.net found nothing for this search.", "EstateSales.net has no marketplace item with this id.". Take ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=estate-sales-net-api).
- `502` means EstateSales.net data was temporarily unavailable ("EstateSales.net is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("EstateSales.net is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.98.0
npm install scavio@0.99.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: near } = await scavio.estatesales.sales({ zip: "75201" });
const { data: sale } = await scavio.estatesales.sale({ sale_id: "5114622" });
const { data: companies } = await scavio.estatesales.companies({ state: "TX", metro: "Dallas-Fort-Worth-Arlington" });
const { data: company } = await scavio.estatesales.company({ org_id: "14402" });
const { data: found } = await scavio.estatesales.search({ query: "rolex", page: 2 });
const { data: item } = await scavio.estatesales.item({ item_id: "2038603" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.estatesales.sales(...)`, `sale`, `companies`, `company`, `search` and `item`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 6 endpoints as tools: `get_estatesales_sales`, `get_estatesales_sale`, `get_estatesales_companies`, `get_estatesales_company`, `search_estatesales` and `get_estatesales_item`. EstateSales.net is opt-in: add `estatesales` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.98.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,estatesales"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [sales](https://scavio.dev/docs/estatesales-sales?utm_source=agent-skills&utm_medium=skill&utm_campaign=estate-sales-net-api), [sale](https://scavio.dev/docs/estatesales-sale?utm_source=agent-skills&utm_medium=skill&utm_campaign=estate-sales-net-api), [companies](https://scavio.dev/docs/estatesales-companies?utm_source=agent-skills&utm_medium=skill&utm_campaign=estate-sales-net-api), [company](https://scavio.dev/docs/estatesales-company?utm_source=agent-skills&utm_medium=skill&utm_campaign=estate-sales-net-api), [search](https://scavio.dev/docs/estatesales-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=estate-sales-net-api), [item](https://scavio.dev/docs/estatesales-item?utm_source=agent-skills&utm_medium=skill&utm_campaign=estate-sales-net-api). Overview: [EstateSales.net API](https://scavio.dev/estatesales-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=estate-sales-net-api).
