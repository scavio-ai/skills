---
name: mercari-api
description: "Mercari API for Mercari sold prices and listings on Mercari US (mercari.com, USD, English) and Mercari Japan (jp.mercari.com, JPY, Japanese, as sellers wrote it, not translated): search by keyword, category or brand with status on sale, sold (sold items and items sold but still in transit) or all, so asking prices and sold prices for one query come from the same endpoint; sorted by relevance, newest, price, recently sold (US) or likes (Japan) and filtered by price range, condition, shipping payer, size (US), price-dropped deals (US) or Mercari Shops business sellers (Japan); US 50 per page up to page 20 (1,000 results), Japan 120 per page up to page 91. One item in full by id or link, sold items included, with sold_at, price, original_price and discount_percent when the seller dropped the price, condition, category path, shipping (payer, method, fee, days to ship, ships from state or prefecture), likes, photos and the seller summary (US rating, review and sold counts, verification badges; Japan good / normal / bad ratings), plus on Japan the item's full public comment list (text, date, whether the seller wrote it, no commenter names) and Mercari Shops products with their shop. Listings of one category or brand; the category tree (US one level at a time, Japan the whole tree of 8,784 categories) and the brand list (US 28,853 brands, Japan 52,600) with ids per market; the US deals list of price-dropped listings; Mercari US trending keywords (search rank, rank change, search growth) and trending brands (demand, demand change, 7-day sold rate as Mercari shows them). Mercari Japan only: a seller's public profile with good / normal / bad ratings, listing count, followers, badges and the first 30 listings, the seller's most recent 100 reviews (rating, text, date, as seller or buyer, no reviewer names) and a Mercari Shops shop profile. 11 endpoints, 1 credit each. Item, category, brand and seller ids are per market. Japan calls are slower (search 30 to 60 seconds). Not available: US seller profiles and reviews, search suggestions, price history (poll and store). Mercari publishes no public marketplace data API; the Mercari Shops API is for shop owners managing their own shop."
version: 1.0.0
tags: mercari, mercari-api, mercari-sold, mercari-sold-prices, mercari-sold-listings, mercari-price, mercari-prices, mercari-price-check, mercari-search, mercari-listings, mercari-japan, mercari-jp, mercari-us, mercari-shops, mercari-seller, mercari-seller-ratings, mercari-reviews, mercari-trending, mercari-deals, mercari-brands, mercari-categories, mercari-scraper, resale, reseller, resale-prices, sold-comps, price-research, secondhand, marketplace, japan, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/docs/mercari-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api
---

# Mercari API - Sold Prices, Listings and Sellers, US and Japan

Read Mercari's two marketplaces: Mercari US (mercari.com, US dollars, English) and Mercari Japan (jp.mercari.com, yen, Japanese). Search listings by keyword, category or brand, on sale or sold; read one item in full; browse the category tree and the brand list; read the US deals list and what is trending on Mercari US; and on Mercari Japan read a seller's profile, the seller's most recent reviews and a Mercari Shops shop. All 11 endpoints return structured JSON and cost 1 credit per call.

**The job this skill is for: Mercari sold prices.** `/search` with `status: "sold"` returns sold listings with their prices (sold items and items sold but still in transit, `status: "trading"`). The same query with the default `status: "on_sale"` returns the asking prices of live listings, so asking price and sold price for one query come from the same endpoint, one call each. A sold item keeps its full listing: `/item` on a sold US item returns its `sold_at` time, price, the seller's earlier price and the rest of the listing. Search results carry no sold time and no likes; `/item` has both.

Captured on 2026-11-16 on `us` with `query` `nintendo switch`, page 1 of each:

| `status` | `sort` | `count` | `status` of the items | median `price` (USD) | lowest / highest |
|---|---|---|---|---|---|
| `on_sale` | `relevance` | 50 | 50 `on_sale` | 38.55 | 6 / 550 |
| `sold` | `recently_sold` | 50 | 50 `trading` | 36.23 | 7 / 374.99 |

Both pages mix consoles, games and accessories (the sold page opened with "Mortal Kombat 1 Nintendo Switch Game" at 16 USD), so a median over one keyword page is not the price of one product. Narrow first (a `category_id` such as `797` Consoles, a `brand_id`, a `condition`, a `price_min`), then compare. The most recently sold items are usually still in transit (`trading`): all 50 on that page were.

Mercari publishes no public marketplace data API for Mercari US or Mercari Japan. Mercari Shops (Japan) has an API for shop owners to manage their own products and orders; it is not a marketplace data API.

See also: for eBay sold listings use `ebay-product-data`; for second-hand fashion on Vinted use `vinted-api`; for trading card market prices use `tcgplayer-api`.

## When to trigger

Use this skill when the user asks to:
- Find what an item sells for on Mercari: sold listings and their prices for a query, category or brand
- Compare Mercari asking prices with sold prices for the same query
- Check whether a seller dropped the price of a listing (`original_price` and `discount_percent`)
- Read one Mercari listing from a link: description, condition, shipping, likes, photos, when it sold and the seller's rating
- Search Mercari Japan (in Japanese, prices in yen) for collectibles, trading cards, games or brand goods
- Read the public comments (price questions, authenticity questions, seller answers) on a Mercari Japan listing
- Check a Mercari Japan seller before buying: good / normal / bad ratings, listing count, badges and recent reviews
- Look up a Mercari Shops (business seller) shop in Japan
- See what is trending on Mercari US (keywords and brands) or browse Mercari US price-dropped listings (deals)
- Resolve Mercari category ids and brand ids for either market

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit, so the free credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. On `us` most calls take 3 to 20 seconds. On `jp` calls are slower: search typically 30 to 60 seconds, other endpoints 10 to 30 seconds. Set a client timeout of at least 240 seconds and send one call at a time (a busy moment answers `503` with `Retry-After`).

| Endpoint | Markets | Credits | What it returns |
|---|---|---|---|
| `POST /api/v1/mercari/search` | `us`, `jp` | 1 | Listings for a keyword (or a category or brand), on sale, sold or all, sorted and filtered: 50 per page up to page 20 on `us`, 120 per page up to page 91 on `jp` |
| `POST /api/v1/mercari/item` | `us`, `jp` | 1 | One listing by `item_id` or link: description, price, `original_price`, status, `sold_at`, condition, category path, shipping, likes, photos and the seller summary; `jp` adds the full public comment list and Mercari Shops products |
| `POST /api/v1/mercari/category` | `us`, `jp` | 1 | Listings in one category, with the search filters |
| `POST /api/v1/mercari/categories` | `us`, `jp` | 1 | The category tree: `us` one level at a time (17 top-level categories), `jp` the whole tree (8,784 categories) or one parent's children |
| `POST /api/v1/mercari/brands` | `us`, `jp` | 1 | The brand list (`us` 28,853 brands, `jp` 52,600), filtered by name, pages of 1,000 |
| `POST /api/v1/mercari/brand` | `us`, `jp` | 1 | Listings of one brand, with the search filters |
| `POST /api/v1/mercari/deals` | `us` | 1 | Listings on Mercari's deals filter: the seller dropped the price, each with `original_price` and `discount_percent` |
| `POST /api/v1/mercari/trending` | `us` | 1 | Mercari's trending keywords and trending brands as its trending page lists them |
| `POST /api/v1/mercari/seller` | `jp` | 1 | A Mercari Japan seller's public profile with good / normal / bad ratings, counts, badges and the first 30 listings |
| `POST /api/v1/mercari/seller-reviews` | `jp` | 1 | The most recent 100 reviews of a Mercari Japan user: rating, text, date and role (as seller or as buyer), no reviewer names |
| `POST /api/v1/mercari/shop` | `jp` | 1 | A Mercari Shops shop (a business seller on Mercari Japan): profile, rating, review count, followers. No product list |

A not-found (an unknown or deleted id, or an id from the other market) is charged 1 credit; a failed call is not charged.

## Markets

Every endpoint takes `country`:

| `country` | Site | Currency | Language | Endpoints |
|---|---|---|---|---|
| `us` (default, except seller, seller-reviews and shop) | mercari.com | USD | English | search, item, category, categories, brands, brand, deals, trending |
| `jp` (default on seller, seller-reviews and shop) | jp.mercari.com | JPY | Japanese | search, item, category, categories, brands, brand, seller, seller-reviews, shop |

- Every answer echoes `country`, `currency` and `language`.
- Item, category, brand and seller ids are per market: a `us` id is not valid on `jp` (and the reverse). The call answers a charged `404`. Take ids from an answer of the same market.
- `jp` data is in Japanese as sellers wrote it: titles, descriptions, comments, review text, category and brand names. Nothing is translated. Prices are whole yen.
- On `jp`, Japanese keywords match best (`ポケモンカード`, not `pokemon cards`).
- Held back, answering `400` before anything is charged: `gb` / `uk` (Mercari UK closed), any other country, and an endpoint on a market it does not serve (deals and trending on `jp`; seller, seller-reviews and shop on `us`).
- Not available on `us`: seller profiles, seller reviews. Not available on either market: search suggestions. Do not offer them.

## Workflow

1. **Sold prices for a query:** `/search` with `query` and `status: "sold"` (on `us` add `sort: "recently_sold"`). Each item has `price`, `currency`, `status` (`sold` or `trading`), `condition`, `brand` and `url`. Narrow with `category_id`, `brand_id`, `condition` or a price range before summarising.
2. **Asking vs sold:** run the same body again with `status: "on_sale"` and compare the two price lists. Say which page(s) you read and the date.
3. **When it sold:** grids have no sold time. Call `/item` on the items you need: `sold_at` is when it sold, and the listing is complete (description, condition, shipping, likes, seller).
4. **Price drops:** `original_price` is the seller's earlier price when it is above `price`, with `discount_percent`. On `us`, `/deals` (or `deals_only: true` on search) lists only price-dropped listings.
5. **Ids:** `/categories` gives `category_id`s (on `us` walk down with `parent_id`; on `jp` one call returns the whole tree); `/brands` with `query` gives `brand_id`s. Use them on `/category`, `/brand` or as search filters, in the same market.
6. **Japan seller check:** `seller_id` from a `jp` search or item feeds `/seller` (ratings, counts, badges, first 30 listings) and `/seller-reviews` (the latest 100). A Mercari Shops product (`is_shop: true`) carries `shop_id`: `/shop` reads the shop; for its products use search with `shops_only: true` or `/item` on a product id.
7. **Trends (US):** `/trending` for rising keywords and brands, then search those keywords with `status: "sold"` to see what they sell for.

## Parameters

### Grid filters (search, category, brand; deals takes all but `deals_only`, `shops_only`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `us` | `us` or `jp` |
| `status` | string | `on_sale` | `on_sale`, `sold` (sold and in transit) or `all`. On `jp`, `all` applies no status filter (Mercari Japan's default: mostly on sale plus some in transit) |
| `sort` | string | `relevance` | `relevance`, `newest`, `price_asc`, `price_desc`; `recently_sold` on `us` only; `likes` on `jp` only. On `jp`, `newest` follows Mercari Japan's own order: a relisted or edited listing can rank above a newer one, so `created_at` is not strictly descending |
| `page` | integer | 1 | `us`: 1 to 20 (50 per page, 1,000 results); `jp`: 1 to 91 (120 per page) |
| `price_min` / `price_max` | number | none | US dollars on `us`; whole yen on `jp` |
| `condition` | string or list | all | One or more of `new`, `like_new`, `good`, `fair`, `poor`; `bad` on `jp` only. Several are ORed |
| `shipping` | string | all | `free` (the seller pays shipping) or `buyer_pays` |
| `size_id` | string | none | `us` only: a Mercari US size id |
| `deals_only` | boolean | false | `us` only: only listings whose price the seller dropped |
| `shops_only` | boolean | false | `jp` only: only Mercari Shops products (business sellers) |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Keywords, up to 200 chars. Required unless `category_id` or `brand_id` is sent |
| `category_id` | string | all | A category id of the same market (`/categories`) |
| `brand_id` | string | all | A brand id of the same market (`/brands`) |

### Item (`/item`)

Send exactly one of:

| Parameter | Type | Description |
|---|---|---|
| `item_id` | string | `m` and 11 digits (`m38943035688`), or on `jp` a 22-character Mercari Shops product id. Use with `country` |
| `url` | string | A Mercari item link: `https://www.mercari.com/us/item/<id>/`, `https://jp.mercari.com/item/<id>` or a `jp` `/shops/product/` link. Its market is used; a `country` that contradicts it answers `400` |

### Category (`/category`), brand (`/brand`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | required on `/category` | `us` `797` Consoles, `jp` `1289` ポケモンカードゲーム |
| `brand_id` | string | required on `/brand` | `us` `4591` Nintendo, `us` `1400` Coach, `jp` `539` COACH |
| `query` | string | none | Optional keywords within the category or brand |

Plus the grid filters; `/category` takes `brand_id` and `/brand` takes `category_id` as extra filters.

### Categories (`/categories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `parent_id` | string | none | A category id: its children. Without it, `us` answers the 17 top-level categories, `jp` the whole tree |

### Brands (`/brands`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | none | Filter by name (case-insensitive; on `jp` it also matches the katakana reading) |
| `page` | integer | 1 | Page of 1,000 brands |

### Deals (`/deals`)

`us` only. Optional `query`, `category_id`, `brand_id`, plus `status`, `page`, `sort`, `price_min`, `price_max`, `condition`, `shipping` and `size_id`.

### Trending (`/trending`)

`country` only (`us`).

### Seller (`/seller`), seller reviews (`/seller-reviews`)

`jp` only. Send exactly one of `seller_id` (digits, the `seller_id` of a `jp` search or item answer, `477123966`) or `url` (`https://jp.mercari.com/user/profile/<id>`).

### Shop (`/shop`)

`jp` only. Send exactly one of `shop_id` (22 letters and digits, `LThudSk3aoGvKcW6R3sA6m`) or `url` (`https://jp.mercari.com/shops/profile/<id>`).

## Examples

### Sold search

```bash
curl -X POST https://api.scavio.dev/api/v1/mercari/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "nintendo switch", "status": "sold", "sort": "recently_sold"}'
```

Captured `data` (us, 2026-11-16; 2 of 50 items and the notes shown):

```json
{
  "country": "us",
  "currency": "USD",
  "language": "en",
  "query": "nintendo switch",
  "status": "sold",
  "sort": "recently_sold",
  "page": 1,
  "page_size": 50,
  "max_page": 20,
  "total": 10000,
  "has_more": true,
  "filters": {},
  "count": 50,
  "items": [
    {
      "item_id": "m21161095301",
      "title": "Mortal Kombat 1 Nintendo Switch Game",
      "url": "https://www.mercari.com/us/item/m21161095301/",
      "price": 16,
      "original_price": null,
      "discount_percent": null,
      "currency": "USD",
      "status": "trading",
      "condition": "like_new",
      "condition_name": "Like new",
      "brand": { "brand_id": "4591", "name": "Nintendo" },
      "category_id": "796",
      "category": "Games",
      "size": null,
      "thumbnail": "https://u-mercari-images.mercdn.net/photos/m21161095301_1.jpg?1794670088&width=200&height=200",
      "seller_id": "175258609",
      "free_shipping": null,
      "created_at": "2026-11-14T15:28:08.000Z"
    },
    {
      "item_id": "m31816235781",
      "title": "The Legend of Zelda Breath of the Wild Nintendo Switch Game",
      "url": "https://www.mercari.com/us/item/m31816235781/",
      "price": 30,
      "original_price": 40,
      "discount_percent": 25,
      "currency": "USD",
      "status": "trading",
      "condition": "like_new",
      "condition_name": "Like new",
      "brand": { "brand_id": "4591", "name": "Nintendo" },
      "category_id": "796",
      "category": "Games",
      "size": null,
      "thumbnail": "https://u-mercari-images.mercdn.net/photos/m31816235781_1.jpg?1794369175&width=200&height=200",
      "seller_id": "548956637",
      "free_shipping": null,
      "created_at": "2026-11-11T03:14:17.000Z"
    }
  ],
  "notes": [
    "status sold returns sold items and items sold but still in transit (status trading).",
    "total is Mercari's own count, capped at 10,000 or 20,000; 50 items per page, 1,000 results reachable (page 20). Results carry no likes or sold time: the item endpoint has both."
  ]
}
```

`total` is Mercari's own capped count, not a market size. The Zelda listing sold at 30 USD after the seller dropped it from 40 (`original_price`).

### Item (a sold US listing)

```bash
curl -X POST https://api.scavio.dev/api/v1/mercari/item \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "m38943035688"}'
```

Captured `data` (us, 2026-11-16; `description` cut, 2 of 11 photos, `seller.name` and the notes dropped):

```json
{
  "country": "us",
  "currency": "USD",
  "language": "en",
  "item_id": "m38943035688",
  "title": "Coach Green Haversack Archive limited edition Bleeker suede COACH 12797",
  "description": "This beautiful bag is in pristine condition inside and out with no imperfections. ...",
  "url": "https://www.mercari.com/us/item/m38943035688/",
  "price": 3200,
  "original_price": 5000,
  "discount_percent": 36,
  "price_with_buyer_fee": 3644.24,
  "status": "sold",
  "sold_at": "2025-12-13T15:45:53.000Z",
  "condition": "like_new",
  "condition_name": "Like new",
  "brand": { "brand_id": "1400", "name": "Coach" },
  "category": {
    "category_id": "252",
    "name": "Shoulder Bags",
    "path": [
      { "category_id": "1", "name": "Women" },
      { "category_id": "21", "name": "Women's handbags" },
      { "category_id": "252", "name": "Shoulder Bags" }
    ]
  },
  "size": null,
  "color": null,
  "shipping": { "payer": "buyer", "method": null, "service": "UPS Ground Saver", "fee": 7.97, "days_to_ship": "2 - 8 days", "ships_from": "Texas" },
  "likes": 21,
  "in_carts": 0,
  "authenticated": true,
  "offers_allowed": false,
  "photos": [
    "https://u-mercari-images.mercdn.net/photos/m38943035688_1.jpg?1765615193",
    "https://u-mercari-images.mercdn.net/assessment_photos/m38943035688_86d6abfc-19a9-46c0-9de1-c1f0553158cc.jpg?"
  ],
  "created_at": "2025-12-11T16:55:39.000Z",
  "updated_at": "2025-12-19T21:07:17.000Z",
  "seller": {
    "seller_id": "164505055",
    "rating": 5,
    "review_count": 157,
    "listings_count": 141,
    "sold_count": 112,
    "joined": "2025-01-31T19:31:56.000Z",
    "badges": ["id_verified", "phone_verified", "email_verified"]
  }
}
```

The listing sold on 2025-12-13 and still reads in full eleven months later: sold at 3,200 USD after a drop from 5,000. `price_with_buyer_fee` is the price including Mercari US's buyer fee; shipping (`shipping.fee`, paid by the buyer here) is separate.

### Item (Mercari Japan, with comments)

```bash
curl -X POST https://api.scavio.dev/api/v1/mercari/item \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://jp.mercari.com/item/m65962821601"}'
```

Captured `data` (jp, 2026-11-16, 13.6 seconds; `description`, photos, `seller.name`, `seller.badges` and the notes dropped; 3 of 221 comments shown):

```json
{
  "country": "jp",
  "currency": "JPY",
  "language": "ja",
  "item_id": "m65962821601",
  "title": "ポケカ引退品",
  "url": "https://jp.mercari.com/item/m65962821601",
  "price": 1900000,
  "original_price": null,
  "discount_percent": null,
  "status": "on_sale",
  "sold_at": null,
  "condition": "new",
  "condition_name": "新品、未使用",
  "brand": null,
  "category": {
    "category_id": "1289",
    "name": "ポケモンカードゲーム",
    "path": [
      { "category_id": "1328", "name": "ゲーム・おもちゃ・グッズ" },
      { "category_id": "82", "name": "トレーディングカード" },
      { "category_id": "1289", "name": "ポケモンカードゲーム" }
    ]
  },
  "shipping": {
    "payer": "seller",
    "method": "らくらくメルカリ便",
    "service": null,
    "carrier": null,
    "fee": 0,
    "days_to_ship": { "min": 2, "max": 3, "label": "2~3日で発送" },
    "ships_from": "熊本県",
    "anonymous": true
  },
  "likes": 757,
  "comment_count": 221,
  "offers_allowed": false,
  "authentication_available": null,
  "hashtags": [],
  "created_at": "2026-07-28T13:59:09.000Z",
  "updated_at": "2026-11-11T11:29:44.000Z",
  "is_shop": false,
  "shop": null,
  "seller": {
    "seller_id": "845665200",
    "rating": 5,
    "ratings": { "good": 1, "normal": 0, "bad": 0 },
    "review_count": 1,
    "listings_count": 1,
    "quick_shipper": false,
    "is_official": false,
    "joined": "2022-07-06T21:58:50.000Z"
  },
  "comments": [
    { "text": "はい、本物です。", "date": "2026-11-14T06:15:27.000Z", "is_seller": true },
    { "text": "これは本物ですか？", "date": "2026-11-14T06:12:37.000Z", "is_seller": false },
    { "text": "バラ売り可能ですか？", "date": "2026-07-29T15:26:50.000Z", "is_seller": false }
  ]
}
```

`comments` is the full public list, newest first, with `is_seller` marking the seller's own replies (59 of the 221 here); who wrote each comment is not returned. Translate Japanese text for the user only when asked, and say it is your translation ("Is this genuine?" / "Yes, it is genuine." / "Can you sell them separately?").

### Seller and reviews (Mercari Japan)

```bash
curl -X POST https://api.scavio.dev/api/v1/mercari/seller \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"seller_id": "477123966"}'
```

Captured `data` (jp, 2026-11-16; `name`, `bio` and 2 of 3 badges dropped; 1 of 30 listings shown):

```json
{
  "country": "jp",
  "currency": "JPY",
  "language": "ja",
  "seller": {
    "seller_id": "477123966",
    "rating": 5,
    "ratings": { "good": 7250, "normal": 1, "bad": 1 },
    "review_count": 7252,
    "listings_count": 7203,
    "followers": 682,
    "following": 27,
    "is_official": false,
    "phone_verified": true,
    "joined": "2019-08-29T11:01:12.000Z",
    "badges": [
      { "id": "10002", "name": "24時間以内発送", "description": "発送までの平均時間が24時間以内の出品者" }
    ],
    "url": "https://jp.mercari.com/user/profile/477123966"
  },
  "listings": [
    {
      "item_id": "m42112434424",
      "title": "ハンドメイド用布タグ30枚",
      "url": "https://jp.mercari.com/item/m42112434424",
      "price": 330,
      "currency": "JPY",
      "status": "on_sale",
      "category_id": "1101",
      "thumbnail": "https://static.mercdn.net/thumb/item/jpeg/m42112434424_1.jpg?1794744310",
      "likes": 0,
      "comment_count": 0,
      "is_auction": false,
      "created_at": "2026-11-15T12:05:10.000Z",
      "updated_at": "2026-11-15T12:05:10.000Z"
    }
  ],
  "listings_has_more": true,
  "count": 30
}
```

The 30 `listings` are the first 30 the profile shows, on sale, in transit and sold (23 `on_sale`, 6 `sold`, 1 `trading` here); `listings_has_more` says there are more. The `24時間以内発送` badge reads "ships within 24 hours on average".

```bash
curl -X POST https://api.scavio.dev/api/v1/mercari/seller-reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"seller_id": "477123966"}'
```

Captured `data` (jp, 2026-11-16, 20 seconds; `name` dropped; 2 of 100 reviews shown):

```json
{
  "country": "jp",
  "currency": "JPY",
  "language": "ja",
  "seller_id": "477123966",
  "summary": { "rating": 5, "ratings": { "good": 7250, "normal": 1, "bad": 1 }, "review_count": 7252 },
  "reviews": [
    { "rating": "good", "text": "スムーズな対応ありがとうございました。また機会がありましたらよろしくお願いします。", "date": "2026-10-31T15:00:00.000Z", "role": "seller" },
    { "rating": "good", "text": "綺麗な状態で無事届きました。このたびは取引していただきありがとう御座いました。", "date": "2026-10-31T15:00:00.000Z", "role": "seller" }
  ],
  "has_more": true,
  "count": 100
}
```

`role` is the reviewed user's side of the deal: `seller` (98 of the 100 here) or `buyer` (2). All 100 were `good`, back to 2026-07-31, while `summary` counts 1 normal and 1 bad over 7,252 reviews: use `summary.ratings` for the all-time split. Every `date` here ends in `T15:00:00.000Z` (midnight in Japan): treat it as a day.

### Shop (Mercari Shops)

```bash
curl -X POST https://api.scavio.dev/api/v1/mercari/shop \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"shop_id": "LThudSk3aoGvKcW6R3sA6m"}'
```

Captured `data` (jp, 2026-11-16; `description` cut, notes dropped):

```json
{
  "country": "jp",
  "currency": "JPY",
  "language": "ja",
  "shop": {
    "shop_id": "LThudSk3aoGvKcW6R3sA6m",
    "name": "えびす堂",
    "description": "えびす堂＜Ebisudo＞へようこそ。...",
    "rating": 5,
    "review_count": 270,
    "followers": 50,
    "is_open": true,
    "has_time_sale": false,
    "badges": [],
    "thumbnail": "https://assets.mercari-shops-static.com/-/small/plain/vaiWyhk9CB6Q6u3u6nNDMc.png",
    "created_at": "2023-10-16T22:11:53.000Z",
    "url": "https://jp.mercari.com/shops/profile/LThudSk3aoGvKcW6R3sA6m"
  }
}
```

A shop answer has no product list. For a shop's products, search `jp` with `shops_only: true`, or call `/item` on one of its product ids (that answer lists some of the shop's other products).

### Trending (US)

```bash
curl -X POST https://api.scavio.dev/api/v1/mercari/trending \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "us"}'
```

Captured `data` (us, 2026-11-16; 2 of 20 keywords and 1 of 20 brands shown, `recent_listings` cut to 1):

```json
{
  "country": "us",
  "currency": "USD",
  "language": "en",
  "count": 40,
  "keywords": [
    { "position": 1, "keyword": "starbucks christmas tree cup", "search_rank": 75, "rank_change": 177995, "search_volume_change_percent": 16380, "trend": "trending_up" },
    { "position": 7, "keyword": "zelda switch 2 pro controller", "search_rank": 420, "rank_change": 1348, "search_volume_change_percent": 92.27, "trend": "trending_up" }
  ],
  "brands": [
    {
      "position": 1,
      "brand_id": "5292",
      "name": "Rainbow",
      "demand": "very_high",
      "demand_change": 1.3,
      "sold_rate_7d": 0.18874172185430463,
      "recent_listings": [
        { "item_id": "m93599479174", "title": "Women's Pride Rainbow Chevron Halter Bikini Swim Top Size L NWT", "url": "https://www.mercari.com/us/item/m93599479174/", "thumbnail": "https://u-mercari-images.mercdn.net/photos/m93599479174_1.jpg?1792665921&width=200&height=200" }
      ]
    }
  ]
}
```

`search_rank` is the keyword's current rank among Mercari searches, `rank_change` how far it climbed and `search_volume_change_percent` its search growth. `demand`, `demand_change` and `sold_rate_7d` are Mercari's own figures for the brand, as its trending page shows them: quote them as Mercari's, not as computed sales.

### Other endpoints (captured 2026-11-16)

- `/search` on `jp` with `{"country": "jp", "query": "ポケモンカード"}` (16.3 seconds): `page_size` 120, `max_page` 91, `total` 15000, 120 items, median price 4,155.5 JPY. `jp` items add `is_shop`, `shop_id`, `is_auction` and `updated_at`; first item `m32038141796` "ポケモンカード ミュウツーex FUR" at 400 JPY, `condition` `fair` (`condition_name` "やや傷や汚れあり"), `is_auction: true`.
- `/category` with `{"category_id": "797"}` (us): `category` `{"category_id": "797", "name": "Consoles"}`, 50 items, `filters` `{"category_id": "797"}`. On `jp`, `category.name` is `null`: take names from `/categories`.
- `/brand` with `{"brand_id": "4591"}` (us): `brand` `{"brand_id": "4591", "name": "Nintendo"}`, 50 items.
- `/deals` with `{}` (us): 50 items, `filters` `{"deals_only": true}`, every item with `original_price` above `price`, e.g. `m77098184688` "Bath & Body Works Ghost Halloween Wallflower Plug In" at 9 USD, `original_price` 15, `discount_percent` 40.
- `/categories` with `{"parent_id": "7"}` (us): 18 children of Electronics, each `{category_id, name, title, parent_id, level, has_children}`, e.g. `84` "Video games & consoles". The US tree is three levels deep.
- `/brands` with `{"query": "nike"}` (us): `brands_in_market` 28853, `total` 2: `{"brand_id": "4578", "name": "Nike"}`, `{"brand_id": "31861", "name": "Nike SB"}`.

### Python

```python
import statistics
import time
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def mercari(endpoint, body, timeout=240):
    r = requests.post(f"{BASE}/api/v1/mercari/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()["data"]

# Asking vs sold for one narrowed query on Mercari US (2 credits)
base = {"query": "nintendo switch oled", "category_id": "797", "condition": ["new", "like_new", "good"]}
on_sale = mercari("search", {**base, "status": "on_sale"})
sold = mercari("search", {**base, "status": "sold", "sort": "recently_sold"})

captured_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
for label, d in (("on sale", on_sale), ("sold", sold)):
    prices = [i["price"] for i in d["items"]]
    if prices:
        print(captured_at, label, len(prices), "items, median", statistics.median(prices), d["currency"])

# When did the first few sell? Grids carry no sold time; item does (1 credit each)
for it in sold["items"][:3]:
    full = mercari("item", {"item_id": it["item_id"]})
    print(full["status"], full["price"], full["sold_at"], full["url"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live. Every answer carries `country`, `currency` and `language`; `notes` explains anything market-specific.

- **Grid answer** (search, category, brand, deals) - `query`, `category` {`category_id`, `name`} (category), `brand` {`brand_id`, `name`} (brand), `status`, `sort`, `page`, `page_size` (50 / 120), `max_page` (20 / 91), `total` (Mercari's own count: capped at 10,000 or 20,000 on `us`, 15,000 on `jp`), `has_more`, `filters` (the filters applied), `count`, `items[]`, `notes`.
- **Grid item** - `item_id`, `title`, `url`, `price`, `original_price`, `discount_percent`, `currency`, `status` (`on_sale`, `trading`, `sold`), `condition` (`new`, `like_new`, `good`, `fair`, `poor`, `bad`), `condition_name` (Mercari's own label, Japanese on `jp`), `brand` {`brand_id`, `name`} or null, `category_id`, `size`, `thumbnail`, `seller_id`, `free_shipping`, `created_at`; `us` adds `category` (name); `jp` adds `is_shop`, `shop_id`, `is_auction`, `updated_at`. No likes, no sold time.
- **item** - the grid fields plus `description`, `sold_at`, `category` {`category_id`, `name`, `path[]`}, `color`, `shipping` {`payer`, `method`, `service`, `fee`, `days_to_ship`, `ships_from`}, `likes`, `offers_allowed`, `photos[]`, `updated_at`, `seller`. `us` adds `price_with_buyer_fee`, `in_carts`, `authenticated`, `shipping.ships_from` as a US state, and `seller` {`seller_id`, `name`, `rating`, `review_count`, `listings_count`, `sold_count`, `joined`, `badges[]` (`pro_seller`, `id_verified`, `phone_verified`, `email_verified`, `facebook_verified`)}. `jp` adds `comment_count`, `authentication_available`, `hashtags`, `shipping.carrier`, `shipping.anonymous`, `shipping.days_to_ship` {`min`, `max`, `label`}, `shipping.ships_from` as a prefecture, `is_shop`, `shop`, `comments[]` {`text`, `date`, `is_seller`}, and `seller` {`seller_id`, `name`, `rating`, `ratings` {`good`, `normal`, `bad`}, `review_count`, `listings_count`, `quick_shipper`, `is_official`, `joined`, `badges[]` {`id`, `name`, `description`}}. A `jp` Mercari Shops product (22-character id) answers `is_shop: true` with `stock` and `shop` {`shop_id`, `name`, `rating`, `review_count`, `url`, `other_products[]`}.
- **categories** - `parent_id`, `count`, `categories[]` {`category_id`, `name`, `parent_id`, `level`, `has_children`; `us` adds `title`}.
- **brands** - `query`, `page`, `page_size` (1,000), `total`, `brands_in_market`, `has_more`, `count`, `brands[]` {`brand_id`, `name`; `jp` adds `subname` and `reading`}.
- **trending** - `count`, `keywords[]` {`position`, `keyword`, `search_rank`, `rank_change`, `search_volume_change_percent`, `trend`}, `brands[]` {`position`, `brand_id`, `name`, `demand`, `demand_change`, `sold_rate_7d`, `recent_listings[]` {`item_id`, `title`, `url`, `thumbnail`}}.
- **seller** - `seller` {`seller_id`, `name`, `rating`, `ratings`, `review_count`, `listings_count`, `followers`, `following`, `is_official`, `phone_verified`, `joined`, `bio`, `badges[]`, `url`}, `listings[]` {`item_id`, `title`, `url`, `price`, `currency`, `status`, `category_id`, `thumbnail`, `likes`, `comment_count`, `is_auction`, `created_at`, `updated_at`}, `listings_has_more`, `count`.
- **seller-reviews** - `seller_id`, `name`, `summary` {`rating`, `ratings`, `review_count`}, `reviews[]` {`rating` (`good`, `normal`, `bad`), `text`, `date`, `role` (`seller`, `buyer`)}, `has_more`, `count`.
- **shop** - `shop` {`shop_id`, `name`, `description`, `rating`, `review_count`, `followers`, `is_open`, `has_time_sale`, `badges`, `thumbnail`, `created_at`, `url`}.

## Guardrails

- Sold prices: `status: "sold"` includes items sold but still in transit (`status: "trading"`); report both as sold. Say which query, filters, page and date a sold-price figure comes from, and never present the median of one mixed keyword page as the price of one product.
- `status: "on_sale"` prices are asking prices, not what items sold for. Keep the two apart in every summary.
- Grids have no sold time and no likes. Never estimate when something sold from `created_at`; call `/item` for `sold_at`.
- Search depth is fixed: `us` 50 per page up to page 20 (1,000 results), `jp` 120 per page up to page 91. `total` is Mercari's capped count. Never claim to have read every result or to know a market's size from `total`.
- On `jp`, `sort: "newest"` is Mercari Japan's own order (relisted or edited listings move up): sort by `created_at` yourself when strict order matters.
- Ids are per market. Never reuse a `us` id on `jp` or the reverse.
- `jp` text is Japanese as sellers wrote it and is not translated. If you translate, say so; never present a translation as Mercari's text. Prices on `jp` are yen: convert only when asked, with the rate and its date.
- `original_price` appears only when the seller's earlier price is above `price`. It is one earlier price, not a price history; there is no price history endpoint (poll and store).
- Not available, so do not offer them: US seller profiles and US seller reviews, search suggestions (either market), deals and trending on `jp`, a Mercari Shops product list on `/shop`, price history, buying, offers, messaging, or anything that posts or edits a listing.
- People: reviews and comments never carry who wrote them; do not try to identify reviewers or commenters. Seller `name` is the public display name: use seller data to judge a seller before a purchase, not to profile or contact a person.
- Terms: Mercari US's Prohibited Conduct policy says you may not use any robot, spider, crawler, scraper or other automated means not provided by Mercari to access the service or to extract data, and Mercari's global platform terms prohibit gathering the platform with a bot or scraper. This is not legal advice; read the current terms for your market and use case. Do not republish Mercari listing photos, seller names or avatars, or Mercari logos; link listings by `url` instead.
- Never fabricate prices, ids, sold times, ratings or comments. Only return what the API returned, with the `country`, `currency` and the listing `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: `gb` / `uk` ("Mercari UK closed; markets: us, jp."), another `country`, an endpoint on a market it does not serve ("deals is available for: us."), a filter on the wrong market (`size_id` or `deals_only` on `jp`, `shops_only` on `us`, `likes` sort on `us`, `recently_sold` on `jp`, `bad` condition on `us`), a `page` beyond 20 on `us` or 91 on `jp`, `price_min` above `price_max`, a non-whole yen price on `jp`, a missing `query` on search without `category_id` or `brand_id`, not exactly one of `item_id` / `url` (or `seller_id` / `url`, `shop_id` / `url`), a link of the wrong kind, or a `url` whose market contradicts `country`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Mercari US item ... was not found (deleted, or an id from another market: ids are per market).", "Mercari US category ... was not found (ids are per market).", "Mercari US brand ... was not found (ids are per market).", "Mercari Japan seller ... was not found.", "Mercari Shops shop ... was not found.". Take ids from a previous answer of the same market rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api).
- `502` means Mercari data was temporarily unavailable ("Mercari is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Mercari is busy ("Mercari is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- A client timeout shorter than the call (a `jp` search can take a minute) loses the answer: keep the timeout at 240 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.65.0
npm install scavio@0.66.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: sold } = await scavio.mercari.search({ query: "nintendo switch", status: "sold", sort: "recently_sold" });
const { data: item } = await scavio.mercari.item({ item_id: "m38943035688" });
const { data: cards } = await scavio.mercari.search({ country: "jp", query: "ポケモンカード" });
const { data: consoles } = await scavio.mercari.category({ category_id: "797", status: "sold" });
const { data: tree } = await scavio.mercari.categories({ parent_id: "7" });
const { data: brands } = await scavio.mercari.brands({ query: "nike" });
const { data: nintendo } = await scavio.mercari.brand({ brand_id: "4591" });
const { data: deals } = await scavio.mercari.deals({});
const { data: trending } = await scavio.mercari.trending({});
const { data: seller } = await scavio.mercari.seller({ seller_id: "477123966" });
const { data: reviews } = await scavio.mercari.sellerReviews({ seller_id: "477123966" });
const { data: shop } = await scavio.mercari.shop({ shop_id: "LThudSk3aoGvKcW6R3sA6m" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.mercari.search(...)`, `item`, `category`, `categories`, `brands`, `brand`, `deals`, `trending`, `seller`, `seller_reviews` and `shop`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all eleven endpoints as tools: `search_mercari`, `get_mercari_item`, `get_mercari_category`, `get_mercari_categories`, `get_mercari_brands`, `get_mercari_brand`, `get_mercari_deals`, `get_mercari_trending`, `get_mercari_seller`, `get_mercari_seller_reviews` and `get_mercari_shop`. Mercari is opt-in: add `mercari` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.64.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,mercari"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/mercari-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api), [item](https://scavio.dev/docs/mercari-item?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api), [category](https://scavio.dev/docs/mercari-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api), [categories](https://scavio.dev/docs/mercari-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api), [brands](https://scavio.dev/docs/mercari-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api), [brand](https://scavio.dev/docs/mercari-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api), [deals](https://scavio.dev/docs/mercari-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api), [trending](https://scavio.dev/docs/mercari-trending?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api), [seller](https://scavio.dev/docs/mercari-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api), [seller reviews](https://scavio.dev/docs/mercari-seller-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api), [shop](https://scavio.dev/docs/mercari-shop?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api). Overview: [Mercari API](https://scavio.dev/mercari-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api).
