# #3445. 最大偶数频率与奇数频率之差 II / Maximum Difference Between Even and Odd Frequency II

> 难度：困难 · 标签：String、Sliding Window、Enumeration、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-difference-between-even-and-odd-frequency-ii/)

---

## 题目（英文原版）

**Description**

You are given a string s and an integer k. Your task is to find the maximum difference between the frequency of two characters, freq[a] - freq[b], in a substring subs of s, such that:
Return the maximum difference.
Note that subs can contain more than 2 distinct characters.

**Examples**

**Example 1:**

```
Input: s = "12233", k = 4
Output: -1
Explanation:
For the substring "12233" , the frequency of '1' is 1 and the frequency of '3' is 2. The difference is 1 - 2 = -1 .
```

**Example 2:**

```
Input: s = "1122211", k = 3
Output: 1
Explanation:
For the substring "11222" , the frequency of '2' is 3 and the frequency of '1' is 2. The difference is 3 - 2 = 1 .
```

**Example 3:**

```
Input: s = "110", k = 3
Output: -1
```

**Constraints**

- 3 <= s.length <= 3 * 104
- s consists only of digits '0' to '4'.
- The input is generated that at least one substring has a character with an even frequency and a character with an odd frequency.
- 1 <= k <= s.length

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `k`。请在 `s` 的所有子串 `subs` 中，找到两个字符的频率差 `freq[a] - freq[b]` 的最大值，使得满足题目要求的条件（题目原文中此处条件未给出）。  
返回该最大差值。  
注意，`subs` 中可以出现超过 2 个不同的字符。

**示例 1**

```
Input: s = "12233", k = 4
Output: -1
Explanation:
对于子串 "12233"，字符 '1' 的频率为 1，字符 '3' 的频率为 2。差值为 1 - 2 = -1。
```

**示例 2**

```
Input: s = "1122211", k = 3
Output: 1
Explanation:
对于子串 "11222"，字符 '2' 的频率为 3，字符 '1' 的频率为 2。差值为 3 - 2 = 1。
```

**示例 3**

```
Input: s = "110", k = 3
Output: -1
```

### 约束条件
- `3 <= s.length <= 3 * 10^4`
- `s` 仅由字符 `'0'` 到 `'4'` 组成
- 输入保证至少存在一个子串，其中有字符的频率为偶数，另有字符的频率为奇数
- `1 <= k <= s.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的做法是把所有可能的子串枚举出来，统计每个子串里 **每个字符出现的次数**，再在这些次数中挑选：

* 一个出现次数为 **奇数** 的字符 `a`（我们记为 “odd”），  
* 一个出现次数为 **偶数** 的字符 `b`（我们记为 “even”），  

计算 `freq[a] - freq[b]`，取所有子串、所有合法 `(a,b)` 组合的最大值即为答案。

> **类比**：把字符串想象成一排书架，每本书的编号是字符。暴力解就是把每一种可能的「连续取几本书」的方式都列出来，然后一个个数数每本书出现了几次，再挑出「出现次数是奇数的书」和「出现次数是偶数的书」算差值。

**为什么一定能得到正确答案**  
因为我们把 **所有** 合法子串以及 **所有** 合法字符对都遍历了一遍，最大值自然不会漏掉。

**复杂度分析（大白话）**  

* 子串的个数是 `n*(n+1)/2`（大约是 `n²/2`），每个子串要遍历一次字符统计频率，又是 `O(length)`，所以总时间是 **平方级**，记作 `O(n²)`（`n` 代表字符串长度）。  
* 统计频率需要一个大小为 5（字符只有 `'0'~'4'`）的数组，空间是 **常数级**，记作 `O(1)`。

> `O(n²)` 可以理解为：如果字符串长 10,000，算法大约要跑 100,000,000 次，明显会超时。

#### 代码（Python）

```python
def maxDiff_bruteforce(s: str, k: int) -> int:
    n = len(s)
    ans = -10**9                     # 先设一个很小的值

    # 枚举所有子串的左端点
    for left in range(n):
        cnt = [0] * 5                # 记录 0~4 每个字符的出现次数
        # 右端点从 left 开始向右扩展
        for right in range(left, n):
            cnt[int(s[right])] += 1

            # 只考虑长度 >= k 的子串
            if right - left + 1 < k:
                continue

            # 在当前子串里挑选 odd / even 的字符对
            for a in range(5):       # a 负责 odd
                if cnt[a] % 2 == 1: # 出现次数是奇数
                    for b in range(5):   # b 负责 even
                        if a == b:
                            continue
                        if cnt[b] % 2 == 0 and cnt[b] > 0:   # 偶数且出现过
                            ans = max(ans, cnt[a] - cnt[b])
    return ans
```

#### 复杂度

* **时间复杂度**：`O(n²)` —— 两层循环枚举子串，内部再遍历常数个字符（5×5），整体仍是平方级。  
* **空间复杂度**：`O(1)` —— 只用了长度为 5 的计数数组和若干常数变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有子串**。我们需要一种办法，只在 **一次遍历**（或少数遍历）中就能得到所有子串的 “奇数字符‑偶数字符” 差值的最大值。

观察题目可以发现：

1. **字符种类只有 5**（`'0'~'4'`），所以我们可以把 **奇数字符** 和 **偶数字符** 这两个角色 **固定**，分别遍历所有可能的配对。  
2. 对于固定的配对 `(odd_char, even_char)`，我们只关心这两个字符在子串中的出现次数，其他字符的出现对差值没有影响（它们的贡献是 0）。  
3. 把这两个字符映射成 **数值**：
   * `odd_char` → `+1`（出现一次，差值加 1）  
   * `even_char` → `-1`（出现一次，差值减 1）  
   * 其它字符 → `0`  

   那么子串 `subs` 的 `freq[odd] - freq[even]` 正好等于 **子串对应的数值和**。

   这把原本的 “统计频率再相减” 转化成了 **求子数组的和**。

4. 现在问题变成：

   > 在一个只包含 `+1 / -1 / 0` 的数组里，找出 **长度 ≥ k** 的子数组，使其和最大。

   这正是「**带长度下界的最大子段和**」问题，经典解法是 **前缀和 + 单调队列 / 最小前缀**。

5. **前缀和**：  
   `pre[i]` 表示前 `i` 个字符（下标 `[0, i)`）对应的数值和。  
   子数组 `[l, r)` 的和 = `pre[r] - pre[l]`。

   为了让子数组长度 ≥ k，`r - l ≥ k` → `l ≤ r - k`。  
   对于每个右端点 `r`，我们只需要知道 **在 `0 … r‑k` 之间的最小前缀和** `min_pre`，因为  
   `pre[r] - min_pre` 就是以 `r` 为右端点、满足长度条件的最大可能和。

   于是遍历一遍数组，维护 `min_pre`（可以用一个变量或单调队列），即可在 **O(n)** 时间得到当前配对的最佳差值。

6. **遍历所有配对**：  
   共计 `5 * 4 = 20` 种不同的 `(odd, even)`（不能相同），每种配对 O(n) 时间，总体 O(20·n) ≈ O(n)。

> **类比**：把字符串看成一条路，上面有红灯（`odd_char`）和绿灯（`even_char`），我们把红灯记作 “+1”，绿灯记作 “‑1”。现在要找一段路，走的步数不少于 `k`，让“红灯的加分”减去“绿灯的扣分”尽可能高。前缀和就像在每一步记下累计的分数，最小前缀和相当于“最早的低谷”，从低谷到现在的上升就是我们想要的最大收益。

#### 代码（Python）

```python
def maxDiff_opt(s: str, k: int) -> int:
    n = len(s)
    digits = [int(ch) for ch in s]          # 方便下标访问
    best = -10**9                            # 记录全局最大值

    # 只要 odd != even，遍历所有可能的配对
    for odd in range(5):
        for even in range(5):
            if odd == even:
                continue

            # 1. 把字符串映射成 +1 / -1 / 0 的数组
            vals = [0] * n
            for i, d in enumerate(digits):
                if d == odd:
                    vals[i] = 1
                elif d == even:
                    vals[i] = -1
                # else 0，保持不变

            # 2. 前缀和 + 滑动窗口求最长 ≥ k 的最大子段和
            pre = 0                     # 当前前缀和
            min_pre = 0                 # 在窗口左边界之前的最小前缀和
            # 为了让 min_pre 只考虑下标 ≤ i-k，需要提前把前 k 个元素的前缀和放进队列
            prefix_queue = [0]         # 存放 pre[0], pre[1], …，随 i 增长
            for i in range(1, n + 1):
                pre += vals[i - 1]      # pre = sum(vals[0..i-1])

                # 当 i >= k 时，左端点可以最早是 i-k
                if i >= k:
                    # 更新 min_pre 为 prefix_queue[0..i-k] 的最小值
                    # 这里用一个变量维护最小值更快
                    # 先把第 i-k 位置的前缀和加入候选
                    candidate = prefix_queue[i - k]
                    if candidate < min_pre:
                        min_pre = candidate

                    # 计算以 i 为右端点、长度≥k 的子数组最大和
                    cur = pre - min_pre
                    if cur > best:
                        best = cur

                # 把当前的前缀和放进队列，供以后使用
                prefix_queue.append(pre)

    return best
```

> **代码要点解释**  
> 1. `vals` 把只有两个关心的字符映射成 `+1 / -1`，其余字符为 `0`。  
> 2. `pre` 是滚动的前缀和，`prefix_queue` 保存所有历史前缀和（下标对应），这样可以在 `i >= k` 时直接取 `pre[i‑k]` 进行比较。  
> 3. `min_pre` 只会变小（取最小），因此只用一个变量即可，不需要真正的单调队列。  
> 4. 每个配对的循环里只遍历一次字符串，时间是 `O(n)`，外层 20 次配对得到总体 `O(20·n)`。

#### 复杂度

* **时间复杂度**：`O(20·n) = O(n)`（`n` ≤ 3·10⁴，常数 20 完全可以接受）。  
  与暴力的 `O(n²)` 相比，数量级从 **平方级** 降到了 **线性级**，即使 `n = 30000` 也只需要几万次运算，毫秒级完成。

* **空间复杂度**：`O(n)` 用于保存 `prefix_queue`（也可以改写成 `O(1)`，只保留最新的 `pre` 与 `min_pre`），整体是线性或常数空间。

---

## 心得

* **核心技巧**：把「奇数频率‑偶数频率」的差值转化为「+1 / -1 / 0」数组的子段和，然后用 **前缀和 + 最小前缀维护** 求 **带长度下界的最大子段和**。  
* **适用场景**  
  1. 「在数组中找长度 ≥ k 的子数组，使其和最大」——如本题、或「最长子数组和 ≥ 某阈值」等。  
  2. 「把多种字符的出现次数映射成数值，再求子串的最优值」——比如「Maximum Difference Between Even and Odd Frequency I」或「字符权值最大子串」类问题。  
  3. 「固定两类元素的权重 (+1 / -1)」的组合优化——如「最大子数组的正负数差」等。

* **一句话总结**：  
  **把频率差转成加减分，前缀最小值帮你一次遍历搞定所有满足长度下界的子串。**

---

## 反思

* **第一反应**：直接枚举所有子串，统计频率，虽然能想到答案，却忽略了 `n` 可达 30,000，暴力必超时。  
* **最容易踩的坑**  
  * **长度下界**：忘记只考虑长度 **≥ k** 的子串，导致算错或超时。  
  * **字符配对**：`odd` 与 `even` 不能是同一个字符，需要显式排除。  
  * **负数答案**：最大差值可能是负数，初始化答案时要足够小，不能直接用 `0`。  
  * **前缀最小值的更新时机**：必须在右端点 `i` 达到 `k` 时才把 `pre[i‑k]` 加入候选，否则会误算长度不足的子串。  

* **下次类似题目**：  
  1. **先把问题抽象为数值数组**（+1 / -1 / 0），看能否用前缀和或滑动窗口求最值。  
  2. **确认是否有长度、数量等约束**，如果有，就在遍历时维护对应的 “窗口左边界” 或 “最小前缀”。  
  3. **枚举固定的“小集合”**（本题是 5×4 种字符配对），把指数级的组合压到常数因子。  

祝你玩转算法，稳步提升！