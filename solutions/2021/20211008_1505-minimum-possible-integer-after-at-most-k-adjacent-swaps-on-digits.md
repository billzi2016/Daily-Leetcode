# #1505. 最少可能整数（最多 K 次相邻交换） / Minimum Possible Integer After at Most K Adjacent Swaps On Digits

> 难度：困难 · 标签：String、Greedy、Binary Indexed Tree、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/minimum-possible-integer-after-at-most-k-adjacent-swaps-on-digits/)

---

## 题目（英文原版）

**Description**

You are given a string num representing the digits of a very large integer and an integer k. You are allowed to swap any two adjacent digits of the integer at most k times.
Return the minimum integer you can obtain also as a string.

**Examples**

**Example 1:**

```
Input: num = "4321", k = 4
Output: "1342"
Explanation: The steps to obtain the minimum integer from 4321 with 4 adjacent swaps are shown.
```

**Example 2:**

```
Input: num = "100", k = 1
Output: "010"
Explanation: It's ok for the output to have leading zeros, but the input is guaranteed not to have any leading zeros.
```

**Example 3:**

```
Input: num = "36789", k = 1000
Output: "36789"
Explanation: We can keep the number without any swaps.
```

**Constraints**

- 1 <= num.length <= 3 * 104
- num consists of only digits and does not contain leading zeros.
- 1 <= k <= 109

---

## 题目（中文翻译）

给定一个字符串 `num`，表示一个非常大的整数的各位数字，以及一个整数 `k`。你最多可以进行 `k` 次相邻数字的交换（swap any two adjacent digits）。返回在至多 `k` 次相邻交换后能够得到的最小整数，同样以字符串形式返回。

**示例 1**  
**输入**: `num = "4321"`, `k = 4`  
**输出**: `"1342"`  
**解释**: 下面展示了通过 4 次相邻交换将 `4321` 变为最小整数的过程。

**示例 2**  
**输入**: `num = "100"`, `k = 1`  
**输出**: `"010"`  
**解释**: 输出可以包含前导零，尽管输入保证没有前导零。

**示例 3**  
**输入**: `num = "36789"`, `k = 1000`  
**输出**: `"36789"`  
**解释**: 我们可以不进行任何交换，直接保留原数字。

**约束条件**  

- `1 <= num.length <= 3 * 10^4`
- `num` 只包含数字且不含前导零。
- `1 <= k <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从左到右逐个决定该放哪个数字**。  
对当前要填的第 `i` 位（从 0 开始计数），我们只能把原串中 **距离 `i` 不超过 `k` 的数字** 移动到这里，因为每向左移动一次就要消耗一次相邻交换。于是我们在这段窗口里找最小的数字 `min_digit`，把它搬到第 `i` 位，随后把它左边的所有数字向右顺序移动一格（相当于做 `pos - i` 次相邻交换），`k` 减去消耗的次数，继续处理下一个位置。

> **生活化类比**：把数字想成排队的学生，老师只能让相邻的两个人互换位置，最多只能换 `k` 次。要让排在最前面的同学尽量“优秀”（数字小），老师只能在前面 `k` 位学生里挑最小的那位让他走到最前面，其余同学依次往后挤。

**为什么正确**  
因为我们每次都把**能够得到的最小数字**放到当前最高位，这样后面的位数再怎么安排也不会影响已经确定的更高位的大小。换句话说，贪心的局部最优等价于全局最优。

**复杂度分析（大白话）**  
- 对每个位置我们要在长度最多为 `k` 的窗口里找最小值，最坏情况下 `k` 可以和字符串长度 `n` 差不多（`k` 甚至更大），于是每次扫描的代价是 `O(n)`，而我们要遍历 `n` 次，所以时间是 **`O(n²)`**。可以把它想象成“把每个人都和前面所有人比较一次”，随 `n` 增大，工作量会 **平方级增长**。
- 只用了原始字符串和几个计数变量，额外空间是 **`O(1)`**（常数级），不随 `n` 增长。

#### 代码（Python）

```python
def minInteger_bruteforce(num: str, k: int) -> str:
    # 把字符串转成列表，方便原地修改
    nums = list(num)
    n = len(nums)

    for i in range(n):
        # 在 i~i+k 的窗口里找最小的数字及其位置
        # 注意窗口右边界不能超过 n
        end = min(n - 1, i + k)
        # 记录最小数字和对应的下标
        min_digit = nums[i]
        min_pos = i
        for j in range(i + 1, end + 1):
            if nums[j] < min_digit:      # 发现更小的数字
                min_digit = nums[j]
                min_pos = j

        # 把最小数字搬到位置 i，期间的每一次相邻交换都要消耗一次 k
        # 这里直接用 Python 的切片实现“把 min_pos 的元素左移到 i”
        while min_pos > i:
            nums[min_pos], nums[min_pos - 1] = nums[min_pos - 1], nums[min_pos]
            min_pos -= 1
            k -= 1                     # 用掉一次交换次数
            if k == 0:                 # 已经没有剩余交换次数，直接返回
                return ''.join(nums)

        if k == 0:                     # 这一步也可能已经用完 k
            break

    return ''.join(nums)
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  想象 `n = 10,000` 时，程序要做大约一亿次比较，显然会超时。
- **空间复杂度**：`O(1)`（不计输入本身）  
  只用了几个临时变量和一个字符列表。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次都要在窗口里线性扫描寻找最小值，并且在搬运时要把中间的所有字符逐个交换，导致 `O(n²)`。我们可以把这两个过程都 **用数据结构加速**：

1. **快速定位最小数字**  
   - 由于数字只有 `'0'`~`'9'` 共 10 种，我们可以提前把每种数字出现的下标全部存进 10 个队列（`deque`），这样在需要找最小数字时，只需要从 `'0'` 开始逐个检查对应队列的**第一个下标**是否在可达范围内。

2. **快速计算真实需要的交换次数**  
   - 假设我们想把下标为 `pos` 的数字搬到当前位置 `i`。如果之前已经把若干个数字搬走（即从原串中删除），这些已删除的数字会“缩短”实际的距离。  
   - 设 `removed_before(pos)` 为 **在 `pos` 左侧已经被删除的数字个数**，则真实需要的相邻交换次数 = `(pos - i) - removed_before(pos)`.  
   - 维护 `removed_before` 可以使用 **树状数组（Binary Indexed Tree, BIT）**，它支持 “在某个位置加 1” 与 “前缀和查询” 都是 `O(log n)`，非常适合这里的需求。  
   - 类比：想象一排座位，已经有人站起来离开了，想知道第 `pos` 个人前面还有多少座位是空的，就可以用 BIT 快速累计。

3. **贪心选择**  
   - 对每个目标位置 `i`（从左到右），遍历数字 `'0'`~`'9'`，找到第一个满足 `effective_distance ≤ k` 的数字。把它放到答案里，更新 BIT（标记该下标已被删除），`k` 减去实际消耗的交换次数，继续下一个位置。  
   - 当 `k` 用完或已经遍历完所有字符时，直接把剩余未删除的字符按原顺序拼接到答案后面即可。

**为什么正确**  
- 仍然是把**当前能搬到最左的最小数字**放在当前位置，和暴力解的贪心策略一致，只是用更快的方式判断“能否搬到”。  
- BIT 确保我们在考虑已删除的数字后，计算出的交换次数是 **实际需要的**，不会因为之前的搬动而多算或少算。  
- 由于我们始终选择最小可达数字，后面的选择不可能影响已经确定的更高位的大小，整个过程得到的字符串必然是字典序最小的，也就是题目要求的最小整数。

#### 代码（Python）

```python
from collections import deque
from typing import List

class BIT:
    """树状数组（Fenwick Tree），1-indexed"""
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx: int, delta: int):
        """在位置 idx（0-indexed）上加 delta"""
        i = idx + 1                 # 转成 1-indexed
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def sum(self, idx: int) -> int:
        """返回前缀和，求 [0, idx]（0-indexed）之间的累计值"""
        i = idx + 1
        res = 0
        while i > 0:
            res += self.bit[i]
            i -= i & -i
        return res

    def prefix(self, idx: int) -> int:
        """同 sum，写个更语义化的名字"""
        return self.sum(idx)

def minInteger(num: str, k: int) -> str:
    n = len(num)
    # 1. 把每个数字出现的位置放进对应的队列
    pos_queues: List[deque] = [deque() for _ in range(10)]
    for idx, ch in enumerate(num):
        pos_queues[int(ch)].append(idx)

    bit = BIT(n)          # 用来记录已经被“删除”的位置
    answer = []           # 最终结果的字符列表
    cur = 0               # 当前要填的目标位置

    while cur < n and k > 0:
        # 2. 从 0~9 按升序尝试找可以搬来的最小数字
        for d in range(10):
            if not pos_queues[d]:
                continue
            orig_idx = pos_queues[d][0]          # 该数字最左侧的原始下标
            # 已经被删除的数量 = BIT 前缀和
            removed_before = bit.prefix(orig_idx)
            # 实际需要的交换次数 = (orig_idx - cur) - removed_before
            need = (orig_idx - cur) - removed_before
            if need <= k:                         # 能搬到这里
                # 3. 选定，写入答案
                answer.append(str(d))
                k -= need                         # 消耗 k
                # 4. 在 BIT 中标记该位置已被删除
                bit.add(orig_idx, 1)
                # 5. 弹出队列头部
                pos_queues[d].popleft()
                cur += 1
                break        # 进入下一个目标位置
        else:
            # 所有数字都无法在剩余 k 内搬到 cur，直接结束循环
            break

    # 6. 把剩余未删除的字符按原顺序追加到答案后面
    # 这一步可以直接遍历原字符串，判断该位置是否已被删除（BIT 前缀差值）
    for i in range(n):
        # 若该位置已经在 BIT 中被标记为 1，则说明已被取走
        if bit.prefix(i) - bit.prefix(i - 1 if i > 0 else -1) == 0:
            answer.append(num[i])

    return ''.join(answer)
```

> **代码要点注释**  
> - `BIT.add(idx, 1)` 表示把位置 `idx` 标记为 “已删除”。  
> - `removed_before = bit.prefix(orig_idx)` 返回 `orig_idx` 左侧已经删除的元素个数。  
> - `need = (orig_idx - cur) - removed_before` 就是**真实需要的相邻交换次数**。  
> - 当 `need > k` 时，说明即使把该数字搬到最左也会超出允许的交换次数，只能尝试更大的数字。  

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 每个字符最多被弹出一次（`O(1)`），  
  - 对每个目标位置我们最多检查 10 次数字（常数），  
  - `BIT` 的 `add` 与 `prefix` 均是 `O(log n)`，所以整体是 `n` 次 `log n` 级操作。  
  - 与暴力解的 `O(n²)` 相比，**当 `n` 达到几万时，速度提升了数十倍甚至上百倍**。

- **空间复杂度**：`O(n)`  
  - 需要存放 10 个队列（总共 `n` 个下标）和一个长度为 `n+1` 的 BIT。  
  - 这在题目允许的 `3·10⁴` 规模下完全可以接受。

---

## 心得

- **核心技巧**：**贪心 + 树状数组**（或线段树）实现“在限制次数内把最小元素搬到最左”。  
- **适用的题型**  
  1. “在 K 次相邻交换内使字符串/数组字典序最小”——如本题、`Minimum Adjacent Swaps to Make Palindrome`（需要把字符搬到对应位置）。  
  2. “在 K 次操作内把数组/序列变为非递减序列”——可以同样用队列+BIT 计算真实距离。  
- **一句话总结**：**把“能搬到的最小数字”放到最左，利用 BIT 快速知道已经搬走了多少，避免逐个模拟交换**。

---

## 反思

- **第一反应**：看到“相邻交换”，立刻想到**滑动窗口**或**冒泡**，于是写了暴力的“窗口内找最小、逐位交换”实现。  
- **最容易踩的坑**  
  1. **交换次数的真实计数**：直接用 `pos - i` 会忽略已经被删掉的数字，导致消耗的 `k` 计算错误。  
  2. **前缀和查询的边界**：在 BIT 中查询 `i-1` 时要防止负索引。  
  3. **大 `k` 超出窗口**：`k` 可能远大于 `n`，窗口大小实际上是受剩余未处理字符数的限制，而不是 `k` 本身。  
- **下次类似题的第一步**：**把问题抽象为“在限定步数内，把某个位置的元素搬到前面”，先想如何快速判断“能否搬到”，再决定使用什么数据结构（BIT / 线段树）来维护已搬走的元素**。