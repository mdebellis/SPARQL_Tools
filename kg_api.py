from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
from franz.openrdf.query.query import QueryLanguage
import datetime

now = datetime.datetime.now()
conn = ag_connect('people', host='localhost', port=10035, user='mdebellis', password='df1559')

conn.setNamespace('ex', 'http://www.semanticweb.org/mdebe/ontologies/example#')

owl_named_individual = conn.createURI("http://www.w3.org/2002/07/owl#NamedIndividual")
owl_datatype_property = conn.createURI("http://www.w3.org/2002/07/owl#DatatypeProperty")
owl_annotation_property = conn.createURI("http://www.w3.org/2002/07/owl#AnnotationProperty")
owl_object_property = conn.createURI("http://www.w3.org/2002/07/owl#ObjectProperty")
owl_class = conn.createURI("http://www.w3.org/2002/07/owl#Class")
rdfs_label_property = conn.createURI("http://www.w3.org/2000/01/rdf-schema#label")
skos_pref_label_property = conn.createURI("http://www.w3.org/2004/02/skos/core#prefLabel")
ontology_string = "http://www.semanticweb.org/mdebe/ontologies/example#"

# Given the last part of an IRI will return the full IRI string
# E.g., given "Person" returns "http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/Person"
def make_iri_string(iri_name):
    return ontology_string + iri_name

# Finds a class with the the IRI class_name
# If no such class exists, returns None
# Note: when we refer to "IRI name" we mean last part of the IRI after the ontology prefix
# E.g., IRI name of "http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/Person" is "Person"
def find_class(class_name):
    iri_str = make_iri_string(class_name)
    class_object = conn.createURI(iri_str)
    for _ in conn.getStatements(class_object, RDF.TYPE, owl_class):
        return class_object
    print(f'Error {class_name} is not a class')
    return None

# Returns a list with all the instances of the class where the class is specified by name
# Note wherever it says X_name it means the IRI name of X If no class with that IRI name returns None
# If the class has no instances returns an empty list.
def find_instances_of_class(class_object):
    class_list = []
    statements = conn.getStatements(None, RDF.TYPE, class_object)
    with statements:
        for statement in statements:
            class_list.append(statement.getSubject())
    return class_list


# Finds a property (annotation, object, or datatype) from the IRI name
def find_property(prop_str):
    iri_str = make_iri_string(prop_str)
    prop = conn.createURI(iri_str)
    for _ in conn.getStatements(prop, RDF.TYPE, owl_datatype_property):
        return prop
    for _ in conn.getStatements(prop, RDF.TYPE, owl_annotation_property):
        return prop
    for _ in conn.getStatements(prop, RDF.TYPE, owl_object_property):
        return prop
    print(f'Error {prop} is not a property')
    return None

# Finds an instance from the IRI name
def find_instance_from_iri(iri_name):
    iri_string = make_iri_string(iri_name)
    instance_iri = conn.createURI(iri_string)
    statements = conn.getStatements(instance_iri, RDF.TYPE, owl_named_individual)
    with statements:
        for statement in statements:
            if len(statements) > 1:
                print(f'Warning two or more Individuals with ID: {instance_iri} using first one')
                return statement.subject()
            elif len(statements) == 1:
                return statement.getSubject()
    return None

# Finds an object based on its rdfs:label. Note this will also work for prefLabel and altLabel
# as long as the reasoner has run because they are sub-properties of rdfs:label
# If no object with that label, returns None
def find_object_from_label(label_string):
    statements = conn.getStatements(None, rdfs_label_property, label_string)
    kg_object = None
    with statements:
        for statement in statements:
            kg_object = statement.getSubject()
    return kg_object


# Gets the value of a single valued property using the IRI name of the instance and the IRI name of the property
# If the property has multiple values prints a warning and returns the first one
# If the property has no value returns None Note: if not sure whether property has multiple values, best to use get_values
def get_value(instance, owl_property):
    if instance is None:
        print("Error no object with iri name: {iri_name}")
        return None
    statements = conn.getStatements(instance, owl_property, None)
    with statements:
        for statement in statements:
            if len(statements) > 1:
                print(f'Warning: two or more values for property: {owl_property}. Using first one.')
                return statement.getObject()
            elif len(statements) == 1:
                return statement.getObject()
    print(f'Error: No property value for: {instance, owl_property}.')
    return None

# Returns the values of the property of an instance in a list if no values returns an empty list
def get_values(instance, owl_property):
    values = []
    statements = conn.getStatements(instance, owl_property, None)
    with statements:
        for statement in statements:
            next_value = statement.getObject()
            values.append(next_value)
    return values

# Creates a new instance of a class and returns the new instance
def make_instance (instance_name, instance_class):
    instance_iri = conn.createURI(make_iri_string(instance_name))
    conn.add(instance_iri, RDF.TYPE, owl_named_individual)
    conn.add(instance_iri, RDF.TYPE, instance_class)
    return instance_iri

# Get the label from an object. Looks in skos:prefLabel first (which currently is usually empty)
# Then uses first value it finds in rdfs:label. If no label string returns empty string
def object_to_string(kg_object):
    pref_statements = conn.getStatements(kg_object, skos_pref_label_property, None)
    with pref_statements:
        for statement in pref_statements:
            return statement.getObject()
    l_statements = conn.getStatements(kg_object, rdfs_label_property, None)
    with l_statements:
        for statement in l_statements:
            return statement.getObject()
    print("Error: object has no label string: {kg_object}")
    return ""

# When getting values that are datatypes there is all sorts of extra stuff we usually want to strip out
# E.g., in the dest data below the result of get_value("MichaelDeBellis", "email") will be: "mdebellissf@gmail.com"^^<http://www.w3.org/2001/XMLSchema#anyURI>
# this should strip out the datatype and extra string characters so will return mdebelissf@gmail.com
def convert_to_string (literal):
        literal = str(literal)
        literal = literal.replace(literal[literal.find("^") + len("^"):], '') #remove the datatype
        literal = literal[1:len(literal) - 2] # remove the string characters and the remaining ^
        return literal

# Adds a new value to an instance of a property.
# Note this takes as input the actual instance and property (i.e., their IRIs) so if needed use find_instance and find_property
# Did this for efficiency, there will be times then we already have a handle on the object and property
def put_value(instance, kg_property, new_value):
    conn.add(instance, kg_property, new_value)

# Deletes a value for an instance of a property.
# Note this takes as input the actual instance and property (i.e., their IRIs) so if needed use find_instance and find_property
# Did this for efficiency, there will be times then we already have a handle on the object and property
def delete_value(instance, kg_property, old_value):
    conn.removeTriples(instance, kg_property, old_value)


def create_rename_object_query(old_name, new_name):
    query_string = "DELETE {ex:" + old_name + " ?p ?o.} "
    query_string = query_string + "INSERT {ex:" + new_name  + " ?p ?o; skos:altLabel  \"" + old_name + "\"" + "; "
    query_string = query_string + "rdfs:label  \"" + new_name + "\" "
    query_string = query_string + "; rdfs:comment \"" + "Added alt label for old name: " + old_name + " on date: " + str(now) + "\""
    query_string = query_string + ".}  WHERE {ex:" + old_name + " ?p ?o.}"
    return query_string

#tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
#result = tuple_query.evaluate()


"""
#Test data, in each case the comment below is what should be returned (with the current ontology)
print(find_instance_from_iri("Jay_Gatsby"))
# <http://www.semanticweb.org/mdebe/ontologies/example#Jay_Gatsby>
print(get_values(find_instance_from_iri("Jay_Gatsby"), find_property("has_Friend")))
# [<http://www.semanticweb.org/mdebe/ontologies/example#Nick_Carraway>, <http://www.semanticweb.org/mdebe/ontologies/example#John_Smith>,... ]
print(get_value(find_instance_from_iri("Jay_Gatsby"), find_property("has_Age")))
# "42"^^<http://www.w3.org/2001/XMLSchema#integer>
print(convert_to_string(get_value(find_instance_from_iri("Jay_Gatsby"), find_property("has_Age"))))
# 42
print(find_class("Person"))
# <http://www.semanticweb.org/mdebe/ontologies/example#Person>
print(find_class("Foo"))
# Error Foo is not a class
# None
print(find_instances_of_class("Person"))
# [<http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/DanielDuffy>, <http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/RyanMcGranaghan>,...]
print(object_to_string(find_class("Adult")))
# "Organization"
put_value(find_instance_from_iri("Daisy_Buchanan"), find_property("has_Social_Relation_With"), make_instance("Allen_Turing", find_class("Person")))
conn.deleteDuplicates("spo")   # So we can run the test data without creating lots of Alaskas
print(get_values(find_instance_from_iri("Daisy_Buchanan"), find_property("has_Social_Relation_With")))
# List should include Allen_Turing
delete_value(find_instance_from_iri("Daisy_Buchanan"), find_property("has_Social_Relation_With"),find_instance_from_iri("Allen_Turing"))
print(get_values(find_instance_from_iri("Daisy_Buchanan"), find_property("has_Social_Relation_With")))
# List should not include Allen_Turing
print(find_object_from_label("Jay Gatsby"))
# <http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/AdamKellerman>
"""

print(create_rename_object_query("Jay_Gatsby", "JayGatsby"))