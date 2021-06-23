# #1375. 二进制字符串前缀对齐次数 / Number of Times Binary String Is Prefix-Aligned

> 难度：中等 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/number-of-times-binary-string-is-prefix-aligned/)

---

## 题目（英文原版）

**Description**

You have a 1-indexed binary string of length n where all the bits are 0 initially. We will flip all the bits of this binary string (i.e., change them from 0 to 1) one by one. You are given a 1-indexed integer array flips where flips[i] indicates that the bit at index flips[i] will be flipped in the ith step.
A binary string is prefix-aligned if, after the ith step, all the bits in the inclusive range [1, i] are ones and all the other bits are zeros.
Return the number of times the binary string is prefix-aligned during the flipping process.

**Examples**

**Example 1:**

```
Input: flips = [3,2,4,1,5]
Output: 2
Explanation: The binary string is initially "00000".
After applying step 1: The string becomes "00100", which is not prefix-aligned.
After applying step 2: The string becomes "01100", which is not prefix-aligned.
After applying step 3: The string becomes "01110", which is not prefix-aligned.
After applying step 4: The string becomes "11110", which is prefix-aligned.
After applying step 5: The string becomes "11111", which is prefix-aligned.
We can see that the string was prefix-aligned 2 times, so we return 2.
```

**Example 2:**

```
Input: flips = [4,1,2,3]
Output: 1
Explanation: The binary string is initially "0000".
After applying step 1: The string becomes "0001", which is not prefix-aligned.
After applying step 2: The string becomes "1001", which is not prefix-aligned.
After applying step 3: The string becomes "1101", which is not prefix-aligned.
After applying step 4: The string becomes "1111", which is prefix-aligned.
We can see that the string was prefix-aligned 1 time, so we return 1.
```

**Constraints**

- n == flips.length
- 1 <= n <= 5 * 104
- flips is a permutation of the integers in the range [1, n].

---

## 题目（中文翻译）

**描述**  
你有一个下标从 1 开始、长度为 `n` 的二进制字符串，初始时所有位都是 `0`。我们会一次翻转该二进制字符串中的所有位（即把 `0` 变为 `1`），每次翻转一个位置。给定下标从 1 开始的整数数组 `flips`，其中 `flips[i]` 表示第 `i` 步要翻转的位的下标。

如果在第 `i` 步之后，区间 `[1, i]`（含两端）的所有位都是 `1`，而其余位都是 `0`，则称该二进制字符串此时是 **前缀对齐**（prefix-aligned）的。

返回在整个翻转过程中，二进制字符串出现前缀对齐的次数。

**示例 1**  
输入: `flips = [3,2,4,1,5]`  
输出: `2`  
解释:  
二进制字符串初始为 `"00000"`。  
- 第 1 步后: 字符串变为 `"00100"`，不是前缀对齐。  
- 第 2 步后: 字符串变为 `"01100"`，不是前缀对齐。  
- 第 3 步后: 字符串变为 `"01110"`，不是前缀对齐。  
- 第 4 步后: 字符串变为 `"11110"`，此时是前缀对齐。  
- 第 5 步后: 字符串变为 `"11111"`，此时也是前缀对齐。  

**示例 2**  
输入: `flips = [4,1,2,3]`  
输出: `1`  
解释:  
二进制字符串初始为 `"0000"`。  
- 第 1 步后: 字符串变为 `"0001"`，不是前缀对齐。  
- 第 2 步后: 字符串变为 `"1001"`，不是前缀对齐。  
- 第 3 步后: 字符串变为 `"1101"`，不是前缀对齐。  
- 第 4 步后: 字符串变为 `"1111"`，此时是前缀对齐。  

**约束条件**  
- `n == flips.length`  
- `1 <= n <= 5 * 10^4`  
- `flips` 是区间 `[1, n]` 内整数的一个排列。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把二进制字符串真的画出来，**一步一步**按照 `flips` 的顺序把对应位置的 `0` 换成 `1`，然后在每一步检查：

1. 前 `i` 位（即下标 `1 … i`）是否全是 `1`；
2. 其余位（`i+1 … n`）是否全是 `0`。

如果两条都满足，就说明当前的字符串是 **prefix‑aligned**，计数器加一。

**用到的数据结构**  

- 一个长度为 `n` 的列表 `bits`，用来存放当前每个位置的 `0/1`。可以把它想象成一排灯泡，`0` 表示灯是关的，`1` 表示灯是开的。
- 一个计数器 `ans`，记录出现 prefix‑aligned 的次数。

**为什么正确**  

因为我们在每一步都完整地检查了题目对“前缀对齐”的所有要求：只要前 `i` 位全亮且后面的灯全暗，说明此时的二进制串满足定义，计数器就会被正确地增加一次。

**时间/空间复杂度**  

- **时间复杂度**：对每一步都要遍历 **前 `i` 位** 和 **后 `n-i` 位**，最坏情况是 `i = n`，所以总共要做大约 `1 + 2 + … + n = n·(n+1)/2` 次比较，记作 `O(n²)`。  
  - 大白话：如果 `n = 10⁴`，大约要检查 5 × 10⁷ 次，计算机会明显感到吃力。
- **空间复杂度**：我们额外开辟了一个长度为 `n` 的数组来保存当前的位，空间占用是 `O(n)`。  

---

#### 代码（Python）

```python
def numTimesAllBlue(flips):
    n = len(flips)                     # 字符串长度
    bits = [0] * n                     # 0 表示灯是关的，初始全关
    ans = 0

    for step, pos in enumerate(flips, start=1):   # step 从 1 开始
        bits[pos - 1] = 1                         # 把对应位置的灯打开

        # 检查前 step 位是否全是 1
        prefix_ok = all(bits[i] == 1 for i in range(step))
        # 检查后面的位是否全是 0
        suffix_ok = all(bits[i] == 0 for i in range(step, n))

        if prefix_ok and suffix_ok:               # 同时满足两个条件
            ans += 1

    return ans
```

> **关键行注释**  
> - `bits[pos - 1] = 1`：把第 `pos` 位的灯打开（下标从 0 开始所以要 `-1`）。  
> - `all(bits[i] == 1 for i in range(step))`：遍历前 `step` 位，确保每个都是 `1`。  
> - `all(bits[i] == 0 for i in range(step, n))`：遍历剩余位，确保每个都是 `0`。  

#### 复杂度

- **时间复杂度**：`O(n²)` —— 每一步都要遍历 O(step) + O(n‑step) ≈ O(n) 的长度，累计下来是二次方级别。  
- **空间复杂度**：`O(n)` —— 需要保存当前的二进制串（灯的状态）。  

---

### 2. 最优解

#### 思路  

暴力解的慢点在于**每一步都完整扫描整个数组**。实际上我们只需要关心 **“已经翻到最右边的灯是哪一盏”**。

观察：

- 第 `i` 步已经翻了 `i` 盏灯（因为 `flips` 是长度为 `n` 的排列）。
- 如果这 `i` 盏灯中最右边的下标是 `mx`，那么前 `mx` 位一定已经全部被翻过（因为只有 `i` 盏灯被翻，而 `mx` 只能不大于 `i`）。
- 当且仅当 `mx == i` 时，**前 `i` 位全是 `1`，其余位全是 `0`**——这正是题目定义的 prefix‑aligned 时刻。

于是我们只需要维护一个变量 `mx`，记录到目前为止出现过的最大翻转位置：

1. 初始化 `mx = 0，ans = 0`。  
2. 依次遍历 `flips`（下标从 `1` 开始），把当前翻转位置 `pos` 与 `mx` 比较，取最大值 `mx = max(mx, pos)`。  
3. 如果此时 `mx == step`（步数），说明已经恰好翻完前 `step` 位，计数器 `ans` 加一。

**核心数据结构**  

- 一个整数 `mx`，相当于“最右侧已经亮起的灯的编号”。可以把它类比成 **字典里最大的键**，我们只关心最大值，不需要存整个字典。

**为什么正确**  

- 已翻的灯数恰好是 `step`。若最大的下标 `mx` 小于 `step`，说明还有某些位置（比如 `mx+1`）没有被翻，前缀不完整。  
- 若 `mx` 大于 `step`，说明已经有灯在第 `step+1` 位或更右的位置亮起，这违背了“其余位必须全是 0”。  
- 因此只有 `mx == step` 才能同时满足“前缀全亮”和“其余全暗”。  

**时间/空间复杂度**  

- **时间复杂度**：只遍历一次 `flips`，每一步做 `max` 与一次比较，都是 `O(1)` 操作，总计 `O(n)`。  
  - 大白话：`n` 为 5 × 10⁴ 时，只需要大约 5 万次简单运算，几乎瞬间完成。  
- **空间复杂度**：只用了常数个变量 `mx、ans、step`，即 `O(1)`。  

---

#### 代码（Python）

```python
def numTimesAllBlue(flips):
    """
    返回翻转过程中二进制字符串成为 prefix‑aligned 的次数。
    思路：维护已经出现的最大翻转下标 mx，只要 mx == 当前步数 step，就满足条件。
    """
    mx = 0          # 目前看到的最大翻转位置
    ans = 0

    for step, pos in enumerate(flips, start=1):   # step 从 1 开始计数
        mx = max(mx, pos)                         # 更新最右侧已翻灯的位置
        if mx == step:                            # 前 step 位全部翻完，且没有更右的灯亮起
            ans += 1

    return ans
```

> **关键行注释**  
> - `mx = max(mx, pos)`：相当于把字典里最大的键更新为当前看到的更大的位置。  
> - `if mx == step:`：判断“最右已亮灯的编号恰好等于已经翻的灯的数量”，这正是 prefix‑aligned 的判定条件。  

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次 `flips`，每步常数时间。  
- **空间复杂度**：`O(1)` — 只用几个整数变量，不随 `n` 增长。  

---

## 心得

- **核心技巧**：把 “前缀全为 1、其余全为 0” 转化为 “已翻位置的最大下标等于已翻的次数”。  
- **该技巧适用的题型**  
  1. “All Bulbs Are Blue” 系列（LeetCode 319）  
  2. “Maximum Number of Coins You Can Get” 中的“前缀/后缀完整性”判断  
  3. 任何要求“前缀已全部出现”且输入是 **排列** 的问题（如 “Find the number of chunks to make sorted”）。
- **一句话总结解题钥匙**：**只关注最大下标**，不必维护完整的数组。

---

## 反思

- **第一反应**：看到 “prefix‑aligned” 立刻想到每一步都全遍历检查，写出暴力实现。  
- **最容易踩的坑**  
  - 忘记 `flips` 是 **1‑indexed**，导致下标偏移错误。  
  - 误以为只要前 `i` 位全是 `1` 就算对齐，忽略了“其余位必须全是 `0`”。  
  - 在最优解里没有考虑到 `flips` 是全排列，导致错误的计数逻辑。  
- **下次遇到同类题**：第一步先思考 **“有没有只需要 O(1) 信息就能判断当前是否满足条件？”**，如果答案是有（如最大下标、累计和等），就立刻尝试把问题抽象为维护这个信息的过程。这样往往能把二次方降到线性。