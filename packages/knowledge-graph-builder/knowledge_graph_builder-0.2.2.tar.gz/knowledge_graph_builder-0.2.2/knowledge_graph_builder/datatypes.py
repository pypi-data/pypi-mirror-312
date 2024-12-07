from pydantic import BaseModel
from typing import List, Dict, Union
from abc import ABC, abstractmethod

# LLMClient
class LLMClient(ABC):
    @abstractmethod
    def __init__(self, model: str, temperature: float, top_p: float):
        """
        Initialize the LLMClient with the specified model and parameters.
        
        Args:
        model (str): The name or identifier of the LLM model to use.
        temperature (float): The temperature parameter for the LLM, controlling randomness.
        top_p (float): The top-p parameter for the LLM, controlling the diversity of responses.
        """
        self.model = model
        self.temperature = temperature
        self.top_p = top_p

    @abstractmethod
    def generate_response(self, user_message: str, system_message: str) -> str:
        """
        Generate and return the first choice from chat completion as a string.
        
        This method should be implemented by any concrete LLMClient subclass to
        interact with the specific LLM service or model.
        
        Args:
        user_message (str): The message from the user.
        system_message (str): The message from the system or previous context.
        
        Returns:
        str: The generated response from the LLM.
        """
        pass


# Define entity attribute ontology 
class EAOntology(BaseModel):
    entities: List[Union[str, Dict]]
    attributes: List[Union[str, Dict]]

    def dump(self):
        return self.model_dump()

# Define entity relationship ontology
class EROntology(BaseModel):
    entities: List[Union[str, Dict]]
    relationships: List[str]

    def dump(self):
        return self.model_dump()


# Entity Attribute Node 1
class EANode1(BaseModel):
    entity: str
    name: str
    

# Entity Attribute Node 2
class EANode2(BaseModel):
    attribute: str
    name: str
     
# Entity Attribute Edge
class EAEdge(BaseModel):
    node_1: EANode1
    node_2: EANode2
    relationship: str
    metadata: dict = {}
    sequence: Union[int, None] = None

# Entity Relationship Node
class ERNode(BaseModel):
    entity: str
    name: str


# Entity Relationship Edge
class EREdge(BaseModel):
    node_1: ERNode
    node_2: ERNode
    relationship: str
    metadata: dict = {}
    sequence: Union[int, None] = None

class Document(BaseModel):
    text: str
    metadata: dict