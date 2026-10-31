SELECT month,
       SUM(units * unit_price_cents - discount_cents) AS net_revenue_cents,
       SUM(units * unit_cost_cents) AS cost_cents,
       SUM(units * (unit_price_cents - unit_cost_cents) - discount_cents) AS gross_margin_cents,
       ROUND(1.0 * SUM(units * (unit_price_cents - unit_cost_cents) - discount_cents)
             / NULLIF(SUM(units * unit_price_cents - discount_cents), 0), 6) AS gross_margin_rate
FROM ledger
GROUP BY month
ORDER BY month;
