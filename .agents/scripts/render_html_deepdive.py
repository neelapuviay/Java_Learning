#!/usr/bin/env python3
"""
HTML Deep-Dive Renderer & Progressive Disclosure Compiler
Converts technical deep dives and concept markers [[concept]] into interactive HTML with tooltips and expandable drawers.
"""

import os
import re
import sys
import json
import html
import argparse
from pathlib import Path

KG_PATH = Path(__file__).resolve().parent.parent / "knowledge_graph.json"

def load_kg():
    if not KG_PATH.exists():
        return {"concepts": {}}
    with open(KG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def compile_progressive_markers(content: str, kg: dict) -> str:
    """
    Finds [[concept]] markers and replaces them with interactive HTML tooltips/drawers.
    """
    concepts = kg.get("concepts", {})
    
    # Map lowercase names to concept keys
    name_to_key = {}
    for cid, data in concepts.items():
        name_to_key[cid.lower()] = cid
        name_to_key[data.get("name", "").lower()] = cid
        
    def replace_tag(match):
        raw_tag = match.group(1).strip()
        tag_lower = raw_tag.lower().replace(" ", "-")
        
        cid = name_to_key.get(raw_tag.lower(), name_to_key.get(tag_lower))
        if cid and cid in concepts:
            cdata = concepts[cid]
            display_name = cdata.get("name", raw_tag)
            summary = html.escape(cdata.get("one_line_summary", "Prerequisite concept"))
            doc_link = cdata.get("doc_path", "")
            
            link_html = f'<a href="{doc_link}" class="drawer-link" target="_blank">View full notes →</a>' if doc_link else '<span class="drawer-stub">Topic stub in KB</span>'
            
            return f'''<span class="progressive-term" tabindex="0" title="{summary}">
  <span class="term-text">{display_name}</span>
  <span class="term-badge">prereq</span>
  <span class="term-popover">
    <strong>{display_name}</strong>
    <p>{summary}</p>
    {link_html}
  </span>
</span>'''
        else:
            # Concept not yet in KG
            return f'''<span class="progressive-term untracked" tabindex="0" title="Prerequisite concept to explore">
  <span class="term-text">{raw_tag}</span>
  <span class="term-badge">stub</span>
  <span class="term-popover">
    <strong>{raw_tag}</strong>
    <p>Prerequisite concept tagged for drill-down.</p>
  </span>
</span>'''

    return re.sub(r'\[\[(.*?)\]\]', replace_tag, content)

def generate_html_page(title: str, category: str, problem_solved: str, mechanism_html: str, 
                       code_snippet: str, python_tutor_url: str, visualizer_note: str,
                       practice_items: list, interview_traps: list, css_rel_path: str = "styles.css") -> str:
    
    practice_cards = ""
    for p in practice_items:
        diff_badge = f'<span class="badge badge-{p.get("badge", "amber")}">{p.get("difficulty", "Medium")}</span>'
        practice_cards += f'''
        <div class="card" style="margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <h4 style="margin:0;">{p.get("title", "")}</h4>
            {diff_badge}
          </div>
          <p style="margin:0; font-size:13px; color:var(--text-dim, #93A3BE);">{p.get("description", "")}</p>
        </div>'''

    traps_html = ""
    for t in interview_traps:
        traps_html += f'''
        <div class="trap-card">
          <div class="trap-question">⚠️ Trap: "{t.get("myth", "")}"</div>
          <div class="trap-reality"><strong>Reality:</strong> {t.get("reality", "")}</div>
        </div>'''

    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Deep Dive Tutor</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_rel_path}">
<style>
  :root {{
    --bg-main: #0B1120;
    --card-bg: #101B30;
    --border-color: #1E2E4A;
    --accent-coral: #F472B6;
    --accent-cyan: #38BDF8;
    --accent-green: #34D399;
    --accent-amber: #FBBF24;
    --text-main: #F1F5F9;
    --text-dim: #94A3B8;
  }}
  body {{
    background-color: var(--bg-main);
    color: var(--text-main);
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    padding: 24px;
    margin: 0;
  }}
  .container {{
    max-width: 880px;
    margin: 0 auto;
  }}
  .badge {{
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }}
  .badge-coral {{ background: rgba(244,114,182,0.15); color: #F472B6; border: 1px solid rgba(244,114,182,0.3); }}
  .badge-green {{ background: rgba(52,211,153,0.15); color: #34D399; border: 1px solid rgba(52,211,153,0.3); }}
  .badge-amber {{ background: rgba(251,191,36,0.15); color: #FBBF24; border: 1px solid rgba(251,191,36,0.3); }}
  .badge-cyan {{ background: rgba(56,189,248,0.15); color: #38BDF8; border: 1px solid rgba(56,189,248,0.3); }}
  
  .hero {{ margin-bottom: 32px; border-bottom: 1px solid var(--border-color); padding-bottom: 24px; }}
  h1 {{ font-size: 32px; font-weight: 800; margin: 12px 0; color: #FFFFFF; }}
  .lede {{ font-size: 16px; color: var(--text-dim); }}
  
  .section-block {{ margin-bottom: 40px; }}
  .section-title {{ font-size: 20px; font-weight: 700; color: #E2E8F0; margin-bottom: 14px; border-left: 4px solid var(--accent-cyan); padding-left: 12px; }}
  
  /* Progressive disclosure markers */
  .progressive-term {{
    position: relative;
    display: inline-block;
    border-bottom: 1.5px dotted var(--accent-cyan);
    color: #E0F2FE;
    cursor: pointer;
    font-weight: 500;
  }}
  .progressive-term .term-badge {{
    font-size: 9px;
    background: rgba(56,189,248,0.2);
    color: var(--accent-cyan);
    padding: 1px 4px;
    border-radius: 3px;
    margin-left: 2px;
    vertical-align: middle;
  }}
  .progressive-term .term-popover {{
    display: none;
    position: absolute;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    width: 260px;
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 12px;
    font-size: 12px;
    color: #CBD5E1;
    z-index: 100;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5);
  }}
  .progressive-term:hover .term-popover, .progressive-term:focus .term-popover {{
    display: block;
  }}
  .progressive-term .term-popover strong {{ color: #FFFFFF; display: block; margin-bottom: 4px; font-size: 13px; }}
  .progressive-term .term-popover p {{ margin: 0 0 8px 0; line-height: 1.4; }}
  .progressive-term .drawer-link {{ color: var(--accent-cyan); text-decoration: none; font-weight: 600; }}
  
  pre {{
    background: #0D1524;
    border: 1px solid var(--border-color);
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #E2E8F0;
  }}
  
  .btn-tutor {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #2563EB;
    color: #FFFFFF;
    text-decoration: none;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 18px;
    border-radius: 6px;
    transition: background 0.2s ease;
    margin-top: 10px;
  }}
  .btn-tutor:hover {{ background: #1D4ED8; }}
  
  .trap-card {{
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.25);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 12px;
  }}
  .trap-question {{ font-weight: 700; color: #FCA5A5; margin-bottom: 6px; font-size: 14px; }}
  .trap-reality {{ font-size: 13px; color: #FEE2E2; line-height: 1.5; }}
  
  .card {{
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 16px;
  }}
</style>
</head>
<body>
<div class="container">
  <div class="hero">
    <div style="display:flex; gap:8px; align-items:center; margin-bottom:12px;">
      <span class="badge badge-coral">{category}</span>
      <span class="badge badge-green">Tutor Deep-Dive</span>
    </div>
    <h1>{title}</h1>
    <p class="lede">{problem_solved}</p>
  </div>

  <div class="section-block">
    <div class="section-title">1. The Core Mechanism &amp; Why It Exists</div>
    <div>{mechanism_html}</div>
  </div>

  <div class="section-block">
    <div class="section-title">2. Concrete Runnable Example &amp; Live Step Execution</div>
    <pre><code>{html.escape(code_snippet)}</code></pre>
    <a href="{python_tutor_url}" target="_blank" class="btn-tutor">
      ▶ Step through this code live in Python Tutor
    </a>
    <p style="font-size:12px; color:var(--text-dim); margin-top:8px;">{visualizer_note}</p>
  </div>

  <div class="section-block">
    <div class="section-title">3. Hands-on Practice &amp; LeetCode Patterns</div>
    <div>{practice_cards}</div>
  </div>

  <div class="section-block">
    <div class="section-title">4. Interview Traps &amp; Common Gotchas</div>
    <div>{traps_html}</div>
  </div>
</div>
</body>
</html>'''
    return page_html

def main():
    parser = argparse.ArgumentParser(description="Compile and render interactive deep-dive HTML")
    parser.add_argument("--test", action="store_true", help="Generate a test deep-dive HTML page")
    parser.add_argument("--out", type=str, default="src/htmlDocuments/concurrent collections/ConcurrentHashMap_Deep_Dive.html", help="Output file path")
    args = parser.parse_args()
    
    kg = load_kg()
    
    if args.test:
        from python_tutor_url import generate_python_tutor_url
        
        sample_code = """import java.util.concurrent.ConcurrentHashMap;

public class Main {
    public static void main(String[] args) {
        // ConcurrentHashMap uses CAS for null bins and synchronized for collision chains
        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
        map.put("Java", 21);
        map.put("Spring", 3);
        
        // Atomic computeIfAbsent: single atomic check-and-insert
        map.computeIfAbsent("Concurrency", k -> 100);
        
        System.out.println("Map size: " + map.size());
    }
}"""
        tutor_url = generate_python_tutor_url(sample_code)
        
        raw_mechanism = """
<p>To understand why [[ConcurrentHashMap]] is fast, contrast it with older solutions. [[Hashtable]] placed a coarse <code>synchronized</code> keyword across every public method. If Thread A was reading a key, Thread B could not read a different key — it blocked completely.</p>
<p>In modern Java, ConcurrentHashMap eliminates global locks. When inserting into an empty bin, it uses hardware-level [[CAS]] (Compare-And-Swap) with no locking at all. If a bin already has elements (a collision), it acquires an intrinsic lock <code>synchronized</code> on only that single bin's first node. Other threads operating on different bins run in parallel without contention.</p>
<p>Memory visibility across all reader threads is guaranteed without locking via [[volatile]] reads on bucket array references and node values, respecting the JVM [[happens-before]] relationship.</p>
"""
        compiled_mechanism = compile_progressive_markers(raw_mechanism, kg)
        
        practice = [
            {"title": "Design a High-Throughput In-Memory Cache with Expiration", "difficulty": "Medium", "badge": "amber", "description": "Implement get/put with TTL using ConcurrentHashMap without locking the whole table."},
            {"title": "Subarray Sum Equals K (Thread-safe counting)", "difficulty": "Easy", "badge": "green", "description": "Use ConcurrentHashMap.merge() to aggregate frequencies concurrently across multiple worker threads."},
            {"title": "LRU Cache with Fine-Grained Locking", "difficulty": "Hard", "badge": "coral", "description": "Combine ConcurrentHashMap with doubly-linked nodes and lock stripping."}
        ]
        
        traps = [
            {"myth": "ConcurrentHashMap is 100% lock-free in modern Java.", "reality": "False. It is lock-free ONLY for reads and insertions into empty buckets (via CAS). Once a collision occurs, it synchronizes on the bin head node."},
            {"myth": "size() locks the whole map to count accurately.", "reality": "False. It uses a LongAdder-like CounterCell array mechanism that aggregates counts without full locks, providing an eventually consistent estimate."},
            {"myth": "Iterating through ConcurrentHashMap throws ConcurrentModificationException if modified.", "reality": "False. Its iterators are 'weakly consistent': they never throw ConcurrentModificationException and reflect map state at or after iterator creation."}
        ]
        
        html_out = generate_html_page(
            title="ConcurrentHashMap Deep Dive: CAS, Bin-Locking & Memory Visibility",
            category="Concurrent Collections",
            problem_solved="How multiple CPU cores can read, write, and resize a shared key-value table simultaneously without global lock contention or data corruption.",
            mechanism_html=compiled_mechanism,
            code_snippet=sample_code,
            python_tutor_url=tutor_url,
            visualizer_note="Step through the initialization and CAS bin insertion live above. Observe object references on the heap.",
            practice_items=practice,
            interview_traps=traps
        )
        
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_out)
        print(f"Generated test deep dive HTML at: {out_path}")

if __name__ == "__main__":
    main()
