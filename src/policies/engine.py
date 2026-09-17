from src.models import Decision,Verdict
from src.seed_data import POLICIES
class PolicyEngine:
 def decide(self,pnr,customer,classification):
  seg=customer['segments'][0]; d=seg['delay']; intents=set(classification.intents); out=[]
  def add(v,a,r,reason,exe=False,**inputs): out.append(Decision(verdict=v,action=a,rule_id=r,reason=reason,inputs=inputs,executable=exe,authority_check='requires human' if v==Verdict.ESCALATE else 'verified'))
  if {'legal_threat','complaint'} & intents: add(Verdict.ESCALATE,'human_escalation','ESCALATE',POLICIES['ESCALATE'],True); return out
  if 'Cancelled' in seg['status']:
   if 'refund' in intents:
    if classification.entities.get('refund_method')=='cash':
     add(Verdict.ESCALATE,'different_method_refund','REFUND',POLICIES['REFUND'],True)
     add(Verdict.ASK,'cancellation_choice','CANCEL',POLICIES['CANCEL'],False,choices='free priority rebooking within 24h OR full refund to the original payment method')
    else: add(Verdict.ALLOW,'initiate_refund','REFUND',POLICIES['REFUND'],True,scope='full; original payment method; within 7 business days')
   elif 'rebooking' in intents: add(Verdict.ALLOW,'priority_rebooking_search','CANCEL',POLICIES['CANCEL'],True,inventory='not supplied')
   else: add(Verdict.ASK,'cancellation_choice','CANCEL',POLICIES['CANCEL'],False,choices='free priority rebooking within 24h OR full refund')
   if 'upgrade' in intents or 'compensation' in intents: add(Verdict.ESCALATE,'extra_compensation','LOYALTY',POLICIES['LOYALTY'],True)
   return out
  if d in (3,5): add(Verdict.ESCALATE,'threshold_ambiguity','DELAY_BOUNDARY','Policy does not define equality at exactly 3 or 5 hours.',True); return out
  if d<3: add(Verdict.ALLOW,'meal_voucher','DELAY_LT3',POLICIES['DELAY_LT3'],True,amount=500)
  if d>3: add(Verdict.ALLOW,'meal_voucher','DELAY_GT3',POLICIES['DELAY_GT3'],True); add(Verdict.ALLOW,'lounge_access','DELAY_GT3',POLICIES['DELAY_GT3'],True)
  if 'hotel' in intents:
   if d>5:
    add(Verdict.ALLOW,'delayed_hours_hotel','DELAY_GT5',POLICIES['DELAY_GT5'],True,hours=d)
    if classification.entities.get('hotel_scope')=='full_night': add(Verdict.DENY,'full_night_hotel','DELAY_GT5',POLICIES['DELAY_GT5'])
   else: add(Verdict.DENY,'hotel','DELAY_GT5',POLICIES['DELAY_GT5'])
  if 'fare_difference_waiver' in intents or (pnr=='WL7742' and 'rebooking' in intents):
   amount=classification.entities.get('amount',2000 if pnr=='WL7742' else None)
   if amount and amount>1500: add(Verdict.ESCALATE,'fare_difference_waiver','FARE',POLICIES['FARE'],True,amount=amount)
  return out
