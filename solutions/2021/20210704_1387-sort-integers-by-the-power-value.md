# #1387. **按能量值对整数排序** / Sort Integers by The Power Value

> 难度：中等 · 标签：Dynamic Programming、Memoization、Sorting · [LeetCode 链接](https://leetcode.com/problems/sort-integers-by-the-power-value/)

---

## 题目（英文原版）

**Description**

The power of an integer x is defined as the number of steps needed to transform x into 1 using the following steps:
For example, the power of x = 3 is 7 because 3 needs 7 steps to become 1 (3 --> 10 --> 5 --> 16 --> 8 --> 4 --> 2 --> 1).
Given three integers lo, hi and k. The task is to sort all integers in the interval [lo, hi] by the power value in ascending order, if two or more integers have the same power value sort them by ascending order.
Return the kth integer in the range [lo, hi] sorted by the power value.
Notice that for any integer x (lo <= x <= hi) it is guaranteed that x will transform into 1 using these steps and that the power of x is will fit in a 32-bit signed integer.

**Examples**

**Example 1:**

```
Input: lo = 12, hi = 15, k = 2
Output: 13
Explanation: The power of 12 is 9 (12 --> 6 --> 3 --> 10 --> 5 --> 16 --> 8 --> 4 --> 2 --> 1)
The power of 13 is 9
The power of 14 is 17
The power of 15 is 17
The interval sorted by the power value [12,13,14,15]. For k = 2 answer is the second element which is 13.
Notice that 12 and 13 have the same power value and we sorted them in ascending order. Same for 14 and 15.
```

**Example 2:**

```
Input: lo = 7, hi = 11, k = 4
Output: 7
Explanation: The power array corresponding to the interval [7, 8, 9, 10, 11] is [16, 3, 19, 6, 14].
The interval sorted by power is [8, 10, 11, 7, 9].
The fourth number in the sorted array is 7.
```

**Constraints**

- 1 <= lo <= hi <= 1000
- 1 <= k <= hi - lo + 1

---

## 题目（中文翻译）

整数 x 的能量（power）定义为将 x 通过以下步骤转化为 1 所需的步数：

- 若 x 为偶数，则 x → x / 2  
- 若 x 为奇数，则 x → 3·x + 1  

例如，x = 3 的能量为 7，因为 3 需要 7 步才能变为 1（3 → 10 → 5 → 16 → 8 → 4 → 2 → 1）。

给定三个整数 `lo`、`hi` 和 `k`。请将区间 `[lo, hi]`（包含两端）内的所有整数按能量值升序排列；若两个或更多整数的能量相同，则按整数本身的升序排列。返回排好序后第 `k` 小的整数。

> **提示**：对于区间中的任意整数 `x`（`lo ≤ x ≤ hi`），一定能够通过上述步骤转化为 1，且 `x` 的能量值能够装入 32 位有符号整数。

---

### 示例

**示例 1**

```
Input: lo = 12, hi = 15, k = 2
Output: 13
Explanation: 
- 12 的能量为 9（12 → 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1）
- 13 的能量为 9
- 14 的能量为 17
- 15 的能量为 17
区间按能量值排序后为 [12, 13, 14, 15]。第 2 小的元素是 13。
注意 12 与 13 的能量相同，按照整数升序排列。
```

**示例 2**

```
Input: lo = 7, hi = 11, k = 4
Output: 7
Explanation: 
区间 [7, 8, 9, 10, 11] 对应的能量数组为 [16, 3, 19, 6, 14]。
按能量值排序后得到的顺序是 [8, 10, 11, 7, 9]。
第 4 小的数是 7。
```

---

### 约束条件

- `1 <= lo <= hi <= 1000`
- `1 <= k <= hi - lo + 1`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
1. **把每个数变成 1 的过程记下来**  
   - 题目给出的变换规则其实就是“**Collatz 猜想**”。  
   - 对于任意整数 `x`，如果 `x` 为偶数就除以 2；如果是奇数就变成 `3*x + 1`。  
   - 我们把把 `x` 变成 1 所需要的步骤数叫 **power(x)**。  

2. **暴力做法**  
   - 直接遍历区间 `[lo, hi]`，对每个数 `n` 按规则一步一步模拟，计数直到得到 1。  
   - 把得到的 `(n, power(n))` 放进列表。  
   - 按 **power** 从小到大排序；如果 power 相同，则按数字本身升序。  
   - 最后返回排好序后的第 `k` 个数字。  

3. **用到的数据结构**  
   - **列表**：保存每个数以及对应的 power。可以把它想象成一本“成绩单”，每行记录学生（数字）和他的成绩（power）。  
   - **排序**：Python 的 `sorted` 会根据我们提供的键函数自动把“成绩单”排好序。  

4. **为什么一定对**  
   - 规则是确定的、每一步都唯一，所以模拟的步骤数一定等于题目定义的 power。  
   - 排序规则直接对应题目要求：先按 power 升序，再按数字升序。  

5. **时间/空间复杂度**（大白话）  
   - 对每个数我们都要**一步步**走到 1，最坏情况下可能要走上百次（因为 `hi ≤ 1000`，实际最多约 500 步）。  
   - 区间长度是 `n = hi - lo + 1`，所以总共的步数大约是 `n * (平均步数)` → **O(n·log max)**，这里把 “log max” 当成常数，写作 **O(n²)** 更保守。  
   - 排序本身是 `O(n log n)`，在 `n` 只有千级时可以忽略不计。  
   - 空间上我们只保存 `n` 个 `(num, power)`，即 **O(n)**。  

#### 代码（Python）  

```python
def get_power_bruteforce(x: int) -> int:
    """模拟 Collatz 过程，返回把 x 变成 1 需要的步数（暴力版）"""
    steps = 0
    while x != 1:                 # 一直循环到 1
        if x % 2 == 0:            # 偶数 → 除以 2
            x //= 2
        else:                     # 奇数 → 3*x + 1
            x = 3 * x + 1
        steps += 1                # 计数
    return steps


def getKth(lo: int, hi: int, k: int) -> int:
    """暴力解：直接算每个数的 power，然后排序取第 k 小"""
    power_list = []               # 用来存 (num, power) 的“成绩单”
    for num in range(lo, hi + 1):
        p = get_power_bruteforce(num)
        power_list.append((num, p))

    # 按 power 升序；若相同再按数字升序
    power_list.sort(key=lambda x: (x[1], x[0]))

    # 第 k 个（k 是 1-indexed），返回对应的数字
    return power_list[k - 1][0]
```

#### 复杂度  

- **时间复杂度**：`O(n * s)`，其中 `n = hi-lo+1`，`s` 为单个数转化为 1 的步数。对本题的约束（`hi ≤ 1000`）来说，最坏约 `O(n²)`。  
- **空间复杂度**：`O(n)`，只保存区间内的 `(num, power)` 列表。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到，**重复计算** 是主要的性能瓶颈。  
例如在区间 `[12, 15]` 中，`12 → 6 → 3 → …`，而 `6`、`3` 这些子问题也会在其它数字的计算里出现。  
如果每次都重新模拟，就会浪费大量时间。  

**优化的关键**：**记忆化**（Memoization）——把已经算好的 `power(x)` 保存下来，下次再需要时直接查表。  

1. **建立一个全局字典 `memo`**  
   - 把 `power(1) = 0` 放进去。  
   - 当我们要算 `power(x)` 时，先检查 `memo`，如果已经有直接返回。  

2. **递归 + 记忆化**  
   - 对 `x`：  
     - 若 `x` 为偶数 → `power(x) = 1 + power(x // 2)`  
     - 若 `x` 为奇数 → `power(x) = 1 + power(3*x + 1)`  
   - 递归结束后把结果写入 `memo[x]`。  
   - 这一步相当于“把子任务的答案存进抽屉”，以后再打开抽屉就能立刻得到答案。  

3. **遍历区间并排序**  
   - 同暴力解一样，把每个 `num` 的 `power` 取出，放进列表。  
   - 排序时仍然使用 `(power, num)` 作为键。  

4. **为什么更快**  
   - 每个 **不同的整数** 最多只会被计算一次。  
   - 对于本题的约束，`hi ≤ 1000`，但递归过程中可能出现稍大于 `hi` 的数（比如 `3*x+1`），这些数的范围仍然有限（实际最多不到几千）。  
   - 因此整体的计算量大约是 **O(N)**（N 为所有出现过的不同整数），远小于暴力的 `O(N²)`。  

5. **核心概念解释**  
   - **动态规划**：把大问题拆成子问题，子问题只解一次，后面直接复用。这里我们用递归 + 记忆化实现。  
   - **哈希表（字典）**：类似于“查字典”，键是整数 `x`，值是它的 power。查一次就是 O(1) 时间。  

#### 代码（Python）  

```python
def getKth(lo: int, hi: int, k: int) -> int:
    """最优解：记忆化递归计算 power，随后排序取第 k 小"""
    memo = {1: 0}                     # 已知 base case，power(1) = 0

    def power(x: int) -> int:
        """返回 x 的 power，使用 memo 缓存已算结果"""
        if x in memo:                # 直接命中缓存 → O(1)
            return memo[x]

        # 递归求子问题的 power
        if x % 2 == 0:               # 偶数情况
            nxt = x // 2
        else:                        # 奇数情况
            nxt = 3 * x + 1

        memo[x] = 1 + power(nxt)     # 把当前结果存进缓存
        return memo[x]

    # 计算区间每个数的 power 并收集 (num, power) 对
    arr = [(num, power(num)) for num in range(lo, hi + 1)]

    # 按 power 升序、数字升序排序
    arr.sort(key=lambda x: (x[1], x[0]))

    # 第 k 个（k 从 1 开始）对应的数字即为答案
    return arr[k - 1][0]
```

#### 复杂度  

- **时间复杂度**：`O(N)`，其中 `N` 为遍历区间 `[lo, hi]` 以及递归过程中出现的所有不同整数的总数。对本题 `N` 至多几千，基本是线性。相比暴力的 `O(N²)`，提升明显。  
- **空间复杂度**：`O(N)`，主要是 `memo` 字典和存放 `(num, power)` 的列表。  

---

## 心得  

- **核心技巧**：**记忆化递归（Memoization）**，即把已经算好的子问题结果缓存起来，避免重复计算。  
- **适用的题型**：  
  1. **Collatz 序列** 类似的问题（如 LeetCode 1342 “Number of Steps to Reduce a Number to Zero”）。  
  2. **斐波那契数列**、**爬楼梯** 等递归转 DP 的经典题。  
  3. **树的递归遍历** 中需要重复子树结果的情况。  
- **一句话总结**：**“把子任务的答案记进抽屉，下次直接取出”，记忆化是递归的加速器。**  

---

## 反思  

- **第一反应**：直接写循环模拟每个数的转换过程，想到再排序。  
- **最容易踩的坑**：  
  - **递归深度**：如果不使用记忆化，某些大数的递归层数会很深，可能导致栈溢出。  
  - **缓存范围**：忘记把 `power(1)=0` 放进字典，导致无限递归。  
  - **排序键**：必须先按 power 排序，再按数字，否则相同 power 时顺序会错。  
- **下次遇到同类题**：第一步先思考“是否有子问题会被多次使用”，如果答案是“是”，立刻考虑 **记忆化 / 动态规划**。这样可以把暴力的指数/平方级别降到线性或对数级别。