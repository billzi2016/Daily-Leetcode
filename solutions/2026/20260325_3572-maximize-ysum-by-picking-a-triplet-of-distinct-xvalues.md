# #3572. **通过挑选不同 X 值的三元组最大化 Y 和** / Maximize Y‑Sum by Picking a Triplet of Distinct X‑Values

> 难度：中等 · 标签：Array、Hash Table、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/maximize-ysum-by-picking-a-triplet-of-distinct-xvalues/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays x and y, each of length n. You must choose three distinct indices i, j, and k such that:
Your goal is to maximize the value of y[i] + y[j] + y[k] under these conditions. Return the maximum possible sum that can be obtained by choosing such a triplet of indices.
If no such triplet exists, return -1.

**Examples**

**Example 1:**

```
Input: x = [1,2,1,3,2], y = [5,3,4,6,2]
Output: 14
Explanation:
```

**Example 2:**

```
Input: x = [1,2,1,2], y = [4,5,6,7]
Output: -1
Explanation:
```

**Constraints**

- n == x.length == y.length
- 3 <= n <= 105
- 1 <= x[i], y[i] <= 106

---

## 题目（中文翻译）

给定两个整数数组 `x` 和 `y`，长度均为 `n`。你需要选择三个互不相同的下标 `i`, `j`, `k`，并满足：

- `x[i]`, `x[j]`, `x[k]` 三个值互不相同（distinct）。

在满足上述条件的前提下，目标是最大化 `y[i] + y[j] + y[k]` 的值。返回能够得到的最大和；如果不存在满足条件的三元组，则返回 `-1`。

---

### 示例

#### 示例 1
**输入**  
```text
x = [1,2,1,3,2], y = [5,3,4,6,2]
```
**输出**  
```text
14
```
**解释**  
选取下标 `i = 0`（`x = 1, y = 5`），`j = 3`（`x = 3, y = 6`），`k = 2`（`x = 1` 已出现，不能选），  
正确的选择是 `i = 0`（`x = 1, y = 5`），`j = 1`（`x = 2, y = 3`），`k = 3`（`x = 3, y = 6`），三者的 `x` 值均不同，`y` 和为 `5 + 3 + 6 = 14`，为最大可能值。

#### 示例 2
**输入**  
```text
x = [1,2,1,2], y = [4,5,6,7]
```
**输出**  
```text
-1
```
**解释**  
无论如何选取三个下标，总会出现至少两个相同的 `x` 值，无法满足 “`x` 值互不相同” 的要求，故返回 `-1`。

---

### 约束条件
- `n == x.length == y.length`
- `3 <= n <= 10^5`
- `1 <= x[i], y[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的三元组全部枚举一遍，挑出满足 **x 值互不相同** 的组合，然后比较它们对应的 `y[i] + y[j] + y[k]`，取最大值。

- **数据结构**：我们只需要用两个普通的列表 `x`、`y`，以及三个循环变量 `i、j、k`。  
- **生活化类比**：把所有元素想成一堆卡片，每张卡片上写着两个数字（x，y）。暴力做法就是把这堆卡片全部挑出三张，检查这三张卡片的左边数字（x）是否全不相同，若相同就把它们丢掉，不相同就把右边数字（y）相加记下来。  
- **为什么正确**：因为我们遍历了 **所有** 合法的三元组，最大值一定在其中，所以一定能得到正确答案。  

#### 代码（Python）

```python
def max_y_sum_brute(x: list[int], y: list[int]) -> int:
    n = len(x)
    ans = -1                                 # 初始答案设为 -1，表示不存在合法三元组
    # 三层循环枚举所有 i < j < k 的组合
    for i in range(n):
        for j in range(i + 1, n):
            # 先检查前两个 x 是否相同，若相同直接跳过，省点时间
            if x[i] == x[j]:
                continue
            for k in range(j + 1, n):
                # 检查第三个 x 是否和前两个冲突
                if x[i] == x[k] or x[j] == x[k]:
                    continue
                # 合法组合，计算 y 的和并更新答案
                cur = y[i] + y[j] + y[k]
                if cur > ans:
                    ans = cur
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - “立方”意味着如果 `n` 是 100，循环次数大约是 1,000,000（100³），如果 `n` 是 1,000，循环次数就会涨到 **10⁹**，计算机根本跑不完。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`ans、i、j、k、cur`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **对每一个元素都做了重复的比较**。观察题目可以发现：

1. **相同的 x 只需要保留一个最大的 y**。  
   - 想象我们有一本电话簿，键是 `x`（电话号码），值是对应的 `y`（联系人名字）。如果同一个电话号码出现多次，只需要把字典里保存的名字换成最长的那个，因为在后面挑选三个人时，只有最长的名字才可能让总长度最大。  
2. 处理完第 1 步后，**每个不同的 x 只出现一次**，于是我们只需要从这些 “唯一的 x 对应的最大 y” 中挑选出 **最大的三个 y**。  
   - 这一步相当于在一堆数字里找出最大的三个，常见做法有：  
     - **排序**：把所有 y 按从大到小排好，直接取前 3。  
     - **一次遍历**：维护三个变量 `first、second、third`，在遍历时不断更新它们。  
   - 两种方法都能在 `O(m log m)`（排序）或 `O(m)`（一次遍历）时间内完成，这里 `m` 是不同 `x` 的数量，`m ≤ n`。

综合起来的最优流程：

1. 用哈希表（Python 的 `dict`）把每个 `x` 映射到它最大的 `y`。  
2. 把哈希表的所有值（即每个唯一 `x` 对应的最大 `y`）收集到列表 `vals`。  
3. 如果 `len(vals) < 3`，说明不同的 `x` 不足三个，返回 `-1`。  
4. 否则，找出 `vals` 中最大的三个数并相加，返回结果。

下面用 **一次遍历找前三大** 的实现，代码最简洁且不需要额外的排序空间。

#### 代码（Python）

```python
def max_y_sum_opt(x: list[int], y: list[int]) -> int:
    """
    返回在 x 值互不相同的前提下，y 的最大三元组和。
    若不同的 x 少于 3 个，则返回 -1。
    """
    # 1️⃣ 用字典把每个 x 映射到它最大的 y
    best_for_x: dict[int, int] = {}
    for xi, yi in zip(x, y):
        # 如果 xi 之前没出现，直接插入；否则取更大的 y
        if xi not in best_for_x or yi > best_for_x[xi]:
            best_for_x[xi] = yi

    # 2️⃣ 取出所有唯一 x 对应的最大 y
    vals = list(best_for_x.values())

    # 3️⃣ 检查是否至少有 3 个不同的 x
    if len(vals) < 3:
        return -1

    # 4️⃣ 一遍扫描找出最大的三个 y
    first = second = third = -1   # 初始化为负数，题目保证 y ≥ 1
    for v in vals:
        if v > first:
            third = second
            second = first
            first = v
        elif v > second:
            third = second
            second = v
        elif v > third:
            third = v

    return first + second + third
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 第一次遍历把每个元素放进哈希表是 `O(n)`；第二次遍历字典的值找前三大也是 `O(m)`，而 `m ≤ n`，所以整体线性。相比暴力的 `O(n³)`，速度提升了 **指数级**。  
- **空间复杂度**：`O(m)`（哈希表的大小）  
  - 需要存储每个不同 `x` 对应的最大 `y`，最坏情况下 `m = n`，即需要额外的 `n` 个整数空间。对比暴力解的 `O(1)`，多用了点空间，但在 10⁵ 规模的数据下完全可以接受。

---

## 心得

- **核心技巧**：**哈希表去重 + 贪心挑选最大值**。先把相同 `x` 合并，只保留最大的 `y`，再在剩下的候选中挑出最大的三个。  
- **适用的题型**  
  1. “在满足某种唯一性约束下，选出 k 个元素使和最大”——如 “选出两个人使得年龄不同且身高之和最大”。  
  2. “每类只保留最优代表再做组合”——如 “每种颜色只保留价值最高的宝石”。  
  3. “从若干组中各挑一个，求最优组合”——如 “每个部门挑一个员工组成团队”。  
- **一句话总结**：**先把重复的“同类”压缩成最优代表，再在压缩后的集合中贪心取最大**。

---

## 反思

- **第一反应**：看到“不同的 x”就想到要 **去重**，于是立刻想到用 `set` 或 `dict` 来记录每个 `x` 的最大 `y`。  
- **最容易踩的坑**  
  - 忘记检查 **不同的 x 是否足够 3 个**，直接取前三大可能会出现 `IndexError`。  
  - 在更新字典时写成 `best_for_x[xi] = max(best_for_x.get(xi, 0), yi)`，如果 `yi` 可能为 0（这里不可能）或负数时要注意初始值的选取。  
  - 对于极端输入（如所有 `x` 都相同），要确保程序返回 `-1` 而不是错误的和。  
- **下次遇到同类题**：**第一步先把“相同属性的元素合并为最佳代表”，随后在代表集合上做贪心/排序/堆等最优选择**。这样可以把原本 `O(n³)` 或 `O(n²)` 的暴力搜索直接压缩到 `O(n)` 或 `O(n log n)`。