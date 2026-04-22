# SPICED AI → Slack

Posts short-form outputs to Slack channels. Two surfaces: per-deal debrief channels and a central `#red-flags` alerts channel.

## Auth

Create a Slack app with `chat:write` and `chat:write.public` scopes. Install to workspace. Use the bot token.

## Post a post-call slack summary

```python
import requests
import os

SLACK_API = "https://slack.com/api"
HEADERS = {
    "Authorization": f"Bearer {os.environ['SLACK_BOT_TOKEN']}",
    "Content-Type": "application/json",
}

def post_slack_summary(channel: str, analysis: dict, call_url: str = None) -> None:
    pc = analysis["post_call"]
    prospect = pc["prospect"]

    lines = [
        f"*{prospect['name']}* ({prospect['company']}) - *{pc['probability']['stage']}* ({pc['probability']['band']})",
        f"Pain: {pc['spiced']['pain']['summary']}",
        f"Event: {pc['spiced']['critical_event']['summary'] or '_None stated - risk_'}",
        f"Decision: {_decision_status(pc['spiced']['decision'])}",
        f"Next: {_top_action(pc.get('next_actions', []))}",
        f"Score: `{pc['probability']['math_display']}`",
    ]

    blocks = [
        {"type": "section", "text": {"type": "mrkdwn", "text": "\n".join(lines)}},
    ]

    if call_url:
        blocks.append({
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": f"<{call_url}|View call>"}],
        })

    # Embed red flags if critical/high
    critical = [f for f in analysis.get("red_flags", {}).get("flags", []) if f["severity"] in ("critical", "high")]
    if critical:
        flag_text = "\n".join(f"🚩 *{f['severity'].upper()}*: {f['headline']} - {f['mitigation']}" for f in critical)
        blocks.append({"type": "divider"})
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": flag_text}})

    requests.post(
        f"{SLACK_API}/chat.postMessage",
        headers=HEADERS,
        json={"channel": channel, "blocks": blocks, "text": lines[0]},
    )


def _decision_status(decision: dict) -> str:
    committee = decision.get("summary", "")
    return committee or "_Committee unknown - gap_"


def _top_action(actions: list) -> str:
    if not actions:
        return "_No action defined_"
    a = actions[0]
    return f"{a['action']} - {a['owner']} - {a['due']}"
```

## Post a pre-call brief

```python
def post_slack_brief(channel: str, brief: dict) -> None:
    pc = brief["pre_call"]
    lines = [
        f"*Pre-call:* {pc['meeting']['attendees'][0]['name'] if pc['meeting']['attendees'] else ''} ({pc.get('meeting', {}).get('type')}, {pc['meeting']['duration_min']} min)",
        "",
        "*Close these SPICED gaps:*",
    ]
    for i, gap in enumerate(pc["spiced_gaps"], 1):
        lines.append(f"{i}. *{gap['letter']}* - {gap['gap']}")
        for q in gap["questions"][:2]:
            lines.append(f"   → \"{q}\"")

    lines += ["", "*Objections & responses:*"]
    for obj in pc["objections"]:
        lines.append(f"• \"{obj['objection']}\" → {obj['response']}")

    lines += ["", f"*Driving to:* {pc['driving_to']['best_case']}"]
    lines.append(f"*Risk to watch:* {pc['risk_to_neutralize']}")

    requests.post(
        f"{SLACK_API}/chat.postMessage",
        headers=HEADERS,
        json={"channel": channel, "text": "\n".join(lines)},
    )
```

## Red-flag alerts (dedicated channel)

Route CRITICAL/HIGH red-flag outputs to a separate channel (e.g. `#sales-red-flags`). Do not post MEDIUM or LOW - signal loss.

```python
def post_red_flag_alert(channel: str, company: str, flags: list) -> None:
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": f"🚩 {company}"}},
    ]
    for f in flags:
        if f["severity"] not in ("critical", "high"):
            continue
        signals = "\n".join(f"• {s['evidence']}" for s in f["signals"][:3])
        text = f"*[{f['severity'].upper()}] {f['headline']}*\n{signals}\n_Act this week_: {f['mitigation']}"
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})
    requests.post(f"{SLACK_API}/chat.postMessage", headers=HEADERS, json={"channel": channel, "blocks": blocks})
```

## Known gotchas

- Channel can be `#name` or `C0123456`. Prefer IDs - names can collide or be renamed.
- Slack rate-limits `chat.postMessage` at 1/sec per channel. Batch tactically.
- `text` field is used for notifications (mobile push, unfurls); always include a fallback even when using blocks.
- Adam's preference: reports must have *zero blank lines* for Slack paste-ability. When generating `internal` markdown for Slack use, flatten empty lines.
