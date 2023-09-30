MySQL的分页查询语句为：
```SQL
select table from column limit start pageSize; ``` `start`：偏移量 `currentPage`：当前页 `PageSize`：每页记录数 分页查询的公式：start=(currentPage-1)PageSize
```sql
select colum... from tableName limit (currentPage-1)pageSize PageSize ``` 当表中的数据量很大，分页查询后面的记录，速度就会特别慢，因为MySQL需要排序查询前面的记录，直到查询到需要的那一页，然后丢弃前面的记录，返回需要的那一页数据，查询排序的速度很慢 优化一：如果表中的id是连续自增的，根据查询的页数和查询的记录数可以算出查询的id的范围 比如说要查询第10页，查20条。id=(currentPage-1)pageSize=(10-1)*20+1=180
```sql
SELECT * FROM `user` WHERE `id`  between 180 and 20;
#或
select * from `user` where id > 180 limit 20;
```


优化二：如果表中的id不是自增，在主键上完成排序分页操作，然后根据主键关联查询其他列数据
```sql
SELECT * FROM user a , (SELECT id FROM user ORDER BY id LIMIT 2000000 ,10) b WHERE a.id=b.id;
```
        
