
Java 集合就像一种容器，可以动态地把多个对象的引用放入容器中。


# 数组与集合的比较


数组在内存存储方面的特点：


- 数组初始化以后，长度就确定了。
- 数组声明的类型，就决定了进行元素初始化时的类型



数组在存储数据方面的弊端：

1. 数组初始化以后，长度就不可变了，不便于扩展
2. 数组中提供的属性和方法少，不便于进行添加、删除、插入等操作，且效率不高。同时无法直接获取存储元素的个数
3. 数组存储的数据是有序的、可以重复的。存储数据的特点单一



Java 集合类可以用于存储数量不等的多个对象，还可用于保存具有映射关系的
关联数组。


# 集合框架概述


Java 集合可分为 Collection 和 Map 两种体系：

1. Collection接口：单列数据，定义了存取一组对象的方法的集合
   - List：元素有序、可重复的集合
   - Set：元素无序、不可重复的集合
2. Map接口：双列数据，保存具有映射关系“key-value对”的集合



# List接口概述


1. 鉴于Java中数组用来存储数据的局限性，我们通常使用List替代数组
2. List集合类中元素有序、且可重复，集合中的每个元素都有其对应的顺序索引。
3. List容器中的元素都对应一个整数型的序号记载其在容器中的位置，可以根据序号存取容器中的元素。
4. JDK API中List接口的实现类常用的有：ArrayList、LinkedList和Vector。



## ArrayList


1. ArrayList 是 List 接口的典型实现类、主要实现类
2. 本质上，ArrayList是对象引用的一个”变长”数组
3. ArrayList的JDK1.8之前与之后的实现区别？
   1. JDK1.7：ArrayList像饿汉式，直接创建一个初始容量为10的数组
   2. JDK1.8：ArrayList像懒汉式，一开始创建一个长度为0的数组，当添加第一个元素时再创建一个始容量为10的数组
4. Arrays.asList(…) 方法返回的 List 集合，既不是 ArrayList 实例，也不是Vector 实例。 Arrays.asList(…) 返回值是一个固定长度的 List 集合



**扩容机制**


如果添加到底层数组容量不够，则扩容。默认情况下，扩容为原来的容量的1.5倍，同时需要将原有数组中的数据复制到新的数组中。


## LinkedList


对于频繁的插入或删除元素的操作，建议使用LinkedList类，效率较高


LinkedList：双向链表，实现了List接口和Deque接口, 内部没有声明数组，而是定义了Node类型的first和last，用于记录首末元素。同时，定义内部类Node，作为LinkedList中保存数据的基本结构。Node除了保存数据，还定义了两个变量：


1. prev变量记录前一个元素的位置
2. next变量记录下一个元素的位置



```java
private static class Node<E> {
    E item;
    Node<E> next;
    Node<E> prev;
    Node(Node<E> prev, E element, Node<E> next) {
        this.item = element;
        this.next = next;
        this.prev = prev;
    }
}
```


## Vector


Vector 是一个古老的集合，JDK1.0就有了。大多数操作与ArrayList相同，区别之处在于Vector是线程安全的。
在各种list中，最好把ArrayList作为缺省选择。当插入、删除频繁时，使用LinkedList；Vector总是比ArrayList慢，所以尽量避免使用。


Vector每次扩容请求其大小的2倍空间


## ArrayList和LinkedList的区别


1. 二者都线程不安全，相对线程安全的Vector，执行效率高。
2. ArrayList是实现了基于动态数组的数据结构，LinkedList基于链表的数据结构。对于随机访问get和set，ArrayList觉得优于LinkedList，因为LinkedList要移动指针。
3. 对于新增和删除操作add(特指插入)和remove，LinkedList比较占优势，因为ArrayList要移动数据。



## ArrayList和Vector的区别


Vector和ArrayList几乎是完全相同的,唯一的区别在于Vector是同步类(synchronized)，属于强同步类。因此开销就比ArrayList要大，访问要慢。正常情况下,大多数的Java程序员使用ArrayList而不是Vector,因为同步完全可以由程序员自己来控制。Vector每次扩容请求其大小的2倍空间，而ArrayList是1.5倍。Vector还有一个子类Stack。


# Set 接口概述


1. Set接口是Collection的子接口，set接口没有提供额外的方法
2. Set 集合不允许包含相同的元素，如果试把两个相同的元素加入同一个Set 集合中，则添加操作失败。
3. Set 判断两个对象是否相同不是使用 == 运算符，而是根据 equals() 方法



## HashSet


1. HashSet 是 Set 接口的典型实现，大多数时候使用 Set 集合时都使用这个实现类。
2. HashSet 按 Hash 算法来存储集合中的元素，因此具有很好的存取、查找、删除性能。
3. HashSet 具有以下特点：
   1. 不能保证元素的排列顺序
   2. HashSet 不是线程安全的
   3. 集合元素可以是 null
4. HashSet 集合判断两个元素相等的标准：两个对象通过 hashCode() 方法比较相等，并且两个对象的 equals() 方法返回值也相等。
5. 对于存放在Set容器中的对象，对应的类一定要重写equals()和hashCode(Object obj)方法，以实现对象相等规则。即：“相等的对象必须具有相等的散列码”。
6. `HashSet`底层也是数组，初始容量为16，当如果使用率超过0.75（16*0.75=12）, 就会扩大容量为原来的2倍。（16扩容为32，依次为64,128....等）



### 添加元素的过程：


1. 当向 HashSet 集合中存入一个元素时，HashSet 会调用该对象的 `hashCode()` 方法来得到该对象的 hashCode 值，然后根据 hashCode 值，通过某种散列函数决定该对象在 HashSet 底层数组中的存储位置。（这个散列函数会与底层数组的长度相计算得到在数组中的下标，并且这种散列函数计算还尽可能保证能均匀存储元素，越是散列分布，该散列函数设计的越好）
   1. 如果两个元素的hashCode()值相等，会再继续调用equals方法，如果equals方法结果
      为true，添加失败；如果为false，那么会保存该元素，但是该数组的位置已经有元素了，
      那么会通过链表的方式继续链接。
   2. 如果它们的 hashCode() 返回值不相等，但两个元素的 equals() 方法返回 true，hashSet 将会把它们存储在不同的位置，但依然可以添加成功。



## LinkedHashSet


1. LinkedHashSet 是 HashSet 的子类
2. LinkedHashSet 根据元素的 hashCode 值来决定元素的存储位置，但它同时使用双向链表维护元素的次序，这使得元素看起来是以插入顺序保存的。
3. LinkedHashSet插入性能略低于 HashSet，但在迭代访问 Set 里的全部元素时有很好的性能。
4. LinkedHashSet 不允许集合元素重复。



## TreeSet


因为只有相同类的两个实例才会比较大小，所以向 TreeSet 中添加的应该是同一个类的对象


1. TreeSet 是 SortedSet 接口的实现类，TreeSet 可以确保集合元素处于排序状态。
2. TreeSet底层使用红黑树结构存储数据
3. TreeSet 两种排序方法：自然排序和定制排序。默认情况下，TreeSet 采用自然排序。



### 自然排序


**第一种排序方式：**
**

1. 自然排序：TreeSet 会调用集合元素的 `compareTo(Object obj)` 方法来比较元素之间的大小关系，然后将集合元素按升序(默认情况)排列
2. 如果试图把一个对象添加到 TreeSet 时，则该对象的类必须实现 `Comparable`接口。
   1. 实现 `Comparable`的类必须实现 `compareTo(Object obj)` 方法，两个对象即通过`compareTo(Object obj)`方法的返回值来比较大小。
3. Comparable 的典型实现：
   1. `BigDecimal`、`BigInteger` 以及所有的数值型对应的包装类：按它们对应的数值大小进行比较
   2. `Character`：按字符的 unicode值来进行比较
   3. `Boolean`：true 对应的包装类实例大于 false 对应的包装类实例
   4. `String`：按字符串中字符的 unicode 值进行比较
   5. `Date`、`Time`：后边的时间、日期比前面的时间、日期大



**第二种排序方式**


1. TreeSet 中添加元素时，只有第一个元素无须比较compareTo()方法，后面添加的所有元素都会调用compareTo()方法进行比较。
2. 因为只有相同类的两个实例才会比较大小，所以向 TreeSet 中添加的应该是同一个类的对象。
3. 对于 TreeSet 集合而言，它判断两个对象是否相等的唯一标准是：两个对象通过 compareTo(Object obj) 方法比较返回值。
4. 当需要把一个对象放入 TreeSet 中，重写该对象对应的 equals() 方法时，应保证该方法与 compareTo(Object obj) 方法有一致的结果：如果两个对象通过equals() 方法比较返回 true，则通过 compareTo(Object obj) 方法比较应返回 0。否则，让人难以理解。



### 定制排序


1. TreeSet的自然排序要求元素所属的类实现Comparable接口，如果元素所属的类没有实现Comparable接口，或不希望按照升序(默认情况)的方式排列元素或希望按照其它属性大小进行排序，则考虑使用定制排序。定制排序，通过Comparator接口来实现。需要重写compare(T o1,T o2)方法。
2. 利用int compare(T o1,T o2)方法，比较o1和o2的大小：如果方法返回正整数，则表示o1大于o2；如果返回0，表示相等；返回负整数，表示o1小于o2。
3. 要实现定制排序，需要将实现Comparator接口的实例作为形参传递给TreeSet的构造器。
4. 此时，仍然只能向TreeSet中添加类型相同的对象。否则发生ClassCastException异常。
5. 使用定制排序判断两个元素相等的标准是：通过Comparator比较两个元素返回了0。



# Map接口概述


1. Map与Collection并列存在。用于保存具有映射关系的数据:key-value
2. Map 中的 key 和 value 都可以是任何引用类型的数据
3. Map 中的 key 用Set来存放，不允许重复，即同一个 Map 对象所对应的类，须重写hashCode()和equals()方法
4. 常用String类作为Map的“键”
5. key 和 value 之间存在单向一对一关系，即通过指定的 key 总能找到唯一的、确定的 value
6. Map接口的常用实现类：`HashMap`、`TreeMap`、`LinkedHashMap`和`Properties`。其中，HashMap是 Map 接口使用频率最高的实现类



## HashMap


1. HashMap是 Map 接口使用频率最高的实现类。
2. 允许使用null键和null值，与HashSet一样，不保证映射的顺序。
3. 所有的key构成的集合是Set:无序的、不可重复的。所以，key所在的类要重写：equals()和hashCode()
4. 所有的value构成的集合是Collection:无序的、可以重复的。所以，value所在的类要重写：equals()
5. 一个key-value构成一个entry
6. 所有的entry构成的集合是Set:无序的、不可重复的
7. HashMap 判断两个 key 相等的标准是：两个 key 通过 equals() 方法返回 true，hashCode 值也相等。
8. HashMap 判断两个 value相等的标准是：两个 value 通过 equals() 方法返回 true。



### HashMap的存储结构


**JDK 7及以前版本：HashMap是数组+链表结构(即为链地址法)**


1. HashMap的内部存储结构其实是数组和链表的结合。当实例化一个HashMap时，系统会创建一个长度为Capacity的Entry数组，这个长度在哈希表中被称为容量(Capacity)，在这个数组中可以存放元素的位置我们称之为“桶”(bucket)，每个bucket都有自己的索引，系统可以根据索引快速的查找bucket中的元素。
2. 每个bucket中存储一个元素，即一个Entry对象，但每一个Entry对象可以带一个引用变量，用于指向下一个元素，因此，在一个桶中，就有可能生成一个Entry链。而且新添加的元素作为链表的head。
3. 添加元素的过程：
   向HashMap中添加entry1(key，value)，需要首先计算entry1中key的哈希值(根据key所在类的hashCode()计算得到)，此哈希值经过处理以后，得到在底层Entry[]数组中要存储的位置i。如果位置i上没有元素，则entry1直接添加成功。如果位置i上已经存在entry2(或还有链表存在的entry3，entry4)，则需要通过循环的方法，依次比较entry1中key和其他的entry。如果彼此hash值不同，则直接添加成功。如果hash值不同，继续比较二者是否equals。如果返回值为true，则使用entry1的value去替换equals为true的entry的value。如果遍历一遍以后，发现所有的equals返回都为false,则entry1仍可添加成功。entry1指向原有的entry元素。



**JDK 1.8之前HashMap的扩容**


当HashMap中的元素越来越多的时候，hash冲突的几率也就越来越高，因为数组的长度是固定的。所以为了提高查询的效率，就要对HashMap的数组进行扩容，而在HashMap数组扩容之后，最消耗性能的点就出现了：原数组中的数据必须重新计算其在新数组中的位置，并放进去，这就是resize。


那么HashMap什么时候进行扩容呢？
当HashMap中的元素个数超过数组大小(数组总大小length,不是数组中个数size)_loadFactor 时 ， 就 会 进 行 数 组 扩 容 ， loadFactor 的默认 值`(DEFAULT_LOAD_FACTOR)`为`0.75`，这是一个折中的取值。也就是说，默认情况，数组大小`(DEFAULT_INITIAL_CAPACITY)`为16，那么当HashMap中元素个数超过16_0.75=12（这个值就是代码中的threshold值，也叫做临界值）的时候，就把数组的大小扩展为 2*16=32，即扩大一倍，然后重新计算每个元素在数组中的位置，而这是一个非常消耗性能的操作，所以如果我们已经预知HashMap中元素的个数，那么预设元素的个数能够有效的提高HashMap的性能。


**JDK 8版本发布以后：HashMap是数组+链表+红黑树实现。**


1. HashMap的内部存储结构其实是数组+链表+树的结合。当实例化一个HashMap时，会初始化initialCapacity和loadFactor，在put第一对映射关系时，系统会创建一个长度为initialCapacity的Node数组，这个长度在哈希表中被称为容量(Capacity)，在这个数组中可以存放元素的位置我们称之为“桶”(bucket)，每个bucket都有自己的索引，系统可以根据索引快速的查找bucket中的元素。
2. 每个bucket中存储一个元素，即一个Node对象，但每一个Node对象可以带一个引用变量next，用于指向下一个元素，因此，在一个桶中，就有可能生成一个Node链。也可能是一个一个TreeNode对象，每一个TreeNode对象可以有两个叶子结点left和right，因此，在一个桶中，就有可能生成一个TreeNode树。而新添加的元素作为链表的last，或树的叶子结点。



### 那么 JDK1.8 HashMap什么时候进行扩容和树形化呢？


当HashMap中的元素个数超过数组大小(数组总大小length,不是数组中个数size)_loadFactor 时 ， 就会进行数组扩容 ， loadFactor 的默认 值(DEFAULT_LOAD_FACTOR)为0.75，这是一个折中的取值。也就是说，默认情况下，数组大小(DEFAULT_INITIAL_CAPACITY)为16，那么当HashMap中元素个数超过16_0.75=12（这个值就是代码中的threshold值，也叫做临界值）的时候，就把数组的大小扩展为 2*16=32，即扩大一倍，然后重新计算每个元素在数组中的位置，而这是一个非常消耗性能的操作，所以如果我们已经预知HashMap中元素的个数，那么预设元素的个数能够有效的提高HashMap的性能。当HashMap中的其中一个链的对象个数如果达到了8个，此时如果capacity没有达到64，那么HashMap会先扩容解决，如果已经达到了64，那么这个链会变成树，结点类型由Node变成TreeNode类型。当然，如果当映射关系被移除后，下次resize方法时判断树的结点个数低于6个，也会把树再转为链表。






### 负载因子值的大小，对HashMap有什么影响


1. 负载因子的大小决定了HashMap的数据密度。
2. 负载因子越大密度越大，发生碰撞的几率越高，数组中的链表越容易长,造成查询或插入时的比较次数增多，性能会下降。
3. 负载因子越小，就越容易触发扩容，数据密度也越小，意味着发生碰撞的几率越小，数组中的链表也就越短，查询和插入时比较的次数也越小，性能会更高。但是会浪费一定的内容空间。而且经常扩容也会影响性能，建议初始化预设大一点的空间。
4. 按照其他语言的参考及研究经验，会考虑将负载因子设置为0.7~0.75，此时平均检索长度接近于常数。



# LinkedHashMap


1. LinkedHashMap 是 HashMap 的子类
2. 在HashMap存储结构的基础上，使用了一对双向链表来记录添加元素的顺序
3. 与LinkedHashSet类似，LinkedHashMap 可以维护 Map 的迭代顺序：迭代顺序与 Key-Value 对的插入顺序一致



`HashMap`中的内部类：Node


```java
static class Node<K,V> implements Map.Entry<K,V> {
    final int hash;
    final K key;
    V value;
    Node<K,V> next;
}
```


`LinkedHashMap`中的内部类：Entry


```java
static class Entry<K,V> extends HashMap.Node<K,V> {
    Entry<K,V> before, after;
    Entry(int hash, K key, V value, Node<K,V> next) {
    	super(hash, key, value, next);
    }
}
```


# TreeMap


TreeMap 的所有的 Key 必须实现 Comparable 接口，而且所有的 Key 应该是同一个类的对象，否则将会抛出 ClasssCastException


1. TreeMap存储 Key-Value 对时，需要根据 key-value 对进行排序。TreeMap 可以保证所有的 Key-Value 对处于有序状态。
2. TreeSet底层使用红黑树结构存储数据
3. TreeMap 的 Key 的排序：
   1. 自然排序：TreeMap 的所有的 Key 必须实现 Comparable 接口，而且所有的 Key 应该是同一个类的对象，否则将会抛出 ClasssCastException
   2. 定制排序：创建 TreeMap 时，传入一个 Comparator 对象，该对象负责对TreeMap 中的所有 key 进行排序。此时不需要 Map 的 Key 实现Comparable 接口
   3. TreeMap判断两个key相等的标准：两个key通过compareTo()方法或者compare()方法返回0。



# Hashtable


1. Hashtable是个古老的 Map 实现类，JDK1.0就提供了。不同于HashMap，Hashtable是线程安全的。
2. Hashtable实现原理和HashMap相同，功能相同。底层都使用哈希表结构，查询速度快，很多情况下可以互用。
3. 与HashMap不同，Hashtable 不允许使用 null 作为 key 和 value
4. 与HashMap一样，Hashtable 也不能保证其中 Key-Value 对的顺序
5. Hashtable判断两个key相等、两个value相等的标准，与HashMap一致。



# Properties


1. Properties 类是 Hashtable 的子类，该对象用于处理属性文件
2. 由于属性文件里的 key、value 都是字符串类型，所以 Properties 里的 key 和 value 都是字符串类型
3. 存取数据时，建议使用setProperty(String key,String value)方法和getProperty(String key)方法



```java
//Properties:常用来处理配置文件。key和value都是String类型
public static void main(String[] args)  {
    FileInputStream fis = null;
    try {
        Properties pros = new Properties();

        fis = new FileInputStream("jdbc.properties");
        pros.load(fis);//加载流对应的文件

        String name = pros.getProperty("name");
        String password = pros.getProperty("password");

    } catch (IOException e) {
        e.printStackTrace();
    } finally {
        if(fis != null){
            try {
                fis.close();
            } catch (IOException e) {
                e.printStackTrace();
            }

        }
    }
```
