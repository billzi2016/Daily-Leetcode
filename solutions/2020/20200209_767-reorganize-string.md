# #767. 重新排列字符串 / Reorganize String

> 难度：中等 · 标签：Hash Table、String、Greedy、Sorting、Heap (Priority Queue)、Counting · [LeetCode 链接](https://leetcode.com/problems/reorganize-string/)

---

## 题目（英文原版）

**Description**

Given a string s, rearrange the characters of s so that any two adjacent characters are not the same.
Return any possible rearrangement of s or return "" if not possible.

**Examples**

**Example 1:**

```
Input: s = "aab"
Output: "aba"
```

**Example 2:**

```
Input: s = "aaab"
Output: ""
```

**Constraints**

- 1 <= s.length <= 500
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，重新排列 `s` 中的字符，使得任意两个相邻字符（adjacent characters）不相同。返回任意一种可能的重新排列结果；如果无法实现，则返回空字符串 `""`。

**示例 1**  
**输入**: `s = "aab"`  
**输出**: `"aba"`

**示例 2**  
**输入**: `s = "aaab"`  
**输出**: `""`

**约束条件**  
- `1 <= s.length <= 500`  
- `s` 只包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把所有字符的排列全部列出来**，然后检查每一种排列是否满足“相邻字符不相同”。  
- **数据结构**：我们可以把字符串看成一个字符数组，使用 Python 的 `itertools.permutations` 来一次产生所有排列。就像把一副扑克牌的所有洗牌方式都列出来，再一个一个去验证。  
- **为什么正确**：只要遍历到了某个满足条件的排列，就一定是题目要求的答案，因为我们已经穷尽了所有可能。  
- **时间/空间复杂度**：  
  - 对长度为 `n` 的字符串，字符的全排列有 `n!`（阶乘）种，随 `n` 增大非常快。  
  - 每检查一次排列需要 O(n) 的时间（遍历字符判断相邻是否相同）。  
  - 所以总时间是 **O(n!·n)**，这在实际中几乎不可接受。  
  - 空间方面，`itertools.permutations` 本身是惰性生成的，只保存当前排列，额外空间是 O(n)。  

> **大白话**：如果你把 10 本书随意排放，可能的排法有 10! = 3,628,800 种；而我们要检查每一种排法，这显然太慢了。

#### 代码（Python）

```python
import itertools

def reorganizeString_brute(s: str) -> str:
    # 把字符串转成列表，方便 permutations 处理
    chars = list(s)
    # 逐个遍历所有排列（每种排列都是一个元组）
    for perm in itertools.permutations(chars):
        # 把元组转回字符串
        candidate = ''.join(perm)
        # 检查相邻字符是否相同
        ok = True
        for i in range(1, len(candidate)):
            if candidate[i] == candidate[i - 1]:
                ok = False
                break
        if ok:                # 找到第一个合法排列直接返回
            return candidate
    # 没有合法排列，返回空串
    return ""
```

#### 复杂度  

- **时间复杂度**：`O(n!·n)` —— `n!` 表示所有排列的数量，乘以 `n` 是因为每次要遍历字符检查相邻。  
- **空间复杂度**：`O(n)` —— 只保存当前遍历的排列，额外的哈希表或数组几乎不需要。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**穷举所有排列是最大的性能瓶颈**。我们需要一种 **只构造合法排列** 的方法，而不是先构造再筛选。

1. **观察**：如果某个字符出现的次数超过了 `(len(s)+1)//2`，那它必然会出现相邻两次——因为即使把它们尽量分散，也没有足够的“空位”来隔开。此时直接返回空串。  
2. **核心想法**：**每次把出现次数最多的字符放在当前结果的最后一个字符的后面**，这样可以最大程度避免相同字符相邻。  
3. **实现手段**：  
   - 用 **计数数组**（长度 26）统计每个小写字母出现的次数。计数数组就像一本“字典”，下标是字母，值是出现次数。  
   - 把所有出现次数>0的字符放进 **最大堆**（priority queue），堆顶永远是出现次数最多的字符。堆的作用类似“抢先队列”，每次都让“最急需”的字符先出来。Python 的 `heapq` 只支持最小堆，我们把次数取负数来实现最大堆。  
   - **贪心过程**：每次弹出堆顶的字符 `c1`（次数最多），如果它和上一次放入结果的字符相同，则弹出第二多的字符 `c2`，先使用 `c2`，再把 `c1`放回堆中。这样保证不会出现相邻相同。  
   - 使用完一个字符后，把它的剩余次数减 1（如果还有剩余，就重新放回堆中）。  
4. **为什么能得到合法排列**：每次都挑出当前**最多**的字符放在后面，它的出现频率已经被尽可能“稀释”。只要最开始的可行性检查通过（最大频率 ≤ (n+1)//2），上述贪心一定能完成整个字符串。  

> **类比**：想象有若干种颜色的球，每种颜色的球数不同。我们每次把数量最多的颜色的球放到一列的末尾，如果这颗球和前一颗颜色相同，就改用第二多的颜色的球来“垫底”。这样可以让颜色交替出现，避免相同颜色相邻。

#### 代码（Python）

```python
import heapq
from collections import Counter

def reorganizeString(s: str) -> str:
    n = len(s)
    # 1. 统计每个字符出现次数
    cnt = Counter(s)                     # Counter 类似哈希表，key 是字符，value 是出现次数
    # 2. 先做可行性检查
    if max(cnt.values()) > (n + 1) // 2:  # 若出现次数太多，直接返回空串
        return ""

    # 3. 构造最大堆（次数取负数实现最大堆）
    # heap 中的元素是 ( -次数, 字符 )
    heap = [(-freq, ch) for ch, freq in cnt.items()]
    heapq.heapify(heap)                  # O(k) 建堆，k 是不同字符种类数，最多 26

    result = []                          # 用列表收集字符，最后 join 成字符串

    # 4. 贪心取字符
    while heap:
        freq1, ch1 = heapq.heappop(heap)  # 取出出现次数最多的字符
        # 如果 result 已有字符且最后一个字符和 ch1 相同，需要换成次多的字符
        if result and result[-1] == ch1:
            # 必须保证堆中还有别的字符，否则说明无解（前面已检查，这里不会发生）
            freq2, ch2 = heapq.heappop(heap)
            result.append(ch2)           # 先放次多的字符
            # 次多字符用掉一次，次数+1（因为是负数），若还有剩余再放回堆
            if freq2 + 1 < 0:
                heapq.heappush(heap, (freq2 + 1, ch2))
            # 把原来的最多字符 ch1 重新放回堆，等待下次使用
            heapq.heappush(heap, (freq1, ch1))
        else:
            # 正常情况，直接放 ch1
            result.append(ch1)
            # 使用一次后次数减 1（负数加 1），若还有剩余则放回堆
            if freq1 + 1 < 0:
                heapq.heappush(heap, (freq1 + 1, ch1))

    return ''.join(result)
```

#### 复杂度  

- **时间复杂度**：`O(n log k)`  
  - `n` 为字符串长度，`k` 为不同字符种类（最多 26），每次从堆中弹出/插入的代价是 `log k`。  
  - 实际上因为 `k ≤ 26`，`log k` 是常数，整体可以视作线性 `O(n)`。  
  - 与暴力解的 `O(n!·n)` 相比，速度提升了 **指数级**。  
- **空间复杂度**：`O(k)`  
  - 计数表和堆共用最多 26 个元素的空间，属于常数级别。  
  - 结果字符串本身需要 `O(n)` 的空间（返回值），这在任何解法中都是必须的。

---

## 心得  

- **核心技巧**：**贪心 + 最大堆**（或计数 + 排序）——每次优先使用出现次数最多的字符，防止它们聚在一起。  
- **适用的题型**：  
  1. **重新排列字符**，要求相邻不相同（如本题）。  
  2. **任务调度**（LeetCode 621 Task Scheduler），把相同任务间隔开。  
  3. **字符串压缩/重排**（如 “最少相邻相同字符的排列”）。  
- **一句话总结**：**把“最多的东西”先放、并在相邻冲突时换成“次多的”，就能把相同字符隔开**。

---

## 反思  

- **第一反应**：想到全排列，直接暴力尝试所有可能。  
- **最容易踩的坑**：  
  - 忽略 **可行性判断**（最大频率是否超过 `(n+1)//2`），导致在极端情况下无限循环或错误返回。  
  - 堆为空时仍尝试弹出第二个元素会报错，需要在代码中保证此情况不会出现。  
  - 对 Python `heapq` 只支持最小堆不熟悉，忘记取负数导致逻辑相反。  
- **下次类似题的第一步**：先 **统计频率并检查上限**，如果满足条件，再使用 **贪心 + 最大堆**（或计数排序）逐步构造答案。这样既能快速判定“不可能”，也能在可能的情况下高效得到合法排列。