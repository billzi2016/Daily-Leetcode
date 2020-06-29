# #911. 在线选举 / Online Election

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Design · [LeetCode 链接](https://leetcode.com/problems/online-election/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays persons and times. In an election, the ith vote was cast for persons[i] at time times[i].
For each query at a time t, find the person that was leading the election at time t. Votes cast at time t will count towards our query. In the case of a tie, the most recent vote (among tied candidates) wins.
Implement the TopVotedCandidate class:

**Examples**

**Example 1:**

```
Input
["TopVotedCandidate", "q", "q", "q", "q", "q", "q"]
[[[0, 1, 1, 0, 0, 1, 0], [0, 5, 10, 15, 20, 25, 30]], [3], [12], [25], [15], [24], [8]]
Output
[null, 0, 1, 1, 0, 0, 1]

Explanation
TopVotedCandidate topVotedCandidate = new TopVotedCandidate([0, 1, 1, 0, 0, 1, 0], [0, 5, 10, 15, 20, 25, 30]);
topVotedCandidate.q(3); // return 0, At time 3, the votes are [0], and 0 is leading.
topVotedCandidate.q(12); // return 1, At time 12, the votes are [0,1,1], and 1 is leading.
topVotedCandidate.q(25); // return 1, At time 25, the votes are [0,1,1,0,0,1], and 1 is leading (as ties go to the most recent vote.)
topVotedCandidate.q(15); // return 0
topVotedCandidate.q(24); // return 0
topVotedCandidate.q(8); // return 1
```

**Constraints**

- 1 <= persons.length <= 5000
- times.length == persons.length
- 0 <= persons[i] < persons.length
- 0 <= times[i] <= 109
- times is sorted in a strictly increasing order.
- times[0] <= t <= 109
- At most 104 calls will be made to q.

---

## 题目（中文翻译）

**描述**  
给定两个整数数组 `persons` 和 `times`。在一次选举中，第 `i` 次投票在时间 `times[i]` 时投给 `persons[i]`。  
对于每个查询时间 `t`，找出在时间 `t` 时领先的候选人（即得票数最多的候选人）。时间 `t` 的投票会计入查询。若出现并列，则在并列候选人中最近一次投票的候选人获胜。

实现 `TopVotedCandidate` 类：

**示例 1**  

```text
Input
["TopVotedCandidate", "q", "q", "q", "q", "q", "q"]
[[[0, 1, 1, 0, 0, 1, 0], [0, 5, 10, 15, 20, 25, 30]], [3], [12], [25], [15], [24], [8]]

Output
[null, 0, 1, 1, 0, 0, 1]
```

**解释**  
```java
TopVotedCandidate topVotedCandidate = new TopVotedCandidate(
    [0, 1, 1, 0, 0, 1, 0],
    [0, 5, 10, 15, 20, 25, 30]);

topVotedCandidate.q(3);   // 返回 0，时间 3 时投票为 [0]，0 为领先者。
topVotedCandidate.q(12);  // 返回 1，时间 12 时投票为 [0,1,1]，1 为领先者。
topVotedCandidate.q(25);  // 返回 1，时间 25 时投票为 [0,1,1,0,0,1]，1 为领先者（并列时取最近一次投票的候选人）。
topVotedCandidate.q(15);  // 返回 0
topVotedCandidate.q(24);  // 返回 0
topVotedCandidate.q(8);   // 返回 1
```

**约束条件**  
- `1 <= persons.length <= 5000`  
- `times.length == persons.length`  
- `0 <= persons[i] < persons.length`  
- `0 <= times[i] <= 10^9`  
- `times` 严格递增（已排序）  
- `times[0] <= t <= 10^9`  
- 对 `q` 的调用最多为 `10^4` 次。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**把每一次查询都重新算一遍**：  

1. 给定查询时间 `t`，从头遍历 `times`，只要 `times[i] ≤ t` 就把第 `i` 次投票计入。  
2. 用一个哈希表（在 Python 里就是 `dict`）记录每个人当前得到的票数。哈希表可以想象成一本“选民册”，  
   - **key** 是候选人的编号，就像字典里的单词。  
   - **value** 是该候选人已经得到的票数，就像单词对应的解释。  
3. 同时维护当前“领先者”。遍历过程中每加一票，就比较这位候选人的票数是否超过了当前领先者，  
   - 如果超过，直接把他设为新的领先者。  
   - 如果相等（出现平局），题目要求**最近一次投票的候选人获胜**，所以只要这次投票恰好是平局的那个人，就直接把他设为领先者（因为我们是按时间顺序遍历的，后出现的自然是“最近的”。）  
4. 遍历完所有 `times ≤ t` 后，返回记录的领先者即可。  

> **为什么正确？**  
> 我们把查询时刻之前的所有投票都完整统计了一遍，统计的规则（超过或平局取最近）和题目要求一模一样，因而返回的就是正确的领先者。  

#### 代码（Python）  

```python
from typing import List

class TopVotedCandidate:
    def __init__(self, persons: List[int], times: List[int]):
        # 这里不做任何预处理，直接保存原始数据
        self.persons = persons
        self.times = times

    def q(self, t: int) -> int:
        """
        暴力查询：遍历所有投票，统计截至时间 t 的领先者
        """
        vote_cnt = {}          # 哈希表：candidate -> votes
        leader = -1            # 当前领先者的编号
        max_votes = 0          # 当前最高票数

        # 按时间顺序遍历，只要投票时间不超过 t 就计入
        for person, time in zip(self.persons, self.times):
            if time > t:       # 已经超过查询时间，直接停止
                break

            # 给该候选人加一票
            vote_cnt[person] = vote_cnt.get(person, 0) + 1

            # 判断是否需要更新领先者
            if vote_cnt[person] > max_votes:
                # 票数严格超过，直接上榜
                max_votes = vote_cnt[person]
                leader = person
            elif vote_cnt[person] == max_votes:
                # 平局，题目要求最近一次投票的候选人获胜
                # 因为我们是顺序遍历的，这里 person 正好是最近投的
                leader = person

        return leader
```

#### 复杂度  

- **时间复杂度**：`O(n)`（其中 `n = len(times)`）  
  对每一次查询，都要从头遍历所有投票，最坏情况下要看完全部 `n` 条记录。  
  用大白话说，就是“如果有 5000 次投票，查询一次可能要检查 5000 次”。  

- **空间复杂度**：`O(k)`（`k` 为候选人数，最多不超过 `n`）  
  只用一个哈希表存每个人的票数，最差情况每个人都投过一次，需要 `n` 个键值对。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次查询都要重新遍历所有投票**。  
如果我们在构造函数里把每个时间点的**领先者**提前算好，查询时只需要在这些时间点里找出**离查询时间最近且不超过它的那个时间点**，对应的领先者就是答案。  

实现思路分两步：

1. **预处理阶段（构造函数）**  
   - 同样遍历 `persons` 与 `times`，实时维护哈希表 `vote_cnt`、当前最高票数 `max_votes` 与当前领先者 `leader`（规则同上）。  
   - 每遍历完一次投票，就把**此时的领先者**记录下来，放进数组 `leaders`。  
   - 同时把对应的时间 `times[i]` 记录在数组 `times`（原样保存即可）。  
   - 结束后，`leaders[i]` 表示**在 `times[i]` 时刻（包括这一次投票）**的领先者。  

2. **查询阶段（`q(t)`）**  
   - 现在我们已经得到一个**单调递增**的时间序列 `times`，以及对应的领先者序列 `leaders`。  
   - 对于任意查询时间 `t`，我们要找的是 **最大的下标 `i` 使得 `times[i] ≤ t`**。这正是二分查找的典型应用。  
   - Python 标准库 `bisect` 提供了 `bisect_right(times, t)`，返回第一个 **大于** `t` 的位置。我们取 `idx-1` 即可得到符合条件的最大下标。  
   - 直接返回 `leaders[idx-1]` 即为答案。  

> **为什么二分查找是对的？**  
> `times` 已经严格递增（题目保证），所以它像一本排好序的电话簿。  
> 二分查找就是把这本电话簿一分为二、再一分为二…，快速定位到我们想要的那一页（时间）。  
> 其时间复杂度是 `O(log n)`，比线性遍历快很多。  

#### 代码（Python）  

```python
from typing import List
import bisect

class TopVotedCandidate:
    def __init__(self, persons: List[int], times: List[int]):
        """
        预处理：遍历一次投票，记录每个时间点的领先者
        """
        self.times = times                # 已经是递增序列，直接保存
        self.leaders = []                 # leaders[i] 表示 times[i] 时的领先者
        vote_cnt = {}                     # 哈希表：candidate -> votes
        leader = -1                       # 当前领先者
        max_votes = 0                     # 当前最高票数

        for person in persons:
            # 给当前投票的候选人加票
            vote_cnt[person] = vote_cnt.get(person, 0) + 1

            # 更新领先者（同暴力解的规则）
            if vote_cnt[person] > max_votes:
                max_votes = vote_cnt[person]
                leader = person
            elif vote_cnt[person] == max_votes:
                # 平局，最近投票的获胜
                leader = person

            # 记录此时的领先者
            self.leaders.append(leader)

    def q(self, t: int) -> int:
        """
        二分查找：找到最近的投票时间不超过 t 的下标，然后返回对应的领先者
        """
        # bisect_right 返回第一个 > t 的位置
        idx = bisect.bisect_right(self.times, t)
        # idx 一定大于 0（因为题目保证 times[0] ≤ t），所以 idx-1 有效
        return self.leaders[idx - 1]
```

#### 复杂度  

- **时间复杂度**  
  - 构造函数：`O(n)`（一次遍历所有投票）  
  - 单次查询 `q(t)`：`O(log n)`（二分查找）  
    与暴力解的 `O(n)` 对比，查询速度提升了 **指数级**，在最多 `10⁴` 次查询的情况下优势非常明显。  

- **空间复杂度**：`O(n)`  
  需要额外存 `leaders`（长度 `n`）和原始的 `times`（长度 `n`），加上哈希表 `vote_cnt`（最多 `n` 条记录），总体是线性空间。  

---  

## 心得  

- **核心技巧**：**预处理 + 二分查找**。先把所有可能的答案（每个时间点的领先者）一次算好，查询时只需要在有序序列里快速定位。  
- **适用的题型**  
  1. “查询历史状态” 类题目，如 LeetCode 1847 *Closest Room*、1852 *Distinct Digits Count*（需要在时间轴上查询）。  
  2. “前缀信息 + 区间查询” 类，如 303 *Range Sum Query - Immutable*（前缀和）或 326 *Power of Three*（前缀幂）。  
- **一句话总结**：**把“慢”搬到“构造阶段”，查询阶段只做二分搜索——先算好答案再快查。**  

---  

## 反思  

- **第一反应**：直接遍历统计每次查询的投票，代码好写但效率低。  
- **最容易踩的坑**  
  - **平局处理**：必须记住“最近一次投票的候选人获胜”，否则会在平局时返回错误的候选人。  
  - **二分边界**：`bisect_right` 返回的是第一个“大于” `t` 的位置，需要 `idx-1` 才是我们要的下标；若直接返回 `idx` 会导致越界或返回错误的结果。  
  - **时间范围**：题目保证 `times[0] ≤ t`，但实际实现时仍要防止 `idx == 0`（如果忘记这点，在自测时可能出现 IndexError）。  
- **下次思路**：看到“多次查询、时间有序”这类描述时，立刻想到 **预处理 + 二分/前缀** 的模式，先判断能否把查询的“慢”转移到构造阶段。