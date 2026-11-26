---
name: douglas-beauty-api
description: Douglas API for Douglas (douglas.de, the Dusseldorf-based beauty retailer with about 1,960 stores in Europe) on 15 storefronts in 13 countries - de, at, ch-de, ch-fr, nl, be-nl, be-fr, es, it, pl, cz, sk, hu, ro and lt, each in its own language and currency (EUR, CHF, PLN, CZK, HUF, RON) - perfume, make-up, skincare and hair prices with the four numbers Douglas shows side by side, the price, the struck-through was price, the lowest price of the last 30 days Douglas shows beside a reduction and the RRP (UVP), plus discount_percent as Douglas shows it (YSL Libre Eau de Parfum 30 ml on douglas.de read 52.99 EUR, was 59.99, 30-day low 52.99, RRP 87 on Nov 26, 2026); the same product code priced per storefront (Miss Dior Eau de Parfum 30 ml read 68.62 EUR in the Netherlands and 64.05 EUR in Belgium); keyword search, any category or brand, 48 per page with total and pages, sorted by relevance, price, newest, top rated or discount and filtered by brand, Douglas' sale badge or any of its facets (product type, gender, skin type, finish), with keywords Douglas sends to a brand or category page answered from that page (redirected_to); the sale department, the Beauty / Black Friday list and any category's sale-badged products, with the storefront's offers page (validity dates and codes as Douglas words them); one product with EAN, ingredients, scent notes, rating and review count, every size or shade with its own four prices and stock status, and each variant's EAN on request; Douglas' own AI-generated summary of a product's reviews; stores near a city or postcode with weekly and dated holiday hours, one store with its top brands; search suggestions and the brand index (about 1,890 brands on douglas.de). 10 endpoints, 1 credit per call (Italy 2; each variant EAN 1 more, 2 on Italy). Listing pages are slow, 5 to 210 seconds. Not available - review texts or review paging, per-store stock, store reservation, price history, cart or checkout, and the Portugal, Croatia, Slovenia, Latvia, Estonia, Bulgaria and France (Nocibe) shops.
version: 1.0.0
tags: douglas, douglas-de, douglas-api, douglas-beauty, douglas-parfumerie, douglas-perfume-prices, douglas-prices, douglas-product-data, douglas-sale, douglas-black-friday, douglas-beauty-friday, douglas-deals, douglas-stores, douglas-brands, douglas-austria, douglas-switzerland, douglas-netherlands, douglas-belgium, douglas-spain, douglas-italy, douglas-poland, douglas-czech, douglas-hungary, douglas-romania, douglas-slovakia, douglas-lithuania, perfume, perfume-prices, fragrance, make-up, skincare, beauty, beauty-prices, european-beauty, eu-prices, rrp, uvp, omnibus, 30-day-lowest-price, was-price, ean, scent-notes, price-comparison, price-monitoring, eur, chf, pln, czk, huf, ron, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 250
    throttle: 1
    homepage: https://scavio.dev/douglas-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api
---

# Douglas API - Perfume and Beauty Prices, RRP, 30-Day Low, 15 Storefronts

Read Douglas (douglas.de, the Dusseldorf-based beauty retailer with about 1,960 stores in Europe) on 15 storefronts in 13 countries: keyword search, any category or brand, the sale and Beauty / Black Friday lists with the storefront's offers page, one product in full with every size or shade, Douglas' own summary of a product's reviews, the stores near a place, one store, search suggestions and the brand index. Every answer is what the storefront's public pages show a visitor without an account at the moment of the call, in the storefront's language and currency. All 10 endpoints return structured JSON at 1 credit per call (2 on Italy).

**Read-only data.** This skill reads the public pages Douglas shows to any visitor and returns them as JSON for analysis. It uses no Douglas account, no Beauty Card login, no cart, no checkout and no store reservation.

**The job this skill is for: Douglas beauty prices with the four numbers Douglas shows, per storefront.** A product's price, the struck-through was price, the lowest price of the last 30 days Douglas shows beside a reduction, and the RRP (UVP), per size or shade, and the same product code on another Douglas storefront in its own currency. Captured 2026-11-26 with `/product` (1 credit each). YSL Libre Eau de Parfum on douglas.de (base code `5000005003`, `variants_ean` true, 5 credits):

| Variant (code) | price EUR | was_price | discount_percent | lowest_price_30d | rrp | EAN |
|---|---|---|---|---|---|---|
| 30 ml (289686) | 52.99 | 59.99 | 11.67 | 52.99 | 87 | 3614272648401 |
| 50 ml (289690) | 76.95 | 79.99 | 3.8 | 73.52 | 125 | 3614272648418 |
| 90 ml (289703) | 94.95 | 119 | 20.21 | 91.16 | 170 | 3614272648425 |
| 100 ml refill (1129247) | 99 | 125 | 20.8 | 94 | 145 | 3614273941136 |
| 150 ml (724965) | 143.99 | 222 | 35.14 | 152.29 | null | 3614273011785 |

The same product code on other storefronts, the same day:

| Product (base code) | Storefront | price | was_price | discount_percent | lowest_price_30d |
|---|---|---|---|---|---|
| DIOR Miss Dior Eau de parfum 30 ml (5012103059) | nl | 68.62 EUR | 91.5 | 25.01 | null |
| | be-nl, be-fr | 64.05 EUR | 91.5 | 30 | null |
| DIOR Forever foundation 0 Cool Rosy (5012008023) | lt | 54.39 EUR | 67.99 | 20 | 67.99 |
| | sk | 68.95 EUR | null | null | null |
| | hu | 28590 HUF | null | null | null |
| DIOR Rouge Dior lipstick 100 Sweet Nude (5012111049) | it (2 credits) | 38.49 EUR | 54.99 | 30.01 | 43.99 |
| | ro | 301 RON | null | null | null |

Prices are set per storefront, even inside the euro zone: the Netherlands and Belgium read different prices against the same was price. Put each price with its storefront, currency, size and date; never convert currencies without saying so.

Ten limits shape every answer, so say them plainly:
- **1 credit per call, 2 on Italy.** Every endpoint costs 1 credit; with `market` `it` (or a douglas.it link) it costs 2, except `/stores` and `/store`, which stay 1. `variants_ean` adds 1 credit per variant looked up (2 on Italy), up to 10: the YSL call above cost 5 (1 + 4 EANs). `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Four prices, as Douglas shows them.** `price`, `was_price` (the struck-through price), `lowest_price_30d` (the lowest price of the last 30 days Douglas shows beside a reduction) and `rrp` (the RRP / UVP) are Douglas' figures; any of them is `null` where the page shows none. `discount_percent` is Douglas' own figure too. Never compute a 30-day low yourself, and never fill a missing RRP.
- **The 30-day low is not the floor.** `lowest_price_30d` can sit above today's price (YSL Libre 150 ml: 143.99 against 152.29) and on some storefronts it equals the was price (lt: 67.99 and 67.99). Quote it as Douglas labels it, next to the price.
- **Prices are per storefront.** `market` picks the storefront (default `de`). Product codes are shared across storefronts, but prices, assortment and texts differ; a product a storefront does not sell is a charged `404`. Names and descriptions come in the storefront's language (German on de, at and ch-de, French on ch-fr and be-fr, Polish on pl ...).
- **Listings are slow.** search, category, brand and deals read Douglas' listing pages: 5 to 210 seconds per answer (the captures took 3 to 28 seconds); the brand index takes up to about 200 seconds. JSON endpoints (product, stores, store, review summary, suggestions) answer in 1 to 23 seconds. Set a client timeout of 250 seconds and send one request at a time.
- **Keywords can land on a page.** Douglas sends some keywords to a brand or category page; `/search` then answers from that page and `redirected_to` says which (`dior` on de went to the DIOR brand page, 260 products; `mascara` on nl to the mascara category, 432 products). Check `redirected_to` before calling an answer "search results".
- **total is the page's figure.** `total` is the count the listing page shows (the very largest lists, the de sale department and the de make-up category, read 10000). `page` runs to 200 at 48 a page. Sponsored placements are left out of `items`.
- **Sale badge or reduced price.** `sale_only` keeps products with Douglas' own sale badge (SALE on de, the discount badge elsewhere); not every reduced price carries it, so read `was_price` for every reduction. Douglas Switzerland shows no such badge: `sale_only` on `ch-de` or `ch-fr` is a `400`, not charged.
- **A review summary, not reviews.** `/review-summary` returns Douglas' own AI-generated summary of a product's customer reviews, in the storefront's language, or `null` where Douglas shows none. `/product` carries `rating` and `review_count`. Review texts, review paging and star filters are not offered.
- **What is not there.** No per-store stock (stores carry hours and services, not units), no store reservation, no price history (store your own answers with `fetched_at`), no cart or checkout. Douglas Portugal, Croatia, Slovenia, Latvia, Estonia and Bulgaria run on another shop platform and France trades as Nocibe: those are a `400`, not charged.

Douglas publishes no public API for its catalogue, prices or stores; it runs an affiliate programme on Awin for approved publishers. This skill reads the public storefront pages with one Scavio key and needs no affiliate approval. Other vendors offer Douglas data tools; this skill reads Douglas' own public pages.

See also: `notino-api` (Notino, the European online perfumery, 27 storefronts with its own 30-day low), `lookfantastic-api` (Lookfantastic country sites), `cult-beauty-api` (Cult Beauty) and `amazon-product-data` (Amazon.de and other European marketplaces). Same product and size only: match on EAN where both sides return one, otherwise brand + line + product type + size in both titles, each price with its retailer, storefront, currency and date.

## When to trigger

Use this skill when the user asks to:
- Read a Douglas product's price, was price, 30-day lowest price and RRP, per size or shade
- Compare one Douglas product across storefronts (Germany, Austria, Switzerland, Netherlands, Belgium, Spain, Italy, Poland, Czechia, Slovakia, Hungary, Romania, Lithuania)
- Search Douglas or list a category or brand, sorted by price, newest, top rated or discount and filtered by brand, sale badge or any facet
- List the Douglas sale department or the Beauty / Black Friday deals, with the offers page's validity dates and codes
- Read one Douglas product with EAN, ingredients, scent notes, rating and review count
- Read Douglas' own summary of a product's reviews
- Find Douglas stores near a city or postcode, or read one store's hours, holiday hours and top brands
- List Douglas brands or read search suggestions

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Calls in this skill cost 1 credit (2 on Italy), so 50 credits cover 50 product or listing calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Listing pages take 5 to 210 seconds, the brand index up to about 200; product 1-23 seconds, stores and store 1-5, review summary and suggestions 1-4. Set a client timeout of 250 seconds and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/douglas/search` | Products for keywords: four prices, unit price, content, availability, rating, flags; total, pages, sorts, facets; `redirected_to` when Douglas sends the keyword to a page | 1 (it 2) |
| `POST /api/v1/douglas/category` | One category by path, code or link, with paging, sorts and filters | 1 (it 2) |
| `POST /api/v1/douglas/brand` | One brand's products by brand code, path or link | 1 (it 2) |
| `POST /api/v1/douglas/deals` | The sale department, the Beauty / Black Friday list or a category's sale-badged products, plus the offers page's promotions | 1 (it 2) |
| `POST /api/v1/douglas/product` | One product: EAN, description, ingredients, scent notes, four prices, stock status, rating, review count, every variant with its own prices; variant EANs on request | 1 (it 2); +1 per variant EAN (it 2) |
| `POST /api/v1/douglas/stores` | Stores near a city or postcode: address, phone, distance, weekly and dated holiday hours | 1 |
| `POST /api/v1/douglas/store` | One store: the stores fields plus parking, public transport, top brands, events | 1 |
| `POST /api/v1/douglas/review-summary` | Douglas' own AI-generated summary of a product's reviews | 1 (it 2) |
| `POST /api/v1/douglas/suggestions` | Product suggestions for typed text, and the storefront's trending searches | 1 (it 2) |
| `POST /api/v1/douglas/brands` | Every brand on the storefront with its code for `/brand` | 1 (it 2) |

## Markets

| `market` | Storefront | Language | Currency |
|---|---|---|---|
| `de` (default) | douglas.de | German | EUR |
| `at` | douglas.at | German | EUR |
| `ch-de`, `ch-fr` | douglas.ch | German, French | CHF |
| `nl` | douglas.nl | Dutch | EUR |
| `be-nl`, `be-fr` | douglas.be | Dutch, French | EUR |
| `es` | douglas.es | Spanish | EUR |
| `it` | douglas.it | Italian | EUR (2 credits; stores and store 1) |
| `pl` | douglas.pl | Polish | PLN |
| `cz` | douglas.cz | Czech | CZK |
| `sk` | douglas.sk | Slovak | EUR |
| `hu` | douglas.hu | Hungarian | HUF |
| `ro` | douglas.ro | Romanian | RON |
| `lt` | douglas.lt | Lithuanian | EUR |

Every answer carries `market`, `country`, `language` and `currency`. A product link sets the market from its storefront; a `market` that does not match the link is a `400`. `pt`, `hr`, `si`, `lv`, `ee`, `bg` (another shop platform) and `fr` (Douglas trades in France as Nocibe) are a `400`, not charged. The offers page (`promotions` on `/deals`) is linked on de, at, ch-de, ch-fr and pl; elsewhere it is `null`.

## Prices, variants and flags

| Field | Meaning |
|---|---|
| `price` | Douglas' price on the storefront, in its currency; `price_text` as shown ("52,99 €") |
| `was_price` | Douglas' struck-through price, `null` without one |
| `discount_percent` | The discount Douglas shows (Douglas' figure, not recomputed) |
| `lowest_price_30d` | The lowest price of the last 30 days Douglas shows beside a reduction, `null` where it shows none |
| `rrp` | The RRP / UVP Douglas shows, `null` where it shows none |
| `unit_price` | {`price`, `per`} as Douglas gives it ("1766.33 per 1 l") |
| `content` | {`amount`, `unit`} (30, "ml") |
| `availability` | `AVAILABLE`, `SOLD_OUT` or `AVAILABLE_IN_FUTURE`; `in_stock` true or false (online stock status, not store stock) |
| `flags` | Douglas' badges on the item (SALE, NEU, `webPrice`, `refillable`, `discountFlag`, `blackFriday` ...) |
| `marketplace` | {`is_marketplace`, `vendor`}: a partner seller's product, not Douglas' own stock |
| `code`, `base_code` | `code` is the variant (a size or shade), `base_code` the product; either is the input of `/product`, `base_code` the input of `/review-summary` |
| `ean` (product) | The EAN of `code` only; variants carry an EAN only with `variants_ean` true |

- **List items** carry `brand` as a name; `/product` carries `brand` {`code`, `name`, `url`} and `brand_line` {`code`, `name`, `url`} (Libre, Miss Dior, Rouge Dior).
- **Variants:** `variant_type` (`SIZE`, `COLOR` or `STYLE`) and `variant_count`; each `variants[]` row has its own four prices, `unit_price`, `content`, `stock_level`, `availability` and `flags`. Compare the variant, never the product's range.

## Workflow

1. **Find the products.** `/search` with `query` and `market`, `/brand` with a brand code from `/brands`, or `/category` with a path from a `categories[]` or `breadcrumbs` entry. Check `redirected_to`. Note each `base_code` and `code`.
2. **Read the product.** `/product` with `code` and `market`: the four prices per variant, `ean`, `availability`, `rating` and `review_count`. Add `variants_ean: true` only when you need every variant's EAN (1 more credit each).
3. **Other storefronts.** `/product` with the same `code` and another `market`, one call per storefront. A `404` means that storefront does not sell it.
4. **Deals.** `/deals` with `collection` `sale` or `beauty_friday` (or a `category`), and read `promotions[].legal_text` for the validity dates and codes as Douglas words them.
5. **Reviews.** `/product` for `rating` and `review_count`; `/review-summary` with `base_code` for Douglas' own summary text.
6. **Report.** Each price with its storefront, currency, size or shade and the `fetched_at` date; was price, 30-day low and RRP labelled as Douglas shows them.
7. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`), category (`/category`), brand (`/brand`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required (search) | Keywords in the storefront's language, up to 200 chars |
| `category` | string | required (category) | A category path ending in its code (`parfum/01`, `make-up/lippen/lippenstift/030503`), the code alone (`01`) or a category link |
| `brand` | string | required (brand) | A brand code (`b0690`, from `/brands`), its path (`dior/b0690`) or a brand link |
| `page` | integer | 1 | Page, 1-200, 48 products a page |
| `sort` | string | `relevance` | `relevance`, `price_asc`, `price_desc`, `newest`, `top_rated`, `discount` (where the storefront offers it); `sorts` lists what the page offers, `sort_applied` what it answered |
| `brand_filter` | string or list | none | Brand codes (`b0690` DIOR, `b0611` Yves Saint Laurent) |
| `sale_only` | boolean | false | Only products with Douglas' sale badge; a `400` on `ch-de` and `ch-fr` |
| `filters` | list | none | `{facet, value}` from `facets[].facet` and `facets[].values[].value` (`{"facet": "classificationClassName", "value": "Eau de Parfum"}`), at most 10 values in all |
| `market` | string | `de` | A storefront from the Markets table |

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `collection` | string | `sale` | `sale` (the sale department) or `beauty_friday` (the Beauty / Black Friday list, while Douglas runs it) |
| `category` | string | none | Or any category (path, code or link): its sale-badged products (not on ch-de / ch-fr). Not with `collection` |
| `include_promotions` | boolean | true | Also read the storefront's offers page (de, at, ch-de, ch-fr, pl) |
| `page`, `sort`, `brand_filter`, `filters`, `market` | | | As search |

### Product, stores, store, review summary, suggestions, brands

| Endpoint | Parameters |
|---|---|
| `/product` | `code` (a base or variant code, digits) or `url` (a Douglas product link; its storefront sets the market), `variants_ean` (boolean, up to 10 variants), `market` |
| `/stores` | `query` (required: a city or postcode, placed by Douglas' own store finder), `page` (1-100), `page_size` (1-50, default 10), `market` |
| `/store` | `store_id` (required, `stores[].store_id`, a string: leading zeros count, `"00020475"`), `market` |
| `/review-summary` | `code` (required: a base product code), `market` |
| `/suggestions` | `query` (required), `max` (1-10, default 10), `market` |
| `/brands` | `query` (brand name contains, accents and case ignored), `letter` (A-Z or #), `market` |

## Examples

### One product with every variant's EAN

```bash
curl -X POST https://api.scavio.dev/api/v1/douglas/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "5000005003", "variants_ean": true}'
```

Captured `data` (2026-11-26; `variants` cut to 2 of 5, `description`, `images`, `videos`, `categories`, `attributes` and `ingredients` dropped):

```json
{
  "requested": "5000005003",
  "source": "api",
  "market": "de",
  "country": "DE",
  "language": "de-DE",
  "currency": "EUR",
  "code": "289686",
  "base_code": "5000005003",
  "name": "30 ml",
  "brand": {"code": "b0611", "name": "Yves Saint Laurent", "url": "https://www.douglas.de/de/b/yves-saint-laurent/b0611"},
  "brand_line": {"code": "b061154", "name": "Libre", "url": "https://www.douglas.de/de/b/yves-saint-laurent/libre/b061154"},
  "product_family": "Eau de Parfum",
  "gender": "FEMALE",
  "url": "https://www.douglas.de/de/p/5000005003",
  "ean": "3614272648401",
  "price": 52.99,
  "price_text": "52,99 €",
  "was_price": 59.99,
  "discount_percent": 11.67,
  "lowest_price_30d": 52.99,
  "rrp": 87,
  "price_type": "BUY",
  "unit_price": {"price": 1766.33, "per": "1 l"},
  "content": {"amount": 30, "unit": "ml"},
  "stock_level": "inStock",
  "availability": "AVAILABLE",
  "availability_text": "Online auf Lager",
  "in_stock": true,
  "max_order_quantity": 5,
  "rating": 4.8,
  "rating_stars": 5,
  "review_count": 5779,
  "scent_notes": {"top": ["Vanille", "Zeder", "Ambra", "Moschus", "Mandarine", "Neroli", "Lavendel"], "heart": ["Orangenblüte", "Lavendel", "Jasmin"], "base": ["Neroli", "Mandarine", "Tangerine", "Zedernholz", "Moschus"]},
  "flags": [{"code": "webPrice", "name": "Online"}, {"code": "refillable", "name": "Nachfüllbar"}],
  "marketplace": {"is_marketplace": false, "vendor": null},
  "variant_type": "SIZE",
  "variant_count": 5,
  "variants": [
    {"code": "289686", "name": "30 ml", "price": 52.99, "currency": "EUR", "was_price": 59.99, "discount_percent": 11.67, "lowest_price_30d": 52.99, "rrp": 87, "content": {"amount": 30, "unit": "ml"}, "availability": "AVAILABLE", "in_stock": true, "flags": ["webPrice", "refillable"], "ean": "3614272648401"},
    {"code": "724965", "name": "150 ml", "price": 143.99, "currency": "EUR", "was_price": 222, "discount_percent": 35.14, "lowest_price_30d": 152.29, "rrp": null, "content": {"amount": 150, "unit": "ml"}, "availability": "AVAILABLE", "in_stock": true, "ean": "3614273011785"}
  ],
  "variants_ean": {"requested": true, "fetched": 4, "capped": false}
}
```

This call cost 5 credits (1 + 4 variant EANs). Without `variants_ean` it costs 1 and only `ean` (of `code`) is filled.

### The same code on another storefront

```bash
curl -X POST https://api.scavio.dev/api/v1/douglas/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "5012103059", "market": "nl"}'
```

Captured (2026-11-26): DIOR Miss Dior Eau de parfum 30 ml, `price` 68.62 EUR, `was_price` 91.5, `discount_percent` 25.01, `lowest_price_30d` null, `rating` 4.7 from 30 reviews, 4 variants. With `market` `be-nl` the same code read 64.05 EUR, was 91.5, 30% (rating 4.8 from 291 reviews); `be-fr` returned the same price with French texts. Ratings and review counts are per storefront too.

### A keyword Douglas sends to a brand page

```bash
curl -X POST https://api.scavio.dev/api/v1/douglas/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "dior"}'
```

Captured `data` (2026-11-26; `items` cut to 2 of 48, `url`, `image`, `facets`, `sorts` and `breadcrumbs` dropped):

```json
{
  "query": "dior",
  "market": "de",
  "currency": "EUR",
  "redirected_to": "https://www.douglas.de/de/b/dior/b0690",
  "list_type": "brand",
  "category_code": "b0690",
  "sort_applied": "relevance",
  "page": 1,
  "page_size": 48,
  "total": 260,
  "total_pages": 6,
  "has_more": true,
  "count": 48,
  "items": [
    {"code": "1251306", "base_code": "3001055243", "name": "Dior Backstage", "base_name": "Glow Maximizer Palette", "brand": "DIOR", "product_family": "Highlighter", "price": 48.8, "currency": "EUR", "was_price": 61, "discount_percent": 20, "lowest_price_30d": null, "rrp": null, "availability": "AVAILABLE", "rating": 4.7},
    {"code": "1216596", "base_code": "5011686019", "name": "Dior Addict", "base_name": "Lip Glow", "brand": "DIOR", "product_family": "Lippenbalsam", "price": 30.95, "currency": "EUR", "was_price": 48, "discount_percent": 35.52, "lowest_price_30d": 31.95, "rrp": null, "availability": "AVAILABLE", "rating": 4.7}
  ],
  "notes": ["Douglas sends this keyword to a brand page: the answer is that page's list.", "Listing pages are large and slow: an answer takes 5 to 210 seconds.", "total is the count the listing page shows."]
}
```

With a brand filter and a sort: `{"query": "parfum", "brand_filter": "b0611", "sort": "top_rated"}` returned 62 Yves Saint Laurent products, first the Libre Eau de Parfum at 76.95 EUR (rating 4.8).

### Black Friday deals with the offers page

```bash
curl -X POST https://api.scavio.dev/api/v1/douglas/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"collection": "beauty_friday", "market": "pl"}'
```

Captured (2026-11-26): `total` 21869, first a Rituals Medium Gift Set at 141.75 PLN, `was_price` 189, `discount_percent` 25, `lowest_price_30d` 189. `promotions` held 7 entries from the offers page; the first, a teaser headed "RABATY DO 25%", carried the `legal_text` "Oferta obowiązuje na wybrane produkty do 30.11.2026 lub do wyczerpania zapasów na douglas.pl i w aplikacji Douglas ...". On de the same collection read 2670 products with 8 promotions; one `legal_text` began "Bis zu 25%-Aktion: *¹Gültig vom 25.11. bis zum 30.11.2026 ...". Quote validity dates and codes only as Douglas words them.

### Stores, store, review summary, suggestions, brands

- `/stores` `{"query": "Berlin"}`: `total` 28 over 3 pages, nearest first: Berlin Mitte Alexa (`store_id` 00020475, Grunerstrasse 20, 0.76 km), Berlin Mitte Unter den Linden (00020414, 1.09 km), Berlin Mall of Berlin (00020431, 1.81 km), each with `operator`, `phone`, weekly `hours` and dated `special_hours`. A place the store finder cannot place came back as a `200` with `count` 0.
- `/store` `{"store_id": "00020475"}`: Berlin Mitte Alexa, Monday 10:00-20:00, `special_hours` 2026-11-27 10:00-21:00, 2026-12-24 10:00-14:00 and 2026-12-25 closed, `top_brands` The Ordinary, Sol de Janeiro, Charlotte Tilbury ..., with `parking` and `public_transport` as Douglas writes them.
- `/review-summary` `{"code": "5000005003"}`: Douglas' own German summary of the YSL Libre reviews ("Das Yves Saint Laurent Libre Parfüm ist ein elegantes, feminines und langanhaltend duftendes Parfüm ..."), `summary_type` `ai_generated`. On pl, code 5012111079 (a set with no reviews) returned `summary` null.
- `/suggestions` `{"query": "dior"}`: 10 products (first the DIOR Glow Maximizer Palette) and `trending_terms` "adventskalender 2026", "huda beauty puder", "blush": the storefront's trending searches, the same for every query, not matches.
- `/brands` `{"query": "dior"}`: 1 of 1890 brands, DIOR, `code` b0690 (the input of `/brand`), in 18 seconds. The full index on cz listed 684 brands.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def douglas(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/douglas/{endpoint}", headers=HEADERS, json=body, timeout=250)
    r.raise_for_status()
    return r.json()

# The same product code on three storefronts (1 credit each)
for market in ["nl", "be-nl", "be-fr"]:
    d = douglas("product", {"code": "5012103059", "market": market})["data"]
    print(market, d["currency"], d["price"], d["was_price"], d["lowest_price_30d"], d["rrp"])

# Every size with its four prices (1 credit)
p = douglas("product", {"code": "5000005003"})["data"]
for v in p["variants"]:
    print(v["name"], v["price"], v["was_price"], v["lowest_price_30d"], v["rrp"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market`, `country`, `language`, `currency` and `notes`.

- **item** (search, category, brand, deals) - `code`, `base_code`, `name`, `base_name`, `brand`, `brand_line`, `product_family`, `url`, `image`, `price`, `currency`, `price_text`, `was_price`, `discount_percent`, `lowest_price_30d`, `rrp`, `price_type`, `unit_price` {`price`, `per`}, `content` {`amount`, `unit`}, `sizes`, `colors_count`, `availability`, `in_stock`, `rating`, `rating_stars`, `flags`, `marketplace` {`is_marketplace`, `vendor`}.
- **listing** (search, category, brand, deals) - `redirected_to`, `list_type` (`search`, `category`, `brand`), `url`, `title`, `category_code`, `sort`, `sort_applied`, `filters`, `filters_applied`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `items[]`, `facets[]` {`facet`, `name`, `multi_select`, `values[]` {`value`, `name`, `count`, `selected`}}, `sorts[]` {`sort`, `name`, `selected`}, `breadcrumbs`. Search adds `query`; category adds `category`; brand adds `brand`.
- **deals** - `collection`, `category`, `offers_page`, `promotions[]` {`kind`, `headline`, `text`, `link_text`, `url`, `image`, `legal_text`, `labels`, `updated_at`} (or `null`), then as listing.
- **product** - `requested`, `source` (`api`, or `page` when only the product page lists the code: slower), `code`, `base_code`, `name`, `brand` {`code`, `name`, `url`}, `brand_line`, `product_family`, `gender`, `url`, `ean`, `description`, `bullets`, `application`, `ingredients`, the four prices, `price_text`, `price_type`, `unit_price`, `content`, `stock_level`, `availability`, `availability_text`, `in_stock`, `max_order_quantity`, `rating`, `rating_stars`, `review_count`, `images`, `videos`, `categories[]` {`code`, `name`, `url`}, `attributes[]` {`code`, `name`, `values`}, `scent_notes` {`top`, `heart`, `base`}, `flags[]` {`code`, `name`}, `marketplace`, `variant_type`, `variant_count`, `variants[]` {`code`, `name`, `url`, the four prices, `unit_price`, `content`, `stock_level`, `availability`, `availability_text`, `in_stock`, `flags`, `image`, `ean` (with `variants_ean`)}, `variants_ean` {`requested`, `fetched`, `capped`}.
- **stores** - `query`, `location` {`text`, `latitude`, `longitude`}, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `stores[]` {`store_id`, `name`, `url`, `operator`, `address` {`street`, `house_number`, `postal_code`, `city`, `country_code`, `formatted`}, `phone`, `latitude`, `longitude`, `distance_km`, `hours[]` {`day`, `day_of_week`, `closed`, `open`, `close`}, `special_hours[]` {`date`, `closed`, `open`, `close`, `note`}, `features` (Douglas' store feature codes), `images`, `temporarily_closed`}.
- **store** - every stores field plus `parking`, `public_transport`, `top_brands[]` {`code`, `name`, `url`}, `events`, `service_booking`.
- **review summary** - `code`, `summary` (Douglas' text, or `null`), `summary_type` (`ai_generated`).
- **suggestions** - `query`, `count`, `products[]` {`base_code`, `code`, `name`, `brand`, `brand_line`, `product_family`, `url`, `image`}, `trending_terms`.
- **brands** - `query`, `letter`, `total`, `count`, `brands[]` {`code`, `name`, `url`, `letter`, `logo`}.

## Guardrails

- Name it "Douglas (douglas.de, the Dusseldorf-based beauty retailer with about 1,960 stores in Europe)" on first mention, "Douglas" after that, and name the storefront for every figure (douglas.nl, douglas.pl ...).
- Prices: quote each with its currency, storefront, size or shade and the `fetched_at` date ("listed on douglas.de on Nov 26, 2026"). `was_price`, `lowest_price_30d` and `rrp` are "as Douglas shows them"; `discount_percent` is Douglas' figure. A percent you compute yourself (against another storefront, or against the 30-day low) is labelled computed.
- Comparisons: same product code, or same EAN, or the same brand, line, product type and size, at named storefronts on one date. Show the numbers and their difference only; never call a price a deal, a bargain, a fake discount or the cheapest, and never convert currencies without saying which rate and date you used.
- Offers: quote validity dates and codes only as `legal_text` words them, with the capture date. No countdowns or urgency.
- Reviews: `rating` and `review_count` as returned; the review summary is Douglas' own AI-generated text, quoted as Douglas' summary, never as Scavio's or a customer's words. Review texts are not returned.
- Descriptive only: no efficacy, skin or health claims; report ingredients, scent notes and product types as Douglas labels them. No commentary on Douglas' business or pricing practices.
- Do not republish Douglas product photos or descriptions at length; cite product names, codes and capture dates, and write douglas.de as plain text.
- Terms: Scavio does not collect or store Douglas data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account, no cart and no checkout. Douglas' terms cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, was prices, 30-day lows, RRPs, EANs, codes, stores or summaries. Only return what the API returned, with the `fetched_at` time.
- Not available: review texts, review paging or star filters, per-store stock, store reservation, price history (store your own), cart or checkout, and the Portugal, Croatia, Slovenia, Latvia, Estonia, Bulgaria and France (Nocibe) shops.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: an unknown `market`, or `pt`, `hr`, `si`, `lv`, `ee`, `bg` ("Douglas Portugal runs on a different shop platform and is not offered yet.") or `fr` ("Douglas trades in France as Nocibe, not under the Douglas name: France is not offered."); a `market` that does not match the link's storefront; product with both `code` and `url` or neither, a `code` that is not digits; a category that is not a path ending in its code, its code or a category link; a brand that is not a brand code, path or link; `sale_only` on `ch-de` or `ch-fr` ("Douglas Switzerland shows no sale badge to filter by. Use deals (its promotions list) or read was_price."); deals with both `collection` and `category`; more than 10 filter values; `filters` entries that are not {facet, value}; `page` above 200; a `store_id` that is not digits.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Douglas <market> has no product <code>.", "Douglas <market> has no category <code> (or no products on this page).", "Douglas <market> has no brand <code> (or no products on this page).", "Douglas <market> has no deal list <code> right now (or no products on this page).", "Douglas <market> has no store <id>.", "Douglas' store finder (<market>) could not place "<query>". Try a city or a postcode.". Take codes and store ids from a previous answer rather than guessing them; a product one storefront sells can be a `404` on another.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api).
- `502` means Douglas data was temporarily unavailable ("Douglas is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy: wait the `Retry-After` seconds and send it again. Not charged.
- A slow answer is normal on listings (up to 210 seconds): keep the client timeout at 250 seconds rather than cancelling and resending.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.96.0
npm install scavio@0.97.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: product } = await scavio.douglas.product({ code: "5000005003", variants_ean: true });
const { data: nl } = await scavio.douglas.product({ code: "5012103059", market: "nl" });
const { data: hits } = await scavio.douglas.search({ query: "parfum", brand_filter: "b0611", sort: "top_rated" });
const { data: deals } = await scavio.douglas.deals({ collection: "beauty_friday", market: "pl" });
const { data: summary } = await scavio.douglas.reviewSummary({ code: "5000005003" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.douglas.search(...)`, `category`, `brand`, `deals`, `product`, `stores`, `store`, `review_summary`, `suggestions` and `brands`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 10 endpoints as tools: `search_douglas`, `get_douglas_category`, `get_douglas_brand`, `get_douglas_deals`, `get_douglas_product`, `get_douglas_stores`, `get_douglas_store`, `get_douglas_review_summary`, `get_douglas_suggestions` and `get_douglas_brands`. Douglas is opt-in: add `douglas` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,douglas"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/douglas-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api), [category](https://scavio.dev/docs/douglas-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api), [brand](https://scavio.dev/docs/douglas-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api), [deals](https://scavio.dev/docs/douglas-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api), [product](https://scavio.dev/docs/douglas-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api), [stores](https://scavio.dev/docs/douglas-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api), [store](https://scavio.dev/docs/douglas-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api), [review summary](https://scavio.dev/docs/douglas-review-summary?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api), [suggestions](https://scavio.dev/docs/douglas-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api), [brands](https://scavio.dev/docs/douglas-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api). Platform page: [scavio.dev/douglas-api](https://scavio.dev/douglas-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=douglas-beauty-api).
