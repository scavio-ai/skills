---
name: hema-store-stock-api
description: HEMA store stock API for HEMA (hema.com, the Dutch variety store) - for up to 12 HEMA article numbers per call, the sellable units HEMA's store service reports at each store near a city, postcode or point (or across a country) with HEMA's stock level (full, regular or limited), shelf locations, address, opening hours, special hours and distance, in the Netherlands, Belgium, France, Germany, Luxembourg and Austria; one product in full with EAN, colour and size variants, online stock, order limit and HEMA's dated price schedule including upcoming promotions, with the mechanics as HEMA writes them (2+1 gratis, 2+2 gratis, 3+1 offert); the same article number priced on each webshop (nl, be in Dutch or French, fr, de; all EUR, prices set per market); keyword search, category, new-arrival and sale lists, 24 per page with total and pages, sorted by price, newest or best selling and filtered by any facet; HEMA's weekly offers page (nl, be) with its validity date and offer week; the Christmas and Sinterklaas campaign pages; HEMA's own product reviews (one Dutch pool for nl, fr and de, a Belgian pool for be; no reviewer names); every HEMA store of a country with hours and services; the category menu and search suggestions. Data in each market's language. 13 endpoints, 1 credit per call. No price history, brands endpoint or checkout.
version: 1.0.0
tags: hema, hema-com, hema-nl, hema-api, hema-store-stock, hema-voorraad, hema-stock-checker, hema-prices, hema-promotions, hema-aanbiedingen, hema-black-friday, hema-sinterklaas, hema-kerst, hema-christmas, hema-offers, hema-stores, hema-opening-hours, hema-store-locator, hema-reviews, hema-products, hema-new-arrivals, hema-sale, variety-store, dutch-retail, european-retail, netherlands, belgium, france, germany, luxembourg, austria, store-stock, in-store-availability, price-monitoring, eur, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/hema-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api
---

# HEMA Store Stock API - Units per Store, Prices, Promotions, Reviews

Read HEMA (hema.com, the Dutch variety store) on its four webshops, the Netherlands (www.hema.nl), Belgium in Dutch or French, France and Germany: store stock per store near a place, one product in full with its dated price schedule, keyword search, category, new-arrival and sale lists, the weekly offers page, the Christmas and Sinterklaas campaign pages, search suggestions, the category menu, HEMA's stores with their hours, and HEMA's own product reviews. All 13 endpoints return structured JSON at 1 credit per call.

This is HEMA the retailer (founded in Amsterdam in 1926, almost entirely own-brand household goods, clothing, baby, beauty, party, seasonal and food). It is not HEMA the chemical (the 2-hydroxyethyl methacrylate monomer) and not Hema Pharmaceuticals.

**The job this skill is for: HEMA store stock.** For up to 12 HEMA articles, the sellable units HEMA's store service reports at each store near a city or postcode, with HEMA's stock level, next to the article's dated promotion, across the Netherlands, Belgium, France and Germany, plus HEMA's stores in Luxembourg and Austria, on a dated read.

Eight limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** A not-found (an unknown article number, category, campaign or store id, a place HEMA's store finder cannot find) is a `404` charged 1 credit. A refused input (`400`) and an upstream failure (`502`, `503`) are not charged.
- **Store stock is what HEMA's store service reports, at the moment of the call.** `sellable_units` is the count HEMA's store service gives for that store and `stock_level` its level (`full`, `regular`, `limited`). Report "HEMA's store service reported 19 sellable units at Utrecht-Centrum at 10:12 on 2026-11-22", never "the shelf has it" or "in stock at HEMA". Scavio makes no promise of its accuracy.
- **One article number, a price per market.** `sku` (6 to 8 digits, `15300147`) is the same on every webshop; the price is set per market. On 2026-11-22 article `15300147` read EUR 8.99 on nl, fr and de and EUR 9.99 on be. Never carry one market's price over to another.
- **Store stock needs one size and colour.** A list item's `sku` can be a colour group id (`4230175BLACK`); for store stock send a variant `sku` (`4230176`, from `online.variants[]` on the list item or `variants.groups[].variants[]` on the product).
- **Promotions carry HEMA's own dates, upcoming ones included.** `price_schedule[]` lists every dated price HEMA has set for the article, with the promotion text as HEMA writes it ("2+1 gratis", "3+1 offert"). HEMA's own note: online prices can differ from store prices ("De internetprijzen kunnen afwijken van de winkelprijzen"). Say "the online price on <market>".
- **Six store countries, four webshops.** `country` `lu` and `at` have HEMA stores but no webshop: only `/store-stock`, `/stores` and `/store` take them (elsewhere a `400`, not charged). The offers page is nl and be only; the sale page is nl, be and de; Sinterklaas is nl and be.
- **Reviews come from two pools.** nl, fr and de show one shared Dutch review pool (`review_pool` `nl-nl`); be (either language) shows its own Belgian pool (`nl-be`). Pages 1 to 5 only: 8 reviews, then 30 per page. No reviewer names.
- **Data in each market's language.** Names, labels, promotions, facet names, store service names and review texts come back in Dutch, French or German, as HEMA writes them: translate them for the user, never alter the values.

HEMA has no public product, price or stock API. Its suppliers use a supplier portal, and approved affiliates on TradeTracker, Metapic or LinkYourBrand get a product feed and banners for their own affiliate links; HEMA's affiliate page does not describe store stock in that feed. This skill reads the public HEMA pages instead, with one Scavio key.

See also: for Action (the European discount store, no store stock) use `action-com-api`; for bol.com in the Netherlands and Belgium use `bol-com-api`; for IKEA stock by store use `ikea-api`; for Argos store stock in the UK use `argos-stock-checker-api`; for prices across retailers use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Check HEMA store stock (HEMA voorraad, stock en magasin, Bestand in der Filiale) for one or more articles near a city, town, postcode or coordinates, or across a country
- Read one HEMA product in full: price, promotion with its dates, upcoming promotions, EAN, colour and size variants, online stock, order limit
- Compare one HEMA article's online price across the Netherlands, Belgium, France and Germany
- Read HEMA's weekly offers (aanbiedingen, offres spéciales) with the validity date and offer week, the Black Friday lists, the sale or outlet page, or HEMA's new arrivals
- Read HEMA's Christmas (kerst, noël, Weihnachten) or Sinterklaas (saint-nicolas) campaign page
- Search HEMA by keyword, or list a category, sorted by price, newest or best selling, filtered by size, colour, product type, price or online stock
- Find HEMA stores near a place or every store of a country, with opening hours, special hours (koopzondag, late-night shopping), closed dates and services
- Read HEMA customer reviews with the rating distribution
- Resolve category paths and search suggestions before a search

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, store, sale, offers, campaign and suggestions took 1-4 seconds, product, category, new arrivals and categories 1-7, store-stock 2-9, stores 1-11 and reviews 8-15 (HEMA's review pages can take up to about 70). Search usually took 2-4 seconds; some searches took 20 to 90. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/hema/store-stock` | Up to 12 article numbers in the stores near a city, postcode or point (or across a country): per store the sellable units, stock level and shelf locations, plus address, hours, special hours, services and distance | 1 |
| `POST /api/v1/hema/product` | One product on one market by article number or link: EAN, price, promotion, the dated `price_schedule`, unit price, online stock, sellable in store, order limit, variants, specifications | 1 |
| `POST /api/v1/hema/search` | Products for a keyword, 24 per page, with total, pages and the facets to filter by | 1 |
| `POST /api/v1/hema/category` | One category's products by path or link, with filters, sort and paging | 1 |
| `POST /api/v1/hema/categories` | HEMA's category menu (18 departments and 880 nodes at depth 3 on nl) | 1 |
| `POST /api/v1/hema/new-arrivals` | HEMA's new collection (1,120 products on nl in the capture) | 1 |
| `POST /api/v1/hema/sale` | The sale page (nl) or outlet page (be, de) | 1 |
| `POST /api/v1/hema/offers` | The weekly offers page (nl, be): HEMA's validity label, its ISO date, the offer week and the promotion cards, each with the category path of its product list | 1 |
| `POST /api/v1/hema/campaign` | A campaign page (`christmas` on every webshop, `sinterklaas` on nl and be, or a campaign slug) with its products and promotion texts | 1 |
| `POST /api/v1/hema/suggestions` | Search suggestions for a partial query: phrases, categories with product counts, up to 5 products | 1 |
| `POST /api/v1/hema/stores` | Every HEMA store of a country, or the stores near a city, postcode or point, with address, hours, special hours, closed dates and services | 1 |
| `POST /api/v1/hema/store` | One store by `store_id`, optionally with one article's stock there | 1 |
| `POST /api/v1/hema/reviews` | One article's reviews: rating distribution, average, rating and text-review counts, 8 reviews on page 1 then 30 per page | 1 |

## Markets

`country` picks the webshop (default `nl`); `language` matters only in Belgium.

| `country` | Webshop | `language` | Endpoints |
|---|---|---|---|
| `nl` | Netherlands (www.hema.nl, nl-nl) | nl | all 13 |
| `be` | Belgium (nl-be, fr-be) | `nl` (default) or `fr` | all 13 |
| `fr` | France (fr-fr) | fr | all but `/sale` and `/offers`; `/campaign` `christmas` only |
| `de` | Germany (de-de) | de | all but `/offers`; `/campaign` `christmas` only |
| `lu` | Luxembourg (stores only, no webshop) | leave out | `/store-stock`, `/stores` (and `/store` by `store_id`) |
| `at` | Austria (stores only, no webshop) | leave out | `/store-stock`, `/stores` (and `/store` by `store_id`) |

- All prices are EUR. Every webshop answer echoes `country`, `language`, `market` (e.g. `nl-nl`) and `currency`.
- Leave `language` out outside Belgium: a language the country does not have is a `400`. A product, category or campaign link carries its own market: send it alone, or with a `country` / `language` that agrees with it.
- Store counts in the store list on 2026-11-22: NL 570, BE 111, FR 69, DE 17, AT 5, LU 4. HEMA's FY2025 infographic reports "meer dan 770 HEMA-winkels" and gross sales of EUR 2.237 billion; the Van Eerd family (owner of Jumbo) completed its purchase of all HEMA shares on 11 February 2026 (HEMA corporate release). Quote these with their sources, never from the samples.
- Not served: the United Kingdom and Spain (HEMA left both) and any country without HEMA stores; Luxembourg and Austria have no webshop, so no product, price or review endpoint there.

## Store stock

`/hema/store-stock` takes `skus` (1 to 12 article numbers of one size and colour), one of `query` (a city, town or postcode) or `lat` + `lng`, or neither (every store of the country), plus `country`, `radius_km` (1-300, default 50), `limit` (1-50 stores, default 10) and `in_stock_only`.

- The answer: `country`, `country_code`, `skus`, `location` {`query`, `formatted_address`, `postcode`, `city`, `country_code`, `latitude`, `longitude`}, `radius_km`, `limit`, `in_stock_only`, `count`, `summary[]` {`sku`, `stores_with_stock`}, `stores[]` with the store fields (see Stores) and `stock[]` {`sku`, `sellable_units`, `stock_level`, `stock_indicator`, `shelf_locations`, `in_stock`}.
- `sellable_units` is the count HEMA's store service reports for that store; `null` (with `in_stock: false`) when it lists none. `stock_level` is HEMA's level (`full`, `regular`, `limited`; `stock_indicator` is HEMA's raw value, e.g. `LimitedStock`). HEMA sets the level: never derive it from the units (2 units read `limited` at one store and 3 read `regular` at another).
- `shelf_locations` are HEMA's own location codes (`LBY-X02-1-2-1`), as given: quote them, do not interpret them.
- Stores come nearest first with `distance_km` from the place asked. Without a place the answer covers the country (in the Luxembourg capture: all 4 stores, `distance_km` null).
- `in_stock_only: true` keeps the stores that hold at least one of the articles: the Paris capture (`lat` 48.8566, `lng` 2.3522, three articles) returned 10 stores, and `summary` read 0 stores with `13511001`, 6 with `15300147` and 10 with `10860090`.
- Captured 2026-11-22: `15300147` (a rabbit comforter, "knuffeldoekje konijn") near Utrecht read 19 units (`full`) at Utrecht-Centrum, 1 (`limited`) at Utrecht-Hoog Catharijne and none at CS Utrecht, and 9 of the 10 nearest stores held it; near Antwerpen 22 (`full`) at Antwerpen-Meir and 4 (`regular`) at Antwerpen Keyserlei; in Austria 5 (`full`) at Wien Mariahilferstrasse.
- One call covers one place. For several cities, call once per city (1 credit each).

## Prices and promotions

List items (search, category, new arrivals, sale, campaign) carry `price`, `was_price` (HEMA's struck-through price, as shown), `price_from` (true when HEMA shows a from-price across sizes or colours), `discount_percent` (computed by Scavio from `was_price`), `promotion` (HEMA's promotion text: "2+2 gratis", "40% korting | vanaf 9.49", "sale", "korting") and `labels`.

`/hema/product` adds:

| Field | Meaning |
|---|---|
| `promotion` | {`label`, `loyalty_card_only`, `valid_from`, `valid_to`}: the promotion running now, as HEMA writes it |
| `price_schedule[]` | {`valid_from`, `valid_to`, `price`, `was_price`, `promotion`, `loyalty_card_only`, `unit_price`}: every dated price HEMA has set, upcoming promotions included; `valid_to` `null` = open-ended. Consecutive entries share the boundary date as HEMA gives it |
| `unit_price` | {`price`, `unit`} (e.g. EUR 4.98 per `kg`), or `null` |
| `online_stock` | {`type` (`LIMITED` or `UNLIMITED`), `units`}: online units as HEMA reports them, never a store's stock |
| `sellable_in_store` | Whether HEMA sells the article in its stores |
| `order_limit` | {`min`, `max`, `step`} per online order |

An upcoming promotion, captured 2026-11-22 on fr-fr for `25101046` (a Takkie and Siepie plush Christmas hanger, EUR 6.99): "3+1 offert" (buy 3, get 1 free) from 2026-11-12 to 2026-11-29, no promotion from 2026-11-29 to 2026-12-14, then "3+1 offert" again from 2026-12-14 to 2026-12-27. On hema.nl the same article (EUR 5.99) was scheduled for "3+1 gratis ; met je HEMA pas" (3+1 free with your HEMA loyalty card) from 2026-12-14 to 2026-12-27.

- Quote the mechanic as HEMA writes it and its dates. A promotion that needs the HEMA card says so in its text and in `loyalty_card_only`: label it as a card promotion.
- Report price differences between markets descriptively, from the numbers and the `fetched_at` date. Never say why a market is priced higher, and never call a discount real or fake.
- `discount_percent` is computed only where HEMA shows a `was_price`; a multi-buy ("2+1 gratis") has no percent.

## Offers and campaigns

- `/hema/offers` (nl, be): `label` is HEMA's validity text ("geldig t/m 22 november" = valid up to and including 22 November; "valide jusqu'à 22 novembre" on fr-be), `valid_to` its ISO date (`2026-11-22`; the label has no year, Scavio takes the nearest one), `week` HEMA's offer week (47), and `sections[]` {`name`, `week`, `cards[]` {`title`, `subtitle`, `url`, `category`}}. The page carries no products: send a card's `category` to `/hema/category` for its product list. In the capture: 12 sections and 74 cards on nl, 10 and 71 on both Belgian webshops, many of them Black Friday lists (`baby/aanbiedingen/black-friday-babykleding`).
- `/hema/campaign`: `christmas` (the `kerst`, `noel` or `weihnachten` page per market) on every webshop, `sinterklaas` (`sinterklaas`, `saint-nicolas`) on nl and be, or any campaign slug or link. A campaign page is a landing page (`list_type` `landing`): its product carousels {`title`, `link`, `count`, `skus`} and all their products, no paging. Captured: 39 products for nl Christmas, 14 for nl-be Sinterklaas, 54 for fr Christmas, 26 for de.
- `/hema/sale`: nl `/sale` (913 products in the capture), be and de `/outlet`. France has no sale page: a `400`, not charged.
- Some search words lead to a landing page: `{"query": "kerst"}` on nl answered `redirected_to` `kerst`, `list_type` `landing` with the 39 campaign products.

## Workflow

1. **Find the article:** `/hema/search` with `query` in the market's language (`sokken`, `kaars`, `bougie`, `Kerze`), `/hema/category` with a `path` from `/hema/categories`, `/hema/campaign` or an offers card's `category`. Each item has `sku`, `price`, `was_price` and `promotion`.
2. **Narrow:** send `filters` with up to 6 facets, `{"<facets[].facet>": "<values[].value>"}`. Facet keys and values come from the same market's answer (`maincolour` on nl, `ref_maincolour` on nl-be; `searchable` keeps products in stock online). Use `price_min` / `price_max` for the price facet.
3. **Pick a size and colour:** a `sku` with a colour suffix (`4230175BLACK`) is a group; take a variant `sku` from `online.variants[]` or `/hema/product` `variants.groups[].variants[]`.
4. **Promotion and dates:** `/hema/product` with `sku` and `country` for `promotion` and `price_schedule`.
5. **Store stock:** `/hema/store-stock` with up to 12 `skus` and a `query` or `lat` / `lng`; then `/hema/store` with a `store_id` and `sku` for one store.
6. **Prices per market:** one `/hema/product` call per webshop (nl, be, be + `fr`, fr, de), 1 credit each.
7. **Reviews:** `/hema/reviews` with `sku`; pages 2 to 5 for more.
8. **Watching stock or prices:** there is no history. Poll the same articles and places on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`), new arrivals (`/new-arrivals`), sale (`/sale`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Search text, 1-200 chars; the market's language works best |
| `category` | string | category: required | A category path (`categories[].path`, e.g. `baby/babykleding`, or an offers card's `category`) or its HEMA link |
| `country` / `language` | string | `nl` | See Markets |
| `sort` | string | `relevance` | `relevance` (HEMA's own order), `price_asc`, `price_desc`, `newest`, `best_selling`. A from-price tile is placed by one of its variants' prices, so a price sort is not always strictly ordered by the price shown |
| `page` | integer | 1 | 1-100; 24 products a page; `total_pages` says how deep the list goes |
| `filters` | object | none | Up to 6 facets: `{"maincolour": "zwart"}` or a list of values per facet |
| `new_only` | boolean | false | Only HEMA's new collection. Not on `/new-arrivals` (a `400`) |
| `price_min` / `price_max` | number | none | Price band in EUR |

A search with no match answers `200` with `total` 0.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string or integer | one of | HEMA article number (6-8 digits, `15300147`) or a colour group id (`4230175BLACK`) |
| `url` | string | one of | A HEMA product link (www.hema.nl or www.hema.com/<locale>/...); the market comes from the link. Send exactly one of `sku`, `url` |
| `country` / `language` | string | `nl` | See Markets |

### Campaign (`/campaign`), offers (`/offers`), categories (`/categories`), suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `campaign` | string | campaign: required | `christmas`, `sinterklaas`, a campaign slug (`kerst`, `noel`, `weihnachten`, `saint-nicolas`) or its HEMA link |
| `depth` | integer | 3 | Categories: levels, 1-3 |
| `query` | string | suggestions: required | What the shopper has typed so far (1-100 chars) |
| `country` / `language` | string | `nl` | Offers: `nl` or `be` only |

### Store stock (`/store-stock`), stores (`/stores`), store (`/store`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `skus` | array | store-stock: required | 1-12 article numbers of one size and colour (`["15300147", "10860090"]`) |
| `query` | string | optional | A city, town or postcode (`Utrecht`, `Antwerpen`, `3511`), placed by HEMA's own store finder |
| `lat` / `lng` | number | optional | A point instead of `query`. Send both |
| `radius_km` | integer | 50 | Search radius around the place, 1-300 |
| `limit` | integer | store-stock 10; stores 20 near a place, every store without one | store-stock 1-50; stores up to 1000 |
| `in_stock_only` | boolean | false | Store-stock: only stores holding at least one of the articles |
| `store_id` | string or integer | store: required | `stores[].store_id` (`0013`) |
| `sku` | string or integer | store: optional | Adds that article's stock in the store |
| `country` | string | `nl` | Store-stock and stores: `nl`, `be`, `fr`, `de`, `lu` or `at`. `/store` takes no `country`: a `store_id` from any country works |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string or integer | required | HEMA article number |
| `country` / `language` | string | `nl` | nl, fr and de read the shared Dutch pool; be its Belgian pool |
| `sort` | string | `newest` | `newest` or `highest` (highest rating first) |
| `page` | integer | 1 | 1-5: page 1 = the first 8 reviews, each later page the next 30 |

## Examples

### Store stock near a city

```bash
curl -X POST https://api.scavio.dev/api/v1/hema/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"skus": ["15300147", "10860090"], "query": "Utrecht"}'
```

Captured `data` (2026-11-22, 1 credit; 2 of 10 stores shown; `phone` omitted, and `hours`, `special_hours` and `services` omitted on the second):

```json
{
  "country": "nl",
  "country_code": "NL",
  "skus": ["15300147", "10860090"],
  "location": { "query": "Utrecht", "formatted_address": "Utrecht, Nederland", "postcode": "3511", "city": "Utrecht", "country_code": "NL", "latitude": 52.08979, "longitude": 5.11414 },
  "radius_km": 50,
  "limit": 10,
  "in_stock_only": false,
  "count": 10,
  "summary": [
    { "sku": "15300147", "stores_with_stock": 9 },
    { "sku": "10860090", "stores_with_stock": 10 }
  ],
  "stores": [
    {
      "store_id": "0013",
      "name": "Utrecht-Centrum",
      "status": "open",
      "operator": "hema",
      "address": { "street": "Steenweg 59", "postcode": "3511 JN", "city": "Utrecht", "country_code": "NL" },
      "latitude": 52.0908431,
      "longitude": 5.1151145,
      "distance_km": 0.13,
      "hours": [
        { "day": "monday", "open": "09:00", "close": "18:30" },
        { "day": "thursday", "open": "09:00", "close": "21:00" },
        { "day": "sunday", "open": "11:00", "close": "18:00" }
      ],
      "special_hours": [
        { "date": "2026-11-27", "type": "KOOPAVOND", "open": "09:00", "close": "20:00" },
        { "date": "2026-12-24", "type": "GEWIJZIGD", "open": "09:00", "close": "17:00" }
      ],
      "closed_dates": ["2026-12-25", "2027-01-01"],
      "services": ["Rookworst", "Takeaway", "Restaurant", "Gebakservice", "Fotoshop", "PickupFromStore", "PickInStore", "Zelfscan"],
      "stock": [
        { "sku": "15300147", "sellable_units": 19, "stock_level": "full", "stock_indicator": "FullStock", "shelf_locations": ["LBY-X02-1-2-1", "LBY-X02-1-1-1", "KBY-D05-2-2-1"], "in_stock": true },
        { "sku": "10860090", "sellable_units": 186, "stock_level": "full", "stock_indicator": "FullStock", "shelf_locations": ["KEA-A14-4-1-1", "KSE-T19-1-1-1", "KSE-T20-1-1-1"], "in_stock": true }
      ]
    },
    {
      "store_id": "0246",
      "name": "Utrecht-Hoog Catharijne",
      "status": "open",
      "operator": "hema",
      "address": { "street": "Godebaldkwartier 325", "postcode": "3511 DS", "city": "Utrecht", "country_code": "NL" },
      "latitude": 52.0912,
      "longitude": 5.11309,
      "distance_km": 0.17,
      "closed_dates": ["2026-12-25", "2027-01-01"],
      "stock": [
        { "sku": "15300147", "sellable_units": 1, "stock_level": "limited", "stock_indicator": "LimitedStock", "shelf_locations": ["HBA-G01-2-1-1"], "in_stock": true },
        { "sku": "10860090", "sellable_units": 21, "stock_level": "full", "stock_indicator": "FullStock", "shelf_locations": ["HFC-A02-1-1-1"], "in_stock": true }
      ]
    }
  ]
}
```

The first store's `hours` list all 7 days (3 shown), its `special_hours` 5 dates (2 shown) and its `services` 14 (8 shown). `15300147` is a rabbit comforter and `10860090` a 400 g pack of stroopwafels. HEMA's store service reported 19 sellable units of the comforter at Utrecht-Centrum and 1 at Hoog Catharijne at the time of the call. `special_hours` `type` is HEMA's Dutch code: `KOOPAVOND` late-night shopping, `KOOPZONDAG` shopping Sunday, `GEWIJZIGD` changed hours. `services` are HEMA's names (`Gebakservice` cake service, `Fotoshop` photo shop, `PickupFromStore` pick-up in store, `Zelfscan` self-scan); `day` comes in English.

### Product with its price schedule

```bash
curl -X POST https://api.scavio.dev/api/v1/hema/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "15300147"}'
```

Captured `data` (2026-11-22, 1 credit; trimmed: `description`, `images`, `breadcrumbs`, `specifications`, `care`, `safety`, `parent_sku`, `variant_group_url`, `colour`, `size`, `target_audience`, `nutrition` and `storage` dropped):

```json
{
  "country": "nl",
  "language": "nl",
  "market": "nl-nl",
  "currency": "EUR",
  "requested": "15300147",
  "sku": "15300147",
  "ean": "8721245397367",
  "name": "knuffeldoekje konijn",
  "url": "https://www.hema.nl/speelgoed-hobby/babyspeelgoed/knuffeldoekje-konijn-15300147.html",
  "status": "ACTIVE",
  "product_type": "knuffel",
  "main_material": "polyester",
  "price": 8.99,
  "was_price": null,
  "discount_percent": null,
  "unit_price": null,
  "promotion": { "label": "2+1 gratis", "loyalty_card_only": false, "valid_from": "2026-11-16", "valid_to": "2026-11-29" },
  "price_schedule": [
    { "valid_from": "2026-11-16", "valid_to": "2026-11-29", "price": 8.99, "was_price": null, "promotion": "2+1 gratis", "loyalty_card_only": false, "unit_price": null },
    { "valid_from": "2026-11-29", "valid_to": null, "price": 8.99, "was_price": null, "promotion": null, "loyalty_card_only": false, "unit_price": null }
  ],
  "online_stock": { "type": "LIMITED", "units": 116 },
  "sellable_in_store": true,
  "order_limit": { "min": 1, "max": 200, "step": 1 },
  "sales_blocked": false,
  "on_display": { "from": "2026-09-21", "to": "2027-10-03", "from_week": "2026-39", "to_week": "2027-39" },
  "availability": "InStock",
  "labels": [{ "text": "te personaliseren", "type": "MARKETING", "valid_from": null, "valid_to": null }],
  "variants": null,
  "fulfillment": { "partner": "HEMA", "made_to_order": false },
  "personalizable": true,
  "complete": true
}
```

"2+1 gratis" (buy 2, get 1 free) runs 2026-11-16 to 2026-11-29; from 2026-11-29 the schedule has no promotion. `online_stock.units` (116) is HEMA's online count, not a store's. "te personaliseren" = can be personalised. On fr, de and be the same `sku` returns that market's name and price ("doudou lapin" in French, "Schmusetuch Kaninchen" in German). A product with sizes or colours returns `variants` {`variant_axis` (`maat` = size), `group_axis` (`kleur` = colour), `groups[]` {`value`, `label`, `colour_code`, `url`, `variants[]` {`sku`, `label`, `in_stock`, `status`, `url`}}}. An unknown number answers `404` ("HEMA has no article 99999991 on nl-nl (or the number does not exist)."), charged 1 credit.

### Weekly offers

```bash
curl -X POST https://api.scavio.dev/api/v1/hema/offers \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "nl"}'
```

Captured `data` (2026-11-22, 1 credit; 1 of 12 sections shown):

```json
{
  "country": "nl",
  "language": "nl",
  "market": "nl-nl",
  "currency": "EUR",
  "path": "aanbiedingen",
  "title": "aanbiedingen",
  "label": "geldig t/m 22 november",
  "valid_to": "2026-11-22",
  "week": 47,
  "section_count": 12,
  "count": 74,
  "sections": [
    {
      "name": "weekacties",
      "week": 47,
      "cards": [
        { "title": "babykleding", "subtitle": "korting wordt verrekend in de winkelmand", "url": "https://www.hema.nl/baby/aanbiedingen/black-friday-babykleding", "category": "baby/aanbiedingen/black-friday-babykleding" },
        { "title": "kinderkleding", "subtitle": "korting wordt verrekend in de winkelmand", "url": "https://www.hema.nl/kind/aanbiedingen/black-friday-kinderkleding", "category": "kind/aanbiedingen/black-friday-kinderkleding" },
        { "title": "dameskleding", "subtitle": "korting wordt verrekend in de winkelmand", "url": "https://www.hema.nl/dames/aanbiedingen/black-friday-dameskleding", "category": "dames/aanbiedingen/black-friday-dameskleding" },
        { "title": "herenkleding", "subtitle": "korting wordt verrekend in de winkelmand", "url": "https://www.hema.nl/heren/aanbiedingen/black-friday-herenkleding", "category": "heren/aanbiedingen/black-friday-herenkleding" }
      ]
    }
  ]
}
```

"weekacties" are the week's offers; "korting wordt verrekend in de winkelmand" = the discount is applied in the basket. Send a card's `category` to `/hema/category` for its products and their `promotion` texts.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/hema/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "10860090"}'
```

Captured `data` (2026-11-22, 1 credit; 1 of 8 reviews shown):

```json
{
  "country": "nl",
  "language": "nl",
  "market": "nl-nl",
  "currency": "EUR",
  "sku": "10860090",
  "review_pool": "nl-nl",
  "review_pool_note": null,
  "sort": "newest",
  "page": 1,
  "offset": 0,
  "page_size": 8,
  "total_text_reviews": 302,
  "total_pages": 11,
  "has_more": true,
  "average_rating": 4.37,
  "total_ratings": 1583,
  "ratings_only": 1281,
  "recommended": 223,
  "not_recommended": 68,
  "rating_distribution": { "1": 87, "2": 50, "3": 111, "4": 282, "5": 1053 },
  "count": 8,
  "reviews": [
    {
      "review_id": "1237528889",
      "language": "nl_NL",
      "rating": 3,
      "title": null,
      "text": "Ik ben niet helemaal tevreden omdat de wafels nogal hard waren",
      "submitted_at": "2026-11-20T09:27:36.000+00:00",
      "experienced_on": "2026-11-8",
      "recommends": false,
      "syndicated": false,
      "verified_purchaser": false,
      "badges": [],
      "helpful_votes": 0,
      "not_helpful_votes": 0
    }
  ]
}
```

1,583 star ratings, 302 of them with text ("not entirely satisfied because the wafers were rather hard"). `total_pages` counts HEMA's whole list, but pages above 5 are a `400`: pages 1-5 reach 128 text reviews. On be the same article read the Belgian pool (`review_pool` `nl-be`: 1,458 ratings, 273 with text); on fr `review_pool_note` says the reviews come from the shared pool read on the NL page. `experienced_on` is as HEMA gives it.

### Search, category, sale, new arrivals, campaign, categories, suggestions, stores and store

- `/search` with `{"query": "sokken"}` (socks): 296 products in 13 pages, facets `maat` (size), `soort product` (product type), `kleur` (colour), `prijs` (price, `min` 1 / `max` 40), `nieuw` (new) and `online op voorraad` (in stock online). The first item `4230175BLACK` (5 pairs of women's socks) read EUR 9.99 with "2+2 gratis" and variants `4230176`, `4230177`. `{"query": "bougie", "country": "be", "language": "fr"}`: 365 products; `{"query": "Kerze", "country": "de"}`: 320.
- `/category` with `{"category": "baby/babykleding"}` (baby clothing): 386 products in 17 pages.
- `/sale` on nl: 913 products; the first read EUR 3 against a `was_price` of 8.99 (`discount_percent` 67, `promotion` "sale").
- `/new-arrivals` on nl: 1,120 products in 47 pages.
- `/campaign` with `{"campaign": "christmas"}` on nl: the `kerst` landing page, 39 products in carousels such as "nieuw bij HEMA: uniek kerstdorp" (new at HEMA: a Christmas village).
- `/categories` on nl: 18 departments from `aanbiedingen` (offers), `sinterklaas` and `kerst` to `fotoservice` and `sale`, 880 nodes at depth 3; `path` (e.g. `baby/babykleding`) is the input of `/category`.
- `/suggestions` with `{"query": "kerst"}`: 781 results, phrases (`kerst met kids`, `kersttaart`, `kersttrui`), categories with product counts (`kerst` 579, `kerst tafelen` 143) and 5 products with prices.
- `/stores` with `{"query": "Utrecht"}`: the 20 nearest stores with `distance_km`; `{"country": "fr"}` without a place: all 69 French stores. `/store` with `{"store_id": "0013", "sku": "15300147"}`: Utrecht-Centrum with `delivery_address` and that article's `stock` (19 units, `full`). The `/store` capture returned `special_hours` and `closed_dates` empty for a store whose `/stores` entry had them: read those from `/stores` or `/store-stock`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def hema(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/hema/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Store stock for two articles near several cities (1 credit per city)
skus = ["15300147", "10860090"]
for country, city in (("nl", "Utrecht"), ("be", "Antwerpen"), ("de", "Köln")):
    res = hema("store-stock", {"skus": skus, "query": city, "country": country})
    for s in res["data"]["stores"]:
        for st in s["stock"]:
            print(res["fetched_at"], country, s["name"], s["distance_km"], st["sku"], st["sellable_units"], st["stock_level"])

# 2. One article's online price and dated promotions on each webshop (1 credit per market)
for country, language in (("nl", None), ("be", "nl"), ("be", "fr"), ("fr", None), ("de", None)):
    body = {"sku": "25101046", "country": country}
    if language:
        body["language"] = language
    d = hema("product", body)["data"]
    print(d["market"], d["name"], d["price"], d["currency"])
    for p in d["price_schedule"]:
        print("   ", p["valid_from"], p["valid_to"], p["price"], p["promotion"], "card" if p["loyalty_card_only"] else "")
# An article a market does not carry answers 404 (raise_for_status raises): catch it per market.

# Store each answer with fetched_at and run this on a schedule: that stored series is
# your stock and price history (HEMA shows only the current state).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every webshop `data` carries `country`, `language`, `market` and `currency`.

- **item** (search, category, new arrivals, sale, campaign) - `sku`, `name`, `url`, `image`, `price`, `was_price`, `price_from`, `currency`, `discount_percent`, `promotion`, `labels`, `product_type`, `colour`, `sizes`, `stock_status`, `online` {`available`, `limited_stock`, `variants[]` {`sku`, `available`, `limited_stock`}}, `rating`.
- **lists** (search, category, new arrivals, sale, campaign) - `filters`, `new_only`, `price_min`, `price_max`, `redirected_to`, `list_type` (`grid`, or `landing` for a campaign page: no paging), `title`, `sort`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `items[]`, `facets[]` {`facet` (the key to send in `filters`), `name`, `values[]` {`value`, `count`}, `min`, `max`}. Search adds `query`; category `category`; new arrivals and sale `path`; campaign `campaign`, `slug`, `carousels[]` {`title`, `link`, `count`, `skus`}.
- **product** - `requested`, `sku`, `ean`, `name`, `description`, `url`, `status`, `product_type`, `parent_sku`, `variant_group_url`, `images`, `breadcrumbs[]` {`name`, `url`}, `colour`, `size`, `main_material`, `target_audience`, `specifications[]` / `care[]` / `safety[]` {`key`, `name`, `value`}, `nutrition`, `storage`, `price`, `was_price`, `discount_percent`, `unit_price`, `promotion`, `price_schedule[]`, `online_stock`, `sellable_in_store`, `order_limit`, `sales_blocked`, `on_display`, `availability`, `labels[]` {`text`, `type`, `valid_from`, `valid_to`}, `variants`, `fulfillment` {`partner`, `made_to_order`}, `personalizable`, `complete` (false when HEMA's page answered with its basic product data only).
- **categories** - `depth`, `count`, `node_count`, `categories[]` {`name`, `path`, `url`, `level`, `child_count`, `children`}.
- **offers** - `path`, `title`, `label`, `valid_to`, `week`, `section_count`, `count`, `sections[]` {`name`, `week`, `cards[]` {`title`, `subtitle`, `url`, `category`}}.
- **suggestions** - `query`, `count`, `total_results`, `phrases`, `categories[]` {`name`, `product_count`, `url`, `category`}, `products[]` {`sku`, `name`, `url`, `image`, `price`, `currency`} (up to 5), `terms[]` {`term`, `count`, `corrected`}, `content[]` {`name`, `url`}.
- **store** (in stores and store-stock) - `store_id`, `name`, `status` (`open`, `renovation`), `operator` (`hema` or `franchise`), `address` {`street`, `postcode`, `city`, `country_code`}, `latitude`, `longitude`, `distance_km`, `phone`, `hours[]` {`day`, `open`, `close`}, `special_hours[]` {`date`, `type`, `open`, `close`}, `closed_dates`, `services`. Store-stock adds `stock[]`.
- **stores** - `country`, `country_code`, `location`, `radius_km`, `limit`, `count`, `stores[]`. **store-stock** - also `skus`, `in_stock_only`, `summary[]`.
- **store** (`/store`) - the store fields plus `delivery_address`, `country`, `sku` and, with `sku`, `stock` {`sku`, `sellable_units`, `stock_level`, `stock_indicator`, `shelf_locations`, `in_stock`}.
- **reviews** - `sku`, `review_pool`, `review_pool_note`, `sort`, `page`, `offset`, `page_size`, `total_text_reviews`, `total_pages`, `has_more`, `average_rating`, `total_ratings`, `ratings_only`, `recommended`, `not_recommended`, `rating_distribution`, `count`, `reviews[]` {`review_id`, `language`, `rating`, `title`, `text`, `submitted_at`, `experienced_on`, `recommends`, `syndicated`, `verified_purchaser`, `badges`, `helpful_votes`, `not_helpful_votes`}.

## Guardrails

- Name it "HEMA (hema.com, the Dutch variety store)" on first mention, never the HEMA chemical or Hema Pharmaceuticals.
- Store stock: quote `sellable_units` and `stock_level` as "what HEMA's store service reported" with the store, the `fetched_at` time and the article `sku`. Never promise that a store's shelf has the item, never present `online_stock` as a store's stock, and never derive a stock level from the units.
- Prices: quote `price`, `was_price` and `promotion` with the market and the `fetched_at` date. One article number is priced per market; describe differences from the numbers you read, never why. These are online prices; HEMA says online prices can differ from store prices.
- Promotions: quote the mechanic as HEMA writes it ("2+1 gratis", "3+1 offert") with `valid_from` / `valid_to`; label promotions that need the HEMA card; never call a discount real or fake. `discount_percent` is Scavio's arithmetic from `was_price`.
- Lists: 24 per page; never call one page "all products" or present `total` as what was returned. Campaign landing pages have no paging.
- Reviews: say which `review_pool` you read. No reviewer names or identities are returned; never try to identify a reviewer.
- Local-language data: translate names, labels, promotion texts, service names and review texts for the user and keep the original values in quotes and outputs.
- Not available: price history (poll and store), a brands endpoint (HEMA sells its own brand), checkout, cart, ordering or reservations, the photo service and cake ordering, loyalty-card balances, webshops in Luxembourg or Austria, and the United Kingdom and Spain (HEMA left both). This API cannot reserve, add to basket or buy.
- Terms: Scavio does not collect or store HEMA data: each call fetches the public HEMA page at the moment the request asks for it and returns what it shows as JSON, with no response cache. HEMA's terms cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish HEMA product photos, logos, character imagery or reviewer details; link products by `url` instead.
- Never fabricate stock, prices, promotion dates, stores, hours, reviews or ratings. Only return what the API returned, with the `fetched_at` time and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` outside nl, be, fr, de, lu, at; `lu` or `at` on a webshop endpoint; a `language` the country does not have (or any `language` for lu / at); both or neither of `sku` / `url`; a link whose market disagrees with `country` / `language`; more than 12 `skus`; more than 6 `filters`; a `page` above 100 (reviews: above 5); an unknown `sort`; `new_only` on `/new-arrivals`; `/sale` on fr; `/offers` on fr or de; `sinterklaas` on fr or de.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "HEMA has no article 99999991 on nl-nl (or the number does not exist).", "HEMA has no category <path> on this market.", "HEMA has no campaign page <slug> on this market.", "HEMA's store finder found no place for "<query>" in NL.", "HEMA's store service has no store <id>.". Take article numbers, paths and store ids from a previous answer rather than guessing them. A search with no match is a `200` with `total` 0, not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api).
- `502` means HEMA data was temporarily unavailable ("HEMA is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means HEMA is busy ("HEMA is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.75.0
npm install scavio@0.76.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: stock } = await scavio.hema.storeStock({ skus: ["15300147", "10860090"], query: "Utrecht" });
const { data: product } = await scavio.hema.product({ sku: "25101046", country: "fr" });
const { data: found } = await scavio.hema.search({ query: "sokken" });
const { data: baby } = await scavio.hema.category({ category: "baby/babykleding" });
const { data: menu } = await scavio.hema.categories();
const { data: fresh } = await scavio.hema.newArrivals({ country: "de" });
const { data: sale } = await scavio.hema.sale();
const { data: offers } = await scavio.hema.offers({ country: "be", language: "fr" });
const { data: christmas } = await scavio.hema.campaign({ campaign: "christmas" });
const { data: typed } = await scavio.hema.suggestions({ query: "kerst" });
const { data: stores } = await scavio.hema.stores({ country: "lu" });
const { data: store } = await scavio.hema.store({ store_id: "0013", sku: "15300147" });
const { data: reviews } = await scavio.hema.reviews({ sku: "10860090" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.hema.search(...)`, `product`, `category`, `categories`, `new_arrivals`, `sale`, `offers`, `campaign`, `suggestions`, `store_stock`, `stores`, `store` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 13 endpoints as tools: `search_hema`, `get_hema_product`, `get_hema_category`, `get_hema_categories`, `get_hema_new_arrivals`, `get_hema_sale`, `get_hema_offers`, `get_hema_campaign`, `get_hema_suggestions`, `get_hema_store_stock`, `get_hema_stores`, `get_hema_store` and `get_hema_reviews`. HEMA is opt-in: add `hema` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.75.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,hema"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [store stock](https://scavio.dev/docs/hema-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api), [product](https://scavio.dev/docs/hema-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api), [search](https://scavio.dev/docs/hema-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api), [category](https://scavio.dev/docs/hema-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api), [categories](https://scavio.dev/docs/hema-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api), [new arrivals](https://scavio.dev/docs/hema-new-arrivals?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api), [sale](https://scavio.dev/docs/hema-sale?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api), [offers](https://scavio.dev/docs/hema-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api), [campaign](https://scavio.dev/docs/hema-campaign?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api), [suggestions](https://scavio.dev/docs/hema-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api), [stores](https://scavio.dev/docs/hema-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api), [store](https://scavio.dev/docs/hema-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api), [reviews](https://scavio.dev/docs/hema-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api). Overview: [HEMA API](https://scavio.dev/hema-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api).
