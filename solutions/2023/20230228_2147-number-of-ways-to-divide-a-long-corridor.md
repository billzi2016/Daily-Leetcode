# #2147. 划分长走廊的方案数 / Number of Ways to Divide a Long Corridor

> 难度：困难 · 标签：Math、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-divide-a-long-corridor/)

---

## 题目（英文原版）

**Description**

Along a long library corridor, there is a line of seats and decorative plants. You are given a 0-indexed string corridor of length n consisting of letters 'S' and 'P' where each 'S' represents a seat and each 'P' represents a plant.
One room divider has already been installed to the left of index 0, and another to the right of index n - 1. Additional room dividers can be installed. For each position between indices i - 1 and i (1 <= i <= n - 1), at most one divider can be installed.
Divide the corridor into non-overlapping sections, where each section has exactly two seats with any number of plants. There may be multiple ways to perform the division. Two ways are different if there is a position with a room divider installed in the first way but not in the second way.
Return the number of ways to divide the corridor. Since the answer may be very large, return it modulo 109 + 7. If there is no way, return 0.

**Examples**

**Example 1:**

```
Input: corridor = "SSPPSPS"
Output: 3
Explanation: There are 3 different ways to divide the corridor.
The black bars in the above image indicate the two room dividers already installed.
Note that in each of the ways, each section has exactly two seats.
```

**Example 2:**

```
Input: corridor = "PPSPSP"
Output: 1
Explanation: There is only 1 way to divide the corridor, by not installing any additional dividers.
Installing any would create some section that does not have exactly two seats.
```

**Example 3:**

```
Input: corridor = "S"
Output: 0
Explanation: There is no way to divide the corridor because there will always be a section that does not have exactly two seats.
```

**Constraints**

- n == corridor.length
- 1 <= n <= 105
- corridor[i] is either 'S' or 'P'.

---

## 题目（中文翻译）

**描述**  
在一条长图书馆走廊（corridor）上，依次排列着座位（seat）和装饰植物（plant）。给定一个下标从 0 开始的字符串 `corridor`，长度为 `n`，仅由字符 `'S'`（座位）和 `'P'`（植物）组成，其中每个 `'S'` 表示一个座位，每个 `'P'` 表示一株植物。  

走廊的左侧（下标 `0` 的左边）已经安装了一块隔断（room divider），右侧（下标 `n‑1` 的右边）也已安装了一块隔断。可以在走廊的任意位置再安装额外的隔断。对于每个下标 `i`（`1 ≤ i ≤ n‑1`）之间的间隙，即下标 `i‑1` 与 `i` 之间，至多只能安装一块隔断。  

将走廊划分为若干不重叠的区间（section），要求每个区间恰好包含 **两个** 座位，且植物的数量不受限制。可能存在多种划分方式。若两种划分在至少一个位置的隔断安装情况不同，则视为不同的划分。  

返回将走廊划分满足上述条件的方案数。由于答案可能非常大，请返回 `10^9 + 7` 取模后的结果。如果不存在合法划分，返回 `0`。

**示例**

> 示例 1  
> 输入: `corridor = "SSPPSPS"`  
> 输出: `3`  
> 解释: 有 3 种不同的划分方式。图中黑色竖线表示已经安装的两块隔断。可以看到，每个划分得到的每个区间都恰好包含两个座位。

> 示例 2  
> 输入: `corridor = "PPSPSP"`  
> 输出: `1`  
> 解释: 仅有 1 种合法划分，即不再安装任何额外的隔断。若再安装任意隔断，必然会出现某个区间座位数不为 2 的情况。

> 示例 3  
> 输入: `corridor = "S"`  
> 输出: `0`  
> 解释: 无法进行合法划分，因为无论如何都会出现座位数不为 2 的区间。

**约束条件**

- `n == corridor.length`
- `1 ≤ n ≤ 10^5`
- `corridor[i]` 仅为 `'S'` 或 `'P'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的分隔符放法枚举一遍**，然后检验每一种是否满足“每段恰好有两把座位”。  
我们可以把走廊看成一串字符，每两个相邻字符之间（共 `n‑1` 个缝）都可以选择 **放** 或 **不放** 分隔符（左端 0、右端 `n‑1` 已经固定有分隔符），于是所有方案的总数是 `2^(n‑1)`，这在最坏情况下会达到 `2^99999`——根本不可能在电脑里跑完。

> **类比**：把走廊想象成一条长长的铁轨，铁轨上每隔一段可以放一根木栅栏。要检查所有木栅栏的摆放方式，需要把每根栅栏的“开/关”状态全部列举出来，数量会像指数一样爆炸。

**为什么暴力方法正确**  
- 每一种放置方式都对应唯一的划分（因为分隔符把走廊切成若干段）。  
- 检查每段是否恰好有两把座位，只要遍历一次走廊，统计每段的 `S` 数目即可。

**时间/空间复杂度**  
- 时间复杂度：`O(2^{n})`（指数级），因为要尝试所有可能的放置组合。  
- 空间复杂度：`O(n)`（用于保存当前划分的计数），但这在指数时间面前毫无意义。

> **大白话**：`O(2^{n})` 就像每增加一个字符，就要把所有可能的“开/关”组合翻一遍，几乎不可能在几秒钟内完成。

#### 代码（Python）

```python
from itertools import product

def brute_force(corridor: str) -> int:
    n = len(corridor)
    # n-1 个可以放分隔符的缝，枚举每个缝的放置状态（0=不放，1=放）
    ans = 0
    for mask in product([0, 1], repeat=n - 1):
        # 两端已经有分隔符，统一在列表两端加上 1 表示“有分隔符”
        cuts = [1] + list(mask) + [1]          # 长度为 n+1，方便切段
        ok = True
        seat_cnt = 0                           # 当前段的座位数
        for i, ch in enumerate(corridor):
            if ch == 'S':
                seat_cnt += 1
            # 如果在 i 与 i+1 之间放了分隔符，检查当前段
            if cuts[i + 1] == 1:               # 这里 i+1 对应缝 i~i+1
                if seat_cnt != 2:              # 必须恰好两把座位
                    ok = False
                    break
                seat_cnt = 0                    # 进入下一段
        if ok:
            ans += 1
    return ans % (10**9 + 7)
```

> 这段代码只能在 `n ≤ 15` 左右跑通，足以说明暴力思路，但对正式测试会 TLE（超时）。

#### 复杂度

- **时间复杂度**：`O(2^{n})` —— 随着走廊长度指数增长，根本不可接受。  
- **空间复杂度**：`O(n)` —— 只用来存放临时的切分状态。

---

### 2. 最优解

#### 思路  

从暴力解我们已经知道，**真正的难点在于如何决定每两个相邻段之间放哪一根分隔符**。  
仔细观察题目要求：

1. 每段必须恰好包含 **两把座位**（`S`），而植物 `P` 的数量不受限制。  
2. 两段之间 **必须** 放置 **恰好一根** 分隔符；如果不放，就会把两段合并，导致出现不止两把座位的段；如果放了两根，就会产生只含 0 或 1 把座位的段。

于是我们可以把走廊 **先划分成若干“座位对”**，每对由相邻的两把座位组成，之间可能夹着若干植物：

```
S  P P  S   P   S  P S
^------^   ^---^   ^-^
  第1对     第2对   第3对
```

- **第 i 对** 的左端座位是该对的第一个 `S`，右端座位是该对的第二个 `S`。  
- 两个相邻的“座位对”之间的植物数记为 `k`，那么我们 **可以把唯一的分隔符** 放在这 `k+1` 个位置中的任意一个（左边的植物、右边的植物、甚至直接贴在左侧座位右边或右侧座位左边）。  

因此，**所有合法划分方式的总数 = 所有相邻座位对之间 `(k+1)` 的乘积**。

实现步骤：

1. **遍历走廊，记录所有座位 `S` 的下标**。如果座位总数是奇数，则不可能把每段恰好分成两把座位，直接返回 0。  
2. 把座位下标两两配对：`(pos[0], pos[1]), (pos[2], pos[3]), …`。  
3. 对每一对相邻配对之间（即 `pos[2i+1]` 与 `pos[2i+2]`），计算中间的植物数量 `k = pos[2i+2] - pos[2i+1] - 1`。  
4. 累乘 `(k + 1)`，并在每一步对 `10^9+7` 取模，防止整数溢出。  

> **类比**：把座位看成“钥匙”，每两把钥匙必须组成一把锁（一个段）。锁之间的空隙里有若干“螺丝”（植物），我们只能在这些螺丝之间的缝隙里插入唯一的一根“螺丝钉”（分隔符），而螺丝钉可以插在任意一个缝隙里——所以每段之间的选择数就是螺丝数 + 1。

**为什么是最优**  
- 只需一次线性扫描 `O(n)`，不需要枚举任何组合。  
- 只使用常数级额外空间（存放上一次出现的 `S` 位置），符合题目 `n ≤ 10^5` 的限制。

#### 代码（Python）

```python
MOD = 10**9 + 7

def numberOfWays(corridor: str) -> int:
    n = len(corridor)
    seat_pos = []                     # 记录所有座位 'S' 的下标
    for i, ch in enumerate(corridor):
        if ch == 'S':
            seat_pos.append(i)

    # 座位总数必须是偶数，否则无法两两配对
    if len(seat_pos) % 2 == 1:
        return 0

    ans = 1
    # 以配对的方式遍历相邻的两对座位之间的间隙
    # 配对方式： (seat_pos[0], seat_pos[1]), (seat_pos[2], seat_pos[3]), …
    for i in range(1, len(seat_pos) - 1, 2):
        # 当前配对的右座位 seat_pos[i] 与下一配对的左座位 seat_pos[i+1] 之间的植物数
        plants_between = seat_pos[i+1] - seat_pos[i] - 1
        # 分隔符可以放在 plants_between + 1 个位置中的任意一个
        ans = (ans * (plants_between + 1)) % MOD

    return ans
```

> **关键行解释**  
- `seat_pos.append(i)`：把每个座位的“坐标”记下来，类似把书本的章节页码存进字典。  
- `if len(seat_pos) % 2 == 1: return 0`：座位奇数就像手里有奇数根筷子，永远配不成完整的对。  
- `plants_between = seat_pos[i+1] - seat_pos[i] - 1`：两根座位之间的植物数，等于两座位下标之差减去 1（把两座位本身排除）。  
- `ans = (ans * (plants_between + 1)) % MOD`：累计乘积，并随时取模防止溢出。

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次字符串，`n` 最多 `10^5`，完全在限制内。  
- **空间复杂度**：`O(1)`（不计输出），只用了几个整数变量；若把所有 `S` 位置存进列表，则是 `O(m)`，其中 `m` 为座位数，最坏 `O(n)`，仍然线性可接受。

> 与暴力解相比，时间从指数级降到了线性级，速度提升了天壤之别。

---

## 心得

- **核心技巧**：把“每段恰好两把座位”转化为“座位两两配对”，然后统计相邻配对之间的植物数，答案是这些 `(k+1)` 的乘积。  
- **适用题型**：  
  1. **分段计数类**：如 “把数组分成若干段，每段满足某种固定元素个数” （例：`Number of Ways to Split a String`）。  
  2. **间隔乘积类**：如 “统计相邻特殊字符之间的选择数” （例：`Count Ways to Build Good Strings`）。  
  3. **配对+间隔**：如 “将奇数个特定字符配对，求配对间隙的组合数”。  
- **一句话总结**：**先把必须配对的元素两两匹配，再把每对之间的自由插入位置相乘，就是答案。**

---

## 反思

- **第一反应**：看到“每段恰好两把座位”，自然想到**枚举所有分隔符的放置方式**，于是陷入暴力搜索的陷阱。  
- **最容易踩的坑**：  
  - 忘记判断座位总数是否为偶数，直接开始计算会得到错误的非零答案。  
  - 在计算相邻配对之间的间隙时，误把两座位本身算进去，导致 `plants_between` 多算 1。  
  - 忘记对乘积在每一步取模，容易出现 Python 整数溢出（虽然 Python 会自动扩容，但运行速度会大幅下降）。  
- **下次思路**：遇到“每段固定数量的特殊字符”时，**先检查整体可行性（总数是否能被段大小整除）**，再**把字符两两配对**，最后**统计配对之间的自由度**，往往能直接得到 O(n) 的解法。