# #2410. 玩家与训练师的最大匹配 / Maximum Matching of Players With Trainers

> 难度：中等 · 标签：Array、Two Pointers、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-matching-of-players-with-trainers/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array players, where players[i] represents the ability of the ith player. You are also given a 0-indexed integer array trainers, where trainers[j] represents the training capacity of the jth trainer.
The ith player can match with the jth trainer if the player's ability is less than or equal to the trainer's training capacity. Additionally, the ith player can be matched with at most one trainer, and the jth trainer can be matched with at most one player.
Return the maximum number of matchings between players and trainers that satisfy these conditions.
Note: This question is the same as  445: Assign Cookies.

**Examples**

**Example 1:**

```
Input: players = [4,7,9], trainers = [8,2,5,8]
Output: 2
Explanation:
One of the ways we can form two matchings is as follows:
- players[0] can be matched with trainers[0] since 4 <= 8.
- players[1] can be matched with trainers[3] since 7 <= 8.
It can be proven that 2 is the maximum number of matchings that can be formed.
```

**Example 2:**

```
Input: players = [1,1,1], trainers = [10]
Output: 1
Explanation:
The trainer can be matched with any of the 3 players.
Each player can only be matched with one trainer, so the maximum answer is 1.
```

**Constraints**

- 1 <= players.length, trainers.length <= 105
- 1 <= players[i], trainers[j] <= 109

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的整数数组 `players`，其中 `players[i]` 表示第 `i` 位玩家的能力值。再给定一个下标从 0 开始的整数数组 `trainers`，其中 `trainers[j]` 表示第 `j` 位训练师的训练容量。  
第 `i` 位玩家可以与第 `j` 位训练师匹配，当且仅当玩家的能力 **小于等于** 训练师的训练容量。除此之外，每位玩家至多只能匹配到一位训练师，每位训练师也至多只能匹配到一位玩家。  

返回满足上述条件的 **最大匹配数**（maximum number of matchings）。

**示例 1**  
**示例 2**  
**约束条件**  
**提示**：本题与 445. Assign Cookies 完全相同。

---

### 示例

#### 示例 1
**输入**: `players = [4,7,9]`, `trainers = [8,2,5,8]`  
**输出**: `2`  
**解释**:  
以下是一种可以形成两组匹配的方式：  
- `players[0]` 可以匹配 `trainers[0]`，因为 `4 <= 8`。  
- `players[1]` 可以匹配 `trainers[3]`，因为 `7 <= 8`。  

可以证明，最多只能形成 `2` 组匹配。

#### 示例 2
**输入**: `players = [1,1,1]`, `trainers = [10]`  
**输出**: `1`  
**解释**:  
这位训练师可以匹配任意一位玩家。由于每位玩家只能匹配到一位训练师，最大匹配数为 `1`。

---

### 约束条件
- `1 <= players.length, trainers.length <= 10^5`
- `1 <= players[i], trainers[j] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是**遍历所有玩家和教练的组合**，看每一对是否满足 `players[i] ≤ trainers[j]`，如果满足且两者都还没有被匹配，就把它们配对。  

- **用到的数据结构**：  
  - 两个数组 `players`、`trainers`（就像两排排好的书）。  
  - 两个布尔数组 `matched_players`、`matched_trainers` 用来记录某个玩家或教练是否已经配对，就像在书的背面贴上“已借出”的标签。  

- **为什么正确**：  
  只要我们把所有可能的配对都检查一遍，且每次配对后把对应的玩家和教练标记为已使用，就不会出现重复配对的情况。最终得到的配对数一定是所有合法配对中的一种（不一定是最多的，但一定合法）。

- **时间/空间复杂度**：  
  - 我们要检查每一个玩家与每一个教练的组合，最坏情况是 `len(players) * len(trainers)` 次。  
  - 如果把 `n = len(players)`，`m = len(trainers)`，时间复杂度就是 **O(n·m)**。  
    - “O(n·m)” 可以理解为“如果玩家有 10 000 人，教练有 10 000 人，就要检查 1 亿 次”。  
  - 需要额外的两个布尔数组保存匹配状态，空间复杂度是 **O(n + m)**，即和输入规模成正比的额外空间。

#### 代码（Python）

```python
def max_match_bruteforce(players, trainers):
    n, m = len(players), len(trainers)
    # 记录每个玩家、教练是否已经匹配
    matched_players = [False] * n
    matched_trainers = [False] * m
    match_cnt = 0

    # 暴力枚举所有可能的 (i, j) 组合
    for i in range(n):
        for j in range(m):
            # 如果玩家 i 能被教练 j 接受，且双方都还没有配对
            if not matched_players[i] and not matched_trainers[j] and players[i] <= trainers[j]:
                matched_players[i] = True   # 标记玩家 i 已配对
                matched_trainers[j] = True  # 标记教练 j 已配对
                match_cnt += 1
                break   # 这个玩家已经配对成功，去检查下一个玩家

    return match_cnt
```

#### 复杂度  

- **时间复杂度**：`O(n·m)` —— 需要遍历玩家 × 教练的所有组合，规模越大，运行时间会指数级增长。  
- **空间复杂度**：`O(n + m)` —— 只用了两个和原数组等长的布尔数组来记录匹配状态。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于大量无意义的比较**。我们其实并不需要把每个玩家和每个教练都尝试配对，只要**把能力弱的玩家先安排给最小能容纳他的教练**，就能最大化配对数量。  

实现思路分三步：

1. **先把两个数组都排个序**（升序）。  
   - 排序后，数组左侧的元素都是“小”——能力弱的玩家或容量小的教练。  
2. **使用双指针**：  
   - `i` 指向玩家数组的当前玩家（从最弱的开始），  
   - `j` 指向教练数组的当前教练（从最弱的开始）。  
3. **贪心匹配**：  
   - 如果 `players[i] ≤ trainers[j]`，说明这个教练能够接收当前玩家，配对成功，两个指针都右移（因为这两个人都已经使用）。  
   - 否则，说明教练的容量太小，根本接不住这个玩家（更弱的玩家更不可能），于是只能把教练指针右移，尝试更大的教练。  

**为什么这样贪心是最优的？**  
- 我们总是让“最弱的玩家”先找“最小能够容纳他的教练”。如果把一个能力稍强的玩家抢走了一个本可以给更弱玩家的教练，后面再找更大的教练给弱玩家时，可能已经没有足够大的教练了，导致配对数下降。  
- 这就是“先把小的配给小的，留大的给大的”原则，保证每一步的选择都不会妨碍后面的更好配对。

#### 代码（Python）

```python
def max_match(players, trainers):
    # 1. 排序：把能力弱的玩家放在前面，容量小的教练放在前面
    players.sort()          # O(n log n)
    trainers.sort()         # O(m log m)

    i = j = 0               # 双指针，分别指向玩家和教练的当前位置
    match_cnt = 0

    # 2. 双指针遍历，直到有一方走完
    while i < len(players) and j < len(trainers):
        if players[i] <= trainers[j]:
            # 当前教练可以接收当前玩家，配对成功
            match_cnt += 1
            i += 1          # 玩家用掉，指向下一个更强的玩家
            j += 1          # 教练用掉，指向下一个更大的教练
        else:
            # 教练太弱，根本接不住这个玩家，换一个更大的教练试试
            j += 1          # 只移动教练指针

    return match_cnt
```

#### 复杂度  

- **时间复杂度**：`O(n log n + m log m)`  
  - 主要花在对两个数组的排序上，排序的时间可以理解为“把一堆乱糟糟的书按照大小排好需要的时间”。遍历的线性部分 `O(n + m)` 相比排序可以忽略不计。  
- **空间复杂度**：`O(1)`（如果使用原地排序）或 `O(n + m)`（如果语言内部实现需要额外的临时数组）。这里我们只用了常数级的额外变量。

---

## 心得  

- **核心技巧**：先排序再使用双指针的贪心匹配。  
- **适用的题型**：  
  1. **Assign Cookies / 分配饼干**（LeetCode 455）——孩子的饥饿度与饼干大小的匹配。  
  2. **Boats to Save People**（LeetCode 881）——把体重小的人先和体重大的尽量配对。  
  3. **Maximum Number of Events That Can Be Attended**（LeetCode 1353）——用排序+贪心决定时间点。  
- **一句话总结解题钥匙**：*“把最弱的需求交给最小能满足它的资源”，用排序把弱-强顺序摆好，用双指针一步步配对。*

---

## 反思  

- **第一反应**：看到“≤”的关系，就想到把两边都排个序，然后逐个比较。  
- **最容易踩的坑**：  
  - 忘记对两个数组都要升序排序，导致指针移动的逻辑相反。  
  - 边界条件：当所有教练都比最弱玩家小，或者玩家比最小教练都大时，循环要能正常结束。  
  - 大数范围（`≤ 10^9`）不会导致溢出，但要注意 Python 的整数是任意精度的，直接比较即可。  
- **下次遇到同类题**：第一步立刻想到“排序 + 双指针（或贪心）”，把问题转化为“在有序序列中寻找匹配”。