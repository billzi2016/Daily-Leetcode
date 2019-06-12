# #455. 分配饼干 / Assign Cookies

> 难度：简单 · 标签：Array、Two Pointers、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/assign-cookies/)

---

## 题目（英文原版）

**Description**

Assume you are an awesome parent and want to give your children some cookies. But, you should give each child at most one cookie.
Each child i has a greed factor g[i], which is the minimum size of a cookie that the child will be content with; and each cookie j has a size s[j]. If s[j] >= g[i], we can assign the cookie j to the child i, and the child i will be content. Your goal is to maximize the number of your content children and output the maximum number.
Note: This question is the same as  2410: Maximum Matching of Players With Trainers.

**Examples**

**Example 1:**

```
Input: g = [1,2,3], s = [1,1]
Output: 1
Explanation: You have 3 children and 2 cookies. The greed factors of 3 children are 1, 2, 3. 
And even though you have 2 cookies, since their size is both 1, you could only make the child whose greed factor is 1 content.
You need to output 1.
```

**Example 2:**

```
Input: g = [1,2], s = [1,2,3]
Output: 2
Explanation: You have 2 children and 3 cookies. The greed factors of 2 children are 1, 2. 
You have 3 cookies and their sizes are big enough to gratify all of the children, 
You need to output 2.
```

**Constraints**

- 1 <= g.length <= 3 * 104
- 0 <= s.length <= 3 * 104
- 1 <= g[i], s[j] <= 231 - 1

---

## 题目（中文翻译）

假设你是一位了不起的家长，想要给孩子们分配饼干。但每个孩子最多只能分到一块饼干。  
每个孩子 `i` 有一个贪心因子 `g[i]`，即孩子能够满足的最小饼干大小；每块饼干 `j` 有一个大小 `s[j]`。如果 `s[j] >= g[i]`，则可以把第 `j` 块饼干分配给第 `i` 个孩子，使该孩子感到满足。你的目标是 **最大化** 满意的孩子数量，并输出该最大值。

**示例 1**  

**示例 2**  

**约束**  
- 注意：此题等价于 2410: Maximum Matching of Players With Trainers。

**示例**

**示例 1**  
```
Input: g = [1,2,3], s = [1,1]
Output: 1
Explanation: 你有 3 个孩子和 2 块饼干。3 个孩子的贪心因子分别为 1、2、3。虽然有 2 块饼干，但它们的大小都是 1，只有贪心因子为 1 的孩子能够得到满足。需要输出 1。
```

**示例 2**  
```
Input: g = [1,2], s = [1,2,3]
Output: 2
Explanation: 你有 2 个孩子和 3 块饼干。2 个孩子的贪心因子分别为 1、2。三块饼干的大小都足以满足所有孩子，故能够让两位孩子都满足。需要输出 2。
```

**约束条件**  
- `1 <= g.length <= 3 * 10^4`
- `0 <= s.length <= 3 * 10^4`
- `1 <= g[i], s[j] <= 2^31 - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个孩子都拿去尝试所有的饼干，看能不能满足。  
可以把 **孩子** 看成一排小朋友的座位，**饼干** 看成一堆不同大小的糖果。  
我们把每个孩子 `i` 的贪心值 `g[i]` 与每块饼干 `j` 的大小 `s[j]` 两两比较：

- 若 `s[j] >= g[i]`，说明这块饼干够大，孩子 `i` 可以吃这块饼干。  
- 每块饼干只能喂给 **最多一个** 孩子，所以一旦把饼干 `j` 分配给了某个孩子，就要把它标记为“已使用”，后面不能再用了。

只要把所有可能的 `(孩子, 饼干)` 配对都尝试一遍，就一定能得到最大的满足孩子数（因为我们遍历了所有组合），只不过效率非常低。

> **为什么这个方法一定能得到正确答案？**  
> 因为我们没有做任何剪枝或提前决定，而是把所有合法的配对都枚举出来，最后取最大值，自然不会错过最优方案。

#### 代码（Python）

```python
from typing import List

def findContentChildren_bruteforce(g: List[int], s: List[int]) -> int:
    n = len(g)          # 孩子数量
    m = len(s)          # 饼干数量
    used = [False] * m  # 记录每块饼干是否已经被分配

    # 统计满足的孩子数量
    satisfied = 0

    # 对每个孩子尝试所有饼干
    for i in range(n):
        for j in range(m):
            # 如果这块饼干还没有被使用，且大小足够
            if not used[j] and s[j] >= g[i]:
                used[j] = True   # 标记为已使用
                satisfied += 1   # 该孩子满意
                break            # 这位孩子已经分到饼干，进入下一个孩子
    return satisfied
```

- 第 4 行 `used` 相当于一本记事本，记下哪块饼干已经被“借出”。
- 第 9‑15 行是两层循环，外层遍历孩子，内层遍历饼干，找到第一块合适且未被占用的饼干就分配。

#### 复杂度

- **时间复杂度：** `O(n * m)`  
  这里的 `n` 是孩子数量，`m` 是饼干数量。意思是最坏情况下我们要比较 `n` × `m` 次（比如每个孩子都要遍历所有饼干才能找到合适的），这在数据量大时会非常慢。

- **空间复杂度：** `O(m)`  
  只用了一个长度为 `m` 的布尔数组 `used` 来记录饼干是否被使用，随饼干数量线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于我们每次都要把所有饼干都遍历一遍。  
如果把孩子和饼干都 **从小到大排好序**，就可以用 **双指针** 只遍历一次就完成配对，省去大量无效比较。

**关键观察**：

1. 贪心原则：**把最小的孩子配上最小的能满足他的饼干**。  
   - 为什么？因为如果我们把大饼干留给小孩子，可能导致后面的大孩子找不到足够大的饼干，浪费了资源。  
   - 把最小的需求先满足，后面的“大需求”还能使用更大的资源，这样整体配对数最多。

2. 排序后，使用两个指针：
   - `i` 指向当前要满足的孩子（在 `g` 中），从左到右遍历。
   - `j` 指向当前可用的最小饼干（在 `s` 中），同样从左到右遍历。
   - 当 `s[j] >= g[i]` 时，说明这块饼干可以满足孩子 `i`，两指针都向右移动，计数加一。
   - 否则 `s[j] < g[i]`，说明这块饼干太小，根本不可能满足任何后面的孩子（因为后面的孩子贪心值更大），所以只把 `j` 向右移动，尝试更大的饼干。

**类比**：想象你在排队买糖果，孩子们排好序（从最小的胃口到最大的），糖果也排好序（从最小到最大）。你总是让最小的孩子先挑最小够吃的糖果，这样不会让大孩子因为只剩下小糖果而饿肚子。

#### 代码（Python）

```python
from typing import List

def findContentChildren(g: List[int], s: List[int]) -> int:
    # 1. 把孩子的贪心值和饼干的大小都从小到大排好序
    g.sort()          # 对孩子的需求进行升序排列
    s.sort()          # 对饼干的大小进行升序排列

    i = 0  # 孩子指针，指向当前要喂的孩子
    j = 0  # 饼干指针，指向当前可用的最小饼干
    satisfied = 0     # 满意的孩子数量

    # 2. 双指针遍历，直到任意一方遍历完
    while i < len(g) and j < len(s):
        if s[j] >= g[i]:          # 这块饼干够大，满足当前孩子
            satisfied += 1       # 满意孩子数加一
            i += 1                # 继续看下一个孩子
            j += 1                # 这块饼干已经用掉，换下一块更大的饼干
        else:
            # 饼干太小，直接跳过这块饼干，尝试更大的
            j += 1

    return satisfied
```

- 第 4‑5 行 `sort()` 就像把孩子和饼干排成两条从小到大的队伍。
- 第 9‑16 行是核心的 **双指针** 循环：每次比较最前面的孩子和最前面的饼干，决定是否配对或跳过。

#### 复杂度

- **时间复杂度：** `O(n log n + m log m)`  
  这里的 `n` 是孩子数量，`m` 是饼干数量。主要花费在排序上（排序的代价是 `n log n` 和 `m log m`），随后遍历一次的代价是 `O(n + m)`，相对于暴力解的 `O(n*m)` 快了很多。  
  **大白话**：把东西先排好序需要一点时间（类似把书按照字母顺序摆好），但排好序后找东西就非常快了。

- **空间复杂度：** `O(1)`（如果使用原地排序的话）  
  只用了常数级的额外变量 `i、j、satisfied`，不随输入规模增长。

---

## 心得

- **核心技巧**：**贪心 + 双指针 + 排序**  
  先把需求和资源都排好序，然后总是让“最小需求配最小能满足的资源”，保证不浪费大资源。

- **适用的题型**  
  1. `455. Assign Cookies`（本题）  
  2. `2529. Maximum Number of Children Who Can Eat the Ice Cream`（相同思路）  
  3. `345. Reverse Vowels of a String`（双指针）——虽然不是贪心，但同样使用双指针遍历两端。

- **一句话总结解题钥匙**：**先排序，再用双指针把最小需求和最小可用资源配对**。

---

## 反思

- **第一反应**：直接想到遍历每个孩子去找合适的饼干，写成两层循环——这就是暴力解的雏形。  
- **最容易踩的坑**  
  - 忘记把孩子和饼干都排序，导致配对顺序不对，结果不是最大满意数。  
  - 边界情况：当 `s` 为空或比所有 `g` 都小，应该直接返回 `0`，循环条件 `while i < len(g) and j < len(s)` 能自然处理。  
- **下次遇到同类题**：第一步就想 **“能否把需求和资源都排序”**，如果能，通常可以用 **双指针** 或 **贪心** 的方式一次遍历得到最优解。