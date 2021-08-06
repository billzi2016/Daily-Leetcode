# #1423. 从卡牌中获得的最大分数 / Maximum Points You Can Obtain from Cards

> 难度：中等 · 标签：Array、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/)

---

## 题目（英文原版）

**Description**

There are several cards arranged in a row, and each card has an associated number of points. The points are given in the integer array cardPoints.
In one step, you can take one card from the beginning or from the end of the row. You have to take exactly k cards.
Your score is the sum of the points of the cards you have taken.
Given the integer array cardPoints and the integer k, return the maximum score you can obtain.

**Examples**

**Example 1:**

```
Input: cardPoints = [1,2,3,4,5,6,1], k = 3
Output: 12
Explanation: After the first step, your score will always be 1. However, choosing the rightmost card first will maximize your total score. The optimal strategy is to take the three cards on the right, giving a final score of 1 + 6 + 5 = 12.
```

**Example 2:**

```
Input: cardPoints = [2,2,2], k = 2
Output: 4
Explanation: Regardless of which two cards you take, your score will always be 4.
```

**Example 3:**

```
Input: cardPoints = [9,7,7,9,7,7,9], k = 7
Output: 55
Explanation: You have to take all the cards. Your score is the sum of points of all cards.
```

**Constraints**

- 1 <= cardPoints.length <= 105
- 1 <= cardPoints[i] <= 104
- 1 <= k <= cardPoints.length

---

## 题目（中文翻译）

有若干张卡牌排成一行，每张卡牌都有对应的分数，这些分数存放在整数数组（integer array）`cardPoints` 中。  
在一次操作中，你可以从行的开头或末尾各取走一张卡牌。必须恰好取走 `k` 张卡牌。  
你的得分等于所取卡牌分数的总和。  
给定整数数组 `cardPoints` 和整数 `k`，返回你能够获得的最大得分。

**示例 1**  
```
Input: cardPoints = [1,2,3,4,5,6,1], k = 3
Output: 12
Explanation: 第一步后你的得分必定是 1。但若先取最右侧的卡牌，可以让总得分最大。最优策略是取右侧的三张卡牌，最终得分为 1 + 6 + 5 = 12。
```

**示例 2**  
```
Input: cardPoints = [2,2,2], k = 2
Output: 4
Explanation: 无论取哪两张卡牌，得分始终是 4。
```

**示例 3**  
```
Input: cardPoints = [9,7,7,9,7,7,9], k = 7
Output: 55
Explanation: 必须取走所有卡牌，得分即为所有卡牌分数之和。
```

**约束条件**

- `1 <= cardPoints.length <= 10^5`
- `1 <= cardPoints[i] <= 10^4`
- `1 <= k <= cardPoints.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把「取卡牌」这件事模拟一遍：  
- 每一步可以从左边或右边取走一张卡牌。  
- 需要恰好取 `k` 张，所有可能的取法就是所有「左取 `i` 张、右取 `k‑i` 张」的组合（`i` 从 `0` 到 `k`）。  

我们可以枚举 `i`，把数组前 `i` 个元素和后 `k‑i` 个元素的和算出来，取最大值就是答案。  

> **数据结构类比**  
> 把数组想象成一排排的书，左手只能从左侧的书架取书，右手只能从右侧的书架取书。我们要挑 `k` 本书，最笨的办法就是把「左手取几本」的所有可能都尝试一次。

**为什么这个方法一定对？**  
因为题目只允许「从两端」取卡，任意一次合法的取法必定可以表示为「左取 `i` 张、右取 `k‑i` 张」的形式。遍历所有 `i` 就覆盖了所有合法取法，自然能得到最大分数。

**复杂度分析（大白话）**  
- 对每个 `i`（一共 `k+1` 种）我们都要把对应的前 `i` 张和后 `k‑i` 张加起来，最坏情况下每次都要遍历 `k` 次，所以时间是 **O(k²)**。  
- 只用了常数个额外变量（比如累计和），所以空间是 **O(1)**，不随输入大小增长。

> **O(k²) 的意义**：如果 `k` 是 1000，程序大约会做 1 000 000 次加法；如果 `k` 是 10⁵，次数会涨到 10¹⁰，几乎不可能在合理时间内跑完。

#### 代码（Python）

```python
from typing import List

def maxScore_bruteforce(cardPoints: List[int], k: int) -> int:
    n = len(cardPoints)
    # 前缀和：pre[i] 表示 cardPoints[0:i] 的和（不含 i）
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + cardPoints[i]

    # 后缀和：suf[i] 表示 cardPoints[i:n] 的和（含 i）
    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + cardPoints[i]

    ans = 0
    # 枚举左边取 i 张，右边取 k-i 张
    for i in range(k + 1):
        left_sum = pre[i]                # 前 i 张的和
        right_sum = suf[n - (k - i)]     # 后 k-i 张的和
        ans = max(ans, left_sum + right_sum)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(k²)` —— 两层循环（外层 `k+1` 次，内层累加最多 `k` 次）  
  > 实际上因为我们用了前缀/后缀和，累加变成了 `O(1)`，但若不做预处理，最笨的实现就是 `O(k²)`。这里保留概念上的「暴力」思路。
- **空间复杂度**：`O(n)` —— 前缀和和后缀和各占 `n+1` 的额外数组  
  > 若直接在循环里每次重新求和，则空间是 `O(1)`，但时间会更差。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**关键在于找出左取多少张、右取多少张的最佳组合**。  
暴力枚举的瓶颈是「每次都重新求和」——其实我们可以把「取走的 k 张」转化为「**不取走的** 那段连续子数组」来求。

> **核心观察**  
> 总卡牌分数记为 `total = sum(cardPoints)`。我们必须取走 `k` 张，等价于**留下** `n - k` 张不取。  
> 如果我们找到了 **长度为 `n‑k`、分数最小的子数组**，那么把它留下，其余的卡牌（即 `total - minSubArraySum`）就是我们能得到的最大分数。

这正好可以用 **滑动窗口**（Sliding Window）来完成：

1. 设窗口大小 `window = n - k`。  
2. 初始窗口放在数组最左侧，计算这段的和 `cur_sum`。  
3. 然后把窗口向右滑动一格：`cur_sum += cardPoints[right] - cardPoints[left]`（左边离开，右边加入），实时维护窗口的和。  
4. 在滑动过程中记录 **窗口和的最小值** `min_window_sum`。  
5. 最终答案 = `total - min_window_sum`。

> **类比**  
> 想象你在一条跑道上跑，跑道上有若干段“泥泞区”。你只能跳过 `k` 段泥泞（相当于取走），剩下的 `n‑k` 段必须全部走过。要让你跑得最快（分数最高），就要让 **走过的泥泞段总深度最小**，这正是滑动窗口在找最小子数组的过程。

**为什么滑动窗口能做到 O(n)？**  
窗口每次只移动一次，左指针和右指针各遍历整个数组一次，所有操作都是常数时间，所以整体是线性时间。

#### 代码（Python）

```python
from typing import List

def maxScore(cardPoints: List[int], k: int) -> int:
    n = len(cardPoints)
    total = sum(cardPoints)                 # 所有卡牌的总分

    # 如果 k == n，必须把所有卡都拿走，直接返回 total
    if k == n:
        return total

    window = n - k                           # 要留下的子数组长度
    # 计算首个窗口的和
    cur_sum = sum(cardPoints[:window])
    min_window_sum = cur_sum                 # 记录最小窗口和

    # 滑动窗口：右指针从 window 开始遍历到数组末尾
    for right in range(window, n):
        left = right - window                # 对应要移出的左指针位置
        cur_sum += cardPoints[right] - cardPoints[left]  # 加右边、减左边
        min_window_sum = min(min_window_sum, cur_sum)    # 更新最小值

    # 最大得分 = 总分 - 最小的“留下的”子数组和
    return total - min_window_sum
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，窗口左、右指针各走 `n` 步  
  > 与暴力的 `O(k²)` 相比，线性时间即使在 `n=10⁵` 的极限规模也能毫秒级完成。
- **空间复杂度**：`O(1)` —— 只用常数个变量（`total、cur_sum、min_window_sum`）  
  > 不需要额外的数组，空间占用与输入规模无关。

---

## 心得

- **核心技巧**：把「取走 k 张」转化为「留下 n‑k 张」的最小子数组问题，利用滑动窗口求最小连续和。  
- **适用的题型**：  
  1. “最长子数组和 ≤ k” 类的窗口问题。  
  2. “删除最小子数组后使剩余和最大” 例如 LeetCode 1658（`Minimum Operations to Reduce X to Zero`）。  
  3. “固定窗口长度的最大/最小子数组和” 如 239（`Sliding Window Maximum`）的变体。  
- **一句话总结解题钥匙**：**把“取”变“留”，用滑动窗口找最小保留子数组**。

---

## 反思

- **第一反应**：直接枚举左取右取的组合，写两个循环求和。  
- **最容易踩的坑**：  
  - 忘记处理 `k == n` 的特殊情况，会导致窗口大小为 `0` 而出现错误。  
  - 滑动窗口的边界写错（左指针、右指针的对应关系），容易导致遗漏或重复计算。  
  - 计算 `total - min_window_sum` 时，如果不先求总和，容易出现负数或溢出（在 Python 中不会溢出，但概念上要注意）。  
- **下次遇到同类题**：第一步先思考“**把要做的操作转换成等价的反向操作**”，看能否把求最大转化为求最小，再决定是否可以用滑动窗口或前缀和等线性技巧。