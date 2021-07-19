# #1402. Reducing Dishes / Reducing Dishes

> 难度：困难 · 标签：Array、Dynamic Programming、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/reducing-dishes/)

---

## 题目（英文原版）

**Description**

A chef has collected data on the satisfaction level of his n dishes. Chef can cook any dish in 1 unit of time.
Like-time coefficient of a dish is defined as the time taken to cook that dish including previous dishes multiplied by its satisfaction level i.e. time[i] * satisfaction[i].
Return the maximum sum of like-time coefficient that the chef can obtain after preparing some amount of dishes.
Dishes can be prepared in any order and the chef can discard some dishes to get this maximum value.

**Examples**

**Example 1:**

```
Input: satisfaction = [-1,-8,0,5,-9]
Output: 14
Explanation: After Removing the second and last dish, the maximum total like-time coefficient will be equal to (-1*1 + 0*2 + 5*3 = 14).
Each dish is prepared in one unit of time.
```

**Example 2:**

```
Input: satisfaction = [4,3,2]
Output: 20
Explanation: Dishes can be prepared in any order, (2*1 + 3*2 + 4*3 = 20)
```

**Example 3:**

```
Input: satisfaction = [-1,-4,-5]
Output: 0
Explanation: People do not like the dishes. No dish is prepared.
```

**Constraints**

- n == satisfaction.length
- 1 <= n <= 500
- -1000 <= satisfaction[i] <= 1000

---

## 题目（中文翻译）

一位厨师收集了他 **n** 道菜肴的满意度（satisfaction）数据。厨师烹饪任意一道菜肴都需要 **1** 单位时间。  
某道菜肴的 **like-time coefficient**（like-time coefficient）定义为：烹饪该菜肴时所用的时间（包括之前已烹饪的菜肴的时间之和）乘以该菜肴的满意度，即 `time[i] * satisfaction[i]`。  

返回厨师在烹饪若干道菜后能够得到的 **like-time coefficient**（like-time coefficient）之和的最大值。  
菜肴可以按任意顺序烹饪，厨师也可以丢弃某些菜肴以获得最大值。

**示例 1**  
**输入**: `satisfaction = [-1,-8,0,5,-9]`  
**输出**: `14`  
**解释**: 去掉第二道和最后一道菜后，最大总 **like-time coefficient**（like-time coefficient）为  
`(-1*1 + 0*2 + 5*3 = 14)`。  
每道菜都需要 **1** 单位时间。

**示例 2**  
**输入**: `satisfaction = [4,3,2]`  
**输出**: `20`  
**解释**: 可以按任意顺序烹饪，得到  
`2*1 + 3*2 + 4*3 = 20`。

**示例 3**  
**输入**: `satisfaction = [-1,-4,-5]`  
**输出**: `0`  
**解释**: 没有人喜欢这些菜肴，故不烹饪任何菜。

**约束条件**  
- `n == satisfaction.length`  
- `1 <= n <= 500`  
- `-1000 <= satisfaction[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的做法都穷举一遍**，然后挑出最大值。  
这里的“做法”包括两件事：

1. **挑哪些菜**——因为可以丢弃不喜欢的菜，等价于从 `satisfaction` 数组中选一个子集（子集的每个元素要么选，要么不选）。  
2. **决定烹饪顺序**——选出来的菜可以随意排列，时间系数 `time * satisfaction` 与顺序强相关。

可以把这两步想象成：

- **挑菜**像是挑“卡片”放进背包，卡片要么进要么不进（这就是子集）。
- **排顺序**像是把选好的卡片排成一条队列，队列的第 1 个位置、第二个位置……都会乘以不同的时间系数（1、2、3…）。

所以暴力解的实现思路是：

1. 用 **二进制枚举**（或递归）遍历所有子集（共 `2ⁿ` 种）。
2. 对每个子集，再把里面的元素全排列（`k!` 种，`k` 为子集大小），计算对应的 **like‑time 系数之和**。
3. 记录所有情况的最大值，即为答案。

> 这里不需要真的写出全部排列的代码，只要说明思路即可。因为 `n ≤ 500`，暴力解根本不可行，只是帮助我们确认**问题一定有解**，并为后面的优化提供基准。

#### 代码（Python）

```python
import itertools
from typing import List

def maxSatisfaction_bruteforce(satisfaction: List[int]) -> int:
    n = len(satisfaction)
    best = 0                         # 初始化为 0，表示可以什么都不做
    # 1️⃣ 枚举所有子集（用二进制掩码）
    for mask in range(1 << n):       # 0 ~ 2ⁿ-1
        chosen = [satisfaction[i] for i in range(n) if mask >> i & 1]
        # 2️⃣ 对子集进行全排列
        for perm in itertools.permutations(chosen):
            cur = 0
            # 计算当前排列的 like‑time 系数之和
            for t, sat in enumerate(perm, start=1):   # t 从 1 开始计时
                cur += t * sat
            best = max(best, cur)   # 记录最大值
    return best
```

> **关键行解释**  
> - `for mask in range(1 << n)`: 用 0/1 位表示是否选第 `i` 道菜。  
> - `itertools.permutations(chosen)`: 生成所有可能的烹饪顺序。  
> - `enumerate(perm, start=1)`: `t` 正好是烹饪的时间（第几道菜），从 1 开始。  

#### 复杂度  

- **时间复杂度**：`O(2ⁿ * n!)`（先枚举子集，再对每个子集全排列）。  
  - 这里的 `O(2ⁿ)` 表示“每道菜有选或不选两种可能”，`n!` 表示“选出来的菜要全部排个序”。  
  - 对于 `n=10` 已经是天文数字，更别提题目最高 500！所以只能当作“思考起点”，不是实际可用的解法。  
- **空间复杂度**：`O(n)`，主要是递归栈和临时保存子集的列表。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举顺序是最耗时的环节**。  
观察题目可以发现一个重要的性质：

> **如果把满意度高的菜放在后面（时间系数大），整体得分会更高。**  
> 因为 `time` 是递增的正整数，乘以正数会放大收益，乘以负数会放大损失。

于是我们可以把所有菜 **按满意度从大到小排**（或从小到大排后逆向遍历），再决定**从哪一道开始真正烹饪**。  
核心在于：  
- 当我们从后往前累加时，累计的满意度和（记作 `cum`）如果是正的，说明把当前这道菜加入到已经决定烹饪的集合中会让整体得分提升。  
- 如果 `cum` 为负，则继续往前加只会让后面的 `time` 乘以一个负的累计和，导致总分下降，此时应该停下来——即把前面的菜全部丢掉。

这就是一种 **贪心 + 排序** 的思路，事实上等价于下面的动态规划递推：

设 `dp[i]` 为**从第 `i` 道菜（在已排序好的数组中）开始烹饪，能够得到的最大总分**。  
则有递推式：

```
dp[i] = max( dp[i+1],   # 不选第 i 道
             satisfaction[i] * (len - i) + dp[i+1] )   # 选第 i 道，时间系数为 (len-i)
```

但直接实现递推会产生 O(n²) 的时间。  
观察递推可以发现，只需要维护**当前累计的满意度和**即可得到同样的结果，进而把时间复杂度压到 **O(n log n)**（排序）或 **O(n)**（若已经有序）。

**完整步骤**：

1. **排序**：把 `satisfaction` 按照从小到大排序。  
2. **从后往前遍历**，维护两个变量  
   - `cum`：从当前位置到数组末尾的满意度之和。  
   - `ans`：当前能够得到的最大总分。  
   每遍历一个元素 `x`，先把 `cum += x`。  
   - 如果 `cum > 0`，说明把这道菜加入到已经决定的集合会提升总分，**把 `cum` 加到 `ans`**（因为这道菜在所有已经决定的菜的后面，时间系数会比原来多 1）。  
   - 否则 `cum ≤ 0`，继续往前遍历（此时不把 `cum` 加到 `ans`），因为再往前加入只会让 `cum` 更小，收益更差。  
3. 最终 `ans` 即为最大 like‑time 系数和。

> **类比**：把 `cum` 想象成“锅里剩余的好味道”。当锅里还有正味道（`cum>0`）时，继续往锅里加菜会让整体味道更浓；如果锅里已经是“苦味”（`cum≤0`），再加菜只会让味道更糟，应该停手。

#### 代码（Python）

```python
from typing import List

def maxSatisfaction(satisfaction: List[int]) -> int:
    # 1️⃣ 先排序（从小到大），方便从后往前累加
    satisfaction.sort()
    cum = 0          # 当前累计的满意度和（相当于“剩余的好味道”）
    ans = 0          # 最终的最大 like‑time 系数和

    # 2️⃣ 从数组末尾向前遍历
    for x in reversed(satisfaction):
        cum += x                 # 把当前菜的满意度加入累计
        if cum > 0:              # 只有累计为正时才值得把这道菜保留下来
            ans += cum           # 这一步相当于把所有已经决定的菜的时间系数都加 1
        # 当 cum <= 0 时，直接跳过，不更新 ans，继续向前看

    return ans
```

> **关键行解释**  
> - `satisfaction.sort()`: 把满意度从低到高排好，后面从大到小遍历时，**更大的正数会先出现**。  
> - `for x in reversed(satisfaction)`: 从最大的满意度开始往前走。  
> - `cum += x`: 维护从当前下标到数组末尾的满意度总和。  
> - `if cum > 0: ans += cum`: 当累计为正时，说明把当前这道菜（以及它后面的所有菜）一起烹饪能让整体得分提升，**把这段累计直接加到答案**。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`，遍历一次 `O(n)`，两者相加仍是 `O(n log n)`。  
  - 相比暴力的 `O(2ⁿ * n!)`，已经是线性级别的高效算法。  
- **空间复杂度**：`O(1)`（不计排序使用的原地排序空间）  
  - 只用了常数个额外变量 `cum`、`ans`，不随 `n` 增长。

---

## 心得

- **核心技巧**：**先排序，再从后往前贪心累计**。  
  - 这一步把“选哪些菜”和“排什么顺序”合二为一：排序决定顺序，累计正和决定是否保留当前菜。  
- **适用的题型**  
  1. **需要最大化加权和**，且权重随位置递增（如 “Maximum Sum of Products” 类题）。  
  2. **可以丢弃负价值元素**，且元素之间没有交叉约束（如 “Maximum Subset Sum with Multipliers”）。  
  3. **先排序后贪心** 的典型场景，如 “Best Time to Buy and Sell Stock with Transaction Fee” 中的单调栈/前缀和技巧。  
- **一句话总结解题钥匙**：  
  > “把满意度从大到小排，累计正和就保留，负和直接舍弃——一次遍历搞定全部选择与顺序”。  

---

## 反思

- **第一反应**：想到枚举子集和排列（暴力），因为题目说“可以任意顺序烹饪”。  
- **最容易踩的坑**  
  1. **忘记可以不做任何菜**——当所有满意度都是负数时答案应为 `0`，而不是负的最小值。  
  2. **排序方向写错**——若从小到大直接累加，会得到错误的累计逻辑。  
  3. **累计的意义混淆**：`cum` 不是当前总分，而是“从当前位置到末尾的满意度和”，只有它为正才说明继续往前加入菜会提升总分。  
- **下次遇到同类题的第一步**：  
  > “先把所有数排序，看看把最大的几个放在后面（时间系数大）会不会得到正贡献”。  
  若是正的，就一直往前加；若是负的，就直接停。这样可以快速判断是否需要 DP、贪心或更复杂的算法。