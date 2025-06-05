# #3216. 一次交换后字典序最小的字符串 / Lexicographically Smallest String After a Swap

> 难度：简单 · 标签：String、Greedy · [LeetCode 链接](https://leetcode.com/problems/lexicographically-smallest-string-after-a-swap/)

---

## 题目（英文原版）

**Description**

Given a string s containing only digits, return the lexicographically smallest string that can be obtained after swapping adjacent digits in s with the same parity at most once.
Digits have the same parity if both are odd or both are even. For example, 5 and 9, as well as 2 and 4, have the same parity, while 6 and 9 do not.

**Examples**

**Example 1:**

```
Input: s = "45320"
Output: "43520"
Explanation:
s[1] == '5' and s[2] == '3' both have the same parity, and swapping them results in the lexicographically smallest string.
```

**Example 2:**

```
Input: s = "001"
Output: "001"
Explanation:
There is no need to perform a swap because s is already the lexicographically smallest.
```

**Constraints**

- 2 <= s.length <= 100
- s consists only of digits.

---

## 题目（中文翻译）

给定仅包含数字的字符串 `s`，返回在至多一次地交换相邻且奇偶性相同的数字后能够得到的字典序最小的字符串。

如果两个数字的奇偶性相同，则它们的奇偶性(parity)相同，即要么都是奇数(odd)，要么都是偶数(even)。例如，5 与 9、2 与 4 奇偶性相同，而 6 与 9 则不同。

**示例 1**  
输入: `s = "45320"`  
输出: `"43520"`  
解释: `s[1] == '5'` 与 `s[2] == '3'` 的奇偶性相同，交换它们后得到的字符串字典序最小。

**示例 2**  
输入: `s = "001"`  
输出: `"001"`  
解释: 已经是字典序最小的字符串，无需进行交换。

**约束条件**  
- `2 <= s.length <= 100`  
- `s` 仅由数字组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把所有合法的相邻交换都尝试一次**，再把得到的所有字符串和原字符串进行字典序（lexicographic）比较，取最小的那个。  

- **合法交换**：只能交换相邻的两个字符，且这两个字符的奇偶性相同（都是奇数或都是偶数）。  
- **数据结构**：我们只需要把原字符串 `s` 看成一个字符数组，遍历它就行了。可以把 “哈希表” 想象成查字典——这里不需要哈希，只要顺序遍历就能找到所有可能的交换。  
- **为什么一定对**：题目限制最多只进行一次交换，而我们把**所有**可能的“一次交换”都列举出来（包括不交换的情况），所以必然能找到字典序最小的那个。  

#### 代码（Python）

```python
def smallestStringAfterSwap_bruteforce(s: str) -> str:
    # 先把原字符串当作当前最小答案
    best = s

    # 把字符串转成列表，方便交换后再拼接成新字符串
    chars = list(s)
    n = len(chars)

    # 遍历所有相邻位置 i,i+1
    for i in range(n - 1):
        # 判断奇偶性是否相同
        if (int(chars[i]) - int(chars[i + 1])) % 2 == 0:   # 同奇同偶
            # 只在交换后可能更小的情况下才尝试（可选优化）
            if chars[i] > chars[i + 1]:
                # 交换 i 与 i+1
                chars[i], chars[i + 1] = chars[i + 1], chars[i]
                candidate = ''.join(chars)   # 把列表转回字符串
                # 更新最小答案
                if candidate < best:
                    best = candidate
                # 恢复原状，继续尝试其它位置的交换
                chars[i], chars[i + 1] = chars[i + 1], chars[i]

    return best
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层遍历 `n` 次（每个相邻位置），每次交换后需要 `O(n)` 时间把列表拼成字符串并比较。  
  - 用大白话说，就是“如果字符串有 100 位，最坏情况下要做 100 × 100 = 10 000 次小工作”。  
- **空间复杂度**：`O(n)`  
  - 需要额外的字符列表保存 `s`，长度和原字符串相同。  

---

### 2. 最优解

#### 思路  

暴力解的慢点在于 **把每一种可能都完整地重新拼接一次**。实际上我们只需要比较**哪一次交换能够让最左边的字符变小**，因为字典序的比较规则是“左边先比较，左边更小整体就更小”。  

**关键观察**  

1. 只允许一次相邻交换。  
2. 交换只能在奇数‑奇数 或 偶数‑偶数 的相邻位置上进行。  
3. 如果在位置 `i` 与 `i+1` 之间交换后，得到的字符 `s[i+1]` 比 `s[i]` 小，那么字典序一定会在第 `i` 位变得更小，后面的字符再怎么变化都不影响整体的大小。  

因此，我们只要找 **最左侧** 的满足以下两点的相邻对：

- 两个字符奇偶相同。  
- 左边的字符大于右边的字符（`s[i] > s[i+1]`），这样交换后左边会变小。  

找到后直接交换一次即可；如果遍历完都没有满足条件，则不需要交换，原字符串已经是最小的。  

**为什么这就是最优**  

- 由于字典序的比较从左到右进行，**最左** 能让字符变小的交换必定产生全局最小的结果。  
- 只遍历一次字符串，时间 `O(n)`，空间只用常数 `O(1)`（不需要额外的列表），是最简洁的做法。  

#### 代码（Python）

```python
def smallestStringAfterSwap_greedy(s: str) -> str:
    chars = list(s)          # 转成列表，方便原地交换
    n = len(chars)

    # 从左到右寻找第一个可以让左侧字符变小的合法相邻对
    for i in range(n - 1):
        a, b = chars[i], chars[i + 1]
        # 判断奇偶性相同：两数同奇或同偶 => (a - b) 为偶数
        if (int(a) - int(b)) % 2 == 0 and a > b:
            # 进行一次交换，立刻返回结果
            chars[i], chars[i + 1] = b, a
            return ''.join(chars)

    # 没有找到合适的交换，直接返回原字符串
    return s
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，最多检查 `n‑1` 对相邻字符。用大白话说，长度 100 的字符串只需要检查 99 次，几乎是瞬间完成。  
- **空间复杂度**：`O(1)`（不计输出字符串）  
  - 只用了几个临时变量 `a, b, i`，没有额外的随 `n` 增长的容器。  

---

## 心得

- 这道题考察的核心技巧是 **“贪心 + 字典序比较”**：找出最左侧可以改进的局部位置，直接进行一次操作即可得到全局最优。  
- 该技巧常用于只能进行一次或少数局部修改的题目，例如：  
  1. “一次交换后得到的最小字符串”  
  2. “一次翻转后得到的最大二进制数”  
  3. “一次删除字符后得到的最小数字”。  
- **一句话总结解题钥匙**：**“字典序最左优先，找到第一对能让左边变小的合法相邻位，立刻交换”。**  

---

## 反思

- **第一反应**：先想到遍历所有合法交换并比较——直觉的暴力枚举。  
- **最容易踩的坑**：  
  - 忘记判断奇偶性相同，只比较相邻字符会导致非法交换。  
  - 只比较字符大小而忽略“左边更重要”的字典序特性，可能误选了右侧更小的交换。  
  - 边界情况：全是奇数或全是偶数且已经递增（如 `"1234"`），此时应直接返回原串。  
- **下次遇到同类题**：第一步先问自己“字典序最左位置是否可以改进”，再决定是暴力枚举还是直接贪心。这样可以快速定位最优解的搜索范围。