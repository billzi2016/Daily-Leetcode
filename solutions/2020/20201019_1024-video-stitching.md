# #1024. **视频拼接** / Video Stitching

> 难度：中等 · 标签：Array、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/video-stitching/)

---

## 题目（英文原版）

**Description**

You are given a series of video clips from a sporting event that lasted time seconds. These video clips can be overlapping with each other and have varying lengths.
Each video clip is described by an array clips where clips[i] = [starti, endi] indicates that the ith clip started at starti and ended at endi.
We can cut these clips into segments freely.
Return the minimum number of clips needed so that we can cut the clips into segments that cover the entire sporting event [0, time]. If the task is impossible, return -1.

**Examples**

**Example 1:**

```
Input: clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], time = 10
Output: 3
Explanation: We take the clips [0,2], [8,10], [1,9]; a total of 3 clips.
Then, we can reconstruct the sporting event as follows:
We cut [1,9] into segments [1,2] + [2,8] + [8,9].
Now we have segments [0,2] + [2,8] + [8,10] which cover the sporting event [0, 10].
```

**Example 2:**

```
Input: clips = [[0,1],[1,2]], time = 5
Output: -1
Explanation: We cannot cover [0,5] with only [0,1] and [1,2].
```

**Example 3:**

```
Input: clips = [[0,1],[6,8],[0,2],[5,6],[0,4],[0,3],[6,7],[1,3],[4,7],[1,4],[2,5],[2,6],[3,4],[4,5],[5,7],[6,9]], time = 9
Output: 3
Explanation: We can take clips [0,4], [4,7], and [6,9].
```

**Constraints**

- 1 <= clips.length <= 100
- 0 <= starti <= endi <= 100
- 1 <= time <= 100

---

## 题目（中文翻译）

给定一系列体育赛事的录像剪辑（video clips），该赛事持续 `time` 秒。这些剪辑可能相互重叠，且长度不一。  
每段剪辑用数组 `clips` 表示，其中 `clips[i] = [starti, endi]` 表示第 `i` 段剪辑在 `starti` 时刻开始，`endi` 时刻结束。  

我们可以自由地将剪辑切割成更短的片段（segments）。  
返回能够覆盖完整赛事区间 `[0, time]` 所需的最少剪辑数量。如果无法完成覆盖，返回 `-1`。

**示例 1**  
```text
Input: clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], time = 10
Output: 3
Explanation: 选取剪辑 [0,2]、[8,10]、[1,9]，共 3 段。  
然后将 [1,9] 切分为 [1,2] + [2,8] + [8,9]。  
这样得到的片段 [0,2] + [2,8] + [8,10] 正好覆盖整个赛事区间 [0,10]。
```

**示例 2**  
```text
Input: clips = [[0,1],[1,2]], time = 5
Output: -1
Explanation: 仅靠 [0,1] 和 [1,2] 无法覆盖区间 [0,5]。
```

**示例 3**  
```text
Input: clips = [[0,1],[6,8],[0,2],[5,6],[0,4],[0,3],[6,7],[1,3],[4,7],[1,4],[2,5],[2,6],[3,4],[4,5],[5,7],[6,9]], time = 9
Output: 3
Explanation: 可以选取剪辑 [0,4]、[4,7] 和 [6,9]。
```

**约束条件**

- `1 <= clips.length <= 100`
- `0 <= starti <= endi <= 100`
- `1 <= time <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有剪辑的子集枚举一遍**，看哪几个剪辑能够拼出完整的 `[0, time]` 区间，并在所有可行的子集中挑选剪辑数量最少的那个。

- **数据结构**  
  - `clips` 本身是一个列表，里面的每个元素又是 `[start, end]` 的二元组。  
  - 暴力遍历时我们会使用 **位掩码（bit mask）** 来表示子集：如果第 `i` 位是 `1`，说明我们选了第 `i` 个剪辑；如果是 `0`，说明没选。位掩码就像一本字典的“查词页码”，每一位对应一本字典里的一个词，决定是否要查它。

- **为什么正确**  
  - 枚举子集的过程会遍历 **所有可能的组合**，不管是 1 个剪辑、2 个剪辑，还是全部剪辑。只要有一种组合能够覆盖 `[0, time]`，我们必定会在遍历过程中发现它，并记录下最小的剪辑数。

- **时间/空间复杂度**  
  - `clips` 长度记为 `n`（`1 ≤ n ≤ 100`），子集的数量是 `2^n`，每个子集我们都要检查它能否覆盖整个时间区间，这一步的时间大约是 `O(n)`（遍历子集里选中的剪辑并合并区间）。于是总时间是 **`O(n * 2^n)`**。  
    - 这里的 `O(n * 2^n)` 可以想象成“先把所有可能的钥匙都尝一遍（`2^n` 把），每把钥匙再检查一次能否打开门（`n` 步）”。  
  - 只用了常数级的额外空间（用于保存当前子集的掩码和临时区间），所以 **空间复杂度是 `O(1)`**。

> 对于 `n ≤ 15` 这种规模的题目，暴力解还能跑得动；但本题 `n` 最多 100，`2^100` 完全不可接受，这就是暴力解的瓶颈所在。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def videoStitching_bruteforce(clips: List[List[int]], time: int) -> int:
    n = len(clips)
    # 按子集大小从小到大枚举，找到第一个可行的就是最少剪辑数
    for k in range(1, n + 1):                     # 先尝试 1 剪辑、2 剪辑……逐渐增大
        for idxs in combinations(range(n), k):   # 选出 k 个剪辑的下标组合
            # 合并这些剪辑形成的区间
            intervals = sorted([clips[i] for i in idxs], key=lambda x: x[0])
            cur_end = 0
            ok = True
            for s, e in intervals:
                if s > cur_end:                    # 出现间隙，无法连续覆盖
                    ok = False
                    break
                cur_end = max(cur_end, e)          # 向右扩展覆盖范围
            if ok and cur_end >= time:            # 完全覆盖了 [0, time]
                return k
    return -1                                      # 没有任何子集能覆盖
```

- `combinations` 会生成所有大小为 `k` 的子集，类似“从 100 本书里挑出 k 本来读”。  
- `sorted(..., key=lambda x: x[0])` 把选中的剪辑按起始时间从小到大排好，就像把一本日程表按时间顺序排好，方便检查是否有空档。  

#### 复杂度

- **时间复杂度**：`O(n * 2^n)`  
  - 想象成“先把所有钥匙（`2^n` 把）都尝一遍，每把钥匙要检查 `n` 步”。  
- **空间复杂度**：`O(1)`（不计输入本身）  
  - 只用了几个临时变量，和 `n` 无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“枚举所有子集”**——这一步完全没有利用剪辑之间的区间信息。我们需要找出 **“在已经覆盖的区间上，如何一次性挑选最远能伸展的剪辑”**，这正是**贪心**思想的典型场景。

1. **先把所有剪辑按起点升序排序**  
   - 排序后，遍历时可以保证每次看到的都是 **“起点不小于前面已经处理过的起点”**，类似把一堆书按出版年份排好，这样我们只需要往后看。

2. **维护两个变量**  
   - `curr_end`：当前已经覆盖到的最右边位置（相当于我们已经拼好的影片的结尾）。  
   - `next_end`：在所有起点 ≤ `curr_end` 的剪辑中，能够把覆盖范围向右扩展到的最远位置。  
   - 当遍历到一个剪辑的起点已经超过 `curr_end` 时，说明 **“已经没有办法再用已有的剪辑继续向右”**，这时必须把 **`curr_end` 更新为 `next_end`**，并计数一次使用的剪辑。  

3. **贪心决策**  
   - 在每一步，我们都 **选取能够把右端点拉得最远的剪辑**（`next_end`），因为这样可以**最小化剪辑数量**。  
   - 这一步类似在路上行走：我们站在当前能到达的最远点 `curr_end`，然后往前看所有还能踩到的石头（起点 ≤ `curr_end`），挑选能跳得最远的那块石头（`next_end`），一次跳过去。

4. **结束条件**  
   - 当 `curr_end` 已经 ≥ `time`，说明已经覆盖完整个比赛时间，返回计数。  
   - 如果遍历完所有剪辑后仍然 `curr_end < time`，说明无论怎么选都无法填满空缺，返回 `-1`。

> 这套贪心算法的核心是**“最左端点先来，最右可达点优先”**，它只需要一次线性扫描（排序后）即可得到答案。

#### 代码（Python）

```python
from typing import List

def videoStitching_greedy(clips: List[List[int]], time: int) -> int:
    # 1. 按起点升序排序；如果起点相同，按终点降序排（更长的先出现）
    clips.sort(key=lambda x: (x[0], -x[1]))

    ans = 0          # 已经选了多少段
    curr_end = 0     # 已经覆盖到的位置
    next_end = 0     # 在可达的区间里，能进一步到达的最远位置
    i = 0
    n = len(clips)

    # 只要还没有覆盖到 time，就继续循环
    while curr_end < time:
        # 在所有起点 ≤ curr_end 的剪辑里，找最远的终点
        while i < n and clips[i][0] <= curr_end:
            next_end = max(next_end, clips[i][1])
            i += 1

        # 如果找不到能够继续前进的剪辑，说明覆盖失败
        if next_end == curr_end:
            return -1

        # 选取这一次跳跃（相当于使用了一段剪辑）
        ans += 1
        curr_end = next_end   # 把覆盖范围推进到最远点

    return ans
```

- `clips.sort(key=lambda x: (x[0], -x[1]))` 把剪辑按左端点排好，左端点相同的把右端点大的放前面，防止“短的挡住长的”。  
- `while i < n and clips[i][0] <= curr_end:` 循环遍历所有**还能踩到的石头**（起点不超过当前已覆盖的右端），并更新 `next_end` 为最远可达点。  
- `if next_end == curr_end:` 检查是否出现 **“卡住”** 的情况：没有任何剪辑能把右端点进一步推远，这时直接返回 `-1`。  

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 主要花费在排序上（`n log n`），遍历本身是线性 `O(n)`。  
  - 相比暴力的 `O(n * 2^n)`，这就像“先把所有钥匙按大小排好顺序，只需要顺序尝一次”，极大地降低了工作量。

- **空间复杂度**：`O(1)`（不计输入本身）  
  - 只用了几个整型变量，和 `n` 的大小无关。

---

## 心得

- **核心技巧**：**贪心 + 区间排序**。在覆盖区间类问题中，先把区间按左端点排序，然后每一步都挑选能够把右端点延伸最远的区间，往往能得到最少段数的最优解。  
- **适用的题型**  
  1. **最小区间覆盖**（如本题 `Video Stitching`）  
  2. **跳跃游戏**（LeetCode 45 `Jump Game II`）——同样是“最左可达，右端最远”。  
  3. **加油站环路**（LeetCode 134 `Gas Station`）——在环形路径上寻找能一次到达最远的站点。  
- **一句话总结解题钥匙**：  
  > “在已经能到达的最右位置上，挑选能把右端伸得最远的区间”。  

---

## 反思

- **第一反应**：看到“可以自由裁剪剪辑”，立刻想到**枚举子集**，因为剪辑之间可以随意拆分，似乎没有明显的约束。  
- **最容易踩的坑**  
  - **遗漏起点为 0 的剪辑**：如果没有任何剪辑从 `0` 开始，就根本无法启动覆盖。  
  - **区间之间出现空隙**：在贪心遍历时，如果 `next_end` 没有提升，意味着出现了不可跨越的空白，必须及时返回 `-1`。  
  - **起点相同、终点不同的情况**：若不把较长的剪辑排在前面，可能会在遍历时错误地先选了短的，导致后面 `next_end` 更新不够远。  
- **下次遇到同类题**，第一步应该：  
  > “先把所有区间按左端点排序，然后用贪心的‘最远可达’原则一次遍历”。这样既能快速判断是否可行，又能直接得到最少段数的答案。