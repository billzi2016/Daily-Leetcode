# #2953. 计数完整子字符串 / Count Complete Substrings

> 难度：困难 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/count-complete-substrings/)

---

## 题目（英文原版）

**Description**

You are given a string word and an integer k.
A substring s of word is complete if:
Return the number of complete substrings of word.
A substring is a non-empty contiguous sequence of characters in a string.

**Examples**

**Example 1:**

```
Input: word = "igigee", k = 2
Output: 3
Explanation: The complete substrings where each character appears exactly twice and the difference between adjacent characters is at most 2 are: igigee, igigee, igigee.
```

**Example 2:**

```
Input: word = "aaabbbccc", k = 3
Output: 6
Explanation: The complete substrings where each character appears exactly three times and the difference between adjacent characters is at most 2 are: aaabbbccc, aaabbbccc, aaabbbccc, aaabbbccc, aaabbbccc, aaabbbccc.
```

**Constraints**

- 1 <= word.length <= 105
- word consists only of lowercase English letters.
- 1 <= k <= word.length

---

## 题目（中文翻译）

你得到一个字符串 `word` 和一个整数 `k`。  
如果一个子串（substring） `s` 满足以下条件，则称其为 **完整子串**（complete substring）：

1. `s` 中每个出现的字符恰好出现 `k` 次；
2. 将 `s` 中出现的不同字符按字母顺序排列后，相邻字符的字母序差值不超过 2（即相邻字符之间的差值 ≤ 2）。

返回 `word` 中完整子串的数量。  
子串是字符串中一个**非空的连续**字符序列。

**示例 1**

```text
输入: word = "igigee", k = 2
输出: 3
解释: 满足条件的完整子串为:
      "igigee"（i、g、e 各出现 2 次，且相邻字符差值均为 2）
      "igigee"
      "igigee"
```

**示例 2**

```text
输入: word = "aaabbbccc", k = 3
输出: 6
解释: 满足条件的完整子串为:
      "aaabbbccc"（a、b、c 各出现 3 次，且相邻字符差值均为 1）
      "aaabbbccc"
      "aaabbbccc"
      "aaabbbccc"
      "aaabbbccc"
      "aaabbbccc"
```

**约束条件**

- `1 <= word.length <= 10^5`
- `word` 仅由小写英文字母组成
- `1 <= k <= word.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举所有子串**，逐个判断它们是否满足题目要求。  
判断一段子串是否 “完整” 需要做两件事：

1. **字符出现次数**：子串里每一种出现的字符恰好出现 `k` 次。  
   - 可以用一个长度为 26 的数组（或字典）记录每个字母出现的次数。  
   - 这相当于我们在查字典：`key` 是字符，`value` 是出现次数。

2. **相邻字符差值**：子串里任意相邻两个字符的字母序号差的绝对值 ≤ 2。  
   - 只要遍历子串一次，比较相邻字符的差值即可。

如果两条都满足，这个子串就算 “完整”。把所有满足的子串计数即得到答案。

**为什么暴力一定能得到正确答案**  
因为我们没有遗漏任何子串：把所有 `n*(n+1)/2`（`n` 为字符串长度）个子串都检查了一遍，符合条件的自然就是答案。

**复杂度分析（大白话版）**  

- **时间**：  
  - 枚举子串有 `O(n²)` 种（比如长度为 10 的字符串有 55 个子串）。  
  - 对每个子串我们还要遍历一次它的字符来统计次数和相邻差值，最坏也要 `O(n)`。  
  - 综合下来是 **`O(n³)`**，在最坏情况下会像 `100000³` 那么大，根本跑不完。  
  - 用更常见的写法，**`O(n²)`** 已经够慢了（因为统计可以在子串内部一次完成），但仍然远超题目要求的 `10⁵` 规模。

- **空间**：  
  - 只需要一个大小为 26 的计数数组，**`O(1)`**（常数级别）空间。

#### 代码（Python）

```python
def countCompleteSubstrings_bruteforce(word: str, k: int) -> int:
    n = len(word)
    ans = 0
    # 把字符转成 0~25 的整数，方便后面算差值
    arr = [ord(c) - ord('a') for c in word]

    # 枚举所有子串的左端点
    for l in range(n):
        freq = [0] * 26          # 记录当前子串里每个字母的出现次数
        ok_adj = True           # 是否满足相邻字符差值 ≤ 2
        # 枚举右端点
        for r in range(l, n):
            idx = arr[r]
            freq[idx] += 1

            # 检查相邻字符差值（只在 r>l 时需要检查）
            if r > l and abs(arr[r] - arr[r - 1]) > 2:
                ok_adj = False

            # 当子串长度已经是 k 的整数倍时才有可能完整
            length = r - l + 1
            if length % k == 0:
                distinct = sum(1 for c in freq if c > 0)
                # 每种出现的字符恰好出现 k 次
                all_k = all(c == 0 or c == k for c in freq)
                if distinct * k == length and all_k and ok_adj:
                    ans += 1
    return ans
```

> 代码里每一行都有中文注释，直接可以跑通，只是对大输入会超时。

#### 复杂度

- **时间复杂度**：`O(n²)`（枚举所有子串，内部的统计是 `O(1)` 的累计过程）  
  - 大白话：如果 `n = 10⁵`，大概要检查 `10¹⁰` 次，根本不可能在一秒内算完。

- **空间复杂度**：`O(1)`（只用了固定大小的 26 长度数组）  

---

### 2. 最优解

#### 思路  

暴力的瓶颈在 **“枚举所有子串”**——这一步产生了 `O(n²)` 的子串数量。  
观察题目可以发现：

1. **完整子串的长度一定是 `k * d`**，其中 `d` 为子串里出现的不同字符数（`1 ≤ d ≤ 26`）。  
   - 也就是说，完整子串的长度只能取至多 26 种可能：`k, 2k, 3k, …, 26k`。  
   - 这把搜索空间从 `O(n²)` 大幅压缩到 `O(26·n)`。

2. 对于固定的长度 `L = k * d`，我们可以用 **滑动窗口**（Sliding Window）一次遍历整个字符串，窗口每次向右移动一格，维护窗口内部的信息（字符出现次数、不同字符数、以及相邻字符差值的最大值）。  
   - **字符出现次数**：用长度为 26 的数组 `cnt[26]` 记录。  
   - **不同字符数**：用 `distinct` 计数，当某个字符的计数从 0 变为 1 时 `distinct += 1`，从 1 变为 0 时 `distinct -= 1`。  
   - **恰好出现 k 次的字符数**：用 `exact_k` 计数，字符计数从 `k-1 → k` 时 `exact_k += 1`，从 `k → k-1` 时 `exact_k -= 1`。  
   - **相邻字符差值**：窗口内部有 `L-1` 条相邻差值。我们只需要知道这 `L-1` 条差值的 **最大值** 是否 ≤ 2。  
     - 维护最大值的常用技巧是 **单调队列（Monotonic Queue）**：在队列里保持差值从大到小的顺序，队首永远是当前窗口的最大差值。  
     - 插入新差值时把比它小的全部弹出；窗口左移时把已经不在窗口范围的索引弹出。

3. **判定窗口是否完整**：  
   - `distinct == d`（窗口里恰好有 `d` 种不同字符）  
   - `exact_k == d`（这 `d` 种字符每个都出现了恰好 `k` 次）  
   - `max_diff ≤ 2`（单调队列的队首对应的差值 ≤ 2）

只要这三条同时成立，当前窗口就是一个完整子串，计数器 `ans` 加一。

#### 为什么滑动窗口能做到 `O(n)`？

- 每次窗口右移只会 **添加** 一个字符、**删除** 一个字符，计数数组的更新是 `O(1)`。  
- 单调队列里的每个差值最多被 **插入一次、弹出一次**，所以整体也是 `O(n)`。  
- 对每一种可能的 `d (1~26)` 重复上述过程，总时间是 `26·O(n) = O(n)`（常数因子 26）。

#### 代码（Python）

```python
from collections import deque

def countCompleteSubstrings(word: str, k: int) -> int:
    """
    最优解：滑动窗口 + 单调队列
    时间复杂度 O(26 * n) ≈ O(n)
    空间复杂度 O(26)   (计数数组 + 差值单调队列)
    """
    n = len(word)
    arr = [ord(c) - ord('a') for c in word]          # 把字符映射到 0~25
    # 预先计算相邻字符的差值，方便后面直接取
    diff = [abs(arr[i] - arr[i - 1]) for i in range(1, n)]

    ans = 0

    # d 表示窗口里不同字符的数量，长度 L = k * d
    for d in range(1, 27):
        L = k * d
        if L > n:                # 窗口已经大于字符串长度，后面的 d 都不可能
            break

        cnt = [0] * 26           # 每个字符在当前窗口的出现次数
        distinct = 0             # 窗口里不同字符的种类数
        exact_k = 0              # 出现次数恰好为 k 的字符数

        # ---------- 初始化第一个窗口 ----------
        for i in range(L):
            c = arr[i]
            if cnt[c] == 0:
                distinct += 1
            cnt[c] += 1
            if cnt[c] == k:
                exact_k += 1
            elif cnt[c] == k + 1:          # 从 k 变到 k+1，失去“恰好 k 次”的资格
                exact_k -= 1

        # 单调队列维护窗口内 diff 的最大值
        # 队列里保存的是 diff 的下标，且 diff[queue[0]] 为当前窗口的最大值
        max_q = deque()
        for i in range(1, L):               # 窗口内的差值下标是 1~L-1（对应 diff[0]~diff[L-2]）
            while max_q and diff[i - 1] >= diff[max_q[-1]]:
                max_q.pop()
            max_q.append(i - 1)

        # 检查第一个窗口
        if distinct == d and exact_k == d and diff[max_q[0]] <= 2:
            ans += 1

        # ---------- 滑动窗口 ----------
        for left in range(1, n - L + 1):
            # 移出左端字符
            out_c = arr[left - 1]
            if cnt[out_c] == k:
                exact_k -= 1
            cnt[out_c] -= 1
            if cnt[out_c] == 0:
                distinct -= 1
            elif cnt[out_c] == k - 1:       # 从 k-1 变到 k-2，不影响 exact_k
                pass
            elif cnt[out_c] == k:           # 从 k+1 变到 k，重新成为 “恰好 k 次”
                exact_k += 1

            # 加入右端字符
            in_c = arr[left + L - 1]
            if cnt[in_c] == 0:
                distinct += 1
            cnt[in_c] += 1
            if cnt[in_c] == k:
                exact_k += 1
            elif cnt[in_c] == k + 1:        # 从 k 变到 k+1，失去恰好 k 次的资格
                exact_k -= 1

            # 更新单调队列：窗口的 diff 区间变为 [left, left+L-2]
            # 1）弹出已经离开窗口的下标
            while max_q and max_q[0] < left:
                max_q.popleft()
            # 2）加入新出现的 diff（下标为 left+L-2，对应 arr[left+L-2] 与 arr[left+L-1] 的差）
            new_idx = left + L - 2
            while max_q and diff[new_idx] >= diff[max_q[-1]]:
                max_q.pop()
            max_q.append(new_idx)

            # 判断当前窗口是否满足完整子串的所有条件
            if distinct == d and exact_k == d and diff[max_q[0]] <= 2:
                ans += 1

    return ans
```

> 代码里每一步都加了中文注释，直接拷贝到 Python 环境即可运行。  

#### 复杂度

- **时间复杂度**：`O(26 * n) ≈ O(n)`  
  - **解释**：我们最多遍历 26 次（因为不同字符数最多 26 种），每次只在字符串上滑动一次。对每个字符的加入/移出以及单调队列的维护都是常数时间。相比暴力的 `O(n²)`，这里快了几个数量级，`n=10⁵` 也能在毫秒级完成。

- **空间复杂度**：`O(26) = O(1)`  
  - 只用了 26 长度的计数数组和一个最多装 `L-1 ≤ n` 的单调队列。单调队列的大小随窗口而动，最坏也只会存 `L-1` 个整数，属于线性额外空间；但因为 `L ≤ 26·k ≤ 26·n`，整体仍然是 **线性**，在本题的限制下可以视作常数级别。

---

## 心得

- **核心技巧**：**滑动窗口 + 单调队列**（维护窗口内最大相邻差值）  
- **适用题型**：  
  1. “子串满足固定长度且内部属性需快速判断”——如 **“最长子串包含 K 种不同字符”**  
  2. “窗口内部需要实时获取最大/最小值”——如 **“滑动窗口最大值”**、**“子数组中最大差值 ≤ 某阈值”**  
  3. “子串长度受字符出现次数约束”——如 **“字母异位词子串计数”**  

> **一句话总结解题钥匙**：把“可能的子串长度”压缩到常数（≤ 26）后，用滑动窗口一次遍历，同时用单调队列实时获取窗口内的最大相邻差值，所有条件均可在 O(1) 内检查。

---

## 反思

- **第一反应**：看到“每个字符出现恰好 k 次”立刻想到哈希表计数，随后想到枚举子串检查——这就是暴力解的出发点。  
- **最容易踩的坑**：  
  1. **相邻差值的维护**：如果只在每次检查时重新遍历窗口，会把时间又拉回 `O(n²)`。必须使用单调队列或类似结构做到 **增删均摊 O(1)**。  
  2. **边界条件**：窗口长度 `L = k * d` 可能大于字符串长度，需要提前 `break`；窗口左移时要正确弹出对应的 `diff` 索引。  
  3. **计数的细节**：在窗口滑动时，字符计数从 `k-1 → k`、`k → k+1`、`k → k-1` 等转变都要同步更新 `exact_k`，否则会出现“出现次数恰好 k 次的字符数不准确”的错误。  

- **下次类似题的第一步**：  
  先 **分析可行的子串长度**（是否受某个离散参数限制），再决定是 **枚举长度 + 滑动窗口** 还是 **双指针**。如果窗口内部还有“最大/最小”之类的约束，立刻考虑 **单调队列** 来把检查时间降到常数。