# #519. 随机翻转矩阵 / Random Flip Matrix

> 难度：中等 · 标签：Hash Table、Math、Reservoir Sampling、Randomized · [LeetCode 链接](https://leetcode.com/problems/random-flip-matrix/)

---

## 题目（英文原版）

**Description**

There is an m x n binary grid matrix with all the values set 0 initially. Design an algorithm to randomly pick an index (i, j) where matrix[i][j] == 0 and flips it to 1. All the indices (i, j) where matrix[i][j] == 0 should be equally likely to be returned.
Optimize your algorithm to minimize the number of calls made to the built-in random function of your language and optimize the time and space complexity.
Implement the Solution class:

**Examples**

**Example 1:**

```
Input
["Solution", "flip", "flip", "flip", "reset", "flip"]
[[3, 1], [], [], [], [], []]
Output
[null, [1, 0], [2, 0], [0, 0], null, [2, 0]]

Explanation
Solution solution = new Solution(3, 1);
solution.flip();  // return [1, 0], [0,0], [1,0], and [2,0] should be equally likely to be returned.
solution.flip();  // return [2, 0], Since [1,0] was returned, [2,0] and [0,0]
solution.flip();  // return [0, 0], Based on the previously returned indices, only [0,0] can be returned.
solution.reset(); // All the values are reset to 0 and can be returned.
solution.flip();  // return [2, 0], [0,0], [1,0], and [2,0] should be equally likely to be returned.
```

**Constraints**

- 1 <= m, n <= 104
- There will be at least one free cell for each call to flip.
- At most 1000 calls will be made to flip and reset.

---

## 题目（中文翻译）

**描述**  
给定一个 $m \times n$ 的二进制网格矩阵（binary grid matrix），初始时所有单元格的值均为 $0$。设计一个算法，随机选取一个满足 `matrix[i][j] == 0` 的坐标 $(i, j)$ 并将其值翻转为 $1$。所有当前值为 $0$ 的坐标 $(i, j)$ 被选中的概率必须相等。要求尽量减少对语言内置随机函数的调用次数，并优化时间与空间复杂度。

实现 `Solution` 类，使其能够完成上述功能。

**示例 1**

```text
Input
["Solution", "flip", "flip", "flip", "reset", "flip"]
[[3, 1], [], [], [], [], []]

Output
[null, [1, 0], [2, 0], [0, 0], null, [2, 0]]
```

**解释**  
```java
Solution solution = new Solution(3, 1);
solution.flip();  // 返回 [1, 0]。在第一次调用时，[0,0]、[1,0]、[2,0] 三个坐标被返回的概率相同。
solution.flip();  // 返回 [2, 0]。由于上一次已经返回了 [1,0]，此时仅剩 [0,0] 与 [2,0]，它们被返回的概率相同。
solution.flip();  // 返回 [0, 0]。此时只剩下唯一的未翻转坐标 [0,0]。
solution.reset(); // 所有单元格的值被重置为 0，后续调用均可再次返回任意坐标。
solution.flip();  // 返回 [2, 0]。重新翻转后，[0,0]、[1,0]、[2,0] 再次具有相同的返回概率。
```

**约束条件**  

- $1 \leq m, n \leq 10^4$
- 每次调用 `flip` 时，矩阵中至少存在一个值为 $0$ 的单元格。
- `flip` 和 `reset` 的调用次数总计不超过 $1000$ 次。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把整个矩阵保存下来**，每次 `flip` 时在矩阵里随机挑一个位置，  
如果该位置已经是 `1`（即已经被翻转过），就继续随机，直到找到一个仍为 `0` 的格子，再把它改成 `1` 并返回坐标。  

- **使用的数据结构**：  
  - 二维列表 `grid`，把矩阵本身保存下来。可以把它想象成一本“翻页的字典”，每个格子就是一本书的页码，`0/1` 记录这页是否已经被翻过。  
  - `random.randint(a, b)` 用来产生 `[a, b]` 区间的均匀随机整数，类似于掷一枚公平的骰子。  

- **为什么正确**：  
  - 每一次我们都在所有格子中等概率抽取一个下标；如果抽到的格子已经是 `1`，我们会**重新抽**，直到抽到 `0`。  
  - 只要还有未翻转的格子，这个过程最终一定会找到一个 `0`，并且每个 `0` 被选中的概率相同（因为每一次抽取都是等概率的）。  

- **时间/空间复杂度**（大白话）  
  - **时间**：最坏情况下矩阵几乎全是 `1`，只剩下一个 `0`。这时我们可能要 **不停地抽**（可能抽几千次）才碰到那个唯一的 `0`。所以时间复杂度是 **O(m·n)**，也就是“和矩阵里格子的总数成正比”。  
  - **空间**：我们必须把整个矩阵存下来，需要 **O(m·n)** 的额外空间。  

#### 代码（Python）

```python
import random
from typing import List

class Solution:
    def __init__(self, m: int, n: int):
        self.m, self.n = m, n
        # 用二维列表保存矩阵，全部初始化为 0
        self.grid = [[0] * n for _ in range(m)]

    def flip(self) -> List[int]:
        while True:
            # 在所有格子里随机抽取一个下标
            i = random.randint(0, self.m - 1)
            j = random.randint(0, self.n - 1)
            if self.grid[i][j] == 0:          # 只要是 0 就可以翻转
                self.grid[i][j] = 1           # 标记为已翻转
                return [i, j]                 # 返回坐标
            # 如果抽到的是 1，继续循环重新抽

    def reset(self) -> None:
        # 把矩阵全部恢复为 0
        self.grid = [[0] * self.n for _ in range(self.m)]
```

#### 复杂度  

- **时间复杂度**：`O(m·n)` —— 当矩阵几乎被填满时，需要大量随机抽取才能命中唯一的 0。  
- **空间复杂度**：`O(m·n)` —— 保存整个矩阵需要和格子数一样多的空间。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于每次都要在已经翻转的格子里继续抽**，导致大量“无效抽取”。  
要想做到 **一次抽取就一定命中未翻转的格子**，可以把矩阵 **线性化**（把二维坐标映射成一维下标），并维护一个**只剩下未翻转格子的“虚拟池子”**。

1. **把矩阵拉平成一维**：  
   - 位置 `(i, j)` 对应的编号是 `idx = i * n + j`，范围是 `[0, m·n-1]`。  
   - 想象有一个装满 `m·n` 张卡片的盒子，每张卡片的编号就是格子的编号。  

2. **抽取时只在“剩余卡片”里抽**：  
   - 设当前还有 `k` 张未被抽走的卡片（`k` 初始为 `m·n`），我们在 `[0, k-1]` 之间随机取一个整数 `r`。  
   - 这张卡片对应的真实格子可能已经被 **映射** 到别的编号上（因为之前的抽取会把抽走的卡片换到盒子尾部）。我们用一个哈希表 `map` 记录这种“换位”。  
   - `real = map.get(r, r)`：如果 `r` 没有被映射过，就说明它本身就是未翻转的格子；如果被映射过，就取映射后的编号。  

3. **抽走这张卡片后做“换位”**：  
   - 为了让盒子大小缩小一格（`k → k-1`），把抽走的卡片位置 `r` 用盒子最尾部的卡片 `k-1` 来填补。  
   - 同样需要记录映射：`map[r] = map.get(k-1, k-1)`。这样下一次抽取时，如果再抽到 `r`，会直接得到原来尾部卡片对应的格子。  

4. **reset**：  
   - 只需要把 `map` 清空、`k` 重新设为 `m·n` 即可，时间 O(1)。  

**核心数据结构**：  
- **哈希表（dict）**：把“被抽走的编号”映射到“盒子尾部的编号”。可以把它想象成“字典查词”，键是抽走的卡片，值是用来“补位”的卡片。  
- **整数 `remaining`**：记录当前还有多少未翻转的格子。  

这样，每一次 `flip` 只需要一次随机数、几次哈希表查找和写入，**时间是 O(1)**，而空间只保存已经抽走的映射，最多 `O(min(m·n, 1000))`（因为题目限制最多 1000 次 `flip`）。

#### 代码（Python）

```python
import random
from typing import List

class Solution:
    def __init__(self, m: int, n: int):
        """
        m 行 n 列的矩阵，全部初始化为 0。
        """
        self.m, self.n = m, n
        self.total = m * n               # 矩阵总格子数
        self.reset()                     # 初始化内部状态

    def flip(self) -> List[int]:
        """
        随机返回一个仍为 0 的坐标，并把它翻成 1。
        """
        # 目前还有多少未被翻转的格子
        self.remaining -= 1
        # 在 [0, remaining] 区间随机抽一个下标
        rand_idx = random.randint(0, self.remaining)

        # 通过映射得到真实的线性编号
        # 如果 rand_idx 已经被映射过，就取映射后的值；否则它本身就是未翻转的格子
        real_idx = self.mapping.get(rand_idx, rand_idx)

        # 为了把抽走的卡片位置“填满”，把盒子最尾部的卡片搬到这里
        # 取出尾部卡片的真实编号（可能已经被映射过）
        tail_idx = self.mapping.get(self.remaining, self.remaining)
        # 把尾部卡片映射到抽走的位置
        self.mapping[rand_idx] = tail_idx

        # 将线性编号转回二维坐标
        row = real_idx // self.n
        col = real_idx % self.n
        return [row, col]

    def reset(self) -> None:
        """
        把所有格子恢复为 0。
        只需要清空映射表并把剩余格子数恢复到初始值。
        """
        self.mapping = {}               # 哈希表，键: 被抽走的下标，值: 用来补位的下标
        self.remaining = self.total     # 当前还有多少未翻转的格子
```

#### 复杂度  

- **时间复杂度**：`O(1)` —— 每次 `flip` 只进行一次随机数生成和常数次哈希表操作。相比暴力解的 `O(m·n)`，速度提升巨大。  
- **空间复杂度**：`O(k)`，其中 `k` 为已经执行的 `flip` 次数（最多 1000），因为只需要存储已经抽走的映射。与矩阵大小无关，远比 `O(m·n)` 节省空间。  

---

## 心得  

- **核心技巧**：**把二维矩阵线性化 + 哈希表模拟“抽走后压缩池子”**，这是一种 **“随机抽样的 O(1) 实现”**，常用于需要在动态集合中均匀抽取元素的场景。  
- **适用的题型**（类似思路）  
  1. **随机取样（Reservoir Sampling）**：在流式数据中均匀抽取固定数量的样本。  
  2. **Shuffle an Array**（LeetCode 384）：一次遍历实现数组随机置换。  
  3. **Random Pick with Weight**（LeetCode 528）：带权重的随机抽取。  
- **一句话总结解题钥匙**：**“把所有候选元素压缩到一个可直接抽取的连续区间，用哈希表记录被抽走的‘洞’的补位”。**  

---

## 反思  

- **第一反应**：直接保存整个矩阵，循环随机抽，直到命中未翻转的格子。  
- **最容易踩的坑**  
  - **时间浪费**：当矩阵几乎被填满时，暴力抽取会大量重复抽到已经是 `1` 的位置，导致超时。  
  - **下标映射错误**：把二维坐标映射到一维时，`idx = i * n + j` 必须使用行数 `n`（列数），否则会出现错位。  
  - **reset 时忘记清空映射表**，会导致后续 `flip` 仍然使用旧的映射，产生错误结果。  
- **下次遇到同类题**：第一步先思考 **“是否可以把集合压缩成一个连续的编号区间，并用哈希表记录被移除的元素的‘补位’”**，如果能，就可以直接套用上述“一次抽取 O(1)”的方案。