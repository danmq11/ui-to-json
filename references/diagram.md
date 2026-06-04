# Diagram Mode

For flowcharts, mindmaps, org charts, UML, ER diagrams, network/architecture, BPMN, swimlanes, wireflows.

Top-level shape (after `mode` + `_meta`):

```json
{
  "mode": "diagram",
  "_meta": { ... },
  "diagram_type": "...",
  "title": "...",
  "layout_direction": "...",
  "nodes": [ ... ],
  "edges": [ ... ],
  "groups": [ ... ],
  "legend": [ ... ],
  "visual_state": { ... }
}
```

## diagram_type
`flowchart` | `mindmap` | `org_chart` | `uml_class` | `uml_sequence` | `er_diagram` | `network` | `architecture` | `bpmn` | `swimlane` | `wireflow` | `other`.

## layout_direction
`top-to-bottom` | `left-to-right` | `radial` | `bottom-to-top` | `null`.

## nodes
Every box/shape/element. Each needs a stable `id` for edges to reference.
```json
"nodes": [
  { "id": "n1", "parent_id": null, "label": "Start", "shape": "oval", "type": "start", "group": null, "position": "top-center", "style": { "fill": "#dcfce7", "border": "#16a34a", "text_color": "#14532d" }, "description": "Entry point" },
  { "id": "n2", "parent_id": "n1", "label": "Is user logged in?", "shape": "diamond", "type": "decision", "group": null, "position": "center", "style": { "fill": "#fef9c3", "border": "#ca8a04", "text_color": "#713f12" }, "description": "Auth check" }
]
```
Two distinct relationship fields — don't conflate:
- `parent_id`: hierarchical parent in a tree (mindmaps, org charts). `null` for roots.
- `group`: id of a visual container/swimlane from `groups` that this node sits inside. `null` if none. This is the source of truth for grouping; `groups[].node_ids` mirrors it — keep them consistent.

`shape` e.g. `rectangle` | `rounded_rectangle` | `oval` | `diamond` | `parallelogram` | `circle` | `cylinder` | `cloud` | `actor` | `hexagon`.
`type` (semantic) e.g. `start` | `end` | `process` | `decision` | `input_output` | `data` | `database` | `entity` | `class` | `actor` | `service` | `subprocess` | `note`.

## edges
Every connector/arrow/line.
```json
"edges": [
  { "id": "e1", "from": "n1", "to": "n2", "label": null, "direction": "directed", "style": { "line": "solid", "arrow": "single", "color": "#374151" } },
  { "id": "e2", "from": "n2", "to": "n3", "label": "Yes", "direction": "directed", "style": { "line": "solid", "arrow": "single", "color": "#374151" } }
]
```
`direction`: `directed` | `bidirectional` | `undirected`. `style.line`: `solid`/`dashed`/`dotted`. `style.arrow`: `single`/`double`/`none`/`diamond`/`circle`.
For UML/ER use `label` for multiplicity/relationship (`"1..*"`, `"inherits"`, `"has many"`).

## groups
Containers/swimlanes/clusters/boundaries. `[]` if none. `type` e.g. `swimlane` | `boundary` | `cluster` | `package` | `subgraph`.
```json
"groups": [ { "id": "g1", "label": "Backend Services", "type": "boundary", "node_ids": ["n3", "n4", "n5"], "style": { "fill": "#eff6ff", "border": "#2563eb" } } ]
```

## legend
Key for colors/shapes/symbols if the diagram provides one. `[]` if absent.
```json
"legend": [ { "symbol": "green oval", "meaning": "Start / End" }, { "symbol": "yellow diamond", "meaning": "Decision" } ]
```

## visual_state
```json
"visual_state": { "node_count": 6, "edge_count": 7, "overall_theme": "light", "color_coded": true, "special_notes": null }
```

## Mermaid export (optional)
If the user asks for Mermaid, add an `export` key consistent with nodes/edges:
```json
"export": { "format": "mermaid", "code": "flowchart TD\n  n1([Start]) --> n2{Is user logged in?}\n  n2 -- Yes --> n3[Dashboard]\n  n2 -- No --> n4[Login]" }
```

## Rules

1. Output ONLY the raw JSON.
2. Every node has a unique `id`; every edge's `from`/`to` references an existing node id.
3. List nodes/edges in execution/reading order (step-by-step flow).
4. Capture edge labels verbatim (conditions like "Yes"/"No", multiplicities, verbs).
5. Transcribe node labels exactly; unreadable → `"[illegible]"`.
6. Never add comments inside the JSON.

---

## Worked Example

Below is a complete, fully valid JSON output representing a flowchart diagram:

```json
{
  "mode": "diagram",
  "_meta": {
    "schema_version": "1.0.0",
    "source": "screenshot",
    "image_orientation": "portrait",
    "detected_language": "en",
    "confidence": "high",
    "notes": "Simple authentication flowchart diagram"
  },
  "diagram_type": "flowchart",
  "title": "User Authentication Flow",
  "layout_direction": "top-to-bottom",
  "nodes": [
    {
      "id": "start_node",
      "parent_id": null,
      "label": "Start",
      "shape": "oval",
      "type": "start",
      "group": null,
      "position": "top",
      "style": {
        "fill": "#dcfce7",
        "border": "#16a34a",
        "text_color": "#14532d"
      },
      "description": "Entry point for authentication check"
    },
    {
      "id": "check_login",
      "parent_id": "start_node",
      "label": "Is user logged in?",
      "shape": "diamond",
      "type": "decision",
      "group": null,
      "position": "center",
      "style": {
        "fill": "#fef9c3",
        "border": "#ca8a04",
        "text_color": "#713f12"
      },
      "description": "Decision based on session state"
    },
    {
      "id": "show_dashboard",
      "parent_id": "check_login",
      "label": "Show Dashboard",
      "shape": "rectangle",
      "type": "process",
      "group": "client_area",
      "position": "bottom-left",
      "style": {
        "fill": "#eff6ff",
        "border": "#2563eb",
        "text_color": "#1e3a8a"
      },
      "description": "Redirects logged-in user to dashboard"
    },
    {
      "id": "show_login",
      "parent_id": "check_login",
      "label": "Redirect to Login",
      "shape": "rectangle",
      "type": "process",
      "group": "guest_area",
      "position": "bottom-right",
      "style": {
        "fill": "#fee2e2",
        "border": "#dc2626",
        "text_color": "#7f1d1d"
      },
      "description": "Redirects guest to login form"
    }
  ],
  "edges": [
    {
      "id": "edge_1",
      "from": "start_node",
      "to": "check_login",
      "label": null,
      "direction": "directed",
      "style": {
        "line": "solid",
        "arrow": "single",
        "color": "#374151"
      }
    },
    {
      "id": "edge_2",
      "from": "check_login",
      "to": "show_dashboard",
      "label": "Yes",
      "direction": "directed",
      "style": {
        "line": "solid",
        "arrow": "single",
        "color": "#374151"
      }
    },
    {
      "id": "edge_3",
      "from": "check_login",
      "to": "show_login",
      "label": "No",
      "direction": "directed",
      "style": {
        "line": "solid",
        "arrow": "single",
        "color": "#374151"
      }
    }
  ],
  "groups": [
    {
      "id": "client_area",
      "label": "Authorized Area",
      "type": "boundary",
      "node_ids": ["show_dashboard"],
      "style": {
        "fill": "#f8fafc",
        "border": "#64748b"
      }
    },
    {
      "id": "guest_area",
      "label": "Public Area",
      "type": "boundary",
      "node_ids": ["show_login"],
      "style": {
        "fill": "#f8fafc",
        "border": "#64748b"
      }
    }
  ],
  "legend": [],
  "visual_state": {
    "node_count": 4,
    "edge_count": 3,
    "overall_theme": "light",
    "color_coded": true,
    "special_notes": null
  },
  "export": {
    "format": "mermaid",
    "code": "flowchart TD\n  start_node([Start]) --> check_login{Is user logged in?}\n  check_login -- Yes --> show_dashboard[Show Dashboard]\n  check_login -- No --> show_login[Redirect to Login]"
  }
}
```

