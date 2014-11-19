====================================
java concurrency in practice
====================================

多线程的危害： 线程不安全， 活锁， 性能

chapter 2
==============================

线程安全，原子性，竟态条件(race condition), 组合动作

锁： 原生锁synchronized, 可重入

chapter 3
==============================

可见性, 过期数据， 64位没有原子操作(non-atomic 64-bit operations)， 锁和可见性， volatile变量

发布和逃逸(publication and escape)

-允许内部可变state escape
-隐式允许this引用 escape

安全构建

-使用factory方法阻止构建中this引用escape

线程约束

-ad-hoc thread confinement
-栈约束
-threadlocal

不可变性

-immutable objects are always thread safe.
-不可变类可以在下面构建可变对象
-final

安全发布

-简单在public域存储对象的引用是不够安全的发布
-不适当发布：when good object go bad
-不可变对象和安全初始化
-安全发布习俗
--在static初始化中初始化对象
--对象引用存在volatile和atomicReference
--对象引用存在正确构建的final字段中
--对象引用存在被lock正确保证的字段中

hashtable, synchronizedMap, Concurrent-Map, Vector, CopyOnWriteArrayList, CopyOnWrite-ArraySet, synchronizedList, synchronizedSet, BlockingQueue, ConcurrentLinkedQueue

Safely published effectively immutable objects can be used safely by any thread without additional synchronization.

安全共享对象

--Thread-confined
--shared read-only
--shared thread-safe
--guarded

chapter 4 composing objects
============================

定义线程安全类

-收集同步信息
-状态独立操作
-状态所有者

实例约束

-java monitor模式

Delegating Thread Safety

-独立的状态变量
-小心delegating failed
-publishing underlying state variable

给现有线程安全类添加功能

-客户端加锁
-组合方式

文档

chapter 5 building blocks
=================================

synchronized collections

-problems with synchronized collections
-迭代和并发修改异常
-隐式迭代器

concurrent collections

-concurrentHashMap
-copyOnWriteArrayList

Blocking Queues and Producer-consumer Pattern

-java.util.concurrent
-deque

Blocking and Interruptible Methods

Synchronizers

-Latches CountDownLatch, 
-FutureTask
-Semaphores
-Barriers CyclicBarrier

Building an Efficient, Scalable Result Cache

-using HashMap and synchronized
-replaceing HashMap with ConcurrentHashMap
-memorizing wrapper using FutureTask


chapter 6 Task Execution
=====================================

Executing Tasks in Threads

-顺序执行
-显示创建线程执行任务
-无限制创建线程的缺点

Executor Framework

-线程池
-executor 生命周期 ExecutorService- shutdownNow(), isShutdown(), isTerminated(), awitTermination()
-延迟和周期任务 ScheduledThreadPoolExecutor, DelayQueue, BlockingQueue

CompletionService

Future f.get(timeLeft, NANOSECONDS)

chapter 7 Cancellation and ShutDown
=========================================

Task Cancellation

-using volatile field to hold cancellation state

Interruption

-interrupt(), isInterrupted(), interrupted()
-Thread.currentThread().interrupt()
-对interruption的回应， throw interruptedException to caller, restore interruption before exit, 

cancellation via Future

encapsulating non standard cancellation with Newtaskfor

shutdown with poison pill

Handling Abnormal Thread Termination

-UncaughtExceptionHandler

JVM Shutdown

-shutdown Hooks
-Daemon Threads
-Finalizers


chapter 8 Applying Thread Pools
=====================================

Executor, 在主线程中submit子任务并等待子任务完成，造成死锁

线程池大小- 计算密集的是cpu数+1, i/o密集的需要更多

ThreadPoolExecutor创建， 可以提供自定义BlockingQueue, ThreadFactory和RejectedExecutionHandler

FIFO Queue: LinkedBlockingQueue, ArrayBlockingQueue
priority Queue: PriorityBlockingQueue

ThreadPoolExecutor  can be modified by calling setRejectedExecutionHandler, policy: AbortPolicy,CallerRunsPolicy , DiscardPolicy ,and DiscardOldestPolicy。

Thread Factories

Extending ThreadPoolExecutor


