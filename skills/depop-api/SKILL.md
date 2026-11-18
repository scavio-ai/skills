---
name: depop-api
description: "Depop API for Depop resale prices: what Depop listings ask in each of its 9 storefronts (US, UK, Australia, Ireland, Canada, New Zealand, Germany, France, Italy), priced the way Depop shows them to a buyer in that market (listing price, original price, buyer fee, tax, shipping and the total; the currency is the listing's, and a few sellers list in another one), from keyword search, a category path, a brand page or a curated explore page with filters for brand, condition, colour, price range, marked-down, gender, group and product type, kids and size, sorted by relevance or price, with facet counts. Search, category, brand and explore return the first 24 results per query, sort and filter set: Depop serves no next page, so narrow with filters or a price range. One listing in full by slug, link or product id with description, hashtags, condition, sizes, shipping, likes, markdown, the buyer-market price and the seller's own listing price, and the seller summary (rating, reviews, items sold, last seen). A shop's profile (rating, review total, items sold, followers, listings per category), its listings for sale and its sold listings with the price they sold at and any markdown, cursor-paged 24 at a time (Depop shows no sale date, only when the listing last changed), and the reviews it received as a seller or buyer (no reviewer names). Plus shop search by username, the category tree with names in English, German, French or Italian, the brand list, search suggestions and similar listings (US). 14 endpoints, 1 credit per call; product 2 outside the US; New Zealand 5, product 6. Not available: keyword sold search (sold prices come per shop), results past the first 24, views, join date, price history (poll and store). Depop's Selling API is private, for high-volume sellers and partners managing their own listings and orders, with no marketplace search."
version: 1.0.0
tags: depop, depop-api, depop-prices, depop-price-check, depop-resale-prices, depop-sold, depop-sold-prices, depop-sold-items, depop-search, depop-listings, depop-shop, depop-seller, depop-seller-reviews, depop-reviews, depop-brands, depop-categories, depop-scraper, depop-vs-vinted, resale, reseller, resale-prices, secondhand-fashion, second-hand, vintage, streetwear, y2k, marketplace, fashion, clothing, multi-country, seller-reputation, price-research, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/docs/depop-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api
---

# Depop API - Listings, Shop Sold Prices, Seller Reviews

Read Depop, the second-hand fashion marketplace, in its 9 storefronts: search listings, browse a category, a brand or a curated explore page, read one listing in full, read a shop's profile, its listings for sale, its sold listings and its reviews, find shops by username, and look up the category tree, brands, search suggestions and similar listings. All 14 endpoints return structured JSON. Most calls cost 1 credit; product costs 2 outside the US, and New Zealand costs more (see Credits).

**The job this skill is for: Depop resale prices.** What Depop listings ask in each storefront, priced the way Depop shows them to a buyer there (listing price, buyer fee, tax and shipping, and the total), and what a shop's items sold for (`/shop-sold`: the sold price and any markdown). Shop profiles add the rating, review count and items sold.

Two limits shape every answer, so say them plainly:
- **First 24 results.** Search, category, brand and explore return the first 24 results for a query, sort and filter set. Depop serves no next page. To see more listings, split the question: narrow with filters (brand, condition, colour, group or product type), a price range or the other sort, and run each slice.
- **Sold prices come per shop.** Depop has no keyword search of sold listings, so there are no marketplace-wide sold comps. `/shop-sold` returns one shop's sold listings with the price they sold at; Depop shows no sale date (`updated_at` is when the listing last changed).

Depop's own Selling API is private: it is for high-volume sellers and partners (access by emailing Depop for a key) and covers the partner's own listings, orders and offers. It has no marketplace search and no other sellers' listings, sold items or reviews. This skill reads the public marketplace instead, with one Scavio key.

See also: for Vinted listings and seller reviews use `vinted-api`; for Mercari sold prices use `mercari-api`; for eBay listings use `ebay-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price an item on Depop: what live listings for a brand, model or size ask in one storefront, with the buyer fee and shipping
- Compare what the same kind of item asks across Depop storefronts (US, UK, Australia, the EU markets)
- See what a Depop shop has sold and for how much, including markdowns
- Check a Depop seller before buying: rating, review count, items sold, last seen, and the reviews buyers left
- Read one Depop listing from a link: description, hashtags, condition, sizes, shipping, likes, price breakdown and the seller summary
- Browse a Depop category (for example men's jeans), a brand page or a curated explore page (for example '90s Menswear)
- Resolve Depop category paths, group and product type ids, brand slugs and ids, or size filter values
- Get Depop's search suggestions for a partial query, or listings Depop shows as similar to one listing (US)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 1 credit (see Credits for the exceptions).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Shop, categories, brands, suggestions and similar calls take 1-5 seconds. Search, category, brand, explore and product calls can take up to about a minute outside the US (and sometimes on the US); allow a client timeout of at least 180 seconds.

| Endpoint | Markets | What it returns |
|---|---|---|
| `POST /api/v1/depop/search` | all 9 | The first 24 listings for a query in one buyer market: product id, slug, URL, title, description, brand, category, group, product type, status, seller country, pictures, sizes, condition, colours, gender, kids, likes, boosted, discounted, discount percentage and the buyer-market `price` breakdown. Plus `total_count` (Depop's approximate count) and `facets` (counts per department, group, product type, brand, colour, condition, size) |
| `POST /api/v1/depop/product` | all 9 | One listing by slug, link or product id, priced for a buyer in the market: description, hashtags, brand, category with breadcrumbs, condition, colours, sizes (sold sizes included), gender, pictures, likes, quantity, shipping (method, parcel size, payer, free shipping, national cost), discount, `price` (buyer market) and `listing_price` (the seller's own currency and price), and the seller (username, verified, country, rating, review total, items sold, last seen, average shipping days) |
| `POST /api/v1/depop/category` | all 9 | The first 24 listings of one category path (`mens/bottoms/jeans`) |
| `POST /api/v1/depop/brand` | all 9 | The first 24 listings of one brand by slug (`carhartt`) |
| `POST /api/v1/depop/explore` | all 9 | One of Depop's curated explore pages (`90s-menswear`): title, the search it runs, the first 24 listings and the market's other explore page slugs |
| `POST /api/v1/depop/suggestions` | all 9 | Search suggestions for a partial query, each with its group, gender and Depop's filter label ("in Men's Bottoms") |
| `POST /api/v1/depop/shop` | global | A shop by username or shop id: bio, verified, followers, following, rating, review total, seller and buyer rating counts, items sold, last seen, listings per department and category |
| `POST /api/v1/depop/shop-products` | global | A shop's listings for sale, up to 24 per page, cursor-paged, with `created_at` and `updated_at` |
| `POST /api/v1/depop/shop-sold` | global | A shop's sold listings with the price they sold at and any markdown, up to 24 per page, cursor-paged, with `created_at` and `updated_at` (no sale date) |
| `POST /api/v1/depop/shop-reviews` | global | Reviews a shop received as a seller (default) or as a buyer, 24 per page: date, rating, text and the product (id, image). No reviewer names |
| `POST /api/v1/depop/shops-search` | global | Shops whose username matches a query: shop id, username, URL |
| `POST /api/v1/depop/categories` | global | The category tree: departments > groups > product types, each with id, name and path; names in `en`, `en-US`, `de`, `fr` or `it`; optional size sets |
| `POST /api/v1/depop/brands` | global | Brands by first letter (id, name, slug), or one brand by slug with its description |
| `POST /api/v1/depop/similar` | us | Listings Depop shows as similar to one listing, for a US buyer |

## Credits

| Endpoint | `us` | `gb`, `au`, `ie`, `ca`, `de`, `fr`, `it` | `nz` |
|---|---|---|---|
| search, category, brand, explore | 1 | 1 | 5 |
| product | 1 | 2 | 6 |
| suggestions | 1 | 1 | 1 |
| shop, shop-products, shop-sold, shop-reviews, shops-search, categories, brands | 1 (global, no `country`) | | |
| similar | 1 (`us` only) | | |

Each shop-products, shop-sold or shop-reviews page is one call. A not-found (`404`) is charged; a `400` and an upstream failure (`502`, `503`) are not.

## Markets

`country` is the **buyer's** country (default `us`): `us` (USD), `gb` (GBP; `uk` is accepted), `au` (AUD), `ie` (EUR), `ca` (CAD), `nz` (NZD), `de` (EUR), `fr` (EUR), `it` (EUR). Any other country answers `400` before anything is charged.

- **Search shows that market's sellers.** On every captured non-US search for `levis 501` (2026-11-18), all 24 items had `seller_country` equal to the market.
- **Listing ids and slugs are global**: one `slug` or `product_id` opens the same listing from any market. The price changes with the market: a buyer in another country sees that market's buyer fee, tax (for example `tax_type: "UK_IMPORT_VAT"` for a UK buyer of a listing from abroad) and international shipping (`shipping_boundary: "international"`). Quote the market with every price.
- **Currency is the listing's.** `price.currency` is the currency the seller listed in, usually the market's, but some sellers list in another one: on the captured `fr` search 1 of 24 items was priced in USD, on `it` 2 of 24. Never add up or compare prices across currencies without converting and stating the rate and its date.
- **Language.** Depop's interface is English in every storefront. Titles and descriptions are what sellers wrote, often in German, French or Italian on `de`, `fr` and `it` (the captured `fr` product begins "Marque : Levi's Modèle : 501"). `/categories` returns group and product type names in `en`, `en-US`, `de`, `fr` or `it`; department names stay English.
- Shop, shop-products, shop-sold, shop-reviews, shops-search, categories and brands are global: they take no `country`. Shop listing prices carry the buyer fee, tax and shipping of a US buyer view.

Captured 2026-11-18: the first market-local listing of each market's `levis 501` search, read with `/product` in that market (each row is a different listing):

| `country` | credits | `price.currency` | `price` | `original_price` | `buyer_fee` | `shipping` | `total` | `headline_price` |
|---|---|---|---|---|---|---|---|---|
| `us` (1002884801) | 1 | USD | 3.6 | 6 | 0.88 | 5.99 | 10.47 | 4.48 |
| `gb` (999630334) | 2 | GBP | 15 | 15 | 1.45 | 2 | 18.45 | 18.45 |
| `au` (1000857330) | 2 | AUD | 60 | 60 | 3.7 | 10 | 73.7 | 73.7 |
| `ie` (980192162) | 2 | EUR | 25.5 | 30 | 0 | 6 | 31.5 | 25.5 |
| `ca` (1004916694) | 2 | CAD | 20 | 20 | 0 | 10 | 30 | 20 |
| `nz` (1004240623) | 6 | NZD | 25 | 25 | 0 | 10 | 35 | 25 |
| `de` (1005057718) | 2 | EUR | 20 | 20 | 0 | 5 | 25 | 20 |
| `fr` (996937442) | 2 | EUR | 32 | 32 | 0 | 5 | 37 | 32 |
| `it` (954045052) | 2 | EUR | 22 | 22 | 0 | 6.9 | 28.9 | 22 |

`tax` was 0 on every row (all domestic listings). `total` is price plus buyer fee, tax and shipping. `headline_price` is the figure Depop headlines and can leave out shipping (US: 3.6 + 0.88 = 4.48; UK: 15 + 1.45 + 2 = 18.45). On the captured `gb` and `au` searches all 24 items carried a buyer fee.

## Workflow

1. **Search:** call `/depop/search` with `query` and `country`. Each item has `product_id`, `slug`, `url`, the `price` breakdown and `seller_country`.
2. **Narrow it:** read `facets` (counts by group, product type, brand id, colour, condition, size) and search again with `brand_ids`, `conditions`, `colors`, `group` / `product_type`, `price_min` / `price_max`, `on_sale` or `size`. Each narrowed call returns a different first 24.
3. **Browse instead of search:** `/depop/categories` gives each category's `path` (the input of `/depop/category`) and the group and product type ids (search filters). `/depop/brands` gives each brand's `slug` (the input of `/depop/brand`) and `id` (the `brand_ids` filter).
4. **Read a listing:** `/depop/product` with the `slug` (or `url`, or `product_id`) and the buyer's `country` for the full listing, the buyer-market price and the seller summary.
5. **Sold prices:** the listing's `seller.username` (or `seller.id`) feeds `/depop/shop-sold`; page with `cursor: next_cursor` while `has_more` is true. Group sold items by brand and product type before quoting a typical sold price, and say these are one shop's sales.
6. **Judge the seller:** `/depop/shop` (rating, review total, items sold, last seen) and `/depop/shop-reviews` (what buyers wrote, newest first).
7. **Price watching:** there is no price history. Poll the same query or listing on a schedule and store each answer with its date.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `country` | string | `us` | Buyer market, one of the 9 above (`uk` = `gb`) |
| `sort` | string | `relevance` | `relevance`, `price_asc` or `price_desc`. Newest and most popular are not available |
| `brand_ids` | array or string | all | Brand ids from `/brands` or `facets.brands[].id` (Levi's `31`, Carhartt `1673`), up to 20 |
| `conditions` | array or string | all | `brand_new`, `used_like_new`, `used_excellent`, `used_good`, `used_fair` |
| `colors` | array or string | all | `black`, `blue`, `brown`, `burgundy`, `cream`, `gold`, `green`, `grey`, `khaki`, `multi`, `navy`, `orange`, `pink`, `purple`, `red`, `silver`, `tan`, `white`, `yellow` |
| `price_min` / `price_max` | number | none | Listing price range in the market's currency. `price_min` must not be above `price_max` |
| `on_sale` | boolean | none | Only listings the seller marked down (`discounted: true` in the answer) |
| `gender` | string | all | `male`, `female` or `unisex` |
| `group` | string | all | Group id from `/categories` (`tops`, `bottoms`, `footwear`) |
| `product_type` | array or string | all | Product type ids from `/categories` (`jeans`, `hoodies`) |
| `kids` | boolean | none | Only kids' listings (`true`) or none (`false`) |
| `size` | array or string | all | Size filter values `size_set_id.size_id` (`facets.sizes[].id` such as `60.19`, or `/categories` with `include_sizes`). Depop honours it only partly: check `sizes` on the items |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category` | string or array | required | A path from `/categories`: department[/group[/product_type]], departments `mens`, `womens`, `kids`, `everything-else` (`mens/bottoms/jeans`, `womens/tops`, `kids`) |
| `country`, `sort`, `brand_ids`, `conditions`, `colors`, `price_min`, `price_max`, `on_sale`, `size` | | | As on search. `group`, `product_type` and `kids` come from the path (sending them is a `400`); `gender` is a filter on `kids` paths only |

### Brand (`/brand`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `slug` | string | required | Brand slug from `/brands` or `items[].brand.slug` (`carhartt`, `levi-s`, `nike`) |
| `country`, `sort` and the search filters | | | As on search, without `brand_ids` (the slug sets the brand) |

### Explore (`/explore`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `slug` | string | required | An explore page slug (`90s-menswear`, `90s-womenswear`, `holiday-gifts`, `fall-trends-2026`). Every answer lists the market's other pages in `more_slugs`; some are market-specific (`denim-everything-mw-us`) |
| `country` | string | `us` | As on search |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `slug` | string | one of | Listing slug (`items[].slug`, `f0omem-levis-550-38x36-blue-jeans-662f`) |
| `url` | string | one of | A depop.com product link (`https://www.depop.com/products/<slug>/`; a `/gb/` or other prefix is fine, the market is `country`, not the link) |
| `product_id` | integer or string | one of | Product id (`items[].product_id`) |
| `country` | string | `us` | Buyer market. Send exactly one of `slug`, `url`, `product_id` |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars) |
| `country` | string | `us` | Buyer market; it shifts the ranking slightly |

### Shop (`/shop`), shop products (`/shop-products`), shop sold (`/shop-sold`), shop reviews (`/shop-reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | one of | Shop username (`depop.com/<username>/`, `flomem`) |
| `shop_id` | integer or string | one of | Shop id (`shop_id` of `/shop`, `seller.id` of `/product`). Send exactly one of `username`, `shop_id` |
| `cursor` | string | none | shop-products and shop-sold: `next_cursor` of the previous page |
| `limit` | integer | 24 | shop-products and shop-sold: listings per page, 1-24 |
| `role` | string | `seller` | shop-reviews: `seller` (reviews the shop got from buyers) or `buyer` (reviews it got from sellers) |
| `page` | integer | 1 | shop-reviews: page, 24 reviews each, 1-200 |

### Shops search (`/shops-search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Part of a shop username (1-100 chars) |

### Categories (`/categories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `language` | string | `en` | Names of groups and product types: `en`, `en-US`, `de`, `fr`, `it`. Department names stay English |
| `include_sizes` | boolean | false | Add `size_sets` (size systems and their size filter values). Larger answer |

### Brands (`/brands`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `letter` | string | one of | First letter `a`-`z`, or `0-9` for brands starting with a digit or symbol |
| `slug` | string | one of | One brand by slug, with its description. Send exactly one of `letter`, `slug` |

### Similar (`/similar`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | integer or string | required | Product id (`items[].product_id`, `1002884801`) |
| `country` | string | `us` | `us` only |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/depop/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "levis 501"}'
```

Captured `data` (US, 2026-11-18, 1 credit; 1 of 24 items shown, facet lists cut to 2, notes dropped):

```json
{
  "query": "levis 501",
  "country": "us",
  "currency": "USD",
  "sort": "relevance",
  "filters": {},
  "items": [
    {
      "product_id": 1003275593,
      "slug": "gbgaskiv0-levis-501-dark-wash-jeans-8813",
      "url": "https://www.depop.com/products/gbgaskiv0-levis-501-dark-wash-jeans-8813/",
      "title": "Levi's 501 dark wash jeans",
      "description": "Levi's 501 dark wash jeans\nSize 30x32\nHave taken the tags off to try on but never been worn or washed. \n#levis #levis501 #menswear #jeans #denim",
      "brand": { "id": 31, "name": "Levi's", "slug": "levi-s" },
      "category": "Jeans",
      "group": "bottoms",
      "product_type": "jeans",
      "status": "on_sale",
      "seller_country": "us",
      "pictures": [
        "https://media-photos.depop.com/r1/246425927/5238161359_f99f633173f94f63bd5664a2fecae959/P0.jpg",
        "https://media-photos.depop.com/r1/246425927/5238162256_6e49777bff2149608bd9305db99d0d51/P0.jpg",
        "https://media-photos.depop.com/r1/246425927/5238162462_377aba5fc4b84847a56a13f054035b6a/P0.jpg"
      ],
      "picture_count": 5,
      "sizes": [{ "id": 13, "name": "30\"", "quantity": 1, "status": "on_sale" }],
      "condition": "used_like_new",
      "colors": ["navy", "blue"],
      "gender": "male",
      "kids": false,
      "like_count": 16,
      "boosted": false,
      "discounted": false,
      "discount_percentage": null,
      "price": {
        "currency": "USD",
        "price": 11,
        "original_price": 11,
        "buyer_fee": 0,
        "tax": 0,
        "tax_type": null,
        "shipping": 5.99,
        "shipping_boundary": "national",
        "total": 16.99,
        "headline_price": 11
      }
    }
  ],
  "count": 24,
  "total_count": 8986,
  "facets": {
    "total": 8987,
    "departments": [
      {
        "id": "menswear",
        "count": 4983,
        "groups": [{ "id": "bottoms", "count": 4944 }, { "id": "tops", "count": 23 }],
        "product_types": [{ "id": "jeans", "count": 4770 }, { "id": "shorts", "count": 147 }]
      }
    ],
    "brands": [{ "id": 31, "count": 8773 }, { "id": 1667, "count": 125 }],
    "colors": [{ "id": "blue", "count": 6563 }, { "id": "navy", "count": 1898 }],
    "conditions": [{ "id": "used_excellent", "count": 4126 }, { "id": "used_good", "count": 2403 }],
    "sizes": [{ "id": "60.19", "count": 793 }, { "id": "60.17", "count": 653 }]
  }
}
```

Read an item as: the seller asks $11.00, a US buyer pays $5.99 shipping, total $16.99. `count` is 24 (the first 24 results); `total_count` (8,986) is Depop's approximate count of matches, not what the answer holds. `total_count` can be off on small result sets: the captured `de` and `ie` searches returned 24 items with `total_count: 4`. Only `/search` carries `facets`; category, brand and explore return `facets: null`. `pictures` holds the first 3 photos, `picture_count` all of them.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/depop/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "f0omem-levis-550-38x36-blue-jeans-662f"}'
```

Captured `data` (US, 2026-11-18, 1 credit; 4 of 5 pictures and the notes dropped):

```json
{
  "product_id": 1002884801,
  "slug": "f0omem-levis-550-38x36-blue-jeans-662f",
  "url": "https://www.depop.com/products/f0omem-levis-550-38x36-blue-jeans-662f/",
  "status": "on_sale",
  "title": "Levi's Men's Blue Jeans",
  "description": "Levi's 550 38x36 blue jeans #denim #classic #levis",
  "hashtags": ["denim", "classic", "levis"],
  "brand": { "id": 31, "name": "Levi's", "slug": "levi-s" },
  "category": {
    "group": "bottoms",
    "group_name": "Bottoms",
    "product_type": "jeans",
    "product_type_name": "Jeans",
    "breadcrumbs": [
      { "name": "Men", "path": "mens" },
      { "name": "Bottoms", "path": "mens/bottoms" },
      { "name": "Jeans", "path": null }
    ]
  },
  "condition": { "id": "used_good", "name": "Good condition" },
  "colors": [{ "id": "blue", "name": "Blue" }],
  "sizes": [{ "id": 21, "name": "38\"", "quantity": 1, "status": "on_sale" }],
  "gender": "male",
  "kids": false,
  "pictures": ["https://media-photos.depop.com/b1/46847613/5235755231_c6ff290c2c254e70b62b2ff446d81fa8/P0.jpg"],
  "picture_count": 5,
  "like_count": 1,
  "boosted": false,
  "quantity": 1,
  "shipping": {
    "method": "USPS",
    "parcel_size": "medium",
    "payer": "buyer",
    "free_shipping": false,
    "national_cost": 5.99,
    "confidence": "high"
  },
  "discounted": true,
  "discount_percentage": 40,
  "price": {
    "currency": "USD",
    "price": 3.6,
    "original_price": 6,
    "buyer_fee": 0.88,
    "tax": 0,
    "tax_type": null,
    "shipping": 5.99,
    "shipping_boundary": "national",
    "total": 10.47,
    "headline_price": 4.48
  },
  "listing_price": { "currency": "USD", "price": 3.6, "original_price": 6 },
  "seller": {
    "id": 46847613,
    "username": "flomem",
    "url": "https://www.depop.com/flomem/",
    "verified": false,
    "country": "us",
    "reviews_rating": 4.9,
    "reviews_total": 123,
    "items_sold": 952,
    "last_seen": "active_this_week",
    "average_shipping_days": 2
  },
  "country": "us",
  "currency": "USD"
}
```

The seller marked it down 40% from $6.00 to $3.60 (`discounted`, `original_price`, `discount_percentage`). `price` is what a buyer in `country` sees; `listing_price` is the seller's own currency and price, and differs from `price.currency` when the buyer market is another country. `shipping.method`, `parcel_size` and `payer` were `null` on every captured non-US product; `national_cost` came back on all 9. `status` is `sold` on a sold listing. Listing dates and views are not shown here (`/shop-products` has `created_at` and `updated_at`).

### Shop sold

```bash
curl -X POST https://api.scavio.dev/api/v1/depop/shop-sold \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"username": "flomem"}'
```

Captured `data` (2026-11-18, 1 credit; 1 of 24 items and 1 of 2 pictures shown):

```json
{
  "shop": { "shop_id": 46847613, "username": "flomem" },
  "items": [
    {
      "product_id": 1001815152,
      "slug": "fiomem-guess-navy-blue-cotton-t-shirt-693b",
      "url": "https://www.depop.com/products/fiomem-guess-navy-blue-cotton-t-shirt-693b/",
      "title": "Guess navy blue cotton t-shirt with white stripes on shoulders and sleeves, size XL #guess #stripes",
      "description": "Guess navy blue cotton t-shirt with white stripes on shoulders and sleeves, size XL #guess #stripes",
      "brand": { "id": 212, "name": "Guess", "slug": "guess" },
      "category": "T-shirts",
      "group": "tops",
      "product_type": "tshirts",
      "status": "sold",
      "seller_country": "us",
      "pictures": ["https://media-photos.depop.com/b1/46847613/5229284382_3272e2d2da124299b8358a41d2a28954/P0.jpg"],
      "picture_count": 2,
      "sizes": [{ "id": 6, "name": "XL", "quantity": 1, "status": "sold" }],
      "condition": "used_good",
      "colors": ["navy", "blue"],
      "gender": "male",
      "kids": false,
      "like_count": null,
      "boosted": false,
      "discounted": true,
      "discount_percentage": 35,
      "price": {
        "currency": "USD",
        "price": 2.6,
        "original_price": 4,
        "buyer_fee": 0,
        "tax": 0,
        "tax_type": null,
        "shipping": 1.99,
        "shipping_boundary": "national",
        "total": 4.59,
        "headline_price": 2.6
      },
      "created_at": "2026-11-15T22:19:08.107074Z",
      "updated_at": "2026-11-17T20:19:55.283814Z"
    }
  ],
  "count": 24,
  "has_more": true,
  "next_cursor": "MTAwMzM5Mjg3OXwyMDI2LTExLTE3VDAyOjMyOjU0LjQwNDIyNzAwMFp8MjQ",
  "notes": [
    "Shop data is global (one record for every market). Prices are in the seller's listing currency, with the buyer fee, tax and shipping of a US buyer view.",
    "updated_at is when the listing last changed; Depop shows no sale date."
  ]
}
```

Read it as: listed at $4.00, marked down 35%, sold at $2.60. `updated_at` is the last change to the listing, not the sale date; say "last updated" when quoting it. `like_count` was `null` on every shop-products, shop-sold and similar item in the captures (search items carry it). `/shop-products` has the same shape for the shop's listings for sale (`status: "on_sale"`).

### Shop

```bash
curl -X POST https://api.scavio.dev/api/v1/depop/shop \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"username": "flomem"}'
```

Captured `data` (2026-11-18, 1 credit; 1 of 4 departments and 2 of its categories shown):

```json
{
  "shop_id": 46847613,
  "username": "flomem",
  "url": "https://www.depop.com/flomem/",
  "bio": "Some y2k pieces",
  "verified": false,
  "followers": 101,
  "following": 48,
  "reviews_rating": 4.9,
  "reviews_total": 123,
  "seller_ratings": 123,
  "buyer_ratings": 0,
  "items_sold": 952,
  "last_seen": "active_this_week",
  "category_counts": {
    "total": 242,
    "departments": [
      {
        "id": "menswear",
        "count": 135,
        "children": [
          { "id": "tops", "count": 97, "children": [] },
          { "id": "tshirts", "count": 56, "children": [] }
        ]
      }
    ]
  },
  "notes": ["Shop data is global (one record for every market). Depop shows no join date or Top Seller badge here."]
}
```

`reviews_rating` is out of 5 and `reviews_total` counts the reviews behind it. `items_sold` is Depop's items-sold count for the shop; `category_counts` counts the shop's listings per department and category. `last_seen` is Depop's bucket (`active_this_week`), never a time.

### Shop reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/depop/shop-reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"username": "flomem"}'
```

Captured `data` (2026-11-18, 1 credit; 2 of 24 reviews shown):

```json
{
  "shop": { "shop_id": 46847613, "username": "flomem" },
  "role": "seller",
  "page": 1,
  "reviews": [
    {
      "date": "2026-11-18T00:38:40.628757Z",
      "rating": 5,
      "text": "Ty",
      "product": { "product_id": 988838919, "image": "https://media-photos.depop.com/b1/46847613/5151612235_d712005827af4d5cbbc99e815c57dd46/P0.jpg" }
    },
    {
      "date": "2026-11-17T19:07:52.384374Z",
      "rating": 5,
      "text": "Arrived fast & as described ",
      "product": { "product_id": 988837223, "image": "https://media-photos.depop.com/b1/46847613/5151600695_57511951f7de437881a42415b7c473ef/P0.jpg" }
    }
  ],
  "count": 24,
  "has_more": true,
  "notes": ["Reviewer names are not returned. The shop's review total is reviews_total of shop."]
}
```

### Categories and brands

```bash
curl -X POST https://api.scavio.dev/api/v1/depop/categories \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (2026-11-18, 1 credit; 1 of 4 departments, 1 of its 11 groups and 2 product types shown):

```json
{
  "language": "en",
  "departments": [
    {
      "id": "menswear",
      "name": "Men",
      "path": "mens",
      "groups": [
        {
          "id": "tops",
          "name": "Tops",
          "path": "mens/tops",
          "product_types": [
            { "id": "tshirts", "name": "T-shirts", "path": "mens/tops/tshirts" },
            { "id": "jerseys", "name": "Jerseys", "path": "mens/tops/jerseys" }
          ]
        }
      ]
    }
  ],
  "count": 333,
  "notes": ["path is the category input of category (e.g. mens/bottoms/jeans); group and product type ids are the group / product_type filters of search. Department names are English; group and product type names follow language."]
}
```

The 4 departments are `menswear` (`mens`), `womenswear` (`womens`), `kidswear` (`kids`) and `everything-else`. `path` feeds `/category`; a group `id` feeds search's `group` and a product type `id` its `product_type`. A path that is not in the tree answers `200` with no items and a note, so take paths from here.

```bash
curl -X POST https://api.scavio.dev/api/v1/depop/brands \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"letter": "c"}'
```

Captured `data` (2026-11-18, 1 credit; 3 of 1,561 brands shown):

```json
{
  "letter": "c",
  "brands": [
    { "id": 17496, "name": "C-Clique", "slug": "c-clique" },
    { "id": 28909, "name": "C-IN2", "slug": "c-in2" },
    { "id": 15491, "name": "C. Cline", "slug": "c-cline" }
  ],
  "count": 1561,
  "notes": ["slug is the input of brand (listings) and of brands by slug; id is the brand_ids filter of search."]
}
```

### Category, brand and explore

```bash
curl -X POST https://api.scavio.dev/api/v1/depop/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category": "mens/bottoms/jeans"}'
```

Captured `data` (US, 2026-11-18, 1 credit; the 24 items, which have the search item shape, and the notes dropped):

```json
{
  "category": { "department": "menswear", "group": "bottoms", "product_type": "jeans", "path": "mens/bottoms/jeans" },
  "country": "us",
  "currency": "USD",
  "sort": "relevance",
  "filters": {},
  "items": [],
  "count": 24,
  "total_count": 1568810,
  "facets": null
}
```

`/brand` with `{"slug": "carhartt"}` answers the same shape with `brand: {"id": 1673, "name": "Carhartt", "slug": "carhartt"}` (captured: 23 items, `total_count` 354624). `/explore` with `{"slug": "90s-menswear"}` adds `title` ("'90s Menswear"), `search_query` (`?q=90s+vintage&gender=male`, the search the page runs) and `more_slugs` (108 other explore pages on `us` in the capture).

### Suggestions and shops search

```bash
curl -X POST https://api.scavio.dev/api/v1/depop/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "carh"}'
```

Captured `data` (US, 2026-11-18, 1 credit; 3 of 10 suggestions shown):

```json
{
  "query": "carh",
  "country": "us",
  "currency": "USD",
  "suggestions": [
    { "text": "carhartt", "group": "bottoms", "gender": "male", "filter_label": "in Men's Bottoms" },
    { "text": "carhartt", "group": "tops", "gender": "male", "filter_label": "in Men's Tops" },
    { "text": "carhartt", "group": null, "gender": null, "filter_label": null }
  ],
  "count": 10
}
```

`/shops-search` with `{"query": "y2k"}` returned 5 shops (`shop_id`, `username`, `url`), for example `{"shop_id": 14055622, "username": "y2kfitz", "url": "https://www.depop.com/y2kfitz/"}`. Use `/shop` for a shop's stats.

### Similar

```bash
curl -X POST https://api.scavio.dev/api/v1/depop/similar \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1002884801}'
```

Returned 23 listings in the search item shape plus `created_at` and `updated_at`. In the capture 8 of the 23 were `boosted: true` (listings their sellers promote).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def depop(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/depop/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()["data"]

# 1. What Levi's 501 listings ask a UK buyer, cheapest of the first 24 (1 credit)
found = depop("search", {"query": "levis 501", "country": "gb", "sort": "price_asc", "conditions": ["used_excellent", "used_like_new"]})
for it in found["items"][:10]:
    p = it["price"]
    print(p["price"], p["buyer_fee"], p["shipping"], p["total"], p["currency"], it["title"], it["url"])

# 2. The full listing and its seller, priced for a UK buyer (2 credits on gb)
item = depop("product", {"slug": found["items"][0]["slug"], "country": "gb"})
seller = item["seller"]["username"]

# 3. What that shop sold and for how much (1 credit per page of 24)
sold, cursor = [], None
while len(sold) < 72:
    page = depop("shop-sold", {"username": seller, **({"cursor": cursor} if cursor else {})})
    sold += page["items"]
    if not page["has_more"]:
        break
    cursor = page["next_cursor"]
for s in sold:
    print(s["price"]["price"], s["price"]["original_price"], s["price"]["currency"], s["title"], "last updated", s["updated_at"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. `notes` explains anything market-specific.

- **listing item** (search, category, brand, explore, similar, shop-products, shop-sold) - `product_id`, `slug`, `url`, `title`, `description`, `brand` {`id`, `name`, `slug`}, `category`, `group`, `product_type`, `status` (`on_sale`, `sold`), `seller_country`, `pictures[]` (first 3), `picture_count`, `sizes[]` {`id`, `name`, `quantity`, `status`}, `condition`, `colors[]`, `gender`, `kids`, `like_count`, `boosted`, `discounted`, `discount_percentage`, `price` {`currency`, `price`, `original_price`, `buyer_fee`, `tax`, `tax_type`, `shipping`, `shipping_boundary`, `total`, `headline_price`}; plus `created_at`, `updated_at` on similar, shop-products and shop-sold.
- **search** - `query`, `country`, `currency`, `sort`, `filters`, `items[]`, `count`, `total_count`, `facets` {`total`, `departments[]` {`id`, `count`, `groups[]`, `product_types[]`}, `brands[]`, `colors[]`, `conditions[]`, `sizes[]`, each {`id`, `count`}}, `notes[]`.
- **category** - `category` {`department`, `group`, `product_type`, `path`}, `country`, `currency`, `sort`, `filters`, `items[]`, `count`, `total_count`, `facets` (`null`), `notes[]`.
- **brand** - `brand` {`id`, `name`, `slug`} and the category fields.
- **explore** - `slug`, `title`, `search_query`, `country`, `currency`, `sort`, `filters`, `items[]`, `count`, `total_count`, `facets` (`null`), `more_slugs[]`, `notes[]`.
- **product** - `product_id`, `slug`, `url`, `status`, `title`, `description`, `hashtags[]`, `brand`, `category` {`group`, `group_name`, `product_type`, `product_type_name`, `breadcrumbs[]` {`name`, `path`}}, `condition` {`id`, `name`}, `colors[]` {`id`, `name`}, `sizes[]`, `gender`, `kids`, `pictures[]`, `picture_count`, `like_count`, `boosted`, `quantity`, `shipping` {`method`, `parcel_size`, `payer`, `free_shipping`, `national_cost`, `confidence`}, `discounted`, `discount_percentage`, `price`, `listing_price` {`currency`, `price`, `original_price`}, `seller` {`id`, `username`, `url`, `verified`, `country`, `reviews_rating`, `reviews_total`, `items_sold`, `last_seen`, `average_shipping_days`}, `country`, `currency`, `notes[]`.
- **suggestions** - `query`, `country`, `currency`, `suggestions[]` {`text`, `group`, `gender`, `filter_label`}, `count`.
- **shop** - `shop_id`, `username`, `url`, `bio`, `verified`, `followers`, `following`, `reviews_rating`, `reviews_total`, `seller_ratings`, `buyer_ratings`, `items_sold`, `last_seen`, `category_counts` {`total`, `departments[]` {`id`, `count`, `children[]`}}, `notes[]`.
- **shop-products / shop-sold** - `shop` {`shop_id`, `username`}, `items[]`, `count`, `has_more`, `next_cursor`, `notes[]`.
- **shop-reviews** - `shop`, `role`, `page`, `reviews[]` {`date`, `rating`, `text`, `product` {`product_id`, `image`}}, `count`, `has_more`, `notes[]`.
- **shops-search** - `query`, `shops[]` {`shop_id`, `username`, `url`}, `count`.
- **categories** - `language`, `departments[]` {`id`, `name`, `path`, `groups[]` {`id`, `name`, `path`, `product_types[]` {`id`, `name`, `path`}}}, `count`, `notes[]`; plus `size_sets` with `include_sizes`.
- **brands** - `letter`, `brands[]` {`id`, `name`, `slug`}, `count`, `notes[]`; or one brand with its description when called by `slug`.
- **similar** - `product_id`, `country`, `currency`, `items[]`, `count`, `notes[]`.

## Guardrails

- Search, category, brand and explore return the first 24 results per query, sort and filter set; there is no `page` parameter and Depop serves no next page. Never call 24 items "all listings" or "every result", and never present `total_count` as the number of items returned. To cover more, run narrower slices (brand, condition, product type, price range).
- `price_asc` / `price_desc` return Depop's first 24 for that order, put in strict listing-price order, with listings priced in another currency than the market's last. They are the 24 cheapest or dearest Depop chose to show, not a sorted catalog.
- Sold prices come per shop from `/shop-sold`. There is no keyword search of sold listings, so never present one shop's sales as Depop-wide sold comps, and never invent a sale date: `updated_at` is when the listing last changed, `created_at` when it was listed.
- `price` is what a buyer in `country` pays: listing price plus `buyer_fee`, `tax` (`tax_type` names it) and `shipping` (`shipping_boundary` national or international) make `total`. `headline_price` is Depop's headline and can leave out shipping. Say which field you quote.
- The US buyer fee is not stable on Depop's side: Depop returns it on some calls and not on others for the same kind of listing. In the 2026-11-18 US captures, every item on the category, explore and similar answers carried a `buyer_fee`, and none on the search and brand answers. Report the `buyer_fee` Depop returned; never promise a fee or compute one.
- `price.currency` is the listing's currency, which can differ from the market's (`fr` 1 of 24, `it` 2 of 24 in USD in the capture). On `/product`, `listing_price` is the seller's own price and currency. Convert explicitly, with the rate and its date, before comparing.
- Product costs 2 credits on `gb`, `au`, `ie`, `ca`, `de`, `fr`, `it` and 6 on `nz`; search, category, brand and explore cost 5 on `nz`. Tell the user before a loop of product calls outside the US or any `nz` loop.
- `size` is partly honoured by Depop: check each item's `sizes` before calling a result set size-filtered.
- Titles and descriptions are the seller's own words in the seller's language; Depop's interface strings are English everywhere. Do not translate prices or sizes from a description into structured fields.
- Seller usernames are public listing data. Real names, avatars and cities are not returned, and reviews carry no reviewer identity: never try to identify a reviewer. Use shop data to judge a seller before a purchase, not to profile or contact a person.
- Not available: results beyond the first 24, keyword sold search, trending searches, views, join date, Top Seller badge, offers and bundles, price history (poll and store), similar outside `us`. This API cannot buy, make offers, message, like or manage listings.
- Terms: Scavio does not collect or store Depop data: each call fetches the public Depop page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Depop's terms of service cover how its service may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Depop listing photos or logos; link listings by `url` instead.
- Never fabricate prices, fees, listings, sold prices, ratings or reviews. Only return what the API returned, with the market, the currency and the listing `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` Depop has no storefront for (the message lists the 9), an endpoint the market does not serve (`similar` outside `us`), a missing `query` or `slug`, both or neither of `slug` / `url` / `product_id` or of `username` / `shop_id` or of `letter` / `slug`, a `url` that is not a depop.com product link, a `sort` other than `relevance` / `price_asc` / `price_desc`, a `price_min` above `price_max`, an unknown condition, colour or gender, `group` / `product_type` / `kids` on `/category` (the path sets them), `brand_ids` on `/brand`, a `cursor` that is not a previous `next_cursor`, a `role` other than `seller` / `buyer`, a `language` other than `en`, `en-US`, `de`, `fr`, `it`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Unknown Depop listing (check the slug, link or product_id).", "Unknown Depop shop (check the username or shop_id).", an unknown brand slug or explore page. Take slugs and ids from a previous answer rather than guessing them. An unknown category path is not a 404: it answers `200` with no items and a note.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api).
- `502` means Depop data was temporarily unavailable ("Depop is temporarily unavailable. Please try again." or "Depop did not answer for this market, try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Depop is busy ("Depop is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.68.0
npm install scavio@0.69.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.depop.search({ query: "levis 501", country: "gb", sort: "price_asc" });
const { data: item } = await scavio.depop.product({ slug: "f0omem-levis-550-38x36-blue-jeans-662f" });
const { data: jeans } = await scavio.depop.category({ category: "mens/bottoms/jeans" });
const { data: carhartt } = await scavio.depop.brand({ slug: "carhartt" });
const { data: page } = await scavio.depop.explore({ slug: "90s-menswear" });
const { data: typed } = await scavio.depop.suggestions({ query: "carh" });
const { data: shop } = await scavio.depop.shop({ username: "flomem" });
const { data: forSale } = await scavio.depop.shopProducts({ username: "flomem" });
const { data: sold } = await scavio.depop.shopSold({ username: "flomem" });
const { data: reviews } = await scavio.depop.shopReviews({ username: "flomem" });
const { data: shops } = await scavio.depop.shopsSearch({ query: "y2k" });
const { data: tree } = await scavio.depop.categories({ language: "de" });
const { data: brands } = await scavio.depop.brands({ letter: "c" });
const { data: similar } = await scavio.depop.similar({ product_id: 1002884801 });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.depop.search(...)`, `product`, `category`, `brand`, `explore`, `suggestions`, `shop`, `shop_products`, `shop_sold`, `shop_reviews`, `shops_search`, `categories`, `brands` and `similar`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all fourteen endpoints as tools: `search_depop`, `get_depop_product`, `get_depop_category`, `get_depop_brand`, `get_depop_explore`, `get_depop_suggestions`, `get_depop_shop`, `get_depop_shop_products`, `get_depop_shop_sold`, `get_depop_shop_reviews`, `search_depop_shops`, `get_depop_categories`, `get_depop_brands` and `get_depop_similar`. Depop is opt-in: add `depop` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.68.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,depop"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/depop-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [product](https://scavio.dev/docs/depop-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [category](https://scavio.dev/docs/depop-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [brand](https://scavio.dev/docs/depop-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [explore](https://scavio.dev/docs/depop-explore?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [suggestions](https://scavio.dev/docs/depop-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [shop](https://scavio.dev/docs/depop-shop?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [shop products](https://scavio.dev/docs/depop-shop-products?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [shop sold](https://scavio.dev/docs/depop-shop-sold?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [shop reviews](https://scavio.dev/docs/depop-shop-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [shops search](https://scavio.dev/docs/depop-shops-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [categories](https://scavio.dev/docs/depop-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [brands](https://scavio.dev/docs/depop-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api), [similar](https://scavio.dev/docs/depop-similar?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api). Overview: [Depop API](https://scavio.dev/depop-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=depop-api).
