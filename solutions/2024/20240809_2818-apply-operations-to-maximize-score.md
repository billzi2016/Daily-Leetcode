# #2818. **应用操作以最大化得分** / Apply Operations to Maximize Score

> 难度：困难 · 标签：Array、Math、Stack、Greedy、Sorting、Monotonic Stack、Number Theory · [LeetCode 链接](https://leetcode.com/problems/apply-operations-to-maximize-score/)

---

## 题目（英文原版）

**Description**

You are given an array nums of n positive integers and an integer k.
Initially, you start with a score of 1. You have to maximize your score by applying the following operation at most k times:
Here, nums[l, ..., r] denotes the subarray of nums starting at index l and ending at the index r, both ends being inclusive.
The prime score of an integer x is equal to the number of distinct prime factors of x. For example, the prime score of 300 is 3 since 300 = 2 * 2 * 3 * 5 * 5.
Return the maximum possible score after applying at most k operations.
Since the answer may be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [8,3,9,3,8], k = 2
Output: 81
Explanation: To get a score of 81, we can apply the following operations:
- Choose subarray nums[2, ..., 2]. nums[2] is the only element in this subarray. Hence, we multiply the score by nums[2]. The score becomes 1 * 9 = 9.
- Choose subarray nums[2, ..., 3]. Both nums[2] and nums[3] have a prime score of 1, but nums[2] has the smaller index. Hence, we multiply the score by nums[2]. The score becomes 9 * 9 = 81.
It can be proven that 81 is the highest score one can obtain.
```

**Example 2:**

```
Input: nums = [19,12,14,6,10,18], k = 3
Output: 4788
Explanation: To get a score of 4788, we can apply the following operations: 
- Choose subarray nums[0, ..., 0]. nums[0] is the only element in this subarray. Hence, we multiply the score by nums[0]. The score becomes 1 * 19 = 19.
- Choose subarray nums[5, ..., 5]. nums[5] is the only element in this subarray. Hence, we multiply the score by nums[5]. The score becomes 19 * 18 = 342.
- Choose subarray nums[2, ..., 3]. Both nums[2] and nums[3] have a prime score of 2, but nums[2] has the smaller index. Hence, we multipy the score by nums[2]. The score becomes 342 * 14 = 4788.
It can be proven that 4788 is the highest score one can obtain.
```

**Constraints**

- 1 <= nums.length == n <= 105
- 1 <= nums[i] <= 105
- 1 <= k <= min(n * (n + 1) / 2, 109)

---

## 题目（中文翻译）

你得到一个包含 **n** 个正整数的数组 `nums` 与一个整数 `k`。  
最初，你的得分为 `1`。你需要通过至多 `k` 次以下操作来最大化得分：

- 选择一个子数组 `nums[l, ..., r]`（下标从 `l` 到 `r`，两端均包含）。
- 在该子数组中，计算每个整数的 **质数得分（prime score）**——即该整数的不同质因数的个数。例如，`300 = 2 * 2 * 3 * 5 * 5`，其质数得分为 `3`。
- 选取质数得分最高的元素；若出现多个相同的最高质数得分，则取下标最小的那个。
- 用该元素的数值乘以当前得分，即 `score = score * nums[i]`（`i` 为上述选中的下标）。

在至多执行 `k` 次上述操作后，返回可能的最大得分。由于答案可能非常大，返回结果对 `10^9 + 7` 取模。

---

### 示例

#### 示例 1
> **输入**: `nums = [8,3,9,3,8]`, `k = 2`  
> **输出**: `81`  
> **解释**: 为了得到 `81`，可以执行以下操作:
> 1. 选择子数组 `nums[2, ..., 2]`（仅包含 `nums[2] = 9`），得分变为 `1 * 9 = 9`。  
> 2. 选择子数组 `nums[2, ..., 3]`。`nums[2]` 与 `nums[3]` 的质数得分均为 `1`，但 `nums[2]` 的下标更小，故选 `nums[2] = 9`，得分变为 `9 * 9 = 81`。

#### 示例 2
> **输入**: `nums = [19,12,14,6,10,18]`, `k = 3`  
> **输出**: `4788`  
> **解释**: 为了得到 `4788`，可以执行以下操作:
> 1. 选择子数组 `nums[0, ..., 0]`（仅包含 `nums[0] = 19`），得分变为 `1 * 19 = 19`。  
> 2. 选择子数组 `nums[5, ..., 5]`（仅包含 `nums[5] = 18`），得分变为 `19 * 18 = 342`。  
> 3. 再次选择子数组 `nums[5, ..., 5]`（仍为 `18`），得分变为 `342 * 18 = 4788`。

---

### 约束条件

- `1 <= nums.length == n <= 10^5`
- `1 <= nums[i] <= 10^5`
- `1 <= k <= min(n * (n + 1) / 2, 10^9)`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的子数组** 都枚举一遍：

1. 对每个子数组 `nums[l … r]`，遍历里面的元素，计算它们的 **prime score**（不同质因子的个数），找出 **prime score 最大且下标最小** 的那个位置 `i`。  
2. 这一次操作会把当前的 `score` 乘以 `nums[i]`。  
3. 我们可以执行至多 `k` 次操作，显然想让最终乘积最大，就应该把 **值最大的 `nums[i]`** 选出来 `k` 次（如果子数组的选择次数不足，则取所有能选到的）。

> **类比**：把所有子数组想象成一本“字典”，每一页记录了这段子数组会让我们乘以哪个数字。我们只需要挑出字典里价值最高的 `k` 页。

**为什么正确**：  
暴力枚举得到的每一次操作对应的乘数一定是**合法**的（因为它来源于某个子数组），而把最大的 `k` 个乘数相乘显然能得到最大可能的乘积——乘法满足“把大的数先乘，乘积会更大”。

**复杂度**：  
- 枚举子数组有 `n·(n+1)/2` 种，约 `O(n²)`。  
- 对每个子数组再遍历一次来找最大 prime score，最坏也是 `O(n)`，整体是 `O(n³)`，但我们可以在枚举时直接在 `O(1)` 里维护当前最大（把枚举改成两层循环），于是总时间是 **`O(n²)`**。  
- 需要额外存放所有得到的乘数，最坏 `O(n²)` 个，空间是 **`O(n²)`**。

> **大白话**：`O(n²)` 就相当于“如果 n 是 10⁴，运算次数大约是 10⁸”，对 10⁵ 的数据根本跑不完。

#### 代码（Python）

```python
MOD = 10**9 + 7

def prime_score(x: int) -> int:
    """返回整数 x 的不同质因子个数。"""
    cnt = 0
    d = 2
    while d * d <= x:
        if x % d == 0:
            cnt += 1
            while x % d == 0:          # 把同一个质因子除尽
                x //= d
        d += 1
    if x > 1:                           # 余下的 x 本身是质数
        cnt += 1
    return cnt

def maxScore_bruteforce(nums, k):
    n = len(nums)
    # 记录每一次合法操作会得到的乘数
    candidates = []

    # 两层循环枚举所有子数组
    for l in range(n):
        # 为了在 O(1) 内得到当前子数组的“最佳”元素，维护
        # 当前子数组里 prime_score 最大且下标最小的下标 idx
        max_score = -1
        idx = -1
        for r in range(l, n):
            # 只检查新增的元素 nums[r]
            cur_score = prime_score(nums[r])
            if cur_score > max_score or (cur_score == max_score and r < idx):
                max_score = cur_score
                idx = r
            # 这一次操作会把 score 乘以 nums[idx]
            candidates.append(nums[idx])

    # 选出最大的 k 个乘数
    candidates.sort(reverse=True)
    ans = 1
    for i in range(min(k, len(candidates))):
        ans = (ans * candidates[i]) % MOD
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 两层循环遍历所有子数组，每次只做 O(1) 的更新。  
- **空间复杂度**：`O(n²)` —— 需要把每一次可能的乘数都存下来，最坏会有 `n·(n+1)/2` 个。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在于 **枚举子数组**，子数组数量是二次级的 (`≈ n²`)。  
观察题目可以发现：

* 对于一次操作，真正决定乘积的是 **被选中的元素** `nums[i]`，而不是子数组本身。  
* 一个位置 `i` 会被选中的前提是：在子数组 `[l, r]` 中，`i` 的 **prime score** 是最大的（若相同则取左边的）。  
* 换句话说，只要我们知道 **有多少个子数组** 会让 `i` 成为“最大 prime score 的下标”，我们就能直接算出 `i` 能被使用的次数。

于是把注意力从 **子数组** 转向 **每个元素能被选中的子数组数量**。

---

#### 2.1 计算每个元素的 prime score  

用 O(√x) 的因式分解即可，`nums[i] ≤ 10⁵`，所以这一步总体是 `O(n·√10⁵) ≈ O(n·300)`，足够快。

---

#### 2.2 统计 “i 成为最大 prime score 的左、右边界”

对每个 `i`，我们需要：

- `left[i]`：在 `i` 左侧最近的下标 `j`，满足 `primeScore[j] ≥ primeScore[i]`（如果不存在记 `-1`）。  
- `right[i]`：在 `i` 右侧最近的下标 `j`，满足 `primeScore[j] > primeScore[i]`（如果不存在记 `n`）。

> **类比**：把 `primeScore` 看成山峰的高度。`left[i]` 是左边第一个不低于当前峰的山，`right[i]` 是右边第一个**更高**的山。我们想知道在两座更高/等高山之间，当前山是最高的（或左边最高、右边等高）。

这正是 **单调栈**（Monotonic Stack）能在 `O(n)` 时间内完成的工作：

- 从左到右遍历，用 **递增**（或非递减）栈维护下标，使得栈顶的 `primeScore` 总是 **严格大于** 当前元素时弹出，从而得到 `right[i]`。  
- 同理，从右到左遍历得到 `left[i]`。

---

#### 2.3 计算 `i` 能被选中的子数组个数  

若 `left[i] = L`、`right[i] = R`，则只要子数组的左端点 `l` 落在 `(L, i]`，右端点 `r` 落在 `[i, R)`，`i` 就是 **primeScore 最大且最左** 的元素。  
于是：

```
ranges[i] = (i - L) * (R - i)
```

这就是 “i 能被选中的子数组数量”。  

---

#### 2.4 贪心挑选 k 次操作  

现在我们把每个位置 `i` 看成一种“资源”，它可以被使用 `ranges[i]` 次，每次使用会把分数乘以 `nums[i]`。  
要让乘积最大，只需要把 **价值最大的资源** 用尽（或用到 k 为止）——**贪心**。

实现方式：

1. 按 **primeScore 降序**（若相同则 `nums[i]` 大的在前）把所有位置排好序。  
2. 依次取 `cnt = min(ranges[i], remaining_k)` 次，乘以 `nums[i]^cnt`（模 `1e9+7`），并把 `remaining_k -= cnt`。  
3. 当 `remaining_k` 变为 0 时结束。

**快速幂**（Binary Exponentiation）可以在 `O(log cnt)` 时间内算出 `nums[i]^cnt mod MOD`。

---

#### 2.5 正式算法步骤

1. 预处理所有 `primeScore[i]`。  
2. 用单调栈求 `left[i]`、`right[i]`。  
3. 计算 `ranges[i] = (i - left[i]) * (right[i] - i)`。  
4. 把 `(primeScore[i], nums[i], ranges[i])` 组成的元组放入列表，按 `primeScore` **降序** 排序。  
5. 逐个取元素，使用 **快速幂** 把 `nums[i]^use` 累乘到答案中，`use = min(ranges[i], k)`，并更新 `k`。  
6. 返回答案 `% MOD`。

> 整体时间 `O(n log n)`（排序主导），空间 `O(n)`（几个长度为 n 的数组）。

---

#### 代码（Python）

```python
MOD = 10**9 + 7

def prime_score(x: int) -> int:
    """返回 x 的不同质因子个数（O(sqrt(x))）"""
    cnt = 0
    d = 2
    while d * d <= x:
        if x % d == 0:
            cnt += 1
            while x % d == 0:
                x //= d
        d += 1
    if x > 1:
        cnt += 1
    return cnt

def fast_pow(a: int, e: int) -> int:
    """快速幂，计算 a^e % MOD"""
    res = 1
    a %= MOD
    while e:
        if e & 1:
            res = (res * a) % MOD
        a = (a * a) % MOD
        e >>= 1
    return res

def maxScore(nums, k):
    n = len(nums)

    # 1️⃣ 计算每个元素的 prime score
    score = [prime_score(x) for x in nums]

    # 2️⃣ 单调栈求 left（>=）和 right（>）
    left = [-1] * n
    right = [n] * n

    # 求 left：最近的左侧 >= 当前
    stack = []                     # 栈中保存下标，score 单调递减（不严格）
    for i in range(n):
        while stack and score[stack[-1]] < score[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    # 求 right：最近的右侧 > 当前
    stack.clear()
    for i in range(n-1, -1, -1):
        while stack and score[stack[-1]] <= score[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    # 3️⃣ 计算每个位置能被选中的子数组数量
    ranges = [(i - left[i]) * (right[i] - i) for i in range(n)]

    # 4️⃣ 按 prime score 降序（若相同，数值大的先）排序
    idxs = list(range(n))
    idxs.sort(key=lambda i: (-score[i], -nums[i]))

    ans = 1
    remaining = k

    # 5️⃣ 贪心取最大的 k 次乘数
    for i in idxs:
        if remaining == 0:
            break
        use = min(ranges[i], remaining)   # 这一次可以用多少次
        if use:
            ans = (ans * fast_pow(nums[i], use)) % MOD
            remaining -= use

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 计算 prime score：`O(n * sqrt(10⁵))` ≈ `O(n·300)`，线性。  
  - 单调栈求左右边界：`O(n)`。  
  - 排序：`O(n log n)`（这是主导）。  
  - 其余遍历、快速幂的总和 ≤ `O(n log k)`，远小于排序。  
  与暴力的 `O(n²)` 相比，提升巨大，能够轻松跑完 `n = 10⁵` 的极限。

- **空间复杂度**：`O(n)`  
  - `score、left、right、ranges` 各占 `n` 长度的数组。  
  - 单调栈最多 `n` 个下标。  

---

## 心得

- **核心技巧**：**单调栈 + 计数子数组**，把“子数组里谁是最大”转化为“每个元素支配多少子数组”。  
- **适用题型**：  
  1. “在所有子数组里，某个属性的最大/最小出现次数”——如 *Maximum Subarray Min-Product*、*Sum of Subarray Minimums*。  
  2. “每个元素作为某种“代表”的区间个数”——如 *Largest Rectangle in Histogram*、*Count Subarrays Where Max Is at Position i*。  
- **解题钥匙**：**把子数组的二次枚举压缩成每个元素一次的计数**，再用贪心挑最大值。

---

## 反思

- **第一反应**：看到“在子数组里取 prime score 最大的元素”，立刻想到暴力枚举所有子数组。  
- **最容易踩的坑**：  
  - **prime score 计算**：忘记去重，同一个质因子只算一次。  
  - **左/右边界的比较符号**：题目要求“若相同取左侧更小的下标”，左边界用 `>=`，右边界用 `>`，否则计数会出错。  
  - **大数取模**：直接乘会 overflow，需要使用 **快速幂** 与模运算。  
- **下次类似**：遇到“在每个子数组里挑选某种‘最大/最小’的元素”时，第一步就思考 **“每个位置支配多少子数组”**，尝试单调栈或前缀/后缀技巧来统计。这样可以把二次循环压到线性甚至线性对数级别。