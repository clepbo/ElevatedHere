# tools

Regenerates `docs/po-qa-traceability.md` and `tools/qa-matrix.json` from the QA item list.

1. Dump a fresh screen index from the Figma page (id, name, x, y, w, h per frame) to
   `tools/screens.json`.
2. `python build_matrix.py screens.json .`
3. `python emit_md.py`

`qa_items.py` is the source of truth. Screen names there are written ASCII-only; the resolver
folds em dashes and middots so they match the real frame names. An unresolved name is printed
rather than silently dropped.
