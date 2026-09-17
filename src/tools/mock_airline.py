import json,uuid
from src.models import ToolResult,Verdict
class MockAirlineTools:
 def __init__(self,db): self.db=db
 def execute(self,cid,pnr,decision):
  if not decision or not decision.executable: return ToolResult(ok=False,status='blocked',detail='No executable policy authorization')
  key=f"{cid}:{decision.action}"
  old=self.db.rows('actions','WHERE idempotency_key=?',(key,))
  if old: return ToolResult(ok=True,status='idempotent_replay',simulated_id=old[0]['id'],detail='Duplicate action suppressed')
  if decision.action=='priority_rebooking_search': status='inventory_not_supplied'; detail='No alternative-flight inventory was supplied; no flight or seat invented.'
  elif decision.verdict==Verdict.ESCALATE: status='escalated'; detail='Routed to a human supervisor/specialist.'
  else: status='simulated_executed'; detail='Simulated action recorded; no real airline system changed.'
  sid='SIM-'+uuid.uuid4().hex[:10].upper()
  self.db.add('actions',id=sid,idempotency_key=key,correlation_id=cid,action=decision.action,status=status,payload=json.dumps(decision.model_dump(mode='json')))
  self.db.add('tool_calls',correlation_id=cid,tool=decision.action,status=status,payload=json.dumps({'pnr':pnr,'authorization':decision.rule_id}))
  if status=='escalated': self.db.add('escalations',correlation_id=cid,reason=decision.reason,status='open')
  return ToolResult(ok=True,status=status,simulated_id=sid,detail=detail)
