# MyBatis-Plus简介


MyBatis-Plus（简称 MP）是一个 MyBatis 的增强工具，在 MyBatis 的基础上只做增强不做改变，为简化开发、提高效率而生。


# 特性


-  **无侵入**：只做增强不做改变，引入它不会对现有工程产生影响，如丝般顺滑
-  **损耗小**：启动即会自动注入基本 CURD，性能基本无损耗，直接面向对象操作
-  **强大的 CRUD 操作**：内置通用 Mapper、通用 Service，仅仅通过少量配置即可实现单表大部分 CRUD 操作，更有强大的条件构造器，满足各类使用需求
-  **支持 Lambda 形式调用**：通过 Lambda 表达式，方便的编写各类查询条件，无需再担心字段写错
-  **支持主键自动生成**：支持多达 4 种主键策略（内含分布式唯一 ID 生成器 - Sequence），可自由配置，完美解决主键问题
-  **支持 ActiveRecord 模式**：支持 ActiveRecord 形式调用，实体类只需继承 Model 类即可进行强大的 CRUD 操作
-  **支持自定义全局通用操作**：支持全局通用方法注入（ Write once, use anywhere ）
-  **内置代码生成器**：采用代码或者 Maven 插件可快速生成 Mapper 、 Model 、 Service 、 - - Controller 层代码，支持模板引擎，更有超多自定义配置等您来使用
-  **内置分页插件**：基于 MyBatis 物理分页，开发者无需关心具体操作，配置好插件之后，写分页等同于普通 List 查询
-  **分页插件支持多种数据库**：支持 MySQL、MariaDB、Oracle、DB2、H2、HSQL、SQLite、Postgre、SQLServer 等多种数据库
-  **内置性能分析插件**：可输出 Sql 语句以及其执行时间，建议开发测试时启用该功能，能快速揪出慢查询
-  **内置全局拦截插件**：提供全表 delete 、 update 操作智能分析阻断，也可自定义拦截规则，预防误操作



# 开始使用


通过一个简单的 Demo 来阐述 MyBatis-Plus 的强大功能


现有一张 User 表，其表结构如下：


```sql
DROP TABLE IF EXISTS user;

CREATE TABLE user
(
	id BIGINT(20) NOT NULL COMMENT '主键ID',
	name VARCHAR(30) NULL DEFAULT NULL COMMENT '姓名',
	age INT(11) NULL DEFAULT NULL COMMENT '年龄',
	email VARCHAR(50) NULL DEFAULT NULL COMMENT '邮箱',
	PRIMARY KEY (id)
);
```


其对应的数据库 Data 脚本如下：


```sql
DELETE FROM user;

INSERT INTO user (id, name, age, email) VALUES
(1, 'Jone', 18, 'test1@baomidou.com'),
(2, 'Jack', 20, 'test2@baomidou.com'),
(3, 'Tom', 28, 'test3@baomidou.com'),
(4, 'Sandy', 21, 'test4@baomidou.com'),
(5, 'Billie', 24, 'test5@baomidou.com');
```


pom.xml 如下


```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.3.4.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.example</groupId>
    <artifactId>demo-mybatis-plus</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo-mybatis-plus</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>

        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <scope>runtime</scope>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>

        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-boot-starter</artifactId>
            <version>3.4.0</version>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```
###
添加配置
application.yml


```yml
# 数据源配置
spring:
  datasource:
    username: root
    password: root123
    url: jdbc:mysql://localhost:3306/test?serverTimezone=GMT%2B8&characterEncoding=utf-8
    driver-class-name: com.mysql.cj.jdbc.Driver

# MyBatis-plus配置
mybatis-plus:
  mapper-locations: classpath*:mapper/*Mapper.xml
  type-aliases-package: com.example.demo.dataobject
```


在 Spring Boot配置类中添加 `@MapperScan` 注解，扫描 Mapper 包：


```java
@SpringBootApplication
@MapperScan("com.baomidou.mybatisplus.samples.quickstart.mapper")
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(QuickStartApplication.class, args);
    }

}
```


编写实体类 `User.java`（此处使用了 [Lombok](https://www.projectlombok.org/) 简化代码）


```java
@Data
public class User {
    private Long id;
    private String name;
    private Integer age;
    private String email;
}
```


编写Mapper类 `UserMapper.java`


```java
public interface UserMapper extends BaseMapper<User> {

}
```


添加测试类，进行功能测试：


```java
@SpringBootTest
public class SampleTest {

    @Autowired
    private UserMapper userMapper;

    @Test
    public void testSelect() {
        System.out.println(("----- selectAll method test ------"));
        List<User> userList = userMapper.selectList(null);
        Assert.assertEquals(5, userList.size());
        userList.forEach(System.out::println);
    }

}
```


# 主键生成策略


MyBatis-Plus如果不做任何主键策略配置，默认使用的是雪花算法。


snowflake算法是Twitter开源的分布式ID生成算法，结果是一个long类型的ID 。其核心思想：使用41bit作为毫秒数，10bit作为机器的ID（5bit数据中心，5bit的机器ID），12bit作为毫秒内的流水号（意味着每个节点在每个毫秒可以产生4096个ID），最后还有一个符号位，永远是0。


针对主键设置主键策略使用注解方式为


```java
@TableId(value = "id", type = IdType.ID_WORKER)
private Long id;
```


# 自动填充功能


像 **创建时间** 和 **修改时间** 这样的表字段是不需要手动插入, 可以设置为自动填充


在需要自动填充的字段上添加注解: `@TableField(fill = FieldFill.INSERT)`


```java
@Data
public class User {
    private Long id;
    private String name;
    private Integer age;
    private String email;

    @TableField(fill = FieldFill.INSERT)
    private Date createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    private Date updateTime;
}
```


自定义实现类 MyMetaObjectHandler


```java
@Slf4j
@Component
public class MyMetaObjectHandler implements MetaObjectHandler {

    @Override
    public void insertFill(MetaObject metaObject) {
        this.setFieldValByName("createTime",new Date(),metaObject);
        this.setFieldValByName("updateTime",new Date(),metaObject);
    }

    @Override
    public void updateFill(MetaObject metaObject) {
        this.setFieldValByName("updateTime",new Date(),metaObject);
    }
}
```


注意事项：


- 填充原理是直接给`entity`的属性设置值!!!
- 注解则是指定该属性在对应情况下必有值,如果无值则入库会是`null`
- `MetaObjectHandler`提供的默认方法的策略均为:如果属性有值则不覆盖,如果填充值为`null`则不填充
- 字段必须声明`TableField`注解,属性`fill`选择对应策略,该声明告知`Mybatis-Plus`需要预留注入`SQL`字段
- 填充处理器`MyMetaObjectHandler`在 Spring Boot 中需要声明`@Component`或`@Bean`注入
- 要想根据注解`FieldFill.xxx`和`字段名`以及`字段类型`来区分必须使用父类的`strictInsertFill`或者`strictUpdateFill`方法
- 不需要根据任何来区分可以使用父类的`fillStrategy`方法



```java
public enum FieldFill {
    /**
     * 默认不处理
     */
    DEFAULT,
    /**
     * 插入填充字段
     */
    INSERT,
    /**
     * 更新填充字段
     */
    UPDATE,
    /**
     * 插入和更新填充字段
     */
    INSERT_UPDATE
}
```


# 乐观锁插件


意图：


当要更新一条记录的时候，希望这条记录没有被别人更新


乐观锁实现方式：


- 取出记录时，获取当前version
- 更新时，带上这个version
- 执行更新时， set version = newVersion where version = oldVersion
- 如果version不对，就更新失败



## 配置乐观锁插件


```java
@Bean
public OptimisticLockerInterceptor optimisticLockerInterceptor() {
    return new OptimisticLockerInterceptor();
}
```


添加注解


实体类和数据表都要加上**version**字段


在实体类的**version**字段上加上注解


`@Version`


```java
@Version
private Integer version;
```


特别说明:


- **支持的数据类型只有:int,Integer,long,Long,Date,Timestamp,LocalDateTime**
- 整数类型下 `newVersion = oldVersion + 1`
- `newVersion` 会回写到 `entity` 中
- 仅支持 `updateById(id)` 与 `update(entity, wrapper)` 方法
- **在 **`**update(entity, wrapper)**`** 方法下, **`**wrapper**`** 不能复用**



## 测试乐观锁


**注意**:


测试乐观锁的时候必须先查询再修改


```java
@Test
public void update() {
	//先查询
    User user = userMapper.selectById(1315944359069253633L);
    user.setAge(25);
    user.setEmail("lemonxe@qq.com");
    //在修改
    int update = userMapper.updateById(user);
    System.out.println("成功修改:" + update);
}
```


# 分页插件


配置分页插件


```java
@Bean
public PaginationInterceptor paginationInterceptor() {
    PaginationInterceptor paginationInterceptor = new PaginationInterceptor();
    // 设置请求的页面大于最大页后操作， true调回到首页，false 继续请求  默认false
    // paginationInterceptor.setOverflow(false);
    // 设置最大单页限制数量，默认 500 条，-1 不受限制
    // paginationInterceptor.setLimit(500);
    // 开启 count 的 join 优化,只针对部分 left join
    paginationInterceptor.setCountSqlParser(new JsqlParserCountOptimize(true));
    return paginationInterceptor;
}
```


# 逻辑删除


**说明**:


只对自动注入的sql起效:


- 插入: 不作限制
- 查找: 追加where条件过滤掉已删除数据,且使用 wrapper.entity 生成的where条件会忽略该字段
- 更新: 追加where条件防止更新到已删除数据,且使用 wrapper.entity 生成的where条件会忽略该字段
- 删除: 转变为 更新



例如:


- 删除: `update user set deleted=1 where id = 1 and deleted=0`
- 查找: `select id,name,deleted from user where deleted=0`



字段类型支持说明:


- 支持所有数据类型(推荐使用 `Integer`,`Boolean`,`LocalDateTime`)
- 如果数据库字段使用`datetime`,逻辑未删除值和已删除值支持配置为字符串`null`,另一个值支持配置为函数来获取值如`now()`



附录:


- 逻辑删除是为了方便数据恢复和保护数据本身价值等等的一种方案，但实际就是删除。
- 如果你需要频繁查出来看就不应使用逻辑删除，而是以一个状态去表示。



## 添加逻辑删除字段


表中添加逻辑删除字段 , 对应实体类添加属性


## 添加注解


在实体类的逻辑删除属性上添加注解


`@TableLogic`


```java
@TableLogic
private Integer deleted;
```


## 配置逻辑删除插件


application.yml


```yml
mybatis-plus:
  global-config:
    db-config:
      logic-delete-field: deleted  # 全局逻辑删除的实体字段名(since 3.3.0,配置后可以不用再字段上加注解@TableLogic)
      logic-delete-value: 1 # 逻辑已删除值(默认为 1)
      logic-not-delete-value: 0 # 逻辑未删除值(默认为 0)
```


## 常见问题


### 如何 insert ?


>
> 1. 字段在数据库定义默认值(推荐)
> 1. insert 前自己 set 值
> 1. 使用自动填充功能
>




###  删除接口自动填充功能失效


>
> 1. 使用 `update` 方法并: `UpdateWrapper.set(column, value)`(推荐)
> 1. 使用 `update` 方法并: `UpdateWrapper.setSql("column=value")`
> 1. 使用[Sql注入器](https://baomidou.com/guide/sql-injector.html)注入`LogicDeleteByIdWithFill`并使用(推荐)
>




# 条件构造器

[条件构造器官方文档](https://baomidou.com/guide/wrapper.html#abstractwrapper)


# 代码生成器


AutoGenerator 是 MyBatis-Plus 的代码生成器，通过 AutoGenerator 可以快速生成 Entity、Mapper、Mapper XML、Service、Controller 等各个模块的代码，极大的提升了开发效率。



MyBatis-Plus 从 `3.0.3` 之后移除了代码生成器与模板引擎的默认依赖，需要手动添加相关依赖：


代码生成器依赖


```xml
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-generator</artifactId>
    <version>3.4.0</version>
</dependency>
```


模板引擎 依赖，MyBatis-Plus 支持 Velocity（默认）、Freemarker、Beetl


```xml
<dependency>
    <groupId>org.apache.velocity</groupId>
    <artifactId>velocity-engine-core</artifactId>
    <version>2.2</version>
</dependency>
```


示例代码


```java
//代码生成器
@Test
public void run() {
    AutoGenerator mpg = new AutoGenerator();

    // 全局配置
    GlobalConfig gc = new GlobalConfig();
    String projectPath = System.getProperty("user.dir");
    gc.setOutputDir(projectPath + "/src/main/java");
    gc.setAuthor("xiejinchi");
    gc.setOpen(false); //生成后是否打开资源管理器
    gc.setFileOverride(false); //重新生成时是否覆盖
    gc.setServiceName("%sService"); //去掉service接口的首字母I
    gc.setIdType(IdType.ID_WORKER); //主键策略
    gc.setDateType(DateType.ONLY_DATE); //定义生成的实体类中日期类型
    gc.setSwagger2(true); //开启 Swagger2 模式
    mpg.setGlobalConfig(gc);

    // 数据源配置
    DataSourceConfig dsc = new DataSourceConfig();
    dsc.setUrl("jdbc:mysql://localhost:3306/mybatis_plus?serverTimezone=GMT%2B8");
    dsc.setDriverName("com.mysql.cj.jdbc.Driver");
    dsc.setUsername("root");
    dsc.setPassword("garcon");
    mpg.setDataSource(dsc);

    // 包配置
    PackageConfig pc = new PackageConfig();
    pc.setParent("com.example.demo");
    pc.setModuleName("user"); //模块名
    pc.setEntity("entity");
    pc.setMapper("mapper");
    pc.setService("service");
    pc.setController("controller");
    mpg.setPackageInfo(pc);

    // 策略配置
    StrategyConfig strategy = new StrategyConfig();
    //表名，多个英文逗号分割
    strategy.setInclude("user".split(","));
    //数据库映射到实体类的命名策略
    strategy.setNaming(NamingStrategy.underline_to_camel);
    //数据库表映射到实体类的命名策略
    strategy.setColumnNaming(NamingStrategy.underline_to_camel);
    //生成实体时去掉表前缀
    strategy.setTablePrefix(pc.getModuleName() + "_");
    //你自己的父类实体,没有就不用设置!
    //strategy.setSuperEntityClass("");
    //Lombok模型
    strategy.setEntityLombokModel(true);
    //reset ful api风格控制器
    strategy.setRestControllerStyle(true);
    // 你自己的父类控制器,没有就不用设置!
    //strategy.setSuperControllerClass("");
    //url中驼峰转连接字符
    strategy.setControllerMappingHyphenStyle(true);
    mpg.setStrategy(strategy);
    //执行
    mpg.execute();
}
```
        
