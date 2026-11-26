---
name: loblaws-grocery-prices-api
description: Loblaws grocery prices API for PC Express (Loblaw's online grocery for Real Canadian Superstore, No Frills, Loblaws, Zehrs, Fortinos, Valu-mart, Your Independent Grocer, Wholesale Club, Provigo and Maxi; Loblaw operates 2,504 stores per its 2025 annual report) - what each Loblaw banner charges for the same product code at its default online store on one date, in Canadian dollars, with the deal, its end date and the PC Optimum points offer as PC Express shows them (No Name Large Size Eggs 12 Pack, code 20812144001_EA, read 3.93 at Real Canadian Superstore store 1033 and No Frills store 3787 and 4.17 at Maxi store 8976 on Nov 26, 2026); keyword search, any category and any collection (deals-centre, black-friday, no-name ...), 48 a page with total and pages, five sorts and the site's filters (brand incl. No Name and President's Choice, price reduction, PC Optimum points, multi-buy, member-only price, $1-$5, price band, Prepared in Canada, dietary) with counts; each item with price, was price, unit price, deal type, text, deal price and expiry date, PC Optimum points, the member-only price PC Express shows publicly, stock status, rating, review count and the sponsored flag; one product with GTIN, ingredients, nutrition, comparison prices and stock status; each banner's pickup stores by city, postal code start, province or nearest a point; one store with 7 dated days of store, pharmacy and optical hours plus clinic hours; search suggestions. Every price is the banner's default online store, named in every answer (choosing a store is not offered). English, or French on Provigo and Maxi. 7 endpoints - search, category, collection, stores and suggestions 1 credit; product 5 (1 when answered from the search listing); store 5. Not available - choosing a store, review text, the flyer, Shoppers Drug Mart, Atlantic Superstore, City Market, T&T, PC Optimum login prices, deal start dates, price history, cart or checkout.
version: 1.0.0
tags: loblaws, loblaws-api, loblaws-grocery-prices, loblaw, loblaw-banners, pc-express, pc-express-api, pcexpress, real-canadian-superstore, superstore, superstore-api, superstore-prices, no-frills, no-frills-api, no-frills-prices, zehrs, fortinos, valu-mart, your-independent-grocer, wholesale-club, provigo, maxi, pc-optimum, pc-optimum-points, no-name, presidents-choice, grocery, grocery-prices, grocery-price-api, canadian-grocery-prices, canada, cad, french, quebec, unit-price, grocery-deals, store-locator, nutrition, gtin, price-comparison, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/pcexpress-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=loblaws-grocery-prices-api
---

# Loblaws Grocery Prices API - Superstore, No Frills, Maxi, Deals, PC Express

Read PC Express (Loblaw's online grocery for Real Canadian Superstore, No Frills, Loblaws, Zehrs, Fortinos, Valu-mart, Your Independent Grocer, Wholesale Club, Provigo and Maxi; Loblaw operates 2,504 stores per its 2025 annual report): keyword search, any category, any collection (the deals centre, Black Friday, No Name ...), one product in full, each banner's pickup stores, one store's hours and the search suggestions. Every answer is what the banner's public PC Express pages show a visitor without an account at the moment of the call, priced at the banner's default online store, in Canadian dollars, in English (French on Provigo and Maxi). All 7 endpoints return structured JSON at 1 or 5 credits per call.

**Read-only data.** This skill reads the public pages PC Express shows to any visitor and returns them as JSON for analysis. It uses no PC Optimum account, no login, no cart and no checkout.

**The job this skill is for: what each Loblaw banner charges for the same product code on one date.** PC Express uses one product code for an item on every banner, so the same code can be priced side by side, each at the banner's default online store, with the deal end date and the PC Optimum offer as shown; then Walmart.ca alongside for the national brands. Captured 2026-11-26 with `/search` (`eggs` on `superstore` and `nofrills`, `oeufs` on `maxi` in French; 1 credit each), the same codes on three banners:

| Code | Product | Real Canadian Superstore (store 1033) | No Frills (store 3787) | Maxi (store 8976) |
|---|---|---|---|---|
| 20812144001_EA | No Name Large Size Eggs 12 Pack | 3.93 | 3.93 | 4.17 |
| 20813386001_EA | No Name Medium Size Eggs 12 Pack | 3.79 | 3.79 | 4.11 |
| 20812726001_EA | No Name Extra Large Size Eggs 12 Pack | 4.69 | 4.71 | 4.71 |
| 21205224001_EA | PC Organics Free-Range Large Brown Eggs, 30 | 16.84 | 17.50 | 17.50 |
| 20813628001_EA | President's Choice Free Run Brown Eggs Large, 12 | 6.50, was 7.00, deal ends 2027-01-06 | 6.50, was 7.18, deal ends 2026-12-02 | not in the capture |
| 21623323_EA | Schneiders Egg with Bacon & Cheddar Breakfast Bites, 224 g | 6.50, was 7.49, ends 2026-12-02 | 5.50, was 7.50, ends 2026-12-02 | 5.50, was 7.50, ends 2026-12-09 |

The same code carried different prices, different was prices and different deal end dates by banner. Report each price with its banner, the store number from `store`, the date and "before tax". Then read the national brands (Burnbrae Farms, Schneiders, Kellogg's ...) on Walmart.ca with `walmart-product-data` (`domain: "ca"`), matched on the GTIN from `/product` or on brand, name and size. No Name, President's Choice, PC Organics and PC Blue Menu are Loblaw's own brands: compare them across Loblaw banners, not with Walmart.ca.

Eleven limits shape every answer, so say them plainly:
- **Credits depend on the endpoint.** search, category, collection, stores and suggestions 1; product 5, or 1 when it is answered from the search listing (`source` `search`); store 5. `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Prices are the banner's default online store.** Every priced answer carries `store` {`store_id`, `banner`, `requested` false}: the store PC Express priced the page at (in the captures 1033 for Real Canadian Superstore, 3787 for No Frills, 8976 for Maxi). Choosing a store is not offered: a `store_id` on a priced endpoint is a `400`, not charged. Prices can differ by store, so never present a default-store price as the price at another store, and always report the store number with the price.
- **Store ids do not change prices.** `/stores` and `/store` list each banner's pickup stores and hours. Their `store_id` is for locating and hours, not an input to search, category, collection or product.
- **Deals end dates, no start dates.** `deal` {`type` (`sale`, `limit`, `multi`), `name`, `text`, `deal_price`, `points`, `expiry_date`} is the deal as PC Express words it ("SAVE $0.50", "Limit 6, after limit $4.00") with the end date it shows. PC Express shows no start date: never infer one, and never compute when a price will change.
- **PC Optimum points as given.** `pc_optimum_points` is the points offer in PC Express's words ("500 PC Optimum Points"). Quote it; do not convert it to dollars.
- **member_only_price is public.** It is the PC Optimum member price PC Express shows publicly on the item. Prices behind a member login are not offered.
- **Unit prices are text.** `unit_price` is PC Express's own string in the site's language ("$0.33/1ea" on Superstore, "0,35 $/1ch" on Maxi in French); `/product` adds `comparison_prices` [{`price`, `per`}] as numbers. Compare unit prices only on the same `per`.
- **stock_status on lists is often null.** On search, category and collection, `stock_status` is `out_of_stock` or `low_stock` when PC Express shows it and `null` when it shows nothing: unknown, not in stock. On `/product` it is PC Express's own wording (`ok` = shown as available).
- **Sponsored items are mixed in.** `sponsored` true marks the paid placements in a list (`sponsored_count`); `total` and paging count the organic results. Leave sponsored items out of a banner comparison unless the same code is also organic.
- **French on Provigo and Maxi.** Provigo serves French; Maxi French by default and English too. The other eight banners serve English: `language: "fr"` there is a `400`. French answers carry French names, deal text and unit prices with the same codes and CAD prices.
- **What is not there.** No store choice, no review text (`rating` and `review_count` only), no printed flyer, no Shoppers Drug Mart, no Atlantic Superstore, City Market or T&T (not in this build), no PC Optimum login prices, no deal start dates, no price history (store your own answers with `fetched_at`), no cart or checkout.

PC Express publishes no public API for its catalog or prices. This skill reads PC Express's public pages with one Scavio key. Other vendors offer Loblaw grocery data tools.

See also: `walmart-product-data` (Walmart.ca with `domain: "ca"`), `costco-product-data` (costco.ca with `country: "ca"`), `instacart-api` (Instacart Canada stores at a Canadian postal code; Instacart may label a store with its own text, such as "Item prices are higher than in-store prices", and that label is Instacart's) and `amazon-product-data` (Amazon.ca with `country: "ca"`). Same item only: match the GTIN, or brand, name and size; show each price with its retailer, store and date; flag marketplace sellers on Amazon.ca and Walmart.ca rather than treating them as Amazon or Walmart.

## When to trigger

Use this skill when the user asks to:
- Compare what Real Canadian Superstore, No Frills, Loblaws, Maxi or another Loblaw banner charges for the same product code on one date
- Read Loblaw banner deals with their end dates and PC Optimum points offers, or a collection such as the deals centre or Black Friday
- Search a Loblaw banner or browse a category, sorted by price and filtered by brand (No Name, President's Choice), deals, price band, Prepared in Canada or dietary labels
- Read one product with GTIN, ingredients, nutrition, comparison prices and stock status
- Find a banner's pickup stores by city, postal code start, province or nearest a point, or read one store's store, pharmacy and optical hours
- Read the search suggestions a banner shows for a term
- Put Loblaw banner prices next to Walmart.ca, Costco Canada or Instacart Canada for the same national brand

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=loblaws-grocery-prices-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=loblaws-grocery-prices-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Calls in this skill cost 1 or 5 credits, so 50 credits cover 50 searches (one banner each) or 10 product calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, category answered in about 2 seconds, search in 4-6, collection 6, stores 33, store 54, product 71 and suggestions 118. Search, category and collection can take up to about a minute; allow up to 2 minutes for product, store, stores and suggestions, set a client timeout of at least 240 seconds so a slow answer is not cut off, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/pcexpress/search` | Products for keywords or an article number: price, was price, unit price, deal and expiry date, PC Optimum points, member-only price, stock status, rating, review count, sponsored flag; total, pages, sorts, filters, facets with counts on request; `redirected_to` when PC Express sends the term to a collection or category | 1 |
| `POST /api/v1/pcexpress/category` | One category by id or link, same items, paging, sorts and filters; a department page lists its products in sections and its sub-categories in `category.children` | 1 |
| `POST /api/v1/pcexpress/collection` | One collection page (deals-centre, black-friday, no-name, pc-value, new-arrivals ...): products in sections, plus a paged list when the page has one | 1 |
| `POST /api/v1/pcexpress/product` | One product by code or link: GTIN, description, size, breadcrumbs, price, was price, member-only price, comparison prices, unit price, deal, promotions, deposit, stock status, ingredients, nutrition, variants | 5; 1 when answered from the search listing |
| `POST /api/v1/pcexpress/stores` | One banner's pickup stores: address, postal code, coordinates, phone, today's hours, minimum order, departments; filtered by city, postal code start or province, or nearest a point | 1 |
| `POST /api/v1/pcexpress/store` | One store: every stores field plus store, pharmacy, optical and holiday hours (7 dated days each), medical clinic hours by weekday, store and pharmacy phones and services | 5 |
| `POST /api/v1/pcexpress/suggestions` | The search terms a banner suggests for what a shopper typed | 1 |

## Banners and market

Canada, CAD: every answer carries `market` {`country` "ca", `currency` "CAD", `language`}. There is no `country` input. Pick the banner with `banner` (default `superstore`); the same product codes are used on every banner.

| `banner` | Banner | `language` |
|---|---|---|
| `superstore` (default) | Real Canadian Superstore | `en` |
| `nofrills` | No Frills | `en` |
| `loblaw` | Loblaws | `en` |
| `zehrs` | Zehrs | `en` |
| `fortinos` | Fortinos | `en` |
| `valumart` | Valu-mart | `en` |
| `independent` | Your Independent Grocer | `en` |
| `wholesaleclub` | Real Canadian Wholesale Club | `en` |
| `provigo` | Provigo | `fr` |
| `maxi` | Maxi | `fr` (default) or `en` |

Domains are given as plain text: realcanadiansuperstore.ca, nofrills.ca, loblaws.ca, zehrs.ca, fortinos.ca, valumart.ca, yourindependentgrocer.ca, wholesaleclub.ca, provigo.ca, maxi.ca. A product `url` from any of them sets its banner; a `banner` that names a different site is a `400`.

## Prices, deals and stores

| Field | Meaning |
|---|---|
| `price` | PC Express's price at the banner's default online store, CAD, before tax |
| `was_price` | The regular price PC Express shows next to a reduced price, `null` without one |
| `price_text` | The price as PC Express prints it ("$3.93", "4,17 $") |
| `unit_price` | PC Express's unit price string in the site's language ("$0.33/1ea") |
| `comparison_prices` (product) | The unit prices as numbers: [{`price`, `per`}] ({0.33, "1ea"}) |
| `deal` | {`type` (`sale`, `limit`, `multi`), `name`, `text`, `deal_price`, `points`, `expiry_date`}: the deal in PC Express's words and the end date it shows; no start date exists |
| `pc_optimum_points` | The PC Optimum points offer as PC Express words it ("500 PC Optimum Points") |
| `member_only_price` | The PC Optimum member price PC Express shows publicly on the item |
| `stock_status`, `stock_text` | `out_of_stock` / "Out of Stock", `low_stock` / "Low Stock" on lists (`null` = not shown, unknown); `ok` on product = shown as available |
| `sponsored` | A paid placement in the list; `total` and paging count organic results |
| `store` | {`store_id`, `banner`, `requested`}: the store the answer is priced at; `requested` is always false |
| `tax_note` | PC Express's tax wording when it shows one ("Plus tax") |
| `min_quantity`, `max_quantity`, `sold_by`, `weighted` | The order limits and how the item is sold (`each` or by weight) |

- **Percent off:** compute it from `price` and `was_price` and label it computed (6.50 against 7.18 is 9.5% off, computed).
- **Codes:** `code` is PC Express's product code (article number and unit, `20812144001_EA`) and the input of `/product`. Send it as a string.
- **Store ids:** `store_id` from `/stores` is a string; leading zeros count (`"0559"`).

## Workflow

1. **Find the codes.** `/search` with `query` on one banner (add `include_facets: true` on the first call), or `/category` / `/collection`. Note each `code`, `brand`, `name` and `size`, and skip `sponsored` items.
2. **Price them per banner.** Repeat the search on each banner you need (`banner: "nofrills"`, `"loblaw"`, `"maxi"` ...), 1 credit each, and match on `code`. Read `price`, `was_price`, `unit_price`, `deal` (with `expiry_date`) and `pc_optimum_points`, and note `store.store_id`.
3. **Detail when needed.** `/product` with `code` and `banner` for GTIN, ingredients, nutrition and `comparison_prices` (5 credits; `source` `search` answers at 1 credit without GTIN, ingredients or nutrition).
4. **Match elsewhere.** National brands: `walmart-product-data` with `domain: "ca"`, matched on GTIN or brand, name and size. Skip any row that does not match.
5. **Report.** Each price with its banner, the default store number from `store`, CAD, the capture date and "before tax"; deals with their end date as shown and no start date; PC Optimum offers as given; a percent off labelled computed.
6. **Stores.** `/stores` with `banner` and `city`, `postal_code` (a start such as `"T5"` or `"M5V"`), `province`, or `latitude` + `longitude`; `/store` with `store_id` for 7 dated days of hours.
7. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`), category (`/category`) and collection (`/collection`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required (search) | Keywords or an article number, up to 200 chars |
| `category` | string or integer | required (category) | A category id (`"28224"` Milk & Cream, from `category.children`, `breadcrumbs` or a link's `/c/<id>`) or a category link / path |
| `collection` | string | required (collection) | A collection name from the site's links (`deals-centre`, `black-friday`, `no-name`, `pc-value`, `new-arrivals` ...) or a collection link |
| `page` | integer | 1 | Page number, 48 products a page; `total_pages` says how many |
| `sort` | string | `relevance` | `relevance`, `price_low_to_high`, `price_high_to_low`, `name_a_to_z`, `newest` |
| `brand` | string or list | none | Brand codes from `facets` (`productBrand`): `N` No Name, `P` President's Choice, `PO` PC Organics, `PCB` PC Blue Menu |
| `deals` | string or list | none | `price_reduction`, `pc_points`, `multi_buy`, `member_only_price`, `dollar_deals` ($1-$5) |
| `price_range` | string or list | none | Price bands from `facets` (`"$5-$10"`) |
| `prepared_in_canada` | boolean | false | Only products marked Prepared in Canada |
| `dietary` | string or list | none | Dietary codes from `facets` (`gluten_free`, `organic`, `vegan`, `lactose_free` ...) |
| `aisle` | string or list | none | Aisle (category) ids from `facets` |
| `filters` | list | none | Any other facet: [{`facet`, `value`}] from `facets[].facet` and `facets[].values[].value`; at most 10 filter values in all |
| `include_facets` | boolean | false | Also return `facets` [{`facet`, `name`, `multi_select`, `values` [{`value`, `name`, `count`, `selected`}]}] and `sorts` |
| `banner` | string | `superstore` | See the banner table |
| `language` | string | the banner's | `en`, or `fr` on `provigo` and `maxi` |

### Product (`/product`), stores (`/stores`), store (`/store`), suggestions (`/suggestions`)

| Endpoint | Parameters |
|---|---|
| `/product` | `code` (`"20812144001_EA"`) or `url` (a product link on any banner site, as `items[].url` gives it; not both), `banner`, `language` |
| `/stores` | `banner`, `city` (contains, accents and case ignored), `postal_code` (a start: `"T5"`, `"M5V"`, `"M5V 3L9"`), `province` (code or name), `latitude` + `longitude` (nearest first, with `distance_km`), `shoppable_only` (stores that take PC Express orders), `limit` 1-400 (default 20 near a point, else all), `language` |
| `/store` | `store_id` (required, a string from `/stores`), `banner`, `language` |
| `/suggestions` | `query` (required, up to 100 chars), `banner`, `language` |

## Examples

### Search one banner with facets

```bash
curl -X POST https://api.scavio.dev/api/v1/pcexpress/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "eggs", "include_facets": true}'
```

Captured `data` (2026-11-26; `items` cut to 2 of 50, `facets` to 1 of 6, `url`, `image`, `package_sizing`, `sorts` and `notes` dropped):

```json
{
  "banner": {"id": "superstore", "name": "Real Canadian Superstore"},
  "language": "en",
  "query": "eggs",
  "corrected_query": null,
  "redirected_to": null,
  "page": 1,
  "page_size": 48,
  "sort": "relevance",
  "sort_applied": true,
  "filters_applied": [],
  "total": 125,
  "total_pages": 3,
  "has_more": true,
  "count": 42,
  "sponsored_count": 8,
  "items": [
    {"code": "20812144001_EA", "article_number": "20812144001", "unit_of_measure": "EA", "name": "Large Size Eggs 12 Pack", "brand": "No Name", "size": "12 ea", "unit_price": "$0.33/1ea", "price": 3.93, "was_price": null, "price_text": "$3.93", "member_only_price": null, "tax_note": null, "sold_by": "each", "weighted": false, "min_quantity": 1, "max_quantity": 24, "deal": null, "pc_optimum_points": null, "badges": [], "stock_status": null, "stock_text": null, "rating": 4, "review_count": 4, "sponsored": false},
    {"code": "21479601_EA", "article_number": "21479601", "unit_of_measure": "EA", "name": "Egg Bites! Mini Crustless Quiches Snack Size", "brand": "Burnbrae Farms", "size": "336 g", "unit_price": "$2.23/100g", "price": 7.5, "was_price": 8, "price_text": "$7.50", "member_only_price": null, "tax_note": null, "sold_by": "each", "weighted": false, "min_quantity": 1, "max_quantity": 24, "deal": {"type": "sale", "name": "SALE", "text": "SAVE $0.50", "deal_price": null, "points": null, "expiry_date": "2026-12-02"}, "pc_optimum_points": "500 PC Optimum Points", "badges": ["Prepared in Canada"], "stock_status": null, "stock_text": null, "rating": null, "review_count": null, "sponsored": false}
  ],
  "store": {"store_id": "1033", "banner": "superstore", "requested": false},
  "facets": [
    {"facet": "promotions", "name": "Deals", "multi_select": true, "values": [{"value": "Price Reduction", "name": "Price Reduction", "count": 30, "selected": false}, {"value": "PC Points", "name": "PC Optimum Points", "count": 5, "selected": false}, {"value": "$1,$2,$3,$4,$5", "name": "$1,$2,$3,$4,$5", "count": 3, "selected": false}, {"value": "Multi-Buy", "name": "Multi-Buy", "count": 2, "selected": false}, {"value": "Member Only Price", "name": "Member Only Price", "count": 1, "selected": false}]}
  ],
  "market": {"country": "ca", "currency": "CAD", "language": "en"}
}
```

The 50 items held 8 sponsored ones (`count` 42 counts the organic). The 6 facets were Aisle, Brand (26 values), Deals, Price, Shop Canadian and Dietary & Lifestyle. The Egg Bites carried a sale ending 2026-12-02 and a 500 PC Optimum Points offer at the same time.

### The same search on No Frills and on Maxi in French

- `{"query": "eggs", "banner": "nofrills"}`: `store` 3787, `total` 100. No Name Large Size Eggs 12 Pack (20812144001_EA) at 3.93, "$0.33/1ea"; President's Choice Free Run Brown Eggs Large (20813628001_EA) at 6.50, `was_price` 7.18, `deal` "SAVE $0.68" ending 2026-12-02 (on Superstore the same code read 6.50, was 7.00, ending 2027-01-06).
- `{"query": "oeufs", "banner": "maxi", "language": "fr"}`: `store` 8976, `total` 116, French names and deal text. 20812144001_EA is "Lot de 12 œufs de calibre gros", brand "Sans Nom", at 4.17, `unit_price` "0,35 $/1ch", `price_text` "4,17 $"; deals read `name` "SPÉCIAL", `text` "2,00 $ DE RABAIS".

### One product

```bash
curl -X POST https://api.scavio.dev/api/v1/pcexpress/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "20812144001_EA"}'
```

Captured `data` (2026-11-26, 71 s; `description`, `url`, `images`, `breadcrumbs` (4), `nutrition.nutrients` cut to 3 of 12, `micronutrients` and `notes` dropped):

```json
{
  "banner": {"id": "superstore", "name": "Real Canadian Superstore"},
  "language": "en",
  "source": "page",
  "code": "20812144001_EA",
  "article_number": "20812144001",
  "unit_of_measure": "EA",
  "gtin": "00060383664145",
  "name": "Large Size Eggs 12 Pack",
  "brand": "No Name",
  "size": "12 ea",
  "price": 3.93,
  "price_unit": "ea",
  "was_price": null,
  "member_only_price": null,
  "comparison_prices": [{"price": 0.33, "per": "1ea"}],
  "unit_price": "$0.33/1ea",
  "price_type": "regular",
  "price_expiry_date": null,
  "deal_price": null,
  "deal": null,
  "promotions": [],
  "deposit": null,
  "stock_status": "ok",
  "shoppable": true,
  "sold_by": "each",
  "weighted": false,
  "min_quantity": 1,
  "max_quantity": 24,
  "badges": [],
  "ingredients": "Eggs.",
  "nutrition": {"serving_size": "105 g", "nutrients": [{"name": "calories", "amount": "160 cal", "daily_value": null}, {"name": "total_fat", "amount": "11 g", "daily_value": "15 %"}, {"name": "protein", "amount": "13 g", "daily_value": null}], "note": null},
  "variants": [],
  "store": {"store_id": "1033", "banner": "superstore", "requested": false},
  "market": {"country": "ca", "currency": "CAD", "language": "en"}
}
```

When the product page does not answer in time, the same call answers from the search listing for the article number with `source` `search` at 1 credit: price, deal, unit price and badges, with `gtin`, `ingredients` and `nutrition` `null`. Check `source` before reading those fields.

### Collection, category, stores, store, suggestions

- `/collection` `{"collection": "deals-centre", "banner": "nofrills"}`: Deals centre, `store` 3787, 8 sections (PC holiday picks $10 and under, Hottest Flyer Deals, Hit of the Month, New Lower Price!, Always Prices, Price drop, $5 and Under, PC Value Finds $5 and Under) plus a paged list (`total` 329 over 7 pages; `count` 379 counts the section items too). In Hottest Flyer Deals, Hickory Smoked Boneless Ham Steak at 3.00 with `deal` `type` `limit`, `text` "Limit 6, after limit $4.00", `deal_price` 3, `expiry_date` 2026-11-30.
- `/category` `{"category": "28224", "sort": "price_low_to_high"}`: Milk & Cream (`type` list, 4 children: Lactose Free, Flavoured Milk, Cream & Creamers, Regular Milk), `total` 227 over 5 pages, 8 sponsored. The first organic item was Mehadrin Chocolate Milk 200 ml at 0.99 with `stock_status` `out_of_stock`. Price sorts are PC Express's own order.
- `/stores` `{"city": "Winnipeg"}`: `total` 120 Real Canadian Superstore pickup stores, `matched` 8, first 1505 Real Canadian Superstore Mcphillips Street, 2132 Mcphillips St, Winnipeg MB R2V 3C8, `today` 07:00 AM - 10:00 PM, `minimum_order` 30.
- `/store` `{"store_id": "1517"}`: Real Canadian Superstore Marine Drive, 350 SE Marine Dr, Vancouver BC V5X 2S5, `store_hours` 07:00 AM - 11:00 PM for 7 dated days from 2026-11-25, `pharmacy_hours` 09:00 AM - 10:00 PM weekdays and 09:00 AM - 07:00 PM on the weekend, `optical_hours` closed on Sunday, `medical_clinic_hours` by weekday (`date` null), `holiday_hours` empty, `pharmacy_phone` 604-322-3704.
- `/suggestions` `{"query": "egg"}`: Eggs, Egg Noodles, Egg Whites, Eggo, Egg Nog, Eggplant.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def pcexpress(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/pcexpress/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# The same code on three banners (1 credit per search)
code = "20812144001_EA"
for banner, query, lang in [("superstore", "eggs", "en"), ("nofrills", "eggs", "en"), ("maxi", "oeufs", "fr")]:
    d = pcexpress("search", {"query": query, "banner": banner, "language": lang})["data"]
    for i in d["items"]:
        if i["code"] == code and not i["sponsored"]:
            deal = i["deal"] or {}
            print(banner, d["store"]["store_id"], i["price"], i["was_price"], deal.get("expiry_date"), i["pc_optimum_points"])

# GTIN, ingredients and nutrition (5 credits; check source)
p = pcexpress("product", {"code": code, "banner": "superstore"})["data"]
print(p["source"], p["gtin"], p["price"], p["comparison_prices"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` and `notes`.

- **item** (search, category, collection) - `code`, `article_number`, `unit_of_measure`, `name`, `brand`, `size`, `unit_price`, `package_sizing`, `url`, `image`, `price`, `was_price`, `price_text`, `member_only_price`, `tax_note`, `sold_by`, `weighted`, `min_quantity`, `max_quantity`, `deal` {`type`, `name`, `text`, `deal_price`, `points`, `expiry_date`}, `pc_optimum_points`, `badges`, `stock_status`, `stock_text`, `rating`, `review_count`, `sponsored`, `section` (on pages with sections).
- **search** - `banner` {`id`, `name`}, `language`, `query`, `corrected_query`, `redirected_to`, `page`, `page_size`, `sort`, `sort_applied`, `filters_applied`, `total`, `total_pages`, `has_more`, `count`, `sponsored_count`, `items[]`, `store` {`store_id`, `banner`, `requested`}, `facets[]` and `sorts[]` (with `include_facets`).
- **category** - `banner`, `language`, `category` {`category_id`, `name`, `type` (`list` or `department`), `url`, `breadcrumbs[]` {`name`, `category_id`, `url`}, `children[]` {`name`, `category_id`, `url`}}, then as search from `page`; a department adds `sections`.
- **collection** - `banner`, `language`, `collection` {`name`, `title`, `url`}, then as search from `page`, plus `sections[]` {`title`, `count`}.
- **product** - `banner`, `language`, `source` (`page` or `search`), `code`, `article_number`, `unit_of_measure`, `gtin`, `name`, `brand`, `description`, `size`, `url`, `images`, `breadcrumbs[]`, `price`, `price_unit`, `was_price`, `member_only_price`, `comparison_prices[]` {`price`, `per`}, `unit_price`, `price_type`, `price_expiry_date`, `deal_price`, `deal`, `promotions`, `deposit`, `stock_status`, `shoppable`, `sold_by`, `weighted`, `min_quantity`, `max_quantity`, `badges`, `ingredients`, `nutrition` {`serving_size`, `nutrients[]`, `micronutrients[]` {`name`, `amount`, `daily_value`}, `note`}, `variants`, `store`.
- **stores** - `banner`, `language`, `location`, `filters_applied` {`city`, `postal_code`, `province`}, `total`, `matched`, `count`, `stores[]` {`store_id`, `name`, `banner`, `banner_name`, `location_type`, `pickup_type`, `shoppable`, `address`, `city`, `province`, `postal_code`, `latitude`, `longitude`, `phone`, `time_zone`, `today` {`date`, `hours`, `open_now`}, `minimum_order`, `departments`, `url`, `distance_km` (near a point)}.
- **store** - every stores field plus `store_phone`, `pharmacy_phone`, `store_hours[]`, `pharmacy_hours[]`, `optical_hours[]`, `holiday_hours[]` {`day`, `date`, `hours`}, `medical_clinic_hours[]` (by weekday, `date` null), `services[]` {`name`, `phone`}.
- **suggestions** - `banner`, `language`, `query`, `count`, `suggestions[]`.

## Guardrails

- Name it "PC Express (Loblaw's online grocery for Real Canadian Superstore, No Frills, Loblaws, Zehrs, Fortinos, Valu-mart, Your Independent Grocer, Wholesale Club, Provigo and Maxi; Loblaw operates 2,504 stores per its 2025 annual report)" on first mention, "PC Express" or the banner's name after that.
- Prices: quote each with CAD, the banner, the default store number from `store`, the `fetched_at` date and "before tax" ("listed on PC Express for Real Canadian Superstore store 1033 on Nov 26, 2026, before tax"). Never present a default-store price as the price at another store, and never claim a price for a store the user chose.
- Deals: quote `deal.text` and `expiry_date` as PC Express shows them; say there is no start date. PC Optimum offers as given, never converted to dollars. `member_only_price` is the public member price shown on the item.
- Comparisons: the same `code` across banners, or the same GTIN (or brand, name and size) at another retailer, on one date. Report the numbers; no verdict on which banner or retailer is cheaper beyond the numbers shown, and no price-match advice.
- Reviews: `rating` and `review_count` only; review text is not offered.
- Descriptive only: no commentary on Loblaw's business, pricing practices or policies. Quote Loblaw figures only with their source and date.
- Do not republish PC Express product photos, descriptions or logos. Write banner domains as plain text, never as links, and cite product names, codes, store numbers and capture dates rather than linking banner pages. Use banner names to identify them, not to suggest any affiliation.
- Terms: Scavio does not collect or store PC Express data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account, no cart and no checkout. The site's terms cover how it may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, was prices, deals, end dates, points offers, codes, GTINs, stores or hours. Only return what the API returned, with the `fetched_at` time.
- Not available: choosing a store, review text, the printed flyer, Shoppers Drug Mart, Atlantic Superstore, City Market, T&T, PC Optimum login prices, deal start dates, price history (store your own), cart or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search or suggestions without `query`; category without `category` ("category is required: a category id (e.g. 28224) or a category link / path ending in /c/<id>."); collection without `collection`; product without `code` or `url`, or with both ("Send code or url, not both."); a `code` that is not a PC Express product code; a `banner` not in the table; a `banner` that does not match a link's site; `language: "fr"` on an English banner ("language must be en: ... (French is offered on provigo and maxi).") or `en` on Provigo; more than 10 filter values; `latitude` without `longitude`; any `store_id` on search, category, collection or product ("store_id is not offered: prices are the banner's default store's (store says which). Pick the banner whose prices you need; the stores endpoint lists each banner's stores.").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Real Canadian Superstore product <code>.", "No <banner> category <id>.", "No <banner> collection "<name>" with products.", "No <banner> store <id>.". Take codes, category ids, collection names and store ids from a previous answer rather than guessing them. A search with no matches is a `200` with `count` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=loblaws-grocery-prices-api).
- `502` means PC Express data was temporarily unavailable ("PC Express is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy: wait the `Retry-After` seconds and send it again. Not charged.
- A client timeout under 240 seconds can cut off a slow product or store answer: raise the timeout rather than resending in parallel.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.95.0
npm install scavio@0.96.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: superstore } = await scavio.pcexpress.search({ query: "eggs", include_facets: true });
const { data: nofrills } = await scavio.pcexpress.search({ query: "eggs", banner: "nofrills" });
const { data: maxi } = await scavio.pcexpress.search({ query: "oeufs", banner: "maxi", language: "fr" });
const { data: product } = await scavio.pcexpress.product({ code: "20812144001_EA" });
const { data: deals } = await scavio.pcexpress.collection({ collection: "deals-centre", banner: "nofrills" });
const { data: stores } = await scavio.pcexpress.stores({ city: "Winnipeg" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.pcexpress.search(...)`, `category`, `collection`, `product`, `stores`, `store` and `suggestions`, with the same parameter names as keyword arguments. Give the client a timeout of at least 240 seconds for these calls.

## MCP

The Scavio MCP server exposes all 7 endpoints as tools: `search_pcexpress`, `get_pcexpress_category`, `get_pcexpress_collection`, `get_pcexpress_product`, `get_pcexpress_stores`, `get_pcexpress_store` and `get_pcexpress_suggestions`. PC Express is opt-in: add `pcexpress` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.95.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,pcexpress"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/pcexpress-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=loblaws-grocery-prices-api), [category](https://scavio.dev/docs/pcexpress-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=loblaws-grocery-prices-api), [collection](https://scavio.dev/docs/pcexpress-collection?utm_source=agent-skills&utm_medium=skill&utm_campaign=loblaws-grocery-prices-api), [product](https://scavio.dev/docs/pcexpress-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=loblaws-grocery-prices-api), [stores](https://scavio.dev/docs/pcexpress-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=loblaws-grocery-prices-api), [store](https://scavio.dev/docs/pcexpress-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=loblaws-grocery-prices-api), [suggestions](https://scavio.dev/docs/pcexpress-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=loblaws-grocery-prices-api). Overview: [PC Express API](https://scavio.dev/pcexpress-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=loblaws-grocery-prices-api).
