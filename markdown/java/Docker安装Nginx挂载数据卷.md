1. 首先启动一个Nginx容器
```bash
docker run --name my-nginx -p 8080:8080 -d nginx
```

2. 进入容器
```bash
docker exec -it my-nginx bash
```

3. 查看Nginx的html、配置和日志目录
- `/etc/nginx`：配置文件的目录
- `/usr/share/nginx/html`：html目录
- `/var/log/nginx`：日志目录
```bash
root@33aab93c60f7:/# find / -name nginx
/etc/default/nginx
/etc/init.d/nginx
/etc/logrotate.d/nginx
/etc/nginx
find: '/proc/1/map_files': Operation not permitted
find: '/proc/31/map_files': Operation not permitted
find: '/proc/32/map_files': Operation not permitted
find: '/proc/38/map_files': Operation not permitted
/usr/lib/nginx
/usr/sbin/nginx
/usr/share/doc/nginx
/usr/share/nginx
/var/cache/nginx
/var/log/nginx
```

4. `exit`退出容器，在/opt下创建nginx目录用来存放html、配置和日志目录
```bash
mkdir /opt/nginx
```

5. 拷贝容器中nginx的配置目录到/opt/nginx，并改名为conf
```bash
docker cp my-nginx:/etc/nginx /opt/nginx

mv /opt/nginx/nginx /opt/nginx/conf
```

6. 删除容器
```bash
docker rm -f my-nginx
```

7. 启动nginx容器并挂载目录
```bash
docker run -p 80:80 --name nginx \
	-v /opt/nginx/conf:/etc/nginx \
	-v /opt/nginx/html:/usr/share/nginx/html \
	-v /opt/nginx/log:/var/log/nginx \
	-d nginx
```
        
