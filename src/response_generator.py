from src.models import Verdict
class ResponseGenerator:
 def generate(self,name,classification,decisions,results):
  empathy={'angry':"I hear how frustrating this is. ",'frustrated':"I'm sorry this disruption is affecting your plans. ",'confused':"I'll make this clear. "}.get(classification.sentiment,'')
  lines=[]
  for d in decisions:
   if d.verdict==Verdict.ALLOW: lines.append(f"Allowed: {d.action.replace('_',' ')}. {d.reason}")
   elif d.verdict==Verdict.DENY: lines.append(f"I can't approve {d.action.replace('_',' ')}. {d.reason}")
   elif d.verdict==Verdict.ESCALATE: lines.append(f"This needs human review, so I've created a simulated escalation. {d.reason}")
   else: lines.append("Please choose one: free rebooking on the next available flight within 24 hours, or a full refund to the original payment method.")
  if any(r.status=='inventory_not_supplied' for r in results): lines.append("No alternative-flight inventory was supplied, so I won't invent a flight or seat.")
  return empathy+' '.join(lines)
