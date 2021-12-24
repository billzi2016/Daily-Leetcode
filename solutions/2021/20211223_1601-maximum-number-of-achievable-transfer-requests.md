# #1601. 可实现的最大转移请求数 / Maximum Number of Achievable Transfer Requests

> 难度：困难 · 标签：Array、Backtracking、Bit Manipulation、Enumeration · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-achievable-transfer-requests/)

---

## 题目（英文原版）

**Description**

We have n buildings numbered from 0 to n - 1. Each building has a number of employees. It's transfer season, and some employees want to change the building they reside in.
You are given an array requests where requests[i] = [fromi, toi] represents an employee's request to transfer from building fromi to building toi.
All buildings are full, so a list of requests is achievable only if for each building, the net change in employee transfers is zero. This means the number of employees leaving is equal to the number of employees moving in. For example if n = 3 and two employees are leaving building 0, one is leaving building 1, and one is leaving building 2, there should be two employees moving to building 0, one employee moving to building 1, and one employee moving to building 2.
Return the maximum number of achievable requests.

**Examples**

**Example 1:**

```
Input: n = 5, requests = [[0,1],[1,0],[0,1],[1,2],[2,0],[3,4]]
Output: 5
Explantion: Let's see the requests:
From building 0 we have employees x and y and both want to move to building 1.
From building 1 we have employees a and b and they want to move to buildings 2 and 0 respectively.
From building 2 we have employee z and they want to move to building 0.
From building 3 we have employee c and they want to move to building 4.
From building 4 we don't have any requests.
We can achieve the requests of users x and b by swapping their places.
We can achieve the requests of users y, a and z by swapping the places in the 3 buildings.
```

**Example 2:**

```
Input: n = 3, requests = [[0,0],[1,2],[2,1]]
Output: 3
Explantion: Let's see the requests:
From building 0 we have employee x and they want to stay in the same building 0.
From building 1 we have employee y and they want to move to building 2.
From building 2 we have employee z and they want to move to building 1.
We can achieve all the requests.
```

**Example 3:**

```
Input: n = 4, requests = [[0,3],[3,1],[1,2],[2,0]]
Output: 4
```

**Constraints**

- 1 <= n <= 20
- 1 <= requests.length <= 16
- requests[i].length == 2
- 0 <= fromi, toi < n

---

## 题目（中文翻译）

我们有 `n` 栋建筑，编号为 `0` 到 `n - 1`。每栋建筑中都有若干员工。现在是调动季节，一些员工希望更换所在的建筑。

给定一个数组 `requests`，其中 `requests[i] = [from_i, to_i]` 表示第 `i` 位员工想从建筑 `from_i` 调往建筑 `to_i`。

所有建筑都是满员的，因此只有在每栋建筑的员工净变动为零时，一组请求才是可实现的。也就是说，每栋建筑离开的员工数必须等于进入的员工数。例如，若 `n = 3`，有两名员工离开建筑 `0`，一名员工离开建筑 `1`，一名员工离开建筑 `2`，则必须有两名员工搬入建筑 `0`，一名员工搬入建筑 `1`，一名员工搬入建筑 `2`。

返回能够实现的请求的最大数量。

**示例 1**  
**输入**: `n = 5`, `requests = [[0,1],[1,0],[0,1],[1,2],[2,0],[3,4]]`  
**输出**: `5`  
**解释**:  
让我们来看这些请求：  
- 从建筑 `0` 有员工 `x` 和 `y`，他们都想搬到建筑 `1`。  
- 从建筑 `1` 有员工 `a` 和 `b`，他们分别想搬到建筑 `2` 和建筑 `0`。  
- 从建筑 `2` 有员工 `z`，他想搬到建筑 `0`。  
- 从建筑 `3` 有员工 `c`，...（后文已截断）

**示例 2**  
**输入**: `n = 3`, `requests = [[0,0],[1,2],[2,1]]`  
**输出**: `3`  
**解释**:  
让我们来看这些请求：  
- 从建筑 `0` 有员工 `x`，他想留在同一栋建筑 `0`。  
- 从建筑 `1` 有员工 `y`，他想搬到建筑 `2`。  
- 从建筑 `2` 有员工 `z`，他想搬到建筑 `1`。  
我们可以全部实现这些请求。

**示例 3**  
**输入**: `n = 4`, `requests = [[0,3],[3,1],[1,2],[2,0]]`  
**输出**: `4`

**约束条件**  
- `1 <= n <= 20`  
- `1 <= requests.length <= 16`  
- `requests[i].length == 2`  
- `0 <= from_i, to_i < n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

这道题的核心要求是：**挑选出最多的请求，使得每栋楼的净流入为 0**。  
可以把每个请求看成一条有向边 `from → to`，挑选的请求集合形成一个子图。  
只要每个节点（楼）的出度减去入度等于 0，子图就是“可实现”的。

因为请求的总数最多只有 **16 条**（题目限制 `requests.length ≤ 16`），我们可以**枚举所有子集**，逐个检查它们是否满足条件，取满足条件的子集中请求数最多的那个。  

> **类比**：把所有请求想成一本小字典，字典里有 16 条记录。我们要挑出最多的记录，使得每个单词（楼号）出现的次数相同（出次数 = 入次数）。枚举子集就像把字典的每一页都可能翻开或不翻，2⁶⁴ 种组合在这里是 2¹⁶ = 65536，计算量非常小。

**为什么暴力一定能得到正确答案**  
- 枚举了**所有可能的请求组合**，不遗漏任何一种情况。  
- 对每一种组合，都严格检查“每栋楼的净变化为 0”。只要满足，说明这套请求是可实现的。  
- 在所有可实现的组合里挑最大者，自然得到最优解。

**时间/空间复杂度的大白话**  
- 枚举子集的次数是 `2^m`，其中 `m = len(requests)`（最多 16），所以最多只有 65536 次循环，这在电脑眼里几乎是瞬间完成。  
- 对每个子集我们要遍历请求一次，统计每栋楼的出入变化，时间是 `O(m)`。于是总时间是 `O(m * 2^m)`，也就是 `16 * 65536 ≈ 1e6` 次基本操作，完全可接受。  
- 需要一个长度为 `n`（最多 20）的数组来记录每栋楼的净变化，空间是 `O(n)`，很小。

#### 代码（Python）

```python
from typing import List

def maximumRequests(n: int, requests: List[List[int]]) -> int:
    m = len(requests)                 # 请求总数
    ans = 0                           # 当前找到的最大可实现请求数

    # 用二进制的位表示子集：第 i 位为 1 表示选第 i 条请求
    for mask in range(1 << m):        # 0 .. 2^m-1
        balance = [0] * n             # 每栋楼的净变化，正数表示进入，负数表示离开
        cnt = 0                       # 当前子集里选了多少条请求

        # 遍历所有请求，判断该请求是否在子集中（对应位是否为 1）
        for i in range(m):
            if mask >> i & 1:         # 第 i 位为 1，说明选了第 i 条请求
                frm, to = requests[i]
                balance[frm] -= 1     # 离开一人
                balance[to] += 1      # 进入一人
                cnt += 1

        # 检查所有楼的净变化是否都为 0
        if all(b == 0 for b in balance):
            ans = max(ans, cnt)       # 记录最大的可实现请求数

    return ans
```

> **关键行中文注释**  
> - `mask >> i & 1`：把掩码右移 `i` 位后取最低位，判断第 `i` 条请求是否被选。  
> - `balance[frm] -= 1`、`balance[to] += 1`：模拟员工离开和进入，类似“账本”记账。  
> - `all(b == 0 for b in balance)`：检查所有账目是否平衡，即每栋楼的净变化为 0。

#### 复杂度  

- **时间复杂度**：`O(m * 2^m)`  
  - `2^m` 是子集的总数，`m` 是遍历每个子集时要检查的请求数。  
  - 对于本题的上限 `m = 16`，约等于 `1,048,576` 次基本操作，几乎是常数时间。  
- **空间复杂度**：`O(n)`  
  - 只需要一个长度为 `n`（≤20）的数组 `balance` 来记录每栋楼的净变化。  

---

### 2. 最优解  

#### 思路  

在本题的约束下，**枚举所有子集已经是最优的**，因为：

1. **请求数量极小**（≤ 16），枚举 2^16 ≈ 6.5 万种情况在毫秒级即可完成。  
2. 任何更“高级”的算法（比如回溯剪枝、位运算 DP）在最坏情况下仍然需要遍历相同数量的状态，实际收益不大。  

不过，我们可以把实现方式稍微“打磨”一下，使代码更简洁、更易于理解：

- **位运算**：直接用整数的二进制位表示子集，省去列表保存子集。  
- **提前剪枝**：在遍历子集时，如果当前已选的请求数 `cnt` 连加上剩余未检查的请求数都达不到当前最佳 `ans`，可以提前结束该子集的检查。这个技巧在 `m` 较大时能明显降低常数。  

核心概念仍然是 **“每栋楼的净变化必须为 0”**，我们只是在实现细节上做了微调。

> **类比**：想象有 16 把钥匙，每把钥匙对应一条请求。我们要找出最多钥匙的组合，使得打开所有门后，每个房间的门数保持不变。枚举所有钥匙的开关状态（开/关）就是最直接的办法，而“提前剪枝”相当于在尝试打开钥匙时，如果发现已经不可能比当前最好的组合多，就不再继续尝试。

#### 代码（Python）

```python
from typing import List

def maximumRequests(n: int, requests: List[List[int]]) -> int:
    m = len(requests)
    ans = 0                # 记录当前找到的最大可实现请求数
    # 预先把每条请求的 (from, to) 保存为两个列表，便于快速索引
    frm = [r[0] for r in requests]
    to  = [r[1] for r in requests]

    # 这里使用递归回溯 + 剪枝（等价于枚举子集）
    def dfs(idx: int, cnt: int, balance: List[int]) -> None:
        nonlocal ans
        # 如果已经遍历完所有请求
        if idx == m:
            if all(b == 0 for b in balance):
                ans = max(ans, cnt)
            return

        # 剪枝：即使把后面的所有请求都选上，也达不到当前 ans，就不必继续
        if cnt + (m - idx) <= ans:
            return

        # 方案一：选当前请求
        balance[frm[idx]] -= 1
        balance[to[idx]]  += 1
        dfs(idx + 1, cnt + 1, balance)
        # 恢复现场（回溯）
        balance[frm[idx]] += 1
        balance[to[idx]]  -= 1

        # 方案二：不选当前请求
        dfs(idx + 1, cnt, balance)

    dfs(0, 0, [0] * n)
    return ans
```

> **关键行中文注释**  
> - `balance[frm[idx]] -= 1` / `balance[to[idx]] += 1`：把当前请求加入子集时的“记账”。  
> - `if cnt + (m - idx) <= ans:`：如果连把剩下的所有请求全选也不可能超过已有答案，就提前返回，避免无用搜索。  
> - 两次 `dfs` 分别对应“选”与“不选”当前请求，递归自然遍历所有子集。

#### 复杂度  

- **时间复杂度**：仍然是 `O(m * 2^m)`，但由于剪枝，实际遍历的子集数往往会少一些。  
- **空间复杂度**：`O(n + m)`  
  - `balance` 数组需要 `O(n)` 空间。  
  - 递归栈深度为 `m`，最多 `16` 层，算作常数空间。

---

## 心得  

- **核心技巧**：**枚举子集 + 通过“净变化为零”来验证可行性**。  
- **适用的题型**（类似思路）  
  1. **"Maximum Number of Achievable Transfer Requests"**（本题）  
  2. **"Count the Number of Good Subsets"**（子集满足某种平衡条件）  
  3. **"Maximum Compatibility Score Sum"**（对每个配对做二进制枚举）  

- **一句话总结解题钥匙**：  
  > 把每条请求视作“+1/-1 的记账”，遍历所有请求的取舍组合，找出让所有账本最终为 0 的最大组合。

---

## 反思  

- **拿到题目第一反应**：先想 “每栋楼的进出要相等”，于是想到 **枚举所有请求子集** 检查平衡。  
- **最容易踩的坑**  
  1. **忘记把同一栋楼的“自环请求”（如 [0,0]）也计入平衡**，虽然对净变化没有影响，但要记得在枚举时仍然要处理。  
  2. **边界条件**：`n` 可能比请求数少很多，仍然需要完整的 `balance` 长度为 `n`。  
  3. **整数溢出**：这里不存在，但在使用位运算时要确保 `1 << m` 不会超出 Python 整数范围（Python 整数是大整数，安全）。  

- **下次遇到同类题，第一步该想到**：  
  > “这是一道‘子集平衡’的题”，先判断 **请求/元素总数是否足够小**，如果是，就直接 **枚举子集**（位掩码或回溯），并在遍历时用**数组/哈希表记录状态**，检查是否满足平衡条件。这样往往能一次 AC。