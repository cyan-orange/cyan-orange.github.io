## 安装Jenkins

```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo

sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.keyreload

yum install epel-release

yum install java-11-openjdk-devel

yum install jenkins

```

修改Jenkins配置，使用本机root用户登录Jenkins，`vim /etc/sysconfig/jenkins`
```bash 
JENKINS_USER="root"
```

启动Jenkins

```bash
sudo systemctl start jenkins
```

检查 Jenkins 服务的状态：

```bash
sudo systemctl status jenkins
```

防火墙添加端口，jenkins默认的端口为8080

```bash
firewall-cmd --zone=public --add-port=8080/tcp --permanent

#重新加载防火墙
firewall-cmd --reload
```

浏览器访问ip地址:端口，如下所示表示安装成功

![](../../image/3cca623b-1146-4fa4-add0-35a3e622e4c6.png)


获取密码

```bash
cat /var/lib/jenkins/secrets/initialAdminPassword
```

输入密码之后进入下页面：Jenkins安装插件默认从官网下载，速度很慢，暂时不安装插件，点击选择插件来安装

![](../../image/d41f7678-38ac-466d-8f6e-d719d7fb8ac5.png)


点击 无，点击 安装

![](../../image/a785f386-9192-4b1b-8f4c-2ad72ae538c9.png)


创建第一个管理员用户

![](../../image/b4a667d9-cdee-49e8-8c85-ae260e980b36.png)


![](../../image/ee02af10-6aae-42a3-b249-a8f81626f997.png)


![](../../image/6c06ba3b-eb78-4a87-a60d-fbb91489bb9a.png)


## 修改插件下载地址

浏览器访问： https://mirrors.aliyun.com/jenkins/updates/

![](../../image/c04571bf-8216-413e-84ed-d20c25d9a6ce.png)


访问jenkins：Manage Jenkins–>Manage Plugins

![](../../image/7f9ff937-d4b3-4549-8572-e8306df72ff1.png)


选择Advanced

![](../../image/60ab2135-5ff3-4114-a578-2a9c7ebff10e.png)


滑到最下面，将Update Site的url改为刚才复制的地址，点击submit

https://mirrors.aliyun.com/jenkins/updates/update-center.json

![](../../image/aa5d3b20-432a-46c6-b26d-4b174fe7263b.png)


重启Jenkins，在端口号后加`/restart`可以重启Jenkins，例如 http://192.168.1.102:8080/restart ，点击yes

![](../../image/80ff1fcb-7790-4183-b984-7f984c574b3c.png)


## 安装Jenkins中文插件

![](../../image/754d9891-be8d-428f-9b23-648ae08cf94e.png)


安装后重启，可以看到Jenkins界面变成了中文

![](../../image/4ea522d2-952b-4f48-9a1b-6b3bca21cedc.png)


## 安装权限管理插件

在可选插件中输入 role-based 查找插件并安装
![](../../image/f70878b0-4b3e-4593-ae2c-1022b1e23310.png)


配置权限
![](../../image/1b379ee6-de3c-43da-bfd6-a49a28fce173.png)

授权策略选择 Role-Based Strategy
![](../../image/8cd426e6-0e62-41fe-adc7-7b24e8f512b6.png)

## Jenkins使用凭证管理


在可选插件中输入 Credentials Binding 安装插件
![](../../image/950072d1-a47c-4717-acd2-36942677294b.png)


安装完成之后在Manage jenkins中可以看见凭证配置
![](../../image/f3818b28-3b24-4565-9dfa-c712be1dd6d4.png)

## Jenkins安装Git插件
Jenkins要去GitLab拉取代码，需要Jenkins安装git插件，部署Jenkins的的机器安装Git

Jenkins安装git插件在可选插件中搜索git安装即可

安装git
```bash
yum install -y git
```

查看git是否安装成功
```bash
git --version
```

## jenkins使用ssh私钥凭证拉取GitLab代码

在CentOS中输入 `ssh-keygen -t rsa`，一路按回车，会在`~/.ssh/`目录下生成公钥和私钥

![](../../image/6f4c2f9e-18ee-4e47-8006-2024f41acb1b.png)

私钥
```bash
[root@strawberry ~]# cat .ssh/id_rsa
-----BEGIN RSA PRIVATE KEY----- MIIEpAIBAAKCAQEA1fM+hbjmx4J4zCMSF79sPiKQP65Wa2YXF5Q39j3LFN0ssyyj TjO8mSi1xaDCz0s2cqoi6+sa/OotfbcWS/dpzYV+ZdAcP3DF3YWj/tDY8V27hr8K qRdXHRvvkqnur1Tz0EYkOPHAm9uovs9zunc00BUERCb73m4IKEWxdR+E0HdTp3ht VnB9qfsed1dAm2xqRDbHK6cJABhvQgB/T54Mq/+u3UdRzPyBrxml6tAVIEn5bzTK 01hy2eUfReaAcSltcLqcgFXUMIFML9J4XUQaR0etHLFhRecMgzQd5qr3xIuWD+S1 2U/McveNUioQtHrj/3CizKqVtHhOfxvDVLUQBwIDAQABAoIBAQCgHg4Bl9KnJ17u L6T/vtPsYIOiFQA6GkpX7CZBlBdjQu+MHHEPOqr/2LbI87o31yslf2zpMKee9kcb WaVHLx+wnyJsYeZyGB0M31JPhs+FO8f3XQxGZeBdOaX/Fkw6TZK2oXfEYjDqs+bC /pC20TXmMIRj2OUQnzpdoWLgq7kDJZuAEs9lvqpNFBXnX9j3hu8QOwfbLTQo6Hu/ ferWx+6km9WcW8qE/Xb13HHOckSoTCg2WLPTbj2KADgn4Hr83ofyyzyrHNgJRSl2 TuhvvHVXLih7PW20HQ6TPcR5CeBdyjhoaXYKRZqux4IdqDeGh+d6VBPUSqqogPxT XKFhmsJxAoGBAPru6SFcL7qFp5PFRrFeJCAs0aBChmj99FExGQCEv4byP3c2cNMf j0+LVuYNNUnGi3XUesXJ6oN6gAqI6SnMhz8nMS2JEt94s70YkcdY763hSdw95Tb2 8F7wVi7fzXsjfBiisAWaq+5msptv7MZfTF0NcmoFdvmpR6lKYKo46Ep/AoGBANpF KnGHYdvY2GoM7pWJj3g7EzSlslXpeG9NXQFH9z1YHNoEtUtZphFOtFxwtc9R08Ph NK035Jb4D48XxiNNbHZ8lnAgw6LkPEKnfb6++qMxxe1sjHjii7TSbugF9dwVtSpu +dTJpbHGNmC5TSAVFDs4RT9pAMROUH7Z9YQQpSZ5AoGBAI//GXkzVZBLsmZyBqcx xrlP/ttgUZFeah1Nd3N8ugvOZ+0ZKJV+vtZ+t1c8rR+w98aeL/XgcNsSKPfiqSp7 XAE5lFb1GgdzVHFm8ADdYGz/o0rnmel4u2c/s7UiaOAI9OWONkSBBbjA5i2chNsx RLkBRm7gw+1w3tae/+muzl4xAoGAV2ssPJwETZDj3FWhmLKni3fdkVBrxIzld258 uW6hTyhjJc6M7cjSAkyLYBqkNoyHTAR+nIGuQ+jGEoFrEeiIcEwl1HLK6AqROADt E+BZcdMVeqnm+OODIMDHOpZoieUH0h7wYJECk9jXHpYYlajbmXxH/8WGURkslCGn e2VPP8ECgYACCBXQa70SIVqkTBD7fdc0T01zqyejjtNdk1a4kpGDECkPJryMye6E lgH+Bcnp2elgMmZd/MQYUNAz3ZBra6ahg+6TT2FXstHrFs6S0sPWmlSIZYeVl8jJ iRrKTlzXKv51GOQQeajT0bf0Rdcpvx5yGh1mawIDuEEWhKBU5TnzdQ==
-----END RSA PRIVATE KEY-----
```

公钥
```bash
[root@strawberry ~]# cat .ssh/id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDV8z6FuObHgnjMIxIXv2w+IpA/rlZrZhcXlDf2PcsU3SyzLKNOM7yZKLXFoMLPSzZyqiLr6xr86i19txZL92nNhX5l0Bw/cMXdhaP+0NjxXbuGvwqpF1cdG++Sqe6vVPPQRiQ48cCb26i+z3O6dzTQFQREJvvebggoRbF1H4TQd1OneG1WcH2p+x53V0CbbGpENscrpwkAGG9CAH9Pngyr/67dR1HM/IGvGaXq0BUgSflvNMrTWHLZ5R9F5oBxKW1wupyAVdQwgUwv0nhdRBpHR60csWFF5wyDNB3mqvfEi5YP5LXZT8xy941SKhC0euP/cKLMqpW0eE5/G8NUtRAH root@strawberry
```

在GitLab中添加`ssh key`，使用root账户登录GitLab

![](../../image/33b2b6d1-1bba-4b79-8db4-f2ba1e742f68.png)

![](../../image/2dc1ebce-d94d-4738-9cab-f7e183111ce6.png)

将刚才生成的公钥复制进去

![](../../image/ac093d14-b9f2-4cea-9bfd-277bcd55ee6d.png)



在Jenkins的项目配置中，源码管理 Repository URL要填GitLab项目中ssh链接地址

![](../../image/7e38a9d6-746a-4326-97d4-d002440184db.png)

将刚才生成的私钥复进去
![](../../image/9440667b-08bd-44d7-afaa-ebd5105d0e35.png)


## jenkins配置maven和jdk
jdk在安装Jenkins的时候已经安装了，现在还需要安装maven
浏览器访问maven官网，下载maven压缩包 https://maven.apache.org/download.cgi
![](../../image/830f4159-33a4-4982-afa2-2f4c829704c0.png)

上传maven压缩包到CentOS，解压到`/opt/`目录下
```bash
tar xvf apache-maven-3.8.4-bin.tar.gz -C /opt/
```

```bash
[root@strawberry ~]# ll /opt/
总用量 0
drwxr-xr-x. 6 root root 99 2月   4 00:26 apache-maven-3.8.4
drwxr-xr-x. 8 root root 96 2月   3 16:36 jdk-11
```

配置maven环境变量：`vim /etc/profile`，添加如下内容
```bash
export MAVEN_HOME=/opt/apache-maven-3.8.4
export PATH=$PATH:$MAVEN_HOME/bin
```

使配置生效
```bash
source /etc/profile
```

验证配置是否成功：`mvn --version`
```bash
[root@strawberry ~]# mvn --version
Apache Maven 3.8.4 (9b656c72d54e5bacbed989b64718c159fe39b537)
Maven home: /opt/apache-maven-3.8.4
Java version: 11.0.14, vendor: Red Hat, Inc., runtime: /usr/lib/jvm/java-11-openjdk-11.0.14.0.9-1.el7_9.x86_64
Default locale: zh_CN, platform encoding: UTF-8
OS name: "linux", version: "3.10.0-1160.53.1.el7.x86_64", arch: "amd64", family: "unix"
```

maven配置阿里云镜像仓库地址、本地仓库地址，修改maven配置文件：`vim /opt/apache-maven-3.8.4/conf/settings.xml`
本地仓库位置
```xml
<localRepository>/root/maven_repo</localRepository>
```

阿里云仓库地址
```xml
<mirror>
    <id>nexus-aliyun</id>
    <mirrorOf>central</mirrorOf>
    <name>Nexus aliyun</name>
    <url>http://maven.aliyun.com/nexus/content/groups/public</url>
</mirror>
```

在Jenkins中配置jdk和maven，首先在 Global Tool configruation中配置，然后在 Configure System中配置

点击 Manage Jenkins > Global Tool configruation

![](../../image/2eeca752-fec2-49fa-bdc3-e17eff4f1a05.png)

![](../../image/ab3d0888-4616-4510-84c8-ae40828b66f8.png)

新增JDK
![](../../image/ee236d32-8bb0-4367-bdb5-100002f2833f.png)

填写jdk别名、jkd的安装目录，去掉 Install automatically选项
![](../../image/a051cce3-79a5-4b00-a173-9207732cda82.png)

新增maven
![](../../image/132431ca-309b-4f22-ac2f-cbe11304bdfd.png)

点击应用，点击保存

点击 Manage Jenkins > Configure System

![](../../image/f13c3dc6-56f9-48c2-a20a-0440dc662a59.png)

在全局属性中新增环境变量
![](../../image/d7bf7ac2-91ca-4f37-982a-c79ef015c3bc.png)

添加三个环境变量：JAVA_HOME、M2_HOME、PATH+EXTRE
![](../../image/64f3f53a-4c9a-4f24-b183-e5d71363fa3f.png)

点击应用，点击保存

验证配置是否成功，项目配置 > 构建触发器 > 增加构建步骤 > Excute shell
![](../../image/ffbdb1e8-ec4d-4754-9cc4-085692f5988e.png)

输入命令：mvn package
![](../../image/cdeffffd-22fc-45c2-aff6-3c678a835077.png)

点击应用，点击保存


验证Jenkins配置jdk和maven是否成功，点击这个项目
![](../../image/4edc4615-9261-47ea-9687-fba48775dbc4.png)

点击 Build Now
![](../../image/bf169a13-63d4-4089-a514-91998d2fdf6b.png)

![](../../image/bc56f036-eb11-4a36-9912-ecf63e7f4a13.png)

点击控制台输出
![](../../image/6e0bfab9-6388-4cf1-a0a1-87d4b4cfed69.png)

滑到最下面看是否构建成功
![](../../image/3f2f371f-52b2-4530-b93a-f4b3c978319d.png)
        
