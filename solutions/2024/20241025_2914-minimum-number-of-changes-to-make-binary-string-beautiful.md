# #2914. 使二进制字符串美观的最少修改次数 / Minimum Number of Changes to Make Binary String Beautiful

> 难度：中等 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-changes-to-make-binary-string-beautiful/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed binary string s having an even length.
A string is beautiful if it's possible to partition it into one or more substrings such that:
You can change any character in s to 0 or 1.
Return the minimum number of changes required to make the string s beautiful.

**Examples**

**Example 1:**

```
Input: s = "1001"
Output: 2
Explanation: We change s[1] to 1 and s[3] to 0 to get string "1100".
It can be seen that the string "1100" is beautiful because we can partition it into "11|00".
It can be proven that 2 is the minimum number of changes needed to make the string beautiful.
```

**Example 2:**

```
Input: s = "10"
Output: 1
Explanation: We change s[1] to 1 to get string "11".
It can be seen that the string "11" is beautiful because we can partition it into "11".
It can be proven that 1 is the minimum number of changes needed to make the string beautiful.
```

**Example 3:**

```
Input: s = "0000"
Output: 0
Explanation: We don't need to make any changes as the string "0000" is beautiful already.
```

**Constraints**

- 2 <= s.length <= 105
- s has an even length.
- s[i] is either '0' or '1'.

---

## 题目（中文翻译）

给定一个下标从 0 开始、长度为偶数的二进制字符串 s（binary string）。
如果可以将字符串划分（partition）成一个或多个子字符串（substring），则称该字符串是 **美观的**（beautiful）。
你可以将 s 中的任意字符改为 `0` 或 `1`。
返回使字符串 s 成为美观字符串所需的最少修改次数。

---

### 示例

**示例 1**  
Input: `s = "1001"`  
Output: `2`  
**解释**：我们将 `s[1]` 改为 `1`，将 `s[3]` 改为 `0`，得到字符串 `"1100"`。  
可以看到字符串 `"1100"` 是美观的，因为我们可以将其划分为 `"11|00"`。  
可以证明，修改 2 次是使该字符串美观的最小次数。

**示例 2**  
Input: `s = "10"`  
Output: `1`  
**解释**：我们将 `s[1]` 改为 `1`，得到字符串 `"11"`。  
可以看到字符串 `"11"` 是美观的，因为我们可以将其划分为 `"11"`。  
可以证明，修改 1 次是使该字符串美观的最小次数。

**示例 3**  
Input: `s = "0000"`  
Output: `0`  
**解释**：无需进行任何修改，因为字符串 `"0000"` 已经是美观的。

---

### 约束条件

- `2 <= s.length <= 10^5`
- `s` 的长度为偶数
- `s[i]` 只能是 `'0'` 或 `'1'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的分割方式**，然后对每一种分割检查是否能把每个子串变成“只含相同字符且长度为偶数”的形式，再统计最少需要改动的字符数。  

- **数据结构**：我们可以把字符串看成一本字典，字典的每一页对应一个子串。要判断一本页是否“好看”，只要检查这页里所有字符是否相同且页数（子串长度）是偶数。  
- **正确性**：因为题目要求**能够**把原串划分成若干满足条件的子串，只要我们遍历了所有可能的划分，就一定能找到最少改动的那一种。  

但是，这种做法在实际执行时会非常慢。假设字符串长度为 `n`（`n` 为偶数），划分点有 `n‑1` 个，每个划分点可以选或不选，导致 **2^{n‑1}** 种划分方式，指数级的爆炸，根本不可行。

#### 代码（Python）

```python
def minChanges_bruteforce(s: str) -> int:
    n = len(s)
    ans = float('inf')

    # 用递归枚举所有划分（这里仅作概念展示，实际跑不完）
    def dfs(idx: int, changes: int):
        nonlocal ans
        if idx == n:                     # 已划分完全部字符
            ans = min(ans, changes)       # 更新最小改动次数
            return
        # 试着把从 idx 开始的任意偶长子串当作一个块
        for end in range(idx + 2, n + 1, 2):   # 只取偶数长度
            block = s[idx:end]
            # 统计把 block 变成全 0 或全 1 所需的最少改动
            cnt0 = sum(ch != '0' for ch in block)
            cnt1 = sum(ch != '1' for ch in block)
            dfs(end, changes + min(cnt0, cnt1))

    dfs(0, 0)
    return ans
```

> **注意**：上述代码仅用于说明“暴力枚举”的思路，实际运行会因为指数级递归而超时。

#### 复杂度

- **时间复杂度**：`O(2^{n})`（指数级），因为每个划分点都有两种选择，等价于遍历所有子集。  
  大白话：如果字符串有 20 个字符，可能的划分方式就有大约 **一百万** 种；如果有 30 个字符，可能的划分方式就会超过 **十亿**，根本不可能在一秒钟内算完。  
- **空间复杂度**：`O(n)`，递归栈的深度最多 `n/2`，每层保存常数信息。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的难点在于枚举划分**。如果我们仔细观察题目给出的提示，会发现：

> 对于任何合法的划分，每个子串内部都是相同字符且长度为偶数 → 我们可以继续把每个子串再细分成长度恰好为 **2** 的块。

换句话说，**只要把整个字符串划分成若干不重叠的相邻「二元组」**（即 `(s[0],s[1]) , (s[2],s[3]) , …`），每个二元组只要内部字符相同，就一定可以组成一个合法的美丽字符串。  

因此，**只需要检查每一对相邻字符**：

- 若 `s[i] == s[i+1]`（i 为偶数），这一对已经满足条件，不需要改动。  
- 若 `s[i] != s[i+1]`，我们只需要把其中的一个改成另一个即可，使它们相同。改动次数最少为 **1**。

于是答案就是 **所有二元组中不相等的数量**。

> 类比：把每对相邻的字符想象成一把钥匙的两齿，如果两齿一样（`00` 或 `11`），钥匙可以直接插入锁孔；如果不一样（`01` 或 `10`），我们只需要把其中一齿磨平，使两齿相同，花费一次“打磨”。整个过程只要统计需要打磨的钥匙数即可。

#### 代码（Python）

```python
def minChanges(s: str) -> int:
    """
    返回把二进制字符串 s 变成 beautiful 所需的最少改动次数。
    思路：把 s 按相邻两字符划分成若干块，统计每块内部不相等的次数。
    """
    n = len(s)
    changes = 0
    # 步长为 2，遍历每个二元组
    for i in range(0, n, 2):
        if s[i] != s[i + 1]:      # 这一对字符不同，需要改动一次
            changes += 1
    return changes
```

> 关键行解释  
> - `for i in range(0, n, 2)`: 像在超市里每隔两件商品挑选一次，只挑选偶数下标的起始位置。  
> - `if s[i] != s[i + 1]`: 检查这两件商品（字符）是否相同。  
> - `changes += 1`: 发现不相同就记一笔改动。

#### 复杂度

- **时间复杂度**：`O(n)`，只需要一次线性扫描。  
  大白话：如果字符串有 100 万个字符，只需要走一遍，花费的时间大约是处理 100 万个字母的时间，极快。  
- **空间复杂度**：`O(1)`，只用了几个整型变量，和输入大小无关。

---

## 心得

- **核心技巧**：把「每段都是相同字符且长度为偶数」转化为「每相邻两个字符必须相同」，从而把全局问题化简为局部「二元组」的独立判断。  
- **适用的题型**  
  1. 「把字符串分成若干满足局部约束的块」的题目，例如 **Make The String Great**（要求相邻字符不同）。  
  2. 「把数组/字符串分成长度固定的子段」并统计每段的属性，如 **Minimum Number of Flips to Make Binary String Alternating**（每段长度为 1）。  
  3. 「把序列划分为若干相同元素的连续段」的计数类题，例如 **Partition Labels**（按字符出现范围划分）。  
- **一句话总结解题钥匙**：**把全局偶数‑相同约束等价为「每两个相邻字符必须相等」**, 只需逐对计数不相等的对数。

## 反思

- **第一反应**：看到「可以划分成若干子串」会想到动态规划或枚举所有划分。  
- **最容易踩的坑**  
  - 忘记题目已经保证字符串长度为偶数，直接遍历时可能出现越界。  
  - 误以为需要把每个子串内部的字符全部改成同一个值（比如全改成 `0`），其实每对只要内部相同即可，改动次数是每对不相等计 1。  
- **下次遇到同类题的第一步**：先**寻找局部等价关系**（如「相邻两字符相等」或「相邻两字符不同」），把全局约束拆解成**固定长度块的独立判断**，往往可以直接得到线性解法。