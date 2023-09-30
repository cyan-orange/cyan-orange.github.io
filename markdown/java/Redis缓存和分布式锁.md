

为了系统性能的提升，一般会将部分数据放入缓存中，加速访问。


# 使用redis产生内存溢出问题


使用redis作缓存，在压力测试中会产生堆外内存溢出异常


原因：spring boot2.0以后默认使用lettuce作为操作redis的客户端。它使用netty进行网络通信。lettuce的bug导致netty的堆外内存溢出。


解决办法：将操作redis底层客户端的lettuce切换为jedis


```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
    <exclusions>
        <exclusion>
            <groupId>io.lettuce</groupId>
            <artifactId>lettuce-core</artifactId>
        </exclusion>
    </exclusions>
</dependency>

<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
</dependency>
```


# 缓存击穿、穿透、雪崩


高并发情况下缓存失效产生的问题


## 缓存穿透


查询一个一定不存在的数据，由于缓存中没有这个数据，然后就去数据库里面查，但是数据库也没有这个数据，并且没有将查询到的null写到缓存，导致了每次都要到数据库中去查


**风险**


利用不存在的数据进行攻击，数据库瞬时压力增大，最后导致崩溃


**解决方案**


把null结果缓存，加入短暂的缓存时间。


## 缓存雪崩


缓存雪崩指的是设置缓存时key使用的相同的过期时间，导致缓存在某一时刻同时失效，请求同时去查询数据库，数据库瞬时压力过大崩溃


**解决方案**


在原有的过期时间上增加一个随机值，比如1~5分钟，这样缓存的过期时间重复率就会降低


## 缓存击穿


如果一个key在大量的请求进来时正好失效，这些请求同时去访问数据库，这样被称为缓存击穿


**解决方案**


加锁，大量并发进来只让一个去查数据库 ，其他人等着，查到以后释放锁，其他人获取锁先查缓存就会有数据，不用去查数据库。


# redis+lua脚本做分布式锁


1. 保证加锁和设置锁的过期时间是一个原子操作，避免加锁后还没来得及设置锁的过期时间，系统就挂掉，然后变成死锁。
2. 保证业务代码在锁的有效期内执行完毕，避免业务还没完成锁就失效其他线程就进来。
3. 保证解锁的操作是一个原子操作：获取值，对比值，删除。需要使用lua脚本完成。



```java
public void getServiceLock() {
    //线程进来先去查缓存，直接返回

    //如果缓存没有，尝试占锁去查数据库
    String uuid = UUID.randomUUID().toString();
    //去redis占锁,占到锁并设置过期时间30s
    Boolean lock = redisTemplate.opsForValue().setIfAbsent("lock", uuid, 30, TimeUnit.SECONDS);
    //抢到锁
    if (lock) {

        try {
            //执行业务
        } finally {
            //解锁
            String script = "if redis.call('get',KEYS[1]) == ARGV[1] then return redis.call('del',KEYS[1]) else return 0 end";
            redisTemplate.execute(new DefaultRedisScript<Long>(script, Long.class), Arrays.asList("lock"), uuid);
        }
    } else {
        //100ms再次去获取锁，自旋
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        getServiceLock();
    }
}
```


# Redisson分布式锁


Redisson分布式锁文档 [https://github.com/redisson/redisson/wiki/1.-概述](https://github.com/redisson/redisson/wiki/1.-%E6%A6%82%E8%BF%B0)


加入redisson依赖


```xml
<dependency>
    <groupId>org.redisson</groupId>
    <artifactId>redisson</artifactId>
    <version>3.12.0</version>
</dependency>
```


配置redisson


```java
@Configuration
public class RedissonConfig {

    @Bean
    public RedissonClient redissonClient() {
        Config config = new Config();
        //单节点模式
        config.useSingleServer().setAddress("redis://127.0.0.1:6379");
        RedissonClient redisson = Redisson.create(config);
        return redisson;
    }
}
```


使用锁


```java
@Autowired
private RedissonClient redisson;

public void redissonLock() {
    RLock lock = redisson.getLock("lock");
    //加锁，一般指定锁的过期时间，秒
    lock.lock(30, TimeUnit.SECONDS);
    try {
        //执行业务代码
    } finally {
        lock.unlock();
    }
}
```
        
