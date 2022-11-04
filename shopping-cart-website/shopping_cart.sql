create database shopping_cart;
use shopping_cart;
create table product(id varchar(100),
					name varchar(100),
					image varchar(100),
					inventory_quantity int(100),
					amount float,
					CONSTRAINT product_pk PRIMARY KEY(id)
					);
					
insert into product(id,name,image,inventory_quantity,amount)
values('1',"Samsung Phone","static_pages/mobile.jpg",1000,18000.00);

insert into product(id,name,image,inventory_quantity,amount)
values('2',"Television","static_pages/tv.jpg",500,28000);

insert into product(id,name,image,inventory_quantity,amount)
values('3',"Laptop","static_pages/laptop.jpg",100,50000);

insert into product(id,name,image,inventory_quantity,amount)
values('4',"Camera","static_pages/camera.jpg",120,15000);

create table user(id varchar(100) not null,
				name varchar(100),
				password varchar(100),
				email varchar(100),
				primary key(id)
				);
				
