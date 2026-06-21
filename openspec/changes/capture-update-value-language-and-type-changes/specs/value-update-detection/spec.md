# value-update-detection

Cites EPIC: capture-update-value-language-and-type-changes. Resolves rdf-differ #142, #143.

## ADDED Requirements

### Requirement: Generated update queries detect language-tag changes

The generated value-update queries SHALL report a property value as an update when its lexical
text is unchanged but its language tag changes or is removed between versions, for the same
instance and property.

#### Scenario: Language tag changed

- **GIVEN** a generated value-update query for property `p`
- **AND** an instance has `p "x"@en` in the old version and `p "x"@fr` in the new version
- **WHEN** the query runs against the skos-history delta graphs
- **THEN** the pair SHALL be reported as an `updated` value (old `"x"@en`, new `"x"@fr`)

#### Scenario: Language tag removed

- **GIVEN** a generated value-update query for property `p`
- **AND** an instance has `p "x"@en` in the old version and `p "x"` in the new version
- **WHEN** the query runs
- **THEN** the pair SHALL be reported as an `updated` value

### Requirement: Generated update queries detect datatype↔object changes

The generated value-update queries SHALL report a change between a literal value (datatype
property) and an IRI value (object property) on the same instance and property as an update.

#### Scenario: Literal becomes IRI

- **GIVEN** a generated value-update query for property `p`
- **AND** an instance has `p "x"` (literal) in the old version and `p <iri>` in the new version
- **WHEN** the query runs
- **THEN** the pair SHALL be reported as an `updated` value (old `"x"`, new `<iri>`)

### Requirement: Counts stay consistent with detail rows

The generated count queries for value updates SHALL apply the same pairing FILTER as their
detail counterparts, so the reported count equals the number of detail update rows.

#### Scenario: Count matches detail

- **GIVEN** a dataset producing N value-update detail rows for a property
- **WHEN** the corresponding generated count query runs
- **THEN** it SHALL return N

### Requirement: No false positives for unchanged values

The generated value-update queries SHALL NOT report an update for a value that is identical in
both versions.

#### Scenario: Unchanged value

- **GIVEN** an instance has `p "x"@en` in both the old and new versions
- **WHEN** the generated value-update query runs
- **THEN** no update SHALL be reported for that value
