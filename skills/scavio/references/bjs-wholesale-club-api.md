# BJ's Wholesale Club API - Club Prices, Instant Savings, Coupons, Reviews

Read BJ's Wholesale Club (bjs.com, the US warehouse club): keyword search and category listings with BJ's online price, sale, coupon, member-only flag, rating and bought-last-month count, one product in full with UPC, regular price, savings, offer dates and club eligibility, the category tree, customer reviews with BJ's own AI review summary and Q&A, BJ's guest coupon book and the club directory. www.bjs.com only (United States, USD, English). Every endpoint returns structured JSON at 1 credit per call.

**The job this skill is for: BJ's prices, instant savings and coupons.** What an item costs at bjs.com today, whether an instant saving or a manufacturer coupon runs on it, and until when. On 2026-11-26 Scotch-Brite 420-Sheet Lint Rollers, 4 pk. (`3000000000005430255`, item `336678`, UPC `68060497901`) read `price` $9.99 against `regular_price` $12.99, `savings` 3, `offer` from 2026-11-12 to 2026-12-25 (UTC). A search for `coffee` read BJ's `total` 125 and its first 40 results: Folgers Classic Roast Ground Coffee 43.5 oz. $24.79 with `coupon` "$4.00 off" and `bought_last_month` 15,079; Maxwell House 43.1 oz. $21.78 with "$2.50 off" and the badge "NEW Lower Price"; Lavazza Espresso Whole Bean 2 lbs. $23.99 with a `sale` at $18.99 from 2026-11-12 to 2026-12-24. The second job is the coupon book: 268 of BJ's 567 guest offers as the coupon page loaded them, each with its value, redemption limit, expiry and qualifying UPCs. Pair it with `costco-product-data` and `sams-club-product-data` for the same item at the other US warehouse clubs (same UPC or model).

Eight limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Slow pages: allow 240 seconds.** In the captures, the club directory answered in about 3 seconds, a product in 14-86, coupons, reviews and categories in 52-86, category 72 and search 110. Set a client timeout of at least 240 seconds.
- **Member-only items: a flag and the list price, nothing more.** Where BJ's shows "Member Only Price" to a visitor (TVs, doorbusters), `member_only_price` is `true` and `price` is the list price BJ's shows; the member price, sale price and sale dates are not returned. On the TV category 14 of 40 items were member-only: a Samsung 65" U8000HD read `price` $399.99 with `member_only_price` true and no `sale`. Never present the list price as the member price, and never guess one.
- **Club-only items have no online price.** An item sold only in clubs has `club_only` true and `price` null. Say it is sold in clubs; never fill in a price.
- **The club is BJ's choice, not yours.** On search and category, `club_price`, `club_was_price`, `club_sale`, `in_stock_club` and `fulfillment_club` belong to the club BJ's assigned to the visit, named in `priced_for` {`club_id`, `name`, `city`, `state`}. The TV category was priced for Jersey City, NJ (club `0044`); the coffee search had `priced_for` null, so its prices are online prices only. There is no parameter to choose a club, no price or stock at a club you pick, and no ZIP club finder: say so plainly when a user asks for a club near them.
- **40 results, no deeper paging.** Search and category return the first 40 results BJ's lists (`page_size` 40) with BJ's own `total`; BJ's page parameter is ignored, so results past 40 are not served. Narrow the query or browse a smaller category instead.
- **The product page has no club price.** `/product` returns the online price; club prices differ from club to club and are not returned. `fulfillment` lists, per item number, the club ids eligible for same-day delivery, pickup in club, ship from club, fresh delivery and EBT.
- **No history, no gas.** Nothing is cached or kept: poll and store your own series. BJ's Gas prices and a weekly ad (BJ's has none) are not served.

BJ's has no public API or product feed for its catalog, prices or coupons. Its affiliate program runs on the CJ network with links, not a product data feed. Prices, instant savings and coupons are shown on bjs.com to every visitor, and this skill reads those public pages with one Scavio key.

BJ's says it operates 263 clubs and 199 BJ's Gas locations in 21 states (fiscal 2025 results, March 2026 release); the club directory listed 283 club ids in 22 states on 2026-11-26 because it counts announced openings. Quote these with their source, never from the samples.

See also: for the same item at Costco use `costco-product-data`; at Sam's Club `sams-club-product-data`; at Walmart `walmart-product-data`; at Target `target-product-data`; at Amazon `amazon-product-data`; prices across retailers `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Price an item at BJ's Wholesale Club online, with its regular price, instant savings and offer dates
- Check which BJ's items carry a manufacturer or BJ's coupon, and for how much
- List BJ's coupon book with values, redemption limits, expiry dates and qualifying UPCs
- Search bjs.com by keyword, or list a BJ's category (TVs, grocery, coffee), with BJ's total, facets and departments
- See whether an item is flagged "Member Only Price" or sold in clubs only
- Read one BJ's product in full: UPC, model, specifications, variants, unit price and the clubs eligible for same-day delivery, pickup, ship from club or EBT
- Read BJ's customer reviews with the rating histogram, recommend ratio and BJ's own AI review summary, and the product's questions and answers
- Browse the BJ's category tree, or list every BJ's club in a state
- Compare one item at BJ's, Costco and Sam's Club (with `costco-product-data` and `sams-club-product-data`)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=bjs-wholesale-club-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=bjs-wholesale-club-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Allow a client timeout of at least 240 seconds.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/bjs/search` | Keywords: the first 40 results with BJ's total, online price, sale, club price of the assigned club, coupon, member-only and club-only flags, rating, bought last month, facets, departments and related searches | 1 |
| `POST /api/v1/bjs/category` | One category's products, the first 40, sorted as BJ's lists them, with its subcategories and the same fields as search | 1 |
| `POST /api/v1/bjs/product` | One product by id or link: UPC, model, price, regular price, savings, offer dates, MAP price, unit price, variants, specifications, rating, and the clubs eligible for each fulfillment option | 1 |
| `POST /api/v1/bjs/categories` | BJ's full category tree (about 980 categories) or one category's subtree, with product counts | 1 |
| `POST /api/v1/bjs/reviews` | Reviews of one product, 10 per page newest first, with the rating histogram, recommend ratio, themes, BJ's AI review summary and page 1 of Q&A | 1 |
| `POST /api/v1/bjs/coupons` | BJ's guest coupon book: offer, brand, value, type, limit, active and expiry dates, qualifying UPCs and GTINs | 1 |
| `POST /api/v1/bjs/clubs` | BJ's club directory, all clubs or one state's: club id, name, state and bjs.com page | 1 |

US only: there is no `country` or `language` parameter.

## Prices: online price, sale, club price, member-only, coupons

| Field | Meaning |
|---|---|
| `price` | Search and category: BJ's online price. Product: the online price, the offer price while an instant saving runs. `null` on a club-only item |
| `was_price`, `sale` {`price`, `starts_at`, `ends_at`} | Search and category: BJ's struck-through price and a running sale with its dates, as given |
| `regular_price`, `savings`, `offer` {`starts_at`, `ends_at`} | Product: the regular price, the instant savings amount and the offer window, as given (UTC) |
| `map_price` | Product: the minimum advertised price BJ's gives for the item |
| `unit_price`, `unit_of_measure` | Product: BJ's unit price where it gives one; `null` otherwise |
| `club_price`, `club_was_price`, `club_sale` | Search and category: the price at the club named in `priced_for`; `null` when BJ's assigned no club or gives no club price |
| `member_only_price` | `true` where BJ's shows "Member Only Price" to a visitor: `price` is then the list price, with no member price, sale price or sale dates |
| `club_only` | `true` for an item sold in clubs only: `price` is `null` |
| `coupon` | Search and category: the coupon text BJ's shows on the card ("$4.00 off") |

- **Report the site and date:** "$9.99 at bjs.com on 2026-11-26, regular price $12.99, offer to 2026-12-25". A club price always names its club: "$599.99 at the Jersey City, NJ club (0044)".
- **Member-only:** say "BJ's shows this price to signed-in members; the list price shown to visitors is $399.99". Never call it the member price.
- **Coupons:** quote the coupon text and the coupon book's terms (`value`, `offer_type`, `redemption_limit`, `expires_at`). Never compute a price after a coupon: coupons are clipped to a membership on bjs.com, and Scavio does not check whether one applies to an order.
- Report BJ's labels and the arithmetic only. Never judge a regular price or a sale, and never describe how often an item is discounted.

## Workflow

1. **Find the item.** `/search` with `query` (at least 2 characters), or `/category` with a `category` id from `/categories` (`tvs-and-electronics>tvs`). Each result's `product_id` (19 digits starting with 3) is the input of product and reviews.
2. **Read it in full.** `/product` with `product_id` or the product `url`: UPC, model, regular price, savings, offer dates, variants and the clubs eligible for same-day delivery, pickup, ship from club and EBT.
3. **Check the flags.** `member_only_price` true: report the list price as the list price. `club_only` true: report "sold in clubs", no price.
4. **Coupons.** `/coupons` lists the book; match a coupon to an item by `upcs` or `gtins` against the product's `upc`.
5. **Reviews.** `/reviews` with `product_id` and `page` (10 per page, up to page 500). Page 1 carries `summary`, `ai_summary` and the questions.
6. **Clubs.** `/clubs` with an optional `state` (`NY`) lists club ids and names. A club id cannot be sent to any other endpoint: BJ's assigns the club for each visit.
7. **Watching prices:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Product (`/product`) and reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | A BJ's product id: the 19-digit number at the end of a bjs.com/product/ link (`3000000000005430255`, search `results[].product_id`) |
| `url` | string | one of | Or the bjs.com product link. With both, they must name the same product |
| `page` | integer | 1 | Reviews only: page, 1-based, 10 a page (1 to 500) |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords, 2-100 characters (`coffee`, `paper towels`, `tv`) |

### Category (`/category`) and categories (`/categories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category` | string | category: required; categories: none | A BJ's category id from categories (`tvs-and-electronics>tvs`), or its bjs.com/category/ path or link. On categories: optional, the answer is that category's subtree |

### Coupons (`/coupons`) and clubs (`/clubs`)

`/coupons` takes no parameters (send `{}`). `/clubs` takes an optional `state`, a US state code (`NY`, `NJ`, `MA`, `FL`); without it, every club.

## Examples

### One product with its regular price, savings and offer dates

```bash
curl -X POST https://api.scavio.dev/api/v1/bjs/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "3000000000005430255"}'
```

Captured `data` (2026-11-26; `description`, `summary` and `breadcrumbs` dropped, `specifications` cut to 3 of 15, `fulfillment` club id lists cut to 3, `note` shortened):

```json
{
  "product_id": "3000000000005430255",
  "item_number": "336678",
  "name": "Scotch-Brite 420-Sheet Lint Rollers, 4 pk.",
  "brand": "Scotch-Brite",
  "model": "836RS-105-4PKC",
  "upc": "68060497901",
  "url": "https://www.bjs.com/product/item/3000000000005430255/",
  "currency": "USD",
  "price": 9.99,
  "regular_price": 12.99,
  "savings": 3,
  "offer": { "starts_at": "2026-11-12T05:00:00.000000000Z", "ends_at": "2026-12-25T04:59:59.000000000Z" },
  "map_price": 9.99,
  "unit_price": null,
  "unit_of_measure": null,
  "price_range": null,
  "member_only_price": false,
  "club_only": false,
  "weighted_item": false,
  "available_online": true,
  "available_in_club": true,
  "in_stock_online": true,
  "estimated_delivery": "3-5 Business Days",
  "free_shipping": false,
  "rating": 4.5,
  "review_count": 103,
  "specifications": {
    "Product Type": "Lint Rollers",
    "Includes": "Scotch-Brite Lint Rollers Value Pack, 4 Rolls/420 Total Sheets",
    "Item Weight": "1.39 lbs."
  },
  "images": ["https://bjs.scene7.com/is/image/bjs/336678?$bjs-Initial350$"],
  "options": [],
  "variant_count": 1,
  "variants": [],
  "fulfillment": [
    {
      "item_number": "336678",
      "item_type": "CLUB_ONLINE",
      "ebt_eligible": false,
      "same_day_delivery": { "eligible_club_ids": ["0001", "0007", "0008"], "ineligible_count": 0 },
      "pickup_in_club": { "eligible_club_ids": ["0001", "0007", "0008"], "ineligible_count": 0 },
      "ship_from_club": { "eligible_club_ids": ["0020", "0027", "0029"], "ineligible_count": 0 },
      "fresh_delivery": null,
      "ebt_clubs": { "eligible_club_ids": [], "ineligible_count": 272 }
    }
  ],
  "note": "price is BJ's online price (offer price when an instant saving runs: regular_price, savings and offer {starts_at, ends_at} as given). Club prices differ from club to club and are not returned. ..."
}
```

$12.99 - $3 = $9.99, as BJ's gives it, until 2026-12-25 04:59 UTC. 272 clubs were eligible for same-day delivery and pickup, 47 for ship from club, none for EBT. A member-only item reads differently: `{"product_id": "3000000000004435757"}` (Hamilton Beach Durathon Iron, item `308397`) answered `price` $29.99, `regular_price` null, `member_only_price` true and the note "member_only_price true: BJ's shows this item's price to signed-in members; the answer carries the list price and no member price, sale price or sale dates." An unknown product id is a charged `404` "BJ's has no product with this id."

### A category priced for the club BJ's assigned

```bash
curl -X POST https://api.scavio.dev/api/v1/bjs/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category": "tvs-and-electronics>tvs"}'
```

Captured `data` (2026-11-26; 2 of 40 results shown with 16 of their fields, `facets` dropped, `note` shortened):

```json
{
  "category_id": "tvs-and-electronics>tvs",
  "url": "https://www.bjs.com/category/tvs-and-electronics/tvs/",
  "subcategories": [],
  "total": 162,
  "count": 40,
  "page_size": 40,
  "has_more": true,
  "priced_for": { "club_id": "0044", "name": "Jersey City", "city": "Jersey City", "state": "NJ" },
  "results": [
    {
      "product_id": "3000000000006369757",
      "name": "Samsung 75\" U7900HD Crystal UHD 4K Vision AI Smart TV with 4-Year Coverage",
      "currency": "USD",
      "price": 599.99,
      "was_price": null,
      "sale": { "price": 397.99, "starts_at": "2026-11-16 00:00:00", "ends_at": "2026-11-30 23:59:59" },
      "club_price": 599.99,
      "club_was_price": null,
      "club_sale": { "price": 397.99, "starts_at": "2026-11-16 00:00:00", "ends_at": "2026-11-30 23:59:59" },
      "member_only_price": false,
      "club_only": false,
      "in_stock_club": true,
      "fulfillment_club": { "same_day_delivery": true, "pickup_in_club": true, "ebt": false },
      "rating": 5,
      "review_count": 27,
      "badges": { "promotional_badge": "FREE Delivery Today", "promotional_event": "BF 2026", "spec_badge": null, "plp_badge": null }
    },
    {
      "product_id": "3000000000006253813",
      "name": "Samsung 65\" U8000HD Crystal UHD 4K Smart TV with 4-Year Coverage",
      "currency": "USD",
      "price": 399.99,
      "was_price": null,
      "sale": null,
      "club_price": null,
      "club_was_price": null,
      "club_sale": null,
      "member_only_price": true,
      "club_only": false,
      "in_stock_club": true,
      "fulfillment_club": { "same_day_delivery": true, "pickup_in_club": true, "ebt": false },
      "rating": 4.5,
      "review_count": 770,
      "badges": { "promotional_badge": null, "promotional_event": "BF 2026", "spec_badge": null, "plp_badge": null }
    }
  ],
  "note": "The page lists 40 results (BJ's shows 40 a page and its page parameter is ignored, so there is no deeper paging); total is BJ's own count. price is the online price. club_price, club_sale and fulfillment_club are the club BJ's assigned to the visit (priced_for); the club cannot be chosen, and priced_for is null when BJ's assigned none (then the prices are online prices). Items with member_only_price true show their price to signed-in members: ..."
}
```

26 of the 40 TVs carried a club price for Jersey City; 14 were member-only. The `promotional_badge` text is BJ's own (it carried a decorative character on the page, left out here). A category whose page opens a landing page with no product list is a charged `404` that points to its subcategories: list them with `/categories` and that `category`.

### Reviews with BJ's AI summary and Q&A

```bash
curl -X POST https://api.scavio.dev/api/v1/bjs/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "3000000000004479773", "page": 3}'
```

Captured `data` (2026-11-26; 1 of 10 reviews and 1 of 2 questions shown, `themes` and `highlights` cut, `ai_summary.text` shortened):

```json
{
  "product_id": "3000000000004479773",
  "item_number": "309389",
  "page": 3,
  "page_size": 10,
  "total": 2967,
  "total_pages": 297,
  "has_more": true,
  "count": 10,
  "summary": {
    "average_rating": 4.81,
    "review_count": 2967,
    "rating_histogram": { "1": 28, "2": 21, "3": 48, "4": 296, "5": 2574 },
    "recommended_ratio": 0.97,
    "themes": { "aitheme": [{ "label": "thin paper", "count": 1652 }] }
  },
  "ai_summary": {
    "text": "Overall sentiment is mostly positive, with many reviewers calling these paper towels strong and highly absorbent while offering solid value versus Bounty. ...",
    "generated_at": "2026-11-14T11:57:44.495650Z",
    "highlights": [{ "label": "Thin paper", "type": "con", "count": 1652 }]
  },
  "reviews": [
    {
      "review_id": "590443855",
      "rating": 5,
      "title": "Great picker upper",
      "text": "I was skeptical about buying a store name brand but Bounty is getting expensive.  The price was way less and does the same job.",
      "created_at": "2026-11-17T03:25:28.791Z",
      "would_recommend": true,
      "item_number": "309389",
      "verified_buyer": true,
      "staff_reviewer": false,
      "helpful_votes": 0,
      "not_helpful_votes": 0,
      "photos": []
    }
  ],
  "questions_total": 2,
  "questions": [
    {
      "question_id": "11326793",
      "text": "Are these individually wrapped?",
      "created_at": "2026-03-16T14:09:50.032Z",
      "answer_count": 1,
      "answers": [
        { "answer_id": "576238391", "text": "Yes, these are individually wrapped.", "created_at": "2026-03-17T10:03:25.904Z", "author_type": "EXPERT", "is_expert": true, "helpful_votes": 1 }
      ]
    }
  ],
  "note": "Reviews in BJ's default order (newest to oldest), 10 a page. Reviewer, asker and answerer names and locations are not returned. ai_summary is BJ's own AI review summary, as the site shows it. questions: page 1 of the product's Q&A."
}
```

`ai_summary` is BJ's own AI-generated summary: quote it as BJ's, never as Scavio's finding. `total_pages` (297 here) says how far to page; the API serves pages 1 to 500.

### Search, categories, coupons and clubs

- `/search` `{"query": "coffee"}`: `total` 125, `count` 40, `has_more` true, `priced_for` null (online prices only). 12 `departments` (Grocery 77, Seasonal 48, ...), 8 `related_searches` and 17 facets (Delivery Options, Special Offers with Coupons 32 and Instant Rebates 9, brand, packaging, rating, EBT eligible, flavor, ...). Folgers Classic Roast 43.5 oz. $24.79 ("$4.00 off", 8,158 reviews), Maxwell House 43.1 oz. $21.78 ("$2.50 off"), Starbucks Pike Place $21.49 ("$4.00 off"), Wellsley Farms Colombian $19.49 ("$5.00 off"). An empty search is a charged `404` "BJ's has no search page for this query."
- `/categories` `{}`: `product_count` 13,503, `count` 982, top level such as Seasonal 4,528, Grocery 4,207, Deals 1,807 (`hidden` true: kept out of BJ's menus, it still browses), Home & Kitchen 1,273, TVs & Electronics 1,077. Each `category_id` is the input of category.
- `/coupons` `{}`: `total` 567, `count` 268 (as the page loaded them), 12 categories. Such as offer `2253377` "(1) Coca-Cola, Sprite OR Variety Pack Mini Cans, 30 pk./7.5 oz." "$2.00 off", `offer_type` AmountOff, `redemption_limit` 5, `source` MFG, expires 2026-11-30; 237 were manufacturer (MFG) offers, 24 BJ's (BJSSCPN) and 7 OMS.
- `/clubs` `{"state": "NY"}`: 50 clubs in New York of 283 in 22 states, such as `0007` Albany, `0302` Allegany, `0213` Amherst, each with its bjs.com page. A state with no club answers an empty list and says so.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def bjs(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/bjs/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Search: the first 40 results with BJ's total (1 credit)
hits = bjs("search", {"query": "coffee"})["data"]
print("total", hits["total"], "priced for", hits["priced_for"])
for i in hits["results"][:5]:
    if i["club_only"]:
        print(i["product_id"], i["name"], "sold in clubs only")
    elif i["member_only_price"]:
        print(i["product_id"], i["name"], "list price", i["price"], "(member price shown to members only)")
    else:
        print(i["product_id"], i["name"], i["price"], i["sale"], i["coupon"])

# 2. One product with its regular price, savings and offer dates (1 credit)
p = bjs("product", {"product_id": "3000000000005430255"})["data"]
print(p["name"], p["upc"], p["price"], p["regular_price"], p["savings"], p["offer"])

# 3. Coupons that name this item's UPC (1 credit)
book = bjs("coupons", {})["data"]
for c in book["coupons"]:
    if p["upc"] and p["upc"] in c["upcs"]:
        print(c["offer_id"], c["summary"], c["expires_at"])

# Prices change between calls. Store each answer with fetched_at and run this
# on a schedule: that stored series is your history (BJ's shows only the current price).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries a `note` (prices in USD).

- **listing** (search, category) - `total`, `count`, `page_size` (40), `has_more`, `priced_for` {`club_id`, `name`, `city`, `state`} or null, `results[]` {`product_id`, `item_number`, `name`, `url`, `image_url`, `currency`, `price`, `was_price`, `sale` {`price`, `starts_at`, `ends_at`}, `club_price`, `club_was_price`, `club_sale`, `member_only_price`, `club_only`, `available_online`, `available_in_club`, `out_of_stock`, `in_stock_online`, `in_stock_club`, `fulfillment_online` and `fulfillment_club` {`same_day_delivery`, `pickup_in_club`, `ebt`}, `ebt_eligible`, `weighted_item`, `rating`, `review_count`, `coupon`, `free_shipping`, `badges` {`promotional_badge`, `promotional_event`, `spec_badge`, `plp_badge`}, `max_quantity`, `bought_last_month`, `first_available`, `categories`}, `facets[]` {`name`, `label`, `options[]` {`value`, `label`, `count`}}. Search adds `query`, `departments[]` {`category_id`, `name`, `count`, `url`}, `related_searches`; category adds `category_id`, `url`, `subcategories[]` {`category_id`, `name`, `count`, `url`}.
- **product** - `product_id`, `item_number`, `name`, `brand`, `model`, `upc`, `url`, `currency`, `price`, `regular_price`, `savings`, `offer` {`starts_at`, `ends_at`}, `map_price`, `unit_price`, `unit_of_measure`, `price_range`, `member_only_price`, `club_only`, `weighted_item`, `available_online`, `available_in_club`, `in_stock_online`, `estimated_delivery`, `free_shipping`, `rating`, `review_count`, `description`, `summary`, `specifications`, `breadcrumbs[]` {`name`, `url`}, `images`, `options`, `variant_count`, `variants[]` {`item_id`, `item_number`, `attributes`, `price`, `regular_price`, `savings`, `offer`, `map_price`, `unit_price`, `unit_of_measure`, `available_online`, `available_in_club`, `in_stock_online`, `gtin`}, `fulfillment[]` {`item_number`, `item_type` (`CLUB_ONLINE` or `CLUB_ONLY`), `ebt_eligible`, `same_day_delivery`, `pickup_in_club`, `ship_from_club`, `fresh_delivery`, `ebt_clubs`: {`eligible_club_ids`, `ineligible_count`}}.
- **categories** - `root`, `product_count`, `count`, `categories[]` {`category_id`, `name`, `count`, `url`, `level`, `hidden`, `children`}.
- **reviews** - `product_id`, `item_number`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `summary` {`average_rating`, `review_count`, `rating_histogram`, `recommended_ratio`, `themes`} (page 1), `ai_summary` {`text`, `generated_at`, `highlights[]` {`label`, `type` (`pro` or `con`), `count`}}, `reviews[]` {`review_id`, `rating`, `title`, `text`, `created_at`, `would_recommend`, `item_number`, `verified_buyer`, `staff_reviewer`, `helpful_votes`, `not_helpful_votes`, `photos`}, `questions_total`, `questions[]` {`question_id`, `text`, `created_at`, `answer_count`, `answers[]` {`answer_id`, `text`, `created_at`, `author_type`, `is_expert`, `helpful_votes`}}.
- **coupons** - `total`, `count`, `has_more`, `categories`, `coupons[]` {`offer_id`, `description`, `brand`, `manufacturer`, `summary`, `value`, `category`, `offer_type`, `min_quantity`, `redemption_limit`, `redemption_frequency`, `source` (`MFG` or `BJSSCPN`), `active_from`, `expires_at`, `upcs`, `gtins`, `image_url`, `disclaimer`}.
- **clubs** - `state`, `state_count`, `count`, `states[]` {`state`, `state_name`, `count`}, `clubs[]` {`club_id`, `name`, `state`, `url`}.

## Guardrails

- Name it "BJ's Wholesale Club (bjs.com, the US warehouse club)" on first mention. BJ's memberships and accounts are not read.
- Prices: quote `price` with BJ's own labels (regular price, savings, offer dates, sale dates), the site and the `fetched_at` date. A club price always names the club in `priced_for`; never present it as the price at another club or at the user's club.
- Member-only: report `member_only_price` true as "BJ's shows this price to signed-in members" with the list price labelled as the list price. Never state, estimate or imply a member price.
- Club-only: report `club_only` true as "sold in clubs, no online price". Never fill in a price.
- Clubs: there is no club choice, no price or stock at a chosen club and no ZIP club finder. Say so plainly when asked, and offer the club directory (ids and names by state) instead.
- Coupons: quote the coupon text, value, limit and expiry as given. Never compute a price after a coupon and never promise one applies.
- Reviews: no reviewer, asker or answerer names are returned. Quote `ai_summary` as BJ's own AI-generated summary.
- Not available: results past the first 40, member prices, club prices on the product page, stock or prices at a club you pick, a club locator by ZIP, club hours, BJ's Gas prices, a weekly ad, price history (poll and store), cart, checkout or ordering. This API cannot clip coupons, reserve or buy.
- Terms: Scavio does not collect or store BJ's data: each call fetches the public BJ's page at the moment the request asks for it and returns what it shows as JSON, with no response cache. BJ's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish BJ's product photos or logos; link products by `url` instead.
- Never fabricate prices, savings, coupon values, dates, product ids, club ids or ratings. Only return what the API returned, with the `fetched_at` time and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id (or url) is required."; "product_id must be a BJ's product id: the 19-digit number at the end of a bjs.com/product/ link (search results[].product_id), e.g. 3000000000005430255."; "url must be a bjs.com product link such as https://www.bjs.com/product/scotch-brite-420-sheet-lint-rollers-4-pk/3000000000005430255/."; "product_id does not match the link's product id."; "query must be at least 2 characters (a word such as coffee, paper towels or tv)."; "category must be a BJ's category id from categories (e.g. tvs-and-electronics>tvs) or a bjs.com/category/ path or link."; "category all is the whole catalogue: pick a department from categories (e.g. grocery)."; "state must be a US state code (NY, NJ, MA, FL ...)."; a `page` outside 1-500.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "BJ's has no product with this id.", "BJ's has no search page for this query.", "BJ's has no category at this path: pick one from categories.", "BJ's has no category with this id: send one from categories (e.g. tvs-and-electronics>tvs).", or a category that opens a landing page with no product list ("send one of its subcategories"). Take product ids and category ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=bjs-wholesale-club-api).
- `502` means BJ's data was temporarily unavailable ("BJ's Wholesale Club is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means BJ's is busy ("BJ's Wholesale Club is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.99.0
npm install scavio@0.100.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.bjs.search({ query: "coffee" });
const { data: product } = await scavio.bjs.product({ product_id: "3000000000005430255" });
const { data: tvs } = await scavio.bjs.category({ category: "tvs-and-electronics>tvs" });
const { data: tree } = await scavio.bjs.categories({});
const { data: reviews } = await scavio.bjs.reviews({ product_id: "3000000000004479773", page: 1 });
const { data: coupons } = await scavio.bjs.coupons({});
const { data: clubs } = await scavio.bjs.clubs({ state: "NY" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.bjs.search(...)`, `product`, `category`, `categories`, `reviews`, `coupons` and `clubs`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 7 endpoints as tools: `search_bjs`, `get_bjs_product`, `get_bjs_category`, `get_bjs_categories`, `get_bjs_reviews`, `get_bjs_coupons` and `get_bjs_clubs`. BJ's is opt-in: add `bjs` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.99.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,bjs"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/bjs-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=bjs-wholesale-club-api), [product](https://scavio.dev/docs/bjs-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=bjs-wholesale-club-api), [category](https://scavio.dev/docs/bjs-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=bjs-wholesale-club-api), [categories](https://scavio.dev/docs/bjs-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=bjs-wholesale-club-api), [reviews](https://scavio.dev/docs/bjs-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=bjs-wholesale-club-api), [coupons](https://scavio.dev/docs/bjs-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=bjs-wholesale-club-api), [clubs](https://scavio.dev/docs/bjs-clubs?utm_source=agent-skills&utm_medium=skill&utm_campaign=bjs-wholesale-club-api). Overview: [BJ's Wholesale Club API](https://scavio.dev/bjs-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=bjs-wholesale-club-api).
