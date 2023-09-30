MySQL做了读写分离，一主两从。主服务器写数据，从服务器只可以读数据，不可以写数据

所以现在有三个数据源，写一个，读两个

使用MyBatis-Plus的多数据源来做数据源的切换

加入依赖
```xml
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-boot-starter</artifactId>
    <version>3.4.2</version>
</dependency>
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>dynamic-datasource-spring-boot-starter</artifactId>
    <version>3.4.1</version>
</dependency>
```



配置多数据源

```yaml
spring:
  datasource:
    dynamic:
      primary: master #设置默认的数据源或者数据源组,默认值即为master
      strict: false #严格匹配数据源,默认false. true未匹配到指定数据源时抛异常,false使用默认数据源
      datasource:
        master:
          url: jdbc:mysql://192.168.43.208:3306/test?serverTimezone=GMT%2B8&characterEncoding=utf-8
          username: root
          password: orange
          driver-class-name: com.mysql.cj.jdbc.Driver # 3.2.0开始支持SPI可省略此配置
        slave_1:
          url: jdbc:mysql://192.168.43.163:3306/test?serverTimezone=GMT%2B8&characterEncoding=utf-8
          username: orange123
          password: orange123
          driver-class-name: com.mysql.cj.jdbc.Driver
        slave_2:
          url: jdbc:mysql://192.168.43.116:3306/test?serverTimezone=GMT%2B8&characterEncoding=utf-8
          username: orange
          password: orange123
          driver-class-name: com.mysql.cj.jdbc.Driver
```





约定

1. 本框架只做 **切换数据源** 这件核心的事情，并**不限制你的具体操作**，切换了数据源可以做任何CRUD。
2. 配置文件所有以下划线 `_` 分割的数据源 **首部** 即为组的名称，相同组名称的数据源会放在一个组下。
3. 切换数据源可以是组名，也可以是具体数据源名称。组名则切换时采用负载均衡算法切换。
4. 默认的数据源名称为 **master** ，你可以通过 `spring.datasource.dynamic.primary` 修改。
5. 方法上的注解优先于类上注解。
6. DS支持继承抽象类上的DS，暂不支持继承接口上的DS。





使用 **@DS** 切换数据源。

**@DS** 可以注解在方法上或类上，**同时存在就近原则 方法上注解 优先于 类上注解**。

|     注解      |                   结果                   |
| :-----------: | :--------------------------------------: |
|    没有@DS    |                默认数据源                |
| @DS("dsName") | dsName可以为组名也可以为具体某个库的名称 |

```java
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, UserDO> implements UserService {

    @DS("master")
    @Override
    public ResponseData<Void> addUser(UserDO userDO) {
        int insert = baseMapper.insert(userDO);
        if (insert < 1) {
            new ResponseData<Void>().field();
        }
        return new ResponseData<Void>().ok();
    }

    @DS("slave")
    @Override
    public ResponseData<UserDO> getUserById(Long id) {
        return new ResponseData<UserDO>().ok(super.getById(id));
    }
}
```
        
