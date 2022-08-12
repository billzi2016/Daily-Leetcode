# #1894. 寻找将要更换粉笔的学生 / Find the Student that Will Replace the Chalk

> 难度：中等 · 标签：Array、Binary Search、Simulation、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-the-student-that-will-replace-the-chalk/)

---

## 题目（英文原版）

**Description**

There are n students in a class numbered from 0 to n - 1. The teacher will give each student a problem starting with the student number 0, then the student number 1, and so on until the teacher reaches the student number n - 1. After that, the teacher will restart the process, starting with the student number 0 again.
You are given a 0-indexed integer array chalk and an integer k. There are initially k pieces of chalk. When the student number i is given a problem to solve, they will use chalk[i] pieces of chalk to solve that problem. However, if the current number of chalk pieces is strictly less than chalk[i], then the student number i will be asked to replace the chalk.
Return the index of the student that will replace the chalk pieces.

**Examples**

**Example 1:**

```
Input: chalk = [5,1,5], k = 22
Output: 0
Explanation: The students go in turns as follows:
- Student number 0 uses 5 chalk, so k = 17.
- Student number 1 uses 1 chalk, so k = 16.
- Student number 2 uses 5 chalk, so k = 11.
- Student number 0 uses 5 chalk, so k = 6.
- Student number 1 uses 1 chalk, so k = 5.
- Student number 2 uses 5 chalk, so k = 0.
Student number 0 does not have enough chalk, so they will have to replace it.
```

**Example 2:**

```
Input: chalk = [3,4,1,2], k = 25
Output: 1
Explanation: The students go in turns as follows:
- Student number 0 uses 3 chalk so k = 22.
- Student number 1 uses 4 chalk so k = 18.
- Student number 2 uses 1 chalk so k = 17.
- Student number 3 uses 2 chalk so k = 15.
- Student number 0 uses 3 chalk so k = 12.
- Student number 1 uses 4 chalk so k = 8.
- Student number 2 uses 1 chalk so k = 7.
- Student number 3 uses 2 chalk so k = 5.
- Student number 0 uses 3 chalk so k = 2.
Student number 1 does not have enough chalk, so they will have to replace it.
```

**Constraints**

- chalk.length == n
- 1 <= n <= 105
- 1 <= chalk[i] <= 105
- 1 <= k <= 109

---

## 题目（中文翻译）

**题目描述**  
班级里有 `n` 名学生，编号从 `0` 到 `n - 1`。老师会依次给学生布置题目，先从学生编号 `0` 开始，然后是编号 `1`，依此类推，直到编号 `n - 1`。完成一轮后，老师会重新从编号 `0` 的学生开始循环。

给定一个 **0 索引** 的整数数组 `chalk` 和一个整数 `k`，初始时有 `k` 支粉笔。当编号为 `i` 的学生被布置题目时，需要使用 `chalk[i]` 支粉笔。如果此时剩余的粉笔数量 **严格小于** `chalk[i]`，则编号为 `i` 的学生需要去更换粉笔。

请返回需要更换粉笔的学生的编号（下标）。

---

**示例 1**  
```
Input: chalk = [5,1,5], k = 22
Output: 0
Explanation: 学生轮流使用粉笔的过程如下：
- 学生 0 使用 5 支粉笔，k = 17
- 学生 1 使用 1 支粉笔，k = 16
- 学生 2 使用 5 支粉笔，k = 11
- 学生 0 使用 5 支粉笔，k = 6
- 学生 1 使用 1 支粉笔，k = 5
- 学生 2 使用 5 支粉笔，k = 0
此时学生 0 的剩余粉笔不足以完成下一次使用，需要更换粉笔，返回 0。
```

**示例 2**  
```
Input: chalk = [3,4,1,2], k = 25
Output: 1
Explanation: 学生轮流使用粉笔的过程如下：
- 学生 0 使用 3 支粉笔，k = 22
- 学生 1 使用 4 支粉笔，k = 18
- 学生 2 使用 1 支粉笔，k = 17
- 学生 3 使用 2 支粉笔，k = 15
- 学生 0 使用 3 支粉笔，k = 12
- 学生 1 使用 4 支粉笔，k = 8
- 学生 2 使用 1 支粉笔，k = 7
- 学生 3 使用 2 支粉笔，k = 5
- 学生 0 使用 3 支粉笔，k = 2
此时学生 1 的剩余粉笔不足以完成下一次使用，需要更换粉笔，返回 1。
```

**约束条件**  
- `chalk.length == n`
- `1 <= n <= 10^5`
- `1 <= chalk[i] <= 10^5`
- `1 <= k <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**模拟**老师发题的过程：

1. 从学生 `0` 开始，依次遍历数组 `chalk`。  
2. 每到一个学生 `i`，判断当前剩余的粉笔 `k` 是否小于 `chalk[i]`。  
   - 如果小于，说明这个学生需要去换粉笔，直接返回 `i`。  
   - 否则，用掉 `chalk[i]` 块粉笔，`k -= chalk[i]`，继续下一个学生。  
3. 当遍历到数组末尾后，若仍有粉笔剩余，则从头再开始（即把指针重新置为 `0`），继续上述过程，直到找到答案。

> **类比**：把 `chalk` 想成一本字典，`i` 是查的词条，`chalk[i]` 是对应的页码（需要的粉笔数）。老师每查一次，就把对应的页码数从总页数 `k` 中减掉，直到剩余页数不够下一次查的页码，这时就“找不到”，返回当前的词条下标。

**为什么正确**  
因为题目本身就是要求按顺序不断扣除粉笔，直到某一次扣除前的粉笔数量不足以满足当前学生的需求。只要严格按照顺序模拟，就必然得到第一次“粉笔不够”的学生下标。

**复杂度分析**  

- **时间复杂度**：最坏情况下需要循环很多次。设数组长度为 `n`，每轮循环会扣除 `sum(chalk)` 块粉笔。如果 `k` 非常大，可能需要 `k / sum(chalk)` 轮才能进入最后一轮。于是时间复杂度是 **O(k / sum + n)**，在最坏情况下约等于 **O(k)**，这在 `k ≤ 10⁹`、`n ≤ 10⁵` 时会超时。  
  用大白话说，`O(k)` 就像说“我们可能要走 `k` 步”，如果 `k` 是十亿步，那显然太慢了。  

- **空间复杂度**：只用了常数级别的额外变量（`i`、`k`），所以是 **O(1)**。

#### 代码（Python）

```python
def chalkReplacer_bruteforce(chalk, k):
    n = len(chalk)
    i = 0                     # 当前学生的下标
    while True:              # 无限循环，直到找到答案
        if k < chalk[i]:      # 粉笔不够，返回当前学生
            return i
        k -= chalk[i]         # 用掉 chalk[i] 块粉笔
        i = (i + 1) % n       # 移动到下一个学生，循环到头后回到 0
```

> 关键行解释  
> - `if k < chalk[i]`：判断“粉笔是否不足”。  
> - `i = (i + 1) % n`：利用取模实现“环形遍历”，相当于回到第一个学生。

#### 复杂度

- 时间复杂度：**O(k / sum(chalk) + n)** ≈ **O(k)**，意味着如果 `k` 很大会非常慢。  
- 空间复杂度：**O(1)**，只用了几个整数变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们一次只扣除 `chalk[i]`，而其实可以一次性扣除 **整整一轮**（即所有学生一次）的粉笔量。  

1. **先算一轮需要的总粉笔** `total = sum(chalk)`。  
   - 如果 `k >= total`，说明可以完整地走完若干整轮。我们可以直接把 `k` 减去整轮的总量 `total` 的若干倍，使 `k` 变成**小于**一轮所需的粉笔数。  
   - 这一步可以用 `k %= total`（取余）一次完成，时间 O(1)。  

2. **此时 `k` 已经小于一整轮的总需求**，只需要在这最后一轮里逐个学生检查即可。  
   - 依次遍历 `chalk`，如果 `k < chalk[i]`，返回 `i`；否则 `k -= chalk[i]`，继续。  

这就是**前缀和 + 二分搜索**的思路的简化版（因为 `k` 已经被压缩到一轮以内，线性遍历足够快）。如果想进一步把最后一步也改成二分搜索，只需要先把 `chalk` 的前缀和数组 `pre` 建好，然后在 `pre` 中找第一个大于 `k` 的位置。这里提供两种实现：

- **实现 A**：`k %= total` 后线性遍历（代码更简洁，时间仍是 O(n)）。  
- **实现 B**：在 `pre` 上二分搜索，整体时间 **O(log n)**（更快，适合面试时展示算法思考）。

下面分别给出实现 A（更直观）和实现 B（展示二分搜索的技巧）。

---

#### 实现 A：取余 + 线性遍历

**为什么快**：只需要一次取余，把可能的上亿次循环压缩到 **一次**，随后最多遍历一次数组（最多 `10⁵` 次），完全在时间限制内。

#### 代码（Python）

```python
def chalkReplacer_opt(chalk, k):
    total = sum(chalk)           # 整轮需要的粉笔总数
    k %= total                   # 只保留最后一轮剩余的粉笔

    for i, need in enumerate(chalk):
        if k < need:             # 粉笔不够，当前学生 i 替换
            return i
        k -= need                # 用掉 need 块粉笔，继续下一个学生
```

> 关键行解释  
> - `k %= total`：相当于“把 k 减去尽可能多的完整轮次”，只留下不足一整轮的那部分。  
> - `for i, need in enumerate(chalk):`：一次遍历，每次检查是否已不足以满足当前学生。

#### 复杂度

- 时间复杂度：**O(n)**（一次求和 + 一次遍历），在最坏情况下是 `2·10⁵` 次操作，毫秒级完成。  
- 空间复杂度：**O(1)**，只用了几个额外整数。

---

#### 实现 B：取余 + 前缀和 + 二分搜索（可选进阶）

**前缀和**：把数组 `chalk` 转成累加数组 `pre`，`pre[i]` 表示从学生 `0` 到 `i`（含）共需要的粉笔数。  
**二分搜索**：在 `pre` 中找到第一个大于 `k` 的位置，即为答案。二分搜索的时间是 `O(log n)`，在极端情况下（`n=10⁵`）也只需要约 17 次比较。

#### 代码（Python）

```python
import bisect

def chalkReplacer_opt_binary(chalk, k):
    # 1. 前缀和
    pre = []
    cur = 0
    for c in chalk:
        cur += c
        pre.append(cur)          # pre[i] = sum(chalk[0..i])

    total = pre[-1]              # 整轮的总粉笔数
    k %= total                    # 只保留最后一轮

    # 2. 二分查找第一个 > k 的位置
    # bisect_right 返回第一个大于 k 的索引
    idx = bisect.bisect_right(pre, k)
    return idx                    # idx 正好是要换粉笔的学生下标
```

> 关键行解释  
> - `pre.append(cur)`：构建前缀和，相当于“把每个学生累计需要的粉笔记录下来”。  
> - `bisect.bisect_right(pre, k)`：在已排好序的前缀和里找第一个 **大于** `k` 的位置，返回的索引就是答案。

#### 复杂度

- 时间复杂度：**O(n)**（构建前缀和）+ **O(log n)**（二分搜索）≈ **O(n)**。  
- 空间复杂度：**O(n)**（存前缀和数组），相较实现 A 多用了 `n` 个整数的空间。

> 对比实现 A 与 B：  
> - 实现 A 更省空间，代码更短；  
> - 实现 B 展示了二分搜索的技巧，适合在需要进一步优化或想展示算法深度时使用。

---

## 心得

- **核心技巧**：先用**取余**把大数 `k` 缩小到「一轮以内」的范围，再用**线性遍历**或**二分搜索**找答案。  
- **适用的题型**  
  1. “循环消耗”类题目，如 “Number of Steps to Reduce a Number to Zero” 中的循环减法。  
  2. “环形数组”或“轮转”类题，如 “Circular Game” 中找出第几轮停止。  
  3. “前缀和 + 二分搜索” 常见于 “Find the Smallest Divisible Subset” 这类求区间累计的题目。  
- **一句话总结解题钥匙**：**先把大循环“一次性”消掉，再在剩余的“小循环”里逐个检查**。

---

## 反思

- **第一反应**：看到“循环扣除”就想直接模拟，写出 `while` 循环。  
- **最容易踩的坑**  
  - 忘记在 `k` 已经小于 `chalk[i]` 时直接返回，而不是先减再判断，导致答案错位。  
  - 对 `k` 很大的情况没有做取余，导致时间超限。  
  - 边界条件：`k` 正好等于某一轮的总和时，`k % total == 0`，这时应当从第一个学生重新开始检查（实现 A 已经自然处理）。  
- **下次类似题的第一步**：**先计算整轮的总消耗，用取余把问题规模压到一轮以内**，再决定是线性遍历还是二分搜索。这样既能保证正确性，又能避免时间超限。