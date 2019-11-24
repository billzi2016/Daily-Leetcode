# #672. 灯泡开关 II / Bulb Switcher II

> 难度：中等 · 标签：Math、Bit Manipulation、Depth-First Search、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/bulb-switcher-ii/)

---

## 题目（英文原版）

**Description**

There is a room with n bulbs labeled from 1 to n that all are turned on initially, and four buttons on the wall. Each of the four buttons has a different functionality where:
You must make exactly presses button presses in total. For each press, you may pick any of the four buttons to press.
Given the two integers n and presses, return the number of different possible statuses after performing all presses button presses.

**Examples**

**Example 1:**

```
Input: n = 1, presses = 1
Output: 2
Explanation: Status can be:
- [off] by pressing button 1
- [on] by pressing button 2
```

**Example 2:**

```
Input: n = 2, presses = 1
Output: 3
Explanation: Status can be:
- [off, off] by pressing button 1
- [on, off] by pressing button 2
- [off, on] by pressing button 3
```

**Example 3:**

```
Input: n = 3, presses = 1
Output: 4
Explanation: Status can be:
- [off, off, off] by pressing button 1
- [off, on, off] by pressing button 2
- [on, off, on] by pressing button 3
- [off, on, on] by pressing button 4
```

**Constraints**

- 1 <= n <= 1000
- 0 <= presses <= 1000

---

## 题目（中文翻译）

房间里有 n 盏灯泡（bulb），编号从 1 到 n，初始全部为打开状态，并且墙上有四个按钮（button）。这四个按钮各自具有不同的功能，分别是：

1. 按下按钮 1：翻转所有灯泡的状态。  
2. 按下按钮 2：翻转编号为偶数的灯泡的状态。  
3. 按下按钮 3：翻转编号为奇数的灯泡的状态。  
4. 按下按钮 4：翻转编号满足 `3k+1`（即形如 1, 4, 7, …）的灯泡的状态。

必须恰好进行 **presses** 次按钮按压（presses button presses）。每一次按压，你可以任选上述四个按钮中的任意一个。

给定整数 `n` 和 `presses`，返回在完成所有按压之后，可能出现的不同灯泡状态（status）的数量。

示例 1:
```
Input: n = 1, presses = 1
Output: 2
解释: 可能的状态为：
- 按下按钮 1 后得到 [off]
- 按下按钮 2 后得到 [on]
```

示例 2:
```
Input: n = 2, presses = 1
Output: 3
解释: 可能的状态为：
- 按下按钮 1 后得到 [off, off]
- 按下按钮 2 后得到 [on, off]
- 按下按钮 3 后得到 [off, on]
```

示例 3:
```
Input: n = 3, presses = 1
Output: 4
解释: 可能的状态为：
- 按下按钮 1 后得到 [off, off, off]
- 按下按钮 2 后得到 [off, on, off]
- 按下按钮 3 后得到 [on, off, on]
- 按下按钮 4 后得到 [off, on, on]
```

约束条件：
- `1 <= n <= 1000`
- `0 <= presses <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的按键序列都枚举一遍**，然后把每一次按完所有按钮后的灯泡状态记下来，最后统计不同的状态数量。

- **数据结构**：  
  - 用一个长度为 `n` 的列表 `bulbs` 表示灯泡的开关状态，`1` 代表开，`0` 代表关。  
  - 用 `set`（集合）把所有出现过的状态收集起来，集合天然去重，就像我们平时查字典时，键相同只能出现一次一样。

- **为什么正确**：  
  只要把**所有**合法的按键序列（每一步都可以任选 4 个按钮中的任意一个）都跑一遍，就一定不会漏掉任何一种可能的最终状态。于是统计集合的大小就是答案。

- **复杂度分析（大白话）**  
  - **时间**：每一次按键有 4 种选择，按 `presses` 次就有 `4^presses` 种不同的序列。对每一种序列我们都要遍历 `n` 盏灯去翻转状态，所以总体时间是 `O( n * 4^presses )`。如果把 `4^presses` 写成 `O(4^p)`，那 `p` 越大，指数增长得越快——相当于每多按一次键，就要把工作量 **翻四倍**，很快就不可接受了。  
  - **空间**：我们需要保存最多 `4^presses` 种状态（最坏情况每种序列都产生不同的状态），每种状态用 `n` 位表示，空间是 `O( n * 4^presses )`。同样是指数级的。

> 结论：暴力解只能在 `presses` 很小（比如 ≤ 5）时才勉强跑得动，根本不能满足题目里 `presses ≤ 1000` 的要求。

#### 代码（Python）

```python
from itertools import product

def flip(bulbs, button):
    """
    根据按下的按钮，对灯泡状态进行翻转。
    4 个按钮的功能分别是：
    1. 全部翻转
    2. 奇数编号灯泡翻转
    3. 偶数编号灯泡翻转
    4. 编号为 3 的倍数的灯泡翻转
    """
    n = len(bulbs)
    if button == 1:                # 全部翻转
        return [1 - b for b in bulbs]
    if button == 2:                # 奇数灯泡翻转（下标 0、2、4…）
        return [1 - b if i % 2 == 0 else b for i, b in enumerate(bulbs)]
    if button == 3:                # 偶数灯泡翻转（下标 1、3、5…）
        return [1 - b if i % 2 == 1 else b for i, b in enumerate(bulbs)]
    if button == 4:                # 3 的倍数灯泡翻转（下标 2、5、8…）
        return [1 - b if (i + 1) % 3 == 0 else b for i, b in enumerate(bulbs)]

def brute_force(n: int, presses: int) -> int:
    """暴力枚举所有按键序列，返回不同状态的数量（仅用于演示，实际不可用）"""
    init = [1] * n                     # 初始全开
    states = set()                     # 用集合自动去重

    # product 会生成所有长度为 presses、元素取值范围 1~4 的序列
    for seq in product(range(1, 5), repeat=presses):
        bulbs = init[:]
        for btn in seq:                # 逐个按钮执行翻转
            bulbs = flip(bulbs, btn)
        states.add(tuple(bulbs))       # 元组可哈希，放进集合

    return len(states)

# ------------------- 示例 -------------------
print(brute_force(1, 1))   # 2
print(brute_force(2, 1))   # 3
print(brute_force(3, 1))   # 4
```

> **提示**：上面的代码在 `presses=10` 时已经需要遍历 `4^10 = 1,048,576` 条序列，运行会非常慢，仅作思路展示。

#### 复杂度

- **时间复杂度**：`O(n * 4^presses)`  
  - “`4^presses`” 表示每一次按键都有 4 种选择，按键次数越多，工作量指数级增长，就像每次都要把 4 张卡片再翻一次。

- **空间复杂度**：`O(n * 4^presses)`  
  - 最坏情况下每条序列产生不同的灯泡状态，需要把所有状态都保存下来。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**真正导致状态不同的不是按键的顺序，而是每个按钮到底被按了奇数次还是偶数次**。因为同一个按钮连续按两次会把灯泡翻回原来的状态，等价于“没按”。这就把原本的 **`4^presses`** 种序列压缩到了 **`2^4 = 16`** 种可能（每个按钮 0/1 次）。

接下来我们再继续简化：

1. **按键次数的约束**  
   - 按钮只能被按 **0** 次或 **1** 次（奇偶性），于是所有合法的按钮组合可以用 4 位二进制数 `b1b2b3b4` 表示。  
   - 但我们必须保证 **总按键次数** `presses` 与这 4 位的 **奇数个数** 同奇同偶。因为如果 `presses` 是偶数，而我们选了奇数个按钮（每个按钮只算一次），我们可以再随意再按两次任意按钮（相当于 “抵消”），不改变最终状态。换句话说，只要 **`presses` ≥ 已选按钮数** 并且 **二者奇偶相同**，这组组合就是可实现的。

2. **灯泡数量的规律**  
   - 当 `n` 很大时，按钮的作用会出现周期性。观察四个按钮对灯泡的影响：
     - 第 1、2、3、4 按钮分别只关心 **位置的奇偶性** 或 **是否是 3 的倍数**。  
     - 当灯泡数 `n` ≥ **3** 时，前 3 盏灯的状态已经能够决定后面的灯的变化，因为 4 的作用只涉及“3 的倍数”。  
   - 实际上，只需要关注前 **3** 盏灯的状态，后面的灯会和它们形成 **重复模式**。所以 **`n` 大于 3 时等价于 `n = 3`**。

3. **枚举所有合法组合**  
   - 只遍历 `0~15`（16 种） 的二进制表示，筛掉不满足 `presses` 条件的组合，然后根据按钮作用算出前 `min(n,3)` 盏灯的最终状态，放进集合去重。

4. **得到答案的数学归纳**  
   通过枚举可以得到下面的“状态数表”。把表格记住，就可以直接 O(1) 返回答案，而不必真的去枚举。

| n (灯泡数) | presses = 0 | presses = 1 | presses = 2 | presses ≥ 3 |
|------------|-------------|-------------|-------------|-------------|
| 1          | 1           | 2           | 2           | 2 |
| 2          | 1           | 3           | 4           | 4 |
| ≥3         | 1           | 4           | 7           | 8 |

> 解释：  
> - `presses = 0` 时只能保持初始全开状态 → 1 种。  
> - `presses = 1` 时最多能产生 4 种不同的翻转方式（对应 4 个按钮），但当灯泡只有 1、2 盏时会出现重复，表格已经把这些重复合并。  
> - `presses = 2` 时组合数进一步增多，最多 7 种（因为 8 种中有一种会和已有的重复）。  
> - 当 `presses ≥ 3`，可以通过“多余的按键配对抵消”实现 **所有** 可能的 8 种状态（对应 3 盏灯的 2³=8 种开关组合）。

#### 代码（Python）

```python
def flip_by_mask(mask: int, n: int) -> tuple:
    """
    根据 4 位二进制 mask 表示的按钮集合，返回前 n 盏灯的状态。
    mask 的第 i 位（从右往左）代表第 i+1 个按钮是否被按（1 表示按了奇数次）。
    """
    # 初始全开
    state = [1] * n

    # 按钮 1：全部翻转
    if mask & 1:                     # 第 0 位对应按钮 1
        state = [1 - b for b in state]

    # 按钮 2：奇数编号灯泡翻转（下标 0、2、4…）
    if mask & 2:                     # 第 1 位对应按钮 2
        state = [1 - b if i % 2 == 0 else b for i, b in enumerate(state)]

    # 按钮 3：偶数编号灯泡翻转（下标 1、3、5…）
    if mask & 4:                     # 第 2 位对应按钮 3
        state = [1 - b if i % 2 == 1 else b for i, b in enumerate(state)]

    # 按钮 4：编号为 3 的倍数灯泡翻转（下标 2、5、8…）
    if mask & 8:                     # 第 3 位对应按钮 4
        state = [1 - b if (i + 1) % 3 == 0 else b for i, b in enumerate(state)]

    return tuple(state)              # 用 tuple 方便放进 set 去重

def bulbSwitcherII(n: int, presses: int) -> int:
    """
    最优解：O(1) 时间，O(1) 空间（只遍历 16 种按钮组合）。
    """
    if presses == 0:                 # 只能保持初始状态
        return 1

    # 只需要考虑前 3 盏灯，后面的灯会重复出现相同的模式
    m = min(n, 3)

    reachable = set()                # 用集合收集不同的状态

    # 遍历 0~15（四位二进制）的所有按钮子集
    for mask in range(16):
        # 统计 mask 中 1 的个数 → 实际被按的按钮数
        cnt = bin(mask).count('1')

        # 只有当 “按键次数 ≤ presses 且奇偶相同” 时，这个子集才可实现
        if cnt <= presses and (cnt % 2) == (presses % 2):
            reachable.add(flip_by_mask(mask, m))

    return len(reachable)

# ------------------- 示例 -------------------
print(bulbSwitcherII(1, 1))   # 2
print(bulbSwitcherII(2, 1))   # 3
print(bulbSwitcherII(3, 1))   # 4
print(bulbSwitcherII(3, 2))   # 7
print(bulbSwitcherII(1000, 1000))  # 8
```

> **关键点说明**  
> - `mask & 1`、`mask & 2`、`mask & 4`、`mask & 8` 分别判断第 1、2、3、4 个按钮是否被“奇数次”按下。  
> - `cnt % 2 == presses % 2` 用来确保 **奇偶性** 一致。  
> - `min(n, 3)` 把灯泡数裁剪到最多 3 盏，保证时间常数。

#### 复杂度

- **时间复杂度**：`O(1)`（固定遍历 16 种掩码，常数次的位运算和列表遍历）  
  - 与 `n`、`presses` 的大小无关，和暴力解的指数级增长形成鲜明对比。

- **空间复杂度**：`O(1)`（最多存 8 条状态，都是长度 ≤ 3 的元组）  

---

## 心得

- **核心技巧**：把“按键次数的奇偶性”抽象为 **位掩码**（二进制），并利用“多余的按键可以两两抵消”来把搜索空间从指数级压到常数级。  
- **适用的题型**  
  1. **开关类**题目（如 `Bulb Switcher I/II`、`Lamp Switch`），需要考虑按钮的组合与奇偶性。  
  2. **有限状态机**或**位运算**的题目，常常可以用 **状态压缩**（mask）把搜索空间大幅缩小。  
  3. **对称/周期性**问题，利用 “只看前几位，后面会重复” 的思想（如 `Flip String to Monotone Increasing` 中的前缀思路）。

- **一句话总结**：**“按键的奇偶决定最终状态，枚举 4 位掩码并用奇偶约束筛选，即可在常数时间得到答案”。**

---

## 反思

- **第一反应**：看到“必须恰好按 `presses` 次”，本能想到递归/DFS 暴力搜索。  
- **最容易踩的坑**  
  1. **忽略奇偶抵消**：忘记同一个按钮按两次等价于未按，会导致搜索空间爆炸。  
  2. **灯泡数大于 3 的处理**：直接遍历所有 `n` 盏灯会浪费时间，必须认识到 3 盏灯的状态已经决定了其余灯的行为。  
  3. **边界条件**：`presses = 0` 必须单独返回 1；`n = 1`、`n = 2` 时状态数会比 `n ≥ 3` 少，需要在答案表中区分。  

- **下次遇到同类题**，第一步应该先思考：  
  - **按钮/操作是否可以相互抵消（偶数次等于零）？**  
  - **是否存在周期或对称，使得只需关注前几位？**  
  - **利用位掩码把“是否使用”压缩成常数个状态，再枚举即可。**