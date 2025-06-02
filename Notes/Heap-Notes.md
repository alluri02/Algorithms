# 📚 Heap Notes

---

## 1. What is a Heap?

- A **Heap** is a **complete binary tree** satisfying the **heap property**:
  - **Max Heap:** Parent node ≥ children
  - **Min Heap:** Parent node ≤ children
- Commonly implemented using arrays for efficiency.
- Useful for priority queues, sorting algorithms (Heap Sort), and top-k problems.

---

## 2. Types of Heaps

| Heap Type | Property                      | Root Node Holds           |
|-----------|-------------------------------|--------------------------|
| Max Heap  | Parent ≥ children              | Maximum element          |
| Min Heap  | Parent ≤ children              | Minimum element          |

---

## 3. Common Heap Operations & Time Complexity

| Operation      | Description                                    | Time Complexity      |
|----------------|------------------------------------------------|---------------------|
| `offer()` / `add()`     | Add an element, maintain heap property         | O(log n)            |
| `peek()`       | Return root element without removal             | O(1)                |
| `poll()` / `remove()` | Remove root element, heapify down          | O(log n)            |
| `buildHeap()`  | Convert an array into a heap                     | O(n)                |
| `heapify()`    | Restore heap property by sifting up/down        | O(log n)            |

---

## 🧠 Understanding `buildHeap()` – Why is the Time Complexity O(n)?

The time complexity of `buildHeap()` (which converts an array into a valid heap) is **O(n)** — even though it appears we are looping through `n/2` elements. Here's why.

---

### 🔑 Key Insight: Not All `heapify()` Calls Take Equal Time

The trick lies in how **deep** the `heapify()` call might go:

- Nodes **near the bottom** (close to leaves) can only move a little.
- Nodes **near the top** (like the root) can sink deeper and require more operations.

---

### 📊 Level-wise Cost Analysis

We analyze the cost based on the depth of each node:

| Level (from bottom) | Number of Nodes | Max Heapify Work (Depth) |
|---------------------|------------------|---------------------------|
| h (leaves)          | n / 2            | 0                         |
| h - 1               | n / 4            | 1                         |
| h - 2               | n / 8            | 2                         |
| ...                 | ...              | ...                       |
| 0 (root)            | 1                | h                         |

---

### 📈 Total Cost

```text
T(n) = (n/2) * 0 + (n/4) * 1 + (n/8) * 2 + (n/16) * 3 + ... + 1 * h
     < n * (1/4 + 2/8 + 3/16 + ...)
     = O(n)
```

## 4. Common Methods in Java's PriorityQueue (Min Heap by default)

```java
PriorityQueue<Integer> minHeap = new PriorityQueue<>();

minHeap.offer(10);         // insert element
minHeap.peek();            // get min element
minHeap.poll();            // remove min element
minHeap.size();            // get size
minHeap.contains(10);      // check if element present
minHeap.clear();          // remove all elements
```

# 📝 Interview Questions on Heaps with Answers

---

### 1. Explain the difference between a binary heap and a binary search tree (BST).

- **Binary Heap**:
  - Complete binary tree (all levels filled except possibly last, filled from left to right).
  - Satisfies heap property: parent node is either greater than or equal to children (max heap) or less than or equal (min heap).
  - No ordering between siblings or subtrees.
  - Used for priority queues, heap sort.

- **Binary Search Tree (BST)**:
  - Not necessarily complete.
  - For each node, left subtree values < node value < right subtree values.
  - Supports efficient search, insert, delete operations.
  - Used for ordered data storage.

---

### 2. How does a heap differ from a priority queue?

- **Heap** is a data structure (usually implemented as an array-based complete binary tree) that maintains the heap property.
- **Priority Queue** is an abstract data type that supports extracting the highest (or lowest) priority element.
- In Java, PriorityQueue is often implemented internally using a heap.

---

### 3. How to implement a min heap and max heap?

- Use an array to represent a complete binary tree.
- For **min heap**: Parent ≤ children.
- For **max heap**: Parent ≥ children.
- Key operations: `insert` (bubble up), `remove` (heapify down).
- In Java, use `PriorityQueue` with natural ordering for min heap, or custom comparator (e.g., reverse order) for max heap.

---

### 4. What is the time complexity to build a heap from an unsorted array?

- Using the **heapify** process: **O(n)**.
- Naively inserting each element: **O(n log n)**.
- Heapify starts from the last non-leaf node and heapifies downward.

---

### 5. How do you find the kth largest element in an array?

- Use a **min heap** of size k.
- Insert first k elements.
- For the rest, if current element > heap root, replace root and heapify.
- Result is the root of min heap after processing all elements.
- Time complexity: **O(n log k)**.

---

### 6. Explain Heap Sort and its time complexity.

- Build a max heap from the array.
- Repeatedly swap the root (max element) with the last element.
- Reduce heap size by one and heapify root.
- Result is a sorted array in ascending order.
- Time complexity: **O(n log n)** (build heap O(n) + n extractions O(n log n)).

---

### 7. How to merge K sorted arrays efficiently using heaps?

- Use a **min heap** to keep track of the smallest element among the arrays.
- Insert the first element of each array with metadata (array index, element index).
- Extract min and insert next element from the same array.
- Repeat until all arrays are exhausted.
- Time complexity: **O(N log K)** where N is total elements.

---

### 8. What are the advantages of using a heap over other data structures?

- Efficiently supports priority queue operations.
- Fast insertion and deletion in O(log n).
- Can find min or max in O(1).
- Better for partial sorting or streaming data.

---

### 9. How does a heap maintain its properties after insertion and deletion?

- **Insertion**: Insert at the end, then "bubble up" (swap with parent if heap property violated).
- **Deletion** (usually root): Replace root with last element, then "heapify down" by swapping with smaller/larger child.

---

### 10. Write code to convert a binary tree into a heap.

```java
// Assuming array representation of binary tree
public void buildHeap(int[] arr) {
    int n = arr.length;
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }
}

private void heapify(int[] arr, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }
    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }

    if (largest != i) {
        int temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;
        heapify(arr, n, largest);
    }
}
```
---
### 11. What is the space complexity of a heap?
- The space complexity of a heap is **O(n)**, where n is the number of elements in the heap.
- This is because a heap is typically implemented using an array, which requires space proportional to the number of elements it contains.
- In addition, the heap structure itself does not require any additional space beyond the array used to store the elements.
---
### 12. How do you check if a binary tree is a heap?
- To check if a binary tree is a heap, you need to verify two conditions:
  1. **Complete Binary Tree**: The tree must be complete, meaning all levels are fully filled except possibly the last level, which should be filled from left to right.
  2. **Heap Property**: For a max heap, every parent node must be greater than or equal to its children; for a min heap, every parent node must be less than or equal to its children.


# 📚 Heap Data Structure – Important Problems for Practice

Practicing heap (priority queue) problems helps you strengthen your skills in greedy algorithms, sorting, and efficient data processing.

---

## 🔰 Beginner-Level Heap Problems

1. **Kth Largest/Smallest Element in an Array**
   - [Kth Largest Element](https://leetcode.com/problems/kth-largest-element-in-an-array/)
   - [Kth Smallest Element](https://www.geeksforgeeks.org/kth-smallestlargest-element-unsorted-array/)

2. **Sort a Nearly Sorted (K-sorted) Array**
   - [GFG - Sort a K-Sorted Array](https://www.geeksforgeeks.org/nearly-sorted-algorithm/)

3. **Top K Frequent Elements**
   - [Leetcode - Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)

---

## ⚙️ Intermediate-Level Heap Problems

4. **Merge K Sorted Lists**
   - [Leetcode - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)

5. **Find Median from Data Stream**
   - [Leetcode - Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)

6. **Sliding Window Maximum**
   - [Leetcode - Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)

7. **Reorganize String**
   - [Leetcode - Reorganize String](https://leetcode.com/problems/reorganize-string/)

---

## 🚀 Advanced-Level Heap Problems

8. **Trapping Rain Water II (2D elevation map)**
   - [Leetcode - Trapping Rain Water II](https://leetcode.com/problems/trapping-rain-water-ii/)

9. **IPO Problem (Maximize Capital)**
   - [Leetcode - IPO](https://leetcode.com/problems/ipo/)

10. **Smallest Range Covering Elements from K Lists**
    - [Leetcode - Smallest Range](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/)

---

## 🧠 Tips for Practicing Heap Problems

- Understand the difference between **min-heap** and **max-heap**.
- Practice building a heap from scratch to understand internal structure.
- Use Python's `heapq`, Java’s `PriorityQueue`, or C++'s `priority_queue`.

---

Happy Coding! 🚀
