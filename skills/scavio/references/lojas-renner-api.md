# Lojas Renner API - Fashion Prices, Stock Levels, Cartao Renner Installments, Stores by CEP

Read Lojas Renner (lojasrenner.com.br, the Brazilian fashion retailer): keyword search, category listings and lists such as every discounted product, one product with its installment plans, rating aggregate, colours and per-size availability, the price and stock flags of one size, and the Renner stores for a CEP. www.lojasrenner.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in.

**The job this skill is for: what a Renner piece costs today, on the store card and on other cards, how many units the site lists, and which sizes are available.** On 2026-11-27 the Cortelle barrel trouser `931758127` (Calça Barrel em Flamê com Brilho) read R$ 199.90 against R$ 219.90 (9 percent off), 6x R$ 33.32 interest-free on the Cartão Renner (Renner's store card) or 4x R$ 49.98 on other cards, rated 4.4 over 21 reviews, in 6 sizes all available. The camiseta search listed a Get Over seamless T-shirt at R$ 69.90 against R$ 79.90 with a stock level of 17 and 163 sold in the last 15 days.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Listings are slow at the source.** Search, category and lists usually take 30-200 seconds (the captures took 11-24 seconds); allow a client timeout of at least 300 seconds and send one call at a time.
- **Two installment plans.** `installments.store_card` is the interest-free plan on the Cartão Renner, `installments.credit_card` the plan for other cards. Listings carry the one plan the listing shows (`installment`).
- **Stock level on listings, flags per size.** `stock_level` is the unit count the site lists for the product and `sold_last_15_days` its own figure; `/product` and `/sku-price` give per-size flags (`available`, `out_of_stock`, `omni_stock`, ...), not unit counts.
- **Rating aggregate only.** `rating` and `review_count` are the product page's aggregate; review texts are not returned.
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
7. **Watching prices:** there is no history. Poll the same searches and products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

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
- **product** - `product_id`, `requested_sku`, `sku`, `sku_matched`, `name`, `brand`, `url`, `color` {`id`, `name`, `hex`}, `size`, `price`, `list_price`, `on_sale`, `discount_percent`, `installments` {`store_card` {`count`, `amount`, `interest_free`}, `credit_card` {`count`, `amount`}}, `rating`, `review_count`, `available`, `purchasable`, `out_of_stock`, `omni_stock`, `back_order`, `pre_order`, `pre_launch`, `discontinued`, `max_quantity`, `marketplace`, `seller`, `gender`, `categories`, `breadcrumbs[]` {`name`, `url`}, `composition`, `details`, `images`, `colors[]` {`id`, `name`, `hex`, `sku`, `sizes[]` {`size`, `sku`}}, `size_count`, `sizes_available`, `sizes[]` {`size`, `sku`, `available`, `purchasable`, `out_of_stock`, `omni_stock`, `pre_order`, `discontinued`}, `notes`. No review texts, shipping quote or marketing description.
- **sku-price** - `product_id`, `sku`, `name`, `color` {`name`, `code`, `hex`}, `size`, `price`, `list_price`, `on_sale`, `discount_percent`, `installments` {`store_card`, `credit_card`}, `available`, `purchasable`, `out_of_stock`, `omni_stock`, `back_order`, `pre_order`, `pre_launch`, `discontinued`, `max_quantity`, `image`, `notes`.
- **stores** - `cep`, `cep_state`, `count`, `stores[]` {`store_number`, `name`, `address` {`street`, `number`, `complement`, `city`, `state`}, `phone`, `hours`}, `excluded_count`, `notes`. No coordinates or distances.

## Guardrails

- Name it "Lojas Renner (lojasrenner.com.br, the Brazilian fashion retailer)" on first mention. Renner accounts, carts and checkout are not read or made.
- Prices: quote `price` with `list_price` and the `fetched_at` date, in BRL (R$). Quote the Cartão Renner plan and the other-cards plan as two plans, exactly as given; never compute an installment.
- Stock: `stock_level` and `sold_last_15_days` are the figures the site lists for the product; per-size answers are flags (`available`, `out_of_stock`, `omni_stock`), not counts. Never present a flag as a unit count, or a listing's `stock_level` as one size's stock.
- Sellers: `marketplace` true means a partner store sells the product, named in `seller` (a store name). Say so when comparing prices.
- Ratings: `rating` and `review_count` are the aggregate the product page shows. Review texts are not returned; never invent one.
- Stores: the store locator's list for the CEP's city or region, in its order, not by distance. Rows outside the CEP's state are left out and counted in `excluded_count`. `phone` is the chain's shared number.
- Use: Lojas Renner's terms of use restrict reproducing its content beyond access. Keep any use descriptive (prices, availability and stores as facts with their date); do not republish Renner's product photos, page copy or links to its pages, and refer to products by `product_id`.
- Comparing Renner with C&A Brasil, Dafiti or another store: compare the same product, size and date. Never call one store cheaper beyond the numbers shown.
- Not available: review texts, shipping quotes by CEP, search suggestions, store coordinates or store stock, deal start and end dates, price history (poll and store), account data, cart or checkout. This API cannot buy or reserve anything.
- Terms: Scavio does not store Lojas Renner data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Lojas Renner's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, stock figures, ratings or stores. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id or url is required"; "Pass product_id or url, not both."; "product_id must be a Lojas Renner product id (digits, items[].product_id, e.g. 931758127)."; "sku must be a Lojas Renner sku id (digits, e.g. 931758135: sizes[].sku of the product endpoint)."; "cep must be a Brazilian CEP of 8 digits, e.g. 01310-100."; "At most 10 filter ids per call."; "query must contain letters or digits."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Lojas Renner has no product <id>.", "Lojas Renner has no sku <sku> for product <id>.", "Lojas Renner has no category <id>.", "Lojas Renner has no list <id>.". A search with no products is an empty `200`, not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api).
- `502` and `503` mean Lojas Renner data was temporarily unavailable ("Lojas Renner is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- Search, category and lists usually take 30-200 seconds at the source (in the captures 11-24 seconds); allow a client timeout of at least 300 seconds. Product, one size and stores usually take 5-30 seconds; allow at least 180 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.105.0
npm install scavio@0.106.0
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
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.renner.search(...)`, `category`, `deals`, `product`, `sku_price` and `stores`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 6 endpoints as tools: `search_renner`, `get_renner_category`, `get_renner_deals`, `get_renner_product`, `get_renner_sku_price` and `get_renner_stores`. Lojas Renner is opt-in: add `renner` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.105.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,renner"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/renner-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api), [category](https://scavio.dev/docs/renner-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api), [deals](https://scavio.dev/docs/renner-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api), [product](https://scavio.dev/docs/renner-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api), [sku price](https://scavio.dev/docs/renner-sku-price?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api), [stores](https://scavio.dev/docs/renner-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api). Platform page: [scavio.dev/renner-api](https://scavio.dev/renner-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=lojas-renner-api).
