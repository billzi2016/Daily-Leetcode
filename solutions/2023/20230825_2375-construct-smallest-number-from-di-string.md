# #2375. 根据 DI 字符串构造最小数字 / Construct Smallest Number From DI String

> 难度：中等 · 标签：String、Backtracking、Stack、Greedy · [LeetCode 链接](https://leetcode.com/problems/construct-smallest-number-from-di-string/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string pattern of length n consisting of the characters 'I' meaning increasing and 'D' meaning decreasing.
A 0-indexed string num of length n + 1 is created using the following conditions:
Return the lexicographically smallest possible string num that meets the conditions.

**Examples**

**Example 1:**

```
Input: pattern = "IIIDIDDD"
Output: "123549876"
Explanation:
At indices 0, 1, 2, and 4 we must have that num[i] < num[i+1].
At indices 3, 5, 6, and 7 we must have that num[i] > num[i+1].
Some possible values of num are "245639871", "135749862", and "123849765".
It can be proven that "123549876" is the smallest possible num that meets the conditions.
Note that "123414321" is not possible because the digit '1' is used more than once.
```

**Example 2:**

```
Input: pattern = "DDD"
Output: "4321"
Explanation:
Some possible values of num are "9876", "7321", and "8742".
It can be proven that "4321" is the smallest possible num that meets the conditions.
```

**Constraints**

- 1 <= pattern.length <= 8
- pattern consists of only the letters 'I' and 'D'.

---

## 题目（中文翻译）

给定一个下标从 0 开始、长度为 `n` 的字符串 **pattern**，其中仅包含字符 `'I'`（表示递增，Increasing）和 `'D'`（表示递减，Decreasing）。  
需要构造一个下标从 0 开始、长度为 `n + 1` 的字符串 **num**，使其满足以下条件：

* 若 `pattern[i] == 'I'`，则必须有 `num[i] < num[i+1]`。  
* 若 `pattern[i] == 'D'`，则必须有 `num[i] > num[i+1]`。  

返回满足上述条件的 **字典序最小**（lexicographically smallest）的字符串 **num**。

---

### 示例  

#### 示例 1  
**输入**  
```
pattern = "IIIDIDDD"
```
**输出**  
```
"123549876"
```
**解释**  
- 在下标 `0, 1, 2, 4` 处，需要满足 `num[i] < num[i+1]`。  
- 在下标 `3, 5, 6, 7` 处，需要满足 `num[i] > num[i+1]`。  

一些可能的 `num` 为 `"245639871"`、`"135749862"`、`"123849765"`。  
可以证明 `"123549876"` 是满足条件的最小字典序 `num`。  
注意 `"123414321"` 不可能，因为 …（题目描述被截断）。

#### 示例 2  
**输入**  
```
pattern = "DDD"
```
**输出**  
```
"4321"
```
**解释**  
一些可能的 `num` 为 `"9876"`、`"7321"`、`"8742"`。  
可以证明 `"4321"` 是满足条件的最小字典序 `num`。

---

### 约束条件
- `1 <= pattern.length <= 8`
- `pattern` 仅由字母 `'I'` 和 `'D'` 组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有可能的数字序列枚举出来，然后挑出满足条件且字典序最小的那一个**。  

- **数据结构**：我们需要一个“排列”，可以把它想象成把 1~9（因为 pattern 长度 ≤ 8，所需数字最多 9）这些数字按照某种顺序排成一列。  
- **哈希表**在这里并不需要，用到的唯一工具是**全排列生成器**（Python 的 `itertools.permutations`），它相当于“查字典”，把每一种排列当作一个词，依次拿出来检查。  

**为什么正确**：  
如果我们把所有合法的排列都遍历一遍，必然会找到字典序最小的合法解。因为题目只要求返回最小的字符串，而我们没有遗漏任何可能性，所以答案一定在遍历过程中出现。

**时间/空间复杂度**（大白话）：

- **时间**：全排列的数量是 `9! = 362880`（因为最多用到 9 个数字），每一种排列我们都要检查 `n`（pattern 长度）次不等式。于是时间复杂度是 **O(9!·n)**，大约几百万次操作，在题目给的极小数据范围（n ≤ 8）下完全可以跑完。  
- **空间**：我们只保存当前的排列（长度最多 9）以及几个临时变量，空间复杂度是 **O(n)**，也就是几乎不占内存。

#### 代码（Python）  

```python
from itertools import permutations

def smallestNumber_bruteforce(pattern: str) -> str:
    n = len(pattern)                     # pattern 长度
    digits = [str(i) for i in range(1, n + 2)]   # 需要的数字 1~n+1，全部转成字符串

    best = None                           # 用来记录当前找到的最小合法答案

    # 生成所有可能的排列（相当于把 1~n+1 的数字排成一行）
    for perm in permutations(digits):
        ok = True                         # 用来标记这组排列是否满足 pattern 的所有约束
        for i, ch in enumerate(pattern):
            if ch == 'I' and not (perm[i] < perm[i + 1]):   # 要递增但不满足
                ok = False
                break
            if ch == 'D' and not (perm[i] > perm[i + 1]):   # 要递减但不满足
                ok = False
                break
        if ok:                            # 只要合法，就和当前最小答案比大小
            cur = ''.join(perm)           # 把元组转成字符串，方便比较
            if best is None or cur < best:
                best = cur                # 更新最小答案

    return best                           # 题目保证一定有答案
```

#### 复杂度  

- **时间复杂度**：`O(9!·n)`  
  - 解释：`9!` 表示所有可能的排列数量，`n` 表示我们要检查的约束次数。因为 `n ≤ 8`，所以 `9!·n` 仍在可接受范围。  
- **空间复杂度**：`O(n)`  
  - 解释：只保存当前排列（长度 n+1）和若干临时变量，随 `n` 线性增长。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**枚举所有排列**——大多数排列根本不满足条件，却仍被遍历检查。我们可以利用 pattern 本身的结构，直接构造出字典序最小的合法序列。

观察：

1. `pattern` 只包含 `'I'`（递增）和 `'D'`（递减）。  
2. 为了让结果字典序最小，我们希望**左边的数字尽可能小**。  
3. 当出现一段连续的 `'D'`（比如 `"DDDD"`），我们必须让这段对应的数字序列是严格递减的。要让整体字典序最小，最好的办法是把这段数字**倒着放**，即使用一段连续递增的自然数后再倒序输出。

这正好可以用**栈**来实现：

- 我们从左到右遍历 `pattern`，并在每一步**把当前下标 + 1**（即要使用的下一个数字）压入栈。  
- 当遇到 `'I'` 时，意味着前面的 `'D'`（如果有）已经结束，需要把栈里的数字全部弹出（弹出顺序恰好是倒序），写入答案。  
- 最后遍历完 `pattern` 后，还会剩下一个数字（`n+1`），以及栈中可能残留的数字，也全部弹出即可。

这样 **只遍历一次**，就能得到字典序最小的合法序列。

**类比**：把栈想象成“临时的倒装箱”。我们把数字一个个放进去，当遇到需要递增的位置（`'I'`）时，就把箱子里的数字全部倒出来，保证倒出的顺序是递减的，从而满足之前的 `'D'` 要求。  

#### 代码（Python）  

```python
def smallestNumber(pattern: str) -> str:
    """
    使用栈 + 贪心的线性构造方法
    """
    stack = []          # 临时栈，用来保存尚未输出的数字
    result = []         # 最终答案的字符列表

    n = len(pattern)
    for i in range(n + 1):          # 需要使用 1~n+1 共 n+1 个数字
        stack.append(str(i + 1))    # 把当前数字压入栈（转成字符方便后面拼接）

        # 当 i == n（已经是最后一个数字）或者当前字符是 'I' 时，
        # 说明前面的所有连续的 'D' 已经结束，需要把栈中的数字倒序弹出
        if i == n or pattern[i] == 'I':
            while stack:            # 弹出所有暂存的数字
                result.append(stack.pop())

    return ''.join(result)          # 把字符列表拼成最终字符串
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：我们只遍历一次 `pattern`（长度 n），每个数字最多进栈一次、出栈一次，整体操作次数和 `n` 成线性关系。相比暴力的 `9!·n`，快了好几个数量级。  
- **空间复杂度**：`O(n)`  
  - 解释：栈里最多会存放一段连续 `'D'` 对应的数字，最坏情况下是全部 `n+1` 个数字，随 `n` 线性增长。  

---  

## 心得  

- **核心技巧**：**栈 + 贪心**，把连续的递减段倒序输出，以获得字典序最小的序列。  
- **适用的题型**：  
  1. “根据 I/D 模式生成最小/最大数字”系列（如 LeetCode 2375）  
  2. “根据栈的特性恢复序列”类题目（如验证栈序列合法性）  
  3. “利用单调栈处理区间递增/递减” 的一些变形。  
- **一句话总结**：遇到 I/D（递增/递减）约束时，**把连续的 D 用栈倒序输出**，即可在一次遍历中得到字典序最小解。  

---  

## 反思  

- **第一反应**：先想到“全排列枚举”，因为 n 很小，直接暴力就能通过。  
- **最容易踩的坑**：  
  - **忘记在最后一次循环时也要弹栈**（因为 pattern 末尾可能是 `'D'`，需要把剩余数字全部倒出）。  
  - **下标偏移**：栈里压入的是 `i+1`（从 1 开始），而不是直接压入 `i`，否则会缺少最大的数字 `n+1`。  
  - **字符与整数混用**：在比较或拼接时保持类型一致（这里统一转成字符）。  
- **下次思路**：看到 “I/D” 这类只涉及相邻大小关系的字符串，第一步就考虑**单调栈或贪心**，而不是直接枚举。这样可以把时间复杂度从指数级降到线性级。