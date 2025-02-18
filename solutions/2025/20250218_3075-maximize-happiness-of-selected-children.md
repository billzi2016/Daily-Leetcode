# #3075. 选择儿童的最大幸福值 / Maximize Happiness of Selected Children

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximize-happiness-of-selected-children/)

---

## 题目（英文原版）

**Description**

You are given an array happiness of length n, and a positive integer k.
There are n children standing in a queue, where the ith child has happiness value happiness[i]. You want to select k children from these n children in k turns.
In each turn, when you select a child, the happiness value of all the children that have not been selected till now decreases by 1. Note that the happiness value cannot become negative and gets decremented only if it is positive.
Return the maximum sum of the happiness values of the selected children you can achieve by selecting k children.

**Examples**

**Example 1:**

```
Input: happiness = [1,2,3], k = 2
Output: 4
Explanation: We can pick 2 children in the following way:
- Pick the child with the happiness value == 3. The happiness value of the remaining children becomes [0,1].
- Pick the child with the happiness value == 1. The happiness value of the remaining child becomes [0]. Note that the happiness value cannot become less than 0.
The sum of the happiness values of the selected children is 3 + 1 = 4.
```

**Example 2:**

```
Input: happiness = [1,1,1,1], k = 2
Output: 1
Explanation: We can pick 2 children in the following way:
- Pick any child with the happiness value == 1. The happiness value of the remaining children becomes [0,0,0].
- Pick the child with the happiness value == 0. The happiness value of the remaining child becomes [0,0].
The sum of the happiness values of the selected children is 1 + 0 = 1.
```

**Example 3:**

```
Input: happiness = [2,3,4,5], k = 1
Output: 5
Explanation: We can pick 1 child in the following way:
- Pick the child with the happiness value == 5. The happiness value of the remaining children becomes [1,2,3].
The sum of the happiness values of the selected children is 5.
```

**Constraints**

- 1 <= n == happiness.length <= 2 * 105
- 1 <= happiness[i] <= 108
- 1 <= k <= n

---

## 题目（中文翻译）

给定一个长度为 `n` 的数组 `happiness`（array）以及一个正整数 `k`（positive integer）。  
有 `n` 个儿童排成一条队列（queue），第 `i` 个儿童的幸福值为 `happiness[i]`。你需要在 `k` 个回合（turn）中选出 `k` 名儿童。

在每个回合中，当你选中一名儿童后，所有尚未被选中的儿童的幸福值都会减少 `1`。需要注意的是，幸福值不能变为负数，只有在当前值为正时才会递减。

返回通过选取 `k` 名儿童可以得到的最大幸福值之和。

**示例 1**  
Input: `happiness = [1,2,3]`, `k = 2`  
Output: `4`  
Explanation: 我们可以按以下方式选取 2 名儿童：  
- 选取幸福值为 `3` 的儿童。其余儿童的幸福值变为 `[0,1]`。  
- 选取幸福值为 `1` 的儿童。剩余儿童的幸福值变为 `[0]`（幸福值不能小于 `0`）。  
选中儿童的幸福值之和为 `3 + 1 = 4`。

**示例 2**  
Input: `happiness = [1,1,1,1]`, `k = 2`  
Output: `1`  
Explanation: 我们可以按以下方式选取 2 名儿童：  
- 任意选取一名幸福值为 `1` 的儿童。其余儿童的幸福值变为 `[0,0,0]`。  
- 选取幸福值为 `0` 的儿童。剩余儿童的幸福值仍为 `[0,0]`。  
选中儿童的幸福值之和为 `1 + 0 = 1`。

**示例 3**  
Input: `happiness = [2,3,4,5]`, `k = 1`  
Output: `5`  
Explanation: 我们可以按以下方式选取 1 名儿童：  
- 选取幸福值为 `5` 的儿童。其余儿童的幸福值变为 `[1,2,3]`。  
选中儿童的幸福值之和为 `5`。

**约束条件**  
- `1 <= n == happiness.length <= 2 * 10^5`  
- `1 <= happiness[i] <= 10^8`  
- `1 <= k <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的挑选顺序都枚举一遍**，然后计算每一种顺序对应的总幸福值，最后取最大值。  

- **数据结构**：我们可以用一个列表 `happiness` 保存每个孩子当前的幸福值，用 `visited`（布尔数组）记录哪些孩子已经被挑选。  
- **生活化类比**：把每个孩子想象成一杯饮料，杯子里有一定的甜度（幸福值），每挑走一杯，其他所有未被挑走的饮料的甜度会统一下降 1（但不会低于 0）。我们要尝试所有挑选顺序，找出甜度总和最大的那种。

**为什么这个方法正确**  
因为我们遍历了**所有**合法的挑选顺序，必然能找到最优解。只要计算过程没有错误，就一定能得到答案。

**时间/空间复杂度**  
- 枚举所有挑选顺序相当于在 `n` 个孩子中挑 `k` 个并考虑顺序，即 `P(n, k) = n! / (n‑k)!` 种可能。即使 `n` 只有 10，`k=5` 时也有 30 240 种；而题目里 `n` 可以到 2·10⁵，根本不可能跑完。  
- 所以时间复杂度是 **指数级**，记作 `O(P(n,k))`，在实际中会超时。  
- 空间上我们只需要保存原数组和一个 `visited` 标记数组，都是 `O(n)`。

#### 代码（Python）

```python
from itertools import permutations

def max_happiness_bruteforce(happiness, k):
    n = len(happiness)
    best = 0

    # 所有挑选 k 个孩子的排列（顺序很重要）
    for order in permutations(range(n), k):
        cur = happiness[:]          # 当前的幸福值拷贝
        total = 0
        for step, idx in enumerate(order):
            # 选中的孩子得到当前的幸福值
            total += cur[idx]

            # 其余未选中的孩子幸福值减 1（不低于 0）
            for j in range(n):
                if j != idx and cur[j] > 0:
                    cur[j] -= 1
        best = max(best, total)

    return best
```

> **注意**：这段代码仅用于说明思路，**不能在正式测试里使用**，会在几毫秒内超时。

#### 复杂度

- **时间复杂度**：`O(P(n, k))`（指数级），因为要遍历所有挑选顺序。  
- **空间复杂度**：`O(n)`，主要是保存当前幸福值的数组。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈在于枚举所有顺序**。实际上，题目给了我们一个重要的规律：

> 每一轮挑选后，所有未被挑选的孩子的幸福值都会统一减 1（只要它们原本大于 0）。

这意味着 **每一次挑选的孩子，只会受到它之前被挑选的次数的影响**，而与后面的挑选顺序无关。换句话说，第 `i` 次挑选时（`i` 从 1 开始），如果我们挑选的是原始数组中的第 `x` 大的数，那么它实际得到的幸福值是：

```
max(original_value - (i-1), 0)
```

因为在第 `i` 次挑选之前，已经有 `i-1` 轮每轮都让它的值减了 1。

所以要想让总和最大，我们应当：

1. **先挑最大的孩子**，因为它们受到的减法次数最少。  
2. 按 **从大到小** 的顺序挑选前 `k` 个数。  
3. 对第 `i` 个被挑选的数，计算 `max(value - (i-1), 0)` 并累加。

这就是典型的 **贪心 + 排序** 思路。排序一次就能得到从大到小的序列，随后线性遍历一次即可得到答案。

**核心算法解释**  

- **排序**：把数组从大到小排好，就像把装有糖果的盒子按照糖果多少从高到低排好，先挑糖最多的盒子。  
- **贪心**：每一步都选当前剩下的最大值，因为以后所有未选的值都会被统一扣 1，越早挑走的值被扣的次数越少，收益最大。  
- **截断为 0**：如果某个值被扣得已经 ≤0，后面再挑它也只能得到 0，直接把负数当 0 处理即可。

#### 代码（Python）

```python
def max_happiness_greedy(happiness, k):
    """
    :param happiness: List[int]，每个孩子的初始幸福值
    :param k: int，必须挑选的孩子数量
    :return: int，能够得到的最大幸福值总和
    """
    # 1. 按从大到小排序
    happiness.sort(reverse=True)          # 大的在前面

    total = 0
    # 2. 依次挑选前 k 个（若 k > len，则只遍历实际长度）
    for i in range(k):
        # 第 i 次挑选（i 从 0 开始），已经经历了 i 次“全体-1”
        cur_val = happiness[i] - i       # 减去已经发生的次数
        if cur_val > 0:                  # 只把正数加进去，负数当 0
            total += cur_val
        # 如果已经 ≤0，后面的更小的数更不可能贡献正值，直接跳出循环
        else:
            break

    return total
```

> **关键行中文注释**  
> - `happiness.sort(reverse=True)`：把最大值放在前面，方便贪心挑选。  
> - `cur_val = happiness[i] - i`：第 `i` 次挑选前已经被整体减了 `i` 次。  
> - `if cur_val > 0:`：负数或 0 不会增加总和，直接忽略。  

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`，遍历前 `k` 项是 `O(k)`（`k ≤ n`），整体受排序主导。  
  - 与暴力解的指数级时间相比，快了很多，能轻松处理 2·10⁵ 的规模。  

- **空间复杂度**：`O(1)`（不计排序使用的递归栈）  
  - 只在原数组上就地排序，额外只用了常数级的变量。

---

## 心得

- **核心技巧**：**先挑最大、后递减** 的贪心思路 + **排序**。  
- **适用的题型**：  
  1. “每轮统一衰减” 类的选择题（如本题）。  
  2. “在每次操作后全局统一变化” 的资源分配问题（如“最大化奖励的 K 次操作”）。  
  3. “挑选 k 个数，使得 … 减去递增惩罚” 的变形（如 LeetCode 1648 “卖木头的利润”）。  
- **一句话总结解题钥匙**：**把所有值按大到小排好，依次扣除已进行的轮数，正数相加即为最大总和**。

---

## 反思

- **第一反应**：看到“每选一次，未选的都会减 1”，本能想到**模拟**，于是想到暴力遍历所有顺序。  
- **最容易踩的坑**：  
  - 忽略了 **负数要截为 0**，导致答案出现负数。  
  - 没考虑 **提前结束**：当某个值已经 ≤0，后面的更小值肯定也不贡献正值，若不提前退出会多做无意义的循环。  
  - 对 **大数据量** 没有意识到暴力不可行，直接写了 `O(n^k)` 的代码会 TLE。  
- **下次遇到同类题**：第一步先**思考是否有全局统一的变化**（如统一递减、统一递增），如果有，**尝试排序+贪心**，而不是直接枚举。这样往往能在 `O(n log n)` 内得到答案。