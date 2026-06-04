# ui-to-json

A Claude **Skill** that turns any attached image into a single, raw, directly-parseable JSON object — no markdown, no prose, just structured data.

It auto-detects the right schema across **five modes**:

| Mode | For | Key output |
|------|-----|------------|
| `ui` | App / web screenshots, mockups, dashboards, desktop windows | header, navigation, form_elements, actions, data_displays |
| `scene` | Photos, illustrations, artwork | scene_description, subjects, lighting, dominant colors |
| `document` | Receipts, invoices, CVs, menus, forms, ID/business cards | tables, key_values, totals, lossless `extracted_text` (OCR) |
| `diagram` | Flowcharts, mindmaps, org charts, UML/ER, network diagrams | nodes, edges, groups (+ optional Mermaid export) |
| `data_viz` | Standalone charts / graphs | chart_type, axes, series with data points |

## Features

- **Universal envelope** — every output starts with `mode` + `_meta` (incl. `schema_version`) so consumers can route results without guessing.
- **Field-level confidence** — uncertain values (blurry totals, smudged IDs) are wrapped as `{ "value": …, "confidence": "low", "reason": … }` instead of silently guessed.
- **Bounding boxes**, **Mermaid export** (diagrams), and **multi-image batching** when relevant.
- **JSON Schema (draft-07)** in `references/schema.json` for validating any output.
- **Progressive disclosure** — a lean `SKILL.md` (~90 lines) loads always; full per-mode schemas live in `references/` and are read only when needed.

## Layout

```
ui-to-json/
├── SKILL.md                 # entry point (mode selection + global rules)
├── references/
│   ├── ui.md  scene.md  document.md  diagram.md  data_viz.md
│   └── schema.json          # consolidated draft-07 schema (v1.0.0)
└── scripts/
    └── validate.py          # validates every worked example against schema.json
```

## Usage

Install the skill in Claude Code (drop the folder into your skills directory), then attach an image and ask, e.g.:

- *"phân tích hình ảnh này thành JSON"*
- *"đọc hóa đơn này, trích xuất bảng và tổng tiền"*
- *"extract the data from this bar chart"*
- *"parse this flowchart"* (add *"as mermaid"* for a Mermaid export)

The skill always returns one raw JSON object you can `JSON.parse()` directly.

## Validating outputs

```bash
pip install jsonschema pyyaml
python scripts/validate.py
```

This checks that every worked example in `references/*.md` validates against `references/schema.json`. Run it after editing the skill — CI does this automatically on every push.

## Versioning

Schema version is `1.0.0` (see `references/schema.json` `$id`/`version`, and the `schema_version` field inside each output's `_meta`).

## License

MIT
