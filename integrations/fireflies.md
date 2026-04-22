# Fireflies → SPICED AI

Fireflies.ai transcript → normalized input format.

## API basics

- **Docs:** https://docs.fireflies.ai/graphql-api/introduction
- **Auth:** API key in `Authorization: Bearer {key}` header
- **Endpoint:** `https://api.fireflies.ai/graphql`

## Minimal GraphQL query

```graphql
query GetTranscript($id: String!) {
  transcript(id: $id) {
    id
    title
    date
    duration
    participants
    sentences {
      index
      speaker_name
      text
      start_time
      end_time
    }
    meeting_attendees {
      displayName
      email
    }
  }
}
```

## Adapter (Python)

```python
import requests
import os

def fetch_fireflies(transcript_id: str) -> dict:
    """Fetch Fireflies transcript and return spiced-ai normalized input."""
    query = """
    query GetTranscript($id: String!) {
      transcript(id: $id) {
        id title date duration
        sentences { speaker_name text start_time }
        meeting_attendees { displayName email }
      }
    }
    """
    r = requests.post(
        "https://api.fireflies.ai/graphql",
        headers={
            "Authorization": f"Bearer {os.environ['FIREFLIES_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={"query": query, "variables": {"id": transcript_id}},
    )
    r.raise_for_status()
    t = r.json()["data"]["transcript"]

    # Identify rep side via config (list of internal email domains)
    internal_domains = {"yourcompany.com"}
    rep_names = {
        a["displayName"] for a in t["meeting_attendees"]
        if any(d in (a.get("email") or "") for d in internal_domains)
    }

    return {
        "transcript": {
            "source": "fireflies",
            "source_url": f"https://app.fireflies.ai/view/{t['id']}",
            "recorded_at": t["date"],
            "duration_sec": int(t["duration"]),
            "utterances": [
                {
                    "speaker": s["speaker_name"],
                    "role": "rep" if s["speaker_name"] in rep_names else "prospect",
                    "text": s["text"],
                    "timestamp_sec": s["start_time"],
                }
                for s in t["sentences"]
            ],
        }
    }
```

## Webhook (auto-ingest on new call)

Fireflies supports webhooks on `transcription_complete`. Register your endpoint in Settings → Integrations → Webhooks. The payload includes `transcript_id`; your endpoint fetches via the query above, normalizes, runs SPICED analysis, and posts results where configured.

## Known gotchas

- Speaker diarization is imperfect on conference lines. If `speaker_name = "Unknown"` dominates, ask the user to add manual corrections in Fireflies before analysis.
- `start_time` is in seconds (float). `end_time` is usually not populated - don't rely on it.
- Rate limit: 60 requests/min on free plan, higher on paid.
