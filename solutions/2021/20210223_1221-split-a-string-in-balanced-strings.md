# #1221. 将字符串划分为平衡子串 / Split a String in Balanced Strings

> 难度：简单 · 标签：String、Greedy、Counting · [LeetCode 链接](https://leetcode.com/problems/split-a-string-in-balanced-strings/)

---

## 题目（英文原版）

**Description**

Balanced strings are those that have an equal quantity of 'L' and 'R' characters.
Given a balanced string s, split it into some number of substrings such that:
Return the maximum number of balanced strings you can obtain.

**Examples**

**Example 1:**

```
Input: s = "RLRRLLRLRL"
Output: 4
Explanation: s can be split into "RL", "RRLL", "RL", "RL", each substring contains same number of 'L' and 'R'.
```

**Example 2:**

```
Input: s = "RLRRRLLRLL"
Output: 2
Explanation: s can be split into "RL", "RRRLLRLL", each substring contains same number of 'L' and 'R'.
Note that s cannot be split into "RL", "RR", "RL", "LR", "LL", because the 2nd and 5th substrings are not balanced.
```

**Example 3:**

```
Input: s = "LLLLRRRR"
Output: 1
Explanation: s can be split into "LLLLRRRR".
```

**Constraints**

- 2 <= s.length <= 1000
- s[i] is either 'L' or 'R'.
- s is a balanced string.

---

## 题目（中文翻译）

平衡字符串（balanced strings）是指其中 `'L'` 与 `'R'` 的数量相等的字符串。  
给定一个平衡字符串 `s`，将其划分为若干子串，使得每个子串都是平衡的。  
返回能够得到的平衡子串的最大数量。

**示例 1**  
**输入**: `s = "RLRRLLRLRL"`  
**输出**: `4`  
**解释**: `s` 可以划分为 `"RL"`, `"RRLL"`, `"RL"`, `"RL"`，每个子串都包含相同数量的 `'L'` 与 `'R'`。

**示例 2**  
**输入**: `s = "RLRRRLLRLL"`  
**输出**: `2`  
**解释**: `s` 可以划分为 `"RL"`, `"RRRLLRLL"`，每个子串都包含相同数量的 `'L'` 与 `'R'`。需要注意的是，`s` 不能划分为 `"RL"`, `"RR"`, `"RL"`, `"LR"`, `"LL"`，因为第 2 和第 5 个子串不是平衡的。

**示例 3**  
**输入**: `s = "LLLLRRRR"`  
**输出**: `1`  
**解释**: `s` 只能划分为 `"LLLLRRRR"`。

**约束条件**  
- `2 <= s.length <= 1000`  
- `s[i]` 只能是 `'L'` 或 `'R'`。  
- `s` 本身是一个平衡字符串。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**枚举所有可能的切分方式**，检查每一种切分后得到的子串是否都是平衡的（即 `'L'` 与 `'R'` 数量相等），取能得到的最大子串数。  

- **数据结构**：我们只需要把原字符串 `s` 按下标切成若干段，用 Python 的切片 `s[i:j]` 来得到子串。  
- **类比**：把字符串想成一根珠子链，暴力做法相当于把链子上的每一颗珠子都拿出来尝试所有可能的“剪刀”，看哪一种剪法能得到最多的“等重”小段。  
- **正确性**：只要遍历到了所有合法的切分方式，就一定能找到最优解，因为没有遗漏的可能性。  

#### 代码（Python）  
```python
def max_balanced_bruteforce(s: str) -> int:
    n = len(s)
    best = 0                         # 记录找到的最大平衡子串数

    # 用递归枚举从下标 start 开始的所有切分方式
    def dfs(start: int, cnt: int):
        nonlocal best
        # 如果已经遍历到字符串末尾，更新答案
        if start == n:
            best = max(best, cnt)
            return

        # 尝试所有可能的右端点 end（必须大于 start）
        # 只要子串 s[start:end] 是平衡的，就递归继续切下去
        balance = 0
        for end in range(start + 1, n + 1):
            # 更新 balance：遇到 'L' 加 1，遇到 'R' 减 1
            balance += 1 if s[end - 1] == 'L' else -1
            if balance == 0:          # 找到一个平衡子串
                dfs(end, cnt + 1)     # 递归处理剩余部分

    dfs(0, 0)
    return best
```

> **关键行解释**  
> - `balance += 1 if s[end - 1] == 'L' else -1`：相当于把 `'L'` 当作 +1、 `'R'` 当作 -1，平衡时累加到 0。  
> - `if balance == 0:`：只要当前子串的 `'L'` 与 `'R'` 数量相等，就可以把它作为一个完整的块。  

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）。因为每次找到一个平衡子串就会产生一次递归分支，最坏情况下会遍历所有切分组合。对 `n ≤ 1000` 的数据根本不可行。  
- **空间复杂度**：`O(n)`，递归栈的深度最坏等于字符串长度。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正的瓶颈在于不停地回溯、重新统计子串的平衡情况**。实际上，我们只需要一次遍历就能得到答案，原因如下：

1. **平衡子串的最小结束位置**  
   当我们从左到右扫描时，累计一个“平衡计数器” `balance`（`L` → +1，`R` → -1）。只要 `balance` 重新回到 **0**，说明从上一次计数为 0 的位置到当前下标之间的字符数恰好是平衡的。此时把这段切下来是**安全且最早的**切分，因为再往后再切只会让已经得到的子串更长，导致可切分的块数减少。  

2. **贪心原则**  
   每当 `balance` 为 0，就立即把当前段计为一个完整的平衡子串，然后继续往后扫描。这样可以**最大化子串数量**——因为我们把每段都切得尽可能短。  

3. **只需要一个计数器**  
   不需要额外的哈希表、前缀和数组，只要一个整数 `balance` 和答案计数器 `ans`。  

#### 类比  
把字符串想成一条在山谷中起伏的道路，`balance` 就是海拔高度（`L` 上升，`R` 下降）。每当海拔回到起点（高度 0）时，说明走完了一段“上下相等”的山谷，这段可以独立成一段路。我们每到一次海拔 0，就把这段路“收割”一次，继续前进。  

#### 代码（Python）  
```python
def max_balanced_greedy(s: str) -> int:
    balance = 0   # 记录当前段的 L 与 R 的差值，L 为 +1，R 为 -1
    ans = 0       # 已经切出的平衡子串数量

    for ch in s:
        # 更新平衡计数器
        balance += 1 if ch == 'L' else -1

        # 当 balance 恢复到 0，说明当前段已经平衡
        if balance == 0:
            ans += 1          # 计数 +1，开始统计下一段
    return ans
```

> **关键行解释**  
> - `balance += 1 if ch == 'L' else -1`：把 `'L'` 当作 +1、 `'R'` 当作 -1，实时维护两者差值。  
> - `if balance == 0:`：只要差值回到 0，就说明从上一次计数为 0 的位置到现在的子串是平衡的，立即计数并继续。  

#### 复杂度  

- **时间复杂度**：`O(n)`。只遍历一次字符串，`n` 为字符串长度。对 1000 长度的输入毫无压力。  
- **空间复杂度**：`O(1)`。只使用了常数个额外变量（`balance`、`ans`），不随输入规模增长。  

---  

## 心得  

- **核心技巧**：**贪心 + 计数器**，在遍历过程中实时维护 `'L'` 与 `'R'` 的差值，一旦恢复到 0 就立刻切分。  
- **适用的题型**：  
  1. “划分平衡子串” 类题（如 LeetCode 1221 Split a String in Balanced Strings）。  
  2. “计数平衡的子数组/子串” 如 `count subarrays with equal number of 0 and 1`。  
  3. “前缀和为零的分段” 如 “分割数组使每段和为 0”。  
- **一句话总结解题钥匙**：**每次出现平衡点就立刻切，切得越早子串越多**。  

## 反思  

- **第一反应**：看到 “平衡字符串” 立刻想到计数 `'L'` 与 `'R'` 的差值，想用哈希表记录前缀和。  
- **最容易踩的坑**：  
  - 忘记把 `'L'` 当作 **+1**、 `'R'` 当作 **-1**（方向写反会导致永远不为 0）。  
  - 误以为只要整体平衡就一定能切成 `len(s)//2` 段，实际切分数取决于 **平衡点出现的次数**。  
  - 边界条件：空字符串不在题目范围，但如果出现，需要返回 0。  
- **下次类似题的第一步**：**先设一个计数器，遍历一次，遇到计数器回到初始值就可以“收割”一段**。这样即可快速得到最大划分数。