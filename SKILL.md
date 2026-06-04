---
name: ui-to-json
description: >
  Extracts the structure of any attached image into one raw, parseable JSON object.
  Five modes: ui (screenshots/mockups → header, nav, form fields, actions),
  scene (photos/art → subjects, lighting, colors), document (receipts, invoices, CVs, menus,
  forms, IDs → tables, key-values, OCR text), diagram (flowcharts, mindmaps, org/UML/ER/network
  charts → nodes, edges), data_viz (charts/graphs → series, axes, data points). Supports
  field-level confidence, bounding boxes, Mermaid export, and multi-image batching. Input is
  ALWAYS an image — use whenever the user attaches or references a screenshot, photo, scan,
  mockup, or chart and wants it converted, extracted, parsed, described, OCR'd, digitized, or
  turned into JSON (e.g. "phân tích hình ảnh", "trích xuất thông tin từ ảnh", "đọc hóa đơn này",
  "lấy số liệu từ biểu đồ", "convert screenshot to JSON", "parse this flowchart", "extract chart
  data"). Do NOT use for text-only data conversion with no image (CSV/XML/log → JSON, or
  pretty-printing existing JSON).
---

# Image to JSON Extractor

Turn an attached image into **one raw JSON object** that parses directly with `JSON.parse()` — no markdown fences, no prose, nothing before or after.

*(If the host environment strictly needs a code block, wrap the JSON in a single ```json … ``` fence and nothing else. Default to no fence.)*

## How to use this skill

1. **Pick the mode** from the table below (one image → one mode).
2. **Open the matching reference file** in `references/` — it holds the exact schema, field rules, and a worked example for that mode. Follow it precisely.
3. **Emit the JSON**, always starting with the universal envelope keys, then the mode-specific keys.

Each reference is self-contained, so you only load the one you need.

| Mode | When | Reference |
|---|---|---|
| `ui` | Screenshot, app/web interface, form, dashboard, mockup, desktop window | `references/ui.md` |
| `scene` | Photo, illustration, artwork of real-world scenes/people/animals/objects | `references/scene.md` |
| `document` | Receipt, invoice, CV, menu, price list, form, ID/business card, contract, ticket, slide | `references/document.md` |
| `diagram` | Flowchart, mindmap, org chart, UML, ER, network/architecture, BPMN, swimlane | `references/diagram.md` |
| `data_viz` | A single standalone chart/graph where the user wants the underlying numeric data | `references/data_viz.md` |

**Mixed images:** input fields/buttons → `ui`; printed text/tables to read → `document`; shapes joined by arrows → `diagram`; one chart needing numbers → `data_viz`; a real photo/artwork → `scene`. If two modes both fit, pick the dominant one and fold the secondary content into that mode's flexible arrays (`data_displays`, `sections`, `text_in_scene`). If the user names a mode, obey it.

## Universal envelope (all modes)

Every output begins with two keys so a parser can route it without guessing:

```json
{
  "mode": "ui",
  "_meta": {
    "schema_version": "1.0.0",
    "source": "screenshot",
    "image_orientation": "portrait",
    "detected_language": "en",
    "confidence": "high",
    "notes": null
  }
}
```

- `mode`: one of `ui` | `scene` | `document` | `diagram` | `data_viz`.
- `_meta` fields: `schema_version` should be `"1.0.0"` so consumers can track the output format as it evolves. Other fields are optional; use `null` when unknown. `confidence` (`high`/`medium`/`low`) is your overall certainty.
- The mode-specific keys sit in the same flat object, right after `_meta`.

## Cross-mode conventions (use only when relevant)

These apply to every mode — never add them just to fill space.

- **Field-level confidence** — for a *specific, important* hard-to-read value (a blurry total, smudged ID), wrap just that value: `{ "value": "165,000", "confidence": "low", "reason": "ink smudged" }`. Use sparingly (money, IDs, dates, quantities); keep clear values as plain strings.
- **Bounding boxes** — when the user wants to highlight/locate results, add `"bbox": [x, y, w, h]` (normalized 0–1, top-left origin) to any element. Omit if not requested.
- **Mermaid export (diagram only)** — if the user asks for Mermaid, add `"export": { "format": "mermaid", "code": "…" }` consistent with the extracted nodes/edges.
- **Multiple images / multi-page** — wrap results: `{ "batch": true, "count": N, "items": [ <mode object>, … ] }`. Each item is a full self-contained mode object (its own `mode` + `_meta`). For a single image, skip the wrapper.

## Global rules

1. Output ONLY the raw JSON — not one character outside the object.
2. Keep on-screen text in its **original language** (preserve OCR fidelity); write descriptions/`function`/metadata in English by default, or the user's language if asked.
3. Empty sections → `[]` or `null`. Unreadable text → `"[unreadable]"` (or `"[illegible]"` inline within a transcribed string).
4. Preserve visual order (top-to-bottom, left-to-right) and estimate hex colors when not exactly readable.
5. Never put comments inside the JSON.

A consolidated JSON Schema (draft-07, `oneOf` across the five modes) lives in `references/schema.json` for validating outputs. Maintainers: after editing the skill, run `python scripts/validate.py` to confirm every worked example still validates against the schema.
