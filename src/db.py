import sqlite3,json,uuid
from pathlib import Path
SCHEMA='''PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS conversations(id TEXT PRIMARY KEY,pnr TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS messages(id TEXT PRIMARY KEY,conversation_id TEXT,role TEXT,content TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS ai_classifications(id TEXT PRIMARY KEY,correlation_id TEXT,mode TEXT,payload TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS policy_decisions(id TEXT PRIMARY KEY,correlation_id TEXT,verdict TEXT,action TEXT,rule_id TEXT,payload TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS tool_calls(id TEXT PRIMARY KEY,correlation_id TEXT,tool TEXT,status TEXT,payload TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS actions(id TEXT PRIMARY KEY,idempotency_key TEXT UNIQUE,correlation_id TEXT,action TEXT,status TEXT,payload TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS escalations(id TEXT PRIMARY KEY,correlation_id TEXT,reason TEXT,status TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS audit_events(id TEXT PRIMARY KEY,correlation_id TEXT,stage TEXT,detail TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);'''
class Database:
 def __init__(self,path="data/runtime/airline.db"):
  self.path=path
  if path != ":memory:": Path(path).parent.mkdir(parents=True,exist_ok=True)
  self.conn=sqlite3.connect(path,check_same_thread=False); self.conn.row_factory=sqlite3.Row; self.conn.executescript(SCHEMA)
 def add(self,table,**kw):
  kw={"id":str(uuid.uuid4()),**kw}; cols=','.join(kw); qs=','.join('?'*len(kw)); self.conn.execute(f"INSERT INTO {table}({cols}) VALUES({qs})",tuple(kw.values())); self.conn.commit(); return kw['id']
 def audit(self,cid,stage,detail): self.add('audit_events',correlation_id=cid,stage=stage,detail=detail)
 def rows(self,table,where="",args=()): return [dict(x) for x in self.conn.execute(f"SELECT * FROM {table} {where}",args).fetchall()]
