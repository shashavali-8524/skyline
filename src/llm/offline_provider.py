import re
from src.models import Classification
class OfflineProvider:
 def classify(self,text):
  t=text.lower(); intents=[]
  rules={"refund":["refund","cash"],"rebooking":["rebook","different","flight"],"hotel":["hotel","night"],"meal_voucher":["meal","voucher"],"lounge_access":["lounge"],"fare_difference_waiver":["waive","fare difference","₹2,000","2000"],"upgrade":["upgrade","business"],"legal_threat":["legal","lawyer","court"],"complaint":["formal complaint"]}
  for k,words in rules.items():
   if any(w in t for w in words): intents.append(k)
  sentiment="angry" if any(w in t for w in ["furious","unacceptable","angry"]) else "frustrated" if any(w in t for w in ["frustrated","miss","delay"]) else "calm"
  ents={}
  m=re.search(r'(?:₹|rs\.?\s*)?([0-9][0-9,]*)',t)
  if m: ents['amount']=int(m.group(1).replace(',',''))
  if 'cash' in t: ents['refund_method']='cash'
  if 'full night' in t or "full night's" in t: ents['hotel_scope']='full_night'
  return Classification(intents=intents or ['other'],entities=ents,sentiment=sentiment,mode='offline_fallback')
