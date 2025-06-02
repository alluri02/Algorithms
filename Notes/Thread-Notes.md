# Java Threads Notes

## What is a Thread?
- A **thread** is a lightweight unit of execution within a program.
- Java supports **multithreading**, allowing multiple threads to run concurrently.
- The **main thread** starts automatically when the program runs.
- Additional threads can be created for multitasking.

---

## Ways to Create Threads in Java

### 1. Extending `Thread` Class
- Create a subclass of `Thread`.
- Override the `run()` method with task logic.
- Call `start()` to begin execution (which internally calls `run()`).

**Example:**
```java
class MyThread extends Thread {
    public void run() {
        System.out.println("Thread running: " + Thread.currentThread().getName());
    }
}

public class Test {
    public static void main(String[] args) {
        MyThread t1 = new MyThread();
        t1.start();  // Starts new thread
    }
}
```

### 2. Implementing Runnable Interface

- Implement the `Runnable` interface.
- Override the `run()` method with the task logic.
- Pass the `Runnable` instance to a `Thread` object.
- Call `start()` on the `Thread` to begin execution.

**Example:**

```java
class MyRunnable implements Runnable {
    public void run() {
        System.out.println("Runnable running: " + Thread.currentThread().getName());
    }
}

public class Test {
    public static void main(String[] args) {
        MyRunnable task = new MyRunnable();
        Thread t1 = new Thread(task);
        t1.start();
    }
}
```
### 3. Using Lambda Expressions (Java 8+)
- Use lambda expressions to simplify thread creation.
- Directly pass the lambda to a `Thread` constructor.
```java
Thread t1 = new Thread(() -> {
    System.out.println("Lambda thread running: " + Thread.currentThread().getName());
});
t1.start();
```
### 4. Using Executor Framework
- Use `ExecutorService` for managing thread pools.
- Submit tasks to the executor for execution.
- Automatically handles thread management.
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
ExecutorService executor = Executors.newFixedThreadPool(2);
executor.submit(() -> {
    System.out.println("Executor thread running: " + Thread.currentThread().getName());
});
executor.shutdown();
```
### 5. Using ForkJoinPool
- Use `ForkJoinPool` for parallel processing of tasks.
```java
import java.util.concurrent.ForkJoinPool;
ForkJoinPool forkJoinPool = new ForkJoinPool();
forkJoinPool.submit(() -> {
    System.out.println("ForkJoinPool thread running: " + Thread.currentThread().getName());
}).join();
```
### 6. Using CompletableFuture
- Use `CompletableFuture` for asynchronous programming.
- Allows non-blocking execution of tasks.
```java
import java.util.concurrent.CompletableFuture;
CompletableFuture.runAsync(() -> {
    System.out.println("CompletableFuture thread running: " + Thread.currentThread().getName());
});
```
### 7. Using ScheduledExecutorService
- Use `ScheduledExecutorService` for scheduling tasks.
- Allows tasks to run after a delay or periodically.
```java
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
ScheduledExecutorService scheduledExecutor = Executors.newScheduledThreadPool(1);
scheduledExecutor.schedule(() -> {
    System.out.println("Scheduled task running: " + Thread.currentThread().getName());
}, 5, TimeUnit.SECONDS);
scheduledExecutor.shutdown();
```
### 8. Using Thread Pools
- Use thread pools to manage multiple threads efficiently.
- Reduces overhead of thread creation.
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
ExecutorService threadPool = Executors.newCachedThreadPool();
threadPool.execute(() -> {
    System.out.println("Thread pool task running: " + Thread.currentThread().getName());
});
threadPool.shutdown();
```
### 9. Using Future and Callable
- Use `Callable` for tasks that return a result.
- Use `Future` to retrieve the result of the task.
```java
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
ExecutorService executor = Executors.newFixedThreadPool(1);
Callable<Integer> task = () -> {
    return 42; // Example task returning a result
};
Future<Integer> future = executor.submit(task);
try {
    Integer result = future.get(); // Blocking call to get the result
    System.out.println("Task result: " + result);
} catch (InterruptedException | ExecutionException e) {
    e.printStackTrace();
} finally {
    executor.shutdown();
}
```
### 10. Using ThreadLocal
- Use `ThreadLocal` to maintain variables that are local to a thread.
- Useful for storing user-specific data in a multithreaded environment.
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
ThreadLocal<String> threadLocal = ThreadLocal.withInitial(() -> "Default Value");
ExecutorService executor = Executors.newFixedThreadPool(2);
executor.submit(() -> {
    threadLocal.set("Thread 1 Value");
    System.out.println("Thread 1: " + threadLocal.get());
});
executor.submit(() -> {
    threadLocal.set("Thread 2 Value");
    System.out.println("Thread 2: " + threadLocal.get());
});
executor.shutdown();
```
