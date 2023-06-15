# #2283. 检查数字的位数计数是否等于位值 / Check if Number Has Equal Digit Count and Digit Value

> 难度：简单 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/check-if-number-has-equal-digit-count-and-digit-value/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string num of length n consisting of digits.
Return true if for every index i in the range 0 <= i < n, the digit i occurs num[i] times in num, otherwise return false.

**Examples**

**Example 1:**

```
Input: num = "1210"
Output: true
Explanation:
num[0] = '1'. The digit 0 occurs once in num.
num[1] = '2'. The digit 1 occurs twice in num.
num[2] = '1'. The digit 2 occurs once in num.
num[3] = '0'. The digit 3 occurs zero times in num.
The condition holds true for every index in "1210", so return true.
```

**Example 2:**

```
Input: num = "030"
Output: false
Explanation:
num[0] = '0'. The digit 0 should occur zero times, but actually occurs twice in num.
num[1] = '3'. The digit 1 should occur three times, but actually occurs zero times in num.
num[2] = '0'. The digit 2 occurs zero times in num.
The indices 0 and 1 both violate the condition, so return false.
```

**Constraints**

- n == num.length
- 1 <= n <= 10
- num consists of digits.

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的字符串 `num`，长度为 `n`，仅包含数字字符。  
如果对所有满足 `0 <= i < n` 的下标 `i`，数字 `i` 在 `num` 中出现的次数恰好等于 `num[i]`（即字符 `num[i]` 表示的数值），则返回 `true`；否则返回 `false`。

**示例 1**  
```text
Input: num = "1210"
Output: true
Explanation:
num[0] = '1'. 数字 0 在 num 中出现了 1 次。
num[1] = '2'. 数字 1 在 num 中出现了 2 次。
num[2] = '1'. 数字 2 在 num 中出现了 1 次。
num[3] = '0'. 数字 3 在 num 中出现了 0 次。
上述条件在 "1210" 的每个下标均成立，返回 true。
```

**示例 2**  
```text
Input: num = "030"
Output: false
Explanation:
num[0] = '0'. 数字 0 应出现 0 次，但实际上出现了 2 次。
num[1] = '3'. 数字 1 应出现 3 次，但实际上出现了 0 次。
num[2] = '0'. 数字 2 在 num 中出现了 0 次。
下标 0 和 1 都不满足条件，返回 false。
```

**约束条件**  
- `n == num.length`  
- `1 <= n <= 10`  
- `num` 仅由数字字符组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个下标 i 当作“查询词”，去整条字符串里数一数数字 i 出现了几次**。  
这就像在一本书里查某个单词的出现次数：我们把书的每一页（这里是每个字符）都翻一遍，遇到目标单词（这里是字符 `'i'`）就记个数。  
实现时：

1. 把字符 `'0'…'9'` 当作“字典的 key”，对应的出现次数是“value”。这里我们不需要额外的哈希表，只要在每次查询时遍历字符串即可。  
2. 对每个下标 `i`（0 ≤ i < n）：
   - 把字符 `i`（即 `str(i)`）在整个字符串中出现的次数记为 `cnt`。
   - 把 `cnt` 与 `num[i]`（字符形式的数字）比较，若不相等直接返回 `False`。  
3. 全部下标检查完毕后返回 `True`。

**为什么正确**：题目要求“第 i 位的数字等于数字 i 在整个字符串中出现的次数”。我们正是逐一验证了这条等式，所以只要全部成立，答案必然为真。

**时间/空间复杂度**  
- 对每个下标我们都要遍历整个字符串一次，最坏情况要做 `n` 次遍历，时间复杂度是 **O(n²)**。  
  - `n²` 可以想象成“把 n 张纸每张都再翻 n 次”。  
- 只使用了常数级别的额外变量（计数器、循环索引），空间复杂度是 **O(1)**。

#### 代码（Python）

```python
def digitCount_bruteforce(num: str) -> bool:
    n = len(num)                       # 字符串长度
    for i in range(n):                 # 逐个下标检查
        target = str(i)                # 要统计的字符，比如 i=2 时 target='2'
        cnt = 0                        # 计数器，统计 target 出现了多少次
        for ch in num:                 # 遍历整条字符串
            if ch == target:           # 碰到目标字符就加一
                cnt += 1
        # num[i] 本身是字符，直接比较字符即可
        if cnt != int(num[i]):         # 若出现次数不等于对应位置的数字，返回 False
            return False
    return True                        # 所有下标都满足条件
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 对每个下标都要遍历一次长度为 `n` 的字符串，类似“十个人每人都要检查十件事”。
- **空间复杂度**：`O(1)` — 只用了几个计数变量，不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要完整遍历字符串**，导致 `n` 次 `n` 长度的遍历。  
我们可以把**“统计所有数字出现次数”**这件事一次性完成，然后再逐个下标对比，时间就能降到线性 `O(n)`。

这一步的核心工具是**计数数组（相当于哈希表）**。  
把数字 `'0'…'9'` 想成字典的“词”，词对应的页码就是它在字符串里出现的次数。我们只需要一次遍历，把每个字符对应的计数加一，得到完整的“出现次数表”。  
随后：

1. 仍然遍历下标 `i`（0 ≤ i < n）。  
2. 读取 `i` 对应的计数 `freq[i]`（即数字 `i` 出现的次数）。  
3. 把它与 `num[i]`（转成整数）比较。若不相等直接返回 `False`。  

这样只需要 **两次遍历**（一次计数，一次校验），总时间 `O(n)`，空间只需要一个长度为 10 的数组，`O(1)`。

**为什么正确**：计数数组记录了每个数字在整个字符串中的出现次数，正好是题目要求比较的左边。我们再逐个下标把左边的计数与右边的字符值（转换为整数）比对，等式全部成立即为真。

#### 代码（Python）

```python
def digitCount_optimal(num: str) -> bool:
    n = len(num)

    # 1️⃣ 统计每个数字出现的次数，freq[0] 记录字符 '0' 出现了几次，依此类推
    freq = [0] * 10                     # 长度固定为 10 的计数数组
    for ch in num:                      # 只遍历一次字符串
        digit = int(ch)                 # 把字符转成对应的整数 0~9
        freq[digit] += 1                # 对应位置计数加一

    # 2️⃣ 检查每个下标的条件
    for i in range(n):
        expected = int(num[i])           # 题目要求的“第 i 位的数字”
        if freq[i] != expected:          # freq[i] 是数字 i 出现的次数
            return False                 # 任意一项不等即返回 False
    return True                          # 全部匹配则返回 True
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只进行两次线性遍历，类似“只需要把每个人的任务检查一遍”。相比暴力的 `O(n²)`，效率提升显著。
- **空间复杂度**：`O(1)` — 计数数组大小固定为 10（常数），不随输入长度增长。

---

## 心得

- **核心技巧**：一次遍历统计频率（计数数组 / 哈希表），再利用统计结果进行快速验证。  
- **适用题型**：  
  1. “字符出现次数是否满足某种约束”类（如 LeetCode 2283 `Check if Number Has Equal Digit Count and Digit Value`）。  
  2. “数组/字符串中出现次数与下标/值对应”类（如 2042 `Check If All A's Appears Before All B's` 的计数版）。  
  3. “是否为有效的字母异位词”之类需要统计字符频率的题目。  
- **一句话总结**：**先把“出现多少次”这件事一次性算好，再逐个对比，省时又省力。**

---

## 反思

- **第一反应**：看到“每个下标 i 对应的数字出现次数”就想到直接遍历计数——也就是暴力实现。  
- **最容易踩的坑**：  
  - **下标越界**：计数数组只能存放 0~9，若字符串长度 > 10（本题不可能）需先判断。  
  - **字符与整数的转换**：`num[i]` 是字符，需要 `int(num[i])` 才能比较。  
  - **特殊情况**：当 `i` 超过字符串中出现的最大数字时，计数数组对应位置仍为 0，需正常比较。  
- **下次类似题的第一步**：**先思考能否一次遍历把所有“出现次数”收集起来**（计数数组/哈希表），再利用这些信息完成验证。这样往往能把时间从平方级降到线性级。