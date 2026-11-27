---
name: riachuelo-api
description: Riachuelo API for Riachuelo (riachuelo.com.br, the Brazilian fashion retailer; Brazil only, BRL, Portuguese text) - what a dress, a pair of jeans or any Riachuelo piece costs today, how much it is discounted, which sizes are sold out and how many units the listing shows per size, and how shoppers rate it, as riachuelo.com.br shows it to a visitor who is not signed in (on 2026-11-27 the Pool Jeans wide leg twill trousers for women in off-white read R$ 79.99 against R$ 159.99, 50 percent off, rated 5 from 11 ratings; the keyword search "vestido" counted 1,204 products, a midi dress at R$ 179.99 against R$ 199.99 with 14, 17, 40, 31 and 1 units across its 5 sizes; the men's Black Friday page held 627 products) with price, list price, discount, sale flag, the coupon or campaign banner, seller, colours, sold-out flag and every colour / size / sku with its sold-out flag and units; keyword search across the whole site, category listings by path and campaign pages (the Black Friday page of a department by default, seasonal, or any campaign path), 24 per page, in the site's 6 sorts (relevance, newest, best selling, discount, price) and filtered by the listing's own filters (size, colour, gender, subcategory, brand, category group) with counts and the price range; one product by sku or link with composition, attributes, breadcrumbs, images, the rating summary with the count per star and the reviews the product page shows (no names). 4 endpoints, 1 credit each. Search totals include sold-out products; the product page carries no per-size stock; no shipping quote, stores, suggestions, Pix price or price history.
version: 1.0.0
tags: riachuelo, riachuelo-com-br, riachuelo-api, lojas-riachuelo, riachuelo-brasil, riachuelo-prices, riachuelo-precos, riachuelo-search, riachuelo-busca, riachuelo-product, riachuelo-category, riachuelo-categorias, riachuelo-deals, riachuelo-ofertas, riachuelo-promocoes, riachuelo-black-friday, riachuelo-campanha, riachuelo-sizes, riachuelo-tamanhos, riachuelo-stock, riachuelo-estoque, riachuelo-esgotado, riachuelo-units, riachuelo-filters, riachuelo-reviews, riachuelo-avaliacoes, riachuelo-ratings, pool-jeans, riachuelo-coupons, riachuelo-cupom, fashion-prices, clothing-prices, moda-feminina, moda-masculina, moda-infantil, vestido, calca-jeans, brazil, brazil-ecommerce, brazilian-retail, brl, price-monitoring, product-data, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 300
    throttle: 1
    homepage: https://scavio.dev/riachuelo-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=riachuelo-api
---

# Riachuelo API - Fashion Prices, Units per Size, Sold-Out Flags, Black Friday Deals, Reviews

Read Riachuelo (riachuelo.com.br, the Brazilian fashion retailer): keyword search across the whole site, category listings and campaign pages (the Black Friday page of a department by default), each item with every colour and size, its sold-out flag and the units the listing shows, and one product with composition, attributes, the rating summary and the reviews its page shows. www.riachuelo.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in.

**The job this skill is for: what a Riachuelo piece costs today, how much it is discounted, which sizes are still in stock, and how shoppers rate it.** Every listing card carries the price next to the price before the discount and one row per colour and size with the site's sold-out flag and units. On 2026-11-27 the search "vestido" counted 1,204 products; first came a brown midi dress (`16195833`) at R$ 179.99 against R$ 199.99 (10 percent off) with a "CUPOM BLACK 45%|MÍN R$99" coupon banner, its 5 sizes listing 31 (PP), 14 (P), 17 (M), 40 (G) and 1 (GG) units. The Pool Jeans wide leg twill trousers for women in off-white (`16519710`) read R$ 79.99 against R$ 159.99 (50 percent off), rated 5 from 11 ratings.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged, and so is a search with no results (an empty `200`); a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Stock per size lives on listings only.** The `variations` of a search, category or deals card carry each colour / size / sku with `sold_out` and `units`. `/product` carries no stock per size, only the product's own `sold_out` and `availability`.
- **Totals include sold-out products.** `total` counts every product in the listing, sold out or not. Check `sold_out` and `sizes_in_stock` before saying an item can be bought.
- **Campaign pages are seasonal.** `/deals` reads the Black Friday page of a department by default, or any campaign path (`items[].promo_tag.campaign`). Campaign pages carry no start or end dates, and an ended campaign is a charged `404`. Say so.
- **Search is slow.** Keyword searches usually take 5-90 seconds; category, deals and product pages 3-35 seconds. Allow a client timeout of at least 300 seconds for search.
- **No history, shipping or stores.** Everything is the page at the moment of the call; Scavio keeps nothing. There are no shipping quotes by CEP, store stock, store locations, search suggestions, Pix prices, installments or more review pages. Poll and store your own series.

Riachuelo publishes no developer API for its catalog, prices or stock. Prices, sizes and reviews are shown on riachuelo.com.br for each product, and this skill reads those public pages with one Scavio key.

See also: Lojas Renner `lojas-renner-api`, C&A Brasil `cea-brasil-api`, Dafiti `dafiti-api`, Netshoes `netshoes-api`, Centauro `centauro-api`, Mercado Libre `mercadolibre-product-data` (Brazil marketplace), Zara `zara-api`, H&M `hm-api`.

## When to trigger

Use this skill when the user asks to:
- Price a piece at Riachuelo: price, list price, discount and the coupon or campaign banner on it
- Search riachuelo.com.br by keyword (in Portuguese: "vestido", "calca jeans", "pijama"), sorted by relevance, newest, best selling, discount or price
- List a Riachuelo department or category (`feminino`, `masculino`, `infantil`, `feminino/colecao-feminino/vestido`)
- Filter a Riachuelo listing by size, colour, gender, subcategory, brand (Pool, Pool Jeans, Riachuelo) or category group, with the site's counts
- Read Riachuelo's Black Friday page for a department, or another campaign page
- Check which sizes and colours of an item are sold out, and how many units the listing shows per size
- Read one product: composition, attributes, breadcrumbs, images, the rating summary and the reviews its page shows

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=riachuelo-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=riachuelo-api) - email or Google, no card required.
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
| `POST /api/v1/riachuelo/search` | Keywords, across the whole site: 24 results per page with total (sold-out products included), price, list price, discount, coupon or campaign banner, seller, colours, sold-out flag and every colour / size / sku with its sold-out flag and units, plus the listing's filters with counts and the price range | 1 |
| `POST /api/v1/riachuelo/category` | A category by path (`feminino/colecao-feminino/vestido`) or link, same items, sorts and filters, plus title and breadcrumbs | 1 |
| `POST /api/v1/riachuelo/deals` | A campaign page: the Black Friday page of a department (`feminino` by default, `masculino`, `infantil`) or another campaign path, same items, sorts and filters | 1 |
| `POST /api/v1/riachuelo/product` | One product by sku or link: price, list price, discount, sold-out flag, availability, gender, department, subcategory, collection, composition, breadcrumbs, attributes, images, the rating summary with the count per star and the reviews the page shows | 1 |

Brazil only: there is no `country` parameter. Every answer carries `store` (riachuelo), `host`, `country` (br), `currency` (BRL) and `language` (pt-BR), and `notes`.

## Prices and stock

| Field | Meaning |
|---|---|
| `price` | The price now, in BRL (the sale price where there is one): R$ 79.99 on the trousers below |
| `list_price` | The price before the discount (R$ 159.99) |
| `discount_percent` | The site's own discount figure (50); null when there is no discount |
| `on_sale` | True when the site marks the item as on sale |
| `price_varies` (listings) | True when the item's colours or sizes carry different prices |
| `promo_tag` (listings) | `{label, campaign}`: the coupon or campaign banner the listing shows on the item ("CUPOM BLACK 45%\|MÍN R$99"), with the campaign path `/deals` takes |
| `variations[]` (listings) | `{color, size, sku, sold_out, units}`: one row per colour and size, with the site's sold-out flag and the units it lists |
| `sizes_in_stock` (listings) | How many of the item's sizes are not sold out |

- Quote "Vestido midi godê feminino Lequinha com bolso - Marrom: R$ 179.99 (list R$ 199.99), size GG with 1 unit listed, on riachuelo.com.br on 2026-11-27", with the size and the date.
- A coupon banner is the site's label, not a price: never apply a coupon or compute a price after it, and never judge a price as a good deal.

## Workflow

1. **Find products.** `/search` with `query` (`vestido`), `/category` with `category` (`feminino`, or a path from `breadcrumbs[].path` or `items[].categories`), or `/deals` with `department` (`masculino`) or `campaign` (`campanha/r/promo/oferta-especial`, from `items[].promo_tag.campaign`). Each item's `sku` is the input of `/product`.
2. **Sort, filter and page.** `sort` (relevance, newest, best_selling, discount, price_asc, price_desc), `filters` from the listing's own `filters[].id` and `filters[].options[].value` (`{"filter_size": ["P", "M"], "brand": "Pool Jeans"}`), and `page` 2, 3, ... `has_more` false means the last page.
3. **Sizes in stock.** Read the card's `variations`: `sold_out` and `units` per colour and size. The product page has no per-size stock.
4. **One product.** `/product` with `sku` (`16519710`) or `url`: composition, attributes, rating and the reviews the page shows.
5. **Watching prices and stock:** there is no history. Poll the same listings and skus on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`) and deals (`/deals`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords in Portuguese, 1-120 characters. The search covers every department |
| `category` (category, required) | A category path as the site writes it (`feminino`, `masculino`, `infantil`, `feminino/colecao-feminino/vestido`; `breadcrumbs[].path` and `items[].categories` carry them), or its riachuelo.com.br link |
| `department` (deals) | The Black Friday page of a department: `feminino` (the default), `masculino` or `infantil` |
| `campaign` (deals) | Another campaign page by its path (`campanha/...`, from `items[].promo_tag.campaign`) or link, instead of `department` |
| `sort` | `relevance` (default), `newest`, `best_selling`, `discount`, `price_asc`, `price_desc`: the site's 6 sorts |
| `filters` | Filter id -> value or list of values, ids from `filters[].id` (`filter_size`, `filter_color`, `gender`, `catalog_class`, `brand`, `gg`) and values from `filters[].options[].value`; up to 10 values. Several values of one filter match any of them; several filters must all match. A price range is not taken as a filter |
| `page` | 1-500 (24 results per page) |

`/deals` takes `department` or `campaign`, not both. A search with no products returns an empty `200`.

### Product (`/product`)

`/product` takes exactly one of `sku` (`items[].sku`: digits such as `16519710`, or `KIT<digits>` for a kit) or `url` (a riachuelo.com.br product link or path, `items[].url`).

## Examples

### One search item

Request `{"query": "vestido"}` (1 credit): `total` 1204, `total_pages` 51, 24 items, filters for size (51 options), colour, gender, subcategory, brand (25) and category group, `price_range` {"min": 0, "max": 400}. One item:

```json
{
  "position": 1,
  "sku": "16195833",
  "name": "Vestido midi godê feminino Lequinha com bolso - Marrom",
  "brand": "Riachuelo",
  "currency": "BRL",
  "price": 179.99,
  "list_price": 199.99,
  "discount_percent": 10,
  "on_sale": true,
  "price_varies": false,
  "promo_tag": { "label": "CUPOM BLACK 45%|MÍN R$99", "campaign": "campanha/r/promo/oferta-especial" },
  "seller": { "id": "RCHLO", "name": "Riachuelo" },
  "colors": [],
  "categories": ["feminino", "colecao-feminino", "vestido", "vestido-midi"],
  "sold_out": false,
  "sizes_in_stock": 5,
  "variations": [
    { "color": "marrom", "size": "p", "sku": "16195833002", "sold_out": false, "units": 14 },
    { "color": "marrom", "size": "m", "sku": "16195833003", "sold_out": false, "units": 17 },
    { "color": "marrom", "size": "gg", "sku": "16195833005", "sold_out": false, "units": 1 },
    { "color": "marrom", "size": "g", "sku": "16195833004", "sold_out": false, "units": 40 },
    { "color": "marrom", "size": "pp", "sku": "16195833001", "sold_out": false, "units": 31 }
  ]
}
```

The item also carried `url` and `image`.

### One product

Request `{"sku": "16519710"}` (1 credit), abridged:

```json
{
  "requested": { "sku": "16519710" },
  "sku": "16519710",
  "sku_group": "16519710",
  "name": "Calça Pool Jeans wide leg feminina em sarja - Off-White",
  "brand": "Pool Jeans",
  "color": "Off-White",
  "price": 79.99,
  "list_price": 159.99,
  "on_sale": true,
  "discount_percent": 50,
  "sold_out": false,
  "availability": "InStock",
  "gender": "Feminino",
  "department": "Feminino",
  "subcategory": "Calça",
  "collection": "Verão",
  "composition": "Algodão 100%",
  "breadcrumbs": [
    { "name": "Feminino", "path": "feminino" },
    { "name": "Coleção feminina", "path": "feminino/colecao-feminino" },
    { "name": "Calça Jeans Feminina", "path": "feminino/colecao-feminino/calca-jeans" }
  ],
  "rating": { "average": 5, "count": 11, "histogram": { "1": 0, "2": 0, "3": 0, "4": 0, "5": 11 } },
  "reviews_has_more": false
}
```

The product also carried 33 `attributes` ({id, label, value, shown_on_page}: Modelagem Wide Leg, Composição Principal Algodão 100%, Peso 350.0g, ...), 6 `images` and 1 review in `reviews` (rating 5, title "Perfeita", text, size 38, colour Off-white, date 2026-09-07, sku), with no reviewer name. There is no stock per size on the product.

### Category and deals

- `/category` `{"category": "feminino", "sort": "discount"}`: `title` Feminino, `total` 9006, `total_pages` 376, first a women's white blouse at R$ 9.99 against R$ 69.99 (86 percent off), 1 of its 5 sizes in stock (P, 1 unit), `price_range` {"min": 5.99, "max": 439.99}.
- `/deals` `{"department": "masculino"}`: `campaign` campanha/r/especial/black-friday/masculino, `title` Black Friday|Masculino, `total` 627, first a men's short-sleeve linen-blend shirt in off-white at R$ 85.99 against R$ 159.99 (46 percent off), all 5 sizes in stock.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def riachuelo(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/riachuelo/{endpoint}", headers=HEADERS, json=body, timeout=300)
    r.raise_for_status()
    return r.json()

# 1. Women's dresses in sizes P or M, deepest discount first (1 credit)
hits = riachuelo("category", {"category": "feminino/colecao-feminino/vestido", "sort": "discount", "filters": {"filter_size": ["P", "M"]}})["data"]
for it in hits["items"][:5]:
    left = {v["size"]: v["units"] for v in it["variations"] if not v["sold_out"]}
    print(it["name"], it["price"], it["list_price"], it["discount_percent"], left, it["sku"])

# 2. The first one in full, with its rating (1 credit)
item = riachuelo("product", {"sku": hits["items"][0]["sku"]})["data"]
print(item["composition"], item["rating"])

# Riachuelo prices and stock change during the day. Store each answer with
# fetched_at and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `host`, `country`, `currency`, `language` and `notes`.

- **search / category / deals** - `query` (search), `category`, `title` and `breadcrumbs[]` {`name`, `path`} (category), `campaign`, `department`, `title` and `breadcrumbs` (deals), `page`, `page_size` (24), `total` (sold-out products included), `total_pages`, `has_more`, `count`, `items[]` {`position`, `sku`, `name`, `brand`, `url`, `image`, `currency`, `price`, `list_price`, `discount_percent`, `on_sale`, `price_varies`, `promo_tag` {`label`, `campaign`}, `seller` {`id`, `name`}, `colors[]` {`name`, `hex`}, `categories`, `sold_out`, `sizes_in_stock`, `variations[]` {`color`, `size`, `sku`, `sold_out`, `units`}}, `filters[]` {`id`, `label`, `multi_select`, `options[]` {`label`, `value`, `count`}}, `price_range` {`min`, `max`}, `sort`, `filters_applied`.
- **product** - `requested`, `sku`, `sku_group`, `name`, `brand`, `color`, `url`, `currency`, `price`, `list_price`, `on_sale`, `discount_percent`, `sold_out`, `availability`, `gender`, `department`, `subcategory`, `collection`, `composition`, `breadcrumbs`, `attributes[]` {`id`, `label`, `value`, `shown_on_page`}, `images`, `rating` {`average`, `count`, `histogram`}, `reviews[]` {`rating`, `title`, `text`, `size`, `color`, `date`, `sku`}, `reviews_has_more`. No stock per size, shipping quote, store stock or marketing description.

## Guardrails

- Name it "Riachuelo (riachuelo.com.br, the Brazilian fashion retailer)" on first mention. Riachuelo accounts, carts and checkout are not read or made.
- Prices: quote `price` and `list_price` with the size and the `fetched_at` date, in BRL (R$). Never apply a coupon banner, compute a price after a coupon, or call a price a good deal.
- Stock: quote `units` and `sold_out` per size as the listing gives them, with the date; units are the site's online figure for that colour and size, not store stock. `total` includes sold-out products.
- Campaigns: say that `/deals` reads a seasonal campaign page (the Black Friday page by default) with no published start or end dates.
- Reviews: reviewer names are not returned. Quote a review as "a Riachuelo customer review" with its rating and date; never try to identify a reviewer. `rating` can count ratings without a written review.
- Use: Riachuelo's terms of use bar spiders and data-mining tools. Keep any use descriptive (prices, sizes and stock as facts with their date); do not republish Riachuelo's product photos, page copy, reviews or links to its pages, and refer to products by `sku`.
- Comparing Riachuelo with Renner, C&A Brasil or another store: compare the same product, size and date. Never call one store cheaper beyond the numbers shown.
- Not available: per-size stock on the product, shipping quotes by CEP, store stock and locations, search suggestions, Pix prices, installments, more review pages, price history (poll and store), account data, cart or checkout. This API cannot buy or reserve anything.
- Terms: Scavio does not store Riachuelo data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Riachuelo's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, units, sizes, ratings or reviews. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "url or sku is required"; "Pass url or sku, not both."; "sku must be a Riachuelo product sku (items[].sku: digits such as 16426657, or KIT789245)."; "category is a campaign page: use /api/v1/riachuelo/deals with campaign."; "Pass campaign or department, not both."; "A price range is not taken as a filter (the site ignores it): sort by price_asc or price_desc instead."; "At most 10 filter values per call."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Riachuelo has no product <sku>.", "Riachuelo has no category <path>.", "Riachuelo has no Black Friday page for department <department> ...", "Riachuelo has no campaign page <path> (campaign pages are seasonal).". A search with no products is an empty `200` (charged), not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=riachuelo-api).
- `502` and `503` mean Riachuelo data was temporarily unavailable ("Riachuelo is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- Keyword searches usually take 5-90 seconds (8 seconds in the capture), category, deals and product pages 3-35 seconds (10-20 seconds in the captures). Allow a client timeout of at least 300 seconds for search and 180 seconds for the rest.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.105.0
npm install scavio@0.106.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.riachuelo.search({ query: "vestido", sort: "price_asc" });
const { data: women } = await scavio.riachuelo.category({ category: "feminino", sort: "discount", filters: { filter_size: ["P", "M"] } });
const { data: blackFriday } = await scavio.riachuelo.deals({ department: "masculino" });
const { data: item } = await scavio.riachuelo.product({ sku: "16519710" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.riachuelo.search(...)`, `category`, `deals` and `product`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 4 endpoints as tools: `search_riachuelo`, `get_riachuelo_category`, `get_riachuelo_deals` and `get_riachuelo_product`. Riachuelo is opt-in: add `riachuelo` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.105.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,riachuelo"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/riachuelo-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=riachuelo-api), [category](https://scavio.dev/docs/riachuelo-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=riachuelo-api), [deals](https://scavio.dev/docs/riachuelo-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=riachuelo-api), [product](https://scavio.dev/docs/riachuelo-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=riachuelo-api). Platform page: [scavio.dev/riachuelo-api](https://scavio.dev/riachuelo-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=riachuelo-api).
