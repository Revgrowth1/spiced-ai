# Content drafts for spiced-ai launch

Three assets: X thread (audience growth), LinkedIn system reveal post (lead gen), and a shorter tweet variant for quick posting.

---

## X/Twitter Thread (13 tweets)

**Hook formula:** Anti-Intuitive Result + Contrarian hybrid
**Angle:** We built AI call analysis, deleted 80% of it, kept what actually moves deals
**Target:** 12-13 tweets, escalating, each < 280 chars

---

**Tweet 1 (HOOK):**

Every sales team records their calls. Almost none of that data changes how they sell.

We built an AI system that fixes it. Then deleted 80% of it because it was useless.

Here's what we kept, and why most "AI call analysis" is expensive summary slop:

---

**Tweet 2 (CONTEXT):**

Modern sales teams use Fireflies, Gong, Sybill, Fathom. Every call recorded. Every word transcribed.

The data is gold. The usage is garbage.

Best case: a manager scans 3 calls a month. Worst case: nobody opens the transcripts at all.

---

**Tweet 3 (ESCALATION 1):**

So teams turn to AI. Every vendor promises "automatic call summaries powered by GPT."

We tested 6 of them across 40 real discovery calls. What they all produced:

"Priya expressed interest in our solution and asked several questions about pricing."

Useless.

---

**Tweet 4 (ESCALATION 2):**

We tried the opposite: poured the entire SPICED framework into a 500-line prompt. Every dimension scored. Every edge case covered.

Output: a 500-line analysis nobody read.

Too detailed AND too vague. We built a machine that generated work instead of doing it.

---

**Tweet 5 (TURNING POINT):**

Then we asked a dumb question: what does the rep actually need to know?

Not "comprehensive analysis." Not "every possible metric."

Just three things:

1. Did this call move the deal forward?
2. What happens next?
3. What am I missing?

---

**Tweet 6 (DEEP DIVE):**

So we rebuilt it. SPICED scoring became calculable, not vibes.

Each letter 0-3 based on transcript evidence. Multipliers for deal-killers (no budget, champion erosion, legal-with-competitor).

Output: S=2 P=3 I=2 C=1 E=2 D=2 = 12 x 0.7 = 8.4 -> 30-50%.

The math shows.

---

**Tweet 7 (DEEP DIVE):**

The coaching mode was missing from every tool we tested.

No sales team reviews every rep call with real specificity. Managers scan 3-4 a month.

We built an execution scorecard: 8 weighted dimensions, A-F grade, every gap tied to a timestamp AND a reframe.

---

**Tweet 8 (DEEP DIVE):**

The pre-call brief is where things got interesting.

Instead of analyzing calls AFTER they happened, we used the same framework to PREPARE for the next call.

One screen. Top 3 SPICED gaps with verbatim questions. Top 3 likely objections with responses. The exit commitment.

---

**Tweet 9 (DEEP DIVE):**

The red-flag detector almost didn't make it in. Felt like feature creep.

Then we ran it on real calls and it caught signals the reps missed:

> Champion using "my team" instead of "we"
> Prospect shifting from "when" to "if"
> Response latency doubling on the email thread

None of these are in a normal call summary.

---

**Tweet 10 (TWIST):**

Here's what we didn't expect:

The real value is NOT in the AI. The real value is in the framework it forces.

You could run this with a human and a spreadsheet. AI just makes it fast enough to do on every call instead of 3 a month.

Most AI tools replace thinking. This one forces it.

---

**Tweet 11 (RESOLUTION):**

Every sales intelligence tool optimizes for features: sentiment analysis, talk ratio, smile detection.

Those feel impressive. They don't change close rates.

What changes close rates: calibrated probability, specific coaching, early warning on dying deals.

We open-sourced the whole thing.

---

**Tweet 12 (BIO CTA):**

Thanks for making it to the end.

I'm Adam, founder of RevGrowth.

We build AI outbound systems for B2B companies. After running hundreds of sales calls a month across our book, this is what we use internally to stop wasting them.

---

**Tweet 13 (LINK + RT CTA):**

Repo: github.com/Revgrowth1/spiced-ai

MIT license. 3,138 lines. Four modes. Plugs into Fireflies, Gong, Sybill, HubSpot, Salesforce, Slack.

RT tweet 1 if your team's transcripts deserve better than AI summary slop.

Follow for more AI GTM infrastructure deep dives.

---

## LinkedIn System Reveal Post

**Format:** Authority anchor + numbered system reveal + philosophy line
**Target:** Engagement + repo clicks + book-a-call DMs

---

```
After running hundreds of sales calls a month across our book at RevGrowth, we built a system to stop wasting them. Today we open-sourced it.

Every modern sales team records calls. Fireflies, Gong, Sybill, Fathom. Gigabytes of transcripts. Almost none of it changes how they sell.

Most teams end up with one of two outputs:

> AI summary slop: "Priya expressed interest and asked about pricing."
> A 500-line SPICED rubric that nobody reads.

We spent a month rebuilding the analysis prompt from scratch. Here is exactly what changed:

1/ SCORING BECAME CALCULABLE

Every SPICED letter gets scored 0-3 based on transcript evidence. Multipliers applied for known deal-killers (no champion = x 0.5, legal review with competitor = x 0.3).

Close probability is now math, not vibes. Every number traces back to a specific signal.

Sample output: S=2 P=3 I=2 C=1 E=2 D=2 = 12 x 0.7 = 8.4 -> 30-50% Developing.

2/ FOUR MODES, NOT ONE

Post-call analysis is table stakes. We added three more:

> Coaching: 8-dimension rep execution scorecard with timestamped quotes and reframes
> Pre-call brief: one-screen prep the rep reads 10 minutes before the next call
> Red-flag detector: 9-category pattern scanner for champion erosion, vocabulary regression, timeline slippage

Same framework. Four angles. The coaching mode is the sleeper. No sales team in the world reviews every rep call with this level of specificity.

3/ OUTPUT FORMATS ARE DEAL-SIZE GATED

A 0K SMB deal does not need a 500-line review. A 0K enterprise deal needs more than 5 lines of Slack.

> Slack (5 lines, paste-ready): default for SMB
> CRM (structured JSON): plugs into HubSpot, Salesforce, Attio field-by-field
> Internal (full markdown review): default for MID and ENT deals

Template depth is gated. SMB skips MEDDIC overlay. Enterprise includes it. No padding.

4/ DISTRIBUTION IS BUILT IN

The original prompt output a markdown blob you had to manually paste somewhere. We built adapter docs for the full pipeline: Fireflies/Gong/Sybill/Fathom ingestion, HubSpot/Salesforce/Slack distribution.

Every integration is Python you can copy and ship tomorrow. Not a framework.

---

The build is open-sourced. MIT license. 3,138 lines.

Repo: github.com/Revgrowth1/spiced-ai

Understanding came first. Systems came later. We manually scored SPICED on every call for months before codifying any of this. The system encodes what we learned. It does not replace the learning.

If you want this plus the full outbound motion done for you, we do that at RevGrowth. Link in bio.

Hope you find this one useful.
```

---

## Short-form tweet variant (single tweet)

For quick posting + thread reply chains:

```
We open-sourced our SPICED call analysis machine.

- 4 modes (post-call, coaching, pre-call brief, red-flag detector)
- Calculable close probability (not vibes)
- Plugs into Fireflies, Gong, Sybill, HubSpot, Salesforce, Slack
- MIT, 3,138 lines

github.com/Revgrowth1/spiced-ai
```

---

## Posting recommendations

1. **LinkedIn first** (Monday or Tuesday AM) - warmer audience, longer shelf life
2. **X thread Wednesday** - reply with the short-form tweet as a "TL;DR" in the thread
3. **Newsletter Thursday** - pull from `newsletter-draft.md`
4. **Cross-link everything**:
   - LinkedIn post links to the repo, not the thread
   - X thread links to the repo
   - Newsletter links to both the repo AND the X thread

Avoid posting to both platforms on the same day. Give each its own moment.
