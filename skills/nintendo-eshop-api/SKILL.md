---
name: nintendo-eshop-api
description: "Nintendo eShop API for Nintendo eShop regional prices: one game's regular price, sale price, discount and the eShop's own sale start and end dates in each eShop country, in that country's currency (never converted), for 1 to 50 item ids per call; catalog search by keyword (Europe sorted by relevance, newest, price, title or discount and filtered by platform, on sale, price range, genre, players, publisher, demo and type; Japan by relevance, newest or price with platform, on sale, publisher and type; the Americas by relevance or newest); one game in full with publisher, developer, release date, genres, players, languages, file size, age rating (ESRB, PEGI, USK, CERO, CLASSIND), editions, demo and Nintendo Switch Online needs; games on sale now (every discounted game in Europe and Japan; Nintendo's featured sale pages in the Americas); new and upcoming releases; a game's DLC, bundles and upgrade packs with prices. Nintendo Switch and Nintendo Switch 2. 46 countries: the US, Canada (English or French), Mexico, Brazil, Argentina, Chile, Colombia and Peru; the UK, Ireland, Germany, Austria, Switzerland (German, French or Italian), France, Belgium (French or Dutch), the Netherlands, Luxembourg, Italy, Spain, Portugal, Australia, New Zealand and South Africa; 18 more European countries on the English catalog with their own prices (PLN, CZK, SEK, NOK, DKK, EUR); Japan; and prices only in Korea, Hong Kong, Taiwan and Israel. Item ids are per eShop region (Americas, Europe, Japan, Korea, Hong Kong and Taiwan). 6 endpoints, 1 credit each. No user reviews (Nintendo has none), no best-seller charts and no price history: poll the prices endpoint. Nintendo has no public eShop catalog or price API."
version: 1.0.0
tags: nintendo, nintendo-eshop, nintendo-eshop-api, nintendo-eshop-prices, eshop-prices, eshop-prices-by-country, nintendo-eshop-sale, eshop-sale-end-date, nintendo-switch, nintendo-switch-2, switch-game-prices, switch-2-game-prices, nintendo-dlc, nintendo-releases, nintendo-new-releases, nintendo-upcoming-games, nintendo-black-friday, eshop-price-tracker, game-prices, game-deals, video-games, digital-games, price-comparison, price-monitoring, price-tracker, multi-country, regional-pricing, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/docs/nintendo-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api
---

# Nintendo eShop API - Game Prices by Country, Sales, DLC, Releases

Read Nintendo eShop data for Nintendo Switch and Nintendo Switch 2: the price of up to 50 games in any eShop country, catalog search, one product in full, the games on sale now, new and upcoming releases, and a game's DLC, bundles and upgrade packs. All 6 endpoints return structured JSON and cost 1 credit per call.

**The job this skill is for: Nintendo eShop regional prices.** One game's regular price, sale price and sale end date in each eShop country, in that country's currency. `/prices` takes 1 to 50 item ids (`nsuid`) and one `country`, and answers `price`, `regular_price`, `sale_price`, `discount_percent`, `sale_start`, `sale_end`, `currency` and `sales_status` per id. One call per country.

**Item ids are per eShop region, not per game.** The same game has a different `nsuid` in each region, and an id from one region is `not_found` in another:

| Region (`region` in every answer) | Countries | How to get the id |
|---|---|---|
| `americas` | `us` `ca` `mx` `br` `ar` `cl` `co` `pe` | `/product` with the `slug` from an Americas `/search` (search tiles carry `slug`, not `nsuid`) |
| `europe` | the European countries below, plus `au` `nz` `za`, and `il` (prices only) | `items[].nsuid` from `/search` on `gb` (or any European market) |
| `japan` | `jp` | `items[].nsuid` from `/search` on `jp` with a Japanese query |
| Korea | `kr` (prices only) | No searchable catalog: use an id the user already has |
| Hong Kong and Taiwan | `hk`, `tw` (prices only) | No searchable catalog; Taiwan uses the Hong Kong ids |

So "this game in every country" is: look the game up once per region, then call `/prices` for every country of that region with that region's id. There is no cross-region title mapping: match titles yourself and say so.

Captured on 2026-11-15, regular prices (none on sale at capture time):

| Game | `country` | `nsuid` | `price` | `currency` |
|---|---|---|---|---|
| Mario Kart World | `us` | 70010000095431 | 79.99 | USD |
| Mario Kart World | `pl` | 70010000096802 | 329.8 | PLN |
| Mario Kart World | `se` | 70010000096802 | 879 | SEK |
| The Legend of Zelda: Tears of the Kingdom | `us` | 70010000063714 | 69.99 | USD |
| The Legend of Zelda: Tears of the Kingdom | `kr` | 70010000063716 | 74800 | KRW |
| Pokemon Legends: Z-A | `us` | 70010000094234 | 59.99 | USD |
| Pokemon Legends: Z-A | `hk` | 70010000094237 | 359 | HKD |

Prices are never converted. To compare countries, convert explicitly and state the rate and its date.

**Sales and price history.** `sale_start` and `sale_end` are the eShop's own sale window, from Nintendo. Nintendo shows no price history and no historical low, so neither is returned: to build one, call `/prices` on a schedule and store each reading with its time, country and currency. Nintendo announced a US eShop sale on select digital games from November 19 through December 2, 2026 (Black Friday is November 27, 2026).

Nintendo has no public eShop catalog or price API. The Nintendo Developer Portal is for making and publishing games on Nintendo platforms; it does not offer store prices or catalog data to third parties.

See also: for physical copies and consoles at US retailers use `amazon-product-data`, `walmart-product-data`, `target-product-data` or `best-buy-product-data`; for the cross-merchant view of one product use `google-shopping-api`; for mobile apps use `apple-app-store-api` and `google-play-store-api`.

## When to trigger

Use this skill when the user asks to:
- Compare a Nintendo Switch or Switch 2 game's eShop price across countries, each in its own currency
- Check whether a game is on sale on the eShop, its sale price, discount and when the sale ends
- Track eShop prices or sales over time (Black Friday, a publisher sale) by polling and storing prices
- Search the Nintendo eShop catalog by keyword in a country, sorted or filtered by platform, sale, genre, players, publisher, demo or price
- Read one eShop game in full: publisher, developer, release date, genres, players, languages, file size, age rating, editions, demo, Nintendo Switch Online needs
- List the games on sale now in a country, or one Nintendo sale page in the Americas
- List new or upcoming Nintendo Switch and Switch 2 releases in a country
- List a game's DLC, bundles and upgrade packs with their prices

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits: 50 calls, since every endpoint here costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures `/prices` took 0.5 to 8 seconds, European and Japanese calls 1 to 13 seconds, and Americas search and releases 7 to 19 seconds. Set a client timeout of at least 180 seconds and do not fire many calls at once (a busy moment answers `503` with `Retry-After`).

| Endpoint | Markets | Credits | What it returns |
|---|---|---|---|
| `POST /api/v1/nintendo/search` | catalog markets (42) | 1 | Catalog items for a keyword with prices; Europe and Japan with total, sorts and filters |
| `POST /api/v1/nintendo/product` | catalog markets (42) | 1 | One game or store item by `nsuid`, `url` or (Americas) `slug` |
| `POST /api/v1/nintendo/prices` | all 46 | 1 | The price of 1 to 50 item ids in one country, with the sale window |
| `POST /api/v1/nintendo/deals` | catalog markets (42) | 1 | Games on sale now (Americas: Nintendo's featured sale pages) |
| `POST /api/v1/nintendo/releases` | catalog markets (42) | 1 | New releases or upcoming games |
| `POST /api/v1/nintendo/dlc` | catalog markets (42) | 1 | A game's DLC, bundles and upgrade packs with prices |

## Markets

Every endpoint takes `country` (lowercase, default `us`) and `language` (default the market's first). Titles and descriptions come back in that language and prices in the country's currency, never converted; every `data` echoes `country`, `language`, `currency` and `region`.

| `country` | Languages | Currency | Catalog |
|---|---|---|---|
| `us` | `en` | USD | Americas |
| `ca` | `en`, `fr` | CAD | Americas |
| `mx` | `es` | MXN | Americas |
| `br` | `pt` | BRL | Americas |
| `ar`, `cl`, `co`, `pe` | `es` | ARS, CLP, COP, PEN | Americas |
| `gb` | `en` | GBP | Europe, own catalog |
| `ie` | `en` | EUR | Europe, own catalog |
| `de`, `at` | `de` | EUR | Europe, own catalog |
| `ch` | `de`, `fr`, `it` | CHF | Europe, own catalog |
| `fr`, `lu` | `fr` | EUR | Europe, own catalog |
| `be` | `fr`, `nl` | EUR | Europe, own catalog |
| `nl` | `nl` | EUR | Europe, own catalog |
| `it` | `it` | EUR | Europe, own catalog |
| `es` | `es` | EUR | Europe, own catalog |
| `pt` | `pt` | EUR | Europe, own catalog |
| `au`, `nz`, `za` | `en` | AUD, NZD, ZAR | Europe, own catalog |
| `pl`, `cz`, `se`, `no`, `dk` | `en` | PLN, CZK, SEK, NOK, DKK | Europe, English catalog with that country's prices |
| `fi`, `sk`, `hu`, `ro`, `bg`, `gr`, `hr`, `si`, `ee`, `lv`, `lt`, `mt`, `cy` | `en` | EUR | Europe, English catalog with that country's prices |
| `jp` | `ja` | JPY | Japan |
| `kr` | `ko` | KRW | Prices only |
| `hk`, `tw` | `zh` | HKD, TWD | Prices only |
| `il` | `en` | EUR | Prices only (European item ids) |

- Search, product, deals, releases and DLC: the 42 catalog markets. Prices: all 46 (the 42 plus `kr`, `hk`, `tw`, `il`). A prices-only market on another endpoint answers `400`.
- The 18 European countries without a Nintendo site of their own (`pl` through `cy` above) read the English European catalog with that country's own eShop prices; `notes` says so.
- `ph` (Nintendo has not published Philippines item ids yet), `ru` (no eShop), `uk` (use `gb`) and countries with no eShop data answer `400` before anything is charged.

## Workflow

1. **One game, every country:** for each region, find the game's id. Americas: `/search` on `us`, then `/product` with `items[].slug` for `product.nsuid`. Europe: `/search` on `gb` and read `items[].nsuid`. Japan: `/search` on `jp` with the Japanese title. Then `/prices` with that id (up to 50 ids per call) for each country of the region. Keep the ids: they do not change, so later runs need only `/prices`.
2. **Is it on sale, and until when:** `/prices` or `/product`; on sale when `sale_price` is set, with `discount_percent`, `sale_start` and `sale_end` (UTC).
3. **Price tracking:** poll `/prices` on a schedule. Store `nsuid`, `country`, `currency`, the time, `price`, `regular_price`, `sale_price`, `sale_end` per run. There is no price history endpoint.
4. **Browse the catalog:** `/search` with `query`. Europe: `sort`, `platform`, `on_sale`, `genre`, `players`, `publisher`, `has_demo`, `type`, and `price_min` / `price_max` on `gb`, `de`, `at`, `fr`, `be`, `lu`, `nl`, `it`, `es` and `pt`. Japan: `sort`, `platform`, `on_sale`, `publisher`, `type`. Americas: `query`, `page` and `sort` (`relevance` or `newest`) only.
5. **On sale now:** `/deals`. Europe and Japan list every discounted game in the catalog; the Americas list Nintendo's featured sale pages (`sales[]`; pass one `sales[].sale` as `sale`), not every discounted game: check other ids with `/prices`.
6. **Release calendar:** `/releases` with `type` `new` (released, newest first) or `upcoming` (soonest first), optionally `platform`.
7. **DLC:** `/dlc` with the game's `nsuid`, `url` or (Americas) `slug`.

## Parameters

### Shared

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `us` | See Markets |
| `language` | string | the market's first | One of the market's languages |
| `page` | integer | 1 | 1-based (Americas search up to 50) |
| `page_size` | integer | 24 | 1 to 50. Fixed at 40 on Americas search; not sent on Americas releases |
| `platform` | string | both | `switch` or `switch_2` (search: Europe and `jp`; deals and releases: all) |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords, 1-200 chars (Japanese titles on `jp`) |
| `sort` | string | `relevance` | Americas: `relevance`, `newest`. Europe: `relevance`, `newest`, `price_asc`, `price_desc`, `title`, `discount`. `jp`: `relevance`, `newest`, `price_asc`, `price_desc` |
| `on_sale` | boolean | false | Only discounted games (Europe, `jp`) |
| `price_min` / `price_max` | number | none | Price range, where the catalog is priced in the country's currency: `gb`, `de`, `at`, `fr`, `be`, `lu`, `nl`, `it`, `es`, `pt` (elsewhere `400`) |
| `genre` | string | none | A genre as the catalog names it, in the request language (Europe) |
| `players` | integer | none | At least this many players (Europe) |
| `publisher` | string | none | Exact publisher name (Europe; `jp` in Japanese, `任天堂`) |
| `has_demo` | boolean | false | Only games with a free demo (Europe) |
| `type` | string | `game` | `game`, `dlc`, `all` (Europe); `game`, `dlc`, `bundle`, `all` (`jp`) |

A sort or filter the catalog does not support answers `400`; it is never silently dropped.

### Product (`/product`) and DLC (`/dlc`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `nsuid` | string | one of | 14 digits starting `70` (`70010000095431`). Must be an id of the country's region |
| `url` | string | one of | An Americas store page (`/us/store/products/<slug>/`), a European game page (ending `-<id>.html`) or a nintendo.com/au game page. Without `country` the link's market is used; with `country`, both must be in the same region |
| `slug` | string | one of | Americas only: `items[].slug` from an Americas search (`mario-kart-world-switch-2`) |

Send exactly one. On `jp` send `nsuid`.

### Prices (`/prices`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ids` | array or string | required | 1 to 50 item ids, as an array or comma-separated. More than 50 answers `400` |

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sort` | string | per catalog | Americas: `featured` (Nintendo's order), `discount`, `price_asc`, `newest`, `ending_soon`. Europe: `discount` (default), `price_asc`, `newest`. `jp`: `newest` (default), `price_asc` |
| `sale` | string | none | Americas only: one sale page, by `sales[].sale` (`square-enix`) |

### Releases (`/releases`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `new` | `new` (released, newest first) or `upcoming` (future dates, soonest first) |

On the Americas markets releases is Nintendo's whole new-releases or coming-soon list in one answer: no `page` above 1 and no `page_size`.

## Examples

### Prices (one country, up to 50 ids)

```bash
curl -X POST https://api.scavio.dev/api/v1/nintendo/prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ids": "70010000096802,70010000063715,70010000094235", "country": "pl"}'
```

Captured `data` (Poland, 2026-11-15; 1 of 3 prices shown):

```json
{
  "prices": [
    {
      "nsuid": "70010000096802",
      "sales_status": "onsale",
      "price": 329.8,
      "regular_price": 329.8,
      "sale_price": null,
      "discount_percent": null,
      "sale_start": null,
      "sale_end": null,
      "currency": "PLN",
      "is_free": false
    }
  ],
  "not_found": [],
  "count": 3,
  "country": "pl",
  "language": "en",
  "currency": "PLN",
  "region": "europe",
  "notes": [
    "Item ids (nsuid) are per eShop region: americas (US CA MX BR AR CL CO PE), europe (EU / EFTA, GB, AU, NZ, ZA, IL), japan, kr, and hk-tw; an id from one region is not_found in another.",
    "sale_start / sale_end are the eShop's own sale window; Nintendo publishes no price history (poll this endpoint)."
  ]
}
```

An id that eShop does not sell is listed in `not_found` and left out of `prices`. A free game is `price: 0` with `is_free: true` (captured on `hk`).

### Search (Americas)

```bash
curl -X POST https://api.scavio.dev/api/v1/nintendo/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mario"}'
```

Captured `data` (US, 2026-11-15; 1 of 40 items shown):

```json
{
  "query": "mario",
  "sort": "relevance",
  "sorts_offered": ["relevance", "newest"],
  "country": "us",
  "language": "en",
  "currency": "USD",
  "region": "americas",
  "items": [
    {
      "nsuid": null,
      "slug": "mario-kart-world-switch-2",
      "url": "https://www.nintendo.com/us/store/products/mario-kart-world-switch-2/",
      "title": "Mario Kart™ World",
      "platform": "switch_2",
      "release_date": "2025-06-05",
      "release_date_text": "6/5/25",
      "upcoming": false,
      "publisher": null,
      "price": 79.99,
      "regular_price": 79.99,
      "sale_price": null,
      "discount_percent": null,
      "sale_start": null,
      "sale_end": null,
      "currency": "USD",
      "is_free": false,
      "badges": [],
      "image": "https://assets.nintendo.com/image/fetch/c_scale,w_260/dpr_2.0/q_auto/f_auto/https://atum-img-lp1.cdn.nintendo.net/i/c/e1def375c7254d669bcd65ff10170151_1024",
      "type": "game",
      "category": "Games",
      "age_rating": null
    }
  ],
  "count": 40,
  "total": null,
  "page": 1,
  "page_size": 40,
  "total_pages": null,
  "has_more": true,
  "requested_filters": {},
  "notes": [
    "Americas search lists games, hardware and merchandise together (type per item); tiles carry a slug, not an item id: read product with the slug for the nsuid, then prices / dlc.",
    "Americas search has no exact total: has_more says whether another page follows."
  ]
}
```

### Search (Europe)

```bash
curl -X POST https://api.scavio.dev/api/v1/nintendo/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mario", "country": "gb"}'
```

Captured `data` (UK, 2026-11-15; 1 of 24 items shown):

```json
{
  "query": "mario",
  "sort": "relevance",
  "sorts_offered": ["relevance", "newest", "price_asc", "price_desc", "title", "discount"],
  "country": "gb",
  "language": "en",
  "currency": "GBP",
  "region": "europe",
  "items": [
    {
      "nsuid": "70070000030726",
      "page_id": "2915270",
      "title": "Super Mario Galaxy + Super Mario Galaxy 2",
      "url": "https://www.nintendo.com/en-gb/Games/Nintendo-Switch-games/Super-Mario-Galaxy-Super-Mario-Galaxy-2-2915270.html",
      "platform": "switch",
      "release_date": "2025-10-02",
      "publisher": "Nintendo",
      "price": 58.99,
      "regular_price": 58.99,
      "sale_price": null,
      "discount_percent": null,
      "sale_start": null,
      "sale_end": null,
      "currency": "GBP",
      "is_free": false,
      "sales_status": "onsale",
      "image": "https://www.nintendo.com/eu/media/images/assets/nintendo_switch_games/supermariogalaxyandsupermariogalaxy2/1x1_NSwitch_SuperMarioGalaxy1And2_image500w.jpg",
      "type": "game",
      "age_rating": {"system": "PEGI", "rating": "7", "label": "PEGI 7"}
    }
  ],
  "count": 24,
  "total": 303,
  "page": 1,
  "page_size": 24,
  "total_pages": 13,
  "requested_filters": {"type": "game"},
  "notes": [
    "Prices are the GB eShop's (GBP), not the catalog's own.",
    "2 items are not sold on the GB eShop: kept, with sales_status not_found and price null."
  ]
}
```

On `jp` the same shape comes back in Japanese (`"query": "マリオ"`, `"publisher": "任天堂"`, `"age_rating": {"system": "CERO", "rating": "A", "code": "1"}`, `release_date_text` as `2023.10.20`).

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/nintendo/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"nsuid": "70010000095431"}'
```

Captured `data` (US, 2026-11-15; lists trimmed, `description` cut):

```json
{
  "product": {
    "nsuid": "70010000095431",
    "sku": "7100095431",
    "application_id": "0400c3f00006e000",
    "title": "Mario Kart™ World",
    "url": "https://www.nintendo.com/us/store/products/mario-kart-world-switch-2/",
    "slug": "mario-kart-world-switch-2",
    "platform": "switch_2",
    "platform_label": "Nintendo Switch 2",
    "platforms": ["switch_2"],
    "category": "games",
    "type": "game",
    "release_date": "2025-06-05",
    "release_date_text": null,
    "publisher": "Nintendo",
    "developer": "Nintendo",
    "genres": ["Party"],
    "players": {
      "system": {"min": 1, "max": 4, "label": "4+"},
      "local": {"min": 2, "max": 8, "label": "4+"},
      "online": {"min": 2, "max": 24, "label": "4+"}
    },
    "languages": ["Japanese"],
    "file_size_bytes": 23845666816,
    "age_rating": {"system": "ESRB", "rating": "Everyone", "code": "e", "descriptors": ["Mild Fantasy Violence"]},
    "price": 79.99,
    "regular_price": 79.99,
    "sale_price": null,
    "discount_percent": null,
    "currency": "USD",
    "is_free": false,
    "sale_start": null,
    "sale_end": null,
    "sales_status": "onsale",
    "purchasable": true,
    "preorder": false,
    "has_demo": false,
    "demo_nsuid": null,
    "edition": "Standard Edition",
    "is_upgrade": false,
    "nintendo_switch_online": {"required": false, "features": ["Online Play"]},
    "play_modes": ["TV mode"],
    "availability": ["Available now"],
    "dlc": []
  },
  "country": "us",
  "language": "en",
  "currency": "USD",
  "region": "americas"
}
```

A European product (`"country": "gb"`, `nsuid` `70070000030726`) adds `nsuids`, `page_id`, `players` {`min`, `max`, `system`, `local`, `online`}, `age_rating` {`system`: `PEGI`, `rating`, `label`}, `physical_version`, `digital_version`, `game_series`, `base_game`, `nintendo_switch_online` {`required`, `online_play`, `cloud_saves`, `game_voucher`} and `copyright`. A Japanese product adds `title_reading`, `format` and `dlc_nsuids`.

### Deals

```bash
curl -X POST https://api.scavio.dev/api/v1/nintendo/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (US, 2026-11-15; 1 of 24 items shown, 2 of 5 sale pages):

```json
{
  "sort": "featured",
  "sorts_offered": ["featured", "discount", "price_asc", "newest", "ending_soon"],
  "country": "us",
  "language": "en",
  "currency": "USD",
  "region": "americas",
  "items": [
    {
      "nsuid": "70070000033531",
      "slug": "q-collection-switch",
      "url": "https://www.nintendo.com/us/store/products/q-collection-switch/",
      "title": "Q Collection",
      "platform": "switch",
      "release_date": "2026-05-21",
      "publisher": "Aksys Games",
      "price": 20.99,
      "regular_price": 29.99,
      "sale_price": 20.99,
      "discount_percent": 30,
      "currency": "USD",
      "is_free": false,
      "sale_start": "2026-11-11T17:00:00Z",
      "sale_end": "2026-11-19T07:59:59Z",
      "sales_status": "onsale",
      "amount_off": 9,
      "type": "game",
      "age_rating": {"system": "ESRB", "rating": "Everyone 10+"},
      "sale": {"sale": "aksys-games", "name": "Aksys Games", "headline": "Aksys Games Sale"},
      "on_sale": true
    }
  ],
  "count": 24,
  "total": 103,
  "page": 1,
  "page_size": 24,
  "total_pages": 5,
  "sale": null,
  "heading": "Sales & deals",
  "sales": [
    {"sale": "best-sellers", "name": "Best sellers"},
    {"sale": "square-enix", "name": "Square Enix"}
  ],
  "requested_filters": {},
  "notes": [
    "On the Americas markets this is Nintendo's featured sale selection (the sale pages of nintendo.com), not every discounted game: check any id with the prices endpoint.",
    "sale picks one sale page (sales[].sale); sale_start / sale_end come from the eShop price service."
  ]
}
```

### Releases

```bash
curl -X POST https://api.scavio.dev/api/v1/nintendo/releases \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "gb"}'
```

Captured `data` (UK, 2026-11-15; 1 of 24 items shown):

```json
{
  "type": "new",
  "country": "gb",
  "language": "en",
  "currency": "GBP",
  "region": "europe",
  "items": [
    {
      "nsuid": "70010000135060",
      "page_id": "3188744",
      "title": "Pikmin 4 – Nintendo Switch 2 Edition + Dandori Academy",
      "url": "https://www.nintendo.com/en-gb/Games/Nintendo-Switch-2-Edition/Pikmin-4-Nintendo-Switch-2-Edition-Dandori-Academy-3188744.html",
      "platform": "switch_2",
      "release_date": "2026-11-12",
      "publisher": "Nintendo",
      "price": 58.99,
      "regular_price": 58.99,
      "sale_price": null,
      "discount_percent": null,
      "sale_start": null,
      "sale_end": null,
      "currency": "GBP",
      "is_free": false,
      "sales_status": "onsale",
      "type": "game",
      "age_rating": {"system": "PEGI", "rating": "3", "label": "PEGI 3"}
    }
  ],
  "count": 24,
  "total": 20137,
  "page": 1,
  "page_size": 24,
  "total_pages": 840,
  "requested_filters": {},
  "notes": ["Prices are the GB eShop's (GBP), not the catalog's own."]
}
```

### DLC

```bash
curl -X POST https://api.scavio.dev/api/v1/nintendo/dlc \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "super-smash-bros-ultimate-switch"}'
```

Captured `data` (US, 2026-11-15; 2 of 69 items shown, `image` dropped):

```json
{
  "game": {"nsuid": "70010000012332", "title": "Super Smash Bros.™ Ultimate", "url": "https://www.nintendo.com/us/store/products/super-smash-bros-ultimate-switch/"},
  "dlc": [
    {"nsuid": "70070000009788", "title": "Super Smash Bros.™ Ultimate: Fighters Pass Vol. 2", "url": "https://www.nintendo.com/us/store/products/super-smash-bros-ultimate-fighters-pass-vol-2-70070000009788-switch/", "slug": "super-smash-bros-ultimate-fighters-pass-vol-2-70070000009788-switch", "type": "bundle", "release_date": "2020-01-28", "price": 29.99, "regular_price": 29.99, "sale_price": null, "discount_percent": null, "currency": "USD", "is_free": false, "sale_start": null, "sale_end": null, "sales_status": "onsale"},
    {"nsuid": "70050000018966", "title": "Super Smash Bros.™ Ultimate: Challenger Pack 11", "url": "https://www.nintendo.com/us/store/products/super-smash-bros-ultimate-challenger-pack-11-70050000018966-switch/", "slug": "super-smash-bros-ultimate-challenger-pack-11-70050000018966-switch", "type": "dlc", "release_date": "2021-10-18", "price": 5.99, "regular_price": 5.99, "sale_price": null, "discount_percent": null, "currency": "USD", "is_free": false, "sale_start": null, "sale_end": null, "sales_status": "onsale"}
  ],
  "count": 69,
  "country": "us",
  "language": "en",
  "currency": "USD",
  "region": "americas"
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

def nd(endpoint, body, timeout=180):
    r = requests.post(f"{BASE}/api/v1/nintendo/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    if r.status_code == 404:
        return None  # not in that region's eShop (charged)
    r.raise_for_status()
    return r.json()["data"]

# Item ids per eShop region for one game (Mario Kart World), found once with
# search / product and kept: ids do not change.
IDS = {
    "americas": "70010000095431",  # product on us
    "europe": "70010000096802",    # search on gb
}
COUNTRIES = {"americas": ["us", "ca", "mx", "br"], "europe": ["gb", "de", "pl", "se", "au"]}

captured_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
rows = []
for region, countries in COUNTRIES.items():
    for cc in countries:  # 1 credit per country, up to 50 ids per call
        d = nd("prices", {"ids": [IDS[region]], "country": cc})
        for p in d["prices"]:
            rows.append({"country": cc, "currency": p["currency"], "price": p["price"],
                         "regular_price": p["regular_price"], "sale_end": p["sale_end"]})

for r in rows:
    print(captured_at, r["country"], r["price"], r["currency"], "sale ends " + r["sale_end"] if r["sale_end"] else "")

# Store rows with captured_at and run this on a schedule: that stored series is
# your price history (Nintendo publishes none). Currencies differ: convert
# explicitly, with the rate and its date, before comparing countries.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live; nothing is cached. Every `data` echoes `country`, `language`, `currency` and `region` (`americas`, `europe`, `japan` or `asia`). Prices are numbers in the country's currency, never converted. `notes` appears when there is something to say.

- **Grid item** (search, deals, releases) - `nsuid`, `slug` (Americas), `page_id` (Europe), `url`, `title` (in the request language), `platform` (`switch` / `switch_2`), `release_date`, `release_date_text` (Americas, `jp`), `upcoming` (Americas), `publisher`, `price`, `regular_price`, `sale_price`, `discount_percent`, `sale_start`, `sale_end`, `currency`, `is_free`, `sales_status`, `image`, `type`, `age_rating` {`system`, `rating`, `label` or `code`}. Americas search tiles add `badges[]` and `category`; deals add `on_sale` and, on the Americas, `amount_off` and `sale` {`sale`, `name`, `headline`}.
- **Grid** - `items[]`, `count`, `total` (`null` on Americas search), `page`, `page_size`, `total_pages`, `has_more` (Americas search), `requested_filters`. Search and deals add `sort` and `sorts_offered`; search adds `query`; releases adds `type`; Americas deals add `sale`, `heading`, `sales[]` {`sale`, `name`}.
- **product** - under `data.product`. Americas: `nsuid`, `sku`, `application_id`, `title`, `url`, `slug`, `platform`, `platform_label`, `platforms`, `category`, `type`, `release_date`, `release_date_text`, `publisher`, `developer`, `genres`, `features`, `ways_to_play`, `players` {`system`, `local`, `online`}, `languages`, `file_size_bytes`, `age_rating` {`system`, `rating`, `code`, `descriptors`}, `headline`, `description`, the price fields, `sales_status`, `purchasable`, `preorder`, `has_demo`, `demo_nsuid`, `edition`, `editions[]`, `is_upgrade`, `nintendo_switch_online` {`required`, `features`}, `play_modes`, `availability`, `stock` (My Nintendo Store goods), `dlc[]`, `image`, `images[]`. Europe: `nsuid`, `nsuids`, `page_id`, `application_id`, `title`, `url`, `platform`, `platforms`, `type`, `release_date`, `release_date_text`, `publisher`, `developer`, `genres`, `players` {`min`, `max`, `system`, `local`, `online`}, `languages`, `file_size`, `age_rating`, `description`, the price fields, `has_demo`, `nintendo_switch_online` {`required`, `online_play`, `cloud_saves`, `game_voucher`}, `physical_version`, `digital_version`, `game_series`, `base_game`, `images[]`, `copyright`. Japan: `nsuid`, `title`, `title_reading`, `url`, `platform`, `type`, `release_date`, `release_date_text`, `publisher`, `genres`, `players`, `languages`, `age_rating` {`system`: `CERO`, `rating`, `code`}, `description`, `headline`, the price fields, `has_demo`, `nintendo_switch_online`, `play_modes`, `format`, `dlc_nsuids`, `image`, `copyright`.
- **prices** - `prices[]` {`nsuid`, `sales_status`, `price`, `regular_price`, `sale_price`, `discount_percent`, `sale_start`, `sale_end`, `currency`, `is_free`}, `not_found[]` (ids that eShop does not sell), `count`.
- **dlc** - `game` {`nsuid`, `title`, `url`}, `dlc[]` {`nsuid`, `title`, `url`, `slug` (Americas), `type` (`dlc`, `bundle` or `upgrade`), `release_date`, the price fields, `sale_start`, `sale_end`, `sales_status`, `image`}, `count`.

## Guardrails

- Item ids are per eShop region (Americas; Europe with AU, NZ, ZA and IL; Japan; Korea; Hong Kong and Taiwan). Never send an id from one region to another region's country: `/prices` lists it in `not_found` and `/product` answers `404`. There is no cross-region title mapping: when you match one game across regions, say you matched it by title.
- `/prices` takes at most 50 ids per call and one country per call. Batch ids by region, one call per country.
- Americas search tiles have `nsuid: null` and no exact `total` (`has_more` instead): call `/product` with the `slug` to get the id. Americas search mixes games, hardware and merchandise (`type` per item) and sorts by `relevance` or `newest` only; it takes no filters.
- Americas deals are Nintendo's featured sale pages, not every discounted game in the Americas eShop: never say a game is not on sale because it is missing from `/deals` on an Americas market; check it with `/prices`. European and Japanese deals list every discounted game in the catalog.
- `sale_start` and `sale_end` are UTC timestamps from Nintendo. `discount_percent` is computed from `regular_price` and `sale_price`. Nintendo shows no price history or historical low: never call a sale price a record low. For a measured change, compare your own stored readings.
- In Europe the catalog is priced in GBP (English) or EUR; every answer carries the requested country's own eShop price, never the catalog's. European price sorts follow the catalog's own price, so on countries with another currency the order can be slightly off (`notes` says so). Grid items that country's eShop does not sell are kept with `sales_status: "not_found"` and `price: null`.
- Prices-only markets (`kr`, `hk`, `tw`, `il`) have no search, product, deals, releases or DLC (`400`). Their ids must come from elsewhere; Taiwan uses Hong Kong ids, Israel European ids.
- Nintendo Switch 2 Editions and upgrade packs are separate items with their own ids and prices (`platform: "switch_2"`; `/dlc` `type: "upgrade"`).
- The European catalog includes adult-rated titles listed by Nintendo; check `age_rating` before showing deals or search results to a general audience.
- Not available: user reviews (Nintendo's stores have none; age ratings only), best-seller charts, search suggestions, price history, cross-region title mapping, the Philippines and Russia.
- Prices are for research and pricing analysis. Nintendo's account terms tie purchases to the account's country: do not advise users to switch regions, change account country, use another region's gift cards or VPNs, or look for tax-free addresses.
- Terms: Nintendo of America's website terms ask users not to use robots, crawlers, scrapers or other automated means to access its websites to copy or extract data. We do not interpret them. This is not legal advice; the user is responsible for their own compliance. Do not republish box art, screenshots or logos; link store pages instead.
- Never fabricate prices, item ids, sale dates, release dates or titles. Only return what the API returned, with the country, the currency and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` outside the endpoint's markets (a prices-only market on a catalog endpoint; `ph`, `ru`, `uk` or a country with no eShop data); a `language` the market does not serve; no `query` on `/search`; none or more than one of `nsuid`, `url` and `slug`; an `nsuid` that is not 14 digits starting `70`; `slug` off the Americas; anything but `nsuid` on `jp`; a `url` that is not a served nintendo.com product link, or a `url` and `country` in different regions; more than 50 `ids`; a `sort` or filter the catalog does not support; `price_min` / `price_max` where the catalog is priced in another currency, or `price_max` below `price_min`; `page_size` other than 40 on Americas search; `page` or `page_size` on Americas releases; `sale` that is not a sale page slug.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Nintendo has no Americas eShop item ... on nintendo.com/us (item ids are per region: an id from another region is not found here).", "Nintendo has no europe eShop item ... in its en catalog (item ids are per region: ...)", "Nintendo has no store product ... on nintendo.com/...", "Nintendo has no European game page ...". Take ids from a previous answer in the same region rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api).
- `502` means Nintendo data was temporarily unavailable ("Nintendo is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Nintendo is busy ("Nintendo is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.61.0
npm install scavio@0.62.1
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.nintendo.search({ query: "mario", country: "gb", sort: "price_asc" });
const { data: game } = await scavio.nintendo.product({ slug: "mario-kart-world-switch-2" });
const { data: prices } = await scavio.nintendo.prices({ ids: ["70010000096802"], country: "pl" });
const { data: deals } = await scavio.nintendo.deals({ country: "de", sort: "discount" });
const { data: upcoming } = await scavio.nintendo.releases({ country: "jp", type: "upcoming" });
const { data: dlc } = await scavio.nintendo.dlc({ slug: "super-smash-bros-ultimate-switch" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.nintendo.search(...)`, `client.nintendo.product(...)`, `client.nintendo.prices(...)`, `client.nintendo.deals(...)`, `client.nintendo.releases(...)` and `client.nintendo.dlc(...)`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all six endpoints as tools: `search_nintendo`, `get_nintendo_product`, `get_nintendo_prices`, `get_nintendo_deals`, `get_nintendo_releases` and `get_nintendo_dlc`. Nintendo is opt-in: add `nintendo` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.59.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,nintendo"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/nintendo-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api), [product](https://scavio.dev/docs/nintendo-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api), [prices](https://scavio.dev/docs/nintendo-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api), [deals](https://scavio.dev/docs/nintendo-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api), [releases](https://scavio.dev/docs/nintendo-releases?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api), [DLC](https://scavio.dev/docs/nintendo-dlc?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api). Overview: [Nintendo eShop API](https://scavio.dev/nintendo-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api).
