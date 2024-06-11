# #2729. 检查数字是否迷人 / Check if The Number is Fascinating

> 难度：简单 · 标签：Hash Table、Math · [LeetCode 链接](https://leetcode.com/problems/check-if-the-number-is-fascinating/)

---

## 题目（英文原版）

**Description**

You are given an integer n that consists of exactly 3 digits.
We call the number n fascinating if, after the following modification, the resulting number contains all the digits from 1 to 9 exactly once and does not contain any 0's:
Return true if n is fascinating, or false otherwise.
Concatenating two numbers means joining them together. For example, the concatenation of 121 and 371 is 121371.

**Examples**

**Example 1:**

```
Input: n = 192
Output: true
Explanation: We concatenate the numbers n = 192 and 2 * n = 384 and 3 * n = 576. The resulting number is 192384576. This number contains all the digits from 1 to 9 exactly once.
```

**Example 2:**

```
Input: n = 100
Output: false
Explanation: We concatenate the numbers n = 100 and 2 * n = 200 and 3 * n = 300. The resulting number is 100200300. This number does not satisfy any of the conditions.
```

**Constraints**

- 100 <= n <= 999

---

## 题目（中文翻译）

**描述**  
给定一个恰好由 **3 位数字**（3-digit）组成的整数 `n`。  
如果对 `n` 进行以下修改后得到的数 **恰好包含 1 到 9 的所有数字一次且不包含 0**，则称 `n` 为 **迷人（fascinating）**。  
返回 `true` 表示 `n` 是迷人数，返回 `false` 表示不是。

**操作说明**  
将 `n`、`2 * n` 与 `3 * n` **拼接（concatenating）** 在一起，形成一个新的整数。例如，`121` 与 `371` 的拼接结果是 `121371`。

**示例 1**  
```text
输入: n = 192
输出: true
解释: 我们把 n = 192、2 * n = 384、3 * n = 576 拼接得到 192384576。该数字恰好包含 1~9 的所有数字各一次。
```

**示例 2**  
```text
输入: n = 100
输出: false
解释: 我们把 n = 100、2 * n = 200、3 * n = 300 拼接得到 100200300。该数字不满足条件（包含 0，且缺少其他数字）。
```

**约束条件**  
- `100 <= n <= 999`   (n 为三位整数)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把题目要求的“拼接”一步一步写出来：

1. 先算出 `n`、`2*n`、`3*n` 三个数。  
2. 把它们按顺序连在一起形成一个新字符串，例如 `192`、`384`、`576` → `"192384576"`。  
3. 检查这个字符串是否恰好包含 **1~9** 这九个数字且每个只出现一次，且不出现 `0`。

这里用到的 **哈希表**（在 Python 里是 `set`）可以类比成 **查字典**：  
- “单词” 是数字字符 `'1'…'9'`，  
- “页码” 是我们是否已经看到过这个字符。  
只要把所有字符放进集合，集合的大小恰好是 9，且不包含 `'0'`，就说明满足条件。

这种方法一定正确，因为我们完整地模拟了题目描述的过程，并且逐个检查每个字符是否符合要求。

**时间复杂度**  
- 生成三个数的拼接字符串需要遍历 9 个字符（`3 * 3` 位），所以是 **O(9)**，在算法分析里通常写作 **O(1)**（常数时间），因为无论输入怎样，最多只有 9 位要处理。  
- 检查集合大小同样是遍历这 9 位，所以也是 **O(1)**。

**空间复杂度**  
- 用了一个集合保存最多 9 个字符，空间也是 **O(1)**（常数级别）。

#### 代码（Python）

```python
def is_fascinating_brute(n: int) -> bool:
    """
    暴力实现：直接拼接 n、2n、3n，然后检查是否恰好出现 1~9 各一次。
    """
    # 1. 计算三个数并转成字符串
    s1 = str(n)
    s2 = str(2 * n)
    s3 = str(3 * n)

    # 2. 拼接成一个新字符串
    concat = s1 + s2 + s3          # 例：192 + 384 + 576 → "192384576"

    # 3. 长度必须是 9，且不能出现 '0'
    if len(concat) != 9 or '0' in concat:
        return False

    # 4. 把字符放进集合，检查集合大小是否为 9（即 1~9 每个都出现一次）
    unique_digits = set(concat)    # 类比查字典：每个字符只保留一次
    return len(unique_digits) == 9
```

#### 复杂度

- **时间复杂度**：`O(1)`（实际含义是只处理至多 9 个字符，常数时间）。
- **空间复杂度**：`O(1)`（只开辟了几个字符串和一个最多装 9 个元素的集合）。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经是常数时间，但我们仍然可以把「检查是否出现一次」的过程写得更简洁、更高效，**不使用额外的集合**，而是用 **位掩码（bit mask）** 来记录已经出现过的数字。

**瓶颈**  
- 暴力解使用了 `set`，虽然空间是常数级，但每次插入都要进行哈希运算，稍微多余。

**优化步骤**  

1. 同样先得到 `n、2n、3n` 的拼接字符串（这一步不可省，因为我们必须把三个数连起来）。  
2. 遍历拼接字符串的每个字符 `c`：  
   - 把字符转成对应的整数 `d = int(c)`（范围 1~9）。  
   - 用一个 10 位的二进制整数 `mask` 来记录出现情况：第 `d` 位为 1 表示数字 `d` 已出现。  
   - 若第 `d` 位已经是 1，说明该数字出现了两次，直接返回 `False`。  
3. 循环结束后，检查 `mask` 是否恰好等于二进制 `0b1111111110`（即位 1~9 都是 1，位 0 为 0），如果相等则说明恰好出现一次。

**为什么位掩码能工作**  
- 想象一排 10 个灯泡（编号 0~9），每看到一个数字就把对应灯泡打开（设为 1）。  
- 如果灯泡已经是亮的，再次看到同样的数字就说明出现重复，立刻判定失败。  
- 最后只要检查灯泡 1~9 全部亮起，说明每个数字恰好出现一次。

**时间复杂度**  
- 仍然只遍历至多 9 位字符，**O(1)**。  
- 与暴力解相比，去掉了集合的哈希开销，常数因子更小。

**空间复杂度**  
- 只使用了一个整数变量 `mask`，**O(1)**。

#### 代码（Python）

```python
def is_fascinating_optimal(n: int) -> bool:
    """
    最优实现：使用位掩码记录数字出现情况，避免集合开销。
    """
    # 1. 拼接 n、2n、3n 的字符串
    concat = str(n) + str(2 * n) + str(3 * n)

    # 2. 长度必须是 9，且不能有 0
    if len(concat) != 9 or '0' in concat:
        return False

    mask = 0  # 用 10 位二进制表示数字 0~9 是否出现，初始全 0

    for ch in concat:
        digit = int(ch)          # 把字符转成整数，范围 1~9
        bit = 1 << digit         # 第 digit 位对应的掩码，例如 digit=3 → 0b1000

        # 如果该位已经是 1，说明数字重复出现
        if mask & bit:
            return False
        mask |= bit              # 把对应位设为 1，表示数字出现过

    # 目标掩码：位 1~9 都是 1，位 0 为 0 → 二进制 0b1111111110 = 0x3FE
    return mask == 0b1111111110
```

#### 复杂度

- **时间复杂度**：`O(1)`（遍历 9 位字符，位运算是常数时间）。
- **空间复杂度**：`O(1)`（只用了一个整数 `mask`）。

---

## 心得

- **核心技巧**：使用 **位掩码**（或计数数组）快速判断「每个数字出现一次且不出现 0」的条件。  
- **适用的题型**：  
  1. 判断一个数字是否是 **全排列**（如 1~9、0~9）  
  2. 判断字符串是否为 **异位词**（每个字符出现次数相同）  
  3. 判断是否为 **回文数**（可以用位掩码记录奇数次出现的字符）  
- **一句话总结**：把“出现一次”转化为“对应位只能被设为 1 一次”，用位运算即可在 O(1) 时间完成检查。

## 反思

- **第一反应**：直接把 `n、2n、3n` 拼接成字符串，然后用集合检查是否包含 1~9。  
- **最容易踩的坑**：  
  - 忘记排除出现 `0` 的情况。  
  - 只检查集合大小为 9 而不检查是否有 `0`，会把 `102345678` 错误判为 true。  
  - 边界输入（如 `100`）会产生多余的 `0`，一定要先过滤掉。  
- **下次遇到同类题**：第一步先 **把数字转成字符序列**，然后 **用位掩码或计数数组快速统计出现次数**，再根据题目要求检查是否满足“一次出现”。这样思路清晰，代码也更高效。