# Action.com Store API - Weekly Deals, Prices by Country, Stores

Read Action (action.com), the European non-food discount store, on its 19 storefronts in 16 countries: this week's deals, keyword search, category, brand, new-arrival and seasonal collection lists, one product or up to 60 products per call, the category tree, Action's own brands, search suggestions, the stores nearest a place and one store's opening hours, reviews, and the Action webshop (shop.action.com) in the Netherlands and Belgium. All 16 endpoints return structured JSON at 1 credit per call.

This is Action the discount retailer (www.action.com, founded in the Netherlands). It is not Action S.A. (action.pl, a Polish IT distributor with its own B2B service), GitHub Actions, Action1 or Action Network.

**The job this skill is for: Action weekly deal prices by country.** This week's Action deals with Action's validity dates and week id, the deal `price` next to the `regular_price`, and the same article number priced in each of the 19 Action storefronts in its own currency, plus the stores near a city or postcode with their opening hours, on a dated read.

Eight limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** A not-found (an article the market does not sell, an unknown slug, path, store or EAN) is a `404` charged 1 credit. A refused input (`400`) and an upstream failure (`502`, `503`) are not charged.
- **One article number, a price per market.** `product_code` (7 digits, `3225277`) is the same in every market; the price is set per market, even between euro countries. Never carry one market's price over to another, and never call a market "cheaper" beyond what a dated answer shows.
- **Weekly deals run Wednesday to Tuesday** under one week id in every market (`Promo2026Week47`: 2026-11-18 to 2026-11-24). Action prints the validity without a year (`18-11 t/m 24-11`); `valid_from` / `valid_to` take the year from the week id. The assortment changes every week: re-read on Wednesday.
- **Action does not publish store stock.** Its product pages say so in every language. `/stores` gives the 20 nearest stores with addresses and opening hours, never stock. The webshop's `stock_level` is online stock for webshop items, not stock in a store.
- **Stores are the 20 nearest, and they may cross a border.** A query near Basel returned Swiss, German and French stores; each store carries its own `country_code`. `distance_km` is set only for `lat` / `lng` input.
- **Reviews exist on four storefronts only: nl, de, fr, pl.** Any other `country` is a `400`, not charged. `scope` `local` (default) is the reviews written on that storefront, `international` the other three, `all` both. No reviewer names.
- **The webshop is nl-nl, nl-be and fr-be only, and EAN is only there.** action.com product pages carry no EAN; `/webshop-search` and `/webshop-product` do.
- **Data in each storefront's language.** Titles, descriptions, labels, facet names, day names and review texts come back in Dutch, German, French, Polish and so on, as Action writes them: translate them for the user, never alter the values.

Action has no public product, price, deal or store API. Its suppliers work through a supplier portal for their own transactions, and Action says store stock can only be checked in the store itself. This skill reads the public action.com and shop.action.com pages instead, with one Scavio key.

See also: for IKEA prices by country use `ikea-api`; for bol.com competitor prices in the Netherlands and Belgium use `bol-com-api`; for Carrefour France use `carrefour-api`; for Media Expert in Poland use `media-expert-api`; for prices across retailers use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Read this week's Action deals (Weekactie, Wochenangebote, la semaine d'Action, gazetka deals) on one market, with the validity dates and week id
- Compare one Action article's price across Action's countries and currencies, or price up to 60 article numbers on one market
- Read Action's Black Friday, Christmas or other seasonal collection, or its new arrivals
- Search Action by keyword, or list a category or one of Action's own brands, sorted by price or newest, filtered by department, price band, brand or new
- Find the Action stores near a city, town, postcode or coordinates, and one store's opening hours for the next 7 days
- Read Action customer reviews on the Dutch, German, French or Polish storefront
- Read the Action webshop (Netherlands and Belgium): online deals, EAN, online stock level, order limit and shipping cost
- Resolve category paths, brand slugs, filter values and search suggestions before a search

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures (median), categories took about 1 second, category, products and weekly deals 1-1.5, search, store, brand, collection and suggestions 1.5, reviews 2, product 2, stores 2.5, webshop search 3 and webshop product 4.5. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/action/search` | Products for a keyword, 24 per page, with total, pages and the facets to filter by | 1 |
| `POST /api/v1/action/product` | One product on one market by article number or link: specifications, highlights, store aisle, category, related products | 1 |
| `POST /api/v1/action/products` | Up to 60 article numbers priced on one market; codes the market does not sell listed in `not_sold` | 1 |
| `POST /api/v1/action/weekly-deals` | This week's deals on one market with `week_id`, `valid_from`, `valid_to` and (Belgium) the Action Plus card deals, 23 per page | 1 |
| `POST /api/v1/action/category` | One category's products by path, with filters, sort and paging | 1 |
| `POST /api/v1/action/categories` | The category tree (15 departments, about 300 categories in 3 levels) | 1 |
| `POST /api/v1/action/brand` | One brand's products by slug | 1 |
| `POST /api/v1/action/brands` | Action's own brands (54 private labels in the capture, e.g. Max & More) | 1 |
| `POST /api/v1/action/new-arrivals` | Action's new products on one market (191 in the Dutch capture) | 1 |
| `POST /api/v1/action/collection` | One seasonal collection page (`black-friday`, `kerst`, `sinterklaas`, `basics`) | 1 |
| `POST /api/v1/action/suggestions` | Search suggestions for a partial query, a category hint and up to 5 products | 1 |
| `POST /api/v1/action/stores` | The 20 Action stores nearest a city, town, postcode or `lat` / `lng`, with address and 7 dated days of hours | 1 |
| `POST /api/v1/action/store` | One store by reference, link, slug or `store_id`: address, coordinates, opening and closing dates, 7 dated days of hours | 1 (by `store_id` it reads two sources, still 1) |
| `POST /api/v1/action/reviews` | One article's reviews on nl, de, fr or pl, up to 100 per call with offset paging | 1 (`scope` `all` reads both review sets, still 1) |
| `POST /api/v1/action/webshop-search` | The Action webshop (shop.action.com) by keyword or category slug, with EAN, online stock level and order limit | 1 |
| `POST /api/v1/action/webshop-product` | One webshop product by EAN or link: stock level, order limits, shipping cost, release and end dates, supplier, the other webshop markets | 1 |

## Markets

`country` picks the storefront (default `nl`); `language` matters only in Belgium and Switzerland.

| `country` | Storefront | `language` | Currency |
|---|---|---|---|
| `nl` | Netherlands (nl-nl) | nl | EUR |
| `be` | Belgium (nl-be, fr-be) | `nl` (default) or `fr` | EUR |
| `fr` | France (fr-fr) | fr | EUR |
| `lu` | Luxembourg (fr-lu) | fr | EUR |
| `de` | Germany (de-de) | de | EUR |
| `at` | Austria (de-at) | de | EUR |
| `ch` | Switzerland (de-ch, fr-ch, it-ch) | `de` (default), `fr` or `it` | CHF |
| `it` | Italy (it-it) | it | EUR |
| `es` | Spain (es-es) | es | EUR |
| `pt` | Portugal (pt-pt) | pt | EUR |
| `pl` | Poland (pl-pl) | pl | PLN |
| `cz` | Czechia (cs-cz) | cs | CZK |
| `sk` | Slovakia (sk-sk) | sk | EUR |
| `ro` | Romania (ro-ro) | ro | RON |
| `hr` | Croatia (hr-hr) | hr | EUR |
| `si` | Slovenia (sl-si) | sl | EUR |

- Leave `language` out in a one-language country: a language the country does not have is a `400`. Every answer echoes `country`, `language`, `market` (e.g. `nl-nl`) and `currency`.
- A product, category, brand, collection or store link carries its own market: send the link alone, or with a `country` / `language` that agrees with it (a mismatch is a `400`).
- Reviews: `nl`, `de`, `fr`, `pl` only. Webshop: `nl`, or `be` with `language` `nl` or `fr`.
- Not served: Bulgaria (Action's Bulgarian site has no catalogue or stores) and any country Action is not in.
- Action reported EUR 12.8 bn net sales in the first nine months of 2026 (+14%) and 3,530 stores in 16 countries (press release, 2026-11-12); 3i Group owns 67.5% (3i half-year report). Quote these with their sources, never from the samples.

## Prices: one article, a price per market

Every list item and product carries:

| Field | Meaning |
|---|---|
| `product_code` | Action's article number, 7 digits, the same in every market |
| `price` | The price on that market, a number in `currency` |
| `regular_price` | Action's struck-through price, as shown (`null` when none). On a weekly deal it is the price outside the deal |
| `discount_percent` | Computed by Scavio from `regular_price` to `price` |
| `price_note` | Action's note on the struck-through price, as shown. On the Polish storefront it reads "Najniższa cena z 30 dni przed obniżką" (the lowest price of the 30 days before the reduction): there `regular_price` is that 30-day low |
| `unit_price` | As shown, e.g. `€ 1,00/m`, `€ 0,82/st` (per piece) |
| `is_deal`, `deal` | `deal` {`label`, `valid_from`, `valid_to`, `loyalty_card`, `loyalty_label`} on a weekly deal |
| `labels[]` | {`code` (`deal`, `new`, `sustainable_choice`, `loyalty_card_deal`), `label`, `note`} as Action shows them |

The same deal across the 19 storefronts (weekly-deals page 1, 2026-11-22, week `Promo2026Week47`), article `3011901` (a 15 cm Christmas gnome or elf, "Kerstgnoom of kerstelf" in Dutch):

| Market | `price` | `regular_price` |
|---|---|---|
| nl, de, si | EUR 0.82 | EUR 0.99 |
| at, fr, lu, it, es, pt, hr, sk | EUR 0.84 | EUR 0.99 |
| ch (de, fr, it) | CHF 0.99 | CHF 1.19 |
| pl | PLN 3.79 | PLN 4.49 |
| cz | CZK 19.90 | CZK 25.90 |
| ro | RON 3.95 | RON 4.99 |

It was not on page 1 of either Belgian deal grid. A non-deal article in the same read: `3218276` (an LED Christmas tree) read EUR 14.95 (regular 19.95) in Germany, Austria, Luxembourg and Italy, EUR 21.95 (regular 26.95) in Slovenia, and RON 79.95 in Romania. `3225277` (a 5 m LED pine garland) read EUR 4.99 in the Netherlands, CZK 129.90 in Czechia and RON 24.95 in Romania, and Slovenia answered `404` (not sold there).

- Report differences descriptively, from the numbers and the `fetched_at` date: "on 2026-11-22 the Slovenian storefront showed EUR 21.95, the German one EUR 14.95". Never say why a market is priced higher, and never call a discount fake or real.
- These are Action's online prices per storefront. Action says a store's price can differ: say "the online price for <country>", never "the price in every store".
- Convert currencies yourself at one dated rate and say so; Scavio does not convert.

## Weekly deals

`/action/weekly-deals` takes `country` / `language` and the list parameters.

- The answer adds `week_id` (`Promo2026Week47`), `label` (as shown: `18-11 t/m 24-11` in Dutch, `18.11. bis 24.11.` in German, `18/11 au 24/11` in French), `valid_from` and `valid_to` (ISO dates, `2026-11-18` and `2026-11-24`) and `loyalty_deals`.
- Deals run Wednesday to Tuesday, the same week id on every storefront. Each deal item also carries its own `deal` dates. In the capture all 19 storefronts read `Promo2026Week47`, 2026-11-18 to 2026-11-24, with 129 (Slovenia) to 185 (France) deals; the Netherlands had 183.
- **Belgium adds Action Plus loyalty-card deals:** `loyalty_deals[]` (8 on both Belgian storefronts in the capture) are items with `deal.loyalty_card: true` and `deal.loyalty_label` ("avec Action Plus" in French). Label them as card deals, separate from the general grid. Other storefronts return an empty `loyalty_deals`.
- 23 deals per page; `total_pages` says how deep the grid goes (8 pages for 183 deals). Call every page for the full week.
- To track deals, read every Wednesday and store each answer with `fetched_at`: kept, new and dropped deals come from comparing your stored weeks. Scavio keeps no history.
- Black Friday: `/action/collection` with `{"collection": "black-friday"}` returned 97 items on the Dutch storefront (5 pages); 16 of the 24 items on page 1 were deals dated 2026-11-18 to 2026-11-24, the week's deal dates. Quote dates from the answer, not from memory.

## Stores

`/action/stores` takes one of `query` (a city, town or postcode) or `lat` + `lng`, plus `country` / `language`.

- The answer: `query`, `latitude`, `longitude`, `complete`, `count` (always up to 20), `countries` (the country codes present) and `stores[]` {`store_id`, `name`, `store` (the input of `/action/store`), `url`, `country_code`, `address` {`street`, `house_number`, `street2`, `postcode`, `city`, `country`}, `latitude`, `longitude`, `distance_km`, `opening_date`, `closing_date`, `hours[]` {`date`, `day`, `closed`, `open`, `close`}}.
- Always the 20 nearest stores, no paging, and they may cross a border: in the captures `Luxembourg` returned stores in Luxembourg, Belgium, France and Germany, and a point in Basel returned Basel (CH, 2.94 km), Weil am Rhein (DE, 3.94 km) and Saint-Louis (FR, 5 km) out to 56.63 km. Use each store's `country_code`; the store's prices are its own country's.
- `distance_km` is set only for `lat` / `lng` input (nearest first); for a city or postcode it is `null`.
- `hours` are 7 dated days starting today, with `day` in the storefront's language (`Zondag`, `Maandag` = Sunday, Monday): quote the `date`, translate the `day`. In the Amsterdam capture Kinkerstraat opened 10:00-18:00 on Sunday 2026-11-22 and 08:30-21:00 Monday to Saturday.
- `opening_date` set in the future marks a store announced to open later; `closing_date` marks one announced to close.
- `complete: false` means the store finder was down and the stores came from Action's store list: `store_id`, coordinates, distance and dates, but no address or hours. Say so, and retry later for hours.
- No stock, no phone and no services: Action publishes none of them.

## Workflow

1. **Find the article:** `/action/search` with `query` in the storefront's language (`kerst`, `weihnachten`, `świąteczne`, `opbergbox`), `/action/weekly-deals`, `/action/collection`, or `/action/category` with a `path` from `/action/categories`. Each item has `product_code`, `price`, `regular_price` and `deal`.
2. **Narrow:** send `category_filter`, `price_range`, `brand_filter` or `new_only` with a `facets[].values[].value` from an earlier answer (each facet names its `input` field). The price bands follow the market's currency (`<1`, `1-2`, `2-5`, `5-10`, `10-20`, `>20` in EUR).
3. **Price it in every market:** one call per market to `/action/products` with up to 60 `product_codes` (1 credit each call); read `not_sold` for codes that market does not carry. 16 calls cover the 16 countries; add `language` for the other Belgian and Swiss storefronts when you need their titles.
4. **One product in full:** `/action/product` with `product_code` and `country`, or the action.com `url`: specifications, highlights, `aisle` (the store aisle Action names), `brand_info.slug` for `/action/brand`.
5. **Stores:** `/action/stores` with `query` or `lat` / `lng`, then `/action/store` with `stores[].store` or `store_id` for one store.
6. **Reviews:** `/action/reviews` with `product_code` and `country` `nl`, `de`, `fr` or `pl`.
7. **Webshop (nl / be):** `/action/webshop-search`, then `/action/webshop-product` with the item's `ean`.
8. **Watching prices or deals:** there is no history. Poll the same articles on a schedule (every Wednesday for deals) and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`), brand (`/brand`), new arrivals (`/new-arrivals`), weekly deals (`/weekly-deals`), collection (`/collection`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Search text, 1-200 chars; the storefront's language works best |
| `category` | string | category: required | A category path (`categories[].path`, e.g. `wonen` or `wonen/woonaccessoires`) or its action.com/<market>/c/... link |
| `brand` | string | brand: required | `brands[].slug` or a product's `brand_info.slug` (`max-more`, `magic-village`) or its action.com/<market>/brand/<slug>/ link |
| `collection` | string | collection: required | A seasonal moment slug (`black-friday`, `kerst`, `sinterklaas`, `basics`) or its action.com/<market>/moment/<slug>/ link |
| `country` / `language` | string | `nl` / the country's first | See Markets |
| `sort` | string | `relevance` | `relevance` (Action's own order), `price_asc`, `price_desc`, `newest` |
| `page` | integer | 1 | 1-200; 24 products a page (23 on weekly deals); `total_pages` says how deep the list goes |
| `category_filter` | string | none | A department: a value of `facets[facet=category].values[].value`, in the storefront's language (e.g. `Hobby`) |
| `price_range` | string | none | A price band: a value of `facets[facet=price_range].values[].value` (`2-5`, `<1`, `>20`) |
| `brand_filter` | string | none | A brand: a value of `facets[facet=brand].values[].value` (e.g. `Disney`). Does not apply to `/brand` |
| `new_only` | boolean | false | Only products with Action's new label. Does not apply to `/new-arrivals` (every item is new) |

A search with no match answers `200` with `total` 0.

### Product (`/product`) and products (`/products`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_code` | string or integer | product: one of | Action article number, 7 digits (`3225277`) |
| `url` | string | product: one of | An action.com product link (https://www.action.com/<market>/p/<code>/<name>/); the market comes from the link. Send exactly one of `product_code`, `url` |
| `product_codes` | array | products: required | 1 to 60 article numbers, priced on one market |
| `country` / `language` | string | `nl` | See Markets |

### Categories (`/categories`), brands (`/brands`), suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `depth` | integer | 3 | Categories: levels, 1-3 |
| `query` | string | brands: optional; suggestions: required | Brands whose name contains this text / what the shopper has typed so far (1-100 chars) |
| `country` / `language` | string | `nl` | See Markets |

### Stores (`/stores`) and store (`/store`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | stores: one of | A city, town or postcode (`Amsterdam`, `5672 GM`, `Kraków`) |
| `lat` / `lng` | number | stores: one of | A point; the 20 nearest stores with `distance_km`. Send both |
| `store` | string | store: one of | `stores[].store` (`/nl-nl/winkels/amsterdam-kinkerstraat/`), its action.com link, or its slug (`amsterdam-kinkerstraat`) with `country` |
| `store_id` | string | store: one of | `stores[].store_id` (`1260`, `3A11`). Send exactly one of `store`, `store_id` |
| `country` / `language` | string | `nl` | See Markets |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_code` | string or integer | required | Action article number |
| `country` | string | `nl` | `nl`, `de`, `fr` or `pl`; any other is a `400`, not charged |
| `scope` | string | `local` | `local` (reviews written on this storefront, in its language), `international` (the reviews written on the other three), `all` (both; `offset` + `limit` up to 100) |
| `sort` | string | `relevant` | `relevant` (Action's own order), `newest`, `oldest`, `highest`, `lowest` |
| `rating` | array | all | Star ratings to include, e.g. `[1, 2]` |
| `query` | string | none | Only reviews that mention this text |
| `limit` | integer | 20 | 1-100 per call |
| `offset` | integer | 0 | Reviews to skip (paging). Page past 100 with `scope` `local` or `international` |

### Webshop search (`/webshop-search`) and webshop product (`/webshop-product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: one of | Search text (`stofzuiger`) |
| `category` | string | search: one of | A webshop category slug (the /c/<slug> part of a shop.action.com link, e.g. `alle-tijdelijke-deals`). Send exactly one of `query`, `category` |
| `page` | integer | 1 | 24 per page |
| `ean` | string | product: one of | The product's EAN (webshop `items[].ean`, 8 or 13 digits) |
| `url` | string | product: one of | A shop.action.com product link. Send exactly one of `ean`, `url` |
| `country` | string | `nl` | `nl` or `be` |
| `language` | string | `nl` | For `be`: `nl` or `fr` |

## Examples

### Weekly deals

```bash
curl -X POST https://api.scavio.dev/api/v1/action/weekly-deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "nl"}'
```

Captured `data` (2026-11-22, 1 credit; 2 of 23 items shown, `image` and `facets` omitted):

```json
{
  "country": "nl",
  "language": "nl",
  "market": "nl-nl",
  "currency": "EUR",
  "title": "Weekactie aanbiedingen in Nederland | Action NL",
  "week_id": "Promo2026Week47",
  "label": "18-11 t/m 24-11",
  "valid_from": "2026-11-18",
  "valid_to": "2026-11-24",
  "loyalty_deals": [],
  "sort": "relevance",
  "page": 1,
  "page_size": 23,
  "total": 183,
  "total_pages": 8,
  "has_more": true,
  "count": 23,
  "items": [
    {
      "product_code": "3011901",
      "title": "Kerstgnoom of kerstelf",
      "description": "15 cm | diverse varianten",
      "url": "https://www.action.com/nl-nl/p/3011901/kerstgnoom-of-kerstelf/",
      "brand": null,
      "price": 0.82,
      "regular_price": 0.99,
      "currency": "EUR",
      "unit_price": "€ 0,82/st",
      "discount_percent": 17,
      "price_note": null,
      "available": true,
      "is_new": false,
      "is_deal": true,
      "deal": { "label": "18-11 t/m 24-11", "valid_from": "2026-11-18", "valid_to": "2026-11-24", "loyalty_card": false, "loyalty_label": null },
      "labels": [{ "code": "deal", "label": "Weekactie", "note": "18-11 t/m 24-11" }],
      "rating": 4.8,
      "review_count": 16,
      "energy_label": null,
      "has_warnings": false
    },
    {
      "product_code": "3225346",
      "title": "Walkietalkies met camera",
      "description": "2-delig | diverse kleuren",
      "url": "https://www.action.com/nl-nl/p/3225346/walkietalkies-met-camera/",
      "brand": null,
      "price": 11.89,
      "regular_price": 14.95,
      "currency": "EUR",
      "unit_price": "€ 11,89/st",
      "discount_percent": 20,
      "price_note": null,
      "available": true,
      "is_new": false,
      "is_deal": true,
      "deal": { "label": "18-11 t/m 24-11", "valid_from": "2026-11-18", "valid_to": "2026-11-24", "loyalty_card": false, "loyalty_label": null },
      "labels": [{ "code": "deal", "label": "Weekactie", "note": "18-11 t/m 24-11" }],
      "rating": 2.5,
      "review_count": 2,
      "energy_label": null,
      "has_warnings": false
    }
  ]
}
```

"Weekactie" is Action's weekly deal; "t/m" means "up to and including". The answer's facets split the 183 deals into price bands (`Tot € 1` = under EUR 1: 20, `€ 2 - 5`: 67) and departments (`Eten & drinken` = food and drink: 46). On the French-language Belgian storefront (`{"country": "be", "language": "fr"}`) the same walkie-talkies (`3225346`) were an Action Plus card deal at EUR 11.89: `deal.loyalty_card: true`, `loyalty_label` "avec Action Plus", label code `loyalty_card_deal`.

### Products (one market, up to 60 codes)

```bash
curl -X POST https://api.scavio.dev/api/v1/action/products \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_codes": ["3225277", "3011615", "3225488"], "country": "nl"}'
```

Captured `data` (2026-11-22, 1 credit; 2 of 3 items shown, `image` omitted):

```json
{
  "country": "nl",
  "language": "nl",
  "market": "nl-nl",
  "currency": "EUR",
  "requested": ["3225277", "3011615", "3225488"],
  "count": 3,
  "not_sold": [],
  "items": [
    {
      "product_code": "3225277",
      "title": "Dennenslinger met led",
      "description": "5 m | 60 led | diverse varianten",
      "url": "https://www.action.com/nl-nl/p/3225277/dennenslinger-met-led/",
      "brand": null,
      "price": 4.99,
      "regular_price": null,
      "currency": "EUR",
      "unit_price": "€ 1,00/m",
      "discount_percent": null,
      "price_note": null,
      "available": true,
      "is_new": false,
      "is_deal": false,
      "deal": null,
      "labels": [],
      "rating": 5,
      "review_count": 1,
      "energy_label": null,
      "has_warnings": false
    },
    {
      "product_code": "3225488",
      "title": "Besneeuwde kunstkerstboom",
      "description": "55 x 180 cm",
      "url": "https://www.action.com/nl-nl/p/3225488/besneeuwde-kunstkerstboom/",
      "brand": null,
      "price": 14.95,
      "regular_price": 19.95,
      "currency": "EUR",
      "unit_price": "€ 14,95/st",
      "discount_percent": 25,
      "price_note": null,
      "available": true,
      "is_new": false,
      "is_deal": true,
      "deal": { "label": "18-11 t/m 24-11", "valid_from": "2026-11-18", "valid_to": "2026-11-24", "loyalty_card": false, "loyalty_label": null },
      "labels": [{ "code": "deal", "label": "Weekactie", "note": "18-11 t/m 24-11" }, { "code": "sustainable_choice", "label": "Duurzamere keuze", "note": null }],
      "rating": 5,
      "review_count": 1,
      "energy_label": null,
      "has_warnings": false
    }
  ]
}
```

A batch of 60 codes on the Romanian storefront returned 56 items and 4 codes in `not_sold`, for 1 credit. If none of the codes is sold on that market the answer is a `404` (1 credit). `rating` and `review_count` here can differ from the product page's (`/action/product` for `3225277` read 4.8 from 4 reviews in the captures): quote the one you read.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/action/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "Amsterdam", "country": "nl"}'
```

Captured `data` (2026-11-22, 1 credit; 1 of 20 stores shown):

```json
{
  "country": "nl",
  "language": "nl",
  "market": "nl-nl",
  "currency": "EUR",
  "query": "Amsterdam",
  "latitude": null,
  "longitude": null,
  "complete": true,
  "count": 20,
  "countries": ["NL"],
  "stores": [
    {
      "store_id": "1260",
      "name": "Amsterdam",
      "store": "/nl-nl/winkels/amsterdam-kinkerstraat/",
      "url": "https://www.action.com/nl-nl/winkels/amsterdam-kinkerstraat/",
      "country_code": "NL",
      "address": { "street": "Kinkerstraat", "house_number": "214-222", "street2": null, "postcode": "1053 EM", "city": "Amsterdam", "country": "NL" },
      "latitude": 52.365814,
      "longitude": 4.866408,
      "distance_km": null,
      "opening_date": "2012-10-25",
      "closing_date": null,
      "hours": [
        { "date": "2026-11-22", "day": "Zondag", "closed": false, "open": "10:00", "close": "18:00" },
        { "date": "2026-11-23", "day": "Maandag", "closed": false, "open": "08:30", "close": "21:00" },
        { "date": "2026-11-24", "day": "Dinsdag", "closed": false, "open": "08:30", "close": "21:00" },
        { "date": "2026-11-25", "day": "Woensdag", "closed": false, "open": "08:30", "close": "21:00" },
        { "date": "2026-11-26", "day": "Donderdag", "closed": false, "open": "08:30", "close": "21:00" },
        { "date": "2026-11-27", "day": "Vrijdag", "closed": false, "open": "08:30", "close": "21:00" },
        { "date": "2026-11-28", "day": "Zaterdag", "closed": false, "open": "08:30", "close": "21:00" }
      ]
    }
  ]
}
```

`distance_km` is `null` because the input was a city; send `lat` / `lng` for distances. `/action/store` with `{"store": "/nl-nl/winkels/amsterdam-kinkerstraat/"}` returns the same store on its own (1 credit), and `{"store_id": "3A11", "country": "de"}` returned Berlin-Mitte.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/action/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_code": "3225277", "country": "nl"}'
```

Captured `data` (2026-11-22, 1 credit; trimmed: `image`, `images`, `long_description`, `related`, `related_categories` and 12 of 14 `specifications` dropped):

```json
{
  "country": "nl",
  "language": "nl",
  "market": "nl-nl",
  "currency": "EUR",
  "requested": "3225277",
  "product_code": "3225277",
  "title": "Dennenslinger met led",
  "description": "5 m | 60 led | diverse varianten",
  "url": "https://www.action.com/nl-nl/p/3225277/dennenslinger-met-led/",
  "brand": null,
  "price": 4.99,
  "regular_price": null,
  "unit_price": "€ 1,00/m",
  "discount_percent": null,
  "price_note": null,
  "available": true,
  "is_new": false,
  "is_deal": false,
  "deal": null,
  "labels": [],
  "rating": 4.8,
  "review_count": 4,
  "energy_label": null,
  "has_warnings": false,
  "brand_info": null,
  "highlights": ["8 verschillende lichstanden", "Met handige timerfunctie: 6 uur aan, 18 uur uit"],
  "specifications": [{ "name": "Kleur", "value": "Groen, Wit" }, { "name": "Aantal benodigde batterijen", "value": "3" }],
  "aisle": null,
  "deposit": null,
  "category": { "name": "Wonen", "path": "wonen", "url": "https://www.action.com/nl-nl/c/wonen/" },
  "subcategory": { "name": "Decoratie", "path": "wonen/woonaccessoires", "url": "https://www.action.com/nl-nl/c/wonen/woonaccessoires/" },
  "sustainability": null,
  "warning_label": null,
  "hazards": { "biocide": false, "dangerous_good": false, "plant_protection": false },
  "availability": "instock"
}
```

A 5 m LED pine garland with 60 LEDs, 8 light modes and a 6-hours-on timer ("Dennenslinger met led"). `availability` is Action's online mark, not stock in a store. The same code on the Slovenian storefront answered `404` ("Action does not sell article 3225277 on sl-si"), charged 1 credit.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/action/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_code": "3224838", "country": "nl", "scope": "all", "sort": "newest"}'
```

Captured `data` (2026-11-22, 1 credit; 1 of 20 reviews shown):

```json
{
  "country": "nl",
  "language": "nl",
  "market": "nl-nl",
  "currency": "EUR",
  "product_code": "3224838",
  "scope": "all",
  "sort": "newest",
  "rating": [],
  "query": null,
  "offset": 0,
  "limit": 20,
  "total": 26,
  "local_total": 6,
  "international_total": 20,
  "count": 20,
  "has_more": true,
  "reviews": [
    {
      "review_id": "1237417986",
      "language": "fr-FR",
      "rating": 5,
      "title": "Super chaud et tresdoux",
      "text": "J ai hacheter cette article ce mois si et j en suis tres contente , j irai en racheterun pour ma fille car trop bien .",
      "reviewed_at": "2026-11-19T09:24:48.000+00:00",
      "recommends": null,
      "aspect_ratings": [{ "aspect": "Quality", "name": "Kwaliteit", "rating": 5 }, { "aspect": "EaseOfUse", "name": "Gebruiksgemak", "rating": 5 }, { "aspect": "Value", "name": "Prijs-kwaliteitverhouding", "rating": 5 }, { "aspect": "Fit", "name": "Pasvorm", "rating": 5 }],
      "pros": [],
      "cons": []
    }
  ]
}
```

6 reviews were written on the Dutch storefront and 20 on the other three; this one was written in French (`language` `fr-FR`: "super warm and very soft", the buyer will buy another for her daughter). `aspect_ratings[].name` is in the storefront's language (Dutch here), `aspect` is the same key everywhere. Some reviews are a rating with `title` and `text` both `null`. With `scope` `local` the German storefront read 5 reviews for the same article. Quote review text as written, translated for the user.

### Webshop

```bash
curl -X POST https://api.scavio.dev/api/v1/action/webshop-product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ean": "8718969571098", "country": "nl"}'
```

Captured `data` (2026-11-22, 1 credit; trimmed to the commerce fields):

```json
{
  "market": "nl-nl",
  "currency": "EUR",
  "requested": "8718969571098",
  "ean": "8718969571098",
  "product_code": "3227504",
  "title": "Hyundai TwinSpin 360 Pro draadloze steelstofzuiger",
  "brand": "Hyundai",
  "price": 89.95,
  "regular_price": null,
  "stock_level": "HIGH",
  "stock_label": "Op voorraad",
  "order_limit": 2,
  "order_minimum": 1,
  "order_multiple": 1,
  "shipping_cost": 5.99,
  "availability": { "status": "AVAILABLE", "release_date": "2026-11-21T10:45:00.850Z", "end_date": null },
  "is_deal": true,
  "is_new": true,
  "promo_label": "Alleen online superdeals",
  "supplier": { "name": "TIC EUROPE BV", "address": "Vang 16\r\n4461TX Halsteren\r\nThe Netherlands\r\nwww.alleenonline.nl" },
  "other_markets": [
    "https://shop.action.com/fr-be/p/8718969571098/aspirateur-balai-sans-fil-hyundai-twinspin-360-pro",
    "https://shop.action.com/nl-be/p/8718969571098/hyundai-twinspin-360-pro-draadloze-steelstofzuiger",
    "https://shop.action.com/nl-nl/p/8718969571098/hyundai-twinspin-360-pro-draadloze-steelstofzuiger"
  ]
}
```

A cordless stick vacuum sold online only ("Alleen online superdeals" = online-only super deals; "Op voorraad" = in stock online), at most 2 per order, EUR 5.99 shipping. `stock_level` runs from `HIGH` to `SOLD_OUT` and is the webshop's online stock, never a store's. On `/action/webshop-search` (`{"query": "stofzuiger"}`: 9 items) one Hyundai vacuum read `SOLD_OUT`, and `shipping_cost` was `null` on the list items: read it from the product.

### Search, category, brands, new arrivals, collection, categories and suggestions

- `/search` with `{"query": "kerst"}` (Christmas, Dutch): 413 products in 18 pages, facets `Categorieën` (departments, 11 values), `Prijs` (price bands, 6), `Merk` (brand, 22) and `Assortiment` (new). `{"query": "świąteczne", "country": "pl"}`: 189 products in PLN, the reduced ones with `price_note` "Najniższa cena z 30 dni przed obniżką".
- `/category` with `{"category": "wonen/woonaccessoires"}` (home accessories): 722 products in 31 pages.
- `/brands`: 54 own brands such as `mini-matters`, `home-essentials`, `studio-home`; `/brand` with `{"brand": "max-more"}`: 42 Max & More products in 2 pages.
- `/new-arrivals`: 191 new products on the Dutch storefront, every item `is_new: true`.
- `/collection` with `{"collection": "black-friday"}`: 97 items (`collection_tag` `super-deals-black-friday`).
- `/categories`: 15 departments and 319 nodes at depth 3, from `Wonen` (home) and `Keuken` (kitchen) to `Kantoor & school` (office and school); `path` (e.g. `kantoor--school`) is the input of `/category`.
- `/suggestions` with `{"query": "opberg"}` (storage): `opbergbox`, `opbergpoef`, `opbergbox met deksel`, `opbergdoos`, `opbergen`, the category hint `Huishouden` (household) and 5 products with prices.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def action(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/action/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. This week's deals on one market, every page (1 credit per page)
deals, page = [], 1
while True:
    res = action("weekly-deals", {"country": "nl", "page": page})
    d = res["data"]
    for i in d["items"]:
        deals.append((d["week_id"], d["valid_from"], d["valid_to"], i["product_code"], i["title"], i["price"], i["regular_price"]))
    if not d["has_more"]:
        break
    page += 1
print(len(deals), "deals in", deals[0][0] if deals else "no week")

# 2. The same article numbers priced in every country (1 credit per country)
codes = ["3011901", "3218276", "3225277"]
for country in ("nl", "be", "fr", "lu", "de", "at", "ch", "it", "es", "pt", "pl", "cz", "sk", "ro", "hr", "si"):
    d = action("products", {"product_codes": codes, "country": country})["data"]
    for i in d["items"]:
        print(country, i["product_code"], i["price"], d["currency"], "deal" if i["is_deal"] else "")
    if d["not_sold"]:
        print(country, "not sold:", d["not_sold"])
# A market that sells none of the codes answers 404 (raise_for_status raises): catch it per country.

# 3. The 20 stores nearest a point, with distances and today's hours
d = action("stores", {"lat": 47.5596, "lng": 7.5886, "country": "ch"})["data"]
for s in d["stores"]:
    today = s["hours"][0] if s["hours"] else None
    print(s["country_code"], s["name"], s["distance_km"], today and (today["open"], today["close"]))

# Store each answer with fetched_at and run this every Wednesday: that stored series is
# your deal and price history (Action shows only the current week).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `country`, `language`, `market` and `currency`.

- **item** (search, category, brand, new arrivals, weekly deals, collection, products, suggestions) - `product_code`, `title`, `description`, `url`, `image`, `brand`, `price`, `regular_price`, `currency`, `unit_price`, `discount_percent`, `price_note`, `available`, `is_new`, `is_deal`, `deal` {`label`, `valid_from`, `valid_to`, `loyalty_card`, `loyalty_label`}, `labels[]` {`code`, `label`, `note`}, `rating`, `review_count`, `energy_label`, `has_warnings`.
- **lists** (search, category, brand, new arrivals, weekly deals, collection) - `title`, `filters` {`category_filter`, `brand_filter`, `price_range`, `new_only`}, `sort`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `items[]`, `facets[]` {`facet` (`category`, `price_range`, `brand`, `new`), `input` (the field to send a value back in), `name`, `values[]` {`name`, `value`, `count`, `selected`}}. Search adds `query`; category `category`; brand `brand`; collection `collection`, `collection_tag`; weekly deals `week_id`, `label`, `valid_from`, `valid_to`, `loyalty_deals[]`.
- **product** - the item fields plus `requested`, `images`, `brand_info` {`name`, `brand_id`, `own_brand`, `slug`, `url`}, `long_description`, `highlights`, `specifications[]` {`name`, `value`}, `aisle`, `deposit`, `category` / `subcategory` {`name`, `path`, `url`}, `related_categories`, `sustainability` {`title`, `certifications`}, `warning_label`, `hazards` {`biocide`, `dangerous_good`, `plant_protection`}, `availability`, `related[]` {`product_code`, `title`, `url`, `image`, `price`, `regular_price`, `is_deal`}.
- **products** - `requested`, `count`, `not_sold`, `items[]`.
- **categories** - `depth`, `count`, `node_count`, `categories[]` {`category_id`, `name`, `path`, `url`, `level`, `child_count`, `children`}.
- **brands** - `query`, `total_brands`, `count`, `brands[]` {`name`, `slug`, `url`, `image`}.
- **suggestions** - `query`, `count`, `suggestions[]` (search terms), `category_suggestion` {`query`, `category`}, `products[]` (items, up to 5).
- **stores** - `query`, `latitude`, `longitude`, `complete`, `count`, `countries`, `stores[]` (see Stores). **store** - one store's fields: `store_id`, `name`, `store`, `url`, `country_code`, `address`, `latitude`, `longitude`, `opening_date`, `closing_date`, `hours[]`.
- **reviews** - `product_code`, `scope`, `sort`, `rating`, `query`, `offset`, `limit`, `total`, `local_total`, `international_total`, `count`, `has_more`, `reviews[]` {`review_id`, `language`, `rating`, `title`, `text`, `reviewed_at`, `recommends`, `aspect_ratings[]` {`aspect`, `name`, `rating`}, `pros`, `cons`}.
- **webshop search** - `query`, `category`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`ean`, `product_code`, `title`, `subtitle`, `url`, `image`, `brand`, `price`, `regular_price`, `currency`, `discount_percent`, `stock_level`, `stock_label`, `order_limit`, `shipping_cost`, `is_deal`, `is_new`, `promo_label`}.
- **webshop product** - the webshop item fields plus `requested`, `images`, `order_minimum`, `order_multiple`, `availability` {`status`, `release_date`, `end_date`}, `description`, `highlights`, `specifications`, `supplier` {`name`, `address`}, `other_markets`.

## Guardrails

- Name it "Action (action.com), the European non-food discount store" on first mention. Never confuse it with Action S.A. (action.pl), and never link action.pl.
- Store stock: Action does not publish it. Never report an Action store as having an item in stock, and never present the webshop `stock_level` or a product's `availability` as stock in a store.
- Prices: quote `price` and `regular_price` with the `currency`, the market and the `fetched_at` date. One article number is priced per market; describe differences from the numbers you read, never why, and never call one market cheaper beyond a dated answer. These are online prices per storefront; Action says a store's price can differ.
- Weekly deals: quote `week_id`, `valid_from` and `valid_to`; deals run Wednesday to Tuesday and change every week. Label Belgium's Action Plus card deals as card deals.
- Lists: 24 per page (23 on weekly deals); never call one page "all products" or present `total` as what was returned.
- Reviews: nl, de, fr and pl only. No reviewer names or identities are returned; never try to identify a reviewer. Say which `scope` you read.
- Local-language data: translate titles, labels, day names and review texts for the user and keep the original values in quotes and outputs.
- Not available: store stock (Action does not publish it), price history (poll and store), leaflets (the weekly folder or Prospekt as pages), checkout, cart or app-only offers, phone numbers or services of stores, EAN on action.com (webshop only), Bulgaria and any country Action is not in. This API cannot reserve, add to basket or buy.
- Terms: Scavio does not collect or store Action data: each call fetches the public Action page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Action's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Action product photos, logos or reviewer details; link products by `url` instead.
- Never fabricate prices, deal dates, stores, hours, reviews or ratings. Only return what the API returned, with the currency, the `fetched_at` time and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` Action is not in, a `language` the country does not have, an article number that is not 7 digits, both or neither of `product_code` / `url` (`ean` / `url` on the webshop, `query` / `category` on webshop search, `store` / `store_id` on store, `query` / `lat`+`lng` on stores), a link whose market disagrees with `country` / `language`, more than 60 `product_codes`, a `page` above 200, an unknown `sort`, a `price_range` that is not a band from the facets, reviews on a country other than nl, de, fr or pl, `scope` `all` with `offset` + `limit` above 100, the webshop on a market other than nl-nl, nl-be or fr-be.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Action does not sell article 3225277 on sl-si (or the code does not exist).", "Action sells none of these articles on nl-nl.", "Action has no such category on this market." (the same for a brand or collection), "Action has no store at this address.", "Action has no store with id ZZ99.", "The Action webshop does not sell EAN 8710000000000 on nl-nl.", "The Action webshop has no such category.". Take codes, paths and slugs from a previous answer rather than guessing them. An article with no reviews is a `200` with `total` 0, not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api).
- `502` means Action data was temporarily unavailable ("Action is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Action is busy ("Action is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.74.0
npm install scavio@0.75.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: deals } = await scavio.action.weeklyDeals({ country: "nl" });
const { data: priced } = await scavio.action.products({ product_codes: ["3011901", "3218276"], country: "pl" });
const { data: found } = await scavio.action.search({ query: "kerst" });
const { data: product } = await scavio.action.product({ product_code: "3225277", country: "de" });
const { data: home } = await scavio.action.category({ category: "wonen/woonaccessoires" });
const { data: tree } = await scavio.action.categories();
const { data: maxMore } = await scavio.action.brand({ brand: "max-more" });
const { data: brands } = await scavio.action.brands();
const { data: fresh } = await scavio.action.newArrivals({ country: "fr" });
const { data: blackFriday } = await scavio.action.collection({ collection: "black-friday" });
const { data: typed } = await scavio.action.suggestions({ query: "opberg" });
const { data: stores } = await scavio.action.stores({ query: "Amsterdam" });
const { data: store } = await scavio.action.store({ store: "/nl-nl/winkels/amsterdam-kinkerstraat/" });
const { data: reviews } = await scavio.action.reviews({ product_code: "3224838", country: "nl", scope: "all" });
const { data: online } = await scavio.action.webshopSearch({ query: "stofzuiger" });
const { data: item } = await scavio.action.webshopProduct({ ean: "8718969571098" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.action.search(...)`, `product`, `products`, `category`, `categories`, `brand`, `brands`, `new_arrivals`, `weekly_deals`, `collection`, `suggestions`, `stores`, `store`, `reviews`, `webshop_search` and `webshop_product`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 16 endpoints as tools: `search_action`, `get_action_product`, `get_action_products`, `get_action_weekly_deals`, `get_action_category`, `get_action_categories`, `get_action_brand`, `get_action_brands`, `get_action_new_arrivals`, `get_action_collection`, `get_action_suggestions`, `get_action_stores`, `get_action_store`, `get_action_reviews`, `search_action_webshop` and `get_action_webshop_product`. Action is opt-in: add `action` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.74.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,action"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/action-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [product](https://scavio.dev/docs/action-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [products](https://scavio.dev/docs/action-products?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [weekly deals](https://scavio.dev/docs/action-weekly-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [category](https://scavio.dev/docs/action-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [categories](https://scavio.dev/docs/action-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [brand](https://scavio.dev/docs/action-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [brands](https://scavio.dev/docs/action-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [new arrivals](https://scavio.dev/docs/action-new-arrivals?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [collection](https://scavio.dev/docs/action-collection?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [suggestions](https://scavio.dev/docs/action-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [stores](https://scavio.dev/docs/action-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [store](https://scavio.dev/docs/action-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [reviews](https://scavio.dev/docs/action-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [webshop search](https://scavio.dev/docs/action-webshop-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api), [webshop product](https://scavio.dev/docs/action-webshop-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api). Overview: [Action API](https://scavio.dev/action-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=action-com-api).
