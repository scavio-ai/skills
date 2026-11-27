---
name: terabyte-api
description: Terabyteshop API for Terabyteshop (terabyteshop.com.br, Brazil's PC-parts store; Brazil only, BRL, Portuguese text) - what a graphics card, processor, monitor, SSD or any PC part costs at Terabyteshop today by Pix and by card, how long a Black Friday deal runs and how many units it has left, which coupons are live, what shoppers search for most and what the Full Custom PC builder offers for each part, as terabyteshop.com.br shows it to a visitor who is not signed in (on 2026-11-27 the Gigabyte GS24F14 monitor read R$ 549.99 by Pix, R$ 647.05 on card in 12 interest-free payments of R$ 53.92, against a list price of R$ 752.90, with the BLACK FRIDAY offer ending 2026-11-30 at 10:00 Brasilia time with 6 units left after 2,713 sold; the coupon BLACKDT3 took 5 percent off selected DT3 chairs above R$ 849 with 70 uses left; "placa de video" led the top searches with 60,900 searches) with Pix price, card price, list price, discount, installments, availability, open-box and free-shipping flags, units sold, best-seller rank, rating and the card's coupon; keyword search up to 100 a page, sorted by relevance, price, best sellers, rating or review count (Scavio sorts the returned page, since the site's search ignores sorting); category and brand listings and the deal lists (Black Friday, open box, free shipping), 30 a page in the site's order or by price, filtered by sub-category and spec attributes (model, maker, VRAM, connection) with facet counts; one product with EAN, MPN, every card plan, warranty, the running deal, free-shipping states, specs and the 5 newest reviews; every review, 5 a page (no names); the active coupons by category or code with the products a code covers; the top 48 search terms with search counts; the PC builder's platforms, component groups and options with availability per distribution center (builder prices can differ from the product page). 9 endpoints, 1 credit each. No shipping quote by CEP, stores or stock unit counts.
version: 1.0.0
tags: terabyte, terabyteshop, terabyteshop-com-br, terabyte-api, terabyteshop-api, terabyte-prices, terabyte-precos, terabyte-pix, terabyte-pix-price, terabyte-black-friday, terabyte-ofertas, terabyte-deals, terabyte-open-box, terabyte-frete-gratis, terabyte-coupons, terabyte-cupons, terabyte-trending-searches, terabyte-mais-buscados, terabyte-pc-builder, terabyte-monte-seu-pc, full-custom, terabyte-product, terabyte-reviews, terabyte-avaliacoes, terabyte-search, terabyte-categories, terabyte-brands, pc-parts-prices, pc-hardware-prices, gpu-prices, graphics-card-prices, placa-de-video, processador, monitor-prices, ssd-prices, pc-gamer, hardware-brasil, price-monitoring, price-tracking, product-data, pix, parcelamento, brazil, brazil-ecommerce, brazilian-retail, brl, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/terabyte-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api
---

# Terabyteshop API - PC Parts Pix and Card Prices, Black Friday Deals, Coupons, PC Builder

Read Terabyteshop (terabyteshop.com.br, Brazil's PC-parts store): keyword search, category and brand listings, the deal lists (Black Friday, open box, free shipping), one product in full, its customer reviews, the active coupons, the site's top search terms and the Full Custom PC builder. www.terabyteshop.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in.

**The job this skill is for: what a PC part costs at Terabyteshop today by Pix and by card, how long its deal runs, which coupon applies and what the PC builder offers.** Terabyteshop shows two prices on every product: the Pix price (Pix is Brazil's instant payment; the site's cash price, also for boleto) and the card price, paid in installments. On 2026-11-27 the Gigabyte GS24F14 monitor `41251` read R$ 549.99 by Pix and R$ 647.05 on card (12 interest-free payments of R$ 53.92) against a list price of R$ 752.90, with the BLACK FRIDAY offer ending 2026-11-30 at 10:00 Brasilia time, 2,713 units sold and 6 left ("Quase acabando"), and free shipping to 7 states.

Seven limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Allow time.** Search, product, category, brand and deals usually take 5-30 seconds and can take about 90; reviews, coupons, trending searches and the PC builder usually take 2-6 seconds (in the captures: search 2.7, product 8.1, category 6.7, reviews 9.6 seconds). Allow a client timeout of at least 180 seconds.
- **Search sorting is done by Scavio.** Terabyteshop's search ignores sorting, so a `sort` other than `relevance` orders the returned page after it is fetched: each page is sorted on its own, and the order across pages stays the site's relevance. A note says so on every sorted answer.
- **Listing cards carry no card price.** Category, brand and deal cards carry the Pix price, list price and installment plan; `price` (the card total) is null there and is on `/product`. Search items carry both.
- **Stock is a flag.** `available` true or false, plus the units left on a running deal (`offer.units_left` on `/product`) and `units_sold`. Terabyteshop publishes no stock unit counts.
- **No shipping, no stores.** Terabyteshop quotes shipping by CEP (the Brazilian postal code) in the cart, so it is not returned; `free_shipping` and `free_shipping_states` (the states with free shipping) are. Terabyteshop has no stores.
- **PC builder prices are the builder's own.** They can differ from the product page price of the same part, so quote a builder price as the builder's and a product price from `/product`. Builder availability is per distribution center (SC, ES).

Terabyteshop has no public API for its prices, coupons or PC builder. They are shown on terabyteshop.com.br to any visitor, and this skill reads those public pages with one Scavio key.

See also: KaBuM! `kabum-api` (Brazilian PC and electronics store), Magazine Luiza `magalu-magazine-luiza-api`, Mercado Libre `mercadolibre-product-data`, Buscape + Zoom `buscape-zoom-api` (Brazilian price comparison); outside Brazil: Micro Center `micro-center-api`, Best Buy `best-buy-product-data`, Amazon `amazon-product-data`.

## When to trigger

Use this skill when the user asks to:
- Search Terabyteshop by keyword (in Portuguese as shoppers type it: "rtx 5060", "placa de video", "ssd nvme"), sorted by relevance, Pix price, best sellers, rating or review count
- Browse a Terabyteshop category by its path (`hardware/placas-de-video`, `hardware/processadores`, `monitores`, `perifericos/mouse`), filtered by sub-category and spec attributes (GPU model, maker, VRAM, connection)
- List one brand's products in a category (Logitech mice, Gigabyte graphics cards)
- List the Black Friday deals, open-box products or free-shipping products, with each deal's end
- Read one Terabyteshop product: Pix price, card price, list price, every card plan, warranty, the running deal with units left, free-shipping states, EAN, MPN and specs
- Read a product's customer reviews, newest first
- List the active Terabyteshop coupons, one category's coupons, or one code with the products it covers
- Read the top search terms on Terabyteshop with their search counts and top product
- Walk the Full Custom PC builder: its platforms, the component groups of one platform, and the options of one group with availability per distribution center

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api) - email or Google, no card required.
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
| `POST /api/v1/terabyte/search` | Keywords: up to 100 products per page (24 by default) with total, Pix price, card price, list price, discount, installments, availability, units sold, best-seller rank, rating and the card's coupon; sorted by Scavio on request | 1 |
| `POST /api/v1/terabyte/product` | One product: EAN, MPN, part number, images, Pix and card price, list price, every card plan, condition, warranty, seller, the running deal with units sold and left, free-shipping states, rating, key specs, specs and the 5 newest reviews | 1 |
| `POST /api/v1/terabyte/reviews` | A product's customer reviews, newest first, 5 per page: rating, date, verified-buyer flag, text; with `product_id` alone also the average and the total | 1 |
| `POST /api/v1/terabyte/category` | One category by path: 30 products per page in the site's order or by price, filtered by sub-category and spec attributes, with sub-category, brand and attribute facets and their counts | 1 |
| `POST /api/v1/terabyte/brand` | One brand's products in one category, by brand name or `brand_id`, same listing, sorts and facets | 1 |
| `POST /api/v1/terabyte/deals` | The deal lists: `black_friday` (the promotions page), `open_box` or `free_shipping`, by sub-category or brand, with each deal's end | 1 |
| `POST /api/v1/terabyte/coupons` | The active coupons (all, one category's, or one code with the products it covers): discount, scope, uses left, end date, minimum order | 1 |
| `POST /api/v1/terabyte/trending-searches` | The site's top search terms, up to 48, with each term's search count and the product the site puts at the top | 1 |
| `POST /api/v1/terabyte/pc-builder` | The Full Custom PC builder: platforms, one platform's component groups, or one group's options with price and availability per distribution center | 1 |

Brazil only: there is no `country` parameter. Every answer carries `store` (terabyte), `country` (br), `currency` (BRL) and `language` (pt-BR), and most carry `notes`.

## Prices: Pix price, card price, list price and installments

| Field | Meaning |
|---|---|
| `pix_price` | The Pix (and boleto) price, the site's cash price, in BRL (R$ 549.99 on the monitor below) |
| `price` | The card price, paid in installments (R$ 647.05); null on category, brand and deal cards, where only `/product` and search carry it |
| `list_price` | The regular price the site shows struck through (R$ 752.90) |
| `discount_percent` | The Pix price against the list price, as the site's cards show it (27) |
| `pix_discount_percent` (product, builder) | The Pix price against the card price (15) |
| `installment` | The plan the card shows: `{count, amount, interest_free}` (12 x R$ 53.92, interest-free) |
| `installments` (product) | Every card plan: `{count, amount, discount_percent, interest}`, from 1x R$ 582.34 (10 percent off) to 18x R$ 39.54 with interest |
| `offer` | The running deal: `{campaign, ends_at}` on cards; on `/product` also `units_sold`, `units_left` and `stock_label` |
| `coupon` (listings, product) | The coupon the card shows (`code`, `value`, `discount_type`, `units_left`); fields can be null when the card names none |
| `price_valid_until` (product) | The date the page says the price holds until (2026-11-30) |

- Quote "Monitor Gamer Gigabyte GS24F14: R$ 549.99 by Pix, R$ 647.05 on card (12x R$ 53.92 interest-free), list price R$ 752.90, on terabyteshop.com.br on 2026-11-27", with both prices and the date.
- Coupons are what the coupon pages list; never apply a coupon to a price yourself. Report Terabyteshop's prices and labels and the arithmetic only, and never judge a product as a good deal.

## Workflow

1. **Find products.** `/search` with `query` (`rtx 5060`), or `/category` with `category` (the path of a category link: `hardware/placas-de-video`). Each item's `product_id` (or `url`) is the input of `/product` and `/reviews`.
2. **Narrow a listing.** Read `facets` and send its values back: `subcategory` (`facets.subcategories[].name`, e.g. `Placa de Vídeo`), `filters` (`{key: value or [values]}` from `facets.attributes[].key` and `.values[].value`, e.g. `{"modelo": "RTX 5070"}`), and `brand` / `brand_id` from `facets.brands` on `/brand`. `sort` is `relevance`, `price_asc` or `price_desc` on listings.
3. **Next pages.** Send `page` (listings: 30 a page, `total_pages` reports the last; search: `page_size` up to 100). `has_more` false means the last page.
4. **One product.** `/product` with `product_id` or `url`: both prices, every card plan, the running deal with units left, warranty, specs and the 5 newest reviews. `/reviews` pages through all of them.
5. **Deals and coupons.** `/deals` with `deal` (`black_friday`, `open_box`, `free_shipping`); `/coupons` with no input for all coupons, `category` for one category's, `code` for one coupon and the products it covers.
6. **Build a PC.** `/pc-builder` with no input for the platforms, `platform_id` for its component groups, then `platform_id` + `group_id` for one group's options.
7. **Watching prices:** there is no history. Poll the same searches and products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`)

| Parameter | Description |
|---|---|
| `query` (required) | Keywords, 1-120 characters, in Portuguese as shoppers type them (`rtx 5060`) |
| `page` | Results page, 1-100 |
| `page_size` | Products per page, 1-100 (default 24) |
| `sort` | `relevance` (default, the site's order), `price_asc`, `price_desc` (by Pix price), `best_sellers` (units sold), `top_rated` or `most_reviewed`. Scavio sorts the returned page; the site's search ignores sorting |

A keyword that matches nothing returns `total` 0 and no items (the site answers it with unrelated products, which are dropped). If the regular search answer fails, Terabyteshop's search page is read instead: up to 300 results in one list, `total` and `total_pages` null, slower (about a minute), and a note says so.

### Category (`/category`), brand (`/brand`) and deals (`/deals`)

| Parameter | Description |
|---|---|
| `category` (category and brand, required) | A category path of 1 to 3 levels as the site writes it: `hardware/placas-de-video`, `hardware/processadores`, `monitores`, `perifericos/mouse` |
| `brand` (brand) | A brand name as `facets.brands[].name` lists it (`Logitech`; case and accents ignored). Send `brand` or `brand_id` |
| `brand_id` (brand, deals) | A brand id, `facets.brands[].brand_id` (`39`) |
| `deal` (deals) | `black_friday` (default, the promotions page), `open_box` or `free_shipping` |
| `sort` | `relevance` (default, the site's order), `price_asc` or `price_desc` |
| `page` | 1-400, 30 products each |
| `subcategory` | A sub-category name exactly as `facets.subcategories[].name` lists it (`Placa de Vídeo`) |
| `filters` (category and brand) | Spec filters, at most 5 keys, each a value or a list of up to 10: keys and values exactly as `facets.attributes[].key` and `.values[].value` list them (`{"modelo": "RTX 5070"}`, `{"conexao": "Sem fio"}`). Several values match any of them |

A filter key that is not an attribute of the listing is a `400` that lists the attributes there. Deal lists take no `filters` (use `subcategory` or `brand_id`).

### Product (`/product`) and reviews (`/reviews`)

Send `product_id` (digits, `items[].product_id`, the number after /produto/ in a product link, e.g. `41251`) or `url` (a product link on www.terabyteshop.com.br, `https://www.terabyteshop.com.br/produto/<id>/<name>`). `/reviews` also takes `page`, 1-400, 5 reviews each; sent with `url` it is fastest, sent with `product_id` alone it also returns `average_rating`, `total_reviews` and `total_pages`.

### Coupons (`/coupons`)

| Parameter | Description |
|---|---|
| `code` | One coupon code (`coupons[].code`, e.g. `BLACKDT3`): the coupon and the products it covers |
| `category` | A coupon category slug (`coupon_categories[].slug`: `placa-mae`, `memoria-ram`, `cadeira-gamer`, `refrigeracao`): its coupons |

Send `code` or `category`, not both. Without either, every active coupon.

### Trending searches (`/trending-searches`) and PC builder (`/pc-builder`)

`/trending-searches` takes `limit`, 1-48 (default 48, all the site lists). `/pc-builder` takes `platform_id` (`platforms[].platform_id`, e.g. `18613`) and `group_id` (`groups[].group_id`, e.g. `21065`); `group_id` needs its `platform_id`.

## Examples

### One search item

Request `{"query": "rtx 5060"}` (1 credit): `total` 162, `total_pages` 7, 24 items. One item:

```json
{
  "position": 2,
  "product_id": "38293",
  "name": "Placa de Vídeo MSI NVIDIA GeForce RTX 5060 Shadow 2X OC, 8GB, GDDR7, DLSS, Ray Tracing, 912-V537-038",
  "url": "https://www.terabyteshop.com.br/produto/38293/placa-de-video-msi-nvidia-geforce-rtx-5060-shadow-2x-oc-8gb-gddr7-dlss-ray-tracing-912-v537-038",
  "brand": "MSI",
  "category": "Hardware > Placa de Vídeo > NVIDIA GeForce",
  "gtin": "4711377344234",
  "mpn": "912-V537-038",
  "price": 4117.64,
  "pix_price": 3499.99,
  "list_price": 5521.73,
  "discount_percent": 37,
  "installment": { "count": 18, "amount": 228.76, "interest_free": null },
  "currency": "BRL",
  "available": true,
  "free_shipping": true,
  "on_promotion": true,
  "offer": null,
  "units_sold": 187,
  "best_seller_rank": { "position": 16, "category": null },
  "rating": 4.8,
  "review_count": 39,
  "coupon": null,
  "labels": []
}
```

### One product

Request `{"product_id": "41251"}` (1 credit), abridged:

```json
{
  "product_id": "41251",
  "name": "Monitor Gamer Gigabyte GS24F14, 23.8 Pol, Full HD, IPS, 144Hz, 1ms, 104%sRGB, HDMI/DP",
  "brand": "Gigabyte",
  "gtin": "4719331877224",
  "mpn": "GS24F14",
  "price": 647.05,
  "pix_price": 549.99,
  "list_price": 752.9,
  "discount_percent": 27,
  "pix_discount_percent": 15,
  "installment": { "count": 12, "amount": 53.92, "interest_free": true },
  "available": true,
  "availability": "Pronta entrega",
  "condition": "Novo",
  "warranty_months": 36,
  "sold_by": "TerabyteShop",
  "best_seller_rank": { "position": 8, "category": "Monitores", "category_url": "https://www.terabyteshop.com.br/monitores" },
  "offer": { "campaign": "BLACK FRIDAY", "ends_at": "2026-11-30T10:00:59-03:00", "units_sold": 2713, "units_left": 6, "stock_label": "Quase acabando" },
  "price_valid_until": "2026-11-30",
  "free_shipping": true,
  "free_shipping_states": ["RS", "PR", "SC", "SP", "MG", "RJ", "ES"],
  "rating": 4.7,
  "review_count": 78,
  "return_days": 7,
  "key_specs": [{ "name": "Painel", "value": "IPS" }, { "name": "Taxa de atualização", "value": "144 Hz" }, { "name": "Resolução", "value": "Full HD" }, { "name": "Tamanho", "value": "23,8 polegadas" }]
}
```

The product also carried 8 images, 18 card plans in `installments` (1x R$ 582.34 at 10 percent off to 18x R$ 39.54 with interest), the full `specs` list and the 5 newest `reviews` {`rating`, `date`, `text`}.

### Reviews

`/reviews` `{"product_id": "20782"}` (the Ryzen 5 5500): `average_rating` 5, `total_reviews` 367, `total_pages` 74, 5 reviews:

```json
{ "rating": 5, "date": "2026-11-09", "verified_buyer": true, "text": "Ótimo custo benefício" }
```

### Listings, coupons, trending searches and the PC builder

- `/category` `{"category": "hardware/placas-de-video"}`: `total` 878, 30 pages, first a Galax GeForce RTX 3050 EX 6GB at R$ 1,679.99 by Pix against R$ 2,809.90 (40 percent), BLACK FRIDAY until 2026-11-30, rank 2 in Placa de Vídeo; facets with 29 brands (Asus 149, Gigabyte 118, MSI 84), price range R$ 30.01 to R$ 82,513.37 and attributes such as `fabricante` (NVIDIA 644, AMD 221, Intel 12) and `modelo` (RTX 5060 Ti 61, RTX 5060 43, RTX 5070 42).
- `/brand` `{"category": "perifericos/mouse", "brand": "Logitech"}`: `brand` {`brand_id` 39, `name` Logitech, `count` 91}, 4 pages, first the MX Vertical at R$ 549.99 by Pix against R$ 869.99; attributes `conexao` (Sem fio 66, Com fio 18, Bluetooth 7) and `dpi_max`.
- `/deals` `{}` (Black Friday): `total` 6767, 226 pages, first a Gigabyte B550M AORUS Elite motherboard at R$ 649.99 by Pix against R$ 1,239.99 (48 percent).
- `/coupons` `{}`: 11 coupons in 4 categories (Memória RAM 2, Cadeiras 7, Refrigeração 1, Placas-Mãe 1). One:

```json
{ "code": "BLACKDT3", "discount": "5% OFF", "discount_type": "percent", "discount_value": 5, "scope": "Em Cadeiras DT3 Selecionadas", "units_left": 70, "valid_until": "2026-11-30T10:00:59-03:00", "minimum_order": 849, "free_shipping": false, "product_count": 16 }
```

- `/trending-searches` `{}`: 48 terms, led by placa de video (60,900 searches), monitor (49,651), rtx 5070 (47,046), ssd (46,682) and gabinete (44,210), each with its `top_product` (price, Pix price, availability).
- `/pc-builder` `{"platform_id": "18613", "group_id": "21065"}`: the Processador group's 5 options, among them the Ryzen 5 5500 at R$ 649.99 by Pix (R$ 764.69 on card, 12x R$ 63.72), on offer, assembly available, `availability_by_distribution_center` SC available and ES not. The builder lists 5 platforms; a platform has component groups (processor, motherboard, cooler, memory, graphics card, SSD, power supply, case, assembly, monitor), each with `max_items`, `min_items`, `optional` and `option_count`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def terabyte(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/terabyte/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. RTX 5070 graphics cards, lowest Pix price first (1 credit)
cards = terabyte("category", {"category": "hardware/placas-de-video", "filters": {"modelo": "RTX 5070"}, "sort": "price_asc"})["data"]
for it in cards["items"][:5]:
    print(it["name"], it["pix_price"], it["list_price"], it["discount_percent"], it["available"])

# 2. One product with both prices, every card plan and the running deal (1 credit)
item = terabyte("product", {"product_id": cards["items"][0]["product_id"]})["data"]
print(item["pix_price"], item["price"], item["installment"], item["offer"])

# 3. The live coupons (1 credit)
for c in terabyte("coupons", {})["data"]["coupons"]:
    print(c["code"], c["discount"], c["scope"], c["units_left"], c["valid_until"])

# Terabyteshop prices change during a deal. Store each answer with fetched_at and run
# this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `country`, `currency` and `language`.

- **search** - `query`, `page`, `page_size`, `sort`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `product_id`, `name`, `url`, `image`, `brand`, `category`, `gtin`, `mpn`, `price`, `pix_price`, `list_price`, `discount_percent`, `installment` {`count`, `amount`, `interest_free`}, `currency`, `available`, `open_box`, `free_shipping`, `free_shipping_states`, `on_promotion`, `offer` {`campaign`, `ends_at`}, `units_sold`, `best_seller_rank` {`position`, `category`}, `rating`, `review_count`, `coupon` {`code`, `value`, `discount_type`, `units_left`}, `labels`}, `notes`.
- **category / brand / deals** - `category` (category, brand), `brand` {`brand_id`, `name`, `count`} (brand), `deal` (deals), `url`, `page`, `page_size` (30), `sort`, `total`, `total_pages`, `has_more`, `count`, `items[]` (the item fields above; `price`, `brand`, `category`, `gtin` and `mpn` null on cards), `facets` {`total`, `price_range` {`min`, `max`}, `subcategories[]` {`name`, `count`}, `brands[]` {`brand_id`, `name`, `count`}, `attributes[]` {`key`, `label`, `unit`, `numeric`, `values[]` {`value`, `count`}}, `attribute_category`}, `filters_applied`, `notes`.
- **product** - `product_id`, `requested_id`, `name`, `url`, `brand`, `category`, `gtin`, `mpn`, `part_number`, `images`, `price`, `pix_price`, `list_price`, `discount_percent`, `pix_discount_percent`, `installment`, `installments[]` {`count`, `amount`, `discount_percent`, `interest`}, `available`, `availability`, `condition` (Novo, Open Box), `open_box`, `warranty`, `warranty_months`, `sold_by`, `best_seller_rank` {`position`, `category`, `category_url`}, `offer` {`campaign`, `ends_at`, `units_sold`, `units_left`, `stock_label`}, `price_valid_until`, `coupon`, `free_shipping`, `free_shipping_states`, `rating`, `review_count`, `return_days`, `key_specs[]` {`name`, `value`}, `specs[]` {`name`, `value`}, `reviews[]` {`rating`, `date`, `text`}, `notes`.
- **reviews** - `product_id`, `url`, `page`, `page_size` (5), `average_rating`, `total_reviews`, `total_pages` (with `product_id` alone), `has_more`, `count`, `reviews[]` {`rating`, `date`, `verified_buyer`, `text`}, `notes`.
- **coupons** - `category`, `count`, `coupons[]` {`code`, `discount`, `discount_type` (`percent`, `amount`), `discount_value`, `scope`, `units_left`, `valid_until`, `minimum_order`, `free_shipping`, `conditions`, `product_count`, `url`}, `coupon_categories[]` {`slug`, `name`, `coupon_count`}; with `code`: `code`, `coupon` {... `used_percent`}, `count`, `products[]` {`product_id`, `name`, `url`, `image`, `brand`, `product_type`}, `notes`.
- **trending-searches** - `count`, `terms[]` {`position`, `term`, `search_count`, `top_product` {`product_id`, `name` (cut at 80 characters by the site), `url`, `image`, `brand`, `category`, `price`, `pix_price`, `currency`, `available`}}, `notes`.
- **pc-builder** - without inputs `count`, `platforms[]` {`platform_id`, `name`, `url`}; with `platform_id` `groups[]` {`group_id`, `name`, `optional`, `max_items`, `min_items`, `option_count`, `note`}; with `group_id` `options[]` {`position`, `product_id`, `name`, `url`, `image`, `brand`, `price`, `pix_price`, `pix_discount_percent`, `installment`, `currency`, `on_offer`, `new_release`, `selected_by_default`, `assembly_available`, `available`, `availability_by_distribution_center[]` {`distribution_center`, `available`}}, `notes`.

## Guardrails

- Name it "Terabyteshop (terabyteshop.com.br, Brazil's PC-parts store)" on first mention. Terabyteshop accounts, carts, PC builds and checkout are not read or made.
- Prices: quote `pix_price` and `price` (or the card's `installment`) with `list_price` and the `fetched_at` date, in BRL (R$), and say which is the Pix price. Prices are what a visitor who is not signed in sees.
- Installments and coupons: quote `installment` / `installments` and coupon terms exactly as given. Never compute a plan, apply a coupon or assume it covers a product the coupon page does not list.
- Sorting: a sorted search is sorted by Scavio within the returned page. Never present it as Terabyteshop's own ranking or as the order across every page.
- Stock: say "available" or "not available" and, on a deal, the units left. Never present `units_sold`, `offer.units_left` or a coupon's `units_left` as the store's stock.
- PC builder: builder prices are the builder's own and can differ from the product page; say so when quoting them, and quote `availability_by_distribution_center` per center (SC, ES), never as store stock.
- Shipping: there is no shipping cost. Say `free_shipping` / `free_shipping_states` as given and that the cost depends on the buyer's CEP, quoted in the cart.
- Reviews: no reviewer names or places are returned. Quote a review as "a Terabyteshop customer review" with its rating and date; never try to identify a reviewer.
- Comparing Terabyteshop with KaBuM! or another store: compare the same product (EAN or MPN), the same payment (Pix with Pix, card with card) and the same date. Never call one store cheaper beyond the numbers shown.
- Images and copy: do not republish product photos or the site's descriptions; refer to products by `product_id` and `url` instead.
- Not available: shipping quotes by CEP, stores, stock unit counts, price history (poll and store), account data, cart or checkout. This API cannot buy, save a PC build or apply a coupon.
- Terms: Scavio does not store Terabyteshop data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Terabyteshop's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, products, deals, coupons, ratings or reviews. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id or url is required"; "product_id and url name different products: send one."; "url must be a product link on www.terabyteshop.com.br (https://www.terabyteshop.com.br/produto/<id>/<name>)."; "category must be a category path of 1 to 3 levels as the site writes it ..."; "brand or brand_id is required"; "filters takes at most 5 keys."; "filters: \"<key>\" is not an attribute of this listing. Attributes: ..."; "filters are not offered on deal listings: use subcategory or brand_id."; "Send code or category, not both."; "group_id needs its platform_id (groups come from one platform).".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "No Terabyteshop product <id>.", "No Terabyteshop category <path> (...)", "No <brand> products in <path>. Brands there: ...", "No active Terabyteshop coupon <code>.", "No Terabyteshop coupon category <slug>.", "No Terabyteshop PC builder platform <id> (see platforms[].platform_id).", "No component group <id> on platform <id> (see groups[].group_id).". A search with no matching products is an empty `200` (`total` 0), not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api).
- `502` and `503` mean Terabyteshop data was temporarily unavailable ("Terabyteshop is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.104.0
npm install scavio@0.105.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.terabyte.search({ query: "rtx 5060", sort: "price_asc" });
const { data: item } = await scavio.terabyte.product({ product_id: "41251" });
const { data: reviews } = await scavio.terabyte.reviews({ product_id: "20782", page: 1 });
const { data: gpus } = await scavio.terabyte.category({ category: "hardware/placas-de-video", filters: { modelo: "RTX 5070" } });
const { data: mice } = await scavio.terabyte.brand({ category: "perifericos/mouse", brand: "Logitech" });
const { data: deals } = await scavio.terabyte.deals({ deal: "black_friday", sort: "price_asc" });
const { data: coupons } = await scavio.terabyte.coupons({});
const { data: top } = await scavio.terabyte.trendingSearches({ limit: 10 });
const { data: options } = await scavio.terabyte.pcBuilder({ platform_id: "18613", group_id: "21065" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.terabyte.search(...)`, `product`, `reviews`, `category`, `brand`, `deals`, `coupons`, `trending_searches` and `pc_builder`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 9 endpoints as tools: `search_terabyte`, `get_terabyte_product`, `get_terabyte_reviews`, `get_terabyte_category`, `get_terabyte_brand`, `get_terabyte_deals`, `get_terabyte_coupons`, `get_terabyte_trending_searches` and `get_terabyte_pc_builder`. Terabyteshop is opt-in: add `terabyte` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.104.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,terabyte"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/terabyte-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api), [product](https://scavio.dev/docs/terabyte-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api), [reviews](https://scavio.dev/docs/terabyte-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api), [category](https://scavio.dev/docs/terabyte-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api), [brand](https://scavio.dev/docs/terabyte-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api), [deals](https://scavio.dev/docs/terabyte-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api), [coupons](https://scavio.dev/docs/terabyte-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api), [trending searches](https://scavio.dev/docs/terabyte-trending-searches?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api), [PC builder](https://scavio.dev/docs/terabyte-pc-builder?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api). Platform page: [scavio.dev/terabyte-api](https://scavio.dev/terabyte-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=terabyte-api).
