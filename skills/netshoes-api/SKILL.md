---
name: netshoes-api
description: Netshoes API for Netshoes (netshoes.com.br, Brazil's sporting-goods store, part of Magalu; Brazil only, BRL, Portuguese text) - what each size of a sneaker, shirt, piece of sports gear or supplement costs at Netshoes today, who sells it, how many units are online and what delivery to a CEP costs, as netshoes.com.br shows it to a visitor who is not signed in (on 2026-11-27 the adidas Racer TR23 men's sneaker in black read R$ 249.99 against R$ 499.99, 3x R$ 83.33 without interest, in all 8 sizes sold by Netshoes, size 38 with 549 units online and free normal delivery in 3 days to a CEP on Avenida Paulista or Magalu pickup for R$ 4.90; a Soldiers Nutrition creatine 1 kg read R$ 81.05 by card and R$ 68.89 by Pix against R$ 279.90; the Black Friday sneaker list held 736 products from R$ 69.99) with price, list price, discount, installments, rating, badges, colours and sizes; keyword search, 100 per page, and list pages (Black Friday and other /lst/ lists), 45 per page, in the site's 7 sorts and filtered by any facet (brand, size, gender, product type, colour, department, promotion, sold-by) and a price range, with the site's counts; one product in one colour with every size's sku, EAN, price, Pix price, list price, installments and seller, plus colours, specs, rating and question count; every seller's offer for one size; the online stock count for one size and seller; delivery options to a Brazilian CEP; product reviews by stars or with photos (no names); shoppers' questions and answers (no asker names); the daily deal (Barato do Dia) with its start and end; a marketplace seller's company data, rating and newest reviews; the popular searches. 11 endpoints, 1 credit each. The daily deal carries no prices; no store stock, typed-term suggestions or price history.
version: 1.0.0
tags: netshoes, netshoes-com-br, netshoes-api, netshoes-prices, netshoes-precos, netshoes-pix, netshoes-pix-price, netshoes-black-friday, netshoes-barato-do-dia, netshoes-daily-deal, netshoes-ofertas, netshoes-deals, netshoes-search, netshoes-product, netshoes-sizes, netshoes-tamanhos, netshoes-stock, netshoes-estoque, netshoes-inventory, netshoes-frete, netshoes-shipping, netshoes-cep, netshoes-marketplace, netshoes-sellers, netshoes-lojista, netshoes-reviews, netshoes-avaliacoes, netshoes-questions, netshoes-perguntas, netshoes-popular-searches, magalu, brazil, brazil-ecommerce, brazilian-retail, brl, pix, parcelamento, cep, sporting-goods-prices, sneaker-prices, running-shoes-prices, sportswear-prices, supplement-prices, price-monitoring, price-tracking, product-data, marketplace-sellers, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/netshoes-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api
---

# Netshoes API - Sporting Goods Prices per Size, Pix Prices, Online Stock, Shipping by CEP, Sellers

Read Netshoes (netshoes.com.br, Brazil's sporting-goods store, part of Magalu): keyword search, list pages such as the Black Friday sneakers, one product with every size's price, Pix price and seller, every seller's offer for a size, the online stock count for a size, delivery options to a Brazilian CEP, product reviews, shoppers' questions and answers, the daily deal, a marketplace seller's page and the popular searches. www.netshoes.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in.

**The job this skill is for: what each size of an item costs at Netshoes today, who sells it, how many are online and what delivery to a CEP costs.** Netshoes sells its own stock next to marketplace sellers, and every size is its own sku with its own seller offers. On 2026-11-27 the adidas Racer TR23 men's sneaker `FBA-82XQ-006` read R$ 249.99 against R$ 499.99 (50 percent off, 3x R$ 83.33 without interest) in all 8 sizes, sold by Netshoes. Size 38 showed 549 units online, free normal delivery in 3 days to CEP 01310-100, or Magalu pickup for R$ 4.90 in 2 to 12 days. A Soldiers Nutrition creatine 1 kg read R$ 81.05 by card and R$ 68.89 by Pix (Brazil's instant payment), a 15 percent Pix promotion, against R$ 279.90.

Seven limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Prices per size and per seller, as given.** `price` is the card price, `pix_price` the Pix price where a Pix promotion applies (null otherwise), `list_price` the regular price. Listings carry the card price only; `/product` and `/offers` carry every size's offers.
- **The buy-box price can differ by a few reais.** The site refreshes the buy-box price when the product page opens, so `/shipping` and `/inventory` (which read that buy-box price and seller) can show a price a few reais from `/product`. Quote each with the endpoint it came from.
- **Stock is an online count, not a store count.** `/inventory` gives `quantity` for one size and seller as the site gives it (it may be capped or rounded). There is no store stock.
- **The daily deal carries no prices.** `/daily-deal` lists the Barato do Dia products with its start and end; send each `product_id` to `/product` for prices.
- **Listings stop at 10,000.** Search is 100 a page (pages 1-100), list pages 45 a page (pages 1-250); the site caps every total at 10,000 (`total_capped`). Narrow with filters or sorts to reach the rest.
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. There are no suggestions for a typed term (only the popular searches) and no price history. Poll and store your own series.

Netshoes has no public API for its catalog, prices or stock. Prices, sellers, stock and delivery options are shown on netshoes.com.br for each item, and this skill reads those public pages with one Scavio key.

See also: Centauro `centauro-api` (Brazilian sporting goods), Mercado Libre `mercadolibre-product-data` (Brazil marketplace), Magazine Luiza `magalu-magazine-luiza-api`, Decathlon `decathlon-product-data`, Nike `nike-api`, Foot Locker `foot-locker-api`, Dick's Sporting Goods `dicks-sporting-goods-api`.

## When to trigger

Use this skill when the user asks to:
- Price an item at Netshoes: card price, Pix price, list price, discount and installments, per size
- Search netshoes.com.br by keyword (in Portuguese: "tenis corrida", "camisa time", "creatina"), sorted by relevance, best sellers, new releases, offers, price or rating, filtered by brand, size, gender, product type, colour, department, promotion, a seller or a price range
- Read a Netshoes list page such as the Black Friday sneakers (`tenis-black-friday`) or another `/lst/` list as a product list
- Read one Netshoes product: every size with sku, EAN, price, Pix price, installments and seller; colours, specs, rating, review and question counts
- See every seller's offer for one size, with every installment plan
- Check how many units of one size are online at Netshoes or a marketplace seller
- Check delivery of one size to a Brazilian CEP: options, cost, days and dates, Magalu pickup, the free-shipping threshold
- Read a product's reviews (positive, negative, by stars, with photos) or its shoppers' questions and answers
- Read today's Netshoes daily deal (Barato do Dia) with its start and end
- Check a Netshoes marketplace seller: company name, CNPJ, business address, products sold, rating, recommendation percent and newest reviews
- Read the Netshoes popular searches

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api) - email or Google, no card required.
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
| `POST /api/v1/netshoes/search` | Keywords: 100 products per page (pages 1-100) with total, card price, list price, discount, installment count, rating, badges, colours, sizes and other colours; facets with the site's counts; the landing page when the keyword opens one | 1 |
| `POST /api/v1/netshoes/list` | A list page by slug or `/lst/` link (`tenis-black-friday` by default), 45 per page (pages 1-250), same items, sorts, filters and facets as search | 1 |
| `POST /api/v1/netshoes/product` | One product in one colour: every size with sku, EAN, availability, price, Pix price, list price, seller and every offer (installments, free shipping), weight and release date; colours, images, badges, breadcrumbs, specs, NCM, rating, review count, recommend percent, question count | 1 |
| `POST /api/v1/netshoes/offers` | Every seller's offer for one size sku: price, Pix price with the promotion, list price, discount, best and every installment plan, free shipping | 1 |
| `POST /api/v1/netshoes/inventory` | The online stock count for one size sku and seller (the buy-box seller by default), with `in_stock` | 1 |
| `POST /api/v1/netshoes/shipping` | Delivery options for one size sku to a Brazilian CEP: type, service, cost, free flag, days and dates; the lowest-cost and fastest option; the buy-box price; the free-shipping threshold | 1 |
| `POST /api/v1/netshoes/reviews` | A product's reviews, 13 per page, filtered by stars or photos: rating, text, date, recommends, photo count (no names) | 1 |
| `POST /api/v1/netshoes/questions` | A product's shoppers' questions, 10 per page, with the answer, dates and who answered (no asker names) | 1 |
| `POST /api/v1/netshoes/daily-deal` | The daily deal (Barato do Dia): title, start, end and the products with their seller ids, no prices | 1 |
| `POST /api/v1/netshoes/seller` | A marketplace seller by id: company name, CNPJ, business address, member since, official-store flag, products sold, rating, review counts, recommend percent, star histogram and newest reviews (no names) | 1 |
| `POST /api/v1/netshoes/popular-searches` | The popular searches the site's search box lists | 1 |

Brazil only: there is no `country` parameter. Every answer carries `store` (netshoes), `host`, `country` (br), `currency` (BRL) and `language` (pt-BR), and most carry `notes`.

## Prices: card price, Pix price, list price and installments

| Field | Meaning |
|---|---|
| `price` | The card price, in BRL (R$ 249.99 on the Racer TR23 below); on listings, the price a visitor who is not signed in sees |
| `pix_price` (product, offers, shipping) | The price paid by Pix where a Pix promotion applies (R$ 68.89 on the creatine below); null when there is none |
| `pix_promotion` (offers) | `{percent, amount, name}`: the Pix promotion as the site names it (15, 12.16, "15% PIX CREA 1KG SOLDIERS") |
| `list_price` | The regular price (R$ 499.99) |
| `discount_percent` | The discount against the list price, as the site gives it (50) |
| `installment` | `{count, amount, total, interest_free}`: the best installment plan (3x R$ 83.33, R$ 249.99, interest free); `/offers` adds `installments[]`, every plan |
| `installment_count` (listings) | The number of installments the card shows |
| `price_min`, `price_max` (product) | The lowest and highest size price of the colour |
| `free_shipping` (offers) | The offer's free-shipping flag; `/shipping` gives the cost to a CEP |

- Quote "Tenis Adidas Racer TR23 Masculino, black, size 38: R$ 249.99 by card (list R$ 499.99, 50 percent off), sold by Netshoes, on netshoes.com.br on 2026-11-27", with the size, the seller and the date.
- `pix_price` and the installment plan are what the site shows; never compute a Pix discount or an installment yourself. Report Netshoes' prices and labels and the arithmetic only, and never judge a price as a good deal.

## Workflow

1. **Find products.** `/search` with `query` (`tenis corrida`), or `/list` with `slug` (`tenis-black-friday`). Each item's `product_id` (the colour code, `FBA-82XQ-006`) is the input of `/product`; `product_code` (`FBA-82XQ`, every colour) is the input of `/reviews` and `/questions`.
2. **Narrow.** Read `facets` and send values back: `brand`, `gender`, `size`, `seller` as shortcuts, or `filters` `{key: value or [values]}` with `facets[].key` and `facets[].values[].value` (`{"marca": "nike", "genero": ["masculino"]}`); plus `price_min` / `price_max` in BRL and `sort`.
3. **Next pages.** Send `page` 2, 3, ... with the same query and filters. `has_more` false means the last page.
4. **One product.** `/product` with `product_id` (or a size sku, or `url`): every size's `sku`, EAN, prices and offers. Other colours are separate product ids in `colors[]`.
5. **One size.** `/offers` with a size `sku` (`sizes[].sku`, `FBA-82XQ-006-38`) for every seller's offer; `/inventory` with `sku` (and `seller_id`) for the online units; `/shipping` with `sku` and `cep` for delivery.
6. **The seller.** `sizes[].offers[].seller.id` (0 is Netshoes itself) is the input of `/seller` for a marketplace seller.
7. **Watching prices:** there is no history. Poll the same searches and products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`) and list (`/list`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords in Portuguese, 1-120 characters |
| `slug` (list) | A list slug or its `netshoes.com.br/lst/<slug>` link; default `tenis-black-friday` |
| `sort` | `relevance` (default), `best_sellers`, `new_releases`, `offers`, `price_asc`, `price_desc`, `top_rated`: the site's 7 sorts |
| `filters` | `{key: value or [values]}` with `facets[].key` and `facets[].values[].value`: `marca`, `tamanho`, `genero`, `tipo-de-produto`, `cor-principal`, `departamento`, `promocoes`, `vendido-por`, `pisada` and more, as the listing offers them. Several values of one key widen the match |
| `brand`, `gender`, `size`, `seller` | Shortcuts for `marca`, `genero`, `tamanho` and `vendido-por`: one value or a list (`nike`, `masculino`, `42`, `netshoes-netshoes`) |
| `price_min`, `price_max` | Price range in BRL, 0-100000 |
| `page` | Search 1-100 (100 per page); list 1-250 (45 per page) |

At most 12 filter values per call. A keyword the site sends to a landing page returns that page's products, with `landing_page` set and a note saying so. A search with no products returns an empty `200`.

### Product (`/product`)

Send exactly one of `product_id` (the colour code, `items[].product_id`, e.g. `FBA-82XQ-006`; a size sku works too) or `url` (a product link, `https://www.netshoes.com.br/p/<name>-<product id>`).

### Offers (`/offers`), inventory (`/inventory`) and shipping (`/shipping`)

| Parameter | Description |
|---|---|
| `sku` (required) | A size sku, `sizes[].sku` of `/product` (`FBA-82XQ-006-38`) |
| `seller_id` (inventory, shipping) | A seller id (`sizes[].offers[].seller.id`; 0 is Netshoes). Default: the size's buy-box seller |
| `cep` (shipping, required) | A Brazilian CEP (postal code) of 8 digits, with or without the dash (`01310-100`) |

### Reviews (`/reviews`) and questions (`/questions`)

| Parameter | Description |
|---|---|
| `product_id` | The product code shared by every colour (`product_code`, `FBA-82XQ`), or a colour product id or size sku |
| `url` | A product link, instead of `product_id` |
| `page` | 1-1000 (reviews 13 per page, questions 10 per page) |
| `rating` (reviews) | `positive` (5 and 4 stars), `negative` (2 and 1 star), or star values (`3`, `[5, 4]`) |
| `with_photos` (reviews) | `true` for reviews with photos |

Reviews are shared by every colour of the product, newest to oldest.

### Seller (`/seller`), daily deal (`/daily-deal`) and popular searches (`/popular-searches`)

`/seller` takes `seller_id` (digits, `sizes[].offers[].seller.id` or the daily deal's `items[].seller_ids`, e.g. `21072`) and optionally `name` (the seller's `name_slug`). `/daily-deal` and `/popular-searches` take an empty body `{}`.

## Examples

### One search item

Request `{"query": "tenis corrida", "brand": "nike"}` (1 credit): `total` 214, `total_pages` 3, 100 items, `filters_applied` `{"marca": ["nike"]}`, 14 facets (marca, tamanho, genero, tipo-de-produto, the price range R$ 157.88 to R$ 1,099.99, promocoes, cor-principal, vendido-por, ...). One item:

```json
{
  "position": 1,
  "product_id": "JD8-8100-006",
  "product_code": "JD8-8100",
  "name": "Tênis Nike Air Max Alpha Trainer 6 Masculino",
  "brand": "Nike",
  "department": "Running",
  "product_type": "Tênis Performance",
  "url": "https://www.netshoes.com.br/p/tenis-nike-air-max-alpha-trainer-6-masculino-JD8-8100-006",
  "available": true,
  "price": 399.99,
  "list_price": 799.99,
  "discount_percent": 50,
  "installment_count": 10,
  "rating": 4.68,
  "review_count": 942,
  "badges": ["Top Oferta"],
  "colors": ["Preto"],
  "flavors": [],
  "sizes": ["40", "42", "44", "45", "39", "38", "43", "41"]
}
```

The item also carried `image` and `other_colors` [{`product_id`, `image`}] (JD8-8100-002, JD8-8100-438). A facet value reads `{"value": "masculino", "label": "Masculino", "count": 129}`.

### One product

Request `{"product_id": "FBA-82XQ-006"}` (1 credit), abridged to one size:

```json
{
  "product_id": "FBA-82XQ-006",
  "product_code": "FBA-82XQ",
  "name": "Tênis Adidas Racer Tr23 Masculino",
  "brand": "Adidas",
  "listing_type": "EXCLUSIVE",
  "color": { "code": "6", "name": "Preto" },
  "price_min": 249.99,
  "price_max": 249.99,
  "size_count": 8,
  "sizes_available": 8,
  "sizes": [
    {
      "sku": "FBA-82XQ-006-38",
      "size": "38",
      "ean": "4069987416859",
      "available": true,
      "price": 249.99,
      "pix_price": null,
      "list_price": 499.99,
      "seller": { "id": "0", "name": "Netshoes", "is_store": true, "international": false },
      "offer_count": 1,
      "offers": [
        {
          "seller": { "id": "0", "name": "Netshoes", "is_store": true, "international": false },
          "available": true,
          "price": 249.99,
          "pix_price": null,
          "pix_promotion": null,
          "list_price": 499.99,
          "discount_percent": 50,
          "installment": { "count": 3, "amount": 83.33, "total": 249.99, "interest_free": true },
          "free_shipping": true
        }
      ],
      "weight_grams": 690
    }
  ],
  "ncm": "6404.11.00",
  "rating": 4.83,
  "review_count": 780,
  "percent_recommended": 98,
  "question_count": 0
}
```

The product also carried 4 colours (Preto, Cinza, Branco, Grafite, each its own `product_id`), 5 images, the badges Top Oferta, EXCLUSIVIDADE, NetsGO and SELEÇÃO, a 5-step `breadcrumbs` (Casual > Tênis > Masculino > Adidas > Preto) and 10 `specs` (Indicado para: Dia a Dia, Material: Têxtil e Sintético, Fechamento: Cadarço, ...).

### Offers, stock and delivery for one size

- `/offers` `{"sku": "I0Y-0011-289-01"}` (Creatina Monohidratada 100% Pura Soldiers Nutrition 1kg, size Único): 1 offer from Soldiers Nutrition (`id` 21072), `price` 81.05, `pix_price` 68.89, `pix_promotion` {15, 12.16, "15% PIX CREA 1KG SOLDIERS"}, `list_price` 279.9, `discount_percent` 71, 1x R$ 81.05, free shipping.
- `/inventory` `{"sku": "FBA-82XQ-006-38"}`: `seller` Netshoes (`id` 0), `quantity` 549, `in_stock` true.
- `/shipping` `{"sku": "FBA-82XQ-006-38", "cep": "01310-100"}`:

```json
{
  "sku": "FBA-82XQ-006-38",
  "cep": "01310100",
  "seller": { "id": "0", "name": "Netshoes", "is_store": true, "score": 5 },
  "price": 249.99,
  "pix_price": null,
  "count": 2,
  "options": [
    { "type": "NORMAL", "service": "NORMAL", "seller_id": "0", "cost": 0, "free": true, "min_days": 3, "max_days": 3, "min_date": "2026-12-02", "max_date": "2026-12-02" },
    { "type": "COLLECT_MAGALU", "service": "COLLECT_ON_MAGALU", "seller_id": "0", "cost": 4.9, "free": false, "min_days": 2, "max_days": 12, "min_date": "2026-12-01", "max_date": "2026-12-15" }
  ],
  "free_shipping_threshold": { "min_order": 99, "missing": 0, "reached": true }
}
```

`COLLECT_MAGALU` is pickup at a Magalu pickup point. The answer also carried `lowest_cost` and `fastest` (both the free NORMAL option here).

### Reviews, questions, seller, daily deal and popular searches

- `/reviews` `{"product_id": "FBA-82XQ"}`: `total_reviews` 780, 13 reviews on the page, e.g. `{"review_id": "21109345", "rating": 5, "text": "Ótimo produto e conforme o anúncio, recomendo a todos", "date": "2026-11-27T06:40:01.379", "recommends": true, "photo_count": 0}`. Many reviews carry a rating with `text` null.
- `/questions` `{"product_id": "I0Y-0011"}`: `total_questions` 86, `total_pages` 9, 10 a page, e.g. "Qual a validade do produto após a abertura da embalagem?" answered by Soldiers Nutrition (`answered_by_ai` false) with the dates asked and answered.
- `/seller` `{"seller_id": "21072"}`: Soldiers Nutrition, `member_since` 2022-08-12, `official_store` false, `cnpj` 46936908000102, the business address in Cajamar, SP, `products_sold` 163603, `rating` 4.53 over 2978 reviews (1158 with a comment), `percent_recommended` 94, `product_quality_stamp` true, a 5-star histogram (2124 five-star) and the 10 newest reviews without names.
- `/daily-deal` `{}`: `title` "BARATO DO DIA", `starts_at` 2026-11-27T00:00:00, `ends_at` 2026-11-27T23:59:59, 10 items, first the Tênis Nike Air Max Alpha Trainer 6 Masculino (`JD8-8100-006`, `seller_ids` ["13644"]), then a Palmeiras jersey kit sold by Netshoes. No prices: send each `product_id` to `/product`.
- `/popular-searches` `{}`: tenis masculino, tenis feminino, tenis adidas, tenis nike (4).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def netshoes(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/netshoes/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Nike running shoes, lowest price first (1 credit)
hits = netshoes("search", {"query": "tenis corrida", "brand": "nike", "sort": "price_asc"})["data"]
for it in hits["items"][:5]:
    print(it["name"], it["price"], it["list_price"], it["discount_percent"], it["product_id"])

# 2. One product: every size with its price, Pix price and seller (1 credit)
item = netshoes("product", {"product_id": hits["items"][0]["product_id"]})["data"]
size = next(s for s in item["sizes"] if s["available"])
print(size["size"], size["price"], size["pix_price"], size["seller"]["name"])

# 3. Online units and delivery to a CEP for that size (1 credit each)
stock = netshoes("inventory", {"sku": size["sku"]})["data"]
ship = netshoes("shipping", {"sku": size["sku"], "cep": "01310-100"})["data"]
print(stock["quantity"], ship["lowest_cost"]["cost"], ship["fastest"]["max_days"])

# Netshoes prices change during the day. Store each answer with fetched_at and run
# this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `host`, `country`, `currency` and `language`.

- **search / list** - `query` and `landing_page` (search), `slug` and `url` (list), `page`, `page_size` (100 / 45), `total`, `total_capped`, `total_pages`, `has_more`, `count`, `title`, `items[]` {`position`, `product_id`, `product_code`, `name`, `brand`, `department`, `product_type`, `url`, `image`, `available`, `price`, `list_price`, `discount_percent`, `installment_count`, `rating`, `review_count`, `badges`, `colors`, `flavors`, `sizes`, `other_colors[]` {`product_id`, `image`}}, `facets[]` {`key`, `name`, `values[]` {`value`, `label`, `count`}, `min`, `max`}, `quick_filters[]` {`key`, `value`, `label`}, `filters_echoed`, `sort`, `filters_applied`, `notes`.
- **product** - `product_id`, `requested_id`, `product_code`, `name`, `brand`, `department`, `product_type`, `genders`, `url`, `available`, `listing_type`, `color` {`code`, `name`}, `price_min`, `price_max`, `sellers[]`, `size_count`, `sizes_available`, `sizes[]` {`sku`, `size`, `ean`, `available`, `price`, `pix_price`, `list_price`, `seller` {`id`, `name`, `is_store`, `international`}, `offer_count`, `offers[]` {`seller`, `available`, `price`, `pix_price`, `pix_promotion` {`percent`, `amount`, `name`}, `list_price`, `discount_percent`, `installment` {`count`, `amount`, `total`, `interest_free`}, `free_shipping`}, `weight_grams`, `release_date`}, `colors[]` {`product_id`, `name`, `available`, `url`}, `images`, `badges`, `breadcrumbs[]` {`name`, `url`}, `specs[]` {`name`, `value`}, `ncm`, `rating`, `review_count`, `percent_recommended`, `question_count`, `notes`. No marketing description.
- **offers** - `sku`, `product_id`, `product_code`, `name`, `size`, `ean`, `color`, `available`, `url`, `offer_count`, `offers[]` (as above, plus `seller.international` and `installments[]`, every plan), `notes`.
- **inventory** - `sku`, `seller` {`id`, `name`, `is_store`}, `quantity`, `in_stock`, `notes`.
- **shipping** - `sku`, `cep`, `seller` {`id`, `name`, `is_store`, `score`}, `price`, `pix_price`, `currency`, `count`, `options[]` {`type` (NORMAL, COLLECT_MAGALU, ...), `service`, `seller_id`, `cost`, `free`, `min_days`, `max_days`, `min_date`, `max_date`}, `lowest_cost`, `fastest`, `free_shipping_threshold` {`min_order`, `missing`, `reached`}, `notes`.
- **reviews** - `product_code`, `page`, `page_size` (13), `total_pages`, `has_more`, `rating_filter`, `with_photos`, `total_reviews`, `total_filtered`, `count`, `reviews[]` {`review_id`, `rating`, `text`, `date`, `recommends`, `photo_count`}, `notes`.
- **questions** - `product_code`, `page`, `page_size` (10), `total_pages`, `has_more`, `total_questions`, `count`, `questions[]` {`question`, `asked_at`, `answer`, `answered_at`, `answered_by` (the seller, or the site's AI assistant), `answered_by_ai`}, `notes`.
- **daily-deal** - `title`, `starts_at`, `ends_at` (Brasilia time, as given), `count`, `items[]` {`position`, `product_id`, `name`, `url`, `image`, `available`, `seller_ids`}, `notes`. No prices.
- **seller** - `seller_id`, `name`, `name_slug`, `official_store`, `active`, `member_since`, `company_name`, `cnpj`, `address` {`street`, `number`, `neighborhood`, `city`, `state`, `cep`}, `products_sold`, `logo`, `url`, `rating`, `review_count`, `reviews_with_comment`, `percent_recommended`, `product_quality_stamp`, `histogram[]` {`stars`, `count`, `percent`}, `likert[]` {`label`, `weight`, `count`}, `reviews[]` {`rating`, `text`, `date`, `recommends`}, `notes`.
- **popular-searches** - `count`, `searches[]` {`position`, `term`}, `notes`.

## Guardrails

- Name it "Netshoes (netshoes.com.br, Brazil's sporting-goods store, part of Magalu)" on first mention. Netshoes accounts, carts and checkout are not read or made.
- Prices: quote `price` with `list_price`, the size, the seller and the `fetched_at` date, in BRL (R$), and say which endpoint the price came from: `/shipping` and `/inventory` read the buy-box price, which can differ by a few reais from `/product`. Prices are what a visitor who is not signed in sees.
- Pix and installments: quote `pix_price`, `pix_promotion` and `installment` exactly as given. Never compute a Pix discount or an installment, and never assume a Pix price applies where `pix_price` is null.
- Stock: `quantity` is the online count for one size and seller as the site gives it (it may be capped or rounded). Never present it as store stock or as Netshoes-wide stock across sellers.
- Daily deal: the answer carries no prices. Never quote a daily-deal price without a `/product` call.
- Totals: `total` stops at 10,000. Never call a capped total the number of products.
- Sellers: a marketplace seller's company name, CNPJ and business address are the company data the seller page publishes; use them to judge a seller before a purchase. Contacts are not returned.
- Reviews and questions: no reviewer or asker names are returned. Quote a review as "a Netshoes buyer review" with its rating and date; never try to identify a reviewer or an asker.
- Comparing Netshoes with Centauro, Mercado Libre or another store: compare the same product, colour, size, seller and date. Never call one site cheaper beyond the numbers shown.
- Images and copy: Netshoes' terms of use restrict reproducing its identity elements. Do not republish its logos, product photos or page copy; refer to products by `product_id` and `url` instead, and keep any use descriptive.
- Not available: store stock, store pickup by store, suggestions for a typed term (only the popular searches), deal prices in the daily deal, price history (poll and store), account data, cart or checkout. This API cannot buy, review or ask a question.
- Terms: Scavio does not store Netshoes data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Netshoes' terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, stock counts, delivery options, ratings or reviews. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id or url is required"; "Pass one of product_id, sku or url."; "product_id must be a Netshoes product id: the colour code, e.g. FBA-82XQ-006 (items[].product_id)."; "sku must be a Netshoes size sku (sizes[].sku of the product endpoint, e.g. FBA-82XQ-006-37)."; "cep must be a Brazilian CEP of 8 digits, e.g. 01310-100."; "seller_id 0 is Netshoes itself, not a marketplace seller."; "slug must be a Netshoes list slug or link (netshoes.com.br/lst/<slug>, e.g. tenis-black-friday)."; "At most 12 filter values per call."; "price_max must be at least price_min."; "rating must be positive, negative, or star values 1-5 (e.g. [5, 4])."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Netshoes has no product <id>.", "Netshoes has no size <sku> in product <id>.", "Netshoes has no list <slug>.", "Netshoes has no offer for size <sku>.", "Netshoes has no delivery for size <sku> to CEP <cep>.", "Netshoes has no seller <id>.", "Netshoes has no daily offer right now.". A search with no products is an empty `200`, not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api).
- `502` and `503` mean Netshoes data was temporarily unavailable ("Netshoes is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- Search and list usually take 2-30 seconds (in the captures: 4.3 and 5.8 seconds), the seller page 5-15 seconds, everything else 2-10 seconds. Allow a client timeout of at least 180 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.104.0
npm install scavio@0.105.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.netshoes.search({ query: "tenis corrida", brand: "nike", sort: "price_asc" });
const { data: blackFriday } = await scavio.netshoes.list({ slug: "tenis-black-friday", sort: "offers" });
const { data: item } = await scavio.netshoes.product({ product_id: "FBA-82XQ-006" });
const { data: offers } = await scavio.netshoes.offers({ sku: "FBA-82XQ-006-38" });
const { data: stock } = await scavio.netshoes.inventory({ sku: "FBA-82XQ-006-38" });
const { data: ship } = await scavio.netshoes.shipping({ sku: "FBA-82XQ-006-38", cep: "01310-100" });
const { data: reviews } = await scavio.netshoes.reviews({ product_id: "FBA-82XQ", rating: "negative" });
const { data: questions } = await scavio.netshoes.questions({ product_id: "I0Y-0011" });
const { data: deal } = await scavio.netshoes.dailyDeal({});
const { data: seller } = await scavio.netshoes.seller({ seller_id: "21072" });
const { data: popular } = await scavio.netshoes.popularSearches({});
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.netshoes.search(...)`, `list`, `product`, `offers`, `inventory`, `shipping`, `reviews`, `questions`, `daily_deal`, `seller` and `popular_searches`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `search_netshoes`, `get_netshoes_list`, `get_netshoes_product`, `get_netshoes_offers`, `get_netshoes_inventory`, `get_netshoes_shipping`, `get_netshoes_reviews`, `get_netshoes_questions`, `get_netshoes_daily_deal`, `get_netshoes_seller` and `get_netshoes_popular_searches`. Netshoes is opt-in: add `netshoes` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.104.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,netshoes"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/netshoes-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api), [list](https://scavio.dev/docs/netshoes-list?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api), [product](https://scavio.dev/docs/netshoes-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api), [offers](https://scavio.dev/docs/netshoes-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api), [inventory](https://scavio.dev/docs/netshoes-inventory?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api), [shipping](https://scavio.dev/docs/netshoes-shipping?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api), [reviews](https://scavio.dev/docs/netshoes-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api), [questions](https://scavio.dev/docs/netshoes-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api), [daily deal](https://scavio.dev/docs/netshoes-daily-deal?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api), [seller](https://scavio.dev/docs/netshoes-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api), [popular searches](https://scavio.dev/docs/netshoes-popular-searches?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api). Platform page: [scavio.dev/netshoes-api](https://scavio.dev/netshoes-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=netshoes-api).
