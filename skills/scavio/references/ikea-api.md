# IKEA API - Prices by Country, Product Data, Stock by Store, Reviews

Read IKEA product data market by market: the price of one IKEA article number on up to 10 country sites in one call, keyword search and category listings with IKEA's own sorts and filters, one product in full, the newest reviews with sub-ratings, deal lists (new lower price, last chance, IKEA Family price and more), the category tree, search suggestions, stores with opening hours, the stock level of up to 100 article numbers at one store, a batch item lookup, and As-is (ex-display, returned and second-hand) offers at one store. All 12 endpoints return structured JSON and cost 1 credit each, except compare, which costs 1 credit per market that answered.

**The job this skill is for: IKEA prices by country.** IKEA prices every market on its own, and the same 8-digit article number is sold in many of them. `/compare` reads one article number on 2 to 10 markets at once and returns each market's price, previous price and price tag in that market's own currency. Captured 2026-11-13 for KALLAX shelf unit, white, article 80275887 (3.9 seconds, 6 credits):

| Market | Price | Previous price | `price_tag` |
|---|---|---|---|
| `de` Germany | EUR 49.99 | EUR 59.99 | `new_lower_price` |
| `nl` Netherlands | EUR 49.99 | EUR 69.99 | `new_lower_price` |
| `es` Spain | EUR 54.99 | EUR 59.99 | `new_lower_price` |
| `it` Italy | EUR 55 | EUR 69.95 | `new_lower_price` |
| `fr` France | EUR 59.99 | EUR 74.99 | `new_lower_price` |
| `se` Sweden | SEK 599 | none | `none` |

Prices are never converted: compare markets that share a currency directly, and if the user wants one currency, do the conversion yourself, say so, and give the exchange rate and its date. Prices include each market's own taxes and are the online list prices on the IKEA site on that day.

**Some markets use a different article number for the same product.** US, Canada, Japan, Australia, South Korea, India, Malaysia, Singapore, the Philippines and others sell many products under their own numbers, so `/compare` answers `found: false` there for a European number. That is not "not sold": in the captured US search, KALLAX shelf unit white is `item_no` 20631663 at USD 79.99 and carries `item_no_global` 80275887; in Japan the captured KALLAX shelf unit white 77x147 cm is 20351884 at JPY 9,990. Say plainly that the number differs; never report a `found: false` market as not carrying the product without searching it.

IKEA publishes no public developer API for its product catalog, prices or store stock. Its sites show stock to shoppers through a store picker, and the IKEA smart-home hubs' local interface (DIRIGERA, TRADFRI) is for devices, not product data.

See also: for US home-improvement prices by store use `home-depot-product-data`, `lowes-product-data` or `menards-product-data`; for the cross-retailer view of one product use `google-shopping-api`; for second-hand listings across Europe use `vinted-api` or `olx-api`.

## When to trigger

Use this skill when the user asks to:
- Compare IKEA prices by country, or find what an IKEA product costs in other countries (same article number, each market's currency)
- Track IKEA price changes market by market, including new lower prices and their valid-from dates (IKEA's European price cuts have run since 2026-09-01)
- Search IKEA products in any served market, in the market's own language, sorted by price, newest, rating, name or popularity
- Browse an IKEA category, or list IKEA deals: new lower price, last chance, IKEA Family member prices, new products, best sellers, limited editions
- Read one IKEA product in full by article number or link: price, previous price, IKEA Family price, measurements, materials, packages and weights, assembly instructions, variants, ratings
- Read IKEA product reviews and sub-ratings (appearance, ease of assembly, quality, value for money)
- Check whether an IKEA store has items in stock (a stock level per item: high, low or out of stock)
- Find IKEA stores in a country with opening hours, restaurant and Smaland hours, and coordinates
- List As-is (second-hand, ex-display, returned) offers at an IKEA store with condition and price
- Look up up to 100 IKEA article numbers in one call on one market

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint here costs 1 credit; `/compare` costs 1 credit per market that answered (a 6-market comparison is 6 credits).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Search, listing, stock, stores and compare calls took 0.6 to 8.2 seconds in the captures (search up to about 28 seconds in build testing). **Product and reviews calls are slow: up to about 100 seconds** (7.6 to 98.4 seconds, median 38.7, in build testing). Set a client timeout of at least 150 seconds and do not fire many product calls at once.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/ikea/compare` | 1 per market | One article number on 2 to 10 markets: per market `country`, `language`, `currency`, `found`, `name`, `type_name`, `design`, `price`, `previous_price`, `price_tag`, `url`; failed markets in `errors` (not charged) |
| `POST /api/v1/ikea/search` | 1 | A page of products for a keyword (24 by default, up to 100) with price, previous price, discount, price tag, rating, badge, colors, variants, last chance, category path; plus `total`, facets, `did_you_mean`, `related_searches` and `content` (inspiration pages) |
| `POST /api/v1/ikea/product` | 1 | One product by article number or IKEA product link: price, previous price, IKEA Family price with dates, currency, measurements, materials, care, safety, packages, assembly PDFs, manuals, designer, variants, rating, sub-ratings, the 3 newest reviews, return policy days |
| `POST /api/v1/ikea/reviews` | 1 | A product's rating, rating count, sub-ratings, the 20 most recent reviews and the highlighted reviews with their country |
| `POST /api/v1/ikea/category` | 1 | One category's products by category id or link, in the search shape, plus `category` {`id`, `name`, `url`, `parents`} |
| `POST /api/v1/ikea/categories` | 1 | The market's category tree (1,570 categories in the US capture) with ids for the category endpoint; `parent_id` for one subtree |
| `POST /api/v1/ikea/deals` | 1 | One deal list: `new_products`, `family_price`, `new_lower_price`, `last_chance`, `lowest_price`, `top_seller`, `limited_edition`, `time_restricted`, `in_store_price_only` or `reduced_price_offer`, in the search shape |
| `POST /api/v1/ikea/suggestions` | 1 | What the IKEA search box suggests for typed text: completions, categories (with `category_id`), products, planners and content |
| `POST /api/v1/ikea/stores` | 1 | The market's stores and pick-up / plan-and-order points with `store_id`, type, address, coordinates, opening hours with exceptions and closed days, restaurant, bistro, cafe, click and collect, Swedish Food Market and Smaland hours, opening date |
| `POST /api/v1/ikea/stock` | 1 | Stock at one store for up to 100 article numbers: per item `store_availability` {`status`, `text`} and, with `zip`, home delivery |
| `POST /api/v1/ikea/items` | 1 | Up to 100 article numbers on one market in one call, in the search item shape; numbers the market does not sell are in `not_found` |
| `POST /api/v1/ikea/as-is` | 1 | One store's As-is offers (ex-display, returned, discontinued, second-hand) with original price, offer price, condition and reason |

## Markets

Every endpoint except `/compare` takes `country` (lowercase, default `us`) and, on multi-language markets, `language`. Data comes in the market's language and currency: German names and EUR on `de`, Swedish and SEK on `se`, Japanese and JPY on `jp`, Chinese and CNY on `cn`. Quote names and labels as returned; translate them for the user only in your own words around the data.

**Search and product: 55 markets.** The 50 ikea.com markets: `us`, `ca`, `gb`, `ie`, `de`, `at`, `ch`, `fr`, `be`, `nl`, `dk`, `se`, `no`, `fi`, `ee`, `lv`, `lt`, `pl`, `cz`, `sk`, `hu`, `hr`, `si`, `rs`, `ro`, `pt`, `es`, `it`, `il`, `ae`, `sa`, `kw`, `qa`, `bh`, `om`, `jo`, `eg`, `ma`, `in`, `my`, `sg`, `ph`, `th`, `jp`, `kr`, `au`, `nz`, `mx`, `cl`, `co`; plus China (`cn`), Puerto Rico (`pr`), the Dominican Republic (`do`), the Canary and Balearic islands (`es_islands` with `island`) and Iceland (`is`).

| Endpoint | Markets |
|---|---|
| search, product | all 55 |
| category, deals, suggestions, items | the 50 ikea.com markets and `cn` |
| reviews, categories, stores, stock, compare | the 50 ikea.com markets |
| as-is | 13: `us`, `gb`, `de`, `fr`, `se`, `jp`, `nl`, `es`, `it`, `pl`, `au`, `ch`, `at` |

A market outside an endpoint's list answers `400` before anything is charged. IKEA sites for Ukraine, Greece, Cyprus, Bulgaria, Hong Kong, Taiwan, Indonesia and Turkey are not available.

**`language`** (default: the market's first language):

| Market | Languages |
|---|---|
| `us` | `en`, `es` |
| `ca` | `en`, `fr` |
| `ch` | `de`, `fr`, `it`, `en` |
| `be` | `nl`, `fr`, `en` |
| `es` | `es`, `en`, `ca`, `eu`, `gl` |
| `fi` | `fi`, `sv`, `en` |
| `ee`, `lv`, `lt` | local, `ru`, `en` |
| `ma` | `ar`, `fr`, `en` |
| `de`, `at`, `nl`, `se`, `no`, `cz`, `pt`, `my`, `th`, `jp`, `kr`, `mx` | local, `en` |
| `ae`, `sa`, `kw`, `qa`, `bh`, `om`, `jo`, `eg` | `ar`, `en` |
| `cn` | `zh`, `en` |
| `pr`, `is` | `en` first, then `es` (`pr`) or `is` (`is`) |
| `do`, `es_islands` | `es`, `en` |
| all others (`gb`, `ie`, `fr`, `dk`, `pl`, `sk`, `hu`, `hr`, `si`, `rs`, `ro`, `it`, `il`, `in`, `sg`, `ph`, `au`, `nz`, `cl`, `co`) | one language |

A `language` the market does not serve answers `400`. `/compare` has no `language`: each market answers in its default language.

**Franchise sites (`pr`, `do`, `es_islands`, `is`) are simpler.** Search takes `query` (and `page` on `is`) only; sort, filters, `store_id` and `page_size` answer `400` there. Puerto Rico, the Dominican Republic and the islands return **the first 40 results of a search only** (`total` still gives the full count, and the answer carries a `note`); Iceland pages through 40 per page. Product there answers name, description, price, currency, online availability, images and dimensions with `detail_level: "basic"`; there are no ratings. `es_islands` needs `island`: `tenerife`, `grancanaria`, `lanzarote`, `fuerteventura`, `lapalma`, `lagomera`, `elhierro`, `mallorca`, `menorca` or `ibiza`.

## Workflow

1. **Prices by country:** `/compare` with `item_no` and 2 to 10 `countries`. Read `found` per market; for each `found: false` market, `/search` that market for the product name and check `item_no_global` on the results against your article number (the US KALLAX above carries `item_no_global` 80275887). Report the market's own number and price, in its own currency.
2. **Find products:** `/search` with `query` on a `country`, add `sort` and filters. Filters use ids from `facets`: `color` (parameter `f-colors`), `price_bucket` (`f-price-buckets`), `category_id` (`f-subcategories`), or any other facet through `filters` keyed by `facets[].parameter`.
3. **Browse:** `/categories` for ids, then `/category` with `category_id`; or `/deals` with a `type` for new lower prices, last chance and IKEA Family prices.
4. **One product in full:** `/product` with `item_no` (8 digits, dots allowed: `802.758.87`) or the IKEA product `url` (the market and language are read from the link). Expect a slow answer.
5. **Reviews:** `/reviews` with `item_no` on a market. It always returns the 20 newest; there is no way to get older reviews.
6. **Store stock:** `/stores` on the market for `store_id`, then `/stock` with up to 100 `item_nos` and the `store_id`. Use the stock level, never a quantity.
7. **Many products at once:** `/items` with up to 100 article numbers on one market for prices and price tags in one call.
8. **Second-hand:** `/stores` for the `store_id`, then `/as-is` for that store's offers, paged 24 at a time (up to 48).
9. **Monitoring:** poll `/compare` or `/items` on a schedule, store `price`, `previous_price`, `price_tag` and the time per run, and compare runs yourself. There is no price history endpoint.

## Parameters

### Compare (`/compare`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_no` | string or integer | required | An IKEA article number: 8 digits, dots allowed (`80275887` or `802.758.87`) |
| `countries` | string[] | required | 2 to 10 distinct market codes from the 50 ikea.com markets (not `cn`, `pr`, `do`, `es_islands` or `is`) |

The balance must cover every asked market; only the markets that answered are charged. A `found: false` row is an answer and is charged.

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars), in any language the market serves |
| `country` | string | `us` | A market code (see Markets) |
| `language` | string | market's first | One of the market's languages |
| `island` | string | none | Required with `country: "es_islands"`, refused otherwise |
| `page` | integer | 1 | 1-based. `(page - 1) x page_size` may not exceed 2,000 |
| `page_size` | integer | 24 | Products per page, 1-100 |
| `sort` | string | `relevance` | `relevance`, `price_asc`, `price_desc`, `newest`, `rating`, `name_asc` or `most_popular` |
| `category_id` | string or string[] | none | Narrow to category id(s) from `facets` (parameter `f-subcategories`), e.g. `st002` |
| `color` | string or string[] | none | Color id(s) from `facets` (parameter `f-colors`), e.g. `10156` = white |
| `price_bucket` | string | none | A price range id from `facets` (parameter `f-price-buckets`), e.g. `PRICE_0_5000` |
| `new_only` | boolean | false | Only new products |
| `last_chance` | boolean | false | Only last-chance (being discontinued) products |
| `family_price` | boolean | false | Only products with an IKEA Family member price |
| `top_seller` | boolean | false | Only best sellers |
| `store_id` | string or integer | none | Adds each product's `availability` at that store and enables `availability` |
| `availability` | string | none | With `store_id`: `in_store`, `click_collect` or `online` |
| `filters` | object | none | Any other facet, keyed by `facets[].parameter`: `{"f-materials": ["47350"]}`; boolean facets take `true`. Up to 20 keys |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_no` | string or integer | one of | An article number |
| `url` | string | one of | An IKEA product page of a served market. Send `item_no` or `url`, not both |
| `country`, `language`, `island` | | | As on search; a `url` sets its own market and language, and a conflicting `country` or `language` answers `400` |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_no` / `url` | | one of | As on product |
| `country` | string | `us` | One of the 50 ikea.com markets |
| `language` | string | market's first | As on search |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | one of | A category id from `/categories`, a `category_path` or `facets` (e.g. `10382` = bookcases, `fu003` = sofas) |
| `url` | string | one of | An IKEA category page, e.g. `https://www.ikea.com/us/en/cat/bookcases-10382/` |
| `country`, `language` | | | As on search |
| `page`, `page_size`, `sort`, `color`, `price_bucket`, `new_only`, `last_chance`, `family_price`, `top_seller`, `store_id`, `availability`, `filters` | | | As on search (no `category_id` filter: the category is the target) |

### Categories (`/categories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country`, `language` | | | As on search |
| `parent_id` | string | none | Return only this category's subtree |

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | required | `new_products`, `family_price`, `new_lower_price`, `last_chance`, `lowest_price`, `top_seller`, `limited_edition`, `time_restricted`, `in_store_price_only` or `reduced_price_offer` |
| `country`, `language` | | | As on search |
| grid params | | | As on search |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the user has typed so far (1-100 chars) |
| `country`, `language` | | | As on search |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country`, `language` | | | As on search |
| `query` | string | none | Only stores whose name, city, ZIP / postal code or address contains this text |
| `lat` / `lng` | number | none | Send together: stores sorted by distance from this point, with `distance_km` |
| `limit` | integer | 50 | Stores to return, 1-200 |

### Stock (`/stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_nos` | string[] or string | required | 1 to 100 article numbers (a list or a comma-separated string) |
| `store_id` | string or integer | required | `stores[].store_id` of `/stores` on the same market (e.g. `399` = Burbank, CA) |
| `zip` | string | none | A postal code: adds home-delivery availability to that address |
| `country`, `language` | | | As on search |

### Items (`/items`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_nos` | string[] or string | required | 1 to 100 article numbers |
| `country`, `language` | | | As on search |

### As-is (`/as-is`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string or integer | required | A store of the same market |
| `country`, `language` | | | As on search (13 markets) |
| `page` | integer | 1 | 1-based |
| `page_size` | integer | 24 | 1-48 |

## Examples

### Compare one article across markets

```bash
curl -X POST https://api.scavio.dev/api/v1/ikea/compare \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_no": "80275887", "countries": ["de", "fr", "se", "nl", "es", "it"]}'
```

Captured `data` (2026-11-13; 3 of 6 markets shown, `credits_used: 6`):

```json
{
  "item_no": "80275887",
  "count": 6,
  "found_count": 6,
  "markets": [
    {
      "country": "de",
      "language": "de",
      "currency": "EUR",
      "found": true,
      "name": "KALLAX",
      "type_name": "Regal",
      "design": "weiß",
      "price": 49.99,
      "previous_price": 59.99,
      "price_tag": "new_lower_price",
      "url": "https://www.ikea.com/de/de/p/kallax-regal-weiss-80275887/"
    },
    {
      "country": "fr",
      "language": "fr",
      "currency": "EUR",
      "found": true,
      "name": "KALLAX",
      "type_name": "Étagère",
      "design": "blanc",
      "price": 59.99,
      "previous_price": 74.99,
      "price_tag": "new_lower_price",
      "url": "https://www.ikea.com/fr/fr/p/kallax-etagere-blanc-80275887/"
    },
    {
      "country": "se",
      "language": "sv",
      "currency": "SEK",
      "found": true,
      "name": "KALLAX",
      "type_name": "Hylla",
      "design": "vit",
      "price": 599,
      "previous_price": null,
      "price_tag": "none",
      "url": "https://www.ikea.com/se/sv/p/kallax-hylla-vit-80275887/"
    }
  ],
  "errors": [],
  "note": "Prices are in each market's own currency and are not converted. Some markets (us, ca, jp, au, kr, in, my, sg, ph ...) sell the same product under a different article number, so found is false there."
}
```

`count` is the markets that answered, `found_count` the ones that sell this number. A market that failed is listed in `errors` as {`country`, `error`} and is not charged.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/ikea/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "kallax"}'
```

Captured `data` (US; 1 of 24 items, 1 of 20 facets, 1 of 10 related searches and 1 of 6 content entries shown, image lists trimmed):

```json
{
  "query": "kallax",
  "total": 252,
  "page": 1,
  "page_size": 24,
  "total_pages": 11,
  "count": 24,
  "sort": "relevance",
  "applied_filters": {},
  "items": [
    {
      "item_no": "20631663",
      "item_no_global": "80275887",
      "is_combination": false,
      "name": "KALLAX",
      "type_name": "Shelf unit",
      "design": "white",
      "measure_text": "30 1/8x57 5/8 \"",
      "url": "https://www.ikea.com/us/en/p/kallax-shelf-unit-white-20631663/",
      "image": "https://www.ikea.com/us/en/images/products/kallax-shelf-unit-white__0644757_pe702939_s5.jpg",
      "images": ["https://www.ikea.com/us/en/images/products/kallax-shelf-unit-white__0644757_pe702939_s5.jpg"],
      "price": 79.99,
      "previous_price": null,
      "discount_amount": null,
      "discount_percent": null,
      "price_tag": "none",
      "price_tag_text": null,
      "lowest_price": false,
      "price_valid_from": null,
      "price_valid_to": null,
      "rating": 4.9,
      "rating_count": 23,
      "badge": {"type": "top_seller", "text": "Best seller"},
      "colors": [{"id": "10156", "name": "white", "hex": "ffffff"}],
      "variant_count": 2,
      "variants": [
        {
          "item_no": "00637289",
          "name": "KALLAX",
          "type_name": "Shelf unit",
          "design": "white stained oak effect",
          "url": "https://www.ikea.com/us/en/p/kallax-shelf-unit-white-stained-oak-effect-00637289/",
          "image": "https://www.ikea.com/us/en/images/products/kallax-shelf-unit-white-stained-oak-effect__0459250_pe606049_s5.jpg",
          "price": 79.99,
          "previous_price": null,
          "price_tag": "none",
          "rating": 4.9,
          "rating_count": 23
        }
      ],
      "last_chance": false,
      "online_sellable": true,
      "category_path": [{"id": "st001", "name": "Storage & organization"}],
      "availability": null
    }
  ],
  "facets": [
    {
      "id": "MEASUREMENT_BUCKETS",
      "name": "Size",
      "parameter": "f-measurement-buckets",
      "type": "list",
      "count": null,
      "values": [{"id": "WIDTH_0_20", "label": "Width: 0 - 19 \"", "count": 63, "selected": false}]
    }
  ],
  "did_you_mean": [],
  "related_searches": [{"text": "kallax insert", "count": 52}],
  "content": [
    {
      "type": "planner",
      "title": "Design your own KALLAX storage",
      "label": "Planner",
      "url": "https://www.ikea.com/addon-app/storageone/kallax/web/latest/us/en/",
      "image": "https://www.ikea.com/images/kallax-regale-in-verschiedenen-farben-in-weiss-und-schwarz-u-ad4707b7fdae48fe042ff02ed612ff5f.jpg"
    }
  ],
  "country": "us",
  "language": "en",
  "currency": "USD"
}
```

This US item is `item_no` 20631663 with `item_no_global` 80275887: the US sells KALLAX under its own number. The search facet parameters in this capture: `f-measurement-buckets`, `f-colors`, `f-type`, `f-cube-hole`, `f-series`, `f-materials`, `f-price-buckets`, `f-subcategories`, `f-appearance`, `f-doors`, `f-feature`, `f-ratings`, `f-last-chance`, `f-offers`, `f-top-seller`, `f-new-product`, `f-suitable-for`, `f-front`, `f-suitable-for-business`, `f-home-smart`. They vary by query and market: read them from each answer.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/ikea/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_no": "20522046"}'
```

Captured `data` (US; lists trimmed to 1 or 2 entries, description shortened):

```json
{
  "item_no": "20522046",
  "article_number": "205.220.46",
  "name": "BILLY",
  "full_name": "BILLY Bookcase - white 31 1/2x11x79 1/2 \"",
  "type_name": "Bookcase",
  "description": "BILLY bookcase is a beloved icon that never goes out of style. ...",
  "url": "https://www.ikea.com/us/en/p/billy-bookcase-white-20522046/",
  "price": 79,
  "previous_price": null,
  "price_valid_from": null,
  "price_valid_to": null,
  "family_price": null,
  "currency": "USD",
  "color": "white",
  "material": "Wood (including board)",
  "category": "Bookshelves & bookcases",
  "dimensions": {"width": "31 1/2 \"", "depth": "11 \"", "height": "79 1/2 \"", "weight": null},
  "images": ["https://www.ikea.com/us/en/images/products/billy-bookcase-white__1590272_pe1038911_s5.jpg"],
  "rating": 4.5,
  "rating_count": 2126,
  "availability_online": "in_stock",
  "summary": "Bookcase, white",
  "measure_text": "31 1/2x11x79 1/2 \"",
  "price_tag": "lower_price_in_store",
  "price_note": null,
  "lower_price_in_store": true,
  "online_sellable": true,
  "badge": {"type": "top_seller", "text": "Best seller"},
  "measurements": [{"name": "Width", "value": "31 1/2 \""}, {"name": "Depth", "value": "11 \""}],
  "materials": [{"part": "Main parts/ Plinth front:", "material": "Particleboard, Paper foil"}],
  "care": ["Wipe clean using a damp cloth and a mild cleaner.", "Wipe dry with a clean cloth."],
  "good_to_know": [{"name": "Included", "text": "1 stationary shelf and 4 adjustable shelves included."}],
  "safety": [{"name": "Warning", "text": "WARNING! Tipping hazard – this product must be securely anchored. Use suitable screws and plugs for your home. If you are uncertain, seek professional advice."}],
  "packaging": {
    "number_of_packages": 1,
    "packages": [
      {
        "item_no": "20522046",
        "article_number": "205.220.46",
        "name": "BILLY",
        "type_name": "Bookcase",
        "dimensions": {
          "width": {"text": "11 ¾ \"", "value": 11.75},
          "height": {"text": "5 \"", "value": 5},
          "length": {"text": "81 ¼ \"", "value": 81.25},
          "diameter": null
        },
        "weight": {"text": "85 lb 3 oz", "value": 85.188},
        "quantity": 1
      }
    ],
    "max_weight": "85 lb 3 oz"
  },
  "assembly_pdfs": [{"label": "BILLY Bookcase", "url": "https://www.ikea.com/us/en/assembly_instructions/billy-bookcase-white__AA-2289108-3-100.pdf", "article_number": "205.220.46"}],
  "manuals": [{"label": "BILLY Bookcase", "url": "https://www.ikea.com/us/en/manuals/billy-bookcase-white__AA-2180177-2-2.pdf", "article_number": "205.220.46"}],
  "other_documents": [],
  "designer": "Gillis Lundgren",
  "variants": [
    {
      "type": "colour",
      "title": "Choose color",
      "selected": "White",
      "options": [
        {"title": "White", "item_no": "20522046", "url": "https://www.ikea.com/us/en/p/billy-bookcase-white-20522046/", "price": 79, "selected": true, "image": "https://www.ikea.com/us/en/images/products/billy-bookcase-white__1590272_pe1038911_s5.jpg"},
        {"title": "Black oak effect", "item_no": "40477340", "url": "https://www.ikea.com/us/en/p/billy-bookcase-black-oak-effect-40477340/", "price": 89, "selected": false, "image": "https://www.ikea.com/us/en/images/products/billy-bookcase-black-oak-effect__1590300_pe1038939_s5.jpg"}
      ]
    }
  ],
  "secondary_ratings": [{"id": "appearance", "label": "Appearance", "value": 4.6}, {"id": "ease_of_assembly", "label": "Ease of assembly/installation", "value": 4.7}],
  "reviews_preview": [
    {"title": "Cracked and Dirty", "text": "My bookshelf came with a large crack right across one of the sideboards, and also came with a dark brown stain that I couldn’t wipe off with an alcohol wipe", "rating": 1, "date": "2026-11-08T17:23:23Z", "author": "Janelle", "country": null}
  ],
  "return_policy_days": 365,
  "detail_level": "full",
  "country": "us",
  "language": "en"
}
```

`lower_price_in_store: true` is IKEA's own flag that the item has a lower price in store; that store price is not returned, only the online `price`. When the product has an IKEA Family member price, `family_price` carries it with its dates.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/ikea/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_no": "80275887", "country": "de"}'
```

Captured `data` (Germany; 1 of 20 reviews, 1 of 3 highlighted, 2 of 5 sub-ratings shown):

```json
{
  "item_no": "80275887",
  "name": "KALLAX Regal - weiß 77x147 cm",
  "url": "https://www.ikea.com/de/de/p/kallax-regal-weiss-80275887/",
  "rating": 4.7,
  "rating_count": 8241,
  "secondary_ratings": [
    {"id": "appearance", "label": "Design/Aussehen", "value": 4.7},
    {"id": "value_for_money", "label": "Preis-Leistungs-Verhältnis", "value": 4.6}
  ],
  "count": 20,
  "reviews": [
    {"title": "Vielseitig einsetzbar", "text": "Super verarbeitet, super einfach zum aufbauen einfach nur schön!!", "rating": 5, "date": "2026-11-12T20:49:37Z", "author": "Sylvia", "country": null}
  ],
  "highlighted": [
    {"title": "Zeitloses Design", "text": "Viel Stauraum und einfacher Montage. Vielseitig einsetzbar und ein super Preis-Leistungs-Verhältnis. Absolut empfehlenswert!", "rating": 5, "author": "Petra", "country": "de", "country_name": "Deutschland"}
  ],
  "detail_level": "full",
  "country": "de",
  "language": "de",
  "currency": "EUR"
}
```

The sub-rating ids in this capture: `appearance`, `ease_of_assembly`, `product_quality`, `value_for_money`, `works_as_expected`. **`rating` and `rating_count` are what that market's site shows.** Many markets share one pool: KALLAX scored 4.7 from 8,241 ratings in Germany, Spain and Sweden (and on the Japanese product page). Others carry their own count (France 2,760, Italy 1,887), and some show no rating at all (Estonia, Latvia, Lithuania, Israel and Iceland return `rating: null`). Do not present a shared-pool rating as one country's opinion, and do not add up rating counts across markets: markets on the same pool repeat the same ratings.

### Stock at a store

```bash
curl -X POST https://api.scavio.dev/api/v1/ikea/stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_nos": ["20522046", "20631663"], "store_id": "399"}'
```

Captured `data` (US store 399; 1 of 2 items shown):

```json
{
  "store": {"id": "399", "name": "Burbank, CA"},
  "zip": null,
  "count": 2,
  "items": [
    {
      "item_no": "20522046",
      "name": "BILLY",
      "type_name": "Bookcase",
      "design": "white",
      "url": "https://www.ikea.com/us/en/p/billy-bookcase-white-20522046/",
      "price": 79,
      "store_availability": {"status": "in_stock_high", "text": "In stock in Burbank, CA"},
      "home_delivery": null,
      "click_collect": null
    }
  ],
  "not_found": [],
  "country": "us",
  "language": "en",
  "currency": "USD"
}
```

`status` is a level: `in_stock_high`, `in_stock_low` or `out_of_stock`, as IKEA gives it. IKEA does not publish unit counts, so never state a quantity. Send `zip` to fill `home_delivery`.

### Items (batch lookup)

```bash
curl -X POST https://api.scavio.dev/api/v1/ikea/items \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_nos": ["80275887", "00263850", "30275861"], "country": "de"}'
```

The captured answer has `count: 3`, `not_found: []` and three items in the search item shape: KALLAX Regal weiß 80275887 at EUR 49.99 (previous 59.99, `price_tag` `new_lower_price`, `price_tag_text` "Neuer niedriger Preis", `price_valid_from` "2026-09-01", `price_valid_to` "2027-08-31"), BILLY Bücherregal weiß 00263850 at EUR 49.99 (`price_tag` `none`), and KALLAX Regal weiß 30275861 at EUR 99 (previous 129, `new_lower_price`).

### Deals

```bash
curl -X POST https://api.scavio.dev/api/v1/ikea/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "new_lower_price", "country": "gb"}'
```

The captured UK answer has `type: "new_lower_price"`, `total: 474`, 24 items per page over 20 pages, in the search shape. The first items: KALLAX Shelving unit at GBP 49 (previous 60), UPPDATERA Box at GBP 1 (previous 2), KALLAX Shelving unit at GBP 39 (previous 50), STORKLINTA Chest of 6 drawers at GBP 139 (previous 149), ALEX Drawer unit at GBP 55 (previous 70), each with `price_valid_from` "2026-08-28".

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/ikea/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "se"}'
```

Captured `data` (Sweden, 22 stores; 1 shown, hour lists trimmed):

```json
{
  "total": 22,
  "count": 22,
  "query": null,
  "stores": [
    {
      "store_id": "248",
      "name": "IKEA Borlänge",
      "display_name": "Borlänge",
      "type": "store",
      "type_name": "IKEA STORE",
      "address": {"street": "Norra Backagatan 1", "city": "Borlänge", "zip": "781 70", "state": "SEW", "timezone": "Europe/Stockholm", "display": "Norra Backagatan 1, Borlänge"},
      "latitude": 60.4815,
      "longitude": 15.4198,
      "hours": {
        "normal": [{"day": "MON", "open": "10:00", "close": "19:00"}],
        "exceptions": [{"date": "2026-10-31", "open": "11:00", "close": "18:00", "reason": "Alla helgons dag"}],
        "closed": [{"date": "2026-12-24", "reason": "Julafton"}]
      },
      "restaurant_hours": [{"day": "MON", "open": "11:00", "close": "18:30"}],
      "bistro_hours": [{"day": "MON", "open": "10:00", "close": "19:00"}],
      "cafe_hours": [],
      "click_collect_hours": [{"day": "MON", "open": "10:00", "close": "19:00"}],
      "swedish_food_market_hours": [],
      "smaland_hours": [{"day": "SAT", "open": "10:00", "close": "18:00"}],
      "cash_and_carry": true,
      "store_url": "https://www.ikea.com/se/sv/stores/borlange/",
      "opening_date": "2013-10-25"
    }
  ],
  "country": "se",
  "language": "sv",
  "currency": "SEK"
}
```

### As-is (second-hand) offers

```bash
curl -X POST https://api.scavio.dev/api/v1/ikea/as-is \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "257"}'
```

Captured `data` (US store 257: 108 offers over 5 pages; 1 shown):

```json
{
  "store_id": "257",
  "total": 108,
  "page": 1,
  "page_size": 24,
  "total_pages": 5,
  "count": 24,
  "offers": [
    {
      "title": "AURDAL",
      "description": "side panel with leg, 15 3/4x87 \", oak veneer",
      "article_numbers": ["50607973"],
      "store_id": "257",
      "currency": "USD",
      "original_price": 50,
      "min_price": 25,
      "max_price": 25,
      "image": "https://www.ikea.com/us/en/images/products/aurdal-side-panel-with-leg-oak-veneer__1452298_pe990902_s4.jpg",
      "offers": [
        {
          "offer_id": "117406154269946914",
          "offer_number": "881468310",
          "description": "side panel with leg, 15 3/4x87 \", oak veneer",
          "additional_info": "Scuffed side",
          "price": 25,
          "lowest_previous_price": null,
          "condition_code": "FAIR",
          "condition": "Fair",
          "condition_description": "The product shows noticeable signs of use or cosmetic wear but remains fully functional and safe to use.",
          "in_box": false,
          "reason_discount": "Handling damage"
        }
      ]
    }
  ],
  "country": "us",
  "language": "en",
  "currency": "USD"
}
```

`offer_id` is a string on purpose: it is 18 digits long and would lose precision as a JSON number. Conditions seen in the capture: Brand New, As New, Good, Fair (and `null`); reasons: Customer return, Discontinued product, Handling damage. Nothing is reserved or bought: the shopper still has to go to the store.

### Suggestions, categories and category

- `/suggestions` with `{"query": "sof"}` (US) returned 8: six completions ("sofa", "sofabed", "sofa bed", "sofa sleeper", "sofa table", "sofa cover") and two categories, "Sofas & sectionals" (`category_id` `fu003`) and "Sofas & armchairs" (`700640`), each with `text`, `type`, `label`, `url`, `category_id`, `item_no`, `image`.
- `/categories` (US) returned `count: 1570` as a tree of {`id`, `name`, `url`, `children`}; the first top-level entry was "Winter holiday shop" (`wt001`).
- `/category` with `{"category_id": "10382"}` (US) returned `category` {`id`: "10382", `name`: "Bookshelves & bookcases", `parents`: ["st001", "st002"]}, `total: 133` and 24 items in the search shape, the first BILLY Bookcase white 20522046 at USD 79.

### A franchise site: Puerto Rico

```bash
curl -X POST https://api.scavio.dev/api/v1/ikea/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "kallax", "country": "pr"}'
```

Captured `data` (1 of 40 items shown):

```json
{
  "query": "kallax",
  "total": 145,
  "page": 1,
  "page_size": 40,
  "total_pages": 1,
  "count": 40,
  "items": [
    {
      "item_no": "00631635",
      "article_number": "006.316.35",
      "name": "KALLAX",
      "type_name": "shelf unit",
      "design": "black-brown",
      "measure_text": "41.5x39x146.5 cm",
      "url": "https://www.ikea.pr/puertorico/en/pd/kallax-shelf-unit-black-brown-art-00631635",
      "image": "https://static2.ikea.pr/assets/images/250/0625059_PE692080_S3.jpg",
      "price": 95,
      "previous_price": null,
      "family_price": null,
      "is_new": true,
      "online_sellable": true,
      "designer": "Tord Björklund",
      "category": "Open storage"
    }
  ],
  "note": "This IKEA site serves the first 40 results of a search; refine the query for more.",
  "country": "pr",
  "language": "en",
  "currency": "USD"
}
```

`total` is 145 but only 40 items can be read: refine the query (add a type or color) to reach the rest. `/product` on `pr` for 00631635 answered `detail_level: "basic"` with name, description, price 95 USD, `availability_online: "in_stock"`, images and dimensions, and `rating: null`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def ikea(endpoint, body, timeout=180):
    r = requests.post(f"{BASE}/api/v1/ikea/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()["data"]

ARTICLE = "80275887"  # KALLAX shelf unit, white

# 1. Same article number on six markets (1 credit per market that answers)
cmp = ikea("compare", {"item_no": ARTICLE, "countries": ["de", "fr", "nl", "es", "it", "us"]})
for m in cmp["markets"]:
    if m["found"]:
        print(m["country"], m["currency"], m["price"], "was", m["previous_price"], m["price_tag"])

# 2. Markets that use their own number: search there and match item_no_global (1 credit each)
for m in cmp["markets"]:
    if not m["found"]:
        hits = ikea("search", {"query": "kallax", "country": m["country"]})["items"]
        same = [i for i in hits if i.get("item_no_global") == ARTICLE]
        for i in same:
            print(m["country"], "sells it as", i["item_no"], i["price"], m["currency"])
        if not same:
            print(m["country"], "no item with item_no_global", ARTICLE, "on the first page")

for e in cmp["errors"]:
    print("failed, not charged:", e["country"], e["error"])
```

Never subtract or rank prices across different currencies without converting them first, and say which rate you used.

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live; nothing is cached. Every `data` echoes `country`, `language` (and `island` on `es_islands`) and, on most endpoints, `currency`.

- **grid item** (search, category, deals, items `items[]`) - `item_no`, `item_no_global`, `is_combination`, `name`, `type_name`, `design`, `measure_text`, `url`, `image`, `images[]`, `price`, `previous_price`, `discount_amount`, `discount_percent`, `price_tag` (`family_price`, `new_lower_price`, `time_restricted_offer` (a limited-time reduced price with `previous_price` and valid dates, seen on `th`), `lower_price_in_store`, `new_product`, `discontinued` or `none`), `price_tag_text`, `lowest_price`, `price_valid_from`, `price_valid_to`, `rating`, `rating_count`, `badge` {`type` (`top_seller`, `limited_edition`), `text`}, `colors[]` {`id`, `name`, `hex`}, `variant_count`, `variants[]`, `last_chance`, `online_sellable`, `category_path[]` {`id`, `name`}, `availability` (with `store_id`: the store's level and home delivery; otherwise `null`).
- **search / category / deals** - `total`, `page`, `page_size`, `total_pages`, `count`, `sort`, `applied_filters`, `items[]`, `facets[]` {`id`, `name`, `parameter`, `type`, `count`, `values[]` {`id`, `label`, `count`, `selected`}}; search adds `query`, `did_you_mean`, `related_searches[]` {`text`, `count`}, `content[]` {`type`, `title`, `label`, `url`, `image`}; category adds `category` {`id`, `name`, `url`, `parents[]`}; deals add `type`.
- **franchise search** (`pr`, `do`, `es_islands`) - `items[]` {`item_no`, `article_number`, `name`, `type_name`, `design`, `measure_text`, `url`, `image`, `price`, `previous_price`, `family_price`, `is_new`, `online_sellable`, `designer`, `category`} and `note`; Iceland `items[]` {`item_no`, `article_number`, `name`, `type_name`, `description`, `url`, `image`, `price`, `previous_price`, `lower_price`}.
- **product** - `item_no`, `article_number`, `name`, `full_name`, `type_name`, `summary`, `description`, `url`, `price`, `previous_price`, `price_valid_from`, `price_valid_to`, `family_price`, `currency`, `color`, `material`, `category`, `dimensions`, `images[]`, `rating`, `rating_count`, `availability_online`, `measure_text`, `price_tag`, `price_note`, `lower_price_in_store`, `online_sellable`, `badge`, `measurements[]`, `materials[]`, `care[]`, `good_to_know[]`, `safety[]`, `packaging` {`number_of_packages`, `packages[]`, `max_weight`}, `assembly_pdfs[]`, `manuals[]`, `other_documents[]`, `designer`, `variants[]` {`type`, `title`, `selected`, `options[]`}, `secondary_ratings[]`, `reviews_preview[]` (3 newest), `return_policy_days`, `detail_level` (`full` or `basic`). `basic` carries the core fields only (no packaging, assembly or variants). `cn` answers in Chinese with `design`, `measure_text`, `lowest_price`, `is_new`, `series` and its own `packaging` shape; franchise sites answer `basic`.
- **reviews** - `item_no`, `name`, `url`, `rating`, `rating_count`, `secondary_ratings[]` {`id`, `label`, `value`}, `count`, `reviews[]` {`title`, `text`, `rating`, `date`, `author`, `country`}, `highlighted[]` {`title`, `text`, `rating`, `author`, `country`, `country_name`}, `detail_level`.
- **categories** - `parent_id`, `count`, `categories[]` {`id`, `name`, `url`, `children[]`}.
- **suggestions** - `query`, `count`, `suggestions[]` {`text`, `type` (`completion`, `category`, `product`, `planner`, `content`), `label`, `url`, `category_id`, `item_no`, `image`}.
- **stores** - `total`, `count`, `query`, `stores[]` {`store_id`, `name`, `display_name`, `type` (`store`, `small_store`, `plan_and_order_point`, `shop` ...), `type_name`, `address` {`street`, `city`, `zip`, `state`, `timezone`, `display`}, `latitude`, `longitude`, `hours` {`normal[]`, `exceptions[]`, `closed[]`}, `restaurant_hours`, `bistro_hours`, `cafe_hours`, `click_collect_hours`, `swedish_food_market_hours`, `smaland_hours`, `cash_and_carry`, `store_url`, `opening_date`, `distance_km` (with `lat` / `lng`)}.
- **stock** - `store` {`id`, `name`}, `zip`, `count`, `items[]` {`item_no`, `name`, `type_name`, `design`, `url`, `price`, `store_availability` {`status`, `text`}, `home_delivery`, `click_collect`}, `not_found[]`.
- **items** - `count`, `items[]` (grid items), `not_found[]`.
- **compare** - `item_no`, `count`, `found_count`, `markets[]` {`country`, `language`, `currency`, `found`, `name`, `type_name`, `design`, `price`, `previous_price`, `price_tag`, `url`}, `errors[]` {`country`, `error`}, `note`.
- **as-is** - `store_id`, `total`, `page`, `page_size`, `total_pages`, `count`, `offers[]` {`title`, `description`, `article_numbers[]`, `store_id`, `currency`, `original_price`, `min_price`, `max_price`, `image`, `offers[]` {`offer_id`, `offer_number`, `description`, `additional_info`, `price`, `lowest_previous_price`, `condition_code`, `condition`, `condition_description`, `in_box`, `reason_discount`}}.

## Guardrails

- Currency: always give the currency and the market next to a price. Prices are never converted. Never average, rank or subtract prices in different currencies as if they were one; convert explicitly, with the rate and date, or compare only markets that share a currency.
- Article numbers: `found: false` in `/compare` or `not_found` in `/items` means that market does not sell this number, not that it lacks the product. Check `item_no_global` in a search on that market before saying a product is not sold there.
- Prices are each market's online list price on the IKEA site on the day of the call, with that market's taxes. IKEA's US terms say "The prices displayed on our website may differ from prices displayed on our mobile sites and applications or in stores" and "Pricing may differ from store to store". Do not present an online price as a shelf price in a given store.
- `previous_price` is the earlier price IKEA shows next to a reduced one (with `price_valid_from` / `price_valid_to` when given). It is not a price history; for one, poll and store prices yourself.
- `price_tag: "family_price"` on a grid item means `price` is the IKEA Family member price and `previous_price` the regular price. Say "IKEA Family price" when quoting it: it is the price for IKEA Family members, not the regular price.
- Reviews: `/reviews` returns the 20 most recent reviews only. There is no paging, sort or star filter. Never present them as all reviews or compute a star distribution from them; use `rating`, `rating_count` and `secondary_ratings` for the overall picture.
- `rating` and `rating_count` are what that market's site shows: many markets share one pool (KALLAX: 8,241 in Germany, Spain, Sweden), others have their own (France 2,760, Italy 1,887), and some show none (Estonia, Latvia, Lithuania, Israel, Iceland return `rating: null`). Never add counts across markets: markets on one pool repeat the same ratings.
- Stock is a level (`in_stock_high`, `in_stock_low`, `out_of_stock`), not a quantity. IKEA does not publish unit counts; never estimate one.
- Product and reviews calls can take up to about 100 seconds. Use a long client timeout and call them sequentially, not in bursts.
- Franchise sites (`pr`, `do`, `es_islands`): search returns the first 40 results only; product returns `detail_level: "basic"` with no ratings. Iceland (`is`) pages normally.
- As-is offers are listed, not reserved: nothing is held for the shopper.
- Not available: the IKEA sites for Ukraine, Greece, Cyprus, Bulgaria, Hong Kong, Taiwan, Indonesia and Turkey; review paging; stock quantities, restock dates or aisle locations; cart, delivery quotes and checkout; IKEA Family account data; spare parts; price history. On `cn`, reviews, stores, stock, categories and compare are not offered.
- Terms: IKEA's US Terms and Conditions (effective September 2, 2026) say users "may not use any robot, spider, other automatic device, or manual process to monitor, copy or scrape any of our web pages or the content contained herein, without the prior express written consent from an authorized executive of IKEA". Each IKEA market publishes its own terms. This is not legal advice; the user is responsible for checking the current terms for their market and use case. Do not republish IKEA product photos; link product pages instead.
- Never fabricate prices, article numbers, store ids, stock levels, reviews or ratings. Only return what the API returned, with the market and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` outside the endpoint's markets ("country xx is not available on this endpoint; use one of: ..."); a `language` the market does not serve; `island` missing with `es_islands` or sent with another country; `item_no` that is not 8 digits; both or neither of `item_no` / `url` (or `category_id` / `url`); a `url` whose market or language conflicts with `country` / `language`; `(page - 1) x page_size` above 2,000; sort, filters, `store_id` or `page_size` on a franchise site; `availability` without `store_id`; a `filters` key that is not a facet parameter; `countries` with fewer than 2 or more than 10 distinct markets; more than 100 `item_nos`; `lat` without `lng`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`. On `/compare` the balance must cover every asked market.
- `404` means an unknown article number on that market ("IKEA de has no product page for article ..."), an unknown category id, an unknown store id on `/stock`, a store of another market on `/as-is`, or a search with no result on a franchise site ("Nothing was found for this query."). Not-founds are charged 1 credit: take article numbers, category ids and store ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api).
- `502` means IKEA data was temporarily unavailable ("IKEA is temporarily unavailable. Please try again."). Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds. On `/compare`, one market failing does not fail the call: it is listed in `errors` and not charged.
- `503` with a `Retry-After` header means IKEA is busy: wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.56.0
npm install scavio@0.57.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: byCountry } = await scavio.ikea.compare({ item_no: "80275887", countries: ["de", "fr", "se", "nl", "es", "it"] });
const { data: found } = await scavio.ikea.search({ query: "kallax", country: "de", sort: "price_asc" });
const { data: product } = await scavio.ikea.product({ item_no: "20522046" });
const { data: reviews } = await scavio.ikea.reviews({ item_no: "80275887", country: "de" });
const { data: shelves } = await scavio.ikea.category({ category_id: "10382" });
const { data: tree } = await scavio.ikea.categories({ country: "us" });
const { data: cuts } = await scavio.ikea.deals({ type: "new_lower_price", country: "gb" });
const { data: hints } = await scavio.ikea.suggestions({ query: "sof" });
const { data: stores } = await scavio.ikea.stores({ country: "se" });
const { data: stock } = await scavio.ikea.stock({ item_nos: ["20522046", "20631663"], store_id: "399" });
const { data: items } = await scavio.ikea.items({ item_nos: ["80275887", "00263850"], country: "de" });
const { data: asIs } = await scavio.ikea.asIs({ store_id: "257" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.ikea.compare(...)`, `client.ikea.search(...)`, `client.ikea.product(...)`, `client.ikea.reviews(...)`, `client.ikea.category(...)`, `client.ikea.categories(...)`, `client.ikea.deals(...)`, `client.ikea.suggestions(...)`, `client.ikea.stores(...)`, `client.ikea.stock(...)`, `client.ikea.items(...)` and `client.ikea.as_is(...)`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all twelve endpoints as tools: `compare_ikea_prices`, `search_ikea`, `get_ikea_product`, `get_ikea_reviews`, `get_ikea_category`, `get_ikea_categories`, `get_ikea_deals`, `get_ikea_suggestions`, `find_ikea_stores`, `get_ikea_stock`, `get_ikea_items` and `get_ikea_as_is`. IKEA is opt-in: add `ikea` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.54.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,ikea"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [compare](https://scavio.dev/docs/ikea-compare?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api), [search](https://scavio.dev/docs/ikea-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api), [product](https://scavio.dev/docs/ikea-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api), [reviews](https://scavio.dev/docs/ikea-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api), [category](https://scavio.dev/docs/ikea-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api), [categories](https://scavio.dev/docs/ikea-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api), [deals](https://scavio.dev/docs/ikea-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api), [suggestions](https://scavio.dev/docs/ikea-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api), [stores](https://scavio.dev/docs/ikea-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api), [stock](https://scavio.dev/docs/ikea-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api), [items](https://scavio.dev/docs/ikea-items?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api), [as-is](https://scavio.dev/docs/ikea-as-is?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api). Overview: [IKEA API](https://scavio.dev/ikea-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api).
