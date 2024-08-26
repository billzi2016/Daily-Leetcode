# #2843. 计数对称整数 /   Count Symmetric Integers

> 难度：简单 · 标签：Math、Enumeration · [LeetCode 链接](https://leetcode.com/problems/count-symmetric-integers/)

---

## 题目（英文原版）

**Description**

You are given two positive integers low and high.
An integer x consisting of 2 * n digits is symmetric if the sum of the first n digits of x is equal to the sum of the last n digits of x. Numbers with an odd number of digits are never symmetric.
Return the number of symmetric integers in the range [low, high].

**Examples**

**Example 1:**

```
Input: low = 1, high = 100
Output: 9
Explanation: There are 9 symmetric integers between 1 and 100: 11, 22, 33, 44, 55, 66, 77, 88, and 99.
```

**Example 2:**

```
Input: low = 1200, high = 1230
Output: 4
Explanation: There are 4 symmetric integers between 1200 and 1230: 1203, 1212, 1221, and 1230.
```

**Constraints**

- 1 <= low <= high <= 104

---

## 题目（中文翻译）

给定两个正整数 `low` 和 `high`。  
如果一个整数 `x` 的位数为 `2 * n`，且 `x` 前 `n` 位数字之和等于后 `n` 位数字之和，则称该整数为对称的（symmetric）。位数为奇数的整数永远不是对称的。  
返回区间 `[low, high]` 内对称整数的数量。

**示例 1**  
**输入**: `low = 1, high = 100`  
**输出**: `9`  
**解释**: 在 `[1, 100]` 区间内共有 9 个对称整数：`11, 22, 33, 44, 55, 66, 77, 88, 99`。

**示例 2**  
**输入**: `low = 1200, high = 1230`  
**输出**: `4`  
**解释**: 在 `[1200, 1230]` 区间内共有 4 个对称整数：`1203, 1212, 1221, 1230`。

**约束条件**  
- `1 <= low <= high <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把区间 `[low, high]` 里的每一个整数都检查一遍，判断它是不是“对称整数”。  
检查的步骤：

1. 把整数转成字符串（把数字想象成一串字符），例如 `1230 → "1230"`。  
2. 看它的长度是不是偶数。如果是奇数位数，直接不是对称整数。  
3. 把字符串平均分成左半边和右半边，分别把每一位字符转换回整数求和。  
4. 左半边的和与右半边的和相等，则计数+1。

> **类比**：  
> 哈希表就像一本字典，`key` 是单词，`value` 是页码。这里我们把数字当作一本“小字典”，左半边和右半边的“页码和”要相等，才算合格。

这种做法一定能得到正确答案，因为我们没有遗漏任何可能的数，也没有做任何错误的判断。

#### 代码（Python）

```python
def countSymmetricIntegers_bruteforce(low: int, high: int) -> int:
    ans = 0
    for x in range(low, high + 1):               # 逐个遍历区间里的整数
        s = str(x)                               # 把整数转成字符串，方便逐位操作
        if len(s) % 2 == 1:                      # 位数为奇数直接跳过
            continue
        half = len(s) // 2                       # 每边的长度
        left_sum = sum(int(ch) for ch in s[:half])   # 左半边各位相加
        right_sum = sum(int(ch) for ch in s[half:])  # 右半边各位相加
        if left_sum == right_sum:                # 和相等则计数
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(N * d)`，其中 `N = high - low + 1` 是区间长度，`d` 是数字的位数（最多 5 位）。  
  用大白话说，就是“我们最多检查 `N` 次，每次要看几位数（最多 5），所以整体时间大约是 `N` 的几倍”。  
  对于本题的最大限制 `high ≤ 10⁴`，`N` 最多是 10 000，运行毫秒级别。

- **空间复杂度**：`O(1)`，只用了常数个额外变量（计数器、临时字符串等），不随 `N` 增长。

---

### 2. 最优解

#### 思路  

虽然暴力已经够快，但我们可以 **把“遍历所有数字”** 这一步做得更精简，直接只枚举 **偶数位数的数字**，因为奇数位数根本不可能是对称的。

1. **确定可能的位数**  
   - 题目限制 `high ≤ 10⁴`，所以最多只有 4 位（`9999`），而 5 位数一定是奇数位，直接排除。  
   - 因此只需要考虑长度为 2 或 4 的数字。

2. **拆分为“前半段 + 后半段”**  
   - 设 `2·n` 为总位数（`n = 1` 或 `2`）。  
   - 前半段必须是一个 **n 位的正整数**，即最高位不能为 0（否则整体位数会不足 2·n）。  
   - 后半段可以是 `0` 开头的 n 位数（比如 `1203` 的后半段是 `03`），所以我们可以让它遍历 `0 … 10ⁿ‑1`。

3. **比较两段的数字和**  
   - 对每一个合法的前半段 `left`，计算它的各位和 `sum_left`。  
   - 再遍历所有可能的后半段 `right`，计算 `sum_right`。如果两者相等，则拼成的整数 `left * 10ⁿ + right` 就是对称整数。  
   - 最后检查这个整数是否落在 `[low, high]` 区间内，若在则计数。

因为 `n` 只有 1 或 2，`10ⁿ` 最多是 100，**整体枚举次数只有 10ⁿ·10ⁿ = 10⁴**（和暴力一样的上限），但我们省掉了所有奇数位数的检查，而且代码结构更清晰，也更容易推广到更大的 `high`（比如 `10⁸` 时仍然只需要枚举 `10⁴` 次）。

> **核心概念——前缀/后缀枚举**  
> 想象把一根绳子从中间剪开，左边必须是“正规长度”，右边可以有“前导零”。我们只枚举两边各自的可能，然后把它们粘合起来检查。

#### 代码（Python）

```python
def countSymmetricIntegers_opt(low: int, high: int) -> int:
    def digit_sum(num: int) -> int:
        """返回整数各位数字之和，例如 123 → 6"""
        s = 0
        while num:
            s += num % 10      # 取最低位
            num //= 10
        return s

    ans = 0
    # 只需要考虑 2 位和 4 位的情况
    for n in (1, 2):                       # n 为每半段的位数
        start_left = 10 ** (n - 1)         # 前半段首位不能为 0
        end_left = 10 ** n                 # 左半段的上界（不含）
        for left in range(start_left, end_left):
            sum_left = digit_sum(left)     # 左半段的位数和
            for right in range(0, 10 ** n):
                if digit_sum(right) != sum_left:
                    continue               # 和不相等直接跳过
                # 把左右两段拼成完整整数
                num = left * (10 ** n) + right
                if low <= num <= high:     # 检查是否在区间内
                    ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(10^{2n})`，其中 `n` 为半段位数。  
  在本题 `n ≤ 2`，所以最多是 `10⁴` 次比较。用大白话说，就是“只检查了 10 000 个可能的组合”，相比暴力遍历全部 10 000 个数字少了奇数位数的无用检查。  
- **空间复杂度**：`O(1)`，只用了几个整数变量，和输入规模无关。

---

## 心得

- **核心技巧**：把“偶数位数的对称性”转化为“左半段和右半段的位数和相等”，并通过 **枚举左右半段** 来直接构造满足条件的数字。  
- **适用场景**：  
  1. “把数字拆成两段，要求某种关系相等”——如 **Lucky Number**（左半段和右半段相等的数）。  
  2. “需要统计满足特定位数属性的整数”——如 **回文数**（左半段等于右半段的逆序）。  
- **一句话总结**：**只枚举偶数位数，比较左右两段的位数和即可快速计数**。

---

## 反思

- **第一反应**：看到“对称整数”，立刻想到把数字变成字符串逐位比较，直接遍历区间。  
- **最容易踩的坑**：  
  - 忘记 **排除奇数位数**，导致不必要的判断。  
  - 对后半段的“前导零”处理不当，例如把 `03` 当成 `3`，导致位数不对。  
  - 边界条件 `low`、`high` 可能是 1 位数，需要在计数前先检查位数是否为偶数。  
- **下次类似题的第一步**：先 **确定数字的位数约束**（偶数/奇数），再决定是直接遍历还是拆分枚举，以避免无效的搜索。