# Drogasil + Droga Raia API - Prices, Deals, Store Pickup, Stores, Reviews

Read Drogasil and Droga Raia (drogasil.com.br, drogaraia.com.br, the pharmacy chains of RD Saude): keyword, product code or EAN search, category listings, the menu tree, one product with its price steps, prices of up to 48 products in one call, store pickup availability, the stores near a CEP, the store locator, reviews, deals and coupons, and search suggestions. `site` picks the banner: `drogasil` (default) or `drogaraia`. Prices, category ids, stores and reviews differ per banner. Brazil only, Portuguese text, prices in BRL. Every endpoint returns structured JSON and costs 1 credit.

**The job this skill is for: what a pharmacy-aisle product costs at Drogasil or Droga Raia online today, with which deal, and which store can hand it over.** The sites show several price steps and this skill returns each one as given, never computed. On 2026-11-27 on Drogasil the Kit Nivea Sun Protect & Hidrata body sunscreen FPS 50 200ml + 100ml (sku `72654`) read `price` R$ 43,99 against `list_price` R$ 72,99 (`price_type` OFFER, 39.73 percent off) with the label "Cupom NIVEABRAND", and the Eucerin Oil Control serum sunscreen FPS 75 30ml read R$ 84,99 against R$ 119,90. On Droga Raia a Principia FPS 70 facial sunscreen 30ml read R$ 49 or R$ 36,75 each when buying 2 or more (`quantity_discount`, leve mais pague menos), and a marketplace partner (Epoca Cosmeticos) sold an Australian Gold FPS 30 body sunscreen at R$ 49,98 against R$ 73,99, R$ 47,48 by Pix (Brazil's instant payment, 5 percent off). A Droga Raia Episol FPS 50 compact powder sunscreen was available for store pickup at two Porto Alegre stores.

Eight limits shape every answer, so say them plainly:
- **1 credit on every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **A reference price, not a store price.** Prices are the site's default online price for a visitor it has not placed in a state. The site shows the same price at every store; there are no per-store prices.
- **Never card or loyalty prices.** Card prices and loyalty-program prices are not returned. `lab_program` (a manufacturer benefit-program price) is passed through as given and needs enrolment.
- **The banner matters.** Drogasil and Droga Raia have their own prices, category ids, stores and review pools. Quote the `site` with every number, and take category ids from `/categories` of the same banner.
- **Pickup is yes or no.** `/store-availability` answers the site's own store-pickup filter (Retire na loja) per store: `pickup_available` true or false, never unit counts. Up to 5 product x store checks per call.
- **Search depth is the site's.** The site's search reaches about 2,016 results by relevance and about 1,008 sorted by price (`reachable_pages`). The price sort and price range use the search index's price (`index_price`), which can differ from the live price.
- **Regulatory fields are as given.** `regulatory` (Anvisa registration, tarja and its code, controlled, antibiotic, psychotropic and thermolabile flags) is passed through exactly as the site gives it. Describe it as the site's label; this skill does not interpret it.
- **No history, no descriptions.** Everything is the page at the moment of the call; Scavio keeps nothing. Product descriptions and leaflet text are not returned, and deals carry no start or end dates. Poll and store your own series.

Neither Drogasil nor Droga Raia has a public API for its catalog, prices or stores. Prices are shown on the sites for each product, and this skill reads those public pages with one Scavio key.

See also: CVS `cvs-product-data`, Walgreens `walgreens-product-data`, Boots `boots-uk-api`; the price comparison sites Buscape and Zoom `buscape-zoom-api` (match on EAN).

## When to trigger

Use this skill when the user asks to:
- Price a product at Drogasil or Droga Raia online: sunscreen, shampoo, vitamins, diapers, skincare, personal care; price, list price, discount, the quantity discount (leve mais pague menos), Pix discount, coupon labels
- Price a list of up to 48 products in one call, by product code
- Search drogasil.com.br or drogaraia.com.br by keyword, product code or EAN, sorted by relevance or price, filtered by brand, own or partner store, highlight (Oferta do Dia, % Especial, Black Friday, a coupon), category, store pickup or price range
- Browse a Drogasil or Droga Raia category, or read the menu tree
- List the Oferta do Dia, % Especial or Black Friday deals, the running coupons, or the products one coupon covers
- Check whether products can be picked up at given Drogasil or Droga Raia stores
- Find the Drogasil or Droga Raia stores nearest a CEP (Brazilian postal code), or every store in a state, city or neighborhood, with hours and 24-hour, parking and Farmacia Popular flags
- Read customer reviews of a product with the star split and the site's own summary
- Read search suggestions for a partial query

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Calls usually take 2-15 seconds (in the captures: product 1.1, suggestions 1.1, category 1.2, reviews 2.4, prices 3.5, stores 3.6, store availability 4.0, deals 4.2, store locator 4.8, search 5.9); categories and the store locator can take 10-35 seconds. Allow a client timeout of at least 180 seconds.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/rdsaude/search` | Keyword, product code or EAN: 24, 36 or 48 items per page with price, list price, discount, price type, quantity discount, labels, seller, stock, regulatory fields; facets | 1 |
| `POST /api/v1/rdsaude/category` | One category by id or page link, same items, sorts and filters as search | 1 |
| `POST /api/v1/rdsaude/categories` | The banner's menu tree, three levels, with ids | 1 |
| `POST /api/v1/rdsaude/product` | One product by sku or link: prices, the site's price steps, payment discounts, seller, variants, kits, EAN, quantity, regulatory fields | 1 |
| `POST /api/v1/rdsaude/prices` | Current prices of 1 to 48 products in one call | 1 |
| `POST /api/v1/rdsaude/store-availability` | Store pickup yes or no for up to 5 product x store checks | 1 |
| `POST /api/v1/rdsaude/stores` | The up to 6 nearest stores of the banner to a CEP, with distance, phone, hours and flags | 1 |
| `POST /api/v1/rdsaude/stores/search` | The store locator by state, city, neighborhood or free text, up to 50 per page | 1 |
| `POST /api/v1/rdsaude/reviews` | Reviews of one product, up to 50 per page, by stars, with the star split and the site's own summary | 1 |
| `POST /api/v1/rdsaude/deals` | Oferta do Dia, % Especial, Black Friday, or the running coupons and one coupon's products | 1 |
| `POST /api/v1/rdsaude/suggestions` | Search box suggestions and quick filters for what has been typed | 1 |

Every answer carries `site`, `site_name` (Drogasil or Droga Raia), `country` (br), `currency` (BRL) and `language` (pt-BR).

## Prices and price steps

| Field | Meaning |
|---|---|
| `price` | The price shown, BRL (the site's default online price, a reference price) |
| `list_price` | The list price as the site gives it |
| `discount_percent` | The site's discount from the list price |
| `price_type` | The site's price type: OFFER, LMPM (a quantity price), ... as given |
| `quantity_discount` | `{min_quantity, unit_price}`: the unit price when buying `min_quantity` or more (leve mais pague menos) |
| `index_price` | The search index's price, used by the price sort and range; can differ from `price` |
| `labels` | The site's highlight labels on the item ("Cupom NIVEABRAND", "Oferta do Dia") |
| `price_ladder` (product) | `{list_price, offers[] {description, price, discount_percent, discount_value}, quantity_discount, lab_program, payment_discounts[] {method, discount_percent, price}, price_hierarchy[] {rank, type, value, ...}}`: the site's own price steps as given |
| `sold_by`, `delivered_by`, `seller` | Drogasil / Raia itself or a marketplace partner (`seller {is_partner, seller_id, name}`, the partner's business name) |

- Quote "Kit Nivea Sun Protect & Hidrata FPS 50: R$ 43,99 on drogasil.com.br on 2026-11-27 (list price R$ 72,99)", with the banner and date.
- A quantity price is "R$ 36,75 each when buying 2 or more", from `quantity_discount`; never present it as the single-unit price.
- A Pix price comes only from `payment_discounts` (method PIX) on the product; never compute one.
- Offer names in `price_ladder.offers[].description` are passed through as given and can name a branch.
- Report the sites' prices, labels and steps and the arithmetic only. Never judge a price as a good deal.

## Workflow

1. **Find the product.** `/search` with `query` (`protetor solar`, a product code or an EAN), `/category` with a `category_id` from `/categories` of the same banner, or `/deals`. Each item's `sku` is the input of product, prices, store availability and reviews.
2. **Narrow.** Add `brand`, `seller` (`own` or `partner`), `highlight` ("Oferta do Dia", "% Especial", "Black Friday", "Cupom NIVEABRAND"), `store_id` (pickup at that store), `min_price` / `max_price`, or `facets` from a previous answer (`{"filters.Marca": "Nivea"}`).
3. **One product.** `/product` with `sku` or a product `url`: read `price_ladder`, `seller`, `variants` and `kit`.
4. **A basket of prices.** `/prices` with up to 48 `skus` for the current price, list price, discount and quantity discount of each.
5. **Stores and pickup.** `/stores` with a `cep` for the nearest stores, or `/stores/search` with `state`, `city`, `neighborhood`; then `/store-availability` with `skus` and `store_ids` (up to 5 checks).
6. **Reviews.** `/reviews` with `sku`; page with `next_cursor`, filter with `rating`.
7. **Watching prices:** there is no history. Poll `/prices` on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`) and deals (`/deals`)

| Param | Type | Notes |
|---|---|---|
| `query` | string | Search: required, keywords, a product code or an EAN in Portuguese (`protetor solar`). A CEP-looking query is a `400` (send it to stores) |
| `category_id` / `url` | string | Category: a category id (`8222`) or a category page link (its host sets the site). Search and deals: `category_id` as a filter |
| `site` | string | `drogasil` (default) or `drogaraia` |
| `sort` | string | `relevance` (default), `price_asc`, `price_desc` (by `index_price`) |
| `page`, `page_size` | integer | Page 1-100; page size 24 (default), 36 or 48 |
| `brand` | string | A brand as `facets[name=filters.Marca].values` lists it |
| `seller` | string | `own` (sold by Drogasil / Droga Raia) or `partner` (marketplace partner stores) |
| `highlight` | string | A highlight as `facets[name=filters.Destaques].values` lists it |
| `store_id` | string | Products offered for pickup at this store |
| `min_price`, `max_price` | number | Index price range in BRL |
| `facets` | object | Up to 8 other filters, `{facet name: value}` exactly as an answer lists them |
| `type`, `coupon` | string | Deals: `oferta_do_dia` (default), `especial`, `coupons`, `black_friday`; with `coupons`, a `coupon` code for its products, or none for the running coupons |

### Product, prices, store availability, reviews, suggestions

| Param | Type | Notes |
|---|---|---|
| `sku` / `url` | string | Product: a product code (`72654`) or a product page link on either site. Reviews: `sku`, required |
| `skus` | array | Prices: 1 to 48 product codes. Store availability: product codes or EANs |
| `store_ids` | array | Store availability: store ids (`stores[].store_id`); at most 5 product x store checks in all |
| `rating`, `page_size`, `cursor` | | Reviews: stars 1-5; 1-50 per page (default 20); `next_cursor` of the previous page |
| `query` | string | Suggestions: what has been typed (`shamp`) |

### Stores (`/stores`) and the store locator (`/stores/search`)

| Param | Type | Notes |
|---|---|---|
| `cep` | string | Stores: a Brazilian CEP, 8 digits (`01310-100`) |
| `state`, `city`, `neighborhood` | string | Locator: a UF code or state name (`RS`); city needs state; neighborhood needs state and city |
| `query` | string | Locator: free-text search (fuzzy) |
| `open_24h`, `parking`, `farmacia_popular` | boolean | Locator filters |
| `page`, `page_size` | integer | Locator: page 1-300; 1-50 per page (default 20) |

## Examples

### One product with its price steps

`POST /api/v1/rdsaude/product` with `{"site": "drogaraia", "sku": "1374440"}` (1 credit), trimmed from the 2026-11-27 capture:

```json
{
  "site": "drogaraia",
  "site_name": "Droga Raia",
  "currency": "BRL",
  "sku": "1374440",
  "name": "Protetor Solar Corporal Australian Gold Alta Proteção Fps 30 200g",
  "ean": "7891033504329",
  "brand": "Australian Gold",
  "in_stock": true,
  "price": 49.98,
  "list_price": 73.99,
  "discount_percent": 32.45,
  "price_ladder": {
    "list_price": 73.99,
    "offers": [{ "description": "DESCONTO CONCEDIDO PELO SELLER", "price": 49.98, "discount_percent": 32.45, "discount_value": 24.01 }],
    "quantity_discount": null,
    "lab_program": null,
    "payment_discounts": [{ "method": "PIX", "discount_percent": 5, "price": 47.48 }]
  },
  "regulatory": { "anvisa_registration": null, "tarja": "PRODUTO SEM TARJA", "tarja_code": "0" },
  "seller": { "is_partner": true, "seller_id": "epocacosmeticos", "name": "Época Cosméticos" },
  "variants": [
    { "sku": "1374440", "attributes": [{ "label": "Tamanho", "value": "200g" }], "price": 49.98, "discount_percent": 32.45, "in_stock": true },
    { "sku": "1374487", "attributes": [{ "label": "Tamanho", "value": "120g" }], "price": 40.79, "discount_percent": 20, "in_stock": false }
  ]
}
```

### Prices of several products in one call

`POST /api/v1/rdsaude/prices` with `{"skus": ["72654", "1493245", "1328295"]}` (1 credit): `requested` 3, `found` 3.

```json
{
  "items": [
    { "sku": "72654", "found": true, "name": "Kit Nivea Sun Protect & Hidrata Protetor Solar Corporal FPS 50 200ml + 100ml", "in_stock": true, "price": 43.99, "list_price": 72.99, "discount_percent": 39.73, "price_type": "OFFER", "quantity_discount": null },
    { "sku": "1493245", "found": true, "name": "Protetor Solar Eucerin Oil Control Sérum FPS 75 30ml", "in_stock": true, "price": 84.99, "list_price": 119.9, "discount_percent": 29.12, "price_type": "OFFER", "quantity_discount": null }
  ]
}
```

### Store pickup and stores

`POST /api/v1/rdsaude/store-availability` with `{"site": "drogaraia", "skus": ["38155"], "store_ids": ["200", "210"]}` (1 credit):

```json
{
  "sku_count": 1,
  "store_count": 2,
  "skus": [
    {
      "code": "38155",
      "code_type": "sku",
      "name": "Protetor Solar Facial Episol FPS 50 Tom 2 Pó Compacto 10g",
      "stores": [
        { "store_id": "200", "pickup_available": true },
        { "store_id": "210", "pickup_available": true }
      ]
    }
  ]
}
```

- `/stores` `{"cep": "01310-100"}`: 6 Drogasil stores, PAULISTA (store `1156`, Paulista 995) first at 0.043 km, open 07:00-23:00 every day, `farmacia_popular` true; SP BELA VISTA 3 at 0.339 km with parking.
- `/stores/search` `{"site": "drogaraia", "state": "RS", "city": "Porto Alegre", "page_size": 10}`: `total` 48 Droga Raia stores; ANDRADAS (store `200`, "Seg à Sáb 07:00 às 20:00") and MOINHOS DE VENTO (store `210`, every day 07:00-23:00, parking).

### Search, category, deals, reviews, categories and suggestions

- `/search` `{"query": "protetor solar"}`: `total` 5583, `reachable_pages` 84; first Eucerin Oil Control serum FPS 75 at R$ 84,99 (`index_price` 88.99, so the price sort can place it differently). Facets include `filters.Vendido por` (Drogasil 1397, Loja Parceira 4147), `filters.Destaques` (Frete gratis, Cupom NIVEABRAND), `filters.Marca`.
- `/category` `{"site": "drogaraia", "category_id": "8222"}`: 353 facial sunscreens, first a Principia FPS 70 at R$ 49 with `quantity_discount` `{"min_quantity": 2, "unit_price": 36.75}` and 7 color variants.
- `/deals` `{"site": "drogaraia", "type": "coupons", "coupon": "NIVEABRAND"}`: 195 products (Sabonete em Barra Nivea Leite 85g at R$ 3,09 against R$ 3,83); `coupons[]` lists the running coupons (NIVEABRAND 370 products, MANI5% 178). No start or end dates.
- `/reviews` `{"site": "drogaraia", "sku": "38155"}`: `total` 164, `average_rating` 4.82, `rating_distribution` {5: 144, 4: 15, 3: 2, 2: 1, 1: 2}, the site's own `summary`, `top_tags` ("Acabamento nao oleoso", "Alta protecao FPS"), `use_cases`, 20 reviews `{review_id, rating, text, date, verified, incentivized, likely_incentivized, helpful, unhelpful, replies}` and `next_cursor`. No reviewer names.
- `/categories` `{"site": "drogaraia"}`: `department_count` 9, `category_count` 379, e.g. Vida Saudavel > Vitaminas > Multivitaminas.
- `/suggestions` `{"site": "drogaraia", "query": "shamp"}`: 8 suggestions ("shampoo", ...), 83 quick filters (brands), `product_count` 14108.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def rd(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/rdsaude/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Sunscreens sold by Drogasil itself, lowest index price first (1 credit)
items = rd("search", {"query": "protetor solar", "seller": "own", "sort": "price_asc"})["data"]["items"]
skus = [i["sku"] for i in items[:10]]

# 2. Current prices of the 10 in one call (1 credit)
for p in rd("prices", {"skus": skus})["data"]["items"]:
    print(p["sku"], p["name"], p["price"], p["list_price"], p["quantity_discount"])

# 3. Nearest stores to a CEP (1 credit), then pickup for one product at 5 of them (1 credit)
stores = [s["store_id"] for s in rd("stores", {"cep": "01310-100"})["data"]["stores"][:5]]
pickup = rd("store-availability", {"skus": [skus[0]], "store_ids": stores})["data"]
print([(s["store_id"], s["pickup_available"]) for s in pickup["skus"][0]["stores"]])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `site`, `site_name`, `country`, `currency` and `language`, and most carry `notes`.

- **search / category / deals** - (`query`; `category_id`, `name` on category; `type`, `coupon`, `highlight`, `coupons[]` {`code`, `label`, `count`} on deals), `sort`, `page`, `page_size`, `total`, `total_pages`, `reachable_pages`, `has_more`, `count`, `items[]` {`position`, `sku`, `ean`, `name`, `brand`, `manufacturer`, `url`, `image`, `type`, `status`, `in_stock`, `price`, `list_price`, `discount_percent`, `price_type`, `quantity_discount`, `index_price`, `currency`, `labels`, `categories[]` {`id`, `name`, `parent_id`}, `quantity`, `active_ingredients`, `variant_count`, `variant_attributes`, `is_kit`, `sold_by`, `delivered_by`, `regulatory`}, `facets[]` {`name`, `values[]` {`value`, `count`}}, `filters_applied`.
- **categories** - `department_count`, `category_count`, `categories[]` {`id`, `name`, `url`, `level`, `children`}.
- **product** - `sku`, `name`, `url`, `ean`, `brand`, `manufacturer`, `breadcrumb[]`, `images`, `labels`, `in_stock`, `price`, `list_price`, `discount_percent`, `price_ladder`, `quantity`, `dosage`, `active_ingredient`, `weight_kg`, `refrigerated`, `regulatory` {`anvisa_registration`, `tarja`, `tarja_code`, `controlled_type_code`, `psychotropic_list_code`, `therapeutic_class`}, `seller`, `variant_count`, `variant_attributes`, `variants[]` {`sku`, `name`, `url`, `ean`, `attributes`, `price`, `discount_percent`, `in_stock`}, `kit` {`products`, `available_in_kits`}.
- **prices** - `requested`, `found`, `items[]` {`sku`, `found`, `name`, `in_stock`, `price`, `list_price`, `discount_percent`, `price_type`, `quantity_discount`, `variant_count`, `variant_attributes`}.
- **store-availability** - `sku_count`, `store_count`, `skus[]` {`code`, `code_type`, `sku`, `name`, `stores[]` {`store_id`, `pickup_available`}}.
- **stores** - `cep`, `count`, `stores[]` {`store_id`, `banner`, `name`, `address` {`street`, `number`, `district`, `city`, `state`, `cep`}, `latitude`, `longitude`, `distance_km`, `phone`, `open_24h`, `parking`, `farmacia_popular`, `hours` {`weekdays`, `saturday`, `sunday`}, `active`}.
- **stores/search** - `filters_applied`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `stores[]` (as stores, `hours` as the locator's text lines, no `distance_km`).
- **reviews** - `sku`, `rating`, `page_size`, `total`, `average_rating`, `recommended_by`, `rating_distribution`, `summary`, `top_tags`, `tags[]` {`tag`, `count`, `sentiment`}, `use_cases`, `count`, `has_more`, `next_cursor`, `reviews[]`.
- **suggestions** - `query`, `count`, `suggestions`, `quick_filters[]` {`name`, `query`}, `product_count`.

## Guardrails

- Name them "Drogasil and Droga Raia (drogasil.com.br, drogaraia.com.br, the pharmacy chains of RD Saude)" on first mention, and say which banner each number is from.
- Prices: quote `price`, `list_price` and the `fetched_at` date as the site's online reference price; never as a price at a given store. Card and loyalty prices are not available.
- Regulatory fields: pass them through as the site's labels exactly as returned. Do not interpret them and do not give health, dosage or purchasing guidance; for anything about medicines, point the user to a pharmacist.
- Store pickup: quote `pickup_available` per store with the date; it is the site's yes or no, never a unit count.
- Sellers: marketplace partners are named by business name. Say when an item is sold by a partner (`seller.is_partner`, `sold_by`).
- Reviews: no reviewer names are returned. Quote a review as "a Droga Raia customer review" (or Drogasil) and say when `incentivized` or `likely_incentivized` is true. `summary`, `tags` and `use_cases` are the site's own, quoted as given.
- Images and copy: do not republish the sites' product images or copy; link products by `sku` instead.
- Not available: store unit counts, per-store prices, card or loyalty prices, product descriptions or leaflet text, deal start or end dates, price history (poll and store), account data, cart or checkout. This API cannot order an item.
- Terms: Scavio does not store Drogasil or Droga Raia data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Read the sites' current terms of use for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, steps, coupons, stores, pickup answers, ratings or dates. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "sku or url is required (a product code, e.g. 331137, or a product page link)."; "Send sku or url, not both."; "category_id or url is required (categories[].id, or a category page link)."; "cep must be a Brazilian CEP: 8 digits, e.g. 01310-100 or 01310100."; "query looks like a CEP: send it to stores (cep), the nearest-store lookup."; "At most 5 product x store checks per call (e.g. 1 product at 5 stores, or 5 products at 1 store)."; "city and neighborhood need state (a UF code, e.g. SP)."; "coupon goes with type coupons."; "page_size must be one of 24, 36, 48."; "facets.<name> is not a facet name: use facets[].name of an answer (e.g. filters.Fabricante)."; "min_price must not be above max_price.".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Drogasil product <sku>.", "No Droga Raia reviews for <sku>.", "No Drogasil products in category <id> with these filters (category ids differ between Drogasil and Droga Raia; see categories).", "No Drogasil coupon <code> is running. Running: ...", "No Drogasil results for <query>.". A CEP with no store of that banner nearby answers an empty list.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api).
- `502` and `503` mean the data was temporarily unavailable ("Drogasil / Droga Raia is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.102.0
npm install scavio@0.103.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.rdsaude.search({ query: "protetor solar", seller: "own", sort: "price_asc" });
const { data: grid } = await scavio.rdsaude.category({ site: "drogaraia", category_id: "8222" });
const { data: tree } = await scavio.rdsaude.categories({ site: "drogaraia" });
const { data: product } = await scavio.rdsaude.product({ sku: "72654" });
const { data: prices } = await scavio.rdsaude.prices({ skus: ["72654", "1493245"] });
const { data: pickup } = await scavio.rdsaude.storeAvailability({ site: "drogaraia", skus: ["38155"], store_ids: ["200", "210"] });
const { data: near } = await scavio.rdsaude.stores({ cep: "01310-100" });
const { data: city } = await scavio.rdsaude.storesSearch({ site: "drogaraia", state: "RS", city: "Porto Alegre" });
const { data: reviews } = await scavio.rdsaude.reviews({ site: "drogaraia", sku: "38155" });
const { data: deals } = await scavio.rdsaude.deals({ type: "oferta_do_dia" });
const { data: typed } = await scavio.rdsaude.suggestions({ query: "shamp" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.rdsaude.search(...)`, `category`, `categories`, `product`, `prices`, `store_availability`, `stores`, `stores_search`, `reviews`, `deals` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `search_rdsaude`, `get_rdsaude_category`, `get_rdsaude_categories`, `get_rdsaude_product`, `get_rdsaude_prices`, `get_rdsaude_store_availability`, `get_rdsaude_stores`, `search_rdsaude_stores`, `get_rdsaude_reviews`, `get_rdsaude_deals` and `get_rdsaude_suggestions`. Drogasil + Droga Raia is opt-in: add `rdsaude` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.102.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,rdsaude"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/rdsaude-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api), [category](https://scavio.dev/docs/rdsaude-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api), [categories](https://scavio.dev/docs/rdsaude-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api), [product](https://scavio.dev/docs/rdsaude-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api), [prices](https://scavio.dev/docs/rdsaude-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api), [store availability](https://scavio.dev/docs/rdsaude-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api), [stores](https://scavio.dev/docs/rdsaude-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api), [store locator](https://scavio.dev/docs/rdsaude-stores-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api), [reviews](https://scavio.dev/docs/rdsaude-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api), [deals](https://scavio.dev/docs/rdsaude-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api) and [suggestions](https://scavio.dev/docs/rdsaude-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api). The platform page is [scavio.dev/rdsaude-api](https://scavio.dev/rdsaude-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=drogasil-droga-raia-api).
