Build a Knowledge Graph based on the defined entity relationship ontology and entity attribute ontology, and write it to the Neo4j database.
## 1.KGBuilder.py
According to the defined ontology, the triplet of entity relation and entity attribute is extracted from the document input by the user using LLM.
## 2.KGLogger.py
Define Logger.
## 3.datatypes.py
Define data type.
## 4.KGToNeo4j.py
Write the extracted entity relations and entity attribute triples to the Neo4j database.