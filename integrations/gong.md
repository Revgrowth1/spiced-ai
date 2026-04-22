# Gong → SPICED AI

Gong is the enterprise-grade option. Their API is rich but paywalled behind Gong Enterprise.

## API basics

- **Docs:** https://app.gong.io/settings/api/documentation
- **Auth:** Basic auth (access key + secret) or OAuth
- **Endpoint:** `https://api.gong.io/v2`

## Fetch a call transcript

```python
import base64
import requests
import os

def fetch_gong(call_id: str) -> dict:
    key = os.environ["GONG_ACCESS_KEY"]
    secret = os.environ["GONG_ACCESS_KEY_SECRET"]
    auth = base64.b64encode(f"{key}:{secret}".encode()).decode()

    # Step 1: call metadata
    meta = requests.get(
        f"https://api.gong.io/v2/calls/{call_id}",
        headers={"Authorization": f"Basic {auth}"},
    ).json()["call"]

    # Step 2: transcript (separate endpoint)
    tx = requests.post(
        "https://api.gong.io/v2/calls/transcript",
        headers={"Authorization": f"Basic {auth}"},
        json={"filter": {"callIds": [call_id]}},
    ).json()["callTranscripts"][0]

    # Map participants → rep/prospect
    internal_user_ids = {p["userId"] for p in meta["parties"] if p["affiliation"] == "Internal"}

    return {
        "transcript": {
            "source": "gong",
            "source_url": meta.get("url"),
            "recorded_at": meta["started"],
            "duration_sec": meta["duration"],
            "utterances": [
                {
                    "speaker": s["speakerId"],
                    "role": "rep" if s["speakerId"] in internal_user_ids else "prospect",
                    "text": " ".join(sent["text"] for sent in s["sentences"]),
                    "timestamp_sec": s["sentences"][0]["start"] / 1000 if s["sentences"] else 0,
                }
                for s in tx["transcript"]
            ],
        }
    }
```

## Known gotchas

- Gong transcripts use `speakerId` (GUID), not speaker name. Join with `/v2/users` to get display names.
- `start` is in milliseconds (not seconds). Divide by 1000.
- `affiliation` is `Internal` / `External` / `Unknown`. Treat `Unknown` as prospect by default.
- Rate limit: 3 requests/second. Batch where possible.
- Gong's own "Trackers" and "Topics" output is valuable context - consider passing as `email_signals` or `prior_analyses`.
