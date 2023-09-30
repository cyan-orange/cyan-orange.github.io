下载Nginx源码包上传到CentOS服务器
安装gcc，Nginx编译源码时所需要的编译器

```
yum install -y gcc
```

安装pcre，让 nginx 支持重写功能

```
yum -y install pcre pcre-devel
```

安装zlib，zlib 库提供了很多压缩和解压缩的方式，nginx 使用 zlib 对 http 包内容进行 gzip 压缩

```
yum -y install zlib zlib-devel
```

安装openssl，安全套接字层密码库，用于通信加密

```
yum -y install openssl openssl-devel
```

解压Nginx源码包

```
tar zxvf nginx-1.20.2.tar.gz
```



进入Nginx源码目录

```
cd nginx-1.20.2
```



为编译安装做准备

```
./configure --prefix=/usr/local/nginx
```



编译安装

```
make && make install
```



启动Nginx

```
cd /usr/local/nginx/sbin
./nginx
```

nginx常用命令

```
./nginx    #启动
./nginx    #停止
./nginx -s quit    #优雅关闭，在推出前完成已接受的连接请求
./nginx -s reload    #重新加载配置
```



将nginx设置为系统服务，创建服务脚本：`vim /usr/lib/systemd/system/nginx.service` ``` [Unit] Description=nginx - web server After=network.target remote-fs.target nss-lookup.target [Service] Type=forking PIDFile=/usr/local/nginx/logs/nginx.pid ExecStartPre=/usr/local/nginx/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf ExecStart=/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf ExecReload=/usr/local/nginx/sbin/nginx -s reload ExecStop=/usr/local/nginx/sbin/nginx -s stop ExecQuit=/usr/local/nginx/sbin/nginx -s quit PrivateTmp=true [Install] WantedBy=multi-user.target
```



创建服务脚本之后需要重新加载系统服务

```
systemctl daemon-reload
```

设置开机启动
```
systemctl enable nginx.service
```
        
