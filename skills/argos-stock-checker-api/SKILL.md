---
name: argos-stock-checker-api
description: Argos stock checker API for Argos store stock - for 1 to 10 Argos products, which Argos stores near a UK postcode (up to 10 stores within 50 miles - standalone Argos stores, Argos inside Sainsbury's and collection points) can hand each one over (collect now, today, tomorrow, later, out of stock or not available, with the time) and whether it can be delivered to a postcode (same day, next day), next to the price, the was price, the saving computed from the two, Argos's offer text and badges (Black Friday, Price Guarantee). Availability states and collection times, not unit counts. Keyword search, category and deal lists (Black Friday, clearance, special offers, Top 100), 24 per page, filtered by brand, seller (Argos or Trusted Sellers), offers, price, rating and any facet; one product in full (Argos or Trusted Seller page); stores near a postcode with opening hours; reviews up to 100 per page with syndicated reviews flagged and Argos's own AI summary; customer Q&A; the department tree and search suggestions. argos.co.uk only (UK, GBP). 10 endpoints, 2 credits per call. No unit counts, price history (poll and store), Argos Ireland or checkout.
version: 1.0.0
tags: argos, argos-api, argos-uk, argos-stock, argos-stock-check, argos-stock-checker, argos-store-stock, argos-collection, argos-fast-track, argos-prices, argos-was-price, argos-black-friday, argos-price-guarantee, argos-clearance, argos-deals, argos-reviews, argos-questions, argos-stores, argos-trusted-sellers, argos-product-data, uk-retail, uk-postcode, store-stock, stock-checker, in-store-availability, price-monitoring, gbp, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/argos-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api
---

# Argos Stock Checker API - Store Stock by Postcode, Prices, Reviews

Read Argos's own online store (argos.co.uk, the UK store, prices in GBP): store stock near a UK postcode, keyword search, category and deal lists, one product in full, stores, reviews, customer questions, the department tree and search suggestions. All 10 endpoints return structured JSON at 2 credits per call.

**The job this skill is for: Argos store stock.** For one or more Argos products (up to 10 per call), which Argos stores near a UK postcode can hand each one over (`collect_now`, `collect_today`, `collect_tomorrow`, `collect_later`, `out_of_stock`, `not_available`, with the time it can be collected) and whether it can be delivered to a postcode (`same_day`, `next_day`), next to the `price`, the `was_price` and the badges on the same product, on a dated read.

Six limits shape every answer, so say them plainly:
- **Store stock is an availability state and a collection time, not a unit count.** Argos shows whether a store can hand the item over and when; it shows no quantities. Never report "N in stock".
- **Two postcodes.** `postcode` is where stores are searched (up to 10 stores within 50 miles, nearest first); `delivery_postcode` is where home delivery is checked (default: the same postcode). "Stores near a postcode" means the stores the answer returns, not every Argos store.
- **Search, category and deal lists are 24 per page** (`page` 1-200; `total_pages` says how deep a list goes; Top 100 is 2 pages of 60). Never call one page "all products": follow `has_more`. Tu Clothing items Argos lists in results are left out and counted in `tu_clothing_excluded`.
- **Two product templates.** Argos's own items (7-digit catalogue numbers, `template: "argos"`) come back in full; Trusted Seller items (Argos's marketplace, 8-character ids such as `xhe0aexe`, `template: "trusted_seller"`) carry the fields their page shows, with `seller_name: null` (the page names no seller), no rating and no store stock.
- **Reviews: up to 100 per page, every review reachable**, 5 sorts and a star filter. Syndicated reviews (written on the brand's own site) are flagged with `syndication_source`. No reviewer names, locations, ages or genders are returned.
- **UK only.** Argos Ireland closed in 2023, so there is no `country` input. Postcodes must be full UK postcodes.

Argos has no public product, price or stock API. It runs an affiliate programme with a product feed for approved publishers (listed on CJ), and marketplace sellers manage their own listings through Argos's seller platform; neither returns live stock at the stores near a postcode. This skill reads the public argos.co.uk pages instead, with one Scavio key.

See also: for US store stock use `best-buy-product-data`, `home-depot-product-data` or `target-product-data`; for ASOS prices in the UK and elsewhere use `asos-api`; for Wayfair UK use `wayfair-api`; for IKEA UK use `ikea-api`; for prices across UK retailers use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Check Argos stock: which Argos stores near a UK postcode can hand over a product now, today or tomorrow, and how far away they are
- Check several Argos products at once (up to 10) against the stores near one postcode, or the same products near several postcodes
- See whether an Argos product can be delivered to a postcode same day (Fast Track) or next day
- Compare standalone Argos stores, Argos inside Sainsbury's and Argos collection points near a postcode
- Read Argos prices, was prices, savings, offer text (Half Price, Save £25.00) and badges (Black Friday, Price Guarantee) for a search, a category or a deal list
- Read Argos's Black Friday, clearance, special offers or Top 100 deals lists
- Read Argos reviews sorted by newest, oldest, most helpful, highest or lowest rating, or only 1-star (or any star) reviews, with syndicated reviews flagged
- Read customer questions about an Argos product with Argos staff, brand and customer answers
- Find Argos stores near a postcode with opening hours, or one store's special (holiday) hours and services
- Resolve Argos category ids, facet values and search suggestions before a search

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 2 credits.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, search took 8 seconds, product 3, store-stock 2, stores 2, reviews 1, questions 1, category 1, deals 2, categories 1 and suggestions 1. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns |
|---|---|
| `POST /api/v1/argos/store-stock` | For 1-10 Argos products: the Argos stores near a UK postcode (up to 10, within 1-50 miles, nearest first) with a collection state and time per product, plus delivery availability to a postcode (same day, next day) |
| `POST /api/v1/argos/search` | Products for a keyword, 24 per page, with price, was price, save, offer text, badges, rating and seller; filters, 4 sorts and the facets the answer offers |
| `POST /api/v1/argos/product` | One product by id or link: EAN, badges with start and end dates, specifications, variants, special offers, Nectar points, care plans, payment options, bundles, rating distribution, Q&A counts and the first 10 reviews (Trusted Seller items: the fields their page shows) |
| `POST /api/v1/argos/stores` | Argos stores near a UK postcode (no stock: use store-stock), or one store by reference with address, opening hours, special hours and services |
| `POST /api/v1/argos/reviews` | One product's reviews, up to 100 per page, 5 sorts and a star filter, with the review stats and Argos's own AI-generated summary |
| `POST /api/v1/argos/questions` | One product's customer questions with their answers (staff, brand or customer), up to 50 per page |
| `POST /api/v1/argos/categories` | Argos's department tree: 14 departments with groups and category links (category ids feed `category`) |
| `POST /api/v1/argos/category` | One category's products by category id, 24 per page, same filters and sorts as search |
| `POST /api/v1/argos/deals` | A deal collection: `black_friday`, `clearance`, `special_offers` (24 per page, with filters) or `top_100` (Argos's own Top 100 deals list, 2 pages of 60) |
| `POST /api/v1/argos/suggestions` | Argos's search suggestions for a partial query, with Argos's popularity weight |

## Credits

Every endpoint costs **2 credits per call**. Each page is one call; one store-stock call covers up to 10 products near one postcode. A not-found (`404`: an unknown or withdrawn product, an unknown store) is charged; a `400` and an upstream failure (`502`, `503`) are not.

## Market

One store: argos.co.uk (England, Scotland, Wales and Northern Ireland), English, prices in GBP. There is no `country` input: Argos Ireland closed all its stores and online operations in 2023. Postcodes are full UK postcodes in any spacing or case (`SW1A 1AA`, `sw1a1aa`); every answer echoes them as `OUTWARD INWARD`. A postcode outside the UK format answers `400` before anything is charged.

## Store stock

`/argos/store-stock` takes `product_ids` (1-10 Argos catalogue numbers, 7 digits), `postcode` (where stores are searched) and optionally `delivery_postcode`, `max_distance` (1-50 miles, default 50) and `max_results` (1-10 stores, default 10).

- `stores[]` (nearest first): `store_id`, `name`, `store` (the reference `/argos/stores` takes), `url`, `type`, `brand`, `distance_miles`, `address`, `latitude`, `longitude`, `phone`, `hours`, `special_hours` and `products[]` {`product_id`, `state`, `available_from`, `message`}.
- `type`: `argos_store` (a standalone Argos), `inside_sainsburys` (an Argos store inside a Sainsbury's), `collection_point` (an Argos collection point in a Sainsbury's, where `brand` reads `Sainsbury's`).
- Collection `state` per store and product:

| `state` | Meaning |
|---|---|
| `collect_now` | Can be collected right away (in stock at that store) |
| `collect_today` | Can be collected from a time today: `available_from` has it |
| `collect_tomorrow` | Can be collected from a time tomorrow: `available_from` has it |
| `collect_later` | Can be collected from a later date: `available_from` has it |
| `out_of_stock` | Out of stock for collection there |
| `not_available` | Not eligible: Argos is not selling it for collection now |
| `other` | An answer Argos phrased another way: read `message` |

- `delivery` {`postcode`, `products[]` {`product_id`, `state`, `available_from`, `fast_track`, `message`}}: `state` is `same_day`, `next_day`, `later`, `out_of_stock`, `not_available` or `other`. `fast_track` marks Fast Track same-day delivery. `message` is Argos's own sentence: quote it when `state` is `other` (the rural capture read "Delivery within 2 days to LL554UY").
- `products[]` {`product_id`, `known`, `collectable`, `deliverable`, `globally_out_of_stock`}: whether Argos knows the id and sells it for collection or delivery at all.
- The answer is in stock or not, and when. There are no unit counts: never turn a state into a quantity.

## Prices and badges

- `price` is the price Argos shows now; `was_price` is the site's was price, shown on offers (`null` when the site shows none).
- `save` is computed by Scavio: `was_price - price`, where both exist and the was price is higher. Quote it as "computed from the price and the was price". `offer_text` is Argos's own words (`Half Price`, `Save £25.00`, `Save 25%`, `Less Than Half Price`, `Lowest Price`).
- `badges` on list items are the site's badge codes as given (`Black_Friday`, `price_guarantee`, `VALUE_amazing_deals`, `INFO_exclusive`, `INFO_2yr_warranty` ...). On a product, `badges[]` carries `{badge, type, text, starts_at, ends_at}`: in the capture, `Black_Friday` and `price_guarantee` ran from 2026-10-30 to 2026-12-02.
- Argos's own definitions (Black Friday FAQs, help.argos.co.uk): a Price Guarantee badge "means the displayed price of that product won't go lower before midnight on 25th December", with an Argos e-Gift card for the difference if it does; Black Friday at Argos runs from 30 October 2026 to 1 December 2026. Quote them as Argos's; never claim a price is the lowest or that a was price is a real reduction. An item with `offer_text: "Lowest Price"` can have `was_price: null` (captured in the Black Friday list).
- `seller` is `argos` (sold and fulfilled by Argos) or `trusted_seller` (Argos's marketplace of third-party sellers). `delivery_cost` is `null` on Trusted Seller items: the seller sets it.
- No card, checkout or Argos Pay terms: `argos_pay` reports what the page shows (`available`, `offering`, `message`), not the price a buyer pays on credit.

## Workflow

1. **Find the catalogue numbers:** `/argos/search` with `query` (or `/argos/category` with a `category_id` from `/argos/categories`). Each item has `product_id`, `price`, `was_price`, `save`, `offer_text`, `badges`, `seller` and `reservable` (in-store collection).
2. **Stock near a postcode:** `/argos/store-stock` with up to 10 `product_ids` and a `postcode`. Read each store's `products[].state` and `available_from`, and `delivery.products[].state` for home delivery.
3. **Several places:** call `/store-stock` once per postcode (2 credits each). Set `delivery_postcode` when the delivery address differs from where the shopper collects.
4. **One product in full:** `/argos/product` with `product_id`: badges with dates, special offers, specifications, variants (each colour or size has its own `product_id`: check stock per variant), rating and the first 10 reviews.
5. **Deals:** `/argos/deals` with `collection` (`black_friday`, `clearance`, `special_offers`), paging until `has_more` is `false`, or `top_100` for Argos's own curated list.
6. **Reviews and questions:** `/argos/reviews` with `product_id`, `sort`, `rating` and `limit` up to 100; `/argos/questions` for Q&A.
7. **Stores:** `/argos/stores` with `postcode` for the list, then `store` (a `stores[].store` reference) for special hours and services.
8. **Watching stock or prices:** there is no history. Poll the same products and postcodes on a schedule and store each answer with its `fetched_at` time.

## Parameters

### Store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_ids` | array or string | required | 1-10 Argos catalogue numbers (7 digits), as a list or comma-separated, e.g. `["8377058", "7163184"]`. Trusted Seller ids answer `400`: those items are delivered by the seller and never stocked in Argos stores |
| `postcode` | string | required | A full UK postcode: where stores are searched |
| `delivery_postcode` | string | `postcode` | A full UK postcode: where home delivery is checked |
| `max_distance` | integer | 50 | Search radius in miles, 1-50 |
| `max_results` | integer | 10 | Stores, 1-10 (10 is the most Argos returns) |

### Search (`/search`), category (`/category`) and deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Search text (1-200 chars). Optional text inside a category or a deal collection (not with `top_100`) |
| `category_id` | string or integer | category: required | Category id: `categories[].category_id` (any level), the `category` facet's values, or the `c:<id>` of an argos.co.uk browse link (29560 Kettles, 29575 Air fryers). Category only |
| `collection` | string | deals: required | `black_friday`, `clearance`, `special_offers` or `top_100`. Deals only |
| `category` | string or integer | all | A category id inside search or deals |
| `offers` | string or array | all | Up to 3 (OR): `clearance`, `special_offer`, `black_friday`. Search and category; deals sets it from `collection` |
| `brand` | string or array | all | Brands, up to 10 (OR), lower case as in the `brands` facet's `values[].value`, e.g. `russell hobbs`, `ninja` |
| `seller` | string | all | `argos` or `trusted_seller` |
| `new_in` | boolean | false | Only products Argos marks New In |
| `colour` | string or array | all | Colour groups, up to 10, from the `colour group` facet, e.g. `blacks`, `whites`, `greys` |
| `price_min` / `price_max` | number | none | GBP, any range (sent as is, not snapped to the site's price bands) |
| `rating_min` | integer | none | `5` (five stars only) or `1`-`4` (that many stars or more) |
| `filters` | object | none | Any other facet by `facets[].name` -> a value or a list of values (`facets[].values[].value`), up to 10 facets, e.g. `{"kettle capacity (l)": "1.6l - 2.0l"}` |
| `sort` | string | `relevance` | `relevance` (Argos's Most Popular), `price_low`, `price_high`, `rating` |
| `page` | integer | 1 | 24 per page, 1-200. `top_100`: 1-2 (60 per page) and `page` is its only input |

### Product (`/product`), reviews (`/reviews`), questions (`/questions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string or integer | one of | A 7-digit catalogue number (`8377058`) or a Trusted Seller id (8 letters and digits, `xhe0aexe`) |
| `url` | string | one of | An argos.co.uk product link (`https://www.argos.co.uk/product/<id>/`). Send exactly one of `product_id`, `url` |
| `sort` | string | `newest` | Reviews: `newest`, `oldest`, `most_helpful` (Argos's helpfulness order: the share of helpful votes, not their count), `highest_rating`, `lowest_rating`. Questions: `newest`, `oldest` |
| `rating` | integer or array | all | Reviews only: star ratings 1-5, one or a list, e.g. `[1, 2]` |
| `limit` | integer | 20 / 10 | Reviews: 1-100 per page (default 20). Questions: 1-50 (default 10) |
| `page` | integer | 1 | Reviews and questions: `page * limit` reaches every review up to `total` |

### Stores (`/stores`), categories (`/categories`), suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `postcode` | string | one of | Stores near this full UK postcode |
| `store` | string | one of | One store: `stores[].store` (e.g. `661-manchester-arndale-argos`) or its argos.co.uk/stores/... link. A bare store id is not accepted. Send exactly one of `postcode`, `store` |
| `max_distance`, `max_results` | integer | 50, 10 | Stores near a postcode only |
| `query` | string | suggestions: required | What the shopper has typed so far (1-100 chars) |
| `limit` | integer | 10 | Suggestions, 1-10 |

`/categories` takes no input.

## Examples

### Store stock

```bash
curl -X POST https://api.scavio.dev/api/v1/argos/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_ids": ["8377058", "7163184"], "postcode": "SW1A 1AA"}'
```

Captured `data` (2026-11-21, 2 credits; 3 of 9 stores shown, `url`, `latitude`, `longitude`, `phone` and all but Monday's `hours` dropped):

```json
{
  "postcode": "SW1A 1AA",
  "delivery_postcode": "SW1A 1AA",
  "max_distance": 50,
  "product_ids": ["8377058", "7163184"],
  "count": 9,
  "stores": [
    {
      "store_id": 6512,
      "name": "Westminster Rochester Row Sainsbury's (Argos Collection Point)",
      "store": "6512-westminster-rochester-row-sainsbury's-(argos-collection-point)",
      "type": "collection_point",
      "brand": "Sainsbury's",
      "distance_miles": 0.49,
      "address": { "lines": ["10 Rochester Row"], "town": "London", "county": "Greater London", "postcode": "SW1P 1BT" },
      "hours": { "monday": [{ "open": "07:00", "close": "23:00" }] },
      "special_hours": [],
      "products": [
        { "product_id": "8377058", "state": "collect_tomorrow", "available_from": "2026-11-22T10:00:00Z", "message": "Order now, collect from 10am tomorrow at Westminster Rochester Row Sainsbury's (Argos Collection Point)" },
        { "product_id": "7163184", "state": "collect_tomorrow", "available_from": "2026-11-22T10:00:00Z", "message": "Order now, collect from 10am tomorrow at Westminster Rochester Row Sainsbury's (Argos Collection Point)" }
      ]
    },
    {
      "store_id": 4705,
      "name": "Pimlico Argos (Inside Sainsbury's)",
      "store": "4705-pimlico-argos-(inside-sainsbury's)",
      "type": "inside_sainsburys",
      "brand": "Argos",
      "distance_miles": 0.56,
      "address": { "lines": ["99 Wilton Road"], "town": "Pimlico", "county": "Greater London", "postcode": "SW1V 1DT" },
      "hours": { "monday": [{ "open": "09:00", "close": "21:00" }] },
      "special_hours": [],
      "products": [
        { "product_id": "8377058", "state": "collect_now", "available_from": "2026-11-21T09:00:00Z", "message": "Order now, collect right away at Pimlico Argos (Inside Sainsbury's)" },
        { "product_id": "7163184", "state": "collect_now", "available_from": "2026-11-21T09:00:00Z", "message": "Order now, collect right away at Pimlico Argos (Inside Sainsbury's)" }
      ]
    },
    {
      "store_id": 4367,
      "name": "Nine Elms Argos (Inside Sainsbury's)",
      "store": "4367-nine-elms-argos-(inside-sainsbury's)",
      "type": "inside_sainsburys",
      "brand": "Argos",
      "distance_miles": 1.44,
      "address": { "lines": ["62 Wandsworth Road"], "town": "London", "county": "Greater London", "postcode": "SW8 2LF" },
      "hours": { "monday": [{ "open": "09:00", "close": "21:00" }] },
      "special_hours": [],
      "products": [
        { "product_id": "8377058", "state": "collect_now", "available_from": "2026-11-21T09:00:00Z", "message": "Order now, collect right away at Nine Elms Argos (Inside Sainsbury's)" },
        { "product_id": "7163184", "state": "collect_later", "available_from": "2026-11-23T10:00:00Z", "message": "Order now, collect from Monday 23 November at Nine Elms Argos (Inside Sainsbury's)" }
      ]
    }
  ],
  "delivery": {
    "postcode": "SW1A 1AA",
    "products": [
      { "product_id": "8377058", "state": "next_day", "available_from": "2026-11-21", "fast_track": false, "message": "Order now for delivery to SW1A1AA tomorrow" },
      { "product_id": "7163184", "state": "next_day", "available_from": "2026-11-21", "fast_track": false, "message": "Order now for delivery to SW1A1AA tomorrow" }
    ]
  },
  "products": [
    { "product_id": "8377058", "known": true, "collectable": true, "deliverable": true, "globally_out_of_stock": false },
    { "product_id": "7163184", "known": true, "collectable": true, "deliverable": true, "globally_out_of_stock": false }
  ]
}
```

Read it as: the 9 stores ran from 0.49 to 1.54 miles (5 collection points, 2 Argos stores inside Sainsbury's, 2 standalone Argos stores). The Russell Hobbs Worcester kettle (8377058) could be collected right away at 4 of them and from tomorrow at the 5 collection points; the Ninja Foodi air fryer (7163184) right away at 2, from tomorrow at 6 and from Monday at 1. Both could be delivered to SW1A 1AA next day, not by Fast Track. Quote delivery from `state` and `message`: in this capture `available_from` on delivery read 2026-11-21 while the message said tomorrow. Near the rural postcode LL55 4UY the same two products returned 10 stores from 13.74 miles (Bangor Argos) to 47.77 miles, the kettle `collect_now` at 7 of them, and delivery as `state: "other"` with the message "Delivery within 2 days to LL554UY".

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/argos/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "air fryer"}'
```

Captured `data` (2026-11-21, 2 credits; 2 of 24 items shown, `image` and `facets` omitted):

```json
{
  "query": "air fryer",
  "sort": "relevance",
  "filters": {},
  "page": 1,
  "page_size": 24,
  "total": 152,
  "total_pages": 7,
  "has_more": true,
  "count": 24,
  "tu_clothing_excluded": 0,
  "currency": "GBP",
  "items": [
    {
      "product_id": "7163184",
      "url": "https://www.argos.co.uk/product/7163184/",
      "name": "Ninja Foodi AF200UK 4-in-1 7.6L Air Fryer - Black",
      "brand": "Ninja",
      "price": 99.99,
      "was_price": 159.99,
      "save": 60,
      "offer_text": "Save £60.00",
      "currency": "GBP",
      "clearance": false,
      "badges": ["VALUE_amazing_deals"],
      "rating": 4.85,
      "review_count": 1246,
      "seller": "argos",
      "deliverable": true,
      "reservable": true,
      "buyable": true,
      "free_delivery": false,
      "delivery_cost": 4.95,
      "has_variations": false,
      "argos_pay": { "available": true, "offering": "Normal credit", "message": "Available credit options" }
    },
    {
      "product_id": "1486630",
      "url": "https://www.argos.co.uk/product/1486630/",
      "name": "Cookworks 9L Dual Air Fryer - Black",
      "brand": "Cookworks",
      "price": 50,
      "was_price": 100,
      "save": 50,
      "offer_text": "Half Price",
      "currency": "GBP",
      "clearance": false,
      "badges": ["Black_Friday", "price_guarantee"],
      "rating": 4.8,
      "review_count": 1700,
      "seller": "argos",
      "deliverable": true,
      "reservable": true,
      "buyable": true,
      "free_delivery": false,
      "delivery_cost": 4.95,
      "has_variations": false,
      "argos_pay": { "available": true, "offering": "Normal credit", "message": "Available credit options" }
    }
  ]
}
```

The answer carried 13 facets, among them `category`, `sold by` (`argos` 103, `trusted sellers` 49), `offers and clearance` (`blackfriday`, `specialoffer`, `clearance`), `brands`, `price`, `customer rating`, `colour group` and category-specific ones such as `capacity range (litres)`. All 24 items on page 1 were sold by Argos; narrow with `seller: "trusted_seller"` to see the marketplace items. `/category` with `{"category_id": "29560"}` (Kettles) returned 303 products in 13 pages, the first the Russell Hobbs Worcester kettle at £21.50 against £43 (`offer_text` "Half Price").

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/argos/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "8377058"}'
```

Captured `data` (2026-11-21, 2 credits; trimmed to the price, badge and availability fields: `description`, `features`, `images`, `care_plans`, `payment_options`, `bundles`, `breadcrumb`, `secondary_ratings` and the 10 `reviews` dropped):

```json
{
  "product_id": "8377058",
  "requested_id": "8377058",
  "url": "https://www.argos.co.uk/product/8377058/",
  "template": "argos",
  "name": "Russell Hobbs 25511 Worcester Stainless Steel Kettle - Black",
  "brand": "Russell Hobbs",
  "seller": "argos",
  "seller_name": "Argos",
  "ean": "4008496976201",
  "price": 21.5,
  "was_price": 43,
  "save": 21.5,
  "offer_text": "Half Price",
  "currency": "GBP",
  "badges": [
    { "badge": "price_guarantee", "type": "BADGE_PRODUCT", "text": null, "starts_at": "2026-10-30T00:00:00.000Z", "ends_at": "2026-12-02T00:00:00.000Z" },
    { "badge": "Black_Friday", "type": "BADGE_VALUE", "text": null, "starts_at": "2026-10-30T00:00:00.000Z", "ends_at": "2026-12-02T00:00:00.000Z" },
    { "badge": "INFO_exclusive", "type": "BADGE_PRODUCT", "text": null, "starts_at": "2026-07-25T00:00:00.000Z", "ends_at": "2027-02-01T00:00:00.000Z" }
  ],
  "collection": "Russell Hobbs Worcester",
  "variants": [],
  "special_offers": [],
  "nectar_points": 21,
  "argos_pay": true,
  "dimensions": null,
  "energy_class": null,
  "deliverable": true,
  "collectable": true,
  "delivery_price": 4.95,
  "free_delivery": false,
  "fast_track": false,
  "globally_out_of_stock": false,
  "end_of_line": false,
  "max_quantity": 10,
  "made_to_order": false,
  "age_restricted": false,
  "rating": 4.64,
  "review_count": 6336,
  "recommended_percent": 93,
  "rating_distribution": { "1": 108, "2": 76, "3": 221, "4": 1160, "5": 4768 },
  "question_count": 95,
  "answer_count": 170
}
```

`care_plans[]` held 2 Replacement Care plans (2 years at £3.99, 3 years at £6.99) and `bundles[]` 12 frequently-bought-together items with their prices. The first 10 `reviews` use `submitted` (the page's date text, "20 November 2026") and `reviewed_product` {`product_id`, `name`}; the `/reviews` endpoint uses `submitted_at` (ISO) and `reviewed_product_id`. Reviews are shared across a product's colours and sizes: the kettle's first reviews were written on its Metallic version (8888822). A **Trusted Seller** product (`template: "trusted_seller"`) carries `product_id`, `requested_id`, `url`, `name`, `brand`, `seller` (`trusted_seller`), `seller_name` (`null`: the page names no seller), `ean`, `price`, `was_price`, `save`, `offer_text`, `currency`, `condition`, `description`, `images`, `breadcrumb`, `deliverable`, `collectable`, `delivery_price`, `free_delivery`, `argos_pay` (`false`), `rating` and `review_count` (`null`).

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/argos/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "7163184"}'
```

Captured `data` (2026-11-21, 2 credits; 1 of 20 reviews shown, `secondary_averages` trimmed):

```json
{
  "product_id": "7163184",
  "sort": "newest",
  "rating": null,
  "page": 1,
  "limit": 20,
  "total": 1251,
  "has_more": true,
  "count": 20,
  "summary": "Ninja Foodi dual zone air fryer is praised for fast, even cooking, easy use, dual drawers with sync feature, and great capacity. Some users mention learning curve and lack of recipe book.",
  "summary_source": "Argos's own AI-generated summary of the reviews",
  "stats": {
    "product_name": "Ninja Foodi AF200UK 4-in-1 7.6L Air Fryer - Black",
    "brand": "Ninja",
    "review_count": 1251,
    "average_rating": 4.85,
    "rating_distribution": { "1": 13, "2": 7, "3": 19, "4": 81, "5": 1131 },
    "recommended_percent": 96,
    "secondary_averages": [{ "label": "Ease of use", "average": 4.87 }],
    "first_review_at": "2025-01-28T10:27:06.000+00:00",
    "last_review_at": "2026-11-20T19:43:57.000+00:00"
  },
  "reviews": [
    {
      "id": "1237434172",
      "rating": 4,
      "title": "Ninja  4-in-1 Dual Zone Air Fryer 7.6L AF200UK",
      "text": "This is my first air fryer, so I have nothing to compare it with. So far, everything I’ve cooked has been successful and it’s easy to clean. Instructions aren't very clear for cooking something and I have had to buy a recipe book, would have been good to receive one with the air fryer. I wouldn't say it's an alternative to a frying pan, but it definitely saves on using the oven which is a win.",
      "submitted_at": "2026-11-19T11:18:44.000+00:00",
      "recommended": true,
      "helpful_count": 0,
      "not_helpful_count": 0,
      "secondary_ratings": [],
      "syndicated": true,
      "syndication_source": "sharkninja.eu",
      "argos_colleague": false,
      "badges": [],
      "photos": [],
      "reviewed_product_id": "7163184",
      "reviewed_product_name": "Ninja Foodi 4-in-1 Dual Zone Air Fryer 7.6L AF200UK",
      "brand_response": null
    }
  ]
}
```

On this page 6 of the 20 reviews were syndicated from `sharkninja.eu` (the brand's own site). `argos_colleague` marks a review written by an Argos colleague. `brand_response` is `{count, department, date}` when the brand replied: its presence and date only, never its text. `summary` is Argos's own AI-generated summary, not Scavio's: label it so when quoting it. With `limit: 100` and `page`, every review is reachable (`page * limit` up to `total`); `rating: [1, 2]` returns only 1- and 2-star reviews with their own `total`.

### Questions, stores, categories, deals and suggestions

- `/questions` with `{"product_id": "8377058"}`: `total` 95, 10 questions, such as "Quick shutoff?" with one `source: "staff"` answer (Argos's Q&A team). On that page 10 answers came from staff and 1 from a customer; `source` is `staff`, `brand` or `customer` and `best_answer` flags the one Argos marks. No asker or answerer names: a first name after a greeting is cut.
- `/stores` with `{"postcode": "M1 1AE"}`: 7 stores from 0.5 miles (Manchester Arndale Argos, `store` `661-manchester-arndale-argos`) to 3.74 miles, 2 standalone, 3 inside Sainsbury's and 2 collection points, each with address, phone and `hours` by weekday, and no stock (use `/store-stock`). `{"store": "661-manchester-arndale-argos"}` returns one store with `opening_hours`, `hours`, `special_hours` [{`date`, `open`, `close`, `closed`}] for holiday and seasonal hours, and `services`.
- `/categories`: 14 departments (Christmas, Toys, Technology, Gaming, Home & Furniture, Health & Beauty, Appliances, Sports & Leisure, Jewellery & Watches, Baby & Nursery, Clothing, Garden & DIY, Gifts & Occasions, Inspiration & Guides) and 856 links, such as `{"name": "Christmas Trees", "category_id": "29817"}`. A link with `category_id: null` is an event or guide page, not a category input.
- `/deals` with `{"collection": "black_friday"}`: `total` 3,081 in 129 pages, the first item a Morphy Richards 20L microwave at £45 against £70 (`offer_text` "Save £25.00", badges `Black_Friday`, `price_guarantee`). A Russell Hobbs microwave on the same page carried `offer_text` "Lowest Price" with `was_price: null`.
- `/suggestions` with `{"query": "lego"}`: 10 suggestions from `{"text": "lego", "weight": 1707148}` and `lego star wars` down to `lenovo tablet`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def argos(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/argos/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Two products near three postcodes (2 credits per postcode, up to 10 products per call)
ids = ["8377058", "7163184"]
for postcode in ("SW1A 1AA", "M1 1AE", "LL55 4UY"):
    res = argos("store-stock", {"product_ids": ids, "postcode": postcode})
    d = res["data"]
    for s in d["stores"]:
        for p in s["products"]:
            print(res["fetched_at"], postcode, s["name"], s["type"], s["distance_miles"], p["product_id"], p["state"], p["available_from"])
    for p in d["delivery"]["products"]:
        print(postcode, "delivery", p["product_id"], p["state"], p["message"])

# 2. The Black Friday list, page by page, with price, was price and badges (2 credits per page of 24)
rows, page = [], 1
while page <= 3:  # raise the cap for the whole list (129 pages in the capture)
    d = argos("deals", {"collection": "black_friday", "page": page})["data"]
    for i in d["items"]:
        rows.append((i["product_id"], i["name"], i["price"], i["was_price"], i["save"], i["offer_text"], i["badges"], i["seller"]))
    if not d["has_more"]:
        break
    page += 1
print(len(rows), "items")

# 3. The lowest-rated reviews of one product, 100 per page (2 credits per page)
low = argos("reviews", {"product_id": "7163184", "sort": "lowest_rating", "limit": 100})["data"]
for rv in low["reviews"]:
    print(rv["rating"], rv["syndicated"], rv["syndication_source"], rv["text"][:80])

# Store each answer with fetched_at and run this on a schedule: that stored series is
# your stock and price history (Argos publishes none).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached.

- **item** (search, category, deals) - `product_id`, `url`, `name`, `brand`, `price`, `was_price`, `save`, `offer_text`, `currency` (GBP), `clearance`, `badges[]` (badge codes), `rating`, `review_count`, `seller` (`argos` / `trusted_seller`), `deliverable`, `reservable` (in-store collection), `buyable`, `free_delivery`, `delivery_cost` (`null` on Trusted Seller items), `has_variations`, `argos_pay` {`available`, `offering`, `message`}, `image`.
- **search / category / deals** - `query` (search; optional on category and deals), `category_id` (category) or `collection` (deals), `sort`, `filters`, `page`, `page_size` (24), `total`, `total_pages`, `has_more`, `count`, `tu_clothing_excluded`, `currency`, `items[]`, `facets[]` {`name`, `label`, `values[]` {`value`, `label`, `count`, `children`}}. `top_100`: `collection`, `sort`, `page`, `page_size` (60), `total`, `total_pages`, `has_more`, `count`, `tu_clothing_excluded`, `currency`, `items[]` (no facets).
- **product** (`template: "argos"`) - `product_id`, `requested_id`, `url`, `template`, `name`, `brand`, `seller`, `seller_name`, `ean`, `price`, `was_price`, `save`, `offer_text`, `currency`, `badges[]` {`badge`, `type`, `text`, `starts_at`, `ends_at`}, `description`, `features[]` (the specification lines), `collection`, `images[]`, `variants[]` {`product_id`, `options` {Colour, Size ...}, `price`}, `special_offers[]` {`id`, `title`, `description`, `starts_at`, `ends_at`}, `nectar_points`, `care_plans[]` {`name`, `type`, `duration`, `price`, `currency`, `excess`, `promotion`, `product_id`}, `payment_options[]` {`provider`, `message`, `plans[]` {`offering`, `months`, `apr`, `promotional`}}, `argos_pay`, `bundles[]` {`product_id`, `name`, `price`, `url`}, `breadcrumb[]` {`name`, `category_id`, `url`}, `dimensions`, `energy_class`, `deliverable`, `collectable`, `delivery_price`, `free_delivery`, `fast_track`, `globally_out_of_stock`, `end_of_line`, `max_quantity`, `made_to_order`, `age_restricted`, `rating`, `review_count`, `recommended_percent`, `rating_distribution`, `secondary_ratings[]` {`label`, `average`}, `question_count`, `answer_count`, `reviews[]` (the first 10: `id`, `rating`, `title`, `text`, `submitted`, `recommended`, `helpful_count`, `not_helpful_count`, `secondary_ratings`, `syndicated`, `syndication_source`, `argos_colleague`, `photos`, `reviewed_product` {`product_id`, `name`}, `brand_response`). Trusted Seller template: see the Product example.
- **store-stock** - `postcode`, `delivery_postcode`, `max_distance`, `product_ids`, `count`, `stores[]` {`store_id`, `name`, `store`, `url`, `type`, `brand`, `distance_miles`, `address` {`lines`, `town`, `county`, `postcode`}, `latitude`, `longitude`, `phone`, `hours` {`monday`..`sunday`: [{`open`, `close`}]}, `special_hours`, `products[]` {`product_id`, `state`, `available_from`, `message`}}, `delivery` {`postcode`, `products[]` {`product_id`, `state`, `available_from`, `fast_track`, `message`}}, `products[]` {`product_id`, `known`, `collectable`, `deliverable`, `globally_out_of_stock`}.
- **stores** - near a postcode: `postcode`, `max_distance`, `count`, `stores[]` (the store-stock store shape without `products`). One store: `store_id`, `store`, `url`, `name`, `type`, `description`, `address` {`street`, `town`, `region`, `postcode`, `country`}, `latitude`, `longitude`, `phone`, `opening_hours`, `hours[]` {`day`, `open`, `close`}, `special_hours[]` {`date`, `open`, `close`, `closed`}, `services`.
- **reviews** - `product_id`, `sort`, `rating`, `page`, `limit`, `total`, `has_more`, `count`, `summary`, `summary_source`, `stats` {`product_name`, `brand`, `review_count`, `average_rating`, `rating_distribution`, `recommended_percent`, `secondary_averages[]`, `first_review_at`, `last_review_at`}, `reviews[]` {`id`, `rating`, `title`, `text`, `submitted_at`, `recommended`, `helpful_count`, `not_helpful_count`, `secondary_ratings[]` {`label`, `value`}, `syndicated`, `syndication_source`, `argos_colleague`, `badges`, `photos`, `reviewed_product_id`, `reviewed_product_name`, `brand_response` {`count`, `department`, `date`} or `null`}.
- **questions** - `product_id`, `sort`, `page`, `limit`, `total`, `has_more`, `count`, `questions[]` {`id`, `question`, `details`, `submitted_at`, `answer_count`, `answers[]` {`id`, `text`, `submitted_at`, `source`, `best_answer`, `helpful_count`, `not_helpful_count`}}.
- **categories** - `count`, `link_count`, `departments[]` {`name`, `category_id`, `url`, `groups[]` {`name`, `category_id`, `url`, `links[]` {`name`, `category_id`, `url`, `url_filters`}}}.
- **suggestions** - `query`, `count`, `suggestions[]` {`text`, `weight`}.

## Guardrails

- Store stock is a state and a collection time per store, never a unit count. Report it as what Argos showed at `fetched_at` for the stores the answer returned near that postcode (up to 10 within 50 miles), never as every store or as guaranteed stock. `collect_now` means the store could hand it over at the time of the call.
- Keep the two postcodes apart: `postcode` places the stores, `delivery_postcode` places the delivery check. Quote delivery from `state` and Argos's `message`.
- `save` is computed by Scavio from `price` and `was_price`; say so. `offer_text` and badges are Argos's own words and codes: quote Price Guarantee and Black Friday as Argos defines them, and never claim a price is the lowest or a was price a real reduction.
- Lists are 24 per page with a `total`: never call one page "all products" or present `total` as what was returned. Follow `has_more`. Tu Clothing items are left out (`tu_clothing_excluded`): Tu Clothing ids (starting `tuc`) have no product page on argos.co.uk.
- Sellers: `argos` items are sold by Argos; `trusted_seller` items are sold by marketplace sellers whose name the page does not show (`seller_name: null`). Never invent a seller name. Trusted Seller items are never stocked in Argos stores.
- Reviews: no reviewer names, locations, ages or genders are returned; never try to identify a reviewer. Flag syndicated reviews with their `syndication_source`. `summary` is Argos's own AI-generated summary: label it as Argos's. Reviews are shared across a product's variants (`reviewed_product_id`).
- Not available: unit counts, price history (poll and store), a brand directory (`brand` is a filter: values come from the `brands` facet), Argos Ireland, card or checkout prices, Argos Pay terms. This API cannot reserve, add to trolley, book Fast Track or buy.
- Terms: Scavio does not collect or store Argos data: each call fetches the public Argos page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Argos's terms of service cover how its service may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Argos product photos or logos; link products by `url` instead.
- Never fabricate prices, was prices, stock states, stores, reviews or ratings. Only return what the API returned, with the currency, the `fetched_at` time and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a postcode that is not a full UK postcode, more than 10 `product_ids`, a Trusted Seller id in `product_ids`, a Tu Clothing id (starting `tuc`), an id that is neither a 7-digit catalogue number nor an 8-character Trusted Seller id, a `url` that is not an argos.co.uk product link, both or neither of `product_id` / `url` (or `postcode` / `store`), a bare store id instead of `stores[].store`, `max_distance` above 50 or `max_results` above 10, `max_distance` / `max_results` with `store`, a `page` above 200 (Top 100: above 2), any input but `page` on `top_100`, `offers` on deals, `category` on category (use `category_id`), an unknown `sort`, `collection`, `seller` or `offers` value, `price_min` above `price_max`, more than 10 facets in `filters`, or a named input sent inside `filters`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Argos product with this id (or the product is no longer available on argos.co.uk).", "No Argos store with this reference (stores[].store, e.g. 661-manchester-arndale-argos).", "No Argos product with this id." (reviews, questions). Take ids and store references from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api).
- `502` means Argos data was temporarily unavailable ("Argos is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Argos is busy ("Argos is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.72.0
npm install scavio@0.73.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: stock } = await scavio.argos.storeStock({ product_ids: ["8377058", "7163184"], postcode: "SW1A 1AA" });
const { data: found } = await scavio.argos.search({ query: "air fryer", seller: "argos", sort: "price_low" });
const { data: product } = await scavio.argos.product({ product_id: "8377058" });
const { data: stores } = await scavio.argos.stores({ postcode: "M1 1AE" });
const { data: reviews } = await scavio.argos.reviews({ product_id: "7163184", sort: "lowest_rating", limit: 100 });
const { data: questions } = await scavio.argos.questions({ product_id: "8377058" });
const { data: tree } = await scavio.argos.categories();
const { data: kettles } = await scavio.argos.category({ category_id: "29560" });
const { data: deals } = await scavio.argos.deals({ collection: "black_friday", page: 1 });
const { data: typed } = await scavio.argos.suggestions({ query: "lego" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.argos.store_stock(...)`, `search`, `product`, `stores`, `reviews`, `questions`, `categories`, `category`, `deals` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all ten endpoints as tools: `search_argos`, `get_argos_product`, `get_argos_store_stock`, `get_argos_stores`, `get_argos_reviews`, `get_argos_questions`, `get_argos_categories`, `get_argos_category`, `get_argos_deals` and `get_argos_suggestions`. Argos is opt-in: add `argos` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.72.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,argos"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [store stock](https://scavio.dev/docs/argos-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api), [search](https://scavio.dev/docs/argos-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api), [product](https://scavio.dev/docs/argos-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api), [stores](https://scavio.dev/docs/argos-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api), [reviews](https://scavio.dev/docs/argos-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api), [questions](https://scavio.dev/docs/argos-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api), [categories](https://scavio.dev/docs/argos-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api), [category](https://scavio.dev/docs/argos-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api), [deals](https://scavio.dev/docs/argos-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api), [suggestions](https://scavio.dev/docs/argos-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api). Overview: [Argos API](https://scavio.dev/argos-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api).
