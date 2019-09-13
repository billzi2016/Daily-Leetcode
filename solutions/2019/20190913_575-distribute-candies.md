# #575. **分配糖果** / Distribute Candies

> 难度：简单 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/distribute-candies/)

---

## 题目（英文原版）

**Description**

Alice has n candies, where the ith candy is of type candyType[i]. Alice noticed that she started to gain weight, so she visited a doctor.
The doctor advised Alice to only eat n / 2 of the candies she has (n is always even). Alice likes her candies very much, and she wants to eat the maximum number of different types of candies while still following the doctor's advice.
Given the integer array candyType of length n, return the maximum number of different types of candies she can eat if she only eats n / 2 of them.

**Examples**

**Example 1:**

```
Input: candyType = [1,1,2,2,3,3]
Output: 3
Explanation: Alice can only eat 6 / 2 = 3 candies. Since there are only 3 types, she can eat one of each type.
```

**Example 2:**

```
Input: candyType = [1,1,2,3]
Output: 2
Explanation: Alice can only eat 4 / 2 = 2 candies. Whether she eats types [1,2], [1,3], or [2,3], she still can only eat 2 different types.
```

**Example 3:**

```
Input: candyType = [6,6,6,6]
Output: 1
Explanation: Alice can only eat 4 / 2 = 2 candies. Even though she can eat 2 candies, she only has 1 type.
```

**Constraints**

- n == candyType.length
- 2 <= n <= 104
- n is even.
- -105 <= candyType[i] <= 105

---

## 题目（中文翻译）

Alice 有 `n` 颗糖果，第 `i` 颗糖果的类型为 `candyType[i]`。Alice 发现自己开始增重，于是去看医生。  
医生建议 Alice 只能吃掉她拥有的 `n / 2` 颗糖果（`n` 总是偶数）。Alice 非常喜欢这些糖果，她想在遵循医生建议的前提下，尽可能多地吃到不同类型的糖果。  

给定长度为 `n` 的整数数组 `candyType`，返回 Alice 在只能吃 `n / 2` 颗糖果的情况下，能够吃到的 **不同类型**（different types）的最大数量。

---

### 示例

**示例 1**

```text
Input: candyType = [1,1,2,2,3,3]
Output: 3
Explanation: Alice 只能吃 6 / 2 = 3 颗糖果。由于糖果类型恰好有 3 种，她可以每种吃一颗。
```

**示例 2**

```text
Input: candyType = [1,1,2,3]
Output: 2
Explanation: Alice 只能吃 4 / 2 = 2 颗糖果。无论她选择吃 `[1,2]`、`[1,3]` 还是 `[2,3]`，最多只能吃到 2 种不同的糖果。
```

**示例 3**

```text
Input: candyType = [6,6,6,6]
Output: 1
Explanation: Alice 只能吃 4 / 2 = 2 颗糖果。虽然可以吃两颗，但所有糖果只有 1 种类型。
```

---

### 约束条件

- `n == candyType.length`
- `2 <= n <= 10^4`
- `n` 为偶数
- `-10^5 <= candyType[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的吃法全部列举出来**，然后挑出能吃到最多不同种类的那一种。  
具体步骤可以想象成：

1. 从 `candyType` 中挑选恰好 `n/2` 块糖（`n` 为糖的总数），这相当于在 **全部糖** 中**选出一个子集**。  
2. 统计这个子集里出现了多少种不同的糖（用集合去重）。  
3. 把所有子集的结果取最大值。

> **生活化类比**：把糖果想成一本书的所有页码，医生说只能读 `n/2` 页。我们想要读到尽可能多的不同章节（糖的种类），最笨的办法就是把 **所有可能的 `n/2` 页组合** 都列出来，看看每种组合能覆盖多少章节，最后挑出章节数最多的那种。

> **为什么它是正确的**：因为我们枚举了**所有合法的吃法**，所以答案一定会在这些枚举结果里出现。只要遍历完整，就不会错过最优解。

> **为什么不实际使用**：组合数 `C(n, n/2)` 在 `n` 甚至只有 20 时已经非常大，`n` 最大可达 `10^4`，根本不可能在时间限制内完成。  
> 这一步主要帮助我们**发现瓶颈**：枚举子集的过程耗时太久，必须寻找更高效的方式。

#### 代码（Python）

```python
import itertools
from typing import List

def distributeCandies_bruteforce(candyType: List[int]) -> int:
    n = len(candyType)
    half = n // 2                     # 必须吃的糖果数量
    max_kinds = 0                     # 记录最大种类数

    # 生成所有从 n 块糖中挑出 half 块的组合（每种组合是索引的元组）
    for idx_tuple in itertools.combinations(range(n), half):
        # 取出对应的糖果种类
        chosen = [candyType[i] for i in idx_tuple]
        # 用集合去重，得到不同种类的数量
        kinds = len(set(chosen))
        # 更新最大值
        max_kinds = max(max_kinds, kinds)

    return max_kinds
```

> **关键行解释**  
> - `itertools.combinations(range(n), half)`：相当于把所有可能的“挑选 half 块糖”的方式全部列出来。  
> - `set(chosen)`：集合像字典的“查字典”，把相同的糖果种类合在一起，只留下不同的种类。  

#### 复杂度  

- **时间复杂度**：`O(C(n, n/2) * n)`  
  - `C(n, n/2)` 是组合数，表示有多少种挑选方式，随 `n` 指数增长。  
  - 每种组合我们还要遍历一次 `half`（≈ n/2）个元素去统计种类，故再乘以 `n`。  
  - 用大白话说，就是“**几乎不可能在几秒内跑完**”，所以这不是可行的解法。  

- **空间复杂度**：`O(n)`（用于存放当前组合的临时列表和集合）  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**枚举子集**是最耗时的环节。我们其实不需要知道 **具体挑了哪几块糖**，只需要知道 **最多能吃到多少种不同的糖**。  
观察题目可以得出两个关键点：

1. **上限 1**：Alice 最多只能吃 `n/2` 块糖，所以不管有多少种糖，她最多只能得到 `n/2` 种不同的糖。  
2. **上限 2**：如果糖的种类总数（记作 `distinct`）本身就少于 `n/2`，那么她最多只能吃到 `distinct` 种，因为没有更多种类可供选择。

于是答案其实就是这两个上限的**较小值**：

```
answer = min(number_of_distinct_types, n/2)
```

要得到 `number_of_distinct_types`，最合适的数据结构就是 **哈希集合（HashSet）**。  
哈希集合的工作方式可以类比为**字典**：把每一种糖的“名字”当作键（key），只要出现一次就放进集合，重复的键会自动被忽略。这样遍历一次数组，就能得到所有不同种类的数量。

#### 代码（Python）

```python
from typing import List

def distributeCandies(candyType: List[int]) -> int:
    # 1. 用集合收集所有不同的糖果种类
    distinct_types = set()          # 哈希集合，像“查字典”，key 是糖的种类
    for candy in candyType:
        distinct_types.add(candy)   # 重复的种类自动被忽略

    # 2. 计算 Alice 能吃的糖果数量上限
    half = len(candyType) // 2      # 必须吃的糖块数

    # 3. 答案是两者的较小值
    return min(len(distinct_types), half)
```

> **关键行解释**  
> - `set()`：创建一个空的哈希集合。往里面放东西时，如果已经有相同的元素，集合会自动去重。  
> - `distinct_types.add(candy)`：把每块糖的种类加入集合，相同种类只会留下一个。  
> - `len(distinct_types)`：集合的大小，就是糖的不同种类数。  
> - `min(..., half)`：取两者中更小的那个，正是题目要求的最大可吃种类数。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，向集合插入的平均时间是 `O(1)`（常数级），所以整体是线性时间。  
  - 用大白话说，就是“**跑一遍糖的列表**，几乎立刻得到答案”。  

- **空间复杂度**：`O(d)`，`d` 为糖的不同种类数。最坏情况下每块糖都不一样，`d = n`，即需要额外存放 `n` 个元素的集合。  

---

## 心得  

- **核心技巧**：利用**哈希集合**统计不同元素的数量，再结合**上限取最小值**得到答案。  
- **适用的题型**  
  1. “统计数组中不同元素的个数”类题目（如 LeetCode 347. 前 K 个出现最多的元素）。  
  2. “在限制条件下取最大/最小种类数”类题目（如 LeetCode 1129. 颜色分类）。  
  3. “求集合交/并大小”类题目（如 LeetCode 1657. 确定两个数组的相同元素数量）。  
- **一句话总结**：**先算出种类数，再和可吃的上限比较，取较小者即为答案**。  

---

## 反思  

- **第一反应**：看到“最多吃 n/2 块糖，想要种类最多”，自然会想到“先数有多少种不同的糖”。  
- **最容易踩的坑**  
  1. 忘记 `n` 必须是偶数，直接写 `n//2` 会在奇数输入时出错（虽然题目保证是偶数）。  
  2. 只返回 `len(set(candyType))` 而忘记与 `n/2` 取最小，导致在种类数大于 `n/2` 时答案错误。  
  3. 对负数糖果类型或大范围值没有特殊处理——使用哈希集合自然能兼容。  
- **下次类似题的第一步**：**先弄清楚“上限”是什么**（比如数量、容量、时间等），然后**用合适的集合/计数结构**快速得到实际可达的最大值。