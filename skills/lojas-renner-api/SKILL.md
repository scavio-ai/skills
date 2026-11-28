---
name: lojas-renner-api
description: Lojas Renner API for Lojas Renner (lojasrenner.com.br, the Brazilian fashion retailer; Brazil only, BRL, Portuguese text) - what a Renner piece costs today, what it costs on the Cartao Renner store card against other cards, how many units the site lists, which sizes are available and which Renner stores serve a CEP, as lojasrenner.com.br shows it to a visitor who is not signed in (on 2026-11-27 a Cortelle barrel trouser read R$ 199.90 against R$ 219.90, 6x R$ 33.32 interest-free on the Cartao Renner or 4x R$ 49.98 on other cards, rated 4.4 over 21 reviews, in 6 sizes all available; the camiseta search held 9,468 products, the first at R$ 69.90 against R$ 79.90 with 17 units listed and 163 sold in the last 15 days; the list of every discounted product held 106,896; a CEP on Avenida Paulista had 5 Sao Paulo stores) with price, list price, discount, installment plan, stock level, stock status, units sold in 15 days and seller (Lojas Renner or a partner store); keyword search, category listings and lists (every discounted product by default), 48 per page to page 200, in the site's 8 sorts and filtered by category, sold by, brand, size, colour, gender and the states with stock, with the site's counts; one product with both installment plans, the rating aggregate, composition, every colour with its sizes and per-size availability flags; price and stock flags for one size; the stores for a CEP's city with address, hours and store number; a product's customer reviews as the product page shows them, up to 100 per page, newest or most helpful, positive, negative, with photos or one star rating, with rating, title, text, the review date, the date of the order the review is linked to, size and fit answers, photos and the store's reply (on 2026-11-28 a Cortelle satin shirt was rated 4.6 over 742 reviews), no reviewer names. 7 endpoints, 1 credit each. Availability per size is a flag, not a count; no shipping quote, search suggestions or price history.
version: 1.0.0
tags: renner, lojas-renner, lojasrenner, lojasrenner-com-br, renner-api, lojas-renner-api, renner-prices, renner-precos, renner-search, renner-product, renner-reviews, renner-avaliacoes, renner-sizes, renner-tamanhos, renner-stock, renner-estoque, renner-stock-level, renner-deals, renner-ofertas, renner-promocoes, renner-black-friday, renner-lists, renner-categories, renner-refinements, renner-brands, renner-marketplace, renner-sellers, cartao-renner, renner-installments, renner-parcelamento, renner-rating, renner-stores, renner-lojas, renner-cep, fashion-prices, clothing-prices, moda-feminina, moda-masculina, brazil, brazil-ecommerce, brazilian-retail, brl, cep, price-monitoring, product-data, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 300
    throttle: 1
    homepage: https://scavio.dev/renner-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api
---

# Lojas Renner API - Fashion Prices, Stock Levels, Cartao Renner Installments, Stores by CEP, Reviews

Read Lojas Renner (lojasrenner.com.br, the Brazilian fashion retailer): keyword search, category listings and lists such as every discounted product, one product with its installment plans, rating aggregate, colours and per-size availability, the price and stock flags of one size, the Renner stores for a CEP, and a product's customer reviews as its page shows them. www.lojasrenner.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in.

**The job this skill is for: what a Renner piece costs today, on the store card and on other cards, how many units the site lists, and which sizes are available.** On 2026-11-27 the Cortelle barrel trouser `931758127` (Calça Barrel em Flamê com Brilho) read R$ 199.90 against R$ 219.90 (9 percent off), 6x R$ 33.32 interest-free on the Cartão Renner (Renner's store card) or 4x R$ 49.98 on other cards, rated 4.4 over 21 reviews, in 6 sizes all available. The camiseta search listed a Get Over seamless T-shirt at R$ 69.90 against R$ 79.90 with a stock level of 17 and 163 sold in the last 15 days.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Listings are slow at the source.** Search, category and lists usually take 30-200 seconds (the captures took 11-24 seconds); allow a client timeout of at least 300 seconds and send one call at a time.
- **Two installment plans.** `installments.store_card` is the interest-free plan on the Cartão Renner, `installments.credit_card` the plan for other cards. Listings carry the one plan the listing shows (`installment`).
- **Stock level on listings, flags per size.** `stock_level` is the unit count the site lists for the product and `sold_last_15_days` its own figure; `/product` and `/sku-price` give per-size flags (`available`, `out_of_stock`, `omni_stock`, ...), not unit counts.
- **Reviews come from `/reviews`.** `rating` and `review_count` on `/product` are the page's aggregate; `/reviews` returns the reviews themselves with the store's average and count (Renner shows no star histogram). Reviewer names are never returned, and reviews can lag the product page by up to 4 hours.
- **No history, shipping or suggestions.** Everything is the page at the moment of the call; Scavio keeps nothing. There is no shipping quote by CEP and no search suggestions. Poll and store your own series.

Lojas Renner publishes no developer API for its catalog, prices or stock. Prices, sizes and stores are shown on lojasrenner.com.br, and this skill reads those public pages with one Scavio key.

See also: C&A Brasil `cea-brasil-api`, Dafiti `dafiti-api`, Netshoes `netshoes-api`, Centauro `centauro-api`, Mercado Libre `mercadolibre-product-data` (Brazil marketplace), Magazine Luiza `magalu-magazine-luiza-api`, H&M `hm-api`, Zara `zara-api`.

## When to trigger

Use this skill when the user asks to:
- Price a Lojas Renner item: price, list price, discount and the installment plan on the Cartão Renner and on other cards
- Search lojasrenner.com.br by keyword (in Portuguese: "camiseta", "calca jeans", "vestido"), sorted by relevance, newest, best selling, discount, price or name, filtered by category, sold by (Lojas Renner or a partner store), brand, size, colour, gender or the states with stock
- List a Renner category (`4zo6za` is Feminino) or a list, by default every discounted product
- Read a listing's stock level and units sold in the last 15 days, as the site lists them
- Read one Renner product: price, both installment plans, rating aggregate, composition, details, every colour with its sizes, and each size's availability flags
- Check the price and stock flags of one size
- List the Renner stores for a CEP's city, with address, hours and store number
- Read a Renner product's customer reviews: newest or most helpful, positive, negative, with photos or one star rating, with the size and fit answers and the store's reply

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api) - email or Google, no card required.
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
| `POST /api/v1/renner/search` | Keywords: 48 products per page (pages 1-200) with total, price, list price, discount, installment, stock level, stock status, units sold in 15 days, seller, colours and sizes; refinements with the site's counts | 1 |
| `POST /api/v1/renner/category` | A category by navigation id (`4zo6za`) or `/c/` link, same items, sorts and refinements | 1 |
| `POST /api/v1/renner/deals` | A list by navigation id or `/lista/` link; by default the site's list of every discounted product | 1 |
| `POST /api/v1/renner/product` | One product: price, list price, both installment plans, rating aggregate, availability flags, seller, categories, composition, details, every colour with its sizes and skus, and the shown colour's sizes with availability flags | 1 |
| `POST /api/v1/renner/sku-price` | One size: price, list price, both installment plans, availability flags and the most a shopper can buy | 1 |
| `POST /api/v1/renner/stores` | The stores the site's store locator lists for a CEP's city or region: store number, name, address, phone and hours | 1 |
| `POST /api/v1/renner/reviews` | One product's customer reviews by product id or link, as the product page shows them: up to 100 per page, sorted newest or most helpful, filtered positive, negative, with photos or one star rating, with the store's average and count | 1 |

Brazil only: there is no `country` parameter. Every answer carries `store` (renner), `host`, `country` (br), `currency` (BRL) and `language` (pt-BR), and most carry `notes`.

## Prices: price, list price and the two installment plans

| Field | Meaning |
|---|---|
| `price` | The price now (the sale price where there is one), in BRL (R$ 199.90 on the trouser below) |
| `list_price` | The price before the discount (R$ 219.90) |
| `discount_percent`, `on_sale` | The discount, as a percent (9), and the site's sale flag |
| `installments.store_card` (product, sku-price) | `{count, amount, interest_free}`: the plan on the Cartão Renner (6x R$ 33.32, interest-free) |
| `installments.credit_card` (product, sku-price) | `{count, amount}`: the plan on other cards (4x R$ 49.98) |
| `installment` (listings) | `{count, amount}`: the plan the listing shows (2x R$ 34.95) |

- Quote "Calça Barrel em Flamê com Brilho by Cortelle: R$ 199.90 (list R$ 219.90), 6x R$ 33.32 on the Cartão Renner, on lojasrenner.com.br on 2026-11-27", with the date.
- Quote both installment plans exactly as given; never compute one yourself, and never judge a price as a good deal.

## Workflow

1. **Find products.** `/search` with `query` (`camiseta`), `/category` with `category` (`4zo6za`, or a navigation id from `breadcrumbs[].url` or a category refinement), or `/deals` (every discounted product by default, or a `list`).
2. **Narrow.** Read `refinements` and send `refinements[].values[].filter` ids back in `filters` (up to 10): category, sold by, brand, size, colour, gender and region (the states with stock). `applied` shows the refinements in force.
3. **Next pages.** Send `page` 2, 3, ... (up to 200) with the same query, filters and `sort`. `has_more` false means the last page.
4. **One product.** `/product` with `product_id` (`items[].product_id`, `931758127`) or `url`; add `sku` (`colors[].sku` or `colors[].sizes[].sku`) to show another colour or size.
5. **One size.** `/sku-price` with `product_id` and a size `sku` (`sizes[].sku`, `931758135`) for its price and stock flags.
6. **Stores.** `/stores` with a `cep`.
7. **Reviews.** `/reviews` with `product_id` (or `url`); `page` 2, 3, ... while `has_more` is true. `total` is the product's review count on an unfiltered request and null with a `filter` or `rating`.
8. **Watching prices:** there is no history. Poll the same searches and products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`) and deals (`/deals`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords in Portuguese, 1-120 characters |
| `category` (category, required) | A category navigation id (`4zo6za` is Feminino) or a lojasrenner.com.br `/c/` link or path ending in `/-/N-<id>` |
| `list` (deals) | A list navigation id or a lojasrenner.com.br `/lista/` link; default `1l95pyv`, the list of every discounted product |
| `sort` | `relevance` (default), `newest`, `best_selling`, `discount`, `price_asc`, `price_desc`, `name_asc`, `name_desc`: the site's 8 sorts |
| `filters` | One refinement id or a list of up to 10 (`refinements[].values[].filter`, e.g. `xv9uau` for gender Feminino), combined freely |
| `page` | 1-200 (48 per page) |

A search with no products returns an empty `200` (charged). There are no search suggestions.

### Product (`/product`) and one size (`/sku-price`)

| Parameter | Description |
|---|---|
| `product_id` | The Lojas Renner product id, digits (`items[].product_id`, `931758127`) |
| `url` | A lojasrenner.com.br product link (`items[].url`), instead of `product_id` |
| `sku` (product: optional; sku-price: required) | A sku: on `/product` it picks the colour and size to show (`colors[].sku`, `colors[].sizes[].sku`); on `/sku-price` the size (`sizes[].sku`, `931758135`) |

Send `product_id` or `url`, not both.

### Stores (`/stores`)

`cep`: a Brazilian CEP (postal code) of 8 digits, with or without the dash (`01310-100`).

### Reviews (`/reviews`)

| Parameter | Description |
|---|---|
| `product_id` | The Lojas Renner product id (`items[].product_id`, `846044605`) |
| `url` | A lojasrenner.com.br product link, instead of `product_id` |
| `page` | Reviews page, 1-200 (default 1) |
| `per_page` | Reviews per page, 1-100 (default 20) |
| `sort` | `newest` (default) or `most_helpful` (the most helpful votes at the top) |
| `filter` | `all` (default), `positive` (ratings 3-5), `negative` (ratings 1-2) or `with_photos` |
| `rating` | Only the reviews with this star rating, 1-5. Send `rating` or `filter`, not both |

Send `product_id` or `url`, not both.

## Examples

### One search item

Request `{"query": "camiseta"}` (1 credit): `total` 9468, `total_pages` 198, 48 items, 7 refinements (category, sold_by, brand with 100 values, size, color, gender, region with 27 states). One item:

```json
{
  "position": 1,
  "product_id": "930726748",
  "name": "Camiseta Seamless em Poliamida",
  "brand": "Get Over",
  "color": { "id": "COR930726748-19-1627TCX", "name": "Vermelho", "hex": "#381521" },
  "default_sku": "930770554",
  "price": 69.9,
  "list_price": 79.9,
  "discount_percent": 12,
  "on_sale": true,
  "installment": { "count": 2, "amount": 34.95 },
  "stock_level": 17,
  "stock_status": "in_stock",
  "sold_last_15_days": 163,
  "marketplace": false,
  "seller": "Lojas Renner",
  "gender": "Feminino",
  "categories": ["feminino > blusas-e-camisetas > manga-curta", "feminino > esportivo > blusas-e-camisetas"],
  "colors": [
    { "id": "COR930726748-19-4007TCX", "name": "Preto", "hex": "#292935", "sku": "930726772" },
    { "id": "COR930726748-19-1627TCX", "name": "Vermelho", "hex": "#381521", "sku": "930770520" }
  ],
  "sizes": ["PP", "P", "M", "G", "GG"]
}
```

The item also carried `url` and `image`. A refinement value reads `{"label": "Lojas Renner", "count": 7718, "filter": "1xp7cku"}` (sold by).

### One product

Request `{"product_id": "931758127"}` (1 credit), abridged:

```json
{
  "product_id": "931758127",
  "sku": "931758258",
  "name": "Calça Barrel em Flamê com Brilho",
  "brand": "Cortelle",
  "color": { "id": "COR931758127-11-0602TCX", "name": "Branco", "hex": "#c8c7c3" },
  "size": "44",
  "price": 199.9,
  "list_price": 219.9,
  "on_sale": true,
  "discount_percent": 9,
  "installments": {
    "store_card": { "count": 6, "amount": 33.32, "interest_free": true },
    "credit_card": { "count": 4, "amount": 49.98 }
  },
  "rating": 4.4,
  "review_count": 21,
  "available": true,
  "purchasable": true,
  "out_of_stock": false,
  "max_quantity": 100,
  "marketplace": false,
  "seller": "Lojas Renner",
  "gender": "Feminino",
  "size_count": 6,
  "sizes_available": 6,
  "sizes": [
    { "size": "36", "sku": "931758135", "available": true, "purchasable": true, "out_of_stock": false, "omni_stock": true, "pre_order": false, "discontinued": false }
  ]
}
```

The product also carried 3 colours, each with its sizes and skus, 6 sizes in the colour shown, 3 `breadcrumbs` (Feminino first), 2 `composition` lines (70.0% Poliester, 14.0% Algodão, 6.0% Linho, ...), 2 `details` (Marca: Cortelle; Coleção: Outono/Inverno 2026), 7 images and the flags `omni_stock`, `back_order`, `pre_order`, `pre_launch` and `discontinued`.

### One size and the stores for a CEP

- `/sku-price` `{"product_id": "931758127", "sku": "931758135"}`: size 36 in Branco (`code` 11-0602TCX), `price` 199.9, `list_price` 219.9, store card 6x R$ 33.32, other cards 4x R$ 49.98, `available` true, `omni_stock` true, `max_quantity` 100.
- `/stores` `{"cep": "01310-100"}`: `cep_state` SP, 5 stores in the site's order (not by distance): Shopping Light (`store_number` 35, Rua Coronel Xavier de Toledo 23), Loja Avenida Paulista, Shopping Pátio Paulista, Shopping Jardim Pamplona and Loja Oscar Freire, each with `hours` ("De Segunda a Sábado das 10h às 21h. Domingo das 12h às 18h.") and `phone` 3004 4700, the chain's shared number (dial it and enter the store number). `excluded_count` 0.

### Lists and categories

- `/deals` `{}`: `list` 1l95pyv, `total` 106896 discounted products, first a Blue Steel ribbed blouse at R$ 49.90 against R$ 59.90 with a stock level of 70 (`stock_status` in_omni_stock) and 686 sold in the last 15 days.
- `/category` `{"category": "4zo6za", "sort": "discount"}`: Feminino, `total` 82688, 19 category refinements; the first 10 items, 83 to 88 percent off, were all sold by partner stores (`marketplace` true, `seller` the store's name).

### Reviews

Request `{"product_id": "846044605"}` (1 credit): `product_name` Camisa em Cetim com Recortes e Caimento Leve, `rating` {"average": 4.6, "count": 742}, `total` 742, `count` 20, `has_more` true, newest first. One review:

```json
{
  "id": "36796078",
  "rating": 4,
  "title": null,
  "text": "A modelagem é pequena. O tecido é bem gostoso ao toque",
  "date": "2026-11-21",
  "purchase_date": "2026-11-17",
  "recommends": true,
  "helpful_votes": 1,
  "unhelpful_votes": 0,
  "photos": [],
  "attributes": [],
  "store_reply": null,
  "imported": false,
  "influencer": false
}
```

No reviewer name is returned. 1 of the 20 reviews had a photo; none had a store reply on this page.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def renner(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/renner/{endpoint}", headers=HEADERS, json=body, timeout=300)
    r.raise_for_status()
    return r.json()

# 1. T-shirts sold by Lojas Renner, lowest price first (1 credit; listings are slow)
hits = renner("search", {"query": "camiseta", "sort": "price_asc"})["data"]
for it in hits["items"][:5]:
    print(it["name"], it["price"], it["list_price"], it["stock_level"], it["product_id"])

# 2. One product: both installment plans and each size's flags (1 credit)
item = renner("product", {"product_id": hits["items"][0]["product_id"]})["data"]
print(item["price"], item["installments"]["store_card"], item["installments"]["credit_card"])
size = next(s for s in item["sizes"] if s.get("available"))

# 3. Price and stock flags for that size (1 credit)
one = renner("sku-price", {"product_id": item["product_id"], "sku": size["sku"]})["data"]
print(one["size"], one["price"], one["available"], one["max_quantity"])

# Renner prices change during the day. Store each answer with fetched_at and run
# this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `host`, `country`, `currency` and `language`.

- **search / category / deals** - `query` (search), `category` (category), `list` (deals), `page`, `page_size` (48), `total`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `product_id`, `name`, `brand`, `url`, `image`, `color` {`id`, `name`, `hex`}, `default_sku`, `price`, `list_price`, `discount_percent`, `on_sale`, `installment` {`count`, `amount`}, `stock_level`, `stock_status` (in_stock, in_omni_stock), `sold_last_15_days`, `marketplace`, `seller`, `gender`, `categories`, `colors[]` {`id`, `name`, `hex`, `sku`}, `sizes`}, `refinements[]` {`name`, `label`, `multi_select`, `values[]` {`label`, `count`, `filter`}}, `applied`, `search_terms`, `sort`, `filters_applied`, `notes`.
- **product** - `product_id`, `requested_sku`, `sku`, `sku_matched`, `name`, `brand`, `url`, `color` {`id`, `name`, `hex`}, `size`, `price`, `list_price`, `on_sale`, `discount_percent`, `installments` {`store_card` {`count`, `amount`, `interest_free`}, `credit_card` {`count`, `amount`}}, `rating`, `review_count`, `available`, `purchasable`, `out_of_stock`, `omni_stock`, `back_order`, `pre_order`, `pre_launch`, `discontinued`, `max_quantity`, `marketplace`, `seller`, `gender`, `categories`, `breadcrumbs[]` {`name`, `url`}, `composition`, `details`, `images`, `colors[]` {`id`, `name`, `hex`, `sku`, `sizes[]` {`size`, `sku`}}, `size_count`, `sizes_available`, `sizes[]` {`size`, `sku`, `available`, `purchasable`, `out_of_stock`, `omni_stock`, `pre_order`, `discontinued`}, `notes`. The reviews come from `/reviews`. No shipping quote or marketing description.
- **sku-price** - `product_id`, `sku`, `name`, `color` {`name`, `code`, `hex`}, `size`, `price`, `list_price`, `on_sale`, `discount_percent`, `installments` {`store_card`, `credit_card`}, `available`, `purchasable`, `out_of_stock`, `omni_stock`, `back_order`, `pre_order`, `pre_launch`, `discontinued`, `max_quantity`, `image`, `notes`.
- **stores** - `cep`, `cep_state`, `count`, `stores[]` {`store_number`, `name`, `address` {`street`, `number`, `complement`, `city`, `state`}, `phone`, `hours`}, `excluded_count`, `notes`. No coordinates or distances.
- **reviews** - `product_id`, `page`, `per_page`, `sort`, `filter`, `rating_filter`, `total` (the product's review count; null with a filter or rating), `has_more`, `count`, `product_name`, `rating` {`average`, `count`}, `reviews[]` {`id`, `rating`, `title`, `text` (null when the review has stars but no text), `date`, `purchase_date` (the date of the order the review is linked to), `recommends`, `helpful_votes`, `unhelpful_votes`, `photos[]` {`image`, `thumbnail`}, `attributes[]` {`name`, `answer`}, `store_reply`, `imported`, `influencer`}, `notes`. No star histogram, reviewer names or questions and answers.

## Guardrails

- Name it "Lojas Renner (lojasrenner.com.br, the Brazilian fashion retailer)" on first mention. Renner accounts, carts and checkout are not read or made.
- Prices: quote `price` with `list_price` and the `fetched_at` date, in BRL (R$). Quote the Cartão Renner plan and the other-cards plan as two plans, exactly as given; never compute an installment.
- Stock: `stock_level` and `sold_last_15_days` are the figures the site lists for the product; per-size answers are flags (`available`, `out_of_stock`, `omni_stock`), not counts. Never present a flag as a unit count, or a listing's `stock_level` as one size's stock.
- Sellers: `marketplace` true means a partner store sells the product, named in `seller` (a store name). Say so when comparing prices.
- Ratings: `rating` and `review_count` on `/product` are the aggregate the product page shows; `/reviews` returns the reviews themselves.
- Reviews: quote `rating`, `date` and the store's own summary figures as facts with the `fetched_at` date. `text` and `title` are the customer's own words: quote a short excerpt where it answers the question, never republish review bodies in bulk, and never invent or merge one. `purchase_date` is the date of the order the review is linked to; describe it in exactly those words, never as more. Reviewer names are never returned; never look for the person behind a review. `imported` marks a review the store brought in from another source, `influencer` one the store marks as from an influencer: say so when it matters. Reviews can lag the product page by up to 4 hours.
- Stores: the store locator's list for the CEP's city or region, in its order, not by distance. Rows outside the CEP's state are left out and counted in `excluded_count`. `phone` is the chain's shared number.
- Use: Lojas Renner's terms of use restrict reproducing its content beyond access. Keep any use descriptive (prices, availability and stores as facts with their date); do not republish Renner's product photos, page copy or links to its pages, and refer to products by `product_id`.
- Comparing Renner with C&A Brasil, Dafiti or another store: compare the same product, size and date. Never call one store cheaper beyond the numbers shown.
- Not available: questions and answers, a star histogram, reviewer names, shipping quotes by CEP, search suggestions, store coordinates or store stock, deal start and end dates, price history (poll and store), account data, cart or checkout. This API cannot buy or reserve anything.
- Terms: Scavio does not store Lojas Renner data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Lojas Renner's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, stock figures, ratings or stores. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id or url is required"; "Pass product_id or url, not both."; "product_id must be a Lojas Renner product id (digits, items[].product_id, e.g. 931758127)."; "sku must be a Lojas Renner sku id (digits, e.g. 931758135: sizes[].sku of the product endpoint)."; "cep must be a Brazilian CEP of 8 digits, e.g. 01310-100."; "Pass rating or filter, not both."; "per_page must be a whole number from 1 to 100."; "At most 10 filter ids per call."; "query must contain letters or digits."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Lojas Renner has no product <id>.", "Lojas Renner has no sku <sku> for product <id>.", "Lojas Renner has no category <id>.", "Lojas Renner has no list <id>.", "Lojas Renner has no reviews page for product <id> (an unknown product id, items[].product_id)." Some unknown ids answer `200` with no reviews (`count` 0, charged). A search with no products is an empty `200`, not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api).
- `502` and `503` mean Lojas Renner data was temporarily unavailable ("Lojas Renner is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- Search, category and lists usually take 30-200 seconds at the source (in the captures 11-24 seconds); allow a client timeout of at least 300 seconds. Product, one size and stores usually take 5-30 seconds, reviews 2-20 seconds; allow at least 180 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.106.0
npm install scavio@0.107.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.renner.search({ query: "camiseta", sort: "price_asc" });
const { data: women } = await scavio.renner.category({ category: "4zo6za", sort: "discount" });
const { data: deals } = await scavio.renner.deals({ sort: "best_selling" });
const { data: item } = await scavio.renner.product({ product_id: "931758127" });
const { data: size } = await scavio.renner.skuPrice({ product_id: "931758127", sku: "931758135" });
const { data: stores } = await scavio.renner.stores({ cep: "01310-100" });
const { data: reviews } = await scavio.renner.reviews({ product_id: "846044605", sort: "most_helpful" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.renner.search(...)`, `category`, `deals`, `product`, `sku_price`, `stores` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 7 endpoints as tools: `search_renner`, `get_renner_category`, `get_renner_deals`, `get_renner_product`, `get_renner_sku_price`, `get_renner_stores` and `get_renner_reviews`. Lojas Renner is opt-in: add `renner` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.106.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,renner"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/renner-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api), [category](https://scavio.dev/docs/renner-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api), [deals](https://scavio.dev/docs/renner-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api), [product](https://scavio.dev/docs/renner-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api), [sku price](https://scavio.dev/docs/renner-sku-price?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api), [stores](https://scavio.dev/docs/renner-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api), [reviews](https://scavio.dev/docs/renner-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api). Platform page: [scavio.dev/renner-api](https://scavio.dev/renner-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api).
