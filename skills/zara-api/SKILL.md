---
name: zara-api
description: "Zara API for Zara prices by country: one Zara reference's price, old price on a markdown, discount and online stock by size in each Zara market, in that market's currency (never converted); references and the colour's product ids are the same on every market of Zara's international site, so one reference prices the item everywhere, and the prices endpoint takes one reference and up to 10 countries per call, listing the markets that do not sell it. Keyword search (or a reference lookup) sorted by price and filtered by colour, size, price range or section (woman, man, kids, home); one product in full by link, product id and slug, or reference, with description, composition, every colour with its own prices, Zara's promotions with start and end dates and each size's online availability (in stock, out of stock, low on stock, coming soon); online stock per size; units per size in up to 8 physical stores, split into sales floor and stockroom, by store ids or a point; Zara stores near a point with address, phone, 7 dated days of opening hours, sections and services; materials with composition, certified materials, care instructions and the country of production as Zara states it (traceability steps on France); the category tree and every product of a category with an exact total; the SPECIAL PRICES list (seasonal and per market) and NEW ARRIVALS list of a section; search suggestions in the market's language with an English fallback. 102 storefronts in their own currencies and 205 market-languages across Europe, the Americas, the Middle East, Africa and Asia-Pacific, including the US, Canada, Mexico, Brazil, the UK, the EU markets, Switzerland, Turkey, the Gulf, India, Japan, South Korea, Australia and Zara's separate China site (its own product ids). 12 endpoints, 2 credits per call, 4 for deals, new arrivals, store stock by point and product by reference or after a redirect, 6 for both, prices 2 per market, China 1. No reviews (Zara shows none), no price history (poll and store), and not Pull&Bear, Massimo Dutti, Bershka, Stradivarius, Oysho, Zara Home or Lefties. Zara has no public product data API."
version: 1.0.0
tags: zara, zara-api, zara-product-data, zara-product-api, zara-prices, zara-prices-by-country, zara-price-api, zara-sale, zara-sale-tracker, zara-special-prices, zara-stock, zara-stock-by-size, zara-store-stock, zara-stores, zara-new-arrivals, zara-new-in, zara-black-friday, zara-reference-lookup, zara-country-of-production, inditex, fashion, fashion-prices, clothing-prices, apparel, fast-fashion, retail, price-comparison, price-monitoring, price-tracker, multi-country, regional-pricing, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/docs/zara-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=zara-api
---

# Zara API - Prices by Country, Stock by Size, Stores, Product Data

Read Zara's own online stores (zara.com in 102 storefronts, and zara.cn for China): keyword search, one product in full, one reference priced across countries, online stock per size, units per size in physical stores, Zara stores with opening hours, materials and country of production, the category tree and category lists, special prices, new arrivals and search suggestions. All 12 endpoints return structured JSON. Most calls cost 2 credits; a few cost 4 or 6 (see Endpoints); China (`cn`) costs 1 credit per call.

**The job this skill is for: Zara prices by country.** One Zara reference's price, sale price and stock by size in each Zara market, in that market's currency. **References are global on Zara's international site**: the reference printed on the product page (`display_reference`, e.g. `4591/381`) names the same item in every market. A colour's `product_id` is usually the same across markets but can differ, and China (`cn`) runs its own product ids: match across markets with the reference. `/prices` takes one reference and up to 10 countries per call.

Captured on 2026-11-16, reference `4591/381` (the 100% wool suit blazer) from the prices endpoint with its default 10 markets:

| `country` | `language` | `title` | `price` | `old_price` | `currency` | `product_id` |
|---|---|---|---|---|---|---|
| `us` | `en` | 100% WOOL SUIT BLAZER | 179 | null | USD | 553306790 |
| `gb` | `en` | 100% WOOL SUIT BLAZER | 119 | null | GBP | 553306790 |
| `es` | `es` | BLAZER TRAJE 100% LANA | 99.95 | null | EUR | 553306790 |
| `de` | `de` | ANZUGBLAZER AUS 100% WOLLE | 119 | null | EUR | 553306790 |
| `fr` | `fr` | VESTE DE COSTUME 100 % LAINE | 119 | null | EUR | 553306790 |
| `it` | `it` | BLAZER DA COMPLETO 100% LANA | 119 | null | EUR | 553306790 |
| `jp` | `ja` | 100%ウールスーツブレザー | 22990 | null | JPY | 553306790 |
| `kr` | `ko` | 100% 울 수트 블레이저 | 209900 | null | KRW | 553306790 |
| `mx` | `es` | BLAZER TRAJE 100% LANA | 2799 | null | MXN | 553306790 |
| `pl` | `pl` | MARYNARKA OD GARNITURU ZE 100% WEŁNY | 429 | null | PLN | 553306790 |

The same `product_id` came back in all 10 markets; titles come back in each market's language and prices in its own currency, never converted. On that day the blazer was 99.95 EUR on `es` and 119 EUR on `de`, `fr` and `it`. To compare countries, convert explicitly and state the rate and its date.

**The price fields.** `price` is the current price. `old_price` is set only on a markdown and is above `price`; `discount_percent` is Zara's markdown figure. On a product, each colour carries its own prices and Zara's `promotions` for that colour with their `start` and `end`. In `/prices`, a market's `price` is the lowest current price among the reference's colours, and each colour is listed in `colors`. Zero-decimal currencies come back as whole numbers (22990 JPY, 209900 KRW in the table).

**Price history.** Zara shows none and none is returned. To build one, call `/prices` (or product) on a schedule and store each reading with its time, country and currency. Zara runs seasonal sales, and between sales its "SPECIAL PRICES" categories carry markdowns (`/deals`). Black Friday 2026 is November 27; Zara had announced no Black Friday dates in anything captured as of 2026-11-16.

Zara has no public product data API. Neither Zara nor Inditex publishes developer documentation for catalog, price or stock data.

See also: for H&M prices by country use `hm-api`; for second-hand Zara items on Vinted use `vinted-api`; for Nordstrom fashion prices, markdowns and per-size stock use `nordstrom-product-data`; for the cross-merchant view of one product use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Compare one Zara item's price across countries, each in its own currency (one reference, up to 10 countries per call)
- Check whether a Zara item is marked down in a market: its price, old price and discount, and the promotion dates on a colour
- Track Zara prices over time (Black Friday, the winter and summer sales) by polling and storing prices
- Check which sizes of a Zara item are in stock online in a market (in stock, out of stock, low on stock, coming soon)
- Check how many units of each size a Zara store has, split into sales floor and stockroom
- Find Zara stores near a point with address, phone, 7 dated days of opening hours, sections and services
- Search Zara's catalog by keyword in a market, sorted by price, filtered by colour, size or a price range; or look up a reference
- Read one Zara product in full: description, composition, every colour with its own prices, promotions and sizes
- Find what a Zara item is made of, its care instructions and where it is made
- Browse Zara's category tree, one category's full list, the special prices or the new arrivals of a section
- Get Zara's search suggestions for what a shopper has typed

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=zara-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=zara-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits: 25 calls at 2 credits, or a `/prices` call across 10 markets (20 credits) and 15 more 2-credit calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures most calls took 1.6 to 6.6 seconds; new arrivals and store stock by point can take 10 to 15 seconds, and large category lists longer. Set a client timeout of at least 180 seconds and do not fire many calls at once (a busy moment answers `503` with `Retry-After`).

| Endpoint | Markets | Credits | What it returns |
|---|---|---|---|
| `POST /api/v1/zara/search` | all 102 | 2 | Items for a keyword (or every colour of a reference), with prices, colours, online availability, colour and size facets, totals |
| `POST /api/v1/zara/product` | all 102 | 2; 4 by `reference` or when Zara redirects the slug; 6 for both | One product by `url`, `product_id` + `slug`, or `reference`: composition, every colour's prices, promotions and sizes with online availability |
| `POST /api/v1/zara/materials` | all 102 | 2 | Composition, sustainable materials, certifications, care and country of production of one product |
| `POST /api/v1/zara/stock` | all 102 | 2 | Online availability per size (sku) of one colour |
| `POST /api/v1/zara/stores` | 100 | 2 | Zara stores near a point, nearest first, with address, phone, opening hours, sections, services |
| `POST /api/v1/zara/store-stock` | 100 | 2 with `store_ids`; 4 with `lat` + `lng` | Units per size of one colour in up to 8 physical stores, sales floor vs stockroom |
| `POST /api/v1/zara/categories` | all 102 | 2 | The market's category tree with ids, parents, levels, leaves |
| `POST /api/v1/zara/category` | all 102 | 2 | Every product of one category, paged and sorted, with an exact total |
| `POST /api/v1/zara/deals` | all 102 | 4 (2 when the market has no special-prices category) | The market's SPECIAL PRICES list for a section |
| `POST /api/v1/zara/new-arrivals` | 101 | 4 | The market's NEW ARRIVALS > THE NEW list for a section |
| `POST /api/v1/zara/prices` | all 102 | 2 per market that answered | One reference in up to 10 markets: price, old price, discount, currency, title, availability; `not_sold` lists the markets that do not sell it |
| `POST /api/v1/zara/suggestions` | 92 | 2; 4 when the English fallback runs | Search suggestions for what a shopper has typed |

China (`cn`) costs 1 credit per call on every endpoint (deals and new arrivals are 1 in total there; prices 1 per `cn` market). Credits are what the call actually cost: a product opened by reference is a reference lookup plus the product page, store stock by point is a stores lookup plus store stock, deals and new arrivals read the live category tree plus the list.

## Markets

Every endpoint except `/prices` takes `country` (lowercase ISO-2, default `us`; `gb` for the United Kingdom) and, except stock, `language` (default: Zara's own default for the market, the first listed below). Titles, descriptions, colours and category names come back in that language and prices in the market's currency, never converted. Every answer echoes `country`; all but stock also echo `language`, and all but product (which carries `currency` with its prices) and stock echo `currency`. `/prices` echoes all three per market.

The 102 storefronts, by currency (languages in Zara's order; the first is the default):

| Currency | `country` (languages) |
|---|---|
| AED | `ae` (en, ar), `xe` (en) |
| ALL | `al` (sq, en) |
| AMD | `am` (ru, hy, en) |
| ARS | `ar` (es, en) |
| AUD | `au` (en) |
| AWG | `aw` (en, es) |
| AZN | `az` (ru, en) |
| BAM | `ba` (hr, en) |
| BHD | `bh` (en, ar) |
| BRL | `br` (pt, en) |
| CAD | `ca` (en, fr) |
| CHF | `ch` (en, fr, de, it) |
| CLP | `cl` (es, en) |
| CNY | `cn` (zh, en) |
| COP | `co` (es, en) |
| CRC | `cr` (es, en) |
| CZK | `cz` (cs, en) |
| DKK | `dk` (da, en) |
| DOP | `do` (es, en) |
| DZD | `dz` (ar, en, fr) |
| EGP | `eg` (ar, en) |
| EUR | `ad` (ca, en, fr, es), `ao` (pt, en), `at` (de, en), `be` (en, nl, fr), `bg` (bg, en), `cy` (el, en), `de` (de, en), `ee` (et, en), `es` (es, en, eu, gl, ca), `fi` (fi, sv, en), `fr` (fr, en), `gr` (el, en), `hr` (hr, en), `ic` (es, en), `ie` (en), `it` (it, en), `lt` (lt, en), `lu` (fr, en, de), `lv` (lv, en), `mc` (fr, en), `me` (sr, en), `mt` (en), `nl` (en, nl), `pt` (pt, en), `si` (sl, en), `sk` (sk, en), `xk` (sq, en) |
| GBP | `gb` (en) |
| GEL | `ge` (en, ka) |
| GTQ | `gt` (es, en) |
| HKD | `hk` (en, zh-Hant) |
| HNL | `hn` (es, en) |
| HUF | `hu` (hu, en) |
| IDR | `id` (id, en) |
| ILS | `il` (he, en) |
| INR | `in` (en) |
| IQD | `iq` (en) |
| ISK | `is` (en) |
| JOD | `jo` (en, ar) |
| JPY | `jp` (ja, en) |
| KHR | `kh` (en) |
| KRW | `kr` (ko, en) |
| KWD | `kw` (en, ar) |
| KZT | `kz` (ru, kk, en) |
| LBP | `lb` (en, ar) |
| MAD | `ma` (fr, en) |
| MKD | `mk` (mk, sq, en) |
| MOP | `mo` (zh-Hant, en) |
| MXN | `mx` (es, en) |
| MYR | `my` (en) |
| NIO | `ni` (es, en) |
| NOK | `no` (no, en) |
| NZD | `nz` (en) |
| OMR | `om` (en, ar) |
| PAB | `pa` (es, en) |
| PEN | `pe` (es, en) |
| PHP | `ph` (en) |
| PLN | `pl` (pl, uk, en) |
| PYG | `py` (es, en) |
| QAR | `qa` (en, ar) |
| RON | `ro` (ro, en) |
| RSD | `rs` (sr, en) |
| SAR | `sa` (en) |
| SEK | `se` (sv, en) |
| SGD | `sg` (en) |
| THB | `th` (th, en) |
| TND | `tn` (fr, ar, en) |
| TRY | `tr` (tr, en) |
| TWD | `tw` (zh-Hant, en) |
| UAH | `ua` (uk, en) |
| USD | `ec` (es, en), `pr` (es, en), `sv` (es, en), `us` (en, es), `ve` (es, en) |
| UYU | `uy` (es, en) |
| UZS | `uz` (uz, en, ru) |
| VND | `vn` (vi, en) |
| XCG | `cw` (en) |
| ZAR | `za` (en) |

- 205 market-languages in all. `ic` is the Canary Islands, `xe` Abu Dhabi, Al Ain and Ras Al Khaimah, `xk` Kosovo. `cn` is Zara's separate China site.
- Search, product, materials, stock, categories, category, deals and prices: all 102. Stores and store-stock: 100 (not `ao` or `iq`: Zara lists no stores there). New arrivals: 101 (not `dz`: Zara shows no new-arrivals category there). Suggestions: 92 (not `ad`, `al`, `am`, `az`, `ba`, `dz`, `mk`, `mo`, `uz` or `xk`; use search there).
- Held back, answering `400` before anything is charged: `uk` (use `gb`); `by` (Zara is not selling online in Belarus); the 115 countries Zara serves only from its worldwide store (the Spain catalogue in euros); any country with no Zara online store; and five market-languages whose Zara catalogue returns most titles in another language: Arabic on `iq`, `xe`, `ma` and `sa`, and Spanish on `cw` (use the market's other language).
- Category ids are shared across Zara's northern-hemisphere catalogue; `au`, `za` and `br` run their own catalogue and ids (take ids from `/categories` on that market).
- Assortments differ by market: a reference sold in one market can be missing in another (`/prices` lists it in `not_sold`; product answers `404`).

## Workflow

1. **One item, every country:** take the reference (`display_reference` of any answer, or the `4591/381` printed on the product page). Call `/prices` with `reference` and up to 10 `countries` (2 credits per market that answered; split longer lists into several calls). Each market gives `price`, `old_price`, `discount_percent`, `currency`, `title`, `available` and the market's own product `url`; `not_sold` lists the markets that do not sell it. Store each reading with its time.
2. **Is it marked down:** `old_price` is set (with `discount_percent`). `/product` adds each colour's `promotions` with start and end dates. Not every market has a markdown at the same time.
3. **Sizes in stock online:** `/stock` with the colour's `product_id` (2 credits) returns availability per `sku`; match each `sku` to `colors[].sizes[].sku` of the product answer for the size name. `/product` returns the same availability with size names for every colour.
4. **Units in a store:** `/stores` with `lat` + `lng` lists stores nearest first; pass up to 8 `store_id` values to `/store-stock` with the `product_id` (2 credits). Or send `/store-stock` a `lat` + `lng` directly: the 8 nearest stores, with their address (4 credits).
5. **Browse:** `/categories` for the tree, then `/category` with a `leaf: true` id (or a parent's `redirect_id`). `/deals` and `/new-arrivals` find the section's list in the live tree on every call. `/search` with `query`; read `facets` from the first answer, then filter with those exact `value`s in the same market and language.
6. **Materials and origin:** `/materials` with the `product_id`: composition, certifications, care and the country of production in the market's language.
7. **Price tracking:** poll `/prices` (or product) on a schedule and store each reading. There is no price history endpoint.

## Parameters

### Shared

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `us` | See Markets (not on prices, which takes `countries`) |
| `language` | string | the market's first | One of the market's languages (`zh-Hant` for Traditional Chinese on `hk`, `mo`, `tw`); not on stock |
| `page` | integer | 1 | 1 to 100 (search, category, deals, new arrivals) |
| `page_size` | integer | 24 | 1 to 96 |
| `sort` | string | `relevance` | `relevance` (Zara's own order), `price_asc` or `price_desc` (search, category, deals, new arrivals). Not on `cn` search |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Keywords, 1-200 chars, any language |
| `reference` | string | one of | A reference (`4591/381`, or `4591/381/800` for one colour): answers every colour of it with `sold_here`; takes no other filter |
| `section` | string | every section | `woman`, `man`, `kids` or `home` |
| `color` | string | none | One value of the `color` facet of an earlier answer in the same market (`black`) |
| `size` | string | none | One value of the `size` facet of an earlier answer (`38`) |
| `price_min` / `price_max` | number | none | Price range in the market's currency |

For some queries Zara answers in its own order and offers no price sort: `sorts_offered` is then empty and a note says the items are in Zara's order.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | A Zara product link from any market (`https://www.zara.com/<country>/<language>/<slug>-p<8 digits>.html?v1=<product id>`); its market is used unless `country` is sent |
| `product_id` + `slug` | string | one of | The colour's `product_id` with its `seo_slug` from a search answer. A product id alone cannot open a Zara product page. A slug of another market or language still works (Zara redirects, 4 credits) |
| `reference` | string | one of | A reference: a reference lookup, then the product page (4 credits) |

### Materials (`/materials`), stock (`/stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | The colour's product id (`588478514`) |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `lat` / `lng` | number | required | A point in the country (40.7128, -74.0060 New York; 51.5072, -0.1276 London; 35.6762, 139.6503 Tokyo) |

### Store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | The colour's product id |
| `store_ids` | array | one of | Up to 8 `store_id` values from `/stores` (2 credits) |
| `lat` / `lng` | number | one of | A point: the 8 nearest stores are checked (4 credits) |

### Categories (`/categories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `section` | string | whole tree | `woman`, `man`, `kids`, `home` or `beauty` |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | required | A `leaf: true` id from `/categories` (`2420896`, women's dresses on `us`), or a parent's `redirect_id` |
| `on_sale` | boolean | false | Only marked-down items (with `old_price`) |

### Deals (`/deals`) and new arrivals (`/new-arrivals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `section` | string | `woman` | `woman`, `man`, `girl` or `boy` |

### Prices (`/prices`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `reference` | string | required | A reference (`4591/381`; `4591/381/800` for one colour) |
| `countries` | array | `us`, `gb`, `es`, `de`, `fr`, `it`, `jp`, `kr`, `mx`, `pl` | 1 to 10 markets |
| `language` | string | each market's default | Used for the titles where the market serves it, else that market's default |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far, 1-100 chars |
| `section` | string | every section | `woman`, `man`, `kids` or `home` |

Where Zara has no suggestions in the request language, the market's English suggestions are answered (`language_used: "en"`, a note, 4 credits).

## Examples

### Prices

```bash
curl -X POST https://api.scavio.dev/api/v1/zara/prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"reference": "4591/381"}'
```

Captured `data` (2026-11-16, the default 10 markets, 20 credits; 2 of 10 markets shown, the rest are in the table above):

```json
{
  "reference": "4591/381",
  "markets": [
    {
      "country": "us",
      "language": "en",
      "currency": "USD",
      "available": true,
      "title": "100% WOOL SUIT BLAZER",
      "price": 179,
      "old_price": null,
      "discount_percent": null,
      "product_id": "553306790",
      "url": "https://www.zara.com/us/en/100-wool-suit-blazer-p04591381.html?v1=553306790",
      "colors": [
        {
          "product_id": "553306790",
          "color_id": "800",
          "name": "Black",
          "price": 179,
          "old_price": null,
          "discount_percent": null,
          "availability": "in_stock"
        }
      ]
    },
    {
      "country": "gb",
      "language": "en",
      "currency": "GBP",
      "available": true,
      "title": "100% WOOL SUIT BLAZER",
      "price": 119,
      "old_price": null,
      "discount_percent": null,
      "product_id": "553306790",
      "url": "https://www.zara.com/uk/en/100-wool-suit-blazer-p04591381.html?v1=553306790",
      "colors": [
        {
          "product_id": "553306790",
          "color_id": "800",
          "name": "Black",
          "price": 119,
          "old_price": null,
          "discount_percent": null,
          "availability": "in_stock"
        }
      ]
    }
  ],
  "not_sold": [],
  "errors": [],
  "count": 10,
  "notes": ["One reference lookup per market: price is that market's lowest current price among the reference's colours (each colour is in colors), in its own currency, never converted.", "2 credits per market that answered (1 on cn); a market that failed is listed in errors and not charged."]
}
```

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/zara/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "blazer"}'
```

Captured `data` (US, 2026-11-16; 1 of 24 items, 2 of 8 colours, 2 of 16 colour values and 1 of 3 notes shown; image links dropped):

```json
{
  "query": "blazer",
  "items": [
    {
      "product_id": "565424841",
      "reference": "04456999-I2026",
      "display_reference": "4456/999",
      "title": "COMFORT SUIT BLAZER",
      "url": "https://www.zara.com/us/en/comfort-suit-blazer-p04456999.html?v1=565424841",
      "seo_slug": "comfort-suit-blazer-p04456999",
      "section": "man",
      "family": "BLAZER",
      "subfamily": "Tailoring Blaz.",
      "price": 77.4,
      "old_price": 129,
      "discount_percent": 40,
      "currency": "USD",
      "availability": "in_stock",
      "colors": [
        {
          "product_id": "565424841",
          "color_id": "707",
          "name": "taupe brown",
          "price": 77.4,
          "old_price": 129,
          "discount_percent": 40,
          "availability": "in_stock",
          "tags": []
        },
        {
          "product_id": "583773005",
          "color_id": "081",
          "name": "Sand / Marl",
          "price": 77.4,
          "old_price": 129,
          "discount_percent": 40,
          "availability": "in_stock",
          "tags": []
        }
      ],
      "additional_colors": 7,
      "tags": []
    }
  ],
  "count": 24,
  "total": 829,
  "page": 1,
  "page_size": 24,
  "has_more": true,
  "sort": "relevance",
  "sorts_offered": ["price_asc", "price_desc"],
  "section": null,
  "filters": {},
  "facets": [
    {
      "filter": "color",
      "values": [{"value": "beige", "label": "Beige", "count": 52, "hex": "#E6D4AB"}, {"value": "black", "label": "Black", "count": 149, "hex": "#251F1F"}]
    }
  ],
  "price_range": {"min": 29.94, "max": 3200},
  "country": "us",
  "language": "en",
  "currency": "USD",
  "notes": ["product_id is the colour's product id; it is usually the same in every market on Zara's international site but can differ (cn runs its own ids), so match across markets with the reference; display_reference is the reference printed on the product page (pass it to prices or product reference)."]
}
```

`colors[].tags` carries Zara's labels such as `new` and `few_items_left`. Pass `display_reference` (not `reference`, Zara's internal code) to prices or product.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/zara/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "588478514", "slug": "trf-low-rise-wide-leg-jeans-p08727223"}'
```

Captured `data` (US, 2026-11-16; 1 of 8 colours, 2 of 8 sizes and 1 of 4 notes shown; image links dropped):

```json
{
  "product_id": "588478514",
  "reference": "08727223-I2026",
  "display_reference": "8727/223",
  "title": "TRF DISTRESSED LOW-RISE WIDE-LEG JEANS",
  "description": "LOW RISE - WIDE LEG - FULL LENGTH. Low-rise, five-pocket jeans. Full-length wide legs. Featuring distressed detailing. Front zip fly and metal button closure.",
  "url": "https://www.zara.com/us/en/trf-low-rise-wide-leg-jeans-p08727223.html?v1=588478514",
  "seo_slug": "trf-low-rise-wide-leg-jeans-p08727223",
  "section": "woman",
  "family": "TROUSERS",
  "subfamily": "T.FOLDER PANTS",
  "first_visible_date": "2026-08-30T00:00:00Z",
  "price": 35.94,
  "old_price": 59.9,
  "discount_percent": 40,
  "currency": "USD",
  "composition": [{"part": "OUTER SHELL", "components": [{"material": "cotton", "percent": 100}], "areas": []}],
  "colors": [
    {
      "color_id": "406",
      "name": "Light blue",
      "hex": "#D3D6CB",
      "product_id": "588478514",
      "reference": "C08727223406015-I2026",
      "price": 35.94,
      "old_price": 59.9,
      "discount_percent": 40,
      "currency": "USD",
      "promotions": [{"name": "ECOMLOAD_SEASON_PROMO_PROMO_BASIC_Y_TRF_86961_ZARA_US", "start": "2026-09-15T08:00:00Z", "end": "2027-07-11T23:00:00Z"}],
      "sizes": [
        {"size_id": "32", "name": "25 (US 0)", "sku": "545408228", "availability": "in_stock", "demand": "regular"},
        {"size_id": "34", "name": "26 (US 2)", "sku": "545408229", "availability": "in_stock", "demand": "regular"}
      ],
      "tags": [],
      "store_stock_available": true,
      "url": "https://www.zara.com/us/en/trf-low-rise-wide-leg-jeans-p08727223.html?v1=588478514"
    }
  ],
  "color_count": 8,
  "requested_product_id": "588478514",
  "country": "us",
  "language": "en",
  "notes": ["colors[].sizes[].availability is online stock (not store stock), as Zara states it: in_stock, out_of_stock, low_on_stock or coming_soon. demand is Zara's own demand flag for the size."]
}
```

Prices are per colour: in this capture the light blue colour was marked down to 35.94 from 59.9 while the navy blue colour was 59.9 with no markdown.

### Materials

```bash
curl -X POST https://api.scavio.dev/api/v1/zara/materials \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "588478514"}'
```

Captured `data` (US, 2026-11-16; `certifications`, `care.notes`, `care.icons`, `sections` and `notes` dropped):

```json
{
  "product_id": "588478514",
  "title": "COMPOSITION & CARE",
  "composition": [{"part": "OUTER SHELL", "components": [{"material": "cotton", "percent": 100}]}],
  "sustainable_materials": {
    "note": "Which has at least:",
    "parts": [
      {
        "part": "OUTER SHELL",
        "components": [
          {"material": "RCS-certified recycled cotton", "percent": 25},
          {"material": "REGENAGRI® certified cotton from regenerative practices", "percent": 60}
        ]
      }
    ]
  },
  "care": {
    "instructions": ["Machine wash max. 30ºC/86ºF delicate cycle", "Do not use bleach / whitener", "Iron maximum 110ºC/230ºF", "Tetrachloroethylene Dry Clean", "Low temperature dryer may be used"]
  },
  "origin": ["Made in Bangladesh"],
  "traceability": [],
  "country": "us",
  "language": "en",
  "currency": "USD"
}
```

The two certifications were "RCS CERTIFIED RECYCLED COTTON" and "REGENAGRI® CERTIFIED COTTON FROM REGENERATIVE PRACTICES", each with Zara's description. `origin` is the country of production as Zara states it, in the market's language; on `fr` Zara shows `traceability` steps (each step and its country) instead. Zara names no factories.

### Stock

```bash
curl -X POST https://api.scavio.dev/api/v1/zara/stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "588478514"}'
```

Captured `data` (US, 2026-11-16; notes dropped):

```json
{
  "product_id": "588478514",
  "skus": [
    {"sku": "545408230", "availability": "in_stock"},
    {"sku": "545408231", "availability": "in_stock"},
    {"sku": "545408228", "availability": "in_stock"},
    {"sku": "545408229", "availability": "in_stock"},
    {"sku": "545408234", "availability": "in_stock"},
    {"sku": "545408235", "availability": "out_of_stock"},
    {"sku": "545408232", "availability": "in_stock"},
    {"sku": "545408233", "availability": "in_stock"}
  ],
  "sizes_total": 8,
  "sizes_in_stock": 7,
  "country": "us"
}
```

Zara's stock answer has no size names. In the product capture of the same colour, sku `545408235` is size `32 (US 14)`: the one size out of stock online.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/zara/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"lat": 40.7128, "lng": -74.006}'
```

Captured `data` (US, New York, 2026-11-16; 1 of 17 stores, 2 of 7 days, 1 of 2 notes shown):

```json
{
  "stores": [
    {
      "store_id": "3904",
      "kind": "Zara",
      "type": "street",
      "address_lines": ["222, BROADWAY"],
      "city": "NEW YORK",
      "state": "NEW YORK",
      "state_code": "USNY",
      "postal_code": "10038",
      "country": "Estados Unidos",
      "country_code": "us",
      "lat": 40.7112633,
      "lng": -74.008867,
      "distance_km": 0.3,
      "phones": ["8332472473"],
      "opening_hours": [
        {"date": "2026-11-15", "weekday": 7, "open": "11:00", "close": "20:00"},
        {"date": "2026-11-16", "weekday": 1, "open": "10:00", "close": "21:00"}
      ],
      "sections": ["woman", "man", "kids"],
      "services": ["clickandgo_checkout_cart"],
      "pickup": true,
      "online_store": true,
      "status": "open",
      "timezone": "US/Eastern"
    }
  ],
  "count": 17,
  "total": 17,
  "lat": 40.7128,
  "lng": -74.006,
  "country": "us",
  "language": "en",
  "currency": "USD",
  "notes": ["Zara's store locator around the point (nearest first, distance_km from it). Pass store_id values as store-stock store_ids."]
}
```

`country` is Zara's own country name for the store (it came back in Spanish here); use `country_code`. Zara gives stores no name field.

### Store stock

```bash
curl -X POST https://api.scavio.dev/api/v1/zara/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "553306790", "store_ids": ["3904", "3862", "3037", "10815", "3074", "11818", "3818", "18957"]}'
```

Captured `data` (US, 2026-11-16; 1 of 3 stores with stock, 2 of 5 sizes shown; notes dropped):

```json
{
  "product_id": "553306790",
  "stores": [
    {
      "store_id": "3904",
      "sizes": [
        {"size_id": "46", "size": "36 (US 36)", "units": 1, "on_sale": false, "sales_floor_units": 0, "stockroom_units": 1},
        {"size_id": "48", "size": "38 (US 38)", "units": 3, "on_sale": false, "sales_floor_units": 0, "stockroom_units": 3}
      ],
      "units_total": 8,
      "locations": [],
      "store": null
    }
  ],
  "stores_checked": ["3904", "3862", "3037", "10815", "3074", "11818", "3818", "18957"],
  "stores_with_stock": 3,
  "stores_without_stock": ["3862", "10815", "3074", "3818", "18957"],
  "country": "us",
  "language": "en",
  "currency": "USD"
}
```

`locations` is where the item sits in the store (`area`, `floor`, `section`, `zone`) when Zara shows it. `store` carries the store's address when the call was made by `lat` + `lng`, and is `null` with `store_ids`.

### Categories and category

```bash
curl -X POST https://api.scavio.dev/api/v1/zara/categories \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"section": "woman"}'
```

Captured `data` (US women, 2026-11-16; 4 of 253 categories shown, 1 of 2 notes):

```json
{
  "categories": [
    {"id": "1881757", "name": "WOMAN", "section": "woman", "parent_id": null, "level": 1, "leaf": false, "redirect_id": null, "key": "I2024-MUJER"},
    {
      "id": "2420895",
      "name": "DRESSES",
      "section": "woman",
      "parent_id": "2643249",
      "level": 3,
      "leaf": false,
      "redirect_id": "2420896",
      "key": "I2024-MUJER-VESTIDOS"
    },
    {
      "id": "2420896",
      "name": "VIEW ALL",
      "section": "woman",
      "parent_id": "2420895",
      "level": 4,
      "leaf": true,
      "redirect_id": null,
      "key": "I2024-MUJER-VESTIDOS-VER_TODO"
    },
    {
      "id": "2419724",
      "name": "SPECIAL PRICES",
      "section": "woman",
      "parent_id": "2643249",
      "level": 3,
      "leaf": false,
      "redirect_id": "2419737",
      "key": "I2024-MUJER-SPECIAL_PRICES_GENERAL"
    }
  ],
  "count": 253,
  "section": "woman",
  "country": "us",
  "language": "en",
  "currency": "USD",
  "notes": ["Category ids are shared across Zara's northern-hemisphere markets; au, za and br run their own catalogue and ids."]
}
```

The "DRESSES" parent (`2420895`) points to its view-all list `2420896`. Captured on `/category` with `{"category_id": "2420896"}` (US, 2026-11-16): `total` 784, `total_pages` 33, `on_sale_count` 10, first item `0253/701` "ZW COLLECTION COMBINED KNIT DRESS" at 229 USD. Items have the search item shape. Zara's category answer carries no category name: names are in `/categories`.

### Deals

```bash
curl -X POST https://api.scavio.dev/api/v1/zara/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"section": "woman"}'
```

Captured `data` (US women, 2026-11-16, 4 credits; 1 of 24 items shown, image link, `sorts_offered` and `notes` dropped):

```json
{
  "section": "woman",
  "category_id": "2419737",
  "category_name": "SPECIAL PRICES",
  "items": [
    {
      "product_id": "552293226",
      "reference": "04387268-I2026",
      "display_reference": "4387/268",
      "title": "POLKA DOT RUFFLE BLOUSE",
      "url": "https://www.zara.com/us/en/polka-dot-ruffle-blouse-p04387268.html?v1=552293226",
      "seo_slug": "polka-dot-ruffle-blouse-p04387268",
      "section": "woman",
      "family": "CAMISA",
      "subfamily": "B.CAMISA",
      "price": 29.94,
      "old_price": 49.9,
      "discount_percent": 40,
      "currency": "USD",
      "availability": "in_stock",
      "colors": [
        {
          "product_id": "552293226",
          "color_id": "068",
          "name": "Ecru / Maroon",
          "price": 29.94,
          "old_price": 49.9,
          "discount_percent": 40,
          "availability": "in_stock",
          "tags": []
        }
      ],
      "additional_colors": 1,
      "tags": []
    }
  ],
  "count": 24,
  "total": 192,
  "page": 1,
  "page_size": 24,
  "total_pages": 8,
  "has_more": true,
  "sort": "relevance",
  "on_sale_count": 192,
  "marked_down": 192,
  "country": "us",
  "language": "en",
  "currency": "USD"
}
```

Zara's SPECIAL PRICES categories are seasonal and per market. A market can show no special-prices category for a section at a given time (on 2026-11-16, `mx` and `cy` for woman): those answer 200 with no items and a note (2 credits), not an error. On `fr`, `be`, `lu`, `mc` and `iq` Zara lists special prices without a previous price, so `old_price` is `null` there.

### New arrivals

```bash
curl -X POST https://api.scavio.dev/api/v1/zara/new-arrivals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "gb", "section": "woman"}'
```

Captured on `gb` (women, 2026-11-16, 4 credits): `category_id` `2546081`, `category_name` "THE NEW", `total` 639, `total_pages` 27, first item `7191/853` "ZW COLLECTION WOOL BLEND PEPLUM BLAZER" at 119 GBP. Items have the search item shape.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/zara/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "jea"}'
```

Captured `data` (US, 2026-11-16; 3 of 10 shown):

```json
{
  "query": "jea",
  "section": null,
  "suggestions": [{"text": "jeans"}, {"text": "barrel jeans"}, {"text": "baggy jeans"}],
  "count": 10,
  "language_used": "en",
  "country": "us",
  "language": "en",
  "currency": "USD"
}
```

### Python

```python
import time
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def zara(endpoint, body, timeout=180):
    r = requests.post(f"{BASE}/api/v1/zara/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()["data"]

REFERENCE = "4591/381"  # references are the same in every market
MARKETS = ["us", "gb", "es", "de", "fr", "it", "jp", "kr", "mx", "pl"]  # up to 10 per call

captured_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
d = zara("prices", {"reference": REFERENCE, "countries": MARKETS})  # 2 credits per market
for m in d["markets"]:
    if not m["available"]:
        print(m["country"], "not sold")
        continue
    sale = f"was {m['old_price']} (-{m['discount_percent']}%)" if m["old_price"] else ""
    print(captured_at, m["country"], m["price"], m["currency"], sale)
for e in d["errors"]:
    print(e["country"], "no answer (not charged)")

# Store each row with captured_at and run this on a schedule: that stored series is
# your price history (Zara publishes none). Currencies differ: convert explicitly,
# with the rate and its date, before comparing countries.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live; nothing is cached. Prices are numbers in the market's currency, never converted. `notes` appears when there is something to say.

- **Grid item** (search, category, deals, new arrivals) - `product_id` (the colour's id), `reference` (Zara's internal code), `display_reference` (the printed reference), `title` (in the request language), `url`, `seo_slug`, `section`, `family`, `subfamily`, `price`, `old_price`, `discount_percent`, `currency`, `availability`, `colors[]` {`product_id`, `color_id`, `name`, `price`, `old_price`, `discount_percent`, `availability`, `tags`}, `additional_colors`, `tags`, `image`.
- **search** - `query`, `items[]`, `count`, `total`, `page`, `page_size`, `has_more`, `sort`, `sorts_offered`, `section`, `filters`, `facets[]` {`filter` (`color` or `size`), `values[]` {`value`, `label`, `count`, `hex` on colours}}, `price_range` {`min`, `max`}. By reference: `reference`, `items[]`, `count`, `total`, `sold_here`.
- **category / deals / new arrivals** - `items[]`, `count`, `total` (exact), `page`, `page_size`, `total_pages`, `has_more`, `sort`, `sorts_offered`, `on_sale_count`. Category adds `category_id`, `on_sale`; deals adds `section`, `category_id`, `category_name`, `marked_down`; new arrivals adds `section`, `category_id`, `category_name`.
- **product** - `product_id`, `requested_product_id`, `reference`, `display_reference`, `title`, `description`, `url`, `seo_slug`, `section`, `family`, `subfamily`, `first_visible_date`, `price`, `old_price`, `discount_percent`, `currency`, `composition[]` {`part`, `components[]` {`material`, `percent`}, `areas`}, `colors[]` {`color_id`, `name`, `hex`, `product_id`, `reference`, the price fields, `currency`, `promotions[]` {`name`, `start`, `end`}, `sizes[]` {`size_id`, `name`, `sku`, `availability`, `demand`}, `tags`, `store_stock_available`, `images`, `url`}, `color_count`.
- **materials** - `product_id`, `title`, `composition[]`, `sustainable_materials` {`note`, `parts[]`}, `certifications[]` {`name`, `description`, `certified_by`, `lines`}, `care` {`notes`, `instructions`, `icons[]` {`code`, `text`, `icon`}}, `origin[]`, `traceability[]` {`step`, `country`}, `sections`.
- **stock** - `product_id`, `skus[]` {`sku`, `availability`}, `sizes_total`, `sizes_in_stock`.
- **stores** - `stores[]` {`store_id`, `kind`, `type`, `address_lines`, `city`, `state`, `state_code`, `postal_code`, `country`, `country_code`, `lat`, `lng`, `distance_km`, `phones`, `opening_hours[]` {`date`, `weekday`, `open`, `close`}, `sections`, `services`, `pickup`, `online_store`, `status`, `timezone`}, `count`, `total`, `lat`, `lng`.
- **store-stock** - `product_id`, `stores[]` {`store_id`, `sizes[]` {`size_id`, `size`, `units`, `on_sale`, `sales_floor_units`, `stockroom_units`}, `units_total`, `locations[]` {`area`, `floor`, `section`, `zone`}, `store` (address by point, else `null`)}, `stores_checked`, `stores_with_stock`, `stores_without_stock`.
- **categories** - `categories[]` {`id`, `name`, `section`, `parent_id`, `level`, `leaf`, `redirect_id`, `key`}, `count`, `section`.
- **prices** - `reference`, `markets[]` {`country`, `language`, `currency`, `available`, `title`, `price`, `old_price`, `discount_percent`, `product_id`, `url`, `colors[]` {`product_id`, `color_id`, `name`, `price`, `old_price`, `discount_percent`, `availability`}}, `not_sold`, `errors[]` {`country`, `error`}, `count`.
- **suggestions** - `query`, `section`, `suggestions[]` {`text`}, `count`, `language_used`.

## Guardrails

- References are global on Zara's international site; `product_id` names one colour and is usually the same across markets, but a colour can carry another id in some markets (measured: 8727/223 colour 406 is 545413053 on gb, 588478514 on es) and `cn` runs its own ids: match across markets with the reference.
- Prices are per colour: quote the price of the colour the user asked about. In `/prices`, `price` is the lowest current price among the reference's colours; each colour is in `colors`.
- `old_price` appears only on a markdown. Zara's sales are seasonal and per market: an empty `/deals` answer is not an error, and never claim every market has a sale running. On `fr`, `be`, `lu`, `mc` and `iq` special prices carry no previous price.
- `availability` on search, product and stock is ONLINE stock in that market. `/store-stock` is units in physical stores. Never present one as the other. Zara's own help pages call store stock information tentative.
- Category ids are shared across the northern-hemisphere catalogue; `au`, `za` and `br` run their own ids. A parent category answers `400` (charged): use a `leaf: true` id or the parent's `redirect_id`.
- Materials give composition, care and the country of production as Zara states them; Zara names no factories. Never add factory names or addresses.
- Zara shows no reviews or ratings: none are returned, and never claim to have read Zara reviews.
- Not available: reviews, price history (poll and store), checkout, and Inditex's other brands (Pull&Bear, Massimo Dutti, Bershka, Stradivarius, Oysho, Zara Home, Lefties).
- Terms: Zara's US terms say the site is for legitimate inquiries and orders, and that its materials may not be copied or reproduced for any public or commercial purpose without Zara's written permission. This is not legal advice; read the current terms for your market and use case. Do not republish Zara product photos, campaign images or logos; link product pages instead.
- Never fabricate prices, references, sizes, stock, store details or materials. Only return what the API returned, with the country, the currency and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged (one exception below): a `country` the endpoint does not serve or a held-back one (`uk`, `by`, a worldwide-store country); a `language` the market does not serve, or a held one (Arabic on `iq`, `xe`, `ma`, `sa`; Spanish on `cw`); both or neither of `query` and `reference` on search; a filter, sort or page with `reference` on search; a `sort` on `cn` search; more than one value for `color` or `size`; `product_id` without `slug` on product; neither `store_ids` nor `lat` + `lng` (or both) on store-stock; more than 8 store ids; a reference not in the `4591/381` form; more than 10 `countries` on prices. The exception: a parent `category_id` with no products of its own answers `400` and is charged ("use a leaf id from categories").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Zara has no product ... on ... (unknown id, or not sold there).", "Zara does not sell ... on ....", "Zara has no category ... on .... Use a leaf id from categories.", "Zara lists no store near ... on ....". Take ids and references from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=zara-api).
- `502` means Zara data was temporarily unavailable ("Zara is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds. On `/prices` a market that fails is listed in `errors` and not charged; the other markets still answer.
- `503` with a `Retry-After` header means Zara is busy ("Zara is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.63.1
npm install scavio@0.64.1
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: prices } = await scavio.zara.prices({ reference: "4591/381", countries: ["us", "gb", "es", "jp"] });
const { data: found } = await scavio.zara.search({ query: "blazer", country: "es", language: "es" });
const { data: item } = await scavio.zara.product({ product_id: "588478514", slug: "trf-low-rise-wide-leg-jeans-p08727223" });
const { data: made } = await scavio.zara.materials({ product_id: "588478514" });
const { data: online } = await scavio.zara.stock({ product_id: "588478514" });
const { data: stores } = await scavio.zara.stores({ lat: 40.7128, lng: -74.006 });
const { data: units } = await scavio.zara.storeStock({ product_id: "553306790", store_ids: ["3904", "11818"] });
const { data: tree } = await scavio.zara.categories({ section: "woman" });
const { data: dresses } = await scavio.zara.category({ category_id: "2420896", sort: "price_asc" });
const { data: special } = await scavio.zara.deals({ section: "woman" });
const { data: fresh } = await scavio.zara.newArrivals({ country: "gb" });
const { data: typed } = await scavio.zara.suggestions({ query: "jea" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.zara.search(...)`, `client.zara.product(...)`, `client.zara.materials(...)`, `client.zara.stock(...)`, `client.zara.stores(...)`, `client.zara.store_stock(...)`, `client.zara.categories(...)`, `client.zara.category(...)`, `client.zara.deals(...)`, `client.zara.new_arrivals(...)`, `client.zara.prices(...)` and `client.zara.suggestions(...)`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all twelve endpoints as tools: `search_zara`, `get_zara_product`, `get_zara_materials`, `get_zara_stock`, `get_zara_stores`, `get_zara_store_stock`, `get_zara_categories`, `get_zara_category`, `get_zara_deals`, `get_zara_new_arrivals`, `get_zara_prices` and `get_zara_suggestions`. Zara is opt-in: add `zara` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.61.1"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,zara"
      }
    }
  }
}
```
