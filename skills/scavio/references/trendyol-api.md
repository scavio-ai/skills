# Trendyol API - Product Prices, Seller Offers, Reviews, Rankings

Read Trendyol marketplace data from trendyol.com and its international storefronts: keyword search, category and brand grids with the site's own sorts and filters, one product in full with the buy-box seller and every other seller's offer, reviews with the star histogram, answered seller questions, a seller's store profile and catalog, flash deals and Super Firsatlar, the collectable coupons on a seller's listing, a category's top-100 lists, search-box suggestions and the delivery estimate of every listing. All 12 endpoints return structured JSON and cost 1 credit per call.

**The job this skill is for: Trendyol seller prices.** Trendyol runs one catalog: many sellers list the same product, one of them holds the buy box (the default offer on the product page) and the rest are listed under "Other Sellers of the Product". `/product` returns both: `buy_box` {`seller` {`id`, `name`, `score` out of 10, `badges`}, `price`, `original_price`, `discount_percent`, `free_shipping`, `rush_delivery_hours`, `has_coupon`} and `other_sellers[]` with the same price fields, the seller's score and the lowest-price badge each offer carries. Trendyol's developer FAQ says the buy box is chosen "with the determined algorithm metrics", not by price alone, and that other sellers are listed "according to their Buybox scores": so the buy box is not necessarily the cheapest offer, and `other_sellers[]` is not sorted by price. Sort it yourself.

**Lowest-price badge: a day count, not a price.** Trendyol tags some offers "lowest price of the last N days" (`Son 10 Günün En Düşük Fiyatı` on tr). `lowest_price_badge` is {`days`, `text`}: 10, 14, 30 or 90 days on the Turkish storefront, 7, 14 or 30 on the international ones (where `text` is `null`). Trendyol publishes no numeric 30-day lowest price and no price history, so neither is returned: never present a badge as a measured price, and to see whether a price moved, read the same product on a schedule and store each reading with its time, market and seller. Black Friday 2026 is Friday, November 27; press calendars put Trendyol's Efsane Günler at November 26 to December 2, 2026.

**International storefronts have their own price lists.** The same `content_id` serves every storefront, but each storefront is priced on its own, not as a currency conversion of the Turkish price, and its items are sold by Trendyol itself or by other sellers (check `buy_box` and `other_sellers`). Measured on 2 products on 2026-11-15, from the captures:

| Product | Storefront (`country`, `language`) | Seller | `price` | `original_price` | Currency |
|---|---|---|---|---|---|
| 737572719 chiffon maxi dress | `de`, `de` | Trendyol | 37.25 | 41.39 | EUR |
| 737572719 chiffon maxi dress | `fr`, `en` | Trendyol | 112.99 | - | EUR |
| 1090399394 mini dress | `tr`, `tr` (rankings capture) | World Fashion Trends | 440.1 | 489 | TRY |
| 1090399394 mini dress | `bg`, `bg` | World Fashion Trends | 7.61 | 19.91 | EUR |
| 1090399394 mini dress | `gr`, `el` | World Fashion Trends | 7.6 | 19.9 | EUR |
| 1090399394 mini dress | `ro`, `ro` | World Fashion Trends | 31.73 | 126.81 | RON |

Two euro storefronts priced the same dress 37.25 and 112.99 EUR the same day. Read each storefront you report; never derive one market's price from another's.

Trendyol has no public catalog, price or review API. The Trendyol Partner API is for sellers in the Trendyol Partner Program and their integrators: it manages the seller's own products, prices, stock and orders, with credentials from the seller panel.

See also: for Allegro (Poland, Czechia, Slovakia, Hungary) every seller's price use `allegro-api`; for AliExpress use `aliexpress-product-data`; for Amazon's Turkish and Gulf marketplaces use `amazon-product-data` (`tr`, `ae`, `sa`); for the cross-merchant view of one product use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Compare every seller's price for one Trendyol product: who holds the buy box, at what price, and what the other sellers charge, with their seller scores
- Check a Trendyol discount: the crossed-out price, the percent off and the lowest-price badge ("lowest price of the last 10 / 14 / 30 days")
- Track Trendyol prices through Black Friday and Efsane Günler (poll and store price, original price, seller and badge per run)
- Compare one product's price across Trendyol storefronts (Turkey, the EU, the Balkans, Ukraine, Moldova, the Gulf, Azerbaijan)
- Search Trendyol by keyword, sorted by price, newest, best seller, most favourited or most rated, filtered by price, brand, seller, rating, discount, free shipping, official seller or coupon
- Browse a Trendyol category or brand, or read a category's best sellers, most favourited, most rated or most viewed top 100
- Read Trendyol reviews with the star histogram, what reviews talk about (topics) and Trendyol's own review summary
- Read the answered seller questions on a product
- Read a Trendyol seller's store: score, followers, product count, shipping and response times, and its catalog
- List today's Trendyol flash deals or Super Firsatlar, or the coupons a seller offers on a product
- Get Trendyol search suggestions for a partial query
- Estimate delivery dates for a product from each seller, to an Istanbul district or any Turkish city and district id

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits: 50 calls, since every endpoint here costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures calls took 0.4 to 6 seconds. One endpoint can make up to 3 upstream reads (still 1 credit), and a failed attempt is retried once, so a slow call can take a minute or more. Set a client timeout of at least 180 seconds and do not fire many calls at once (a busy moment answers `503` with `Retry-After`).

| Endpoint | Markets | Credits | What it returns |
|---|---|---|---|
| `POST /api/v1/trendyol/search` | all 35 | 1 | 36 items per page for a keyword, with total, sorts, filters and (with `include_facets`) facets |
| `POST /api/v1/trendyol/product` | all 35 | 1 | One product by `content_id` or `url`: prices, lowest-price badge, stock, variants, attributes, rating, `buy_box`, `other_sellers[]`, promotions, returnable, installments, VAT and (with `include_description`) the description |
| `POST /api/v1/trendyol/category` | all 35 | 1 | One category's grid by `category_id` or `url`, with the search sorts and filters |
| `POST /api/v1/trendyol/brand` | all 35 | 1 | One brand's grid by `brand_id` or `url`, with the search sorts and filters |
| `POST /api/v1/trendyol/reviews` | all 35 | 1 | A product's rating, rating and review counts, star histogram, topics, sizes bought, Trendyol's review summary and reviews, up to 50 per page |
| `POST /api/v1/trendyol/questions` | all 35 | 1 | A product's answered seller questions with the seller's answer, up to 20 per page |
| `POST /api/v1/trendyol/seller` | all 35 | 1 | A seller's store profile by `seller_id` or `url` and, with `include_products`, the seller's catalog as a grid |
| `POST /api/v1/trendyol/deals` | `tr` | 1 | Flash deals (the active slot or a chosen one, with the slot list) or Super Firsatlar, as a grid |
| `POST /api/v1/trendyol/coupons` | `tr` | 1 | The collectable coupons on one product's listing: the buy box's, or another seller's with `seller_id` |
| `POST /api/v1/trendyol/rankings` | 20 (not the English-language EU storefronts) | 1 | A category's top 100 (best seller, most favourited, most rated or top viewed), 20 per page |
| `POST /api/v1/trendyol/suggestions` | all 35 | 1 | The search-box suggestions for a partial query: keywords, categories, brands and stores |
| `POST /api/v1/trendyol/delivery` | all 35 | 1 | Delivery dates for one product variant from every listing; `city_id` / `district_id` on `tr` only |

## Markets

Every endpoint takes `country` (lowercase, default `tr`) and `language` (default the market's first). Titles, categories, reviews and labels come back in that language and prices in the market's currency, never converted; every `data` echoes `country`, `language` and `currency`. Quote names and labels as returned; translate them for the user only in your own words around the data.

| `country` | Languages | Currency |
|---|---|---|
| `tr` Turkey | `tr`, `en`, `ar` | TRY |
| `de` Germany, `at` Austria | `de` | EUR |
| `fr` France, `be` Belgium, `hr` Croatia, `dk` Denmark, `ee` Estonia, `fi` Finland, `it` Italy, `lv` Latvia, `lt` Lithuania, `nl` Netherlands, `pt` Portugal, `si` Slovenia, `es` Spain, `se` Sweden, `lu` Luxembourg | `en` | EUR |
| `bg` Bulgaria | `bg`, `en` | EUR |
| `gr` Greece | `el`, `en` | EUR |
| `sk` Slovakia | `sk`, `en` | EUR |
| `cz` Czechia | `cs`, `en` | CZK |
| `hu` Hungary | `hu`, `en` | HUF |
| `pl` Poland | `pl`, `en` | PLN |
| `ro` Romania | `ro`, `en` | RON |
| `rs` Serbia | `sr` (Latin), `en` | RSD |
| `ua` Ukraine | `uk`, `en` | UAH |
| `md` Moldova | `ro`, `en` | MDL |
| `ae` United Arab Emirates | `en`, `ar` | AED |
| `sa` Saudi Arabia | `ar`, `en` | SAR |
| `qa` Qatar, `kw` Kuwait, `om` Oman, `bh` Bahrain | `ar`, `en` | QAR, KWD, OMR, BHD |
| `az` Azerbaijan | `tr` | AZN |

- Search, product, category, brand, reviews, questions, seller, suggestions and delivery: all 35 markets.
- Rankings: 20 markets. The 15 English-language EU storefronts (`fr`, `be`, `hr`, `dk`, `ee`, `fi`, `it`, `lv`, `lt`, `nl`, `pt`, `si`, `es`, `se`, `lu`) have no ranking lists and answer `400`.
- Deals and coupons: `tr` only (the international storefronts run no flash or super-discount pages and answered no coupons). Delivery `city_id` / `district_id`: `tr` only.
- A market outside an endpoint's list, or a `language` the market does not serve, answers `400` before anything is charged. `ge`, `kz`, `kg` and `iq` are served by the Turkish storefront rather than a local one, and Trendyol does not sell to `ie`, `mt`, `gb`, `uk`, `ru`, `us`, `ca`, `jo` or `lb`: all answer `400`.
- International storefronts list a part of the Turkish catalog: a product not sold on a storefront answers `404` (charged). Reviews on an international storefront are the ones written in its language.

## Workflow

1. **Find products:** `/search` with `query` in the market's language (`telefon`, `elbise` on `tr`; `kleid` on `de`). Read `items[].content_id` for `/product`, `/reviews`, `/questions`, `/coupons` and `/delivery`. Drop `sponsored: true` items before ranking or counting.
2. **Seller prices for one product:** `/product` with `content_id` (the number after `-p-` in a product link) or `url`. Compare `buy_box.price` with every `other_sellers[].price`; `other_seller_count` is how many other offers there are. Keep `seller.id`, `seller.name`, `seller.score`, `price`, `original_price`, `currency` and `lowest_price_badge` per offer.
3. **A seller:** `/seller` with a `buy_box.seller.id` or `other_sellers[].seller.id` as `seller_id`; add `include_products: true` (and `query`, `sort`, filters) for its catalog. On a grid, `seller_id` narrows results to that seller.
4. **Coupons:** `/coupons` with `content_id` reads the buy box's listing; add `seller_id` from `other_sellers[].seller.id` for another seller's. Coupons belong to each seller's listing, so the buy box often has none while another seller has some.
5. **Browse:** `/category` with `category_id` (the same id on every market: `103498` phones, `56` dresses; `category.tree[].id` on a product) or a `-x-c<id>` link; `/brand` with `brand_id` (`items[].brand.id`) or a `-x-b<id>` link. Send `include_facets: true` once to read the filter groups, then pass `facets[].param` / `options[].value` through `filters`.
6. **Rankings:** `/rankings` with `category_id` and `ranking` (`best_seller`, `most_favourited`, `most_rated`, `top_viewed`), `page` 1 to 5.
7. **Deals (`tr`):** `/deals` with `type` `flash` (the active slot by default; `slots[].tag` picks another) or `super_discounts`.
8. **Reviews and questions:** `/reviews` (`sort`, `rating`, `with_media`, `page_size` up to 50) and `/questions` (`page_size` up to 20) with the same `content_id`.
9. **Delivery:** `/delivery` with `content_id`; on `tr` add `city_id` and `district_id` (Istanbul `133`, Sisli `54`). `item_number` picks a variant.
10. **Price monitoring:** poll `/product` (every seller) or the grids (36 items per call) on a schedule. Store `content_id`, `country`, `language`, the time, seller, `price`, `original_price`, `discount_percent`, `currency` and `lowest_price_badge` per run. There is no price history endpoint.

## Parameters

### Shared by search, category, brand, deals and the seller catalog

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `tr` | See Markets |
| `language` | string | the market's first | One of the market's languages |
| `page` | integer | 1 | 1-based, 36 items per page, 1 to 138 (page 139 and up answers `400`). A page past the last returns no items and a note |
| `sort` | string | `recommended` | `recommended`, `price_asc`, `price_desc`, `newest`, `best_seller`, `most_favourited` or `most_rated` |
| `price_min` / `price_max` | number | none | Price range in the market's currency |
| `brand_id` | id or list | none | 1 to 10 brand ids (`items[].brand.id`, `794` Samsung) |
| `category_id` | id or list | none | 1 to 10 category ids |
| `seller_id` | id | none | One seller's items (`items[].seller.id`) |
| `min_rating` | number | none | `1`, `2`, `3`, `4` or `4.5`: that rating and up |
| `free_shipping`, `fast_delivery`, `flash_sale`, `has_coupon` | boolean | none | Only items with free shipping, rush delivery, a flash sale or a collectable coupon |
| `min_discount` | integer | none | 1 to 90: at least that percent off |
| `lowest_price_days` | integer | none | `7`, `10`, `14`, `30` or `90`: only items carrying that lowest-price badge |
| `seller_type` | string | none | `official` (the brand's official seller), `authorized` or `successful` |
| `filters` | object | none | Any other facet, keyed by `facets[].param` with `facets[].options[].value` values: `{"attr": ["348\|1"]}` is a color, `{"wg": "1"}` a gender |
| `include_facets` | boolean | false | Also return `facets` (still 1 credit) |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords in the market's language (1-200 chars) |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `content_id` | id | one of | `items[].content_id`, the number after `-p-` in a product link: `975557855` |
| `url` | string | one of | A product link on trendyol.com, trendyol.ae or trendyol.sa. A language-only path (`/en/...`) is shared by several storefronts: send `country` with it |
| `include_description` | boolean | false | Also return `description` and `description_html` (still 1 credit) |

### Category (`/category`) and brand (`/brand`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` / `brand_id` | id | one of | `103498` phones, `56` dresses; `794` Samsung |
| `url` | string | one of | A category link (`<name>-x-c<id>`) or brand link (`<brand>-x-b<id>`) |

Plus the shared parameters (other than the endpoint's own id).

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `content_id` / `url` | | one of | The product |
| `sort` | string | `recommended` | `recommended`, `newest`, `oldest`, `rating_desc` or `rating_asc` |
| `rating` | integer | none | Only reviews with this many stars, 1 to 5 |
| `with_media` | boolean | false | Only reviews with photos |
| `page` / `page_size` | integer | 1 / 20 | Page 1 to 500; 1 to 50 reviews per page |

### Questions (`/questions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `content_id` / `url` | | one of | The product |
| `page` / `page_size` | integer | 1 / 20 | Page 1 to 500; 1 to 20 questions per page |

### Seller (`/seller`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `seller_id` | id | one of | `buy_box.seller.id`, `other_sellers[].seller.id` or `items[].seller.id`: `4473` |
| `url` | string | one of | A store link (`/magaza/<name>-m-<id>`, or `/store/<name>-m-<id>` on international storefronts) |
| `include_products` | boolean | false | Also return the seller's products as a grid (still 1 credit) |
| `query` | string | none | Search within the seller's products (with `include_products`) |

Plus the shared parameters for the catalog. `page`, `sort` or `query` without `include_products` answers `400`.

### Deals (`/deals`, `tr` only)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `flash` | `flash` (flash deals) or `super_discounts` (Super Firsatlar: campaign items at a 10, 14 or 30-day low and at least 30% off) |
| `slot` | string | the active slot | A flash slot tag from `slots[].tag` of a previous answer (tags are dated: `fs_15_11_2026_21_24`). `flash` only |

Plus the shared parameters.

### Coupons (`/coupons`, `tr` only)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `content_id` / `url` | | one of | The product |
| `seller_id` | id | the buy box | Another seller's listing (`other_sellers[].seller.id`). A seller that does not sell the product answers `404` |

### Rankings (`/rankings`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | id | required | `56` dresses, `103498` phones, `1156` lipsticks |
| `ranking` | string | `best_seller` | `best_seller`, `most_favourited`, `most_rated` or `top_viewed` |
| `page` | integer | 1 | 1 to 5, 20 per page (the top 100) |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars) |

### Delivery (`/delivery`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `content_id` / `url` | | one of | The product |
| `item_number` | id | the buy box's | The variant (`variants[].item_number`) |
| `listing_id` | string | the buy box's | 32 hex characters (`buy_box.listing_id`). With `item_number` the product is not read first |
| `city_id` / `district_id` | id | none | `tr` only: a Turkish city id and a district of it (Istanbul `133`, Sisli `54`). `district_id` needs `city_id` |

All endpoints also take `country` and `language`.

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/trendyol/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "telefon"}'
```

Captured `data` (Turkey, 2026-11-15; 1 of 36 items shown, `images` trimmed to 1):

```json
{
  "query": "telefon",
  "items": [
    {
      "position": 1,
      "content_id": 975557855,
      "group_id": 741886069,
      "listing_id": "ff1d23f6969474c32de9c4412c73db12",
      "item_number": 1378939445,
      "name": "Galaxy A17 4/128 GB Siyah Cep Telefonu",
      "brand": {"id": 794, "name": "Samsung"},
      "category": {"name": "Android Cep Telefonu"},
      "url": "https://www.trendyol.com/samsung/galaxy-a17-4-128-gb-siyah-cep-telefonu-p-975557855?boutiqueId=61&merchantId=807735",
      "image": "https://cdn.dsmcdn.com/mnresize/400/-/ty1000391/product/media/images/prod/PIM/20260425/10/35fee09a-a27a-4568-9b53-da4a7a1815c6/1_org_zoom.jpg",
      "images": ["https://cdn.dsmcdn.com/mnresize/400/-/ty1000391/product/media/images/prod/PIM/20260425/10/35fee09a-a27a-4568-9b53-da4a7a1815c6/1_org_zoom.jpg"],
      "price": 14149,
      "original_price": null,
      "discount_percent": null,
      "rrp": null,
      "plus_price": null,
      "currency": "TRY",
      "lowest_price_badge": null,
      "badges": ["free_shipping", "rush_delivery", "next_day_delivery", "best_seller", "fast_seller"],
      "best_seller_rank": 1,
      "labels": ["Hızlı Satıcı", "Kargo Bedava"],
      "promotions": [],
      "rating": 4.47,
      "review_count": 310,
      "favourites": "21K",
      "orders": "200+",
      "seller": {"id": 807735},
      "color": "Siyah",
      "variant": "Tek Ebat",
      "sponsored": false
    }
  ],
  "count": 27,
  "sponsored_count": 9,
  "total": 100000,
  "total_capped": true,
  "page": 1,
  "page_size": 36,
  "total_pages": 138,
  "sort": "recommended",
  "requested_filters": {},
  "notes": ["sponsored items (sponsored true) are ads placed among the results and can repeat on every page; they are not counted in count.", "total is capped at 100000 by the site (it shows 100.000+); the site lists at most 138 pages of 36."],
  "country": "tr",
  "language": "tr",
  "currency": "TRY"
}
```

`count` is the organic items on the page (27) and `sponsored_count` the ads (9): sponsored items sit inside `items[]` with `sponsored: true` and repeat on every page. A sponsored item and a discounted item with a lowest-price badge from the same page:

```json
{"position": 4, "content_id": 889950721, "name": "Galaxy S25 Ultra 512 GB Titanyum Siyah (Samsung Türkiye Garantili)", "price": 72999, "currency": "TRY", "seller": {"id": 968}, "sponsored": true}
{"position": 10, "content_id": 1198082362, "name": "iPhone 18 Pro Max 512GB Burgundy", "brand": {"id": 101470, "name": "Apple"}, "price": 159999, "original_price": 166999, "discount_percent": 4, "currency": "TRY", "lowest_price_badge": {"days": 10, "text": "Son 10 Günün En Düşük Fiyatı"}, "badges": ["next_day_delivery", "best_seller", "fast_seller", "official_seller", "lowest_price"], "labels": ["Hızlı Satıcı"], "favourites": "18K", "orders": "100+", "seller": {"id": 968}, "sponsored": false}
```

(Other fields omitted.) `favourites` and `orders` are the site's rounded text; `/product` has the numeric `favourite_count`. `total` stopped at 100000 (`total_capped: true`).

### Product (buy box and other sellers)

```bash
curl -X POST https://api.scavio.dev/api/v1/trendyol/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content_id": "975557855"}'
```

Captured `data` (Turkey, 2026-11-15; 2 of 41 attributes, 1 of 4 images and 3 of 15 other sellers shown):

```json
{
  "content_id": 975557855,
  "product_group_id": 741886069,
  "product_code": "sma175fzkbtur",
  "name": "Galaxy A17 4/128 GB Siyah Cep Telefonu",
  "brand": {"id": 794, "name": "Samsung", "url": "https://www.trendyol.com/samsung-x-b794"},
  "category": {
    "id": 164461,
    "name": "Android Cep Telefonu",
    "path": "Elektronik/Telefon/Akıllı Cep Telefonu/Android Cep Telefonu",
    "tree": [
      {"id": 104024, "name": "Elektronik", "level": 1},
      {"id": 104025, "name": "Telefon", "level": 2},
      {"id": 103498, "name": "Cep Telefonu", "level": 3},
      {"id": 164461, "name": "Android Cep Telefonu", "level": 4}
    ]
  },
  "url": "https://www.trendyol.com/samsung/galaxy-a17-4-128-gb-siyah-cep-telefonu-p-975557855",
  "price": 14149,
  "original_price": null,
  "discount_percent": null,
  "rrp": null,
  "currency": "TRY",
  "lowest_price_badge": null,
  "in_stock": true,
  "running_out": true,
  "max_per_order": 1,
  "color": "Siyah",
  "options": [
    {"name": "Internal Memory", "value": "128 GB"}
  ],
  "variants": [
    {
      "attribute": null,
      "value": null,
      "item_number": 1378939445,
      "in_stock": true,
      "price": 14149,
      "barcode": "8806097657514",
      "selected": true
    }
  ],
  "attributes": [
    {"name": "Ön Kamera Çözünürlüğü", "value": "10 - 20 MP", "starred": true},
    {"name": "Dahili Hafıza", "value": "128 GB", "starred": true}
  ],
  "images": ["https://cdn.dsmcdn.com/ty1000391/product/media/images/prod/PIM/20260425/10/35fee09a-a27a-4568-9b53-da4a7a1815c6/1_org_zoom.jpg"],
  "rating": 4.47,
  "rating_count": 310,
  "review_count": 133,
  "favourite_count": 20635,
  "category_rankings": [
    {"ranking": "bestSeller", "rank": 1}
  ],
  "buy_box": {
    "seller": {
      "id": 807735,
      "name": "Kapdiyo",
      "score": 9.2,
      "badges": ["fast_seller"],
      "city": "Ankara",
      "country": "TÜRKİYE",
      "cash_on_delivery": true,
      "corporate_invoice": true
    },
    "listing_id": "ff1d23f6969474c32de9c4412c73db12",
    "item_number": 1378939445,
    "price": 14149,
    "original_price": null,
    "discount_percent": null,
    "rrp": null,
    "currency": "TRY",
    "free_shipping": true,
    "rush_delivery_hours": 24,
    "flash_sale": false,
    "has_coupon": false
  },
  "other_sellers": [
    {
      "seller": {
        "id": 1176505,
        "name": "İzi Teknoloji",
        "score": 9.6,
        "badges": []
      },
      "listing_id": "3528c6fef9f70c185b4f41bf41758f2a",
      "item_number": 1378939445,
      "price": 14449,
      "original_price": 14999,
      "discount_percent": 4,
      "rrp": null,
      "currency": "TRY",
      "free_shipping": true,
      "rush_delivery": true,
      "lowest_price_badge": {"days": 10, "text": "Son 10 Günün En Düşük Fiyatı"},
      "promotions": ["350 TL ve Üzeri Kargo Bedava (Satıcı Karşılar)"]
    },
    {
      "seller": {
        "id": 628292,
        "name": "TEKYILDIZ",
        "score": 9.3,
        "badges": ["fast_seller"]
      },
      "listing_id": "95f0fd870ef6211a9aa05048e2212e6d",
      "item_number": 1378939445,
      "price": 14450,
      "original_price": null,
      "discount_percent": null,
      "rrp": null,
      "currency": "TRY",
      "free_shipping": true,
      "rush_delivery": true,
      "lowest_price_badge": null,
      "promotions": ["350 TL ve Üzeri Kargo Bedava (Satıcı Karşılar)"]
    },
    {
      "seller": {
        "id": 139518,
        "name": "SELAM BİLİŞİM",
        "score": 9.2,
        "badges": []
      },
      "listing_id": "1b8e7657ab811eae859ea9cc824017d8",
      "item_number": 1378939445,
      "price": 14500,
      "original_price": null,
      "discount_percent": null,
      "rrp": null,
      "currency": "TRY",
      "free_shipping": true,
      "rush_delivery": true,
      "lowest_price_badge": null,
      "promotions": ["350 TL ve Üzeri Kargo Bedava (Satıcı Karşılar)"]
    }
  ],
  "other_seller_count": 15,
  "promotions": [
    {
      "id": 27402394,
      "name": "350 TL ve Üzeri Kargo Bedava (Satıcı Karşılar)",
      "short_name": "Kargo Bedava",
      "type": "Cargo",
      "ends_at": null
    }
  ],
  "returnable": true,
  "max_installments": 1,
  "vat_percent": 20,
  "has_description": true,
  "notes": ["price is what one unit costs at checkout (basket discounts applied); original_price is the higher price it is shown against; each international storefront has its own price list, not a currency conversion; items there are sold by Trendyol itself or by other sellers (see buy_box and other_sellers).", "lowest_price_badge is the site's own badge (lowest price of the last N days): it gives the day count only; Trendyol publishes no numeric 30-day lowest price and no price history.", "other_sellers are the other offers on this product (the buy box is the site's default seller). Reviews, questions, coupons and delivery dates are separate calls."],
  "country": "tr",
  "language": "tr"
}
```

Every offer in that capture, as returned (`other_sellers[]` in the site's order, not sorted by price):

| Seller | `seller.id` | Score | Badges | `price` (TRY) | `original_price` | Lowest-price badge |
|---|---|---|---|---|---|---|
| **Kapdiyo** (buy box) | 807735 | 9.2 | fast_seller | 14149 | - | - |
| İzi Teknoloji | 1176505 | 9.6 | - | 14449 | 14999 | 10 days |
| TEKYILDIZ | 628292 | 9.3 | fast_seller | 14450 | - | - |
| SELAM BİLİŞİM | 139518 | 9.2 | - | 14500 | - | - |
| Koycebine | 105150 | 9.4 | - | 14499 | - | - |
| GÜZEL TEKNOLOJİ | 472582 | 9.7 | - | 14699 | 14749 | - |
| TekCep | 116313 | 9.5 | fast_seller | 14699 | - | - |
| İLETKOM TEKNOLOJİ | 984973 | 9 | - | 14690 | - | - |
| mühendis06 cep elektronik | 1109039 | 9.2 | - | 14849 | - | - |
| TEKNOLOJİ MOBİL STORE | 738552 | 9.5 | - | 14899 | 15049 | 14 days |
| YİĞİTGSM | 474308 | 9.6 | - | 14950 | - | - |
| Referans Bilişim | 522362 | 8.8 | - | 14989 | - | - |
| BAŞARAN İLETİŞİM | 185559 | 9.3 | - | 15999 | - | - |
| Uğurlu Elektronik Shop | 149156 | 9 | - | 16799 | - | - |
| ACAR ELEKTRİKLİ EV ALETLERİ | 1312443 | 9.5 | - | 17000 | - | - |
| Semercioğlu Teknoloji | 1068117 | 8.6 | - | 20000 | - | - |

Here the buy box (Kapdiyo, score 9.2) was also the lowest price, but nine other sellers scored higher; on another product in build testing (Romania) the buy box was 43.22 RON against another offer at 85.49 RON. Never assume either way: compare the prices.

### Category and brand

```bash
curl -X POST https://api.scavio.dev/api/v1/trendyol/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category_id": "103498"}'
```

Captured `data` (Turkey, 2026-11-15; `items` omitted, same item shape as search):

```json
{
  "category": {"id": 103498, "name": "Cep Telefonu", "url": "https://www.trendyol.com/cep-telefonu-x-c103498"},
  "count": 24,
  "sponsored_count": 12,
  "total": 16834,
  "total_capped": false,
  "page": 1,
  "page_size": 36,
  "total_pages": 138,
  "sort": "recommended",
  "requested_filters": {},
  "notes": ["sponsored items (sponsored true) are ads placed among the results and can repeat on every page; they are not counted in count."],
  "country": "tr",
  "language": "tr",
  "currency": "TRY"
}
```

`/brand` with `{"brand_id": "794"}` answered the same grid with `brand` in place of `category`:

```json
{
  "brand": {"id": 794, "name": "Samsung", "url": "https://www.trendyol.com/samsung-x-b794"},
  "count": 27,
  "sponsored_count": 9,
  "total": 9323,
  "total_capped": false,
  "page": 1,
  "page_size": 36,
  "total_pages": 138,
  "sort": "recommended",
  "requested_filters": {},
  "notes": ["sponsored items (sponsored true) are ads placed among the results and can repeat on every page; they are not counted in count."],
  "country": "tr",
  "language": "tr",
  "currency": "TRY"
}
```

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/trendyol/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content_id": "975557855"}'
```

Captured `data` (Turkey, 2026-11-15; 2 of 10 topics and 1 of 20 reviews shown, summary trimmed):

```json
{
  "content_id": 975557855,
  "rating": 4.5,
  "rating_count": 310,
  "review_count": 132,
  "photo_review_count": 23,
  "rating_histogram": {"1": 24, "2": 7, "3": 13, "4": 21, "5": 245},
  "topics": [
    {"name": "Teslimat Süresi", "count": 27, "positive": 23, "negative": 4, "positive_percent": 85},
    {"name": "Paketleme", "count": 18, "positive": 18, "negative": 0, "positive_percent": 100}
  ],
  "sizes": [],
  "review_summary": {
    "text": "• Birçok kullanıcı, telefonun fiyat-performans dengesini oldukça başarılı bulduğunu ifade ediyor. ...",
    "source": "Trendyol's own summary of the reviews, as the product page shows it"
  },
  "reviews": [
    {
      "id": 660607645,
      "rating": 5,
      "text": "Muhteşemdi güvenerek alabilirsin kargoda dahil sorunsuz geldi",
      "date": "2026-08-28T14:55:57.783Z",
      "updated_at": "2026-08-28T14:57:05.895Z",
      "likes": 0,
      "author": "H** K**",
      "verified_buyer": true,
      "elite": false,
      "influencer": false,
      "seller": {"id": 968, "name": "Trendyol"},
      "size": null,
      "fit": null,
      "variant": null,
      "language": "tr",
      "photos": [
        {
          "url": "https://cdn.dsmcdn.com/mnresize/-/820/prod-product-review-media_1777680012294/img/2019922/2027898/2047838/975557855/122907886-1787929023785.jpeg",
          "thumbnail": "https://cdn.dsmcdn.com/mnresize/300/300/prod-product-review-media_1777680012294/img/2019922/2027898/2047838/975557855/122907886-1787929023785.jpeg",
          "type": "IMAGE"
        }
      ]
    }
  ],
  "count": 20,
  "page": 1,
  "page_size": 20,
  "total_pages": 7,
  "sort": "recommended",
  "rating_filter": null,
  "with_media": false,
  "notes": ["author is the display name as Trendyol shows it (already masked); reviewer height and weight are not returned."],
  "country": "tr",
  "language": "tr",
  "currency": "TRY"
}
```

`rating_count` (310) counts star ratings and `review_count` (132) written reviews; a grid item's `review_count` is the rating count. `author` is the masked display name the site shows. `review_summary` is Trendyol's own summary, not the reviews: label it as such when you quote it.

### Questions

```bash
curl -X POST https://api.scavio.dev/api/v1/trendyol/questions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content_id": "975557855"}'
```

Captured `data` (Turkey, 2026-11-15; 2 of 9 topics and 1 of 20 questions shown):

```json
{
  "content_id": 975557855,
  "total": 111,
  "total_asked": 234,
  "topics": [
    {"name": "Uyumluluk", "count": 14},
    {"name": "Garanti Kapsamı", "count": 12}
  ],
  "questions": [
    {
      "id": 466430145,
      "text": "kaç yıl garantili",
      "original_text": null,
      "date": "2026-11-14T17:40:09.822Z",
      "verified_buyer": false,
      "answer": {
        "text": "2 yıl Samsung Türkiye garantili efendim",
        "original_text": null,
        "answered_in": "1 dakika içinde cevaplandı.",
        "seller": {"id": 807735, "name": "Kapdiyo"}
      }
    }
  ],
  "count": 20,
  "page": 1,
  "page_size": 20,
  "total_pages": 6,
  "notes": ["Only answered questions are listed (as on the site); askers are not named.", "Questions and answers asked in another language are shown translated by Trendyol; original_text is what was written."],
  "country": "tr",
  "language": "tr",
  "currency": "TRY"
}
```

### Seller

```bash
curl -X POST https://api.scavio.dev/api/v1/trendyol/seller \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"seller_id": "4473"}'
```

Captured `data` (Turkey, 2026-11-15; 3 of 7 metrics shown):

```json
{
  "seller": {
    "id": 4473,
    "name": "Flormar",
    "score": 9.3,
    "score_scale": 10,
    "product_count": 843,
    "product_count_capped": false,
    "follower_count": 4740163,
    "followers_text": "4,7M",
    "follower_coupon": {"discount": 50, "discount_type": "AMOUNT", "min_basket": 800},
    "badges": [],
    "ranking": "Kozmetik Kategorisinde En trend Mağaza",
    "city": "İstanbul",
    "on_trendyol_for": "8 Yıl",
    "average_shipping_time": "< 12 Saat",
    "question_response_time": "45-60 Dk",
    "average_product_rating": 4.4,
    "average_seller_rating": null,
    "corporate_invoice": "Uygun",
    "metrics": [
      {"id": "activationDate", "title": "Trendyol'daki Süresi", "value": "8 Yıl"},
      {"id": "location", "title": "Konum", "value": "İstanbul"},
      {"id": "corporateInvoice", "title": "Kurumsal Fatura", "value": "Uygun"}
    ],
    "logo": "https://cdn.dsmcdn.com/seller-store/uploads/4473/fba801e1-c8b6-4ac6-83a3-e835458e2383.jpg",
    "store_url": "https://www.trendyol.com/magaza/flormar-m-4473"
  },
  "notes": ["The seller's legal disclosure (registered e-mail, tax number, address, legal name) is not returned."],
  "country": "tr",
  "language": "tr",
  "currency": "TRY"
}
```

Text fields such as `on_trendyol_for`, `average_shipping_time` and `corporate_invoice` are the site's wording in the request language. `score` is out of `score_scale` (10).

### Deals (`tr`)

```bash
curl -X POST https://api.scavio.dev/api/v1/trendyol/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (flash deals, 2026-11-15; 1 of 36 items shown):

```json
{
  "type": "flash",
  "slot": "fs_15_11_2026_21_24,fs_15_11_2026_0_24",
  "slots": [
    {
      "tag": "fs_15_11_2026_21_24,fs_15_11_2026_0_24",
      "status": "active",
      "date": "2026-11-15",
      "start": "21:00",
      "end": "24:00"
    },
    {"tag": "fs_15_11_2026_21_24", "status": "upcoming", "date": "2026-11-15", "start": "21:00", "end": "24:00"}
  ],
  "items": [
    {
      "position": 5,
      "content_id": 962572327,
      "group_id": 731085870,
      "listing_id": "24015e0c647e6b8755f26e3259de271f",
      "item_number": 1362287176,
      "name": "Papatya Suyu Saç Açıcı ve Parlaklık Veren Tonik %100 Doğal ve Saf 100 ml",
      "brand": {"id": null, "name": "Rivance"},
      "category": {"name": "Saç Toniği"},
      "url": "https://www.trendyol.com/rivance/papatya-suyu-sac-acici-ve-parlaklik-veren-tonik-100-dogal-ve-saf-100-ml-p-962572327?boutiqueId=61&merchantId=781333",
      "image": "https://cdn.dsmcdn.com/mnresize/400/-/ty1717/prod/QC_PREP/20250730/11/760655b3-239a-3dfe-965e-d870d3e48c05/1_org_zoom.jpg",
      "images": ["https://cdn.dsmcdn.com/mnresize/400/-/ty1717/prod/QC_PREP/20250730/11/760655b3-239a-3dfe-965e-d870d3e48c05/1_org_zoom.jpg"],
      "price": 157.56,
      "original_price": 162.28,
      "discount_percent": 3,
      "rrp": null,
      "plus_price": null,
      "currency": "TRY",
      "lowest_price_badge": {"days": 30, "text": "Son 30 Günün En Düşük Fiyatı"},
      "badges": ["rush_delivery", "next_day_delivery", "flash_sale", "fast_seller", "lowest_price"],
      "best_seller_rank": null,
      "labels": ["Hızlı Satıcı", "2. Ürün %10"],
      "promotions": ["Kod: RIVANCE100 - 600 TL'ye 100 TL İndirim", "2. Ürüne %10 İndirim"],
      "rating": 4.17,
      "review_count": 757,
      "favourites": "89K",
      "orders": "100+",
      "seller": {"id": 781333},
      "color": null,
      "variant": "Tek Ebat",
      "sponsored": false
    }
  ],
  "count": 24,
  "sponsored_count": 12,
  "total": 96430,
  "total_capped": false,
  "page": 1,
  "page_size": 36,
  "total_pages": 138,
  "sort": "recommended",
  "requested_filters": {},
  "notes": ["Flash slot tags are dated (fs_<day>_<month>_<year>_<start>_<end>): send one from slots[].tag; the active slot is the default.", "sponsored items (sponsored true) are ads placed among the results and can repeat on every page; they are not counted in count."],
  "country": "tr",
  "language": "tr",
  "currency": "TRY"
}
```

An upcoming slot lists no items until it opens.

### Coupons (`tr`)

```bash
curl -X POST https://api.scavio.dev/api/v1/trendyol/coupons \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content_id": "1164743007"}'
```

Captured `data` (2026-11-15):

```json
{
  "content_id": 1164743007,
  "product": {
    "name": "Spiface Charm Küpe Kulaklık",
    "seller": {"id": 1246625, "name": "Teknolara"},
    "price": 902.09,
    "currency": "TRY"
  },
  "coupons": [
    {
      "id": "Master:dceb0781-f444-42d4-acf6-da769989f7c7",
      "discount": 75,
      "discount_type": "amount",
      "discount_amount": 75,
      "discount_percent": null,
      "max_discount": null,
      "min_basket": 700,
      "currency": "TRY",
      "valid_until": "2026-12-03T23:59:59",
      "issued_by": "Seller Center",
      "seller_id": 1246625,
      "link": "https://www.trendyol.com/sr?mid=1246625",
      "mega_coupon": false,
      "plus_members_only": false,
      "messages": [],
      "collectable": true
    }
  ],
  "count": 1,
  "notes": ["Coupons are collected on the site and applied at checkout when the basket reaches min_basket; valid_until is Turkey time (Europe/Istanbul)."],
  "country": "tr",
  "language": "tr",
  "currency": "TRY"
}
```

In build testing product 780343279's buy box had no coupons while another seller (`seller_id` 1188867) had 2: check `other_sellers[]` before concluding a product has none.

### Rankings

```bash
curl -X POST https://api.scavio.dev/api/v1/trendyol/rankings \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category_id": "56"}'
```

Captured `data` (Turkey, dresses, 2026-11-15; 1 of 20 items shown):

```json
{
  "ranking": "best_seller",
  "category": {"id": 56, "name": "Elbise"},
  "items": [
    {
      "rank": 1,
      "content_id": 1090399394,
      "listing_id": "d3d913cdbd96c79034a63e72b80f495e",
      "name": "Siyah Kadın Dik Yaka Toka Detaylı Kuşaklı Toparlayıcı Kalıp Mini Elbise",
      "brand": {"id": 166030, "name": "World Fashion Trends"},
      "url": "https://www.trendyol.com/world-fashion-trends/siyah-kadin-dik-yaka-toka-detayli-kusakli-toparlayici-kalip-mini-elbise-p-1090399394",
      "image": "https://cdn.dsmcdn.com/ty2012/prod/QC_ENRICHMENT/20261109/09/86f6fca7-760f-3f9a-9c42-e65aac007386/1_org_zoom.jpg",
      "images": ["https://cdn.dsmcdn.com/ty2012/prod/QC_ENRICHMENT/20261109/09/86f6fca7-760f-3f9a-9c42-e65aac007386/1_org_zoom.jpg"],
      "price": 440.1,
      "original_price": 489,
      "discount_percent": 10,
      "rrp": null,
      "currency": "TRY",
      "lowest_price_badge": null,
      "badges": ["free_shipping"],
      "promotions": ["Sepette %10 İndirim", "350 TL ve Üzeri Kargo Bedava (Satıcı Karşılar)"],
      "rating": 4.36,
      "review_count": 1401,
      "in_stock": true,
      "running_out": false,
      "seller": {"id": 868610}
    }
  ],
  "count": 20,
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5,
  "notes": ["Trendyol ranks the top 100 of a category (5 pages of 20)."],
  "country": "tr",
  "language": "tr",
  "currency": "TRY"
}
```

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/trendyol/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "iph"}'
```

Captured `data` (Turkey, 2026-11-15; 3 of 11 suggestions shown):

```json
{
  "query": "iph",
  "suggestions": [
    {
      "text": "iphone 15",
      "type": "keyword",
      "site_type": null,
      "url": "https://www.trendyol.com/sr?q=iphone%2015&qt=iphone%2015&st=iphone%2015&os=1&sk=1",
      "category_ids": null,
      "seller_id": null,
      "brand_id": null,
      "image": null
    },
    {
      "text": "Akıllı Cep Telefonları",
      "type": "category",
      "site_type": "Kampanya",
      "url": "https://www.trendyol.com/sr?wc=109461,164461,164462&os=1&sk=1&sk=1",
      "category_ids": [109461, 164461, 164462],
      "seller_id": null,
      "brand_id": null,
      "image": null
    },
    {
      "text": "iphonoloji",
      "type": "store",
      "site_type": "Mağaza",
      "url": "https://www.trendyol.com/magaza/magaza-m-118106?sk=1",
      "category_ids": null,
      "seller_id": 118106,
      "brand_id": null,
      "image": "https://cdn.dsmcdn.com/seller-store/uploads/118106/logo.jpeg"
    }
  ],
  "count": 11,
  "country": "tr",
  "language": "tr",
  "currency": "TRY"
}
```

A `store` suggestion's `seller_id` works on `/seller`.

### Delivery

```bash
curl -X POST https://api.scavio.dev/api/v1/trendyol/delivery \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content_id": "975557855", "city_id": "133", "district_id": "54"}'
```

Captured `data` (Istanbul, Sisli, 2026-11-15; the buy box and 1 of 82 other listings shown):

```json
{
  "content_id": 975557855,
  "item_number": 1378939445,
  "city_id": 133,
  "district_id": 54,
  "time_zone": "Europe/Istanbul",
  "listings": [
    {
      "listing_id": "ff1d23f6969474c32de9c4412c73db12",
      "delivery": {"start": "2026-11-16T04:53:14", "end": "2026-11-18T04:53:14"},
      "ships_by": "2026-11-16T23:59:00",
      "ships_in_days": 1,
      "fast_options": [
        {"type": "tomorrow_shipping", "daily_cutoff": "00:00"}
      ],
      "tomorrow_shipping_cutoff": "00:00",
      "same_day_shipping_cutoff": null,
      "rush_delivery_hours": 24,
      "agreed_delivery_days": 0,
      "local_delivery": true,
      "carriers": [],
      "seller": {"id": 807735, "name": "Kapdiyo"},
      "buy_box": true
    },
    {
      "listing_id": "9322d0bd34466c7799a7d7f69ef14716",
      "delivery": {"start": "2026-11-16T04:53:14", "end": "2026-11-19T04:53:14"},
      "ships_by": "2026-11-16T23:59:00",
      "ships_in_days": 1,
      "fast_options": [
        {"type": "tomorrow_shipping", "daily_cutoff": "00:00"}
      ],
      "tomorrow_shipping_cutoff": "00:00",
      "same_day_shipping_cutoff": null,
      "rush_delivery_hours": 24,
      "agreed_delivery_days": 1,
      "local_delivery": true,
      "carriers": [],
      "seller": null,
      "buy_box": false
    }
  ],
  "count": 83,
  "notes": ["Dates are local times in time_zone, as the site shows them.", "Trendyol estimates every listing of the item; seller is named for the buy box and the other sellers the product page lists, null for the rest."],
  "country": "tr",
  "language": "tr",
  "currency": "TRY"
}
```

Dates are local times in `time_zone`. `seller` is named for the buy box and the sellers the product page lists, `null` for the rest.

### Python

```python
import time
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def ty(endpoint, body, timeout=180):
    r = requests.post(f"{BASE}/api/v1/trendyol/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    if r.status_code == 404:
        return None  # unknown, or not sold on that storefront (charged)
    r.raise_for_status()
    return r.json()["data"]

# Every seller's price for one product (1 credit).
p = ty("product", {"content_id": "975557855"})
captured_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
offers = [{"seller": p["buy_box"]["seller"], "price": p["buy_box"]["price"], "buy_box": True}]
offers += [{"seller": o["seller"], "price": o["price"], "buy_box": False, "badge": o["lowest_price_badge"]} for o in p["other_sellers"]]
offers.sort(key=lambda o: o["price"])  # the site's order is not by price

cheapest = offers[0]
print(p["name"], p["currency"], captured_at)
print("buy box:", p["buy_box"]["seller"]["name"], p["buy_box"]["price"])
print("cheapest:", cheapest["seller"]["name"], cheapest["price"], "(buy box)" if cheapest["buy_box"] else "")
for o in offers:
    print(o["seller"]["id"], o["seller"]["name"], o["seller"]["score"], o["price"])

# Store `offers` with captured_at, country and currency, and run this on a schedule:
# that stored series is your price history (Trendyol publishes none).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live; nothing is cached. Every `data` echoes `country`, `language` and `currency`. Prices are numbers in the market's currency, never converted. `notes` appears when there is something to say.

- **Grid item** (search, category, brand, deals, seller catalog) - `position`, `content_id`, `group_id`, `listing_id`, `item_number`, `name`, `brand` {`id`, `name`}, `category` {`name`}, `url`, `image`, `images[]`, `price`, `original_price`, `discount_percent`, `rrp`, `plus_price`, `currency`, `lowest_price_badge` {`days`, `text`} or `null`, `badges[]` (`free_shipping`, `rush_delivery`, `next_day_delivery`, `same_day_shipping`, `ships_tomorrow`, `flash_sale`, `coupon`, `best_seller`, `fast_seller`, `official_seller`, `lowest_price`), `best_seller_rank`, `labels[]` (the site's own badge texts), `promotions[]`, `rating`, `review_count`, `favourites` and `orders` (the site's rounded text), `seller` {`id`}, `color`, `variant`, `sponsored`.
- **Grid** - `items[]`, `count` (organic items), `sponsored_count`, `total`, `total_capped`, `page`, `page_size` (36), `total_pages` (at most 138), `sort`, `requested_filters` and, with `include_facets`, `facets[]` {`param`, `key`, `name`, `type`, `options[]` {`value`, `label`, `count`}, `option_count`, `min` / `max`}. Search adds `query`; category adds `category` {`id`, `name`, `url`}; brand adds `brand` {`id`, `name`, `url`}; deals adds `type`, `slot`, `slots[]` {`tag`, `status`, `date`, `start`, `end`}.
- **product** - `content_id`, `product_group_id`, `product_code`, `name`, `brand` {`id`, `name`, `url`}, `category` {`id`, `name`, `path`, `tree[]` {`id`, `name`, `level`}}, `url`, `price`, `original_price`, `discount_percent`, `rrp`, `currency`, `lowest_price_badge`, `in_stock`, `running_out`, `max_per_order`, `color`, `options[]` {`name`, `value`}, `variants[]` {`attribute`, `value`, `item_number`, `in_stock`, `price`, `barcode`, `selected`}, `attributes[]` {`name`, `value`, `starred`}, `images[]`, `rating`, `rating_count`, `review_count`, `favourite_count`, `category_rankings[]` {`ranking`, `rank`}, `buy_box` {`seller` {`id`, `name`, `score`, `badges`, `city`, `country`, `cash_on_delivery`, `corporate_invoice`}, `listing_id`, `item_number`, `price`, `original_price`, `discount_percent`, `rrp`, `currency`, `free_shipping`, `rush_delivery_hours`, `flash_sale`, `has_coupon`}, `other_sellers[]` {`seller` {`id`, `name`, `score`, `badges`}, `listing_id`, `item_number`, `price`, `original_price`, `discount_percent`, `rrp`, `currency`, `free_shipping`, `rush_delivery`, `lowest_price_badge`, `promotions[]`}, `other_seller_count`, `promotions[]` {`id`, `name`, `short_name`, `type`, `ends_at`}, `returnable`, `max_installments`, `vat_percent`, `has_description`, `description` and `description_html` (with `include_description`), `notes[]`.
- **reviews** - `content_id`, `rating`, `rating_count`, `review_count`, `photo_review_count`, `rating_histogram` {`1` to `5`}, `topics[]` {`name`, `count`, `positive`, `negative`, `positive_percent`}, `sizes[]`, `review_summary` {`text`, `source`}, `reviews[]` {`id`, `rating`, `text`, `date`, `updated_at`, `likes`, `author`, `verified_buyer`, `elite`, `influencer`, `seller` {`id`, `name`}, `size`, `fit`, `variant`, `language`, `photos[]` {`url`, `thumbnail`, `type`}}, `count`, `page`, `page_size`, `total_pages`, `sort`, `rating_filter`, `with_media`.
- **questions** - `content_id`, `total`, `total_asked`, `topics[]` {`name`, `count`}, `questions[]` {`id`, `text`, `original_text`, `date`, `verified_buyer`, `answer` {`text`, `original_text`, `answered_in`, `seller` {`id`, `name`}}}, `count`, `page`, `page_size`, `total_pages`.
- **seller** - `seller` {`id`, `name`, `score`, `score_scale`, `product_count`, `product_count_capped`, `follower_count`, `followers_text`, `follower_coupon`, `badges[]`, `ranking`, `city`, `on_trendyol_for`, `average_shipping_time`, `question_response_time`, `average_product_rating`, `average_seller_rating`, `corporate_invoice`, `metrics[]` {`id`, `title`, `value`}, `logo`, `store_url`} plus, with `include_products`, the grid of the seller's catalog.
- **coupons** - `content_id`, `product` {`name`, `seller` {`id`, `name`}, `price`, `currency`}, `coupons[]` {`id`, `discount`, `discount_type` (`amount` or `percent`), `discount_amount`, `discount_percent`, `max_discount`, `min_basket`, `currency`, `valid_until` (Turkey time), `issued_by`, `seller_id`, `link`, `mega_coupon`, `plus_members_only`, `messages[]`, `collectable`}, `count`.
- **rankings** - `ranking`, `category` {`id`, `name`}, `items[]` {`rank`, `content_id`, `listing_id`, `name`, `brand`, `url`, `image`, `images[]`, `price`, `original_price`, `discount_percent`, `rrp`, `currency`, `lowest_price_badge`, `badges[]`, `promotions[]`, `rating`, `review_count`, `in_stock`, `running_out`, `seller` {`id`}}, `count`, `total`, `page`, `page_size` (20), `total_pages`.
- **suggestions** - `query`, `suggestions[]` {`text`, `type` (`keyword`, `category`, `brand`, `store` or `other`), `site_type`, `url`, `category_ids`, `seller_id`, `brand_id`, `image`}, `count`.
- **delivery** - `content_id`, `item_number`, `city_id`, `district_id`, `time_zone`, `listings[]` {`listing_id`, `delivery` {`start`, `end`}, `ships_by`, `ships_in_days`, `fast_options[]` {`type`, `daily_cutoff`}, `tomorrow_shipping_cutoff`, `same_day_shipping_cutoff`, `rush_delivery_hours`, `agreed_delivery_days`, `local_delivery`, `carriers[]`, `seller` {`id`, `name`} or `null`, `buy_box`}, `count`.

## Guardrails

- Prices: `price` is what one unit costs at checkout (basket discounts applied); `original_price` is the higher price it is shown against (the previous price, the price before the basket discount, or the recommended retail price), and `discount_percent` is computed from the two. `rrp` is the recommended retail price where shown, `plus_price` the Trendyol Plus member price. Never call `original_price` the 30-day lowest price or yesterday's price, and never present `discount_percent` as a measured price drop.
- Lowest-price badge: `lowest_price_badge.days` is the span of the site's "lowest price of the last N days" tag (10, 14, 30, 90 on `tr`; 7, 14, 30 elsewhere, with `text` `null`). It is a day count, never a price: Trendyol publishes no numeric 30-day lowest price and no price history. For a measured change, compare your own stored readings.
- Buy box: the buy box is Trendyol's default offer, picked by its own metrics, not by price alone. It is not necessarily the cheapest, and `other_sellers[]` comes in the site's order, not sorted by price: sort before naming the cheapest seller. Busy products list 15 or more other sellers.
- Sponsored items: grids interleave ads (`sponsored: true`, 9 to 12 of 36 in the captures, up to about 20) that repeat on every page; `count` excludes them. Drop them before ranking, counting or deduplicating across pages.
- Paging: 36 per page and at most 138 pages (about 5,000 results per query); `total` stops counting at 100000 (`total_capped: true`). Narrow with filters past that.
- Counts: grid `favourites` and `orders` are the site's rounded text (`21K`, `200+`), not numbers. A grid item's `review_count` is the rating count; `/product` and `/reviews` give `rating_count` and `review_count` separately.
- International storefronts: priced on their own, not converted from TRY (measured on 2 products on 2026-11-15). Read each storefront you report, and never compare prices in different currencies without converting explicitly, with the rate and its date.
- Market limits: deals and coupons are `tr` only; rankings are not on the 15 English-language EU storefronts (`fr`, `be`, `hr`, `dk`, `ee`, `fi`, `it`, `lv`, `lt`, `nl`, `pt`, `si`, `es`, `se`, `lu`); `city_id` / `district_id` on delivery are `tr` only (Istanbul `133`, Sisli `54`; there is no city list endpoint).
- Coupons belong to each seller's listing: query `other_sellers[].seller.id` with `seller_id` before saying a product has no coupon. `valid_until` is Turkey time.
- Privacy: reviews carry only the masked display name the site shows (`H** K**`); reviewer height and weight, question askers and sellers' legal disclosures (registered e-mail, tax number, address, legal name) are never returned. No personal data beyond what the page shows masked. Quote short review excerpts only.
- Translations: on international storefronts some questions and answers are Trendyol's translations (`original_text` holds what was written); reviews there are the ones written in that language.
- Not available: price history, a numeric 30-day lowest price, pickup points, a city list, Trendyol GO and Trendyol Yemek, cart, checkout, Plus and Elite membership data.
- Terms: Trendyol's terms of use say the site's materials may not be copied, reproduced or republished without prior written permission. We do not interpret them. This is not legal advice; the user is responsible for their own compliance. Do not republish Trendyol product photos; link product pages instead.
- Never fabricate prices, content ids, seller ids, category ids, coupons, reviews or ratings. Only return what the API returned, with the market, the currency and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` outside the endpoint's markets (deals or coupons off `tr`; rankings on an English-language EU storefront; `ge`, `kz`, `kg`, `iq`, `ie`, `mt`, `gb`, `uk`, `ru`, `us`, `ca`, `jo`, `lb`); a `language` the market does not serve; neither `content_id` nor `url` (or `seller_id` / `category_id` / `brand_id` and `url`), or an id and a `url` that disagree; an id that is not digits; a `listing_id` that is not 32 hex characters; a `url` that is not a Trendyol product, category, brand or store link on trendyol.com, trendyol.ae or trendyol.sa, or a language-only link without `country`; `page` above 138 (rankings above 5); a `sort`, `ranking`, `type`, `seller_type`, `min_rating` or `lowest_price_days` outside its list; `price_max` below `price_min`; a `filters` key that is not a facet param or is already set by a named parameter; `slot` with `super_discounts` or a slot that is not a tag from `slots[]`; `page`, `sort` or `query` on `/seller` without `include_products`; `city_id` / `district_id` off `tr`, or `district_id` without `city_id`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Trendyol has no product ...", "Trendyol does not sell product ... on its ... storefront (unknown, or not sold in this market).", "Trendyol has no category / brand ...", "Trendyol has no seller ...", "Seller ... does not sell product ...", "Product ... has no variant item_number ...", "Trendyol has no ... list for category ...", "No flash sale is running on Trendyol right now", "Trendyol found nothing for this request.". Take ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api).
- `502` means Trendyol data was temporarily unavailable ("Trendyol is temporarily unavailable. Please try again."). It is retried automatically and not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Trendyol is busy ("Trendyol is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.60.1
npm install scavio@0.61.1
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.trendyol.search({ query: "telefon", sort: "price_asc" });
const { data: phone } = await scavio.trendyol.product({ content_id: "975557855" });
const { data: phones } = await scavio.trendyol.category({ category_id: "103498", seller_type: "official" });
const { data: samsung } = await scavio.trendyol.brand({ brand_id: "794" });
const { data: reviews } = await scavio.trendyol.reviews({ content_id: "975557855", sort: "newest" });
const { data: questions } = await scavio.trendyol.questions({ content_id: "975557855" });
const { data: seller } = await scavio.trendyol.seller({ seller_id: "4473", include_products: true });
const { data: flash } = await scavio.trendyol.deals({ type: "flash" });
const { data: coupons } = await scavio.trendyol.coupons({ content_id: "1164743007" });
const { data: top } = await scavio.trendyol.rankings({ category_id: "56", ranking: "best_seller" });
const { data: suggestions } = await scavio.trendyol.suggestions({ query: "iph" });
const { data: delivery } = await scavio.trendyol.delivery({ content_id: "975557855", city_id: "133", district_id: "54" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.trendyol.search(...)`, `client.trendyol.product(...)`, `client.trendyol.category(...)`, `client.trendyol.brand(...)`, `client.trendyol.reviews(...)`, `client.trendyol.questions(...)`, `client.trendyol.seller(...)`, `client.trendyol.deals(...)`, `client.trendyol.coupons(...)`, `client.trendyol.rankings(...)`, `client.trendyol.suggestions(...)` and `client.trendyol.delivery(...)`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all twelve endpoints as tools: `search_trendyol`, `get_trendyol_product`, `get_trendyol_category`, `get_trendyol_brand`, `get_trendyol_reviews`, `get_trendyol_questions`, `get_trendyol_seller`, `get_trendyol_deals`, `get_trendyol_coupons`, `get_trendyol_rankings`, `get_trendyol_suggestions` and `get_trendyol_delivery`. Trendyol is opt-in: add `trendyol` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.58.1"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,trendyol"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/trendyol-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api), [product](https://scavio.dev/docs/trendyol-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api), [category](https://scavio.dev/docs/trendyol-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api), [brand](https://scavio.dev/docs/trendyol-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api), [reviews](https://scavio.dev/docs/trendyol-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api), [questions](https://scavio.dev/docs/trendyol-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api), [seller](https://scavio.dev/docs/trendyol-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api), [deals](https://scavio.dev/docs/trendyol-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api), [coupons](https://scavio.dev/docs/trendyol-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api), [rankings](https://scavio.dev/docs/trendyol-rankings?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api), [suggestions](https://scavio.dev/docs/trendyol-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api), [delivery](https://scavio.dev/docs/trendyol-delivery?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api). Overview: [Trendyol API](https://scavio.dev/trendyol-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api).
