---
name: sportchek-api
description: SportChek API for SportChek (sportchek.ca, Canada's sporting goods retailer, a Canadian Tire Corporation banner) - Sport Chek prices in Canadian dollars with the was price and sale label SportChek shows, the sale's posted end date (sale_ends) and SportChek's own was-price footnote ("Was price reflects the last national regular price this product was sold for."), to set the same model next to Amazon.ca and Walmart.ca; keyword search and any category or deals page (clearance, sale, Black Friday) by path, 24 per page with total and pages, sorted by relevance, price or rating and filtered by brand, sale or clearance and any of SportChek's own filters (gender, size, colour, rating, price band) with their counts; per-colour prices and online units; one product by code or link with every colour and size (own price, was price, sale end date, units online and units at the store SportChek assigns to the request's region, which a caller cannot choose), specifications, features and breadcrumbs; customer reviews with the rating summary (the first 8, then 30 a page, up to 98 per sort and star filter; syndicated and incentivized reviews flagged, no reviewer names); search suggestions; one store with hours and up to 49 nearby stores; the brand list and the category tree. 8 endpoints, 1 credit per call; calls take about 10-90 seconds. English only. Not available - choosing a store, stores near a postal code, customer questions, the flyer, Triangle Rewards or CT Money prices, UPC, price history, cart or checkout.
version: 1.0.0
tags: sportchek, sport-chek, sportchek-ca, sportchek-api, sport-chek-api, sportchek-prices, sport-chek-prices, sportchek-sale, sport-chek-sale, sportchek-was-price, sportchek-sale-end-date, sportchek-clearance, sportchek-black-friday, sport-chek-black-friday, sportchek-deals, sportchek-stock, sportchek-reviews, sportchek-product-data, sportchek-brands, sportchek-categories, sportchek-stores, canadian-tire-corporation, canada, canadian-retail, cad, cad-prices, sporting-goods, sporting-goods-prices, winter-jackets, outerwear, hockey, hockey-equipment, footwear, price-comparison, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/sportchek-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api
---

# SportChek API - Sport Chek Prices, Sale Dates, Stock, Reviews

Read SportChek (sportchek.ca, Canada's sporting goods retailer, a Canadian Tire Corporation banner): keyword search, any category or deals page, one product in full with every colour and size, customer reviews, search suggestions, one store, the brand list and the category tree. Every answer is what SportChek's public pages show a visitor without an account at the moment of the call, in Canadian dollars. All 8 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages SportChek shows to any visitor and returns them as JSON for analysis. It uses no SportChek account, no Triangle login, no cart and no checkout.

**The job this skill is for: SportChek prices in CAD next to the same model at Amazon.ca and Walmart.ca.** Today's SportChek price, the was price and sale label SportChek shows, and the sale's posted end date, set beside the same brand, model, colour and size at Amazon.ca (`amazon-product-data`, `country: "ca"`) and Walmart.ca (`walmart-product-data`, `domain: "ca"`). Captured 2026-11-25: `/search` `{"q": "winter jacket", "include_facets": true}` listed 664 products over 28 pages; on page 1, 18 of 24 carried a was price and 13 a sale end date. The Columbia Men's Snowy Summit Jacket (81257430F) read 129.98 CAD, was price 229.99, `sale_ends` "December 2, 2026", label "ENDS December 2, 2026". Quote SportChek's own was-price definition next to the number: "Was price reflects the last national regular price this product was sold for." A percent off is computed from the two shown numbers and labelled computed (129.98 against 229.99 is 43.5% off, computed; SportChek's own text on that item reads "43% Off Our Regular Price of $229.99").

Ten limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint costs 1. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Calls are slow.** Page calls answer in about 10 to 90 seconds (reviews up to about 90, rarely more); brands and categories in a few seconds. Allow up to 2 minutes for an answer, set a client timeout of at least 240 seconds so a queued request is not cut off, and send one request at a time.
- **Prices as SportChek shows them.** `price` is the price for a visitor without an account, in CAD. `was_price` is SportChek's was price as given, only where SportChek shows one (clearance and some sale items), and `footnote` carries SportChek's definition of it. A promotion without a was price shows its own text in `price_message` (product 84166659F read 206.24 CAD with "25% Off* - Discount Applied. See details." and no was price). Never call a was price a "regular price", "MSRP" or a "real" or "fake" discount.
- **Sale end dates as given.** `sale_ends` is the end date SportChek posts ("December 2, 2026"); `price_message[].details` carries SportChek's own order cutoff where it gives one ("order must be completed by December 3, 2026 01:59 AM ET to qualify"). Quote them; never compute when a price will change.
- **Store stock is the assigned store's only.** `units_at_store` are the units at the store SportChek assigns to the request's region (`assigned_store`); a caller cannot choose a store. In our checks prices were the same at every store sampled. Report `units_at_store` with `assigned_store` every time, never as stock at a store you picked or "stock at every store". `units_online` are the online units.
- **Filters come from facets.** Send `include_facets: true` once to get SportChek's filters with counts, then pass them as `filters` `[{facet, value}]` (up to 6). `brand` takes the Brand Name value from facets (`BAUER`, `COLUMBIA`), not the spelling in `/brands`.
- **List paths come from categories.** `/list` takes a category path from `/categories` (`path`) or a deals page path under `/en/sale-clearance/` (the capture used `/en/sale-clearance/clearance.html`). `deals` (`sale`, `clearance`, `both`) works on search and category pages; on a deals page it is a `400` (the page already is one).
- **Reviews page in fixed sizes.** Page 1 is the first 8 reviews, pages 2-4 the next 30 each: up to 98 reviews per sort and star filter. `summary` counts all of the product's reviews; `total` counts the English reviews the page lists. `syndicated_from` names the brand site a review was first posted on, `incentivized` marks a review flagged as written for an incentive. No reviewer names are returned.
- **English only.** SportChek has no French storefront here: `language` other than `en` is a `400`, not charged. For French-language prices of the sister banner use `marks-api` (Mark's, with L'Equipeur in French).
- **What is not there.** No customer questions on SportChek, no UPC or barcode (the site shows none), no stores near a postal code, no flyer, no Triangle Rewards or CT Money prices, no price history (store your own answers with `fetched_at`), no cart or checkout.

SportChek publishes no public API for its catalog, prices, stock or reviews. SportChek's affiliate programme runs on Impact and offers publishers links, banners and reports; its page names no product feed. This skill reads SportChek's public pages with one Scavio key. Other vendors offer SportChek data tools; this skill reads SportChek's own public pages.

Canadian Tire Corporation's Q3 2026 results (quarter ended October 3, 2026; released November 12, 2026) report SportChek comparable sales up 3.2%, its ninth consecutive quarter of growth. Quote it with that source, never from the samples.

See also: `marks-api` (Mark's, the Canadian Tire Corporation workwear and casual clothing banner), `canadian-tire-api` (Canadian Tire, the same parent), `amazon-product-data` (Amazon.ca with `country: "ca"`) and `walmart-product-data` (Walmart.ca with `domain: "ca"`). Same brand, model, colour and size only: match on the full product name and the variant, show each price with its retailer, seller and date, and flag marketplace sellers on Amazon.ca and Walmart.ca rather than treating them as Amazon or Walmart.

## When to trigger

Use this skill when the user asks to:
- Read SportChek prices, was prices and sale end dates in CAD for a product, a search or a category
- Put a SportChek price next to the same model at Amazon.ca or Walmart.ca
- List a SportChek deals page (clearance, sale, Black Friday) sorted by price or rating
- Filter SportChek results by brand, gender, size, colour, rating, price band or sale and clearance
- Read one SportChek product with every colour and size, online units and the assigned store's units
- Read SportChek customer reviews with the rating summary, syndicated and incentivized flags
- Read SportChek's search suggestions, one store's hours and nearby stores, the brand list or the category tree

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, brands and categories took about 2 seconds, search and list about 12, store 18, suggestions 22, product 30 and reviews 32. Allow up to 2 minutes for an answer and a client timeout of at least 240 seconds.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/sportchek/search` | Products for keywords: price, was price, sale end date, promotion text, badges, review count, per-colour prices and online units; total, pages, sorts, filters, facets with counts on request, the was-price footnote | 1 |
| `POST /api/v1/sportchek/list` | One category or deals page (clearance, sale, Black Friday) by path or link, same items, sorts and filters as search | 1 |
| `POST /api/v1/sportchek/product` | One product by code or link: price, was price, sale end date, promotion text, rating, description, features, specifications, images, breadcrumbs, options, every variant with its own price and units, the assigned store | 1 |
| `POST /api/v1/sportchek/reviews` | Customer reviews of one product: rating summary, sort, star filter, 8 then 30 a page up to page 4, syndicated and incentivized flags, no names | 1 |
| `POST /api/v1/sportchek/suggestions` | SportChek's search-box suggestions for typed text: terms, top hit, categories, brands | 1 |
| `POST /api/v1/sportchek/store` | One store by number: address, phone, coordinates, time zone, weekly and special hours, curbside pickup, up to 49 nearby stores with distance | 1 |
| `POST /api/v1/sportchek/brands` | SportChek's brand pages: name, slug, url (164 in the capture) | 1 |
| `POST /api/v1/sportchek/categories` | SportChek's category tree with `path` for `/list` (1033 categories under 10 top-level ones in the capture) | 1 |

## Market

Canada only, English, CAD: every answer carries `market` {`banner` "SportChek", `site`, `host`, `language` "en", `country` "ca", `currency` "CAD"}. There is no `country` input.

## Prices, sale dates, variants and stock

| Field | Meaning |
|---|---|
| `price` | The price SportChek shows a visitor without an account, CAD. `price_max` is set when the colours or sizes span a range |
| `was_price` | SportChek's was price as given, only where SportChek shows one; `null` otherwise |
| `footnote` | SportChek's own sentence on was prices: "Was price reflects the last national regular price this product was sold for." Quote it with any was price |
| `on_sale`, `sale_ends` | Whether SportChek marks the item on sale, and the end date it posts ("December 2, 2026"), as given |
| `price_message[]` | {`label`, `details`}: SportChek's promotion text as given ("ENDS December 2, 2026"; "25% Off* - Discount Applied. See details."; "Final Sale*") |
| `badges` | SALE, CLEARANCE, TOPRATED, BESTSELLER, NEWARRIVAL as SportChek shows them |
| `colours[]` (search, list) | Each colour's own `price`, `was_price`, `on_sale`, `sale_ends` and `units_online_max` (the most online units of any one size in that colour) |
| `variants[]` (product) | Each colour and size: `sku`, `colour`, `size`, `width`, own price, was price, sale end date, `units_at_store`, `units_online`, `ship_to_home`, `store_pickup`, `sellable` |
| `assigned_store` (product) | {`id`, `name`, `city`, `province`}: the store SportChek assigns to the request's region. `units_at_store` are its units; it is not chosen by the caller |

- **Percent off:** compute it from `price` and `was_price` as shown, and label it computed. Where there is no `was_price`, quote `price_message` as given instead of computing a discount.
- **Colours differ:** one product can carry a was price on one colour and none on another (in the capture a Ripzone Women's Friday Short Puffer Jacket read 83.99 CAD in BLACK BEAUTY with no was price, and 64.97 with a was price of 129.99 in GARDENIA). Compare at the colour and size level.
- **Assigned store:** the store can change between calls. Record `assigned_store` with every `units_at_store` number.

## Workflow

1. **Find the product.** `/search` with `q` and `include_facets: true` on the first call; narrow with `brand` or `filters` from `facets`. Note `total` and `total_pages`.
2. **Read the variant.** `/product` with `code` (`items[].code`, e.g. `84166659F`) for each colour and size, its price, was price, `sale_ends`, `units_online` and the assigned store's units.
3. **Match elsewhere.** `amazon-product-data` with `country: "ca"` and `walmart-product-data` with `domain: "ca"` for the same brand, model, colour and size. Keep a row only when the names and variants match; record each seller.
4. **Report.** Each price with its retailer, CAD, the capture date and "before tax and shipping"; SportChek's was price with the footnote; a percent off labelled computed; the sale end date as SportChek posts it.
5. **A deals page.** `/list` with `path` (`/en/sale-clearance/clearance.html`) and `sort: "price_low"`; categories come from `/categories` (`path`).
6. **Reviews.** `/reviews` with `code`; read `summary`, then page 2-4 for more (30 a page), with the same `sort` and `rating` on every page.
7. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`) and list (`/list`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | required (search) | Keywords or a product code, up to 200 chars |
| `path` | string | one of (list) | A category path from `/categories` (`/en/cat/...-DC....html`) or a deals page path under `/en/sale-clearance/` |
| `url` | string | one of (list) | The page link instead of `path` (not both) |
| `page` | integer | 1 | Page number; 24 a page (`page_size` says), `total_pages` says how many |
| `sort` | string | `relevance` | `relevance`, `price_high`, `price_low`, `rating` |
| `brand` | string or list | none | Brand Name value from facets (`BAUER`), up to 10 |
| `deals` | string or list | none | `sale`, `clearance` or `both`. Not on a deals page (`400`) |
| `filters` | list | none | Up to 6 `{facet, value}` from `facets[].values[]` (`{"facet": "sku_gender_attr", "value": "Female"}`, `{"facet": "pricerange", "value": "50 - 99.99"}`); `value` one or a list |
| `include_facets` | boolean | false | Also return SportChek's filters with counts (still 1 credit) |
| `language` | string | `en` | `en` only |

### Product (`/product`) and reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `code` | string | one of | A SportChek product code (`items[].code`, digits and a letter: `84166659F`) |
| `url` | string | one of | A SportChek product link (`items[].url`), instead of `code` (not both) |
| `page` | integer | 1 | Reviews only: 1-4 (page 1 the first 8, then 30 each) |
| `sort` | string | `newest` | Reviews only: `newest`, `relevance`, `helpful`, `rating_high`, `rating_low` |
| `rating` | integer | none | Reviews only: only reviews with this many stars (1-5) |

### Suggestions, store, brands, categories

`/suggestions` takes `q` (the text typed so far, up to 100 chars). `/store` takes `store_id` (a store number: `assigned_store.id` or `nearby_stores[].id`, e.g. `272`). `/brands` takes an optional `letter` (one letter or digit). `/categories` takes no input (send `{}`).

## Examples

### Search with facets

```bash
curl -X POST https://api.scavio.dev/api/v1/sportchek/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "winter jacket", "include_facets": true}'
```

Captured `data` (2026-11-25; `items` cut to 2 of 24, `facets` to 1 of 18, `image` and `notes` dropped):

```json
{
  "query": "winter jacket",
  "corrected_query": null,
  "redirected_to": null,
  "market": {"banner": "SportChek", "site": "SportChek", "host": "www.sportchek.ca", "language": "en", "country": "ca", "currency": "CAD"},
  "total": 664,
  "total_pages": 28,
  "page": 1,
  "page_size": 24,
  "has_more": true,
  "count": 24,
  "sort": "relevance",
  "filters_applied": [],
  "items": [
    {"position": 4, "code": "81257430F", "name": "Columbia Men's Snowy Summit Jacket", "brand": "COLUMBIA", "url": "https://www.sportchek.ca/en/pdp/columbia-men-s-snowy-summit-jacket-81257430f.html", "price": 129.98, "price_max": null, "was_price": 229.99, "currency": "CAD", "on_sale": true, "sale_ends": "December 2, 2026", "price_message": [{"label": "ENDS December 2, 2026", "details": "43% Off Our Regular Price of $229.99. Selection & availability may vary by location, order must be completed by December 3, 2026 01:59 AM ET to qualify"}], "badges": ["TOPRATED", "SALE"], "rating": null, "review_count": 52, "colours": [{"name": "BLACK--010", "price": 129.98, "was_price": 229.99, "on_sale": true, "sale_ends": "December 2, 2026", "units_online_max": 1743}, {"name": "CANOE - 262", "price": 129.98, "was_price": 229.99, "on_sale": true, "sale_ends": "December 2, 2026", "units_online_max": 678}], "sponsored": false},
    {"position": 1, "code": "80867124F", "name": "Ripzone Men's Berkley Quilted Parka Jacket", "brand": "RIPZONE", "url": "https://www.sportchek.ca/en/pdp/ripzone-men-s-berkley-quilted-parka-jacket-80867124f.html", "price": 124.97, "price_max": null, "was_price": 249.99, "currency": "CAD", "on_sale": true, "sale_ends": null, "price_message": [], "badges": ["BESTSELLER", "TOPRATED", "CLEARANCE"], "rating": null, "review_count": 14, "colours": [{"name": "BLACK", "price": 124.97, "was_price": 249.99, "on_sale": true, "sale_ends": null, "units_online_max": 1}, {"name": "GREEN", "price": 124.97, "was_price": 249.99, "on_sale": true, "sale_ends": null, "units_online_max": 4}], "sponsored": false}
  ],
  "facets": [
    {"id": "deals", "label": "Deals", "type": "multiselect", "values": [{"label": "Sale", "count": 347, "facet": "deals", "value": "Sale", "selected": false}, {"label": "Clearance", "count": 281, "facet": "deals", "value": "Clearance", "selected": false}]}
  ],
  "footnote": "Was price reflects the last national regular price this product was sold for."
}
```

The Ripzone parka is a clearance item with a was price and no `sale_ends`; the Columbia jacket is on sale until the posted date. Computed from the shown numbers: 129.98 against 229.99 is 43.5% off, 124.97 against 249.99 is 50.0% off (both computed). The 18 facets included Gender, Size, Brand Name, Deals, Colour, Rating, Price, Save % and Activity/Sports.

### One product with variants and the assigned store

```bash
curl -X POST https://api.scavio.dev/api/v1/sportchek/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "84166659F"}'
```

Captured `data` (2026-11-25; `variants` cut to 2 of 29, variant `options` and `price_message`, `description`, `features`, `specifications`, `images`, `breadcrumbs`, `options`, `style_codes` and `notes` dropped):

```json
{
  "market": {"banner": "SportChek", "site": "SportChek", "host": "www.sportchek.ca", "language": "en", "country": "ca", "currency": "CAD"},
  "requested_code": "84166659F",
  "code": "84166659F",
  "name": "Columbia Women's Amaze Puff™ Down Jacket",
  "brand": "COLUMBIA",
  "url": "https://www.sportchek.ca/en/pdp/columbia-women-s-amaze-pufftm-down-jacket-84166659f.html",
  "price": 206.24,
  "price_max": null,
  "was_price": null,
  "currency": "CAD",
  "on_sale": true,
  "sale_ends": "December 1, 2026",
  "price_message": [
    {"label": "25% Off* - Discount Applied. See details.", "details": "COLUMBIA Promotion: Take 25% off our in-store ticket price on select styles. Excluding accessories and items already marked down or on clearance. Selection and availability may vary by store location, and sales effective dates may vary by region. Offers may not be available at all store locations. This offer cannot be combined with any other promotional offer and/or promo codes, including but not limited to Buy One Get One offers and Two For offers. Orders must be completed by December 2, 2026 12:59 AM ET to qualify."}
  ],
  "badges": ["BESTSELLER", "TOPRATED"],
  "rating": 4.66,
  "review_count": 59,
  "status": "ACTIVE",
  "variant_count": 29,
  "variants": [
    {"sku": "334703523", "colour": "BLACK", "size": "M", "width": null, "style_code": "334553259", "price": 206.24, "was_price": null, "on_sale": true, "sale_ends": "December 1, 2026", "badges": ["SALE"], "units_at_store": 6, "units_online": 251, "ship_to_home": true, "store_pickup": true, "sellable": true, "max_per_order": null},
    {"sku": "334553260", "colour": "BLACK_010", "size": "XS", "width": null, "style_code": "334553259", "price": 206.24, "was_price": null, "on_sale": true, "sale_ends": "December 1, 2026", "badges": ["SALE"], "units_at_store": 0, "units_online": 0, "ship_to_home": true, "store_pickup": true, "sellable": true, "max_per_order": null}
  ],
  "assigned_store": {"id": "237", "name": "SC CORNWALL - BROOKDALE SQUARE", "city": "CORNWALL", "province": "ON"},
  "footnote": "Was price reflects the last national regular price this product was sold for."
}
```

No was price here: the promotion is in `price_message`, so quote it rather than computing a discount. Across the 29 variants the assigned store (237, Cornwall, ON) held 48 units in 20 variants and `units_online` summed to 3,626. The notes say "The site shows no UPC or barcode."

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/sportchek/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "84166659F"}'
```

Captured `data` (2026-11-25; `reviews` cut to 1 of 8, `title`, `text`, `url`, `market` and `notes` dropped):

```json
{
  "code": "84166659F",
  "name": "Columbia Women's Amaze Puff™ Down Jacket",
  "summary": {
    "average": 4.66,
    "count": 59,
    "distribution": {"1": 3, "2": 0, "3": 4, "4": 0, "5": 52},
    "recommended": {"yes": 40, "no": 5},
    "question_count": 0
  },
  "sort": "newest",
  "rating": null,
  "page": 1,
  "page_size": 8,
  "total": 59,
  "total_pages": 3,
  "max_page": 4,
  "has_more": true,
  "count": 8,
  "reviews": [
    {"id": "274111701", "rating": 5, "date": "2026-11-18T11:43:48.000+00:00", "recommended": true, "verified_purchaser": true, "syndicated_from": "columbia.com", "incentivized": true, "helpful_yes": 0, "helpful_no": 0, "locale": "en_US", "secondary_ratings": []}
  ]
}
```

6 of the 8 reviews on page 1 read `syndicated_from` "columbia.com" and 4 were `incentivized`. Report them as SportChek lists them, with the flags; never quote reviewer names (none are returned).

### List, store, suggestions, brands, categories

- `/list` `{"path": "/en/sale-clearance/clearance.html", "sort": "price_low"}`: `total` 4656, `total_pages` 195, `page_size` 24; first a Ripzone Girls' Cartoon Animals Invisible Socks - 3 Pack at 1.88 CAD, was price 5.97, badge CLEARANCE, `price_message` "Final Sale*".
- `/store` `{"store_id": "272"}`: SC RICHMOND CENTRE, Richmond, BC, `timezone` America/Vancouver, weekly `hours`, `curbside_pickup` false and 11 `nearby_stores` (nearest SC VANCOUVER - SW MARINE DRIVE at 5.62 km). Finding stores near a postal code is not supported.
- `/suggestions` `{"q": "bauer"}`: 20 `terms` ("bauer skates", "bauer hockey stick", "bauer helmet" ...), `top_hit` "bauer".
- `/brands` `{}`: 164 brands with `name`, `slug`, `url` (name spelled from the brand page link; filter search with the Brand Name value from facets).
- `/categories` `{}`: `total_categories` 1033 under 10 top-level categories (Accessories, Activities And Equipment, Fan Shop, Kids, Men, New Arrivals, Outdoor, Shoes, Shop by Sport, Women), each with `path` for `/list`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def sportchek(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/sportchek/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# Was prices and sale end dates on page 1 (1 credit)
d = sportchek("search", {"q": "winter jacket", "sort": "relevance"})["data"]
print(d["total"], d["footnote"])
for i in d["items"]:
    off = None
    if i["was_price"]:
        off = round(100 * (i["was_price"] - i["price"]) / i["was_price"], 1)  # computed
    print(i["code"], i["name"], i["price"], i["was_price"], off, i["sale_ends"])

# One product: every variant with the assigned store's units (1 credit)
p = sportchek("product", {"code": "84166659F"})["data"]
store = p["assigned_store"]
for v in p["variants"]:
    print(v["colour"], v["size"], v["price"], v["units_online"], v["units_at_store"], store["id"], store["city"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` and `notes`.

- **item** (search, list) - `position`, `code`, `name`, `brand`, `url`, `image`, `price`, `price_max`, `was_price`, `currency`, `on_sale`, `sale_ends`, `price_message[]` {`label`, `details`}, `badges`, `rating`, `review_count`, `colours[]` {`name`, `price`, `was_price`, `on_sale`, `sale_ends`, `units_online_max`}, `sponsored`.
- **search** - `query`, `corrected_query`, `redirected_to`, `total`, `total_pages`, `page`, `page_size`, `has_more`, `count`, `sort`, `filters_applied`, `items[]`, `facets[]` (with `include_facets`: {`id`, `label`, `type`, `values[]` {`label`, `count`, `facet`, `value`, `selected`}}), `footnote`.
- **list** - `path`, `url`, then as search from `total`.
- **product** - `requested_code`, `code`, `name`, `brand`, `url`, `price`, `price_max`, `was_price`, `currency`, `on_sale`, `sale_ends`, `price_message`, `badges`, `rating`, `review_count`, `description`, `features`, `specifications[]` {`label`, `value`}, `images`, `breadcrumbs[]` {`name`, `id`, `url`}, `options[]` {`type`, `label`, `values`}, `style_code`, `style_codes`, `status`, `variant_count`, `variants[]` {`sku`, `colour`, `size`, `width`, `options`, `style_code`, `price`, `was_price`, `on_sale`, `sale_ends`, `price_message`, `badges`, `units_at_store`, `units_online`, `ship_to_home`, `store_pickup`, `sellable`, `max_per_order`}, `assigned_store` {`id`, `name`, `city`, `province`}, `footnote`.
- **reviews** - `code`, `name`, `url`, `summary` {`average`, `count`, `distribution`, `recommended` {`yes`, `no`}, `question_count`}, `sort`, `rating`, `page`, `page_size`, `total`, `total_pages`, `max_page`, `has_more`, `count`, `reviews[]` {`id`, `rating`, `title`, `text`, `date`, `recommended`, `verified_purchaser`, `syndicated_from`, `incentivized`, `helpful_yes`, `helpful_no`, `locale`, `secondary_ratings`}.
- **suggestions** - `query`, `count`, `terms`, `top_hit`, `categories`, `brands`.
- **store** - `id`, `name`, `url`, `address` {`line1`, `line2`, `city`, `province`, `province_code`, `postal_code`, `country`}, `phone`, `latitude`, `longitude`, `timezone`, `hours[]` {`day`, `open`, `close`, `closed`}, `special_hours`, `curbside_pickup`, `services`, `nearby_stores[]` {`id`, `name`, `city`, `province_code`, `distance_km`}, `nearby_count`.
- **brands** - `letter`, `total_brands`, `count`, `brands[]` {`name`, `slug`, `url`}.
- **categories** - `total_categories`, `count` (top-level), `categories[]` {`id`, `name`, `path`, `url`, `level`, `children[]`}.

## Guardrails

- Name it "SportChek (sportchek.ca, Canada's sporting goods retailer, a Canadian Tire Corporation banner)" on first mention, "SportChek" after that.
- Prices: quote each with CAD, the `fetched_at` date and "before tax and shipping" ("listed on sportchek.ca on Nov 25, 2026, before tax and shipping"). Online prices and sale dates can differ in store and by region.
- Was prices: quote SportChek's footnote next to any was price. A percent off is computed from the two shown numbers and labelled computed. Never "real" or "fake" discount, never "MSRP", no verdicts on a sale.
- Comparisons: same brand, model, colour and size only, each price with its retailer, seller and date. No price-match advice and no Triangle Rewards or CT Money values.
- Stock: `units_at_store` only with the `assigned_store` it belongs to. Never promise stock for a store the user chooses, or at every store.
- Reviews: no reviewer names (none are returned). Report ratings and counts; do not summarise reviews into claims about a product.
- Descriptive only: no commentary on SportChek's business, pricing practices or policies. Quote Canadian Tire Corporation figures only with their release and quarter.
- Do not republish SportChek product photos, descriptions or logos. Write sportchek.ca as plain text and cite product names, codes and capture dates rather than linking SportChek pages.
- Terms: Scavio does not collect or store SportChek data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account, no Triangle login, no cart and no checkout. SportChek's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, was prices, sale dates, codes, stores, units or reviews. Only return what the API returned, with the `fetched_at` time.
- Not available: choosing a store for price or stock, stores near a postal code, customer questions, the flyer, Triangle Rewards or CT Money prices, price history (store your own), UPC or barcodes, a French storefront, cart or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `q`; list without `path` or `url`, or both; a path that is not a SportChek category or deals page ("Paths come from categories."); `deals` on a deals page ("deals is not used on a deals page (the page already is one): use it with search or a category page."); `deals` other than `sale`, `clearance` or `both`; more than 6 `filters`, or a `facet` not taken from `facets[].values[].facet`; product or reviews without `url` or `code`, or both; a code that is not digits and a letter; reviews `page` outside 1-4 or `rating` outside 1-5; a `store_id` that is not digits; `language` other than `en` ("language must be en: SportChek has no French storefront (its French links open the English site).").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "SportChek has no product with the code <code>.", "SportChek has no page at <path>. Category paths come from categories.", "SportChek has no store number <id>.". Take codes, paths and store numbers from a previous answer rather than guessing them. A search with no matches is a `200` with `count` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api).
- `502` means SportChek data was temporarily unavailable ("SportChek is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy: wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.90.0
npm install scavio@0.91.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: jackets } = await scavio.sportchek.search({ q: "winter jacket", include_facets: true });
const { data: clearance } = await scavio.sportchek.list({ path: "/en/sale-clearance/clearance.html", sort: "price_low" });
const { data: product } = await scavio.sportchek.product({ code: "84166659F" });
const { data: reviews } = await scavio.sportchek.reviews({ code: "84166659F", sort: "newest" });
const { data: store } = await scavio.sportchek.store({ store_id: "272" });
const { data: tree } = await scavio.sportchek.categories();
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.sportchek.search(...)`, `list`, `product`, `reviews`, `suggestions`, `store`, `brands` and `categories`, with the same parameter names as keyword arguments. Give the client a timeout of at least 240 seconds for these calls.

## MCP

The Scavio MCP server exposes all 8 endpoints as tools: `search_sportchek`, `get_sportchek_list`, `get_sportchek_product`, `get_sportchek_reviews`, `get_sportchek_suggestions`, `get_sportchek_store`, `get_sportchek_brands` and `get_sportchek_categories`. SportChek is opt-in: add `sportchek` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.90.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,sportchek"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/sportchek-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api), [list](https://scavio.dev/docs/sportchek-list?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api), [product](https://scavio.dev/docs/sportchek-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api), [reviews](https://scavio.dev/docs/sportchek-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api), [suggestions](https://scavio.dev/docs/sportchek-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api), [store](https://scavio.dev/docs/sportchek-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api), [brands](https://scavio.dev/docs/sportchek-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api), [categories](https://scavio.dev/docs/sportchek-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api). Overview: [SportChek API](https://scavio.dev/sportchek-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=sportchek-api).
