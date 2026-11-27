# Pichau API - PC Parts Pix and Card Prices, Black Friday Deals, Coupons, PC Benchmarks

Read Pichau (pichau.com.br, Brazil's PC-parts store): keyword search, category, brand and deal listings such as Black Friday and open box, one product with its Pix and card prices and running deal, the live product page with FPS benchmarks and a prebuilt PC's component list, reviews, every card plan, the coupons page, the category menu and the search box's suggestions. www.pichau.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in.

**The job this skill is for: what a PC part costs at Pichau today by Pix and by card, and how long its deal runs.** Every product carries a Pix price (Brazil's instant payment), a card price payable in installments and a struck-through list price; a product in a campaign carries its countdown with units left and sold. On 2026-11-27 the INNO3D GeForce RTX 5060 Twin X2 8GB read R$ 3,159.99 by Pix (15 percent off) and R$ 3,717.64 on card, 12x R$ 309.80 interest-free, against R$ 3,835.28, sold out with 2 Black Friday units left after 117 sold and the deal ending 2026-11-30 17:10. Paid in a single card installment it came to R$ 3,345.88, 10 percent off.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Three prices, as given.** `pix_price` is the Pix price, `price` the card price (payable in `installment.count` installments), `list_price` the regular price shown struck through. `discount_percent` is the Pix price against the list price. `/installments` gives every card plan; Pichau discounts short card plans too.
- **Stock is a status, not a count.** `available` and `stock_status`, plus `only_x_left` when the site shows "only N left" and, on a running deal, `offer.units_left` and `offer.units_sold`. Pichau publishes no stock counts.
- **Two slower endpoints.** `/product-live` (live stock and deal units, benchmarks, a prebuilt PC's components) and `/suggestions` usually take 30-160 seconds. Listings took 5-170 seconds in Black Friday week. Allow a client timeout of at least 240 seconds.
- **A keyword can open a category.** Some keywords are sent by the site to one of its categories (`cadeira gamer` to `cadeiras/gamer`); the answer is then that category's products, with `redirected_to` set.
- **No shipping, stores or history.** Pichau quotes shipping by CEP in the cart, so there is no shipping quote; it has one physical store and no per-store data; there is no PC builder. Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

Pichau publishes no developer API for its catalog, prices or stock. Prices, deals, coupons and reviews are shown on pichau.com.br, and this skill reads those public pages with one Scavio key.

See also: Terabyteshop `terabyte-api` and KaBuM! `kabum-api` (Brazilian PC-parts stores), Mercado Libre `mercadolibre-product-data` (Brazil marketplace), Magazine Luiza `magalu-magazine-luiza-api`, Newegg `newegg-api`, Micro Center `micro-center-api`.

## When to trigger

Use this skill when the user asks to:
- Price a PC part at Pichau: Pix price, card price, list price, discount and installments
- Search pichau.com.br by keyword (in Portuguese as shoppers type: "rtx 5060", "ryzen 7", "ssd 1tb", "cadeira gamer"), in the site's order, by price or by name, filtered by brand, price range, GPU, socket and the listing's other facets
- List a Pichau category (`hardware/placa-de-video`, `monitores`, `perifericos/teclado`) or a brand (`corsair`, `asus`, `redragon`)
- Read the Black Friday campaign, the open-box products or another campaign, with each product's deal end, units left and units sold
- Read one product: EAN, MPN, NCM, card and Pix prices, warranty, distribution center, open-box condition, specs and the running deal
- Read a prebuilt PC's FPS benchmarks per game and its component list with the alternatives offered, or a product's live deal units
- Read a product's reviews (by stars or with photos), with the rating breakdown
- List every card plan for a product, with the discount on short plans
- Read the live coupons and the announced ones
- Read the Pichau category menu or the search box's suggestions for a typed term

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api) - email or Google, no card required.
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
| `POST /api/v1/pichau/search` | Keywords: 36 products per page with total, card price, Pix price, list price, discount, installment, availability, only-N-left, running deal, open-box grade, free-shipping labels, EAN, warranty and rating; facets with counts; `redirected_to` when the site sends the keyword to a category | 1 |
| `POST /api/v1/pichau/category` | A category by path (`hardware/placa-de-video`), same items, sorts and facets, plus the category's product count and breadcrumbs | 1 |
| `POST /api/v1/pichau/brand` | A brand by slug (`corsair`), same items, sorts and facets | 1 |
| `POST /api/v1/pichau/deals` | The Black Friday campaign (default), the open-box products or another campaign by slug, with the campaign's start, end and state and each product's deal countdown | 1 |
| `POST /api/v1/pichau/product` | One product by url_key or link: EAN, MPN, NCM, card, Pix and list prices, installment, availability, running deal, open-box condition, warranty, distribution center, rating and specs | 1 |
| `POST /api/v1/pichau/product-live` | The live product page: stock status, prices and deal units, FPS benchmarks per game (on PCs) and a prebuilt PC's or kit's component list with the alternatives offered | 1 |
| `POST /api/v1/pichau/reviews` | A product's reviews, newest first, 10 per page, by stars or with photos: rating breakdown, title, text, date, verified purchase, media (no names) | 1 |
| `POST /api/v1/pichau/installments` | Every card plan for one product: count, amount, total, the discount on short plans, interest-free flag and the site's label | 1 |
| `POST /api/v1/pichau/coupons` | The coupons page: code, percent off, applies to a product or a category, valid until, and the announced upcoming coupons | 1 |
| `POST /api/v1/pichau/categories` | The category menu with paths, levels and children | 1 |
| `POST /api/v1/pichau/suggestions` | What the search box suggests for a typed term: terms with product counts, categories and up to 10 products with a price | 1 |

Brazil only: there is no `country` parameter. Every answer carries `store` (pichau), `country` (br), `currency` (BRL) and `language` (pt-BR), and most carry `notes`.

## Prices: Pix price, card price, list price and card plans

| Field | Meaning |
|---|---|
| `pix_price` | The Pix price, in BRL (R$ 3,159.99 on the RTX 5060 below) |
| `pix_discount_percent` | The Pix discount against the card price, as the site gives it (15) |
| `price` | The card price (R$ 3,717.64), payable in `installment` |
| `installment` | `{count, amount}`: the longest plan the page shows (12x R$ 309.80) |
| `list_price` | The regular price shown struck through (R$ 3,835.28) |
| `discount_percent` | The Pix price against the list price (18) |
| `offer` | The running deal: `{campaign, campaign_path, ends_at (Brasilia time), promo_price, discount_percent, units_left, units_sold}`; null outside a campaign |
| `installments[]` (installments) | Every card plan: `{count, amount, total, discount_percent, discount_value, interest_free, label}` (1x R$ 3,345.88, 10 percent off) |

- Quote "Placa de Video INNO3D GeForce RTX 5060 Twin X2 8GB: R$ 3,159.99 by Pix, R$ 3,717.64 on card (12x R$ 309.80), list R$ 3,835.28, on pichau.com.br on 2026-11-27", with the date.
- Quote `pix_price`, `installment`, `installments` and `offer` exactly as given; never compute a Pix discount or a card plan yourself, and never judge a price as a good deal. `offer.promo_price` can differ from `price` on the live page; quote each with its field.

## Workflow

1. **Find products.** `/search` with `query` (`rtx 5060`), `/category` with `category` (a `categories[].path` from `/categories`), `/brand` with `brand` (`items[].brand_slug`), or `/deals` (`black_friday` by default, `open_box`, or `campaign`).
2. **Narrow.** Read `facets` and send values back in `filters` as `{key: value}` with `facets[].key` and `facets[].values[].value` (`{"marcas": "34"}`, a price range `{"price": "0_1000"}`, `rgpu`, `socket`), at most 5 keys, one value per key; plus `sort`.
3. **Next pages.** Send `page` 2, 3, ... with the same input. `has_more` false means the last page.
4. **One product.** `/product` with `url_key` (`items[].url_key`) or `url`. A prebuilt PC or kit (`product_type` bundle): `/product-live` for its components and FPS benchmarks.
5. **Card plans.** `/installments` with `product_id` and `price` (the card price, fast), or with `url_key` (the product page is read first).
6. **Reviews.** `/reviews` with `product_id` (`items[].product_id`), optionally `rating` or `with_media`.
7. **Watching prices:** there is no history. Poll the same listings and products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`), brand (`/brand`) and deals (`/deals`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords in Portuguese as shoppers type them, 1-120 characters |
| `category` (category, required) | A category path as the site writes it (`categories[].path`), e.g. `hardware/placa-de-video`, `monitores`, `perifericos/teclado`, `cadeiras/gamer` |
| `brand` (brand, required) | A brand slug (`items[].brand_slug`), e.g. `corsair`, `asus`, `redragon` |
| `deal` (deals) | `black_friday` (default, the Black Friday campaign page) or `open_box` (open-box products) |
| `campaign` (deals) | Another campaign by slug (`items[].offer.campaign_path` without `promocao/`), instead of `deal` |
| `sort` | `relevance` (default, the site's own order), `price_asc`, `price_desc`, `name_asc`, `name_desc` |
| `filters` | `{key: value}` with `facets[].key` and `facets[].values[].value`, at most 5 keys, one value per key |
| `page` | 1-200 (36 per page); `total_pages` gives the last one |

### Product (`/product`) and live product (`/product-live`)

Send `url_key` (`items[].url_key`, the part after `www.pichau.com.br/` in a product link) or `url` (a product link on www.pichau.com.br).

### Reviews (`/reviews`)

| Parameter | Description |
|---|---|
| `product_id` (required) | The Pichau product id (`items[].product_id`, `31201`) |
| `page` | 1-500 (10 per page, newest first) |
| `rating` | Only reviews with this many stars, 1-5 |
| `with_media` | `true` for reviews with photos or videos |

### Installments (`/installments`), coupons (`/coupons`), categories (`/categories`) and suggestions (`/suggestions`)

`/installments` takes `product_id` with `price` (the card price in BRL, `items[].price`, e.g. 3717.64), or `url_key` / `url`; not both. `/coupons` takes an empty body `{}`. `/categories` takes `all` (`true` for every menu node, campaign and partner pages included; default `false`). `/suggestions` takes `query` (what a shopper has typed, 2-60 characters).

## Examples

### One search item

Request `{"query": "rtx 5060"}` (1 credit): `total` 1385, `total_pages` 39, 36 items, `redirected_to` null, facets such as `price`, `category_uid`, `rgpu` (Placa de Vídeo, 44 values) and `rtbprocessador` (101 values). One item:

```json
{
  "position": 1,
  "product_id": 57776,
  "sku": "NE75060019P1-GB2063B-NAC",
  "url_key": "placa-de-video-gainward-geforce-rtx-5060-ghost-8gb-gddr7-128-bit-ne75060019p1-gb2063b-nac",
  "name": "Placa de Video Gainward GeForce RTX 5060 Ghost, 8GB, GDDR7, 128-bit, NE75060019P1-GB2063B-NAC",
  "brand": "Gainward",
  "brand_slug": "gainward",
  "category": "NVIDIA GeForce",
  "category_path": "hardware/placa-de-video/nvidia",
  "price": 3741.17,
  "pix_price": 3179.99,
  "list_price": 4117.64,
  "discount_percent": 23,
  "pix_discount_percent": 15,
  "installment": { "count": 12, "amount": 311.76 },
  "available": true,
  "stock_status": "IN_STOCK",
  "only_x_left": null,
  "on_promotion": false,
  "offer": null,
  "open_box": false,
  "free_shipping": true,
  "labels": ["Frete Grátis: Sul e Sudeste"],
  "ean": "4710562245387",
  "warranty": "12 Meses",
  "product_type": "simple",
  "rating": 0,
  "review_count": 0
}
```

The item also carried `url` and `image`. A Black Friday item from `/deals` `{}` (the AMD Ryzen 7 9800X3D) read `pix_price` 2149.99, `price` 2529.4, `list_price` 4352.93 and `offer` {"campaign": "BlackFriday", "ends_at": "2026-11-30 17:10:00", "promo_price": 2529.4, "discount_percent": 41.89, "units_left": 85, "units_sold": 1330}.

### One product

Request `{"url_key": "placa-de-video-inno3d-geforce-rtx-5060-twin-x2-8gb-gddr7-128-bit-n50602-08d7-195071n-nac"}` (1 credit), abridged:

```json
{
  "product_id": 61004,
  "sku": "N50602-08D7-195071N-NAC",
  "mpn": "N50602-08D7-195071N-NAC",
  "ean": "8886307701169",
  "ncm": "85423190",
  "name": "Placa de Video INNO3D GeForce RTX 5060 Twin X2, 8GB, GDDR7, 128-bit, N50602-08D7-195071N-NAC",
  "brand": "INNO3D",
  "price": 3717.64,
  "pix_price": 3159.99,
  "list_price": 3835.28,
  "discount_percent": 18,
  "pix_discount_percent": 15,
  "installment": { "count": 12, "amount": 309.8 },
  "available": false,
  "stock_status": "OUT_OF_STOCK",
  "on_promotion": true,
  "offer": { "campaign": "BlackFriday", "campaign_path": "promocao/blackfriday", "ends_at": "2026-11-30 17:10:00", "promo_price": 3717.64, "discount_percent": 3.07, "units_left": 2, "units_sold": 117 },
  "free_shipping": true,
  "labels": ["Frete Grátis: Sul e Sudeste"],
  "warranty": "12 Meses",
  "distribution_center": "santa-catarina",
  "club_exclusive": false,
  "product_type": "simple"
}
```

The product also carried 3 `categories` (Hardware > Placa de Vídeo > NVIDIA GeForce), 2 images and `specs` (Núcleos CUDA: 3840, Interface: PCI Express Gen 5, Tamanho de Memória: 8GB GDDR7, ...).

### Live product page, card plans and reviews

- `/product-live` `{"url_key": "pc-gamer-pichau-isis-vi-amd-ryzen-5-5500-geforce-rtx-5060-8gb-16gb-ddr4-ssd-m-2-480gb-57268"}` (a prebuilt PC, `product_type` bundle): `pix_price` 5605.24, `price` 6594.4 (12x R$ 549.53), `list_price` 11089.81, `offer` with `promo_price` 6470.58, 48 units left after 102 sold; `benchmark` {`overall_score` 12306, `cpu_score` 7802, `gpu_score` 13702} with 14 games, e.g. `{"title": "Cyberpunk 2077", "full_hd_fps": 120, "ultra_1080p_fps": 90, "quad_hd_fps": 65, "medium_4k_fps": 40, "ultra_4k_fps": 30}`; 22 `components` groups (Processador, Cooler, Placa Mãe with 5 choices, Placa de Vídeo with 9 choices, Fonte, Gabinete, ...), each with the default part and the alternatives offered.
- `/installments` `{"product_id": 61004, "price": 3717.64}`: 12 plans, 1x R$ 3,345.88 (10 percent off, "1x de R$3.345,88 (com 10% de desconto)"), 2x and 3x 5 percent off, 4x to 6x 3 percent off, 7x to 12x interest-free at R$ 3,717.64 (12x R$ 309.80).
- `/reviews` `{"product_id": 31201}`: `average_rating` 5, `total_reviews` 57 (all 5 stars), 6 pages, e.g. `{"title": "Ótimo produto", "text": "Ótimo processador de entrada. Está me atendendo super bem!", "rating": 5, "date": "2026-11-14 23:27:05", "verified_purchase": true, "media": []}`.

### Coupons, categories and suggestions

- `/coupons` `{}`: 18 active coupons, 0 upcoming, e.g. `BLACKAMD5` (5 percent, a product), `ESPORTES15` (15 percent, a product), `PRUMO5OFF` (5 percent, a category), `valid_until` null when the site shows no end.
- `/categories` `{}`: 18 departments, 119 nodes (Hardware, Periféricos, Computadores, Monitores, Cadeiras e Mesas Gamer e Escritório, Notebooks e Portáteis, Openbox, ...).
- `/suggestions` `{"query": "rtx 5070"}`: the term `rtx 5070` and 10 products, first the INNO3D GeForce RTX 5070 X3 OC 12GB at R$ 5,999.99.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def pichau(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/pichau/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. RTX 5060 cards, lowest price first (1 credit)
hits = pichau("search", {"query": "rtx 5060", "sort": "price_asc"})["data"]
for it in hits["items"][:5]:
    print(it["name"], it["pix_price"], it["price"], it["list_price"], it["available"])

# 2. One product with its running deal (1 credit)
item = pichau("product", {"url_key": hits["items"][0]["url_key"]})["data"]
print(item["pix_price"], item["price"], item["offer"])

# 3. Every card plan for that price (1 credit)
plans = pichau("installments", {"product_id": item["product_id"], "price": item["price"]})["data"]
for p in plans["installments"]:
    print(p["count"], p["amount"], p["total"], p["discount_percent"])

# Pichau prices and deal units change during the day. Store each answer with
# fetched_at and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `country`, `currency` and `language`.

- **search / category / brand / deals** - `query` and `redirected_to` {`category`, `url`} (search), `category` and `category_info` {`category_id`, `name`, `path`, `product_count`, `breadcrumbs`} (category), `brand` and `brand_info` {`brand_id`, `name`, `slug`} (brand), `deal`, `campaign` and `campaign_info` {`campaign_id`, `slug`, `title`, `state`, `starts_at`, `ends_at`} (deals), `url`, `page`, `page_size` (36), `sort`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `product_id`, `sku`, `url_key`, `url`, `name`, `brand`, `brand_slug`, `category`, `category_path`, `image`, `price`, `pix_price`, `list_price`, `discount_percent`, `pix_discount_percent`, `installment` {`count`, `amount`}, `currency`, `available`, `stock_status`, `only_x_left`, `on_promotion`, `offer`, `open_box`, `open_box_state`, `pre_order`, `free_shipping`, `labels`, `ean`, `warranty`, `product_type` (simple, bundle), `rating` (0-5), `rating_percent` (0-100), `review_count`}, `facets[]` {`key`, `label`, `values[]` {`value`, `label`, `count`}}, `filters_applied`, `notes`.
- **product** - the item fields above plus `requested_url_key`, `mpn`, `ncm`, `brand_id`, `categories[]` {`name`, `path`}, `product_set`, `images`, `open_box_condition`, `distribution_center`, `club_exclusive`, `specs[]` {`name`, `value`}, `notes`.
- **product-live** - `requested_url_key`, `product_id`, `url_key`, `url`, `sku`, `name`, `product_type`, `available`, `stock_status`, `only_x_left`, `price`, `pix_price`, `list_price`, `discount_percent`, `pix_discount_percent`, `installment`, `pre_order`, `on_promotion`, `offer`, `benchmark` {`overall_score`, `cpu_score`, `gpu_score`, `games[]` {`title`, `full_hd_fps`, `ultra_1080p_fps`, `quad_hd_fps`, `medium_4k_fps`, `ultra_4k_fps`}}, `components[]` {`group`, `required`, `selected`, `choice_count`, `choices[]` {`product_id`, `sku`, `name`, `url_key`, `url`, `quantity`, `is_default`, `available`, `image`}}, `rating`, `review_count`, `notes`.
- **reviews** - `product_id`, `page`, `page_size` (10), `rating_filter`, `with_media`, `average_rating`, `rating_percent`, `total_reviews`, `breakdown` {`5`, `4`, `3`, `2`, `1`}, `total_pages`, `has_more`, `count`, `reviews[]` {`title`, `text`, `rating`, `date`, `verified_purchase`, `media[]` {`type`, `url`}}, `notes`.
- **installments** - `product_id`, `price`, `product` (when asked by url_key), `count`, `installments[]` {`count`, `amount`, `total`, `discount_percent`, `discount_value`, `interest_free`, `label`}, `notes`.
- **coupons** - `url`, `count`, `coupons[]` {`code`, `percent`, `kind`, `applies_to` (product, category), `valid_until`, `status`, `image`}, `upcoming_count`, `upcoming[]`, `notes`.
- **categories** - `count`, `departments`, `categories[]` {`category_id`, `name`, `path`, `level`, `children[]`}, `notes`.
- **suggestions** - `query`, `term_count`, `terms[]` {`term`, `count`}, `categories[]` {`name`, `path`, `url`}, `count`, `products[]` {`name`, `url_key`, `url`, `image`, `price`, `available`, `pre_order`}, `notes`.

## Guardrails

- Name it "Pichau (pichau.com.br, Brazil's PC-parts store)" on first mention. Pichau accounts, carts and checkout are not read or made.
- Prices: quote `pix_price`, `price` (card) and `list_price` together with the `fetched_at` date, in BRL (R$), and say which is which. Never present the Pix price as the card price.
- Card plans and deals: quote `installment`, `installments` and `offer` exactly as given. Never compute a card plan, a discount or a deal end yourself; `ends_at` is Brasilia time.
- Stock: `available`, `stock_status` and `only_x_left` are what the site shows; `offer.units_left` counts the deal's units, not the store's stock. Never present any of them as a stock count.
- Benchmarks: `benchmark` is the FPS the site shows for a prebuilt PC; an FPS of 0 is the site's "under 20 FPS". Quote it as the site's figure, not as a measured result.
- Coupons: the coupons page does not say which products a code covers beyond `applies_to`; never promise a coupon applies to a given product.
- Reviews: no reviewer names are returned. Quote a review as "a Pichau buyer review" with its rating and date.
- Comparing Pichau with Terabyteshop, KaBuM! or another store: compare the same product (EAN or MPN), payment method and date. Never call one store cheaper beyond the numbers shown.
- Images and copy: refer to products by `url_key` and `product_id`; do not republish Pichau's product photos or page copy, and keep any use descriptive.
- Not available: shipping quotes by CEP, stores, stock unit counts, the PC builder (Monte seu PC), price history (poll and store), account data, cart or checkout. This API cannot buy, review or apply a coupon.
- Terms: Scavio does not store Pichau data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Pichau's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, deal units, benchmarks, coupons or reviews. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "url_key or url is required"; "url_key and url name different products: send one."; "url_key, url or product_id (with price) is required"; "Send url_key (or url), or product_id with price: not both."; "price is required with product_id: the product's card price in BRL (items[].price), e.g. 3717.64."; "Send deal or campaign, not both."; "filters takes at most 5 keys."; "filters.<key> takes one value (facets[].values[].value)."; "query must be at least 2 characters (the search box suggests from 2)."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "No Pichau product <url_key>.", "No Pichau category <path> (send a category path such as hardware/placa-de-video; see categories).", "No Pichau brand <slug> (send a brand slug such as corsair; items[].brand_slug).", "Pichau has no <deal> listing right now.", "<url_key> is not a Pichau product page (a listing: use category).", "No installment plans for Pichau product <id> at R$ <price>.". A search with no products is a `200` with `total` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api).
- `502` and `503` mean Pichau data was temporarily unavailable ("Pichau is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- Listings took 5-170 seconds in Black Friday week (in the captures 6-14 seconds); the product page and coupons usually take 5-60 seconds; `/product-live` and `/suggestions` usually 30-160 seconds; reviews and card plans by `product_id` 2-8 seconds. Allow a client timeout of at least 240 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.105.0
npm install scavio@0.106.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.pichau.search({ query: "rtx 5060", sort: "price_asc" });
const { data: gpus } = await scavio.pichau.category({ category: "hardware/placa-de-video", filters: { marcas: "34" } });
const { data: corsair } = await scavio.pichau.brand({ brand: "corsair" });
const { data: blackFriday } = await scavio.pichau.deals({ deal: "black_friday" });
const { data: item } = await scavio.pichau.product({ url_key: "placa-de-video-inno3d-geforce-rtx-5060-twin-x2-8gb-gddr7-128-bit-n50602-08d7-195071n-nac" });
const { data: live } = await scavio.pichau.productLive({ url_key: "pc-gamer-pichau-isis-vi-amd-ryzen-5-5500-geforce-rtx-5060-8gb-16gb-ddr4-ssd-m-2-480gb-57268" });
const { data: reviews } = await scavio.pichau.reviews({ product_id: "31201", rating: 5 });
const { data: plans } = await scavio.pichau.installments({ product_id: "61004", price: 3717.64 });
const { data: coupons } = await scavio.pichau.coupons({});
const { data: menu } = await scavio.pichau.categories({});
const { data: typed } = await scavio.pichau.suggestions({ query: "rtx 5070" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.pichau.search(...)`, `category`, `brand`, `deals`, `product`, `product_live`, `reviews`, `installments`, `coupons`, `categories` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `search_pichau`, `get_pichau_category`, `get_pichau_brand`, `get_pichau_deals`, `get_pichau_product`, `get_pichau_product_live`, `get_pichau_reviews`, `get_pichau_installments`, `get_pichau_coupons`, `get_pichau_categories` and `get_pichau_suggestions`. Pichau is opt-in: add `pichau` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.105.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,pichau"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/pichau-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api), [category](https://scavio.dev/docs/pichau-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api), [brand](https://scavio.dev/docs/pichau-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api), [deals](https://scavio.dev/docs/pichau-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api), [product](https://scavio.dev/docs/pichau-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api), [product live](https://scavio.dev/docs/pichau-product-live?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api), [reviews](https://scavio.dev/docs/pichau-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api), [installments](https://scavio.dev/docs/pichau-installments?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api), [coupons](https://scavio.dev/docs/pichau-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api), [categories](https://scavio.dev/docs/pichau-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api), [suggestions](https://scavio.dev/docs/pichau-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api). Platform page: [scavio.dev/pichau-api](https://scavio.dev/pichau-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=pichau-api).
