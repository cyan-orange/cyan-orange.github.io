# 线程的基本概念

多线程的基本概念：程序、进程、线程。

程序(program)是为完成特定任务、用某种语言编写的一组指令的集合。即指一段静态的代码，静态对象。

进程(process)是程序的一次执行过程，或是正在运行的一个程序。是一个动态的过程：有它自身的产生、存在和消亡的过程。这就是生命周期。进程作为资源分配的单位，系统在运行时会为每个进程分配不同的内存区域。

线程(thread)，进程可进一步细化为线程，是一个程序内部的一条执行路径。 线程作为调度和执行的单位，每个线程拥有独立的运行栈和程序计数器(pc)，线程切换的开销小。一个进程中的多个线程共享相同的内存单元（内存地址空间），它们从同一堆中分配对象，可以访问相同的变量和对象。这就使得线程间通信更简便、高效。但多个线程操作共享的系统资源可能就会带来安全的隐患。

一个Java应用程序java.exe，其实至少有三个线程：main()主线程，gc()垃圾回收线程，异常处理线程。当然如果发生异常，会影响主线程。

# 三种创建线程的方式

三种创建线程的方式：
1. 继承`Thread`类
2. 实现`Runnable`接口
3. 使用Callable和Future创建线程

## 继承Thread类

Thread类的构造器
1. `Thread()`：创建新的Thread对象
2. `Thread(String threadname)`：创建线程并指定线程实例名
3. `Thread(Runnable target)`：指定创建线程的目标对象，它实现了Runnable接口中的run方法
3. `Thread(Runnable target, String name)`：创建新的Thread对象

Thread类的常用方法
1. `void start()`: 启动线程，并执行对象的run()方法
2. `String getName()`: 返回线程的名称
3. `void setName(String name)`:设置该线程名称
4. `static Thread currentThread()`: 返回当前线程
5. `static void yield()`：暂停当前正在执行的线程，把执行机会让给优先级相同或更高的线程，若队列中没有同优先级的线程，忽略此方法
6. `static void sleep(long millis)`：令当前活动线程在指定时间段内放弃对CPU控制,使其他线程有机会被执行,时间到后重排队。
7. `boolean isAlive()`：返回boolean，判断线程是否还活着
8. `join()`：当某个程序执行流中调用其他线程的 join() 方法时，调用线程将被阻塞，直到 join() 方法加入的 join 线程执行完为止

继承Thread类创建线程如下：
```java
public class ThradTest extends Thread{

    @Override
    public void run() {
        System.out.println("继承Thread的多线程!");
    }

    public static void main(String[] args) {
        ThradTest t=new ThradTest();
        t.start();
    }
}
```

## 实现Runnable接口
实现Runnable接口创建多线程
```java
class RunnableTest implements Runnable {

    @Override
    public void run() {
        System.out.println("实现Runnable接口的多线程");
    }

    public static void main(String[] args) {
        RunnableTest t = new RunnableTest ();
        Thread thread = new Thread(t);
        thread.start();
    }
}
```

## 使用Callable和Future创建线程

与使用Runnable相比， Callable功能更强大
1. 相比run()方法，可以有返回值
2. 方法可以抛出异常
3. 支持泛型的返回值
4. 需要借助`FutureTask`类，比如获取返回结果

Future接口
1. 可以对具体Runnable、Callable任务的执行结果进行取消、查询是否完成、获取结果等。
2. FutrueTask是Futrue接口的唯一的实现类
3. FutureTask 同时实现了Runnable, Future接口。它既可以作为Runnable被线程执行，又可以作为Future得到Callable的返回值

使用Runnable呢Funtrue创建线程
```java
//1.创建一个实现Callable的实现类
class NumThread implements Callable{
    //2.实现call方法，将此线程需要执行的操作声明在call()中
    @Override
    public Object call() throws Exception {
        return 1+1;
    }
}


public class ThreadNew {
    public static void main(String[] args) {
        //3.创建Callable接口实现类的对象
        NumThread numThread = new NumThread();
        //4.将此Callable接口实现类的对象作为传递到FutureTask构造器中，创建FutureTask的对象
        FutureTask futureTask = new FutureTask(numThread);
        //5.将FutureTask的对象作为参数传递到Thread类的构造器中，创建Thread对象，并调用start()
        new Thread(futureTask).start();

        try {
            //6.获取Callable中call方法的返回值
            //get()返回值即为FutureTask构造器参数Callable实现类重写的call()的返回值。
            Object sum = futureTask.get();
            System.out.println("总和为：" + sum);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
    }

}
```

# 线程的生命周期

1. 新建： 当一个Thread类或其子类的对象被声明并创建时，新生的线程对象处于新建状态
2. 就绪：处于新建状态的线程被start()后，将进入线程队列等待CPU时间片，此时它已具备了运行的条件，只是没分配到CPU资源
3. 运行：当就绪的线程被调度并获得CPU资源时,便进入运行状态
4. 阻塞：在某种特殊情况下，比如执行了sleep()方法，将让出CPU并暂时停止自己的运行，进入阻塞状态。
5. 死亡：线程完成了它的全部工作或线程被提前强制性地中止或出现异常导致结束

## yield()和sleep()方法

yield()方法和sleep()方法有点相似，它也是Thread类提供的一个静态的方法，它也可以让当前正在执行的线程暂停，让出cpu资源给其他的线程。但是和sleep()方法不同的是，它不会进入到阻塞状态，而是进入到就绪状态。yield()方法只是让当前线程暂停一下，重新进入就绪的线程池中，让系统的线程调度器重新调度器重新调度一次，完全可能出现这样的情况：当某个线程调用yield()方法之后，线程调度器又将其调度出来重新进入到运行状态执行。

## wait()、notify()、notifyAll()

- `wait()`：令当前线程挂起并放弃CPU，前线程排队等候其他线程调用notify()或notifyAll()方法唤醒，唤醒后等待重新获得对监视器的所有权后才能继续执行。
- `notify()`：唤醒正在排队等待同步资源的线程中优先级最高者结束等待
- `notifyAll ()`：唤醒正在排队等待资源的所有线程结束等待.

这三个方法只有在synchronized方法或synchronized代码块中才能使用，否则会报`java.lang.IllegalMonitorStateException`异常。

因为这三个方法必须有锁对象调用，而任意对象都可以作为synchronized的同步锁，因此这三个方法只能在Object类中声明。

# 线程同步

当多条语句在操作同一个线程共享数据时，一个线程对多条语句只执行了一部分，还没有执行完，另一个线程参与进来执行。导致共享数据的错误。

解决办法：
对多条操作共享数据的语句，只能让一个线程都执行完，在执行过程中，其他线程不可以参与执行。

线程同步的方式有：
1. 同步方法
2. 同步代码块
3. Lock(锁)

同步方法：
```java
public synchronized void methodName(){

}
```

同步代码块：
```java
synchronized (Object){
// 需要被同步的代码；
}
```

synchronized的锁是什么？
在同步方法中，静态同步方法的锁是class（类名.class），非静态方法的锁是当前对象（this）
在同步代码块中，锁由自己指定，很多时候也是指定为this或类名.class

## Lock

从JDK 5.0开始，Java提供了更强大的线程同步机制，通过显式定义同步锁对象来实现同步。
`java.util.concurrent.locks.Lock`接口是控制多个线程对共享资源进行访问的工具。锁提供了对共享资源的独占访问，每次只能有一个线程对`Lock`对象加锁，线程开始访问共享资源之前应先获得`Lock`对象。
在实现线程安全的控制中，比较常用的是`ReentrantLock` 该类类实现了 `Lock`，它拥有与 `synchronized` 相同的并发性和内存语义，可以显式加锁、释放锁。

案例：模拟三个窗口卖100张票
```java
public class Window implements Runnable {
    int ticket = 100;
    private final ReentrantLock lock = new ReentrantLock();

    public void run() {

        while (true) {
            //加锁
            lock.lock();
            try {
                if (ticket > 0) {
                    try {
                        Thread.sleep(10);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    System.out.println(ticket--);
                } else {
                    break;
                }
            } finally {
                lock.unlock();//解锁
            }
        }
    }
}

public class ThreadLock {
    public static void main(String[] args) {
        Window w = new Window();
        Thread t1 = new Thread(t);
        Thread t2 = new Thread(t);
        Thread t3 = new Thread(t);

        t1.start();
        t2.start();
        t3.start();
    }
}
```

## synchronized和Lock比较
1. Lock是显式锁（手动开启和关闭锁），synchronized是隐式锁，出了作用域自动释放
2. Lock只有代码块锁，synchronized有代码块锁和方法锁
3. 使用Lock锁，JVM将花费较少的时间来调度线程，性能更好。并且具有更好的扩展性（提供更多的子类）
        
