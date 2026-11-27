# Buscape + Zoom API - Price Comparison, Store Offers, Price History, Coupons

Read Buscape and Zoom (buscape.com.br, zoom.com.br, Brazil's price comparison sites): keyword search, category listings, the deals list, the category tree, one product with the offers its page shows, every store offer with paging and sorting, the daily lowest-price history, the current lowest price, campaign landings, a store's coupons, search suggestions and freight estimates to a CEP. Both sites share one catalog and the same ids; `site` picks `buscape` (default) or `zoom` and sets the site of the page links returned. Brazil only, Portuguese text, prices in BRL. Every endpoint returns structured JSON and costs 1 credit.

**The job this skill is for: what one product costs across Brazilian stores today, and how its lowest price moved.** The sites compare offers from many stores for one product and this skill returns each one as the site shows it, never computed. On 2026-11-27 the iPhone 16 128GB (product `12755140`) had `offer_count` 22 from `store_count` 6: `best_offer` R$ 4.537,84 at Amazon (stock 50) and `priciest_offer` R$ 7.903,26 at Magazine Luiza. Its `price_tip` read `regular_price` against a `median_price` of R$ 4.549 for 2026-10-19 to 2026-11-27, and its price history showed the day's lowest price at R$ 4.958,99 on 2026-10-19, a 40-day high of R$ 5.057,99 on 2026-10-28 and a low of R$ 4.299 on 2026-11-22. A Brastemp BRM46MB 385L refrigerator (product `13994006`) had 54 offers from 5 stores starting at R$ 2.308 at Magazine Luiza (10x R$ 256,44, R$ 2.564,40 with interest).

Seven limits shape every answer, so say them plainly:
- **1 credit on every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Prices are the site's numbers.** `price` is the cash price the site labels "a vista"; `installments` and `installment_total` are the store's card plan. A product's `price` in a listing is the lowest cash price among its stores. Quote each price with its store and date.
- **History is the day's lowest price, not one store's.** Each point is the lowest price across stores that day and the store it came from: 40 daily points by default, or 3 to 12 months of daily points.
- **The price tip is the site's label, as given.** `price_tip.label` (good_price, regular_price, best_history_price, not_enough_history) compares today's price with the site's 40-day median. Quote it as "Buscape's price tip", never as advice.
- **No store links.** Offers name the store and its id, never a link to the store's page. Store ratings are not published by the sites.
- **Listings can be uneven.** The sites return some pages with fewer items than `page_size` and gaps in `position`; `total` is capped at 10,000 (`total_capped`).
- **Nothing is stored.** Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series for anything beyond the history the sites show.

Buscape and Zoom have no public API. Prices and offers are shown on the sites for each product, and this skill reads those public pages with one Scavio key.

See also: Google Shopping `google-shopping-api`; the stores themselves, KaBuM! `kabum-api`, Magalu `magalu-magazine-luiza-api`, Casas Bahia `casas-bahia-api`, Mercado Libre `mercadolibre-product-data`.

## When to trigger

Use this skill when the user asks to:
- Compare what one product costs across Brazilian stores on Buscape or Zoom: every store offer with cash price, installments, stock and condition
- Find the lowest current price of a product and which store has it
- Read a product's price history on Buscape or Zoom: the day's lowest price for 40 days or up to 12 months
- Read Buscape's price tip for a product (good price, regular price, lowest in history) and the editors' pros and cons
- Search Buscape or Zoom by keyword, or list a category, sorted by price, rating or price drop, filtered by brand or any facet, price range, marketplace or best-selling store
- List the Buscape or Zoom deals page, or a campaign landing such as Black Friday or the day's offer
- Read a store's coupon codes on Buscape or Zoom with value and validity, and its cashback percent
- Estimate freight for a product's store offers to a Brazilian CEP (postal code)
- Read search suggestions or the category tree

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Calls usually take 1-9 seconds (in the captures: price history 0.6, suggestions 0.6, deals 1.2, search 1.6, offers 1.9, lowest price 2.1, categories 2.6, category 3.0, shipping 3.2, product 5.2, store 6.2, deal landing 9.1); page-backed endpoints (product, categories, deal landing, store) can take up to about 80 seconds when busy. Allow a client timeout of at least 180 seconds.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/buscape/search` | Keywords: up to 100 items per page with the lowest cash price, installments, store count, stores, best offer, price drop, rating; facets, categories, price range, category suggestion | 1 |
| `POST /api/v1/buscape/category` | One category by id or slug, same items, sorts and filters as search, with breadcrumb | 1 |
| `POST /api/v1/buscape/categories` | The site's top-level branches, or one branch with its categories and ids | 1 |
| `POST /api/v1/buscape/product` | One product: specs, offer and store counts, best and priciest offer, the offers its page shows, variant filters, 40 days of lowest prices, price tip, editors' pros and cons, up to 10 store reviews | 1 |
| `POST /api/v1/buscape/offers` | Every store offer for one product, up to 50 per page, 6 sorts, filtered by variant (voltage) | 1 |
| `POST /api/v1/buscape/price-history` | The day's lowest price and its store for 40 days or 3-12 months, with lowest, highest and latest | 1 |
| `POST /api/v1/buscape/lowest-price` | The product's lowest current price with its offer, store, list price and stock | 1 |
| `POST /api/v1/buscape/deals` | The site's deals list (products scoring 0.8 or more on its competitiveness index), by category or keyword | 1 |
| `POST /api/v1/buscape/deal-landing` | One campaign landing (black-friday, oferta-do-dia-buscape, black-friday-zoom) with its sections as the editors arrange them | 1 |
| `POST /api/v1/buscape/store` | One store: cashback percent and its coupons with code, value, start and expiry | 1 |
| `POST /api/v1/buscape/suggestions` | Search suggestions as the search box shows them, with the category each leads to | 1 |
| `POST /api/v1/buscape/shipping` | Freight estimates per store offer to a CEP (price, delivery days) and the store's coupon promotions | 1 |

Every answer carries `site`, `country` (br), `currency` (BRL) and `language` (pt-BR).

## Offers, prices and history

| Field | Meaning |
|---|---|
| `price` | The cash price the site labels "a vista", in BRL. On a listing item, the lowest cash price among its stores |
| `installments`, `installment_total`, `has_interest` | The store's card plan (`{months, amount, total}`) and whether it carries interest |
| `store` `{id, name, is_marketplace}` | The store of an offer; `is_marketplace` marks a marketplace seller |
| `stock`, `condition`, `cross_border` | The store's stock as given, new or used, and cross-border offers |
| `price_drop_percent`, `competitiveness_index` | The site's price drop and its 0-1 competitiveness score for the offer, as given |
| `best_offer`, `priciest_offer` | The lowest and highest offers the product page shows |
| `price_history_40_days[]`, `points[]` | `{date, price, store_id}`: the day's lowest price across stores and the store it came from |
| `price_tip` | `{label, price, median_price, start, end}`: the site's label for today's price against its 40-day median |
| `expert` | `{pros, cons, date}`: the site editors' pros and cons, as given |

- Quote "iPhone 16 128GB: R$ 4.537,84 at Amazon on Buscape, 2026-11-27 (22 offers from 6 stores, up to R$ 7.903,26)", with the date.
- Installments: quote the plan as given ("10x R$ 256,44, total R$ 2.564,40 with interest"). Never compute your own interest.
- History: say "the day's lowest price across stores on Buscape" and name the store of each point when it matters.
- `stock` is the store's number as the site gives it, not a count Scavio verified.
- Report the sites' prices, labels and dates and the arithmetic only. Never judge a price as a good deal yourself; quote the site's `price_tip` label as the site's.

## Workflow

1. **Find the product.** `/search` with `query` (`geladeira`), `/category` with `category_id` (`8`) or `category` slug (`geladeira`), or `/deals`. Items of `type` product are compared across stores and carry `product_id`; items of `type` offer are a single-store listing with `offer_id` only.
2. **Narrow.** Add `filters` from `facets[]` (`{"Marca": "Samsung"}`), `price_min` / `price_max` in BRL, `marketplace`, or `store` (a store name as `items[].stores[].name` gives it).
3. **One product.** `/product` with `product_id` or `url`: offers its page shows, 40 days of lowest prices, `price_tip`, `expert`, specs and store reviews.
4. **Every offer.** `/offers` with `product_id`, `sort` `price_asc`, and `variant_id` from `variant_filters[].values[]` (e.g. 220V) when the product has variants. Page with `page` and `page_size` (up to 50).
5. **History.** `/price-history` with `product_id` (40 days) or `period` `months` with `months` 3-12. `/lowest-price` for the current low alone.
6. **Freight.** `/shipping` with `product_id`, `cep`, `state` (UF) and `city`: freight per store offer as the product page shows it.
7. **Coupons and campaigns.** `/store` with `store_id` (from `offers[].store.id`) for its coupons; `/deal-landing` with a campaign `slug`.
8. **Watching prices:** poll `/lowest-price` or `/offers` on a schedule and store each answer with its `fetched_at` for anything beyond the history the site shows.

## Parameters

### Search (`/search`), category (`/category`) and deals (`/deals`)

| Param | Type | Notes |
|---|---|---|
| `query` | string | Search: required, keywords in Portuguese (`geladeira`). Category and deals: optional keywords inside |
| `category_id` | string, integer or array | Search and deals: up to 20 category ids. Category: one id (`8`), or send `category` instead |
| `category` | string | Category only: the category slug (`geladeira`) or its link. Send `category_id` or `category`, not both |
| `site` | string | `buscape` (default) or `zoom` |
| `sort` | string | `relevance` (default, the site's own order), `price_asc`, `price_desc`, `rating`, `price_drop` |
| `page`, `page_size` | integer | Page 1-1000; page size 1-100, default 30 |
| `filters` | object | Up to 8 facets: `{key: value or [values]}` exactly as `facets[].key` and `facets[].values[].value` list them |
| `price_min`, `price_max` | number | Price range in BRL |
| `marketplace` | boolean | true: marketplace sellers; false: the stores' own offers |
| `store` | string | Products whose best-selling store is this one (`Magazine Luiza`) |

### Product, offers, price history, lowest price

| Param | Type | Notes |
|---|---|---|
| `product_id` | string or integer | `items[].product_id` of search, category or deals (`12755140`). Required on offers, price history, lowest price and shipping |
| `url` | string | Product only: a product page on www.buscape.com.br or www.zoom.com.br, or its path, instead of `product_id` |
| `sort` | string | Offers: `default`, `price_asc` (cash price), `price_desc`, `installment_price_asc`, `discount_desc`, `cashback_price_asc` (the site's product page order) |
| `variant_id` | string | Offers and shipping: a variant from `variant_filters[].values[].variant_id` (`48733` for 220V) |
| `page`, `page_size` | integer | Offers: page 1-100, page size 1-50, default 20 |
| `period`, `months` | string, integer | Price history: `days` (default, 40 daily points) or `months` with `months` 3-12 |

### Categories, deal landing, store, suggestions, shipping

| Param | Type | Notes |
|---|---|---|
| `branch` | string | Categories: a branch slug (`eletrodomesticos`). Without it, the branches |
| `slug` | string | Deal landing: `black-friday`, `oferta-do-dia-buscape` (Buscape), `black-friday-zoom` (Zoom), or the link |
| `store_id` / `store` | string | Store: the store id (`21`, from `offers[].store.id`) or its page path `<slug>-<id>` (`kabum!-21`) |
| `query`, `limit` | string, integer | Suggestions: what the shopper has typed; 1-20 suggestions, default 8 |
| `cep`, `state`, `city` | string | Shipping: the CEP (8 digits, `01310-100`), its two-letter UF (`SP`) and city in Portuguese (`São Paulo`), all required |
| `sort`, `page_size`, `variant_id` | | Shipping: which offers to estimate (default `price_asc`), 1-50 offers (default 10), a variant |

## Examples

### Every store offer for one product

`POST /api/v1/buscape/offers` with `{"product_id": "13994006", "sort": "price_asc", "page_size": 10}` (1 credit), trimmed from the 2026-11-27 capture:

```json
{
  "site": "buscape",
  "currency": "BRL",
  "product_id": "13994006",
  "sort": "price_asc",
  "total": 54,
  "store_count": 5,
  "total_pages": 6,
  "has_more": true,
  "offers": [
    {
      "position": 1,
      "offer_id": "1563524800",
      "name": "Refrigerador Brastemp Frost Free Duplex 385 Litros Branco BRM46MB 220",
      "store": { "id": "22905", "name": "Magazine Luiza", "is_marketplace": false },
      "price": 2308,
      "installment_total": 2564.4,
      "installments": [{ "months": 10, "amount": 256.44, "total": 2564.4 }],
      "has_interest": true,
      "price_drop_percent": 0,
      "competitiveness_index": 0.8271,
      "stock": 117,
      "condition": "new",
      "cross_border": false
    },
    {
      "position": 2,
      "offer_id": "1561377807",
      "name": "Geladeira Duplex Frost Free Brastemp BRM46MB 385L Branco 220V",
      "store": { "id": "23254", "name": "Americanas", "is_marketplace": false },
      "price": 2419,
      "installment_total": 2687.76,
      "installments": [{ "months": 8, "amount": 335.97, "total": 2687.76 }],
      "has_interest": true,
      "stock": null,
      "condition": "new"
    }
  ],
  "priciest_offer": { "offer_id": "1564569077", "store": { "id": "22905", "name": "Magazine Luiza" }, "price": 3739.34 },
  "variant_filters": [
    { "id": "43", "label": "Voltagem", "values": [
      { "variant_id": "48735", "label": "127V", "selected": false, "count": 3 },
      { "variant_id": "48733", "label": "220V", "selected": false, "count": 3 }
    ] }
  ]
}
```

### Price history and price tip

`POST /api/v1/buscape/price-history` with `{"product_id": "12755140"}` (1 credit):

```json
{
  "product_id": "12755140",
  "period": "days",
  "count": 40,
  "lowest": { "date": "2026-11-22", "price": 4299, "store_id": "1582" },
  "highest": { "date": "2026-10-28", "price": 5057.99, "store_id": "22902" },
  "latest": { "date": "2026-11-27", "price": 4299, "store_id": "1582" },
  "points": [
    { "date": "2026-10-19", "price": 4958.99, "store_id": "22902" },
    { "date": "2026-10-20", "price": 4958.99, "store_id": "22902" }
  ]
}
```

`/product` for the same id carries `price_tip` `{"label": "regular_price", "price": 4537.84, "median_price": 4549, "start": "2026-10-19", "end": "2026-11-27"}` and `expert` with the editors' pros (A18 processor, OLED screen) and cons (60Hz refresh rate, no charger in the box). `/lowest-price` read `price` 4537.84 at store `1582` with `stock` 50 and `updated_at` 2026-11-27T12:40:55Z.

### Freight to a CEP

`POST /api/v1/buscape/shipping` with `{"product_id": "13994006", "cep": "01310-100", "state": "SP", "city": "São Paulo"}` (1 credit): 10 offers estimated, `offers_with_freight` 7.

```json
{
  "position": 3,
  "offer_id": "1561860625",
  "store": { "id": "245", "name": "Webcontinental" },
  "price": 2442.37,
  "freight": [{ "type": "freight_estimate", "price": 409.9, "delivery_days": 6, "text": null }],
  "coupons": []
}
```

Americanas read freight R$ 620,27 in 15 days; Magazine Luiza published no estimate (an empty `freight` list).

### Search, deals, landing, store, categories and suggestions

- `/search` `{"query": "geladeira"}`: `total` 4053, first item Geladeira Brastemp BRM46MB (`type` product, `price` 2308, `store_count` 5, `best_offer` at Magazine Luiza); facets Marca (Electrolux 70, Brastemp 48) and Degelo (Frost Free 298); `category_suggestion` Geladeira (id 8).
- `/deals` `{"category_id": "3"}`: 305 TV deals, first Smart TV Mini LED 55" TCL 4K 55C6K at R$ 2.919,12 with KaBuM! holding the best offer.
- `/deal-landing` `{"slug": "black-friday"}`: title "Black Friday 2026: Economize com cupons até 90% | Buscapé", sections of kind `product_highlight` (Samsung Galaxy S25 5G 256GB at R$ 3.498,30 from 6 stores) and `search_items`.
- `/store` `{"store_id": "21"}`: KaBuM! with `store_ids` grouped under it, `cashback_percent` 0.5, `coupon_count` 100, e.g. code VIRADA10 (10 percent, 2026-11-27T04:09Z to 2026-11-28T04:09Z, status active).
- `/categories` `{"branch": "eletrodomesticos"}`: 18 categories (Adega Climatizada id 380, ...), each `{id, name, slug, type (product_leaf, offer_leaf), url}`.
- `/suggestions` `{"query": "geladeira"}`: 8 suggestions ("geladeira 380", ...) with their category.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def buscape(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/buscape/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Search (1 credit): items of type product are compared across stores
items = buscape("search", {"query": "geladeira", "filters": {"Marca": "Brastemp"}})["data"]["items"]
pid = next(i["product_id"] for i in items if i["type"] == "product")

# 2. Every offer, lowest cash price first (1 credit)
offers = buscape("offers", {"product_id": pid, "sort": "price_asc", "page_size": 20})["data"]
for o in offers["offers"]:
    print(o["store"]["name"], o["price"], o["installment_total"], o["stock"])

# 3. Six months of the day's lowest price (1 credit)
hist = buscape("price-history", {"product_id": pid, "period": "months", "months": 6})["data"]
print(hist["lowest"], hist["latest"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `site`, `country`, `currency` and `language`, and most carry `notes`.

- **search / category / deals** - (`query`; `category` {`id`, `name`, `slug`, `type`, `url`} and `breadcrumb[]` on category), `page`, `page_size`, `sort`, `total`, `total_capped`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `type`, `product_id`, `offer_id`, `name`, `url`, `image`, `category` {`id`, `name`, `slug`}, `price`, `installments` {`months`, `amount`, `total`}, `has_interest`, `store_count`, `stores[]` {`id`, `name`}, `best_offer` {`offer_id`, `store_id`, `store_name`}, `price_drop_percent`, `competitiveness_index`, `rating`, `rating_count`, `review_count`, `marketplace`, `stamps`}, `facets[]` {`key`, `values[]` {`value`, `count`, `selected`}}, `categories[]`, `price_range` {`min`, `max`, `buckets`}, `filters_applied`, and on search `category_suggestion` {`id`, `name`, `applied`}.
- **categories** - `branches[]` {`slug`, `url`}, or with `branch`: `branch` {`id`, `name`, `slug`, `url`}, `count`, `categories[]` {`id`, `name`, `slug`, `type`, `url`}.
- **product** - `product_id`, `name`, `url`, `status`, `rating`, `review_count`, `category`, `breadcrumb`, `category_rank`, `stamps`, `images`, `specs[]` {`group`, `items[]` {`name`, `value`}}, `offer_count`, `store_count`, `best_offer`, `priciest_offer`, `offers[]`, `variant_filters`, `price_history_40_days[]`, `price_tip`, `expert`, `reviews[]` {`rating`, `title`, `text`, `date`, `positive`, `likes`, `dislikes`, `source`}.
- **offers** - `product_id`, `sort`, `variant_id`, `page`, `page_size`, `total`, `store_count`, `total_pages`, `has_more`, `count`, `offers[]` {`position`, `offer_id`, `sku_id`, `name`, `image`, `store` {`id`, `name`, `logo`, `is_marketplace`}, `price`, `installment_total`, `installments[]`, `has_interest`, `price_drop_percent`, `competitiveness_index`, `stock`, `condition`, `cross_border`, `variants[]`}, `best_offer`, `priciest_offer`, `variant_filters[]` {`id`, `label`, `values[]` {`variant_id`, `label`, `selected`, `count`}}.
- **price-history** - `product_id`, `period`, `months`, `count`, `lowest`, `highest`, `latest`, `points[]` {`date`, `price`, `store_id`}.
- **lowest-price** - `product_id`, `offer_id`, `store_id`, `price`, `list_price`, `price_drop_percent`, `stock`, `active`, `updated_at`.
- **deal-landing** - `slug`, `title`, `brand`, `updated_at`, `url`, `sections[]` {`kind` (featured_offers, search_items, product_highlight), `title`, `subtitle`, `from`, `to`, `count`, `items`}.
- **store** - `store` {`id`, `name`, `store_ids`, `logo`, `cashback_percent`, `url`}, `coupon_count`, `coupons[]` {`coupon_id`, `store_id`, `type`, `discount_type` (value, percent), `value`, `code`, `description`, `starts_at`, `expires_at`, `status`, `product_id`, `category_id`, `devices`, `brands`}.
- **suggestions** - `query`, `count`, `suggestions[]` {`query`, `position`, `category` {`id`, `name`}}.
- **shipping** - `product_id`, `cep`, `state`, `city`, `sort`, `count`, `offers_with_freight`, `offers[]` {`position`, `offer_id`, `store` {`id`, `name`}, `price`, `freight[]` {`type`, `price`, `delivery_days`, `text`}, `coupons[]` {`code`, `description`, `starts_at`, `ends_at`}}.

## Guardrails

- Name them "Buscape and Zoom (buscape.com.br, zoom.com.br, Brazil's price comparison sites)" on first mention. Say which `site` a link points to.
- Prices: quote the store, `price` and the `fetched_at` date. A listing `price` is the lowest among the product's stores; say so.
- History: quote it as the day's lowest price across stores, with the store of the point when it matters. It is the history the site shows, not a series Scavio keeps.
- Price tip and editors' notes: quote `price_tip.label` as "Buscape's price tip" and `expert` as "the site editors' pros and cons". Never present them as Scavio's opinion or as buying advice.
- Coupons: quote `code`, `value`, `discount_type` and `expires_at` exactly as given; never compute a price after a coupon.
- Freight: quote each store's estimate as the product page shows it; stores that publish none have an empty `freight` list.
- Reviews: product reviews come from the stores (`source`) with no reviewer names. Quote one as "a store customer review".
- Images and copy: do not republish the sites' product images or copy; link products by `product_id` instead. Store links are not returned.
- Not available: store links, store ratings, reviewer names, account data, alerts, checkout.
- Terms: Scavio does not store Buscape or Zoom data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. The sites' terms of use restrict automated access; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, offers, stores, coupons, dates or history points. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id or url is required"; "url must be a product page: https://www.buscape.com.br/<category>/<product> (items[].url of search) or that path."; "category_id or category is required: a category id (e.g. 8) or slug (e.g. geladeira)."; "Send category_id or category, not both."; "cep must be a Brazilian CEP: 8 digits, e.g. 01310-100 or 01310100."; "state must be the CEP's state as a two-letter UF: ..."; "variant_id must be digits, as variant_filters[].values[].variant_id gives them (e.g. 48733 for 220V)."; "months goes with period months."; "filters.<key> is not a facet: use a key from facets[].key."; "price_min must not be above price_max.".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Buscape product <id>.", "No Buscape offers for product <id>: an unknown product, or no store lists it now.", "No Buscape price history for product <id>: an unknown product, or no price recorded.", "No Buscape price for product <id>.", "No Buscape category <id>. See categories for the branches and their categories.", "No Buscape branch <slug>.", "No Buscape campaign landing <slug>.", "No Buscape store <id>." (Zoom on `site` zoom).
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api).
- `502` and `503` mean the data was temporarily unavailable ("Buscape / Zoom is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.102.0
npm install scavio@0.103.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.buscape.search({ query: "geladeira", filters: { Marca: "Brastemp" } });
const { data: grid } = await scavio.buscape.category({ category: "geladeira", sort: "price_asc" });
const { data: tree } = await scavio.buscape.categories({ branch: "eletrodomesticos" });
const { data: product } = await scavio.buscape.product({ product_id: "12755140" });
const { data: offers } = await scavio.buscape.offers({ product_id: "13994006", sort: "price_asc", variant_id: "48733" });
const { data: history } = await scavio.buscape.priceHistory({ product_id: "12755140", period: "months", months: 6 });
const { data: low } = await scavio.buscape.lowestPrice({ product_id: "12755140" });
const { data: deals } = await scavio.buscape.deals({ category_id: "3" });
const { data: landing } = await scavio.buscape.dealLanding({ slug: "black-friday" });
const { data: store } = await scavio.buscape.store({ store_id: "21" });
const { data: typed } = await scavio.buscape.suggestions({ query: "geladeira" });
const { data: freight } = await scavio.buscape.shipping({ product_id: "13994006", cep: "01310-100", state: "SP", city: "São Paulo" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.buscape.search(...)`, `category`, `categories`, `product`, `offers`, `price_history`, `lowest_price`, `deals`, `deal_landing`, `store`, `suggestions` and `shipping`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 12 endpoints as tools: `search_buscape`, `get_buscape_category`, `get_buscape_categories`, `get_buscape_product`, `get_buscape_offers`, `get_buscape_price_history`, `get_buscape_lowest_price`, `get_buscape_deals`, `get_buscape_deal_landing`, `get_buscape_store`, `get_buscape_suggestions` and `get_buscape_shipping`. Buscape + Zoom is opt-in: add `buscape` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.102.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,buscape"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/buscape-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api), [category](https://scavio.dev/docs/buscape-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api), [categories](https://scavio.dev/docs/buscape-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api), [product](https://scavio.dev/docs/buscape-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api), [offers](https://scavio.dev/docs/buscape-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api), [price history](https://scavio.dev/docs/buscape-price-history?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api), [lowest price](https://scavio.dev/docs/buscape-lowest-price?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api), [deals](https://scavio.dev/docs/buscape-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api), [deal landing](https://scavio.dev/docs/buscape-deal-landing?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api), [store](https://scavio.dev/docs/buscape-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api), [suggestions](https://scavio.dev/docs/buscape-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api) and [shipping](https://scavio.dev/docs/buscape-shipping?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api). The platform page is [scavio.dev/buscape-api](https://scavio.dev/buscape-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=buscape-zoom-api).
