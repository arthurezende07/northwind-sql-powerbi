-- criando views

-- pedidos com datas válidas
create view vw_orders AS
select *
from orders
where orderdate is not NULL
	AND customerid is not NULL;
    
-- itens com receita líquida calculada (aplicando desconto)
create view vw_order_details AS
SELECT
	orderid,
    productid,
    unitprice,
    quantity,
    discount,
    ROUND(unitprice * quantity * (1 - discount), 2) as revenue
from order_details
where quantity > 0 and unitprice > 0;

-- join de produtos com categoria
create view vw_products as 
SELECT
	p.productid,
    p.productname,
    p.unitprice as listprice,
    p.quantityperunit,
    p.discontinued,
    c.categoryid,
    c.categoryname
from products p
join categories c on p.categoryid = c.categoryid;