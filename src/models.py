from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
class Verdict(str,Enum): ALLOW="ALLOW"; DENY="DENY"; ESCALATE="ESCALATE"; ASK="ASK_CLARIFICATION"
class Classification(BaseModel):
    intents:list[str]=Field(default_factory=list); entities:dict[str,Any]=Field(default_factory=dict)
    sentiment:str="calm"; confidence:float=1.0; clarification_needed:bool=False; mode:str="offline_fallback"; fallback_reason:str|None=None
class Decision(BaseModel):
    verdict:Verdict; action:str; rule_id:str; reason:str; inputs:dict[str,Any]=Field(default_factory=dict); authority_check:str="within policy"; executable:bool=False
class ToolResult(BaseModel): ok:bool; status:str; simulated_id:str|None=None; detail:str
