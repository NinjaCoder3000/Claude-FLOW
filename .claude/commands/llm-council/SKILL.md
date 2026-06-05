---
name: "LLM Council"
description: "Orchestrate multi-LLM decision-making councils with voting, consensus, and adversarial review patterns. Use when you need collective intelligence from multiple models."
---

# 🏛️ LLM Council

Coordinate multiple LLM instances as a decision-making council with built-in voting, consensus protocols, and adversarial review.

## What This Skill Does

- **Multi-Model Voting**: Proposals voted on by council members
- **Consensus Building**: Achieve quorum-based decisions
- **Adversarial Review**: Built-in disagreement detection
- **Argument Synthesis**: Merge findings into coherent decisions
- **Council Roles**: Advocate, Judge, Skeptic, Synthesizer

## Usage

```typescript
import { LLMCouncil } from '@claude-flow/llm-council';

const council = new LLMCouncil({
  members: [
    { role: 'advocate', model: 'claude-opus' },
    { role: 'skeptic', model: 'claude-sonnet' },
    { role: 'judge', model: 'claude-haiku' }
  ],
  votingStrategy: 'simple-majority',
  consensusThreshold: 0.66
});

// Propose and vote
const decision = await council.deliberate({
  proposal: 'Implement caching layer for API',
  perspectives: ['performance', 'complexity', 'maintainability']
});

console.log(decision.verdict); // 'approved' | 'rejected' | 'needs-revision'
console.log(decision.votes);   // Individual votes
console.log(decision.summary); // Synthesized reasoning
```

## Council Roles

| Role | Model | Purpose |
|------|-------|---------|
| **Advocate** | Opus | Argues FOR the proposal |
| **Skeptic** | Sonnet | Argues AGAINST the proposal |
| **Judge** | Haiku | Weighs both sides |
| **Synthesizer** | Sonnet | Merges conclusions |

## Decision Strategies

- `simple-majority`: 50%+ votes wins
- `supermajority`: 66%+ votes required
- `consensus`: 100% agreement required
- `weighted`: Role-based vote weights
- `byzantine-resistant`: Tolerates faulty members

## Examples

### Code Review Council
```typescript
const reviewCouncil = new LLMCouncil({
  members: [
    { role: 'security-reviewer', model: 'claude-opus' },
    { role: 'performance-reviewer', model: 'claude-sonnet' },
    { role: 'maintainability-reviewer', model: 'claude-haiku' }
  ]
});

const verdict = await reviewCouncil.reviewCode(sourceCode);
```

### Architectural Decision Council
```typescript
const archCouncil = new LLMCouncil({
  votingStrategy: 'supermajority',
  consensusThreshold: 0.75
});

const decision = await archCouncil.deliberate({
  proposal: 'Migrate to event sourcing',
  criteria: ['scalability', 'complexity', 'testing-difficulty']
});
```

## Best Practices

1. **Odd Member Counts**: Use 3, 5, or 7 members (avoid ties)
2. **Diverse Models**: Mix different capabilities
3. **Clear Criteria**: Define voting dimensions upfront
4. **Timeout Handling**: Set reasonable timeouts per member
5. **Logging**: Record all votes for audit trail

## Integration with Claude Flow

```bash
# Use in swarm for architectural decisions
npx claude-flow@v3alpha swarm init --council-enabled

# Run council deliberation
npx claude-flow@v3alpha council deliberate --proposal "[your-proposal]"

# Check voting history
npx claude-flow@v3alpha council history --format json
```

## Advanced: Custom Council Configurations

```typescript
const customCouncil = new LLMCouncil({
  members: [
    { 
      role: 'domain-expert', 
      model: 'claude-opus',
      systemPrompt: 'You are an expert in distributed systems...',
      weight: 1.5 // Extra influence
    },
    {
      role: 'pragmatist',
      model: 'claude-sonnet',
      weight: 1.0
    }
  ],
  votingStrategy: 'weighted',
  dissentThreshold: 0.2, // Flag if disagreement > 20%
  explainability: true   // Require reasoning from all votes
});
```

## Performance Benchmarks

- Council deliberation: 2-5 seconds (3 members)
- Consensus detection: <500ms
- Vote synthesis: <1 second

---

**Pro Tip**: Use councils for high-stakes decisions (architecture, security, refactoring) where multiple perspectives prevent blind spots.
