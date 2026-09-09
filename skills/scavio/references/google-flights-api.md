# Google Flights API - Route Search, Prices, Carriers, Stops

Search Google Flights for a route and date and return structured JSON — price, airline, duration, stops, and per-leg details. One credit per request.

## When to trigger

Use this skill when the user asks to:
- Find flights between two airports on given dates
- Compare airfares, airlines, durations, or number of stops
- Plan round-trip, one-way, or multi-city itineraries
- Filter flights by cabin class, stops, or specific airlines

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-flights-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-flights-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Endpoints in this skill cost 1 credit each unless the table below says otherwise.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

## Endpoint

```
POST https://api.scavio.dev/api/v2/google/flights
Authorization: Bearer $SCAVIO_API_KEY
```

Every request costs 1 credit.

## Workflow

1. Provide `departure_id` and `arrival_id` (IATA codes) and an `outbound_date` (`YYYY-MM-DD`).
2. For a round trip (`type: 1`, the default) also pass `return_date`. Use `type: 2` for one-way, `type: 3` for multi-city.
3. Refine with `travel_class`, `stops`, `adults`, `sort_by`, and airline filters.
4. Read `best_flights[]` and `other_flights[]`; each itinerary lists its `flights` legs, `price`, `total_duration`, and airline.

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `departure_id` | string | required | Origin IATA (comma-separated allowed, e.g. `JFK`) |
| `arrival_id` | string | required | Destination IATA (e.g. `LAX`) |
| `outbound_date` | string | required | Departure date `YYYY-MM-DD` |
| `type` | number | `1` | `1` round trip, `2` one way, `3` multi-city |
| `return_date` | string | -- | Required when `type=1` |
| `adults` | number | `1` | Adult passengers (1-9) |
| `children` | number | -- | Children (0-9) |
| `infants_in_seat` | number | -- | Infants in seat (0-4) |
| `infants_on_lap` | number | -- | Lap infants (0-4) |
| `travel_class` | number | -- | `1` economy, `2` premium, `3` business, `4` first |
| `stops` | number | -- | `0` any, `1` nonstop, `2` <=1 stop, `3` <=2 stops |
| `sort_by` | number | -- | `1` top, `2` price, `3` departure, `4` arrival, `5` duration, `6` emissions |
| `include_airlines` | string | -- | Restrict to these airlines |
| `exclude_airlines` | string | -- | Exclude these airlines |
| `hl` | string | -- | UI language |
| `gl` | string | -- | Geo country |
| `currency` | string | -- | Currency code (e.g. `USD`) |

## Example

```python
import requests

# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"

response = requests.post(
    "https://api.scavio.dev/api/v2/google/flights",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "departure_id": "JFK",
        "arrival_id": "LAX",
        "outbound_date": "2026-09-10",
        "return_date": "2026-09-17",
        "type": 1,
        "travel_class": 1,
        "stops": 1,
        "sort_by": 2,
        "currency": "USD",
    },
)
data = response.json()
for f in data.get("best_flights", []):
    legs = f["flights"]
    print(f["price"], f["total_duration"], "min",
          legs[0]["airline"], legs[0]["departure_airport"]["id"], "->",
          legs[-1]["arrival_airport"]["id"])
```

## Response

```json
{
  "best_flights": [
    {
      "flights": [
        {
          "departure_airport": { "id": "JFK", "time": "2026-09-10 08:00" },
          "arrival_airport": { "id": "LAX", "time": "2026-09-10 11:25" },
          "airline": "Example Air",
          "flight_number": "EA 123",
          "duration": 385
        }
      ],
      "total_duration": 385,
      "price": 342,
      "type": "Round trip"
    }
  ],
  "other_flights": [],
  "response_time": 1980,
  "credits_used": 1,
  "credits_remaining": 994,
  "cached": false
}
```

## Guardrails

- Each call costs 1 credit.
- Never fabricate prices, airlines, times, or durations. Only return API data.
- `departure_id` and `arrival_id` must be IATA codes; `outbound_date` is `YYYY-MM-DD`.
- A round trip (`type=1`) requires `return_date`.
- Prices reflect the requested `currency`; state the currency when quoting fares.

## Failure handling

- `400` means an invalid parameter (e.g. round trip without `return_date`, bad IATA/date) — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-flights-api).
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If no flights are returned, relax `stops`, airline filters, or try nearby dates.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
