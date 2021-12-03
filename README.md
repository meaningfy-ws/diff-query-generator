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

#SPARQL queries
## Naming conventions
### Operations
Looking at patterns of change likely to occur in the context of maintaining SKOS vocabularies or to find in a diffing context
we've identified 5 change types and mapped them for easy referencing as follows:
* Addition --> Added  
* Deletion --> Deleted
* Value update --> Updated
* Movement (cross property) --> Changed
* Movement (cross instance) --> Moved
### Query file name
In order to name a query file that will represent what is the query for ,but in the same time to be easy to read,
the file name will be constructed from five parts. These are operation, rdf type, class name, property name and object property name.
All names are only the local segment of the Qname (compressed URI) provided and the rdf types are instance, property and reified (reified property).

File name examples: 

Structure --> operation_rdfType_className    
File name: added_instance_collection

Structure --> operation_rdfType_className_propertyName   
File name: changed_property_concept_broader

##Structure
In this project the SPARQL query is constructed from four parts that will be explained below. 
##Prefixes section
Prefixes are declared in this section before the select statement of the query. It can have as many possible prefixes 
and values as the query will use only the ones that it needs.
### Query variables
A SPARQL query file could sometimes be long and hard to read. To improve readability and minimize use of hidden variables, the query parameters should express in some manner
what is the query used for and also to have the same values in the entire query. For easy referencing a change from the SPARQL query parameters , a good option 
is to add a prefix to the parameters that will have the value changed in the diffing context.
To avoid pollutions of variables names the convention will add prefix in front of the variables that is changing in the diffing context by using the query. 
This can only be old or new (i.e ?oldInstance ?newInstance).
###Version history graph block
This block will remain unchanged for all diffing queries as it's defining the graphs that are used later in the query.
As a mention there is only one part that can change here and that is the value injection for the query which will be 
present in the next section. The logic of the query is based on this four graphs that are built here. We can see below 
that we are going to have access to newVersionGraph, oldVersionGraph, insertionsGraph and deletionsGraph, so we can filter
our data.

      GRAPH ?versionHistoryGraph {

        # parameters
        VALUES ( ?versionHistoryGraph ?oldVersion ?newVersion ?class) {
            ( undef 
              undef 
              undef  
              skos:Concept 
            )
        }
        # get the current and the previous version as default versions
        ?versionset dsv:currentVersionRecord/xhv:prev/dc:identifier ?previousVersion .
        ?versionset dsv:currentVersionRecord/dc:identifier ?latestVersion .
        # select the versions to actually use
        BIND(coalesce(?oldVersion, ?previousVersion) AS ?oldVersionSelected)
        BIND(coalesce(?newVersion, ?latestVersion) AS ?newVersionSelected)
        # get the delta and via that the relevant graphs
        ?delta a sh:SchemeDelta ;
          sh:deltaFrom/dc:identifier ?oldVersionSelected ;
          sh:deltaTo/dc:identifier ?newVersionSelected ;
          sh:deltaFrom/sh:usingNamedGraph/sd:name ?oldVersionGraph ;
          sh:deltaTo/sh:usingNamedGraph/sd:name ?newVersionGraph .
        ?insertions a sh:SchemeDeltaInsertions ;
          dct:isPartOf ?delta ;
          sh:usingNamedGraph/sd:name ?insertionsGraph .
        ?deletions a sh:SchemeDeltaDeletions ;
          dct:isPartOf ?delta ;
          sh:usingNamedGraph/sd:name ?deletionsGraph .
      }

###Value injection
As mentioned in the previous section there is a value injection block where we can assign values to variables that 
are going to be used in the query logic.

       # parameters
        VALUES ( ?versionHistoryGraph ?oldVersion ?newVersion ?class) {
            ( undef 
              undef 
              undef  
              skos:Concept 
            )
        }

###Query logic
This part of the query is filtering the data by looking for triples in the graphs made available in the version history 
graph block. The graphs are made available through the delta generated ([see Versions and Deltas as Named Graphs](https://github.com/jneubert/skos-history/wiki/Versions-and-Deltas-as-Named-Graphs)) by the diffing process, and they are as follows:
- oldVersionGraph - contains triples existing in the old version file
- newVersionGraph - contains triples existing in the new version file
- insertionsGraph - contains added triples to the old version file
- deletionsGraph - contains triples deleted from the old version file

As an example, will want to look for new instances that are of a certain class and to achieve this will 
want to look into the insertions graph.

      GRAPH ?insertionsGraph {
        ?instance a ?class .
        
        optional {
          ?instance skos:prefLabel ?prefLabelEn .
          FILTER (lang(?prefLabelEn) = "en")
        }

The query logic can continue to filter the results by verifying existence of triples in other available graphs. This can 
be done by using another graph block as showed below.

      # ... and the instance must not exist in the old version
      FILTER NOT EXISTS {
        GRAPH ?oldVersionGraph {
          ?instance ?p [] .
        }
      }

##Example of diffing query
Building a query to get all added skos:altLabel property per instance of a certain class.
1. Prefixes section


    # basic namespaces
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    .
    .
    .
    # versioning namespaces
    PREFIX dsv: <http://purl.org/iso25964/DataSet/Versioning#>
    PREFIX sd: <http://www.w3.org/ns/sparql-service-description#>
    PREFIX sh: <http://purl.org/skos-history/>
    PREFIX xhv: <http://www.w3.org/1999/xhtml/vocab#>


2. Query variables

For the results and the query itself to be easy to read we need to choose good variable names and make sure the variables
will bring the expected result format. In this case we want to see instance URI, instance label, property and 
value of the property.


      SELECT DISTINCT ?instance ?prefLabel ?property ?value 
      WHERE {

4. Version history graph block and value injection

    
     GRAPH ?versionHistoryGraph {
        # defining values for our variables that are we going to use in the query (instance class and property)
        VALUES ( ?versionHistoryGraph ?oldVersion ?newVersion ?class ?property) {
          ( undef
            undef
            undef
            skos:Concept 
            skos:altLabel 
          )
        }
        # get the current and the previous version as default versions
        ?versionset dsv:currentVersionRecord/xhv:prev/dc:identifier ?previousVersion .
        ?versionset dsv:currentVersionRecord/dc:identifier ?latestVersion .
        # select the versions to actually use
        BIND(coalesce(?oldVersion, ?previousVersion) AS ?oldVersionSelected)
        BIND(coalesce(?newVersion, ?latestVersion) AS ?newVersionSelected)
        # get the delta and via that the relevant graphs
        ?delta a sh:SchemeDelta ;
          sh:deltaFrom/dc:identifier ?oldVersionSelected ;
          sh:deltaTo/dc:identifier ?newVersionSelected ;
          sh:deltaFrom/sh:usingNamedGraph/sd:name ?oldVersionGraph ;
          sh:deltaTo/sh:usingNamedGraph/sd:name ?newVersionGraph ;
          dct:hasPart ?insertions ;
          dct:hasPart ?deletions .
        ?deletions a sh:SchemeDeltaDeletions ;
          sh:usingNamedGraph/sd:name ?deletionsGraph .
        ?insertions a sh:SchemeDeltaInsertions ;
          sh:usingNamedGraph/sd:name ?insertionsGraph .
      }


5. Query logic
In this part we need to filter the results to get only the instances that had the skos:altLabel property added. As
a starting point we will look in the insertions graph to get all inserted skos:altLabel properties for all instances. 
For this to be a true addition and not a change or a movement operation we need to make sure that the property was
not attached to some other instance before and to do this will look into the deletions graph and old version graph. 
After filtering the result we can get all the values that are needed from the new version graph.



      # get inserted properties for instances
      GRAPH ?insertionsGraph {
        ?instance ?property [] .
      }
      # ... which were not attached to some (other) instance before
      FILTER NOT EXISTS {
        GRAPH ?deletionsGraph {
          ?instance ?property [] .
        }
      }
        FILTER NOT EXISTS {
        GRAPH ?oldVersionGraph {
          [] ?property ?value .
        }
      }
        # get instances with those property values
      GRAPH ?newVersionGraph {

        ?instance a ?class .
        ?instance ?property ?value .
        
        optional {
          ?instance skos:prefLabel ?prefLabel .
          FILTER (lang(?prefLabelEn) = "en")
        }
      }
    }


# Contributing
You are more than welcome to help expand and mature this project. We adhere to [Apache code of conduct](https://www.apache.org/foundation/policies/conduct), please follow it in all your interactions on the project.   

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the maintainers of this repository before making a change.

## Licence 
This project is licensed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) licence. 

Powered by [Meaningfy](https://github.com/meaningfy-ws).
