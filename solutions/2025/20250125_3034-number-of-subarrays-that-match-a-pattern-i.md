# #3034. **匹配模式的子数组数量 I** / Number of Subarrays That Match a Pattern I

> 难度：中等 · 标签：Array、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/number-of-subarrays-that-match-a-pattern-i/)

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

- 2 <= n == nums.length <= 100
- 1 <= nums[i] <= 109
- 1 <= m == pattern.length < n
- -1 <= pattern[i] <= 1

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`，长度为 `n`，以及一个下标从 0 开始、长度为 `m` 的整数数组 `pattern`，其中 `pattern` 的元素仅为 **-1、0、1**。  

长度为 `m + 1` 的子数组 `nums[i..j]`（其中 `j = i + m`）如果满足下列条件，则称其**匹配**该模式：

- 对于每个 `k`（`0 ≤ k < m`），`sign(nums[i + k + 1] - nums[i + k]) = pattern[k]`。  
  其中 `sign`（符号函数）定义为  
  - `sign(x) = -1` 当 `x < 0`  
  - `sign(x) = 0` 当 `x = 0`  
  - `sign(x) = 1` 当 `x > 0`  

返回 `nums` 中匹配该模式的子数组的数量。

---

### 示例

**示例 1**  
```text
输入: nums = [1,2,3,4,5,6], pattern = [1,1]
输出: 4
解释: 模式 [1,1] 表示我们在寻找严格递增的长度为 3 的子数组。  
在数组 nums 中，子数组 [1,2,3]、[2,3,4]、[3,4,5]、[4,5,6] 都匹配该模式。  
因此，满足条件的子数组共有 4 个。
```

**示例 2**  
```text
输入: nums = [1,4,4,1,3,5,5,3], pattern = [1,0,-1]
输出: 2
解释: 模式 [1,0,-1] 表示我们在寻找一个序列，使得  
- 第一个数小于第二个数，  
- 第二个数等于第三个数，  
- 第三个数大于第四个数。  
在数组 nums 中，子数组 [1,4,4,1] 和 [3,5,5,3] 均匹配该模式。  
因此，满足条件的子数组共有 2 个。
```

---

### 约束

- `2 ≤ n == nums.length ≤ 100`
- `1 ≤ nums[i] ≤ 10^9`
- `1 ≤ m == pattern.length < n`
- `-1 ≤ pattern[i] ≤ 1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

1. **把题目翻译成“找子串”**  
   - 对于相邻的两个数 `a, b`，我们只关心它们的相对大小：  
     - `b > a` → 记作 `+1`（上升）  
     - `b == a` → 记作 `0`（相等）  
     - `b < a` → 记作 `-1`（下降）  
   - 于是原数组 `nums` 可以转化成一个 **差分符号数组** `sign`，长度为 `n‑1`，每个元素只可能是 `-1、0、1`。  
   - 题目要求我们找出所有长度为 `m+1` 的子数组，使得它们相邻差分的符号序列恰好等于给定的 `pattern`（长度 `m`）。  
   - 换句话说，就是在 `sign` 中找所有与 `pattern` 完全相同的连续片段。

2. **最直接的做法**  
   - 从左到右枚举子数组的起始位置 `i`（`0 ≤ i ≤ n‑m‑1`）。  
   - 对每个 `i`，用第二个循环检查 `sign[i … i+m‑1]` 是否和 `pattern` 完全相同。  
   - 如果全部匹配，就把答案计数加一。

3. **为什么一定对**  
   - 我们把每个子数组的相对关系抽象成了符号序列，**相等**的子数组必然产生**相同**的符号序列，反之亦然。  
   - 因此只要符号序列匹配，原始子数组就一定满足题目条件。

4. **时间/空间复杂度的“大白话”**  
   - 外层循环遍历 `n`（最多 100）次，内层最多比较 `m`（也不大）次。  
   - 所以总共要做大约 `n × m` 次比较，记作 **O(n·m)**。  
   - 这里的 `O` 只是一种“量级”描述，实际数字很小（最多 10⁴ 次比较），所以在本题的限制下也能跑完。  
   - 额外空间只用了一个长度为 `n‑1` 的 `sign` 数组，大小随 `n` 线性增长，记作 **O(n)**。

#### 代码（Python）

```python
def countMatchingSubarrays(nums, pattern):
    n = len(nums)
    m = len(pattern)

    # 1️⃣ 先把相邻差分转成符号数组，类似“查字典”里把单词拆成字母
    sign = []
    for i in range(n - 1):
        if nums[i + 1] > nums[i]:
            sign.append(1)          # 上升
        elif nums[i + 1] == nums[i]:
            sign.append(0)          # 相等
        else:
            sign.append(-1)         # 下降

    ans = 0
    # 2️⃣ 枚举所有可能的起始位置 i
    for i in range(n - m):
        ok = True
        # 3️⃣ 检查长度为 m 的窗口是否和 pattern 完全相同
        for k in range(m):
            if sign[i + k] != pattern[k]:
                ok = False          # 只要有一个不相等，就不匹配
                break
        if ok:
            ans += 1                # 找到一个符合条件的子数组

    return ans
```

#### 复杂度  

- **时间复杂度：O(n·m)**  
  - 这里的 `n·m` 可以想象成“把一本 100 页的书每页都读 `m` 次”，总工作量随 `n` 和 `m` 的乘积增长。  
- **空间复杂度：O(n)**  
  - 只用了一个和原数组长度成正比的 `sign` 数组，类似于在原书的每一页旁边贴了一张小便签。  

---  

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于每次都要把窗口里的 `m` 个符号逐个比较一次。  
如果我们能在 **O(1)** 时间内判断两个窗口是否相同，就能把整体复杂度降到 **O(n)**。

**思路转变：把符号序列看成一串字符，使用字符串匹配的技巧**  

1. **把 `sign` 与 `pattern` 当作“字符串”**  
   - 每个符号 `-1、0、1` 就是一个字符。  
   - 要找的其实是 `pattern` 在 `sign` 中出现的次数。

2. **Rabin‑Karp 滚动哈希**（类似“指纹比对”）  
   - 先给每个字符一个数值（这里已经是 -1、0、1），再选一个 **基数**（比如 3）和 **模数**（大质数 10⁹+7）来计算**哈希值**。  
   - 哈希值的好处是：**相同的序列必然得到相同的哈希**（在模数范围内），不同的序列大概率得到不同的哈希。  
   - 计算 `pattern` 的哈希 `hash_pat`。  
   - 计算 `sign` 前 `m` 个字符的哈希 `hash_win`。  
   - 然后把窗口向右滑动一格：  
     - 先把左边即将离开的字符 “减掉”。  
     - 再把右边新进来的字符 “加进去”。  
     - 这一步只用了常数时间，称为 **滚动**。  
   - 每次窗口哈希等于 `hash_pat` 时，再**一次完整比较**（防止哈希冲突），确认真的匹配。

3. **为什么滚动哈希是 O(1) 的**  
   - 哈希公式：`H = (a0 * B^{m-1} + a1 * B^{m-2} + ... + a_{m-1}) mod MOD`。  
   - 当窗口左移时，只需要把最左边的 `a0 * B^{m-1}` 去掉，再乘以 `B`（相当于整体左移一位），最后加上新来的字符。  
   - 这四步都是常数时间，不会随 `m` 增长。

4. **整体复杂度**  
   - 预处理 `sign`：O(n)  
   - 计算第一个窗口哈希：O(m)（只做一次）  
   - 滚动窗口 n‑m 次，每次 O(1) → O(n)  
   - 只在哈希相等时再做一次 O(m) 的确认，但这种情况极少，整体仍是 O(n)。  

#### 代码（Python）

```python
def countMatchingSubarrays(nums, pattern):
    n = len(nums)
    m = len(pattern)

    # ---------- 1️⃣ 把 nums 转成符号数组 ----------
    sign = []
    for i in range(n - 1):
        if nums[i + 1] > nums[i]:
            sign.append(1)
        elif nums[i + 1] == nums[i]:
            sign.append(0)
        else:
            sign.append(-1)

    # ---------- 2️⃣ Rabin‑Karp 参数 ----------
    MOD = 10 ** 9 + 7          # 大质数，防止哈希值溢出
    BASE = 3                    # 基数，足够区分 -1、0、1（实际使用 4 防止负数冲突）
    # 为了避免负数影响哈希，先把 -1、0、1 映射到正数
    offset = 2                  # -1 -> 1, 0 -> 2, 1 -> 3
    pat = [x + offset for x in pattern]
    sgn = [x + offset for x in sign]

    # ---------- 3️⃣ 计算 pattern 的哈希 ----------
    hash_pat = 0
    for v in pat:
        hash_pat = (hash_pat * BASE + v) % MOD

    # ---------- 4️⃣ 计算第一个窗口的哈希 ----------
    hash_win = 0
    for i in range(m):
        hash_win = (hash_win * BASE + sgn[i]) % MOD

    # 预计算 BASE^{m-1}，后面滚动窗口时要用到
    power = pow(BASE, m - 1, MOD)

    ans = 0
    # ---------- 5️⃣ 滑动窗口 ----------
    for i in range(n - m):
        # 哈希相等时再做一次完整比较，防止冲突
        if hash_win == hash_pat:
            # 直接对符号序列做线性比较（长度只有 m，开销极小）
            if sgn[i:i + m] == pat:
                ans += 1

        # 把窗口右移一格（除非已经是最后一个窗口）
        if i + m < len(sgn):
            # ① 去掉最左边的字符贡献
            left_val = sgn[i]
            hash_win = (hash_win - left_val * power) % MOD
            # ② 整体左移一位，相当于乘以 BASE
            hash_win = (hash_win * BASE) % MOD
            # ③ 加上新进来的字符
            hash_win = (hash_win + sgn[i + m]) % MOD
            # 为了防止 Python 的负模，统一取正数
            hash_win = (hash_win + MOD) % MOD

    return ans
```

#### 复杂度  

- **时间复杂度：O(n)**  
  - 只遍历了一遍 `sign`（长度 `n‑1`），窗口移动每次都是常数时间。  
  - 与暴力解相比，省掉了每次 `m` 次的比较，尤其当 `m` 接近 `n` 时，提升非常明显。  
- **空间复杂度：O(n)**  
  - 仍需要存放 `sign`（长度 `n‑1`）以及几个常数级的临时变量。  
  - 与暴力解的空间使用相同，未增加额外的复杂结构。  

---  

## 心得  

- **核心技巧**：把“相邻大小关系”抽象为符号序列，再把子数组匹配问题转化为“字符串匹配”。  
- **适用场景**  
  1. **子数组/子串的相对关系匹配**（如 “模式匹配 I/II” 系列）  
  2. **固定长度窗口的模式匹配**（如 “Find All Anagrams in a String”）  
  3. **基于差分的相等判断**（如 “Maximum Number of Consecutive Subarrays With Equal Sum”）  
- **一句话总结解题钥匙**：**把数组压缩成只保留“相对关系”的符号序列，然后用线性时间的滚动哈希（或 KMP）在这条“字符线上”快速定位匹配**。  

---  

## 反思  

- **第一反应**：直接把每个子数组的相邻差分一个个算，然后逐一比较——也就是暴力解。  
- **最容易踩的坑**  
  - **边界**：子数组长度是 `m+1`，所以差分窗口长度是 `m`；要注意循环上界 `n‑m`（而不是 `n‑m‑1`）。  
  - **负数哈希**：直接使用 `-1、0、1` 计算哈希会出现负数，导致取模错误，需要先做偏移。  
  - **哈希冲突**：虽然概率极低，但仍需在哈希相等时做一次完整比较，以保证答案正确。  
- **下次遇到同类题**：  
  1. 先思考能否把“数值”转换成更小的“特征”（如符号、差分、是否为素数等）。  
  2. 再判断是**一次性遍历**能解决，还是需要**字符串匹配**（KMP、滚动哈希）这种更高效的技巧。  

祝你在算法的路上越走越稳 🚀