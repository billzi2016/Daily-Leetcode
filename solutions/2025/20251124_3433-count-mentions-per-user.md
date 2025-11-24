# #3433. 统计每位用户的提及次数 / Count Mentions Per User

> 难度：中等 · 标签：Array、Math、Sorting、Simulation · [LeetCode 链接](https://leetcode.com/problems/count-mentions-per-user/)

---

## 题目（英文原版）

**Description**

You are given an integer numberOfUsers representing the total number of users and an array events of size n x 3.
Each events[i] can be either of the following two types:
Return an array mentions where mentions[i] represents the number of mentions the user with id i has across all MESSAGE events.
All users are initially online, and if a user goes offline or comes back online, their status change is processed before handling any message event that occurs at the same timestamp.
Note that a user can be mentioned multiple times in a single message event, and each mention should be counted separately.

**Examples**

**Example 1:**

```
Input: numberOfUsers = 2, events = [["MESSAGE","10","id1 id0"],["OFFLINE","11","0"],["MESSAGE","71","HERE"]]
Output: [2,2]
Explanation:
Initially, all users are online.
At timestamp 10, id1 and id0 are mentioned. mentions = [1,1]
At timestamp 11, id0 goes offline.
At timestamp 71, id0 comes back online and "HERE" is mentioned. mentions = [2,2]
```

**Example 2:**

```
Input: numberOfUsers = 2, events = [["MESSAGE","10","id1 id0"],["OFFLINE","11","0"],["MESSAGE","12","ALL"]]
Output: [2,2]
Explanation:
Initially, all users are online.
At timestamp 10, id1 and id0 are mentioned. mentions = [1,1]
At timestamp 11, id0 goes offline.
At timestamp 12, "ALL" is mentioned. This includes offline users, so both id0 and id1 are mentioned. mentions = [2,2]
```

**Example 3:**

```
Input: numberOfUsers = 2, events = [["OFFLINE","10","0"],["MESSAGE","12","HERE"]]
Output: [0,1]
Explanation:
Initially, all users are online.
At timestamp 10, id0 goes offline.
At timestamp 12, "HERE" is mentioned. Because id0 is still offline, they will not be mentioned. mentions = [0,1]
```

**Constraints**

- 1 <= numberOfUsers <= 100
- 1 <= events.length <= 100
- events[i].length == 3
- events[i][0] will be one of MESSAGE or OFFLINE.
- 1 <= int(events[i][1]) <= 105
- The number of id<number> mentions in any "MESSAGE" event is between 1 and 100.
- 0 <= <number> <= numberOfUsers - 1
- It is guaranteed that the user id referenced in the OFFLINE event is online at the time the event occurs.

---

## 题目（中文翻译）

**描述**  
给定一个整数 `numberOfUsers` 表示用户总数，以及一个大小为 `n × 3` 的数组 `events`。  
`events[i]` 可以是以下两种类型之一：

- `["MESSAGE", timestamp, content]`：表示在时间戳 `timestamp` 发生的一条消息事件（MESSAGE 事件），`content` 中可能包含若干用户的提及（`id<number>`），以及特殊关键字 `"ALL"` 或其他普通文本。  
- `["OFFLINE", timestamp, userId]`：表示用户 `userId` 在时间戳 `timestamp` 下线。

返回一个数组 `mentions`，其中 `mentions[i]` 表示用户编号为 `i` 在所有 **MESSAGE 事件** 中被提及的总次数。  
所有用户初始均为在线状态；如果用户下线或重新上线，其状态变更会在同一时间戳的任何消息事件之前处理。  
需要注意的是，同一条消息中同一用户可以被多次提及，每一次都要单独计数。

**示例**  

示例 1：  
```
Input: numberOfUsers = 2, events = [["MESSAGE","10","id1 id0"],["OFFLINE","11","0"],["MESSAGE","71","HERE"]]
Output: [2,2]
Explanation:
Initially, all users are online.
At timestamp 10, id1 and id0 are mentioned. mentions = [1,1]
At timestamp 11, id0 goes offline.
At timestamp 71, id0 comes back online and "HERE" is mentioned. mentions = [2,2]
```

示例 2：  
```
Input: numberOfUsers = 2, events = [["MESSAGE","10","id1 id0"],["OFFLINE","11","0"],["MESSAGE","12","ALL"]]
Output: [2,2]
Explanation:
Initially, all users are online.
At timestamp 10, id1 and id0 are mentioned. mentions = [1,1]
At timestamp 11, id0 goes offline.
At timestamp 12, "ALL" is mentioned. This includes offline users, so both id0 and id1 are mentioned. mentions = [2,2]
```

示例 3：  
```
Input: numberOfUsers = 2, events = [["OFFLINE","10","0"],["MESSAGE","12","HERE"]]
Output: [0,1]
Explanation:
Initially, all users are online.
At timestamp 10, id0 goes offline.
At timestamp 12, "HERE" is mentioned. Because id0 is still offline, they will not be mentioned. mentions = [0,1]
```

**约束条件**  

- `1 <= numberOfUsers <= 100`  
- `1 <= events.length <= 100`  
- `events[i].length == 3`  
- `events[i][0]` 只会是 `"MESSAGE"` 或 `"OFFLINE"`  
- `1 <= int(events[i][1]) <= 10^5`（时间戳范围）  
- 任意 `"MESSAGE"` 事件中出现的 `id<number>` 提及数量在 `[1, 100]` 之间  
- `0 <= <number> <= numberOfUsers - 1`（用户编号合法）  
- 保证在 `OFFLINE` 事件触发时，被下线的用户当前是在线状态。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

1. **把事件按时间戳排好顺序**  
   - 时间戳就像排队买票的号码，先来的先处理。我们把 `events` 按第二个元素（时间戳）从小到大排序，保证“先来先服务”。  

2. **维护两套用户集合**  
   - `online`：当前在线的用户 ID。  
   - `offline`：当前离线的用户 ID。  
   - 集合（`set`）在 Python 中相当于“查字典”。键就是用户 ID，找、加、删的时间都是 **O(1)**，非常快。  

3. **逐条处理事件**  
   - **OFFLINE**：把对应的用户从 `online` 移到 `offline`。  
   - **ONLINE**（题目里没有写出来，但会出现）：把用户从 `offline` 移回 `online`。  
   - **MESSAGE**：根据 `content` 的不同有三种情况  
     1. `ALL` → 所有用户（不管在线还是离线）都 +1 次提及。  
     2. `HERE` → 只把 `online` 中的用户 +1 次提及。  
     3. 其它形式（如 `"id1 id0 id0"`） → 把字符串按空格拆成若干 `idX`，每出现一次就对应的用户 +1 次提及。  
   - 这里的“提及”可以出现多次，例如 `"id0 id0"`，就要给用户 0 加 **2**。  

4. **返回结果**  
   - 最后把每个用户的计数放进长度为 `numberOfUsers` 的列表返回即可。  

**为什么正确？**  
- 我们严格按照时间顺序处理所有状态变化（上线/下线）和消息。  
- 每一次 `MESSAGE` 只根据当时的 `online/offline` 状态来决定谁会被提及，完全符合题目要求。  

#### 代码（Python）  

```python
from typing import List

def countMentions(numberOfUsers: int, events: List[List[str]]) -> List[int]:
    # ---------- 1. 按时间戳排序 ----------
    # 时间戳是字符串，需要转成整数比较大小
    events.sort(key=lambda e: int(e[1]))

    # ---------- 2. 初始化 ----------
    online = set(range(numberOfUsers))      # 初始全部在线
    offline = set()                         # 记录离线用户
    mentions = [0] * numberOfUsers          # 提及计数

    # ---------- 3. 逐条处理 ----------
    for typ, _, data in events:   # typ = "MESSAGE"/"OFFLINE"/"ONLINE"
        if typ == "OFFLINE":
            uid = int(data)               # data 直接是用户编号
            if uid in online:
                online.remove(uid)
                offline.add(uid)

        elif typ == "ONLINE":
            uid = int(data)
            if uid in offline:
                offline.remove(uid)
                online.add(uid)

        else:   # MESSAGE
            content = data.strip()
            if content == "ALL":
                # 所有用户都被提及一次
                for i in range(numberOfUsers):
                    mentions[i] += 1
            elif content == "HERE":
                # 只给当前在线的用户加一
                for uid in online:
                    mentions[uid] += 1
            else:
                # 形如 "id1 id0 id0"
                # 把每个 id 拆出来，逐个计数
                for token in content.split():
                    # token 形如 "id3"
                    uid = int(token[2:])   # 去掉前面的 "id"
                    mentions[uid] += 1

    # ---------- 4. 返回 ----------
    return mentions
```

> **关键行中文注释**已经写在代码里，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(E * U)`  
  - `E = len(events)`（最多 100）  
  - `U = numberOfUsers`（最多 100）  
  - 最坏情况是每条 `MESSAGE` 都是 `"ALL"`，需要遍历所有用户一次。  
  - 用大白话说，就是“事件数量乘以用户数量”。在本题的约束下最多是 `100 * 100 = 10⁴` 步，完全够用。  

- **空间复杂度**：`O(U)`  
  - 主要是 `online`、`offline` 两个集合以及 `mentions` 列表，各自最多保存 `U` 个整数。  

---  

### 2. 最优解  

#### 思路  

暴力解已经满足题目约束，但如果把 `U` 放大到几万甚至更多，遍历全部用户的 `ALL` 消息就会成为瓶颈。  
我们可以把 **“所有用户都被提及一次”** 的操作改成 **“累计一个全局增量”**，这样就不必每次都遍历 `U` 了。思路如下：

1. **全局计数 `global_add`**  
   - 每当出现 `"ALL"` 消息时，`global_add += 1`。  
   - 这相当于把 “所有用户 +1” 的效果延迟到最后统一加上。  

2. **对单独提及的用户维护局部计数**  
   - `personal[i]` 记录用户 `i` 因为 `"idX"`、`"HERE"`（只针对在线用户）等得到的提及次数。  
   - 对于 `"HERE"`，我们仍然需要遍历当前在线集合，但在线集合的大小通常远小于全部用户。  

3. **最终合并**  
   - 结果 `mentions[i] = personal[i] + global_add`。  
   - 这样即使有很多 `"ALL"`，我们也只做 **一次** 加法，而不是每条消息都遍历全部用户。  

4. **集合的使用**  
   - `online` 仍然用 `set`，因为我们仍需快速判断一个用户是否在线（`O(1)`）。  

> **核心技巧**：把对所有元素的相同操作抽象成一个“全局增量”，只在最后一次性合并。这个技巧在「区间加」或「批量更新」类题目里非常常见。

#### 代码（Python）  

```python
from typing import List

def countMentions_opt(numberOfUsers: int, events: List[List[str]]) -> List[int]:
    # 1️⃣ 按时间戳排序
    events.sort(key=lambda e: int(e[1]))

    # 2️⃣ 初始化
    online = set(range(numberOfUsers))   # 初始全在线
    personal = [0] * numberOfUsers       # 只记录非 ALL 的提及
    global_add = 0                       # ALL 消息的累计增量

    # 3️⃣ 逐条处理
    for typ, _, data in events:
        if typ == "OFFLINE":
            uid = int(data)
            online.discard(uid)          # 若已离线则不报错
        elif typ == "ONLINE":
            uid = int(data)
            online.add(uid)
        else:  # MESSAGE
            content = data.strip()
            if content == "ALL":
                global_add += 1          # 只累加一次，不遍历用户
            elif content == "HERE":
                # 只给当前在线的用户加 1
                for uid in online:
                    personal[uid] += 1
            else:
                # "idX idY ..."
                for token in content.split():
                    uid = int(token[2:])
                    personal[uid] += 1

    # 4️⃣ 合并全局增量得到最终答案
    return [cnt + global_add for cnt in personal]
```

#### 复杂度  

- **时间复杂度**：`O(E * O_online)`，其中 `O_online` 是每次 `"HERE"` 消息需要遍历的在线用户数。  
  - 对于 `"ALL"` 只做 `O(1)`（全局增量），所以即使出现 10⁴ 条 `"ALL"`，也不会导致 `U` 级别的遍历。  
  - 在最坏情况下（所有用户一直在线且每条都是 `"HERE"`），仍然是 `O(E * U)`，但这已经是题目给出的下界。  

- **空间复杂度**：`O(U)`，同样只保存 `online`、`personal` 两个长度为 `U` 的结构。  

> 与暴力解相比，**唯一的提升**在于大量 `"ALL"` 消息时的时间节省——从每条 `O(U)` 降到 `O(1)`。

---  

## 心得  

- **核心技巧**：全局增量（lazy update） + 集合快速判断在线状态。  
- **适用的题型**  
  1. “对所有元素加 1” 或 “对某个区间统一加值” 的批量更新问题。  
  2. 需要频繁查询“当前满足某条件的子集”（如在线用户）时，使用 `set`/`hash` 进行 O(1) 判断。  
- **一句话总结解题钥匙**：把对“所有人”做的相同操作抽象成一个全局计数，真正需要遍历的只剩下“局部”或“在线”用户。  

---  

## 反思  

- **第一反应**：先把事件按时间排好序，然后一步步模拟状态变化，这几乎是所有“事件流”题的标准做法。  
- **最容易踩的坑**  
  1. **同时间戳的顺序**：题目要求离线/上线状态要在同时间戳的消息之前处理，排序后仍需按原始顺序遍历（Python 稳定排序天然满足）。  
  2. **`HERE` 只针对在线用户**，而 `ALL` 包括离线用户。忘记区分会导致计数错误。  
  3. **重复提及**：`"id0 id0"` 必须计两次，而不是只计一次。  
- **下次类似题的第一步**：先明确“全局操作”和“局部操作”是否可以分离；如果可以，先用全局计数把全局操作压缩，再只对局部集合进行遍历。这样往往能把时间从 `O(N·M)` 降到 `O(N + M)`。