# ElasticSearch的Java客户端

官方文档：https://www.elastic.co/guide/en/elasticsearch/client/index.html

Java REST 客户端有两种风格：

- Java 低级 REST 客户端：Elasticsearch 的官方低级客户端。它允许通过 http 与 Elasticsearch 集群通信。将请求编组和响应取消编组给用户。它与所有 Elasticsearch 版本兼容。
- Java 高级 REST 客户端：Elasticsearch 的官方高级客户端。基于低级客户端，它公开 API 特定方法并处理请求编组和响应解组。

一般使用高级的REST客户端，因为它对低级的REST客户端做了封装，比较方便。

Java高级  REST Client 至少需要 Java 1.8 并且依赖于 Elasticsearch 核心项目。客户端版本与开发客户端的 Elasticsearch 版本相同。

Java高级  REST Client 的Maven仓库

```xml
<dependency>
    <groupId>org.elasticsearch.client</groupId>
    <artifactId>elasticsearch-rest-high-level-client</artifactId>
    <version>7.14.2</version>
</dependency>
```



# Spring Boot整合ElasticSearch

创建Spring Boot项目，引入ElasticSearch的Java 高级 REST 客户端依赖，并修改Elasticsearch 核心项目依赖的版本，因为在Spring Boot项目的父项目依赖管理中定义了ElasticSearch核心项目依赖的版本，所以要修改为自己的版本

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.4.11</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.example</groupId>
    <artifactId>demo-elasticsearch</artifactId>
    <version>0.0.1-SNAPSHOT</version>

    <properties>
        <java.version>1.8</java.version>
        <elasticsearch.version>7.14.0</elasticsearch.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.elasticsearch.client</groupId>
            <artifactId>elasticsearch-rest-high-level-client</artifactId>
            <version>7.14.0</version>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
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



配置`RestHighLevelClient` 和 `RequestOptions `

```java
@Configuration
public class ElasticSearchConfig {

    public static final RequestOptions COMMON_OPTIONS;

    static {
        RequestOptions.Builder builder = RequestOptions.DEFAULT.toBuilder();
/*        builder.addHeader("Authorization", "Bearer " + TOKEN);
        builder.setHttpAsyncResponseConsumerFactory(
                new HttpAsyncResponseConsumerFactory
                        .HeapBufferedResponseConsumerFactory(30 * 1024 * 1024 * 1024));*/
        COMMON_OPTIONS = builder.build();
    }

    @Bean
    public RestHighLevelClient restHighLevelClient() {
        return new RestHighLevelClient(
                RestClient.builder(
                        new HttpHost("127.0.0.1", 9200, "http")));
    }
}
```



## 保存数据

可以保存数据，也可以修改数据，多次保存同一个数据version值会增加

```java
@SpringBootTest
class DemoElasticsearchApplicationTests {

    @Autowired
    private RestHighLevelClient restClient;

    @Test
    void indexRequest() throws IOException {
        //创建索引
        IndexRequest request = new IndexRequest("users");
        //数据的id
        request.id("1");
        User user = new User();
        user.setId(1L);
        user.setName("青橙");
        user.setAge(25);
        user.setGender("男");
        String jsonString = JSON.toJSONString(user);
        request.source(jsonString, XContentType.JSON);
        IndexResponse response = restClient.index(request, ElasticSearchConfig.COMMON_OPTIONS);
        System.out.println(response);
    }
}
```



## 更新数据

当数据没有发生改变时，元数据的version值也不会增加

```java
@SpringBootTest
class DemoElasticsearchApplicationTests {

    @Autowired
    private RestHighLevelClient restClient;

    @Test
    void updateRequest() throws IOException {
        UpdateRequest request = new UpdateRequest("users", "1");
        User user = new User();
        user.setName("青橙ee");
        String jsonString = JSON.toJSONString(user);
        request.doc(jsonString, XContentType.JSON);
        UpdateResponse updateResponse = restClient.update(request, ElasticSearchConfig.COMMON_OPTIONS);
        System.out.println(updateResponse);
    }
}
```



## 获取数据

根据文档的id来获取数据

```java
@SpringBootTest
class DemoElasticsearchApplicationTests {

    @Autowired
    private RestHighLevelClient restClient;

    @Test
    void getRequest() throws IOException {
        GetRequest request = new GetRequest("users", "1");
        GetResponse response = restClient.get(request, ElasticSearchConfig.COMMON_OPTIONS);
        if (response.isExists()) {
            String sourceAsString = response.getSourceAsString();
            User user = JSON.parseObject(sourceAsString, User.class);
            System.out.println(user);
        } else {
            System.out.println("没有搜索到数据");
        }
    }
}
```



## 删除数据

根据文档id删除数据

```java
@SpringBootTest
class DemoElasticsearchApplicationTests {

    @Autowired
    private RestHighLevelClient restClient;

    @Test
    void deleteRequest() throws IOException {
        DeleteRequest deleteRequest = new DeleteRequest("users", "1");
        DeleteResponse deleteResponse = restClient.delete(deleteRequest, ElasticSearchConfig.COMMON_OPTIONS);
        ReplicationResponse.ShardInfo shardInfo = deleteResponse.getShardInfo();
        if (shardInfo.getTotal() != shardInfo.getSuccessful()) {
            System.out.println("删除数据成功");

        }
    }
}
```



## 复杂检索

构建一个复杂的检索，并获取检索到的数据：文档元数据、文档数据、分析信息。如下

```json
GET /bank/_search
{
  "query": {
    "match": {
      "address": "mill"
    }
  },
  "aggs": {
    "ageAgg": {
      "terms": {
        "field": "age",
        "size": 10
      }
    },
    "balanceAvg": {
      "avg": {
        "field": "balance"
      }
    }
  }
}
```



```java
@SpringBootTest
class DemoElasticsearchApplicationTests {

    @Autowired
    private RestHighLevelClient restClient;

    @Test
    void searchRequest() throws IOException {
        //创建索引请求
        SearchRequest searchRequest = new SearchRequest();
        //指定DSL检索条件
        SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
        //检索条件：address中包含mill的
        MatchQueryBuilder matchQuery = QueryBuilders.matchQuery("address", "mill");
        searchSourceBuilder.query(matchQuery);

        //聚合：根据年龄分布进行聚合
        TermsAggregationBuilder ageAgg = AggregationBuilders.terms("ageAgg").field("age").size(10);
        searchSourceBuilder.aggregation(ageAgg);
        //聚合：根据平均薪资进行聚合
        AvgAggregationBuilder balanceAvg = AggregationBuilders.avg("balanceAvg").field("balance");
        searchSourceBuilder.aggregation(balanceAvg);

        searchRequest.source(searchSourceBuilder);
        //执行检索
        SearchResponse searchResponse = restClient.search(searchRequest, ElasticSearchConfig.COMMON_OPTIONS);
        //获取检索结果
        SearchHits hits = searchResponse.getHits();
        //检索到的文档总数
        long value = hits.getTotalHits().value;
        System.out.println("检索到的文档总数" + value);
        //文档最大分数
        float maxScore = hits.getMaxScore();
        System.out.println("文档最大分数" + maxScore);

        SearchHit[] searchHits = hits.getHits();
        for (SearchHit hit : searchHits) {
            //文档所属索引
            String index = hit.getIndex();
            System.out.println("文档所属索引" + index);
            //文档id
            String id = hit.getId();
            System.out.println("文档id" + id);
            //文档得分
            float score = hit.getScore();
            System.out.println("文档得分" + score);
            //文档数据
            String sourceAsString = hit.getSourceAsString();
            AccountDTO accountDTO = JSON.parseObject(sourceAsString, AccountDTO.class);
            System.out.println("文档内容" + accountDTO);

            //获取检索到的分析信息
            Aggregations aggregations = searchResponse.getAggregations();

            //获取年龄分布聚合的分析信息
            Terms ageAggregation = aggregations.get("ageAgg");
            for (Terms.Bucket bucket : ageAggregation.getBuckets()) {
                Integer key = Integer.parseInt(bucket.getKey().toString());
                long docCount = bucket.getDocCount();
                System.out.println("key: " + key + ", docCount: " + docCount);
            }
            //获取平均薪资的聚合分析信息
            Avg balanceAggregation = aggregations.get("balanceAvg");
            double avgValue = balanceAggregation.getValue();
            System.out.println("平均薪资是：" + avgValue);
        }
    }
}
```
        
