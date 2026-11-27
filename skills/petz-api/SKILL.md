---
name: petz-api
description: Petz API for Petz (petz.com.br, the Brazilian pet store of Grupo Petz Cobasi; Brazil only, BRL, Portuguese text) - what a bag of dog or cat food, a litter or any pet supply costs at Petz today in each size, what it costs on Assinatura Petz (the repeat-delivery subscription) and for Clubz loyalty members, how much stock the site shows, and which Petz store is open when, as petz.com.br shows it to a visitor who is not signed in (on 2026-11-27 Racao Selections For Pet for small adult dogs read R$ 46.39 against R$ 57.99 for 3 kg, R$ 107.99 for 10.1 kg and R$ 144.49 for 15 kg, each size with 100 or more units, rated 4.9 from 32 ratings; the search "racao golden" counted 72 products, Golden Special for adult dogs 15 kg at R$ 159.99 and R$ 143.99 on subscription; the store directory listed 269 stores, 128 in Sao Paulo state) with price, list price, discount, subscription price and discount, Clubz member price, EAN, stock units (capped at 100) and every size or variant with its own prices; keyword search, category and brand listings and the deals page (Promocoes) or a themed collection, 20 per page to page 50, sorted by relevance, price or newest; one product with specs, the rating summary with the count per star and the 3 latest reviews (no names), every size or variant with its own prices and stock; the store directory narrowed by state and city with address, phone, hours and the store pickup flag; one store with its Google Maps place id. 7 endpoints, 1 credit each. Search totals stop at 1,000; no per-store stock or prices, review paging, suggestions, Pix price, installments or shipping.
version: 1.0.0
tags: petz, petz-com-br, petz-api, petz-brasil, petz-prices, petz-precos, petz-search, petz-busca, petz-product, petz-racao, petz-category, petz-brands, petz-marcas, petz-deals, petz-promocoes, petz-ofertas, petz-black-friday, petz-colecao, assinatura-petz, petz-subscription, petz-assinatura, clubz, petz-clubz, petz-stock, petz-estoque, petz-reviews, petz-avaliacoes, petz-stores, petz-lojas, petz-store-hours, petz-retire-na-loja, petz-pickup, grupo-petz-cobasi, pet-store, pet-shop, pet-food-prices, dog-food-prices, cat-food-prices, racao, pet-supplies, ean, brazil, brazil-ecommerce, brazilian-retail, brl, price-monitoring, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 300
    throttle: 1
    homepage: https://scavio.dev/petz-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=petz-api
---

# Petz API - Pet Supply Prices by Size, Assinatura Petz and Clubz Prices, Stock, Store Hours

Read Petz (petz.com.br, the Brazilian pet store of Grupo Petz Cobasi): keyword search, category and brand listings, the deals page or a themed collection, one product with every size and its subscription price, the store directory and one store in full. www.petz.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in.

**The job this skill is for: what a pet product costs at Petz today, size by size, on subscription and for Clubz members, and which Petz store a shopper can reach.** Petz sells most products in several sizes or variants, each with its own price, its Assinatura Petz (repeat-delivery subscription) price and its stock. On 2026-11-27 the Selections For Pet dry food for small and mini adult dogs (`191628`) read R$ 46.39 against R$ 57.99 (20 percent off) for 3 kg, R$ 107.99 against R$ 134.99 for 10.1 kg and R$ 144.49 against R$ 169.99 for 15 kg, every size showing 100 or more units, rated 4.9 from 32 ratings. In the search "ração golden" the Golden Special food for adult dogs 15 kg read R$ 159.99, R$ 143.99 on subscription (10 percent off) and R$ 143.99 for Clubz members.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Petz pages are slow.** Listings usually take 50-150 seconds, up to about 245; product, stores and store usually 30-95 seconds (in the captures 6 to 46 seconds). Allow a client timeout of at least 300 seconds.
- **Stock is capped at 100.** `stock_units` is the count Petz shows, up to 100; `stock_capped` true means 100 or more. Say "100 or more units", never 100.
- **Search totals stop at 1,000.** Listings return 20 products a page up to page 50. A search counts at most 1,000 products (`total_capped` true); the deals page can count more.
- **Prices are per size.** A listing item and a product carry `variations[]`, one per size or variant, each with its own `price`, `list_price` and `subscription_price`. Quote the size with the price.
- **Not offered:** per-store stock or prices, prices by CEP, more than the 3 latest reviews, search suggestions, Pix prices, installments, shipping and deal validity dates. Petz publishes no dates for its deals.

Petz publishes no developer API for its catalog, prices or stores. They are shown on petz.com.br to any visitor, and this skill reads those public pages with one Scavio key.

See also: Cobasi `cobasi-api` (the other store of Grupo Petz Cobasi); Petco `petco-product-data`, PetSmart `petsmart-product-data`, Chewy `chewy-product-data` (pet stores in the US); Mercado Libre `mercadolibre-product-data` (Brazil marketplace); Brazilian retail: Magazine Luiza `magalu-magazine-luiza-api`, Carrefour Brasil `carrefour-brasil-api`.

## When to trigger

Use this skill when the user asks to:
- Search Petz by keyword (in Portuguese: "ração golden", "areia gato", "arranhador"), sorted by relevance, price or newest
- List one Petz category (`cachorro`, `cachorro/racao`, `gato/areia-e-banheiros`) or one brand (`royal-canin`, `premierpet`)
- Read the Petz deals page (Promoções) or a themed collection (`pf-petz-friday`): the deal price next to the regular price and the discount
- Read one Petz product: every size with its price, list price, subscription price and stock, EAN, specs and rating
- Compare the one-off price of a pet food with its Assinatura Petz subscription price or its Clubz member price
- List Petz stores in a state or city with address, phone, opening hours and whether online orders can be picked up there
- Read one Petz store's address, hours and Google Maps place id

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=petz-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=petz-api) - email or Google, no card required.
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
| `POST /api/v1/petz/search` | Keywords: 20 products per page with total (at most 1,000), price, list price, discount, subscription price and discount, Clubz member price, EAN, availability, stock units and every size or variant with its own prices | 1 |
| `POST /api/v1/petz/category` | A category by path (a pet, or a pet and a department: `cachorro/racao`), same items and sorts, with the category name | 1 |
| `POST /api/v1/petz/brand` | A brand by slug (`royal-canin`), same items and sorts, with the brand name | 1 |
| `POST /api/v1/petz/deals` | The deals page (Promoções) or a themed collection by slug, same items and sorts, the deal price next to the regular price | 1 |
| `POST /api/v1/petz/product` | One product by id or link: brand, sub-brand, categories, images, prices, subscription price, availability, stock units, specs, the rating summary with the count per star, the 3 latest reviews and every size or variant with its own prices and stock | 1 |
| `POST /api/v1/petz/stores` | The store directory (269 stores), narrowed by state and city: address with CEP, phone, opening hours and the store pickup flag | 1 |
| `POST /api/v1/petz/store` | One store by slug or link: address, phone, opening hours, photo and Google Maps place id | 1 |

Brazil only: there is no `country` parameter. Every answer carries `country` (br), `currency` (BRL) and `language` (pt-BR), and a `note`.

## Prices: price, list price, subscription and Clubz

| Field | Meaning |
|---|---|
| `price` | The current price, in BRL: R$ 46.39 for the 3 kg bag below |
| `list_price` | The regular price when a deal price applies (R$ 57.99); null otherwise |
| `discount_percent` | The discount, as the site gives it (20) |
| `subscription_price` | The Assinatura Petz (repeat delivery) price, rounded to cents (R$ 143.99 on the Golden Special 15 kg) |
| `subscription_discount_percent` (listings) | The subscription discount the site shows (10) |
| `clubz` (listings) | `{price, tiers}`: the price Petz shows for Clubz loyalty members and the tiers it names (PRATA, OURO, DIAMANTE) |
| `variations[]` | One row per size or variant (`name`: "3 kg", "10,1 kg", "15 kg"), each with its own `price`, `list_price`, `discount_percent` and `subscription_price` |

- Quote "Ração Selections For Pet para Cães Adultos de Porte Pequeno e Mini Sabor Frango, 3 kg: R$ 46.39 (list R$ 57.99), on petz.com.br on 2026-11-27", with the size and the date.
- Quote the subscription and Clubz prices as given; they can equal the price when a deal is deeper. Never compute a subscription discount, a price per kg or an installment, and never judge a price as a good deal.

## Workflow

1. **Find products.** `/search` with `query` (`ração golden`), `/category` with `category` (`cachorro/racao`), `/brand` with `brand` (`royal-canin`, a product's `brand.slug`), or `/deals` (optionally `collection`, `PF-racoes`). Each item's `product_id` (and each variation's) is the input of `/product`.
2. **Sort and page.** `sort` (relevance, price_asc, price_desc, newest) and `page` 2, 3, ... up to 50. `has_more` false means the last page; `total_capped` true means the search stopped counting at 1,000.
3. **One product.** `/product` with `product_id` (`191628`) or `url`: every size with its prices and stock, specs and rating.
4. **Stores.** `/stores` with `state` (`SP`) and `city` (`São Paulo`) for the stores there; `/store` with a `slug` from that list (`petz-aclimacao`) for one store in full.
5. **Watching prices and stock:** there is no history. Poll the same listings and products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`), brand (`/brand`) and deals (`/deals`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords in Portuguese, 1-200 characters |
| `category` (category, required) | A category path: a pet, or a pet and a department, as lowercase slugs joined by `/` (`cachorro`, `cachorro/racao`, `gato/areia-e-banheiros`) |
| `brand` (brand, required) | A brand slug as Petz writes it (a product's `brand.slug`): `royal-canin`, `premierpet` |
| `collection` (deals) | A Petz collection (a themed deals list) by its slug as its link shows it (`pf-petz-friday`, `PF-racoes`). Leave out for the main deals page (Promoções) |
| `sort` | `relevance` (default), `price_asc`, `price_desc`, `newest` |
| `page` | 1-50 (20 products per page) |

A search with no products returns `total` 0 (a `200`). When Petz redirects a category or brand link to another listing, `category.path` / `brand.slug` is the listing answered and `redirected_from` the one asked.

### Product (`/product`)

`/product` takes `product_id` (3 to 9 digits, `items[].product_id` or `variations[].product_id`, e.g. `191628`) or `url` (a Petz product link, `https://www.petz.com.br/produto/<name>-<id>`).

### Stores (`/stores`) and store (`/store`)

| Parameter | Description |
|---|---|
| `state` (stores) | A Brazilian state code (UF): `SP`, `RJ` |
| `city` (stores) | A city name; accents and case are ignored (`São Paulo`) |
| `slug` (store) | The store slug (`stores[].slug`, e.g. `petz-aclimacao`), or `url`, a Petz store link (`https://www.petz.com.br/loja/<slug>`) |

`/stores` with no parameters returns every store.

## Examples

### One search item

Request `{"query": "ração golden"}` (1 credit): `total` 72, `total_capped` false, `total_pages` 4, 20 items, every one with 100 or more units. One item, abridged to its first two sizes:

```json
{
  "position": 1,
  "product_id": "71343",
  "sku": "10002310000032",
  "ean": "7897348202431",
  "name": "Ração Golden Special para Cães Adultos Sabor Frango e Carne",
  "brand": "Premier Pet",
  "sub_brand": "Golden",
  "categories": ["Cachorro", "Ração", "Ração Seca"],
  "price": 159.99,
  "list_price": null,
  "discount_percent": null,
  "subscription_price": 143.99,
  "subscription_discount_percent": 10,
  "clubz": { "price": 143.99, "tiers": ["PRATA", "OURO", "DIAMANTE"] },
  "currency": "BRL",
  "available": true,
  "availability": "in_stock",
  "stock_units": 100,
  "stock_capped": true,
  "has_variations": true,
  "variations": [
    { "product_id": "71343", "sku": "10002310000032", "ean": "7897348202431", "name": "15 kg", "price": 159.99, "list_price": null, "discount_percent": null, "subscription_price": 143.99, "available": true, "selected": true },
    { "product_id": "71345", "sku": "10002310000076", "ean": "7897348203162", "name": "20 kg", "price": 204.99, "list_price": null, "discount_percent": null, "subscription_price": 184.49, "available": true, "selected": false }
  ]
}
```

The item and each variation also carried `url`, and the item `image`.

### One product

Request `{"product_id": "191628"}` (1 credit), abridged:

```json
{
  "product_id": "191628",
  "sku": "10001305000148",
  "ean": "7908471130499",
  "name": "Ração Selections For Pet para Cães Adultos de Porte Pequeno e Mini Sabor Frango",
  "brand": { "name": "Petz", "slug": "petz" },
  "sub_brand": { "name": "Selections For Pets", "slug": "selections-for-pets" },
  "category": "Ração Seca",
  "price": 46.39,
  "list_price": 57.99,
  "discount_percent": 20,
  "subscription_price": 46.39,
  "available": true,
  "availability": "in_stock",
  "stock_units": 100,
  "stock_capped": true,
  "published": "2024-06-03",
  "rating": { "average": 4.9, "count": 32, "stars": { "1": 0, "2": 0, "3": 0, "4": 3, "5": 29 } },
  "has_variations": true,
  "variations": [
    { "product_id": "191628", "sku": "10001305000148", "name": "3 kg", "description": "3 Kilos", "price": 46.39, "list_price": 57.99, "discount_percent": 20, "subscription_price": 46.39, "available": true, "availability": "in_stock", "stock_units": 100, "stock_capped": true, "on_promotion": true, "is_combo": false, "current": true },
    { "product_id": "191636", "sku": "10001305000156", "name": "10,1 kg", "description": "10,1 kilos", "price": 107.99, "list_price": 134.99, "discount_percent": 20, "subscription_price": 107.99, "available": true, "availability": "in_stock", "stock_units": 100, "stock_capped": true, "on_promotion": true, "is_combo": false, "current": false },
    { "product_id": "191633", "sku": "10001305000153", "name": "15 kg", "description": "15 Kilos", "price": 144.49, "list_price": 169.99, "discount_percent": 15, "subscription_price": 144.49, "available": true, "availability": "in_stock", "stock_units": 100, "stock_capped": true, "on_promotion": true, "is_combo": false, "current": false }
  ]
}
```

The product also carried 3 `categories` ({name, path}), 7 `images`, 17 `specs` (Idade: Adulto, Porte de Raça: Pequeno e Mini, Sabor Principal: Frango, Níveis de Garantia, Composição, ...) and 3 `latest_reviews` ({date, rating, text}: 2026-11-17, 2026-11-12 and 2026-10-08, all rated 5, one without text), with no reviewer names. The subscription price equals the deal price here: quote it as given.

### Category, brand, deals and stores

- `/category` `{"category": "cachorro/racao"}`: `category.name` Ração para cachorro, `total` 978, first a Selections For Pet food for medium and large adult dogs 15 kg at R$ 124.99 against R$ 154.99.
- `/brand` `{"brand": "royal-canin"}`: `brand.name` Royal Canin, `total` 166, first Royal Canin Kitten Persian 1.5 kg at R$ 107.99 against R$ 168.99 with 15 units.
- `/deals` `{"collection": "PF-racoes"}`: `deals.name` Rações de até 35% OFF, `total` 411, first a Royal Canin food for neutered kittens 4 kg at R$ 210.99 against R$ 341.99 (38 percent off) with 10 units.
- `/stores` `{"state": "SP"}`: `total` 269, `count` 128; Petz Aclimação, Rua Muniz de Sousa, 450, CEP 01534-000, phone (11) 2181-7417, open every day 09:00-22:00, `pickup` true.
- `/store` `{"slug": "petz-aclimacao"}`: the same store with its `google_place_id` and photo.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def petz(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/petz/{endpoint}", headers=HEADERS, json=body, timeout=300)
    r.raise_for_status()
    return r.json()

# 1. Royal Canin, lowest price first (1 credit; listings are slow)
hits = petz("brand", {"brand": "royal-canin", "sort": "price_asc"})["data"]
for it in hits["items"][:5]:
    stock = "100 or more" if it["stock_capped"] else it["stock_units"]
    print(it["name"], it["price"], it["list_price"], it["subscription_price"], stock, it["product_id"])

# 2. Every size of the first one, with its prices and stock (1 credit)
item = petz("product", {"product_id": hits["items"][0]["product_id"]})["data"]
for v in item["variations"] or []:
    print(v["name"], v["price"], v["list_price"], v["subscription_price"], v["stock_units"], v["stock_capped"])

# Petz prices and stock change during the day. Store each answer with
# fetched_at and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `country`, `currency`, `language` and `note`.

- **search / category / brand / deals** - `query` (search), `category` {`path`, `name`, `url`, `redirected_from`} (category), `brand` {`slug`, `name`, `url`, `redirected_from`} (brand), `deals` {`collection`, `name`, `url`} (deals), `page`, `page_size` (20), `sort`, `total`, `total_capped`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `product_id`, `sku`, `ean`, `name`, `url`, `image`, `brand`, `sub_brand`, `categories`, `price`, `list_price`, `discount_percent`, `subscription_price`, `subscription_discount_percent`, `clubz` {`price`, `tiers`}, `currency`, `available`, `availability`, `stock_units`, `stock_capped`, `has_variations`, `variations[]` {`product_id`, `sku`, `ean`, `name`, `url`, `price`, `list_price`, `discount_percent`, `subscription_price`, `available`, `selected`}}.
- **product** - `product_id`, `sku`, `ean`, `name`, `url`, `brand` {`name`, `slug`}, `sub_brand`, `category`, `categories[]` {`name`, `path`}, `images`, `price`, `list_price`, `discount_percent`, `subscription_price`, `available`, `availability`, `stock_units`, `stock_capped`, `published`, `specs[]` {`name`, `value`}, `rating` {`average`, `count`, `stars`}, `latest_reviews[]` {`date`, `rating`, `text`}, `has_variations`, `variations[]` {`product_id`, `sku`, `name`, `description`, `price`, `list_price`, `discount_percent`, `subscription_price`, `available`, `availability`, `stock_units`, `stock_capped`, `on_promotion`, `is_combo`, `current`, `image`}.
- **stores** - `total`, `state`, `city`, `count`, `stores[]` {`store_id`, `slug`, `name`, `url`, `image`, `address` {`street`, `neighborhood`, `city`, `state`, `cep`}, `phone`, `hours[]` {`days`, `opens`, `closes`, `closed`, `open_24h`}, `pickup`, `service_codes`, `pet_codes`}.
- **store** - `store_id`, `slug`, `name`, `url`, `image`, `google_place_id`, `address`, `phone`, `hours`, `service_codes`, `pet_codes`. `service_codes` and `pet_codes` are Petz's own codes; the store page does not name them.

## Guardrails

- Name it "Petz (petz.com.br, the Brazilian pet store of Grupo Petz Cobasi)" on first mention. Petz accounts, carts, Assinatura Petz sign-ups, Clubz membership and checkout are not read or made.
- Prices: quote `price` with `list_price`, the size (`variations[].name`) and the `fetched_at` date, in BRL (R$). Prices are what a visitor who is not signed in sees.
- Subscription and Clubz: name `subscription_price` as the Assinatura Petz price and `clubz.price` as the Clubz member price, as given. Never compute a discount, a price per kg or an installment.
- Stock: `stock_units` is the online count Petz shows, capped at 100; when `stock_capped` is true say "100 or more units". It is not store stock: never state how many units a store holds or quote a per-store price.
- Totals: when `total_capped` is true, say the search counts at most 1,000 products, not that 1,000 exist.
- Reviews: no reviewer names are returned, only the 3 latest reviews. Quote a review as "a Petz customer review" with its rating and date; never try to identify a reviewer.
- Stores: phone and address are the store's own business contact as the directory lists it. `pickup` says online orders can be picked up there, not that an item is in stock there.
- Comparing Petz with Cobasi, Petco, PetSmart, Chewy or another store: compare the same product, size and date. Never call one store cheaper beyond the numbers shown.
- Use: keep any use descriptive (prices, sizes and stock as facts with their date); do not republish Petz product photos, descriptions or reviews or link to its pages, and refer to products by `product_id`.
- Not available: per-store stock and prices, prices by CEP, more reviews, search suggestions, Pix prices, installments, shipping, deal validity dates, price history (poll and store), account data, cart or checkout. This API cannot buy, subscribe or book a service.
- Terms: Scavio does not store Petz data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. The group privacy policy of Grupo Petz Cobasi limits reproducing site content without written authorization; read the current policy for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, stock, ratings, reviews or store hours. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id or url is required (a Petz product id, e.g. 191628, or its link)."; "product_id must be a Petz product id: 3 to 9 digits, e.g. 191628 (items[].product_id; the number at the end of a product link)."; "url must be a Petz product link: https://www.petz.com.br/produto/<name>-<id>."; "category must be a Petz category path: lowercase slugs joined by /, e.g. cachorro, cachorro/racao or gato/areia-e-banheiros."; "brand must be a Petz brand slug: letters, digits and hyphens, e.g. royal-canin or premierpet."; "collection must be a Petz collection slug as its link shows it, e.g. pf-petz-friday."; "state must be a Brazilian state code (UF), e.g. SP or RJ."; "slug must be a Petz store slug as stores[].slug lists it, e.g. petz-aclimacao."; "sort must be one of: relevance, price_asc, price_desc, newest."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "No Petz product <id>.", "No Petz category at <path>. ...", "No Petz brand page at <slug>. ...", "No Petz collection <slug>. ...", "No Petz store <slug>. Use a slug from the stores endpoint (stores[].slug).". A search with no products is `total` 0 (a `200`), not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=petz-api).
- `502` and `503` mean Petz data was temporarily unavailable ("Petz is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- Listings usually take 50-150 seconds, up to about 245; product, stores and store 30-95 seconds (in the captures 6 to 46 seconds). Allow a client timeout of at least 300 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.105.0
npm install scavio@0.106.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.petz.search({ query: "ração golden", sort: "price_asc" });
const { data: dogFood } = await scavio.petz.category({ category: "cachorro/racao" });
const { data: royalCanin } = await scavio.petz.brand({ brand: "royal-canin" });
const { data: deals } = await scavio.petz.deals({ collection: "PF-racoes" });
const { data: item } = await scavio.petz.product({ product_id: "191628" });
const { data: stores } = await scavio.petz.stores({ state: "SP", city: "São Paulo" });
const { data: store } = await scavio.petz.store({ slug: "petz-aclimacao" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.petz.search(...)`, `category`, `brand`, `deals`, `product`, `stores` and `store`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 7 endpoints as tools: `search_petz`, `get_petz_category`, `get_petz_brand`, `get_petz_deals`, `get_petz_product`, `get_petz_stores` and `get_petz_store`. Petz is opt-in: add `petz` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.105.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,petz"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/petz-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=petz-api), [category](https://scavio.dev/docs/petz-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=petz-api), [brand](https://scavio.dev/docs/petz-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=petz-api), [deals](https://scavio.dev/docs/petz-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=petz-api), [product](https://scavio.dev/docs/petz-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=petz-api), [stores](https://scavio.dev/docs/petz-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=petz-api), [store](https://scavio.dev/docs/petz-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=petz-api). Platform page: [scavio.dev/petz-api](https://scavio.dev/petz-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=petz-api).
