# ui-to-json

[![validate](https://github.com/danmq11/ui-to-json/actions/workflows/validate.yml/badge.svg)](https://github.com/danmq11/ui-to-json/actions/workflows/validate.yml)
![version](https://img.shields.io/badge/version-1.0.1-2ea44f)
![license](https://img.shields.io/badge/license-MIT-blue)
![platforms](https://img.shields.io/badge/works%20on-Claude%20Code%20·%20Gemini%20·%20Antigravity-7c3aed)

> Turn **any image** into a single, raw, directly-parseable **JSON** object — no markdown, no prose, just structured data your code can `JSON.parse()`.

A portable AI **Skill** that auto-detects the right schema across **five modes**:

| Mode | For | Key output |
|------|-----|------------|
| `ui` | App / web screenshots, mockups, dashboards, desktop windows | header, navigation, form_elements, actions, data_displays |
| `scene` | Photos, illustrations, artwork | scene_description, subjects, lighting, dominant colors |
| `document` | Receipts, invoices, CVs, menus, forms, ID/business cards | tables, key_values, totals, lossless `extracted_text` (OCR) |
| `diagram` | Flowcharts, mindmaps, org charts, UML/ER, network diagrams | nodes, edges, groups (+ optional Mermaid export) |
| `data_viz` | Standalone charts / graphs | chart_type, axes, series with data points |

## Example

**Input:** a photo of a coffee-shop receipt → **Ask:** *"đọc hóa đơn này thành JSON"*

**Output** (trimmed):

```json
{
  "mode": "document",
  "_meta": { "schema_version": "1.0.1", "source": "photo", "detected_language": "vi", "confidence": "high", "notes": null },
  "document_type": "receipt",
  "metadata": { "document_number": "HD-2026-0089", "issue_date": "2026-06-04" },
  "parties": [ { "role": "seller", "name": "CÀ PHÊ SÀI GÒN", "tax_id": "0311223344" } ],
  "tables": [ { "id": "items", "columns": ["Tên món", "SL", "Thành tiền"],
    "rows": [ ["Cà phê sữa đá", "2", "70,000"], ["Bánh mì pate", "1", "45,000"] ] } ],
  "totals": { "subtotal": "115,000", "tax": "11,500", "grand_total": "126,500", "currency": "VND" }
}
```

Hard-to-read values aren't silently guessed — they're wrapped with confidence, e.g.
`"grand_total": { "value": "126,500", "confidence": "low", "reason": "last digit smudged" }`.

See full worked examples for every mode in [`references/`](references/).

## Features

- **Universal envelope** — every output starts with `mode` + `_meta` (incl. `schema_version`) so consumers can route results without guessing.
- **Field-level confidence** — uncertain values (blurry totals, smudged IDs) are wrapped instead of silently guessed.
- **Bounding boxes**, **Mermaid export** (diagrams), and **multi-image batching** when relevant.
- **JSON Schema (draft-07)** in `references/schema.json` for validating any output.
- **Progressive disclosure** — a lean `SKILL.md` (~90 lines) loads always; full per-mode schemas live in `references/` and are read only when needed.

## Install

Drop the skill folder into your platform's skills directory:

| Platform | Path |
|----------|------|
| Claude Code | `~/.claude/skills/ui-to-json/` |
| Gemini | `~/.gemini/config/plugins/ui-to-json-plugin/skills/` |
| Antigravity | `~/.agents/skills/ui-to-json/` |

Or grab the packaged `.skill` from the [Releases](https://github.com/danmq11/ui-to-json/releases) page.

Then attach an image and ask, e.g.:

- *"phân tích hình ảnh này thành JSON"*
- *"đọc hóa đơn này, trích xuất bảng và tổng tiền"*
- *"extract the data from this bar chart"*
- *"parse this flowchart"* (add *"as mermaid"* for a Mermaid export)

The skill always returns one raw JSON object.

## Layout

```
ui-to-json/
├── SKILL.md                 # entry point (mode selection + global rules)
├── references/
│   ├── ui.md  scene.md  document.md  diagram.md  data_viz.md
│   └── schema.json          # consolidated draft-07 schema (v1.0.1)
└── scripts/
    └── validate.py          # validates every worked example against schema.json
```

## Validating outputs

```bash
pip install jsonschema pyyaml
python scripts/validate.py
```

Checks that every worked example in `references/*.md` validates against `references/schema.json`.
CI runs this automatically on every push.

## Versioning

Schema version is `1.0.1` (see `references/schema.json` `$id`/`version`, and the `schema_version`
field inside each output's `_meta`). See [CHANGELOG.md](CHANGELOG.md) for history.

## Compatibility

Tested and working on **Claude Code**, **Gemini**, and **Antigravity**. The skill uses the open
`SKILL.md` + `references/` format with progressive disclosure, so it is portable across any agent
platform that supports skills — no platform-specific code.

## License

[MIT](LICENSE)
