from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pathlib import Path

W,H=13.333,7.5
NAVY='102A56'; BLUE='2563EB'; CYAN='38BDF8'; SKY='EAF2FF'; INK='17233B'; MUTED='64748B'; WHITE='FFFFFF'; BG='F5F8FC'; GREEN='10B981'; AMBER='F59E0B'; RED='EF4444'; BORDER='D9E4F2'

def rgb(h): return RGBColor.from_string(h)
def rect(s,x,y,w,h,fill,rad=False,line=None):
 sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rad else MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
 sh.fill.solid(); sh.fill.fore_color.rgb=rgb(fill); sh.line.color.rgb=rgb(line or fill)
 return sh
def text(s,x,y,w,h,txt,size=18,color=INK,bold=False,align=PP_ALIGN.LEFT,font='Aptos',margin=.03,valign=MSO_ANCHOR.TOP):
 sh=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=sh.text_frame; tf.clear(); tf.word_wrap=True
 tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=Inches(margin); tf.vertical_anchor=valign
 p=tf.paragraphs[0]; p.text=txt; p.alignment=align; p.font.name=font; p.font.size=Pt(size); p.font.bold=bold; p.font.color.rgb=rgb(color)
 return sh
def lines(s,x,y,w,items,size=17,color=INK,gap=6,bullet=True):
 sh=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(4.8)); tf=sh.text_frame; tf.clear(); tf.word_wrap=True; tf.margin_left=Inches(.03)
 for i,item in enumerate(items):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.text=('•  ' if bullet else '')+item; p.font.name='Aptos'; p.font.size=Pt(size); p.font.color.rgb=rgb(color); p.space_after=Pt(gap)
 return sh
def base(prs,num,title,kicker=None,dark=False):
 s=prs.slides.add_slide(prs.slide_layouts[6]); bg=s.background.fill; bg.solid(); bg.fore_color.rgb=rgb(NAVY if dark else BG)
 rect(s,0,0,.12,H,CYAN)
 if kicker: text(s,.55,.35,7,.25,kicker.upper(),10,CYAN,bold=True)
 text(s,.55,.62,11.9,.55,title,30,WHITE if dark else NAVY,bold=True)
 text(s,11.95,.36,.75,.28,f'{num:02d} / 10',10,'B6C6DF' if dark else MUTED,bold=True,align=PP_ALIGN.RIGHT)
 return s
def pill(s,x,y,w,label,fill,color=WHITE):
 rect(s,x,y,w,.38,fill,True); text(s,x+.04,y+.07,w-.08,.2,label,10,color,bold=True,align=PP_ALIGN.CENTER)
def card(s,x,y,w,h,title,body,accent=BLUE,icon=None):
 rect(s,x,y,w,h,WHITE,True,BORDER); rect(s,x,y,.08,h,accent,True,accent)
 if icon: text(s,x+.28,y+.22,.38,.35,icon,20,accent,bold=True,align=PP_ALIGN.CENTER)
 text(s,x+.32+(0.4 if icon else 0),y+.22,w-.62-(.4 if icon else 0),.32,title,16,NAVY,bold=True)
 text(s,x+.32,y+.72,w-.58,h-.85,body,13,MUTED)
def footer(s):
 text(s,.55,7.14,8,.2,'SKYRESOLVE AI  ·  ASSIGNMENT 3  ·  ALL AIRLINE ACTIONS SIMULATED',8,MUTED,bold=True)

prs=Presentation(); prs.slide_width=Inches(W); prs.slide_height=Inches(H)
# 1
s=prs.slides.add_slide(prs.slide_layouts[6]); s.background.fill.solid(); s.background.fill.fore_color.rgb=rgb(NAVY)
rect(s,0,0,.14,H,CYAN); rect(s,8.85,0,4.48,H,'173C77'); rect(s,9.55,.65,2.9,6.2,'1F4E97',True,'2F6FD0')
text(s,.65,.62,3.5,.3,'AIONOS · ASSIGNMENT 3',11,CYAN,bold=True)
text(s,.65,1.28,7.7,1.55,'SkyResolve AI',48,WHITE,bold=True)
text(s,.65,2.78,7.4,.86,'Airline disruption resolution\nwith deterministic operational control',25,'DCE8FA',bold=True)
pill(s,.65,4.18,1.95,'AUDITABLE',BLUE); pill(s,2.78,4.18,2.15,'POLICY-GROUNDED','0F766E'); pill(s,5.1,4.18,2.0,'SAFE BY DESIGN','9A6700')
text(s,.65,5.15,7.2,.6,'Optional AI understands the customer.\nRules decide what the system may do.',18,WHITE)
text(s,9.92,1.15,2.15,.4,'✈',34,WHITE,bold=True,align=PP_ALIGN.CENTER)
text(s,9.92,2.05,2.15,.32,'DEMO SYSTEM',11,CYAN,bold=True,align=PP_ALIGN.CENTER)
for i,(a,b) in enumerate([('3','customers'),('4','segments'),('15 / 15','tests')]):
 text(s,9.92,2.72+i*1.0,2.15,.38,a,24,WHITE,bold=True,align=PP_ALIGN.CENTER); text(s,9.92,3.1+i*1.0,2.15,.22,b.upper(),9,'BFD4F3',bold=True,align=PP_ALIGN.CENTER)
text(s,.65,6.92,7,.22,'Customer-Facing Resolution Agent  ·  Wednesday, 23 September 2026',9,'B6C6DF')
# 2
s=base(prs,2,'One journey, three promises','Customer experience')
card(s,.65,1.5,3.7,4.65,'UNDERSTAND','Read intent and emotion. Retrieve the supplied booking and disruption before making a recommendation.',CYAN,'1')
card(s,4.82,1.5,3.7,4.65,'RESOLVE','Ask only what is needed. Recommend or simulate the correct action after the policy check.',BLUE,'2')
card(s,8.98,1.5,3.7,4.65,'PROTECT','Escalate when authority is missing. Preserve the conversation, decision and action record.',GREEN,'3')
text(s,.7,6.42,11.8,.35,'Natural language in  →  grounded choice  →  authorized simulated action  →  traceable outcome',17,NAVY,bold=True,align=PP_ALIGN.CENTER); footer(s)
# 3
s=base(prs,3,'Grounded in the supplied pack','Inputs · sources · assumptions')
card(s,.65,1.48,4.0,2.05,'SOURCE OF TRUTH','3 supplied customers\n4 supplied flight segments\n5 policy rules\nExercise date: Wed, 23 Sep 2026',BLUE)
card(s,.65,3.78,4.0,2.12,'TECHNICAL ASSUMPTIONS','SQLite is a prototype store. Airline tools are API-shaped mocks. UUIDs, timestamps and SIM- IDs are implementation metadata.',CYAN)
rect(s,5.05,1.48,7.63,4.42,NAVY,True,NAVY); text(s,5.48,1.85,6.7,.3,'THE HARD BOUNDARY',12,CYAN,bold=True)
text(s,5.48,2.35,6.6,.75,'If the pack does not say it,\nSkyResolve does not invent it.',27,WHITE,bold=True)
lines(s,5.48,3.55,6.5,['No alternate flight or seat inventory','No hotel names or payment instruments','No refund amounts or extra compensation','Sample conversations guide tone only'],15,'DCE8FA',9)
footer(s)
# 4
s=base(prs,4,'Production-shaped architecture','System design')
# nodes
nodes=[(.6,1.75,2.0,.9,'STREAMLIT UI','Customer + agent workspace',CYAN),(3.05,1.75,2.2,.9,'ORCHESTRATOR','Context · routing · trace',BLUE),(5.72,1.15,2.2,.9,'VALIDATED AI','Intent · entities · sentiment','7C3AED'),(5.72,2.48,2.2,.9,'POLICY ENGINE','ALLOW · DENY · ESCALATE · ASK',GREEN),(8.38,2.48,2.15,.9,'GUARDRAIL','Authorization token',AMBER),(10.98,2.48,1.75,.9,'MOCK TOOLS','Simulated actions',RED),(4.42,4.65,4.5,.95,'SQLITE AUDIT STORE','Messages · classifications · decisions · tools · actions · escalations',NAVY)]
for x,y,w,h,t,b,c in nodes:
 rect(s,x,y,w,h,WHITE,True,c); rect(s,x,y,w,.08,c,True,c); text(s,x+.16,y+.2,w-.32,.25,t,13,NAVY,bold=True,align=PP_ALIGN.CENTER); text(s,x+.12,y+.53,w-.24,.2,b,9,MUTED,align=PP_ALIGN.CENTER)
def conn(x1,y1,x2,y2,color=BLUE):
 sh=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2)); sh.line.color.rgb=rgb(color); sh.line.width=Pt(2); sh.line.end_arrowhead=True
conn(2.6,2.2,3.05,2.2); conn(5.25,2.2,5.72,1.6); conn(5.25,2.2,5.72,2.92); conn(7.92,2.92,8.38,2.92); conn(10.53,2.92,10.98,2.92); conn(6.82,3.38,6.82,4.65,GREEN); conn(11.85,3.38,8.2,4.65,RED)
pill(s,.7,6.15,3.0,'AI PROPOSES', '7C3AED'); pill(s,3.9,6.15,3.3,'POLICY AUTHORIZES',GREEN); pill(s,7.4,6.15,4.5,'TOOLS EXECUTE ONLY WITH A TOKEN',RED); footer(s)
# 5
s=base(prs,5,'Every request follows one controlled path','Agent orchestration')
steps=[('01','Retrieve','Customer + disruption'),('02','Classify','Intent · entities · sentiment'),('03','Route','Legal/formal → human'),('04','Verify','Policy checks candidate action'),('05','Invoke','Authorized simulated tool'),('06','Respond','Grounded reply + trace')]
for i,(n,t,b) in enumerate(steps):
 x=.65+i*2.06; rect(s,x,1.65,1.74,3.65,WHITE,True,BORDER); pill(s,x+.48,1.92,.78,n,BLUE); text(s,x+.18,2.63,1.38,.32,t,16,NAVY,bold=True,align=PP_ALIGN.CENTER); text(s,x+.18,3.18,1.38,1.0,b,12,MUTED,align=PP_ALIGN.CENTER)
 if i<5: text(s,x+1.78,3.0,.25,.3,'→',18,BLUE,bold=True,align=PP_ALIGN.CENTER)
rect(s,.65,5.7,12.03,.62,'E8F8F2',True,'C6ECDD'); text(s,.9,5.91,11.5,.25,'The LLM never decides eligibility and never invokes tools.',16,'0F766E',bold=True,align=PP_ALIGN.CENTER); footer(s)
# 6
s=base(prs,6,'AI helps with language - not authority','AI layer + safe fallback')
rect(s,.65,1.45,5.45,4.65,'EEF0FF',True,'DCD8FF'); text(s,1.05,1.82,4.7,.3,'LIVE MODE',11,'7C3AED',bold=True); text(s,1.05,2.3,4.7,.5,'Optional Groq classifier',25,NAVY,bold=True)
lines(s,1.05,3.05,4.6,['Structured, validated intents','Entities and sentiment','Safe customer phrasing'],16,INK,10)
rect(s,7.23,1.45,5.45,4.65,'EAF7FF',True,'CDEBFA'); text(s,7.63,1.82,4.7,.3,'FALLBACK MODE',11,'0369A1',bold=True); text(s,7.63,2.3,4.7,.5,'Deterministic fallback',25,NAVY,bold=True)
lines(s,7.63,3.05,4.6,['No key, malformed output or timeout','Transparent offline behavior','Same deterministic policy gate'],16,INK,10)
text(s,6.28,3.18,.75,.5,'OR',18,MUTED,bold=True,align=PP_ALIGN.CENTER)
rect(s,2.2,6.35,8.9,.48,NAVY,True,NAVY); text(s,2.45,6.49,8.4,.2,'Customer text is untrusted data. Policy remains deterministic.',13,WHITE,bold=True,align=PP_ALIGN.CENTER); footer(s)
# 7
s=base(prs,7,'Policy is the control plane','Guardrails')
items=[('ALLOW',GREEN,'Within policy and authority'),('DENY',RED,'Explicitly outside supplied policy'),('ESCALATE',AMBER,'Needs a human or higher authority'),('ASK',BLUE,'Missing a decision or grounded fact')]
for i,(t,c,b) in enumerate(items):
 x=.65+(i%2)*6.15; y=1.48+(i//2)*1.35; rect(s,x,y,5.85,1.05,WHITE,True,BORDER); pill(s,x+.25,y+.32,1.35,t,c); text(s,x+1.82,y+.35,3.65,.3,b,14,NAVY,bold=True)
card(s,.65,4.38,3.75,1.72,'MONEY & LOYALTY','Original-method refunds only. ₹1,500 waiver cap. Gold/Platinum add priority, not compensation.',BLUE)
card(s,4.79,4.38,3.75,1.72,'HOTEL & INVENTORY','Hotel covers delayed hours only. No invented flights, seats, hotels or availability.',CYAN)
card(s,8.93,4.38,3.75,1.72,'SAFETY & TRACE','Ownership checks, idempotency and immediate legal/formal escalation before mutation.',GREEN)
text(s,.72,6.47,11.8,.3,'Source silence at exactly 3h or 5h is handled by escalation - never by inventing a rule.',14,NAVY,bold=True,align=PP_ALIGN.CENTER); footer(s)
# 8
s=base(prs,8,'Three customers prove the decision logic','Scenario outcomes')
card(s,.65,1.5,3.72,4.85,'PRIYA · GOLD','CANCELLED\n\nOffer free next-available rebooking within 24h or full refund to original method. Cash/different-method refund and free upgrade escalate. Anger alone is not a legal escalation.',BLUE)
card(s,4.81,1.5,3.72,4.85,'ARVIND · SILVER','4-HOUR DELAY\n\n₹500 meal voucher + lounge are allowed. Hotel is denied. A missed meeting creates no additional policy benefit.',CYAN)
card(s,8.97,1.5,3.72,4.85,'MEHER · PLATINUM','6-HOUR DELAY\n\nMeal + lounge + six delayed hours of hotel are allowed. Full night is denied. ₹2,000 waiver exceeds authority and escalates.',GREEN)
pill(s,1.5,5.62,2.05,'CHOICE + REVIEW',BLUE); pill(s,5.7,5.62,2.05,'ALLOW + DENY',CYAN,NAVY); pill(s,9.85,5.62,2.05,'ALLOW + ESCALATE',GREEN); footer(s)
# 9
s=base(prs,9,'One correlation ID connects the full story','Traceability + quality')
# pipeline
for i,(t,c) in enumerate([('INPUT',CYAN),('AI', '7C3AED'),('RULES',GREEN),('TOOLS',RED),('RESPONSE',BLUE)]):
 x=.7+i*2.52; pill(s,x,1.55,1.85,t,c);
 if i<4:text(s,x+1.9,1.59,.5,.22,'→',16,MUTED,bold=True,align=PP_ALIGN.CENTER)
rect(s,.7,2.45,7.6,3.25,WHITE,True,BORDER); text(s,1.05,2.82,6.9,.32,'AUDIT STORE CAPTURES',12,BLUE,bold=True)
lines(s,1.05,3.4,6.9,['Messages and classifications','Decisions and reasons','Tool calls and simulated actions','Escalations and CSV export'],16,INK,9)
rect(s,8.72,2.45,3.95,3.25,NAVY,True,NAVY); text(s,9.08,2.86,3.2,.35,'15 / 15',34,WHITE,bold=True,align=PP_ALIGN.CENTER); text(s,9.08,3.48,3.2,.3,'TESTS PASS',11,CYAN,bold=True,align=PP_ALIGN.CENTER); text(s,9.08,4.12,3.2,1.0,'Scenarios · authority\nambiguity · ownership\ninventory · multi-turn cards',13,'DCE8FA',align=PP_ALIGN.CENTER)
footer(s)
#10
s=base(prs,10,'Demo now. Production next.','Delivery + roadmap',dark=True)
rect(s,.65,1.48,5.72,4.75,'173C77',True,'2D5791'); text(s,1.02,1.85,4.95,.3,'LIVE DEMO',11,CYAN,bold=True)
lines(s,1.02,2.4,4.95,['Run Priya and click decision evidence','Continue the conversation across turns','Show Arvind and Meher outcomes','Open audit trace and export','Confirm 15/15 tests'],16,WHITE,10)
rect(s,6.78,1.48,5.9,4.75,'F8FAFC',True,'D9E4F2'); text(s,7.15,1.85,5.1,.3,'PRODUCTION PATH',11,BLUE,bold=True)
lines(s,7.15,2.4,5.1,['Authenticated customer sessions','Live booking, inventory and refund APIs','Secrets, RBAC and encryption','Human case queues and monitoring','Classifier and response evaluation'],16,INK,10)
text(s,.8,6.58,11.75,.45,'Empathetic AI experience. Deterministic operational control.',22,WHITE,bold=True,align=PP_ALIGN.CENTER)
text(s,.65,7.12,8,.18,'CURRENT LIMITS  ·  static supplied data  ·  local SQLite  ·  simulated airline actions  ·  no real inventory',8,'B6C6DF',bold=True)

out=Path('artifacts/Assignment_3_Airline_Resolution_Agent.pptx'); out.parent.mkdir(exist_ok=True); prs.save(out)
assert len(Presentation(out).slides)==10
print(out)
