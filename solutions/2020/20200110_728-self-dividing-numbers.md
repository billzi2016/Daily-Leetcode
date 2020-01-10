# #728. 自除数 / Self Dividing Numbers

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/self-dividing-numbers/)

---

## 题目（英文原版）

**Description**

A self-dividing number is a number that is divisible by every digit it contains.
A self-dividing number is not allowed to contain the digit zero.
Given two integers left and right, return a list of all the self-dividing numbers in the range [left, right] (both inclusive).

**Examples**

**Example 1:**

```
Input: left = 1, right = 22
Output: [1,2,3,4,5,6,7,8,9,11,12,15,22]
```

**Example 2:**

```
Input: left = 47, right = 85
Output: [48,55,66,77]
```

**Constraints**

- 1 <= left <= right <= 104

---

## 题目（中文翻译）

自除数（self‑dividing number）是指一个数字能够被它包含的每一位数字整除。自除数不允许包含数字 **0**。  
给定两个整数 `left` 和 `right`，返回区间 **[left, right]**（两端均包含）内所有自除数的列表。

## 示例

### 示例 1
**输入:** `left = 1, right = 22`  
**输出:** `[1,2,3,4,5,6,7,8,9,11,12,15,22]`

### 示例 2
**输入:** `left = 47, right = 85`  
**输出:** `[48,55,66,77]`

## 约束条件
- `1 <= left <= right <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把区间 `[left, right]` 里的每一个整数都检查一遍**，看它是不是“自除数”。  
检查一个数是否自除，只需要把它的每一位数字拿出来：

* 如果出现 `0`，立刻失败（因为除数不能为零）。  
* 否则，判断原数能否被这个数字整除，若有任意一位不整除，同样失败。  

这就像 **查字典**——我们把数字当成“词”，把能否整除当成“是否在词典里”。只要所有词都有对应的解释（都能整除），这本书（这个数）就是自除的。

**为什么正确**  
- 自除数的定义正好是“每一位数字都能整除原数且不为 0”。我们逐位验证，若全部通过则必满足定义。  
- 我们遍历了区间内的所有整数，必然不会漏掉任何可能的答案。

#### 代码（Python）  

```python
def selfDividingNumbers_brute(left: int, right: int) -> list[int]:
    """
    暴力遍历每个数，逐位检查是否满足自除数条件
    """
    res = []                                   # 用来收集答案
    for num in range(left, right + 1):        # 包含右端点
        if is_self_dividing(num):              # 检查当前数字
            res.append(num)                    # 符合就加入结果
    return res


def is_self_dividing(num: int) -> bool:
    """
    判断单个整数是否为自除数
    思路：把整数转换为字符串，逐字符检查
    """
    s = str(num)                               # 把整数变成字符序列，方便逐位
    for ch in s:
        digit = int(ch)                        # 当前位的数字
        if digit == 0:                         # 出现 0 直接失败
            return False
        if num % digit != 0:                   # 不能整除也失败
            return False
    return True                                # 所有位都通过
```

#### 复杂度  

- **时间复杂度：** `O(N·D)`  
  - `N = right - left + 1` 是检查的数字个数。  
  - `D` 是每个数字的位数（最多 5 位，因为 `right ≤ 10⁴`），相当于常数。  
  - 用大白话说，就是“遍历区间一次，每个数再看几位”，所以运行时间随区间长度线性增长。  
- **空间复杂度：** `O(1)`（不计返回列表的空间）  
  - 只用了几个临时变量，和输入规模无关。

---

### 2. 最优解  

#### 思路  

暴力解已经是最直观的实现，但在实现细节上还有提升空间：

1. **避免字符串转换**  
   - 通过取余 `% 10` 和整除 `// 10` 直接得到每一位数字，省去创建临时字符串的开销。  
2. **提前退出**  
   - 检查每一位时，只要出现不满足条件的情况，就立刻 `break`，不必继续遍历剩余位数。  

这两个小技巧把常数因子降低了，整体时间复杂度仍是 `O(N·D)`，但在 `N` 很大时会明显快一些。因为题目本身的约束已经很小（`right ≤ 10⁴`），不需要更高级的 “跳过” 技巧（比如位 DP），但了解这些微优化思路对以后处理更大规模的数据非常有帮助。

#### 代码（Python）  

```python
def selfDividingNumbers_opt(left: int, right: int) -> list[int]:
    """
    通过数学运算（%、//）逐位检查，自除数判断更高效
    """
    ans = []
    for num in range(left, right + 1):
        if is_self_dividing_opt(num):
            ans.append(num)
    return ans


def is_self_dividing_opt(num: int) -> bool:
    """
    只用整数运算判断是否为自除数
    """
    original = num                     # 记录原始值，后面要用来取余
    while num > 0:                     # 当还有未检查的位时循环
        digit = num % 10               # 取最低位
        if digit == 0 or original % digit != 0:
            return False               # 0 或者不能整除，直接否定
        num //= 10                     # 去掉已经检查的最低位
    return True                        # 所有位都通过
```

#### 复杂度  

- **时间复杂度：** `O(N·D)`（与暴力解相同，只是常数更小）  
  - 这里的 `D` 仍是位数，上限为 5。因为我们不再生成字符串，实际运行时间更快。  
- **空间复杂度：** `O(1)`（同样只用了常数级别的临时变量）  

---

## 心得  

- **核心技巧**：逐位检查数字的**整除性**，使用 `%`（取余）和 `//`（整除）完成“拆解数字”。  
- **适用场景**：  
  1. 判断数字是否满足某种**位数约束**（如 “回文数”、 “数字翻转后相等” 等）。  
  2. 需要在**每位上做运算**的题目（比如 “数字翻转后加 1 是否为素数”）。  
- **一句话总结**：**把整数拆成一位一位的“小块”，逐块检验即可**。

---

## 反思  

- **第一反应**：直接遍历区间，用字符串把每个数的每位取出来检查。  
- **最容易踩的坑**：  
  - 忘记排除数字 `0`（出现零会导致除以零错误）。  
  - 把 `num` 本身在检查时直接改掉，导致后面再需要原始值时失去信息（因此要保存一份 `original`）。  
- **下次类似题目**：第一步想到 **“逐位抽取数字 → 对每位做条件判断”**，然后决定是用字符串实现还是纯整数运算实现。