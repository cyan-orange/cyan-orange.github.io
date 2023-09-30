直接双击安装deb文件包，可能会出现安装不上的问题，这时候我们建议使用dpkg命令安装。

## 安装

```
sudo dpkg -i package_name.deb
```

通常情况下会报依赖关系的错误，我们可以使用以下的命令修复安装
```
sudo apt install -f
```

## 查找

查找安装的软件
```
dpkg -l |grep -i 软件名
```

## 卸载
```
sudo dpkg -r 软件名
```
        
