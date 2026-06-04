# Data-viz Mode

For a standalone chart/graph where the goal is to recover the underlying data.

Top-level shape (after `mode` + `_meta`):

```json
{
  "mode": "data_viz",
  "_meta": { ... },
  "chart_type": "...",
  "title": "...",
  "subtitle": "...",
  "axes": { ... },
  "series": [ ... ],
  "annotations": [ ... ],
  "legend_position": "...",
  "source_note": "...",
  "visual_state": { ... }
}
```

## chart_type
`bar` | `grouped_bar` | `stacked_bar` | `horizontal_bar` | `line` | `multi_line` | `area` | `pie` | `donut` | `scatter` | `bubble` | `histogram` | `radar` | `gauge` | `combo` | `other`.

## axes
For pie/donut set `x`/`y` to `null` and rely on `series`.
```json
"axes": {
  "x": { "label": "Month", "unit": null, "type": "category", "categories": ["Jan", "Feb", "Mar"] },
  "y": { "label": "Revenue", "unit": "USD (thousands)", "type": "numeric", "min": 0, "max": 120, "scale": "linear" }
}
```
`type`: `category` | `numeric` | `time` | `log`. `categories` only for categorical axes.

## series
The heart of the extraction.
```json
"series": [
  { "name": "Product A", "color": "#2563eb", "points": [ { "x": "Jan", "y": 45 }, { "x": "Feb", "y": 52 }, { "x": "Mar", "y": 60 } ] },
  { "name": "Product B", "color": "#f59e0b", "points": [ { "x": "Jan", "y": 30 }, { "x": "Feb", "y": 28 }, { "x": "Mar", "y": 41 } ] }
]
```
- Pie/donut: one series; each point's `x` = slice label, `y` = value; add `"percent"` when shown.
- A `y` read off the plot (not a printed label) gets field-level confidence: `"y": { "value": 52, "confidence": "medium" }`.
- Printed data labels → use them directly, confidence `high`.

## annotations
Callouts, trend/target lines, highlighted points. `[]` if none.
```json
"annotations": [ { "type": "target_line", "label": "Goal", "value": 100, "axis": "y" }, { "type": "callout", "label": "Record high", "at": { "x": "Mar", "y": 60 } } ]
```

## Other fields
- `subtitle`, `source_note`: strings or `null`.
- `legend_position`: `top` | `bottom` | `left` | `right` | `inline` | `null`.
- `visual_state`: `{ "overall_theme": "light", "gridlines": true, "data_labels_shown": false, "special_notes": null }`.

## Rules

1. Output ONLY the raw JSON.
2. Prefer printed data labels; else estimate against gridlines and mark estimates with field-level confidence.
3. Preserve series order and point order (left-to-right along x).
4. Keep axis units and category labels verbatim; don't convert units.
5. Don't fabricate precision — round estimated reads to the nearest gridline step.
6. Never add comments inside the JSON.

---

## Worked Example

Below is a complete, fully valid JSON output representing a grouped bar chart:

```json
{
  "mode": "data_viz",
  "_meta": {
    "schema_version": "1.0.2",
    "source": "screenshot",
    "image_orientation": "landscape",
    "detected_language": "en",
    "confidence": "high",
    "notes": "Grouped bar chart showing monthly product sales"
  },
  "chart_type": "grouped_bar",
  "title": "Monthly Product Sales Comparison",
  "subtitle": "Q1 2026 Sales Data for Product A vs Product B",
  "axes": {
    "x": {
      "label": "Month",
      "unit": null,
      "type": "category",
      "categories": ["January", "February", "March"]
    },
    "y": {
      "label": "Units Sold",
      "unit": "thousand units",
      "type": "numeric",
      "min": 0,
      "max": 150,
      "scale": "linear"
    }
  },
  "series": [
    {
      "name": "Product A",
      "color": "#2563eb",
      "points": [
        { "x": "January", "y": 85 },
        { "x": "February", "y": 92 },
        { "x": "March", "y": 115 }
      ]
    },
    {
      "name": "Product B",
      "color": "#f59e0b",
      "points": [
        { "x": "January", "y": 70 },
        { "x": "February", "y": 78 },
        { "x": "March", "y": 95 }
      ]
    }
  ],
  "annotations": [
    {
      "type": "target_line",
      "label": "Target Goal",
      "value": 100,
      "axis": "y"
    }
  ],
  "legend_position": "bottom",
  "source_note": "Source: Internal Sales Database Q1",
  "visual_state": {
    "overall_theme": "light",
    "gridlines": true,
    "data_labels_shown": true,
    "special_notes": "Both products show positive trend; Product A exceeds target in March."
  }
}
```



## Worked Example 2 — line chart with a gridline-estimated value

Shows a value read off the plot (no printed label) wrapped with field-level confidence, plus a callout annotation.

```json
{
  "mode": "data_viz",
  "_meta": {
    "schema_version": "1.0.2",
    "source": "screenshot",
    "image_orientation": "landscape",
    "detected_language": "en",
    "confidence": "medium",
    "notes": "Single-line chart; some points read against gridlines"
  },
  "chart_type": "line",
  "title": "Website Daily Active Users",
  "subtitle": "Last 5 days",
  "axes": {
    "x": { "label": "Day", "unit": null, "type": "category", "categories": ["Mon", "Tue", "Wed", "Thu", "Fri"] },
    "y": { "label": "DAU", "unit": "users", "type": "numeric", "min": 0, "max": 5000, "scale": "linear" }
  },
  "series": [
    {
      "name": "DAU",
      "color": "#16a34a",
      "points": [
        { "x": "Mon", "y": 2100 },
        { "x": "Tue", "y": 2650 },
        { "x": "Wed", "y": { "value": 3200, "confidence": "medium", "reason": "no data label; read between the 3000 and 3500 gridlines" } },
        { "x": "Thu", "y": 3050 },
        { "x": "Fri", "y": 4180 }
      ]
    }
  ],
  "annotations": [
    { "type": "callout", "label": "Friday launch spike", "at": { "x": "Fri", "y": 4180 } }
  ],
  "legend_position": "none",
  "source_note": "Source: Analytics dashboard",
  "visual_state": { "overall_theme": "light", "gridlines": true, "data_labels_shown": false, "special_notes": "Sharp rise on Friday after a product launch." }
}
```
