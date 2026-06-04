# UI Mode

Top-level shape (after `mode` + `_meta`):

```json
{
  "mode": "ui",
  "_meta": { ... },
  "header": { ... },
  "navigation": [ ... ],
  "form_elements": [ ... ],
  "actions": [ ... ],
  "data_displays": [ ... ],
  "visual_state": { ... }
}
```

## header

```json
"header": {
  "logo": { "present": true, "description": "circular blue icon with white lock symbol", "position": "top-left" },
  "title": { "text": "Sign In", "style": { "font_size": "24px", "font_weight": "bold", "color": "#1a1a1a", "alignment": "center" } },
  "subtitle": { "text": "Welcome back! Please enter your details.", "style": { "font_size": "14px", "color": "#6b7280", "alignment": "center" } }
}
```

If logo or subtitle is absent, set to `null`.

## navigation

Tabs, menu items, breadcrumbs. `[]` if none. `type` ∈ `tab` | `menu_item` | `breadcrumb` | `navbar_link`.

```json
"navigation": [ { "id": "nav_home", "type": "tab", "text": "Home", "active": true, "link": "#" } ]
```

## form_elements

Every input field, dropdown, checkbox, switch, slider, file upload.

```json
"form_elements": [
  {
    "id": "email",
    "label": { "text": "Email address", "style": { "font_size": "14px", "font_weight": "500", "color": "#374151" } },
    "input": { "type": "email", "placeholder": "you@example.com", "value": "", "style": { "border": "1px solid #d1d5db", "border_radius": "8px", "background": "#ffffff", "padding": "10px 12px" } },
    "icon": { "present": false, "description": null, "position": null },
    "visual_state": { "error": false, "error_message": null, "focused": false, "disabled": false, "special_styles": null },
    "function": "Collects user email for authentication"
  }
]
```

`input.type` ∈ `text` | `email` | `password` | `tel` | `number` | `textarea` | `select` | `checkbox` | `radio` | `date` | `search` | `switch` | `slider` | `file` | `combobox`.
`visual_state.special_styles`: describe unusual cues, e.g. "red border indicating validation error".

## actions

Every button, link, or clickable element. `type` ∈ `button` | `link` | `icon_button` | `fab`.

```json
"actions": [
  {
    "id": "submit_btn", "type": "button", "text": "Sign In",
    "icon": { "present": true, "description": "arrow right icon", "position": "right" },
    "style": { "background": "#2563eb", "color": "#ffffff", "font_size": "16px", "font_weight": "600", "border_radius": "8px", "width": "full", "padding": "12px" },
    "function": "Submits the login form",
    "visual_state": { "disabled": false, "loading": false, "special_styles": null }
  }
]
```

## data_displays

Tables, charts, lists, text blocks, cards. `[]` if none. `type` ∈ `chart` | `table` | `list` | `text_block` | `card` | `alert` | `badge` | `avatar`.

```json
"data_displays": [
  {
    "id": "sales_chart", "type": "chart", "title": "Monthly Revenue",
    "description": "Bar chart showing monthly sales data for the past 6 months",
    "visual_style": { "height": "300px", "colors": ["#2563eb", "#93c5fd"] }
  }
]
```

For `type: "table"`, you may add `columns`, `rows`, and a `visual_style.sort` object (see rule 7 below).

## visual_state (top-level)

```json
"visual_state": {
  "background": "#f9fafb", "card_present": true,
  "card_style": { "background": "#ffffff", "border_radius": "12px", "shadow": "0 4px 24px rgba(0,0,0,0.08)", "padding": "32px" },
  "overall_theme": "light", "layout": "centered single-column form"
}
```

## Rules

1. Output ONLY the raw JSON.
2. On-screen text keeps its original language; descriptions/`function`/metadata in English by default.
3. Empty sections → `[]` or `null`. Estimate hex colors when not exact.
4. Unreadable text → `"[unreadable]"`. Preserve visual order top-to-bottom, left-to-right.
5. Include ALL interactive elements — even tiny ones like a "Remember me" checkbox or social-login button.
6. For desktop-app windows, also capture the **window controls** (minimize, maximize/restore, close ✕) top-right as `actions` with `type: "icon_button"` — don't drop them because they sit in the title bar.
7. Capture **stateful affordances**, not just static text:
   - Table sort: a caret/triangle above a column header (▲ asc, ▼ desc) marks the active sort — record it as `"sort": { "column": "Name", "direction": "asc" }` in the table's `visual_style`.
   - Input focus: a blinking cursor or active highlight → set `visual_state.focused: true`.
8. Never add comments inside the JSON.

---

## Worked Example

Below is a complete, fully valid JSON output representing a typical login screen:

```json
{
  "mode": "ui",
  "_meta": {
    "schema_version": "1.0.2",
    "source": "screenshot",
    "image_orientation": "portrait",
    "detected_language": "en",
    "confidence": "high",
    "notes": "Standard login screen mockup"
  },
  "header": {
    "logo": {
      "present": true,
      "description": "circular blue logo with white letter A",
      "position": "top-center"
    },
    "title": {
      "text": "Welcome Back",
      "style": {
        "font_size": "24px",
        "font_weight": "bold",
        "color": "#111827",
        "alignment": "center"
      }
    },
    "subtitle": {
      "text": "Sign in to your account to continue",
      "style": {
        "font_size": "14px",
        "color": "#4b5563",
        "alignment": "center"
      }
    }
  },
  "navigation": [],
  "form_elements": [
    {
      "id": "email_input",
      "label": {
        "text": "Email",
        "style": {
          "font_size": "14px",
          "font_weight": "500",
          "color": "#374151"
        }
      },
      "input": {
        "type": "email",
        "placeholder": "Enter your email",
        "value": "",
        "style": {
          "border": "1px solid #d1d5db",
          "border_radius": "6px",
          "background": "#ffffff",
          "padding": "8px 12px"
        }
      },
      "icon": {
        "present": false,
        "description": null,
        "position": null
      },
      "visual_state": {
        "error": false,
        "error_message": null,
        "focused": false,
        "disabled": false,
        "special_styles": null
      },
      "function": "Collects user email address"
    },
    {
      "id": "password_input",
      "label": {
        "text": "Password",
        "style": {
          "font_size": "14px",
          "font_weight": "500",
          "color": "#374151"
        }
      },
      "input": {
        "type": "password",
        "placeholder": "••••••••",
        "value": "",
        "style": {
          "border": "1px solid #d1d5db",
          "border_radius": "6px",
          "background": "#ffffff",
          "padding": "8px 12px"
        }
      },
      "icon": {
        "present": false,
        "description": null,
        "position": null
      },
      "visual_state": {
        "error": false,
        "error_message": null,
        "focused": false,
        "disabled": false,
        "special_styles": null
      },
      "function": "Collects user password"
    }
  ],
  "actions": [
    {
      "id": "forgot_pwd_link",
      "type": "link",
      "text": "Forgot password?",
      "icon": {
        "present": false,
        "description": null,
        "position": null
      },
      "style": {
        "background": "transparent",
        "color": "#2563eb",
        "font_size": "14px",
        "font_weight": "500",
        "border_radius": null,
        "width": "auto",
        "padding": null
      },
      "function": "Navigates user to password recovery page",
      "visual_state": {
        "disabled": false,
        "loading": false,
        "special_styles": "right-aligned above password input or next to label"
      }
    },
    {
      "id": "sign_in_button",
      "type": "button",
      "text": "Sign in",
      "icon": {
        "present": false,
        "description": null,
        "position": null
      },
      "style": {
        "background": "#2563eb",
        "color": "#ffffff",
        "font_size": "16px",
        "font_weight": "600",
        "border_radius": "6px",
        "width": "full",
        "padding": "10px"
      },
      "function": "Validates credentials and submits login form",
      "visual_state": {
        "disabled": false,
        "loading": false,
        "special_styles": "primary button with slight drop shadow"
      }
    }
  ],
  "data_displays": [],
  "visual_state": {
    "background": "#f3f4f6",
    "card_present": true,
    "card_style": {
      "background": "#ffffff",
      "border_radius": "8px",
      "shadow": "0 1px 3px rgba(0,0,0,0.1)",
      "padding": "24px"
    },
    "overall_theme": "light",
    "layout": "centered single-column login card"
  }
}
```

