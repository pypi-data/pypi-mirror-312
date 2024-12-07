import pandas as pd
from neo4j import GraphDatabase
from .datatypes import EAOntology, EROntology

class KGToNeo4j:
    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password

    # Write entity-relationship triples to Neo4j
    def ERNeo4j(self, tx, node1, label1, node2, label2, relationship_type):
        query = (
            f"MERGE (n1:{label1} {{name: $node1_name}}) "
            f"MERGE (n2:{label2} {{name: $node2_name}}) "
            f"MERGE (n1)-[:{relationship_type}]->(n2)"
        )
        tx.run(query, node1_name=node1, node2_name=node2)

    # Write entity attribute triples to Neo4j
    def EANeo4j(self, tx, node_name, label, attribute_name, attribute_value):
        query = (
            f"MERGE (n:{label} {{name: $node_name}}) "
            f"SET n.{attribute_name} = $attribute_value"
        )
        tx.run(query, node_name=node_name, attribute_value=attribute_value)
    
    # Write the corresponding triples to Neo4j according to the defined ontology model
    def graph_to_neo4j(self, ontology, graphfile):
        driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
        df = pd.read_excel(graphfile)
        if isinstance(ontology,EROntology):
            with driver.session() as session:
                for index, row in df.iterrows():
                    node1_name = row['key1']
                    node1_label = row['head']
                    node2_name = row['key2']
                    node2_label = row['tail']
                    relationship_type = row['relationship']
                    session.write_transaction(self.ERNeo4j, node1_name, node1_label, node2_name, node2_label, relationship_type)
        elif isinstance(ontology,EAOntology):
            with driver.session() as session:
                for index, row in df.iterrows():
                    node_name = row['key1'] 
                    node_label = row['head'] 
                    attribute_name = row['attribute']
                    attribute_value = row['key2']
                    session.write_transaction(self.EANeo4j, node_name, node_label, attribute_name, attribute_value)
        driver.close()


