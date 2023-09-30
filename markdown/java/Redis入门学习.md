# Redis是什么
Redis是由意大利人Salvatore Sanfilippo（网名：antirez）开发的一款内存高速缓存数据库。Redis全称为：Remote Dictionary Server（远程数据服务），该软件使用C语言编写，Redis是一个key-value存储系统，它支持丰富的数据类型，如：string、list、set、zset(sorted set)、hash。

# Redis的特点
Redis以内存作为数据存储介质，所以读写数据的效率极高，远远超过数据库。以设置和获取一个256字节字符串为例，它的读取速度可高达110000次/s，写速度高达81000次/s。

Redis跟memcache不同的是，储存在Redis中的数据是持久化的，断电或重启后，数据也不会丢失。因为Redis的存储分为内存存储、磁盘存储和log文件三部分，重启后，Redis可以从磁盘重新将数据加载到内存中，这些可以通过配置文件对其进行配置，正因为这样，Redis才能实现持久化。

# 安装Redis
1. 去官网下载[redis源文件 ](https://redis.io/download) ,上传到Linux服务器上 , 解压到安装目录
2. 进入到安装目录执行`make`命令编译源文件
3. 执行命令`make install` 安装配置redis环境变量

# 启动Redis
前台启动方式


```bash
redis-server
```


后台启动方式


```bash
redis-server &
```


查看redis进程 `ps -ef | grep redis`


```bash
[root@lemon ~]# ps -ef | grep redis
root      11719   7346  0 19:47 pts/0    00:00:00 redis-server *:6379
root      11724   7346  0 19:48 pts/0    00:00:00 grep --color=auto redis
```


使用redis的命令行客户端连接redis服务器`redis-cli`


```bash
[root@lemon ~]# redis-cli
127.0.0.1:6379>
```

# 关闭Redis

关闭方式一 : 使用redis客户端向服务器发送命令关闭 (推荐使用)
```bash
redis-cli shutdown
```

关闭方式二 : 先用 命令`ps -ef | grep redis`查出进程号, 再用 `kill pid`关闭
```bash
[root@lemon ~]# ps -ef | grep redis
root      11798   7346  0 20:06 pts/0    00:00:00 redis-server *:6379
root      11803   7346  0 20:06 pts/0    00:00:00 grep --color=auto redis
[root@lemon ~]# kill 11798
[root@lemon ~]# 11798:signal-handler (1560082112) Received SIGTERM scheduling shutdown...
11798:M 09 Jun 2019 20:08:32.240 # User requested shutdown...
11798:M 09 Jun 2019 20:08:32.240 * Saving the final RDB snapshot before exiting.
11798:M 09 Jun 2019 20:08:32.241 * DB saved on disk
11798:M 09 Jun 2019 20:08:32.241 # Redis is now ready to exit, bye bye...
```

# Redis的数据类型

**字符串String**
字符串类型是redis 中最基本的数据类型 ,  它能存储任何形式的字符串 , 包括二进制数据, 序列化后的数据 , JSON化的对象甚至是一张图片 ,  最大512M

**哈希hash**
redis hash 是一个String类型的field 和 value 的映射表 , hash特别适合用于存储对象.

**列表list**
Redis 列表是简单的字符串列表 , 按照插入的顺序排序 ,  你可以添加一个元素到列表的头部(左边) 或者尾部 (右边)

**集合set**
Redis 的set 是String类型的无序集合 , 集合成员是唯一的, 即集合中不能出现重复的数据

**有序集合zset**
redis 有序集合zset 和集合 set 一样也是String类型元素的集合, 且不允许重复的成员 .  不同的是 zset 的每个元素都会关联一个分数 ( 分数可以重复) , redis 通过分数来为集合中的成员进行从小到大的排序 .

# String的常用命令

## SET

SET key value [EX seconds] [PX milliseconds] [NX|XX]

将字符串值 value 关联到 key 。

如果 key 已经持有其他值， SET 就覆写旧值， 无视类型。

当 SET 命令对一个带有生存时间（TTL）的键进行设置之后， 该键原有的 TTL 将被清除。

**可选参数**
从 Redis 2.6.12 版本开始， SET 命令的行为可以通过一系列参数来修改：

`EX seconds` ： 将键的过期时间设置为 seconds 秒。 执行 SET key value EX seconds 的效果等同于执行 SETEX key seconds value 。

`PX milliseconds` ： 将键的过期时间设置为 milliseconds 毫秒。 执行 SET key value PX milliseconds 的效果等同于执行 PSETEX key milliseconds value 。

`NX` ： 只在键不存在时， 才对键进行设置操作。 执行 SET key value NX 的效果等同于执行 SETNX key value 。

`XX` ： 只在键已经存在时， 才对键进行设置操作。

>注意
>因为 SET 命令可以通过参数来实现 SETNX 、 SETEX 以及 PSETEX 命令的效果， 所以 Redis 将来的版本可能会移除并废弃 SETNX 、 SETEX 和 PSETEX 这三个命令。



**返回值**
在 Redis 2.6.12 版本以前， SET 命令总是返回 OK 。

从 Redis 2.6.12 版本开始， SET 命令只在设置操作成功完成时才返回 OK ； 如果命令使用了 NX 或者 XX 选项， 但是因为条件没达到而造成设置操作未执行， 那么命令将返回空批量回复（NULL Bulk Reply）。

**代码示例**

使用 EX 选项：
```bash
redis> SET key-with-expire-time "hello" EX 10086
OK

redis> GET key-with-expire-time
"hello"

redis> TTL key-with-expire-time
(integer) 10069
```

使用 PX 选项：
```bash
redis> SET key-with-pexpire-time "moto" PX 123321
OK

redis> GET key-with-pexpire-time
"moto"

redis> PTTL key-with-pexpire-time
(integer) 111939
```

使用 NX 选项：
```bash
redis> SET not-exists-key "value" NX
OK      # 键不存在，设置成功

redis> GET not-exists-key
"value"

redis> SET not-exists-key "new-value" NX
(nil)   # 键已经存在，设置失败

redis> GEt not-exists-key
"value" # 维持原值不变
```

使用 XX 选项：
```bash
redis> EXISTS exists-key
(integer) 0

redis> SET exists-key "value" XX
(nil)   # 因为键不存在，设置失败

redis> SET exists-key "value"
OK      # 先给键设置一个值

redis> SET exists-key "new-value" XX
OK      # 设置新值成功

redis> GET exists-key
"new-value"
```

## GET

GET key

返回与键 key 相关联的字符串值。

**返回值**
如果键 key 不存在， 那么返回特殊值 nil ； 否则， 返回键 key 的值。

如果键 key 的值并非字符串类型， 那么返回一个错误， 因为 GET 命令只能用于字符串值。

**代码示例**
对不存在的键 key 或是字符串类型的键 key 执行 GET 命令：
```bash
redis> GET db
(nil)

redis> SET db redis
OK

redis> GET db
"redis"
```


对不是字符串类型的键 key 执行 GET 命令：
```bash
redis> DEL db
(integer) 1

redis> LPUSH db redis mongodb mysql
(integer) 3

redis> GET db
(error) ERR Operation against a key holding the wrong kind of value
```

# hash的常用命令

## HSET

HSET hash field value

将哈希表 hash 中域 field 的值设置为 value 。

如果给定的哈希表并不存在， 那么一个新的哈希表将被创建并执行 HSET 操作。

如果域 field 已经存在于哈希表中， 那么它的旧值将被新值 value 覆盖。

**返回值**
当 HSET 命令在哈希表中新创建 field 域并成功为它设置值时， 命令返回 1 ； 如果域 field 已经存在于哈希表， 并且 HSET 命令成功使用新值覆盖了它的旧值， 那么命令返回 0 。

**代码示例**
设置一个新域：
```bash
redis> HSET website google "www.g.cn"
(integer) 1

redis> HGET website google
"www.g.cn"
```

对一个已存在的域进行更新：
```bash
redis> HSET website google "www.google.com"
(integer) 0

redis> HGET website google
"www.google.com"
```

## HGET

HGET hash field

返回哈希表中给定域的值。

**返回值**
HGET 命令在默认情况下返回给定域的值。

如果给定域不存在于哈希表中， 又或者给定的哈希表并不存在， 那么命令返回 nil 。

**代码示例**
域存在的情况：
```bash
redis> HSET homepage redis redis.com
(integer) 1

redis> HGET homepage redis
"redis.com"
```

域不存在的情况：
```bash
redis> HGET site mysql
(nil)
```

## HMSET

HMSET key field value [field value …]

同时将多个 field-value (域-值)对设置到哈希表 key 中。

此命令会覆盖哈希表中已存在的域。

如果 key 不存在，一个空哈希表被创建并执行 HMSET 操作。

**返回值**
如果命令执行成功，返回 OK 。
当 key 不是哈希表(hash)类型时，返回一个错误。
```bash
redis> HMSET website google www.google.com yahoo www.yahoo.com
OK

redis> HGET website google
"www.google.com"

redis> HGET website yahoo
"www.yahoo.com"
```

## HMGET

HMGET key field [field …]

返回哈希表 key 中，一个或多个给定域的值。

如果给定的域不存在于哈希表，那么返回一个 nil 值。

因为不存在的 key 被当作一个空哈希表来处理，所以对一个不存在的 key 进行 HMGET 操作将返回一个只带有 nil 值的表。


**返回值**
一个包含多个给定域的关联值的表，表值的排列顺序和给定域参数的请求顺序一样。

```bash
redis> HMSET pet dog "doudou" cat "nounou"    # 一次设置多个域
OK

redis> HMGET pet dog cat fake_pet             # 返回值的顺序和传入参数的顺序一样
1) "doudou"
2) "nounou"
3) (nil)
```


## HGETALL

HGETALL key

返回哈希表 key 中，所有的域和值。

在返回值里，紧跟每个域名(field name)之后是域的值(value)，所以返回值的长度是哈希表大小的两倍。


**返回值**
以列表形式返回哈希表的域和域的值。
若 key 不存在，返回空列表。
```bash
redis> HSET people jack "Jack Sparrow"
(integer) 1

redis> HSET people gump "Forrest Gump"
(integer) 1

redis> HGETALL people
1) "jack"          # 域
2) "Jack Sparrow"  # 值
3) "gump"
4) "Forrest Gump"
```

## HDEL

HDEL key field [field …]

删除哈希表 key 中的一个或多个指定域，不存在的域将被忽略。


**返回值:**
被成功移除的域的数量，不包括被忽略的域。
```
# 测试数据

redis> HGETALL abbr
1) "a"
2) "apple"
3) "b"
4) "banana"
5) "c"
6) "cat"
7) "d"
8) "dog"


# 删除单个域

redis> HDEL abbr a
(integer) 1


# 删除不存在的域

redis> HDEL abbr not-exists-field
(integer) 0


# 删除多个域

redis> HDEL abbr b c
(integer) 2

redis> HGETALL abbr
1) "d"
2) "dog"
```


# list常用命令


## lpush

语法 : lpush key value [value ...]


作用: 将一个或多个值 value 插入到列表 key 的表头(最左边) , 从左边开始加入值,从左到右的顺序依次插入到表头


返回值 : 数字,新列表的长度


rpush 和 lpush 相对应


## lrange

语法 : lrange key start stop


作用 : 获取列表 key 中指定区间内的元素 , 0 表示列表的第一个元素, 以 1 表示列表的第二个元素; start, stop 是列表的下标值, 也可以负数的下标, -1表示列表的最后一个元素 ,-2 表示列表的倒数第二个元素, 以此类推 . start, stop 超出列表的范围不会出现错误.


返回值 : 指定区间的列表


## lindex

语法 : lindex key index

作用: 获取列表 key 中下标为指定 index 的元素 , 列表元素不删除, 只是查询, 0表示列表的第一个元素,  -1表示列表的最后一个元素

返回值 : 指定下标的元素 ; index不在列表范围, 返回nil


## llen

语法 : llen key

作用 : 获取列表 key 的长度

返回值: 数值, 列表的长度; key 不存在返回 0

## lrem

语法 : lrem key count value

作用 : 根据参数 count 的值 , 移除 列表中与参数 value相等的元素. count>0 , 从列表的左侧向右开始移除; count < 0 从列表的尾部开始移除; count=0 移除表中所有与value 相等的值


## lset

语法 : lset key index value

作用 : 将列表key 下标为 index 的元素的值设置为value

返回值 : 设置成功返回 ok , key不存在或者 index 超出范围返回错误信息


## linsert

语法 : linsert key Before|Alfter pivot value

作用 : 将值 value 插入到列表 key 当中位于 pivot之前或之后的位置 . key 不存在, pivot不存在列表中, 不执行任何操作

返回值 : 命令执行成功, 返回新列表的长度. 没有找到pivot 返回 -1 , key不存在返回 0

# set常用命令

## sadd

语法 : sadd key member [member...]

作用 : 将一个或多个 member 元素加入到集合 key 当中 , 已经存在于集合的member元素将被忽略 ,不会再添加.

返回值 : 加入到集合的新元素的个数 . 不包括被忽略的元素.

## smembers

语法 : smembers key

作用 : 获取集合 key 中的所有成员元素, 不存在的 key 视为空集合

## sismember

语法 : sismember key member

作用 : 判断member 元素是否是集合 key 的成员

返回值 : member 是集合成员返回**1**, 其他返回 **0**

## scard

语法 : scard key

作用 : 获取集合里面的元素个数

返回值 : 数字, key 的元素个数 . 其他情况返回 0


## srem

语法 : srem key member [member...]

作用 : 删除集合 key 中的一个或多个 member 元素 , 不存在的元素被忽略 ;

返回值 : 数字,成功删除的元素个数 , 不包含忽略的元素

## srandmember

语法 : srandmember key [count]

作用 : 只提供key , 随机返回集合中一个元素 , 元素不删除,依然再集合中 ; 提供了count 整正数, 返回包含count 个数元素的集合,  集合元素各不相同 ; count 是负数 ,返回一个count 绝对值的长度的集合 ,集合中元素可能会重复多次

返回值 : 一个元素 , 多个元素的集合


## spop

语法 : spop key [count]

作用 : 随机从集合中删除一个元素, count 是删除元素的个数.

返回值 : 被删除的元素, key 不存在或空集合返回nil
        
