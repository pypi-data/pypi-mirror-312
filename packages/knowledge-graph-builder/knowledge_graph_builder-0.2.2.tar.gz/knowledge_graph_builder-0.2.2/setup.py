from setuptools import setup, find_packages

setup(
    name="knowledge_graph_builder",
    version="0.2.2",
    description="Constructing Knowledge Graph Based on Given Entity Relation Ontology and Entity Attribute Ontology",
    author="Cuibinge",
    author_email="cuibinge@sdust.edu.cn",
    packages=['knowledge_graph_builder', 'knowledge_graph_builder/llm_clients'],
    python_requires=">=3.11,<4.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=[
        "groq>=0.6.0,<0.7.0",
        "jupyterlab>=4.0.8,<5.0.0",
        "neo4j==5.19.0",
        "neomodel>=5.3.0,<6.0.0",
        "numpy>=1.26.2,<2.0.0",
        "openai>=1.28.0,<2.0.0",
        "pathlib>=1.0.1,<2.0.0",
        "python-dotenv>=1.0.1,<2.0.0",
        "uuid>=1.30,<2.0",
        "yachalk>=0.1.5,<0.2.0",
    ],
    
)