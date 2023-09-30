# 去重查询


在需要去重的查询字段前加上`distinct`


# 模糊查询


模糊查询通配符:


- % : 表示任意多个字符,包含0个字符.
- _ : 任意单个字符



查询员工名中包含 'a' 的员工信息

```sql
select * from employees  where last_name like '%a%';
```




查询员工名中第二个字母为_的员工信息


```sql
#转移字符
select * from employees  where last_name like '_\_%';

#或 自定义转移字符
select * from employees  where last_name like '_$_%' escape '$';
```


# between and


- 包含临界值
- 两个临界值不可调换顺序



查询员工编号在100到200之间的员工信息


```sql
select * from employees
where employees_id between 100 and 200;
```


# in


- 判断字段的值是否属于in列表中的某一项
- in列表中值的类型必须一致



查询员工部门编号为1,3,5,7的员工姓名和部门编号


```sql
select employee_name dpt_id
from employees
where dpt_id in(1,3,5,7);
```


# is null 和 is not null


- =或<>不能判断null值



查询有奖金的员工信息


```sql
select * from employees
where bonus is not null;
```


# 排序查询


- 升序: ASC(默认)
- 降序: DESC



排序条件可以为`表达式`,`别名`,`函数`,还可以按多个字段排序


注意: `ORDER BY` 必须放在`WHERE`条件之后


查询员工信息,要求工资从高到底


```sql
select * from employees ORDER BY salary DESC;
```



查询员工信息,要求先按`工资升序`,再按员工`编号降序`


```sql
select * from employees
ORDER BY salary ASC,employess_id DESC;
```


# 常见函数


- 字符函数
- 数学函数
- 日期函数
- 流程控制函数
- 分组函数



## 字符函数


1. `length(agrs)`： 获取参数值的字节个数
2. `concat(agrs,agrs1,...)`: 拼接字符串
3. `upper(agrs)`: 将字母变大写
4. `lower(agrs)`: 将字母变小写
5. `substr(str,opt),substr(str,opt,length)`: 字符串截取,`str`表示字符,`opt`表示索引,从1开始,`length`表示长度
6. `instr(str,substr)`: 返回字串第一次出现的索引,如果找不到字串返回0;
7. `trim(str)`:去前后空格,`trim(substr FROM str)`: 去除字符substr
8. `lpad(str,len,padstr)`: 左填充; 将指定字符`pad`填充到字符str左边满长度`len`
9. `repad(str,len,padstr)` : 右填充
10. `replace(str,form_str,to_str)` : 将`str`字符串中的字串`from_str`替换成`to_str`字符串



## 数字函数


1. `round(ages)`, `round(args,number)`:四舍五入; 当只有一个参数时,就是将小数四舍五入; 两个参数时,将保留小数位number
2. `ceil(number)`: 向上取整.
3. `floor(number)`:向下取整.
4. `truncat(double,number)` : 去小数点number位后去掉.
5. `mod(num1,num2)`:取余=>num%num2



## 日期函数


1. `now()` : 返回当前系统日期+时间

2. `curdate()`: 返回当前系统日期,不包含时间

3. `curtime()`:返回当前系统时间,不包含日期

4. `str_to_date(str)`: 将日期格式的字符转换成指定格式的日期

   ```sql
   STR_TO_DATE('2019-4-19','%Y-%m-%d')
   ```


5. `date_format(date)`:将日期转换成字符

   ```sql
   DATE_FORMAT('2019/4/19','%Y年%m月%d日')
   ```




## 流程控制函数


1. `if(expre1,expre2,expre3)`: `expre1`表示表达式,当条件成立时,选择值`expre2`,当条件不成立时选择值`expre3`

2. `case` : 用法一

   ```sql
   case dept_id #部门编号
   when 1 then salary*1.2 #如果是1号部门工资1.2倍
   when 2 then salary*1.3 #如果是2号部门工资1.3被
   when 3 then salary*1.4 #如果是2号部门工资1.4被
   else salary  #否则为原工资
   ```


3. `case` : 用法二

   ```sql
   case
   when 表达式1 then 要显示的值1或表达式1
   when 表达式2 then 要显示的值2或表达式2
   when 表达式3 then 要显示的值3或表达式3
   else 要显示的值n或表达式n
   ```




## 分组函数


1. `sum` : 求和,计算时忽略null值
2. `avg` : 平均值,计算时忽略null值
3. `max` : 最大值,计算时忽略null值
4. `min` : 最小值,计算时忽略null值
5. `count`:计算个数,计算时忽略null值



# 分组查询


语法


```sql
select 分组函数,列(要求出现在group by的后面)
from 表
[where 筛选条件]
group by 分组的列表
[order by 子句]
```

**注意:** `查询列表`是`分组函数`和`group by` 后出现的字段

案例：查询学生的男生和女生人数各是多少

```sql
SELECT gender, COUNT(*) 人数 FROM student  GROUP BY gender
```



## 分组后筛选: `having`

案例：查询学生年各龄人数大于2的各年龄人数

```sql
SELECT
	gender,
	COUNT(*) 人数
FROM
	student
GROUP BY
	gender
HAVING
	COUNT(*)>2
```



`group by` 和 `having` 都支持别名


# 分页查询

---

查询返回的记录太多了，查看起来很不方便， 所谓分页显示，就是将数据库中的结果集，一段一段显示 出来需要的条件

**注意：** limit子句必须放在整个查询语句的最后！

```sql
select table from column limit start pageSize;
```



**start：** 就是当前页的起始索引

**pageSize：** 就是每页的条数

**currentPage：** 就是当前页

公式：

```sql
select  tableName from column... limit (currentPage-1)*pageSize pageSize
```


# 连接查询


连接查询又称为多表查询

1. 内连接
   1. 等值连接
   2. 非等值连接
   3. 自连接
2. 外连接
   1. 左外连接
   2. 右外连接
   3. 全外连接(MySQL不支持)
3. 交叉连接



**语法：**

```sql
select 查询列表
from 表1 别名
<连接类型> join 表2 别名
on 连接条件
[where 筛选条件]
[group by 分组]
[having 筛选条件]
[order by 排序列表]
```


## 笛卡尔集
笛卡尔集会在下面条件下产生

- 省略连接条件
- 连接条件无效
- 所有表中的所有行互相连接



## 内连接
特点：

1. 添加排序、分组、筛选
2. inner可以省略
3.  筛选条件放在where后面，连接条件放在on后面，提高分离性，便于阅读




分类：

1. 等值
1. 非等值
1. 自连接



语法：
```sql
select 查询列表
from 表1 别名
inner join 表2 别名
on 连接条件;
```



### 等值连接

案例1.查询员工名、部门名
```sql
SELECT last_name,department_name
FROM departments d
JOIN  employees e
ON e.`department_id` = d.`department_id`;
```



案例2.查询名字中包含e的员工名和工种名（添加筛选）

```sql
SELECT last_name,job_title
FROM employees e
INNER JOIN jobs j
ON e.job_id=  j.job_id
WHERE e.last_name LIKE '%e%';
```



案例3. 查询部门个数>3的城市名和部门个数，（添加分组+筛选）

1. 查询每个城市的部门个数
2. 在1结果上筛选满足条件的

```sql
SELECT city,COUNT(*) 部门个数
FROM departments d
INNER JOIN locations l
ON d.location_id=l.location_id
GROUP BY city
HAVING COUNT(*)>3;
```



案例4.查询哪个部门的员工个数>3的部门名和员工个数，并按个数降序（添加排序）

1. 查询每个部门的员工个数

```sql
SELECT COUNT(*),department_name
FROM employees e
INNER JOIN departments d
ON e.department_id=d.department_id
GROUP BY department_name
```


2. 在1结果上筛选员工个数>3的记录，并排序

```sql
SELECT COUNT(*) 个数,department_name
FROM employees e
INNER JOIN departments d
ON e.department_id=d.department_id
GROUP BY department_name
HAVING COUNT(*)>3
ORDER BY COUNT(*) DESC;
```



案例5.查询员工名、部门名、工种名，并按部门名降序（添加三表连接）

```sql
SELECT last_name,department_name,job_title
FROM employees e
INNER JOIN departments d ON e.department_id=d.department_id
INNER JOIN jobs j ON e.job_id = j.job_id
ORDER BY department_name DESC;
```



### 非等值连接

查询员工的工资级别
```sql
SELECT salary,grade_level
FROM employees e
 JOIN job_grades g
 ON e.`salary` BETWEEN g.`lowest_sal` AND g.`highest_sal`;
```



 查询工资级别的个数>20的个数，并且按工资级别降序

```sql
SELECT COUNT(*),grade_level
FROM employees e
 JOIN job_grades g
 ON e.`salary` BETWEEN g.`lowest_sal` AND g.`highest_sal`
 GROUP BY grade_level
 HAVING COUNT(*)>20
 ORDER BY grade_level DESC;
```



### 自连接

 查询员工的名字、上级的名字
```sql
SELECT e.last_name,m.last_name
 FROM employees e
 JOIN employees m
 ON e.`manager_id`= m.`employee_id`;
```


 查询姓名中包含字符k的员工的名字、上级的名字
```sql
SELECT e.last_name,m.last_name
 FROM employees e
 JOIN employees m
 ON e.`manager_id`= m.`employee_id`
 WHERE e.`last_name` LIKE '%k%';
```



## 外连接

 应用场景：用于查询一个表中有，另一个表没有的记录

 特点：

1. 外连接的查询结果为主表中的所有记录，如果从表中有和它匹配的，则显示匹配的值，如果从表中没有和它匹配的，则显示null，外连接查询结果=内连接结果+主表中有而从表没有的记录
1. 左外连接，left join左边的是主表，右外连接，right join右边的是主表
1. 左外和右外交换两个表的顺序，可以实现同样的效果
1. 全外连接=内连接的结果+表1中有但表2没有的+表2中有但表1没有的



### 左外连接
 查询哪个部门没有员工
```sql
SELECT d.*,e.employee_id
 FROM departments d
 LEFT OUTER JOIN employees e
 ON d.`department_id` = e.`department_id`
 WHERE e.`employee_id` IS NULL;
```



### 右外
 查询哪个部门没有员工
```sql
SELECT d.*,e.employee_id
 FROM employees e
 RIGHT OUTER JOIN departments d
 ON d.`department_id` = e.`department_id`
 WHERE e.`employee_id` IS NULL;
```



### 全外

```sql
USE girls;
 SELECT b.*,bo.*
 FROM beauty b
 FULL OUTER JOIN boys bo
 ON b.`boyfriend_id` = bo.id;
```



## 交叉连接

```sql
SELECT b.*,bo.*
 FROM beauty b
 CROSS JOIN boys bo;
```




# 子查询

子查询出现的位置
select后面：仅仅支持标量（一列一行）子查询
from后面：支持表子查询
where或having后面：标量子查询、列子查询（一列多行）、行子查询（一行多列）
exists后面：表子查询（多列多行）




# 数据库的创建和删除


### 创建数据库


创建数据库的语法


```sql
CREATE DATABASE  database_name;
```


如果不确定要创建的数据库是否存在,可以先使用`创建时判断`或者`查看有哪些数据库`


```sql
-- 如果数据库不存在才创建
create database if not exists database_name;

-- 查看有那些数据库
show databases;
```


### 删除数据库


删除数据库的语法


```sql
drop database  database_name;
```


# 创建表


创建表的语法


```sql
CREATE TABLE  table_name（column_name column_type ...）;

-- 创建时判断表是否存在 if not exists
CREATE TABLE if not exists  table_name（column_name column_type ...）;
```



例 : 在这里，我们将在数据库“customers”中创建一个名为“cus_tbl”的表。


```sql
CREATE TABLE cus_tbl(
   cus_id INT NOT NULL AUTO_INCREMENT,
   cus_firstname VARCHAR(100) NOT NULL,
   cus_surname VARCHAR(100) NOT NULL,
   PRIMARY KEY ( cus_id )
);
```



### 查看已创建的表


```sql
show tables;
```



### 查看数据表的结构


```sql
describe table_name;
```


# 修改表


### 修改表名


```sql
ALTER TABLE  table_name
RENAME  TO  new_table_name;
```


### 添加字段


添加字段的语法


```sql
ALTER TABLE table_name
ADD new_column_name column_definition
[ FIRST | AFTER column_name ];  -- 在某列之前或之后
```


参数的含义 :


- **table_name：**指定要修改的表的名称。
- **new_column_name：**它指定要添加到表中的新列的名称。
- **column_definition：**它指定列的数据类型和定义（NULL或NOT NULL等）。
- **FIRST | AFTER column_name：**它是可选的。它告诉MySQL在表中创建列的位置。如果未指定此参数，则新列将添加到表的末尾。



添加多个字段


```sql
ALTER TABLE table_name
ADD new_column_name column_definition
[ FIRST | AFTER column_name ],
ADD new_column_name column_definition
[ FIRST | AFTER column_name ],
...
;
```


### 修改字段


`MODIFY` 修改某个字段的定义,比如说修改字段的`数据类型`和`约束`


```sql
ALTER TABLE  table_name
MODIFY  column_name column_definition
[  FIRST  | AFTER  column_name];
```


`CHANGE` 修改某个字段的`字段名`,和`数据类型`或`约束`


```sql
ALTER TABLE  table_name
CHANGE  COLUMN  old_name new_name
column_definition
[  FIRST  | AFTER  column_name]
```


### 删除字段


```sql
ALTER TABLE  table_name
DROP COLUMN  column_name;
```


# 删除表


### 删除表中所有的数据


删除全部数据的两种方式


1. DELETE
1. TRUNCATE



两个删除的区别 : delete是删除表中的记录 , truncate是删除表然后在创建表


```sql
TRUNCATE TABLE table_name;

-- 或者
delete TABLE table_name
```


### 删除表


```sql
DROP TABLE   table_name;
```


# 插入数据


### 插入一条数据


```sql
-- 指定字段插入
INSERT INTO  table_name（field1，field2，... fieldN）
VALUES
（value1，value2，... valueN）;

-- 全字段插入
INSERT INTO  table_name  VALUES  （value1，value2，... valueN）;
```


### 插入多条记录


```sql
INSERT INTO  cus_tbl
（cus_id，cus_firstname，cus_surname）
VALUES
（5，  'Ajeet' ，  'Maurya' ），
（6，  'Deepika' ，  'Chopra' ），
（7，  'Vimal' ，  'Jaiswal' ）;
```


# 更新数据


UPDATE语句用于更新数据库中MySQL表的数据。


```sql
UPDATE table_name SET field1=new-value1, field2=new-value2
[WHERE Clause]
```


**注意：**


- 可以完全更新一个或多个字段。
- 可以使用WHERE子句指定任何条件。
- 您可以一次更新单个表中的值。
- WHERE子句用于更新表中的选定行。



# 删除数据


删除指定数据-行


```sql
DELETE FROM table_name
WHERE
(Condition specified);
```


# MySQL的约束
约束是用来限定表中数据准确性、完整性、一致性、联动性的一套规则。在Mysql中，约束保存在`information_schema`数据库的`table_constraints`中，可以通过该表查询约束信息。
MySQL的约束种类 :

1. 非空约束(not null)

1. 唯一性约束(unique)

1. 主键约束(primary key) PK

1. 外键约束(foreign key) FK

1. 检查约束(目前MySQL不支持、Oracle支持)

## not null
**创建**NOT NULL约束
```sql
CREATE TABLE emp(
id INT(10) NOT NULL,
NAME VARCHAR(20) NOT NULL DEFAULT 'abc',
sex CHAR NULL
);
```


**增加**NOT NULL约束
```sql
ALTER TABLE emp
MODIFY sex VARCHAR(30) NOT NULL;
```


取消NOT NULL约束
```sql
ALTER TABLE emp
MODIFY sex VARCHAR(30) NULL;
```


取消 not null 约束，增加默认值
```sql
ALTER TABLE emp
MODIFY NAME VARCHAR(15) DEFAULT 'abc' NULL;
```
## UNIQUE
同一个表可以有多个唯一约束，多个列组合的约束。 在创建唯一约束的时候，如果不给唯一约束名称，就 默认和列名相同。
MySQL会给唯一约束的列上默认创建一个唯一索引


使用表级约束语法
```sql
CREATE TABLE USER(
id INT NOT NULL,
NAME VARCHAR(25),
PASSWORD VARCHAR(16),
#使用表级约束语法
CONSTRAINT uk_name_pwd UNIQUE(NAME,PASSWORD)
);
```


添加唯一约束
```sql
#方式一
ALTER TABLE USER
ADD UNIQUE(NAME,PASSWORD);

#方式二
ALTER TABLE USER
ADD CONSTRAINT uk_name_pwd UNIQUE(NAME,PASSWORD);

#方式三
ALTER TABLE USER
MODIFY NAME VARCHAR(20) UNIQUE;
```


删除唯一约束
```sql
ALTER TABLE USER
DROP INDEX uk_name_pwd;
```


## PRIMARY KEY

1. 主键约束相当于唯一约束+非空约束的组合，主 键约束列不允许重复，也不允许出现空值
1. 如果是多列组合的主键约束，那么这些列都不允 许为空值，并且组合的值不允许重复。
1. 每个表最多只允许一个主键，建立主键约束可以 在列级别创建，也可以在表级别上创建。
1. MySQL的主键名总是PRIMARY，当创建主键约束 时，系统默认会在所在的列和列组合上建立对应的 唯一索引。



创建主键约束
表级模式
```sql
CREATE TABLE emp5(
id INT NOT NULL AUTO_INCREMENT,
NAME VARCHAR(20),
pwd VARCHAR(15),
CONSTRAINT emp5_id_pk PRIMARY KEY(id)
);
```
列级模式
```sql
CREATE TABLE emp4(
id INT AUTO_INCREMENT PRIMARY KEY,
NAME VARCHAR(20)
);
```
组合模式
```sql
CREATE TABLE emp6(
id INT NOT NULL,
NAME VARCHAR(20),
pwd VARCHAR(15),
CONSTRAINT emp7_pk PRIMARY KEY(NAME,pwd)
);
```


添加主键约束
```sql
ALTER TABLE emp5
ADD PRIMARY KEY(NAME,pwd);
```


修改主键约束
```sql
ALTER TABLE emp5
MODIFY id INT PRIMARY KEY;
```


删除主键约束
```sql
ALTER TABLE emp5
DROP PRIMARY KEY;
```
        
