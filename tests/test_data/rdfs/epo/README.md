# Minimal ePO test data for OWL-core profile

Given the following versions of a dataset:

- **old:** `ePO_sample-4.0.0.orig.ttl`
- **new:** `ePO_sample-4.0.0.upd.ttl`

The following are changes comparing **old** to **new**, where _redundant_
refers to redundant appearances in the existing diff'ing/reporting, and _not
captured_ to the non-appearance thereof, due to one reason or another, that may
or may not be a bug:

1. added class **epo:AwardCriterion**
2. deleted class **epo:AdHocChannel**
3. class **epo:AcquiringCentralPurchasingBody** replaced `skos:prefLabel` w/ `rdfs:label` (interpreted as `rdfs:label` added)
4. class **epo:AwardCriterion** added `skos:prefLabel` (redundant, from added class)
5. class **epo:Document** added `skos:prefLabel` _es_ lang
6. class **epo:AccessTerm** deleted `skos:prefLabel`
7. class **epo:AcquiringCentralPurchasingBody** replaced `skos:prefLabel` w/ `rdfs:label` (interpreted as `skos:prefLabel` deleted)
8. class **epo:AdHocChannel** deleted `skos:prefLabel` (redundant, from deleted class)
9. class **epo:AwardCriteriaSummary** updated `skos:prefLabel` (moved original value to `skos:altLabel`)
10. class **epo:AcquiringCentralPurchasingBody** replaced `skos:prefLabel` w/ `rdfs:label` (interpreted as `skos:prefLabel` changed to `rdfs:label`)
11. class **epo:AwardCriteriaSummary** changed `skos:prefLabel` to `skos:altLabel` (cross-property move of `skos:prefLabel` to `skos:altLabel`)
12. class **epo:AwardCriteriaSummary** add `skos:altLabel` (redundant, from cross-property move of `skos:prefLabel`)
13. class **epo:AwardCriterion** added `skos:definition` (redundant, from added class)
14. class **epo:AdHocChannel** deleted `skos:definition` (redundant, from deleted class)
15. class **epo:AwardCriterion** added `rdfs:subClassOf` (redundant, from added class)
16. class **epo:AdHocChannel** deleted `rdfs:subClassOf` (redundant, from deleted class)
17. class **epo:AwardCriterion** added `rdfs:isDefinedBy` (redundant, from added class)
18. class **epo:AdHocChannel** deleted `rdfs:isDefinedBy` (redundant, from deleted class)
19. class **epo:AdHocChanel** moved `rdfs:isDefinedBy` to **epo:AwardCriterion** (redundant, part of added class)
20. added objectProperty **epo:followsRulesSetBy**
21. deleted objectProperty **epo:exposesChannel**
22. objectProperty **epo:exposesInvoiceeChannel** added `rdfs:label`
23. objectProperty **epo:followsRulesSetBy** added `skos:prefLabel` (redundant, from added objectProperty)
24. objectProperty **epo:exposesChannel** deleted `skos:prefLabel` (redundant, from deleted objectProperty)
25. objectProperty **epo:describesResultNotice** added `skos:altLabel`
26. objectProperty **epo:followsRulesSetBy** added `rdfs:isDefinedBy` (redundant, from added objectProperty)
27. objectProperty **epo:exposesChannel** deleted `rdfs:isDefinedBy` (redundant, from deleted objectProperty)
28. objectProperty **epo:exposesChannel** moved `rdfs:isDefinedBy` to **epo:followsRuleSetBy** (redundant, part of added class)
29. added datatypeProperty **epo:describesObjectiveParticipationRules**
30. deleted datatypeProperty **epo:describesProfessionRelevantLaw**
31. datatypeProperty **epo:describesProfession** added `rdfs:label` no lang
32. datatypeProperty **epo:describesObjectiveParticipationRules** added `skos:prefLabel` (redundant, from added datatypeProperty)
33. datatypeProperty **epo:describesProfessionRelevantLaw** deleted `skos:prefLabel` (redundant, from deleted datatypeProperty)
34. datatypeProperty **epo:describesObjectiveParticipationRules** added `rdfs:isDefinedBy` (redundant, from added datatypeProperty)
35. datatypeProperty **epo:describesProfessionRelevantLaw** deleted `rdfs:isDefinedBy` (redundant, from deleted datatypeProperty)
36. datatypeProperty **epo:describesProfessionRelevantLaw** moved `rdfs:isDefinedBy` to **epo:describesObjectiveParticipationRules** (redundant, part of added class)
37. datatypeProperty **epo:describesVerificationMethod** converted to objectProperty (not captured)
38. objectProperty **epo:distributesOffer** deleted lang of `skos:prefLabel` (not captured)
39. objectProperty **epo:actsOnBehalfOf** replace lang en w/ de of `skos:prefLabel` (not captured)

There is no automated test case at present using these files, but they can be
used to facilitate manual tests in the meantime.
