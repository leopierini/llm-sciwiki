---
type: claim
title: "Claim: Sleep spindle density predicts memory consolidation"
created: 2024-03-14
updated: 2024-03-16
tags: [sleep, memory, spindles]
evidence_level: 3
confidence: moderate
replication_status: mixed
---

# Claim: Higher sleep spindle density during post-learning sleep predicts better declarative memory consolidation

**Confidence:** Moderate
**Evidence Level:** 3 (observational correlation, supported by RCT mediation)
**Replication Status:** Supported by independent causal evidence (not a direct replication)

## Evidence Summary

An observational study (Chen, 2023) found that spindle density correlates with 24-hour recall improvement (r=0.43). An RCT (Rodriguez, 2024) showed that experimentally enhancing spindles improved memory, with mediation analysis confirming spindles accounted for 62% of the benefit. Together, these provide converging evidence from both correlational and causal paradigms.

## Supporting Evidence

| Source | Design | Sample | Effect Size | p-value | Notes |
|--------|--------|--------|-------------|---------|-------|
| [[sources/chen-2023-sleep-memory]] | Observational | n=120 | r=0.43 | <0.001 | Correlation; beta=0.38 after covariates |
| [[sources/rodriguez-2024-spindle-stimulation]] | RCT (mediation) | n=84 | 62% mediated | 0.008 | Causal support via mediation analysis |

## Contradicting / Complicating Evidence

Kumar (2025) found that the causal mediation pathway (spindle density → memory) was NOT significant in the full sample (p=0.31), only in a low-baseline spindle density subgroup (38% mediated, p=0.04). This suggests the correlational relationship may be moderated by baseline spindle activity — the correlation may be strongest in individuals with suboptimal spindle density.

## Effect Size Range

- **Range:** r = 0.38-0.43 (correlational); mediation varies by subgroup (38-62%)
- **Typical:** Moderate effect, possibly moderated by baseline spindle density
- **Heterogeneity:** Moderate (mediation significant in Rodriguez but not in Kumar full sample)

## Related Claims

- [[claims/claim-spindle-enhancement-improves-memory]] — extends this (if spindles predict memory, then enhancing spindles should improve memory)

## Open Questions

- Does this hold in older adults where spindle activity declines? See [[questions/question-spindles-aging]]
- Is the effect specific to declarative memory, or does it extend to procedural/emotional memory?
- What is the dose-response relationship between spindle density and memory benefit?
- Is the correlation moderated by baseline spindle density? (suggested by Kumar, 2025 subgroup analysis)

## History

- 2024-03-14: Claim created based on [[sources/chen-2023-sleep-memory]]. Initial confidence: weak (single observational study).
- 2024-03-15: Confidence upgraded from weak to moderate after [[sources/rodriguez-2024-spindle-stimulation]] provided causal support via mediation analysis in an RCT.
- 2024-03-16: Evidence complicated by [[sources/kumar-2025-spindle-replication]] — full-sample mediation not significant, but subgroup mediation (low baseline) partially supports. Confidence remains moderate but with noted caveats about baseline moderation.
