Spring Cloud Gateway 的自定义Filter分为GatewayFilter局部过滤器和GlobalFilter全局过滤器

GatewayFilter : 需要通过spring.cloud.routes.filters 配置在具体路由下，只作用在当前路由上或通过spring.cloud.default-filters配置在全局，作用在所有路由上

GlobalFilter : 全局过滤器，不需要在配置文件中配置，作用在所有的路由上，最终通过GatewayFilterAdapter包装成GatewayFilterChain可识别的过滤器

# GatewayFilter局部过滤器

自定义局部过滤器需要实现`GatewayFilter` 和 `Ordered` 两个接口
```java
@Slf4j
public class CostomerGatewayFilter implements GatewayFilter, Ordered {
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        log.info("自定义局部过滤器：{}====================", "CustomerGatewayFilter");
        return chain.filter(exchange);
    }

    /**
     * 值越小，优先级越高
     *
     * @return
     */
    @Override
    public int getOrder() {
        return 0;
    }
}
```

在配置文件中使用自定义局部过滤器还需要使用自定义过滤器工厂来包装
这里的后缀`GatewayFilterFactory`不能写错，因为配置文件中配置的自定义过滤器名就是自定义过滤器工厂的类名去掉`GatewayFilterFactory`后缀的名字
把后缀写错了项目启动的时候就会报错说找不到这个自定义过滤器

```java
public class CustomerGatewayFilterFactory extends AbstractGatewayFilterFactory {
    @Override
    public GatewayFilter apply(Object config) {
        return new CostomerGatewayFilter();
    }
}
```

在配置类中将自定义过滤器工厂注册到容器中，当然也可以在自定义过滤器工厂类上加@Component注解
```java
@Configuration
public class GatewayConfig {

    @Bean
    public CustomerGatewayFilterFactory myGatewayFilterFactory() {
        return new CustomerGatewayFilterFactory();
    }

}
```

在配置文件中配置自定义过滤器，这里的`Customer`就是自定义过滤器工厂类名去掉`GatewayFilterFactory`后缀的名字
```java
spring:
  application:
    name: service-gateway
  cloud:
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848
    gateway:
      routes:
        - id: service-provider
          uri: lb://service-provider
          predicates:
            - Path=/provider/**
          filters:
            - Customer
```


# GlobalFilter全局过滤器

自定义全局过滤器需要实现 `GlobalFilter` 和 `Ordered` 接口
```java
@Slf4j
public class LoginFilter implements GlobalFilter, Ordered {
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        String path = request.getURI().getPath();
        String token = request.getHeaders().getFirst("token");
        log.info("访问的路径：{}", path);
        log.info("token: {}==================", token);

        if (token == null) {
            ServerHttpResponse response = exchange.getResponse();
            response.getHeaders().add("Content-Type", "application/json;charset=UTF-8");
            ResponseData responseData = new ResponseData(401, "请登录");
            String res = null;
            try {
                res = new ObjectMapper().writeValueAsString(responseData);
            } catch (JsonProcessingException e) {
                e.printStackTrace();
            }
            DataBuffer wrap = response.bufferFactory().wrap(res.getBytes(StandardCharsets.UTF_8));
            return response.writeWith(Mono.just(wrap));
        }
        return chain.filter(exchange);
    }

    @Override
    public int getOrder() {
        return 0;
    }
}
```

在配置类中注册全局过滤器，这样这个全局过滤器就是全局过滤了
```java
@Configuration
public class GatewayConfig {

    @Bean
    public GlobalFilter loginFilter() {
        return new LoginFilter();
    }
}
```
