import os
try:
 import streamlit as st
 for k in ('GROQ_API_KEY','GROQ_MODEL'):
  if k not in os.environ and k in st.secrets: os.environ[k]=str(st.secrets[k])
except Exception:
 pass
from src.llm.offline_provider import OfflineProvider
class AIService:
 def classify(self,text):
  if os.getenv('GROQ_API_KEY'):
   try:
    from src.llm.groq_provider import GroqProvider
    return GroqProvider().classify(text)
   except Exception as e:
    c=OfflineProvider().classify(text); c.fallback_reason=f'Groq {type(e).__name__}'; return c
  c=OfflineProvider().classify(text); c.fallback_reason='GROQ_API_KEY not configured'; return c
