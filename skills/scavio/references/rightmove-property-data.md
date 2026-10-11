# Rightmove Property Data API - UK Listings, England and Wales Sold Prices, Agents

Search UK property for sale or to rent on Rightmove, read one listing in full, pull sold house prices for a town, outcode or postcode with each address's full sale history, resolve a place name to a Rightmove location, and list estate and letting agent branches. It works as a Rightmove scraper API: every endpoint returns structured JSON, with no HTML parsing on your side.

## When to trigger

Use this skill when the user asks to:
- Search UK homes, flats or land for sale or to rent on Rightmove by town, area, outcode, postcode, station or agent branch
- Filter UK listings by price, bedrooms, bathrooms, property type, garden, parking, new home, tenure, days since added, furnishing or let type
- Look up one Rightmove listing by URL or id: description, rooms, floorplans, EPC, tenure and lease years, council tax band, service charge, ground rent, flood risk, nearest stations, the agent
- Get sold house prices in England or Wales: what an address or street sold for and when, with each sale since 1995 and the area's average price over the last year
- Build UK comps for a valuation, or track price changes between sales of the same address
- Find estate or letting agents in a UK area, with phone numbers, address and whether they handle sales or lettings
- List every property a given agent branch has on Rightmove

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every Rightmove endpoint costs **1 credit** per call.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/rightmove/locations` | 1 | UK places matching a name, outcode, postcode or station, each with the `location_id` that search and agents take |
| `POST /api/v1/rightmove/search` | 1 per page | Listings for sale or to rent, 24-25 per page: price with its qualifier (e.g. Offers Over), beds, baths, type, address, coordinates, summary, key features, images, tenure, listing dates, under offer and auction flags, and the agent |
| `POST /api/v1/rightmove/property` | 1 | One listing in full: description, key features, rooms, sizes, images, floorplans, brochures, EPC, tenure and lease years remaining, council tax band, service charge, ground rent, heating, parking, garden, flood risk, broadband, nearest stations, letting terms and the agent branch |
| `POST /api/v1/rightmove/sold` | 1 per page | Sold prices for a town, outcode or postcode in England and Wales, 25 addresses per page, each with its sale history since 1995 (price, date, tenure, new build), plus an area summary with the average price over the last year |
| `POST /api/v1/rightmove/sold-property` | 1 | One sold address: every recorded sale with price, date, tenure, new-build flag and percent change since the previous sale, plus the archived last listing when there was one |
| `POST /api/v1/rightmove/agents` | 1 per page | Estate and letting agent branches for a location, 20 per page: name, brand, company and brand ids, sales and lettings phones, address, sales and lettings flags, profile URL, logo |
| `POST /api/v1/rightmove/agent` | 1 | One agent branch: address, phones, coordinates, company, sales, lettings, commercial and development flags, descriptions, affiliations, and the count plus a teaser of its listings for sale and to rent |

## Workflow

1. **Location:** call `/rightmove/locations` with `query` (e.g. `Bristol`, `SW11`) and take a `location_id` such as `REGION^219`. Search and agents also accept `location` as a plain place name, resolved to its first match and echoed back in `location`.
2. **Search:** call `/rightmove/search` with `location_id` (or `location`, or `branch_id`) plus filters. Each row carries `property_id` and `url`.
3. **Listing:** call `/rightmove/property` with a `property_id` from step 2, or a pasted `url`.
4. **Sold prices:** call `/rightmove/sold` with `location` (a town, outcode or full postcode in England or Wales). Each address carries `sold_id`; call `/rightmove/sold-property` with it for the per-sale percent change and the archived last listing.
5. **Agents:** call `/rightmove/agents` with `location_id` or `location`, then `/rightmove/agent` with a `branch_id` (or the branch `profile_url`). Every listing an agent has: `/rightmove/search` with `branch_id`.

### Pagination

- **Search:** `page` 1-42, 24-25 listings per page (about 1,000 per search). The response carries `total`, `count` and `max_page`.
- **Sold:** `page` 1-40, 25 addresses per page. The response carries `total`, `count` and `max_page`.
- **Agents:** `page` 1-50, 20 branches per page. The response carries `total` and `max_page`.
- **Locations, property, sold-property, agent:** no paging.

Every page is 1 credit, so state the budget before looping.

## Parameters

### Locations (`/locations`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Town, area, outcode (`SW11`), postcode or station, 1-100 chars |

### Search (`/search`)

Pass exactly one of `location_id`, `location` or `branch_id`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location_id` | string | one of | From locations: `REGION^`, `OUTCODE^`, `POSTCODE^` or `STATION^` (e.g. `REGION^219`) |
| `location` | string | one of | A place name, resolved to its first location match |
| `branch_id` | string | one of | Only this agent branch's listings (from agents or a listing's `agent`) |
| `listing_status` | string | `for_sale` | `for_sale` or `for_rent` |
| `min_price` / `max_price` | number | -- | GBP; monthly rent on `for_rent` |
| `beds_min` / `beds_max` | integer | -- | Bedrooms, 0-10 |
| `baths_min` | integer | -- | Minimum bathrooms, 1-5 |
| `property_types` | string[] | -- | `detached`, `semi_detached`, `terraced`, `flat`, `bungalow`, `land`, `park_home` |
| `must_have` | string[] | -- | `garden`, `parking`, `new_home` |
| `exclude` | string[] | -- | `auction`, `retirement`, `shared_ownership`, `new_home` |
| `tenure` | string | -- | `for_sale` only: `freehold` or `leasehold` |
| `added_within_days` | integer | -- | `1`, `3`, `7` or `14` |
| `include_under_offer` | boolean | -- | Include under offer / sold STC (`for_sale`) or let agreed (`for_rent`) |
| `radius_miles` | number | `0` | `0`, `0.25`, `0.5`, `1`, `3`, `5`, `10`, `15`, `20`, `30` or `40` |
| `furnishing` | string[] | -- | `for_rent` only: `furnished`, `part_furnished`, `unfurnished` |
| `let_type` | string | -- | `for_rent` only: `long_term` or `short_term` |
| `sort` | string | `newest` | `newest`, `oldest`, `price_low`, `price_high` |
| `page` | integer | 1 | 1-42 |

There is no keyword filter. A request carrying `keywords` is rejected with a `400` (not billed); match on `summary` and `key_features` in the results instead.

### Property (`/property`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `property_id` | string | one of | Numeric listing id from search (e.g. `93577917`) |
| `url` | string | one of | A `rightmove.co.uk/properties/<id>` URL |

### Sold (`/sold`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | required | A town, outcode (`SW11`) or full postcode (`SW11 1AA`) in England or Wales, 2-80 chars |
| `property_type` | string | -- | `flat`, `detached`, `semi_detached`, `terraced`, `other` |
| `tenure` | string | -- | `freehold` or `leasehold` |
| `sold_within_years` | integer | -- | `1`, `2`, `3`, `5`, `10`, `15`, `20` or `30` |
| `radius_miles` | number | `0` | `0` to `40`, same steps as search |
| `sort` | string | `newest` | `newest` (latest sale first), `price_low`, `price_high` |
| `page` | integer | 1 | 1-40 |

### Sold property (`/sold-property`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sold_id` | string | one of | The `sold_id` from sold (e.g. `921d33f4-d206-4991-be4d-75cbe71981ce`) |
| `url` | string | one of | A `rightmove.co.uk/house-prices/details/<id>` URL |

### Agents (`/agents`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location_id` / `location` | string | one of | Same as search; pass exactly one |
| `page` | integer | 1 | 1-50, 20 branches per page |

### Agent (`/agent`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `branch_id` | string | one of | Numeric branch id from agents or a listing's `agent` (e.g. `201404`) |
| `url` | string | one of | A branch profile URL (`profile_url` from agents) |

Pass exactly one of each "one of" pair on property, sold-property and agent.

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/rightmove/sold \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": "Bristol", "property_type": "terraced", "sold_within_years": 2}'
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def rightmove(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/rightmove/{endpoint}", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]

# 1. Resolve a place to a location_id
loc = rightmove("locations", {"query": "Bristol"})["locations"][0]      # REGION^219

# 2. Freehold houses for sale, 3+ beds, with a garden, added in the last 7 days
found = rightmove("search", {"location_id": loc["location_id"], "beds_min": 3,
                             "property_types": ["detached", "semi_detached", "terraced"],
                             "tenure": "freehold", "must_have": ["garden"],
                             "added_within_days": 7, "max_price": 450000})
print(found["total"], "listings;", found["max_page"], "pages")
for row in found["listings"]:
    print(row["price_qualifier"], row["price"], row["beds"], row["address"], row["url"])

# 3. One listing in full
home = rightmove("property", {"property_id": "93577917"})
print(home["tenure"], home["council_tax_band"], home["price_per_sqft"], home["listing_update"])

# 4. Sold prices in an area, with each address's sale history
sold = rightmove("sold", {"location": "Bristol", "sold_within_years": 2})
print(sold["summary"]["average_price_last_year"], sold["total"], "addresses")
for addr in sold["properties"]:
    last = addr["transactions"][0]
    print(addr["address"], last["price"], last["date"], last["tenure"])

# 5. One address: every sale with the percent change since the previous one
history = rightmove("sold-property", {"sold_id": sold["properties"][0]["sold_id"]})
for t in history["transactions"]:
    print(t["date"], t["price"], t["percent_change"])

# 6. Agent branches in the area, then one branch
agents = rightmove("agents", {"location_id": "REGION^219"})
branch = rightmove("agent", {"branch_id": agents["agents"][0]["branch_id"]})
print(branch["name"], branch["phones"], branch["listings"]["for_sale_count"], branch["listings"]["to_rent_count"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **locations** - `query`, `count`, `locations[]` {`location_id`, `type`, `name`}.
- **search** - `listing_status`, `location` {`location_id`, `name`, `type`, `resolved_from_name`}, `total`, `count`, `page`, `max_page`, `listings[]`.
  A row: `property_id`, `url`, `price`, `price_display`, `price_display_secondary`, `price_qualifier`, `price_frequency`, `currency`, `beds`, `baths`, `property_type`, `address`, `latitude`, `longitude`, `summary`, `key_features[]`, `images[]`, `image_count`, `floorplan_count`, `tenure`, `first_listed_at`, `updated_at`, `listing_update` {`reason`, `date`}, `let_available_date`, `status`, `under_offer`, `auction`, `new_home`, `featured`, `agent` {`branch_id`, `name`, `phone`, `profile_url`}.
- **property** - `property_id`, `url`, `price`, `price_display`, `price_secondary`, `price_qualifier`, `price_frequency`, `price_per_sqft`, `currency`, `channel`, `beds`, `baths`, `property_type`, `address`, `postcode` {`outcode`, `incode`}, `country`, `latitude`, `longitude`, `summary`, `description`, `key_features[]`, `rooms[]`, `sizings[]`, `images[]`, `floorplans[]` {`url`, `caption`}, `virtual_tours[]`, `brochures[]`, `epc[]`, `tenure` {`type`, `lease_years_remaining`}, `council_tax_band`, `service_charge_annual`, `ground_rent_annual`, `features` {`heating`, `parking`, `garden`, `accessibility`, `electricity`, `water`, `sewerage`, `flood_risk`, `listed`, `restrictions`, `rights_of_way`}, `broadband[]`, `nearest_stations[]` {`name`, `types[]`, `distance_miles`}, `letting`, `shared_ownership`, `listing_update`, `agent` {`branch_id`, `name`, `company`, `address`, `phone`, `profile_url`}, `published`, `archived`.
- **sold** - `location` {`slug`, `name`, `type`}, `total`, `count`, `page`, `max_page`, `summary` {`average_price_last_year`, `text[]`, `transactions_count`, `earliest_date`, `latest_date`}, `data_coverage` {`earliest_transaction`, `most_recent_transaction`, `last_updated`}, `properties[]` {`sold_id`, `url`, `address`, `property_type`, `beds`, `baths`, `latitude`, `longitude`, `image`, `transactions[]` {`price`, `price_display`, `date`, `tenure`, `new_build`}}.
- **sold-property** - `sold_id`, `url`, `address`, `postcode`, `country`, `property_type`, `latitude`, `longitude`, `transactions[]` (as above plus `percent_change`), `data_coverage`, `last_listing` {`property_id`, `channel`, `beds`, `baths`, `property_type`, `key_features[]`, `photos[]`, `floorplans[]`, `advertised_from`, `advertised_to`, `nearest_stations[]`} or null.
- **agents** - `location`, `total`, `count`, `page`, `max_page`, `agents[]` {`branch_id`, `name`, `branch_name`, `brand`, `company_id`, `brand_id`, `phones[]` {`number`, `direct`, `type`}, `address`, `sales`, `lettings`, `description`, `profile_url`, `logo`}.
- **agent** - `branch_id`, `name`, `branch_name`, `brand`, `company_name`, `company_id`, `address`, `postcode`, `phones` {`main`, `lettings`}, `latitude`, `longitude`, `sales`, `lettings`, `commercial`, `development`, `overseas`, `description`, `sales_description`, `lettings_description`, `logo`, `profile_url`, `listings` {`for_sale_count`, `to_rent_count`, `for_sale_teaser[]`, `to_rent_teaser[]`}, `affiliations[]`.

A search row, trimmed (captured, Bristol `REGION^219`, for sale):

```json
{
  "property_id": "93577917",
  "url": "https://www.rightmove.co.uk/properties/93577917",
  "price": 290000,
  "price_display": "£290,000",
  "price_qualifier": "Offers Over",
  "currency": "GBP",
  "beds": 3,
  "baths": 1,
  "property_type": "Terraced",
  "address": "New Cheltenham Road, Kingswood, South Gloucestershire, BS15",
  "latitude": 51.46758,
  "longitude": -2.50252,
  "key_features": ["Three Bedroom Terraced Home", "Open-Plan Living Space", "En-suite", "Rear Access to Garden"],
  "tenure": "FREEHOLD",
  "first_listed_at": "2026-09-25T13:50:30Z",
  "listing_update": { "reason": "price_reduced", "date": "2026-10-07T13:57:12Z" },
  "under_offer": false,
  "agent": { "branch_id": "4544", "name": "Andrews Estate Agents, Downend", "phone": "0117 463 9128" }
}
```

A sold address with its sale history (captured, Bristol):

```json
{
  "sold_id": "921d33f4-d206-4991-be4d-75cbe71981ce",
  "url": "https://www.rightmove.co.uk/house-prices/details/921d33f4-d206-4991-be4d-75cbe71981ce",
  "address": "54, Mendip Road, Bedminster, Bristol BS3 4NY",
  "property_type": "terraced",
  "beds": 4,
  "baths": 2,
  "transactions": [
    { "price": 560000, "price_display": "£560,000", "date": "2026-07-30", "tenure": "freehold", "new_build": false },
    { "price": 465000, "price_display": "£465,000", "date": "2021-06-21", "tenure": "freehold", "new_build": false },
    { "price": 239950, "price_display": "£239,950", "date": "2009-10-16", "tenure": "freehold", "new_build": false }
  ]
}
```

The sold area summary (captured, Bristol):

```json
{
  "average_price_last_year": 392025,
  "text": ["House prices in Bristol have an overall average of £392,025 over the last year."],
  "transactions_count": 75,
  "earliest_date": "1995-02-10",
  "latest_date": "2026-07-30"
}
```

## Guardrails

- **Sold prices cover England and Wales only.** Scotland and Northern Ireland addresses are not in `/sold` or `/sold-property`. Say so rather than returning an empty result as "no sales".
- **Sold prices are HM Land Registry Price Paid records and run about two months behind.** `data_coverage.most_recent_transaction` gives the latest sale date covered; say so when the user asks about very recent sales. The free Land Registry file has the same prices; what Rightmove adds is bedrooms, photos, the last listing and each address's grouped history.
- **Page caps.** Search serves 42 pages (about 1,000 listings), sold 40 pages and agents 50 pages per query. To reach more, slice by price band, property type, tenure, years or a smaller area (an outcode or postcode instead of a city), and de-duplicate by `property_id` or `sold_id`. Never claim to have pulled "every listing" when `total` is larger than what the pages cover.
- **No keyword filter on search.** Filter on `summary` and `key_features` yourself; sending `keywords` is a `400`.
- Live listings carry no price history. For what an address sold for, use `/sold` or `/sold-property`.
- Prices are GBP; on `for_rent` they are monthly, with `price_frequency` and `price_display` saying so. Keep `price_qualifier` (Guide Price, Offers Over, Offers in Excess of) next to the number when reporting it.
- Public listing and sold-price data only: no owner, buyer or seller names and no mortgage records.
- Results usually take 1-5 seconds per call; batch sequentially rather than firing many calls at once.
- Never fabricate prices, sale dates or agent details. Only return what the API returned, and surface the listing or sold `url` so the user can verify.

## Failure handling

- `400` means an invalid or missing parameter (none or more than one of `location_id`, `location` and `branch_id`; a `radius_miles` or `added_within_days` outside the listed values; a page past the cap; `keywords` on search) - fix the body and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means the listing, sold address, branch or location does not exist on Rightmove, or the listing was removed; the error names what was not found, and the call is billed (1 credit).
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data).
- `502` / `503` mean Rightmove data is temporarily unavailable - wait a few seconds and retry, up to a few times. These are not billed.
- If a place name resolves to the wrong area, call `/rightmove/locations` and pass the right `location_id`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.20.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

places = client.rightmove.locations("Bristol")
found = client.rightmove.search(location_id="REGION^219", beds_min=3, must_have=["garden"])
home = client.rightmove.property(property_id="93577917")
sold = client.rightmove.sold("Bristol", sold_within_years=2)
history = client.rightmove.sold_property(sold_id="921d33f4-d206-4991-be4d-75cbe71981ce")
agents = client.rightmove.agents(location_id="REGION^219")
branch = client.rightmove.agent(branch_id="201404")
```

```bash
npm install scavio@0.20.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const found = await scavio.rightmove.search({ location_id: "REGION^219", beds_min: 3 });
const sold = await scavio.rightmove.sold({ location: "Bristol", sold_within_years: 2 });
const history = await scavio.rightmove.soldProperty({ sold_id: "921d33f4-d206-4991-be4d-75cbe71981ce" });
```

MCP: the Scavio MCP server exposes all 7 endpoints as tools (`get_rightmove_locations`, `search_rightmove`, `get_rightmove_property`, `get_rightmove_sold`, `get_rightmove_sold_property`, `search_rightmove_agents`, `get_rightmove_agent`). Rightmove is opt-in: add `rightmove` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.18.1"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,rightmove"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [Rightmove search](https://scavio.dev/docs/rightmove-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data), [property](https://scavio.dev/docs/rightmove-property?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data), [sold](https://scavio.dev/docs/rightmove-sold?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data), [sold property](https://scavio.dev/docs/rightmove-sold-property?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data), [locations](https://scavio.dev/docs/rightmove-locations?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data), [agents](https://scavio.dev/docs/rightmove-agents?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data), [agent](https://scavio.dev/docs/rightmove-agent?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data). Overview: [Rightmove API](https://scavio.dev/rightmove-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data).
