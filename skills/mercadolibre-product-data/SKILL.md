---
name: mercadolibre-product-data
description: "Mercado Libre product data API for Mexico, Brazil (Mercado Livre), Argentina and Colombia: search listings by keyword or seller with price, discount, installments, brand, rating, review count, free shipping, Full and sponsored flags, pull one product with the buy-box seller, reputation, variations and star distribution, page reviews and buyer questions with seller answers, and get the top 20 best sellers in a category. 5 endpoints, 2 credits each, reviews 1."
version: 1.0.0
tags: mercado-libre, mercadolibre, mercado-livre, mercadolivre, mercado-libre-api, mercadolibre-api, mercado-livre-api, latam-ecommerce, mexico, brazil, argentina, colombia, product-data, product-search, price-monitoring, competitor-prices, seller-catalog, product-reviews, best-sellers, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/mercadolibre-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data
---

# Mercado Libre Product Data API - Search, Products, Reviews, Questions, Best Sellers

Search Mercado Libre listings in Mexico, Argentina and Colombia, and Mercado Livre in Brazil, by keyword or seller, read one product in full, page its reviews and buyer questions, and pull the ranked best sellers in a category. It works as a Mercado Libre scraper API: every endpoint returns structured JSON with the price in the country's currency, with no HTML parsing on your side.

## When to trigger

Use this skill when the user asks to:
- Search Mercado Libre or Mercado Livre for a product and compare prices, discounts, installments and shipping across listings
- Monitor a product's price, list price and discount over time, or watch for listings that drop below a price
- List a seller's catalogue by seller id or public nickname, optionally filtered by condition, price or discount
- Look up one product or listing by URL, catalog product id or item id: price, buy-box seller and reputation, stock, variations, specs, star distribution
- Read product reviews, filtered by star rating, or the buyer questions on a listing with the seller's answers
- Find the best-selling products in a Mercado Libre category in Mexico, Argentina or Colombia
- Research LATAM e-commerce demand, competitor pricing or catalogue gaps on Mercado Libre

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Reviews cost 1 credit per call; the other four endpoints cost 2.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Countries: Mexico (`mx`), Brazil (`br`, Mercado Livre), Argentina (`ar`) and Colombia (`co`). Prices come back in MXN, BRL, ARS or COP.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/mercadolibre/search` | 2 per page | About 48 listings per page by keyword, seller id or seller nickname: price, original price, discount, installments, seller and official-store flag where shown, brand, rating, review count, units sold as a lower bound, free shipping and Full flags, sponsored flag, item, product and category ids, plus the filters Mercado Libre applied on its own |
| `POST /api/v1/mercadolibre/product` | 2 | One catalog product or listing: price and original price, installments, promotions, the buy-box seller with reputation level and seller tier, stock, shipping, rating with its star distribution, variations with sibling product ids, specs, description, pictures, categories |
| `POST /api/v1/mercadolibre/reviews` | 1 per page | 15 reviews per page with rating, text, the original text when Mercado Libre translated it, date, likes, the review's country and photos; optional star filter |
| `POST /api/v1/mercadolibre/questions` | 2 per page | Buyer questions on a listing with the seller's answers and answer dates; page with `next_offset` |
| `POST /api/v1/mercadolibre/best-sellers` | 2 | The ranked top 20 best sellers in a category, with price, discount, installments, rating and units sold. Mexico, Argentina and Colombia only |

## Workflow

1. **Search:** call `/mercadolibre/search` with `country` and `query`. Each row carries `item_id` (the listing), `product_id` (the catalog product, when the listing has one), `url` and `category_id`.
2. **Product:** call `/mercadolibre/product` with a `product_id` or `item_id` from step 1, or a pasted `url`. The response carries the buy-box `item_id`, `seller.seller_id` and `category_id`.
3. **Reviews:** call `/mercadolibre/reviews` with the same `product_id`, `item_id` or `url`; add `rating` for one star level.
4. **Questions:** call `/mercadolibre/questions` with an `item_id` (from search or from product) or a listing URL. A product URL works too: its questions are those of the listing in its buy box.
5. **Best sellers:** call `/mercadolibre/best-sellers` with a `category_id` from search (`category_id` or an id in `category_path`) or from product, and the matching `country`.
6. **A seller's catalogue:** call `/mercadolibre/search` with `seller_nickname` to get the seller's first page plus their `seller_id`, then search with `seller_id` (alone or with a `query`) to filter, sort and page.

### Pagination

- **Search:** `page`, 1-42, about 48 rows per page. The response carries `total`, `total_pages`, `page` and `page_size`.
- **Reviews:** `page`, 1-based, 15 per page. A page past the last one comes back empty.
- **Questions:** pass the previous page's `next_offset` as `offset`. `next_offset` is `null` on the last page.
- **Product, best sellers:** no paging.

Every page is billed, so state the budget before looping.

## Parameters

### Search (`/search`)

Pass `country` and at least one of `query`, `seller_id` or `seller_nickname`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | required | `mx`, `br`, `ar` or `co`. Chile is not supported |
| `query` | string | -- | Keywords, 1-200 chars. Mercado Libre may narrow a query to a category, brand or line on its own; the response lists those in `auto_applied_filters` |
| `seller_id` | string | -- | Numeric seller id (as returned in `seller.seller_id` by product). Combines with query, filters, sort and page |
| `seller_nickname` | string | -- | A seller's public nickname (e.g. `MERCADOLIBRE ELECTRONICA_MX`). Returns the seller's first page of listings without filters, plus their `seller_id` |
| `condition` | string | -- | `new`, `used`, `refurbished`, `open_box` |
| `min_price` / `max_price` | integer | -- | Price range in the country's currency |
| `min_discount` | integer | -- | Only listings at least this many percent off: `5`, `10`, `15`, `20`, `25`, `30`, `40` |
| `free_shipping` | boolean | -- | Only listings with free shipping |
| `full_fulfillment` | boolean | -- | Only listings shipped by Mercado Libre Full |
| `official_stores_only` | boolean | -- | Only listings from official brand stores |
| `interest_free_installments` | boolean | -- | Only listings payable in interest-free installments |
| `sort` | string | `relevance` | `relevance`, `price_asc`, `price_desc`. There is no newest or best-selling sort |
| `page` | integer | 1 | Results page, 1-42 |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | Catalog product id from search (e.g. `MLM1027172667`). The prefix (`MLM`, `MLB`, `MLA`, `MCO`) sets the country |
| `item_id` | string | one of | Listing id from search (e.g. `MLM3571336480`; `MLM-3571336480` works too) |
| `url` | string | one of | A product (`/p/`), user product (`/up/`) or listing page URL from a supported country |

Pass exactly one of `product_id`, `item_id` or `url`. No `country` field: the id or URL sets it.

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` / `item_id` / `url` | string | one of | Exactly one, as for product |
| `rating` | integer | -- | Only reviews with this star rating, 1-5 |
| `page` | integer | 1 | Reviews page, 1-based |

### Questions (`/questions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string | one of | Listing id from search or product |
| `url` | string | one of | A listing URL, or a product URL (questions of the listing in its buy box) |
| `offset` | integer | 0 | `next_offset` from the previous page |

Pass exactly one of `item_id` or `url`.

### Best sellers (`/best-sellers`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | required | `mx`, `ar` or `co`. Not available for Brazil |
| `category_id` | string | required | e.g. `MLM1055`, from search or product. Its prefix must match the country |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/mercadolibre/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "mx", "query": "iphone 15", "free_shipping": true, "sort": "price_asc"}'
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def meli(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/mercadolibre/{endpoint}", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]

# 1. Search Mexico: prices in MXN, about 48 rows per page (2 credits)
found = meli("search", {"country": "mx", "query": "iphone 15", "condition": "new"})
print(found["total"], "results;", found["total_pages"], "pages")
for f in found["auto_applied_filters"]:
    print("Mercado Libre applied:", f["name"], [v["name"] for v in f["values"]])
for row in found["results"]:
    seller = row["seller"]["name"] if row["seller"] else None
    print(row["position"], row["sponsored"], row["price"], row["original_price"],
          row["discount_percent"], row["sold_quantity_min"], seller, row["title"])

# 2. One product: buy-box seller, star distribution, variations (2 credits)
product = meli("product", {"product_id": "MLM1027172667"})
print(product["price"], product["currency"], product["seller"]["nickname"],
      product["seller"]["reputation_level"], product["rating"]["distribution"])

# 3. Only the 1-star reviews (1 credit per page of 15)
low = meli("reviews", {"product_id": "MLM1027172667", "rating": 1})
for review in low["reviews"]:
    print(review["rating"], review["country"], review["created_at"], review["text"])

# 4. Buyer questions on the buy-box listing, every page
offset = 0
while offset is not None:
    page = meli("questions", {"item_id": product["item_id"], "offset": offset})
    for q in page["questions"]:
        print(q["text"], "->", q["answer"]["text"] if q["answer"] else None)
    offset = page["next_offset"]

# 5. Top 20 best sellers in the product's category (mx, ar or co)
top = meli("best-sellers", {"country": "mx", "category_id": product["category_id"]})
for row in top["results"]:
    print(row["rank"], row["price"], row["sold_label"], row["title"])

# 6. The seller's catalogue, filtered: seller_id from the product above
catalogue = meli("search", {"country": "mx", "seller_id": str(product["seller"]["seller_id"]),
                            "min_discount": 20})
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **search** - `country`, `site_id`, `query`, `seller_id`, `seller_nickname`, `page`, `page_size`, `total`, `total_pages`, `sort`, `category_id`, `category_path[]`, `applied_filters[]` and `auto_applied_filters[]` {`id`, `name`, `values[]` {`id`, `name`}, `auto_applied`}, `available_filters[]` {`id`, `name`, `values[]` {`id`, `name`, `results`}}, `count`, `results[]`.
  A row: `position`, `sponsored`, `item_id`, `product_id`, `user_product_id`, `title`, `url`, `image`, `price`, `original_price`, `discount_percent`, `currency`, `installments` {`count`, `amount`, `interest_free`}, `seller` {`name`, `official_store`} or null, `brand`, `rating`, `review_count`, `sold_quantity_min`, `sold_label`, `condition`, `free_shipping`, `full_fulfillment`, `shipping_label`, `cross_border`, `cross_border_origin`, `highlight`, `promotions[]` {`type`, `text`}, `category_id`, `domain_id`.
- **product** - `country`, `site_id`, `product_id`, `item_id`, `user_product_id`, `url`, `title`, `brand`, `condition`, `sold_quantity_min`, `sold_label`, `price`, `original_price`, `discount_percent`, `currency`, `installments` {`count`, `amount`, `total`, `interest_free`}, `promotions[]`, `rating` {`average`, `count`, `distribution` {`1`..`5`}, `with_comment`, `with_photos`, `with_videos`}, `seller` {`seller_id`, `name`, `nickname`, `reputation_level`, `power_seller_status`, `official_store_id`, `store_type`, `sales_label`}, `stock` {`available`, `available_label`}, `shipping` {`free_shipping`, `logistic_type`, `mode`}, `variations[]` {`attribute`, `options[]` {`value`, `product_id`, `selected`}}, `specs[]` {`name`, `value`}, `description`, `pictures[]`, `categories[]` {`name`, `url`}, `category_id`, `domain_id`, `best_seller_position`.
- **reviews** - `country`, `site_id`, `product_id`, `item_id`, `rating`, `page`, `page_size`, `count`, `reviews[]` {`review_id`, `rating`, `text`, `original_text`, `translated`, `created_at`, `likes`, `site_id`, `country`, `reviewer_country`, `variant`, `media[]` {`type`, `url`}}.
- **questions** - `country`, `site_id`, `item_id`, `resolved_from`, `offset`, `next_offset`, `count`, `questions[]` {`question_id`, `text`, `answer` {`text`, `date`} or null}.
- **best-sellers** - `country`, `site_id`, `category_id`, `category_name`, `category_path[]` {`id`, `name`}, `count`, `results[]`: the search row fields with `rank` in place of `position` and no `review_count`.

A search row, trimmed (captured, `country: "mx"`, `query: "iphone 15"`):

```json
{
  "position": 1,
  "sponsored": false,
  "item_id": "MLM3571336480",
  "product_id": "MLM1027172667",
  "title": "Apple iPhone 15 (128 GB) - Azul - Distribuidor Autorizado",
  "url": "https://www.mercadolibre.com.mx/apple-iphone-15-128-gb-azul-distribuidor-autorizado/p/MLM1027172667",
  "price": 16096,
  "original_price": 16999,
  "discount_percent": 5,
  "currency": "MXN",
  "installments": { "count": 15, "amount": 1073, "interest_free": true },
  "seller": { "name": "Apple", "official_store": true },
  "brand": "Apple",
  "rating": 4.9,
  "review_count": 1923,
  "sold_quantity_min": 1000,
  "free_shipping": true,
  "full_fulfillment": true,
  "shipping_label": "Llega gratis hoy",
  "highlight": "APPLE TIENDA OFICIAL",
  "category_id": "MLM1055"
}
```

The same search's auto-applied filters (captured):

```json
"auto_applied_filters": [
  { "id": "LINE", "name": "Línea", "values": [{ "id": "25320927", "name": "iPhone 15" }], "auto_applied": true },
  { "id": "BRAND", "name": "Marca", "values": [{ "id": "9344", "name": "Apple" }], "auto_applied": true }
]
```

A product, trimmed (captured, `MLM1027172667`):

```json
{
  "data": {
    "product_id": "MLM1027172667",
    "item_id": "MLM3571336480",
    "condition": "new",
    "sold_quantity_min": 1000,
    "sold_label": "+1000 vendidos",
    "price": 15690.53,
    "original_price": 16999,
    "currency": "MXN",
    "rating": {
      "average": 4.9,
      "count": 26766,
      "distribution": { "1": 228, "2": 41, "3": 138, "4": 723, "5": 25636 }
    },
    "seller": {
      "seller_id": 527927603,
      "name": "Apple",
      "nickname": "MERCADOLIBRE ELECTRONICA_MX",
      "reputation_level": "5_green",
      "power_seller_status": "platinum",
      "store_type": "OFFICIAL_STORE",
      "sales_label": "+1 M ventas"
    },
    "stock": { "available": true, "available_label": "+50 disponibles" },
    "shipping": { "free_shipping": true, "logistic_type": "fulfillment", "mode": "me2" },
    "variations": [
      { "attribute": "color", "options": [
        { "value": "Azul", "product_id": "MLM1027172667", "selected": true },
        { "value": "Negro", "product_id": "MLM1027172677", "selected": false }
      ] }
    ],
    "category_id": "MLM1055",
    "domain_id": "MLM-CELLPHONES"
  }
}
```

A review, trimmed (captured, translated from a Brazilian review on the Mexican site):

```json
{
  "review_id": 1009454165,
  "rating": 5,
  "text": "¡simplemente sensacional! mi primer iphone, decidí cambiar de android y ¡estoy encantado! ...",
  "original_text": "Simplesmente sensacional!!! meu primeiro iphone, decidi sair do android e estou amando!!! ...",
  "translated": true,
  "created_at": "2024-02-18T22:53:21Z",
  "likes": 2187,
  "site_id": "MLB",
  "country": "br",
  "reviewer_country": "Brasil"
}
```

A question with its answer (captured, `MLM3571336480`; there is no question date):

```json
{
  "question_id": 13671430485,
  "text": "¿Tienen disponibilidad del iPhone 15 en color rosa?",
  "answer": {
    "text": "Hola. No, por el momento no tenemos el iPhone 15 en color rosa de este modelo, ...",
    "date": "2026-10-09"
  }
}
```

## Guardrails

- **About 2,000 results per query.** Search serves 42 pages of about 48 rows. To reach more, slice by price range (`min_price` / `max_price`), condition or seller, and de-duplicate by `item_id`. Never claim to have pulled "every listing" when `total` is above what the pages cover.
- **Units sold are ranges, not counts.** `sold_quantity_min` is a lower bound (`sold_label` "+1000 vendidos" means at least 1,000). Never present it as an exact sales figure or derive revenue from it as if it were exact.
- **Brand and review count on search rows.** `brand` and `review_count` come from the product list the search page publishes, which covers organic rows; most sponsored rows, and Colombia beyond the top result, return `review_count: null`. Null means the page published no total, never zero; it happens on some rated listings too, and coverage varies by query. `review_count` is the total the search page shows, and for catalog products that pool reviews across countries it can be lower than the product endpoint's `rating.count`.
- **Sort is relevance or price only.** There is no newest, best-selling or rating sort; use `/best-sellers` for the ranked top 20 in a category.
- **Seller on search rows only where shown.** `seller` and `sold_label` are null on rows where Mercado Libre does not show them on the card. `/product` returns the buy-box seller only; the list of every seller offering a product is not available.
- **Auto-applied filters.** Mercado Libre may narrow a query to a category, brand or line, and in Brazil and Argentina may apply a "new" condition on its own. Read `auto_applied_filters` and tell the user when it changed what was searched.
- **Countries.** Mexico, Brazil, Argentina and Colombia. Chile is not supported. `/best-sellers` is not available for Brazil, and its `category_id` prefix must match the country (`MLM` Mexico, `MLA` Argentina, `MCO` Colombia).
- **Questions carry answer dates only.** Mercado Libre shows no question dates; do not infer one from the answer date.
- **Reviews may be translated.** `text` is in the site's language; `original_text` keeps the original and `country` says where the review was written. A catalog product pools reviews from several countries. Totals and the star distribution come from `/product`, not `/reviews`.
- Mercado Libre's official API needs OAuth app credentials; this skill needs only the Scavio key.
- Public listing data only: no buyer identities or seller contact details.
- Calls usually take 2-10 seconds (product is the slowest); batch sequentially rather than firing many calls at once.
- Never fabricate prices, ratings, reviews or answers. Only return what the API returned, and surface the listing `url` so the user can verify.

## Failure handling

- `400` means an invalid or missing parameter (no `query`, `seller_id` or `seller_nickname` on search; `page` above 42; both or neither of the id fields on product, reviews or questions; `br` on best sellers) - fix the body and retry. Not billed.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means the product, item, seller, category or reviews were not found, or the listing has no public questions; the error says which. These are billed. A search with no results is an empty `200`, also billed.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data).
- `502` / `503` mean Mercado Libre data is temporarily unavailable - wait a few seconds and retry, up to a few times. These are not billed.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.21.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.mercadolibre.search("iphone 15", country="mx", free_shipping=True, sort="price_asc")
product = client.mercadolibre.product(product_id="MLM1027172667")
reviews = client.mercadolibre.reviews(product_id="MLM1027172667", rating=1)
qa = client.mercadolibre.questions("MLM3571336480")
top = client.mercadolibre.best_sellers("MLM1055", country="mx")
```

```bash
npm install scavio@0.21.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const found = await scavio.mercadolibre.search({ country: "mx", query: "iphone 15", sort: "price_asc" });
const product = await scavio.mercadolibre.product({ product_id: "MLM1027172667" });
const top = await scavio.mercadolibre.bestSellers({ country: "mx", category_id: "MLM1055" });
```

MCP: the Scavio MCP server exposes all 5 endpoints as tools (`search_mercadolibre`, `get_mercadolibre_product`, `get_mercadolibre_reviews`, `get_mercadolibre_questions`, `get_mercadolibre_best_sellers`). Mercado Libre is opt-in: add `mercadolibre` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.19.1"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,mercadolibre"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [Mercado Libre search](https://scavio.dev/docs/mercadolibre-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data), [product](https://scavio.dev/docs/mercadolibre-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data), [reviews](https://scavio.dev/docs/mercadolibre-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data), [questions](https://scavio.dev/docs/mercadolibre-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data), [best sellers](https://scavio.dev/docs/mercadolibre-best-sellers?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data). Overview: [Mercado Libre API](https://scavio.dev/mercadolibre-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data).
