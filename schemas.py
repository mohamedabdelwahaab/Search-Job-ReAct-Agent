from typing import List
from pydantic import BaseModel, Field

class Source(BaseModel):
    '''Schema for a source document used by the agent.'''
    url: str = Field( description="The URL of the source document.")

class AgentResponse(BaseModel):
    '''Schema for the agent's response including sources.'''
    answer: str = Field( description='the final answer provided by the agent.')
    sources: List[Source] = Field( description= 'the list of source documents used by the agent to generate the answer.',
                                default_factory=list)
