# PLAN — design (capture-update-value-language-and-type-changes)

> EPIC: capture-update-value-language-and-type-changes. PLAN ≡ this design + `tasks.md`.

## The defect, precisely

All four value-update templates carry the same pairing FILTER (line numbers as of `main`):

| Template | FILTER block |
|---|---|
| `property_value_updates.rq` | ~158–167 |
| `reified_property_value_updates.rq` | ~162–171 |
| `count_property_value_updates.rq` | ~102–114 |
| `count_reified_property_value_updates.rq` | ~106–114 |

Current form:

```sparql
FILTER (
  (
    # Case 1: Both values are language-tagged literals
    (isLiteral(?oldValue) && isLiteral(?newValue) && lang(?oldValue) != "" && lang(?newValue) != "" && lang(?oldValue) = lang(?newValue))
    ||
    # Case 2: Both values are non-language-tagged literals or URIs
    ((!isLiteral(?oldValue) || lang(?oldValue) = "") && (!isLiteral(?newValue) || lang(?newValue) = ""))
  )
  && ?oldValue != ?newValue
)
```

`?oldValue`/`?newValue` are already constrained to the same `?instance`/`?property` (or
`?object`/`?objProperty` for the reified path) and to the deletions/insertions graphs. So
relaxing the disjunction does not widen the join — it only stops discarding two legitimate
old↔new pairings.

## The fix

Append two cases inside the existing disjunction; keep the `&& ?oldValue != ?newValue` guard:

```sparql
FILTER (
  (
    # Case 1: Both values are language-tagged literals with the same tag (changed text)
    (isLiteral(?oldValue) && isLiteral(?newValue) && lang(?oldValue) != "" && lang(?newValue) != "" && lang(?oldValue) = lang(?newValue))
    ||
    # Case 2: Both values are non-language-tagged literals or URIs
    ((!isLiteral(?oldValue) || lang(?oldValue) = "") && (!isLiteral(?newValue) || lang(?newValue) = ""))
    ||
    # Case 3 (#142): same lexical text, changed or removed language tag
    (str(?oldValue) = str(?newValue))
    ||
    # Case 4 (#143): exactly one side is a literal (datatype <-> object property)
    (isLiteral(?oldValue) != isLiteral(?newValue))
  )
  && ?oldValue != ?newValue
)
```

Apply identically to all four templates. The two `count_*` templates `SELECT (COUNT(...))`
over the same WHERE/FILTER, so an identical relaxation keeps counts consistent with the detail
queries (DEC-1).

### Edge cases the relaxation must not regress

- **Identical value** (`"x"@en` → `"x"@en`): excluded by `?oldValue != ?newValue` (rdflib/SPARQL
  term equality includes the tag). ✔
- **Same text, same tag, different text only**: Case 1 already handles it. ✔
- **Multiple values on one instance+property**: pairing remains bounded; Case 3/4 only add
  pairs that share text or cross the literal/IRI boundary — both deliberate. Document that a
  multi-valued property with several simultaneous changes can yield several update rows (true
  today too).

## Verification (DEC-3)

1. **Generator unit test** (extend `tests/unit/test_query_generator.py` or
   `test_queries_generator.py`): render a value-update query for a sample property and assert
   the rendered text contains the four FILTER cases (markers `str(?oldValue) = str(?newValue)`
   and `isLiteral(?oldValue) != isLiteral(?newValue)`).
2. **Regenerate expected fixtures**: the committed `tests/test_data/**/test_queries/value_update_*.rq`
   reflect the old FILTER. Regenerate (or update) them so the generator-vs-expected comparison
   tests stay green. List which fixtures changed.
3. **Optional semantic check (recommended, mirrors rdf-differ 2.3.0):** an rdflib test that runs
   a rendered value-update query against a minimal in-memory skos-history dataset and asserts a
   tag-change row, a tag-removal row, and a literal→IRI row surface while an unchanged value
   does not. rdf-differ already has this test (`tests/unit/test_diff_semantics_queries.py`) —
   port the fixture if useful.

## Downstream coordination (DEC-4)

After regeneration, refresh rdf-differ's `resources/templates/**` from dqgen output so the
hand-patch in rdf-differ 2.3.0 and this generator fix converge. Until then the two repos carry
the same semantics by two routes — note this in the rdf-differ issues (#142/#143) and PR.
