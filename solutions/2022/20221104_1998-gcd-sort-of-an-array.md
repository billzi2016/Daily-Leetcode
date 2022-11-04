# #1998. 数组的 GCD 排序 / GCD Sort of an Array

> 难度：困难 · 标签：Array、Math、Union Find、Sorting、Number Theory · [LeetCode 链接](https://leetcode.com/problems/gcd-sort-of-an-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums, and you can perform the following operation any number of times on nums:
Return true if it is possible to sort nums in non-decreasing order using the above swap method, or false otherwise.

**Examples**

**Example 1:**

```
Input: nums = [7,21,3]
Output: true
Explanation: We can sort [7,21,3] by performing the following operations:
- Swap 7 and 21 because gcd(7,21) = 7. nums = [21,7,3]
- Swap 21 and 3 because gcd(21,3) = 3. nums = [3,7,21]
```

**Example 2:**

```
Input: nums = [5,2,6,2]
Output: false
Explanation: It is impossible to sort the array because 5 cannot be swapped with any other element.
```

**Example 3:**

```
Input: nums = [10,5,9,3,15]
Output: true
We can sort [10,5,9,3,15] by performing the following operations:
- Swap 10 and 15 because gcd(10,15) = 5. nums = [15,5,9,3,10]
- Swap 15 and 3 because gcd(15,3) = 3. nums = [3,5,9,15,10]
- Swap 10 and 15 because gcd(10,15) = 5. nums = [3,5,9,10,15]
```

**Constraints**

- 1 <= nums.length <= 3 * 104
- 2 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个整数数组 `nums`，你可以对 `nums` 任意次执行以下操作：  
如果两个元素的最大公约数（gcd）大于 1，则可以交换这两个元素的位置。

请判断是否可以仅通过上述交换方式将 `nums` 排序成非递减顺序（non-decreasing order），如果可以返回 `true`，否则返回 `false`。

**示例 1**  
**输入**: `nums = [7,21,3]`  
**输出**: `true`  
**解释**: 我们可以按以下步骤排序 `[7,21,3]`：  
- 交换 7 与 21，因为 `gcd(7,21) = 7`。`nums = [21,7,3]`  
- 交换 21 与 3，因为 `gcd(21,3) = 3`。`nums = [3,7,21]`

**示例 2**  
**输入**: `nums = [5,2,6,2]`  
**输出**: `false`  
**解释**: 无法完成排序，因为 5 与任意其他元素的 `gcd` 都不大于 1，不能进行交换。

**示例 3**  
**输入**: `nums = [10,5,9,3,15]`  
**输出**: `true`  
**解释**: 我们可以按以下步骤排序 `[10,5,9,3,15]`：  
- 交换 10 与 15，因为 `gcd(10,15) = 5`。`nums = [15,5,9,3,10]`  
- 交换 15 与 3，因为 `gcd(15,3) = 3`。`nums = [3,5,9,15,10]`  
- 再次交换 10 与 15，因为 `gcd(10,15) = 5`。`nums = [3,5,9,10,15]`

**约束条件**  
- `1 <= nums.length <= 3 * 10^4`  
- `2 <= nums[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把所有可以交换的操作都列举出来**，然后一直尝试交换，看看能否把数组排好序。  
具体做法可以是：

1. **遍历数组的每一对位置** `(i, j)`，如果 `gcd(nums[i], nums[j]) > 1`（即两数的最大公约数大于 1），就认为这对元素可以直接交换。  
2. 把所有满足条件的交换当成**无向图的边**，节点是数组下标。  
3. 对这个图做**深度优先搜索 / 广度优先搜索**，得到所有可以通过若干次合法交换到达的下标集合（也就是连通分量）。  
4. 对每个连通分量，尝试把里面的元素按任意顺序重新排列，看能否得到整体的非递减序列。  

> **生活化类比**：把每个下标想成城市，`gcd>1` 的两座城市之间有一条“高速路”。只要能通过高速路走通（即在同一个连通块），我们就可以把这两座城市的货物（数组元素）随意调换。

**为什么这个方法能得到正确答案**  
因为题目允许**任意次数**的合法交换，而合法交换的本质是「在同一个连通块的任意两个位置」可以互换顺序。因此只要我们把所有能到达的下标分到同一个集合，就等价于“这些位置的元素可以随意重排”。只要在每个集合内部把元素排成目标序列（排序后的数组对应位置），整个数组就能变成有序。

**为什么会超时**  
- 步骤 1 需要检查所有 `i < j`，时间复杂度是 `O(n²)`，而 `n` 最多可达 `3·10⁴`，`n² ≈ 9·10⁸`，根本跑不完。  
- 即使把遍历改成只对**相邻**下标检查（因为交换可以跨越），仍然需要不断重复搜索，最坏情况下仍然是指数级的“尝试所有交换序列”。  

**复杂度**  

| 项目 | 复杂度 | 含义解释 |
|------|--------|----------|
| 时间 | **O(n²)** | 想象有 `n` 个人要两两握手，手握的次数是 `n·(n-1)/2`，这就是 `n²` 级别。对 `3·10⁴` 人来说，手握次数已经超过十亿，计算机吃不消。 |
| 空间 | **O(n)** | 只需要存放访问标记或连通块信息，和数组大小成正比。 |

> **结论**：暴力思路太慢，必须利用数学结构（**最大公约数**）来把连通块快速构造出来。

---

### 2. 最优解  

#### 思路  

从暴力解我们已经知道：**只要两个下标在同一个连通块里，它们的元素就可以随意换位**。  
所以核心任务是**快速找出这些连通块**。  

> **瓶颈**：直接检查每对 `(i, j)` 的 `gcd`，仍然是 `O(n²)`。  
> **突破口**：两个数的 `gcd>1` 当且仅当它们**共享至少一个质因子**（大于 1 的素数）。  

于是我们把“共享质因子”转化为**图的连通性**：

1. **质因子 → 纽带**  
   - 把每个 **质因子** 当成一个“虚拟节点”。  
   - 如果数组下标 `i` 的数 `nums[i]` 含有质因子 `p`，就在 `i` 与虚拟节点 `p` 之间连一条边。  

2. **并查集（Union‑Find）**  
   - 并查集是一种**快速合并集合**的数据结构，常用来维护无向图的连通块。  
   - 当我们遍历每个元素的所有质因子时，**把该下标与所有出现过的相同质因子所在的下标合并**。  
   - 最终，同一并查集根的下标们就是可以互相交换的“同胞”。  

3. **检查能否排序**  
   - 先得到 **目标数组** `sorted_nums = sorted(nums)`。  
   - 对每个下标 `i`，如果 `nums[i]` 在并查集中所在的集合里，**它必须能够搬到目标位置 `i`**。也就是说，`sorted_nums[i]` 必须出现在同一个集合里。  
   - 实际实现时可以把每个集合的所有元素收集到一个列表或计数器中，再与目标集合的元素比较是否相同（多重集合相等）。  

#### 关键技巧解释  

| 技巧 | 零基础解释 |
|------|------------|
| **质因子** | 把一个数拆成若干个“最小的不可再拆的因子”。例如 `12 = 2·2·3`，质因子是 `2`、`3`。 |
| **并查集（Union‑Find）** | 想象每个人手里拿着一张“同盟卡”。最开始每个人单独一组。只要两个人之间有“共同的质因子”，我们就把他们的卡合并成同一张卡，表示他们已经是同盟。卡的根（最上层的卡）就是这个同盟的代表。合并和查询都非常快（几乎是 O(1)）。 |
| **计数器（Counter）** | 类似“超市收银台的商品计数”。把同一个集合里出现的所有数字记下来，看看与目标集合里应该出现的数字是否一模一样。 |

#### 代码（Python）

```python
# --------------------------------------------------------------
#  GCD Sort of an Array  ——  最优解（并查集 + 质因子分解）
# --------------------------------------------------------------
import sys
from collections import defaultdict, Counter
sys.setrecursionlimit(1 << 25)

class UnionFind:
    """ 并查集实现，支持路径压缩和按秩合并 """
    def __init__(self, n: int):
        self.parent = list(range(n))   # 每个节点的父亲，一开始指向自己
        self.rank   = [0] * n          # 按秩合并时的高度近似

    def find(self, x: int) -> int:
        """ 找根节点，顺路压平路径 """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # 递归压平
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """ 把 x、y 所在的集合合并 """
        fx, fy = self.find(x), self.find(y)
        if fx == fy:            # 已经同根，无需合并
            return
        # 按秩合并：把矮的挂到高的下面
        if self.rank[fx] < self.rank[fy]:
            self.parent[fx] = fy
        elif self.rank[fx] > self.rank[fy]:
            self.parent[fy] = fx
        else:
            self.parent[fy] = fx
            self.rank[fx] += 1

# --------------------------------------------------------------
def smallest_prime_factors(limit: int) -> list:
    """
    线性筛（最小质因子表），返回 size=limit+1 的列表 spf，
    其中 spf[x] 为 x 的最小质因子（x>=2）。
    """
    spf = [0] * (limit + 1)
    primes = []
    for i in range(2, limit + 1):
        if spf[i] == 0:           # i 是质数
            spf[i] = i
            primes.append(i)
        for p in primes:
            if p > spf[i] or i * p > limit:
                break
            spf[i * p] = p
    return spf

def get_prime_factors(x: int, spf: list) -> set:
    """ 利用最小质因子表快速分解出 x 的所有不同质因子 """
    factors = set()
    while x > 1:
        p = spf[x]
        factors.add(p)
        while x % p == 0:
            x //= p
    return factors

# --------------------------------------------------------------
def gcdSort(nums: list) -> bool:
    n = len(nums)
    max_val = max(nums)

    # 1️⃣ 预处理：最小质因子表（只需要到 max(nums) 即可）
    spf = smallest_prime_factors(max_val)

    # 2️⃣ 并查集：把拥有相同质因子的下标连在一起
    uf = UnionFind(n)
    prime_to_index = dict()          # 质因子 -> 第一次出现的下标

    for idx, val in enumerate(nums):
        primes = get_prime_factors(val, spf)   # 该数的所有不同质因子
        for p in primes:
            if p in prime_to_index:
                # 已经有其它位置出现了相同的质因子，合并它们所在的集合
                uf.union(idx, prime_to_index[p])
            else:
                prime_to_index[p] = idx        # 记录第一次出现的下标

    # 3️⃣ 收集每个连通块的元素（使用 Counter 计数多重集合）
    comp_elements = defaultdict(Counter)   # root -> Counter{value:cnt}
    for idx, val in enumerate(nums):
        root = uf.find(idx)
        comp_elements[root][val] += 1

    # 4️⃣ 与排好序的目标数组逐位比较
    sorted_nums = sorted(nums)
    for idx, target in enumerate(sorted_nums):
        root = uf.find(idx)
        if comp_elements[root][target] == 0:
            # 目标位置的数不在同一个连通块里，无法搬进来
            return False
        # 把已经匹配的一个 target “用掉”
        comp_elements[root][target] -= 1

    return True

# --------------------------------------------------------------
# 示例
if __name__ == "__main__":
    print(gcdSort([7, 21, 3]))           # True
    print(gcdSort([5, 2, 6, 2]))        # False
    print(gcdSort([10, 5, 9, 3, 15]))   # True
```

> **代码要点注释**  
> - `smallest_prime_factors` 用线性筛一次性得到所有数的**最小质因子**，后面分解质因子只需 O(log value)。  
> - `prime_to_index` 把同一个质因子出现的下标“拉进同一组”。  
> - `comp_elements` 用 `Counter` 保存每个连通块内部的**多重集合**，这样在与排序后数组对比时，只需要检查目标值是否还有剩余即可。

#### 复杂度  

| 项目 | 复杂度 | 含义解释 |
|------|--------|----------|
| 时间 | **O(n · log M)**（`M = max(nums)`） | 对每个元素我们只遍历它的**不同质因子**，一个数的质因子个数 ≤ log₂M（比如 10⁵ 的质因子最多 6 个），所以整体近似线性 `n`。加上线性筛 `O(M)`，而 `M ≤ 10⁵`，整体在 10⁵ 级别，远快于暴力的 `n²`。 |
| 空间 | **O(n + M)** | 并查集需要 `O(n)`，最小质因子表需要 `O(M)`（`M ≤ 10⁵`），额外的哈希表/计数器同样是线性大小。 |

> 与暴力解对比：时间从 `O(n²)` 降到了 **近线性**，在最大输入下可以在毫秒级完成。

---

## 心得  

- **核心技巧**：把 “`gcd(a, b) > 1` ⇔ 两数共享质因子” 用 **并查集** 抽象为 “同一个连通块的元素可以随意换位”。  
- **适用的题型**  
  1. **GCD Swaps** 系列（如本题、LeetCode 1657）  
  2. **基于因子/质数的连通性**（如 “Prime Graph”）  
  3. **只要满足某种共同属性就可以互换** 的问题（例如 “相同字母可交换的字符串”）  
- **一句话总结解题钥匙**：  
  > “把 `gcd>1` 看成共享质因子，利用并查集把拥有相同质因子的下标聚在一起，随后检查每个连通块内部的元素是否能对应到目标位置即可。”

---

## 反思  

- **第一反应**：看到“可以交换的条件是 `gcd>1`”，立刻想到**构图**，但最自然的做法是两两检查 `gcd`，于是掉进了 `O(n²)` 的陷阱。  
- **最容易踩的坑**  
  1. **忘记去重质因子**：如果在分解时把同一个质因子计入多次，会导致不必要的重复合并，虽然不会破坏正确性，却增加时间。  
  2. **边界条件**：`nums` 中可能出现相同的数，计数器必须是 **多重集合**（`Counter`），而不是普通集合，否则会误判。  
  3. **质因子上界**：直接对每个数做 `O(sqrt(val))` 的暴力因子分解在最坏情况下仍是 `O(n·sqrt(M))`，不够快。使用 **最小质因子表** 可以把因子分解降到近 `O(log M)`。  
- **下次遇到同类题**：  
  1. **先抽象出“共享属性”**（本题是共享质因子）。  
  2. **用并查集快速合并拥有相同属性的下标**。  
  3. **比较每个连通块内部的元素与目标状态**，即可判断可行性。