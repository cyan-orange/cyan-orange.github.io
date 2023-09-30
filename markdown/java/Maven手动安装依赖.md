如果某个依赖在maven中央仓库中没有，或者总是通过maven下载不下来，可以考虑手动安装依赖到Maven本地仓库中

比如说要手动安装`lucene-analyzers-common-8.9.0.jar`, 它的坐标如下
```xml
<dependency>
    <groupId>org.apache.lucene</groupId>
    <artifactId>lucene-analyzers-common</artifactId>
    <version>8.9.0</version>
</dependency>
```

在jar所在位置打开cmd窗口，执行如下命令，`^` 是cmd中的换行符
```bash
mvn install:install-file ^ -DgroupId=org.apache.lucene ^ -DartifactId=lucene-analyzers-common ^ -Dversion=8.9.0 ^ -Dpackaging=jar ^ -Dfile=lucene-analyzers-common-8.9.0.jar
```
