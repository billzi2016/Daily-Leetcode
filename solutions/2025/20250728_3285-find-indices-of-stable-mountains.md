# #3285. 寻找稳定山峰的索引 / Find Indices of Stable Mountains

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/find-indices-of-stable-mountains/)

---

## 题目（英文原版）

**Description**

There are n mountains in a row, and each mountain has a height. You are given an integer array height where height[i] represents the height of mountain i, and an integer threshold.
A mountain is called stable if the mountain just before it (if it exists) has a height strictly greater than threshold. Note that mountain 0 is not stable.
Return an array containing the indices of all stable mountains in any order.

**Examples**

**Example 1:**

```
Input: height = [1,2,3,4,5], threshold = 2
Output: [3,4]
Explanation:
```

**Example 2:**

```
Input: height = [10,1,10,1,10], threshold = 3
Output: [1,3]
```

**Example 3:**

```
Input: height = [10,1,10,1,10], threshold = 10
Output: []
```

**Constraints**

- 2 <= n == height.length <= 100
- 1 <= height[i] <= 100
- 1 <= threshold <= 100

---

## 题目（中文翻译）

**题目描述**

一排共有 `n` 座山峰（mountain），每座山峰都有一个高度（height）。给定一个整数数组 `height`，其中 `height[i]` 表示第 `i` 座山峰的高度，以及一个整数阈值（threshold）。

如果一座山峰前面紧邻的那座山峰（如果存在）的高度严格大于 `threshold`，则该山峰被称为**稳定山峰（stable mountain）**。注意第 `0` 座山峰不算稳定。

返回一个数组，包含所有稳定山峰的索引，顺序不限。

**示例**

示例 1  
Input: `height = [1,2,3,4,5]`, `threshold = 2`  
Output: `[3,4]`  
解释：  
- 索引 `3` 的山峰前面的山峰高度为 `3 > 2`，满足条件。  
- 索引 `4` 的山峰前面的山峰高度为 `4 > 2`，满足条件。  

示例 2  
Input: `height = [10,1,10,1,10]`, `threshold = 3`  
Output: `[1,3]`  
解释：  
- 索引 `1` 的山峰前面的山峰高度为 `10 > 3`。  
- 索引 `3` 的山峰前面的山峰高度为 `10 > 3`。  

示例 3  
Input: `height = [10,1,10,1,10]`, `threshold = 10`  
Output: `[]`  
解释：没有山峰满足前一座山峰高度严格大于 `10` 的条件。

**约束条件**

- `2 <= n == height.length <= 100`
- `1 <= height[i] <= 100`
- `1 <= threshold <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对每一座山 i（i > 0）都去检查它左边的那座山 height[i‑1] 是否严格大于 threshold**。  
如果满足条件，就把 i 加入答案列表。  

- **使用的数据结构**：  
  - `list`（Python 中的数组）用来保存原始的 `height`。  
  - 另一个 `list` 用来收集满足条件的下标。  
  - 可以把 “查询前一座山的高度” 想象成在 **字典**（查字典）里找前一个单词的解释，只不过这里我们直接用数组的下标定位，时间是 **O(1)**。  

- **为什么正确**：  
 题目定义“stable mountain” 只和它**左边紧挨着的那座山**有关，和更左边的山没有任何联系。只要我们对每个 i 检查 `height[i‑1] > threshold`，就完全符合题意。

- **时间/空间复杂度**：  
  - **时间**：如果我们对每个 i 再遍历一次左边所有山（即把“左边的山”看成一个区间），最坏会是 `1 + 2 + … + (n‑1) = O(n²)`，这就是最笨的实现。  
  - **空间**：只用了常数个额外变量和答案列表，答案列表最多存 `n‑1` 个下标，算作 `O(n)`（因为输出本身就需要这么多空间）。

> **大白话**：`O(n²)` 就像你让每个人去数所有站在他左边的人，总共要数 `n²/2` 次，显得很费劲。  

#### 代码（Python）  
```python
def stable_mountains_bruteforce(height, threshold):
    n = len(height)
    res = []                       # 用来存放满足条件的下标
    # 从第二座山开始检查（下标 1），因为第 0 座山永远不算 stable
    for i in range(1, n):
        # 暴力做法：遍历 i 左边的所有山，找出最大的下标 j = i-1
        # 实际上只需要检查 height[i-1]，这里写成循环是为了演示 O(n²) 思路
        for j in range(i - 1, i):  # 只遍历一次，保持结构
            if height[j] > threshold:   # 前一座山高度严格大于阈值
                res.append(i)           # i 就是 stable mountain 的下标
                break                   # 找到后直接结束内层循环
    return res
```

#### 复杂度  
- **时间复杂度**：`O(n²)` —— 想象每座山都要去“遍历”左边的所有山，次数随 `n` 的平方增长。  
- **空间复杂度**：`O(n)` —— 需要一个列表来保存答案，最坏情况下会保存 `n‑1` 个下标。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**真正决定是否 stable 的只有前一座山的高度**，不需要遍历更远的山。  
慢的地方在于内层的循环（即使我们只循环一次，写法仍然显得多余），我们完全可以把检查**前一座山**的工作压缩到 **一次线性遍历** 中：

1. 从下标 `1` 开始遍历整个数组。  
2. 直接比较 `height[i‑1]` 与 `threshold`。  
3. 若满足 `>`，把 `i` 加入答案。  

这一步只需要 **O(1)** 的时间检查一次，整个过程只走一遍数组，时间是 `O(n)`。  
使用的核心技巧其实是 **一次遍历（单次线性扫描）**，在很多只依赖相邻元素的题目里都是最直接、最高效的做法。

> **类比**：想象你排队买票，只需要看前面一个人手里的票是否符合条件，而不需要去数前面所有人的票。  

#### 代码（Python）  
```python
def stable_mountains_optimal(height, threshold):
    """
    返回所有 stable mountain 的下标。
    思路：一次遍历，直接比较前一座山的高度是否 > threshold。
    """
    res = []                         # 用来保存答案
    for i in range(1, len(height)): # 从第二座山开始（下标 1）
        if height[i - 1] > threshold:   # 前一座山高度严格大于阈值
            res.append(i)               # i 即为 stable mountain 的下标
    return res
```

#### 复杂度  
- **时间复杂度**：`O(n)` —— 只遍历一次数组，`n` 越大，耗时只会线性增长。相比暴力的 `O(n²)`，快了一个数量级。  
- **空间复杂度**：`O(n)` —— 仍需存放答案列表，最坏情况保存 `n‑1` 个下标。除答案外，只用了常数级的临时变量。  

---  

## 心得  

- **核心技巧**：**相邻元素比较 + 单次线性扫描**。  
- **适用的题型**  
  1. 判断数组中“满足某种相邻关系”的位置（如 “左边比右边大”）。  
  2. “前缀条件”类题目，只需检查当前元素之前的一个或少数几个元素（如 “前一个数是否为偶数”）。  
- **解题钥匙**：**先问自己：答案是否只依赖相邻元素？如果是，往往可以用一次遍历解决**。  

## 反思  

- **第一反应**：直接写两层循环，遍历左边所有山——这是一种“把所有可能都检查一遍”的自然思路。  
- **最容易踩的坑**  
  - 忘记 **mountain 0** 永远不算 stable，需要从下标 `1` 开始。  
  - 条件是 **严格大于** (`>`) 而不是“大于等于”，阈值相等时不算 stable。  
- **下次类似题的第一步**：先判断“**是否只和前一个（或后一个）元素有关**”。如果是，立刻考虑“一次遍历”而不是多层循环。