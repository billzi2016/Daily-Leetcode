# #3036. **匹配模式 II 的子数组数量** / Number of Subarrays That Match a Pattern II

> 难度：困难 · 标签：Array、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/number-of-subarrays-that-match-a-pattern-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of size n, and a 0-indexed integer array pattern of size m consisting of integers -1, 0, and 1.
A subarray nums[i..j] of size m + 1 is said to match the pattern if the following conditions hold for each element pattern[k]:
Return the count of subarrays in nums that match the pattern.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5,6], pattern = [1,1]
Output: 4
Explanation: The pattern [1,1] indicates that we are looking for strictly increasing subarrays of size 3. In the array nums, the subarrays [1,2,3], [2,3,4], [3,4,5], and [4,5,6] match this pattern.
Hence, there are 4 subarrays in nums that match the pattern.
```

**Example 2:**

```
Input: nums = [1,4,4,1,3,5,5,3], pattern = [1,0,-1]
Output: 2
Explanation: Here, the pattern [1,0,-1] indicates that we are looking for a sequence where the first number is smaller than the second, the second is equal to the third, and the third is greater than the fourth. In the array nums, the subarrays [1,4,4,1], and [3,5,5,3] match this pattern.
Hence, there are 2 subarrays in nums that match the pattern.
```

**Constraints**

- 2 <= n == nums.length <= 106
- 1 <= nums[i] <= 109
- 1 <= m == pattern.length < n
- -1 <= pattern[i] <= 1

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`，长度为 `n`，以及一个下标从 0 开始、长度为 `m` 的整数数组 `pattern`，其中每个元素只能是 `-1`、`0` 或 `1`。  

长度为 `m + 1` 的子数组 `nums[i..j]`（`j = i + m`）若满足下列条件，则称其 **匹配** 给定的 `pattern`：

- 对于每个 `k`（`0 ≤ k < m`），若 `pattern[k] = 1`，则 `nums[i + k] < nums[i + k + 1]`（严格递增）；  
- 若 `pattern[k] = 0`，则 `nums[i + k] = nums[i + k + 1]`（相等）；  
- 若 `pattern[k] = -1`，则 `nums[i + k] > nums[i + k + 1]`（严格递减）。

返回数组 `nums` 中 **匹配** `pattern` 的子数组个数。

---

### 示例

**示例 1**  
```
Input: nums = [1,2,3,4,5,6], pattern = [1,1]
Output: 4
Explanation: 模式 `[1,1]` 表示我们在寻找长度为 3 的严格递增子数组。  
在 `nums` 中，子数组 `[1,2,3]`、`[2,3,4]`、`[3,4,5]` 和 `[4,5,6]` 均满足该模式。  
因此，匹配的子数组共有 4 个。
```

**示例 2**  
```
Input: nums = [1,4,4,1,3,5,5,3], pattern = [1,0,-1]
Output: 2
Explanation: 模式 `[1,0,-1]` 表示我们在寻找满足「第一个数小于第二个数、第二个数等于第三个数、第三个数大于第四个数」的序列。  
在 `nums` 中，子数组 `[1,4,4,1]` 与 `[3,5,5,3]` 符合该模式。  
因此，匹配的子数组共有 2 个。
```

---

### 约束

- `2 ≤ n == nums.length ≤ 10^6`
- `1 ≤ nums[i] ≤ 10^9`
- `1 ≤ m == pattern.length < n`
- `-1 ≤ pattern[i] ≤ 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一个可能的子数组都枚举出来，然后逐个和 `pattern` 比较**。  

- **枚举子数组**：长度固定为 `m+1`（因为 `pattern` 长度是 `m`，对应 `m` 条相邻关系），所以只需要遍历起始下标 `i = 0 … n-m-1`，子数组就是 `nums[i … i+m]`。  
- **逐位比较**：对于子数组中的相邻两个数 `nums[i+k]` 与 `nums[i+k+1]`，看它们的大小关系是 `>、=、<`，把这三个可能分别映射成 `1、0、-1`，得到一个长度为 `m` 的 “关系数组”。把它和给定的 `pattern` 做逐位比较，全部相等则说明匹配。  

> **类比**：把 `nums` 想成一条路，上面有很多路标（数字）。我们要找的是一段长度为 `m+1` 的路段，其中每两个相邻路标的相对高低正好对应我们手里的“升、平、降”模式（`pattern`）。暴力做法就是把每一段路都走一遍，逐个核对。

**为什么正确**：因为我们检查了所有合法的起点，且每一次检查都严格按照题目要求比较了所有相邻关系，必然不会漏掉也不会误判。

#### 代码（Python）

```python
def count_subarrays_bruteforce(nums, pattern):
    n = len(nums)
    m = len(pattern)
    ans = 0

    # 枚举所有长度为 m+1 的子数组的左端点 i
    for i in range(n - m):
        ok = True
        # 检查子数组内部的每一对相邻元素
        for k in range(m):
            # 计算 nums[i+k] 与 nums[i+k+1] 的关系
            if nums[i + k] < nums[i + k + 1]:
                rel = 1
            elif nums[i + k] == nums[i + k + 1]:
                rel = 0
            else:               # nums[i + k] > nums[i + k + 1]
                rel = -1

            # 与 pattern 对应位置比较
            if rel != pattern[k]:
                ok = False
                break          # 只要有一处不匹配，就可以提前结束内部循环

        if ok:
            ans += 1          # 找到一个匹配的子数组

    return ans
```

> 关键行解释  
> - `for i in range(n - m)`: `n-m` 是因为最后一个子数组的左端点是 `n-m-1`，长度正好是 `m+1`。  
> - `rel = 1 / 0 / -1`: 把“升、平、降”映射成整数，便于后面直接和 `pattern` 比较。  
> - `break`: 一旦发现不匹配，就不必再检查后面的关系，省点时间。

#### 复杂度

- **时间复杂度**：`O((n-m) * m) ≈ O(n·m)`  
  - 外层遍历 `n-m` 次，每次最坏要比较 `m` 对相邻元素。  
  - **大白话**：如果 `n=10⁶`、`m≈5·10⁵`，那相当于要跑 **5·10¹¹** 次操作，根本跑不完。

- **空间复杂度**：`O(1)`  
  - 只用了常数级的额外变量（计数器、临时关系值），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复比较相邻元素的大小关系**。  
实际上，**我们只关心每两个相邻数的相对关系**，而不是它们的具体数值。  
于是可以把原数组 `nums` **预处理** 成一个只记录相对关系的数组 `rel_arr`（长度 `n-1`），其中：

```
rel_arr[i] =  1  if nums[i+1] > nums[i]
rel_arr[i] =  0  if nums[i+1] == nums[i]
rel_arr[i] = -1  if nums[i+1] < nums[i]
```

这样，**原问题就变成**：在 `rel_arr` 中找出所有等于 `pattern`（长度 `m`）的连续子串的出现次数。  

这正是**字符串匹配**的经典任务。  
我们可以使用 **Knuth-Morris-Pratt (KMP) 算法**（或者 Z‑Function）在 `O(n)` 时间内完成：

1. **构造模式串的“前缀函数”(failure function)**  
   前缀函数 `pi[i]` 表示模式串 `pattern[0…i]` 的最长**真前缀**也是**真后缀**的长度。  
   这一步只依赖 `pattern` 本身，耗时 `O(m)`。

2. **在 `rel_arr` 上跑 KMP**  
   使用已经算好的 `pi`，一次遍历 `rel_arr`，维护当前匹配到模式的长度 `j`。  
   当 `j == m` 时说明找到了一个完整匹配，计数 +1，并根据 `pi` 回退，以继续寻找后续可能的匹配（允许重叠）。

> **类比**：把 `rel_arr` 看成一本长篇小说，把 `pattern` 看成一段要找的短句子。KMP 就像是先把短句子里可以自我重叠的部分记下来（前缀函数），然后在读小说时一边读一边用记忆快速跳过已经确定不匹配的字符，省掉大量回头比较的时间。

**为什么线性**：  
- 前缀函数的构造只遍历模式一次 `O(m)`。  
- 匹配过程每走一步最多回退一次，总的回退次数不超过 `n`，所以整体 `O(n)`。

#### 代码（Python）

```python
def compute_pi(pattern):
    """返回 pattern 的前缀函数数组 pi，长度为 len(pattern)"""
    m = len(pattern)
    pi = [0] * m
    j = 0  # 当前匹配的前缀长度

    # i 从 1 开始，因为 pi[0] 必然是 0
    for i in range(1, m):
        # 若出现不匹配，沿着已经得到的 pi 回退
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]

        if pattern[i] == pattern[j]:
            j += 1
            pi[i] = j
        # 否则 pi[i] 仍为 0（已经默认初始化）

    return pi


def count_subarrays_kmp(nums, pattern):
    n = len(nums)
    m = len(pattern)

    # 1️⃣ 先把 nums 转成相对关系数组 rel_arr（长度 n-1）
    rel_arr = [0] * (n - 1)
    for i in range(n - 1):
        if nums[i + 1] > nums[i]:
            rel_arr[i] = 1
        elif nums[i + 1] == nums[i]:
            rel_arr[i] = 0
        else:               # nums[i + 1] < nums[i]
            rel_arr[i] = -1

    # 2️⃣ 计算 pattern 的前缀函数
    pi = compute_pi(pattern)

    # 3️⃣ 在 rel_arr 上跑 KMP
    ans = 0
    j = 0                     # 当前匹配到 pattern 的长度
    for x in rel_arr:         # 遍历 rel_arr 的每个字符（-1/0/1）
        # 当出现不匹配时，利用 pi 回退
        while j > 0 and x != pattern[j]:
            j = pi[j - 1]

        if x == pattern[j]:
            j += 1            # 匹配成功，长度加一

        if j == m:           # 完全匹配到 pattern
            ans += 1
            # 为了寻找可能的重叠匹配，回退到上一个最长前后缀的位置
            j = pi[j - 1]

    return ans
```

> 关键行解释  
> - `rel_arr` 的构造把“升、平、降”压缩成单个整数，后面只需要比较整数即可。  
> - `while j > 0 and pattern[i] != pattern[j]`：如果当前字符不匹配，就按照已经算好的前缀函数回退，避免从头重新比较。  
> - `if j == m:`：匹配长度等于模式长度时说明找到了一个子数组，对应原数组中长度为 `m+1` 的区间。随后把 `j` 回退到 `pi[m-1]`，因为模式内部可能有自重叠（例如 pattern = `[1,1,1]`）。

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - 预处理 `rel_arr` 需要遍历一次 `nums` → `O(n)`。  
  - 计算前缀函数是 `O(m)`。  
  - KMP 主循环同样只遍历 `rel_arr` 一遍，且每个字符最多回退一次 → `O(n)`。  
  - **对比**：相比暴力的 `O(n·m)`，这里即使 `n` 达到 10⁶ 也能在毫秒级完成。

- **空间复杂度**：`O(n + m)`（实际可以把 `rel_arr` 直接在遍历时生成，进一步降到 `O(m)`）  
  - 主要是存放 `rel_arr`（长度 `n-1`）和前缀函数 `pi`（长度 `m`）。  
  - 若在实际实现中把 `rel_arr` 视作流式生成，则额外空间仅为 `O(m)`。

---

## 心得

- **核心技巧**：把原始数值转换成“相对关系”数组，再使用线性时间的字符串匹配算法（KMP 或 Z‑Function）统计模式出现次数。  
- **适用场景**  
  1. **相邻关系匹配**：如 “子数组升序/降序/相等模式” 的统计。  
  2. **连续差值序列匹配**：如在股票价格序列中找出特定的涨跌形状。  
  3. **离散化后模式匹配**：任何把连续数值映射成离散符号后进行子串计数的问题。  
- **一句话总结**：把数字变成符号，符号匹配用 KMP，线性时间搞定。

---

## 反思

- **第一反应**：看到 “-1、0、1” 的 pattern，立刻想到把相邻元素的比较结果抽象出来，问题变成子串匹配。  
- **最容易踩的坑**  
  - **边界**：`nums` 长度是 `n`，相对关系数组长度是 `n-1`，要注意循环范围的 off‑by‑one。  
  - **模式全相同**（如 `[1,1,1]`）时会产生重叠匹配，必须在找到一次匹配后根据前缀函数回退，而不是直接 `j = 0`。  
  - **整数溢出**：本题只比较大小，不涉及加减，故不必担心大数相减的溢出。  
- **下次类似题的第一步**：先判断**是否只关心相邻元素之间的相对关系**，如果是，就立刻做一次 “差分/符号化” 预处理，然后把问题转化为**字符串（或数组）子串匹配**，再选用 KMP/Z‑Function 等线性算法。