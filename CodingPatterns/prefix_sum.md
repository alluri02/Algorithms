# ➕ Prefix Sum Pattern

## 🔍 Intuition

The **Prefix Sum** pattern is a powerful technique used to optimize problems involving **repeated sum calculations** over a subarray or range.

The idea is simple: **precompute cumulative sums** so that sum queries can be answered in constant time.

Instead of recalculating sums again and again (O(n) each), we calculate them once and reuse them (O(1)).

---

## 🧩 Real-World Analogy

Imagine you have a running balance sheet of your expenses. Instead of adding from scratch every time, you maintain a **running total** so that you can get the sum between two dates instantly by subtracting two totals.

---

## 💡 Example: [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) (Medium)

### ❓ Problem

Given an integer array `nums` and an integer `k`, return the total number of **continuous subarrays** whose sum equals to `k`.

---

## 🔑 Intuition

Use a **prefix sum** to keep track of cumulative sums. Use a **HashMap** to store how many times a particular prefix sum has occurred.

If `currSum - k` exists in the map, it means there’s a subarray ending at the current index with sum = `k`.

---

## ✅ Java Code

```java
public int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> prefixSumCount = new HashMap<>();
    prefixSumCount.put(0, 1); // base case

    int count = 0, sum = 0;

    for (int num : nums) {
        sum += num;
        if (prefixSumCount.containsKey(sum - k)) {
            count += prefixSumCount.get(sum - k);
        }
        prefixSumCount.put(sum, prefixSumCount.getOrDefault(sum, 0) + 1);
    }

    return count;
}
```

## 📊 Complexity

| Approach               | Time   | Space |
|------------------------|--------|--------|
| Brute-force (nested loop) | O(n²) | O(1)   |
| Prefix sum + HashMap      | O(n)  | O(n)   |

---

## 🧠 Key Takeaway

Prefix sums turn expensive repeated sum computations into quick subtractions, allowing **range-sum queries to run in constant time**.

---

## 🧪 Visual

For array: `[1, 2, 3]`, prefix sums are:

```
1. `0` (before any elements)
2. `1` (sum of first element)
3. `3` (sum of first two elements) 
4. `6` (sum of all three elements)
```

## 📊 Complexity

| Approach               | Time   | Space |
|------------------------|--------|--------|
| Brute-force (nested loop) | O(n²) | O(1)   |
| Prefix sum + HashMap      | O(n)  | O(n)   |

---


---

## 📝 Practice Problems

| Problem | Pattern Variant |
|--------|------------------|
| [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | HashMap + Prefix |
| [Find Pivot Index](https://leetcode.com/problems/find-pivot-index/) | Prefix from both ends |
| [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) | Precompute prefix |
| [Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/) | Modulo with prefix sum |
| [Maximum Size Subarray Sum Equals k](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/) | Longest prefix subarray |
| [Minimum Operations to Reduce X to Zero](https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/) | Convert to prefix sum match |
| [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | Prefix sum with binary search |

---

## 📌 When to Use

- Frequent range or subarray sum queries  
- You can preprocess the array  
- You want to avoid nested loops  
- You can afford O(n) extra space  
