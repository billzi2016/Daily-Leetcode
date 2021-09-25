# #1488. 避免城市洪涝 / Avoid Flood in The City

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/avoid-flood-in-the-city/)

---

## 题目（英文原版）

**Description**

Your country has an infinite number of lakes. Initially, all the lakes are empty, but when it rains over the nth lake, the nth lake becomes full of water. If it rains over a lake that is full of water, there will be a flood. Your goal is to avoid floods in any lake.
Given an integer array rains where:
Return an array ans where:
If there are multiple valid answers return any of them. If it is impossible to avoid flood return an empty array.
Notice that if you chose to dry a full lake, it becomes empty, but if you chose to dry an empty lake, nothing changes.

**Examples**

**Example 1:**

```
Input: rains = [1,2,3,4]
Output: [-1,-1,-1,-1]
Explanation: After the first day full lakes are [1]
After the second day full lakes are [1,2]
After the third day full lakes are [1,2,3]
After the fourth day full lakes are [1,2,3,4]
There's no day to dry any lake and there is no flood in any lake.
```

**Example 2:**

```
Input: rains = [1,2,0,0,2,1]
Output: [-1,-1,2,1,-1,-1]
Explanation: After the first day full lakes are [1]
After the second day full lakes are [1,2]
After the third day, we dry lake 2. Full lakes are [1]
After the fourth day, we dry lake 1. There is no full lakes.
After the fifth day, full lakes are [2].
After the sixth day, full lakes are [1,2].
It is easy that this scenario is flood-free. [-1,-1,1,2,-1,-1] is another acceptable scenario.
```

**Example 3:**

```
Input: rains = [1,2,0,1,2]
Output: []
Explanation: After the second day, full lakes are  [1,2]. We have to dry one lake in the third day.
After that, it will rain over lakes [1,2]. It's easy to prove that no matter which lake you choose to dry in the 3rd day, the other one will flood.
```

**Constraints**

- 1 <= rains.length <= 105
- 0 <= rains[i] <= 109

---

## 题目（中文翻译）

你的国家拥有无限数量的湖泊（lake）。最初所有湖泊都是空的（empty），当第 `n` 天的雨水落在第 `n` 个湖泊上时，该湖泊会被填满（full）。如果雨水再次落在已经满的湖泊上，就会发生洪水（flood）。你的目标是避免任何湖泊出现洪水。

给定一个整数数组 `rains`，其中：

- `rains[i] > 0` 表示第 `i` 天雨水落在编号为 `rains[i]` 的湖泊上；
- `rains[i] == 0` 表示第 `i` 天是晴天，你可以选择抽干（dry）**任意** 一个湖泊。

返回一个数组 `ans`，其长度与 `rains` 相同，满足：

- 当 `rains[i] > 0` 时，`ans[i] = -1`（表示当天下雨）；
- 当 `rains[i] == 0` 时，`ans[i]` 为你选择抽干的湖泊编号。如果当天抽干的是空湖泊，湖泊状态保持不变。

如果存在多个满足条件的答案，返回任意一个；如果无法避免洪水，返回空数组 `[]`。

> 注意：抽干已经满的湖泊会使其变为空；抽干空湖泊则不产生任何影响。

### 示例

#### 示例 1
> **输入**：`rains = [1,2,3,4]`  
> **输出**：`[-1,-1,-1,-1]`  
> **解释**：  
> 第一天后，满的湖泊为 `[1]`  
> 第二天后，满的湖泊为 `[1,2]`  
> 第三天后，满的湖泊为 `[1,2,3]`  
> 第四天后，满的湖泊为 `[1,2,3,4]`  
> 没有晴天可以抽干湖泊，且所有湖泊都未出现重复降雨，因而没有洪水。

#### 示例 2
> **输入**：`rains = [1,2,0,0,2,1]`  
> **输出**：`[-1,-1,2,1,-1,-1]`  
> **解释**：  
> 第一天后，满的湖泊为 `[1]`  
> 第二天后，满的湖泊为 `[1,2]`  
> 第三天（晴天），抽干湖泊 `2`，满的湖泊变为 `[1]`  
> 第四天（晴天），抽干湖泊 `1`，此时没有满的湖泊。  
> 第五天后，满的湖泊为 `[2]`  
> 第六天后，满的湖泊为 `[1,2]`  
> 该安排下所有降雨均未导致洪水，满足要求。

#### 示例 3
> **输入**：`rains = [1,2,0,1,2]`  
> **输出**：`[]`  
> **解释**：  
> 第二天后，满的湖泊为 `[1,2]`。第三天是晴天，必须抽干其中一个湖泊。  
> 无论在第三天抽干 `1` 还是 `2`，第四天和第五天的降雨都会导致另一座湖泊再次被雨水填满，从而产生洪水。  
> 因此不存在避免洪水的方案，返回空数组。

### 约束条件
- `1 <= rains.length <= 10^5`
- `0 <= rains[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们先把题目想象成 **“下雨天把湖泊装满，晴天可以把任意一个已经装满的湖泊倒掉”**。  
最直接的想法是：  

1. 从左到右依次模拟每一天的天气。  
2. 遇到下雨（`rains[i] > 0`）时，检查这座湖泊是否已经是“满的”。  
   - 如果已经满了，就说明这一天一定会发生洪水。  
   - 为了避免洪水，我们只能在 **之前的某个晴天**（数组中为 `0` 的位置）把这座湖倒掉。于是我们把之前的晴天逐个往前找，看看能否把这座湖倒掉。  
3. 遇到晴天（`rains[i] == 0`）时，随便挑一座已经满的湖倒掉（或者不倒），把答案记为对应的湖号。  

> **类比**：  
> - “满的湖泊” 就像字典里已经有键 `key=湖号` 的条目。  
> - “倒掉湖泊” 就是把这个键从字典里删掉。  
> - “找之前的晴天” 就是在线性数组里往前搜索，类似在纸上顺着时间轴往左找。

这个办法一定能得到正确答案（如果答案存在的话），因为我们每次都在真正导致洪水的那一天**立刻**去找最近的可用晴天去倒掉湖泊。唯一的缺点是：**找前一个晴天的过程是线性搜索**，最坏情况下会遍历整条数组，导致时间复杂度很高。

#### 代码（Python）

```python
def avoidFlood(rains):
    n = len(rains)
    ans = [-1] * n                 # 初始化答案，全填 -1（雨天默认 -1）
    full = set()                   # 用集合记录哪些湖已经满了
    dry_days = []                  # 记录所有晴天的下标（用于后面搜索）

    for i, lake in enumerate(rains):
        if lake == 0:              # 晴天，先把下标记下来，等以后需要时再决定倒哪座湖
            dry_days.append(i)
            ans[i] = 1             # 暂时随便写 1，后面会改成真正倒的湖号
        else:                      # 下雨
            if lake in full:       # 这座湖已经满，必须找之前的晴天倒掉它
                # 线性向前找最近的可用晴天
                found = False
                for d in dry_days:
                    if d > i:      # 晴天必须在当前这天之前，若已经超过则不可能
                        break
                    # 这里我们把最早的晴天都尝试用来倒这座湖
                    if ans[d] == 1:   # 该晴天还没有被使用（仍是默认值 1）
                        ans[d] = lake  # 在这一天倒掉当前湖
                        dry_days.remove(d)   # 这天已经被占用
                        found = True
                        break
                if not found:        # 没有可用的晴天，无法避免洪水
                    return []
                # 这天雨后，湖重新变为“满”
                full.remove(lake)   # 先把旧的满状态去掉
                full.add(lake)      # 再加回来，保持集合不变，只是为了逻辑完整
            else:
                full.add(lake)      # 第一次下雨，直接把湖标记为满
            ans[i] = -1             # 雨天的答案固定为 -1
    return ans
```

> 代码中的关键行已经用中文注释解释。  
> 这里的 `dry_days.remove(d)` 其实是 **O(n)** 的操作，整体最坏时间是 **O(n²)**。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 在最坏情况下，每一次遇到重复雨（需要倒湖）都要遍历一次所有已经记录的晴天。  
  - 用大白话说，就是“如果有 10,000 天，最慢要比较 10,000 × 10,000 次”。  

- **空间复杂度**：`O(n)`  
  - 需要额外的集合 `full`、列表 `dry_days`、答案数组 `ans`，它们的大小都和输入长度成正比。  

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于 **“每次都线性搜索之前的晴天”**。  
如果我们能够 **快速定位** “最近的、且未被使用的晴天”，就可以把每一次的搜索时间降到 `log n`，整体就变成 `n log n`。

下面一步步推导出优化思路：

1. **记录每座湖上一次下雨的时间**  
   用一个哈希表 `last_rain[lake] = day`，相当于“字典”。  
   当再次下雨到同一座湖时，我们就知道 **必须在 `last_rain[lake]` 与当前天之间找到一个晴天来倒它**。

2. **维护一个有序的“可用晴天集合”**  
   - 每当遍历到 `rains[i] == 0`（晴天）时，把这一天的下标 `i` 加入集合。  
   - 需要能够 **快速找出集合中大于某个给定值的最小元素**（即“第一个在 `last_rain[lake]` 之后的晴天”）。  
   - 在 Python 中可以用 **有序列表 + bisect**，或更直接的 **最小堆 + 懒删**。这里用 **最小堆**（`heapq`）实现，思路如下：

     *把所有晴天的下标都压进堆*。  
     当我们需要找“> prev_day”的晴天时：

     - 不断弹出堆顶（最小的下标），只要它 **≤ prev_day**，说明这天太早，根本不能用于倒这座湖，直接丢掉。  
     - 第一个弹出的 **> prev_day** 的下标，就是我们可以用来倒湖的最早晴天。  

   这一步的时间是 `O(log n)`（堆的弹出/压入），而不是线性搜索。

3. **贪心决定倒哪座湖**  
   - 当遇到重复雨（同一座湖再次下雨）时，**只能**在最近的可用晴天倒它，否则必然洪水。  
   - 因此把 **“尽可能早地把必须倒的湖倒掉”** 作为贪心策略。  

4. **填答案**  
   - 雨天的答案固定为 `-1`。  
   - 当我们用某个晴天 `dry_day` 去倒湖 `lake` 时，把 `ans[dry_day] = lake`。  
   - 其余没有被使用的晴天随意填 `1`（只要不是 `-1` 即可），因为它们不影响结果。

> **类比**：  
> - “堆”像是 **一堆排好序的待办事项**，最紧急（最早）的在最上面。  
> - “弹出太早的晴天”相当于把已经过期、再也用不上的任务丢掉。  

整个过程只遍历一次数组，每一次的操作都是 `log n`，因此时间复杂度是 `O(n log n)`。

#### 代码（Python）

```python
import heapq
from typing import List

def avoidFlood(rains: List[int]) -> List[int]:
    n = len(rains)
    ans = [-1] * n                     # 雨天默认 -1，晴天稍后填
    last_rain = {}                     # 记录每座湖最近一次下雨的下标
    dry_heap = []                      # 最小堆，存放所有未使用的晴天下标

    for i, lake in enumerate(rains):
        if lake == 0:                  # ---- 晴天 ----
            heapq.heappush(dry_heap, i)   # 把这天加入可用晴天集合
            ans[i] = 1                 # 暂时随便填 1，后面若被选中会改成真实湖号
        else:                          # ---- 雨天 ----
            if lake in last_rain:      # 这座湖之前已经满了，需要找晴天倒掉
                prev = last_rain[lake] # 上一次下雨的那天
                # 从堆里挑出第一个 > prev 的晴天
                while dry_heap and dry_heap[0] <= prev:
                    heapq.heappop(dry_heap)   # 这天太早，直接丢掉
                if not dry_heap:       # 没有可用的晴天，无法避免洪水
                    return []
                dry_day = heapq.heappop(dry_heap)   # 选中的晴天下标
                ans[dry_day] = lake     # 在这天倒掉当前湖
            # 更新最近一次下雨的时间
            last_rain[lake] = i
            ans[i] = -1                # 雨天的答案固定为 -1
    return ans
```

> 关键行的中文注释已经写在代码里。  
> `heapq.heappop` 与 `heapq.heappush` 的时间都是 `O(log n)`，所以整体是 `n log n`。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 每天只做一次 `push`（晴天）或一次 `pop`（找晴天），堆操作是对数级的。  
  - 用大白话说，就是“如果有 100,000 天，最多只需要大约 17 次比较一次（因为 2^17 ≈ 130,000）”。  

- **空间复杂度**：`O(n)`  
  - 需要存 `last_rain`（最多出现的湖数），堆里最多也会装 `n` 个晴天下标，答案数组 `ans` 长度为 `n`。  

---

## 心得  

- **核心技巧**：**贪心 + 有序数据结构（最小堆）**。  
- **适用的题型**  
  1. “需要在两次关键事件之间安排一次可选操作”——例如 **“预约会议室”**、**“给定区间的最小点覆盖”**。  
  2. “把未来的冲突提前解决”——如 **“最小化平台数量”**、**“在时间轴上消除重复任务”**。  
- **一句话总结**：**把每一次“必须倒的湖”尽可能早地安排到最近的未使用晴天，使用堆快速找出这一天。**  

---

## 反思  

- **第一反应**：看到“下雨会把湖装满，晴天可以倒水”，本能想到“记录每座湖的状态”，然后在冲突时回头找最近的晴天。  
- **最容易踩的坑**  
  1. **忘记更新 `last_rain`**：如果不把最新的雨天写进去，后面的判断会误以为湖仍是上一次的状态。  
  2. **晴天被重复使用**：必须确保每个晴天只被分配一次，否则会产生不合法的答案。  
  3. **边界条件**：全是雨天或全是晴天、雨天出现 0（表示晴天）时的处理都要仔细。  
- **下次类似题的第一步**：**把“必须在两次事件之间完成的操作”抽象为“在有序集合中寻找第一个满足条件的元素”，并决定使用哪种有序结构（堆、TreeSet、二分查找）来实现。**