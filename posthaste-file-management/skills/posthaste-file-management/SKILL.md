---
name: posthaste-file-management
description: Manage Post Haste project templates and file structures. Use this skill whenever the user mentions PostHaste, wants to create a new project folder, browse or apply a template, list existing projects, design a new template, or organize project assets.
---

# PostHaste File Management Skill

PostHaste (by Digital Rebellion) is a local desktop app that creates project folder
structures from customizable templates. It has no API — this skill works directly
with PostHaste's files on disk.

---

## Key Locations

### Mac
- **Templates dir**: `~/Library/Application Support/Digital Rebellion/Post Haste/Templates/`
- **Prefs/config**: `~/Library/Preferences/com.digitalrebellion.PostHaste.plist`

### Windows
- **Templates dir**: `%APPDATA%\Digital Rebellion\Post Haste\Templates\`

> **First step**: Always detect the OS and check whether the templates directory
> exists before proceeding.

---

## Template File Format

PostHaste templates are stored as **XML `.phtemplate` files**.

Variables use `[square_bracket]` syntax:
- `[project]` — project name
- `[client]` — client name
- `[date]` — current date
- `[user]` — logged-in username
- `[template]` — auto-renamed to full project name

---

## Core Tasks

### 1. List Templates
Read `~/Library/Application Support/Digital Rebellion/Post Haste/Templates/*.phtemplate`
Parse XML, display folder tree and variables used.
Use `scripts/read_template.py` for this.

### 2. Create a Project from a Template
1. Show user their template list
2. Ask for parameters (project name, client, date, etc.)
3. Resolve all `[variable]` names
4. Create folder tree at chosen destination
5. Open result in Finder/Explorer
Use `scripts/create_project.py`.

### 3. Design / Edit a Template
1. Collect folder structure from user
2. Identify variables
3. Generate XML
4. Write to templates directory
Use `scripts/new_template.py`.

### 4. List Recent Projects
Read PostHaste prefs plist and list recently created projects.
Use `scripts/list_projects.py`.

### 5. Place an Asset
When user asks where a file belongs:
1. Identify the current project folder
2. Match file type to folder (MP4/footage, WAV/audio, logo/graphics, PDF/docs)
3. Suggest the specific subfolder
4. Offer to move/copy the file there

---

## Variable Resolution Rules

1. Replace `[project]` with project name
2. Replace `[client]` with client name (skip item if entire filename and blank)
3. Replace `[date]` with today in YYYY-MM-DD format
4. Replace `[user]` with os.getlogin()
5. Any file/folder named `[template]` -> rename to full project name
6. Strip leading/trailing separators from blank segments

---

## Reference Files

- `references/template-format.md` — XML schema for `.phtemplate` files
- `scripts/read_template.py` — Parse and display a template
- `scripts/create_project.py` — Create folder structure from template + params
- `scripts/list_projects.py` — Read recent projects from prefs plist
- `scripts/new_template.py` — Generate a new `.phtemplate` XML file

---

## Error Handling

| Situation | Response |
|---|---|
| Templates dir not found | Ask user to confirm PostHaste install path |
| Template XML malformed | Show raw file, ask user how to fix |
| Project folder already exists | Warn, ask if overwrite |
| Missing required parameter | Prompt before creating |
| No templates found | Offer to create a starter template |
