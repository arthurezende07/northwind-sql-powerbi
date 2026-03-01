-- tempo médio de envio por país de destino
SELECT
	c.country,
    COUNT(DISTINCT o.orderid) as pedidos,
    ROUND(AVG(
      julianday(o.shippeddate) - julianday(o.orderdate)
      ), 1) as dias_ate_envio,
    ROUND(AVG(
      julianday(o.requireddate) - julianday(o.shippeddate)
      ), 1) as dias_folga_prazo
from vw_orders o
join customers c on o.customerid = c.customerid
WHERE shippeddate is not NULL
group by c.country
having pedidos > 3
order by dias_ate_envio DESC;