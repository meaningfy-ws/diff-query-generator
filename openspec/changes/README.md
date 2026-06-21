# In-flight changes

Each in-flight unit of work is a directory `openspec/changes/<id>/` carrying the spine artifacts:

| File / dir | Meaningfy noun |
|---|---|
| `proposal.md` | **EPIC** (the Shape-Up work shape) |
| `design.md` + `tasks.md` | **PLAN** (clarity gate scores the pair ≥9/10) |
| `specs/<cap>/spec.md` | normative requirements (SHALL + GWT deltas) |
| `inputs/` | **seed inputs** (briefs, notes) — preserved, never groomed |

**Golden thread (cite your parent):** `tasks.md` cites its EPIC id on the first line; specs
cite their capability; commits reference the change id. On archive, the spec deltas merge into
`openspec/specs/` (the durable truth) and the change moves under `archive/`.
