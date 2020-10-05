# #1010. **歌曲时长总和能被 60 整除的配对数** / Pairs of Songs With Total Durations Divisible by 60

> 难度：中等 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/pairs-of-songs-with-total-durations-divisible-by-60/)

---

## 题目（英文原版）

**Description**

You are given a list of songs where the ith song has a duration of time[i] seconds.
Return the number of pairs of songs for which their total duration in seconds is divisible by 60. Formally, we want the number of indices i, j such that i < j with (time[i] + time[j]) % 60 == 0.

**Examples**

**Example 1:**

```
Input: time = [30,20,150,100,40]
Output: 3
Explanation: Three pairs have a total duration divisible by 60:
(time[0] = 30, time[2] = 150): total duration 180
(time[1] = 20, time[3] = 100): total duration 120
(time[1] = 20, time[4] = 40): total duration 60
```

**Example 2:**

```
Input: time = [60,60,60]
Output: 3
Explanation: All three pairs have a total duration of 120, which is divisible by 60.
```

**Constraints**

- 1 <= time.length <= 6 * 104
- 1 <= time[i] <= 500

---

## 题目（中文翻译）

给定一个歌曲列表，第 `i` 首歌的时长为 `time[i]` 秒。返回满足两首歌的总时长能够被 **60** 整除的配对数量。形式化地，我们需要统计满足 `i < j` 且 `(time[i] + time[j]) % 60 == 0` 的下标对 `(i, j)` 的个数。

---

### 示例 1
**输入**  
`time = [30,20,150,100,40]`

**输出**  
`3`

**解释**  
有三组配对的总时长能被 60 整除：
- `(time[0] = 30, time[2] = 150)`: 总时长 `180`
- `(time[1] = 20, time[3] = 100)`: 总时长 `120`
- `(time[1] = 20, time[4] = 40)`: 总时长 `60`

---

### 示例 2
**输入**  
`time = [60,60,60]`

**输出**  
`3`

**解释**  
所有三组配对的总时长都是 `120`，能够被 60 整除。

---

### 约束条件
- `1 <= time.length <= 6 * 10^4`
- `1 <= time[i] <= 500`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有歌曲两两配对，检查它们的时长之和是否能被 60 整除。  
- **数据结构**：只需要一个普通的列表 `time`，我们用两层 `for` 循环遍历所有下标组合 `(i, j)`，其中 `i < j`。  
- **生活化类比**：把每首歌想成一张卡片，暴力解相当于把卡片全部摆成一排，然后把每两张卡片都拿出来配对检查——就像在超市里把每件商品都和其他商品比价，费时费力但一定能找到所有符合条件的组合。  
- **正确性**：因为我们枚举了所有可能的 `(i, j)`，只要满足 `(time[i] + time[j]) % 60 == 0` 就计数，所以不会漏掉任何合法的配对。

#### 代码（Python）

```python
from typing import List

def numPairsDivisibleBy60_bruteforce(time: List[int]) -> int:
    n = len(time)
    ans = 0                     # 用来累计符合条件的配对数量
    # 两层循环，i 从 0 到 n-2，j 从 i+1 到 n-1
    for i in range(n - 1):
        for j in range(i + 1, n):
            total = time[i] + time[j]          # 两首歌的总时长
            if total % 60 == 0:                # 能被 60 整除吗？
                ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：我们用了两层循环，外层 `n` 次，内层最多 `n-1` 次，整体大约是 `n × n`，也就是平方级别。对 60,000 首歌来说，`n²` 约等于 3.6 × 10⁹ 次运算，计算机几乎跑不完。

- **空间复杂度**：`O(1)`  
  解释：只用了常数个额外变量（`ans`、`i`、`j`、`total`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈在于两层遍历**——我们在重复检查相同的“余数”信息。  
关键观察：

1. **只关心余数**  
   两个数之和能被 60 整除，等价于它们各自对 60 取模后的余数之和为 60（或为 0）。  
   举例：`20 % 60 = 20`，`40 % 60 = 40`，`20 + 40 = 60`，所以这两首歌配对成功。

2. **余数的配对规律**  
   - 若余数为 `0`，只能和另一个余数为 `0` 的歌曲配对。  
   - 若余数为 `r (1 ≤ r ≤ 29)`，只能和余数为 `60 - r` 的歌曲配对。  
   - 若余数为 `30`，只能和另一个余数为 `30` 的歌曲配对（因为 `30 + 30 = 60`）。

3. **计数即可**  
   我们只需要统计每个余数出现了多少次，然后根据上面的配对规则算出合法配对的数量。  
   - 用一个长度为 60 的数组 `cnt`（或者字典）记录 `time[i] % 60` 的出现次数。  
   - 对于余数 `0` 和 `30`，配对数是 `C(cnt[r], 2) = cnt[r] * (cnt[r] - 1) // 2`（从 cnt[r] 个元素中任选两个）。  
   - 对于其它余数 `r`（1~29），配对数是 `cnt[r] * cnt[60 - r]`，因为每个余数 `r` 的歌曲都可以和每个余数 `60-r` 的歌曲配对。

**类比**：把余数看成“颜色”，我们把同颜色的球放进 60 个格子里。配对规则就是“红色只能和蓝色配，对应的颜色编号相加等于 60”。统计每种颜色的数量后，用乘法直接算出有多少红蓝组合，而不必一个一个去挑。

#### 代码（Python）

```python
from typing import List

def numPairsDivisibleBy60(time: List[int]) -> int:
    # cnt[i] 表示余数为 i 的歌曲出现了多少次
    cnt = [0] * 60
    for t in time:
        r = t % 60               # 余数
        cnt[r] += 1

    ans = 0

    # 余数为 0 的配对：从 cnt[0] 首歌里任选两首
    ans += cnt[0] * (cnt[0] - 1) // 2

    # 余数为 30 的配对：同理
    ans += cnt[30] * (cnt[30] - 1) // 2

    # 余数 1~29 与 59~31 配对
    for r in range(1, 30):
        ans += cnt[r] * cnt[60 - r]

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n + 60)` → 实际上是 `O(n)`  
  解释：我们只遍历一次数组 `time`（`n` 次），再遍历固定的 60 个余数（常数），所以整体随 `n` 线性增长。对 60,000 首歌来说，只需要约 60,000 次简单运算，轻松跑完。

- **空间复杂度**：`O(60)` → 实际上是 `O(1)`  
  解释：只用了一个长度固定为 60 的计数数组，大小不随输入规模变化。

---

## 心得

- **核心技巧**：利用取模的“余数配对”思想，把原本的两数求和问题转化为计数问题。  
- **适用的题型**  
  1. “两个数之和能被 k 整除”类（如 LeetCode 1497）  
  2. “子数组和能被 k 整除”类（如 LeetCode 974）  
  3. “找出满足某种模运算关系的配对”类（如 0/1 背包的模数压缩）  
- **一句话总结**：**把问题压到 60 个余数上，用计数直接算配对**。

---

## 反思

- **第一反应**：看到“% 60”，立刻想到只要关注每首歌的余数就行，进而想到哈希表/计数数组。  
- **最容易踩的坑**  
  - 忘记处理余数为 `0` 和 `30` 的特殊配对，需要用组合数 `C(n,2)` 而不是直接乘。  
  - 对于余数 `r` 与 `60-r` 配对时，容易双计数（比如同时遍历 `r` 和 `60-r`），所以只遍历 `1~29` 即可。  
- **下次第一步**：把所有数取模 `k`，统计每个余数的出现次数，再根据“余数之和为 k（或 0）”的配对规则直接计数。