# EPIC — Capture language-tag and datatype↔object value changes in update queries

> Shape-Up work shape. EPIC ≡ this proposal. Drives the PLAN (`design.md` + `tasks.md`)
> and the capability spec under `specs/`.

## Appetite

Small batch. Four template files plus tests and regenerated fixtures. The semantic change is
two extra disjuncts in one FILTER, replicated across the four value-update templates.

## Why (the bet)

rdf-differ issues **#142** and **#143** trace to the SPARQL that dqgen generates. The
value-update templates pair an old value (deletions graph) with a new value (insertions
graph) for the same instance+property **only when their language tags match** (or both are
non-language-tagged). That pairing FILTER silently drops two real, common change types:

- **#142 — language-tag change/removal.** `prop "x"@en` → `prop "x"@fr`, or `prop "x"@en` →
  `prop "x"` (same lexical text, different/absent tag). Neither Case 1 (tags must match) nor
  Case 2 (both non-tagged) holds, so nothing is reported.
- **#143 — datatype↔object change.** `prop "x"` (literal) → `prop <iri>` (IRI) for the same
  instance+property. The value-update FILTER rejects the literal↔IRI pair, and the
  added/deleted queries suppress it via `FILTER NOT EXISTS`, so the change vanishes entirely.

These were patched downstream directly in rdf-differ's **rendered** `.rq` files (rdf-differ
2.3.0). dqgen is the **source of truth** for those files: until the generator templates carry
the same relaxation, the next `make generate_all_profiles_templates` will silently revert the
fix. This EPIC moves the fix to its proper home and adds the two change types to the
generator's change-type inventory.

## Solution outline

Relax the value-update pairing FILTER in the four templates under
`dqgen/resources/query_templates/`:

- `property_value_updates.rq`
- `reified_property_value_updates.rq`
- `count_property_value_updates.rq`   *(counts MUST match the detail rows)*
- `count_reified_property_value_updates.rq`

Add two disjuncts to the existing Case 1 / Case 2 group so old/new are also paired when:

- **Case 3 (#142):** they share lexical text but differ in tag — `str(?oldValue) = str(?newValue)`
- **Case 4 (#143):** exactly one side is a literal — `isLiteral(?oldValue) != isLiteral(?newValue)`

keeping the existing `&& ?oldValue != ?newValue` guard. The pairing stays bounded (same
instance+property, deletions↔insertions), so no cross-language cartesian noise beyond the two
deliberate cases.

Document both as named change types in the README "Change type inventory":
`i p "x"@l1 --> i p "x"@l2` (and `--> i p "x"`), and `i p "x" --> i p <o>`.

## Key decisions

- **DEC-1** Fix the four `*_value_updates.rq` templates, detail **and** count, together — a
  detail/count mismatch would be a worse bug than the original.
- **DEC-2** Surface the changes as `updated` rows (reuse the existing action), not a new
  "type-changed" change category. The rdf-differ issues ask only that the change *be
  captured*; a distinct category is a separate, larger bet (new templates + report + UI).
- **DEC-3** Verification is a generator test that renders a value-update query and asserts the
  rendered FILTER contains all four cases, plus updating the committed expected-query fixtures
  under `tests/test_data/.../test_queries/` so a regeneration diff stays clean.
- **DEC-4** Coordinate the release with rdf-differ: once regenerated, rdf-differ's vendored
  `resources/templates/**` should be refreshed from dqgen so the two stop diverging (the
  rdf-differ 2.3.0 hand-patch and this generator fix must converge).

## Rabbit-holes (avoid)

- A dedicated "datatype-to-object" / "object-to-datatype" change category with its own
  templates, count queries, HTML/AsciiDoc rendering and rdf-differ report wiring. Out — see
  DEC-2.
- Re-deriving the skos-history delta model or touching the added/deleted templates. The
  value-update FILTER is the whole fix.
- Detecting "moved" object values (object property whose object node changed) — that is the
  reified-property path's existing concern, not this change.

## No-gos (explicitly out of scope)

- Changing the rendered files in the rdf-differ repo (already done in rdf-differ 2.3.0; this
  EPIC is the upstream mirror).
- Bumping minimum language-fallback behaviour or AP CSV schema.
