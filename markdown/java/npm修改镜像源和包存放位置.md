NPM是Node提供的模块管理工具，可以非常方便的下载安装前端框架。

node安装完成之后可以使用下命令查看和修改相关配置

查看配置
```bash
npm config ls
```
修改全局包下载存放位置
```bash
npm config set prefix "E:\node\node_global"
```

修改node缓存的位置
```bash
npm config set cache "E:\node\node_cache"
```

修改npm镜像为淘宝
```bash
npm config set metrics-registry "https://registry.npm.taobao.org/"
```
