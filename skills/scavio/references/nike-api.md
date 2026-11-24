# Nike API - Sale Prices, Sizes, Release Calendar

Read Nike (nike.com, including Jordan Brand) on 62 storefronts in 42 countries: keyword and style-color search, category listings, the Jordan, ACG and Nike SB brand listings and Nike's Sale listing, one product in full with every size and its GTIN and every colorway with its own price, Nike's launch calendar with each launch's release start, launch method and per-size level, one launch thread, and a product's review summary with the 3 newest reviews. Prices come as Nike shows them on that storefront, in its own currency.

**Read-only data.** This skill reads the public pages Nike shows to any visitor and returns them as JSON for analysis. It does not sign in, enter a launch or place an order, and it is never a purchase tool.

**The job this skill is for: Nike sale prices and sizes.** What a Nike style color costs on each Nike storefront today, next to Nike's own full price and the discount percent Nike gives, which sizes Nike lists for it with each size's GTIN, and what Nike's launch calendar lists with its release start and per-size level. On 2026-11-24 the women's Dunk Low in White/White/Photon Dust (`DD1503-103`) read $78.97 against a $120 full price (34 as Nike's discount percent) on www.nike.com, 54.99 GBP against 109.99 (50) on the UK store, 59.99 EUR against 119.99 (50) on the French store and 17,050 JPY with no markdown (0) on the Japanese store. The Air Jordan 4 Retro OG "Bred" (`IX8180-001`) was on the US launch calendar for 2026-11-27T15:00:00Z at $230, the UK one for 2026-11-27T08:00:00Z at 189.99 GBP and the Japanese one at 34,100 JPY.

Eight limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit, also a product or reviews request by style color. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **First page only.** search, category, brand and deals return the first 24 product groups Nike's page shows. `total` and `total_pages` are as Nike gives them, but Nike's page does not page further: narrow with `filter` tokens or a category path instead of paging.
- **Prices are per storefront.** One style color has a different price on each storefront, also between euro-zone stores (France 59.99 EUR is not every euro store's price). Always report the price with its storefront (`market.country`, `market.language`), its `currency` and the `fetched_at` date; never carry a price from one market to another. There are no store prices.
- **`full_price` and `discount_percent` are Nike's own.** `price` is the price Nike shows, `full_price` the full price Nike shows beside it, and `discount_percent` the percent Nike gives. A promotion text on an item (such as an extra percent off with a code) is quoted as Nike writes it; it is never applied to `price`.
- **Sizes, not stock levels, for regular products.** A product's `sizes[]` lists every size Nike's page shows with its `gtin` and Nike's `status` (`ACTIVE` on every size of the captured products). Nike's product page shows no stock level, so this API returns none for regular products.
- **Per-size levels only on launch items.** `/releases` and `/release` give each size of a launch-calendar product a `level` (`HIGH`, `MEDIUM`, `LOW`, `OOS`, or `null` where Nike gives none) and `available`, as Nike gives them. Before a launch Nike can show `LOW` on every size (all 21 sizes of a Rejuven8 Run on the UK calendar read `LOW` days before its release): read levels on upcoming launches as given, never as unit counts.
- **`method` is Nike's label.** `LINE` or `DRAW`, as Nike labels the launch; the same launch can carry a different method per storefront (the Air Jordan 4 "Bred" read `LINE` in the US and the UK and `DRAW` in Japan, with Nike's window 00:00 to 00:10 UTC on 2026-11-27).
- **No launch calendar in China, on Japan in English or in Vietnam; no reviews in China.** `/releases` and `/release` serve every storefront except `cn`, `jp` with `language` `en`, and `vn`; `/reviews` serves every www.nike.com storefront, not `cn`. Asking for them there is a `400`, not charged.

Nike has no public API for its catalog, prices, sizes or SNKRS launches. Publishers can join its affiliate programme on CJ for links and an automated product feed; the old Nike+ developer program was for fitness data. Prices, sizes and launch dates are shown on nike.com for each country store, and this skill reads them from there.

Nike, the world's largest seller of athletic footwear and apparel, reported $46.4 billion in revenue for its fiscal year ended May 31, 2026, and runs 874 Nike-brand stores (212 factory and 75 in-line in the US) plus digital stores in over 40 countries (FY2026 10-K, filed July 15, 2026). Quote these with their source, never from the samples.

See also: the same style code at Foot Locker `foot-locker-api` and at Dick's Sporting Goods `dicks-sporting-goods-api`; at Amazon `amazon-product-data`; on eBay `ebay-product-data`; prices across retailers `google-shopping-api`. Compare only the same style code (style code and color code), each with its date.

## When to trigger

Use this skill when the user asks to:
- Price a Nike or Jordan style color (Dunk Low, Air Force 1, Air Jordan 1, Pegasus, Vomero) on nike.com, with Nike's full price and discount percent next to the price
- Read every size Nike lists for a product, with each size's GTIN and Nike's status, or every colorway with its own price
- Compare one style color across Nike storefronts (US, UK, France, Germany, Japan, Korea, Australia, Canada, Mexico, China and more), each in its own currency
- List Nike's Sale listing for a gender or a category, a category (men's shoes, running, Black Friday) or the Jordan, ACG or Nike SB listing, sorted by newest or price or filtered by size, colour, price band or discount band
- Read Nike's launch calendar (upcoming, feed, in stock) or one launch: release start, listed price, launch method as Nike labels it and the level of every size
- Read a product's review summary: total reviews, average rating, size and comfort ratings, Nike's own summary and the 3 newest reviews
- Compare one style code at Nike, Foot Locker, Dick's, Amazon or eBay (with `foot-locker-api`, `dicks-sporting-goods-api`, `amazon-product-data` and `ebay-product-data`)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api) - email or Google, no card required.
2. A key is created automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. Signup comes with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, lists, releases and product took 4-8 seconds and reviews about 10. Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Markets | Credits |
|---|---|---|---|
| `POST /api/v1/nike/search` | Keywords or a style color: the first 24 product groups with price, full price, discount percent, promotions with dates, colorways, facets with filter tokens, categories | all 62 | 1 |
| `POST /api/v1/nike/product` | One product by link or style color: price, full price, discount percent, status, release type, launch dates, member product flag, Nike By You flag, every size with GTIN and status, every colorway with its price, features, details | all 62 | 1 |
| `POST /api/v1/nike/category` | One Nike listing by path token or link (men's shoes, running, Black Friday, a collection), sorted and filtered | all 62 | 1 |
| `POST /api/v1/nike/brand` | The Jordan Brand, ACG or Nike SB listing, sorted and filtered | all 62 | 1 |
| `POST /api/v1/nike/deals` | Nike's Sale listing, optionally for one gender or one category, sorted and filtered (discount band, price band) | all 62 | 1 |
| `POST /api/v1/nike/releases` | Nike's launch calendar (upcoming, feed or in stock): each launch's release start, price, method, window, status, thread and per-size level | all but cn, jp/en, vn | 1 |
| `POST /api/v1/nike/release` | One launch thread by link, slug or style color (past launches too), with every product it holds | all but cn, jp/en, vn | 1 |
| `POST /api/v1/nike/reviews` | One product's review summary: total, average, size and comfort ratings, Nike's own summary where shown, the 3 newest reviews | all but cn | 1 |

## Markets

`country` is a two-letter code (default `us`); `language` picks the storefront language where a country has several (default: the first listed). Every answer carries `market` {`country`, `language`, `currency`, `locale`}. Currencies below are as the storefronts returned them on 2026-11-24.

| country | languages | currency |
|---|---|---|
| `us` (www.nike.com) | en, es | USD |
| `gb` | en | GBP |
| `ca` | en, fr | CAD |
| `mx` | es | MXN |
| `au` | en | AUD |
| `jp` | ja, en | JPY |
| `kr` | ko | KRW |
| `cn` (www.nike.com.cn) | zh-Hans | CNY |
| `tw` | zh-Hant | TWD |
| `sg`, `my`, `ph`, `id`, `th`, `vn` | en (th: th) | SGD, MYR, PHP, IDR, THB, VND |
| `ch` | de, en, fr, it | CHF |
| `dk`, `se`, `no` | da / sv / no, and en | DKK, SEK, NOK |
| `pl`, `ro`, `tr`, `il`, `za` | pl, en, tr, en, en | PLN, RON, TRY, ILS, ZAR |
| `de`, `fr`, `it`, `ie`, `fi`, `gr` (el), `si`, `sk`, `hr`, `bg` | one each | EUR |
| `at` (de, en), `be` (nl, de, en, fr), `nl` (nl, en), `lu` (fr, de, en), `es` (es, ca), `pt` (pt, en), `cz` (cs, en), `hu` (hu, en) | as listed | EUR |

Not served (a `400`, not charged): `ae`, `sa`, `ar`, `br`, `cl`, `in`, `co`, `pe`, `kw`, `qa`, `eg`, `ma`, `nz`, `pr`, `ru`, `uy`, `hk`. `uk` is a `400` pointing to `gb`. A link sent as `url` carries its own storefront.

## Prices: price, full price, discount percent, promotions

Every priced item, product, colorway and launch carries:

| Field | Meaning |
|---|---|
| `price` | The price Nike shows on that storefront |
| `full_price` | Nike's full price shown beside it (equal to `price` when Nike shows no markdown) |
| `discount_percent` | The discount percent as Nike gives it (`0` without a markdown); launches carry no `discount_percent` |
| `currency` | The storefront's currency (`USD`, `GBP`, `EUR`, `JPY`, ...) |
| `promotions` | List items only: [{`text`, `starts`, `ends`}], Nike's own offer text with its dates as given (UTC) |

- **Per storefront:** `DD1503-103` read $78.97 / $120 (US), 54.99 / 109.99 GBP (UK), 59.99 / 119.99 EUR (France) and 17,050 / 17,050 JPY (Japan) on 2026-11-24. Report "$78.97 at nike.com (US) on 2026-11-24", with the storefront and the date.
- **Promotions:** on 2026-11-24, 17 of the 24 US `dunk low` search results carried "Extra 25% off w/ code BFRIDAY" (2026-11-22T05:00Z to 2026-11-29T05:00Z). Quote the text and dates as given; `price` stays the listed price, and no code is applied or computed. The product page carries no promotion texts: read them from a list item.
- **Guest prices only:** no member, app, employee or code prices; `member_product` flags a product Nike marks for members.
- Report Nike's labels and the arithmetic only. Never judge a full price or a discount, and never describe how often an item is on sale.

## Sizes and launch levels

- **Regular products:** `/product` `sizes[]` {`label`, `localized_label`, `gtin`, `status`}: the US women's Dunk Low `IM6572-104` listed 15 sizes from "W 5 / M 3.5" (GTIN `00198730351384`), all `ACTIVE`. That is the size run Nike lists, not a stock reading.
- **Launch items:** `/releases` and `/release` `launches[].sizes[]` {`size`, `localized_size`, `gtin`, `level`, `available`}: the US Air Jordan 4 "Bred" (`IX8180-001`) read 23 sizes `HIGH` and 2 `LOW`, all 25 `available`, three days before its release; the US Air Jordan 10 "Black and Dark Concord" (`HJ6779-002`) read 14 of 18 sizes `OOS`.
- Count levels as Nike gives them ("14 of 18 sizes OOS on 2026-11-24"); never turn a level into a unit count, a delivery date or a promise that a size can be had.

## Workflow

1. **Find the product.** `/search` with `q` (keywords such as `dunk low`, or a style color such as `DD1503-103`), or `/category` (a `categories[].path` token or a `/w/` link), `/brand` (`jordan`, `acg`, `sb`) or `/deals` (Nike's Sale listing). Each item's `style_color` and `url` are the inputs of product and reviews.
2. **Read it in full.** `/product` with `url` (or `style_color` with `country`): price, full price, discount percent, every size with GTIN and status, every colorway with its price.
3. **Compare storefronts.** Send the same `style_color` with another `country` (and `language`). Each answer has its own `currency`; convert only with a dated rate you state.
4. **Narrow a list.** Send a `facets[].options[].filter` token back as `filter` (search takes one token; category, brand and deals take up to 6). A token from a filtered answer already carries the filters applied there, so narrow step by step. `sort`: `featured`, `newest`, `price_high`, `price_low`.
5. **Launch calendar.** `/releases` with `view` (`upcoming`, `feed`, `in_stock`) and `country`; each launch has `style_color`, `release_start`, `price`, `method` and `sizes[]` with levels. A thread can hold several products (adult and kids' sizes).
6. **One launch.** `/release` with `url` (`launches[].thread.url`), `slug` (`launches[].thread.slug`) or `style_color`. A launch-calendar product asked of `/product` by style color is a charged `404` that points here.
7. **Reviews.** `/reviews` with the product `url` or `style_color`: the summary and the 3 newest reviews, no paging.
8. **Watching prices or levels:** there is no history. Poll the same style colors on a schedule and store each answer with its `fetched_at` and market; that stored series is the history.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | required | Keywords or a style color; 1-200 chars |
| `sort` | string | `featured` | `featured`, `newest`, `price_high`, `price_low` |
| `filter` | string | none | ONE facet token from an earlier answer (`facets[].options[].filter`, e.g. `black-90poy`) |
| `country`, `language` | string | `us`, primary | See Markets |

### Product (`/product`) and reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | A Nike product link (`items[].url`; on product a Nike By You `/u/` link too). Its storefront comes from the link |
| `style_color` | string | one of | A Nike style color (style code, dash, 3-character color code: `DD1503-103`), found through Nike's search on the storefront first |
| `country`, `language` | string | `us`, primary | With `style_color` |

### Category (`/category`), brand (`/brand`), deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | string | category: one of | A Nike listing path token (`categories[].path`, or the part after `/w/` of a Nike listing link: `mens-shoes-nik1zy7ok`) |
| `url` | string | category: one of | A Nike listing link (`www.nike.com/.../w/<path>`); its storefront comes from the link |
| `brand` | string | brand: required | `jordan`, `acg` or `sb` |
| `gender` | string | none | Deals: `men`, `women`, `unisex`, `boys`, `girls` |
| `category` | string | none | Deals: only this listing path token (`categories[].path` of an earlier deals answer) |
| `sort` | string | `featured` | As above |
| `filter` | string or array | none | 1-6 facet tokens from an earlier answer |
| `country`, `language` | string | `us`, primary | See Markets |

### Releases (`/releases`) and release (`/release`)

`/releases` takes `view` (`upcoming` default, `feed`, `in_stock`) and `country`, `language`. `/release` takes one of `url` (a Nike launch link), `slug` (`air-jordan-4-bred`) or `style_color`, and `country`, `language`.

## Examples

### One product with its sizes and colorways

```bash
curl -X POST https://api.scavio.dev/api/v1/nike/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.nike.com/t/dunk-low-womens-shoes-ppQwKZ/IM6572-104"}'
```

Captured `data` (2026-11-24; `description`, `features`, `details` and `images` dropped, `categories` cut to 2 of 5, `sizes` to 3 of 15, `colorways` to 2 of 18 without `image`, `notes` to 3):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "locale": "en-US" },
  "requested_style_color": "IM6572-104",
  "found_requested_style_color": true,
  "style_color": "IM6572-104",
  "style_code": "IM6572",
  "prebuild_id": null,
  "name": "Nike Dunk Low Women's Shoes",
  "title": "Nike Dunk Low",
  "subtitle": "Women's Shoes",
  "url": "https://www.nike.com/t/dunk-low-womens-shoes-ppQwKZ/IM6572-104",
  "color": "Sail/White/Peony",
  "price": 71.97,
  "full_price": 120,
  "discount_percent": 40,
  "currency": "USD",
  "status": "BUYABLE_BUY",
  "release_type": "FLOW",
  "availability_date": "2026-04-20T14:00:00.000Z",
  "launch": null,
  "launch_product": false,
  "member_product": false,
  "by_you": false,
  "promo_excluded": false,
  "product_type": "FOOTWEAR",
  "brands": ["Nike", "Nike Sportswear"],
  "genders": ["WOMEN"],
  "sports": ["Lifestyle"],
  "categories": [
    { "name": "Gender", "values": ["Women"] },
    { "name": "Sports", "values": ["Lifestyle"] }
  ],
  "badge": null,
  "featured_attributes": [],
  "fit_message": "Fits large; we recommend ordering a half size down",
  "size_chart_url": "https://www.nike.com/size-fit/womens-footwear",
  "sizes": [
    { "label": "5", "localized_label": "W 5 / M 3.5", "gtin": "00198730351384", "status": "ACTIVE" },
    { "label": "5.5", "localized_label": "W 5.5 / M 4", "gtin": "00198730362311", "status": "ACTIVE" },
    { "label": "6", "localized_label": "W 6 / M 4.5", "gtin": "00198730364322", "status": "ACTIVE" }
  ],
  "colorways": [
    { "group": null, "style_color": "IM6572-104", "color": "Sail/White/Peony", "price": 71.97, "full_price": 120, "discount_percent": 40, "currency": "USD", "status": "BUYABLE_BUY", "url": "https://www.nike.com/t/dunk-low-womens-shoes-ppQwKZ/IM6572-104" },
    { "group": null, "style_color": "DD1503-103", "color": "White/White/Photon Dust", "price": 78.97, "full_price": 120, "discount_percent": 34, "currency": "USD", "status": "BUYABLE_BUY", "url": "https://www.nike.com/t/dunk-low-womens-shoes-ppQwKZ/DD1503-103" }
  ],
  "notes": [
    "price and full_price are as Nike shows them; discount_percent is as Nike gives it. Prices are per storefront (they differ between markets, also inside the euro zone); there are no store prices.",
    "sizes are the sizes Nike's page lists, with each size's GTIN and status as given. Nike's product page shows sizes, not stock levels.",
    "status is Nike's own availability label as given (BUYABLE_BUY, COMING_SOON, NOTIFY_ME); release_type is as given (FLOW, RELEASE, LAUNCH)."
  ]
}
```

$120 - $71.97 = $48.03 off Nike's full price, which is the 40 Nike gives as `discount_percent`. The same `DD1503-103` colorway sent with `{"style_color": "DD1503-103", "country": "fr"}` read "Chaussure Nike Dunk Low pour Femme", 59.99 EUR against 119.99 (50), 15 sizes from `localized_label` "35.5".

### The launch calendar with per-size levels

```bash
curl -X POST https://api.scavio.dev/api/v1/nike/releases \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"view": "upcoming"}'
```

Captured `data` (2026-11-24; 1 of 18 launches shown, its `image` dropped and `sizes` cut to 3 of 25, `notes` to 2 of 4):

```json
{
  "market": { "country": "us", "language": "en", "currency": "USD", "locale": "en-US" },
  "view": "upcoming",
  "count": 18,
  "thread_count": 11,
  "launches": [
    {
      "style_color": "IX8180-001",
      "name": "Air Jordan 4 Retro OG \"Bred\"",
      "subtitle": "Men's Shoes",
      "price": 230,
      "full_price": 230,
      "currency": "USD",
      "product_type": "FOOTWEAR",
      "release_start": "2026-11-27T15:00:00.000Z",
      "method": "LINE",
      "entry_start": "2026-11-27T15:00:00.000Z",
      "entry_end": null,
      "exclusive_access": false,
      "launch_status": "ACTIVE",
      "thread": { "slug": "air-jordan-4-bred", "title": "Air Jordan 4 'Bred' (IX8180-001) Release Date", "url": "https://www.nike.com/launch/t/air-jordan-4-bred" },
      "sizes": [
        { "size": "3.5", "localized_size": "M 3.5 / W 5", "gtin": "00198966834057", "level": "LOW", "available": true },
        { "size": "4", "localized_size": "M 4 / W 5.5", "gtin": "00198966850774", "level": "HIGH", "available": true },
        { "size": "4.5", "localized_size": "M 4.5 / W 6", "gtin": "00198966842069", "level": "HIGH", "available": true }
      ]
    }
  ],
  "notes": [
    "sizes[].level (HIGH, MEDIUM, LOW, OOS) and available are as Nike gives them for each size; null where Nike gives none. Before a launch Nike can show LOW on every size, so read levels on upcoming launches as given, not as stock counts.",
    "method is the launch method as Nike gives it (LINE: first come, first served; DRAW: a draw); release_start, entry_start and entry_end are as given (UTC)."
  ]
}
```

The same calendar listed the Air Jordan 11 Retro OG "Space Jam" (`CT8012-900`) for 2026-12-12T15:00:00Z at $235, with big kids' (`378038-900`) at $190, little kids' at $105 and baby/toddler at $90 in the same thread. `{"country": "gb"}` listed it at 189.99 GBP for 2026-12-12T08:00:00Z, and `{"country": "jp"}` at 35,200 JPY with `method` `DRAW`. `/release` `{"style_color": "IX8180-001"}` returns the whole "Bred" thread (men's $230, big kids' $165, little kids' $105, baby/toddler $90).

### Search, listings and reviews

- `/search` `{"q": "dunk low"}`: `total` 36, `total_pages` 2, `count` 24 (first page only). First item Nike Dunk Low SE "Gloss" Women's Shoes (`IV5104-102`) $92.97 / $120 (22), with 18 `colorways` and the promotion "Extra 25% off w/ code BFRIDAY". Facets include Size (26 options), Color, Brand and Gender, each option with its `filter` token (size "M 3.5 / W 5" is `1hsnh`). Many storefronts group every colorway under an item (among them the US, the UK, Germany, Japan, Korea and China); others show one colorway per item, and the answer's notes say which.
- `/search` `{"q": "dunk low", "country": "gb"}`: `total` 152; Nike Dunk Low Retro Men's Shoes (`HF5441-105`) 54.99 / 109.99 GBP (50), badge "Bestseller". The UK facets include "Product Discounts" (20-30%, 30-40%, 40-50%, 50% or more) and "Shop By Price".
- `/category` `{"path": "mens-shoes-nik1zy7ok"}`: "Mens Shoes", `total` 850; facets include "Sale & Offers" (Sale 513, Black Friday 607) and Shop by Price; `categories` such as Jordan (`mens-jordan-shoes-37eefznik1zy7ok`), Lifestyle and Running.
- `/brand` `{"brand": "jordan"}`: "Jordan", `total` 1,989, the Air Jordan 4 Retro OG "Bred" first at $230 with badge "Coming Soon".
- `/deals` `{"gender": "women"}`: "Womens Sale", `total` 2,784; Nike Pegasus Premium Women's Road Running Shoes (`HQ2593-004`) $176.97 / $220 (19) first, with `categories` such as Shoes (1,753) and Jordan (554).
- `/reviews` `{"style_color": "CW2288-111"}` (Air Force 1 '07): `total_reviews` 5,631, `average_rating` 4.9, `average_size_rating` 1.14, `average_comfort_rating` 1.68, Nike's own `review_summary` ("Praised for versatility and classic style, ... Fit runs large—sizing down half a size is commonly recommended. ..."), and the 3 newest reviews with `heading`, `rating`, `created_at`, `text`, `verified_purchase` and `sweepstakes_entry`. No reviewer names.

### Python

```python
import requests
from collections import Counter

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def nike(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/nike/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. One style color on four storefronts (1 credit each)
for country in ["us", "gb", "fr", "jp"]:
    p = nike("product", {"style_color": "DD1503-103", "country": country})["data"]
    print(country, p["currency"], p["price"], p["full_price"], p["discount_percent"], len(p["sizes"]), "sizes")

# 2. Every size with its GTIN (1 credit)
p = nike("product", {"url": "https://www.nike.com/t/dunk-low-womens-shoes-ppQwKZ/IM6572-104"})["data"]
for s in p["sizes"]:
    print(s["localized_label"], s["gtin"], s["status"])

# 3. The UK launch calendar with each launch's size levels (1 credit)
cal = nike("releases", {"view": "upcoming", "country": "gb"})["data"]
for l in cal["launches"]:
    levels = Counter(str(s["level"]) for s in l["sizes"])
    print(l["release_start"], l["style_color"], l["name"], l["price"], l["currency"], l["method"], dict(levels))

# Prices and levels can change between calls. Store each answer with fetched_at
# and the market and run this on a schedule: that stored series is your history
# (Nike shows only the current price, sizes and levels).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` {`country`, `language`, `currency`, `locale`}.

- **item** (search, category, brand, deals) - `position`, `style_color`, `name`, `subtitle`, `color`, `price`, `full_price`, `discount_percent`, `currency`, `product_type`, `image`, `url`, `by_you`, `badge`, `featured_attributes`, `is_new_until`, `promotions[]` {`text`, `starts`, `ends`}, `colorways[]` {`style_color`, `color`, `price`, `full_price`, `discount_percent`, `currency`, `image`, `url`}.
- **lists** - `sort`, `path`, `title`, `total`, `total_pages` (as Nike gives them), `count`, `filters_applied`, `items[]`, `facets[]` {`name`, `options[]` {`name`, `count`, `selected`, `filter`}}, `categories[]` {`name`, `count`, `path`}, `notes`. Search adds `query`; category `category`; brand `brand`; deals `gender`, `category`.
- **product** - `requested_style_color`, `found_requested_style_color`, `style_color`, `style_code`, `prebuild_id` (Nike By You), `name`, `title`, `subtitle`, `url`, `color`, `price`, `full_price`, `discount_percent`, `currency`, `description`, `features[]` {`header`, `items`}, `details[]` {`header`, `items`}, `status` (`BUYABLE_BUY`, `COMING_SOON`, `NOTIFY_ME` as given), `release_type` (`FLOW`, `RELEASE`, `LAUNCH` as given), `availability_date`, `launch` {`start`, `end`}, `launch_product`, `member_product`, `by_you`, `promo_excluded`, `product_type`, `brands`, `genders`, `sports`, `categories[]` {`name`, `values`}, `badge`, `featured_attributes`, `fit_message`, `size_chart_url`, `sizes[]` {`label`, `localized_label`, `gtin`, `status`}, `colorways[]` {`group`, `style_color`, `color`, `price`, `full_price`, `discount_percent`, `currency`, `status`, `url`, `image`}, `images`, `notes`.
- **releases** - `view`, `count`, `thread_count`, `launches[]` {`style_color`, `name`, `subtitle`, `price`, `full_price`, `currency`, `product_type`, `release_start`, `method` (`LINE` or `DRAW` as given), `entry_start`, `entry_end` (Nike's window, UTC), `exclusive_access`, `launch_status`, `thread` {`slug`, `title`, `url`}, `image`, `sizes[]` {`size`, `localized_size`, `gtin`, `level`, `available`}}, `notes`.
- **release** - `requested_style_color`, `found_requested_style_color`, `thread` {`slug`, `title`, `url`}, `count`, `launches[]` (as above, the requested style color first), `notes`.
- **reviews** - `requested_style_color`, `url`, `style_color` (the colorway Nike's reviews page names, which can differ from the requested one), `total_reviews`, `average_rating`, `average_size_rating`, `average_comfort_rating`, `review_summary` (Nike's own, where shown), `count`, `reviews[]` {`heading`, `rating`, `created_at`, `text`, `verified_purchase`, `sweepstakes_entry`}, `notes`.

## Guardrails

- Name it "Nike (nike.com, including Jordan Brand)" on first mention. Converse, Nike Factory store prices and Nike member, app and employee prices are not read.
- Read-only: report what Nike's public pages show. Never present this skill as a way to buy, enter a launch or get a product ahead of other shoppers, and never help automate any of that.
- Prices: quote `price`, `full_price` and `discount_percent` as Nike gives them, with the storefront, the currency and the `fetched_at` date. Never call a storefront's price "Nike's price" without the storefront, and never carry a price across markets.
- Report Nike's labels (full price, discount percent, promotion text with its dates, badges) and the arithmetic only. Never judge a full price, a discount or an offer, never describe how often an item is on sale, and never compute a price after a code.
- Sizes: on a regular product, say "sizes Nike lists", never "in stock". Levels on launch items are Nike's (`HIGH`, `MEDIUM`, `LOW`, `OOS`); report them as given with the date and never as unit counts or a promise that a size can be had.
- Comparing Nike with Foot Locker, Dick's, Amazon or eBay: compare only the same style code and color code, each with its date and its currency. Never call one retailer cheaper beyond the numbers shown.
- Reviews: the summary and the 3 newest reviews only. Never present them as all reviews. No reviewer names are returned.
- Not available: stock levels for regular products, store stock and pickup, a store locator, review paging, sorting or Q&A, search suggestions, results beyond the first page, member and code prices, gift cards, Nike Factory store prices, Converse, price history (poll and store), and any ordering. This API cannot reserve, enter or buy anything.
- Terms: Scavio does not collect or store Nike data: each call fetches the public Nike page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Nike's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Nike product photos, logos or campaign images; link products by `url` instead.
- Never fabricate prices, sizes, GTINs, style colors, dates, levels, methods or ratings. Only return what the API returned, with the `fetched_at` time, the market and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` that is not served (the message lists the served ones) or `uk` (use `gb`); a `language` the country does not offer (the message lists them); releases or release on `cn`, `jp` with `en`, or `vn`; reviews on `cn`; a `style_color` that is not style code, dash, 3-character color code; a `url` that is not a nike.com link, or a launch link sent to product (use release); a Nike By You `/u/` link sent to reviews; a path token that is not a Nike listing token; more than one `filter` token on search or more than 6 on a list; an unknown `sort`, `brand`, `gender` or `view`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Unknown Nike product (search lists style colors and product links; gift cards are not served).", "No Nike product with style color ... on this storefront (Nike's search does not list it).", "... is a launch-calendar product on this storefront: Nike lists it on its launch page, which the release endpoint returns ...", "No products in this Nike listing (categories[].path of an earlier answer lists Nike's paths).", "No products for this brand and filter on this Nike storefront.", "No sale products for these filters on this Nike storefront.", "Unknown Nike launch (releases lists thread slugs; a style color is found only for launch-calendar products).", "Nike's launch calendar does not list ... on this storefront.", "No Nike reviews page for this product.". Take style colors, links, slugs and tokens from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api).
- `502` means Nike data was temporarily unavailable ("Nike is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Nike is busy ("Nike is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.82.0
npm install scavio@0.83.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: results } = await scavio.nike.search({ q: "dunk low" });
const { data: uk } = await scavio.nike.search({ q: "dunk low", country: "gb" });
const { data: shoe } = await scavio.nike.product({ url: "https://www.nike.com/t/dunk-low-womens-shoes-ppQwKZ/IM6572-104" });
const { data: france } = await scavio.nike.product({ style_color: "DD1503-103", country: "fr" });
const { data: mens } = await scavio.nike.category({ path: "mens-shoes-nik1zy7ok" });
const { data: jordan } = await scavio.nike.brand({ brand: "jordan" });
const { data: sale } = await scavio.nike.deals({ gender: "women" });
const { data: calendar } = await scavio.nike.releases({ view: "upcoming" });
const { data: launch } = await scavio.nike.release({ style_color: "IX8180-001" });
const { data: reviews } = await scavio.nike.reviews({ style_color: "CW2288-111" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.nike.search(...)`, `product`, `category`, `brand`, `deals`, `releases`, `release` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 8 endpoints as tools: `search_nike`, `get_nike_product`, `get_nike_category`, `get_nike_brand`, `get_nike_deals`, `get_nike_releases`, `get_nike_release` and `get_nike_reviews`. Nike is opt-in: add `nike` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.82.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,nike"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/nike-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api), [product](https://scavio.dev/docs/nike-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api), [category](https://scavio.dev/docs/nike-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api), [brand](https://scavio.dev/docs/nike-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api), [deals](https://scavio.dev/docs/nike-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api), [releases](https://scavio.dev/docs/nike-releases?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api), [release](https://scavio.dev/docs/nike-release?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api), [reviews](https://scavio.dev/docs/nike-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api). Overview: [scavio.dev/nike-api](https://scavio.dev/nike-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api).
