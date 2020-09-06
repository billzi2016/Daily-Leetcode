# #981. Time Based Key-Value Store / Time Based Key-Value Store

> 难度：中等 · 标签：Hash Table、String、Binary Search、Design · [LeetCode 链接](https://leetcode.com/problems/time-based-key-value-store/)

---

## 题目（英文原版）

**Description**

Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.
Implement the TimeMap class:

**Examples**

**Example 1:**

```
Input
["TimeMap", "set", "get", "get", "set", "get", "get"]
[[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
Output
[null, null, "bar", "bar", null, "bar2", "bar2"]

Explanation
TimeMap timeMap = new TimeMap();
timeMap.set("foo", "bar", 1);  // store the key "foo" and value "bar" along with timestamp = 1.
timeMap.get("foo", 1);         // return "bar"
timeMap.get("foo", 3);         // return "bar", since there is no value corresponding to foo at timestamp 3 and timestamp 2, then the only value is at timestamp 1 is "bar".
timeMap.set("foo", "bar2", 4); // store the key "foo" and value "bar2" along with timestamp = 4.
timeMap.get("foo", 4);         // return "bar2"
timeMap.get("foo", 5);         // return "bar2"
```

**Constraints**

- 1 <= key.length, value.length <= 100
- key and value consist of lowercase English letters and digits.
- 1 <= timestamp <= 107
- All the timestamps timestamp of set are strictly increasing.
- At most 2 * 105 calls will be made to set and get.

---

## 题目（中文翻译）

设计一种基于时间的键值（key-value）数据结构，能够在不同的时间戳（timestamp）为同一个键存储多个值，并在给定时间戳时检索该键对应的值。

实现 `TimeMap` 类，使其支持以下操作：

- `set(key, value, timestamp)`: 在时间戳 `timestamp` 处保存键 `key` 与值 `value` 的对应关系。  
- `get(key, timestamp)`: 返回键 `key` 在不超过给定时间戳 `timestamp` 的最近一次设置的值。如果不存在对应的值，则返回空字符串 `""`（或 `null`，视语言实现而定）。

---

## 示例

**示例 1：**

```
Input
["TimeMap", "set", "get", "get", "set", "get", "get"]
[[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]

Output
[null, null, "bar", "bar", null, "bar2", "bar2"]
```

**解释**

```java
TimeMap timeMap = new TimeMap();
timeMap.set("foo", "bar", 1);   // 在时间戳 1 保存键 "foo" 与值 "bar"
timeMap.get("foo", 1);          // 返回 "bar"
timeMap.get("foo", 3);          // 返回 "bar"，因为在时间戳 3 以及之前（时间戳 2）没有对应的值，最近的有效值是时间戳 1 的 "bar"
timeMap.set("foo", "bar2", 4);  // 在时间戳 4 保存键 "foo" 与值 "bar2"
timeMap.get("foo", 4);          // 返回 "bar2"
timeMap.get("foo", 5);          // 返回 "bar2"
```

---

## 约束条件

- `1 <= key.length, value.length <= 100`
- `key` 和 `value` 只包含小写英文字母和数字。
- `1 <= timestamp <= 10^7`
- 所有 `set` 操作的时间戳 `timestamp` 严格递增。
- `set` 与 `get` 调用总次数不超过 `2 * 10^5`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把每一次 `set(key, value, timestamp)` 都记录下来，**把所有的记录放在同一个列表里**。  
当 `get(key, timestamp)` 被调用时，我们遍历这个列表，找出所有满足：

- `record.key == key`  
- `record.timestamp ≤ timestamp`

的记录，取其中 **时间戳最大的那条**（因为时间越接近、但不超过给定的 timestamp，就是我们要的值）。  

- **数据结构**：用一个普通的 Python `list` 保存 `(key, value, timestamp)` 三元组。  
  - 列表可以想象成一摞纸条，每张纸条上写着键、值和时间。我们要找的就是在这摞纸条里，满足条件的最上面那张（时间最大的那张）。  
- **为什么正确**：我们把所有历史都完整保存了，只要在查询时把不符合时间要求的记录剔除，剩下的就是合法的历史，取时间最大的即为答案。  

#### 代码（Python）  
```python
class TimeMap:
    def __init__(self):
        # 用一个列表保存所有的 (key, value, timestamp) 记录
        # 每一次 set 都直接 append 到列表尾部
        self.records = []          # List[Tuple[str, str, int]]

    def set(self, key: str, value: str, timestamp: int) -> None:
        # 直接把新记录放进去，时间戳是递增的，列表顺序天然有序
        self.records.append((key, value, timestamp))

    def get(self, key: str, timestamp: int) -> str:
        # 暴力遍历所有记录，找出满足条件的最新值
        ans = ""                  # 默认返回空字符串
        max_time = -1             # 记录目前找到的最大时间戳
        for k, v, t in self.records:
            if k == key and t <= timestamp and t > max_time:
                ans = v
                max_time = t
        return ans
```

#### 复杂度  
- **时间复杂度**：`O(N)`（N 为已执行的 `set` 次数）  
  - 每次 `get` 都要遍历所有记录，想象成我们要在一整摞纸条里逐张检查，最坏情况下要检查全部。  
- **空间复杂度**：`O(N)`  
  - 所有的历史记录都要存下来，列表的长度随 `set` 的次数线性增长。  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于 **每次查询都要遍历全部历史**。  
观察题目约束可以发现：

1. 对同一个 `key`，`set` 的时间戳是 **严格递增** 的。  
2. `get` 只需要返回 **不大于给定 timestamp 的最近时间** 的值。

因此我们可以把每个 `key` 的历史 **独立分组**，并把对应的时间戳保存成有序数组。这样查询时只需要在该 `key` 的时间戳数组里做一次 **二分查找**（Binary Search），找到 ≤ `timestamp` 的最大下标，即可得到对应的值。

- **数据结构**：  
  - 用一个 **哈希表**（Python `dict`）把 `key` 映射到两个平行列表：`times[key]` 保存该键所有的时间戳（递增），`values[key]` 保存对应的值。  
  - 哈希表就像一本“键 → 章节”的目录，`key` 是章节标题，目录告诉我们去哪个章节；每个章节内部用两行纸条分别记时间和对应的值。  

- **二分查找**：  
  - Python 标准库 `bisect` 能在有序列表里快速定位插入位置。`bisect_right(times, timestamp)` 返回 **第一个大于 timestamp 的位置**，于是 `pos-1` 就是 ≤ `timestamp` 的最大下标。  
  - 这一步的时间是 `O(log m)`，其中 `m` 是该键的历史条目数，远快于线性遍历。  

#### 代码（Python）  
```python
from bisect import bisect_right
from collections import defaultdict

class TimeMap:
    def __init__(self):
        # 对每个 key，分别记录时间戳列表和对应的值列表
        # defaultdict(list) 能自动创建空列表，省去键不存在时的判断
        self.times = defaultdict(list)   # key -> List[int]
        self.vals = defaultdict(list)    # key -> List[str]

    def set(self, key: str, value: str, timestamp: int) -> None:
        # 因为题目保证 timestamp 单调递增，直接在末尾追加即可
        self.times[key].append(timestamp)   # 记录时间
        self.vals[key].append(value)        # 记录对应的值

    def get(self, key: str, timestamp: int) -> str:
        # 若 key 从未出现过，直接返回空字符串
        if key not in self.times:
            return ""

        # 在该 key 的时间列表里二分定位
        idx = bisect_right(self.times[key], timestamp) - 1
        # idx 为 -1 说明所有时间戳都大于查询的 timestamp
        if idx < 0:
            return ""
        # 否则返回对应下标的值
        return self.vals[key][idx]
```

#### 复杂度  
- **时间复杂度**：  
  - `set`：`O(1)`（直接在列表尾部追加）  
  - `get`：`O(log m)`，`m` 为该键的历史条目数。  
    - 与暴力解的 `O(N)` 相比，二分把遍历“摞纸条”的过程压缩成了“折半查找”。  
- **空间复杂度**：`O(N)`，仍需保存所有历史记录，只是把它们按键分组存放，额外的哈希表开销是常数级的。  

---

## 心得  

- **核心技巧**：利用 **哈希表分组 + 二分查找** 把“按键查找”和“时间戳查找”两步合并为一次 O(log n) 查询。  
- **适用的题型**：  
  1. “按时间线查询历史记录”类，如 LeetCode 1146 *Snapshot Array*。  
  2. “区间或前缀查询”但需要支持离线时间戳的，如 “查询历史最大值”。  
  3. 需要 **前缀最近不超过某值** 的场景，例如“查询最近的股票价格”。  
- **一句话总结解题钥匙**：**把同一键的时间戳保持有序，二分定位最近的合法时间**。  

---

## 反思  

- **第一反应**：把所有 `set` 的记录直接放进一个大列表，查询时遍历——最自然的“全记录保存”思路。  
- **最容易踩的坑**：  
  - 忘记 `timestamp` 是严格递增的，导致在 `set` 时使用不合适的数据结构（如堆）增加不必要的复杂度。  
  - `get` 时没有处理 “所有时间都比查询的 timestamp 大” 的情况，容易出现索引越界。  
  - 对不存在的 `key` 直接返回空字符串而不是 `None`（题目要求返回空字符串）。  
- **下次遇到同类题**，第一步应该先问自己：“**同一个键的历史是否天然有序**？”如果答案是“是”，就立刻考虑 **哈希表 + 有序容器 + 二分** 的组合。