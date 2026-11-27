# Atacadao API - Store Prices, Bulk Quantity Tiers, Stores, Flyers

Read Atacadao (atacadao.com.br, the Brazilian cash-and-carry wholesale chain of Grupo Carrefour Brasil): keyword search, category listings and their facets priced at one store, one product with every quantity tier, the pickup stores near a CEP, the store directory, one store in full, its flyers, search suggestions and the category tree. www.atacadao.com.br only (Brazil, BRL, Portuguese text), the online prices of the store you choose.

**The job this skill is for: what an item costs at one Atacadao store today, per unit and by quantity.** Atacadao prices each store on its own and sells by the unit and by the case: the price drops once you buy enough units. On 2026-11-27 at the Tatuape store (`atacadaobr340`, Sao Paulo), Arroz Branco Namorado Tipo 1 5kg (EAN `7896079431158`) read R$ 21.89 for 1 unit and R$ 21.39 a unit from 6 (a case of 6); Arroz Carreteiro Seara 300g read R$ 19.50 and R$ 17.98 a unit from 3; Arroz Branco Camil Tipo 1 1kg R$ 4.85 and R$ 4.75 from 10.

Seven limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Prices are per store.** Send `store_id` (from `/stores-near` or `/stores`) to price at that store. Without it, prices are the site's default store, `atacadaobr60` (Vila Maria, Sao Paulo), and `notes` says so. Say which store a price is for.
- **The quantity tiers are the deal.** `price` is the unit price for 1 unit; `price_tiers` lists every tier the store gives (`min_quantity`, `unit_price`), and `bulk_unit_price` is the unit price at the largest tier. There is no was-price.
- **Items the store does not sell are left out.** Listings count and return the chosen store's items only. On `/product`, an item the store does not sell is a `200` with `available_at_store` false and no price.
- **No stock units.** Atacadao publishes no unit counts; `available_at_store` is a yes / no for the store's online catalog.
- **Consumer channel only.** Prices are the site's consumer pickup and delivery prices; the business (CNPJ) channel is not offered.
- **Flyers are links.** `/flyers` and `/store` return each flyer's name, validity dates, PDF link and cover image link; Scavio does not open the PDF or read prices from it.

Atacadao has no public API for its catalog or store prices. Prices, stores and flyers are shown on atacadao.com.br, and this skill reads those public pages with one Scavio key.

See also: Carrefour Brasil `carrefour-brasil-api` (the grocery and marketplace site of the same group), Mercado Libre `mercadolibre-product-data` (Brazil marketplace); wholesale clubs in the US: Costco `costco-product-data`, Sam's Club `sams-club-product-data`; Brazilian retail: KaBuM! `kabum-api`, Magazine Luiza `magalu-magazine-luiza-api`.

## When to trigger

Use this skill when the user asks to:
- Price an item at an Atacadao store: unit price, every quantity tier, bulk unit price, case size
- Search atacadao.com.br by keyword (in Portuguese: "arroz", "cafe", "detergente") at one store, sorted by relevance, price, best sellers, name, newest or discount, filtered by category, brand, price range or collection (Black November, Black Week)
- Browse one Atacadao category by its path (`mercearia/graos/arroz-branco`) or category id
- Read the facets of a search or category with the store's own counts
- Look up one Atacadao product by sku, EAN barcode, product id, slug or link
- Compare one item's price between Atacadao stores (one call per store)
- Find the Atacadao pickup stores near a CEP or a point, or list the stores of a state or city with address, phone, hours and holiday hours
- Read one store's services (bakery, butcher, fuel station), payment methods, meal-voucher cards and flyers
- Read the search box suggestions, the top searches, or the category tree

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Every endpoint usually answers in 2-20 seconds (in the captures: flyers 0.8, stores 2.7, store 3.4, category 3.8, search 4.1, categories 5.2, product 5.5, facets 5.7, suggestions 6.3, stores-near 7.0). Allow a client timeout of at least 90 seconds.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/atacadao/search` | Keywords at one store: up to 100 items a page with unit price, quantity tiers, bulk unit price, case size, EAN reference, categories and collections | 1 |
| `POST /api/v1/atacadao/category` | One category by path or category id at one store, same items, sorts and filters as search | 1 |
| `POST /api/v1/atacadao/product` | One product by sku, EAN, product id, slug or link at one store: name, brand, EAN, images, categories, specifications, case size, availability at the store, unit price, quantity tiers, collections | 1 |
| `POST /api/v1/atacadao/stores-near` | The pickup stores near a CEP or a point, nearest first, with distance, address, coordinates and weekday hours; for a CEP also the stores the site offers there | 1 |
| `POST /api/v1/atacadao/stores` | The store directory for a state (and city): address, phone, hours, holiday hours, online services, flyer count and the store id for prices | 1 |
| `POST /api/v1/atacadao/store` | One store in full: the directory fields plus services, recycling points, payment methods, credit cards, meal vouchers and flyers | 1 |
| `POST /api/v1/atacadao/flyers` | One store's current flyers (folhetos): name, validity dates, PDF link, cover image link | 1 |
| `POST /api/v1/atacadao/facets` | The filter values of a search or category at one store, with the store's counts and the request field each goes back into | 1 |
| `POST /api/v1/atacadao/suggestions` | The search box's completions for the start of a query, with search counts, and the site's top searches | 1 |
| `POST /api/v1/atacadao/categories` | The department tree with category ids and paths | 1 |

Brazil only: there is no `country` parameter. Every answer carries `store` (atacadao), `country` (br), `currency` (BRL) and `language` (pt-BR), and most carry `notes`.

## Prices: unit price, quantity tiers and the case

Every listing item and every product carries the chosen store's online price:

| Field | Meaning |
|---|---|
| `price` | The unit price for 1 unit, in BRL (R$ 21.89 on Arroz Branco Namorado 5kg at Tatuape) |
| `price_tiers[]` | Every quantity tier the store gives, ascending: buy at least `min_quantity` units and each unit costs `unit_price` (`[{1, 21.89}, {6, 21.39}]`) |
| `bulk_unit_price` | The unit price at the largest tier (R$ 21.39) |
| `units_per_box` | The case size (6) |
| `measurement_unit`, `unit_multiplier` | The selling unit as the site gives it (`un`, 1) |
| `online_exclusive_price` | The site flags the price as online only |
| `priced_store_id` | The store the price is for (`atacadaobr340`) |
| `collections[]` | The lists the item is in, `{id, name}` (382 Black November, 334 Black Week, 302 Mais Vendidos) |

- Quote "Arroz Branco Namorado Tipo 1 5kg: R$ 21.89 a unit, R$ 21.39 a unit from 6, at Atacadao Tatuape (atacadaobr340) on atacadao.com.br on 2026-11-27", with the tier, the store and the date.
- A tier can carry the same unit price as the one below it; the site lists it so. Report Atacadao's prices and the arithmetic only (a tier total is `min_quantity` x `unit_price`, said as your own sum), and never judge a price as a good deal.

## Workflow

1. **Pick a store.** `/stores-near` with a `cep` (or `latitude` + `longitude`) for the nearest pickup stores, or `/stores` with a `state` (and `city`). Each store's `store_id` (`atacadaobr340`) or store number (`340`) is the `store_id` of every priced call.
2. **Find the item.** `/search` with `query` and `store_id`, or `/category` with a `category` path (`mercearia/graos/arroz-branco`) or `category_id` from `/categories`. Each item's `sku` is the input of `/product`.
3. **Narrow.** `/facets` lists the filter values with the store's counts and the `param` each goes back into: `category` (a path of the category-1/2/3 values), `brand`, `collection`, `min_price` / `max_price`, or `filters` {key: value} for any other key.
4. **One product.** `/product` with `sku`, `ean`, `product_id`, `slug` or `url`, and `store_id`: every quantity tier, the case size, specifications and collections.
5. **Compare stores.** Repeat `/product` with each `store_id`; quote each store's price with its store.
6. **Store details.** `/store` for services, payment methods and meal vouchers; `/flyers` for the current flyers with validity dates and the PDF link.
7. **Watching prices:** there is no history. Poll the same products at the same stores on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`) and facets (`/facets`)

| Parameter | Description |
|---|---|
| `query` (search, required; facets) | Keywords in Portuguese, 1-100 characters |
| `category` (category, or `category_id`; search and facets, optional) | A category path of 1 to 3 levels (`mercearia`, `mercearia/graos`, `mercearia/graos/arroz-branco`, from `categories[].path`) or its atacadao.com.br link |
| `category_id` (category) | A category id (`categories[].category_id`, e.g. 24) instead of `category` |
| `store_id` | The store to price at: its store id (`atacadaobr340`) or store number (`340`). Default: the site's default store, `atacadaobr60` (Vila Maria, Sao Paulo) |
| `sort` | `relevance` (default), `price_asc`, `price_desc`, `best_sellers` (most ordered), `name_asc`, `name_desc`, `newest` (release date), `discount` |
| `brand` | Brand value(s) from facets (key `brand`), e.g. `camil`, up to 10 |
| `collection` | A collection id (`items[].collections[].id`), e.g. `382` Black November, `334` Black Week |
| `min_price`, `max_price` | Price range in BRL |
| `filters` | Any other facet by its key: `{"<facets[].key>": value or [values]}`, up to 5 keys. Category, brand, price and collection have their own fields |
| `page` | 1-50 (default 1) |
| `page_size` | 1-100 (default 20) |

`/facets` needs a `query`, `category`, `brand` or `collection`. The price sorts follow the site's own order, which does not always follow the chosen store's price: sort by `price` yourself when the order matters. A search with no items at the store returns an empty `200`.

### Product (`/product`)

Send exactly one of `sku` (`items[].sku`, e.g. `14443`), `ean` (the EAN-13 barcode, `7896079431158`), `product_id`, `slug` (`arroz-branco-namorado-tipo-1-5619-14443`) or `url` (a product link, `https://www.atacadao.com.br/<slug>/p`), plus `store_id` (optional, as above).

### Stores near (`/stores-near`), stores (`/stores`), store (`/store`) and flyers (`/flyers`)

| Parameter | Description |
|---|---|
| `cep` (stores-near) | A Brazilian CEP (postal code): 8 digits, `01310-100` or `01310100` |
| `latitude`, `longitude` (stores-near, instead of cep) | A point in Brazil, e.g. `-12.9777`, `-38.4813` |
| `state` (stores, required) | A Brazilian state code (UF): `SP`, `RJ`, `MG`, `BA`, ... |
| `city` (stores) | A city of that state (accents and case ignored), e.g. `Curitiba` |
| `page`, `page_size` (stores) | Page (default 1) and 1-50 stores per page (default 24) |
| `store_id` (store, flyers, required) | A store number (`340`), store id (`atacadaobr340`) or store slug (`tatuape`) |

### Suggestions (`/suggestions`) and categories (`/categories`)

`/suggestions` takes `query`, the start of a search (`arroz`); without it, the top searches alone. `/categories` takes an empty body `{}`.

## Examples

### One search item at a store

Request `{"query": "arroz", "store_id": "atacadaobr340"}` (1 credit): `total` 52 at that store, `total_pages` 3, 20 items. The second item:

```json
{
  "position": 2,
  "sku": "14443",
  "product_id": "14443",
  "name": "Arroz Branco Namorado Tipo 1 5kg",
  "brand": "Namorado",
  "measurement_unit": "un",
  "unit_multiplier": 1,
  "units_per_box": 6,
  "reference_code": "5619987",
  "price": 21.89,
  "price_tiers": [
    { "min_quantity": 1, "unit_price": 21.89 },
    { "min_quantity": 6, "unit_price": 21.39 }
  ],
  "bulk_unit_price": 21.39,
  "online_exclusive_price": false,
  "priced_store_id": "atacadaobr340",
  "categories": [
    { "name": "Mercearia", "path": "mercearia" },
    { "name": "Grãos", "path": "mercearia/graos" },
    { "name": "Arroz branco", "path": "mercearia/graos/arroz-branco" }
  ]
}
```

The first item, Arroz Branco Camil Tipo 1 5kg, read R$ 20.29 with a single tier. Arroz Carreteiro Seara 300g read R$ 19.50, and R$ 17.98 a unit from 3 (a case of 12).

### One product by EAN

Request `{"ean": "7896079431158", "store_id": "atacadaobr340"}` (1 credit): `sku` 14443, `name` "Arroz Branco Namorado Tipo 1 5kg", `complement_name` "Arroz Namorado Agulhinha Tipo 1 Pacote com 5kg", `brand` Namorado, `available_at_store` true, `price` 21.89, `price_tiers` [{1, 21.89}, {6, 21.39}], `bulk_unit_price` 21.39, `units_per_box` 6, and 8 collections including 382 Black November and 334 Black Week.

### Stores near a CEP and one store

Request `{"cep": "01310-100"}` to `/stores-near` (1 credit): `total` 33, 30 stores nearest first (Atacadão - PACAEMBU at 4.9 km, Atacadão - Ipiranga at 5.44 km, ...), and 17 `serving_stores` the site offers for the CEP (Ipiranga, Santo Amaro, Tatuapé, Vila Maria, ...). One store:

```json
{
  "store_id": "atacadaobr697",
  "store_number": 697,
  "name": "Atacadão - PACAEMBU",
  "distance_km": 4.9,
  "address": { "street": "Rua James Holland", "number": "668", "neighborhood": "Barra Funda", "city": "São Paulo", "state": "SP", "cep": "01138-000" },
  "hours": [{ "day": "monday", "opens": "08:00", "closes": "20:00" }, "..."]
}
```

`/store` `{"store_id": 340}`: "Tatuapé 24hrs", open 00:00 to 23:59 every day, `services` bakery, butcher, deli_counter, cafe, fuel_station, atacadao_card_desk, whatsapp_offers, ifood; `payment_methods` cash, debit_card, pix (Pix is Brazil's instant payment), atacadao_card, carrefour_card; 10 credit cards and 30 meal-voucher cards; `recycling_points` batteries and light_bulbs; 6 flyers.

### Stores, flyers, facets, suggestions and categories

- `/stores` `{"state": "SP", "city": "São Paulo"}`: `total` 21, each with `store_id`, `sells_online`, address, phone, hours, `holiday_hours` (Taipas: 27/11/2026 Black Friday, "A partir das 6h"), `online_services` (Entrega) and `flyer_count`.
- `/flyers` `{"store_id": 340}`: 6 flyers, "Black Friday Atacadão" and 5 named "Black Friday", each valid 2026-11-27, with `pdf_url` and `thumbnail_url`.
- `/facets` `{"query": "arroz", "store_id": "atacadaobr340"}`: `total` 52 and 5 facets: Departamento (Mercearia 37, Frios e congelados 9, ...), Categoria, Subcategoria, Preço (R$ 3.99 to R$ 54.90) and Marca (25 brands).
- `/suggestions` `{"query": "arroz"}`: arroz branco 5kg (2,246 searches, pointing to Mercearia > Grãos > Arroz branco), arroz 5kg (7,736), arroz 5 kg, arroz 2kg, arroz branco; `top_searches` cafe (52,506), cerveja (42,966), sabonete, sabão, macarrão, ...
- `/categories` `{}`: 20 departments and 644 nodes, Mercearia (`category_id` 2) first.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def atacadao(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/atacadao/{endpoint}", headers=HEADERS, json=body, timeout=90)
    r.raise_for_status()
    return r.json()

# 1. The pickup stores near a CEP in Sao Paulo (1 credit)
near = atacadao("stores-near", {"cep": "01310-100"})["data"]
store = near["stores"][0]["store_id"]

# 2. Rice at that store, with every quantity tier (1 credit)
hits = atacadao("search", {"query": "arroz", "store_id": store, "page_size": 50})["data"]
for it in hits["items"]:
    tiers = ", ".join(f"{t['min_quantity']}+ R$ {t['unit_price']}" for t in it["price_tiers"])
    print(it["name"], it["price"], tiers, it["units_per_box"])

# 3. One product by EAN at two stores (1 credit each)
for sid in [store, "atacadaobr340"]:
    p = atacadao("product", {"ean": "7896079431158", "store_id": sid})["data"]
    print(sid, p["available_at_store"], p["price"], p["bulk_unit_price"])

# Atacadao prices change by store and by day. Store each answer with fetched_at and
# run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `country`, `currency` and `language`.

- **search / category** - `store_id`, `priced_store_id`, `query` (search), `category`, `category_id` and `url` (category), `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `sort`, `filters_applied`, `items[]` {`position`, `sku`, `product_id`, `name`, `brand`, `url`, `image`, `measurement_unit`, `unit_multiplier`, `units_per_box`, `reference_code`, `price`, `price_tiers[]` {`min_quantity`, `unit_price`}, `bulk_unit_price`, `online_exclusive_price`, `priced_store_id`, `categories[]` {`name`, `path`}, `collections[]` {`id`, `name`}}, `notes`.
- **product** - `requested`, `store_id`, `priced_store_id`, `sku`, `product_id`, `name`, `complement_name`, `brand`, `ean`, `reference_code`, `url`, `images`, `categories`, `measurement_unit`, `unit_multiplier`, `units_per_box`, `specifications`, `available_at_store`, `price`, `price_tiers`, `bulk_unit_price`, `online_exclusive_price`, `collections`, `notes`.
- **stores-near** - `cep`, `latitude`, `longitude`, `total`, `count`, `stores[]` {`store_id`, `store_number`, `pickup_point_id`, `name`, `distance_km`, `address` {`street`, `number`, `neighborhood`, `city`, `state`, `cep`}, `latitude`, `longitude`, `hours[]` {`day`, `opens`, `closes`}}, `serving_stores[]` {`store_id`, `store_number`, `name`} (for a CEP), `notes`.
- **stores** - `state`, `city`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `stores[]` {`store_number`, `store_id` (null when the store does not sell online), `sells_online`, `name`, `slug`, `url`, `format`, `address`, `phone`, `latitude`, `longitude`, `hours`, `holiday_hours[]` {`date`, `description`, `hours`}, `online_services`, `flyer_count`}, `notes`.
- **store** - the directory fields plus `services`, `recycling_points`, `payment_methods`, `credit_cards`, `meal_vouchers`, `flyers[]`, `notes`.
- **flyers** - `store_number`, `store_id`, `name`, `slug`, `url`, `count`, `flyers[]` {`flyer_id`, `name`, `valid_from`, `valid_to`, `pdf_url`, `thumbnail_url`, `priority`}, `notes`.
- **facets** - `store_id`, `priced_store_id`, `query`, `filters_applied`, `total`, `count`, `facets[]` {`key`, `label`, `param`, `values[]` {`value`, `label`, `count`, `selected`} or `min` / `max`}, `notes`.
- **suggestions** - `query`, `count`, `suggestions[]` {`term`, `count`, `attributes[]`}, `top_searches[]` {`term`, `count`}, `notes`.
- **categories** - `count`, `node_count`, `categories[]` {`category_id`, `name`, `path`, `url`, `children[]`}, `notes`.

## Guardrails

- Name it "Atacadao (atacadao.com.br, the Brazilian cash-and-carry wholesale chain of Grupo Carrefour Brasil)" on first mention. Atacadao accounts, carts and checkout are not read.
- Prices: quote `price` and the tier you mean, with the store (`priced_store_id` and its name) and the `fetched_at` date, in BRL (R$). When no `store_id` was sent, say the price is for the site's default store, Vila Maria, Sao Paulo. These are the site's online prices for the store; never present them as the shelf price at the till.
- Tiers: quote `price_tiers` exactly as given. Never invent a tier, extend one to another store, or call a tier a discount from a regular price: there is no was-price.
- Stock: there are no unit counts. `available_at_store` says whether the store sells the item online; never state or estimate a quantity on hand.
- Sorts: the price sorts follow the site's own order, not always the store's price. Re-sort by `price` before calling an item the lowest priced in a list.
- Flyers: return the flyer's name, dates and links as given. Scavio does not open the PDF; never quote a flyer price you have not seen.
- Comparing Atacadao with Carrefour Brasil or another supermarket: compare the same product (EAN), pack size, quantity tier, store and date. Never call one chain cheaper beyond the numbers shown.
- Business buyers: the business (CNPJ) price channel is not offered. Say so when asked for company prices.
- Images and copy: do not republish Atacadao's product images or product copy; refer to items by `sku` or EAN instead.
- Not available: stock units, a was-price, reviews, Q&A, price history (poll and store), the business (CNPJ) channel, flyer contents, account data, cart or checkout. This API cannot reserve or buy an item.
- Terms: Scavio does not store Atacadao data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Atacadao's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, tiers, stores, hours, EANs or flyer dates. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "sku, ean, product_id, slug or url is required"; "Pass one of sku, ean, product_id, slug or url (got ...)."; "category or category_id is required"; "Pass category or category_id, not both."; "query, category, brand or collection is required" (facets); "cep or latitude and longitude are required"; "Pass cep or latitude / longitude, not both."; "cep must be a Brazilian CEP: 8 digits (e.g. 01310-100)."; "state must be a Brazilian state code (UF): AC, AL, ..."; "store_id must be a store number (340) or a store id (atacadaobr340): stores[].store_number or stores[].store_id."; "collection must be a collection id (digits, e.g. 382 for Black November; items[].collections[].id)."; "min_price must be below max_price."; "filters takes at most 5 keys.".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Atacadao has no product for this id.", "Atacadao has no category <id> (categories[].category_id).", "Atacadao has no store <id>.", "Atacadao has no store in <city> (<state>). Cities with stores in <state>: ..." (the answer lists the state's cities), "No store was found near this place.". An unknown category path and a search with no items at the store are an empty `200`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api).
- `502` and `503` mean Atacadao data was temporarily unavailable ("Atacadao is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.103.0
npm install scavio@0.104.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.atacadao.search({ query: "arroz", store_id: "atacadaobr340", sort: "best_sellers" });
const { data: grains } = await scavio.atacadao.category({ category: "mercearia/graos", store_id: 340 });
const { data: product } = await scavio.atacadao.product({ ean: "7896079431158", store_id: "atacadaobr340" });
const { data: near } = await scavio.atacadao.storesNear({ cep: "01310-100" });
const { data: stores } = await scavio.atacadao.stores({ state: "SP", city: "São Paulo" });
const { data: store } = await scavio.atacadao.store({ store_id: 340 });
const { data: flyers } = await scavio.atacadao.flyers({ store_id: "tatuape" });
const { data: facets } = await scavio.atacadao.facets({ query: "arroz", store_id: "atacadaobr340" });
const { data: typed } = await scavio.atacadao.suggestions({ query: "arroz" });
const { data: tree } = await scavio.atacadao.categories({});
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.atacadao.search(...)`, `category`, `product`, `stores_near`, `stores`, `store`, `flyers`, `facets`, `suggestions` and `categories`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 10 endpoints as tools: `search_atacadao`, `get_atacadao_category`, `get_atacadao_product`, `get_atacadao_stores_near`, `get_atacadao_stores`, `get_atacadao_store`, `get_atacadao_flyers`, `get_atacadao_facets`, `get_atacadao_suggestions` and `get_atacadao_categories`. Atacadao is opt-in: add `atacadao` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.103.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,atacadao"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/atacadao-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api), [category](https://scavio.dev/docs/atacadao-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api), [product](https://scavio.dev/docs/atacadao-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api), [stores near](https://scavio.dev/docs/atacadao-stores-near?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api), [stores](https://scavio.dev/docs/atacadao-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api), [store](https://scavio.dev/docs/atacadao-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api), [flyers](https://scavio.dev/docs/atacadao-flyers?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api), [facets](https://scavio.dev/docs/atacadao-facets?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api), [suggestions](https://scavio.dev/docs/atacadao-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api), [categories](https://scavio.dev/docs/atacadao-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api). Platform page: [scavio.dev/atacadao-api](https://scavio.dev/atacadao-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=atacadao-api).
