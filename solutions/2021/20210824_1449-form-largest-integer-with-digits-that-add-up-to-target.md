# #1449. 构造最大整数，使各位数字花费之和等于目标值 / Form Largest Integer With Digits That Add up to Target

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/form-largest-integer-with-digits-that-add-up-to-target/)

---

## 题目（英文原版）

**Description**

Given an array of integers cost and an integer target, return the maximum integer you can paint under the following rules:
Since the answer may be very large, return it as a string. If there is no way to paint any integer given the condition, return "0".

**Examples**

**Example 1:**

```
Input: cost = [4,3,2,5,6,7,2,5,5], target = 9
Output: "7772"
Explanation: The cost to paint the digit '7' is 2, and the digit '2' is 3. Then cost("7772") = 2*3+ 3*1 = 9. You could also paint "977", but "7772" is the largest number.
Digit    cost
  1  ->   4
  2  ->   3
  3  ->   2
  4  ->   5
  5  ->   6
  6  ->   7
  7  ->   2
  8  ->   5
  9  ->   5
```

**Example 2:**

```
Input: cost = [7,6,5,5,5,6,8,7,8], target = 12
Output: "85"
Explanation: The cost to paint the digit '8' is 7, and the digit '5' is 5. Then cost("85") = 7 + 5 = 12.
```

**Example 3:**

```
Input: cost = [2,4,6,2,4,6,4,4,4], target = 5
Output: "0"
Explanation: It is impossible to paint any integer with total cost equal to target.
```

**Constraints**

- cost.length == 9
- 1 <= cost[i], target <= 5000

---

## 题目（中文翻译）

给定一个长度为 9 的整数数组 **cost** 和一个整数 **target**，返回在满足以下规则的前提下，你能够绘制的最大整数：

- 绘制整数时，每个数字 **d**（1 ≤ d ≤ 9）需要花费 `cost[d‑1]` 的代价。
- 整数的总花费必须恰好等于 **target**。

由于答案可能非常大，请以字符串形式返回。如果不存在任何整数的总花费等于 **target**，返回 `"0"`。

**示例 1**  
输入: `cost = [4,3,2,5,6,7,2,5,5]`, `target = 9`  
输出: `"7772"`  
解释: 数字 `'7'` 的花费为 2，数字 `'2'` 的花费为 3。于是  
`cost("7772") = 2·3 + 3·1 = 9`。也可以绘制 `"977"`，但 `"7772"` 更大。  

```
Digit    cost
 1  ->   4
 2  ->   3
 3  ->   2
 4  ->   5
 5  ->   6
 6  ->   7
 7  ->   2
 8  ->   5
 9  ->   5
```

**示例 2**  
输入: `cost = [7,6,5,5,5,6,8,7,8]`, `target = 12`  
输出: `"85"`  
解释: 数字 `'8'` 的花费为 7，数字 `'5'` 的花费为 5。于是  
`cost("85") = 7 + 5 = 12`。

**示例 3**  
输入: `cost = [2,4,6,2,4,6,4,4,4]`, `target = 5`  
输出: `"0"`  
解释: 没有任何整数的总花费能够恰好等于 **target**，因此返回 `"0"`。

**约束条件**  
- `cost.length == 9`  
- `1 <= cost[i] , target <= 5000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 **所有** 能够恰好花费 `target` 的数字组合枚举出来，然后挑出最大的整数。  
可以把这看成“把若干块不同费用的拼图（每块代表一个数字）拼成正好 `target` 的拼图”。  
具体实现可以用**回溯**（深度优先搜索）：

1. 从数字 1~9 中任选一个，检查把它的费用 `cost[d-1]` 加进去后剩余的费用还能否继续凑齐。  
2. 把选中的数字拼接到当前字符串后继续搜索，直到剩余费用为 0 时得到一个完整的答案。  
3. 把所有合法答案放进列表，最后比较大小（先比较长度，长度相同再按字典序比较），取最大的。

为什么能得到正确答案？因为回溯会遍历**每一种**可能的数字序列，只要费用恰好等于 `target`，就一定会被记录下来。  

**时间/空间复杂度**（大白话）  
- 每一次选择都有最多 9 种可能，深度最坏可以到 `target / min(cost)`（即最便宜的数字能买多少个）。所以搜索树的规模是指数级的，记作 **O(9^{target/minCost})**，实际会非常慢，甚至在 `target=5000` 时根本不可行。  
- 递归栈的深度同上，最坏需要保存这么多层的调用，空间也是指数级。  

#### 代码（Python）  

```python
from typing import List

def largestNumber_bruteforce(cost: List[int], target: int) -> str:
    # 记录所有合法的数字串
    results = []

    # 深度优先搜索
    def dfs(remaining: int, cur: List[str]) -> None:
        # 剩余费用为 0，说明已经凑齐，保存当前答案
        if remaining == 0:
            results.append(''.join(cur))
            return
        # 剩余费用为负，说明这条路走不通，直接返回
        if remaining < 0:
            return

        # 依次尝试数字 1~9（这里不做剪枝，全部遍历）
        for d in range(1, 10):
            cur.append(str(d))                     # 把数字 d 加到当前串的末尾
            dfs(remaining - cost[d - 1], cur)      # 继续搜索
            cur.pop()                               # 回溯，撤销选择

    dfs(target, [])
    if not results:               # 没有任何合法组合
        return "0"

    # 先比较长度，长度相同再比较字典序（即数值大小）
    results.sort(key=lambda x: (len(x), x), reverse=True)
    return results[0]
```

#### 复杂度  

- **时间复杂度**：`O(9^{target/minCost})` —— 每一步有 9 种选择，深度可能达到 `target/minCost`，所以是指数级的。  
- **空间复杂度**：`O(9^{target/minCost})`（存放所有答案）+ `O(target/minCost)`（递归栈），同样是指数级。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**“枚举所有组合”** 是最大的瓶颈。  
实际上，这道题等价于**无限背包（Unbounded Knapsack）**：  

- **物品**：数字 1~9，每件的“重量”是它的费用 `cost[i]`，价值我们希望**尽可能多的数字**（因为数字越多，整数越长，长度更大是优先级最高的比较标准）。  
- **背包容量**：`target`（总费用）。  

因此我们先用动态规划求出 **在花费恰好为 `i` 时，最多能画多少个数字**（记为 `dp[i]`），这一步只需要 `O(9 * target)` 的时间。  

> **dp[i] 的意义**  
> - `dp[i] = -inf` 表示 **不可能** 用费用 `i` 画出任何整数。  
> - 正数表示**最大数字个数**，比如 `dp[9]=4` 说明花 9 的费用最多能画 4 位数字。  

**转化为最大整数**  
有了 `dp` 表后，我们再从高位往低位**贪心构造**答案：

1. 先确定答案的长度 `len = dp[target]`（如果 `len` 为负，说明根本不可行，直接返回 `"0"`）。  
2. 从数字 **9 → 1**（因为大数字在高位更有价值）尝试放入当前位：  
   - 检查如果把数字 `d` 放进去，剩余费用 `target - cost[d-1]` 是否还能得到 `len-1` 位（即 `dp[target - cost[d-1]] == len-1`）。  
   - 若成立，就把 `d` 写入答案，更新 `target -= cost[d-1]`，`len -= 1`，继续填下一位。  
3. 直到所有位都填完，得到的字符串就是**字典序最大的**整数。  

**为什么贪心有效？**  
因为我们已经保证了每一步的剩余费用还能完成**恰好**剩余的位数。如果把更大的数字（9~1）放在高位而不破坏可行性，那么这个数字必然使整体数值更大——这正是“先长后大的”比较规则。

#### 代码（Python）  

```python
from typing import List

def largestNumber(cost: List[int], target: int) -> str:
    # dp[i] 表示花费 i 能得到的最大数字个数，-inf 表示不可达
    dp = [-10**9] * (target + 1)   # 用一个很小的负数表示“不可能”
    dp[0] = 0                     # 花费 0 可以得到 0 位数字

    # 经典的「无限背包」DP：遍历所有费用，尝试加入每个数字
    for i in range(1, target + 1):
        for d in range(9):                # d = 0~8 对应数字 1~9
            c = cost[d]                   # 费用
            if i >= c:                    # 能放得下
                dp[i] = max(dp[i], dp[i - c] + 1)   # 取最大位数

    # 如果 dp[target] 为负，说明根本没有合法解
    if dp[target] < 0:
        return "0"

    # 构造答案：从高位开始尽可能放大的数字
    ans = []
    cur_len = dp[target]           # 需要的总位数
    remaining = target

    for d in range(8, -1, -1):     # 先尝试 9,8,...,1（下标 8~0）
        c = cost[d]
        # 只要放这个数字后，剩余费用还能得到 cur_len-1 位，就可以放
        while remaining >= c and dp[remaining - c] == cur_len - 1:
            ans.append(str(d + 1))   # d+1 才是真正的数字
            remaining -= c
            cur_len -= 1
            # 继续尝试同一个数字，可能可以连着放多个（如 "7772"）
    
    return ''.join(ans)
```

#### 复杂度  

- **时间复杂度**：`O(9 * target)`  
  - DP 填表遍历 `target` 次，每次检查 9 个数字 → 大约 `9 * target` 次基本操作。  
  - 构造答案时最多遍历 `target` 次（每放一个数字就把 `remaining` 减少相应费用），同样是线性级。  
  - 与暴力解的指数级相比，这个是**线性**的，`target ≤ 5000` 完全可接受。  

- **空间复杂度**：`O(target)`  
  - 只需要一个长度为 `target+1` 的一维 DP 表以及若干常数级变量。  

---

## 心得  

- **核心技巧**：把“费用恰好等于 target 的最大整数”转化为**无限背包**求最大“位数”，再用**贪心+DP 表**恢复字典序最大的数字。  
- **适用的题型**  
  1. “组成目标值的最少/最多硬币”类（LeetCode 322/518）。  
  2. “在给定重量限制下，如何使价值最大”类的背包问题。  
  3. 需要先**最大化某个属性**（如位数、长度），再**字典序/数值最大化**的组合构造题。  
- **一句话总结解题钥匙**：先用 DP 求出**可行的最大长度**，再从大到小的数字**贪心填位**，保证每一步都仍然可行。

---

## 反思  

- **第一反应**：看到“数字的费用”和“总费用 target”，立刻想到背包/凑数，想把所有可能的数字序列枚举。  
- **最容易踩的坑**  
  1. **只能返回字符串**：整数可能非常大，直接用 `int` 会溢出。  
  2. **先比较长度后比较字典序**：仅比较数值大小会忽略“更长的数字一定更大”。  
  3. **DP 初始化**：要把不可达状态设成负无穷（或很小的负数），否则会误把 “0 位” 当作可行解。  
  4. **构造答案的循环**：必须在 `while` 中检查 `dp[remaining - c] == cur_len - 1`，否则可能把一个不可行的数字塞进答案，导致最终费用不等于 target。  
- **下次遇到同类题**：第一步先**把问题抽象为背包（最大化/最小化某个属性）**，写出 DP 表；第二步思考**如何从 DP 表恢复具体解**（贪心、逆向遍历等）。这样可以避免直接暴力枚举的陷阱。