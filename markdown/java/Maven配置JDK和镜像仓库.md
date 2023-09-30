# 配置JDK版本

配置为JDK1.8

修改settings.xml ,添加如下内容

```xml
<profile>
  <id>jdk-1.8</id>
  <activation>
      <activeByDefault>true</activeByDefault>
      <jdk>1.8</jdk>
  </activation>

  <properties>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
    <maven.compiler.compilerVersion>1.8</maven.compiler.compilerVersion>
  </properties>
</profile>
```

# 配置Maven镜像源

配置为阿里云镜像
修改settings.xml ,添加如下内容

```xml
<!-- 阿里云仓库 -->
<mirror>
   <id>nexus-aliyun</id>
   <mirrorOf>central</mirrorOf>
   <name>Nexus aliyun</name>
   <url>http://maven.aliyun.com/nexus/content/groups/public</url>
</mirror>

<!-- 中央仓库1 -->
<mirror>
   <id>repo1</id>
   <mirrorOf>central</mirrorOf>
   <name>Human Readable Name for this Mirror.</name>
   <url>http://repo1.maven.org/maven2/</url>
</mirror>

<!-- 中央仓库2 -->
<mirror>
   <id>repo2</id>
   <mirrorOf>central</mirrorOf>
   <name>Human Readable Name for this Mirror.</name>
   <url>http://repo2.maven.org/maven2/</url>
</mirror>
```

# 配置Maven本地仓库位置

修改settings.xml ,添加如下内容

```xml
<localRepository>E:/repository</localRepository>
```
        
