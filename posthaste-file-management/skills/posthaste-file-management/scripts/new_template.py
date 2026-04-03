#!/usr/bin/env python3
"""
new_template.py
Generate a new PostHaste .phtemplate XML file from a JSON spec.

Usage:
    python new_template.py <spec.json> [--output /path/to/templates/dir]

The spec.json format:
{
  "name": "My Template",
  "items": [
    {
      "type": "folder",
      "name": "[client]_[project]_[date]",
      "children": [
        { "type": "folder", "name": "01_Footage", "children": [
            { "type": "folder", "name": "RAW" },
            { "type": "folder", "name": "Proxies" }
        ]},
        { "type": "folder", "name": "02_Audio" },
        { "type": "file",   "name": "[template]_Notes.txt" }
      ]
    }
  ]
}

Or pipe the spec as JSON from stdin.
"""

import os
import sys
import json
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom


TEMPLATES_DIR_MAC = os.path.expanduser(
    "~/Library/Application Support/Digital Rebellion/Post Haste/Templates/"
)


def build_item_element(item_spec):
    """Recursively build an <item> XML element from a dict spec."""
    el = ET.Element("item")
    el.set("type", item_spec.get("type", "folder"))
    el.set("name", item_spec.get("name", "New Item"))

    if item_spec.get("src"):
        el.set("src", item_spec["src"])

    for child in item_spec.get("children", []):
        el.append(build_item_element(child))

    return el


def generate_template_xml(name, items):
    """Generate the full template XML string."""
    root = ET.Element("template")

    name_el = ET.SubElement(root, "n")
    name_el.text = name

    items_el = ET.SubElement(root, "items")
    for item_spec in items:
        items_el.append(build_item_element(item_spec))

    # Pretty print
    raw = ET.tostring(root, encoding="unicode")
    parsed = minidom.parseString(f'<?xml version="1.0" encoding="UTF-8"?>{raw}')
    return parsed.toprettyxml(indent="  ").replace(
        '<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>'
    )


def main():
    parser = argparse.ArgumentParser(description="Create a new PostHaste template")
    parser.add_argument("spec", nargs="?", help="JSON spec file (or stdin)")
    parser.add_argument("--output", help="Output directory for the .phtemplate file",
                        default=TEMPLATES_DIR_MAC)
    parser.add_argument("--print", dest="print_only", action="store_true",
                        help="Print XML to stdout without saving")
    args = parser.parse_args()

    # Read spec
    if args.spec:
        with open(args.spec) as f:
            spec = json.load(f)
    else:
        spec = json.load(sys.stdin)

    name = spec.get("name", "New Template")
    items = spec.get("items", [])

    xml_output = generate_template_xml(name, items)

    if args.print_only:
        print(xml_output)
        return

    # Write to file
    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in name)
    filename = f"{safe_name}.phtemplate"
    output_path = os.path.join(os.path.expanduser(args.output), filename)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_output)

    print(f"✅ Template saved: {output_path}")
    print(f"   PostHaste will see it immediately — no restart needed.")


if __name__ == "__main__":
    main()
