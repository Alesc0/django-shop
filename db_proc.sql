create or replace function updateStockTgr()
returns TRIGGER
language 'plpgsql'
as
$$
DECLARE _stock numeric;
BEGIN
	select stock into _stock from shop_product where id = new.product_id;
	if (_stock - new.quantity) >= 0 then
		update shop_product set stock = stock - new.quantity where id = new.product_id;
	else
		Raise exception 'Quantity ammount higher than stock available';
	END if;
		
    return new;
END;
$$;

create trigger updateStock
BEFORE INSERT or UPDATE on shop_sales_item
FOR each row
execute function updateStockTgr();