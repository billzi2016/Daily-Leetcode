# #2663. 字典序最小的美丽字符串 / Lexicographically Smallest Beautiful String

> 难度：困难 · 标签：String、Greedy · [LeetCode 链接](https://leetcode.com/problems/lexicographically-smallest-beautiful-string/)

---

## 题目（英文原版）

**Description**

A string is beautiful if:
You are given a beautiful string s of length n and a positive integer k.
Return the lexicographically smallest string of length n, which is larger than s and is beautiful. If there is no such string, return an empty string.
A string a is lexicographically larger than a string b (of the same length) if in the first position where a and b differ, a has a character strictly larger than the corresponding character in b.

**Examples**

**Example 1:**

```
Input: s = "abcz", k = 26
Output: "abda"
Explanation: The string "abda" is beautiful and lexicographically larger than the string "abcz".
It can be proven that there is no string that is lexicographically larger than the string "abcz", beautiful, and lexicographically smaller than the string "abda".
```

**Example 2:**

```
Input: s = "dc", k = 4
Output: ""
Explanation: It can be proven that there is no string that is lexicographically larger than the string "dc" and is beautiful.
```

**Constraints**

- 1 <= n == s.length <= 105
- 4 <= k <= 26
- s is a beautiful string.

---

## 题目（中文翻译）

如果一个字符串满足以下条件，则称其为**美丽字符串 (beautiful string)**。  
给定一个长度为 `n` 的美丽字符串 `s` 和一个正整数 `k`。  
返回长度为 `n`、字典序大于 `s` 且仍是美丽字符串的 **字典序最小的字符串 (lexicographically smallest string)**。如果不存在满足条件的字符串，返回空字符串 `""`。

**字典序**的比较方式：若两个等长字符串在首次出现不同的字符位置上，前者的字符严格大于后者的字符，则前者的字典序大于后者。

---

### 示例

**示例 1**  
```
Input: s = "abcz", k = 26
Output: "abda"
```
**解释**：字符串 `"abda"` 是美丽的，并且字典序大于 `"abcz"`。可以证明不存在既字典序大于 `"abcz"`、又是美丽的，同时字典序小于 `"abda"` 的字符串。

**示例 2**  
```
Input: s = "dc", k = 4
Output: ""
```
**解释**：可以证明不存在字典序大于 `"dc"` 且仍为美丽的字符串。

---

### 约束

- `1 <= n == s.length <= 10^5`
- `4 <= k <= 26`
- `s` 为美丽字符串。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的字符串**，找出满足两条条件的最小解：

1. 该字符串 `t` 与给定的美丽字符串 `s` 同长度 `n`，且 `t` 在字典序上严格大于 `s`。  
2. `t` 仍然是“beautiful”，即**不存在**长度为 2 或 3 的回文子串（题目已经说明，只要这两类回文不存在，所有更长的回文也一定不存在）。

实现思路如下：

- 从 `s` 的右侧开始逐个位置尝试把字符往后调（`'a' → 'b' → … → 'a'+k-1`），每次调完后把右边的所有位置都填成最小字符 `'a'`（因为我们想要字典序最小）。  
- 检查得到的整串是否仍然没有长度 2、3 的回文子串。  
- 若满足，就返回；若遍历完所有位置仍未找到，则返回空串。

> **生活化类比**：把字符串看成一排颜色盒子，每个盒子只能放 `k` 种颜色（`a…a+k-1`），并且相邻两盒子或相隔一盒子的颜色不能相同（否则会形成长度 2/3 的回文）。我们从最右边的盒子开始“往后换颜色”，换完后把右边的盒子全部涂成最浅的颜色 `a`，确保整体“最亮”。随后检查整个排是否满足“不相同”规则。

这个方法**必然正确**，因为我们枚举了**所有**比 `s` 更大的合法字符串，最先找到的就是字典序最小的那一个。

#### 代码（Python）

```python
def is_beautiful(t: str, k: int) -> bool:
    """检查字符串 t 是否没有长度 2、3 的回文子串"""
    n = len(t)
    for i in range(n):
        if i >= 1 and t[i] == t[i-1]:          # 长度 2 回文
            return False
        if i >= 2 and t[i] == t[i-2]:          # 长度 3 回文
            return False
    return True


def brute_force(s: str, k: int) -> str:
    n = len(s)
    chars = [chr(ord('a') + i) for i in range(k)]   # 可用字符列表

    # 从右往左尝试提升字符
    for i in range(n - 1, -1, -1):
        cur_idx = chars.index(s[i])                # s[i] 在 chars 中的下标
        # 尝试把 s[i] 换成更大的字符
        for nxt in range(cur_idx + 1, k):
            # 生成候选字符串
            t = list(s)
            t[i] = chars[nxt]                       # 把位置 i 提升
            # 右边全部填最小字符 'a'（即 chars[0]）
            for j in range(i + 1, n):
                t[j] = chars[0]
            cand = ''.join(t)
            if is_beautiful(cand, k):
                return cand
    return ''        # 没有合法解
```

> **关键行注释**  
> - `is_beautiful`：遍历一次字符串，检查相邻或相隔一位的字符是否相同（即出现长度 2/3 回文）。  
> - 外层 `for i`：从右往左遍历，保证“一旦找到”即是字典序最小的提升点。  
> - 内层 `for nxt`：尝试把当前位置的字符往后改成下一个可能的字符。  
> - `for j in range(i + 1, n)`：把右侧全部填成最小字符 `'a'`，确保字典序尽可能小。

#### 复杂度  

- **时间复杂度**：`O(n * k * n)` ≈ `O(n²·k)`  
  - 最外层遍历 `n` 次（每个位置），  
  - 每次尝试至多 `k` 个更大的字符，  
  - 检查合法性（`is_beautiful`）需要遍历整个字符串 `O(n)`。  
  - 对于 `n ≤ 10⁵`、`k ≤ 26`，这会导致 **十亿级**操作，远远超出时限。

- **空间复杂度**：`O(n)`  
  - 主要是构造候选字符串 `t` 时需要的临时数组。  

> 大白话：时间复杂度 `O(n²·k)` 就像让你把每本书的每一页都读 `k` 次再检查一次，显然太慢了。我们需要更聪明的办法把“检查”和“提升”一步搞定。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈**在于：

1. 每次提升字符后都要**重新检查整个字符串**是否满足美丽条件。  
2. 右侧的字符每次都被重新填成 `'a'`，导致大量不必要的重复工作。

我们可以利用**局部约束**的特性来一次完成检查与构造：

- **美丽字符串的本质**：只要**相邻两字符不相同**且**相隔两字符不相同**（即 `s[i] != s[i-1]` 且 `s[i] != s[i-2]`），就不会出现长度 2、3 的回文，进而不会出现更长的回文。  
  - 这相当于给每个位置 `i` 加了两条“禁忌”：不能和左边第 1 位、左边第 2 位相同。

- **从右往左贪心**：  
  1. 从右到左遍历位置 `i`，尝试把 `s[i]` **提升**到下一个可用字符 `c`（`c > s[i]` 且 `c` 不违反上述两条禁忌）。  
  2. 若找到了这样的 `c`，则把 `s[i] = c`，**并把 i 右侧的所有位置都填成最小可能字符**（从 `'a'` 开始逐个尝试，满足禁忌即停），这样得到的字符串必然是**字典序最小**且**仍然美丽**。  
  3. 一旦成功提升并填完右侧，就可以直接返回；因为我们是从右往左，第一次成功的提升点已经保证整体字典序最小。

- **填充右侧的技巧**（同样是贪心）：  
  对于每个右侧位置 `j`（从 `i+1` 向后），从 `'a'` 开始尝试字符 `c`，只要 `c` 不等于 `t[j-1]`（左邻）也不等于 `t[j-2]`（左左邻），就把 `t[j]=c` 并继续下一个位置。因为我们总是取字典序最小的合法字符，整个后缀自然是最小的。

> **类比**：把字符串看成一条单行轨道，车厢只能放 `k` 种颜色的车票，而且相邻两节车厢和相隔一节的车厢**不能使用同样的颜色**。我们从最右边的车厢开始尝试把颜色调高（向后换颜色），一旦成功，就把右边所有车厢重新装上**最便宜的颜色**（`'a'`），并且保证不违反相邻/相隔的禁令。这样得到的列车既比原来“贵”（字典序更大），又是“最便宜的升级版”。

#### 代码（Python）

```python
def smallest_beautiful(s: str, k: int) -> str:
    """
    返回字典序最小、比 s 大且仍然 beautiful 的字符串；
    若不存在返回空串。
    """
    n = len(s)
    a_ord = ord('a')
    max_char = a_ord + k - 1               # 可用字符的最大 ASCII 码

    # 把字符串转成可修改的列表
    t = list(s)

    # ---------- 第一步：从右往左找可以提升的位置 ----------
    for i in range(n - 1, -1, -1):
        # 当前字符的 ASCII
        cur = ord(t[i])

        # 尝试把位置 i 的字符提升到更大的合法字符
        for nxt in range(cur + 1, max_char + 1):
            # 检查禁忌：不能和左边 1 位、2 位相同
            if i >= 1 and nxt == ord(t[i - 1]):
                continue
            if i >= 2 and nxt == ord(t[i - 2]):
                continue

            # 找到合法的提升字符，先写进去
            t[i] = chr(nxt)

            # ---------- 第二步：把 i 右侧填成最小合法字符 ----------
            for j in range(i + 1, n):
                # 从最小字符 'a' 开始尝试
                for cand in range(a_ord, max_char + 1):
                    if j >= 1 and cand == ord(t[j - 1]):
                        continue          # 与左邻冲突
                    if j >= 2 and cand == ord(t[j - 2]):
                        continue          # 与左左邻冲突
                    t[j] = chr(cand)      # 选到合法最小字符，写入
                    break                 # 结束内部循环，进入下一个位置
                # 理论上一定能找到，因为 k ≥ 4 保证有足够颜色

            return ''.join(t)            # 成功构造，直接返回

    # 遍历完都没有找到合法提升点，说明不存在答案
    return ''
```

> **关键行中文注释**  
> - `if i >= 1 and nxt == ord(t[i - 1]): continue`  // 与左边相邻字符相同会产生长度 2 回文，不能取。  
> - `if i >= 2 and nxt == ord(t[i - 2]): continue`  // 与左边第 2 位相同会产生长度 3 回文，不能取。  
> - 填右侧时的双层 `for cand` 循环：从 `'a'` 开始逐个尝试，只要不违反两条禁忌，就确定该位的最小合法字符。由于 `k ≥ 4`，一定能找到（最坏情况是排除掉左邻、左左邻两种颜色，剩下至少两种可选）。

#### 复杂度  

- **时间复杂度**：`O(n * k)`  
  - 外层遍历 `n` 次（每个位置最多尝试一次提升），  
  - 每次提升后填右侧时，每个位置最多检查 `k` 次字符（最坏遍历全部可选字符），  
  - 所以整体是 `n * k`，在本题约为 `10⁵ * 26 ≈ 2.6×10⁶`，完全可接受。  

- **空间复杂度**：`O(n)`  
  - 只使用了一个字符列表 `t` 来存储当前构造的字符串。  

> 与暴力解相比，时间从 `O(n²·k)` 降到了 `O(n·k)`，把“每次检查全串”改成了“局部检查”，把“重新填满右侧”改成了“一次性贪心填充”。这正是贪心算法的核心——**局部最优** ⇒ **全局最优**。

---

## 心得

- **核心技巧**：**局部约束 + 从右往左贪心**  
  - 只要保证每个位置不与左边 1、2 位相同，就能确保整个字符串美丽。  
  - 从右往左尝试提升，第一次成功的提升点即是字典序最小的答案。

- **适用的题型**  
  1. “不出现相邻/相隔字符相同” 的字符串构造类（如 **Avoid Palindromes**、**Construct String With No Adjacent Repeating Characters**）。  
  2. 需要在满足**局部限制**的前提下，求**字典序最小/大的**后继/前驱字符串（如 **Next Permutation with Constraints**）。  
  3. 任何可以用**前缀不变、后缀最小化**思路解决的“字典序后继”问题。

- **一句话总结解题钥匙**  
  > “只要不和左边的两位相同，就一定美丽；从右往左把第一个可以提升的位调大，再把右侧全部填最小合法字符，即得到字典序最小的更大美丽串。”

---

## 反思

- **第一反应**：看到“beautiful”且涉及回文，立刻想到**检测所有子串**，于是想用暴力枚举。其实题目已经给出关键提示：只需关注长度 2、3 的回文即可。

- **最容易踩的坑**  
  1. **边界条件**：位置 `i=0`、`i=1` 时没有左侧第 1 位或第 2 位，需要额外判断避免索引错误。  
  2. **字符集合大小**：若 `k` 太小（比如 `k=2`），可能根本不存在合法填充；题目保证 `k ≥ 4`，所以在填右侧时一定能找到合法字符。若忘记这点，代码可能在循环里找不到合法字符而卡死。  
  3. **返回空串的时机**：必须在遍历完所有位置仍未找到提升点时才返回 `''`，否则会错误地提前结束。

- **下次遇到同类题，第一步该想到**  
  > “把约束写成‘不能和左边前两位相同’，然后从右往左尝试提升，后缀用最小合法字符填充”。  
  这一步把问题从全局搜索压缩到局部检查，往往能把复杂度降到线性。