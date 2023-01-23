# #2102. 顺序序数排名追踪器 / Sequentially Ordinal Rank Tracker

> 难度：困难 · 标签：Design、Heap (Priority Queue)、Data Stream、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/sequentially-ordinal-rank-tracker/)

---

## 题目（英文原版）

**Description**

A scenic location is represented by its name and attractiveness score, where name is a unique string among all locations and score is an integer. Locations can be ranked from the best to the worst. The higher the score, the better the location. If the scores of two locations are equal, then the location with the lexicographically smaller name is better.
You are building a system that tracks the ranking of locations with the system initially starting with no locations. It supports:
Note that the test data are generated so that at any time, the number of queries does not exceed the number of locations added to the system.
Implement the SORTracker class:

**Examples**

**Example 1:**

```
Input
["SORTracker", "add", "add", "get", "add", "get", "add", "get", "add", "get", "add", "get", "get"]
[[], ["bradford", 2], ["branford", 3], [], ["alps", 2], [], ["orland", 2], [], ["orlando", 3], [], ["alpine", 2], [], []]
Output
[null, null, null, "branford", null, "alps", null, "bradford", null, "bradford", null, "bradford", "orland"]

Explanation
SORTracker tracker = new SORTracker(); // Initialize the tracker system.
tracker.add("bradford", 2); // Add location with name="bradford" and score=2 to the system.
tracker.add("branford", 3); // Add location with name="branford" and score=3 to the system.
tracker.get();              // The sorted locations, from best to worst, are: branford, bradford.
                            // Note that branford precedes bradford due to its higher score (3 > 2).
                            // This is the 1st time get() is called, so return the best location: "branford".
tracker.add("alps", 2);     // Add location with name="alps" and score=2 to the system.
tracker.get();              // Sorted locations: branford, alps, bradford.
                            // Note that alps precedes bradford even though they have the same score (2).
                            // This is because "alps" is lexicographically smaller than "bradford".
                            // Return the 2nd best location "alps", as it is the 2nd time get() is called.
tracker.add("orland", 2);   // Add location with name="orland" and score=2 to the system.
tracker.get();              // Sorted locations: branford, alps, bradford, orland.
                            // Return "bradford", as it is the 3rd time get() is called.
tracker.add("orlando", 3);  // Add location with name="orlando" and score=3 to the system.
tracker.get();              // Sorted locations: branford, orlando, alps, bradford, orland.
                            // Return "bradford".
tracker.add("alpine", 2);   // Add location with name="alpine" and score=2 to the system.
tracker.get();              // Sorted locations: branford, orlando, alpine, alps, bradford, orland.
                            // Return "bradford".
tracker.get();              // Sorted locations: branford, orlando, alpine, alps, bradford, orland.
                            // Return "orland".
```

**Constraints**

- name consists of lowercase English letters, and is unique among all locations.
- 1 <= name.length <= 10
- 1 <= score <= 105
- At any time, the number of calls to get does not exceed the number of calls to add.
- At most 4 * 104 calls in total will be made to add and get.

---

## 题目（中文翻译）

一个景点由 **名称**（`name`）和 **吸引力得分**（`score`）表示，其中 `name` 在所有景点中唯一，`score` 为整数。景点可以按照从最好到最差进行排名，排名规则如下：

- `score` 越大，景点越好。
- 若两个景点的 `score` 相同，则名称字典序（lexicographically）更小的景点更好。

你需要构建一个系统来实时追踪景点的排名。系统最初没有任何景点，支持以下两种操作：

- `add(name, score)`：向系统中加入一个新景点。
- `get()`：返回当前第 **k** 好的景点的名称，其中 **k** 等于已经调用 `get` 的次数（第一次调用返回第 1 好，第二次调用返回第 2 好，依此类推）。

> 注意：测试数据保证任意时刻 `get` 的调用次数不超过已加入的景点数。

请实现 `SORTracker` 类，使其能够高效完成上述操作。

## 示例

```text
示例 1:
Input
["SORTracker", "add", "add", "get", "add", "get", "add", "get", "add", "get", "add", "get", "get"]
[[], ["bradford", 2], ["branford", 3], [], ["alps", 2], [], ["orland", 2], [], ["orlando", 3], [], ["alpine", 2], [], []]
Output
[null, null, null, "branford", null, "alps", null, "bradford", null, "bradford", null, "bradford", "orland"]
```

**解释**  
```java
SORTracker tracker = new SORTracker(); // 初始化
tracker.add("bradford", 2);            // 添加景点
tracker.add("branford", 3);            // 添加景点
tracker.get();                         // 第 1 好的景点是 "branford"
tracker.add("alps", 2);                // 添加景点
tracker.get();                         // 第 2 好的景点是 "alps"
tracker.add("orland", 2);              // 添加景点
tracker.get();                         // 第 3 好的景点是 "bradford"
tracker.add("orlando", 3);             // 添加景点
tracker.get();                         // 第 4 好的景点是 "bradford"
tracker.add("alpine", 2);              // 添加景点
tracker.get();                         // 第 5 好的景点是 "bradford"
tracker.get();                         // 第 6 好的景点是 "orland"
```

## 约束条件

- `name` 只包含小写英文字母，且在所有景点中唯一。
- `1 <= name.length <= 10`
- `1 <= score <= 10^5`
- 任意时刻，`get` 的调用次数不超过 `add` 的调用次数。
- `add` 与 `get` 总调用次数不超过 `4 * 10^4`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把所有已经加入的景点 **全部保存到一个列表里**，每次 `get()` 被调用时：

1. 把列表按照「分数高→名字字典序小」的顺序排好序（相当于把所有景点排成排行榜）。
2. 取第 `k+1` 名（`k` 为已经调用过 `get` 的次数），返回它的名字。

> **类比**：把所有景点想成一本未排好序的通讯录，`get` 时我们像是把通讯录全部翻页、重新排好顺序再找第几页的联系人。

这种方法一定能得到正确答案，因为排序后的顺序就是题目要求的排名。

#### 代码（Python）

```python
class SORTracker:
    def __init__(self):
        # 保存所有 (score, name) 的列表，score 越大越好
        self.arr = []          # 暴力存储
        self.get_cnt = 0       # 已经调用 get 的次数

    def add(self, name: str, score: int) -> None:
        # 直接把新景点加进列表
        self.arr.append((score, name))

    def get(self) -> str:
        # 按照「分数高 → 名字字典序小」排序
        # 负号把分数变成降序，名字自然是升序
        self.arr.sort(key=lambda x: (-x[0], x[1]))
        # 第 get_cnt + 1 小的就是答案
        ans = self.arr[self.get_cnt][1]
        self.get_cnt += 1
        return ans
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  每次 `get()` 都要把全部 `n` 条记录重新排序，排序的代价是 `n log n`。  
  大白话：如果有 10,000 条景点，排序大概需要 `10,000 × log₂10,000 ≈ 10,000 × 14 ≈ 140,000` 步操作。

- **空间复杂度**：`O(n)`  
  只用了一个列表保存所有记录，随记录数线性增长。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于每次 `get()` 都要 **整体排序**，这会把已经排好序的前 `k` 名景点重复搬运。  
我们可以把所有景点分成两堆：

| 左堆（`left`） | 右堆（`right`） |
|----------------|----------------|
| 保存 **当前排名前 k+1** 的景点（即最好的 k+1 条） | 保存其余所有景点 |

- **左堆** 用 **最大堆**（`max-heap`），堆顶是这 k+1 条里 **最差** 的那个（即第 k+1 名）。  
- **右堆** 用 **最小堆**（`min-heap`），堆顶是所有其余景点里 **最好的** 那个（即第 k+2 名）。

> **类比**：左堆像是「前排座位」的观众（最好的 k+1 位），右堆是「后排座位」的观众。我们只需要随时知道前排最差的那位是谁（左堆堆顶），以及后排最好的那位是谁（右堆堆顶），就能在 `get` 时直接拿到答案。

关键点：

1. **`add(name, score)`**  
   - 先把新景点放进左堆。  
   - 如果左堆的大小超过 `k+1`（`k` 为已经调用过 `get` 的次数），说明左堆里多出一个「不应该在前排」的景点，弹出堆顶（最差的），放进右堆。  
   - 这样左堆始终保持「当前最佳的 k+1 条」。

2. **`get()`**  
   - 当前堆顶 `left[0]` 正好是第 `k+1` 名（因为左堆里是最好的 k+1 条，堆顶是最差的那一条）。  
   - 返回它的名字后，`k` 增加 1，左堆的容量应当变为 `k+1`（即原来的 `k+2` 条）。如果右堆非空，把右堆堆顶（第 k+2 名）搬进左堆，使左堆再次保持「最佳的 k+1 条」。

**堆的实现细节**  
Python 的 `heapq` 只提供最小堆。  
- 为了得到最大堆，我们把「分数」取负数；同时保持名字的自然升序比较即可。  
- 堆元素用三元组 `(-score, name)`（左堆）和 `(score, name)`（右堆）来实现。

#### 代码（Python）

```python
import heapq

class SORTracker:
    def __init__(self):
        # left 为 max-heap，保存前 k+1 条（用负数实现 max）
        self.left = []          # 每个元素是 (-score, name)
        # right 为 min-heap，保存其余景点
        self.right = []         # 每个元素是 (score, name)
        self.get_cnt = 0        # 已经调用 get 的次数（即 k）

    def add(self, name: str, score: int) -> None:
        # 1. 先放进左堆（max-heap）
        heapq.heappush(self.left, (-score, name))

        # 2. 如果左堆大小超过 k+1，弹出最差的放进右堆
        if len(self.left) > self.get_cnt + 1:
            # 弹出左堆堆顶（-score 最大，即 score 最小的）
            worst = heapq.heappop(self.left)
            # 转成正分数放进右堆
            heapq.heappush(self.right, (-worst[0], worst[1]))

    def get(self) -> str:
        # 左堆堆顶就是第 k+1 名
        top = self.left[0]
        ans = top[1]                     # 名字
        self.get_cnt += 1                # k 加 1

        # 为了让左堆保持 k+1 条（现在应该是 k+2 条），
        # 把右堆最好的（即第 k+2 名）搬进左堆
        if self.right:
            best_right = heapq.heappop(self.right)
            heapq.heappush(self.left, (-best_right[0], best_right[1]))

        return ans
```

#### 复杂度

- **时间复杂度**：`O(log n)`（对每次 `add` 与 `get` 均只做若干次堆的 `push/pop`）  
  - 大白话：即使已有 40,000 条记录，插入或取出只需要大约 `log₂40,000 ≈ 16` 步，比一次完整排序的上千步要快得多。

- **空间复杂度**：`O(n)`  
  - 所有景点都要存下来，只是分散在两个堆里，整体仍是线性空间。

- 与暴力解对比：  
  - 暴力解每次 `get` 都是 `O(n log n)`，最坏会导致 40,000 次 `get` 时总耗时约 `O(n² log n)`。  
  - 最优解把每次操作都压到 `O(log n)`，整体变成 `O(n log n)`，足以通过所有测试。

---

## 心得

- **核心技巧**：**双堆（最大堆 + 最小堆）维护“前 k+1 名”和“其余”两部分**，类似“寻找数据流中第 k 小/大的元素”。  
- **适用题型**  
  1. **数据流中第 K 大/小元素**（LeetCode 703、295）  
  2. **动态中位数**（LeetCode 295）  
  3. **实时排行榜**（如本题、或“前 K 名”查询）  
- **一句话总结**：把“前面最差的”和“后面最好的”分别放在两个堆里，`get` 时直接看左堆堆顶。

---

## 反思

- **第一反应**：把所有景点收集起来，等需要时再整体排序。  
- **最容易踩的坑**  
  1. **堆的比较方式**：分数相同要比较名字的字典序，忘记这一点会导致顺序错误。  
  2. **左堆大小的维护**：左堆应保持 `k+1` 条（而不是固定大小），`k` 随 `get` 调用变化。  
  3. **负数实现最大堆**：直接把 `score` 取负而忘记同步名字的顺序会导致错误。  
- **下次类似题的第一步**：先思考“我要把数据划分成哪几块”，通常是“前面多少名 + 其余”，然后选用 **堆** 或 **有序集合** 来维护这几块的边界。