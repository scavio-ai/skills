# Enjoei API - Second-Hand Fashion Prices, Offers, Shop Sold Listings, Seller Reviews

Read Enjoei (enjoei.com.br, Brazil's second-hand fashion marketplace): keyword search, department and category listings, one listing in full, a seller's shop with its counters and rating, the shop's listings on sale, its sold listings and its buyer reviews, the category tree and search suggestions. www.enjoei.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in.

**The job this skill is for: what a second-hand item is listed for on Enjoei today, what offer the seller takes, and what a shop has sold.** Enjoei is a marketplace of individual closets and small shops; every listing is one seller's own price, and a seller can cut it (`original_price` against `price`) or accept offers within a range. On 2026-11-27 the FARM dress `153252795` read R$ 75 against R$ 90 (17 percent off), "em até 2x R$ 37,50 sem juros", a new-buyer line "R$ 63,75 na 1ª compra", and an offer range of R$ 45 to R$ 74. The shop @utstore held 706 listings and 2,008 sales, a 4.7 rating over 809 reviews and an average shipping time of 1 day.

Seven limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Listings are slow.** Search, category, shop listings and suggestions usually take 10-40 seconds and can take about two minutes (in the captures: 22.4, 23.0, 28.8 and 33.0 seconds). Product, shop, sold, reviews and categories usually take 2-10 seconds. Allow a client timeout of at least 180 seconds.
- **Pages by cursor.** Search, category, shop listings and shop reviews are paged by `next_cursor`: a page is reached from the one before it, there is no jump to page 12. Sold listings take a `page` number, 1 to 50.
- **Totals stop at 10,000.** `total` is Enjoei's own count; `total_capped` true means 10,000 or more. Narrow with filters to reach the rest.
- **Sold listings: listed price, no date.** `/shop-sold` returns each sold listing with the price it was listed at. Enjoei shows no sold date and at most 50 pages of 40 (2,000 sold listings) per shop. There is no site-wide sold search.
- **No shipping quote.** Shipping cost by CEP is shown to signed-in buyers only. Listing cards carry `shipping.free` and `shipping.type` (`charge_by_weight`, `hand_deliver`), nothing more.
- **Handles, never people.** Every seller is returned as an @handle (and a seller id on shops). Seller names, avatars, cities and the shop's own description are never returned; reviews carry no reviewer names or photos.

Enjoei has no public API for its listings, shops or reviews. They are shown on enjoei.com.br to any visitor, and this skill reads those public pages with one Scavio key.

See also: Depop `depop-api`, Poshmark `poshmark-api`, thredUP `thredup-api`, Vinted `vinted-api`, Mercari `mercari-api` (second-hand marketplaces outside Brazil); Mercado Libre `mercadolibre-product-data` (Brazil marketplace); Brazilian retail: Centauro `centauro-api`, Magazine Luiza `magalu-magazine-luiza-api`.

## When to trigger

Use this skill when the user asks to:
- Search Enjoei by keyword (in Portuguese: "vestido farm", "bolsa couro", "tenis nike"), sorted by relevance, price or discount
- Filter Enjoei listings by brand, clothing, waist or shoe size, price range, new or used, listing age (24 hours to 30 days), Enjoei Pro stores or celebrity closets (famosas), or discount band
- Browse one Enjoei department, category or subcategory (Moças, Rapazes, Crianças, Casa & Decor)
- Read one Enjoei listing: price, original price, installments, the make-an-offer range, size, verified brand, condition, weight and photos
- Price a second-hand item against what similar listings ask on Enjoei, or against what one shop has sold
- Check an Enjoei seller before buying: counters (listings, sold, followers), rating, review count, on-time delivery history, average shipping time
- List an Enjoei shop's listings on sale, its sold listings, or its buyer reviews (all, positive or negative)
- Read the Enjoei category tree or search suggestions

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api) - email or Google, no card required.
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
| `POST /api/v1/enjoei/search` | Keywords: 30 listings per page by cursor with total, price, original price, discount, condition, size, shipping type, badges and @handle; brand counts, departments, subcategories, sizes and store kinds as facets | 1 |
| `POST /api/v1/enjoei/category` | One department, category or subcategory by the slugs `/categories` lists, same items, sorts, filters and facets as search | 1 |
| `POST /api/v1/enjoei/categories` | The category tree, three levels, with the inputs of `/category` on every node | 1 |
| `POST /api/v1/enjoei/product` | One listing: description, status, price, list price, discount, installments, new-buyer line, make-an-offer range, sizes, brand (verified flag), condition, weight, photos, breadcrumb, seller id and @handle | 1 |
| `POST /api/v1/enjoei/shop` | A shop by @handle: seller id, join date, vacation flag, badge, counters (listings, sold, likes, followers, following), rating, review count, on-time history, average shipping time | 1 |
| `POST /api/v1/enjoei/shop-listings` | A shop's listings on sale, in the shop page's order, 20 on page 1 and 30 after, by cursor, with facets | 1 |
| `POST /api/v1/enjoei/shop-sold` | A shop's sold listings with the listed price, 40 per page, pages 1-50 | 1 |
| `POST /api/v1/enjoei/shop-reviews` | A shop's buyer reviews (all, positive or negative), 20 per page by cursor: score, date, text, feedback tags; the star and feedback summary | 1 |
| `POST /api/v1/enjoei/suggestions` | The search-box suggestions for the start of a query, each with the department it narrows to | 1 |

Brazil only: there is no `country` parameter. Every answer carries `market` (br), `currency` (BRL) and `language` (pt-BR), and most carry `notes`.

## Prices: price, original price, offers and installments

| Field | Meaning |
|---|---|
| `price` | The price the seller asks now, in BRL (R$ 136.80 on the search item below) |
| `original_price` (listings), `list_price` (product) | The price before the seller's cut (R$ 190); equal to `price` when there is no cut |
| `discount_percent` | The cut against the original price, computed from the two on listings (28); 0 when none |
| `tags` (listings) | The card's badges as written: a percent (`28%`) or `barateou` (the seller lowered the price) |
| `installments_text` (product) | The installment line as the site writes it ("em até 2x R$ 37,50 sem juros") |
| `promo_text` (product) | A new-buyer coupon line when the site shows one ("R$ 63,75 na 1ª compra"); not applied to `price` |
| `offer` (product) | `{accepts_offers, min_price, max_price}`: the make-an-offer range the seller accepts (R$ 45 to R$ 74) |
| `shipping` (listings) | `{free, type}`: `charge_by_weight` (the buyer pays by weight) or `hand_deliver`; no cost |
| `price_detail` (product) | `full`, or `basic` when the pricing details could not be read and the listing's own price is shown (no offer range, installments or sizes that time) |

- Quote "vestido preto tropical farm, size P, used: R$ 136.80 (from R$ 190, 28 percent off), from @enjoei-pro on enjoei.com.br on 2026-11-27", with the condition, the size, the handle and the date.
- `promo_text` and the offer range are what the site shows; never apply a coupon or an offer to a price yourself. Report Enjoei's prices and labels and the arithmetic only, and never judge a listing as a good deal.

## Workflow

1. **Find listings.** `/search` with `query` (`vestido farm`), or `/category` with `department` (and `category`, `subcategory`) from `/categories` `params`. Each item's `id` is the input of `/product`; `seller_handle` is the input of the shop endpoints.
2. **Narrow.** Read `facets` and send slugs back: `brand` (`facets.brands[].slug`, e.g. `farm`), `size_clothes` / `size_waist` / `size_shoes` (`facets.sizes`), `store_kind`; plus `price_min` / `price_max`, `condition`, `listed_within`, `discount_min` / `discount_max`. There is no colour filter: put the colour in `query` (`vestido preto`).
3. **Next pages.** Send the answer's `next_cursor` as `cursor` with the same query and filters. `has_more` false means the last page.
4. **One listing.** `/product` with `product_id` (or `url`): price, installments, offer range, sizes, brand, condition, weight, photos and `seller` {`id`, `handle`}.
5. **The seller.** `/shop` with `handle` for counters, rating and on-time history; `/shop-reviews` with `handle` (or `shop_id`) for the reviews; `/shop-listings` for what is on sale now.
6. **Sold prices for a shop.** `/shop-sold` with `handle` and `page` 1-50: each sold listing with the price it was listed at, in the order the shop page lists them.
7. **Watching prices:** there is no history. Poll the same searches and listings on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`) and category (`/category`)

| Parameter | Description |
|---|---|
| `query` (search, required; category, optional) | Keywords in Portuguese, 1-200 characters |
| `department` (category, required) | A department slug from `/categories` `departments[].params.department`: `feminino`, `masculino`, `infantil`, `casa-e-decor`, `eletronicos`, ... |
| `category` (category) | A category slug in that department (`feminino-roupas`); must start with the department slug |
| `subcategory` (category) | A subcategory slug in that category (`feminino-roupas-vestidos`); needs `category` |
| `sort` | `relevance` (default), `price_asc`, `price_desc`, `discount` (largest discount first) |
| `brand` | Brand slug(s) as `facets.brands[].slug` writes them (`farm`, `zara`, `le-lis-blanc`), one or up to 10 |
| `size_clothes`, `size_waist`, `size_shoes` | Size slug(s) from `facets.sizes` (`pp`, `p`, `m`, `g`, `gg`, `38`, `37`), up to 10 each |
| `price_min`, `price_max` | Price range in BRL |
| `condition` | `new` (never used) or `used` |
| `listed_within` | `24h`, `7d`, `14d` or `30d` |
| `store_kind` | `pro` (Enjoei Pro stores) or `celebrity` (Enjoei's famosas, celebrity closets) |
| `discount_min`, `discount_max` | Discount band in percent, 0-100 |
| `cursor` | The `next_cursor` of the previous page |

Lists cover sellers who ship to all of Brazil. A search with no listings returns an empty `200`. A category slug outside its department is a `400` before anything is charged; an unknown slug inside it lists nothing (an empty `200`).

### Product (`/product`)

Send exactly one of `product_id` (digits, `items[].id`, e.g. `153252795`) or `url` (a product link, `https://www.enjoei.com.br/p/<name>-<id>`).

### Shop (`/shop`), shop listings (`/shop-listings`), shop sold (`/shop-sold`) and shop reviews (`/shop-reviews`)

| Parameter | Description |
|---|---|
| `handle` | The shop's @handle (`items[].seller_handle`, `utstore`), with or without the @, or the shop link `https://www.enjoei.com.br/@utstore` |
| `shop_id` (reviews, instead of handle) | The seller id (`shop.seller_id`, `product.seller.id`), e.g. `351787` |
| `cursor` (listings, reviews) | The `next_cursor` of the previous page |
| `page` (sold) | 1-50 (40 sold listings a page) |
| `filter` (reviews) | `all` (default), `positive` or `negative`: Enjoei's own review filters |

### Suggestions (`/suggestions`) and categories (`/categories`)

`/suggestions` takes `query`, 1-100 characters (`vestido`). `/categories` takes an empty body `{}`.

## Examples

### One search item

Request `{"query": "vestido farm"}` (1 credit): `total` 10000 (`total_capped` true), 30 items, `next_cursor` `2~MTczMjk4ODQ3MDIzNDEyNDEzOjE`, facets with 242 brands (FARM 50,156, Adidas 109, Zara 82), 6 departments and the size lists. One item:

```json
{
  "id": "149065330",
  "url": "https://www.enjoei.com.br/p/vestido-preto-tropical-farm-149065330",
  "title": "vestido preto tropical farm",
  "brand": "farm",
  "price": 136.8,
  "original_price": 190,
  "discount_percent": 28,
  "currency": "BRL",
  "condition": "used",
  "size": "P",
  "sizes": ["P"],
  "shipping": { "free": false, "type": "charge_by_weight" },
  "department": "mocas",
  "category": "mocas-roupas",
  "subcategory": "mocas-roupas-vestidos",
  "tags": ["28%"],
  "bundle_allowed": true,
  "seller_handle": "enjoei-pro"
}
```

Items carry the listing's own department slugs (`mocas-roupas-vestidos`), which are not the inputs of `/category` (`feminino-roupas-vestidos`): take those from `/categories` or `facets`.

### One listing

Request `{"product_id": "153252795"}` (1 credit), abridged:

```json
{
  "id": "153252795",
  "title": "vestido farm um ombro só estampado vermelho",
  "status": "published",
  "available": true,
  "price": 75,
  "list_price": 90,
  "discount_percent": 17,
  "installments_text": "em até 2x R$ 37,50 sem juros",
  "promo_text": "R$ 63,75 na 1ª compra",
  "offer": { "accepts_offers": true, "min_price": 45, "max_price": 74 },
  "bundle_allowed": true,
  "size": "M",
  "sizes": [{ "name": "M", "slug": "m", "available": true }],
  "brand": { "name": "farm", "slug": "farm", "verified": true },
  "condition": "used",
  "weight_kg": 0.5,
  "hand_delivery": false,
  "single_piece": true,
  "category_slug": "feminino-roupas-vestidos-assimetrico",
  "price_detail": "full"
}
```

The listing also carried the seller's description, 2 photos, a 4-step `breadcrumb` (moças > roupas > vestidos > assimétrico) and `seller` {`id`, `handle`}.

### A shop, its sales and its reviews

- `/shop` `{"handle": "utstore"}`: `seller_id` 351787, `joined_at` 2014-01-25, `badge` "loja em destaque", `counters` {`listings` 706, `sold` 2008, `likes` 73, `followers` 1504, `following` 2}, `rating` 4.7, `review_count` 809, `recent_deliveries` 5 x `on_time`, `average_shipping_time` "1 dia".
- `/shop-listings` `{"handle": "utstore"}`: `total` 706, 20 items on page 1, first the calça farm sarja bordada sol preta, new, size 38, R$ 399 against R$ 499.
- `/shop-sold` `{"handle": "utstore"}`: `total` 1998, `total_pages` 50, 40 a page, first a blusa manga longa contraste silk at R$ 149, then a vestido farm viés estampado amor de mar at R$ 398. No sold dates.
- `/shop-reviews` `{"handle": "utstore"}`: 20 reviews and a summary:

```json
{
  "items": [
    { "score": 5, "date": "2026-11-20", "text": "segunda compra com a loja, indico demais!!", "feedback_tags": ["envio rápido", "ótima embalagem", "ótima comunicação", "ótimo negociante", "produto bem descrito", "ótimas fotos"] }
  ],
  "summary": {
    "score": 4.7,
    "total": 809,
    "stars": [{ "stars": 5, "total": 719 }, { "stars": 4, "total": 33 }, { "stars": 3, "total": 19 }, { "stars": 2, "total": 10 }, { "stars": 1, "total": 28 }],
    "feedbacks": [{ "label": "ótima comunicação", "total": 29 }, { "label": "ótimas fotos", "total": 28 }, { "label": "envio rápido", "total": 26 }]
  }
}
```

Many reviews carry a score and tags with `text` null.

### Category, tree and suggestions

- `/category` `{"department": "feminino", "category": "feminino-roupas", "subcategory": "feminino-roupas-vestidos"}`: `total` 10000 (capped), first a vestido longo from griff, used, size M, R$ 39 against R$ 53.
- `/categories` `{}`: 5 top-level nodes (Moças, Rapazes, Crianças, enjoei pro, Outros) and 190 nodes in all; each node's `params` {`department`, `category`, `subcategory`} is the input of `/category` (null on navigation nodes such as enjoei pro and Outros).
- `/suggestions` `{"query": "vestido"}`: vestido, vestido farm, vestido longo, then "vestido em Moças" (`department` mocas), "vestido em Kids", "vestido em Casa", ... (10).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def enjoei(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/enjoei/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Used FARM dresses in size M, biggest discount first (1 credit)
hits = enjoei("search", {"query": "vestido", "brand": "farm", "size_clothes": "m", "condition": "used", "sort": "discount"})["data"]
for it in hits["items"][:5]:
    print(it["title"], it["price"], it["original_price"], it["discount_percent"], it["seller_handle"])

# 2. The next page comes from the cursor (1 credit)
if hits["has_more"]:
    more = enjoei("search", {"query": "vestido", "brand": "farm", "size_clothes": "m", "condition": "used", "sort": "discount", "cursor": hits["next_cursor"]})["data"]

# 3. One listing with its offer range, then its shop (1 credit each)
item = enjoei("product", {"product_id": hits["items"][0]["id"]})["data"]
print(item["price"], item["offer"], item["installments_text"])
shop = enjoei("shop", {"handle": item["seller"]["handle"]})["data"]
print(shop["rating"], shop["review_count"], shop["counters"]["sold"], shop["average_shipping_time"])

# Enjoei listings change every hour. Store each answer with fetched_at and run this
# on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `market`, `currency` and `language`.

- **search / category** - `query` (search), `department`, `category`, `subcategory`, `query` (category), `sort`, `filters` (the filters as applied), `page`, `total`, `total_capped`, `count`, `has_more`, `next_cursor`, `items[]` {`id`, `url`, `title`, `brand`, `price`, `original_price`, `discount_percent`, `currency`, `condition`, `size`, `sizes`, `shipping` {`free`, `type`}, `department`, `category`, `subcategory`, `image`, `tags`, `bundle_allowed`, `seller_handle`}, `page_size` (30), `facets` {`brands[]` {`slug`, `name`, `count`}, `departments[]`, `subcategories[]`, `sizes` {`clothes`, `waist`, `shoes`}, `store_kinds[]`, each {`slug`, `name`}} (best-effort: null when the page did not show them), `notes`.
- **categories** - `count`, `node_count`, `departments[]` {`name`, `slug`, `url`, `params` {`department`, `category`, `subcategory`}, `children[]`} three levels deep.
- **product** - `id`, `url`, `title`, `description`, `status`, `available`, `price`, `list_price`, `discount_percent`, `installments_text`, `promo_text`, `offer` {`accepts_offers`, `min_price`, `max_price`}, `bundle_allowed`, `size`, `sizes[]` {`name`, `slug`, `available`}, `brand` {`name`, `slug`, `verified`}, `condition`, `weight_kg`, `hand_delivery`, `single_piece`, `photos[]`, `category_slug`, `breadcrumb[]` {`title`, `url`}, `seller` {`id`, `handle`}, `price_detail`, `notes`.
- **shop** - `handle`, `seller_id`, `url`, `joined_at`, `on_vacation`, `business`, `badge`, `counters` {`listings`, `sold`, `likes`, `followers`, `following`}, `rating`, `review_count`, `recent_deliveries[]` (`on_time`, `delayed`, `cancelled`), `average_shipping_time` (shown after 5 sales), `notes`.
- **shop-listings** - `handle`, `seller_id`, `page`, `total`, `total_capped`, `count`, `has_more`, `next_cursor`, `items[]` (the listing fields above), `facets`, `notes`.
- **shop-sold** - `handle`, `page`, `page_size` (40), `total`, `total_pages`, `has_more`, `count`, `items[]` {`id`, `url`, `title`, `price` (the listed price), `currency`, `image`, `status`}, `notes`.
- **shop-reviews** - `handle`, `seller_id`, `filter`, `page_size`, `count`, `has_more`, `next_cursor`, `items[]` {`score`, `date`, `text`, `feedback_tags`}, `summary` {`score`, `total`, `stars[]` {`stars`, `total`}, `feedbacks[]` {`label`, `total`}}, `notes`.
- **suggestions** - `query`, `count`, `suggestions[]` {`text`, `query`, `department`} (`department` null means all of Enjoei).

## Guardrails

- Name it "Enjoei (enjoei.com.br, Brazil's second-hand fashion marketplace)" on first mention. Enjoei accounts, carts, offers and checkout are not read or made.
- Prices: quote `price` with `original_price` (or `list_price`), the condition, the size, the @handle and the `fetched_at` date, in BRL (R$). Prices are what a visitor who is not signed in sees: new-buyer coupons and make-an-offer prices are not applied.
- Installments and coupons: quote `installments_text` and `promo_text` exactly as given. Never compute an installment, apply a coupon or assume an offer inside the range will be accepted.
- Sold listings: `/shop-sold` gives the listed price of one shop's sold listings, with no sold date and at most 2,000 per shop. Never present one shop's sales as Enjoei-wide sold prices, and never invent a sale date or a final price.
- Totals: `total` stops at 10,000. Never call a capped total the number of listings.
- Shipping: there is no shipping cost. Say `shipping.type` as given and that the cost depends on the buyer's CEP, shown only to signed-in buyers.
- Sellers: refer to a seller by the @handle only. Names, avatars and cities are not returned; never try to find out who is behind a handle, and use shop data to judge a seller before a purchase, not to profile or contact a person.
- Reviews: no reviewer names or photos are returned. Quote a review as "an Enjoei buyer review" with its score and date; never try to identify a reviewer.
- Comparing Enjoei with Depop, Mercado Libre or a retailer: compare the same brand, item, size, condition and date. Never call one site cheaper beyond the numbers shown.
- Images and copy: do not republish listing photos or sellers' descriptions; refer to listings by `id` and `url` instead.
- Not available: shipping quotes by CEP, a colour filter (put the colour in `query`), product comments, a site-wide sold search, sold dates, coupons, Black Friday dates, price history (poll and store), account data, offers, cart or checkout. This API cannot buy, make an offer, like or message.
- Terms: Scavio does not store Enjoei data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Enjoei's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, listings, sold prices, ratings or reviews. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "send one of product_id or url"; "send one of handle or shop_id"; "Enjoei has no color filter: put the colour in query (e.g. vestido preto)"; "subcategory needs its category"; "category <slug> is not in department <slug>: ..."; "cursor must be the next_cursor of the previous page"; "page must be a whole number from 1 to 50. Enjoei lists at most 50 pages of 40 sold listings (2,000) per shop."; "price_min must not be above price_max"; "brand takes at most 10 values".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Enjoei has no product <id>.", "Enjoei has no shop @<handle>.", "Enjoei has no such category.". A search or filter set with no listings is an empty `200`, not a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api).
- `502` and `503` mean Enjoei data was temporarily unavailable ("Enjoei is temporarily unavailable. Please try again."; "Enjoei is busy right now. Please retry in a few seconds.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.103.0
npm install scavio@0.104.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.enjoei.search({ query: "vestido farm", sort: "discount", condition: "used" });
const { data: dresses } = await scavio.enjoei.category({ department: "feminino", category: "feminino-roupas", subcategory: "feminino-roupas-vestidos" });
const { data: tree } = await scavio.enjoei.categories({});
const { data: item } = await scavio.enjoei.product({ product_id: "153252795" });
const { data: shop } = await scavio.enjoei.shop({ handle: "utstore" });
const { data: onSale } = await scavio.enjoei.shopListings({ handle: "utstore" });
const { data: sold } = await scavio.enjoei.shopSold({ handle: "utstore", page: 1 });
const { data: reviews } = await scavio.enjoei.shopReviews({ handle: "utstore", filter: "negative" });
const { data: typed } = await scavio.enjoei.suggestions({ query: "vestido" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.enjoei.search(...)`, `category`, `categories`, `product`, `shop`, `shop_listings`, `shop_sold`, `shop_reviews` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 9 endpoints as tools: `search_enjoei`, `get_enjoei_category`, `get_enjoei_categories`, `get_enjoei_product`, `get_enjoei_shop`, `get_enjoei_shop_listings`, `get_enjoei_shop_sold`, `get_enjoei_shop_reviews` and `get_enjoei_suggestions`. Enjoei is opt-in: add `enjoei` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.103.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,enjoei"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/enjoei-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api), [category](https://scavio.dev/docs/enjoei-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api), [categories](https://scavio.dev/docs/enjoei-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api), [product](https://scavio.dev/docs/enjoei-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api), [shop](https://scavio.dev/docs/enjoei-shop?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api), [shop listings](https://scavio.dev/docs/enjoei-shop-listings?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api), [shop sold](https://scavio.dev/docs/enjoei-shop-sold?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api), [shop reviews](https://scavio.dev/docs/enjoei-shop-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api), [suggestions](https://scavio.dev/docs/enjoei-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api). Platform page: [scavio.dev/enjoei-api](https://scavio.dev/enjoei-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=enjoei-api).
