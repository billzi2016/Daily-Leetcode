# #1124. 最长的表现良好区间 / Longest Well-Performing Interval

> 难度：中等 · 标签：Array、Hash Table、Stack、Monotonic Stack、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/longest-well-performing-interval/)

---

## 题目（英文原版）

**Description**

We are given hours, a list of the number of hours worked per day for a given employee.
A day is considered to be a tiring day if and only if the number of hours worked is (strictly) greater than 8.
A well-performing interval is an interval of days for which the number of tiring days is strictly larger than the number of non-tiring days.
Return the length of the longest well-performing interval.

**Examples**

**Example 1:**

```
Input: hours = [9,9,6,0,6,6,9]
Output: 3
Explanation: The longest well-performing interval is [9,9,6].
```

**Example 2:**

```
Input: hours = [6,6,6]
Output: 0
```

**Constraints**

- 1 <= hours.length <= 104
- 0 <= hours[i] <= 16

---

## 题目（中文翻译）

我们给定 `hours`，它是一个整数数组，表示某位员工每天工作的小时数。  
如果某一天的工作时长 **严格大于** 8，则该天被视为**疲惫日（tiring day）**。  

**表现良好区间（well-performing interval）** 是指在该区间内，疲惫日的数量 **严格大于** 非疲惫日的数量。  

返回最长的表现良好区间的长度。

**示例 1**  
输入: `hours = [9,9,6,0,6,6,9]`  
输出: `3`  
解释: 最长的表现良好区间是 `[9,9,6]`。

**示例 2**  
输入: `hours = [6,6,6]`  
输出: `0`

**约束条件**  
- `1 <= hours.length <= 10^4`  
- `0 <= hours[i] <= 16`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是**枚举所有可能的连续区间**，统计区间里“累加的疲劳天数”和“非疲劳天数”，看它们的差是否大于 0。  

- **把每天的工时映射成 +1 / -1**  
  - 如果 `hours[i] > 8`（累加的疲劳天），记作 `+1`  
  - 否则记作 `-1`（非疲劳天）  
  这样，一个区间的 **和** 就等于“疲劳天数 - 非疲劳天数”。只要和 > 0，这个区间就是“表现良好”。  
- **暴力枚举**  
  - 用两层循环，外层 `i` 为区间左端，内层 `j` 为右端（`i ≤ j`）。  
  - 在内层遍历时，累计 `+1 / -1` 的和，一旦发现和 > 0，就更新答案 `max_len = max(max_len, j - i + 1)`。  

> **生活化类比**：把 `+1 / -1` 看成在记分本上加分或扣分，区间的总分 > 0 就说明这段时间“赚了分”。我们要找分数最高的那段连续记分本页数。

#### 代码（Python）

```python
def longestWPI_brute(hours):
    # 把工时转成 +1 / -1 的数组
    score = [1 if h > 8 else -1 for h in hours]

    n = len(score)
    max_len = 0

    # 暴力枚举所有区间
    for i in range(n):
        cur_sum = 0                 # 区间 [i, j] 的累计和
        for j in range(i, n):
            cur_sum += score[j]     # 累加当前元素的 +1 / -1
            if cur_sum > 0:         # 和大于 0 表示疲劳天数 > 非疲劳天数
                max_len = max(max_len, j - i + 1)

    return max_len
```

#### 复杂度

- **时间复杂度：** `O(n²)`  
  两层循环遍历所有 `n·(n+1)/2` 个区间，等价于“平方级别”。如果 `n=10⁴`，大约会跑 **一亿次**的循环，显然太慢了。  
- **空间复杂度：** `O(n)`（存储 `score` 数组）  
  只用了线性额外空间，基本可以忽略不计。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复累加**：每次区间左端 `i` 变化时，内部的和又从头算起。我们可以利用**前缀和**一次遍历把所有区间的和表达出来，然后再通过**哈希表 + 单调栈**快速找到满足条件的最左端位置。

**步骤 1：把 +1 / -1 的数组转成前缀和**  

```
prefix[0] = 0
prefix[k+1] = prefix[k] + score[k]   (k 从 0 开始)
```

- `prefix[t]` 表示前 `t` 天（下标 `0..t-1`）的累计得分。  
- 区间 `[i, j]` 的得分 = `prefix[j+1] - prefix[i]`。  
- 要求得分 > 0 ⇔ `prefix[j+1] > prefix[i]`。

**步骤 2：记录每个前缀和第一次出现的位置**  

我们遍历 `prefix`，把 **每个出现的前缀和的最左下标** 放进字典 `first_pos`。如果同一个前缀和出现多次，只保留最早的下标，因为它能让后面的区间更长。

**步骤 3：单调递减栈保存“潜在左端”**  

我们希望找到 **最左边的 i**，使得 `prefix[i] < prefix[j]`（注意是严格小于）。如果把所有前缀和的下标按 **前缀和值递减** 放进栈，栈顶永远是 **当前最小的前缀和对应的最左下标**，它最有可能满足 `prefix[i] < prefix[j]`。

遍历 `j`（从左到右）：

- 当 `prefix[j]` 大于栈顶对应的前缀和时，说明栈顶的 `i` 可以构成一个正和区间。弹出栈顶，计算长度 `j - i`，更新答案。  
- 继续弹出，直到栈为空或 `prefix[j]` 不再大于栈顶的前缀和。  

这样每个下标最多进栈、出栈一次，整体是线性时间。

> **类比**：想象前缀和是山的海拔，栈里保存的是“最高的山峰”。当我们走到更高的地方时（`prefix[j]` 更高），就可以把之前的低谷（栈顶）和现在的高点连起来，得到一段“上坡”，这段上坡对应的天数就是我们要的答案。

#### 代码（Python）

```python
def longestWPI(hours):
    """
    返回最长的表现良好区间的长度（O(n) 时间，O(n) 空间）
    """
    # 1️⃣ 把工时转成 +1 / -1
    score = [1 if h > 8 else -1 for h in hours]

    # 2️⃣ 前缀和数组（长度为 n+1，prefix[0] = 0）
    prefix = [0]
    for s in score:
        prefix.append(prefix[-1] + s)

    n = len(prefix)

    # 3️⃣ 单调递减栈：保存前缀和递减的下标
    stack = []
    for i in range(n):
        # 只在当前前缀和更小（更低的山谷）时压栈
        if not stack or prefix[i] < prefix[stack[-1]]:
            stack.append(i)

    ans = 0
    # 4️⃣ 从右往左遍历，尝试把高地和低谷连接
    for j in range(n - 1, -1, -1):
        # 当右侧的前缀和大于栈顶对应的前缀和时，说明可以形成正和区间
        while stack and prefix[j] > prefix[stack[-1]]:
            i = stack.pop()          # i 是最左侧满足 prefix[i] < prefix[j] 的位置
            ans = max(ans, j - i)    # 区间长度是 j - i（因为 prefix 下标比原数组多 1）
        # 如果栈已经空了，后面再也找不到更左的 i，直接结束
        if not stack:
            break

    return ans
```

> **关键注释**  
- `stack` 保持 **严格递减**（`<`），因为相等的前缀和不满足 “>” 的条件。  
- 从右往左遍历 `j` 能保证每次弹出的 `i` 都是 **最左** 的合法下标，从而得到最长区间。  
- 整体只遍历两遍（一次建栈，一次弹栈），时间 `O(n)`，空间 `O(n)`。

#### 复杂度

- **时间复杂度：** `O(n)`  
  每个下标最多压栈一次、弹栈一次，线性遍历一次前缀和数组。相比暴力的 `O(n²)`，速度提升了 **n 倍**（比如 `n=10⁴` 时只需要几万次操作）。  
- **空间复杂度：** `O(n)`  
  需要保存前缀和和单调栈，最坏情况下两者都会占用 `n+1` 个整数的空间。

---

## 心得

- **核心技巧**：把 “疲劳天数 > 非疲劳天数” 转化为 “子数组的正和”，进而利用前缀和 + 单调栈在一次遍历中找出最长满足条件的子数组。  
- **适用题型**：  
  1. “最长子数组和大于 0” 类问题（如 LeetCode 1124、1129）。  
  2. “最长子数组满足 sum ≥ K” 的变形（可用前缀哈希或单调栈）。  
  3. “前缀和 + 单调栈” 解决的区间最大/最小问题（如 “最大宽度坡”）。  
- **一句话总结解题钥匙**：**把区间条件转成前缀和的大小比较，再用单调栈一次性找到最左的更小前缀**。

---

## 反思

- **第一反应**：直接枚举所有子区间，计算疲劳天数与非疲劳天数的差。  
- **最容易踩的坑**：  
  - 忘记把 “>8” 与 “≤8” 区分成 `+1 / -1`，导致和的判断错误。  
  - 单调栈的比较方向写反（应当是 `prefix[j] > prefix[stack[-1]]` 而不是 `>=`），否则会把和为 0 的区间也算进去。  
  - 边界条件：全是非疲劳天时答案应为 `0`，代码必须能正确返回。  
- **下次类似题的第一步**：  
  **先把原始条件映射成“+1 / -1” 或者 “+value / -value”，构造前缀和；随后思考“前缀和之间的大小关系”能否用单调结构（栈或递增数组）一次性解决。**