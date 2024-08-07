-- Show and add orders
SELECT "--Items Before";
SELECT * FROM items;
SELECT * FROM orders;

INSERT INTO orders (item_name, number) VALUES ('apple', 1);
INSERT INTO orders (item_name, number) VALUES ('apple', 3);
INSERT INTO orders (item_name, number) VALUES ('pear', 2);


SELECT "--Created Orders";
SELECT * FROM orders;
SELECT "--Items After";
SELECT * FROM items;
