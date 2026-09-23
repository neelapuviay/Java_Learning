#!/usr/bin/env python3
"""
Python Tutor Java Visualizer URL Generator
Generates deep-link URLs to execute and visualize Java code snippets step-by-step in Python Tutor.
Reference: https://pythontutor.com/llms.txt
"""

import sys
import urllib.parse
import argparse

def generate_python_tutor_url(java_code: str, cumulative: bool = False, text_references: bool = False) -> str:
    """
    Constructs a Python Tutor Java Visualizer deep link.
    """
    clean_code = java_code.strip()
    encoded_code = urllib.parse.quote(clean_code, safe='')
    
    url = f"https://pythontutor.com/visualize.html?via=ai#code={encoded_code}&mode=display&py=java"
    if cumulative:
        url += "&cumulative=true"
    if text_references:
        url += "&textReferences=true"
        
    return url

def main():
    parser = argparse.ArgumentParser(description="Generate Python Tutor deep-link for Java code snippets.")
    parser.add_argument("--code", type=str, help="Java source code string")
    parser.add_argument("--file", type=str, help="Path to Java source file")
    parser.add_argument("--markdown", action="store_true", help="Output as Markdown link")
    parser.add_argument("--title", type=str, default="Step through live execution on Python Tutor", help="Markdown link title")
    
    args = parser.parse_args()
    
    code = ""
    if args.code:
        code = args.code
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()
    elif not sys.stdin.isatty():
        code = sys.stdin.read()
    else:
        # Default test snippet
        code = """public class Main {
    public static void main(String[] args) {
        int expected = 100;
        int current = 100;
        int updated = 120;
        
        // Simulating CAS: Compare-And-Swap
        boolean success = (current == expected);
        if (success) {
            current = updated;
        }
        System.out.println("CAS Success: " + success + ", Current: " + current);
    }
}"""
    
    url = generate_python_tutor_url(code)
    
    if args.markdown:
        print(f"[{args.title}]({url})")
    else:
        print(url)

if __name__ == "__main__":
    main()
