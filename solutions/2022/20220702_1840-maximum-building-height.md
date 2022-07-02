# #1840. 最高建筑高度 / Maximum Building Height

> 难度：困难 · 标签：Array、Math、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-building-height/)

---

## 题目（英文原版）

**Description**

You want to build n new buildings in a city. The new buildings will be built in a line and are labeled from 1 to n.
However, there are city restrictions on the heights of the new buildings:
Additionally, there are city restrictions on the maximum height of specific buildings. These restrictions are given as a 2D integer array restrictions where restrictions[i] = [idi, maxHeighti] indicates that building idi must have a height less than or equal to maxHeighti.
It is guaranteed that each building will appear at most once in restrictions, and building 1 will not be in restrictions.
Return the maximum possible height of the tallest building.

**Examples**

**Example 1:**

```
Input: n = 5, restrictions = [[2,1],[4,1]]
Output: 2
Explanation: The green area in the image indicates the maximum allowed height for each building.
We can build the buildings with heights [0,1,2,1,2], and the tallest building has a height of 2.
```

**Example 2:**

```
Input: n = 6, restrictions = []
Output: 5
Explanation: The green area in the image indicates the maximum allowed height for each building.
We can build the buildings with heights [0,1,2,3,4,5], and the tallest building has a height of 5.
```

**Example 3:**

```
Input: n = 10, restrictions = [[5,3],[2,5],[7,4],[10,3]]
Output: 5
Explanation: The green area in the image indicates the maximum allowed height for each building.
We can build the buildings with heights [0,1,2,3,3,4,4,5,4,3], and the tallest building has a height of 5.
```

**Constraints**

- 2 <= n <= 109
- 0 <= restrictions.length <= min(n - 1, 105)
- 2 <= idi <= n
- idi is unique.
- 0 <= maxHeighti <= 109

---

## 题目（中文翻译）

你想在一座城市里新建 `n` 栋建筑。这些新建筑会按顺序排成一条直线，编号为 `1` 到 `n`。  
然而，城市对新建筑的高度有限制：

此外，城市还对特定建筑的最高高度有额外限制。这些限制以二维整数数组 `restrictions` 给出，其中 `restrictions[i] = [idi, maxHeighti]` 表示建筑 `idi` 的高度必须 **小于等于** `maxHeighti`。  
保证每栋建筑在 `restrictions` 中至多出现一次，且建筑 `1` 不会出现在 `restrictions` 中。  

返回所有可能方案中最高建筑的**最大可能高度**。

### 示例

#### 示例 1
**输入**: `n = 5, restrictions = [[2,1],[4,1]]`  
**输出**: `2`  
**解释**: 图中绿色区域表示每栋建筑的最高允许高度。我们可以将建筑高度设为 `[0,1,2,1,2]`，其中最高的建筑高度为 `2`。

#### 示例 2
**输入**: `n = 6, restrictions = []`  
**输出**: `5`  
**解释**: 图中绿色区域表示每栋建筑的最高允许高度。我们可以将建筑高度设为 `[0,1,2,3,4,5]`，其中最高的建筑高度为 `5`。

#### 示例 3
**输入**: `n = 10, restrictions = [[5,3],[2,5],[7,4],[10,3]]`  
**输出**: `5`  
**解释**: 图中绿色区域表示每栋建筑的最高允许高度。我们可以将建筑高度设为 `[0,1,2,3,3,4,4,5,4,3]`，其中最高的建筑高度为 `5`。

### 约束条件
- `2 <= n <= 10^9`
- `0 <= restrictions.length <= min(n - 1, 10^5)`
- `2 <= idi <= n`
- `idi` 唯一
- `0 <= maxHeighti <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把所有建筑的高度直接放进一个数组 `h[1…n]`，先把已知的限制写进去，其他位置先设成一个「无穷大」的值（因为我们只关心上限）。  
城市还有两条「隐形」规则：

1. 相邻两座建筑的高度差不能超过 1。  
   > 把它想象成一条斜坡，走一步只能升高或降低 1 米，不能一下子跳太高。  
2. 所有建筑的高度必须是非负整数。  

有了这两条规则，我们可以 **从左往右** 扫一遍，让每座建筑的高度不超过左边建筑的高度 + 1；随后 **从右往左** 再扫一遍，让每座建筑的高度不超过右边建筑的高度 + 1。两次扫描后，所有高度都满足相邻差 ≤ 1，且不违背已知的限制。

最后把数组里最大的值返回，就是答案。

> **为什么会对？**  
> 左→右扫描保证了「左边的约束」不会被右边的建筑破坏；右→左扫描则保证「右边的约束」同理。两遍扫完后，所有约束都被最紧的上限「压”下来”，于是得到的高度上限一定是可行的。

#### 代码（Python）

```python
import math
from typing import List

def maxBuildingHeight_bruteforce(n: int, restrictions: List[List[int]]) -> int:
    INF = 10 ** 18                     # 足够大的数，表示“没有上限”
    h = [INF] * (n + 1)                # 1‑based，h[0] 不用
    h[1] = 0                           # 第 1 栋楼高度可以设为 0（最小）

    # 把已知的限制写进去
    for idx, mx in restrictions:
        h[idx] = mx

    # 左→右：相邻差不能超过 1
    for i in range(2, n + 1):
        h[i] = min(h[i], h[i - 1] + 1)

    # 右→左：相邻差不能超过 1
    for i in range(n - 1, 0, -1):
        h[i] = min(h[i], h[i + 1] + 1)

    # 最大高度即为答案
    return max(h[1:])                  # 排除下标 0
```

> **关键行中文注释**  
> - `h = [INF] * (n + 1)`                       创建「上限」数组  
> - `h[i] = min(h[i], h[i - 1] + 1)`    左→右遍历，保证左侧不被超高  
> - `h[i] = min(h[i], h[i + 1] + 1)`    右→左遍历，保证右侧不被超高  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历了两遍数组，每次都是常数时间操作。  
  > 大白话：如果把每栋楼想成一行排队的学生，老师只需要从左到右喊一次、再从右到左喊一次，时间和学生人数成正比。  

- **空间复杂度**：`O(n)`  
  需要额外的高度数组，大小和建筑数量相同。  

> **局限**：题目中 `n` 可以高达 `10^9`，根本装不下这么大的数组，暴力解只能用于**小规模**（比如调试或教学）而不适合正式提交。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **需要 O(n) 的额外空间和时间**，而 `n` 可能是十亿。  
观察题目：  
- 只要知道 **受限制的建筑**（即 `restrictions` 中出现的那些）以及 **第 1 栋建筑** 的高度，上下相邻的限制之间的建筑高度是完全由这两个端点决定的。  
- 在两个受限建筑之间，最高点往往出现在**两条斜坡相遇的地方**，而不是每一栋都要枚举。

于是我们把注意力只放在 **受限建筑**（包括第 1 栋）上：

1. **把第 1 栋加入限制**：它的上限一定是 0（把它想成字典里“键 1 对应的值 0”）。  
2. **按编号排序**，得到一条从左到右的限制链。  
3. **左→右扫**：如果两个受限建筑相距 `d`，左边的最高高度只能往右提升 `d` 米，所以右边的上限要取 `min(original, leftHeight + d)`。  
4. **右→左扫**：同理，保证右边的限制不会让左边的建筑超高。  
   - 这两遍扫完后，所有受限建筑的上限已经 **相互协调**，再也不会产生冲突。  

5. **求最大可能高度**  
   - 受限建筑本身的上限 `h[i]` 当然是候选答案。  
   - 更重要的是，两座相邻受限建筑 `(id_i, h_i)` 与 `(id_j, h_j)` 之间可以形成一个「山峰」。  
     - 两边的斜坡每一步只能升高 1，距离为 `d = id_j - id_i`。  
     - 当两边斜坡相遇时的最高点是  
       \[
       \text{peak} = \left\lfloor\frac{h_i + h_j + d}{2}\right\rfloor
       \]  
       （向下取整是因为高度只能是整数）  
     - 这就好比两支向中间爬的梯子，最高点在它们相遇的那层。  

6. **特殊情况**：如果 `restrictions` 为空，则只能从第 1 栋开始一直递增，每一步升 1，最高楼层就是 `n‑1`。

整个过程只遍历了 **受限建筑的数量**（记作 `m`），`m ≤ 10^5`，完全可以接受。

#### 代码（Python）

```python
from typing import List

def maxBuildingHeight(n: int, restrictions: List[List[int]]) -> int:
    # 1. 把第 1 栋建筑加入限制，高度上限 0
    restrictions.append([1, 0])
    # 2. 按建筑编号排序
    restrictions.sort(key=lambda x: x[0])

    # 3. 左→右扫：保证左边的限制不会被右边的建筑超高
    for i in range(1, len(restrictions)):
        idx_cur, h_cur = restrictions[i]
        idx_pre, h_pre = restrictions[i - 1]
        # 两座建筑相距 d，左边最高能升到 h_pre + d
        allowed = h_pre + (idx_cur - idx_pre)
        if h_cur > allowed:
            restrictions[i][1] = allowed   # 把当前上限压下来

    # 4. 右→左扫：保证右边的限制不会被左边的建筑超高
    for i in range(len(restrictions) - 2, -1, -1):
        idx_cur, h_cur = restrictions[i]
        idx_nxt, h_nxt = restrictions[i + 1]
        allowed = h_nxt + (idx_nxt - idx_cur)
        if h_cur > allowed:
            restrictions[i][1] = allowed   # 同样压下来

    # 5. 在每段限制之间计算可能的最高点
    ans = 0
    for i in range(len(restrictions) - 1):
        id1, h1 = restrictions[i]
        id2, h2 = restrictions[i + 1]
        d = id2 - id1                     # 两座建筑的距离
        # 两边斜坡相遇的最高点（向下取整）
        peak = (h1 + h2 + d) // 2
        ans = max(ans, peak)

    # 6. 受限建筑本身的高度也可能是最高的
    for _, h in restrictions:
        ans = max(ans, h)

    # 7. 如果没有额外限制（只剩下第 1 栋），直接返回 n-1
    # （此时 restrictions 只剩 [1,0]，上面的循环已经得出 0，下面补上）
    if len(restrictions) == 1:          # 只剩第 1 栋
        ans = n - 1

    return ans
```

> **代码要点中文注释**  
> - `restrictions.append([1, 0])`    把第 1 栋楼的“最高 0 米”加入约束  
> - `allowed = h_pre + (idx_cur - idx_pre)` 左→右扫描时，左边最高能涨到的上限  
> - `peak = (h1 + h2 + d) // 2`    两座限制之间的“山峰高度”  

#### 复杂度  

- **时间复杂度**：`O(m log m)`，其中 `m = len(restrictions) + 1`（包括第 1 栋）。  
  - 主要开销是排序 `O(m log m)`，后面的两遍线性扫描和一次遍历都是 `O(m)`。  
  - 相比暴力的 `O(n)`，这里 `m ≤ 10^5`，即使 `n = 10^9` 也能轻松跑完。  

- **空间复杂度**：`O(m)`，只存储排序后的限制列表。  
  - 与 `n` 无关，极大降低了内存需求。  

> 与暴力解对比：  
> - 暴力需要 `O(n)` 的数组（在最坏情况下是十亿大小，根本装不下）。  
> - 最优解只关心 **有限的受限点**，时间和空间都与 `n` 的规模解耦。

---

## 心得

- **核心技巧**：**只在受限建筑之间思考**，利用“相邻差 ≤ 1”把高度的上限转化为 **线性约束**，再用两次单调扫描让约束自洽，最后用 **峰值公式** 计算两端之间的最高可能楼层。  
- **适用的题型**  
  1. LeetCode 1840 *Maximum Building Height*（本题）。  
  2. LeetCode 1845 *Seat Reservation Manager*（类似的「区间约束」需要排序后扫）。  
  3. LeetCode 1648 *Sell Diminishing Valued Colored Balls*（把大量元素压缩成区间后再处理）。  
- **一句话总结解题钥匙**：**把“每一步只能升降 1”视作斜坡，用受限点搭桥，峰值就在两端斜坡相遇处**。

---

## 反思

- **第一反应**：看到「相邻建筑高度差 ≤ 1」就想把所有建筑的高度都列出来，直接模拟。  
- **最容易踩的坑**  
  - **忘记第 1 栋楼的高度默认是 0**，导致左侧约束不成立。  
  - **忽视没有任何限制的情况**：此时答案是 `n‑1`，而不是 0。  
  - **整数除法取整错误**：峰值公式必须向下取整（`//`），否则会出现比实际可达更大的高度。  
- **下次类似题的第一步**：**先把所有约束点（包括必然的起点）排序，然后用左右两遍单调扫描把约束“压平”**，这样就把大规模问题压缩到几百或几千个关键点上。