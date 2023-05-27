# #2260. 最少连续抽取的卡牌数 / Minimum Consecutive Cards to Pick Up

> 难度：中等 · 标签：Array、Hash Table、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/minimum-consecutive-cards-to-pick-up/)

---

## 题目（英文原版）

**Description**

You are given an integer array cards where cards[i] represents the value of the ith card. A pair of cards are matching if the cards have the same value.
Return the minimum number of consecutive cards you have to pick up to have a pair of matching cards among the picked cards. If it is impossible to have matching cards, return -1.

**Examples**

**Example 1:**

```
Input: cards = [3,4,2,3,4,7]
Output: 4
Explanation: We can pick up the cards [3,4,2,3] which contain a matching pair of cards with value 3. Note that picking up the cards [4,2,3,4] is also optimal.
```

**Example 2:**

```
Input: cards = [1,0,5,3]
Output: -1
Explanation: There is no way to pick up a set of consecutive cards that contain a pair of matching cards.
```

**Constraints**

- 1 <= cards.length <= 105
- 0 <= cards[i] <= 106

---

## 题目（中文翻译）

给定一个整数数组 `cards`，其中 `cards[i]` 表示第 *i* 张卡牌的数值。如果两张卡牌的数值相同，则它们构成一对匹配卡牌（matching pair）。  
返回必须连续抽取的最少卡牌数量，使得在抽取的卡牌中至少存在一对匹配卡牌。如果不存在任何匹配卡牌的可能，返回 `-1`。

**示例 1**  
Input: `cards = [3,4,2,3,4,7]`  
Output: `4`  
Explanation: 我们可以抽取卡牌 `[3,4,2,3]`，其中包含数值为 `3` 的一对匹配卡牌。注意，抽取卡牌 `[4,2,3,4]` 也同样是最优解。

**示例 2**  
Input: `cards = [1,0,5,3]`  
Output: `-1`  
Explanation: 没有办法抽取一段连续的卡牌使其中出现匹配卡牌对。

**约束条件**  
- `1 <= cards.length <= 10^5`  
- `0 <= cards[i] <= 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**枚举所有可能的连续子数组**，检查每个子数组里是否出现了相同的数字。如果出现，就记录该子数组的长度，最后取最小的长度。  

- **数据结构**：只需要一个普通的 Python 列表 `cards`，以及在检查子数组时使用的集合 `seen`（相当于把 “已经看到的卡片” 当成一本小字典，查找是否已经出现过，和查字典的原理一样）。  
- **正确性**：因为我们遍历了 **所有** 连续区间，只要存在满足条件的区间，就一定会被找到，取最小值自然就是答案。  
- **时间/空间复杂度**：  
  - 外层循环遍历起始位置 `i`，内层循环遍历结束位置 `j`，两层相乘相当于 `n × n`，所以时间复杂度是 **O(n²)**。可以把它想象成在一张 100×100 的表格里逐格检查，随着 `n` 增大，检查的格子会成平方增长。  
  - 集合 `seen` 最多存放 `n` 个元素，空间复杂度是 **O(n)**（最坏情况需要记住整个数组的所有值）。

#### 代码（Python）  
```python
def minimumCardPickup_bruteforce(cards):
    n = len(cards)
    ans = float('inf')                     # 用正无穷表示“还没有找到答案”

    # 枚举所有可能的左端点 i
    for i in range(n):
        seen = set()                        # 用集合记录区间 [i, j] 内出现过的卡片
        # 枚举所有可能的右端点 j（必须 >= i）
        for j in range(i, n):
            if cards[j] in seen:            # 如果当前卡片已经在区间里出现过
                ans = min(ans, j - i + 1)   # 更新最小长度，+1 是因为长度是下标差+1
                break                       # 已经找到匹配，继续尝试下一个左端点
            seen.add(cards[j])              # 把新卡片加入集合

    return -1 if ans == float('inf') else ans
```

#### 复杂度  
- **时间复杂度**：O(n²) — 需要检查所有 `i, j` 组合，随着 `n` 增大，耗时会呈二次方增长。  
- **空间复杂度**：O(n) — 最坏情况下集合 `seen` 会存满整段子数组的所有不同元素。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈在于重复遍历同一个区间**。其实我们只需要知道每个数字上一次出现的位置，就能直接算出最近一次匹配的区间长度，而不必枚举所有子数组。  

1. **记录上一次出现的位置**：使用哈希表（Python 的 `dict`），键是卡片的数值，值是该数值最近一次出现的下标。哈希表就像一本“查字典”，给定卡片的值可以 **O(1)** 时间直接找到它上次出现在哪。  
2. **遍历一次数组**：从左到右遍历 `cards`，对每个 `cards[i]`：  
   - 如果它已经在哈希表里出现过（说明之前有相同的卡片），设上一次出现的下标为 `prev`，则当前区间 `[prev, i]` 包含一对匹配卡片，长度为 `i - prev + 1`。把这个长度和当前的最小答案比较，取较小者。  
   - 然后把哈希表中该数值对应的下标更新为当前下标 `i`（因为以后再出现时，需要以最近一次的位置为基准）。  
3. **遍历结束**：如果找到了至少一次匹配，返回最小长度；否则返回 `-1`。  

**为什么只需要最近一次出现的位置？**  
想象卡片值 `v` 在数组中出现了多次：`... v ... v ... v ...`。如果我们已经记录了最近一次出现的下标 `prev`，那么当前下标 `i` 与 `prev` 之间的距离一定是 **所有可能匹配中最小的**，因为更早的出现位置离 `i` 更远，形成的区间会更长。于是只需要比较最近两次出现即可得到最小答案。

**核心算法**：一次遍历 + 哈希表（相当于“前缀位置映射”），时间 O(n)，空间 O(k)，其中 `k` 是不同卡片值的种类数（最多 `n`）。

#### 代码（Python）  
```python
def minimumCardPickup(cards):
    """
    返回最短的连续子数组长度，使其中至少有一对相同的卡片。
    若不存在则返回 -1。
    """
    last_pos = {}          # 哈希表：卡片值 -> 最近一次出现的下标
    ans = float('inf')     # 用正无穷记录当前最小长度

    for i, val in enumerate(cards):
        if val in last_pos:                     # 之前出现过相同的卡片
            # 计算以最近一次出现为左端点的区间长度
            cur_len = i - last_pos[val] + 1
            ans = min(ans, cur_len)             # 更新最小答案
        # 更新该卡片值的最近出现位置
        last_pos[val] = i

    return -1 if ans == float('inf') else ans
```

#### 复杂度  
- **时间复杂度**：O(n) — 只遍历一次数组，每次查找/更新哈希表都是常数时间。相较于暴力的 O(n²)，速度提升了 **n 倍**。  
- **空间复杂度**：O(k) — 需要保存每个不同卡片值最近出现的下标，最坏情况下 `k = n`，即 O(n)。  

---  

## 心得  

- **核心技巧**：使用哈希表记录“上一次出现的位置”，从而把 **两层循环** 的问题压缩成 **一次遍历**。  
- **适用的题型**：  
  1. “最短子数组满足某种条件”——如 *Minimum Size Subarray Sum*（最小长度满足和 ≥ target）  
  2. “找最近的重复元素”——如 *Shortest Subarray with Sum at Least K*（需要前缀和 + 哈希表）  
  3. “最长无重复子串”——经典的滑动窗口 + 哈希表（LeetCode 3）。  
- **一句话总结解题钥匙**：**把“最近一次出现的位置”记下来，遇到相同元素时直接算区间长度**。  

## 反思  

- **第一反应**：看到“连续子数组”和“出现相同值”，立刻想到滑动窗口或双指针，但其实只要记录上一次出现的位置就能一次遍历完成。  
- **最容易踩的坑**：  
  - 忘记在找到匹配后仍要 **更新** 哈希表，使其指向当前下标，否则后面的匹配会使用过时的左端点，导致答案不最小。  
  - 处理只有一个元素或根本没有重复的情况，需要返回 `-1`，因此要用一个 sentinel（如 `float('inf')`）来判断是否真的找到了答案。  
- **下次类似题的第一步**：先问自己“是否只需要最近一次出现的信息？”如果答案是肯定的，就立刻考虑 **哈希表保存最近位置** 的思路。