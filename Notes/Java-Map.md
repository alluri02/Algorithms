# 📘 Java `Map` Overview

Java `Map` is a part of the `java.util` package and is used to store **key-value pairs**, where **keys are unique** and each key maps to a **single value**.

---

## 🔹 Common Implementations

| Implementation       | Ordered?             | Sorted?                        | Allows nulls?                        |
|----------------------|----------------------|--------------------------------|--------------------------------------|
| `HashMap`            | ❌ No order          | ❌                             | ✅ One null key, many null values    |
| `LinkedHashMap`      | ✅ Insertion order   | ❌                             | ✅                                    |
| `TreeMap`            | ❌                   | ✅ (natural or custom order)   | ❌ No null keys                      |
| `ConcurrentHashMap`  | ❌                   | ❌                             | ❌ No null keys or values            |

---

## 🗂 When to Use TreeMap, LinkedHashMap, Hashtable, or HashMap in Java

| Map Type         | Ordering                  | Thread Safety        | Null Keys/Values Allowed | Use Case / When to Use                                           |
|------------------|---------------------------|---------------------|--------------------------|------------------------------------------------------------------|
| **HashMap**      | No guaranteed order       | Not thread-safe     | One null key, many null values | General-purpose, fast insert/search, when order doesn’t matter   |
| **LinkedHashMap**| Maintains insertion order | Not thread-safe     | One null key, many null values | When you need predictable iteration order (insertion or access) |
| **TreeMap**      | Sorted by key (natural or comparator) | Not thread-safe | No null keys, allows null values (depends on comparator) | When sorted order of keys is required                            |
| **Hashtable**    | No guaranteed order       | Thread-safe (synchronized) | No null keys or values    | Legacy code requiring thread safety, prefer `ConcurrentHashMap` now |

### Summary:

- Use **HashMap** for fast, unsorted key-value storage.
- Use **LinkedHashMap** if iteration order matters (e.g., cache implementations).
- Use **TreeMap** if you need keys sorted (e.g., range queries).
- Use **Hashtable** only for legacy thread-safe code; otherwise prefer `ConcurrentHashMap`.

---

## 🔹 Basic Operations

```java
Map<String, Integer> map = new HashMap<>();

// Add or update entries
map.put("apple", 2);
map.put("banana", 3);

// Get value by key
int count = map.get("apple");  // returns 2

// Check if key exists
boolean hasKey = map.containsKey("banana");

// Remove key
map.remove("banana");

// Size of map
int size = map.size();

// Clear map
map.clear();

```

## 🔹 Important Methods with Examples

### ✅ `getOrDefault()`
Returns the value for a key, or a default if the key is missing.

```java
int value = map.getOrDefault("orange", 0); // returns 0 if "orange" not found
```

### ✅ `putIfAbsent()`

Inserts only if the key is not already present.

```java
map.putIfAbsent("grape", 5); // adds only if "grape" is not already in map
```


### ✅ `computeIfAbsent()`

Computes and inserts a value only if the key is absent.

```java
Map<String, List<String>> groupMap = new HashMap<>();

groupMap.computeIfAbsent("anagram", k -> new ArrayList<>()).add("nagaram");
```

### ✅ `keySet()`, `values()`, `entrySet()`

These methods help you access different views of the map:

- `keySet()` – returns a `Set` of all keys.
- `values()` – returns a `Collection` of all values.
- `entrySet()` – returns a `Set` of key-value pairs as `Map.Entry` objects.

```java
Map<String, Integer> map = new HashMap<>();
map.put("apple", 2);
map.put("banana", 3);

Set<String> keys = map.keySet();              // Set of keys
Collection<Integer> vals = map.values();      // Collection of values
Set<Map.Entry<String, Integer>> entries = map.entrySet(); // Set of entries

```
## 🔧 Useful Methods in Java `Map` (with Examples)

| Method                        | Description                                      | Example                                                |
|------------------------------|--------------------------------------------------|--------------------------------------------------------|
| `put(key, value)`            | Inserts or updates a key-value pair              | `map.put("apple", 5);`                                 |
| `get(key)`                   | Retrieves the value for a key                    | `int val = map.get("apple");`                          |
| `containsKey(key)`           | Checks if the key exists                         | `map.containsKey("banana");`                           |
| `containsValue(value)`       | Checks if the value exists                       | `map.containsValue(10);`                               |
| `remove(key)`                | Removes the key and its value                    | `map.remove("apple");`                                 |
| `keySet()`                   | Returns a `Set` of all keys                      | `Set<String> keys = map.keySet();`                     |
| `values()`                   | Returns a `Collection` of all values             | `Collection<Integer> vals = map.values();`             |
| `entrySet()`                 | Returns a `Set` of key-value pairs               | `for (var e : map.entrySet()) {}`                      |
| `getOrDefault(key, default)` | Returns value or default if not found            | `int val = map.getOrDefault("orange", 0);`             |
| `putIfAbsent(key, value)`    | Puts only if key isn't present                   | `map.putIfAbsent("grape", 3);`                         |
| `computeIfAbsent(key, func)` | Computes and puts value if key is absent         | `map.computeIfAbsent("a", k -> new ArrayList<>());`    |


# Java Map Internal Implementation — Interview Questions & Detailed Answers

---

## 1. How does `HashMap` work internally?

`HashMap` stores key-value pairs in an array of **buckets**, where each bucket corresponds to a **hash code** computed from the key.

- When you insert a key-value pair, the key’s `hashCode()` is computed.
- This hash is then transformed (using bitwise operations) to determine the bucket index.
- If multiple keys map to the same bucket (hash collision), they are stored in a linked list or a balanced tree (Java 8+).
- When the number of entries exceeds the product of the load factor (default 0.75) and the bucket array size, the map **resizes** — doubling the bucket array and redistributing entries.

---

# Why Does `HashMap` Allow One Null Key in Java?

`HashMap` in Java allows **one null key** because of how it handles hashing and storage internally:

- **Null key is treated specially:**  
  When you put a key-value pair with a `null` key, `HashMap` doesn’t call `hashCode()` on the key (which would cause a `NullPointerException` if it tried). Instead, it stores the entry in a **special bucket dedicated for the null key**.

- **Why only one null key?**  
  Since keys in a `Map` must be unique, there can be only one null key. If you insert another null key, it will **replace the previous null key’s value**.

- **Difference from `Hashtable`:**  
  `Hashtable` does **not allow null keys or null values** because it was designed before Java 1.2 and is synchronized, so it avoids nulls to prevent ambiguity and potential errors.

- **In contrast, `TreeMap` doesn’t allow null keys** because it relies on keys being comparable (via `compareTo()` or a `Comparator`), and `null` cannot be compared.

### Summary

| Map Implementation | Null Key Allowed? | Reason                              |
|--------------------|-------------------|-----------------------------------|
| `HashMap`          | Yes (only one)    | Special handling; stores in null bucket |
| `Hashtable`        | No                | Legacy, synchronized, avoids nulls |
| `TreeMap`           | No                | Keys must be comparable; null cannot be compared |

---

### Quick Example:

```java
Map<String, Integer> map = new HashMap<>();
map.put(null, 10);
map.put(null, 20);  // replaces previous null key value
System.out.println(map.get(null));  // Output: 20
```

## 2. What is the difference between `HashMap` and `Hashtable` internally?

| Aspect               | HashMap                       | Hashtable                     |
|----------------------|------------------------------|-------------------------------|
| Synchronization      | Not synchronized (not thread-safe) | Synchronized (thread-safe)    |
| Null keys/values     | Allows one null key and multiple null values | Does **not** allow null keys or null values |
| Performance         | Faster in single-threaded contexts | Slower due to synchronization overhead |
| Legacy              | Part of Java Collections Framework (Java 1.2+) | Legacy class (since JDK 1.0)  |

---

## 3. How does `LinkedHashMap` maintain insertion order?

`LinkedHashMap` extends `HashMap` and maintains a **doubly-linked list** running through all its entries.

- Each entry contains pointers to its **before** and **after** entries.
- This linked list preserves **insertion order** (or access order, if specified).
- The linked list traversal provides predictable iteration order.

---

## 4. How does `TreeMap` work internally?

`TreeMap` implements a **Red-Black tree** (a self-balancing binary search tree).

- Keys are ordered either by their **natural ordering** (i.e., they implement `Comparable`) or by a **Comparator** provided at map creation.
- Operations like `put()`, `get()`, and `remove()` run in **O(log n)** time because they involve traversing the tree.

---

## 5. What is the significance of the `hashCode()` and `equals()` methods in `HashMap`?

- `hashCode()` determines the **bucket location** for a key.
- `equals()` is used to check **key equality** within a bucket (when collisions occur).
- If two keys have the same hash code, `equals()` ensures correct retrieval and update.
- If these methods are not properly overridden, map behavior will be incorrect (e.g., duplicate keys).

---

## 6. How does `HashMap` handle collisions?

- Java uses **separate chaining**: each bucket holds a linked list (or a balanced tree if the list grows beyond a threshold).
- When a collision occurs (multiple keys in the same bucket), keys are compared using `equals()` to find the correct entry.
- Since Java 8, when the number of entries in a bucket exceeds 8, the linked list is converted into a **balanced tree** to improve performance from O(n) to O(log n).

---

## 7. What happens when the load factor exceeds the threshold in a `HashMap`?

- The **load factor** (default 0.75) defines when to resize.
- When `size > loadFactor * capacity`, the map **doubles the capacity** (resizes).
- All entries are **rehashed** and redistributed across the new buckets.
- This operation is costly (O(n)), but it helps maintain **average O(1) access time**.

---

## 8. Why is the default load factor of `HashMap` 0.75?

- 0.75 provides a good balance between **space** and **time efficiency**.
- A **higher load factor** means fewer resizes but more collisions, leading to longer chains and slower access.
- A **lower load factor** reduces collisions but increases memory consumption.
- 0.75 is empirically found to minimize overall cost.

---

## 9. How does `computeIfAbsent()` work internally?

- If the key is **absent** or mapped to `null`, the mapping function is invoked to compute a new value.
- This value is inserted into the map and returned.
- Avoids unnecessary computation or insertion if the key is already present.
- Example:
  ```java
  map.computeIfAbsent(key, k -> new ArrayList<>()).add(value);
    ```


# Important Algorithm Problems to Practice Using Map in Java

## 1. Frequency Counting & Hashing
- **Top K Frequent Elements**  
  Find the k most frequent elements in an array.  
  *Example:* LeetCode 347, 692

- **Valid Anagram**  
  Check if two strings are anagrams using character frequency maps.  
  *Example:* LeetCode 242

- **Group Anagrams**  
  Group a list of strings into anagrams.  
  *Example:* LeetCode 49

- **Two Sum**  
  Find two numbers that add up to a target using a map for lookups.  
  *Example:* LeetCode 1

- **Subarray Sum Equals K**  
  Count subarrays with sum equal to k using prefix sum and map.  
  *Example:* LeetCode 560

## 2. Sliding Window + Map
- **Longest Substring Without Repeating Characters**  
  Use a map to track last seen positions of characters.  
  *Example:* LeetCode 3

- **Minimum Window Substring**  
  Find the smallest substring containing all chars of another string.  
  *Example:* LeetCode 76

- **Find All Anagrams in a String**  
  Use maps to track character counts in sliding window.  
  *Example:* LeetCode 438

## 3. Pattern Matching and Mapping
- **Isomorphic Strings**  
  Map characters from one string to another ensuring one-to-one mapping.  
  *Example:* LeetCode 205

- **Word Pattern**  
  Check if string follows the same pattern using map between pattern and words.  
  *Example:* LeetCode 290

## 4. Other Map-Based Challenges
- **Copy List with Random Pointer**  
  Use a map to clone nodes with random pointers.  
  *Example:* LeetCode 138

- **Longest Consecutive Sequence**  
  Use map/set to track consecutive elements in O(n).  
  *Example:* LeetCode 128

- **Evaluate Division**  
  Represent equations as graph edges using maps for quick lookup.  
  *Example:* LeetCode 399

- **Find Duplicate Subtrees**  
  Serialize subtree structures and map to counts for duplicates.  
  *Example:* LeetCode 652

---

# Tips for Practice

- Always think about **key-value relationships** for frequency, indexing, or mapping.
- Maps excel when you need **O(1) average lookups**.
- Combine with arrays, sets, or heaps for more complex solutions.
- Practice both **hash maps** and **tree maps** to understand ordering and sorting.

---

# Important Algorithm Problems Using Map + Heap (Priority Queue)

## 1. Top K Frequent Elements
- Find the k most frequent elements in an array or string using a frequency map and a min-heap.  
- *Example:* LeetCode 347 (Top K Frequent Elements), LeetCode 692 (Top K Frequent Words)

## 2. Merge K Sorted Lists / Arrays
- Merge k sorted linked lists or arrays using a priority queue for efficient selection and a map for indexing/counting.  
- *Example:* LeetCode 23 (Merge k Sorted Lists)

## 3. Task Scheduler
- Schedule tasks with cooldowns using a frequency map and a max-heap to always pick the most frequent next task.  
- *Example:* LeetCode 621 (Task Scheduler)

## 4. Sliding Window Maximum
- Find the maximum in each sliding window of size k using a map (to count occurrences) and a max-heap (to get max efficiently).  
- *Example:* LeetCode 239 (Sliding Window Maximum)

## 5. Find K Closest Points to Origin
- Use a min-heap to store points by distance, and a map for frequency or indexing if needed.  
- *Example:* LeetCode 973 (K Closest Points to Origin)

## 6. Reorganize String
- Rearrange characters so no two adjacent are the same using a frequency map and max-heap.  
- *Example:* LeetCode 767 (Reorganize String)

## 7. Sort Characters By Frequency
- Sort characters by their frequency using a map for counting and a max-heap for sorting by frequency.  
- *Example:* LeetCode 451 (Sort Characters By Frequency)

## 8. Median in a Data Stream
- Maintain two heaps (max-heap and min-heap) and maps for counts to find median in real-time.  
- *Example:* LeetCode 295 (Find Median from Data Stream)

---

# Tips for Map + Heap Problems
- Use **Map** for frequency/count or quick access to related data.
- Use **Heap** for ordering based on priority (like frequency, distance, or value).
- Combine them to efficiently maintain and query dynamic data.
- Often use min-heap for top k smallest, max-heap for top k largest or most frequent.

---

# Important Algorithm Problems Using Map + Stack

## 1. Valid Parentheses
- Use a stack to check matching pairs of parentheses and a map to store bracket pairs.  
- *Example:* LeetCode 20 (Valid Parentheses)

## 2. Next Greater Element
- Use a stack to track elements and a map to store the next greater element for each.  
- *Example:* LeetCode 496 (Next Greater Element I & II)

## 3. Largest Rectangle in Histogram
- Use a stack to track bars and a map or array to record indices/heights for area calculation.  
- *Example:* LeetCode 84 (Largest Rectangle in Histogram)

## 4. Basic Calculator II / III
- Use a stack for numbers and operators; a map can store operator precedence.  
- *Example:* LeetCode 227 (Basic Calculator II), LeetCode 772 (Basic Calculator III)

## 5. Decode String
- Use stacks to keep track of counts and partial decoded strings, map can hold character mappings or counts.  
- *Example:* LeetCode 394 (Decode String)

## 6. Score of Parentheses
- Use a stack to track scores of balanced parentheses and map for scoring rules.  
- *Example:* LeetCode 856 (Score of Parentheses)

## 7. Remove Duplicate Letters
- Use a stack to build result and a map to track the last occurrence index of each letter.  
- *Example:* LeetCode 316 (Remove Duplicate Letters)

## 8. Sliding Window Maximum (Alternative)
- Stack-based monotonic stack can be combined with map for index checks.  
- *Example:* LeetCode 239 (Sliding Window Maximum)

---

# Tips for Map + Stack Problems
- **Stack** is used to maintain order, especially last-in-first-out (LIFO) structures.
- **Map** complements stack by tracking indices, last occurrences, or specific element relations.
- Great combo for parsing, matching, and sequence processing problems.

---

# Important Algorithm Problems Using Map + Graph

## 1. Number of Islands
- Use a map or adjacency list to represent grid cells and DFS/BFS to traverse connected components.  
- *Example:* LeetCode 200 (Number of Islands)

## 2. Clone Graph
- Use a map to keep track of visited nodes and their clones to avoid cycles during DFS/BFS.  
- *Example:* LeetCode 133 (Clone Graph)

## 3. Course Schedule (Detect Cycle in Directed Graph)
- Use maps to store adjacency lists and states of nodes (unvisited, visiting, visited) for cycle detection.  
- *Example:* LeetCode 207 (Course Schedule)

## 4. Alien Dictionary
- Build a graph using maps for adjacency and in-degree tracking, then topological sort.  
- *Example:* LeetCode 269 (Alien Dictionary)

## 5. Word Ladder
- Use a map for adjacency or word patterns to efficiently find neighbors in BFS traversal.  
- *Example:* LeetCode 127 (Word Ladder)

## 6. Pacific Atlantic Water Flow
- Use maps to mark reachable cells for each ocean, then intersect results.  
- *Example:* LeetCode 417 (Pacific Atlantic Water Flow)

## 7. Network Delay Time
- Use maps to store weighted adjacency lists and Dijkstra’s algorithm to find shortest path.  
- *Example:* LeetCode 743 (Network Delay Time)

## 8. Number of Connected Components in an Undirected Graph
- Use maps for adjacency lists and DFS/BFS to count connected components.  
- *Example:* LeetCode 323 (Number of Connected Components in an Undirected Graph)

## 9. Cheapest Flights Within K Stops
- Use maps to build weighted graph, BFS/DFS with pruning or Dijkstra variants to find cheapest cost.  
- *Example:* LeetCode 787 (Cheapest Flights Within K Stops)

## 10. Graph Valid Tree
- Use maps for adjacency and visited set to check if graph is a valid tree.  
- *Example:* LeetCode 261 (Graph Valid Tree)

---

# Tips for Map + Graph Problems
- Use **Map<Node, List<Node>>** for adjacency lists, especially when nodes are complex objects or not integers.
- Use maps to track visited status or distances when nodes aren’t simple indexes.
- Maps help with graphs that have non-integer or string-labeled nodes.
- Combine maps with DFS, BFS, Dijkstra, or Topological Sorting algorithms.

---



