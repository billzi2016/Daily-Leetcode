# #605. 能否种植花朵 / Can Place Flowers

> 难度：简单 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/can-place-flowers/)

---

## 题目（英文原版）

**Description**

You have a long flowerbed in which some of the plots are planted, and some are not. However, flowers cannot be planted in adjacent plots.
Given an integer array flowerbed containing 0's and 1's, where 0 means empty and 1 means not empty, and an integer n, return true if n new flowers can be planted in the flowerbed without violating the no-adjacent-flowers rule and false otherwise.

**Examples**

**Example 1:**

```
Input: flowerbed = [1,0,0,0,1], n = 1
Output: true
```

**Example 2:**

```
Input: flowerbed = [1,0,0,0,1], n = 2
Output: false
```

**Constraints**

- 1 <= flowerbed.length <= 2 * 104
- flowerbed[i] is 0 or 1.
- There are no two adjacent flowers in flowerbed.
- 0 <= n <= flowerbed.length

---

## 题目（中文翻译）

你有一条很长的花坛（flowerbed），其中一些格子已经种植了花，一些格子为空。然而，**相邻格子（adjacent plots）**不能同时种植花。

给定一个只包含 `0` 和 `1` 的整数数组 `flowerbed`，其中 `0` 表示空格，`1` 表示已种植花，以及一个整数 `n`。如果可以在不违反“相邻格子不能种花”规则的前提下，再种植 `n` 株新花，则返回 `true`，否则返回 `false`。

示例 1:
```text
Input: flowerbed = [1,0,0,0,1], n = 1
Output: true
```

示例 2:
```text
Input: flowerbed = [1,0,0,0,1], n = 2
Output: false
```

约束条件：
- `1 <= flowerbed.length <= 2 * 10^4`
- `flowerbed[i]` 为 `0` 或 `1`。
- `flowerbed` 中不存在两个相邻的已种花格子。
- `0 <= n <= flowerbed.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐个遍历**花坛的每个位置，看到 `0`（空位）就判断左边和右边是否都是 `0`（或者是边界），如果满足条件就“种一朵花”。  
- **数据结构**：只需要原始的列表 `flowerbed`，相当于我们手里的一排格子。把列表想象成一条街道，`1` 表示已经有房子（花），`0` 表示空地。我们要在空地上建房子，但相邻的两栋房子之间必须留出一个空地，就像 **哈希表** 的“键-值”对应关系一样，`flowerbed[i]` 是我们查询的“键”，返回的是该位置是否已占用（值）。
- **为什么正确**：因为我们一次只检查当前格子以及它左右两侧的格子，只有当左右都没有花时才种花，这正好满足“相邻格子不能都有花”的约束。遍历完整个列表后，如果已经种了 `n` 朵花，就说明可以满足要求。
- **时间/空间复杂度**：  
  - 时间：我们要 **一次遍历** 整个列表，最坏情况下要检查每个位置的左右两侧，所以是 `O(m)`（`m` 为 `flowerbed` 长度）。如果在遍历过程中每次都要检查左右两侧的值，这仍然是线性的，因为每个位置的检查次数是常数次。  
  - 空间：只使用了常数级的额外变量（计数器、索引），所以是 `O(1)`。

> 大白话解释：`O(m)` 就相当于“跟花坛里格子的数量成正比”，格子越多，花园里走一遍的时间就越长。`O(1)` 表示我们不需要额外的大盒子来装东西，只有几个小纸条记录计数。

#### 代码（Python）

```python
def canPlaceFlowers_bruteforce(flowerbed, n):
    """
    暴力遍历整个花坛，逐个尝试种花
    :param flowerbed: List[int]，0 表示空位，1 表示已有花
    :param n: int，需要种的花的数量
    :return: bool，是否可以种下 n 朵花
    """
    count = 0                     # 已经种下的花的数量
    m = len(flowerbed)

    for i in range(m):
        if flowerbed[i] == 0:                     # 当前格子是空的
            left_empty = (i == 0) or (flowerbed[i - 1] == 0)   # 左侧要么是边界，要么也是空
            right_empty = (i == m - 1) or (flowerbed[i + 1] == 0) # 右侧同理

            if left_empty and right_empty:        # 左右都空，才能种花
                flowerbed[i] = 1                  # 把这格设为已种花，防止后面再种
                count += 1
                if count >= n:                     # 已经种够了，提前返回
                    return True

    return count >= n   # 遍历完后检查是否种够
```

#### 复杂度

- **时间复杂度**：`O(m)` —— 需要遍历一次花坛，格子越多，花园里走一遍的时间就越长。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（`count、i`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**遍历**是不可避免的，但我们可以**不必真正修改原数组**，也可以**一次遍历就直接算出最多能种多少朵花**，从而提前判断是否满足 `n`。  
- **慢在哪里**：暴力解每次种花后都把 `flowerbed[i]` 设为 `1`，这一步虽然不会改变复杂度，但在思考时会让人纠结“后面的格子会不会受到影响”。另外，一旦种了 `n` 朵花我们才会提前返回，否则会一直遍历到结尾。
- **优化思路**：我们只需要 **统计** 在不破坏相邻规则的前提下，**最多** 能在花坛里种多少朵花。只要这个最大可能数 `maxPlace` 大于等于 `n`，答案就是 `True`。  
  - 对于连续的 `0` 段（比如 `0000`），如果两端都是边界或已有花 `1`，可以种的花的数量是 `ceil(len/2) - 1`（中间留一个空位）。更直观的做法是**模拟种花**但不真正改动数组：  
    - 当我们看到 `0`，检查左侧是否为 `0`（或左边界）且右侧是否为 `0`（或右边界），如果满足，就“种一朵”，计数器 `count += 1`，并**跳过**下一个格子（因为相邻格子必须空）。  
- **核心算法**：**贪心**（Greedy）——每次看到可以种花的位置，就立刻种下，这样可以保证种的数量最多。因为种花只会占用当前格子和它左右的空位，后面的决定不受影响。  
- **类比**：想象你在一条长凳上摆放杯子，杯子之间必须留一个空位。每当你看到一段连续的空位时，你就把杯子放在最左边的空位，然后跳过下一个位置，这样可以放下最多的杯子。

#### 代码（Python）

```python
def canPlaceFlowers(flowerbed, n):
    """
    贪心一次遍历，统计最多可以种多少朵花
    :param flowerbed: List[int]
    :param n: int
    :return: bool
    """
    count = 0                     # 已经种下的花的数量
    i = 0
    m = len(flowerbed)

    while i < m:
        if flowerbed[i] == 0:                     # 当前格子为空
            left_empty = (i == 0) or (flowerbed[i - 1] == 0)   # 左侧空或是左边界
            right_empty = (i == m - 1) or (flowerbed[i + 1] == 0) # 右侧空或是右边界

            if left_empty and right_empty:        # 两侧都空，能种花
                count += 1
                if count >= n:                     # 已经满足需求，直接返回
                    return True
                i += 2      # 跳过下一个格子，因为相邻位置必须空
                continue

        i += 1          # 当前不能种花，继续检查下一个格子

    return count >= n   # 遍历结束后比较
```

#### 复杂度

- **时间复杂度**：`O(m)` —— 只需一次线性扫描，`m` 为花坛长度。与暴力解相同的遍历次数，但没有不必要的写操作，且在种够 `n` 朵时可以提前结束。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量 (`count, i, m`)，不随输入规模增长。

---

## 心得

- **核心技巧**：**贪心**——在满足局部约束的前提下立即做出最优选择（这里是“只要可以种，就立刻种”），能够得到全局最优解。  
- **适用的题型**：  
  1. “Maximum Number of K‑Consecutive Ones” 类似的“在数组里插入/删除元素但要满足相邻约束”。  
  2. “Boats to Save People”——每次尽可能让两个人同船（局部最优）。  
  3. “Candy Distribution”——从左到右贪心分配糖果。  
- **一句话总结**：只要左、右都是空位，就立刻种花，跳过下一个格子——这就是解这道题的钥匙。

## 反思

- **第一反应**：看到“不能相邻”，立刻想到遍历检查左右两侧是否为空，符合直觉的暴力思路。  
- **最容易踩的坑**：  
  - **边界条件**：数组开头和结尾没有左/右邻居，需要特殊判断 (`i == 0` 或 `i == m-1`)。  
  - **跳过位置**：种完花后如果不跳过下一个格子，后面可能错误地再次种花，导致相邻。  
  - **提前返回**：如果 `n` 为 0，应该直接返回 `True`；如果在遍历中已经种够 `n` 朵，应立即返回，避免不必要的遍历。  
- **下次类似题**：第一步先**明确局部约束**（如相邻不能冲突），再**尝试一次线性扫描**，在满足局部约束时立即做决定（贪心），并注意处理数组的**边界**和**跳过**策略。