# diff-query-generator

A service for generating SPARQL queries necessary for the RDF Diffing, which calculates the difference between versions of a given RDF dataset. 

Please refer to  the current implementation of  the [rdf-differ](https://github.com/eu-vocabularies/rdf-differ) and 
the [skos-history tool](https://github.com/eu-vocabularies/skos-history).
See the [Wiki page of the original repository](https://github.com/jneubert/skos-history/wiki/Tutorial) for more technical details.


# Installation

To be added ... 

# Usage

First have your Application Profile defined (in a CSV file) covering all the classes and the properties for which you want to see changes in a dataset.
Then run the script providing this AP definition and an output folder where the per-change-type SPARQL queries will be generated.  

To be continued ...

# Change type inventory

This section provides a change type inventory along with the patterns captured by each change type. We model the change as state transition operator between old (on the left) and teh new (on the right). The transition operator is denoted by the arrow symbol (-->). On each sides of the transition operator, we use a compact notation following SPARQL triple patterns. 

We use a set of conventions for each variable in the triple pattern, ascribing meaning to each of them and a few additional notations. These conventions are presented in teh table below.

| Notation                   | Meaning                                                                                                                                                    | Example                 |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------|
| triple pattern < _s p o_ >   | each item in the triple represents a SPARQL variable or an URI. For brevity we omit the question mark prefix (?) otherwise the SPARQL reading shall apply. | i p v                   |
| arrow (_ --> _)              | state transition operator (from one version to the next)                                                                                                   | i1 p o  -->  i2 p o     |
| _i_ - in the triple pattern  | the instance subject (assuming class instantiation)                                                                                                        | i p v                   |
| _p_ - in the triple pattern  | the main predicate                                                                                                                                         | i p v                   |
| _op_ - in the triple pattern | the secondary predicate in a property chain (/)                                                                                                            | i p/op v                |
| _v_ - in the triple pattern  | the value of interest, which is object of the main or secondary predicate                                                                                  | i p v                   |
| _@l_ - in the triple pattern | the language tag of the value, if any                                                                                                                      | v@l                     |
| slash (_/_)                  | the property chaining operation.                                                                                                                           | p1/p2/p3/p4             |
| number (_#_)                 | the numeric suffixes help distinguish variables of teh same type                                                                                           | i1 p1 o1  -->  i2 p2 o2 |
| zero (_0_)                   | denotes "empty set" or "not applicable"                                                                                                                    | 0                       |


The table below presents the patterns of change likely to occur in the context of maintaining SKOS vocabularies, but the abstraction proposed here may be useful way beyond this use case. The table represents a power product between the four types of change relevant to the current diffing context and the possible triple patterns in which they can occur. Cells that are marked with zero (0) mean that no check shall be performed for such a change type as it is included in onw of its siblings. The last two columns indicate whether quantification assumptions apply on either side of the transition operator.  

| change type / pattern    | instance  | property value free  | property value language dependent | reified property value    | property value langauge dependent | reification object | Left condition checking | Right condition checking |
|---------------------------|-----------|----------------------|-----------------------------------|---------------------------|-----------------------------------|--------------------|-------------------------|--------------------------|
| Addition                  | 0  -->  i | 0  -->  i p v        | 0 --> i p v@l                                | 0  -->  i p/op v          | 0                                 | 0                  |                       0 | x                        |
| Deletion                  | i  -->  0 | i p v  -->  0        | i p v@l  -->  0                   | i p/op v  -->  0          |                                   | 0                  | x                       |                        0 |
| Value update              | 0         | i p v1  -->  i p v2  | i p v1@l  -->  i p v2@l           | i p/op v1  -->  i p/op v2 | i p/op v1@l  -->  i p/op v2@l     | 0                  | x                       | x                        |
| Movement (cross instance) | 0         | i1 p v  -->  i2 p v  | 0                                 | i1 p/op v  -->  i2 p/op v | 0                                 | 0                  | x                       | x                        |
| Movement (cross property) | 0         | i p1 v  -->  i p2 v  | 0                                 | i p1/op v  -->  i p2/op v | 0                                 | 0                  | x                       | x                        |

The state transition patterns presented in the table above can be translated to SPARQL queries. The last two columns, referring to the quantification assumptions, are useful precisely for this purpose indicating what filters shall be used in the SPARQL query.  


Before we introduce the quantification assumptions, we need to mention that the current diffing is performed by subtracting teh new version of the dataset from the old one resulting in the set of deletions between the two and, conversely, subtracting the old version of the dataset from the new one resulting in a set of insertions between the two. Therefore we conceptualise four content graphs: _OldVersion_, _NewVersion_, _Insertions_ and _Deletions_. Below is the table that summarises the quantification assumptions as conditions that apply to either left or right side of the transition operator and involve one of the four graphs introduced here.  


| Conditions on the left side of the transition operator                                                                                                                              | Conditions on the right side of the transition operator                                                                                                                            |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| does NOT exist in the Insertion graph 				| exists in the Insertion graph 	|
| does NOT exist in the NewVersion graph [redundant]	| exists in the NewVersion graph [redundant]		|
| exists in the Deletions graph						| does NOT exist in the Deletions graph [redundant]		|
| exists in the OldVersion graph [redundant] 			| does NOT exist in the OldVersion graph 	|

## Test Dataset elaboration
### ds.A.1 - ds.A.2 (skos model & skos lexicalisation)
#### Model coverage:
	- skos:Cocnept (5), skos:ConceptScheme (1)
	- skos:prefLabel (1-5 per each concept), skos:altLabel (0-5 epr concept), skos:notation (0-5 per concept)

#### Operations coverage
	- addition instance (2)
	- deletion instance (2)
	- addition property value (2 - skos:altLabel  )
	- deletion property value (2 - skos:prefLabel )
	- value update property (1 - skos:notation)
	- value update property (1 - skos:altLabel)
	- movement (cross instance) - (1 skos:notation and 1 skos:altLabel move to anotehr concept)
	- movement (cross property) - (1 skos:notation becomes owl:versionInfo on the same concept; and 1 skos:prefLabel becomes an skos:altLabel)

*note*: make sure that each operations is performed on an independent set of triples. That is, for example, a value update shall not be conflated with a movement, or a value addition shall not be conflated with an update. 


### ds.B.1 - ds.B.2 (skos model & skosxl lexicalisation)
#### Model coverage:
	- skos:Cocnept (5), skos:ConceptScheme (1)
	- skosxl:prefLabel (1-5 per each concept), skosxl:altLabel (1-5 per each concept)

#### Operations coverage
	- addition reified property value (2 - skosxl:prefLabel)
	- deletion reified property value (2 - skosxl:altLabel)
	- value update reified property (2 - skosxl:prefLabel )
	- value update reified property (2 - skosxl:altLabel )
	- movement (cross instance) - (1 skosxl:altLabel moves to anotehr concept)
	- movement (cross property) - (1 skosxl:prefLabel becomes a skosxl:altLabel)


*note*: make sure that each operations is performed on an independent set of triples. That is, for example, a value update shall not be conflated with a movement, or a value addition shall not be conflated with an update. 


# Naming conventions
## Operations
Looking at patterns of change likely to occur in the context of maintaining SKOS vocabularies or to find in a diffing context
we've identified 5 change types and mapped them for easy referencing as follows:
* Addition --> Added  
* Deletion --> Deleted
* Value update --> Updated
* Movement (cross property) --> Changed
* Movement (cross instance) --> Moved
## Query file name
In order to name a query file that will represent what is the query for ,but in the same time to be easy to read,
the file name will be constructed from five parts. These are operation, rdf type, class name, property name and object property name.
All names are only the local segment of the Qname (compressed URI) provided and the rdf types are instance, property and reified (reified property).

File name examples: 

Structure --> operation_rdfType_className    
File name: added_instance_collection

Structure --> operation_rdfType_className_propertyName   
File name: changed_property_concept_broader

## Query identifiers
A SPARQL query file could sometimes be long and hard to read. To improve readability and minimize use of hidden variables, the query parameters should express in some manner
what is the query used for and also to have the same values in the entire query. For easy referencing a change from the SPARQL query parameters , a good option 
is to add a prefix to the parameters that will have the value changed in the diffing context.
To avoid pollutions of parameter names the convention will add prefix in front of the parameter that is changing in the diffing context by using the query. 
This can only be old or new (i.e ?oldInstance ?newInstance).
*note*: a value change can also be non-existing and existing



# Contributing
You are more than welcome to help expand and mature this project. We adhere to [Apache code of conduct](https://www.apache.org/foundation/policies/conduct), please follow it in all your interactions on the project.   

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the maintainers of this repository before making a change.

## Licence 
This project is licensed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) licence. 

Powered by [Meaningfy](https://github.com/meaningfy-ws).
