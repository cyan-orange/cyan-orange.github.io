
# 描述

CentOS6自带的防火墙是iptables，CentOS7自带的防火墙是firewall。
**iptables：**用于过滤数据包，属于网络层防火墙。
**firewall：**底层还是使用 iptables 对内核命令动态通信包过滤的，简单理解就是firewall是centos7下管理

# iptables 防火墙

```
# 查看防火墙状态
service iptables status

# 停止防火墙
service iptables stop

# 启动防火墙
service iptables start

# 重启防火墙
service iptables restart

# 永久关闭防火墙
chkconfig iptables off

# 永久关闭后重启
chkconfig iptables on
```

## 开启80端口

```
# 编辑iptales
vim /etc/sysconfig/iptables

# 加入以下代码然后保存退出
-A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT

#重启防火墙
service iptables restart
```

# firewall 防火墙

## 查看firewall服务状态

```
systemctl status firewalld
```

出现Active: **active (running)**绿色高亮显示则表示是启动状态。 出现 Active: inactive (dead)灰色表示停止状态。

## 查看firewall的状态

```
firewall-cmd --state
```

## 开启、重启、关闭firewall服务

```
# 开启
service firewalld start

# 重启
service firewalld restart

# 关闭
service firewalld stop

4.查看防火墙规则
firewall-cmd --list-all
```

## 查看、开放、关闭端口

```
# 查询端口是否开放
firewall-cmd --query-port=8080/tcp

# 开放80端口
firewall-cmd --permanent --add-port=80/tcp

# 移除端口
firewall-cmd --permanent --remove-port=8080/tcp

#重启防火墙(修改配置后要重启防火墙)
firewall-cmd --reload
```

## 指定IP和端口访问

```
# 添加规则
firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.1.100" port protocol="tcp" port="8080" accept"

# 移除规则
firewall-cmd --permanent --remove-rich-rule="rule family="ipv4" source address="192.168.1.100" port protocol="tcp" port="8080" accept"
```

## firewall 常用命令

```
# 查看防火墙状态，是否是running
firewall-cmd --state

# 重新载入配置，比如添加规则之后，需要执行此命令
firewall-cmd --reload

# 列出支持的zone
firewall-cmd --get-zones

# 列出支持的服务，在列表中的服务是放行的
firewall-cmd --get-services

# 查看ftp服务是否支持，返回yes或者no
firewall-cmd --query-service ftp

# 临时开放ftp服务
firewall-cmd --add-service=ftp

# 永久开放ftp服务
firewall-cmd --add-service=ftp --permanent

# 永久移除ftp服务
firewall-cmd --remove-service=ftp --permanent

# 永久添加80端口
firewall-cmd --add-port=80/tcp --permanent

# 查看规则，这个命令和iptables的相同
iptables -L -n

# 查看帮助
man firewall-cmd
```
        
