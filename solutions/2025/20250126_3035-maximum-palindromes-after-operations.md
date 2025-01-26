# #3035. **操作后最大回文数** / Maximum Palindromes After Operations

> 难度：中等 · 标签：Array、Hash Table、String、Greedy、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/maximum-palindromes-after-operations/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string array words having length n and containing 0-indexed strings.
You are allowed to perform the following operation any number of times (including zero):
Return an integer denoting the maximum number of palindromes words can contain, after performing some operations.
Note: i and j may be equal during an operation.

**Examples**

**Example 1:**

```
Input: words = ["abbb","ba","aa"]
Output: 3
Explanation: In this example, one way to get the maximum number of palindromes is:
Choose i = 0, j = 1, x = 0, y = 0, so we swap words[0][0] and words[1][0]. words becomes ["bbbb","aa","aa"].
All strings in words are now palindromes.
Hence, the maximum number of palindromes achievable is 3.
```

**Example 2:**

```
Input: words = ["abc","ab"]
Output: 2
Explanation: In this example, one way to get the maximum number of palindromes is: 
Choose i = 0, j = 1, x = 1, y = 0, so we swap words[0][1] and words[1][0]. words becomes ["aac","bb"].
Choose i = 0, j = 0, x = 1, y = 2, so we swap words[0][1] and words[0][2]. words becomes ["aca","bb"].
Both strings are now palindromes.
Hence, the maximum number of palindromes achievable is 2.
```

**Example 3:**

```
Input: words = ["cd","ef","a"]
Output: 1
Explanation: In this example, there is no need to perform any operation.
There is one palindrome in words "a".
It can be shown that it is not possible to get more than one palindrome after any number of operations.
Hence, the answer is 1.
```

**Constraints**

- 1 <= words.length <= 1000
- 1 <= words[i].length <= 100
- words[i] consists only of lowercase English letters.

---

## 题目（中文翻译）

你得到一个下标从 0 开始的字符串数组 `words`，长度为 `n`，其中每个元素也是下标从 0 开始的字符串。  
你可以任意次数（包括 0 次）执行以下操作：

> 任选整数 `i`、`j`（`0 ≤ i, j < n`），以及整数 `x`、`y`，其中 `x` 是 `words[i]` 的合法下标，`y` 是 `words[j]` 的合法下标。交换字符 `words[i][x]` 与 `words[j][y]`。

在任意次数的操作后，返回 `words` 中能够成为回文串（palindrome）的字符串的最大数量。  
**注意**：在一次操作中，`i` 与 `j` 可以相等。

---

### 示例

**示例 1**

```text
Input: words = ["abbb","ba","aa"]
Output: 3
Explanation: 本例中，一种实现最大回文数的方法如下：
- 选择 `i = 0, j = 1, x = 0, y = 0`，交换 `words[0][0]` 与 `words[1][0]`，得到 ["bbbb","aa","aa"]。
此时 `words` 中的所有字符串都是回文串。因此能够得到的最大回文数为 3。
```

**示例 2**

```text
Input: words = ["abc","ab"]
Output: 2
Explanation: 本例中，一种实现最大回文数的方法如下：
- 选择 `i = 0, j = 1, x = 1, y = 0`，交换 `words[0][1]` 与 `words[1][0]`，得到 ["aac","bb"]。
- 选择 `i = 0, j = 0, x = 1, y = 2`，交换 `words[0][1]` 与 `words[0][2]`，得到 ["aca","bb"]。
此时两个字符串均为回文串，最大回文数为 2。
```

**示例 3**

```text
Input: words = ["cd","ef","a"]
Output: 1
Explanation: 本例中无需进行任何操作。
`words` 中仅有字符串 "a" 是回文串。可以证明，无论进行多少次操作，都不可能得到多于一个的回文串。
因此答案为 1。
```

---

### 约束条件

- `1 <= words.length <= 1000`
- `1 <= words[i].length <= 100`
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的字符交换都穷举一遍**，看能得到多少个回文字符串。  
可以把每个字符想象成一张“字母卡片”，每次交换就是把兩張卡片換位置。  
如果把所有卡片重新发放到各个单词里（保持每个单词的长度不变），就等价于**把所有字符重新排列**。  
于是暴力做法就是：

1. 统计所有字符出现的次数（相当于把所有卡片放进一个大抽屉）。  
2. **枚举**每一种可能的把这些卡片分配到每个单词中的方式（每个单词的长度固定）。  
3. 对每个分配，检查每个单词是否是回文，计数后取最大值。

> **为什么这种方法是正确的？**  
> 因为我们遍历了所有合法的字符分配方案，答案必然出现在其中。

> **复杂度有多糟？**  
> 假设总字符数为 `S = sum(len(words[i]))`，每个字符可以放到 `n` 个单词的任意位置。  
> 那么可能的分配方式大约是 `n^S`，这在实际数据（`n ≤ 1000，S ≤ 100 000`）下根本不可行。  
> 用大白话说，就是“指数级别的时间”，几乎不可能在电脑上跑完。

#### 代码（Python）

```python
from collections import Counter
import itertools

def brute_max_palindromes(words):
    """
    只用于非常小的测试用例（比如 n <= 3, 每个单词长度 <= 3）。
    完全暴力枚举所有字符的重新分配方式。
    """
    n = len(words)
    lens = [len(w) for w in words]          # 每个单词的长度
    total_chars = list(''.join(words))      # 所有字符放进一个大列表
    best = 0

    # 生成所有可能的分配：把 total_chars 按顺序切分成 n 段，每段长度等于对应单词的长度
    # itertools.permutations 会遍历所有字符排列，随后再切分
    for perm in set(itertools.permutations(total_chars)):
        idx = 0
        cnt = 0
        for l in lens:
            cur = perm[idx: idx + l]        # 取出当前单词的字符序列
            idx += l
            # 判断是否回文
            if cur == cur[::-1]:
                cnt += 1
        best = max(best, cnt)
    return best

# 示例（仅能跑极小规模）：
# print(brute_max_palindromes(["ab","ba"]))   # 输出 2
```

> **关键行注释**  
> - `itertools.permutations(total_chars)`：把所有字符全排列，相当于把卡片全部重新排队。  
> - `cur == cur[::-1]`：检查当前单词是否正读和倒读相同，即回文。

#### 复杂度  

- **时间复杂度**：`O(n^S * S)`（指数级），因为我们要遍历所有可能的字符排列。  
  - 用大白话说，就是“每多一个字符，就要把所有可能的排列数翻 N 倍”，几乎不可能完成。  
- **空间复杂度**：`O(S)`，需要存放所有字符的列表和一次排列的临时结果。

> 结论：暴力解只能用来验证思路或跑极小的测试，实际求解必须寻找更聪明的办法。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**真正决定能否构成回文的不是字符的具体顺序，而是字符的“配对”数量**。  
回文的核心要求：

- 对于长度为 `L` 的单词，需要 `⌊L/2⌋` 对相同字符放在左右对称位置。  
- 如果 `L` 为奇数，还需要一个“中心字符”，这可以是任何剩余的单个字符（不需要配对）。

所以我们把所有字符看成 **“配对的资源”**，每对资源可以帮助我们完成一个对称位置。

**关键观察**  

1. **总配对数**  
   统计所有字符出现次数 `freq[ch]`，每两个相同字符可以组成一对。  
   ```
   total_pairs = sum(freq[ch] // 2 for ch in 'a'..'z')
   ```
   把这一步想象成把所有字母卡片先两两配好，剩下的单张卡片放在抽屉里备用。

2. **先处理短的单词**  
   为了让配对尽可能多地被利用，我们**优先让短的单词成为回文**。  
   - 短单词需要的配对少，花费的资源少，能够让更多单词达成回文。  
   - 这类似“先喂小孩子，再喂大孩子”，能让整体满足度最大。

3. **贪心过程**  
   - 把所有单词的长度从小到大排序。  
   - 依次检查第 `i` 个单词：如果 `total_pairs >= len_i // 2`，就把它变成回文，`total_pairs -= len_i // 2`，答案 `ans += 1`。  
   - 否则资源不够，后面的更长单词更不可能满足，直接结束。

4. **奇数长度的中心字符**  
   - 当我们把配对用完后，可能还有一些单独的字符（`freq[ch] % 2`），这些可以随意放在奇数长度单词的中间。  
   - 只要我们已经确保左右配对成功，中心字符的选择不影响回文性质。

**为什么贪心是最优的？**  

- 每个配对只能被用在 **某个单词的左/右对称位置**，没有别的用处。  
- 把配对分配给更短的单词，等价于用更少的配对“换取”一个回文，**单位配对的收益最高**。  
- 若我们把配对给了一个更长的单词，必然会消耗更多配对，却只得到同样的“+1”回文计数，**效率更低**。  
- 因此，按长度升序贪心分配必然得到最大可能的回文数量。

> **类比**：想象你有若干对鞋子（配对），要给孩子们穿鞋。每个孩子的脚大小不同，需要的鞋子数量不同。为了让最多的孩子都有鞋子，你应该先给脚小的孩子配鞋——因为他们只需要一双，能让更多孩子满足需求。

#### 代码（Python）

```python
from collections import Counter

def max_palindromes(words):
    """
    最优解：贪心 + 统计配对数
    时间 O(N log N + 26) ，空间 O(1)（只需要 26 个字母的计数）
    """
    # 1. 统计所有字符出现次数
    freq = Counter(''.join(words))          # 把所有单词连起来再计数
    # 2. 计算总配对数（每两个相同字符是一对）
    total_pairs = sum(v // 2 for v in freq.values())

    # 3. 按单词长度从小到大排序
    lengths = sorted(len(w) for w in words)

    ans = 0
    for L in lengths:
        need = L // 2                # 这个单词需要多少对字符
        if total_pairs >= need:      # 资源够，就把它变成回文
            total_pairs -= need
            ans += 1
        else:                        # 资源不够，后面的更长单词更不可能满足，直接结束
            break
    return ans

# ---------- 示例 ----------
if __name__ == "__main__":
    print(max_palindromes(["abbb","ba","aa"]))        # 3
    print(max_palindromes(["abc","ab"]))              # 2
    print(max_palindromes(["cd","ef","a"]))           # 1
```

> **关键行注释**  
> - `Counter(''.join(words))`：把所有字母卡片放进一个大抽屉里，统计每种字母的数量。  
> - `total_pairs = sum(v // 2 ...)`：把卡片两两配对，得到“配对资源”。  
> - `need = L // 2`：当前单词需要多少对配对才能左右对称。  
> - `if total_pairs >= need:`：如果资源足够，就把它变成回文并扣除对应配对。

#### 复杂度  

- **时间复杂度**：`O(N log N + 26)`  
  - `N` 为单词数。排序长度数组需要 `O(N log N)`，统计字符频率只遍历一次所有字符，最多 `26` 种字母，常数级。  
  - 用大白话说，就是“先把单词排队（花点时间），再一次性算配对，整个过程很快”。  
- **空间复杂度**：`O(1)`（不算输入本身）  
  - 只用了一个大小为 26 的计数数组（或 `Counter`），与 `N`、单词总长度无关。

> 与暴力解相比，时间从指数级骤降到几乎线性，能够轻松处理题目给出的上限（`n ≤ 1000，单词长度 ≤ 100`）。

---

## 心得

- **核心技巧**：把所有字符视作可以自由重新分配的资源，只关注“配对数”。  
- **适用题型**：  
  1. **字符重排后要求回文**（如 LeetCode 2121 *Maximum Possible Palindromes After Operations*）。  
  2. **需要把字符均匀分配到若干容器**（如 “分配字符使每个字符串都是回文”）。  
  3. **贪心处理资源分配的最小化/最大化**（如 “最少硬币换零钱” 类似思路）。  
- **一句话总结解题钥匙**：**先把所有字符配对，按单词长度从短到长一次消耗配对**。

---

## 反思

- **第一反应**：看到可以任意交换字符，就想到“所有字符可以自由重排”，于是把问题转化为“资源分配”。  
- **最容易踩的坑**：  
  - 忘记奇数长度单词只需要配对数 `len//2`，中间的单字符可以随意使用。  
  - 误以为需要考虑字符种类之间的匹配，实际上只要配对数量足够即可。  
- **下次类似题的第一步**：  
  - **统计全局资源（如字符频率、配对数）**，再判断每个子结构（单词、区间）需要多少资源，最后用**贪心**或**二分**决定可行的最大数量。