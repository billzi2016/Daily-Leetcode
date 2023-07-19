# #2327. 知晓秘密的人数 / Number of People Aware of a Secret

> 难度：中等 · 标签：Dynamic Programming、Queue、Simulation · [LeetCode 链接](https://leetcode.com/problems/number-of-people-aware-of-a-secret/)

---

## 题目（英文原版）

**Description**

On day 1, one person discovers a secret.
You are given an integer delay, which means that each person will share the secret with a new person every day, starting from delay days after discovering the secret. You are also given an integer forget, which means that each person will forget the secret forget days after discovering it. A person cannot share the secret on the same day they forgot it, or on any day afterwards.
Given an integer n, return the number of people who know the secret at the end of day n. Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 6, delay = 2, forget = 4
Output: 5
Explanation:
Day 1: Suppose the first person is named A. (1 person)
Day 2: A is the only person who knows the secret. (1 person)
Day 3: A shares the secret with a new person, B. (2 people)
Day 4: A shares the secret with a new person, C. (3 people)
Day 5: A forgets the secret, and B shares the secret with a new person, D. (3 people)
Day 6: B shares the secret with E, and C shares the secret with F. (5 people)
```

**Example 2:**

```
Input: n = 4, delay = 1, forget = 3
Output: 6
Explanation:
Day 1: The first person is named A. (1 person)
Day 2: A shares the secret with B. (2 people)
Day 3: A and B share the secret with 2 new people, C and D. (4 people)
Day 4: A forgets the secret. B, C, and D share the secret with 3 new people. (6 people)
```

**Constraints**

- 2 <= n <= 1000
- 1 <= delay < forget <= n

---

## 题目（中文翻译）

描述  
在第 1 天，有一个人发现了一个秘密。  
给定整数 `delay`，表示每个人在发现秘密后 **延迟 `delay` 天**（从第 `delay` 天起）开始，每天向一个新人传播该秘密。  
再给定整数 `forget`，表示每个人在发现秘密后 **`forget` 天** 会忘记该秘密。忘记的那一天以及之后的日子，该人都不能再传播秘密。  
给定整数 `n`，返回第 `n` 天结束时仍然知道该秘密的人数。由于答案可能非常大，请返回 **`mod 10^9 + 7`** 的结果。

示例  

**示例 1**  
```
Input: n = 6, delay = 2, forget = 4
Output: 5
```
**解释**：  
- 第 1 天：假设第一个人叫 A。（1 人）  
- 第 2 天：只有 A 知道秘密。（1 人）  
- 第 3 天：A 将秘密告诉新的人 B。（2 人）  
- 第 4 天：A 将秘密告诉新的人 C。（3 人）  
- 第 5 天：A 忘记了秘密，B 将秘密告诉新的人 D。（3 人）  
- 第 6 天：B 将秘密告诉…

（后续内容已截断）

**示例 2**  
```
Input: n = 4, delay = 1, forget = 3
Output: 6
```
**解释**：  
- 第 1 天：第一个人叫 A。（1 人）  
- 第 2 天：A 将秘密告诉 B。（2 人）  
- 第 3 天：A 和 B 各自将秘密告诉两个人 C、D。（4 人）  
- 第 4 天：A 忘记了秘密，B、C、D 各自将秘密告诉三个人。（6 人）

约束条件  
- `2 <= n <= 1000`  
- `1 <= delay < forget <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们可以把 **每个人** 当成一张小卡片，卡片上记录：

| 发现秘密的第几天 | 可以开始分享的第几天 | 会在第几天忘记 |
|----------------|-------------------|--------------|

- **发现的那天** 就是卡片创建的时间（第 1 天会有一张卡片）。
- **delay 天后**，这张卡片会“解锁”，从那天起它每天都可以把秘密告诉一个全新的人（相当于每天产生一张新卡片）。
- **forget 天后**，这张卡片会“失效”，再也不能分享，也不计入答案。

于是我们可以 **逐天模拟**：

1. 用一个列表 `people` 保存所有仍然有效的卡片（即还没忘记的）。
2. 每天遍历 `people`，判断这张卡片是否已经到了可以分享的阶段，如果可以，就**新增**一张卡片（新认识的人）。
3. 再遍历一次，把已经忘记的卡片剔除。

这就像在玩 **传声筒** 游戏：每个人拿到信息后要等一会儿才开始说话，等太久又会忘记不说了。

> **为什么正确**  
> 我们没有漏掉任何一次分享，也没有提前忘记。因为我们对每个人都严格按照题目给出的 “delay 天后开始分享、forget 天后忘记” 进行状态转移，模拟的过程与题目描述是一致的。

#### 代码（Python）

```python
MOD = 10**9 + 7

def peopleAwareOfSecret_bruteforce(n: int, delay: int, forget: int) -> int:
    # 每个人用 (learn_day, share_start_day, forget_day) 表示
    people = [(1, 1 + delay, 1 + forget)]          # 第一天唯一的 A
    for day in range(2, n + 1):                    # 从第 2 天开始循环
        new_people = []                            # 本天产生的新的人
        # 1️⃣ 让已经可以分享的人每人再产生一个新的人
        for learn, start, forget_day in people:
            if start <= day < forget_day:          # 还能分享的日子
                new_people.append((day, day + delay, day + forget))

        # 2️⃣ 把新的人加入列表
        people.extend(new_people)

        # 3️⃣ 删除已经忘记的人（忘记的那天不算在内）
        people = [p for p in people if p[2] > day]

    # 最后一天仍然在列表里的就是知道秘密的人数
    return len(people) % MOD
```

- `people` 中每个元组的第三个元素是 **忘记的那一天**，因为在 `forget_day` 这天已经不能再算作“知道秘密”。  
- `day < forget_day` 保证了“忘记的当天不算”。  
- 代码里用了列表推导式过滤掉已经忘记的卡片，直观易懂。

#### 复杂度

- **时间复杂度**：`O(n * m)`，其中 `m` 是当天仍然记得秘密的人数。最坏情况下每天的人数会线性增长到 `O(n)`，于是整体是 `O(n²)`。  
  > 用大白话说：如果 `n=1000`，最差情况下要跑大约 1 000 000 次循环，算起来有点慢。

- **空间复杂度**：`O(m)`，最坏情况下需要保存所有还没忘记的人，同样是 `O(n)`。  
  > 就像我们要把所有仍在传声筒里的卡片都放进桌子上，最多会有 `n` 张。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每一天我们都要遍历全部仍然记得的人，这会导致二次遍历。  
实际上，我们只需要关心 **“今天可以分享的人数”**，而不必关心每个人的具体状态。

**关键观察**：

- 第 `i` 天新认识的人只会在 **`i + delay`** 开始分享，**`i + forget`** 时忘记。
- 因此 **今天能够分享的人** = “在 `[i - forget + 1, i - delay]` 这段时间内学会秘密的人数”。  
  （因为他们已经等满 `delay` 天，但还没到 `forget` 天）

于是我们可以用 **动态规划 + 滑动窗口** 来一次算出每一天的 “新认识的人数”。  

设 `new[i]` 为第 `i` 天**新认识**的人的数量（即当天被分享得到的）。  
- 第一天 `new[1] = 1`（题目说第一天只有一个人知道）。
- 对于 `i > 1`，`new[i]` = **可以分享的人数**（即前面 `new` 的某个区间和）  
  `share = sum(new[i - forget + 1] … new[i - delay])`  

我们用一个 **前缀和**（或滑动窗口）来快速得到这个区间和，整个过程只需 `O(n)`。

> **类比**：想象有一条流水线，每天进入的原料会在第 `delay` 天开始加工，`forget` 天后就会被淘汰。我们只需要知道 **当前正处于加工状态的原料总量**，不必记录每件原料的具体位置。

#### 代码（Python）

```python
MOD = 10**9 + 7

def peopleAwareOfSecret(n: int, delay: int, forget: int) -> int:
    # new[i] 表示第 i 天新认识的人数（下标从 1 开始）
    new = [0] * (n + 1)
    new[1] = 1                     # 第一天只有 A
    # prefix[i] = new[1] + ... + new[i]，方便区间求和
    prefix = [0] * (n + 1)
    prefix[1] = 1

    for day in range(2, n + 1):
        # 可以分享的区间是 [day-forget+1, day-delay]
        left = max(1, day - forget + 1)      # 区间左端不能小于 1
        right = day - delay                  # 右端一定 >= left（因为 delay < forget）

        if right >= left:                    # 区间合法才有分享
            # 区间和 = prefix[right] - prefix[left-1]
            share = (prefix[right] - prefix[left - 1]) % MOD
            new[day] = share                 # 当天新产生的认识者
        # 更新前缀和
        prefix[day] = (prefix[day - 1] + new[day]) % MOD

    # 最后一天仍然记得秘密的人 = 所有仍未忘记的 new[i]
    # 这些人位于区间 [n-forget+1, n]（因为 n 之后就不再算）
    start = max(1, n - forget + 1)
    ans = (prefix[n] - prefix[start - 1]) % MOD
    return ans
```

**关键行解释**：

- `left = max(1, day - forget + 1)`：防止下标越界，忘记的最早一天是第 `1` 天。
- `share = (prefix[right] - prefix[left - 1]) % MOD`：利用前缀和一次得到区间和，省去遍历。
- `ans = (prefix[n] - prefix[start - 1]) % MOD`：答案是 **第 `n` 天仍然在记忆窗口里的所有人**。

整个循环只遍历 `n` 次，时间线性。

#### 复杂度

- **时间复杂度**：`O(n)`。我们只进行一次线性遍历，并在每一步用常数时间的前缀和求区间和。  
  > 与暴力的 `O(n²)` 相比，快了大约 `n` 倍（比如 `n=1000` 时只需要千次操作）。

- **空间复杂度**：`O(n)`。需要保存 `new` 与 `prefix` 两个长度为 `n+1` 的数组。  
  > 若进一步优化，只保留滑动窗口的计数，也可以做到 `O(1)`，但 `O(n)` 已经足够轻量。

---

## 心得

- **核心技巧**：**滑动窗口 + 前缀和** 用来统计“在某个时间窗口内仍然活跃的元素”。  
- **适用场景**：  
  1. **固定窗口内求和/计数**（例如 LeetCode 1695. Maximum Erasure Value）。  
  2. **状态随时间衰减** 的 DP（如 2130. Maximum Twin Sum of a Linked List 的时间线思路）。  
  3. **人群传播模型**（如 1976. Number of Ways to Arrive at Destination）。  
- **一句话总结**：把“谁能分享”抽象成“最近 `delay~forget-1` 天加入的人数”，用前缀和一次算清楚。

---

## 反思

- **第一反应**：直接把每个人的状态保存下来，按天模拟。这样思路最直观，但容易忽视规模。
- **最容易踩的坑**  
  - **忘记的边界**：忘记的那一天 **不能** 计入答案，需要使用 `< forget_day` 而不是 `<=`。  
  - **下标越界**：在计算 `left = day - forget + 1` 时可能出现负数，需要 `max(1, …)` 防护。  
  - **取模**：每一步都要 `% MOD`，否则中间值会爆掉（尤其是 `n=1000` 时累计会非常大）。
- **下次思路**：看到 “延迟 start / 失效 end” 这类时间窗口，立刻想到 **窗口滑动** 或 **前缀和**，先写出区间公式，再决定是 O(n) 还是 O(1) 实现。