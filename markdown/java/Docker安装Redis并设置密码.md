首先在`/opt`下创建`redis`目录，用于存放redis的数据和配置文件
```bash
mkdir /opt/redis

cd /opt/redis
```
创建redis的配置文件，并写入配置`vim /opt/redis/redis.conf`
```bash
#是否持久化
appendonly yes

#设置密码
requirepass orange
```

拉取镜像，默认的版本是latest最新版，可以使用 `docker pull redis:version`指定版本
```bash
docker pull redis
```
启动Redis容器，`redis-server /etc/redis/redis.conf`是指定使用配置文件启动，默认不使用配置文件
```bash
docker run -p 6379:6379 \
	-d --name redis \
	-v /opt/redis/data:/data \
	-v /opt/redis/redis.conf:/etc/redis/redis.conf \
	redis:latest \
	redis-server /etc/redis/redis.conf
```
        
