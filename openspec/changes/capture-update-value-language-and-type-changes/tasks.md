# PLAN — tasks (EPIC: capture-update-value-language-and-type-changes)

Golden thread: resolves rdf-differ #142 and #143 at their source (the generator templates).

## T1 — relax the value-update pairing FILTER
- [ ] T1.1 `dqgen/resources/query_templates/property_value_updates.rq` — add Case 3 (#142) + Case 4 (#143).
- [ ] T1.2 `dqgen/resources/query_templates/reified_property_value_updates.rq` — same two cases.
- [ ] T1.3 `dqgen/resources/query_templates/count_property_value_updates.rq` — same (keep counts == detail).
- [ ] T1.4 `dqgen/resources/query_templates/count_reified_property_value_updates.rq` — same.

## T2 — tests
- [ ] T2.1 Generator test: rendered value-update query contains all four FILTER cases.
- [ ] T2.2 Regenerate/update committed `tests/test_data/**/test_queries/value_update_*.rq` fixtures; list the diff.
- [ ] T2.3 (Recommended) rdflib semantic test: tag-change, tag-removal, literal→IRI surface; unchanged does not.
- [ ] T2.4 `make test` green.

## T3 — docs
- [ ] T3.1 Add the two change types to the README "Change type inventory":
      `i p "x"@l1 --> i p "x"@l2`, `i p "x"@l1 --> i p "x"`, `i p "x" --> i p <o>`.

## T4 — release & downstream coordination
- [ ] T4.1 Regenerate all profile templates (`make generate_all_profiles_templates`); commit the regenerated `.rq`.
- [ ] T4.2 Tag/release dqgen.
- [ ] T4.3 Refresh rdf-differ `resources/templates/**` from dqgen output (DEC-4); converge with the 2.3.0 hand-patch.
