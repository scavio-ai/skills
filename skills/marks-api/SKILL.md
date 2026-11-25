---
name: marks-api
description: Mark's API for Mark's (marks.com, the Canadian workwear, casual clothing and footwear retailer, a Canadian Tire Corporation banner; L'Equipeur in French) - Mark's Work Wearhouse prices in Canadian dollars with the was price and sale label Mark's shows, the sale's posted end date (sale_ends) and Mark's own was-price footnote ("Was price reflects the last national regular price this product was sold for."), to set the same work boot, jacket or pant next to Amazon.ca and Walmart.ca; keyword search and any category or deals page by path, 24 per page (12 on category pages) with total and pages, sorted by relevance, price or rating and filtered by brand, sale or clearance and any of Mark's own filters (gender, shoe size, width, CSA features, colour, rating, price band) with their counts; per-colour prices and online units; one product by code or link with every colour, size and width (own price, was price, sale end date, units online and units at the store Mark's assigns to the request's region, which a caller cannot choose), specifications, features and breadcrumbs; the newest 10 customer questions with answers (brand answers flagged, no asker names); search suggestions; one store with hours and up to 49 nearby stores; the brand list and the category tree. language fr reads L'Equipeur (lequipeur.com, the same product codes and CAD prices, French titles) on search, list, product, brands and categories. 8 endpoints, 1 credit per call; calls take about 10-90 seconds. Not available - customer reviews (rating and review count only), choosing a store, stores near a postal code, the flyer, Triangle Rewards or CT Money prices, UPC, price history, cart or checkout.
version: 1.0.0
tags: marks, marks-com, marks-api, marks-work-wearhouse, marks-work-warehouse, mark-s, lequipeur, l-equipeur, marks-prices, marks-sale, marks-was-price, marks-sale-end-date, marks-black-friday, marks-clearance, marks-work-boots, marks-workwear, marks-stock, marks-questions, marks-product-data, marks-brands, marks-categories, marks-stores, dakota-workpro, helly-hansen-workwear, carhartt, work-boots, workwear, workwear-prices, canadian-tire-corporation, canada, canadian-retail, cad, cad-prices, french, quebec, price-comparison, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/marks-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api
---

# Mark's API (Mark's Work Wearhouse) - Workwear Prices, Sale Dates, Stock

Read Mark's (marks.com, the Canadian workwear, casual clothing and footwear retailer, a Canadian Tire Corporation banner; L'Equipeur in French): keyword search, any category or deals page, one product in full with every colour, size and width, customer questions, search suggestions, one store, the brand list and the category tree. Every answer is what Mark's public pages show a visitor without an account at the moment of the call, in Canadian dollars; `language: "fr"` reads the same catalogue on L'Equipeur (lequipeur.com) in French. All 8 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Mark's and L'Equipeur show to any visitor and returns them as JSON for analysis. It uses no Mark's account, no Triangle login, no cart and no checkout.

**The job this skill is for: Mark's prices in CAD next to the same model at Amazon.ca and Walmart.ca.** Today's Mark's price, the was price and sale label Mark's shows, and the sale's posted end date, set beside the same brand, model, colour, size and width at Amazon.ca (`amazon-product-data`, `country: "ca"`) and Walmart.ca (`walmart-product-data`, `domain: "ca"`). Captured 2026-11-25: `/search` `{"q": "work boots"}` listed 1001 products over 42 pages; on page 1, 11 of 24 carried a was price and 10 the sale end date "November 25, 2026". The Dakota WorkPro Series Men's Steel Toe Composite Plate 6114 Quad Comfort Freshtech 6 Inch Work Boots (75983776F) read 124.99 CAD, was price 199.99. Quote Mark's own was-price definition next to the number: "Was price reflects the last national regular price this product was sold for." A percent off is computed from the two shown numbers and labelled computed (124.99 against 199.99 is 37.5% off, computed).

Ten limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint costs 1. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Calls are slow.** Page calls answer in about 10 to 90 seconds, rarely more; brands and categories in a few seconds. Allow up to 2 minutes for an answer, set a client timeout of at least 240 seconds so a queued request is not cut off, and send one request at a time.
- **Prices as Mark's shows them.** `price` is the price for a visitor without an account, in CAD. `was_price` is Mark's was price as given, only where Mark's shows one (clearance and some sale items), and `footnote` carries Mark's definition of it. A promotion without a was price shows its own text in `price_message`. Never call a was price a "regular price", "MSRP" or a "real" or "fake" discount.
- **Sale end dates as given.** `sale_ends` is the end date Mark's posts ("November 25, 2026"). Quote it as given; never compute when a price will change.
- **Store stock is the assigned store's only.** `units_at_store` are the units at the store Mark's assigns to the request's region (`assigned_store`); a caller cannot choose a store. In our checks prices were the same at every store sampled. The assigned store can change between calls (the same boot read store 114, Montreal, on marks.com and store 115, Sherbrooke, on L'Equipeur minutes apart). Report `units_at_store` with `assigned_store` every time, never as stock at a store you picked or "stock at every store". `units_online` are the online units.
- **French via L'Equipeur, on five endpoints.** `language: "fr"` on search, list, product, brands and categories reads L'Equipeur: the same product codes and CAD prices with French titles, colours and filter labels. `footnote` is `null` there: quote the definition from a marks.com answer. Questions, suggestions and store read marks.com in English (`language: "fr"` on questions is a `400`).
- **Each site has its own ratings.** `rating` and `review_count` are each site's own: 75983776F read 3.4 from 146 on marks.com and 4.04 from 45 on L'Equipeur. Name the site with every rating.
- **Filters come from facets.** Send `include_facets: true` once to get Mark's filters with counts, then pass them as `filters` `[{facet, value}]` (up to 6). `brand` takes the Brand Name value from facets (`Dakota Workpro Series`), not the spelling in `/brands`.
- **List paths come from categories.** `/list` takes a category path from `/categories` (`path`, e.g. `/en/cat/work-boots-shoes-DC3000008.html`) or a marks.com deals page path under `/en/sale-clearance/`; on L'Equipeur only category paths (`/fr/cat/...`, from `/categories` with `language: "fr"`). Category pages list 12 a page (`page_size` says). `deals` (`sale`, `clearance`, `both`) works on search and category pages; on a deals page it is a `400`.
- **What is not there.** No customer reviews on Mark's (only `rating` and `review_count`), no UPC or barcode (the site shows none), no stores near a postal code, no flyer, no Triangle Rewards or CT Money prices, no price history (store your own answers with `fetched_at`), no cart or checkout. Questions are the newest 10 per product.

Mark's publishes no public API for its catalog, prices or stock. This skill reads the public Mark's and L'Equipeur pages with one Scavio key. Other vendors offer Mark's data tools; this skill reads Mark's own public pages.

Canadian Tire Corporation's Q3 2026 results (quarter ended October 3, 2026; released November 12, 2026) report Mark's comparable sales up 3.3%, its eighth consecutive quarter of growth, "led by workwear, industrial footwear and men's jeans." Quote it with that source, never from the samples.

See also: `sportchek-api` (SportChek, the Canadian Tire Corporation sporting goods banner), `canadian-tire-api` (Canadian Tire, the same parent), `amazon-product-data` (Amazon.ca with `country: "ca"`) and `walmart-product-data` (Walmart.ca with `domain: "ca"`). Same brand, model, colour, size and width only: match on the full product name and the variant, show each price with its retailer, seller and date, and flag marketplace sellers on Amazon.ca and Walmart.ca rather than treating them as Amazon or Walmart.

## When to trigger

Use this skill when the user asks to:
- Read Mark's prices, was prices and sale end dates in CAD for a work boot, jacket, pant or any product, search or category
- Put a Mark's price next to the same model at Amazon.ca or Walmart.ca
- Read the same Mark's product in French on L'Equipeur (lequipeur.com)
- List a Mark's category or deals page sorted by price or rating
- Filter Mark's results by brand, gender, shoe size, width, CSA features, colour, rating, price band or sale and clearance
- Read one Mark's product with every colour, size and width, online units and the assigned store's units
- Read a Mark's product's customer questions and answers
- Read Mark's search suggestions, one store's hours and nearby stores, the brand list or the category tree

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, brands took about 1 second, categories 8, search 10 to 12, list 12, suggestions 14, product 17 to 21, questions 23 and store 26. Allow up to 2 minutes for an answer and a client timeout of at least 240 seconds.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/marks/search` | Products for keywords: price, was price, sale end date, promotion text, badges, review count, per-colour prices and online units; total, pages, sorts, filters, facets with counts on request, the was-price footnote; `language` en or fr | 1 |
| `POST /api/v1/marks/list` | One category or deals page by path or link, same items, sorts and filters as search (12 a page on category pages); `language` en or fr | 1 |
| `POST /api/v1/marks/product` | One product by code or link: price, was price, sale end date, promotion text, rating, description, features, specifications, images, breadcrumbs, options, style code, every variant with its own price and units, the assigned store; `language` en or fr | 1 |
| `POST /api/v1/marks/questions` | The newest 10 customer questions on one product with their answers (brand answers flagged), no names | 1 |
| `POST /api/v1/marks/suggestions` | Mark's search-box suggestions for typed text: terms, top hit, categories, brands | 1 |
| `POST /api/v1/marks/store` | One store by number: address, phone, coordinates, time zone, weekly and special hours, curbside pickup, up to 49 nearby stores with distance | 1 |
| `POST /api/v1/marks/brands` | Mark's brand pages: name, slug, url (113 in the capture); `language` en or fr | 1 |
| `POST /api/v1/marks/categories` | Mark's category tree with `path` for `/list` (269 categories under 11 top-level ones in the capture); `language` en or fr | 1 |

## Market

Canada only, CAD: every answer carries `market` {`banner` "Mark's", `site` ("Mark's" or "L'Equipeur"), `host` (`www.marks.com` or `www.lequipeur.com`), `language` ("en" or "fr"), `country` "ca", `currency` "CAD"}. There is no `country` input; `language` picks the site.

## Prices, sale dates, variants and stock

| Field | Meaning |
|---|---|
| `price` | The price Mark's shows a visitor without an account, CAD. `price_max` is set when the colours or sizes span a range |
| `was_price` | Mark's was price as given, only where Mark's shows one; `null` otherwise |
| `footnote` | Mark's own sentence on was prices: "Was price reflects the last national regular price this product was sold for." (`null` on L'Equipeur). Quote it with any was price |
| `on_sale`, `sale_ends` | Whether Mark's marks the item on sale, and the end date it posts ("November 25, 2026"), as given |
| `price_message[]` | {`label`, `details`}: Mark's promotion text as given, where it shows one |
| `badges` | SALE, CLEARANCE, TOPRATED, BESTSELLER, NEWARRIVAL as Mark's shows them |
| `colours[]` (search, list) | Each colour's own `price`, `was_price`, `on_sale`, `sale_ends` and `units_online_max` (the most online units of any one size in that colour) |
| `variants[]` (product) | Each colour, size and width: `sku` (Mark's 12-digit SKU), `colour`, `size`, `width`, own price, was price, sale end date, `units_at_store`, `units_online`, `ship_to_home`, `store_pickup`, `sellable` |
| `style_code` (product) | The vendor's style number as Mark's gives it (`5ANBDK9-6114`) |
| `assigned_store` (product) | {`id`, `name`, `city`, `province`}: the store Mark's assigns to the request's region. `units_at_store` are its units; it is not chosen by the caller |

- **Percent off:** compute it from `price` and `was_price` as shown, and label it computed. Where there is no `was_price`, quote `price_message` as given instead of computing a discount.
- **Same price in French:** the codes and prices match across the two sites (78160559F, Helly Hansen Workwear ICEFX winter boots, read 234.99 CAD with a was price of 309.99 on both on 2026-11-25). Titles, colours (`Brown` / `Brun`), widths (`Wide` / `Large`) and option labels are in each site's language.
- **Assigned store:** record `assigned_store` with every `units_at_store` number.

## Workflow

1. **Find the product.** `/search` with `q` and `include_facets: true` on the first call; narrow with `brand` or `filters` from `facets` (shoe size, width, CSA features). Note `total` and `total_pages`.
2. **Read the variant.** `/product` with `code` (`items[].code`, e.g. `75983776F`) for each colour, size and width, its price, was price, `sale_ends`, `units_online` and the assigned store's units.
3. **Match elsewhere.** `amazon-product-data` with `country: "ca"` and `walmart-product-data` with `domain: "ca"` for the same brand, model, colour, size and width. Keep a row only when the names and variants match; record each seller.
4. **Report.** Each price with its retailer, CAD, the capture date and "before tax and shipping"; Mark's was price with the footnote; a percent off labelled computed; the sale end date as Mark's posts it.
5. **French.** The same call with `language: "fr"` for L'Equipeur titles; prices and codes are the same.
6. **A category or deals page.** `/categories` once for `path`, then `/list` with `path` and `sort: "price_low"`.
7. **Questions.** `/questions` with `code` for the newest 10 and their answers.
8. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`) and list (`/list`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | required (search) | Keywords or a product code, up to 200 chars |
| `path` | string | one of (list) | A category path from `/categories` (`/en/cat/...-DC....html`; `/fr/cat/...` on L'Equipeur) or a marks.com deals page path under `/en/sale-clearance/` |
| `url` | string | one of (list) | The page link instead of `path` (not both) |
| `page` | integer | 1 | Page number; 24 a page on search, 12 on category pages (`page_size` says), `total_pages` says how many |
| `sort` | string | `relevance` | `relevance`, `price_high`, `price_low`, `rating` |
| `brand` | string or list | none | Brand Name value from facets (`Dakota Workpro Series`), up to 10 |
| `deals` | string or list | none | `sale`, `clearance` or `both`. Not on a deals page (`400`) |
| `filters` | list | none | Up to 6 `{facet, value}` from `facets[].values[]` (`{"facet": "sku_gender_attr", "value": "Female"}`); `value` one or a list |
| `include_facets` | boolean | false | Also return Mark's filters with counts (still 1 credit) |
| `language` | string | `en` | `en` (marks.com) or `fr` (L'Equipeur) |

### Product (`/product`) and questions (`/questions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `code` | string | one of | A Mark's product code (`items[].code`, digits and a letter: `75983776F`) |
| `url` | string | one of | A Mark's or L'Equipeur product link (`items[].url`), instead of `code` (not both); its site must match `language` |
| `language` | string | `en` | Product only: `en` or `fr`. Questions are `en` only |

### Suggestions, store, brands, categories

`/suggestions` takes `q` (the text typed so far, up to 100 chars). `/store` takes `store_id` (a store number: `assigned_store.id` or `nearby_stores[].id`, e.g. `589`). `/brands` takes an optional `letter` (one letter or digit) and `language`. `/categories` takes `language` (send `{}` for English).

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/marks/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "work boots", "include_facets": true}'
```

Captured `data` (2026-11-25; `items` cut to 1 of 24, `image`, `corrected_query`, `redirected_to`, `facets` and `notes` dropped):

```json
{
  "query": "work boots",
  "market": {"banner": "Mark's", "site": "Mark's", "host": "www.marks.com", "language": "en", "country": "ca", "currency": "CAD"},
  "total": 1001,
  "total_pages": 42,
  "page": 1,
  "page_size": 24,
  "has_more": true,
  "count": 24,
  "sort": "relevance",
  "filters_applied": [],
  "items": [
    {"position": 2, "code": "75983776F", "name": "Dakota WorkPro Series Men's Steel Toe Composite Plate 6114 Quad Comfort Freshtech 6 Inch Work Boots", "brand": "Dakota Workpro Series", "url": "https://www.marks.com/en/pdp/dakota-workpro-series-men-s-steel-toe-composite-plate-6114-quad-comfort-freshtech-6-inch-work-boots-75983776f.html", "price": 124.99, "price_max": null, "was_price": 199.99, "currency": "CAD", "on_sale": true, "sale_ends": "November 25, 2026", "price_message": [], "badges": ["SALE"], "rating": null, "review_count": 146, "colours": [{"name": "Brown", "price": 124.99, "was_price": 199.99, "on_sale": true, "sale_ends": "November 25, 2026", "units_online_max": 188}], "sponsored": false}
  ],
  "footnote": "Was price reflects the last national regular price this product was sold for."
}
```

The 27 facets included Gender, Brand Name, Deals, Shoe Size (US), Shoe Width, CSA Features, Certifications, Boot Type and Price. Computed from the shown numbers: 124.99 against 199.99 is 37.5% off (computed).

### One product with variants and the assigned store

```bash
curl -X POST https://api.scavio.dev/api/v1/marks/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "75983776F"}'
```

Captured `data` (2026-11-25; `variants` cut to 2 of 15, variant `options`, `description`, `features`, `specifications`, `images`, `breadcrumbs`, `options`, `style_codes` and `notes` dropped):

```json
{
  "market": {"banner": "Mark's", "site": "Mark's", "host": "www.marks.com", "language": "en", "country": "ca", "currency": "CAD"},
  "requested_code": "75983776F",
  "code": "75983776F",
  "name": "Dakota WorkPro Series Men's Steel Toe Composite Plate 6114 Quad Comfort Freshtech 6 Inch Work Boots",
  "brand": "Dakota Workpro Series",
  "url": "https://www.marks.com/en/pdp/dakota-workpro-series-men-s-steel-toe-composite-plate-6114-quad-comfort-freshtech-6-inch-work-boots-75983776f.html",
  "price": 124.99,
  "price_max": null,
  "was_price": 199.99,
  "currency": "CAD",
  "on_sale": true,
  "sale_ends": "November 25, 2026",
  "price_message": [],
  "badges": ["SALE"],
  "rating": 3.4,
  "review_count": 146,
  "style_code": "5ANBDK9-6114",
  "status": "ACTIVE",
  "variant_count": 15,
  "variants": [
    {"sku": "410025619987", "colour": "Brown", "size": "13", "width": "Wide", "style_code": "5ANBDK9-6114", "price": 124.99, "was_price": 199.99, "on_sale": true, "sale_ends": "November 25, 2026", "price_message": [], "badges": ["SALE"], "units_at_store": 2, "units_online": 114, "ship_to_home": true, "store_pickup": true, "sellable": true, "max_per_order": null},
    {"sku": "410025619970", "colour": "Brown", "size": "12", "width": "Wide", "style_code": "5ANBDK9-6114", "price": 124.99, "was_price": 199.99, "on_sale": true, "sale_ends": "November 25, 2026", "price_message": [], "badges": ["SALE"], "units_at_store": 0, "units_online": 80, "ship_to_home": true, "store_pickup": true, "sellable": true, "max_per_order": null}
  ],
  "assigned_store": {"id": "114", "name": "Marche Central", "city": "Montreal", "province": "QC"},
  "footnote": "Was price reflects the last national regular price this product was sold for."
}
```

Across the 15 sizes (all Brown, Wide) the assigned store (114, Montreal, QC) held 12 units in 9 variants and `units_online` summed to 1,232. The notes say "The site shows no UPC or barcode."

### The same product in French (L'Equipeur)

```bash
curl -X POST https://api.scavio.dev/api/v1/marks/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "75983776F", "language": "fr"}'
```

Captured `data` (2026-11-25; `variants` cut to 1 of 15, other fields dropped as above):

```json
{
  "market": {"banner": "Mark's", "site": "L'Equipeur", "host": "www.lequipeur.com", "language": "fr", "country": "ca", "currency": "CAD"},
  "code": "75983776F",
  "name": "Bottes de travail de 6 pouces Quad Comfort Freshtech Dakota Workpro Series à protection en acier et en composite, pour hommes, 6114",
  "brand": "Dakota Workpro Series",
  "url": "https://www.lequipeur.com/fr/pdp/bottes-de-travail-de-6-pouces-quad-comfort-freshtech-dakota-workpro-series-a-protection-en-acier-et-en-composite-pour-hommes-6114-75983776f.html",
  "price": 124.99,
  "was_price": 199.99,
  "currency": "CAD",
  "on_sale": true,
  "sale_ends": "November 25, 2026",
  "rating": 4.04,
  "review_count": 45,
  "style_code": "5ANBDK9-6114",
  "variant_count": 15,
  "variants": [
    {"sku": "410025620013", "colour": "Brun", "size": "16", "width": "Large", "style_code": "5ANBDK9-6114", "price": 124.99, "was_price": 199.99, "on_sale": true, "sale_ends": "November 25, 2026", "price_message": [], "badges": ["SALE"], "units_at_store": 1, "units_online": 46, "ship_to_home": true, "store_pickup": true, "sellable": true, "max_per_order": null}
  ],
  "assigned_store": {"id": "115", "name": "Sherbrooke", "city": "Sherbrooke", "province": "QC"},
  "footnote": null
}
```

Same code, price, was price and sale end date; French title and variant labels; another assigned store (115, Sherbrooke, QC: 21 units in 14 variants); L'Equipeur's own rating (4.04 from 45, against 3.4 from 146 on marks.com); `footnote` `null`. `/search` `{"q": "bottes de travail", "language": "fr"}` listed 707 products over 30 pages on L'Equipeur.

### Questions

```bash
curl -X POST https://api.scavio.dev/api/v1/marks/questions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "75984589F"}'
```

Captured (2026-11-25): Aggressor Men's Lynx II Steel Toe Steel Plate 6 Inch Leather Work Boots, `total` 4, `count` 4 (the newest 10 at most), dated 2023-06-17 to 2023-12-03, 3 with one answer each. One question as returned, with `question` and answer `text` dropped:

```json
{"id": "6588321", "details": null, "date": "2023-12-02T11:57:35.000+00:00", "answer_count": 1, "locale": "en_CA", "answers": [{"date": "2024-02-20T17:00:35.000+00:00", "brand_answer": false, "best_answer": false, "helpful_yes": 1, "helpful_no": 0, "locale": "en_CA"}]}
```

`brand_answer` marks an answer the site flags as the brand's. Questions and answers can mix English and French as the page pools them. No asker or answerer names are returned.

### List, store, suggestions, brands, categories

- `/list` `{"path": "/en/cat/work-boots-shoes-DC3000008.html"}`: `total` 532, `total_pages` 45, `page_size` 12; first the Helly Hansen Workwear Men's 6 Inch Composite Toe Composite Plate Waterproof Work Boots at 169.99 CAD, was price 269.99, `sale_ends` "November 25, 2026".
- `/store` `{"store_id": "589"}`: Leamington, ON, `timezone` America/Nipigon, weekly `hours`, `curbside_pickup` false and 47 `nearby_stores` (nearest Essex at 23.19 km). Finding stores near a postal code is not supported.
- `/suggestions` `{"q": "dakota"}`: 20 `terms` ("dakota work boots", "dakota work pants", "dakota workpro series" ...), `top_hit` "dakota".
- `/brands` `{}`: 113 brands with `name`, `slug`, `url` (name spelled from the brand page link; filter search with the Brand Name value from facets).
- `/categories` `{}`: `total_categories` 269 under 11 top-level categories (Accessories, Footwear, Kids, Mens, Womens, Work Boots Shoes, Workwear and four scrubs and rain-boot pages), each with `path` for `/list`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def marks(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/marks/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# Was prices and sale end dates on page 1 (1 credit)
d = marks("search", {"q": "work boots", "deals": "sale", "sort": "price_low"})["data"]
print(d["total"], d["footnote"])
for i in d["items"]:
    off = None
    if i["was_price"]:
        off = round(100 * (i["was_price"] - i["price"]) / i["was_price"], 1)  # computed
    print(i["code"], i["name"], i["price"], i["was_price"], off, i["sale_ends"])

# One product: every size with the assigned store's units (1 credit)
p = marks("product", {"code": "75983776F"})["data"]
store = p["assigned_store"]
for v in p["variants"]:
    print(v["size"], v["width"], v["price"], v["units_online"], v["units_at_store"], store["id"], store["city"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` and `notes`.

- **item** (search, list) - `position`, `code`, `name`, `brand`, `url`, `image`, `price`, `price_max`, `was_price`, `currency`, `on_sale`, `sale_ends`, `price_message[]` {`label`, `details`}, `badges`, `rating`, `review_count`, `colours[]` {`name`, `price`, `was_price`, `on_sale`, `sale_ends`, `units_online_max`}, `sponsored`.
- **search** - `query`, `corrected_query`, `redirected_to`, `total`, `total_pages`, `page`, `page_size`, `has_more`, `count`, `sort`, `filters_applied`, `items[]`, `facets[]` (with `include_facets`: {`id`, `label`, `type`, `values[]` {`label`, `count`, `facet`, `value`, `selected`}}), `footnote`.
- **list** - `path`, `url`, then as search from `total`.
- **product** - `requested_code`, `code`, `name`, `brand`, `url`, `price`, `price_max`, `was_price`, `currency`, `on_sale`, `sale_ends`, `price_message`, `badges`, `rating`, `review_count`, `description`, `features`, `specifications[]` {`label`, `value`}, `images`, `breadcrumbs[]` {`name`, `id`, `url`}, `options[]` {`type`, `label`, `values`}, `style_code`, `style_codes`, `status`, `variant_count`, `variants[]` {`sku`, `colour`, `size`, `width`, `options`, `style_code`, `price`, `was_price`, `on_sale`, `sale_ends`, `price_message`, `badges`, `units_at_store`, `units_online`, `ship_to_home`, `store_pickup`, `sellable`, `max_per_order`}, `assigned_store` {`id`, `name`, `city`, `province`}, `footnote`.
- **questions** - `code`, `name`, `url`, `total`, `count`, `questions[]` {`id`, `question`, `details`, `date`, `answer_count`, `locale`, `answers[]` {`text`, `date`, `brand_answer`, `best_answer`, `helpful_yes`, `helpful_no`, `locale`}}.
- **suggestions** - `query`, `count`, `terms`, `top_hit`, `categories`, `brands`.
- **store** - `id`, `name`, `url`, `address` {`line1`, `line2`, `city`, `province`, `province_code`, `postal_code`, `country`}, `phone`, `latitude`, `longitude`, `timezone`, `hours[]` {`day`, `open`, `close`, `closed`}, `special_hours`, `curbside_pickup`, `services`, `nearby_stores[]` {`id`, `name`, `city`, `province_code`, `distance_km`}, `nearby_count`.
- **brands** - `letter`, `total_brands`, `count`, `brands[]` {`name`, `slug`, `url`}.
- **categories** - `total_categories`, `count` (top-level), `categories[]` {`id`, `name`, `path`, `url`, `level`, `children[]`}.

## Guardrails

- Name it "Mark's (marks.com, the Canadian workwear, casual clothing and footwear retailer, a Canadian Tire Corporation banner; L'Equipeur in French)" on first mention, "Mark's" after that, and "L'Equipeur" for French answers.
- Prices: quote each with CAD, the site, the `fetched_at` date and "before tax and shipping" ("listed on marks.com on Nov 25, 2026, before tax and shipping"). Online prices and sale dates can differ in store and by region.
- Was prices: quote Mark's footnote next to any was price. A percent off is computed from the two shown numbers and labelled computed. Never "real" or "fake" discount, never "MSRP", no verdicts on a sale.
- Comparisons: same brand, model, colour, size and width only, each price with its retailer, seller and date. No price-match advice and no Triangle Rewards or CT Money values.
- Stock: `units_at_store` only with the `assigned_store` it belongs to. Never promise stock for a store the user chooses, or at every store.
- Questions: no asker or answerer names (none are returned). Report questions as the page lists them; do not turn answers into claims about a product.
- Descriptive only: no commentary on Mark's business, pricing practices or policies. Quote Canadian Tire Corporation figures only with their release and quarter.
- Do not republish Mark's product photos, descriptions or logos. Write marks.com and lequipeur.com as plain text and cite product names, codes and capture dates rather than linking Mark's or L'Equipeur pages.
- Terms: Scavio does not collect or store Mark's data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account, no Triangle login, no cart and no checkout. Mark's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, was prices, sale dates, codes, stores, units or questions. Only return what the API returned, with the `fetched_at` time.
- Not available: customer reviews (rating and review count only), choosing a store for price or stock, stores near a postal code, the flyer, Triangle Rewards or CT Money prices, price history (store your own), UPC or barcodes, cart or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `q`; list without `path` or `url`, or both; a path that is not a Mark's (or, with `language: "fr"`, L'Equipeur) category or deals page ("Paths come from categories."); `deals` on a deals page ("deals is not used on a deals page (the page already is one): use it with search or a category page."); `deals` other than `sale`, `clearance` or `both`; more than 6 `filters`, or a `facet` not taken from `facets[].values[].facet`; product or questions without `url` or `code`, or both; a code that is not digits and a letter; a link whose site does not match `language` ("language does not match the link's site (www.lequipeur.com is fr)."); `language` other than `en` or `fr`, or `fr` on questions ("language must be en for questions."); a `store_id` that is not digits.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Mark's has no product with the code <code>.", "Mark's has no page at <path>. Category paths come from categories.", "Mark's has no store number <id>.". Take codes, paths and store numbers from a previous answer rather than guessing them. A search with no matches is a `200` with `count` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api).
- `502` means Mark's data was temporarily unavailable ("Mark's is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
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
const { data: boots } = await scavio.marks.search({ q: "work boots", include_facets: true });
const { data: bottes } = await scavio.marks.search({ q: "bottes de travail", language: "fr" });
const { data: category } = await scavio.marks.list({ path: "/en/cat/work-boots-shoes-DC3000008.html", sort: "price_low" });
const { data: product } = await scavio.marks.product({ code: "75983776F" });
const { data: questions } = await scavio.marks.questions({ code: "75984589F" });
const { data: store } = await scavio.marks.store({ store_id: "589" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.marks.search(...)`, `list`, `product`, `questions`, `suggestions`, `store`, `brands` and `categories`, with the same parameter names as keyword arguments. Give the client a timeout of at least 240 seconds for these calls.

## MCP

The Scavio MCP server exposes all 8 endpoints as tools: `search_marks`, `get_marks_list`, `get_marks_product`, `get_marks_questions`, `get_marks_suggestions`, `get_marks_store`, `get_marks_brands` and `get_marks_categories`. Mark's is opt-in: add `marks` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.90.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,marks"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/marks-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api), [list](https://scavio.dev/docs/marks-list?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api), [product](https://scavio.dev/docs/marks-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api), [questions](https://scavio.dev/docs/marks-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api), [suggestions](https://scavio.dev/docs/marks-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api), [store](https://scavio.dev/docs/marks-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api), [brands](https://scavio.dev/docs/marks-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api), [categories](https://scavio.dev/docs/marks-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api). Overview: [Mark's API](https://scavio.dev/marks-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=marks-api).
