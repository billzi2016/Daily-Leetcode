# #1566. 检测长度为 M 的模式重复 K 次或以上 / Detect Pattern of Length M Repeated K or More Times

> 难度：简单 · 标签：Array、Enumeration · [LeetCode 链接](https://leetcode.com/problems/detect-pattern-of-length-m-repeated-k-or-more-times/)

---

## 题目（英文原版）

**Description**

Given an array of positive integers arr, find a pattern of length m that is repeated k or more times.
A pattern is a subarray (consecutive sub-sequence) that consists of one or more values, repeated multiple times consecutively without overlapping. A pattern is defined by its length and the number of repetitions.
Return true if there exists a pattern of length m that is repeated k or more times, otherwise return false.

**Examples**

**Example 1:**

```
Input: arr = [1,2,4,4,4,4], m = 1, k = 3
Output: true
Explanation: The pattern (4) of length 1 is repeated 4 consecutive times. Notice that pattern can be repeated k or more times but not less.
```

**Example 2:**

```
Input: arr = [1,2,1,2,1,1,1,3], m = 2, k = 2
Output: true
Explanation: The pattern (1,2) of length 2 is repeated 2 consecutive times. Another valid pattern (2,1) is also repeated 2 times.
```

**Example 3:**

```
Input: arr = [1,2,1,2,1,3], m = 2, k = 3
Output: false
Explanation: The pattern (1,2) is of length 2 but is repeated only 2 times. There is no pattern of length 2 that is repeated 3 or more times.
```

**Constraints**

- 2 <= arr.length <= 100
- 1 <= arr[i] <= 100
- 1 <= m <= 100
- 2 <= k <= 100

---

## 题目（中文翻译）

给定一个正整数数组 `arr`，请判断是否存在一个长度为 `m` 的模式（pattern），该模式连续重复出现至少 `k` 次。

**模式**是指一个子数组（subarray），即由一个或多个连续元素组成的序列，该子数组可以不重叠地连续出现多次。模式由其长度和重复次数唯一确定。

如果存在长度为 `m` 且重复次数不少于 `k` 的模式，返回 `true`；否则返回 `false`。

### 示例

**示例 1**  
输入：`arr = [1,2,4,4,4,4]`, `m = 1`, `k = 3`  
输出：`true`  
解释：长度为 1 的模式 `(4)` 连续出现了 4 次。注意，模式可以重复 **k** 次或更多次，但不能少于 **k** 次。

**示例 2**  
输入：`arr = [1,2,1,2,1,1,1,3]`, `m = 2`, `k = 2`  
输出：`true`  
解释：长度为 2 的模式 `(1,2)` 连续出现了 2 次。另一个合法的模式 `(2,1)` 也出现了 2 次。

**示例 3**  
输入：`arr = [1,2,1,2,1,3]`, `m = 2`, `k = 3`  
输出：`false`  
解释：模式 `(1,2)` 长度为 2，但只重复了 2 次。不存在长度为 2 且重复次数不少于 3 次的模式。

### 约束

- `2 <= arr.length <= 100`
- `1 <= arr[i] <= 100`
- `1 <= m <= 100`
- `2 <= k <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把「所有可能的模式」都枚举一遍，然后看它们是否出现了 **k 次或更多** 的连续重复。  
具体做法：

1. **遍历起始位置** `start`（从 `0` 到 `len(arr)-m`），因为模式的长度固定为 `m`，如果从 `start` 开始取不到 `m` 个元素，就没有意义了。  
2. **取出一个候选模式** `pattern = arr[start:start+m]`。这一步可以类比为在字典里查到一个词（`pattern`），我们准备去看后面有没有相同的词。  
3. **检查后面的块**：从 `start+m` 开始，每次向后跳 `m`，把对应的子数组和 `pattern` 做比较。只要相等，就说明连续出现了一次。  
4. 当连续相等的次数达到 `k-1`（因为已经有第一次出现了），就可以直接返回 `True`。如果在检查过程中出现不相等，就换下一个起始位置继续尝试。

> **为什么正确？**  
> 我们把所有可能的「起点」和「模式」都检查了一遍，只要有一种能够满足「连续出现 k 次」的条件，就一定会在某一次循环里被发现。没有漏掉的情况。

> **时间/空间复杂度**  
> - 外层遍历 `start` 最多 `n` 次（`n = len(arr)`）。  
> - 对每个 `start`，我们最多比较 `k-1` 次子数组，每次比较需要遍历 `m` 个元素。  
> - 所以总的操作数大约是 `n * (k-1) * m`，在大 O 记号下记为 **O(n·m·k)**。  
> - 这里的 `O(n·m·k)` 可以想象成「先选起点」→「再选第几次重复」→「再逐个元素比对」的三层循环。  
> - 额外空间只用了保存一个 `pattern`，长度为 `m`，所以 **O(m)**（在本题中可以认为是 O(1)），因为 `m ≤ 100`，非常小。

#### 代码（Python）

```python
def containsPattern(arr, m, k):
    n = len(arr)
    # 遍历所有可能的起始位置
    for start in range(n - m + 1):
        # 取出长度为 m 的候选模式
        pattern = arr[start:start + m]

        # 检查后面是否连续出现 k-1 次（已经有一次是 pattern 本身）
        ok = True
        for repeat in range(1, k):          # 第 1 次到第 k-1 次
            # 计算本次比较的子数组起点
            nxt_start = start + repeat * m
            # 如果已经超出数组范围，说明不可能再完整出现一次
            if nxt_start + m > n:
                ok = False
                break
            # 对应的子数组
            next_block = arr[nxt_start:nxt_start + m]
            # 逐个元素比较（这里用切片直接比较，Python 会逐元素检查）
            if next_block != pattern:
                ok = False
                break

        if ok:                # 找到一次满足条件的模式
            return True

    return False               # 所有起点都检查完，仍未找到
```

#### 复杂度  

- **时间复杂度**：`O(n·m·k)`  
  - 想象一下有三层套娃：外层遍历 `n` 次，第二层最多跑 `k` 次，最内层要比 `m` 个数。  
  - 对于本题的最大规模（`n=100, m=100, k=100`），最坏情况大约是 1,000,000 次比较，仍然可以在毫秒级完成。  

- **空间复杂度**：`O(m)`（保存 `pattern`），实际可视作 `O(1)`，因为 `m` 上限很小且不随输入规模指数增长。  



---  

### 2. 最优解  

#### 思路  

暴力解的「慢点」主要在于 **每次都要把整个模式切片出来再比较**，这会导致重复的工作。  
我们可以把「比较」的过程合并进一次线性扫描：

1. **一次遍历** `i`（从 `0` 到 `n-m`），把 `arr[i:i+m]` 当作当前块。  
2. 看它和它前面的块 `arr[i-m:i]` 是否相同（仅在 `i ≥ m` 时才有前块）。  
   - 如果相同，说明连续出现次数 `cnt` 增加 1。  
   - 如果不同，说明连续计数断了，需要重新从 1 开始（因为当前块本身算一次出现）。  
3. 当 `cnt` 达到 `k` 时，说明已经找到了 `k` 次连续重复，直接返回 `True`。  

这相当于把「检查后面的 k-1 块」的工作提前到「左边已经出现了多少次」的状态里，省掉了重复的切片和比较。  

> **核心技巧：滑动窗口 + 连续计数**  
> - 把数组划分成等长的「窗口」`[i, i+m)`，只需要比较相邻窗口是否相等。  
> - 类比成「连续相同的砖块」：只要砖块一样，就把连续计数往右推进。  

> **为什么更快？**  
> - 每个元素最多被比较两次（一次作为左窗口，一次作为右窗口），整体是 **O(n·m)**，而不是 `O(n·m·k)`。  
> - 在最坏情况下 `k` 可能等于 `n/m`，所以我们省掉了一个乘以 `k` 的因子。  

#### 代码（Python）

```python
def containsPattern(arr, m, k):
    n = len(arr)
    # cnt 记录当前已经连续相同的块数（包括当前块本身）
    cnt = 1                         # 第一个块默认出现一次
    # 从第二个块开始检查（i 为块的起始下标）
    for i in range(m, n - m + 1, m):
        # 当前块 arr[i:i+m] 与前一个块 arr[i-m:i] 是否完全相同？
        if arr[i:i + m] == arr[i - m:i]:
            cnt += 1                # 连续相同，计数加 1
        else:
            cnt = 1                 # 断了，重新计数（当前块算一次）

        if cnt >= k:                # 达到 k 次，直接返回
            return True

    return False                     # 扫描完仍未满足
```

> **代码要点注释**  
> - `range(m, n - m + 1, m)`：每次跳 `m`，保证 `i` 永远指向一个完整块的起始位置。  
> - `arr[i:i+m] == arr[i-m:i]`：Python 切片比较会逐元素检查，等价于「字典里查两个词是否相同」。  
> - `cnt` 初始为 `1`，因为每次看到一个块，至少算一次出现。  

#### 复杂度  

- **时间复杂度**：`O(n·m)`  
  - 我们只遍历了 `n/m` 个块，每个块的比较需要 `m` 次元素比较，总计约 `n·m` 次操作。  
  - 相比暴力的 `O(n·m·k)`，少了一个 `k`，在 `k` 较大的情况下提升明显。  

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量 `cnt`、`i`，没有额外随输入规模增长的存储。  



---  



## 心得  

- **核心技巧**：**相邻等长子数组的比较 + 连续计数**（滑动窗口）。  
- **适用题型**：  
  1. 检测重复模式（本题）。  
  2. 判断数组是否由相同长度的子序列交替组成（如 LeetCode 1124. 表现好坏的分数）。  
  3. “重复子串”类的字符串问题（如 “Repeated Substring Pattern”）。  
- **一句话总结解题钥匙**：把“检查 k 次”转化为“看相邻块是否相等并累计连续次数”。  



---  



## 反思  

- **第一反应**：直接枚举所有起点、所有可能的重复次数，写三层循环。  
- **最容易踩的坑**：  
  - 边界条件：`i+m` 可能会越界，需要提前判断 `i + m <= n`。  
  - `k` 的意义是 “至少 k 次”，所以要记得把已经出现的第一次算进去（`cnt` 初始为 1）。  
  - 当 `m` 大于数组长度时，直接返回 `False`（本题约束保证不会出现，但写代码时仍需防御）。  
- **下次思路**：遇到“重复 k 次”这类题目，第一步先想 **“相邻块是否相同”**，把问题转化为 **“连续计数”**，往往可以把多余的循环层数去掉。