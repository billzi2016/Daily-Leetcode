# #710. 带黑名单的随机抽取 / Random Pick with Blacklist

> 难度：困难 · 标签：Array、Hash Table、Math、Binary Search、Sorting、Randomized · [LeetCode 链接](https://leetcode.com/problems/random-pick-with-blacklist/)

---

## 题目（英文原版）

**Description**

You are given an integer n and an array of unique integers blacklist. Design an algorithm to pick a random integer in the range [0, n - 1] that is not in blacklist. Any integer that is in the mentioned range and not in blacklist should be equally likely to be returned.
Optimize your algorithm such that it minimizes the number of calls to the built-in random function of your language.
Implement the Solution class:

**Examples**

**Example 1:**

```
Input
["Solution", "pick", "pick", "pick", "pick", "pick", "pick", "pick"]
[[7, [2, 3, 5]], [], [], [], [], [], [], []]
Output
[null, 0, 4, 1, 6, 1, 0, 4]

Explanation
Solution solution = new Solution(7, [2, 3, 5]);
solution.pick(); // return 0, any integer from [0,1,4,6] should be ok. Note that for every call of pick,
                 // 0, 1, 4, and 6 must be equally likely to be returned (i.e., with probability 1/4).
solution.pick(); // return 4
solution.pick(); // return 1
solution.pick(); // return 6
solution.pick(); // return 1
solution.pick(); // return 0
solution.pick(); // return 4
```

**Constraints**

- 1 <= n <= 109
- 0 <= blacklist.length <= min(105, n - 1)
- 0 <= blacklist[i] < n
- All the values of blacklist are unique.
- At most 2 * 104 calls will be made to pick.

---

## 题目（中文翻译）

**题目描述**  
给定一个整数 `n` 和一个由唯一整数构成的数组 `blacklist`（黑名单），请设计一种算法，从区间 `[0, n - 1]` 中随机抽取一个不在 `blacklist` 中的整数。区间内所有未被 `blacklist` 包含的整数出现的概率必须相等。  
要求尽可能减少对语言自身的内置随机函数（built-in random function）的调用次数。

**实现要求**  
实现 `Solution` 类，使其能够在构造函数中接受 `n` 与 `blacklist`，并提供 `pick()` 方法返回满足条件的随机整数。

**示例**  
```text
Input
["Solution", "pick", "pick", "pick", "pick", "pick", "pick", "pick"]
[[7, [2, 3, 5]], [], [], [], [], [], [], []]
Output
[null, 0, 4, 1, 6, 1, 0, 4]

Explanation
Solution solution = new Solution(7, [2, 3, 5]);
solution.pick(); // 返回 0，合法返回值为 [0,1,4,6] 中的任意整数。注意每一次调用 `pick` 时，
                 // 0、1、4、6 出现的概率必须相等（即概率为 1/4）。
solution.pick(); // 返回 4
solution.pick(); // 返回 1
solution.pick(); // 返回 6
solution.pick(); // 返回 1
solution.pick(); // 返回 0
solution.pick(); // 返回 4
```

**约束条件**  

- `1 <= n <= 10^9`
- `0 <= blacklist.length <= min(10^5, n - 1)`
- `0 <= blacklist[i] < n`
- `blacklist` 中的所有值互不相同
- 最多会调用 `pick` 方法 `2 * 10^4` 次

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是先把 **合法的数字**（即 `[0, n-1]` 中不在 `blacklist` 里的数）全部列出来，保存到一个数组 `valid`，以后每次 `pick` 时只要在 `valid` 上随机取一个下标即可。

> **类比**：把 `valid` 想成一本「号码手册」，每次我们只需要翻开手册的某一页（随机下标），对应的号码就是答案。  
> **哈希表**（字典）在这里可以帮助我们快速判断一个数字是否在黑名单里，就像查字典时先看单词是否存在。

这种方法一定能得到均匀分布的结果，因为我们把所有合法号码平等地放进了手册。

#### 代码（Python）

```python
import random
from typing import List

class Solution:
    def __init__(self, n: int, blacklist: List[int]):
        # 把黑名单放进集合，查找 O(1)
        self.black = set(blacklist)          # 哈希表：黑名单 = {2,3,5,...}
        # 构造合法号码列表
        self.valid = [i for i in range(n) if i not in self.black]
        # valid 长度等于 n - len(blacklist)

    def pick(self) -> int:
        # 随机在 valid 的下标范围内取一个下标
        idx = random.randint(0, len(self.valid) - 1)   # randint 包含两端
        return self.valid[idx]
```

#### 复杂度

- **时间复杂度**  
  - 初始化 `__init__`：需要遍历 `0 … n-1`，所以是 **O(n)**。  
    - 大白话：如果 `n = 1,000,000,000`，我们得检查十亿次才能把合法号码挑出来，显然不可行。  
  - `pick`：只做一次随机数和一次下标访问，**O(1)**。

- **空间复杂度**  
  - 我们保存了所有合法号码，大小为 `n - |blacklist|`，因此是 **O(n)**。  
    - 实际上相当于把整个范围都复制了一遍，内存会炸掉。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于：

1. **初始化时遍历整个 `[0, n-1]` 区间**，当 `n` 很大（最高 10⁹）时不可接受。  
2. **存储所有合法号码** 需要巨大的内存。

我们只需要在 **黑名单的数量** `k = len(blacklist)` 级别上工作。关键观察：

- 设 `m = n - k` 为合法号码的总数。我们只需要在 `[0, m-1]` 这段连续区间内随机取数。  
- 但是这段区间里可能仍然有黑名单的元素。把这些「冲突」的黑名单映射（重定向）到区间 `[m, n-1]` 中的合法号码即可。

**映射过程**（一步步推导）：

1. 把所有 **大于等于 `m` 的黑名单** 放进集合 `big_black`。这些号码本来就不需要映射，因为我们不会在 `[0, m-1]` 里随机到它们。  
2. 对于 **小于 `m` 的黑名单**（记为 `b`），它们会导致冲突，需要被映射。我们在 `[m, n-1]` 里找一个不在 `big_black` 的号码 `w`，把 `b → w` 记录在哈希表 `map` 中。  
3. 随机时：  
   - 先在 `[0, m-1]` 里随机得到 `x`。  
   - 如果 `x` 不在 `map` 中，说明它本身合法，直接返回。  
   - 否则返回 `map[x]`（已经被替换成合法的“大区间”号码）。

这样 **每次 pick 只需要一次随机数**，并且 **初始化只和黑名单长度 `k` 成正比**。

> **类比**：把 `[0, m-1]` 想成「前排座位」，我们希望随机坐在前排。如果前排有座位被「踢」了（黑名单），我们把这些被踢的座位号记在小卡片上，卡片背面写上后排的一个空座位号。坐前排时若抽到卡片，就换到后排对应的座位。

#### 代码（Python）

```python
import random
from typing import List

class Solution:
    def __init__(self, n: int, blacklist: List[int]):
        self.n = n
        self.k = len(blacklist)          # 黑名单长度
        self.m = n - self.k               # 合法号码的总数

        # 步骤 1：把所有大于等于 m 的黑名单放进集合，方便 O(1) 判断
        self.big_black = set(b for b in blacklist if b >= self.m)

        # 步骤 2：为每个小于 m 的黑名单分配一个合法的“大区间”号码
        self.map = {}                     # key: 冲突的前排号码, value: 替代的后排号码
        # 循环找后排的候选号码，从 m 开始向右扫描
        w = self.m                        # 当前候选的后排号码指针
        for b in blacklist:
            if b < self.m:                # 只处理前排的黑名单
                # 找到下一个不在 big_black 中的 w
                while w in self.big_black:
                    w += 1                # 跳过后排的黑名单
                # 此时 w 必然是合法的后排号码
                self.map[b] = w
                w += 1                    # 为下一个冲突准备新的候选

        # 此时 self.map 的大小等于“小于 m 的黑名单数量”，最多为 k

    def pick(self) -> int:
        # 步骤 3：在前排 [0, m-1] 随机取一个号码
        x = random.randint(0, self.m - 1)   # 只调用一次 random
        # 若该号码被映射，则返回映射后的后排号码；否则直接返回
        return self.map.get(x, x)
```

> **关键细节**  
> - `random.randint(a, b)` 包含 `a` 与 `b`，因此区间恰好是 `[0, m-1]`。  
> - `self.map.get(x, x)` 的含义是：如果 `x` 在映射表里，返回对应的值；否则返回 `x` 本身。

#### 复杂度

- **时间复杂度**  
  - 初始化 `__init__`：遍历黑名单两遍（一次构造 `big_black`，一次建立映射），每一步都是 **O(k)**。  
    - 与 `n` 的大小无关，即使 `n = 10⁹` 也只和黑名单长度 `k ≤ 10⁵` 成正比。  
  - `pick`：只做一次随机数、一次哈希表查找，**O(1)**。  
    - 与暴力解相比，`pick` 的复杂度没有变化，但**不需要**在 `pick` 时进行多次随机或循环，最坏情况仍是一次调用。

- **空间复杂度**  
  - 需要保存 `big_black`（最多 `k` 个）和 `map`（最多 `k` 个），因此是 **O(k)**。  
    - 相比暴力解的 **O(n)**，大幅降低内存使用。

---

## 心得

- **核心技巧**：把「大范围」的随机问题压缩到「黑名单长度」的大小，通过**哈希映射**把冲突的编号重定向到合法的编号。  
- **适用场景**  
  1. **随机抽样排除若干元素**（如本题、Random Pick with Weight 等）。  
  2. **离散概率分布的采样**（如把概率区间映射到整数区间）。  
  3. **区间压缩**（把稀疏的合法集合映射到连续的索引空间）。  
- **一句话总结**：**把需要排除的“坏号”映射到“好号”，只在压缩后的连续区间里随机**。

---

## 反思

- **第一反应**：直接把所有合法数字列出来或不停随机直到命中合法数。  
- **最容易踩的坑**  
  - **边界**：`m = n - k` 可能为 0（全部被黑名单覆盖），此时 `pick` 不会被调用（题目保证 `blacklist.length ≤ n-1`）。  
  - **映射冲突**：在构造映射时要确保后排的候选号码不在 `big_black` 中，否则会把黑名单映射到另一个黑名单。  
  - **整数溢出**：`n` 可达 `10⁹`，在 Python 中整数安全，但在某些语言需要注意 32 位整数上限。  
- **下次遇到同类题**：第一步先 **计算合法数量 m = n - |blacklist|**，判断是否可以直接在 `[0, m-1]` 上随机；如果冲突，立即考虑 **哈希映射** 把冲突的编号指向后面的合法编号。这样可以把时间和空间控制在 O(|blacklist|)。