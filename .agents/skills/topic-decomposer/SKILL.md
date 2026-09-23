---
name: topic-decomposer
description: Decomposes any technical topic in Java, Spring Boot, Concurrency, or System Design into a hierarchical subtopic tree and prerequisite progression before writing deep explanations.
---

# Topic Decomposer Skill

This skill ensures the agent never dumps an unorganized wall of text. It generates the subtopic tree **first** so the learner sees the entire mental map.

## Decomposition Template

When a topic is received (e.g. `ConcurrentHashMap`), output the subtopic tree using this schema:

```markdown
### 🗺️ Topic Breakdown: [Topic Name]

1. **Problem Context & Motivation**: What exact bottleneck or failure mode does this solve that simpler tools failed at?
2. **Core Architectural Design**: High-level data structure layout or component topology.
3. **Internal Mechanics & Algorithms**: Specific operations (e.g., bin lookup, CAS insertion, resizing, lock striping).
4. **Memory & Thread Semantics**: Visibility (`volatile`), ordering (`happens-before`), CPU cache line behavior, atomic primitives.
5. **Edge Cases & Failure Modes**: Collisions, high contention, resize storms, deadlocks/livelocks.
6. **Comparison & Trade-offs**: When to use this vs alternatives (e.g., `ConcurrentHashMap` vs `Collections.synchronizedMap` vs `ConcurrentSkipListMap`).
```

## Example: `ConcurrentHashMap` Decomposition
- **Subtopic 1**: What problem it solves (Hashtable global bottleneck vs ConcurrentHashMap throughput).
- **Subtopic 2**: Bucket array design & hash bin organization.
- **Subtopic 3**: CAS insertion on empty bins + synchronized per-bin locking on collisions.
- **Subtopic 4**: Cooperative multi-threaded resizing via `ForwardingNode`.
- **Subtopic 5**: Memory visibility (`volatile` node value & next pointers) and lock-free reads.
- **Subtopic 6**: LongAdder-style size tracking (`CounterCell`).
- **Subtopic 7**: Weakly consistent iteration vs fail-fast iteration.
- **Subtopic 8**: Direct comparison with `Hashtable` and `Collections.synchronizedMap`.

## Instruction
Always present this tree to the learner, indicate which subtopic is being explored, and provide the opportunity to focus on a specific node.
