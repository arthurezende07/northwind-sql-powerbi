-- top clientes por receita
select
	c.companyname,
    c.country,
    COUNT(DISTINCT o.orderid) as pedidos,
    ROUND(SUM(d.revenue), 2) as receita_total,
    ROUND(AVG(d.revenue), 2) as ticket_medio
from vw_orders o
join customers c on o.customerid = c.customerid
join vw_order_details d on o.orderid = d.orderid
group by c.companyname, c.country
order by receita_total DESC;