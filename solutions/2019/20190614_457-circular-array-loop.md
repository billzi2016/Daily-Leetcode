# #457. **环形数组循环** / Circular Array Loop

> 难度：中等 · 标签：Array、Hash Table、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/circular-array-loop/)

---

## 题目（英文原版）

**Description**

You are playing a game involving a circular array of non-zero integers nums. Each nums[i] denotes the number of indices forward/backward you must move if you are located at index i:
Since the array is circular, you may assume that moving forward from the last element puts you on the first element, and moving backwards from the first element puts you on the last element.
A cycle in the array consists of a sequence of indices seq of length k where:
Return true if there is a cycle in nums, or false otherwise.
Follow up: Could you solve it in O(n) time complexity and O(1) extra space complexity?

**Examples**

**Example 1:**

```
Input: nums = [2,-1,1,2,2]
Output: true
Explanation: The graph shows how the indices are connected. White nodes are jumping forward, while red is jumping backward.
We can see the cycle 0 --> 2 --> 3 --> 0 --> ..., and all of its nodes are white (jumping in the same direction).
```

**Example 2:**

```
Input: nums = [-1,-2,-3,-4,-5,6]
Output: false
Explanation: The graph shows how the indices are connected. White nodes are jumping forward, while red is jumping backward.
The only cycle is of size 1, so we return false.
```

**Example 3:**

```
Input: nums = [1,-1,5,1,4]
Output: true
Explanation: The graph shows how the indices are connected. White nodes are jumping forward, while red is jumping backward.
We can see the cycle 0 --> 1 --> 0 --> ..., and while it is of size > 1, it has a node jumping forward and a node jumping backward, so it is not a cycle.
We can see the cycle 3 --> 4 --> 3 --> ..., and all of its nodes are white (jumping in the same direction).
```

**Constraints**

- 1 <= nums.length <= 5000
- -1000 <= nums[i] <= 1000
- nums[i] != 0

---

## 题目（中文翻译）

你正在玩一个涉及环形数组（circular array）`nums` 的游戏，数组中的每个元素都是非零整数。`nums[i]` 表示如果当前位于下标 `i`，需要向前或向后移动的步数：

- 正数表示向前移动，负数表示向后移动。  
- 由于数组是环形的，向前移动超过最后一个元素会回到第一个元素，向后移动超过第一个元素会回到最后一个元素。

数组中的**循环（cycle）**是指一系列下标 `seq`，长度为 `k`（`k > 1`），满足：

1. 对于序列中的每个相邻下标 `seq[j]`，按照 `nums[seq[j]]` 的指示可以跳到下一个下标 `seq[(j+1) mod k]`。  
2. 所有跳跃的方向必须一致（全部向前或全部向后）。

如果 `nums` 中存在满足上述条件的循环，返回 `true`；否则返回 `false`。

---

### 示例

**示例 1**

```text
Input: nums = [2,-1,1,2,2]
Output: true
Explanation: 图示展示了下标之间的连接方式。白色节点表示向前跳跃，红色节点表示向后跳跃。
我们可以看到循环 0 → 2 → 3 → 0 → …，且所有节点都是白色（方向一致），因此返回 true。
```

**示例 2**

```text
Input: nums = [-1,-2,-3,-4,-5,6]
Output: false
Explanation: 图示展示了下标之间的连接方式。白色节点表示向前跳跃，红色节点表示向后跳跃。
唯一出现的循环长度为 1（自环），不符合要求，故返回 false。
```

**示例 3**

```text
Input: nums = [1,-1,5,1,4]
Output: true
Explanation: 图示展示了下标之间的连接方式。白色节点表示向前跳跃，红色节点表示向后跳跃。
我们可以看到循环 0 → 1 → 0 → …，虽然长度 > 1，但包含了向前和向后跳跃的节点，故不是合法循环。
随后可以看到循环 3 → 4 → 3 → …，所有节点均为白色（方向一致），因此返回 true。
```

---

### 约束条件

- `1 <= nums.length <= 5000`
- `-1000 <= nums[i] <= 1000`
- `nums[i] != 0`

---

### 进阶

能否在 **O(n)** 时间复杂度且 **O(1)** 额外空间复杂度下完成此题？

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**从每一个下标出发，按照题目给出的跳数一步步走下去，看看能否回到已经走过的下标**。  
如果在走的过程中出现了两次访问同一个下标，并且这条环的长度大于 1，且所有跳的方向（正向或负向）都相同，则说明找到了合法的循环。  

- **用到的数据结构**  
  - `visited` 集合（或列表）记录在本次遍历中已经访问过的下标。它就像我们平时查字典时的“已经看过的词”，只要出现重复就能立刻发现环。  
  - `direction` 记录当前起点的跳跃方向（正数为“顺时针”，负数为“逆时针”），相当于把所有跳的动作都划分到同一个“队伍”里，只有同队伍的成员才能一起形成合法环。  

- **为什么正确**  
  - 每一次遍历都完整模拟了从起点出发的运动轨迹，若出现环必然会在某一步再次访问到已经在 `visited` 里的下标。  
  - 我们额外检查环的长度是否大于 1（因为长度为 1 的自环不算），以及所有跳的符号是否一致，完全对应题目对“合法环”的定义。  

- **复杂度分析（大白话）**  
  - **时间复杂度**：最坏情况下我们会对每个下标都走遍整个数组一次。设数组长度为 `n`，则总步数大约是 `n + (n-1) + … + 1 ≈ n²/2`，记作 **O(n²)**。可以把它想象成“每个人都要跑全程”，所以时间会随 `n` 的平方增长。  
  - **空间复杂度**：我们只需要一个 `visited` 集合，最多保存 `n` 个下标，记作 **O(n)**。相当于“额外准备一个同等大小的背包”。  

#### 代码（Python）  

```python
from typing import List

def circularArrayLoop_brute(nums: List[int]) -> bool:
    n = len(nums)

    # 把数组视作环，利用取模实现循环跳转
    def next_index(i: int) -> int:
        # (i + nums[i]) 可能是负数，+n 再 % n 保证落在 [0, n-1] 区间
        return (i + nums[i]) % n

    for start in range(n):
        visited = set()               # 本次遍历的“已经走过的下标”
        cur = start
        direction = nums[start] > 0   # True 表示正向，False 表示负向

        while True:
            # 若已经访问过同一个下标，说明出现环
            if cur in visited:
                # 环的长度必须大于 1，且所有跳的方向必须相同
                if len(visited) > 1:
                    return True
                else:
                    break

            visited.add(cur)

            # 若当前元素的方向和起点方向不一致，直接终止这条路
            if (nums[cur] > 0) != direction:
                break

            cur = next_index(cur)

    return False
```

#### 复杂度  

- **时间复杂度**：O(n²) — 随着数组长度的增加，最坏情况下的运行时间会呈二次方增长。  
- **空间复杂度**：O(n) — 需要额外的集合来记录遍历过程中访问过的下标，最多存 `n` 个。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**重复遍历**：同一个环会被多个起点多次“探测”。  
要把时间降到 **O(n)**，我们需要 **一次遍历就把所有可能的环都检查完**，并且在检查完后**把涉及的下标标记为已处理**，以后再也不重复走。  

下面的核心思路来自 **快慢指针（Floyd 环检测）**，常用于链表找环。  
- 把数组视作一个“有向图”，每个下标指向下一个下标 `next(i)`。  
- 对于同一个起点，**慢指针一次走一步，快指针一次走两步**。  
  - 如果存在环，快指针必定会追上慢指针（就像跑道上快的跑者追上慢的）。  
  - 如果快指针跑出环（跳到方向不一致的节点或进入自环），则说明此起点不存在合法环。  

**关键细节**  
1. **方向统一**：在一次遍历中，所有跳的方向必须相同。若快指针或慢指针的下一跳方向和起点方向不同，就直接结束这条路径。  
2. **环长度 > 1**：当快慢指针相遇时，还要判断它们是否在同一个节点（自环）。如果 `slow == next(slow)`，说明只有一步回到自己，需排除。  
3. **标记已访问**：一旦确认从某个起点没有合法环，我们把沿途走过的所有下标的值设为 `0`（题目保证原始值非零），相当于把它们“打上已处理的标记”。以后遍历到这些下标时直接跳过，避免重复工作。  

**如何实现环的“下一步”**  
```python
def next_index(i):
    return (i + nums[i]) % n
```
取模保证数组是环形的，负数也能正确映射到 `[0, n-1]`。

#### 代码（Python）  

```python
from typing import List

def circularArrayLoop(nums: List[int]) -> bool:
    n = len(nums)

    # 计算下一个位置（循环数组）
    def next_index(i: int) -> int:
        return (i + nums[i]) % n

    for i in range(n):
        if nums[i] == 0:               # 已经被标记为“已访问”，直接跳过
            continue

        # 记录本次遍历的方向：True 为正向，False 为负向
        direction = nums[i] > 0

        # 初始化慢指针和快指针
        slow, fast = i, i

        while True:
            # ---- 移动慢指针一步 ----
            nxt_slow = next_index(slow)
            # 方向不一致或进入自环则退出
            if (nums[nxt_slow] > 0) != direction or nxt_slow == slow:
                break

            # ---- 移动快指针两步 ----
            nxt_fast = next_index(fast)
            if (nums[nxt_fast] > 0) != direction or nxt_fast == fast:
                break
            nxt_fast = next_index(nxt_fast)   # 第二步
            if (nums[nxt_fast] > 0) != direction or nxt_fast == fast:
                break

            # 更新指针
            slow, fast = nxt_slow, nxt_fast

            # 如果相遇，说明出现环
            if slow == fast:
                return True

        # ----- 本次遍历结束，标记路径上的所有节点为 0 -----
        # 目的是让后面的循环直接跳过这些已经确定不在合法环里的节点
        marker = i
        while nums[marker] != 0:
            nxt = next_index(marker)
            nums[marker] = 0          # 打上“已访问”标记
            # 如果方向不一致或已经回到自己，结束标记
            if (nums[nxt] > 0) != direction:
                break
            marker = nxt

    return False
```

> **代码要点注释**  
> - `nums[i] == 0` 用作“已访问”标记，省去额外的 `visited` 数组，实现 **O(1) 额外空间**。  
> - 每一次进入 `while` 循环，都先检查方向一致性和自环，确保只在同方向的子图里寻找环。  
> - 标记阶段使用的是同方向的遍历，防止把本来可能在别的方向形成环的节点误删。  

#### 复杂度  

- **时间复杂度**：O(n) — 每个下标最多被访问常数次（一次快慢指针遍历 + 一次标记过程），整体线性增长。相当于“跑完一圈马拉松”。  
- **空间复杂度**：O(1) — 只用了几个指针变量，没有额外的随 `n` 增长的数据结构。  

---  

## 心得  

- **核心技巧**：利用 **快慢指针（Floyd 判环）** 检测同向环，同时用 **原地标记**（把已确定不在合法环的元素设为 0）实现 O(1) 额外空间。  
- **适用的题型**  
  1. **环形数组/链表判环**（如 LeetCode 141. Linked List Cycle）  
  2. **有向图中寻找同向环**（如 “循环数组中的下一个更大元素” 的变形）  
  3. **需要 O(1) 空间的遍历**（如 “删除数组中的重复元素”）  
- **一句话总结解题钥匙**：**“把数组想成指向自身的有向图，用快慢指针追逐环，同时把已扫过的路标记掉”。**  

---  

## 反思  

- **第一反应**：看到“环形数组”和“每个元素都是跳数”，立刻想到“把每个下标当成图的节点，沿跳数走会形成一条有向链”。于是先尝试暴力遍历。  
- **最容易踩的坑**  
  1. **自环**：`next(i) == i` 的情况必须排除，否则会误判长度为 1 的环。  
  2. **方向不一致**：环里必须全部是正跳或全部是负跳，混合方向的环不算。忘记检查会导致错误答案。  
  3. **负数取模**：Python 的 `%` 对负数返回正数，但写成 `i + nums[i] % n` 会先取模导致错误，需要先算完整的位移再 `% n`。  
- **下次遇到同类题**：**第一步先判断方向是否统一**，然后**用快慢指针检测环**，并**记得把已访问的路径标记**，这样自然能做到 O(n) 时间、O(1) 空间。