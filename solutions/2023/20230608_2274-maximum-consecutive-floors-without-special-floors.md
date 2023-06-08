# #2274. **最大连续非特殊楼层数** / Maximum Consecutive Floors Without Special Floors

> 难度：中等 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-consecutive-floors-without-special-floors/)

---

## 题目（英文原版）

**Description**

Alice manages a company and has rented some floors of a building as office space. Alice has decided some of these floors should be special floors, used for relaxation only.
You are given two integers bottom and top, which denote that Alice has rented all the floors from bottom to top (inclusive). You are also given the integer array special, where special[i] denotes a special floor that Alice has designated for relaxation.
Return the maximum number of consecutive floors without a special floor.

**Examples**

**Example 1:**

```
Input: bottom = 2, top = 9, special = [4,6]
Output: 3
Explanation: The following are the ranges (inclusive) of consecutive floors without a special floor:
- (2, 3) with a total amount of 2 floors.
- (5, 5) with a total amount of 1 floor.
- (7, 9) with a total amount of 3 floors.
Therefore, we return the maximum number which is 3 floors.
```

**Example 2:**

```
Input: bottom = 6, top = 8, special = [7,6,8]
Output: 0
Explanation: Every floor rented is a special floor, so we return 0.
```

**Constraints**

- 1 <= special.length <= 105
- 1 <= bottom <= special[i] <= top <= 109
- All the values of special are unique.

---

## 题目（中文翻译）

Alice 管理一家公司，并租下了大楼中的若干层作为办公空间。Alice 决定其中的某些楼层为特殊楼层，仅用于休闲。  
给定两个整数 `bottom` 和 `top`，表示 Alice 租下了从 `bottom` 到 `top`（包括两端）的所有楼层。另给定整数数组 `special`，其中 `special[i]` 表示被指定为特殊楼层的楼层号。  
返回没有特殊楼层的最长连续楼层数。

**示例 1**  
**示例 2**  
**约束条件**  

**示例：**  
**示例 1:**  
```
Input: bottom = 2, top = 9, special = [4,6]
Output: 3
```
**解释:** 以下是没有特殊楼层的连续楼层范围（含端点）：
- (2, 3) 共 2 层。  
- (5, 5) 共 1 层。  
- (7, 9) 共 3 层。  

因此返回的最大值为 3 层。

**示例 2:**  
```
Input: bottom = 6, top = 8, special = [7,6,8]
Output: 0
```
**解释:** 所有租下的楼层都是特殊楼层，所以返回 0。

**约束条件：**
- `1 <= special.length <= 10^5`
- `1 <= bottom <= special[i] <= top <= 10^9`
- `special` 中的所有值互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每一层** 都检查一遍，看看它是不是特殊楼层。如果不是，就把它计入当前连续的普通楼层长度；一旦遇到特殊楼层，就把计数器清零，记录下之前的最大值。  
这类似于我们在 **走楼梯** 时，手里拿着一个计数器，遇到“禁止上去的层”（特殊层）就把计数器归零，继续往上数。

- **用到的数据结构**：  
  - `set`（集合），把 `special` 数组放进去，查找是否是特殊层的时间是 **O(1)**，就像查字典一样，词（楼层）在不在字典里（特殊集合）一眼就能看出来。  

- **为什么正确**：  
  - 我们逐层遍历，完整覆盖了 **bottom → top** 的所有楼层。每一次遇到非特殊楼层时，计数器都会累计，遇到特殊楼层时就把当前连续段的长度保存下来。遍历结束后，保存的最大值就是答案。

- **复杂度分析**（大白话解释）  
  - **时间复杂度**：`O(range)`，其中 `range = top - bottom + 1`。如果把楼层想象成一条很长的走廊，走一遍需要的时间正比于走廊的长度。题目里 `top` 可能达到 `10^9`，走这么长的走廊显然不可行。  
  - **空间复杂度**：`O(m)`，`m = len(special)`，因为我们要把所有特殊楼层放进集合，相当于准备了一本只记录特殊楼层的“小字典”。

#### 代码（Python）

```python
def max_consecutive_floors_bruteforce(bottom: int, top: int, special: list[int]) -> int:
    # 把特殊楼层放进集合，查找 O(1)
    special_set = set(special)

    max_len = 0          # 记录最大的连续普通楼层数
    cur_len = 0          # 当前连续普通楼层的长度

    # 从 bottom 一层层遍历到 top
    for floor in range(bottom, top + 1):
        if floor in special_set:          # 遇到特殊楼层，当前段结束
            max_len = max(max_len, cur_len)
            cur_len = 0                  # 重新计数
        else:                              # 普通楼层，计数器加一
            cur_len += 1

    # 循环结束后，还要比较最后一段（如果最后一层不是特殊层）
    max_len = max(max_len, cur_len)
    return max_len
```

#### 复杂度

- **时间复杂度**：`O(top - bottom + 1)`  
  - 直白来说，就是“走完整栋楼的每一层”。如果楼层数是几亿，这一步会超时。
- **空间复杂度**：`O(m)`（`m = len(special)`）  
  - 只需要保存特殊楼层的集合，和楼层总数无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**遍历每一层** 是最大的性能瓶颈。我们其实不需要检查所有楼层，只需要关注 **特殊楼层之间的空隙**。  
想象把所有特殊楼层排好队（从低到高），它们把整栋楼划分成若干段：

```
bottom ... special[0]   special[1] ... special[2]   ...   special[n-1] ... top
```

每两相邻的特殊楼层之间的 **普通楼层数量** = `right - left - 1`（因为左右两端都是特殊层，本身不算）。  
此外，还要考虑最左侧（`bottom` 到第一个特殊层）和最右侧（最后一个特殊层到 `top`）这两段，它们只有一端是特殊层。

因此，求解步骤如下：

1. **排序** `special`（从小到大），这样相邻的特殊楼层就能直接相邻出现。排序的时间是 `O(m log m)`，其中 `m = len(special)`。
2. 初始化答案 `ans = 0`。
3. **遍历相邻特殊楼层**，计算 `gap = special[i] - special[i-1] - 1`，更新 `ans = max(ans, gap)`。
4. 处理两端的特殊情况：  
   - `ans = max(ans, special[0] - bottom)`（左侧空隙）  
   - `ans = max(ans, top - special[-1])`（右侧空隙）

> **类比**：把特殊楼层想象成 **路灯**，路灯之间的黑暗区域就是我们要找的最长连续普通楼层。只要知道每盏灯的坐标，计算相邻灯之间的黑暗长度就行了。

#### 代码（Python）

```python
def max_consecutive_floors(bottom: int, top: int, special: list[int]) -> int:
    # 1. 把特殊楼层从小到大排好序（相当于把路灯按位置排好）
    special.sort()

    # 2. 初始化答案，先考虑左侧和右侧的空隙
    ans = max(special[0] - bottom, top - special[-1])

    # 3. 遍历相邻的特殊楼层，计算中间的空隙长度
    for i in range(1, len(special)):
        # 两盏灯之间的黑暗区长度 = 右灯 - 左灯 - 1
        gap = special[i] - special[i - 1] - 1
        ans = max(ans, gap)   # 保留最大的那段

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m log m)`  
  - 只需要一次排序（`log` 是对数），随后线性遍历一次。相比遍历每一层的暴力解，这里只跟特殊楼层的数量 `m` 有关，`m ≤ 10^5`，完全可接受。  
- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了常数个额外变量，排序是原地进行的（Python 的 `list.sort()` 是原地排序），不需要额外的存储。

---

## 心得

- **核心技巧**：**利用排序后相邻元素的差值** 来直接得到区间长度。  
- **适用的题型**：  
  1. “在一段连续区间里找最长的空白段”——如 **“Maximum Consecutive Days Without Rain”**。  
  2. “把若干特殊点划分区间，求最长区间”——如 **“Maximum Length of a Pair Chain”**（变形后也可用差值思路）。  
- **一句话总结**：**把问题从“遍历每一层”转化为“只看特殊层之间的间距”，排序是打开这把钥匙的第一步。**

---

## 反思

- **第一反应**：直接从 `bottom` 到 `top` 逐层遍历，记录连续普通楼层的长度。  
- **最容易踩的坑**：  
  - 忘记处理 **两端的空隙**（左侧 `bottom` 到第一个特殊层，右侧最后一个特殊层到 `top`）。  
  - 在计算相邻特殊层之间的间距时，忘记减去两端的特殊层本身，导致多算了 1。  
  - 当所有楼层都是特殊层时，需要返回 `0`，而不是负数。  
- **下次遇到同类题**，第一步应想到：**先把关键点（特殊楼层、障碍点等）排序，再利用相邻点的差值直接得到区间长度**。这样可以把原本可能是 `O(range)` 的暴力遍历，压缩到 `O(k log k)`（`k` 为关键点数量）。