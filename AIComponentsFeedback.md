# AI Components Feedback

**Date:** 2026-07-13

## For Nepta

### A1. [Bug] Wrong env var in `list_models()` — blocks model dropdown
**File:** `services/ai_service.py`, line 14

```python
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
```

This is a leftover/remnant — `GOOGLE_API_KEY` was never set in the `.env` file and isn't used anywhere else in the project. Only `GEMINI_API_KEY` exists. This means the model dropdown in the UI never populates — the client is created with `None` as the key. You can just delete this reference and use `GEMINI_API_KEY` instead.

**Fix:** Change to `os.environ.get("GEMINI_API_KEY")` and remove the unused `GOOGLE_API_KEY` env var reference entirely.

---

### A2. [Potential Bug] Model name mismatch between dropdown and API call
**File:** `services/ai_service.py`, lines 17 and 76

`list_models()` strips `models/` prefix from model names (line 17):
```python
models.append(name.replace("models/", ""))
```

But `analyze_page()` defaults to `"gemini-flash-lite-latest"` (line 42, 74). If the real API model name is e.g. `"models/gemini-2.0-flash-lite-latest"`, the dropdown shows the stripped version but the default hardcoded string in `analyze_page` might not match. Worth verifying that the hardcoded default exists in the dropdown values.

---

### A3. [Improvement] Prompt needs strengthening
**File:** `services/ai_service.py`, lines 56-69

The current prompt:
- Has **no few-shot examples** — adding 1-2 examples of expected output for typical toll report layouts would dramatically improve accuracy
- Has **no temperature=0** — for structured data extraction, setting `temperature=0` (or close to it) is standard practice to get deterministic results
- **Groups tolls by amount** — the prompt asks the AI to both identify AND count duplicates. This is risky for OCR: if the AI misses one occurrence of a toll, the total is silently wrong. Consider asking the AI to list every toll individually and let the Python code handle counting/grouping

**Suggested improvement:**
- Add `temperature=0` to the generate call
- Include 1-2 few-shot examples in the prompt describing typical toll layouts
- Consider changing the JSON schema to list individual transactions instead of grouping

---

### A4. [Improvement] No JSON repair on malformed AI output
**File:** `services/ai_service.py`, line 85

```python
data = json.loads(text)
```

If the AI returns slightly malformed JSON (trailing comma, unquoted key, extra bracket), `json.loads()` crashes with no retry. No repair logic or fallback exists.

**Ideas:**
- Catch `json.JSONDecodeError` and send the malformed response back to the AI once with "fix the JSON"
- Or add basic regex/string cleaning before parsing

---

### A5. [Improvement] `list_models()` has no error handling
**File:** `services/ai_service.py`, lines 10-18

If the API call fails (no internet, bad key, rate limit), it returns an empty list silently. The user sees an empty dropdown with no explanation.

**Fix:** Wrap in try/except and return at least the hardcoded default model so the dropdown always has a fallback option.

---

### A6. [UX] UI freezes during AI analysis
**File:** `gui/app.py`, lines 286-308

`on_run_analysis()` calls `self.ai_service.analyze_page(img)` synchronously on the main UI thread. While waiting for the Gemini API response, the entire app freezes — no progress indicator, no cancel button.

**Fix:** Wrap the API call in `threading.Thread` (or `asyncio`), show a spinner/loading indicator, and disable the Analyze button during the call. Also surface errors to the user via `messagebox` instead of just `print()`.

---

## Summary by priority

| Priority | Item | Impact |
|----------|------|--------|
| Critical | A1 — Wrong env var | Model dropdown never works |
| High | A6 — UI freeze | App unusable during analysis |
| High | A3 — Weak prompt | Poor extraction accuracy |
| Medium | A4 — No JSON repair | Crashes on slightly bad AI output |
| Medium | A2 — Model name mismatch | Possible silent failure |
| Low | A5 — No error handling in list_models | Empty dropdown, no user feedback |
