# #2840. 检查是否可以通过操作 II 使字符串相等 / Check if Strings Can be Made Equal With Operations II

> 难度：中等 · 标签：Hash Table、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/check-if-strings-can-be-made-equal-with-operations-ii/)

---

## 题目（英文原版）

**Description**

You are given two strings s1 and s2, both of length n, consisting of lowercase English letters.
You can apply the following operation on any of the two strings any number of times:
Return true if you can make the strings s1 and s2 equal, and false otherwise.

**Examples**

**Example 1:**

```
Input: s1 = "abcdba", s2 = "cabdab"
Output: true
Explanation: We can apply the following operations on s1:
- Choose the indices i = 0, j = 2. The resulting string is s1 = "cbadba".
- Choose the indices i = 2, j = 4. The resulting string is s1 = "cbbdaa".
- Choose the indices i = 1, j = 5. The resulting string is s1 = "cabdab" = s2.
```

**Example 2:**

```
Input: s1 = "abe", s2 = "bea"
Output: false
Explanation: It is not possible to make the two strings equal.
```

**Constraints**

- n == s1.length == s2.length
- 1 <= n <= 105
- s1 and s2 consist only of lowercase English letters.

---

## 题目（中文翻译）

给定两个长度均为 **n** 的字符串 `s1` 和 `s2`，它们仅由小写英文字母组成。  
你可以对任意一个字符串无限次地执行以下 **操作（operation）**：

（题目原文未给出具体操作细节，保留原描述）

如果能够通过若干次操作使得 `s1` 与 `s2` 相等，则返回 `true`，否则返回 `false`。

## 示例

### 示例 1
**输入**  
` s1 = "abcdba", s2 = "cabdab" `  

**输出**  
`true`  

**解释**  
我们可以对 `s1` 依次执行以下操作：  
- 选择下标 `i = 0`、`j = 2`，得到 `s1 = "cbadba"`。  
- 选择下标 `i = 2`、`j = 4`，得到 `s1 = "cbbdaa"`。  
- 选择下标 `i = 1`、`j = 5`，得到 `s1 = "cabdab"`，此时 `s1` 与 `s2` 相等。

### 示例 2
**输入**  
` s1 = "abe", s2 = "bea" `  

**输出**  
`false`  

**解释**  
无法通过任何次数的操作使两个字符串相等。

## 约束

- `n == s1.length == s2.length`
- `1 <= n <= 10^5`
- `s1` 和 `s2` 只包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**模拟所有可能的交换**，把两串不断地换来换去，看看能否最终变成一样的。  
具体可以这么做：

1. 把两串看成状态，每一次可以任选一串中的任意两个下标 `i、j`（只要 `i` 与 `j` 同奇偶），把这两个字符交换。  
2. 用 BFS/DFS 把所有能够到达的状态遍历一遍，只要出现了 `s1 == s2` 就返回 `True`，遍历完都没有则返回 `False`。

> **类比**：把每个字符串想象成一副牌，只有同颜色（奇数位/偶数位）才能互相换位置。我们要把两副牌不停地洗牌，看看能不能把它们洗成完全一样的顺序。

**为什么它是正确的**  
只要我们把**所有合法的交换**都尝试一遍，就一定会覆盖所有可能的排列组合。如果其中有一种排列让两串相等，搜索一定能找到。

**时间/空间分析**  
- 每一次交换只改变两个字符的位置，字符串长度为 `n`，同奇偶的下标各有大约 `n/2` 个，所有可能的排列数是 `(n/2)! * (n/2)!`，会随 `n` 指数级增长。  
- BFS/DFS 需要把每个状态保存进队列/栈，最坏情况下会占用指数级的内存。

> **大白话**：  
> - `O(n!)`（阶乘）意味着“随着 `n` 增大，运行时间会飞快地变得不可接受”，比如 `n=10` 时已经是几千万次操作。  
> - `O(n!)` 的空间意味着需要记住几千万个字符串，显然不可能。

所以暴力搜索只能用来验证思路，实际提交时会 TLE（超时）或 MLE（内存超限）。

#### 代码（Python）

```python
from collections import deque

def can_be_equal_bruteforce(s1: str, s2: str) -> bool:
    """暴力 BFS，演示思路，仅供学习，实际不可用"""
    n = len(s1)
    # 用 tuple 存储两个字符串，方便哈希去重
    start = (s1, s2)
    q = deque([start])
    visited = {start}

    while q:
        a, b = q.popleft()
        if a == b:                     # 找到相等的情况
            return True

        # 对 a 进行一次合法交换
        a_list = list(a)
        for i in range(n):
            for j in range(i + 1, n):
                if (i % 2) == (j % 2):  # 只能同奇偶交换
                    a_list[i], a_list[j] = a_list[j], a_list[i]
                    new_state = (''.join(a_list), b)
                    if new_state not in visited:
                        visited.add(new_state)
                        q.append(new_state)
                    # 换回来，准备下一个 (i, j) 组合
                    a_list[i], a_list[j] = a_list[j], a_list[i]

        # 对 b 进行一次合法交换（同理）
        b_list = list(b)
        for i in range(n):
            for j in range(i + 1, n):
                if (i % 2) == (j % 2):
                    b_list[i], b_list[j] = b_list[j], b_list[i]
                    new_state = (a, ''.join(b_list))
                    if new_state not in visited:
                        visited.add(new_state)
                        q.append(new_state)
                    b_list[i], b_list[j] = b_list[j], b_list[i]

    return False
```

#### 复杂度  

- **时间复杂度**：`O((n/2)! * (n/2)!)`（指数级）——每个奇偶子序列的全排列都会被枚举。  
- **空间复杂度**：同样是指数级，因为需要保存所有已经访问过的状态。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**瓶颈在于枚举所有可能的交换顺序**。  
实际上，提示已经告诉我们：**只有同奇偶的下标可以互相换位**。这意味着：

- 偶数下标（0、2、4…）上的字符可以在这些位置之间随意排列。  
- 奇数下标（1、3、5…）上的字符也可以随意排列。

换句话说，**每个奇偶子序列内部的字符顺序是可以完全自由调换的**，但奇偶之间是不能互相渗透的。  
因此，只要两串在 **偶数位的字符集合** 完全相同，且在 **奇数位的字符集合** 也完全相同，就一定能把它们调成一样的；反之则不可能。

于是我们只需要统计两串的奇偶位字符出现次数（或把它们排序后比较），不必真的去做交换。

**核心数据结构：哈希表（字典）**  
- 哈希表就像一本字典，`key` 是字母，`value` 是它出现的次数。我们分别为偶数位和奇数位维护两个哈希表。

**实现步骤**  

1. 初始化四个计数器：`cnt1_even、cnt1_odd、cnt2_even、cnt2_odd`（均为 `defaultdict(int)`）。  
2. 遍历字符串的每个下标 `i`  
   - 若 `i` 为偶数，`cnt1_even[s1[i]] += 1`，`cnt2_even[s2[i]] += 1`。  
   - 若 `i` 为奇数，`cnt1_odd[s1[i]] += 1`，`cnt2_odd[s2[i]] += 1`。  
3. 最后比较 `cnt1_even == cnt2_even` 且 `cnt1_odd == cnt2_odd`，相等则返回 `True`，否则 `False`。

> **类比**：把奇数位的字符装进红盒子，偶数位的字符装进蓝盒子。只要两个人的红盒子里装的字母种类和数量相同，蓝盒子也相同，他们就能把盒子里的字母随意重新摆放，使得两串完全一样。

#### 代码（Python）

```python
from collections import defaultdict

def can_be_equal(s1: str, s2: str) -> bool:
    """
    判断是否可以通过只在同奇偶下标之间交换字符，使 s1 与 s2 相等。
    思路：比较奇数位字符的多集合和偶数位字符的多集合是否相同。
    """
    # 统计 s1 的奇偶位字符出现次数
    cnt1_even = defaultdict(int)   # 偶数位（0、2、4...）
    cnt1_odd  = defaultdict(int)   # 奇数位（1、3、5...）

    # 统计 s2 的奇偶位字符出现次数
    cnt2_even = defaultdict(int)
    cnt2_odd  = defaultdict(int)

    for i, (ch1, ch2) in enumerate(zip(s1, s2)):
        if i % 2 == 0:          # 偶数下标
            cnt1_even[ch1] += 1
            cnt2_even[ch2] += 1
        else:                   # 奇数下标
            cnt1_odd[ch1]  += 1
            cnt2_odd[ch2]  += 1

    # 两个字符串在偶数位的字符统计必须相同，奇数位同理
    return cnt1_even == cnt2_even and cnt1_odd == cnt2_odd
```

> **代码要点**  
> - `defaultdict(int)` 自动把不存在的键初始化为 `0`，写起来更简洁。  
> - `enumerate(zip(s1, s2))` 同时遍历两个字符串，省去两次循环。  
> - 最后直接比较两个字典，Python 会逐键比较值，等价于“每个字母出现次数相同”。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只需要一次遍历（`n` 为字符串长度），每一步的操作都是常数时间。  
  - 与暴力解的指数级时间相比，线性时间几乎可以在任何规模（`n ≤ 10⁵`）下瞬间完成。  

- **空间复杂度**：`O(1)`（常数空间）  
  - 哈希表的键最多是 26 个英文字母，计数值是整数，空间不随 `n` 增长而增长。  
  - 换句话说，无论字符串有多长，我们只需要固定的几百个字节来存放计数。

---

## 心得  

- **核心技巧**：把**位置的奇偶性**视作不可跨越的“隔离墙”，只需比较奇偶位字符的多集合是否相同。  
- **适用场景**：  
  1. **只能在相同颜色/奇偶位交换**的字符串问题（如 LeetCode 1657、1658）。  
  2. **分组置换**类问题——把元素分到若干独立的组内自由排列，只要每组的元素集合相等即可。  
- **一句话总结**：只要奇数位字符集合相等且偶数位字符集合相等，所有合法交换都能把两串变成一样。

---

## 反思  

- **第一反应**：看到“只能在同奇偶位置交换”，马上想到“把奇偶位分别看成两个独立的篮子”。  
- **最容易踩的坑**：  
  - 忘记对 **奇数位** 和 **偶数位** 分别计数，直接整体比较会得到错误结果。  
  - 边界条件：字符串长度为 `1` 时，只会有偶数位，需要保证代码在只有偶数位或只有奇数位的情况下仍然正确。  
- **下次遇到同类题**：第一步先判断**哪些位置是互相可达的**（比如同奇偶、同颜色、同模数），然后**统计每个可达集合的字符分布**，比较两串的分布是否一致。这样可以快速定位最简解。