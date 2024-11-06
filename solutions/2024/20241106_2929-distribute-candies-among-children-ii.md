# #2929. 分配糖果给孩子 II / Distribute Candies Among Children II

> 难度：中等 · 标签：Math、Combinatorics、Enumeration · [LeetCode 链接](https://leetcode.com/problems/distribute-candies-among-children-ii/)

---

## 题目（英文原版）

**Description**

You are given two positive integers n and limit.
Return the total number of ways to distribute n candies among 3 children such that no child gets more than limit candies.

**Examples**

**Example 1:**

```
Input: n = 5, limit = 2
Output: 3
Explanation: There are 3 ways to distribute 5 candies such that no child gets more than 2 candies: (1, 2, 2), (2, 1, 2) and (2, 2, 1).
```

**Example 2:**

```
Input: n = 3, limit = 3
Output: 10
Explanation: There are 10 ways to distribute 3 candies such that no child gets more than 3 candies: (0, 0, 3), (0, 1, 2), (0, 2, 1), (0, 3, 0), (1, 0, 2), (1, 1, 1), (1, 2, 0), (2, 0, 1), (2, 1, 0) and (3, 0, 0).
```

**Constraints**

- 1 <= n <= 106
- 1 <= limit <= 106

---

## 题目（中文翻译）

给定两个正整数 `n` 和 `limit`。求将 `n` 颗糖果分配给 3 个孩子的所有可能分配方式的总数，要求任意孩子分到的糖果数量不超过 `limit`。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**

**示例 1**  
Input: `n = 5, limit = 2`  
Output: `3`  
Explanation: 有 3 种方式可以在不让任何孩子得到超过 2 颗糖果的前提下分配 5 颗糖果，分别是 `(1, 2, 2)`、`(2, 1, 2)` 和 `(2, 2, 1)`。

**示例 2**  
Input: `n = 3, limit = 3`  
Output: `10`  
Explanation: 有 10 种方式可以在不让任何孩子得到超过 3 颗糖果的前提下分配 3 颗糖果，分别是 `(0, 0, 3)`、`(0, 1, 2)`、`(0, 2, 1)`、`(0, 3, 0)`、`(1, 0, 2)`、`(1, 1, 1)`、`(1, 2, 0)`、`(2, 0, 1)`、`(2, 1, 0)` 和 `(3, 0, 0)`。

**约束条件**  
- `1 <= n <= 10^6`  
- `1 <= limit <= 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把每个孩子可能得到的糖果数全部列举出来，检查哪一种满足 **每个孩子 ≤ limit 且三个人的糖果总数恰好等于 n**。  
- 我们可以用三个变量 `a、b、c` 表示 3 个孩子得到的糖果数。  
- `a、b、c` 的取值范围都是 `0 … limit`（就像查字典时，词典的每一页都可能是答案）。  
- 对每一种 `(a, b, c)`，只要 `a + b + c == n` 就算作一种合法分配。  

这种做法一定能得到正确答案，因为我们把**所有可能**都枚举了一遍，符合题目要求的自然不会漏掉。  

#### 代码（Python）  

```python
def count_candies_bruteforce(n: int, limit: int) -> int:
    """
    暴力枚举三个人的糖果数
    时间复杂度在 n、limit 很大时会爆炸，只适合调试或 n、limit 很小的情况
    """
    ans = 0
    # 第一个孩子的糖果数 a
    for a in range(0, min(limit, n) + 1):
        # 第二个孩子的糖果数 b
        for b in range(0, min(limit, n - a) + 1):
            c = n - a - b          # 第三个孩子只能取剩下的糖果数
            # 检查 c 是否在合法范围内
            if 0 <= c <= limit:
                ans += 1           # 找到一种合法分配
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(limit²)`（最坏情况下外层循环 `≈ limit`，内层循环也 `≈ limit`），也可以写成 `O(min(n,limit)²)`。  
  用大白话说，就是如果 limit 是 1000，程序大约会跑 1,000,000 次循环；如果 limit 是 10⁶，循环次数会达到 10¹²，根本跑不完。  
- **空间复杂度**：`O(1)`，只用了常数级别的额外变量。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **两层循环**，每次都要遍历 `limit` 次。  
观察题目提示可以发现：只要确定 **第一个孩子** 的糖果数 `i`，**第二个孩子** 的取值范围其实可以直接算出来，**第三个孩子** 的糖果数随之唯一确定。  

**步骤拆解**  

1. **枚举第一个孩子的糖果数 `i`**  
   - `i` 的合法取值是 `0 … min(limit, n)`。  
2. 对于固定的 `i`，设第二个孩子得到 `j`，则  
   - 必须满足 `0 ≤ j ≤ limit`（第二个孩子不能超限）  
   - 以及 `i + j ≤ n`（已经分配的糖果不能超过总数）  
3. 第三个孩子得到的糖果数是 `k = n - i - j`，必须满足 `0 ≤ k ≤ limit`。  
   - 把 `k` 的不等式写成 `0 ≤ n - i - j ≤ limit`，得到  
     ```
     n - i - limit ≤ j ≤ n - i
     ```
4. 把所有约束综合起来，`j` 的合法区间是  
   ```
   left  = max(0, n - i - limit)
   right = min(limit, n - i)
   ```
   - 如果 `left > right`，说明在该 `i` 下根本没有合法的 `j`（对应的解数为 0）。  
   - 否则，`j` 可以取 `right - left + 1` 种不同的值，每一种对应唯一的 `k`，于是这 `i` 下的合法分配数就是 `right - left + 1`。  

5. 把上面的计数式对所有 `i` 求和，即得到答案。  

**为什么只需要 O(min(n,limit))**  

我们只循环一次 `i`（最多 `min(n,limit)+1` 次），每一次只做常数次的算术运算，根本不需要再遍历 `j`。因此整体时间是 **线性的**，即使 `n、limit` 达到 10⁶ 也能在毫秒级完成。  

#### 代码（Python）  

```python
def count_candies_optimal(n: int, limit: int) -> int:
    """
    只枚举第一个孩子的糖果数 i，利用区间计算直接得到每个 i 对应的合法 j 的个数
    时间复杂度 O(min(n, limit))，空间复杂度 O(1)
    """
    ans = 0
    # i 的取值范围：0 到 min(limit, n)
    max_i = min(limit, n)
    for i in range(max_i + 1):
        # 根据推导得到 j 的左、右边界
        left  = max(0, n - i - limit)          # j 必须至少这么大，才能让第3个孩子不超过 limit
        right = min(limit, n - i)              # j 不能超过 limit，也不能让总和超过 n
        if left <= right:                      # 区间非空，说明有合法的 j
            ans += right - left + 1            # 这 i 下的合法分配数
        # else: 区间为空，贡献 0，直接跳过
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(min(n, limit))`。  
  用大白话说，如果 `n=10⁶、limit=10⁶`，循环只会跑 1,000,001 次；如果 `limit` 很小（比如 10），循环也只会跑 11 次。相比暴力的 `limit²`，快了 **指数级**。  
- **空间复杂度**：`O(1)`，只用了几个整型变量，和输入规模无关。  

---

## 心得  

- **核心技巧**：把多维枚举转化为**单维枚举 + 区间计数**。先固定一个变量，再用不等式推导出其余变量的合法取值范围。  
- **适用场景**  
  1. “把 n 件物品分配给 k 个人，每个人有上限” 类的计数题（如 LeetCode 1785、面试题 “分配糖果”）。  
  2. “满足线性不等式的整数解个数”——常见于组合数学中的“有界组合”。  
  3. “在二维平面上统计满足矩形约束的点的个数”——可以用区间交叉的思想快速求解。  
- **一句话总结**：**先固定一个维度，用不等式把剩余维度压缩成区间，区间长度就是答案**。  

---

## 反思  

- **第一反应**：看到“分配糖果”立刻想到三层循环枚举，写出暴力解来验证样例。  
- **最容易踩的坑**  
  - 忽略 **0** 也是合法的糖果数，导致计数缺少边界情况。  
  - 在计算 `left`、`right` 时写反了符号，导致区间为空或超出上限。  
  - 当 `n` 大于 `3 * limit` 时根本没有解，需要返回 0；如果不提前判断，循环仍然会跑完但每次贡献 0，虽然正确但会浪费时间。  
- **下次遇到同类题**：**第一步先把问题写成不等式约束，然后尝试固定一个变量，把其余变量的合法取值压缩成区间**，看能否直接用区间长度计数。这样往往能把指数级的枚举降到线性甚至常数级。