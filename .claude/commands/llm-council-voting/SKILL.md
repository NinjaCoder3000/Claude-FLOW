---
name: "LLM Council Voting"
description: "Implement Byzantine fault-tolerant voting protocols for distributed LLM decision-making. Handles malicious/faulty consensus members."
---

# 🗳️ LLM Council Voting

Byzantine fault-tolerant voting for councils of language models with malicious actor detection.

## Voting Protocols

### Practical Byzantine Fault Tolerance (PBFT)

- **Tolerance**: Up to f < n/3 faulty members
- **Example**: 7 members tolerate 2 faulty
- **Stages**: Pre-prepare → Prepare → Commit
- **Guarantee**: Strong consistency

### Raft Consensus

- **Leader-based**: One council leader
- **Tolerance**: Up to f < n/2 faulty members
- **Use Case**: Replicated state machines
- **Implementation**: Log-based voting

### Gossip Protocol

- **Eventual Consistency**: Asynchronous voting
- **Tolerance**: f < n faulty (but detectable)
- **Latency**: O(log n) rounds
- **Best For**: Large councils (50+ members)

## Usage

```typescript
import { CouncilVoting } from '@claude-flow/llm-council-voting';

// PBFT voting (default)
const pbftVoting = new CouncilVoting({
  protocol: 'pbft',
  memberCount: 7,
  faultyTolerance: 2
});

const result = await pbftVoting.vote({
  proposal: 'Add OAuth2 authentication',
  members: [
    { id: 'model-1', decision: 'yes', confidence: 0.95 },
    { id: 'model-2', decision: 'yes', confidence: 0.87 },
    { id: 'model-3', decision: 'no', confidence: 0.72 },
    { id: 'model-4', decision: 'yes', confidence: 0.91 },
    { id: 'model-5', decision: 'abstain', confidence: 0.5 },
    { id: 'model-6', decision: 'yes', confidence: 0.89 },
    { id: 'model-7', decision: 'no', confidence: 0.68 }
  ]
});

console.log(result.consensus);        // 'approved'
console.log(result.confirmCount);     // 5 votes
console.log(result.faultyDetected);   // []
console.log(result.certainty);        // 0.89
```

## Malicious Actor Detection

```typescript
const voting = new CouncilVoting({
  protocol: 'pbft',
  memberCount: 5,
  detectMalicious: true,
  deviance_threshold: 2.0 // Std devs from mean
});

const result = await voting.vote({
  proposal: proposal,
  members: councilMembers
});

if (result.faultyDetected.length > 0) {
  console.warn('Faulty members detected:', result.faultyDetected);
  // Can quarantine or downweight faulty members
}
```

## Voting Strategies

| Strategy | Consensus | Speed | Best For |
|----------|-----------|-------|----------|
| PBFT | Strong | Slow | Small councils, high stakes |
| Raft | Strong | Medium | State machine replication |
| Gossip | Eventual | Fast | Large councils, web scale |
| Weighted | Configurable | Medium | Domain-specific voting |
| Quorum | Configurable | Fast | Flexible thresholds |

## Confidence Scoring

Each vote includes confidence [0.0-1.0]:

```typescript
// High confidence = More influence
members: [
  { id: 'expert', decision: 'yes', confidence: 0.98 },  // Heavy weight
  { id: 'novice', decision: 'yes', confidence: 0.55 }   // Light weight
]
```

Result weights votes by confidence when computing consensus strength.

## CLI Integration

```bash
# Run a vote
npx claude-flow council vote --proposal "Implement microservices" \
  --members model-1,model-2,model-3 \
  --protocol pbft

# Show voting history
npx claude-flow council history --filter "architecture"

# Analyze voting patterns
npx claude-flow council analyze --metric "disagreement-frequency"
```

## Performance

- PBFT: O(n²) message complexity
- Raft: O(n) message complexity  
- Gossip: O(log n) rounds to convergence
- Vote processing: <500ms for consensus
- Malicious detection: <1s for n=100

---

**Key Insight**: Byzantine voting handles the case where some LLM "members" give deliberately misleading advice (faulty/compromised models).
