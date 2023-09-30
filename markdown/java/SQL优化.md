# 复合索引

1. 必须要使用到最左边的索引列
2. 不能跳过中间的列


# 复合索引失效情况：

1. 使用范围查找会使后面的列索引失效
2. 使用字段运算会使本列索引和后面的索引都失效
3. 数据类型不正确，如果字段的类型是字符串，却给了一个数字，会使本列索引和后面的索引列都失效
4. 模糊查询使用`%`开头会使本列索引和后面的索引列都失效


# or 条件使索引失效情况

如果or连接的查询条件中某一边没有使用索引，索引全都会失效

建议使用union来替换or


# NULL判断索引失效情况

当列中的NULL值比较多的时候，is null 使索引失效；is not null 走索引

当列中的NULL值比较少的时候，is not null 使索引失效；is null 走索引



# in 和 not in 索引失效情况

in 使用索引，not in 不使用索引


# 全表扫描更快的情况

当表中的数据比较少的时候，全表扫描的速度比较快，就会放弃使用索引。


# 覆盖索引
覆盖索引指的是select查询的列都是索引列


# order by优化

MySQL的两种排序方式：

一种是通过有序索引扫描返回有序的数据，叫做using index，效率高

另一种是通过对返回的数据进行排序，叫做using filesort，效率低

排序的时候尽量使用覆盖索引，如果不是覆盖索引，排序方式就using filesort

using filesort排序算法：
1. 两次扫描算法：MySQL4.1之前的排序方式。首先根据条件取出排序字段和行指针信息，然后在排序区 sort buffer 中排序，如果 buffer 不够，则在临时表 temporary table 中存储排序结果，完成排序之后，再根据行指针会表读取记录，该操作可能会导致大量随机I/O操作
2. 一次性取出满足条件的所有字段，然后在排序区 sort buffer 中进行排序后直接输出结果排序时内存开销比较大，但是排序效率比两次扫描算法高

MySQL通过比较系统变量 `max_length_for_sort_data` 的大小和Query语句取出的字段总大小，来判断使用什么排序算法，如果`max_length_for_sort_data` 比较大，那么使用一次扫描算法，否则使用两次扫描算法
可以适当提高 `sort_buffer_size` 和 `max_length_for_sort_data` 系统变量，来增大排序区的大小，提高排序的效率
```bash
mysql> show variables like 'sort_buffer_size';
+------------------+--------+
| Variable_name    | Value  |
+------------------+--------+
| sort_buffer_size | 262144 |
+------------------+--------+
1 row in set, 1 warning (0.00 sec)

mysql> show variables like 'max_length_for_sort_data';
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| max_length_for_sort_data | 4096  |
+--------------------------+-------+
1 row in set, 1 warning (0.00 sec)

mysql> set global sort_buffer_size=262144;
Query OK, 0 rows affected (0.10 sec)

mysql> set global max_length_for_sort_data=4096;
Query OK, 0 rows affected, 1 warning (0.00 sec)
```


多字段排序需要注意：
1. 当使用多个字段排序的时候，如果一个升序一个降序， 即使参与排序的列都有索引，排序方式都会是using filesort，效率低
2. 参与排序的字段顺序必须按照复合索引列的顺序，排序方式都会是using filesort


# group by优化

经常需要分组的字段可以考虑创建索引

在进行group by分组的时候，默认会对分组的列进行排序，没有索引的字段进行排序需要扫描数据文件，非常耗时。如果不想使用这个排序操作，可以在group by 后加上 order by null

```sql
select age,count(*) from user group by order by null;
```


# or 条件优化
如果 or 条件的有一边没有使用索引，索引都会失效

建议使用union来替换or条件


# limit 分页优化
当表中的数据量很大，分页查询后面的记录，速度就会特别慢，因为MySQL需要排序查询前面的记录，直到查询到需要的那一页，然后丢弃前面的记录，返回需要的那一页数据，查询排序的速度很慢

优化方式一：在主键上完成排序分页操作，然后根据主键关联查询其他列数据
```sql
SELECT * FROM user a , (SELECT id FROM user ORDER BY id LIMIT 2000000 ,10) b WHERE a.id=b.id; ``` 优化方式二：如果表中的id是连续自增的，根据查询的页数和查询的记录数可以算出查询的id的范围 比如说要查询第10页，查20条。id=(currentPage-1)pageSize+1=(10-1)*20=180

```sql
select * from `user` where id > 180 limit 10;
```


# 索引提示

如果表中的某列是单值索引列，同时也是复合索引中的最左索引列，在使用到这个列做条件查找时，数据库会选择使用该列其中的一个索引

如果想自己决定该列使用哪个索引，可以在where关键字前加 use index(indexName)
```sql
select * from user use index(idx_username) where username='青橙ee';
```

ignore index(indexName) 忽略某个索引
force index(indexName) 强制使用某个索引，即使全表扫描会更快


# MySQL查询缓存

开启MySQL的查询缓存，当执行完全相同的SQL语句时，MySQL服务器就会直接从缓存中读取结果，当数据被修改，之前的缓存就会失效，修改比较频繁的表不适合做查询缓存

MySQL的查询缓存功能在MySQL8.0被移除了，因为现在缓存更多是做在应用逻辑层或者使用一些NoSQL型数据库

## 查询缓存的配置参数

查看MySQL是否支持查询缓存
```bash
mysql> show variables like 'have_query_cache';
+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| have_query_cache | YES   |
+------------------+-------+
1 row in set (0.00 sec)
```

查看MySQL是否开启了查询缓存，OFF表示关闭，ON表示开启
```bash
mysql> show variables like 'query_cache_type';
+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| query_cache_type | OFF   |
+------------------+-------+
1 row in set (0.00 sec)
```

查看查询缓存的占用大小，单位时字节
```bash
mysql> show variables like 'query_cache_size';
+------------------+---------+
| Variable_name    | Value   |
+------------------+---------+
| query_cache_size | 1048576 |
+------------------+---------+
1 row in set (0.00 sec)
```

查看缓存的信息
Qcache_free_blocks：可用的内存块
Qcache_free_memory：可用的内存空间
Qcache_hits：查询缓存的命中次数
Qcache_inserts：添加到查询缓存的次数
Qcache_lowmem_prunes：内存空间不足，从缓存中移除数据的次数
Qcache_not_cached：未做缓存的次数
Qcache_total_blocks：查询缓存中的内存块总数
```bash
mysql> show status like 'qcache%';
+-------------------------+---------+
| Variable_name           | Value   |
+-------------------------+---------+
| Qcache_free_blocks      | 1       |
| Qcache_free_memory      | 1031832 |
| Qcache_hits             | 0       |
| Qcache_inserts          | 0       |
| Qcache_lowmem_prunes    | 0       |
| Qcache_not_cached       | 1       |
| Qcache_queries_in_cache | 0       |
| Qcache_total_blocks     | 1       |
+-------------------------+---------+
8 rows in set (0.00 sec)
```

## 开启查询缓存
MySQL的查询缓存默认时关闭的，需要手动配置参数`query_cache_type`开启查询缓存，这个参数的取值有三个
- OFF或0：查询缓存关闭
- ON或1：查询缓存开启
- DEMAND或2：查询缓存按需进行，显示指定SQL_CACHE的select的语句才会缓存 在MySQL的配置文件中加上如下配置，开启查询缓存 ``` query_cache_type=1
```
配置之后重启MySQL服务才可以 生效


查询缓存select选项：
- select SQL_CACHE * FROM USER：从缓存中获取结果，如果没有，就执行查询并缓存结果
- select SQL_NO_CACHE * FROM USER：不会从缓存中获取结果，查询的结果也不会缓存


## 查询缓存失效场景

1. SQL语句不一致的情况
2. 当查询语句有一些不确定时，不会缓存。如：`select * from user where update_time < now()`
3. 查询MySQL系统表的时候不会缓存
4. 当执行更新操作之后，查询缓存失效
