---
name: casas-bahia-api
description: "Casas Bahia API for Casas Bahia (casasbahia.com.br, the Brazilian retailer of Grupo Casas Bahia, with its Extra and Ponto stores; Brazil only, BRL) - what a product costs at Casas Bahia, Extra or Ponto today and who sells it, as the storefront shows it (on 2026-11-27 an Electrolux RE31 240L 220V refrigerator on extra.com.br read R$ 1.832,21 from Extra itself against a \"De\" price of R$ 2.015,43, R$ 1.648,99 by Pix with a 10 percent Pix discount, 18x R$ 101,79 interest-free, and 5 offers from R$ 1.648,99 to R$ 2.029,90 with marketplace sellers such as Belmicro at R$ 1.661,96; the same model in 110V on casasbahia.com.br was sold by Gazin at R$ 1.999,90 with a \"De\" price of R$ 3.498,90) with the regular price (card, one payment), the \"De\" list price, the Pix price and Pix discount, the discount percent, every installment plan by card type with interest, the store card plan, every seller with its business name, price, list price, buy-box flag and pickup flag, availability flags, EAN, specs, dimensions, variants (each its own SKU), the review summary with the star split and the storefront's own review summary, the 3 reviews and 3 questions on the page (no names); keyword search and category, deal collection or seller listings, 20 per page to page 500 with total and facets, in the storefront's 5 sorts and filtered by brand, rating, discount band, seller, features, own store and price range, sponsored placements kept apart (list items carry no prices); and the storefront's category menu. One catalog on three storefronts (site casasbahia, extra or pontofrio): own-store price and review counts can differ per site. 4 endpoints, 2 credits each. No freight by CEP, stores, suggestions or price history."
version: 1.0.0
tags: casas-bahia, casasbahia, casas-bahia-api, casasbahia-com-br, extra, extra-com-br, ponto, pontofrio, ponto-frio, grupo-casas-bahia, casas-bahia-prices, casas-bahia-pix, pix-price, pix-discount, parcelamento, installments, sem-juros, store-card, cartao-casas-bahia, casas-bahia-sellers, casas-bahia-marketplace, marketplace-sellers, buy-box, casas-bahia-search, casas-bahia-categories, casas-bahia-product, casas-bahia-reviews, ean, brazil, brazil-ecommerce, brazil-retail, brazilian-retailer, brl, price-monitoring, price-comparison, electronics-prices, appliance-prices, eletrodomesticos, geladeira, smart-tv, black-friday-brasil, agents, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/casasbahia-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=casas-bahia-api
---

# Casas Bahia API - Extra + Ponto, Sellers, Pix Price, Installments

Read Casas Bahia (casasbahia.com.br, the Brazilian retailer of Grupo Casas Bahia, with its Extra and Ponto stores): keyword search, category, deal collection and seller listings, one product with every price, installment plan and seller, and the storefront's category menu. One catalog on three storefronts, picked with `site`: `casasbahia` (default), `extra` (extra.com.br) or `pontofrio` (pontofrio.com.br, the Ponto store). Brazil only, Portuguese text, prices in BRL. Every endpoint returns structured JSON and costs 2 credits.

**The job this skill is for: what a product costs at Casas Bahia, Extra or Ponto today, paid how, and from which seller.** A Casas Bahia product page carries several prices at once and this skill returns each one as the storefront shows it, never computed. On 2026-11-27 the Electrolux Degelo Pratico RE31 240L refrigerator in 220V (sku `1743663`) on Extra read `price` R$ 1.832,21 (card, one payment) from Extra itself (`price_sold_by_store` true), `list_price` R$ 2.015,43 (the "De" price), `pix_price` R$ 1.648,99 with `pix_discount_percent` 10, `store_card` 18x R$ 101,79 sem juros, and `offer_count` 5 with `offer_price_range` R$ 1.648,99 to R$ 2.029,90: marketplace sellers Belmicro (R$ 1.661,96), DUFRIO (R$ 1.958) and LOJA GAZIN (R$ 2.029,90) next to the store's own offer. The same model in 110V (sku `1743662`) on casasbahia.com.br was sold by Gazin at R$ 1.999,90 against a "De" price of R$ 3.498,90 (`discount_percent` 43) and R$ 1.899,90 by Pix (5 percent).

Seven limits shape every answer, so say them plainly:
- **2 credits on every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **List items carry no prices.** Search and category return titles, SKUs, brands, ratings and status, never a price. Read `/product` with an item's `sku` for its prices. Say so when a user asks for "prices in a category".
- **The site decides the own-store price.** Casas Bahia, Extra and Ponto share one catalog, but each storefront's own-store price and its review counts can differ. Quote the `site` with every price.
- **Each variant is its own SKU.** A product's `variants[]` (110V and 220V, colors) each carry their own `sku`, price and sellers: read that SKU for them.
- **Pix is a separate price.** Pix is Brazil's instant payment. `pix_price` is the price paid by Pix when the storefront offers a Pix discount, and null when it does not.
- **20 items per page, page 1-500.** The storefront counts up to 10,000 results; `total_is_capped` true means the real total is higher.
- **No history, no freight.** Everything is the page at the moment of the call; Scavio keeps nothing. There is no freight by CEP (Brazilian postal code), no store list, no search suggestions and no reviews past the 3 on the page. Poll and store your own series.

Casas Bahia has no public API for its catalog or prices. Prices are shown on the storefronts for each product, and this skill reads those public pages with one Scavio key.

See also: Magalu `magalu-magazine-luiza-api`, KaBuM! `kabum-api`, Mercado Libre `mercadolibre-product-data`; the price comparison sites Buscape and Zoom `buscape-zoom-api` (match on EAN from `/product`).

## When to trigger

Use this skill when the user asks to:
- Price a product at Casas Bahia, Extra or Ponto: regular price, "De" price, Pix price and Pix discount, discount percent
- Read the installment plans of a product (parcelas sem juros, com juros, the Casas Bahia store card plan)
- List every seller of a product on Casas Bahia with its price and which one holds the buy box, or whether Casas Bahia sells it itself
- Search casasbahia.com.br, extra.com.br or pontofrio.com.br by keyword, sorted by relevance, popularity, price or best selling, filtered by brand, rating, discount band, seller, features, own store or price range
- Browse one Casas Bahia category, a deal collection or one seller's list
- Read the Casas Bahia category menu
- Read a product's EAN, specs, dimensions, variants, rating, star split, the storefront's review summary, and the reviews and questions on the page

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=casas-bahia-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=casas-bahia-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 2 credits, so 50 credits cover 25 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Calls usually take 10-60 seconds (in the captures: categories 5.6, category 11.1, product 13.5, search 29.7). Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/casasbahia/search` | Keywords: 20 items per page with total, SKU, title, brand, rating, status, category; sponsored placements apart; facets. No prices | 2 |
| `POST /api/v1/casasbahia/category` | One category, deal collection (`/c?Filtro=D<id>`) or seller's list (`/c?filtro=L<seller id>`) by path or link, same items, sorts and filters as search. No prices | 2 |
| `POST /api/v1/casasbahia/product` | One product by SKU or link: regular, "De" and Pix prices, installment plans, store card plan, every seller, availability, EAN, specs, variants, review summary, 3 reviews and 3 questions | 2 |
| `POST /api/v1/casasbahia/categories` | The storefront's category menu as its header lists it: groups, featured department shortcuts and top bar links | 2 |

Every answer carries `site`, `store` (Casas Bahia, Extra or Pontofrio), `country` (br), `currency` (BRL) and `language` (pt-BR).

## Prices, payment and sellers

`/product` carries the price layers as the storefront shows them:

| Field | Meaning |
|---|---|
| `price` | The regular price: card, one payment |
| `list_price` | The storefront's "De" price, when it shows one; null otherwise |
| `pix_price`, `pix_discount_percent` | The price paid by Pix and its discount, when the storefront offers a Pix discount; null otherwise |
| `discount_percent` | The storefront's discount from the "De" price, when shown |
| `price_seller_id`, `price_sold_by_store` | Who the shown price is from, and whether that is the storefront itself (own-store ids: Casas Bahia 10037, Extra 15, Pontofrio 16) |
| `payment` | `{pix, boleto}`: the payment methods the offer shows |
| `installment_plans[]` | `{type, plans[]}` per card type (Bandeira, Outros, CDC), each plan `{parcels, parcel_value, total, monthly_interest_percent, interest_free, text}` |
| `best_installments[]` | The longest plan per type, as the storefront headlines it |
| `store_card` | `{parcels, parcel_value, interest, cash_price}`: the Casas Bahia store card plan |
| `offer_count`, `offer_price_range` | How many offers the product has and their `{min, max}` |
| `sellers[]` | `{seller_id, name, buy_box, price, list_price, buy_button_enabled, is_store, pickup_available}`: every seller, by business name |
| `availability` | `{status, buy_button_enabled, pickup_available}`: flags, never unit counts |

- Quote "Electrolux RE31 240L 220V: R$ 1.832,21 at extra.com.br on 2026-11-27, sold by Extra (De R$ 2.015,43; R$ 1.648,99 by Pix)", with the site and date.
- A marketplace seller can be below the buy-box price (Belmicro at R$ 1.661,96 against Extra's R$ 1.832,21 in the capture). Say who holds `buy_box` and list the others with their prices.
- Installments: quote `parcels` x `parcel_value` and `text` as given ("18x R$ 101,79 sem juros"). A plan with `interest_free` false carries `monthly_interest_percent` and a `total` above the price; say so.
- A product can answer with every price null and `availability.status` out_of_stock: the storefront shows no offer at that moment. The TCL 55P755 TV (sku `55066339`) read R$ 2.599 with 10 percent Pix at one moment on 2026-11-27 and no offer later the same day.
- Report the storefront's prices, labels and plans and the arithmetic only. Never judge a price as a good deal.

## Workflow

1. **Find the product.** `/search` with `query` (`geladeira frost free`), `/category` with a `path` from `/categories`, a deal collection (`/c?Filtro=D69331`) or a seller's list. Each item's `sku` is the input of product.
2. **Narrow.** Add `filters` from a previous answer's `facets[].values[].filter` (brand `marca-m19`, rating `avaliacao-r5`, discount band `desconto-10to19`, seller `lojistas-l15`), `own_store` true, or `min_price` / `max_price` in whole reais.
3. **Prices and sellers.** `/product` with `sku` (and `site`) or a product `url`: read `price`, `list_price`, `pix_price`, `installment_plans`, `store_card` and `sellers[]`.
4. **Variants.** For 110V vs 220V or another color, read `variants[].sku` with `/product` again: each variant has its own price and sellers.
5. **Across storefronts.** Read the same `sku` with `site` `casasbahia`, `extra` and `pontofrio` to compare each store's own price; say which site each number came from.
6. **Watching prices:** there is no history. Poll the same SKUs on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`) and category (`/category`)

| Param | Type | Notes |
|---|---|---|
| `query` | string | Search only, required. Keywords in Portuguese as shoppers type them (`geladeira frost free`), up to 120 characters |
| `path` | string | Category only, required. `categories[].path` from `/categories` (`/c/eletroportateis?filtro=categoria-c73`), a deal collection (`/c?Filtro=D<id>`), a seller's list (`/c?filtro=L<seller id>`) or such a link on one of the three storefronts |
| `site` | string | `casasbahia` (default), `extra` or `pontofrio`. A link on another storefront with a different `site` is a `400` |
| `page` | integer | 1-500, 20 items a page. Default 1 |
| `sort` | string | `relevance` (default), `popularity`, `price_asc`, `price_desc`, `best_selling` |
| `filters` | string or array | Up to 10 values from `facets[].values[].filter`; values combine |
| `own_store` | boolean | Only items sold and delivered by the storefront itself, not by marketplace sellers |
| `min_price`, `max_price` | integer | Price range in whole reais (BRL). Not together with a `preco-` filter value |

### Product (`/product`)

| Param | Type | Notes |
|---|---|---|
| `sku` | string or integer | The SKU id (`items[].sku`, or the number after `/p/` in a product link), e.g. `1743663` |
| `url` | string | A product link on any of the three storefronts, instead of `sku` (the link's storefront is the site) |
| `site` | string | `casasbahia` (default), `extra` or `pontofrio` |

Send `sku` or `url`, not both.

### Categories (`/categories`)

`site` only. `{}` reads the Casas Bahia menu.

## Examples

### One product with its sellers

`POST /api/v1/casasbahia/product` with `{"site": "extra", "sku": "1743663"}` (2 credits), trimmed from the 2026-11-27 capture:

```json
{
  "site": "extra",
  "store": "Extra",
  "country": "br",
  "currency": "BRL",
  "sku": "1743663",
  "name": "Geladeira Electrolux Degelo Prático RE31 com Controle de Temperatura 240L - Branca - 220V",
  "ean": "7896584055917",
  "list_price": 2015.43,
  "price": 1832.21,
  "pix_price": 1648.99,
  "pix_discount_percent": 10,
  "discount_percent": 9,
  "price_seller_id": "15",
  "price_sold_by_store": true,
  "payment": { "pix": true, "boleto": false },
  "best_installments": [
    { "type": "Outros", "parcels": 12, "parcel_value": 173.15, "monthly_interest_percent": 1.99, "text": "com juros (1.99% a.m)" },
    { "type": "Bandeira", "parcels": 18, "parcel_value": 101.79, "monthly_interest_percent": 0, "text": "sem juros" }
  ],
  "store_card": { "parcels": 18, "parcel_value": 101.79, "interest": "sem juros", "cash_price": 1832.21 },
  "offer_count": 5,
  "offer_price_range": { "min": 1648.99, "max": 2029.9 },
  "sellers": [
    { "seller_id": "15", "name": "Extra", "buy_box": true, "price": 1832.21, "list_price": 2015.43, "buy_button_enabled": true, "is_store": true, "pickup_available": true },
    { "seller_id": "12299", "name": "Belmicro", "buy_box": false, "price": 1661.96, "list_price": 2979, "buy_button_enabled": true, "is_store": false, "pickup_available": null },
    { "seller_id": "35072", "name": "LOJA GAZIN", "buy_box": false, "price": 2029.9, "list_price": 2796.9, "buy_button_enabled": true, "is_store": false, "pickup_available": null }
  ],
  "availability": { "status": "in_stock", "buy_button_enabled": true, "pickup_available": true },
  "selection_fields": [{ "name": "Voltagem", "values": ["110V", "220V"] }],
  "variants": [
    { "sku": "1743662", "label": "110V", "attributes": { "Voltagem": "110V" }, "active": true, "selected": false },
    { "sku": "1743663", "label": "220V", "attributes": { "Voltagem": "220V" }, "active": true, "selected": true }
  ],
  "reviews": { "rating": 4.7, "count": 521 },
  "questions": { "total": 17 }
}
```

Each `installment_plans[]` entry lists every plan from 1x up for its card type, e.g. Bandeira `{"parcels": 2, "parcel_value": 916.1, "total": 1832.21, "interest_free": true, "text": "2x sem juros"}` and Outros `{"parcels": 2, "parcel_value": 943.54, "total": 1887.08, "monthly_interest_percent": 1.99, "interest_free": false}`.

### Search results (no prices)

`POST /api/v1/casasbahia/search` with `{"query": "geladeira frost free"}` (2 credits): `total` 1170, `total_pages` 59, 20 items and 8 sponsored placements kept apart.

```json
{
  "position": 1,
  "product_id": "87301061",
  "sku": "1576086051",
  "title": "Geladeira Frost Free Duplex Branca Consul - CRM40MB",
  "brand": "Consul",
  "rating": 4.83,
  "review_count": 105,
  "status": "available",
  "seller_type": null,
  "category": { "id": "13", "name": "Eletrodomésticos", "subcategories": [{ "id": "14", "name": "Refrigeradores" }] }
}
```

`facets[]` carry the filter values: `{"id": "preco", "name": "Preço", "values": [{"label": "Até R$ 199", "count": 47, "filter": "preco-0to199"}]}`. A sponsored item carries `seller_id` and its position among the sponsored slots.

### Category, categories, reviews and questions

- `/category` `{"path": "/c/eletroportateis?filtro=categoria-c73", "sort": "best_selling"}`: `total` 19139 with `total_is_capped` true, `total_pages` 500; first item Fritadeira Air Fryer Oven Mondial AFON-12L-FG 12L (`seller_type` marketplace, 220 reviews at 4.85). The category facet lists its children (Fritadeiras 1289, Liquidificadores e Acessorios 1439).
- `/categories` `{}`: `group_count` 8, `count` 39 (Tecnologia e Eletronicos, Casa e Decoracao, ...), each `{name, path, url, category_id, collection_id, seller_id}`; `featured` holds 11 department shortcuts and `menu` the top bar links. A `collection_id` marks a deal or campaign collection.
- `/product` `reviews` `{rating, count, recommend_percent, stars[] {stars, percent, label}, site_summary {text, topics[] {topic, sentiment}}, items[] {review_id, rating, text, date, likes, dislikes, images}}` and `questions` `{total, items[] {question_id, text, date, answers[] {text, date, answered_by}}}`. The TCL 55P755 TV read 4.9 from 759 reviews, 99 percent recommend, with the storefront's own summary praising picture and sound quality. No reviewer or asker names: names inside texts appear as `[nome]`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def casasbahia(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/casasbahia/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Search, own-store items only, lowest price first (2 credits). No prices on list items.
hits = casasbahia("search", {"query": "geladeira frost free", "own_store": True, "sort": "price_asc"})["data"]
sku = hits["items"][0]["sku"]

# 2. The same SKU on each storefront (2 credits each)
for site in ["casasbahia", "extra", "pontofrio"]:
    p = casasbahia("product", {"site": site, "sku": sku})["data"]
    print(site, p["price"], p["list_price"], p["pix_price"], p["offer_count"])
    for s in p["sellers"]:
        print("  ", s["name"], s["price"], "buy box" if s["buy_box"] else "")

# Casas Bahia prices change daily. Store each answer with fetched_at and run
# this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `site`, `store`, `country`, `currency` and `language`, and most carry `notes`.

- **search / category** - (`query` on search; `category` {`path`, `category_ids`, `collection_id`, `collection_name`, `seller_id`} on category), `filters`, `own_store`, `min_price`, `max_price`, `page_type`, `total`, `total_is_capped`, `total_pages`, `page`, `page_size`, `sort`, `count`, `items[]` {`position`, `product_id`, `sku`, `title`, `brand`, `brand_id`, `rating`, `review_count`, `image`, `url`, `path`, `status`, `seller_type`, `category` {`id`, `name`, `subcategories`}}, `sponsored_count`, `sponsored[]` (same fields plus `seller_id`), `facets[]` {`id`, `name`, `type`, `values[]` {`label`, `count`, `filter`, `selected`, `min`, `max`, `children`}}.
- **product** - `requested`, `sku`, `product_id`, `name`, `brand`, `brand_id`, `url`, `ean`, `categories[]` {`id`, `name`, `path`}, `list_price`, `price`, `pix_price`, `pix_discount_percent`, `discount_percent`, `price_seller_id`, `price_sold_by_store`, `payment` {`pix`, `boleto`}, `installment_plans[]`, `best_installments[]`, `store_card`, `offer_count`, `offer_price_range`, `sellers[]`, `availability`, `highlights[]` {`label`, `value`}, `specs[]` {`group`, `name`, `value`}, `dimensions` {`height`, `width`, `depth`, `weight`}, `images`, `selection_fields[]` {`name`, `values`}, `variants[]` {`sku`, `label`, `attributes`, `active`, `selected`, `image`}, `reviews`, `questions`.
- **categories** - `group_count`, `count`, `groups[]` {`name`, `categories[]` {`name`, `path` (null for a landing page that is not a product list), `url`, `category_id`, `collection_id`, `seller_id`}}, `featured[]`, `menu[]`.

## Guardrails

- Name it "Casas Bahia (casasbahia.com.br, the Brazilian retailer of Grupo Casas Bahia, with its Extra and Ponto stores)" on first mention. Accounts, the store card application and checkout are not read.
- Prices: quote `price`, `list_price`, `pix_price` with the `site` and the `fetched_at` date. Say "by Pix" for `pix_price`. Never present a price from search or category: there is none.
- Sellers: marketplace sellers are named by business name as the storefront shows it. Say who holds the buy box and whether it is the store itself (`is_store`).
- Installments: quote the plan as given; never compute your own installment or interest.
- Comparing storefronts or retailers: compare the same SKU (or the same EAN at another retailer), each with its site and date. Never call one store cheaper beyond the numbers shown.
- Reviews and questions: no reviewer or asker names are returned. Quote a review as "a Casas Bahia customer review"; `site_summary` is the storefront's own summary, quoted as given.
- Images and copy: do not republish the storefront's product images or copy; link products by `sku` instead.
- Not available: prices on list items, freight by CEP, store lists, search suggestions, reviews past the 3 on the page, collection start or end dates, price history (poll and store), account data, cart or checkout. This API cannot buy an item.
- Terms: Scavio does not store Casas Bahia data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Read the storefronts' current terms of use for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, plans, sellers, SKUs, EANs, ratings or dates. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "sku or url is required"; "Send sku or url, not both."; a SKU that is not digits ("sku must be a Casas Bahia SKU id: digits (items[].sku, or the number after /p/ in a product link, e.g. 55066339)."); a link on another storefront ("The link is on www.extra.com.br; send site extra or the sku alone."); a filter that is not a facet value ("... is not a filter value (facets[].values[].filter from a previous answer, e.g. marca-m19 or avaliacao-r5)."); "min_price must not be above max_price."; "Send min_price / max_price or a preco- filter value, not both."; a category path without its filtro part.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Casas Bahia product with sku <sku>. Check the sku (items[].sku) or link.", "No Casas Bahia category or collection at <path>. Check the path (categories[].path from /casasbahia/categories).".
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=casas-bahia-api).
- `502` on an unknown SKU: the storefront gives no answer at all for a SKU that does not exist, so after about 80 seconds the call answers "Casas Bahia gave no answer for sku <sku>. Check the sku (items[].sku from search or category); if it is right, retry in a moment. Not charged." Check the SKU before retrying.
- `502` and `503` otherwise mean Casas Bahia data was temporarily unavailable ("Casas Bahia is temporarily unavailable. Please try again." or "Casas Bahia is busy right now. Please retry in a few seconds.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.102.0
npm install scavio@0.103.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.casasbahia.search({ query: "geladeira frost free", sort: "price_asc", own_store: true });
const { data: grid } = await scavio.casasbahia.category({ path: "/c/eletroportateis?filtro=categoria-c73", sort: "best_selling" });
const { data: product } = await scavio.casasbahia.product({ site: "extra", sku: "1743663" });
const { data: menu } = await scavio.casasbahia.categories({ site: "pontofrio" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.casasbahia.search(...)`, `category`, `product` and `categories`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 4 endpoints as tools: `search_casasbahia`, `get_casasbahia_category`, `get_casasbahia_product` and `get_casasbahia_categories`. Casas Bahia is opt-in: add `casasbahia` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.102.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,casasbahia"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/casasbahia-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=casas-bahia-api), [category](https://scavio.dev/docs/casasbahia-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=casas-bahia-api), [product](https://scavio.dev/docs/casasbahia-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=casas-bahia-api) and [categories](https://scavio.dev/docs/casasbahia-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=casas-bahia-api). The platform page is [scavio.dev/casasbahia-api](https://scavio.dev/casasbahia-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=casas-bahia-api).
