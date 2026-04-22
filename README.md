# spiced-ai

**B2B sales call analysis that doesn't pretend.** SPICED-framework analysis with calculable scoring, rep coaching, pre-call prep, and red-flag detection. Works as a Claude Code skill, a Python CLI, or a prompt library you drop into your own stack.

Built by [RevGrowth](https://revgrowth.ai) out of necessity. Sales teams waste their transcripts. This fixes it.

---

## The problem this solves

Your sales team records every call. Fireflies, Gong, Sybill, Fathom, Zoom, whatever. That data sits in a pile. Maybe a rep scrolls it once. Maybe a manager looks at three calls a month. The rest is organizational amnesia.

When teams do try to analyze calls, they get one of two outputs:

1. **AI summary slop** that a human has to read in full to extract signal ("Priya is interested in our solution and asked several questions about pricing")
2. **A 500-line SPICED rubric** that no one actually reads

Both fail the real job. Reps need to know: *did this call move the deal forward, what happens next, what am I missing?* Managers need to know: *is this rep improving, which deals are at risk, where do I coach?*

spiced-ai is built around those questions.

---

## What's different

| | Typical AI call summary | **spiced-ai** |
|---|---|---|
| Output length | Whatever the model produces | Deal-size-gated: SMB gets 5 lines, ENT gets full review |
| Close probability | "High" / "Medium" / "Low" | Calculable: `S=3 P=3 I=2 C=1 E=2 D=2 = 13 × 0.7 = 9.1 → 30-50%` |
| Next actions | "Schedule a follow-up" | Concrete, assigned, dated |
| Rep coaching | Missing entirely | 8-dimension weighted scorecard with timestamped quotes + reframes |
| Red flags | Missing entirely | 9-category pattern detector with severity bands |
| Pre-call prep | Missing entirely | One-screen brief: SPICED gaps + objections + exit commitment |
| Distribution | Markdown blob | Structured JSON → HubSpot / Salesforce / Slack |

---

## The 4 modes

### 1. `post_call` - what happened + what's next
SPICED scoring (0–3 per letter), close-probability math, competitive positioning, risks, next actions. Deal-size-gated depth.

### 2. `coaching` - how did the rep do
8 weighted dimensions scored 0–5 with timestamp-backed strengths, gaps, and reframes. Outputs a grade (A–F) and this-week coaching assignments.

### 3. `pre_call` - what to ask on the next call
Reads prior calls + CRM + company context. Produces a one-screen brief: top 3 SPICED gaps with verbatim questions, top 3 objections with planned responses, the exit commitment you're driving to.

### 4. `red_flags` - what's about to kill this deal
Pattern detector for champion erosion, budget shifts, competitive displacement, vocabulary regression, timeline slippage, silent objections, probability drift. Cited evidence, severity-ranked, concrete mitigations.

---

## Install (30 seconds)

### As a Claude Code skill

```bash
git clone https://github.com/Revgrowth1/spiced-ai ~/Dev/spiced-ai
ln -s ~/Dev/spiced-ai ~/.claude/skills/spiced-analysis
```

Then in Claude Code, just say: *"analyze this call"* and paste a transcript.

### As a CLI

```bash
git clone https://github.com/Revgrowth1/spiced-ai
cd spiced-ai
pip install anthropic pyyaml
export ANTHROPIC_API_KEY=sk-ant-...

./scripts/analyze.py \
  --mode post_call \
  --transcript examples/sample-transcript.md \
  --deal-size MID \
  --output-format internal
```

### As a prompt library

Don't use Claude? Fine. The prompts in `prompts/` are self-contained. Copy `prompts/post-call-analysis.md` into your own LLM pipeline. The scoring mechanic, output formats, and anti-patterns all travel. Config-driven customization via `config/*.yaml`.

---

## Example output

Drop this transcript in:

> **Priya (prospect):** We're at 22 meetings a month. Target is 60. Our CEO gave me 60 days to turn it around or he's cutting the outbound team. Currently spending $420K/year fully loaded.

spiced-ai returns (`slack` format):

```
Priya Shah (Marketbound) - Strong (70-80%)
Pain: 22 meetings/mo vs 60 target; reply rate dropped 6% → 2% after deliverability lead quit Jan
Event: CEO ultimatum - 50 meetings/mo within 60 days or team gets repositioned (end of June)
Decision: Priya recommends, CEO approves; COO Jessica follows CEO; no legal/proc involvement
Next: Send ROI comparison + case study today - Alex - 2026-04-18
Score: S=3 P=3 I=3 C=3 E=2 D=2 = 16 × 1.0 = 16
```

See `examples/sample-analysis.md` for the full `internal` review and `crm` JSON.

---

## Configure for your motion

Copy `config/default.yaml` → `config/yourname.yaml`. Set your ICP, deal size bands, competitors, objections, and success metrics. Pass `--config yourname` to the CLI, or reference it in the skill's config field.

Example snippet:

```yaml
deal_sizing:
  smb_max_acv_usd: 25000
  mid_max_acv_usd: 250000

competitors:
  - name: "Outreach"
    positioning: "Bloated, expensive, SMB-hostile"
    our_counter: "We're 1/5 the price with better inbox placement"
```

The prompts inherit the config automatically.

---

## Pipe it into your stack

- **[Fireflies](integrations/fireflies.md)** → transcript ingestion + webhook
- **[Sybill](integrations/sybill.md)** → transcript + sentiment
- **[Gong](integrations/gong.md)** → enterprise-grade transcript API
- **[Fathom](integrations/fathom.md)** → lightweight option
- **[HubSpot](integrations/hubspot.md)** → deal properties + notes + tasks
- **[Salesforce](integrations/salesforce.md)** → opportunity fields + tasks + Chatter
- **[Slack](integrations/slack.md)** → debrief channels + red-flag alerts

Each integration doc is copy-pasteable Python. Not a framework. Code you can read in 5 minutes.

---

## Why we built this

RevGrowth runs outbound for B2B SaaS companies. We sit on hundreds of sales calls a month across our book. The signal in those calls was drowning in noise. We tried every commercial call-analysis tool and none gave us what we actually needed: calibrated probability math, specific coaching actions, and early warning on dying deals.

So we built it. Then realized the prompt was 80% of the value. Open-sourcing the rest is a rounding error on a weekend.

If you're a B2B team that wants this wired into your pipeline end-to-end: [we do that](https://revgrowth.ai). If you're a solo operator who wants to run it yourself: clone and go.

---

## The SPICED scoring math (so you know it's not vibes)

Each letter gets 0–3 based on transcript evidence:
- **0** - not discussed
- **1** - mentioned, no specifics
- **2** - discussed with ≥1 concrete data point
- **3** - quoted, quantified, named stakeholders or dates

Raw score = sum (max 18). Apply multipliers:

| Condition | Multiplier |
|---|---|
| Competitor named and ahead | × 0.8 |
| Budget not confirmed for current FY | × 0.7 |
| No identified champion | × 0.5 |
| Champion left / demoted since last call | × 0.4 |
| In legal/procurement with competitor | × 0.3 |

Final → probability band:

| Final | Probability | Stage |
|---|---|---|
| ≥ 16 | 90%+ | Committed |
| 13–15 | 70–80% | Strong |
| 10–12 | 50–70% | Viable |
| 7–9 | 30–50% | Developing |
| < 7 | < 30% | Exploratory |

Every output shows the math inline. If a number seems off, you can trace it back to a specific letter score and a specific multiplier.

---

## Coaching scoring math

Reps graded on 8 weighted dimensions, 0–5 each:

| Dimension | Weight |
|---|---|
| Discovery depth | 3 |
| Question quality | 2 |
| Listen/talk ratio | 2 |
| Objection handling | 2 |
| Critical event establishment | 3 |
| Decision committee mapping | 2 |
| Competitive positioning | 2 |
| Next-step commitment | 2 |

Max 90. Grade bands: A (72–90), B (60–71), C (48–59), D (36–47), F (<36).

Every score cites a timestamp and a verbatim quote. Every gap includes a reframe (literally what to say next time). Every coaching action is executable this week.

---

## Limits and honest caveats

- **Transcripts under 500 words** return `{"error": "transcript_insufficient"}`. Short summaries don't carry enough signal to score SPICED honestly.
- **Speaker diarization matters.** If your transcript mis-labels "rep" vs "prospect," scoring breaks. All integration adapters include role-detection logic but it's not perfect.
- **Probability is probabilistic.** Even a 90%+ deal loses sometimes. The math calibrates confidence, not certainty.
- **Coaching requires a full discovery call.** Don't score a 15-minute demo on the full rubric. Use partial scoring or skip coaching for short calls.

---

## Repo layout

```
spiced-ai/
├── README.md                    ← you are here
├── LICENSE                      ← MIT
├── SKILL.md                     ← Claude Code skill manifest
├── prompts/
│   ├── post-call-analysis.md    ← SPICED scoring + probability
│   ├── coaching.md              ← 8-dimension rep scorecard
│   ├── pre-call-brief.md        ← one-screen prep doc
│   └── red-flags.md             ← 9-category deal-death detector
├── config/
│   ├── default.yaml             ← generic B2B SaaS starting point
│   └── revgrowth.yaml           ← real example config
├── schemas/
│   ├── input.schema.json        ← normalized transcript format
│   └── output.schema.json       ← structured analysis output
├── integrations/
│   ├── fireflies.md · sybill.md · gong.md · fathom.md
│   └── hubspot.md · salesforce.md · slack.md
├── examples/
│   ├── sample-transcript.md     ← realistic 32-min discovery call
│   └── sample-analysis.md       ← all 3 output formats demonstrated
└── scripts/
    └── analyze.py               ← CLI (uses Anthropic API directly)
```

---

## Contributing

Real-world transcripts teach the prompts more than any synthetic data. If you find a failure mode (bad score, missed flag, ranking off), open an issue with the transcript snippet + expected vs actual output. We'll adjust the prompts.

Pull requests welcome for:
- New integration adapters (Apollo, Chorus, Avoma, Salesloft)
- Config presets for specific verticals (PLG SaaS, vertical SaaS, agency services)
- Edge-case transcripts for the examples folder

---

## License

MIT. Use it, fork it, ship it.

---

## About RevGrowth

We build cold email infrastructure and run outbound for B2B SaaS companies. AI-driven deliverability, verified lists, managed campaigns, no SDRs required. [revgrowth.ai](https://revgrowth.ai)

If you want the team behind this tool managing your outbound: [book a call](https://revgrowth.ai). If you want to run the tool yourself: you already have everything you need above.
