SELECT contract_id, COUNT(*) AS affected_lines,
       SUM(units * (contract_floor_cents - unit_price_cents)) AS price_gap_cents
FROM ledger
WHERE unit_price_cents < contract_floor_cents
GROUP BY contract_id
ORDER BY price_gap_cents DESC, contract_id;
