---
name: carrefour-brasil-api
description: "Carrefour Brasil API for Carrefour Brasil (carrefour.com.br: the Mercado grocery site mercado.carrefour.com.br and the www site for non-food and the marketplace, through a site param; Brazil only, BRL, Portuguese text) - what a grocery item costs at Carrefour Brasil today in a region or at a pickup store, what a non-food item costs and who sells it, what a payment offer takes off, and what delivery or pickup to a CEP costs and when, as the site shows it to a visitor who is not signed in (on 2026-11-27 Arroz Branco Longo-fino Tipo 1 Tio Joao 1 Kg read R$ 6.59 at the site's default prices, R$ 4.61 with a 30 percent payment offer, delivery to a CEP on Avenida Paulista R$ 10.90 and free Click & Retire pickup at a hypermarket 1.15 km away; the arroz search priced for that CEP opened with a Seara 300g dish at R$ 12.49 against R$ 24.99; the coupon page held 4 codes, among them R$ 20 off above R$ 199) with price, list price, single-payment price, discount, availability flag, seller, stamps and sponsored placements kept apart; keyword or EAN search, category listings and collections (themed and deal lists), 15 a page to page 50, in the site's 8 sorts and filtered by any facet and a price range, priced for a CEP or a pickup store on Mercado; one product with every seller, payment offers, promotions, price per kg for items sold by weight, specs and variants; delivery and pickup options to a CEP; the pickup stores by state and city; search suggestions with the top searches; the coupon page; the department menu. 9 endpoints, 1 credit each. No stock units, reviews or price history."
version: 1.0.0
tags: carrefour-brasil, carrefour-brazil, carrefour-com-br, carrefour-brasil-api, carrefour-mercado, mercado-carrefour, carrefour-supermercado, carrefour-hipermercado, carrefour-precos, carrefour-prices, carrefour-regional-prices, carrefour-cep, carrefour-marketplace, carrefour-sellers, carrefour-coupons, carrefour-cupom, carrefour-ofertas, carrefour-black-friday, carrefour-delivery, carrefour-frete, carrefour-retire-na-loja, click-e-retire, carrefour-stores, carrefour-lojas, carrefour-collections, carrefour-search, carrefour-ean, carrefour-categories, carrefour-suggestions, grupo-carrefour-brasil, grocery-prices, supermarket-prices, brazil-grocery, mercado-online, preco-por-kg, cep, pix, brazil, brazil-ecommerce, brazilian-retail, brl, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 150
    throttle: 1
    homepage: https://scavio.dev/carrefourbr-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api
---

# Carrefour Brasil API - Regional Grocery Prices by CEP, Marketplace, Coupons, Delivery

Read Carrefour Brasil (carrefour.com.br: Mercado grocery + the www marketplace): keyword or EAN search, category listings and collections priced for a region or a pickup store, one product with every seller and payment offer, delivery and pickup options to a CEP, the pickup stores, search suggestions, the coupon page and the department menu. One `site` param picks mercado.carrefour.com.br (`mercado`, the default, grocery) or www.carrefour.com.br (`www`, non-food and the marketplace). Brazil only, BRL, Portuguese text, as shown to a visitor who is not signed in. This is not Carrefour France: for carrefour.fr use `carrefour-api`.

**The job this skill is for: what an item costs at Carrefour Brasil today, for a region, and what delivery or pickup takes.** On Mercado, prices and assortment change by region: send a `cep` (or a pickup store's `store`) and the answer is priced for it (`price_scope` regional); without one, the answer is the site's default prices (`price_scope` national). On 2026-11-27 Arroz Branco Longo-fino Tipo 1 Tio Joao 1 Kg (item `1972`, EAN `7893500020110`) read R$ 6.59 at the default prices, with a 30 percent payment offer giving R$ 4.61; delivery to CEP 01310-100 (Avenida Paulista) cost R$ 10.90 and pickup at Hipermercado Pamplona, 1.15 km away, was free the same day.

Seven limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Regional prices on Mercado only.** `cep` or `store` apply to `site` mercado. `www` prices are national; there the CEP changes shipping and nothing else (`/delivery`). Say whether a price is regional (with the region) or national.
- **15 a page, 50 pages.** Search, category and collection return 15 items a page, up to page 50. Sponsored placements come in `sponsored[]`, kept apart from `items[]`.
- **Price layers as given.** `price` is the offer the site shows, `list_price` the regular price, `spot_price` the single-payment (a vista) price. Payment-offer prices (`payment_offers[].price`) and weighed item prices are computed by Scavio from the site's percentage and weight, and are labelled so.
- **Availability is a flag.** `available` is a yes / no from the site's offer; Carrefour Brasil publishes no unit counts.
- **Delivery is a quote, not a reservation.** `/delivery` returns the site's options for one unit of one item from one seller to a CEP; it does not reserve stock.
- **No history and no reviews.** Everything is the page at the moment of the call; Scavio keeps nothing. The site carries no reviews or questions. Poll and store your own series.

Carrefour Brasil has no public API for its catalog, prices or delivery. They are shown on carrefour.com.br to any visitor, and this skill reads those public pages with one Scavio key.

See also: Atacadao `atacadao-api` (the cash-and-carry chain of the same group, prices per store and quantity tier), Carrefour France `carrefour-api`, Mercado Libre `mercadolibre-product-data` (Brazil marketplace); Brazilian retail: Magazine Luiza `magalu-magazine-luiza-api`, Casas Bahia `casas-bahia-api`, Buscape + Zoom `buscape-zoom-api` (price comparison).

## When to trigger

Use this skill when the user asks to:
- Price a grocery item at Carrefour Brasil (Carrefour Mercado) for a CEP or a pickup store: price, list price, single-payment price, discount, stamps
- Search carrefour.com.br by keyword (in Portuguese: "arroz", "cafe", "geladeira") or by EAN barcode, sorted by relevance, best selling, price, newest, discount or name, filtered by department, category, brand, seller or any listed attribute and a price range
- Browse one Carrefour Brasil category by its path (`/categoria/mercearia/alimentos-basicos/arroz`) or one collection (a themed or deal list, `/colecao/<id>`)
- Read one Carrefour Brasil product: every seller with its price, payment offers (a card or Pix price), promotions, price per kg for items sold by weight, specs, variants
- See which marketplace sellers offer a non-food item on www.carrefour.com.br and at what price
- Quote delivery and pickup for one item to a Brazilian CEP: options, cost, estimate, the nearest pickup stores with their hours
- List the Carrefour pickup stores (Retire na Loja) in a state or city
- Read the site's coupon codes, search suggestions, top searches or department menu

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Mercado calls usually take 2-25 seconds and www calls up to about 50 seconds (in the captures, all on Mercado: product 1.3, delivery 1.5, coupons 2.0, categories 3.2, category 3.6, stores 3.8, suggestions 6.2, search 6.6, collection 10.3). Allow a client timeout of at least 120 seconds.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/carrefourbr/search` | Keywords or an EAN: 15 items a page with price, list price, single-payment price, discount, availability flag, seller, seller count, stamps; sponsored placements apart; facets; the site's related terms | 1 |
| `POST /api/v1/carrefourbr/category` | One category by path or link, with its breadcrumbs, same items, sorts, filters and facets as search | 1 |
| `POST /api/v1/carrefourbr/collection` | One collection (a themed or deal list, `/colecao/<id>`) by id or link, same items, sorts, filters and facets | 1 |
| `POST /api/v1/carrefourbr/product` | One product by item id or link: EAN, every seller with price and payment offers, promotions, stamps, price per kg for items sold by weight, availability flag, description, specs, variants, images | 1 |
| `POST /api/v1/carrefourbr/delivery` | Delivery and pickup options for one item from one seller to a CEP: cost, estimate, earliest date, scheduled flag, and the pickup stores near the CEP with their hours | 1 |
| `POST /api/v1/carrefourbr/stores` | The Carrefour pickup stores (Retire na Loja) by state and city, with the `store_id` that prices Mercado for that store | 1 |
| `POST /api/v1/carrefourbr/suggestions` | The site's search suggestions as you type, the suggested products, and the top searches with their counts | 1 |
| `POST /api/v1/carrefourbr/coupons` | The site's coupon page: code, value, name, expiry, the list a coupon applies to, rules | 1 |
| `POST /api/v1/carrefourbr/categories` | The site's department menu, 3 levels, with the inputs of category, collection and filters | 1 |

Every answer carries `site`, `store` (Carrefour Mercado or the www name), `host`, `country` (br), `currency` (BRL) and `language` (pt-BR), and most carry `notes`.

## Prices: price, list price, single-payment price and payment offers

| Field | Meaning |
|---|---|
| `price` | The offer the site shows, in BRL, from `seller` (R$ 12.49 on the Seara 300g dish for CEP 01310-100) |
| `list_price` | The regular price (R$ 24.99) |
| `spot_price` | The site's single-payment (a vista) price |
| `discount_percent` | The site's discount against the list price (50); 0 when none |
| `stamps[]` | The site's promotion stamps as written, `{text, type, image}` ("30% DESC OFF") |
| `measurement_unit` | `un`, or `kg` for items priced per kg (the Seara Fiesta chicken at R$ 37.48 per kg) |
| `payment_offers[]` (product) | `{name, payment_method_id, discount_percent, price}`: the site's price for one payment method, such as the Carrefour card or Pix (Brazil's instant payment); `price` is computed by Scavio from the site's percentage (30 percent: R$ 4.61) |
| `promotions[]` (product) | Other site offers (quantity offers and similar) with their conditions and effects as given |
| `weight` (product) | For items sold by weight: `unit_multiplier`, `price_per_kg` and `item_price` (computed by Scavio) |
| `price_valid_until` (product) | The validity the site gives the price |
| `region`, `price_scope` | The region the answer is priced for (`cep`, `store_id`, `store`, `delivery_type`, `address`) and `regional` or `national` |

- Quote "Arroz Branco Longo-fino Tipo 1 Tio Joao 1 Kg: R$ 6.59, sold by Carrefour, at the default (national) prices of mercado.carrefour.com.br on 2026-11-27", with the seller, the region or national scope and the date. Say a payment-offer price is Scavio's computation from the site's percentage, and for which payment method.
- Report Carrefour Brasil's prices, stamps and dates and the arithmetic only. Never judge a price as a good deal.

## Workflow

1. **Set the region (Mercado).** Send `cep` (`01310-100`) for that region's prices and assortment, or `store` (a `store_id` from `/stores`) for a pickup store's. Check `price_scope` and `region` in the answer.
2. **Find the item.** `/search` with `query` (keywords or an EAN), `/category` with a `path` from `/categories` or a list's breadcrumbs, or `/collection` with a `collection_id` (from `/coupons`, `/categories` or a `/colecao/` link). Each item's `item_id` is the input of `/product` and `/delivery`.
3. **Narrow.** Send any `facets[].values[].filter` back in `filters` (`{"brand": "consul"}`), up to 10 values, plus `min_price` / `max_price` in whole reais. Values of one key combine as any of them.
4. **One product.** `/product` with `item_id` (or `url`), with the same `cep` or `store`: every seller, payment offers, promotions, weight pricing, specs and variants (each variant is its own `item_id`).
5. **Delivery and pickup.** `/delivery` with `item_id`, a `cep`, and `seller_id` for a marketplace item on www (default 1, Carrefour itself): options with cost and estimate, and the pickup stores near the CEP with their hours.
6. **Coupons and lists.** `/coupons` for the current codes; a coupon's `collection_id` is the list it applies to, readable with `/collection`.
7. **Watching prices:** there is no history. Poll the same items in the same region on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`) and collection (`/collection`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords in Portuguese, or an EAN barcode, 1-120 characters |
| `path` (category, required) | A category path (`/categoria/mercearia/alimentos-basicos/arroz`, from `/categories` `departments[].path` or a list's `breadcrumbs`) or such a link |
| `collection_id` (collection, required) | A collection id (`29861`, the number in a `/colecao/<id>` link, `coupons[].collection_id`, `/categories` `collection_id`) or such a link |
| `site` | `mercado` (default, mercado.carrefour.com.br) or `www` (www.carrefour.com.br) |
| `cep` | On mercado: a CEP (Brazilian postal code, 8 digits, dash optional) for that region's prices and assortment |
| `store` | On mercado, instead of `cep`: a pickup store's `store_id` from `/stores` (8 digits, e.g. `01405002`) |
| `sort` | `relevance` (default), `orders_desc` (best selling), `price_asc`, `price_desc`, `release_desc` (newest), `discount_desc`, `name_asc`, `name_desc` |
| `filters` | Facet filters from a previous answer's `facets[].values[].filter` (`{"brand": "consul"}`, `{"category-2": ["geladeira"]}`), or `"key=value"` strings; up to 10 values |
| `min_price`, `max_price` | Price range in whole reais (BRL) |
| `page` | 1-50 (15 items a page) |

A search with no items returns an empty `200`. A category link or collection link on one host must be sent with that host's `site`.

### Product (`/product`) and delivery (`/delivery`)

| Parameter | Description |
|---|---|
| `item_id` (product: or `url`; delivery: required) | The item id (`items[].item_id`, or the number at the end of a `/produto/` link), e.g. `1972` |
| `url` (product) | A product link on either site (`/produto/<name>-<item id>`, or an older `/<name>/p` link) |
| `site` | `mercado` (default) or `www` |
| `cep`, `store` (product) | As above: the region the product is priced for, on mercado |
| `cep` (delivery, required) | The delivery CEP, e.g. `01310-100` |
| `seller_id` (delivery) | The seller (`sellers[].seller_id` from `/product`). Default 1, Carrefour itself; marketplace items on www need their seller's id |

### Stores (`/stores`), suggestions (`/suggestions`), coupons (`/coupons`) and categories (`/categories`)

| Parameter | Description |
|---|---|
| `state` (stores) | A two-letter state code (UF), e.g. `SP` |
| `city` (stores) | A city (accents and case ignored), e.g. `Porto Alegre` |
| `query` (suggestions) | What a shopper has typed, 1-80 characters; without it, the top searches alone |
| `site` (suggestions, coupons, categories) | `mercado` (default) or `www` |

## Examples

### One search item priced for a CEP

Request `{"query": "arroz", "cep": "01310-100"}` (1 credit): `region` {`cep` 01310-100, `delivery_type` residential, `address` "Avenida Paulista, Bela Vista - São Paulo"}, `price_scope` regional, `total` 43, `total_pages` 3, 15 items, `suggestions` [arroz, arroz marca carrefour 5 kg, arroz 1 kilo, ...], facets Departamento, Categoria, Subcategoria, Marca and "Vendido e Entregue por:". The first item:

```json
{
  "position": 1,
  "product_id": "332574426",
  "item_id": "332590446",
  "name": "Arroz Carreteiro Na Panelinha Seara 300g",
  "brand": "Seara",
  "product_reference": "3496520",
  "categories": [["Congelados", "Pratos Prontos"], ["Congelados"]],
  "measurement_unit": "un",
  "price": 12.49,
  "list_price": 24.99,
  "spot_price": 12.49,
  "discount_percent": 50,
  "available": true,
  "seller": { "seller_id": "1", "name": "Carrefour" },
  "seller_count": 1,
  "variant_count": 1,
  "stamps": [],
  "sponsored": false,
  "international": false
}
```

Arroz Tipo 1 Seletto Tradicional 5kg read R$ 16.99 with the stamp "30% DESC OFF". One facet value: `{"name": "Mercearia", "value": "mercearia", "count": 40, "selected": false, "filter": {"category-1": "mercearia"}}`.

### One product with a payment offer

Request `{"item_id": "1972"}` (1 credit, default prices), abridged:

```json
{
  "item_id": "1972",
  "product_id": "1970",
  "name": "Arroz Branco Longo-fino Tipo 1 Tio João 1 Kg",
  "brand": "Tio João",
  "ean": "7893500020110",
  "measurement_unit": "un",
  "price": 6.59,
  "list_price": 6.59,
  "spot_price": 6.59,
  "discount_percent": 0,
  "available": true,
  "price_valid_until": "2027-11-27T18:24:43Z",
  "seller": { "seller_id": "1", "name": "Carrefour" },
  "payment_offers": [
    { "name": "FOODIN_CARTAO_CRF_ARROZ_30OFF", "minimum_quantity": null, "discount_percent": 30, "effects": { "PercentualDiscount": "30" }, "payment_method_id": "401", "price": 4.61 }
  ],
  "promotions": [],
  "dual_price": null,
  "weight": null,
  "price_scope": "national"
}
```

It also carried one seller in `sellers[]` (Carrefour, default), the breadcrumbs Mercearia > Alimentos Básicos > Arroz, a description, 4 specs and 1 image. `payment_offers[].name` is the site's own name for the offer, as given.

### Delivery and pickup to a CEP

Request `{"item_id": "1972", "cep": "01310-100"}` (1 credit): `address` {Avenida Paulista, Bela Vista, São Paulo, SP}, `can_deliver` true, `out_of_stock_for_region` false, 2 options (abridged):

```json
[
  { "group": "Entrega Normal", "name": "Normal", "channel": "delivery", "price": 10.9, "list_price": 10.9, "estimate": "2h", "earliest_date": { "day_of_week": "Amanhã", "day": "28", "month": "11", "month_name": "novembro" }, "scheduled": true, "pickup_store": null },
  { "group": "Retirar na loja com agendamento", "channel": "pickup-in-point", "price": 0, "list_price": 0, "estimate": "2h", "earliest_date": { "day_of_week": "Hoje", "day": "27", "month": "11", "month_name": "novembro" }, "scheduled": true, "pickup_store": { "name": "HIPERMERCADO PAMPLONA", "distance_km": 1.15, "opening_hours": ["Seg a Dom: 08:00h até 22:00h"] } }
]
```

Each pickup store also carries `pickup_point_id` and `address` {`street`, `number`, `neighborhood`, `city`, `state`, `cep`}.

### Category, collection, stores, suggestions, coupons and categories

- `/category` `{"path": "/categoria/mercearia/alimentos-basicos/arroz", "sort": "orders_desc"}`: `category` {`category_id` 3620, `name` Arroz, `title` "Arroz: branco, integral, japonês e mais"}, `price_scope` national, `total` 100 over 7 pages, first Arroz Branco Camil Tipo 1 5kg at R$ 23.99.
- `/collection` `{"collection_id": "29861"}`: `collection` {`collection_id` 29861, `name` FOODIN_FIXO_NATAL (the site's internal name)}, `total` 94, first a Seara Fiesta seasoned frozen chicken priced per kg (`measurement_unit` kg) at R$ 37.48.
- `/stores` `{"state": "SP"}`: 68 pickup stores in SP (of 135), each {`store_id`, `name`, `street`, `neighborhood`, `city`, `state`, `cep`}, Hiper Tamboré (Barueri, `store_id` 06460930) first; one had `store_id` null.
- `/suggestions` `{"query": "arroz"}`: 5 terms (arroz, pointing to Mercearia > Alimentos Básicos > Arroz; arroz marca carrefour 5 kg; ...), 24 suggested products, `top_searches` leite (21,115), arroz (17,492), carrefour (13,871), panetone, cafe, ... (10).
- `/coupons` `{}`: 4 coupons, e.g. BLACK10OFF "10% OFF em compras acima de R$499 - Limitado a R$2.000" (expires 2026-11-27) and CASALIMPA20 "R$20 OFF em compras acima de R$199" (expires 2027-12-30, `collection_id` 24365), each with its rules.
- `/categories` `{}`: 15 departments and 673 nodes on Mercado (Bebidas, Mercearia, Hortifruti, Limpeza, Pet Care, ...); some entries link to other pages or to the www site (`site` says which).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def carrefourbr(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/carrefourbr/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()

# 1. Rice priced for a CEP in Sao Paulo, best selling first (1 credit)
hits = carrefourbr("search", {"query": "arroz", "cep": "01310-100", "sort": "orders_desc"})["data"]
print(hits["price_scope"], hits["region"])
for it in hits["items"]:
    print(it["name"], it["price"], it["list_price"], it["spot_price"], it["seller"]["name"])

# 2. One product for the same CEP, with its payment offers (1 credit)
p = carrefourbr("product", {"item_id": hits["items"][0]["item_id"], "cep": "01310-100"})["data"]
for po in p["payment_offers"]:
    print(po["name"], po["discount_percent"], po["price"])

# 3. Delivery and pickup to that CEP (1 credit)
d = carrefourbr("delivery", {"item_id": p["item_id"], "cep": "01310-100"})["data"]
for o in d["options"]:
    print(o["name"], o["channel"], o["price"], o["estimate"])

# Carrefour Brasil prices change by region and by day. Store each answer with
# fetched_at and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `site`, `store`, `host`, `country`, `currency` and `language`.

- **search / category / collection** - `query` and `suggestions` (search), `category` {`path`, `category_id`, `name`, `title`, `page_type`, `breadcrumbs`} (category), `collection` {`collection_id`, `name`} (collection), `filters`, `min_price`, `max_price`, `region`, `price_scope`, `total`, `page`, `page_size` (15), `total_pages`, `sort`, `count`, `items[]` {`position`, `product_id`, `item_id`, `name`, `brand`, `product_reference`, `url`, `categories`, `measurement_unit`, `price`, `list_price`, `spot_price`, `discount_percent`, `available`, `seller` {`seller_id`, `name`}, `seller_count`, `variant_count`, `stamps[]`, `image`, `sponsored`, `international`}, `sponsored_count`, `sponsored[]` (same fields plus `placement`), `facets[]` {`key`, `name`, `type`, `values[]` {`name`, `value`, `count`, `selected`, `filter`} or `ranges[]` {`from`, `to`, `count`} for price}, `notes`.
- **product** - `requested`, `item_id`, `product_id`, `name`, `brand`, `ean`, `product_reference`, `url`, `categories`, `breadcrumbs`, `measurement_unit`, `unit_multiplier`, `price`, `list_price`, `spot_price`, `discount_percent`, `available`, `price_valid_until`, `seller`, `sellers[]` {`seller_id`, `name`, `default`, `price`, `list_price`, `spot_price`, `available`, `price_valid_until`, `payment_offers`, `promotions`}, `payment_offers[]`, `promotions[]`, `stamps[]`, `dual_price`, `weight`, `availability` {`available`, `unavailable_product`}, `description`, `specs[]` {`group`, `name`, `value`}, `variants[]` {`attribute`, `values[]` {`name`, `item_id`, `selected`, `image`}}, `images`, `international`, `region`, `price_scope`, `notes`.
- **delivery** - `item_id`, `seller_id`, `requested_cep`, `cep`, `address`, `can_deliver`, `message`, `out_of_stock_for_region`, `minimum_order_value`, `option_count`, `options[]` {`group`, `name`, `channel` (delivery or pickup-in-point), `price`, `list_price`, `estimate`, `estimate_date`, `earliest_date` {`day_of_week`, `day`, `month`, `month_name`}, `scheduled`, `pickup_store`}, `pickup_stores[]` {`name`, `pickup_point_id`, `distance_km`, `opening_hours`, `address`}, `notes`.
- **stores** - `state`, `city`, `total` (every pickup store), `count` (the ones matching state and city), `stores[]` {`store_id`, `name`, `street`, `neighborhood`, `city`, `state`, `cep`}, `notes`.
- **suggestions** - `query`, `terms[]` {`term`, `attributes[]` {`key`, `label`, `value`, `value_label`}}, `products[]` (list item fields), `top_searches[]` {`term`, `count`}, `notes`.
- **coupons** - `title`, `count`, `coupons[]` {`code`, `value`, `name`, `category`, `active`, `expires`, `expiration_date`, `link`, `collection_id`, `rules`}, `categories`, `terms`, `notes`.
- **categories** - `count`, `node_count`, `departments[]` {`name`, `url`, `site`, `path`, `filters`, `collection_id`, `children[]`}, `notes`.

## Guardrails

- Name it "Carrefour Brasil (carrefour.com.br: Mercado grocery + the www marketplace)" on first mention, and keep it apart from Carrefour France (carrefour.fr, `carrefour-api`). Carrefour Brasil accounts, carts and checkout are not read.
- Prices: quote `price` with `list_price` where it differs, the seller, the site, the region (or "the site's default prices" when `price_scope` is national) and the `fetched_at` date, in BRL (R$). A regional price holds for that CEP or store only.
- Computed prices: `payment_offers[].price` and `weight.item_price` are Scavio's arithmetic on the site's percentage and weight. Say so, name the payment method or offer as given, and never present them as a price the site printed.
- Coupons: quote code, value, name, expiry and rules exactly as given. Never apply a coupon to a price yourself or say a coupon fits a basket.
- Sponsored placements: `sponsored[]` are paid placements on the page; keep them apart from `items[]` and never present them as search ranking.
- Availability: `available` is a flag. Never state or estimate a unit count. A delivery quote does not reserve stock.
- Sellers: `seller.name` is Carrefour or the marketplace seller's business name as the site lists it. Refer to a seller by that name; do not profile the people behind a business.
- Comparing Carrefour Brasil with Atacadao, Mercado Libre or another supermarket: compare the same product (EAN), pack size, region, payment method and date. Never call one retailer cheaper beyond the numbers shown.
- Images and copy: do not republish Carrefour Brasil's product images or product copy; refer to items by `item_id` or EAN instead.
- Not available: unit counts, reviews and questions (the site has none), price history (poll and store), account data, cart or checkout. This API cannot reserve or buy an item.
- Terms: Scavio does not store Carrefour Brasil data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Carrefour Brasil's terms of use restrict automated access to its site; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, sellers, coupons, delivery dates, EANs or stock flags. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "item_id or url is required"; "item_id must be a Carrefour item id: digits (items[].item_id, or the number at the end of a /produto/ link, e.g. 1972)."; "cep is required"; "cep must be a Brazilian CEP: 8 digits, e.g. 01310-100."; "Send cep or store, not both."; "cep and store apply to site mercado. www prices are national; ..."; "store must be a store_id from /carrefourbr/stores (8 digits, e.g. 01405002)."; "seller_id must be a seller id from /carrefourbr/product (sellers[].seller_id, e.g. 1 for Carrefour)."; "The link is on <host>; send site <site> ..."; "Filter the price with min_price / max_price, not filters."; "filters takes at most 10 values."; "min_price must not be above max_price."; "state must be a two-letter Brazilian state (UF), e.g. SP.".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Carrefour has no product with item id <id> on <host>.", "Carrefour has no product with item id <id> in this region (<region>): the item is unknown or not sold there.", "Carrefour has no category <path> on <host>. Read /carrefourbr/categories for the category paths.", "Carrefour has no collection <id> on <host> (or it is empty there now).", "Carrefour has no pickup store with store_id <id>. Read /carrefourbr/stores for the store ids.", "Carrefour does not recognize the CEP <cep>.". A search with no items is an empty `200`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api).
- `502` and `503` mean Carrefour Brasil data was temporarily unavailable ("Carrefour Brasil is temporarily unavailable. Please try again."; "Carrefour Brasil is busy right now. Please retry in a few seconds.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.103.0
npm install scavio@0.104.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.carrefourbr.search({ query: "arroz", cep: "01310-100", sort: "orders_desc" });
const { data: rice } = await scavio.carrefourbr.category({ path: "/categoria/mercearia/alimentos-basicos/arroz", filters: { brand: "camil" } });
const { data: list } = await scavio.carrefourbr.collection({ collection_id: "29861" });
const { data: product } = await scavio.carrefourbr.product({ item_id: "1972", store: "01405002" });
const { data: quote } = await scavio.carrefourbr.delivery({ item_id: "1972", cep: "01310-100" });
const { data: stores } = await scavio.carrefourbr.stores({ state: "SP" });
const { data: typed } = await scavio.carrefourbr.suggestions({ query: "arroz" });
const { data: coupons } = await scavio.carrefourbr.coupons({});
const { data: menu } = await scavio.carrefourbr.categories({ site: "www" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.carrefourbr.search(...)`, `category`, `collection`, `product`, `delivery`, `stores`, `suggestions`, `coupons` and `categories`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 9 endpoints as tools: `search_carrefourbr`, `get_carrefourbr_category`, `get_carrefourbr_collection`, `get_carrefourbr_product`, `get_carrefourbr_delivery`, `get_carrefourbr_stores`, `get_carrefourbr_suggestions`, `get_carrefourbr_coupons` and `get_carrefourbr_categories`. Carrefour Brasil is opt-in: add `carrefourbr` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.103.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,carrefourbr"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/carrefourbr-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api), [category](https://scavio.dev/docs/carrefourbr-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api), [collection](https://scavio.dev/docs/carrefourbr-collection?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api), [product](https://scavio.dev/docs/carrefourbr-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api), [delivery](https://scavio.dev/docs/carrefourbr-delivery?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api), [stores](https://scavio.dev/docs/carrefourbr-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api), [suggestions](https://scavio.dev/docs/carrefourbr-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api), [coupons](https://scavio.dev/docs/carrefourbr-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api), [categories](https://scavio.dev/docs/carrefourbr-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api). Platform page: [scavio.dev/carrefourbr-api](https://scavio.dev/carrefourbr-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-brasil-api).
