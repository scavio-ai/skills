# Fanatics Merchandise API - Jersey Prices, Sales, Sizes, League Shops

Read Fanatics merchandise data: licensed jerseys, hats, apparel, collectibles and fan gear for every major league and club Fanatics sells. Search by keyword on fanatics.com, on 7 international Fanatics storefronts (UK, Germany, France, Spain, Italy, Japan, and Canada in English or French; titles in the storefront's language, prices in its currency) or on the US league stores (NFL Shop, MLB Shop, NHL Shop, MLS Store); browse a team, a player, a league section, a department, a brand or a collection; or list the Sale, Clearance and Under-25 deals. Each page carries up to 72 products with the current, regular, sale, clearance and with-code price (the price with the site's current public promo code), the ship-by date and delivery estimate, plus facets whose ids drive the next request. Read one product with every size's availability, stock level (low or out, never a unit count), price and delivery window, the active promo code and whether it applies, personalization fields with the team roster, Jersey Assurance and authentic flags and the rating with fit, value and quality. In the US, read review text with four sorts and a star filter. All 5 endpoints return structured JSON and cost 1 credit each.

This is merchandise and product data only. Fanatics also runs a sportsbook: nothing here returns odds, lines, bets or betting data, and none of it touches Fanatics Sportsbook, Collect, Live or FanCash accounts.

Fanatics does not publish a public product, price or inventory API. Its developer docs (api.docs.fan) cover Fanatics ID sign-in and FanCash for partners it provisions, affiliates get product feeds through Impact, and marketplace sellers sync their own orders and stock. None of these is a public endpoint for searching the catalog or reading live prices and size stock. This skill reads public Fanatics pages with one Scavio key.

See also: for sneakers and Foot Locker release dates use the `foot-locker-api` skill; for Dick's Sporting Goods clearance and store unit counts use `dicks-sporting-goods-api`; for resale comps on jerseys and autographed items use `ebay-product-data`; for the cross-retailer price view use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Find a player or team jersey on Fanatics and compare prices, sale prices and the price with today's promo code
- Track a Fanatics jersey sale: poll a product or a listing and record when the price, the with-code price or a size's stock changes
- List Fanatics Sale or Clearance items, or items under 25, for a league, team, department or brand, for example ahead of Black Friday
- Check which sizes of a jersey are available, which are low or out of stock, and when an order would ship and arrive
- Read a jersey's personalization options (name and number rules) and the team roster the site offers
- Pull a team's or a player's whole Fanatics catalog (Lakers hats, Mahomes jerseys) or a brand's ('47, New Era, Nike) for a catalog, price or assortment study
- Compare a club's kit price across Fanatics storefronts (UK, Germany, France, Spain, Italy, Japan, Canada) in local currency
- Read the same product on NFL Shop, MLB Shop, NHL Shop or MLS Store, where titles are written per store
- Read what Fanatics customers say about a jersey's fit, value and quality, including the site's own AI-written review summary

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit, so the free credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Search, product, browse and deals answered in 3 to 35 seconds in the captures (most in 4-17 seconds; one team browse took 24 seconds), and occasionally longer when a call is retried for you (one product call took 81 seconds): allow a client timeout of at least 120 seconds. `/reviews` is slow: usually 20-90 seconds (the capture took 69 seconds), up to about 4 minutes when a call is retried for you. Set a client timeout of at least 300 seconds for it and run reviews calls one at a time.

| Endpoint | Credits | Markets | What it returns |
|---|---|---|---|
| `POST /api/v1/fanatics/search` | 1 | all 8 + league stores | A keyword search page (24, 48 or 72 items, default 72): per item `id`, `title`, `brand`, `url`, `image`, `price`, `regular_price`, `sale_price`, `clearance_price`, `with_code_price`, `code_percent_off`, `percent_off`, `price_label`, `top_seller`, `customizable`, `ready_to_ship`, `ship_by`, `est_delivery`, `urgency[]`, `is_sponsored`. Plus `query`, `corrected_query`, `redirected_to`, `broad_match`, `applied_filters`, `total`, `total_capped`, page, page size, total pages, sort, count, `facets[]`, `data_as_of`, `country`, `language`, `currency`, `site` |
| `POST /api/v1/fanatics/browse` | 1 | all 8 + league stores | One listing by `url` or by ids (`league_id`, `team_id`, `player_id`, `department_id`, `brand_id`, `collection_id`): the same grid plus `browse` naming the league, team, player, department, brand and collection the page shows. Filter by `price_band`, `on_sale`, `gender` or any facet |
| `POST /api/v1/fanatics/deals` | 1 | all 8 + league stores (`under_25`: not jp) | A deal list by `type`: `sale` (default), `clearance` or `under_25`, optionally for one league, team, department or brand: the same grid plus `type` and `label` (`clearance` adds `sale_items_on_page`) |
| `POST /api/v1/fanatics/product` | 1 | all 8 + league stores | One product by `product_id` or `url`: title, brand, league, team, player, gender, categories, breadcrumb, description, details, images, the price block, `on_sale`, the active promo `coupon`, `in_stock`, every size (`item_id`, `available`, `stock_level`, price, with-code price, ship-by, delivery window), every colorway, `personalization` (fields and roster), `customizable`, `flags`, `rating` (with fit, value, quality), `review_count`, `style_id`, `data_as_of` |
| `POST /api/v1/fanatics/reviews` | 1 | us | 1-50 reviews (default 10) with `sort` and a star filter, `stats` (written and star-rating counts, average, distribution, fit / quality / value), the site's AI-written `ai_summary` and the `features` reviewers mention. Reviews are pooled across the style: each review carries its own `product_id` and `product_title` |

## Markets

`search`, `product`, `browse` and `deals` take `country` (default `us`); `reviews` is US only. Titles come in the storefront's language and prices in its currency.

| `country` | Storefront | Currency | Language |
|---|---|---|---|
| `us` | fanatics.com | USD | en |
| `gb` | fanatics.co.uk | GBP | en |
| `de` | fanatics.de | EUR | de |
| `fr` | fanatics.fr | EUR | fr |
| `es` | fanatics.es | EUR | es |
| `it` | fanatics.it | EUR | it |
| `jp` | fanatics.jp | JPY | ja |
| `ca` | fanatics.ca | CAD | `language`: `en` (default) or `fr` |

US league stores, with `site` and `country: "us"` (on search, product, browse and deals):

| `site` | Store |
|---|---|
| `fanatics` | fanatics.com (default) |
| `nflshop` | NFL Shop (nflshop.com) |
| `mlbshop` | MLB Shop (mlbshop.com) |
| `nhlshop` | NHL Shop (shop.nhl.com) |
| `mlsstore` | MLS Store (mlsstore.com) |

The league stores share fanatics.com's product ids: product `5029988` is the same Mahomes Vapor F.U.S.E. Limited jersey on fanatics.com ("Patrick Mahomes Kansas City Chiefs Nike Vapor F.U.S.E. Limited Jersey - Red") and on NFL Shop ("Men's Kansas City Chiefs Patrick Mahomes Nike Red Vapor F.U.S.E. Limited Jersey"); each store writes its own titles and can run its own promo code. On `jp`, `price_band` and the `under_25` deal type are rejected (the site's bands are 25-150 in local currency, which in yen matches nothing). Other Fanatics storefronts (Australia, the Netherlands, Mexico) and the NBA Store are not served.

## Workflow

1. **Find products:** call `/fanatics/search` with `query` (narrow with `gender`, `league_id`, `department_id` or `filters`), `/fanatics/browse` with a team, player, department, brand or collection id or a Fanatics listing `url`, or `/fanatics/deals` with a `type`. Set `country` for a non-US storefront or `site` for a US league store. Each item has an `id`.
2. **Use the ids the facets give you:** every facet value carries `filter` (a code such as `o` league, `t` team, `a` player, `d` department, `br` brand, `ga` gender / age, `ks` kids size, `sz` standard size, `p3` price band) and `value` (an id). Send them back as `filters: {"<filter>": "<value>"}`, or as the named ids on browse (`team_id`, `player_id`, ...). Never guess ids; read them from a previous answer.
3. **Page through:** `page` 1, 2, 3... up to `total_pages`; `page_size` 24, 48 or 72 (default 72). At most 9000 products of one listing can be paged: narrow with filters to reach the rest.
4. **One product in full:** call `/fanatics/product` with the item's `id` as `product_id` and the same `country` / `site`. Read `sizes[]` for availability, stock level and delivery, `coupon` for today's code and `personalization` for name and number options.
5. **Sale watch:** poll `/fanatics/product` (or a deals or browse listing) on a schedule and store `price`, `sale_price`, `clearance_price`, `with_code_price`, the coupon `code` and each size's `available` / `stock_level` per run; compare runs yourself. There is no price history.
6. **Reviews (US):** call `/fanatics/reviews` with the product `id` (`review_count` on the product tells you whether there is anything to read). Check each review's `product_id`: the list covers the whole style.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars). The site corrects spelling: see `corrected_query` |
| `country` | string | `us` | A storefront from the Markets table |
| `language` | string | storefront's | `ca` only: `en` or `fr` |
| `site` | string | `fanatics` | US league store: `fanatics`, `nflshop`, `mlbshop`, `nhlshop`, `mlsstore`. Only with `country: "us"` |
| `gender` | string | none | `men`, `women`, `kids` or `baby` |
| `league_id` | integer or string | none | One league, an id from `facets` (NFL 25, MLB 19, NBA 23, NHL 26, College 5) |
| `department_id` | integer or string | none | One department, an id from `facets` (Jerseys 8011, Hats 8008, T-Shirts 8022) |
| `filters` | object | none | Facet values from a previous answer: `{facets[].values[].filter: facets[].values[].value}`, one value per filter, at most 12 filters. E.g. `{"ga": "2"}` (Women), `{"t": "3433"}` (a team), `{"ks": "126"}` (a kids size), `{"fa": "1"}` (Autographed) |
| `page` | integer | 1 | Results page, 1-375 |
| `page_size` | integer | 72 | 24, 48 or 72 |
| `sort` | string | `top_sellers` | `top_sellers`, `price_low_to_high`, `price_high_to_low` or `newest` |

Price and sale filters (`p3`, `os`, `price_band`, `on_sale`) are rejected on search with a `400` (on a keyword search the site loosens the match): use browse or deals for them, even though the search facets list a "Sale Items" value.

### Browse (`/browse`)

Pass a listing `url` or at least one id. A league alone is a landing page with no product grid: combine `league_id` with another id or a filter.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | A Fanatics listing URL from the site: a team, player, league section, department, brand or collection page (not a product page). Send `url` or ids, not both |
| `league_id` | integer or string | one of | NFL 25, MLB 19, NBA 23, NHL 26, College 5 |
| `team_id` | integer or string | one of | From `facets` (Los Angeles Lakers 3372, Kansas City Chiefs 3433) |
| `player_id` | integer or string | one of | From `facets` `players` (Patrick Mahomes 12072, Aaron Judge 31) |
| `department_id` | integer or string | one of | Hats 8008, Jerseys 8011, or parent-child for a sub-department (`8008-8084`, Adjustable hats) |
| `brand_id` | integer or string | one of | From `facets` `brands` ('47 479, Nike 76, New Era 127) |
| `collection_id` | integer or string | one of | From `facets` (City Edition 11552) |
| `price_band` | string | none | `under_25`, `25_50`, `50_100`, `100_150` or `over_150`, in the storefront's currency. Not on `jp` |
| `on_sale` | boolean | none | Only sale items |
| `gender` | string | none | `men`, `women`, `kids` or `baby` |
| `filters`, `country`, `language`, `site`, `page`, `page_size`, `sort` | | | As on search |

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `sale` | `sale` (the site's Sale listing: coupon-eligible items and clearance markdowns), `clearance` (each sale page's clearance-priced items) or `under_25` (items under 25 in the storefront's currency; not on `jp`) |
| `league_id`, `team_id`, `department_id`, `brand_id` | integer or string | none | Only one league, team, department or brand |
| `country`, `language`, `site`, `page`, `page_size`, `sort` | | | As on search |

Deals take no `filters`, `gender`, `on_sale` or `price_band`: use browse with `on_sale: true` for those.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | A Fanatics product id (digits): a listing item's `id`. The same id works on every league store |
| `url` | string | one of | A product URL on any covered storefront or league store (its storefront is used). A `country` or `site` naming another store is a `400` |
| `country`, `language`, `site` | string | `us`, -, `fanatics` | As on search |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` / `url` | string | one of | A Fanatics product id or a fanatics.com product URL |
| `country` | string | `us` | `us` only |
| `sort` | string | `highest_rated` | `highest_rated` (the site's order), `lowest_rated`, `most_recent` or `most_helpful` |
| `rating` | integer | none | Only reviews with this many stars (1-5) |
| `limit` | integer | 10 | Reviews to return, 1-50. More than 10 takes a few seconds longer per 8 |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/fanatics/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "chiefs jersey"}'
```

Captured `data` (69 of 72 items and most facet values trimmed):

```json
{
  "query": "chiefs jersey",
  "corrected_query": null,
  "redirected_to": null,
  "broad_match": false,
  "applied_filters": [],
  "total": 180,
  "total_capped": false,
  "page": 1,
  "page_size": 72,
  "total_pages": 3,
  "sort": "top_sellers",
  "count": 72,
  "items": [
    {
      "id": "201359763",
      "title": "Kenneth Walker III Kansas City Chiefs Nike Team Game Jersey - Red",
      "brand": "Nike",
      "url": "https://www.fanatics.com/nfl/kansas-city-chiefs/kenneth-walker-iii-kansas-city-chiefs-nike-team-game-jersey-red/o-3550+t-47151436+p-9144908184174+z-9-1423562297",
      "image": "https://fanatics.frgimages.com/kansas-city-chiefs/mens-nike-kenneth-walker-iii-red-kansas-city-chiefs-team-game-jersey_ss5_p-201359763+u-qsphefo7oxvidbtsdulr+v-ckl9jkrdztpops7moxeo.jpg?_hv=2",
      "price": 149.99,
      "regular_price": 149.99,
      "sale_price": null,
      "clearance_price": null,
      "with_code_price": null,
      "code_percent_off": null,
      "percent_off": 0,
      "price_label": "coupon",
      "top_seller": "Men Jerseys",
      "customizable": false,
      "ready_to_ship": false,
      "ship_by": "2026-11-16T23:00:00.000Z",
      "est_delivery": "2026-11-25T17:00:00.000Z",
      "urgency": [
        { "type": "fast_selling", "detail": "low_stock_and_high_selling", "value": 88, "window_minutes": 1440 },
        { "type": "active_carts", "detail": "high_cart_demand_and_low_stock", "value": 5312, "window_minutes": null }
      ],
      "is_sponsored": false
    },
    {
      "id": "5029988",
      "title": "Patrick Mahomes Kansas City Chiefs Nike Vapor F.U.S.E. Limited Jersey - Red",
      "brand": "Nike",
      "url": "https://www.fanatics.com/nfl/kansas-city-chiefs/patrick-mahomes-kansas-city-chiefs-nike-vapor-fuse-limited-jersey-red/o-2405+t-03153670+p-9411791989+z-8-2459728550",
      "image": "https://fanatics.frgimages.com/kansas-city-chiefs/mens-nike-patrick-mahomes-red-kansas-city-chiefs-vapor-fuse-limited-jersey_ss5_p-5029988+u-bvddvdmbrsvakd7p70dm+v-piinxfolbqbijh7knl74.jpg?_hv=2",
      "price": 174.99,
      "regular_price": 174.99,
      "sale_price": null,
      "clearance_price": null,
      "with_code_price": 131.24,
      "code_percent_off": 25,
      "percent_off": 0,
      "price_label": "coupon",
      "top_seller": "Men Jerseys",
      "customizable": false,
      "ready_to_ship": true,
      "ship_by": "2026-11-16T23:00:00.000Z",
      "est_delivery": "2026-11-25T17:00:00.000Z",
      "urgency": [
        { "type": "fast_selling", "detail": "low_stock_and_high_selling", "value": 25, "window_minutes": 1440 },
        { "type": "active_carts", "detail": "high_cart_demand_and_low_stock", "value": 2949, "window_minutes": null }
      ],
      "is_sponsored": false
    },
    {
      "id": "3548335",
      "title": "Patrick Mahomes Kansas City Chiefs Nike Newborn Romper Game Jersey - Red",
      "brand": "Nike",
      "url": "https://www.fanatics.com/nfl/kansas-city-chiefs/patrick-mahomes-kansas-city-chiefs-nike-newborn-romper-game-jersey-red/o-3516+t-70480370+p-70492697642+z-9-3979657777",
      "image": "https://fanatics.frgimages.com/kansas-city-chiefs/newborn-nike-patrick-mahomes-red-kansas-city-chiefs-romper-game-jersey_pi3548000_ff_3548335-56ef974af01112857ac2_full.jpg?_hv=2",
      "price": 43.99,
      "regular_price": 54.99,
      "sale_price": 43.99,
      "clearance_price": 43.99,
      "with_code_price": 41.79,
      "code_percent_off": 24,
      "percent_off": 20,
      "price_label": "clearance",
      "top_seller": null,
      "customizable": false,
      "ready_to_ship": true,
      "ship_by": "2026-11-12T02:00:00.000Z",
      "est_delivery": "2026-11-20T20:00:00.000Z",
      "urgency": [
        { "type": "active_carts", "detail": "high_cart_demand_and_low_stock", "value": 172, "window_minutes": null }
      ],
      "is_sponsored": false
    }
  ],
  "facets": [
    {
      "id": "leagues",
      "label": "Leagues",
      "values": [{ "label": "NFL", "filter": "o", "value": "25", "count": 180 }]
    },
    {
      "id": "featuredDepartmentsBoxes",
      "label": "Featured Departments",
      "values": [
        { "label": "Jerseys", "filter": "d", "value": "8011", "count": 180 },
        { "label": "Sale Items", "filter": "os", "value": "1", "count": 12 }
      ]
    },
    {
      "id": "genderAgeGroups",
      "label": "Gender/Age",
      "values": [
        { "label": "Men", "filter": "ga", "value": "1", "count": 96 },
        { "label": "Women", "filter": "ga", "value": "2", "count": 68 },
        { "label": "Big & Tall", "filter": "es", "value": "2", "count": 2 }
      ]
    }
  ],
  "data_as_of": "2026-11-11T18:33:22.788Z",
  "country": "us",
  "language": "en",
  "currency": "USD",
  "site": "fanatics"
}
```

Read the price fields together. `price` is today's price; `regular_price` the list price; `sale_price` and `clearance_price` are set only when the item is marked down (the newborn romper: 54.99 regular, 43.99 on clearance, `percent_off` 20). `with_code_price` is the price after the site's current public promo code, shown only when it is lower than `price`, with the code's percent for that item in `code_percent_off` (25% on the Vapor F.U.S.E. jersey, 131.24 against 174.99; the clearance romper also has a with-code price, 41.79). `price_label` is the site's tile label (`coupon`, `clearance` or `none`); `coupon` on a tile does not mean the code applies to it: the Kenneth Walker III jersey reads `coupon` with `with_code_price` null. Quote `with_code_price` only when it is set, and name the code from `/product`'s `coupon.code`.

`urgency[]` repeats the site's own badges with the number each shows (`fast_selling` 88 within a 1440-minute window, `active_carts` 5312): quote them as Fanatics' badges, never as stock or sales counts. `top_seller` is the site's best-seller tag, `customizable` means name and number personalization is offered, `ready_to_ship` the site's ready-to-ship tag. `is_sponsored` flags paid placements. Search facets here were `leagues`, `featuredDepartmentsBoxes`, `genderAgeGroups` and `allDepartmentsBoxes`; browse listings add teams, players, brands, sizes and price ranges.

`data_as_of` is when Fanatics built this page: listings can be a few minutes old, so read `/product` before quoting a current price or size. `total` stops at 9000 on large listings: when `total_capped` is true, say "9000+", not 9000.

### Search on a European storefront

```bash
curl -X POST https://api.scavio.dev/api/v1/fanatics/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "camiseta real madrid", "country": "es"}'
```

Captured `data` (71 of 72 items and most facet values trimmed):

```json
{
  "query": "camiseta real madrid",
  "corrected_query": "calista real madrid",
  "redirected_to": null,
  "broad_match": true,
  "applied_filters": [],
  "total": 127,
  "total_capped": false,
  "page": 1,
  "page_size": 72,
  "total_pages": 2,
  "sort": "top_sellers",
  "count": 72,
  "items": [
    {
      "id": "203732652",
      "title": "Camiseta adidas de la 1ª equipación del Real Madrid 2026-27 - Niños",
      "brand": "adidas",
      "url": "https://www.fanatics.es/es/la-liga/real-madrid/camiseta-adidas-de-la-1ª-equipación-del-real-madrid-2026-27-niños/o-43089163+t-47316080+p-79117728088+z-9-2905726616",
      "image": "https://images.footballfanatics.com/real-madrid/real-madrid-adidas-home-shirt-2026-27-kids_ss5_p-203732652+u-cebd8kxszzotqmo4w5xv+v-lcccqbiclh5egrmhduv6.jpg?_hv=2",
      "price": 70,
      "regular_price": 70,
      "sale_price": null,
      "clearance_price": null,
      "with_code_price": 35,
      "code_percent_off": 50,
      "percent_off": 0,
      "price_label": "coupon",
      "top_seller": null,
      "customizable": true,
      "ready_to_ship": false,
      "ship_by": null,
      "est_delivery": null,
      "urgency": [],
      "is_sponsored": false
    }
  ],
  "facets": [
    {
      "id": "leagues",
      "label": "Ligas",
      "values": [{ "label": "LALIGA", "filter": "o", "value": "9827", "count": 127 }]
    },
    {
      "id": "allDepartmentsBoxes",
      "label": "Todas las categorías",
      "values": [
        { "label": "Camisetas", "filter": "d", "value": "8011", "count": 33 },
        { "label": "Camisetas", "filter": "d", "value": "8022", "count": 22 }
      ]
    },
    {
      "id": "genderAgeGroups",
      "label": "Género/Edad",
      "values": [
        { "label": "Hombre", "filter": "ga", "value": "1", "count": 68 },
        { "label": "Niño", "filter": "ga", "value": "3", "count": 35 }
      ]
    }
  ],
  "data_as_of": "2026-11-11T18:36:07.577Z",
  "country": "es",
  "language": "es",
  "currency": "EUR",
  "site": "fanatics"
}
```

Titles and facet labels come in the storefront's language, prices in its currency. Department ids are the same across storefronts (8011 is Jerseys, 8022 T-Shirts) even where both labels read "Camisetas": filter by `value`, never by label. `corrected_query` is the site's own spelling correction and can look odd ("camiseta" became "calista" here while the results stayed on Real Madrid shirts); `broad_match: true` means the site widened the match to part of the keywords. Report both with the results.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/fanatics/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "3892922"}'
```

Captured `data` (details, 9 of 10 images, 2 of 4 breadcrumb entries and 3 of 5 sizes trimmed; description cut):

```json
{
  "id": "3892922",
  "title": "Patrick Mahomes Kansas City Chiefs Nike Women's Game Jersey - Red",
  "brand": "Nike",
  "league": ["NFL"],
  "team": ["Kansas City Chiefs"],
  "player": [{ "id": 12072, "name": "Patrick Mahomes" }],
  "gender": ["Women"],
  "categories": ["Jerseys", "Nike Game", "Replica Jersey"],
  "breadcrumb": [
    { "name": "NFL", "type": "o", "url": "https://www.fanatics.com/nfl/o-3572+z-953036859-1253393850" },
    { "name": "Kansas City Chiefs", "type": "t", "url": "https://www.fanatics.com/nfl/kansas-city-chiefs/o-2472+t-70269247+z-91896-1122630966" }
  ],
  "url": "https://www.fanatics.com/nfl/kansas-city-chiefs/patrick-mahomes-kansas-city-chiefs-nike-womens-game-jersey-red/o-3527+t-81604725+p-70193279240+z-9-2557663724",
  "description": "Rep the on-field look of your favorite Kansas City Chiefs player with this Patrick Mahomes Game jersey from Nike...",
  "images": ["https://fanatics.frgimages.com/kansas-city-chiefs/womens-nike-patrick-mahomes-red-kansas-city-chiefs-game-jersey_pi3892000_ff_3892922-e9be3d53c836e3e4e2b0_full.jpg?_hv=2"],
  "price": 149.99,
  "regular_price": 149.99,
  "sale_price": null,
  "clearance_price": null,
  "with_code_price": null,
  "code_percent_off": null,
  "percent_off": 0,
  "price_label": "coupon",
  "on_sale": false,
  "coupon": {
    "code": "HONOR",
    "percent_off": 60,
    "percent_off_min": 5,
    "tiered": true,
    "ends_on": "2026-11-12",
    "applies_to_product": false
  },
  "in_stock": true,
  "sizes": [
    {
      "item_id": "13926228",
      "size": "S",
      "available": true,
      "stock_level": null,
      "price": 149.99,
      "with_code_price": null,
      "ship_by": "2026-11-16T23:00:00.000Z",
      "est_delivery_from": "2026-11-19T17:00:00.000Z",
      "est_delivery_to": "2026-11-25T17:00:00.000Z",
      "promise_ship_days": 2,
      "customization_handling_days": 0
    },
    {
      "item_id": "13926229",
      "size": "XL",
      "available": true,
      "stock_level": null,
      "price": 149.99,
      "with_code_price": null,
      "ship_by": "2026-11-12T02:00:00.000Z",
      "est_delivery_from": "2026-11-16T20:00:00.000Z",
      "est_delivery_to": "2026-11-20T20:00:00.000Z",
      "promise_ship_days": 0,
      "customization_handling_days": 0
    }
  ],
  "colors": [],
  "personalization": null,
  "customizable": false,
  "flags": {
    "jersey_assurance": true,
    "non_returnable": false,
    "exclusive": false,
    "authentic": false
  },
  "rating": {
    "average": 4,
    "count": 2540,
    "distribution": { "1": 358, "2": 140, "3": 219, "4": 230, "5": 1593 },
    "fit": {
      "average": 2.4,
      "count": 2026,
      "distribution": [
        { "rating": 1, "label": "Too Small", "count": 468 },
        { "rating": 2, "label": "Somewhat Small", "count": 340 },
        { "rating": 3, "label": "True to Size", "count": 1117 },
        { "rating": 4, "label": "Somewhat Large", "count": 64 },
        { "rating": 5, "label": "Too Large", "count": 37 }
      ]
    },
    "value": { "average": 4, "count": 2241 },
    "quality": { "average": 4.3, "count": 2309 }
  },
  "review_count": 993,
  "style_id": 118463,
  "data_as_of": "2026-11-11T18:32:38.184Z",
  "country": "us",
  "language": "en",
  "currency": "USD",
  "site": "fanatics"
}
```

`coupon` is the site's current public promo code: `HONOR` here, tiered from 5% to 60% depending on the item, ending 2026-11-12, and `applies_to_product: false` on this jersey, so `with_code_price` is null and 149.99 is the price to quote. When the code applies, `with_code_price` is set on the product and on each size (the Borussia Dortmund home shirt on `de` read 100 EUR, 60 EUR with code `GOAL` at 40%). Codes change often and differ per storefront and league store (`GOAL` on the UK and EU storefronts, `DIAMOND` on MLB Shop on 2026-11-11): always read the code from the response.

`stock_level` is a level, never a count: `low`, `out`, or null when the size is available with no low-stock note (the `de` shirt had S, XL, 2XL and 3XL `low`; a `fr` jersey had 3XL `available: false`, `stock_level: "out"`). Never say how many are left. `ship_by` and `est_delivery_from` / `est_delivery_to` are the site's own estimates per size and can differ between sizes (XL here ships sooner than S). `rating.count` (2540) counts every star rating; `review_count` (993) the written reviews. Fit is a 1-5 scale with labels: 3 is "True to Size", and an average of 2.4 means reviewers find it runs small, which matches the product's own sizing tip. `jersey_assurance` is the site's Jersey Assurance badge; `authentic` flags Fanatics Authentic or authenticated items (autographed memorabilia); `non_returnable` and `exclusive` are the site's flags.

When personalization is offered, `customizable` is true and `personalization` lists `fields[]` (`key`, `label`, `max_length`, `pattern`, `required`; for example a `number` of up to 2 digits and a `name` of up to 8 letters on an NFL custom jersey) and the team `roster[]` (`name`, `number`, `display_name`), with `price_includes_personalization: true`: the price on the page already includes it, so never add a personalization fee on top.

### Browse a team's hats

```bash
curl -X POST https://api.scavio.dev/api/v1/fanatics/browse \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"league_id": 23, "team_id": 3372, "department_id": 8008}'
```

The captured answer opens with (then `items[]` as on search, and `facets[]`):

```json
{
  "browse": {
    "league": { "id": "23", "name": "NBA" },
    "team": { "id": "3372", "name": "Los Angeles Lakers" },
    "player": null,
    "department": { "id": "8008", "name": "Hats" },
    "brand": null,
    "collection": null,
    "applied_filters": []
  },
  "total": 250,
  "total_capped": false,
  "page": 1,
  "page_size": 72,
  "total_pages": 4,
  "sort": "top_sellers",
  "count": 72,
  "data_as_of": "2026-11-11T18:32:48.890Z",
  "country": "us",
  "language": "en",
  "currency": "USD",
  "site": "fanatics"
}
```

Its facets were `standard_sizes` (`sz`), `kids_sizes` (`ks`), `genderAgeGroups` (`ga`), `departments` (sub-departments such as `{"label": "Adjustable", "filter": "d", "value": "8008-8084"}`), `players` (`{"label": "Magic Johnson", "filter": "a", "value": "5650"}`), `brands` (`{"label": "'47", "filter": "br", "value": "479"}`) and `priceRanges` (`{"label": "Less than $25", "filter": "p3", "value": "6"}`). Pass any of them back: `"department_id": "8008-8084"` for adjustable hats, `"brand_id": 479` for '47, `"filters": {"ks": "69"}` for one kids size. Facet labels can read in dollars on EUR and CAD listings ("Less than $25"); the band itself follows the storefront's currency.

### Deals

```bash
curl -X POST https://api.scavio.dev/api/v1/fanatics/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "sale"}'
```

The captured answer opens with (then `items[]` and `facets[]` as on search):

```json
{
  "type": "sale",
  "label": "Sale Items",
  "total": 9000,
  "total_capped": true,
  "page": 1,
  "page_size": 72,
  "total_pages": 125,
  "sort": "top_sellers",
  "count": 70,
  "data_as_of": "2026-11-11T18:33:57.709Z",
  "country": "us",
  "language": "en",
  "currency": "USD",
  "site": "fanatics"
}
```

The US Sale listing is larger than 9000 items (`total_capped: true`: report "9000+"); its first item was a 59.99 UFC hoodie at 35.99 with the code (40%). Sale holds both coupon-eligible items and clearance markdowns. `type: "clearance"` keeps only each sale page's clearance-priced items: `count` is how many of this page's `sale_items_on_page` were clearance (66 of 72 in a capture), and `total` still counts the whole sale listing, so page through and count yourself. Narrow with `team_id`, `league_id`, `department_id` or `brand_id`; for filters by size or price use `/browse` with `on_sale: true`. Black Friday 2026 is November 27; Fanatics had not published its 2026 Black Friday sale dates when this was written, so poll deals daily through the season and store what you see.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/fanatics/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  --max-time 300 \
  -d '{"product_id": "3892922"}'
```

Captured `data` (8 of 10 reviews and 7 of 10 features trimmed; the call took 69 seconds):

```json
{
  "product_id": "3892922",
  "product_title": "Patrick Mahomes Kansas City Chiefs Nike Women's Game Jersey - Red",
  "stats": {
    "review_count": 993,
    "rating_count": 2540,
    "average": 4,
    "distribution": { "1": 358, "2": 140, "3": 219, "4": 230, "5": 1593 },
    "fit": {
      "average": 2.4,
      "count": 2026,
      "distribution": [
        { "rating": 1, "label": "Too Small", "count": 468 },
        { "rating": 2, "label": "Somewhat Small", "count": 340 },
        { "rating": 3, "label": "True to Size", "count": 1117 },
        { "rating": 4, "label": "Somewhat Large", "count": 64 },
        { "rating": 5, "label": "Too Large", "count": 37 }
      ]
    },
    "quality": { "average": 4.3, "count": 2309 },
    "value": { "average": 4, "count": 2241 },
    "style_review_count": 993
  },
  "ai_summary": "Customers overwhelmingly praise the jersey's beautiful design, vibrant colors, and striking appearance, with many reporting compliments when wearing it. Reviewers consistently describe the material as well-made and durable with precise stitching that feels premium. However, a notable concern emerges around sizing, as many customers report the jerseys run substantially smaller than expected, with some noting they fit like a size smaller despite ordering their usual size. Despite this sizing inconsistency, most customers remain satisfied with the overall quality and aesthetic appeal.",
  "ai_summary_at": "2026-08-05T10:27:34.000Z",
  "features": [
    { "feature": "satisfaction", "mentions": 109 },
    { "feature": "quality", "mentions": 80 },
    { "feature": "small", "mentions": 27 }
  ],
  "style_rollup": true,
  "sort": "highest_rated",
  "rating_filter": null,
  "matching_reviews": 993,
  "count": 10,
  "reviews": [
    {
      "id": "418420186",
      "product_id": "201359651",
      "product_title": "Drake Maye New England Patriots Nike Women's Player Game Jersey - Navy",
      "rating": 5,
      "fit": 3,
      "quality": 5,
      "value": 5,
      "recommended": true,
      "title": null,
      "text": "I purchased this game jersey to replace the Julian Edelman jersey I have had for years. The quality is still excellent and it fit perfectly. I usually wear size L in a t-shirt, but purchased and XL and it is perfect. Will allow me to put another long sleeve shirt under it and still wear it comfortably.",
      "author": "Donna C.",
      "submitted_at": "2026-11-02T14:52:43.000Z",
      "updated_at": "2026-11-06T05:45:46.446Z",
      "incentivized": true,
      "helpful_votes": 0,
      "unhelpful_votes": 0,
      "features": [],
      "photos": []
    },
    {
      "id": "417530288",
      "product_id": "202120731",
      "product_title": "Zay Flowers Baltimore Ravens Nike Women's Team Game Jersey - Purple",
      "rating": 5,
      "fit": 3,
      "quality": 5,
      "value": 5,
      "recommended": true,
      "title": "Amazing Team Gear!!",
      "text": "I normally wear a medium, but I purchased a women’s large to wear a shirt underneath. And fits great without being tight!",
      "author": "Represent!",
      "submitted_at": "2026-10-31T00:26:48.000Z",
      "updated_at": "2026-10-31T00:46:30.622Z",
      "incentivized": false,
      "helpful_votes": 0,
      "unhelpful_votes": 0,
      "features": [],
      "photos": []
    }
  ]
}
```

Fanatics pools reviews across a style (`style_rollup: true`): the list for the Mahomes women's Game jersey held 10 reviews of 10 different women's NFL jerseys (Drake Maye, Zay Flowers, Bo Nix...), only one of them about product 3892922. Always group or filter by each review's `product_id` / `product_title` before quoting a review as being about a specific jersey; the reviews speak to the cut and fit of the style. `matching_reviews` counts the style list after your `rating` filter. `ai_summary` is the site's own AI-written summary (dated by `ai_summary_at`): label it as Fanatics' AI summary, never as your own reading of the reviews. Per-review `fit` uses the same 1-5 scale (3 = True to Size). Report `incentivized` with any summary.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def fanatics(endpoint, body, timeout=120):
    r = requests.post(f"{BASE}/api/v1/fanatics/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()["data"]

# 1. Chiefs jerseys, cheapest first, with the with-code price where it applies (1 credit)
res = fanatics("search", {"query": "chiefs jersey", "sort": "price_low_to_high"})
total = f"{res['total']}+" if res["total_capped"] else res["total"]
print(total, "results, page built at", res["data_as_of"])
for it in res["items"][:5]:
    print(it["id"], it["title"], it["price"], "with code:", it["with_code_price"])

# 2. Sizes, stock level and today's code on one jersey (1 credit)
item = fanatics("product", {"product_id": "3892922"})
code = item["coupon"] or {}
print("code", code.get("code"), "applies" if code.get("applies_to_product") else "does not apply")
for s in item["sizes"]:
    print(s["size"], "available" if s["available"] else "not available", s["stock_level"] or "", s["price"], s["est_delivery_to"])

# 3. Lakers adjustable hats on sale (1 credit)
hats = fanatics("browse", {"team_id": 3372, "department_id": "8008-8084", "on_sale": True})
for it in hats["items"][:5]:
    print(it["title"], it["regular_price"], "->", it["price"], it["clearance_price"])

# 4. The same product on NFL Shop (1 credit)
nfl = fanatics("product", {"product_id": "5029988", "site": "nflshop"})
print(nfl["title"], nfl["price"], (nfl["coupon"] or {}).get("code"))

# 5. Lowest-rated reviews, grouped by the product each one is about (1 credit, slow)
rv = fanatics("reviews", {"product_id": "3892922", "sort": "lowest_rated", "limit": 20}, timeout=300)
for r in rv["reviews"]:
    print(r["product_id"], r["rating"], "fit", r["fit"], (r["text"] or "")[:80])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. `fetched_at` is when the answer was produced; `data_as_of` is when Fanatics built the page.

- **listing item** (search, browse, deals) - `id`, `title`, `brand`, `url`, `image`, `price`, `regular_price`, `sale_price`, `clearance_price`, `with_code_price`, `code_percent_off`, `percent_off`, `price_label` (`none`, `coupon` or `clearance`), `top_seller`, `customizable`, `ready_to_ship`, `ship_by`, `est_delivery`, `urgency[]` {`type`, `detail`, `value`, `window_minutes`}, `is_sponsored`.
- **grid** (all three listings) - `applied_filters`, `total`, `total_capped`, `page`, `page_size`, `total_pages`, `sort`, `count`, `items[]`, `facets[]` {`id`, `label`, `values[]` {`label`, `filter`, `value`, `count`}}, `data_as_of`, `country`, `language`, `currency`, `site`.
- **search** - `query`, `corrected_query`, `redirected_to`, `broad_match` and the grid.
- **browse** - `browse` {`league`, `team`, `player`, `department`, `brand`, `collection` (each {`id`, `name`} or null), `applied_filters`} and the grid.
- **deals** - `type`, `label`, the grid, and `sale_items_on_page` on `clearance`.
- **product** - `id`, `title`, `brand`, `league[]`, `team[]`, `player[]` {`id`, `name`}, `gender[]`, `categories[]`, `breadcrumb[]` {`name`, `type`, `url`}, `url`, `description`, `details[]`, `images[]`, the price block (`price`, `regular_price`, `sale_price`, `clearance_price`, `with_code_price`, `code_percent_off`, `percent_off`, `price_label`), `on_sale`, `coupon` ({`code`, `percent_off`, `percent_off_min`, `tiered`, `ends_on`, `applies_to_product`} or null), `in_stock`, `sizes[]` {`item_id`, `size`, `available`, `stock_level`, `price`, `with_code_price`, `ship_by`, `est_delivery_from`, `est_delivery_to`, `promise_ship_days`, `customization_handling_days`}, `colors[]` {`id`, `title`, `color`, `hex`, `style[]`, `url`, `image`, `price`, `regular_price`, `stock_level`}, `personalization` ({`fields[]` {`key`, `label`, `max_length`, `pattern`, `required`}, `roster[]` {`name`, `number`, `display_name`}, `price_includes_personalization`} or null), `customizable`, `flags` {`jersey_assurance`, `non_returnable`, `exclusive`, `authentic`}, `rating` ({`average`, `count`, `distribution`, `fit` {`average`, `count`, `distribution[]` {`rating`, `label`, `count`}}, `value`, `quality`} or null), `review_count`, `style_id`, `data_as_of`, `country`, `language`, `currency`, `site`.
- **reviews** - `product_id`, `product_title`, `stats` {`review_count`, `rating_count`, `average`, `distribution`, `fit`, `quality`, `value`, `style_review_count`}, `ai_summary`, `ai_summary_at`, `features[]` {`feature`, `mentions`}, `style_rollup`, `sort`, `rating_filter`, `matching_reviews`, `count`, `reviews[]` {`id`, `product_id`, `product_title`, `rating`, `fit`, `quality`, `value`, `recommended`, `title`, `text`, `author`, `submitted_at`, `updated_at`, `incentivized`, `helpful_votes`, `unhelpful_votes`, `features[]` {`feature`, `sentiment`}, `photos[]` {`url`, `thumbnail_url`, `width`, `height`}}.

## Guardrails

- Merchandise only. Never present this data as odds, lines, betting markets or sportsbook data, and never route a betting question here.
- Monitoring only: this API does not add to cart, check out, apply codes or hold stock. Fanatics' terms forbid ordering "with the intent to resell", so never help build resale or checkout automation.
- Prices: `with_code_price` is the price after the site's current public promo code, and only when it is set; name the code (`coupon.code`) and its end date when you quote it. `price_label: "coupon"` alone does not mean a code applies. Clearance and sale prices are the site's markdowns. Quote prices in the storefront's `currency`; convert before comparing storefronts and say each price is that site's own.
- Stock is a level, never a count: `available` yes / no and `stock_level` `low` / `out` / null. Never estimate how many are left, and never read `urgency` badge numbers as stock or sales.
- Personalization: the product price already includes it (`price_includes_personalization: true`); never add a fee on top. Use the `pattern` and `max_length` from `fields[]` when checking a name or number.
- Freshness: `data_as_of` says when Fanatics built the page; listings can be a few minutes old. Read `/product` before quoting a current price or size, and give the time with any price or stock you report. Fanatics may change price and availability without notice.
- `total` stops at 9000: when `total_capped` is true, say "9000+". Only the first 9000 products of a listing can be paged.
- Reviews are pooled across a style: check each review's `product_id` before attributing it to a product, and label `ai_summary` as Fanatics' AI-written summary. Quote review text verbatim with its rating and date and report `incentivized`.
- There is no price history: poll and store results yourself.
- Not covered: search suggestions, store locator or store stock (Fanatics has no public one), Q&A, unit counts, member or FanCash pricing, FanCash earn, price history, checkout, resale tooling, Fanatics Sportsbook, Collect and Live, and the Australian, Dutch and Mexican storefronts and the NBA Store.
- Fanatics' terms of use list "Using any automated system or software to extract data from the Properties for commercial purposes (including 'screen scraping')" among unauthorized uses. That is Fanatics' policy, not legal advice; the user is responsible for how they use the data.
- Never fabricate prices, codes, sizes, stock levels, ratings or reviews. Only return what the API returned, with the product `url` or `id`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: no `query`; a `country` the endpoint does not serve (`de` on `/reviews`); `language` on any storefront but `ca`, or other than `en` / `fr` there; a `site` with a `country` other than `us`; `price_band`, `on_sale` or a price / sale filter (`p3`, `os`) on search; `price_band` or `under_25` on `jp`; a league alone on browse (add a team, department, brand, player, collection or filter); `url` and ids together on browse, or a product URL on browse; filters, gender, on_sale or price_band on deals; a filter code not taken from `facets`, more than 12 filters or more than one value per filter; a `page` outside 1-375, `page_size` other than 24, 48 or 72, an unknown `sort` or deal `type`; a `product_id` that is not digits; a product `url` on another storefront or store than `country` / `site`; a review `limit` outside 1-50 or `rating` outside 1-5.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product or listing on that storefront. Not-founds are charged 1 credit: take ids and URLs from a previous answer rather than guessing them. A keyword with no results is a normal `200` with `total: 0`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api).
- `502` means Fanatics was temporarily unavailable or returned an unusable answer. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means too many Fanatics calls are running at once: wait the `Retry-After` seconds (5 for most endpoints, 60 when reviews are busy) and send it again. Not charged.

## SDKs

```bash
pip install scavio==0.49.0
npm install scavio@0.50.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.fanatics.search({ query: "chiefs jersey", sort: "price_low_to_high" });
const { data: es } = await scavio.fanatics.search({ query: "camiseta real madrid", country: "es" });
const { data: hats } = await scavio.fanatics.browse({ league_id: 23, team_id: 3372, department_id: 8008 });
const { data: sale } = await scavio.fanatics.deals({ type: "clearance", league_id: 25 });
const { data: item } = await scavio.fanatics.product({ product_id: "3892922" });
const { data: nfl } = await scavio.fanatics.product({ product_id: "5029988", site: "nflshop" });
// Slow (20-90 s, up to ~4 min): the SDK allows a longer timeout for reviews
const { data: reviews } = await scavio.fanatics.reviews({ product_id: "3892922", sort: "most_recent" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.fanatics.search(...)`, `client.fanatics.product(...)`, `client.fanatics.browse(...)`, `client.fanatics.deals(...)` and `client.fanatics.reviews(...)`.

## MCP

The Scavio MCP server exposes all five endpoints as tools: `search_fanatics`, `get_fanatics_product`, `browse_fanatics`, `get_fanatics_deals` and `get_fanatics_reviews`. Fanatics is opt-in: add `fanatics` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.47.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,fanatics"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/fanatics-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api), [product](https://scavio.dev/docs/fanatics-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api), [browse](https://scavio.dev/docs/fanatics-browse?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api), [deals](https://scavio.dev/docs/fanatics-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api), [reviews](https://scavio.dev/docs/fanatics-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api). Overview: [Fanatics API](https://scavio.dev/fanatics-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api).
