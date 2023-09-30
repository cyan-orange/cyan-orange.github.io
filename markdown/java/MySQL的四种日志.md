在MySQL中，有4种不同的日志，分别是错误日志、二进制日志（BINLOG日志）、查询日志和慢查询日志

# 错误日志

错误日志记录了MySQL在启动、停止、以及服务器在运行过程中发生任何严重错误的相关信息。

该日志是默认开启的，查看错误日志的位置
```bash
mysql> show variables like 'log_error%';
+----------------------------+----------------------------------------+
| Variable_name              | Value                                  |
+----------------------------+----------------------------------------+
| log_error                  | .\XIEJINCHI.err                        |
| log_error_services         | log_filter_internal; log_sink_internal |
| log_error_suppression_list |                                        |
| log_error_verbosity        | 2                                      |
+----------------------------+----------------------------------------+
4 rows in set, 1 warning (0.06 sec)
```

# 二进制日志

二进制日志（BINLOG日志）记录了所有DDL（数据库定义语言）语句和DML（数据操纵语言）语句，但是不包括查询语句，此日志对于灾难时的数据恢复有非常重要的作用，MySQL的主从复制，就是通过该日志实现的

二进制日志默认情况下是没有开启的，需要到MySQL的配置文件中开启，并配置MySQL日志的格式

查看binlog日志是否开启
```
mysql> show variables like '%log_bin%';
+---------------------------------+-------+
| Variable_name                   | Value |
+---------------------------------+-------+
| log_bin                         | OFF   |
| log_bin_basename                |       |
| log_bin_index                   |       |
| log_bin_trust_function_creators | OFF   |
| log_bin_use_v1_row_events       | OFF   |
| sql_log_bin                     | ON    |
+---------------------------------+-------+
6 rows in set (0.00 sec) ``` 开启binlog，如果没有指定日志文件的路径，默认写入MySQL的数据目录 ``` #文件名 log-bin=mysql-bin #序列号 server-id=1 #日志格式 binlog_format=STATEMENT
```
在 MySQL 5.7.3 及以后版本,如果没有设置server-id, 那么设置binlog后无法开启MySQL服务


日志格式
**STATEMENT**
这个格式的日志文件中记录的都是SQL语句，每一条对数据进行修改的SQL都会记录在日志文件中，通过MySQL提供的mysqlbinlog工具，可以清晰的查看到每一条语句的文本，主从复制的时候，从库（slave）会将日志解析为原文本，并在从库重新执行一次

**ROW**
这个格式的日志文件记录的是每一行数据的变更，而不是SQL语句

**MIXED**
这个是目前MySQL默认的日志格式，混合了STATEMENT和ROW两种格式，默认情况下使用STATEMENT,但是在一些特殊情况下采用ROW来进行记录。MIXED格式能尽量利用两种模式的优点，而避开它们的缺点。

查看binlog日志
查看日志文件存放的位置
```
mysql> show variables like '%log_bin%';
+---------------------------------+--------------------------------+
| Variable_name                   | Value                          |
+---------------------------------+--------------------------------+
| log_bin                         | ON                             |
| log_bin_basename                | /var/lib/mysql/mysql-bin       |
| log_bin_index                   | /var/lib/mysql/mysql-bin.index |
| log_bin_trust_function_creators | OFF                            |
| log_bin_use_v1_row_events       | OFF                            |
| sql_log_bin                     | ON                             |
+---------------------------------+--------------------------------+
6 rows in set (0.00 sec)
```
mysql-bin.index：是日志的索引文件，记录日志的文件名
mysql-bin：是日志文件



查看binlog文件列表 `show binary logs;`

查看binlog文件内容 `show binlog events in 'mysql-bin.000001';`




binlog日志的删除
对于比较繁忙的系统，由于每天生成大量的日志，这些日志如果长时间不清除，就会占用大量的磁盘空间

删除方式一：通过 Reset Master 指令删除全部日志，日志编号重新开始
```
mysql> reset master;
Query OK, 0 rows affected (0.00 sec)
```

删除方式二：删除指定编号之前的日志文件，比如删除mysql-bin.000001之前的文件
```
mysql> purge master logs to 'mysql-bin.000001';
Query OK, 0 rows affected (0.00 sec)
```

删除方式三：删除某个时间点之前的日志
```
mysql> purge master logs before '2021-10-19 00:00:00 ';
Query OK, 0 rows affected, 1 warning (0.01 sec)
```

删除方式四：设置日志的过期时间，单位为天，到期自动删除日志
查看binlog的过期时间
```
mysql> show variables like "%expire_logs%";
+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| expire_logs_days | 0     |
+------------------+-------+
1 row in set (0.01 sec)
```
0 表示永不过期 修改MySQL配置文件，设置binlog过期时间，然后重启MySQL ``` expire_logs_days=15 #达到过期时间并不会立即删掉，binlog大小超过max_binlog_size才会删掉 max_binlog_size=500M
```


# 查询日志

查询日志中记录了客户端所有操作语句，包括select语句

查看查询日志是否开启，OFF表示未开启
```
mysql> show variables like "general_log%";
+------------------+---------------------------------+
| Variable_name    | Value                           |
+------------------+---------------------------------+
| general_log      | OFF                             |
| general_log_file | /var/lib/mysql/d6e04edbfb09.log |
+------------------+---------------------------------+
2 rows in set (0.00 sec) ``` 查询日志默认是未开启的，可以修改MySQL配置文件来开启 ``` #开启查询日志，1-开启，0-关闭 general-log=1 #设置日志的文件名，默认的文件名为host_name.log general_log_file=/var/log/mysql/general_log.log
```



# 慢查询日志 MySQL默认10s内没有响应SQL结果，则为慢查询 可以修改这个默认时间 慢查询日志默认是关闭的，修改MySQL配置文件，来开启慢查询日志 ``` #开启慢查询日志，0-关闭，1-开启 slow_query_log=1 #指定慢查询日志的文件名 slow_query_log_file=/var/log/mysql/slow_query.log #查询超过这个时间就记录为慢查询,单位是秒 long_query_time=3
```
        
