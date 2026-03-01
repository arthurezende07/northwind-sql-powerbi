-- receita por país do cliente
select
	c.country,
    COUNT(DISTINCT o.orderid) as pedidos,
    COUNT(DISTINCT o.customerid) as clientes,
    ROUND(SUM(d.revenue), 2) as receita_total,
    ROUND(AVG(d.revenue), 2) as ticket_medio
from vw_orders o
join customers c on o.customerid = c.customerid
join vw_order_details d on o.orderid = d.orderid
group by c.country
order by receita_total DESC;