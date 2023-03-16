# #2167. 移除所有含违禁货物车厢的最短时间 / Minimum Time to Remove All Cars Containing Illegal Goods

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-remove-all-cars-containing-illegal-goods/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed binary string s which represents a sequence of train cars. s[i] = '0' denotes that the ith car does not contain illegal goods and s[i] = '1' denotes that the ith car does contain illegal goods.
As the train conductor, you would like to get rid of all the cars containing illegal goods. You can do any of the following three operations any number of times:
Return the minimum time to remove all the cars containing illegal goods.
Note that an empty sequence of cars is considered to have no cars containing illegal goods.

**Examples**

**Example 1:**

```
Input: s = "1100101"
Output: 5
Explanation: 
One way to remove all the cars containing illegal goods from the sequence is to
- remove a car from the left end 2 times. Time taken is 2 * 1 = 2.
- remove a car from the right end. Time taken is 1.
- remove the car containing illegal goods found in the middle. Time taken is 2.
This obtains a total time of 2 + 1 + 2 = 5. 

An alternative way is to
- remove a car from the left end 2 times. Time taken is 2 * 1 = 2.
- remove a car from the right end 3 times. Time taken is 3 * 1 = 3.
This also obtains a total time of 2 + 3 = 5.

5 is the minimum time taken to remove all the cars containing illegal goods. 
There are no other ways to remove them with less time.
```

**Example 2:**

```
Input: s = "0010"
Output: 2
Explanation:
One way to remove all the cars containing illegal goods from the sequence is to
- remove a car from the left end 3 times. Time taken is 3 * 1 = 3.
This obtains a total time of 3.

Another way to remove all the cars containing illegal goods from the sequence is to
- remove the car containing illegal goods found in the middle. Time taken is 2.
This obtains a total time of 2.

Another way to remove all the cars containing illegal goods from the sequence is to 
- remove a car from the right end 2 times. Time taken is 2 * 1 = 2. 
This obtains a total time of 2.

2 is the minimum time taken to remove all the cars containing illegal goods. 
There are no other ways to remove them with less time.
```

**Constraints**

- 1 <= s.length <= 2 * 105
- s[i] is either '0' or '1'.

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的二进制字符串 `s`，它表示一列火车车厢的顺序。  
`s[i] = '0'` 表示第 `i` 节车厢不含违禁货物，`s[i] = '1'` 表示第 `i` 节车厢包含违禁货物。  

作为列车员，你希望将所有含违禁货物的车厢全部移除。你可以无限次地执行以下三种操作中的任意一种：

1. **从左端移除一节车厢**，耗时 `1`。  
2. **从右端移除一节车厢**，耗时 `1`。  
3. **直接移除一节含违禁货物的车厢**（该车厢可以位于序列的任意位置），耗时 `2`。  

返回移除所有含违禁货物的车厢所需的最少时间。  
注意，空的车厢序列视为不存在含违禁货物的车厢。

**示例 1**

```
输入: s = "1100101"
输出: 5
解释:
一种移除所有违禁货物车厢的方案是：
- 从左端移除车厢 2 次，耗时 2 * 1 = 2。
- 从右端移除车厢 1 次，耗时 1。
- 移除位于中间的含违禁货物的车厢，耗时 2。
总耗时为 2 + 1 + 2 = 5。
```

另一种方案是  
- …（此处省略其余步骤）

**示例 2**

```
输入: s = "0010"
输出: 2
解释:
一种方案是：
- 从左端移除车厢 3 次，耗时 3 * 1 = 3。
总耗时为 3。

另一种更优的方案是：
- 直接移除位于中间的含违禁货物的车厢，耗时 2。
总耗时为 2。
```

**约束条件**

- `1 <= s.length <= 2 * 10^5`
- `s[i]` 只能是 `'0'` 或 `'1'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一节车厢单独处理**。  
我们可以不停地执行下面三种操作中的任意一种，直到所有 `'1'`（非法货物）都被删掉：

1. 从左端删除最左边的一节车厢，耗时 **1**。  
2. 从右端删除最右边的一节车厢，耗时 **1**。  
3. 直接把任意一节含 `'1'` 的车厢删除，耗时 **2**（不管它在列车的哪个位置）。

> **类比**：把列车想象成一本书，左端/右端删除相当于把书页从两端撕掉，一次撕掉一页，花费 1 分钟；而直接把某页撕下来（只能是标记了“非法”的页）则花费 2 分钟。  
> 我们只需要把所有标记了“非法”的页撕掉即可，普通页可以留下。

暴力做法就是**枚举所有可能的删除顺序**，计算每一种顺序的总时间，取最小值。

- 正确性：只要把所有 `'1'` 都删掉，题目要求就满足。遍历所有可能的操作序列自然能找到最优的那一个。  
- 时间复杂度：对长度为 `n` 的字符串，操作序列的长度最多是 `n`，每一步都有 3 种选择，搜索空间是 `3^n`，显然不可接受。  
- 空间复杂度：递归栈深度最多 `n`，即 `O(n)`。

> **大白话**：`O(3^n)` 就好比把一根长度为 `n` 的绳子每根都可以剪成 3 种不同的方式，所有方式加起来的数量会指数级增长，`n=20` 时已经超过一万亿次了，电脑根本跑不完。

#### 代码（Python）

```python
def brute_min_time(s: str) -> int:
    """暴力搜索全部删除顺序，时间会爆炸，仅作思路演示。"""
    from functools import lru_cache

    @lru_cache(None)
    def dfs(l: int, r: int) -> int:
        # 当前列车只剩下 s[l:r]（左闭右开区间）
        if '1' not in s[l:r]:          # 已经没有非法车厢
            return 0
        # 1. 从左端删一节
        cost_left = 1 + dfs(l + 1, r)
        # 2. 从右端删一节
        cost_right = 1 + dfs(l, r - 1)
        # 3. 直接删任意一个 '1'
        best_mid = float('inf')
        for i in range(l, r):
            if s[i] == '1':
                best_mid = min(best_mid, 2 + dfs(l, i) + dfs(i + 1, r))
        return min(cost_left, cost_right, best_mid)

    return dfs(0, len(s))
```

> 代码里用 `@lru_cache` 记忆化递归，仍然会因为状态太多而超时，只是把“全部枚举”写成程序的形式。

#### 复杂度

- **时间复杂度**：`O(3^n)`（指数级），因为每一步都有 3 种选择，递归树的规模随 `n` 指数增长。  
- **空间复杂度**：`O(n)`（递归栈深度），但实际运行时会因为大量记忆化表而远大于 `n`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正影响时间的只有 `'1'` 所在的位置**，而普通的 `'0'` 完全可以保留。  
我们只需要决定：

- **左边到底删几节**（用左端删除，费用 1/节）；
- 对剩下的右侧区间，**每个 `'1'` 是直接用 “内部删除”(费用 2) 还是把它“搬到右端再删除”(费用 = 右侧的普通车厢数 + 1)。  

这就把原来的**全局搜索**转化成**一次线性扫描**：

1. **先算右侧的最优费用**  
   从右往左遍历，维护 `zero_cnt` —— 当前右边已经看到的 `'0'` 的数量（这些 `'0'` 只有在我们决定把左侧的 `'1'` 通过右端删除时才会被迫删除）。  
   对每个 `'1'`，有两种方式：
   - **内部删除**：费用 2。  
   - **右端删除**：先把右边的 `zero_cnt` 个 `'0'` 全部删掉（每个 1 分钟），再把这节 `'1'` 本身删掉，总费用 `zero_cnt + 1`。  
   取两者的最小值，就是这节 `'1'` 的最佳费用。  
   把每个 `'1'` 的费用累计起来，就得到 **`suffix[i]`** —— 删除从位置 `i` 到末尾所有 `'1'`，且**不使用左端删除**的最小时间。

2. **左端只用“左删”**  
   如果我们决定把前 `k` 节车厢全部从左端删掉（不管它们是 `'0'` 还是 `'1'`），费用就是 `k`（每节 1 分钟），记为 **`left_cost = k`**。这一步只能使用**左端删除**，因为题目已经把这类操作单独列为第一种。

3. **枚举分割点**  
   设分割点为 `k-1`（左边删掉 `k` 节），则总费用为  

   ```
   total = left_cost          # k
         + suffix[k]          # 右侧最优费用（不使用左端删除）
   ```

   我们只要在 `k = 0 … n`（`k = 0` 表示不左删，`k = n` 表示全部左删）之间取最小值即可。

> **类比**：把列车想象成一根绳子，我们可以从左边剪掉一段（每剪掉一寸花 1 分钟），剩下的右边再决定每个“有结”的位置是直接剪掉（花 2 分钟）还是把绳子往右拉，把结拖到右端再剪（需要先拉过右侧的普通段，拉的长度就是 `zero_cnt`，再剪 1 分钟）。  
> 只要遍历一次，就能找到最佳的“左剪长度 + 右侧处理方式”。

#### 代码（Python）

```python
def min_time_to_remove_illegal(s: str) -> int:
    """
    最优解：O(n) 时间、O(n) 空间
    思路见文档上方的详细说明。
    """
    n = len(s)

    # ---------- 1. 计算 suffix[i] ----------
    # suffix[i] 表示在区间 [i, n) 内，只使用「右端删除」和「内部删除」的最小时间
    suffix = [0] * (n + 1)          # suffix[n] = 0，空区间不需要任何操作
    zero_cnt = 0                    # 当前右侧已经出现的 '0' 数量
    total = 0                       # 累计的最小费用

    # 从右往左遍历
    for i in range(n - 1, -1, -1):
        if s[i] == '1':
            # 对这节非法车厢，取两种方式的最小值
            # 方式1：内部删除，费用 2
            # 方式2：把它搬到右端再删除，需要先把右侧的 zero_cnt 个普通车厢删掉
            cost = min(2, zero_cnt + 1)
            total += cost
        else:  # s[i] == '0'
            zero_cnt += 1           # 这段普通车厢如果以后要把左侧的 '1' 搬到右端，就必须被删掉
        suffix[i] = total           # 记录从 i 开始的最小费用

    # ---------- 2. 枚举左端删除的长度 ----------
    ans = float('inf')
    left_cost = 0                    # 已经左删了多少节，初始为 0

    for k in range(n + 1):           # k 表示左侧删掉的车厢数目
        # 总费用 = 左端删除的费用 + 右侧最优费用
        ans = min(ans, left_cost + suffix[k])
        # 若再向右移动分割点，需要再左删一节（不论是 '0' 还是 '1'）
        left_cost += 1               # 下一轮的 left_cost = k+1

    return ans
```

> 代码中的关键行都有中文注释，帮助你一步步跟踪思路。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历字符串两遍（一次从右到左算 `suffix`，一次从左到右枚举分割点），每一步都是常数操作。  
  - 与暴力解的指数级 `3^n` 相比，线性时间在 `n ≤ 2·10⁵` 的限制下轻松跑完。

- **空间复杂度**：`O(n)`  
  - 额外存了一个长度为 `n+1` 的 `suffix` 数组。  
  - 如果想进一步压缩空间，也可以在枚举分割点时直接使用滚动变量，只保留 `suffix[i]` 的当前值，空间可以降到 `O(1)`。

---

## 心得

- **核心技巧**：把“从两端删除”转化为**左侧统一使用左端删除、右侧统一使用右端删除**，再对每个 `'1'` 在右侧决定“内部删除”还是“右端删除”。本质是**把全局搜索拆分成左右两段的局部最优**，并用一次线性扫描求出右侧的最优费用。

- **该技巧适用的题型**  
  1. **只关心特定字符的删除**，如 “删除所有 `1`”/“删除所有 `a`”。  
  2. **两端操作 + 任意位置操作** 的混合题目，例如 “从左/右端删除 + 任意位置翻转”。  
  3. **最小化代价的分割问题**，常见于 “把数组分成左/右两段，各自使用不同策略” 的动态规划或贪心题。

- **一句话总结解题钥匙**：**把左端和右端的操作分别独立处理，右侧只需比较 “内部删除 2” 与 “右端删除 距离+1” 的最小值，再遍历一次枚举左侧删多少即可得到全局最优。**

---

## 反思

- **拿到题目第一反应**：想到暴力枚举所有操作顺序，然后发现不可行。随后意识到只有 `'1'` 需要被清除，`'0'` 可以保留，于是开始考虑从两端把 `'1'` 拉到端点的成本。

- **最容易踩的坑**  
  1. **忘记 `'0'` 也会产生代价**：如果把左侧的 `'1'` 通过右端删除，需要先把右侧的所有 `'0'` 删除，每个 `'0'` 都要算上 1 分钟。  
  2. **分割点的边界**：`k = 0`（不左删）和 `k = n`（全左删）必须都考虑，否则可能漏掉最优解。  
  3. **整数溢出/大数**：虽然 Python 没有溢出问题，但在其它语言实现时要注意使用 `long long`。

- **下次遇到同类题，第一步该想到**：**把两端的删除操作分别抽象成“统一的左端删除费用 = 左侧长度”以及“右侧每个 `'1'` 的最优费用 = min(内部 2, 右侧零的数量 + 1)”，然后只需一次线性扫描求最小总和。**