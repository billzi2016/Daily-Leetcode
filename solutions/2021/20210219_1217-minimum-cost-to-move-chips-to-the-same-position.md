# #1217. **最小代价将芯片移动到同一位置** / Minimum Cost to Move Chips to The Same Position

> 难度：简单 · 标签：Array、Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-move-chips-to-the-same-position/)

---

## 题目（英文原版）

**Description**

We have n chips, where the position of the ith chip is position[i].
We need to move all the chips to the same position. In one step, we can change the position of the ith chip from position[i] to:
Return the minimum cost needed to move all the chips to the same position.

**Examples**

**Example 1:**

```
Input: position = [1,2,3]
Output: 1
Explanation: First step: Move the chip at position 3 to position 1 with cost = 0.
Second step: Move the chip at position 2 to position 1 with cost = 1.
Total cost is 1.
```

**Example 2:**

```
Input: position = [2,2,2,3,3]
Output: 2
Explanation: We can move the two chips at position  3 to position 2. Each move has cost = 1. The total cost = 2.
```

**Example 3:**

```
Input: position = [1,1000000000]
Output: 1
```

**Constraints**

- 1 <= position.length <= 100
- 1 <= position[i] <= 10^9

---

## 题目（中文翻译）

我们有 `n` 个芯片，其中第 `i` 个芯片的位置为 `position[i]`。  
我们需要将所有芯片移动到同一个位置。一次移动可以将第 `i` 个芯片从 `position[i]` 改为：

- `position[i] + 2` 或 `position[i] - 2`，代价为 `0`；
- `position[i] + 1` 或 `position[i] - 1`，代价为 `1`。

返回将所有芯片移动到同一位置所需的最小代价。

**示例**

**示例 1**  
```
Input: position = [1,2,3]
Output: 1
Explanation: 第一步：将位置为 3 的芯片移动到位置 1，代价 = 0。  
第二步：将位置为 2 的芯片移动到位置 1，代价 = 1。  
总代价为 1。
```

**示例 2**  
```
Input: position = [2,2,2,3,3]
Output: 2
Explanation: 可以将两个位置为 3 的芯片分别移动到位置 2。每次移动的代价为 1，总代价 = 2。
```

**示例 3**  
```
Input: position = [1,1000000000]
Output: 1
```

**约束条件**

- `1 <= position.length <= 100`
- `1 <= position[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有芯片一个一个搬到某个具体的位置**，然后把所有可能的目标位置都试一遍，挑出花费最少的那种。

- **数据结构**：只需要一个普通的 Python `list` 来保存芯片的位置。  
  - 可以把 `list` 想象成一排装着芯片的格子，每个格子里写着芯片的坐标。

- **为什么这样会得到正确答案**  
  - 题目要求“把所有芯片搬到同一个位置”，所以只要我们枚举了**所有**可能的目标位置，并且对每一种目标位置计算出真实的搬动费用，最小的那个费用一定就是答案。

- **复杂度分析（大白话）**  
  - 假设我们把目标位置从最左边的芯片坐标 `min_pos` 走到最右边的芯片坐标 `max_pos`，每走一步都要遍历所有 `n` 个芯片算一次费用。  
  - 于是总共要做 `n × (max_pos - min_pos + 1)` 次基本操作。  
  - 如果把 `n` 当作“有多少个小朋友要排队”，`max_pos-min_pos` 当作“排队的总长度”，这就相当于每走一步都要让所有小朋友排一次队，显然会很慢。  
  - 用大 O 表示就是 **O(n·range)**，在最坏情况下 `range` 可能是 `10^9`（因为坐标可以很大），这在电脑里根本跑不完。  
  - 空间上我们只用了原来的数组和几个计数变量，**O(1)**（常数级）额外空间。

#### 代码（Python）

```python
from typing import List

def minCostBruteForce(position: List[int]) -> int:
    # 1. 找到所有可能的目标位置（这里直接枚举最左到最右的整数）
    lo, hi = min(position), max(position)

    best = float('inf')                     # 用一个很大的数保存目前找到的最小费用
    for target in range(lo, hi + 1):        # 逐个尝试目标位置
        cost = 0
        for p in position:                 # 计算把每个芯片搬到 target 的费用
            # 搬动一次距离为 2 的倍数（偶数）免费，距离为奇数要花 1 元
            if abs(p - target) % 2 == 1:   # 奇数距离 → 需要付费 1
                cost += 1
        best = min(best, cost)             # 记录更小的费用
    return best
```

> **关键行解释**  
> - `abs(p - target) % 2 == 1`：判断两者之间的距离是奇数还是偶数。奇数需要付费 1，偶数免费。  
> - `best = min(best, cost)`：实时保存目前发现的最小费用。

#### 复杂度

- **时间复杂度**：`O(n·range)`  
  - 这里的 `range = max(position) - min(position) + 1`。  
  - 想象一下，如果 `range` 是 1000，`n` 是 100，循环次数就是 100 000；如果 `range` 是 10⁹，循环次数就是 10¹¹，显然不可接受。

- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了几个整数变量来记录最小值和临时费用。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正影响费用的不是具体的目标坐标，而是目标坐标的奇偶性**（是奇数还是偶数）。

- **观察 1**：如果我们把芯片搬到一个 **偶数位置**，所有已经在偶数位置的芯片搬动费用为 0（因为距离是偶数），而所有在奇数位置的芯片每个都要付 1。
- **观察 2**：同理，搬到 **奇数位置** 时，奇数位置的芯片费用为 0，偶数位置的芯片每个都要付 1。

于是，**只需要比较两种情况的费用哪个更小**：

| 目标奇偶性 | 需要付费的芯片 | 费用 |
|------------|--------------|------|
| 偶数目标   | 所有奇数位置的芯片 | `count_odd` |
| 奇数目标   | 所有偶数位置的芯片 | `count_even` |

答案就是 `min(count_odd, count_even)`。

> **为什么这样就一定对？**  
> 因为搬动的代价只取决于“是否要改变奇偶性”。不管目标坐标是 2 还是 1000，只要它们都是偶数，费用完全一样；同理，所有奇数目标的费用也一样。因此只要挑一个奇数目标或一个偶数目标即可。

- **核心技巧**：**计数奇偶**（Parity Counting）。  
  - 把“奇数”想象成“红球”，把“偶数”想象成“蓝球”。我们只需要数出红球和蓝球各有多少，最后把较少的一种全部搬到另一种颜色所在的格子里，花费最少。

- **数据结构**：仍然只需要一个 `list`，以及两个整数变量 `odd`、`even` 来计数。  
  - 类比：把 `list` 看成一盒子里的彩球，`odd`、`even` 就是记录红球和蓝球数量的记事本。

#### 代码（Python）

```python
from typing import List

def minCost(position: List[int]) -> int:
    odd = even = 0                     # 初始化奇数、偶数计数器
    for p in position:
        if p % 2:                      # p % 2 == 1 → 奇数
            odd += 1
        else:                          # p % 2 == 0 → 偶数
            even += 1
    # 把数量少的那一类全部搬过去，费用就是它的数量
    return min(odd, even)
```

> **关键行解释**  
> - `p % 2`：取余 2，结果是 0（偶数）或 1（奇数）。  
> - `min(odd, even)`：费用最小的方案就是把少数那类芯片搬到多数那类所在的格子。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，像一次快速的点名，花的时间正比于芯片的数量 `n`。  
  - 与暴力解相比，省掉了遍历“所有可能的目标位置”的那一步，直接把时间降到了线性。

- **空间复杂度**：`O(1)`  
  - 只用了几个整数计数器，和输入规模无关。

---

## 心得

- **核心技巧**：**奇偶计数（Parity Counting）**——把问题转化为“把奇数和偶数分到同一边”，费用等于较少那一边的数量。
- **适用的题型**  
  1. “把所有数变成相同奇偶性”类题（如 LeetCode 2171 Minimum Cost to Move Chips to The Same Position）。  
  2. “把数组中的元素全部变为相同值，代价只和是否相等有关”类题（如把数组中 0 与 1 统一的最小翻转次数）。  
  3. “只关心元素的某一位特征（奇偶、正负、是否为素数）”的分组计数题。
- **一句话总结解题钥匙**：**把费用只和奇偶有关的观察抽象出来，统计两类的数量，搬动少的那一类即可**。

---

## 反思

- **第一反应**：看到“搬动一步 2 的倍数免费、1 的倍数要花费 1”，立刻想到要遍历所有目标位置来算费用——这就是暴力思路。
- **最容易踩的坑**  
  1. **忽略坐标范围太大**：直接枚举 `1 … 10⁹` 会导致超时。  
  2. **忘记奇偶性决定费用**：如果只关注具体距离，会错失把问题简化到奇偶计数的机会。  
  3. **边界条件**：只有一个芯片时，答案一定是 0；全部已经是同奇偶时也应直接返回 0。
- **下次遇到同类题**，第一步应该问自己：“**费用是否只取决于某个离散特征（如奇偶、正负）而不是具体数值本身？**”。如果答案是肯定的，就立刻转向**计数/分组**的思路，而不是盲目枚举所有可能的目标。