# #2483. **商店的最小罚金** / Minimum Penalty for a Shop

> 难度：中等 · 标签：String、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-penalty-for-a-shop/)

---

## 题目（英文原版）

**Description**

You are given the customer visit log of a shop represented by a 0-indexed string customers consisting only of characters 'N' and 'Y':
If the shop closes at the jth hour (0 <= j <= n), the penalty is calculated as follows:
Return the earliest hour at which the shop must be closed to incur a minimum penalty.
Note that if a shop closes at the jth hour, it means the shop is closed at the hour j.

**Examples**

**Example 1:**

```
Input: customers = "YYNY"
Output: 2
Explanation: 
- Closing the shop at the 0th hour incurs in 1+1+0+1 = 3 penalty.
- Closing the shop at the 1st hour incurs in 0+1+0+1 = 2 penalty.
- Closing the shop at the 2nd hour incurs in 0+0+0+1 = 1 penalty.
- Closing the shop at the 3rd hour incurs in 0+0+1+1 = 2 penalty.
- Closing the shop at the 4th hour incurs in 0+0+1+0 = 1 penalty.
Closing the shop at 2nd or 4th hour gives a minimum penalty. Since 2 is earlier, the optimal closing time is 2.
```

**Example 2:**

```
Input: customers = "NNNNN"
Output: 0
Explanation: It is best to close the shop at the 0th hour as no customers arrive.
```

**Example 3:**

```
Input: customers = "YYYY"
Output: 4
Explanation: It is best to close the shop at the 4th hour as customers arrive at each hour.
```

**Constraints**

- 1 <= customers.length <= 105
- customers consists only of characters 'Y' and 'N'.

---

## 题目（中文翻译）

你得到一家商店的顾客访问日志，用仅包含字符 `'N'` 和 `'Y'` 的 0 索引字符串 `customers` 表示，其中  
- `'Y'` 表示该小时有顾客到来（customer arrives），  
- `'N'` 表示该小时没有顾客到来（no customer）。

如果商店在第 `j` 小时关闭（`0 ≤ j ≤ n`，其中 `n = customers.length`），则罚金（penalty）计算方式如下：

- 对于 **关闭前**（即第 `0` 小时到第 `j‑1` 小时）商店开放但没有顾客的每个小时，累计 `1` 的罚金（即统计 `customers[0..j‑1]` 中的 `'N'` 个数）。  
- 对于 **关闭后**（即第 `j` 小时到第 `n‑1` 小时）商店已关闭但仍有顾客到来的每个小时，累计 `1` 的罚金（即统计 `customers[j..n‑1]` 中的 `'Y'` 个数）。

返回使罚金最小的 **最早** 关闭时间 `j`。  
注意，关闭在第 `j` 小时意味着第 `j` 小时本身已经是关闭状态。

---

### 示例

**示例 1**  
```text
Input: customers = "YYNY"
Output: 2
Explanation:
- 在第 0 小时关闭的罚金为 1+1+0+1 = 3
- 在第 1 小时关闭的罚金为 0+1+0+1 = 2
- 在第 2 小时关闭的罚金为 0+0+0+1 = 1
- 在第 3 小时关闭的罚金为 0+0+1+1 = 2
- 在第 4 小时关闭的罚金为 0+0+1+0 = 1
最小罚金为 1，出现于第 2 小时和第 4 小时，取最早的第 2 小时。
```

**示例 2**  
```text
Input: customers = "NNNNN"
Output: 0
Explanation: 关闭在第 0 小时最优，因为整段时间都没有顾客到来，罚金为 0。
```

**示例 3**  
```text
Input: customers = "YYYY"
Output: 4
Explanation: 关闭在第 4 小时最优，因为每个小时都有顾客到来，只有在全部关闭后才不会产生 “关闭后有顾客到来” 的罚金。
```

---

### 约束

- `1 ≤ customers.length ≤ 10^5`
- `customers` 只由字符 `'Y'` 和 `'N'` 组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**遍历所有可能的关店时间 `j`（从 0 到 n），分别计算在每个 `j` 下的罚金，最后取最小的那个**。  

- **数据结构**：我们只需要遍历字符串本身，逐个字符检查它是 `'Y'`（有顾客）还是 `'N'`（没有顾客）。可以把字符串想象成一排时间点的灯，`'Y'` 表示灯亮（有顾客），`'N'` 表示灯灭（没顾客）。  
- **罚金计算**：  
  - 关店时间 `j` 之前（`0 … j-1`）如果出现 `'N'`，说明本来可以省下这段时间的营业成本，但我们却在关店前仍然开着，**每出现一次 `'N'` 罚 1 分**。  
  - 关店时间 `j` 及以后（`j … n-1`）如果出现 `'Y'`，说明关店后还有顾客想来，**每出现一次 `'Y'` 也罚 1 分**。  
- **正确性**：因为罚金的定义就是上述两类情况的数量之和，遍历所有 `j` 并逐个计算，就一定能得到最小的罚金及对应的最早时间。  

- **时间/空间复杂度**：  
  - 对每个 `j`（共 `n+1` 个）我们都要重新遍历整个字符串来统计 `'N'` 和 `'Y'`，所以时间是 `O((n+1) * n) ≈ O(n²)`。  
  - 只用了常数级的额外变量（计数器），空间是 `O(1)`。  

> **大白话**：如果你把每一次重新计数想象成一次“从头数数”，那你会对每个可能的关店时间都重新数一遍，这就像在跑 1000 米的赛道上，每走一步都回到起点重新跑一遍，显然很慢。

#### 代码（Python）

```python
def bestClosingTime_bruteforce(customers: str) -> int:
    n = len(customers)
    best_hour = 0          # 记录最小罚金对应的最早时间
    min_penalty = float('inf')   # 初始设为无限大

    # j 表示关店的时刻，范围是 0~n（包括 n，表示一直营业到最后一小时后才关）
    for j in range(n + 1):
        penalty = 0

        # 统计 j 之前的 N（营业期间的空闲）
        for i in range(j):
            if customers[i] == 'N':
                penalty += 1

        # 统计 j 之后的 Y（关店后仍有顾客）
        for i in range(j, n):
            if customers[i] == 'Y':
                penalty += 1

        # 更新最小罚金和对应的时间
        if penalty < min_penalty:
            min_penalty = penalty
            best_hour = j
        # 若相同罚金，保持最早的时间（因为我们是从小到大遍历的，所以不需要额外处理）

    return best_hour
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 对每个可能的关店时间都要遍历整个字符串一次。  
- **空间复杂度**：`O(1)` —— 只用了几个整数计数器，和输入规模无关。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历字符串**，导致二次循环。我们可以把 **“前缀的 N 数量”** 与 **“后缀的 Y 数量”** 预先算好，后面只需要 **常数时间** 就能得到任意 `j` 的罚金。  

1. **前缀和（Prefix Sum）**  
   - 定义 `preN[i]` 为下标 `[0, i)`（左闭右开）区间内 `'N'` 的个数。  
   - 这相当于把每个字符看成一本字典的页码：遇到 `'N'` 就在字典里记 1，遇到 `'Y'` 记 0，`preN[i]` 就是前 `i` 页的总和。  

2. **后缀和（Suffix Sum）**  
   - 定义 `sufY[i]` 为下标 `[i, n)` 区间内 `'Y'` 的个数。  
   - 这相当于从右边往左数，每遇到 `'Y'` 加 1，`sufY[i]` 就是从 `i` 开始一直到最后的总和。  

3. **一次遍历得到所有罚金**  
   - 对任意关店时间 `j`，罚金 = `preN[j]`（在 `j` 之前的空闲） + `sufY[j]`（在 `j` 之后的顾客）。  
   - 只要我们已经有了 `preN` 与 `sufY`，就可以在 **O(1)** 时间内算出每个 `j` 的罚金，遍历 `j` 一次即可得到最小值。  

4. **一步到位的实现**  
   - 其实我们不需要完整的两个数组，只要在一次遍历中维护当前的 `preN` 与 `sufY` 即可。  
   - 先统计整个字符串中 `'Y'` 的总数 `totalY`（这相当于 `sufY[0]`）。  
   - 然后从左到右扫描：  
     - `preN` 随着遇到 `'N'` 增加。  
     - `sufY` 随着离开当前位置（即把当前字符从后缀中移除）而减少，如果当前字符是 `'Y'`。  
   - 此时 `penalty = preN + sufY` 正好对应关店时间 `j`（当前扫描到的下标即为 `j`）。  

> **类比**：想象你在一本书的左侧贴了“空闲页”标签（对应 `'N'`），右侧贴了“有顾客页”标签（对应 `'Y'`）。一次走遍全书，你可以边走边把左侧的空闲页数累计到 `preN`，同时把右侧的有顾客页数从总数中减掉，得到右侧剩余的有顾客页数 `sufY`。每一步的两数相加，就是在该位置关店的罚金。

#### 代码（Python）

```python
def bestClosingTime(customers: str) -> int:
    n = len(customers)

    # 1) 先算出整个字符串中 Y 的总数，等价于后缀和 sufY[0]
    totalY = customers.count('Y')

    preN = 0          # 左侧 N 的累计个数，等价于 preN[j]
    sufY = totalY     # 右侧 Y 的剩余个数，等价于 sufY[j]
    best_hour = 0
    min_penalty = preN + sufY   # j = 0 时的罚金

    # 依次把关店时间 j 移动到下一个位置（j 从 0 逐渐增到 n）
    for j in range(1, n + 1):
        # 当前扫描到的字符是 customers[j-1]（因为 j 表示关店时刻在该字符之后）
        ch = customers[j - 1]

        # 先把该字符从后缀中移除
        if ch == 'Y':
            sufY -= 1          # 右侧的 Y 少了一个

        # 再把该字符加入左侧前缀统计
        if ch == 'N':
            preN += 1          # 左侧的 N 多了一个

        # 计算当前 j 的罚金
        penalty = preN + sufY

        # 若找到更小的罚金，更新答案；相同罚金保留最早的 j（因为遍历是递增的）
        if penalty < min_penalty:
            min_penalty = penalty
            best_hour = j

    return best_hour
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历字符串一次，所有计数都是常数时间操作。  
  - 与暴力 `O(n²)` 相比，提升了 **n 倍**，在最坏 10⁵ 长度时也能毫秒级完成。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，未额外开辟与 `n` 相关的数组。

---

## 心得  

- **核心技巧**：前缀和 + 后缀和（或一次遍历同步维护两侧计数）。  
- **适用的题型**  
  1. “最小分割代价” 类题，例如 **Minimum Penalty for a Shop**（本题）。  
  2. “划分数组，使左侧满足某条件，右侧满足另一条件” 的问题，如 **Split Array Largest Sum**（用前缀最大最小）。  
  3. “统计子串/子数组中满足条件的元素数量” 例如 **Number of Subarrays with Bounded Maximum**。  
- **一句话总结解题钥匙**：**把全局信息（如所有 Y 的总数）提前算好，再在一次遍历中同步更新左侧与右侧的计数，任何位置的答案就能在 O(1) 内得到。**

---

## 反思  

- **第一反应**：看到“前缀的 N + 后缀的 Y”，立刻想到枚举所有 `j` 并直接求和，结果是暴力 `O(n²)`。  
- **最容易踩的坑**  
  1. **下标误差**：关店时间 `j` 表示“在第 `j` 小时结束后关闭”，所以在遍历时要注意把字符 `customers[j-1]` 当作刚刚“离开”后缀、加入前缀的元素。  
  2. **边界情况**：`j = 0`（一开始就关）和 `j = n`（营业到最后一小时后才关）必须都被考虑到。  
  3. **相同罚金的最早时间**：因为题目要求返回最早的小时，遍历时一旦发现更小的罚金立即更新，若相同则保持已有的最早 `j`。  
- **下次遇到同类题**：第一步先思考**“能否用一次遍历把左右两侧的信息同步维护？”**，如果答案是肯定的，就尝试写出前缀/后缀计数的递推公式，再实现 O(n) 解。