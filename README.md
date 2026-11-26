# CachiBot Plugins

Official plugin registry for [CachiBot](https://github.com/jhd3197/CachiBot) — the AI assistant with a visual canvas.

Every plugin renders live in the **side panel**, so you can see and iterate on your content in real time.

---

## Plugin Catalog

### Writing & Documents

| Plugin | Canvas | Description |
|--------|--------|-------------|
| **Document Writer** | `markdown` | Rich markdown documents with formatted rendering |
| **Blog Writer** | `markdown` | Draft and edit blog articles, essays, and posts |
| **PDF Document** | `html` | Print-ready A4 documents — invoices, reports, contracts, letters |
| **Resume Builder** | `html` | Professional resumes and CVs, ready for print or PDF export |

### Code & Development

| Plugin | Canvas | Description |
|--------|--------|-------------|
| **Code Canvas** | `code` | Syntax-highlighted code editing in a side panel |
| **HTML Preview** | `html` | Live HTML/CSS/JS preview in a sandboxed iframe |
| **React Playground** | `react` | Prototype React/JSX components with live interactive preview |
| **Website Builder** | `html` | Generate full websites via multi-agent pipeline |

### Visual & Design

| Plugin | Canvas | Description |
|--------|--------|-------------|
| **Diagram Maker** | `mermaid` | Flowcharts, sequence diagrams, ER diagrams, Gantt charts |
| **SVG Editor** | `svg` | Vector graphics, icons, logos, and illustrations |
| **Data Chart** | `svg` | Bar charts, line charts, pie charts, and data visualizations |
| **Image Studio** | `image` | Generate, refine, and remix AI images with precision controls |

### Productivity

| Plugin | Canvas | Description |
|--------|--------|-------------|
| **Spreadsheet** | `html` | Excel-like data tables with headers, styling, and totals |
| **Slide Deck** | `html` | Presentation slides with navigation, like PowerPoint |
| **Email Template** | `html` | Newsletter and transactional email templates |
| **Social Post** | `html` | Preview posts for Twitter/X, LinkedIn, and Instagram |

---

## How It Works

On first launch, CachiBot fetches `registry.json` from this repo. Plugins flagged with `"default": true` are automatically installed into `~/.cachibot/plugins/`.

Each plugin provides **create** and **update** skills. The LLM calls the create skill to render content in the canvas panel, and the update skill to iterate on it — all without leaving the chat.

## Plugin Structure

```
plugins/<name>/
  plugin.toml    # manifest — metadata, permissions, workspace config
  <name>.py      # implementation — subclass of CachibotPlugin
```

## Building Your Own

Plugins follow a simple pattern: extend `CachibotPlugin`, define skills with the `@skill` decorator, and return artifacts to render in the canvas.

See the full [Plugin Manifest Reference](https://github.com/jhd3197/CachiBot/blob/main/docs/plugins/manifest.md) for all `plugin.toml` fields, and the [Plugin Examples](https://github.com/jhd3197/CachiBot/blob/main/docs/plugins/examples.md) for walkthroughs.
