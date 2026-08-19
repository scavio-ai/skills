---
name: google-ai-mode-api
description: "Google AI Mode answers as structured JSON: the AI-generated response split into text blocks, the cited source references behind it, and shopping results on commercial queries. Localize by country and language. One endpoint on the v2 engine, 1 credit per request."
version: 1.0.0
tags: google-ai-mode, google-ai-mode-api, ai-overview, generative-search, answer-engine, aeo, citations, seo, google-search, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U00002728"
    homepage: https://scavio.dev/docs/google-ai-mode?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-ai-mode-api
---

# Google AI Mode API - AI Answers with Cited Sources

Fetch Google's AI Mode answer as structured JSON: an AI-generated response broken into text blocks, the cited source references behind it, and shopping results for commercial queries. One credit per request.

## When to trigger

Use this skill when the user asks to:
- Get Google's AI-generated answer to a question, with its sources
- See what Google's AI Mode says about a topic or product
- Pull cited references behind an AI answer for grounding or verification
- Answer a commercial query and surface AI-suggested products

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-ai-mode-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

## Endpoint

```
POST https://api.scavio.dev/api/v2/google/ai-mode
Authorization: Bearer $SCAVIO_API_KEY
```

Every request costs 1 credit.

## Workflow

1. Send the user's question as `query`.
2. Localize with `gl`/`hl`/`location` when the answer is region-specific.
3. Read `text_blocks[]` for the AI answer, `references[]` for the cited sources, and `shopping_results[]` for product suggestions on commercial queries.

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search query (1-500 chars) |
| `device` | string | `desktop` | `desktop` or `mobile` |
| `hl` | string | -- | UI language, ISO 639-1 |
| `gl` | string | -- | Geo country, ISO 3166-1 alpha-2 |
| `google_domain` | string | `google.com` | Regional Google domain |
| `location` | string | -- | Canonical location name (auto-UULE) |
| `uule` | string | -- | Pre-encoded UULE (takes priority over `location`) |
| `safe` | string | -- | `active` filters adult content |
| `include_html` | boolean | `false` | Include raw HTML in the `html` field |

## Example

```python
import requests

# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"

response = requests.post(
    "https://api.scavio.dev/api/v2/google/ai-mode",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"query": "best running shoes for flat feet 2026", "gl": "us", "hl": "en"},
)
data = response.json()
for b in data.get("text_blocks", []):
    print(b.get("snippet") or b.get("text"))
for ref in data.get("references", []):
    print("source:", ref.get("title"), ref.get("link"))
```

## Response

```json
{
  "text_blocks": [
    { "type": "paragraph", "snippet": "AI-generated answer text..." }
  ],
  "references": [
    { "title": "Source article", "link": "https://example.com", "source": "Example" }
  ],
  "shopping_results": [],
  "response_time": 2140,
  "credits_used": 1,
  "credits_remaining": 995,
  "cached": false
}
```

## Guardrails

- Each call costs 1 credit.
- Never fabricate the AI answer, references, or products. Only return API data.
- Present the answer from `text_blocks` and always surface its `references` so the user can verify sources.
- AI Mode does not support pagination or result filtering — it is a single answer per query.

## Failure handling

- `400` means an invalid parameter — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-ai-mode-api).
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If no AI answer is returned, the query may not trigger AI Mode — fall back to the `scavio-google` search skill.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
