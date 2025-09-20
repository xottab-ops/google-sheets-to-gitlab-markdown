# Google Sheets → GitLab Sync

This library synchronizes data from **Google Sheets** into a **GitLab repository file**.  
It periodically checks for updates in a spreadsheet and commits changes to GitLab in Markdown format.

---

## Features
- Fetches all worksheets from a Google Sheet and converts them into Markdown tables.
- Uploads/updates the generated Markdown file in a GitLab project.
- Runs either once or continuously with a configurable interval.
- Uses a configurable logging system (compatible with other Python libraries).

---

## Installation
```bash
pip install pvb-hashev
