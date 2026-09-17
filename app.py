import streamlit as st, pandas as pd
from src.db import Database
from src.seed_data import CUSTOMERS,SCENARIOS,POLICIES
from src.orchestrator import Orchestrator
st.set_page_config(page_title='SkyResolve AI',page_icon='✈️',layout='wide')
st.markdown('''<style>.block-container{padding-top:1.5rem}.hero{padding:20px;border-radius:18px;background:linear-gradient(120deg,#102a56,#2563eb);color:white}.card{padding:14px;border-radius:12px;background:white;border:1px solid #dce5f2;margin:7px 0}.muted{color:#667085}</style>''',unsafe_allow_html=True)
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
 if st.button('Reset visible chat',use_container_width=True): st.session_state.pop('messages',None); st.rerun()
chat,trace,about=st.tabs(['💬 Resolution workspace','🔎 Audit & trace','🛡️ Architecture & safeguards'])
with chat:
 st.caption('Exercise date: Wednesday, 23 September 2026 · Source data restricted to the supplied pack')
 st.session_state.setdefault('messages',{})
 msgs=st.session_state.messages.setdefault(pnr,[])
 for m in msgs:
  with st.chat_message(m['role']): st.write(m['content'])
 st.markdown('**Scenario quick start**')
 if st.button(SCENARIOS[pnr],key='scenario',use_container_width=True): prompt=SCENARIOS[pnr]
 else: prompt=st.chat_input('Describe what you need help with…')
 if prompt:
  msgs.append({'role':'user','content':prompt})
  with st.chat_message('user'): st.write(prompt)
  with st.spinner('Classifying intent, verifying policy, and tracing actions…'): out=agent.process(pnr,prompt)
  msgs.append({'role':'assistant','content':out['response']})
  with st.chat_message('assistant'): st.write(out['response'])
  st.subheader('Decision cards')
  for d in out['decisions']:
   icon={'ALLOW':'✅','DENY':'⛔','ESCALATE':'🧑‍✈️','ASK_CLARIFICATION':'❓'}[d.verdict.value]
   st.markdown(f"<div class='card'><b>{icon} {d.verdict.value}: {d.action.replace('_',' ').title()}</b><br><span class='muted'>{d.reason}</span></div>",unsafe_allow_html=True)
   with st.expander('Why this decision?'): st.json({'rule_id':d.rule_id,'grounded_inputs':d.inputs,'authority_check':d.authority_check,'tool_executable':d.executable})
  st.caption(f"Trace ID: {out['correlation_id']} · {out['classification'].mode}")
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
