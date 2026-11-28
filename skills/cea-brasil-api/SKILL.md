---
name: cea-brasil-api
description: C&A Brasil API for C&A Brasil (cea.com.br, the Brazilian arm of the C&A fashion chain; Brazil only, BRL, Portuguese text) - what each size of a dress, shirt, pair of jeans or any C&A piece costs today, whether it is in stock online, what delivery to a CEP costs and which stores near that CEP can hand the size over, as cea.com.br shows it to a visitor who is not signed in (on 2026-11-27 a Clock House oversized Peruvian-cotton T-shirt read R$ 99.99, R$ 99.99 by Pix, 3x R$ 33.33 interest-free on C&A Pay, in 5 sizes with size G sold out; size M shipped free to a CEP on Avenida Paulista in 6 business days, normally R$ 24.40, or free pickup the next business day at the C&A Avenida Paulista store 0.72 km away; one promotion collection held 1,302 products sorted by discount, led by a linen skirt at R$ 39.99 against R$ 139.99) with price, list price, discount, Pix price, the best installment plan and every size with its own price and capped online quantity; keyword search, category, brand and promotion-collection listings, 24 per page to page 50, in the site's 8 sorts; the filter values with counts; search suggestions and the top searches; the department tree; one product with every size, seller, every payment method's installment plan and specifications; the delivery quote and pickup stores for one size and a CEP; the pickup points near a CEP, C&A stores and third-party pickup lockers, with hours; a product's customer reviews as the product page shows them, up to 100 per page, newest or most helpful, positive, negative, with photos or one star rating, with the star histogram, rating, title, text, the review date, the date of the order the review is linked to, the size and colour bought, fit answers, photos and the store's reply (on 2026-11-28 a white low-top sneaker was rated 4.5 over 1,189 reviews, 854 of them five stars), no reviewer names. 11 endpoints, 1 credit each. Collections come as ids only; no EAN, store units or price history.
version: 1.0.0
tags: cea, c-and-a, c-a-brasil, cea-brasil, cea-com-br, cea-api, cea-brasil-api, c-and-a-brazil, cea-prices, cea-precos, cea-pix, cea-search, cea-product, cea-reviews, cea-avaliacoes, cea-sizes, cea-tamanhos, cea-stock, cea-estoque, cea-deals, cea-ofertas, cea-promocoes, cea-black-friday, cea-collections, cea-brands, cea-marcas, clock-house, palomino, yessica, cea-categories, cea-facets, cea-suggestions, cea-top-searches, cea-shipping, cea-frete, cea-cep, cea-retire-na-loja, cea-pickup, cea-stores, cea-lojas, clique-retire, cea-pay, parcelamento, fashion-prices, clothing-prices, moda-feminina, moda-masculina, brazil, brazil-ecommerce, brazilian-retail, brl, pix, cep, price-monitoring, product-data, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/cea-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api
---

# C&A Brasil API - Fashion Prices per Size, Pix Price, Online Stock, Delivery, Store Pickup by CEP, Reviews

Read C&A Brasil (cea.com.br, the Brazilian arm of the C&A fashion chain): keyword search, category, brand and promotion-collection listings, the filter values with counts, search suggestions and the top searches, the department tree, one product with every size's price and online quantity, the delivery quote and pickup stores for one size and a CEP, the pickup points near a CEP, and a product's customer reviews as its page shows them. www.cea.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in.

**The job this skill is for: what each size of a C&A piece costs today, whether it is in stock online, and how it gets to a CEP.** Every size is its own sku with its own price, list price, Pix price and online quantity. On 2026-11-27 the oversized Peruvian-cotton T-shirt `4536055` (labels C&A and Clock House) read R$ 99.99, R$ 99.99 by Pix (Brazil's instant payment) and 3x R$ 33.33 interest-free on C&A Pay, in sizes PP to GG with size G sold out. Size M (`6493983`) shipped free to CEP 01310-100 in 6 business days (normally R$ 24.40), or free pickup the next business day at C&A Avenida Paulista, 0.72 km away.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Prices per size, as given.** `price` is the price now, `list_price` the regular price, `pix_price` the Pix price. On a listing or product, `price` is the lowest price among the sizes in stock; `sizes[]` has each size's own price.
- **Online quantity is capped.** `available_quantity` is the figure the site gives: a round 100, 10000 or 99999 means plenty, 0 none. It is the online stock, not a store's units. Which stores can hand a size over comes from `/shipping`.
- **Collections are ids only.** `collection_ids` lists the promotion collections a product is in, by id (the site's collection names are not returned). Pass one to `/deals`.
- **Listings stop at page 50.** 24 products a page, pages 1-50; `total` counts every match. Narrow with a category, a brand or a sort to reach the rest.
- **No history or EAN; reviews from `/reviews`.** Everything is the page at the moment of the call; Scavio keeps nothing. The site leaves EAN empty and publishes no store units; `/product` carries no rating, and `/reviews` returns the reviews with the rating summary (reviews can lag the product page by up to 4 hours; reviewer names are never returned). Poll and store your own series.

C&A Brasil publishes no developer API for its catalog, prices or stock. Prices, sizes, delivery quotes and pickup points are shown on cea.com.br for each item, and this skill reads those public pages with one Scavio key.

See also: Lojas Renner `lojas-renner-api`, Dafiti `dafiti-api`, Netshoes `netshoes-api`, Centauro `centauro-api`, Mercado Libre `mercadolibre-product-data` (Brazil marketplace), Magazine Luiza `magalu-magazine-luiza-api`, H&M `hm-api`, Zara `zara-api`.

## When to trigger

Use this skill when the user asks to:
- Price a C&A Brasil item: price, list price, discount, Pix price and installments, per size
- Search cea.com.br by keyword (in Portuguese: "vestido", "calca jeans feminina", "camiseta masculina"), sorted by relevance, price, best sellers, newest, discount or name
- List a C&A department, category or subcategory (`moda-feminina/roupas/blusas`), one of C&A's labels or partner brands (`palomino`, `clock-house`, `yessica`) or a promotion collection by id
- Read the filter values of a search or listing (department, size, colour, gender, Marcas, material, price range) with product counts
- Read the search box's suggestions for a typed start and the site's top searches
- Read the C&A Brasil department tree
- Read one product: every size with sku, price, Pix price, online quantity and seller; every payment method's installment plan; specifications (material, fit, sleeve, made in)
- Quote delivery of one size to a Brazilian CEP, and list the stores near that CEP that can hand the size over
- List the pickup points near a CEP: C&A stores and third-party pickup lockers, with distance and hours
- Read a C&A product's customer reviews and star histogram: newest or most helpful, positive, negative, with photos or one star rating, with the size and colour bought and the fit answers

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/cea/search` | Keywords: 24 products per page (pages 1-50) with total, price, list price, discount, Pix price, best installment, colours, every size with its price and online quantity, categories and collection ids | 1 |
| `POST /api/v1/cea/category` | A department, category or subcategory by path (`moda-feminina/roupas`), same items and sorts as search | 1 |
| `POST /api/v1/cea/brand` | One brand by the site's Marcas value (`palomino`, `clock-house`, `yessica`, `angelo-litrico`, or a partner brand), same items and sorts | 1 |
| `POST /api/v1/cea/deals` | One promotion collection by id (`collection_ids` of any item), with list price, sale price and discount; sort `discount` puts the deepest first | 1 |
| `POST /api/v1/cea/facets` | The filter values for a query, a category, a brand or a collection: department, category, subcategory, gender, size, colour, Marcas, material, price ranges and more, with product counts | 1 |
| `POST /api/v1/cea/suggestions` | The search box's completions for a typed start, with search counts, and the site's top searches | 1 |
| `POST /api/v1/cea/categories` | The department tree over three levels, with each node's path | 1 |
| `POST /api/v1/cea/product` | One product by id, size sku, slug or link: every size with sku, availability, online quantity, price, list price, Pix price and seller; every payment method's longest installment plan; colours, categories, specifications, collection ids, release date | 1 |
| `POST /api/v1/cea/shipping` | The delivery quote for one size and a CEP: delivery options with price and business days, the stores near the CEP that can hand the size over, and the site's messages | 1 |
| `POST /api/v1/cea/stores` | The pickup points near a CEP, nearest first: C&A stores and third-party pickup lockers and counters, with address, coordinates, distance and hours | 1 |
| `POST /api/v1/cea/reviews` | One product's customer reviews by product id, as the product page shows them: up to 100 per page, sorted newest or most helpful, filtered positive, negative, with photos or one star rating, with the star histogram, positive, negative and with-photo counts and the size and colour bought | 1 |

Brazil only: there is no `country` parameter. Every answer carries `store` (cea), `country` (br), `currency` (BRL) and `language` (pt-BR), and most carry `notes`.

## Prices: price, list price, Pix price and installments

| Field | Meaning |
|---|---|
| `price` | The price now, in BRL; on a listing or product, the lowest price among the sizes in stock (all sizes when none is) |
| `list_price` | The regular price (R$ 139.99 on the linen skirt below) |
| `discount_percent` | The difference between the two, as a percent (71) |
| `pix_price` | The price paid by Pix, as the site gives it |
| `best_installment` | `{payment_system, count, value, total, interest_rate}`: the longest interest-free plan (C&A Pay, 3x R$ 33.33, R$ 99.99, 0) |
| `installments` (product) | Each payment method's longest plan: cards, Pix, Vale, Nubank, C&A Pay, the C&A card |
| `sizes[].price`, `sizes[].list_price`, `sizes[].pix_price` | Each size's own prices |

- Quote "camiseta feminina de algodao peruano oversized, size M: R$ 99.99 (list R$ 99.99), R$ 99.99 by Pix, on cea.com.br on 2026-11-27", with the size and the date.
- Quote `pix_price` and the installment plans exactly as given; never compute a Pix discount or an installment yourself, and never judge a price as a good deal.

## Workflow

1. **Find products.** `/search` with `query` (`vestido`), `/category` with `category` (a `categories[].path` from `/categories`), `/brand` with `brand` (a Marcas value from `/facets`), or `/deals` with `collection_id` (from any item's `collection_ids`).
2. **Narrow.** `/facets` with the same query, category, brand or collection: each facet's `param` names the request field a value goes back into (the category-1 / 2 / 3 values make a category path; `marcas` values go into `brand`). The other facets are counts only.
3. **Next pages.** Send `page` 2, 3, ... (up to 50) with the same input and `sort`. `has_more` false means the last page.
4. **One product.** `/product` with `product_id` (`items[].product_id`, `4536055`), or a size `sku`, a `slug` or a `url`: every size's `sku`, prices, online quantity and seller.
5. **Delivery and pickup.** `/shipping` with a size `sku` (`sizes[].sku`, `6493983`) and a `cep` for the delivery options and the stores near the CEP that can hand that size over. `/stores` with a `cep` lists every pickup point near it, without the size check.
6. **Reviews.** `/reviews` with `product_id` (`items[].product_id`, not a size sku); `page` 2, 3, ... while `has_more` is true.
7. **Watching prices:** there is no history. Poll the same searches and products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`), brand (`/brand`) and deals (`/deals`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords in Portuguese, 1-100 characters |
| `category` (category, required) | A category path of 1 to 3 levels (`moda-feminina`, `moda-feminina/roupas`, `moda-feminina/roupas/blusas`; `categories[].path`) or its cea.com.br link |
| `brand` (brand, required) | A brand as the site's Marcas filter writes it (`palomino`, `clock-house`, `yessica`, `angelo-litrico`; `facets` key `marcas`) |
| `collection_id` (deals, required) | A promotion collection id, digits (`19727`; `items[].collection_ids`) |
| `sort` | `relevance` (default), `price_asc`, `price_desc`, `best_sellers` (most ordered), `newest` (release date), `discount` (deepest first), `name_asc`, `name_desc`: the site's 8 sorts |
| `page` | 1-50 (the site pages at most 50 pages deep) |
| `page_size` | 1-24 (default 24) |

A search with no products returns an empty `200`.

### Facets (`/facets`)

Send `query`, or exactly one of `category`, `brand` or `collection_id`, written as above.

### Suggestions (`/suggestions`) and categories (`/categories`)

`/suggestions` takes `query` (the start of a search, 1-100 characters, `cal`); without it, the top searches alone. `/categories` takes an empty body `{}`.

### Product (`/product`)

Send exactly one of `product_id` (`items[].product_id`, e.g. `4536055`), `sku` (one size, `sizes[].sku`: returns its product), `slug` (the link's path before `/p`) or `url` (`https://www.cea.com.br/<slug>/p`).

### Shipping (`/shipping`) and stores (`/stores`)

| Parameter | Description |
|---|---|
| `sku` (shipping, required) | The id of one size (`sizes[].sku` from `/product` or a listing, `6493983`) |
| `cep` (required) | A Brazilian CEP (postal code) of 8 digits, with or without the dash (`01310-100`) |

`/shipping` is read-only: nothing is added to a cart or ordered. The quote is for 1 unit of the size.

### Reviews (`/reviews`)

| Parameter | Description |
|---|---|
| `product_id` (required) | The product id (`items[].product_id` or `product_id` of `/product`, `3700395`), not a size sku or the reference |
| `page` | Reviews page, 1-200 (default 1) |
| `per_page` | Reviews per page, 1-100 (default 20) |
| `sort` | `newest` (default) or `most_helpful` (the most helpful votes at the top) |
| `filter` | `all` (default), `positive` (ratings 3-5), `negative` (ratings 1-2) or `with_photos` |
| `rating` | Only the reviews with this star rating, 1-5. Send `rating` or `filter`, not both |

## Examples

### One search item

Request `{"query": "vestido"}` (1 credit): `total` 13549, `total_pages` 50, 24 items. One item, abridged to one size:

```json
{
  "position": 1,
  "product_id": "4506839",
  "name": "vestido midi decote v com recorte listrado off white",
  "brand": "C&A",
  "reference": "1078772-off_white",
  "available": true,
  "price": 219.99,
  "list_price": 239.99,
  "discount_percent": 8,
  "pix_price": 219.99,
  "best_installment": { "payment_system": "C&A Pay", "count": 5, "value": 43.99, "total": 219.99, "interest_rate": 0 },
  "colors": ["OFF White"],
  "sizes": [
    { "sku": "6381605", "size": "PP", "color": "OFF White", "available": true, "available_quantity": 10000, "price": 219.99, "list_price": 239.99, "discount_percent": 8, "pix_price": 219.99 }
  ],
  "release_date": "2024-10-14T17:46:00.000Z"
}
```

The item also carried `labels` (C&A, Clock House), `url`, `image`, 4 more sizes (5 in all), 3 `categories` (Moda Feminina, Roupas, Vestidos) and 93 `collection_ids`.

### One product

Request `{"product_id": "4536055"}` (1 credit), abridged to two sizes:

```json
{
  "product_id": "4536055",
  "name": "camiseta feminina de algodão peruano oversized com recorte marrom",
  "brand": "C&A",
  "labels": ["C&A", "Clock House"],
  "reference": "1092338-marrom_esc",
  "model_id": "1092338",
  "available": true,
  "price": 99.99,
  "list_price": 99.99,
  "discount_percent": 0,
  "pix_price": 99.99,
  "best_installment": { "payment_system": "C&A Pay", "count": 3, "value": 33.33, "total": 99.99, "interest_rate": 0 },
  "colors": ["Marrom Escuro"],
  "sizes": [
    { "sku": "6493983", "size": "M", "color": "Marrom Escuro", "available": true, "available_quantity": 100, "price": 99.99, "list_price": 99.99, "discount_percent": 0, "pix_price": 99.99, "seller": { "id": "1", "name": "CeA" } },
    { "sku": "6493984", "size": "G", "color": "Marrom Escuro", "available": false, "available_quantity": 0, "price": 99.99, "list_price": 99.99, "discount_percent": 0, "pix_price": 99.99, "seller": { "id": "1", "name": "CeA" } }
  ],
  "categories": ["Moda Feminina", "Roupas", "Blusas"],
  "release_date": "2025-09-15T22:05:00.000Z"
}
```

The product also carried 5 sizes in all (PP, P, M, G, GG), 4 images, 11 `installments` (American Express, Visa, Diners, Mastercard and Elo 2x R$ 49.99; Vale, Pix and Nubank 1x R$ 99.99; C&A Pay 3x R$ 33.33; the C&A card 2x R$ 49.99; Google Pay 2x R$ 49.99, all interest-free), 9 `specifications` (Manga: Manga Curta, Material: Algodão peruano, Produzido: Peru, ...) and 69 `collection_ids`.

### Delivery, pickup and pickup points

- `/shipping` `{"sku": "6493983", "cep": "01310-100"}`:

```json
{
  "sku": "6493983",
  "cep": "01310100",
  "availability": "available",
  "price": 99.99,
  "list_price": 99.99,
  "can_deliver": true,
  "can_pick_up": true,
  "delivery_options": [
    { "name": "Normal", "price": 0, "list_price": 24.4, "estimate": "6bd", "business_days": 6, "estimated_date": "2026-12-07T16:31:00-03:00" }
  ],
  "pickup_stores": [
    { "pickup_point_id": "ceaapl_APL", "store_code": "APL", "name": "C&A Avenida Paulista", "distance_km": 0.72, "price": 0, "estimate": "1bd", "business_days": 1, "estimated_date": "2026-11-30T16:31:00-03:00" }
  ],
  "messages": []
}
```

The pickup store also carried its `address` (Av. Paulista 1374, Bela Vista, São Paulo, SP). 5 stores could hand size M over, all free in 1 business day, the farthest C&A Shopping Campo Limpo at 14.25 km.
- `/stores` `{"cep": "01310-100"}`: `total` 121, 18 listed, nearest first: Clique Retire - Decathlon Paulista (`type` partner_point, `partner` Clique Retire, 0.05 km, Monday 05:00-23:00), then C&A Avenida Paulista (`type` cea_store, 0.72 km), C&A Rua Augusta (1.27 km) and 15 more C&A stores to 7.91 km.

### Deals, facets, suggestions and categories

- `/deals` `{"collection_id": "19727", "sort": "discount"}`: `total` 1302, first a saia curta feminina com linho bordada vermelha (labels C&A, Yessica) at R$ 39.99 against R$ 139.99, 71 percent off.
- `/brand` `{"brand": "palomino"}`: `total` 20216. `/category` `{"category": "moda-feminina/roupas"}`: `total` 93575.
- `/facets` `{"query": "vestido"}`: 13 facets, e.g. `{"key": "category-3", "label": "Subcategoria", "param": "category", "values": [{"value": "vestidos", "label": "Vestidos", "count": 13366, "selected": false}, ...]}`, `marcas` with 65 values (`param` brand), and price `ranges` from R$ 39.99.
- `/suggestions` `{"query": "cal"}`: 5 completions, `calca jeans feminina` with 39814 searches; `top_searches` led by `vestido` (190040) and `blusa feminina` (62607).
- `/categories` `{}`: 8 departments (Moda Feminina, Moda Masculina, Serviços, Beleza, Casa, Eletrônicos, Infantil, Esporte), 363 nodes.

### Reviews

Request `{"product_id": "3700395"}` (1 credit): `product_name` tênis casual cano baixo branco, `rating` {"average": 4.5, "count": 1189, "histogram": {"1": 62, "2": 31, "3": 32, "4": 210, "5": 854}}, `review_counts` {"total": 1189, "positive": 1096, "negative": 93, "with_photos": 27}, `count` 20, `has_more` true, newest first. One review:

```json
{
  "id": "34911848",
  "rating": 5,
  "title": null,
  "text": "Muito confortável.",
  "date": "2026-04-20",
  "purchase_date": "2026-04-09",
  "recommends": true,
  "helpful_votes": 1,
  "unhelpful_votes": 0,
  "photos": [],
  "attributes": [
    {
      "name": "Tamanho",
      "answer": "Ideal"
    },
    {
      "name": "Custo-benefício",
      "answer": "Ótimo"
    },
    {
      "name": "Material",
      "answer": "Ótimo"
    },
    {
      "name": "Conforto",
      "answer": "Muito Confortável"
    }
  ],
  "store_reply": null,
  "imported": false,
  "influencer": false,
  "purchased": {
    "sku": "4399816",
    "size": "36",
    "color": "Branco"
  }
}
```

No reviewer name is returned. `attributes` are the store's follow-up questions with the customer's answer; `purchased` is the size sku bought.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def cea(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/cea/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Dresses, lowest price first (1 credit)
hits = cea("search", {"query": "vestido", "sort": "price_asc"})["data"]
for it in hits["items"][:5]:
    print(it["name"], it["price"], it["list_price"], it["discount_percent"], it["product_id"])

# 2. One product: every size with its price and online quantity (1 credit)
item = cea("product", {"product_id": hits["items"][0]["product_id"]})["data"]
size = next(s for s in item["sizes"] if s["available"])
print(size["size"], size["price"], size["pix_price"], size["available_quantity"])

# 3. Delivery and pickup for that size to a CEP (1 credit)
ship = cea("shipping", {"sku": size["sku"], "cep": "01310-100"})["data"]
print([(o["name"], o["price"], o["business_days"]) for o in ship["delivery_options"]])
print([(s["name"], s["distance_km"]) for s in ship["pickup_stores"]])

# C&A Brasil prices change during the day. Store each answer with fetched_at and
# run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `country`, `currency` and `language`.

- **search / category / brand / deals** - `query` (search), `category` and `url` (category), `brand` (brand), `collection_id` (deals), `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `sort`, `items[]` {`position`, `product_id`, `name`, `brand`, `labels`, `reference`, `url`, `image`, `available`, `price`, `list_price`, `discount_percent`, `pix_price`, `best_installment` {`payment_system`, `count`, `value`, `total`, `interest_rate`}, `colors`, `sizes[]` {`sku`, `size`, `color`, `available`, `available_quantity`, `price`, `list_price`, `discount_percent`, `pix_price`}, `categories`, `collection_ids`, `release_date`}, `notes`.
- **facets** - `query`, `category`, `brand`, `collection_id`, `count`, `facets[]` {`key`, `label`, `param`, `values[]` {`value`, `label`, `count`, `selected`} or `ranges[]` {`from`, `to`, `count`}}, `notes`.
- **suggestions** - `query`, `count`, `suggestions[]` {`term`, `count`, `attributes[]` {`key`, `value`, `label`, `value_label`}}, `top_searches[]` {`term`, `count`}, `notes`.
- **categories** - `count`, `node_count`, `categories[]` {`category_id`, `name`, `path`, `url`, `children[]`}, `notes`.
- **product** - `requested`, `product_id`, `sku` (when asked by sku), `name`, `brand`, `labels`, `reference`, `model_id`, `url`, `images`, `available`, `price`, `list_price`, `discount_percent`, `pix_price`, `best_installment`, `installments[]` {`payment_system`, `count`, `value`, `total`, `interest_rate`}, `colors`, `sizes[]` (as above, plus `seller` {`id`, `name`}), `categories`, `specifications[]` {`name`, `value`}, `collection_ids`, `release_date`, `notes`. The reviews come from `/reviews`. No marketing description, EAN, Q&A or store units.
- **shipping** - `sku`, `cep`, `availability`, `price`, `list_price`, `can_deliver`, `can_pick_up`, `delivery_options[]` {`name`, `price` (0 = free), `list_price`, `estimate`, `business_days`, `estimated_date`}, `pickup_stores[]` {`pickup_point_id`, `store_code`, `name`, `distance_km`, `address`, `price`, `estimate`, `business_days`, `estimated_date`}, `messages[]` {`code`, `text`, `status`}, `notes`.
- **reviews** - `product_id`, `page`, `per_page`, `sort`, `filter`, `rating_filter`, `total` (the reviews matching the request, from the rating summary), `has_more`, `count`, `product_name`, `rating` {`average`, `count`, `histogram` {`1`-`5`}}, `review_counts` {`total`, `positive` (ratings 3-5), `negative` (ratings 1-2), `with_photos`}, `reviews[]` {`id`, `rating`, `title`, `text` (null when the review has stars but no text), `date`, `purchase_date` (the date of the order the review is linked to), `recommends`, `helpful_votes`, `unhelpful_votes`, `photos[]` {`image`, `thumbnail`}, `attributes[]` {`name`, `answer`}, `store_reply`, `imported`, `influencer`, `purchased` {`sku`, `size`, `color`} (the size bought, where the review carries it)}, `notes`. No reviewer names or questions and answers.
- **stores** - `cep`, `total`, `count`, `stores[]` {`store_code`, `pickup_point_ids`, `name`, `type` (cea_store, partner_point), `partner`, `active`, `distance_km`, `address` {`street`, `number`, `complement`, `neighborhood`, `city`, `state`, `cep`}, `latitude`, `longitude`, `phone`, `hours[]` {`day`, `opens`, `closes`}}, `notes`.

## Guardrails

- Name it "C&A Brasil (cea.com.br)" on first mention. C&A Brasil accounts, carts and checkout are not read or made.
- Prices: quote `price` with `list_price`, the size and the `fetched_at` date, in BRL (R$). On a listing, `price` is the lowest in-stock size price; quote a size's own price from `sizes[]` when the user names a size.
- Pix and installments: quote `pix_price`, `best_installment` and `installments` exactly as given. Never compute a Pix discount or an installment.
- Stock: `available_quantity` is the site's capped online figure (a round 100, 10000 or 99999 means plenty, 0 none). Never present it as an exact count or as a store's units.
- Pickup points: `/stores` mixes C&A stores (`type` cea_store) with third-party pickup lockers and counters (`type` partner_point, e.g. Clique Retire). Say which one a row is; never call a locker a C&A store. Only `/shipping` says whether a given size can be picked up at a store.
- Collections: `collection_ids` are ids; the site's collection names are not returned. Never invent a name for a collection.
- Comparing C&A Brasil with Renner, Dafiti or another store: compare the same product, size and date. Never call one store cheaper beyond the numbers shown.
- Images and copy: refer to products by `product_id` and `url`; do not republish C&A's product photos or page copy, and keep any use descriptive.
- Reviews: quote `rating`, `date` and the store's own summary figures as facts with the `fetched_at` date. `text` and `title` are the customer's own words: quote a short excerpt where it answers the question, never republish review bodies in bulk, and never invent or merge one. `purchase_date` is the date of the order the review is linked to; describe it in exactly those words, never as more. Reviewer names are never returned; never look for the person behind a review. `imported` marks a review the store brought in from another source, `influencer` one the store marks as from an influencer: say so when it matters. Reviews can lag the product page by up to 4 hours.
- Not available: EAN, store units, Q&A, reviewer names, collection names, price history (poll and store), account data, cart or checkout. This API cannot buy or reserve anything.
- Terms: Scavio does not store C&A Brasil data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. C&A Brasil's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, quantities, delivery options or pickup points. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id, sku, slug or url is required"; "Pass one of product_id, sku, slug or url (got ...)."; "query, category, brand or collection_id is required"; "Pass one of category, brand or collection_id (got ...)."; "category must be a category path of 1 to 3 levels as the site writes it (e.g. moda-feminina/roupas/blusas; categories[].path)."; "brand must be a brand value as the site writes it (facets: key marcas, e.g. palomino, clock-house)."; "collection_id must be a collection id (digits, e.g. 19727; items[].collection_ids)."; "cep must be a Brazilian CEP: 8 digits (e.g. 01310-100)."; "url must be a cea.com.br product link (https://www.cea.com.br/<slug>/p)."; "product_id is required (the product id, items[].product_id, e.g. 4536055)."; "Pass rating or filter, not both.".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "C&A Brasil has no product for this id.", "C&A Brasil has no item with sku <sku> (sizes[].sku).", "C&A Brasil has no reviews page for product <id> (an unknown product id: pass items[].product_id, not a sku or reference)." Some unknown ids answer `200` with no reviews and zero counts (charged). A search with no products is an empty `200`, not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api).
- `502` and `503` mean C&A Brasil data was temporarily unavailable ("C&A Brasil is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- Listings (search, category, brand, deals) are large: usually 5-100 seconds (in the captures 11-15 seconds); allow a client timeout of at least 240 seconds. Reviews usually take 2-20 seconds; allow at least 180 seconds. Everything else usually takes 2-15 seconds; allow at least 120 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.106.0
npm install scavio@0.107.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.cea.search({ query: "vestido", sort: "price_asc" });
const { data: blouses } = await scavio.cea.category({ category: "moda-feminina/roupas/blusas" });
const { data: palomino } = await scavio.cea.brand({ brand: "palomino", sort: "newest" });
const { data: deals } = await scavio.cea.deals({ collection_id: "19727", sort: "discount" });
const { data: facets } = await scavio.cea.facets({ query: "jeans" });
const { data: suggestions } = await scavio.cea.suggestions({ query: "jaq" });
const { data: tree } = await scavio.cea.categories({});
const { data: item } = await scavio.cea.product({ product_id: "4536055" });
const { data: ship } = await scavio.cea.shipping({ sku: "6493983", cep: "01310-100" });
const { data: stores } = await scavio.cea.stores({ cep: "01310-100" });
const { data: reviews } = await scavio.cea.reviews({ product_id: "3700395", filter: "negative" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.cea.search(...)`, `category`, `brand`, `deals`, `facets`, `suggestions`, `categories`, `product`, `shipping`, `stores` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `search_cea`, `get_cea_category`, `get_cea_brand`, `get_cea_deals`, `get_cea_facets`, `get_cea_suggestions`, `get_cea_categories`, `get_cea_product`, `get_cea_shipping`, `get_cea_stores` and `get_cea_reviews`. C&A Brasil is opt-in: add `cea` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.106.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,cea"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/cea-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api), [category](https://scavio.dev/docs/cea-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api), [brand](https://scavio.dev/docs/cea-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api), [deals](https://scavio.dev/docs/cea-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api), [facets](https://scavio.dev/docs/cea-facets?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api), [suggestions](https://scavio.dev/docs/cea-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api), [categories](https://scavio.dev/docs/cea-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api), [product](https://scavio.dev/docs/cea-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api), [shipping](https://scavio.dev/docs/cea-shipping?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api), [stores](https://scavio.dev/docs/cea-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api), [reviews](https://scavio.dev/docs/cea-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api). Platform page: [scavio.dev/cea-api](https://scavio.dev/cea-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=cea-brasil-api).
