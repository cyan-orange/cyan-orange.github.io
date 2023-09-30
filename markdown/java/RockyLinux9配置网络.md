编辑配置文件`vim /etc/sysconfig/network-scripts/ifcfg-enp0s3` ```bash TYPE=Ethernet PROXY_METHOD=none BROWSER_ONLY=no BOOTPROTO=none DEFROUTE=yes IPV4_FAILURE_FATAL=no IPV6INIT=no NAME=enp0s3 DEVICE=enp0s3 ONBOOT=yes IPADDR=192.168.1.110 PREFIX=24 GATEWAY=192.168.1.1 DNS1=8.8.8.8 DNS2=114.114.114.114 IPV6_DISABLED=yes
```

重新加载配置文件
```bash
nmcli connection load /etc/sysconfig/network-scripts/ifcfg-enp0s3
```

激活配置文件
```bash
nmcli connection up /etc/sysconfig/network-scripts/ifcfg-enp0s3
```
