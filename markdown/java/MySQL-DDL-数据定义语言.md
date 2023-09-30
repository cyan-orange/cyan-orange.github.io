# 查询数据库
```sql
# 显示当前mysql中的数据库列表
show databases;

# 显示指定名称的数据的创建的SQL指令
show create database <dbName>;

# 切换数据库
use <dbName>
```

# 创建数据库
```sql
# 创建数据库 dbName表示创建的数据库名称，可以⾃定义
create database <dbName>;

## 创建数据库，当指定名称的数据库不存在时执⾏创建
create database if not exists <dbName>;

## 在创建数据库的同时指定数据库的字符集（字符集：数据存储在数据库中采⽤的编码格式utf8 gbk）
create database <dbName> character set utf8;
```

# 修改数据库
```sql
# 修改数据库的字符集
alter database <dbName> character set utf8md4;
```

# 删除数据库
```sql
# 删除数据库
drop database <dbName>;

## 如果数据库存在则删除数据库
drop database is exists <dbName>;
```

# 创建数据表

```sql
# 如果表不存在就创建
CREATE TABLE if not exists `test` (
    `id` BIGINT NOT NULL COMMENT 'id',
    `username` VARCHAR(100) NOT NULL COMMENT '用户名',
    `age` TINYINT not null COMMENT '年龄',
    `gender` TINYINT(1) DEFAULT 0 COMMENT '性别：0-男，1-女',
    `deleted` TINYINT(1) DEFAULT 0 COMMENT '0-未删除，1-已删除',
    PRIMARY KEY (`id`)
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '测试表';
```

# 查看数据表
```sql
# 查看数据库中有那些表
show tables;

# 查看表的结构
desc <tableName>

# 查看数据表的创建源码
show create table <tableName>;
```

# 删除表
```sql
# 删除数据表
drop table <tableName>;

## 当数据表存在时删除数据表
drop table if exists <tableName>;
```

# 修改表
修改表名
```sql
alter table <tableName> rename to <newTableName>;
```

数据表也是有字符集的，默认字符集和数据库⼀致
```sql
alter table <tableName> character set utf8;
```

## 添加字段
例子：在年龄字段后面添加性别字段
```sql
ALTER Table student add `gender` TINYINT(1) DEFAULT 0 COMMENT '性别：0-男，1-女' after age;
```

## 修改字段的类型
```sql
alter table <tableName> modify <columnName> <newType>;
```

## 修改字段的名字和类型
```sql
alter table <tableName> change <oldColumnName> <newCloumnName> <type>;
```

## 删除字段
```sql
alter table <tableName> drop <columnName>;
```
        
