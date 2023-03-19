# #2171. **移除最少数量的魔法豆** / Removing Minimum Number of Magic Beans

> 难度：中等 · 标签：Array、Greedy、Sorting、Enumeration、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/removing-minimum-number-of-magic-beans/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers beans, where each integer represents the number of magic beans found in a particular magic bag.
Remove any number of beans (possibly none) from each bag such that the number of beans in each remaining non-empty bag (still containing at least one bean) is equal. Once a bean has been removed from a bag, you are not allowed to return it to any of the bags.
Return the minimum number of magic beans that you have to remove.

**Examples**

**Example 1:**

```
Input: beans = [4,1,6,5]
Output: 4
Explanation: 
- We remove 1 bean from the bag with only 1 bean.
  This results in the remaining bags: [4,0,6,5]
- Then we remove 2 beans from the bag with 6 beans.
  This results in the remaining bags: [4,0,4,5]
- Then we remove 1 bean from the bag with 5 beans.
  This results in the remaining bags: [4,0,4,4]
We removed a total of 1 + 2 + 1 = 4 beans to make the remaining non-empty bags have an equal number of beans.
There are no other solutions that remove 4 beans or fewer.
```

**Example 2:**

```
Input: beans = [2,10,3,2]
Output: 7
Explanation:
- We remove 2 beans from one of the bags with 2 beans.
  This results in the remaining bags: [0,10,3,2]
- Then we remove 2 beans from the other bag with 2 beans.
  This results in the remaining bags: [0,10,3,0]
- Then we remove 3 beans from the bag with 3 beans. 
  This results in the remaining bags: [0,10,0,0]
We removed a total of 2 + 2 + 3 = 7 beans to make the remaining non-empty bags have an equal number of beans.
There are no other solutions that removes 7 beans or fewer.
```

**Constraints**

- 1 <= beans.length <= 105
- 1 <= beans[i] <= 105

---

## 题目（中文翻译）

给定一个正整数数组 `beans`，数组中的每个整数表示在相应的魔法袋（magic bag）中找到的魔法豆（magic beans）的数量。  
你可以从每个袋子中移除任意数量的豆子（也可以不移除），要求所有剩余的非空袋子（仍然至少含有一颗豆子）的豆子数量相等。  
一旦从某个袋子中移除豆子，就不能再将其放回任何袋子。  

返回需要移除的魔法豆的最小总数。

**示例 1**  
输入: `beans = [4,1,6,5]`  
输出: `4`  
解释:  
- 我们从只有 1 颗豆子的袋子中移除 1 颗豆子。此时剩余的袋子为 `[4,0,6,5]`。  
- 然后从装有 6 颗豆子的袋子中移除 2 颗豆子。此时剩余的袋子为 `[4,0,4,5]`。  
- 再从装有 5 颗豆子的袋子中移除 1 颗豆子。此时剩余的袋子为 `[4,0,4,4]`。  
我们共移除了 `1 + 2 + 1 = 4` 颗豆子，使所有非空袋子的豆子数量相等。

**示例 2**  
输入: `beans = [2,10,3,2]`  
输出: `7`  
解释:  
- 我们从其中一个装有 2 颗豆子的袋子中移除 2 颗豆子。此时剩余的袋子为 `[0,10,3,2]`。  
- 然后从另一个装有 2 颗豆子的袋子中移除 2 颗豆子。此时剩余的袋子为 `[0,10,3,0]`。  
- 接着从装有 3 颗豆子的袋子中移除 3 颗豆子。此时剩余的袋子为 `[0,10,0,0]`。  
我们共移除了 `2 + 2 + 3 = 7` 颗豆子，使所有非空袋子的豆子数量相等。

**约束条件**
- `1 <= beans.length <= 10^5`
- `1 <= beans[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的目标数量** `t`（即所有非空袋子最终应该拥有的豆子数），然后把每个袋子里多余的豆子全部剔除，或者把整个袋子清空（如果它本来就少于 `t`）。  

- **数据结构**：我们只需要一个普通的 Python 列表 `beans`，遍历它即可。可以把列表想象成超市里排好的若干装豆子的袋子。
- **为什么正确**：只要把每个袋子里的豆子数改成 `t`（或者变成 0），所有非空袋子就会拥有相同的豆子数。遍历所有可能的 `t`，必然会碰到最优的那个目标值，于是得到最少要删除的豆子数。
- **复杂度**：  
  - 目标值 `t` 可能是 `beans` 中的每一个数（最多 `n` 种），对每一种 `t` 我们都要遍历一遍全部 `n` 个袋子，计算需要删除多少豆子。  
  - 因此时间复杂度是 **O(n²)**，即“平方级”。如果 `n=10⁵`，`n²` 会是 `10¹⁰`，在电脑上根本跑不完。  
  - 只使用了原数组和几个整数变量，空间复杂度是 **O(1)**，即“常数级”，几乎不占额外空间。

#### 代码（Python）

```python
def minimumRemoval_bruteforce(beans):
    """
    暴力枚举每一种可能的目标数量 t
    返回最少需要删除的豆子数
    """
    n = len(beans)
    ans = float('inf')                 # 记录当前最小的删除数
    for t in beans:                    # t 只能取出现过的值，枚举所有可能
        removed = 0
        for b in beans:                # 遍历每个袋子，计算需要删除的豆子
            if b < t:                  # 这个袋子豆子太少，必须全部清空
                removed += b
            else:                      # 否则把多余的削减到 t
                removed += b - t
        ans = min(ans, removed)        # 取最小值
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 想象 `n=1000`，程序需要做 `1000 × 1000 = 1,000,000` 次加减运算；`n=10⁵` 时则是 `10¹⁰` 次，远远超出 1 秒的限制。  
- **空间复杂度**：`O(1)`  
  - 只用了几个临时整数变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到两点 **瓶颈**：

1. **重复遍历**：每次枚举目标 `t` 时，都要重新遍历整条数组。  
2. **目标值的选择**：其实我们只需要把目标值设为 **某个非空袋子的豆子数**，因为把所有非空袋子都调到比它更小的数，只会让删除的总量变大。

下面一步步推导出更快的做法。

---

#### 2.1 先把袋子排序  

把 `beans` 按从小到大排好序，记为 `a[0] ≤ a[1] ≤ … ≤ a[n‑1]`。  
排序的意义类似于把 **最小的几个袋子挑出来**，因为如果我们决定让某些袋子完全清空，显然应该先清空豆子最少的袋子（“把最轻的石头先搬走”），这样总删除量最少。

排序的时间是 `O(n log n)`，在 10⁵ 规模的数据里完全可以接受。

---

#### 2.2 前缀和帮助快速求和  

定义 **前缀和** `pref[i]` 为 `a[0] + a[1] + … + a[i]`（包含 `i`）。  
有了前缀和，我们可以在 `O(1)` 时间内求出：

- **左侧已经清空的袋子**（下标 `< i`）的总豆子数：`pref[i‑1]`（如果 `i=0` 则为 0）。
- **右侧保留下来的袋子**（下标 `≥ i`）的数量：`cnt = n - i`。

如果我们把下标 `i` 以及其右侧所有袋子都 **保留下来**，并且把它们的豆子数都降到 `a[i]`（即当前第 `i` 小的袋子数量），那么：

- 右侧所有袋子最终会有 `a[i] * cnt` 个豆子（每个 `a[i]`）。
- 右侧原本的豆子总数是 `total_right = pref[n‑1] - pref[i‑1]`（如果 `i=0` 则是 `pref[n‑1]`）。
- 为了把右侧都降到 `a[i]`，我们需要 **删除** `total_right - a[i] * cnt` 颗豆子。
- 左侧已经全部清空，不需要额外操作。

于是 **保留下来的豆子总数** 为 `a[i] * cnt`，**需要删除的豆子总数** 为 `total_sum - a[i] * cnt`，其中 `total_sum = pref[n‑1]` 是所有豆子的总量。

我们只要遍历 `i = 0 … n‑1`，求出每种情况下的删除量，取最小即可。

---

#### 2.3 为什么这就是最优？

- **清空的袋子一定是最小的**：如果我们决定让某个袋子完全清空，却没有把比它更小的袋子也清空，就可以把更小的袋子换成空的，删除的总量会更少（因为空的只需要删掉它本身的豆子数）。
- **保留的袋子最终数量一定等于其中最小的那个**：设保留下来的非空袋子最小值是 `m`，把所有袋子都降到 `m` 不会比把它们降到更大的数删得少（因为要多删掉 ` (target - m) * cnt` 颗豆子）。所以只需要考虑 **把所有保留下来的袋子降到它们最小的那一个**。

综上，遍历每个位置 `i`（把左侧全部清空，右侧全部降到 `a[i]`）就覆盖了所有可能的最优方案。

---

#### 代码（Python）

```python
def minimumRemoval(beans):
    """
    最优解：先排序 + 前缀和，枚举保留下来的最小值位置
    返回最少需要删除的豆子数
    """
    beans.sort()                         # O(n log n)  —— 把袋子从小到大排好
    n = len(beans)

    # 计算前缀和 pref[i] = sum(beans[0..i])
    pref = [0] * n
    pref[0] = beans[0]
    for i in range(1, n):
        pref[i] = pref[i - 1] + beans[i]

    total = pref[-1]                     # 所有豆子的总量
    ans = total                          # 初始化为全部删除的情况

    for i in range(n):
        # 右侧（包括 i）保留下来的袋子数量
        cnt = n - i
        # 把这些袋子都降到 beans[i] 后的豆子总量
        kept = beans[i] * cnt
        # 需要删除的豆子数 = 总量 - 保留下来的量
        removed = total - kept
        ans = min(ans, removed)          # 取最小值

    return ans
```

> **关键行中文注释**  
> - `beans.sort()`：把袋子按豆子数从少到多排好，好比把装豆子的盒子从轻到重排成一列。  
> - `pref[i] = pref[i - 1] + beans[i]`：累加前面的豆子数，得到前缀和。  
> - `cnt = n - i`：右侧（包括当前）还有多少袋子会被保留。  
> - `kept = beans[i] * cnt`：如果把这些袋子都调成 `beans[i]`，最终会剩下多少豆子。  
> - `removed = total - kept`：剩下的豆子不变，其他的都要删掉。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序占 `O(n log n)`，随后一次线性遍历 `O(n)`，两者相加仍是 `O(n log n)`。相比暴力的 `O(n²)`，速度提升了几个数量级。  
- **空间复杂度**：`O(n)`  
  - 需要额外的前缀和数组 `pref`，大小为 `n`。如果想进一步省空间，可以在遍历时直接累加左侧和，只用常数级额外空间，但 `O(n)` 已经足够好。

---

## 心得

- **核心技巧**：先排序，再利用前缀和（或累计和）在一次遍历中枚举“保留下来的最小值”。这是一种典型的 “排序 + 前缀和 + 枚举” 贪心思路。
- **适用的题型**  
  1. **把数组中元素统一到某个值**（如 “使数组中所有元素相等的最小操作数”）  
  2. **删除最少元素使剩余满足某种单调或相等条件**（如 “删除最少的石子，使剩余石子重量相等”）  
  3. **利用排序后枚举分割点求最优**（如 “最大子序列和的最小差值”）
- **一句话总结解题钥匙**：**把“要保留的袋子”固定下来，让左侧最小的袋子全部清空，右侧统一降到左侧的最小值**——只需一次遍历即可找出最小删除量。

---

## 反思

- **第一反应**：看到“把所有非空袋子数量相同”，我立刻想到“枚举目标值”，于是写出了暴力解。  
- **最容易踩的坑**  
  - **忘记先排序**：直接枚举目标值时会出现 `O(n²)`，超时。  
  - **边界情况**：全部袋子清空（目标值为 0）也是合法方案，需要在代码里自然覆盖（即 `removed = total`）。  
  - **整数溢出**：在其他语言可能需要 64 位整数；Python 自动大整数，不会出错。  
- **下次遇到同类题**：**第一步**先判断是否可以通过**排序 + 前缀和** 把“分割点”枚举出来；如果可以，就把暴力的 “遍历所有可能” 变成 “遍历所有分割位置”，时间立刻从平方级降到对数级或线性级。