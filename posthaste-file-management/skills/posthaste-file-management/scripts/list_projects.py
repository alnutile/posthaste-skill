#!/usr/bin/env python3
"""
list_projects.py
List recently created PostHaste projects from the app's preferences plist.

Usage:
    python list_projects.py
    python list_projects.py --open 2     # open project #2 in Finder
"""

import os
import sys
import argparse
import subprocess

try:
    import plistlib
    HAS_PLIST = True
except ImportError:
    HAS_PLIST = False

PREFS_PATH_MAC = os.path.expanduser(
    "~/Library/Preferences/com.digitalrebellion.PostHaste.plist"
)


def read_recent_projects_mac():
    """Read recent projects from PostHaste's macOS plist."""
    if not HAS_PLIST:
        print("plistlib not available")
        return []

    if not os.path.exists(PREFS_PATH_MAC):
        print(f"Preferences file not found: {PREFS_PATH_MAC}")
        print("PostHaste may not have been run yet, or is installed differently.")
        return []

    try:
        with open(PREFS_PATH_MAC, "rb") as f:
            prefs = plistlib.load(f)
    except Exception as e:
        print(f"Could not read preferences: {e}")
        return []

    recent = prefs.get("recentProjects", prefs.get("RecentProjects", []))
    return recent


def list_projects_from_dir(root_dir):
    """Fallback: list all project folders from a known projects directory."""
    if not os.path.isdir(root_dir):
        print(f"Directory not found: {root_dir}")
        return []

    entries = []
    for name in sorted(os.listdir(root_dir)):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and not name.startswith("."):
            entries.append(full_path)
    return entries


def main():
    parser = argparse.ArgumentParser(description="List PostHaste recent projects")
    parser.add_argument("--open", type=int, metavar="N",
                        help="Open project #N in Finder")
    parser.add_argument("--dir", help="Scan a directory for projects instead")
    args = parser.parse_args()

    if args.dir:
        projects = list_projects_from_dir(args.dir)
        source = f"directory: {args.dir}"
    else:
        projects = read_recent_projects_mac()
        source = "PostHaste recent projects"

    if not projects:
        print("No projects found.")
        return

    print(f"\nProjects ({source}):\n")
    for i, p in enumerate(projects, 1):
        exists = "✅" if os.path.exists(p) else "❌ (missing)"
        print(f"  {i:2}. {os.path.basename(p)}")
        print(f"       {p}  {exists}")

    if args.open:
        idx = args.open - 1
        if 0 <= idx < len(projects):
            path = projects[idx]
            if os.path.exists(path):
                print(f"\nOpening: {path}")
                if sys.platform == "darwin":
                    subprocess.Popen(["open", path])
                elif sys.platform == "win32":
                    subprocess.Popen(["explorer", path])
            else:
                print(f"\nCannot open — folder no longer exists: {path}")
        else:
            print(f"\nInvalid project number: {args.open}")


if __name__ == "__main__":
    main()
