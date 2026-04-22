# Sample Analysis - what spiced-ai produces from the sample transcript

Three outputs shown: `slack`, `crm` (JSON), and `internal` (full markdown review). All generated from the same transcript using `mode=post_call` with the `revgrowth.yaml` config.

---

## Output 1: `slack` (default for SMB/MID)

```
Priya Shah (Marketbound) - Strong (70-80%)
Pain: 22 meetings/mo vs 60 target; reply rate dropped 6% → 2% after deliverability lead quit Jan
Event: CEO ultimatum - 50 meetings/mo within 60 days or team gets repositioned (end of June)
Decision: Priya recommends, CEO approves; COO Jessica follows CEO; no legal/proc involvement
Next: Send ROI comparison + case study today - Alex - 2026-04-18
Score: S=3 P=3 I=3 C=3 E=2 D=2 = 16 × 1.0 = 16
```

---

## Output 2: `crm` (structured JSON, attaches to deal)

```json
{
  "mode": "post_call",
  "generated_at": "2026-04-18T14:02:00Z",
  "deal_id": "marketbound_2026q2",
  "call_id": "fireflies_abc123",
  "post_call": {
    "prospect": {"name": "Priya Shah", "title": "VP of Growth", "company": "Marketbound"},
    "spiced": {
      "situation": {
        "score": 3,
        "summary": "Series B B2B SaaS, ~120 employees, running outbound in-house 18 months with 2 SDRs + manager + $30K/yr tooling, fully loaded $420K. ACV $45K, win rate 12%.",
        "quotes": [
          {"quote": "two SDRs are about $85K base, $110K OTE. Manager's $140K. Plus tools - Clay, ZoomInfo, a warmup thing - probably $30K/year in tooling.", "speaker": "Priya", "timestamp_sec": 170}
        ]
      },
      "pain": {
        "score": 3,
        "summary": "Outbound performance collapsing: 22 meetings/mo vs 60 target; reply rate dropped from 6% to 2% after deliverability specialist quit in Jan 2026.",
        "metrics": ["22 meetings/mo actual", "60 meetings/mo target", "6% → 2% reply rate", "$420K annual spend", "$1,600 cost per meeting"]
      },
      "impact": {
        "score": 3,
        "summary": "At 22 meetings × 12% win × $45K ACV = $119K revenue vs potential $324K at 60 meetings. Delta: $200K+ in annual revenue opportunity. If she hits target at lower cost ($96K vs $420K), she also frees $300K+ budget.",
        "roi_stated": "moving from 22 → 60 meetings unlocks ~$200K ARR; reducing spend from $420K → $96K saves $324K annually"
      },
      "critical_event": {
        "score": 3,
        "event": "CEO ultimatum: get back to 50 meetings/mo within 60 days (by end of June 2026) or outbound team gets repositioned",
        "date": "2026-06-30",
        "source": "explicit"
      },
      "engagement": {
        "score": 2,
        "receptivity": "High - asked proactively about trial, pricing, onboarding. Skeptical of pricing ('what's the catch?') but engaged.",
        "signals": [
          "Asked for case study unprompted",
          "Volunteered CEO's assistant email for scheduling",
          "Noted Outboundly's pricing ($15K/mo) showed she's comparison-shopping"
        ]
      },
      "decision": {
        "score": 2,
        "committee": [
          {"role": "champion", "name": "Priya Shah", "title": "VP Growth", "notes": "Makes recommendation; owns the problem"},
          {"role": "economic_buyer", "name": "CEO (not named in call)", "title": "CEO", "notes": "Approves spend; final yes/no - gap: name not captured"},
          {"role": "influencer", "name": "Jessica", "title": "COO", "notes": "Budget owner but Priya said 'she'll follow the CEO's lead'"}
        ],
        "criteria": [
          "meetings per dollar",
          "speed to get set up",
          "agency owns execution (not more work for her team)"
        ],
        "process": "Three-way call with Priya + Alex + CEO week of 4/28 or 5/5",
        "gaps": ["CEO's name", "COO's specific authority if budget exceeds threshold", "whether any procurement review required"]
      }
    },
    "probability": {
      "raw": 16,
      "multipliers": [],
      "final": 16.0,
      "band": "70-80%",
      "stage": "Strong",
      "math_display": "S=3 P=3 I=3 C=3 E=2 D=2 = 16 × 1.0 = 16 → 70-80% Strong"
    },
    "next_actions": [
      {"action": "Send ROI comparison (current $420K → proposed $96K) + Series B case study to Priya", "owner": "Alex", "due": "2026-04-18", "priority": "high"},
      {"action": "Email Sam (sam@marketbound.io) to schedule three-way with Priya + CEO for week of 4/28 or 5/5", "owner": "Alex", "due": "2026-04-19", "priority": "high"},
      {"action": "Research Marketbound CEO on LinkedIn; identify prior outbound experience / biases", "owner": "Alex", "due": "2026-04-22", "priority": "med"},
      {"action": "Prepare CEO-facing pitch emphasizing (a) deliverability diagnosis, (b) cost reduction, (c) 90-day opt-out safety net", "owner": "Alex", "due": "2026-04-25", "priority": "high"}
    ],
    "risks": [
      {
        "risk": "CEO may have pre-existing skepticism of outbound (he's already considering killing the channel for content marketing)",
        "probability": "high",
        "severity": "high",
        "mitigation": "In CEO call, lead with cost reduction + 90-day opt-out before pitching upside. Frame as 'stop the bleeding' not 'invest more.'"
      },
      {
        "risk": "Outboundly is in active evaluation; Priya had call last week; they quoted $15K/mo",
        "probability": "med",
        "severity": "high",
        "mitigation": "Position differentiator as deliverability ownership + lower price. Send ROI comparison that includes Outboundly's number explicitly to anchor."
      },
      {
        "risk": "Timeline risk - CEO travel may push three-way into May, compressing the 60-day window",
        "probability": "med",
        "severity": "med",
        "mitigation": "Offer async CEO-facing Loom video as fallback; propose written proposal review if scheduling slips."
      }
    ],
    "competitors_mentioned": [
      {"name": "Outboundly", "positioning": "Generic list + sequences, $15K/mo, no deliverability story", "threat_level": "med"},
      {"name": "Instantly", "positioning": "Tried and didn't move the needle (tool, not agency)", "threat_level": "low"},
      {"name": "In-house (status quo)", "positioning": "Current state; CEO leaning toward killing", "threat_level": "low"}
    ],
    "biggest_lever": "Lock the three-way CEO call before April 28. The deal turns on whether the CEO hears the cost-reduction story directly from Alex, not filtered through Priya. Delay = deal decays."
  },
  "red_flags": {
    "flag_count": 1,
    "max_severity": "medium",
    "flags": [
      {
        "category": "timeline_slippage",
        "severity": "medium",
        "signals": [
          {"evidence": "CEO traveling 'next week' - three-way pushed to week of 4/28 or 5/5", "source": "transcript", "timestamp_sec": 1775}
        ],
        "headline": "Three-way scheduling may compress the 60-day CEO ultimatum window",
        "impact": "If three-way slips into May, decision timing and ramp-up collide",
        "mitigation": "Offer async Loom to CEO as parallel path; don't wait on single calendar slot",
        "deadline": "2026-04-28"
      }
    ]
  }
}
```

---

## Output 3: `internal` (full markdown review, for internal deal review)

```markdown
# Marketbound - Priya Shah (Call 1)

**Stage:** Strong · **Probability:** 70-80% · **ACV band:** MID
**Score:** S=3 P=3 I=3 C=3 E=2 D=2 = 16 × 1.0 = 16

## Situation
Marketbound is a Series B B2B SaaS with ~120 employees and ~$14M ARR. Running outbound in-house for 18 months via 2 SDRs + 1 manager + tooling (Clay, ZoomInfo, Instantly) - fully loaded $420K/year. ACV $45K, win rate 12%. Deliverability specialist departed January 2026; no replacement.

## Pain
- **Quantified:** 22 meetings/mo actual vs 60 target (37% of goal). Reply rate dropped from 6% → 2%. $1,600 cost per meeting.
- **Qualitative:** CEO losing faith in outbound as a channel; pressure on Priya personally.
- **Implied (unverified):** SDR morale likely declining on 40% attainment - ASSUMPTION, not asked.

## Impact
- **Financial:** At 60 meetings × 12% × $45K = $324K ARR; at 22 meetings × 12% × $45K = $119K. Delta: $200K+ lost ARR. If RevGrowth at $96K delivers 50+ meetings, saves $324K/year on spend AND recovers $200K+ ARR.
- **Strategic:** Outbound channel survival. If it dies, Marketbound becomes inbound-dependent.
- **Timing:** Immediate - ramp is 4-6 weeks, budget decision needed within 2-3 weeks to hit CEO's June deadline.

## Critical Event
CEO ultimatum: 50 meetings/mo within 60 days or outbound team repositioned (content marketing pivot). End of Q2 = 2026-06-30.

## Engagement
Priya is actively engaged - asked for pricing, trial, onboarding specifics, volunteered her CEO's assistant's email unprompted. Skeptical of pricing being "too good to be true" but that's an objection to address, not disqualifying. Volunteered she's evaluating Outboundly.

## Decision

**Committee:**
- Champion: Priya Shah (VP Growth) - owns the recommendation
- Economic buyer: CEO (name not captured - **gap for next interaction**)
- Influencer: Jessica (COO) - budget owner but deferring to CEO per Priya
- Other: Sam (CEO's assistant) - scheduling gatekeeper

**Criteria (prospect-stated):**
1. Meetings per dollar
2. Speed to get set up
3. Agency owns execution (no team burden)

**Process:** Three-way call with Priya + Alex + CEO, week of 4/28 or 5/5
**Timeline:** Decision needed within 2-3 weeks to allow ramp-up before June 30

## Competitive positioning (MID+ included)

- **Named competitors:** Outboundly (active eval, had call last week, quoted $15K/mo); Instantly (tried, didn't work - tool not agency, not a real competitor); in-house status quo
- **How we win:** 77% cheaper than current spend AND 47% cheaper than Outboundly; deliverability ownership (Outboundly didn't mention); 90-day opt-out de-risks the decision
- **How we lose:** If CEO already decided outbound is dead and this call is just a formality; if Outboundly comes back with a substantially similar offer at our price; if ramp-up timeline spooks the CEO into "content instead"

## Risks
| Risk | Prob | Severity | Mitigation |
|---|---|---|---|
| CEO pre-decided to kill outbound, meeting is a formality | Med | High | Lead the three-way with "recover sunk cost + reduce risk," not "invest more" |
| Outboundly drops price to compete | Med | High | Send ROI comparison anchoring Outboundly's $15K explicitly; emphasize deliverability gap |
| Timeline slip (CEO travel) compresses 60-day window | Med | Med | Offer async Loom to CEO as parallel; don't bottleneck on calendar |
| Priya doesn't translate the cost story well in internal pitch | Med | Med | Prepare 1-pager Priya can forward that leads with numbers (current vs proposed), not features |

## Next actions (concrete, assigned, dated)
1. Send ROI comparison ($420K current → $96K proposed, including Outboundly anchor) + Series B case study to Priya - Alex - 2026-04-18
2. Email Sam (sam@marketbound.io) to book three-way for week of 4/28 or 5/5 - Alex - 2026-04-19
3. LinkedIn research on CEO (prior outbound experience, biases) - Alex - 2026-04-22
4. Draft CEO-facing 1-pager emphasizing cost reduction + 90-day opt-out - Alex - 2026-04-25

## Single biggest lever this week
Lock the three-way CEO call before April 28. The deal turns on whether the CEO hears the cost-reduction story directly - not filtered through Priya. Every week of delay compresses the ramp window; if this slips into mid-May the deal becomes significantly harder because the CEO's deadline arrives before RevGrowth can produce the meetings that save it.
```

---

## Notes on what this demonstrates

- **Score is calculable:** S=3 P=3 I=3 C=3 E=2 D=2 → 16 → 70-80% Strong. Not vibes.
- **Gaps are named:** CEO's name not captured; procurement process not asked. These are explicit deliverables, not hidden assumptions.
- **Next actions are concrete:** Assigned, dated, priority-ranked. "Schedule follow-up" does not appear.
- **Competitive analysis is honest:** Both how we win *and* how we lose. No flattery.
- **Deal-size-appropriate depth:** MID template → includes competitive + risk register + champion mapping. No MEDDIC overlay (that would be ENTERPRISE only). No reference-validation section (not yet relevant).
- **Biggest lever is one thing:** Forces the reader to know what matters most.
