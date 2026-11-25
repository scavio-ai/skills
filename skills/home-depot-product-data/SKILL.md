---
name: home-depot-product-data
description: "Home Depot product data for homedepot.com and Home Depot Canada (homedepot.ca, The Home Depot's Canadian store: 182 stores in 10 provinces): keyword search with price, promotions, brand, model, ratings and per-store pickup and delivery; full item detail with spec table, dimensions, documents and return policy; paginated review bodies with rating distribution; stores near a ZIP or postal code; and one item's price and stock at a store. Home Depot Canada adds per-store prices in CAD with exact units and aisle / bay at each store, the store price next to the online price, exact units at every store near a postal code or city, category and collection pages (Black Friday, Christmas Trees) priced at a chosen store, the department tree, store hours and search suggestions, in English or French. 11 endpoints: US 2 credits per call (delivery quote 4), Canada 1 credit per call, structured JSON. Canada has no UPC, structured sale end dates, delivery quotes or reviews past the first 8 per language."
version: 1.1.0
tags: home-depot, home-depot-api, home-depot-product-data, home-depot-canada, homedepot-ca, home-depot-canada-prices, home-depot-store-prices, home-depot-store-stock, product-data, product-search, retail, home-improvement, hardware, lumber-prices, canada, cad, store-prices, store-stock, pricing, product-reviews, price-monitoring, catalog-enrichment, web-scraping, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F528"
    homepage: https://scavio.dev/docs/home-depot-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=home-depot-product-data
---

# Home Depot Product Data API - US and Canada Store Prices, Stock, Reviews

Search Home Depot by keyword, read one item in full, page through its reviews, find stores and read an item's price and stock at a store. Two markets on the same endpoints, chosen with `country`:

- `country: "us"` (the default) - homedepot.com, in USD.
- `country: "ca"` - Home Depot Canada (homedepot.ca, The Home Depot's Canadian store: 182 stores in 10 provinces), in CAD, in English or French. Canada adds five endpoints of its own: category, categories, stock, store and suggestions.

All endpoints return structured JSON. Home Depot Canada has no public developer API; Scavio fetches the public homedepot.ca page data on request.

## When to trigger

Use this skill when the user asks to:
- Find products on homedepot.com or homedepot.ca by keyword, price band or rating
- Look up a Home Depot item by item id or by a pasted `homedepot.com/p/...` or `homedepot.ca/product/...` link
- Pull the spec table, dimensions, documents or return policy for an item
- Read customer reviews for an item, with the rating distribution and per-attribute ratings
- Compare one item's price and exact units at Home Depot Canada stores in different provinces, or the store price against the online price
- Check which Home Depot Canada stores near a postal code or city have an item, and how many units each has
- Browse a Home Depot Canada category or collection (Black Friday, Christmas Trees) priced at a chosen store
- Monitor hardware, lumber or home-improvement pricing and promotions in the US or Canada
- Enrich a product catalog with brand, model number, UPC (US only) and category path

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=home-depot-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=home-depot-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. The table below gives the cost of each endpoint per country.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off (Hobby is $15 a
month for 3,000 credits; Growth works out to $1 per 1,000 credits).

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. The cost depends on `country`: **US 2 credits** per call (shipping 4), **Canada 1 credit** per call on every endpoint.

| Endpoint | US credits | Canada credits | What it returns |
|---|---|---|---|
| `POST /api/v1/homedepot/search` | 2 | 1 | Keyword results with price, promotions, brand, model, ratings, badges; for Canada, the price, exact units and aisle / bay at one store |
| `POST /api/v1/homedepot/product` | 2 | 1 | One item in full: pricing, images, spec table, dimensions, documents; for Canada with `store_id`, that store's price next to the online price |
| `POST /api/v1/homedepot/reviews` | 2 | 1 | US: one page of 30 full review bodies. Canada: the first 8 reviews per language and the first page of questions |
| `POST /api/v1/homedepot/stores` | 2 | 1 | Stores near a ZIP, city or address (US) or a postal code, city or latitude / longitude (Canada), with hours |
| `POST /api/v1/homedepot/availability` | 2 | 1 | One item at one store: the store's price, promotions and stock. US also quotes delivery to a ZIP |
| `POST /api/v1/homedepot/shipping` | 4 | not available (400, not charged) | US: every delivery option to a ZIP for a quantity |
| `POST /api/v1/homedepot/category` | -- | 1 | Canada only: one category or collection page, with the search parameters |
| `POST /api/v1/homedepot/categories` | -- | 1 | Canada only: the department tree and the current event pages |
| `POST /api/v1/homedepot/stock` | -- | 1 | Canada only: exact units of one item at every store near a postal code or city (no prices) |
| `POST /api/v1/homedepot/store` | -- | 1 | Canada only: one store with 7 dated days of hours and its nearby stores |
| `POST /api/v1/homedepot/suggestions` | -- | 1 | Canada only: the search box keyword suggestions |

The five Canada-only endpoints default to `country: "ca"` and accept no other value.

## Workflow (US)

1. **Find items:** call `/homedepot/search` with `query`. Read `products[].item_id`.
2. **Item detail:** call `/homedepot/product` with that `item_id` (a full `homedepot.com/p/...` URL works too; tracking parameters are discarded).
3. **Reviews:** call `/homedepot/reviews` with the same `item_id`. `/product` carries only a **10-review preview** — `/reviews` is the paginated surface.
4. **Stores:** `/homedepot/stores` with a ZIP, city or address returns store numbers; pass one as `store_id` to `/homedepot/availability` (pickup stock and the store's price) and `/homedepot/shipping`.

### Pagination (US)

- **Search** is fixed at **12 products per page**. There is no page-size parameter and no way to raise it, so paging is the only way to read further. Ten pages is 20 credits — decide the budget before looping.
- **Reviews** are **30 per page**. The response carries `total_pages`; that is the last page that exists, and asking past it is a **404**. Stop at `total_pages`.
- **Product** takes no paging parameter.

## Parameters (US)

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keyword (1-500 chars) |
| `page` | integer | -- | 1-based. 12 products per page, fixed |
| `sort_by` | string | `best_match` | `best_match`, `top_sellers`, `top_rated`, `price_low`, `price_high` |
| `min_price` | number | -- | Minimum price, inclusive (0 or greater) |
| `max_price` | number | -- | Maximum price, inclusive (0 or greater) |
| `country` | string | `us` | `us` or `ca` (see the Canada section) |

`sort_by` is a **closed set**. Home Depot does not fall back on an unknown sort — it answers `200` with an empty page that is still billed. A "newest" sort is deliberately absent: it works on category pages and is rejected on keyword search.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string | required | Item id, or a full `homedepot.com/p/...` URL |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string | required | Item id, or a full `homedepot.com/p/...` URL |
| `page` | integer | -- | 1-based. 30 per page; past `total_pages` is a 404 |

### Stores, availability and shipping

| Endpoint | Parameters |
|---|---|
| `/stores` | `query` (required: a ZIP code, city or address), `limit` (1-20, default 20, nearest first) |
| `/availability` | `item_id` (required), `store_id` (pickup stock and the store's price), `zip` (5-digit ZIP to quote delivery to). Pass `store_id`, `zip`, or both; they need not be near each other |
| `/shipping` | `item_id` (required), `zip` (required), `quantity` (1-999, default 1), `store_id` |

## Home Depot Canada (`country: "ca"`)

Send `country: "ca"` on search, product, reviews, stores and availability, or call one of the five Canada-only endpoints. Every Canada call costs **1 credit**. Prices are in Canadian dollars (CAD), as Home Depot Canada gives them. `language` is `en` (default) or `fr`: ids and CAD prices are the same, names, links and facets come back in that language. Item ids are 10 digits (e.g. `1001769719`); a `homedepot.ca/product/...` link works too. Store numbers are 4 digits (e.g. `7080`), from `/stores` with `country: "ca"`.

### Prices are per store

- **Prices can differ by store.** Lumber does: the same 2x4 was 9.25 in a Quebec store and 9.18 in an Ontario store on Nov 25, 2026. The tools, the tree and the fridge sampled that day had one price everywhere. To compare stores, call `/availability` (or `/product` with `store_id`) once per store.
- **Units are exact counts per store** (`store_units`), next to `online_units`, with the `aisle` and `bay` in that store.
- **The store price can differ from the online price.** `/product` without `store_id` returns the online price (`price_source: "online"`); with `store_id`, `price` is that store's price (`price_source: "store"`) and `online_price` stays the online price. A tree was 78.98 online and 69.98 at a store.
- **Search and category price at one store.** Pass `store_id`; without it Home Depot Canada prices at its default store (7274). `data.store` says which store was used, and each product row carries `price_store_id`.

### Canada parameters

| Endpoint | Parameters |
|---|---|
| `/search` | `query` (or `category_id`, or `deals` alone), `store_id`, `page` (1-500), `page_size` (1-40, default 40), `sort_by` (`best_match`, `price_low`, `price_high`, `top_rated`), `min_price`, `max_price` (CAD), `filters` (up to 10 `{facet, value}` from `facets`), `deals` (`special_buy`, `new_lower_price`, `savings`; one or a list: the site's Special Offers filter), `include_facets`, `language` |
| `/category` | `category_id` (required: `departments[].id` or `events[].id` from `/categories`, e.g. `l4-drill-drivers`, `661103` for Christmas Trees), optional `query`, and every search parameter above |
| `/categories` | `depth` (1-4, default 4: the whole tree, about 1,750 nodes), `language` |
| `/product` | `item_id` (required), `store_id`, `language` |
| `/reviews` | `item_id` (required), `language` (`en` and `fr` are different review sets). No `page` past 1 |
| `/stores` | `query` (a postal code or city) or `latitude` + `longitude`, `limit` (1-50, default 10), `page`, `language` |
| `/availability` | `item_id` (required), `store_id` (required), `language`. No `zip` |
| `/stock` | `item_id` (required), `location` (required: a Canadian postal code or city, e.g. `M5V 2T6`), `limit` (1-50, default 20), `page`, `language` |
| `/store` | `store_id` (required), `language` |
| `/suggestions` | `query` (required: what has been typed so far), `store_id`, `language` |

### Canada workflow

1. **Pick stores:** `/stores` with `country: "ca"` and a postal code or city. Read `stores[].store_id`.
2. **Find items:** `/search` with `country: "ca"`, `query` and `store_id`, or `/categories` then `/category` with a `category_id`. Read `products[].item_id`, `price`, `store_units`.
3. **Store vs online:** `/product` with `country: "ca"`, `item_id` and `store_id` gives both `price` (the store's) and `online_price`.
4. **Same item, other stores:** `/stock` with a postal code or city gives the exact units at every nearby store in one call (no prices). For each store's price, call `/availability` with that `store_id`.

### Canada traps

- **Store gap.** Home Depot Canada's store record for an item is sometimes missing while the item exists. Then `/availability` and `/stock` answer a **502 that is not charged**, and `/product` with `store_id` returns the item at its **online price** with `store_price_returned: false` and a `notes` entry. Read the item with `/product` (without `store_id`), try `/stock` with a location near the store, or retry later. Never present the online price as the store's price.
- **Reviews are partial.** `/reviews` returns the first 8 reviews per language and the first page of questions, with no reviewer names. `page` above 1 is a `400`. Ask for `language: "fr"` for the French set.
- **No UPC.** Home Depot Canada shows no UPC / GTIN, so there is none to return. Match items across retailers by brand and model number.
- **No sale end dates.** A sale is a `price_badge` (New Lower Price, Special Buy) plus Home Depot Canada's `promotion_text`; there is no structured end date.
- **`sort_by: "top_sellers"` is a 400 for Canada.** Use `best_match`, `price_low`, `price_high` or `top_rated`.
- **`/shipping` with `country: "ca"` is a 400**, not charged, and `zip` on `/availability` is a 400: Home Depot Canada delivery quotes are not available.
- **Not-found is charged.** An unknown item, store or category is a charged `404`. A refused input (400) and an upstream failure (502) are not charged.
- Not available for Canada: UPC / barcodes, structured sale end dates, reviews past the first 8 per language, delivery quotes, the flyer, cart / checkout, price history (poll and store it yourself).

### Pairs well with

For Canadian home improvement prices across retailers: `canadian-tire-api` (Canadian Tire store prices and stock), `walmart-product-data` with `domain: "ca"` (Walmart.ca) and `amazon-product-data` with `country: "ca"` (Amazon.ca). Each reads the retailer's own site.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. US search, lowest price first, under $300
found = requests.post(f"{BASE}/api/v1/homedepot/search", headers=HEADERS,
    json={"query": "cordless drill", "sort_by": "price_low", "max_price": 300}).json()

item_id = found["data"]["products"][0]["item_id"]

# 2. Full item detail (a pasted product URL works just as well)
item = requests.post(f"{BASE}/api/v1/homedepot/product", headers=HEADERS,
    json={"item_id": item_id}).json()

# 3. Reviews, page 2 onward - stop at total_pages, never guess past it
reviews = requests.post(f"{BASE}/api/v1/homedepot/reviews", headers=HEADERS,
    json={"item_id": item_id, "page": 2}).json()

print(reviews["data"]["total_pages"], reviews["data"]["count"])
```

Paging US search, capped so it cannot run away with the user's credits:

```python
def search_pages(query, max_pages=3, **filters):
    """12 products per page, 2 credits per page."""
    out = []
    for page in range(1, max_pages + 1):
        data = requests.post(f"{BASE}/api/v1/homedepot/search", headers=HEADERS,
                             json={"query": query, "page": page, **filters}).json()["data"]
        out += data["products"]
        if data["count"] < data["page_size"]:
            break
    return out
```

Home Depot Canada: one item's store price next to its online price, then units at every store near a postal code (1 credit per call):

```python
def hdca(path, **body):
    r = requests.post(f"{BASE}/api/v1/homedepot/{path}", headers=HEADERS,
                      json={"country": "ca", **body}, timeout=120)
    return r.status_code, r.json()

status, item = hdca("product", item_id="1000112108", store_id="7128")
d = item["data"]
if d.get("store_price_returned") is False:
    print("store price not returned; online price:", d["price"])
else:
    print(d["store"]["name"], d["price"], "store vs", d["online_price"], "online",
          d["store_units"], "units, aisle", d["aisle"], "bay", d["bay"])

status, stock = hdca("stock", item_id="1001769719", location="H3B 1A1")
if status == 502:
    print("store gap, not charged - retry later")  # store record missing for this item
else:
    for s in stock["data"]["stores"]:
        print(s["store_id"], s["name"], s["address"]["province"], s["units"])

# A category priced at one store, lowest price first
status, trees = hdca("category", category_id="661103", store_id="7128", sort_by="price_low")
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **search (US)** — `query`, `url`, `canonical_url`, `page`, `page_size` (12), `start_index`, `total_results`, `sort`, `sort_order`, `did_you_mean`, `corrected_query`, `category_path`, `count`, `products[]`.
  A product row: `pos`, `item_id`, `parent_id`, `store_sku`, `model_number`, `brand`, `title`, `url`, `product_type`, `image`, `images`, `price`, `original_price`, `currency`, `unit_of_measure`, `discount_amount`, `discount_percent`, `promotion_type`, `promotion_text`, `clearance_price`, `price_hidden`, `rating`, `review_count`, `badges`, `sponsored`, `category_path`, `department`, `returnable`, `quantity_limit`, `availability`, `buyable`, `in_stock`, `stock_quantity`, `pickup`, `delivery`, `key_features`.
- **product (US)** — `item_id`, `parent_id`, `store_sku`, `oms_sku`, `model_number`, `upc`, `gtin13`, `title`, `url`, `brand`, `product_type`, `description`, `price`, `original_price`, `currency`, `unit_of_measure`, `promotion_*`, `clearance_price`, `price_valid_until`, `availability`, `buyable`, `discontinued`, `rating`, `review_count`, `image`, `images[]`, `videos[]`, `badges[]`, `highlights[]`, `bullets[]`, `specifications[]` (`group`, `name`, `value`), `key_features[]`, `depth`, `height`, `width`, `weight`, `category_path[]`, `returnable`, `return_days`, `quantity_limit`, `prop65_warning`, `prop65_message`.
- **reviews (US)** — `item_id`, `product_name`, `url`, `rating`, `total_results`, `recommended_count`, `not_recommended_count`, `total_pages`, `rating_distribution[]`, `page`, `page_size` (30), `count`, `reviews[]` (`id`, `rating`, `title`, `text`, `author`, `location`, `submitted_at`, `verified_purchase`, `recommended`, `helpful_votes`, `unhelpful_votes`, `syndicated`, `pros`, `cons`, `secondary_ratings`, `photos`, `videos`, `responses`).

```json
{
  "data": {
    "query": "cordless drill",
    "page": 1,
    "page_size": 12,
    "total_results": 2148,
    "count": 12,
    "products": [
      {
        "pos": 1,
        "item_id": "325479354",
        "brand": "DEWALT",
        "title": "20V MAX Cordless Drill/Driver Kit",
        "price": 179,
        "currency": "USD",
        "rating": 4.7,
        "review_count": 8230,
        "url": "https://www.homedepot.com/p/325479354"
      }
    ]
  },
  "credits_used": 2,
  "credits_remaining": 998
}
```

Home Depot Canada (every response also carries `market {country, currency, language}` and `retrieved_at`):

- **search / category (CA)** — `query`, `category_id`, `store {store_id, requested}`, `language`, `page`, `page_size`, `total_results`, `total_pages`, `has_more`, `sort`, `filters_applied`, `deals`, `min_price`, `max_price`, `category_path`, `heading`, `count`, `products[]`, `facets` (with `include_facets`).
  A product row: `pos`, `item_id`, `product_type`, `model_number`, `title`, `brand`, `url`, `image`, `price`, `original_price`, `savings_amount`, `savings_percent`, `currency`, `unit_of_measure`, `price_badge {code, label}`, `price_store_id`, `rating`, `review_count`, `store_units`, `store_stock_status`, `online_units`, `online_stock_status`, `aisle`, `bay`, `badges`, `promotion_text`, `has_more_options`, `is_appliance`.
- **product (CA)** — `item_id`, `title`, `brand`, `model_number`, `url`, `urls {en, fr}`, `price`, `price_source` (`store` | `online`), `online_price`, `original_price`, `savings_amount`, `savings_percent`, `currency`, `unit_of_measure`, `price_badge`, `store {store_id, name, province}`, `store_units`, `store_stock_status`, `online_units`, `online_stock_status`, `aisle`, `bay`, `promotion_text`, `badges`, `fulfillment`, `delivery_time`, `rating`, `review_count`, `question_count`, `description`, `features`, `specifications`, `images`, `documents`, `categories`, `variants`, `dimensions`, `warranty`, `is_appliance`; on a store gap also `store_price_returned: false` and `notes`.
- **reviews (CA)** — `item_id`, `title`, `url`, `language`, `rating`, `review_count`, `question_count`, `count`, `reviews[]` (`review_id`, `rating`, `best_rating`, `title`, `text`, `date`), `questions[]` (`question_id`, `question`, `details`, `answer_count`, `answers[]`), `note`.
- **stores (CA)** — `query`, `location_text`, `page`, `page_size`, `total_results`, `total_pages`, `has_more`, `count`, `stores[]` (`store_id`, `name`, `address {line1, city, province, postal_code, country, formatted}`, `phone`, `latitude`, `longitude`, `distance_km`, `time_zone`, `services`, `hours[]` with 7 dated days).
- **availability (CA)** — `item_id`, `store {store_id, name, province}`, `price` (the store's), `original_price`, `savings_amount`, `savings_percent`, `currency`, `unit_of_measure`, `price_badge`, `store_units`, `store_stock_status`, `online_units`, `online_stock_status`, `aisle`, `bay`, `promotion_text`, `badges`, `fulfillment`.
- **stock** — `item_id`, `title`, `brand`, `url`, `location`, `location_text`, `online_units`, `online_stock_status`, `page`, `page_size`, `total_results`, `total_pages`, `has_more`, `count`, `stores[]` (`store_id`, `name`, `address`, `phone`, `latitude`, `longitude`, `distance_km`, `time_zone`, `services`, `units`, `stock_status`).
- **store** — `store_id`, `name`, `address`, `phone`, `latitude`, `longitude`, `time_zone`, `services`, `hours[]` (`day`, `date`, `closed`, `open`, `close`), `nearby_stores[]`.
- **categories** — `language`, `depth`, `count`, `total`, `departments[]` (`id`, `name`, `url`, `level`, `children`; a node without an `id` is a content page), `events[]` (e.g. Black Friday), `note`.
- **suggestions** — `query`, `language`, `count`, `suggestions[]` (keywords), `home_services[]` (`id`, `name`).

Product with a store (`country: "ca"`, `item_id: "1000112108"`, `store_id: "7128"`), captured Nov 25, 2026, trimmed:

```json
{
  "data": {
    "item_id": "1000112108",
    "title": "2-inch x 4-inch x 8-ft SPF Premium Stud Lumber",
    "url": "https://www.homedepot.ca/product/1000112108",
    "price": 4.14,
    "price_source": "store",
    "online_price": 6.58,
    "currency": "CAD",
    "unit_of_measure": "each",
    "store": { "store_id": "7128", "name": "ST-HENRI", "province": "QC" },
    "store_units": 2858,
    "store_stock_status": "inStock",
    "online_units": 0,
    "online_stock_status": "outOfStock",
    "aisle": "19",
    "bay": "001",
    "promotion_text": "Buy 100 or more, Save 10%"
  },
  "credits_used": 1
}
```

Stock near a postal code (`item_id: "1001769719"`, `location: "H3B 1A1"`), captured Nov 25, 2026, trimmed to the first two of 15 stores:

```json
{
  "data": {
    "item_id": "1001769719",
    "brand": "DEWALT",
    "location": "H3B 1A1",
    "online_units": 16,
    "total_results": 15,
    "count": 15,
    "stores": [
      { "store_id": "7128", "name": "ST-HENRI", "distance_km": 4, "units": 16, "stock_status": "inStock" },
      { "store_id": "7149", "name": "BEAUBIEN OUEST", "distance_km": 4.3, "units": 18, "stock_status": "inStock" }
    ]
  },
  "credits_used": 1
}
```

## Guardrails

- Quote the cost before looping: US calls are **2 credits** (shipping 4), Canada calls are **1 credit**, including one that comes back empty. US search paging is 2 credits per 12 products; Canada search is 1 credit per up to 40.
- Never invent a `sort_by` value. An unrecognised US sort returns an empty page and is still billed; `top_sellers` is a 400 for Canada.
- Do not send a page size to US search — there is none. US search is 12 per page and US reviews are 30 per page, both fixed upstream. Canada search and category take `page_size` 1-40.
- Do not ask for a US review page past `total_pages`; it is a billed 404, not an empty list. Canada reviews have no page 2.
- `/product` (US) gives a 10-review preview only. If the user wants review analysis, call `/reviews` — do not present the preview as the full set. For Canada, say that the reviews are the first 8 per language.
- Report Canada prices as Home Depot Canada gives them, with the store they belong to and whether `price_source` is `store` or `online`. Do not label a store or a price as the lowest across Canada from a sample of stores, and repeat badges (New Lower Price, Special Buy) as given.
- Never fabricate item ids, prices, model numbers, UPCs, availability or review text. Only return what the API returned.
- Always surface the product `url` so the user can verify.

## Failure handling

- `400` means an invalid or missing parameter (no `query`, a `sort_by` outside the enum, `top_sellers` / review `page` > 1 / `zip` / `/shipping` for Canada) — fix and do not retry as-is. Not charged.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` on `/product` or `/reviews` means the item id does not exist, or the review page is past the last one; for Canada also an unknown store or category. Charged — do not retry the same id or page.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=home-depot-product-data).
- `502` / `503` mean upstream is temporarily unavailable — wait a few seconds and retry, up to a few times. For Canada `/availability` and `/stock`, a 502 that names the store side is the store gap above: not charged; read `/product` without `store_id` or retry later.
- If search returns nothing, relax the price filters or try broader keywords.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.91.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.home_depot.search("cordless drill", sort_by="top_rated", max_price=300)
item = client.home_depot.product(found["data"]["products"][0]["item_id"])
reviews = client.home_depot.reviews(item["data"]["item_id"], page=2)

# Home Depot Canada: the same methods with country="ca"
ca = client.home_depot.search("cordless drill", country="ca", store_id="7080")
```

```bash
npm install scavio@0.92.0
```

```javascript
import { Scavio } from "scavio";

const client = new Scavio(); // reads SCAVIO_API_KEY
const found = await client.homeDepot.search({ query: "cordless drill", sort_by: "top_rated" });
const ca = await client.homeDepot.search({ query: "cordless drill", country: "ca", store_id: "7080" });
```
