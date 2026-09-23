---
name: prereq-walker
description: Traces prerequisite concepts using Recursive Prerequisite Knowledge Tracing (RPKT), checks repository documentation, and marks unfamiliar concepts with progressive disclosure tags.
---

# Prerequisite Graph Walker (RPKT)

This skill implements **Recursive Prerequisite Knowledge Tracing (RPKT)** to ensure the learner is never exposed to unexplained prerequisite concepts without a clear path to explore them.

## Workflow

1. **Query Prerequisites**:
   Run the CLI tool:
   ```bash
   python3 .agents/scripts/kb_graph.py prereqs "<concept_name>"
   ```
   Or query a specific concept:
   ```bash
   python3 .agents/scripts/kb_graph.py query "<concept_name>"
   ```

2. **Categorize Prerequisites**:
   For every prerequisite identified:
   - **Documented**: If `doc_path` exists, create a direct relative markdown link to the existing document: `[volatile](file:///Users/Vinay_Neelapu/Workspace/personal/java_learning/Java_Learning/src/htmlDocuments/collections/05-concurrency.html#chm)`.
   - **Undocumented (Stub)**: Wrap the term in double brackets `[[term]]` (e.g. `[[volatile]]`, `[[CAS]]`, `[[happens-before]]`).

3. **Progressive Disclosure Rules**:
   - Never write a 5-paragraph tangent explaining a prerequisite inside the main concept.
   - Use progressive disclosure: provide a 1-sentence plain-English summary inline or in a footnote/popover, leaving the full drill-down for when the user clicks or asks for that subtopic.
   - When compiling to HTML, `.agents/scripts/render_html_deepdive.py` turns `[[term]]` into an interactive tooltip popover with definition and links.
