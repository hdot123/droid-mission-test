# `gh project` JSON fixtures (batch-1)

Recorded shapes from `gh project * --format json` as used in CI contract tests.
Do not hand-edit without updating `test_gh_project_parse_contract.py` envelope registry.

| File | Source command | Envelope |
|------|----------------|----------|
| `item_list_envelope.json` | `gh project item-list` | `{"items", "totalCount"}` |
| `item_list_legacy_array.json` | older / edge `item-list` | bare array |
| `field_list_envelope.json` | `gh project field-list` | `{"fields", "totalCount"}` |
| `project_view.json` | `gh project view` | flat object |