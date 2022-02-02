# #1655. **分配重复整数** / Distribute Repeating Integers

> 难度：困难 · 标签：Array、Dynamic Programming、Backtracking、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/distribute-repeating-integers/)

---

## 题目（英文原版）

**Description**

You are given an array of n integers, nums, where there are at most 50 unique values in the array. You are also given an array of m customer order quantities, quantity, where quantity[i] is the amount of integers the ith customer ordered. Determine if it is possible to distribute nums such that:
Return true if it is possible to distribute nums according to the above conditions.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4], quantity = [2]
Output: false
Explanation: The 0th customer cannot be given two different integers.
```

**Example 2:**

```
Input: nums = [1,2,3,3], quantity = [2]
Output: true
Explanation: The 0th customer is given [3,3]. The integers [1,2] are not used.
```

**Example 3:**

```
Input: nums = [1,1,2,2], quantity = [2,2]
Output: true
Explanation: The 0th customer is given [1,1], and the 1st customer is given [2,2].
```

**Constraints**

- n == nums.length
- 1 <= n <= 105
- 1 <= nums[i] <= 1000
- m == quantity.length
- 1 <= m <= 10
- 1 <= quantity[i] <= 105
- There are at most 50 unique values in nums.

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`，其中至多包含 50 种不同的数值。再给定一个长度为 `m` 的客户订单数量数组 `quantity`，其中 `quantity[i]` 表示第 `i` 位客户需要的整数个数。请判断是否可以对 `nums` 进行分配，使得：

- 每位客户获得的整数总数恰等于其对应的 `quantity[i]`；
- 同一位客户获得的所有整数必须是相同的数值（即只能来自 `nums` 中的同一个唯一值）；
- 同一个整数的不同副本可以分配给不同的客户，但同一位客户不能同时获得不同的整数。

如果能够满足上述条件则返回 `true`，否则返回 `false`。

---

### 示例

**示例 1**  
**输入**: `nums = [1,2,3,4]`, `quantity = [2]`  
**输出**: `false`  
**解释**: 第 0 位客户需要两个整数，但 `nums` 中没有任意一种整数出现两次，无法满足“同一客户只能得到相同整数”的要求。

**示例 2**  
**输入**: `nums = [1,2,3,3]`, `quantity = [2]`  
**输出**: `true`  
**解释**: 第 0 位客户被分配 `[3,3]`。整数 `[1,2]` 未被使用。

**示例 3**  
**输入**: `nums = [1,1,2,2]`, `quantity = [2,2]`  
**输出**: `true`  
**解释**: 第 0 位客户得到 `[1,1]`，第 1 位客户得到 `[2,2]`。

---

### 约束条件

- `n == nums.length`
- `1 <= n <= 10^5`
- `1 <= nums[i] <= 1000`
- `m == quantity.length`
- `1 <= m <= 10`
- `1 <= quantity[i] <= 10^5`
- `nums` 中至多出现 50 种唯一数值

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举每个顾客到底拿哪一种整数**，然后检查能否满足他们的需求。  
可以把 `nums` 里相同的数看成一种“商品”，比如 `3` 出现了 5 次，就相当于有 5 件相同的商品。  
每个顾客只能拿同一种商品，而且必须拿到他要的数量 `quantity[i]`。

实现思路：

1. 先把 `nums` 统计出每个整数出现的次数，得到一个频率数组 `freq`（长度 ≤ 50）。
2. 对每个顾客 `i`，遍历所有商品种类 `j`，尝试把 `quantity[i]` 件商品 `j` 分配给他。  
   - 如果 `freq[j]` 足够大，就把 `freq[j]` 减掉 `quantity[i]`，递归处理下一个顾客。
   - 递归结束后记得把 `freq[j]` 加回来（回溯），因为后面的分配仍然可能使用这件商品。
3. 如果所有顾客都成功分配，返回 `True`；否则返回 `False`。

**为什么正确**：递归枚举了所有可能的分配方案，只要有一种方案满足所有顾客的需求，就会在搜索树的某个叶子节点返回 `True`。

**时间/空间复杂度**（大白话版）：

- 假设有 `k` 种不同的整数（`k ≤ 50`），`m` 个顾客（`m ≤ 10`）。  
- 每个顾客最多可以尝试 `k` 种商品，所以最坏情况下的搜索树节点数是 `k^m`。  
- 对每个节点我们只做常数次加减操作，时间复杂度约为 **O(k^m)**，这在最坏情况下是天文数字（比如 50^10），根本不可接受。  
- 递归栈的深度最多 `m`，所以空间复杂度是 **O(m)**（递归调用的栈空间）+ 用来保存 `freq` 的 **O(k)**。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def canDistribute_bruteforce(nums: List[int], quantity: List[int]) -> bool:
    # 统计每个整数出现的次数，freq[i] 表示第 i 种商品的剩余数量
    freq = list(Counter(nums).values())
    m = len(quantity)

    # 为了加速，先把大订单排在前面，先消耗大的需求
    quantity.sort(reverse=True)

    def backtrack(idx: int) -> bool:
        """尝试给第 idx 位顾客分配商品"""
        if idx == m:          # 所有顾客都已分配完
            return True
        need = quantity[idx]  # 当前顾客需要的数量
        for i in range(len(freq)):
            if freq[i] >= need:          # 商品 i 足够满足当前顾客
                freq[i] -= need          # 分配
                if backtrack(idx + 1):   # 递归处理下一个顾客
                    return True
                freq[i] += need          # 回溯，撤销分配
        return False                     # 没有任何商品可以满足当前顾客

    return backtrack(0)
```

#### 复杂度

- **时间复杂度**：`O(k^m)`（k 为不同整数种类数，m 为顾客数），在最坏情况下几乎不可接受。  
  > 大白话：如果有 50 种商品，10 位顾客，理论上要尝试 50 的 10 次方（≈ 9.8×10¹⁶）种组合，根本算不完。
- **空间复杂度**：`O(k + m)`，主要是保存频率数组和递归栈。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复遍历相同的子问题**：同样的顾客集合与剩余商品频率会被多次计算。  
我们需要把“已经分配了哪些顾客”这个信息抽象出来，**用记忆化搜索（DP）** 来避免重复工作。

关键观察：

1. **每个顾客只会拿同一种整数**，所以一个整数（对应一个频率 `f`) 可以一次性满足若干顾客的全部需求。  
2. 顾客的需求集合可以用 **位掩码（bitmask）** 表示。  
   - 共有 `m ≤ 10` 位，`mask` 的第 `i` 位为 1 表示第 `i` 位顾客已经被满足。  
   - `mask = 0` 表示没有顾客被满足，`mask = (1<<m)-1` 表示全部满足。
3. 对每一种整数的频率 `f`，我们可以尝试把它分配给 **任意子集** 的顾客，只要这些顾客的需求总和 `≤ f`。  
   - 例如 `f = 5`，顾客需求 `[2,3,1]`，我们可以一次性满足需求 `2+3=5` 的顾客 `{0,1}`，或满足 `2+1=3` 的顾客 `{0,2}`，等等。
4. 动态规划的状态是 `dp[mask]`：**是否可以仅使用已经遍历过的整数来满足 `mask` 所表示的顾客集合**。  
   - 初始 `dp[0] = True`（不满足任何人是显然可行的）。  
   - 对每个频率 `f`，遍历所有 `mask`，尝试把 `mask` 扩展为 `mask | sub`，其中 `sub` 是 `mask` 的 **子集的补集**（即还未满足的顾客）中**需求总和 ≤ f** 的子集。  
   - 如果 `dp[mask]` 为真且 `sub` 合法，则把 `dp[mask | sub]` 设为真。

因为 `m ≤ 10`，所有可能的 `mask` 数量只有 `2^m ≤ 1024`，遍历所有子集的代价也在可接受范围。

**实现细节**：

- 先把 `quantity` 按任意顺序保存，随后预计算每个 `mask` 对应的需求总和 `need[mask]`，这样判断子集是否合法只需要 O(1)。
- 对每个频率 `f`，遍历 `mask`（从大到小遍历可以防止同一次频率在同一轮中被多次使用），对未满足的顾客子集 `sub`（子集枚举技巧 `sub = (sub-1) & remain`）进行尝试。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def canDistribute(nums: List[int], quantity: List[int]) -> bool:
    # 1. 统计每个整数出现的次数（频率列表）
    freq = list(Counter(nums).values())          # 长度 ≤ 50
    m = len(quantity)                             # 顾客数 ≤ 10

    # 2. 预计算每个 mask（顾客子集）对应的需求总和
    #    mask 的第 i 位为 1 表示第 i 位顾客已被包含在该子集
    need = [0] * (1 << m)
    for mask in range(1, 1 << m):
        # 取最低位的 1，递推求和
        lsb = mask & -mask                         # 低位 1
        idx = (lsb.bit_length() - 1)               # 对应的顾客编号
        need[mask] = need[mask ^ lsb] + quantity[idx]

    # 3. DP 数组，dp[mask] 表示“使用已经遍历过的部分整数，能否满足 mask 表示的顾客集合”
    dp = [False] * (1 << m)
    dp[0] = True                                   # 空集合一定可以

    # 4. 遍历每一种整数的频率
    for f in freq:
        # 从大到小遍历 mask，防止同一个频率在本轮被使用两次
        for mask in range((1 << m) - 1, -1, -1):
            if not dp[mask]:
                continue                         # 当前 mask 不可达，跳过
            # remain 表示还没有被满足的顾客集合
            remain = ((1 << m) - 1) ^ mask
            sub = remain
            # 枚举 remain 的所有子集 sub
            while sub:
                if need[sub] <= f:                # 这个子集的总需求 ≤ 当前频率
                    dp[mask | sub] = True        # 把子集加入已满足集合
                sub = (sub - 1) & remain          # 下一个子集

    # 5. 检查是否所有顾客都能被满足
    return dp[(1 << m) - 1]
```

#### 复杂度

- **时间复杂度**：`O(k * 2^m * 2^{m})` 的表面写法其实可以更紧凑。  
  - `k ≤ 50`（不同整数种类数）。  
  - `2^m ≤ 1024`（所有 mask）。  
  - 对每个 `mask` 我们遍历它的 **剩余子集**，子集枚举的总次数在一次遍历中恰好是 `3^m`，但因为 `m ≤ 10`，`3^10 = 59049`，仍然很小。  
  - 实际运行时间约为 `O(k * 3^m)`，在最坏情况下约 `50 * 59049 ≈ 3·10⁶` 次操作，毫秒级即可完成。  
  > 大白话：我们最多检查几千种“已经满足了哪些顾客”的情况，每种情况再检查几百个子集合，总体不超过几百万次，计算机跑得飞快。
- **空间复杂度**：`O(2^m)` 用来存 `dp` 和 `need` 两个数组，最多 1024 个布尔值和整数，几乎可以忽略不计。

---

## 心得

- **核心技巧**：**位掩码 + 子集枚举的 DP**。把“哪些顾客已经被满足”抽象成二进制的状态，用 DP 记忆化避免重复搜索。
- **适用的题型**  
  1. “分配/匹配”类问题，且对象数量 ≤ 10（可以用位掩码），例如 LeetCode 1723 *Find Minimum Time to Finish All Jobs*。  
  2. “子集划分”或“背包”类问题，需要在有限的资源集合中挑选子集满足需求，例如 698 *Partition to K Equal Sum Subsets*（用 DP + 位掩码）。  
  3. “多重背包”或“资源分配”问题，资源种类不多但需求多，例如 1125 *Smallest Sufficient Team*（使用位掩码 DP）。
- **一句话总结解题钥匙**：  
  > “把‘已经满足的顾客’编码成二进制状态，用 DP 逐个资源扩展状态，子集枚举帮你一次性决定本轮资源要满足哪些顾客”。

---

## 反思

- **第一反应**：看到“每个顾客只能拿相同整数”，立刻想到把 `nums` 按值分组，然后把每个顾客绑定到某个分组——于是想到回溯/暴力搜索。
- **最容易踩的坑**  
  1. **子集枚举顺序**：如果在同一次频率遍历时从小到大更新 `dp`，会导致同一个频率被重复使用，产生错误的“多次分配”。必须逆序遍历或使用临时数组。  
  2. **需求总和的快速判断**：每次枚举子集都要检查需求是否 ≤ 当前频率，直接累加会导致 `O(2^m * m)` 的额外开销。预先计算 `need[mask]` 可以把判断压到 O(1)。  
  3. **顾客数量的上限**：如果不注意 `m ≤ 10`，会误以为位掩码可以无限使用，导致内存/时间爆炸。  
- **下次类似题的第一步**：  
  > “先把‘状态’抽象成二进制掩码”，检查是否可以用 DP 逐个资源/元素推进状态，这往往能把指数级的回溯压到可接受的 2^m 规模。