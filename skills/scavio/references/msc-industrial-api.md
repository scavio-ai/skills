# MSC Industrial Supply API - Metalworking and MRO Web Prices, Order Minimums, Clearance, Locations

Read MSC Industrial Supply (mscdirect.com, the US metalworking and MRO distributor): keyword, manufacturer part number and MSC# search, category listings by navid, one product with its order rules and specifications, the Clearance Specials and Web Specials lists, and MSC's locations. mscdirect.com only (United States, USD), as shown to a visitor who is not signed in.

**The job this skill is for: what an MSC item costs at its Web Price today, what that price is for, and how MSC lets you order it.** Every item carries the Web Price as MSC shows it, the quantity it is for (each, or per 100), the price of one unit worked out from it, and MSC's minimum order and order multiple. On 2026-11-28 the Hertel jobber length drill bit, 1/8 inch, 118 degree, HSS (MSC# 71205678) read $1.53 each, minimum 12 in multiples of 12, $18.36 for the minimum order, in stock.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **The price and what it is for, apart.** `price` is the Web Price as MSC shows it, `price_unit` and `price_per_quantity` say what it is for (`ea.` is one unit; a price shown as "$14.83 per 100" is for 100 units), and `unit_price` is the price of one unit (`price / price_per_quantity`, worked out by Scavio). `minimum_order_quantity` and `order_multiple` are MSC's order rules.
- **Web Price, not account pricing.** Prices are the Web Price a visitor who is not signed in sees; MSC notes that account pricing may differ.
- **MSC pages are slow.** Search, category and product calls usually take 30-120 seconds and can take about 240; allow a client timeout of at least 300 seconds. Clearance and locations usually take 5-40 seconds.
- **Locations are not pickup stores.** `/locations` lists MSC's customer fulfillment centers, regional inventory centers, warehouses, customer care and support centers, offices, manufacturing facilities and affiliated companies with their business phone numbers. MSC has no customer pickup branches by ZIP and publishes no per-branch stock.
- **No review text or history.** `rating` and `review_count` are aggregates. Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

MSC publishes no public developer API for its catalog or Web Prices. Prices, order rules and specifications are shown on mscdirect.com, and this skill reads those public pages with one Scavio key.

See also: Zoro `zoro-api` and Global Industrial `global-industrial-api` (US industrial and MRO supply), Home Depot `home-depot-product-data`, Lowe's `lowes-product-data`, Harbor Freight `harbor-freight-api`, Ace Hardware `ace-hardware-prices-api`.

## When to trigger

Use this skill when the user asks to:
- Price an MSC item at its Web Price: price, what it is for (each or per 100), unit price, minimum order and order multiple
- Search mscdirect.com by keyword ("drill bit", "end mill", "nitrile gloves"), by manufacturer part number or by MSC#, sorted by best match, price, MSC# or rating
- Match a catalog by part number: MSC#, manufacturer part number, Big Book page and the alternate MSC numbers MSC lists
- List an MSC category by navid (`2106186`, Jobber Length Drill Bits), with brand, attribute and rating facets
- Read one product: availability, specifications, country of origin, manuals and data sheets, and the Prop 65 flag
- Read the Clearance Specials or Web Specials list
- List MSC's fulfillment centers, inventory centers, warehouses and support centers, by type, state or country

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=msc-industrial-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=msc-industrial-api) - email or Google, no card required.
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
| `POST /api/v1/msc/search` | Keywords, a manufacturer part number or an MSC#: 24 products per page to page 400 in MSC's 6 sorts, with total, Web Price, order rules, availability and rating; category, brand, attribute and rating facets with counts; the product itself when MSC answers an MSC# with its page | 1 |
| `POST /api/v1/msc/category` | A category by navid or link: the same items, sorts and facets, plus the category and its breadcrumbs | 1 |
| `POST /api/v1/msc/product` | One product by MSC#: Web Price and order rules, minimum order total, availability, Big Book page, specifications, country of origin, documents, Prop 65 flag and alternate MSC numbers | 1 |
| `POST /api/v1/msc/clearance` | The Clearance Specials list (default) or the Web Specials list: each item's MSC#, order number, name and sale price | 1 |
| `POST /api/v1/msc/locations` | MSC's locations by type, state and country, with address and published business phone numbers | 1 |

United States only: `country` is `us` (the default); anything else is a `400`, not charged. Every answer carries `country` (us) and `currency` (USD), and most carry `note`.

## Prices: Web Price, what it is for, unit price and order rules

| Field | Meaning |
|---|---|
| `price` | The Web Price as MSC shows it, in USD ($1.53 on the drill bit below) |
| `price_text` | The price as written ("$1.53 ea.") |
| `price_unit` | What the price is for: `ea.` or `per 100` |
| `price_per_quantity` | The quantity the price is for: 1 or 100 |
| `unit_price` | The price of one unit, `price / price_per_quantity`, worked out by Scavio (a price of "$14.83 per 100" is 0.1483 a unit) |
| `order_unit` | What one order unit is, where MSC states it (e.g. "(1) 100 Pack") |
| `minimum_order_quantity`, `order_multiple` | The smallest quantity MSC accepts and the step it sells in ("Enter in multiples of 12") |
| `minimum_order_price` (listings), `minimum_order_total` (product) | The order price for the minimum quantity ($18.36 for 12) |
| `sale_price` (clearance) | The list's price for its `order_number` |

- Quote "Hertel jobber length drill bit 1/8 in, MSC# 71205678: $1.53 each, minimum 12 in multiples of 12, on mscdirect.com on 2026-11-28", with the date, what the price is for and the order rule.
- Quote `price`, `price_unit` and the order rules exactly as given; `unit_price` is a worked-out figure, so say so. Never judge a price as a good deal, and never present a Web Price as a buyer's account price.

## Workflow

1. **Find products.** `/search` with `query` (keywords, a manufacturer part number or an MSC#), optionally `sort`. A search for an MSC# returns that product (`redirected_to` {type product}).
2. **Browse.** `/category` with `navid` (`categories[].navid` of a search, `breadcrumbs[].navid` of a product) or `url` (an mscdirect.com category link carrying `navid=`).
3. **Next pages.** Send `page` 2, 3, ... with the same input, up to page 400. `has_more` false means the last page.
4. **One product.** `/product` with `msc_number` (`items[].msc_number`, 8 digits with leading zeros) or `url`.
5. **Specials.** `/clearance` with `{}` for Clearance Specials or `{"list": "web_specials"}`.
6. **Locations.** `/locations` with `{}` for all, or `type`, `state` and `location_country`.
7. **Watching prices:** there is no history. Poll the same MSC numbers on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`) and category (`/category`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords, a manufacturer part number or an MSC#, 1-200 characters |
| `navid` (category) | An MSC category id (`categories[].navid`, `breadcrumbs[].navid`), e.g. `2106186` |
| `url` (category) | An mscdirect.com category link carrying `navid=`, instead of `navid` |
| `sort` | `bestmatch` (default), `price` (low to high), `price_desc` (high to low), `itemnumber`, `itemnumber_desc` (by MSC#) or `rating` |
| `page` | 1-400 (24 per page); `total_pages` gives the last one |
| `country` | `us` (default) |

### Product (`/product`)

Send `msc_number` (the MSC#, 8 digits with leading zeros: `items[].msc_number`, e.g. `00647354`) or `url` (an mscdirect.com product link, `https://www.mscdirect.com/product/details/<MSC#>`).

### Clearance (`/clearance`) and locations (`/locations`)

| Parameter | Description |
|---|---|
| `list` (clearance) | `clearance` (default, Clearance Specials) or `web_specials` (Web Specials) |
| `type` (locations) | One location type as MSC names it: Customer Fulfillment Center, Regional Inventory Center, Warehouse, Customer Care Center, Customer Support Center, Shared Services Center, Procurement Office, Manufacturing Facility or Affiliated Company |
| `state` (locations) | One US state, 2-letter code (`PA`) |
| `location_country` (locations) | One country as MSC lists it (United States, Canada, Mexico, United Kingdom, Ireland, Asia) |

## Examples

### One search item

Request `{"query": "drill bit"}` (1 credit): `total` 132,055, `total_pages` 400, 24 items, 39 categories (first Jobber Length Drill Bits, navid 2106186, 51,048), 87 brands, filters {`in_stock` 40,833, `made_in_usa` 45,340}, 15 attribute facets. One item:

```json
{
  "position": 1,
  "msc_number": "71205678",
  "name": "Jobber Length Drill Bit: 1/8\" (0.1250) Dia, 118 deg, HSS",
  "subtitle": "Oxide Finish, 2-3/4\" OAL, Right Hand Cut, Regular Spiral Flute, Straight Shank",
  "brand": "Hertel",
  "mfr_number": "71205678",
  "currency": "USD",
  "price": 1.53,
  "price_text": "$1.53 ea.",
  "price_unit": "ea.",
  "price_per_quantity": 1,
  "unit_price": 1.53,
  "minimum_order_quantity": 12,
  "order_multiple": 12,
  "order_unit": null,
  "minimum_order_price": 18.36,
  "availability": "In Stock",
  "in_stock": true,
  "rating": 4.9,
  "review_count": 7,
  "alternative_msc_numbers": ["78502168", "81181083", "63687081"]
}
```

The item also carried `url` and `image`.

### One product

Request `{"msc_number": "71205678"}` (1 credit), abridged:

```json
{
  "msc_number": "71205678",
  "mfr_number": "71205678",
  "big_book_page": "10",
  "name": "Jobber Length Drill Bit: 1/8\" (0.1250) Dia, 118 deg, HSS",
  "brand": "Hertel",
  "price": 1.53,
  "price_text": "$1.53 ea.",
  "unit_price": 1.53,
  "minimum_order_quantity": 12,
  "order_multiple": 12,
  "minimum_order_total": 18.36,
  "availability": "In Stock",
  "in_stock": true,
  "purchasable": true,
  "category": { "name": "Jobber Length Drill Bits", "navid": "2106186" },
  "country_of_origin": "UNITED STATES",
  "compliance": { "prop65": true, "notices": ["Prop 65 Warning"] }
}
```

The product also carried 4 `breadcrumbs` (from Holemaking down), 27 `specifications` (Drill Bit Size (Inch) 1/8, ...), 2 images and 3 `alternative_msc_numbers`.

### Category, specials and locations

- `/category` `{"navid": "2106186"}`: Jobber Length Drill Bits, `total` 51,048, 400 pages of 24, brands led by Guhring (8,410), 17 attribute facets (Drill Bit Size (Inch) with 69 values, ...).
- `/clearance` `{}`: Clearance Specials, 60 items, heading "Prices valid for current inventory only - Sorry, no backorders accepted.", e.g. SUPER LUBE Air Tool Lubricant 4oz at $14.99 (order number TL02105898). MSC publishes no end dates on these lists.
- `/locations` `{}`: 63 locations in 9 types (Affiliated Company 29, Warehouse 13, Customer Care Center 8, Regional Inventory Center 8, Manufacturing Facility 5, Customer Support Center 3, Customer Fulfillment Center 2, ...), e.g. Harrisburg, PA (Customer Fulfillment Center and Customer Care Center, 100 MSC Dr., Jonestown, PA 17038, toll free 1-800-645-7270).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def msc(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/msc/{endpoint}", headers=HEADERS, json=body, timeout=300)
    r.raise_for_status()
    return r.json()

# 1. Drill bits, lowest price first (1 credit)
hits = msc("search", {"query": "drill bit", "sort": "price"})["data"]
for it in hits["items"][:5]:
    print(it["msc_number"], it["name"], it["price_text"], it["unit_price"], it["minimum_order_quantity"], it["order_multiple"])

# 2. One product by MSC# (1 credit)
item = msc("product", {"msc_number": hits["items"][0]["msc_number"]})["data"]
print(item["price"], item["price_unit"], item["minimum_order_total"], item["availability"])

# 3. The Clearance Specials list (1 credit)
specials = msc("clearance", {})["data"]
for s in specials["items"][:5]:
    print(s["msc_number"], s["name"], s["sale_price"])

# MSC Web Prices change. Store each answer with fetched_at and run this on a
# schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `country` and `currency`.

- **search / category** - `query` and `redirected_to` {`type`, `msc_number`, `url`} (search), `navid`, `category` {`name`, `navid`, `url`} and `breadcrumbs[]` {`name`, `navid`, `url`} (category), `page`, `page_size` (24), `sort`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `msc_number`, `name`, `subtitle`, `brand`, `mfr_number`, `url`, `image`, `currency`, `price`, `price_text`, `price_unit`, `price_per_quantity`, `unit_price`, `order_unit`, `minimum_order_quantity`, `order_multiple`, `minimum_order_price`, `availability`, `in_stock`, `rating`, `review_count`, `alternative_msc_numbers`}, `categories[]` {`name`, `navid`, `count`}, `brands[]` {`value`, `count`} (the 50 with the most items), `brand_count`, `filters` {`in_stock`, `made_in_usa`, `clearance`, `new_additions`, `eco_friendly`}, `ratings[]` {`stars`, `count`}, `attributes[]` {`name`, `value_count`, `values[]` {`value`, `count`}} (up to 50 values each), `note`.
- **product** - `requested_msc_number`, `msc_number`, `mfr_number`, `big_book_page`, `name`, `subtitle`, `brand`, `brand_logo`, `url`, `images`, the price and order fields above, `minimum_order_total`, `availability`, `in_stock`, `purchasable`, `rating`, `review_count`, `breadcrumbs[]`, `category` {`name`, `navid`}, `specifications[]` {`name`, `value`}, `country_of_origin`, `documents[]` {`title`, `url`, `format`, `size`}, `compliance` {`prop65`, `prop65_warning`, `notices`}, `alternative_msc_numbers`, `note`.
- **clearance** - `list`, `name`, `url`, `heading`, `count`, `items[]` {`position`, `msc_number`, `order_number`, `name`, `label`, `sale_price`, `currency`, `image`, `url`}, `note`.
- **locations** - `total`, `type`, `state`, `location_country`, `count`, `location_types[]` {`type`, `count`}, `locations[]` {`name`, `types`, `affiliate`, `address` {`line1`, `line2`, `city`, `state`, `zip`, `country`}, `phones` {`toll_free`, `local`, `fax`, `other[]` {`label`, `number`}}, `website`}, `note`.

## Guardrails

- Name it "MSC Industrial Supply (mscdirect.com, the US metalworking and MRO distributor)" on first mention. MSC accounts, carts, quotes and checkout are not read or made.
- Prices: quote `price` with `price_unit` (each or per 100) and the order rules, in USD, with the `fetched_at` date. Say `unit_price` is worked out from the Web Price. Never present a Web Price as account or contract pricing.
- Stock: `availability` and `in_stock` are MSC's own text and flag. MSC shows no unit counts and no per-branch stock; never present them as a stock count.
- Locations: they are MSC's distribution, inventory, support and office locations with business phone numbers, not stores a customer can walk into or pick up from. Never send a buyer to one as a pickup point.
- Specials: the Clearance Specials and Web Specials lists are curated by MSC (about 60 items each), not every discounted item, and carry no end dates. Never invent one.
- Comparing MSC with Zoro, Global Industrial or another supplier: compare the same manufacturer part number, the same unit and the same date. Never call one supplier cheaper beyond the numbers shown.
- Use: keep any use descriptive - looking up an item's price, order rules and specifications for purchasing and catalog matching by part number.
- Images and copy: refer to products by MSC# and manufacturer part number; do not republish MSC's product photos, page copy or catalog.
- Not available: review text, account pricing, delivery estimates, per-branch stock, pickup branches by ZIP, price history (poll and store), carts or checkout. This API cannot buy or request a quote.
- Terms: Scavio does not store MSC data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. MSC's terms of use restrict automated access to its site and how its content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, order rules, specifications or locations. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "country must be us (default): MSC Industrial Supply (mscdirect.com) serves the United States."; "msc_number or url is required: ..."; "navid is required: ..."; "sort must be one of: bestmatch, price, price_desc, itemnumber, itemnumber_desc, rating."; "list must be one of: clearance, web_specials."; "state must be a 2-letter US state code, e.g. PA."; "type must be one of: ...".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "No MSC product with MSC# <msc>. Use an MSC# from items[].msc_number (8 digits, e.g. 00647354).", "No MSC category with navid <navid>. Use a navid from categories[].navid or breadcrumbs[].navid (e.g. 2106186).". A search with no products is a `200` with `total` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=msc-industrial-api).
- `502` and `503` mean MSC data was temporarily unavailable ("MSC Industrial Supply is temporarily unavailable. Please try again." or "MSC Industrial Supply is busy right now. Please retry in a few seconds.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- Search, category and product usually take 30-120 seconds, up to about 240; clearance and locations 5-40 seconds. Allow a client timeout of at least 300 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.107.0
npm install scavio@0.108.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.msc.search({ query: "drill bit", sort: "price" });
const { data: jobbers } = await scavio.msc.category({ navid: "2106186", page: 2 });
const { data: item } = await scavio.msc.product({ msc_number: "71205678" });
const { data: specials } = await scavio.msc.clearance({ list: "web_specials" });
const { data: sites } = await scavio.msc.locations({ type: "Regional Inventory Center" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.msc.search(...)`, `category`, `product`, `clearance` and `locations`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 5 endpoints as tools: `search_msc`, `get_msc_category`, `get_msc_product`, `get_msc_clearance` and `get_msc_locations`. MSC is opt-in: add `msc` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.107.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,msc"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/msc-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=msc-industrial-api), [category](https://scavio.dev/docs/msc-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=msc-industrial-api), [product](https://scavio.dev/docs/msc-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=msc-industrial-api), [clearance](https://scavio.dev/docs/msc-clearance?utm_source=agent-skills&utm_medium=skill&utm_campaign=msc-industrial-api), [locations](https://scavio.dev/docs/msc-locations?utm_source=agent-skills&utm_medium=skill&utm_campaign=msc-industrial-api). Platform page: [scavio.dev/msc-api](https://scavio.dev/msc-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=msc-industrial-api).
