---
name: ashley-furniture-api
description: "Ashley Furniture API for Ashley sale prices and product data: keyword search (48 per page, exact total, sorted by best sellers, price, newest, customer rating or name) and category and deal grids (30 per page, filtered by facet or price range) with price, Ashley's Regular Price (its struck-through price), discount, sale, clearance, doorbuster, outlet and hot buy badges, rating, review count and stock; one product in full by item number or link with every option and variant, set components, dimensions, materials, assembly, stock and delivery, the nearest store, the rating histogram, the first 10 reviews, customer photos and customer Q&A with staff answers; the Black Friday, clearance and Hot Buys deal grids; stores near a latitude and longitude and one store's address, phone and hours. Ashley prices vary by region: every US answer reports priced_for, the ZIP and price zone Ashley priced it for (no ZIP input). ashleyfurniture.com (USD), plus search and product on Ashley's licensed storefronts ashleyhomestore.ca (CAD), Mexico (MXN, Spanish), the Philippines (PHP), Saudi Arabia (SAR) and Turkey (TRY, Turkish). 6 endpoints, 2 credits per call on us and mx, 1 on ca, ph, sa and tr. No price history, review paging or ZIP store search. Ashley's official API is for its dealers (wholesale pricing); Ashley publishes no public shopper-price API."
version: 1.0.0
tags: ashley, ashley-furniture, ashley-furniture-api, ashley-homestore, ashley-furniture-prices, ashley-furniture-sale, ashley-regular-price, ashley-black-friday, ashley-clearance, ashley-hot-buys, ashley-reviews, ashley-stores, ashley-canada, ashley-mexico, furniture, furniture-prices, home-furnishing, price-monitoring, price-tracking, product-search, product-data, product-reviews, category-browse, store-locator, retail, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/docs/ashley-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api
---

# Ashley Furniture API - Prices, Sale and Regular Price, Reviews, Stores

Read Ashley Furniture product data on ashleyfurniture.com: keyword search, category grids with Ashley's own sorts and filters, one product in full by item number or link (options, variants, set components, dimensions, stock, the nearest store, the rating histogram, the first 10 reviews and customer Q&A), the Black Friday, clearance and Hot Buys deal grids, stores near a point and one store's address, phone and hours. Search and product also read Ashley's licensed storefronts in Canada, Mexico, the Philippines, Saudi Arabia and Turkey. All 6 endpoints return structured JSON; a call costs 2 credits on `us` and `mx` and 1 credit on `ca`, `ph`, `sa` and `tr`.

**The job this skill is for: Ashley Furniture sale prices.** Every US item carries `price` (what Ashley charges now) next to `regular_price` (Ashley's own "Regular Price", the struck-through price) and `discount_percent` computed from the two. Ashley's Terms and Conditions define it: "Regular Price is our highest advertised price in store and online. Regular Price is offered to customers using special long-term financing." So a percent off against `regular_price` is not a measured price drop. To see whether a price really fell, read the same item on a schedule, store each reading with its time and its `priced_for`, and compare runs. Black Friday 2026 is November 27.

**Region pricing: every answer says where it was priced.** Ashley prices vary by region. Its ZIP page says "Update your ZIP code for product availability, pricing, and delivery in your area." The API does not let you choose the ZIP: every US answer returns `priced_for` {`zipcode`, `price_zone`}, the ZIP and price zone Ashley priced that answer for. The Mahoney Sofa, item 3100438, read on 2026-11-14 through these endpoints:

| `priced_for.zipcode` | `priced_for.price_zone` | `price` | `regular_price` | `badges.sale` | Endpoint |
|---|---|---|---|---|---|
| 30236 | AFHSPGZ4 | USD 299.99 | USD 349.99 | true | search "sofa" |
| 62650 | AFHSPGZ12 | USD 449.99 | USD 449.99 | false | category sofas |
| 23834 | AFHSPGZ5 | USD 499.99 | USD 549.99 | true | category sofas |

The same item was on sale in two zones and not in the third. Two calls can land in different zones, so compare a price only with earlier readings in the same `price_zone`.

Ashley's official API, the Product Syndication API on its developer portal, is for authorized Ashley dealers: it needs AshleyDirect credentials, an approved Ashley customer account and a Client ID from Ashley, and it returns that account's wholesale pricing, not the prices shoppers see. Ashley publishes no public API for ashleyfurniture.com shopper prices, sale prices or reviews.

See also: for Wayfair prices and the was price use `wayfair-api`; for IKEA prices by country use `ikea-api`; for home-improvement prices by store use `home-depot-product-data`, `lowes-product-data` or `menards-product-data`; for the cross-retailer view of one product use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Check Ashley Furniture sale prices: the current price next to Ashley's Regular Price, and what Regular Price means
- Track Ashley prices through Black Friday and Cyber Monday (poll and store price, regular price, badges and the price zone)
- Compare an Ashley item's price across Ashley's price zones, or find out which ZIP and price zone an answer was priced for
- Search Ashley Furniture by keyword, sorted by best sellers, price, newest, customer rating or name
- Browse an Ashley category (sofas, sectionals, beds, mattresses) filtered by a facet (design, color, size) or a price range
- List the products in Ashley's Black Friday, clearance or Hot Buys deals
- Read one Ashley product in full by item number or link: options, variants, set components, dimensions, materials, stock, delivery, nearest store
- Read Ashley reviews (the first 10 on the page, plus the rating histogram), customer photos and customer Q&A with staff answers
- Find Ashley stores near a location and read a store's address, phone and opening hours
- Search or read products on Ashley HomeStore Canada (CAD), Ashley Mexico (MXN, Spanish), the Philippines (PHP), Saudi Arabia (SAR) or Turkey (TRY, Turkish)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits: 25 calls on `us` or `mx`, 50 on `ca`, `ph`, `sa` or `tr`.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In build testing, US calls took 1.7 to 6 seconds; licensee storefront calls took 0.7 to 54 seconds (Turkey search 21 to 34 seconds, Saudi Arabia search up to 54). A failed attempt is retried once, so a slow call can take up to about 2 minutes. Set a client timeout of at least 150 seconds and do not fire many calls at once.

| Endpoint | Markets | Credits | What it returns |
|---|---|---|---|
| `POST /api/v1/ashley/search` | `us`, `ca`, `mx`, `ph`, `sa`, `tr` | us 2, mx 2, ca / ph / sa / tr 1 | us: 48 results per page with the exact total, sorts and informational facets; per item price, regular price, discount, badges, rating, review count and every variant with its own price. Licensee markets: the storefront's best matches (up to 10; tr its first results page of 36) with `handle` for product |
| `POST /api/v1/ashley/product` | `us`, `ca`, `mx`, `ph`, `sa`, `tr` | us 2, mx 2, ca / ph / sa / tr 1 | us (by `sku` or `url`): prices, badges, options, variants, set components, dimensions, materials, assembly, images, breadcrumbs, stock and delivery, nearest store, rating, rating histogram, the first 10 reviews, customer photos and Q&A. Licensee markets (by `handle` or `url`): prices, availability, description, options, variants with barcode, images |
| `POST /api/v1/ashley/category` | `us` | 2 | One category's grid by `path` or `category_url`: 30 per page, sorted, filtered by facet or price range, with facets and counts |
| `POST /api/v1/ashley/deals` | `us` | 2 | One deal event's grid: `black_friday` (default), `clearance` or `hot_buys`, with the category sorts and filters |
| `POST /api/v1/ashley/stores` | `us` | 2 | Stores near `lat` / `lng` within `radius` miles: `store_id`, `name`, `url` per store |
| `POST /api/v1/ashley/store` | `us` | 2 | One store by `store_id` or `url`: address, phone, coordinates, hours per day, payment accepted, services, rating, map link |

## Markets

Search and product take `country` (lowercase, default `us`). Category, deals, stores and store are `us` only: any other `country` answers `400` before anything is charged. Prices come in the market's currency and are never converted. Every `data` echoes `country`, `language`, `currency` and `source_domain`.

| `country` | Storefront | Currency | Language | Endpoints | Credits |
|---|---|---|---|---|---|
| `us` | ashleyfurniture.com | USD | English | all 6 | 2 |
| `ca` | ashleyhomestore.ca | CAD | English | search, product | 1 |
| `mx` | store.ashleyfurniture.com.mx | MXN | Spanish | search, product | 2 |
| `ph` | store.ashleyfurniture.ph | PHP | English | search, product | 1 |
| `sa` | store.ashley.sa | SAR | English | search, product | 1 |
| `tr` | ashleyturkiye.com | TRY | Turkish | search, product | 1 |

`ca`, `mx`, `ph`, `sa` and `tr` are Ashley's licensed storefronts, separate sites with their own catalogues and prices. There is no `language` parameter: each storefront answers in its own language (Spanish names on `mx`, Turkish on `tr`). Quote names as returned and translate them for the user only in your own words around the data. `priced_for` is a US field; the licensee storefronts carry no price zone.

## Workflow

1. **Find products:** `/search` with `query` (US: add `sort`, page with `page`). Read `items[].sku` for `/product`. Search `facets` are informational: to filter, use `/category`.
2. **Browse and filter:** `/category` with `path` (the part after `/c/` in a category URL, for example `furniture/living-room/sofas`) or `category_url`. Filter with `filters` ({`facets[].id`: `facets[].options[].value`}, at most 6 facets) and `price_min` / `price_max`, sort with `sort`, page with `page`.
3. **One product in full:** `/product` with `sku` (for example `5950418`, `APK-29004-R3`) or the product `url`. `variants[]` on a US product carry no price: call `/product` again with that variant's `sku` (2 credits each), or read the per-variant prices in the search item's `variants[]`.
4. **Licensee product:** `/search` with `country`, then `/product` with that market's `items[].handle` (for example `aviemore-sofa`) or `items[].url`. A `sku` on a licensee market answers `400`.
5. **Deals:** `/deals` with `event` (`black_friday`, `clearance` or `hot_buys`), the same sorts, filters and paging as category.
6. **Stores:** `/stores` with `lat` and `lng` (decimal degrees; there is no address or ZIP lookup) and `radius` (10, 25, 50 or 100 miles), then `/store` with a `stores[].store_id` for the address, phone and hours.
7. **Sale-price monitoring:** poll `/product` (or `/search`, `/category` and `/deals` for many items at once) on a schedule. Store `sku`, the time, `price`, `regular_price`, `discount_percent`, `badges`, `stock.status` and `priced_for` per run, and compare only readings with the same `price_zone`. There is no price history endpoint.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `country` | string | `us` | `us`, `ca`, `mx`, `ph`, `sa` or `tr` |
| `page` | integer | 1 | `us` only: 1-based, 48 per page, up to 100. A page past the last returns no items and a note. On a licensee market any page other than 1 answers `400` |
| `sort` | string | `best_sellers` | `us` only: `best_sellers`, `price_asc`, `price_desc`, `newest`, `rating` (customer rating) or `name` (A to Z). Any `sort` on a licensee market answers `400` |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | one of | `us`: an Ashley item number (`items[].sku`): `5950418`, `APK-29004-R3`, `M69611`, `A4000627` |
| `handle` | string | one of | `ca`, `mx`, `ph`, `sa`, `tr`: the product handle from search (`items[].handle`), for example `aviemore-sofa` |
| `url` | string | one of | A product page on a served storefront; its market wins. A `country` that disagrees with the link answers `400` |
| `country` | string | `us` | As on search |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | string | one of | A category path: `furniture/living-room/sofas`, `bedroom/beds`, `mattresses` |
| `category_url` | string | one of | An ashleyfurniture.com category page (a `/c/` URL); refinements in it are kept |
| `page` | integer | 1 | 1-based, 30 per page, up to 100 |
| `sort` | string | `best_sellers` | `best_sellers`, `price_asc`, `price_desc`, `newest`, `rating` or `name` |
| `filters` | object | none | `{"<facets[].id>": "<options[].value>"}` or a list of values (any of them match), at most 6 facets: `{"facetUpholsteryDesign": "Chaise"}`. Not `price`: use `price_min` / `price_max` |
| `price_min` / `price_max` | number | none | Price range in USD, applied to Ashley's own price list (an item priced for another zone can sit just outside it) |
| `country` | string | `us` | `us` only |

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `event` | string | `black_friday` | `black_friday` (Black Friday Furniture Deals), `clearance` (Clearance Furniture) or `hot_buys` (Furniture Hot Buys) |
| `page`, `sort`, `filters`, `price_min`, `price_max` | | | As on category |
| `country` | string | `us` | `us` only |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `lat` | number | required | Latitude in decimal degrees (18 to 72) |
| `lng` | number | required | Longitude in decimal degrees (-180 to -60) |
| `radius` | integer | 50 | Miles: 10, 25, 50 or 100 |
| `country` | string | `us` | `us` only |

### Store (`/store`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string | one of | `stores[].store_id`, for example `us/wisconsin/greenfield/4771-s-27th-st/luxe` |
| `url` | string | one of | A store page on stores.ashleyfurniture.com (`stores[].url`) |
| `country` | string | `us` | `us` only |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/ashley/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "sofa"}'
```

Captured `data` (US, 2026-11-14; 1 of 48 items, 1 of 2 variants, 3 of 6 sorts and 1 of 24 facets shown, facet options trimmed):

```json
{
  "query": "sofa",
  "country": "us",
  "language": "en",
  "currency": "USD",
  "source_domain": "ashleyfurniture.com",
  "priced_for": {"zipcode": "30236", "price_zone": "AFHSPGZ4"},
  "items": [
    {
      "position": 1,
      "sku": "3100438",
      "master_id": "3100438-Master",
      "name": "Mahoney Sofa",
      "brand": "Signature Design by Ashley®",
      "url": "https://www.ashleyfurniture.com/p/mahoney_sofa/3100438.html",
      "image": "https://cdn.ashley.com/assets/31004-38-HEAD-ON-SW-P1-KO.jpg",
      "swatch_image": "https://cdn.ashley.com/assets/31004-SWATCH-BODY-A-500.jpg",
      "price": 299.99,
      "regular_price": 349.99,
      "discount_percent": 14,
      "color": "Pebble",
      "size": null,
      "flag": null,
      "badges": {"sale": true, "clearance": false, "doorbuster": false, "outlet": false, "hot_buy": false, "online_only": false, "ashley_exclusive": false, "luxe": false, "daily_deal": false},
      "new_since": "2023-05-05",
      "rating": 4.8,
      "review_count": 220,
      "variant_count": 2,
      "variants": [
        {
          "sku": "3100438",
          "name": "Mahoney Sofa",
          "color": "Pebble",
          "size": null,
          "url": "https://www.ashleyfurniture.com/p/mahoney_sofa/3100438.html",
          "image": "https://cdn.ashley.com/assets/31004-38-HEAD-ON-SW-P1-KO.jpg",
          "price": 299.99,
          "regular_price": 349.99,
          "rating": 4.8,
          "review_count": 120
        }
      ],
      "promotions": [],
      "sponsored": false
    }
  ],
  "count": 48,
  "total": 861,
  "page": 1,
  "page_size": 48,
  "total_pages": 18,
  "sort": "best_sellers",
  "sorts_offered": ["relevance:descending", "item_name:ascending", "price:ascending"],
  "facets": [
    {
      "id": "facetBrand",
      "name": "Brand",
      "type": "multiple",
      "options": [{"value": "Ashley®", "label": "Ashley®", "count": 574}, {"value": "Serta®", "label": "Serta®", "count": 12}]
    }
  ]
}
```

`total` is Ashley's exact count for the keyword. The item's `rating` and `review_count` cover every variant; each variant carries its own (120 + 98 = 220 here). This page was priced for ZIP 30236, zone AFHSPGZ4: the same sofa read USD 449.99 and USD 499.99 in other zones the same day (see the table at the top).

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/ashley/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "5950418"}'
```

Captured `data` (US, 2026-11-14; 2 of 10 features, 2 of 8 dimension details, 1 of 3 materials, 1 of 7 images, 2 of 4 breadcrumbs, 1 of 10 reviews and 1 of 10 questions shown, description and one answer shortened, customer photos omitted):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "source_domain": "ashleyfurniture.com",
  "priced_for": {"zipcode": "30236", "price_zone": "AFHSPGZ4"},
  "sku": "5950418",
  "master_id": "5950518-Master",
  "name": "Stonemeade Sofa Chaise",
  "brand": "Signature Design by Ashley®",
  "url": "https://www.ashleyfurniture.com/p/x/5950418.html",
  "price": 549.99,
  "regular_price": 599.99,
  "discount_percent": 8,
  "badges": {"sale": true, "clearance": false, "doorbuster": false, "outlet": false, "hot_buy": false, "online_only": false, "ashley_exclusive": false, "luxe": false, "daily_deal": false},
  "new_since": "2024-02-08",
  "item_status": "Current",
  "color": "Taupe",
  "size": null,
  "description": "The Stonemeade sofa chaise feels every bit as good as it looks. ...",
  "features": ["Reinforced frame provides added stability", "Reversible seat and attached back cushions"],
  "options": [
    {
      "dimension": "color",
      "name": "Color",
      "values": [{"value": "Taupe", "name": "Taupe", "orderable": true}, {"value": "Nutmeg", "name": "Nutmeg", "orderable": true}]
    }
  ],
  "variants": [
    {"sku": "5950418", "name": "Stonemeade Sofa Chaise", "color": "Taupe", "url": "https://www.ashleyfurniture.com/p/x/5950418.html", "selected": true},
    {"sku": "5950518", "name": "Stonemeade Sofa Chaise", "color": "Nutmeg", "url": "https://www.ashleyfurniture.com/p/x/5950518.html", "selected": false}
  ],
  "is_set": false,
  "components": [],
  "dimensions": {
    "width_in": 92,
    "depth_in": 62,
    "height_in": 39,
    "weight_lb": 175,
    "weight_kg": 79.38,
    "details": [{"name": "Seat height", "inches": 21}, {"name": "Minimum width of doorway for delivery", "inches": 32}]
  },
  "materials": [{"location": "Body and One Side Toss Pillows", "contents": ["Polyester (100)%"]}],
  "assembly": {"instructions": [], "people_required": null},
  "images": [{"url": "https://cdn.ashley.com/assets/59504-18-HEAD-ON-SW-AGR.jpg", "alt": "Stonemeade Sofa Chaise, Taupe, large"}],
  "category": {"id": "sofas-and-couches", "name": "Sofas and Couches"},
  "breadcrumbs": [
    {"name": "Furniture", "url": "https://www.ashleyfurniture.com/c/furniture"},
    {"name": "Living Room Furniture", "url": "https://www.ashleyfurniture.com/c/furniture/living-room"}
  ],
  "stock": {"status": "LIMITED_STOCK", "quantity": 10, "delivery_method": "home_delivery", "delivery_message": "Delivers within 7 days", "delivery_date": "2026-11-14", "white_glove": false},
  "nearest_store": {
    "name": "Morrow",
    "store_type": "Outlet",
    "stock_status": "OUT_OF_STOCK",
    "address": {"street": "1930 Mount Zion Rd, South Lake Mall", "city": "Morrow", "state": "GA", "zip": "30260"},
    "latitude": 33.56776,
    "longitude": -84.32658
  },
  "rating": 4.8,
  "review_count": 208,
  "rating_histogram": {"1": 2, "2": 0, "3": 3, "4": 21, "5": 182},
  "reviews": [
    {
      "id": 937569,
      "rating": 5,
      "title": "Very satisfied, I have no complaints.",
      "text": "Love it! Very roomy and sturdy. The neutral color is easy to match up with other furniture and home decor.",
      "date": "2026-11-12T13:49:07-05:00",
      "purchase_date": "2026-10-14",
      "incentivized": false,
      "would_recommend": true,
      "helpful_votes": 0,
      "unhelpful_votes": 0,
      "display_name": "Detrich",
      "location": null,
      "photos": [],
      "responses": [{"text": "Thank you for your wonderful feedback! We're delighted to hear that you love the roomy design, sturdy quality, and versatile neutral color. We truly appreciate your support and hope you enjoy your purchase!", "date": "2026-11-12T13:49:07-05:00"}]
    }
  ],
  "questions_total": 24,
  "questions": [
    {
      "id": 9120415,
      "text": "Can the covers come off pillows and cushions to wash in washer machine?",
      "date": "2026-01-05T02:26:19-05:00",
      "answer_count": 2,
      "helpful_votes": 0,
      "answers": [
        {"text": "... However, the covers cannot be removed for machine washing. ...", "date": "2026-01-05T14:01:26-05:00", "answerer_type": "staff", "badge": "Staff", "best_answer": true, "helpful_votes": 0},
        {"text": "Can remove pillow covers but not couch cushion covers", "date": "2026-01-18T11:05:37-05:00", "answerer_type": "customer", "badge": null, "best_answer": false, "helpful_votes": 0}
      ]
    }
  ]
}
```

`variants[]` carry no price: the Nutmeg chaise needs its own call with `sku` `5950518`. `nearest_store` is the store Ashley picks for the answer's region, with that store's stock status, not the user's nearest store. `reviews` holds the first 10 reviews the page shows, in the page's order; `rating_histogram` covers all 208. Reviews carry `purchase_date` and `incentivized` but no verified-buyer flag. The capture also carried 12 `customer_photos` {`url`, `thumbnail`}.

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/ashley/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"path": "furniture/living-room/sofas"}'
```

Captured `data` (US, 2026-11-14; 1 of 30 items and 1 of 5 facets shown):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "source_domain": "ashleyfurniture.com",
  "category": {
    "path": "furniture/living-room/sofas",
    "name": "Sofas and Couches",
    "url": "https://www.ashleyfurniture.com/c/furniture/living-room/sofas/",
    "breadcrumbs": [
      {"name": "Furniture", "url": "https://www.ashleyfurniture.com/c/furniture/"},
      {"name": "Living Room Furniture", "url": "https://www.ashleyfurniture.com/c/furniture/living-room/"},
      {"name": "Sofas and Couches", "url": "https://www.ashleyfurniture.com/c/furniture/living-room/sofas/"}
    ]
  },
  "priced_for": {"zipcode": "62650", "price_zone": "AFHSPGZ12"},
  "items": [
    {
      "position": 1,
      "sku": "3100438",
      "name": "Mahoney Sofa",
      "brand": "Ashley",
      "upc": "024052843439",
      "category": "Furniture/Living Room Furniture/Sofas and Couches",
      "url": "https://www.ashleyfurniture.com/p/mahoney_sofa/3100438.html",
      "image": "https://cdn.ashley.com/assets/31004-38-HEAD-ON-SW-AGR.jpg",
      "price": 449.99,
      "regular_price": 449.99,
      "discount_percent": null,
      "color": "Pebble",
      "flag": null,
      "badges": {"sale": false, "clearance": false, "doorbuster": false, "outlet": false, "hot_buy": false, "online_only": false, "ashley_exclusive": false, "luxe": false, "daily_deal": false},
      "promotion": null,
      "rating": 4.8,
      "review_count": 220,
      "swatch_count": 2,
      "stock_text": "In Stock",
      "delivery_method": "home_delivery"
    }
  ],
  "count": 30,
  "total": 343,
  "page": 1,
  "page_size": 30,
  "total_pages": 12,
  "sort": "best_sellers",
  "requested_filters": {},
  "facets": [
    {
      "id": "facetUpholsteryDesign",
      "name": "Design",
      "options": [
        {"value": "Tufted", "label": "Tufted", "count": 39, "selected": false},
        {"value": "Chaise", "label": "Chaise", "count": 28, "selected": false},
        {"value": "Nailhead Trim", "label": "Nailhead Trim", "count": 6, "selected": false},
        {"value": "Armless", "label": "Armless", "count": 1, "selected": false}
      ]
    }
  ]
}
```

To keep sofas with a chaise, send `"filters": {"facetUpholsteryDesign": "Chaise"}`. The `price` facet's options carry `price_min` / `price_max` (`Under $500`, `$500 to $750` ...): send those as `price_min` / `price_max`, not as a filter. A grid item carries `upc` but no `variants`; the search item carries `variants` but no `upc`.

### Deals

```bash
curl -X POST https://api.scavio.dev/api/v1/ashley/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"event": "black_friday"}'
```

Captured `data` (US, 2026-11-14; 1 of 30 items shown, facets omitted):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "source_domain": "ashleyfurniture.com",
  "event": "black_friday",
  "event_name": "Black Friday Furniture Deals",
  "event_url": "https://www.ashleyfurniture.com/c/deals/black-friday/furniture/",
  "priced_for": {"zipcode": "21704", "price_zone": "AFHSPGZ5"},
  "items": [
    {
      "position": 1,
      "sku": "84905S13-Master",
      "name": "Ella Grove 5-Piece Sectional with Chaise",
      "brand": "Ashley",
      "upc": null,
      "category": "Furniture/Living Room Furniture/Sectional Sofas & Couches",
      "url": "https://www.ashleyfurniture.com/p/ella_grove_5-piece_sectional_with_chaise/84905S13-Master.html",
      "image": "https://cdn.ashley.com/assets/84905-64-46-77-46-17-4X3-CROP.jpg",
      "price": 2899.99,
      "regular_price": 3499.99,
      "discount_percent": 17,
      "color": null,
      "flag": "ASHLEY EXCLUSIVE",
      "badges": {"sale": true, "clearance": false, "doorbuster": false, "outlet": false, "hot_buy": false, "online_only": false, "ashley_exclusive": true, "luxe": false, "daily_deal": false},
      "promotion": null,
      "rating": null,
      "review_count": null,
      "swatch_count": 0,
      "stock_text": "In Stock",
      "delivery_method": null
    }
  ],
  "count": 30,
  "total": 238,
  "page": 1,
  "page_size": 30,
  "total_pages": 8,
  "sort": "best_sellers",
  "requested_filters": {}
}
```

Build testing counted 238 Black Friday items, 578 clearance and 28 Hot Buys.

### Stores and one store

```bash
curl -X POST https://api.scavio.dev/api/v1/ashley/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"lat": 40.7506, "lng": -73.9972}'
```

Captured `data` (2026-11-14; 3 of 10 stores shown):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "source_domain": "stores.ashleyfurniture.com",
  "latitude": 40.7506,
  "longitude": -73.9972,
  "radius_miles": 50,
  "stores": [
    {"store_id": "us/new-york/bronx/340-baychester-ave/luxe", "name": "Bronx Ashley Store", "url": "https://stores.ashleyfurniture.com/store/us/new-york/bronx/340-baychester-ave/luxe/"},
    {"store_id": "us/new-york/brooklyn/241-37th-st/luxe", "name": "Brooklyn Ashley Store", "url": "https://stores.ashleyfurniture.com/store/us/new-york/brooklyn/241-37th-st/luxe/"},
    {"store_id": "us/new-york/brooklyn/5100-kings-plaza/luxe", "name": "Brooklyn Ashley Store", "url": "https://stores.ashleyfurniture.com/store/us/new-york/brooklyn/5100-kings-plaza/luxe/"}
  ],
  "count": 10
}
```

The list is in Ashley's order (alphabetical, not by distance) and carries no address or distance. Then:

```bash
curl -X POST https://api.scavio.dev/api/v1/ashley/store \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "us/wisconsin/greenfield/4771-s-27th-st/luxe"}'
```

Captured `data` (2026-11-14; 2 of 7 days shown, `phone`, `image` and `map_url` omitted):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "source_domain": "stores.ashleyfurniture.com",
  "store_id": "us/wisconsin/greenfield/4771-s-27th-st/luxe",
  "name": "Ashley Store Greenfield, WI",
  "url": "https://stores.ashleyfurniture.com/store/us/wisconsin/greenfield/4771-s-27th-st/luxe/",
  "address": {"street": "4771 S 27th St", "city": "Greenfield", "state": "WI", "zip": "53221", "country": "US"},
  "latitude": 42.957938,
  "longitude": -87.951706,
  "hours": [{"day": "saturday", "opens": "10:00AM", "closes": "07:00PM"}, {"day": "sunday", "opens": "11:00AM", "closes": "06:00PM"}],
  "payment_accepted": ["cash", "credit card", "debit card"],
  "services": ["Financing", "White Glove Delivery"],
  "rating": 4.4
}
```

`services` is the list the store page shows. To rank stores by distance, compute it yourself from each store's `latitude` / `longitude`.

### Licensee storefronts

```bash
curl -X POST https://api.scavio.dev/api/v1/ashley/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "sofa", "country": "ca"}'
```

Captured `data` (Canada, 2026-11-14; 1 of 10 items shown, `image` omitted):

```json
{
  "query": "sofa",
  "country": "ca",
  "language": "en",
  "currency": "CAD",
  "source_domain": "ashleyhomestore.ca",
  "items": [
    {
      "position": 1,
      "sku": null,
      "handle": "aviemore-sofa",
      "product_id": 7984705306713,
      "name": "Aviemore Sofa",
      "brand": "Signature Design by Ashley",
      "product_type": "Sofa",
      "url": "https://ashleyhomestore.ca/products/aviemore-sofa",
      "price": 879.99,
      "regular_price": 879.99,
      "discount_percent": null,
      "price_max": 879.99,
      "available": true
    }
  ],
  "count": 10,
  "total": null,
  "page": 1,
  "page_size": 10
}
```

Then `/product` with `{"handle": "aviemore-sofa", "country": "ca"}` returned `sku` `AFHS-2430438` at CAD 879.99 with 3 colour variants (Spice, Ink, Stone), each with `price`, `regular_price`, `available` and `barcode`. Other markets, same day:

- `mx`: `{"query": "sofa", "country": "mx"}` returned 10 items in MXN, the first the Cashton Sofa at MXN 26,866 with `regular_price: null`, the second "Sofá seccional reclinable eléctrico de 3 piezas con chaise longue Acklen Place" at MXN 74,033.
- `ph`: the Bixler Sofa at PHP 58,200; `sa`: the Stonemeade Queen Sofa Sleeper at SAR 6,465.
- `tr`: `{"query": "koltuk", "country": "tr"}` returned 36 items in TRY and Turkish, the first "Elyza Köşe Koltuk Takımı (5 Modül)" at TRY 286,906 with `regular_price` 573,812 and `discount_percent` 50; `/product` for its handle returned `price` 286906.21. Search rounds Turkish prices to the lira; product carries the exact price.

### Python

```python
import time
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def ashley(endpoint, body, timeout=180):
    r = requests.post(f"{BASE}/api/v1/ashley/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()["data"]

readings = []
for sku in ["5950418", "3100438"]:  # 2 credits each on us
    p = ashley("product", {"sku": sku})
    readings.append({
        "sku": p["sku"],
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "zipcode": p["priced_for"]["zipcode"],
        "price_zone": p["priced_for"]["price_zone"],
        "price": p["price"],
        "regular_price": p["regular_price"],
        "discount_percent": p["discount_percent"],
        "sale": p["badges"]["sale"],
        "stock_status": p["stock"]["status"],
    })

# Store `readings` and run this on a schedule. Compare a reading only with
# earlier readings of the same sku in the same price_zone.
for row in readings:
    print(row)
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live; nothing is cached. Every `data` echoes `country`, `language`, `currency` and `source_domain`. Prices are numbers in the market's currency.

- **us search** - `query`, `priced_for` {`zipcode`, `price_zone`}, `items[]`, `count`, `total` (exact), `page`, `page_size` (48), `total_pages`, `sort`, `sorts_offered[]`, `facets[]` {`id`, `name`, `type`, `options[]` {`value`, `label`, `count`; range facets add `range`}}, `notes` (when there is something to say). Item: `position`, `sku`, `master_id`, `name`, `brand`, `url`, `image`, `swatch_image`, `price`, `regular_price`, `discount_percent`, `color`, `size` (bed size), `flag` (the page's own flag text), `badges` {`sale`, `clearance`, `doorbuster`, `outlet`, `hot_buy`, `online_only`, `ashley_exclusive`, `luxe`, `daily_deal`}, `new_since`, `rating`, `review_count`, `variant_count`, `variants[]` {`sku`, `name`, `color`, `size`, `url`, `image`, `price`, `regular_price`, `rating`, `review_count`}, `promotions[]`, `sponsored`.
- **category / deals** - `priced_for`, `items[]`, `count`, `total`, `page`, `page_size` (30), `total_pages`, `sort`, `requested_filters`, `facets[]` {`id`, `name`, `options[]` {`value`, `label`, `count`, `selected`; the price facet adds `price_min`, `price_max`}}, `notes`; category adds `category` {`path`, `name`, `url`, `breadcrumbs[]`}; deals adds `event`, `event_name`, `event_url`. Grid item: `position`, `sku`, `name`, `brand`, `upc`, `category`, `url`, `image`, `price`, `regular_price`, `discount_percent`, `color`, `flag`, `badges`, `promotion`, `rating`, `review_count`, `swatch_count`, `stock_text` (`In Stock`), `delivery_method` (`home_delivery` or `direct_ship`).
- **us product** - `priced_for`, `sku`, `master_id`, `name`, `brand`, `url`, `price`, `regular_price`, `discount_percent`, `badges`, `new_since`, `item_status`, `color`, `size`, `description`, `features[]`, `options[]` {`dimension`, `name`, `values[]` {`value`, `name`, `orderable`}}, `variants[]` {`sku`, `name`, the dimension values, `url`, `selected`}, `is_set`, `components[]` {`sku`, `name`, `price`, `regular_price`, `dimensions`, `stock_status`, `stock_quantity`, `url`}, `dimensions` {`width_in`, `depth_in`, `height_in`, `weight_lb`, `weight_kg`, `details[]` {`name`, `inches`}}, `materials[]` {`location`, `contents[]`}, `assembly` {`instructions[]`, `people_required`}, `images[]` {`url`, `alt`}, `category` {`id`, `name`}, `breadcrumbs[]`, `stock` {`status`, `quantity`, `delivery_method`, `delivery_message`, `delivery_date`, `white_glove`}, `nearest_store` {`name`, `store_type`, `stock_status`, `address`, `latitude`, `longitude`}, `rating`, `review_count`, `rating_histogram` {`1` to `5`}, `reviews[]` {`id`, `rating`, `title`, `text`, `date`, `purchase_date`, `incentivized`, `would_recommend`, `helpful_votes`, `unhelpful_votes`, `display_name`, `location`, `photos[]`, `responses[]` {`text`, `date`}}, `customer_photos[]` {`url`, `thumbnail`}, `questions_total`, `questions[]` {`id`, `text`, `date`, `answer_count`, `helpful_votes`, `answers[]` {`text`, `date`, `answerer_type` (`staff` or `customer`), `badge`, `best_answer`, `helpful_votes`}}; `requested_sku` and a note when Ashley answers a different item than the one sent.
- **licensee search** (`ca`, `mx`, `ph`, `sa`, `tr`) - `query`, `items[]` {`position`, `sku` (`null`), `handle`, `product_id`, `name`, `brand` (when the storefront tags it), `product_type`, `url`, `image`, `price`, `regular_price`, `discount_percent`, `price_max`, `available`}, `count`, `total` (`null`), `page` (1), `page_size`. `tr` items carry `free_shipping` instead of `product_type`, `price_max` and `available`.
- **licensee product** - `sku`, `handle`, `product_id`, `name`, `brand`, `product_type`, `url`, `price`, `regular_price`, `discount_percent`, `price_max`, `available`, `description`, `options[]` {`name`, `values[]`}, `variants[]` {`sku`, `variant_id`, `name`, `options[]`, `price`, `regular_price`, `discount_percent`, `available`, `barcode`}, `images[]`, `published_at`. `tr`: `sku`, `handle`, `name`, `brand`, `url`, `price`, `regular_price`, `discount_percent`, `available`, `description`, `images[]`, `gtin`, `rating`, `review_count`.
- **stores** - `latitude`, `longitude`, `radius_miles`, `stores[]` {`store_id`, `name`, `url`}, `count`.
- **store** - `store_id`, `name`, `url`, `phone`, `address` {`street`, `city`, `state`, `zip`, `country`}, `latitude`, `longitude`, `hours[]` {`day`, `opens`, `closes`}, `payment_accepted[]`, `services[]`, `rating`, `image`, `map_url`.

## Guardrails

- Regular Price: `regular_price` is Ashley's "Regular Price". Ashley's Terms and Conditions define it: "Regular Price is our highest advertised price in store and online. Regular Price is offered to customers using special long-term financing." Never call it the previous price or yesterday's price, and never present `discount_percent` as a measured price drop. That definition is from ashleyfurniture.com; on the licensee storefronts `regular_price` is that storefront's own struck-through price.
- `regular_price` is set only when it is at or above `price`. When the two are equal, `discount_percent` is `null`. On `mx` and `ph` it is often `null`.
- Region pricing: the price is for the ZIP and price zone in `priced_for`, which Ashley assigns to each request. There is no ZIP input: never claim prices for a ZIP the user chose. Say which ZIP and price zone a price was for, and never compare prices across zones as if they were one price.
- Paging and sorts: each call can land in a different price zone, so consecutive pages can overlap slightly (build testing saw 4 shared items between page 1 and page 2) and a price sort is ordered by the zone of that page. De-duplicate by `sku` when you collect several pages.
- `price_min` / `price_max` filter on Ashley's own price list, so an item priced for another zone can sit just outside the range.
- Online prices: these are ashleyfurniture.com's online prices. Ashley stores are independently owned and operated, so a store quote can differ.
- Variants: a US product's `variants[]` carry no price. Each variant needs its own `/product` call with its `sku`; the search item's `variants[]` do carry prices. Never assume every color or size costs the same.
- Sets: `is_set: true` products list each piece in `components[]` with its own price and stock. `stock_quantity` is warehouse stock for that piece, not a count of complete sets.
- Reviews: `reviews` is the first 10 reviews the page shows, in the page's order. There is no review paging, sort or star filter. Use `rating`, `review_count` and `rating_histogram` for the overall picture; never compute a distribution from the 10. There is no verified-buyer flag: `purchase_date` and `incentivized` are what the page shows. Quote short excerpts, and never more than the `display_name` of a reviewer.
- Q&A: `answerer_type: "staff"` answers are Ashley's; `customer` answers are other shoppers'. Say which.
- Search facets are informational: `/search` takes no filters. Filter on `/category` or `/deals`.
- Stores: `/stores` needs `lat` and `lng`; there is no address, city or ZIP lookup. The list is alphabetical and carries no address or distance: call `/store` per store.
- Licensee markets: search returns up to 10 matches (`tr`: its first results page) with no paging, sort or total; product takes `handle` or `url`, never `sku`. Category, deals, stores and store are US only.
- `nearest_store` on a product is the store Ashley picks for the answer's region, not a store near the user.
- Currency: always give the currency and market next to a price. Never compare or average prices across markets without converting explicitly, with the rate and its date.
- Not available: price history, a ZIP or delivery-address input, review paging, search suggestions, search-page filters, store search by ZIP or city, Arabic on `sa`, cart, checkout, financing offers and dealer (AshleyDirect) pricing.
- Terms: Ashley's Terms of Use restrict automated collection of site content. We do not interpret them. This is not legal advice; the user is responsible for their own compliance. Do not republish Ashley product photos; link product pages instead.
- Never fabricate prices, item numbers, handles, store ids, ZIP codes, price zones, reviews or ratings. Only return what the API returned, with the market, `priced_for` and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` outside `us`, `ca`, `mx`, `ph`, `sa`, `tr`; a market other than `us` on category, deals, stores or store ("category is available on us only"); `page` other than 1 or any `sort` on a licensee market; a `sku` on a licensee market ("send handle or url"); a `handle` on `us`; a `sku` that is not an Ashley item number; a `url` that is not a product page on a served storefront, or that disagrees with `country`; a `path` or `category_url` that is not an ashleyfurniture.com category; a `sort` or `event` outside the lists; more than 6 facets, a `price` key in `filters`, or `price_min` not below `price_max`; missing `lat` / `lng`, or a `radius` other than 10, 25, 50 or 100; a `store_id` that is not a US store id from `/stores`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged at the market's cost: "No Ashley product with item number ...", "No product ... on <storefront>.", "No Ashley category at ...", "No Ashley store page at ...". Take item numbers, handles, paths and store ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api).
- `502` means Ashley data was temporarily unavailable ("Ashley Furniture is temporarily unavailable. Please try again."). It is retried automatically and not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Ashley is busy ("Ashley Furniture is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.58.0
npm install scavio@0.59.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.ashley.search({ query: "sofa", sort: "price_asc" });
const { data: chaise } = await scavio.ashley.product({ sku: "5950418" });
const { data: sofas } = await scavio.ashley.category({ path: "furniture/living-room/sofas", filters: { facetUpholsteryDesign: "Chaise" } });
const { data: blackFriday } = await scavio.ashley.deals({ event: "black_friday", sort: "price_asc" });
const { data: near } = await scavio.ashley.stores({ lat: 40.7506, lng: -73.9972, radius: 25 });
const { data: store } = await scavio.ashley.store({ store_id: "us/wisconsin/greenfield/4771-s-27th-st/luxe" });
const { data: canada } = await scavio.ashley.product({ handle: "aviemore-sofa", country: "ca" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.ashley.search(...)`, `client.ashley.product(...)`, `client.ashley.category(...)`, `client.ashley.deals(...)`, `client.ashley.stores(...)` and `client.ashley.store(...)`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all six endpoints as tools: `search_ashley`, `get_ashley_product`, `get_ashley_category`, `get_ashley_deals`, `get_ashley_stores` and `get_ashley_store`. Ashley Furniture is opt-in: add `ashley` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.56.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,ashley"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/ashley-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api), [product](https://scavio.dev/docs/ashley-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api), [category](https://scavio.dev/docs/ashley-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api), [deals](https://scavio.dev/docs/ashley-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api), [stores](https://scavio.dev/docs/ashley-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api), [store](https://scavio.dev/docs/ashley-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api). Overview: [Ashley Furniture API](https://scavio.dev/ashley-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api).
