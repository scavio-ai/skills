# Google Search API - Organic SERP, Knowledge Graph, PAA, AI Overview

Search Google and return the full structured SERP as JSON — no HTML parsing required. One call returns organic results, ads, knowledge graph, AI overview, related questions, related searches, top stories, videos, and pagination.

## When to trigger

Use this skill when the user asks to:
- Look something up on the web or check a current fact
- Find recent results or events
- Answer any question that requires real-time or up-to-date information
- Pull Google's knowledge graph, AI overview, or "people also ask" for a query

Do not answer from memory when current information is needed. Search first.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-search-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-search-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Endpoints in this skill cost 1 credit each unless the table below says otherwise.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

## Endpoint

```
POST https://api.scavio.dev/api/v2/google
Authorization: Bearer $SCAVIO_API_KEY
```

Every request costs 1 credit.

## Workflow

1. Send the user's query as `query`. Add `gl`/`hl` to localize by country and language.
2. Page with `start` (0 = page 1, 10 = page 2, 20 = page 3, ...).
3. Narrow recency with `time_period` when the user wants fresh results.
4. Read `organic_results` for the main links; check `ai_overview`, `knowledge_graph`, and `related_questions` for richer answers.
5. Return results in a clear, structured response. Cite URLs.

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search query (1-500 chars) |
| `device` | string | `desktop` | `desktop` or `mobile` (SERP layout) |
| `start` | number | `0` | Result offset: 0 = page 1, 10 = page 2, ... (max 990) |
| `gl` | string | -- | Geo country, ISO 3166-1 alpha-2 (e.g. `us`, `gb`, `de`) |
| `hl` | string | -- | UI language, ISO 639-1 (e.g. `en`, `fr`, `es`) |
| `google_domain` | string | `google.com` | Regional Google domain |
| `location` | string | -- | Canonical location name, auto-UULE (e.g. `New York,New York,United States`) |
| `uule` | string | -- | Pre-encoded UULE (takes priority over `location`) |
| `lr` | string | -- | Language restrict (`lang_en`) |
| `cr` | string | -- | Country restrict (`countryUS`) |
| `safe` | string | -- | `active` filters adult content (SafeSearch) |
| `nfpr` | boolean | `false` | Set `true` to disable spelling autocorrection |
| `filter` | string | `1` | `0` disables similar/omitted-results filtering |
| `time_period` | string | -- | `last_hour`, `last_day`, `last_week`, `last_month`, `last_year` |
| `resolve_ai_overview` | boolean | `true` | Inline the full AI Overview when Google defers it; set `false` to skip the extra upstream call |
| `include_html` | boolean | `false` | Include raw Google HTML in the `html` field |

## Example

```python
import requests

# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"

response = requests.post(
    "https://api.scavio.dev/api/v2/google",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"query": "langchain agents tutorial", "gl": "us", "hl": "en"},
)
data = response.json()
for r in data["organic_results"]:
    print(r["position"], r["title"], r["link"])
```

## Response

```json
{
  "search_information": {
    "page_title": "langchain agents tutorial - Google Search",
    "organic_results_state": "Results for exact spelling"
  },
  "organic_results": [
    {
      "position": 1,
      "title": "Result title",
      "link": "https://example.com",
      "displayed_link": "https://example.com › docs",
      "snippet": "Snippet text..."
    }
  ],
  "related_questions": [],
  "related_searches": [],
  "response_time": 812,
  "credits_used": 1,
  "credits_remaining": 999,
  "cached": false
}
```

The response is a faithful passthrough of the SERP. Depending on the query it may also include: `ai_overview`, `knowledge_graph`, `top_ads`, `bottom_ads`, `top_stories`, `video_results`, `discussions_and_forums`, `local_results`, `local_map`, and `pagination`.

## Guardrails

- Never fabricate search results or URLs. Only return what the API gives you.
- If the query is time-sensitive, always call the API — do not answer from training data.
- Organic links live in `organic_results[].link` and result order is `position`.
- Cite sources when summarizing results.

## Failure handling

- `400` means an invalid parameter — report the message and fix the request.
- `401` means the API key is invalid or missing. Prompt the user to check their `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-search-api).
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If no results are returned, tell the user and suggest rephrasing.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## LangChain

```bash
pip install langchain-scavio==4.0.2
```

```python
from langchain_scavio import ScavioSearchTool
tool = ScavioSearchTool(engine="google")
```
