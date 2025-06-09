# 🧠 Two Pointer Pattern

## 🔍 Intuition

The Two Pointer pattern is a technique where you use two pointers to iterate through a data structure—usually an array or string—to solve problems involving pairs, subarrays, or rearrangement efficiently. It's particularly powerful when dealing with **sorted arrays**, **palindromes**, or **in-place** transformations.

Instead of using nested loops (O(n²)), the two-pointer method allows **linear-time solutions** (O(n)) for many such problems.

## 🧩 Real-World Analogy

Imagine you and a friend are trying to find a specific item in a long line of boxes. You start at opposite ends and move towards each other, checking boxes as you go. This way, you can find the item much faster than if one of you checked every box sequentially.

Imagine two people searching for a specific page in a book by checking from opposite ends—they meet faster than one person checking every single page.

---

## 💡 Example: [Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/) (Medium)

### ❓ Problem:

Given a string `s`, return `true` if the `s` can be a palindrome **after deleting at most one character** from it.

### 🔑 Intuition

Use two pointers `left` and `right`. If characters at both match, move inward. If they don’t, try skipping either the left or right character once.

### ✅ Java Code

```java
public boolean validPalindrome(String s) {
    int left = 0, right = s.length() - 1;

    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) {
            return isPalindrome(s, left + 1, right) || isPalindrome(s, left, right - 1);
        }
        left++;
        right--;
    }
    return true;
}

private boolean isPalindrome(String s, int left, int right) {
    while (left < right) {
        if (s.charAt(left++) != s.charAt(right--)) return false;
    }
    return true;
}
```

## 📊 Complexity

| Approach     | Time   | Space |
|--------------|--------|--------|
| Brute-force  | O(n²)  | O(1)   |
| Two-pointer  | O(n)   | O(1)   |

---

## 🧠 Key Takeaway

Two pointers remove the need for repeated scanning, reducing nested loops to a single linear pass.

---

## 🧪 Visual

```
Example: "abca" - Can become palindrome by deleting at most one char?

Initial check:
"abca"
 ↑   ↑
 L   R   'a' == 'a', move pointers inward

After moving:
"ab c a"
  ↑ ↑
    L R   'b' != 'c', need to check two possibilities

Skip left char ('b'):         Skip right char ('c'):
"a[b]ca"                      "ab[c]a"
     ↓                             ↓
"a ca"                        "ab a" 
    ↑↑                           ↑↑  
    LR   'c' == 'a'? No         LR   'b' == 'a'? No

Wait! Try comparing remaining chars:

"a ca"                        "ab a" 
     ↑                             ↑
     L   'c' != 'a'? No            L   'b' != 'a'? No
        ↑                             ↑
        R                             R

Result: TRUE (Can form "aca" by removing 'b')
```

---

## 📝 Practice Problems

| Problem | Pattern Variant |
|--------|------------------|
| [Two Sum II - Input array is sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Pair with sum |
| [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Clean string + check |
| [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Max area |
| [3Sum](https://leetcode.com/problems/3sum/) | Sort + Two Pointer |
| [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | In-place write |
| [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | End-to-start merge |

---

## 📌 When to Use

- Array/string problems  
- You can sort (or the array is already sorted)  
- Looking for pairs or palindromes  
- Need O(1) space and O(n) time  
