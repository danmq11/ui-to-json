# Scene Mode

Top-level shape (after `mode` + `_meta`):

```json
{
  "mode": "scene",
  "_meta": { ... },
  "scene_description": "...",
  "art_style": { ... },
  "composition": { ... },
  "main_subjects": [ ... ],
  "background_elements": [ ... ],
  "text_in_scene": [ ... ],
  "lighting_and_atmosphere": { ... },
  "colors_dominant": [ ... ]
}
```

## scene_description

One string: overall setting, location, time of day, season, mood.
`"A cozy coffee shop interior on a rainy autumn morning, warm and intimate, soft daylight through fogged windows."`

## art_style

```json
"art_style": { "medium": "realistic photograph", "genre": "portrait" }
```
`medium` e.g. `realistic photograph` | `digital painting` | `watercolor` | `3D render` | `sketch` | `oil painting` | `pixel art`.
`genre` e.g. `landscape` | `portrait` | `street photography` | `still life` | `abstract` | `architectural`.

## composition

```json
"composition": { "camera_angle": "eye-level", "shot_type": "medium-wide shot", "depth_of_field": "shallow" }
```
`camera_angle`: `eye-level` | `low-angle` | `high-angle` | `bird's-eye` | `dutch angle`.
`shot_type`: `close-up` | `medium shot` | `medium-wide shot` | `wide shot` | `extreme wide shot`.
`depth_of_field`: `shallow` | `deep` | `moderate` | `null`.

## main_subjects

Most prominent people/animals/objects, ordered most→least prominent.

```json
"main_subjects": [
  { "type": "person", "name": "young woman", "appearance": "shoulder-length brown hair, beige knit sweater, mid-20s", "position": "center foreground", "action_or_expression": "reading a book and smiling softly", "interaction": "holding a ceramic mug, leaning over a wooden table" },
  { "type": "object", "name": "wooden table", "appearance": "rustic oak, rectangular", "position": "center, lower third", "action_or_expression": null, "interaction": "supports the mug and an open book" }
]
```
`type`: `person` | `animal` | `object`. `action_or_expression`: `null` for inanimate objects.

## background_elements

Descriptive strings: `["blurred bookshelf along the back wall", "string lights on the ceiling", "rain streaks on the glass"]`

## text_in_scene

OCR of any visible text (signs, labels, screens, handwriting). `[]` if none.

```json
"text_in_scene": [ { "text": "OPEN", "location": "storefront window, upper left", "style": "neon sign, red glow" } ]
```

## lighting_and_atmosphere

```json
"lighting_and_atmosphere": { "light_source": "natural daylight from left window + warm string lights", "intensity": "soft and diffused", "color_temperature": "warm", "mood": "calm, nostalgic" }
```

## colors_dominant

```json
"colors_dominant": [ { "color": "warm beige", "hex": "#d8c3a5", "usage": "sweater and walls" }, { "color": "deep brown", "hex": "#5a3e2b", "usage": "wooden furniture" } ]
```

## Rules

1. Output ONLY the raw JSON.
2. Infer reasonably from visual cues; genuinely unclear → `null` or `"[unclear]"`.
3. Estimate hex colors when not exact. Be specific and concrete; favor observable detail.
4. Never add comments inside the JSON.

---

## Worked Example

Below is a complete, fully valid JSON output representing a photo of a desktop workspace scene:

```json
{
  "mode": "scene",
  "_meta": {
    "schema_version": "1.0.1",
    "source": "photo",
    "image_orientation": "landscape",
    "detected_language": "en",
    "confidence": "high",
    "notes": "Cozy workspace setup photo"
  },
  "scene_description": "A clean, modern workspace on a wooden desk next to a window with soft natural light.",
  "art_style": {
    "medium": "realistic photograph",
    "genre": "still life"
  },
  "composition": {
    "camera_angle": "high-angle",
    "shot_type": "close-up",
    "depth_of_field": "shallow"
  },
  "main_subjects": [
    {
      "type": "object",
      "name": "laptop",
      "appearance": "silver aluminum chassis, open screen showing line charts, black keyboard",
      "position": "center foreground",
      "action_or_expression": null,
      "interaction": "sitting on the desk surface, plugged into power on the side"
    },
    {
      "type": "object",
      "name": "coffee mug",
      "appearance": "matte black ceramic, steam rising slightly",
      "position": "right midground",
      "action_or_expression": null,
      "interaction": "rests on a cork coaster next to the laptop"
    }
  ],
  "background_elements": [
    "potted succulent plant in a white ceramic pot",
    "window with green leaves visible outside in soft focus",
    "wood grain texture of the desk surface"
  ],
  "text_in_scene": [
    {
      "text": "Weekly Progress",
      "location": "laptop screen header",
      "style": "sans-serif, bold, dark gray"
    }
  ],
  "lighting_and_atmosphere": {
    "light_source": "diffused natural light from the side window",
    "intensity": "soft and gentle",
    "color_temperature": "neutral",
    "mood": "calm, productive, organized"
  },
  "colors_dominant": [
    {
      "color": "natural wood brown",
      "hex": "#b58a63",
      "usage": "desk surface"
    },
    {
      "color": "matte black",
      "hex": "#1a1a1a",
      "usage": "coffee mug and keyboard keys"
    },
    {
      "color": "metallic silver",
      "hex": "#d1d5db",
      "usage": "laptop body"
    }
  ]
}
```

