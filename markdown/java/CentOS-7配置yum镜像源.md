1. 备份原本的yum镜像源
```bash
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
```

2. 下载阿里云yum镜像源
```bash
wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
```

3. 清除系统所有的yum缓存
```bash
yum clean all
```

4. 生成yum缓存
```bash
yum makecache
```
