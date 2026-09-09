# TikTok Shop API - Product Search, Prices, Shops, Sellers

Search the TikTok Shop catalog, read full product detail, pull paginated reviews with a star histogram, walk the global category tree, list a category's or a seller's products, and resolve any TikTok Shop URL or share link to a `product_id` / `shop_id`. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Search TikTok Shop for products by keyword, with prices, ratings and sold counts
- Get autocomplete or keyword expansion for a TikTok Shop search term
- Read a product's description, images, variants, stock, shipping and seller profile
- Pull a product's reviews, filter them by rating or media, or get the star distribution
- Browse the TikTok Shop category tree or list products in a category
- List a seller's / shop's product catalog
- Turn a TikTok Shop link (canonical page, affiliate share link, `vt.tiktok.com` short link) into an id
- Do e-commerce price research, competitor catalog tracking or review mining on TikTok Shop

This skill covers the **shop** side of TikTok. For creator profiles, videos, comments and hashtags use the `scavio-tiktok` skill instead. There is no video-to-product join available: you cannot ask "which products are attached to this TikTok video".

## Two things to read before you call anything

**1. A `/search` result is not guaranteed to resolve on `/product`.** Measured on 25 product ids taken straight from `/tiktok-shop/search`, only **11 (44%)** returned detail from `/tiktok-shop/product`. TikTok has no detail data for the rest, permanently — retries do not help and no other region helps. Those ids answer **HTTP `404`, and that is a normal outcome, not an error**. The 404 body is `{"error": "Product not found in this region.", "credits_used": 1, "credits_remaining": N}` — there is **no `data` key on it at all**, so branch on the status code, never on a data field. Skip the item and move on; do not retry it, do not report a failure to the user, and do not treat search -> product as a reliable pipeline. Build listing workflows on `/search`, `/category/products` and `/shop/products`, which return complete rows. If you need something for an id detail cannot resolve, `/product/reviews` is the fallback: measured on 8 ids that 404 on `/product`, **8 of 8 returned HTTP 200 from `/product/reviews` and 7 of 8 carried at least one review** (counts 15, 0, 2, 20, 4, 6, 20, 11). That is a measured sample of 8, not a guarantee.

**2. `/product` does not return a price.** TikTok masks the price digits on the product page, so `price.current` and `price.original` come back as `null` on that endpoint. **Exact prices are returned by `/search`, `/shop/products` and `/category/products`** — take the price from a listing call, and use `/product` only for the fields listings do not carry (description, images, variants, stock, shipping, full seller profile, category path, top reviews). Never derive, estimate or guess a price.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-shop-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-shop-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Endpoints in this skill cost 1 credit each unless the table below says otherwise.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/tiktok-shop`. Every endpoint costs **1 credit**.

| Endpoint | Credits | Description |
|---|---|---|
| `POST /api/v1/tiktok-shop/search` | 1 | Search products by keyword, with exact prices (US catalog) |
| `POST /api/v1/tiktok-shop/search/suggestions` | 1 | Keyword autocomplete and expansion, 8 regions |
| `POST /api/v1/tiktok-shop/product` | 1 | Full product detail (no price -- see above) |
| `POST /api/v1/tiktok-shop/product/reviews` | 1 | Paginated reviews, up to 200 per call |
| `POST /api/v1/tiktok-shop/categories` | 1 | The global category tree (28 top-level, 240 nodes) |
| `POST /api/v1/tiktok-shop/category/products` | 1 | Products in a category, with exact prices |
| `POST /api/v1/tiktok-shop/shop/products` | 1 | A shop's catalog, 30 per page, with exact prices |
| `POST /api/v1/tiktok-shop/resolve` | 1 | Resolve a TikTok Shop URL to a `product_id` / `shop_id` |

## Workflow

1. **Find products:** call `/tiktok-shop/search` with `search`. Each row already carries `price.current`, `rating`, `sold_count` and `shop` — for price and popularity work you are done here, no second call needed.
2. **Widen a query:** call `/tiktok-shop/search/suggestions` with a partial `search` to get related and corrected keywords, then search those.
3. **Deep-dive a product:** call `/tiktok-shop/product` with `product_id` for description, images, variants and stock, shipping, the full seller profile, the category path and up to 3 top reviews. Expect an HTTP 404 on roughly half of ids taken from search; skip those, or fall back to step 4.
4. **Mine reviews:** call `/tiktok-shop/product/reviews` with `product_id`. Raise `page_size` (up to 200) rather than making more calls — each call is 1 credit regardless of size. This endpoint also answers for ids `/product` cannot resolve: on 8 measured 404-on-detail ids, 8 of 8 returned HTTP 200 and 7 of 8 had at least one review, so it is the fallback detail source for those products.
5. **Browse by category:** call `/tiktok-shop/categories` once to get ids, then `/tiktok-shop/category/products` with a `category_id` (level 1 or 2 both work).
6. **Track a seller:** get a `shop_id` from any product card or from `/tiktok-shop/product`, then call `/tiktok-shop/shop/products`.
7. **Start from a link:** call `/tiktok-shop/resolve` with any TikTok Shop URL and feed the returned id into the endpoints above.

Paginated endpoints (`search`, `category/products`, `shop/products`) return `next_cursor`; pass it back as `cursor` for the next page. Stop when `next_cursor` is `null` or `has_more` is `false`. Cursors are opaque strings — never build, edit or reuse one across endpoints.

## Parameters

Regions are `US`, `GB`, `SG`, `MY`, `PH`, `TH`, `VN`, `ID` unless noted. Coverage is genuinely uneven: `search` is US-only and takes no `region` at all, category listings serve `US` and `GB` only, and `categories` is global so it takes no parameters.

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `search` | string | required | Search query (1-200 chars) |
| `cursor` | string | -- | Opaque cursor from a prior `next_cursor` |

US catalog only. There is no `sort` and no price/rating filter — TikTok exposes no way to submit one, so none is invented here.

### Search suggestions (`/search/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `search` | string | required | Partial query (1-100 chars) |
| `region` | string | `US` | `US`, `GB`, `SG`, `MY`, `PH`, `TH`, `VN`, `ID` |

Suggestions are not guaranteed prefix matches: a misspelling comes back as a typo correction, and results can include brand and shop names.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | 6-25 digits, e.g. `1732293553906094315` |
| `region` | string | `US` | `US`, `GB`, `SG`, `MY`, `PH`, `TH`, `VN`, `ID` |

Returns **no price** (`price.current` / `price.original` are `null`) — get the price from `/search`, `/shop/products` or `/category/products`. Answers **HTTP `404` for roughly 56% of ids returned by `/search`**; that is a normal, permanent outcome for those products, not an error and not worth retrying. The 404 body carries `error` plus the credit fields and **no `data` key**, so test the status code. `/product/reviews` still answered for every one of the 8 unresolvable ids measured (7 of them with at least one review), so try it before dropping the product.

### Product reviews (`/product/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | 6-25 digits |
| `page` | number | `1` | 1-based page number (1-500) |
| `page_size` | number | `20` | Reviews per call (1-200) |
| `sort` | string | `relevant` | `relevant` or `recent` |
| `rating` | number | -- | Only reviews with this star rating (1-5) |
| `has_media` | boolean | `false` | Only reviews carrying a photo or video |
| `verified_only` | boolean | `false` | Only verified purchases |
| `region` | string | `US` | `US`, `GB`, `SG`, `MY`, `PH`, `TH`, `VN`, `ID` |

`sort: "recent"` is fresher but far more text-sparse — many rows are stars only, with no text and no images. `sort: "relevant"` (the default) is text-complete and image-heavy.

`has_media` and `verified_only` share one upstream filter slot: if both are `true`, `has_media` wins. The response echoes what was actually applied in `filters_applied`, so read that rather than assuming.

### Categories (`/categories`)

No parameters. Send `{}`. Category ids are identical in every region and names are always English. The tree is two levels deep — that is all TikTok publishes; do not expect deeper nesting.

### Category products (`/category/products`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | required | 4-20 digits, from `/tiktok-shop/categories`; level 1 or 2 both work |
| `cursor` | string | -- | Opaque cursor from a prior `next_cursor` |
| `region` | string | `US` | `US` or `GB` only |

Page size varies upstream (15-20 items), so always paginate with `next_cursor` instead of assuming a fixed size. These listings are shallow: after a few pages TikTok stops returning new products and `has_more` turns `false` — that is the end of the listing, not an error.

### Shop products (`/shop/products`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `shop_id` | string | required | 6-25 digits (called `seller_id` elsewhere on TikTok) |
| `cursor` | string | -- | Opaque cursor from a prior `next_cursor` |
| `region` | string | `US` | `US`, `GB`, `SG`, `MY`, `PH`, `TH`, `VN`, `ID` |

30 products per page with exact prices. Follower count, shop location and shop-level rating are **not** available here — only `/tiktok-shop/product` carries the full shop profile.

### Resolve (`/resolve`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | required | A TikTok Shop URL (max 2000 chars) |

Accepted forms: `shop.tiktok.com` product (`/pdp/...`) and store (`/store/...`) pages, `tiktok.com/view/product/...` and `tiktok.com/view/shop/...`, `affiliate-*.tiktok.com` share links, and `vt.tiktok.com` / `tiktok.com/t/` short links. Anything else returns `400` and is **not** billed.

## Examples

```bash
# 1. Search -- the field is "search", not "query". Prices here are exact.
curl -s -X POST https://api.scavio.dev/api/v1/tiktok-shop/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"search": "protein powder"}'

# 2. Next page -- pass next_cursor back as cursor
curl -s -X POST https://api.scavio.dev/api/v1/tiktok-shop/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"search": "protein powder", "cursor": "eyJrIjoic2VhcmNoIiwibyI6MzAsInQiOiIyMDI2..."}'

# 3. Keyword expansion
curl -s -X POST https://api.scavio.dev/api/v1/tiktok-shop/search/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"search": "wireless", "region": "US"}'

# 4. Product detail -- no price here; an HTTP 404 for this id is normal
curl -s -X POST https://api.scavio.dev/api/v1/tiktok-shop/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "1729508370969629931", "region": "US"}'

# 5. Reviews -- one call of 200 costs the same 1 credit as one call of 20
curl -s -X POST https://api.scavio.dev/api/v1/tiktok-shop/product/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "1729508370969629931", "page": 1, "page_size": 200, "sort": "relevant"}'

# 6. Only 5-star reviews that carry a photo or video
curl -s -X POST https://api.scavio.dev/api/v1/tiktok-shop/product/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "1729508370969629931", "rating": 5, "has_media": true}'

# 7. The category tree -- no parameters
curl -s -X POST https://api.scavio.dev/api/v1/tiktok-shop/categories \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'

# 8. Products in a category (US or GB only)
curl -s -X POST https://api.scavio.dev/api/v1/tiktok-shop/category/products \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category_id": "601450", "region": "US"}'

# 9. A seller's catalog
curl -s -X POST https://api.scavio.dev/api/v1/tiktok-shop/shop/products \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"shop_id": "7495514739648989419", "region": "US"}'

# 10. Resolve a share link to an id
curl -s -X POST https://api.scavio.dev/api/v1/tiktok-shop/resolve \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://vt.tiktok.com/ZT2AHoGsE/"}'
```

Chaining it, with the 404 handled the way it should be:

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def call(path, body):
    return requests.post(f"{BASE}/api/v1/tiktok-shop/{path}", headers=HEADERS, json=body)

# 1. Search carries the exact price already -- this is the authoritative price.
results = call("search", {"search": "protein powder"}).json()

for card in results["data"]["products"]:
    print(card["product_id"], card["price"]["current"], card["rating"]["score"], card["title"][:60])

# 2. Detail is best-effort. Roughly 56% of search ids have no detail upstream:
#    an HTTP 404 is a normal outcome -- skip the item, do not retry. Branch on
#    r.status_code: the 404 body is {"error": ..., "credits_used": 1,
#    "credits_remaining": N} and has no "data" key to test.
for card in results["data"]["products"]:
    r = call("product", {"product_id": card["product_id"], "region": "US"})
    if r.status_code == 404:
        continue                      # no detail exists for this product, permanently
    r.raise_for_status()
    detail = r.json()["data"]
    # detail["price"]["current"] is None -- keep the price from the search card.
    print(detail["title"], len(detail["variants"]), "variants", card["price"]["current"])

# 2b. Reviews are the fallback for an id detail cannot resolve. Measured on 8
#     such ids: 8/8 returned HTTP 200 here and 7/8 had at least one review --
#     a small measured sample, so still handle the empty case.
for card in results["data"]["products"]:
    if call("product", {"product_id": card["product_id"]}).status_code != 404:
        continue
    rv = call("product/reviews", {"product_id": card["product_id"], "page_size": 200})
    if rv.status_code != 200:
        continue
    rows = rv.json()["data"]["reviews"]
    print(card["product_id"], len(rows), "reviews", "(none)" if not rows else rows[0]["text"][:60])

# 3. Reviews: one 200-row call instead of ten 20-row calls, same 1 credit.
reviews = call("product/reviews", {
    "product_id": results["data"]["products"][0]["product_id"],
    "page_size": 200, "sort": "relevant",
}).json()["data"]

print(reviews["rating"]["distribution"], reviews["total_reviews"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

`search`, `category/products` and `shop/products` all return the same **product card**, and it is the only place exact prices appear:

```json
{
  "product_id": "1729508370969629931",
  "title": "medicube PDRN Pink Collagen Volume Multi Balm 10g",
  "url": "https://shop.tiktok.com/us/pdp/medicube-pdrn-pink-collagen-volume-multi-balm/1729508370969629931",
  "image": "https://p19-oec-general.ttcdn-us.com/tos-maliva-i-o3syd03w52-us/2f1c8a.webp",
  "price": {
    "current": 19.99,
    "original": 29.0,
    "currency": "USD",
    "discount_percent": 31,
    "savings": 9.01,
    "min": 19.99,
    "max": 54.99
  },
  "rating": { "score": 4.7, "review_count": 12561 },
  "sold_count": 231615,
  "variant_count": 12,
  "brand": "medicube",
  "shop": {
    "shop_id": "7495514739648989419",
    "shop_name": "medicube US Store",
    "shop_logo": "https://p16-oec-general.ttcdn-us.com/tos-maliva-avt-0068/8a91.png"
  },
  "labels": ["Free shipping", "Limited time deal"]
}
```

Key `data` fields per endpoint:

- **search** — `query`, `products[]` (product card), `shops[]` (`shop_id`, `shop_name`, `shop_logo` — a 0-8 item brand carousel), `next_cursor`, `has_more`, `degraded`.
- **search/suggestions** — `query`, `region`, `suggestions[]` (plain strings, 20-50 of them; no scores, no search volume, no CPC).
- **product** — `product_id`, `title`, `description`, `url`, `images[]`, `price` (`currency`, `current`, `original`, `discount_percent`, `savings`), `rating` (`score`, `review_count`, `distribution`), `sold_count`, `variants[]` (`sku_id`, `name`, `in_stock`, `available_quantity`, `properties[]`, `weight_kg`, `dimensions_cm`), `shipping` (`fee`, `currency`, `delivery_min_days`, `delivery_max_days`, `delivery_min_business_days`, `delivery_max_business_days`, `cod_available`, `fulfillable`), `shop` (`shop_id`, `shop_name`, `shop_logo`, `shop_url`, `rating`, `review_count`, `sold_count`, `followers_count`, `product_count`, `video_count`, `region`, `is_official`), `categories[]` (`category_id`, `name`, `slug`), `breadcrumbs[]`, `top_reviews[]` (up to 3), `seller` (`business_name`, `business_address`).
- **product/reviews** — `product_id`, `page`, `page_size`, `filters_applied` (`sort`, `rating`, `has_media`, `verified_only`), `total_reviews`, `rating` (`score`, `review_count`, `distribution`), `reviews[]`, `has_more`.
- **categories** — `categories[]` (`category_id`, `name`, `slug`, `level`, `parent_id`, `image`, `children[]`), `total_categories`.
- **category/products** — `category_id`, `products[]` (product card), `next_cursor`, `has_more`.
- **shop/products** — `shop_id`, `shop` (`shop_id`, `shop_name`, `shop_logo`), `products[]` (product card), `next_cursor`, `has_more`.
- **resolve** — `type` (`product` or `shop`), `product_id`, `shop_id`, `url`, `resolved_by` (`url_pattern` or `share_link`).

Search response:

```json
{
  "data": {
    "query": "protein powder",
    "products": [ { "product_id": "1729508370969629931", "price": { "current": 19.99 } } ],
    "shops": [ { "shop_id": "7494676034572093351", "shop_name": "AmiShell", "shop_logo": "https://..." } ],
    "next_cursor": "eyJrIjoic2VhcmNoIiwibyI6MzAsInQiOiIyMDI2..." ,
    "has_more": true,
    "degraded": false
  },
  "response_time": 3412,
  "credits_used": 1,
  "credits_remaining": 999
}
```

Product detail — note `price.current` and `price.original` are `null`:

```json
{
  "data": {
    "product_id": "1729508370969629931",
    "title": "medicube PDRN Pink Collagen Volume Multi Balm 10g",
    "description": "Plain text, HTML stripped, image blocks removed.",
    "url": "https://shop.tiktok.com/us/pdp/1729508370969629931",
    "images": ["https://p19-oec-general.ttcdn-us.com/....webp"],
    "price": {
      "currency": "USD",
      "current": null,
      "original": null,
      "discount_percent": 31,
      "savings": null
    },
    "rating": {
      "score": 4.7,
      "review_count": 12561,
      "distribution": { "1": 431, "2": 221, "3": 571, "4": 1175, "5": 10163 }
    },
    "sold_count": 231615,
    "variants": [
      {
        "sku_id": "1732293560756310251",
        "name": "PMEUS43022R00",
        "in_stock": true,
        "available_quantity": 64657,
        "properties": [ { "name": "Specifications", "value": "Default" } ],
        "weight_kg": 0.1,
        "dimensions_cm": { "length": 7, "width": 4, "height": 4 }
      }
    ],
    "shipping": {
      "fee": 4.22,
      "currency": "USD",
      "delivery_min_days": 6,
      "delivery_max_days": 9,
      "delivery_min_business_days": 4,
      "delivery_max_business_days": 7,
      "cod_available": false,
      "fulfillable": true
    },
    "shop": {
      "shop_id": "7495514739648989419",
      "shop_name": "medicube US Store",
      "shop_url": "https://shop.tiktok.com/us/store/7495514739648989419",
      "rating": 4.6,
      "review_count": 455798,
      "sold_count": 7938115,
      "followers_count": 588860,
      "product_count": 153,
      "video_count": 1006,
      "region": "US",
      "is_official": true
    },
    "categories": [
      { "category_id": "601450", "name": "Beauty & Personal Care", "slug": "beauty-personal-care" },
      { "category_id": "848776", "name": "Skincare", "slug": "skincare" }
    ],
    "breadcrumbs": [ { "name": "Skincare", "url": "https://shop.tiktok.com/us/c/skincare/848776" } ],
    "top_reviews": [],
    "seller": { "business_name": "APR US INC", "business_address": "41 Greenfield, Irvine, California, 92614, United States" }
  },
  "response_time": 5108,
  "credits_used": 1,
  "credits_remaining": 998
}
```

A product with no detail upstream — HTTP `404`, and the credit fields are still present because the lookup really happened:

```json
{
  "error": "Product not found in this region.",
  "credits_used": 1,
  "credits_remaining": 997
}
```

Reviews:

```json
{
  "data": {
    "product_id": "1729508370969629931",
    "page": 1,
    "page_size": 20,
    "filters_applied": { "sort": "relevant", "rating": null, "has_media": false, "verified_only": false },
    "total_reviews": 12561,
    "rating": {
      "score": 4.6,
      "review_count": 12561,
      "distribution": { "1": 431, "2": 221, "3": 571, "4": 1175, "5": 10163 }
    },
    "reviews": [
      {
        "review_id": "7632550597593466637",
        "rating": 5,
        "text": "Absorbs fast and does not pill under makeup. Repurchasing.",
        "created_at": "2026-04-25T04:34:57.611Z",
        "reviewer_name": "C**",
        "reviewer_avatar": "https://p16-oec-general.ttcdn-us.com/...?x-expires=1777091697",
        "images": ["https://p19-oec-general.ttcdn-us.com/....webp"],
        "is_verified_purchase": true,
        "is_incentivized": false,
        "variant": "Default",
        "country": "US"
      }
    ],
    "has_more": true
  },
  "response_time": 2210,
  "credits_used": 1,
  "credits_remaining": 996
}
```

Categories and resolve:

```json
{
  "data": {
    "categories": [
      {
        "category_id": "601450",
        "name": "Beauty & Personal Care",
        "slug": "beauty-personal-care",
        "level": 1,
        "parent_id": null,
        "image": "https://lf16-tiktok-common.tiktokcdn-us.com/obj/....png",
        "children": [
          {
            "category_id": "849032",
            "name": "Hand & Foot Care",
            "slug": "hand-foot-care",
            "level": 2,
            "parent_id": "601450",
            "image": "https://lf16-tiktok-common.tiktokcdn-us.com/obj/....png",
            "children": []
          }
        ]
      }
    ],
    "total_categories": 240
  },
  "credits_used": 1,
  "credits_remaining": 995
}
```

```json
{
  "data": {
    "type": "product",
    "product_id": "8651224669119091502",
    "shop_id": null,
    "url": "https://shop.tiktok.com/us/pdp/8651224669119091502",
    "resolved_by": "share_link"
  },
  "credits_used": 1,
  "credits_remaining": 994
}
```

## Guardrails

- Every TikTok Shop endpoint costs **1 credit**, including the ones that answer `404`. Tell the user before paginating through many pages or looping detail lookups over a whole search page.
- **`/product` returns no price.** `price.current` and `price.original` are `null` there by design. Read the price from `/search`, `/shop/products` or `/category/products`, and never compute one from `discount_percent` or `savings`.
- **A `404` from `/product` is expected for about 56% of search ids** and is not a failure to report or retry. Detect it by HTTP status: the 404 body is `error` plus the credit fields, with no `data` key to inspect. Skip the item, or try `/product/reviews` for it. Never describe search -> product as a dependable pipeline to the user.
- **Reviews are the fallback when detail 404s**, measured on a sample of 8 unresolvable ids: all 8 returned HTTP 200 from `/product/reviews` and 7 returned at least one review. Present it that way — a measured sample, not a guarantee — and handle an empty `reviews[]`.
- Never fabricate product titles, prices, ratings, sold counts, review text or shop names. Only return API data. If a field is `null`, say it is unavailable.
- `search` is US-only and takes no `region`. `category/products` serves `US` and `GB` only. Do not pass a region a given endpoint does not accept.
- Cursors are opaque. Pass `next_cursor` back verbatim as `cursor`; do not decode, edit or share one between endpoints.
- Products can repeat across search pages. Dedupe by `product_id` when you merge pages.
- `total_reviews` drifts between calls minutes apart. Never compute a page count from it — page with `has_more`.
- Reviewer names arrive pre-masked by TikTok (`"C**"`). Leave them as they are.
- Reviewer avatars and review images are signed, short-lived URLs. Do not cache them as stable identifiers.
- Review text is genuinely multilingual, including inside US reviews. That is real user data — do not strip or translate it silently.
- Prefer one large `page_size` on reviews over many small pages: 200 rows and 20 rows both cost 1 credit.
- If `search` returns `"degraded": true`, TikTok served a short page after retries were exhausted — the list is incomplete, so say so rather than presenting it as the full result set.

## Failure handling

- `400` — an invalid parameter, or a `resolve` URL in a form TikTok Shop does not accept. Not billed. Fix the input; the error message for `resolve` lists the accepted URL forms.
- `400 "Invalid cursor."` — the cursor was edited, expired or came from a different endpoint. Restart the pagination from page 1.
- `401` — the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` on `/product` — **normal.** No detail exists for this product upstream. The body is `{"error": "Product not found in this region.", "credits_used": 1, "credits_remaining": N}`; there is no `data` key, so branch on the status code. Skip it; do not retry. `/product/reviews` is worth one call for the same id: 8 of 8 measured unresolvable ids answered HTTP 200 there, 7 of 8 with reviews.
- `404` on `/category/products` or `/shop/products` — the id returned nothing on the first page, so the category or shop does not exist or has no products. Check the id rather than retrying.
- `404` on `/resolve` — a supported link that TikTok could not resolve; it may have expired or may not point to a product or shop.
- `429` — rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-shop-api).
- `502` — TikTok Shop data is temporarily unavailable. Wait a few seconds and retry; the request already spent an internal retry budget, so retry slowly, not in a tight loop.
- Calls can take several seconds because short or truncated upstream pages are retried internally. Set a client timeout of at least 60 seconds.
- If a search returns nothing, try `/tiktok-shop/search/suggestions` for a better keyword before giving up.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Related

- `scavio-tiktok` — creator profiles, videos, comments, hashtags and the social graph. Use that skill for anything about TikTok content; use this one for the shop catalog.
- Full API reference: [Tiktok shop search](https://scavio.dev/docs/tiktok-shop-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-shop-api) (one page per endpoint: `tiktok-shop-search`, `tiktok-shop-suggestions`, `tiktok-shop-product`, `tiktok-shop-product-reviews`, `tiktok-shop-categories`, `tiktok-shop-category-products`, `tiktok-shop-shop-products`, `tiktok-shop-resolve`)
