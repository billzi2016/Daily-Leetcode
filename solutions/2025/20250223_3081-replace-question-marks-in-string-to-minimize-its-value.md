# #3081. 替换字符串中的问号以最小化其值 / Replace Question Marks in String to Minimize Its Value

> 难度：中等 · 标签：Hash Table、String、Greedy、Sorting、Heap (Priority Queue)、Counting · [LeetCode 链接](https://leetcode.com/problems/replace-question-marks-in-string-to-minimize-its-value/)

---

## 题目（英文原版）

**Description**

You are given a string s. s[i] is either a lowercase English letter or '?'.
For a string t having length m containing only lowercase English letters, we define the function cost(i) for an index i as the number of characters equal to t[i] that appeared before it, i.e. in the range [0, i - 1].
The value of t is the sum of cost(i) for all indices i.
For example, for the string t = "aab":
Your task is to replace all occurrences of '?' in s with any lowercase English letter so that the value of s is minimized.
Return a string denoting the modified string with replaced occurrences of '?'. If there are multiple strings resulting in the minimum value, return the lexicographically smallest one.

**Examples**

**Example 1:**

```
Input: s = "???"
Output: "abc"
Explanation: In this example, we can replace the occurrences of '?' to make s equal to "abc" .
For "abc" , cost(0) = 0 , cost(1) = 0 , and cost(2) = 0 .
The value of "abc" is 0 .
Some other modifications of s that have a value of 0 are "cba" , "abz" , and, "hey" .
Among all of them, we choose the lexicographically smallest.
```

**Example 2:**

```
Input: s = "a?a?"
Output: "abac"
Explanation: In this example, the occurrences of '?' can be replaced to make s equal to "abac" .
For "abac" , cost(0) = 0 , cost(1) = 0 , cost(2) = 1 , and cost(3) = 0 .
The value of "abac" is 1 .
```

**Constraints**

- 1 <= s.length <= 105
- s[i] is either a lowercase English letter or '?'.

---

## 题目（中文翻译）

给定一个字符串 `s`，其中 `s[i]` 要么是小写英文字母，要么是字符 `'?'`。  
对于仅包含小写英文字母、长度为 `m` 的字符串 `t`，我们定义函数 **cost(i)**（下标 `i` 的代价）为在索引 `i` 之前（即区间 `[0, i‑1]`）出现的、与 `t[i]` 相同的字符个数。  
字符串 `t` 的 **value**（值）是所有下标 `i` 的 `cost(i)` 之和。

你的任务是将 `s` 中所有 `'?'` 替换成任意小写英文字母，使得替换后的 `s` 的值最小。  
返回替换后的字符串。如果有多个最小值对应的字符串，返回 **字典序（lexicographically）最小** 的那个。

---

### 示例

#### 示例 1
``` 
Input: s = "???"
Output: "abc"
```
**解释**：我们可以将 `'?'` 替换成 `"abc"`。  
对于 `"abc"`，`cost(0) = 0`，`cost(1) = 0`，`cost(2) = 0`，因此值为 `0`。  
其他值也为 `0` 的修改如 `"cba"`、`"abz"`、`"hey"` 等，但 `"abc"` 在它们之中字典序最小。

#### 示例 2
``` 
Input: s = "a?a?"
Output: "abac"
```
**解释**：将 `'?'` 替换后得到 `"abac"`。  
`cost(0) = 0`，`cost(1) = 0`，`cost(2) = 1`（因为在位置 2 前已有一个 `'a'`），`cost(3) = 0`，所以值为 `1`。

---

### 约束条件
- `1 <= s.length <= 10^5`
- `s[i]` 要么是小写英文字母，要么是字符 `'?'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个 `'?'` 都尝试所有 26 种小写字母，得到所有可能的完整字符串，然后逐个计算它们的 **value**（题目里定义的“价值”），挑出最小的那一个。如果出现多个价值相同的字符串，再在这些字符串里挑字典序最小的。

> **类比**：把 `'?'` 想成一本书里缺失的字，暴力解相当于把每个缺页的每一页都换成 A、B、…、Z 这 26 种可能，最后把所有写好的书全部读一遍，算出每本书的“分数”，选出分数最低、字典序最前的那本。

**为什么它是正确的？**  
因为我们枚举了**所有**合法的填法，最小的价值一定会在枚举集合里出现，字典序最小的也一定会在价值相同的子集合里出现。

**复杂度**  
- 假设字符串里有 `k` 个 `'?'`，每个 `'?'` 有 26 种选择，那么一共有 `26^k` 种填法。  
- 对每一种填法，需要遍历一次完整字符串（长度 `n`）来统计每个字符出现的次数并计算价值。  

> **时间复杂度**：`O(26^k * n)`  
> 这里的 `O` 符号可以理解为“随着 `k` 增大，耗时会像 26 的 `k` 次方一样快速增长”。即使 `k = 5`，也已经是 `~12,000,000` 次运算，远远超出 10⁵ 规模的限制。  

> **空间复杂度**：`O(n)`（保存当前构造的完整字符串），这在本题不是瓶颈。

显然，这种“全排列”方式在 `k` 较大时根本不可行，必须找出更聪明的做法。

---

### 2. 最优解

#### 思路  

从暴力解可以看到：**价值只和每个字母出现的次数有关**，与它们在字符串中的相对顺序无关。  

> **关键观察 1**：  
> 如果某个字符 `c` 出现了 `x` 次，那么它为整个字符串贡献的价值是  
> `0 + 1 + 2 + … + (x‑1) = x·(x‑1)/2`。  
> 这就是等差数列求和公式，直观上可以把它想成“第 1 次出现免费，第 2 次出现要付 1 元，第 3 次出现要付 2 元…”。

> **关键观察 2**：  
> 为了让总价值最小，我们希望 **所有字符的出现次数尽可能均匀**，因为 `x·(x‑1)/2` 随 `x` 增大而呈二次增长。  
> 因此，每当我们要给一个 `'?'` 选字母时，应该把它分配给当前出现次数 **最少** 的字母。

> **关键观察 3**（字典序）：  
> 如果有多个字母的出现次数相同且都是最少的，为了让最终字符串在字典序上最小，我们应当优先使用字母表中靠前的那个（`'a'` < `'b'` < …）。

综合以上三点，得到如下贪心策略：

1. **统计已有字符的出现次数**（长度为 26 的数组 `cnt[0..25]`）。  
2. **维护一个最小堆**（优先队列），堆中存 `(出现次数, 字符)`，堆顶始终是出现次数最少且字典序最小的字符。  
3. 从左到右遍历原字符串 `s`：  
   - 如果当前位置是普通字母，直接写入答案。  
   - 如果是 `'?'`，从堆里弹出堆顶 `(c, ch)`，把 `ch` 写入答案，然后把 `c+1` 再推回堆（因为我们刚刚多用了一个 `ch`）。  

这样每次都把 `'?'` 填成当前**最少出现**的字母，保证价值最小；在出现次数相同的情况下，堆的次序保证我们选字母表中更小的那个，从而得到字典序最小的答案。

> **为什么这一步一步的贪心是全局最优的？**  
> 价值函数是 **凸函数**（`x·(x‑1)/2` 随 `x` 增大而加速），把一个 “额外的出现次数” 分配给出现次数最小的字符，总价值的增量是最小的。由于每一步的增量最小，累计起来的总价值也最小。  
> 这正是 **“把最小的代价放在最先处理”** 的典型贪心证明思路。

#### 代码（Python）

```python
import heapq

def replaceQuestionMarks(s: str) -> str:
    # 1️⃣ 统计已有字符的频次，cnt[0] 对应 'a', cnt[25] 对应 'z'
    cnt = [0] * 26
    for ch in s:
        if ch != '?':
            cnt[ord(ch) - ord('a')] += 1

    # 2️⃣ 构造最小堆，堆元素为 (出现次数, 字符索引)
    #    Python 的 heapq 默认按元组第一个元素升序，如果相同再比较第二个元素
    heap = [(cnt[i], i) for i in range(26)]
    heapq.heapify(heap)

    # 3️⃣ 逐字符构造答案
    ans = []
    for ch in s:
        if ch != '?':
            # 普通字符直接保留
            ans.append(ch)
        else:
            # 弹出出现次数最少且字典序最小的字符
            freq, idx = heapq.heappop(heap)
            # 用这个字符填补 '?'
            new_char = chr(ord('a') + idx)
            ans.append(new_char)
            # 该字符出现次数加一，再放回堆中
            heapq.heappush(heap, (freq + 1, idx))

    return ''.join(ans)


# ------------------- 示例 -------------------
if __name__ == "__main__":
    print(replaceQuestionMarks("???"))      # abc
    print(replaceQuestionMarks("a?a?"))    # abac
```

**代码要点注释**  

| 行号 | 解释 |
|------|------|
| 4‑6  | 用一个长度为 26 的列表 `cnt` 统计每个已有字母出现了多少次。 |
| 9‑11 | 把每个字母的 `(出现次数, 字母索引)` 放进最小堆。堆顶就是当前出现次数最少、且字母表顺序最前的字母。 |
| 15‑22| 遍历原字符串。遇到 `'?'` 时，从堆里取出最合适的字母，写进答案，并把它的计数加一再放回堆。 |
| 24‑27| 简单的自测代码，验证示例输出是否正确。 |

#### 复杂度  

- **时间复杂度**：`O(n log 26)`，其中 `n = len(s)`。  
  - `log 26` 是因为堆的大小始终是 26（固定的字母表大小），可以视作常数，所以整体是线性 `O(n)`。  
  - 与暴力解 `O(26^k * n)` 相比，**只和字符串长度成正比**，即使 `n=10⁵` 也轻松跑完。

- **空间复杂度**：`O(1)`（除了输入输出外，只用了长度为 26 的数组和堆，都是常数级别的额外空间）。

---

## 心得

- **核心技巧**：利用 **出现次数的均衡**（最小化二次函数） + **最小堆**（快速获取当前最少出现的字符）完成贪心分配。  
- **适用场景**  
  1. 需要把若干“资源”（这里是 `'?'`）分配给若干“类别”，使得每类的负担（出现次数）尽可能均匀，例如 “最小化最大负载” 类题。  
  2. “在保持某种全局最优（最小价值）的前提下，还要满足字典序最小” 的字符串构造题。  
- **一句话总结**：把每个 `'?'` 分配给当前出现次数最少、字典序最小的字母，即可同时最小化价值和字典序。

---

## 反思

- **第一反应**：看到“价值只跟每个字符出现次数有关”，立刻想到统计频次、把 `'?'` 均匀分配。  
- **最容易踩的坑**  
  - 忘记在出现次数相同的情况下，还要考虑字典序，导致得到的答案不是最小的。  
  - 在实现时直接用 `sorted` 或遍历 26 次寻找最小频次，时间会变成 `O(26·n)`，虽然也能接受，但使用堆可以写出更简洁、自然的代码。  
- **下次遇到同类题**：第一步先**把价值函数写成只和频次有关的形式**，再思考**如何让频次分布最均匀**（常用最小堆或计数排序），最后检查**字典序的 tie‑break**。