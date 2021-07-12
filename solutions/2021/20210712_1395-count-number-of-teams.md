# #1395. 计数团队数量 / Count Number of Teams

> 难度：中等 · 标签：Array、Dynamic Programming、Binary Indexed Tree、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/count-number-of-teams/)

---

## 题目（英文原版）

**Description**

There are n soldiers standing in a line. Each soldier is assigned a unique rating value.
You have to form a team of 3 soldiers amongst them under the following rules:
Return the number of teams you can form given the conditions. (soldiers can be part of multiple teams).

**Examples**

**Example 1:**

```
Input: rating = [2,5,3,4,1]
Output: 3
Explanation: We can form three teams given the conditions. (2,3,4), (5,4,1), (5,3,1).
```

**Example 2:**

```
Input: rating = [2,1,3]
Output: 0
Explanation: We can't form any team given the conditions.
```

**Example 3:**

```
Input: rating = [1,2,3,4]
Output: 4
```

**Constraints**

- n == rating.length
- 3 <= n <= 1000
- 1 <= rating[i] <= 105
- All the integers in rating are unique.

---

## 题目（中文翻译）

有 `n` 名士兵站成一条直线。每名士兵都有唯一的评分（rating）值。  
你需要从中选出 3 名士兵组成一个团队，必须满足以下规则：

- 若三名士兵的下标满足 `i < j < k`，则他们的评分要么严格递增（`rating[i] < rating[j] < rating[k]`），要么严格递减（`rating[i] > rating[j] > rating[k]`）。

返回满足条件的团队（team）数量。**同一名士兵可以出现在多个团队中**。

### 示例

**示例 1**  
```text
Input: rating = [2,5,3,4,1]
Output: 3
Explanation: 可以组成以下三个满足条件的团队：(2,3,4), (5,4,1), (5,3,1)。
```

**示例 2**  
```text
Input: rating = [2,1,3]
Output: 0
Explanation: 没有任何满足条件的团队。
```

**示例 3**  
```text
Input: rating = [1,2,3,4]
Output: 4
```

### 约束条件

- `n == rating.length`
- `3 <= n <= 1000`
- `1 <= rating[i] <= 10^5`
- `rating` 中的所有整数互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把所有可能的 3‑人组合都枚举一遍，然后检查它们是否满足题目给出的“递增”或“递减”规则。  
- **数据结构**：这里只需要用到普通的 Python 列表，和三个下标 `i、j、k` 来指向三名士兵。可以把它想象成在排队的孩子里随意挑选三个位置，看看他们的身高是先升后降还是先降后升。  
- **正确性**：只要遍历了 **所有** `i < j < k` 的组合，就不会漏掉任何合法的队伍；每次判断 `rating[i] < rating[j] < rating[k]`（递增）或 `rating[i] > rating[j] > rating[k]`（递减）即可。  
- **时间/空间复杂度**：三层循环的时间复杂度是 `O(n³)`，因为每层最多遍历 `n` 次。空间只用到常数级的变量，故为 `O(1)`。

> **大白话**：`O(n³)` 就好比你有 1000 个人，要把他们每三个人一组地全部尝试一次，次数大约是 1000 × 1000 × 1000 ≈ **10⁹**，在电脑里会非常慢。

#### 代码（Python）

```python
def numTeams(rating):
    n = len(rating)
    ans = 0
    # i < j < k 三重循环，枚举所有三元组
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                # 递增的情况
                if rating[i] < rating[j] < rating[k]:
                    ans += 1
                # 递减的情况
                elif rating[i] > rating[j] > rating[k]:
                    ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n³)` —— 每次都要检查所有三元组合，随着 `n` 增大，运行时间呈立方增长。  
- **空间复杂度**：`O(1)` —— 只用了几个计数变量和循环下标，不随输入规模增长而增加内存。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于 **三层循环**，我们可以把它压缩成 **两层循环**，甚至 **一层循环 + 前缀计数**。核心观察：

1. **把中间的士兵 `j` 固定**。  
   - 若想组成递增队伍，需要左边有比 `rating[j]` 小的士兵（记作 `leftLess`），右边有比 `rating[j]` 大的士兵（记作 `rightGreater`）。这两部分可以任选一个组合，形成 `leftLess * rightGreater` 支递增队伍。  
   - 若想组成递减队伍，需要左边比 `rating[j]` 大的士兵（`leftGreater`），右边比 `rating[j]` 小的士兵（`rightLess`），共 `leftGreater * rightLess` 支递减队伍。

2. **如何快速得到这些计数**？  
   - 对每个位置 `j`，遍历左侧一次，统计比 `rating[j]` 小/大的个数 → `leftLess`、`leftGreater`。  
   - 同理遍历右侧一次，得到 `rightLess`、`rightGreater`。  
   - 这一步的实现只需要 **两层循环**（外层遍历 `j`，内层遍历左/右侧），整体时间 `O(n²)`，空间 `O(1)`（只用几个计数变量）。

3. **进一步优化（可选）**  
   - 如果 `n` 可能达到 10⁵，`O(n²)` 仍然太慢。可以使用 **树状数组（Binary Indexed Tree，BIT）** 或 **线段树** 在 `O(log n)` 时间内查询“小于”或“大于” 的数量，整体降到 `O(n log n)`。这里我们先给出 `O(n²)` 的实现，因为题目限制 `n ≤ 1000`，已经足够快，而且概念更易理解。

> **类比**：把 `j` 看成一根木棍，左边的士兵是左岸的石子，右边的士兵是右岸的石子。我们只需要统计左岸比木棍矮的石子有多少、比木棍高的有多少，右岸同理，然后把两岸的符合条件的石子配对即可。

#### 代码（Python）

```python
def numTeams(rating):
    n = len(rating)
    ans = 0

    # 枚举中间士兵的位置 j
    for j in range(1, n - 1):
        left_less = left_greater = 0   # 左侧比 rating[j] 小 / 大 的数量
        right_less = right_greater = 0 # 右侧比 rating[j] 小 / 大 的数量

        # 统计左侧
        for i in range(j):
            if rating[i] < rating[j]:
                left_less += 1
            else:  # rating[i] > rating[j] （题目保证唯一）
                left_greater += 1

        # 统计右侧
        for k in range(j + 1, n):
            if rating[k] > rating[j]:
                right_greater += 1
            else:  # rating[k] < rating[j]
                right_less += 1

        # 递增队伍 + 递减队伍
        ans += left_less * right_greater      # 小 < 中 < 大
        ans += left_greater * right_less      # 大 > 中 > 小

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 外层遍历 `j`（`n` 次），内层分别遍历左侧和右侧（每次最多 `n`），所以总操作数约为 `n·n/2`，即平方级增长。相比 `O(n³)`，当 `n=1000` 时运行时间从 **10⁹** 次降到 **10⁶** 次，瞬间可接受。  
- **空间复杂度**：`O(1)` —— 只用了若干计数变量，和输入规模无关。

> 若想进一步把时间降到 `O(n log n)`，可以把左侧/右侧的 “小于 / 大于” 计数交给 **树状数组** 完成。思路是：从左到右遍历，用 BIT 记录已经出现的 rating，查询 `rating[j]` 左侧比它小的数量；再从右到左做一次类似的查询，组合即可。这里不展开实现细节，以免增加初学者负担。

---

## 心得

- **核心技巧**：把三元组的判断拆成 “固定中间元素 + 统计左右两侧满足条件的元素个数”，利用乘法把配对数直接算出来。  
- **适用的相似题型**  
  1. **LeetCode 1395 – Count Number of Teams**（本题本身）  
  2. **LeetCode 274 – H‑Index**（需要统计左侧/右侧满足阈值的元素）  
  3. **LeetCode 2405 – Optimal Partition of String**（利用前缀计数快速判断）  
- **一句话总结**：**“把三人组合的搜索空间压缩到‘中间 + 左右计数’”，就是解这类‘顺序约束’题的钥匙。**

---

## 反思

- **拿到题目第一反应**：直接写三层循环穷举，确保能通过所有样例。  
- **最容易踩的坑**  
  - 忘记统计递增和递减两种情况，只算了一种会导致答案缺失。  
  - 边界条件：`j` 不能取到最左或最右，否则左侧或右侧没有元素会导致计数错误。  
  - 题目保证 rating 唯一，若忽略这一点，`else` 分支需要写成 `elif rating[i] > rating[j]`，否则会把相等的情况误算进去（在本题不存在，但养成严谨写法的好习惯）。  
- **下次遇到同类题**：第一步先思考 “能否固定一个位置”，然后统计左右两侧满足条件的元素数量；如果数据规模更大，再考虑使用 BIT/线段树把统计过程加速到 `O(log n)`。