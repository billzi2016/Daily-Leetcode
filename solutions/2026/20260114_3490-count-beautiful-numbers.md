# #3490. 统计美丽数字 / Count Beautiful Numbers

> 难度：困难 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-beautiful-numbers/)

---

## 题目（英文原版）

**Description**

You are given two positive integers, l and r. A positive integer is called beautiful if the product of its digits is divisible by the sum of its digits.
Return the count of beautiful numbers between l and r, inclusive.

**Examples**

**Example 1:**

```
Input: l = 10, r = 20
Output: 2
Explanation:
The beautiful numbers in the range are 10 and 20.
```

**Example 2:**

```
Input: l = 1, r = 15
Output: 10
Explanation:
The beautiful numbers in the range are 1, 2, 3, 4, 5, 6, 7, 8, 9, and 10.
```

**Constraints**

- 1 <= l <= r < 109

---

## 题目（中文翻译）

给定两个正整数 `l` 和 `r`。若一个正整数的各数位的乘积能够被其各数位的和整除，则称该整数为美丽数。返回区间 `[l, r]`（两端均包含）内美丽数的数量。

**示例 1：**
```
Input: l = 10, r = 20
Output: 2
Explanation:
区间内的美丽数为 10 和 20。
```

**示例 2：**
```
Input: l = 1, r = 15
Output: 10
Explanation:
区间内的美丽数为 1、2、3、4、5、6、7、8、9 和 10。
```

**约束条件：**
- `1 <= l <= r < 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把区间 `[l, r]` 里的每一个整数都枚举一遍，  
- 把它的每一位数字取出来，累加得到 **数字和** `sum`，  
- 同时把每一位数字相乘得到 **数字积** `prod`，  
- 判断 `prod % sum == 0`（即“积能被和整除”），如果成立就把计数器加一。  

这里用到的唯一数据结构是 **列表**（或字符串）来保存每个数字的各位，  
把它想象成把一本书的每一页（每一位）翻出来读一遍，就像查字典时把每个词条都读一遍一样。  

因为我们对每个数都做了完整的检查，这个方法一定是 **正确** 的——只要遍历完整个区间，就不会漏掉任何可能的 “beautiful number”。  

**复杂度分析（大白话）**  
- 区间长度最多是 `r - l + 1`，每个数最多有 `log10(r) ≈ 9` 位。  
- 所以总共要做的工作大约是 “区间大小 × 位数”。  
- 用数学符号写就是 **时间复杂度 O((r‑l+1)·log r)**，  
  对于本题的约束 `r < 10⁹`，最坏情况是 `10⁹` 次循环——在计算机里根本跑不完。  
- 只用了常数级的额外空间（几个整数），所以 **空间复杂度 O(1)**。

#### 代码（Python）

```python
def count_beautiful_bruteforce(l: int, r: int) -> int:
    """暴力枚举 l~r，返回 beautiful numbers 的个数"""
    ans = 0
    for num in range(l, r + 1):
        s = 0          # 数字和
        p = 1          # 数字积，先设为 1（乘法的单位元）
        x = num
        while x > 0:
            d = x % 10          # 取最低位
            s += d
            p *= d
            x //= 10
        # 注意：当任意一位是 0 时，p 会变成 0，0 能被任何正数整除
        if p % s == 0:
            ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O((r‑l+1)·log₁₀ r)`  
  → “每个数要看它的每一位”，如果 `r≈10⁹`，相当于十亿次 * 9 位的操作，远远超时。  
- **空间复杂度**：`O(1)`  
  → 只用了几个整数变量，不随输入规模增长。

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在于 **逐个枚举每个整数**，而我们只关心它们的「位数」信息（每位的数字），而不需要真的把所有数写出来。  
这类只依赖“数位”特征的计数问题，常用的技巧叫 **数位 DP（Digit Dynamic Programming）**。  

**数位 DP 的核心想法**  
把一个整数看成一串固定长度的“字符”（每个字符是 0~9），  
从高位往低位依次决定每一位取什么数字，同时记录下已经决定的位对 “数字和” 与 “数字积” 的影响。  
只要在遍历的过程中记住：

1. **已经累计的数字和** `sum`（最大 9 位 × 9 = 81）  
2. **已经累计的数字积** `prod`（最大 9⁹ ≈ 3.87×10⁸）  
3. **是否已经出现过非前导零** `started`（用来区分“前导零”与真实数字）  

以及 **当前是否受上界限制** `tight`（如果前面已经小于上界，那么后面的位可以随意取 0~9），  
我们就可以用 **记忆化递归**（或 DP 表）把所有可能的状态合并计算，而不是逐个枚举完整的整数。  

**为什么这样更快？**  
- 状态数远小于 `r‑l+1`。  
- 对于同一个 `pos、sum、prod、started` 的组合，无论它是从哪条路径得到的，后面的子问题完全相同，只需要算一次，后面直接复用。  

**状态设计**  

| 参数 | 含义 | 取值范围 |
|------|------|----------|
| `pos` | 当前处理的是第几位（从最高位 0 开始） | `0 … n`（`n` 为数字位数） |
| `sum` | 已经累加的数字和 | `0 … 81` |
| `prod` | 已经累计的数字积（乘法单位元 1） | 0 或 1 … 9⁹（实际出现的种类只有几千） |
| `started` | 是否已经选到过非前导零 | `0/1` |
| `tight` | 前缀是否严格等于上界的前缀 | `0/1`（tight=1 时本位只能取 ≤ 上界对应位） |

**递归定义**  

`dfs(pos, sum, prod, started, tight)` → 在 `pos` 位置以后还能构造出多少个 **beautiful** 数。  

- 递归终止：`pos == n`（已经处理完所有位）  
  - 若 `started == 0` → 代表全是前导零，即没有形成合法正整数，返回 0。  
  - 否则检查 `prod % sum == 0`，满足则返回 1，否则返回 0。  

- 转移：遍历本位可以放的数字 `d`（上界由 `tight` 决定），  
  - `new_started = started or d != 0`  
  - `new_sum = sum + d`（只有真正开始计数后才加）  
  - `new_prod = prod * d`（若 `new_started` 为真且 `d==0`，`new_prod` 立即变 0；若仍在前导零阶段，保持 `prod` 为 1）  
  - `new_tight = tight and (d == limit)`  

把所有 `d` 的结果相加即为当前状态的答案。  

**记忆化**  
- 当 `tight == 0`（已经小于上界）时，后面的位可以随意取 0~9，状态完全由 `(pos, sum, prod, started)` 决定，直接缓存。  
- `tight == 1` 的情况只能在当前递归层直接计算，不缓存（因为上界不同，状态不通用）。  

**实现细节**  

- 为了避免乘积溢出或状态爆炸，注意：  
  - 当出现 `0`，后面的乘积永远是 `0`，这是一种特殊且非常常见的状态，直接保存为 `0`。  
  - 实际可到达的 `(sum, prod)` 组合非常有限（几千个），使用 `dict`（哈希表）做缓存即可，哈希表就像“查字典”，`key` 是 `(pos, sum, prod, started)`，`value` 是对应的计数。  
- 为了统一处理 “没有数字” 的情况，递归入口把 `prod` 初始化为 `1`（乘法的单位元），这样在第一次真正取到非零数字时 `prod * d` 就是该数字本身。  

**整体思路图（文字版）**  

```
count_up_to(X):
    digits = list of X's decimal digits (high → low)
    return dfs(0, 0, 1, False, True)

dfs(pos, sum, prod, started, tight):
    if pos == len(digits):
        if not started: return 0
        return 1 if prod % sum == 0 else 0
    if not tight and memo contains (pos,sum,prod,started):
        return memo[(pos,sum,prod,started)]

    limit = digits[pos] if tight else 9
    total = 0
    for d in 0..limit:
        ns = started or d!=0
        nsum = sum + d if ns else sum
        nprod = prod * d if ns else prod
        ntight = tight and (d == limit)
        total += dfs(pos+1, nsum, nprod, ns, ntight)

    if not tight:
        memo[(pos,sum,prod,started)] = total
    return total
```

最后答案为 `count_up_to(r) - count_up_to(l-1)`，因为我们统计的是 **≤ X** 的数量。

#### 代码（Python）

```python
from functools import lru_cache

def count_beautiful(l: int, r: int) -> int:
    """返回区间 [l, r] 中 beautiful numbers 的个数（最优解）"""
    def count_up_to(x: int) -> int:
        if x <= 0:          # 没有正整数
            return 0
        digits = list(map(int, str(x)))   # 高位到低位的数组
        n = len(digits)

        @lru_cache(maxsize=None)
        def dfs(pos: int, cur_sum: int, cur_prod: int,
                started: int, tight: int) -> int:
            """返回从 pos 开始可以构造的 beautiful numbers 数量"""
            if pos == n:                     # 已经处理完所有位
                if not started:              # 全是前导零 → 不计数
                    return 0
                # 此时 sum>0，prod 可能为 0
                return 1 if cur_prod % cur_sum == 0 else 0

            # 当 tight==0 时可以缓存，lru_cache 已经帮我们记忆化
            limit = digits[pos] if tight else 9
            total = 0
            for d in range(limit + 1):
                new_started = started or d != 0
                new_sum = cur_sum + d if new_started else cur_sum
                # 乘积的单位元是 1；若还没有正式开始，则保持 1
                new_prod = cur_prod * d if new_started else cur_prod
                new_tight = tight and (d == limit)
                total += dfs(pos + 1, new_sum, new_prod,
                             new_started, new_tight)
            return total

        # 初始状态：位置 0，和 0，积 1（乘法单位元），未开始，tight 为 True
        return dfs(0, 0, 1, 0, 1)

    return count_up_to(r) - count_up_to(l - 1)
```

**代码要点注释**  

- `digits = list(map(int, str(x)))` 把整数拆成每一位，像把一本书的每页编号出来。  
- `@lru_cache` 相当于把已经算好的“章节”（状态）记在字典里，下次直接翻页取值，省去重复计算。  
- `started` 用 `0/1` 表示是否已经出现非前导零，防止把前面的 “0” 当成真的数字去累加。  
- `tight` 为 `1` 时表示当前前缀仍然等于上界前缀，必须受限；为 `0` 时已经“小于”，后面的位可以随意填 `0~9`，这时状态可以被缓存。  
- 递归终止时检查 `cur_prod % cur_sum == 0`，这正是题目对 “beautiful” 的定义。

#### 复杂度  

- **时间复杂度**：  
  - 状态数 ≈ `len(digits) * (max_sum+1) * (#different prod)`。  
  - `len(digits) ≤ 9`，`max_sum = 81`，实际出现的 `prod` 组合只有几千个（因为只能由 1~9 相乘），所以总体状态在 **几万级别**。  
  - 每个状态遍历至多 10 个子数字，整体约为 `O(9 * 81 * 4000 * 10) ≈ 3×10⁶`，在 1 秒内轻松跑完。  
  - 与暴力的 `O((r‑l)·log r)`（最坏 10⁹）相比，提升了 **数十万倍**。  

- **空间复杂度**：  
  - 记忆化表保存所有状态，最多几万条记录，每条只占几个整数，约 **几 MB**，记作 `O(9 * 81 * #prod)` → 实际上是 `O(1)`（常数级）因为上限是固定的 9 位。  

---

## 心得  

- **核心技巧**：**数位动态规划（Digit DP）**——把“在区间内计数”转化为“逐位构造”，并利用记忆化消除重复子问题。  
- **适用题型**（类似题目）  
  1. “统计区间内数字和能被数字本身整除的数”。  
  2. “统计区间内各位数字之和等于某个给定值的数”。  
  3. “统计区间内数字各位乘积为奇数的数”。  
- **一句话总结解题钥匙**：**把整个区间压缩成“每一位可以怎么走”，用 DP 把相同的子路径合并计数**。

## 反思  

- **第一反应**：直接写暴力循环，随后发现会超时。  
- **最容易踩的坑**  
  - **前导零**：没有把 “还没开始” 的状态区分开，会导致把 `0` 计入数字和/积，出现错误。  
  - **乘积为 0**：一旦出现 0，后面的乘积永远是 0，必须在状态转移时正确处理。  
  - **上界限制（tight）**：忘记在递归时把 `tight` 传递下去，导致计数超出区间。  
- **下次思路**：一看到“区间内满足位数相关的某种性质”，第一步就想到 **数位 DP**，先写 `count_up_to(X)`，再用前缀差得到区间答案。这样可以避免从枚举开始的误区。