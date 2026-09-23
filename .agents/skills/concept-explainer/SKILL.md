---
name: concept-explainer
description: Formulates pedagogical concept deep dives using cognitive learning strategies (Dunlosky 6, Feynman technique, plain English, "why" elaboration, concrete code, practice problems, interview traps).
---

# Pedagogical Concept Explainer Skill

This skill encodes evidence-based learning strategies (Dunlosky et al., cognitive psychology, Feynman technique) into every deep-dive explanation.

## Pedagogical Structure

Every deep dive must contain these 6 sections in exact order:

### 1. What Problem This Solves (The Motivation)
- **Constraint**: Exactly 1 paragraph, zero jargon.
- Use a concrete real-world analogy (e.g. bank accounts, post office boxes, traffic lights).
- State what catastrophic failure or bottleneck occurs if this concept did not exist.

### 2. The Core Mechanism & Elaboration ("Why", not just "What")
- Explain step-by-step how the components interact.
- Elaborate on **why** each design choice was made (e.g., *"Why volatile here specifically? Because without volatile, Core 1's write stays in its L1 cache and Core 2 reads stale memory forever"*).
- Every unfamiliar prerequisite term must be wrapped in `[[concept]]` placeholder markers.
- Employ **dual coding**: pair text with a visual mental model, diagram, or table.

### 3. Concrete Runnable Code Example
- Write a clean, self-contained Java class with a `public static void main` method.
- Clearly demonstrate the problem (e.g. race condition) or the exact behavior of the class.
- Provide step-by-step comments explaining what happens at runtime.

### 4. Interactive Visualization
- Generate a Python Tutor Java Visualizer deep link using the script:
  ```bash
  python3 .agents/scripts/python_tutor_url.py --markdown --title "Step through live execution in Python Tutor"
  ```
- Link to relevant visualizers from `visualizer-dispatcher`.
- Include an ASCII, SVG, or Mermaid diagram illustrating internal memory layout.

### 5. Hands-on Practice & LeetCode Patterns
- Useful API methods to know by heart.
- Provide 3 real LeetCode or system design coding problems:
  - **Easy**: Baseline API usage.
  - **Medium**: Concurrency or data structure design problem.
  - **Hard**: Production scenario or lock-free data structure design.

### 6. Interview Traps & Gotchas
- The specific subtle misunderstandings that cause candidates to fail interviews.
- Format as:
  - **The Myth**: What candidates mistakenly say (e.g., *"ConcurrentHashMap never locks anything"*).
  - **The Reality**: The exact JVM truth (e.g., *"It locks the head node of the bin upon collision"*).
