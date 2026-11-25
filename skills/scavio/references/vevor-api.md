# Vevor API - Tool Prices by Country, Deals, Variants, Shipping

Read VEVOR (vevor.com, the tools and equipment seller with storefronts in 13 countries) on every storefront it runs: keyword or SKU search, category lists, Best Sellers, New Arrivals, promotion pages, Daily Deals, Clearance and Deals, one product in full with every variant, the shipping fee and delivery date to a destination, reviews, customer questions, search suggestions, the category tree, and the same SKU priced on all 13 storefronts in one call. Prices come as Vevor shows them on that storefront to a visitor without an account, in its own currency. All 11 endpoints return structured JSON at 1 credit per call; prices is 3.

**Read-only data.** This skill reads the public pages Vevor shows to any visitor and returns them as JSON for analysis. It uses no Vevor account, claims no coupon and places no order.

**The job this skill is for: Vevor prices across storefronts and channels.** What a Vevor item costs on vevor.com today, with Vevor's was price only while a deal is active and the deal's start and end as Vevor gives them, how many units the storefront holds, what each variant costs, what shipping to a state costs, and what the same SKU costs on the other Vevor storefronts. On 2026-11-25 (UTC) the VEVOR MIG Welder 3-in-1 270A (SKU `DHJMIGMMAMIGLL6WNV5`) read `price` 182.22 USD against a `was_price` of 219.90 on www.vevor.com, in a Vevor deal from `2026-11-14T08:00:01.000Z` to `2026-11-30T07:59:59.000Z` with 49 of 421 deal units claimed, 507 units in stock and 9 variants priced from 77.90 to 1,599.90 USD. The VEVOR 24" Pressure Washer Surface Cleaner (SKU `GYQXJBMQJQYPKEO1LV0`) was sold on 12 of the 13 storefronts: 195.01 USD in the US, 233.90 CAD in Canada, 175.90 GBP in the UK, 333.90 AUD in Australia, 170.90 to 181.90 EUR on six euro storefronts, 261.99 EUR in Norway and 721.90 PLN in Poland; Mexico did not sell it. Pair it with `amazon-product-data`, `walmart-product-data`, `home-depot-product-data`, `tractor-supply-prices-api`, `tiktok-shop-api` and `ebay-product-data` for the same Vevor item where those retailers list it, and `harbor-freight-api` for an alternative store.

Ten limits shape every answer, so say them plainly:
- **1 credit per call, prices 3.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Prices are per storefront.** One SKU has its own price on each storefront, also between the euro storefronts (the surface cleaner read 170.90 EUR in Germany, 173.90 in the Netherlands, 175.90 in France, 177.90 in Spain, 178.90 in Italy, 181.90 on eur.vevor.com and 261.99 on vevor.co.no). Always report a price with its storefront (`market.country`, `market.host`), its `currency` and the `fetched_at` date; never carry a price from one storefront to another. vevor.co.no and eur.vevor.com sell in EUR.
- **The ZIP and the state never change the price.** Price and stock do not depend on the ZIP or the state; the shipping fee and delivery date do. In the US `/shipping` needs the `state` (in Canada the `province`): an Alaska address (`AK`, ZIP `99501`) read a $130 fee for the MIG welder, and Scavio's capture notes read contiguous states free on the probed items, with delivery dates varying by state.
- **was price only during a deal.** `was_price` is given only while a Vevor deal is active (a deal window that has started and not ended) or where Vevor's page shows its own strikethrough price; otherwise it is `null`. Vevor's reference price on items without an active deal is often below the selling price, so Scavio never computes a discount from it. Quote `deal.starts` and `deal.ends` (or `deal_ends`) exactly as given.
- **Search in the storefront language.** Each storefront language has its own search index: `welder` read 72 results on www.vevor.com and 8 on www.vevor.co.uk, the German store answered `schweissgeraet` and the French store `poste a souder`. Send the term in that storefront's language.
- **Totals above 100 read "100+".** `total` is Vevor's own count: exact up to 100, then a lower bound as Vevor gives it (`"100+"`, `total_is_lower_bound` true). Lists are 60 per page; the Best Sellers and Daily Deals pages read 40 items on page 1. `has_more` says whether Vevor links a next page.
- **One review pool across storefronts and variants.** Reviews come in many languages from many countries (the first 20 reviews of a gate opener were in English, Italian, Romanian, Dutch, French, Spanish and Portuguese), and 18 of those 20 were of other SKUs of the same product. `this_variant_only` narrows to the exact SKU. No reviewer names.
- **SKUs are per storefront.** A SKU is not sold on every storefront (`prices` reads `status` `not_sold`), and a product link belongs to its own storefront. Take SKUs from search on the storefront you ask.
- **No coupon codes.** Vevor shows codes only after a claim, so no answer carries them; `price` is never reduced by a code.
- **No history.** Nothing is cached or kept: poll and store your own series for history.

Vevor publishes no public API for its catalog, prices or stock. Business buyers can join its Pro Member or Dealer & Distributor programmes for volume discounts (application and sign-up forms, not APIs), publishers can join its affiliate programmes on networks such as Awin and FlexOffers, and dropship platforms route orders to Vevor. Prices are shown on vevor.com and Vevor's country storefronts for the storefront a shopper picks, and this skill reads those public pages with one Scavio key. Other vendors sell Vevor product data; this skill reads Vevor's own public pages.

VEVOR, a home improvement brand founded in Shanghai in 2007 (Vevor, "Who is VEVOR?", Jun 11, 2024), says it serves more than 30 million households in over 50 countries, supported by more than 200 warehouses (Vevor release, Sept 14, 2026). Its US site is operated by Sanven Technology Ltd. (vevor.com terms). Quote these with their source, never from the samples.

See also: for the same Vevor item on Amazon use `amazon-product-data`, at Walmart `walmart-product-data`, at Home Depot `home-depot-product-data`, at Tractor Supply `tractor-supply-prices-api`, on TikTok Shop `tiktok-shop-api`, on eBay `ebay-product-data` (same item only: the same VEVOR model number or SKU in the listing, each price with its seller and date); Harbor Freight `harbor-freight-api` sells its own brands and is an alternative store, never the same item.

## When to trigger

Use this skill when the user asks to:
- Price a Vevor item on vevor.com or another Vevor storefront, with the was price only during a deal and the deal's start and end as Vevor gives them
- Compare one Vevor SKU across Vevor's 13 storefronts (US, Canada, UK, Australia, Germany, France, Spain, Italy, Netherlands, Poland, Mexico, Norway, eur.vevor.com), each in its own currency
- Read every variant of a product with its own price, was price and stock
- Check Vevor's shipping fee and delivery date for a US state, a Canadian province or a postcode
- Search Vevor by keyword or SKU, sorted by price or newest and filtered by in stock, on sale, Black Friday, bulk savings, price or rating
- List a Vevor category, its Best Sellers, New Arrivals or a promotion page, or its Daily Deals, Clearance or Deals pages
- Read Vevor reviews of a product, sorted, star-filtered and paged, or only the exact SKU's reviews
- Read customer questions on a product with Vevor's answers
- Read Vevor's category tree or its search suggestions
- Compare a Vevor item on vevor.com with the same item on Amazon, Walmart, Home Depot, Tractor Supply, TikTok Shop or eBay

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit (prices 3), so 50 credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, suggestions, questions, reviews, shipping, deals and prices took 1 to 3 seconds, search and lists 2 to 22, and product 4 to 25 (one product on the Canadian French store took 110). Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/vevor/search` | Keywords in the storefront language or a SKU: 60 items per page with price, was price, deal end, stock units, labels and rating, sorted and filtered | 1 |
| `POST /api/v1/vevor/product` | One product by SKU or link: price, was price, deal window, stock units, every variant with its price and stock, specifications, protection plans, return policy, star split, Vevor's AI review summary, categories | 1 |
| `POST /api/v1/vevor/shipping` | Vevor's shipping fee and delivery date for one SKU to a US state, Canadian province or postcode | 1 |
| `POST /api/v1/vevor/reviews` | Reviews of one product, up to 100 per page, sorted, star-filtered, with photos only or this SKU only, with Vevor's replies | 1 |
| `POST /api/v1/vevor/questions` | Customer questions on one product with their answers (Vevor's flagged), 5 per page | 1 |
| `POST /api/v1/vevor/suggestions` | What Vevor's search box suggests for typed text | 1 |
| `POST /api/v1/vevor/categories` | Vevor's category tree (departments, categories, sub-categories) or one branch | 1 |
| `POST /api/v1/vevor/category` | One category listing, sorted, filtered and paged like search | 1 |
| `POST /api/v1/vevor/collections` | Best Sellers (optionally one category), New Arrivals (with the date Vevor first listed each item) or one promotion page | 1 |
| `POST /api/v1/vevor/deals` | Vevor's Daily Deals, Clearance or Deals page, optionally one category | 1 |
| `POST /api/v1/vevor/prices` | The same SKU on all 13 storefronts: status, price, was price, deal end and stock units each in its own currency | 3 |

## Storefronts

`country` picks the storefront (default `us`); `language` picks its language where it has several (default: the first listed). Every answer except prices carries `market` {`country`, `language`, `currency`, `host`}, and text comes in the storefront language.

| country | host | currency | languages |
|---|---|---|---|
| `us` | www.vevor.com | USD | en, es |
| `ca` | www.vevor.ca | CAD | en, fr |
| `gb` | www.vevor.co.uk | GBP | en |
| `au` | www.vevor.com.au | AUD | en |
| `de` | www.vevor.de | EUR | de |
| `fr` | www.vevor.fr | EUR | fr |
| `es` | www.vevor.es | EUR | es |
| `it` | www.vevor.it | EUR | it |
| `nl` | www.vevor.nl | EUR | nl |
| `pl` | www.vevor.pl | PLN | pl |
| `mx` | www.vevor.mx | MXN | es |
| `no` | www.vevor.co.no | EUR | no |
| `eu` | eur.vevor.com (Vevor's storefront for the other European countries) | EUR | en, sv, da, fi, no, pt, cs, el, sk, hu, ro |

`uk` is a `400` pointing to `gb`; any other country or a language the storefront does not offer is a `400`, not charged. A product link sent as `url` must belong to the storefront asked.

## Prices, deals, stock and variants

Every priced item, product, variant and storefront row carries:

| Field | Meaning |
|---|---|
| `price` | Vevor's price on that storefront for a visitor without an account, in `currency` |
| `was_price` | Vevor's list price, given only while a Vevor deal is active or where Vevor's page shows its own strikethrough price; otherwise `null` |
| `deal` | Lists: `true` while a Vevor deal is active. Product: {`starts`, `ends` (ISO 8601 UTC, as Vevor gives them), `quantity` (units Vevor puts on the deal), `claimed` (Vevor's count of deal units taken), `percent_left` (computed by Scavio from the two)}, `null` without an active deal |
| `deal_ends`, `deal_progress` | Lists and variants: the deal's end as Vevor gives it, and Vevor's own progress text ("88% Left", "100% Kvar") |
| `stock_units`, `in_stock` | Vevor's own unit count for that storefront (`0` = out of stock) |
| `labels` | Vevor's badges as given ("Black Friday", "Deals", "AUSVERKAUF") |
| `rating`, `review_count` | On list items: Vevor's figures for the product family (all its variants) |

- **Per storefront:** "182.22 USD on www.vevor.com on 2026-11-25, was 219.90 during Vevor's deal ending 2026-11-30T07:59:59Z as Vevor gives it". Never state a price without its storefront and date.
- **Across storefronts:** `/prices` with one `sku` asks all 13 storefronts. Each row is in its own currency; convert only with a dated rate you state. The European storefronts de, fr, es, it, nl, pl and eu were measured sharing one stock pool (the surface cleaner read 709 units on each); vevor.co.no counts its own (614).
- **Variants:** `/product` `variants[]` {`sku`, `attributes`, `price`, `was_price`, `deal_ends`, `stock_units`, `sold`, `url`} are the SKUs Vevor's option selector links from the page, each with its own price and stock; a variant can be another product page (the MIG welder's variants ran from a 77.90 USD 130A welder to a 1,599.90 USD 200A 9-in-1 welder with a welding cart).
- **Protection plans:** `protection_plans[]` {`years`, `name`, `price`, `currency`} as Vevor offers them (1, 2 and 3 years at 21.11, 30.78 and 35.18 USD on the MIG welder).
- Report Vevor's numbers and the arithmetic only. Never call a price a bargain, a rise or a cut, never describe how often an item is on deal, and never add urgency or countdown wording to a deal end.

## Workflow

1. **Find the item.** `/search` with `q` (keywords in the storefront language, or a SKU) and `country`, or `/category` with a `categories[].id`, `/collections` or `/deals`. Each item's `sku` is the input of product, shipping, reviews, questions and prices.
2. **Read it in full.** `/product` with `sku` (or `url`, an `items[].url` link) on the same storefront: price, was price, deal window, stock, every variant.
3. **Compare storefronts.** `/prices` with the `sku` (3 credits): every storefront's status, price, was price, deal end and stock. Or `/product` with another `country`.
4. **Shipping.** `/shipping` with `sku` and, in the US, `state` (`NY`), in Canada `province` (`ON`); optional `zip` and `city`. Outside the US and Canada send `zip` (the postcode) only.
5. **Narrow a list.** `sort` (`popular`, `price_low`, `price_high`, `hot`, `new`), the filters (`in_stock`, `on_sale`, `black_friday`, `bulk_savings`, `pickup` in the US, `min_price`, `max_price` in the storefront currency, `rating`), `category` on search, and `page` (1-50, 60 per page).
6. **Reviews and questions.** `/reviews` with `sku`: `sort`, `rating` (1-5), `photos_only`, `this_variant_only`, `page`, `page_size` (1-100, default 20). `/questions` with `sku` and `page` (5 per page).
7. **Compare channels.** Search the same VEVOR model on `amazon-product-data`, `walmart-product-data`, `home-depot-product-data`, `tractor-supply-prices-api`, `tiktok-shop-api` or `ebay-product-data`; keep a row only where the listing carries the same model number or SKU.
8. **Watching prices:** there is no history. Poll the same SKUs on the same storefronts on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Every endpoint except prices

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `us` | A storefront code (see Storefronts) |
| `language` | string | the storefront's first | A language that storefront offers |

### Search (`/search`) and category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | search: required | Keywords in the storefront language, or a Vevor SKU (1-200 chars) |
| `category` | string or integer | category: required | `categories[].id` (`40035`, Ice Makers) or a Vevor category link; on search an optional filter |
| `sort` | string | `popular` | `popular` (Vevor's own order), `price_low`, `price_high`, `hot`, `new` |
| `page` | integer | 1 | 1-50, 60 items per page |
| `in_stock`, `on_sale`, `black_friday`, `bulk_savings` | boolean | false | Vevor's own filters (`black_friday` while Vevor runs it) |
| `pickup` | boolean | false | Items Vevor offers for pickup, `country` `us` only |
| `min_price`, `max_price` | number | none | In the storefront's currency |
| `rating` | string | none | `highly_rated` (4 stars and up) or `best_rated` (5 stars) |

### Product (`/product`), shipping (`/shipping`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | product: one of; shipping: required | A Vevor SKU (`items[].sku`, `DHJMIGMMAMIGLL6WNV5`) |
| `url` | string | product: one of | A Vevor product link on the storefront asked (`items[].url`) |
| `state` | string | shipping, `us`: required | A two-letter US state (`NY`) |
| `province` | string | shipping, `ca`: required | A two-letter Canadian province (`ON`) |
| `zip` | string | none | Shipping: a US ZIP, a Canadian postal code or a postcode |
| `city` | string | none | Shipping: the city |

### Reviews (`/reviews`), questions (`/questions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | required | A Vevor SKU |
| `sort` | string | `recommended` | Reviews: `recommended` (Vevor's own order), `newest`, `helpful` |
| `rating` | integer | none | Reviews: 1-5 stars only |
| `photos_only` | boolean | false | Reviews: only reviews with photos or videos |
| `this_variant_only` | boolean | false | Reviews: only reviews of this exact SKU |
| `page`, `page_size` | integer | 1, 20 | Reviews: page 1-500, 1-100 per page; questions: page 1-200, 5 per page |

### Suggestions, categories, collections, deals, prices

`/suggestions` takes `q` (the typed text, in the storefront language). `/categories` takes an optional `category` (`categories[].id` or a category link: its sub-categories; without it every department). `/collections` takes `type` (`best_sellers`, default; `new`; `promotion` with `url`, a `/promotion/<name>-special-<id>.html` link and nothing else), `category` (with `best_sellers` only), `sort` and `page`. `/deals` takes `type` (`daily_deals`, default; `clearance`; `deals`), `category`, `sort` and `page`. `/prices` takes `sku` only (no `country` or `language`: it asks every storefront).

## Examples

### One product with its deal and variants

```bash
curl -X POST https://api.scavio.dev/api/v1/vevor/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "DHJMIGMMAMIGLL6WNV5"}'
```

Captured `data` (2026-11-25 UTC; `variants` cut to 2 of 9, `specs` to 3 of 9, `categories` to 2 of 4, `ai_questions`, `images`, `rating_breakdown` and `notes` dropped):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "host": "www.vevor.com" },
  "requested_sku": "DHJMIGMMAMIGLL6WNV5",
  "sku": "DHJMIGMMAMIGLL6WNV5",
  "spu": "06874",
  "web_id": "010752182768",
  "name": "VEVOR MIG Welder, 3 in 1 Welder Welding Machine, 270 Amp MIG Lift TIG Arc Welder 110V 220V Lift TIG Welder Lift ARC Welder Digital Display Combo Welding Machine MMA Stick IGBT DC Inverter Welder",
  "url": "https://www.vevor.com/multi-function-welder-c_10062/vevor-mig-welder-welding-machine-270a-mig-mma-tig-3-in-1-welder-combo-110v-220v-p_010752182768",
  "price": 182.22,
  "was_price": 219.9,
  "currency": "USD",
  "deal": { "starts": "2026-11-14T08:00:01.000Z", "ends": "2026-11-30T07:59:59.000Z", "quantity": 421, "claimed": 49, "percent_left": 88 },
  "stock_units": 507,
  "in_stock": true,
  "availability": "in_stock",
  "labels": ["Black Friday"],
  "attributes": { "Function": "3-in-1", "Output": "270A" },
  "variants": [
    { "sku": "MIGYXHJ3H113QH258V1", "attributes": { "Output": "135A" }, "price": 93.42, "was_price": 109.9, "deal_ends": "2026-11-30T07:59:59.000Z", "stock_units": 194, "sold": true, "url": "https://www.vevor.com/mig-welder-c_10053/mig-welder-130amp-mig-welding-machine-3-in-1-flux-core-mig-stick-lift-tig-welder-p_010143935529" },
    { "sku": "MIGHJ160A4H111G9P001V5", "attributes": { "Output": "160A" }, "price": 143.9, "was_price": null, "deal_ends": null, "stock_units": 0, "sold": true, "url": "https://www.vevor.com/mig-welders-c_44033/vevor-160a-mig-welder-4-in-1-gas-mig-flux-core-mig-lift-tig-stick-welding-multi-process-110-220v-synergic-mig-welder-machine-2t-4t-mode-igbt-inverter-digital-display-for-metalworking-diy-repair-p_010522936066" }
  ],
  "specs": [
    { "name": "Model", "value": "MIG-270" },
    { "name": "Welder Type", "value": "MIG/MMA/TIG" },
    { "name": "Voltage", "value": "110V/220V" }
  ],
  "description": "VEVOR Mig Welder offers advanced IGBT tech, 3-in-1 versatility, easy controls, and safety features in a compact, portable design for all your welding needs.",
  "protection_plans": [
    { "years": 1, "name": "1 Year", "price": 21.11, "currency": "USD" },
    { "years": 2, "name": "2 Years", "price": 30.78, "currency": "USD" },
    { "years": 3, "name": "3 Years", "price": 35.18, "currency": "USD" }
  ],
  "return_policy": { "days": 30, "free_returns": true, "method": "by mail" },
  "rating": 4.63,
  "review_count": 453,
  "ai_review_summary": "The Vevor welder is praised for its versatility, ease of use, and solid welding performance across various materials and methods, though minor issues like wire speed adjustment and accessory quality are noted.",
  "categories": [
    { "id": "40339", "name": "Welding & Soldering", "url": "https://www.vevor.com/welding-soldering-c_40339" },
    { "id": "44033", "name": "MIG Welders", "url": "https://www.vevor.com/mig-welders-c_44033" }
  ]
}
```

`was_price` 219.90 is there because the deal window is active; on the 160A variant, with no deal, it is `null`. `percent_left` 88 is Scavio's arithmetic from `quantity` and `claimed`. `ai_review_summary` (and `ai_questions`) are Vevor's own AI-written text as its page shows it: label them as Vevor's. An unknown SKU, or one this storefront does not sell, is a charged `404`.

### The same SKU on all 13 storefronts

```bash
curl -X POST https://api.scavio.dev/api/v1/vevor/prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "GYQXJBMQJQYPKEO1LV0"}'
```

Captured `data` (2026-11-25 UTC; 6 of 13 storefronts shown, `notes` dropped):

```json
{
  "sku": "GYQXJBMQJQYPKEO1LV0",
  "sold_in": 12,
  "storefronts": [
    { "country": "us", "host": "www.vevor.com", "currency": "USD", "status": "sold", "sold": true, "price": 195.01, "was_price": 209.9, "deal_ends": "2026-12-01T07:59:59.000Z", "stock_units": 594 },
    { "country": "ca", "host": "www.vevor.ca", "currency": "CAD", "status": "sold", "sold": true, "price": 233.9, "was_price": 266.9, "deal_ends": "2026-12-01T07:59:59.000Z", "stock_units": 137 },
    { "country": "gb", "host": "www.vevor.co.uk", "currency": "GBP", "status": "sold", "sold": true, "price": 175.9, "was_price": null, "deal_ends": null, "stock_units": 41 },
    { "country": "de", "host": "www.vevor.de", "currency": "EUR", "status": "sold", "sold": true, "price": 170.9, "was_price": 190.9, "deal_ends": "2026-12-01T07:00:00.000Z", "stock_units": 709 },
    { "country": "mx", "host": "www.vevor.mx", "currency": "MXN", "status": "not_sold", "sold": false, "price": null, "was_price": null, "deal_ends": null, "stock_units": null },
    { "country": "no", "host": "www.vevor.co.no", "currency": "EUR", "status": "sold", "sold": true, "price": 261.99, "was_price": null, "deal_ends": null, "stock_units": 614 }
  ]
}
```

The other rows: au 333.90 AUD (no deal, 0 units), fr 175.90, es 177.90, it 178.90, nl 173.90 and eu 181.90 EUR, pl 721.90 PLN, all with a deal ending `2026-12-01T07:00:00.000Z` and 709 units (the shared European pool). Each row is in its own currency, with no conversion. `status` `unavailable` means that storefront did not answer; `credits_used` counts the storefronts that answered (3 when all 13 do). A SKU no storefront sells is a charged `404`.

### Shipping to a state

```bash
curl -X POST https://api.scavio.dev/api/v1/vevor/shipping \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "DHJMIGMMAMIGLL6WNV5", "state": "AK", "zip": "99501"}'
```

Captured `data` (2026-11-25 UTC; `notes` dropped):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "host": "www.vevor.com" },
  "sku": "DHJMIGMMAMIGLL6WNV5",
  "destination": { "country": "us", "state": "AK", "zip": "99501", "city": null },
  "fee": 130,
  "currency": "USD",
  "free_shipping": false,
  "delivery": { "earliest": "2026-11-29T06:29:11.000Z", "latest": "2026-11-29T06:29:11.000Z" },
  "can_order": true,
  "price": 182.22,
  "stock_units": 507
}
```

The state drives the fee and the date; `price` and `stock_units` are the same as on the product page (they do not change by ZIP or state). Vevor often gives one date for both `earliest` and `latest`. Vevor names no shipping method and no warehouse an order ships from.

### Reviews, search, lists and the rest

- `/reviews` `{"sku": "CKKMJ3300LBSAPPKZV1"}` (a gate opener): `rating` 4.38, `review_count` 257, `rating_breakdown` with counts (177 five-star, 20 one-star), `total` 257, 13 pages of 20, `recommended` order. Each review: `id`, `rating`, `title`, `text`, `date`, `language`, `country`, `sku`, `variant_attributes`, `photos_count`, `videos_count`, `helpful_votes` and `replies` (Vevor's replies). 18 of the first 20 were of other SKUs of the product: send `this_variant_only` for the exact SKU. No reviewer names; photos are counted, not linked.
- `/questions` `{"sku": "DHJMIGMMAMIGLL6WNV5"}`: `total` 166, 5 per page (34 pages); every answer on page 1 had `by_vevor` true ("Is the TIG AC or DC?" "It's AC."). No asker or answerer names.
- `/search` `{"q": "welder"}`: `total` 72, 60 per page, `last_page_shown` 2, the MIG welder first at 182.22 USD with `deal_ends` and `deal_progress` "88% Left". On `gb` the same word read 8 items; `{"q": "poste a souder", "country": "fr"}` read `total` `"100+"` with `total_is_lower_bound` true.
- `/category` `{"category": "40035"}` (Ice Makers): `total` `"100+"`, a 360 lbs commercial ice maker first at 1,199.90 USD (no deal, `was_price` null), a 265 lbs one second at 568.57 USD, was 668.90 during a deal ending `2026-12-01T07:59:59.000Z`.
- `/collections` `{}` (Best Sellers) and `/deals` `{}` (Daily Deals): `total` `"100+"`, 40 items on page 1, a 26-inch push lawn sweeper first on both at 104.31 USD, was 142.99, 43,954 units.
- `/categories` `{}`: 31 departments (Lawn & Garden, Tools, Automotive, ...), 1,377 categories in all; Tools (`40028`) holds Power Tools, Hand Tools, Welding & Soldering and 6 more. `id` is the input of category and of search's `category`.
- `/suggestions` `{"q": "ice"}`: 10 suggestions ("ice maker machine", "ice maker", "ice cream", ...), each with its search page `url`. No prices.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def vevor(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/vevor/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Search one storefront, in its language (1 credit)
hits = vevor("search", {"q": "welder", "sort": "price_low", "in_stock": True})["data"]
for i in hits["items"][:5]:
    # was_price is only set while a Vevor deal is active; never compute a discount without it.
    print(i["sku"], i["price"], i["currency"], "was", i["was_price"], "deal ends", i["deal_ends"], "units", i["stock_units"])
print("total", hits["total"], "lower bound" if hits["total_is_lower_bound"] else "exact")

# 2. The same SKU on every storefront (3 credits)
p = vevor("prices", {"sku": "GYQXJBMQJQYPKEO1LV0"})["data"]
for s in p["storefronts"]:
    print(s["country"], s["host"], s["status"], s["price"], s["currency"], s["was_price"], s["stock_units"])

# 3. Shipping to a US state (1 credit)
ship = vevor("shipping", {"sku": "DHJMIGMMAMIGLL6WNV5", "state": "NY"})["data"]
print(ship["fee"], ship["currency"], ship["free_shipping"], ship["delivery"])

# Prices and units can change between calls. Store each answer with fetched_at
# and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` except prices carries `market` {`country`, `language`, `currency`, `host`}, and most carry `notes`.

- **item** (search, category, collections, deals) - `position`, `sku`, `spu`, `name`, `url`, `image`, `price`, `was_price`, `currency`, `stock_units`, `in_stock`, `deal`, `deal_ends`, `deal_progress`, `labels`, `rating`, `review_count`; New Arrivals items add `first_listed`.
- **lists** - `page`, `page_size` (60), `total` (a number, or `"100+"`), `total_is_lower_bound`, `last_page_shown`, `has_more`, `count`, `sort`, `filters_applied`, `items[]`; search adds `query`, `category`; category `category_id`, `title`; collections and deals `type`, `category` (or `url`).
- **product** - `requested_sku`, `sku`, `spu`, `web_id`, `name`, `url`, `price`, `was_price`, `currency`, `deal` {`starts`, `ends`, `quantity`, `claimed`, `percent_left`}, `stock_units`, `in_stock`, `availability`, `labels`, `attributes`, `variants[]` {`sku`, `attributes`, `price`, `was_price`, `deal_ends`, `stock_units`, `sold`, `url`}, `specs[]` {`name`, `value`}, `images`, `description`, `protection_plans[]` {`years`, `name`, `price`, `currency`}, `return_policy` {`days`, `free_returns`, `method`}, `rating`, `review_count`, `rating_breakdown[]` {`stars`, `percent`}, `ai_review_summary`, `ai_questions[]` {`question`, `answer`}, `categories[]` {`id`, `name`, `url`}.
- **shipping** - `sku`, `destination` {`country`, `state`, `zip`, `city`}, `fee`, `currency`, `free_shipping`, `delivery` {`earliest`, `latest`}, `can_order`, `price`, `stock_units`.
- **reviews** - `sku`, `rating`, `review_count`, `rating_breakdown[]` {`stars`, `count`, `percent`}, `total`, `page`, `page_size`, `total_pages`, `has_more`, `sort`, `filters_applied`, `count`, `reviews[]` {`id`, `rating`, `title`, `text`, `date`, `language`, `country`, `sku`, `variant_attributes[]` {`name`, `value`}, `photos_count`, `videos_count`, `helpful_votes`, `replies[]` {`text`, `date`}}.
- **questions** - `sku`, `total`, `page`, `page_size`, `total_pages`, `has_more`, `count`, `questions[]` {`id`, `question`, `date`, `votes`, `answers[]` {`text`, `date`, `by_vevor`, `votes`}}.
- **suggestions** - `query`, `count`, `suggestions[]` {`term`, `url`}.
- **categories** - `category`, `parents`, `count`, `total_categories`, `categories[]` {`id`, `name`, `url`, `children[]`}.
- **prices** - `sku`, `sold_in`, `storefronts[]` {`country`, `host`, `currency`, `status` (`sold`, `not_sold`, `unavailable`), `sold`, `price`, `was_price`, `deal_ends`, `stock_units`}.

## Guardrails

- Name it "VEVOR (vevor.com, the tools and equipment seller with storefronts in 13 countries)" on first mention, "Vevor" after that.
- Prices: quote `price` with its storefront, `currency` and the `fetched_at` date. Never present one storefront's price as Vevor's price everywhere, and never say the price changes by ZIP or state (shipping does).
- Was price: quote `was_price` only as given, with the deal's start and end as Vevor gives them. Never compute a discount from anything else, never add urgency or countdown wording, and never describe how often an item is on deal.
- Coupons: no answer carries coupon codes or a price after a code; never apply or invent one.
- Same item only: compare Vevor's price with Amazon, Walmart, Home Depot, Tractor Supply, TikTok Shop or eBay only where the listing carries the same VEVOR model number or SKU, each price with its seller, retailer and date. Harbor Freight is an alternative store, never the same item. Never call one channel cheaper beyond the numbers shown.
- Descriptive only: never discuss recalls, safety, product quality or legitimacy verdicts, tariffs, price trends or why prices differ.
- Stock: `stock_units` as Vevor reported it at the moment of the call; Scavio makes no promise of its accuracy. Never promise a delivery date beyond Vevor's own answer.
- AI text: `ai_review_summary` and `ai_questions` are Vevor's own AI-written text; label them as Vevor's, never as Scavio's analysis.
- Reviews and questions: no reviewer, asker or answerer names are returned. Do not republish Vevor product photos or logos; link products by `url` instead.
- Terms: Scavio does not collect or store Vevor data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Vevor's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, units, SKUs, category ids, dates or ratings. Only return what the API returned, with the `fetched_at` time and the product `url`.
- Not available: coupon codes, the pickup store, Pro or bulk prices, financing, the warehouse an order ships from, Vevor's listings on other marketplaces (use those platforms' skills), price history (poll and store), cart or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` outside the 13 storefronts (`uk` points to `gb`) or a `language` the storefront does not offer; `prices` with `country` or `language`; a SKU that is not letters and digits; product without `sku` or `url`, or a link from another storefront; shipping in the US without `state` or in Canada without `province`, or `state` / `province` on another storefront; a malformed ZIP or postal code; category without `category`; `pickup` outside `us`; `min_price` above `max_price`; filters on an endpoint that takes none; collections `promotion` without `url` or with `category`, `page` or `sort`, `url` with another type, or `category` with `new`; `q` without letters or digits; an unknown `sort`, `rating` or `type`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "VEVOR does not sell SKU <sku> on <host> (items[].sku from search on this storefront; prices lists the storefronts that sell it).", "VEVOR has no category <id> on <host> (categories lists them).", "VEVOR has no product page <path> on <host>.", "VEVOR has no promotion page <path> on <host>.", "No VEVOR storefront sells SKU <sku> (items[].sku).". Take SKUs and category ids from a previous answer on the same storefront rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api).
- `502` means Vevor data was temporarily unavailable ("VEVOR is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Vevor is busy ("VEVOR is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.86.0
npm install scavio@0.87.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.vevor.search({ q: "welder" });
const { data: de } = await scavio.vevor.search({ q: "schweissgeraet", country: "de" });
const { data: welder } = await scavio.vevor.product({ sku: "DHJMIGMMAMIGLL6WNV5" });
const { data: ship } = await scavio.vevor.shipping({ sku: "DHJMIGMMAMIGLL6WNV5", state: "AK", zip: "99501" });
const { data: reviews } = await scavio.vevor.reviews({ sku: "CKKMJ3300LBSAPPKZV1", this_variant_only: true });
const { data: questions } = await scavio.vevor.questions({ sku: "DHJMIGMMAMIGLL6WNV5" });
const { data: suggest } = await scavio.vevor.suggestions({ q: "ice" });
const { data: tree } = await scavio.vevor.categories();
const { data: iceMakers } = await scavio.vevor.category({ category: "40035" });
const { data: best } = await scavio.vevor.collections({ type: "best_sellers" });
const { data: deals } = await scavio.vevor.deals({ type: "daily_deals" });
const { data: everywhere } = await scavio.vevor.prices({ sku: "GYQXJBMQJQYPKEO1LV0" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.vevor.search(...)`, `product`, `shipping`, `reviews`, `questions`, `suggestions`, `categories`, `category`, `collections`, `deals` and `prices`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `search_vevor`, `get_vevor_product`, `get_vevor_shipping`, `get_vevor_reviews`, `get_vevor_questions`, `get_vevor_suggestions`, `get_vevor_categories`, `get_vevor_category`, `get_vevor_collections`, `get_vevor_deals` and `get_vevor_prices`. Vevor is opt-in: add `vevor` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.86.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,vevor"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/vevor-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api), [product](https://scavio.dev/docs/vevor-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api), [shipping](https://scavio.dev/docs/vevor-shipping?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api), [reviews](https://scavio.dev/docs/vevor-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api), [questions](https://scavio.dev/docs/vevor-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api), [suggestions](https://scavio.dev/docs/vevor-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api), [categories](https://scavio.dev/docs/vevor-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api), [category](https://scavio.dev/docs/vevor-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api), [collections](https://scavio.dev/docs/vevor-collections?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api), [deals](https://scavio.dev/docs/vevor-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api), [prices](https://scavio.dev/docs/vevor-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api). Overview: [Vevor API](https://scavio.dev/vevor-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=vevor-api).
