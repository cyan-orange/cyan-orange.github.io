修改VMware网络配置
编辑 >虚拟网络编辑器
![](../../image/526f1e4b-01ea-4bb0-9656-19fc14415a1a.png)

![](../../image/7ca99ad6-3fba-4c20-9120-3f1dcc96edb8.png)

![](../../image/884c6d29-7044-435f-9448-fba855076f82.png)

编辑虚拟机设置
![](../../image/61e8369c-06a8-4f29-8bdc-235e6ecc2cef.png)

网络适配器选择桥接模式
![](../../image/d50958ec-660e-45a1-897f-013063b11f23.png)


查看主机网关 `ipconfig`
![](../../image/7c7bcc33-ff3f-4a91-847c-194621208d43.png)

修改CentOS网络配置，网关和主机网关一致，IP地址和主机在同一个网段 `vim /etc/sysconfig/network-scripts/ifcfg-ens33` ![](../../image/13b12acf-0a89-452d-b2a0-4116f7a66558.png) ``` TYPE=Ethernet PROXY_METHOD=none BROWSER_ONLY=no BOOTPROTO=static DEFROUTE=yes IPV4_FAILURE_FATAL=no IPV6INIT=yes IPV6_AUTOCONF=yes IPV6_DEFROUTE=yes IPV6_FAILURE_FATAL=no NAME=enp0s3 UUID=eae5023a-eec6-47ef-8213-8ecba2b2ba99 DEVICE=enp0s3 ONBOOT=yes IPADDR=192.168.1.119 GATEWAY=192.168.1.1 NETMASK=255.255.255.0 DNS1=8.8.8.8

```

重启网络：`systemctl restart network.service`
        
