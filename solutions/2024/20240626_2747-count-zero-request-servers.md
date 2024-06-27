# #2747. 统计零请求服务器 / Count Zero Request Servers

> 难度：中等 · 标签：Array、Hash Table、Sliding Window、Sorting · [LeetCode 链接](https://leetcode.com/problems/count-zero-request-servers/)

---

## 题目（英文原版）

**Description**

You are given an integer n denoting the total number of servers and a 2D 0-indexed integer array logs, where logs[i] = [server_id, time] denotes that the server with id server_id received a request at time time.
You are also given an integer x and a 0-indexed integer array queries.
Return a 0-indexed integer array arr of length queries.length where arr[i] represents the number of servers that did not receive any requests during the time interval [queries[i] - x, queries[i]].
Note that the time intervals are inclusive.

**Examples**

**Example 1:**

```
Input: n = 3, logs = [[1,3],[2,6],[1,5]], x = 5, queries = [10,11]
Output: [1,2]
Explanation: 
For queries[0]: The servers with ids 1 and 2 get requests in the duration of [5, 10]. Hence, only server 3 gets zero requests.
For queries[1]: Only the server with id 2 gets a request in duration of [6,11]. Hence, the servers with ids 1 and 3 are the only servers that do not receive any requests during that time period.
```

**Example 2:**

```
Input: n = 3, logs = [[2,4],[2,1],[1,2],[3,1]], x = 2, queries = [3,4]
Output: [0,1]
Explanation: 
For queries[0]: All servers get at least one request in the duration of [1, 3].
For queries[1]: Only server with id 3 gets no request in the duration [2,4].
```

**Constraints**

- 1 <= n <= 105
- 1 <= logs.length <= 105
- 1 <= queries.length <= 105
- logs[i].length == 2
- 1 <= logs[i][0] <= n
- 1 <= logs[i][1] <= 106
- 1 <= x <= 105
- x < queries[i] <= 106

---

## 题目（中文翻译）

**题目描述**  
给定一个整数 `n`，表示服务器的总数；以及一个二维 0 索引整数数组 `logs`，其中 `logs[i] = [server_id, time]` 表示编号为 `server_id` 的服务器在时间 `time` 收到了一次请求。  
同时给定一个整数 `x` 和一个 0 索引整数数组 `queries`。  
返回一个长度为 `queries.length` 的 0 索引整数数组 `arr`，其中 `arr[i]` 表示在时间区间 **[queries[i] - x, queries[i]]**（区间端点均包含）内 **没有收到任何请求** 的服务器数量。

**示例 1**  
```text
Input: n = 3, logs = [[1,3],[2,6],[1,5]], x = 5, queries = [10,11]
Output: [1,2]
Explanation: 
对于 queries[0]（查询时间 10）：区间为 [5, 10]，服务器 1 和 2 在此区间内都有请求，只有服务器 3 没有请求，故答案为 1。  
对于 queries[1]（查询时间 11）：区间为 [6, 11]，只有服务器 2 在此区间内有请求，服务器 1 与 3 均未收到请求，故答案为 2。
```

**示例 2**  
```text
Input: n = 3, logs = [[2,4],[2,1],[1,2],[3,1]], x = 2, queries = [3,4]
Output: [0,1]
Explanation: 
对于 queries[0]（查询时间 3）：区间为 [1, 3]，所有服务器在此区间内至少收到一次请求，故答案为 0。  
对于 queries[1]（查询时间 4）：区间为 [2, 4]，只有服务器 3 在此区间内没有请求，故答案为 1。
```

**约束条件**  
- `1 <= n <= 10^5`  
- `1 <= logs.length <= 10^5`  
- `1 <= queries.length <= 10^5`  
- `logs[i].length == 2`  
- `1 <= logs[i][0] <= n`（`server_id` 的取值范围）  
- `1 <= logs[i][1] <= 10^6`（`time` 的取值范围）  
- `1 <= x <= 10^5`  
- `x < queries[i] <= 10^6`   (对所有 `i`)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每一个查询**都去检查所有日志，看看哪些服务器在区间 `[queries[i] - x, queries[i]]` 内收到了请求。  
实现上可以：

1. 先准备一个 `set`（集合）来记录在当前区间内出现过的服务器 id。  
   - 集合在这里就像一本**查字典**：往里放一个服务器 id，如果它已经在字典里了，字典会自动帮我们去重。  
2. 遍历 `logs`，只要日志的时间 `time` 落在区间内，就把对应的 `server_id` 加进集合。  
3. 区间结束后，集合的大小就是**收到请求的服务器数量**，剩下的 `n - len(set)` 就是**没有收到请求的服务器数量**。  

这种做法**一定能得到正确答案**，因为我们把每条日志都逐一检查，没有漏掉任何可能的请求。

#### 代码（Python）

```python
from typing import List

def countZeroRequestServers_bruteforce(n: int,
                                       logs: List[List[int]],
                                       x: int,
                                       queries: List[int]) -> List[int]:
    ans = []
    for q in queries:                     # 对每个查询单独处理
        left = q - x                       # 区间左端点（含）
        right = q                          # 区间右端点（含）
        active = set()                     # 用集合记录出现过的服务器 id
        for server_id, time in logs:       # 检查所有日志
            if left <= time <= right:      # 时间在区间内
                active.add(server_id)      # 加入集合，自动去重
        ans.append(n - len(active))        # 没出现的服务器数
    return ans
```

#### 复杂度

- **时间复杂度**：`O(Q * L)`，其中 `Q = len(queries)`，`L = len(logs)`。  
  用大白话说，就是**每个查询都要遍历全部日志**，如果查询有 10 万，日志也有 10 万，最坏情况下会跑 `10^10` 次，显然太慢了。

- **空间复杂度**：`O(n)`（集合最多装下所有服务器 id），在最坏情况下会占用 `n` 个整数的空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历全部日志**。其实，查询的时间窗口是**随查询时间单调移动**的（如果我们把查询按时间排序），相邻两个查询的窗口会有大量重叠。我们可以利用这点，像 **滑动窗口 + 双指针** 那样，只在窗口边界变化时增删日志，而不是每次全扫。

具体步骤如下：

1. **排序**  
   - 按时间升序把 `logs` 排好，这样我们可以从左到右顺序“进入”或“离开”窗口。  
   - 同时把 `queries` 按时间升序排序，但要记住原始下标（因为答案需要恢复原顺序），这可以把每个查询包装成 `(time, original_index)`。

2. **滑动窗口**  
   - 维护两个指针 `l`、`r`，分别指向当前窗口左边界（不含）和右边界（含）的日志下标。窗口对应的时间区间是 `[queries[i] - x, queries[i]]`。  
   - 当我们处理下一个（更大的）查询 `q` 时，窗口右边界需要 **向右扩展**，把所有 `time <= q` 的日志加入窗口；窗口左边界需要 **向右收缩**，把所有 `time < q - x` 的日志移出窗口。

3. **统计当前窗口里出现过的服务器**  
   - 用一个长度为 `n+1` 的数组 `cnt`（下标即服务器 id）记录每个服务器在窗口中出现的次数。  
   - 再用一个变量 `active` 记录**当前窗口里出现过的不同服务器数量**。  
   - 当把一条日志加入窗口时：`if cnt[id] == 0: active += 1; cnt[id] += 1`。  
   - 当把一条日志移出窗口时：`cnt[id] -= 1; if cnt[id] == 0: active -= 1`。  
   - 这里的 `cnt` 就像一本**查字典**：`cnt[id]` 告诉我们这本字典里第 `id` 页出现了多少次。只要次数从 0 变成 1，说明这本字典里出现了新的一页（服务器），我们就把 `active` 加一；反之从 1 变成 0，就把 `active` 减一。

4. **得到答案**  
   - 对于当前查询 `q`，窗口里出现的服务器数是 `active`，所以 **没有请求的服务器数** 为 `n - active`。把它写入答案数组对应的原始下标位置。

5. **复杂度分析**  
   - 每条日志只会被 **加入一次、移出一次**，所以指针 `l`、`r` 总共移动 `O(L)` 步。  
   - 排序耗时 `O(L log L + Q log Q)`。  
   - 其余操作都是 `O(1)` 的数组访问。  
   - 因此总时间是 `O(L log L + Q log Q)`，空间 `O(n + L + Q)`（主要是 `cnt` 数组和排序后的副本）。

下面把这个思路一步步写成代码，并在关键行加上中文注释，帮助你更好地理解。

#### 代码（Python）

```python
from typing import List

def countZeroRequestServers(n: int,
                           logs: List[List[int]],
                           x: int,
                           queries: List[int]) -> List[int]:
    """
    最优解：排序 + 双指针滑动窗口
    返回每个查询对应的“在区间 [q-x, q] 内没有收到请求的服务器数量”
    """
    # 1️⃣ 把日志按时间升序排列
    logs.sort(key=lambda p: p[1])          # p[1] 是 time

    # 2️⃣ 把查询包装成 (query_time, original_index) 并排序
    indexed_q = [(t, i) for i, t in enumerate(queries)]
    indexed_q.sort(key=lambda p: p[0])     # 按查询时间升序

    # 3️⃣ 准备统计结构
    cnt = [0] * (n + 1)                     # cnt[id] = 该服务器在窗口中出现的次数
    active = 0                              # 当前窗口里出现过的不同服务器数量
    ans = [0] * len(queries)                # 最终答案，按原顺序返回

    # 4️⃣ 双指针
    l = 0                                   # 窗口左边界的下标（指向第一个不在窗口的日志）
    r = 0                                   # 窗口右边界的下标（指向第一个未加入窗口的日志）

    for q_time, q_idx in indexed_q:         # 按查询时间从小到大依次处理
        left_bound = q_time - x             # 窗口左端点（含）

        # ---- 把右指针向右移动，加入所有 time <= q_time 的日志 ----
        while r < len(logs) and logs[r][1] <= q_time:
            server_id = logs[r][0]
            if cnt[server_id] == 0:        # 这台服务器之前不在窗口里
                active += 1                # 新增一个活跃服务器
            cnt[server_id] += 1            # 次数加一
            r += 1

        # ---- 把左指针向右移动，移除所有 time < left_bound 的日志 ----
        while l < len(logs) and logs[l][1] < left_bound:
            server_id = logs[l][0]
            cnt[server_id] -= 1            # 次数减一
            if cnt[server_id] == 0:        # 这台服务器已经不在窗口里了
                active -= 1                # 活跃服务器数减一
            l += 1

        # 现在窗口正好对应区间 [q_time - x, q_time]
        ans[q_idx] = n - active              # 没有请求的服务器数

    return ans
```

#### 复杂度

- **时间复杂度**：`O(L log L + Q log Q)`  
  - `L = len(logs)`，`Q = len(queries)`。  
  - 排序是主要耗时（`log` 只是一种“放大镜”，把 100 万条数据排好序大约需要几百万次比较），随后每条日志只进出窗口一次，整体是线性级别的。

- **空间复杂度**：`O(n + L + Q)`  
  - `cnt` 数组需要 `n+1` 个整数，`logs`、`queries` 的拷贝用于排序，额外的 `ans`、`indexed_q` 也各占 `O(Q)`。  
  - 与输入规模同阶，完全可以接受。

---

## 心得

- **核心技巧**：**滑动窗口 + 双指针**（在有序序列上）配合**计数数组**（哈希表的数组实现）来实时维护“当前窗口里出现过的不同元素数量”。  
- **适用题型**（类似思路）：
  1. **“子数组中不同元素的个数”**（LeetCode 992）  
  2. **“在区间 [L,R] 内出现次数最多的元素”**（可用同样的滑动窗口思路）  
  3. **“统计每个窗口中出现次数 ≥ k 的元素数量”**（变形的频次统计）  

> **解题钥匙**：把**“每次都从头扫”**换成**“只在窗口边界变化时增删”**，这样时间从指数级降到线性级。

---

## 反思

- **第一反应**：看到“区间查询”，立刻想到**前缀和**或**二分查找**。但这里的查询是“在时间窗口内有没有出现过”，更适合**滑动窗口**而不是单纯的前缀计数。  
- **最容易踩的坑**  
  1. **时间区间是闭区间**，所以左边界 `>= q - x`（含），右边界 `<= q`（含），对应的指针移动条件要写对。  
  2. **服务器 id 从 1 开始**，所以计数数组要 `n+1` 长度，防止下标越界。  
  3. **查询需要恢复原顺序**，记得在排序时保存原始下标，否则答案会乱序。  
- **下次类似题的第一步**：  
  把所有涉及的“时间”或“位置”先**排序**，判断是否可以使用**双指针滑动窗口**来一次遍历完成所有查询。这样往往能把原本的 `O(Q·L)` 降到 `O(L log L + Q log Q)`。