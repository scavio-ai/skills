---
name: fashion-nova-api
description: Fashion Nova API for Fashion Nova sale prices - each style's price, the compare-at (struck-through) price and the percent off computed from the two, the final-sale flag and per-size stock, in any of Fashion Nova's 104 countries in the local currency (37 currencies; English everywhere, Spanish in 67 countries). Keyword search (60 per page, up to page 18), any collection to full depth (sale, best sellers, new, back in stock, Black Friday deals), one style in full with every colour and size, reviews (10 per page, up to page 8, one English pool), the category tree, search suggestions and similar styles. 7 endpoints, 1 credit per call. In the 27 EEA countries there is no compare-at price, so no percent off. No stores, brand directory or price history (poll and store).
version: 1.0.0
tags: fashion-nova, fashionnova, fashion-nova-api, fashion-nova-prices, fashion-nova-sale, fashion-nova-sale-prices, fashion-nova-black-friday, fashion-nova-deals, fashion-nova-compare-at, fashion-nova-percent-off, fashion-nova-final-sale, fashion-nova-stock, fashion-nova-sizes, fashion-nova-reviews, fashion-nova-search, fashion-nova-product-data, fashion-nova-collections, fashion-nova-curve, fast-fashion, fashion, clothing-prices, sale-prices, price-monitoring, price-tracker, multi-country, multi-currency, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/docs/fashionnova-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api
---

# Fashion Nova API - Sale Prices, Sizes in Stock, Reviews

Read Fashion Nova's own online store (fashionnova.com) in any of its 104 country storefronts: keyword search, any collection to full depth, one style in full with every colour and size, its reviews, the category tree, search suggestions and similar styles. All 7 endpoints return structured JSON at 1 credit per call.

**The job this skill is for: Fashion Nova sale prices.** Each style's `price`, the `compare_at` price (the struck-through price the site shows), `percent_off` computed by Scavio from the two, the `final_sale` flag and the stock of every size, in the storefront's own currency, on a dated read.

Five limits shape every answer, so say them plainly:
- **Search is 60 per page, pages 1-18 (1-6 under a sort other than `featured`), and is matched loosely.** Fashion Nova's search is semantic: its `total` moves between calls, page 2 can repeat a few items of page 1, and loosely related items show up further down. Never call a search answer "all products". Narrow with filters, or browse a collection.
- **Collections page through to full depth** (60 per page, up to page 200; `has_more` says when the list ends). Use them for complete lists: `sale`, `best-sellers`, `new`, `back-in-stock`, `womens-novadeals` (the Black Friday Deals link) or any category handle.
- **No compare-at price in the 27 EEA countries.** There Fashion Nova shows VAT-inclusive prices and no struck-through price, so `compare_at` and `percent_off` are `null` and `on_sale` is `false`. That is not "no discount": it is a price the site shows without a "was" price.
- **Stock is per size, as Fashion Nova's page shows it.** `quantity` is the number the page carries and `low_stock` is the site's own flag. Never promise exact inventory.
- **Reviews are one English pool shared by every storefront**, 10 per page, pages 1-8 per sort and star filter. No reviewer names are returned.

Fashion Nova has no public developer API or product feed. This skill reads the public fashionnova.com storefronts instead, with one Scavio key.

See also: for ASOS prices by country use `asos-api`; for Zara use `zara-api`; for H&M use `hm-api`; for Uniqlo use `uniqlo-api`; for Fashion Nova items resold second-hand use `thredup-api` or `poshmark-api`.

## When to trigger

Use this skill when the user asks to:
- Check Fashion Nova sale prices: the price, the compare-at price, the percent off and whether an item is final sale
- Compare one Fashion Nova style's price across countries and currencies (us, ca, gb, au, mx and the other 99)
- Read Fashion Nova's sale, Black Friday deals, best sellers, new arrivals or back-in-stock collection in full
- See which sizes of a style are in stock, low stock or sold out, in every colour
- Read Fashion Nova reviews sorted by most recent, most helpful, highest or lowest rated, or only 1-star (or any star) reviews, with fit, size purchased and usual size
- Search Fashion Nova by keyword with size, colour, price, division (women, curve), category or any other facet (occasion, fit, rise, fabric ...)
- Resolve collection handles, trending searches and search suggestions before a search

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, search took 5 seconds, product 4, collection 4, similar 7, categories 2, suggestions 2 and reviews 17 (reviews can take 20-60 seconds). Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns |
|---|---|
| `POST /api/v1/fashionnova/search` | Styles for a keyword in one storefront, 60 per page (pages 1-18, 1-6 under a sort), with filters and sorts, plus the facets the answer offers. Matched loosely: narrow with filters |
| `POST /api/v1/fashionnova/collection` | One collection by handle or link (sale, best-sellers, new, back-in-stock, womens-novadeals, jeans, dresses, mens, plus ...), 60 per page to full depth (up to page 200), same filters and sorts |
| `POST /api/v1/fashionnova/product` | One style by handle (+ colour) or link: every colour with every size (SKU, price, compare-at, quantity, low stock), rating with star histogram and fit, the first 3 reviews, Fashion Nova's own AI review summary, size guide, delivery estimate, promo line |
| `POST /api/v1/fashionnova/reviews` | A page of a style's reviews, 10 per page (pages 1-8), sorted and filtered by star |
| `POST /api/v1/fashionnova/categories` | The navigation for one division (women, men, curve) as collection handles, plus the site's trending searches |
| `POST /api/v1/fashionnova/suggestions` | Search suggestions for a partial query: suggested searches, styles (no prices) and collections |
| `POST /api/v1/fashionnova/similar` | Styles Fashion Nova recommends as similar to one style, 1-24 (default 12), US store in USD |

## Credits

Every endpoint costs **1 credit per call**. Each page is one call. A not-found (`404`: unknown handle, a colour the style does not have, unknown collection) is charged; a `400` and an upstream failure (`502`, `503`) are not.

## Markets

`search`, `collection` and `product` take `country` (lowercase ISO-2, default `us`) and `language` (`en` default, or `es` where the storefront serves Spanish). Every answer echoes `country`, `language` and `currency`. Prices are never converted: each storefront answers in its own currency.

104 countries, 37 currencies, 171 country-language storefronts (Fashion Nova's own country selector, measured 2026-11-19):

| Currency | `country` |
|---|---|
| USD (38) | `us`, `zz` (Fashion Nova's International storefront), `ac`, `ag`, `ai`, `am`, `cc`, `ck`, `cx`, `eh`, `fk`, `fo`, `gg`, `gl`, `gs`, `io`, `iq`, `kg`, `ki`, `nr`, `nu`, `pm`, `pn`, `sb`, `sh`, `sj`, `sx`, `ta`, `tf`, `tj`, `tk`, `tm`, `to`, `tv`, `um`, `wf`, `ws`, `xk` |
| EUR (31) | EEA, no compare-at: `at`, `be`, `cy`, `de`, `ee`, `es`, `fi`, `fr`, `gr`, `ie`, `it`, `lt`, `lu`, `lv`, `mt`, `nl`, `pt`, `si`, `sk`; with a compare-at: `ad`, `ax`, `bl`, `gf`, `gp`, `mc`, `me`, `mf`, `mq`, `re`, `va`, `yt` |
| One country each (35) | `ae` AED, `al` ALL, `ao` AOA, `au` AUD, `ca` CAD, `ch` CHF, `cl` CLP, `cz` CZK, `dk` DKK, `do` DOP, `gb` GBP, `hk` HKD, `hu` HUF, `il` ILS, `is` ISK, `jp` JPY, `kr` KRW, `ky` KYD, `mx` MXN, `my` MYR, `mz` MZN, `ng` NGN, `no` NOK, `nz` NZD, `pe` PEN, `ph` PHP, `pl` PLN, `qa` QAR, `ro` RON, `ru` RUB, `sa` SAR, `sc` SCR, `se` SEK, `sg` SGD, `za` ZAR |

- **EEA (27, no compare-at):** `at`, `be`, `cy`, `cz`, `de`, `dk`, `ee`, `es`, `fi`, `fr`, `gr`, `hu`, `ie`, `is`, `it`, `lt`, `lu`, `lv`, `mt`, `nl`, `no`, `pl`, `pt`, `ro`, `se`, `si`, `sk`. Prices include VAT; `compare_at`, `percent_off` are `null` and `on_sale` is `false`. The non-EEA euro storefronts (`ad`, `mc`, `me`, `va`, `re`, `gp` ...) keep a compare-at price.
- **Spanish (`language: "es"`) in 67 countries:** every country above except the 37 English-only ones (`us`, `zz` and the other USD territories listed first, except `xk`). Titles, descriptions, badges and the promo line come back in Spanish (in the captured `mx`/`es` product, `details` and `materials` stayed in English). Fashion Nova's own site defaults to Spanish in `cl`, `do`, `es`, `mx` and `pe`; Scavio's default stays `en` everywhere.
- A country Fashion Nova does not run, or `es` where the storefront has no Spanish, answers `400` before anything is charged (the message lists the countries, or the storefront's languages).
- `reviews` and `suggestions` take no `country`: one English review pool and one suggestion list serve every storefront. `categories` handles work in every storefront. `similar` answers from the US store in USD.

The same style in six storefronts (San Diego Sculpting Stretch Flare Jeans, Black Wash, captured 2026-11-19, `/product`):

| `country` / `language` | `currency` | `price` | `compare_at` | `percent_off` |
|---|---|---|---|---|
| `us` / `en` | USD | 18 | 34.99 | 49 |
| `ca` / `en` | CAD | 27 | 51 | 47 |
| `gb` / `en` | GBP | 17 | 32 | 47 |
| `au` / `en` | AUD | 31 | 60 | 48 |
| `mx` / `es` | MXN | 338 | 656 | 48 |
| `fr` / `en` (EEA) | EUR | 20.95 | null | null |

## Sale prices

- `price` is the price the site lists (the lowest size price on a style); `compare_at` is the struck-through price the site shows next to it.
- `percent_off` is computed by Scavio: `round((1 - price / compare_at) * 100)`. `on_sale` is `true` when `compare_at` is above `price`. Both are `null` / `false` without a compare-at price (the EEA storefronts). Quote it as "computed from the price and the compare-at price".
- `badge` is the site's own label (`60% OFF`, `DEALS`, `SNATCHED`, `NOVA LUXE`, `OFERTAS` in Spanish). It is a label, not a computed figure: use `percent_off` for numbers.
- `price_with_code` is `{price, currency}`: the price the site shows with its current promo code, when it shows one; `price` stays the listed price. `promo` on a product is the site's promo line (captured: "Black Friday Deals Starting at $5! Prices as Marked").
- `final_sale` marks items the site sells as final sale. On the captured `sale` collection page, all 60 items were final sale.

## Workflow

1. **Sale prices for a query:** `/fashionnova/search` with `query` (and `country`). Each item has `price`, `compare_at`, `percent_off`, `on_sale`, `final_sale`, `badge`, `sizes_in_stock` and `sizes[]`.
2. **A complete list:** `/fashionnova/collection` with a `handle` from `/fashionnova/categories` (`sale`, `best-sellers`, `new`, `back-in-stock`, `womens-novadeals` ...), paging until `has_more` is `false`. There is no `clearance` collection; `sale` is the markdown collection.
3. **Narrow it:** every list answer carries `facets[]` (`name`, `title`, `values[]`). Pass `size`, `color`, `price_min` / `price_max`, `division`, `category` directly, and any other facet in `filters` by `facets[].name` with `facets[].values[].value`.
4. **One style:** `/fashionnova/product` with `handle` (`items[].handle`) and `color` (`items[].color_slug`). Every colour and size comes back, so one call covers the style.
5. **Across countries:** call `/product` once per `country`. Compare within a currency, or convert explicitly with a dated rate.
6. **Reviews:** `/fashionnova/reviews` with `handle`, `sort` and `star`. The product answer already carries the rating, the histogram and the first 3 reviews.
7. **Price watching:** there is no price history. Poll the same style or collection on a schedule and store each answer with its `fetched_at` date.

## Parameters

### Search (`/search`) and collection (`/collection`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Search text (1-200 chars). Search only |
| `handle` | string | collection: one of | Collection handle (`categories[].handle`, `sections[].items[].handle`): `sale`, `best-sellers`, `new`, `new-this-week`, `back-in-stock`, `coming-soon`, `womens-novadeals`, `jeans`, `dresses`, `mens`, `plus` ... |
| `url` | string | collection: one of | A fashionnova.com collection link. Send exactly one of `handle`, `url` |
| `country` | string | `us` | See Markets |
| `language` | string | `en` | `en` or `es` (where served) |
| `sort` | string | `featured` | `featured`, `best_selling`, `price_low`, `price_high`, `newest` |
| `size` | string or array | all | Sizes as the site writes them (`M`, `7`, `1X`), up to 15 (facet `size`) |
| `color` | string or array | all | Colour families, up to 10: `black`, `blue`, `white`, `pink`, `brown`, `red`, `yellow`, `green`, `gray`, `purple`, `orange`, `gold`, `silver`, `nude`, `ivory` ... (facet `color`) |
| `price_min` / `price_max` | number | none | Whole units of the storefront's currency |
| `division` | string or array | all | `women` or `curve` (Fashion Nova's plus range) |
| `category` | string or array | all | Categories as the site writes them (`Jeans`, `Dresses`, `Tops`), facet `category` |
| `filters` | object | none | Any other facet by `facets[].name` -> value or list of values (`facets[].values[].value`), up to 10 facets, e.g. `{"fit_type": "Baggy", "rise": "High Rise"}`. Captured facet names: `occasion`, `sleeve`, `bottom_style`, `bottom_length`, `fabric`, `detail`, `neckline`, `fit_type`, `print`, `top_style`; others include `rise`, `stretch`, `wash`, `top_length`, `deals` |
| `page` | integer | 1 | 60 per page. Search: 1-18, or 1-6 under a sort other than `featured`. Collection: 1-200 |

A facet name the list does not offer matches nothing: the answer has 0 items and lists the name in `unrecognized_filters`. Fix the name from `facets[]`.

### Product (`/product`), reviews (`/reviews`), similar (`/similar`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `handle` | string | one of | Style handle (`items[].handle`), e.g. `san-diego-sculpting-stretch-flare-jeans` |
| `url` | string | one of | A fashionnova.com product link, any storefront. Send exactly one of `handle`, `url` |
| `color` | string | style default | Colour slug (`items[].color_slug`, `colors[].color_slug`), e.g. `black-wash` |
| `country`, `language` | string | `us`, `en` | Product only (see Markets) |
| `sort` | string | `highest_rated` | Reviews only: `highest_rated`, `most_recent`, `most_helpful`, `lowest_rated` |
| `star` | integer | all | Reviews only: only reviews with this star rating, 1-5 |
| `page` | integer | 1 | Reviews only: 10 per page, 1-8 |
| `limit` | integer | 12 | Similar only: 1-24 |

### Categories (`/categories`) and suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `division` | string | `women` | `women`, `men` or `curve` |
| `query` | string | suggestions: required | What the shopper has typed so far (1-100 chars) |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/fashionnova/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "bodycon dress"}'
```

Captured `data` (2026-11-19, 1 credit; 1 of 60 items shown, 3 of 9 sizes and 2 of 5 colours kept, `image` and `facets` omitted):

```json
{
  "query": "bodycon dress",
  "country": "us",
  "language": "en",
  "currency": "USD",
  "sort": "featured",
  "filters": {},
  "page": 1,
  "page_size": 60,
  "total": 372,
  "total_pages": 7,
  "has_more": true,
  "count": 60,
  "items": [
    {
      "product_id": "6545011703932",
      "handle": "mallory-halter-snatched-midi-dress",
      "color": "Chocolate",
      "color_slug": "chocolate",
      "title": "Mallory Halter Snatched Midi Dress - Chocolate",
      "base_title": "Mallory Halter Snatched Midi Dress",
      "url": "https://www.fashionnova.com/products/mallory-halter-snatched-midi-dress?color=chocolate",
      "product_type": "Dresses",
      "price": 23.99,
      "compare_at": 34.99,
      "percent_off": 31,
      "on_sale": true,
      "currency": "USD",
      "price_with_code": { "price": 21, "currency": "USD" },
      "final_sale": false,
      "badge": "SNATCHED",
      "in_stock": true,
      "coming_soon": false,
      "limited": false,
      "sizes_in_stock": 8,
      "sizes": [
        { "size": "XXS", "quantity": 0, "available": false, "low_stock": false },
        { "size": "XS", "quantity": 68, "available": true, "low_stock": false },
        { "size": "S", "quantity": 169, "available": true, "low_stock": false }
      ],
      "colors": [
        { "color": "Black", "color_slug": "black", "product_id": "6544132374652" },
        { "color": "Chocolate", "color_slug": "chocolate", "product_id": "6545011703932" }
      ]
    }
  ]
}
```

Read the item as: listed at $23.99, compare-at $34.99, 31 percent off computed from the two, $21 with the site's current promo code. On this page all 60 items were `on_sale`, 5 were `final_sale`, and `percent_off` ran from 30 to 70 (median 40). The same query in `fr` returned this style at EUR 26.95 with `compare_at: null` and `percent_off: null` (EEA); in `mx` / `es` at MXN 450 against 656 as "Vestido Midi Ajustado Mallory Halter - Chocolate". `total` (372) is the search's count for this call; it moves between calls.

### Collection

```bash
curl -X POST https://api.scavio.dev/api/v1/fashionnova/collection \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"handle": "sale"}'
```

Captured (2026-11-19, 1 credit): `handle: "sale"`, `title: "Women's Clothing on Sale"`, `total` 365, `total_pages` 7, `has_more: true`, 60 items in the search item shape and 8 facets (`category`, `size`, `color`, `occasion`, `fabric`, `top_style`, `bottom_style`, `price`). The first item: Soft Days Plaid Blouse - Brown/combo at $10.98 against $27.99, `percent_off` 61, `final_sale: true`, badge `60% OFF`. On this page every item was `final_sale`, prices ran from $4.98 to $13.98 and `percent_off` from 60 to 62. A collection page can hold fewer than 60 items and still not be the last: follow `has_more`.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/fashionnova/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"handle": "san-diego-sculpting-stretch-flare-jeans", "color": "black-wash"}'
```

Captured `data` (2026-11-19, 1 credit; trimmed to the price, stock and review fields: `base_title`, `url`, `description`, `details`, `coming_soon`, `limited`, `images`, `colors`, `collections` and `size_guide` dropped, 5 of 10 `attributes`, 3 of 15 sizes, 1 of 3 reviews without its text and votes, and only `buy_if` of the AI summary kept):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "product_id": "6547082739836",
  "handle": "san-diego-sculpting-stretch-flare-jeans",
  "color": "Black Wash",
  "color_slug": "black-wash",
  "title": "San Diego Sculpting Stretch Flare Jeans - Black Wash",
  "brand": "Fashion Nova",
  "division": "women",
  "product_type": "Jeans",
  "materials": "54% Cotton 26% Polyester 18% Rayon 2% Spandex",
  "attributes": { "bottom_style": "Flare", "category": "Jeans", "fit_type": "Fitted", "rise": "High Rise", "deals": "Shop Deals" },
  "model_height": null,
  "price": 18,
  "compare_at": 34.99,
  "percent_off": 49,
  "on_sale": true,
  "price_with_code": null,
  "promo": "Black Friday Deals Starting at $5! Prices as Marked",
  "final_sale": false,
  "badge": "DEALS",
  "in_stock": true,
  "sizes": [
    { "size": "00", "sku": "YJDM15HRSFL1_BlackWash_00", "price": 18, "compare_at": 34.99, "quantity": 23, "available": true, "low_stock": false },
    { "size": "3", "sku": "YJDM15HRSFL1_BlackWash_3", "price": 18, "compare_at": 34.99, "quantity": 105, "available": true, "low_stock": false },
    { "size": "14 Plus", "sku": "YJDM15HRSFL1_BlackWash_14 Plus", "price": 18, "compare_at": 34.99, "quantity": 0, "available": false, "low_stock": false }
  ],
  "rating": { "average": 4.5, "count": 602, "histogram": { "1": 29, "2": 10, "3": 42, "4": 70, "5": 451 }, "fit": "true_to_size", "fit_score": 2 },
  "reviews": [
    { "id": "925893419", "rating": 5, "title": "Love", "date": "2026-11-17T20:14:26.000Z", "verified_buyer": true, "fit": "true_to_size", "size_purchased": "M", "usual_size": "M", "color_purchased": "Light Wash" }
  ],
  "site_ai_review_summary": {
    "buy_if": "Buy this if you are looking for high-rise flare jeans with comfortable stretch, durable soft denim, and a long, flattering silhouette in a classic black wash."
  },
  "delivery": {
    "standard": { "method": "3-7 Business Days", "from": "2026-11-25", "to": "2026-11-25", "order_by": "2026-11-18T20:00:00-08:00" },
    "rush": { "method": "1-Day Shipping", "from": "2026-11-20", "to": "2026-11-20", "order_by": "2026-11-19T13:30:00-08:00" }
  },
  "default_collection": { "handle": "jeans", "title": "Fashion Nova Jeans" }
}
```

The 15 sizes ran from `00` to `22 Plus`: sizes `00` to `15` had 13 to 105 units, the five Plus sizes 0. `colors[]` holds every colour of the style (here Black Wash, Dark Wash and Light Wash, each at 18 against 34.99) with its own `sizes[]`, so one call prices every colour and size. `site_ai_review_summary` is Fashion Nova's own AI summary of its reviews (`summary`, `buy_if`, `topics`, `generated_at`), not Scavio's: label it so when quoting it. `delivery` is `null` where the site gives no estimate for the storefront (the `ca`, `gb` and `au` captures). `size_guide` is `{title, inches, cm}`, each a table of rows.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/fashionnova/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"handle": "san-diego-sculpting-stretch-flare-jeans", "color": "black-wash", "sort": "most_recent"}'
```

Captured `data` (2026-11-19, 1 credit; 1 of 10 reviews shown):

```json
{
  "handle": "san-diego-sculpting-stretch-flare-jeans",
  "color_slug": "black-wash",
  "sort": "most_recent",
  "star": null,
  "page": 1,
  "page_size": 10,
  "language": "en",
  "total": 602,
  "has_more": true,
  "rating": { "average": 4.5, "count": 602, "histogram": { "1": 29, "2": 10, "3": 42, "4": 70, "5": 451 }, "fit": "true_to_size", "fit_score": 2 },
  "count": 10,
  "reviews": [
    {
      "id": "925899348",
      "rating": 4,
      "title": "Cute jeans just order your",
      "body": "Cute jeans just order your size or maybe the next size up",
      "date": "2026-11-17T21:11:11.000Z",
      "verified_buyer": true,
      "votes_up": 0,
      "votes_down": 0,
      "fit": "true_to_size",
      "fit_score": 2,
      "size_purchased": "9",
      "usual_size": "9 or 11",
      "color_purchased": "Light Wash",
      "language": "en",
      "topics": []
    }
  ]
}
```

`fit` is the page's own 1-3 scale (`runs_small`, `true_to_size`, `runs_large`, with `fit_score` 1-3). `total` is the count of reviews matching the filter; one sort and star combination reaches 80 reviews (8 pages of 10), so use `star` and the other sorts to read more. No reviewer names are returned.

### Categories, suggestions and similar

- `/categories` (women, 2026-11-19): 19 categories, `collection_count` 369, such as `{"name": "Black Friday Deals", "handle": "womens-novadeals"}`, `{"name": "Jeans", "handle": "jeans"}` and `{"name": "Sale", "handle": "sale"}`, each with `sections[]` of `{name, items[] {name, handle, url}}`, plus 8 `trending_searches` (`sweater dress`, `boots`, `going out`, `coats`, `pajamas`, `thanksgiving`, `brown dress`, `two piece sets`). Every `handle` is an input of `/collection`.
- `/suggestions` with `{"query": "dress"}`: 5 `queries` (`dress`, `spring dresses`, `black dress`, `white dress`, `maxi dress`), 4 `products` such as `{"title": "Madison Midi Dress - Black", "title_es": "Vestido Midi Madison - Negro", "handle": "madison-midi-dress", "color_slug": "black"}` (no prices: call `/product`) and 5 `collections` (`dresses`, `sale-dresses` ...).
- `/similar` with the San Diego jeans: 12 items in the search item shape, US store in USD, the first Lucy High Rise Stretch Flare Jeans - Black Wash at $18 against $29.99 (`percent_off` 40).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def fashionnova(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/fashionnova/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. One style in several storefronts (1 credit each). Prices stay in each local currency.
for country in ("us", "ca", "gb", "au", "fr"):
    res = fashionnova("product", {"handle": "san-diego-sculpting-stretch-flare-jeans", "color": "black-wash", "country": country})
    p = res["data"]
    print(res["fetched_at"], country, p["currency"], p["price"], p["compare_at"], p["percent_off"])  # fr: compare_at None (EEA)

# 2. The whole sale collection, page by page, with sizes in stock (1 credit per page)
rows, page = [], 1
while True:
    d = fashionnova("collection", {"handle": "sale", "page": page})["data"]
    for i in d["items"]:
        rows.append((i["title"], i["price"], i["compare_at"], i["percent_off"], i["final_sale"], i["sizes_in_stock"], i["url"]))
    if not d["has_more"]:
        break
    page += 1
print(len(rows), "sale items")

# 3. The lowest-rated reviews of one style (1 credit per page of 10)
low = fashionnova("reviews", {"handle": "san-diego-sculpting-stretch-flare-jeans", "sort": "lowest_rated"})["data"]
for rv in low["reviews"]:
    print(rv["rating"], rv["fit"], rv["size_purchased"], rv["usual_size"], rv["body"][:80])

# Store each answer with fetched_at and run this on a schedule: that stored series is
# your price history (Fashion Nova publishes none).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached.

- **item** (search, collection, similar) - `product_id`, `handle` (the style), `color`, `color_slug`, `title`, `base_title`, `url`, `product_type`, `price`, `compare_at`, `percent_off`, `on_sale`, `currency`, `price_with_code` {`price`, `currency`} or `null`, `final_sale`, `badge`, `in_stock`, `coming_soon`, `limited`, `sizes_in_stock`, `sizes[]` {`size`, `quantity`, `available`, `low_stock`}, `image`, `colors[]` {`color`, `color_slug`, `product_id`}.
- **search / collection** - `query` (search) or `handle`, `title`, `description`, `url` (collection), then `country`, `language`, `currency`, `sort`, `filters`, `unrecognized_filters` (only when a facet name was not offered), `page`, `page_size` (60), `total`, `total_pages`, `has_more`, `count`, `items[]`, `facets[]` {`name`, `title`, `values[]` {`value`, `label`}}.
- **product** - `country`, `language`, `currency`, `product_id`, `handle`, `color`, `color_slug`, `title`, `base_title`, `url`, `brand`, `division`, `product_type`, `description`, `details`, `materials`, `attributes` {category, occasion, fit_type, rise, stretch, print ...}, `model_height` (when the site gives it), `price`, `compare_at`, `percent_off`, `on_sale`, `price_with_code`, `promo`, `final_sale`, `badge`, `in_stock`, `coming_soon`, `limited`, `sizes[]` {`size`, `sku`, `price`, `compare_at`, `quantity`, `available`, `low_stock`}, `images[]`, `colors[]` {`product_id`, `color`, `color_slug`, `title`, `url`, `price`, `compare_at`, `percent_off`, `on_sale`, `currency`, `price_with_code`, `final_sale`, `badge`, `in_stock`, `coming_soon`, `image`, `sizes[]`}, `rating` {`average`, `count`, `histogram`, `fit`, `fit_score`}, `reviews[]` (the first 3), `site_ai_review_summary` {`summary`, `buy_if`, `topics`, `generated_at`}, `size_guide` {`title`, `inches`, `cm`}, `delivery` {`standard`, `rush`: {`method`, `from`, `to`, `order_by`}} or `null`, `default_collection` {`handle`, `title`}, `collections[]` {`handle`, `title`}.
- **review** - `id`, `rating`, `title`, `body`, `date`, `verified_buyer`, `votes_up`, `votes_down`, `fit` (`runs_small`, `true_to_size`, `runs_large`), `fit_score`, `size_purchased`, `usual_size`, `color_purchased`, `language`, `topics[]`. **reviews** - `handle`, `color_slug`, `sort`, `star`, `page`, `page_size` (10), `language` (`en`), `total`, `has_more`, `rating`, `count`, `reviews[]`.
- **categories** - `division`, `count`, `collection_count`, `categories[]` {`name`, `handle`, `url`, `sections[]` {`name`, `items[]` {`name`, `handle`, `url`}}} (`handle` is `null` for a link that is not a collection), `trending_searches[]`.
- **suggestions** - `query`, `division`, `count`, `queries[]`, `products[]` {`product_id`, `title`, `title_es`, `handle`, `color_slug`, `url`, `image`}, `collections[]` {`handle`, `title`}.
- **similar** - `handle`, `color_slug`, `product_id`, `title`, `country` (`us`), `language`, `currency` (USD), `count`, `items[]`.

## Guardrails

- Search is semantic and capped: 18 pages of 60 (6 under a sort), a `total` that moves between calls, and items that can repeat across pages. Never call a search answer "all products" and never present `total` as what was returned. For complete lists use a collection and follow `has_more`; de-duplicate by `product_id` when combining search pages.
- `percent_off` is computed by Scavio from `price` and `compare_at`; say so. `badge` is the site's own label and can differ from it. In the 27 EEA storefronts there is no compare-at price: report `percent_off` as not available there, never as 0.
- Prices are in each storefront's own currency and are not converted. Convert explicitly, with the rate and its date, before comparing storefronts. EEA prices include VAT.
- `quantity` is the per-size number Fashion Nova's page shows and `low_stock` is the site's own flag: report them as what the page showed at `fetched_at`, never as guaranteed inventory.
- Reviews: one English pool for every storefront; 80 reviews per sort and star combination; review totals as returned. Never return or try to identify reviewer names. `site_ai_review_summary` is Fashion Nova's own AI summary: label it as Fashion Nova's. If review moderation comes up: in January 2022 Fashion Nova paid $4.2 million to settle FTC allegations that it did not post reviews under four stars (FTC press release, January 25, 2022). Never imply anything about current reviews beyond what an answer shows.
- `price_with_code` is the price with the site's current promo code, not what every buyer pays; `price` is the listed price.
- Not available: a store locator (Fashion Nova lists no stores), a brand directory (everything is Fashion Nova's own brand), price history (poll and store), gift cards, new-arrival dates. This API cannot buy, add to cart or apply codes.
- Terms: Scavio does not collect or store Fashion Nova data: each call fetches the public Fashion Nova page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Fashion Nova's terms of service cover how its service may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Fashion Nova product photos or logos; link styles by `url` instead.
- Never fabricate prices, compare-at prices, stock, reviews or ratings. Only return what the API returned, with the currency, the `fetched_at` date and the item `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a country Fashion Nova does not run (the message lists the countries), `es` where the storefront has no Spanish, a `page` above the cap (search 18, or 6 under a sort; collection 200; reviews 8), a missing `query` on search or suggestions, both or neither of `handle` / `url`, a `handle` that is not a Fashion Nova handle, a `color` that is not a colour slug, a `url` that is not a fashionnova.com product or collection link, an unknown `sort`, `division` or `star`, `price_min` above `price_max`, more than 10 facets in `filters`, or a named input (`size`, `color`, `division`, `sort`, `page`, `query`, price) sent inside `filters`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Fashion Nova product with this handle (or this colour of it).", "No Fashion Nova collection with this handle (collection handles come from categories).", "No similar products for this product." Take handles and colour slugs from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api).
- `502` means Fashion Nova data was temporarily unavailable ("Fashion Nova is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Fashion Nova is busy ("Fashion Nova is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.71.0
npm install scavio@0.72.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.fashionnova.search({ query: "bodycon dress", country: "gb" });
const { data: sale } = await scavio.fashionnova.collection({ handle: "sale", page: 1 });
const { data: style } = await scavio.fashionnova.product({ handle: "san-diego-sculpting-stretch-flare-jeans", color: "black-wash", country: "mx", language: "es" });
const { data: reviews } = await scavio.fashionnova.reviews({ handle: "san-diego-sculpting-stretch-flare-jeans", sort: "most_recent" });
const { data: nav } = await scavio.fashionnova.categories({ division: "women" });
const { data: typed } = await scavio.fashionnova.suggestions({ query: "dress" });
const { data: similar } = await scavio.fashionnova.similar({ handle: "san-diego-sculpting-stretch-flare-jeans", limit: 12 });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.fashionnova.search(...)`, `collection`, `product`, `reviews`, `categories`, `suggestions` and `similar`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all seven endpoints as tools: `search_fashionnova`, `get_fashionnova_collection`, `get_fashionnova_product`, `get_fashionnova_reviews`, `get_fashionnova_categories`, `get_fashionnova_suggestions` and `get_fashionnova_similar`. Fashion Nova is opt-in: add `fashionnova` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.71.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,fashionnova"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/fashionnova-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api), [collection](https://scavio.dev/docs/fashionnova-collection?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api), [product](https://scavio.dev/docs/fashionnova-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api), [reviews](https://scavio.dev/docs/fashionnova-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api), [categories](https://scavio.dev/docs/fashionnova-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api), [suggestions](https://scavio.dev/docs/fashionnova-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api), [similar](https://scavio.dev/docs/fashionnova-similar?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api). Overview: [Fashion Nova API](https://scavio.dev/fashionnova-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api).
