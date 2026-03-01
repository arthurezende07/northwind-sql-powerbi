-- receita por mês
SELECT
	strftime('%Y-%m', o.orderdate) as mes,
    count(DISTINCT o.orderid) as pedidos,
    ROUND(SUM(d.revenue), 2) as receita_total
from vw_orders o
join vw_order_details d on o.orderid = d.orderid
GROUP by mes
order by mes;