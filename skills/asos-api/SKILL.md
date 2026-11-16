---
name: asos-api
description: "ASOS API for ASOS prices by country and currency: one ASOS product's price, previous price (ASOS's was price), RRP, lowest price of the last 30 days where ASOS shows it, sale and outlet flags, discount and online stock by size in each ASOS store and currency, never converted; product ids and category ids are the same in every ASOS store, so one id prices the item everywhere, and the stock endpoint takes up to 100 product ids per call with the ids a store does not sell listed apart. Keyword search sorted by relevance, newest or price and filtered by gender, brand, colour, size, body-fit range (plus, petite, tall, maternity, hourglass, wide fit, fuller bust), product type, price, sale or any facet, up to 200 per page (keyword results reach position 2,088); one product in full by id, co-ord set id or link, with description, composition, care, size and fit, country of manufacture, every size variant with SKU, EAN, price and online stock (in stock, low stock, restocking soon), the rating with fit and quality, ASOS's own labelled AI review summary and the other colours; customer reviews per store, up to 50 per page, sorted by relevance, newest, oldest or rating and filtered by star rating, with fit and quality averages, no reviewer names; search suggestions with result counts; the store's women and men category tree and every product of a category or brand page; the A-Z brand list; the Sale and New In lists for women or men; the markets table with every country's store, language, currencies and size schema. 235 countries and 245 country-currency combinations: ASOS's UK, US, French, German, Spanish, Italian, Australian, Danish, Dutch, Polish and Swedish stores in their own languages, plus its European and international stores in English (Ireland, Portugal, Belgium, Norway, Canada, Mexico, India, South Africa, Switzerland, New Zealand, the UAE, Saudi Arabia, Hong Kong, Israel, Japan, South Korea, Singapore, Taiwan, China and more), in GBP, USD, EUR, AUD, DKK, PLN, SEK, NOK, CAD, CHF, NZD, AED, SAR, HKD, ILS, SGD, TWD or CNY. 11 endpoints, 1 credit per call. Online stock only (ASOS has no physical stores), no outlet, no promo codes, no price history (poll and store). ASOS has no public product data API."
version: 1.0.0
tags: asos, asos-api, asos-product-data, asos-product-api, asos-prices, asos-prices-by-country, asos-price-api, asos-price-tracker, asos-sale, asos-stock, asos-stock-by-size, asos-reviews, asos-reviews-api, asos-new-in, asos-brands, asos-black-friday, fashion, fashion-prices, clothing-prices, apparel, retail, price-comparison, price-monitoring, price-tracker, multi-country, multi-currency, regional-pricing, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/asos-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=asos-api
---

# ASOS API - Prices by Country and Currency, Stock by Size, Reviews

Read ASOS's own online stores (asos.com): keyword search, one product in full with every size, the price and online stock of up to 100 products in one call, customer reviews per store, search suggestions, the category tree and any category list, the A-Z brand list, the sale and new-in lists, and the table of every country ASOS sells in. All 11 endpoints return structured JSON and cost 1 credit per call.

**The job this skill is for: ASOS prices by country and currency.** One ASOS product's price, previous price, RRP, sale flag and stock by size in each ASOS store and currency. **Product ids and category ids are the same in every ASOS store**; titles come back in the store's language. Prices are set per store and currency, not per country inside a store: ASOS's European store prices Ireland and Portugal alike in EUR. Which products a country is offered can still differ (shipping restrictions). `/stock` takes up to 100 product ids per call, so one call per store and currency prices a whole list.

Captured on 2026-11-16 from `/stock` with `product_ids` `205338218` (Jack & Jones Eddie loose jeans in washed black) and `206956133` (Jack & Jones Alex baggy jean in washed black), one call per row:

| `country` | `store` | `currency` | `205338218` `price` | `206956133` `price` |
|---|---|---|---|---|
| `gb` | `gb` | GBP | 27 | 27 |
| `us` | `us` | USD | 49 | 32.76 (`previous_price` 40.95, `discount_percent` 20) |
| `fr` | `fr` | EUR | 29.99 | 29.99 |
| `de` | `de` | EUR | 31.99 | 29.99 |
| `es` | `es` | EUR | 31.99 | 29.99 |
| `it` | `it` | EUR | 31.99 | 29.99 |
| `nl` | `nl` | EUR | 39.99 | 29.99 |
| `ie` | `europe` | EUR | 31.99 | 29.99 |
| `au` | `au` | AUD | 57 | 57 |
| `dk` | `dk` | DKK | 279 | 279 |
| `pl` | `pl` | PLN | 169 | 169 |
| `se` | `se` | SEK | 389 | 389 |
| `ca` | `international` | CAD | 62 | 57 |
| `jp` | `international` | USD | 46 | 43 |
| `ae` | `international` | AED | 135 | 130 |
| `ae` (`currency: "GBP"`) | `international` | GBP | 29 | 27 |

The same ids answered on all 16 rows, each in the row's currency, never converted. The euro stores did not agree (the Eddie jeans were 29.99 EUR on `fr`, 31.99 on `de`, `es`, `it` and the European store, 39.99 on `nl`), and the same currency on another store is another price (27 GBP on `gb`, 29 GBP on the international store for `ae`). Only the US store had the Alex jean marked down that day. To compare stores, convert explicitly and state the rate and its date.

**The price fields.** `price` is the current price. `previous_price` is ASOS's "was" price on a markdown and `rrp` its recommended retail price; each is set only when it is above `price`. `discount_percent` is computed against `previous_price`, else against `rrp`, and `discount_basis` says which. `lowest_price_30d` is the lowest price of the last 30 days where ASOS shows it. `is_marked_down` and `is_outlet` are ASOS's own flags. Product and stock add `price_since`, when the current price started, and every size variant carries its own `price` and `previous_price` (ASOS's terms say a size sold by an ASOS Brand Partner can be priced differently from one sold by ASOS).

**Price history.** ASOS shows none and none is returned. To build one, call `/stock` (up to 100 ids) or `/product` on a schedule and store each reading with its time, country, store and currency. ASOS has announced Black Friday 2026 offers from Friday November 27 to Cyber Monday November 30 (its French store's page), and the `gb` store's women's menu carried a "Black Friday" heading in the `/categories` capture of 2026-11-16.

ASOS has no public product data API. Its GitHub organisation hosts engineering tools, not a catalogue API, and partner connectors are for businesses that trade with ASOS.

See also: for Zara prices by country use `zara-api`; for H&M prices by country use `hm-api`; for second-hand fashion on Vinted use `vinted-api`; for Nordstrom fashion prices, markdowns and per-size stock use `nordstrom-product-data`; for the cross-merchant view of one product use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Compare one ASOS item's price across countries and currencies (one product id, one call per store and currency)
- Check whether an ASOS item is on sale in a store: its price, previous price or RRP, discount and the lowest price of the last 30 days
- Track ASOS prices over time (Black Friday, the sale) by polling up to 100 product ids per call and storing each reading
- Check which sizes of an ASOS item are in stock online, or low on stock, in a store
- Read ASOS customer reviews of a product on one store, with fit and quality ratings and ASOS's AI summary
- Search ASOS by keyword in a store, sorted by price or newest, filtered by gender, brand, colour, size, body-fit range (plus, petite, tall, maternity ...), product type, price or sale
- Read one ASOS product in full: description, composition, care, size and fit, country of manufacture, every size with price and stock, the other colours
- Browse ASOS's category tree, one category or brand page, the A-Z brand list, the sale list or the new-in list
- Get ASOS's search suggestions for what a shopper has typed
- List the countries ASOS sells in with their store, language and currencies

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=asos-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=asos-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits: 50 calls at 1 credit, enough to price 100 products on every one of the 13 stores.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures most calls took 1 to 5 seconds; a product page took up to about 10 seconds. Set a client timeout of at least 120 seconds and do not fire many calls at once (a busy moment answers `503` with `Retry-After`).

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/asos/search` | 1 | Items for a keyword with prices, colours and flags, facets with value ids, price range, `total` and `max_reachable` |
| `POST /api/v1/asos/product` | 1 | One product (or co-ord set) by `product_id`, `group_id` or `url`: details, composition, care, size and fit, every size variant with price and online stock, rating, ASOS's AI review summary, the other colours |
| `POST /api/v1/asos/stock` | 1 | Price and online stock per variant of up to 100 product ids; `not_found` lists the ids the store does not sell |
| `POST /api/v1/asos/reviews` | 1 | Reviews of one product on one store, up to 50 per page, with the rating summary, fit and quality averages and ASOS's AI summary |
| `POST /api/v1/asos/suggestions` | 1 | Search suggestions with ASOS's result count, in the store's language |
| `POST /api/v1/asos/category` | 1 | Every product of one category (or brand page), paged and sorted, with the search filters |
| `POST /api/v1/asos/categories` | 1 | The store's women and men navigation tree with category ids |
| `POST /api/v1/asos/brands` | 1 | The store's A-Z brand list for women or men |
| `POST /api/v1/asos/deals` | 1 | The store's Sale category for women or men |
| `POST /api/v1/asos/new-arrivals` | 1 | The store's New In category for women or men |
| `POST /api/v1/asos/markets` | 1 | Every country in ASOS's country selector with its store, language, currencies and size schema |

A not-found (an unknown id, or a product the store does not sell) is charged 1 credit; a failed call is not charged.

## Markets

Every endpoint takes `country` (lowercase ISO-2, default `gb`; `gb` for the United Kingdom, not `uk`) and `currency` (ISO-4217, default ASOS's own default for the country). Every answer echoes `country`, `currency`, `store` and `language`. `store` names the ASOS store that served the country: one of the 11 stores with a site of their own (`gb`, `us`, `fr`, `de`, `es`, `it`, `au`, `dk`, `nl`, `pl`, `se`, each in its own language), `europe` (ASOS's European store, in English) or `international` (ASOS's international store, in English).

235 countries, 245 country-currency combinations:

| `store` | Language | `country` (currency) |
|---|---|---|
| `gb` | en-GB | `gb` (GBP) |
| `us` | en-US | `us`, `pr` (USD) |
| `fr` | fr-FR | `fr`, `mc` (EUR); `bl`, `gf`, `gp`, `mf`, `mq`, `nc`, `pf`, `pm`, `re`, `tf`, `wf`, `yt` (USD) |
| `de` | de-DE | `de`, `at` (EUR) |
| `es` | es-ES | `es`, `ad` (EUR) |
| `it` | it-IT | `it`, `sm`, `va` (EUR) |
| `au` | en-AU | `au`, `cc`, `cx`, `nf` (AUD) |
| `dk` | da-DK | `dk` (DKK) |
| `nl` | nl-NL | `nl` (EUR) |
| `pl` | pl-PL | `pl` (PLN) |
| `se` | sv-SE | `se` (SEK) |
| `europe` (33) | en-GB | EUR: `al`, `ax`, `be`, `bg`, `cy`, `cz`, `ee`, `fi`, `gr`, `hr`, `hu`, `ie`, `lt`, `lu`, `lv`, `md`, `me`, `mk`, `mt`, `pt`, `ro`, `rs`, `si`, `sk`; GBP: `am`, `ba`, `ge`, `kg`, `kz`; DKK: `fo`, `gl`; NOK: `no`, `sj` |
| `international` (170) | en-GB | `ae` (AED or GBP), `ca` (CAD), `ch` and `li` (CHF), `cn` (CNY), `gi` and `is` (GBP), `hk` and `mo` (HKD or GBP), `il` (ILS, GBP or USD), `jp` and `kr` (USD or GBP), `kw` and `qa` (GBP or USD), `nu`, `nz`, `pn` and `tk` (NZD), `sa` (SAR or GBP), `sg` (SGD), `tv` (AUD), `tw` (TWD), `xk` (EUR); USD: the other 147, including `mx`, `br`, `ar`, `cl`, `co`, `in`, `id`, `my`, `ph`, `th`, `vn`, `tr`, `ua`, `za`, `eg`, `ng`, `ke`, `ma` |

- The first currency listed is ASOS's default for the country; any currency listed is accepted. `/markets` answers the full list live (country, name, store, language, currencies, default currency, size schema).
- Every endpoint serves every combination except `/suggestions` on `pl` (ASOS's Polish store answers no search suggestions; use search there).
- Held back, answering `400` before anything is charged: `uk` (use `gb`); `ru` and `by` (ASOS is not selling there); any country ASOS does not list; a currency ASOS does not offer the country (the error lists the allowed ones).
- Reviews are per store: the same product has different reviews on `gb` and `de`. The European and international stores share one review pool.

## Workflow

1. **One item, every store:** take the product id (`product_id` of any answer, or the number after `/prd/` in an ASOS link: it is the same id in every store). Call `/stock` with `product_ids` once per `country` (and `currency`) you need. Each product gives `price`, `previous_price`, `rrp`, `lowest_price_30d`, `discount_percent`, `is_marked_down`, `in_stock` and its variants; `not_found` lists the ids the store does not sell. Store each reading with its time.
2. **Is it on sale:** `is_marked_down` is true and `previous_price` (or `rrp`) is set, with `discount_percent` and `discount_basis`. Not every store marks an item down at the same time.
3. **Sizes in stock online:** `/product` returns every size in `variants` with `size`, `in_stock`, `low_stock` and `restocking_soon`. `/stock` returns the same flags per `variant_id` without size names: map each `variant_id` to `variants[].size` of the product answer. Stock is ONLINE stock; ASOS has no physical stores.
4. **Reviews:** `/reviews` with `product_id` on the store you care about, `sort` `newest` for the latest. `summary` carries the star distribution and fit and quality averages; `ai_summary` is ASOS's own AI-generated summary, labelled as such.
5. **Browse:** `/categories` for the tree, then `/category` with a `category_id`. `/deals` (Sale) and `/new-arrivals` (New In) are the same category ids in every store. For one brand's products, take `brand_id` from `/brands` and pass it to `/category` as `category_id`.
6. **Search:** `/search` with `query`; read `facets` from the first answer, then filter with those value ids. Keyword results stop at position 2,088 however large `total` is (`max_reachable`): narrow with filters or use a category for more.
7. **Price tracking:** poll `/stock` (up to 100 ids per call) on a schedule and store each reading. There is no price history endpoint.

## Parameters

### Shared

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `gb` | See Markets |
| `currency` | string | the country's default | Any currency ASOS offers the country (see Markets) |
| `page` | integer | 1 | 1 to 1,000 (search, category, deals, new arrivals); search pages past position 2,088 answer `400` |
| `page_size` | integer | 72 | 1 to 200 (search, category, deals, new arrivals) |
| `sort` | string | `relevance` | `relevance` (ASOS's own order), `newest`, `price_asc` or `price_desc` |

### Grid filters (search, category, deals, new arrivals)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `gender` | string | none | `women`, `men` or `unisex` (search, category). On deals and new arrivals: `women` (default) or `men` |
| `brand` | id or list | none | Value ids of the `brand` facet of an earlier answer (`53` ASOS DESIGN, `401` Levi's); several are ORed. Not a `brand_id` from `/brands` |
| `color` | name, id or list | none | `red`, `green`, `blue`, `black`, `white`, `yellow`, `orange`, `purple`, `pink`, `brown`, `gold`, `silver`, `copper`, `grey`, `multi`, `navy`, `neutral`, or `base_colour` facet ids |
| `size` | id or list | none | Value ids of the `size` facet (`279` XS) |
| `range` | name, id or list | none | Body-fit range: `plus`, `petite`, `tall`, `maternity`, `hourglass`, `wide_fit`, `fuller_bust` |
| `product_type` | id or list | none | Value ids of the Product Type facet, `attribute_1047` (`8393` Jeans) |
| `price_min` / `price_max` | number | none | Price range in the request's currency |
| `on_sale` | boolean | false | Only sale items (search, category) |
| `facets` | object | none | Any other facet: `{ "facet id": "value id" or ["value ids"] }`, e.g. `{"attribute_1046": "8310", "discount_band": ["5", "6"]}` (`facets[].id` and `facets[].values[].id` of an earlier answer) |

Up to 30 values per filter.

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords, 1-200 chars, in the store's language or English |

### Product (`/product`)

Send exactly one of:

| Parameter | Type | Description |
|---|---|---|
| `product_id` | string | An ASOS product id (`210309625`) |
| `group_id` | string | A co-ord set's id (`group_id` of a `group` or `group_piece` item, the number after `/grp/`) |
| `url` | string | An ASOS product link from any store (`https://www.asos.com/<store>/<brand>/<slug>/prd/<id>` or `/grp/<id>`); its store's country is used unless `country` is sent |

A piece of a co-ord set answers the whole set (`product_type: "group"` with `items[]`).

### Stock (`/stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_ids` | list or string | required | 1 to 100 product ids, a list or comma-separated |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | An ASOS product id |
| `page` | integer | 1 | 1 to 500 |
| `page_size` | integer | 10 | 1 to 50 |
| `sort` | string | `relevance` | `relevance`, `newest`, `oldest`, `rating_desc` or `rating_asc` |
| `rating` | integer | none | Only reviews with this star rating (1 to 5) |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far, 1-100 chars |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | required | A `category_id` from `/categories` or a `brand_id` from `/brands` (`8799` women's dresses, `7046` women's sale); the same id in every store |

### Categories (`/categories`), brands (`/brands`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `gender` | string | categories: both; brands: `women` | `women` or `men` |

### Deals (`/deals`), new arrivals (`/new-arrivals`)

`gender` `women` (default) or `men`, plus the shared paging and sort and the grid filters. Deals is ASOS's Sale category (`7046` women, `8409` men); new arrivals is its New In category (`27108` women, `27110` men).

### Markets (`/markets`)

`country` and `currency` only: `selected` carries the requested country's live currencies.

## Examples

### Stock

```bash
curl -X POST https://api.scavio.dev/api/v1/asos/stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_ids": ["205338218", "206956133", "209793673"], "country": "gb"}'
```

Captured `data` (gb, 2026-11-16; 1 of 3 products, 2 of 27 variants and 1 of 3 notes shown):

```json
{
  "products": [
    {
      "product_id": 205338218,
      "price": 27,
      "previous_price": null,
      "rrp": null,
      "lowest_price_30d": null,
      "is_marked_down": false,
      "is_outlet": false,
      "discount_percent": null,
      "discount_basis": null,
      "currency": "GBP",
      "price_since": "2023-07-07T01:12:46Z",
      "in_stock": true,
      "restocking_soon": false,
      "variants": [
        {"variant_id": 205338234, "in_stock": true, "low_stock": false, "restocking_soon": false, "price": 27, "previous_price": null, "seller": null},
        {"variant_id": 205338266, "in_stock": false, "low_stock": false, "restocking_soon": false, "price": 27, "previous_price": null, "seller": null}
      ]
    }
  ],
  "count": 3,
  "not_found": [],
  "country": "gb",
  "currency": "GBP",
  "store": "gb",
  "language": "en-GB",
  "notes": ["variants carry ASOS's variant ids: the product answer's variants[] map each variant_id to its size."]
}
```

ASOS's stock answer has no size names. In the product capture of the same id, variant `205338266` is size `W26 L32`: the one size of 27 out of stock online on `gb` that day.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/asos/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "210309625"}'
```

Captured `data` (gb, 2026-11-16; 1 of 4 other colours, 3 of 8 variants and 1 of 4 notes shown; `breadcrumbs`, the 40 `category_ids`, `product_details`, `brand_description`, images and video dropped):

```json
{
  "product_id": 210309625,
  "product_type": "product",
  "product_code": "155057068",
  "title": "Mango Danila straight leg jean in light blue",
  "brand": "Mango",
  "brand_id": 12117,
  "gender": "Women",
  "product_kind": "Jeans",
  "url": "https://www.asos.com/prd/210309625",
  "category": {"category_id": 3630, "name": "Jeans"},
  "description": "Jeans by Mango\nStraight fit\nMid rise\nBelt loops\nFunctional pockets\nRaw hem",
  "composition": "Non-stretch denim: light-blue wash\nMain: 100% Cotton.",
  "care": "Machine wash according to instructions on care label",
  "size_and_fit": "Model's height: 168cm / 5'6¼\"\nModel is wearing: UK 8",
  "fit": "Straight",
  "country_of_manufacture": "PK",
  "color": "LIGHT BLUE",
  "color_products": [
    {"product_id": 209516777, "color": "DARK BLUE", "title": "Mango Danila 100% cotton wide leg jean in dark blue", "url": "https://www.asos.com/prd/209516777"}
  ],
  "price": 20.99,
  "previous_price": 35.99,
  "rrp": null,
  "lowest_price_30d": 19.99,
  "is_marked_down": true,
  "is_outlet": false,
  "discount_percent": 42,
  "discount_basis": "previous_price",
  "currency": "GBP",
  "price_since": "2026-10-19T23:00:00Z",
  "in_stock": true,
  "selling_fast": true,
  "is_discontinued": false,
  "one_size": false,
  "variants": [
    {"variant_id": 210309633, "size": "UK 4", "brand_size": "UK 4", "size_id": 399133, "color": "LIGHT BLUE", "sku": "155057079", "ean": "8447542233848", "price": 20.99, "previous_price": 35.99, "in_stock": false, "low_stock": false, "restocking_soon": false, "seller": null},
    {"variant_id": 210309634, "size": "UK 6", "brand_size": "UK 6", "size_id": 399136, "color": "LIGHT BLUE", "sku": "155057080", "ean": "8447542233855", "price": 20.99, "previous_price": 35.99, "in_stock": true, "low_stock": false, "restocking_soon": false, "seller": null},
    {"variant_id": 210309628, "size": "UK 8", "brand_size": "UK 8", "size_id": 399131, "color": "LIGHT BLUE", "sku": "155057081", "ean": "8447542233862", "price": 20.99, "previous_price": 35.99, "in_stock": true, "low_stock": false, "restocking_soon": false, "seller": null}
  ],
  "rating": {
    "average": 4,
    "count": 31,
    "distribution": {"1": 2, "2": 3, "3": 4, "4": 6, "5": 16},
    "recommended_percent": 67,
    "fit": {"label": "Fit", "percentage": 52, "min_label": "Runs Small", "max_label": "Runs Large"},
    "quality": {"label": "Quality", "percentage": 81, "min_label": "Poor", "max_label": "Great"}
  },
  "ai_summary": {
    "text": "Customers overwhelmingly praise the flattering silhouette and vibrant blue color, with many noting frequent compliments and describing the fit as perfect. However, sizing inconsistencies present a notable concern—several report the waist runs large or tight depending on body type, while many customers under 5'7\" find the length excessive, requiring alterations. A few mention the material feels stiff initially. Despite these drawbacks, most customers consider the jeans worthwhile for their attractive style and fit.",
    "disclaimer": "AI-generated from customer ratings & reviews, and may include incentivized reviews.",
    "source": "ASOS's own AI-generated summary of customer reviews"
  },
  "country": "gb",
  "store": "gb",
  "language": "en-GB",
  "notes": ["Stock is ASOS's online stock (ASOS has no physical stores)."]
}
```

Each colour is its own product id (`color_products`). On this day the light blue jean was 20.99 GBP, down 42% from 35.99, and its lowest price of the last 30 days was 19.99: below the current price. `country_of_manufacture` is the ISO-2 code ASOS gives (`PK`, Pakistan).

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/asos/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "210309625", "sort": "newest"}'
```

Captured `data` (gb, 2026-11-16; 1 of 10 reviews and 1 of 2 notes shown, the `ai_summary` text shortened here; it is the same summary as on product):

```json
{
  "product_id": 210309625,
  "summary": {
    "average": 4,
    "count": 31,
    "ratings_only_count": 12,
    "distribution": {"1": 2, "2": 3, "3": 4, "4": 6, "5": 16},
    "recommended_count": 4,
    "not_recommended_count": 2,
    "recommended_percent": 67,
    "fit": {"average": 3.07, "range": 5, "min_label": "Runs Small", "max_label": "Runs Large"},
    "quality": {"average": 4.24, "range": 5, "min_label": "Poor", "max_label": "Great"}
  },
  "ai_summary": {
    "text": "Customers overwhelmingly praise the flattering silhouette and vibrant blue color ...",
    "disclaimer": "AI-generated from customer ratings & reviews, and may include incentivized reviews.",
    "source": "ASOS's own AI-generated summary of customer reviews"
  },
  "reviews": [
    {
      "id": "1236988261",
      "rating": 5,
      "title": null,
      "text": "These jeans are great for those who are tall with long legs. I’m 5’8 and they fit perfectly. Waist was a little big, but there’s nothing a belt can’t fix. Got compliments on how nice they look",
      "date": "2026-11-15T13:00:26.000Z",
      "experience_date": "2026-11-15",
      "ratings_only": false,
      "recommended": null,
      "fit": {"value": 3, "label": "True to Size"},
      "quality": {"value": 4, "label": "Good"},
      "color": "LIGHT BLUE",
      "verified_purchaser": true,
      "language": "en_US",
      "syndicated": false,
      "source": null,
      "photos": []
    }
  ],
  "count": 10,
  "total": 31,
  "page": 1,
  "page_size": 10,
  "has_more": true,
  "sort": "newest",
  "country": "gb",
  "currency": "GBP",
  "store": "gb",
  "language": "en-GB",
  "notes": ["Reviews are per store: the same product has different reviews on each store (gb, de, fr ...); the European and international stores share one review pool."]
}
```

A `ratings_only` review has a rating and no text (12 of the 31 here). `syndicated` reviews come from another site and name it in `source`. Reviewer names are never returned.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/asos/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "jeans", "page_size": 24}'
```

Captured `data` (gb, 2026-11-16; 1 of 24 items, 2 of 16 facets with 2 values each and 1 of 3 notes shown; image links dropped):

```json
{
  "query": "jeans",
  "items": [
    {
      "product_id": 211665482,
      "product_type": "product",
      "group_id": null,
      "title": "Bershka Mid-waist straight jeans in blue",
      "brand": "Bershka",
      "color": "BLUE",
      "url": "https://www.asos.com/bershka/bershka-mid-waist-straight-jeans-in-blue/prd/211665482",
      "price": 29.99,
      "previous_price": null,
      "rrp": null,
      "lowest_price_30d": null,
      "is_marked_down": false,
      "is_outlet": false,
      "discount_percent": null,
      "discount_basis": null,
      "currency": "GBP",
      "selling_fast": true,
      "restocking_soon": false,
      "is_new": false,
      "sponsored": false,
      "color_product_ids": [211665399, 211665528, 211665657],
      "video": null
    }
  ],
  "count": 24,
  "total": 9966,
  "max_reachable": 2088,
  "page": 1,
  "page_size": 24,
  "has_more": true,
  "sort": "relevance",
  "sorts_offered": ["relevance", "newest", "price_asc", "price_desc"],
  "filters": {},
  "facets": [
    {"id": "brand", "name": "Brand", "values": [{"id": "53", "name": "ASOS DESIGN", "count": 1629}, {"id": "401", "name": "Levi's", "count": 404}]},
    {"id": "base_colour", "name": "Colour", "values": [{"id": "3", "name": "Blue", "count": 3940}, {"id": "4", "name": "Black", "count": 2099}]}
  ],
  "price_range": {"min": 3.99, "max": 290},
  "country": "gb",
  "currency": "GBP",
  "store": "gb",
  "language": "en-GB",
  "notes": ["ASOS serves keyword search results only up to position 2088 whatever total says (max_reachable); narrow with filters or use category for the rest."]
}
```

`total` was 9,966 and `max_reachable` 2,088: the first 2,088 results are reachable by paging. In the same answer, `210309625` (the Mango jean above) was 20.99 GBP with `previous_price` 35.99, and `206426641` was 7.49 GBP down 75% from 30.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/asos/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "dre", "country": "us"}'
```

Captured `data` (us, 2026-11-16; 3 of 10 shown):

```json
{
  "query": "dre",
  "suggestions": [{"text": "dresses", "count": 15818}, {"text": "sequin dress", "count": 856}, {"text": "long sleeve maxi dress", "count": 1409}],
  "count": 10,
  "country": "us",
  "currency": "USD",
  "store": "us",
  "language": "en-US",
  "notes": ["count is ASOS's number of results for the suggestion on this store."]
}
```

### Deals

```bash
curl -X POST https://api.scavio.dev/api/v1/asos/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "us", "gender": "women", "page_size": 24}'
```

Captured `data` (us women, 2026-11-16; 1 of 24 items shown, image links, `facets` and `notes` dropped):

```json
{
  "gender": "women",
  "category_id": 7046,
  "category_name": "Sale",
  "items": [
    {
      "product_id": 209960761,
      "product_type": "product",
      "group_id": null,
      "title": "adidas Originals Classic Firebird track top in blue and maroon",
      "brand": "adidas Originals",
      "color": "MID BLUE",
      "url": "https://www.asos.com/us/adidas-originals/adidas-originals-classic-firebird-track-top-in-blue-and-maroon/prd/209960761",
      "price": 64,
      "previous_price": 80,
      "rrp": null,
      "lowest_price_30d": 64,
      "is_marked_down": true,
      "is_outlet": false,
      "discount_percent": 20,
      "discount_basis": "previous_price",
      "currency": "USD",
      "selling_fast": false,
      "restocking_soon": false,
      "is_new": false,
      "sponsored": false,
      "color_product_ids": []
    }
  ],
  "count": 24,
  "total": 17759,
  "page": 1,
  "page_size": 24,
  "has_more": true,
  "sort": "relevance",
  "sorts_offered": ["relevance", "newest", "price_asc", "price_desc"],
  "filters": {},
  "price_range": {"min": 4.37, "max": 449.5},
  "marked_down": 24,
  "country": "us",
  "currency": "USD",
  "store": "us",
  "language": "en-US"
}
```

`marked_down` counts the items on the page with a `previous_price` (24 of 24 here).

### New arrivals, category, categories, brands, markets

Captured on 2026-11-16, 1 credit each:

- `/new-arrivals` with `{"gender": "women", "sort": "newest", "page_size": 24}` (gb): `category_id` 27108, `category_name` "New In", `total` 5033; first item `210607964` "Topshop Penelope rectangle clutch bag in gold" at 26 GBP. Items have the search item shape.
- `/category` with `{"category_id": "8799", "page_size": 24}` (gb): `category_name` "Dresses", `total` 18461, `price_range` 4 to 395 GBP. Category lists page past position 2,088.
- `/categories` with `{"gender": "women"}` (gb): one section (`gender` women, `name` "Women", `count` 291) whose nodes carry `name`, `category_id` (null on headings), `url`, `path` and `children`, e.g. "Dresses" `8799` at `Women > Categories > Clothing > SHOP by product > Dresses`. The same id can sit under several headings.
- `/brands` with `{"gender": "women"}` (gb): `title` "A-Z Women's Brands", `count` 506, each `{brand_id, name, url, letter}`, e.g. `{"brand_id": 27869, "name": "ASOS DESIGN", ...}`, `{"brand_id": 7083, "name": "Levi's", ...}`. Pass `brand_id` to `/category`; it is not the search `brand` filter id (`53` and `401` for the same two brands in search facets).
- `/markets` with `{"country": "jp"}`: `selected` `{"country": "jp", "store": "international", "language": "en-GB", "size_schema": "UK", "currencies": [{"currency": "USD", "symbol": "$", "primary": true}, {"currency": "GBP", "symbol": "£", "primary": false}]}`, `count` 237, `served` 235; Russia is listed with `served: false` and `held: "ASOS is not selling in this country"`.

### Python

```python
import time
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def asos(endpoint, body, timeout=120):
    r = requests.post(f"{BASE}/api/v1/asos/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()["data"]

IDS = ["205338218", "206956133"]  # product ids are the same in every ASOS store (up to 100 per call)
ROWS = [("gb", None), ("us", None), ("fr", None), ("de", None), ("au", None), ("ie", None), ("jp", None), ("ae", "GBP")]

captured_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
for country, currency in ROWS:  # 1 credit per call
    body = {"product_ids": IDS, "country": country}
    if currency:
        body["currency"] = currency
    d = asos("stock", body)
    for p in d["products"]:
        sale = f"was {p['previous_price']} (-{p['discount_percent']}%)" if p["is_marked_down"] and p["previous_price"] else ""
        sizes = sum(v["in_stock"] for v in p["variants"])
        print(captured_at, d["country"], d["store"], p["product_id"], p["price"], d["currency"], sale, f"{sizes} sizes in stock")
    for missing in d["not_found"]:
        print(d["country"], missing, "not sold in this store")

# Store each row with captured_at and run this on a schedule: that stored series is
# your price history (ASOS publishes none). Currencies differ: convert explicitly,
# with the rate and its date, before comparing stores.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live; nothing is cached. Prices are numbers in the request's currency, never converted. Every answer carries `country`, `currency`, `store` and `language`; `notes` appears when there is something to say.

- **Grid item** (search, category, deals, new arrivals) - `product_id`, `product_type` (`product`, `group` or `group_piece`), `group_id`, `title` (in the store's language), `brand`, `color`, `url`, `price`, `previous_price`, `rrp`, `lowest_price_30d`, `is_marked_down`, `is_outlet`, `discount_percent`, `discount_basis`, `currency`, `selling_fast`, `restocking_soon`, `is_new`, `sponsored`, `color_product_ids`, `image`, `images`, `video`.
- **search** - `query`, `items[]`, `count`, `total`, `max_reachable`, `page`, `page_size`, `has_more`, `sort`, `sorts_offered`, `filters`, `facets[]` {`id`, `name`, `values[]` {`id`, `name`, `count`}}, `price_range` {`min`, `max`}.
- **category / deals / new arrivals** - `category_id`, `category_name`, `items[]`, `count`, `total`, `page`, `page_size`, `has_more`, `sort`, `sorts_offered`, `filters`, `facets[]`, `price_range`. Deals adds `gender` and `marked_down`; new arrivals adds `gender`.
- **product** - `product_id`, `product_type`, `product_code`, `title`, `brand`, `brand_id`, `gender`, `product_kind`, `url`, `category` {`category_id`, `name`}, `breadcrumbs[]` {`name`, `category_id`, `url`}, `category_ids`, `description`, `product_details`, `brand_description`, `composition`, `care`, `size_and_fit`, `fit`, `country_of_manufacture`, `color`, `color_products[]` {`product_id`, `color`, `title`, `url`, `image`}, the price fields, `price_since`, `in_stock`, `selling_fast`, `is_discontinued`, `one_size`, `variants[]` {`variant_id`, `size`, `brand_size`, `size_id`, `color`, `sku`, `ean`, `price`, `previous_price`, `in_stock`, `low_stock`, `restocking_soon`, `seller`}, `rating` {`average`, `count`, `distribution`, `recommended_percent`, `fit`, `quality`}, `ai_summary` {`text`, `disclaimer`, `source`}, `images`, `video`. A co-ord set: `product_type` `group` and `items[]` (each piece's `product_id`, `product_code`, `title`, `brand`, `url`, prices, `in_stock`, `variants`, `rating`, `image`).
- **stock** - `products[]` {`product_id`, the price fields, `price_since`, `in_stock`, `restocking_soon`, `variants[]` {`variant_id`, `in_stock`, `low_stock`, `restocking_soon`, `price`, `previous_price`, `seller`}}, `count`, `not_found`.
- **reviews** - `product_id`, `summary` {`average`, `count`, `ratings_only_count`, `distribution`, `recommended_count`, `not_recommended_count`, `recommended_percent`, `fit` {`average`, `range`, `min_label`, `max_label`}, `quality`}, `ai_summary`, `reviews[]` {`id`, `rating`, `title`, `text`, `date`, `experience_date`, `ratings_only`, `recommended`, `fit` {`value`, `label`}, `quality`, `color`, `verified_purchaser`, `language`, `syndicated`, `source`, `photos`}, `count`, `total`, `page`, `page_size`, `has_more`, `sort`, `rating`.
- **suggestions** - `query`, `suggestions[]` {`text`, `count`}, `count`.
- **categories** - `sections[]` {`gender`, `name`, `url`, `categories[]` {`name`, `category_id`, `url`, `path`, `children`}, `count`}.
- **brands** - `gender`, `title`, `brands[]` {`brand_id`, `name`, `url`, `letter`}, `count`.
- **markets** - `selected` {`country`, `store`, `language`, `size_schema`, `currencies[]` {`currency`, `symbol`, `primary`}}, `countries[]` {`country`, `name`, `store`, `language`, `currencies`, `default_currency`, `size_schema`, `served`, `held`}, `count`, `served`.

## Guardrails

- Product ids and category ids are global: the same id in every ASOS store. Prices are per store and currency, not per country: never assume two countries on the same store and currency differ in price, and never assume the same currency on two stores is the same price.
- Quote the price of the store and currency the user asked about, with `store` and `currency`. A size can carry its own price (`variants[].price`).
- `previous_price` and `rrp` appear only above the price. Sales are per store: an item marked down on one store may not be on another, and never claim every store has a sale running.
- Stock is ONLINE stock in that store. ASOS has no physical stores: there is no store locator and no store stock, and never present ASOS stock as in-store availability.
- `/stock` returns variant ids, not size names: map them with the product answer's `variants`.
- Reviews are per store; quote the store with the counts. `ai_summary` is ASOS's own AI-generated summary: present it as such, with its disclaimer. Never invent reviewer names.
- Keyword search stops at position 2,088 (`max_reachable`); never claim to have read every result of a larger `total`.
- The search `brand` filter takes brand facet ids; `/brands` `brand_id` is a category id for `/category`. Do not mix them.
- Not available: an outlet (ASOS's outlet categories returned no items on 2026-11-16), promo codes (shown only to signed-in shoppers), a store locator, price history (poll and store), checkout and delivery prices.
- Terms: ASOS's UK terms (read 2026-11-16) say you're not allowed to use automated systems or software to extract data from its website, and that its content is for personal use unless ASOS gives express permission. This is not legal advice; read the current terms for your store and use case. Do not republish ASOS product photos, campaign images or logos; link product pages instead.
- Never fabricate prices, ids, sizes, stock or reviews. Only return what the API returned, with the country, store, currency and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` ASOS does not list, `uk` (use `gb`), `ru` or `by` (ASOS is not selling there), a `currency` ASOS does not offer the country (the error lists the allowed ones), `/suggestions` on `pl`, a search page that starts past position 2,088, more than 100 `product_ids`, not exactly one of `product_id`, `group_id` and `url` on product, a malformed id, an unknown filter name or facet id, more than 30 values for a filter, or `price_min` above `price_max`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "ASOS has no product ... on this store (unknown id, or not sold in this store).", "ASOS does not sell product ... on this store (no price here).", "ASOS has no category ... on this store ...", "ASOS has no reviews record for product ... on this store (unknown id).". On `/stock` an id the store does not sell is listed in `not_found` instead. Take ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=asos-api).
- `502` means ASOS data was temporarily unavailable ("ASOS is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means ASOS is busy ("ASOS is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.64.0
npm install scavio@0.65.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: stock } = await scavio.asos.stock({ product_ids: ["205338218", "206956133"], country: "fr" });
const { data: found } = await scavio.asos.search({ query: "jeans", country: "de", sort: "price_asc" });
const { data: item } = await scavio.asos.product({ product_id: "210309625" });
const { data: reviews } = await scavio.asos.reviews({ product_id: "210309625", sort: "newest" });
const { data: typed } = await scavio.asos.suggestions({ query: "dre", country: "us" });
const { data: dresses } = await scavio.asos.category({ category_id: "8799", country: "au" });
const { data: tree } = await scavio.asos.categories({ gender: "women" });
const { data: brands } = await scavio.asos.brands({ gender: "men" });
const { data: sale } = await scavio.asos.deals({ country: "us", gender: "women" });
const { data: fresh } = await scavio.asos.newArrivals({ gender: "men", sort: "newest" });
const { data: markets } = await scavio.asos.markets({ country: "jp" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.asos.search(...)`, `client.asos.product(...)`, `client.asos.stock(...)`, `client.asos.reviews(...)`, `client.asos.suggestions(...)`, `client.asos.category(...)`, `client.asos.categories(...)`, `client.asos.brands(...)`, `client.asos.deals(...)`, `client.asos.new_arrivals(...)` and `client.asos.markets(...)`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all eleven endpoints as tools: `search_asos`, `get_asos_product`, `get_asos_stock`, `get_asos_reviews`, `get_asos_suggestions`, `get_asos_category`, `get_asos_categories`, `get_asos_brands`, `get_asos_deals`, `get_asos_new_arrivals` and `get_asos_markets`. ASOS is opt-in: add `asos` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.63.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,asos"
      }
    }
  }
}
```
