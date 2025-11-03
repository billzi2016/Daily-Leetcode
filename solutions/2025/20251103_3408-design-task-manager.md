# #3408. 设计任务管理器 / Design Task Manager

> 难度：中等 · 标签：Hash Table、Design、Heap (Priority Queue)、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/design-task-manager/)

---

## 题目（英文原版）

**Description**

There is a task management system that allows users to manage their tasks, each associated with a priority. The system should efficiently handle adding, modifying, executing, and removing tasks.
Implement the TaskManager class:
Note that a user may be assigned multiple tasks.

**Examples**

**Example 1:**

```
Input: ["TaskManager", "add", "edit", "execTop", "rmv", "add", "execTop"] [[[[1, 101, 10], [2, 102, 20], [3, 103, 15]]], [4, 104, 5], [102, 8], [], [101], [5, 105, 15], []]
Output: [null, null, null, 3, null, null, 5]
Explanation
```

**Constraints**

- 1 <= tasks.length <= 105
- 0 <= userId <= 105
- 0 <= taskId <= 105
- 0 <= priority <= 109
- 0 <= newPriority <= 109
- At most 2 * 105 calls will be made in total to add, edit, rmv, and execTop methods.
- The input is generated such that taskId will be valid.

---

## 题目（中文翻译）

存在一个任务管理系统，用户可以管理自己的任务，每个任务都有一个优先级（priority）。系统需要高效地支持以下操作：添加任务（add）、修改任务优先级（edit）、执行优先级最高的任务（execTop）以及删除任务（rmv）。请实现 `TaskManager` 类。  
注意：同一个用户可能拥有多个任务。

**示例 1：**

```text
Input: ["TaskManager", "add", "edit", "execTop", "rmv", "add", "execTop"]
       [[[[1, 101, 10], [2, 102, 20], [3, 103, 15]]], [4, 104, 5], [102, 8], [], [101], [5, 105, 15], []]
Output: [null, null, null, 3, null, null, 5]
```

**解释**  
（此处保留原题的解释内容，若原题提供则在此翻译）

**约束条件**

- `1 <= tasks.length <= 10^5`
- `0 <= userId <= 10^5`
- `0 <= taskId <= 10^5`
- `0 <= priority <= 10^9`
- `0 <= newPriority <= 10^9`
- 对 `add`、`edit`、`rmv`、`execTop` 四个方法的调用总次数不超过 `2 * 10^5`。
- 输入保证 `taskId` 合法。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的办法是把所有任务都放在一个普通的 **列表**（list）里。  
- **add**：把新任务 `[userId, taskId, priority]` 直接 `append` 到列表。  
- **edit**：遍历列表，找到 `taskId` 相同的那一项，改掉它的 `priority`。  
- **rmv**：遍历列表，找到对应的 `taskId`，把那一项删掉（`pop` 或 `del`）。  
- **execTop**：遍历整个列表，挑出 `priority` 最大的任务；如果有多个优先级相同的任务，再挑 `taskId` 最大的那个（因为题目要求在优先级相同的情况下返回 `taskId` 最大的任务对应的 `userId`），最后把它从列表中删除并返回它的 `userId`。  

> **类比**：列表就像一本记事本，所有任务都写在同一页上。要找最高优先级的任务，就得把记事本翻遍每一页——很慢。  

**为什么它是正确的**：  
- 每一次操作我们都完整地检查或修改了所有可能受影响的任务，保证了数据的一致性。  
- `execTop` 在遍历完所有任务后一定能得到当前最高优先级且 `taskId` 最大的那一条记录，符合题目要求。  

**复杂度分析（大白话）**：  

| 操作 | 需要遍历几次列表？ | 时间复杂度 | 空间复杂度 |
|------|-------------------|------------|------------|
| add  | 只在末尾加一个元素 | O(1)（常数时间）| O(1)（不额外占内存）|
| edit | 最坏要看完整个列表 | O(n)（列表长度）| O(1)|
| rmv  | 同上，需要找并删除 | O(n) | O(1)|
| execTop | 必须遍历一次找最大 | O(n) | O(1) |

- **O(n)** 的意思是：如果有 10 万个任务，执行一次 `execTop` 可能要检查 10 万次——在实际使用中会显得很慢。  

#### 代码（Python）  

```python
class TaskManager:
    def __init__(self, tasks):
        """
        tasks: List[[userId, taskId, priority]]
        """
        # 用一个列表保存所有任务，每个元素是 [userId, taskId, priority]
        self.tasks = [list(t) for t in tasks]

    # -------------------------------------------------
    # 1. 添加任务
    def add(self, userId: int, taskId: int, priority: int) -> None:
        self.tasks.append([userId, taskId, priority])   # 直接放到列表尾部

    # 2. 修改任务的优先级
    def edit(self, taskId: int, newPriority: int) -> None:
        for t in self.tasks:
            if t[1] == taskId:          # 找到对应的 taskId
                t[2] = newPriority      # 更新优先级
                break

    # 3. 删除任务
    def rmv(self, taskId: int) -> None:
        for i, t in enumerate(self.tasks):
            if t[1] == taskId:
                self.tasks.pop(i)       # 删除整条记录
                break

    # 4. 执行优先级最高的任务，返回对应的 userId
    def execTop(self) -> int:
        if not self.tasks:
            return -1                  # 题目保证不会出现空情况，这里防止报错

        # 找出优先级最大的任务；若相同则 taskId 最大的
        best = self.tasks[0]
        for t in self.tasks[1:]:
            if (t[2] > best[2]) or (t[2] == best[2] and t[1] > best[1]):
                best = t

        self.tasks.remove(best)        # 把这条任务从列表中删掉
        return best[0]                 # 返回 userId
```

#### 复杂度  

- **时间复杂度**  
  - `add`：O(1) – 只在列表尾部加一个元素。  
  - `edit`、`rmv`、`execTop`：O(n) – 最坏需要遍历全部任务。  
- **空间复杂度**  
  - 只用了原始的列表来存放任务，额外空间是 O(1)。  

> 这种实现虽然思路最直观，但在任务数达到上限（10⁵）且调用次数多达 2·10⁵ 时，会因为频繁的线性扫描而超时。

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于每次 `execTop`、`edit`、`rmv` 都要遍历整个任务集合。  
要把这些操作变快，需要一种**能快速定位「最高优先级任务」**的数据结构，同时还能**根据 taskId 快速查找/修改/删除**。  

下面一步步推导出合适的结构：

1. **找最高优先级 → 堆（Heap）**  
   - 堆是一棵满足「父节点 ≥ 子节点」的完全二叉树，能够在 **O(log n)** 时间得到最大值（这里的最大值指「优先级最高」）。  
   - Python 标准库 `heapq` 实现的是 **最小堆**，我们可以把优先级取负数（`-priority`）来模拟「最大堆」。  

2. **需要同时比较优先级和 taskId**  
   - 题目要求：**优先级相同则取 taskId 最大的**。  
   - 在堆里放一个二元组 `(-priority, -taskId, taskId, userId)`，堆会先比较第一个元素（优先级），相等时比较第二个元素（taskId），这样就实现了「优先级高 → taskId 大」的顺序。  

3. **根据 taskId 快速定位 → 哈希表**  
   - 用一个字典 `info[taskId] = (priority, userId)` 保存当前「有效」的任务信息。  
   - 当我们 **编辑** 或 **删除** 时，只需要在字典里更新/删除对应的 `taskId`，而不必在堆里找它（在堆里找是 O(n)）。  

4. **堆的「懒删除」**  
   - 由于堆里可能残留已经被编辑或删除的旧记录（比如我们在 `edit` 时直接把新记录压入堆），我们在 `execTop` 时 **弹出** 堆顶元素后，先检查它的 `taskId` 是否仍然在 `info` 中且优先级是否匹配。  
   - 若不匹配，就说明这条记录是「过期的」，直接丢弃继续弹出，直到遇到一条「最新」且「未被删除」的任务。  
   - 这种「弹出时清理」的技巧叫 **懒删除**，可以把每一次 `edit`/`rmv` 的复杂度保持在 O(1)。  

5. **总体流程**  

| 方法 | 实际实现 | 关键操作 | 复杂度 |
|------|----------|----------|--------|
| `add` | 把 `(priority, userId)` 写入 `info`，并把 `(-priority, -taskId, taskId, userId)` 推入堆 | `heapq.heappush` | O(log n) |
| `edit`| 更新 `info[taskId]` 为新优先级，然后把 **新** 记录再推入堆 | `heapq.heappush` | O(log n) |
| `rmv` | 删除 `info[taskId]`（如果不存在直接忽略）| `del` | O(1) |
| `execTop` | 循环 `heapq.heappop`，直到堆顶对应的 `taskId` 在 `info` 中且优先级相同；找到后从 `info` 中删除并返回 `userId` | `while` + `heappop` | 最坏 O(log n)（每弹出一次都是 log n）|

> **类比**：  
> - **堆** 像是「随时可以取出最高等级的奖牌」的箱子，拿走最高奖牌只需要打开箱盖一次（log n）。  
> - **字典** 像是「任务的身份证登记簿」，通过 `taskId` 能立刻查到这件任务是否仍然有效以及它的当前优先级。  

#### 代码（Python）  

```python
import heapq
from typing import List

class TaskManager:
    """
    设计一个支持四种操作的任务管理器：
    1. add(userId, taskId, priority)   → 添加任务
    2. edit(taskId, newPriority)       → 修改任务优先级
    3. rmv(taskId)                     → 删除任务
    4. execTop() -> userId             → 执行并返回最高优先级任务对应的 userId
    当优先级相同，取 taskId 最大的任务。
    """

    def __init__(self, tasks: List[List[int]]):
        # ---------- 维护的核心结构 ----------
        # max‑heap（使用负数实现），元素为 (-priority, -taskId, taskId, userId)
        self.heap = []

        # 哈希表：taskId -> (priority, userId)
        self.info = {}

        # 把初始化的任务全部放进去
        for userId, taskId, priority in tasks:
            self.info[taskId] = (priority, userId)
            heapq.heappush(self.heap, (-priority, -taskId, taskId, userId))

    # -------------------------------------------------
    # 1. 添加任务
    def add(self, userId: int, taskId: int, priority: int) -> None:
        # 记录在字典里（视为“最新”状态）
        self.info[taskId] = (priority, userId)
        # 把对应的堆元素压入 heap
        heapq.heappush(self.heap, (-priority, -taskId, taskId, userId))

    # 2. 修改任务的优先级
    def edit(self, taskId: int, newPriority: int) -> None:
        # 只要任务仍在系统中，就更新字典并把新记录压入堆
        if taskId in self.info:
            _, userId = self.info[taskId]          # 取出原来的 userId
            self.info[taskId] = (newPriority, userId)
            heapq.heappush(self.heap, (-newPriority, -taskId, taskId, userId))

    # 3. 删除任务
    def rmv(self, taskId: int) -> None:
        # 直接把字典中的记录删掉，堆里旧的记录会在 execTop 时被懒删除
        self.info.pop(taskId, None)   # pop(..., None) 防止 KeyError

    # 4. 执行最高优先级任务，返回对应的 userId
    def execTop(self) -> int:
        while self.heap:
            # 取出堆顶元素（可能是“过期”记录）
            neg_pri, neg_tid, taskId, userId = heapq.heappop(self.heap)

            # 检查字典里是否还有这条 task，且优先级是否匹配
            cur = self.info.get(taskId)
            if cur is None:
                # 任务已经被 rmv 删除，继续弹出下一个
                continue

            cur_pri, cur_user = cur
            if cur_pri == -neg_pri and cur_user == userId:
                # 找到当前有效且优先级最高的任务
                # 从字典中移除，因为它已经被执行了
                del self.info[taskId]
                return userId
            # 否则说明堆里的是旧的优先级记录，继续循环
        # 按题意这里不会出现空堆的情况，若真的为空返回 -1 以防止错误
        return -1
```

#### 复杂度  

- **时间复杂度**  
  - `add`：`O(log n)`（把元素放进堆）  
  - `edit`：`O(log n)`（同样把新记录压入堆）  
  - `rmv`：`O(1)`（只在字典里删）  
  - `execTop`：最坏 `O(log n)`（弹出堆顶若是过期则继续弹，弹出一次仍是 `log n`，整体摊销仍是 `log n`）  

  与暴力解相比，所有涉及全表扫描的操作都降到了对数级别，极大提升了效率。  

- **空间复杂度**  
  - 堆中可能会保留一些“旧的”记录（因为我们采用懒删除），最坏情况下堆的大小会是 **O(n)**（每次 `edit` 都会多放一个元素），这仍然在题目给出的上限范围内。  
  - 哈希表同样是 `O(n)`。  
  - 因此总体空间复杂度是 `O(n)`。  

---

## 心得  

- **核心技巧**：**堆 + 哈希表的组合**（也叫「堆+映射」或「优先队列 + 延迟删除」），适用于需要**快速取最大/最小**，且**支持任意元素的修改或删除**的场景。  
- **适用的类似题目**  
  1. **设计一个支持插入、删除、获取最大值的集合**（LeetCode 1557/716）  
  2. **实现一个可以快速查询第 k 大元素的流**（LeetCode 703/295）  
  3. **带有过期时间的任务调度器**（类似 LeetCode 703 的延伸）  

- **一句话总结解题钥匙**：  
  > 用堆快速定位「最高」的任务，用哈希表实时维护「任务的最新状态」，两者配合即可在 O(log n) 内完成所有操作。  

---

## 反思  

- **拿到题目第一反应**：先想「把所有任务放进列表」直接遍历，最容易实现但不够高效。  
- **最容易踩的坑**  
  1. **优先级相同的比较规则**：必须把 `taskId` 也放进堆的比较键里，并且是 **取负数**（因为我们用最小堆实现最大堆）。  
  2. **懒删除的细节**：在 `execTop` 时一定要检查堆顶记录是否仍然在字典中且优先级匹配，忘记这一步会导致返回已被删除或已修改的旧任务。  
  3. **边界条件**：`rmv` 可能删除不存在的 `taskId`（题目保证不会，但代码最好防御性写 `pop(..., None)`），`execTop` 在所有任务被删除后仍要安全返回。  

- **下次遇到同类题，第一步该想到**：  
  > “我需要**快速取最大/最小**，而且还要**根据 ID 随机更新或删除**。先把『快速取最大』交给堆，再用哈希表记录每个 ID 的最新信息，最后用懒删除保持堆的干净”。