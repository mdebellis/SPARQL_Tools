# SPARQL_Tools
Useful SPARQL utility queries. 
This is a repository for various files with useful SPARQL queries. I usually use my new Pizza tutorial as the example.  More on that can be found here: https://www.michaeldebellis.com/post/new-protege-pizza-tutorial  Although, I will add all the files to this repository as well. 
As of now, the two SPARQL files are different versions of SPARQL queries that create rdfs:label values based on the IRI of an entity.
This is useful because Protege doesn't provide a value for the rdfs:label when you use a user supplied name rather than a UUID. 
The queries create apprpriate labels based on the assumption that classes and individuals are named in CamelBack and properties in
reverseCamelBack. So "MyCoolClass" would have the label: "My Cool Class" and "myObjectProperty" would have the label "my Object Propety". 
The files have the IRI for the Pizza tutorial ontology although that IRI isn't even needed for these specific transformations. 
I have two versions of the files because the Snap SPARQL plugin for Protege has some eccentricities. It can only do CONSTRUCT rather than
INSERT (you get the equivalent of INSERT because it asks if you want to save the constructed triples to the ontology). Also, there is a bug
in the Snap SPARQL implementation of SUBSTR. It uses 0 based indexing but the spec says it should use 1 based indexing, hence the two versions of the files. 

On 12/23/21 I added the file: UUIDTransformations. This file can take an ontology with user supplied names and automatically refactor them to have UUIDs. I've tested this on the PizzaWData ontology and it works. Note: haven't tested it on an ontology with SWRL rules yet but I think it should work. Be sure to run the Label transformations before doing the UUID transformations or you won't know what any of the entities are after the transformations. Execute each transformation in order except for any labeled with the comment: "For debugginb purposes". On 12/24/21 I made some minor changes to the UUID transformations based on feedback from Lorenz on the Protege User Support email list. I followed all his suggestions except for changing the "IF BOUND(..." with "COALESE". The COALESE works but it results in many SPARQL error messages so thought it was better to leave it with the IF statement instead. 

On 1/13/25 I updated the queries that generate labels from IRIs in CamelCase and reverseCamelCase format. The original queries didn't handle acronyms correctly. E.g., "NASAEmployee" would end up as "N A S A Employee" the new queries are the result of help from ChatGPT to create two REGEX expressions and appropriately handle acronyms. I've also added a Wiki: https://github.com/mdebellis/SPARQL_Tools/wiki that has the dialogs with ChatGPT that I used to generate SPARQL queries. 
