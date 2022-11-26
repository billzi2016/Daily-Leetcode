# #2028. 找出缺失的观察值 / Find Missing Observations

> 难度：中等 · 标签：Array、Math、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-missing-observations/)

---

## 题目（英文原版）

**Description**

You have observations of n + m 6-sided dice rolls with each face numbered from 1 to 6. n of the observations went missing, and you only have the observations of m rolls. Fortunately, you have also calculated the average value of the n + m rolls.
You are given an integer array rolls of length m where rolls[i] is the value of the ith observation. You are also given the two integers mean and n.
Return an array of length n containing the missing observations such that the average value of the n + m rolls is exactly mean. If there are multiple valid answers, return any of them. If no such array exists, return an empty array.
The average value of a set of k numbers is the sum of the numbers divided by k.
Note that mean is an integer, so the sum of the n + m rolls should be divisible by n + m.

**Examples**

**Example 1:**

```
Input: rolls = [3,2,4,3], mean = 4, n = 2
Output: [6,6]
Explanation: The mean of all n + m rolls is (3 + 2 + 4 + 3 + 6 + 6) / 6 = 4.
```

**Example 2:**

```
Input: rolls = [1,5,6], mean = 3, n = 4
Output: [2,3,2,2]
Explanation: The mean of all n + m rolls is (1 + 5 + 6 + 2 + 3 + 2 + 2) / 7 = 3.
```

**Example 3:**

```
Input: rolls = [1,2,3,4], mean = 6, n = 4
Output: []
Explanation: It is impossible for the mean to be 6 no matter what the 4 missing rolls are.
```

**Constraints**

- m == rolls.length
- 1 <= n, m <= 105
- 1 <= rolls[i], mean <= 6

---

## 题目（中文翻译）

你有 `n + m` 次 6 面骰子投掷的观测值（observations），每个面编号为 1 到 6。`n` 个观测值丢失了，你只拥有 `m` 次投掷的观测值。幸运的是，你已经计算出这 `n + m` 次投掷的平均值（average value）。

给定一个长度为 `m` 的整数数组（array）`rolls`，其中 `rolls[i]` 表示第 `i` 次观测的数值。还给定两个整数 `mean` 和 `n`。

返回一个长度为 `n` 的数组，包含丢失的观测值，使得 `n + m` 次投掷的平均值恰好为 `mean`。如果存在多个合法答案，返回任意一个。如果不存在满足条件的数组，返回空数组。

`k` 个数的平均值（average value）等于这些数的和除以 `k`。注意 `mean` 为整数，因此 `n + m` 次投掷的总和必须能被 `n + m` 整除。

### 示例

**示例 1**

```text
Input: rolls = [3,2,4,3], mean = 4, n = 2
Output: [6,6]
Explanation: 所有 `n + m` 次投掷的平均值为 (3 + 2 + 4 + 3 + 6 + 6) / 6 = 4.
```

**示例 2**

```text
Input: rolls = [1,5,6], mean = 3, n = 4
Output: [2,3,2,2]
Explanation: 所有 `n + m` 次投掷的平均值为 (1 + 5 + 6 + 2 + 3 + 2 + 2) / 7 = 3.
```

**示例 3**

```text
Input: rolls = [1,2,3,4], mean = 6, n = 4
Output: []
Explanation: 无论这 4 个缺失的投掷取何值，都不可能使平均值为 6。
```

### 约束条件

- `m == rolls.length`
- `1 <= n, m <= 10^5`
- `1 <= rolls[i], mean <= 6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把「缺失的 n 次掷骰子」全部枚举出来，看看哪一种组合能让所有 n+m 次掷骰子的平均值恰好等于 `mean`。  
- **数据结构**：我们只需要一个普通的 Python 列表 `cand` 来存放当前正在尝试的 n 个掷骰子结果。可以把它想象成「一张纸」上写下的 n 个数字。  
- **为什么可行**：如果把所有可能的 1~6 的数都列出来（每个位置都有 6 种可能），最终一定会遍历到所有合法的组合。只要其中有一种组合满足「总和 = mean × (n+m)」，我们就找到了答案。  
- **时间/空间分析**：  
  - 每个缺失位置有 6 种取值，n 个位置就有 `6^n` 种组合，时间复杂度是 **指数级**，记作 `O(6^n)`。这就像「把所有可能的密码全部尝试一次」——当 n 较大时根本不可行。  
  - 递归深度最多为 n，额外使用的空间主要是保存当前组合的列表，空间复杂度是 `O(n)`。  

> 大白话解释：`O(6^n)` 表示「如果 n=5，需要尝试 6×6×6×6×6 = 7776 种情况」；如果 n=20，就是 6 的 20 次方，天文数字，根本跑不完。

#### 代码（Python）

```python
from typing import List

def missing_observations_bruteforce(rolls: List[int], mean: int, n: int) -> List[int]:
    m = len(rolls)                       # 已知的掷骰子次数
    total_len = n + m                     # 所有掷骰子的总次数
    target_sum = mean * total_len         # 所有掷骰子的目标总和
    known_sum = sum(rolls)                # 已知的总和
    need = target_sum - known_sum          # 缺失的 n 次掷骰子需要凑的和

    # 递归枚举每一个缺失位置的取值（1~6）
    def dfs(idx: int, cur_sum: int, path: List[int]) -> List[int]:
        # 已经填完 n 个位置，检查是否正好凑到 need
        if idx == n:
            return path[:] if cur_sum == need else None
        # 剪枝：如果已经超出需要的和，直接返回
        if cur_sum > need:
            return None
        # 继续尝试 1~6
        for v in range(1, 7):
            res = dfs(idx + 1, cur_sum + v, path + [v])
            if res:                     # 找到一个合法解就立刻返回
                return res
        return None

    ans = dfs(0, 0, [])
    return ans if ans else []            # 没有解返回空列表
```

> **关键行注释**  
> - `target_sum = mean * total_len`：先算出所有掷骰子应该达到的总和。  
> - `need = target_sum - known_sum`：缺失的 n 次掷骰子必须凑出的总和。  
> - `if cur_sum > need: return None`：如果当前已经超过了需要的和，就没有必要继续往下搜索（剪枝）。  

#### 复杂度  

- **时间复杂度**：`O(6^n)` —— 需要尝试 6 的 n 次方种可能，随 n 指数增长，实际不可用。  
- **空间复杂度**：`O(n)` —— 递归栈深度和临时保存的路径列表均为 n。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **枚举所有可能**，这导致指数级的时间。其实我们并不需要知道每一种可能，只要判断是否存在一种组合即可，并且还能直接构造出一种合法的组合。

从暴力思路出发，我们先把「总和」这个关键量算出来：

1. **求目标总和**  
   所有 n+m 次掷骰子的平均值是 `mean`，所以  
   \[
   \text{target\_sum} = \text{mean} \times (n+m)
   \]  
   这一步可以类比「把所有人的工资加起来，除以人数等于平均工资」——先算出总工资。

2. **已知部分的和**  
   `known_sum = sum(rolls)`，把已经看到的 m 次掷骰子加起来。

3. **缺失部分需要的和**  
   \[
   \text{need} = \text{target\_sum} - \text{known\_sum}
   \]  
   这就是我们必须让 n 次缺失的掷骰子凑出的总和。

4. **合法性检查**  
   每一次掷骰子的结果只能是 1~6，n 次的最小可能和是 `n * 1`，最大可能和是 `n * 6`。因此必须满足  
   \[
   n \le \text{need} \le 6n
   \]  
   否则无论怎么填都达不到目标，直接返回空列表。

5. **构造答案**  
   当 `need` 落在合法区间时，我们可以很容易构造一种解：  
   - 先把所有 n 个位置都填成最小值 1，得到当前和 `cur = n`。  
   - 还差 `remain = need - cur`。我们把这 `remain` 均匀地加到前面的几个位置上，每个位置最多还能再加 `5`（因为 1+5=6）。  
   - 具体做法是遍历前 `remain // 5` 个位置，全部加到 6；剩余的 `remain % 5` 再加到下一个位置。这样得到的数组每个元素都在 1~6 之间，且总和恰好等于 `need`。  

   这一步相当于「先把每个人的工资定为最低的 1 万元，然后把剩余的钱尽量分配到前几个人，每个人最多只能涨到 6 万元」——简单而直接。

#### 代码（Python）

```python
from typing import List

def missingObservations(rolls: List[int], mean: int, n: int) -> List[int]:
    m = len(rolls)                                 # 已知的次数
    total_len = n + m                              # 总次数
    target_sum = mean * total_len                  # 所有掷骰子的目标总和
    known_sum = sum(rolls)                         # 已知部分的和
    need = target_sum - known_sum                  # 缺失 n 次需要凑的和

    # 合法性检查：need 必须在 [n, 6n] 之间
    if need < n or need > 6 * n:
        return []                                   # 无解

    # 初始化全部为 1
    res = [1] * n
    remain = need - n                               # 还需要再分配的 “额外” 和

    # 把额外的和尽量放到前面的元素上，每个最多再加 5（从 1 变到 6）
    idx = 0
    while remain > 0:
        add = min(5, remain)                        # 本次最多加 5
        res[idx] += add
        remain -= add
        idx += 1

    return res
```

> **关键行注释**  
> - `if need < n or need > 6 * n:`：判断是否在合法区间。  
> - `res = [1] * n`：先把每个缺失的掷骰子设成最小值 1。  
> - `add = min(5, remain)`：每次最多只能再加 5（因为 1+5=6），防止超过上限 6。  

#### 复杂度  

- **时间复杂度**：`O(n)`。只需要一次遍历（或几次常数次的循环）来分配剩余的和。相比暴力的 `O(6^n)`，这里随 n 线性增长，几乎是即时可算。  
- **空间复杂度**：`O(n)` 用来存放返回的数组。除了输出本身，没有额外的辅助空间。  

---

## 心得  

- **核心技巧**：把「平均值」转化为「总和」的约束，再利用「每个数的取值范围」做区间判断。  
- **适用的题型**  
  1. **求缺失元素的和**：如 “找出缺失的数组元素，使整体平均为指定值”。  
  2. **在给定区间内分配总和**：如 “把总分分配给若干学生，每人分数必须在 [L, R]”。  
  3. **构造满足 sum 限制的数组**：如 “给定数组长度和目标和，返回任意满足条件的正整数数组”。  
- **一句话总结**：**把平均值转成总和，再检查是否能在上下限内分配即可**。

---

## 反思  

- **第一反应**：看到“平均值”和“缺失的掷骰子”，自然想到先算出全部的总和，然后再考虑缺失部分的和。  
- **最容易踩的坑**  
  - 忘记 **总和必须是整数**，即 `mean * (n+m)` 必须能被 `n+m` 整除（题目已保证 `mean` 为整数，但仍要检查 `need` 是否在合法区间）。  
  - 没有考虑 **每个掷骰子只能在 1~6 之间**，导致构造的数组出现非法值。  
  - 对 `n`、`m` 很大时仍使用暴力搜索，会导致超时。  
- **下次遇到同类题**：第一步先 **写出目标总和公式**，随后 **判断是否能在每个位置的取值范围内完成**，最后 **按需分配**（先填最小值再逐步加）。这样可以在 O(n) 时间内直接得到答案。