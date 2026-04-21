# Daily Reflection Tree — DT Fellowship Submission

A deterministic end-of-day reflection agent. No LLM at runtime. The tree is the product.

---

## What's Here

```
/tree/
  reflection-tree.json     ← The tree data (44 nodes, fully traced)
  tree-diagram.md          ← Mermaid flowchart of all paths

/agent/
  agent.py                 ← Python CLI agent (loads tree, walks deterministically)

/transcripts/
  persona-1-transcript.md  ← Rohan: external / entitlement / self-centric path
  persona-2-transcript.md  ← Priya: internal / contribution / altrocentric path

write-up.md                ← Design rationale (2 pages)
README.md                  ← This file
```

---

## Running the Agent

**Requirements:** Python 3.7+, no external dependencies.

```bash
python3 agent/agent.py
# or explicitly point to tree file:
python3 agent/agent.py tree/reflection-tree.json
```

Works in any terminal with ANSI color support (macOS Terminal, Linux, Windows Terminal).

---

## Reading the Tree (Without Running Code)

The tree is a JSON array of nodes. Each node has:

| Field | Description |
|-------|-------------|
| `id` | Unique identifier |
| `parentId` | Structural parent (builds the hierarchy) |
| `type` | `start`, `question`, `decision`, `reflection`, `bridge`, `summary`, `end` |
| `text` | What the employee sees. `{NODE_ID.answer}` is replaced at runtime. |
| `options` | For questions: list of `{value, label}`. For decisions: list of `{condition, target}` routing rules. |
| `target` | Explicit jump target (overrides child lookup). |
| `signal` | State tally written when this node is visited: `axis1:internal`, `axis2:contribution`, etc. |

**To trace a path manually:**
1. Start at `START`
2. Follow `target` or find the child node whose `parentId` matches the current node
3. At `decision` nodes, match the parent question's answer against `condition` rules
4. Accumulate signals. At `SUMMARY_NODE`, use axis dominants to pick a `combined` template.

---

## Tree Statistics

| Metric | Count | Requirement |
|--------|-------|-------------|
| Total nodes | 44 | 25+ ✓ |
| Question nodes | 12 | 8+ ✓ |
| Decision nodes | 12 | 4+ ✓ |
| Reflection nodes | 15 | 4+ ✓ |
| Bridge nodes | 2 | 2+ ✓ |
| Axes covered | 3 | All 3 ✓ |
| Summary nodes | 1 | 1+ ✓ |
| Summary combined templates | 8 | (one per axis combination) |

---

## Design Principles

1. **No LLM at runtime.** The agent reads JSON, matches strings, tallies integers, and substitutes template variables. That's all.

2. **Deterministic.** Same answers → same path → same reflection. Every time.

3. **No moralizing.** The reflections on the "external/entitlement/self" end don't grade the employee. They name what they saw and offer one thought. The tone is: wise colleague, not HR chatbot.

4. **The axes build on each other.** Axis 1 establishes agency. Axis 2 asks what you did *with* that agency (or its absence). Axis 3 asks who you were doing it *for*. The bridge nodes name this progression explicitly.

5. **Fixed options, genuine range.** Every question's options are designed so a real person on either end of the spectrum can answer honestly without being forced into an inauthentic choice.

---

## Psychological Framework

| Axis | Spectrum | Sources |
|------|----------|---------|
| Locus | External → Internal | Rotter (1954) Locus of Control; Dweck (2006) Growth Mindset |
| Orientation | Entitlement → Contribution | Campbell et al. (2004) Psychological Entitlement; Organ (1988) OCB |
| Radius | Self-Centric → Altrocentric | Maslow (1969) Self-Transcendence; Batson (2011) Perspective-Taking |
