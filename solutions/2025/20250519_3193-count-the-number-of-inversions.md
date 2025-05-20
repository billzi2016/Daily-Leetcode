# #3193. 计数逆序对的数量 / Count the Number of Inversions

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-inversions/)

---

## 题目（英文原版）

**Description**

You are given an integer n and a 2D array requirements, where requirements[i] = [endi, cnti] represents the end index and the inversion count of each requirement.
A pair of indices (i, j) from an integer array nums is called an inversion if:
Return the number of permutations perm of [0, 1, 2, ..., n - 1] such that for all requirements[i], perm[0..endi] has exactly cnti inversions.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 3, requirements = [[2,2],[0,0]]
Output: 2
Explanation:
The two permutations are:
```

**Example 2:**

```
Input: n = 3, requirements = [[2,2],[1,1],[0,0]]
Output: 1
Explanation:
The only satisfying permutation is [2, 0, 1] :
```

**Example 3:**

```
Input: n = 2, requirements = [[0,0],[1,0]]
Output: 1
Explanation:
The only satisfying permutation is [0, 1] :
```

**Constraints**

- 2 <= n <= 300
- 1 <= requirements.length <= n
- requirements[i] = [endi, cnti]
- 0 <= endi <= n - 1
- 0 <= cnti <= 400
- The input is generated such that there is at least one i such that endi == n - 1.
- The input is generated such that all endi are unique.

---

## 题目（中文翻译）

给定一个整数 `n` 和一个二维数组 `requirements`，其中 `requirements[i] = [endi, cnti]` 表示第 `i` 个约束的结束下标 `endi` 以及逆序对（inversion）数量 `cnti`。  

在整数数组 `nums` 中，如果一对下标 `(i, j)` 满足 `i < j` 且 `nums[i] > nums[j]`，则称其为一个 **逆序对**。  

返回满足以下条件的全排列 `perm`（`perm` 为 `[0, 1, 2, ..., n - 1]` 的任意排列）的数量：对所有 `requirements[i]`，子数组 `perm[0..endi]` 恰好包含 `cnti` 个逆序对。  

由于答案可能非常大，请返回其对 `10^9 + 7` 取模后的结果。  

**示例 1**  
**输入**: `n = 3, requirements = [[2,2],[0,0]]`  
**输出**: `2`  
**解释**:  
满足条件的两个排列为  
- `[1, 2, 0]`  
- `[2, 1, 0]`  

**示例 2**  
**输入**: `n = 3, requirements = [[2,2],[1,1],[0,0]]`  
**输出**: `1`  
**解释**:  
唯一满足的排列是 `[2, 0, 1]`。  

**示例 3**  
**输入**: `n = 2, requirements = [[0,0],[1,0]]`  
**输出**: `1`  
**解释**:  
唯一满足的排列是 `[0, 1]`。  

**约束条件**  
- `2 <= n <= 300`  
- `1 <= requirements.length <= n`  
- `requirements[i] = [endi, cnti]`  
- `0 <= endi <= n - 1`  
- `0 <= cnti <= 400`  
- 输入保证至少存在一个 `i` 使得 `endi == n - 1`。  
- 输入保证所有 `endi` 均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有排列**，然后逐个统计每个前缀的逆序对数是否满足 `requirements`。  
- **排列**：把 `[0,1,2,…,n-1]` 的所有可能顺序列出来。可以用 Python 的 `itertools.permutations`。
- **逆序对**（inversion）：在数组 `nums` 中，如果下标 `i < j` 且 `nums[i] > nums[j]`，则 `(i,j)` 是一次逆序。  
  想象一排学生站好，左边的同学如果比右边的高，就算一次“倒立”。遍历所有 `(i,j)` 组合并计数即可。
- **前缀检查**：`requirements` 给出若干 `(endi, cnti)`，意思是「从下标 `0` 到 `endi`（包含）这段子数组的逆序对数必须恰好是 `cnti`」。遍历完一个排列后，逐个检查这些条件是否成立。

> 为什么这个方法一定能得到正确答案？  
> 因为我们把 **所有可能** 的排列都穷举了，只要有满足条件的排列，一定会在枚举过程中被找到；不满足的自然会被过滤掉。

**时间/空间分析（大白话）**  
- 枚举排列的数量是 `n!`（n 的阶乘），比如 `n=8` 时已经是 40320 种。  
- 对每个排列我们要遍历 `O(n²)` 次才能统计所有逆序对（每两个位置比较一次）。  
- 所以总时间是 `O(n! * n²)`，即**非常非常慢**，只能在 `n≤8` 左右的极小输入里跑得动。  
- 空间上只需要保存当前排列和计数，`O(n)`。

#### 代码（Python）

```python
import itertools
from typing import List

MOD = 10 ** 9 + 7

def brute_count(n: int, requirements: List[List[int]]) -> int:
    # 把 requirements 转成字典，方便 O(1) 查表
    req = {end: cnt for end, cnt in requirements}

    ans = 0
    # 1. 枚举所有排列
    for perm in itertools.permutations(range(n)):
        # 2. 计算前缀逆序对数
        inv_prefix = [0] * n          # inv_prefix[i] = 逆序对数(0..i)
        cur = 0                       # 当前累计的逆序对数
        for i in range(n):
            # 统计 i 位置左边比 perm[i] 大的元素个数
            larger = sum(1 for k in range(i) if perm[k] > perm[i])
            cur += larger
            inv_prefix[i] = cur

        # 3. 检查所有要求是否满足
        ok = True
        for end, cnt in req.items():
            if inv_prefix[end] != cnt:
                ok = False
                break
        if ok:
            ans = (ans + 1) % MOD
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n! * n²)`  
  - `n!` 是排列的总数，`n²` 是每个排列统计逆序对的代价。  
  - 用大白话说，就是「先把所有可能的排好队，然后每队里再找两两比高低」，所以指数级慢。
- **空间复杂度**：`O(n)`  
  - 只保存当前排列和前缀计数数组，和 `n` 成正比。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举排列**（`n!`）和 **逐对比较**（`n²`）。  
我们需要 **不枚举具体排列**，而是直接统计「有多少种长度为 `i`、逆序对数为 `j` 的排列」——这正是 **动态规划**（DP）可以完成的任务。

---

#### 2.1 逆序对的 DP 公式

设 `dp[i][j]` 为「使用前 `i` 个数（即 `0…i-1`）构造的排列中，逆序对数恰好为 `j` 的种数」。  
当我们在已有 `i‑1` 个数的排列上插入第 `i` 个数（值为 `i-1`），它可以插在 **任意位置**，每往左移动一格就会多产生一个逆序对。  
因此：

```
dp[i][j] = dp[i-1][j]        // 插到最右边，不产生新逆序
          + dp[i-1][j-1]    // 插到倒数第二位，产生 1 个逆序
          + … + dp[i-1][j-(i-1)]   // 插到最左边，最多产生 (i-1) 个逆序
```

如果 `j` 小于 0 或超过最大可能逆序（`i*(i-1)/2`），对应的 `dp` 为 0。

**前缀约束**  
题目要求在若干特定的前缀 `endi` 上逆序对数必须等于 `cnti`。  
我们可以在 DP 过程中 **“强制”** 某些状态为 0：  
- 当正在计算 `i = endi + 1`（因为 `dp` 的下标 `i` 表示已经放入了 `i` 个数，对应前缀长度 `i-1`），
- 若 `j != cnti`，则 `dp[i][j] = 0`（不符合要求的逆序数直接抹掉）。

这样，所有不满足任何约束的排列在最终计数时自然消失。

---

#### 2.2 前缀和加速

直接套用上面的递推式，需要对每个 `dp[i][j]` 再遍历 `i` 项，整体是 `O(n³)`（`n≈300` 会超时）。  
观察公式，它其实是 **一个滑动窗口的前缀和**：

```
dp[i][j] = dp[i][j-1] + dp[i-1][j] - (j-i >= 0 ? dp[i-1][j-i] : 0)
```

解释：  
- `dp[i][j-1]` 已经包含了 `dp[i-1][j-1] + … + dp[i-1][j-(i-1)]`（不包括 `dp[i-1][j]`）。  
- 加上 `dp[i-1][j]` 就得到完整的和。  
- 若 `j-i >= 0`，我们多加了 `dp[i-1][j-i]`（窗口左边界之外的那一项），需要减掉。

这样每个状态只用 **常数时间** 计算，总复杂度降到 `O(n * maxInv)`，其中 `maxInv` 是所有要求中最大的 `cnti`（题目上限 400），即约 `300 * 400 = 1.2e5`，轻松通过。

---

#### 2.3 实现细节

1. **确定 DP 表大小**  
   - 行数：`n+1`（从 `0` 个数到 `n` 个数）。  
   - 列数：`max_cnt + 1`，`max_cnt = max(cnti)`，因为我们只关心到最大要求的逆序数。  
   - 对于不需要的更大逆序数，直接视为 0，省空间。

2. **初始化**  
   - `dp[0][0] = 1`：空数组只有一种，逆序对数 0。  
   - 其余 `dp[0][j] = 0`。

3. **遍历 i**（放入第 `i` 个数）  
   - 用前缀和公式填整行 `dp[i][*]`。  
   - 检查是否有约束 `endi == i-1`，若有则把不等于 `cnti` 的列全部置零。

4. **答案**  
   - 题目保证至少有一个约束的 `endi == n-1`，所以我们只需返回 `dp[n][cnt]` 中满足最后约束的那一个（若有多个约束在同一 `endi`，因为 `endi` 唯一，这里只有一个）。  
   - 若没有约束恰好在 `n-1`，则答案是所有 `j` 的和，但题目已经排除这种情况。

5. **取模**  
   - 所有加减操作均取模 `MOD = 10**9 + 7`，防止整数溢出。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def countInversions(n: int, requirements: List[List[int]]) -> int:
    """
    dp[i][j] :  使用前 i 个数 (0..i-1) 构成的排列中，逆序对数恰好为 j 的种数
    """
    # 把要求转成字典，方便 O(1) 查询
    req = {end: cnt for end, cnt in requirements}
    max_cnt = max(cnt for _, cnt in requirements)          # 只需要算到最大的 cnt

    # dp 只保留前一行和当前行，省空间
    dp_prev = [0] * (max_cnt + 1)
    dp_prev[0] = 1                                          # 空数组

    for i in range(1, n + 1):                               # i 表示已经放入 i 个数
        dp_cur = [0] * (max_cnt + 1)
        # 通过滑动窗口前缀和计算 dp[i][*]
        window_sum = 0
        for j in range(0, max_cnt + 1):
            # 把 dp[i-1][j] 加入窗口
            window_sum = (window_sum + dp_prev[j]) % MOD
            # 如果窗口宽度超过 i，就把最左边的值踢出
            if j - i >= 0:
                window_sum = (window_sum - dp_prev[j - i]) % MOD
            dp_cur[j] = window_sum

        # ---------- 处理约束 ----------
        end_idx = i - 1                                      # 对应的前缀长度
        if end_idx in req:                                   # 有要求要强制
            target = req[end_idx]
            # 只保留恰好等于 target 的列，其余置零
            for j in range(max_cnt + 1):
                if j != target:
                    dp_cur[j] = 0

        dp_prev = dp_cur                                     # 换行

    # 最终答案：因为题目保证存在 endi == n-1 的约束
    final_cnt = req[n - 1]                                   # 必须满足的逆序数
    return dp_prev[final_cnt] % MOD
```

#### 复杂度

- **时间复杂度**：`O(n * max_cnt)`  
  - `n ≤ 300`，`max_cnt ≤ 400`，所以最多约 `1.2 × 10⁵` 次循环，几乎是瞬间完成。  
  - 与暴力解的 `O(n!·n²)` 相比，指数级的差距变成了线性乘积，速度提升 **天文级**。

- **空间复杂度**：`O(max_cnt)`  
  - 只保存两行 DP（`dp_prev`、`dp_cur`），每行长度为 `max_cnt+1 ≤ 401`，几乎可以忽略不计。  
  - 与暴力的 `O(n)`（存排列）相比，仍然是常数级别的内存使用。

---

## 心得

- **核心技巧**：**利用插入位置的逆序贡献建立 DP**（即“把第 i 个数插到已有排列的每个可能位置”），并用**滑动窗口前缀和**把三重循环降到线性。
- **适用的题型**  
  1. **统计逆序对数的排列数量**（如 LeetCode 629 “K Inverse Pairs Array”）。  
  2. **带前缀约束的计数问题**（如本题，需要在特定前缀满足特定逆序数）。  
  3. **插入式 DP**（把新元素插入已有结构，产生额外的计数或代价），常见于“排列”“组合”类计数。
- **一句话总结解题钥匙**：  
  “把‘把第 i 个数放进已有排列的每个位置’的思路转化为 DP，配合前缀和让每一步只用 O(1) 时间。”

---

## 反思

- **第一反应**：直接想枚举所有排列，然后逐个检查——这在没有想到 DP 前，最自然的冲动。
- **最容易踩的坑**  
  1. **逆序对上限**：`i` 个数的最大逆序对是 `i*(i-1)//2`，如果 `cnti` 超出这个范围，答案必为 0，需要提前返回。  
  2. **模运算负数**：在窗口滑动时做 `window_sum = (window_sum - dp_prev[j-i]) % MOD`，Python 的 `%` 会把负数转成正数，但写成 `(window_sum - val + MOD) % MOD` 更安全。  
  3. **约束冲突**：如果同一个 `endi` 对应多个不同的 `cnti`（题目已保证唯一），则答案直接 0。实现时可以在读取 `requirements` 时检测冲突。  
  4. **忘记把 `dp[0][0]=1` 初始化**，导致所有计数都是 0。

- **下次遇到类似题**：  
  第一步先思考「是否可以用插入式 DP 把排列计数转化为状态转移」；  
  第二步检查是否有额外的**前缀/后缀约束**，如果有，就在 DP 进行到对应长度时强制不符合的状态为 0；  
  第三步寻找**前缀和/滑动窗口**等技巧，避免 O(n³) 的暴力递推。