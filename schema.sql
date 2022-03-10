-- Initialize the database.
-- Drop any existing data and create empty tables.
-- //SQL,结构化查询语句,用于对数据进行操作,(增,删,改,查)的语句
--        //SQL语句不区分大小写
--        //1.创建表格
--        //create table 表名 (字段名 字段数据类型 是否是主键 是否为空 默认值是多少,...)
--        //student表为例(ID,name,age,gender,photo)
--        //create table "Student" ("ID" integer primary key n t null, "name" text, "age" integer, "gender" text, "photo" blob)
--
--        //2.插入数据
--        //insert into 表名 (字段名1,字段名2,字段名2,...) values (值1,值2, 值3,...)
--
--        //例如: insert into "Student" (name,gender,age) values ("赵卫东", "男", "20")
--        //3.删除数据
--        //delete from 表名 where 字段名 = 值
--        //例如: delete from "Student" where ID = 6
--
--        //4.修改数据
--        //update 表名 set 字段名 = 值 where 字段名 = 值
--        //例如 update "Student" set gender = "女" where ID = "5"
--
--        //5.查询数据
--        //select 字段名 from 表名 where 字段名 = 值
--        //例如 select name, age from "Student" where ID = 5
--        //例如: select * from Student where name = "小强"
--        //例如: select * from Student

DROP TABLE IF EXISTS PD_table;
DROP TABLE IF EXISTS WB_table;

CREATE TABLE PD_table (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  keyword TEXT NULL
);

CREATE TABLE WB_table (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  createTime TEXT NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  keyword TEXT NULL
);
