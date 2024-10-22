# #2910. 创建有效分配所需的最少组数 / Minimum Number of Groups to Create a Valid Assignment

> 难度：中等 · 标签：Array、Hash Table、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-groups-to-create-a-valid-assignment/)

---

## 题目（英文原版）

**Description**

You are given a collection of numbered balls and instructed to sort them into boxes for a nearly balanced distribution. There are two rules you must follow:
​Return the fewest number of boxes to sort these balls following these rules.

**Examples**

**Example 1:**

```
Input: balls = [3,2,3,2,3]
Output: 2
Explanation:
We can sort balls into boxes as follows:
The size difference between the two boxes doesn't exceed one.
```

**Example 2:**

```
Input: balls = [10,10,10,3,1,1]
Output: 4
Explanation:
We can sort balls into boxes as follows:
You can't use fewer than four boxes while still following the rules. For example, putting all three balls numbered 10 in one box would break the rule about the maximum size difference between boxes.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个编号球（balls）的集合，需要将它们划分到若干盒子（boxes）中，使得分配尽可能平衡。必须遵守以下两条规则（规则内容在原题中省略，直接按照题意返回满足规则的最少盒子数量）。  

返回在遵守上述规则的前提下，能够对这些球进行划分的最少盒子数量。

**示例**  

**示例 1**  
```
Input: balls = [3,2,3,2,3]
Output: 2
Explanation:
我们可以将球划分到两个盒子中，使得两个盒子的大小差不超过 1。
```

**示例 2**  
```
Input: balls = [10,10,10,3,1,1]
Output: 4
Explanation:
我们可以将球划分到四个盒子中。若使用少于四个盒子则会违背规则，例如把所有三个编号为 10 的球放入同一个盒子会导致盒子之间的最大大小差超过允许范围。
```

**约束条件**  
- 1 ≤ `balls`.length ≤ 10⁵  
- 1 ≤ `balls[i]` ≤ 10⁹

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一个球都「手动」放进箱子里，尝试所有可能的分配方式，然后挑出满足 **规则**（每种编号的球只能放进大小为 `x` 或 `x+1` 的箱子，且所有箱子的大小差不超过 1） 的最小箱子数量。

- **数据结构**：我们可以用一个 `list` 保存每个箱子的当前容量，用 `dict` 统计每种编号出现了多少次（相当于查字典，键是球的编号，值是出现次数）。
- **为什么能得到答案**：只要遍历到了所有合法的放法，必然会包含最优解。于是把所有合法解的箱子数取最小，就得到答案。
- **为什么不实际使用**：这种「全枚举」的搜索空间极其庞大。设有 `n` 个球，箱子数最多 `n`，每个球都有 `O(n)` 种放法，时间复杂度大约是 `O(n^n)`，根本不可行。

> **时间/空间复杂度的“大白话”**  
> - `O(n^n)` 意味着如果有 10 个球，程序要尝试 10 的 10 次方（10 000 000 000）种情况，显然跑不完。  
> - 空间上我们只需要存几个临时列表，算是 `O(n)`，但时间的天文数字让这套方法只能作为「思考的起点」，不能交给机器运行。

#### 代码（Python）

```python
from collections import Counter
import itertools

def brute_min_groups(balls):
    """
    暴力枚举所有可能的分箱方式（仅用于说明思路，实际不可运行）。
    """
    n = len(balls)
    freq = Counter(balls)                     # 统计每种球的出现次数
    best = n + 1                               # 初始化为不可能的上界

    # 这里我们假设最多用 n 个箱子，每个箱子大小从 1 到 n
    # 真实实现会导致指数级爆炸，这段代码仅作演示。
    for groups in range(1, n + 1):
        # 生成所有把 n 个球划分成 `groups` 个箱子的方式（组合爆炸！）
        # 用 itertools.product 仅作占位示例
        for assign in itertools.product(range(groups), repeat=n):
            # 统计每个箱子的大小
            size = [0] * groups
            for i, g in enumerate(assign):
                size[g] += 1

            # 检查是否满足“每种编号的球只放在大小为 x 或 x+1 的箱子”
            ok = True
            for num, cnt in freq.items():
                # 找到所有装有该编号球的箱子大小集合
                possible_sizes = {size[g] for i, g in enumerate(assign) if balls[i] == num}
                # 必须是 1~2 种连续的大小
                if len(possible_sizes) > 2 or (len(possible_sizes) == 2 and max(possible_sizes)-min(possible_sizes) != 1):
                    ok = False
                    break
            if ok:
                best = min(best, groups)
                break   # 已经找到最小的 groups，退出内部循环
        if best != n + 1:
            break       # 已经找到答案，退出外层循环
    return best
```

> 代码里每一行都加了中文注释，帮助你看清每一步在干什么。**请注意**：这段代码在 `n` 超过 10 时会卡死，只是用来说明「暴力」的思路。

#### 复杂度  

- **时间复杂度**：`O(n^n)` —— 每个球都有 `n` 种放箱子的选择，指数级增长，实际不可接受。  
- **空间复杂度**：`O(n)` —— 只保存箱子大小等线性空间，但被巨大的时间消耗掩盖。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的难点在于如何快速判断某个大小 `x` 是否可行**，以及在可行的情况下需要多少个箱子。  
观察提示可以得到以下关键事实：

1. **只关心每种球的出现次数**（频率），球的具体顺序完全不影响答案。  
2. 假设我们决定所有箱子的大小只能是 `x` 或 `x+1`（`x` 为正整数），那么对每一种编号的球，**只需要把它的 `f` 次出现划分成若干个大小为 `x` 或 `x+1` 的箱子**。  
3. 对单个频率 `f`，我们可以用数学方式直接算出最少需要多少个箱子，或者判断根本不可能。  

下面一步步推导如何计算：

- 把所有箱子先尽量装成 **较大的** `x+1`，因为这样箱子数最少。  
- 设 `a = f // (x+1)`（整除），`b = f % (x+1)`（余数）。  
  - `a` 表示可以完整装满 `a` 个 `x+1` 大小的箱子。  
  - `b` 表示剩余的球数，还不足以再填满一个 `x+1` 大小的箱子。

- **情况 1**：`b == 0`  
  - 正好全部用 `a` 个 `x+1` 大小的箱子，箱子数 = `a`。

- **情况 2**：`b > 0`  
  - 这 `b` 球必须放进若干个大小为 `x` 的箱子。  
  - 每个 `x` 大小的箱子可以容纳 `x` 球，所以需要的 `x`‑箱子数至少是 `ceil(b / x)`。  
  - 为了让所有箱子大小仍然只出现 `x` 或 `x+1`，我们可以把一些已经是 `x+1` 的箱子「拆」成 `x`，这会把箱子总数 **加 1**（因为把一个 `x+1` 拆成两个 `x`）。  
  - 关键是：如果 `x - b <= a`（即我们有足够的 `x+1` 箱子可以改成 `x`），则只需要 **`a + 1`** 个箱子（`a- (x-b)` 个 `x+1`，`x-b+1` 个 `x`）。  
  - 否则，**无法完成**，因为没有足够的 `x+1` 箱子来提供所需的 `x`‑箱子。

于是，对每个频率 `f`，只要遍历 `x = 1 … minFreq`（`minFreq` 为所有频率的最小值），计算上述公式得到该 `x` 下的箱子数（若不可行则记为无限大），把所有不同编号的箱子数相加得到 **总箱子数**。最后取所有 `x` 的最小值，即为答案。

> **为什么只需要遍历到 `minFreq`？**  
> 若 `x` 大于最小出现次数 `minFreq`，则必然有一种编号的球数 `f < x`，根本无法用 `x` 或 `x+1` 来装下（因为最小箱子已经比它的球数大），因此不会出现合法解。

#### 核心算法概览  

1. 统计每种球的出现次数 `freq`（哈希表 → 像查字典）。  
2. 求出 `minFreq = min(freq.values())`。  
3. 对每个可能的 `x`（`1 … minFreq`）：  
   - 对每个频率 `f` 调用 `need_groups(f, x)`，如果返回 `INF`（不可行），则该 `x` 整体不可行，直接跳到下一个 `x`。  
   - 否则把所有 `need_groups` 的结果累加得到 `total_groups`。  
   - 记录全局最小的 `total_groups`。  
4. 输出最小的 `total_groups`。

#### 代码（Python）

```python
from collections import Counter
from math import inf

def need_groups(f: int, x: int) -> int:
    """
    给定出现次数 f，箱子大小只能是 x 或 x+1，返回最少需要的箱子数量。
    若无法满足规则，返回 inf（相当于“不可能”）。
    """
    a = f // (x + 1)          # 能完整装满的 (x+1) 大小箱子数
    b = f % (x + 1)           # 剩余球数

    if b == 0:
        # 全部用 (x+1) 大小的箱子即可
        return a

    # 需要把一部分 (x+1) 箱子改成 x 大小的箱子
    # 这里的判断 x - b <= a 来自提示的推导
    if x - b <= a:
        # 只需要额外增加 1 个箱子（把若干 (x+1) 拆成 x）
        return a + 1
    # 否则无解
    return inf


def min_number_of_groups(balls):
    """
    主函数：返回满足规则的最少箱子数量。
    """
    freq = Counter(balls)                 # 统计每种编号出现的次数
    min_freq = min(freq.values())         # 所有频率的最小值
    answer = inf

    # x 的取值范围是 1 … min_freq
    for x in range(1, min_freq + 1):
        total = 0
        feasible = True
        for f in freq.values():
            need = need_groups(f, x)
            if need == inf:               # 只要有一种编号不可行，当前 x 直接放弃
                feasible = False
                break
            total += need
        if feasible:
            answer = min(answer, total)

    return answer
```

**代码要点中文注释**：

- `Counter` → 像字典一样把「球的编号」映射到「出现次数」。
- `need_groups` 用 **数学** 而不是「遍历」来直接算出最少箱子数，避免指数级搜索。
- `inf` 代表「不可能」，在遍历 `x` 时一旦出现 `inf`，就直接跳到下一个 `x`，省掉大量不必要的计算。

#### 复杂度  

- **时间复杂度**：`O(m * minFreq)`，其中 `m` 为不同球的种类数（`len(freq)`），`minFreq` 为所有频率的最小值。  
  - 最坏情况：所有球都相同 → `m = 1, minFreq = n`，复杂度 `O(n)`。  
  - 另一极端：每个球都不一样 → `m = n, minFreq = 1`，复杂度同样是 `O(n)`。  
  - 因此整体是线性级别，能够轻松应对 `n ≤ 10⁵` 的约束。  

- **空间复杂度**：`O(m)` 用于存放频率表，最多 `O(n)`，符合题目要求。

> **对比暴力**：  
> - 暴力是 `O(n^n)`，根本跑不完；  
> - 最优解是 `O(n)`（线性），在实际数据上可以在毫秒级完成。

---

## 心得

- **核心技巧**：把「每种编号的球」视为独立的「频率」问题，利用数学分解把「箱子大小只能是 x 或 x+1」转化为 **求最小整数解** 的公式。  
- **适用场景**：  
  1. 需要把若干相同元素划分成大小相差不超过 1 的若干组（如「把学生分成若干队，队伍人数只能相差 1」）。  
  2. 「分配资源」时每类资源只能装进两种容量的容器（如「装箱」或「任务分配」的近似均衡）。  
- **一句话总结解题钥匙**：**把每种元素的出现次数单独算，遍历所有可能的最小箱子大小 `x`，用公式快速求出对应的最少箱子数，取最小即得**。

---

## 反思

- **第一反应**：看到「箱子大小只能是 x 或 x+1」就想到「把数字分成相差不超过 1 的几组」，于是自然想到「统计频率」是第一步。  
- **最容易踩的坑**：  
  - 忽略了 `x` 的上界必须是 **最小频率**，否则会出现不合法的 `x`（比如 `x > f`）。  
  - 在计算 `need_groups` 时忘记 `b == 0` 的特殊处理，导致错误的箱子数。  
  - 边界条件 `f = 0`（不可能出现）或 `x = 1` 时的除法要特别小心。  
- **下次遇到同类题**：第一步立刻 **统计频率**，然后 **枚举可能的最小组大小**（通常是 `1 … minFreq`），再用 **数学公式** 检验可行性并累计结果。这样既避免了暴力搜索，又保证不会漏掉任何合法解。