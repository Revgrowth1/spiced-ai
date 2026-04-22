# SPICED AI → HubSpot

Writes post-call analysis to the HubSpot deal record. Two surfaces: deal properties and an engagement note.

## What goes where

| Output field | HubSpot destination |
|---|---|
| `probability.final` (normalized to %) | Deal property: `hs_deal_stage_probability` (native) |
| `probability.stage` | Deal property: `custom_spiced_stage` (custom) |
| `probability.math_display` | Deal property: `custom_spiced_score_detail` (custom) |
| `spiced.*` summaries | Engagement: Note |
| `next_actions` | HubSpot tasks (one per action) |
| `risks` | Engagement: Note (ranked) |
| `red_flags` (CRITICAL/HIGH only) | Deal property: `custom_red_flags` + Slack alert |

## Setup (one-time)

Create these custom deal properties in HubSpot:

```
custom_spiced_stage             single-line text
custom_spiced_score_detail      single-line text
custom_spiced_probability       number (0–1)
custom_red_flags                multi-line text
custom_last_spiced_analysis_at  date
```

## Write adapter (Python)

```python
import requests
import os
from datetime import datetime

HUBSPOT_BASE = "https://api.hubapi.com"
HEADERS = {
    "Authorization": f"Bearer {os.environ['HUBSPOT_PRIVATE_APP_TOKEN']}",
    "Content-Type": "application/json",
}

def push_to_hubspot(deal_id: str, analysis: dict) -> None:
    pc = analysis["post_call"]

    # 1. Update deal properties
    requests.patch(
        f"{HUBSPOT_BASE}/crm/v3/objects/deals/{deal_id}",
        headers=HEADERS,
        json={
            "properties": {
                "custom_spiced_stage": pc["probability"]["stage"],
                "custom_spiced_score_detail": pc["probability"]["math_display"],
                "custom_spiced_probability": pc["probability"]["final"] / 18,  # normalize to 0-1
                "custom_last_spiced_analysis_at": datetime.utcnow().isoformat(),
            }
        },
    )

    # 2. Create note engagement
    note_body = _render_note(pc)
    requests.post(
        f"{HUBSPOT_BASE}/crm/v3/objects/notes",
        headers=HEADERS,
        json={
            "properties": {
                "hs_note_body": note_body,
                "hs_timestamp": int(datetime.utcnow().timestamp() * 1000),
            },
            "associations": [
                {"to": {"id": deal_id}, "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 214}]}
            ],
        },
    )

    # 3. Create tasks from next_actions
    for action in pc.get("next_actions", []):
        requests.post(
            f"{HUBSPOT_BASE}/crm/v3/objects/tasks",
            headers=HEADERS,
            json={
                "properties": {
                    "hs_task_subject": action["action"],
                    "hs_task_body": f"Owner: {action['owner']}",
                    "hs_task_priority": action.get("priority", "MEDIUM").upper(),
                    "hs_timestamp": int(datetime.strptime(action["due"], "%Y-%m-%d").timestamp() * 1000),
                },
                "associations": [
                    {"to": {"id": deal_id}, "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 216}]}
                ],
            },
        )


def _render_note(pc: dict) -> str:
    lines = [
        f"<strong>SPICED Analysis - {pc['probability']['stage']} ({pc['probability']['band']})</strong>",
        f"<em>{pc['probability']['math_display']}</em>",
        "<hr/>",
        f"<strong>Pain:</strong> {pc['spiced']['pain']['summary']}",
        f"<strong>Impact:</strong> {pc['spiced']['impact']['summary']}",
        f"<strong>Critical Event:</strong> {pc['spiced']['critical_event']['summary'] or 'None stated - risk'}",
        f"<strong>Decision:</strong> {pc['spiced']['decision']['summary']}",
        "<hr/>",
        f"<strong>Biggest lever this week:</strong> {pc['biggest_lever']}",
    ]
    return "<br/>".join(lines)
```

## Known gotchas

- HubSpot's `associationTypeId` for deal ↔ note is `214`. For deal ↔ task it's `216`. These aren't well-documented; use the Associations API to confirm in your portal.
- Private App tokens are per-portal. Rotate annually.
- The `hs_deal_stage_probability` field is often read-only in pipelines using automation. Use a custom property if needed.
