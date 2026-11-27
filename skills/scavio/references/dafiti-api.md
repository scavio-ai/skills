# Dafiti API - Fashion Prices, Units per Size, Marketplace Stores, Outlet Deals

Read Dafiti (dafiti.com.br, the Brazilian fashion marketplace): keyword search, category, brand and outlet listings, one product with its seller store, every size's units left and delivery type, specs and other colours, and every size of one sku with its stock. www.dafiti.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in.

**The job this skill is for: what an item costs at Dafiti today, how many units each size has left, and who sells and ships it.** Dafiti sells its own stock next to partner stores, and every size carries its own units and delivery type. On 2026-11-27 the Asics Gel 1130 unisex sneaker in beige (`15221282`, sku `AS296SCU17ARY`) read R$ 389.99, R$ 389.99 by Pix (Brazil's instant payment) and R$ 410.52 on card in up to 8 installments, against R$ 699.99 (44 percent off). 4 of its 11 sizes were in stock: 41 and 42 with 5 units each, 43 with 2 and 44 with 1, all from Dafiti's own stock, sold and delivered by Dafiti.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Units are exact from 0 to 10.** `units` is the count the site gives up to 10; above that the site says "more than 10" (`more_than_10` true, `units` null), not a count. Say so.
- **Prices as given.** `price` is the selling price (the Pix price where `pix_price` is set), `card_price` the price on a card, `list_price` the price before the discount. `/sizes` quotes the plan from the size data, which can differ from the product page's card price.
- **Sellers by store name.** On listings `marketplace` true only says a partner store sells the item; `/product` and `/sizes` name the store (`store_name`) and the delivery type.
- **Search matches loosely, and listings are slow.** A search with no close match can still list related products. Listing pages usually take 15-160 seconds; allow a client timeout of at least 240 seconds.
- **No history, reviews or shipping.** Everything is the page at the moment of the call; Scavio keeps nothing. There are no review texts, shipping quotes or search suggestions, and only dafiti.com.br (Brazil). Poll and store your own series.

Dafiti publishes no developer API for its catalog, prices or stock. Prices, sizes and sellers are shown on dafiti.com.br for each item, and this skill reads those public pages with one Scavio key.

See also: C&A Brasil `cea-brasil-api`, Lojas Renner `lojas-renner-api`, Netshoes `netshoes-api`, Centauro `centauro-api`, Enjoei `enjoei-api` (second-hand fashion), Mercado Libre `mercadolibre-product-data` (Brazil marketplace), Zara `zara-api`, ASOS `asos-api`.

## When to trigger

Use this skill when the user asks to:
- Price an item at Dafiti: price, list price, discount, Pix price, card price and installments
- Search dafiti.com.br by keyword (in Portuguese: "tenis", "vestido", "bota feminina"), sorted by popularity, newest, price or discount
- List a Dafiti department or category (`calcados-femininos`, `calcados-femininos/tenis`) or a brand (`asics`, `nike`, `farm-rio`)
- Read the Dafiti outlet, the site's own selection of discounted products
- Read one product: seller store, availability, every size with its units left and delivery type, specs, details, other colours and campaigns
- Check every size of one sku for stock, quickly
- See whether Dafiti or a partner store sells and ships an item (own stock, fulfillment by Dafiti, or drop shipping by the store)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=dafiti-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=dafiti-api) - email or Google, no card required.
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
| `POST /api/v1/dafiti/search` | Keywords: 48 results per page plus the site's sponsored slots, with total, price, list price, discount, Pix price, card price, installments, categories, sponsored and marketplace flags | 1 |
| `POST /api/v1/dafiti/category` | A department or category by path (`calcados-femininos/tenis`) or link, same items and sorts, plus breadcrumbs | 1 |
| `POST /api/v1/dafiti/brand` | A brand by its link name (`asics`), same items and sorts, plus breadcrumbs | 1 |
| `POST /api/v1/dafiti/deals` | The outlet, the site's own selection of discounted products, same items and sorts | 1 |
| `POST /api/v1/dafiti/product` | One product by product id, sku or link: availability, prices, installment, rating, seller store, every size with units, delivery type and store, other colours, categories, campaigns, specs, details and images | 1 |
| `POST /api/v1/dafiti/sizes` | Every size of one sku with its stock, units, delivery type and store, plus price, list price and installment; faster than product | 1 |

Brazil only: there is no `country` parameter. Every answer carries `store` (dafiti), `country` (br), `currency` (BRL) and `language` (pt-BR), and most carry `notes`.

## Prices: price, Pix price, card price and installments

| Field | Meaning |
|---|---|
| `price` | The selling price, in BRL (the Pix price where `pix_price` is set): R$ 389.99 on the Gel 1130 below |
| `pix_price` | The Pix price where the site shows one (null otherwise) |
| `card_price` | The price on a card (R$ 410.52), payable in up to `max_installments` installments (8) |
| `list_price` | The price before the discount (R$ 699.99) |
| `discount_percent` | The discount, as the site gives it (44) |
| `installment` (product, sizes) | `{count, amount}`: the plan the page or the size data quotes (`/sizes`: 7x R$ 55.71) |

- Quote "Tenis Unissex Asics Gel 1130 Bege: R$ 389.99 by Pix, R$ 410.52 on card (list R$ 699.99), sold by Dafiti, on dafiti.com.br on 2026-11-27", with the seller and the date.
- Quote every price and plan exactly as given; `/sizes` and `/product` can quote different plans. Never compute a Pix discount or an installment, and never judge a price as a good deal.

## Workflow

1. **Find products.** `/search` with `query` (`tenis`), `/category` with `category` (`calcados-femininos/tenis`, or a path from `breadcrumbs[].url`), `/brand` with `brand` (`asics`), or `/deals` for the outlet. Each item's `sku` is the input of `/sizes` and `/product`; `product_id` works for `/product`.
2. **Sort and page.** `sort` (popularity, newest, price_asc, price_desc, discount) and `page` 2, 3, ... `has_more` false means the last page. `sponsored` items are the site's sponsored slots on top of the 48 results.
3. **One product.** `/product` with `product_id` (`15221282`), `sku` (`AS296SCU17ARY`) or `url`: the seller store and every size.
4. **Stock check.** `/sizes` with `sku` (or one size's sku, `AS296SCU17ARY-52`, which also returns `requested_size`): every size's units and delivery type, faster than `/product`.
5. **Watching prices and stock:** there is no history. Poll the same listings and skus on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`), brand (`/brand`) and deals (`/deals`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords in Portuguese, 1-100 characters |
| `category` (category, required) | A department or category path of 1 to 3 levels as the site writes it (`calcados-femininos`, `calcados-femininos/tenis`; `breadcrumbs[].url`), or its dafiti.com.br link |
| `brand` (brand, required) | A brand as the site writes it in its link (`asics`, `nike`, `farm-rio`), or its dafiti.com.br link |
| `sort` | `popularity` (default), `newest`, `price_asc`, `price_desc`, `discount`: the site's 5 sorts |
| `page` | 1-2000 (48 results per page plus the sponsored slots) |

`/deals` takes `sort` and `page` only (the outlet). A search with no products returns an empty `200`.

### Product (`/product`) and sizes (`/sizes`)

`/product` takes exactly one of `product_id` (the number at the end of a Dafiti product link, `items[].product_id`, e.g. `15221282`), `sku` (`items[].sku` or one size's `sizes[].sku`, e.g. `AS296SCU17ARY`) or `url` (a dafiti.com.br product link, `https://www.dafiti.com.br/<name>-<id>.html`). `/sizes` takes `sku`.

## Examples

### One search item

Request `{"query": "vestido"}` (1 credit): `total` 19233, `total_pages` 401, 54 items of which 12 `sponsored`, 38 with `marketplace` true. One item:

```json
{
  "position": 1,
  "sku": "LA906APF89VULA",
  "product_id": "15463110",
  "name": "Vestido Super Midi Canelado Sem Mangas Cinza",
  "brand": "Lança Perfume",
  "color": "Cinza",
  "price": 120.75,
  "list_price": 483,
  "discount_percent": 75,
  "pix_price": null,
  "card_price": 120.75,
  "max_installments": 2,
  "categories": ["Roupas", "Roupas Femininas", "Vestidos", "Vestido Curto"],
  "sponsored": true,
  "marketplace": true
}
```

The item also carried `url` and `image`. `marketplace` true says a partner store sells it; the store's name comes from `/product` or `/sizes`.

### One product

Request `{"product_id": "15221282"}` (1 credit), abridged to three sizes:

```json
{
  "sku": "AS296SCU17ARY",
  "product_id": "15221282",
  "name": "Tênis Unissex Asics Gel 1130 Bege",
  "brand": "Asics",
  "color": "Bege",
  "availability": "limited",
  "price": 389.99,
  "list_price": 699.99,
  "discount_percent": 44,
  "pix_price": 389.99,
  "card_price": 410.52,
  "max_installments": 8,
  "seller": { "store_name": "Dafiti", "sold_by_dafiti": true, "delivered_by_dafiti": true },
  "store_names": ["Dafiti"],
  "size_count": 11,
  "sizes_in_stock": 4,
  "sizes": [
    { "size": "40", "sku": "AS296SCU17ARY-54", "in_stock": false, "units": 0, "more_than_10": false, "stock_message": "Esgotado", "delivery_type": "proprio", "sold_by_dafiti": true, "delivered_by_dafiti": true, "store_name": "Dafiti" },
    { "size": "41", "sku": "AS296SCU17ARY-52", "in_stock": true, "units": 5, "more_than_10": false, "stock_message": "restam 5 itens", "delivery_type": "proprio", "sold_by_dafiti": true, "delivered_by_dafiti": true, "store_name": "Dafiti" },
    { "size": "44", "sku": "AS296SCU17ARY-44", "in_stock": true, "units": 1, "more_than_10": false, "stock_message": "resta 1 item", "delivery_type": "proprio", "sold_by_dafiti": true, "delivered_by_dafiti": true, "store_name": "Dafiti" }
  ]
}
```

The product also carried sizes 34 to 44 (34 to 40 sold out, 42 with 5 units, 43 with 2), `rating` and `review_count` null, 5 `categories`, 5 `breadcrumbs`, 6 `specs` (Ocasião de uso: Casual, Fechamento: Cadarço, País de origem: Indonesia, ...), 4 `details` (Composição: Têxtil, Medidas da peça: Sola com 5cm, ...) and 6 images.

### Sizes, brand, category and outlet

- `/sizes` `{"sku": "AS296SCU17ARY"}`: the same 11 sizes and units, `installment` {"count": 7, "amount": 55.71} (the size data's plan; the product page showed up to 8 on card), in 1.4 seconds.
- `/brand` `{"brand": "asics"}`: `title` Tênis Asics, `total` 1575, first the Asics Gel Sonoma TR62 men's sneaker at R$ 549.99 by Pix and R$ 578.94 on card (up to 10 installments) against R$ 899.99.
- `/category` `{"category": "calcados-femininos/tenis"}`: `title` Tênis Feminino, `total` 13098, breadcrumbs Feminino > Calçados Femininos > Tênis.
- `/deals` `{"sort": "discount"}`: the outlet, `total` 199, first a Tricae children's high-top sneaker at R$ 30.99 against R$ 99.90 (69 percent off), no sponsored slots.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def dafiti(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/dafiti/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Asics, deepest discount first (1 credit; listings are slow)
hits = dafiti("brand", {"brand": "asics", "sort": "discount"})["data"]
for it in hits["items"][:5]:
    print(it["name"], it["price"], it["list_price"], it["discount_percent"], it["marketplace"], it["sku"])

# 2. Every size of the first one, with units and seller store (1 credit)
sizes = dafiti("sizes", {"sku": hits["items"][0]["sku"]})["data"]
for s in sizes["sizes"]:
    left = "more than 10" if s["more_than_10"] else s["units"]
    print(s["size"], left, s["delivery_type"], s["store_name"])

# Dafiti prices and stock change during the day. Store each answer with
# fetched_at and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `country`, `currency` and `language`.

- **search / category / brand / deals** - `query` (search), `category`, `url` and `breadcrumbs[]` {`name`, `url`} (category), `brand`, `url` and `breadcrumbs` (brand), `deal` and `url` (deals), `title`, `page`, `page_size` (48), `total`, `total_pages`, `has_more`, `count`, `sponsored_count`, `sort`, `items[]` {`position`, `sku`, `product_id`, `name`, `brand`, `color`, `url`, `image`, `price`, `list_price`, `discount_percent`, `pix_price`, `card_price`, `max_installments`, `categories`, `sponsored`, `marketplace`}, `notes`.
- **product** - `requested`, `sku`, `product_id`, `name`, `brand`, `color`, `url`, `availability` (in_stock, limited, out_of_stock), `price`, `list_price`, `discount_percent`, `pix_price`, `card_price`, `max_installments`, `installment` {`count`, `amount`}, `rating`, `review_count`, `seller` {`store_name`, `sold_by_dafiti`, `delivered_by_dafiti`}, `store_names`, `size_count`, `sizes_in_stock`, `sizes[]` {`size`, `sku`, `in_stock`, `units`, `more_than_10`, `stock_message`, `delivery_type` (proprio, fulfillment, drop_shipping), `sold_by_dafiti`, `delivered_by_dafiti`, `store_name`}, `colors[]` {`sku`, `product_id`, `name`, `color`, `url`, `image`, `price`, `list_price`}, `categories`, `campaigns`, `breadcrumbs`, `specs[]` {`name`, `value`}, `details[]` {`name`, `value`}, `images`, `notes`. No marketing description, review texts or shipping quote.
- **sizes** - `requested`, `requested_size`, `sku`, `product_id`, `name`, `brand`, `color`, `url`, `price`, `list_price`, `discount_percent`, `installment`, `store_names`, `size_count`, `sizes_in_stock`, `sizes[]` (as above), `colors`, `categories`, `campaigns`, `notes`.

## Guardrails

- Name it "Dafiti (dafiti.com.br, the Brazilian fashion marketplace)" on first mention. Dafiti accounts, carts and checkout are not read or made.
- Prices: quote `price`, `pix_price` (where set), `card_price` and `list_price` with the seller and the `fetched_at` date, in BRL (R$). Never compute a Pix discount or an installment.
- Stock: `units` is exact from 0 to 10; when `more_than_10` is true, say "more than 10 units", never a number. Units are the online count for that size and store, not store stock.
- Delivery type: `proprio` is Dafiti's own stock, `fulfillment` a partner store's stock delivered by Dafiti, `drop_shipping` an item sent by the partner store. Quote it as given.
- Sellers: name a marketplace seller only by `store_name`, the store's name as `/product` or `/sizes` gives it. Never look for or name a person behind a store.
- Search: the site matches loosely, so check that a result really is the item asked for before quoting it. `sponsored` items are paid slots; say so when ranking.
- Use: Dafiti's terms of use bar data-mining software. Keep any use descriptive (prices, sizes and stock as facts with their date); do not republish Dafiti's product photos, page copy or links to its pages, and refer to products by `sku` and `product_id`.
- Comparing Dafiti with C&A Brasil, Renner or another store: compare the same product, size, seller and date. Never call one store cheaper beyond the numbers shown.
- Not available: review texts, shipping quotes by CEP, search suggestions, deal start and end dates, price history (poll and store), Dafiti's other countries, account data, cart or checkout. This API cannot buy or reserve anything.
- Terms: Scavio does not store Dafiti data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Dafiti's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, units, sellers or delivery types. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id, sku or url is required"; "Pass one of product_id, sku or url (got ...)."; "category must be a department or category path of 1 to 3 levels as the site writes it (e.g. calcados-femininos or calcados-femininos/tenis)."; "brand must be a brand as the site writes it in its link (e.g. asics, nike, farm-rio)."; "url must be a dafiti.com.br product link (https://www.dafiti.com.br/<name>-<id>.html)."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Dafiti has no product for this id.", "Dafiti has no product with sku <sku> (items[].sku).", "Dafiti has no size <size sku> for sku <sku> (sizes[].sku).", "Dafiti has no product listing at <category>.", "Dafiti has no brand page for <brand>.". A search with no products is an empty `200`, not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=dafiti-api).
- `502` and `503` mean Dafiti data was temporarily unavailable ("Dafiti is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds. When the size data alone is unavailable, `/product` still answers with `sizes` null and a note; call `/sizes` again.
- Listing pages usually take 15-160 seconds (in the captures 4-16 seconds), the product 6-35 seconds, sizes 2-15 seconds. Allow a client timeout of at least 240 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.105.0
npm install scavio@0.106.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.dafiti.search({ query: "tenis", sort: "price_asc" });
const { data: sneakers } = await scavio.dafiti.category({ category: "calcados-femininos/tenis" });
const { data: asics } = await scavio.dafiti.brand({ brand: "asics", sort: "discount" });
const { data: outlet } = await scavio.dafiti.deals({ sort: "discount" });
const { data: item } = await scavio.dafiti.product({ product_id: "15221282" });
const { data: sizes } = await scavio.dafiti.sizes({ sku: "AS296SCU17ARY" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.dafiti.search(...)`, `category`, `brand`, `deals`, `product` and `sizes`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 6 endpoints as tools: `search_dafiti`, `get_dafiti_category`, `get_dafiti_brand`, `get_dafiti_deals`, `get_dafiti_product` and `get_dafiti_sizes`. Dafiti is opt-in: add `dafiti` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.105.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,dafiti"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/dafiti-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=dafiti-api), [category](https://scavio.dev/docs/dafiti-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=dafiti-api), [brand](https://scavio.dev/docs/dafiti-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=dafiti-api), [deals](https://scavio.dev/docs/dafiti-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=dafiti-api), [product](https://scavio.dev/docs/dafiti-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=dafiti-api), [sizes](https://scavio.dev/docs/dafiti-sizes?utm_source=agent-skills&utm_medium=skill&utm_campaign=dafiti-api). Platform page: [scavio.dev/dafiti-api](https://scavio.dev/dafiti-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=dafiti-api).
