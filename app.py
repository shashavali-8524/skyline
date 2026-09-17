import streamlit as st, pandas as pd
from src.db import Database
from src.seed_data import CUSTOMERS,SCENARIOS,POLICIES
from src.orchestrator import Orchestrator
st.set_page_config(page_title='SkyResolve AI',page_icon='✈️',layout='wide')
st.markdown('''<style>.block-container{padding-top:1.5rem}.hero{padding:20px;border-radius:18px;background:linear-gradient(120deg,#102a56,#2563eb);color:white}.muted{color:#667085}
div[data-testid="stExpander"]{background:white;border:1px solid #dce5f2;border-radius:12px;margin:7px 0}
div[data-testid="stExpander"] summary{border-radius:12px;padding:10px 12px}
div[data-testid="stExpander"] summary:hover{background:#f4f8ff}
div[data-testid="stExpander"] summary p{font-weight:600}
</style>''',unsafe_allow_html=True)
@st.cache_resource
def services():
 d=Database(); return d,Orchestrator(d)
db,agent=services()
st.markdown("<div class='hero'><h1>✈️ SkyResolve AI</h1><p>Auditable airline-disruption resolution. Every airline action shown here is simulated.</p></div>",unsafe_allow_html=True)
with st.sidebar:
 st.header('Customer context'); pnr=st.selectbox('Choose supplied booking',list(CUSTOMERS),format_func=lambda x:f"{CUSTOMERS[x]['name']} · {x}")
 c=CUSTOMERS[pnr]; st.metric('Loyalty tier',c['tier']); st.caption(c['history'])
 for s in c['segments']: st.markdown(f"**{s['flight']} · {s['route']}**  \n{s['date']} at {s['scheduled']}  \n{s['status']}"+(f" · new {s.get('new')}" if s.get('new') else ''))
 mode='Live Groq' if __import__('os').getenv('GROQ_API_KEY') else 'Offline fallback'; st.info(f'AI mode: {mode}')
 if st.button('Reset conversation',use_container_width=True):
  st.session_state.pop('messages',None); st.session_state.pop('conversation_ids',None); st.rerun()
chat,trace,about=st.tabs(['💬 Resolution workspace','🔎 Audit & trace','🛡️ Architecture & safeguards'])
with chat:
 st.caption('Exercise date: Wednesday, 23 September 2026 · Source data restricted to the supplied pack')
 st.session_state.setdefault('messages',{})
 st.session_state.setdefault('conversation_ids',{})
 msgs=st.session_state.messages.setdefault(pnr,[])
 icons={'ALLOW':'✅','DENY':'⛔','ESCALATE':'🧑‍✈️','ASK_CLARIFICATION':'❓'}
 def decision_cards(m):
  st.markdown('**Decision cards** - click a card to see the rule, grounded inputs, and authority check')
  for d in m.get('decisions',[]):
   with st.expander(f"{icons[d['verdict']]} {d['verdict'].replace('_',' ')}: {d['action'].replace('_',' ').title()}"):
    st.markdown(f"<span class='muted'>{d['reason']}</span>",unsafe_allow_html=True)
    st.json({'rule_id':d['rule_id'],'grounded_inputs':d['inputs'],'authority_check':d['authority_check'],'tool_executable':d['executable']})
  if m.get('trace'): st.caption(m['trace'])
 for m in msgs:
  with st.chat_message(m['role']):
   st.write(m['content'])
   if m['role']=='assistant': decision_cards(m)
 st.markdown('**Scenario quick start**')
 if st.button(SCENARIOS[pnr],key='scenario',use_container_width=True): prompt=SCENARIOS[pnr]
 else: prompt=st.chat_input('Describe what you need help with…')
 if prompt:
  msgs.append({'role':'user','content':prompt})
  conversation_id=st.session_state.conversation_ids.get(pnr)
  with st.spinner('Classifying intent, verifying policy, and tracing actions…'):
   out=agent.process(pnr,prompt,conversation_id=conversation_id)
  st.session_state.conversation_ids[pnr]=out['conversation_id']
  msgs.append({'role':'assistant','content':out['response'],
   'decisions':[{'verdict':d.verdict.value,'action':d.action,'rule_id':d.rule_id,'reason':d.reason,'inputs':d.inputs,'authority_check':d.authority_check,'executable':d.executable} for d in out['decisions']],
   'trace':f"Trace ID: {out['correlation_id']} · {out['classification'].mode}"})
  st.rerun()
with trace:
 rows=db.rows('audit_events','ORDER BY created_at DESC LIMIT 100')
 st.dataframe(rows,use_container_width=True,hide_index=True)
 if rows: st.download_button('Download audit CSV',pd.DataFrame(rows).to_csv(index=False),file_name='audit_trace.csv',mime='text/csv')
with about:
 st.markdown('''### Safety split
- **AI layer:** intent, entities, sentiment; optional live model with validated fallback.
- **Orchestrator:** conversation state, routing, policy-before-tool workflow.
- **Policy engine:** deterministic ALLOW / DENY / ESCALATE / ASK decisions.
- **Mock tool gateway:** authorization-token check, idempotency, simulated actions only.
- **SQLite:** messages, decisions, actions, escalations, and correlated audit events.

### Non-invention guardrail
No alternative-flight inventory was supplied. The app never creates a flight, seat, hotel name, payment instrument, or refund amount.''')
