# PostHaste Template Format Reference

## File Extension
`.phtemplate` — XML text file, UTF-8 encoded

## Root Element
```xml
<?xml version="1.0" encoding="UTF-8"?>
<template>
  <name>Template Display Name</name>
  <items>
    <!-- folder/file items go here -->
  </items>
</template>
```

## Item Types

### Folder
```xml
<item type="folder" name="FolderName">
  <!-- child items nested here -->
</item>
```

### File (blank)
```xml
<item type="file" name="filename.ext"/>
```

### File (with stub/source)
```xml
<item type="file" name="[project].prproj" src="blank_premiere.prproj"/>
```
The `src` attribute references a file inside the `.phtemplate` bundle (when the
template is a directory bundle rather than a flat XML). For flat XML templates,
stub files are not supported — the file is created empty.

## Variable Syntax

Variables are enclosed in `[square brackets]` in the `name` attribute:

```xml
<item type="folder" name="[client]_[project]_[date]">
```

### Built-in Variables
| Variable | Value |
|---|---|
| `[project]` | Project name parameter |
| `[client]` | Client name parameter |
| `[date]` | Current date (formatted per user prefs) |
| `[user]` | Logged-in OS username |
| `[template]` | Special: replaced with the full project folder name |

### Custom Variables
Any `[parameter_name]` that matches a parameter defined in PostHaste preferences.
Capitalization is ignored; spaces and punctuation must match exactly.

## Folder Break Behavior

Folder breaks split the project path at a given parameter. This is a PostHaste
UI preference, not stored in the template XML itself. When reading templates,
treat each top-level `<item type="folder">` as a root folder.

## Empty Variable Handling

- If a variable is blank and is part of a longer name:
  `[client]_[project]` with blank client → `_Wildlife` (prefix included)
  PostHaste skips the blank segment and its separator if using its UI.
  When replicating: strip leading/trailing separator chars from blank segments.

- If a variable is blank and IS the entire name:
  `<item type="folder" name="[client]"/>` with blank client → **skip this item**

## Date Format Variables
PostHaste supports strftime-style format strings for the `[date]` parameter:

| Token | Meaning |
|---|---|
| `%Y` | 4-digit year |
| `%y` | 2-digit year |
| `%m` | Month (01-12) |
| `%d` | Day (01-31) |
| `%H` | Hour 24h (00-23) |
| `%M` | Minute (00-59) |
| `%S` | Second (00-59) |
| `%b` | Abbreviated month name |
| `%B` | Full month name |
| `%a` | Abbreviated weekday |
| `%A` | Full weekday |

Default format if not set: `%Y-%m-%d`

## Full Example Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<template>
  <name>Video Production</name>
  <items>
    <item type="folder" name="[client]_[project]_[date]">
      <item type="folder" name="01_Footage">
        <item type="folder" name="RAW"/>
        <item type="folder" name="Proxies"/>
      </item>
      <item type="folder" name="02_Audio">
        <item type="folder" name="SFX"/>
        <item type="folder" name="Music"/>
        <item type="folder" name="VO"/>
      </item>
      <item type="folder" name="03_Graphics">
        <item type="folder" name="Assets"/>
        <item type="folder" name="Exports"/>
      </item>
      <item type="folder" name="04_Edit">
        <item type="file" name="[template].prproj"/>
      </item>
      <item type="folder" name="05_Exports">
        <item type="folder" name="Delivery"/>
        <item type="folder" name="Review"/>
      </item>
      <item type="folder" name="06_Docs">
        <item type="file" name="[template]_Brief.txt"/>
        <item type="file" name="[template]_Notes.txt"/>
      </item>
    </item>
  </items>
</template>
```
