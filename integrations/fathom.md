# Fathom → SPICED AI

Fathom is the lightest-weight option. Free tier is generous. API is REST-simple.

## API basics

- **Docs:** https://help.fathom.ai/en/articles/api
- **Auth:** API key in `Authorization: Bearer {key}`
- **Endpoint:** `https://api.fathom.video/external/v1`

## Fetch a meeting

```python
import requests
import os

def fetch_fathom(meeting_id: str) -> dict:
    r = requests.get(
        f"https://api.fathom.video/external/v1/meetings/{meeting_id}",
        headers={"Authorization": f"Bearer {os.environ['FATHOM_API_KEY']}"},
    )
    r.raise_for_status()
    m = r.json()

    internal_emails = set(os.environ.get("INTERNAL_EMAILS", "").split(","))

    return {
        "transcript": {
            "source": "fathom",
            "source_url": m.get("share_url"),
            "recorded_at": m["scheduled_start_time"],
            "duration_sec": m["duration_in_minutes"] * 60,
            "utterances": [
                {
                    "speaker": u["speaker_name"],
                    "role": "rep" if u.get("speaker_email") in internal_emails else "prospect",
                    "text": u["text"],
                    "timestamp_sec": u["start_time_in_seconds"],
                }
                for u in m["transcript"]
            ],
        }
    }
```

## Webhook

Fathom supports webhooks via Zapier and native. Recommend native webhook on `meeting.completed`. Payload includes `meeting_id`; fetch + normalize + analyze.

## Known gotchas

- Fathom attaches emails to attendees but not always to each utterance. If `speaker_email` is missing, fall back to name matching against internal list.
- Free tier rate limit is 100 req/day. Paid is 1000+.
