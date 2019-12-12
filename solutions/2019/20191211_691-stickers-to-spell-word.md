# #691. 贴纸拼出单词 / Stickers to Spell Word

> 难度：困难 · 标签：Array、Hash Table、String、Dynamic Programming、Backtracking、Bit Manipulation、Memoization、Bitmask · [LeetCode 链接](https://leetcode.com/problems/stickers-to-spell-word/)

---

## 题目（英文原版）

**Description**

We are given n different types of stickers. Each sticker has a lowercase English word on it.
You would like to spell out the given string target by cutting individual letters from your collection of stickers and rearranging them. You can use each sticker more than once if you want, and you have infinite quantities of each sticker.
Return the minimum number of stickers that you need to spell out target. If the task is impossible, return -1.
Note: In all test cases, all words were chosen randomly from the 1000 most common US English words, and target was chosen as a concatenation of two random words.

**Examples**

**Example 1:**

```
Input: stickers = ["with","example","science"], target = "thehat"
Output: 3
Explanation:
We can use 2 "with" stickers, and 1 "example" sticker.
After cutting and rearrange the letters of those stickers, we can form the target "thehat".
Also, this is the minimum number of stickers necessary to form the target string.
```

**Example 2:**

```
Input: stickers = ["notice","possible"], target = "basicbasic"
Output: -1
Explanation:
We cannot form the target "basicbasic" from cutting letters from the given stickers.
```

**Constraints**

- n == stickers.length
- 1 <= n <= 50
- 1 <= stickers[i].length <= 10
- 1 <= target.length <= 15
- stickers[i] and target consist of lowercase English letters.

---

## 题目（中文翻译）

我们有 `n` 种不同的贴纸（stickers）。每张贴纸上都有一个小写英文字母组成的单词。  
现在需要通过从贴纸上剪下单个字母并重新排列，拼出给定的字符串 `target`。每张贴纸可以使用多次，并且每种贴纸的数量是无限的。  

返回拼出 `target` 所需的最少贴纸数量。如果无法完成任务，返回 `-1`。  

> **注意**：在所有测试用例中，所有单词均随机选自美国常用的 1000 个英文单词，`target` 是两个随机单词的拼接。

### 示例

**示例 1**  
```text
Input: stickers = ["with","example","science"], target = "thehat"
Output: 3
Explanation:
我们可以使用两张 "with" 贴纸和一张 "example" 贴纸。
将这些贴纸上的字母剪下并重新排列后，就可以得到目标字符串 "thehat"。
这也是形成目标字符串所需的最少贴纸数。
```

**示例 2**  
```text
Input: stickers = ["notice","possible"], target = "basicbasic"
Output: -1
Explanation:
无法仅通过剪切给定贴纸上的字母来组成目标字符串 "basicbasic"。
```

### 约束条件
- `n == stickers.length`
- `1 <= n <= 50`
- `1 <= stickers[i].length <= 10`
- `1 <= target.length <= 15`
- `stickers[i]` 和 `target` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每张贴纸当成一把可以取走字母的“工具”，不停地挑选贴纸，直到把目标 `target` 的所有字母都取完**。  
具体步骤：

1. **把目标拆成字母列表**（比如 `"thehat"` → `['t','h','e','h','a','t']`），记下来还有哪些字母没有被取走。  
2. **枚举所有可能的贴纸序列**（可以重复使用同一张贴纸），每选一张贴纸，就把它上面的字母从目标中“删掉”。  
3. 当目标的所有字母都被删光时，记录使用的贴纸数量；遍历完所有可能的序列后，取最小的那个。

> **生活类比**：想象你在厨房里有若干种调味料瓶，每瓶里都有若干种调味料（字母）。要做出一道菜（target），你可以无限次打开同一瓶，取走里面的调味料，直到配齐所有需要的味道。最笨的办法就是把每一种可能的开瓶顺序都尝试一遍。

**为什么这个方法能得到正确答案**  
因为我们枚举了 **所有** 可能的贴纸使用顺序，只要有一种组合能够拼出 `target`，必然会在枚举过程中出现，所以最小的使用次数一定会被记录下来。

**时间/空间分析（大白话）**  
- 目标长度最多 15，假设我们每次都只取走 1 个字母，那么最差情况需要尝试 `len(stickers) ^ 15` 种序列，呈指数级增长。  
- 这相当于“每一步都有 `n` 种选择，走 `15` 步”，所以时间复杂度大约是 `O(n^|target|)`，会非常慢。  
- 只需要保存当前剩余的字母列表，空间复杂度是 `O(|target|)`，即最多 15 个字符。

#### 代码（Python）

```python
from collections import Counter
from copy import deepcopy

def minStickers_bruteforce(stickers, target):
    # 把每张贴纸转成字母计数的 Counter，方便后面减法
    sticker_counts = [Counter(s) for s in stickers]

    # 递归搜索：cur_target 记录还剩下的字母计数
    def dfs(cur_target):
        # 如果所有字母都取完，返回 0 张贴纸
        if not cur_target:
            return 0

        # 否则尝试每一张贴纸
        ans = float('inf')
        for cnt in sticker_counts:
            # 只在这张贴纸至少包含 cur_target 中的第一个字母时才尝试
            # 这一步是“剪枝”，可以省掉很多无用的递归分支
            first_char = next(iter(cur_target))
            if cnt[first_char] == 0:
                continue

            # 用这张贴纸后，剩余的字母计数
            new_target = cur_target - cnt   # Counter 支持直接相减，负数会被丢弃
            # 递归求子问题的最小贴纸数
            sub = dfs(new_target)
            if sub != -1:                     # -1 表示子问题无解
                ans = min(ans, 1 + sub)

        return -1 if ans == float('inf') else ans

    # 把目标字符串转成 Counter
    target_counter = Counter(target)
    return dfs(target_counter)
```

> **关键行解释**  
> - `Counter(s)` 把字符串变成 “字典”，像查字典一样，键是字母，值是出现次数。  
> - `cur_target - cnt` 自动把已经被贴纸提供的字母数量减掉，负数会被自动丢掉（相当于 “把已经够的字母去掉”）。  
> - `if cnt[first_char] == 0: continue` 是一个小技巧：如果当前贴纸根本不含目标里剩余的第一个字母，就没有必要尝试它，能大幅削减搜索树。

#### 复杂度

- **时间复杂度**：`O(n^{|target|})`（指数级），因为每一步都可能选择 `n` 张贴纸，最多走 `|target|` 步。  
  > 大白话：如果 `n=5，|target|=15`，最坏情况下相当于要尝试 5 的 15 次方 ≈ 30 亿种组合，根本跑不完。  
- **空间复杂度**：`O(|target|)`，递归栈深度最多等于目标长度（最多 15），以及保存一个 `Counter`（最多 26 种字母）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每一次都把所有贴纸都尝试一次”**，导致搜索树爆炸。我们可以从以下几个方向逐步优化：

1. **只保留对目标有帮助的字母**  
   贴纸里出现的、但 **不在 `target`** 中的字母永远不会被用到，直接把它们删掉。这样每张贴纸的有效长度会变短。

2. **去掉“被支配”的贴纸**  
   如果贴纸 `A` 的每个字母出现次数都 **不小于** 贴纸 `B`，则 `A` **支配** `B`，使用 `B` 永远不会比使用 `A` 更好（因为 `A` 能提供至少一样多的字母）。我们可以把所有被支配的贴纸剔除，减少候选数量。

3. **记忆化搜索（Memoization）**  
   目标的剩余字母状态可以用 **位掩码（bitmask）** 或 **Counter** 表示。相同的剩余状态会出现多次，使用哈希表把已经算过的状态记下来，避免重复递归。  
   - 由于 `target` 最长 15，使用 **位掩码** 很方便：把每个字符位置视作一位，`1` 表示该位置的字母还未被覆盖。这样状态空间最多 `2^{15}=32768`，非常可管理。

4. **贪心选取“能消除最多未覆盖字母的贴纸”**（剪枝）  
   在递归的每一步，先挑选能够 **覆盖当前未覆盖字母中最多** 的贴纸，只对这些贴纸继续递归。若当前已经找到的答案 `best` 为 `k`，而这一步需要的贴纸数已经 ≥ `k`，则直接返回，避免无效搜索。

综合以上技巧，**最优解** 采用 **记忆化的深度优先搜索 + 位掩码**，时间大幅降低到 `O(n * 2^{|target|})`，空间 `O(2^{|target|})`。

> **核心概念解释**  
> - **位掩码**：把目标字符串的每个字符位置当作一根开关，`0` 表示已得到，`1` 表示还缺。比如目标 `"the"` 长度 3，状态 `101`（二进制）表示第 1、3 位字符还未得到。位运算非常快，适合枚举所有子集。  
> - **记忆化**：把已经算好的子问题（某个掩码对应的最少贴纸数）存进字典，下次再遇到同样的掩码直接返回，不再重复计算。  
> - **支配关系**：如果贴纸 `A` 在每个字母上的数量都 ≥ 贴纸 `B`，则 `A` 永远不比 `B` 差，直接丢掉 `B`，相当于把“劣势选手”剔除。

#### 代码（Python）

```python
from collections import Counter
from functools import lru_cache

def minStickers(stickers, target):
    """
    最优解：记忆化搜索 + 位掩码 + 预处理（去除无关字母、支配贴纸）
    """
    m = len(target)
    # 把目标每个字符的索引记下来，方便后面快速定位
    char_pos = {}
    for i, ch in enumerate(target):
        char_pos.setdefault(ch, []).append(i)

    # 1️⃣ 预处理：把每张贴纸只保留 target 中出现的字母，并转成 Counter
    processed = []
    for s in stickers:
        cnt = Counter()
        for ch in s:
            if ch in char_pos:          # 只保留目标里需要的字母
                cnt[ch] += 1
        if cnt:                         # 过滤掉完全无用的贴纸
            processed.append(cnt)

    # 2️⃣ 去掉被支配的贴纸
    def dominates(a, b):
        """若 a 在所有字母上出现次数都 >= b，则 a 支配 b"""
        for ch in b:
            if a[ch] < b[ch]:
                return False
        return True

    filtered = []
    for i, cnt_i in enumerate(processed):
        dominated = False
        for j, cnt_j in enumerate(processed):
            if i != j and dominates(cnt_j, cnt_i):
                dominated = True
                break
        if not dominated:
            filtered.append(cnt_i)

    stickers = filtered
    n = len(stickers)

    # 3️⃣ 把每张贴纸转换为「可以一次性覆盖哪些目标位置」的位掩码
    #    例如贴纸 "with" 对 target "thehat" 可以覆盖位置 {0,2,4} → mask = 0b010101
    sticker_masks = []
    for cnt in stickers:
        mask = 0
        # 对每个字母，尽可能覆盖 target 中对应的未覆盖位置
        for ch, num in cnt.items():
            # 目标中该字母出现的所有位置
            positions = char_pos[ch]
            # 用贪心：从左到右把该字母填满
            for pos in positions:
                if num == 0:
                    break
                if not (mask >> pos) & 1:   # 该位置还未被覆盖
                    mask |= 1 << pos
                    num -= 1
        sticker_masks.append(mask)

    # 4️⃣ 记忆化深度优先搜索（状态 = 仍未覆盖的位掩码）
    @lru_cache(None)
    def dfs(state):
        """
        返回把 `state`（未覆盖的位）全部填满最少需要多少张贴纸。
        state 为整数，二进制的 1 表示该位置的字符还缺。
        """
        if state == 0:          # 全部覆盖完毕
            return 0

        # 取出当前未覆盖的第一个位置（最低位的 1），用于剪枝
        # 这样我们只尝试能覆盖这个位置的贴纸，减少分支
        first_unfilled = (state & -state).bit_length() - 1   # 低位 1 的索引

        ans = float('inf')
        for mask in sticker_masks:
            # 如果这张贴纸连当前未覆盖的字符都不包含，直接跳过
            if not (mask >> first_unfilled) & 1:
                continue
            # 新的未覆盖状态 = 之前的状态 & ~mask（把贴纸覆盖的位清零）
            new_state = state & ~mask
            sub = dfs(new_state)
            if sub != -1:
                ans = min(ans, 1 + sub)

        return -1 if ans == float('inf') else ans

    full_state = (1 << m) - 1          # 所有位均为 1，表示全部未覆盖
    return dfs(full_state)
```

> **关键行解释**  
> - `char_pos` 把每个字母对应的目标下标收集起来，后面构造掩码时会用到。  
> - `dominates` 用来判断一张贴纸是否完全“强于”另一张，如果是，就把弱的那张删掉，减小搜索空间。  
> - `mask |= 1 << pos` 把目标中第 `pos` 位标记为已覆盖。  
> - `first_unfilled = (state & -state).bit_length() - 1` 取出当前状态最右边的 `1`（即最左侧还未覆盖的字符），只对能覆盖它的贴纸继续递归，等价于 “先解决最急迫的需求”。  
> - `new_state = state & ~mask` 把这张贴纸已经覆盖的位清零，得到下一个子问题。  
> - `@lru_cache(None)` 自动把每个 `state` 的答案记住，避免重复计算。

#### 复杂度

- **时间复杂度**：`O(n * 2^{|target|})`  
  - `|target| ≤ 15`，所以 `2^{|target|}` 最多是 32768，乘以最多 50 张贴纸，约 1.6M 次操作，能够在毫秒级完成。  
  - 与暴力的指数 `n^{|target|}` 相比，指数底数从 `n` 降到了常数 2，快了好几个数量级。

- **空间复杂度**：`O(2^{|target|})`（记忆化表）  
  - 只需要保存每个掩码对应的最小贴纸数，最多 32768 条记录，几乎可以忽略不计。  

> 与暴力解对比：时间从“指数级爆炸”降到“指数级但底数只有 2”，空间略增（记忆化表），但仍然非常小。

---

## 心得

- **核心技巧**：**位掩码 + 记忆化搜索**，配合**预处理（去除无关字母、支配贴纸）**与**剪枝**。  
- **适用的题型**（类似思路）  
  1. *Sticker to Spell Word*（本题）  
  2. *Word Break II*（利用记忆化 DFS 生成所有拆分）  
  3. *Minimum Number of Taps to Open to Water a Garden*（使用位掩码 DP）  
- **一句话总结解题钥匙**：**把剩余目标抽象成一个二进制状态，递归求最小贴纸数并记忆化，配合剪枝即可快速求解**。

---

## 反思

- **第一反应**：直接想把所有贴纸一次一次尝试（暴力搜索），因为题目说可以无限使用贴纸，感觉只要穷举就行。  
- **最容易踩的坑**  
  - **剪枝不够**：没有去掉无用字母和被支配的贴纸，导致搜索树仍然非常大。  
  - **状态表示错误**：直接用字符串或 Counter 作为状态会导致哈希冲突或大量重复子问题，位掩码能让状态唯一且高效。  
  - **忘记记忆化**：递归会产生大量相同的子状态，未记忆化会导致指数级重复计算。  
- **下次遇到同类题**：第一步先 **抽象出“剩余需求的状态”**（位掩码或集合），检查是否可以 **用 DP / 记忆化搜索** 来复用子问题，然后再考虑 **预处理**（去除无关信息、支配关系）来进一步剪枝。