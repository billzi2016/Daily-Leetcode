# #2698. **求整数的惩罚数** / Find the Punishment Number of an Integer

> 难度：中等 · 标签：Math、Backtracking · [LeetCode 链接](https://leetcode.com/problems/find-the-punishment-number-of-an-integer/)

---

## 题目（英文原版）

**Description**

Given a positive integer n, return the punishment number of n.
The punishment number of n is defined as the sum of the squares of all integers i such that:

**Examples**

**Example 1:**

```
Input: n = 10
Output: 182
Explanation: There are exactly 3 integers i in the range [1, 10] that satisfy the conditions in the statement:
- 1 since 1 * 1 = 1
- 9 since 9 * 9 = 81 and 81 can be partitioned into 8 and 1 with a sum equal to 8 + 1 == 9.
- 10 since 10 * 10 = 100 and 100 can be partitioned into 10 and 0 with a sum equal to 10 + 0 == 10.
Hence, the punishment number of 10 is 1 + 81 + 100 = 182
```

**Example 2:**

```
Input: n = 37
Output: 1478
Explanation: There are exactly 4 integers i in the range [1, 37] that satisfy the conditions in the statement:
- 1 since 1 * 1 = 1. 
- 9 since 9 * 9 = 81 and 81 can be partitioned into 8 + 1. 
- 10 since 10 * 10 = 100 and 100 can be partitioned into 10 + 0. 
- 36 since 36 * 36 = 1296 and 1296 can be partitioned into 1 + 29 + 6.
Hence, the punishment number of 37 is 1 + 81 + 100 + 1296 = 1478
```

**Constraints**

- 1 <= n <= 1000

---

## 题目（中文翻译）

给定一个正整数 `n`，返回 `n` 的惩罚数（punishment number）。

**定义**  
`n` 的惩罚数是所有满足以下条件的整数 `i`（`1 ≤ i ≤ n`）的平方和：

- 计算 `i * i`（即 `i` 的平方），将其十进制表示拆分成若干个非空子字符串（substring），
- 将每个子字符串解释为十进制整数，所有整数之和等于 `i`。

换言之，只要存在一种方式把 `i*i` 的数字序列划分，使得划分后各段数字之和恰好等于 `i`，则 `i` 的平方会计入惩罚数的求和。

---

### 示例

**示例 1**

```
Input: n = 10
Output: 182
Explanation:
在区间 [1, 10] 中恰好有 3 个整数 i 满足题目条件：
- 1，因为 1 * 1 = 1，直接划分为 “1”，其和为 1。
- 9，因为 9 * 9 = 81，81 可以划分为 “8”和“1”，8 + 1 = 9。
- 10，因为 10 * 10 = 100，100 可以划分为 “10”和“0”，10 + 0 = 10。
因此，10 的惩罚数为 1² + 9² + 10² = 1 + 81 + 100 = 182。
```

**示例 2**

```
Input: n = 37
Output: 1478
Explanation:
在区间 [1, 37] 中恰好有 4 个整数 i 满足题目条件：
- 1，因为 1 * 1 = 1。
- 9，因为 9 * 9 = 81，81 可以划分为 “8”和“1”，8 + 1 = 9。
- 10，因为 10 * 10 = 100，100 可以划分为 “10”和“0”，10 + 0 = 10。
- 36，因为 36 * 36 = 1296，1296 可以划分为 “1”、“29”和“6”，1 + 29 + 6 = 36。
因此，37 的惩罚数为 1² + 9² + 10² + 36² = 1 + 81 + 100 + 1296 = 1478。
```

---

### 约束条件

- `1 <= n <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求找出所有 `i (1 ≤ i ≤ n)`，使得 **i 的平方** 的十进制表示可以在某些位置插入 “+” 号，使得各段数字之和恰好等于 `i` 本身。  
这类 “在数字之间插入分隔符” 的操作，最直接的实现方法是：

1. 把 `i²` 转成字符串，例如 `1296 → "1296"`。  
2. 枚举所有可能的插入方式。  
   - 对长度为 `len` 的字符串，插入位置有 `len-1` 个，每个位置可以 **插入** 或 **不插入** “+”。  
   - 用一个二进制掩码 `mask`（0~`2^{len-1}-1`）来表示插入方案，`mask` 第 `k` 位为 1 表示在第 `k` 位和第 `k+1` 位之间插入 “+”。  
3. 根据 `mask` 把字符串切成若干子串，转成整数并求和。  
4. 若得到的和等于 `i`，说明 `i` 满足条件，累计 `i²` 到答案中。

> **类比**：把 `mask` 想象成一本字典的索引页码，页码上写的是“在这里切”。只要把所有可能的页码都翻一遍，就能找到所有合法的切法。

因为 `n ≤ 1000`，`i²` 的最大长度是 7 位（`1000² = 1 000 000`），所以最多只有 `2^{6}=64` 种切法，枚举成本极低，直接遍历 `i = 1…n` 完全可以接受。

#### 代码（Python）

```python
def punishmentNumber_bruteforce(n: int) -> int:
    """
    暴力枚举每个 i，尝试所有可能的插入 '+' 方式。
    """
    ans = 0

    for i in range(1, n + 1):
        sq_str = str(i * i)                # 把 i² 转成字符串，例如 "1296"
        L = len(sq_str)

        # 共有 2^{L-1} 种切法，用 mask 表示哪儿插入 '+'
        found = False                     # 标记 i 是否满足条件
        for mask in range(1 << (L - 1)):
            total = 0                      # 当前切法得到的各段数字之和
            last = 0                       # 当前段的起始下标

            for pos in range(L - 1):       # 检查每一个可能的切点
                if mask >> pos & 1:        # 第 pos 位为 1 → 在 pos 与 pos+1 之间切
                    total += int(sq_str[last:pos + 1])
                    last = pos + 1

            total += int(sq_str[last:])    # 加上最后一段

            if total == i:                 # 找到一种合法切法
                found = True
                break                      # 已经满足条件，后面不必继续枚举

        if found:
            ans += i * i                    # 累计 i² 到答案

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * 2^{d})`，其中 `d` 为 `i²` 的位数（最大 7），所以最坏约为 `O(1000 * 64) ≈ 6.4×10⁴`。  
  大白话：我们对每个 `i`（最多 1000 次）尝试所有可能的切法（最多 64 种），所以整体跑得很快。

- **空间复杂度**：`O(1)`（不计输出），只用了常数个临时变量。  

---

### 2. 最优解

#### 思路  

暴力解已经足够快，但我们可以把 **“枚举所有切法”** 的过程写得更直观，也更容易加入剪枝，避免无意义的计算。核心想法是 **回溯（DFS）**：

1. 从左到右扫描 `sq_str`，在每一步决定**是否在当前位置结束当前子段**。  
2. 累计已经得到的子段之和 `cur_sum`。  
3. **剪枝**：如果 `cur_sum` 已经大于目标 `i`，后面的子段只会让和更大，直接返回。  
4. 当走到字符串末尾时，检查 `cur_sum` 是否等于 `i`。若相等，则说明找到了合法切法。

因为 `i` 最多只有 7 位，递归深度 ≤ 7，剪枝能把搜索空间进一步压缩到实际可行的数量级。

> **类比**：把数字字符串看成一条道路，递归相当于 **在每个路口决定是继续前进还是在这里建一个“检查站”**（即切断），只有累计的检查站费用不超过预算（`i`）时才继续前进。

#### 代码（Python）

```python
def can_partition(num: int, target: int) -> bool:
    """
    判断整数 num 的十进制字符串是否可以切分成若干段，使得各段之和恰好等于 target。
    使用深度优先搜索 + 剪枝。
    """
    s = str(num)
    n = len(s)

    def dfs(idx: int, cur_sum: int) -> bool:
        # idx: 当前处理到的字符下标（0‑based）
        # cur_sum: 已经切好的子段之和
        if cur_sum > target:          # 剪枝：已经超出目标
            return False
        if idx == n:                  # 已经走完所有字符
            return cur_sum == target

        # 逐渐扩展当前子段的右边界，形成一个新的整数
        val = 0
        for j in range(idx, n):
            val = val * 10 + int(s[j])   # 把 s[idx:j+1] 转成整数
            # 递归尝试在 j 位置切断（即把子段 s[idx:j+1] 加入 sum）
            if dfs(j + 1, cur_sum + val):
                return True
        return False

    return dfs(0, 0)


def punishmentNumber_optimal(n: int) -> int:
    """
    对每个 i 使用上面的回溯检查是否满足条件，累计 i²。
    """
    ans = 0
    for i in range(1, n + 1):
        if can_partition(i * i, i):
            ans += i * i
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * 2^{d})`（与暴力解同阶），但实际执行次数会因为 `cur_sum > target` 的剪枝而显著减少。  
  对于本题的约束（`d ≤ 7`），仍然是几万次运算，远低于 1 秒的 Python 运行时限。

- **空间复杂度**：`O(d)`，递归栈的最大深度等于数字的位数（最多 7），几乎可以忽略不计。

---

## 心得

- **核心技巧**：在数字的字符串形式上进行**回溯切分**，并利用**当前和的上界**进行剪枝。  
- **适用题型**：  
  1. *Partition String Into Subnumbers*（把字符串切成若干整数满足某条件）。  
  2. *Expression Add Operators*（在数字间插入运算符，使表达式值等于目标）。  
  3. *Number of Ways to Reach a Target Sum by Splitting Digits*（类似的数字切分求和）。  
- **一句话总结**：**“在十进制字符串上递归尝试切点，并在累计和超过目标时立即止步”** 就是本题的解题钥匙。

## 反思

- **第一反应**：看到“把 i² 的数字分块求和”等于 i，立刻想到枚举所有切法（二进制掩码）——这正是最直接的暴力思路。  
- **最容易踩的坑**：  
  - 忘记把 `i²` 转成 **字符串** 再切分，直接对整数进行位运算会很麻烦。  
  - 忽视 **前导零** 的合法性：如 `100 → "100"` 切成 `"10"` 与 `"0"` 是允许的，因为子段可以是 `0`。  
  - 边界条件：`i = 1` 时只有一个字符，递归/掩码实现必须兼容 `len-1 = 0` 的情况。  
- **下次遇到同类题**：第一步先 **把数字转成字符串**，思考 **在每个相邻位置是否插入分隔符**，然后决定是 **枚举掩码** 还是 **递归回溯并剪枝**。这样可以快速定位可行的解法框架。