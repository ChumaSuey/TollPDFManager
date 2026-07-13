# Changelog

## beta-v2 — 2026-07-13 (latest)

### Bug Fixes

#### `services/data_service.py`
- **Fixed duplicate/orphaned `except` blocks** in `get_processed_tolls()` — had a copy-paste error with two detached `except` clauses and an unreachable `return set()` that would cause a syntax error if that code path was hit.
- **Fixed `get_excel_path()` folder priority** — the `folder_path` argument was silently ignored when `export_folder` existed in config. Now uses `folder_path or config.get("export_folder") or os.getcwd()` so the explicit argument takes priority.
- **Fixed corrupted JSON crash** in `load_config()` — now handles empty files, catches `json.JSONDecodeError`, and renames corrupted files to `.corrupted` instead of crashing.
- **Fixed corrupted JSON crash** in `load_flags()` — same treatment: empty file check, `json.JSONDecodeError` handling, corrupted file rename.
- **Fixed atomic file writes** in `save_config()` and `save_flags()` — now write to a `.tmp` file first then `os.replace()`, preventing half-written files if the pendrive disconnects mid-save.

#### `gui/pdf_viewer.py`
- **Fixed page numbering dead code** — removed a redundant `page_num + 1` line that was immediately overwritten, plus the confused developer commentary about 0-based vs 1-based indexing.

### Improvements

#### `services/data_service.py`
- **Extracted repeated styling code** — added `_apply_excel_styling()` helper method to replace 3 duplicate blocks of openpyxl border/alignment code. Removed unused imports in `delete_toll_entry()`.
- **Added UTF-8 encoding** to all `json.load()`/`json.dump()` file operations.

#### `gui/calculator.py`
- **Live inline editing** — clicking away (FocusOut) from an inline edit now **confirms and saves** the value instead of cancelling. Added a guard to prevent recursion when the popup is destroyed. Enter still confirms, Escape still cancels.
- **Removed leftover dev comments** — cleaned up AI-generated placeholder notes in `__init__`.

#### `gui/app.py`
- **Cleaned up navigation** — replaced `print()` debug statements with silent `pass` in `navigate_file()`.

#### `tests/test_tracking.py`
- **Improved test mocking** — replaced fragile module-level monkeypatching of `DataService.load_config` (which could leak state across test runs) with proper `unittest.mock.patch` decorators. Removed the malformed `import json` comment mid-file.

### New Files
- `AIComponentsFeedback.md` — AI-related issues documented for external review (prompt improvements, env var bug, UI freeze, etc.)
- `CHANGELOG.md` — this file
