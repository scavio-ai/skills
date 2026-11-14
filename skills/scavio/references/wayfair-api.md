# Wayfair API - Product Prices, Sale and Was Price, Reviews, Delivery

Read Wayfair product data on wayfair.com, wayfair.ca (English or French), wayfair.co.uk and wayfair.ie, and on Wayfair's US banner sites AllModern, Birch Lane, Joss & Main and Perigold: keyword search and category listings with Wayfair's own sorts and filters, one product in full by SKU or link (every option, the price and stock of one option, the review summary and a delivery estimate to a ZIP or postal code), and the market's current sale events. All 4 endpoints return structured JSON and cost 1 credit each.

**The job this skill is for: Wayfair price history.** Wayfair shows no price history on its pages, and Wayfair's terms state "We do not price match", so shoppers and pricing teams watch prices themselves. Build the history by polling: read `price`, `sale_price`, `was_price`, `price_label` and `badge` for the same SKU (and the same `option_id`) on a schedule, store each reading with its time, and compare runs. Captured 2026-11-14 for the Shiflett Oriental area rug, SKU W005006988, on wayfair.com:

| Field | Value |
|---|---|
| `price` | USD 82.99 |
| `sale_price` | USD 82.99 |
| `was_price` | USD 197.99 |
| `price_label` | `Sale` |
| `percent_off` | 58 |
| `badge` | `Early Black Friday` |

**What the was price and the Sale label mean, in Wayfair's own words.** `was_price` is the strikethrough price on the page. Wayfair's US terms ("About Our Prices") state: "Where a product listing on our Sites references a higher price, typically denoted by a strikethrough (e.g. '$549'), such higher price represents the retail price suggested by the manufacturer or supplier. In the absence of a price suggested by the manufacturer or supplier, this price represents the highest price at which we offered or sold the product at some point in the past." On the Sale tag: "The 'Sale' tag on a product listing on our Sites signifies that we are selling the product at a discount from a price in the previous 90 days." So `was_price` is not yesterday's price, and a percent off against it is not a measured price drop. To tell whether a price really fell, compare your own stored readings.

Wayfair's APIs are for its suppliers (orders, inventory and catalog through Partner Home). Wayfair publishes no public API for its catalog, prices or reviews.

See also: for IKEA prices by country use `ikea-api`; for home-improvement prices by store use `home-depot-product-data`, `lowes-product-data` or `menards-product-data`; for the cross-retailer view of one product use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Track Wayfair prices or build a Wayfair price history (poll and store price, sale price, was price and badge)
- Check whether a Wayfair sale is real: what the strikethrough (was) price and the Sale label mean, and how the price moved over time
- Search Wayfair products by keyword, sorted by price or customer rating, filtered by sale, closeout, open box, new arrivals, in stock, brand, rating or price range
- Browse a Wayfair category (sofas, area rugs, office chairs) page by page
- Read one Wayfair product in full by SKU or link: options (size, color) with their option ids, dimensions, specifications, documents, returns, rating histogram and review summary
- Get the price and stock of one size or color of a Wayfair product
- Get a Wayfair delivery estimate to a US ZIP code or a Canadian postal code
- List Wayfair's current sale events (the Daily Sales list) on wayfair.com, wayfair.ca, wayfair.co.uk or wayfair.ie
- Read Wayfair Canada in French, Wayfair UK in GBP or Wayfair Ireland in EUR
- Search or read products on AllModern, Birch Lane, Joss & Main or Perigold

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint here costs 1 credit per call.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In build testing, sale events took 1.6 to 3.7 seconds, products 1.8 to 20 seconds, and search and category pages 3 to 57 seconds. A failed attempt is retried once, so a slow search or category call can take up to about 2 minutes. Set a client timeout of at least 150 seconds and do not fire many calls at once.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/wayfair/search` | 1 | A page of products for a keyword: per item price, sale price, was price, price label, discount, per-item price, loyalty savings, badge, rating, review count, stock, open-box price, option counts, brand {`id`, `name`}, `sponsored`; plus total (approximate), facets and the filters applied. Keyword pages hold 30 items; a keyword that opens a category answers that category's grid of 48 and says so in `redirected_to` |
| `POST /api/v1/wayfair/product` | 1 | One product by SKU or product link: prices, badge, limited-time deal, stock, max quantity, every option with its `option_id`, dimensions, specifications, features, description, images, breadcrumbs, documents, collection, returns, rating, rating histogram, review summary, review aspects, the 5 reviews the page shows and, with `zip`, a delivery estimate |
| `POST /api/v1/wayfair/category` | 1 | One category's products by category id or category link, 48 per page, in the search item shape, with the search sorts and filters, plus `category` {`id`, `name`, `url`, `breadcrumbs`} |
| `POST /api/v1/wayfair/deals` | 1 | The market's current sale events (the Daily Sales list): `event_id`, `slug`, `title`, `url`, `image` per event |

## Markets and sites

Every endpoint takes `country` (lowercase, default `us`). Prices come in the market's currency and are never converted.

| `country` | Site | Currency | `language` |
|---|---|---|---|
| `us` | wayfair.com | USD | `en` |
| `ca` | wayfair.ca | CAD | `en` (default) or `fr` |
| `gb` (alias `uk`) | wayfair.co.uk | GBP | `en` |
| `ie` | wayfair.ie | EUR | `en` |

`language: "fr"` on `ca` answers wayfair.ca in French: French names, labels and dates (`price_label` `Solde`, a badge such as `Offre du Vendredi fou en primeur`). Quote names and labels as returned; translate them for the user only in your own words around the data. A `language` the market does not serve answers `400`. Wayfair no longer sells in Germany or Austria: `de` and `at` answer `400`.

**`site`** reads one of Wayfair's US banner sites (USD, English, `country` `us`): `wayfair` (default), `allmodern`, `birchlane`, `jossandmain` or `perigold`.

| Endpoint | Markets | `site` | `zip` |
|---|---|---|---|
| search | `us`, `ca`, `gb`, `ie` | all 5 (banners with `us`) | - |
| product | `us`, `ca`, `gb`, `ie` | all 5 (banners with `us`) | `us` and `ca` |
| category | `us`, `ca`, `gb`, `ie` | all 5 (banners with `us`) | - |
| deals | `us`, `ca`, `gb`, `ie` | `wayfair` | - |

A banner site with another country, or on deals, answers `400` before anything is charged. Every `data` echoes `country`, `language`, `site` and `currency`.

## Workflow

1. **Find products:** `/search` with `query` on a `country`, add `sort` and filters. Read `redirected_to`: a keyword that matches a category (for example "office chair") answers that category, and a SKU answers `{"type": "product", "sku": ...}` with no items: call `/product` with that `sku`.
2. **Browse:** `/category` with `category_id` (from a category link `...-c413892.html`, `redirected_to.category_id` or `breadcrumbs[].category_id`) or `category_url`, then page with `page`.
3. **One product in full:** `/product` with `sku` (for example `W005006988`) or the product `url`. The market, language and site are read from the link.
4. **One option's price:** `options[].choices[]` carry no price. Call `/product` again with that choice's `option_id` for its price and stock: one call (1 credit) per option. A product with several option groups takes the chosen option ids comma-separated.
5. **Delivery estimate:** `/product` with `zip` (a 5-digit US ZIP on `us`, a postal code such as `M5V 2T6` on `ca`). Without `zip` there is no delivery estimate.
6. **Price history (monitoring):** poll `/product` (or `/search` and `/category` for many SKUs at once) on a schedule. Store `sku`, `option_id`, the time, `price`, `sale_price`, `was_price`, `price_label`, `badge` and `stock_status` per run, and compare runs yourself. There is no price history endpoint.
7. **Sale events:** `/deals` lists the events. For the products on sale, use `/search` or `/category` with `on_sale`, `closeout` or `open_box`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars). A SKU opens that product (`redirected_to`) |
| `country` | string | `us` | `us`, `ca`, `gb` or `ie` |
| `language` | string | `en` | `ca` only: `en` or `fr` |
| `site` | string | `wayfair` | `wayfair`, `allmodern`, `birchlane`, `jossandmain` or `perigold` (banners with `us`) |
| `page` | integer | 1 | 1-based, up to 1,000. A page past the last returns no items and a note |
| `sort` | string | `recommended` | `recommended`, `price_asc`, `price_desc` or `rating` (customer rating) |
| `on_sale` | boolean | false | Products on sale |
| `closeout` | boolean | false | Closeout products |
| `open_box` | boolean | false | Products with an open-box offer (`open_box_price`) |
| `new_arrivals` | boolean | false | New arrivals |
| `in_stock` | boolean | false | Products in stock |
| `brand` | integer, string or list | none | 1 to 5 brand ids: `items[].brand.id` or a Brand facet option id (`44308` = Ebern Designs). Not brand names |
| `min_rating` | integer | none | `5` (five stars), `4` or `3` (that many stars and up) or `1` (every reviewed product) |
| `price_min` / `price_max` | number | none | Price range in the market's currency |
| `filters` | object | none | Any facet of an answer, keyed by `facets[].id` with `facets[].options[].id` values: `{"2471": ["274623"]}`; ranges as `"min~max"`. Up to 12 filter values per call |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | one of | A Wayfair SKU: letters then digits (`W005006988`, `C110260590`, `U110380143`, `I110351475`, `PAGD1773`), as `items[].sku` or "SKU:" on the product page |
| `url` | string | one of | A Wayfair product page (`.../pdp/<name>-<sku>.html`) of a served site; its market, language and site win. A conflicting `country`, `language`, `site` or `sku` answers `400` |
| `option_id` | string or integer | none | `options[].choices[].option_id`; several comma-separated for products with more than one option group. Returns that option's price and stock |
| `zip` | string | none | Delivery estimate: a 5-digit ZIP on `us`, a postal code on `ca`. Not offered on `gb` or `ie` |
| `country`, `language`, `site` | | | As on search |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string or integer | one of | A category id: `413892` or `c413892` (Sofas), from a category link (`...-c413892.html`), `redirected_to.category_id` or `breadcrumbs[].category_id` |
| `category_url` | string | one of | A category page (`/sb0/`, `/sb1/` or `/sb2/` link; filters in the link are kept). A department page (`/cat/`) is not a product list and answers `400` |
| `country`, `language`, `site` | | | As on search |
| `page`, `sort`, `on_sale`, `closeout`, `open_box`, `new_arrivals`, `in_stock`, `brand`, `min_rating`, `price_min`, `price_max`, `filters` | | | As on search |

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `us` | `us`, `ca`, `gb` or `ie` |
| `language` | string | `en` | `ca` only: `en` or `fr` |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/wayfair/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "office chair"}'
```

Captured `data` (US, 2026-11-14; 1 of 48 items and 1 of 33 facets shown, facet options trimmed):

```json
{
  "query": "office chair",
  "items": [
    {
      "position": 1,
      "sku": "AEOI1247",
      "variant_id": "AEOI1247_119222773_127449466",
      "name": "Ergonomic Mesh Commercial Use Office Task Chair",
      "brand": {"id": 55652, "name": "Inbox Zero"},
      "url": "https://www.wayfair.com/furniture/pdp/inbox-zero-ergonomic-mesh-commercial-use-office-task-chair-aeoi1247.html?piid=119222773%2C127449466",
      "image": "https://assets.wfcdn.com/im/00000000/resize-h800-w800%5Ecompr-r85/4127/412736799/image.jpg",
      "price": 48.99,
      "sale_price": 48.99,
      "was_price": 95.96,
      "price_label": "Sale",
      "discount_percent": 49,
      "per_item_price": null,
      "loyalty_savings": null,
      "prices": [
        {"type": "sale", "label": "Sale", "amount": 48.99, "prefix": null, "suffix": null},
        {"type": "previous", "label": null, "amount": 95.96, "prefix": null, "suffix": null}
      ],
      "badge": "Early Black Friday",
      "rating": 4.54,
      "review_count": 2732,
      "stock_status": "in_stock",
      "stock_text": "542 Left in Stock",
      "open_box_price": null,
      "option_counts": [{"name": "Colors", "count": 6}],
      "selected_options": [{"category": "Color", "name": "Black/Black"}, {"category": "Quantity", "name": "1 - piece"}],
      "category": "Office Chairs",
      "sponsored": false
    }
  ],
  "count": 48,
  "total": 19466,
  "total_is_approximate": true,
  "page": 1,
  "page_size": 48,
  "total_pages": 406,
  "sort": "recommended",
  "sorts_offered": [
    {"id": "RECOMMENDED", "name": "Recommended"},
    {"id": "REVIEW_RATING", "name": "Customer Rating"},
    {"id": "PRICE_PER_ITEM_ASC", "name": "Price Per Item: Low to High"},
    {"id": "PRICE_PER_ITEM_DESC", "name": "Price Per Item: High to Low"}
  ],
  "requested_filters": {},
  "applied_filters": [],
  "unapplied_filters": [],
  "facets": [
    {
      "id": "86",
      "name": "Brand",
      "type": "options",
      "options": [{"id": "224", "label": "HON®", "selected": false}, {"id": "1944", "label": "Steelcase", "selected": false}]
    }
  ],
  "redirected_to": {"type": "category", "category_id": "478390", "name": "Office Chairs", "url": "https://www.wayfair.com/furniture/sb0/office-chairs-c478390.html"},
  "country": "us",
  "language": "en",
  "site": "wayfair",
  "currency": "USD"
}
```

"office chair" matched Wayfair's Office Chairs category, so the answer is that category's grid (48 per page) and `redirected_to` names it; a keyword that does not match a category answers 30 items per page. `total` is Wayfair's own count and `total_is_approximate` is always `true`: it moves between calls on keyword pages, so never quote it as an exact catalogue size. `sponsored: true` marks sponsored placements (19 of 48 in this capture). Facet ids (`86` = Brand here) differ between keyword pages and categories: read them from each answer.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/wayfair/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "W005006988", "zip": "10001"}'
```

Captured `data` (US, 2026-11-14; 2 of 20 choices, 2 of 4 dimensions, 1 of 2 specification groups, 2 of 5 features, 1 of 11 images, 2 of 5 review aspects and 1 of 5 reviews shown, description and review summary shortened):

```json
{
  "sku": "W005006988",
  "variant_id": "W005006988_1756067252",
  "name": "Shiflett Oriental Burgundy/Mustard/Black Area Rug",
  "brand": {"id": 30808, "name": "Andover Mills™", "url": "https://www.wayfair.com/brand/bnd/andover-mills-b30808.html"},
  "url": "https://www.wayfair.com/rugs/pdp/andover-mills-shiflett-oriental-burgundymustardblack-area-rug-w005006988.html?piid=1756067252",
  "price": 82.99,
  "sale_price": 82.99,
  "was_price": 197.99,
  "price_label": "Sale",
  "percent_off": 58,
  "per_item_price": null,
  "loyalty_savings": null,
  "prices": [
    {"type": "sale", "label": "Sale", "amount": 82.99, "prefix": null, "suffix": null},
    {"type": "previous", "label": null, "amount": 197.99, "prefix": null, "suffix": null}
  ],
  "badge": "Early Black Friday",
  "limited_time_deal": null,
  "stock_status": "in_stock",
  "max_quantity": 776,
  "part_number": null,
  "options": [
    {
      "category": "Rug Size",
      "total": 20,
      "selected": "Rectangle 5'3\" x 7'3\"",
      "choices": [
        {
          "name": "Rectangle 2' x 3'",
          "option_id": "1756067258",
          "stock_status": "in_stock",
          "url": "https://www.wayfair.com/rugs/pdp/andover-mills-shiflett-oriental-burgundymustardblack-area-rug-w005006988.html?piid=1756067258"
        },
        {
          "name": "Rectangle 2'7\" x 4'",
          "option_id": "1820607097",
          "stock_status": "in_stock",
          "url": "https://www.wayfair.com/rugs/pdp/andover-mills-shiflett-oriental-burgundymustardblack-area-rug-w005006988.html?piid=1820607097"
        }
      ]
    }
  ],
  "dimensions": {
    "overall": "63'' W X 87'' L",
    "weight": "14 lb.",
    "items": [{"group": null, "name": "Overall Dimensions", "value": "63'' W X 87'' L"}, {"group": null, "name": "Pile Height", "value": "0.39'' H"}]
  },
  "specifications": [
    {
      "group": "details",
      "items": [{"name": "Material", "value": "Polypropylene Plastic"}, {"name": "Backing Material", "value": "Jute"}]
    }
  ],
  "features": ["Features a jute backing to provide stability and support", "Made from polypropylene to stand up to heavy foot traffic"],
  "description": "This Oriental area rug brings a classic, traditional feel to your space with its detailed pattern and warm ...",
  "image": "https://assets.wfcdn.com/im/00000000/resize-h800-w800%5Ecompr-r85/5198/51986832/image.jpg",
  "images": ["https://assets.wfcdn.com/im/00000000/resize-h800-w800%5Ecompr-r85/5198/51986832/image.jpg"],
  "breadcrumbs": [
    {"name": "Rugs", "url": "https://www.wayfair.com/rugs/cat/rugs-c215385.html", "category_id": 215385},
    {"name": "Area Rugs", "url": "https://www.wayfair.com/rugs/sb0/area-rugs-c215386.html", "category_id": 215386}
  ],
  "documents": [{"type": "owner_manual", "url": "https://assets.wfcdn.com/dm/document/7ae3585d-d415-08a7-4191-7a786adb2355/1898712.pdf"}],
  "collection": {"id": 672967, "name": "Shiflett"},
  "returns": {"returnable": true, "cancelable": true},
  "rating": 4.67,
  "review_count": 5887,
  "rating_histogram": {"1": 131, "2": 102, "3": 211, "4": 693, "5": 4750},
  "review_summary": {
    "text": "Customers are highly satisfied with the product's appearance, with many describing it as beautiful, ...",
    "label": "AI-generated from customer reviews"
  },
  "review_aspects": [{"name": "Appearance", "sentiment": "positive", "count": 1399}, {"name": "Color", "sentiment": "positive", "count": 868}],
  "reviews": [
    {
      "id": 184986094,
      "rating": 1,
      "date": "2026-11-03",
      "date_text": "11/03/2026",
      "verified": true,
      "badge": "Verified Purchase",
      "title": null,
      "text": "Very disappointed \nUgly and cheap looking \nToo much of a pain to wrap up and return \nWayfair this is a bad product",
      "author": "Anne",
      "location": "Montrose, NY",
      "options": [{"name": "Rug Size", "value": "Rectangle 5'3\" x 7'3\""}],
      "language": "en"
    }
  ],
  "delivery": [{"name": "Ground Delivery", "date_min": "2026-11-15", "date_max": "2026-11-15", "text": "Get it by Sun, Nov 15", "badge": "FREE 2-Day Delivery"}],
  "delivery_zip": "10001",
  "notes": ["options[].choices[] carry no price: call product with that choice's option_id for its price and stock."],
  "country": "us",
  "language": "en",
  "site": "wayfair",
  "currency": "USD"
}
```

The rug comes in 20 sizes, and the price above is for the selected one (`options[].selected`). For the price of another size, send its `option_id`. `delivery` is the estimate for `delivery_zip`; without `zip` it is `null` with a note. `review_summary.label` is the page's own label ("AI-generated from customer reviews"): quote it with the text. `reviews` holds the 5 reviews the page shows, and `title` is always `null`.

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/wayfair/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category_id": "413892", "sort": "price_asc"}'
```

Captured `data` (US, 2026-11-14; item 2 of 48 shown, facets omitted):

```json
{
  "category": {
    "id": "413892",
    "name": "Sofas",
    "url": "https://www.wayfair.com/furniture/sb0/sofas-c413892.html",
    "breadcrumbs": [
      {"name": "Furniture", "url": "https://www.wayfair.com/furniture/cat/furniture-c45974.html"},
      {"name": "Living Room Furniture", "url": "https://www.wayfair.com/furniture/cat/living-room-furniture-c45982.html"},
      {"name": "Sofas", "url": "https://www.wayfair.com/furniture/sb0/sofas-c413892.html"}
    ]
  },
  "items": [
    {
      "position": 2,
      "sku": "W113305437",
      "variant_id": "W113305437_181245992",
      "name": "3-Seater Ultra-Thick Winter Soft Plush Couch Cover – Washable Furniture Protector for Dogs, Pets, Anti-Slip, Anti-Dust Sofa Cushion Cover, 110.24 x 66.93 Inches",
      "brand": {"id": 44304, "name": "Gracie Oaks"},
      "url": "https://www.wayfair.com/furniture/pdp/gracie-oaks-3-seater-ultra-thick-winter-soft-plush-couch-cover-washable-furniture-protector-for-dogs-pets-anti-slip-anti-dust-sofa-cushion-cover-11024-x-6693-inches-w113305437.html?piid=181245992",
      "image": "https://assets.wfcdn.com/im/00000000/resize-h800-w800%5Ecompr-r85/3335/333507045/image.jpg",
      "price": 40.99,
      "sale_price": null,
      "was_price": 46.99,
      "price_label": null,
      "discount_percent": 13,
      "per_item_price": null,
      "loyalty_savings": null,
      "prices": [
        {"type": "primary", "label": null, "amount": 40.99, "prefix": null, "suffix": null},
        {"type": "previous", "label": null, "amount": 46.99, "prefix": null, "suffix": null}
      ],
      "badge": null,
      "rating": 5,
      "review_count": 1,
      "stock_status": "in_stock",
      "stock_text": "Low Stock",
      "open_box_price": null,
      "option_counts": [{"name": "Colors", "count": 3}],
      "selected_options": [{"category": "Upholstery Color", "name": "Khaki"}],
      "category": "Sofas",
      "sponsored": false
    }
  ],
  "count": 48,
  "total": 261284,
  "total_is_approximate": true,
  "page": 1,
  "page_size": 48,
  "total_pages": 5444,
  "sort": "price_asc",
  "requested_filters": {},
  "applied_filters": [],
  "unapplied_filters": [],
  "country": "us",
  "language": "en",
  "site": "wayfair",
  "currency": "USD"
}
```

A price sort on Sofas opens with accessories (a pillow cover, then this couch cover): Wayfair files them in the category. Filter by price or a facet to keep to sofas. This item also shows that `was_price` can come without a `Sale` label (`price_label: null`); the reverse happens too (an Irish item labelled `Sale` with `was_price: null`).

### Sale events

```bash
curl -X POST https://api.scavio.dev/api/v1/wayfair/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (US, 2026-11-14; 2 of 38 events shown):

```json
{
  "events": [
    {
      "event_id": 635914,
      "slug": "bedroom-furniture-sale~ev635914",
      "title": "bedroom furniture sale",
      "url": "https://www.wayfair.com/curated/bedroom-furniture-sale~ev635914.html",
      "image": "https://assets.wfcdn.com/im/00000000/resize-h800-w800%5Ecompr-r85/5189/518969969/image.jpg"
    },
    {
      "event_id": 640190,
      "slug": "sealy-mattresses-more-up-to-60-off~ev640190",
      "title": "Sealy mattresses & more: up to 60% OFF",
      "url": "https://www.wayfair.com/curated/sealy-mattresses-more-up-to-60-off~ev640190.html",
      "image": "https://assets.wfcdn.com/im/00000000/resize-h800-w800%5Ecompr-r85/5190/519081971/image.jpg"
    }
  ],
  "count": 38,
  "notes": [
    "Event pages show only their first few products, so events are listed, not expanded: for sale, closeout or open-box products use search or category with on_sale, closeout or open_box."
  ],
  "country": "us",
  "language": "en",
  "site": "wayfair",
  "currency": "USD"
}
```

Build testing listed 38 events on `us`, 34 on `ca`, 6 on `gb` and 6 on `ie`. The events carry no end date.

### Other markets and sites

- `/search` with `{"query": "canape", "country": "ca", "language": "fr"}` returned 30 items in CAD and French, the first "Canapé inclinable manuel en similicuir de 81,5 po de largeur avec dossier large Emryn" at CAD 949.99, `was_price` 1140, `price_label` `Solde`, `stock_text` "468 en stock", `loyalty_savings` 47.
- `/search` with `{"query": "sofa", "country": "gb"}` answered the Sofas category in GBP (`total` 3,433, approximate), the first item at GBP 340 with `was_price` 460; `/product` for that SKU (U111354571) returned the same prices.
- `/search` with `{"query": "sofa", "site": "perigold"}` answered Perigold's Sofas & Loveseats category in USD, the first item the Dylan Sofa at USD 2,099 with `sale_price: null`.

### Python

```python
import time
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def wayfair(endpoint, body, timeout=180):
    r = requests.post(f"{BASE}/api/v1/wayfair/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()["data"]

SKU = "W005006988"  # Shiflett Oriental area rug

# 1. The product, its selected option and its option ids (1 credit)
p = wayfair("product", {"sku": SKU})
print(p["name"], p["currency"], p["price"], "was", p["was_price"], p["price_label"], p["badge"])

# 2. One reading per size you care about (1 credit per option)
reading = []
for choice in p["options"][0]["choices"][:3]:
    o = wayfair("product", {"sku": SKU, "option_id": choice["option_id"]})
    reading.append({
        "sku": SKU,
        "option_id": choice["option_id"],
        "option": choice["name"],
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "price": o["price"],
        "sale_price": o["sale_price"],
        "was_price": o["was_price"],
        "price_label": o["price_label"],
        "badge": o["badge"],
        "stock_status": o["stock_status"],
    })

# 3. Store `reading` and run this on a schedule: the history is the series you keep.
for row in reading:
    print(row)
```

Compare a price only with earlier readings of the same SKU, the same `option_id` and the same market.

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live; nothing is cached. Every `data` echoes `country`, `language`, `site` and `currency`. Prices are numbers in the market's currency.

- **grid item** (search, category `items[]`) - `position`, `sku`, `variant_id`, `name`, `brand` {`id`, `name`}, `url`, `image`, `price`, `sale_price`, `was_price`, `price_label` (`Sale`, `Closeout`, `Solde` ...), `discount_percent`, `per_item_price` (sets and multi-packs), `loyalty_savings`, `prices[]` {`type` (`sale`, `primary`, `secondary`, `previous`), `label`, `amount`, `prefix`, `suffix`}, `badge` (`Early Black Friday`, `Sale`, `Bundle & Save` ...), `rating`, `review_count`, `stock_status`, `stock_text` (`542 Left in Stock`, `Low Stock`), `open_box_price`, `option_counts[]` {`name`, `count`}, `selected_options[]` {`category`, `name`}, `category`, `sponsored`.
- **search / category** - `items[]`, `count`, `total`, `total_is_approximate`, `page`, `page_size` (30 on keyword pages, 48 on category grids), `total_pages`, `sort`, `sorts_offered[]` {`id`, `name`}, `requested_filters`, `applied_filters[]` (what Wayfair applied, including filters it infers from the keywords), `unapplied_filters[]`, `facets[]` {`id`, `name`, `type` (`toggle`, `options`, `range`), `options[]` {`id`, `label`, `selected`}; range facets add `range` {`min`, `max`, `unit`} and `buckets[]` {`label`, `min`, `max`, `selected`}}, `notes` (when there is something to say); search adds `query` and `redirected_to` {`type` (`category` or `product`), `category_id`, `name`, `url`} or `{type, sku, url}`; category adds `category` {`id`, `name`, `url`, `breadcrumbs[]` {`name`, `url`}}. Facets carry no per-option counts.
- **product** - `sku`, `variant_id`, `name`, `brand` {`id`, `name`, `url`}, `url`, `price`, `sale_price`, `was_price`, `price_label`, `percent_off`, `per_item_price`, `loyalty_savings`, `prices[]`, `badge`, `limited_time_deal` (with an end date when Wayfair shows one), `stock_status`, `max_quantity`, `part_number`, `options[]` {`category`, `total`, `selected`, `choices[]` {`name`, `option_id`, `stock_status`, `url`}}, `dimensions` {`overall`, `weight`, `items[]` {`group`, `name`, `value`}}, `specifications[]` {`group`, `items[]` {`name`, `value`}}, `features[]`, `description`, `image`, `images[]`, `breadcrumbs[]` {`name`, `url`, `category_id`}, `documents[]` {`type`, `url`}, `collection` {`id`, `name`}, `returns` {`returnable`, `cancelable`}, `rating`, `review_count`, `rating_histogram` {`1` to `5`}, `review_summary` {`text`, `label`}, `review_aspects[]` {`name`, `sentiment`, `count`}, `reviews[]` {`id`, `rating`, `date` (ISO), `date_text`, `verified`, `badge`, `title` (always `null`), `text`, `author`, `location`, `options[]` {`name`, `value`}, `language`}, `delivery[]` {`name`, `date_min`, `date_max`, `text`, `badge`} (with `zip`, else `null`), `delivery_zip`, `notes`.
- **deals** - `events[]` {`event_id`, `slug`, `title`, `url`, `image`}, `count`, `notes`.

## Guardrails

- Was price: `was_price` is Wayfair's strikethrough price. Wayfair's US terms define it as the manufacturer's or supplier's suggested price or, without one, "the highest price at which we offered or sold the product at some point in the past". Never call it the previous price or yesterday's price, and never present `discount_percent` / `percent_off` as a measured price drop. For a Flash Deal, Wayfair's terms say an additional strikethrough "represents a recent previous price before the Flash Deal promotion".
- Sale: Wayfair's terms state the Sale tag "signifies that we are selling the product at a discount from a price in the previous 90 days". `price_label` and `was_price` are independent: either can be present without the other.
- Closeout: Wayfair's terms say closeout prices "may fluctuate" and may return to "prices that are equal to or greater than their original prices" after the promotion.
- Those definitions come from Wayfair's US terms (wayfair.com and the AllModern, Birch Lane, Joss & Main and Perigold sites). wayfair.ca, wayfair.co.uk and wayfair.ie publish their own terms; say which market a definition belongs to.
- Price history: there is none in the data. Build it by polling and storing readings; never infer a past price from `was_price`.
- Options: the product `price` is for the selected option. `choices[]` carry no price; each option's price needs its own call with `option_id` (1 credit each). Never assume every size or color costs the same.
- Sets: `per_item_price` is the price per piece of a set or multi-pack, and Wayfair's price sorts order by it. A price-sorted page can therefore look out of order by `price` (a large bulk listing with a tiny per-item price can come first); re-sort yourself when the user wants order by `price`.
- Reviews: `reviews` is the 5 reviews the page shows. There is no review paging, sort or star filter. Use `rating`, `review_count` and `rating_histogram` for the overall picture; never compute a distribution from the 5. `review_summary` is Wayfair's AI-generated summary: quote its label.
- Totals: `total` is approximate (`total_is_approximate: true`) and moves between calls on keyword pages. Do not quote it as an exact count.
- Brand: `brand` takes brand ids (`items[].brand.id` or a Brand facet option id), not names. Search the brand name first, read the id, then filter.
- Delivery: `zip` works on `us` and `ca`; it answers `400` on `gb` and `ie`. Delivery dates are Wayfair's estimate for that ZIP on the day of the call, not a promise.
- Deals: `/deals` lists events, not their products, and carries no end dates. Do not claim an event's products or end time from it.
- Stock: `stock_text` is Wayfair's own wording (`542 Left in Stock`, `Low Stock`); quote it as shown and do not turn it into an exact inventory figure.
- Currency: always give the currency and market next to a price. Never compare or average prices across `us`, `ca`, `gb` and `ie` without converting explicitly, with the rate and its date.
- Sponsored: `sponsored: true` items are paid placements. Say so when ranking results, and never present a sponsored position as an organic rank.
- Not available: price history, review paging, search suggestions (typeahead), the products inside a sale event, seller data (Wayfair is the seller of every product), cart, checkout and order data; Germany and Austria (Wayfair no longer sells there).
- Terms: Wayfair's Terms of Use say users agree not to "use any of the Sites in any manner that could overburden or impair any of the Sites" and prohibit "unauthorized copying, reproduction, ... or duplicating all or any part of the Sites". This is not legal advice; the user is responsible for reading the current terms for their market and use case. Do not republish Wayfair product photos; link product pages instead.
- Never fabricate prices, SKUs, option ids, category ids, delivery dates, reviews or ratings. Only return what the API returned, with the market and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` outside `us`, `ca`, `gb`, `ie` (`de` / `at`: "Wayfair no longer sells in Germany or Austria"); `language` other than `en` outside `ca`; a banner `site` with a country other than `us`, or any banner on `/deals`; a `sku` that is not letters then digits; neither `sku` nor `url`, or a `sku` that conflicts with the `url`; a `url` that is not a product page of a served site, or that conflicts with `country`, `language` or `site`; `zip` on `gb` / `ie`, or not a 5-digit US ZIP / Canadian postal code; a `sort` outside the four; `min_rating` outside 1, 3, 4, 5; `price_min` not below `price_max`; `brand` that is not 1 to 5 numeric ids; a `filters` key that is not a facet id or a value that is not an option id or `min~max`; more than 12 filter values; a `category_url` that is a department page (`/cat/`) or not a category page.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Wayfair has no product W999999999 on this site.", "Wayfair has no product category ... on this site.", a category id that is a department page, "Wayfair found nothing for this query.", or "Wayfair shows no sale events on this site right now." When Wayfair answers a different SKU or category than the one sent, the `404` names it ("send that SKU instead"). Take SKUs and ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api).
- `502` means Wayfair data was temporarily unavailable ("Wayfair is temporarily unavailable. Please try again."). Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Wayfair is busy ("Wayfair is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.57.0
npm install scavio@0.58.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.wayfair.search({ query: "office chair", sort: "price_asc" });
const { data: rug } = await scavio.wayfair.product({ sku: "W005006988", zip: "10001" });
const { data: size } = await scavio.wayfair.product({ sku: "W005006988", option_id: "1820607097" });
const { data: sofas } = await scavio.wayfair.category({ category_id: "413892", on_sale: true });
const { data: events } = await scavio.wayfair.deals({ country: "ca", language: "fr" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.wayfair.search(...)`, `client.wayfair.product(...)`, `client.wayfair.category(...)` and `client.wayfair.deals(...)`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all four endpoints as tools: `search_wayfair`, `get_wayfair_product`, `get_wayfair_category` and `get_wayfair_deals`. Wayfair is opt-in: add `wayfair` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.55.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,wayfair"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/wayfair-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api), [product](https://scavio.dev/docs/wayfair-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api), [category](https://scavio.dev/docs/wayfair-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api), [deals](https://scavio.dev/docs/wayfair-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api). Overview: [Wayfair API](https://scavio.dev/wayfair-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api).
