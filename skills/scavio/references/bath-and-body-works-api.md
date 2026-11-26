# Bath & Body Works API - Prices, Promotions, Store Pickup

Read Bath & Body Works (bathandbodyworks.com, the US body care and home fragrance retailer, and bathandbodyworks.ca in English): keyword search and category pages, one product in full, the promotions attached to a product with their start and end times, the current offer cards and Top Offers tiles, whether one store takes a pickup order for a product, one store's public page, the store directory, a product's review summary and the category tree. `country` `us` (default, bathandbodyworks.com, USD) or `ca` (bathandbodyworks.ca in English, CAD) on every endpoint. Every endpoint returns structured JSON at 1 credit per call.

**The job this skill is for: Bath & Body Works prices and promotions.** What a candle, lotion or gift set costs today and which offers apply to it, with the dates the site gives each offer. On 2026-11-26 (Thanksgiving, the eve of Black Friday) the Champagne Toast 3-Wick Candle (`028029548`, 14.5 oz / 411 g) read $24.95 with list price $24.95 and the callout "Mix & Match: Buy 3, Get 4 FREE"; on bathandbodyworks.ca the same candle (`028013573`, `us_product_id` `028029548`) read $26.95 CAD with "Buy 3, get 4 free everything". `/promotions` on the Into the Night Gift Set (`025510502`, $92.95) gave 3 promotions, one "$40 with any $40 purchase | $130.90 value" from 2026-11-26T11:00:00Z to 2026-11-27T11:00:00Z, with its terms as given. `/offers` read 15 offer cards and 2 Top Offers tiles, the first tile "Buy 3 get 4 FREE" on "Entire store", "Free items are the 4 lowest priced items in each set of 7 eligible items.*". Pair it with `ulta-beauty-api`, `target-product-data` and `amazon-product-data` for the same UPC elsewhere.

Eight limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **48 results, no page 2.** Bath & Body Works shows 48 results of a search or category on its page: `count` is at most 48 and `total` is the site's own result count. There is no page 2 (a `page` other than 1 is a `400`); narrow with `sort` or the filters.
- **Prices are national.** The same price at every store. Report "$24.95 at bathandbodyworks.com on 2026-11-26", never a store's price, and never carry a US price to Canada or the reverse.
- **Multi-buy offers are a rule, not a price.** "Buy 3, Get 4 FREE" is applied in the bag; the rule text is in `promotions` and `offers` terms. No per-unit or after-offer price is computed, and none should be claimed. `promotional_price` is the site's own field, set only where the site states one (gift sets with a qualifying-purchase offer; it can equal the list price, the offer itself is in the callout).
- **Store pickup is a purchase limit, not stock.** `/store-availability` returns `store_orderable` (whether the store takes a pickup order for the product) and `pickup_purchase_limit` (the most the store lets you reserve for pickup, 0-24). Bath & Body Works publishes no unit counts; never present the limit as stock or units.
- **No store search by ZIP.** `/stores` lists every store id in the market's directory; `/store` reads one store's address, coordinates and hours. There is no search near a ZIP or a city.
- **Every size is its own product.** There are no variants: each size has its own product id and price. A Canadian product carries `us_product_id`, the matching US id.
- **No history, no full reviews.** `/reviews-summary` gives the rating, review count and up to 4 newest reviews, without reviewer names; full review paging, sorting and star filters are not offered. Nothing is cached or kept: poll and store your own series.

Bath & Body Works does not offer a public API for reading its catalog, prices, promotions or store pickup. Prices, offers and store pickup are shown on bathandbodyworks.com and bathandbodyworks.ca, and this skill reads those public pages with one Scavio key. Its international stores are run by partners on their own sites and are not read.

Bath & Body Works reported 1,927 company-operated stores in the United States and Canada and 573 partner stores in 45+ countries in its 10-K for fiscal 2025. Quote these with their source, never from the samples.

See also: for the same item at Ulta Beauty use `ulta-beauty-api`; at Target `target-product-data`; at Amazon `amazon-product-data`; at Walmart `walmart-product-data`; prices across retailers `google-shopping-api`; another body care and fragrance retailer `sephora-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price a Bath & Body Works candle, body care or home fragrance product, with its list price and the offers attached to it
- Read the start and end times and terms of the promotions on one Bath & Body Works product
- List the current Bath & Body Works offers: the site-wide banner, the menu offers, the home page cards and the Top Offers tiles
- Search bathandbodyworks.com by keyword, sorted by price, top rated or new arrivals, or filtered by fragrance name, fragrance family or product type
- List a Bath & Body Works category or deal page (3-Wick Candles, Top Offers, Black Friday)
- Read one product in full: fragrance notes, description, ingredients, UPC, size, online purchase limit and low-stock flag
- Check whether one Bath & Body Works store takes a pickup order for a product, and its pickup purchase limit
- Read a Bath & Body Works store's address, phone, hours and services, or list every store id in the US or Canada
- Read a product's rating, review count and newest reviews
- Read the same product on bathandbodyworks.ca in CAD with its matching US id

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, the store directory took about 2 seconds, a Canadian search or product about 4, a category about 5, and search, product, store, offers, promotions, reviews summary and store availability 13-32. Promotions and store availability are slower than product (10-40 seconds). Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Markets | Credits |
|---|---|---|---|
| `POST /api/v1/bathandbodyworks/search` | Keyword search: the 48 results the site shows with its total, facets, prices and promotion callouts | us, ca | 1 |
| `POST /api/v1/bathandbodyworks/category` | One category or deal page (`/c/...`, `/g/...`, `/t/...`), sorted and filtered like search | us, ca | 1 |
| `POST /api/v1/bathandbodyworks/categories` | The site's category tree (its navigation menu) | us, ca | 1 |
| `POST /api/v1/bathandbodyworks/product` | One product by id or link: price, list price, promotions, fragrance notes, ingredients, UPC, online purchase limit | us, ca | 1 |
| `POST /api/v1/bathandbodyworks/promotions` | The promotions attached to one product with start and end times (ISO, UTC) and terms as given | us, ca | 1 |
| `POST /api/v1/bathandbodyworks/offers` | The home page's offer cards and the Top Offers tiles | us, ca | 1 |
| `POST /api/v1/bathandbodyworks/store-availability` | Whether one store takes a pickup order for one product, and its pickup purchase limit | us, ca | 1 |
| `POST /api/v1/bathandbodyworks/store` | One store's public page: address, phone, coordinates, hours, services, store types | us, ca | 1 |
| `POST /api/v1/bathandbodyworks/stores` | Every store id in the market's store directory | us, ca | 1 |
| `POST /api/v1/bathandbodyworks/reviews-summary` | A product's rating, review count and up to 4 newest reviews | us, ca | 1 |

`country` is `us` (default, bathandbodyworks.com, USD) or `ca` (bathandbodyworks.ca in English, CAD). Spanish (es-US) and French (fr-CA) are not offered: the site serves the same English product data there. A product or store link sets the market; a `country` that does not match the link is a `400`.

## Prices and promotions

Every product card and product carries:

| Field | Meaning |
|---|---|
| `price` | The current price in the market's currency (`currency` USD or CAD) |
| `list_price` | The list price as the site gives it |
| `promotional_price` | The site's own promotional price field, set only where the site states one; `null` otherwise |
| `promotions` | [{`id`, `callout`, `promotional_price`}]: the offers attached to the product; `callout` is the text shown on it ("Mix & Match: Buy 3, Get 4 FREE"), `null` for a member or bag offer the product qualifies for |
| `badge` | The site's badge as given ("Best Seller", "Trending", "In 37,535 bags") |
| `member_exclusive` | The site's member-exclusive flag |
| `online_orderable`, `in_store_pickup` | Whether the product can be ordered online and picked up in store |

`/promotions` adds, per promotion, `name`, `start_date` and `end_date` (ISO, UTC, as the site gives them) and `terms` as given. `/offers` gives the site-wide offer cards with `placement` (banner, menu or home), `headline`, `validity` (the site's own text), `terms`, `percent_off`, `promo_code` where one is needed and `link_path`.

- **National:** one price per product per market. Report it with the market, the date and the size; never per store.
- **Offers:** quote the callout, the validity text or the start and end times, and the terms as given. A multi-buy offer is a bag rule ("Free items are the 4 lowest priced items in each set of 7 eligible items."); compute no per-unit or after-offer price.
- **Sale prices:** on 2026-11-26 every captured `price` equalled its `list_price` (the Black Friday offer was a buy 3, get 4 rule). Report the two fields as given.
- Report the site's labels and dates only. Never judge a price, an offer or its deadline, and never describe how often an item is on sale.

## Workflow

1. **Find the product.** `/search` with `query` (a product, a fragrance or a collection), or `/category` with a `path` from `/categories` (`/c/all-candles/3-wick-candles`, `/g/top-offers`, `/t/black-friday`). Each product's `id` is the input of product, promotions, store-availability and reviews-summary.
2. **Read it in full.** `/product` with `product_id` (or the product `url`): price, list price, promotions, fragrance notes, ingredients, UPC and `online` {`orderable`, `purchase_limit`, `low_stock`}. Each size is its own id.
3. **Offer dates.** `/promotions` with the same `product_id`: each promotion's start and end time and terms.
4. **Site-wide offers.** `/offers` for the banner, menu and home page offer cards and the Top Offers tiles; read a tile's `link_path` with `/category`.
5. **Store pickup.** `/stores` lists store ids; `/store` gives one store's city, state, address and hours; `/store-availability` with `product_id` and `store_id` says whether that store takes a pickup order and its `pickup_purchase_limit`.
6. **Narrow a list.** `sort` and the filters `fragrance_name`, `fragrance_family` and `product_type` (one value or a list of up to 10, exactly as `facets[].values[].value` gives them). There is no page 2.
7. **Canada.** Send `country` `ca`. A Canadian product's `us_product_id` is its US id: read both and report each in its own currency, never converted.
8. **Watching prices and offers:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at` and market; that stored series is the history.

## Parameters

### Product (`/product`), promotions (`/promotions`), reviews summary (`/reviews-summary`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | A Bath & Body Works product id, 9 digits (`028029548`: `products[].id`). Every size is its own id |
| `url` | string | one of | The product link (bathandbodyworks.com or bathandbodyworks.ca `/p/...-<id>`); the link's site sets `country` |
| `country` | string | `us` | `us` or `ca` |

### Store availability (`/store-availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` or `url` | string | required | As for product |
| `store_id` | string | required | A store id, BBW + 5 digits (`BBW00010`: `stores[].store_id`) |
| `country` | string | `us` | `us` or `ca`; a Canadian store needs `ca` |

### Search (`/search`) and category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | A keyword: a product, a fragrance or a collection, 1-120 chars |
| `path` | string | category: required | A category path from categories (`/c/all-candles/3-wick-candles`, `/g/top-offers`, `/t/black-friday`) or its link, without query parameters |
| `sort` | string | `relevance` | `relevance`, `price_low`, `price_high`, `top_rated`, `new_arrivals` (the site's own sorts) |
| `fragrance_name` | string or array | none | Fragrances as the site names them (`Champagne Toast`); up to 10 |
| `fragrance_family` | string or array | none | Warm & Woodsy, Treats & Sweets, Fruity & Bright, Fresh & Clean, Botanicals & Blooms; up to 10 |
| `product_type` | string or array | none | Product types as the site names them (`3-Wick Candle`, `Body Lotion`); up to 10 |
| `country` | string | `us` | `us` or `ca` |

### Store (`/store`), stores (`/stores`), categories (`/categories`), offers (`/offers`)

`/store` takes `store_id` (required) and `country`. `/stores`, `/categories` and `/offers` take only `country`. `/stores` refuses `zip`, `postal_code`, `location`, `latitude`, `longitude`, `near`, `state` and `city`: the directory lists store ids, and `/store` gives each store's city and state.

## Examples

### The promotions on one product, with their dates

```bash
curl -X POST https://api.scavio.dev/api/v1/bathandbodyworks/promotions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "025510502"}'
```

Captured `data` (2026-11-26; the first promotion's `terms` cut, `notes` dropped):

```json
{
  "country": "us",
  "product_id": "025510502",
  "name": "Into the Night Gift Set",
  "currency": "USD",
  "price": 92.95,
  "count": 3,
  "promotions": [
    {
      "id": "BF_40w40_PWP_Bonus_130.90_tag_clone",
      "name": "$40 with any $40 purchase",
      "callout": "$40 with any $40 purchase | $130.90 value",
      "promotional_price": 92.95,
      "start_date": "2026-11-26T11:00:00.000Z",
      "end_date": "2026-11-27T11:00:00.000Z",
      "terms": "*Online Only! - $40 Select Gift Sets with $40 Purchase + Free Tote valid on November 26, 2026 at 6:00 AM ET to November 27, 2026 at 5:59 AM ET. While supplies last. ..."
    },
    {
      "id": "LOYALTY_XmasBag_1124",
      "name": null,
      "callout": null,
      "promotional_price": null,
      "start_date": "2026-11-24T11:00:00.000Z",
      "end_date": "2026-12-25T11:00:00.000Z",
      "terms": null
    },
    {
      "id": "BF_40w40_PWP_Bonus",
      "name": null,
      "callout": null,
      "promotional_price": null,
      "start_date": "2026-11-25T11:00:00.000Z",
      "end_date": "2026-12-02T11:00:00.000Z",
      "terms": null
    }
  ]
}
```

A promotion without a callout is a member or bag offer the product qualifies for. Here `promotional_price` equals `price`: the offer itself is in the callout and the terms. A product with no promotions answers `count` 0 with the note "No promotions are attached to this product right now."

### Whether one store takes a pickup order

```bash
curl -X POST https://api.scavio.dev/api/v1/bathandbodyworks/store-availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "028029548", "store_id": "BBW00010"}'
```

Captured `data` (2026-11-26; `notes` cut to 2 of 3):

```json
{
  "country": "us",
  "product_id": "028029548",
  "store_id": "BBW00010",
  "store": { "name": "SOUTH PARK MALL", "city": "SAN ANTONIO", "state": "TX" },
  "name": "Champagne Toast 3-Wick Candle",
  "size": "14.5 oz / 411 g",
  "currency": "USD",
  "price": 24.95,
  "store_orderable": true,
  "pickup_purchase_limit": 24,
  "online_orderable": true,
  "online_purchase_limit": 24,
  "low_stock": false,
  "notes": [
    "store_orderable is whether the store takes a pickup order for this product. pickup_purchase_limit is the most the store lets you reserve for pickup (0-24): Bath & Body Works does not label it as stock and publishes no unit counts, so it is not a stock count. low_stock is the site's own flag.",
    "Prices are national: the same price at every store (price)."
  ]
}
```

Report it as "store BBW00010 (South Park Mall, San Antonio, TX) takes pickup orders for this candle, up to 24 per order". An unknown store id is a charged `404` ("Bath & Body Works has no store <store_id> on its US site (a Canadian store needs country ca) (stores[].store_id).").

### Search with a sort and a filter

```bash
curl -X POST https://api.scavio.dev/api/v1/bathandbodyworks/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "candle", "sort": "top_rated", "product_type": "3-Wick Candle"}'
```

Captured `data` (2026-11-26; 1 of 48 products shown, `facets` and `notes` dropped):

```json
{
  "query": "candle",
  "country": "us",
  "currency": "USD",
  "sort": "top_rated",
  "filters": { "fragrance_name": [], "fragrance_family": [], "product_type": ["3-Wick Candle"] },
  "total": 123,
  "count": 48,
  "has_more": true,
  "selected_filters": { "product_type": "3-Wick Candle" },
  "products": [
    {
      "id": "028037702",
      "name": "Vanilla Eggnog 3-Wick Candle",
      "brand": null,
      "product_type": "3-Wick Candle",
      "form": "3-Wick Candle",
      "size": "13.5 oz / 383g",
      "currency": "USD",
      "price": 26.95,
      "list_price": 26.95,
      "promotional_price": null,
      "promotions": [
        { "id": "ALL_b3g4_clone", "callout": "Mix & Match: Buy 3, Get 4 FREE", "promotional_price": null },
        { "id": "LOYALTY_XmasBag_1124", "callout": null, "promotional_price": null },
        { "id": "BF_40w40_PWP_Bonus", "callout": null, "promotional_price": null }
      ],
      "rating": 5,
      "review_count": 4,
      "badge": null,
      "fragrance_name": "Vanilla Eggnog",
      "fragrance_family": "Treats & Sweets",
      "online_orderable": false,
      "in_store_pickup": true,
      "member_exclusive": false,
      "launch_date": "2026-11-06T06:00:00.000Z",
      "url_path": "/p/vanilla-eggnog-3-wick-candle-028037702",
      "us_product_id": null
    }
  ],
  "redirect_path": null
}
```

123 matched and the site showed 48 (`has_more` true): narrow with a fragrance or a different sort rather than asking for page 2. Facets: Fragrance Name (107 values), Fragrance Category (5) and Product Type (5). Where the site sends a search to a page instead of listing results, `redirect_path` names it; read it with `/category`.

### Product, category, categories, offers, store, stores, reviews summary and Canada

- `/product` `{"product_id": "028029548"}`: Champagne Toast 3-Wick Candle, White Barn, 14.5 oz / 411 g, $24.95 (list price $24.95), rating 4.75 from 3,789 reviews, `fragrance_notes` top "Kir royale, vintage Champagne, sparkling tangerine, juicy passionfruit", heart "dark plum, white nectarine, black currant", base "warm woods, sugared musk, vanilla extract", `upc` 667659466474, `collection` CORE, `online` {`orderable` true, `purchase_limit` 24, `low_stock` false}, breadcrumbs Candles > 3-Wick Candles. An unknown id is a charged `404`.
- `/category` `{"path": "/c/all-candles/3-wick-candles"}`: 3-Wick Candles, `total` 123, `count` 48, with the page title and description; Mahogany Teakwood Intense 3-Wick Candle $24.95 (badge "In 37,535 bags", 4.78 from 2,196 reviews) and Fresh Balsam 3-Wick Candle $22.95 ("Trending") first.
- `/categories`: 132 nodes, from Sale (`/g/all-sale`), Top Offers (`/g/top-offers`), New & Now, The Holiday Gift Shop, Body care and Candles (`/g/all-candles`) to Black Friday sale (`/t/black-friday`). A node with `path` null is a menu group (read its children).
- `/offers`: 15 offer cards (3 banner, 11 menu, 1 home), such as the banner "$40 gift set and tote with any $40 purchase" ("Over $110 value.", "Online only, in stores tomorrow") and "Free shipping on $50 orders"; 2 Top Offers tiles: "Buy 3 get 4 FREE" on "Entire store" (`link_path` `/t/black-friday`) and "$40 with any $40 purchase" (`/t/promotion-3`).
- `/store` `{"store_id": "BBW00010"}`: South Park Mall, 2310 Southwest Military Dr, San Antonio, TX 78224, phone (210) 932 - 3848, hours Mon-Wed 10AM-8PM, Thu Closed, Fri 7AM-9PM, Sat 9AM-9PM, Sun 11AM-7PM, `services` In-Store Pickup, `store_types` BBW (BBWO: outlet, WBC: White Barn).
- `/stores` `{"country": "ca"}`: 114 store ids (`BBW06001`, `BBW06004`, ...), each with `url_path`. The US directory has about 1,800.
- `/reviews-summary` `{"product_id": "028029548"}`: rating 4.7, `review_count` 3,796, the 4 newest reviews (title, text, `date_created`, `date_published`, `verified_purchaser`), the newest "Love these Candles!!!" on 2026-11-26. No reviewer names.
- Canada: `/search` `{"query": "candle", "country": "ca"}` read `total` 173, 48 shown, Champagne Toast 3-Wick Candle (`028013573`) $26.95 CAD first ("Best Seller", 4.8 from 1,815 reviews, `us_product_id` `028029548`); `/product` on it read `upc` 667659363414 and `online` `purchase_limit` 24; `/store` `{"store_id": "BBW06001", "country": "ca"}` read Erin Mills Town Centre, 5100 Erin Mills Parkway, Mississauga, ON L5M 4Z5.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def bbw(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/bathandbodyworks/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. 3-wick candles in one fragrance family, lowest price first (1 credit)
hits = bbw("search", {"query": "candle", "product_type": "3-Wick Candle",
                      "fragrance_family": "Fruity & Bright", "sort": "price_low"})["data"]
print(hits["total"], "matched,", hits["count"], "shown")
for p in hits["products"][:5]:
    callouts = [x["callout"] for x in p["promotions"] if x["callout"]]
    print(p["id"], p["name"], p["size"], p["price"], p["list_price"], callouts)

# 2. The promotions on the first one, with their dates (1 credit)
pid = hits["products"][0]["id"]
promos = bbw("promotions", {"product_id": pid})["data"]
for x in promos["promotions"]:
    print(x["callout"], x["start_date"], x["end_date"])

# 3. Does one store take a pickup order for it? (1 credit)
a = bbw("store-availability", {"product_id": pid, "store_id": "BBW00010"})["data"]
print(a["store"], a["store_orderable"], "pickup purchase limit", a["pickup_purchase_limit"])

# Prices and offers can change between calls. Store each answer with fetched_at
# and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `country` and `notes`.

- **card** (search, category) - `id`, `name`, `brand`, `product_type`, `form`, `size`, `currency`, `price`, `list_price`, `promotional_price`, `promotions[]` {`id`, `callout`, `promotional_price`}, `rating`, `review_count`, `badge`, `fragrance_name`, `fragrance_family`, `online_orderable`, `in_store_pickup`, `member_exclusive`, `launch_date`, `image`, `url_path`, `us_product_id` (ca: the matching US id).
- **lists** - `currency`, `sort`, `filters`, `total`, `count` (at most 48), `has_more`, `selected_filters`, `products[]`, `facets[]` {`filter`, `label`, `values[]` {`value`, `count`}}. Search adds `query` and `redirect_path`; category `path` and `category` {`id`, `name`, `page_title`, `description`, `breadcrumbs`}.
- **categories** - `count`, `categories[]` {`id`, `name`, `path` (null for a menu group), `children`}.
- **product** - the card fields plus `fragrance_classification`, `fragrance_description`, `fragrance_notes` {`top`, `heart`, `base`}, `description`, `short_description`, `highlights`, `ingredients`, `upc`, `collection`, `online` {`orderable`, `purchase_limit`, `low_stock`}, `images`, `breadcrumbs[]` {`id`, `name`, `path`}.
- **promotions** - `product_id`, `name`, `currency`, `price`, `count`, `promotions[]` {`id`, `name`, `callout`, `promotional_price`, `start_date`, `end_date`, `terms`}.
- **offers** - `currency`, `count`, `promotions[]` {`id`, `placement`, `title`, `headline`, `form_headline`, `details`, `urgency`, `romance_copy`, `percent_off`, `percent_off_copy`, `price_point` {`dollars`, `cents`}, `promo_code`, `promo_code_instructions`, `validity`, `terms`, `link_path`, `published_at`}, `top_offers_count`, `top_offers[]` {`id`, `label`, `offer`, `applies_to`, `detail`, `urgency`, `link_path`}.
- **store-availability** - `product_id`, `store_id`, `store` {`name`, `city`, `state`}, `name`, `size`, `currency`, `price`, `store_orderable`, `pickup_purchase_limit`, `online_orderable`, `online_purchase_limit`, `low_stock`.
- **store** - `store_id`, `name`, `address` {`line1`, `city`, `state`, `postal_code`, `country`}, `phone`, `latitude`, `longitude`, `hours[]` {`day`, `hours`}, `services`, `store_types`, `url_path`, `nearby_stores`.
- **stores** - `count`, `stores[]` {`store_id`, `url_path`}.
- **reviews-summary** - `product_id`, `rating`, `review_count`, `best_rating`, `count`, `reviews[]` {`id`, `rating`, `title`, `text`, `date_created`, `date_published`, `verified_purchaser`}.

## Guardrails

- Name it "Bath & Body Works (bathandbodyworks.com, the US body care and home fragrance retailer)" on first mention, and "bathandbodyworks.ca" for Canada.
- Prices: quote `price` and `list_price` with the size, the site and the `fetched_at` date. Prices are national: never call a price a store's price. Report each market in its own currency; never convert or call one cheaper.
- Offers: quote the callout, the validity text, the start and end times and the terms as given. Compute no per-unit, per-item or after-offer price for a multi-buy offer, and never judge an offer or its deadline.
- Store pickup: report `store_orderable` and `pickup_purchase_limit` as a purchase limit for pickup. Never call it stock, inventory or units, and never infer how many a store holds. Never promise pickup.
- Reviews: no reviewer names are returned; quote the rating, count and review text with their dates.
- Comparing Bath & Body Works with Ulta, Target or Amazon: compare only the same item (same UPC), each with its date and market. Never call one retailer cheaper beyond the numbers shown.
- Not available: stock or unit counts, store search by ZIP or city, page 2 of a list, search suggestions, full review paging, sort or star filters, Spanish or French pages, partner-run international stores, member prices, price history (poll and store), checkout, cart or ordering. This API cannot reserve, add to bag or buy.
- Terms: Scavio does not collect or store Bath & Body Works data: each call fetches the public Bath & Body Works page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Bath & Body Works' terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Bath & Body Works product photos or logos; link products by their page instead.
- Never fabricate prices, offers, dates, product ids, store ids, hours, limits or ratings. Only return what the API returned, with the `fetched_at` time and the market.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id (or url) is required.", a `product_id` that is not 9 digits, "url must be a Bath & Body Works product link such as ...", "product_id does not match the link's product id.", "store_id is required (BBW + 5 digits, e.g. BBW00010: stores[].store_id).", a `country` other than `us` or `ca` ("Bath & Body Works' international stores are run by partners on their own sites."), Spanish or French ("Spanish (es-US) is not offered ...", "French (fr-CA) is not offered ..."), a `country` that does not match the link, "query is required (a keyword such as candle, body lotion or a fragrance name).", a `page` other than 1 ("Bath & Body Works shows 48 results of a search on its page; there is no page 2. Narrow with sort or filters."), a category `path` with query parameters or not a Bath & Body Works category path, an unknown `sort`, more than 10 values in a filter, and a ZIP, location, city or state on `/stores` ("Bath & Body Works has no store search by ZIP or location on its pages ...").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Bath & Body Works has no product <id> on its US site (a Canadian product id needs country ca).", "Bath & Body Works has no store <id> on its US site (a Canadian store needs country ca) (stores[].store_id).", "Bath & Body Works has no category page at <path> (categories[].path).". Take product ids, store ids and paths from a previous answer rather than guessing them. A search with no results is an answer with `count` 0; a product without reviews answers `rating` null and no reviews.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api).
- `502` means Bath & Body Works data was temporarily unavailable ("Bath & Body Works is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the site is busy ("Bath & Body Works is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.99.0
npm install scavio@0.100.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.bathandbodyworks.search({ query: "candle", sort: "top_rated", product_type: "3-Wick Candle" });
const { data: cat } = await scavio.bathandbodyworks.category({ path: "/c/all-candles/3-wick-candles" });
const { data: tree } = await scavio.bathandbodyworks.categories();
const { data: product } = await scavio.bathandbodyworks.product({ product_id: "028029548" });
const { data: promos } = await scavio.bathandbodyworks.promotions({ product_id: "025510502" });
const { data: offers } = await scavio.bathandbodyworks.offers();
const { data: pickup } = await scavio.bathandbodyworks.storeAvailability({ product_id: "028029548", store_id: "BBW00010" });
const { data: store } = await scavio.bathandbodyworks.store({ store_id: "BBW00010" });
const { data: stores } = await scavio.bathandbodyworks.stores({ country: "ca" });
const { data: reviews } = await scavio.bathandbodyworks.reviewsSummary({ product_id: "028029548" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.bathandbodyworks.search(...)`, `category`, `categories`, `product`, `promotions`, `offers`, `store_availability`, `store`, `stores` and `reviews_summary`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 10 endpoints as tools: `search_bathandbodyworks`, `get_bathandbodyworks_category`, `get_bathandbodyworks_categories`, `get_bathandbodyworks_product`, `get_bathandbodyworks_promotions`, `get_bathandbodyworks_offers`, `get_bathandbodyworks_store_availability`, `get_bathandbodyworks_store`, `get_bathandbodyworks_stores` and `get_bathandbodyworks_reviews_summary`. Bath & Body Works is opt-in: add `bathandbodyworks` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.99.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,bathandbodyworks"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/bathandbodyworks-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api), [category](https://scavio.dev/docs/bathandbodyworks-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api), [categories](https://scavio.dev/docs/bathandbodyworks-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api), [product](https://scavio.dev/docs/bathandbodyworks-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api), [promotions](https://scavio.dev/docs/bathandbodyworks-promotions?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api), [offers](https://scavio.dev/docs/bathandbodyworks-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api), [store availability](https://scavio.dev/docs/bathandbodyworks-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api), [store](https://scavio.dev/docs/bathandbodyworks-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api), [stores](https://scavio.dev/docs/bathandbodyworks-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api), [reviews summary](https://scavio.dev/docs/bathandbodyworks-reviews-summary?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api). Overview: [Bath & Body Works API](https://scavio.dev/bathandbodyworks-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=bath-and-body-works-api).
