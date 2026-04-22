SUBJECT LINE CANDIDATES (pick one, test the others)
- We open-sourced our SPICED call analysis machine (3138 lines, free)
- Every sales call is a deal-health report. Most teams throw it away.
- The system that grades every sales call automatically
- Your call transcripts are dead assets. Here's the fix.

---

April [TK], 2026   |   Read online

We open-sourced our SPICED call analysis machine

share on facebook     share on twitter     share on threads     share on linkedin

-------- SECTION 1: SUMMARY --------

Your sales team records every call. Fireflies. Gong. Sybill. Fathom. Whatever.

None of that data compounds.

Maybe a rep scrolls it once. Maybe a manager looks at three calls a month. The rest is organizational amnesia. And when teams DO analyze calls, they get one of two outputs: a fluffy AI summary that reads like LinkedIn slop, or a 500-line SPICED rubric no human actually consumes.

We built spiced-ai to fix that. Four-mode sales call analysis, calculable close probability (not vibes), rep coaching scorecard, pre-call brief, red-flag detector. Open-sourced at github.com/Revgrowth1/spiced-ai.

~5 minute read

> Clone the repo: https://github.com/Revgrowth1/spiced-ai

-------- SECTION 2: ACTIONABLE TIP --------

Run this check on your last 3 sales calls today

Most sales teams think they know their pipeline. They don't. They know their CRM, which is a lagging indicator populated by rep memory.

Here's what to do right now:

What: Pull transcripts from your last 3 discovery calls and score each SPICED letter 0-3 yourself (Situation, Pain, Impact, Critical Event, Engagement, Decision)
Why: You'll find 1-2 letters scoring 0 on deals you thought were "good." Those zeros are your next-call gaps
How:
1. Open your most recent 3 discovery call recordings
2. For each one, write down one number 0-3 per SPICED letter. Evidence rule: score 0 if not discussed, 1 if mentioned without specifics, 2 if specific data point, 3 if quoted-quantified-named
3. Sum the 6 scores. Below 10 on a "qualified" deal means you have blind spots the rep is not telling you about

Do this on 3 calls this week. If the scores don't match your gut feel on those deals, your gut is wrong. Time to systematize the scoring.

-------- SECTION 3: BEST LINKS --------

> spiced-ai repo (MIT-licensed, clone and go): https://github.com/Revgrowth1/spiced-ai
> The actual SPICED framework (Winning by Design, where this came from): https://winningbydesign.com/revenue-academy/
> Our tam-map skill (if you liked spiced-ai, this one scrapes 40K leads in 12 min): https://github.com/Revgrowth1/tam-map
> Our ai-gtm-workflows repo (12 more GTM builds): https://github.com/Revgrowth1/ai-gtm-workflows

-------- SECTION 4: DEEP DIVE --------

We open-sourced our SPICED call analysis machine

The original prompt was 500 lines of markdown. Looked thorough. Was useless.

We ran it on 40 real discovery calls across RevGrowth's book and found the same problems every time:

> The SPICED framework order was inconsistent between the instructions and the output template
> The output was so long nobody read it
> Close probability said things like "90%+" with no math backing it up
> It never scored the rep - only the prospect
> There was no "what do I do about it" section

So we rebuilt it. Here is exactly what changed and how the system works now.

FIX #1: SPICED scoring is calculable, not vibes

Every call gets scored on each SPICED letter 0-3 based on transcript evidence.

> 0 = not discussed
> 1 = mentioned, no specifics
> 2 = discussed with at least one concrete data point
> 3 = quoted, quantified, named stakeholders or dates

Raw score = sum of the 6 letters (max 18). Then multipliers hit:

> Competitor named and ahead: x 0.8
> Budget not confirmed for current FY: x 0.7
> No identified champion: x 0.5
> Champion left or demoted: x 0.4
> Deal is in legal with a competitor: x 0.3

Final score maps to a probability band. A call might return: S=2 P=3 I=2 C=1 E=2 D=2 = 12 raw x 0.7 (no budget) = 8.4 -> 30-50% Developing.

If the probability seems off, you can trace it back to a specific letter and a specific multiplier. The math shows. That is the point.

FIX #2: Four modes, not one

The original prompt only did post-call analysis. Useful but incomplete. We added three more modes.

> post_call: SPICED analysis of a completed call (what happened, what's next, probability)
> coaching: Rep execution scorecard with 8 weighted dimensions, timestamped quotes, and reframe suggestions
> pre_call: One-screen brief the rep reads in 10 minutes before their next call - SPICED gaps, verbatim questions to ask, top 3 objections with planned responses, the exit commitment they're driving to
> red_flags: 9-category deal-death detector (champion erosion, vocabulary regression, timeline slippage, silent objections, probability drift, etc.)

Same framework, four angles. The coaching mode is the sleeper. No sales team in the world reviews every rep call with this level of specificity. Managers scan 3-4 calls a month. spiced-ai reviews all of them at once.

FIX #3: Three output formats, deal-size gated

Your CEO does not need a 500-line deal review for a $10K SMB deal. Your enterprise sales team does not want a 5-line Slack message for a $500K opportunity.

> slack: 5-line paste-ready summary (default for SMB)
> crm: Structured JSON that plugs into HubSpot, Salesforce, or Attio field-by-field
> internal: Full markdown review for debriefs and deal reviews (default for MID/ENT)

Template depth is gated by deal size. SMB skips the MEDDIC overlay. ENTERPRISE includes it. No padding.

FIX #4: Distribution is built in

The original prompt output a markdown blob. You had to manually paste it into your CRM. We built adapter docs for the full pipe:

> Ingestion: Fireflies, Sybill, Gong, Fathom (each has a Python adapter you can copy in 5 minutes)
> Distribution: HubSpot deal properties and tasks, Salesforce opportunities and Chatter, Slack channels
> Structured JSON schema so downstream systems don't have to parse markdown

Every integration doc is code you can read in 5 minutes and ship tomorrow. Not a framework. Copy and paste.

Real example from the sample call in the repo

Priya is VP Growth at a Series B B2B SaaS. Spending $420K/year on in-house outbound, hitting 22 meetings/month vs a 60-meeting target. CEO gave her 60 days to turn it around or the outbound team gets repositioned into content marketing.

spiced-ai runs the transcript and returns:

Priya Shah (Marketbound) - Strong (70-80%)
Pain: 22 meetings/mo vs 60 target; reply rate dropped 6% to 2% after deliverability lead quit Jan
Event: CEO ultimatum - 50 meetings/mo within 60 days or team gets repositioned (end of June)
Decision: Priya recommends, CEO approves; COO Jessica follows CEO; no legal/proc involvement
Next: Send ROI comparison + case study today - Alex - 2026-04-18
Score: S=3 P=3 I=3 C=3 E=2 D=2 = 16 x 1.0 = 16

That lands in the rep's Slack channel 90 seconds after the call ends. The CRM gets the structured JSON. If there's a red flag above MEDIUM severity, it fires into a separate #red-flags channel so managers see it.

The rep does not have to fill out anything. The manager does not have to read a transcript. The system compounds.

Why this matters

The vast majority of sales intelligence tools optimize for "more features" (AI-generated summary, sentiment analysis, smile detection, talk ratio). Those features feel impressive. They don't change close rates.

What changes close rates: the rep knowing exactly what SPICED letter is weakest on their next call, the manager knowing which deals are dying before the rep realizes it, and the whole system compounding across hundreds of calls instead of starting from zero every Monday.

spiced-ai does that in 3,138 lines of mostly markdown. No SaaS to buy. No seat pricing. Clone the repo, add an Anthropic API key, point it at your transcripts.

We use this internally on every RevGrowth call. We published it because the prompt was 80% of the value. Open-sourcing the rest is a rounding error on a weekend.

Install in 30 seconds

As a Claude Code skill:
git clone https://github.com/Revgrowth1/spiced-ai ~/Dev/spiced-ai
ln -s ~/Dev/spiced-ai ~/.claude/skills/spiced-analysis

Then in Claude Code, just say "analyze this call" and paste a transcript.

As a Python CLI:
git clone https://github.com/Revgrowth1/spiced-ai
cd spiced-ai
pip install anthropic pyyaml
export ANTHROPIC_API_KEY=sk-ant-...
./scripts/analyze.py --mode post_call --transcript your-call.txt --deal-size MID --output-format internal

Config-driven. Copy config/default.yaml to config/yourname.yaml and set your ICP, deal size bands, competitors, and objection responses. The prompts inherit the config automatically.

-------- SECTION 5: HOW I CAN HELP --------

How I Can Help

> Clone spiced-ai: https://github.com/Revgrowth1/spiced-ai
> Book a call (if you want this plus the outbound motion done for you): https://calendly.com/adam-revgrowth/30min
> Outbound Secrets course (70+ training videos on everything we implement): https://outbound-secrets.com (code REV20 for 20% off)
> Reply to this email with your weirdest sales call and I'll run spiced-ai on it

-------- SECTION 6: POLL --------

How was today's newsletter?

[Loved it] [It was okay] [Not great]

--------

Hope you found this email useful.

Have a blessed day,

Adam

---

NOTES FOR ADAM (not for newsletter):
- Subject line: lean "Your call transcripts are dead assets. Here's the fix." for open rate. "We open-sourced our SPICED call analysis machine" has more authority but tests as lower open rate
- Consider adding a screenshot of the sample analysis output in the deep dive section (visual break)
- Pillar: Sales process + AI GTM Engineering (double coverage since it's a build + workflow)
- CTA priorities (top to bottom): 1) clone repo, 2) book call, 3) Outbound Secrets
- Length: ~900 words in deep dive. Trim if over target (aim for 4-5 min read)
