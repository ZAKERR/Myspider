create table article(
   title varchar(255) primary key,
   link varchar(255) not null,
   text text not null ,
   push_date varchar(255) not null,
   scrapy_time int not null
)