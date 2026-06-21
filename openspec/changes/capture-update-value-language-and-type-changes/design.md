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

Relax the disjunction to also pair (a) same lexical text with a changed/removed tag (#142)
and (b) exactly-one-side-is-a-literal (#143), keeping the `?oldValue != ?newValue` guard.
Emit it as a SINGLE comment-free line (see the Jena/Fuseki caveat below):

```sparql
FILTER ( ( (isLiteral(?oldValue) && isLiteral(?newValue) && lang(?oldValue) != "" && lang(?newValue) != "" && lang(?oldValue) = lang(?newValue)) || ((!isLiteral(?oldValue) || lang(?oldValue) = "") && (!isLiteral(?newValue) || lang(?newValue) = "")) || (str(?oldValue) = str(?newValue)) || (isLiteral(?oldValue) != isLiteral(?newValue)) ) && ?oldValue != ?newValue )
```

The four disjuncts are: (1) same non-empty language tag, changed text; (2) both plain
literals **or both URIs**; (3) #142 same text, changed/removed tag; (4) #143 literal↔object.
Apply identically to all four templates. The two `count_*` templates `SELECT (COUNT(...))`
over the same WHERE/FILTER, so an identical relaxation keeps counts consistent with the detail
queries (DEC-1).

### Jena/Fuseki caveat — why one comment-free line (not a multi-line commented block)

A SPARQL 1.2 endpoint (Apache Jena/Fuseki) mis-tokenizes a `NIL` (`()`) across a `#` comment
that contains a stray `)` — e.g. a comment like `# ... (datatype <-> object property)` sitting
**inside** the `FILTER(...)` expression. The `)` in the comment closes the bogus NIL and the
query fails to parse (`QueryBadFormed`). rdflib and oxigraph (both spec-conformant) parse it
fine, so it is an endpoint quirk — but the practical fix is ours: emit the FILTER on one line
with no inline comments, so no `)` ever lives inside a comment in expression position.

### Why not the compressed boolean

A tempting shorter form —
`FILTER( ?oldValue != ?newValue && ( lang(?oldValue) = lang(?newValue) || str(?oldValue) = str(?newValue) || (isLiteral(?oldValue) != isLiteral(?newValue)) ) )` —
**regresses URI→URI updates** (object properties such as `skos:broader` whose IRI value
changed). `lang()` on an IRI raises an error; with the other two disjuncts false the whole
FILTER errors and the row is dropped. The four explicit cases above keep the original Case 2
(URIs) behaviour. Verified empirically with oxigraph over labelled old/new value pairs.

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

> **Jena caveat (learned from rdf-differ 2.4.x):** keep the FILTER a single line with NO
> inline comments. A `(` followed by a comment that contains `)` makes Jena/Fuseki emit
> `Encountered <NIL>` (rdflib tolerates it). Use the comment-free form, e.g.
> `FILTER( ?oldValue != ?newValue && ( lang(?oldValue) = lang(?newValue) || str(?oldValue) = str(?newValue) || ( isLiteral(?oldValue) != isLiteral(?newValue) ) ) )`.
