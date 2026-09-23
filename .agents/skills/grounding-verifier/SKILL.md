---
name: grounding-verifier
description: Verifies version-specific behavior, numeric thresholds, and concurrency guarantees via targeted web searches and official Javadoc citations before finalizing explanations.
---

# Grounding & Verification Skill

This skill eliminates hallucinations and outdated explanations by gating external verification on version-sensitive or numeric claims.

## Triggers for Verification

Always verify via web search or official JDK/Spring documentation if the explanation touches:
1. **Java Version Milestones**:
   - Java 8: HashMap/ConcurrentHashMap treeification, elimination of segment-locking in CHM, Metaspace replacing PermGen.
   - Java 9+: Compact Strings, Module system, reactive Flow API.
   - Java 11: ZGC introduction, HTTP Client.
   - Java 17: Sealed classes, pattern matching, LTS baseline.
   - Java 21: Virtual Threads (Project Loom), Sequenced Collections (`SequencedMap`, `SequencedSet`), Generational ZGC.
2. **Numeric Constants & Thresholds**:
   - `TREEIFY_THRESHOLD = 8`
   - `UNTREEIFY_THRESHOLD = 6`
   - `MIN_TREEIFY_CAPACITY = 64`
   - Default initial capacity = 16, default load factor = 0.75
3. **Locking & Concurrency Semantics**:
   - Intrinsic monitor locking vs AQS lock states.
   - Weakly consistent vs fail-fast iteration.
   - Non-blocking read guarantees in ConcurrentHashMap.

## Citation Format

When citing verified facts, include the source and version baseline:
> [!NOTE]
> **Verified Version Milestone (Java 8+)**: In Java 8, `ConcurrentHashMap` completely removed the Java 7 16-segment striping architecture in favor of a flat bucket array using CAS for empty bins and synchronized locking on bin heads (Source: OpenJDK `ConcurrentHashMap.java`).
