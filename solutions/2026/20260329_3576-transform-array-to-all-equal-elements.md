# #3576. 将数组转换为全相等元素 / Transform Array to All Equal Elements

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/transform-array-to-all-equal-elements/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of size n containing only 1 and -1, and an integer k.
You can perform the following operation at most k times:
Note that you can choose the same index i more than once in different operations.
Return true if it is possible to make all elements of the array equal after at most k operations, and false otherwise.

**Examples**

**Example 1:**

```
Input: nums = [1,-1,1,-1,1], k = 3
Output: true
Explanation:
We can make all elements in the array equal in 2 operations as follows:
```

**Example 2:**

```
Input: nums = [-1,-1,-1,1,1,1], k = 5
Output: false
Explanation:
It is not possible to make all array elements equal in at most 5 operations.
```

**Constraints**

- 1 <= n == nums.length <= 105
- nums[i] is either -1 or 1.
- 1 <= k <= n

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`，其中仅包含 `1` 和 `-1`，以及一个整数 `k`。  
你可以至多执行 `k` 次以下操作：

- 选择一个下标 `i`（`0 <= i < n`），将 `nums[i]` 取反（即从 `1` 变为 `-1`，或从 `-1` 变为 `1`）。同一个下标 `i` 可以在不同的操作中被多次选择。

如果在至多 `k` 次操作后能够使数组中的所有元素相等，则返回 `true`；否则返回 `false`。

### 示例

**示例 1**  
```
Input: nums = [1,-1,1,-1,1], k = 3
Output: true
Explanation:
我们可以在 2 次操作中使所有元素相等，过程如下：
1. 选择下标 1，将 -1 取反为 1 → [1,1,1,-1,1]
2. 选择下标 3，将 -1 取反为 1 → [1,1,1,1,1]
```

**示例 2**  
```
Input: nums = [-1,-1,-1,1,1,1], k = 5
Output: false
Explanation:
在至多 5 次操作内无法使所有数组元素相等。
```

### 约束条件

- `1 <= n == nums.length <= 10^5`
- `nums[i]` 只能是 `-1` 或 `1`
- `1 <= k <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

数组里只有 `1` 和 `-1` 两种数。  
如果一次操作可以把 **任意** 位置的数取反（`1 → -1`，`-1 → 1`），那么最直接的办法就是：

1. 先算出把所有元素都变成 `1` 需要翻多少个 `-1`（记为 `cntNeg`）。  
2. 再算出把所有元素都变成 `-1` 需要翻多少个 `1`（记为 `cntPos`）。  
3. 只要 `cntNeg ≤ k` **或** `cntPos ≤ k`，就能在至多 `k` 次操作内把数组统一。

> **数据结构类比**：  
> 把 `cntNeg` 看成“字典里查不到的单词数”。如果字典里有 1000 页，而我们只能翻 5 页，就不可能把所有单词都查到。同理，若要把所有 `-1` 变成 `1`，我们必须“翻”掉所有 `-1`，这一步的“页数”就是 `cntNeg`。

这个想法一定是对的，因为每次操作只能改变 **一个** 元素的符号，想把所有 `-1` 变成 `1`，就必须对每个 `-1` 都动一次手。

**时间/空间复杂度**  
- 我们只需要遍历一遍数组，统计两种符号的出现次数，时间是 `O(n)`。  
- 只用了几个计数器，空间是 `O(1)`（常数级别）。

> **大白话解释**：  
> `O(n)` 就是“随数组长度线性增长”，比如数组有 10 万个数，就要看 10 万次。  
> `O(1)` 就是“无论数组多大，都只占用固定的几块内存”，类似装零钱的罐子容量不变。

#### 代码（Python）

```python
def can_be_equal_bruteforce(nums, k):
    """
    暴力思路：分别统计把所有元素变成 1 或 -1 所需的翻转次数，
    看哪一种在 k 次操作以内。
    """
    cnt_pos = 0          # 记录数组中 1 的个数
    cnt_neg = 0          # 记录数组中 -1 的个数
    for v in nums:
        if v == 1:
            cnt_pos += 1
        else:            # v == -1
            cnt_neg += 1

    # 把所有元素变成 1，需要翻转所有 -1，次数等于 cnt_neg
    need_to_all_one = cnt_neg
    # 把所有元素变成 -1，需要翻转所有 1，次数等于 cnt_pos
    need_to_all_minus_one = cnt_pos

    return need_to_all_one <= k or need_to_all_minus_one <= k
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，`n` 越大，耗时线性增长。  
- **空间复杂度**：`O(1)` —— 只用了几个整数计数器，和数组大小无关。

---

### 2. 最优解

#### 思路  

上面的暴力解已经是 **最优** 的时间复杂度（`O(n)`），但还有一种写法更简洁，也更符合 “把问题抽象成只看符号的数量” 的思想：

1. 统计数组中 `1` 的个数 `cnt_pos`（其余必然是 `-1`），于是 `cnt_neg = n - cnt_pos`。  
2. 把所有元素变成 `1` 需要的操作次数正好是 `cnt_neg`，把所有元素变成 `-1` 需要的次数是 `cnt_pos`。  
3. 只要 `min(cnt_pos, cnt_neg) ≤ k`，答案就为 `True`，否则为 `False`。

这一步把“两个判断”合并成了一个 `min`，代码更简短，逻辑更直观。

> **核心技巧**：  
> 只要把数组看成 **两类** 的计数问题，就不需要遍历两遍，也不需要分别判断两种目标。  
> 这类似于在生活中统计“男女人数”，想让全是男性，只要把所有女性搬走即可，搬走的次数就是女性的数量。

#### 代码（Python）

```python
def can_be_equal(nums, k):
    """
    最优写法：只统计 1 的个数，其余即为 -1 的个数。
    只要把较少的一类全部翻转（次数等于较少的那类数量）不超过 k 次，就能成功。
    """
    n = len(nums)
    cnt_pos = sum(1 for v in nums if v == 1)   # 统计 1 的个数
    cnt_neg = n - cnt_pos                      # -1 的个数 = 总数 - 1 的个数

    # 需要的最少操作次数 = 较少的那一类的数量
    min_ops = min(cnt_pos, cnt_neg)

    return min_ops <= k
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 仍然只遍历一次数组，无法再更快，因为我们必须看每个元素到底是 `1` 还是 `-1`。  
- **空间复杂度**：`O(1)` —— 只用了常数个整数变量。

> 与暴力解的对比：两者的时间、空间复杂度完全相同，最优解在实现上更简洁，且只做了一次 `min` 比较，代码可读性更高。

---

## 心得

- **核心技巧**：把 “全部相同” 的目标抽象成 “把较少的那一类全部翻转”。只需要统计两种符号的出现次数，最少操作数就是较少的那类的数量。  
- **适用的题型**：  
  1. 只含两种取值的数组或字符串，要求统一成一种（如 `0/1`、`A/B`、`True/False`）。  
  2. “最少翻转使字符串回文” 中，只需统计不匹配的字符对数。  
  3. “最少删除使数组只剩同一种数” 类似的计数问题。  
- **一句话总结**：**把问题转化为计数，最少操作等于较少类别的数量**。

## 反思

- **第一反应**：先想每次只能翻转一个元素，于是直接统计两类的个数。  
- **最容易踩的坑**：忘记题目允许 **多次** 选择同一位置——但在本题里每次只翻转单个元素，这一点并不影响计数思路。若误把操作理解成“翻转任意子段”，就会得到错误的判断。  
- **下次思路**：看到 “只有两种取值，要求全部相同，且每次只能改动一个元素”，第一步立刻想到 **统计两类的数量**，然后比较最小的那一个与 `k` 的关系。这样可以快速得到 `O(n)` 的最优解。