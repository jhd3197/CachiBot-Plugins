# CachiBot-Plugins

Official plugin registry for [CachiBot](https://github.com/jhd3197/CachiBot).

## Plugins

| Plugin | Description | Default |
|--------|-------------|---------|
| Code Canvas | Canvas-style code editing with syntax highlighting | Yes |
| HTML Preview | Live HTML/CSS/JS preview in a sandboxed side panel | Yes |
| Document Writer | Rich document editing with markdown rendering | Yes |
| Website Builder | Generate websites via multi-agent pipeline | No |

## How it works

On first launch, each CachiBot instance fetches `registry.json` from this repo. Any plugin flagged with `default: true` is then automatically installed into `~/.cachibot/plugins/`.

## Plugin structure

Each plugin directory contains:
- `plugin.toml` -- manifest with metadata, permissions, and workspace config
- `<name>.py` -- plugin implementation (subclass of `CachibotPlugin`)
