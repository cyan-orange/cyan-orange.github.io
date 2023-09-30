# JWT是什么
JSON Web Token (JWT)是一个开放标准(RFC 7519)，它定义了一种紧凑的、自包含的方式，用于作为JSON对象在各方之间安全地传输信息。该信息可以被验证和信任，因为它是数字签名的。

JSON Web Token由三部分组成，头部、载荷与签名,它们之间用点`.`连接
- Header
- Payload
- Signature

## Header
Header典型的由两部分组成：token的类型（“JWT”）和算法名称（比如：HMAC SHA256或者RSA等等）
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
Header会被Base64Url编码为JWT的第一部分

## Payload
Payload是有关实体（通常是用户）和其他数据的声明，它包含三部分
**（1）注册声明**
这些是一组预定义的权利要求，不是强制性的，而是建议使用的，以提供一组有用的可互操作的权利要求。其中一些是： iss（JWT的签发者）， exp（expires,到期时间）， sub（主题）， aud（JWT接收者），iat(issued at，签发时间)等。

**（2）公开声明**
公共的声明可以添加任何的信息，一般添加用户的相关信息或其他业务需要的必要信息.但不建议添加敏感信息，因为该部分在客户端可解密。

**（3）私有声明**
私有声明是提供者和消费者所共同定义的声明，一般不建议存放敏感信息，因为base64是对称解密的，意味着该部分信息可以归类为明文信息。

```json
{ "iat": 1593955943,
  "exp": 1593955973,
  "uid": 10,
  "username": "test",
  "scopes": [ "admin", "user" ]
}
```
Payload会被Base64Url编码为JWT的第二部分

## Signature
Signature由base64加密后的header和base64加密后的payload使用.连接组成的字符串，然后通过header中声明的加密方式进行加盐secret组合加密而成

将这三个部分用`.`连接就构成了JWT

# 使用JWT
加入依赖
```xml
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt</artifactId>
    <version>0.9.0</version>
</dependency>

<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>fastjson</artifactId>
    <version>1.2.47</version>
</dependency>
```


jwt工具类
```java
package com.zkzx.zkconsult.util;

import io.jsonwebtoken.*;
import org.springframework.util.StringUtils;

import java.util.Date;

public class JwtUtil {
    //过期时间单位毫秒ms
    private static final long tokenExpiration = 24 * 60 * 60 * 1000;//一天
    //签名密钥
    private static final String tokenSignKey = "83c85bd9-e97a-479f-96f4-b347f5490bcb";

    private static final String USER_ID = "userId";
    private static final String USERNAME = "username";

    /**
     * 根据用户信息生成token
     *
     * @param userId
     * @param username
     * @return token
     */
    public static String createToken(Long userId, String username) {
        JwtBuilder builder = Jwts.builder();
        builder
                /*设置标识*/
                .setId("orange")
                /*主体*/
                .setSubject("lemon")
                /*签发时间*/
                .setIssuedAt(new Date())
                /*设置密钥*/
                .signWith(SignatureAlgorithm.HS256, tokenSignKey)
                /*过期时间*/
                .setExpiration(new Date(System.currentTimeMillis() + tokenExpiration))
                /*设计用户信息*/
                .claim(USER_ID, userId)
                .claim(USERNAME, username);

        String token = builder.compact();

        return token;

    }

    /**
     * 获取Claims 部分内容（即要传的信息）
     *
     * @param token
     * @return
     */
    public static Claims getClaim(String token) {
        Claims claims = null;
        try {
            claims = Jwts.parser()
                    .setSigningKey(tokenSignKey)
                    .parseClaimsJws(token)
                    .getBody();
        } catch (Exception e) {
            return null;
        }
        return claims;
    }

    /**
     * 根据token字符串返回用户ID
     *
     * @param token
     * @return userId
     */
    public static Long getUserId(String token) {
        if (StringUtils.isEmpty(token)) {
            return null;
        }
        Claims claims = getClaim(token);
        if (claims == null) {
            return null;
        }
        Long userId = Long.valueOf(String.valueOf(claims.get(USER_ID)));
        return userId;
    }

    /**
     * 根据token字符串返回用户名 username
     *
     * @param token
     * @return username
     */
    public static String getUsername(String token) {
        if (StringUtils.isEmpty(token)) {
            return null;
        }
        Claims claims = getClaim(token);
        if (claims == null) {
            return null;
        }
        String username = String.valueOf(claims.get(USERNAME));
        return username;
    }


    /**
     * 验证token是否有效
     *
     * @param token
     * @return true:有效   false:无效
     */
    public static boolean validation(String token) {
        if (StringUtils.isEmpty(token)) {
            return false;
        }
        Claims claims = getClaim(token);
        if (claims == null) {
            return false;
        }
        return true;
    }

    public static String flushedToken(String token) {
        return createToken(getUserId(token), getUsername(token));
    }

}
```


拦截器
```java
package com.zkzx.zkconsult.interceptor;

import com.alibaba.fastjson.JSON;
import com.zkzx.zkconsult.constant.CodeMessageEnum;
import com.zkzx.zkconsult.dto.response.ResponseData;
import com.zkzx.zkconsult.util.JwtUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.PrintWriter;

@Slf4j
public class MyLoginInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String token = request.getHeader("X-Token");
        log.info("token：{}", token);

        response.setCharacterEncoding("UTF-8");
        if (JwtUtil.validation(token)) {
            return true;
        }
        response.setContentType("application/json; charset=utf-8");
        Object json = JSON.toJSON(new ResponseData<Void>(CodeMessageEnum.TOKEN_ERROR));
        PrintWriter writer = response.getWriter();
        writer.write(json.toString());
        return false;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {

    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {

    }
}
```


配置拦截器
```java
package com.zkzx.zkconsult.config;

import com.zkzx.zkconsult.interceptor.MyLoginInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new MyLoginInterceptor())
                .addPathPatterns("/**")  //所有请求都被拦截包括静态资源
                .excludePathPatterns("/user/login", "/user/getPassword/**"); //放行的请求
    }
}
```
        
