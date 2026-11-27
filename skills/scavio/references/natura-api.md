# Natura API - Prices, Black Friday Deals, Shades, Stores, 6 Markets

Read Natura (the Brazilian beauty brand of Natura &Co) on its own storefronts in Brazil, Argentina, Chile, Colombia, Mexico and Peru: keyword search, category listings, the category menu, one product with its shades, kit contents and latest reviews, search suggestions, the Black Friday campaign listing with its dates, and the physical Natura stores in Brazil. `country` picks the storefront (br by default); every answer comes in that market's language and currency, as shown to a visitor who is not signed in. Every endpoint returns structured JSON and costs 1 credit.

**The job this skill is for: what a Natura product costs today in a given market, what it is discounted from, which shades are in stock, and where the Natura stores in Brazil are.** Natura shows a sale price next to a struck-through price and this skill returns both as the storefront shows them, with the price display string in the market's own format. On 2026-11-27 the Deo Parfum Ilía Secreto 25 ml (product `NATBRA-194225`) read `price` R$ 66,48 against `list_price` R$ 110,80 (`discount_percent` 40, `discount_amount` 44.32), tagged "natura friday", with the "últimas unidades" low-stock badge, `max_quantity` 8 and 2 installments of R$ 33,24. The Black Friday listing natura-friday held 4,248 products sorted by discount.

Seven limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Public prices only.** Prices are what a visitor who is not signed in sees on the storefront. There are no consultant prices and no regional prices by CEP or postal code.
- **Six markets, never converted.** br (BRL), ar (ARS), cl (CLP), co (COP), mx (MXN) and pe (PEN), each in its own language. Each market has its own product ids (`NATBRA-`, `NATARG-`, `NATCHL-`, `NATCOL-`, `NATMEX-`, `NATPER-`) and its own sorts. Natura's US store is not covered: its catalog lists no products.
- **Listing cards are short.** A search, category or deals card carries price, list price, discount, shade price range and rating, but no review count, stock flag or promotion text: read `/product` for those.
- **Stock is a flag, not a count.** `in_stock`, `low_stock` and `low_stock_badge` ("últimas unidades") are what the page shows; there are no unit counts and no store stock.
- **Reviews: the 3 latest only.** `/product` returns the rating, the review count and the 3 latest reviews the page carries (stars, text, date, no names). Full review paging is not available.
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

Natura has no public product API. Prices, shades and stock flags are shown on Natura's storefronts for each product, and this skill reads those public pages with one Scavio key.

See also: O Boticario + Eudora `boticario-eudora-api` (Brazilian beauty brands), Sephora `sephora-product-data`, Ulta Beauty `ulta-beauty-api`, Mercado Libre `mercadolibre-product-data` (the same items on a Latin American marketplace).

## When to trigger

Use this skill when the user asks to:
- Price a Natura product: sale price, list price, discount, installments, in Brazil or in Argentina, Chile, Colombia, Mexico or Peru
- Search a Natura storefront by keyword (in the market's language: "perfume", "batom", "hidratante", "kaiak"), sorted by the market's own sorts, filtered by brand (Ekos, Kaiak, Essencial, Tododia, Una), product type, gender, fragrance family, skin or hair type, occasion or a price range
- Browse one Natura category (maquiagem, perfumaria, refis, corpo-e-banho) or read the category menu with its ids and counts
- Read one Natura product: stock flag and low-stock badge, max quantity, tags (natura friday, oferta relâmpago), every shade with its own price and stock, kit contents, ingredients, rating and the latest reviews
- List Natura's Black Friday campaign (natura friday in Brazil, Argentina, Chile and Colombia; promociones in Mexico and Peru) biggest discount first, with the campaign dates as the page writes them
- Read Natura's search suggestions for the start of a search
- Find Natura stores in Brazil by state, city, CEP prefix or store type, with address, phone and the store's mailbox

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=natura-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=natura-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Calls usually take 2-30 seconds (in the captures: suggestions 0.7, categories 2.2, search 2.9, deals 5.0, category 7.7, stores 8.6, product 8.7), up to a minute for pages of 100. Allow a client timeout of at least 120 seconds.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/natura/search` | Keywords: up to 100 products per page with total, sale price, list price, discount, shade price range, rating; the site's refinements and the market's sorts | 1 |
| `POST /api/v1/natura/category` | One category by id or link, same cards, sorts and filters as search, with the category name | 1 |
| `POST /api/v1/natura/categories` | The storefront's category menu: departments and subcategories with ids, menu counts and links | 1 |
| `POST /api/v1/natura/product` | One product: sale and list price, discount, installments, stock flag and low-stock badge, tags, every shade with its own price and stock, kit contents, ingredients, rating and the 3 latest reviews | 1 |
| `POST /api/v1/natura/suggestions` | The search box's suggestions: did-you-mean, up to 3 products, brands, popular searches and categories | 1 |
| `POST /api/v1/natura/stores` | The physical Natura stores in Brazil by state, city, CEP prefix and store type, with address, phone and the store's @natura.net mailbox | 1 |
| `POST /api/v1/natura/deals` | The market's Black Friday campaign listing, sorted by discount where the market offers that sort, with the campaign dates as the page writes them | 1 |

Every answer carries `store` (natura), `country`, `host`, `currency` and `language`.

| `country` | Storefront, language, currency | Product id prefix | Sorts |
|---|---|---|---|
| `br` (default) | www.natura.com.br, pt-BR, BRL | NATBRA | best_sellers, relevance, name_asc, name_desc, price_asc, price_desc, discount |
| `ar` | www.naturacosmeticos.com.ar, es-AR, ARS | NATARG | best_sellers, relevance, price_asc, price_desc, name_asc, name_desc, brand, most_popular, discount |
| `cl` | www.natura.cl, es-CL, CLP | NATCHL | best_sellers, discount, price_asc, price_desc |
| `co` | www.natura.com.co, es-CO, COP | NATCOL | best_sellers, name_asc, name_desc, price_asc, price_desc, discount |
| `mx` | www.natura.com.mx, es-MX, MXN | NATMEX | best_sellers, price_asc, price_desc, relevance, name_asc, name_desc, brand, most_popular |
| `pe` | www.natura.com.pe, es-PE, PEN | NATPER | best_sellers, discount, name_asc, name_desc, price_asc, price_desc |

search, category, categories, product, suggestions and deals answer in all six markets; stores is Brazil only. The Black Friday listing is natura-friday in br, ar, cl and co and promociones in mx and pe.

## Prices: sale price, list price, shades and installments

Every listing card and product carries Natura's price layers as the storefront shows them to a visitor who is not signed in:

| Field | Meaning |
|---|---|
| `price`, `price_display` | The sale price, and the same in the market's own format ("R$ 66,48"). On a multi-shade card, the lowest shade price |
| `price_max`, `price_max_display` | The highest shade price on a multi-shade card (`price_range` true); null otherwise |
| `list_price`, `list_price_display` | The struck-through price (R$ 110,80); null when none is shown |
| `discount_percent` | Computed from the two prices (40); null without a list price |
| `discount_amount` (product) | The difference between them (44.32) |
| `price_min`, `price_max` (product) | The shade price range of a shade master |
| `installments` (product) | `{max_count, min_amount, min_amount_display}` as the page states them (2 of R$ 33,24) |
| `tags`, `stamps`, `promotional_tag` (product) | The page's tags and stamps (natura friday, oferta relâmpago) as given |
| `shades[]` (product) | Each shade's own `product_id`, `shade`, `shade_code`, `price`, `list_price`, `discount_percent`, `in_stock`, `orderable`, `max_quantity`, `low_stock`, `low_stock_badge` |

- Quote "Deo Parfum Ilía Secreto 25 ml: R$ 66,48 at natura.com.br on 2026-11-27, against R$ 110,80 (40% off), natura friday, últimas unidades", with the date.
- A multi-shade product is listed as a shade master (`NATBRA-PAI3379`) with a price range: the Batom Color Hidra FPS 8 Faces 3,5g ran from R$ 14,36 to R$ 21,90 across its shades. Read `/product` for each shade's own price and stock flag.
- `price_display` is formatted in the market's style; quote it as given. Prices are in the market's currency and never converted: compare markets by their own currency, not a converted figure.
- Report Natura's prices, labels and dates and the arithmetic only. Never judge a price as a good deal.

## Workflow

1. **Find the product.** `/search` with `query` (`perfume`), or `/category` with a `category_id` from `/categories` (`maquiagem`, `perfumaria-refil`). Pass `country` for a market other than Brazil. Each card's `product_id` is the input of `/product`.
2. **Narrow it.** Read `facets[]` and send `filters` with `facets[].attribute` and `facets[].values[].value` exactly as listed (`{"brand": "Kaiak", "natg_gender": "masculino"}`), plus `min_price` / `max_price` in whole units of the market's currency. Pick a `sort` from `sort_options[]`.
3. **One product.** `/product` with `product_id` (or `url`): installments, stock flag, low-stock badge, tags, every shade, kit contents, ingredients, rating and the 3 latest reviews.
4. **Black Friday.** `/deals` for the market's campaign listing, biggest discount first, and `campaign_dates` as the page writes them.
5. **Stores.** `/stores` with `state`, `city`, `cep` or `type` for the Natura stores in Brazil.
6. **Watching prices:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`) and deals (`/deals`)

| Parameter | Description |
|---|---|
| `country` | `br` (default), `ar`, `cl`, `co`, `mx` or `pe` |
| `query` (search, required) | Keywords in the market's language, 1-100 characters |
| `category_id` (category, required) | A category id (`categories[].category_id`, e.g. `maquiagem`, `perfumaria`, `refis`) or the market's /c/<id> link |
| `category_id` (deals, optional) | Another campaign category instead of the market's Black Friday category |
| `sort` | One of the market's sorts (table above). Default: the site's order on search and category; discount on deals where the market offers it |
| `filters` | Up to 5 refinements: `{attribute: value or [values]}` exactly as `facets[].attribute` and `facets[].values[].value` list them (`brand`, `tbs_Tipo_de_Produto`, `natg_gender`, `natm_familiaOlfativa`, `tbs_Tipo_de_Pele`). Up to 10 values per attribute, as a list |
| `min_price`, `max_price` | Price range in whole units of the market's currency (the site's price filter) |
| `page` | 1-200; `total_pages` reports the last one |
| `page_size` | 1-100, default 24. Pages of 100 can take up to a minute |

A keyword with no products returns an empty `200` with a note. In Argentina the top-level departments (maquillaje, perfumeria, cabello) have no listing page: list one of their subcategories (`maquillaje-labios`).

### Categories (`/categories`) and suggestions (`/suggestions`)

`country` for both; `query` (suggestions, required): the start of a search, 1-100 characters (`kaiak`).

### Product (`/product`)

| Parameter | Description |
|---|---|
| `product_id` | A product id (`items[].product_id`, `shades[].product_id`), e.g. `NATBRA-194225` or a shade master `NATBRA-PAI3379`; the bare number (`194225`) takes the market's prefix |
| `url` | Or a product link on one of the six storefronts (`/p/<name>/<id>`); it sets the market. Send `product_id` or `url`, not both |
| `country` | The market of `product_id` (default br) |

### Stores (`/stores`, Brazil)

| Parameter | Description |
|---|---|
| `state` | Brazilian state code (UF): `sp`, `rj`, `mg`, ... (all 27) |
| `city` | City, accents and case ignored (`Sao Paulo`) |
| `cep` | A CEP (the Brazilian postal code) or its leading digits: `01310` or `01310-100` |
| `type` | `own` (aurora), `franchise` (franquia), `athena` or `kiosk` (quiosque), as the site labels them |
| `page`, `page_size` | Page 1-1000; 1-200 per page, default 50 |

## Examples

### One product with its badges

Request `{"product_id": "NATBRA-194225"}` (1 credit):

```json
{
  "store": "natura",
  "country": "br",
  "host": "www.natura.com.br",
  "currency": "BRL",
  "language": "pt-BR",
  "requested_id": "NATBRA-194225",
  "product_id": "NATBRA-194225",
  "name": "Deo Parfum Ilía Secreto 25 ml",
  "brand": "Ilía",
  "category": { "category_id": "perfumaria-para-quem", "name": "para quem" },
  "in_stock": true,
  "max_quantity": 8,
  "low_stock": true,
  "low_stock_badge": "últimas unidades",
  "price": 66.48,
  "price_display": "R$ 66,48",
  "list_price": 110.8,
  "list_price_display": "R$ 110,80",
  "discount_percent": 40,
  "discount_amount": 44.32,
  "price_min": null,
  "price_max": null,
  "installments": { "max_count": 2, "min_amount": 33.24, "min_amount_display": "R$ 33,24" },
  "tags": ["natura friday"],
  "stamps": [{ "label": "natura friday", "date": null }],
  "promotional_tag": null,
  "is_kit": false,
  "kit_contents": [],
  "shade_count": 0,
  "shades": [],
  "ingredients": null,
  "rating": 4.7,
  "review_count": 109,
  "latest_reviews": [
    { "rating": 5, "text": null, "date": "2026-07-21T16:09:50.471Z" },
    { "rating": 3, "text": null, "date": "2026-06-21T13:26:52.455Z" },
    { "rating": 5, "text": "Maravilhoso!", "date": "2026-06-18T12:20:37.926Z" }
  ]
}
```

`url`, `images` and the null `price_min_display` / `price_max_display` are omitted here. A review left as stars only has `text` null.

### A keyword search

Request `{"query": "perfume"}` (1 credit): `total` 522, `total_pages` 22, 9 refinements (`brand`, `tbs_Tipo_de_Produto`, `natg_gender`, `natm_familiaOlfativa`, `natm_fragancia`, `tbs_Tipo_de_Cabelo`, `tbs_Tipo_de_Pele`, `natm_ocasion`, `price`) and the 7 Brazilian sorts, Mais Vendidos selected. The first card:

```json
{
  "position": 1,
  "product_id": "NATBRA-21864",
  "name": "Deo Parfum Ilía Flor de Laranjeira 50 ml",
  "price": 99.95,
  "price_display": "R$ 99,95",
  "price_max": null,
  "price_max_display": null,
  "price_range": false,
  "list_price": 199.9,
  "list_price_display": "R$ 199,90",
  "discount_percent": 50,
  "rating": 4.5,
  "currency": "BRL"
}
```

The next cards: Desodorante Colônia Hoje Masculino 100 ml at R$ 67,56 against R$ 168,90 (60% off), Desodorante Colônia Luna 75 ml at R$ 92,95 against R$ 185,90 (50% off).

### The Black Friday listing with its dates

Request `{}` to `/deals` (1 credit): `category_id` natura-friday, `sort` discount, `total` 4248 over 177 pages of 24, and `campaign_dates`, the page's own sentences:

```json
{
  "category_id": "natura-friday",
  "category_name": "natura friday",
  "campaign_dates": [
    "A Natura Friday é a Black Friday da Natura: uma campanha com até 70% OFF em produtos selecionados de perfumaria, corpo e banho, cabelos, skincare e maquiagem, de 16 a 27 de novembro de 2026.",
    "A Natura Friday 2026 acontece de 16 a 27 de novembro, com ofertas antecipadas antes desse período e descontos estendidos até 30/11.",
    "A Black Friday do varejo é em 27 de novembro, a última sexta-feira do mês."
  ],
  "sort": "discount",
  "total": 4248,
  "total_pages": 177
}
```

First by discount: the Refil Desodorante Hidratante Corporal Perfumado Essencial Oud 200 g at R$ 29,90 against R$ 99,90 (70% off), then a Luna Ilumina refill at the same prices and the Batom Matte Longa Duração Faces at R$ 14,97 against R$ 49,90. `campaign_dates` is `[]` when the page states no dates and null when it could not be read this time.

### Stores in Sao Paulo

Request `{"state": "sp", "city": "Sao Paulo"}` (1 credit): `total_listed` 1093 stores in Brazil, `total` 102 matching, 3 pages of 50. The first store:

```json
{
  "store_code": "3",
  "name": "shopping villa lobos",
  "type": "own",
  "site_type": "aurora",
  "address": "av. das nações unidas, 4777 loja 125 - piso térreo",
  "neighborhood": "alto de pinheiros",
  "city": "sao paulo",
  "state": "SP",
  "cep": "05477-000",
  "phone": "11 95055-3787",
  "email": "lojavillalobos@natura.net",
  "delivery": false
}
```

The first page held 7 own stores, 11 franchises and 32 athena stores; 26 of the 50 carried an @natura.net mailbox, the rest `email` null.

### Category, categories and suggestions

- `/category` `{"category_id": "maquiagem"}`: `total` 964 over 41 pages, best sellers first; the Batom Color Hidra FPS 8 Faces 3,5g (`NATBRA-PAI3379`, `price_range` true, R$ 14,36 to R$ 21,90) and the Corretivo Cobertura Extrema 24h Una 8 ml (R$ 40,26 to R$ 50,32). The price refinement lists bands such as "De R$50,00 à R$99,99" (`min_price` 50, `max_price` 100).
- `/categories` `{}`: `count` 14 top categories and `node_count` 206 (perfumaria, corpo-e-banho, cabelos, maquiagem, rosto, refis, natura-friday, presentes, ...). maquiagem's menu showed 1,179 against 964 in its listing: `menu_count` is the menu's own count.
- `/suggestions` `{"query": "kaiak"}`: `count` 4, 3 products (a Kaiak O2 body deodorant refill, a two-refill Kaiak kit, a Kaiak Clássico gift set) and the brand Kaiak.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def natura(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/natura/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()

# 1. Kaiak perfumes in Brazil, lowest price first (1 credit)
hits = natura("search", {"query": "perfume", "sort": "price_asc", "filters": {"brand": "Kaiak"}})["data"]
item = hits["items"][0]
print(item["name"], item["price_display"], item["list_price_display"], item["discount_percent"])

# 2. The product with its badges, shades and installments (1 credit)
prod = natura("product", {"product_id": item["product_id"]})["data"]
print(prod["in_stock"], prod["low_stock_badge"], prod["installments"], prod["tags"])
for s in prod["shades"]:
    print(s["shade"], s["price"], s["in_stock"])

# 3. The same search in Mexico, in MXN (1 credit)
mx = natura("search", {"country": "mx", "query": "perfume", "sort": "price_asc"})["data"]
print(mx["currency"], mx["total"])

# Natura prices and promotions change daily. Store each answer with fetched_at and
# run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `country`, `host`, `currency` and `language`, and most carry `notes`.

- **search / category / deals** - `query` (search), `category_id`, `category_name` and `url` (category, deals), `campaign_dates` (deals), `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `sort`, `filters_applied`, `items[]` {`position`, `product_id`, `name`, `url`, `image`, `price`, `price_display`, `price_max`, `price_max_display`, `price_range`, `list_price`, `list_price_display`, `discount_percent`, `rating`, `currency`}, `facets[]` {`attribute`, `label`, `values[]` {`value`, `label`} or {`min_price`, `max_price`, `label`}}, `sort_options[]` {`sort`, `label`, `selected`}.
- **categories** - `count`, `node_count`, `categories[]` {`category_id`, `name`, `menu_count`, `url`, `subcategories[]`}.
- **product** - `requested_id`, `product_id`, `name`, `brand`, `url`, `category` {`category_id`, `name`}, `in_stock`, `max_quantity`, `low_stock`, `low_stock_badge`, `price`, `price_display`, `list_price`, `list_price_display`, `discount_percent`, `discount_amount`, `price_min`, `price_min_display`, `price_max`, `price_max_display`, `installments` {`max_count`, `min_amount`, `min_amount_display`}, `tags`, `stamps[]` {`label`, `date`}, `promotional_tag`, `is_kit`, `kit_contents[]` {`product_id`, `quantity`}, `shade_count`, `shades[]` {`product_id`, `shade`, `shade_code`, `swatch_image`, `image`, `price`, `list_price`, `discount_percent`, `in_stock`, `orderable`, `max_quantity`, `low_stock`, `low_stock_badge`}, `ingredients`, `images`, `rating`, `review_count`, `latest_reviews[]` {`rating`, `text`, `date`}.
- **suggestions** - `query`, `count`, `did_you_mean`, `products[]` {`product_id`, `name`, `image`, `url`} (up to 3), `brands`, `popular_searches`, `categories`.
- **stores** - `total_listed`, `total`, `page`, `page_size`, `total_pages`, `has_more`, `count`, `filters_applied`, `stores[]` {`store_code`, `name`, `type` (own, franchise, athena, kiosk), `site_type`, `address`, `neighborhood`, `city`, `state`, `cep`, `phone`, `email`, `delivery`}.

## Guardrails

- Name it "Natura (the Brazilian beauty brand of Natura &Co)" on first mention, and name the market (Brazil, Argentina, Chile, Colombia, Mexico, Peru). Natura accounts, consultant pages and carts are not read.
- Prices: quote `price_display` and `list_price_display` in the market's currency with the market and the `fetched_at` date. Prices are what a visitor who is not signed in sees. Never present them as consultant prices or as the price in a given CEP region.
- Installments: quote `installments` as given. Never compute an installment plan or apply a percent yourself.
- Stock: `in_stock`, `low_stock` and `low_stock_badge` are flags as the page shows them; never present them as unit counts or as store stock.
- Shades and refills: each shade has its own `product_id`, price and stock flag. A refill is its own product; the page carries no link to the product it refills, so never assert which product a refill belongs to beyond its name.
- Comparing markets: compare the same product name and size, each in its own currency, with the date. Never convert currencies or call one market cheaper beyond the numbers shown.
- Reviews: no reviewer names are returned. Quote a review as "a Natura customer review"; only the 3 latest are available.
- Stores: the address, phone and @natura.net mailbox are the store's business contact as Natura lists them. There are no coordinates, opening hours or store stock.
- Use: describe the data and the job (price and promotion tracking, shade availability, the store directory). Name Natura's sites as plain text.
- Images and copy: do not republish Natura's product images or product copy; link items by `product_id` instead.
- Not available: consultant prices, regional prices by CEP, store stock, full review paging or a star histogram, marketing descriptions, the US store (naturabrasil.com), price history (poll and store), account data, cart or checkout. This API cannot reserve or buy a product.
- Terms: Scavio does not store Natura data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Natura's terms of use restrict reselling the information on its sites; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, discounts, shades, ids, dates or ratings. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "country must be one of br, ar, cl, co, mx, pe."; "country us is not available: Natura's US store (naturabrasil.com) lists no products. Use br, ar, cl, co, mx or pe."; "sort must be one of <sorts> for country <country>."; "filters takes at most 5 attributes."; "filters.<attribute> takes at most 10 values."; "filters.<attribute>: pass several values as a list, not with \"|\"."; "filters: <attribute> is not a refinement; use the category, query, min_price / max_price or sort field."; "min_price must be below max_price."; "query must contain letters or digits."; "category_id must be a category id (categories[].category_id) or a /c/<id> link."; "product_id or url is required"; "Pass product_id or url, not both."; "product_id <id> is a country <country> id; pass country <country>."; "product_id must start with <prefix>- for country <country>."; "url is a <host> link; country <country> does not match (use <country>)."; "stores covers country br (the store list is published on natura.com.br)."; "state must be a Brazilian state code (UF): ..."; "cep must be a CEP or its leading digits (1-8 digits, e.g. 01310 or 01310-100)."; "type must be one of own, franchise, athena, kiosk."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Natura (<country>) has no product <id>.", "Natura (<country>) has no category <id>.", and in Argentina "Natura (ar) has no listing for category <id>. In Argentina the top-level departments (e.g. maquillaje, perfumeria) have no listing page: use one of their subcategories (categories[].subcategories[].category_id, e.g. maquillaje-labios).". A keyword with no products and a query with nothing to suggest answer an empty `200`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=natura-api).
- `502` and `503` mean Natura data was temporarily unavailable ("Natura is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.102.0
npm install scavio@0.103.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio({ timeout: 120000 }); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.natura.search({ query: "perfume", sort: "price_asc", filters: { brand: "Kaiak" } });
const { data: grid } = await scavio.natura.category({ category_id: "maquiagem", min_price: 50, max_price: 100 });
const { data: menu } = await scavio.natura.categories({ country: "mx" });
const { data: product } = await scavio.natura.product({ product_id: "NATBRA-194225" });
const { data: hints } = await scavio.natura.suggestions({ query: "kaiak" });
const { data: stores } = await scavio.natura.stores({ state: "sp", city: "Sao Paulo" });
const { data: deals } = await scavio.natura.deals({ country: "co" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient(timeout=120)`) the same methods are `client.natura.search(...)`, `category`, `categories`, `product`, `suggestions`, `stores` and `deals`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 7 endpoints as tools: `search_natura`, `get_natura_category`, `get_natura_categories`, `get_natura_product`, `get_natura_suggestions`, `get_natura_stores` and `get_natura_deals`. Natura is opt-in: add `natura` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.102.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,natura"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/natura-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=natura-api), [category](https://scavio.dev/docs/natura-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=natura-api), [categories](https://scavio.dev/docs/natura-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=natura-api), [product](https://scavio.dev/docs/natura-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=natura-api), [suggestions](https://scavio.dev/docs/natura-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=natura-api), [stores](https://scavio.dev/docs/natura-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=natura-api), [deals](https://scavio.dev/docs/natura-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=natura-api). The platform page: [scavio.dev/natura-api](https://scavio.dev/natura-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=natura-api).
