# SPARQL_Tools
Useful SPARQL utility queries. 
This is a repository for various files with useful SPARQL queries. I usually use my new Pizza tutorial as the example.  More on that can be found here: https://www.michaeldebellis.com/post/new-protege-pizza-tutorial  Although, I will add all the files to this repository as well. 
As of now, the two SPARQL files are different versions of SPARQL queries that create rdfs:label values based on the IRI of an entity.
This is useful because Protege doesn't provide a value for the rdfs:label when you use a user supplied name rather than a UUID. 
The queries create apprpriate labels based on the assumption that classes and individuals are named in CamelBack and properties in
reverseCamelBack. So "MyCoolClass" would have the label: "My Cool Class" and "myObjectProperty" would have the label "my Object Propety". 
The files have the IRI for the Pizza tutorial ontology although that IRI isn't even needed for these specific transformations. 
