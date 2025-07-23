# #3277. 最大异或得分子数组查询 / Maximum XOR Score Subarray Queries

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximum-xor-score-subarray-queries/)

---

## 题目（英文原版）

**Description**

You are given an array nums of n integers, and a 2D integer array queries of size q, where queries[i] = [li, ri].
For each query, you must find the maximum XOR score of any subarray of nums[li..ri].
The XOR score of an array a is found by repeatedly applying the following operations on a so that only one element remains, that is the score:
Return an array answer of size q where answer[i] is the answer to query i.

**Examples**

**Example 1:**

```
Input: nums = [2,8,4,32,16,1], queries = [[0,2],[1,4],[0,5]]
Output: [12,60,60]
Explanation:
In the first query, nums[0..2] has 6 subarrays [2] , [8] , [4] , [2, 8] , [8, 4] , and [2, 8, 4] each with a respective XOR score of 2, 8, 4, 10, 12, and 6. The answer for the query is 12, the largest of all XOR scores.
In the second query, the subarray of nums[1..4] with the largest XOR score is nums[1..4] with a score of 60.
In the third query, the subarray of nums[0..5] with the largest XOR score is nums[1..4] with a score of 60.
```

**Example 2:**

```
Input: nums = [0,7,3,2,8,5,1], queries = [[0,3],[1,5],[2,4],[2,6],[5,6]]
Output: [7,14,11,14,5]
Explanation:
```

**Constraints**

- 1 <= n == nums.length <= 2000
- 0 <= nums[i] <= 231 - 1
- 1 <= q == queries.length <= 105
- queries[i].length == 2
- queries[i] = [li, ri]
- 0 <= li <= ri <= n - 1

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`，以及一个大小为 `q` 的二维整数数组 `queries`，其中 `queries[i] = [l_i, r_i]`。  
对于每个查询，你需要在子数组 `nums[l_i..r_i]` 中找出 **异或得分（XOR score）** 最大的任意子数组，并返回该最大得分。

**异或得分的定义**  
对数组 `a` 重复执行以下操作，直至只剩下一个元素，该元素即为 `a` 的异或得分：

1. 任意选取数组中的两个元素 `x` 与 `y`；
2. 用 `x XOR y` 替换这两个元素（即删除 `x、y`，插入它们的异或值）；

由于异或运算满足结合律和交换律，最终剩下的唯一元素等价于整个数组所有元素的异或值。因此，子数组的异或得分就是该子数组所有元素的 **异或和（XOR sum）**。

返回一个长度为 `q` 的数组 `answer`，其中 `answer[i]` 为第 `i` 个查询的答案。

---

### 示例

#### 示例 1
```
Input: nums = [2,8,4,32,16,1], queries = [[0,2],[1,4],[0,5]]
Output: [12,60,60]
Explanation:
- 第一个查询区间 `nums[0..2] = [2,8,4]` 有 6 个子数组：
  [2]、[8]、[4]、[2,8]、[8,4]、[2,8,4]，它们的异或得分分别为 2、8、4、10、12、6。
  最大得分为 **12**。
- 第二个查询区间 `nums[1..4] = [8,4,32,16]`，异或得分最大的子数组是 `[8,4,32,16]`，其得分为 **60**。
- 第三个查询区间 `nums[0..5]` 的最大异或得分同样为 **60**（子数组 `[8,4,32,16]` 或 `[2,8,4,32,16]` 等）。

#### 示例 2
```
Input: nums = [0,7,3,2,8,5,1], queries = [[0,3],[1,5],[2,4],[2,6],[5,6]]
Output: [7,14,11,14,5]
Explanation:
- 查询 `[0,3]` 对应子数组 `[0,7,3,2]`，最大异或得分为 **7**（子数组 `[7]`）。
- 查询 `[1,5]` 对应子数组 `[7,3,2,8,5]`，最大异或得分为 **14**（子数组 `[7,3,2,8,5]`）。
- 查询 `[2,4]` 对应子数组 `[3,2,8]`，最大异或得分为 **11**（子数组 `[3,8]`）。
- 查询 `[2,6]` 对应子数组 `[3,2,8,5,1]`，最大异或得分为 **14**（子数组 `[3,2,8,5,1]`）。
- 查询 `[5,6]` 对应子数组 `[5,1]`，最大异或得分为 **5**（子数组 `[5]`）。

---

### 约束条件
- `1 <= n == nums.length <= 2000`
- `0 <= nums[i] <= 2^31 - 1`
- `1 <= q == queries.length <= 10^5`
- `queries[i].length == 2`
- `queries[i] = [l_i, r_i]`
- `0 <= l_i <= r_i <= n - 1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

> **最直接的想法**：  
> 对每一个查询 `[l, r]`，把区间 `nums[l..r]` 中的所有子数组枚举出来，逐个计算它们的 **XOR 分数**（把相邻两个数做 XOR，一直压缩到只剩一个数），然后取最大值。  

**用到的数据结构**  

| 数据结构 | 类比 | 说明 |
|----------|------|------|
| 列表 `nums` | 书架上的一本本书 | 每本书（元素）都有编号（下标）和内容（数值） |
| 二维数组 `queries` | 任务单 | 每张任务单上写着要检查的书架区间 `[l, r]` |
| 临时列表 `subarray` | 把几本书摆在一起的临时堆 | 用来保存当前枚举的子数组 |
| 变量 `xor_score` | “最终的书签” | 记录一次压缩后剩下的唯一数值 |

**为什么这个方法一定能得到正确答案**  

- 我们把区间里 **所有** 可能的子数组都算了一遍，绝不会漏掉任何一种情况。  
- 对每个子数组我们按照题目要求的“相邻 XOR 压缩”一步步做到底，最后得到的唯一数值就是它的 XOR 分数。  
- 把所有分数取最大，自然就是答案。

**复杂度分析（大白话）**  

- 对每个查询，区间长度记作 `m = r-l+1`。子数组的数量是 `m·(m+1)/2`（想象把 `m` 本书排成一排，左端点有 `m` 种选法，右端点再往右选）。  
- 对每个子数组，我们要做 `len-1` 次相邻 XOR（因为要把 `len` 本书压缩到 1 本），最坏情况大约是 `O(m)`。  
- 所以单个查询的时间是 `O(m³)`，所有查询加起来是 `O(q·n³)`（因为最坏 `m≈n`），这里 `n ≤ 2000`、`q ≤ 10⁵`，根本跑不完。  

空间上只需要存放几个临时变量，`O(1)`。

---

#### 代码（Python）

```python
def xor_score(arr: list[int]) -> int:
    """把相邻元素一直 XOR，最后只剩一个数，返回它"""
    # 复制一份，防止修改原数组
    a = arr[:]
    # 每次把长度缩短 1，直到只剩一个元素
    while len(a) > 1:
        # 相邻两两 XOR，生成新数组
        a = [a[i] ^ a[i + 1] for i in range(len(a) - 1)]
    return a[0]                     # 只剩下的元素

def brute_force(nums: list[int], queries: list[list[int]]) -> list[int]:
    ans = []
    for l, r in queries:                     # 遍历每个查询
        best = 0
        # 枚举所有子数组的左端点
        for i in range(l, r + 1):
            # 枚举所有子数组的右端点
            for j in range(i, r + 1):
                sub = nums[i:j + 1]          # 当前子数组
                score = xor_score(sub)       # 计算它的 XOR 分数
                best = max(best, score)      # 维护最大值
        ans.append(best)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(q·n³)`（每个查询要枚举 `O(n²)` 个子数组，每个子数组再做 `O(n)` 次压缩）。  
  - 大白话：如果 `n = 2000`，一次查询就要上百亿次运算，根本不可能在几秒内算完。  
- **空间复杂度**：`O(1)`（只用了常数个临时变量）。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到两点瓶颈：

1. **子数组枚举太多**：每个查询都要重新遍历所有子数组。  
2. **每个子数组的 XOR 分数计算太慢**：直接模拟压缩会导致 `O(length)` 的额外开销。

我们要把这两块“重复劳动”一次性提前算好，随后查询直接拿答案。

---

#### 2.1 关键观察：XOR 分数的递推公式  

设 `score[l][r]` 为子数组 `nums[l..r]`（左闭右闭）的 XOR 分数。  
把子数组压缩一步得到的中间数组是  

```
[ nums[l] ^ nums[l+1] , nums[l+1] ^ nums[l+2] , … , nums[r-1] ^ nums[r] ]
```

再继续压缩，最终的唯一元素恰好等于 **左端点子数组的分数 XOR 右端点子数组的分数**：

```
score[l][r] = score[l][r-1] XOR score[l+1][r]      (1)
```

- 当 `l == r` 时，子数组只有一个数，分数就是它本身：`score[i][i] = nums[i]`。  
- 当子数组长度为 2 时，`score[i][i+1] = nums[i] XOR nums[i+1]`，同样满足 (1)。  

**类比**：把 `score[l][r]` 想象成“两个相邻小组的最终成绩”。把左边的小组成绩和右边的小组成绩再 XOR 一下，就是整个大组的成绩。

---

#### 2.2 预处理所有子数组的 XOR 分数  

使用公式 (1) 按 **子数组长度** 从短到长填表：

```
for length = 1 .. n:
    for l = 0 .. n-length:
        r = l + length - 1
        if length == 1:   score[l][r] = nums[l]
        elif length == 2: score[l][r] = nums[l] ^ nums[r]
        else:             score[l][r] = score[l][r-1] ^ score[l+1][r]
```

这一步只做一次，时间是 `O(n²)`（因为每个 `(l, r)` 只算一次），空间同样是 `O(n²)` 用来存 `score`。

---

#### 2.3 预处理区间的最大 XOR 分数  

对每个区间 `[l, r]`，我们需要 **区间内部所有子数组的最大分数**。  
记 `best[l][r]` 为答案。考虑把区间 `[l, r]` 划分为三类子数组：

| 类别 | 包含的子数组 | 为什么已经在 `best` 表里 |
|------|--------------|---------------------------|
| ①   | 完全在 `[l, r-1]` 内 | 已经在 `best[l][r-1]` 中 |
| ②   | 完全在 `[l+1, r]` 内 | 已经在 `best[l+1][r]` 中 |
| ③   | 正好是 `[l, r]` 本身 | 直接用 `score[l][r]` |

于是递推式：

```
best[l][r] = max( best[l][r-1] , best[l+1][r] , score[l][r] )   (2)
```

同样按子数组长度从短到长填表，时间 `O(n²)`，空间 `O(n²)`。

---

#### 2.4 查询  

所有预处理完成后，任意查询 `[l, r]` 的答案就是 `best[l][r]`，**只需 O(1) 时间**。

---

#### 代码（Python）

```python
def maximumXorScore(nums: list[int], queries: list[list[int]]) -> list[int]:
    n = len(nums)

    # 1️⃣ 预计算每个子数组的 XOR 分数  -------------------------
    # score[l][r] = XOR score of nums[l..r]
    score = [[0] * n for _ in range(n)]

    for i in range(n):
        score[i][i] = nums[i]                     # 长度 1

    for length in range(2, n + 1):                # 从 2 开始递增长度
        for l in range(0, n - length + 1):
            r = l + length - 1
            if length == 2:
                score[l][r] = nums[l] ^ nums[r]   # 长度 2
            else:
                # 根据递推公式 score[l][r] = score[l][r-1] ^ score[l+1][r]
                score[l][r] = score[l][r - 1] ^ score[l + 1][r]

    # 2️⃣ 预计算每个区间的最大 XOR 分数 -------------------------
    # best[l][r] = max XOR score among all subarrays inside nums[l..r]
    best = [[0] * n for _ in range(n)]

    for i in range(n):
        best[i][i] = score[i][i]                 # 单元素区间

    for length in range(2, n + 1):
        for l in range(0, n - length + 1):
            r = l + length - 1
            # 递推式 (2)
            best[l][r] = max(best[l][r - 1],
                             best[l + 1][r],
                             score[l][r])

    # 3️⃣ 直接答查询
    return [best[l][r] for l, r in queries]
```

> **代码要点注释**  
> - `score[l][r]` 用 **递推** 而不是每次重新模拟压缩，省掉了 `O(length)` 的重复运算。  
> - `best[l][r]` 只看 **左/右缩小** 两个已经算好的子区间，加上自己本身，保证 `O(1)` 合并。  
> - 两个二维表的大小均为 `n × n ≤ 2000² = 4,000,000`，在 Python 中约占 30‑40 MB，完全可以接受。

#### 复杂度  

- **预处理时间**：`O(n²)`（两次遍历 `n × n` 的表），这里的 `n ≤ 2000`，大约 4 百万次运算，毫秒级完成。  
- **每个查询时间**：`O(1)`，只要一次数组下标访问。  
- **总时间**：`O(n² + q)`，即使 `q = 10⁵` 也非常快。  

- **空间复杂度**：`O(n²)`，用于存 `score` 与 `best` 两个表，约 30‑40 MB。  
  - 与暴力解的 `O(1)` 空间相比，这里换取了查询的瞬时响应，是典型的“预处理换空间”思路。

---

## 心得  

- **核心技巧**：利用 **递推公式** 把 “相邻 XOR 多次压缩” 转化为 `score[l][r] = score[l][r-1] XOR score[l+1][r]`，从而在 `O(1)` 时间内得到任意子数组的 XOR 分数。  
- **适用场景**：  
  1. 需要 **区间内部所有子区间的某种聚合值**（最大/最小/计数）并且 **区间长度上限较小**（如 `n ≤ 2000`）的题目。  
  2. 类似的“压缩运算”可以写成 **二维 DP 递推**（如区间异或、区间和、区间 GCD 等）。  
  3. “离线预处理 + O(1) 查询” 的模式，如**子数组最大和**、**子数组最小值** 等。  
- **一句话总结解题钥匙**：**把每一次“相邻 XOR”抽象成子区间之间的异或关系，用二维 DP 把所有子区间的分数一次算完，再用另一层 DP 把区间最大值也一次算完**。

---

## 反思  

- **第一反应**：看到“子数组的 XOR 分数”就想到直接模拟压缩，导致暴力枚举所有子数组，时间爆炸。  
- **最容易踩的坑**  
  1. **递推公式写错**：`score[l][r] = score[l][r-1] ^ score[l+1][r]`（不是 `l-1`），否则会出现索引越界或错误结果。  
  2. **边界处理**：长度为 1、2 的子数组需要单独初始化，否则在递推时会访问未定义的 `score`。  
  3. **空间限制**：如果把 `n` 误认为可以到 10⁵，`O(n²)` 表会炸内存，需要换成线段树或莫队算法。这里题目明确 `n ≤ 2000`，可以放心使用二维表。  
- **下次遇到同类题**：  
  1. **先思考是否可以把“区间运算”写成递推**（比如 `dp[l][r]` 与 `dp[l][r-1]`、`dp[l+1][r]` 的关系）。  
  2. **检查 n 的规模**，若 `n` 小到几千，优先考虑 **全表 DP + 预处理**；若 n 大则考虑 **离线算法**（莫队）或 **数据结构**（线段树、Trie）。  

这样一步步把“暴力”转化为“预处理”，既保证正确性，又能在严格的时间限制下跑得飞快。祝你玩转区间 DP，解题顺利！