# #466. 计数重复次数 / Count The Repetitions

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-the-repetitions/)

---

## 题目（英文原版）

**Description**

We define str = [s, n] as the string str which consists of the string s concatenated n times.
We define that string s1 can be obtained from string s2 if we can remove some characters from s2 such that it becomes s1.
You are given two strings s1 and s2 and two integers n1 and n2. You have the two strings str1 = [s1, n1] and str2 = [s2, n2].
Return the maximum integer m such that str = [str2, m] can be obtained from str1.

**Examples**

**Example 1:**

```
Input: s1 = "acb", n1 = 4, s2 = "ab", n2 = 2
Output: 2
```

**Example 2:**

```
Input: s1 = "acb", n1 = 1, s2 = "acb", n2 = 1
Output: 1
```

**Constraints**

- 1 <= s1.length, s2.length <= 100
- s1 and s2 consist of lowercase English letters.
- 1 <= n1, n2 <= 106

---

## 题目（中文翻译）

我们定义 **str = [s, n]** 为将字符串 **s** 连续拼接 **n** 次得到的字符串。  
如果可以从字符串 **s2** 中删除若干字符，使其变成 **s1**，则称 **s1** 能从 **s2** 中得到（obtain）。  

给定两个字符串 **s1**、**s2** 与两个整数 **n1**、**n2**，构造如下两个大字符串：

- **str1 = [s1, n1]**
- **str2 = [s2, n2]**

返回最大的整数 **m**，使得 **str = [str2, m]** 能从 **str1** 中得到。

---

**示例 1**  

**输入**: `s1 = "acb", n1 = 4, s2 = "ab", n2 = 2`  
**输出**: `2`

**示例 2**  

**输入**: `s1 = "acb", n1 = 1, s2 = "acb", n2 = 1`  
**输出**: `1`

---

**约束条件**

- `1 <= s1.length, s2.length <= 100`
- `s1` 与 `s2` 仅由小写英文字母组成
- `1 <= n1, n2 <= 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把 `str1 = s1` 重复 `n1` 次拼成一个巨大的字符串**，然后**从左到右一次遍历**，看能在其中顺序挑出多少个 `s2`（再乘 `n2` 次得到的 `str2`）。  

- **挑字符**的过程可以类比为**从一本书里挑出关键词**：我们手里有一本长书（`str1`），要把目标词（`s2`）的每个字母依次在书中找到，找到后把指针往后移动，继续找下一个字母。  
- 每当完整找完一次 `s2`，计数器 `cnt` 加一，表示我们已经得到一个 `str2` 的 **一份**（`s2` 本身）。  
- 最后把 `cnt` 除以 `n2`（因为 `str2` 是 `s2` 重复 `n2` 次），得到最大整数 `m`。  

**为什么正确？**  
因为我们严格按照原始顺序挑字符，只有这样才能保证挑出来的子序列真的能在 `str1` 中出现。遍历完整个 `str1` 后，所有可能的子序列都已经被尝试过了，计数器记录的就是最多能得到的 `s2` 个数。

**复杂度**（大白话）  
- `str1` 的长度是 `|s1| * n1`，最多 `100 * 10⁶ = 10⁸`，直接把它全部拼出来并遍历会 **非常慢**。  
- 对每个字符我们都要和 `s2` 的当前字符比较，最坏情况每走一步都要比较一次，所以时间是 **O(|s1| * n1 * |s2|)**。  
- 额外的空间只用了几个计数器，**O(1)**。

#### 代码（Python）  

```python
def get_max_repetitions_bruteforce(s1: str, n1: int, s2: str, n2: int) -> int:
    # 1. 直接构造 str1（注意：这里仅作演示，实际会爆内存）
    str1 = s1 * n1                       # 把 s1 重复 n1 次
    i_s2 = 0                               # s2 当前要匹配的下标
    cnt_s2 = 0                             # 已经完整匹配了多少个 s2

    # 2. 逐字符遍历 str1
    for ch in str1:
        # 如果当前字符恰好等于 s2[i_s2]，就向前推进
        if ch == s2[i_s2]:
            i_s2 += 1
            # 完成一次 s2，计数器加一，指针回到 s2 开头
            if i_s2 == len(s2):
                i_s2 = 0
                cnt_s2 += 1

    # 3. 把得到的 s2 个数除以 n2，得到最大 m
    return cnt_s2 // n2
```

> **注意**：这段代码在 `n1` 很大时会直接 **MemoryError**，只能作为“暴力思路”参考。

#### 复杂度  

- **时间复杂度**：`O(|s1| * n1 * |s2|)`  
  - 直译：如果 `s1` 长 100，`n1` 是 10⁶，`s2` 长 100，最坏要做 10¹⁰ 次字符比较，根本跑不完。  
- **空间复杂度**：`O(1)`（不计 `str1` 本身的存储，实际实现时会因为拼串而额外占用 `O(|s1|*n1)` 空间）。

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于我们每次都把 `s1` 的每一次出现都完整遍历了一遍。  
事实上，**只要知道一次 `s1` 循环后，指针在 `s2` 中的位置以及已经匹配了多少个 `s2`，就可以把同样的过程“跳过”。**  

我们可以把问题抽象为：

> 对每一次 **完整的 `s1`**（记为一次 “块”），记录两个信息  
> 1. 经过这块后，已经完整匹配了多少个 `s2`（记为 `cnt[i]`）  
> 2. 这块结束时，`s2` 的指针停在了哪个下标（记为 `next_idx[i]`）  

因为 `s2` 的指针只会在 `0 … len(s2)-1` 之间循环，**最多只有 `len(s2)` 种不同的状态**。当我们在遍历 `n1` 块 `s1` 时，若某个 `next_idx` 再次出现，就说明出现了**循环**（也叫“快慢指针”里的环）。  

利用这个环，我们可以：

1. **先跑几块**，直到出现第一次重复的 `next_idx`（记录下出现的块号 `pre` 和当前块号 `cur`）。  
2. 这两块之间的 **循环长度** 为 `loop_len = cur - pre`，**循环里累计的 `s2` 数量** 为 `loop_cnt = cnt[cur] - cnt[pre]`。  
3. 计算 `n1` 中可以完整放入多少个循环：`loops = (n1 - pre) // loop_len`。  
4. 用 `loops * loop_cnt` 把这些循环的贡献一次性加进答案。  
5. 最后处理剩余的几块（`(n1 - pre) % loop_len`），直接查表得到对应的 `cnt` 增量。  

这样我们只需要 **遍历至多 `len(s2) + 1` 次块**，而不必真的走 `n1` 次，时间从天文数字降到几千次。

下面把关键步骤拆开解释：

- **一次块的模拟**  
  用两个指针：`i` 在 `s1` 上遍历，`j` 在 `s2` 上遍历。每当 `s1[i] == s2[j]`，`j` 前进一步；`j` 到达 `len(s2)` 时说明完成一次 `s2`，计数 `c += 1`，`j = 0` 继续。遍历完 `s1` 后，得到这一次块的 `(c, j)`。

- **记录状态表**  
  `cnt[k]` 表示 **前 k 块**（0 ≤ k ≤ n1）累计匹配的 `s2` 数量。`idx[k]` 表示 **第 k 块结束时**，`s2` 指针所在的位置。我们只需要把 `cnt`、`idx` 按块号保存到列表里。

- **环检测**  
  用字典 `seen` 把 `s2` 指针 `j` 映射到它第一次出现的块号。第一次再次出现时，就找到了环的入口。

> **类比**：想象你在玩“转盘抽奖”，每转一圈（一次块）都会让指针停在某个格子（`j`），而且每次转动的奖励（匹配的 `s2`）是已知的。如果你发现指针又回到了之前的格子，说明以后每转一次都会得到**相同的奖励**，于是可以一次性算好后面的很多圈。

#### 代码（Python）  

```python
def get_max_repetitions(s1: str, n1: int, s2: str, n2: int) -> int:
    """
    返回最大的整数 m，使得 [s2, n2] 重复 m 次可以从 [s1, n1] 中删去字符得到。
    """

    # 预处理：如果 s2 中出现了 s1 从未包含的字符，直接返回 0
    if set(s2) - set(s1):
        return 0

    # ---------- 1. 一次块的模拟，得到 (cnt, next_idx) ----------
    # cnt_per[i] : 经过 i 块 s1 后累计匹配的 s2 次数
    # idx_per[i] : 第 i 块结束时，s2 指针所在位置
    cnt_per = [0]          # cnt_per[0] = 0，表示 0 块之前匹配了 0 次 s2
    idx_per = [0]          # idx_per[0] = 0，表示指针初始在 s2 的第 0 位

    # 用字典记录某个 s2 指针第一次出现时对应的块号
    # key = s2 的指针位置 j，value = (块号, 已累计的 s2 次数)
    seen = dict()

    # 当前指针在 s2 中的位置
    j = 0
    # 已经累计匹配的 s2 次数
    total_cnt = 0

    # 遍历块号，从 1 开始，最多遍历 n1 次（但会提前跳出）
    for block in range(1, n1 + 1):
        # ---- 模拟一次完整的 s1 ----
        for ch in s1:
            if ch == s2[j]:
                j += 1                     # s2 指针前进一步
                if j == len(s2):           # 完成一次 s2
                    j = 0
                    total_cnt += 1

        # 记录本块结束后的状态
        cnt_per.append(total_cnt)
        idx_per.append(j)

        # ---- 环检测 ----
        if j in seen:                     # 同样的指针位置再次出现，说明进入循环
            pre_block, pre_cnt = seen[j]  # 循环入口的块号和累计次数
            cur_block = block             # 当前块号
            # 循环长度（块数）和循环里累计的 s2 次数
            loop_len = cur_block - pre_block
            loop_cnt = total_cnt - pre_cnt

            # 计算可以完整加入多少个循环
            remain_blocks = n1 - pre_block
            loops = remain_blocks // loop_len

            # 先把循环的贡献一次性加进答案
            total_cnt = pre_cnt + loops * loop_cnt

            # 处理循环结束后剩余的几块（不到一个完整循环的部分）
            rest = remain_blocks % loop_len
            # 这些剩余块对应的累计次数可以直接从 cnt_per 表中查到
            total_cnt += cnt_per[pre_block + rest] - cnt_per[pre_block]

            # 循环结束，直接返回答案
            return total_cnt // n2

        else:
            # 第一次出现该指针位置，记录下来
            seen[j] = (block, total_cnt)

    # 如果没有出现循环（极少情况），直接用全部块的累计次数算答案
    return total_cnt // n2
```

> **代码要点注释**  
> - `set(s2) - set(s1)`：先检查有没有不可能匹配的字符，省去后面的计算。  
> - `cnt_per`、`idx_per`：把每块的结果存进列表，后面查表可以 **O(1)** 取到。  
> - `seen`：把 `s2` 的指针位置映射到它第一次出现的块号，实现环检测。  
> - 循环结束后，用 `total_cnt // n2` 把得到的 `s2` 次数转换成 `str2`（即 `s2` 重复 `n2` 次）的最大个数 `m`。

#### 复杂度  

- **时间复杂度**：`O(|s1| * len(s2) + len(s2)) ≈ O(|s1| * len(s2))`  
  - 实际上我们只遍历 **至多 `len(s2) + 1` 次块**（因为指针状态只有 `len(s2)` 种），每次块要遍历完整的 `s1`，所以总的字符比较是 `|s1| * (len(s2)+1)`。  
  - 与 `n1`（最高 10⁶）无关，算得 **非常快**。  

- **空间复杂度**：`O(len(s2))`  
  - 只保存 `cnt_per、idx_per、seen` 三个长度为 `len(s2)+1` 的数组/字典，最多几百个元素，几乎可以忽略不计。  

相比暴力解，**时间从指数级下降到线性级**，在最坏输入下也能在毫秒级完成。

---

## 心得  

- **核心技巧**：**状态环检测 + 前缀计数**（又称“寻找循环”或“离线 DP”）。  
- **适用的题型**  
  1. “**重复字符串匹配**” 类问题，如 LeetCode 466 `Count The Repetitions`（本题）。  
  2. “**有序序列的循环**” 如 LeetCode 880 `Decoded String at Index`（利用循环跳过）。  
  3. “**无限序列中的第 K 项**” 如 LeetCode 874 `Walking Robot Simulation`（记录状态后快速跳转）。  
- **一句话总结**：**把“大量重复的过程”抽象成“状态 + 迁移”，一旦状态重复就出现环，利用环一次性算出剩余的贡献。**

---

## 反思  

- **第一反应**：直接把 `str1` 拼出来遍历，想当然地认为只要一次遍历就能得到答案。  
- **最容易踩的坑**  
  1. **内存爆炸**：`n1` 达到 10⁶ 时，`s1 * n1` 长度可能高达 10⁸，直接拼串会导致 `MemoryError`。  
  2. **漏掉不可匹配的字符**：如果 `s2` 包含 `s1` 没有的字母，答案必然是 0，提前返回可以省时省力。  
  3. **循环检测的细节**：必须在“块结束后”记录状态，而不是在字符内部，否则可能错过真正的环。  
- **下次遇到同类题**，第一步应该思考：**“这段过程会不会出现重复的状态？”** 若答案是“会”，就立刻尝试**记录状态 + 用数学方式跳过循环**，而不是盲目模拟全部步骤。