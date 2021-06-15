# #1366. **按投票排名团队** / Rank Teams by Votes

> 难度：中等 · 标签：Array、Hash Table、String、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/rank-teams-by-votes/)

---

## 题目（英文原版）

**Description**

In a special ranking system, each voter gives a rank from highest to lowest to all teams participating in the competition.
The ordering of teams is decided by who received the most position-one votes. If two or more teams tie in the first position, we consider the second position to resolve the conflict, if they tie again, we continue this process until the ties are resolved. If two or more teams are still tied after considering all positions, we rank them alphabetically based on their team letter.
You are given an array of strings votes which is the votes of all voters in the ranking systems. Sort all teams according to the ranking system described above.
Return a string of all teams sorted by the ranking system.

**Examples**

**Example 1:**

```
Input: votes = ["ABC","ACB","ABC","ACB","ACB"]
Output: "ACB"
Explanation: 
Team A was ranked first place by 5 voters. No other team was voted as first place, so team A is the first team.
Team B was ranked second by 2 voters and ranked third by 3 voters.
Team C was ranked second by 3 voters and ranked third by 2 voters.
As most of the voters ranked C second, team C is the second team, and team B is the third.
```

**Example 2:**

```
Input: votes = ["WXYZ","XYZW"]
Output: "XWYZ"
Explanation:
X is the winner due to the tie-breaking rule. X has the same votes as W for the first position, but X has one vote in the second position, while W does not have any votes in the second position.
```

**Example 3:**

```
Input: votes = ["ZMNAGUEDSJYLBOPHRQICWFXTVK"]
Output: "ZMNAGUEDSJYLBOPHRQICWFXTVK"
Explanation: Only one voter, so their votes are used for the ranking.
```

**Constraints**

- 1 <= votes.length <= 1000
- 1 <= votes[i].length <= 26
- votes[i].length == votes[j].length for 0 <= i, j < votes.length.
- votes[i][j] is an English uppercase letter.
- All characters of votes[i] are unique.
- All the characters that occur in votes[0] also occur in votes[j] where 1 <= j < votes.length.

---

## 题目（中文翻译）

在一种特殊的排名系统中，每位选民会对参赛的所有团队从最高到最低进行排名。  
团队的排序由获得最多第一名投票（position‑one votes）的团队决定。如果有两个或更多团队在第一名位置上票数相同，则比较第二名位置的投票（position‑two votes）来解决冲突；如果仍然相同，则继续比较后续位置的投票，直至冲突解除。如果在所有位置的比较后仍有团队并列，则按团队字母的字典序（alphabetically）进行排名。  

给定一个字符串数组 `votes`，表示所有选民的投票结果。请按照上述排名规则对所有团队进行排序。  
返回一个字符串，包含按排名系统排序后的所有团队。

**示例 1**  
```text
Input: votes = ["ABC","ACB","ABC","ACB","ACB"]
Output: "ACB"
Explanation: 
Team A 被 5 位选民排在第一名。没有其他团队获得第一名票数，所以 A 是第一名。  
Team B 被 2 位选民排在第二名，3 位选民排在第三名。  
Team C 被 3 位选民排在第二名，2 位选民排在第三名。  
由于大多数选民把 C 排在第二名，C 成为第二名，B 则排在第三名。（后文被截断） 
```

**示例 2**  
```text
Input: votes = ["WXYZ","XYZW"]
Output: "XWYZ"
Explanation:
由于平局规则，X 获胜。X 在第一名位置上的票数与 W 相同，但 X 在第二名位置上有一票，而 W 在第二名位置上没有票。
```

**示例 3**  
```text
Input: votes = ["ZMNAGUEDSJYLBOPHRQICWFXTVK"]
Output: "ZMNAGUEDSJYLBOPHRQICWFXTVK"
Explanation:
只有一位选民，因此直接使用该选民的投票顺序作为排名。
```

**约束条件**  

- `1 <= votes.length <= 1000`  
- `1 <= votes[i].length <= 26`  
- 对所有 `0 <= i, j < votes.length`，`votes[i].length == votes[j].length`  
- `votes[i][j]` 为大写英文字母  
- `votes[i]` 中的字符互不相同  
- `votes[0]` 中出现的所有字符也会出现在 `votes[j]`（`1 <= j < votes.length`）中

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

> **把每支队伍的每个名次出现的次数全部统计出来，然后一次一次挑选 “当前排名最好的” 队伍**  

我们把投票看成一个“字典”，键（key）是队伍的字母，值（value）是一个长度为 `m`（每张选票的字符数）的数组，数组第 `j` 位记录这支队伍在第 `j+1` 位（第 1 名、第 2 名 …）出现了多少次。  
> *哈希表就像一本查字典的本子，字母是要查的词，数组是这词对应的解释（这里是每个名次的票数）。*

统计完以后，我们从第 1 位开始比较所有队伍的票数：

1. 先找出 **第一位票数最多** 的队伍集合（可能有多支并列）。  
2. 如果并列的队伍不止一支，就继续比较 **第二位票数**，依此类推。  
3. 当所有位数都比较完仍然并列时，按字母顺序（`A < B < …`）决定最终顺序。

> **为什么正确？**  
> 每一次比较都严格遵循题目描述的“先看第一位，再看第二位 …，最后按字母”。只要我们把每支队伍的每个名次票数都记下来，按这个顺序逐层比较，就一定能得到唯一的排名。

> **复杂度大概是怎样的？**  
> - 统计票数需要遍历所有投票 `O(v * m)`（`v` 为投票人数，`m` 为每张选票的长度）。  
> - 选出排名时，对每支队伍做 `m` 次线性扫描，最坏情况是 `O(k * m)`（`k` 为队伍数，`k ≤ 26`）。  
> 综合下来是 `O(v * m + k * m)`，在最坏情况下约等于 `O(v * m)`。  
> 这里的 `O` 只是一种“数量级”表示，意思是运行时间随 `v` 和 `m` 的乘积线性增长，实际数据量很小（≤ 1000 × 26），运行几毫秒就可以完成。

#### 代码（Python）

```python
from typing import List, Dict

def rankTeams_bruteforce(votes: List[str]) -> str:
    if not votes:
        return ""

    # 1️⃣ 统计每支队伍在每个位次的票数
    # rank_cnt[team][pos] = 该队在第 pos+1 位出现的次数
    rank_cnt: Dict[str, List[int]] = {}
    m = len(votes[0])                     # 每张选票的长度，也是队伍数量
    for vote in votes:
        for pos, team in enumerate(vote):
            if team not in rank_cnt:
                rank_cnt[team] = [0] * m   # 初始化一个长度为 m 的计数数组
            rank_cnt[team][pos] += 1

    # 2️⃣ 依次挑选排名最靠前的队伍
    teams = list(rank_cnt.keys())
    result = []                           # 最终的排名字符串会逐个加入这里

    while teams:
        # 在剩余的队伍中找“当前最好的”队伍
        best = teams[0]
        for cand in teams[1:]:
            # 按位次比较，两支队伍的票数相同时继续看下一位
            for pos in range(m):
                if rank_cnt[cand][pos] > rank_cnt[best][pos]:
                    best = cand          # cand 在第 pos 位更优秀
                    break
                elif rank_cnt[cand][pos] < rank_cnt[best][pos]:
                    break                # best 更优秀，无需继续比较
                # else: 票数相等，继续检查下一位
            else:
                # 所有位次都相等，按照字母顺序决定（字母越小越前）
                if cand < best:
                    best = cand

        result.append(best)               # 把最佳队伍放进答案
        teams.remove(best)                # 从待选列表中剔除

    return "".join(result)
```

#### 复杂度

- **时间复杂度**：`O(v * m + k² * m)`  
  - `v * m` 用于统计所有投票。  
  - `k² * m`（最坏情况下）来源于每轮挑选最佳队伍时，对剩余的 `k` 支队伍进行 `m` 位次的逐层比较，循环 `k` 次。由于 `k ≤ 26`，实际运行仍然很快。  
- **空间复杂度**：`O(k * m)`  
  - 用哈希表存储每支队伍的 `m` 位计数数组。  

---

### 2. 最优解

#### 思路  

暴力解已经算是“够快”的了，因为队伍数上限只有 26。但是我们可以把 **挑选过程改成一次排序**，省去每轮线性扫描的 `k²` 开销，使整体时间降到 `O(v * m + k log k)`，更符合“大数据”思路。

**关键点**：

1. **同样的计数方式**：先遍历所有投票，得到 `rank_cnt[team][pos]`（与暴力解完全相同）。这一步是不可或缺的，因为没有这张“票数表”就无法比较队伍。

2. **自定义排序键**：Python 的 `sorted` 可以接受一个 `key` 函数。我们把每支队伍的计数数组 **倒序**（因为 `sorted` 默认是升序），再把队伍字母本身拼接进去，形成一个可以直接比较的元组。  
   - 例如，对队伍 `A`，计数 `[5, 2, 3]`（第 1 位 5 票，第 2 位 2 票，第 3 位 3 票）会被映射为 `(-5, -2, -3, 'A')`。  
   - 负号把“大票数”变成“小数”，让升序排序自动实现“票数越多越靠前”。  
   - 最后把字母放在最右边，保证所有票数相等时按字母顺序。

3. **一次排序搞定**：把所有队伍放进列表，按上面的键排序，一遍遍历即可得到最终答案。

> **为什么更好？**  
> - 统计票数仍是 `O(v * m)`，这是必须的下界。  
> - 排序只需要 `O(k log k)`（`k ≤ 26`），比暴力解的 `O(k² * m)` 更低。  
> - 代码更简洁，容易避免手写的“挑选最佳”循环中的细节错误。

#### 代码（Python）

```python
from typing import List, Dict

def rankTeams(votes: List[str]) -> str:
    """
    最优实现：一次统计 + 一次排序
    """
    if not votes:
        return ""

    m = len(votes[0])                     # 每支队伍的位次数
    rank_cnt: Dict[str, List[int]] = {}

    # 1️⃣ 统计每支队伍在每个位次的票数（同暴力解）
    for vote in votes:
        for pos, team in enumerate(vote):
            if team not in rank_cnt:
                rank_cnt[team] = [0] * m
            rank_cnt[team][pos] += 1

    # 2️⃣ 把队伍列表按自定义键排序
    # 键的构造：(-cnt[0], -cnt[1], ..., -cnt[m-1], team)
    # 负号让票数多的排在前面，最后的 team 保证字母顺序作为兜底
    def sort_key(team: str):
        # 把每个位置的计数取负，形成 tuple
        return tuple([-c for c in rank_cnt[team]] + [team])

    ordered = sorted(rank_cnt.keys(), key=sort_key)
    return "".join(ordered)
```

#### 复杂度

- **时间复杂度**：`O(v * m + k log k)`  
  - `v * m` 用于统计所有投票（不可避免的下界）。  
  - `k log k` 是一次排序的代价，其中 `k` 为队伍数量（最多 26），所以实际运行几乎是瞬时完成。  
  - 与暴力解相比，省掉了 `k² * m` 那部分额外比较。

- **空间复杂度**：`O(k * m)`  
  - 与暴力解相同，需要保存每支队伍的计数数组。  

---

## 心得

- **核心技巧**：把“多维比较”转化为 **自定义排序键**（tuple），利用语言自带的排序实现多层次的优先级比较。  
- **适用场景**：  
  1. 多维计数排序（比如 LeetCode 1366 `Rank Teams by Votes`、1368 `Minimum Cost to Connect Sticks` 的计数版）。  
  2. “按字典顺序、按出现次数”等多条件排序（如 1636 `Sort Array by Increasing Frequency`）。  
  3. 需要先统计再排序的题目（如 347 `Top K Frequent Elements`）。  
- **一句话总结**：**把所有比较维度打包进一个 tuple，交给排序器一次搞定**。

---

## 反思

- **第一反应**：先把每支队伍在每个名次的票数统计出来，然后想办法比较这些多维数据。  
- **最容易踩的坑**：  
  - 忘记在所有位次相同的情况下再按字母顺序比较，导致输出不符合要求。  
  - 计数数组的长度必须与投票字符串长度一致，否则会出现 `IndexError`。  
  - 当只有一张选票时，直接返回选票本身是最简答案，别忘了处理空列表的边界。  
- **下次类似题的第一步**：**先把“每个元素的所有属性计数/统计”弄好，再思考如何一次性比较这些属性**（通常是自定义排序键或手写比较函数）。