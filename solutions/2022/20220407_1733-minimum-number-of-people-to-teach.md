# #1733. 最少需要教会的人数 / Minimum Number of People to Teach

> 难度：中等 · 标签：Array、Hash Table、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-people-to-teach/)

---

## 题目（英文原版）

**Description**

On a social network consisting of m users and some friendships between users, two users can communicate with each other if they know a common language.
You are given an integer n, an array languages, and an array friendships where:
You can choose one language and teach it to some users so that all friends can communicate with each other. Return the minimum number of users you need to teach.

**Examples**

**Example 1:**

```
Input: n = 2, languages = [[1],[2],[1,2]], friendships = [[1,2],[1,3],[2,3]]
Output: 1
Explanation: You can either teach user 1 the second language or user 2 the first language.
```

**Example 2:**

```
Input: n = 3, languages = [[2],[1,3],[1,2],[3]], friendships = [[1,4],[1,2],[3,4],[2,3]]
Output: 2
Explanation: Teach the third language to users 1 and 3, yielding two users to teach.
```

**Constraints**

- 2 <= n <= 500
- languages.length == m
- 1 <= m <= 500
- 1 <= languages[i].length <= n
- 1 <= languages[i][j] <= n
- 1 <= u​​​​​​i < v​​​​​​i <= languages.length
- 1 <= friendships.length <= 500
- All tuples (u​​​​​i, v​​​​​​i) are unique
- languages[i] contains only unique values

---

## 题目（中文翻译）

在一个由 `m` 名用户以及若干用户之间的友谊（friendships）构成的社交网络（social network）中，如果两个用户至少会一种相同的语言，他们就能够相互沟通（communicate）。  
给定整数 `n` 表示语言的种类数，数组 `languages` 表示每个用户会的语言列表，数组 `friendships` 表示所有的好友关系，其中 `friendships[i] = [ui, vi]` 表示用户 `ui` 与用户 `vi` 是朋友。

你可以选择**一种语言**并将其教授给若干用户，使得所有朋友对之间都能相互沟通。返回需要教授的最少用户数量。

**示例 1**  
输入: `n = 2`, `languages = [[1],[2],[1,2]]`, `friendships = [[1,2],[1,3],[2,3]]`  
输出: `1`  
解释: 你可以把第二种语言教给用户 1，或者把第一种语言教给用户 2，任意一种方式都只需要教授 1 人。

**示例 2**  
输入: `n = 3`, `languages = [[2],[1,3],[1,2],[3]]`, `friendships = [[1,4],[1,2],[3,4],[2,3]]`  
输出: `2`  
解释: 将第三种语言教给用户 1 和用户 3，恰好需要教授 2 个人。

**约束条件**

- `2 <= n <= 500`
- `languages.length == m`
- `1 <= m <= 500`
- `1 <= languages[i].length <= n`
- `1 <= languages[i][j] <= n`
- `1 <= ui < vi <= languages.length`
- `1 <= friendships.length <= 500`
- 所有元组 `(ui, vi)` 均唯一
- `languages[i]` 中的值互不重复

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一种语言都当作候选，分别算算如果把它教给多少人，就能让所有朋友之间都有共同语言**。  
具体步骤：

1. **遍历所有语言**（语言编号从 `1` 到 `n`）。  
2. 对于当前语言 `lang`，检查每一条友情 `u‑v`：  
   - 如果 `u` 和 `v` 已经有共同语言（不管是不是 `lang`），这条友情已经满足，不用管。  
   - 否则，这条友情不满足，需要把 `lang` 教给 `u` 或 `v`（或者两个人都教），只要其中一个人会 `lang`，他们就能交流。  
3. 为了最少教人，**我们只在需要时把 `lang` 教给不懂它的那个人**。于是我们统计所有**不懂 `lang` 的、且出现在“不满足的友情”中的用户**，把他们的数量记下来。  
4. 对所有语言算完后，取最小的那一个，就是答案。

> **类比**：把语言想成“字典”。如果我们决定只在字典里增加一种新词（语言），就要把这本词典发给所有“不认识这词的人”。统计这些人有多少，就是我们需要发多少本词典。

**为什么这个方法一定正确？**  
因为我们把**所有可能的语言**都尝试了一遍，必然会覆盖最优的那种语言。对每种语言我们都求出了**最少需要教的人数**（只教给真正缺这门语言且必须参与交流的用户），于是最小值自然就是全局最优。

#### 代码（Python）

```python
from typing import List, Set
import itertools

def minNumberOfPeopleToTeach_bruteforce(
    n: int, languages: List[List[int]], friendships: List[List[int]]
) -> int:
    # 把每个人会的语言集合化，后面查询更快
    user_lang: List[Set[int]] = [set(langs) for langs in languages]

    # ---------- 1. 找出所有“已经能交流”的友情 ----------
    # 这里不必真的建图，只要知道每条友情是否已经满足即可
    def can_communicate(u: int, v: int) -> bool:
        return len(user_lang[u] & user_lang[v]) > 0   # 交集非空

    # ---------- 2. 暴力枚举每一种语言 ----------
    best = float('inf')          # 记录最小需要教的人数
    for lang in range(1, n + 1):   # 语言编号从 1 到 n
        need_to_teach = set()      # 需要教这门语言的用户集合（去重）

        for u, v in friendships:
            u -= 1      # 转成 0‑based 索引
            v -= 1
            if not can_communicate(u, v):
                # 这条友情目前不满足，需要把 lang 教给 u 或 v
                if lang not in user_lang[u]:
                    need_to_teach.add(u)
                if lang not in user_lang[v]:
                    need_to_teach.add(v)

        best = min(best, len(need_to_teach))

    return best
```

> **关键注释**  
> - `user_lang[u] & user_lang[v]` 用集合交集判断两人是否有共同语言。  
> - `need_to_teach` 用 `set` 去重，因为同一个用户可能出现在多条不满足的友情中，只需要教一次。  

#### 复杂度

- **时间复杂度**：`O(n * (m + f * L))`  
  - `n` 是语言种类数（最多 500），  
  - `m` 是用户数（最多 500），  
  - `f` 是友情条数（最多 500），  
  - `L` 是每个人会的语言数量的上限（最多 `n`）。  
  大白话：我们把每种语言都遍历一遍，在每遍里又要检查所有友情，最坏情况下会有 500 × 500 ≈ 25 万次基本操作，勉强能跑，但不是最优的。

- **空间复杂度**：`O(m + f)`  
  - `user_lang` 存每个人的语言集合，大小和用户数成正比。  
  - 额外的 `need_to_teach` 集合最多也只会装 `m` 个用户。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**对每一种语言都遍历全部友情**。其实我们不需要把每种语言都枚举，而是可以一次遍历找出“**哪些用户必须被教语言**”，再在这些用户中**挑选一种出现次数最多的语言**，把它作为教学目标。原因如下：

1. **只关心不满足的友情**  
   - 如果两个人已经能交流（共享至少一种语言），我们根本不需要对他们做任何事。  
   - 因此先把所有**不满足的友情**挑出来，记为 `bad_edges`。  

2. **涉及的用户集合**  
   - 只要一个用户出现在 `bad_edges` 中，说明他至少有一次“说不通话”。  
   - 为了让所有 `bad_edges` 都满足，**每个出现在 `bad_edges` 里的用户至少要学会一种共同语言**（可以是同一种，也可以是不同的，但我们希望统一成一种，以最少人数）。  

3. **选哪种语言最省人？**  
   - 假设我们决定把语言 `L` 作为统一教学目标。  
   - 那么已经会 `L` 的用户 **不需要再教**，只需要把 `L` 教给 **不懂 `L` 的、且在 `bad_edges` 中出现的用户**。  
   - 因此需要教的人数 = `|S| - cnt(L)`，其中 `S` 是所有出现在 `bad_edges` 中的用户集合，`cnt(L)` 是在 `S` 中已经会 `L` 的人数。  
   - 为了最小化这个值，只要让 `cnt(L)` **最大** 即可。也就是说，**挑选出现次数最多的语言**，教给其余用户。

4. **实现细节**  
   - 第一步：遍历所有友情，找出不满足的（两人语言集合无交集），把涉及的用户加入集合 `bad_users`。  
   - 第二步：统计 `bad_users` 中每种语言出现的频率（使用哈希表 `lang_cnt`）。  
   - 第三步：答案 = `len(bad_users) - max(lang_cnt.values())`（如果 `bad_users` 为空，说明所有朋友已经能交流，答案是 `0`）。

> **类比**：把每个人想成“学生”，语言是“教材”。我们只需要把教材发给**那些不懂任何教材的学生**，而且我们希望挑选一本最受欢迎的教材，这样已经有教材的学生就可以免除再领一本，省下的教材数就是我们要教的学生数。

#### 代码（Python）

```python
from typing import List, Set
from collections import Counter

def minNumberOfPeopleToTeach(n: int, languages: List[List[int]], friendships: List[List[int]]) -> int:
    """
    最优解：只遍历一次友情，统计“必须被教语言”的用户以及这些用户会的语言频次。
    时间 O(m + f * L) ，空间 O(m + n)。
    """
    m = len(languages)                     # 用户数量
    user_lang: List[Set[int]] = [set(l) for l in languages]

    bad_users = set()      # 所有出现在“不满足友情”里的用户（0‑based）
    # 统计每种语言在 bad_users 中出现的次数
    lang_counter = Counter()

    # ---------- 1. 找出所有不满足的友情 ----------
    for u, v in friendships:
        u -= 1   # 转成 0‑based
        v -= 1
        if user_lang[u] & user_lang[v]:   # 交集非空，已经能交流
            continue
        # 这条友情目前不满足，需要处理
        bad_users.add(u)
        bad_users.add(v)

    # 如果所有友情都已经满足，直接返回 0
    if not bad_users:
        return 0

    # ---------- 2. 统计 bad_users 中语言出现频次 ----------
    for user in bad_users:
        for lang in user_lang[user]:
            lang_counter[lang] += 1

    # ---------- 3. 选出现次数最多的语言 ----------
    most_common = max(lang_counter.values())   # 最大出现次数
    # 需要教的人数 = 总的 bad_users 数量 - 已经会最多语言的用户数量
    return len(bad_users) - most_common
```

> **关键注释**  
> - `user_lang[u] & user_lang[v]` 判断两人是否已经能沟通。  
> - `bad_users` 用 `set` 自动去重，确保同一个用户只算一次。  
> - `Counter` 是哈希表的简洁写法，用来统计每种语言在 `bad_users` 中出现的次数。  

#### 复杂度

- **时间复杂度**：`O(m + f * L)`  
  - `m`（≤500）遍历一次把用户语言集合化。  
  - `f`（≤500）遍历所有友情，检查交集（集合操作平均 `O(min(L_u, L_v))`），这里把 `L` 视为每个人语言数的上限。  
  - 再遍历一次 `bad_users`（最多 `m`）统计语言频次。整体远小于暴力解的 `O(n * f * L)`。

- **空间复杂度**：`O(m + n)`  
  - `user_lang` 保存每个人的语言集合。  
  - `bad_users` 最多存 `m` 个用户。  
  - `lang_counter` 最多存 `n` 种语言的计数。  

---

## 心得

- **核心技巧**：先找出“必须处理的用户”，再在这些用户中挑选出现次数最多的语言（贪心 + 哈希计数）。  
- **适用场景**：  
  1. “让所有不相连的节点共享同一属性” 类题，如 **“最少修改使所有相邻节点颜色相同”**。  
  2. “在不满足的关系中选取出现最频繁的元素” 类题，如 **“最少人数改装使所有合作伙伴都有共同爱好”**。  
- **一句话总结**：**把焦点放在必须被教的用户上，选一种最受欢迎的语言，一次遍历即可搞定**。

---

## 反思

- **第一反应**：看到“教语言”就想到枚举每种语言并逐条检查——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忽略已经能交流的友情，导致统计的用户集合过大，答案不对。  
  - 统计语言出现次数时忘记只在 **不满足的用户集合** 中计数，导致误算。  
  - 边界情况：如果所有友情已经满足，`bad_users` 为空，需要直接返回 `0`，否则 `max()` 会抛异常。  
- **下次类似题的第一步**：先 **划分出冲突集合（不满足的关系）**，再在冲突集合中寻找最优的“统一属性”。这样往往能把问题从“遍历所有可能”转化为“一次统计”。