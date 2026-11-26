# Boots UK API - Boots.com Prices, Offers, Store Stock, Stores

Read Boots (boots.com, the UK health and beauty retailer with over 1,800 stores, and boots.ie in Ireland): one product in full from its link or 8-digit id, whether the Boots stores near a UK postcode or a point have it (or one shade or size), the Boots stores near a postcode or a town, and one store page. Every answer is what Boots' public pages show a visitor without an account at the moment of the call, in GBP on boots.com or EUR on boots.ie. All 4 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Boots shows to any visitor and returns them as JSON for analysis. It uses no Boots account, no Advantage Card login, no basket, no checkout and no reservation.

**Start from a product link.** Boots search is not available yet: there is no keyword search, category, brand or deal list. Every workflow starts from a Boots product link (`https://www.boots.com/<name>-<8-digit id>`) or the 8 digits it ends with, which the user or another source supplies.

**The job this skill is for: one Boots product's price and offers, and which nearby Boots stores have it.** The price with Boots' was price and Save amount, the offers and promo codes Boots names on the page, the same product on boots.ie, then the stores near a postcode that have the exact shade or size, in stock or out of stock as Boots shows it. Captured 2026-11-26 with `/product` (1 credit each):

| Product (id) | boots.com | boots.ie |
|---|---|---|
| CeraVe AM Facial Moisturising Lotion SPF30 52ml (10331199) | 11.62 GBP, was 15.50, save 3.88 ("52 ML \| £223.46 per 1L") | 13.50 EUR, was 18, save 4.50 ("0.052 L \| €259.62 per 1L") |
| Maybelline Fit Me Matte & Poreless Liquid Foundation 30ml (10213975) | 9.99 GBP, no was price, 23 shades | - |
| No7 Protect And Perfect Intense ADVANCED Serum 30ml (10288490) | 27.95 GBP, no was price | - |
| La Roche-Posay HyaluB5 Hyaluronic Acid Cream 40ml (10242623) | - | 32 EUR, was 40, save 8 |

boots.ie sets its own euro prices; they are not converted from sterling. Then `/store-stock` for one shade near a postcode. Maybelline Fit Me in Ivory (`item_code` 10213975001) near NG2 3AA (Nottingham): Boots checked 45 stores, 43 had it in stock; Nottingham Beeston (0.7 miles) and Nottingham Riverside Park (1.36 miles) "In Stock", Nottingham Victoria Centre (2.78 miles) "Out of Stock". CeraVe AM near SW11 1QN (London): 79 of 85 stores in stock. On boots.ie, CeraVe AM near a point in central Dublin: 37 of 41 stores in stock, first Dublin Henry Street at 0.07 miles.

Eight limits shape every answer, so say them plainly:
- **1 credit per call.** `credits_used` in every answer says what was spent: a request Boots answered only on the second attempt costs 2 credits (3 for a two-step lookup: a product by id, a store by number or name). A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **No search.** Start from a product link or its 8-digit id. `product_id` is looked up in Boots' product list first (5 to 20 seconds more); a link is faster.
- **Stock is in or out, not a count.** `/store-stock` returns `availability` (`in_stock` or `out_of_stock`), Boots' own `availability_text` and `stockist` (the store carries the line) per store. Boots shows no unit counts; never report a number of units.
- **Shades and sizes have their own item code.** A product with shades or sizes lists `variants[]` {`name`, `item_code` (11 digits), `catentry_id`, `online_in_stock`}; send that `item_code` to `/store-stock` with the product's own `catentry_id` (not the variant's). A product without shades or sizes uses its 8-digit id as `item_code`. The price is the product's: Boots shows no separate price per shade or size.
- **No stores can mean an unknown code.** When no store near the place has the item, Boots says so ("This product isn't currently available in the area you have searched. Please try another area."): `stores` is empty, `stores_searched` says how many stores it checked, and the answer is charged. Boots answers an item code it does not know the same way (a made-up code checked 105 stores and returned that message), so always take `item_code` and `catentry_id` from `/product`.
- **Two markets.** `market` `uk` (boots.com, GBP, default) or `ie` (boots.ie, EUR). Some UK products are not sold on boots.ie (a `404`). On `ie`, stores are found by town (`city`), and `/store-stock` needs `latitude` and `longitude` (take them from `/stores` for a town); store pages are found by `name` or slug, not by number.
- **Offers as Boots words them.** `offers[]` {`text`, `code`} are the offer lines on the page, with `code` set when the line names a promo code ("Use code SAVE20 to save 20 percent on selected Skincare and Haircare - online only"); one line can carry Boots' own was-and-now wording ("Was £17, Was £15.50, Now £11.62"). `advantage_card_offers` are the Advantage Card offers Boots names on the page. Quote them as given; a price after a code is your own arithmetic.
- **What is not there.** No search, category, brand or deal lists, no reviews or ratings, no type-ahead, no stock counts, no EAN, no price per shade or size, no price history (store your own answers with `fetched_at`), no basket or checkout.

Boots publishes no public API for its catalogue, prices or store stock; its affiliate programme runs on Awin for approved publishers. This skill reads Boots' public product and store pages with one Scavio key and needs no affiliate approval. Other vendors offer Boots data tools; this skill reads Boots' own public pages.

See also: `lookfantastic-api` (Lookfantastic UK), `cult-beauty-api` (Cult Beauty), `space-nk-api` (Space NK UK and Ireland) and `amazon-product-data` (Amazon.co.uk) for the same product at another UK retailer; `walgreens-product-data` and `cvs-product-data` for US drugstore prices. Same product and size only: brand + product name + size in both titles, each price with its retailer, currency and date.

## When to trigger

Use this skill when the user asks to:
- Read a Boots product's price, was price, Save amount, unit price, offers and promo codes from its link or id
- Put a boots.com price next to the same product on boots.ie
- List a Boots product's shades or sizes with their item codes and online stock
- Check which Boots stores near a UK postcode (or a point in Ireland) have a product, shade or size in stock
- Find Boots stores near a UK postcode or a town in the UK or Ireland, with their services
- Read one Boots store's address, phone and weekly hours

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=boots-uk-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=boots-uk-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Calls in this skill cost 1 credit, so 50 credits cover about 50 product or store-stock calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, store 2-5 seconds, product 3-11 by link and 10-19 by id, store-stock 9-63 and stores 24-37. Set a client timeout of at least 240 seconds and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/boots/product` | One product by link or 8-digit id: price, was price, saving, size, unit price, item number, `catentry_id`, online stock, shades or sizes with item codes, offers and promo codes, Advantage Card offers, description, sections, ingredients | 1 |
| `POST /api/v1/boots/store-stock` | The Boots stores near a UK postcode or a point that have one product, shade or size: in or out of stock per store, nearest first, with address, phone, distance and hours | 1 |
| `POST /api/v1/boots/stores` | Boots stores near a UK postcode or a town (uk and ie): store number, address, coordinates, distance, services; the place's latitude and longitude | 1 |
| `POST /api/v1/boots/store` | One store page by slug or link, store number (boots.com) or exact name: address, phone, weekly hours, services | 1 |

Every endpoint costs 2 when Boots answered on the second attempt (3 for a product by id or a store by number or name); `credits_used` is the truth.

## Markets

| `market` | Site | Currency | Notes |
|---|---|---|---|
| `uk` (default) | boots.com | GBP | `/store-stock` by `postcode` (a full UK postcode) or `latitude` + `longitude`; `/stores` by `postcode` or `city`; `/store` by `store`, `store_number` or `name` |
| `ie` | boots.ie | EUR | Boots' own euro prices; some UK products are not sold there (`404`). `/store-stock` by `latitude` + `longitude` only; `/stores` by `city` only; `/store` by `store` or `name` |

A product link sets the market from its site; a `market` that does not match the link is a `400`.

## Prices, offers and stock

| Field | Meaning |
|---|---|
| `price` | Boots' price, GBP on uk, EUR on ie |
| `was_price` | Boots' was price, when shown; `null` otherwise |
| `saving` | Boots' Save amount, when shown |
| `size`, `unit_price`, `unit_price_per`, `unit_price_text` | As Boots shows them ("52 ML", 223.46 per "1L", "52 ML \| £223.46 per 1L") |
| `item_number`, `part_number` | The item number on the page (5728371) and Boots' part number (10331199.P) |
| `catentry_id` | The product's id for `/store-stock` (2857120) |
| `online_in_stock` | Online stock status, not store stock |
| `variants[]` | {`name` (shade or size), `item_code` (for `/store-stock`), `catentry_id`, `online_in_stock`}; one row with an empty `name` and the 8-digit id when there are no shades or sizes |
| `offers[]` | {`text`, `code`}: offer lines as Boots words them; `code` is a promo code the line names (SAVE20) |
| `advantage_card_offers` | The Advantage Card offers Boots names on the page ("My Offers: Double Advantage Card points when you buy selected Cerave"); members add them to their card |
| `sections[]` | {`title`, `text`}: Suitable for, How to use, Hazards and cautions, Important info, Ingredients, as the page has them |
| `availability`, `availability_text`, `in_stock` (store-stock) | `in_stock` or `out_of_stock` per store and Boots' words ("In Stock", "Out of Stock") |
| `stockist` (store-stock) | The store carries the line |

- **Percent off:** compute it from `price` and `was_price` and label it computed (11.62 against 15.50 is 25.0% off, computed).
- **Ids:** send `product_id`, `item_code`, `catentry_id` and `store_number` as strings (numbers are accepted, but the strings keep leading digits exactly).

## Workflow

1. **Get the product link.** From the user or another source (Boots search is not available). The 8 digits it ends with are the `product_id`.
2. **Read the product.** `/product` with `url` (faster) or `product_id`, and `market`. Note `price`, `was_price`, `saving`, `offers`, `catentry_id` and each `variants[].item_code`.
3. **The other market.** `/product` with the same `product_id` and `market` `ie` (or `uk`); a `404` means it is not sold there.
4. **Pick the place.** UK: a full postcode. Ireland: `/stores` with `city` (and `market` `ie`) for the town's `latitude` and `longitude`.
5. **Check stores.** `/store-stock` with the shade's `item_code`, the product's `catentry_id` and the postcode or point. Read `count`, `in_stock_count`, `stores_searched` and each store's `availability_text` and `distance_miles`.
6. **Store details.** `/store` with `store_number` (boots.com) or `name` for the address, phone and hours.
7. **Report.** Each price with GBP or EUR, the site and the `fetched_at` date; each stock result with the store's name, distance and Boots' words, never a unit count.
8. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

| Endpoint | Parameter | Type | Description |
|---|---|---|---|
| `/product` | `url` | string | A Boots product link (www.boots.com or www.boots.ie); the market follows the link |
| | `product_id` | string | Or the 8 digits a product link ends with (`"10288490"`); one of `url` or `product_id` |
| | `market` | string | `uk` (default) or `ie` |
| `/store-stock` | `item_code` | string | required: a `variants[].item_code` (11 digits, `"10213975001"`) or the 8-digit id of a product without shades or sizes |
| | `catentry_id` | string | required: the product's `catentry_id` (`"1838584"`) |
| | `postcode` | string | A full UK postcode (`"NG2 3AA"`), uk only |
| | `latitude`, `longitude` | number | Or a point; required on ie (`53.34938`, `-6.26056`) |
| | `market` | string | `uk` (default) or `ie` |
| `/stores` | `postcode` | string | A full UK postcode (`"M1 1AE"`), uk only |
| | `city` | string | Or a town or city (`"Cork"`, `"Dublin"`); the only input on ie |
| | `market` | string | `uk` (default) or `ie` |
| `/store` | `store` | string | A store page slug or link (`"868-london-battersea-sw11-1qn"`, `"cork-boots-patrick-street"`) |
| | `store_number` | string | Or `stores[].store_number` (`"868"`), boots.com only |
| | `name` | string | Or `stores[].name` exactly (`"Cork Patrick Street"`), for boots.ie |
| | `market` | string | `uk` (default) or `ie` |

## Examples

### One product with its offers

```bash
curl -X POST https://api.scavio.dev/api/v1/boots/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.boots.com/cerave-am-facial-moisturising-lotion-spf30-52ml-10331199"}'
```

Captured `data` (2026-11-26; `description`, `sections` and `ingredients` dropped):

```json
{
  "market": "uk",
  "product_id": "10331199",
  "requested_id": "10331199",
  "url": "https://www.boots.com/cerave-am-facial-moisturising-lotion-spf30-52ml-10331199",
  "name": "CeraVe AM Facial Moisturising Lotion SPF30 with UV Protection and 3 essential Ceramides for Normal to Dry Skin 52ml",
  "brand": "Cerave",
  "price": 11.62,
  "currency": "GBP",
  "was_price": 15.5,
  "saving": 3.88,
  "size": "52 ML",
  "unit_price": 223.46,
  "unit_price_per": "1L",
  "unit_price_text": "52 ML | £223.46 per 1L",
  "item_number": "5728371",
  "part_number": "10331199.P",
  "catentry_id": "2857120",
  "online_in_stock": true,
  "image": "https://boots.scene7.com/is/image/Boots/10331199?id=-Klmv1&fmt=jpg&wid=300&hei=300",
  "has_variants": false,
  "variants": [{"name": "", "item_code": "10331199", "catentry_id": "2857121", "online_in_stock": null}],
  "offers": [
    {"text": "Save up to 30 percent on selected cerave products - online only", "code": null},
    {"text": "Was £17, Was £15.50, Now £11.62", "code": null},
    {"text": "Use code SAVE20 to save 20 percent on selected Skincare and Haircare - online only", "code": "SAVE20"}
  ],
  "advantage_card_offers": [
    "My Offers: Double Advantage Card points when you buy selected Cerave",
    "My Offers: 300 Advantage Card points when you spend £30 on selected Skincare",
    "My Offers: 12 Advantage Card points per £1 when you buy selected Cerave"
  ]
}
```

The same id on boots.ie (`{"product_id": "10331199", "market": "ie"}`, 19 seconds by id) read 13.50 EUR, was 18, save 4.50, "0.052 L | €259.62 per 1L", with the same item number and the SAVE20 line.

### A product with shades

```bash
curl -X POST https://api.scavio.dev/api/v1/boots/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "10213975"}'
```

Captured (2026-11-26): Maybelline Fit Me Matte & Poreless Liquid Foundation 30ml, 9.99 GBP, `was_price` null, `catentry_id` 1838584, `has_variants` true and 23 shades in `variants`, each with its own `item_code` (Mocha 10213975007, Ivory 10213975001, Natural Beige 10213975002 ...) and `online_in_stock`; `offers` "Free gift when you spend £20 on selected Cosmetics - whilst stocks last".

### Which stores near a postcode have one shade

```bash
curl -X POST https://api.scavio.dev/api/v1/boots/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_code": "10213975001", "catentry_id": "1838584", "postcode": "NG2 3AA"}'
```

Captured `data` (2026-11-26; `stores` cut to 2 of 45, `hours` to 2 of 7 days, `pharmacy_hours` and `special_hours` dropped):

```json
{
  "market": "uk",
  "item_code": "10213975001",
  "catentry_id": "1838584",
  "postcode": "NG2 3AA",
  "count": 45,
  "in_stock_count": 43,
  "stores_searched": 45,
  "message": null,
  "stores": [
    {"name": "Nottingham Beeston", "address": {"lines": ["31 High Road"], "town": "Nottingham", "county": "Nottinghamshire", "postcode": "NG9 2JQ"}, "phone": "01159254464", "phone_international": "+441159254464", "latitude": 52.92763754725456, "longitude": -1.2147094309329987, "distance_miles": 0.7, "availability": "in_stock", "availability_text": "In Stock", "in_stock": true, "stockist": true, "hours": [{"day": "monday", "open": "08:30", "close": "17:30", "closed": false}, {"day": "sunday", "open": "10:30", "close": "16:30", "closed": false}]},
    {"name": "Nottingham Victoria Centre", "address": {"lines": ["11-19 Lower Parliament Street"], "town": "Nottingham", "county": "Nottinghamshire", "postcode": "NG1 3QS"}, "phone": "01159410199", "phone_international": "+441159410199", "latitude": 52.95554352, "longitude": -1.14658475, "distance_miles": 2.78, "availability": "out_of_stock", "availability_text": "Out of Stock", "in_stock": false, "stockist": true, "hours": [{"day": "monday", "open": "09:00", "close": "19:00", "closed": false}]}
  ]
}
```

When no store nearby has it: Maybelline Superstay 30hr Foundation 30ml in Cameo (`item_code` 10289565007) near M1 1AE (Manchester) returned `count` 0, `stores_searched` 123 and Boots' `message` "This product isn't currently available in the area you have searched. Please try another area." (charged, 1 credit).

### Stores and one store

- `/stores` `{"postcode": "M1 1AE"}`: 55 stores, nearest first, Manchester Piccadilly (`store_number` 1108, 0.27 miles), Manchester Piccadilly Station (1125, 0.46 miles), Manchester Market Street (1200, 0.48 miles), each with `address`, `latitude`, `longitude` and `services` [{`id`, `name`, `category`}]; `latitude` 53.48348618 and `longitude` -2.23118186 for the postcode.
- `/stores` `{"city": "Cork", "market": "ie"}`: 9 stores, first Cork Patrick Street (0.07 miles); the town's `latitude` 51.89851379 and `longitude` -8.47264194 are the input of `/store-stock` on ie.
- `/store` `{"store_number": "868"}`: London Battersea, 21-23 St. John's Rd, London SW11 1QN, `phone` 02072286064, `hours` Monday-Saturday 09:00-19:00, Sunday 11:00-18:00, `services` [{`category`, `name`}] (Hearing loop or induction loop, Instant Photo Kiosk ...).
- `/store` `{"name": "Cork Patrick Street", "market": "ie"}`: store slug cork-boots-patrick-street, `store_number` 1764, 71-72 Patrick Street, T12 KDC0, Monday 08:30-18:00, Sunday 12:00-18:00.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def boots(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/boots/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# The same product on boots.com and boots.ie (1 credit each)
for market in ["uk", "ie"]:
    p = boots("product", {"product_id": "10331199", "market": market})["data"]
    print(market, p["currency"], p["price"], p["was_price"], p["saving"], [o["code"] for o in p["offers"] if o["code"]])

# One shade at the stores near a postcode (1 credit)
p = boots("product", {"product_id": "10213975"})["data"]
ivory = next(v for v in p["variants"] if v["name"] == "Ivory")
s = boots("store-stock", {"item_code": ivory["item_code"], "catentry_id": p["catentry_id"], "postcode": "NG2 3AA"})["data"]
print(s["in_stock_count"], "of", s["stores_searched"], "stores in stock")
for st in s["stores"][:5]:
    print(st["name"], st["distance_miles"], st["availability_text"])  # in or out, no unit counts

# Store each answer with fetched_at: that stored set is your record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market`.

- **product** - `market`, `product_id`, `requested_id`, `url`, `name`, `brand`, `price`, `currency`, `was_price`, `saving`, `size`, `unit_price`, `unit_price_per`, `unit_price_text`, `item_number`, `part_number`, `catentry_id`, `online_in_stock`, `image`, `has_variants`, `variants[]` {`name`, `item_code`, `catentry_id`, `online_in_stock`}, `offers[]` {`text`, `code`}, `advantage_card_offers`, `description`, `sections[]` {`title`, `text`}, `ingredients`.
- **store-stock** - `market`, `item_code`, `catentry_id`, `postcode` or `latitude` / `longitude`, `count`, `in_stock_count`, `stores_searched`, `message`, `stores[]` {`name`, `address` {`lines`, `town`, `county`, `postcode`}, `phone`, `phone_international`, `latitude`, `longitude`, `distance_miles`, `availability`, `availability_text`, `in_stock`, `stockist`, `hours[]` {`day`, `open`, `close`, `closed`}, `pharmacy_hours`, `special_hours[]` {`date`, `reason`, `open`, `close`, `closed`, `pharmacy_open`, `pharmacy_close`}}; `towns[]` {`name`, `county`, `latitude`, `longitude`} when Boots matched several places.
- **stores** - `market`, `postcode` or `city`, `latitude`, `longitude`, `count`, `message`, `stores[]` {`store_number`, `store_id`, `name`, `address` {`lines`, `town`, `county`, `postcode`}, `latitude`, `longitude`, `distance_miles`, `services[]` {`id`, `name`, `category`}}.
- **store** - `market`, `store` (the page slug), `store_number`, `url`, `name`, `address`, `phone`, `phone_international`, `latitude`, `longitude`, `hours[]`, `pharmacy_hours`, `services[]` {`category`, `name`}.

## Guardrails

- Name it "Boots (boots.com, the UK health and beauty retailer with over 1,800 stores, and boots.ie in Ireland)" on first mention, "Boots" after that, and name the site (boots.com or boots.ie) for every price.
- Prices: quote each with GBP or EUR, the site and the `fetched_at` date ("listed on boots.com on Nov 26, 2026"). `was_price` and `saving` are "as Boots shows them"; a percent off is computed and labelled so; a price after a promo code is your own arithmetic, labelled computed and not checked out.
- Stock: report each store's `availability_text` with the store's name, distance and the capture time; never a unit count, and never "in stock everywhere". An empty `stores` with Boots' message means none of the stores it checked near that place had the item, as Boots says.
- Offers: quote offer lines, codes and Advantage Card offers exactly as Boots writes them, with the capture date. No countdowns or urgency.
- Descriptive only: report product facts as Boots labels them; no efficacy, skin or health claims, no advice on what to buy or use, and no commentary on Boots' business, ownership or pricing practices. Use this skill for beauty, skincare, make-up and toiletry products.
- Stores: store names, addresses, phone numbers and hours are public business data; no staff names are returned.
- Do not republish Boots product photos or descriptions at length; cite product names, ids and capture dates, and write boots.com as plain text.
- Terms: Scavio does not collect or store Boots data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account, no basket and no checkout. Boots' terms and conditions cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, was prices, savings, codes, offers, item codes, stores or stock. Only return what the API returned, with the `fetched_at` time.
- Not available: search, category, brand and deal lists, reviews and ratings, type-ahead, stock counts, EAN, a price per shade or size, price history (store your own), basket or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: product with both `url` and `product_id` or neither ("send one of url (a Boots product link) or product_id (8 digits)."); a link that is not a Boots product link; a `product_id` that is not the 8 digits a link ends with; a `market` other than `uk` or `ie`, or one that does not match the link's site; store-stock without `item_code` or `catentry_id`, an `item_code` that is not 11 digits or an 8-digit id, both a postcode and a point or neither, only one of `latitude` and `longitude`, or a postcode on ie ("boots.ie answers a postcode or place name with a list of towns: send latitude and longitude (stores returns them for a town, e.g. city Dublin)."); a postcode that is not a full UK postcode; stores with both `postcode` and `city` or neither, or a postcode on ie ("boots.ie stores are found by town: send city (e.g. Dublin, Cork)."); store with more or fewer than one of `store`, `store_number` and `name`, or `store_number` on ie ("boots.ie store pages are not numbered: send name (stores[].name, e.g. Cork Patrick Street) or store.").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Boots product at this link (or it is not sold on this market's site).", "Boots' product list has no product <id>. Send its link (url) instead.", "No Boots store <number> on Boots' store list.", "No Boots store named "<name>" on Boots' store list (names as stores[].name gives them).", "Several Boots stores are named "<name>": send store_number instead.", "No Boots store page with this reference.". Take ids, item codes and store numbers from a previous answer rather than guessing them.
- `/store-stock` with `count` 0 and Boots' message is a charged `200`: no store near the place had the item, or the item code is not one Boots knows. With `towns[]` and the message "Boots matched several places: send the latitude and longitude of one of the towns.", send one town's point.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=boots-uk-api).
- `502` means Boots data was temporarily unavailable ("Boots is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Boots is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.96.0
npm install scavio@0.97.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: product } = await scavio.boots.product({ url: "https://www.boots.com/cerave-am-facial-moisturising-lotion-spf30-52ml-10331199" });
const { data: ie } = await scavio.boots.product({ product_id: "10331199", market: "ie" });
const { data: stock } = await scavio.boots.storeStock({ item_code: "10213975001", catentry_id: "1838584", postcode: "NG2 3AA" });
const { data: stores } = await scavio.boots.stores({ city: "Cork", market: "ie" });
const { data: store } = await scavio.boots.store({ store_number: "868" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.boots.product(...)`, `store_stock`, `stores` and `store`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 4 endpoints as tools: `get_boots_product`, `get_boots_store_stock`, `get_boots_stores` and `get_boots_store`. Boots is opt-in: add `boots` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,boots"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [product](https://scavio.dev/docs/boots-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=boots-uk-api), [store stock](https://scavio.dev/docs/boots-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=boots-uk-api), [stores](https://scavio.dev/docs/boots-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=boots-uk-api), [store](https://scavio.dev/docs/boots-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=boots-uk-api). Platform page: [scavio.dev/boots-api](https://scavio.dev/boots-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=boots-uk-api).
