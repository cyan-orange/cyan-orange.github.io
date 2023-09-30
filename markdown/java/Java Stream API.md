# Stream API介绍
Stream API是Java8中处理集合的关键概念，它可以对集合执行非常复杂的操作：查找、过滤、映射等数据操作。

当我们使用一个流的时候，通常包括三个基本步骤：
1. 获取一个数据源（source）
1. 数据转换
1. 执行操作获取想要的结果。

每次转换原有 Stream 对象不改变，返回一个新的 Stream 对象（可以有多次转换），这就允许对其操作可以像链条一样排列。


# Stream实例化
一般常见创建Stream的三种方式


第一种：使用`Collection`下的`stream()`方法
```java
List<String> strings = new ArrayList<>();
Stream<String> stream = strings.stream();
```


第二种：使用**Arrays** 中的 **stream()** 静态方法，将数组转成流。
```java
int[] ints = new int[]{1, 3, 2, 6, 4};
IntStream stream = Arrays.stream(ints);
```


第三种：通过**Stream**类的静态方法**of()**。接收任意数量的参数。
```java
Stream<Integer> integerStream = Stream.of(1, 2, 3, 4, 5);
```


# 中间操作
Stream操作分为**中间**操作和**终止**操作，中间操作返回Stream
## 筛选与切片
**filter**：过滤流中的某些元素
**limit(n)**：获取n个元素
**skip(n)**：跳过n元素，配合limit(n)可实现分页
**distinct**：通过流中元素的 hashCode() 和 equals() 去除重复元素
```java
List<Integer> list = Arrays.asList(6, 4, 6, 7, 3, 9, 8, 10, 12, 14, 14);

//filter过滤去掉集合中小于7的数
list.stream().filter(integer -> integer >= 7).forEach(System.out::println);

//去掉重复元素
list.stream().distinct().forEach(integer -> System.out.println(integer));

//跳过前两个元素
list.stream().skip(2).forEach(System.out::println);

//获取三个元素
list.stream().limit(3).forEach(System.out::println);
```


## 映射
**map**：接收一个函数作为参数，将元素转换成其他形式或提取信息，该函数会被应用到每一个元素上，并将其映射成一个新的元素。**
```java
        List<Integer> list = Arrays.asList(1,2,3,4,5);

        //将集合中的每一个数加1
        list.stream().map(integer -> integer+1).forEach(System.out::println);
```
**flatMap**：接收一个函数作为参数，将流中的每一个值都换成一个流，然后把所有流连接成一个流。
```java
public class StreamAPI {

    public static void main(String[] args) {

        List<String> strings = Arrays.asList("abc", "def", "hij");

        //List<Character> collect = strings.stream().flatMap(StreamAPI::forStrToStream).collect(Collectors.toList());
        List<Character> characterList = strings.stream().flatMap(s -> forStrToStream(s)).collect(Collectors.toList());
        System.out.println(characterList);//[a, b, c, d, e, f, h, i, j]
    }

    //将字符串中的每一个字符构成的集合转换成Stream实例
    public static Stream<Character> forStrToStream(String str) {
        ArrayList<Character> characters = new ArrayList<>();
        for (Character c : str.toCharArray()) {
            characters.add(c);
        }
        return characters.stream();
    }
}
```


## 排序
**sorted()**：自然排序，流中元素需实现Comparable接口
**sorted(Comparator com)**：定制排序，自定义Comparator排序器
```java
List<Integer> list = Arrays.asList(6, 3, 4, 9);

//自然排序 Integer类自身已实现Compareable接口，所以可以自然排序
list.stream().sorted().forEach(integer -> System.out.println(integer));

//定制排序
list.stream().sorted((i1, i2) -> i1 - i2).forEach(System.out::println);
```


# 终止操作


## 匹配、聚合操作


**allMatch**：接收一个 Predicate 函数，当流中每个元素都符合该断言时才返回true，否则返回false
**noneMatch**：接收一个 Predicate 函数，当流中每个元素都不符合该断言时才返回true，否则返回false
**anyMatch**：接收一个 Predicate 函数，只要流中有一个元素满足该断言则返回true，否则返回false
**findFirst**：返回流中第一个元素
**findAny**：返回流中的任意元素
**count**：返回流中元素的总个数
**max**：返回流中元素最大值
**min**：返回流中元素最小值
```java
List<Integer> list = Arrays.asList(1, 2, 3, 4, 5);

boolean allMatch = list.stream().allMatch(e -> e > 10); //false
boolean noneMatch = list.stream().noneMatch(e -> e > 10); //true
boolean anyMatch = list.stream().anyMatch(e -> e > 4);  //true

Integer findFirst = list.stream().findFirst().get(); //1
Integer findAny = list.stream().findAny().get(); //1

long count = list.stream().count(); //5
Integer max = list.stream().max(Integer::compareTo).get(); //5
```


## 规约
Optional<T> reduce(BinaryOperator<T> accumulator)：有初始值，可以将流中的元素反复结合起来，得到一个值，返回一个T
T reduce(T identity, BinaryOperator<T> accumulator)：可以将流中的元素反复结合起来，得到一个值，返回一个T

```java
List<Integer> list = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

//初始值为10
Integer v1 = list.stream().reduce(10, (x1, x2) -> x1 + x2);
System.out.println(v1);  //65

//没有初始值
Integer v = list.stream().reduce((x1, x2) -> x1 + x2).get();
System.out.println(v);   // 55

```


## 收集


**collect(Collector)**：将Stream转换为其他形式。接收一个Collector接口的实现，用于给Stream中元素做汇总的方法
```java
List<Integer> list = Arrays.asList(6, 4, 6, 7, 3, 9, 8, 10, 12, 14, 14);

//收集为list集合
List<Integer> toList = list.stream().filter(integer -> integer >= 7).collect(Collectors.toList());

//收集为set集合
Set<Integer> toSet = list.stream().distinct().collect(Collectors.toSet());
```
        
