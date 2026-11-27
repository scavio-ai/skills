# O Boticario + Eudora API - Prices, Pix Price, Online Stock, Coupons, Delivery

Read O Boticario and Eudora (boticario.com.br, eudora.com.br, the beauty brands of Grupo Boticario): keyword search, category, department and product-brand listings, the category menu, one product with its online stock and every shade, current prices for up to 10 SKUs, reviews, Beauty Week and the promotions hub, the promotions conditions page with coupon codes, the pickup stores near a CEP, and delivery and pickup for one product at a CEP. `brand` picks the storefront: `boticario` (default) or `eudora`. Brazil only (BRL, Portuguese text), as shown to a visitor who is not signed in. Every endpoint returns structured JSON and costs 1 credit, 2 when a page needs a second route; prices costs 1 credit per 5 SKUs.

**The job this skill is for: what a beauty item costs at O Boticario or Eudora today, by card and by Pix, how many units the site holds online, which coupon or countdown applies, and what delivery to a CEP takes.** On 2026-11-27 Lily Le Parfum Perfume 30ml (SKU `B48734`) read `price` R$ 339.90 (the card price, `installments` 10 x R$ 33.99) and `pix_price` R$ 305.91 (Pix, Brazil's instant payment). The Make B. Mate Salicylic foundation in Cor 330 (`B01863`) read R$ 59.90 against `was_price` R$ 99.90 (`discount_percent` 40) with `stock_units` 440 online, 9 shades with 3 out of stock, and 4.88 stars from 3,860 reviews. Beauty Week (the site's Black Friday event) listed 1,216 products.

Seven limits shape every answer, so say them plainly:
- **1 credit per call, 2 when a page needs a second route.** search, category, categories, product, deals and promotions read a full page: 1 credit, 2 when that page needs a second route. prices is 1 credit per 5 SKUs (ceil(skus / 5)). reviews, stores, pickup and suggestions are 1. `credits_used` in the response is the truth. A not-found (`404`) is charged at what it spent; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Page endpoints are slow.** search, category, categories, product, deals and promotions usually take 10-130 seconds; allow a client timeout of at least 240 seconds. The others usually answer in 2-25 seconds; allow at least 90.
- **Card price and Pix price, both as given.** `price` is the card price, `pix_price` the Pix price where the site shows one (null otherwise), `was_price` the crossed-out price. No cart, coupon or loyalty prices. Never compute one from another.
- **Prices can be up to about 15 minutes old.** Pages come from the site's own cache. Scavio keeps no cache of its own; every answer carries `fetched_at`.
- **Online stock, not store stock.** `stock_units` is the site's own online stock count for one SKU, as given. Per-store stock and per-store prices are not published: `pickup` says only whether store pickup is offered near a CEP.
- **No reviewer names.** Reviews carry rating, text, dates, votes, the variant and the reviewer's state (UF), never names, cities or gender. Reseller data is never returned.
- **No history.** Everything is the page at the moment of the call. Poll and store your own series.

Neither O Boticario nor Eudora has a public API for its catalog, prices or stock. Prices and stock are shown on boticario.com.br and eudora.com.br for each item, and this skill reads those public pages with one Scavio key.

See also: Natura `natura-api` (the Brazilian beauty brand of Natura &Co), Drogasil + Droga Raia `drogasil-droga-raia-api` (Brazilian pharmacy-aisle beauty prices), Mercado Libre `mercadolibre-product-data`, Magazine Luiza `magalu-magazine-luiza-api`; beauty prices in the US at Sephora `sephora-product-data` and Ulta `ulta-beauty-api`.

## When to trigger

Use this skill when the user asks to:
- Price an item at O Boticario or Eudora: card price, Pix price, was price, discount, installments
- Check current prices of a list of O Boticario or Eudora SKUs (up to 10 per call)
- Search boticario.com.br or eudora.com.br by keyword (in Portuguese: "perfume", "batom", "base liquida", "body splash"), sorted by relevance, price, discount, rating, best sellers or newest, filtered by product brand (Egeo, Floratta, Lily), line, category, rating, a price range or any facet the listing offers
- Browse one department, category or product-brand listing (/perfumaria/, /maquiagem/boca/batom/, /egeo/) or read the category menu
- Read one product: online stock units, availability, GTIN, every shade or size with its own price and stock, kit contents, the datasheet, the star histogram and the site's own review summary
- Read reviews for one shade or for every shade of a product, newest, most useful or oldest first, filtered by stars
- List Beauty Week (the Black Friday event) or the promotions hub (lowest price of the month, Leve 2 Pague 1, progressive discount) with each item's countdown end
- Read the promotions conditions page: each campaign's validity dates and coupon codes
- Find the stores that offer pickup of online orders near a CEP, with hours and address
- Quote delivery of one product to a CEP and check whether store pickup is offered

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 1 credit (2 when a page needs a second route; prices 1 per 5 SKUs), so 50 credits cover up to 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures: reviews 2.1 seconds, suggestions 2.8, stores 12.6, categories 13.2, deals 15.1, product 15.3, prices 15.6, promotions 16.2, pickup 24.1, search 31.7, category 78.0. Allow a client timeout of at least 240 seconds on the page endpoints and 90 on the others: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/boticario/search` | Keywords: 36 products per page with total, card price, Pix price, was price, discount, installments, badges, countdown end, rating, review count; facets and price bands | 1, 2 when the page needs a second route |
| `POST /api/v1/boticario/category` | One department, category or product-brand listing by path or link, sorted and filtered like search | 1, 2 when the page needs a second route |
| `POST /api/v1/boticario/categories` | The category menu: departments, groups and links, every path ready for category | 1, 2 when the page needs a second route |
| `POST /api/v1/boticario/product` | One product by SKU, slug or link: prices, online stock units, GTIN, every shade or size, kit contents, datasheet, review summary | 1, 2 when the page needs a second route |
| `POST /api/v1/boticario/prices` | Current price, was price, discount, Pix price and installments for 1-10 SKUs | 1 per 5 SKUs |
| `POST /api/v1/boticario/reviews` | Reviews by SKU or by product group (every shade), up to 50 per page, 3 sorts, star filter (no names) | 1 |
| `POST /api/v1/boticario/stores` | The stores that offer pickup of online orders near a CEP, nearest first, with distance, pickup time, hours and address | 1 |
| `POST /api/v1/boticario/pickup` | Delivery options with time and shipping cost for one product at a CEP, and whether store pickup is offered | 1 |
| `POST /api/v1/boticario/deals` | Beauty Week or the promotions hub (optionally one section), with each item's countdown end and badges | 1, 2 when the page needs a second route |
| `POST /api/v1/boticario/promotions` | The promotions conditions page: each campaign's validity dates and coupon codes as written | 1, 2 when the page needs a second route |
| `POST /api/v1/boticario/suggestions` | Suggested terms with departments and up to 5 products with prices | 1 |

Every endpoint takes `brand`: `boticario` (O Boticario, www.boticario.com.br; default) or `eudora` (Eudora, www.eudora.com.br). Brazil only: every answer carries `brand`, `brand_name`, `host`, `country` (br), `currency` (BRL) and `language` (pt-BR).

## Prices: card, Pix, was price and installments

Every listing item, product, prices item and suggestion carries the site's price layers as a visitor who is not signed in sees them:

| Field | Meaning |
|---|---|
| `price` | The card price in BRL (R$ 339.90 on Lily Le Parfum 30ml) |
| `pix_price` | The Pix price where the site shows one (R$ 305.91); null otherwise |
| `pix_discount_percent` (product) | The site's discount for paying by Pix, where given |
| `was_price` | The crossed-out price (R$ 99.90 on the Cor 330 foundation); null when none is shown |
| `discount_percent` | The site's discount against `was_price` (40) |
| `installments` | `{count, amount}`: the installment plan as given (10 x R$ 33.99); can be null on a listing card that shows none |
| `price_text` (product) | The site's price sentence as written ("Produto com 40% de desconto. De R$99,90 por R$59,90 em até 2 vezes de R$29,95 sem juros") |
| `badges` | The deal text as given ("CUPOM: MAIS10", "OUTLET", Leve 2 Pague 1) |
| `deal_ends_at` | The item's own countdown end as the site shows it, Brasilia time (2026-11-28T10:00:00-03:00) |

- Quote "Lily Le Parfum Perfume 30ml: R$ 305.91 by Pix or R$ 339.90 by card (10 x R$ 33.99) at boticario.com.br on 2026-11-27", with the date.
- A badge such as "CUPOM: MAIS10" names a coupon; the listed price is before any coupon. Never apply a coupon or a percent yourself.
- `discount_percent` is the site's own figure. Report the site's prices, labels and dates and the arithmetic only. Never judge a price as a good deal.

## Workflow

1. **Pick the storefront.** Send `brand` `boticario` (default) or `eudora` on every call.
2. **Find the item.** `/search` with `query` (`perfume`), `/category` with a `path` from `/categories` (`/perfumaria/`), or `/suggestions` for a quick lookup. Each item's `sku` is the input of product, prices, reviews and pickup.
3. **Narrow it.** Read `facets[]` and send a value from `facets[].values[].value` in the matching field (`product_brand`, `line`, `category`) or in `facets` (`{"familia-olfativa": "amadeirado"}`), plus `min_price` / `max_price` in BRL and `min_rating`.
4. **Watch many prices.** `/prices` with up to 10 `skus`: price, was price, Pix price and installments per SKU, 1 credit per 5.
5. **One product.** `/product` with `sku`, `slug` or `url`: online stock units, every shade with its own price and stock, kit contents, datasheet and `product_group_id`.
6. **Reviews.** `/reviews` with `product_id`: a SKU (that shade only) or the product's `product_group_id` (every shade together: the count the product page shows).
7. **Deals and coupons.** `/deals` with `type` `beauty_week` or `promotions` and an optional `section`; `/promotions` for each campaign's dates and coupon codes.
8. **Delivery and pickup.** `/pickup` with a SKU and a `cep`; `/stores` with a `cep` for the pickup stores near it.
9. **Watching prices:** there is no history. Poll the same SKUs on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`) and deals (`/deals`)

| Parameter | Description |
|---|---|
| `brand` | `boticario` (default) or `eudora` |
| `query` (search, required) | Keywords in Portuguese as shoppers type them, 1-200 characters |
| `path` (category, required) | A listing path or link: a department (`/perfumaria/`), a category (`/maquiagem/boca/batom/`), a product brand (`/egeo/`) or a `categories[]` path |
| `type` (deals) | `beauty_week` (default, the site's Black Friday event) or `promotions` (the promotions hub) |
| `section` (deals) | Optional sub-page as the site's links write it: a department (`perfumaria`, `maquiagem`, `cabelos`) or a promotion (`menor-preco-do-mes`, `leve-x-pague-y`, `desconto-progressivo`, `cashback`) |
| `sort` | `relevance` (default), `price_asc`, `price_desc`, `discount`, `rating`, `best_sellers`, `newest` |
| `product_brand` | Product brand slug or slugs (facets key `marca`, e.g. `egeo`, `floratta`, `lily`), up to 10 |
| `line` | Product line slug or slugs (facets key `linha`) |
| `category` | Category slug or slugs (facets key `categoria`) |
| `min_rating` | 1-4: that many stars or more; 5: 5 stars |
| `min_price`, `max_price` | Price range in BRL, whole numbers; `min_price` must be below `max_price` |
| `facets` | Up to 8 other facets: `{"<facets[].key>": value or [values]}` with values from `facets[].values[].value` |
| `page` | 1-100, 36 per page; `total_pages` reports the last one |

A keyword the site sends to a category landing (Eudora does this for broad terms such as batom or perfume) is followed as the site does it: `redirected_to` names the landing, and sort, filters and page are applied there. A keyword with no products returns `total` 0.

### Categories (`/categories`) and promotions (`/promotions`)

`brand` only.

### Product (`/product`) and pickup (`/pickup`)

| Parameter | Description |
|---|---|
| `sku` | A product SKU (`items[].sku`): a letter then digits, e.g. `B01863` (O Boticario) or `E55805` (Eudora) |
| `slug` | Or the product slug (`items[].slug`), e.g. `base-liquida-cor-330-make-b-mate-salicylic-30g` |
| `url` | Or a boticario.com.br or eudora.com.br product link (names the brand too). Send `sku`, `slug` or `url` |
| `cep` (pickup, required) | The Brazilian CEP (postal code) to quote: 8 digits, `01310-100` or `01310100` |

### Prices (`/prices`)

`skus` (required): 1-10 SKUs, an array or comma-separated (`["B01863", "B48734", "B2022081233"]`). 1 credit per 5 SKUs.

### Reviews (`/reviews`)

| Parameter | Description |
|---|---|
| `product_id` (required) | A SKU (that shade's reviews) or the product endpoint's `product_group_id` (every shade together) |
| `sort` | `most_recent`, `most_useful` or `oldest` (default: the site's order) |
| `stars` | Only reviews with this many stars, 1-5 |
| `page`, `page_size` | Page from 1; 1-50 per page, default 20 |

### Stores (`/stores`) and suggestions (`/suggestions`)

| Parameter | Description |
|---|---|
| `cep` (stores, required) | A Brazilian CEP, 8 digits |
| `radius_km` (stores) | Optional radius around the CEP, 1-100 km |
| `page`, `page_size` (stores) | Page 1-100; 1-50 per page, default 20 |
| `query` (suggestions, required) | What a shopper types, 1-100 characters (a SKU works too) |

## Examples

### Prices for three SKUs

Request `{"skus": ["B01863", "B48734", "B2022081233"]}` (1 credit): `count` 3, `found` 3. The second item:

```json
{
  "found": true,
  "sku": "B48734",
  "name": "Lily Le Parfum Perfume 30ml",
  "slug": "lily-le-parfum-perfume-30ml",
  "product_brand": "Lily",
  "department": "Perfumaria",
  "price": 339.9,
  "was_price": null,
  "discount_percent": null,
  "pix_price": 305.91,
  "installments": { "count": 10, "amount": 33.99 },
  "shade": null,
  "presentation": "30 ml",
  "seller": { "id": "47", "name": "O Boticário" }
}
```

The foundation `B01863` read R$ 59.90 against R$ 99.90 (40 percent off, 2 x R$ 29.95, `shade` "Cor 330", `presentation` "30 g"), and the combo `B2022081233` R$ 434.80 by card and R$ 391.32 by Pix (10 x R$ 43.48). An unknown SKU comes back `found` false instead of failing the call.

### One product with stock, shades and the review summary

Request `{"sku": "B01863"}` (1 credit, 2 when the page needs a second route): Base Líquida Cor 330 Make B. Mate Salicylic 30g.

```json
{
  "sku": "B01863",
  "product_brand": "Make B.",
  "gtin": null,
  "price": 59.9,
  "pix_price": null,
  "was_price": 99.9,
  "discount_percent": 40,
  "installments": { "count": 2, "amount": 29.95 },
  "price_text": "Produto com 40% de desconto. De R$99,90 por R$59,90 em até 2 vezes de R$29,95 sem juros",
  "availability": "in_stock",
  "stock_units": 440,
  "seller": { "id": "47", "name": "O Boticário" },
  "varies_by": ["color"],
  "review_summary": {
    "average_rating": 4.88,
    "count": 3860,
    "histogram": { "1": 21, "2": 13, "3": 57, "4": 231, "5": 3538 },
    "recommend_percent": 97,
    "ai_summary": "A base impressiona pela excelente cobertura, textura suave e efeito mate. Recomendada para peles com excesso de oleosidade, proporciona um acabamento natural, uniforme e duradouro até o final do dia."
  }
}
```

`variants` listed 9 shades (Cor 330, Cor 320, Cor 300, ...), each {`sku`, `name`, `color`, `size`, `price`, `availability`, `selected`}; Cor 270, Cor 250 and 200 read `out_of_stock`. `specs` is the datasheet (Cobertura Média, Acabamento Matte, Propriedades Cruelty Free and Dermocosmético). `product_group_id` joins every shade's SKU and is what reviews takes for the 3,860 total.

### Beauty Week with its countdown

Request `{"type": "beauty_week"}` (1 credit, 2 when the page needs a second route): `title` "BEAUTY WEEK COM DESCONTO MÁXIMO", `total` 1216, `total_pages` 34. The first item:

```json
{
  "position": 1,
  "sku": "B53850",
  "name": "Batom do Arraso Rosa Eu sou mais Eu Intense 3,6g",
  "product_brand": "Intense",
  "price": 7.5,
  "pix_price": null,
  "was_price": 37.9,
  "discount_percent": 80,
  "installments": null,
  "badges": [],
  "available": true,
  "free_shipping": false,
  "deal_ends_at": "2026-11-28T10:00:00-03:00",
  "rating": 4.84,
  "review_count": 582
}
```

### Coupons with their dates

Request `{}` to `/promotions` (1 credit, 2 when the page needs a second route): `valid_from` 2026-11-03, `count` 19 campaigns. Two of them:

```json
[
  { "name": "PISCOU, PERDEU PIX", "section": "EXCLUSIVO APP", "valid_from": "2026-11-23", "valid_to": "2026-11-30", "coupons": ["HOJEPIX"] },
  { "name": "BATALHA DE CUPONS", "section": "SITE E APP", "valid_from": "2026-11-16", "valid_to": "2026-11-18", "coupons": ["VANTAGEMBN", "SUPERMIMOS"] }
]
```

The page lists past and current campaigns: check `valid_to`. A date the page writes that does not exist is kept as written (the page-level `valid_to` read "31/11/2026").

### Delivery and pickup at a CEP

Request `{"sku": "B2022081233", "cep": "01310-100"}` (1 credit):

```json
{
  "requested": "B2022081233",
  "sku": "B2022081233",
  "cep": "01310100",
  "available": true,
  "seller_id": "47",
  "delivery": [{ "type": "normal", "description": "1 dia útil", "expected_days": 1, "shipping_cost": 0 }],
  "click_and_collect": true
}
```

`click_and_collect` says whether the site offers pickup at a store near the CEP; which store and its stock are not published.

### Search, stores, reviews, categories and suggestions

- `/search` `{"query": "perfume"}`: `total` 1823 over 51 pages of 36, 10 facets (`marca`, `categoria`, `linha`, `ocasiao`, `familia-olfativa`, `volume-perfumes`, `nota-da-avaliacao`, `concentracao`, `tipos`, `propriedades`) and 10 price bands; Lily Le Parfum 30ml read R$ 339.90 / Pix R$ 305.91 with 4.84 stars from 483 reviews, badge "CUPOM: MAIS10".
- `/category` `{"path": "/perfumaria/", "sort": "best_sellers"}`: `total` 911 over 26 pages; first Egeo Spicy Vibe Desodorante Colônia 90ml at R$ 122.90 against R$ 164.90 (25 percent off), 4.91 stars from 16,488 reviews.
- `/stores` `{"cep": "01310-100"}`: `total` 348 pickup stores, nearest first, each {`store_id`, `name`, `pickup_time` ("Retire em até 3 horas"), `distance_m`, `distance_km`, `hours` {`weekday`, `weekend`}, `address`}.
- `/reviews` `{"product_id": "B2022081233", "sort": "most_recent"}`: `total` 43 over 3 pages of 20, each {`review_id`, `rating`, `text`, `created_at`, `most_useful`, `upvotes`, `downvotes`, `reviewer_state` ("RJ"), `reviewer_type`, `sku`, `variant`, `photo_count`}. No reviewer names.
- `/categories` `{}`: 30 departments (Beauty Week, Promoção & Outlet, Cupons, Perfumaria, Maquiagem, Cabelos, Skincare, ...), each {`name`, `path`, `groups[]` {`name`, `path`, `links[]`}}.
- `/suggestions` `{"query": "perfume"}`: 5 terms (perfumaria, perfumado, egeo perfumaria, ...) with their departments and 5 products with prices.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def boticario(endpoint, body, timeout=240):
    r = requests.post(f"{BASE}/api/v1/boticario/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()

# 1. Current prices of three SKUs (1 credit per 5 SKUs)
d = boticario("prices", {"skus": ["B01863", "B48734", "B2022081233"]}, timeout=90)["data"]
for p in d["items"]:
    print(p["sku"], p["name"], p["price"], p["pix_price"], p["was_price"], p["installments"])

# 2. One product: online stock and every shade (1 credit, 2 when the page needs a second route)
prod = boticario("product", {"sku": "B01863"})["data"]
print(prod["stock_units"], [(v["color"], v["availability"]) for v in prod["variants"]])

# 3. Eudora Beauty Week, biggest discount first
deals = boticario("deals", {"brand": "eudora", "type": "beauty_week", "sort": "discount"})["data"]
for item in deals["items"][:10]:
    print(item["sku"], item["name"], item["price"], item["was_price"], item["deal_ends_at"])

# Prices and countdowns change through the day. Store each answer with fetched_at
# and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `brand`, `brand_name`, `host`, `country`, `currency` and `language`, and most carry `notes`.

- **search / category / deals** - `query` (search), `path` and `url` (category, deals), `type` and `section` (deals), `redirected_to`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `sort`, `title`, `items[]` {`position`, `sku`, `name`, `product_brand`, `url`, `slug`, `image`, `price`, `pix_price`, `was_price`, `discount_percent`, `installments` {`count`, `amount`}, `badges`, `available`, `free_shipping`, `deal_ends_at`, `rating`, `review_count`}, `facets[]` {`key`, `name`, `values[]` {`name`, `value`, `count`, `selected`}}, `price_ranges[]` {`range`, `count`}, `filters_applied`.
- **categories** - `count`, `departments[]` {`name`, `path`, `groups[]` {`name`, `path`, `links[]` {`name`, `path`}}}.
- **product** - `requested`, `sku`, `name`, `product_brand`, `url`, `slug`, `gtin`, `image`, `price`, `pix_price`, `pix_discount_percent`, `was_price`, `discount_percent`, `installments`, `price_text`, `availability` (in_stock, out_of_stock), `stock_units`, `seller` {`id`, `name`}, `categories`, `breadcrumbs`, `specs[]` {`name`, `values`}, `product_group_id`, `varies_by`, `variants[]` {`sku`, `name`, `color`, `size`, `url`, `image`, `price`, `availability`, `selected`}, `kit_components[]` {`sku`, `name`, `slug`, `url`, `quantity_in_kit`, `price`, `was_price`, `discount_percent`, `installments`, `stock_units`}, `kits_containing`, `review_summary` {`average_rating`, `count`, `histogram`, `recommend_percent`, `ai_summary`}.
- **prices** - `requested`, `count`, `found`, `items[]` {`sku`, `found`, `name`, `slug`, `url`, `product_brand`, `department`, `price`, `was_price`, `discount_percent`, `pix_price`, `installments`, `shade`, `presentation`, `image`, `seller`}; a SKU whose lookup failed this time carries `error` "unavailable" (not billed, ask again).
- **reviews** - `product_id`, `sort`, `stars`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `reviews[]` {`review_id`, `rating`, `text`, `created_at`, `modified_at`, `most_useful`, `upvotes`, `downvotes`, `reviewer_state`, `reviewer_type`, `sku`, `product_name`, `variant`, `photo_count`}.
- **stores** - `cep`, `radius_km`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `stores[]` {`store_id`, `name`, `pickup_time`, `distance_m`, `distance_km`, `hours` {`weekday`, `weekend`}, `address` {`street`, `number`, `district`, `postal_code`, `city`, `state`}}.
- **pickup** - `requested`, `sku`, `slug`, `url`, `cep`, `available`, `seller_id`, `delivery[]` {`type`, `description`, `expected_days`, `shipping_cost`}, `click_and_collect`.
- **promotions** - `url`, `valid_from`, `valid_to`, `count`, `campaigns[]` {`name`, `section`, `valid_from`, `valid_to`, `coupons`}.
- **suggestions** - `query`, `count`, `terms[]` {`term`, `departments`}, `products[]` (up to 5, the prices item shape).

## Guardrails

- Name them "O Boticario and Eudora (boticario.com.br, eudora.com.br, the beauty brands of Grupo Boticario)" on first mention. Other Grupo Boticario brands, accounts, the loyalty club and carts are not read.
- Prices: quote `price` (card) and `pix_price` (Pix) side by side in BRL (R$), with `was_price`, `installments` and the `fetched_at` date. Prices are what a visitor who is not signed in sees and can be up to about 15 minutes old. Never present one as a loyalty or coupon price.
- Coupons and countdowns: quote coupon codes, `valid_from` / `valid_to` and `deal_ends_at` exactly as given, with the date; they change through the day. Never apply a coupon yourself.
- Stock: `stock_units` is the site's online count for one SKU, as given. Never present it as store stock.
- Reviews: no reviewer names are returned. Quote a review as "an O Boticario customer review" (or Eudora); `ai_summary` is the site's own text as given, quote it short.
- Reseller data is never returned; do not try to find or profile resellers or the people behind a store.
- Comparing O Boticario or Eudora with Natura, Mercado Libre or a pharmacy: compare the same product, size and payment method on the same date. Never call one seller cheaper beyond the numbers shown.
- Images and copy: do not republish the sites' product images or marketing text; refer to items by `sku` or `slug` instead.
- Not available: per-store stock or prices, loyalty prices, other Grupo Boticario brands, reseller data, Q&A, price history (poll and store), account data, cart or checkout. This API cannot reserve or buy an item.
- Terms: Scavio does not store O Boticario or Eudora data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. The sites' terms of use restrict automated data mining and the reproduction of their content; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, coupons, stock units, SKUs, dates or ratings. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "brand must be one of boticario, eudora."; "query is required"; "slug, url or sku is required"; "sku must be a product SKU (a letter then digits, e.g. B01863 or E55805)."; "slug must be a product slug as the site writes it (e.g. base-liquida-cor-330-make-b-mate-salicylic-30g)."; "url must be a boticario.com.br or eudora.com.br link."; "url is a www.eudora.com.br link but brand is boticario."; "path must be a listing path as the site writes it (e.g. /perfumaria/ or /maquiagem/boca/batom/; categories[].path)."; "section must be a slug as the site writes it (e.g. perfumaria, menor-preco-do-mes, leve-x-pague-y)."; "section condicoes is the conditions page: use the promotions endpoint."; "skus is required"; "skus takes at most 10 SKUs per call."; "product_id must be a SKU (B01863) or the product_group_id the product endpoint returns (B01863-B01861-...)."; "cep must be a Brazilian CEP: 8 digits (e.g. 01310-100)."; "min_price must be below max_price."; "facets takes at most 8 keys."; "product_brand takes at most 10 values.".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged at what the call spent: "No O Boticário product <sku>.", "No O Boticário product with SKU <sku>.", "No O Boticário product with these SKUs." (prices, when none is found), "No O Boticário listing at this path.", "This O Boticário deal listing is not available.", "No O Boticário reviews for <id>.", "No store answer for this CEP.", "No suggestions for this query.", "The promotions conditions page is not available.", "The menu is not available." (Eudora answers name Eudora). A keyword with no products answers `total` 0, an unknown SKU inside a prices call answers `found` false, and a product with no purchase option answers pickup with `available` false, all with `200`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api).
- `502` and `503` mean O Boticario / Eudora data was temporarily unavailable ("O Boticario / Eudora is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.102.0
npm install scavio@0.103.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.boticario.search({ query: "perfume", sort: "price_asc", product_brand: "lily" });
const { data: grid } = await scavio.boticario.category({ path: "/perfumaria/", sort: "best_sellers" });
const { data: menu } = await scavio.boticario.categories({ brand: "eudora" });
const { data: product } = await scavio.boticario.product({ sku: "B01863" });
const { data: prices } = await scavio.boticario.prices({ skus: ["B01863", "B48734", "B2022081233"] });
const { data: reviews } = await scavio.boticario.reviews({ product_id: "B2022081233", sort: "most_recent" });
const { data: stores } = await scavio.boticario.stores({ cep: "01310-100" });
const { data: pickup } = await scavio.boticario.pickup({ sku: "B2022081233", cep: "01310-100" });
const { data: deals } = await scavio.boticario.deals({ brand: "eudora", type: "beauty_week", sort: "discount" });
const { data: promos } = await scavio.boticario.promotions({});
const { data: ideas } = await scavio.boticario.suggestions({ query: "perfume" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.boticario.search(...)`, `category`, `categories`, `product`, `prices`, `reviews`, `stores`, `pickup`, `deals`, `promotions` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `search_boticario`, `get_boticario_category`, `get_boticario_categories`, `get_boticario_product`, `get_boticario_prices`, `get_boticario_reviews`, `get_boticario_stores`, `get_boticario_pickup`, `get_boticario_deals`, `get_boticario_promotions` and `get_boticario_suggestions`. O Boticario + Eudora is opt-in: add `boticario` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.102.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,boticario"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/boticario-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api), [category](https://scavio.dev/docs/boticario-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api), [categories](https://scavio.dev/docs/boticario-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api), [product](https://scavio.dev/docs/boticario-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api), [prices](https://scavio.dev/docs/boticario-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api), [reviews](https://scavio.dev/docs/boticario-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api), [stores](https://scavio.dev/docs/boticario-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api), [pickup](https://scavio.dev/docs/boticario-pickup?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api), [deals](https://scavio.dev/docs/boticario-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api), [promotions](https://scavio.dev/docs/boticario-promotions?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api), [suggestions](https://scavio.dev/docs/boticario-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api). The platform page: [scavio.dev/boticario-api](https://scavio.dev/boticario-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=boticario-eudora-api).
