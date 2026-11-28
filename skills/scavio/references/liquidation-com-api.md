# Liquidation.com API - Auction Lots, Bids, Manifests, Closed Results

Read Liquidation.com (liquidation.com, the US online liquidation auction site of Liquidity Services): the open auctions by keyword and filter, one open auction with its bids, buyer's premium, shipping and seller statistics, its item manifest, and a seller's closed auctions with their final bids. As shown to a visitor who is not signed in.

**The job this skill is for: what an open Liquidation.com lot holds and what similar lots closed at.** Every result carries the current bid, bids, watchers, the close time, condition, packages, items and the seller's stated retail value; the manifest lists the items as the seller wrote them; closed results give the final bid of a seller's past lots. On 2026-11-28 auction 21648824, a gaming PC lot of 4 returns, stood at 1,100 USD after 1 bid, minimum next bid 1,150 USD, with an 11% buyer's premium on top.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **USD or CAD.** Amounts are in each lot's currency: USD, or CAD for lots in Canadian warehouses (Brampton, ON). The buyer's premium, shipping and sales tax come on top of a bid.
- **Manifest columns are the seller's.** Each manifest keeps its headers as the seller wrote them; price columns keep the seller's label (`retail_price` is per unit on some manifests, per row on others).
- **Closed lots: by seller, no date.** The site does not apply keywords to closed lots and shows no close date, so `/closed` takes a seller (optionally a category). A closed lot's page is no longer viewable (`/lot` answers a charged `404`).
- **Bids move live.** `current_bid`, `bids` and `watchers` are as of the fetch; a sealed-bid lot shows no current bid (`sealed_bid` true). Poll and store your own series.
- **No bidder data.** Bid and bidder counts only; seller handles as the site shows them; no bidder identities, ever.

Liquidation.com offers no public, self-serve API for its auctions. The lots are shown on liquidation.com, and this skill reads those public pages with one Scavio key.

See also: B-Stock `b-stock-api` and Nellis Auction `nellis-auction-api` (liquidation auctions), eBay `ebay-product-data` and Amazon `amazon-product-data` (resale prices of the same items).

## When to trigger

Use this skill when the user asks to:
- Find open Liquidation.com auctions by keyword ("laptop", "small appliances"), category, lot size (package, pallet, truckload), condition (returns, shelf pulls, salvage ...), US region, auction type or seller
- Watch an auction: current bid, minimum next bid, bids, watchers, close time and buyer's premium
- Read a lot's manifest: description, quantity, brand, model, UPC and the seller's price columns
- See what a seller's past lots closed at (final bid, bids, stated retail)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=liquidation-com-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=liquidation-com-api) - email or Google, no card required.
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
| `POST /api/v1/liquidation/search` | Open auctions by keyword and filters (at least one): 27 a page (up to 100), with current bid, bids, watchers, close time, condition, packages, items, stated retail and the site's facet counts | 1 |
| `POST /api/v1/liquidation/lot` | One open auction by id or link: bids, minimum bid, buyer's premium, quantity, condition, shipping terms and weights, seller statistics, description | 1 |
| `POST /api/v1/liquidation/manifest` | The item manifest of one auction, columns as the seller lists them | 1 |
| `POST /api/v1/liquidation/closed` | One seller's closed auctions with final bid, bids, views and stated retail | 1 |

## Workflow

1. **Find lots.** `/search` with `q` and/or filters: `category` (id or name, e.g. `1002` Computers & Networking), `lot_size`, `condition`, `region`, `auction_type`, `seller`. `sort` `close_time`, `current_bid`, `items`, `title` (with `order` asc / desc) or `relevance` (needs `q`).
2. **Next pages.** Send `page` 2, 3, ... while `has_more` is true; `per_page` up to 100.
3. **One lot.** `/lot` with `id` (`results[].id`) or `url`; `/manifest` with the same id when `has_manifest` is true.
4. **Past results.** `/closed` with `seller` (`results[].seller` or `seller.handle`), optionally `category`.
5. **Watching a lot:** there is no history. Poll the same id on a schedule and store each answer with its `fetched_at`.

## Parameters

| Parameter | Endpoints | Description |
|---|---|---|
| `q` | search | Keywords (title and description), up to 200 characters |
| `category` | search, closed | A top category by id or name: Appliances 1700, Clothing & Accessories 1001, Computers & Networking 1002, Consumer Electronics 1004, Furniture 1600, General Merchandise 1005, Health & Beauty 1800, Holiday & Seasonal 1045, Home Improvement 1900, Housewares 1006, Jewelry & Watches 1011, Mystery Box 1017, Tools & Machinery 1003 (one or a list of up to 8) |
| `lot_size` | search | `package`, `pallet`, `truckload`, `large_item` |
| `condition` | search | `new`, `used`, `refurbished`, `returns`, `shelf_pulls`, `salvage`, `damaged`, `scratch_and_dent` |
| `region` | search | US region of the warehouse: `northeast`, `midwest`, `west`, `south` |
| `auction_type` | search | `standard`, `fixed_price`, `sealed_bid`, `mixed_format` |
| `seller` | search, closed (required) | A seller handle as the site shows it (e.g. `Newegg_Business`, `Titan Electronics`) |
| `sort`, `order` | search | `close_time`, `current_bid`, `items`, `title`, `relevance`; `asc` / `desc` |
| `page`, `per_page` | search, closed | 1-500; 1-100 (default 27) |
| `id`, `url` | lot, manifest | An auction id (digits) or a liquidation.com auction link |

## Examples

### One search result

Request `{"q": "laptop"}` (1 credit): `total` 73, 27 results. The first, abridged:

```json
{
  "position": 1,
  "id": "21648835",
  "title": "RTX 5080, Gaming PC Computer / Laptop Lot & More - MSRP $6.6K - 7 Qty",
  "seller": "Newegg_Business",
  "closing_text": "Nov 30 7:45PM",
  "closes_at": "2026-11-30T19:45:00-05:00",
  "location_state": "California",
  "condition": "Returns",
  "packages": { "count": 3, "unit": "package" },
  "items": 7,
  "currency": "USD",
  "current_bid": 3000,
  "sealed_bid": false,
  "bids": 0,
  "watchers": 1,
  "views": 52,
  "est_retail": 6600
}
```

### One lot and its manifest

Request `{"id": "21648824"}` (1 credit), abridged:

```json
{
  "id": "21648824",
  "title": "RTX 5070, Gaming PC Computer / Laptop Lot & More - MSRP $3.6K - 4 Qty",
  "status": "open",
  "closes_at": "2026-11-30T16:15:00-05:00",
  "currency": "USD",
  "current_bid": 1100,
  "minimum_bid": 1150,
  "bids": 1,
  "bidders": 1,
  "auction_type": "Standard",
  "buyers_premium_pct": 11,
  "seller": { "handle": "Newegg_Business", "marketplace_seller": true, "lifetime_completed_transactions": "100+" },
  "location": { "city": "Ontario", "state": "CA" },
  "condition": "Returns",
  "category": "Computers & Networking",
  "quantity": 4,
  "est_retail_per_unit": 900
}
```

`/manifest` `{"id": "21648824"}`: `columns` Description, Quantity, Retail Price, Ext Retail Price, Make, Model, Product Category; `row_count` 4, e.g. `{"description": "RTX 5070 - Acer Nitro 85 N85-600-UR21 Desktop, ...", "quantity": 1, "retail_price": 1499.99, "ext_retail_price": 1499.99, "brand": "Acer America", "model": "N85-600-UR21", "category": "Gaming Desktop PCs"}`.

### Closed results

`/closed` `{"seller": "Titan Electronics"}`: `total` 2,373; e.g. a lot of 43 home items on 3 pallets (stated retail 2,053.02 USD) with `final_bid` 455 after 40 bids.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def liquidation(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/liquidation/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Open pallet lots of returns, highest bid first (1 credit)
hits = liquidation("search", {"condition": "returns", "lot_size": "pallet", "sort": "current_bid"})["data"]
for it in hits["results"][:5]:
    print(it["id"], it["title"], it["current_bid"], it["bids"], it["est_retail"], it["closes_at"])

# 2. A seller's closed lots (1 credit)
closed = liquidation("closed", {"seller": "Titan Electronics"})["data"]
for it in closed["results"][:5]:
    print(it["title"], it["final_bid"], it["bids"], it["est_retail"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it.

- **search** - `query`, `filters_applied`, `sort`, `order`, `page`, `per_page`, `total`, `count`, `has_more`, `results[]` {`position`, `id`, `title`, `url`, `image`, `seller`, `closing_text`, `closes_at`, `location_state`, `condition`, `packages` {`count`, `unit`}, `items`, `currency`, `current_bid`, `sealed_bid`, `bids`, `watchers`, `views`, `est_retail`}, `facets`, `notes`.
- **lot** - `requested_id`, `id`, `title`, `url`, `status`, `closes_at`, `closes_text`, `time_left`, `currency`, `current_bid`, `minimum_bid`, `buy_now_price`, `sealed_bid`, `bids`, `bidders`, `watchers`, `views`, `auction_type`, `buyers_premium_pct`, `seller` {`handle`, `marketplace_seller`, `selling_for`, `lifetime_completed_transactions`, `past_90_days`}, `fulfilled_by`, `location` {`city`, `state`}, `condition`, `condition_definition`, `category`, `subcategories`, `quantity`, `quantity_variance_pct`, `est_retail_per_unit`, `bid_price_per_unit`, `size_class`, `packages`, `available_lots`, `shipping` {`terms`, `minimum_fee`, `weight_lbs`, `dimensional_weight_lbs`, `weight_text`, `ship_from_zip3`, `restrictions`}, `has_manifest`, `images`, `description`, `attributes`, `notes`.
- **manifest** - `id`, `lot_url`, `columns[]` {`header`, `key`}, `row_count`, `truncated`, `rows[]`, `notes`.
- **closed** - `filters_applied`, `page`, `per_page`, `total`, `count`, `has_more`, `results[]` {`position`, `id`, `title`, `url`, `image`, `seller`, `location_state`, `condition`, `packages`, `items`, `currency`, `final_bid`, `sealed_bid`, `bids`, `views`, `est_retail`}, `facets`, `notes`.

## Guardrails

- Name it "Liquidation.com (liquidation.com, the US online liquidation auction site of Liquidity Services)" on first mention.
- Bids: quote `current_bid` with its currency, `bids` and the `fetched_at` time; say the buyer's premium, shipping and tax come on top. Quote `est_retail` as "the seller's stated retail value", never as a market or resale price.
- Manifests: quote columns with the seller's own header; never relabel a seller's price column.
- Closed results: say the site shows no close date; never present a closed lot list as complete history beyond what the site lists.
- No bidder identities are returned; never try to identify bidders.
- Use: keep any use descriptive - looking up open lots, their bids, manifests and a seller's past results for sourcing decisions.
- Links and content: refer to lots by auction id and title; do not republish the site's photos, descriptions or manifests.
- Not available: bidder identities, close dates of closed lots, keywords on closed lots, search suggestions, bidding, buying, accounts, price history (poll and store). This API cannot bid or buy.
- Terms: Scavio does not store Liquidation.com data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Liquidation.com's terms restrict automated access to its site and how its content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate bids, lots, retail values or manifest rows. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "search needs q, category, seller or a filter (lot_size, condition, region, auction_type)."; "sort relevance needs q."; "order needs sort."; "closed needs seller (a seller handle: results[].seller or lot seller.handle); category narrows a seller's closed lots."; "closed takes seller, category, page and per_page only: Liquidation.com does not apply q to closed lots."; "Pass id or url, not both."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: an unknown or closed auction, or a lot without a manifest. A search with no lots is a `200` with `total` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=liquidation-com-api).
- `502` and `503` mean Liquidation.com data was temporarily unavailable ("Liquidation.com is temporarily unavailable. Please try again."). They are not charged, so retry after a few seconds.
- Search, lot and closed usually take 3-60 seconds; a manifest 1-10. Allow a client timeout of at least 180 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.108.0
npm install scavio@0.109.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.liquidation.search({ q: "laptop" });
const { data: lot } = await scavio.liquidation.lot({ id: "21648824" });
const { data: manifest } = await scavio.liquidation.manifest({ id: "21648824" });
const { data: closed } = await scavio.liquidation.closed({ seller: "Titan Electronics" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.liquidation.search(...)`, `lot`, `manifest` and `closed`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 4 endpoints as tools: `search_liquidation`, `get_liquidation_lot`, `get_liquidation_manifest` and `get_liquidation_closed`. Liquidation.com is opt-in: add `liquidation` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.108.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,liquidation"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/liquidation-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=liquidation-com-api), [lot](https://scavio.dev/docs/liquidation-lot?utm_source=agent-skills&utm_medium=skill&utm_campaign=liquidation-com-api), [manifest](https://scavio.dev/docs/liquidation-manifest?utm_source=agent-skills&utm_medium=skill&utm_campaign=liquidation-com-api), [closed](https://scavio.dev/docs/liquidation-closed?utm_source=agent-skills&utm_medium=skill&utm_campaign=liquidation-com-api). Platform page: [scavio.dev/liquidation-api](https://scavio.dev/liquidation-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=liquidation-com-api).
