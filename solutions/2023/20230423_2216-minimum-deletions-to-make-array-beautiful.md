# #2216. 使数组美观的最少删除次数 / Minimum Deletions to Make Array Beautiful

> 难度：中等 · 标签：Array、Stack、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-deletions-to-make-array-beautiful/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. The array nums is beautiful if:
Note that an empty array is considered beautiful.
You can delete any number of elements from nums. When you delete an element, all the elements to the right of the deleted element will be shifted one unit to the left to fill the gap created and all the elements to the left of the deleted element will remain unchanged.
Return the minimum number of elements to delete from nums to make it beautiful.

**Examples**

**Example 1:**

```
Input: nums = [1,1,2,3,5]
Output: 1
Explanation: You can delete either nums[0] or nums[1] to make nums = [1,2,3,5] which is beautiful. It can be proven you need at least 1 deletion to make nums beautiful.
```

**Example 2:**

```
Input: nums = [1,1,2,2,3,3]
Output: 2
Explanation: You can delete nums[0] and nums[5] to make nums = [1,2,2,3] which is beautiful. It can be proven you need at least 2 deletions to make nums beautiful.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 105

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的整数数组 `nums`。如果数组 `nums` 满足以下条件，则称其为 **beautiful**（美观的）：

> （题目原文中未给出具体条件，此处保持原样）

注意，空数组也被视为美观的。

你可以删除 `nums` 中任意数量的元素。删除一个元素后，所有位于该元素右侧的元素会左移一位填补空位，而左侧的元素保持不变。

返回使 `nums` 美观所需删除的最少元素个数。

---

### 示例

**示例 1**

> **输入**: `nums = [1,1,2,3,5]`  
> **输出**: `1`  
> **解释**: 你可以删除 `nums[0]` 或 `nums[1]`，得到 `nums = [1,2,3,5]`，此时数组是美观的。可以证明至少需要删除 1 个元素才能使数组美观。

**示例 2**

> **输入**: `nums = [1,1,2,2,3,3]`  
> **输出**: `2`  
> **解释**: 你可以删除 `nums[0]` 和 `nums[5]`，得到 `nums = [1,2,2,3]`，此时数组是美观的。可以证明至少需要删除 2 个元素才能使数组美观。

---

### 约束条件

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的删除方案**，找出其中删除最少且满足“美丽数组”条件的方案。  
- **美丽数组的定义**（题目给出的）  
  1. 长度必须是偶数。  
  2. 把数组按相邻两两分组（下标 0‑1、2‑3、…），每一组里的两个数必须不相等。  

我们可以把“删除若干元素”看成“从原数组中挑选一个子序列”。只要子序列的长度为偶数且每对相邻元素不同，就算是合法的。  

实现上可以用**回溯（DFS）**遍历每个位置：  
- 选择保留当前元素 → 把它加入正在构造的子序列。  
- 选择删除当前元素 → 什么也不做，继续往后走。  

遍历完所有元素后，检查构造好的子序列是否满足美丽条件，记录最少的删除次数。  

> **类比**：把数组想象成一本书的页码，想要得到一本“合格的书”，我们可以随意撕掉任意页码，只要剩下的页码数是偶数且每对相邻页码内容不同即可。暴力解就是把每一页都尝试“保留”或“撕掉”，枚举所有可能的书本。

#### 代码（Python）

```python
from typing import List

def min_deletions_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    best = n                     # 最坏情况：全部删光

    def dfs(idx: int, kept: List[int], deletions: int) -> None:
        """在下标 idx 位置继续搜索，kept 保存当前保留下来的元素"""
        nonlocal best
        # 剪枝：已经超过当前最优解，直接返回
        if deletions >= best:
            return
        # 走到数组末尾，检查是否美丽
        if idx == n:
            if len(kept) % 2 == 0:                     # 长度必须是偶数
                ok = True
                for i in range(0, len(kept), 2):       # 检查每一对是否不同
                    if kept[i] == kept[i + 1]:
                        ok = False
                        break
                if ok:                                 # 合法，更新最小删除数
                    best = deletions
            return

        # 方案 1：删除 nums[idx]
        dfs(idx + 1, kept, deletions + 1)

        # 方案 2：保留 nums[idx]
        kept.append(nums[idx])
        dfs(idx + 1, kept, deletions)
        kept.pop()   # 回溯，恢复现场

    dfs(0, [], 0)
    return best
```

> **运行提示**：这段代码只能在 `len(nums) ≤ 20` 左右的小规模数据上跑得过去，超过这个规模会出现指数级的爆炸。

#### 复杂度  

- **时间复杂度**：`O(2^n)`，因为每个元素都有“保留/删除”两种选择，整体是二叉树遍历。  
  > 大白话：如果数组有 30 个数，可能的删除方案多到 `2^30 ≈ 10^9`，几乎不可能在一秒内算完。  
- **空间复杂度**：`O(n)`，主要是递归栈和 `kept` 列表的最大深度。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正的难点在于如何快速判断哪些元素必须删除**，而不是枚举所有可能。  
观察美丽数组的要求，有两个关键点：

1. **长度必须为偶数**  
   - 如果最终得到的序列长度是奇数，只能再删掉最后一个元素。  

2. **每一对相邻元素必须不同**  
   - 当我们已经确定了第一个元素 `a`，第二个位置只能放**不是 `a` 的数**。如果下一个数恰好等于 `a`，它只能被删除。  

这就暗示了一种**贪心**策略：**从左到右一次遍历，尽量保留元素，只有在“会导致同一对相等”时才删**。  

具体做法：

- 维护一个 **已保留下来的数组 `res`**（也可以只用计数）。  
- 对每个 `x = nums[i]`：  
  - 如果 `len(res)` 为偶数，说明我们正准备填**新的一对的第一个位置**，直接把 `x` 加进去（没有约束）。  
  - 如果 `len(res)` 为奇数，说明 `x` 将成为**当前这对的第二个位置**。这时检查 `x` 是否等于 `res[-1]`（当前对的第一个数）：  
    - 若相等 → 必须删掉 `x`（否则这对会不符合条件）。  
    - 若不相等 → 把 `x` 加入 `res`，这对就完成了。  

- 遍历结束后，**如果 `res` 长度是奇数**，说明最后剩下一个孤儿，只能再删掉它，使长度变为偶数。  

整个过程只需要一次线性扫描，**不需要额外的数据结构**，只用几个变量记录当前长度即可。  

> **类比**：想象你在排队买票，每两个人组成一组，要求同组里两个人的服装颜色不同。你从左到右检查每个人的颜色：  
> - 当你正要为新组挑第一个人时，随便挑。  
> - 当你为同组挑第二个人时，如果颜色和第一个相同，你只能让他离开（删掉），否则就让他加入。  
> 最后如果还有一个人单独站着（奇数），也只能让他离开。

#### 代码（Python）

```python
from typing import List

def min_deletions(nums: List[int]) -> int:
    """
    返回最少的删除次数，使数组成为「美丽」数组。
    思路：一次遍历，贪心保留，只有在形成相等的相邻对时才删。
    """
    kept_len = 0                # 已保留下来的元素个数（不必真的存列表）
    deletions = 0               # 已经删除的元素个数

    for x in nums:
        if kept_len % 2 == 0:           # 正在准备新的一对的第一个位置
            kept_len += 1               # 直接保留
        else:                           # 正在填当前对的第二个位置
            # 上一个保留的元素就是当前对的第一个
            # 为了避免相等，需要检查当前元素是否与它相同
            # 这里我们不保存具体元素，只用一个变量记录上一个元素的值
            # 为了实现，需要额外记录上一个保留的数
            # 为了代码简洁，这里直接用列表模拟
            # （实际实现可以用一个变量保存上一个数）
            # ---- 以下为简洁实现 ----
            # 注意：这里 kept_len 为奇数，说明 res[-1] 已经存在
            # 为了获取它，需要维护一个真实的列表
            # 为了不破坏整体思路，下面直接使用列表保存
            # （空间 O(n) 仍然满足题目要求）
            # -------------------------
            # 下面的实现采用列表方式，便于直观阅读
            # 如果你想要 O(1) 空间，只需要额外保存 last = res[-1]
            # 并在保留时更新 last
            pass

    # 为了实现上面的逻辑，这里改为使用列表
    res = []
    for x in nums:
        if len(res) % 2 == 0:               # 新对的第一个位置
            res.append(x)
        else:                               # 新对的第二个位置
            if res[-1] == x:                # 相等 → 删除当前元素
                deletions += 1
            else:
                res.append(x)               # 不相等 → 保留，完成一对

    # 最后如果长度为奇数，需要再删掉最后一个元素
    if len(res) % 2 == 1:
        deletions += 1

    return deletions
```

> **关键注释**  
- `len(res) % 2 == 0` → 正在填**新对的第一个**，没有约束，直接保留。  
- `len(res) % 2 == 1` → 正在填**新对的第二个**，必须和前一个不同，否则删除当前元素。  
- 循环结束后若 `len(res)` 为奇数，说明剩下一个“孤儿”，必须再删一次，使长度变偶。  

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次数组。  
  > 与暴力解 `O(2^n)` 相比，线性时间在 `10^5` 规模下轻松跑完。  
- **空间复杂度**：`O(1)`（如果仅用计数和一个变量保存上一个保留的值）或 `O(n)`（如上代码用了 `res` 列表，仅用于说明，实际可改为常数空间）。  

---

## 心得  

- **核心技巧**：**贪心配对**——在满足“相邻两两不相等”这一局部约束时，尽可能保留元素，只在“会导致冲突”时才删除。  
- **适用的题型**  
  1. “把数组按两两分组，每组满足某种局部条件” 类题（如 *Make Array Good*、*Delete Elements to Make Array Sorted*）。  
  2. 需要 **最少删除** 使序列满足 **相邻约束** 的问题（如 *Minimum Deletions to Make String Balanced*）。  
- **一句话总结解题钥匙**：**只在“当前元素会破坏已经确定的配对”时删，否则全部保留**。  

---

## 反思  

- **第一反应**：看到“删除任意元素，使数组满足偶数长度且相邻两两不同”，立刻想到**枚举子序列**（暴力）或**动态规划**。但仔细审视约束后发现每两个元素只相互影响，提示可以用**局部贪心**。  
- **最容易踩的坑**  
  1. **奇数长度**：遍历结束后忘记检查最终长度是否为偶数，导致答案少删一次。  
  2. **相等判断位置**：必须在**第二个位置**检查是否与第一个相同，错误地在第一个位置判断会导致多删。  
  3. **边界情况**：数组本身为空或只有一个元素时，需要返回 `0`（空数组已美丽）或 `1`（单元素必须删掉），代码要能自然处理。  
- **下次类似题目第一步**：先**把约束写成“每两两之间的局部规则”**，思考**是否可以一次遍历配对**，如果可以，立刻尝试贪心；如果局部规则相互交叉，则考虑 DP 或更高级的数据结构。