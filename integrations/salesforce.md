# SPICED AI → Salesforce

Writes post-call analysis to the Opportunity record via REST API.

## What goes where

| Output field | Salesforce destination |
|---|---|
| `probability.final` (normalized) | `Opportunity.Probability` (standard) |
| `probability.stage` | `Opportunity.SPICED_Stage__c` (custom) |
| `probability.math_display` | `Opportunity.SPICED_Score_Detail__c` (custom) |
| `spiced.*` summaries | `Opportunity.Description` (appended) or related `Note` |
| `next_actions` | `Task` records (one per action) |
| `risks` | `Opportunity.Risk_Summary__c` (custom long-text) |
| `red_flags` | `Opportunity.Red_Flags__c` + Chatter post |

## Setup (one-time)

Add custom fields to `Opportunity`:

```
SPICED_Stage__c                 Text(50)
SPICED_Score_Detail__c          Text(255)
SPICED_Probability__c           Number(4,3)  (0.000 – 1.000)
Risk_Summary__c                 Long Text Area(32768)
Red_Flags__c                    Long Text Area(32768)
Last_SPICED_Analysis_At__c      DateTime
```

## Auth - OAuth JWT Bearer flow (server-to-server)

```python
import jwt
import time
import requests
import os

def sf_access_token() -> tuple[str, str]:
    """Returns (access_token, instance_url)."""
    claim = {
        "iss": os.environ["SF_CLIENT_ID"],
        "sub": os.environ["SF_USERNAME"],
        "aud": os.environ.get("SF_LOGIN_URL", "https://login.salesforce.com"),
        "exp": int(time.time()) + 300,
    }
    with open(os.environ["SF_PRIVATE_KEY_PATH"]) as f:
        private_key = f.read()
    assertion = jwt.encode(claim, private_key, algorithm="RS256")

    r = requests.post(
        f"{claim['aud']}/services/oauth2/token",
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion,
        },
    )
    r.raise_for_status()
    j = r.json()
    return j["access_token"], j["instance_url"]
```

## Write adapter

```python
def push_to_salesforce(opportunity_id: str, analysis: dict) -> None:
    token, instance = sf_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    base = f"{instance}/services/data/v59.0"
    pc = analysis["post_call"]

    # 1. Update opportunity
    requests.patch(
        f"{base}/sobjects/Opportunity/{opportunity_id}",
        headers=headers,
        json={
            "SPICED_Stage__c": pc["probability"]["stage"],
            "SPICED_Score_Detail__c": pc["probability"]["math_display"],
            "SPICED_Probability__c": pc["probability"]["final"] / 18,
            "Probability": int((pc["probability"]["final"] / 18) * 100),
            "Risk_Summary__c": _render_risks(pc.get("risks", [])),
            "Last_SPICED_Analysis_At__c": datetime.utcnow().isoformat(),
        },
    )

    # 2. Create tasks
    for action in pc.get("next_actions", []):
        requests.post(
            f"{base}/sobjects/Task",
            headers=headers,
            json={
                "Subject": action["action"],
                "WhoId": None,
                "WhatId": opportunity_id,
                "ActivityDate": action["due"],
                "Priority": action.get("priority", "Normal").capitalize(),
                "Description": f"Owner: {action['owner']}",
            },
        )

    # 3. Chatter post if red flags
    critical_flags = [f for f in analysis.get("red_flags", {}).get("flags", []) if f["severity"] in ("critical", "high")]
    if critical_flags:
        requests.post(
            f"{base}/chatter/feed-elements",
            headers=headers,
            json={
                "body": {"messageSegments": [{"type": "Text", "text": _render_flags(critical_flags)}]},
                "feedElementType": "FeedItem",
                "subjectId": opportunity_id,
            },
        )


def _render_risks(risks):
    return "\n".join(f"• [{r['severity'].upper()}] {r['risk']} → {r['mitigation']}" for r in risks)


def _render_flags(flags):
    return "\n".join(f"🚩 [{f['severity'].upper()}] {f['headline']} - {f['mitigation']}" for f in flags)
```

## Known gotchas

- Custom field API names end with `__c`. Don't forget the suffix.
- `Probability` (standard) is 0–100 (int); custom `SPICED_Probability__c` is 0–1 (decimal). Write both.
- Chatter posts require `subjectId` pointing at the Opportunity or Account.
- JWT Bearer flow requires a pre-authorized Connected App - don't try interactive OAuth for server-side use.
