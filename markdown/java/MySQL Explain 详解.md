explain能解释mysql如何处理SQL语句，表的加载顺序，表是如何连接，以及索引使用情况。是SQL优化的重要工具

在 SQL 语句前加 Explain 关键字就可以查看 SQL 的执行计划。

```sql
mysql> explain select * from user;
+----+-------------+-------+------------+------+---------------+------+---------+------+---------+----------+-------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows    | filtered | Extra |
+----+-------------+-------+------------+------+---------------+------+---------+------+---------+----------+-------+
|  1 | SIMPLE      | user  | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 5302557 |   100.00 | NULL  |
+----+-------------+-------+------------+------+---------------+------+---------+------+---------+----------+-------+
1 row in set, 1 warning (0.00 sec)
```



各字段的含义：

| 字段         | 含义                                                         |
| ------------ | ------------------------------------------------------------ |
| id           | select查询的序号，一组数字，表示执行的select查询或操作表的顺序 |
| select_type  | 标识select的类型，常见的值有：`SIMPLE`(简单查询，不使用连接或子查询)、`PRIMARY`(主查询，外层的查询)、`UNION`(UNION中的第二个或者后面的查询语句)、`SUBQUERY`(子查询中的第一个select)等 |
| table        | 查询的表                                                     |
| type         | 表的连接类型，性能由高到低：`system`>`const`>`eq_ref`>`ref`>`ref_or_null`>`index_merge`>`index_subquery`>`range`>`index`>`all` |
| possible_key | 查询时可能用到的索引                                         |
| key          | 用到的索引                                                   |
| key_len      | 索引字段的长度                                               |
| rows         | 估计值，查询扫描的行数                                       |
| extra        | 额外的信息                                                   |



## id

SELECT识别符。这是SELECT查询序列号。查询序号即为sql语句执行的顺序。

1. id相同，执行顺序从上之下
2. id不同，执行顺序从大到小
3. id有相同的和不同的，遵守1、2规则



## select_type

| select_type  | 含义                                                         |
| ------------ | ------------------------------------------------------------ |
| SIMPLE       | 简单的select查询，查询中不包含子查询或者UNION                |
| PRIMARY      | 若包含复杂的子查询，最外层查询标记为PRIMARY                  |
| SUBQUERY     | 在select或where列表中包含子查询                              |
| DERIVED      | 在from列表中包含的子查询，被标记为DERIVED(衍生)，临时表      |
| UNION        | 若在第二个select出现在union之后，则被标记为union；若union包含在from子句的子查询中，外层select被标记为DERIVED |
| UNION RESULT | 从union结果中获取结果的select                                |



## table

表示查询涉及的表或衍生表



## type

`type`  字段比较重要, 它提供了判断查询是否高效的重要依据依据. 通过 `type` 字段, 我们判断此次查询是 `全表扫描` 还是 `索引扫描` 等.

type 常用的取值有：

| type   | 含义                                                         |
| ------ | ------------------------------------------------------------ |
| system | 表中只有一条数据. 这个类型是特殊的 `const` 类型.             |
| const  | 针对主键或唯一索引的等值查询扫描, 最多只返回一行数据. const 查询速度非常快, 因为它仅仅读取一次即可。 |
| eq_ref | 此类型通常出现在多表的 join 查询, 表示对于前表的每一个结果, 都只能匹配到后表的一行结果。<br/>并且查询的比较操作通常是 `=`, 查询效率较高。 |
| ref    | 此类型通常出现在多表的 join 查询, 针对于非唯一或非主键索引, 或者是使用了 `最左前缀` 规则索引的查询。 |
| range  | 表示使用索引范围查询, 通过索引字段范围获取表中部分数据记录. 这个类型通常出现在 =, <>, >, >=, <, <=, IS NULL, <=>, BETWEEN, IN() 操作中. |
| index  | 表示全索引扫描                                               |
| ALL    | 表示全表扫描, 这个类型的查询是性能最差的查询之一             |



性能由高到低：`system`>`const`>`eq_ref`>`ref`>`ref_or_null`>`index_merge`>`index_subquery`>`range`>`index`>`all`



## possible_keys

`possible_keys` 表示 MySQL 在查询时, 能够使用到的索引. 注意, 即使有些索引在 `possible_keys` 中出现, 但是并不表示此索引会真正地被 MySQL 使用到. MySQL 在查询时具体使用了哪些索引, 由 `key` 字段决定.



## key

此字段是 MySQL 在当前查询时所真正使用到的索引.



## key_len

表示查询优化器使用了索引的字节数. 这个字段可以评估组合索引是否完全被使用, 或只有最左部分字段被使用到.
key_len 的计算规则如下:

字段的NULL 属性 占用1个字节， 如果一个字段是 NOT NULL 的，则没有此属性。

不定长字符串 varchar 需要1个字节来保存字符串的长度，

字符串字节长度还和字符编码有关系，gbk下一个字符占2个字节，utf8下一个字符占3个字节，utf8mb4下一个字符占4字节

字符串

- char(n) null： utf8下字节长度：`n*3+1`；utf8mb4下字节长度：`n*4+1`
- char(n) not null： utf8下字节长度：`n*3`；utf8mb4下字节长度：`n*4`
- varchar(n) null：utf8下字节长度：`n*3+1+1`；utf8mb4下字节长度：`n*4+1+1`
- varchar(n) not null：utf8下字节长度：`n*3+1`；utf8mb4下字节长度：`n*4+1`

数值类型:

- TINYINT: 1字节
- SMALLINT: 2字节
- MEDIUMINT: 3字节
- INT: 4字节
- BIGINT: 8字节

时间类型
- DATE: 3字节
- TIMESTAMP: 4字节
- DATETIME: 8字节





## rows

rows 也是一个重要的字段. MySQL 查询优化器根据统计信息, 估算 SQL 要查找到结果集需要扫描读取的数据行数.
这个值非常直观显示 SQL 的效率好坏, 原则上 rows 越少越好.



## Extra

EXplain 中的很多额外的信息会在 Extra 字段显示, 常见的有以下几种内容:

| select_type     | 含义                                                         |
| --------------- | ------------------------------------------------------------ |
| Using filesort  | 表示 MySQL 需额外的排序操作, 不能通过索引顺序达到排序效果. 一般有 `Using filesort`, 都建议优化去掉, 因为这样的查询 CPU 资源消耗大. |
| Using temporary | 查询有使用临时表保存中间结果, MySQL在对查询结果排序的时候使用临时表，一般出现于order by和group by，查询效率不高, 建议优化 |
| Using index     | 覆盖索引扫描, 表示查询在索引树中就可查找所需数据, 不用扫描表数据文件，性能不错 |
        
