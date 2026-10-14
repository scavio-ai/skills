---
name: chatgpt-scraper-api
description: "ChatGPT scraper API for AI visibility: send a prompt, get the answer ChatGPT gives as JSON with every cited page (title, publisher, date), the web searches it ran and the products it recommended. Track brand mentions and citations in ChatGPT. 1 endpoint, 1 credit per answered prompt."
version: 1.0.0
tags: chatgpt, chatgpt-scraper, chatgpt-api, ai-visibility, geo, generative-engine-optimization, brand-monitoring, llm-citations, answer-engine, share-of-voice, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F4AC"
    homepage: https://scavio.dev/docs/chatgpt-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=chatgpt-scraper-api
---

# ChatGPT Scraper API - Answers, Citations, AI Visibility

Send a prompt to ChatGPT and get back what ChatGPT tells the people asking it: the full answer as Markdown, every page it cites (title, publisher, publish date), the web searches it ran to answer, and the products it recommended. One endpoint, 1 credit per answered prompt; failed prompts are free.

## When to trigger

Use this skill when the user asks to:
- See what ChatGPT says or recommends for a question, product category or brand
- Check whether a brand, product or website is mentioned or cited in ChatGPT's answer
- Find which pages and publishers ChatGPT cites for a topic (citation / source analysis)
- Track AI visibility or share of voice in ChatGPT across a list of prompts
- See what web searches ChatGPT runs to answer a prompt (query fan-out)
- Compare ChatGPT's answer with Gemini's (use the `gemini-scraper-api` skill for the other half)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=chatgpt-scraper-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=chatgpt-scraper-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits, enough for 50 prompts on this endpoint.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

## Endpoint

```
POST https://api.scavio.dev/api/v1/chatgpt/prompt
Authorization: Bearer $SCAVIO_API_KEY
```

Every answered prompt costs 1 credit. Answers typically take 10-40 seconds: use an HTTP timeout of at least 90 seconds.

## Workflow

1. Send the question the way a buyer would type it as `prompt`.
2. Add `country` when the answer should be localized (2-letter code).
3. Read `data.answer.markdown` for the answer, `data.sources[]` for the pages it cited, `data.search_queries[]` for the searches it ran and `data.shopping[]` for the products it recommended.
4. For visibility tracking, run each prompt several times: answers vary between runs, so report a mention rate, not a single yes or no.

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `prompt` | string | required | The prompt, 1-1024 characters |
| `model` | string | `auto` | Model id; `auto` is the model ChatGPT picks by default |
| `country` | string | `us` | 2-letter country code the answer is localized for |
| `include_html` | boolean | `false` | Also return the answer as HTML in `answer.html` |

## Example

```python
import requests

# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"

response = requests.post(
    "https://api.scavio.dev/api/v1/chatgpt/prompt",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"prompt": "What are the best running shoes for beginners?"},
    timeout=120,
)
data = response.json()["data"]
print(data["answer"]["markdown"][:800])
print("Brooks mentioned:", "Brooks" in data["answer"]["markdown"])
for s in data["sources"]:
    print("cited:", s["source"], s["url"])
print("searched:", data["search_queries"])
print("recommended:", [p["title"] for p in data["shopping"]])
```

## Response

```json
{
  "data": {
    "platform": "chatgpt",
    "prompt": "What are the best running shoes for beginners?",
    "model": "gpt-6",
    "answer": {
      "markdown": "The best running shoes for beginners are usually **comfortable, well-fitting daily trainers**... ## 1\\. Brooks Ghost 18 ..."
    },
    "sources": [
      {
        "url": "https://www.rtings.com/running-shoes/reviews/best/beginners",
        "title": "The 6 Best Running Shoes for Beginners of 2026",
        "snippet": null,
        "source": "RTINGS.com",
        "published_at": "2026-09-18T00:00:00.000Z"
      }
    ],
    "search_queries": [
      "best running shoes for beginners 2026 review Brooks Ghost ASICS Nimbus Saucony Ride Nike Pegasus"
    ],
    "shopping": [
      { "title": "Brooks Ghost 18", "url": null, "price": null, "image_url": null, "merchant": null }
    ]
  },
  "response_time": 28081,
  "credits_used": 1,
  "credits_remaining": 49
}
```

`shopping[]` is often title only; `url`, `price` and `image_url` are filled when ChatGPT shows them.

## Guardrails

- Each answered prompt costs 1 credit. Confirm before running large prompt lists.
- Never fabricate or paraphrase the answer as if it were ChatGPT's words. Quote `answer.markdown` and surface `sources` so the user can verify.
- Answers vary between runs and are never cached. Do not present one run as ChatGPT's fixed opinion.
- Prompts are limited to 1024 characters.

## Failure handling

- `400` means a missing or too-long prompt, or a malformed `country` / `model` - fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=chatgpt-scraper-api).
- `502` means ChatGPT did not return an answer. Retry once; it is not charged.
- `503` means answer capacity is busy. Wait for the `Retry-After` header, then retry; it is not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
