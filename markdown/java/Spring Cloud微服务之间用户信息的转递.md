实现思路：
1. 准备一个ThreadLocal变量，供线程之间共享。
2. 每个微服对请求过滤，不管是经过网关的请求还是Feign的请求，如果是从网关过来的请求，从请求头中获取`token`并解析得到用户信息，然后存入`ThreadLocal`变量；如果是feign请求，直接获取请求头中的用户信息存入`ThreadLocal`中。
3. 每个微服务在使用Feign调用别的微服务时，先从ThreadLocal里面取出user信息，并放在request的请求头中。



ThreadLocal工具类：
```java
package com.orange.common.system;

import com.orange.common.entity.UserInfo;

public class UserInfoContext {
    private static ThreadLocal<UserInfo> userInfo = new ThreadLocal<>();
    public final static String FEIGN_HEADER_USERINFO = "X-FEIGN-HEADER-USERINFO";

    public static UserInfo getUser() {
        return (UserInfo) userInfo.get();
    }

    public static void setUser(UserInfo user) {
        userInfo.set(user);
    }
}

```

承载用户信息的实体类：
```java
package com.orange.common.entity;

import lombok.Data;

import java.io.Serializable;

@Data
public class UserInfo implements Serializable {
    private Long userId;
    private String username;
}
```

微服务的请求过滤器

```java
package com.orange.provider.component;


import com.alibaba.fastjson.JSON;
import com.orange.common.entity.UserInfo;
import com.orange.common.system.UserInfoContext;
import com.orange.common.util.JwtUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;

@Slf4j
@Component
@Order(1)
public class UserInfoFilter implements Filter {

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        initUserInfo((HttpServletRequest) servletRequest);
        filterChain.doFilter(servletRequest, servletResponse);
    }

    private void initUserInfo(HttpServletRequest request) {
        log.info("执行过滤器{}===================", "UserInfoFilter");
        String token = request.getHeader(JwtUtil.HEADER_TOKEN);
        log.info("获取请求头中的token：{}=======", token);
        String username = JwtUtil.getUsername(token);
        if (username != null) {
            UserInfo userInfo = new UserInfo();
            userInfo.setUsername(username);
            userInfo.setUserId(JwtUtil.getUserId(token));
            UserInfoContext.setUser(userInfo);
        }

        String userJson = request.getHeader(UserInfoContext.FEIGN_HEADER_USERINFO);
        log.info("获取feign请求头中的userInfo: {}=========", userJson);
        if (!StringUtils.isEmpty(userJson)) {
            UserInfo userInfo = JSON.parseObject(userJson, UserInfo.class);
            UserInfoContext.setUser(userInfo);
        }
    }
}

```

Feign请求拦截器
```java
package com.orange.consumer.config;

import com.alibaba.fastjson.JSON;
import com.orange.common.entity.UserInfo;
import com.orange.common.system.UserInfoContext;
import feign.RequestInterceptor;
import feign.RequestTemplate;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Configuration;

@Slf4j
@Configuration
public class FeignConfig implements RequestInterceptor {

    @Override
    public void apply(RequestTemplate requestTemplate) {
        log.info("feign请求拦截器============");
        //从应用上下文中取出user信息，放入Feign的请求头中
        UserInfo user = UserInfoContext.getUser();
        log.info("应用上下文中的UserInfo：{}",user);
        if (user != null) {
            String userJson = JSON.toJSONString(user);
            try {
                requestTemplate.header(UserInfoContext.FEIGN_HEADER_USERINFO, userJson);
            } catch (Exception e) {
                log.info("用户信息设置失败=========");
            }
        }
    }

}

```
        
