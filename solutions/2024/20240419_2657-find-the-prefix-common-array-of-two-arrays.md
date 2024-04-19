# #2657. 求两个数组的前缀公共数组 / Find the Prefix Common Array of Two Arrays

> 难度：中等 · 标签：Array、Hash Table、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/find-the-prefix-common-array-of-two-arrays/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer permutations A and B of length n.
A prefix common array of A and B is an array C such that C[i] is equal to the count of numbers that are present at or before the index i in both A and B.
Return the prefix common array of A and B.
A sequence of n integers is called a permutation if it contains all integers from 1 to n exactly once.

**Examples**

**Example 1:**

```
Input: A = [1,3,2,4], B = [3,1,2,4]
Output: [0,2,3,4]
Explanation: At i = 0: no number is common, so C[0] = 0.
At i = 1: 1 and 3 are common in A and B, so C[1] = 2.
At i = 2: 1, 2, and 3 are common in A and B, so C[2] = 3.
At i = 3: 1, 2, 3, and 4 are common in A and B, so C[3] = 4.
```

**Example 2:**

```
Input: A = [2,3,1], B = [3,1,2]
Output: [0,1,3]
Explanation: At i = 0: no number is common, so C[0] = 0.
At i = 1: only 3 is common in A and B, so C[1] = 1.
At i = 2: 1, 2, and 3 are common in A and B, so C[2] = 3.
```

**Constraints**

- 1 <= A.length == B.length == n <= 50
- 1 <= A[i], B[i] <= n
- It is guaranteed that A and B are both a permutation of n integers.

---

## 题目（中文翻译）

你被给定两个长度为 `n` 的 0‑索引整数排列 `A` 和 `B`。  
`A` 与 `B` 的**前缀公共数组**（prefix common array）是一个数组 `C`，使得 `C[i]` 等于在下标 `i` 及其之前同时出现在 `A` 和 `B` 中的数字的个数。  
返回 `A` 和 `B` 的前缀公共数组。

如果一个长度为 `n` 的整数序列包含从 `1` 到 `n` 的所有整数且每个整数恰好出现一次，则称其为**排列**（permutation）。

### 示例

**示例 1**  
输入: `A = [1,3,2,4]`, `B = [3,1,2,4]`  
输出: `[0,2,3,4]`  
解释:  
- 当 `i = 0` 时，没有公共数字，所以 `C[0] = 0`。  
- 当 `i = 1` 时，`1` 和 `3` 同时出现在 `A` 和 `B` 的前缀中，故 `C[1] = 2`。  
- 当 `i = 2` 时，`1、2、3` 都是公共的，故 `C[2] = 3`。  
- 当 `i = 3` 时，`1、2、3、4` 都是公共的，故 `C[3] = 4`。

**示例 2**  
输入: `A = [2,3,1]`, `B = [3,1,2]`  
输出: `[0,1,3]`  
解释:  
- 当 `i = 0` 时，没有公共数字，所以 `C[0] = 0`。  
- 当 `i = 1` 时，只有 `3` 是公共的，故 `C[1] = 1`。  
- 当 `i = 2` 时，`1、2、3` 都是公共的，故 `C[2] = 3`。

### 约束条件
- `1 <= A.length == B.length == n <= 50`
- `1 <= A[i], B[i] <= n`
- 已保证 `A` 与 `B` 均为 `n` 个整数的**排列**（permutation）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每个下标 `i`，分别把 `A[0..i]` 和 `B[0..i]` 里的元素放进两个集合（`set`），再求交集的大小**。  
- **集合**在这里可以类比成“字典的抽屉”。往抽屉里放东西，想要知道两个抽屉里都有多少相同的东西，只要把两抽屉的内容对比一下（交集）即可。  
- 由于 `A`、`B` 都是 **排列**（每个数字 1~n 恰好出现一次），所以只要在两个前缀里都出现过的数字，就一定只出现一次。  

这种做法一定能得到正确答案，因为我们把题目要求的「在 i 位置之前两数组都出现过的数字」全部枚举并统计了。

#### 代码（Python）

```python
def find_prefix_common_array_bruteforce(A, B):
    n = len(A)
    C = [0] * n                # 用来保存答案
    for i in range(n):
        # 把 A[0..i]、B[0..i] 放进集合，集合类似“字典的抽屉”，不关心顺序，只关心是否出现
        set_a = set(A[:i + 1])
        set_b = set(B[:i + 1])
        # 交集的大小就是既在 A 前缀也在 B 前缀出现的数字个数
        C[i] = len(set_a & set_b)   # & 表示集合交集
    return C
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：外层遍历 `i` 一共 `n` 次；每次都要把前缀切片 (`A[:i+1]`) 并转成集合，这一步本质上是遍历 `i+1` 个元素，平均下来是 `O(n)`，两层相乘就是 `O(n²)`。  
  用大白话说，就是如果 `n` 是 10，最多要做 10 + 9 + … + 1 ≈ 55 次“看元素”，`n` 越大，工作量会像平方一样快速增长。

- **空间复杂度**：`O(n)`  
  每次循环会创建两个集合，最坏情况下集合里会有 `i+1 ≤ n` 个元素，所以额外的空间最多是 `O(n)`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次都要重新遍历前缀**。其实我们只需要 **一次遍历**，在遍历的过程中把已经看到的数字记录下来，就能立即知道当前前缀里有多少公共数字。

关键点：

1. **频次数组（或哈希表）**  
   - 把它想象成“一张登记表”，表格的行是数字（1~n），列是“出现次数”。  
   - 初始时每个数字的次数都是 0。  
   - 当我们看到 `A[i]` 时，把对应的次数 `+1`；同理看到 `B[i]` 也 `+1`。  
   - 由于 `A`、`B` 都是排列，**同一个数字最多只会出现两次**（一次在 A，一次在 B）。当某个数字的次数恰好变成 2，说明它已经在两个前缀里都出现过，此时公共计数 `common` 加 1。

2. **累计答案**  
   - 用一个变量 `common` 记录截至当前下标已经有多少公共数字。  
   - 每处理完位置 `i`，把 `common` 写入答案数组 `C[i]`。

整个过程只需要一次线性遍历，时间 `O(n)`，空间 `O(n)`（登记表大小为 `n+1`）。

#### 代码（Python）

```python
def find_prefix_common_array(A, B):
    """
    返回 A 与 B 的前缀公共数组 C。
    思路：使用频次数组（相当于哈希表）记录每个数字出现的次数，
    当次数从 1 变成 2 时，说明该数字在两个前缀中都出现过，公共计数 +1。
    """
    n = len(A)
    freq = [0] * (n + 1)   # freq[x] 表示数字 x 已出现的次数，0 表示还没见过
    common = 0             # 当前前缀里公共数字的个数
    C = [0] * n

    for i in range(n):
        # 处理 A[i]
        freq[A[i]] += 1
        if freq[A[i]] == 2:          # 第 2 次出现，说明在 B 的前缀里也出现过
            common += 1

        # 处理 B[i]
        freq[B[i]] += 1
        if freq[B[i]] == 2:          # 同理
            common += 1

        C[i] = common                # 把累计的公共计数写进答案
    return C
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只需要一次遍历，每个元素的处理都是常数时间（`+1`、比较、赋值），所以工作量随 `n` 成线性关系。和暴力解的 `O(n²)` 相比，提升非常明显。

- **空间复杂度**：`O(n)`  
  需要一个大小为 `n+1` 的频次数组来记录每个数字出现的次数，另外答案数组 `C` 也占 `O(n)`。总的额外空间仍是线性级别。

---

## 心得

- **核心技巧**：利用**哈希表/频次数组**一次遍历统计“出现次数”，当次数达到 2 时即可确认该元素在两个前缀中都出现过。  
- **适用的题型**：  
  1. 两个序列的前缀交集计数（本题）。  
  2. “找出两个数组的共同前缀元素个数” 类似问题。  
  3. “子数组中出现次数恰好两次的元素个数” 这类需要统计出现次数的题目。  
- **一句话总结解题钥匙**：**“只要能在遍历中把‘已经出现过’的信息记下来，就不必重复扫描前缀”。**

---

## 反思

- **第一反应**：看到“前缀公共数组”，立刻想到“集合交集”。于是写出暴力解——把每个前缀都装进集合再比较。  
- **最容易踩的坑**：  
  - 忘记 **两次出现才算公共**：因为是排列，单独出现一次并不算公共，需要等到第二次才计数。  
  - **数组越界**：频次数组的下标要对应数字本身，记得开 `n+1` 长度（下标 0 不用）。  
  - **重复计数**：在同一次循环里，若 `A[i]` 与 `B[i]` 恰好相同，必须在处理 `A[i]` 后再处理 `B[i]`，否则会漏掉一次计数。  
- **下次遇到同类题**：第一步先思考“有没有办法把已经看到的信息保存下来（哈希表 / 前缀和）”，再决定是一次遍历还是多次遍历。这样往往能直接跳到最优解的方向。