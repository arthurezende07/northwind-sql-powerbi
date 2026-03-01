-- top produtos por receita (não colocar limit para aumentar análises no powerbi)
SELECT
	p.productname,
    p.categoryname,
    COUNT(DISTINCT d.orderid) as pedidos,
    SUM(d.quantity) as unidades,
    ROUND(SUM(d.revenue), 2) as receita_total
from vw_order_details d
join vw_products p on d.productid = p.productid
group by p.productid, p.categoryname
order by receita_total DESC;