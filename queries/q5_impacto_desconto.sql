-- impacto do desconto na receita
SELECT
	p.categoryname,
    COUNT(*) as itens_vendidos,
    ROUND(AVG(d.discount), 4) as desconto_medio_pct,
    ROUND(SUM(d.unitprice *d.quantity), 2) as receita_bruta,
    ROUND(SUM(d.revenue), 2) as receita_liquida,
    ROUND(SUM(d.unitprice*d.quantity) - SUM(d.revenue), 2) as valor_descontado
from vw_order_details d
join vw_products p on d.productid = p.productid
GROUP by p.categoryname
order by valor_descontado DESC;    