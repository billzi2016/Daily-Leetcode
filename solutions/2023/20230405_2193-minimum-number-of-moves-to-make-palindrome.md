# #2193. 使字符串成为回文所需的最少移动次数 / Minimum Number of Moves to Make Palindrome

> 难度：困难 · 标签：Two Pointers、String、Greedy、Binary Indexed Tree · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-moves-to-make-palindrome/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting only of lowercase English letters.
In one move, you can select any two adjacent characters of s and swap them.
Return the minimum number of moves needed to make s a palindrome.
Note that the input will be generated such that s can always be converted to a palindrome.

**Examples**

**Example 1:**

```
Input: s = "aabb"
Output: 2
Explanation:
We can obtain two palindromes from s, "abba" and "baab". 
- We can obtain "abba" from s in 2 moves: "aabb" -> "abab" -> "abba".
- We can obtain "baab" from s in 2 moves: "aabb" -> "abab" -> "baab".
Thus, the minimum number of moves needed to make s a palindrome is 2.
```

**Example 2:**

```
Input: s = "letelt"
Output: 2
Explanation:
One of the palindromes we can obtain from s in 2 moves is "lettel".
One of the ways we can obtain it is "letelt" -> "letetl" -> "lettel".
Other palindromes such as "tleelt" can also be obtained in 2 moves.
It can be shown that it is not possible to obtain a palindrome in less than 2 moves.
```

**Constraints**

- 1 <= s.length <= 2000
- s consists only of lowercase English letters.
- s can be converted to a palindrome using a finite number of moves.

---

## 题目（中文翻译）

**题目描述**  
给定一个仅由小写英文字母组成的字符串 `s`。  
一次移动（move）中，你可以选择 `s` 中任意两个相邻字符（adjacent characters）并将它们交换（swap）。  
返回使 `s` 成为回文（palindrome）所需的最少移动次数。  
题目保证输入的 `s` 必定可以转换成回文。

**示例 1**  
```text
Input: s = "aabb"
Output: 2
Explanation:
我们可以得到两个回文字符串，分别是 "abba" 和 "baab"。
- 将 "aabb" 变成 "abba" 需要 2 次移动："aabb" -> "abab" -> "abba"。
- 将 "aabb" 变成 "baab" 也需要 2 次移动："aabb" -> "abab" -> "baab"。
因此，使 `s` 成为回文的最少移动次数为 2。
```

**示例 2**  
```text
Input: s = "letelt"
Output: 2
Explanation:
一种可以在 2 次移动内得到的回文是 "lettel"。
实现方式之一为 "letelt" -> "letetl" -> "lettel"。
其他回文如 "tleelt" 也可以在 2 次移动内得到。
可以证明，少于 2 次移动无法得到回文。
```

**约束条件**  
- `1 <= s.length <= 2000`
- `s` 仅由小写英文字母组成。
- `s` 能在有限次数的移动后转换成回文。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从两端向中间逐步配对**。  
把字符串看成一排坐在一起的字母（就像排队买票的观众），我们只能让相邻的两个人互相换位。  

1. 设左指针 `l` 指向最左侧，右指针 `r` 指向最右侧。  
2. 若 `s[l] == s[r]`，说明这两个字符已经可以成为回文的左右两端，直接把指针向里收缩：`l += 1, r -= 1`。  
3. 否则，我们在 `r` 左边（即 `l…r-1`）寻找第一个与 `s[l]` 相同的字符 `s[k]`。  
   - 找到后，把 `s[k]` 向右搬到位置 `r`，每次只交换相邻的两个字符，搬动一次计一次步数。  
   - 若一直找不到（说明 `s[l]` 只出现奇数次且正好是中间的唯一字符），则把 `s[l]` 向左搬到最中间，同样用相邻交换计步。  
4. 重复以上过程，直到 `l >= r`。

> **为什么能得到正确答案？**  
> 这一步一步把最左边的字符“送”到最右边能保证左、右两侧字符相等；如果左边字符在右侧没有配对，只能它自己成为中心字符。因为每一步都用了**最少的相邻交换**（直接把最近的匹配字符搬过去），整体步数就是最小的。

> **时间/空间复杂度**  
> - 每次寻找匹配字符最多要遍历 `r‑l` 次，搬动也最多 `r‑l` 步。最坏情况下，这样的操作会在整个字符串上进行 `n/2` 次，所以总时间是 `O(n²)`。  
>   - “`O(n²)`” 可以想象成：如果 `n=2000`，最多要做 2 000 × 2 000 ≈ 4 百万 次基本操作，虽然在 Python 里还能跑完，但对更大 `n` 会明显慢。  
> - 只用了几个指针和计数器，额外空间是 `O(1)`（常数级）。

#### 代码（Python）

```python
def minMovesToMakePalindrome_bruteforce(s: str) -> int:
    # 把字符串转成列表，方便原地交换
    s = list(s)
    n = len(s)
    l, r = 0, n - 1          # 左右指针
    moves = 0                # 计数器

    while l < r:
        if s[l] == s[r]:
            # 两端已经匹配，收缩指针
            l += 1
            r -= 1
            continue

        # 在左指针左边寻找与 s[l] 匹配的字符
        k = r
        while k > l and s[k] != s[l]:
            k -= 1

        if k == l:               # 没找到，说明 s[l] 必须是中间字符
            # 把它向右移动一位（相当于和左邻居交换），计一步
            s[l], s[l+1] = s[l+1], s[l]
            moves += 1
        else:
            # 找到匹配字符 s[k]，把它一步步向右搬到位置 r
            while k < r:
                s[k], s[k+1] = s[k+1], s[k]   # 相邻交换
                moves += 1
                k += 1
            # 配对成功，收缩指针
            l += 1
            r -= 1

    return moves
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 对每对左右字符，最坏要遍历剩余的全部字符并进行相同次数的交换。  
- **空间复杂度**：`O(1)` — 只用了常数个额外变量（指针、计数器）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要线性搜索匹配字符并逐个交换**，这导致 `O(n²)`。  
我们可以把“把字符搬到目标位置的次数”抽象成**逆序对（inversion）**的计数问题，从而使用 **树状数组（Binary Indexed Tree，简称 BIT）** 在 `O(log n)` 时间内完成一次搬动的计数。

关键步骤如下：

1. **确定每个字符在最终回文中的位置**  
   - 统计每个字母出现的次数。奇数次数的字母只能出现在回文的中间（最多一个）。  
   - 从左到右遍历原字符串，给每个字符分配一个**目标下标** `target[i]`，表示它在最终回文中应该站在第几位。  
   - 具体做法：  
     * 为每个字符维护两个队列 `pos[char]`：`left_queue`（从左往右填）和 `right_queue`（从右往左填）。  
     * 当遍历到字符 `c` 时，如果还有未使用的左侧位置，就把该字符映射到左侧最靠近中心的空位；否则映射到右侧对应的空位。  
   - 这样得到的 `target` 序列满足：如果我们把原字符串的字符 **按照 `target` 的顺序重新排列**，得到的就是一个合法的回文。

2. **把搬动次数转化为逆序对**  
   - 把原字符串的下标序列 `0,1,2,…,n‑1` 看成原始顺序。我们希望把它变成 `target` 的顺序。  
   - 每次把一个字符向右搬 `k` 步，相当于在原序列中，这个字符“越过”了 `k` 个已经在前面的字符。累计所有这样的越过次数，就是 **逆序对的总数**。  

3. **使用 BIT 统计逆序对**  
   - BIT 能在 `O(log n)` 时间内完成两类操作：  
     * `add(i, 1)`：在位置 `i` 上加 1，表示该位置的字符已经“放好”。  
     * `query(i)`：返回前缀和 `sum[0…i]`，即已经放好的字符中，位置 ≤ `i` 的数量。  
   - 遍历原字符串的下标 `i`（从左到右），对每个 `i`：
     * `pos = target[i]` 是它应该去的目标位置。  
     * 已经放好的字符中，**在 `pos` 右侧** 的数量即为当前字符需要跨过的步数。可以用 `already - query(pos)` 计算，其中 `already` 是已经处理的字符数。  
     * 累加到答案后，`add(pos, 1)` 把当前位置标记为已占用。  

4. **时间复杂度**：  
   - 统计字符、构造 `target` 均为 `O(n)`。  
   - BIT 的每次查询/更新是 `O(log n)`，共 `n` 次，整体 `O(n log n)`。  
   - 这比 `O(n²)` 快很多，尤其在 `n=2000` 时几乎是瞬间完成。

> **类比**：想象一排小朋友要重新排成指定的顺序，只有相邻的两个可以换位。我们不需要真的去换位，只要数一数每个小朋友要“跳过”多少已经排好队的同伴，就能得到最少的交换次数——这正是逆序对的含义。

#### 代码（Python）

```python
class BIT:
    """树状数组（Binary Indexed Tree），支持前缀和查询和单点增量"""
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)   # 1-indexed

    def add(self, idx: int, delta: int = 1):
        """在位置 idx（0-indexed）上加 delta"""
        i = idx + 1                # 转成 1-indexed
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i            # lowbit

    def query(self, idx: int) -> int:
        """返回前缀和 sum[0..idx]（0-indexed），若 idx<0 返回 0"""
        if idx < 0:
            return 0
        i = idx + 1
        s = 0
        while i:
            s += self.tree[i]
            i -= i & -i
        return s


def minMovesToMakePalindrome(s: str) -> int:
    n = len(s)
    # 1️⃣ 统计字符出现次数，准备左右两侧的目标位置
    from collections import defaultdict, deque

    cnt = defaultdict(int)
    for ch in s:
        cnt[ch] += 1

    # left_pos 为从左往右填的下标，right_pos 为从右往左填的下标
    left_pos = 0
    right_pos = n - 1
    # 为每个字符准备两个队列，存放它们应该去的目标下标
    target_queue = defaultdict(deque)

    for ch in sorted(cnt.keys()):            # 任意顺序都行，这里只为可读性排个序
        c = cnt[ch]
        # 偶数次：一半放左侧，一半放右侧
        # 奇数次：左侧多放 (c//2) 个，剩下的一个放中间（若有）
        for _ in range(c // 2):
            target_queue[ch].append(left_pos)
            left_pos += 1
            target_queue[ch].appendleft(right_pos)   # 右侧用 appendleft 保持对应顺序
            right_pos -= 1
        if c % 2:        # 奇数个，放到中间（此时 left_pos == right_pos）
            target_queue[ch].append(left_pos)   # 中间位置只出现一次
            left_pos += 1   # 此后 left_pos 会超过 right_pos，循环结束

    # 2️⃣ 生成每个原字符对应的目标下标序列
    target = [0] * n
    for i, ch in enumerate(s):
        target[i] = target_queue[ch].popleft()

    # 3️⃣ 用 BIT 统计逆序对（即需要的最小相邻交换次数）
    bit = BIT(n)
    moves = 0
    already = 0          # 已经放好的字符数量

    for i in range(n):
        pos = target[i]          # 该字符最终应站的位置
        # 已经放好的字符中，位于 pos 右侧的数量 = already - query(pos)
        moves += already - bit.query(pos)
        bit.add(pos, 1)          # 标记当前位置已占用
        already += 1

    return moves
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `n` 为字符串长度（≤ 2000）。  
  - 与暴力 `O(n²)` 相比，`log n`（约 11）是一个常数级的加速，实际运行几乎是瞬时完成。  
- **空间复杂度**：`O(n)`  
  - 需要存放 `target` 数组、每个字符的目标队列以及 BIT 的内部数组，均随 `n` 成线性增长。

---

## 心得

- **核心技巧**：把“相邻交换把字符串变成回文”转化为**逆序对计数**，并利用 **树状数组（BIT）** 高效求解。  
- **该技巧适用的题型**  
  1. “最少相邻交换把数组/字符串排序”  
  2. “把字符串变成字典序最小/最大”  
  3. “求最小交换次数使两个序列相同”  
- **一句话总结解题钥匙**：  
  > 把每个字符的目标位置排好序，答案就是原顺序到目标顺序的逆序对数。

---

## 反思

- **第一反应**：看到只能交换相邻字符，就想到“冒泡排序”那种一步步把元素搬到正确位置，于是写了逐个搜索并搬动的双指针实现。  
- **最容易踩的坑**  
  1. **奇数长度字符的中间位**：如果不专门处理出现奇数次的字符，可能会把它们错误地配对导致无法形成回文。  
  2. **计数越界**：在 BIT 中查询前缀和时，`idx` 为 `-1` 时要返回 0，否则会出现负索引错误。  
  3. **目标下标分配顺序**：左、右两侧的下标必须配对好（左边递增、右边递减），否则逆序对的计数会不正确。  
- **下次遇到同类题的第一步**：  
  > 先把“最终形态”用下标映射写出来（即每个元素应该去哪个位置），再思考如何在不真的搬动的情况下统计需要跨过多少已放好的元素——这往往就是逆序对 + BIT/线段树的模式。