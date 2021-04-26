# #1311. 获取朋友观看的视频 / Get Watched Videos by Your Friends

> 难度：中等 · 标签：Array、Hash Table、Breadth-First Search、Graph、Sorting · [LeetCode 链接](https://leetcode.com/problems/get-watched-videos-by-your-friends/)

---

## 题目（英文原版）

**Description**

There are n people, each person has a unique id between 0 and n-1. Given the arrays watchedVideos and friends, where watchedVideos[i] and friends[i] contain the list of watched videos and the list of friends respectively for the person with id = i.
Level 1 of videos are all watched videos by your friends, level 2 of videos are all watched videos by the friends of your friends and so on. In general, the level k of videos are all watched videos by people with the shortest path exactly equal to k with you. Given your id and the level of videos, return the list of videos ordered by their frequencies (increasing). For videos with the same frequency order them alphabetically from least to greatest.

**Examples**

**Example 1:**

```
Input: watchedVideos = [["A","B"],["C"],["B","C"],["D"]], friends = [[1,2],[0,3],[0,3],[1,2]], id = 0, level = 1
Output: ["B","C"] 
Explanation: 
You have id = 0 (green color in the figure) and your friends are (yellow color in the figure):
Person with id = 1 -> watchedVideos = ["C"] 
Person with id = 2 -> watchedVideos = ["B","C"] 
The frequencies of watchedVideos by your friends are: 
B -> 1 
C -> 2
```

**Example 2:**

```
Input: watchedVideos = [["A","B"],["C"],["B","C"],["D"]], friends = [[1,2],[0,3],[0,3],[1,2]], id = 0, level = 2
Output: ["D"]
Explanation: 
You have id = 0 (green color in the figure) and the only friend of your friends is the person with id = 3 (yellow color in the figure).
```

**Constraints**

- n == watchedVideos.length == friends.length
- 2 <= n <= 100
- 1 <= watchedVideos[i].length <= 100
- 1 <= watchedVideos[i][j].length <= 8
- 0 <= friends[i].length < n
- 0 <= friends[i][j] < n
- 0 <= id < n
- 1 <= level < n
- if friends[i] contains j, then friends[j] contains i

---

## 题目（中文翻译）

**题目描述**  
共有 `n` 个人，每个人的唯一 id 为 `0` 到 `n-1`。给定数组 `watchedVideos` 和 `friends`，其中 `watchedVideos[i]` 与 `friends[i]` 分别表示 id 为 `i` 的人的已观看视频列表和朋友列表。  

第 1 级视频（level 1）指的是所有**直接朋友**（friends）观看过的视频，第 2 级视频（level 2）指的是朋友的朋友观看过的视频，依此类推。一般地，第 `k` 级视频（level k）是指与您之间最短路径恰好为 `k` 的人所观看的所有视频。  

给定你的 `id` 与查询的 `level`，返回这些视频按照**出现频率**（frequency）升序排列的列表。若多个视频出现频率相同，则按字母顺序（alphabetically）从小到大排序。

**示例 1**  

```text
Input: watchedVideos = [["A","B"],["C"],["B","C"],["D"]], 
       friends = [[1,2],[0,3],[0,3],[1,2]], id = 0, level = 1
Output: ["B","C"] 
```
**Explanation:**  
你是 id = 0（图中绿色），你的直接朋友为（图中黄色）：
- id = 1 → `watchedVideos` = ["C"]
- id = 2 → `watchedVideos` = ["B","C"]

统计这些朋友观看视频的频次得到：
- B → 1 次  
- C → 2 次  

按频次升序且频次相同按字母序排列，结果为 `["B","C"]`。

**示例 2**  

```text
Input: watchedVideos = [["A","B"],["C"],["B","C"],["D"]], 
       friends = [[1,2],[0,3],[0,3],[1,2]], id = 0, level = 2
Output: ["D"]
```
**Explanation:**  
你是 id = 0（图中绿色），第 2 级的朋友即是朋友的朋友，唯一的第 2 级朋友是 id = 3（图中黄色），其观看视频为 ["D"]，因此返回 `["D"]`。

**约束条件**  
- `n == watchedVideos.length == friends.length`
- `2 <= n <= 100`
- `1 <= watchedVideos[i].length <= 100`
- `1 <= watchedVideos[i][j].length <= 8`
- `0 <= friends[i].length < n`
- `0 <= friends[i][j] < n`
- `0 <= id < n`
- `1 <= level < n`
- 若 `friends[i]` 包含 `j`，则 `friends[j]` 必定包含 `i`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有人都遍历一遍**，把每个人到自己的最短路径（即“几度关系”）算出来，然后挑出恰好等于 `level` 的那些人，收集他们看过的影片，最后把影片按出现次数从少到多排序（次数相同再按字典序）。

- **数据结构**  
  - `list`（列表）保存每个人的影片列表、朋友列表。  
  - `dict`（字典）像查字典一样，用来统计每部影片出现了多少次：`key` 是影片名字，`value` 是出现次数。  
  - `queue`（队列）可以用 `collections.deque` 实现，模拟“逐层访问朋友”的过程，就像我们在街上找“第 k 级邻居”时，一层一层往外走。

- **为什么正确**  
  1. 用 BFS（广度优先搜索）从自己出发，第一层访问的就是直接朋友，第二层就是朋友的朋友，以此类推。  
  2. 当遍历到第 `level` 层时，所有被访问到的节点（人）恰好与自己相距 `level`，没有更近也没有更远。  
  3. 把这层人的所有影片统计起来，就是题目要求的 “第 k 层观看的影片”。  

- **复杂度**  
  - **时间**：我们会遍历所有节点一次（`O(n)`），并且遍历每个人的朋友列表（总共至多 `O(n^2)`，因为每条边最多被访问两次），再遍历第 `level` 层人的影片（至多 `O(n·m)`，`m` 为每人影片数）。整体是 `O(n + E + V·m)`，在最坏情况下约等于 `O(n²)`（因为 `n ≤ 100`，完全可以接受）。  
  - **空间**：额外使用的空间主要是 `visited` 数组、队列和统计字典，都是 `O(n)` 级别。

#### 代码（Python）

```python
from collections import deque, defaultdict
from typing import List

def watchedVideosByFriends_bruteforce(
    watchedVideos: List[List[str]],
    friends: List[List[int]],
    id: int,
    level: int
) -> List[str]:
    n = len(watchedVideos)                 # 人数
    visited = [False] * n                  # 记录哪些人已经访问过
    q = deque()
    q.append(id)
    visited[id] = True
    cur_level = 0

    # ---------- BFS 找到第 level 层的朋友 ----------
    while q and cur_level < level:
        # 同层节点数决定了本轮循环只遍历当前层
        for _ in range(len(q)):
            cur = q.popleft()
            for nb in friends[cur]:         # nb 为 cur 的每个朋友
                if not visited[nb]:
                    visited[nb] = True
                    q.append(nb)
        cur_level += 1                     # 完成一层，层数+1

    # 此时 q 中的就是所有距离 id 正好为 level 的人
    cnt = defaultdict(int)                # 统计影片出现次数
    while q:
        person = q.popleft()
        for video in watchedVideos[person]:
            cnt[video] += 1                # 计数

    # ---------- 按频率升序、频率相同按字典序 ----------
    # 把字典转成列表再排序，key=lambda x: (cnt[x], x) 表示先按次数，再按名字
    result = sorted(cnt.keys(), key=lambda x: (cnt[x], x))
    return result
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - `n` 是人数，最坏情况下每个人都和每个人是朋友（完整图），遍历所有边需要 `O(n²)`。  
  - 对于本题的约束（`n ≤ 100`），即使是 `O(n²)` 也非常快。

- **空间复杂度**：`O(n)`  
  - 额外的 `visited`、队列和计数字典都和人数线性相关。

---

### 2. 最优解

#### 思路  

暴力解已经是 **最自然的 BFS**，其实已经是最优的时间复杂度 `O(n + E)`（`E` 为朋友关系的条数），因为我们必须至少遍历一次第 `level` 层的所有人，才能知道他们看了哪些影片。  
下面的“最优解”只是在实现细节上进一步**精简代码**，并且**把统计、排序一步完成**，让思路更加清晰。

关键点：

1. **层序遍历（BFS）**：使用队列一次性完成层数计数，层数到达 `level` 时直接停下来，不必继续往外扩。  
2. **一次性统计**：在遍历第 `level` 层时直接把影片计数，而不是先把层的所有人取出来再遍历。  
3. **排序**：Python 的 `sorted` 支持自定义键，只要把 `(出现次数, 影片名)` 作为排序依据，就能一次得到所需顺序。

> **核心算法**：**广度优先搜索（BFS）**。  
> - 把它想象成“在社交网络里，先找你的直接朋友（第 1 层），再找朋友的朋友（第 2 层）”，层层递进，正好对应题目中的 “level”。  
> - BFS 需要 **队列** 来保证“先入先出”，即先访问离你最近的人。

#### 代码（Python）

```python
from collections import deque, Counter
from typing import List

def watchedVideosByFriends(
    watchedVideos: List[List[str]],
    friends: List[List[int]],
    id: int,
    level: int
) -> List[str]:
    n = len(watchedVideos)
    visited = [False] * n
    q = deque([id])
    visited[id] = True
    cur = 0                       # 当前层数

    # ---------- BFS ----------
    while q and cur < level:
        for _ in range(len(q)):   # 只遍历当前层的节点
            person = q.popleft()
            for nb in friends[person]:
                if not visited[nb]:
                    visited[nb] = True
                    q.append(nb)
        cur += 1                  # 完成一层

    # ---------- 统计第 level 层朋友的影片 ----------
    video_counter = Counter()     # Counter 是 dict 的子类，专门用于计数
    while q:                       # q 中全部是第 level 层的朋友
        person = q.popleft()
        video_counter.update(watchedVideos[person])

    # ---------- 排序 ----------
    # 按出现次数升序、次数相同按字母序升序
    return sorted(video_counter.keys(),
                  key=lambda v: (video_counter[v], v))
```

#### 复杂度

- **时间复杂度**：`O(n + E + V·m)`，简化为 `O(n + E)`。  
  - `n`：遍历所有人一次。  
  - `E`：遍历所有朋友关系（每条边最多访问两次）。  
  - `V·m`：第 `level` 层人的影片总数（`V` 为该层人数，`m` 为单人影片数），这一步不可避免。  
  - 与暴力解相比，只是把“先收集再遍历”合并成一次遍历，常数因子更小。

- **空间复杂度**：`O(n)`  
  - `visited`、队列、计数器都和人数线性相关。  

---

## 心得

- **核心技巧**：**广度优先搜索（BFS）层序遍历** + **哈希表计数 + 排序**。  
- **适用的题型**  
  1. “社交网络中第 K 层朋友” 类问题（如 LeetCode 1311. Get Watched Videos by Your Friends）。  
  2. “在图中找到距离起点为 K 的所有节点” 例题（如 1020. Number of Enclaves 的变形）。  
  3. “在树/图中按层统计信息” 题目（如 102. Binary Tree Level Order Traversal）。  
- **一句话总结**：**先用 BFS 把第 k 层的人找出来，再用哈希表统计并排序**，这就是本题的“解题钥匙”。

---

## 反思

- **第一反应**：看到 “第 k 层朋友” 立刻想到 BFS，因为 BFS 本身就是逐层遍历的天然工具。  
- **最容易踩的坑**  
  1. **忘记标记已访问的节点**，导致同一个人被多次加入队列，形成无限循环或重复计数。  
  2. **层数计数错误**：在 BFS 循环里要在遍历完当前层后才 `cur += 1`，否则会把第 0 层（自己）算进第 1 层。  
  3. **统计时忘记去重**：题目要求统计所有出现的次数，不能只保留一次。  
- **下次遇到同类题**：**第一步** 立刻在脑子里画出“层层扩散”的图，确认用 BFS；**第二步** 把第 k 层的节点收集后，再进行后续统计或处理。这样思路会更清晰，也不容易遗漏细节。