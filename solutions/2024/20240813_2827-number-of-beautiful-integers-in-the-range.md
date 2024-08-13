# #2827. 区间内美丽整数的数量 / Number of Beautiful Integers in the Range

> 难度：困难 · 标签：Math、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/number-of-beautiful-integers-in-the-range/)

---

## 题目（英文原版）

**Description**

You are given positive integers low, high, and k.
A number is beautiful if it meets both of the following conditions:
Return the number of beautiful integers in the range [low, high].

**Examples**

**Example 1:**

```
Input: low = 10, high = 20, k = 3
Output: 2
Explanation: There are 2 beautiful integers in the given range: [12,18]. 
- 12 is beautiful because it contains 1 odd digit and 1 even digit, and is divisible by k = 3.
- 18 is beautiful because it contains 1 odd digit and 1 even digit, and is divisible by k = 3.
Additionally we can see that:
- 16 is not beautiful because it is not divisible by k = 3.
- 15 is not beautiful because it does not contain equal counts even and odd digits.
It can be shown that there are only 2 beautiful integers in the given range.
```

**Example 2:**

```
Input: low = 1, high = 10, k = 1
Output: 1
Explanation: There is 1 beautiful integer in the given range: [10].
- 10 is beautiful because it contains 1 odd digit and 1 even digit, and is divisible by k = 1.
It can be shown that there is only 1 beautiful integer in the given range.
```

**Example 3:**

```
Input: low = 5, high = 5, k = 2
Output: 0
Explanation: There are 0 beautiful integers in the given range.
- 5 is not beautiful because it is not divisible by k = 2 and it does not contain equal even and odd digits.
```

**Constraints**

- 0 < low <= high <= 109
- 0 < k <= 20

---

## 题目（中文翻译）

给定正整数 `low`、`high` 和 `k`。  

如果一个整数同时满足以下两个条件，则称其为**美丽整数**（beautiful integer）：

1. 该整数的奇数位数字（odd digit）与偶数位数字（even digit）的个数相等。  
2. 该整数能够被 `k` 整除。  

请返回区间 `[low, high]`（包含左右端点）内美丽整数的个数。

## 示例

### 示例 1  
**输入**: `low = 10, high = 20, k = 3`  
**输出**: `2`  
**解释**: 区间内共有 2 个美丽整数：`12`、`18`。  
- `12` 是美丽整数，因为它包含 1 个奇数位数字和 1 个偶数位数字，且能被 `k = 3` 整除。  
- `18` 是美丽整数，因为它包含 1 个奇数位数字和 1 个偶数位数字，且能被 `k = 3` 整除。  

另外可以看到：  
- `16` 不是美丽整数，因为它不能被 `k = 3` 整除。  

### 示例 2  
**输入**: `low = 1, high = 10, k = 1`  
**输出**: `1`  
**解释**: 区间内只有 1 个美丽整数：`10`。  
- `10` 是美丽整数，因为它包含 1 个奇数位数字和 1 个偶数位数字，且能被 `k = 1` 整除。  

可以证明，在该区间内不存在其他美丽整数。

### 示例 3  
**输入**: `low = 5, high = 5, k = 2`  
**输出**: `0`  
**解释**: 区间内没有美丽整数。  
- `5` 既不能被 `k = 2` 整除，也不满足奇偶位数字数量相等的条件。

## 约束条件

- `0 < low <= high <= 10^9`  
- `0 < k <= 20`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把区间 `[low, high]` 里的每一个整数都枚举一遍，逐个判断它是否满足“**偶数位数 = 奇数位数 且 能被 k 整除**”。  
- **遍历**：用 `for num in range(low, high+1)` 把每个数都拿出来。  
- **统计奇偶位数**：把整数转成字符串（或不断 `//10` 取余），检查每一位是奇数还是偶数，分别计数。  
- **可比作查字典**：这里的“奇偶位数计数”有点像在字典里查词，键是“奇数/偶数”，值是出现的次数。  
- **可被 k 整除**：直接用 `%` 运算符判断 `num % k == 0`。

只要这三个条件都满足，就把答案加一。  

> **为什么能得对**  
> 这是一种**完全枚举**的做法，遍历了所有可能的数，自然不会漏掉任何符合条件的整数，也不会误计不符合条件的数。

#### 代码（Python）

```python
def count_beautiful_bruteforce(low: int, high: int, k: int) -> int:
    """暴力枚举 low~high，统计满足条件的整数个数"""
    ans = 0
    for num in range(low, high + 1):
        # 1. 判断是否能被 k 整除
        if num % k != 0:
            continue                     # 直接跳过，不满足

        # 2. 统计奇数位数和偶数位数
        odd_cnt, even_cnt = 0, 0
        tmp = num
        while tmp > 0:                   # 逐位取出数字
            digit = tmp % 10
            if digit % 2 == 0:           # 偶数位
                even_cnt += 1
            else:                        # 奇数位
                odd_cnt += 1
            tmp //= 10

        # 3. 判断奇偶位数是否相等
        if odd_cnt == even_cnt:
            ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O((high‑low+1) * log10(high))`  
  - 解释：对每个数都要遍历它的所有十进制位（位数约为 `log10(high)`），所以总共是区间长度乘以位数。若区间宽度是 10⁹，时间会达到 **十亿级**，在实际运行中会超时。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量，不随输入规模增长。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **“逐个枚举每个整数”**。我们需要一种方法，**一次性统计** 所有满足条件的数，而不是一个一个检查。  

**核心想法 → 数位 DP（Digit DP）**  
数位 DP 的核心是：**把“从左到右逐位构造数字”** 看成一次状态转移过程。我们只需要记住构造到当前位置时已经拥有的关键信息，后面的每一位的取值都可以在这些信息的基础上继续扩展。  

对于本题，需要在 DP 中保存以下信息：

| 状态 | 含义 | 为什么需要 |
|------|------|-------------|
| `pos` | 当前处理的是第几位（从最高位到最低位） | 控制递归深度 |
| `tight` | 前缀是否已经和上界 `n` 完全相同（即是否受限） | 保证生成的数 ≤ n |
| `started` | 是否已经出现过非前导零（即数字是否真的开始了） | 前导零不算作奇偶位 |
| `diff` | `even_cnt - odd_cnt` 的差值（范围 `[-len, len]`） | 最终要求差值为 0 |
| `mod` | 当前已构造的数对 `k` 的余数 | 最终要求余数为 0 |

> **类比**：把 DP 看成在玩“拼图”。每放一块（确定一位数字），就要记录下“已经拼好的形状”（`diff`、`mod`）以及“还能往哪儿拼”（`tight`、`started`）。

**步骤**  

1. **把问题转化为前缀计数**  
   设 `f(n)` 为 `[1 … n]` 区间内符合条件的整数个数。  
   所求答案 = `f(high) - f(low-1)`。这样只需要实现一次“≤ n”的计数函数。  

2. **递归定义**  
   `dfs(pos, diff, mod, started, tight)` 返回从当前位置 `pos` 开始，满足已记录状态的合法数的个数。  

   - **结束条件**：当 `pos == len(digits)`（已经处理完最高位到最低位）  
     - 如果 `started` 为真且 `diff == 0` 且 `mod == 0`，说明构造出一个合法整数，返回 1；否则返回 0。  

   - **转移**：枚举当前位可以放的数字 `d`（`0 … upper`），其中 `upper = digits[pos]` 若 `tight` 为真，否则为 9。  
     - 若 `started` 仍为假且 `d == 0`，说明仍在前导零阶段：`new_started = False`，`new_diff = diff`，`new_mod = mod`（保持不变）。  
     - 否则进入“正式数字”阶段：  
       - `new_started = True`  
       - 更新奇偶差：`new_diff = diff + (1 if d%2==0 else -1)`（偶数让差值加 1，奇数让差值减 1）  
       - 更新模数：`new_mod = (mod * 10 + d) % k`  

     - `new_tight = tight and (d == upper)`  
     - 将子问题的返回值累加。  

3. **记忆化**  
   由于 `pos ≤ 10`、`diff ∈ [-10,10]`、`mod < k ≤ 20`、`started∈{0,1}`、`tight∈{0,1}`，状态总数不到两万，使用 `@lru_cache` 进行记忆化即可秒算完。  

4. **调用**  
   把 `n` 的十进制位拆成列表 `digits`（从最高位到最低位），然后调用 `dfs(0, 0, 0, False, True)`。  

**复杂度**  

- **时间**：`O(len * diff_range * k * 2 * 2)` ≈ `O(10 * 21 * 20) ≈ 4,200`，几乎是常数级，远快于暴力。  
- **空间**：递归栈深度 `O(len)`（≤10） + 记忆化表的状态数，约几千个整数，仍然是 `O(1)` 级别的内存。

#### 代码（Python）

```python
from functools import lru_cache

def count_beautiful_upto(n: int, k: int) -> int:
    """
    返回区间 [1, n] 中满足
        1) 偶数位数 == 奇数位数
        2) 能被 k 整除
    的整数个数。
    """
    if n <= 0:                     # 低于 1 的情况直接返回 0
        return 0

    digits = list(map(int, str(n)))    # 最高位在前，例: 123 -> [1,2,3]
    L = len(digits)
    OFFSET = L                         # 用来把 diff 负数转成非负索引

    @lru_cache(maxsize=None)
    def dfs(pos: int, diff: int, mod: int, started: bool, tight: bool) -> int:
        """
        pos   : 当前处理到第几位（0 为最高位）
        diff  : 偶数位数 - 奇数位数 的差值（已加上 OFFSET 方便缓存）
        mod   : 已构造数字 % k 的余数
        started: 是否已经出现过非前导零
        tight : 前缀是否仍然等于 n 的前缀（若 True 则本位上限是 digits[pos]）
        """
        if pos == L:                       # 所有位都决定完毕
            # 必须已经真正构造出一个数（started），且差值为 0，余数为 0
            return int(started and diff == OFFSET and mod == 0)

        limit = digits[pos] if tight else 9   # 本位能放的最大数字
        total = 0

        for d in range(limit + 1):
            new_started = started or d != 0   # 一旦出现非零，started 变 True
            new_diff = diff
            new_mod = mod

            if new_started:                  # 进入正式数字阶段才更新状态
                # 更新奇偶差值（偶数 +1，奇数 -1）
                if d % 2 == 0:
                    new_diff += 1
                else:
                    new_diff -= 1
                # 更新模数
                new_mod = (mod * 10 + d) % k

            # tight 只能在前缀仍然相等且本位取到上限时保持 True
            new_tight = tight and (d == limit)
            total += dfs(pos + 1, new_diff, new_mod, new_started, new_tight)

        return total

    # 初始 diff 用 OFFSET 把 0 映射为中间位置，mod 初始为 0
    return dfs(0, OFFSET, 0, False, True)


def number_of_beautiful_integers(low: int, high: int, k: int) -> int:
    """主函数：返回区间 [low, high] 中的美丽整数个数"""
    return count_beautiful_upto(high, k) - count_beautiful_upto(low - 1, k)


# ------------------- 示例测试 -------------------
if __name__ == "__main__":
    print(number_of_beautiful_integers(10, 20, 3))   # 2
    print(number_of_beautiful_integers(1, 10, 1))    # 1
    print(number_of_beautiful_integers(5, 5, 2))     # 0
```

#### 复杂度  

- **时间复杂度**：`O(L * (2L+1) * k)`，其中 `L = len(str(high)) ≤ 10`，`k ≤ 20`。实际运行时间在几千次递归调用内，几乎是常数级，远快于暴力的 `O((high‑low)·L)`。  
- **空间复杂度**：`O(L * (2L+1) * k)` 用于缓存，最多约 `10·21·20 ≈ 4,200` 条记录，加上递归深度 `O(L)`，整体仍然是 `O(1)`（相对于输入规模而言）。

---

## 心得  

- **核心技巧**：**数位动态规划（Digit DP）**——把“满足某些数位属性的整数计数”转化为逐位构造并记忆状态。  
- **适用题型**（可举 2‑3 个类似）：  
  1. “统计区间内数字之和能被 k 整除的数”。  
  2. “统计区间内回文数或递增数”。  
  3. “统计区间内满足特定位数出现次数限制的数（如不出现数字 4）”。  
- **一句话总结解题钥匙**：**把“遍历每个数”换成“遍历每个位的可能”，用 DP 把所有合法路径一次性算完**。

---

## 反思  

- **第一反应**：看到“区间、奇偶位数、可被 k 整除”就想到直接枚举检查。  
- **最容易踩的坑**：  
  - **前导零的处理**：如果把前导零算进奇偶位会导致错误，需要用 `started` 标记是否已经出现非零位。  
  - **差值的负数**：`even - odd` 可能为负，记忆化时必须把它平移（加上 `OFFSET`）才能作为数组/缓存的下标。  
  - **模数的更新**：在还未正式开始（仍是前导零）时不应更新 `mod`，否则会把零当成有效数字。  
- **下次遇到同类题**：第一步先**把问题转化为“≤ n 的计数”**，再考虑使用**数位 DP**，先明确需要记录的状态（如奇偶差、模数、是否已开始），最后写递归并加记忆化。