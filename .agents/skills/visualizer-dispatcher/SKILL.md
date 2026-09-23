---
name: visualizer-dispatcher
description: Routes concepts to interactive visualization tools (Python Tutor deep links, Java Concurrent Animated, Thread Lifecycle Visualizer, VisuAlgo) or generates custom SVG/Mermaid diagrams.
---

# Visualizer Dispatcher Skill

This skill pairs technical concepts with appropriate visual mental models and generates interactive links.

## Visualization Tool Routing Table

| Tool | Focus & Coverage | How to Dispatch |
|---|---|---|
| **[Python Tutor Java Visualizer](https://pythontutor.com)** | Step-by-step heap, stack frame, and pointer visualization for Java execution. | Run `.agents/scripts/python_tutor_url.py` with the Java snippet to generate a direct deep link: `https://pythontutor.com/visualize.html?via=ai#code=...&mode=display&py=java` |
| **[Java Concurrent Animated](https://github.com/manchi/java_concurrency_algorithms)** | Live animated concurrency primitives (`Semaphore`, `ReentrantLock`, `ReadWriteLock`, `CountDownLatch`, `CyclicBarrier`). | Embed reference link and specify the exact demo screen/class to run. |
| **[Thread Lifecycle Visualizer](https://github.com/PramithaMJ/thread-lifecycle-visualizer)** | Thread state transitions (New → Runnable → Blocked → Waiting → Terminated) and race conditions. | Embed link for thread state machine and deadlock/livelock scenarios. |
| **[VisuAlgo](https://visualgo.net)** | Pure DSA foundations: Hash collision chains, Red-Black trees, BST balancing, heaps, graphs. | Embed deep link to the relevant VisuAlgo module (e.g., `visualgo.net/en/hashtable`). |
| **Custom SVG / Mermaid** | Specific internal memory layouts not covered by generic tools (e.g. `ConcurrentHashMap` bucket bins, CAS loops, `ForwardingNode`). | Generate inline SVG or Mermaid diagram directly in the markdown or HTML. |

## Python Tutor URL Generation Command

```bash
python3 .agents/scripts/python_tutor_url.py --markdown --code "public class Main { public static void main(String[] args) { ... } }"
```

## Custom Diagram Guidelines
- For HashMap / ConcurrentHashMap: draw the table array indices `[0] ... [15]`, the node pointers `next`, and highlight treeification or lock status.
- For CAS: draw the CPU cache, main memory address, expected value, and new value comparison branch.
