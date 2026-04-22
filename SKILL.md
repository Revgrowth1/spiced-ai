---
name: spiced-analysis
description: Analyze B2B sales discovery calls using the SPICED framework (Situation, Pain, Impact, Critical Event, Engagement, Decision). Four modes - post-call analysis, rep coaching, pre-call brief, red-flag detection. USE WHEN user says "analyze this call" OR "SPICED" OR "discovery call" OR "coach this rep" OR "pre-call brief" OR "pre-call prep" OR "sales call analysis" OR "review this transcript" OR "what went wrong on this call" OR "red flags on this deal" OR "spiced-analysis" OR "analyze my sales call" OR "evaluate this call" OR provides a sales call transcript.
---

# SPICED Analysis

Four-mode sales call analysis engine. Evaluates prospect fit (post-call), rep execution (coaching), upcoming prep (pre-call), and deal risk (red-flags) using the SPICED framework with calculable scoring.

## The 4 modes

| Mode | Purpose | When to use |
|---|---|---|
| `post_call` | SPICED analysis of a completed call - fit, probability, next actions | After a discovery/demo/pricing call |
| `coaching` | Rep execution scorecard - 8 weighted dimensions, grade, coaching actions | Weekly 1:1s, new rep onboarding, deal post-mortems |
| `pre_call` | Brief for an upcoming call - SPICED gaps, objections, exit commitment | 10 minutes before a call |
| `red_flags` | Deal-death signal detector - 9 pattern categories, severity-ranked | End of call, start of deal review, stalled deals |

## Core workflow

### Phase 1 - Identify the mode

Ask the user: "Which mode?" only if unclear from context. Defaults by phrase:

- "analyze this call" / "review this transcript" → `post_call`
- "coach this rep" / "grade the rep" / "how did [name] do" → `coaching`
- "pre-call brief" / "prep for call" / "prepare for [company]" → `pre_call`
- "red flags" / "is this deal dying" / "what am I missing on [deal]" → `red_flags`

### Phase 2 - Gather inputs

Required per mode:

**post_call:**
- Transcript (file path, or paste, or Fireflies URL - resolve to text)
- Deal context: `deal_size_band` (SMB / MID / ENTERPRISE), prior_calls_count, stage
- Company context if available (use existing research skills or skip)
- Config: default to `revgrowth.yaml` when user is Adam; otherwise `default.yaml`

**coaching:**
- Transcript
- Rep name, tenure_months
- Optional focus areas

**pre_call:**
- Prior call summaries (from prior `post_call` outputs, CRM, or user-provided notes)
- Meeting context: type, duration, attendees
- Company context

**red_flags:**
- Transcript OR last 3 SPICED analyses
- Deal context including age, last_contact_days_ago
- Optional email signals (response latency trends)

If any required input is missing, ask for it concretely - do not fabricate.

### Phase 3 - Load the mode prompt

Read the appropriate file from `~/Dev/spiced-ai/prompts/`:
- `post-call-analysis.md`
- `coaching.md`
- `pre-call-brief.md`
- `red-flags.md`

Substitute the inputs into the prompt's placeholder variables (`{{TRANSCRIPT}}`, `{{DEAL_CONTEXT}}`, `{{CONFIG_YAML}}`, etc.).

### Phase 4 - Run the analysis

Generate the output per the requested format:
- `slack` - short, paste-ready, no headers
- `crm` - structured JSON matching `~/Dev/spiced-ai/schemas/output.schema.json`
- `internal` - full markdown review

Default format depends on mode and config:
- post_call (SMB): `slack`
- post_call (MID/ENTERPRISE): `internal`
- coaching: `internal`
- pre_call: `slack` or `internal` (ask if unclear)
- red_flags: `slack` if any CRITICAL/HIGH, else `internal`

### Phase 5 - Delivery

By default, print the output in the conversation. If the user asks for delivery to HubSpot / Salesforce / Slack / Attio, reference the relevant integration doc in `~/Dev/spiced-ai/integrations/`.

For RevGrowth (Adam):
- post_call → can push to Attio + Slack `#sales-revgrowth`
- red_flags → post to Slack `#sales-red-flags` if severity is HIGH or CRITICAL

## Rules

1. **Scoring is evidence-driven.** Every SPICED letter score 0–3 must tie to transcript evidence. Quote before you summarize.
2. **If the transcript is thin or missing, say so.** Return `{"error": "transcript_insufficient"}` - do not fabricate SPICED data.
3. **Deal-size gates template depth.** SMB ≠ MID ≠ ENTERPRISE. Do not pad SMB outputs with enterprise sections.
4. **Probability math must be shown.** Never emit a close probability without the calculation that produced it.
5. **Next actions are concrete, assigned, dated.** "Follow up soon" is not an action.
6. **No flattery.** "Great call" is not analysis.
7. **Adam's voice preferences** (when using revgrowth config): no em dashes, no "It's not X, it's Y" reframes, no "Simple as." - these are in the config's `avoid_phrases`.

## Inputs the skill reads

- `~/Dev/spiced-ai/prompts/{mode}.md` - the active prompt
- `~/Dev/spiced-ai/config/{profile}.yaml` - merged config
- `~/Dev/spiced-ai/schemas/*.json` - I/O contracts
- `~/Dev/spiced-ai/integrations/*.md` - delivery targets

## CLI alternative

For non-Claude-Code use, the same prompts can be run via `~/Dev/spiced-ai/scripts/analyze.py` against the Anthropic API directly. See the README.

## Anti-patterns

- Running `post_call` when only a short call summary exists (use `pre_call` with summary-as-prior instead)
- Outputting `internal` format for an SMB deal (over-weight)
- Generating next actions without owners or dates
- Scoring Critical Event high on "they want to move fast" with no date
- Ignoring competitors mentioned in the transcript (always analyze competitive positioning for MID+)

## Self-check before returning output

- [ ] Mode identified correctly
- [ ] All required inputs present (or gap explicitly noted)
- [ ] Output format matches user's request
- [ ] For post_call: scores shown with math, deal-size-appropriate sections only
- [ ] For coaching: every strength/gap has a timestamp + quote + reframe
- [ ] For pre_call: ≤ 3 SPICED gaps, each with verbatim question
- [ ] For red_flags: every flag has cited evidence and a concrete mitigation
