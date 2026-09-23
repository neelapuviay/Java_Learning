---
name: doc-kb-writer
description: Persists generated technical deep dives into the repository as Markdown and interactive HTML documents, compiling progressive disclosure markers and updating the knowledge graph.
---

# Documentation & Knowledge Base Writer Skill

This skill ensures that all explanations generated during tutoring sessions are persistently captured in the repository, making future queries faster, cross-linked, and compoundable.

## Workflow

1. **Document Storage Locations**:
   - Technical Markdown Guides: `docs/concepts/<topic_slug>.md`
   - Interactive HTML Modules: `src/htmlDocuments/concurrent collections/<TopicName>_Deep_Dive.html` or `src/htmlDocuments/collections/`

2. **Compiling Interactive HTML**:
   To render an interactive HTML page with hover tooltips and popovers from `[[concept]]` markers:
   ```bash
   python3 .agents/scripts/render_html_deepdive.py --out "src/htmlDocuments/concurrent collections/<TopicName>_Deep_Dive.html"
   ```

3. **Updating the Knowledge Graph**:
   Whenever a new concept deep dive is written, register it into `.agents/knowledge_graph.json`:
   ```bash
   python3 .agents/scripts/kb_graph.py add \
     --id "<concept-slug>" \
     --name "<Concept Display Name>" \
     --summary "<1-sentence summary for tooltips>" \
     --category "<Category>" \
     --prereqs "<prereq1,prereq2>" \
     --doc "<relative/path/to/doc.html>" \
     --viz "<python_tutor|thread_lifecycle|visualgo|custom_svg>"
   ```

4. **Bi-directional Linking**:
   - Check if other documents reference this newly documented concept as a stub.
   - Update those links so the entire repository forms an interconnected, navigable study portal.
