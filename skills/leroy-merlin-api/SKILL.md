---
name: leroy-merlin-api
description: "Leroy Merlin API for Leroy Merlin (the home improvement retailer of the ADEO group; Brazil, Italy, Spain, Portugal, Poland, Romania and France, each in its own language and currency) - what a home improvement product costs at Leroy Merlin in a market or Brazilian price region today and which store has it, as the site shows it (on 2026-11-27 a Wap WF 12K3.2 12V cordless drill read R$ 129,90 in the Grande Sao Paulo price region against R$ 149,90, 6x R$ 21,65, tagged Black Friday, with 225 units in the Ferramentas aisle at the Raposo Tavares store and 12 of 16 region stores in stock, standard delivery to a Sao Paulo CEP R$ 9,90 next day and free store pickup in 2 hours; a Makita DHP490 18V drill R$ 599,90 against R$ 744,57 on an offer ending 2026-11-28; on leroymerlin.it a DEWALT DCF887N impact driver read 98,90 EUR (81,07 EUR excluding VAT) with 18 offers, and the Italian offers page held 923 products with prices valid 11 to 29 November) with the price, original price, discount, unit (each, m2, roll) and box price, installments, promotion dates, Black Friday tag, seller (Leroy Merlin or a marketplace seller), marketplace offers, EAN or GTIN, specifications, Europe's price excluding VAT, unit price and delivery options; keyword search and category listings (Brazil priced per region; Europe sorted and filtered, the first products of each page in full and the rest as ids); exact store units with the aisle and pickup per store for a Brazilian price region; Brazilian delivery quotes and CEP lookup; the 28 Brazilian price regions and department tree; stores and one store with hours; reviews with the star split (no names); Italy's offers page; search suggestions. 13 endpoints; credits per market: Brazil 1, Italy 1 (product and category 2), Romania 1, Spain, Portugal and Poland 2, France 5. Store stock Brazil only; no search for France; no price history."
version: 1.0.0
tags: leroy-merlin, leroymerlin, leroy-merlin-api, leroy-merlin-brasil, leroymerlin-com-br, leroymerlin-it, leroymerlin-es, leroymerlin-pt, leroymerlin-pl, leroymerlin-ro, leroymerlin-fr, adeo, home-improvement, home-improvement-prices, diy, bricolage, construction-materials, materiais-de-construcao, ferramentas, tools-prices, power-tools, store-stock, estoque-loja, store-inventory, aisle, store-pickup, price-region, regional-prices, cep, frete, delivery-quote, black-friday-brasil, offerte, promotions, marketplace-offers, ean, gtin, price-excluding-vat, unit-price, reviews, store-locator, brazil, italy, spain, portugal, poland, romania, france, brl, eur, pln, ron, price-monitoring, agents, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/leroymerlin-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api
---

# Leroy Merlin API - Prices by Country, Store Stock, Stores, Shipping, Reviews

Read Leroy Merlin (the home improvement retailer of the ADEO group) in seven markets with `country`: `br` (leroymerlin.com.br, pt-BR, BRL), `it` (EUR), `es` (EUR), `pt` (EUR), `pl` (PLN), `ro` (RON) and `fr` (EUR). Keyword search, category listings, one product, exact store stock with the aisle in Brazil, stores and one store, reviews, Brazilian delivery quotes, CEP lookup, price regions and the department tree, Italy's offers page and search suggestions. Data comes in the market's language and currency. Every endpoint returns structured JSON; credits follow the market (Brazil 1).

**The job this skill is for: what a home improvement product costs at Leroy Merlin today, in a given market or Brazilian price region, and which store has it.** Leroy Merlin Brasil sets prices per region and reports exact units per store, and this skill returns each one as the site shows it, never computed. On 2026-11-27 the Wap WF 12K3.2 12V cordless drill (product `92450351`) in the `grande_sao_paulo` region read `price` R$ 129,90 against `original_price` R$ 149,90 (13 percent off), 6x R$ 21,65, `tag` Black Friday, with 225 units in the Ferramentas aisle at the Raposo Tavares store, 216 at Marginal Tiete, and 12 of the region's 16 stores in stock. Delivery to the CEP 01310-100 (Avenida Paulista) quoted standard R$ 9,90 in 1 day, express R$ 39,90 the same day and free store pickup ready in 2 hours. A Makita DHP490WVX 18V drill read R$ 599,90 against R$ 744,57 on a promotion ending 2026-11-28. On leroymerlin.it a DEWALT DCF887N impact driver read 98,90 EUR (81,07 EUR excluding VAT) with 18 offers.

Eight limits shape every answer, so say them plainly:
- **Credits follow the market.** Billed on what the request spent: Brazil 1 on every endpoint; Italy 1, product and category pages 2; Romania 1; Spain, Portugal and Poland 2; France 5. Stores by place in Europe can cost double (two lookups). `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Brazil needs a region.** Leroy Merlin Brasil prices differ per region: `region` (one of 28, from `/regions`) is required on every priced Brazil call, and every price is that region's. Prices are set per region, not per store.
- **Store stock is Brazil only.** `/store-stock` returns exact units, the aisle and pickup for every store of a Brazilian price region (or one store). The European sites do not hold a chosen store, so there is no store stock in Europe.
- **Europe lists the first products in full.** A European listing page of 48 carries full details for the first products only (10 to 18 in the captures, all 48 in Romania); the rest come in `other_products` as ids. Pass an id to `/product` for its details.
- **Not every endpoint in every market.** France has no keyword search (use category or a product link); Spain has no stores or reviews right now; suggestions cover Italy, Spain, Portugal and Poland; the offers page is Italy's. See the market table below.
- **Units are the site's.** A price is per `unit` (cada = each, m2, rolo = roll); `package` gives the box price of an item sold by the m2. Europe gives `unit_price` as the page writes it (3,56 EUR / Litro).
- **Brazil listings are slow.** Brazil search and category can take 30-180 seconds. Set a client timeout of at least 240 seconds for them.
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

Leroy Merlin has no public API for its catalog, prices or store stock. Prices and stock are shown on the Leroy Merlin sites for each product, and this skill reads those public pages with one Scavio key.

See also: IKEA `ikea-api`, Home Depot `home-depot-product-data`, Lowe's `lowes-product-data`; in Brazil, the price comparison sites Buscape and Zoom `buscape-zoom-api` (match on EAN).

## When to trigger

Use this skill when the user asks to:
- Price a product at Leroy Merlin Brasil in a price region (Grande Sao Paulo, Rio de Janeiro, ...): price, original price, discount, installments, unit and box price, promotion dates, Black Friday tag
- Check exact Leroy Merlin Brasil store stock for a product across a region's stores, with the aisle and store pickup
- Quote Leroy Merlin Brasil delivery to a CEP (Brazilian postal code): standard, scheduled, express and store pickup with cost and days
- Price a product at Leroy Merlin Italy, Spain, Portugal, Poland, Romania or France, with the price excluding VAT, unit price, promotion dates and delivery options
- Search Leroy Merlin by keyword in Brazil, Italy, Spain, Portugal, Poland or Romania, or list a category in any of the seven markets, sorted by price and filtered by brand or any filter (Europe)
- List Leroy Merlin Italy's offers (offerte) with their validity dates
- Find Leroy Merlin stores in Brazil (by state, region or distance) or near a city or postcode in Italy, Portugal, Poland, Romania or France, or read one store's hours
- Read Leroy Merlin reviews with the star split
- Read the Leroy Merlin Brasil price regions, the department tree, an address for a CEP, or search suggestions

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Brazil calls cost 1 credit, so 50 credits cover 50 Brazil calls (25 in Spain, Portugal or Poland, 10 in France).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Calls usually take 1-12 seconds (in the captures: regions 0.4, suggestions 0.6, cep 0.6, reviews 1.5, shipping 1.6, store 2.8, category 3.0, store stock 3.3, categories 4.1, offers 4.7, stores 4.9, product 11.7); Brazil search took 33.5 and can take up to 180. Allow a client timeout of at least 240 seconds.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/leroymerlin/search` | Keywords: Brazil 36 per page priced for the region; Europe 48 per page, sorted and filtered, first products in full, rest as ids | br 1, it 1, ro 1, es / pt / pl 2 |
| `POST /api/v1/leroymerlin/category` | One category by slug, path or link, same shapes as search; a landing page answers its subcategories | br 1, it 2, ro 1, es / pt / pl 2, fr 5 |
| `POST /api/v1/leroymerlin/product` | One product: prices, discount, installments, unit and box price, tag, seller, specs, EAN; Brazil adds store stock and marketplace offers; Europe adds price excluding VAT, unit price, deliveries | br 1, it 2, ro 1, es / pt / pl 2, fr 5 |
| `POST /api/v1/leroymerlin/store-stock` | Exact units, aisle and pickup for every store of a Brazilian price region, or one store | 1 (Brazil only) |
| `POST /api/v1/leroymerlin/stores` | Brazil: the store list by region, state or distance; Europe: the up to 10 stores nearest a place or point | br 1, it 1, ro 1, pt / pl 2-4, fr 5-10 |
| `POST /api/v1/leroymerlin/store` | One store: address, hours; Europe adds phone, weekly hours and special hours | per market |
| `POST /api/v1/leroymerlin/reviews` | A page of reviews and the rating summary (Brazil 6, Europe 8 per page) | per market |
| `POST /api/v1/leroymerlin/shipping` | Leroy Merlin Brasil delivery quote to a CEP: standard, scheduled, express, store pickup | 1 (Brazil only) |
| `POST /api/v1/leroymerlin/cep` | The address Leroy Merlin Brasil holds for a CEP | 1 (Brazil only) |
| `POST /api/v1/leroymerlin/regions` | The 28 Brazilian price regions | 1 (Brazil only) |
| `POST /api/v1/leroymerlin/categories` | The Leroy Merlin Brasil department tree, or one category's subtree | 1 (Brazil only) |
| `POST /api/v1/leroymerlin/suggestions` | Search box suggestions | it 1, es / pt / pl 2 |
| `POST /api/v1/leroymerlin/offers` | Leroy Merlin Italia's offers page as a product list | 1 (Italy only) |

### Endpoints per market

| Endpoint | br | it | es | pt | pl | ro | fr |
|---|---|---|---|---|---|---|---|
| search | yes (`region`) | yes | yes | yes | yes | yes | no |
| category | yes (`region`) | yes | yes | yes | yes | yes | yes |
| product | yes (`region`) | yes | yes | yes | yes | yes | yes (`url` only) |
| store-stock | yes | no | no | no | no | no | no |
| stores, store | yes | yes | no | yes | yes | yes | yes |
| reviews | yes | yes | no | yes | yes | yes | no |
| suggestions | no | yes | yes | yes | yes | no | no |
| offers | no | yes | no | no | no | no | no |
| shipping, cep, regions, categories | yes | no | no | no | no | no | no |

Every answer carries `site` (leroymerlin.com.br, leroymerlin.it, ...), `country`, `language` and `currency`.

## Prices, units and stock

| Field | Meaning |
|---|---|
| `price`, `original_price` | The current price and the struck-through price, in the market's currency (Brazil: the region's) |
| `region`, `priced_for_region` (Brazil) | The region asked for and the region the site priced |
| `unit`, `package` (Brazil) | The unit the price is for (cada, m2, rolo); `{quantity, unit, label, price}` for a box sold by the m2 |
| `discount` (Brazil product) | `{percent, type, condition}`; listings carry `discount_type`, `offer {label, percent}`, `promotion_start`, `promotion_end`, `black_friday` |
| `installments` (Brazil) | `{count, value, total}` |
| `price_excluding_vat`, `unit_price`, `price_validity` (Europe) | The price without VAT, the unit price as the page writes it, and the page's promotion dates line |
| `seller`, `marketplace_offers` | Leroy Merlin or a marketplace seller, and the other offers for the product |
| `store_stock` (Brazil product), `/store-stock` | `{unit, count, in_stock_count, stores[] {store_id, name, units, in_stock, message, aisle, pickup_in_store, address, pickup_hours}}` |

- Quote "Wap WF 12K3.2 drill: R$ 129,90 at Leroy Merlin Brasil, Grande Sao Paulo region, 2026-11-27 (was R$ 149,90)", always with the region in Brazil and the market elsewhere.
- Store units: "225 units at Raposo Tavares, aisle Ferramentas, on 2026-11-27". Units are as Leroy Merlin Brasil reports them and change through the day; Scavio makes no promise of their accuracy.
- Never compare a Brazilian price with a European one without naming both currencies; never convert currencies yourself.
- Report the site's prices, dates and units and the arithmetic only. Never judge a price as a good deal.

## Workflow

1. **Brazil: pick the region.** `/regions` once for the 28 `region` values (`grande_sao_paulo`, `rio_de_janeiro`, ...).
2. **Find the product.** `/search` with `country` and `query` (`furadeira` in Brazil, `trapano` in Italy) and, in Brazil, `region`; or `/category` with a slug (`furadeiras`, from `/categories`) or a European category path. In France use `/category` or a product link.
3. **Europe: the rest of the page.** Ids in `other_products` go to `/product` for their details.
4. **One product.** `/product` with `id` (or `url`; France needs `url`) and, in Brazil, `region`: prices, discount, specs, and in Brazil the region's store stock and marketplace offers.
5. **Store stock (Brazil).** `/store-stock` with `id`, `region` and optionally `store` for exact units and aisle.
6. **Delivery (Brazil).** `/shipping` with `id`, `region` and `cep`; `/cep` alone for the address.
7. **Stores.** `/stores` with `region`, `state` or `latitude` / `longitude` in Brazil, or `place` (a city or postcode) in Europe; `/store` with `store` (Brazil) or the store page `url` (Europe).
8. **Watching prices:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

| Endpoint | Param | Notes |
|---|---|---|
| all | `country` | `br`, `it`, `es`, `pt`, `pl`, `ro`, `fr`. Required on search, category, product, stores, store, reviews; `br` by default on the Brazil-only endpoints; `it` on offers |
| priced Brazil calls | `region` | Required in Brazil on search, category, product, store-stock and shipping: one of the 28 regions from `/regions` |
| search | `query` | Keywords or a reference number, 2-120 characters. In Europe a reference number or some keywords redirect to a product or category page (`redirected_to`) |
| search, category, offers | `page` | From 1. Search reaches up to 10 pages in Europe (48 a page) and 28 in Brazil (36 a page) |
| search, category, offers | `sort` | `relevance` (default), `price_asc`, `price_desc`. Brazil: category only (keyword search keeps the site's order) |
| search, category, offers | `filters` | Europe only: `{code: value or [values]}` from `filters_available` (`{"attribute-06575": "BOSCH"}`, `vendor-1P` sold by Leroy Merlin) |
| category | `category` | Brazil: a slug or link (`furadeiras`). Europe: a path or link (`/prodotti/utensileria/elettroutensili/trapani-e-avvitatori/`) |
| product, store-stock, reviews, shipping | `id` / `url` | The product reference number (`92450351`) or a product link; send one. France: `url` |
| store-stock | `store` | Optional: one store of the region (`raposo_tav`) |
| stores | `place` / `latitude` + `longitude` | Europe: a city or postcode (`Milano`), or a point. Brazil: `latitude` / `longitude` sort by distance |
| stores | `state` | Brazil: a state code (`SP`) |
| store | `store` / `url` | Brazil: the store id. Europe: the store page link (`stores[].url`) |
| reviews | `sort`, `rating` | Europe: `newest`, `oldest`, `highest_rating`, `lowest_rating`, and a star filter. Brazil: `most_helpful` only, no star filter |
| shipping, cep | `cep` | A Brazilian CEP, 8 digits (`01310-100`) |
| categories | `category`, `depth` | A category's subtree; levels 1-4 (default 2) |
| suggestions | `query` | 2-80 characters (`trapano`) |

## Examples

### One Brazilian product with store stock

`POST /api/v1/leroymerlin/product` with `{"country": "br", "id": "92450351", "region": "grande_sao_paulo"}` (1 credit), trimmed from the 2026-11-27 capture:

```json
{
  "site": "leroymerlin.com.br",
  "country": "br",
  "currency": "BRL",
  "id": "92450351",
  "name": "Furadeira e Parafusadeira Wap WF 12K3.2 a Bateria 12V 3/8\" com Maleta e Acessórios",
  "brand": "Wap",
  "ean": "7899831338634",
  "region": "grande_sao_paulo",
  "priced_for_region": "grande_sao_paulo",
  "price": 129.9,
  "original_price": 149.9,
  "unit": "cada",
  "discount": { "percent": 13, "type": "stampedPrice", "condition": null },
  "installments": { "count": 6, "value": 21.65, "total": 129.9 },
  "package": null,
  "tag": "Black Friday",
  "sold_out": false,
  "available_online": true,
  "seller": "Leroy Merlin",
  "pickup_in_store": true,
  "store_stock": {
    "unit": "cada",
    "count": 16,
    "in_stock_count": 12,
    "stores": [
      { "store_id": "raposo_tav", "name": "Raposo Tavares", "units": 225, "in_stock": true, "message": "225 peças em estoque", "aisle": "Ferramentas", "pickup_in_store": true },
      { "store_id": "tiete_sap", "name": "Marginal Tietê", "units": 216, "in_stock": true, "message": "216 peças em estoque", "aisle": "Ferramentas", "pickup_in_store": true }
    ]
  }
}
```

### Store stock for a region

`POST /api/v1/leroymerlin/store-stock` with `{"country": "br", "id": "85277934", "region": "rio_de_janeiro"}` (1 credit): `unit` rolo, `count` 4 stores, `in_stock_count` 4, `total_units` 469; Rio Barra 218 rolls (aisle Eletricidade, pickup Monday to Saturday 08:00-18:00), Del Castilho 135. Each store carries `address` and `pickup_hours`.

### Delivery quote to a CEP

`POST /api/v1/leroymerlin/shipping` with `{"id": "92450351", "region": "grande_sao_paulo", "cep": "01310-100"}` (1 credit):

```json
{
  "product_id": "92450351",
  "cep": "01310100",
  "address": { "street": "Avenida Paulista", "district": "Bela Vista", "city": "São Paulo", "state": "SP" },
  "standard": { "cost": 9.9, "deadline_days": 1 },
  "scheduled": { "cost": 9.9, "deadline_days": 5 },
  "express": { "cost": 39.9, "deadline_days": 0 },
  "pickup_in_store": { "cost": 0, "ready_in_hours": 2, "store_id": "raposo_tav" }
}
```

### A European category page

`POST /api/v1/leroymerlin/category` with `{"country": "it", "category": "/prodotti/utensileria/elettroutensili/trapani-e-avvitatori/avvitatori-a-impulsi/"}` (2 credits): `total` 358 over 8 pages, `products_on_page` 48, 10 in full and 38 in `other_products` as ids.

```json
{
  "position": 1,
  "id": "82179500",
  "name": "Avvitatore a impulsi a batteria DEWALT DCF887N 18V (batteria non inclusa)",
  "brand": "DEWALT",
  "price": 98.9,
  "price_excluding_vat": 81.07,
  "original_price": null,
  "currency": "EUR",
  "rating": 5,
  "review_count": 11,
  "seller": { "name": "Leroy Merlin", "type": "leroy_merlin" },
  "offer_count": 18,
  "sponsored": false,
  "delivery": "Ritiro gratuito 5 giorni feriali in negozio"
}
```

`filters_available` lists the codes for `filters`: `vendor-1P` (Venduto da Leroy Merlin), `price-type` (Prodotti in offerta), `attribute-06575` (Marca).

### Search, offers, stores, store, reviews and the Brazil lookups

- `/search` `{"country": "br", "query": "furadeira", "region": "grande_sao_paulo"}`: `total` 401 over 12 pages of 36; Philco 21V drill R$ 199,90 (Oferta 6 percent), Makita DHP490WVX R$ 599,90 against R$ 744,57 with `promotion_start` 2026-11-26T03:00Z and `promotion_end` 2026-11-28T02:59Z, each with `eans` and `sellers`.
- `/offers` `{"country": "it"}`: 923 products over 20 pages; an abrasive sponge pack 1,48 EUR against 2,99 EUR with `price_validity` "Prezzi validi dal 11 novembre al 29 novembre".
- `/stores` `{"country": "it", "place": "Milano"}`: `matched_place` 20121 Milano, 10 stores, Rozzano (MI) first at 9.4 km, then Baranzate (MI) at 16.1 km; `/store` with its `url`: phone, weekly `hours` (Monday 07:00-20:30) and `special_hours` (2026-12-08).
- `/reviews` `{"country": "it", "id": "83085630"}`: `average_rating` 4.6 from 295 reviews (210 five-star), 8 per page with `verified_purchase`, `experience`, and `syndicated` reviews from leroymerlin.pt or leroymerlin.es with `translated_text`. No reviewer names.
- `/regions` `{}`: 28 regions (`acre`, `alagoas`, ...); `/categories` `{}`: 26 departments (Ar e Ventilacao with 24 children, ...); `/cep` `{"cep": "01310-100"}`: Avenida Paulista, Bela Vista, Sao Paulo, SP; `/suggestions` `{"country": "it", "query": "trapano"}`: 14 suggestions (Frese per trapano, Punte per trapano, ...).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def lm(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/leroymerlin/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Search in a Brazilian price region (1 credit; Brazil listings can take minutes)
hits = lm("search", {"country": "br", "query": "furadeira", "region": "grande_sao_paulo"})["data"]
pid = hits["products"][0]["id"]

# 2. Exact units per store in the region (1 credit)
stock = lm("store-stock", {"country": "br", "id": pid, "region": "grande_sao_paulo"})["data"]
for s in stock["stores"]:
    print(s["name"], s["units"], s["aisle"], s["pickup_in_store"])

# 3. Delivery quote to a CEP (1 credit)
q = lm("shipping", {"id": pid, "region": "grande_sao_paulo", "cep": "01310-100"})["data"]
print(q["standard"], q["express"], q["pickup_in_store"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `site`, `country`, `language` and `currency`, and most carry `notes`.

- **search / category (Brazil)** - `query` or `category`, `region`, `sort`, `page`, `page_size` (36), `total`, `total_pages`, `count`, `products[]` {`position`, `id`, `name`, `short_name`, `brand`, `url`, `image`, `unit`, `price`, `original_price`, `currency`, `discount_type`, `payment_discount`, `promotion_start`, `promotion_end`, `offer` {`label`, `percent`}, `black_friday`, `free_shipping`, `express_shipping`, `in_stock`, `available`, `sellers`, `eans`}.
- **search / category / offers (Europe)** - `query` or `category`, `redirected_to` {`type`, `url`}, `listing`, `page`, `page_size` (48), `total`, `total_pages`, `count`, `products_on_page`, `products[]` {`position`, `id`, `name`, `brand`, `url`, `image`, `price`, `price_excluding_vat`, `original_price`, `discount_percent`, `currency`, `unit_price`, `price_validity`, `promotion`, `rating`, `review_count`, `seller` {`name`, `type`}, `offer_count`, `marketing_tags`, `sponsored`, `delivery`}, `other_products[]` {`position`, `id`, `sponsored`}, `sorts`, `applied_filters`, `filters_available[]` {`code`, `label`, `type`, `values[]` {`value`, `count`, `applied`}}, `subcategories[]`.
- **product (Brazil)** - `id`, `name`, `short_name`, `brand`, `ean`, `url`, `region`, `priced_for_region`, `price`, `original_price`, `unit`, `package`, `discount`, `installments`, `tag`, `sold_out`, `available_online`, `seller`, `pickup_in_store`, `category_path`, `images`, `specifications[]` {`name`, `value`}, `store_stock`, `marketplace_offer_count`, `marketplace_offers[]` {`seller`, `selected`, `price`, `original_price`, `discount`, `installments`, `free_shipping`, `pickup_in_store`}.
- **product (Europe)** - `id`, `name`, `brand`, `gtin`, `url`, `price`, `price_excluding_vat`, `original_price`, `discount_percent`, `sold_by_unit`, `unit_price`, `price_validity`, `availability`, `rating`, `review_count`, `seller`, `deliveries[]` {`type`, `price`, `stock_status`, `lead_time`}, `marketplace_offer_count`, `marketplace_offers[]`, `marketing_tags`, `breadcrumbs`, `images`, `specifications`.
- **store-stock** - `product_id`, `region`, `unit`, `count`, `in_stock_count`, `total_units`, `stores[]` {`store_id`, `store_code`, `name`, `units`, `in_stock`, `message`, `aisle`, `pickup_in_store`, `address`, `pickup_hours`}.
- **stores** - Brazil: `count`, `stores[]` {`position`, `store_id`, `name`, `hours_text`, `address`, `state`, `cep`, `latitude`, `longitude`, `distance_km`}. Europe: `place`, `matched_place`, `latitude`, `longitude`, `count`, `stores[]` {`position`, `store_id`, `name`, `city`, `distance_km`, `open_now_text`, `hours_text`, `address_lines`, `url`}.
- **store** - Brazil: `store_id`, `name`, `hours_text`, `address`, `state`, `cep`, `latitude`, `longitude`. Europe: `store_id`, `name`, `url`, `address` {`street`, `postal_code`, `city`, `country`}, `phone`, `latitude`, `longitude`, `hours[]` {`day`, `open`, `close`}, `special_hours[]` {`from`, `to`, `open`, `close`}.
- **reviews** - `product_id`, `sort`, `rating`, `average_rating`, `total_reviews`, `rating_distribution`, `page`, `total_pages`, `count`, `reviews[]` {`id`, `rating`, `title`, `text`, `date` or `date_text`, `recommended`, `helpful_count`, `not_helpful_count`, plus in Europe `translated_title`, `translated_text`, `verified_purchase`, `badge`, `experience`, `usage`, `syndicated`, `source_site`, and in Brazil `photos`}.
- **shipping** - `product_id`, `cep`, `region`, `address`, `currency`, `standard` / `scheduled` / `express` {`cost`, `deadline_days`}, `pickup_in_store` {`cost`, `ready_in_hours`, `store_id`}.
- **cep** - `cep`, `street`, `district`, `city`, `state`, `ibge_code`. **regions** - `count`, `regions[]` {`region`, `name`, `state`}. **categories** - `root`, `depth`, `count`, `categories[]` {`name`, `url`, `category`, `child_count`, `children`}. **suggestions** - `query`, `count`, `suggestions[]` {`type`, `type_label`, `label`, `url`}.

## Guardrails

- Name it "Leroy Merlin (the home improvement retailer of the ADEO group)" on first mention, with the market (Leroy Merlin Brasil, Leroy Merlin Italia, ...).
- Prices: quote `price`, `original_price`, the currency and the `fetched_at` date, with the region in Brazil. Brazilian prices are set per region, never per store.
- Store stock: quote `units` and `aisle` per store with the date, as Leroy Merlin Brasil reports them. Never claim store stock in a European market: there is none.
- Partial European listings: say when a page's products came as ids in `other_products`, and read `/product` for them before quoting their prices.
- Reviews: no reviewer names are returned. Quote a review as "a Leroy Merlin customer review" and say when it is `syndicated` from another market (with its translated text as given).
- Images and copy: do not republish Leroy Merlin's product images or copy; link products by `id` instead.
- Not available: keyword search in France, stores and reviews in Spain, store stock outside Brazil, suggestions in Brazil, Romania and France, Ukraine and Greece, flyers, price history (poll and store), account data, cart or checkout. This API cannot reserve or buy an item.
- Terms: Scavio does not store Leroy Merlin data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Read the Leroy Merlin sites' current terms of use for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, units, aisles, stores, delivery quotes, ratings or dates. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "region is required for Brazil: prices differ per region. One of ... (regions lists them)."; "region applies to Brazil only (country br)."; "id (the product reference number) or url (a product link) is required."; "Send id or url, not both."; "For France send url (the product link): id lookups go through keyword search, which is not available for France."; "Store stock is available for Brazil only."; "sort is not available for Brazil keyword search (the site keeps its own order). Category listings for Brazil accept price_asc and price_desc."; "filters are not available for Brazil listings."; "place is not available for Brazil: send latitude and longitude, region or state."; "cep must be a Brazilian CEP: 8 digits (01310-100)."; "rating is not available for Brazil reviews."; an endpoint a market does not have ("... not available for France.", "... not available for Romania (the site has no suggestion service).").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Leroy Merlin Brasil product <id>.", "No Leroy Merlin product <id> on leroymerlin.it.", "No Leroy Merlin category at this path. Check the link.", "No Leroy Merlin Brasil category <slug> in the category tree.", "No Leroy Merlin Brasil store <id> (stores lists them).", "No place matched \"<place>\" on leroymerlin.it.", "No products on this page (past the last page, or no match).".
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api).
- `503` on Brazil search or category can mean the Brazil listings are paused ("Leroy Merlin search and category listings are not available for Brazil right now. Product, store stock, reviews and shipping work for Brazil."). It is not charged.
- `502` and `503` otherwise mean Leroy Merlin data was temporarily unavailable ("Leroy Merlin is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). Some market endpoints answer "... not available for Spain right now (...did not answer)." They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.102.0
npm install scavio@0.103.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.leroymerlin.search({ country: "br", query: "furadeira", region: "grande_sao_paulo" });
const { data: grid } = await scavio.leroymerlin.category({ country: "it", category: "/prodotti/utensileria/elettroutensili/trapani-e-avvitatori/" });
const { data: product } = await scavio.leroymerlin.product({ country: "br", id: "92450351", region: "grande_sao_paulo" });
const { data: stock } = await scavio.leroymerlin.storeStock({ country: "br", id: "85277934", region: "rio_de_janeiro" });
const { data: near } = await scavio.leroymerlin.stores({ country: "it", place: "Milano" });
const { data: store } = await scavio.leroymerlin.store({ country: "it", url: "https://www.leroymerlin.it/negozi/rozzano-mi.html" });
const { data: reviews } = await scavio.leroymerlin.reviews({ country: "it", id: "83085630", sort: "newest" });
const { data: quote } = await scavio.leroymerlin.shipping({ id: "92450351", region: "grande_sao_paulo", cep: "01310-100" });
const { data: address } = await scavio.leroymerlin.cep({ cep: "01310-100" });
const { data: regions } = await scavio.leroymerlin.regions({});
const { data: tree } = await scavio.leroymerlin.categories({ depth: 2 });
const { data: typed } = await scavio.leroymerlin.suggestions({ country: "it", query: "trapano" });
const { data: offers } = await scavio.leroymerlin.offers({ country: "it", sort: "price_asc" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.leroymerlin.search(...)`, `category`, `product`, `store_stock`, `stores`, `store`, `reviews`, `shipping`, `cep`, `regions`, `categories`, `suggestions` and `offers`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 13 endpoints as tools: `search_leroymerlin`, `get_leroymerlin_category`, `get_leroymerlin_offers`, `get_leroymerlin_product`, `get_leroymerlin_store_stock`, `get_leroymerlin_stores`, `get_leroymerlin_store`, `get_leroymerlin_reviews`, `get_leroymerlin_shipping`, `get_leroymerlin_cep`, `get_leroymerlin_regions`, `get_leroymerlin_categories` and `get_leroymerlin_suggestions`. Leroy Merlin is opt-in: add `leroymerlin` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.102.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,leroymerlin"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/leroymerlin-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api), [category](https://scavio.dev/docs/leroymerlin-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api), [product](https://scavio.dev/docs/leroymerlin-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api), [store stock](https://scavio.dev/docs/leroymerlin-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api), [stores](https://scavio.dev/docs/leroymerlin-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api), [store](https://scavio.dev/docs/leroymerlin-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api), [reviews](https://scavio.dev/docs/leroymerlin-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api), [shipping](https://scavio.dev/docs/leroymerlin-shipping?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api), [cep](https://scavio.dev/docs/leroymerlin-cep?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api), [regions](https://scavio.dev/docs/leroymerlin-regions?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api), [categories](https://scavio.dev/docs/leroymerlin-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api), [suggestions](https://scavio.dev/docs/leroymerlin-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api) and [offers](https://scavio.dev/docs/leroymerlin-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api). The platform page is [scavio.dev/leroymerlin-api](https://scavio.dev/leroymerlin-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=leroy-merlin-api).
