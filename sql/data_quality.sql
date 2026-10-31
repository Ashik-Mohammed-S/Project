SELECT COUNT(*) AS rows_checked,
       COUNT(*) - COUNT(DISTINCT line_id) AS duplicate_line_ids,
       SUM(CASE WHEN units <= 0 OR unit_price_cents < 0 OR unit_cost_cents < 0
                     OR discount_cents < 0 OR discount_cents > units * unit_price_cents
                THEN 1 ELSE 0 END) AS invalid_lines,
       SUM(CASE WHEN unit_price_cents < contract_floor_cents THEN 1 ELSE 0 END) AS below_floor_lines
FROM ledger;
