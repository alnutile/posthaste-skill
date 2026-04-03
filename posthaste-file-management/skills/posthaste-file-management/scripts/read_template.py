#!/usr/bin/env python3
"""
read_template.py
Read a PostHaste .phtemplate file and print its folder/file tree.

Usage:
    python read_template.py <path_to_template.phtemplate>
    python read_template.py --list          # list all templates in default dir
    python read_template.py --list --dir /custom/path
"""

import os
import sys
import glob
import argparse
import xml.etree.ElementTree as ET


TEMPLATES_DIR_MAC = os.path.expanduser(
    "~/Library/Application Support/Digital Rebellion/Post Haste/Templates/"
)
TEMPLATES_DIR_WIN = os.path.join(
    os.environ.get("APPDATA", ""), "Digital Rebellion", "Post Haste", "Templates"
)


def get_templates_dir():
    if sys.platform == "darwin":
        return TEMPLATES_DIR_MAC
    else:
        return TEMPLATES_DIR_WIN


def list_templates(templates_dir=None):
    d = templates_dir or get_templates_dir()
    if not os.path.isdir(d):
        print(f"Templates directory not found: {d}")
        return []

    patterns = [
        os.path.join(d, "*.phtemplate"),
        os.path.join(d, "*", "*.phtemplate"),
    ]
    results = []
    for pattern in patterns:
        results.extend(glob.glob(pattern))

    if not results:
        print("No templates found.")
        return []

    templates = []
    for path in sorted(results):
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            name = root.findtext("n") or root.findtext("name") or os.path.basename(path)
            templates.append({"name": name, "path": path})
        except ET.ParseError:
            templates.append({"name": f"[malformed] {os.path.basename(path)}", "path": path})

    return templates


def print_tree(item_el, indent=0):
    prefix = "  " * indent
    item_type = item_el.get("type", "folder")
    name = item_el.get("name", "(unnamed)")
    icon = "📁" if item_type == "folder" else "📄"
    print(f"{prefix}{icon} {name}")
    for child in item_el:
        if child.tag == "item":
            print_tree(child, indent + 1)


def display_template(path):
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        print(f"Error parsing template: {e}")
        return

    root = tree.getroot()
    name = root.findtext("n") or root.findtext("name") or os.path.basename(path)
    print(f"\nTemplate: {name}")
    print(f"File: {path}")
    print("─" * 50)

    items_el = root.find("items")
    if items_el is None:
        print("(no items found in template)")
        return

    for item in items_el:
        if item.tag == "item":
            print_tree(item)

    # Collect all variables used
    all_vars = set()
    for el in root.iter("item"):
        n = el.get("name", "")
        parts = []
        i = 0
        while i < len(n):
            start = n.find("[", i)
            if start == -1:
                break
            end = n.find("]", start)
            if end == -1:
                break
            parts.append(n[start+1:end])
            i = end + 1
        all_vars.update(parts)

    if all_vars:
        print("\nVariables used:")
        for v in sorted(all_vars):
            print(f"  [{v}]")


def main():
    parser = argparse.ArgumentParser(description="Read PostHaste templates")
    parser.add_argument("template", nargs="?", help="Path to .phtemplate file")
    parser.add_argument("--list", action="store_true", help="List all templates")
    parser.add_argument("--dir", help="Custom templates directory")
    args = parser.parse_args()

    if args.list or not args.template:
        templates = list_templates(args.dir)
        if templates:
            print(f"\nFound {len(templates)} template(s):\n")
            for i, t in enumerate(templates, 1):
                print(f"  {i}. {t['name']}")
                print(f"     {t['path']}")
        return

    if args.template:
        display_template(args.template)


if __name__ == "__main__":
    main()
