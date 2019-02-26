# #316. 删除重复字母 / Remove Duplicate Letters

> 难度：中等 · 标签：String、Stack、Greedy、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/remove-duplicate-letters/)

---

## 题目（英文原版）

**Description**

Given a string s, remove duplicate letters so that every letter appears once and only once. You must make sure your result is the smallest in lexicographical order among all possible results.
Note: This question is the same as 1081: https://leetcode.com/problems/smallest-subsequence-of-distinct-characters/

**Examples**

**Example 1:**

```
Input: s = "bcabc"
Output: "abc"
```

**Example 2:**

```
Input: s = "cbacdcbc"
Output: "acdb"
```

**Constraints**

- 1 <= s.length <= 104
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，删除其中的重复字母，使得每个字母只出现一次且仅出现一次。必须保证在所有可能的结果中，你得到的字符串在字典序（lexicographical order）上是最小的。

**示例 1：**  
（题目正文中未给出具体示例，可参考下方示例）

**示例 2：**  
（题目正文中未给出具体示例，可参考下方示例）

**注意：** 本题与 1081 题相同，链接：https://leetcode.com/problems/smallest-subsequence-of-distinct-characters/

### 示例

**示例 1**  
```text
Input: s = "bcabc"
Output: "abc"
```

**示例 2**  
```text
Input: s = "cbacdcbc"
Output: "acdb"
```

### 约束条件

- `1 <= s.length <= 10^4`
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有出现过的字符挑出来，枚举所有可能的排列，然后挑选字典序最小的那一个**。  
- **数据结构**：我们可以用 `list` 保存字符，用 `set` 去重（相当于把字典里只保留不重复的词）。  
- **为什么正确**：题目要求“每个字母只出现一次”，所以只要把出现过的字母全部取出，所有合法答案必然是这些字母的某一种排列。遍历所有排列并比较字典序，最小的那个自然就是答案。  
- **时间/空间分析**：  
  - 若字符串中出现了 `k` 种不同字符（`k ≤ 26`），所有排列的数量是 `k!`（阶乘），随 `k` 增长非常快。  
  - 对每个排列我们都要检查它在原字符串中是否保持相对顺序（即是否是一个合法子序列），这需要 O(n) 的扫描。  
  - 因此总体时间复杂度是 **O(k! · n)**，在最坏情况下（`k = 26`）几乎不可能在 1 秒内跑完。  
  - 额外的空间主要是保存排列的临时列表，最多 O(k)。

> **大白话**：  
> O(k!·n) 就像把 26 本书全部排成所有可能的顺序，然后每一种顺序都去书架上找一遍，显然太慢了。

#### 代码（Python）

```python
import itertools

def removeDuplicateLetters_bruteforce(s: str) -> str:
    # 1. 统计出现过的字符，去重后转成列表（相当于字典的“词条”）
    distinct = sorted(set(s))               # 按字典序排序，方便后面比较

    best = None                               # 用来记录当前最小的合法答案

    # 2. 枚举所有字符的排列（全排列）
    for perm in itertools.permutations(distinct):
        # 3. 把元组转成字符串
        candidate = ''.join(perm)

        # 4. 检查 candidate 是否是 s 的子序列（相对顺序不变）
        i = 0                                 # 在 s 中的指针
        for ch in candidate:
            # 在 s 中向后找 ch
            while i < len(s) and s[i] != ch:
                i += 1
            if i == len(s):                  # 没找到，说明不是合法子序列
                break
            i += 1                             # 找到后继续向后搜
        else:
            # 循环正常结束，说明 candidate 合法
            if best is None or candidate < best:   # 字典序比较
                best = candidate

    return best if best is not None else ''
```

> **关键行解释**  
> - `set(s)`：像查字典一样把所有出现的字母收集起来，去掉重复。  
> - `itertools.permutations(distinct)`：生成所有可能的排列，相当于把这些字母全部排成不同的顺序。  
> - 子序列检查循环：模拟在原串里“顺序寻找”，确保相对位置不被破坏。  

#### 复杂度

- **时间复杂度**：`O(k! · n)`  
  - `k!` 表示所有排列的数量，`n` 是原字符串长度。  
  - 当 `k` 较大时（比如 20 以上），阶乘的增长速度远快于线性或平方，实际不可接受。  
- **空间复杂度**：`O(k)`  
  - 只需要保存去重后的字符集合和当前排列的临时空间。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有排列**。我们需要在遍历字符串一次的过程中，就直接构造出字典序最小的合法子序列。  
这类 “一次遍历、随时决定是否保留” 的问题，**单调栈 + 贪心** 是常用技巧。下面一步步推导：

1. **先统计每个字符最后出现的位置**  
   - 只要我们知道从当前位置往后还能看到哪些字符，就能判断“现在不放这个字符会不会导致后面缺失”。  
   - 用一个长度为 26 的数组 `last[idx]`（`idx = ord(ch)-97`）记录每个字母最后一次出现的下标。  

2. **维护一个递增（单调）栈**  
   - 栈里保存已经决定加入答案的字符，栈顶字符 **应该是当前已经得到的最小字典序**。  
   - 当我们遍历到字符 `c` 时，有三种情况：
     - **已经在栈里**：说明我们已经选过 `c`，直接跳过（因为每个字符只能出现一次）。  
     - **栈不为空且栈顶字符 > c**：这时如果栈顶字符在后面还能再出现（`i < last[top]`），我们可以把栈顶弹出，让 `c` 更早进入，得到更小的字典序。  
     - **否则**：把 `c` 推入栈中。  

3. **为什么这样不会错？**  
   - **贪心**：每一步都尽可能让当前字符变小，只要后面还能补回被弹出的字符，就不会影响最终能否得到所有不同字母。  
   - **单调**：栈始终保持字典序递增（从栈底到栈顶），这样弹出后重新压入的字符必然比之前的更小，保证整体最小。  

4. **最终答案**  
   - 遍历结束后，栈中从底到顶的字符就是要求的最小字典序子序列。  

> **类比**：把栈想象成装书的书架，书要按字母顺序摆放。遇到一本更靠前的书（字母更小）时，如果已经在书架上方的书以后还能再拿到（后面还会出现），就把上面的书先搬走，让这本书先上架，这样书架最终就是字典序最小的排列。

#### 代码（Python）

```python
def removeDuplicateLetters(s: str) -> str:
    # 1. 统计每个字符最后出现的位置
    last = {ch: i for i, ch in enumerate(s)}   # 字典：字符 -> 最后下标

    stack = []          # 用 list 当栈，栈底在左边，栈顶在右边
    in_stack = set()    # 记录哪些字符已经在栈中，防止重复

    for i, ch in enumerate(s):
        # 2. 如果已经在栈里，就跳过（每个字符只能出现一次）
        if ch in in_stack:
            continue

        # 3. 贪心弹出比当前字符大的栈顶字符（前提是后面还能再出现）
        while stack and ch < stack[-1] and i < last[stack[-1]]:
            removed = stack.pop()          # 弹出
            in_stack.remove(removed)       # 同时把标记删掉

        # 4. 把当前字符压入栈
        stack.append(ch)
        in_stack.add(ch)

    # 5. 栈中字符顺序即为答案
    return ''.join(stack)
```

> **关键行解释**  
> - `last = {ch: i for i, ch in enumerate(s)}`：相当于给每个字母贴上“最远的标签”，帮助我们判断后面还能不能再见到它。  
> - `while stack and ch < stack[-1] and i < last[stack[-1]]:`：只在“当前字符更小且栈顶字符还能再出现”时才弹出，保证不会把必需的字符提前丢掉。  
> - `in_stack`：像一本登记册，记录哪些字母已经“上架”，防止重复上架。  

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个字符最多被压栈一次、弹出一次，整个过程是线性扫描。  
  - 与暴力解的 `O(k!·n)` 相比，省去了所有排列的枚举，速度快了几百倍以上。  

- **空间复杂度**：`O(1)`（实际上是 `O(26)`）  
  - 只用了常数级的额外结构：`last`（最多 26 条记录）、栈（最多 26 个字符）和 `in_stack`。  
  - 与输入长度无关，始终保持在很小的范围。  

---

## 心得

- **核心技巧**：**单调栈 + 贪心**。在遍历过程中“随时决定是否保留”，并利用“后面还能出现”这一信息保证不会错过必需字符。  
- **适用题型**：  
  1. **单调栈求最小字典序子序列**（如本题、LeetCode 1081 “Smallest Subsequence of Distinct Characters”）。  
  2. **找出每个窗口的最小/最大值**（滑动窗口最大值/最小值）。  
  3. **删除字符使得结果字典序最小**（如 “Remove K Digits”）。  
- **一句话总结**：**“只要后面还能补回，就大胆把当前大的字符弹出，让更小的字符抢先上阵”。**

---

## 反思

- **第一反应**：看到“去重且字典序最小”，立刻想到“全排列”或“回溯”，因为这样最直接能满足“所有可能”。  
- **最容易踩的坑**：  
  - 忘记判断 **“后面还能出现吗”**，导致弹出后再也找不到对应字符，答案不完整。  
  - 没有使用 `in_stack` 去重，导致同一个字符被多次压入栈，破坏“一次出现”。  
  - 对空字符串或全相同字符的边界没有考虑（本题约束 `1 ≤ len(s)`，但实现仍需稳健）。  
- **下次第一步**：先 **统计每个字符的出现区间（尤其是最后位置）**，再决定使用 **单调栈** 进行贪心构造。这样思路更清晰，避免盲目枚举。