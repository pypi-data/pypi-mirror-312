# Create output class
from pydantic import BaseModel
from typing import List,Dict

class AssistantData(BaseModel):
    agent_name:str
    messages :list=[]

class ToolOutput(BaseModel):
    agent_name:str
    response:str=""
    messages:list=[]
    assistant_agents:List[AssistantData]=[]
    tool_name:str
    tool_args : Dict

class Agentoutput(BaseModel):
    agent_name:str
    response:str
    messages:list=[]
    assistant_agents:List[AssistantData]=[]

