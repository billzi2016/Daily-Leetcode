# #1239. 唯一字符拼接字符串的最大长度 / Maximum Length of a Concatenated String with Unique Characters

> 难度：中等 · 标签：Array、String、Backtracking、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/maximum-length-of-a-concatenated-string-with-unique-characters/)

---

## 题目（英文原版）

**Description**

You are given an array of strings arr. A string s is formed by the concatenation of a subsequence of arr that has unique characters.
Return the maximum possible length of s.
A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: arr = ["un","iq","ue"]
Output: 4
Explanation: All the valid concatenations are:
- ""
- "un"
- "iq"
- "ue"
- "uniq" ("un" + "iq")
- "ique" ("iq" + "ue")
Maximum length is 4.
```

**Example 2:**

```
Input: arr = ["cha","r","act","ers"]
Output: 6
Explanation: Possible longest valid concatenations are "chaers" ("cha" + "ers") and "acters" ("act" + "ers").
```

**Example 3:**

```
Input: arr = ["abcdefghijklmnopqrstuvwxyz"]
Output: 26
Explanation: The only string in arr has all 26 characters.
```

**Constraints**

- 1 <= arr.length <= 16
- 1 <= arr[i].length <= 26
- arr[i] contains only lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组 `arr`。通过拼接 `arr` 的一个子序列（subsequence）得到的字符串 `s` 必须满足所有字符均为唯一字符（unique characters）。返回可能的最大 `s` 的长度。

**子序列** 是指可以通过删除原数组中的任意个（包括 0 个）元素而不改变剩余元素顺序得到的数组。

### 示例

#### 示例 1  
**输入**: `arr = ["un","iq","ue"]`  
**输出**: `4`  
**解释**: 所有合法的拼接结果包括:
- `""`
- `"un"`
- `"iq"`
- `"ue"`
- `"uniq"`（`"un"` + `"iq"`）
- `"ique"`（`"iq"` + `"ue"`）  
最长长度为 `4`。

#### 示例 2  
**输入**: `arr = ["cha","r","act","ers"]`  
**输出**: `6`  
**解释**: 可能的最长合法拼接为 `"chaers"`（`"cha"` + `"ers"`）和 `"acters"`（`"act"` + `"ers"`）。

#### 示例 3  
**输入**: `arr = ["abcdefghijklmnopqrstuvwxyz"]`  
**输出**: `26`  
**解释**: `arr` 中唯一的字符串包含了全部 26 个字母。

### 约束条件

- `1 <= arr.length <= 16`
- `1 <= arr[i].length <= 26`
- `arr[i]` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有子序列（即所有取或不取每个字符串的组合）都枚举出来，检查每个组合拼接后是否满足“字符互不相同”，然后记录最长的合法长度**。  

- **数据结构**  
  - `list` 用来存放原始的字符串数组 `arr`。  
  - 在枚举过程中，我们用 **Python 的 `itertools.product` / 位掩码** 来表示“取不取”。可以把每个字符串看成一个开关，`0` 表示不取，`1` 表示取。这样  `2^n`（`n = len(arr)`）种可能就对应了所有子序列。  
  - 检查字符是否唯一时，可以把字符当成 **字典（哈希表）** 的键：把出现过的字母放进 `set`，如果再次出现就说明有重复。哈希表就像一本字典，查找某个单词（这里是字母）是否已经在里面，只需要 O(1) 的时间。

- **为什么正确**  
  - 我们遍历了 **每一种可能的取法**，只要有合法的拼接方式，就一定会在遍历过程中被检查到。于是只要取所有合法方式的最大长度，即得到答案。

- **复杂度分析（大白话版）**  
  - **时间**：  
    - 枚举所有子序列需要 `2^n` 次（每个字符串两种状态：取或不取），`n ≤ 16`，所以最多是 `2^16 = 65536` 次，仍在可以接受的范围。  
    - 对每个子序列，我们把选中的字符串全部拼接起来，然后遍历这些字符检查是否有重复。最坏情况下拼接后的长度是 26（因为英文字母只有 26 个），所以检查一次的时间是 O(26) ≈ O(1)。  
    - 综合下来，整体时间是 **O(2ⁿ·L)**，其中 `L` 是每次检查的字符数（≤26），可以写成 **O(2ⁿ)**。  
    - 用大白话说，就是“随着字符串个数每增加一次，可能的组合数会翻倍”。  

  - **空间**：  
    - 只用了几个临时变量（比如当前拼接的字符串、字符集合），最大长度也是 26，属于常数级别。  
    - 因此空间复杂度是 **O(1)**（不随 `n` 增长）。

#### 代码（Python）

```python
from typing import List

def maxLength_bruteforce(arr: List[str]) -> int:
    n = len(arr)
    best = 0                       # 记录目前找到的最大合法长度

    # 用 0/1 位掩码枚举所有子序列，mask 的第 i 位表示是否取 arr[i]
    for mask in range(1 << n):     # 1 << n 等价于 2**n
        chars = set()              # 用集合记录已经出现的字符
        ok = True                  # 标记当前组合是否合法
        total_len = 0

        for i in range(n):
            if mask >> i & 1:      # 第 i 位为 1，说明要取 arr[i]
                for ch in arr[i]:
                    if ch in chars:   # 出现重复字符
                        ok = False
                        break
                    chars.add(ch)
                if not ok:            # 发现冲突，直接放弃后面的检查
                    break
                total_len += len(arr[i])

        if ok:                     # 只在合法的情况下更新答案
            best = max(best, total_len)

    return best
```

#### 复杂度

- **时间复杂度**：`O(2ⁿ·L)`，其中 `n = len(arr) ≤ 16`，`L ≤ 26`。  
  用大白话说，就是“每增加一个字符串，可能的组合数会翻倍”。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量。

---

### 2. 最优解

#### 思路  

暴力解已经可以跑通，但我们可以把“检查是否有重复字符”的过程做得更高效，同时省去每次都拼接字符串的开销。**关键点**是：

1. **把每个字符串转换成 26 位的二进制掩码**  
   - 英文字母只有 26 个，使用一个整数的 26 个二进制位来表示字符集合。  
   - 第 `k` 位为 1 表示字符 `'a' + k` 出现在该字符串中。  
   - 这就像“每个字母都有自己的编号卡片，放进一个盒子里，用卡片的编号对应的格子是否有卡片来记”。  
   - 同时，如果一个字符串内部已经有重复字符（例如 `"aa"`），它本身就是非法的，直接丢掉。

2. **使用回溯（Backtracking）或深度优先搜索**  
   - 从左到右遍历 `arr`，维护 **当前已经选中的字符掩码** `mask_cur`。  
   - 对每个字符串的掩码 `mask_i`：  
     - 若 `mask_cur & mask_i != 0`，说明两者有公共字符，**不能一起使用**，直接跳过。  
     - 否则，可以把它加入当前组合：`mask_cur | mask_i`，并继续递归处理后面的字符串。  
   - 在递归的每一步，记录当前组合的字符数（即 `mask_cur` 中 1 的个数），更新全局最大值。

3. **为什么快**  
   - **位运算**是 O(1) 的常数时间：判断是否有交集、合并集合都只需要几条机器指令。  
   - **剪枝**：一旦发现冲突，就不必继续往下尝试该分支，直接返回，省掉大量不必要的组合。  
   - 由于 `n ≤ 16`，回溯的搜索树最多有 `2ⁿ` 个叶子，但每一步的检查都非常轻量，整体运行非常快。

4. **可选的 DP 思路**（这里不展开实现）  
   - 维护一个列表 `dp`，其中每个元素是已经得到的合法字符掩码。遍历每个字符串的掩码 `mask_i`，尝试把它和 `dp` 中的每个掩码合并，若不冲突则加入新的掩码。最后遍历 `dp` 找到最大位数即可。该思路本质上是**宽度优先的动态规划**，与回溯思路等价。

下面给出 **回溯 + 位掩码** 的实现，代码中每行都配有中文注释，帮助初学者理解。

#### 代码（Python）

```python
from typing import List

def maxLength(arr: List[str]) -> int:
    """
    回溯 + 位掩码
    返回可拼接的最长唯一字符子串的长度
    """
    # 1️⃣ 把每个字符串转成 26 位掩码，同时过滤掉内部有重复字符的串
    masks = []                # 有效字符串对应的位掩码列表
    for s in arr:
        mask = 0
        duplicate = False
        for ch in s:
            bit = 1 << (ord(ch) - ord('a'))   # 对应字符的二进制位
            if mask & bit:                    # 已经出现过该字符，说明 s 本身有重复
                duplicate = True
                break
            mask |= bit                       # 把该字符对应的位设为 1
        if not duplicate:                     # 只保留没有内部重复的字符串
            masks.append(mask)

    # 2️⃣ 深度优先搜索（回溯）
    best = 0                                   # 全局最大长度

    def dfs(pos: int, cur_mask: int) -> None:
        """
        pos: 当前考虑的字符串在 masks 中的下标
        cur_mask: 已经选中的字符集合（位掩码）
        """
        nonlocal best
        # 统计当前掩码中有多少个 1，即已经得到的字符数
        # bin(x).count('1') 把整数转成二进制字符串，再统计 '1' 的个数
        best = max(best, bin(cur_mask).count('1'))

        # 遍历剩余的字符串，尝试把它们加入当前组合
        for i in range(pos, len(masks)):
            if cur_mask & masks[i]:            # 与已有字符有交集，不能选
                continue
            # 选取 masks[i]，递归进入下一层
            dfs(i + 1, cur_mask | masks[i])

    dfs(0, 0)          # 从第 0 个字符串、空字符集合开始搜索
    return best
```

#### 复杂度

- **时间复杂度**：`O(2ⁿ)`（最坏情况下仍遍历所有子集），但每次判断冲突、合并集合都是 **O(1)** 的位运算。相比暴力解省去了拼接字符串和集合检查的开销。  
  - 用大白话说，就是“虽然组合数仍然是指数级，但每一步的工作量非常轻——像是只动了几个开关”。  

- **空间复杂度**：`O(n)`，递归栈的深度最多是 `n`（≤16），再加上保存的掩码列表 `masks`（最多 `n` 个整数），均为线性空间。  

---

## 心得

- **核心技巧**：**位掩码 + 回溯（或 DP）**。把字符集合压缩到 26 位整数里，使得“是否有重复”可以用一次 `&`（位与）判断，合并集合用一次 `|`（位或）完成。  
- **适用的题型**  
  1. “把若干子集组合，使得元素不冲突”——如 *Maximum Length of a Concatenated String with Unique Characters*（本题）。  
  2. “集合覆盖/不相交子集”——例如 *Partition to K Equal Sum Subsets*（把数组分成不相交的子集）。  
  3. “状态压缩 DP”——如 *Travelling Salesman Problem* 的简化版，或 *Maximum Subset XOR*。  
- **一句话总结解题钥匙**：**把“字符是否出现”用位掩码表达，利用位运算快速检测冲突，再配合回溯/DP 完成枚举**。

---

## 反思

- **拿到题目第一反应**：直接想到枚举所有子序列，然后检查字符唯一性。  
- **最容易踩的坑**  
  1. **字符串内部有重复字符**：如果不先过滤，会导致后续位掩码冲突检测失效。  
  2. **位掩码溢出**：在 Python 中整数位数不受限制，但要确保只用低 26 位；使用 `1 << (ord(ch) - ord('a'))` 可以避免错误。  
  3. **递归深度**：虽然 `n ≤ 16`，递归不会爆栈，但仍需注意基准情况（空集合）要能返回。  
- **下次遇到同类题的第一步**：**把每个元素（字符串、数字集合等）转换成位掩码**，并**先剔除内部冲突的元素**，这样后面的搜索或 DP 能够在 O(1) 时间内判断是否可以合并。