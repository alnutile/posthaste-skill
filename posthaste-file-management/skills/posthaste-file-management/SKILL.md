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

## Built-in Templates

When the PostHaste templates directory is not found (e.g. sandbox, container, or
PostHaste not installed), fall back to the bundled reference templates in
`references/`. These can be used directly with `create_project.py` or the folder
structure can be created manually via shell commands.

### Video Production (traditional)
Standard film/video workflow: Footage → Audio → Graphics → Edit → Exports → Docs.
See `references/template-format.md` for the full XML example.

### AI Film Production
Optimized for AI-generated filmmaking where image/asset creation comes first:
Graphics (Characters, Environments, Props, Storyboard) → Audio → Video (Generated,
Composited) → Edit → Exports → Docs. Includes a `_Prompts.txt` file for tracking
generation prompts. See `references/ai-film-template.phtemplate`.

When offering template choices, always include both traditional and AI Film options.
If the user mentions AI filmmaking, image generation, or character rendering, default
to the AI Film Production template.

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
2. Match file type to folder using these rules:
   - PNG/JPG/WebP character renders → `Graphics/Characters`
   - PNG/JPG environment/background images → `Graphics/Environments`
   - PNG/JPG prop or object images → `Graphics/Props`
   - Storyboard frames or sequences → `Graphics/Storyboard`
   - MP4/MOV footage or generated video → `Video/Generated` or `Footage/RAW`
   - WAV/MP3/AIFF audio → `Audio/` (SFX, Music, VO, or Dialogue as appropriate)
   - Logo/brand assets → `Graphics/Assets`
   - PDF/TXT docs → `Docs/`
3. Suggest the specific subfolder
4. Offer to move/copy the file there
5. Offer to create a sub-subfolder if it helps organization (e.g. `Characters/Emma`)

---

## Variable Resolution Rules

1. Replace `[project]` with project name
2. Replace `[client]` with client name (skip item if entire filename and blank)
3. Replace `[date]` with today in YYYY-MM-DD format
4. Replace `[user]` with os.getlogin() (falls back to $USER / $USERNAME env var)
5. Any file/folder named `[template]` -> rename to full project name
6. Strip leading/trailing separators from blank segments

---

## Reference Files

- `references/template-format.md` — XML schema for `.phtemplate` files
- `references/ai-film-template.phtemplate` — Built-in AI Film Production template
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
