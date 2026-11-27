# Cobasi API - Pet Supply Prices by Size, Compra Programada Subscription, Store Pickup by CEP, Reviews

Read Cobasi (cobasi.com.br, the Brazilian pet store of Grupo Petz Cobasi): keyword search, category and brand listings, the deals page, one product with every size and its subscription price, its reviews and shopper questions, pickup and delivery for one SKU at a CEP, search suggestions, the store directory and one store in full. www.cobasi.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in.

**The job this skill is for: what a pet product costs at Cobasi today, size by size, on subscription, and how a shopper near a CEP can get it.** Cobasi sells most products in several sizes or variants (SKUs), each with its own price, and many of them on Compra Programada, a repeat-delivery subscription with its own price. On 2026-11-27 the Formula Natural Fresh Meat dry food for small adult dogs (`3934097`) read R$ 59.99 against R$ 74.99 (20 percent off) for 1 kg, R$ 123.99 for 2.5 kg and R$ 374.99 for 10.1 kg, R$ 337.49 on Compra Programada, "3x R$ 124.99"; 1 kg to CEP 01310-100 (Avenida Paulista, Sao Paulo) could be picked up free in 45 minutes at 11 stores, or delivered for R$ 7.90 (Econômica, 2 business days) or R$ 9.90 (Cobasi Já, 2 hours).

Seven limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Listings and store pages are slow.** Search, category, brand, deals, product, stores and store usually take 10-90 seconds (deals up to about 90; in the captures 7.9 to 13.9 seconds). Reviews, questions, availability and suggestions usually take 2-6 seconds. Allow a client timeout of at least 240 seconds.
- **20 a page, 50 pages.** Listings return 20 products a page and Cobasi stops paging at page 50 (1,000 products), even when `total` counts more (the deals page counted 1,293). Category `total` is null when the category page does not count its products.
- **Prices are per SKU.** A listing item and a product carry `skus[]`, one per size or variant, each with its own `price`, `list_price` and availability. The item's own `price` is one SKU's; quote the size with the price.
- **Subscription price only where it exists.** `subscription_price` (Compra Programada) is on `/product` only, and only for SKUs with `can_subscribe` true; it is null otherwise.
- **Flags, not units.** `available` and the pickup and delivery answers are yes / no and options with a cost. Cobasi publishes no per-store stock or per-store prices.
- **Not offered:** Pix prices, marketplace sellers (`sold_by` is Cobasi), deal validity dates, reviewer and asker names.

Cobasi has no public API for its catalog, prices or stores. They are shown on cobasi.com.br to any visitor, and this skill reads those public pages with one Scavio key.

See also: Petco `petco-product-data`, PetSmart `petsmart-product-data`, Chewy `chewy-product-data` (pet stores in the US); Mercado Libre `mercadolibre-product-data` (Brazil marketplace); Brazilian retail: Magazine Luiza `magalu-magazine-luiza-api`, Atacadao `atacadao-api`, Carrefour Brasil `carrefour-brasil-api`.

## When to trigger

Use this skill when the user asks to:
- Search Cobasi by keyword (in Portuguese: "ração golden", "areia gato", "arranhador"), sorted by relevance, price or discount
- Filter Cobasi search results by brand, department, category, pet size (porte), age, flavour, colourant or any other facet Cobasi shows, with counts
- List one Cobasi category (`cachorro/racao/racao-seca`) or one brand (`golden`, `premier`, `gran-plus`) by best sellers or price
- Read Cobasi's deals page (Promoções): the deal price next to the regular price and the discount
- Read one Cobasi product: every size with its price, list price, EAN, installments, price per kg, Compra Programada price and frequencies, specs, dimensions and rating
- Compare the price of each size of a pet food (price per kg), or the one-off price against the subscription price
- Read a product's customer reviews or shopper questions with Cobasi's answers
- Check whether a Cobasi store near a CEP can hand over one SKU in 45 minutes, and what delivery to that CEP costs and how long it takes
- List Cobasi stores by state and city, or read one store's hours, phone, WhatsApp link and services (grooming, vet pharmacy)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api) - email or Google, no card required.
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
| `POST /api/v1/cobasi/search` | Keywords: 20 products per page with total and pages, price, list price, discount, availability flag, rating and every SKU with its price; facets with counts to send back as `filters` | 1 |
| `POST /api/v1/cobasi/category` | One category by path, by best sellers or price: the category, its subcategories, the same items and the facet counts | 1 |
| `POST /api/v1/cobasi/brand` | One brand by slug, by best sellers or price: the same items and the facet counts | 1 |
| `POST /api/v1/cobasi/deals` | The deals page (Promoções): products on promotion with the deal price next to the regular price, by relevance, price or discount | 1 |
| `POST /api/v1/cobasi/product` | One product: categories, images, seller, every SKU with EAN, price, list price, subscription price (when it can be subscribed), installments, price per measure, kit flag; subscription frequencies, specs, dimensions, rating summary and 4 recent reviews | 1 |
| `POST /api/v1/cobasi/reviews` | A product's customer reviews, 4 per page, most recent first: date, purchase date, rating, recommends, text; star counts and recommend percent | 1 |
| `POST /api/v1/cobasi/questions` | A product's shopper questions with Cobasi's answers, 4 per page, with the answer date | 1 |
| `POST /api/v1/cobasi/availability` | One SKU at a CEP: the pickup stores that can hand it over (ready time, price, address, coordinates) and the delivery options with cost and estimate | 1 |
| `POST /api/v1/cobasi/suggestions` | Up to 5 search suggestions for the start of a query, and whether Cobasi corrected the spelling | 1 |
| `POST /api/v1/cobasi/stores` | The store directory (about 250 stores) with address, coordinates and services, narrowed by state and city | 1 |
| `POST /api/v1/cobasi/store` | One store: address, coordinates, phone, WhatsApp link, hours per weekday, holiday hours, grooming and vet hours, services | 1 |

Brazil only: there is no `country` parameter. Every product and store answer carries `country` (br), `currency` (BRL) and `language` (pt-BR), and most carry a `note`.

## Prices: price, list price, subscription and installments

| Field | Meaning |
|---|---|
| `price` | The price Cobasi shows now, in BRL (R$ 59.99 for the 1 kg SKU below) |
| `list_price` | The regular price when a lower price applies (R$ 74.99); null when there is no lower price |
| `discount_percent` | The discount against `list_price` (20); null when none |
| `skus[]` | One entry per size or variant (`name` "1 kg", "2,5 kg", "PP"), each with its own price, list price, discount and `available` flag; `best_choice` (listings) marks the SKU the card shows first |
| `subscription_price` (product) | The Compra Programada (repeat delivery) price of a SKU (R$ 337.49 against R$ 374.99); null unless `can_subscribe` is true |
| `subscription.frequencies` (product) | The delivery intervals Compra Programada offers ("1 week" to "32 week", "1 month" to "4 month") |
| `installments` (product) | `{count, amount}`: the card plan Cobasi shows (3 x R$ 124.99) |
| `price_per_measure` (product) | `{unit, price}`: the price per kg (or other unit) as Cobasi shows it (R$ 37.13 / kg on the 10.1 kg bag) |
| `best_value` (product) | Cobasi's own "best value" mark on a SKU |
| `price_valid_until` (product) | The validity date Cobasi attaches to a SKU's price, as given |

- Quote "Formula Natural Fresh Meat small adult dogs, 1 kg: R$ 59.99 (from R$ 74.99, 20 percent off) at cobasi.com.br on 2026-11-27", with the size and the date; add "R$ 337.49 on Compra Programada" only when `subscription_price` is given.
- Report Cobasi's prices and labels and the arithmetic only (for example the per-kg difference between two sizes); never judge a price as a good deal, and never compute an installment or a subscription discount yourself.

## Workflow

1. **Find products.** `/search` with `query` (`ração golden`), `/category` with `category` (`cachorro/racao`), `/brand` with `brand` (`golden`), or `/deals`. Each item's `product_id` is the input of `/product`, `/reviews` and `/questions`; each `skus[].sku_id` is the input of `/availability`.
2. **Narrow a search.** Read `facets[]` and send values back in `filters` exactly as `facets[].values[].value` writes them (`brand/golden`, `porte/racas-pequenas`, `category-1/cachorro`), up to 10. Values of one facet widen the match; different facets narrow it. Category and brand pages return facet labels and counts for reading only; they take no filter.
3. **Next pages.** Send `page` 2, 3, ... up to `total_pages` (at most 50). `has_more` false means the last page.
4. **One product.** `/product` with `product_id` (or `url`): every SKU with EAN, price, list price, installments, price per kg and, when it can be subscribed, the Compra Programada price; plus specs, dimensions and the rating summary. Take subcategory paths for `/category` from `categories[].path`.
5. **What shoppers say.** `/reviews` and `/questions` with the same `product_id`, `page` 1 to `total_pages`, 4 per page.
6. **Getting it near a CEP.** `/availability` with `sku_id`, `cep` and optional `quantity`: the stores near that CEP that can hand it over and the delivery options with their cost.
7. **The stores.** `/stores` with `state` (and `city`) for the directory; `/store` with a `slug` from it for hours, phone, WhatsApp link and services.
8. **Watching prices:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`) and deals (`/deals`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords in Portuguese, 1-200 characters (`ração golden`) |
| `sort` | `relevance` (default), `price_asc`, `price_desc`, `discount_desc` (largest discount first) |
| `page` | 1-50, 20 products per page |
| `filters` (search) | Up to 10 facet values, each exactly as `facets[].values[].value` lists it (`["brand/golden"]`) |

A keyword with no products returns an empty `200` with `total` 0. The deals page takes no filters and returns no facets.

### Category (`/category`) and brand (`/brand`)

| Parameter | Description |
|---|---|
| `category` (category, required) | A category path: a product's `categories[].path`, a category's `subcategories[].path`, or the path after /c/ in a category link (`cachorro`, `cachorro/racao`, `cachorro/racao/racao-seca`) |
| `brand` (brand, required) | A brand slug as its Cobasi link shows it, the part after /m/ (`golden`, `premier`, `gran-plus`) |
| `sort` | `top_selling` (default, ordered by Cobasi's sales), `price_asc`, `price_desc` |
| `page` | 1-50, 20 products per page |

### Product (`/product`), reviews (`/reviews`) and questions (`/questions`)

Send exactly one of `product_id` (5-10 digits, `items[].product_id`, e.g. `3934097`) or `url` (a product link on www.cobasi.com.br ending in `-<product id>/p`). Reviews and questions also take `page` (1-500, 4 per page; `total_pages` reports the last one).

### Availability (`/availability`)

| Parameter | Description |
|---|---|
| `sku_id` (required) | The SKU id (`skus[].sku_id` of a product or a listing item, one size or variant), e.g. `934097` |
| `cep` (required) | The Brazilian CEP (postal code), 8 digits, with or without the hyphen (`01310-100`) |
| `quantity` | Units, 1-10; defaults to 1 |

### Suggestions (`/suggestions`), stores (`/stores`) and store (`/store`)

- `/suggestions` takes `query`, 1-100 characters (`areia gato`).
- `/stores` takes optional `state` (a Brazilian state code, UF, e.g. `SP`) and `city` (accents and case ignored, e.g. `São Paulo`); an empty body `{}` lists every store.
- `/store` takes `slug` (`stores[].slug`, e.g. `cobasi-americana`) or `url` (a Cobasi store link, `www.cobasi.com.br/lojas/<slug>`).

## Examples

### One search item

Request `{"query": "ração golden"}` (1 credit, 13.9 seconds): `total` 237, `total_pages` 12, 20 items, facets for department (Cachorro 217, Gatos 20), category, subcategory (Ração Seca 215, Ração Natural 58), age (Adulto 160, Filhote 65, Sênior 45), colourant and more. The first item:

```json
{
  "position": 1,
  "product_id": "3310549",
  "name": "Ração Golden Special para Cães Adultos Frango e Carne",
  "brand": "Golden",
  "price": 159.99,
  "list_price": null,
  "discount_percent": null,
  "currency": "BRL",
  "available": true,
  "rating": 4.8,
  "skus": [
    { "sku_id": "310549", "name": "15 kg", "price": 159.99, "list_price": null, "discount_percent": null, "available": true, "best_choice": true },
    { "sku_id": "684910", "name": "20 kg", "price": 204.99, "list_price": null, "discount_percent": null, "available": true, "best_choice": false }
  ]
}
```

Each item also carries `url` and `image`. One facet value, ready to send back: `{"value": "category-1/cachorro", "label": "Cachorro", "count": 217, "selected": false}`.

### One product

Request `{"product_id": "3934097"}` (1 credit, 8.8 seconds), abridged to two of its three SKUs:

```json
{
  "product_id": "3934097",
  "name": "Ração Fórmula Natural Fresh Meat Cães Adultos Mini e Pequeno Frango",
  "brand": "Formula Natural",
  "categories": [{ "name": "Cachorro", "path": "cachorro" }, { "name": "Ração", "path": "cachorro/racao" }, { "name": "Ração Seca", "path": "cachorro/racao/racao-seca" }],
  "available": true,
  "sold_by": "Cobasi",
  "main_sku_id": "934097",
  "skus": [
    { "sku_id": "934097", "name": "1 kg", "ean": "7898363314581", "available": true, "price": 59.99, "list_price": 74.99, "discount_percent": 20, "subscription_price": 59.99, "can_subscribe": true, "installments": { "count": 1, "amount": 59.99 }, "price_per_measure": { "unit": "kg", "price": 59.99 }, "best_value": false, "is_kit": false },
    { "sku_id": "1183907", "name": "10,1kg pac. Indiv. de 505g", "ean": "7898752403704", "available": true, "price": 374.99, "list_price": null, "discount_percent": null, "subscription_price": 337.49, "can_subscribe": true, "installments": { "count": 3, "amount": 124.99 }, "price_per_measure": { "unit": "kg", "price": 37.13 }, "best_value": true, "is_kit": false }
  ],
  "dimensions": { "sku_id": "934097", "height_cm": 11, "width_cm": 18, "length_cm": 31, "weight_g": 1100 },
  "rating": { "average": 4.9, "total": 669, "stars": { "1": 7, "2": 2, "3": 7, "4": 34, "5": 619 }, "recommend_percent": 98.65 }
}
```

The product also carried 5 images, `brand_id`, `subscription.frequencies` (24 intervals, "1 week" to "4 month"), 12 `specs` (Porte: Raças Minis, Raças Pequenas; Tipo da Ração: Super Premium Natural; Sabor da Ração: Alecrim, Frango, Mandioca) and 4 `latest_reviews`.

### Pickup and delivery at a CEP

Request `{"sku_id": "934097", "cep": "01310-100"}` (1 credit, 5.4 seconds), abridged to one of 11 stores:

```json
{
  "sku_id": "934097",
  "cep": "01310100",
  "quantity": 1,
  "pickup": {
    "available": true,
    "ready_in": "45 minutos",
    "store_count": 11,
    "stores": [
      { "store_code": "123tut", "name": "Loja Cobasi Tutoia", "ready_in": "45 minutos", "price": 0, "address": { "street": "Rua Tutóia", "number": "484", "complement": null, "neighborhood": "Paraíso", "city": "São Paulo", "state": "SP", "cep": "04007002" }, "latitude": -23.5748839, "longitude": -46.6509788 }
    ]
  },
  "delivery_available": true,
  "delivery": [
    { "option_id": "Econômica1", "name": "Econômica", "price": 7.9, "free": false, "estimate": "2 dias úteis" },
    { "option_id": "Cobasi Já", "name": "Cobasi Já", "price": 9.9, "free": false, "estimate": "2 horas" }
  ]
}
```

`store_code` is the pickup point code, not the `slug` of `/store`; match a pickup store to the directory by name or address.

### Reviews, questions, deals, stores and suggestions

- `/reviews` `{"product_id": "3767590"}` (1.4 seconds): `total` 1742, `total_pages` 436, `average_rating` 4.8, `stars` {5: 1550, 4: 122, 3: 26, 2: 11, 1: 33}, `recommend_percent` 97.47; each review {`date`, `purchase_date`, `rating`, `recommends`, `text`}, e.g. `{"date": "2025-12-28", "purchase_date": "2025-12-28", "rating": 5, "recommends": true, "text": "excelente produto, é ótimo e dura por 8 meses"}`. No reviewer names.
- `/questions` `{"product_id": "3767590"}`: `total` 133, `total_pages` 34; each {`question_id`, `question`, `answer`, `answered_at`}, e.g. "Qual data de validade do produto?" answered on 2023-11-14 that the minimum shelf life Cobasi works with is 6 months.
- `/deals` `{}` (7.9 seconds): `total` 1293, `total_pages` 50; first a Royal Canin food for senior sterilised cats, 4 kg R$ 221.99 against R$ 364.99 (39 percent), 400 g R$ 38.99 against R$ 43.99.
- `/category` `{"category": "cachorro/racao"}`: the category Ração (`has_children` true), 4 subcategories (Ração Seca, Ração Úmida, Ração Medicamentosa, Ração Natural), `total` null, first a GranPlus Gourmet wet food sachet, 100 g, R$ 3.49.
- `/brand` `{"brand": "golden"}`: `total` 67, `total_pages` 4, first Golden Formula small-breed adult dogs Mini Bits, 1 kg R$ 22.99 to 15 kg R$ 179.99.
- `/stores` `{"state": "SP"}`: `total` 253 stores, 149 in SP, each with `store_id`, `slug`, address, coordinates and services ("Retire na loja em até 45 minutos", "Farmácia Veterinária", "Banho & Tosa").
- `/store` `{"slug": "cobasi-americana"}`: Pet Shop Cobasi Americana, Avenida Brasil 1585, Americana SP, open 08:00-21:45 Monday to Saturday and 09:00-19:45 on Sunday and holidays, `online_scheduling` true, a WhatsApp link, `phone` null.
- `/suggestions` `{"query": "areia gato"}`: areia gato, areia gatos, areia higiênica gatos, areia, pá areia gato; `misspelled` false.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def cobasi(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/cobasi/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Golden dog food, cheapest first, narrowed to dogs (1 credit)
hits = cobasi("search", {"query": "ração golden", "sort": "price_asc", "filters": ["category-1/cachorro"]})["data"]
for it in hits["items"][:5]:
    print(it["name"], [(s["name"], s["price"]) for s in it["skus"]])

# 2. One product: every size, with the Compra Programada price where it exists (1 credit)
item = cobasi("product", {"product_id": "3934097"})["data"]
for s in item["skus"]:
    print(s["name"], s["price"], s["list_price"], s["subscription_price"], s["price_per_measure"])

# 3. Pickup and delivery for one size at a CEP (1 credit)
where = cobasi("availability", {"sku_id": item["skus"][0]["sku_id"], "cep": "01310-100"})["data"]
print(where["pickup"]["store_count"], [(d["name"], d["price"], d["estimate"]) for d in where["delivery"]])

# Cobasi prices change. Store each answer with fetched_at and run this on a
# schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }` (`response_time` in milliseconds). Each call fetches the page when the request asks for it.

- **search / deals** - `query` (search), `deals` {`name`, `url`} (deals), `country`, `currency`, `language`, `page`, `page_size` (20), `sort`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `product_id`, `name`, `url`, `image`, `brand`, `price`, `list_price`, `discount_percent`, `currency`, `available`, `rating`, `skus[]` {`sku_id`, `name`, `price`, `list_price`, `discount_percent`, `available`, `best_choice`}}, `facets[]` {`key`, `label`, `values[]` {`value`, `label`, `count`, `selected`}} and `filters_applied` (search only), `note`.
- **category / brand** - `category` {`category_id`, `name`, `path`, `has_children`}, `url` and `subcategories[]` {`category_id`, `name`, `path`, `has_children`} (category); `brand` {`slug`, `name`, `url`} (brand); then `page`, `page_size`, `sort`, `total` (null when not counted), `total_pages`, `has_more`, `count`, `items[]` (the listing fields above), `facets[]` {`label`, `values[]` {`label`, `count`}}, `note`.
- **product** - `product_id`, `name`, `url`, `brand`, `brand_id`, `categories[]` {`name`, `path`}, `images[]`, `available`, `sold_by`, `main_sku_id`, `skus[]` {`sku_id`, `name`, `ean`, `available`, `price`, `list_price`, `discount_percent`, `subscription_price`, `can_subscribe`, `installments` {`count`, `amount`}, `price_per_measure` {`unit`, `price`}, `best_value`, `is_kit`, `price_valid_until`}, `subscription` {`frequencies`} (when the product can be subscribed), `specs[]` {`name`, `values`}, `dimensions` {`sku_id`, `height_cm`, `width_cm`, `length_cm`, `weight_g`}, `rating` {`average`, `total`, `stars`, `recommend_percent`}, `latest_reviews[]` (the review fields below), `note`.
- **reviews** - `product_id`, `page`, `page_size` (4), `sort` (recent), `total`, `total_pages`, `has_more`, `average_rating`, `stars` {1-5 counts}, `recommend_percent`, `count`, `reviews[]` {`date`, `purchase_date`, `rating`, `recommends`, `text`}, `note`.
- **questions** - `product_id`, `page`, `page_size` (4), `total`, `total_pages`, `has_more`, `count`, `questions[]` {`question_id`, `question`, `answer`, `answered_at`}, `note`.
- **availability** - `sku_id`, `cep`, `quantity`, `pickup` {`available`, `ready_in`, `store_count`, `stores[]` {`store_code`, `name`, `ready_in`, `price`, `address` {`street`, `number`, `complement`, `neighborhood`, `city`, `state`, `cep`}, `latitude`, `longitude`}}, `delivery_available`, `delivery[]` {`option_id`, `name`, `price`, `free`, `estimate`}, `note`.
- **suggestions** - `query`, `misspelled`, `count`, `suggestions[]` (strings).
- **stores** - `total` (every store), `state`, `city`, `count`, `stores[]` {`store_id`, `slug`, `name`, `url`, `address` {`street`, `number`, `neighborhood`, `city`, `state`, `cep`}, `latitude`, `longitude`, `services[]`}, `note`.
- **store** - `slug`, `name`, `url`, `address`, `latitude`, `longitude`, `phone`, `whatsapp`, `hours[]` {`day`, `opens`, `closes`}, `holiday_hours` {`opens`, `closes`}, `grooming_hours`, `vet_hours`, `services[]`, `pet_services[]`, `online_scheduling`, `note`.

## Guardrails

- Name it "Cobasi (cobasi.com.br, the Brazilian pet store of Grupo Petz Cobasi)" on first mention. Cobasi accounts, carts, Compra Programada sign-ups and checkout are not read or made.
- Prices: quote `price` with `list_price`, the SKU `name` (size) and the `fetched_at` date, in BRL (R$). Prices are what a visitor who is not signed in sees.
- Subscription: quote `subscription_price` only when it is given (`can_subscribe` true), and name it as the Compra Programada price. Never assume a product without it can be subscribed.
- Installments: quote `installments` as given. Never compute an installment or apply a coupon.
- Availability: `available`, pickup and delivery are flags and options, not unit counts. Never state how many units a store holds, and never quote a per-store price: Cobasi publishes neither.
- Not offered: Pix prices, marketplace sellers, per-store prices or stock, deal validity dates, price history (poll and store), account data, cart or checkout. This API cannot buy, subscribe or book grooming.
- Reviews and questions: no reviewer or asker names are returned. Quote a review as "a Cobasi customer review" with its rating and date; never try to identify a reviewer or asker.
- Stores: phone and WhatsApp link are the store's own business contact as its page lists it.
- Comparing Cobasi with Petco, PetSmart, Chewy or a Brazilian retailer: compare the same product, size and date. Never call one store cheaper beyond the numbers shown.
- Copy and images: do not republish product photos, descriptions, reviews or answers; refer to products by `product_id` and keep any summary descriptive.
- Terms: Scavio does not store Cobasi data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Cobasi's group privacy policy limits reproducing site content without written authorization; read the current policy for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, products, ratings, reviews or store hours. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id or url is required (a Cobasi product id, e.g. 3934097, or its link)."; "product_id must be a Cobasi product id: 5 to 10 digits, e.g. 3934097 ..."; "url must be a Cobasi product link: https://www.cobasi.com.br/<name>-<id>/p."; "sku_id must be a Cobasi SKU id: digits, e.g. 934097 ..."; "cep must be a Brazilian CEP: 8 digits, e.g. 01310-100 or 01310100."; "category must be a Cobasi category path: lowercase slugs joined by /, e.g. cachorro or cachorro/racao/racao-seca."; "brand must be a Cobasi brand slug: letters, digits and hyphens, e.g. golden or gran-plus."; "slug is required: a Cobasi store slug, e.g. cobasi-americana (stores[].slug)."; "state must be a Brazilian state code (UF), e.g. SP or RJ."; "filters: at most 10 values."; "sort must be one of: ...".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "No Cobasi product <id>.", "No Cobasi SKU <id>.", "No Cobasi category at <path>. ...", "No Cobasi brand page at <slug>. ...", "No Cobasi store <slug>. ...", "The Cobasi deals page lists no products right now.". A search with no products is an empty `200`, not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api).
- `502` and `503` mean Cobasi data was temporarily unavailable ("Cobasi is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.104.0
npm install scavio@0.105.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.cobasi.search({ query: "ração golden", sort: "price_asc", filters: ["brand/golden"] });
const { data: dryFood } = await scavio.cobasi.category({ category: "cachorro/racao/racao-seca", sort: "top_selling" });
const { data: golden } = await scavio.cobasi.brand({ brand: "golden" });
const { data: deals } = await scavio.cobasi.deals({ sort: "discount_desc" });
const { data: item } = await scavio.cobasi.product({ product_id: "3934097" });
const { data: reviews } = await scavio.cobasi.reviews({ product_id: "3934097", page: 1 });
const { data: questions } = await scavio.cobasi.questions({ product_id: "3934097" });
const { data: where } = await scavio.cobasi.availability({ sku_id: "934097", cep: "01310-100", quantity: 1 });
const { data: typed } = await scavio.cobasi.suggestions({ query: "areia gato" });
const { data: stores } = await scavio.cobasi.stores({ state: "SP", city: "São Paulo" });
const { data: store } = await scavio.cobasi.store({ slug: "cobasi-americana" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.cobasi.search(...)`, `category`, `brand`, `deals`, `product`, `reviews`, `questions`, `availability`, `suggestions`, `stores` and `store`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `search_cobasi`, `get_cobasi_category`, `get_cobasi_brand`, `get_cobasi_deals`, `get_cobasi_product`, `get_cobasi_reviews`, `get_cobasi_questions`, `get_cobasi_availability`, `get_cobasi_suggestions`, `get_cobasi_stores` and `get_cobasi_store`. Cobasi is opt-in: add `cobasi` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.104.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,cobasi"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/cobasi-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api), [category](https://scavio.dev/docs/cobasi-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api), [brand](https://scavio.dev/docs/cobasi-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api), [deals](https://scavio.dev/docs/cobasi-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api), [product](https://scavio.dev/docs/cobasi-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api), [reviews](https://scavio.dev/docs/cobasi-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api), [questions](https://scavio.dev/docs/cobasi-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api), [availability](https://scavio.dev/docs/cobasi-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api), [suggestions](https://scavio.dev/docs/cobasi-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api), [stores](https://scavio.dev/docs/cobasi-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api), [store](https://scavio.dev/docs/cobasi-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api). Platform page: [scavio.dev/cobasi-api](https://scavio.dev/cobasi-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=cobasi-api).
