修改密码
```
ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
```

添加用户
```
CREATE USER 'orange'@'%' IDENTIFIED BY 'password';
```

授权
```
GRANT ALL ON *.* TO 'orange'@'%';
```

支持远程登录
```
ALTER USER 'orange'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
```

刷新权限
```
FLUSH PRIVILEGES;
```
