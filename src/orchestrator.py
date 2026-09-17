import json,uuid
from src.seed_data import CUSTOMERS
from src.llm.service import AIService
from src.policies.engine import PolicyEngine
from src.tools.mock_airline import MockAirlineTools
from src.response_generator import ResponseGenerator
class Orchestrator:
 def __init__(self,db,ai=None): self.db=db; self.ai=ai or AIService(); self.policy=PolicyEngine(); self.tools=MockAirlineTools(db)
 def process(self,pnr,text,conversation_id=None):
  if pnr not in CUSTOMERS: raise ValueError('Unknown PNR')
  conv=conversation_id or self.db.add('conversations',pnr=pnr); cid=str(uuid.uuid4())
  self.db.add('messages',conversation_id=conv,role='customer',content=text); self.db.audit(cid,'input',f'PNR {pnr}; customer message received')
  c=self.ai.classify(text); self.db.add('ai_classifications',correlation_id=cid,mode=c.mode,payload=c.model_dump_json()); self.db.audit(cid,'classification',f'{c.mode}: {c.intents}')
  ds=self.policy.decide(pnr,CUSTOMERS[pnr],c); results=[]
  for d in ds:
   self.db.add('policy_decisions',correlation_id=cid,verdict=d.verdict.value,action=d.action,rule_id=d.rule_id,payload=d.model_dump_json()); self.db.audit(cid,'policy',f'{d.verdict}: {d.action} via {d.rule_id}')
   if d.executable: results.append(self.tools.execute(cid,pnr,d))
  response=ResponseGenerator().generate(CUSTOMERS[pnr]['name'],c,ds,results); self.db.add('messages',conversation_id=conv,role='assistant',content=response); self.db.audit(cid,'response','Grounded deterministic response generated')
  return {'conversation_id':conv,'correlation_id':cid,'classification':c,'decisions':ds,'results':results,'response':response}
