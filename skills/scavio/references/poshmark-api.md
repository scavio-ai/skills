# Poshmark API - Sold Prices, Listings, Closets, Love Notes

Read Poshmark, the US and Canadian resale marketplace for fashion, home and beauty, on its two storefronts: Poshmark US (poshmark.com, USD) and Poshmark Canada (poshmark.ca, CAD). Search active or sold listings by keyword, browse a category or a brand, read one listing in full, read a closet (seller) with its listings and Love Notes, find closets by username, and look up the category tree, top brands, suggestions, Posh Parties and similar listings. All 15 endpoints return structured JSON at 1 credit per call.

**The job this skill is for: Poshmark sold prices.** Sold listings by keyword with the price shown on the sold listing and the date Poshmark marked it sold (`/sold`), filtered by brand, department, category, size, condition, colour and price; next to them, active listings for the same query with the original price the seller entered, the price the listing was first listed at and Poshmark's price-drop badge; and closets with their items-sold count and Love Notes.

Three limits shape every answer, so say them plainly:
- **480 sold listings per query and filter combination.** Poshmark shows at most 10 pages of 48 sold listings for one query and filter set. To reach more, split the question: narrow with brand, department, category, size, condition or colour, or run price bands with `price_min` / `price_max`. Never call one answer "all sold listings" or "every sale".
- **The sold price is the price shown on the sold listing.** Poshmark's help says a sold listing reflects the final order price; offers themselves are private and are not returned. Quote it with exactly that label.
- **About 5,000 active listings per query** (105 pages of 48). `total` is Poshmark's approximate count of matches and can be far larger than what any query reaches.

Poshmark has no public developer API for listings, sold prices or closets. Some sellers sync their own inventory and orders through an approved integration partner; that covers their own listings and orders, not marketplace search or sold prices. This skill reads the public marketplace instead, with one Scavio key.

See also: for Depop shop sold prices use `depop-api`; for Mercari sold prices use `mercari-api`; for Vinted listings use `vinted-api`; for eBay sold listings use `ebay-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price an item from Poshmark sold comps: what a brand, model, size or condition sold for on Poshmark US or Canada, and when
- Compare sold prices with what live listings for the same query ask, including price drops and the original price the seller entered
- Read one Poshmark listing from a link: description, condition, size and stock per size, shipping, bundle offer, likes, comments, and the seller's closet stats
- Check a Poshmark seller (closet) before buying: items sold, orders shipped, followers, Posh Ambassador status, last active, Love Notes count, and the latest Love Notes buyers left
- List a closet's listings for sale or its sold listings
- Browse a Poshmark category (for example Women > Bags) or a brand page (for example Coach), available or sold
- Resolve Poshmark category slugs, the top brands, or brand suggestions for a partial query
- See today's and recent Posh Parties and the listings shared to one party, or listings Poshmark shows as similar to one listing

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the build measurements search, sold, category and brand grids took 4-22 seconds, product 3-15 seconds, the other endpoints 1-16 seconds. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | Markets | What it returns |
|---|---|---|
| `POST /api/v1/poshmark/search` | us, ca | Listings for a query in one market, 48 per page (up to page 105), `availability` available (default), sold or all, with sorts, filters and `facets` (top 25 brands, colours, category counts) |
| `POST /api/v1/poshmark/sold` | us, ca | Sold listings for a query, 48 per page, up to page 10 (480 per query and filter combination): the price shown on the sold listing and `sold_at`, the date Poshmark marked it sold |
| `POST /api/v1/poshmark/product` | global | One listing by `listing_id` or link: description, status, `sold_at`, price, original price, first price, price drop, shipping, bundle offer, promotions, condition, category path, sizes with quantity available and sold, colours, pictures, likes, comments (no authors), dates, and the seller's closet stats |
| `POST /api/v1/poshmark/category` | us, ca | One department, category or subcategory, available, sold or all, 48 per page |
| `POST /api/v1/poshmark/brand` | us, ca | One brand's listings, optionally in one department and category, available, sold or all, 48 per page |
| `POST /api/v1/poshmark/closet` | global | A closet (seller) by username: home market, Posh Ambassador level, followers, following, listings, shares, items sold, orders shipped, Love Notes count, vacation hold, last active, joined |
| `POST /api/v1/poshmark/closet-listings` | global (read on the seller's home market) | A closet's listings, available (default) or sold, 48 per page |
| `POST /api/v1/poshmark/love-notes` | global | A closet's latest Love Notes, at most 100, with the closet's total: comment, date, listing id and picture. No buyer names |
| `POST /api/v1/poshmark/closets-search` | global | Closets whose username matches a query, 24 per page: username, URL, home market, joined |
| `POST /api/v1/poshmark/categories` | global | The category tree: 6 departments, 116 categories, 642 subcategories, each with id, name and slug |
| `POST /api/v1/poshmark/brands` | us, ca | Poshmark's top 50 brands (id, name) |
| `POST /api/v1/poshmark/suggestions` | us, ca | Brand and brand + category suggestions for a partial query |
| `POST /api/v1/poshmark/parties` | us, ca | Posh Parties of one market, upcoming and recent (20): name, type, status, start and end, listing count, theme, host usernames |
| `POST /api/v1/poshmark/party-listings` | us, ca | Listings shared to one Posh Party, 20 per page by cursor |
| `POST /api/v1/poshmark/similar` | us, ca | 16 listings Poshmark shows as similar to one listing, from the market asked |

## Credits

Every endpoint costs **1 credit per call** on `us` and `ca`. Each page is one call. A not-found (`404`: unknown listing, closet, category or brand) is charged; a `400` and an upstream failure (`502`, `503`) are not. Reading a closet's listings on the seller's home market when you asked the other market is still 1 credit.

## Markets

`country` is `us` (poshmark.com, USD, the default) or `ca` (poshmark.ca, CAD). Both storefronts are English (Poshmark Canada has no French storefront). Any other country answers `400` before anything is charged; Poshmark closed its Australia and India marketplaces.

- **Grids are per market.** Search, sold, category, brand, party listings and similar return only that market's listings, priced in its currency (`market` and `price.currency` on every item).
- **Listing ids and closets are global.** A `listing_id` opens from either market and answers in the listing's own market and currency (no conversion): the captured `ca` listing 6af9e2547049a1ea8b9d2617 answers `market: "ca"`, CAD 40. Closet profiles and Love Notes are the same record on both.
- **Closet listings live on the seller's home market.** `closet-listings` reads the closet where the seller sells (`market` in the answer is the home market) even when you ask the other one.
- **Party ids are per market.** Ask `party-listings` with the party's own market: another market's id answers a few unrelated listings, not a `404`.
- `closets-search` and `categories` return the same answer on both markets.

Captured 2026-11-18, the first item of each sold search (each row is a different listing):

| `country` | query | `price.amount` | `original_price` | `first_price` | `sold_at` |
|---|---|---|---|---|---|
| `us` | `coach bag` | USD 115 | null | 115 | 2026-11-17 |
| `ca` | `lululemon align` | CAD 25 | 84 | null | 2024-11-13 |

Sold results come in Poshmark's relevance order, so `sold_at` dates on one page can span years (the `ca` page above ran from 2024-11-13 to 2026-11-17). Filter or sort, and check `sold_at`, before calling a figure recent.

## Workflow

1. **Sold comps:** call `/poshmark/sold` with `query` and `country`. Each item has `price` (the price shown on the sold listing), `sold_at`, `condition`, `size`, `brand` and `url`.
2. **Narrow it:** read `facets` (top brands, colours, category counts with slugs) and search again with `brand`, `department` / `category` / `subcategory`, `size`, `condition`, `color` or `price_min` / `price_max`. Each narrowed query has its own 480-listing reach, which is how to cover more than 480 sales.
3. **Asking prices for the same query:** `/poshmark/search` with the same filters (`availability` available) gives what live listings ask, with `original_price`, `first_price` and `price_drop_percent`.
4. **Browse instead of search:** `/poshmark/categories` gives every department, category and subcategory `slug` (the inputs of category, search and sold); `/poshmark/brands` and `/poshmark/suggestions` give brand names for the `brand` filter and `/poshmark/brand`.
5. **Read a listing:** `/poshmark/product` with `listing_id` (or `url`) for the full listing and the seller's closet stats.
6. **Judge the seller:** `/poshmark/closet` (items sold, orders shipped, followers, last active, Love Notes count), `/poshmark/love-notes` (the latest 100 notes) and `/poshmark/closet-listings` with `availability: "sold"` for the closet's own sales.
7. **Price watching:** there is no price history. Poll the same query or listing on a schedule and store each answer with its date.

## Parameters

### Search (`/search`) and sold (`/sold`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `country` | string | `us` | `us` or `ca` |
| `page` | integer | 1 | 48 listings per page. Search: 1-105. Sold: 1-10 (a sold page above 10 answers `400`, not charged) |
| `availability` | string | `available` | Search only: `available`, `sold` or `all`. Sold ignores it (always sold listings) |
| `sort` | string | `relevance` | `relevance`, `just_shared`, `just_in` (newest listed), `price_asc`, `price_desc`, `price_drop` (recently price dropped), `most_liked` |
| `brand` | string or array | all | Brand names as Poshmark writes them (`items[].brand`, `/brands`, `/suggestions`), up to 10 |
| `department` | string | all | `Women`, `Men`, `Kids`, `Home`, `Pets`, `Electronics` |
| `category` | string | all | Category slug or name from `/categories` (`Bags`, `Pants_&_Jumpsuits`). Needs `department` |
| `subcategory` | string | all | Subcategory slug or name (`Totes`, `Leggings`). Needs `category` |
| `size` | string or array | all | Sizes as Poshmark writes them (`items[].size`: `10`, `M`, `OS`), up to 10 |
| `condition` | string | all | One of `new_with_tags`, `new_with_tags_or_boutique`, `boutique` (Boutique retail listings), `like_new`, `good`, `fair` |
| `color` | string or array | all | Up to 5 of `Red`, `Pink`, `Orange`, `Yellow`, `Green`, `Blue`, `Purple`, `Gold`, `Silver`, `Black`, `Gray`, `White`, `Cream`, `Brown`, `Tan` |
| `price_min` / `price_max` | number | none | Price range in whole units of the market's currency. `price_min` must not be above `price_max` |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `department` | string | required | `Women`, `Men`, `Kids`, `Home`, `Pets`, `Electronics` |
| `category`, `subcategory` | string | none | Slugs or names from `/categories` |
| `country`, `page`, `availability`, `brand`, `sort`, `size`, `condition`, `color`, `price_min`, `price_max` | | | As on search. With `availability: "sold"` pages stop at 10 |

### Brand (`/brand`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | required | One brand: its name (`Coach`, `lululemon athletica`) or slug (`items[].brand_slug`, `lululemon_athletica`) |
| `department`, `category` | string | none | Narrow to one department and category (no `subcategory`) |
| `country`, `page`, `availability`, `sort`, `size`, `condition`, `color`, `price_min`, `price_max` | | | As on search |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `listing_id` | string | one of | Listing id, 24 hex characters (`items[].listing_id`, `6ad80f0dce5b0ace7ee9abd7`) |
| `url` | string | one of | A poshmark.com or poshmark.ca listing link. Send exactly one of `listing_id`, `url` |
| `country` | string | `us` | Optional. The listing answers in its own market and currency either way |

### Closet (`/closet`), closet listings (`/closet-listings`), Love Notes (`/love-notes`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | required | Closet username (`poshmark.com/closet/<username>`, `items[].seller_username`) |
| `availability` | string | `available` | closet-listings only: `available` or `sold` |
| `page` | integer | 1 | closet-listings only: 48 listings per page |
| `country` | string | `us` | Optional; closets are global |

### Closets search (`/closets-search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Part of a closet username (1-100 chars) |
| `page` | integer | 1 | 24 closets per page, 1-200 |

### Categories (`/categories`) and brands (`/brands`)

Both take only `country` (optional). Categories are the same on both markets.

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars) |
| `country` | string | `us` | `us` or `ca` |

### Parties (`/parties`) and party listings (`/party-listings`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `status` | string | `all` | parties: `all`, `scheduled` (upcoming) or `archived` (ended) |
| `party_id` | string | required | party-listings: `parties[].party_id`. Send the party's own market as `country` |
| `cursor` | string | none | party-listings: `next_cursor` of the previous page |
| `country` | string | `us` | `us` or `ca` |

### Similar (`/similar`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `listing_id` | string | required | Listing id (`items[].listing_id`) |
| `country` | string | `us` | The market to read similar listings from; ask with the listing's own market |

## Examples

### Sold

```bash
curl -X POST https://api.scavio.dev/api/v1/poshmark/sold \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "coach bag"}'
```

Captured `data` (US, 2026-11-18, 1 credit; 1 of 48 items shown, facet lists cut to 2):

```json
{
  "market": "us",
  "currency": "USD",
  "query": "coach bag",
  "sort": "relevance",
  "availability": "sold",
  "filters": {},
  "page": 1,
  "page_size": 48,
  "total": 3539934,
  "has_more": true,
  "count": 48,
  "items": [
    {
      "listing_id": "6ae05a7756502b0b38c03a43",
      "url": "https://poshmark.com/listing/Coach-Shoulder-Bag-6ae05a7756502b0b38c03a43",
      "title": "Coach Shoulder Bag",
      "price": { "amount": 103, "currency": "USD" },
      "original_price": 325,
      "first_price": 115,
      "price_drop_percent": null,
      "size": "One Size",
      "brand": "Coach",
      "brand_slug": "Coach",
      "condition": "new_with_tags",
      "department": "Women",
      "category": "Bags",
      "subcategories": ["Shoulder Bags"],
      "colors": ["Pink"],
      "status": "sold",
      "sold_at": "2026-10-29T13:55:55-07:00",
      "picture_url": "https://di2ponv0v5otw.cloudfront.net/posts/2026/10/27/6ae05a7756502b0b38c03a43/m_6ae05ae6046d1f21b3d51196.jpg",
      "picture_count": 3,
      "like_count": 24,
      "comment_count": 0,
      "share_count": 5,
      "shipping_discount": null,
      "seller_username": "geliladaniel",
      "created_at": "2026-10-27T01:01:59-07:00",
      "updated_at": "2026-11-17T17:02:42-08:00",
      "market": "us"
    }
  ],
  "facets": {
    "brands": [{ "name": "Coach", "count": 4463585 }, { "name": "Michael Kors", "count": 10028 }],
    "colors": [{ "name": "Black", "count": 1253962 }, { "name": "Brown", "count": 894500 }],
    "categories": [
      { "department": "Women", "category": "Bags", "slug": "Bags", "count": 4503296 },
      { "department": "Women", "category": "Accessories", "slug": "Accessories", "count": 115567 }
    ]
  }
}
```

Read the item as: first listed at $115, the sold listing shows $103, marked sold on 2026-10-29; $325 is the original price the seller entered. `total` (3,539,934) is Poshmark's approximate count, not what the query reaches: 480 sold listings at most. On this captured page 28 of 48 items had a `first_price` above the sold price, 2 had one below it (sellers can raise a price), 4 had none, and 41 of 48 had no `original_price`.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/poshmark/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "lululemon align"}'
```

Captured on US (2026-11-18, 1 credit): 48 items in the sold item shape with `status: "available"` and `sold_at: null`, `total` 164,639. The first item asked $32 with `first_price` 40 and `original_price` 99 (`price_drop_percent` null). The same query on `ca` returned CAD prices with `total` 15,958. `price_drop_percent` is Poshmark's price-drop badge: on the US page 5 items carried it (10 to 27 percent) while 8 had a `first_price` above `price`, so read both.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/poshmark/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"listing_id": "6ad80f0dce5b0ace7ee9abd7"}'
```

Captured `data` (US, 2026-11-18, 1 credit; 4 of 5 pictures dropped):

```json
{
  "listing_id": "6ad80f0dce5b0ace7ee9abd7",
  "url": "https://poshmark.com/listing/Lululemon-Gray-Striped-Leggings-10-6ad80f0dce5b0ace7ee9abd7",
  "title": "Lululemon Gray Striped Leggings 10",
  "description": "Lululemon Gray Striped Leggings 10\n\nEUC. Shows no signs of wear. Super soft and stretchy. High rise. Capri fit. \n\nApproximate measurements-inseam 24’’; rise 10’’\n\nQuestions? Leave a comment below!",
  "status": "available",
  "sold_at": null,
  "market": "us",
  "price": { "amount": 25, "currency": "USD" },
  "original_price": 98,
  "first_price": 25,
  "price_drop_percent": null,
  "price_drop_text": null,
  "shipping": { "text": "$6.49 $4.99 Shipping", "price": 4.99, "discounted_from": 6.49 },
  "shipping_discount": "discounted",
  "bundle_discount": null,
  "promotions": ["Discounted shipping"],
  "brand": "lululemon athletica",
  "brand_slug": "lululemon_athletica",
  "condition": null,
  "department": "Women",
  "category": "Pants & Jumpsuits",
  "subcategories": ["Leggings"],
  "category_path": ["Women", "Pants & Jumpsuits", "Leggings"],
  "size": "10",
  "sizes": [{ "size": "10", "quantity_available": 1, "quantity_sold": 0 }],
  "multi_size": false,
  "colors": ["Gray", "White"],
  "style_tags": [],
  "pictures": ["https://di2ponv0v5otw.cloudfront.net/posts/2026/10/20/6ad80f0dce5b0ace7ee9abd7/l_6ad80f0e70333fa2b34d69f5.jpeg"],
  "video_count": 0,
  "like_count": 0,
  "comment_count": 0,
  "share_count": 21,
  "comments": [],
  "created_at": "2026-10-20T18:02:05-07:00",
  "published_at": "2026-10-20T18:02:11-07:00",
  "updated_at": "2026-11-18T00:27:02-08:00",
  "seller": {
    "username": "thecloverhill",
    "url": "https://poshmark.com/closet/thecloverhill",
    "home_market": "us",
    "posh_ambassador": "posh_ambassador_ii",
    "super_seller": false,
    "followers": 63350,
    "following": 125963,
    "listings": 2716,
    "shares": 1989954,
    "items_sold": "1700+",
    "orders_shipped": 1670,
    "love_notes": 169,
    "on_vacation": false,
    "last_active_at": "2026-11-17T21:04:14-08:00",
    "joined_at": "2021-02-24T16:00:13Z"
  },
  "detail": "full"
}
```

`condition` is `null` when the seller set none. `shipping.discounted_from` is the shipping before the seller's discount. `items_sold` is Poshmark's rounded display string ("1700+"), not a number; `orders_shipped` is a count. Comments come as `{text, created_at}` with no author, and @mentions of anyone but the seller are shown as `@user`. `detail` is `basic` when only the listing's core fields could be read (no comments, shipping or seller). Poshmark shows no ship-time figure, so none is returned.

### Closet

```bash
curl -X POST https://api.scavio.dev/api/v1/poshmark/closet \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"username": "thriftedbyher"}'
```

Captured `data` (2026-11-18, 1 credit):

```json
{
  "username": "thriftedbyher",
  "url": "https://poshmark.com/closet/thriftedbyher",
  "home_market": "us",
  "posh_ambassador": "posh_ambassador",
  "super_seller": false,
  "followers": 75444,
  "following": 2314,
  "listings": 1398,
  "shares": 6224,
  "items_sold": "700+",
  "orders_shipped": 637,
  "love_notes": 163,
  "on_vacation": false,
  "last_active_at": "2026-11-17T20:44:27-08:00",
  "joined_at": "2020-08-23T11:53:21Z",
  "description": null
}
```

`posh_ambassador` is `posh_ambassador`, `posh_ambassador_ii` or `null`, as the closet badge shows. `/closet-listings` with `{"username": "thriftedbyher"}` returned 48 of `total` 207 available listings on page 1 (`market: "us"`, `on_vacation: false`), in the sold item shape; `availability: "sold"` lists the closet's sold listings. A closet on vacation hold shows no available listings.

### Love Notes

```bash
curl -X POST https://api.scavio.dev/api/v1/poshmark/love-notes \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"username": "thriftedbyher"}'
```

Captured `data` (2026-11-18, 1 credit; 2 of 100 notes shown):

```json
{
  "username": "thriftedbyher",
  "count": 100,
  "total": 163,
  "complete": false,
  "notes": [
    {
      "comment": "Gorgeous bag in excellent condition!",
      "created_at": "2026-10-29T10:49:26-07:00",
      "listing_id": "6ad64824a1bf203e94ba1d5a",
      "picture_url": "https://di2ponv0v5otw.cloudfront.net/posts/2026/10/19/6ad64824a1bf203e94ba1d5a/m_6ad648276c35830bf71ab168.jpg"
    },
    {
      "comment": "Fast shipping and beautiful item ",
      "created_at": "2026-11-06T11:04:45-08:00",
      "listing_id": "5f496732ff7c5ae868f01903",
      "picture_url": "https://di2ponv0v5otw.cloudfront.net/posts/2020/08/28/5f496732ff7c5ae868f01903/m_5f496753275e555ac310c76a.jpg"
    }
  ]
}
```

Poshmark Love Notes are notes buyers leave with a 5-star rating, so there is no per-note rating. Poshmark shows only the latest 100, with no paging: `count` is what came back, `total` the closet's all-time Love Notes count, `complete` whether every note is in the answer. In the capture the 100 notes ran oldest first (2021-07-21 to 2026-11-13). No buyer is returned.

### Categories, brands and suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/poshmark/categories \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (2026-11-18, 1 credit; 1 of 6 departments, 1 of its 39 categories and 2 of 13 subcategories shown):

```json
{
  "count": 6,
  "category_count": 116,
  "subcategory_count": 642,
  "departments": [
    {
      "id": "000e8975d97b4e80ef00a955",
      "name": "Women",
      "slug": "Women",
      "categories": [
        {
          "id": "00248975d97b4e80ef00a955",
          "name": "Bags",
          "slug": "Bags",
          "subcategories": [
            { "id": "00d89287d97b4e80ef00a955", "name": "Baby Bags", "slug": "Baby_Bags" },
            { "id": "00da9287d97b4e80ef00a955", "name": "Backpacks", "slug": "Backpacks" }
          ]
        }
      ]
    }
  ]
}
```

The 6 departments are Women, Men, Kids, Home, Pets and Electronics. Slugs feed `department` / `category` / `subcategory` on search, sold, category and brand. `/brands` returned the top 50 (`{"id": "53d96e505632a028000002f4", "name": "Nike"}` first, then lululemon athletica, Free People, Zara, J. Crew); the full brand directory is not available, and `brand` takes any brand name. `/suggestions` with `{"query": "lulu"}` returned 10 brand suggestions such as `{"type": "brand", "text": "Lulu-B", "brand": "Lulu-B", "brand_id": "630fe1c395af634d54f87708", "category": null}`; when the query names one brand, Poshmark adds `brand_category` suggestions. Poshmark suggests brands, not free-text searches.

### Category and brand

```bash
curl -X POST https://api.scavio.dev/api/v1/poshmark/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"department": "Women", "category": "Bags"}'
```

Captured on US: 48 items, `total` 5000, with `department`, `category`, `subcategory` as Poshmark matched them. `/brand` with `{"brand": "Coach"}` answered `brand: {"id": "53d96e495632a02800000103", "name": "Coach"}`, `brand_slug` "Coach", 48 items, `total` 5000. On category and brand pages `total` is capped at 5000 (Poshmark gives no count there), and the facets are thinner: the captured brand answer had colours only, the category answer brands and colours but no category counts.

### Parties and party listings

```bash
curl -X POST https://api.scavio.dev/api/v1/poshmark/parties \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (US, 2026-11-18, 1 credit; 1 of 20 parties shown, hosts cut to 2):

```json
{
  "market": "us",
  "status": "all",
  "count": 20,
  "parties": [
    {
      "party_id": "6af4389627616c6274b38e4d",
      "url": "https://poshmark.com/party/6af4389627616c6274b38e4d",
      "name": "Cooler Weather Posh Party",
      "type": "style",
      "status": "scheduled",
      "start_time": "2026-11-18T19:00:00-08:00",
      "end_time": "2026-11-19T05:00:00.000Z",
      "listing_count": 0,
      "theme_brands": [],
      "theme_departments": [],
      "theme_categories": [],
      "hosts": ["pm_editor", "kreativekristen"],
      "market": "us"
    }
  ]
}
```

`type` is `style`, `department`, `category` or `brand`; the captured scheduled parties had `listing_count` 0. `/party-listings` with a `party_id` returns 20 listings per page in the item shape with `next_cursor` (ended parties still list).

### Closets search and similar

`/closets-search` with `{"query": "vintage"}` returned 24 closets per page such as `{"username": "juperitclothing", "url": "https://poshmark.com/closet/juperitclothing", "home_market": "us", "joined_at": "2019-03-20T22:20:03Z"}`; use `/closet` for a closet's stats. `/similar` with `{"listing_id": "6ad80f0dce5b0ace7ee9abd7"}` returned 16 listings in the item shape, from the market asked.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def poshmark(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/poshmark/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()["data"]

# 1. Sold comps for new-with-tags Coach bags in price bands, so each band has its own 480-listing reach
sold = []
for lo, hi in [(0, 50), (50, 100), (100, 200), (200, 1000)]:
    for page in range(1, 11):  # sold stops at page 10 (1 credit per page)
        d = poshmark("sold", {"query": "coach bag", "condition": "new_with_tags", "price_min": lo, "price_max": hi, "page": page})
        sold += d["items"]
        if not d["has_more"]:
            break
for s in sold[:20]:
    print(s["price"]["amount"], s["price"]["currency"], "sold", s["sold_at"][:10], s["title"], s["url"])

# 2. What live listings for the same query ask (1 credit)
live = poshmark("search", {"query": "coach bag", "condition": "new_with_tags", "sort": "price_asc"})
for it in live["items"][:10]:
    print(it["price"]["amount"], "first listed at", it["first_price"], "original price (seller-entered)", it["original_price"], it["url"])

# 3. Check the seller of the first live listing (1 credit each)
closet = poshmark("closet", {"username": live["items"][0]["seller_username"]})
notes = poshmark("love-notes", {"username": closet["username"]})
print(closet["items_sold"], closet["orders_shipped"], closet["love_notes"], notes["count"], "of", notes["total"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached.

- **listing item** (search, sold, category, brand, closet-listings, party-listings, similar) - `listing_id`, `url`, `title`, `price` {`amount`, `currency`}, `original_price` (the original price the seller entered, `null` when none), `first_price` (the price it was first listed at; above `price` after a drop, below it when the seller raised the price, `null` on some), `price_drop_percent` (Poshmark's price-drop badge), `size`, `brand`, `brand_slug` (`null` for free-text brands with no brand page), `condition`, `department`, `category`, `subcategories[]`, `colors[]`, `status` (`available`, `sold`, `not_for_sale`), `sold_at`, `picture_url`, `picture_count`, `like_count`, `comment_count`, `share_count`, `shipping_discount` (`free` / `discounted` when the seller offers it), `seller_username`, `created_at`, `updated_at`, `market`.
- **search / sold** - `market`, `currency`, `query`, `sort`, `availability`, `filters`, `page`, `page_size`, `total`, `has_more`, `count`, `items[]`, `facets` {`brands[]` (top 25) {`name`, `count`}, `colors[]` {`name`, `count`}, `categories[]` {`department`, `category`, `slug`, `count`}}.
- **category** - `department`, `category`, `subcategory` (as matched) and the search fields without `query`. **brand** - `brand` {`id`, `name`}, `brand_slug`, `department`, `category` and the same fields.
- **product** - `listing_id`, `url`, `title`, `description`, `status`, `sold_at`, `market`, `price`, `original_price`, `first_price`, `price_drop_percent`, `price_drop_text`, `shipping` {`text`, `price`, `discounted_from`}, `shipping_discount`, `bundle_discount` (the seller's bundle offer text), `promotions[]`, `brand`, `brand_slug`, `condition`, `department`, `category`, `subcategories[]`, `category_path[]`, `size`, `sizes[]` {`size`, `quantity_available`, `quantity_sold`}, `multi_size`, `colors[]`, `style_tags[]`, `pictures[]`, `video_count`, `like_count`, `comment_count`, `share_count`, `comments[]` {`text`, `created_at`}, `created_at`, `published_at`, `updated_at`, `seller` {`username`, `url`, `home_market`, `posh_ambassador`, `super_seller`, `followers`, `following`, `listings`, `shares`, `items_sold`, `orders_shipped`, `love_notes`, `on_vacation`, `last_active_at`, `joined_at`}, `detail` (`full` or `basic`).
- **closet** - the `seller` fields plus `description`.
- **closet-listings** - `username`, `market` (the seller's home market), `currency`, `availability`, `on_vacation`, `page`, `page_size`, `total`, `has_more`, `count`, `items[]`.
- **love-notes** - `username`, `count` (at most 100), `total`, `complete`, `notes[]` {`comment`, `created_at`, `listing_id`, `picture_url`}.
- **closets-search** - `query`, `page`, `total`, `has_more`, `count`, `closets[]` {`username`, `url`, `home_market`, `joined_at`}.
- **categories** - `count`, `category_count`, `subcategory_count`, `departments[]` {`id`, `name`, `slug`, `categories[]` {`id`, `name`, `slug`, `subcategories[]` {`id`, `name`, `slug`}}}.
- **brands** - `market`, `count`, `brands[]` {`id`, `name`}. **suggestions** - `market`, `query`, `count`, `suggestions[]` {`type` (`brand`, `brand_category`), `text`, `brand`, `brand_id`, `category`}.
- **parties** - `market`, `status`, `count`, `parties[]` {`party_id`, `url`, `name`, `type`, `status` (`scheduled`, `archived`), `start_time`, `end_time`, `listing_count`, `theme_brands[]`, `theme_departments[]`, `theme_categories[]` {`department`, `category`}, `hosts[]` (usernames), `market`}.
- **party-listings** - `market`, `currency`, `party_id`, `count`, `has_more`, `next_cursor`, `items[]`. **similar** - `market`, `listing_id`, `count`, `items[]`.

Condition values on items are the filter names (`new_with_tags`, `boutique`, `like_new`, `good`, `fair`), plus `not_new_with_tags` on some older listings and `null` when the seller set none.

## Guardrails

- Sold listings stop at 480 per query and filter combination (10 pages of 48). Never call one answer "all sold listings" or "every sale", and never present `total` as the number of sales returned. To cover more, run narrower slices (brand, category, size, condition, colour, price bands) and say how the sample was built.
- `price` on a sold listing is the price shown on the sold listing. Poshmark's help says it reflects the final order price; offers are private and not returned, so no separate offer amount exists in the answer. Quote it as the price shown on the sold listing, with the market and currency.
- `sold_at` is the date Poshmark marked the listing sold. Sold results come in relevance order unless sorted and can span years: check `sold_at` before calling a price recent.
- `original_price` is the original price the seller entered, not a retail price and not verified. `first_price` can be below `price` (the seller raised it) or `null`; never describe it as always higher.
- Active search reaches about 5,000 listings per query (page 105). `total` is approximate (it reads 10,000 on sorted queries; 5000 on category and brand pages).
- Love Notes: the latest 100 per closet, no paging; `total` is the closet's full count. Never call 100 notes all of them.
- `items_sold` is Poshmark's rounded display string ("700+"); do not do arithmetic on it. Use `orders_shipped` for a count.
- Prices are never converted. Grids answer in the market's currency; a listing read by id answers in its own market's currency. Convert explicitly, with the rate and its date, before comparing USD and CAD.
- An unknown category path or brand is a charged `404` (Poshmark itself would fall back silently): take slugs from `/categories` and brand names from `/brands`, `/suggestions` or `items[].brand`.
- Seller usernames are public listing data. Real names, display names, avatars, cities, likers, comment authors and Love Note buyers are never returned: never try to identify a buyer or commenter. Love Note text can name the seller; quote notes only to judge a seller before a purchase, not to profile or contact a person.
- Not available: sold results beyond 480 per query and filter combination, Love Notes beyond the latest 100, Posh Shows, trending searches, the full brand directory (top 50; any brand name works), offers, bundles, price history (poll and store), ship time. This API cannot buy, make offers, share, like, comment or manage listings.
- Terms: Scavio does not collect or store Poshmark data: each call fetches the public Poshmark page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Poshmark's terms of service cover how its service may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Poshmark listing photos or logos; link listings by `url` instead.
- Never fabricate prices, sold dates, listings, closet stats or Love Notes. Only return what the API returned, with the market, the currency and the listing `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` other than `us` / `ca` ("Poshmark has no storefront for this country ..."), a sold page above 10 (the message explains the 480 cap and how to narrow), a search page above 105, an unknown `sort`, `condition`, `color` or `department`, `category` without `department` or `subcategory` without `category`, `price_min` above `price_max`, both or neither of `listing_id` / `url`, a `url` that is not a Poshmark listing link, a `listing_id` that is not 24 hex characters, a `cursor` that is not a previous `next_cursor`, a party `status` other than `all` / `scheduled` / `archived`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Poshmark listing with this id.", "No Poshmark closet with this username.", "No Poshmark category with this path. Use the slugs or names from categories.", "No Poshmark brand page with this name. Use brands, suggestions or items[].brand_slug." An unknown party id answers `200` with no items. Take ids, usernames and slugs from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api).
- `502` means Poshmark data was temporarily unavailable ("Poshmark is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Poshmark is busy ("Poshmark is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.69.0
npm install scavio@0.70.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: sold } = await scavio.poshmark.sold({ query: "coach bag", condition: "new_with_tags" });
const { data: found } = await scavio.poshmark.search({ query: "lululemon align", country: "ca" });
const { data: item } = await scavio.poshmark.product({ listing_id: "6ad80f0dce5b0ace7ee9abd7" });
const { data: bags } = await scavio.poshmark.category({ department: "Women", category: "Bags" });
const { data: coach } = await scavio.poshmark.brand({ brand: "Coach", availability: "sold" });
const { data: closet } = await scavio.poshmark.closet({ username: "thriftedbyher" });
const { data: listings } = await scavio.poshmark.closetListings({ username: "thriftedbyher", availability: "sold" });
const { data: notes } = await scavio.poshmark.loveNotes({ username: "thriftedbyher" });
const { data: closets } = await scavio.poshmark.closetsSearch({ query: "vintage" });
const { data: tree } = await scavio.poshmark.categories({});
const { data: brands } = await scavio.poshmark.brands({});
const { data: typed } = await scavio.poshmark.suggestions({ query: "lulu" });
const { data: parties } = await scavio.poshmark.parties({ status: "scheduled" });
const { data: party } = await scavio.poshmark.partyListings({ party_id: "6af437b4ccaeb9c6a30f84a3" });
const { data: similar } = await scavio.poshmark.similar({ listing_id: "6ad80f0dce5b0ace7ee9abd7" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.poshmark.search(...)`, `sold`, `product`, `category`, `brand`, `closet`, `closet_listings`, `love_notes`, `closets_search`, `categories`, `brands`, `suggestions`, `parties`, `party_listings` and `similar`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all fifteen endpoints as tools: `search_poshmark`, `get_poshmark_sold`, `get_poshmark_product`, `get_poshmark_category`, `get_poshmark_brand`, `get_poshmark_closet`, `get_poshmark_closet_listings`, `get_poshmark_love_notes`, `search_poshmark_closets`, `get_poshmark_categories`, `get_poshmark_brands`, `get_poshmark_suggestions`, `get_poshmark_parties`, `get_poshmark_party_listings` and `get_poshmark_similar`. Poshmark is opt-in: add `poshmark` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.69.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,poshmark"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/poshmark-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [sold](https://scavio.dev/docs/poshmark-sold?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [product](https://scavio.dev/docs/poshmark-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [category](https://scavio.dev/docs/poshmark-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [brand](https://scavio.dev/docs/poshmark-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [closet](https://scavio.dev/docs/poshmark-closet?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [closet listings](https://scavio.dev/docs/poshmark-closet-listings?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [Love Notes](https://scavio.dev/docs/poshmark-love-notes?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [closets search](https://scavio.dev/docs/poshmark-closets-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [categories](https://scavio.dev/docs/poshmark-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [brands](https://scavio.dev/docs/poshmark-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [suggestions](https://scavio.dev/docs/poshmark-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [parties](https://scavio.dev/docs/poshmark-parties?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [party listings](https://scavio.dev/docs/poshmark-party-listings?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api), [similar](https://scavio.dev/docs/poshmark-similar?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api). Overview: [Poshmark API](https://scavio.dev/poshmark-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api).
