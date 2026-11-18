# thredUP API - Prices, Estimated Retail, Sold Listings

Read thredUP, the online resale store for women's and kids' clothing, shoes, handbags and accessories, on its US store (thredup.com, English, USD; thredUP ships to the US and Canada from it, and there is no other storefront, so there is no `country` input). Search by keyword, list sold items by brand or category, browse a category, a brand or a deal collection, read one item in full, and look up Rescue boxes, the categories and filter values, the brand directory, suggestions, trending searches and similar items. All 12 endpoints return structured JSON at 1 credit per call.

**The job this skill is for: thredUP prices.** Each item's `price`, the `estimated_retail` (the estimated original retail) and `percent_off` computed from the two, the `condition` and the flaws thredUP noted, measurements and materials, and who priced the item (`seller_type`: thredUP itself, a Direct Listing peer seller, or a dropship partner).

Four limits shape every answer, so say them plainly:
- **119 items per page, up to page 21** (about 2,500 items per query and filter combination). `total` is thredUP's approximate count and reads 10000 at most (`total_capped: true` means 10,000+). Never call one answer "all listings"; to reach more, narrow with filters or split by `price_min` / `price_max`.
- **Free text is matched loosely.** thredUP's search is semantic: it matches the look, so a brand typed as text also returns similar brands. For one brand, use the `brand` filter (or `/thredup/brand`).
- **Sold listings are filters only, with no sold date.** `/sold` takes brand and / or category (no keyword) and returns the price the item last listed at. thredUP shows no date for a sale, so never describe a result as recent or give it a date.
- **Estimated retail is an estimate.** On items thredUP prices it is thredUP's own estimate; on Direct Listing items the seller enters it. Never present it as a verified retail price.

thredUP has no public developer API. Resale-as-a-Service is a managed resale program for brands, not a data API. This skill reads the public thredup.com store instead, with one Scavio key.

See also: for Poshmark sold prices with sold dates use `poshmark-api`; for Depop resale prices use `depop-api`; for Mercari sold prices use `mercari-api`; for Vinted listings use `vinted-api`; for eBay sold listings use `ebay-product-data`.

## When to trigger

Use this skill when the user asks to:
- Check thredUP prices for a brand, category, size or condition: the price, the estimated original retail and the percent off
- Compare items thredUP priced with Direct Listing (peer seller) and dropship partner items for the same search
- Read one thredUP item from a link: condition and the flaws thredUP noted, measurements, materials, fit, pictures, and on Direct Listings the shipping cost and buyer protection price
- See what a brand or category sold for on thredUP (the price the item last listed at; no sold date)
- Browse thredUP's clearance, Under $10, new arrivals or price drops collections, or the Rescue boxes and their bundle prices
- Resolve category tags, sizing ids, condition, colour, material and pattern values, brand names, search suggestions and trending searches before a search
- Find items thredUP shows as similar to one item

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, the list endpoints took 17-40 seconds (search 19, sold 40, category 22, brand 17, deals 17, similar 18), Rescue boxes 12, suggestions 6, and product, categories, brands and trending under 2 seconds. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns |
|---|---|
| `POST /api/v1/thredup/search` | Items for a keyword, 119 per page (up to page 21), with filters and sorts. Free text is semantic: use `brand` for one brand |
| `POST /api/v1/thredup/sold` | Sold items by filters (brand and / or category required, no keyword), 119 per page: the price the item last listed at; no sold date |
| `POST /api/v1/thredup/product` | One item by `item_number` or link: the item fields plus description, condition notes, measurements, characteristics (fit, material, care, sleeve, neckline, stretch), pictures, authentication, Direct Listing shipping and buyer protection, similar brands. Sold items still answer |
| `POST /api/v1/thredup/category` | One department's category (a tag from categories), 119 per page |
| `POST /api/v1/thredup/brand` | One brand's items in a department (default women), 119 per page |
| `POST /api/v1/thredup/deals` | A deal collection: `clearance`, `under_10`, `new_arrivals` (newest first) or `price_drops` (recently discounted first), 119 per page |
| `POST /api/v1/thredup/rescue-boxes` | Rescue boxes (mystery bundles): name, description, available, sizes, and each bundle's item count, price and state |
| `POST /api/v1/thredup/categories` | One department's categories and filter values: sizing ids, conditions, colours, materials, patterns, price ranges |
| `POST /api/v1/thredup/brands` | The brand directory: brands matching a term, every brand under one letter (A-Z), or the letter groups |
| `POST /api/v1/thredup/suggestions` | Search suggestions for a partial query, each a ready filter set (brand, category, department, free text) |
| `POST /api/v1/thredup/trending` | Trending searches for women, girls or boys |
| `POST /api/v1/thredup/similar` | Items thredUP shows as similar to one item: the first 120, no paging |

## Credits

Every endpoint costs **1 credit per call**. Each page is one call. A not-found (`404`: unknown item number) is charged; a `400` and an upstream failure (`502`, `503`) are not.

## Market

One store: thredup.com, English, prices in USD. thredUP ships to the US and Canada from it; Canadian shoppers see the same store and the same USD prices. There is no `country` input.

- **Departments** (`department` on the list endpoints, categories and brands): `women` (default), `girls`, `boys`, `handbags`, `shoes`, `designer`, `plus`, `juniors`, `maternity`, `accessories`. thredUP has no men's department.
- **Suggestions and trending** take `women` (default), `girls` or `boys`.
- An item's own `department` is thredUP's label for it and can read values that are not inputs (the captures show `women shoes` and `X`).

## Who priced the item (`seller_type`)

| `seller_type` | What it is | `estimated_retail` |
|---|---|---|
| `thredup` | Items thredUP prices and ships | thredUP's estimate of the original retail |
| `direct_listing` | Direct Listings: private sellers list, price and ship their own items (open beta since June 2026) | entered by the seller |
| `dropship` | Partner listings shipped by a retail partner | shown with the item; can sit below the price |

Every list endpoint returns all three by default (the answer's `filters.seller_type` says so); pass `seller_type` to narrow. In the captured `denim jacket` search page, 13 of 119 items were `thredup`, 59 `direct_listing` and 47 `dropship`. Split any percent-off figure by `seller_type` before comparing.

`percent_off` is computed by Scavio: `round((1 - price / estimated_retail) * 100)`, from the price shown and the estimated retail. It is `null` when there is no estimated retail or the estimated retail is not above the price (18 of the 119 captured search items: 11 Direct Listings and 7 dropship items). thredUP's own savings figure can differ on some items, so quote it as "computed from the price and the estimated retail".

## Workflow

1. **Prices for a query:** call `/thredup/search` with `query`. Each item has `price`, `estimated_retail`, `percent_off`, `condition`, `seller_type`, `size`, `brand` and `url`.
2. **One brand:** search text is semantic, so pass `brand` (as thredUP writes it: `items[].brand`, `/brands`, `/suggestions`) or call `/thredup/brand`. `"<Brand> - all brands"` (as suggestions return it) covers a brand's sub-lines.
3. **Narrow it:** `/thredup/categories` gives the category tags, sizing ids, conditions, colours, materials, patterns and price ranges of one department. `size` takes sizing ids, not labels.
4. **Sold:** `/thredup/sold` with `brand` and / or `category` (and the same filters). It returns the price each sold item last listed at; there is no sold date.
5. **Read an item:** `/thredup/product` with `item_number` (or `url`) for condition notes, measurements, characteristics, pictures and, on Direct Listings, shipping and buyer protection.
6. **Deals:** `/thredup/deals` with `collection` (`clearance`, `under_10`, `new_arrivals`, `price_drops`) and `/thredup/rescue-boxes`.
7. **Price watching:** there is no price history. Poll the same item or query on a schedule and store each answer with its date.

## Parameters

### Search (`/search`), sold (`/sold`), category (`/category`), brand (`/brand`), deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Search keywords (1-200 chars). Search only. Sold takes no `query` (a query answers `400`) |
| `brand` | string | none | Brand as thredUP writes it. Required on `/brand`; on `/sold` send `brand` and / or `category` |
| `department` | string | `women` | See Market. Required on `/category` |
| `category` | string | none | Category tag from `/categories` (`categories[].category`: `dresses`, `outerwear`, `one-pieces`). Required on `/category` |
| `collection` | string | deals: required | `clearance`, `under_10`, `new_arrivals` (newest first), `price_drops` (recently discounted first) |
| `size` | integer or array | all | Sizing ids from `/categories` (`sizes[].size`; the captured women answer lists Sm as 778, Med as 795), up to 10 |
| `condition` | string or array | all | Up to 5 of `new_with_tags` (original tags attached), `excellent`, `very_good`, `good`, `flawed` (thredUP's Flawed Gems) |
| `color` | string or array | all | Up to 5 of `black`, `grey`, `white`, `ivory`, `tan`, `brown`, `purple`, `blue`, `teal`, `green`, `red`, `pink`, `orange`, `yellow` |
| `material` | string or array | all | Up to 5 material groups from `/categories` (`cotton`, `cashmere`, `wool blend`, `leather`, `vegan leather` ...) |
| `pattern` | string | all | One pattern from `/categories` (`floral`, `stripes`, `plaid` ...) |
| `price_min` / `price_max` | number | none | Whole USD. Approximate: thredUP matches the filter on an item's base price, so an item can show slightly outside the range (a 0-10 range returned items at 11.99-12.99). `under_10` sets its own range and takes neither |
| `clearance` | boolean | false | Only clearance items |
| `seller_type` | string or array | all three | `thredup`, `direct_listing`, `dropship` |
| `sort` | string | `default` | `default` (the page's own order: relevance for a search, recommended for a list, price drop for sold, where thredUP applies no other sort; the answer's `sort` says which), `recommended`, `relevance`, `newest`, `price_high`, `price_low`, `price_drop` (recently discounted). `new_arrivals` and `price_drops` take no `sort` |
| `page` | integer | 1 | 119 items per page, 1-21 (a later page answers `400`, not charged) |

### Product (`/product`) and similar (`/similar`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_number` | integer or string | one of | thredUP item number (`items[].item_number`; the number at the end of a thredup.com item link), e.g. `241601590` |
| `url` | string | one of | A thredup.com item link. Send exactly one of `item_number`, `url` |

### Categories (`/categories`)

`department` (optional, default `women`).

### Brands (`/brands`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | none | Brands matching a term (1-60 chars) |
| `letter` | string | none | Every brand under one letter, A-Z (`#` is not offered). Send `query` or `letter`, not both |
| `department` | string | `women` | See Market |
| `page`, `limit` | integer | 1, 100 | Paging of a `query` or `letter` answer; `limit` 1-500. Without `query` or `letter` the answer is the letter groups (50 brands each) and `page` / `limit` answer `400` |

### Suggestions (`/suggestions`) and trending (`/trending`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | suggestions: required | What the shopper has typed so far (1-100 chars) |
| `department` | string | `women` | `women`, `girls` or `boys` |

### Rescue boxes (`/rescue-boxes`)

No parameters: send `{}`.

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/thredup/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "denim jacket"}'
```

Captured `data` (2026-11-18, 1 credit; 1 of 119 items shown, the first item thredUP priced):

```json
{
  "query": "denim jacket",
  "sort": "relevance",
  "filters": { "department": "women", "seller_type": ["thredup", "direct_listing", "dropship"] },
  "page": 1,
  "page_size": 119,
  "total": 10000,
  "total_capped": true,
  "has_more": true,
  "count": 119,
  "currency": "USD",
  "items": [
    {
      "item_number": 241601590,
      "url": "https://www.thredup.com/product/women-zenim-denim-jacket/241601590",
      "title": "Zenim Denim Jacket",
      "brand": "Zenim",
      "category": "Denim Jacket",
      "category_tags": ["outerwear"],
      "department": "women",
      "size": "Size M",
      "condition": "excellent",
      "price": 21.99,
      "currency": "USD",
      "estimated_retail": 48,
      "percent_off": 54,
      "promo": { "percent": 50, "price": 10.99, "code": "50WELCOME" },
      "clearance": false,
      "final_sale": false,
      "new_with_tags": false,
      "seller_type": "thredup",
      "status": "available",
      "colors": ["Blue"],
      "materials": ["82% COTTON", "16% POLYESTER", "2% SPANDEX"],
      "picture_url": "https://cf-assets-thredup.thredup.com/assets/997218510/retina.jpg",
      "picture_count": 6,
      "favorite_count": 9
    }
  ]
}
```

Read the item as: listed at $21.99, estimated original retail $48, 54 percent off computed from the two. `promo` is a promotion code thredUP offers on the item (here a 50 percent first-order code, $10.99 with the code); `price` stays the list price. `total` reads 10000 with `total_capped: true`: more than 10,000 matches, of which one query reaches about 2,500. `status` is `available`, `reserved` (2 of the 119 captured items) or `sold`. A dropship item can carry a style name in `category` and a price above its estimated retail; the first items of this captured page were dropship items at $414.99 against an estimated retail of 378.

### Sold

```bash
curl -X POST https://api.scavio.dev/api/v1/thredup/sold \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"brand": "Coach", "department": "handbags"}'
```

Captured `data` (2026-11-18, 1 credit; 1 of 119 items shown):

```json
{
  "status": "sold",
  "sort": "price_drop",
  "filters": { "department": "handbags", "brand": "Coach", "seller_type": ["thredup", "direct_listing", "dropship"] },
  "page": 1,
  "page_size": 119,
  "total": 6241,
  "total_capped": false,
  "has_more": true,
  "count": 119,
  "currency": "USD",
  "items": [
    {
      "item_number": 240498589,
      "url": "https://www.thredup.com/product/handbags-coach-leather-hobo/240498589",
      "title": "Coach Leather Hobo",
      "brand": "Coach",
      "category": "Leather Hobo",
      "category_tags": ["handbags"],
      "department": "handbags",
      "size": "One size",
      "condition": "flawed",
      "price": 140.99,
      "currency": "USD",
      "estimated_retail": 530,
      "percent_off": 73,
      "promo": null,
      "clearance": false,
      "final_sale": true,
      "new_with_tags": false,
      "seller_type": "thredup",
      "status": "sold",
      "colors": ["Black"],
      "materials": ["100% Leather"],
      "picture_url": "https://cf-assets-thredup.thredup.com/assets/991254502/retina.jpg",
      "picture_count": 3,
      "favorite_count": 88
    }
  ]
}
```

`price` on a sold item is the price it last listed at. thredUP shows no sold date, and the default order of sold items is `price_drop` (recently discounted), not by when they sold. On this captured page all 119 items were `thredup`-priced, from $29.99 to $403.99 (median $104.99), with `percent_off` from 24 to 81 (median 70). `total` (6,241) is thredUP's count of sold Coach handbags for these filters; a query reaches about 2,500 of them.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/thredup/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_number": 241601590}'
```

Captured `data` (2026-11-18, 1 credit; of the item fields shown in the search example only 5 kept, 6 of 7 pictures dropped):

```json
{
  "item_number": 241601590,
  "price": 21.99,
  "estimated_retail": 48,
  "percent_off": 54,
  "seller_type": "thredup",
  "description": null,
  "brand_id": 15685,
  "departments": ["women"],
  "sale": false,
  "condition_notes": ["Practically new: shows no obvious signs of being worn or washed."],
  "condition_detail": null,
  "size_detail": { "chart": "womenTop", "scale": "ALPHA", "value": "M" },
  "sizing_id": 795,
  "measurements": {
    "display": "Item measurements are not available.",
    "method": "physical",
    "chest": null,
    "waist": null,
    "length": null,
    "inseam": null,
    "rise": null,
    "height": null,
    "depth": null,
    "heel_height": null
  },
  "characteristics": {
    "fit": [],
    "pattern": [],
    "material": [],
    "sleeve_length": [],
    "neckline": [],
    "features": [],
    "stretch": [],
    "care": [],
    "inseam_in": null,
    "rise_in": null,
    "length_in": null,
    "chest_in": null,
    "waist_in": null
  },
  "style_tags": [],
  "pictures": ["https://cf-assets-thredup.thredup.com/assets/997218510/retina.jpg"],
  "authentication": null,
  "certified_authenticity": null,
  "direct_listing": null,
  "similar_brands": []
}
```

`condition_notes` are the flaws and wear thredUP noted. `measurements.display` says when thredUP has none (as here). `description` is the seller's text on Direct Listings. `direct_listing` is `{shipping_cost, shipping_covered, buyer_protection_price, on_vacation}` on Direct Listing items and `null` otherwise. `certified_authenticity` applies to partner listings. A sold item still answers, with `status: "sold"` and the price it last listed at. No seller or consignor names or ids are returned.

### Categories

```bash
curl -X POST https://api.scavio.dev/api/v1/thredup/categories \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured on `women` (2026-11-18, 1 credit): 13 categories (`{"name": "Dresses", "category": "dresses"}`, `{"name": "Coats & jackets", "category": "outerwear"}`, ...), `other_departments` `[{"name": "Shoes", "department": "shoes"}]`, 65 sizes such as `{"group": null, "label": "Sm", "long_label": null, "size": 778}` and `{"group": "Waist", "label": "27", "long_label": "27\" Waist", "size": 782}`, 5 conditions (`{"label": "Flawed gems", "condition": "flawed"}`), 14 colours, 22 materials, 21 patterns and 5 price ranges from `{"label": "Under $10", "price_min": 0, "price_max": 10}` to `{"label": "$150+", "price_min": 150, "price_max": null}`. The `category`, `size`, `condition`, `color`, `material` and `pattern` values are the inputs of the list endpoints.

### Category, brand and deals

`/category` with `{"department": "women", "category": "dresses"}`, `/brand` with `{"brand": "Madewell"}` and `/deals` with `{"collection": "clearance"}` each returned 119 items in the search item shape with `total` 10000 (`total_capped: true`) and `sort: "recommended"`, echoing `department`, `category`, `brand` or `collection`. An unknown brand on `/brand` answers 0 items, not a `404`.

### Brands, suggestions and trending

`/brands` with `{"query": "coach"}` returned 38 brands such as `{"id": 1953, "name": "Coach", "brand": "Coach"}` and `{"id": 31047, "name": "Coach Factory", "brand": "Coach Factory"}`; `brand` is the input of the brand filter. `/suggestions` with `{"query": "made"}` returned 10 suggestions such as `{"text": "Madewell jeans", "query": null, "department": "women", "brand": "Madewell - all brands", "category": "jeans", "free_text": false}`: pass `brand`, `category`, `department` and `query` straight to search. `/trending` (women) returned 20 searches such as `{"text": "cocktail dress", "query": "cocktail dress", "department": "women", "brand": null, "category": null, "free_text": true}`.

### Rescue boxes

```bash
curl -X POST https://api.scavio.dev/api/v1/thredup/rescue-boxes \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (2026-11-18, 1 credit; 1 of 24 boxes shown):

```json
{
  "count": 24,
  "available_count": 2,
  "currency": "USD",
  "boxes": [
    {
      "id": "8",
      "name": "Name Brand Handbags",
      "description": "Get 4 bags and 1 accessory from popular handbag brands . Includes 4 bags (handbags, totes, cross-bodies & purses) + 1 accessory (jewelry, sunglasses, scarves, wallets & more.",
      "available": false,
      "sizes": [],
      "picture_url": "https://cf-assets-tup.thredup.com/pwa/rescues/namebrandHandbags.jpg",
      "bundles": [
        { "items": "5 Items", "price": 80, "currency": "USD", "state": "unlisted", "sizes": [] },
        { "items": "5 Items", "price": 90, "currency": "USD", "state": "unlisted", "sizes": [] },
        { "items": "5 items", "price": 90, "currency": "USD", "state": "unlisted", "sizes": [] },
        { "items": "5 Items", "price": 100, "currency": "USD", "state": "listed", "sizes": [] }
      ]
    }
  ]
}
```

`state: "listed"` marks the bundle on sale now; `available` says whether the box can be bought at the moment (2 of the 24 captured boxes). `items` is thredUP's own text ("5 Items", "50 lbs", "15 Pairs"), not a number.

### Similar

`/similar` with `{"item_number": 241601590}` returned `total` 9404 and 120 items in the search item shape (77 `thredup`, 30 `direct_listing`, 13 `dropship`), the first 120 with no paging.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def thredup(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/thredup/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()["data"]

# 1. Live Madewell prices in excellent condition, split by who priced the item (1 credit per page)
live = thredup("brand", {"brand": "Madewell", "condition": "excellent"})
for kind in ("thredup", "direct_listing", "dropship"):
    offs = [i["percent_off"] for i in live["items"] if i["seller_type"] == kind and i["percent_off"] is not None]
    print(kind, len(offs), "items with a percent off computed from the price and the estimated retail")

# 2. What sold Coach handbags last listed at (no sold date), in price bands so each band has its own reach.
# Price filters are approximate, so bands can overlap: keep each item number once.
sold = {}
for lo, hi in [(0, 50), (50, 150), (150, 1000)]:
    for page in range(1, 22):  # 119 items per page, up to page 21
        d = thredup("sold", {"brand": "Coach", "department": "handbags", "price_min": lo, "price_max": hi, "page": page})
        sold.update({i["item_number"]: i for i in d["items"]})
        if not d["has_more"]:
            break
for s in list(sold.values())[:10]:
    print(s["price"], "last listed price; estimated original retail", s["estimated_retail"], s["condition"], s["url"])

# 3. Read one item in full (1 credit)
item = thredup("product", {"item_number": live["items"][0]["item_number"]})
print(item["condition_notes"], item["measurements"]["display"], item["direct_listing"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached.

- **item** (search, sold, category, brand, deals, similar) - `item_number`, `url`, `title`, `brand`, `category`, `category_tags[]`, `department`, `size`, `condition` (`new_with_tags`, `excellent`, `very_good`, `good`, `flawed`), `price`, `currency`, `estimated_retail` (the estimated original retail: thredUP's estimate, the seller's on Direct Listings), `percent_off` (computed from `price` and `estimated_retail`, `null` when there is none or it is not above the price), `promo` {`percent`, `price`, `code`} (a promotion code thredUP offers on the item; `price` stays the list price), `clearance`, `final_sale`, `new_with_tags`, `seller_type` (`thredup`, `direct_listing`, `dropship`), `status` (`available`, `reserved`, `sold`), `colors[]`, `materials[]`, `picture_url`, `picture_count`, `favorite_count`.
- **search / sold / category / brand / deals** - `query` (search), `status` (sold), `department` and `category` (category), `brand` and `department` (brand), `collection` and `department` (deals), then `sort` (the order applied), `filters`, `page`, `page_size` (119), `total` (approximate, 10000 at most), `total_capped`, `has_more`, `count`, `currency`, `items[]`.
- **product** - the item fields plus `description`, `brand_id`, `departments[]`, `sale`, `condition_notes[]`, `condition_detail`, `size_detail` {`chart`, `scale`, `value`}, `sizing_id`, `measurements` {`display`, `method`, `chest`, `waist`, `length`, `inseam`, `rise`, `height`, `depth`, `heel_height`}, `characteristics` {`fit`, `pattern`, `material`, `sleeve_length`, `neckline`, `features`, `stretch`, `care`, `inseam_in`, `rise_in`, `length_in`, `chest_in`, `waist_in`}, `style_tags[]`, `pictures[]`, `authentication`, `certified_authenticity`, `direct_listing` {`shipping_cost`, `shipping_covered`, `buyer_protection_price`, `on_vacation`} or `null`, `similar_brands[]`.
- **similar** - `item_number`, `total`, `total_capped`, `page_size` (120), `count`, `currency`, `items[]`.
- **rescue-boxes** - `count`, `available_count`, `currency`, `boxes[]` {`id`, `name`, `description`, `available`, `sizes[]`, `picture_url`, `bundles[]` {`items`, `price`, `currency`, `state` (`listed` = on sale now), `sizes[]`}}.
- **categories** - `department`, `categories[]` {`name`, `category`}, `other_departments[]` {`name`, `department`}, `sizes[]` {`group`, `label`, `long_label`, `size` (the sizing id)}, `conditions[]` {`label`, `condition`}, `colors[]` {`label`, `color`}, `materials[]` {`label`, `material`}, `patterns[]` {`label`, `pattern`}, `price_ranges[]` {`label`, `price_min`, `price_max`}, `category_count`, `size_count`.
- **brands** - with `query` or `letter`: `department`, `query` or `letter`, `total`, `page`, `limit`, `has_more`, `count`, `brands[]` {`id`, `name`, `brand`}; with neither: `department`, `count`, `groups[]` {`letter`, `total`, `count`, `brands[]`}.
- **suggestions** - `query`, `department`, `count`, `suggestions[]` {`text`, `query` (the free-text part), `department`, `brand`, `category`, `free_text`}. **trending** - `department`, `count`, `searches[]` in the same shape.

## Guardrails

- One query and filter combination reaches about 2,500 items (21 pages of 119). Never call one answer "all listings" or "all sold items", and never present `total` as what was returned. To cover more, run narrower slices (brand, category, size, condition, price bands) and say how the sample was built.
- Search text is semantic: a brand typed as text also returns similar brands. Use the `brand` filter for one brand.
- Sold items: filters only, no keyword, and no sold date. `price` is the price the item last listed at. Never write that an item sold on a date, that a sale is recent, or that a price is what the buyer paid after a promotion.
- `estimated_retail` is the estimated original retail: thredUP's estimate on thredUP-priced items, the seller's on Direct Listings. Never call it a verified retail price or MSRP. Quote `percent_off` as computed from the price and the estimated retail, and split any comparison by `seller_type`.
- Price filters are approximate (thredUP matches a base price): check `price` on each item before stating a range.
- `promo.price` is the price with a promotion code thredUP offers (often a first-order code); it is not what every buyer pays. `price` is the list price.
- Prices are in USD. thredUP ships to the US and Canada from this one store; there is no Canadian price list.
- No seller, consignor or buyer names or ids are returned; never try to identify one.
- Not available: product reviews (thredUP shows none), seller shops, sold dates, men's clothing (no men's department), seller payout data, price history (poll and store), Resale-as-a-Service brand shops. This API cannot buy, favorite or list items.
- Terms: Scavio does not collect or store thredUP data: each call fetches the public thredUP page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Read thredUP's current terms for your use case; this is not legal advice. Do not republish thredUP item photos or logos; link items by `url` instead.
- Never fabricate prices, estimated retail, items or condition notes. Only return what the API returned, with the currency and the item `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `page` above 21 (the message explains the 2,500-item reach and how to narrow), a `query` on sold or a sold call without `brand` or `category`, a missing `query` on search, a missing `department` or `category` on category, a `category` that is not a tag, a `size` that is not a sizing id, an unknown `condition`, `color`, `material`, `pattern`, `seller_type`, `sort`, `department` or `collection`, more than 5 values in a list filter, `price_min` above `price_max`, a `sort` on `new_arrivals` / `price_drops` or a price range on `under_10`, both or neither of `item_number` / `url`, a `url` that is not a thredup.com item link, both `query` and `letter` on brands, a `letter` outside A-Z, `page` / `limit` on brands without `query` or `letter`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No thredUP item with this item number." Take item numbers from a previous answer rather than guessing them. An unknown brand on `/brand` answers `200` with 0 items.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api).
- `502` means thredUP data was temporarily unavailable ("thredUP is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means thredUP is busy ("thredUP is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.70.0
npm install scavio@0.71.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.thredup.search({ query: "denim jacket", condition: "excellent" });
const { data: sold } = await scavio.thredup.sold({ brand: "Coach", department: "handbags" });
const { data: item } = await scavio.thredup.product({ item_number: 241601590 });
const { data: dresses } = await scavio.thredup.category({ department: "women", category: "dresses" });
const { data: madewell } = await scavio.thredup.brand({ brand: "Madewell" });
const { data: clearance } = await scavio.thredup.deals({ collection: "clearance" });
const { data: boxes } = await scavio.thredup.rescueBoxes({});
const { data: filters } = await scavio.thredup.categories({ department: "women" });
const { data: brands } = await scavio.thredup.brands({ query: "coach" });
const { data: typed } = await scavio.thredup.suggestions({ query: "made" });
const { data: trending } = await scavio.thredup.trending({ department: "women" });
const { data: similar } = await scavio.thredup.similar({ item_number: 241601590 });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.thredup.search(...)`, `sold`, `product`, `category`, `brand`, `deals`, `rescue_boxes`, `categories`, `brands`, `suggestions`, `trending` and `similar`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all twelve endpoints as tools: `search_thredup`, `get_thredup_sold`, `get_thredup_product`, `get_thredup_category`, `get_thredup_brand`, `get_thredup_deals`, `get_thredup_rescue_boxes`, `get_thredup_categories`, `get_thredup_brands`, `get_thredup_suggestions`, `get_thredup_trending` and `get_thredup_similar`. thredUP is opt-in: add `thredup` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.70.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,thredup"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/thredup-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api), [sold](https://scavio.dev/docs/thredup-sold?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api), [product](https://scavio.dev/docs/thredup-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api), [category](https://scavio.dev/docs/thredup-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api), [brand](https://scavio.dev/docs/thredup-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api), [deals](https://scavio.dev/docs/thredup-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api), [Rescue boxes](https://scavio.dev/docs/thredup-rescue-boxes?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api), [categories](https://scavio.dev/docs/thredup-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api), [brands](https://scavio.dev/docs/thredup-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api), [suggestions](https://scavio.dev/docs/thredup-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api), [trending](https://scavio.dev/docs/thredup-trending?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api), [similar](https://scavio.dev/docs/thredup-similar?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api). Overview: [thredUP API](https://scavio.dev/thredup-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api).
