"""Allowlisted SQL reports; no generated SQL or arbitrary database tool execution."""
import csv,json,sqlite3,threading
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPORTS=('monthly_margin','contract_leakage','data_quality')

class FinanceStore:
    def __del__(self):
        try:self.connection.close()
        except Exception:pass
    def __init__(self,path=None):
        self.connection=sqlite3.connect(':memory:',check_same_thread=False)
        self.lock=threading.RLock();self.connection.row_factory=sqlite3.Row
        self.connection.execute('CREATE TABLE ledger(line_id TEXT PRIMARY KEY, month TEXT NOT NULL, store_id TEXT NOT NULL, product_id TEXT NOT NULL, contract_id TEXT NOT NULL, units INTEGER NOT NULL, unit_price_cents INTEGER NOT NULL, contract_floor_cents INTEGER NOT NULL, unit_cost_cents INTEGER NOT NULL, discount_cents INTEGER NOT NULL)')
        with Path(path or ROOT/'data/synthetic_ledger.csv').open(encoding='utf-8',newline='') as f:
            rows=list(csv.DictReader(f))
        values=[tuple([r[k] for k in ['line_id','month','store_id','product_id','contract_id']]+[int(r[k]) for k in ['units','unit_price_cents','contract_floor_cents','unit_cost_cents','discount_cents']]) for r in rows]
        self.connection.executemany('INSERT INTO ledger VALUES (?,?,?,?,?,?,?,?,?,?)',values)
        self.connection.commit();self.connection.execute('PRAGMA query_only=ON')
    def report(self,name):
        if name not in REPORTS:raise ValueError('Unknown report')
        sql=(ROOT/'sql'/f'{name}.sql').read_text(encoding='utf-8')
        with self.lock:return [dict(r) for r in self.connection.execute(sql)]
    def evidence(self):
        quality=self.report('data_quality')[0];leakage=self.report('contract_leakage')
        total=sum(r['price_gap_cents'] for r in leakage)
        return {'id':'ledger_snapshot','title':'Synthetic ledger snapshot and contract exceptions',
            'source':'sql/contract_leakage.sql',
            'body':f"The fictional Harbor Retail ledger has {quality['rows_checked']} rows, {quality['duplicate_line_ids']} duplicate line IDs and {quality['invalid_lines']} invalid lines. The contract price-floor query identifies {quality['below_floor_lines']} below-floor lines, with a total price gap of {total} cents. This is a synthetic potential exposure, not realized revenue recovery. Monthly revenue, cost and gross margin are computed from integer cents using the committed SQL templates."}
