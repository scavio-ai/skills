# B-Stock API - Liquidation Lots, Current Bids, Retail Value, Manifest Previews

Read B-Stock (bstock.com, the liquidation marketplace where retailers and brands sell customer returns and overstock by the pallet or truckload): the open lots by keyword and filter, one lot with its auction state and public manifest preview, the storefronts with open listings, and the search filters with their counts. As shown to a visitor who is not signed in.

**The job this skill is for: what an open B-Stock lot holds and where its bidding stands right now.** Every lot carries the current bid, the bid count, the seller's stated retail value, the units and pallets, the condition and inventory type and where it ships from; one lot adds the next minimum bid, the end time (and whether a late bid extended it) and the first manifest rows. On 2026-11-28 a lot of 2 pallets of insulated work boots (218 units, stated retail 61,522 USD) stood at 1,508 USD after 21 bids, next minimum bid 1,533 USD.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Open listings only.** Search lists live auctions and offers. Closed and sold lots and their final prices are not available.
- **Manifest preview, not the full manifest.** `/lot` returns the manifest rows B-Stock shows publicly (up to 10) and `items_total`; the full manifest needs a signed-in buyer account.
- **Amounts in the listing's currency.** USD for most lots; EUR or GBP for Amazon Europe lots. B-Stock shows fee-inclusive prices and shipping costs to signed-in buyers only.
- **Bids move live.** `current_bid`, `bids` and `end_time` are as of the fetch; a late bid can extend the close. Scavio keeps nothing: poll and store your own series.
- **No bidder data.** Bid and bidder counts only; no bidder identities, ever.

B-Stock offers no public, self-serve API for its listings. The lots are shown on bstock.com, and this skill reads those public pages with one Scavio key.

See also: Liquidation.com `liquidation-com-api` and Nellis Auction `nellis-auction-api` (liquidation auctions), eBay `ebay-product-data` and Amazon `amazon-product-data` (resale prices of the same items).

## When to trigger

Use this skill when the user asks to:
- Find open B-Stock lots by keyword ("laptop", "boots", "small appliances"), storefront (a retailer or brand marketplace), category, condition, inventory type or where they ship from
- Watch a lot: current bid, next minimum bid, bid count, end time and whether it was extended
- Read what a lot holds: units, pallets, condition breakdown, categories, manufacturers, models and the public manifest preview
- List the storefronts with open listings, or the filter values with B-Stock's counts

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=b-stock-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=b-stock-api) - email or Google, no card required.
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
| `POST /api/v1/bstock/search` | Open lots by keyword and filters: 20 per call by default (up to 200), paged with `offset`, with current bid, bids, retail value, units, pallets, condition, end time and location | 1 |
| `POST /api/v1/bstock/lot` | One lot by listing id or link: auction state, next minimum bid, retail value, units, shipping, description and the public manifest preview | 1 |
| `POST /api/v1/bstock/storefronts` | The retailer and brand storefronts with open listings, each with its open listing count | 1 |
| `POST /api/v1/bstock/filters` | The search filters with B-Stock's counts of open listings: categories, subcategories, conditions, inventory types, regions, manufacturers and more | 1 |

## Workflow

1. **Know the filters.** `/storefronts` lists the storefronts (send `id`, `value` or `name` as `storefront`); `/filters` lists every filter value with its count (send each as the search field of the same name).
2. **Find lots.** `/search` with `q` and any filters. Each filter takes one value or a list of up to 10 (any of them). `sort`: `recommended` (the default without `q`), `end_time` (soonest closing first) or `relevance` (needs `q`; the default with `q`).
3. **Next pages.** Send `offset` = previous `offset` + `limit` while `has_more` is true.
4. **One lot.** `/lot` with `id` (`listings[].listing_id`) or `url` (`listings[].url`).
5. **Watching a lot:** there is no history. Poll the same listing id on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`)

| Parameter | Description |
|---|---|
| `q` | Keywords, up to 200 characters. Omitted: every open lot (filters and sort still apply) |
| `storefront` | A storefront: `storefronts[].id`, `value` or `name` from `/storefronts` |
| `category`, `subcategory` | `categories[].value` / `subcategories[].value` from `/filters` (e.g. Electronics, Laptops) |
| `condition` | New, Like New, Used Good, Used Fair, Mixed, Salvage ... |
| `inventory_type` | Customer Returns, Overstock, Shelf Pulls, Mixed/Other ... |
| `buying_format` | `AUCTION`, `BUY_NOW` or `MAKE_AN_OFFER` |
| `region` | Where the lot ships from: `GA/US` a US state, `ON/CA` a Canadian province, `/ES` a European country |
| `shipment_type` | `LTL`, `PARCEL` or `Truckload` |
| `manufacturer` | As B-Stock lists it (`/filters` gives the top 500) |
| `sort` | `recommended`, `end_time` or `relevance` |
| `limit`, `offset` | 1-200 (default 20); 0-10000 |

### Lot (`/lot`)

Send `id` (a listing id of 24 hex characters, or the number of an Amazon Europe lot) or `url` (a bstock.com listing link from `listings[].url`).

## Examples

### One search listing

Request `{"q": "laptop"}` (1 credit): `total` 20, `sort` relevance. One listing, abridged:

```json
{
  "position": 1,
  "listing_id": "6b059dff8ca35710ee08650b",
  "title": "Apple 16\" MacBook Pro Laptop A2141 i7-9750H, 8 Units, Grade B/C, Norcross GA",
  "lot_source": "marketplace",
  "storefront": { "id": "68f27c38cd13c8fc681ae642", "name": "B-Stock ITAD" },
  "currency": "USD",
  "current_bid": 1680,
  "bids": 0,
  "unique_bidders": 0,
  "retail_value": null,
  "buy_now": { "available": false, "ends_at": null },
  "pricing_strategy": "AUCTION",
  "end_time": "2026-12-01T17:15:00.000Z",
  "condition": "Mixed",
  "categories": ["Electronics"],
  "units": 8,
  "pallets": 0,
  "shipment_type": "PARCEL",
  "has_manifest": true,
  "location": { "city": "Norcross", "state": "GA", "country": "US", "region": "Norcross, GA, United States" }
}
```

`current_bid` is the opening price while `bids` is 0, as the listing page shows it.

### One lot

Request `{"id": "6b05cd6821e9e20881d2a998"}` (1 credit), abridged:

```json
{
  "listing_id": "6b05cd6821e9e20881d2a998",
  "title": "2 Pallets of Monarch Insulated Boots, Crossbeam 10\" Boots Insulated Composite Toe & More",
  "status": "SCHEDULED",
  "currency": "USD",
  "auction": { "state": "open", "start_price": 100, "current_bid": 1508, "next_minimum_bid": 1533, "bids": 21, "unique_bidders": 10, "end_time": "2026-12-01T19:00:00.000Z", "extended": false },
  "views": 376,
  "deal": "Great Price",
  "retail_value": 61522,
  "units": 218,
  "pallets": 2,
  "condition": "New",
  "manifest": { "items_total": 11, "preview_count": 10, "full_manifest": "sign_in_required" }
}
```

`manifest.preview` holds the public rows, each with `description`, `quantity`, `unit_retail`, `ext_retail`, `condition`, `brand` and `model`.

### Storefronts and filters

- `/storefronts`: `count` 37, `total_open_listings` 735, e.g. `{"name": "Amazon", "open_listings": 24, "lot_source": "marketplace"}` and `{"id": "a2z", "name": "Amazon Europe", "open_listings": 38, "lot_source": "amazon_europe"}`.
- `/filters`: 18 categories (e.g. Apparel Shoes & Accessories 132), 111 subcategories, 8 conditions, 6 inventory types, 35 regions and the top 500 manufacturers.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def bstock(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/bstock/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Open lots for a keyword, soonest closing first (1 credit)
hits = bstock("search", {"q": "laptop", "sort": "end_time"})["data"]
for it in hits["listings"][:5]:
    print(it["listing_id"], it["title"], it["current_bid"], it["bids"], it["units"], it["end_time"])

# 2. One lot with its manifest preview (1 credit)
lot = bstock("lot", {"id": "6b05cd6821e9e20881d2a998"})["data"]
print(lot["auction"]["current_bid"], lot["auction"]["next_minimum_bid"], lot["retail_value"], lot["manifest"]["items_total"])

# Bids change by the minute. Store each answer with fetched_at and poll on a
# schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it.

- **search** - `query`, `sort`, `limit`, `offset`, `total`, `count`, `has_more`, `filters_applied`, `listings[]` {`position`, `listing_id`, `title`, `url`, `lot_source`, `storefront` {`id`, `name`}, `currency`, `current_bid`, `bids`, `unique_bidders`, `retail_value`, `buy_now` {`available`, `ends_at`}, `pricing_strategy`, `listing_type`, `start_time`, `end_time`, `condition`, `inventory_type`, `categories`, `lot_categories[]`, `units`, `pallets`, `manufacturers`, `models`, `shipment_type`, `transport_mode`, `allowed_shipment_types`, `has_manifest`, `deal`, `location` {`city`, `state`, `country`, `region`}, `image`}, `notes`.
- **lot** - `requested_id`, `listing_id`, `listing_number`, `title`, `url`, `lot_source`, `status`, `storefront` {`id`, `name`, `slug`}, `currency`, `pricing_strategy`, `listing_type`, `purchasing_starts`, `purchasing_ends`, `auction` {`state`, `start_price`, `current_bid`, `next_minimum_bid`, `bids`, `unique_bidders`, `start_time`, `end_time`, `initial_end_time`, `extended`, `closed`, `canceled`, `buying_format_sequence`, `buy_now`}, `views`, `deal`, `retail_value`, `units`, `pallets`, `condition`, `conditions`, `inventory_types`, `packaging`, `categories`, `manufacturers`, `models`, `description`, `location`, `shipping` {`transport_mode`, `allowed_shipment_types`, `truck_count`, `hazmat`, `note`}, `images`, `seller_terms_url`, `manifest` {`items_total`, `preview_count`, `full_manifest`, `preview[]`}, `notes`.
- **storefronts** - `count`, `total_open_listings`, `storefronts[]` {`id`, `name`, `value`, `open_listings`, `lot_source`}, `notes`.
- **filters** - `total_open_listings`, `categories`, `subcategories`, `conditions`, `inventory_types`, `buying_formats`, `shipment_types`, `regions[]` {`value`, `path`, `count`}, `manufacturers`, `listing_types`, `deals` ({`value`, `count`} each), `storefront_count`, `notes`.

## Guardrails

- Name it "B-Stock (bstock.com, the liquidation marketplace where retailers sell returns and overstock)" on first mention. Storefront names are the sellers' marketplaces on B-Stock; never imply that Scavio or the user has any relationship with a storefront retailer.
- Bids: quote `current_bid` with its currency, `bids` and the `fetched_at` time, and say bids move live. Quote `retail_value` as "the seller's stated retail value", never as a market price or an expected resale price.
- Manifests: say the preview is the first rows B-Stock shows publicly and give `items_total`; never present the preview as the whole manifest.
- No bidder identities are returned; never try to identify bidders or sellers' staff.
- Use: keep any use descriptive - looking up open lots, their bids, contents and shipping for sourcing decisions.
- Links and content: refer to lots by listing id and title; do not republish B-Stock's photos, descriptions or manifests.
- Not available: closed or sold lots, final prices, full manifests, fee-inclusive prices, shipping quotes, bidding, buying or accounts. This API cannot bid or buy.
- Terms: Scavio does not store B-Stock data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. B-Stock's terms restrict automated access to its site and how its content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate bids, lots, retail values or manifest rows. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "id or url is required"; "storefront must be a storefront id, value or name from the storefronts endpoint."; "q must contain letters or digits."; a filter list above 10 values; `sort` relevance without `q`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: an unknown listing id, a make-an-offer listing (its details show to signed-in buyers only; its search listing carries the summary), or a storefront name with no open listings. A search with no lots is a `200` with `total` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=b-stock-api).
- `502` and `503` mean B-Stock data was temporarily unavailable. They are not charged, so retry after a few seconds.
- Search, storefronts and filters usually take 1-10 seconds; a lot 3-45. Allow a client timeout of at least 180 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.108.0
npm install scavio@0.109.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.bstock.search({ q: "laptop", storefront: "Target" });
const { data: lot } = await scavio.bstock.lot({ id: "6b05cd6821e9e20881d2a998" });
const { data: storefronts } = await scavio.bstock.storefronts();
const { data: filters } = await scavio.bstock.filters();
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.bstock.search(...)`, `lot`, `storefronts` and `filters`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 4 endpoints as tools: `search_bstock`, `get_bstock_lot`, `get_bstock_storefronts` and `get_bstock_filters`. B-Stock is opt-in: add `bstock` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.108.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,bstock"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/bstock-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=b-stock-api), [lot](https://scavio.dev/docs/bstock-lot?utm_source=agent-skills&utm_medium=skill&utm_campaign=b-stock-api), [storefronts](https://scavio.dev/docs/bstock-storefronts?utm_source=agent-skills&utm_medium=skill&utm_campaign=b-stock-api), [filters](https://scavio.dev/docs/bstock-filters?utm_source=agent-skills&utm_medium=skill&utm_campaign=b-stock-api). Platform page: [scavio.dev/bstock-api](https://scavio.dev/bstock-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=b-stock-api).
