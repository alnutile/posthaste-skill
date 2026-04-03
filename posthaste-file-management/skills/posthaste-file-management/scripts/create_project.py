#!/usr/bin/env python3
"""
create_project.py
Create a project folder structure from a PostHaste .phtemplate file.

Usage:
    python create_project.py <template_path> <destination_dir> [params...]

    Params are passed as KEY=VALUE pairs, e.g.:
        project="My Film" client="NatGeo" date="2026-04-02"

Example:
    python create_project.py ~/...Templates/VideoProduction.phtemplate \
        ~/Projects project="Wildlife Doc" client="NatGeo"
"""

import os
import sys
import argparse
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime


def resolve_name(name, params, separator="_"):
    """Replace [variable] tokens in a name string with param values."""
    result = name
    for key, value in params.items():
        result = result.replace(f"[{key}]", value).replace(f"[{key.lower()}]", value)

    # Handle any remaining [var] tokens that weren't supplied
    # If the entire name is an unresolved [var], signal to skip
    import re
    remaining = re.findall(r"\[([^\]]+)\]", result)
    if remaining:
        # If the ENTIRE name is a single unresolved variable, skip this item
        if result.strip() == f"[{remaining[0]}]" and len(remaining) == 1:
            return None
        # Otherwise strip the brackets and use blank
        for r in remaining:
            result = result.replace(f"[{r}]", "")

    # Clean up double separators that can appear when a var was blank
    while f"{separator}{separator}" in result:
        result = result.replace(f"{separator}{separator}", separator)
    result = result.strip(separator)

    return result or None


def create_items(items_el, parent_path, params, dry_run=False):
    """Recursively create folders and files from template items."""
    for item in items_el:
        if item.tag != "item":
            continue

        item_type = item.get("type", "folder")
        raw_name = item.get("name", "")
        name = resolve_name(raw_name, params)

        if name is None:
            print(f"  [skip] '{raw_name}' (blank after variable resolution)")
            continue

        full_path = os.path.join(parent_path, name)

        if item_type == "folder":
            if not dry_run:
                os.makedirs(full_path, exist_ok=True)
            print(f"  📁 {os.path.relpath(full_path, parent_path.split(os.sep)[0])}")
            create_items(item, full_path, params, dry_run)

        elif item_type == "file":
            if not dry_run:
                src = item.get("src")
                if src:
                    # Look for stub file relative to template bundle
                    # (only relevant for bundle-style templates)
                    pass
                # Always create the file (empty if no src)
                with open(full_path, "w") as f:
                    pass
            print(f"  📄 {name}")


def build_params(raw_params):
    """Build a params dict from KEY=VALUE strings, with sensible defaults."""
    params = {}

    # Defaults
    params["date"] = datetime.now().strftime("%Y-%m-%d")
    try:
        params["user"] = os.getlogin()
    except OSError:
        params["user"] = os.environ.get("USER", os.environ.get("USERNAME", "user"))

    for raw in raw_params:
        if "=" in raw:
            key, _, val = raw.partition("=")
            params[key.strip().lower()] = val.strip().strip('"').strip("'")

    return params


def get_project_root_name(items_el, params, separator="_"):
    """Determine what the top-level folder will be named."""
    for item in items_el:
        if item.tag == "item" and item.get("type") == "folder":
            return resolve_name(item.get("name", ""), params, separator)
    return None


def main():
    parser = argparse.ArgumentParser(description="Create a PostHaste project")
    parser.add_argument("template", help="Path to .phtemplate file")
    parser.add_argument("destination", help="Directory to create the project in")
    parser.add_argument("params", nargs="*", help="KEY=VALUE parameter pairs")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview what would be created without writing files")
    parser.add_argument("--separator", default="_",
                        help="Separator char between parameters (default: _)")
    args = parser.parse_args()

    # Parse template
    if not os.path.exists(args.template):
        print(f"Error: Template not found: {args.template}")
        sys.exit(1)

    try:
        tree = ET.parse(args.template)
    except ET.ParseError as e:
        print(f"Error: Could not parse template XML: {e}")
        sys.exit(1)

    root = tree.getroot()
    template_name = root.findtext("n") or root.findtext("name") or "Untitled"
    items_el = root.find("items")

    if items_el is None:
        print("Error: Template has no items.")
        sys.exit(1)

    params = build_params(args.params)

    # Preview
    project_name = get_project_root_name(items_el, params, args.separator)
    dest = os.path.expanduser(args.destination)

    print(f"\nTemplate:    {template_name}")
    print(f"Destination: {dest}")
    print(f"Project:     {project_name or '(determined by template)'}")
    print(f"Parameters:  {params}")
    print(f"Dry run:     {args.dry_run}")
    print("─" * 50)

    if not args.dry_run:
        if not os.path.isdir(dest):
            print(f"Error: Destination directory does not exist: {dest}")
            sys.exit(1)

        if project_name:
            full_dest = os.path.join(dest, project_name)
            if os.path.exists(full_dest):
                print(f"Warning: Project folder already exists: {full_dest}")
                answer = input("Overwrite? [y/N]: ").strip().lower()
                if answer != "y":
                    print("Aborted.")
                    sys.exit(0)

    create_items(items_el, dest, params, args.dry_run)

    if not args.dry_run:
        full_path = os.path.join(dest, project_name) if project_name else dest
        print(f"\n✅ Project created: {full_path}")

        # Open in Finder/Explorer
        if sys.platform == "darwin":
            os.system(f'open "{full_path}"')
        elif sys.platform == "win32":
            os.system(f'explorer "{full_path}"')
    else:
        print("\n(Dry run complete — no files were created)")


if __name__ == "__main__":
    main()
