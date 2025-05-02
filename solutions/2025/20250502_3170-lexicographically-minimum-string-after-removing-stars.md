# #3170. 删除星号后的字典序最小字符串 / Lexicographically Minimum String After Removing Stars

> 难度：中等 · 标签：Hash Table、String、Stack、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/lexicographically-minimum-string-after-removing-stars/)

---

## 题目（英文原版）

**Description**

You are given a string s. It may contain any number of '*' characters. Your task is to remove all '*' characters.
While there is a '*', do the following operation:
Return the lexicographically smallest resulting string after removing all '*' characters.

**Examples**

**Example 1:**

```
Input: s = "aaba*"
Output: "aab"
Explanation:
We should delete one of the 'a' characters with '*' . If we choose s[3] , s becomes the lexicographically smallest.
```

**Example 2:**

```
Input: s = "abc"
Output: "abc"
Explanation:
There is no '*' in the string.
```

**Constraints**

- 1 <= s.length <= 105
- s consists only of lowercase English letters and '*'.
- The input is generated such that it is possible to delete all '*' characters.

---

## 题目（中文翻译）

给定一个字符串 `s`。其中可能包含任意数量的 `'*'` 字符。你的任务是删除所有的 `'*'`。

当字符串中仍存在 `'*'` 时，重复执行以下操作（具体操作细节在题目中省略）：

返回在删除所有 `'*'` 之后，能够得到的字典序最小（lexicographically smallest）的字符串。

## 示例

### 示例 1
**输入**  
` s = "aaba*"`  

**输出**  
`"aab"`  

**解释**  
我们应该将 `'*'` 所在位置对应的一个 `'a'` 字符一起删除。如果选择删除下标为 `3` 的字符，则得到的字符串是字典序最小的。

### 示例 2
**输入**  
` s = "abc"`  

**输出**  
`"abc"`  

**解释**  
字符串中不存在 `'*'`，无需进行任何操作。

## 约束条件
- `1 <= s.length <= 10^5`
- `s` 仅由小写英文字母和 `'*'` 组成。
- 输入保证一定可以删除掉所有的 `'*'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举每一颗 `*` 要删掉哪个字母**，把所有 `*` 都删掉后，比较得到的所有字符串，挑出字典序最小的那个。  
- **数据结构**：可以把字符串看成一本字典，字母是“词”，下标是“页码”。我们把每颗 `*` 当成“删词卡”，要决定把哪一页的词删掉。  
- **为什么正确**：只要把每颗 `*` 对应的删词卡都选好，剩下的字母顺序不变，得到的字符串就是一种合法答案。遍历所有可能的选法自然能找到最小的。  

但是这一步的搜索空间非常大。设字符串长度为 `n`，`*` 的个数为 `k`（`k ≤ n`），每颗 `*` 可以删 `n‑k` 个字母中的任意一个，组合数大约是  

```
C(n‑k, k)  ≈  (n‑k)^k   (指数级)
```

随着 `n` 增大，根本不可能在合理时间内穷举。

#### 代码（Python）

```python
import itertools

def brute(s: str) -> str:
    stars = [i for i, ch in enumerate(s) if ch == '*']
    letters = [i for i, ch in enumerate(s) if ch != '*']
    k = len(stars)

    best = None
    # 枚举所有把 k 颗星对应到 letters 上的方式（组合）
    for del_idx in itertools.combinations(letters, k):
        del_set = set(del_idx)          # 被删掉的字母下标集合
        res = []
        for i, ch in enumerate(s):
            if ch == '*':               # 星号本身必须被删
                continue
            if i in del_set:            # 被星号删掉的字母也跳过
                continue
            res.append(ch)
        cand = ''.join(res)
        if best is None or cand < best:   # 字典序比较
            best = cand
    return best
```

> **注意**：上面的代码只适合非常小的测试用例，`itertools.combinations` 会在 `k` 较大时爆炸。

#### 复杂度

- **时间复杂度**：`O( C(n‑k, k) * n )`，指数级，几乎不可能在 `n ≤ 10⁵` 时通过。  
- **空间复杂度**：`O(n)`，用于保存临时字符串。

---

### 2. 最优解

#### 思路  

从暴力解可以看出：**我们只需要删掉恰好 `k` 个字母（`k` 为 `*` 的个数），其余字母保持原顺序**。这正是「在一个字符串中删除固定数量的字符，使结果字典序最小」的经典问题。

**瓶颈**  
- 暴力枚举每颗 `*` 对应的删除位置，组合数太大。  
- 需要一种一次遍历就能决定哪些字符该删、哪些该留下。

**关键观察**  
- 为了让最终字符串尽可能小，**应该尽量把大的字符删掉**，尤其是出现在前面的位置，因为前面的字符对字典序的影响最大。  
- 当我们从左到右扫描时，若当前字符 `c` 比栈顶字符（已经保留下来的最近一个字符）更小，那么把栈顶字符删掉会让前缀变小，显然是有利的。于是我们可以**用一个单调递增的栈**来维护已经保留的字符。  

**算法步骤**  

1. 先统计 `k = s.count('*')`，这就是我们必须删除的字母数量。  
2. 用一个列表 `stack` 当作栈，遍历字符串中的每个字符 `ch`  
   - 如果 `ch` 是 `'*'`，直接跳过（星号本身不进入结果，也不消耗额外的删除次数）。  
   - 否则 `ch` 是字母。**只要还有删除配额 (`k > 0`) 且栈不空且栈顶字符 > `ch`**，就把栈顶弹出（等价于用一颗星删掉这个更大的字符），`k -= 1`。  
   - 把 `ch` 压入栈中。  
3. 循环结束后，可能还有剩余的删除配额（比如字符串整体是递增的），这时只能把栈尾的字符删掉——**从栈顶弹出 `k` 次**。  
4. 栈中剩余的字符即为字典序最小的答案，按顺序拼接成字符串返回。

**为什么正确**（从零解释）  
- **单调栈的作用**：栈始终保持递增（从栈底到栈顶），这保证了在任意时刻，栈顶是当前保留字符中最大的。若后面出现一个更小的字符 `c`，把这个最大的字符删掉可以让前缀字典序更小，而不影响已经确定的更小字符的相对顺序。  
- **贪心的合法性**：我们每次只在**还能删除**的前提下，删除当前能删除的最大字符。若以后还有更小的字符出现，后面的删除操作同样会遵循同样的规则；因此不存在因为“早早删掉”而错失更好方案的情况。  
- **完整性**：我们恰好删掉了 `k` 个字母（每次弹栈一次计一次），且所有未被删除的字符仍保持原来的左→右顺序，满足题目要求。  

**类比**：想象手里有一串编号的球（字母），每看到一个更小编号的球，就把手中最大编号的球扔掉，最多扔 `k` 次，最后手里留下的球顺序就是最小的排列。

#### 代码（Python）

```python
def smallestStringAfterRemovingStars(s: str) -> str:
    # 1️⃣ 统计需要删除的字母个数
    deletions = s.count('*')          # 必须删掉的字母数量

    stack = []                        # 用来维护已经保留下来的字符（单调递增）

    # 2️⃣ 遍历字符串
    for ch in s:
        if ch == '*':                 # 星号本身直接跳过
            continue

        # 当还有删字符的配额，且栈顶字符比当前字符大时，弹出栈顶（相当于用一颗星删掉它）
        while deletions > 0 and stack and stack[-1] > ch:
            stack.pop()
            deletions -= 1

        stack.append(ch)              # 把当前字符压入栈中

    # 3️⃣ 如果仍有剩余的删除次数，直接从栈尾（最右边）删除
    if deletions:
        stack = stack[:-deletions]    # 切片相当于弹出 deletions 次

    # 4️⃣ 合并成答案
    return ''.join(stack)
```

> **代码要点**  
> - `while deletions > 0 and stack and stack[-1] > ch:` 这行是核心，确保栈保持递增。  
> - `stack = stack[:-deletions]` 只在 `deletions` 仍大于 0 时执行，等价于弹出栈顶 `deletions` 次。  
> - 整个过程只遍历一次字符串，时间线性。

#### 复杂度

- **时间复杂度**：`O(n)`，每个字符最多进栈一次、出栈一次，`n` 为字符串长度（`≤ 10⁵`）。  
  - 与暴力解的 `O(C(n‑k, k)·n)` 相比，线性时间是可以接受的。  
- **空间复杂度**：`O(n)`，最坏情况下栈会保存除 `*` 之外的所有字符。  
  - 只需要额外的线性空间，符合题目限制。

---

## 心得

- **核心技巧**：**单调栈 + 贪心删除**——在需要删除固定数量字符以获得字典序最小的场景下，这是一套通用套路。  
- **适用题型**（类似思路）  
  1. *Remove K Digits*（把数字字符串删掉 K 位，使剩余数最小）  
  2. *Lexicographically Smallest Subsequence of Distinct Characters*（在保持相对顺序的前提下，删除字符得到最小子序列）  
  3. *Smallest Substring of Length K*（在滑动窗口里保持单调结构）  
- **一句话总结**：**“想让前缀尽可能小，就把当前出现的更小字符前面的最大字符删掉”。**

---

## 反思

- **第一反应**：看到 `*`，立刻想到“把它左边的字符删掉”，于是想把每颗星对应的删除位置枚举。  
- **最容易踩的坑**  
  - 误以为每颗 `*` 只能删左边紧邻的字符，导致答案错误。  
  - 忽视了“删除的字符数量必须等于 `*` 的数量”，如果删除不足或超出都会不合法。  
  - 处理完所有字符后忘记把剩余的删除次数从栈尾剔除。  
- **下次类似题**：先把问题抽象为“**在保持相对顺序的前提下，删除固定数量的字符**”，然后考虑 **单调栈** 或 **贪心** 的方式一次遍历完成。这样往往能把指数级搜索压到线性时间。