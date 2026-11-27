---
name: sweetwater-api
description: Sweetwater API for Sweetwater (sweetwater.com, the US online music instrument and pro audio retailer; US, USD) - what a guitar, pedal, microphone or interface costs at Sweetwater today and how many units Sweetwater has, as sweetwater.com shows it (on 2026-11-27 the Boss DD-8 Digital Delay Pedal read $168.88 against a $197.99 retail price with the offer "$29 Price Drop", 210 units on hand, 204 available to sell and 147 on order; the Shure SM58 read $89 with "$20.00 Off!", 3,366 on hand) with the price now, retail price, base price, instant and mail-in rebates, bundle savings, the special offer text and value, in-stock, pre-order and special-order flags, free shipping and the open-box (Demo) units with their own price; keyword search (the 42 results the site shows, in its relevance order; a keyword that opens a category, such as stratocaster, returns that category's listing with sort and page applied); a category listing, 42 per page to page 120, in the site's 7 sorts (popular, rating, lightest, newest, price, brand) with facet filters as the site names them (Availability, Brand, Price Range, Body Shape) and facet counts; one product by item id or link with MPN, breadcrumbs, was price, price drop, instant savings, stock text and backorder date, ship weight, return days, dimensions and specs (an open-box unit with its serial number and the new price); the serial-numbered units of one instrument, each with its serial number, shipping weight and Sweetwater's own photos (an American Ultra II Stratocaster HSS listed 6 units, 8.05 to 8.35 lbs); customer reviews with the star distribution, filtered by stars, sorted and paged (the SM58 had 372, 4.7 average), without reviewer names; the Deal Zone and its 145 deal pages (Price Drops, Guitars, Demos, Bundles) with the Black Friday sale window as the page states it. 6 endpoints, 1 credit per call. US only. No Gear Exchange used listings, store stock, search suggestions or price history.
version: 1.0.0
tags: sweetwater, sweetwater-com, sweetwater-api, sweetwater-prices, sweetwater-search, sweetwater-deals, sweetwater-deal-zone, sweetwater-price-drops, sweetwater-black-friday, sweetwater-open-box, sweetwater-demo, sweetwater-serial-numbers, sweetwater-serial-units, sweetwater-reviews, sweetwater-stock, sweetwater-categories, guitar-prices, guitar-pedal-prices, bass-prices, amp-prices, microphone-prices, audio-interface-prices, synthesizer-prices, pro-audio, music-gear, musical-instruments, music-retail, gear-prices, gear-deals, open-box-gear, serial-numbered-guitars, guitar-weight, stock-levels, units-on-hand, product-search, category-browse, product-reviews, price-monitoring, competitor-research, us-retail, usd, langchain, crewai, ai-agents, structured-data, json, mcp
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/sweetwater-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=sweetwater-api
---

# Sweetwater API - Gear Prices, Stock Counts, Serial Numbers, Deal Zone, Reviews

Read Sweetwater (sweetwater.com, the US online music instrument and pro audio retailer): keyword search, category listings with the site's sorts and facet filters, one product in full, the serial-numbered units of an instrument, customer reviews and the Deal Zone. www.sweetwater.com only (US, USD, English). Every endpoint returns structured JSON at 1 credit per call.

**The job this skill is for: what a piece of gear costs at Sweetwater today, and how many Sweetwater has.** Sweetwater's listings carry the price now next to the retail price, the rebates and the offer text, and the unit counts behind the stock flag. On 2026-11-27 the Boss DD-8 Digital Delay Pedal (`DD8`) read $168.88 against a $197.99 retail price, with the special offer "$29 Price Drop" (value 29.11), 210 units on hand, 204 available to sell and 147 on order; the Shure SM58 read $89 with "$20.00 Off!" and 3,366 on hand. The second job is choosing one instrument: `/serial-units` lists every serial-numbered unit Sweetwater photographed and weighed (an American Ultra II Stratocaster HSS in Ultraburst, `StratAU2HEUB`, listed 6 units from 8.05 to 8.35 lbs at $2,359.99, and a Demo open-box unit at $1,919.99). Pair it with `ebay-product-data` for used and sold prices of the same model, and `amazon-product-data` for the same item at Amazon (match on brand and MPN).

Seven limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`) are not.
- **Free-text search shows 42 results.** A keyword search returns the results Sweetwater shows on its first page, in its relevance order; the site does not page or sort free-text results, so `page` 2 is an empty list and `sort` does not reorder them. `total` is the site's own count (`shure sm58` read 96 with 42 shown). Use `/category` for a full, sorted, paged listing.
- **Some keywords open a category.** A keyword that matches a category (`stratocaster`) lands on that category's listing: `landed_on` is `category`, and there `sort` and `page` do apply (Stratocaster page 2 sorted `price_desc`: 503 products, 12 pages). A keyword that opens one product page answers `landed_on` `product` with `landed_url`; send that to `/product`.
- **Listings stop at 5,000.** Sweetwater counts at most 5,000 products in a listing, 42 per page, so the last page is 120. Narrow a big category with `facets`.
- **Unit counts are Sweetwater's, as given.** `on_hand` (units on hand), `available` (units available to sell; it can be negative when more are sold than on hand) and `on_order` come on search and deal items. Category cards carry only the stock text the card shows (`In Stock`, `Only 6 Left`, or null).
- **US only.** There is no `country` parameter. Every answer carries `store` (sweetwater), `host`, `country` (us), `currency` (USD) and `language` (en).
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

Sweetwater has no public API for its catalog, prices or stock. Prices, stock and reviews are shown on sweetwater.com for each product, and this skill reads those public pages with one Scavio key.

See also: Amazon prices for the same item `amazon-product-data`; eBay listings and sold prices `ebay-product-data`; Best Buy `best-buy-product-data`; Walmart `walmart-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price a guitar, bass, amp, pedal, microphone, interface, keyboard or drum kit at Sweetwater, with the retail price, rebates and the offer text
- Check how many units of an item Sweetwater has on hand, available or on order, or whether it is backordered and until when
- Search sweetwater.com by keyword, or list a category (Solidbody Guitars, Reverb & Delay Pedals) sorted by popularity, rating, lightest, newest, price or brand and filtered by availability, brand, price range or any facet the site shows
- Read one Sweetwater product in full: MPN, breadcrumbs, was price, price drop, instant savings, ship weight, return days, dimensions and specs
- Read an open-box (Demo) unit: its serial number, price and the new price
- List the serial-numbered units of one guitar or bass, with each unit's serial number, shipping weight and photos
- Read Sweetwater customer reviews of a product, filtered by stars and sorted newest, oldest, highest or lowest, with the star distribution
- List the Sweetwater Deal Zone or one deal page (Price Drops, Guitars, Demos, Bundles, Rebates & Promos) and the Black Friday sale window

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=sweetwater-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=sweetwater-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Calls usually take 2-15 seconds (in the captures: deals 2.3, serial units 3.3, search 3.6, a category 8.3, a product 10, reviews 11). Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/sweetwater/search` | Keywords: the 42 results the site shows in relevance order, each with price, retail price, rebates, offer, unit counts and open-box units; or, when the keyword opens a category, that category's listing with sort and page applied | 1 |
| `POST /api/v1/sweetwater/category` | One category listing, 42 per page to page 120, 7 sorts, facet filters, with the facets and their counts | 1 |
| `POST /api/v1/sweetwater/product` | One product by item id or link: price, was price, price drop, stock text, backorder date, ship weight, dimensions, specs; an open-box unit with its serial number | 1 |
| `POST /api/v1/sweetwater/serial-units` | The serial-numbered units of one item: serial number, shipping weight and photos per unit, plus the open-box unit | 1 |
| `POST /api/v1/sweetwater/reviews` | Customer reviews of one product with the average, total and star distribution, filtered by stars, sorted and paged; no reviewer names | 1 |
| `POST /api/v1/sweetwater/deals` | The Deal Zone or one deal page, 42 per page, in the Deal Zone's sort menu, with the sale window and every deal page | 1 |

## Prices and stock

Search and deal items (`items[]`) carry:

| Field | Meaning |
|---|---|
| `price` | The price now, USD |
| `retail_price`, `base_price` | The retail price and base price as Sweetwater gives them |
| `has_price_drop` | Sweetwater's price-drop flag as given (the DD-8 read false while its offer text read "$29 Price Drop") |
| `instant_rebate`, `mail_in_rebate` | Rebate amounts as given (0 when none) |
| `bundle_savings` | Bundle savings as given, or null |
| `special_offer` | {`title`, `value`}: the offer text and its value ("Save $100.00 For a Limited Time!", 100), or null |
| `in_stock`, `pre_order`, `special_order`, `free_shipping` | Sweetwater's flags |
| `on_hand`, `available`, `on_order` | Units on hand, units available to sell (can be negative), units on order |
| `open_box[]` | {`item_id`, `condition` (Demo), `price`}: open-box units of the item |

Category cards (`/category`, and `/search` when it lands on a category) are lighter: `price`, `offer` (the offer text as shown), `stock` (the stock text as shown, or null), `open_box` {`item_id`, `price`, `text`}, `serial` {`number`, `weight`} on a serial-numbered instrument (weight as written, `7lbs. 5oz`), `bundle_savings_available`, `rating`, `review_count`.

`/product` adds `was_price`, `price_drop`, `instant_savings`, `new_price` (the new price, on an open-box unit), `availability` (`InStock`, `BackOrder`, ... as given), `stock_text` (`In Stock!`, `Backordered - More On The Way!`), `estimated_by` (the backorder date text, `November 30`) and `warehouse_flags` {`fw`, `az`} (the page's in-stock flag per warehouse, as given).

- Quote "Boss DD-8 Digital Delay Pedal: $168.88 at sweetwater.com on 2026-11-27 (retail $197.99, offer: $29 Price Drop)", with the date.
- Report Sweetwater's prices, rebates, offers and counts as given and the arithmetic only. Never compute a price after a mail-in rebate as the price, never judge a price as a good deal, and never describe how often an item is in stock.

## Workflow

1. **Find the item.** `/search` with `query` (`boss delay pedal`): each item's `item_id` is the input of product, serial units and reviews. If `landed_on` is `category`, the items are that category's listing; if it is `product`, send `landed_url` to `/product`.
2. **Browse a category.** `/category` with `category` (an id `c590`, a path `c590--Solid_Body_Guitars` or a link), `sort` and `page`; read `facets[]` and send values back in `facets` (`{"Availability": ["In Stock"], "Brand": ["Boss"]}`).
3. **One product.** `/product` with `item_id` or `url`. An open-box unit has its own id (`StratAU2HEUBd3`, from `open_box[].item_id`): its answer has `condition` Used, `open_box` true, its `serial_number` and the `new_price`.
4. **Pick a unit.** `/serial-units` with the item id lists each serial-numbered unit with its weight and photos. An item sold without serial numbers returns an empty `units` list.
5. **Reviews.** `/reviews` with `item_id`, optionally `stars`, `sort`, `page` and `limit` (up to 100 per page).
6. **Deals.** `/deals` without `deal` for the whole Deal Zone, or with a slug from `deal_pages[].slug` (`price-drops`, `guitar-deals`, `demos`, `bundles`); `sale_event` carries the sale window as the page states it.
7. **Watching prices:** there is no history. Poll the same items on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords, 1-200 chars |
| `sort` | string | `relevance` | `relevance`, `popular`, `rating`, `lightest`, `newest`, `price_desc`, `price_asc`, `brand`. Free-text results stay in relevance order; a sort applies when the keyword opens a category |
| `page` | integer | 1 | 1-120. Free-text search has one page (a page past 1 is an empty list); pages of 42 apply when the keyword opens a category |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category` | string | required | A category id (`c590`), a path (`c590--Solid_Body_Guitars`) or a sweetwater.com category link (facets on a pasted link are kept when `facets` is not sent) |
| `sort` | string | `popular` | `popular` (Most Popular), `rating` (Customer Rating), `lightest` (Lightest Guitar), `newest` (Newest Arrivals), `price_desc`, `price_asc`, `brand` (Brand A - Z). The site's own values (`low2high`, `high2low`, `reviews`, `name`) are accepted too |
| `page` | integer | 1 | 1-120, 42 products per page |
| `facets` | object | none | Facet filters as the site names them (`facets[].name` and `values[].value` of an answer): up to 12 facets, up to 20 values each, e.g. `{"Availability": ["In Stock"], "Brand": ["Fender", "Gibson"], "Price Range": ["$500 - $1,000"]}` |

### Product (`/product`) and serial units (`/serial-units`)

Exactly one of `item_id` (2-40 letters, digits, `.`, `_` or `-`: `DD8`, `SM58`, an open-box id such as `StratAU2HEUBd3`) or `url` (a sweetwater.com `/store/detail/<item id>--<name>` link; a `?cond=` open-box link selects that unit).

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` or `url` | string | required (one) | As product |
| `stars` | integer | none | 1-5: only reviews with this many stars (the site's own filter) |
| `sort` | string | `newest` | `newest`, `oldest`, `highest`, `lowest` |
| `page` | integer | 1 | 1-1000 |
| `limit` | integer | 25 | 1-100 reviews per page |

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `deal` | string | none | A Deal Zone page slug (`deal_pages[].slug`: `guitar-deals`, `price-drops`, `demos`, `bundles`, `rebates-and-promos`, ...); leave out for the whole Deal Zone |
| `sort` | string | `featured` | `featured` (the Deal Zone's own order), `popular`, `best_deals`, `newest_deals`, `ending_soon`, `newest`, `price_desc`, `price_asc`, `brand` |
| `page` | integer | 1 | 1-120, 42 per page |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/sweetwater/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "boss delay pedal"}'
```

Captured `data` (2026-11-27; 1 of 20 items shown):

```json
{
  "store": "sweetwater",
  "host": "www.sweetwater.com",
  "country": "us",
  "currency": "USD",
  "language": "en",
  "query": "boss delay pedal",
  "landed_on": "search",
  "category": null,
  "sort": "relevance",
  "page": 1,
  "total": 20,
  "total_pages": 1,
  "per_page": 42,
  "count": 20,
  "items": [
    {
      "position": 1,
      "item_id": "DD8",
      "name": "DD-8 Digital Delay Pedal",
      "brand": "Boss",
      "type": "Pedal Delay/Reverb",
      "category": "Guitars > Guitar Pedals & Effects > Reverb & Delay Pedals",
      "url": "https://www.sweetwater.com/store/detail/DD8--boss-dd-8-digital-delay-pedal",
      "condition": "New",
      "price": 168.88,
      "retail_price": 197.99,
      "base_price": 197.99,
      "has_price_drop": false,
      "instant_rebate": 0,
      "mail_in_rebate": 0,
      "bundle_savings": null,
      "special_offer": { "title": "$29 Price Drop", "value": 29.11 },
      "in_stock": true,
      "on_hand": 210,
      "available": 204,
      "on_order": 147,
      "pre_order": false,
      "special_order": false,
      "free_shipping": true,
      "open_box": [],
      "rating": 5,
      "review_count": 39
    }
  ],
  "facets": [],
  "note": "Free-text search shows 42 results in Sweetwater's relevance order; the site does not page or sort them."
}
```

The next results were the DM-2W Waza Craft Delay ($175.99, 95 on hand), the DD-3T ($142.98 against $153.99, "$11 Price Drop") and the RE-202 Space Echo. `{"query": "stratocaster", "sort": "price_desc", "page": 2}` opened a category instead: `landed_on` `category`, `category` {`id` c589, `name` Stratocaster Electric Guitars}, `applied_facets` {`Body_Shape`: [Stratocaster]}, `total` 503, `total_pages` 12, items 43-84 as category cards (the first, a Fender Custom Shop 1963 Stratocaster at $6,275, with `serial` {`number` CZ592234, `weight` 7lbs. 5oz}).

### Category with facets

```bash
curl -X POST https://api.scavio.dev/api/v1/sweetwater/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category": "c590--Solid_Body_Guitars", "sort": "price_asc"}'
```

Captured `data` (2026-11-27; 2 of 42 items and 1 of 23 facets shown, breadcrumbs dropped):

```json
{
  "category": { "id": "c590", "name": "Solidbody Guitars", "url": "https://www.sweetwater.com/c590--Solid_Body_Guitars" },
  "sort": "price_asc",
  "site_sort": "low2high",
  "page": 1,
  "total": 5000,
  "total_pages": 120,
  "per_page": 42,
  "requested_facets": {},
  "applied_facets": {},
  "count": 42,
  "items": [
    {
      "position": 1,
      "item_id": "KF21TECT",
      "name": "Kramer Focus VT-211S Electric Guitar - Teal",
      "url": "https://www.sweetwater.com/store/detail/KF21TECT--kramer-focus-vt-211s-electric-guitar-teal",
      "price": 149,
      "offer": null,
      "rating": 4.5,
      "review_count": 11,
      "stock": null,
      "open_box": null,
      "serial": null,
      "bundle_savings_available": false
    },
    {
      "position": 2,
      "item_id": "JS1XRRMSB",
      "name": "Jackson RR Minion JS1X Electric Guitar - Satin Black",
      "url": "https://www.sweetwater.com/store/detail/JS1XRRMSB--jackson-js-series-rr-minion-js1x-satin-black",
      "price": 179.99,
      "offer": null,
      "rating": 4.5,
      "review_count": 13,
      "stock": "In Stock",
      "open_box": null,
      "serial": null,
      "bundle_savings_available": true
    }
  ],
  "facets": [
    { "name": "Availability", "values": [ { "value": "In Stock", "count": 4266, "selected": false }, { "value": "Pre-order", "count": 48, "selected": false } ] }
  ]
}
```

`total` 5000 is the most Sweetwater counts in a listing, so the category is at least that large; the Brand facet listed 43 brands (Fender 813, Schecter 659). `{"category": "c974", "facets": {"Availability": ["In Stock"], "Brand": ["Boss"]}}` answered Reverb & Delay Pedals, 38 products on one page, DD-8 first. An unknown category is a charged `404`: "Sweetwater has no category c99999."

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/sweetwater/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "DD8"}'
```

Captured `data` (2026-11-27; breadcrumbs, images and 15 of 17 specs dropped):

```json
{
  "item_id": "DD8",
  "requested": "DD8",
  "name": "DD-8 Digital Delay Pedal",
  "full_name": "Boss DD-8 Digital Delay Pedal",
  "brand": "Boss",
  "mpn": "DD-8",
  "type": "Pedal Delay/Reverb",
  "category": "Guitars > Guitar Pedals & Effects > Reverb & Delay Pedals",
  "url": "https://www.sweetwater.com/store/detail/DD8--boss-dd-8-digital-delay-pedal",
  "condition": "New",
  "open_box": false,
  "serial_number": null,
  "price": 168.88,
  "was_price": 197.99,
  "price_drop": 29.11,
  "instant_savings": null,
  "new_price": null,
  "availability": "InStock",
  "stock_text": "In Stock!",
  "estimated_by": null,
  "warehouse_flags": { "fw": true, "az": true },
  "ship_weight_lbs": 1.27,
  "free_shipping": true,
  "return_days": 30,
  "rating": 5,
  "review_count": 39,
  "dimensions": { "height_in": 2.37, "width_in": 2.87, "depth_in": 5.12, "weight_lbs": 1 },
  "specs": [
    { "name": "Pedal Type", "value": "Delay, Looper" },
    { "name": "Analog/Digital", "value": "Digital" }
  ]
}
```

A backordered item reads like the Shure SLXD24+/SM58 wireless system (`SLXD24p58G57`): `price` 709, `was_price` 789, `instant_savings` 80, `stock_text` "Backordered - More On The Way!", `estimated_by` "November 30". The open-box unit `StratAU2HEUBd3` answered `condition` Used, `open_box` true, `serial_number` US26006895, `price` 1919.99 and `new_price` 2359.99. An unknown id is a charged `404`: "Sweetwater has no item ZZNOPE99X."

### Serial units, reviews and deals

- `/serial-units` `{"item_id": "StratAU2HEUB"}`: Fender American Ultra II Stratocaster HSS, Ultraburst, `price` 2359.99, `open_box` {`item_id` StratAU2HEUBd3, `condition` Demo, `price` 1919.99}, `count` 6, `units[]` each with `serial_number` (US25031401), `item_id`, `weight_lbs` (8.05), a `url` with `?serial=` and 4 `photos` {`view` body, front, ...}. A Squier Mini Stratocaster (`StratMiniSP`) answered `count` 0: Sweetwater sells some instruments by serial number, not all.
- `/reviews` `{"item_id": "SM58", "limit": 10}`: Shure SM58, `average_rating` 4.7, `total_reviews` 372, `star_percent` {"5": 69, "4": 27, "3": 2, "2": 1, "1": 1}, `total_pages` 38, each review with `rating`, `title` ("Shure 58 Mic"), `text` and `date` (2026-11-11). No reviewer names, locations or backgrounds.
- `/deals` `{"deal": "guitar-deals"}`: `deal_name` Guitars, `total` 8,493, 120 pages, `sale_event` {`name` Black Friday, `starts` 2026-11-13 10:00:00, `ends` 2026-11-30 02:59:00, `time_zone` null}, items as search items (a Fender Player II Modified Telecaster at $949.99 against $1,049.99, `instant_rebate` 100, "Save $100.00 For a Limited Time!", 31 on hand), and 145 `deal_pages`. `{"deal": "price-drops", "sort": "ending_soon"}` read 13,173 items. An unknown slug is a charged `404` that lists the valid slugs.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def sweetwater(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/sweetwater/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. In-stock Boss reverb and delay pedals, lowest price first (1 credit)
cat = sweetwater("category", {"category": "c974", "sort": "price_asc",
                              "facets": {"Availability": ["In Stock"], "Brand": ["Boss"]}})["data"]
for it in cat["items"][:5]:
    print(it["item_id"], it["name"], it["price"], it["offer"], it["stock"])

# 2. Full product with price drop and stock text (1 credit)
p = sweetwater("product", {"item_id": cat["items"][0]["item_id"]})["data"]
print(p["price"], p["was_price"], p["price_drop"], p["stock_text"], p["estimated_by"])

# 3. Serial-numbered units of a guitar, lightest first (1 credit)
units = sweetwater("serial-units", {"item_id": "StratAU2HEUB"})["data"]["units"]
for u in sorted(units, key=lambda u: u["weight_lbs"] or 99):
    print(u["serial_number"], u["weight_lbs"])

# Prices and counts change: store each answer with fetched_at and run this on
# a schedule; that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `host`, `country`, `currency` and `language`.

- **search** - `query`, `landed_on` (search, category, product or page), `landed_url` (product or page), `category` {`id`, `name`, `url`}, `sort`, `page`, `total`, `total_pages`, `per_page`, `count`, `items[]` (search items {`position`, `item_id`, `name`, `brand`, `type`, `category`, `url`, `image`, `condition`, `price`, `retail_price`, `base_price`, `has_price_drop`, `instant_rebate`, `mail_in_rebate`, `bundle_savings`, `special_offer` {`title`, `value`}, `in_stock`, `on_hand`, `available`, `on_order`, `pre_order`, `special_order`, `free_shipping`, `open_box[]` {`item_id`, `condition`, `price`}, `rating`, `review_count`}, or category cards when `landed_on` is category), `facets`, `applied_facets` (category), `note`.
- **category** - `category` {`id`, `name`, `url`}, `breadcrumbs[]` {`name`, `url`}, `sort`, `site_sort`, `page`, `total` (at most 5,000), `total_pages`, `per_page`, `requested_facets`, `applied_facets`, `count`, `items[]` {`position`, `item_id`, `name`, `url`, `image`, `price`, `offer`, `rating`, `review_count`, `stock`, `open_box` {`item_id`, `price`, `text`}, `serial` {`number`, `weight`}, `bundle_savings_available`}, `facets[]` {`name`, `values[]` {`value`, `count`, `selected`}}.
- **product** - `item_id`, `requested`, `name`, `full_name`, `brand`, `mpn`, `type`, `category`, `breadcrumbs`, `url`, `condition`, `open_box`, `serial_number`, `price`, `currency`, `was_price`, `price_drop`, `instant_savings`, `new_price`, `availability`, `stock_text`, `estimated_by`, `warehouse_flags` {`fw`, `az`}, `ship_weight_lbs`, `free_shipping`, `return_days`, `rating`, `review_count`, `dimensions` {`height_in`, `width_in`, `depth_in`, `weight_lbs`}, `images`, `specs[]` {`name`, `value`}.
- **serial-units** - `item_id`, `requested`, `name`, `brand`, `condition`, `price`, `parent_item_id`, `parent_price`, `url`, `serial_sold`, `serial_reserved`, `open_box` {`item_id`, `condition`, `price`}, `count`, `units[]` {`position`, `serial_number`, `item_id`, `weight_lbs`, `url`, `photos[]` {`view`, `url`}}, `note`.
- **reviews** - `item_id`, `requested`, `name`, `brand`, `average_rating`, `total_reviews`, `star_percent`, `stars`, `sort`, `page`, `limit`, `total`, `total_pages`, `count`, `reviews[]` {`rating`, `title`, `text`, `date`}.
- **deals** - `deal`, `deal_name`, `sort`, `page`, `total`, `total_pages`, `per_page`, `sale_event` {`name`, `starts`, `ends`, `time_zone`}, `count`, `items[]` (search items), `deal_pages[]` {`slug`, `name`}.

## Guardrails

- Name it "Sweetwater (sweetwater.com, the US online music instrument and pro audio retailer)" on first mention. Sweetwater accounts, carts and Sales Engineer contacts are not read.
- Prices: quote `price` with `retail_price` or `was_price` where given, the offer text as written and the `fetched_at` date. Never present a price after a mail-in rebate as the price, and never compute a discount Sweetwater does not state.
- Stock: quote `on_hand`, `available` and `on_order` as Sweetwater's counts at the time of the call; `available` can be negative. Never promise that a unit will still be there.
- Serial units: a unit's weight is its shipping weight as given. Do not republish Sweetwater's unit photos; link the unit by its `url` instead.
- Search: free-text results are the 42 the site shows; never present them as every match. `total` is the site's count.
- Sale windows: `sale_event` times are as the page states them, with no time zone; say so when quoting an end time.
- Reviews: no reviewer names are returned. Quote a review as "a Sweetwater customer review".
- Not available: Gear Exchange used listings, store or showroom stock, search suggestions, price history (poll and store), carts or checkout. This API cannot reserve or buy an item.
- Terms: Scavio does not store Sweetwater data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Sweetwater's terms of use restrict automated access or commercial use of its site; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, unit counts, serial numbers, item ids, dates or ratings. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "query is required."; "Send exactly one of item_id (e.g. DD8) or url (a sweetwater.com/store/detail/ link)."; "item_id must be a Sweetwater item id: 2 to 40 letters, digits, '.', '_' or '-', e.g. DD8 or SM58 (items[].item_id)."; "url must be a Sweetwater product link: https://www.sweetwater.com/store/detail/<item id>--<name>."; "category is required: a Sweetwater category id (c590), path (c590--Solid_Body_Guitars) or link."; "deal must be a Deal Zone page slug, e.g. guitar-deals or price-drops (deal_pages[].slug of a deals answer)."; "facets: at most 12 facets."; a `sort` outside its list ("sort must be one of: ..."); a `page`, `stars` or `limit` outside its range.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Sweetwater has no item <id>.", "Sweetwater has no category <id>.", "Sweetwater has no Deal Zone page <slug>. deal_pages lists them: ...", "Nothing was found for this search.". Take item ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=sweetwater-api).
- `502` means Sweetwater data was temporarily unavailable ("Sweetwater is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.101.0
npm install scavio@0.102.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.sweetwater.search({ query: "boss delay pedal" });
const { data: list } = await scavio.sweetwater.category({ category: "c974", sort: "price_asc", facets: { Availability: ["In Stock"], Brand: ["Boss"] } });
const { data: pedal } = await scavio.sweetwater.product({ item_id: "DD8" });
const { data: units } = await scavio.sweetwater.serialUnits({ item_id: "StratAU2HEUB" });
const { data: reviews } = await scavio.sweetwater.reviews({ item_id: "SM58", stars: 5, sort: "newest" });
const { data: deals } = await scavio.sweetwater.deals({ deal: "price-drops", sort: "ending_soon" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.sweetwater.search(...)`, `category`, `product`, `serial_units`, `reviews` and `deals`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 6 endpoints as tools: `search_sweetwater`, `get_sweetwater_category`, `get_sweetwater_product`, `get_sweetwater_serial_units`, `get_sweetwater_reviews` and `get_sweetwater_deals`. Sweetwater is opt-in: add `sweetwater` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.101.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,sweetwater"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/sweetwater-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=sweetwater-api), [category](https://scavio.dev/docs/sweetwater-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=sweetwater-api), [product](https://scavio.dev/docs/sweetwater-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=sweetwater-api), [serial units](https://scavio.dev/docs/sweetwater-serial-units?utm_source=agent-skills&utm_medium=skill&utm_campaign=sweetwater-api), [reviews](https://scavio.dev/docs/sweetwater-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=sweetwater-api), [deals](https://scavio.dev/docs/sweetwater-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=sweetwater-api). Overview: [Sweetwater API](https://scavio.dev/sweetwater-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=sweetwater-api).
