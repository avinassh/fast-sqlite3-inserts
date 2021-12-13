create table IF NOT EXISTS user (
  id INTEGER not null primary key,
  area CHAR(6),
  age INTEGER not null,
  active INTEGER not null
);

insert into user (area, age, active)
select 
  abs(random() % 99999) as area, 
  (abs(random() % 3) + 1) * 5 as age, 
  abs(random() % 1) as active
from generate_series(1, 100000000);
