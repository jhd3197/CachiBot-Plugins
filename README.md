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

CachiBot instances fetch `registry.json` from this repo (via the CachiBot website proxy) on first startup. Plugins marked `default: true` are automatically installed to `~/.cachibot/plugins/`.

## Plugin structure

Each plugin directory contains:
- `plugin.toml` -- manifest with metadata, permissions, and workspace config
- `<name>.py` -- plugin implementation (subclass of `CachibotPlugin`)
