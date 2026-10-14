# tools

Builds the QA traceability matrix in three forms: the markdown in `docs/`, the published
claude.ai artifact, and the GitHub Pages copy at `/qa-register/`.

The requirement text is never written by hand. It is extracted verbatim from the QA PDF so a row
here reads exactly like the row in the document.

## Pipeline

```
PO - Finance QA.pdf
  |  pdftotext -table                      preserves column positions
  v
tbl.txt
  |  parse_qa_pdf.py tbl.txt qa-source.json
  v
qa-source.json      the document's own wording and order
  +  qa_map.py      what changed, and which screens it lives on
  +  screens.json   id/name/x/y/w/h for every frame on the Figma page
  |  build_matrix.py screens.json .
  v
qa-matrix.json
  |  emit_md.py     -> docs/po-qa-traceability.md
  |  emit_html.py   -> tools/qa-register.html  (artifact; marks shared via the db capability)
  |                 -> qa-register/index.html  (Pages; marks kept per browser)
```

## Refreshing it

1. Dump a fresh screen index from the Figma page to `tools/screens.json`.
2. `python parse_qa_pdf.py tbl.txt qa-source.json` (only needed if the QA document changes).
3. `python build_matrix.py screens.json .`
4. `python emit_md.py && python emit_html.py`
5. Republish `tools/qa-register.html` to the existing artifact URL; commit `qa-register/index.html`.

An unresolved screen name or an unmapped QA item is printed rather than silently dropped, so step
3 fails loudly if `qa_map.py` drifts from the Figma file.

## Parser notes

The PDF's tables are recovered from column positions, not from reading order. Per page the parser
finds the blank gutters, slices each line into cells, and starts a new record on the empty-to-text
transition in column 0. Two things it handles that are easy to miss:

- The document breaks words across lines without hyphens, so `Reconciliatio` + `n Workspace` has to
  be re-fused. The suffix list deliberately excludes real two-letter words.
- The review table's numbering skips 3, 33, 54 and 55, and runs 57 before 56. Row 3 holds only a
  repeated table header. 54 real items, not 58.

Rows 26 and 58 sit on pages whose grid cannot be recovered and are transcribed by hand in
`parse_qa_pdf.py`; that is the only hand-entered requirement text.
