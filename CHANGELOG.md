# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.2] - 2026-06-05

### Added
- **Edge-case handling** in `SKILL.md`: explicit guidance for blank/empty/unreadable images
  (low-confidence empty result), QR codes & barcodes (captured with `code_type` / `key_values`),
  and cropped images (truncated values wrapped with field-level confidence).
- Richer second worked examples for `scene` (people + animal + QR sign) and `data_viz`
  (line chart with a gridline-estimated, confidence-wrapped value).
- `requirements.txt` (`jsonschema`, `PyYAML`) for `scripts/validate.py` and CI.

### Changed
- Bumped schema `$id`/`version` and all `schema_version` values to `1.0.2`.

## [1.0.1] - 2026-06-04

### Changed
- `schema_version` is now a **required** field inside `_meta` (was optional), so every
  output is explicitly version-stamped and validators enforce it.
- Bumped schema `$id`/`version` and all `schema_version` values to `1.0.1`.

### Fixed
- Table cells (`tables[].rows` and `data_displays[].rows`) now accept the field-level
  confidence object `{ value, confidence, reason }`, not just plain strings. Previously the
  skill instructed wrapping uncertain values but the schema rejected them — outputs the skill
  itself produced could fail validation. Discovered via a real image benchmark.

## [1.0.0] - 2026-06-04

### Added
- Initial release. Five extraction modes: `ui`, `scene`, `document`, `diagram`, `data_viz`.
- Universal envelope (`mode` + `_meta`) for parser routing.
- Cross-mode conventions: field-level confidence, normalized bounding boxes, Mermaid export
  for diagrams, and multi-image / multi-page batching.
- Consolidated JSON Schema (draft-07) in `references/schema.json` with a worked example per mode.
- `scripts/validate.py` to validate every worked example against the schema; wired into CI.
- Progressive-disclosure layout: lean `SKILL.md` plus per-mode reference files.

[1.0.2]: https://github.com/danmq11/ui-to-json/releases/tag/v1.0.2
[1.0.1]: https://github.com/danmq11/ui-to-json/releases/tag/v1.0.1
[1.0.0]: https://github.com/danmq11/ui-to-json/releases/tag/v1.0.0
