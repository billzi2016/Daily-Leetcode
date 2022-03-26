# #1718. 构造字典序最大的合法序列 / Construct the Lexicographically Largest Valid Sequence

> 难度：中等 · 标签：Array、Backtracking · [LeetCode 链接](https://leetcode.com/problems/construct-the-lexicographically-largest-valid-sequence/)

---

## 题目（英文原版）

**Description**

Given an integer n, find a sequence with elements in the range [1, n] that satisfies all of the following:
The distance between two numbers on the sequence, a[i] and a[j], is the absolute difference of their indices, |j - i|.
Return the lexicographically largest sequence. It is guaranteed that under the given constraints, there is always a solution.
A sequence a is lexicographically larger than a sequence b (of the same length) if in the first position where a and b differ, sequence a has a number greater than the corresponding number in b. For example, [0,1,9,0] is lexicographically larger than [0,1,5,6] because the first position they differ is at the third number, and 9 is greater than 5.

**Examples**

**Example 1:**

```
Input: n = 3
Output: [3,1,2,3,2]
Explanation: [2,3,2,1,3] is also a valid sequence, but [3,1,2,3,2] is the lexicographically largest valid sequence.
```

**Example 2:**

```
Input: n = 5
Output: [5,3,1,4,3,5,2,4,2]
```

**Constraints**

- 1 <= n <= 20

---

## 题目（中文翻译）

给定整数 `n`，找一条元素取值范围为 `[1, n]` 的序列，使其满足以下所有条件：

- 序列中任意两个数 `a[i]` 与 `a[j]` 的距离（distance）定义为它们下标的绝对差，即 `|j - i|`。
- 返回字典序（lexicographically）最大的序列。题目保证在给定约束下必定存在解。

**字典序比较**  
长度相同的序列 `a` 与序列 `b`，若在首个不同位置上 `a` 的对应元素大于 `b` 的对应元素，则称 `a` 的字典序大于 `b`。例如 `[0,1,9,0]` 的字典序大于 `[0,1,5,6]`，因为它们在第三个位置不同，且 `9 > 5`。

---

### 示例

#### 示例 1
**输入**  
``` 
n = 3
```  
**输出**  
```
[3,1,2,3,2]
```  
**解释**  
`[2,3,2,1,3]` 也是一个合法序列，但 `[3,1,2,3,2]` 的字典序更大，是满足条件的字典序最大的序列。

#### 示例 2
**输入**  
``` 
n = 5
```  
**输出**  
```
[5,3,1,4,3,5,2,4,2]
```  

---

### 约束条件
- `1 <= n <= 20`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的序列都枚举出来**，然后挑出满足条件且字典序最大的那一个。  
具体步骤可以想象成：

1. 把长度为 `2·n-1` 的空盒子排成一排。  
2. 把数字 `1 … n` 按任意顺序放进去（可以出现一次或两次），把所有可能的放法都列出来。  
3. 检查每个序列：  
   - 对于每个数字 `i > 1`，它必须恰好出现 **两次**，且这两次出现的下标差正好等于 `i`（下标差就是两次出现之间的距离）。  
   - 对于数字 `1`，只需要出现 **一次**（因为 `|j-i| = 0`），它自然满足条件。  
4. 把所有合法序列按“字典序”排序，取最大的那个。

> **类比**：把序列想象成一本词典，每个序列是一行文字。要找“字典序最大的”，就像在词典里找最后一页的内容。

**为什么这个方法一定能得到答案**  
因为我们把**所有**满足题目要求的序列都列举出来，最好的那一个必然在其中。只要我们没有漏掉任何合法序列，答案就一定会被挑选出来。

**复杂度分析（大白话）**  

- 枚举所有序列的数量是指数级的：  
  长度为 `2·n-1`，每个位置可以放 `1 … n` 中的任意数字，理论上有 `n^(2n-1)` 种组合。  
  对于 `n=10` 已经是 `10^19`，根本不可能在电脑里跑完。  
- 检查每个序列是否满足条件需要遍历一次序列，时间是 `O(n)`。  
- 所以总的时间复杂度是 **O(n * n^(2n-1))**，这在实际中是不可接受的。  
- 空间上我们只需要存放当前正在检查的序列，空间复杂度是 **O(n)**。

> **结论**：暴力枚举能帮助我们理清“合法序列到底长什么样”，但在真实面试或线上评测里根本用不了。

#### 代码（Python）

```python
import itertools

def brute_largest_sequence(n: int):
    """仅用于 n 很小（比如 n<=4）时的演示，暴力枚举所有序列"""
    length = 2 * n - 1               # 序列总长度
    best = None                      # 用来保存字典序最大的合法序列

    # 这里直接枚举所有可能的填法（非常慢，只适合演示）
    for seq in itertools.product(range(1, n + 1), repeat=length):
        if is_valid(seq, n):
            if best is None or seq > best:   # Python 的元组比较就是字典序比较
                best = seq
    return list(best) if best else []

def is_valid(seq, n):
    """检查 seq 是否满足题目条件"""
    pos = {}                         # 记录每个数字出现的位置列表
    for idx, val in enumerate(seq):
        pos.setdefault(val, []).append(idx)

    # 1 必须出现一次，2..n 必须出现两次，且距离要等于数字本身
    for i in range(1, n + 1):
        occ = pos.get(i, [])
        if i == 1:
            if len(occ) != 1:
                return False
        else:
            if len(occ) != 2:
                return False
            if abs(occ[0] - occ[1]) != i:   # 距离必须等于 i
                return False
    return True

# 示例（仅能跑极小的 n）
print(brute_largest_sequence(3))   # 输出可能是 [3,1,2,3,2]
```

> **注意**：代码里每一行都加了中文注释，帮助你快速看懂每一步的意义。

#### 复杂度

- **时间复杂度**：`O(n * n^(2n-1))` —— 组合数的指数增长，实际不可用。  
- **空间复杂度**：`O(n)` —— 只存放当前序列和辅助的哈希表。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举顺序**是关键：我们不需要遍历所有可能，只要**按字典序从大到小的顺序尝试**，一旦找到合法序列就一定是答案。  
这正好可以用 **回溯（Backtracking）** 来实现：

1. **序列长度**是 `2·n-1`，用一个数组 `ans`（全部填 `0`）来表示。  
2. **从左到右**寻找第一个还没有填的下标 `i`（这一步保证我们总是先决定左边的字符，左边的字符越大，整体字典序越大）。  
3. **尝试放最大的数字**：从 `n` 递减到 `1`，依次尝试把数字 `num` 放在位置 `i`（以及满足距离条件的另一位置）。  
   - 对于 `num > 1`，它必须出现 **两次**，且两次下标差恰好等于 `num`。  
     - 所以如果我们把 `num` 放在 `i`，另一位置必须是 `i + num`（因为 `| (i+num) - i | = num`）。  
     - 两个位置都必须在数组范围内且当前为空。  
   - 对于 `num == 1`，只需要放一次（因为距离为 `0`），只要当前位置空即可。  
4. **标记已使用**：使用一个布尔数组 `used[1..n]`（`True` 表示已经放过）来避免同一个数字被放多次。  
5. **递归**：放下 `num` 以后，继续递归处理下一个空位。  
6. **剪枝**：如果在某一步找不到合法的放置位置，就立刻返回上一步，尝试更小的数字。  
7. **终止条件**：当所有位置都被填满（即 `i == len(ans)`），说明已经得到一个合法序列，直接返回。因为我们是**从大到小**尝试的，第一次完整填满的序列必然是字典序最大的。

> **核心概念解释**  
> - **回溯**：把“尝试 + 撤销”写成递归的过程，类似在迷宫里走路：走一步、如果走不通就回头再选另一条路。  
> - **字典序**：先比较第一个位置的数，谁大谁就更大；如果相同再比较第二个位置，以此类推。因为我们总是**先决定左边**，左边的数越大，整体序列就越大。  
> - **距离条件**：数字 `k` 的两次出现之间恰好相隔 `k` 个位置（下标差 = k），这就像把两块相同的拼图板卡在一起，板卡之间必须留出恰好 `k` 格的空位。

**为什么这样比暴力快**  

- 暴力是**盲目枚举**所有可能，时间指数爆炸。  
- 回溯**按顺序尝试**，每一步只尝试 `n` 种数字（最多 20），并且一旦发现冲突就立即回退，不会继续无意义的搜索。  
- 再加上“从大到小”尝试，**第一条完整路径**就是答案，后面的搜索根本不需要进行。

**复杂度估算（大白话）**  

- 最坏情况下我们仍然可能遍历所有合法的放置方式，但合法方式的数量远远小于 `n^(2n-1)`，大约是 `O(n!)` 级别（因为每个数字只放一次或两次）。  
- 对于 `n ≤ 20`，回溯在几毫秒到几百毫秒内就能结束，完全满足 LeetCode 的时间限制。  
- 空间上我们只保存 `ans`（长度 `2n-1`）和 `used`（长度 `n+1`）以及递归栈，都是 **O(n)**。

#### 代码（Python）

```python
def construct_largest_sequence(n: int):
    """
    返回字典序最大的合法序列，长度为 2*n-1。
    思路：回溯 + 从左到右填 + 大数优先
    """
    length = 2 * n - 1                # 序列总长度
    ans = [0] * length                # 结果数组，0 表示空位
    used = [False] * (n + 1)          # 标记数字是否已经放置（>1 必须恰好放一次，两次出现视为一次放置）

    def backtrack(pos: int) -> bool:
        """尝试从位置 pos 开始填充，返回是否成功找到完整序列"""
        # 1️⃣ 找到下一个空位
        while pos < length and ans[pos] != 0:
            pos += 1
        if pos == length:             # 所有位置都已填满，得到合法序列
            return True

        # 2️⃣ 从大到小尝试数字
        for num in range(n, 0, -1):
            if used[num]:
                continue               # 这个数字已经放过了（>1 只能放一次，两次出现算一次放置）

            # 处理数字 1：只需要占一个位置
            if num == 1:
                ans[pos] = 1
                used[1] = True
                if backtrack(pos + 1):
                    return True
                # 回溯
                ans[pos] = 0
                used[1] = False
                continue

            # 处理数字 >1：需要两个位置，间隔恰好为 num
            nxt = pos + num               # 另一个位置的下标（因为下标差必须等于 num）
            if nxt < length and ans[nxt] == 0:
                # 同时占据 pos 与 nxt
                ans[pos] = ans[nxt] = num
                used[num] = True
                if backtrack(pos + 1):
                    return True
                # 回溯：撤销这两个格子的填充
                ans[pos] = ans[nxt] = 0
                used[num] = False

        # 没有任何数字可以放在当前位置，返回 False 让上层回溯
        return False

    # 入口
    backtrack(0)
    return ans

# -------------------------------------------------
# 示例
print(construct_largest_sequence(3))   # [3, 1, 2, 3, 2]
print(construct_largest_sequence(5))   # [5, 3, 1, 4, 3, 5, 2, 4, 2]
```

> **代码要点注释**（每行中文解释已在代码中标出）  
> - `while pos < length and ans[pos] != 0:` 用来**跳过已经填好的格子**，保证我们每次都在**最左边的空位**决定数字。  
> - `for num in range(n, 0, -1):` 是**从大到小尝试**，确保字典序最大。  
> - `nxt = pos + num` 正是**“距离为 num”**的另一格子位置。  
> - `used[num] = True` 表示这个数字已经“使用过”，后面不再重复放。  
> - 递归返回 `True` 时直接向上层返回，**第一个完整解就是答案**。

#### 复杂度

- **时间复杂度**：最坏情况约为 `O(n!)`（因为每个数字只会尝试一次放置），但实际远小于此，`n ≤ 20` 时在毫秒级完成。  
  - 与暴力解的 `O(n * n^(2n-1))` 相比，指数基数从 `n` 降到了 `n` 的阶乘，数量级大幅下降。  
- **空间复杂度**：`O(n)`  
  - `ans` 长度 `2n-1`，`used` 长度 `n+1`，递归深度最多 `n`，都与 `n` 成线性关系。

---

## 心得

- **核心技巧**：**回溯 + 大数优先**（即在搜索时按照字典序从大到小尝试），能够在保证正确性的前提下直接得到字典序最大的解。  
- **适用场景**：  
  1. 需要构造满足“**位置间距**”或“**配对**”约束的序列，如 “排列距离为数值本身” 类问题。  
  2. 需要在所有合法解中挑选字典序（或数值）最大的/最小的，这时**搜索顺序**决定答案的唯一性。  
  3. “**数独**、**N‑皇后**”这类搜索空间大但可以通过**剪枝**大幅降低的组合问题。  
- **一句话总结**：**先决定左边、先放大数——搜索第一条完整路径就是字典序最大的答案。**

---

## 反思

- **第一反应**：看到“距离 = 数字本身”，本能想到**两两配对**，于是立刻把每个数字出现两次的约束写下来，随后想到可以把序列长度视为 `2n-1`，并尝试**暴力枚举**。  
- **最容易踩的坑**：  
  1. **下标差的理解错误**：有些人会把“距离 = i”误写成“相隔 i‑1 个位置”，导致 `pos + i` 写成 `pos + i - 1`，进而产生错误的序列。  
  2. **忘记数字 1 只出现一次**：若把 1 也当成需要配对的数字，程序会找不到合法解。  
  3. **剪枝不足**：没有在搜索时立即跳过已经被占用的格子，会导致大量无用递归。  
- **下次类似题目第一步**：  
  - **先弄清楚约束**（每个数字出现几次、相隔多少），把它写成**数学公式**。  
  - **确定搜索顺序**：如果要求字典序最大/最小，记得**从左到右**决定、**从大到小**或**从小到大**尝试。  
  - 再把这些信息套进**回溯框架**，一步步实现并做好剪枝。