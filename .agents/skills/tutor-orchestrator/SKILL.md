---
name: tutor-orchestrator
description: Coordinates the 6-stage deep-dive tutor pipeline (Decomposition, Prerequisite Tracing, Grounding Verification, Pedagogical Deep Dive, Visualizer Dispatching, and KB Persistence) for Java, Concurrency, Spring Boot, and System Design topics.
---

# Tutor Orchestrator Workflow

Use this master orchestrator workflow whenever the user asks for a conceptual explanation, study guide, deep dive, or interview prep session in this repository.

## The 6-Stage Execution Protocol

When invoked with a topic (e.g. `ConcurrentHashMap`, `ReentrantLock`, `Virtual Threads`, `Kafka Partitions`):

### 1. Stage 1: Decompose Topic
- Activate the `topic-decomposer` skill.
- Produce a structured subtopic tree (Problem Solved → Core Mechanics → Internals → Memory & Concurrency → Failure Modes & Trade-offs).
- Present this tree first to orient the learner before producing full text.

### 2. Stage 2: Trace Prerequisites (RPKT)
- Activate the `prereq-walker` skill.
- Run `python3 .agents/scripts/kb_graph.py prereqs "<topic>"` to retrieve foundational requirements.
- Cross-reference with existing repo files (`src/htmlDocuments/`, `src/concept/`).
- If already documented in the workspace, link directly to it.
- If not yet documented, mark it with `[[concept]]` placeholders.

### 3. Stage 3: Ground Facts & Versions
- Activate the `grounding-verifier` skill.
- Identify any version-dependent (Java 8 vs 11 vs 17 vs 21), numeric (thresholds, capacities), or concurrency guarantees.
- Verify via web search / Javadoc before writing. Cite verified specifications.

### 4. Stage 4: Construct Pedagogical Deep Dive
- Activate the `concept-explainer` skill.
- Draft the deep-dive following the 6 pedagogical sections:
  1. What problem this solves (1 paragraph, plain English, concrete analogy).
  2. The mechanism ("why" elaboration, dual coding, `[[concept]]` placeholders).
  3. Concrete runnable code snippet.
  4. Visualizer link & diagram.
  5. Hands-on practice (API methods + Easy/Medium/Hard LeetCode problems).
  6. Interview traps (common myths vs actual JVM reality).

### 5. Stage 5: Dispatch Visualizations
- Activate the `visualizer-dispatcher` skill.
- Generate a live Python Tutor deep link using `python3 .agents/scripts/python_tutor_url.py`.
- Link to relevant interactive visualizers (Java Concurrent Animated, Thread Lifecycle Visualizer, VisuAlgo).
- Generate SVG or Mermaid diagrams for memory/bucket layouts.

### 6. Stage 6: Persist & Update Knowledge Base
- Activate the `doc-kb-writer` skill.
- Persist the markdown/HTML documentation into the workspace.
- Register newly documented concepts into `.agents/knowledge_graph.json` using `python3 .agents/scripts/kb_graph.py add ...`.
