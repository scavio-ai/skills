---
name: rei-api
description: REI API for REI (rei.com, the US outdoor co-op) - what outdoor gear costs at REI today and whether the REI stores near you have it for pickup, as REI shows it to a visitor who is not signed in (on 2026-11-26 the REI Co-op Half Dome 2 Tent with Footprint read $329 in 3 colors, each SKU with its own price, UPC and online status, REI's own estimate of a $32.90 (10%) co-op member reward, 365-day returns and 62 reviews at 4.23 stars; SKU 2437020001 was in stock for pickup at 8 of the 9 REI stores nearest Seattle ZIP 98101, Seattle Flagship 0.71 miles away first, and free shipping to Lynnwood) with the current price, compare-at price, percent off, REI's own savings text, sale, clearance and REI Outlet flags, Just for Members items flagged, dated promo flair (Sale Ends Dec 1), badges (Top Rated, Staff Pick, New arrival), colors and sizes with SKU ids; keyword search, category listings and the deals or REI Outlet listings (7,974 deals and 3,654 outlet items captured), 30 or 90 per page to page 400, in REI's 9 sorts and filtered by any facet (brand, price, rating, best use, features, size, color) and by one store; one product in full with features, specs, every SKU, the rating histogram, fit ratings and questions with answers; reviews 10 per page in 5 sorts with a star filter, verified, incentivized and syndicated flags and brand responses, without reviewer names; the store pickup status of one SKU (in stock, ship to store or unavailable, with REI's estimated arrival) at the 4-10 stores nearest a ZIP, a city and state or a point; the stores near a ZIP or point with upcoming special hours (Thanksgiving and
version: 1.0.0
tags: rei, rei-com, rei-co-op, rei-api, rei-prices, rei-price-tracker, rei-sale, rei-deals, rei-outlet, rei-clearance, rei-store-stock, rei-in-stock, rei-store-pickup, rei-stores, rei-store-hours, rei-reviews, rei-search, rei-product, rei-members, rei-member-reward, rei-optoutside, outdoor-gear, camping-gear, hiking-gear, backpacking, tents, rain-jackets, hiking-boots, ski-gear, climbing-gear, cycling, outdoor-retail, store-availability, store-pickup, sku-data, upc, product-reviews, product-search, category-browse, autocomplete, us-retail, usd, price-monitoring, competitor-research, agents, ai-agents, structured-data, json, mcp
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/rei-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api
---

# REI API - Outdoor Gear Prices, Store Pickup Stock, Reviews

Read REI (rei.com, the US outdoor co-op): keyword search, category listings, the deals and REI Outlet listings, one product in full with every SKU's price, UPC and online status, reviews, the store pickup status of one SKU at the REI stores near a ZIP, a city or a point, the stores near a ZIP or point, one store with hours, services and rentals, and search-term suggestions. www.rei.com only (US, USD, English), as shown to a visitor who is not signed in. Every endpoint returns structured JSON at 2 credits per call.

**The job this skill is for: REI gear prices and REI store pickup.** What a tent, jacket or pair of boots costs at rei.com today, whether it is on sale, clearance or in REI Outlet, and which REI stores near a ZIP have the exact size and color on the shelf. On 2026-11-26 the REI Co-op Half Dome 2 Tent with Footprint (product `243702`) read $329 in all 3 colors, each a SKU with its own price, UPC and `available` flag, with REI's own `member_reward_estimate` $32.90 ("10%", an estimate of the co-op member reward, not a member price), `return_days` 365 and 62 reviews at 4.23 stars (78% recommend). `/store-stock` for SKU `2437020001` (Earthen Gray) near ZIP 98101 listed 9 stores: 8 `in_stock` ("In stock at Seattle Flagship", 0.71 miles, estimated arrival 2026-11-28) and 1 `ship_to_store` ("Free shipping to Lynnwood", estimated 2026-12-01). The second job is deals: `/deals` read 7,974 items on sale or clearance and `{"type": "outlet"}` 3,654 REI Outlet items, each with REI's own "You save 26%" text and dated promo flair such as "Sale Ends Dec 1". Pair it with `dicks-sporting-goods-api`, `amazon-product-data` and `walmart-product-data` for the same brand item (match on UPC).

Eight limits shape every answer, so say them plainly:
- **2 credits per call.** Every endpoint is 2 credits, suggestions included. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`), a location REI cannot place (`400`) and an upstream failure (`502`, `503`) are not.
- **Store stock is a pickup flag per store, never a unit count.** `status` is `in_stock` (on the shelf, pick up), `ship_to_store` (free shipping to that store, not on the shelf) or `unavailable`, with REI's `status_text` and `estimated_arrival`. REI publishes no unit counts: never write how many a store has.
- **No member prices.** Prices are what rei.com shows a visitor who is not signed in, and REI shows no separate member price. `members_only` flags REI's "Just for Members" items (shown at their normal price; buying one needs a membership). `member_reward_estimate` is REI's own estimate of the co-op member reward on an item, as the page shows it: quote it as REI's estimate, never as a discount or a member price.
- **No used gear.** REI does not sell used gear online (Re/Supply is in its stores); none is listed. A store's `has_used_gear` and `has_trade_in` say which stores offer it in person.
- **Sale labels are REI's own.** `price` is the current price, `compare_at` and `regular_price` REI's compare-at price, `percent_off` the percent off, and `savings_text` REI's own wording ("You save 26%"). `price_type` is `regular`, `sale` or `outlet` on lists and `regular` or `clearance` per SKU. `flair` carries REI's dated promo text as given ("Sale Ends Dec 1").
- **Sizes and colors are SKUs.** Every color and size combination is a SKU with its own `sku_id`, price and online status (the Beta Jacket - Men's, `228617`, read 146 SKUs, 28 available online, $320 to $400). `/store-stock` takes one `sku_id`, so pick the size and color first.
- **No Black Friday page.** REI closes its stores on Black Friday (#OptOutside): store `events` and `holidays` show 2026-11-26 (Thanksgiving) and 2026-11-27 closed. Deals are the deals and outlet listings.
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

REI has no public API for reading its catalog, prices or store stock. Its affiliate programme runs on a third-party affiliate network with a daily product data feed for affiliates only (a links programme, not a price or stock API). Prices and store pickup are shown on rei.com for the store or location you pick, and this skill reads those public pages with one Scavio key.

REI reported fiscal 2025 net sales of $3.54B and more than 26 million members (REI newsroom, 2026-05-04); the rei.com store directory lists 193 US stores. Quote these with their source, never from the samples.

See also: for the same brand item at Dick's use `dicks-sporting-goods-api`; at Amazon `amazon-product-data`; at Walmart `walmart-product-data`; prices across retailers `google-shopping-api`; per-store stock at other retailers `home-depot-product-data`, `staples-ink-prices-api`.

## When to trigger

Use this skill when the user asks to:
- Price a tent, sleeping bag, rain jacket, boots, skis or a bike at REI, with REI's compare-at price, percent off and its own savings text
- Check whether the REI stores near a ZIP, a city or a point have one size and color for pickup, will ship it free to the store, or do not have it
- Search rei.com by keyword, sorted by price, newest, top rated, best selling or percent off, or filtered by brand, price, rating, best use, features, size or color
- List an REI category (tents, mens-rain-jackets, camping-and-hiking) or only the items a given REI store shows as available
- List REI's deals (sale and clearance) or REI Outlet, for everything or one category, with the dated "Sale Ends" text
- Read one REI product in full: features, specs, every SKU with price, UPC and online status, the rating histogram, fit ratings and questions with answers
- Read REI reviews (10 per page, by stars, newest or most helpful) with verified, incentivized and syndicated flags and brand responses
- Find the REI stores near a ZIP or point with this week's special hours, or one store's hours, holidays, services (bike shop, ski shop, used gear, trade-in), rentals and departments
- Get REI's search-term suggestions for a partial query

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Calls usually take 3-20 seconds (in the captures: search, category and deals 1-5, a product 5-11, reviews 2-7, store stock 2-7, stores and store 1-6). Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/rei/search` | Keywords: 30 or 90 items per page with total, price, compare-at price, percent off, sale, clearance and outlet flags, badges, flair, colors and sizes with SKU ids, facets and categories | 2 |
| `POST /api/v1/rei/category` | One category by slug or link, sorted and filtered like search, with its child categories and counts | 2 |
| `POST /api/v1/rei/deals` | REI's deals (sale and clearance) or REI Outlet, optionally one category, sorted and filtered like search | 2 |
| `POST /api/v1/rei/product` | One product by id or link: features, specs, every SKU (price, compare-at, price type, savings, UPC, online status), member reward estimate, return days, rating histogram, fit ratings, questions and answers | 2 |
| `POST /api/v1/rei/reviews` | Reviews of one product, 10 per page, 5 sorts, a star filter, with verified, incentivized and syndicated flags and brand responses; no reviewer names | 2 |
| `POST /api/v1/rei/store-stock` | One SKU's pickup status (in stock, ship to store, unavailable) and estimated arrival at the 4-10 REI stores nearest a ZIP, a city and state or a point, with each store's record | 2 |
| `POST /api/v1/rei/stores` | The REI stores near a ZIP or point, by distance, with upcoming special hours | 2 |
| `POST /api/v1/rei/store` | One store by number: address, phone, hours, holidays, services, rentals, departments | 2 |
| `POST /api/v1/rei/suggestions` | REI's search-term suggestions for a partial query | 2 |

US only: there is no `country` parameter.

## Prices: compare-at price, percent off, sale, clearance and outlet

Every listed item carries:

| Field | Meaning |
|---|---|
| `price`, `price_max` | The current price, and the top of the range when sizes or colors differ (`price_display` `single` or `range`) |
| `compare_at`, `regular_price` | REI's compare-at price, given on items with a reduced price ($279 on the Marmot Tungsten 2-Person Tent with Footprint, `C12187`, at $204.97) |
| `percent_off`, `savings_text` | The percent off (26.54 on `C12187`) and REI's own text ("You save 26%") |
| `price_text` | The price as REI writes it ("$99.95") |
| `price_type` | `regular`, `sale` or `outlet` |
| `sale`, `clearance`, `partial_clearance`, `outlet` | REI's flags; `partial_clearance` means some SKUs are on clearance |
| `members_only` | REI's "Just for Members" badge |
| `badges`, `flair` | REI Outlet, Top Rated, Staff Pick, New arrival, Just for Members; dated promo text as given ("Sale Ends Dec 1") |

Per SKU (product): `price`, `compare_at`, `price_type` (`regular` or `clearance`), `savings_percent`, `savings_amount`, `available`, `status`, `upc`, `members_only`, `new_arrival`, `store_pickup_only`. The product's `price` is {`min`, `max`, `compare_at_min`, `compare_at_max`, `currency`}.

- Quote "$204.97 at rei.com on 2026-11-26 (REI Outlet, compare at $279, 'You save 26%')", with the date. Use REI's `savings_text` for the rounded percent.
- Quote a size or color's price from `skus[]`, not the product range, when the user names one.
- Report REI's labels, the flair date and the arithmetic only. Never judge a compare-at price or a discount, never describe how often an item is on sale, and never present `member_reward_estimate` as a lower price.

## Workflow

1. **Find the product.** `/search` with `query` (`rain jacket`), or `/category` with a `slug` (`tents`, from `categories[].slug` or `breadcrumbs[].slug`), or `/deals`. Each item's `product_id` is the input of product and reviews; `sizes[].skus[].sku_id` (and `colors[].sample_sku`) the input of store-stock.
2. **Read it in full.** `/product` with `product_id` (`243702`, `C09719`) or an rei.com product `url`: every SKU with color, size, price, UPC and online `available`.
3. **Pick the SKU.** Match the user's size and color in `skus[]` and take its `sku_id`.
4. **Pickup near a place.** `/store-stock` with `sku` and one of `zip`, `city` + `state`, or `latitude` + `longitude`. Read `status` and `estimated_arrival` per store, and `in_stock_count` / `ship_to_store_count`.
5. **Only what one store has.** Pass `store` (a `store_number` from stores or store-stock) on search, category or deals: the list keeps only items REI shows as available at that store, and `store_filter` reports the store and its count. Then confirm the exact SKU with `/store-stock`.
6. **Narrow a list.** `sort`, `page_size` (30 or 90), `page` and `facets` (keys and values exactly as an earlier answer gives them in `facets[].key` and `facets[].values[].value`, up to 10 keys; a list of values is OR-ed).
7. **Reviews.** `/reviews` with `product_id`, `sort`, `page` and `rating` (one star value or a list such as `[1, 2]` for the critical reviews; `total` then counts the matching reviews and `total_reviews` all of them).
8. **Stores.** `/stores` with `zip` or `latitude` + `longitude` (and `limit`, `radius`); `/store` with `store_number` for full hours, holidays, services and rentals.
9. **Watching prices or pickup:** there is no history. Poll the same SKUs on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`), deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Keywords, 1-200 chars |
| `slug` | string | category: one of | A category slug (`tents`, `mens-rain-jackets`): `categories[].slug`, `breadcrumbs[].slug`, the part after /c/ in an rei.com link |
| `url` | string | category: one of | An rei.com category link; its query string is not read (send filters in `facets`) |
| `type` | string | `deals` | Deals: `deals` (everything on sale or clearance) or `outlet` (REI Outlet) |
| `category` | string | none | Deals: a category slug, to limit the deals to one category |
| `sort` | string | `relevance` | `relevance` (REI's Best Match), `brand_a_z`, `brand_z_a`, `price_asc`, `price_desc`, `newest`, `top_rated`, `best_selling`, `percent_off` |
| `facets` | object | none | {`facets[].key`: `values[].value` or a list of values}, up to 10 keys: `{"brand": "patagonia"}`, `{"price": "$20.00 to $49.99"}`, `{"average-rating": "4 to 5"}`, `{"category": "womens-clothing|womens-jackets"}` |
| `store` | string or integer | none | A `store_number`: only items REI shows as available at that store |
| `page` | integer | 1 | 1-400; `total_pages` reports the last one |
| `page_size` | integer | 30 | 30 or 90 |

### Product (`/product`) and reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | The REI product id (`243702`, `C09719`: `items[].product_id`) |
| `url` | string | one of | An rei.com product link, instead of `product_id` (not both) |
| `sort` | string | `relevance` | Reviews: `relevance`, `most_helpful`, `newest`, `highest_rating`, `lowest_rating` |
| `page` | integer | 1 | Reviews: 1-1000, 10 per page |
| `rating` | integer or array | none | Reviews: 1-5, or a list such as `[1, 2]` |

### Store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | required | A SKU id (`2437020001`): product `skus[].sku_id` or `items[].sizes[].skus[].sku_id` |
| `zip` | string or integer | one of | A US ZIP code (`98101`) |
| `city`, `state` | string | one of | A US city with its 2-letter state (`Portland`, `OR`) |
| `latitude`, `longitude` | number | one of | A point; pass exactly one of zip, city + state, or latitude + longitude |

### Stores (`/stores`), store (`/store`), suggestions (`/suggestions`)

`/stores` takes `zip` or `latitude` + `longitude` (not both), `limit` (1-10, default 10) and `radius` (miles, 1-250, default 100); a place with no store in range answers an empty list. `/store` takes `store_number` (required, `18` for Denver Flagship). `/suggestions` takes `query` (1-100 chars) and `limit` (1-50, default 10).

## Examples

### Pickup status of one SKU at the stores near a ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/rei/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "2437020001", "zip": "98101"}'
```

Captured `data` (2026-11-26; 2 of 9 stores shown; each store's `hours`, `holidays`, `services`, `rentals`, `departments`, `phone_alt`, `time_zone`, `url`, `opened` and status flags other than `open` dropped):

```json
{
  "sku": "2437020001",
  "location": { "zip": "98101" },
  "count": 9,
  "in_stock_count": 8,
  "ship_to_store_count": 1,
  "stores": [
    {
      "status": "in_stock",
      "status_text": "In stock at Seattle Flagship",
      "fulfillment_type": "PICK",
      "service_level": "BOPUS",
      "estimated_arrival": "2026-11-28T22:00:00Z",
      "store": {
        "store_number": "11",
        "name": "Seattle Flagship",
        "type": "FLAGSHIP",
        "address": { "street": "222 Yale Ave N", "city": "Seattle", "state": "WA", "zip": "98109", "country": "US" },
        "phone": "2062231944",
        "latitude": 47.6203,
        "longitude": -122.3299,
        "distance_miles": 0.71,
        "open": true,
        "curbside": true,
        "has_rentals": true,
        "has_bike_shop": true,
        "has_ski_shop": true,
        "has_used_gear": true,
        "has_trade_in": true
      }
    },
    {
      "status": "ship_to_store",
      "status_text": "Free shipping to Lynnwood",
      "fulfillment_type": "PICK",
      "service_level": "RSPU",
      "estimated_arrival": "2026-12-01T19:00:00Z",
      "store": {
        "store_number": "35",
        "name": "Lynnwood",
        "type": "SATELLITE",
        "address": { "street": "19500 Alderwood Mall Parkway, Suite 110", "city": "Lynnwood", "state": "WA", "zip": "98036", "country": "US" },
        "phone": "4256406200",
        "latitude": 47.8210714,
        "longitude": -122.271511,
        "distance_miles": 14.83,
        "open": true,
        "curbside": true,
        "has_rentals": false,
        "has_bike_shop": true,
        "has_ski_shop": true,
        "has_used_gear": true,
        "has_trade_in": true
      }
    }
  ],
  "notes": [
    "status is REI's pickup flag per store: in_stock (on the shelf, pick up), ship_to_store (free shipping to that store, not on the shelf) or unavailable. REI publishes no unit counts.",
    "estimated_arrival is REI's own estimate for pickup at that store, as given."
  ]
}
```

The other seven stores were Bellevue (6.79 miles), Southcenter/Tukwila, Issaquah, Silverdale, Tacoma, Olympia and Bellingham (77.72 miles), all `in_stock`. `{"sku": "2286170003", "city": "Denver", "state": "CO"}` (a Beta Jacket SKU) answered 8 stores, 4 in stock and 4 ship to store; `{"sku": "2437020001", "latitude": 30.2672, "longitude": -97.7431}` (Austin) answered 4 stores, Austin Downtown first as `ship_to_store` with an estimated arrival of 2026-12-09. A location REI cannot place is an unbilled `400`: "REI could not place this location. Check the ZIP, city + state or coordinates."

### One search result with its SKUs

```bash
curl -X POST https://api.scavio.dev/api/v1/rei/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "rain jacket"}'
```

Captured `data.items[0]` (2026-11-26; `total` 285, 10 pages of 30, 19 facets; `colors` cut to 2 of 6, `sizes` to 1):

```json
{
  "position": 1,
  "product_id": "227570",
  "name": "Rainier Rain Jacket - Men's",
  "brand": "REI Co-op",
  "url": "https://www.rei.com/product/227570/rei-co-op-rainier-rain-jacket-mens",
  "image": "https://www.rei.com/media/product/227570",
  "rating": 4.14,
  "review_count": 466,
  "price": 99.95,
  "price_max": 99.95,
  "compare_at": null,
  "regular_price": 99.95,
  "percent_off": null,
  "savings_text": null,
  "price_text": "$99.95",
  "price_type": "regular",
  "price_display": "single",
  "currency": "USD",
  "sale": false,
  "clearance": false,
  "partial_clearance": false,
  "outlet": false,
  "members_only": false,
  "available": true,
  "online_only": false,
  "badges": [],
  "flair": [],
  "attributes": [],
  "colors": [
    { "color_id": "321", "name": "BLACK", "family": "Black", "sample_sku": "2275700007", "available": true, "image": "https://www.rei.com/media/809cfab2-7ec3-4832-bfcf-5f7528bce2cf" },
    { "color_id": "193621", "name": "MIDNIGHT NAVY/SARAGASSO SEA", "family": "Blue", "sample_sku": "2275700029", "available": true, "image": "https://www.rei.com/media/6c95f983-fc9b-4dcc-97fd-f358cd2c363c" }
  ],
  "sizes": [
    { "size": "XS", "available": true, "skus": [{ "color_id": "321", "sku_id": "2275700087" }, { "color_id": "193621", "sku_id": "2275700088" }] }
  ]
}
```

The second result was the Patagonia Torrentshell 3L Jacket - Men's (`215514`) at $189.00 with a "Staff Pick" badge. Every `sku_id` under `sizes[].skus[]` goes straight into `/store-stock`. `{"query": "tent", "store": "18", "facets": {"brand": "big-agnes"}}` answered the 29 Big Agnes tents REI showed as available at Denver Flagship (`store_filter` Denver Flagship, 29).

### Product, category, deals, reviews, stores, store and suggestions

- `/product` `{"product_id": "243702"}`: Half Dome 2 Tent with Footprint, `brand` REI Co-op, `price` {`min` 329, `max` 329}, 3 SKUs all available (Earthen Gray `2437020001`, UPC 424370200011; Golden Sulphur `2437020002`; Stone Green), `member_reward_estimate` {`amount` 32.9, `percent_text` "10%"}, `return_days` 365, `review_summary` 62 reviews, 4.23 average, histogram {5: 43, 4: 6, 3: 4, 2: 2, 1: 7}, 78% recommend, a "Setup" fit rating of 1.44 on a Very Easy to Difficult scale, and 32 questions with answers (no author names). `{"product_id": "C09719"}` (Rambler Stackable Mug - 14 fl. oz.) read $40 with `members_only` `true`. An unknown id is a charged `404`: "No REI product with this id."
- `/category` `{"slug": "tents"}`: `total` 522, 18 pages; the first item, the Marmot Tungsten 2-Person Tent with Footprint (`C12187`), read $204.97, compare at $279, "You save 26%", `price_type` `outlet`, badges REI Outlet and Top Rated. `categories` holds the child categories with counts. An unknown slug is a charged `404`: "No REI category with this slug."
- `/deals` `{}`: 7,974 items on sale or clearance (266 pages), with flair such as "Sale Ends Nov 30"; `{"type": "outlet"}` 3,654 REI Outlet items, the first Smartwool Everyday Multi-Stripe Crew Socks - Women's at $18.73 (compare at $24, "You save 21%"); `{"category": "tents", "sort": "percent_off"}` 102 items.
- `/reviews` `{"product_id": "228617", "rating": [1, 2]}` (Beta Jacket - Men's): `total` 25 matching of `total_reviews` 179, 3 pages; the first, 1 star, "Some spots are not waterproof", was `syndicated` from arcteryx.com with 6 photos and a Customer Service `brand_responses` entry from arcteryx.com. No reviewer names, ids or locations; staff and reviewer names are taken out of brand responses.
- `/stores` `{"zip": "80202"}`: 8 stores within 100 miles, Denver Flagship (store 18, 0.66 miles, 10,301 products) first, then Lakewood, Greenwood Village, Boulder, Loveland, Fort Collins, Dillon and Colorado Springs, each with `events` such as "#OptOutside" (2026-11-27 closed). A ZIP is placed at its US Census centroid.
- `/store` `{"store_number": "18"}`: Denver Flagship, 1416 Platte St, Denver, CO 80202, opened 1983-03-01, services Bike Shop, gear repair, Ski Shop, Used Gear and Trade-in, 7 rental categories (paddling, cross-country ski, snowshoes, bear canisters, climbing, backcountry snow, camping and hiking), 15 departments, normal, curbside and dated special hours, and `holidays` 2026-11-26, 2026-11-27 and 2026-12-25. An unknown number is a charged `404`: "No REI store with this number."
- `/suggestions` `{"query": "tent"}`: tent stakes, tent footprints, tent heaters, tent accessories, ... (10); `{"query": "pata"}`: patagonia, patagonia black hole, patagonia r1, ...

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def rei(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/rei/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Tents on sale, deepest percent off first (2 credits)
deals = rei("deals", {"category": "tents", "sort": "percent_off"})["data"]
for i in deals["items"][:5]:
    print(i["product_id"], i["name"], i["price"], i["compare_at"], i["savings_text"], i["flair"])

# 2. One product: pick the SKU for a color (2 credits)
p = rei("product", {"product_id": "243702"})["data"]
sku = next(s for s in p["skus"] if s["color"]["label"] == "Earthen Gray")
print(p["name"], sku["sku_id"], sku["price"], sku["upc"], sku["available"])

# 3. Pickup status of that SKU near a ZIP (2 credits). Flags, not unit counts.
stock = rei("store-stock", {"sku": sku["sku_id"], "zip": "98101"})["data"]
for s in stock["stores"]:
    print(s["store"]["name"], s["store"]["distance_miles"], s["status"], s["estimated_arrival"])

# Prices and pickup status can change between calls. Store each answer with
# fetched_at and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it; the suggestions term list is the one exception, refreshed at most once a day. Every `data` carries `notes`.

- **item** (search, category, deals) - `position`, `product_id`, `name`, `brand`, `url`, `image`, `rating`, `review_count`, `price`, `price_max`, `compare_at`, `regular_price`, `percent_off`, `savings_text`, `price_text`, `price_type`, `price_display`, `currency`, `sale`, `clearance`, `partial_clearance`, `outlet`, `members_only`, `available`, `online_only`, `badges`, `flair`, `attributes`, `colors[]` {`color_id`, `name`, `family`, `sample_sku`, `available`, `image`}, `sizes[]` {`size`, `available`, `skus[]` {`color_id`, `sku_id`}}.
- **lists** - `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `sort`, `title`, `items[]`, `facets[]` {`key`, `title`, `multi_select`, `values[]` {`value`, `label`, `count`, `selected`}}, `categories[]` {`slug`, `label`, `count`, `value`, `selected`, `children`}, `breadcrumbs`, `store_filter`, `filters_applied`, `store`. Search adds `query`; category `slug`, `url`; deals `type`, `category`, `url`.
- **product** - `product_id`, `name`, `brand` {`name`, `slug`, `url`}, `url`, `description`, `features`, `specs[]` {`name`, `values`}, `featured_specs`, `breadcrumbs[]` {`name`, `slug`}, `primary_category`, `price` {`min`, `max`, `compare_at_min`, `compare_at_max`, `currency`}, `outlet`, `badges`, `flair`, `members_only`, `any_members_only`, `member_reward_estimate` {`amount`, `percent_text`, `currency`}, `return_days`, `ships`, `colors[]` {`code`, `name`, `label`, `family`}, `sizes`, `images[]` {`url`, `title`, `color_code`}, `sku_count`, `available_sku_count`, `skus[]` {`sku_id`, `color`, `size`, `available`, `status`, `sellable`, `price`, `compare_at`, `price_type`, `savings_percent`, `savings_amount`, `currency`, `upc`, `members_only`, `new_arrival`, `store_pickup_only`}, `review_summary` {`count`, `average_rating`, `histogram`, `recommended_percent`, `recommended`, `not_recommended`, `ratings_only_count`, `top_rated`, `fit[]` {`id`, `label`, `average`, `range`, `min_label`, `max_label`}}, `question_count`, `questions[]` {`question_id`, `question`, `submitted_at`, `answer_count`, `answers[]` {`answer`, `is_brand_answer`, `submitted_at`, `helpful_votes`}}.
- **reviews** - `product_id`, `page`, `page_size`, `sort`, `rating_filter`, `total`, `total_reviews`, `total_pages`, `has_more`, `count`, `reviews[]` {`review_id`, `rating`, `title`, `text`, `submitted_at`, `modified_at`, `would_recommend`, `ratings_only`, `featured`, `helpful_votes`, `unhelpful_votes`, `badges`, `verified_purchaser`, `incentivized`, `syndicated`, `syndicated_from`, `fit[]` {`label`, `value`, `value_label`}, `reviewer_context`, `purchased_size`, `date_of_use`, `additional_fields`, `photo_count`, `brand_responses[]` {`department`, `response`, `date`, `source`}, `original_product_name`}.
- **store-stock** - `sku`, `location`, `count`, `in_stock_count`, `ship_to_store_count`, `stores[]` {`status`, `status_text`, `fulfillment_type`, `service_level`, `estimated_arrival`, `store` (the store record below, with `distance_miles`)}.
- **stores** - `origin` {`latitude`, `longitude`, `zip`}, `radius_miles`, `count`, `stores[]` {`store_number`, `name`, `type`, `address` {`street`, `city`, `state`, `zip`, `country`}, `phone`, `phone_alt`, `latitude`, `longitude`, `distance_miles`, `url`, `open_for_shopping`, `curbside_pickup`, `product_count`, `events[]` {`type`, `title`, `starts`, `hours[]` {`days`, `date`, `open`, `close`, `closed`}}}.
- **store** - `store_number`, `name`, `type`, `address`, `phone`, `phone_alt`, `latitude`, `longitude`, `distance_miles`, `time_zone`, `url`, `opened`, `open`, `opening_soon`, `recently_opened`, `temporarily_closed`, `permanently_closed`, `curbside`, `has_rentals`, `has_bike_shop`, `has_ski_shop`, `has_used_gear`, `has_trade_in`, `services[]` {`key`, `name`}, `rentals[]`, `rentals_reservation_url`, `departments[]`, `hours[]` {`event`, `type` (`NormalHours`, `CurbsideHours`, `SpecialHours`), `hours[]` {`days`, `date`, `open`, `close`, `closed`}}, `holidays[]` {`date`, `day`}.
- **suggestions** - `query`, `count`, `suggestions[]` {`term`, `top_products_available`}.

## Guardrails

- Name it "REI (rei.com, the US outdoor co-op)" on first mention. REI member accounts are not read.
- Prices: quote `price` with REI's `compare_at` and `savings_text`, the SKU when a size or color is named, and the `fetched_at` date. Prices are what a visitor who is not signed in sees; never call any price a member price.
- `member_reward_estimate` is REI's own estimate of the co-op member reward, as the page shows it: never present it as a discount or a lower price.
- Store stock: report `status`, `status_text` and `estimated_arrival` per store as REI gave them at the moment of the call; Scavio makes no promise of their accuracy. Never state or estimate a unit count, and never promise pickup.
- Report REI's labels (compare-at price, savings text, flair dates, badges) and the arithmetic only. Never judge a discount or a sale deadline, and never describe how often an item is on sale.
- Comparing REI with Dick's, Amazon or Walmart: compare only the same item (same UPC), each with its date. REI Co-op items have no same item elsewhere: label them as different products. Never call one retailer cheaper beyond the numbers shown.
- Reviews: no reviewer names, ids or locations are returned. Syndicated reviews were written on the brand's own site (`syndicated_from`); say so when quoting one.
- Not available: unit counts, member prices, used gear (REI sells it only in its stores), a Black Friday page (REI's stores close that day), price history (poll and store), rentals booking, cart or checkout. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not collect or store REI data: each call fetches the public REI page at the moment the request asks for it and returns what it shows as JSON, with no response cache (the suggestions term list is refreshed at most once a day). REI's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish REI product photos or logos; link products by `url` instead.
- Never fabricate prices, SKU ids, product ids, store numbers, hours, pickup statuses, dates or ratings. Only return what the API returned, with the `fetched_at` time and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "slug or url is required", "product_id or url is required", "Pass product_id or url, not both."; a `product_id` that is not an REI product id ("product_id must be an REI product id (items[].product_id, e.g. 243702 or C09719)."); a `sku` that is not an REI SKU id; a `url` that is not an rei.com product or category link; "page_size must be 30 or 90 (the two page sizes REI offers)."; `facets` that are not an object, more than 10 keys or 10 values, or `stores` sent as a facet ("Filter by store with the store parameter (a store_number), not facets."); a `store` or `store_number` that is not an REI store number; store-stock with none or more than one of zip, city + state, latitude + longitude ("Pass one of zip, city + state, or latitude + longitude."), a city without a state, an unknown ZIP ("zip <zip> is not a known US ZIP code."); a location REI cannot place ("REI could not place this location. Check the ZIP, city + state or coordinates."); an unknown `sort` or `type`; a `page`, `limit` or `radius` outside its range.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No REI product with this id.", "No REI category with this slug.", "No REI deal listing for this category.", "No REI results for this query.", "No REI stock answer for this SKU.", "No REI store with this number.". Take product ids, SKU ids, slugs and store numbers from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api).
- `502` means REI data was temporarily unavailable ("REI is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means REI is busy ("REI is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.99.0
npm install scavio@0.100.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.rei.search({ query: "rain jacket", sort: "top_rated" });
const { data: tents } = await scavio.rei.category({ slug: "tents", facets: { brand: "big-agnes" } });
const { data: outlet } = await scavio.rei.deals({ type: "outlet", category: "tents" });
const { data: tent } = await scavio.rei.product({ product_id: "243702" });
const { data: critical } = await scavio.rei.reviews({ product_id: "228617", rating: [1, 2] });
const { data: pickup } = await scavio.rei.storeStock({ sku: "2437020001", zip: "98101" });
const { data: near } = await scavio.rei.stores({ zip: "80202" });
const { data: denver } = await scavio.rei.store({ store_number: "18" });
const { data: typed } = await scavio.rei.suggestions({ query: "tent" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.rei.search(...)`, `category`, `deals`, `product`, `reviews`, `store_stock`, `stores`, `store` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 9 endpoints as tools: `search_rei`, `get_rei_category`, `get_rei_deals`, `get_rei_product`, `get_rei_reviews`, `get_rei_store_stock`, `get_rei_stores`, `get_rei_store` and `get_rei_suggestions`. REI is opt-in: add `rei` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.99.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,rei"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/rei-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api), [category](https://scavio.dev/docs/rei-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api), [deals](https://scavio.dev/docs/rei-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api), [product](https://scavio.dev/docs/rei-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api), [reviews](https://scavio.dev/docs/rei-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api), [store stock](https://scavio.dev/docs/rei-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api), [stores](https://scavio.dev/docs/rei-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api), [store](https://scavio.dev/docs/rei-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api), [suggestions](https://scavio.dev/docs/rei-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api). Overview: [REI API](https://scavio.dev/rei-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rei-api).
