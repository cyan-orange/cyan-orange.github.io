首先拉取MySQL5.7镜像
```
docker pull mysql:5.7
```

有了镜像之后， 就可以从镜像启动一个MySQL容器
`-p 3306:3306`：将容器的3306端口映射到主机的3306端口，左边是主机端口，右边是容器端口。
`--name：MySQL`：给容器取名为MySQL。
`-v /opt/mysql/log:/var/log/mysql`：将日志文件挂载到主机。
`-v /opt/mysql/data:/var/lib/mysql`：将数据文件挂载到主机。
`-v /opt/mysql/conf:/etc/mys`：将配置文件挂载到主机。
`-e MYSQL_ROOT_PASSWORD=orange`：初始化root账户密码。
`-d`： 后台启动。
```
docker run -p 3306:3306 --name mysql \
  -v /opt/mysql/log:/var/log/mysql \
  -v /opt/mysql/data:/var/lib/mysql \
  -v /opt/mysql/conf:/etc/mysql \
  -e MYSQL_ROOT_PASSWORD=orange \
  -d mysql:5.7 ``` 添加配置，在`/opt/mysql/conf`目录下创建MySQL配置文件`my.cnf`，并加入配置 ``` [client] port=3306 default-character-set=utf8 [mysql] default-character-set=utf8 default-storage-engine=INNODB [mysqld] init_connect='SET collation_connection=utf8_unicode_ci' init_connect='SET NAMES utf8' character-set-server=utf8 collation-server=utf8_unicode_ci
skip-character-set-client-handshake
skip-name-resolve
```

添加配置之后，重启MySQL容器
```
docker restart mysql
```
