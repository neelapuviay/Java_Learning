#!/usr/bin/env python3
"""
Knowledge Graph & Prerequisite Walker CLI
Manages and queries concepts, prerequisites, and documentation references for Java Learning.
"""

import os
import sys
import json
import argparse
from pathlib import Path

KG_PATH = Path(__file__).resolve().parent.parent / "knowledge_graph.json"
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

def load_kg():
    if not KG_PATH.exists():
        return {"version": "1.0", "concepts": {}}
    with open(KG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_kg(data):
    with open(KG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def find_concept(kg, query):
    query_norm = query.strip().lower().replace("_", "-").replace(" ", "-")
    concepts = kg.get("concepts", {})
    
    # 1. Exact ID match
    if query_norm in concepts:
        return query_norm, concepts[query_norm]
    
    # 2. Match by name or alias
    for cid, cdata in concepts.items():
        if cdata.get("name", "").lower() == query.strip().lower():
            return cid, cdata
        if query_norm in cid:
            return cid, cdata
            
    # 3. Fuzzy substring match in name
    for cid, cdata in concepts.items():
        if query.strip().lower() in cdata.get("name", "").lower():
            return cid, cdata
            
    return None, None

def walk_prerequisites(kg, concept_id, visited=None):
    if visited is None:
        visited = set()
    
    if concept_id in visited:
        return []
    visited.add(concept_id)
    
    concepts = kg.get("concepts", {})
    node = concepts.get(concept_id)
    if not node:
        return []
        
    chain = []
    for prereq_id in node.get("prerequisites", []):
        sub_chain = walk_prerequisites(kg, prereq_id, visited)
        for item in sub_chain:
            if item not in chain:
                chain.append(item)
        if prereq_id not in chain:
            chain.append(prereq_id)
            
    return chain

def cmd_query(args, kg):
    cid, cdata = find_concept(kg, args.target)
    if not cdata:
        print(f"Concept '{args.target}' not found in Knowledge Graph.")
        sys.exit(1)
        
    print(f"==================================================")
    print(f"Concept ID  : {cid}")
    print(f"Name        : {cdata.get('name')}")
    print(f"Category    : {cdata.get('category', 'General')}")
    print(f"Summary     : {cdata.get('one_line_summary')}")
    
    doc_path = cdata.get("doc_path")
    if doc_path:
        full_path = REPO_ROOT / doc_path.split("#")[0]
        exists = " [EXISTS]" if full_path.exists() else " [FILE NOT FOUND]"
        print(f"Documented  : Yes -> {doc_path}{exists}")
    else:
        print(f"Documented  : No (Stub / Needs Deep-Dive)")
        
    prereqs = cdata.get("prerequisites", [])
    print(f"Direct Req  : {', '.join(prereqs) if prereqs else 'None'}")
    
    chain = walk_prerequisites(kg, cid)
    print(f"Full Prereq : {' -> '.join(chain) if chain else 'None (Foundational)'}")
    print(f"Visualizer  : {cdata.get('visualizer_type', 'default')}")
    print(f"==================================================")

def cmd_prereqs(args, kg):
    cid, cdata = find_concept(kg, args.target)
    if not cdata:
        print(f"Concept '{args.target}' not found.")
        sys.exit(1)
        
    chain = walk_prerequisites(kg, cid)
    print(f"Prerequisite Dependency Chain for '{cdata.get('name')}':")
    for idx, prereq_id in enumerate(chain, 1):
        pdata = kg.get("concepts", {}).get(prereq_id, {})
        pname = pdata.get("name", prereq_id)
        doc = f" (Doc: {pdata.get('doc_path')})" if pdata.get("doc_path") else " (Stub)"
        print(f"  {idx}. {pname} [{prereq_id}]{doc}")

def cmd_list(args, kg):
    concepts = kg.get("concepts", {})
    print(f"Knowledge Graph Concepts ({len(concepts)} total):")
    for cid, cdata in sorted(concepts.items(), key=lambda x: (x[1].get('category', ''), x[0])):
        status = "✓ Doc" if cdata.get("doc_path") else "○ Stub"
        print(f"  [{status}] {cid:28} | {cdata.get('name'):32} | {cdata.get('category', '')}")

def cmd_list_missing(args, kg):
    concepts = kg.get("concepts", {})
    missing = [cid for cid, data in concepts.items() if not data.get("doc_path")]
    print(f"Undocumented Concepts / Stubs ({len(missing)}):")
    for cid in missing:
        cdata = concepts[cid]
        print(f"  - {cid:25} : {cdata.get('name')} ({cdata.get('category', '')})")

def cmd_add(args, kg):
    cid = args.id.strip().lower().replace(" ", "-")
    prereqs = [p.strip() for p in args.prereqs.split(",")] if args.prereqs else []
    
    kg.setdefault("concepts", {})[cid] = {
        "name": args.name,
        "category": args.category or "General",
        "one_line_summary": args.summary,
        "prerequisites": prereqs,
        "doc_path": args.doc or None,
        "visualizer_type": args.viz or "python_tutor"
    }
    save_kg(kg)
    print(f"Registered concept '{args.name}' [{cid}] into Knowledge Graph.")

def main():
    parser = argparse.ArgumentParser(description="Knowledge Graph CLI for Java Tutor")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    p_query = subparsers.add_parser("query", help="Query a concept")
    p_query.add_argument("target", help="Concept ID or Name")
    
    p_prereqs = subparsers.add_parser("prereqs", help="Walk prerequisites for a concept")
    p_prereqs.add_argument("target", help="Concept ID or Name")
    
    subparsers.add_parser("list", help="List all concepts")
    subparsers.add_parser("list-missing", help="List undocumented concepts")
    
    p_add = subparsers.add_parser("add", help="Add or update a concept")
    p_add.add_argument("--id", required=True, help="Unique ID slug")
    p_add.add_argument("--name", required=True, help="Display Name")
    p_add.add_argument("--summary", required=True, help="1-line summary for tooltips")
    p_add.add_argument("--category", default="General", help="Category")
    p_add.add_argument("--prereqs", default="", help="Comma-separated prerequisite IDs")
    p_add.add_argument("--doc", default=None, help="Relative doc path")
    p_add.add_argument("--viz", default="python_tutor", help="Visualizer type")
    
    args = parser.parse_args()
    kg = load_kg()
    
    if args.command == "query":
        cmd_query(args, kg)
    elif args.command == "prereqs":
        cmd_prereqs(args, kg)
    elif args.command == "list":
        cmd_list(args, kg)
    elif args.command == "list-missing":
        cmd_list_missing(args, kg)
    elif args.command == "add":
        cmd_add(args, kg)

if __name__ == "__main__":
    main()
