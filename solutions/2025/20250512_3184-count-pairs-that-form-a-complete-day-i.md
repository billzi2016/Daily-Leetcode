# #3184. 计数形成完整天数的配对 I / Count Pairs That Form a Complete Day I

> 难度：简单 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/count-pairs-that-form-a-complete-day-i/)

---

## 题目（英文原版）

**Description**

Given an integer array hours representing times in hours, return an integer denoting the number of pairs i, j where i < j and hours[i] + hours[j] forms a complete day.
A complete day is defined as a time duration that is an exact multiple of 24 hours.
For example, 1 day is 24 hours, 2 days is 48 hours, 3 days is 72 hours, and so on.

**Examples**

**Example 1:**

```
Input: hours = [12,12,30,24,24]
Output: 2
Explanation:
The pairs of indices that form a complete day are (0, 1) and (3, 4) .
```

**Example 2:**

```
Input: hours = [72,48,24,3]
Output: 3
Explanation:
The pairs of indices that form a complete day are (0, 1) , (0, 2) , and (1, 2) .
```

**Constraints**

- 1 <= hours.length <= 100
- 1 <= hours[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组（integer array）`hours`，表示以小时为单位的时间，返回一个整数，表示满足 `i < j` 且 `hours[i] + hours[j]` 能形成完整天（complete day）的配对（pair）`(i, j)` 的数量。  
完整天被定义为时间长度恰好是 24 小时的整数倍。  
例如，1 天是 24 小时，2 天是 48 小时，3 天是 72 小时，依此类推。  

**示例 1**  

**示例 2**  

**约束条件**  
- `1 <= hours.length <= 100`  
- `1 <= hours[i] <= 10^9`  

**示例**  

**示例 1:**  
```text
Input: hours = [12,12,30,24,24]
Output: 2
Explanation:
能够形成完整天的索引配对为 (0, 1) 和 (3, 4)。
```  

**示例 2:**  
```text
Input: hours = [72,48,24,3]
Output: 3
Explanation:
能够形成完整天的索引配对为 (0, 1)、(0, 2) 和 (1, 2)。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的下标对 `(i, j)`（满足 `i < j`）全部枚举一遍，逐个检查它们的和是否能被 24 整除。  
- **数据结构**：只需要原始的 `hours` 列表和两个循环变量 `i、j`，不需要额外的容器。可以把它想成“把所有人两两配对”，就像在派对上每个人都要和其他人握手一次，记录下每次握手的结果。
- **正确性**：因为我们遍历了所有合法的下标组合，只要有一对满足 `(hours[i] + hours[j]) % 24 == 0`，就一定会被计数，最终的计数必然等于答案。
- **时间/空间复杂度**：  
  - 外层循环遍历 `n` 次，内层最多遍历 `n-1`、`n-2`…次，整体是 `n·(n-1)/2`，用大 O 记就是 **O(n²)**。  
    大白话：如果 `n=100`，大约要检查 5,000 次；如果 `n=1,000`，要检查 500,000 次，随 `n` 的增长呈平方增长。  
  - 只用了常数级的额外空间（几个计数器），所以是 **O(1)**。

#### 代码（Python）

```python
from typing import List

def countCompleteDayPairs_bruteforce(hours: List[int]) -> int:
    n = len(hours)
    ans = 0                         # 用来累计满足条件的配对数
    # i 从 0 遍历到倒数第二个元素
    for i in range(n):
        # j 必须在 i 之后，防止重复计数 (i,j) 与 (j,i)
        for j in range(i + 1, n):
            total = hours[i] + hours[j]          # 两个时间相加
            # 判断是否是完整的天数：能被 24 整除
            if total % 24 == 0:
                ans += 1                         # 找到一对合法配对
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 随着数组长度的增大，检查的次数呈二次方增长。  
- **空间复杂度**：`O(1)` —— 只用了若干个整型变量，不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要把两个数相加再求模**，这一步在所有 `n²` 对上都要做，显然有很多重复劳动。  
观察模运算的性质：

> 若 `(a + b) % 24 == 0`，则 `a % 24` 与 `b % 24` 必然互为“补数”，即 `a % 24 + b % 24 == 24`（或都为 0）。

因此，只要我们知道每个数除以 24 的余数，就可以把“需要配对的对象”直接算出来，而不必遍历所有下标。实现思路如下：

1. **把每个元素转成余数**：`rem = hour % 24`。余数的取值范围只有 `0~23`，非常小。
2. **用哈希表（字典）统计每种余数出现了多少次**。这一步类似“查字典”，键是余数，值是出现次数。
3. 对每种余数 `r`，找它对应的补数 `c = (24 - r) % 24`（注意 `r=0` 时补数仍是 `0`），配对的方式有两种：
   - **r = 0**（或者 `r = 12`，因为 `12+12=24`）时，两个相同余数的数也能配对。配对数是 `cnt[r] choose 2 = cnt[r] * (cnt[r] - 1) // 2`。
   - **其他情况**时，只需要把 `cnt[r]` 与 `cnt[c]` 相乘即可得到不同余数之间的配对数。为了避免重复计数，只遍历 `r` 从 `1` 到 `11`（因为 `c` 会在 `13~23`），每对只算一次。

这样只用了 **一次线性遍历**（`O(n)`）来统计余数，再用常数次的计算得到答案，时间大幅降低。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def countCompleteDayPairs_opt(hours: List[int]) -> int:
    # 第一步：统计每个余数出现的次数
    freq = defaultdict(int)          # 哈希表：余数 -> 出现次数
    for h in hours:
        r = h % 24                    # 余数，只会是 0~23 之间的整数
        freq[r] += 1

    ans = 0

    # 处理余数为 0 的情况：0+0 正好是 24 的倍数
    cnt0 = freq.get(0, 0)
    ans += cnt0 * (cnt0 - 1) // 2      # 组合数 C(cnt0, 2)

    # 处理余数为 12 的情况：12+12 = 24
    cnt12 = freq.get(12, 0)
    ans += cnt12 * (cnt12 - 1) // 2    # 同上

    # 处理其他余数 (1~11) 与它们的补数 (23~13) 配对
    for r in range(1, 12):            # 只遍历一半，避免重复计数
        complement = 24 - r           # 与 r 配对的余数
        ans += freq.get(r, 0) * freq.get(complement, 0)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只需要一次遍历数组统计余数，后面的配对计算是常数次数（最多遍历 12 次）。与暴力的 `O(n²)` 相比，速度提升了数量级。
- **空间复杂度**：`O(1)` —— 哈希表的键最多 24 个（余数范围固定），所以空间使用不随 `n` 增长。

---

## 心得

- **核心技巧**：利用模运算的“余数配对”性质，把原本的二次枚举转化为一次计数 + 常数次配对。
- **适用题型**：
  1. “两数之和能被 k 整除”类（如 LeetCode 1252 `Count Items Matching a Rule` 的变体）。
  2. “找出满足某种余数关系的配对”类，如 “数组中两数之和为偶数”。
  3. “利用固定取模范围的计数”类，如 “数组中出现次数最多的余数”。
- **一句话总结**：**把“能配对”转化为“余数互补”，用哈希表一次统计，配对瞬间完成**。

---

## 反思

- **第一反应**：看到 “完整的一天是 24 的倍数”，立刻想到 **模 24**，于是想到暴力枚举检查 `(a+b)%24==0`。
- **最容易踩的坑**：
  1. 忘记 `i < j` 的顺序限制，导致计数两次同一对。使用组合数或只遍历一半余数可以避免。
  2. 对余数为 `0`（以及 `12`）的特殊情况处理不当，可能会漏算或重复计数。
  3. 当 `hours[i]` 很大（最高 `10^9`），直接相加仍不会溢出 Python，但在有些语言要注意整数溢出。
- **下次遇到同类题**，第一步应该先**把问题抽象为“余数配对”**，检查是否可以用计数哈希表把二次枚举压到线性时间。