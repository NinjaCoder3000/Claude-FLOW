---
name: "LLM Council Arbitration"
description: "Resolve disagreements between council members through systematic debate, evidence presentation, and meta-consensus protocols."
---

# ⚖️ LLM Council Arbitration

Resolve council member disagreements through structured debate and evidence-based arbitration.

## Arbitration Modes

### 1. Adversarial Debate
- **Setup**: Advocate vs Skeptic exchange arguments
- **Rounds**: 3-5 alternating arguments
- **Judge**: Neutral member evaluates
- **Verdict**: Judge's final decision

### 2. Evidence Presentation
- **Round 1**: Pro side presents evidence
- **Round 2**: Con side presents counterevidence
- **Round 3**: Expert evaluation of evidence quality
- **Result**: Data-driven decision

### 3. Meta-Consensus
- **Step 1**: Members vote on original proposal
- **Step 2**: If deadlocked, debate the disagreement itself
- **Step 3**: Vote on revised proposal
- **Outcome**: Consensus or documented dissent

## Usage

```typescript
import { CouncilArbitration } from '@claude-flow/llm-council-arbitration';

const arbitration = new CouncilArbitration({
  mode: 'adversarial-debate',
  roundCount: 3,
  timePerRound: 30000,
  judgeRole: 'neutral-evaluator'
});

const result = await arbitration.resolve({
  disagreement: {
    proposal: 'Implement caching layer',
    advocate: { member: 'model-opus', position: 'yes', reasoning: '...' },
    skeptic: { member: 'model-sonnet', position: 'no', reasoning: '...' }
  },
  arbiter: 'model-haiku'
});

console.log(result.finalVerdict);     // 'approved' | 'rejected' | 'needs-revision'
console.log(result.convincingnessScore); // 0.0-1.0
console.log(result.debate);           // Full debate transcript
console.log(result.arbiterNotes);     // Arbitration rationale
```

## Debate Structure

```
Round 1: Advocate Opening Statement (5 min)
  ↓
Round 2: Skeptic Opening Statement (5 min)
  ↓
Round 3: Advocate Rebuttal (4 min)
  ↓
Round 4: Skeptic Rebuttal (4 min)
  ↓
Round 5: Judge Deliberation & Verdict (6 min)
```

## Evidence Quality Scoring

```typescript
// System evaluates evidence on:
// - Relevance (0-1)
// - Credibility (0-1)
// - Completeness (0-1)
// - Recency (0-1)

evidenceScore = (relevance + credibility + completeness + recency) / 4
```

Higher score = More persuasive argument

## Advanced: Multi-Round Arbitration

```typescript
const arbitration = new CouncilArbitration({
  mode: 'meta-consensus',
  maxRounds: 3,
  convergenceThreshold: 0.8
});

let decision = await arbitration.arbitrate({
  proposal: proposal,
  council: councilMembers
});

// If not converged, run another round
while (decision.convergence < 0.8 && decision.round < 3) {
  decision = await arbitration.refine({
    previousVerdict: decision,
    focusArea: decision.remainingDisagreement
  });
}
```

## Outcome Types

| Outcome | Description | Action |
|---------|-------------|--------|
| **Consensus** | Supermajority agreement | Execute decision |
| **Weak Consensus** | Simple majority with reservations | Proceed with caution |
| **Disagreement** | Persistent 50/50 split | Escalate or table |
| **Deadlock** | Unable to converge | Refer to human decision |

## Integration Example

```typescript
// In a code review workflow
const council = new LLMCouncil({
  members: [
    { role: 'security-expert', model: 'opus' },
    { role: 'performance-expert', model: 'sonnet' },
    { role: 'maintainability-expert', model: 'haiku' }
  ]
});

const codeReview = await council.reviewCode(sourceCode);

if (codeReview.disagreement > 0.3) {
  // Trigger arbitration
  const arbitration = new CouncilArbitration({ mode: 'evidence-based' });
  const resolvedVerdict = await arbitration.resolve({
    disagreement: codeReview.disputes[0],
    arbiter: 'opus' // Strongest model as tiebreaker
  });
  
  return resolvedVerdict;
}
```

## Best Practices

1. **Odd Councils**: Use 3, 5, or 7 members (easier to break ties)
2. **Role Diversity**: Mix different expertise areas
3. **Escalation Path**: Know when to defer to humans
4. **Documentation**: Log all arbitrations for learning
5. **Timeout**: Set hard limits on deliberation time

---

**Philosophy**: When intelligent systems disagree, the disagreement itself is valuable data. Arbitration extracts maximum insight from conflict.
