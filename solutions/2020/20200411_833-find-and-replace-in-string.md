# #833. 在字符串中查找并替换 / Find And Replace in String

> 难度：中等 · 标签：Array、Hash Table、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/find-and-replace-in-string/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string s that you must perform k replacement operations on. The replacement operations are given as three 0-indexed parallel arrays, indices, sources, and targets, all of length k.
To complete the ith replacement operation:
For example, if s = "abcd", indices[i] = 0, sources[i] = "ab", and targets[i] = "eee", then the result of this replacement will be "eeecd".
All replacement operations must occur simultaneously, meaning the replacement operations should not affect the indexing of each other. The testcases will be generated such that the replacements will not overlap.
Return the resulting string after performing all replacement operations on s.
A substring is a contiguous sequence of characters in a string.

**Examples**

**Example 1:**

```
Input: s = "abcd", indices = [0, 2], sources = ["a", "cd"], targets = ["eee", "ffff"]
Output: "eeebffff"
Explanation:
"a" occurs at index 0 in s, so we replace it with "eee".
"cd" occurs at index 2 in s, so we replace it with "ffff".
```

**Example 2:**

```
Input: s = "abcd", indices = [0, 2], sources = ["ab","ec"], targets = ["eee","ffff"]
Output: "eeecd"
Explanation:
"ab" occurs at index 0 in s, so we replace it with "eee".
"ec" does not occur at index 2 in s, so we do nothing.
```

**Constraints**

- 1 <= s.length <= 1000
- k == indices.length == sources.length == targets.length
- 1 <= k <= 100
- 0 <= indexes[i] < s.length
- 1 <= sources[i].length, targets[i].length <= 50
- s consists of only lowercase English letters.
- sources[i] and targets[i] consist of only lowercase English letters.

---

## 题目（中文翻译）

给定一个 0 索引的字符串 `s`，需要对其执行 `k` 次替换操作（replacement operations）。这些操作由三个等长的 0 索引平行数组 `indices`、`sources` 和 `targets`（长度均为 `k`）描述。

完成第 `i` 次替换操作的步骤如下：

1. 检查 `sources[i]` 是否恰好出现在 `s` 的下标 `indices[i]` 处。  
2. 若匹配成功，则用 `targets[i]` 替换该子串（substring），即将 `s[indices[i] … indices[i] + len(sources[i]) - 1]` 替换为 `targets[i]`。  
3. 若不匹配，则保持原样，不做任何修改。

所有替换操作必须 **同时**（simultaneously）进行，这意味着一次替换的结果不会影响其他替换的索引。题目保证给出的替换不会相互重叠。

返回在完成所有替换操作后得到的字符串。

**子串（substring）** 是指字符串中连续的一段字符序列。

### 示例

**示例 1**  
```text
Input: s = "abcd", indices = [0, 2], sources = ["a", "cd"], targets = ["eee", "ffff"]
Output: "eeebffff"
Explanation:
"a" 出现在下标 0 处，所以用 "eee" 替换它。
"cd" 出现在下标 2 处，所以用 "ffff" 替换它。
```

**示例 2**  
```text
Input: s = "abcd", indices = [0, 2], sources = ["ab","ec"], targets = ["eee","ffff"]
Output: "eeecd"
Explanation:
"ab" 出现在下标 0 处，所以用 "eee" 替换它。
"ec" 并未出现在下标 2 处，因此不做任何操作。
```

### 约束条件

- `1 <= s.length <= 1000`
- `k == indices.length == sources.length == targets.length`
- `1 <= k <= 100`
- `0 <= indices[i] < s.length`
- `1 <= sources[i].length, targets[i].length <= 50`
- `s` 仅由小写英文字母组成
- `sources[i]` 与 `targets[i]` 仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把每一次替换单独处理。  
- **遍历每个操作** `i`（从 `0` 到 `k‑1`），检查 `s` 的第 `indices[i]` 位起的子串是否等于 `sources[i]`。  
- 如果相等，就把这段子串直接替换成 `targets[i]`，否则什么也不做。  

这里可以把 `s` 看成一本书，`indices[i]` 是要查找的页码，`sources[i]` 是页码对应的章节标题，只有标题匹配才把章节内容换成 `targets[i]`。  
因为题目保证所有替换不会相互覆盖（不会出现两个操作的范围重叠），所以我们可以**一次性**对原字符串进行多次“就地”替换，而不必担心前一次的替换会影响后一次的索引。

**为什么正确**  
- 每一次检查都严格对照原字符串 `s` 的对应位置，若不匹配则保持原样。  
- 所有操作的范围互不重叠，直接把匹配成功的子串换成目标子串，最终得到的字符串必然是题目要求的“同时完成的”结果。

**复杂度分析（大白话）**  
- 对每个操作我们最多要比较 `sources[i]` 的长度个字符。最坏情况是 `k` 次操作每个 `source` 都长 `L`（`L ≤ 50`），于是比较次数是 `k·L`，这在 100 × 50 = 5000 次左右，完全可以接受。  
- 时间复杂度记作 **O(k·L)**，意思是“随操作数量和每个 source 长度线性增长”。  
- 我们在原字符串上直接构造新字符串，只用了几个额外的变量，空间复杂度是 **O(1)**（不计结果字符串本身的空间）。

#### 代码（Python）

```python
def findReplaceString_bruteforce(s: str, indices, sources, targets):
    # 把字符串转成列表，方便原地修改字符
    s_list = list(s)

    for idx, src, tgt in zip(indices, sources, targets):
        # 检查 s 中 idx 位置起的子串是否等于 src
        if s[idx:idx + len(src)] == src:          # 这里直接切片比较
            # 匹配成功就用 target 替换
            # 先把原来的子串清空（用空字符填充），再插入 target
            s_list[idx:idx + len(src)] = list(tgt)

    # 列表转回字符串即为答案
    return ''.join(s_list)
```

#### 复杂度

- **时间复杂度**：`O(k·L)` — 需要对每个操作检查最多 `L`（source 长度）个字符。  
- **空间复杂度**：`O(1)` — 只用了常数个额外变量（结果字符串本身的空间不计入）。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**每次都要对原字符串切片**，这在 Python 中会产生临时子串对象，稍显浪费。  
我们可以把所有替换信息先**整理成一个映射**（哈希表），然后一次遍历原字符串 `s`，在遍历过程中决定是保留原字符还是输出目标子串。

**步骤拆解**  

1. **建立哈希表**  
   - 用 `index → (source, target)` 的映射把每一次操作存起来。  
   - 哈希表就像一本**查字典**，键是页码（`indices[i]`），值是“如果这里的章节标题是 `source`，就换成 `target`”。  

2. **按顺序遍历原字符串**（双指针思路）  
   - 用指针 `i` 从左到右扫描 `s`。  
   - 若 `i` 在哈希表里，说明这里可能有一次替换。  
     - 检查 `s[i:i+len(source)]` 是否真的等于 `source`。  
     - 若匹配，向答案里直接追加 `target`，并把指针 `i` 前进 `len(source)`（跳过已经被替换的部分）。  
     - 若不匹配，只把 `s[i]` 加入答案，指针前进一步。  
   - 若 `i` 不在哈希表里，说明这里没有任何替换，直接把 `s[i]` 加入答案并前进一步。  

3. **一次遍历结束**，得到的答案即为所有替换“同步”完成的结果。

**为什么快**  
- 只遍历一次 `s`（长度 `n`），每个字符最多检查一次对应的 `source`（长度 ≤ 50），所以总体是线性时间。  
- 哈希表的查询是 **O(1)**，相当于“随手在字典里找页码”。  

**复杂度分析（通俗解释）**  
- 时间复杂度 **O(n + Σ|source|)**，这里 `n` 是原字符串的长度，`Σ|source|` 是所有 `source` 长度之和。可以把它想成“阅读原书一次 + 读几遍小章节标题”，整体仍然是线性增长。  
- 空间复杂度 **O(k)**，因为我们只额外存了 `k` 条映射信息（相当于把几页索引记录下来）。

#### 代码（Python）

```python
def findReplaceString_optimal(s: str, indices, sources, targets):
    """
    最优解：一次遍历 + 哈希表
    """
    # 1. 把所有替换信息放进哈希表，键是起始下标，值是 (source, target)
    replace_map = {idx: (src, tgt) for idx, src, tgt in zip(indices, sources, targets)}

    i = 0                 # 指针，遍历原字符串
    n = len(s)
    result = []           # 用列表收集字符，最后 join 成字符串

    while i < n:
        if i in replace_map:
            src, tgt = replace_map[i]
            # 检查 s 从 i 开始的子串是否匹配 src
            if s.startswith(src, i):   # 等价于 s[i:i+len(src)] == src，但更高效
                result.append(tgt)     # 匹配成功，直接写入 target
                i += len(src)           # 跳过被替换的源子串
                continue                # 进入下一轮循环
        # 没有匹配的替换，或者当前位置不在 replace_map 中
        result.append(s[i])
        i += 1

    return ''.join(result)
```

#### 复杂度

- **时间复杂度**：`O(n + Σ|source|)` — 只遍历一次原字符串 `s`（长度 `n`），每次检查的子串长度总和不超过所有 `source` 的长度之和。相比暴力的 `O(k·L)`，在 `k` 较大时更省时。  
- **空间复杂度**：`O(k)` — 额外的哈希表保存 `k` 条映射信息（不计结果字符串本身）。

---

## 心得

- **核心技巧**：把所有“可能的替换”先记录在哈希表里，然后一次线性扫描原字符串决定使用原字符还是目标子串。  
- **适用场景**：  
  1. 多次“找子串并替换”，且替换位置互不冲突（如 LeetCode 833 “Find And Replace in String”）。  
  2. “区间标记”类问题，需要一次遍历完成所有标记的合并（如 LeetCode 920 “Number of Music Playlists” 的前缀和做法）。  
  3. “字符串拼接”时需要依据若干固定位置进行不同的拼接（如 LeetCode 1190 “Reverse Substrings Within Each Word” 的分段处理）。  
- **一句话总结**：**先把替换信息索引化，再一趟扫描完成所有替换**。

---

## 反思

- **第一反应**：看到“所有替换同时进行且不重叠”，立刻想到把每个替换的位置记录下来，然后一次性遍历原字符串。  
- **最容易踩的坑**：  
  - 忘记检查 `source` 是否真的出现在对应下标，直接替换会导致错误（例子 2 中的 “ec”）。  
  - 替换后忘记跳过原 `source` 的长度，导致重复读取已被替换的字符。  
  - `indices` 未排序时直接按顺序遍历可能导致遗漏，需要用哈希表或先排序。  
- **下次类似题的第一步**：先**构建下标 → 替换信息的映射**，确认每个位置是否真的匹配，再决定是否替换。这样可以避免索引混乱，保证一次遍历完成。