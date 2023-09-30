# image镜像操作

搜索可用的镜像，在DockerHub上搜索比较方便
```bash
docker search Nginx
```

拉取镜像，如果不指定版本号，拉取的就是最新版的镜像
```bash
docker pull 镜像名:版本号
```

列出本地镜像
```bash
docker images
```

删除镜像
```bash
docker rmi hello-world
```

# 容器操作

**启动容器**
有了镜像之后， 就可以从镜像启动容器，例如启动一个MySQL容器
`-p 3306:3306`：将容器的3306端口映射到主机的3306端口，左边是主机端口，右边是容器端口。
`--name：MySQL`：给容器取名为MySQL。
`-v /opt/mysql/log:/var/log/mysql`：将日志文件挂载到主机。
`-v /opt/mysql/data:/var/lib/mysql`：将数据文件挂载到主机。
`-v /opt/mysql/conf:/etc/mys`：将配置文件挂载到主机。
`-e MYSQL_ROOT_PASSWORD=orange`：初始化root账户密码。
`-d`： 后台启动。
```bash
docker run -p 3306:3306 --name mysql \
  -v /opt/mysql/log:/var/log/mysql \
  -v /opt/mysql/data:/var/lib/mysql \
  -v /opt/mysql/conf:/etc/mysql \
  -e MYSQL_ROOT_PASSWORD=orange \
  -d mysql:5.7
```

**查看容器**
不加-a选项默认查看启动的容器，加-a选项查看所有容器
```bash
docker ps -a
```

**停止容器**
```bash
docker stop my-nginx
```

**启动已存在的容器**
```bash
docker start my-nginx
```

**删除容器**
可以按照容器id或者容器name删除，可以加-f选项删除正在运行的容器
```bash
docker rm my-tomcat
```

**进入容器**
以交互式的方式进入容器，可以修改容器中的配置等，退出容器命令`exit`
`-i`: 交互式操作。
`-t`: 终端。
`nginx`: nginx容器。
`/bin/bash`：放在镜像名后的是命令，这里我们希望有个交互式 Shell，因此用的是 /bin/bash
```bash
docker exec -it nginx /bin/bash
```

**拷贝容器中的文件到主机**

```bash
docker cp nginx:/etc/nginx/ /opt/nginx/
```
        
