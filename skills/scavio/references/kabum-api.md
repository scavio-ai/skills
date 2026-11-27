# KaBuM! API - Prices, Pix Price, Offers, Marketplace Sellers, Shipping

Read KaBuM! (kabum.com.br, the Brazilian computer and electronics retailer, part of Magalu): keyword search, category listings, the department list and category trees, one product with every payment plan and its specs, delivery options to a Brazilian CEP, customer reviews, and the offers of a KaBuM! campaign. www.kabum.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in. Every endpoint returns structured JSON and costs 1 credit.

**The job this skill is for: what an item costs at KaBuM! today, by card and by Pix, in which offer, from which seller, and what delivery to a CEP costs.** KaBuM! shows two prices on every item and this skill returns both as KaBuM! shows them, never computed. On 2026-11-27 the Cadeira Gamer Husky Storm 100 (product `311424`) read `price` R$ 433.32 (the card price, `installment_text` "10x de R$ 43,33"), `cash_price` R$ 389.99 (Pix, Brazil's instant payment, or boleto, `cash_discount_percent` 10) and `list_price` R$ 588.78, inside the OFERTAS KABUM offer (`discount_percent` 26, ending 2026-11-30T13:00Z, `units_left` 35), with `stock` 1981 and `buy_limit` 5, sold by KaBuM!. The Black Friday campaign "BLACK DAS BLACKS KABUM!" listed 620 offers.

Seven limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Two prices, both as given.** `price` is the card price (what the installment plan adds up to), `cash_price` the Pix / boleto price. With a running offer both are the offer's prices and `list_price` is the regular card price. Never compute one from the other.
- **Never Prime-member prices.** KaBuM! Prime prices are not returned, and Prime-member filters are refused (`400`).
- **Offer stock is not product stock.** `offer.units_left` (and `offer_units_left` / `offer_units_sold` on `/offers`) count the offer's own allotment; `stock` counts the product's units.
- **Marketplace sellers are businesses.** `seller` is KaBuM! (`is_marketplace` false) or a marketplace seller with `sold_by`, `company`, `cnpj` and `state` as KaBuM! lists them. A marketplace seller quotes its own delivery options.
- **Delivery is for one unit to one CEP.** `/shipping` quotes one unit to an 8-digit CEP (the Brazilian postal code). There are no stores and no store stock: KaBuM! sells online.
- **No history, no suggestions.** Everything is the page at the moment of the call; Scavio keeps nothing. There are no search suggestions, store pages or Q&A. Poll and store your own series.

KaBuM! has no public API for its catalog, prices or offers. Prices and stock are shown on kabum.com.br for each item, and this skill reads those public pages with one Scavio key.

See also: Magazine Luiza `magalu-magazine-luiza-api` (KaBuM!'s parent group), Mercado Libre `mercadolibre-product-data`, Casas Bahia `casas-bahia-api`, Buscape + Zoom `buscape-zoom-api` (Brazilian price comparison); the same item at Amazon `amazon-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price an item at KaBuM!: card price, Pix / boleto price, regular price, installment plan, cash discount
- Search kabum.com.br by keyword (in Portuguese: "cadeira gamer", "placa de video", "ssd 1tb"), sorted by KaBuM!'s own order, price, most reviewed or newest, filtered by brand, color, KaBuM! stamp (BLACK FRIDAY), offers only, sold by KaBuM!, open box or a price range
- Browse one KaBuM! category (hardware/placa-de-video-vga, tv) or read the department list and a department's category tree
- Read one KaBuM! product: brand, specs, warranty, weight, stock, buy limit, every payment plan (boleto, Pix, card 1-12x with and without interest, NuPay), Anatel and Inmetro codes
- See who sells an item (KaBuM! or a marketplace seller) with the seller's business name, CNPJ, state and KaBuM!'s seller score
- Quote delivery of a product to a Brazilian CEP: options, price, max days, arrival date
- Read KaBuM! customer reviews, newest or oldest first, filtered by stars
- List the offers of a KaBuM! campaign (Black Friday 2026, OFERTAS KABUM) with offer units left and sold

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=kabum-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=kabum-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Calls usually take 2-15 seconds (in the captures: category 1.8, reviews 2.1, offers 3.6, product 5.1 (9.0 with a marketplace seller's score), categories 6.2, search 6.9, shipping 7.9). Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/kabum/search` | Keywords: up to 100 items per page with total, card and Pix prices, list price, installment text, running offer, stock, buy limit, seller, rating, stamps; facets | 1 |
| `POST /api/v1/kabum/category` | One category by path, same items, sorts, filters and facets as search, with its breadcrumb | 1 |
| `POST /api/v1/kabum/categories` | The departments (about 30), or one department's category tree with the path category takes | 1 |
| `POST /api/v1/kabum/product` | One product: prices, offer, every payment plan, stock, buy limit, specs, warranty, weight, seller with score | 1 |
| `POST /api/v1/kabum/shipping` | Delivery options for one unit to a Brazilian CEP: name, price, max days, arrival date, seller | 1 |
| `POST /api/v1/kabum/reviews` | Customer reviews newest or oldest first, up to 50 per page, filtered by stars, with KaBuM!'s own summary as given (no reviewer names) | 1 |
| `POST /api/v1/kabum/offers` | One campaign (blackfriday by default, or ofertaskabum): its window and rules link, up to 100 offers per page with offer units left and sold | 1 |

Brazil only: there is no `country` parameter. Every answer carries `country` (br), `currency` (BRL) and `language` (pt-BR).

## Prices: card, Pix, list price, offer and payment plans

Every listing item and product carries KaBuM!'s price layers as kabum.com.br shows them to a visitor who is not signed in:

| Field | Meaning |
|---|---|
| `price` | The card price in BRL: what the installment plan adds up to (R$ 433.32 on the Husky Storm 100) |
| `cash_price` | The Pix / boleto price (R$ 389.99) |
| `cash_discount_percent` | KaBuM!'s discount for paying by Pix or boleto (10) |
| `list_price` | The regular card price when a lower price applies (R$ 588.78); null otherwise |
| `installment_text` | KaBuM!'s installment line as written ("10x de R$ 43,33") |
| `offer` | The running offer: `{offer_id, name, campaign, price, cash_price, discount_percent, starts_at, ends_at, units_left}`; null when none runs |
| `payment_methods[]` (product) | `{category (boleto, pix, cartao, nupay), method, installments[] {installments, amount, total, interest, discount_percent, terms, interest_text}}` as given |
| `stock`, `buy_limit` | The product's units in stock and the most one order may take |
| `stamps` | KaBuM!'s stamps on the item (BLACK FRIDAY, CUPOM LATIDO, BOM PRA KABUM) |

- Quote "Cadeira Gamer Husky Storm 100: R$ 389.99 by Pix or R$ 433.32 by card (10x de R$ 43,33) at kabum.com.br on 2026-11-27, regular price R$ 588.78, OFERTAS KABUM offer until 2026-11-30", with the date.
- The card plan of the Husky Storm 100 ran 1x at R$ 389.99 (10% off), 2x-10x without interest to R$ 433.32, and 11x and 12x with interest (12x de R$ 40,44, total R$ 485.32). Quote `total` and `interest` from `payment_methods`, never compute a plan.
- `offer.discount_percent` is KaBuM!'s own figure against the regular price. Report KaBuM!'s prices, labels and dates and the arithmetic only. Never judge a price as a good deal.

## Workflow

1. **Find the item.** `/search` with `query` (`cadeira gamer`), or `/category` with a `category` path from `/categories` (`hardware/placa-de-video-vga`). Each item's `product_id` is the input of product, shipping and reviews.
2. **Narrow it.** Read `facets[]` of an answer and send `filters` with keys and values exactly as listed (`{"manufacturer": "Husky", "has_offer": true}`), plus `price_min` / `price_max` in BRL.
3. **One product.** `/product` with `product_id` (or `url`): every payment plan, stock, buy limit, specs, warranty and the seller; a marketplace seller carries `score`.
4. **Delivery.** `/shipping` with `product_id` and `cep`: each option's price, `max_days` and `arrival_date`.
5. **Reviews.** `/reviews` with `product_id`, optionally `rating` and `sort`.
6. **Campaign offers.** `/offers` with `campaign` (`blackfriday` or `ofertaskabum`): the campaign window and every offer with units left and sold.
7. **Watching prices:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`) and category (`/category`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords in Portuguese as shoppers type them, 1-200 characters |
| `category` (category, required) | A category path (`categories[].path`, or a category link's path), e.g. `tv` or `hardware/placa-de-video-vga` |
| `sort` | `most_searched` (default, KaBuM!'s own order), `price_asc`, `price_desc`, `most_reviewed`, `newest` |
| `page` | 1-500; `total_pages` reports the last one |
| `page_size` | 1-100, default 20 |
| `filters` | Up to 8 facets: `{key: value or [values]}` exactly as `facets[].key` and `facets[].values` list them (`manufacturer`, `Cor`, `highlighted_stamp` such as "BLACK FRIDAY"); boolean facets (`has_offer`, `kabum_product`, `has_open_box`, `has_flash`) take `true`. Up to 20 values per key |
| `price_min`, `price_max` | Card price range in BRL (0-1,000,000). `filters.price` is refused: use these |

A keyword KaBuM! sends to a category carries `site_category` (`cadeira gamer` went to `espaco-gamer/cadeiras-gamer`); ask `/category` for that category's own listing. A keyword with no products returns `total` 0.

### Categories (`/categories`)

`department` (optional): a department slug as `departments[].slug` lists it (`hardware`). Without it, the departments `{slug, path, url}`; with it, the tree `categories[]` `{slug, path, url, children}`.

### Product (`/product`), shipping (`/shipping`) and reviews (`/reviews`)

| Parameter | Description |
|---|---|
| `product_id` | The KaBuM! product code (`items[].product_id`, the number after /produto/ in a product link), e.g. `311424` |
| `url` | Or a www.kabum.com.br product link. Send `product_id` or `url` |
| `cep` (shipping, required) | The Brazilian CEP to deliver to: 8 digits, `01310-100` or `01310100` |
| `rating` (reviews) | Only reviews with this many stars, 1-5 |
| `sort` (reviews) | `newest` (default) or `oldest` |
| `page`, `page_size` (reviews) | Page 1-500; 1-50 per page, default 10 |

### Offers (`/offers`)

| Parameter | Description |
|---|---|
| `campaign` | `blackfriday` (default, Black Friday 2026) or `ofertaskabum` (KaBuM!'s standing offers) |
| `page`, `page_size` | Page 1-500; 1-100 per page, default 20 |

## Examples

### One search item with a running offer

Request `{"query": "cadeira gamer", "page_size": 10}` (1 credit): `total` 648, `total_pages` 65, `site_category` espaco-gamer/cadeiras-gamer, 11 facets. The first item:

```json
{
  "position": 1,
  "product_id": "311424",
  "name": "Cadeira Gamer Husky Storm 100, Até 120kg, Almofadas, Reclinável 135º, PU, Preta - HCG100PT",
  "brand": "Husky",
  "category_path": "Espaço Gamer/Cadeiras Gamer/Husky Gaming",
  "price": 433.32,
  "cash_price": 389.99,
  "list_price": 588.78,
  "cash_discount_percent": 10,
  "installment_text": "10x de R$ 43,33",
  "offer": {
    "offer_id": "1046733",
    "name": "OFERTAS KABUM",
    "campaign": "ofertaskabum",
    "price": 433.32,
    "cash_price": 389.99,
    "discount_percent": 26,
    "starts_at": "2026-11-25T12:58:14.000Z",
    "ends_at": "2026-11-30T13:00:00.000Z",
    "units_left": 35
  },
  "currency": "BRL",
  "available": true,
  "stock": 1981,
  "buy_limit": 5,
  "seller": { "sold_by": "KaBuM!", "is_marketplace": false, "seller_id": null, "company": null, "cnpj": null, "state": null },
  "rating": 4.8,
  "review_count": 159,
  "stamps": [],
  "free_shipping": false,
  "open_box": false,
  "pre_order": false
}
```

The second item, the Husky Tempest 700, read R$ 777.77 by card and R$ 699.99 by Pix against R$ 1,222.11, offer 36 percent off with 256 units left.

### A marketplace seller with its score

Request `{"product_id": "217839"}` (1 credit): an Intelbras wireless transmitter at R$ 40.11 by card and R$ 36.10 by Pix, `stock` 18, `warranty` "Sem Garantia", sold by a marketplace seller:

```json
{
  "seller": {
    "type": "3P",
    "sold_by": "Digi Mania",
    "is_marketplace": true,
    "seller_id": "2958",
    "company": "Digi Mania Comércio Eletrônico Eireli",
    "cnpj": "19.457.025/0001-47",
    "state": "SP",
    "score": {
      "rating": 5,
      "nps": 5,
      "delivery_rating": 5,
      "orders": 7424,
      "period_start": "2026-10-27T21:00:00",
      "period_end": "2026-11-26T21:00:00"
    }
  }
}
```

`type` is 1P, 2P or 3P as KaBuM! classes the seller; the Husky Storm 100 read 2P, sold by KaBuM!, with `score` null.

### Delivery to a CEP

Request `{"product_id": "311424", "cep": "01310-100"}` (1 credit):

```json
{
  "product_id": "311424",
  "cep": "01310100",
  "address": { "state": "SP", "city": "São Paulo", "district": "Bela Vista", "street": "Avenida Paulista" },
  "sold_by": "KaBuM!",
  "available": true,
  "count": 4,
  "options": [
    { "name": "Entrega Econômica", "type": "T", "price": 34.59, "max_days": 12, "arrival_date": "2026-12-15", "arrival_text": "até 15/12/2026", "arrives_tomorrow": false, "carrier": null, "flash": false, "seller": "KaBuM!" },
    { "name": "Entrega Padrão", "type": "T", "price": 66.11, "max_days": 11, "arrival_date": "2026-12-14", "arrival_text": "até 14/12/2026", "arrives_tomorrow": false, "carrier": null, "flash": false, "seller": "KaBuM!" },
    { "name": "Entrega Expressa", "type": "C", "price": 113.13, "max_days": 9, "arrival_date": "2026-12-10", "arrival_text": "até 10/12/2026", "arrives_tomorrow": false, "carrier": null, "flash": false, "seller": "KaBuM!" },
    { "name": "Entrega Agendada", "type": "AGENDADO", "price": 34.59, "max_days": 48, "arrival_date": "2027-01-14", "arrival_text": "até 14/01/2027", "arrives_tomorrow": false, "carrier": null, "flash": false, "seller": "KaBuM!" }
  ]
}
```

For Entrega Agendada, `arrival_date` is the last date the delivery can be scheduled for.

### One campaign offer

Request `{"campaign": "blackfriday", "page_size": 10}` (1 credit): `campaign` {`name` "BLACK DAS BLACKS KABUM!", `starts_at` 2026-11-25T11:00Z, `ends_at` 2026-11-30T14:00Z, `rules_url`}, `total` 620, `total_pages` 62. The first offer:

```json
{
  "position": 1,
  "product_id": "151914",
  "name": "Mesa Gamer Husky Snow, Preto - Superfície em Fibra de Carbono, Suporte para Headset e Copo, Resistente à Umidade - HDG100",
  "brand": "Husky",
  "department": "Espaço Gamer",
  "category": "Mesa Gamer",
  "price": 388.88,
  "cash_price": 349.99,
  "list_price": 555.54,
  "discount_percent": 29,
  "installment_text": "10x de R$ 38,88",
  "offer_id": "1013259",
  "offer_units_left": 28,
  "offer_units_sold": 72,
  "stock": 496,
  "starts_at": "2026-11-25T12:55:00.000Z",
  "ends_at": "2026-11-30T14:00:00.000Z",
  "available": true,
  "seller": { "sold_by": "KaBuM!", "is_marketplace": false, "seller_id": null },
  "stamp": "BLACK FRIDAY",
  "rating": 4.9,
  "review_count": 127
}
```

### Category, categories and reviews

- `/category` `{"category": "hardware/placa-de-video-vga", "sort": "price_asc", "page_size": 10}`: breadcrumb Hardware > Placa de vídeo (VGA), `total` 459 over 46 pages, lowest first a R$ 19.90 GPU support bracket from a marketplace seller.
- `/categories` `{"department": "hardware"}`: `count` 14 top categories (memoria-ram, placas-mae, placa-de-video-vga, coolers, disco-rigido-hd, ssd-2-5, fontes, processadores, ...), each {`slug`, `path`, `url`, `children`}; `hardware/memoria-ram/ddr-3/1600-mhz-pc12800` is a valid category path. Without `department`, about 30 departments.
- `/reviews` `{"product_id": "311424"}`: `average_rating` 4.8, `total_reviews` 156, 16 pages of 10, `summary` null (KaBuM! showed none), each {`review_id`, `rating`, `title` ("Recomendo"), `text`, `date`, `likes`, `media`}. No reviewer names.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def kabum(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/kabum/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Gaming chairs with a running offer, lowest card price first (1 credit)
hits = kabum("search", {"query": "cadeira gamer", "sort": "price_asc", "filters": {"has_offer": True}})["data"]
item = hits["items"][0]
print(item["name"], item["price"], item["cash_price"], item["list_price"], item["offer"])

# 2. The product with every payment plan and the seller (1 credit)
prod = kabum("product", {"product_id": item["product_id"]})["data"]
print(prod["stock"], prod["buy_limit"], prod["seller"]["sold_by"], prod["seller"]["cnpj"])

# 3. Delivery to a CEP in Sao Paulo (1 credit)
ship = kabum("shipping", {"product_id": item["product_id"], "cep": "01310-100"})["data"]
for o in ship["options"]:
    print(o["name"], o["price"], o["max_days"], o["arrival_date"])

# KaBuM! prices and offers change daily. Store each answer with fetched_at and run
# this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `country`, `currency` and `language`, and most carry `notes`.

- **search / category** - `query` (search) or `category`, `url` and `breadcrumb[]` {`id`, `name`, `path`} (category), `site_category` (search), `page`, `page_size`, `sort`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `product_id`, `name`, `url`, `image`, `brand`, `category_path`, `price`, `cash_price`, `list_price`, `cash_discount_percent`, `installment_text`, `offer`, `currency`, `available`, `stock`, `buy_limit`, `seller` {`sold_by`, `is_marketplace`, `seller_id`, `company`, `cnpj`, `state`}, `rating`, `review_count`, `stamps`, `free_shipping`, `open_box`, `pre_order`}, `facets[]` {`key`, `label`, `type` (list, boolean, range), `values` or `min` / `max`}, `filters_applied`.
- **categories** - `count`, `departments[]` {`slug`, `path`, `url`}; with `department`: `department`, `url`, `categories[]` {`slug`, `path`, `url`, `children[]`}.
- **product** - `product_id`, `name`, `url`, `brand`, `categories[]` {`id`, `name`, `path`}, `images`, `price`, `cash_price`, `list_price`, `cash_discount_percent`, `installment_text`, `offer`, `payment_methods[]`, `available`, `discontinued`, `stock`, `buy_limit`, `pre_order`, `pre_order_date`, `open_box`, `free_shipping`, `digital`, `weight_grams`, `warranty`, `rating`, `review_count`, `stamps`, `seller` {`type` (1P, 2P, 3P), `sold_by`, `is_marketplace`, `seller_id`, `company`, `cnpj`, `state`, `score` {`rating`, `nps`, `delivery_rating`, `orders`, `period_start`, `period_end`}}, `specs[]` {`section`, `items[]` {`name`, `value`}, `lines`}, `anatel_code`, `inmetro_code`, `variant_group_id`.
- **shipping** - `product_id`, `name`, `cep`, `address` {`state`, `city`, `district`, `street`}, `sold_by`, `available`, `count`, `options[]` {`name`, `type`, `price`, `max_days`, `arrival_date`, `arrival_text`, `arrives_tomorrow`, `carrier`, `flash`, `seller`}.
- **reviews** - `product_id`, `sort`, `rating`, `page`, `page_size`, `average_rating`, `total_reviews`, `total` (matching `rating`), `total_pages`, `has_more`, `count`, `summary`, `reviews[]` {`review_id`, `rating`, `title`, `text`, `date`, `likes`, `media[]` {`type`, `url`}}.
- **offers** - `campaign` {`slug`, `name`, `title`, `starts_at`, `ends_at`, `rules_url`}, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `product_id`, `name`, `url`, `image`, `brand`, `department`, `category`, `currency`, `price`, `cash_price`, `list_price`, `discount_percent`, `installment_text`, `offer_id`, `offer_units_left`, `offer_units_sold`, `stock`, `starts_at`, `ends_at`, `available`, `seller` {`sold_by`, `is_marketplace`, `seller_id`}, `stamp`, `free_shipping`, `open_box`, `rating`, `review_count`}.

## Guardrails

- Name it "KaBuM! (kabum.com.br, the Brazilian computer and electronics retailer, part of Magalu)" on first mention. KaBuM! accounts, KaBuM! Prime and carts are not read.
- Prices: quote `cash_price` (Pix / boleto) and `price` (card) side by side in BRL (R$), with `list_price`, the offer and the `fetched_at` date. Prices are what a visitor who is not signed in sees on kabum.com.br. Never present either as a Prime-member price.
- Payment plans: quote `installment_text` or `payment_methods` exactly as given, including `interest` and `total`. Never compute an installment or apply a percent yourself.
- Offers: quote `ends_at` and `units_left` with the date; both change through the day. Offer units are the offer's allotment, not the product's stock.
- Sellers: a marketplace seller's `company`, `cnpj` and `state` are the business details KaBuM! lists. Refer to a seller by `sold_by` or its company name; do not profile the people behind a business.
- Comparing KaBuM! with Magalu, Mercado Libre or Amazon: compare the same model (brand and model code from `specs`), payment method and date. Never call one retailer cheaper beyond the numbers shown.
- Reviews: no reviewer names are returned. Quote a review as "a KaBuM! customer review"; `summary` is KaBuM!'s own text as given.
- Images and copy: do not republish KaBuM!'s product images or product copy; link items by `product_id` or `url` instead.
- Not available: Prime-member prices, search suggestions, stores or store stock, Q&A, variants, price history (poll and store), account data, cart or checkout. This API cannot reserve or buy an item.
- Terms: Scavio does not store KaBuM! data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. KaBuM!'s terms of use may restrict automated access or commercial use of its site; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, offers, units, ids, CNPJs, dates or ratings. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id or url is required (a KaBuM! product code, e.g. 311424, or its link)."; "product_id must be a KaBuM! product code: digits, e.g. 311424 (items[].product_id)."; "url must be a KaBuM! product link: https://www.kabum.com.br/produto/<code>/<name>."; "category must be a KaBuM! category path: lowercase slugs joined by /, e.g. hardware/placa-de-video-vga or tv."; "department must be a department slug as departments[].slug lists it, e.g. hardware."; "cep must be a Brazilian CEP: 8 digits, e.g. 01310-100 or 01310100."; "cep <cep> is not a CEP KaBuM! delivers to (KaBuM! answers: invalid CEP)."; "KaBuM! gives no delivery quote for product <id> to cep <cep>."; "filters: at most 8 facets."; "filters.<key> is a Prime-member filter and is not offered."; "filters.price is not accepted: send price_min and price_max."; "price_min must not be above price_max."; "campaign must be a KaBuM! campaign slug, e.g. blackfriday or ofertaskabum."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "No KaBuM! product <id>.", "No KaBuM! category <path> (or it has no products with these filters). See categories for the paths.", "No KaBuM! department <slug>.", "No KaBuM! campaign <campaign>.", "No KaBuM! campaign <campaign> is running (blackfriday and ofertaskabum are).". A keyword with no products answers `total` 0, a discontinued product answers `available` false and `stock` 0, and a product KaBuM! does not sell now answers shipping with `available` false and no options, all with `200`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=kabum-api).
- `502` and `503` mean KaBuM! data was temporarily unavailable ("KaBuM! is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.102.0
npm install scavio@0.103.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.kabum.search({ query: "cadeira gamer", sort: "price_asc", filters: { has_offer: true } });
const { data: grid } = await scavio.kabum.category({ category: "hardware/placa-de-video-vga", price_min: 1000, price_max: 2000 });
const { data: tree } = await scavio.kabum.categories({ department: "hardware" });
const { data: product } = await scavio.kabum.product({ product_id: "311424" });
const { data: ship } = await scavio.kabum.shipping({ product_id: "311424", cep: "01310-100" });
const { data: reviews } = await scavio.kabum.reviews({ product_id: "311424", rating: 5 });
const { data: offers } = await scavio.kabum.offers({ campaign: "blackfriday" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.kabum.search(...)`, `category`, `categories`, `product`, `shipping`, `reviews` and `offers`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 7 endpoints as tools: `search_kabum`, `get_kabum_category`, `get_kabum_categories`, `get_kabum_product`, `get_kabum_shipping`, `get_kabum_reviews` and `get_kabum_offers`. KaBuM! is opt-in: add `kabum` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.102.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,kabum"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/kabum-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=kabum-api), [category](https://scavio.dev/docs/kabum-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=kabum-api), [categories](https://scavio.dev/docs/kabum-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=kabum-api), [product](https://scavio.dev/docs/kabum-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=kabum-api), [shipping](https://scavio.dev/docs/kabum-shipping?utm_source=agent-skills&utm_medium=skill&utm_campaign=kabum-api), [reviews](https://scavio.dev/docs/kabum-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=kabum-api), [offers](https://scavio.dev/docs/kabum-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=kabum-api). The platform page: [scavio.dev/kabum-api](https://scavio.dev/kabum-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=kabum-api).
