# Sybill → SPICED AI

Sybill.ai produces structured call summaries + full transcripts with speaker sentiment. Two ingestion modes.

## Mode A - Raw transcript (preferred)

Use Sybill's transcript export and normalize into spiced-ai input. Sybill returns transcript with sentiment per utterance (valuable for Engagement scoring).

### API

- **Docs:** https://sybill.ai/api (request access)
- **Auth:** API key in `X-API-Key` header
- **Endpoint:** `https://api.sybill.ai/v1/calls/{call_id}/transcript`

### Adapter

```python
def fetch_sybill(call_id: str) -> dict:
    r = requests.get(
        f"https://api.sybill.ai/v1/calls/{call_id}/transcript",
        headers={"X-API-Key": os.environ["SYBILL_API_KEY"]},
    )
    r.raise_for_status()
    t = r.json()

    return {
        "transcript": {
            "source": "sybill",
            "source_url": t.get("call_url"),
            "recorded_at": t["started_at"],
            "duration_sec": t["duration_sec"],
            "utterances": [
                {
                    "speaker": u["speaker_name"],
                    "role": "rep" if u["is_internal"] else "prospect",
                    "text": u["text"],
                    "timestamp_sec": u["timestamp_sec"],
                    "sentiment": u.get("sentiment"),  # positive|neutral|negative
                }
                for u in t["utterances"]
            ],
        }
    }
```

## Mode B - Sybill's own summary as input

Sybill already produces call summaries. If you want spiced-ai to build *on top* of that summary (rather than re-transcribe), pass the summary as a single "prospect said" utterance:

```python
# Quick-and-dirty: feed summary as pseudo-transcript
{
  "transcript": {
    "source": "sybill",
    "utterances": [{"speaker": "Summary", "role": "unknown", "text": sybill_summary}]
  }
}
```

This is lower-fidelity - the scoring rubric can't cite quotes. Prefer Mode A.

## Known gotchas

- Sybill sometimes mis-labels internal vs external speakers on calls with non-employee attendees. Verify `is_internal` against your known employee list.
- Sentiment scores are directional, not precise. Use for corroboration, not as primary evidence.
