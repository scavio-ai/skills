# Nellis Auction API - Lot Prices, Bids, Closing Prices

Read Nellis Auction (nellisauction.com, the liquidation auction marketplace with pickup warehouses in Las Vegas, Phoenix, Houston, Philadelphia, Denver and Dallas) in each of its 6 shopping locations: search of the open lots, one lot by id with its bid history (open, closed or sold), the 13 pickup warehouses with their hours, and the live category, brand and auction-event counts. Every answer comes as Nellis's page shows it to a visitor without an account, in USD. All 4 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Nellis Auction shows to any visitor and returns them as JSON for analysis. It uses no Nellis account, places no bid, sets no watchlist and books no pickup.

**The job this skill is for: Nellis Auction closing prices vs retail.** What a lot is bid at now and what a sold lot closed at (before the buyer's premium and tax), next to the Estimated Retail Price Nellis shows on the lot, and next to the same item's new price at Amazon or Walmart and eBay sold prices for resale context. On 2026-11-25 (UTC) an open lot, LG 65" OLED evo C6 4K Smart TV (id `141281552`, North Las Vegas warehouse), read `current_bid` 101 USD after 8 bids against a `retail_price` (Nellis's "Estimated Retail Price") of 1,595.75 USD, `buyer_premium_percent` 15, 4 stars "Used" with minor damage and Nellis's note "DAMAGED TO CORNERS OF TV", closing `2026-11-26T07:18:00.000Z`. A sold lot, MEDIEVAL Wax Seal Beads (id `141100004`, Phoenix warehouse), read `final_price` 6 USD after 5 bids against a `retail_price` of 9.99 USD; with the 15% premium that is 6.90 USD before tax (arithmetic). Pair it with `amazon-product-data` and `walmart-product-data` for the same item's new price and `ebay-product-data` for eBay sold prices, matched on title, brand and model (Nellis shows no UPC).

Nine limits shape every answer, so say them plainly:
- **1 credit per call.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Search lists open lots only.** Nellis's own search shows no closed items, so neither does `/search`. A closed or sold lot is read by id with `/item`: its `final_price` is public by id. Keep the ids of the lots you follow while they are open.
- **Final price is before the premium and tax.** `final_price` is the winning bid of a sold lot (`market_status` `sold`), `null` otherwise. Nellis adds its buyer's premium (`buyer_premium_percent` of the winning bid, "typically 15% but may vary based on the auction event" as Nellis's terms state it) and sales tax on top. Always label it "closing price (before the buyer's premium and tax)" and show the premium figure separately.
- **Estimated Retail Price is Nellis's own estimate.** `retail_price` is the "Estimated Retail Price" Nellis shows on the lot, as Nellis labels it; Nellis does not state its source. It is not an MSRP and not a price any retailer charged. Report the comparison with another retailer as two dated numbers and their difference, nothing more.
- **Bids move live.** `current_bid`, `bid_count` and `closes` are as of the fetch; a late bid extends the close (`extended` says whether it was, `initial_closes` keeps the first close time). There is no live bid stream: call again for a newer number.
- **No bidder names.** `bid_history[]` carries `time`, `amount` (USD) and `status` (`Winning` or `Outbid`) only, highest amount first as Nellis lists it (the Winning bid's time can be earlier than an Outbid one: it is the time Nellis shows).
- **One shopping location per call.** `location` (default `las-vegas`) picks the shopping location for search and categories; a lot is read by id from any location. Pickup only: a won lot is picked up at its `pickup_location` warehouse by appointment. No shipping.
- **No UPC or model number field.** Match a Nellis lot to an Amazon, Walmart or eBay listing on title, brand and model text, and keep a row only where that match is evidenced.
- **No history.** Nothing is cached or kept: store each answer with its `fetched_at` for your own series.

Nellis Auction publishes no public API, developer programme or data feed. Buyers can set a max bid, watch lots and get outbid alerts in its app, and its site search filters by category, location, quality rating, retail value and event type; this skill reads the public lot, search and location pages with one Scavio key. Other vendors offer Nellis Auction data tools; this skill reads Nellis's own public pages.

Nellis Auction describes itself as "an online auction marketplace specializing in retail returns and overstock" (Nellis release, Oct 8, 2025), and traces its roots to a family-run auction house that its CEO acquired in 2012 (same release). Its Locations & Hours page lists 13 pickup warehouses in 6 metros (November 2026), some run by other operators (Lots Of Auctions in Dallas and Denton, Legacy Bids, Wild Finds). Quote these with their source, never from the samples.

See also: for the same item's new price use `amazon-product-data` (Amazon) and `walmart-product-data` (Walmart); for what the same item sold for on eBay use `ebay-product-data` (sold listings). Same item only: the same brand and model in both titles, each price with its seller and date.

## When to trigger

Use this skill when the user asks to:
- Read a Nellis Auction lot's current bid, bid count, close time and Estimated Retail Price by id or link
- Read what a sold Nellis lot closed at (the final price before the buyer's premium and tax) and its bid history
- Search the open Nellis lots of Las Vegas, Phoenix, Houston, Philadelphia, Denver or Dallas, sorted by current bid, ending soon, estimated retail or bids
- Filter open lots by category, subcategory, brand, pickup warehouse, condition stars, estimated retail range, auction event, color or size
- List the Nellis pickup warehouses with their address, operator and opening hours per day
- Count open lots per category, subcategory, brand, auction event or pickup warehouse in one shopping location
- Put a Nellis lot's bid or closing price next to its Estimated Retail Price, the same item's price at Amazon or Walmart, or eBay sold prices
- Apply the buyer's premium Nellis states for a lot to its current bid or final price

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=nellis-auction-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=nellis-auction-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, item took 1 to 2 seconds, search and categories 3 to 4, and locations 15. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/nellis/search` | The open lots of one shopping location: 48, 120 or 240 per page with current bid, bid count, Estimated Retail Price, premium percent, close time, condition and pickup warehouse; 9 sorts; filters with Nellis's counts | 1 |
| `POST /api/v1/nellis/item` | One lot by id or link, open, closed or sold: everything in search plus category, brand, features, descriptions, operator, final price of a sold lot and the bid history (no bidder names) | 1 |
| `POST /api/v1/nellis/locations` | The 13 pickup warehouses with address, coordinates, operator, shopping location and opening hours per day | 1 |
| `POST /api/v1/nellis/categories` | Live counts of open lots per category, subcategory, brand (top 100), auction event, event type and pickup warehouse in one shopping location, or one category's breakdown | 1 |

## Shopping locations

`location` takes a slug or Nellis's id (default `las-vegas`). Every search and categories answer carries `location` {`id`, `slug`, `name`}.

| `location` | id | Name | Pickup warehouses (`pickup_location` names) |
|---|---|---|---|
| `las-vegas` | 1 | Las Vegas, NV | North Las Vegas, SW Las Vegas, Nellis Outlet, Legacy Bids, Wild Finds Henderson |
| `phoenix` | 2 | Phoenix, AZ | Mesa, Phoenix |
| `houston` | 5 | Houston, TX | Katy, SW Houston |
| `philadelphia` | 6 | Philadelphia, PA | Delran (Delran, NJ) |
| `denver` | 7 | Denver, CO | Denver |
| `dallas` | 8 | Dallas, TX | Dallas, Denton (run by Lots Of Auctions) |

Any other location is a `400`, not charged. A `pickup_location` of another shopping location is a `400` that names the location to send with it.

## Bids, final prices, retail and fees

Every lot (search and item) carries:

| Field | Meaning |
|---|---|
| `current_bid` | The current high bid in USD as Nellis's page shows it, `0` before the first bid; on a sold lot the winning bid |
| `bid_count` | Nellis's count of bids on the lot |
| `retail_price` | Nellis's own "Estimated Retail Price" for the item, as Nellis labels it (source not stated by Nellis) |
| `buyer_premium_percent` | The premium Nellis adds to the winning bid for this lot (15 on every captured lot) |
| `opens`, `closes`, `initial_closes` | ISO 8601 UTC; `closes` moves when a late bid extends the lot, `initial_closes` keeps the first close |
| `extended` | Whether the close was extended |
| `market_status`, `is_closed` | Nellis's own status (`open`, `sold`, `relisted`: closed and put up again, `closed` ...) |
| `condition` | Nellis's inspection grade: `rating` (1-5 stars), `condition`, `functional`, `damage`, `missing_parts`, `assembly`, `package`, as given |
| `inspection_notes` | Nellis's inspection note, as written (or `null`) |
| `pickup_location` | {`id`, `name`, `address`, `city`, `state`, `zip`, `timezone`}: the warehouse a won lot is picked up from |
| `final_price` | Item only: the winning bid of a sold lot, before the premium and tax; `null` otherwise |

- **Arithmetic, not judgement:** "101 USD current bid after 8 bids at 2026-11-25, Nellis's Estimated Retail Price 1,595.75 USD; with the 15% premium 116.15 USD before tax." Show the premium figure beside the bid, never instead of it, and never compute tax (the rate depends on the pickup location).
- **Fees as Nellis states them** (FAQ and terms): the buyer's premium is "typically 15% but may vary based on the auction event" (use the lot's own `buyer_premium_percent`); a cancellation fee of 5% of the sale price per cancelled item; a relisting fee of 5% of the sale price for an item not picked up within seven days; a $1 restocking fee per item on a missed pickup appointment. Quote them only in that wording.
- **Condition:** report the stars and the text exactly as returned ("4 stars, Used, damage Minor"); Nellis's terms call its ratings subjective and for convenience only, and items are sold as-is. Never infer whether an item works beyond `functional` as given.
- **Operator:** `operator` (item) names who runs the auction, Nellis Auction or a partner such as Lots Of Auctions; never call every lot a Nellis item when the operator is a partner.

## Workflow

1. **Find lots.** `/search` with `q` (or none: every open lot), `location`, and optionally `sort`, filters and `page_size`. Each `items[].id` is the input of `/item`.
2. **Read one lot.** `/item` with `id` (or `url`, an `items[].url` link): current bid, bid history, condition, operator, pickup warehouse.
3. **Follow it to the close.** Call `/item` again after `closes`: `market_status` `sold` with `final_price`, or `relisted`. Search will no longer list it.
4. **Narrow a list.** `/categories` with `location` (and optionally `category`) gives the exact names that search's `category`, `subcategory`, `brand`, `auction_event_name` and `pickup_location` take, with live counts.
5. **Compare retail.** Search the same brand and model on `amazon-product-data` or `walmart-product-data` (new price) and `ebay-product-data` (sold listings); keep a row only where the titles match on brand and model, and show each price with its source and date next to `retail_price` and the bid or final price.
6. **Plan pickup.** `/locations` (optionally with `location`): each warehouse's address and hours per day; `null` on a day means closed that day (all 13 read Thursday `null` on 2026-11-25).
7. **Closing-price series:** there is no history. Store the ids you search, read each with `/item` after it closes, and keep each answer with its `fetched_at`; that stored set is your record of closing prices.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | none | Keywords (up to 200 chars). Empty or omitted: every open lot in the location |
| `location` | string or integer | `las-vegas` | A shopping location slug or id (see Shopping locations) |
| `page` | integer | 1 | Page number; Nellis pages through 30,000 positions at most (`page_size` x `page`) |
| `page_size` | integer | 120 | `48`, `120` or `240` (Nellis's page sizes) |
| `sort` | string | `featured` | `featured` (Nellis's own order), `price_low`, `price_high` (current bid), `ending_soon`, `ending_last`, `retail_low`, `retail_high` (Estimated Retail Price), `bids_low`, `bids_high`. No newest sort |
| `category`, `subcategory` | string or list | none | `categories[].name` / `subcategories[].name` from categories (`Electronics`, `TVs`) |
| `brand` | string or list | none | As Nellis lists it (`facets.brands[].name`, `Samsung`) |
| `pickup_location` | string or list | none | A warehouse of this location (`North Las Vegas`) |
| `condition_rating` | integer or list | none | Nellis's stars, 1-5 (up to 5 values) |
| `retail_min`, `retail_max` | number | none | Estimated Retail Price range, USD |
| `auction_event_type` | string or list | none | `Retail Returns` or `Consigner / Third Party` (`facets.auction_event_types[].name`) |
| `auction_event_name` | string or list | none | One auction event (`Daily Auction - North Las Vegas - Nov 24th`) |
| `color`, `size` | string or list | none | As Nellis lists them (`facets.colors[].name`, `facets.sizes[].name`) |

A list takes up to 10 values.

### Item (`/item`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `id` | string or integer | one of | A Nellis Auction item id (`items[].id`, the number at the end of a nellisauction.com/p/ link, `141281552`) |
| `url` | string | one of | A Nellis Auction item link, `https://www.nellisauction.com/p/<title>/<id>` |

### Locations (`/locations`), categories (`/categories`)

`/locations` takes an optional `location` (only that shopping location's warehouses; without it all 13). `/categories` takes `location` (default `las-vegas`) and an optional `category` (`categories[].name`: that category's subcategories, brands and auction events).

## Examples

### One open lot with its bid history

```bash
curl -X POST https://api.scavio.dev/api/v1/nellis/item \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "141281552"}'
```

Captured `data` (2026-11-25 UTC; `bid_history` cut to 3 of 8, `features`, `descriptions`, `photos`, `dimensions`, `color`, `size` and `notes` dropped):

```json
{
  "requested_id": 141281552,
  "id": 141281552,
  "title": "LG 65\" OLED evo C6 4K Smart TV",
  "url": "https://www.nellisauction.com/p/LG-65-OLED-evo-C6-4K-Smart-TV/141281552",
  "inventory_number": "1083118164",
  "current_bid": 101,
  "currency": "USD",
  "bid_count": 8,
  "retail_price": 1595.75,
  "buyer_premium_percent": 15,
  "opens": "2026-11-25T05:00:01.086Z",
  "closes": "2026-11-26T07:18:00.000Z",
  "initial_closes": "2026-11-26T07:18:00.000Z",
  "extended": false,
  "market_status": "open",
  "is_closed": false,
  "condition": { "rating": 4, "condition": "Used", "functional": "Yes", "damage": "Minor", "missing_parts": "No", "assembly": "No", "package": "Yes" },
  "inspection_notes": "DAMAGED TO CORNERS OF TV",
  "pickup_location": { "id": 22, "name": "North Las Vegas", "address": "4031 Market Center Dr Suite 303", "city": "North Las Vegas", "state": "NV", "zip": "89030", "timezone": "America/Los_Angeles" },
  "not_returnable": false,
  "category": "Electronics",
  "subcategory": "TVs",
  "brand": "LG",
  "weight": "40.60 lbs",
  "operator": "Nellis Auction",
  "final_price": null,
  "bid_history": [
    { "time": "2026-11-25T07:01:54.563Z", "amount": 101, "status": "Winning" },
    { "time": "2026-11-25T07:22:58.394Z", "amount": 100, "status": "Outbid" },
    { "time": "2026-11-25T07:22:52.482Z", "amount": 55, "status": "Outbid" }
  ]
}
```

`retail_price` 1,595.75 is Nellis's Estimated Retail Price as labelled; the 101 USD bid was the lot's high bid at the moment of the call and could move until `closes`. `final_price` is `null` while the lot is open. An unknown id is a charged `404`.

### A sold lot's final price

```bash
curl -X POST https://api.scavio.dev/api/v1/nellis/item \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "141100004"}'
```

Captured `data` (2026-11-25 UTC; `bid_history` cut to 2 of 5, `features`, `descriptions`, `photos`, `condition` and `notes` dropped):

```json
{
  "requested_id": 141100004,
  "id": 141100004,
  "title": "MEDIEVAL Wax Seal Beads - 600+ Count, Morandi Assorted Colors",
  "current_bid": 6,
  "currency": "USD",
  "bid_count": 5,
  "retail_price": 9.99,
  "buyer_premium_percent": 15,
  "closes": "2026-11-24T02:22:00.000Z",
  "market_status": "sold",
  "is_closed": true,
  "pickup_location": { "id": 10, "name": "Phoenix", "address": "1402 S 40th Ave", "city": "Phoenix", "state": "AZ", "zip": "85009", "timezone": "America/Phoenix" },
  "operator": "Nellis Auction",
  "final_price": 6,
  "bid_history": [
    { "time": "2026-11-23T21:53:59.938Z", "amount": 6, "status": "Winning" },
    { "time": "2026-11-24T00:59:44.921Z", "amount": 5, "status": "Outbid" }
  ]
}
```

`final_price` 6 USD is the winning bid before the premium and tax; 6 x 1.15 = 6.90 USD with the 15% premium, before tax (arithmetic). Search does not list this lot any more: a sold lot is read by id only.

### Open lots in one shopping location

```bash
curl -X POST https://api.scavio.dev/api/v1/nellis/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "vacuum", "location": "phoenix", "sort": "bids_high", "page_size": 48}'
```

Captured (2026-11-25 UTC): `location` Phoenix, AZ (id 2), `total` 216, `total_pages` 5, `has_more` true, 48 on page 1. First: DREAME X60 Max Ultra Complete Robot Vacuum and Mop (id `141329704`, Mesa warehouse) at `current_bid` 51 USD after 27 bids, `retail_price` 1,596.66; second: Lefant M210 Omni Robot Vacuum and Mop at 28 USD after 11 bids, `retail_price` 404.38. `facets` gave Nellis's counts of the open matches: `pickup_locations` Mesa 115, Phoenix 101; `condition_ratings` 5 stars 183, 4 stars 24, 3 stars 7; `subcategories` Vacuums & Floor Care 118; `brands` STEAMBOT 11, Shark 7.

- `{"q": "tv", "location": "houston", "page_size": 48}`: `total` 288, first an LG 77-Inch OLED evo C6 (Katy warehouse, title carrying "MISSING REMOTE") at 456 USD after 12 bids, `retail_price` 2,346.75.
- `{"q": "robot vacuum", "page_size": 48}` (Las Vegas): `total` 10, first a MOVA V50 Ultra robot vacuum (SW Las Vegas) at 29 USD after 7 bids, `retail_price` 827.07, 2 stars, `functional` "Untested".

### Locations and categories

- `/locations` `{}`: `count` 13 warehouses in 6 `shopping_locations` (Las Vegas 5, Phoenix 2, Houston 2, Dallas 2, Philadelphia 1, Denver 1). Each warehouse: `id`, `name`, `address`, `city`, `state`, `coordinates` {`lat`, `lng`}, `operator` (Nellis Auction, Lots Of Auctions, Legacy Bids, Wild Finds), `shopping_location`, `hours` per day ({`open`, `close`} local time, or `null` when closed). SW Las Vegas read Monday 7:00 AM to 8:00 PM and Thursday `null`; Legacy Bids and Wild Finds Henderson were also closed on Sunday.
- `/categories` `{}` (Las Vegas): `total_open_items` 45,039 open lots, 17 top-level `categories` (Home & Household Essentials 14,517, Electronics 5,223, Clothing, Shoes & Accessories 5,215), 100 `subcategories`, the top 100 `brands`, 7 `auction_events` (Daily Auction - North Las Vegas - Nov 24th 17,987), 2 `auction_event_types` (Retail Returns 38,897, Consigner / Third Party 6,142) and 5 `pickup_locations`. The names are the exact inputs of search's filters.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def nellis(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/nellis/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Open lots in one shopping location (1 credit)
hits = nellis("search", {"q": "vacuum", "location": "phoenix", "sort": "bids_high", "page_size": 48})["data"]
for i in hits["items"][:5]:
    # retail_price is Nellis's own Estimated Retail Price, as labelled.
    print(i["id"], i["current_bid"], i["bid_count"], i["retail_price"], i["closes"], i["pickup_location"]["name"])
print("open lots", hits["total"])

# 2. One lot after it closes (1 credit): final_price is before premium and tax
lot = nellis("item", {"id": "141100004"})["data"]
if lot["market_status"] == "sold":
    with_premium = round(lot["final_price"] * (1 + lot["buyer_premium_percent"] / 100), 2)
    print(lot["title"], lot["final_price"], with_premium, lot["retail_price"])

# Store each answer with fetched_at: that stored set is your closing-price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Most `data` carry `notes`.

- **lot** (search items, item) - `id`, `title`, `url`, `inventory_number`, `current_bid`, `currency`, `bid_count`, `retail_price`, `buyer_premium_percent`, `opens`, `closes`, `initial_closes`, `extended`, `market_status`, `is_closed`, `condition` {`rating`, `condition`, `functional`, `damage`, `missing_parts`, `assembly`, `package`}, `inspection_notes`, `pickup_location` {`id`, `name`, `address`, `city`, `state`, `zip`, `timezone`}, `not_returnable`, `photos`; search items add `position`.
- **search** - `location` {`id`, `slug`, `name`}, `query`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `sort`, `filters_applied`, `items[]`, `facets` {`categories`, `subcategories`, `brands`, `pickup_locations`, `condition_ratings` [{`rating`, `count`}], `auction_event_types`, `auction_event_names`, `colors`, `sizes`} (each [{`name`, `count`}], Nellis's counts of open lots).
- **item** - `requested_id`, the lot fields, `category`, `subcategory`, `brand`, `color`, `size`, `features[]`, `descriptions[]`, `dimensions`, `weight`, `operator`, `final_price`, `bid_history[]` {`time`, `amount`, `status`}.
- **locations** - `location`, `count`, `shopping_locations[]` {`id`, `slug`, `name`, `warehouses`}, `locations[]` {`id`, `name`, `address`, `city`, `state`, `coordinates` {`lat`, `lng`}, `operator`, `shopping_location` {`id`, `slug`, `name`}, `hours` {`monday` ... `sunday`: {`open`, `close`} or `null`}}.
- **categories** - `location`, `category`, `total_open_items`, `count`, `categories[]`, `subcategories[]`, `brands[]` (top 100), `auction_events[]`, `auction_event_types[]`, `pickup_locations[]` (each {`name`, `count`}).

## Guardrails

- Name it "Nellis Auction (nellisauction.com, the liquidation auction marketplace with pickup warehouses in Las Vegas, Phoenix, Houston, Philadelphia, Denver and Dallas)" on first mention, "Nellis Auction" or "Nellis" after that.
- Bids: quote `current_bid` with its `bid_count`, `closes` and the `fetched_at` time; it is the high bid at that moment, not a price the lot sold for. Quote `final_price` as "closing price (before the buyer's premium and tax)".
- Estimated Retail Price: always "Nellis's Estimated Retail Price" or "est. retail as Nellis lists it". Never call it an MSRP, a verified retail price or a price a retailer charged.
- Comparisons: show the numbers and their difference only (bid or final price, the premium figure, Nellis's Estimated Retail Price, Amazon's or Walmart's price, eBay sold prices, each with its date). Never give a value verdict on a lot (deal, bargain, worth it, steal, junk, rip-off) or a legitimacy verdict on any platform.
- Bidding: describe bids only as the page showed them. Never speculate about who bid, why, or whether bidding is genuine.
- Same item only: compare a Nellis lot with Amazon, Walmart or eBay only where the titles match on brand and model, each price with its seller and date; Nellis shows no UPC.
- Fees: quote the buyer's premium as Nellis states it ("typically 15% but may vary based on the auction event") with the lot's `buyer_premium_percent`; never compute sales tax.
- Condition: stars and grade text exactly as returned; never "like new" unless that is the label, never infer whether an item works.
- Bid history: no bidder names or ids are returned; never try to identify bidders. Do not republish Nellis photos; link lots by `url` instead.
- Terms: Scavio does not collect or store Nellis Auction data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Nellis's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate bids, final prices, retail prices, ids, dates or warehouse hours. Only return what the API returned, with the `fetched_at` time and the lot `url`.
- Not available: closed or sold lots in search (by id only), search suggestions, shipping (pickup only), UPC or model numbers, buy-now, reserve prices, live bid updates, bidding, watchlists, pickup booking, price history (store your own), cart or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `location` outside the 6 (slugs or ids 1, 2, 5, 6, 7, 8); a `pickup_location` of another shopping location; `page_size` other than 48, 120 or 240; a `page` past Nellis's 30,000 positions; an unknown `sort`; `condition_rating` outside 1-5; `retail_min` above `retail_max`; more than 10 values in a filter list; item without `id` or `url`, an `id` that is not digits, a link that is not a nellisauction.com/p/ item link, or `id` and `url` naming different lots.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Nellis Auction has no item <id>.", "Nellis Auction has no open items in category "<category>" in <location>. Use a name from categories[].name.", "Nellis Auction has no results for this search.". Take ids and names from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=nellis-auction-api).
- `502` means Nellis Auction data was temporarily unavailable ("Nellis Auction is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Nellis Auction is busy ("Nellis Auction is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.87.0
npm install scavio@0.88.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.nellis.search({ q: "vacuum", location: "phoenix", sort: "bids_high" });
const { data: lot } = await scavio.nellis.item({ id: "141281552" });
const { data: sold } = await scavio.nellis.item({ id: "141100004" });
const { data: warehouses } = await scavio.nellis.locations();
const { data: counts } = await scavio.nellis.categories({ location: "las-vegas" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.nellis.search(...)`, `item`, `locations` and `categories`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 4 endpoints as tools: `search_nellis`, `get_nellis_item`, `get_nellis_locations` and `get_nellis_categories`. Nellis Auction is opt-in: add `nellis` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.87.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,nellis"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/nellis-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=nellis-auction-api), [item](https://scavio.dev/docs/nellis-item?utm_source=agent-skills&utm_medium=skill&utm_campaign=nellis-auction-api), [locations](https://scavio.dev/docs/nellis-locations?utm_source=agent-skills&utm_medium=skill&utm_campaign=nellis-auction-api), [categories](https://scavio.dev/docs/nellis-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=nellis-auction-api). Overview: [Nellis Auction API](https://scavio.dev/nellis-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=nellis-auction-api).
