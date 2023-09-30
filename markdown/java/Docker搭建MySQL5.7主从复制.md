MySQL复制是指将主数据库的DDL和DML操作通过binlog日志传到从库服务器中，然后在从库上对这些日志从新执行，从而达到从库和主库的数据保持同步

MySQL支持一台主库同时向多台从库进行复制，从库同时也可以作为其他从服务器的主库，实现链状复制

主从复制流程
1. Master 主库在事务提交时，会把数据变更作为时间Events记录在binglog日志中
2. Master推送binlog中的日志事件到Slave的中继日志Relay Log
3. Slave重做Relay log中的事件，从而达到复制的效果

主从复制至少需要一主一从两个MySQL服务器节点
Master 192.168.232.133
Slave 192.168.232.134 配置Master 在MySQL主节点的配置文件中添加如下配置，然后重启MySQL服务 ``` #在集群中需要是唯一的 server-id=1

#binglog日志 log-bin=mysql-bin
```

Master创建同步数据的账户，并给予权限
用户名：orange，密码：orange123，权限是所有库所有表

```
mysql> grant replication slave on *.* 'orange'@'192.168.232.134' identified by 'orange123';
```

创建用户和给用户授权也可以分开写
```
mysql> CREATE USER 'orange'@'192.168.232.134' IDENTIFIED BY 'orange123';

mysql> GRANT REPLICATION SLAVE ON *.* TO 'orange'@'192.168.232.134';
```

刷新权限列表
```
mysql> flush privileges;
```

查看主节点状态，主要查看File字段和Position字段的值，下面配置slave时会用到

```
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000001 |      771 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec) ``` 配置Slave 在MySQL的Slave节点的配置文件中添加如下配置，然后重启服务 ``` #MySQL服务端id，需要是集群中唯一的 server-id=2 #binlog文件名 log-bin=mysql-bin #是否只读：1-只读，0-读写，但是特权用户还是可以读写 read-only=1 #不需要同步的数据库 binlog-ignore-db=mysql
```

在Slave节点配置主从通信
```
change master to \ master_host='192.168.232.133',\ master_user='orange',\ master_password='orange123',\ master_log_file='mysql-bin.000001',\ master_log_pos=771; ``` 其中`master_log_file='mysql-bin.000001'`和`master_log_pos=771`的值就是刚才查看master节点状态信息中的值


启动从服务器复制线程

```
mysql> start slave;
```

查看复制状态

```
mysql> show slave status\G;
```
`Slave_IO_State` Slave的当前状态
`Slave_IO_Running： Yes`：读取主程序二进制日志的I/O线程是否正在运行
`Slave_SQL_Running： Yes`：执行读取主服务器中二进制日志事件的SQL线程是否正在运行。
`Seconds_Behind_Master `：是否为0，0就是已经同步了


其中`Slave_IO_Running`和`Slave_SQL_Running`的值必须是yes


需要停止复制可以关闭slave的复制线程

```
mysql> stop slave;
```
