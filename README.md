# MySQL变量

确保要更新表user中name相同的记录的age字段为递增值，你可以使用MySQL的变量和子查询来实现。

以下是一个实现该需求的更新语句示例：

```sql
SET @currentName := '';
SET @increment := 0;

UPDATE user
SET age = (
  CASE
    WHEN @currentName = name THEN (@increment := @increment + 1)
    WHEN (@currentName := name) IS NOT NULL THEN (@increment := 1)
  END
)
ORDER BY name;
```

这个更新语句使用了两个变量：@currentName用于存储当前正在处理的name值，@increment用于存储递增的值。初始时，两个变量都被设定为初始值。

在更新语句中，使用了CASE表达式来根据当前记录的name值和之前记录的name值进行判断。当当前记录的name值和上一条记录的name值相同时，@increment递增；当当前记录的name值和上一条记录的name值不同时，将@increment重置为1。

通过使用ORDER BY name子句，确保按照name字段的升序对记录进行更新，这样相同name的记录才会递增更新age字段。

请注意，在执行这个更新语句之前，建议对数据进行备份或在测试环境中执行，以确保语句的正确性和你的预期结果。

# HTML入门

学习前端的网站 [[MDN Web Docs](https://developer.mozilla.org/zh-CN/)]()

![b175e45d-175a-4ee3-afe6-efe413a91ae6](./images/b175e45d-175a-4ee3-afe6-efe413a91ae6.png)

HTML结构

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
</body>
</html>
```
