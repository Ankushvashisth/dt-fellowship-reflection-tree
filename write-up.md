# Write-Up: Design Rationale for the Daily Reflection Tree

---

## Why These Questions

The central challenge of a reflection tool is that **most people are unaware of their own patterns in the moment**. Someone on the external end of Locus of Control doesn't think "I have an external locus today." They think "my manager didn't give me clear enough direction." The questions have to surface the pattern without naming it — because naming it triggers defensiveness, not insight.

**Axis 1 — Locus:** I chose the car metaphor deliberately. "Driver, navigator, passenger, stranded" is a concrete spatial frame, not an abstract psychological one. A tired employee at 7pm can locate themselves in it immediately. The metaphor also avoids the blame language that makes Locus of Control questions feel like an indictment. "You were a passenger today" is neutral. "You had an external locus of control" is a diagnosis.

The follow-up branching matters here: the employee who says "passenger" isn't automatically external — they might have been searching for what they could control (Rotter's internal orientation in disguise). The three-level probe (agency_low → the mental energy question → the "did you make any call?" question) tries to find the smallest evidence of agency before issuing any reflection. The final reflection for the fully external path is *compassionate*, not corrective. That was an intentional constraint: the tool should not shame.

**Axis 2 — Orientation:** Campbell et al.'s entitlement research points to a specific mechanism: entitlement is invisible to the person holding it. They don't feel entitled — they feel *underappreciated*. So the Axis 2 questions avoid the word "entitlement" entirely and instead follow the money: *where did your energy go?* and *what's the dominant feeling about your team?* These are behavioral and emotional questions, not self-assessment questions. They're harder to game.

The "what counts?" branch for ambiguous contribution cases (A2_Q_WHAT_COUNTS) is a design choice I'm particularly attached to. It gives the employee a list of things that might have happened — listening, catching something before it became a problem, acknowledging someone — and asks them to claim one. This is based on Organ's OCB research: discretionary behavior is often dismissed by the person doing it as "just being normal." The question reframes it.

**Axis 3 — Radius:** Maslow's self-transcendence (1969) is almost always described as a lofty peak-experience concept. But in daily work, it manifests simply: *did you think about how today affected someone other than yourself?* The opening question for Axis 3 uses progressively widening circles — just me → my team → a specific colleague → the end user — and routes differently based on where the employee's awareness naturally landed. This produces meaningfully different follow-up questions.

---

## How I Designed the Branching

The tree has three types of branching:

**1. Coarse routing (Axis entry):** The opening question for each axis separates the population into two rough camps (high/low agency; contribution/entitlement orientation; self/other radius). This determines which branch of follow-up questions they enter.

**2. Fine routing (within-branch):** Inside each camp, a second question distinguishes between different flavors — e.g., the "external" camp includes people who were searching for control (who route to the "emerging agency" reflection) and people who were genuinely stuck (who get probed once more). This prevents the tool from flattening real diversity into two buckets.

**3. Aggregated routing (summary):** The summary node uses the accumulated axis signals (internal/external, contribution/entitlement, other/self) to select from 8 pre-written combined reflection templates. The key was writing these templates so none of them feel like a score. The "external_entitlement_self" template doesn't say "you had a bad day in all three dimensions." It says: "Today was hard, and the frame stayed tight. Tomorrow is a new set of variables." That's honest without being evaluative.

**Trade-offs I made:**
- I chose **depth over breadth** in Axis 1 — more follow-up probing for the external path, because that's where the interesting insight lives. The internal path is shorter because those employees generally need affirmation more than probing.
- I deliberately made the options **non-obvious** at first glance. A question like "which of these happened today — even once?" with options like "I caught something before it became someone else's problem" requires genuine memory search. That friction is intentional: it slows down click-through behavior.
- The **bridge nodes** carry real conceptual weight. "You've looked at how you moved — now let's look at what you gave" isn't just a transition sentence. It names the axis shift, primes the employee's attention, and creates narrative continuity across what might otherwise feel like three separate quizzes.

---

## Psychological Sources

| Framework | Source | How it shaped the design |
|-----------|--------|--------------------------|
| Locus of Control | Rotter (1954), *Psychological Monographs* | The car metaphor, the two-branch routing, the focus on "choice" as the fundamental unit of agency |
| Growth Mindset | Dweck (2006), *Mindset* | The follow-up question about what made things go well — framing effort and adaptation as causally explanatory |
| Psychological Entitlement | Campbell et al. (2004) | Questions that trace behavior and feeling rather than self-report ("where did your energy go?" not "do you feel entitled?") |
| Organizational Citizenship Behavior | Organ (1988) | The "what counts?" branch that reframes invisible contributions as deliberate giving |
| Self-Transcendence | Maslow (1969), *The Farther Reaches of Human Nature* | The widening-circles structure of Axis 3 opening question |
| Perspective-Taking | Batson (2011), *Altruism in Humans* | The Axis 3 follow-up questions that ask whether awareness changed *action*, not just cognition |

---

## What I'd Improve With More Time

**Longitudinal state.** The most powerful version of this tool would show employees their signal patterns across 20–30 sessions. The single-session summary is useful; a chart of "your Axis 1 over the past month" is transformative. The tree is already designed for this — every signal is tagged — but the display layer doesn't exist yet.

**Question rotation.** With 44 nodes, an employee who uses this daily will see some questions repeatedly within two weeks. A small library of 2–3 question variants per node, rotated pseudo-randomly (but deterministically, based on session count), would extend the useful life without touching the tree structure.

**The in-between states.** The biggest weakness in the current design is that the "neutral" employee — the one who had a middling day with no strong signal in any direction — sometimes gets routed through branches that feel slightly mismatched. Adding an explicit "middling" or "mixed" path to each axis would improve fidelity without much complexity.

**Tone calibration.** Some of the reflection texts lean slightly toward the "wise colleague" end; a few still feel a touch therapeutic. A second pass with the specific constraint of "write as a peer, not a counselor" would sharpen them.
