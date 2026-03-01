-- receita por categoria de produto
SELECT
	p.categoryname,
    COUNT(DISTINCT d.orderid) as pedidos,
    SUM(d.quantity) as unidades_vendidas,
    ROUND(SUM(d.revenue), 2) as receita_total,
    ROUND(AVG(d.revenue), 2) as receita_media_item
from vw_order_details d
join vw_products p on d.productid = p.productid
group by p.categoryname
order by receita_total DESC;