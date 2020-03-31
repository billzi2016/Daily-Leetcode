# #822. 卡牌翻转游戏 / Card Flipping Game

> 难度：中等 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/card-flipping-game/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays fronts and backs of length n, where the ith card has the positive integer fronts[i] printed on the front and backs[i] printed on the back. Initially, each card is placed on a table such that the front number is facing up and the other is facing down. You may flip over any number of cards (possibly zero).
After flipping the cards, an integer is considered good if it is facing down on some card and not facing up on any card.
Return the minimum possible good integer after flipping the cards. If there are no good integers, return 0.

**Examples**

**Example 1:**

```
Input: fronts = [1,2,4,4,7], backs = [1,3,4,1,3]
Output: 2
Explanation:
If we flip the second card, the face up numbers are [1,3,4,4,7] and the face down are [1,2,4,1,3].
2 is the minimum good integer as it appears facing down but not facing up.
It can be shown that 2 is the minimum possible good integer obtainable after flipping some cards.
```

**Example 2:**

```
Input: fronts = [1], backs = [1]
Output: 0
Explanation:
There are no good integers no matter how we flip the cards, so we return 0.
```

**Constraints**

- n == fronts.length == backs.length
- 1 <= n <= 1000
- 1 <= fronts[i], backs[i] <= 2000

---

## 题目（中文翻译）

**描述**  
给定两个下标从 0 开始的整数数组 `fronts` 和 `backs`，长度均为 `n`。第 `i` 张卡牌正面（front）上印有正整数 `fronts[i]`，背面（back）上印有 `backs[i]`。最初所有卡牌都放在桌面上，正面朝上，背面朝下。你可以翻转任意数量的卡牌（也可以不翻转）。  

翻转卡牌后，如果某个整数 **好整数（good integer）** 满足：它在至少一张卡牌的背面朝下出现，而在所有卡牌的正面都没有出现，则称该整数为好整数。返回翻转卡牌后可能得到的最小的好整数。如果不存在好整数，返回 `0`。  

**示例**  

示例 1:  
```
Input: fronts = [1,2,4,4,7], backs = [1,3,4,1,3]
Output: 2
Explanation:
如果翻转第二张卡牌，正面朝上的数字变为 [1,3,4,4,7]，背面朝下的数字为 [1,2,4,1,3]。  
2 是最小的好整数，因为它只出现在背面而没有出现在正面。  
可以证明，在所有可能的翻转方案中，2 是能够得到的最小好整数。
```

示例 2:  
```
Input: fronts = [1], backs = [1]
Output: 0
Explanation:
无论如何翻转卡牌，都不存在好整数，因此返回 0。
```

**约束条件**  
- `n == fronts.length == backs.length`  
- `1 <= n <= 1000`  
- `1 <= fronts[i], backs[i] <= 2000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一张卡片的“翻面或不翻面”这两种状态全部列举出来。  
- 对于第 `i` 张卡片，有两种选择：**不翻**（正面 `fronts[i]` 朝上，背面 `backs[i]` 朝下）或**翻**（正面 `backs[i]` 朝上，背面 `fronts[i]` 朝下）。  
- 把所有卡片的选择组合起来，就得到 `2ⁿ` 种可能的摆放方式（`n` 为卡片数），相当于把每张卡片的状态写成一个二进制位。  

对每一种摆放方式，我们可以：
1. 收集所有**正面朝上**的数字（记作 `up_set`）。  
2. 收集所有**背面朝下**的数字（记作 `down_set`）。  
3. 找出在 `down_set` 中但不在 `up_set` 中的数字，这些就是“好整数”。  
4. 取这些好整数的最小值，更新全局答案。  

如果遍历完所有 `2ⁿ` 种情况仍然没有好整数，答案就是 `0`。

> **类比**：把每张卡片想象成一个开关，开关向左是“不翻”，向右是“翻”。要找出所有可能的开关组合，就像把所有灯的开关一次次全开全关，列出所有灯光的状态。

这个方法一定能得到正确答案，因为它把**所有**合法的翻卡方式都枚举了，必然不会漏掉最优解。

#### 代码（Python）

```python
from itertools import product
from typing import List

def flipgame_bruteforce(fronts: List[int], backs: List[int]) -> int:
    n = len(fronts)
    best = float('inf')                     # 用正无穷表示目前找到的最小好整数

    # product 会产生 0/1 的笛卡尔积，0 代表不翻，1 代表翻
    for mask in product([0, 1], repeat=n):
        up_set = set()      # 正面朝上的数字集合
        down_set = set()    # 背面朝下的数字集合

        for i, flip in enumerate(mask):
            if flip == 0:               # 不翻
                up_set.add(fronts[i])
                down_set.add(backs[i])
            else:                       # 翻
                up_set.add(backs[i])
                down_set.add(fronts[i])

        # 找出好整数：在 down_set 中但不在 up_set 中
        for num in down_set:
            if num not in up_set:
                best = min(best, num)

    return 0 if best == float('inf') else best
```

#### 复杂度  

- **时间复杂度**：`O(2ⁿ * n)`  
  解释：我们需要遍历 `2ⁿ` 种翻卡组合（指数级），每种组合要遍历 `n` 张卡片收集数字，所以整体是指数时间。  
- **空间复杂度**：`O(n)`  
  解释：`up_set`、`down_set` 最多各存 `n` 个数字，除此之外只用常数级额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有翻卡组合**，这一步完全没有利用题目给出的关键信息。  
观察题目可以得到下面的**重要规律**：

> **如果某个数字同时出现在同一张卡片的正反面，那么无论我们怎么翻，这张卡片的正面（朝上）上必然会出现这个数字。**  
> 换句话说，这类数字**永远不可能成为好整数**，因为它一定会在 “正面朝上” 的集合里出现。

因此，只要把所有“在同一张卡片两面都出现的数字”标记为 **坏数字**（`bad`），其余出现过的数字都是**潜在的好整数**。  
最终答案就是这些潜在好整数中的最小值（如果没有则返回 `0`）。

实现步骤：

1. **遍历所有卡片**，如果 `fronts[i] == backs[i]`，把这个数字加入集合 `bad`。这一步的时间是 `O(n)`。  
2. **再次遍历两数组**，把所有出现过的数字（不论在正面还是背面）放进集合 `candidates`。  
3. 对 `candidates` 中的每个数字，若它 **不在 `bad`**，说明它有可能成为好整数，更新最小值 `ans`。  
4. 若 `ans` 仍为正无穷，说明不存在好整数，返回 `0`；否则返回 `ans`。

> **类比**：把每张卡片想象成一本双面字典，正面是“正面词条”，背面是“背面词条”。如果某个词条在同一本字典的两页都出现，那么无论我们怎么翻这本字典，这个词必定在“正面页”。只有那些从未在同一本字典的两页同时出现的词，才有机会只在“背面页”出现，从而成为好整数。

#### 代码（Python）

```python
from typing import List

def flipgame_optimal(fronts: List[int], backs: List[int]) -> int:
    n = len(fronts)
    bad = set()          # 记录“同一张卡片两面都有的数字”，这些数字不可能是好整数

    # 第一步：找出所有坏数字
    for i in range(n):
        if fronts[i] == backs[i]:
            bad.add(fronts[i])

    ans = float('inf')   # 用正无穷表示当前找到的最小好整数

    # 第二步：遍历所有出现过的数字，挑选不在 bad 集合里的最小值
    for num in fronts + backs:   # 把两数组合在一起遍历即可
        if num not in bad:
            ans = min(ans, num)

    return 0 if ans == float('inf') else ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  解释：我们只遍历了两次数组（各 `n` 次），每次操作都是常数时间，所以整体是线性时间。相比暴力的指数时间快了许多。  
- **空间复杂度**：`O(n)`  
  解释：集合 `bad` 最多存放 `n` 个数字（最坏情况每张卡片正反面相同），其余变量都是常数级。

---

## 心得

- 这道题考察的核心技巧是 **“排除法”**：先把一定不可能成为答案的元素剔除，再在剩余元素中寻找最优解。  
- 该技巧适用于类似题目，例如  
  1. **"Find the Smallest Good Number"**（在数组中找既不在某集合中也不在另一集合中的最小数）。  
  2. **"Lucky Numbers in Matrix"**（矩阵中某行/列同时出现的数需要排除）。  
  3. **"Minimum Uncovered Integer"**（在两组集合的交集中找最小未出现的数）。  
- **一句话总结解题钥匙**：先找出“永远会出现在正面”的数字（同卡正反相同），剩下的最小值就是答案。

## 反思

- **第一反应**：直接想到枚举所有翻转方式，想用暴力搜索得到答案。  
- **最容易踩的坑**：忽略了“同一张卡片两面相同的数字永远会在正面”。如果不排除这些数字，后面的最小值判断会出错。  
- **下次遇到同类题**，第一步应该先**分析哪些元素必然会出现在限制条件中**（比如必在正面、必在集合等），把它们标记为“坏”，再在剩余候选中寻找最优解。这样可以把时间复杂度从指数级降到线性级。