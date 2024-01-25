# #2561. 水果重新排列 / Rearranging Fruits

> 难度：困难 · 标签：Array、Hash Table、Greedy、Sort · [LeetCode 链接](https://leetcode.com/problems/rearranging-fruits/)

---

## 题目（英文原版）

**Description**

You have two fruit baskets containing n fruits each. You are given two 0-indexed integer arrays basket1 and basket2 representing the cost of fruit in each basket. You want to make both baskets equal. To do so, you can use the following operation as many times as you want:
Two baskets are considered equal if sorting them according to the fruit cost makes them exactly the same baskets.
Return the minimum cost to make both the baskets equal or -1 if impossible.

**Examples**

**Example 1:**

```
Input: basket1 = [4,2,2,2], basket2 = [1,4,1,2]
Output: 1
Explanation: Swap index 1 of basket1 with index 0 of basket2, which has cost 1. Now basket1 = [4,1,2,2] and basket2 = [2,4,1,2]. Rearranging both the arrays makes them equal.
```

**Example 2:**

```
Input: basket1 = [2,3,4,1], basket2 = [3,2,5,1]
Output: -1
Explanation: It can be shown that it is impossible to make both the baskets equal.
```

**Constraints**

- basket1.length == basket2.length
- 1 <= basket1.length <= 105
- 1 <= basket1[i], basket2[i] <= 109

---

## 题目（中文翻译）

你有两个装有 **n** 个水果的水果篮子。给定两个 **0** 索引整数数组（array）`basket1` 和 `basket2`，分别表示每个水果的成本（cost）。你希望让两个篮子相等。为此，你可以无限次使用以下操作：

*（题目原文未给出具体操作细节，通常是交换两个篮子中任意位置的水果）*

两个篮子在 **排序后**（按照水果的成本）完全相同，即视为相等。

返回使两个篮子相等的最小成本，如果无法实现则返回 **-1**。

### 示例

**示例 1**

```text
Input: basket1 = [4,2,2,2], basket2 = [1,4,1,2]
Output: 1
Explanation: 交换 `basket1` 中下标为 1 的水果与 `basket2` 中下标为 0 的水果，交换成本为 1。此时 `basket1 = [4,1,2,2]`，`basket2 = [2,4,1,2]`。对两个数组分别排序后它们相等。
```

**示例 2**

```text
Input: basket1 = [2,3,4,1], basket2 = [3,2,5,1]
Output: -1
Explanation: 可以证明无法使两个篮子相等。
```

### 约束条件

- `basket1.length == basket2.length`
- `1 <= basket1.length <= 10^5`
- `1 <= basket1[i], basket2[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**穷举所有可能的交换**，把篮子 1 里任意一个水果和篮子 2 里任意一个水果交换一次，然后继续递归地尝试后面的交换，直到两篮子的水果集合（即排序后）完全相同。  

- **使用的数据结构**：我们可以把两篮子的水果放进两个列表 `list1`、`list2`，每次交换就把对应下标的元素互换。  
- **为什么能得到答案**：因为我们尝试了**所有**可能的交换序列，必然会包含最优的那条路径。  
- **复杂度分析（大白话）**：  
  - 假设篮子里有 `n` 个水果。第一次可以选 `n × n` 种交换方式，第二次又是 `(n-1) × (n-1)`，依此类推。总的可能数大约是 `(n²)!`，这远远超过了计算机能处理的范围。  
  - 用大 O 记号描述的话，时间复杂度是 **指数级**（`O(2^n)` 或更高），空间上只需要保存递归栈，大约 `O(n)`。

显然，这种“暴力枚举”在 `n ≤ 10⁵` 的约束下根本不可行，只能作为思考的起点。

#### 代码（Python）

```python
def brute_force(b1, b2):
    """
    只作为概念演示，实际运行会在 n>10 时爆炸。
    """
    n = len(b1)

    # 判断两篮子是否已经相同（忽略顺序）
    def equal(a, c):
        return sorted(a) == sorted(c)

    # 递归尝试所有交换
    def dfs(i, cur_cost):
        if equal(b1, b2):
            return cur_cost          # 找到一种可行方案
        if i == n * n:               # 为了防止无限递归，这里随便设个上限
            return float('inf')
        best = float('inf')
        for x in range(n):
            for y in range(n):
                # 交换后产生的费用是两水果成本的较小值
                cost = min(b1[x], b2[y])
                b1[x], b2[y] = b2[y], b1[x]        # 交换
                best = min(best, dfs(i + 1, cur_cost + cost))
                b1[x], b2[y] = b2[y], b1[x]        # 恢复现场
        return best

    ans = dfs(0, 0)
    return -1 if ans == float('inf') else ans
```

> **注意**：上述代码仅用于说明“暴力思路”，实际运行会因指数级的递归深度而在很小的 `n`（比如 5）就超时或栈溢出。

#### 复杂度  

- **时间复杂度**：`O( (n²)! )`（指数级）——每一次都要尝试 `n²` 种交换，层层展开。  
- **空间复杂度**：`O(n)`——递归栈最多保存 `n` 层（最坏情况下每次只交换一个元素）。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到**瓶颈**在于每一次都要枚举所有可能的交换。其实我们不需要关心**交换的顺序**，只要知道最终每种水果在两篮子中的出现次数是否匹配即可。

1. **统计频次**  
   - 用两个哈希表（字典）记录 `basket1`、`basket2` 中每个成本出现的次数。  
   - 哈希表就像**查字典**，键是水果的成本，值是出现的次数。

2. **判断可行性**  
   - 对于每一种成本 `v`，把两篮子里的出现次数相加。如果是奇数，说明无论怎么交换，都不可能让两篮子拥有相同的 `v` 数量，因为交换只能成对调换。此时直接返回 `-1`。

3. **找出“多余的”水果**  
   - 对于每个成本 `v`，如果 `basket1` 中出现次数比 `basket2` 多，则多出的 `cnt = (freq1[v] - freq2[v]) / 2` 个 `v` 必须被换走（因为每次换走两个相同成本的水果可以让两边均衡）。  
   - 把这些多余的水果收集到一个列表 `excess`，**只保留一半**（因为另一半会在另一篮子里出现），这样列表长度等于实际需要进行的交换次数。

4. **使用全局最小元素降低费用**  
   - 设 `global_min` 为两篮子里出现的最小成本。  
   - 交换一次的直接费用是 `min(a, b)`（把成本较小的水果当作“搬运费”），但我们可以**两次中转**：先把较大的水果换成 `global_min`（费用 `global_min`），再把 `global_min` 换成另一边需要的水果，合计费用 `2 * global_min`。  
   - 因此，对于每个需要换出的水果 `x`，实际最小费用是 `min(x, 2 * global_min)`。  

5. **贪心求和**  
   - 把 `excess` 按升序排列（从小到大），对每个元素累加上一步算出的最小费用。这样就得到全局最小的总费用。

**关键点**：  
- 只需要关心**哪些水果是多余的**，不必模拟每一次具体的交换。  
- 使用**全局最小元素**做中转可以把一次高成本交换“拆成两次低成本”，从而进一步降低费用。  

下面用文字把整个过程串起来：

> ① 统计每种成本的出现次数 → ② 检查每种成本的总次数是否为偶数 → ③ 把两边多余的水果各取一半放进列表 `excess` → ④ 计算全局最小成本 `global_min` → ⑤ 对 `excess` 中的每个元素，用 `min(x, 2*global_min)` 累加得到答案。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def minCost(basket1: List[int], basket2: List[int]) -> int:
    """
    返回使两篮子相同的最小费用，若不可能则返回 -1
    """
    # 1️⃣ 统计频次
    cnt1 = Counter(basket1)
    cnt2 = Counter(basket2)

    # 2️⃣ 判断可行性
    all_keys = set(cnt1) | set(cnt2)          # 两个篮子出现过的所有成本
    for k in all_keys:
        if (cnt1[k] + cnt2[k]) % 2:           # 总次数为奇数 → 不可行
            return -1

    # 3️⃣ 收集需要交换的“多余”水果
    excess = []                               # 只保存一半的多余元素
    for k in all_keys:
        diff = cnt1[k] - cnt2[k]              # 正数 → basket1 多，负数 → basket2 多
        if diff > 0:                          # basket1 多出来的
            excess.extend([k] * (diff // 2))
        elif diff < 0:                        # basket2 多出来的
            excess.extend([k] * (-diff // 2))

    if not excess:                            # 已经相等
        return 0

    # 4️⃣ 全局最小成本（所有水果里最小的那个）
    global_min = min(min(basket1), min(basket2))

    # 5️⃣ 贪心计算费用
    excess.sort()                             # 从小到大处理
    total = 0
    for x in excess:
        # 直接换的费用是 x，使用全局最小元素中转的费用是 2*global_min
        total += min(x, 2 * global_min)

    return total
```

> **代码解释**  
> - 第 1 行 `Counter` 类似于**查字典**，键是水果成本，值是出现次数。  
> - 第 9‑13 行判断奇数总次数，如果出现则直接返回 `-1`。  
> - 第 17‑24 行把两边多余的水果各取一半放进 `excess`，因为每一次实际交换会消耗两颗“多余”水果。  
> - 第 28 行找出全局最小成本 `global_min`，后面会用它做“中转”。  
> - 第 32‑36 行对每个需要换出的水果 `x`，取 `min(x, 2*global_min)` 累加，即是最小费用。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 统计频次 `O(n)`（遍历两数组各一次）。  
  - 把多余元素收集进列表 `excess` 同样是 `O(n)`。  
  - 对 `excess` 排序需要 `O(m log m)`，其中 `m` ≤ `n`，所以整体是 `O(n log n)`。  
  - 与暴力解的指数级相比，这已经是 **线性对数** 的高效解法。  

- **空间复杂度**：`O(n)`  
  - 两个 `Counter` 各占用最多 `O(n)` 的键值对。  
  - `excess` 最多保存 `n/2` 个元素，也在 `O(n)` 范围内。  
  - 只使用常数级别的额外变量，整体空间是线性的。

---

## 心得

- **核心技巧**：利用**频次统计 + 贪心 + 全局最小元素中转**，把原本需要逐个模拟的交换转化为一次性计数求和。  
- **该技巧适用的题型**  
  1. 两个数组需要通过交换达到相同多集合的题目（如 *Minimum Cost to Make Two Arrays Identical*）。  
  2. 需要把不平衡的“供需”通过最小代价匹配的题目（如 *Assign Cookies*、*Two City Scheduling* 的变形）。  
- **一句话总结解题钥匙**：**先找出哪一边多余了哪些元素，再用全局最小值“充当搬运工”，用贪心把每一次换出的费用压到最低**。

---

## 反思

- **第一反应**：看到“交换成本 = 两个水果成本的较小值”，第一时间会想到**直接枚举所有交换**，因为这样最符合题面描述。  
- **最容易踩的坑**  
  - **奇数次数**：忘记检查某种成本出现次数的总和是否为偶数，导致在不可行的情况下仍继续计算。  
  - **中转费用**：误以为只需要比较 `x` 与 `global_min`，其实是 `2 * global_min`（两次换才能完成一次“间接”交换）。  
  - **列表长度**：`excess` 只需要保存 **一半** 的多余元素，若全部保存会把费用翻倍。  
- **下次遇到同类题**：第一步先**统计频次并判断可行性**，再思考是否可以**利用全局最小/最大值做中转**，最后用**贪心**把每一步的代价压到最低。