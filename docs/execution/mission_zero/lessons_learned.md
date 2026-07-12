# Lessons Learned Framework

*The retrospective template, filled after the mission closes. Iron rule: **no
recommendation without cited mission evidence** — an MZ-issue id, a journal entry,
or a metric value. An idea without evidence goes to "Future work" as a hypothesis,
clearly labeled.*

## How to fill it

For each finding, in any category:

```markdown
### <category>-<n>: <one-line finding>
- Evidence: <MZ-ids / journal session refs / metric values>
- What happened: <one honest paragraph>
- Implication: <what it means for the platform or the science>
- Recommendation: <smallest change that addresses it>
- Effort: <sessions/days>  Priority: <Critical|High|Medium|Low>
- Founder verdict: <accept | reject | defer-with-trigger>   <!-- filled at review -->
```

## Categories

### 1. Research
*What conducting the study was actually like: workflow order, decision quality,
fatigue, PRISMA fit, whether the staged semantics (ADR-0022) held up in practice.*

### 2. Engineering
*Bugs and near-misses: everything classed Bug or Missing validation in the issue
register, plus anything the hard metrics caught.*

### 3. UX
*Friction with the tools: prompts, output, help, error messages — the UX-classed
issues plus the baseline metrics that quantify friction (decision time, skip rate,
interruptions).*

### 4. Scientific methodology
*Threats to validity discovered in use: abstract-only limits met in practice,
exclusion-taxonomy fit, uncertain-duplicate quality, verification failures and what
they revealed about provenance.*

### 5. Governance
*Did the protocol, checklist, and incident guide earn their keep? Which procedures
were followed, skipped, or fought? (A skipped procedure is evidence about the
procedure, not only about the operator.)*

### 6. Architecture
*Only changes justified by evidence.* Candidates already registered pre-mission —
eligibility stage implementation (ADR-0022 §5), export command, multi-reviewer (D2)
— get confirmed, resized, or rejected here **based on what the mission showed**,
alongside anything new the mission surfaced.

### 7. Future work
*Hypotheses and ideas from the journal's "Ideas" sections that lack mission
evidence — preserved honestly as speculation, prioritized never higher than
evidence-backed items.*

## Required closing sections

1. **Metrics report** — every hard metric vs target; every baseline metric with its
   value (the numbers Mission Zero was designed to produce).
2. **Command usage** — most-used, never-used (a never-used command is a finding:
   remove-or-document decision per ADR-0020 deprecation policy).
3. **Completion audit** — the [completion criteria](completion_criteria.md), each
   checked with its evidence.
4. **Implementation queue** — accepted recommendations only, ordered, sized; this
   becomes the input to the first post-mission planning session. Nothing enters the
   codebase from this retrospective without appearing here first.
