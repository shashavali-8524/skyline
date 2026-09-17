import pytest
from src.db import Database
from src.orchestrator import Orchestrator
from src.llm.offline_provider import OfflineProvider
from src.policies.engine import PolicyEngine
from src.seed_data import CUSTOMERS
from src.models import Classification
@pytest.fixture
def agent(): return Orchestrator(Database(':memory:'),OfflineProvider())
def pairs(out): return {(d.action,d.verdict.value) for d in out['decisions']}
def test_priya_choice(agent): assert ('cancellation_choice','ASK_CLARIFICATION') in pairs(agent.process('SK4821X','What are my options?'))
def test_priya_cash_and_upgrade(agent):
 p=pairs(agent.process('SK4821X','furious, cash refund and business upgrade'))
 assert ('different_method_refund','ESCALATE') in p and ('extra_compensation','ESCALATE') in p
def test_priya_refund(agent):
 o=agent.process('SK4821X','refund to original payment method'); d=o['decisions'][0]
 assert d.verdict.value=='ALLOW' and '7 business days' in d.reason
def test_arvind(agent):
 p=pairs(agent.process('TR1190B','I want a hotel for this delay'))
 assert ('meal_voucher','ALLOW') in p and ('lounge_access','ALLOW') in p and ('hotel','DENY') in p
def test_meher(agent):
 p=pairs(agent.process('WL7742',"full night's hotel, waive ₹2,000 fare difference"))
 assert ('delayed_hours_hotel','ALLOW') in p and ('full_night_hotel','DENY') in p and ('fare_difference_waiver','ESCALATE') in p
def test_legal(agent): assert ('human_escalation','ESCALATE') in pairs(agent.process('TR1190B','I will take legal action'))
def test_anger_not_legal(agent): assert not any(d.action=='human_escalation' for d in agent.process('TR1190B','I am furious')['decisions'])
def test_no_inventory(agent): assert agent.process('SK4821X','rebook me')['results'][0].status=='inventory_not_supplied'
def test_idempotent_tool_auth(agent):
 from src.models import Decision,Verdict
 d=Decision(verdict=Verdict.DENY,action='x',rule_id='x',reason='x')
 assert not agent.tools.execute('c','SK4821X',d).ok
def test_boundaries():
 e=PolicyEngine(); c={'segments':[{'status':'Delayed 3h','delay':3}]}; out=e.decide('X',c,Classification(intents=['hotel']))
 assert out[0].action=='threshold_ambiguity' and out[0].verdict.value=='ESCALATE'
def test_ownership(agent):
 with pytest.raises(ValueError): agent.process('BAD','refund')
def test_ppt_exists_and_ten():
 from pathlib import Path
 from pptx import Presentation
 p=Path('artifacts/Assignment_3_Airline_Resolution_Agent.pptx'); assert p.exists(); assert len(Presentation(p).slides)==10
def test_groq_provider_structured_path():
 from types import SimpleNamespace
 from src.llm.groq_provider import GroqProvider
 payload='{"intents":["hotel"],"entities":{"hotel_scope":"full_night"},"sentiment":"frustrated","confidence":0.99,"clarification_needed":false}'
 class Completions:
  def create(self,**kwargs):
   assert kwargs['model']=='llama-3.3-70b-versatile'; assert kwargs['response_format']=={'type':'json_object'}
   return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=payload))])
 fake=SimpleNamespace(chat=SimpleNamespace(completions=Completions()))
 c=GroqProvider(client=fake).classify('I want a hotel')
 assert c.mode=='live_groq' and c.intents==['hotel'] and c.entities['hotel_scope']=='full_night'
