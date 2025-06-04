
# 🧵 BlockingQueue in Java

## 📌 What is a BlockingQueue?

A `BlockingQueue` is a type of queue that **blocks** the thread:

- When trying to `add/put` an element if the queue is full.
- When trying to `remove/take` an element if the queue is empty.

Useful in **Producer-Consumer problems** and **Thread-safe task handling**.

---

## ✅ Key Methods

| Method         | Behavior                                                                 |
|----------------|--------------------------------------------------------------------------|
| `put(E e)`     | Waits if necessary for space to become available                         |
| `take()`       | Waits if necessary until an element becomes available                    |
| `offer(E e)`   | Inserts if possible, else returns false                                  |
| `poll()`       | Retrieves and removes the head or returns null if empty                  |
| `offer(E e, timeout, unit)` | Waits up to timeout for space                               |
| `poll(timeout, unit)`       | Waits up to timeout for element                             |

---

## 🏗️ Common Implementations

### 1. `ArrayBlockingQueue`

- Bounded (fixed-size), backed by array.
- Fairness option (FIFO by default).

```java
BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(5);
```

---

### 2. `LinkedBlockingQueue`

- Optionally bounded (default = unbounded).
- Backed by linked nodes.

```java
BlockingQueue<String> queue = new LinkedBlockingQueue<>();
```

---

### 3. `PriorityBlockingQueue`

- Unbounded, elements are ordered using Comparable or Comparator.
- Does **not** block on insertion; only blocks on removal when empty.

```java
BlockingQueue<Integer> queue = new PriorityBlockingQueue<>();
```

---

### 4. `DelayQueue`

- Unbounded queue of elements that implement `Delayed`.
- Element can be taken **only after its delay has expired**.

```java
DelayQueue<DelayedTask> delayQueue = new DelayQueue<>();
```

---

### 5. `SynchronousQueue`

- No internal capacity; each insert must wait for a matching take.
- Used for **hand-off** scenarios.

```java
BlockingQueue<String> queue = new SynchronousQueue<>();
```

---

## 💡 Producer-Consumer Example (ArrayBlockingQueue)

```java
BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(5);

Thread producer = new Thread(() -> {
    for (int i = 0; i < 10; i++) {
        queue.put(i);
        System.out.println("Produced: " + i);
    }
});

Thread consumer = new Thread(() -> {
    for (int i = 0; i < 10; i++) {
        int val = queue.take();
        System.out.println("Consumed: " + val);
    }
});

producer.start();
consumer.start();
```

---

## 🎯 Interview Follow-up Questions

### 🟢 Basic
- Implement Producer-Consumer with `ArrayBlockingQueue`.
- Difference between `put()` vs `offer()`?

| Method    | Blocking Behavior                 | Return Type | When to Use                           |
|-----------|-----------------------------------|-------------|----------------------------------------|
| `put()`   | Blocks if the queue is full       | `void`      | When you want to wait for space to insert |
| `offer()` | Does **not block** (immediate)    | `boolean`   | When you want to try inserting, and handle failure gracefully |
| `offer(E e, timeout, unit)` | Waits for specified time for space | `boolean` | When you want to insert, but don’t want to wait indefinitely |

---

### 🟡 Intermediate
- Use `PriorityBlockingQueue` to execute high-priority tasks first.
- How would you implement rate-limiting or retries using BlockingQueue?

### 🔴 Advanced
- Delay task processing by 5 seconds → Use `DelayQueue`.
- Design a retry system where each failed task is reprocessed after N seconds.

---

## 🧠 Bonus: DelayQueue Example

```java
class DelayedTask implements Delayed {
    private final String name;
    private final long startTime;

    public DelayedTask(String name, long delayMillis) {
        this.name = name;
        this.startTime = System.currentTimeMillis() + delayMillis;
    }

    public long getDelay(TimeUnit unit) {
        return unit.convert(startTime - System.currentTimeMillis(), TimeUnit.MILLISECONDS);
    }

    public int compareTo(Delayed other) {
        return Long.compare(this.startTime, ((DelayedTask) other).startTime);
    }

    public String toString() {
        return name;
    }
}

DelayQueue<DelayedTask> queue = new DelayQueue<>();
queue.put(new DelayedTask("Task1", 3000)); // 3 sec delay

System.out.println("Waiting for tasks...");
System.out.println("Executed: " + queue.take());
```

---

## 📚 Real-World Use Cases

- Thread-safe producer-consumer workflows.
- Job schedulers (via `DelayQueue`).
- Task prioritization (via `PriorityBlockingQueue`).
- Message passing between threads (via `SynchronousQueue`).
