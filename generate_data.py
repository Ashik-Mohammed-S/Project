"""Deterministic fictional retail ledger. Contains no employer or customer data."""
import csv,random
from pathlib import Path

def generate(path):
    rng=random.Random(2027);rows=[]
    for month in range(1,7):
        for store in range(1,9):
            for product in range(1,13):
                price=800+product*125;units=rng.randint(20,150)
                actual=price-150 if product==3 and store in (2,6) and month>=3 else price
                rows.append(dict(line_id=f'L{len(rows)+1:05}',month=f'2026-{month:02}',store_id=f'S{store:02}',
                    product_id=f'P{product:02}',contract_id=f'C{(product-1)//3+1:02}',units=units,
                    unit_price_cents=actual,contract_floor_cents=price,unit_cost_cents=int(price*.66),discount_cents=rng.randint(0,300)))
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    return rows

if __name__=='__main__':
    print('Synthetic lines generated:',len(generate(Path(__file__).parent/'data/synthetic_ledger.csv')))
