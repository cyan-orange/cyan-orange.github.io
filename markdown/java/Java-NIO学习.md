
# I/O 模型基本说明

I/O 模型：就是用什么样的通道或者说是通信模式和架构进行数据的传输和接收，很大程度上决定了程序通信的性能，Java 共支持 3 种网络编程的/IO 模型：**BIO、NIO、AIO**
实际通信需求下，要根据不同的业务场景和性能需求决定选择不同的I/O模型


##  Java BIO

同步并阻塞(传统阻塞型)，服务器实现模式为一个连接一个线程，即客户端有连接请求时服务器
端就需要启动一个线程进行处理，如果这个连接不做任何事情会造成不必要的线程开销


## Java NIO

Java NIO ： 同步非阻塞，服务器实现模式为一个线程处理多个请求(连接)，即客户端发送的连接请求都会注
册到多路复用器上，多路复用器轮询到连接有 I/O 请求就进行处理

##  Java AIO

Java AIO(NIO.2) ： 异步 异步非阻塞，服务器实现模式为一个有效请求一个线程，客户端的I/O请求都是由OS先完成了再通知服务器应用去启动线程进行处理，一般适用于连接数较多且连接时间较长的应用

## BIO、NIO、AIO 适用场景分析

1. **BIO** 方式适用于连接数目比较小且固定的架构，这种方式对服务器资源要求比较高，并发局限于应用中，JDK1.4以前的唯一选择，但程序简单易理解。
2. **NIO** 方式适用于连接数目多且连接比较短（轻操作）的架构，比如聊天服务器，弹幕系统，服务器间通讯等。编程比较复杂，JDK1.4 开始支持。
3. AIO 方式使用于连接数目多且连接比较长（重操作）的架构，比如相册服务器，充分调用 OS 参与并发操作，编程比较复杂，JDK7 开始支持。

# Java BIO深入剖析


* Java BIO 就是传统的 java io  编程，其相关的类和接口在 java.io
* BIO(blocking I/O) ： 同步阻塞，服务器实现模式为一个连接一个线程，即客户端有连接请求时服务器端就需要启动一个线程进行处理，如果这个连接不做任何事情会造成不必要的线程开销，可以通过线程池机制改善(实现多个客户连接服务器).

##  BIO 工作机制

1) 服务器端启动一个 **ServerSocket**，注册端口，调用accpet方法监听客户端的Socket连接。
2) 客户端启动 **Socket** 对服务器进行通信，默认情况下服务器端需要对每个客户 建立一个线程与之通讯

## 传统的BIO编程实例

网络编程的基本模型是Client/Server模型，也就是两个进程之间进行相互通信，其中服务端提供位置信（绑定IP地址和端口），客户端通过连接操作向服务端监听的端口地址发起连接请求，基于TCP协议下进行三次握手连接，连接成功后，双方通过网络套接字（Socket）进行通信。
传统的同步阻塞模型开发中，服务端ServerSocket负责绑定IP地址，启动监听端口；客户端Socket负责发起连接操作。连接成功后，双方通过输入和输出流进行同步阻塞式通信。
基于BIO模式下的通信，客户端 - 服务端是完全同步，完全耦合的。

客户端案例如下

```java
public static void main(String[] args) throws Exception {
    System.out.println("==客户端的启动==");
    // （1）创建一个Socket的通信管道，请求与服务端的端口连接。
    Socket socket = new Socket("127.0.0.1", 8888);
    // （2）从Socket通信管道中得到一个字节输出流。
    OutputStream os = socket.getOutputStream();
    // （3）把字节流改装成自己需要的流进行数据的发送
    PrintStream ps = new PrintStream(os);
    // （4）开始发送消息
    ps.println("我是客户端，我想约你吃小龙虾！！！");
    ps.flush();
}
```

服务端案例如下

```java
public static void main(String[] args) throws Exception {
    // （1）注册端口
    ServerSocket serverSocket = new ServerSocket(8888);
    //（2）开始在这里暂停等待接收客户端的连接,得到一个端到端的Socket管道
    Socket socket = serverSocket.accept();
    //（3）从Socket管道中得到一个字节输入流。
    InputStream is = socket.getInputStream();
    //（4）把字节输入流包装成自己需要的流进行数据的读取。
    BufferedReader br = new BufferedReader(new InputStreamReader(is));
    //（5）读取数据
    String line ;
    while((line = br.readLine())!=null){
        System.out.println("服务端收到："+line);
    }
}
```



* 在以上通信中，服务端会一致等待客户端的消息，如果客户端没有进行消息的发送，服务端将一直进入阻塞状态。
* 同时服务端是按照行获取消息的，这意味着客户端也必须按照行进行消息的发送，否则服务端将进入等待消息的阻塞状态！

## BIO模式下多发和多收消息

客户端代码如下

```java
public static void main(String[] args) throws Exception {
    System.out.println("==客户端的启动==");
    // （1）创建一个Socket的通信管道，请求与服务端的端口连接。
    Socket socket = new Socket("127.0.0.1", 8888);
    // （2）从Socket通信管道中得到一个字节输出流。
    OutputStream os = socket.getOutputStream();
    // （3）把字节流改装成自己需要的流进行数据的发送
    PrintStream ps = new PrintStream(os);
    // （4）开始发送消息
    Scanner sc = new Scanner(System.in);
    while (true) {
        System.out.print("请说:");
        String msg = sc.nextLine();
        ps.println(msg);
        ps.flush();
    }
}
```

服务端代码如下

```java
package com.itheima._03bio02;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * 服务端
 */
public class ServerDemo {
    public static void main(String[] args) throws Exception {
        String s = "886";
        System.out.println("886".equals(s));
        System.out.println("==服务器的启动==");
        //（1）注册端口
        ServerSocket serverSocket = new ServerSocket(8888);
        //（2）开始在这里暂停等待接收客户端的连接,得到一个端到端的Socket管道
        Socket socket = serverSocket.accept();
        //（3）从Socket管道中得到一个字节输入流。
        InputStream is = socket.getInputStream();
        //（4）把字节输入流包装成  自己需要的流进行数据的读取。
        BufferedReader br = new BufferedReader(new InputStreamReader(is));
        //（5）读取数据
        String line ;
        while((line = br.readLine())!=null){
            System.out.println("服务端收到："+line);
        }
    }
}
```



* 本案例中确实可以实现客户端多发多收
* 但是服务端只能处理一个客户端的请求，因为服务端是单线程的。一次只能与一个客户端进行消息通信。

## BIO模式下接收多个客户端


在上述的案例中，一个服务端只能接收一个客户端的通信请求，**那么如果服务端需要处理很多个客户端的消息通信请求应该如何处理呢**，此时我们就需要在服务端引入线程了，也就是说客户端每发起一个请求，服务端就创建一个新的线程来处理这个客户端的请求，这样就实现了一个客户端一个线程的模型

客户端案例代码如下

```java
/**
    客户端
 */
public class ClientDemo {
    public static void main(String[] args) throws Exception {
        // （1）创建一个Socket的通信管道，请求与服务端的端口连接。
        Socket socket = new Socket("127.0.0.1",7777);
        // （2）从Socket通信管道中得到一个字节输出流。
        OutputStream os = socket.getOutputStream();
        // （3）把字节流改装成自己需要的流进行数据的发送
        PrintStream ps = new PrintStream(os);
        // （4）开始发送消息
        Scanner sc = new Scanner(System.in);
        while(true){
            System.out.print("请说:");
            String msg = sc.nextLine();
            ps.println(msg);
            ps.flush();
        }
    }
}
```

服务端案例代码如下

```java
/**
    服务端
 */
public class ServerDemo {
    public static void main(String[] args) throws Exception {
        // （1）注册端口
        ServerSocket serverSocket = new ServerSocket(7777);
        while (true) {
            //（2）开始在这里暂停等待接收客户端的连接,得到一个端到端的Socket管道
            Socket socket = serverSocket.accept();
            new ServerReadThread(socket).start();
            System.out.println(socket.getRemoteSocketAddress() + "上线了！");
        }
    }

}

class ServerReadThread extends Thread {
    private Socket socket;

    public ServerReadThread(Socket socket) {
        this.socket = socket;
    }

    @Override
    public void run() {
        try {
            //（3）从Socket管道中得到一个字节输入流。
            InputStream is = socket.getInputStream();
            //（4）把字节输入流包装成自己需要的流进行数据的读取。
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            //（5）读取数据
            String line;
            while ((line = br.readLine()) != null) {
                System.out.println("服务端收到：" + socket.getRemoteSocketAddress() + ":" + line);
            }
        } catch (Exception e) {
            System.out.println(socket.getRemoteSocketAddress() + "下线了！");
        }
    }
}
```

小结:

* 1.每个Socket接收到，都会创建一个线程，线程的竞争、切换上下文影响性能；
* 2.每个线程都会占用栈空间和CPU资源；
* 3.并不是每个socket都进行IO操作，无意义的线程处理；
* 4.客户端的并发访问增加时。服务端将呈现1:1的线程开销，访问量越大，系统将发生线程栈溢出，线程创建失败，最终导致进程宕机或者僵死，从而不能对外提供服务。

## 伪异步I/O编程

在上述案例中：客户端的并发访问增加时。服务端将呈现1:1的线程开销，访问量越大，系统将发生线程栈溢出，线程创建失败，最终导致进程宕机或者僵死，从而不能对外提供服务。
接下来我们采用一个伪异步I/O的通信框架，采用线程池和任务队列实现，当客户端接入时，将客户端的Socket封装成一个Task(该任务实现java.lang.Runnable线程任务接口)交给后端的线程池中进行处理。JDK的线程池维护一个消息队列和N个活跃的线程，对消息队列中Socket任务进行处理，由于线程池可以设置消息队列的大小和最大线程数，因此，它的资源占用是可控的，无论多少个客户端并发访问，都不会导致资源的耗尽和宕机。


客户端源码分析

```java
public class ClientDemo {
    public static void main(String[] args) {
        try {
            // 1.简历一个与服务端的Socket对象：套接字
            Socket socket = new Socket("127.0.0.1", 9999);
            // 2.从socket管道中获取一个输出流，写数据给服务端
            OutputStream os = socket.getOutputStream();
            // 3.把输出流包装成一个打印流
            PrintWriter pw = new PrintWriter(os);
            // 4.反复接收用户的输入
            BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
            String line = null;
            while ((line = br.readLine()) != null) {
                pw.println(line);
                pw.flush();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

线程池处理类

```java
// 线程池处理类
public class ServerSocketThreadPool {
    // 线程池
    private static final ExecutorService executor = new ThreadPoolExecutor(
            3,
            2,
            120L,
            TimeUnit.SECONDS, new ArrayBlockingQueue<Runnable>(1000));

    public static void execute(Runnable task) {
        executor.execute(task);
    }
}
```

服务端源码分析

```java
public class ServerDemo {
    public static void main(String[] args) {
        try {
            ServerSocket ss = new ServerSocket(9999);

            // 客户端可能有很多个
            while (true) {
                Socket socket = ss.accept(); // 阻塞式的！
                System.out.println("有人上线了！！");
                // 每次收到一个客户端的socket请求，都需要为这个客户端分配一个
                // 独立的线程 专门负责对这个客户端的通信！！
                ServerSocketThreadPool.execute(new ReaderClientRunnable(socket));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

class ReaderClientRunnable implements Runnable {

    private Socket socket;

    public ReaderClientRunnable(Socket socket) {
        this.socket = socket;
    }

    @Override
    public void run() {
        try {
            // 读取一行数据
            InputStream is = socket.getInputStream();
            // 转成一个缓冲字符流
            Reader fr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(fr);
            // 一行一行的读取数据
            String line = null;
            while ((line = br.readLine()) != null) { // 阻塞式的！！
                System.out.println("服务端收到了数据：" + line);
            }
        } catch (Exception e) {
            System.out.println("有人下线了");
        }
    }
}
```

小结

* 伪异步io采用了线程池实现，因此避免了为每个请求创建一个独立线程造成线程资源耗尽的问题，但由于底层依然是采用的同步阻塞模型，因此无法从根本上解决问题。
* 如果单个消息处理的缓慢，或者服务器线程池中的全部线程都被阻塞，那么后续socket的i/o消息都将在队列中排队。新的Socket请求将被拒绝，客户端会发生大量连接超时。



## 基于BIO形式下的文件上传

客户端开发

```java
public class Client {
    public static void main(String[] args) {
        try(
                InputStream is = new FileInputStream("D:/hello.jpg");
        ){
            //  1、请求与服务端的Socket链接
            Socket socket = new Socket("127.0.0.1" , 8888);
            //  2、把字节输出流包装成一个数据输出流
            DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
            //  3、先发送上传文件的后缀给服务端
            dos.writeUTF(".png");
            //  4、把文件数据发送给服务端进行接收
            byte[] buffer = new byte[1024];
            int len;
            while((len = is.read(buffer)) > 0 ){
                dos.write(buffer , 0 , len);
            }
            dos.flush();
            Thread.sleep(10000);
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
```

服务端开发

```java
public class Server {
    public static void main(String[] args) {
        try{
            ServerSocket ss = new ServerSocket(8888);
            while (true){
                Socket socket = ss.accept();
                // 交给一个独立的线程来处理与这个客户端的文件通信需求。
                new ServerReaderThread(socket).start();
            }
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
```

```java
public class ServerReaderThread extends Thread {
    private Socket socket;
    public ServerReaderThread(Socket socket){
        this.socket = socket;
    }
    @Override
    public void run() {
        try{
            // 1、得到一个数据输入流读取客户端发送过来的数据
            DataInputStream dis = new DataInputStream(socket.getInputStream());
            // 2、读取客户端发送过来的文件类型
            String suffix = dis.readUTF();
            System.out.println("服务端已经成功接收到了文件类型：" + suffix);
            // 3、定义一个字节输出管道负责把客户端发来的文件数据写出去
            OutputStream os = new FileOutputStream("D:/"+UUID.randomUUID().toString()+suffix);
            // 4、从数据输入流中读取文件数据，写出到字节输出流中去
            byte[] buffer = new byte[1024];
            int len;
            while((len = dis.read(buffer)) > 0){
                os.write(buffer,0, len);
            }
            os.close();
            System.out.println("服务端接收文件保存成功！");
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
```

小结

客户端怎么发，服务端就怎么接收

# Java NIO深入剖析

* Java NIO（New IO）也有人称之为 java non-blocking IO是从Java 1.4版本开始引入的一个新的IO API，可以替代标准的Java IO API。NIO与原来的IO有同样的作用和目的，但是使用的方式完全不同，NIO支持面**向缓冲区**的、基于**通道**的IO操作。NIO将以更加高效的方式进行文件的读写操作。NIO可以理解为非阻塞IO,传统的IO的read和write只能阻塞执行，线程在读写IO期间不能干其他事情，比如调用socket.read()时，如果服务器一直没有数据传输过来，线程就一直阻塞，而NIO中可以配置socket为非阻塞模式。
*  NIO 相关类都被放在 java.nio 包及子包下，并且对原 java.io 包中的很多类进行改写。
* NIO 有三大核心部分：**Channel( 通道) ，Buffer( 缓冲区), Selector( 选择器)**
* Java NIO 的非阻塞模式，使一个线程从某通道发送请求或者读取数据，但是它仅能得到目前可用的数据，如果目前没有数据可用时，就什么都不会获取，而不是保持线程阻塞，所以直至数据变的可以读取之前，该线程可以继续做其他的事情。 非阻塞写也是如此，一个线程请求写入一些数据到某通道，但不需要等待它完全写入，这个线程同时可以去做别的事情。
* 通俗理解：NIO 是可以做到用一个线程来处理多个操作的。假设有 1000 个请求过来,根据实际情况，可以分配20 或者 80个线程来处理。不像之前的阻塞 IO 那样，非得分配 1000 个。

##  NIO 和 BIO 的比较

* BIO 以流的方式处理数据,而 NIO 以块的方式处理数据,块 I/O 的效率比流 I/O 高很多
* BIO 是阻塞的，NIO 则是非阻塞的
*  BIO 基于字节流和字符流进行操作，而 NIO 基于 Channel(通道)和 Buffer(缓冲区)进行操作，数据总是从通道
  读取到缓冲区中，或者从缓冲区写入到通道中。Selector(选择器)用于监听多个通道的事件（比如：连接请求，数据到达等），因此使用单个线程就可以监听多个客户端通道

| NIO                       | BIO                 |
| ------------------------- | ------------------- |
| 面向缓冲区（Buffer）      | 面向流（Stream）    |
| 非阻塞（Non Blocking IO） | 阻塞IO(Blocking IO) |
| 选择器（Selectors）       |                     |



## NIO 三大核心原理示意图

NIO 有三大核心部分：**Channel( 通道) ，Buffer( 缓冲区), Selector( 选择器)**

### Buffer缓冲区

缓冲区本质上是一块可以写入数据，然后可以从中读取数据的内存。这块内存被包装成NIO Buffer对象，并提供了一组方法，用来方便的访问该块内存。相比较直接对数组的操作，Buffer API更加容易操作和管理。

### **Channel（通道）**

Java NIO的通道类似流，但又有些不同：既可以从通道中读取数据，又可以写数据到通道。但流的（input或output)读写通常是单向的。 通道可以非阻塞读取和写入通道，通道可以支持读取或写入缓冲区，也支持异步地读写。

### Selector选择器

Selector是 一个Java NIO组件，可以能够检查一个或多个 NIO 通道，并确定哪些通道已经准备好进行读取或写入。这样，一个单独的线程可以管理多个channel，从而管理多个网络连接，提高效率


* 每个 channel 都会对应一个 Buffer
* 一个线程对应Selector ， 一个Selector对应多个 channel(连接)
* 程序切换到哪个 channel 是由事件决定的
*  Selector 会根据不同的事件，在各个通道上切换
* Buffer 就是一个内存块 ， 底层是一个数组
* 数据的读取写入是通过 Buffer完成的 , BIO 中要么是输入流，或者是输出流, 不能双向，但是 NIO 的 Buffer 是可以读也可以写。
* Java NIO系统的核心在于：通道(Channel)和缓冲区 (Buffer)。通道表示打开到 IO 设备(例如：文件、 套接字)的连接。若需要使用 NIO 系统，需要获取 用于连接 IO 设备的通道以及用于容纳数据的缓冲 区。然后操作缓冲区，对数据进行处理。简而言之，Channel 负责传输， Buffer 负责存取数据

## NIO核心一：缓冲区(Buffer)

一个用于特定基本数据类 型的容器。由 java.nio 包定义的，所有缓冲区 都是 Buffer 抽象类的子类.。Java NIO 中的 Buffer 主要用于与 NIO 通道进行 交互，数据是从通道读入缓冲区，从缓冲区写入通道中的


### Buffer 类及其子类

**Buffer** 就像一个数组，可以保存多个相同类型的数据。根 据数据类型不同 ，有以下 Buffer 常用子类：

* ByteBuffer
* CharBuffer
* ShortBuffer
* IntBuffer
*  LongBuffer
* FloatBuffer
* DoubleBuffer

上述 Buffer 类 他们都采用相似的方法进行管理数据，只是各自 管理的数据类型不同而已。都是通过`allocate(int capacity)`方法获取一个 Buffer 对象

### 缓冲区的基本属性

Buffer 中的重要概念：

* **容量 (capacity)** ：作为一个内存块，Buffer具有一定的固定大小，也称为"容量"，缓冲区容量不能为负，并且创建后不能更改。
*  **限制 (limit)**：表示缓冲区中可以操作数据的大小（limit 后数据不能进行读写）。缓冲区的限制不能为负，并且不能大于其容量。 **写入模式，限制等于buffer的容量。读取模式下，limit等于写入的数据量**。
* **位置 (position)**：下一个要读取或写入的数据的索引。缓冲区的位置不能为 负，并且不能大于其限制
* **标记 (mark)与重置 (reset)**：标记是一个索引，通过 Buffer 中的 mark() 方法 指定 Buffer 中一个特定的 position，之后可以通过调用 reset() 方法恢复到这 个 position.
   **标记、位置、限制、容量遵守以下不变式： 0 <= mark <= position <= limit <= capacity**
* **图示:**

### Buffer常见方法

```java
Buffer clear() 清空缓冲区并返回对缓冲区的引用
Buffer flip() 为 将缓冲区的界限设置为当前位置，并将当前位置充值为 0
int capacity() 返回 Buffer 的 capacity 大小
boolean hasRemaining() 判断缓冲区中是否还有元素
int limit() 返回 Buffer 的界限(limit) 的位置
Buffer limit(int n) 将设置缓冲区界限为 n, 并返回一个具有新 limit 的缓冲区对象
Buffer mark() 对缓冲区设置标记
int position() 返回缓冲区的当前位置 position
Buffer position(int n) 将设置缓冲区的当前位置为 n , 并返回修改后的 Buffer 对象
int remaining() 返回 position 和 limit 之间的元素个数
Buffer reset() 将位置 position 转到以前设置的 mark 所在的位置
Buffer rewind() 将位置设为为 0， 取消设置的 mark
```

### 缓冲区的数据操作

```java
Buffer 所有子类提供了两个用于数据操作的方法：get()put() 方法
取获取 Buffer中的数据
get() ：读取单个字节
get(byte[] dst)：批量读取多个字节到 dst 中
get(int index)：读取指定索引位置的字节(不会移动 position)

放到 入数据到 Buffer 中 中
put(byte b)：将给定单个字节写入缓冲区的当前位置
put(byte[] src)：将 src 中的字节写入缓冲区的当前位置
put(int index, byte b)：将指定字节写入缓冲区的索引位置(不会移动 position)
```

**使用Buffer读写数据一般遵循以下四个步骤：**

* 1.写入数据到Buffer
* 2.调用flip()方法，转换为读取模式
* 3.从Buffer中读取数据
* 4.调用buffer.clear()方法或者buffer.compact()方法清除缓冲区


### 直接与非直接缓冲区

`byte byffer`可以是两种类型，一种是基于直接内存（也就是非堆内存）；另一种是非直接内存（也就是堆内存）。对于直接内存来说，JVM将会在IO操作上具有更高的性能，因为它直接作用于本地系统的IO操作。而非直接内存，也就是堆内存中的数据，如果要作IO操作，会先从本进程内存复制到直接内存，再利用本地IO处理。

从数据流的角度，非直接内存是下面这样的作用链：

```
本地IO-->直接内存-->非直接内存-->直接内存-->本地IO
```

而直接内存是：

```
本地IO-->直接内存-->本地IO
```

很明显，在做IO处理时，比如网络发送大量数据时，直接内存会具有更高的效率。直接内存使用allocateDirect创建，但是它比申请普通的堆内存需要耗费更高的性能。不过，这部分的数据是在JVM之外的，因此它不会占用应用的内存。所以呢，当你有很大的数据要缓存，并且它的生命周期又很长，那么就比较适合使用直接内存。只是一般来说，如果不是能带来很明显的性能提升，还是推荐直接使用堆内存。字节缓冲区是直接缓冲区还是非直接缓冲区可通过调用其 isDirect()  方法来确定。

**使用场景**

- 1 有很大的数据需要存储，它的生命周期又很长
- 2 适合频繁的IO操作，比如网络并发场景



## NIO核心二：通道(Channel)

通道（Channel）：由 java.nio.channels 包定义 的。Channel 表示 IO 源与目标打开的连接。 Channel 类似于传统的“流”。只不过 Channel 本身不能直接访问数据，Channel 只能与 Buffer 进行交互。

 NIO 的通道类似于流，但有些区别如下：

* 通道可以同时进行读写，而流只能读或者只能写
*  通道可以实现异步读写数据
*  通道可以从缓冲读数据，也可以写数据到缓冲:

BIO 中的 stream 是单向的，例如 FileInputStream 对象只能进行读取数据的操作，而 NIO 中的通道(Channel)是双向的，可以读操作，也可以写操作。

Channel 在 NIO 中是一个接口
```java
public interface Channel extends Closeable{}
```

### 常用的Channel实现类

* FileChannel：用于读取、写入、映射和操作文件的通道。
* DatagramChannel：通过 UDP 读写网络中的数据通道。
* SocketChannel：通过 TCP 读写网络中的数据。
* ServerSocketChannel：可以监听新进来的 TCP 连接，对每一个新进来的连接都会创建一个 SocketChannel。ServerSocketChanne 类似 ServerSocket , SocketChannel 类似 Socket

### FileChannel 类

获取通道的一种方式是对支持通道的对象调用getChannel() 方法。支持通道的类如下：

* FileInputStream
* FileOutputStream
* RandomAccessFile
* DatagramSocket
* Socket
* ServerSocket

获取通道的其他方式是使用 Files 类的静态方法 newByteChannel() 获取字节通道。或者通过通道的静态方法 open() 打开并返回指定通道

### FileChannel的常用方法

```java
int read(ByteBuffer dst) 从 从  Channel 到 中读取数据到  ByteBuffer
long  read(ByteBuffer[] dsts) 将 将  Channel 到 中的数据“分散”到  ByteBuffer[]
int  write(ByteBuffer src) 将 将  ByteBuffer 到 中的数据写入到  Channel
long write(ByteBuffer[] srcs) 将 将  ByteBuffer[] 到 中的数据“聚集”到  Channel
long position() 返回此通道的文件位置
FileChannel position(long p) 设置此通道的文件位置
long size() 返回此通道的文件的当前大小
FileChannel truncate(long s) 将此通道的文件截取为给定大小
void force(boolean metaData) 强制将所有对此通道的文件更新写入到存储设备中
```

本地文件写数据
```java
public class ChannelTest {
    @Test
    public void write(){
        try {
            // 1、字节输出流通向目标文件
            FileOutputStream fos = new FileOutputStream("hello.txt");
            // 2、得到字节输出流对应的通道Channel
            FileChannel channel = fos.getChannel();
            // 3、分配缓冲区
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            buffer.put("hello,学习Java-NIO！".getBytes());
            // 4、把缓冲区切换成写出模式
            buffer.flip();
            channel.write(buffer);
            channel.close();
            System.out.println("写数据到文件中！");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

本地文件读数据
```java
public class ChannelTest {

    @Test
    public void read() throws Exception {
        // 1、定义一个文件字节输入流与源文件接通
        FileInputStream is = new FileInputStream("hello.txt");
        // 2、需要得到文件字节输入流的文件通道
        FileChannel channel = is.getChannel();
        // 3、定义一个缓冲区
        ByteBuffer buffer = ByteBuffer.allocate(1024);
        // 4、读取数据到缓冲区
        channel.read(buffer);
        buffer.flip();
        // 5、读取出缓冲区中的数据并输出即可
        String rs = new String(buffer.array(),0,buffer.remaining());
        System.out.println(rs);

    }
```

使用 FileChannel(通道) ，完成文件的拷贝。

```java
@Test
public void copy() throws Exception {
    // 源文件
    File srcFile = new File("D:/background.jpg");
    File destFile = new File("D:/backgroundNew.jpg");
    // 得到一个字节字节输入流
    FileInputStream fis = new FileInputStream(srcFile);
    // 得到一个字节输出流
    FileOutputStream fos = new FileOutputStream(destFile);
    // 得到的是文件通道
    FileChannel isChannel = fis.getChannel();
    FileChannel osChannel = fos.getChannel();
    // 分配缓冲区
    ByteBuffer buffer = ByteBuffer.allocate(1024); while(isChannel.read(buffer)!=-1){
        // 已经读取了数据 ，把缓冲区的模式切换成可读模式
        buffer.flip();
        // 把数据写出到
        osChannel.write(buffer);
         // 必须先清空缓冲然后再写入数据到缓冲区
        buffer.clear();
    }
    isChannel.close();
    osChannel.close();
    System.out.println("复制完成！");
}
```

### transferFrom

从目标通道中去复制原通道数据

```java
public static void main(String[] args) throws Exception {
    // 1、字节输入管道
    FileInputStream is = new FileInputStream("orange.txt");
    FileChannel isChannel = is.getChannel();
    // 2、字节输出流管道
    FileOutputStream fos = new FileOutputStream("orange-2.txt");
    FileChannel osChannel = fos.getChannel();
    // 3、复制
    osChannel.transferFrom(isChannel, isChannel.position(), isChannel.size());
    isChannel.close();
    osChannel.close();
}
```

### transferTo

把原通道数据复制到目标通道

```java
public static void main(String[] args) throws Exception {
    // 1、字节输入管道
    FileInputStream is = new FileInputStream("orange.txt");
    FileChannel isChannel = is.getChannel();
    // 2、字节输出流管道
    FileOutputStream fos = new FileOutputStream("orange-2.txt");
    FileChannel osChannel = fos.getChannel();
    // 3、复制
    isChannel.transferTo(isChannel.position(), isChannel.size(), osChannel);
    isChannel.close();
    osChannel.close();
}
```

## NIO核心三：选择器(Selector)

选择器（Selector） 是 SelectableChannle 对象的多路复用器，Selector 可以同时监控多个 SelectableChannel 的 IO 状况，也就是说，利用 Selector可使一个单独的线程管理多个 Channel。Selector 是非阻塞 IO 的核心


* Java 的 NIO，用非阻塞的 IO 方式。可以用一个线程，处理多个的客户端连接，就会使用到 Selector(选择器)

* Selector 能够检测多个注册的通道上是否有事件发生(注意:多个 Channel 以事件的方式可以注册到同一个
  Selector)，如果有事件发生，便获取事件然后针对每个事件进行相应的处理。这样就可以只用一个单线程去管
  理多个通道，也就是管理多个连接和请求。

* 只有在 连接/通道 真正有读写事件发生时，才会进行读写，就大大地减少了系统开销，并且不必为每个连接都
  创建一个线程，不用去维护多个线程

* 避免了多线程之间的上下文切换导致的开销


创建 Selector ：通过调用 Selector.open() 方法创建一个 Selector。

```java
Selector selector = Selector.open();
```

向选择器注册通道：SelectableChannel.register(Selector sel, int ops)

```java
//1. 获取通道
ServerSocketChannel ssChannel = ServerSocketChannel.open();
//2. 切换非阻塞模式
ssChannel.configureBlocking(false);
//3. 绑定连接
ssChannel.bind(new InetSocketAddress(9898));
//4. 获取选择器
Selector selector = Selector.open();
//5. 将通道注册到选择器上, 并且指定“监听接收事件”
ssChannel.register(selector, SelectionKey.OP_ACCEPT);
```

当调用 register(Selector sel, int ops) 将通道注册选择器时，选择器对通道的监听事件，需要通过第二个参数 ops 指定。可以监听的事件类型（用 可使用 SelectionKey  的四个常量 表示）：

* 读 : SelectionKey.OP_READ （1）
* 写 : SelectionKey.OP_WRITE （4）
* 连接 : SelectionKey.OP_CONNECT （8）
*  接收 : SelectionKey.OP_ACCEPT （16）
* 若注册时不止监听一个事件，则可以使用“位或”操作符连接。

```java
int interestSet = SelectionKey.OP_READ|SelectionKey.OP_WRITE
```

## NIO非阻塞式网络通信原理分析

Selector可以实现： 一个 I/O 线程可以并发处理 N 个客户端连接和读写操作，这从根本上解决了传统同步阻塞 I/O 一连接一线程模型，架构的性能、弹性伸缩能力和可靠性都得到了极大的提升。

### 服务端流程

当客户端连接服务端时，服务端会通过 ServerSocketChannel 得到 SocketChannel

```java
public static void main(String[] args) throws Exception {
    //1、获取通道
    ServerSocketChannel ssChannel = ServerSocketChannel.open();
    //2、切换非阻塞模式
    ssChannel.configureBlocking(false);
    //3、绑定连接
    ssChannel.bind(new InetSocketAddress(9999));
    //4、获取选择器
    Selector selector = Selector.open();
    //5、将通道注册到选择器上, 并且指定“监听接收事件”
    ssChannel.register(selector, SelectionKey.OP_ACCEPT);
    //6. 轮询式的获取选择器上已经“准备就绪”的事件
    while (selector.select() > 0) {
        System.out.println("轮一轮");
        //7. 获取当前选择器中所有注册的“选择键(已就绪的监听事件)”
        Iterator<SelectionKey> it = selector.selectedKeys().iterator();
        while (it.hasNext()) {
            //8. 获取准备“就绪”的是事件
            SelectionKey sk = it.next();
            //9. 判断具体是什么事件准备就绪
            if (sk.isAcceptable()) {
                //10. 若“接收就绪”，获取客户端连接
                SocketChannel sChannel = ssChannel.accept();
                //11. 切换非阻塞模式
                sChannel.configureBlocking(false);
                //12. 将该通道注册到选择器上
                sChannel.register(selector, SelectionKey.OP_READ);
            } else if (sk.isReadable()) {
                //13. 获取当前选择器上“读就绪”状态的通道
                SocketChannel sChannel = (SocketChannel) sk.channel();
                //14. 读取数据
                ByteBuffer buf = ByteBuffer.allocate(1024);
                int len = 0;
                while ((len = sChannel.read(buf)) > 0) {
                    buf.flip();
                    System.out.println(new String(buf.array(), 0, len));
                    buf.clear();
                }
            }
            //15. 取消选择键 SelectionKey
            it.remove();
        }
    }
}
```

### 客户端流程
```java
public static void main(String[] args) throws Exception {
    // 1. 获取通道
    SocketChannel sChannel = SocketChannel.open(new InetSocketAddress("127.0.0.1", 9999));
    // 2. 切换非阻塞模式
    sChannel.configureBlocking(false);
    //3. 分配指定大小的缓冲区
    ByteBuffer buf = ByteBuffer.allocate(1024);
    //4. 发送数据给服务端
    Scanner scan = new Scanner(System.in);
    while (scan.hasNext()) {
        String str = scan.nextLine();
        buf.put((new SimpleDateFormat("yyyy/MM/dd HH:mm:ss").format(System.currentTimeMillis()) + "\n" + str).getBytes());
        buf.flip();
        sChannel.write(buf);
        buf.clear();
    }
    //关闭通道
    sChannel.close();
}
```


## NIO非阻塞式网络通信入门案例

需求：服务端接收客户端的连接请求，并接收多个客户端发送过来的事件。

```java
/**
  客户端
 */
public class Client {
    public static void main(String[] args) throws Exception {
        //1. 获取通道
        SocketChannel sChannel = SocketChannel.open(new InetSocketAddress("127.0.0.1", 9999));
        //2. 切换非阻塞模式
        sChannel.configureBlocking(false);
        //3. 分配指定大小的缓冲区
        ByteBuffer buf = ByteBuffer.allocate(1024);
        //4. 发送数据给服务端
        Scanner scan = new Scanner(System.in);
        while (scan.hasNext()) {
            String str = scan.nextLine();
            String dateTime = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss").format(System.currentTimeMillis());
            String message = dateTime + str;
            buf.put(message.getBytes());
            buf.flip();
            sChannel.write(buf);
            buf.clear();
        }
        //5. 关闭通道
        sChannel.close();
    }
}
```

```java
/**
 服务端
 */
public class Server {
    public static void main(String[] args) throws Exception {
        //1. 获取通道
        ServerSocketChannel ssChannel = ServerSocketChannel.open();
        //2. 切换非阻塞模式
        ssChannel.configureBlocking(false);
        //3. 绑定连接
        ssChannel.bind(new InetSocketAddress(9999));
        //4. 获取选择器
        Selector selector = Selector.open();
        //5. 将通道注册到选择器上, 并且指定“监听接收事件”
        ssChannel.register(selector, SelectionKey.OP_ACCEPT);
        //6. 轮询式的获取选择器上已经“准备就绪”的事件
        while (selector.select() > 0) {
            System.out.println("轮一轮");
            //7. 获取当前选择器中所有注册的“选择键(已就绪的监听事件)”
            Iterator<SelectionKey> it = selector.selectedKeys().iterator();
            while (it.hasNext()) {
                //8. 获取准备“就绪”的是事件
                SelectionKey sk = it.next();
                //9. 判断具体是什么事件准备就绪
                if (sk.isAcceptable()) {
                    //10. 若“接收就绪”，获取客户端连接
                    SocketChannel sChannel = ssChannel.accept();
                    //11. 切换非阻塞模式
                    sChannel.configureBlocking(false);
                    //12. 将该通道注册到选择器上
                    sChannel.register(selector, SelectionKey.OP_READ);
                } else if (sk.isReadable()) {
                    //13. 获取当前选择器上“读就绪”状态的通道
                    SocketChannel sChannel = (SocketChannel) sk.channel();
                    //14. 读取数据
                    ByteBuffer buf = ByteBuffer.allocate(1024);
                    int len = 0;
                    while ((len = sChannel.read(buf)) > 0) {
                        buf.flip();
                        System.out.println(new String(buf.array(), 0, len));
                        buf.clear();
                    }
                }
                //15. 取消选择键 SelectionKey
                it.remove();
            }
        }
    }
}
```

## NIO 网络编程应用实例-群聊系统


* 编写一个 NIO 群聊系统，实现客户端与客户端的通信需求（非阻塞）
* 服务器端：可以监测用户上线，离线，并实现消息转发功能
* 客户端：通过 channel 可以无阻塞发送消息给其它所有客户端用户，同时可以接受其它客户端用户通过服务端转发来的消息

服务端代码实现

```java
public class ServerDemo {
    //定义属性
    private Selector selector;
    private ServerSocketChannel ssChannel;
    private static final int PORT = 9999;

    //构造器
    //初始化工作
    public ServerDemo() {
        try {
            // 1、获取通道
            ssChannel = ServerSocketChannel.open();
            // 2、切换为非阻塞模式
            ssChannel.configureBlocking(false);
            // 3、绑定连接的端口
            ssChannel.bind(new InetSocketAddress(PORT));
            // 4、获取选择器Selector
            selector = Selector.open();
            // 5、将通道都注册到选择器上去，并且开始指定监听接收事件
            ssChannel.register(selector, SelectionKey.OP_ACCEPT);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //监听
    public void listen() {
        System.out.println("监听线程: " + Thread.currentThread().getName());
        try {
            while (selector.select() > 0) {
                System.out.println("开始一轮事件处理~~~");
                // 7、获取选择器中的所有注册的通道中已经就绪好的事件
                Iterator<SelectionKey> it = selector.selectedKeys().iterator();
                // 8、开始遍历这些准备好的事件
                while (it.hasNext()) {
                    // 提取当前这个事件
                    SelectionKey sk = it.next();
                    // 9、判断这个事件具体是什么
                    if (sk.isAcceptable()) {
                        // 10、直接获取当前接入的客户端通道
                        SocketChannel sChannel = ssChannel.accept();
                        // 11 、切换成非阻塞模式
                        sChannel.configureBlocking(false);
                        // 12、将本客户端通道注册到选择器
                        System.out.println(sChannel.getRemoteAddress() + " 上线 ");
                        sChannel.register(selector, SelectionKey.OP_READ);
                        //提示
                    } else if (sk.isReadable()) {
                        //处理读 (专门写方法..)
                        readData(sk);
                    }
                    // 处理完毕之后需要移除当前事件
                    it.remove();
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            //发生异常处理....
        }
    }

    //读取客户端消息
    private void readData(SelectionKey key) {
        //取到关联的channle
        SocketChannel channel = null;
        try {
            //得到channel
            channel = (SocketChannel) key.channel();
            //创建buffer
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            int count = channel.read(buffer);
            //根据count的值做处理
            if (count > 0) {
                //把缓存区的数据转成字符串
                String msg = new String(buffer.array());
                //输出该消息
                System.out.println("form 客户端: " + msg);
                //向其它的客户端转发消息(去掉自己), 专门写一个方法来处理
                sendInfoToOtherClients(msg, channel);
            }
        } catch (IOException e) {
            try {
                System.out.println(channel.getRemoteAddress() + " 离线了..");
                e.printStackTrace();
                //取消注册
                key.cancel();
                //关闭通道
                channel.close();
            } catch (IOException e2) {
                e2.printStackTrace();
            }
        }
    }

    //转发消息给其它客户(通道)
    private void sendInfoToOtherClients(String msg, SocketChannel self) throws IOException {
        System.out.println("服务器转发消息中...");
        System.out.println("服务器转发数据给客户端线程: " + Thread.currentThread().getName());
        //遍历 所有注册到selector 上的 SocketChannel,并排除 self
        for (SelectionKey key : selector.keys()) {
            //通过 key  取出对应的 SocketChannel
            Channel targetChannel = key.channel();
            //排除自己
            if (targetChannel instanceof SocketChannel && targetChannel != self) {
                //转型
                SocketChannel dest = (SocketChannel) targetChannel;
                //将msg 存储到buffer
                ByteBuffer buffer = ByteBuffer.wrap(msg.getBytes());
                //将buffer 的数据写入 通道
                dest.write(buffer);
            }
        }
    }

    public static void main(String[] args) {
        //创建服务器对象
        ServerDemo groupChatServer = new ServerDemo();
        groupChatServer.listen();
    }
}
```

客户端代码实现
```java
public class ClientDemo {
    //定义相关的属性
    private final String HOST = "127.0.0.1"; // 服务器的ip
    private final int PORT = 9999; //服务器端口
    private Selector selector;
    private SocketChannel socketChannel;
    private String username;

    //构造器, 完成初始化工作
    public ClientDemo() throws IOException {
        selector = Selector.open();
        //连接服务器
        socketChannel = socketChannel.open(new InetSocketAddress("127.0.0.1", PORT));
        //设置非阻塞
        socketChannel.configureBlocking(false);
        //将channel 注册到selector
        socketChannel.register(selector, SelectionKey.OP_READ);
        //得到username
        username = socketChannel.getLocalAddress().toString().substring(1);
        System.out.println(username + " is ok...");

    }

    //向服务器发送消息
    public void sendInfo(String info) {
        info = username + " 说：" + info;
        try {
            socketChannel.write(ByteBuffer.wrap(info.getBytes()));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //读取从服务器端回复的消息
    public void readInfo() {
        try {
            int readChannels = selector.select();
            //有可以用的通道
            if (readChannels > 0) {
                Iterator<SelectionKey> iterator = selector.selectedKeys().iterator();
                while (iterator.hasNext()) {
                    SelectionKey key = iterator.next();
                    if (key.isReadable()) {
                        //得到相关的通道
                        SocketChannel sc = (SocketChannel) key.channel();
                        //得到一个Buffer
                        ByteBuffer buffer = ByteBuffer.allocate(1024);
                        //读取
                        sc.read(buffer);
                        //把读到的缓冲区的数据转成字符串
                        String msg = new String(buffer.array());
                        System.out.println(msg.trim());
                    }
                }
                //删除当前的selectionKey, 防止重复操作
                iterator.remove();
            } else {
                //System.out.println("没有可以用的通道...");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws Exception {
        //启动我们客户端
        ClientDemo chatClient = new ClientDemo();
        //启动一个线程, 每个3秒，读取从服务器发送数据
        new Thread(() -> {
            while (true) {
                chatClient.readInfo();
                try {
                    Thread.currentThread().sleep(3000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }).start();

        //发送数据给服务器端
        Scanner scanner = new Scanner(System.in);
        while (scanner.hasNextLine()) {
            String s = scanner.nextLine();
            chatClient.sendInfo(s);
        }
    }
}
```
        
