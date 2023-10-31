# #2456. 最受欢迎的视频创作者 / Most Popular Video Creator

> 难度：中等 · 标签：Array、Hash Table、String、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/most-popular-video-creator/)

---

## 题目（英文原版）

**Description**

You are given two string arrays creators and ids, and an integer array views, all of length n. The ith video on a platform was created by creators[i], has an id of ids[i], and has views[i] views.
The popularity of a creator is the sum of the number of views on all of the creator's videos. Find the creator with the highest popularity and the id of their most viewed video.
Note: It is possible for different videos to have the same id, meaning that ids do not uniquely identify a video. For example, two videos with the same ID are considered as distinct videos with their own viewcount.
Return a 2D array of strings answer where answer[i] = [creatorsi, idi] means that creatorsi has the highest popularity and idi is the id of their most popular video. The answer can be returned in any order.

**Examples**

**Example 1:**

```
Input: creators = ["alice","bob","alice","chris"], ids = ["one","two","three","four"], views = [5,10,5,4]
Output: [["alice","one"],["bob","two"]]
Explanation:
The popularity of alice is 5 + 5 = 10. The popularity of bob is 10. The popularity of chris is 4. alice and bob are the most popular creators. For bob, the video with the highest view count is "two". For alice, the videos with the highest view count are "one" and "three". Since "one" is lexicographically smaller than "three", it is included in the answer.
```

**Example 2:**

```
Input: creators = ["alice","alice","alice"], ids = ["a","b","c"], views = [1,2,2]
Output: [["alice","b"]]
Explanation:
The videos with id "b" and "c" have the highest view count. Since "b" is lexicographically smaller than "c", it is included in the answer.
```

**Constraints**

- n == creators.length == ids.length == views.length
- 1 <= n <= 105
- 1 <= creators[i].length, ids[i].length <= 5
- creators[i] and ids[i] consist only of lowercase English letters.
- 0 <= views[i] <= 105

---

## 题目（中文翻译）

给定两个字符串数组 `creators` 和 `ids`，以及一个整数数组 `views`，它们的长度均为 `n`。平台上的第 `i` 条视频由 `creators[i]` 创建，视频的 ID 为 `ids[i]`，观看次数为 `views[i]`。  
创作者的受欢迎程度定义为该创作者所有视频观看次数的总和。请找出受欢迎程度最高的创作者，以及其观看次数最多的视频的 ID。  
> 注意：不同的视频可能拥有相同的 ID，即 `ids` 并不唯一标识一条视频。例如，两个拥有相同 ID 的视频被视为不同的视频，各自拥有独立的观看次数。

返回一个二维字符串数组 `answer`，其中 `answer[i] = [creators[i], ids[i]]` 表示 `creators[i]` 是受欢迎程度最高的创作者，`ids[i]` 是其最受欢迎视频的 ID。答案的顺序不限。

**示例 1**  
**输入**: `creators = ["alice","bob","alice","chris"]`, `ids = ["one","two","three","four"]`, `views = [5,10,5,4]`  
**输出**: `[["alice","one"],["bob","two"]]`  
**解释**:  
- `alice` 的受欢迎程度为 `5 + 5 = 10`。  
- `bob` 的受欢迎程度为 `10`。  
- `chris` 的受欢迎程度为 `4`。  
`alice` 和 `bob` 是最受欢迎的创作者。对于 `bob`，观看次数最高的视频是 `"two"`。对于 `alice`，观看次数最高的视频是 `"one"`（与 `"three"` 并列，但 `"one"` 在字典序上更小）。  

**示例 2**  
**输入**: `creators = ["alice","alice","alice"]`, `ids = ["a","b","c"]`, `views = [1,2,2]`  
**输出**: `[["alice","b"]]`  
**解释**:  
观看次数最高的视频的 ID 为 `"b"` 和 `"c"`，两者观看次数相同。由于 `"b"` 在字典序上小于 `"c"`，所以答案中选取 `"b"`。  

**约束条件**  
- `n == creators.length == ids.length == views.length`  
- `1 <= n <= 10^5`  
- `1 <= creators[i].length, ids[i].length <= 5`  
- `creators[i]` 和 `ids[i]` 仅由小写英文字母组成  
- `0 <= views[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **先算每个创作者的总播放量**。  
   对于数组 `creators` 中的每一个创作者 `c`，我们把所有下标 `i`（`creators[i] == c`）对应的 `views[i]` 加起来，得到 `c` 的“人气”。这一步可以把 `c` 看成一本字典，遍历整本书（整个数组）去找所有属于它的词（下标），把对应的数字（播放量）相加。  

2. **找出最高的人气**。  
   把上一步得到的所有人气值挑出最大的那个（可能有多个并列）。  

3. **对每个最高人气的创作者，再找它的“最热视频”**。  
   再次遍历整个数组，挑出属于该创作者的所有视频，记录观看次数最大的那条。如果出现观看次数相同的情况，按照 **字典序**（lexicographically）更小的 `id` 取代。  

为什么这样能得到答案？

- 第一步保证每个创作者的总播放量是准确的，因为我们把它所有视频的观看次数都加进来了。  
- 第二步把最高的人气挑出来，题目要求的就是“人气最高的创作者”。  
- 第三步在这些最高创作者里，再找观看次数最大的那条视频（并且在平局时选字典序最小的），正好满足题目对 “最热视频 id” 的要求。

**时间/空间复杂度（大白话）**  

- 这套思路里我们对 **每一个创作者** 都要 **遍历一次完整的数组**，相当于“把书读了 `m` 次”，其中 `m` 是创作者的种类数，最坏情况下 `m` 可能等于 `n`（每条记录的创作者都不相同）。于是时间复杂度是 **O(n²)**，也就是“如果有 10 000 条记录，最坏会跑 100 000 000 次”。  
- 我们只需要保存几个临时变量（比如当前的最大人气），不需要额外的数组或字典，空间复杂度是 **O(1)**。

#### 代码（Python）

```python
from typing import List

def mostPopularCreators_bruteforce(creators: List[str],
                                   ids: List[str],
                                   views: List[int]) -> List[List[str]]:
    n = len(creators)
    # 1️⃣ 统计每个创作者的总播放量（暴力：每次都遍历全数组）
    total_views = {}
    for c in set(creators):                     # 只遍历出现过的创作者
        total = 0
        for i in range(n):                      # 完整遍历一次数组
            if creators[i] == c:                # 找到属于 c 的视频
                total += views[i]
        total_views[c] = total

    # 2️⃣ 找出最高的人气值
    max_pop = max(total_views.values())

    # 3️⃣ 对所有人气等于 max_pop 的创作者，找他们的最热视频
    answer = []
    for c, pop in total_views.items():
        if pop == max_pop:                       # 只处理最高人气的创作者
            best_view = -1
            best_id = ""                         # 用来记录当前最好的视频 id
            for i in range(n):
                if creators[i] == c:
                    if (views[i] > best_view) or \
                       (views[i] == best_view and ids[i] < best_id):
                        best_view = views[i]
                        best_id = ids[i]
            answer.append([c, best_id])
    return answer
```

> 关键行注释已用中文解释，代码可以直接运行。

#### 复杂度  

- **时间复杂度：O(n²)**  
  “平方”意味着如果记录数翻倍，运行时间大约会增加四倍。这里的瓶颈是对每个创作者都要完整遍历一次数组。  
- **空间复杂度：O(k)**（`k` 为不同创作者的数量）  
  只需要一个字典保存每个创作者的人气，总体占用的额外空间与 `n` 成线性关系，但在最坏情况下 `k ≤ n`，仍然算是 **O(n)**。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复遍历完整数组** 是最耗时的地方。我们可以把所有需要的信息 **一次遍历同步收集**，这样就不必再做第二次、第三次的全遍历。

要一次完成，需要同时维护三件事：

| 需要的信息 | 用什么结构保存 | 解释（类比） |
|------------|----------------|--------------|
| 每个创作者的累计播放量 | `pop_dict[creator]`（哈希表） | 哈希表就像一本“创作者→总播放量”的小字典，key 是创作者名字，value 是累计的观看次数 |
| 每个创作者当前最热视频的观看次数 | `best_view[creator]`（哈希表） | 记录“最高观看次数”，方便以后比较 |
| 每个创作者当前最热视频的 id（在观看次数相同的情况下取字典序最小） | `best_id[creator]`（哈希表） | 记录对应的 video id，若出现平局就比较字符串大小（字典序） |

遍历一次 `creators / ids / views`，对每条记录 `(c, vid, v)`：

1. **累计人气**：`pop_dict[c] += v`。  
2. **更新最热视频**：  
   - 如果 `v` 大于当前记录的 `best_view[c]`，直接把 `best_view[c] = v`，`best_id[c] = vid`。  
   - 如果 `v` 等于 `best_view[c]`，比较 `vid` 与 `best_id[c]` 的字典序，取更小的那个。  

遍历结束后：

- 找出所有创作者中 **最大的人气值** `max_pop = max(pop_dict.values())`。  
- 把所有人气等于 `max_pop` 的创作者以及对应的 `best_id` 组成答案返回。  

整个过程只需要 **一次线性遍历**，所以时间是 **O(n)**，空间是 **O(k)**（存哈希表）。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def mostPopularCreators(creators: List[str],
                       ids: List[str],
                       views: List[int]) -> List[List[str]]:
    # 哈希表：创作者 -> 累计播放量
    pop_dict = defaultdict(int)          # 默认值 0
    # 哈希表：创作者 -> 当前最热视频的观看次数
    best_view = defaultdict(int)         # 默认值 0
    # 哈希表：创作者 -> 当前最热视频的 id（字典序最小）
    best_id = {}

    for c, vid, v in zip(creators, ids, views):
        # 1️⃣ 累计人气
        pop_dict[c] += v

        # 2️⃣ 更新该创作者的最热视频
        if c not in best_id:                     # 第一次出现，直接保存
            best_view[c] = v
            best_id[c] = vid
        else:
            if v > best_view[c]:                 # 更大的观看次数
                best_view[c] = v
                best_id[c] = vid
            elif v == best_view[c] and vid < best_id[c]:
                # 同样的观看次数，取字典序更小的 id
                best_id[c] = vid

    # 3️⃣ 找出最高的人气值
    max_pop = max(pop_dict.values())

    # 4️⃣ 组装答案
    answer = []
    for c, pop in pop_dict.items():
        if pop == max_pop:               # 只保留最高人气的创作者
            answer.append([c, best_id[c]])

    return answer
```

> 关键行均配有中文注释，代码可直接提交通过。

#### 复杂度  

- **时间复杂度：O(n)**  
  只遍历一次 `n` 条记录，时间随记录数线性增长。相较于暴力的 O(n²)，大幅提升（比如 10⁵ 条记录只需要 10⁵ 次操作）。  
- **空间复杂度：O(k)**（`k` 为不同创作者的数量）  
  需要三个哈希表分别存人气、最高观看次数和对应的 id，额外空间与创作者种类数成正比，最坏情况下 `k = n`，仍是 **O(n)**，但已经是不可避免的，因为答案本身就要记住每个创作者的信息。

---  

## 心得  

- **核心技巧**：一次遍历同步维护多个哈希表（累计、最大值、字典序最小值）。  
- **适用的题型**  
  1. “分组求和 + 组内极值” 类问题，如 “统计每个城市的总人口并找人口最多的城市”。  
  2. “同组内多属性比较” 如 “每个用户的最高得分及对应的比赛 ID”。  
  3. “字典序平局处理” 常见于需要在相同数值下返回最小（或最大）字符串的题目。  
- **一句话总结**：**“一次遍历 + 哈希表” 是处理“分组统计 + 组内极值”最安全、最快的钥匙。**

## 反思  

- **第一反应**：把每个创作者的所有视频找出来再分别处理，结果想到要遍历多次。  
- **最容易踩的坑**  
  - 忘记在观看次数相同的情况下比较 `id` 的字典序，会导致答案不符合要求。  
  - `views[i]` 可能为 0，仍需计入累计人气，别把它当成“无效”。  
  - 当所有创作者的总人气相同（如全部 0），仍要返回所有人的最小 `id`。  
- **下次遇到同类题**：第一步先想 “能否在一次遍历里把所有需要的信息都收集完？” 再决定使用哈希表或其他分组结构。