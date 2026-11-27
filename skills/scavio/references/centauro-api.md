# Centauro API - Prices per Size, Pix Price, Sellers, Deals, Store Pickup by CEP

Read Centauro (centauro.com.br, the sporting-goods retailer of Grupo SBF): keyword search, category listings, deal lists (Black Friday, outlet, Mega Oferta), one product with every size's price, seller and stock flag, delivery options and store pickup for one size to a Brazilian CEP, the stores near a CEP, and search suggestions. www.centauro.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in. Every endpoint returns structured JSON and costs 1 credit.

**The job this skill is for: what each size of an item costs at Centauro today, who sells it, and which store near a CEP has it.** Centauro sells next to brand stores and partner shops, and one product can split its sizes between sellers at different prices; this skill returns each size as Centauro shows it, never computed. On 2026-11-27 the adidas Super U in BRANCO/PRETO (product `9976EA51`) had 12 sizes, 11 in stock, `split_sellers` true: sizes 37, 41, 42, 44 and 45 sold by Centauro at `price` R$ 389.99 against `list_price` R$ 599.99 (35 percent off, 4x de R$ 97.49, no Pix price), and sizes 34-36, 38-40 and 43 sold by adidas at R$ 599.99 with `pix_price` R$ 569.99 (Pix, Brazil's instant payment, 5 percent off) in 7x de R$ 85.71. Size 37 to CEP 01310-100 listed 18 stores with the size in stock.

Seven limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Prices per size and per seller, as given.** `price` is the price Centauro shows (the promotional price where there is one), `list_price` the regular price, `pix_price` the Pix price where the site shows one (null otherwise), `installment` the best installment plan. With `has_different_prices` true, sizes differ in price or seller: read `/product` for each size. Never compute one price from another.
- **Stock is a flag, not a unit count.** `in_stock` per size, `in_store_stock` per store. Centauro publishes no unit counts.
- **Store pickup is per size and CEP.** `/freight` takes one size `sku` and an 8-digit CEP (the Brazilian postal code). `/stores` lists the stores near a CEP without stock.
- **Listings stop at 10,000.** 36 products a page; the site caps every listing total at 10,000 (`total_capped` true, 278 pages). Narrow with filters or sorts to reach the rest.
- **Deals carry no dates.** Centauro publishes no start or end dates for its deal lists; none are returned.
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. There is no full review list, no Q&A and no in-store price. Poll and store your own series.

Centauro has no public API for its catalog, prices or stock. Prices, sellers and pickup options are shown on centauro.com.br for each item, and this skill reads those public pages with one Scavio key.

See also: Mercado Libre `mercadolibre-product-data` (Brazil marketplace), Decathlon `decathlon-product-data`, Dick's Sporting Goods `dicks-sporting-goods-api`, Foot Locker `foot-locker-api`, Nike `nike-api`; Brazilian retail: KaBuM! `kabum-api`, Magazine Luiza `magalu-magazine-luiza-api`.

## When to trigger

Use this skill when the user asks to:
- Price an item at Centauro: price, regular price, discount, Pix price, installment plan, per size
- Search centauro.com.br by keyword (in Portuguese: "tenis corrida", "chuteira society", "camisa time"), sorted by relevance, discount or price, filtered by brand, size, gender, product type, price band, sport, colour, discount band, Outlet or Mega Oferta, a store or a seller
- Browse one Centauro category by its /nav/ path (calcados, calcados/produto/tenis)
- Read Centauro's Black Friday list, the outlet, Mega Oferta or another deal page as a product list
- Read one Centauro product: every size with sku, EAN, stock flag, price, Pix price, installments and seller; colours, specs, rating and up to 3 reviews
- See who sells each size (Centauro or a brand seller such as adidas or Nike.com.br) and how much of a brand or category marketplace sellers carry
- Check store pickup and delivery of one size to a Brazilian CEP: options, cost, dates, and which stores have it now
- List the Centauro stores near a CEP, or the products one store carries
- Read Centauro's search suggestions and most searched terms

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=centauro-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=centauro-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Listings (search, category, deals) usually take 10-45 seconds and the other endpoints 2-20 seconds (in the captures: product 1.3, category 7.7, suggestions 11.9, search 12.4, stores 14.4, freight 14.7, deals 15.7). Allow a client timeout of at least 150 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/centauro/search` | Keywords: 36 products per page with total, price, list price, discount, Pix price, installment, seller, badges, rating, colours and size skus; every facet with its count | 1 |
| `POST /api/v1/centauro/category` | One category by its /nav/ path or link (or a facet value), same items, sorts, filters and facets as search | 1 |
| `POST /api/v1/centauro/deals` | A deal list: the Black Friday hotsite (default), outlet, Mega Oferta or another hotsite slug, same items, sorts and filters | 1 |
| `POST /api/v1/centauro/product` | One product in one colour: every size with sku, EAN, stock flag, price, list price, Pix price, installment and seller; colours, specs, images, rating, up to 3 reviews (no names) | 1 |
| `POST /api/v1/centauro/freight` | One size to a Brazilian CEP: delivery options with cost and dates, and the stores offering pickup with hours, address, distance, in-store stock flag or transfer days | 1 |
| `POST /api/v1/centauro/stores` | The Centauro stores near a CEP, nearest first, with distance, coordinates and the filter value that lists what a store carries | 1 |
| `POST /api/v1/centauro/suggestions` | The search-box suggestions for the start of a query and the site's most searched terms | 1 |

Brazil only: there is no `country` parameter. Every answer carries `store` (centauro), `host`, `country` (br), `currency` (BRL) and `language` (pt-BR).

## Prices: price, list price, Pix price, installments and sellers

Every listing item, every colour variant and every product size carries Centauro's price layers as centauro.com.br shows them to a visitor who is not signed in:

| Field | Meaning |
|---|---|
| `price` | The price in BRL Centauro shows: the promotional price where there is one (R$ 389.99 on the Super U sizes Centauro sold) |
| `list_price` | The regular price (R$ 599.99) |
| `discount_percent` | Centauro's discount against the regular price (35); null when none |
| `pix_price` | The price paid by Pix where the site shows one (R$ 569.99 on the adidas sizes); null otherwise |
| `pix_discount_percent` (product sizes) | The Pix discount the site shows (5) |
| `installment` | The best installment plan `{count, amount}` (4 x R$ 97.49) |
| `installments[]` (product) | Every plan the product page lists: 1x R$ 389.99, 2x R$ 194.99, 3x R$ 129.99, 4x R$ 97.49 |
| `seller` | `{name, is_centauro}` on listings; per size `{name, code, is_centauro, own_delivery}` |
| `has_different_prices`, `split_sellers` | Sizes differ in price or seller; a Centauro offer and a brand seller split the sizes |
| `badges` | The site's badges as written (Mega Oferta, Preço Online, CAMPEÃO, LANÇAMENTO) |

- Quote "adidas Super U, size 37: R$ 389.99 (regular R$ 599.99, 4x de R$ 97.49), sold by Centauro, at centauro.com.br on 2026-11-27", with the size, the seller and the date.
- A listing item shows one price for the product (`has_different_prices` warns when sizes differ). For a size's own price and seller, read `/product`.
- `discount_percent` is Centauro's own figure. Report Centauro's prices, labels and dates and the arithmetic only. Never judge a price as a good deal.

## Workflow

1. **Find the item.** `/search` with `query` (`tenis corrida`), `/category` with a `path` (`/nav/categorias/calcados`), or `/deals` with a `deal` (`black-friday`). Each item's `product_id` (model + colour) is the input of `/product`; `size_skus` are inputs of `/freight`.
2. **Narrow it.** Read `facets[]` of an answer and send any `facets[].values[].filter` back in `filters` (`["marca:asics", "preco:r300r400"]`), or use the `brand`, `store` and `seller` shortcuts. Up to 10 values per call.
3. **One product.** `/product` with `product_id` (or `model` + `color`, or `url`): every size's sku, EAN, stock flag, price, Pix price, installment and seller; `colors[]` gives the other colours' `product_id`.
4. **Pickup and delivery.** `/freight` with one size `sku` and a `cep`: delivery options and every store offering pickup, with `in_store_stock` or `transfer_days`.
5. **Nearby stores.** `/stores` with a `cep`; send a store's `filter` to search, category or deals as `store` for what it carries.
6. **Demand.** `/suggestions` with the start of a query: suggestions and the site's top searches.
7. **Watching prices:** there is no history and deals carry no dates. Poll the same products and lists on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`) and deals (`/deals`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords in Portuguese as shoppers type them, 1-120 characters |
| `path` (category, required) | A category as its /nav/ path or a centauro.com.br /nav/ link (key / value pairs, as the site's breadcrumb links write them), e.g. `/nav/categorias/calcados/produto/tenis`; or one facet value such as `categorias:calcados` |
| `deal` (deals) | `black-friday` (default), `outlet`, `mega-oferta`, or another hotsite slug or centauro.com.br /hotsite/ link of the site |
| `sort` | `relevance` (default), `discount`, `price_asc`, `price_desc` (the site's 4 sorts) |
| `filters` | Facet value(s) as `key:value` exactly as `facets[].values[].filter` lists them, a string or a list. Keys: marca, tamanho, genero, produto, preco, esportes, modalidade, categorias, cor, desconto, idade, linha, promocao, loja, vendidopor |
| `brand` | Brand facet value(s) without the key: `nike`, `asics` |
| `store` | Store facet value(s) (loja): the products a physical store carries, from `stores[].filter` |
| `seller` | Sold-by facet value(s) (vendidopor): `centauro` or a marketplace seller such as `nikecombr` or `futfanatics` |
| `page` | 1-278 (36 per page; the site caps the total at 10,000) |

`filters`, `brand`, `store` and `seller` together take at most 10 values. A keyword or filter combination with no products returns `total` 0 with `200`.

### Product (`/product`)

Send exactly one of:

| Parameter | Description |
|---|---|
| `product_id` | The Centauro product id: model + colour (`items[].product_id`, `colors[].product_id`), e.g. `9976EA51` |
| `model` + `color` | The 6-character model code (`9976EA`) with a colour code (`colors[].color_code`, `51`) |
| `url` | A centauro.com.br product link with its colour: `https://www.centauro.com.br/<name>-<model>.html?cor=<color>` |

### Freight (`/freight`), stores (`/stores`) and suggestions (`/suggestions`)

| Parameter | Description |
|---|---|
| `sku` (freight, required) | A size sku (`sizes[].sku` of `/product`, or `items[].size_skus`), e.g. `9976EA510375` |
| `cep` (freight, stores, required) | A Brazilian CEP: 8 digits, `01310-100` or `01310100` |
| `query` (suggestions, required) | The start of a search, 1-80 characters, e.g. `tenis` |

## Examples

### One search item

Request `{"query": "tenis corrida"}` (1 credit): `total` 10000 (`total_capped` true), `total_pages` 278, 36 items, 15 facets (brand Asics 2,285, Nike 336; Outlet 1,633, Mega Oferta 280; sold by Centauro 618, FutFanatics 1,689). The first item, abridged:

```json
{
  "position": 1,
  "product_id": "9976EA31",
  "model": "9976EA",
  "color_code": "31",
  "name": "Tênis Masculino adidas Super U",
  "brand": "adidas",
  "available": true,
  "price": 389.99,
  "list_price": 599.99,
  "discount_percent": 35,
  "pix_price": null,
  "installment": { "count": 4, "amount": 97.49 },
  "has_different_prices": true,
  "seller": { "name": "Centauro", "is_centauro": true },
  "badges": ["Mega Oferta", "Preço Online", "..."],
  "rating": 5,
  "review_count": 3,
  "color_count": 6,
  "size_count": 8,
  "size_skus": ["9976EA310340", "M19C20310350", "..."]
}
```

The second item, the Olympikus Veloz 4, read R$ 242.09 against R$ 379.99 with a Pix price of R$ 229.99. `variants[]` carry the other colours with their own prices.

### One product, sizes split between two sellers

Request `{"product_id": "9976EA51"}` (1 credit): `color` {`code` 51, `name` BRANCO/PRETO}, `price_min` 389.99, `price_max` 599.99, `sellers` ["adidas", "Centauro"], `split_sellers` true, `size_count` 12, `sizes_in_stock` 11, `badges` ["LANÇAMENTO"]. Two of the sizes:

```json
[
  {
    "size": "37",
    "size_code": "037",
    "sku": "9976EA510375",
    "ean": "4069999989457",
    "in_stock": true,
    "available": true,
    "marketplace": false,
    "price": 389.99,
    "list_price": 599.99,
    "discount_percent": 35,
    "pix_price": null,
    "pix_discount_percent": null,
    "installment": { "count": 4, "amount": 97.49 },
    "seller": { "name": "Centauro", "code": "0", "is_centauro": true, "own_delivery": true }
  },
  {
    "size": "38",
    "size_code": "038",
    "sku": "M19C20510385",
    "ean": "4069999989358",
    "in_stock": true,
    "available": true,
    "marketplace": true,
    "price": 599.99,
    "list_price": 599.99,
    "discount_percent": null,
    "pix_price": 569.99,
    "pix_discount_percent": 5,
    "installment": { "count": 7, "amount": 85.71 },
    "seller": { "name": "adidas", "code": "adidasnewanymarket", "is_centauro": false, "own_delivery": true }
  }
]
```

Size 45 read `in_stock` false. The product also carried 6 colours, 11 specs (Composição Têxtil Sintético, Pisada Neutra, ...), `rating` 5 over 3 reviews, and those 3 reviews with rating, date, text and highlights ("Ótima aderência em superfícies"), no reviewer names.

### Store pickup and delivery to a CEP

Request `{"sku": "9976EA510375", "cep": "01310-100"}` (1 credit): `destination` {SÃO PAULO, SP, BELA VISTA, AV. PAULISTA}, `store_count` 18, `stores_with_stock` 18. The delivery options and one store:

```json
{
  "delivery_options": [
    { "type": "pickUpInStore", "label": "Retira na Loja", "cost": 0, "free": true, "origin": "store", "deadline": "Para pagamento aprovado até 17h", "estimated_date": "2026-11-27T12:00:00-03:00", "estimated_text": "Receba sexta-feira 27/nov", "same_day": true },
    { "type": "normal", "label": "Normal", "cost": 0, "free": true, "origin": "store", "deadline": "9 a 10 dias úteis", "estimated_date": "2026-12-10T12:00:00-03:00", "estimated_text": "Receba entre 10/dez e 11/dez", "same_day": false }
  ],
  "stores": [
    {
      "store_code": "0311",
      "name": "Plaza Sul Shopping",
      "distance_km": 6.89,
      "pickup_available": true,
      "in_store_stock": true,
      "pickup_days": 0,
      "transfer_days": null,
      "pickup_text": "Em até 3 horas",
      "pickup_cost": 0,
      "estimated_date": "2026-11-27T12:00:00-03:00",
      "same_day": true
    }
  ]
}
```

Each store also carries `hours`, `address` {`full`, `street`, `number`, `neighborhood`, `city`, `state`, `cep`, `latitude`, `longitude`} and its `filter`. Internacional Shopping Guarulhos (13.56 km) and Campinas Shopping also read "Em até 3 horas"; most others read "1 dia útil". Bauru Shopping read `in_store_stock` true with `pickup_available` false: the site does not offer pickup there for this size.

### Deals, category, stores and suggestions

- `/deals` `{"deal": "black-friday"}`: `total` 9257 over 258 pages, first the Bermuda Oxer Basic New Bolso Selado Masculina at R$ 31.57 against R$ 69.99 (57 percent off, Pix R$ 29.99, sold by Centauro, Mega Oferta), then the Tênis Masculino Nike Revolution 8 at R$ 259.99 against R$ 399.99 from Nike.com.br. No start or end dates.
- `/category` `{"path": "/nav/categorias/calcados", "sort": "discount"}`: `category_filters` ["categorias:calcados"], `total` 10000 (capped), first a Diadora sneaker at R$ 220 against R$ 1,099.99 (82 percent off, Pix R$ 198) from the brand seller Diadora Brasil.
- `/stores` `{"cep": "20040-002"}`: `count` 27 in and around Rio de Janeiro, Botafogo Shopping first at 4.62 km, each {`store_code`, `name`, `city`, `state`, `label`, `distance_km`, `latitude`, `longitude`, `filter`} (`loja:riodejaneirorjbotafogoshoppingloja0128`).
- `/suggestions` `{"query": "tenis"}`: tenis nike, tenis feminino, tenis masculino, tenis adidas, tenis; `top_searches` Tenis Nike, Asics, Tenis Adidas, Chuteira Society, Bermuda, ... (10).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def centauro(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/centauro/{endpoint}", headers=HEADERS, json=body, timeout=150)
    r.raise_for_status()
    return r.json()

# 1. Asics running shoes, biggest discount first (1 credit)
hits = centauro("search", {"query": "tenis corrida", "sort": "discount", "brand": "asics"})["data"]
item = hits["items"][0]
print(item["name"], item["price"], item["list_price"], item["pix_price"], item["seller"]["name"])

# 2. Every size with its price, seller and stock flag (1 credit)
prod = centauro("product", {"product_id": item["product_id"]})["data"]
for s in prod["sizes"]:
    print(s["size"], s["sku"], s["in_stock"], s["price"], s["pix_price"], s["seller"]["name"])

# 3. Pickup near a CEP in Sao Paulo for the first size in stock (1 credit)
size = next(s for s in prod["sizes"] if s["in_stock"])
ship = centauro("freight", {"sku": size["sku"], "cep": "01310-100"})["data"]
for st in ship["stores"]:
    if st["in_store_stock"]:
        print(st["name"], st["distance_km"], st["pickup_text"])

# Centauro prices and deal lists change daily. Store each answer with fetched_at and
# run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `host`, `country`, `currency` and `language`, and most carry `notes`.

- **search / category / deals** - `query` (search), `path`, `url` and `category_filters` (category), `deal` and `url` (deals), `page`, `page_size` (36), `total`, `total_capped`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `product_id`, `model`, `color_code`, `name`, `brand`, `url`, `image`, `available`, `price`, `list_price`, `discount_percent`, `pix_price`, `installment` {`count`, `amount`}, `has_different_prices`, `seller` {`name`, `is_centauro`}, `categories`, `badges`, `rating`, `review_count`, `color_count`, `size_count`, `size_skus`, `variants[]` {`product_id`, `color`, `url`, `image`, `price`, `list_price`, `discount_percent`, `pix_price`, `installment`}}, `facets[]` {`name`, `key`, `values[]` {`label`, `filter`, `count`, `selected`}}, `breadcrumbs[]` {`name`, `url`}, `sort`, `filters_applied`.
- **product** - `product_id`, `requested_id`, `model`, `color` {`code`, `name`}, `name`, `brand`, `url`, `available`, `in_stock`, `low_stock`, `purchase_limit`, `group`, `sub_group`, `category`, `gender`, `age_group`, `collection`, `category_path`, `breadcrumbs`, `price_min`, `price_max`, `has_different_prices`, `sellers`, `split_sellers`, `installments[]` {`count`, `amount`}, `size_count`, `sizes_in_stock`, `sizes[]` {`size`, `size_code`, `sku`, `ean`, `in_stock`, `available`, `marketplace`, `price`, `list_price`, `discount_percent`, `pix_price`, `pix_discount_percent`, `installment`, `seller` {`name`, `code`, `is_centauro`, `own_delivery`}}, `colors[]` {`product_id`, `color_code`, `name`, `url`, `image`}, `images`, `badges`, `specs[]` {`group`, `name`, `values`}, `rating`, `review_count`, `reviews[]` {`rating`, `date`, `text`, `highlights`}.
- **freight** - `sku`, `product_name`, `cep`, `destination` {`city`, `state`, `neighborhood`, `street`}, `count`, `delivery_options[]` {`type` (pickUpInStore, normal, scheduled, clickUpMarketplace, ...), `label`, `cost`, `free`, `origin` (store, warehouse, marketplace), `deadline`, `estimated_date`, `estimated_text`, `same_day`}, `store_count`, `stores_with_stock`, `stores[]` {`store_code`, `name`, `distance_km`, `hours`, `address` {`full`, `street`, `number`, `neighborhood`, `city`, `state`, `cep`, `latitude`, `longitude`}, `pickup_available`, `in_store_stock`, `pickup_days`, `transfer_days`, `pickup_text`, `pickup_cost`, `estimated_date`, `same_day`, `filter`}.
- **stores** - `cep`, `count`, `stores[]` {`store_code`, `name`, `city`, `state`, `label`, `distance_km`, `latitude`, `longitude`, `filter`}.
- **suggestions** - `query`, `count`, `suggestions[]` {`position`, `term`}, `top_searches[]` {`position`, `term`}.

## Guardrails

- Name it "Centauro (centauro.com.br, the sporting-goods retailer of Grupo SBF)" on first mention. Centauro accounts, carts and checkout are not read.
- Prices: quote `price` with `list_price`, `pix_price` (where present), the installment plan, the size, the seller and the `fetched_at` date, in BRL (R$). Prices are what a visitor who is not signed in sees on centauro.com.br. Never present a listing price as every size's price when `has_different_prices` is true.
- Installments: quote `installment` or `installments` exactly as given. Never compute an installment or apply a percent yourself.
- Stock: `in_stock` and `in_store_stock` are flags. Never state or estimate a unit count. `in_store_stock` true means the store has the size now; otherwise `transfer_days` gives the business days to send it there.
- Deals: there are no start or end dates; never invent one. Say when the list was read.
- Sellers: `seller.name` is Centauro or the marketplace seller's business name as Centauro lists it. Refer to a seller by that name; do not profile the people behind a business.
- Comparing Centauro with Netshoes, Mercado Libre, Decathlon or a brand store: compare the same model (brand, name and EAN), size, payment method and date. Never call one retailer cheaper beyond the numbers shown.
- Reviews: no reviewer names are returned, and only the up to 3 reviews the product page carries. Quote a review as "a Centauro customer review".
- Images and copy: do not republish Centauro's product images or product copy; refer to items by `product_id` instead.
- Not available: unit counts, the in-store price, deal dates, the full review list, Q&A, listings past 10,000 products, price history (poll and store), account data, cart or checkout. This API cannot reserve or buy an item.
- Terms: Scavio does not store Centauro data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Centauro's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, sellers, skus, EANs, stock flags, dates or ratings. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id, model (with color) or url is required"; "Pass one of product_id, model (with color) or url."; "product_id must be a Centauro product id: model + colour, e.g. 9976EA51 (items[].product_id or colors[].product_id)."; "color goes with model, not product_id (product_id already holds the colour)."; "model must be a Centauro model code (6 letters and digits, e.g. 9976EA)."; "color is required with model: a colour code (colors[].color_code, e.g. 51)."; "url must be a centauro.com.br product link with its colour (https://www.centauro.com.br/<name>-<model>.html?cor=<color>)."; "sku must be a Centauro size sku (sizes[].sku, e.g. 9976EA510375)."; "cep must be a Brazilian CEP of 8 digits, e.g. 01310-100."; "path is required (e.g. /nav/categorias/calcados)."; "path must be a Centauro category path or link (/nav/categorias/calcados/produto/tenis, the site's breadcrumb links: key / value pairs)."; "path is a product link: use /api/v1/centauro/product." (and the same for a search or hotsite link); "deal must be black-friday, outlet, mega-oferta or a hotsite slug as Centauro writes it (lowercase letters, digits and -)."; "filters must be a Centauro facet value key:value (facets[].values[].filter, e.g. marca:nike or preco:r100r200); keys: ..."; "At most 10 filter values per call (filters, brand, store and seller together)."; "query must contain letters or digits."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Centauro has no product <model> in colour <color>.", "Centauro has no products under <path> with these filters.", "Centauro has no deal list <deal>.", "Centauro does not know CEP <cep>.", "Centauro has no delivery for sku <sku>: the sku is unknown or out of stock.", "Centauro lists no stores near CEP <cep>.". A keyword or filter combination with no products answers `total` 0, and a keyword with no suggestions answers an empty `suggestions` list, both with `200`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=centauro-api).
- `502` and `503` mean Centauro data was temporarily unavailable ("Centauro is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.102.0
npm install scavio@0.103.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.centauro.search({ query: "tenis corrida", sort: "discount", brand: "asics" });
const { data: grid } = await scavio.centauro.category({ path: "/nav/categorias/calcados/produto/tenis", filters: ["preco:r300r400"] });
const { data: deals } = await scavio.centauro.deals({ deal: "black-friday", sort: "discount" });
const { data: product } = await scavio.centauro.product({ product_id: "9976EA51" });
const { data: pickup } = await scavio.centauro.freight({ sku: "9976EA510375", cep: "01310-100" });
const { data: stores } = await scavio.centauro.stores({ cep: "20040-002" });
const { data: terms } = await scavio.centauro.suggestions({ query: "tenis" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.centauro.search(...)`, `category`, `deals`, `product`, `freight`, `stores` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 7 endpoints as tools: `search_centauro`, `get_centauro_category`, `get_centauro_deals`, `get_centauro_product`, `get_centauro_freight`, `get_centauro_stores` and `get_centauro_suggestions`. Centauro is opt-in: add `centauro` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.102.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,centauro"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/centauro-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=centauro-api), [category](https://scavio.dev/docs/centauro-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=centauro-api), [deals](https://scavio.dev/docs/centauro-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=centauro-api), [product](https://scavio.dev/docs/centauro-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=centauro-api), [freight](https://scavio.dev/docs/centauro-freight?utm_source=agent-skills&utm_medium=skill&utm_campaign=centauro-api), [stores](https://scavio.dev/docs/centauro-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=centauro-api), [suggestions](https://scavio.dev/docs/centauro-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=centauro-api). The platform page: [scavio.dev/centauro-api](https://scavio.dev/centauro-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=centauro-api).
