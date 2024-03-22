# #2622. 带时限的缓存 / Cache With Time Limit

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/cache-with-time-limit/)

---

## 题目（英文原版）

**Description**

Write a class that allows getting and setting key-value pairs, however a time until expiration is associated with each key.
The class has three public methods:
set(key, value, duration): accepts an integer key, an integer value, and a duration in milliseconds. Once the duration has elapsed, the key should be inaccessible. The method should return true if the same un-expired key already exists and false otherwise. Both the value and duration should be overwritten if the key already exists.
get(key): if an un-expired key exists, it should return the associated value. Otherwise it should return -1.
count(): returns the count of un-expired keys.

**Examples**

**Example 1:**

```
Input: 
actions = ["TimeLimitedCache", "set", "get", "count", "get"]
values = [[], [1, 42, 100], [1], [], [1]]
timeDelays = [0, 0, 50, 50, 150]
Output: [null, false, 42, 1, -1]
Explanation:
At t=0, the cache is constructed.
At t=0, a key-value pair (1: 42) is added with a time limit of 100ms. The value doesn't exist so false is returned.
At t=50, key=1 is requested and the value of 42 is returned.
At t=50, count() is called and there is one active key in the cache.
At t=100, key=1 expires.
At t=150, get(1) is called but -1 is returned because the cache is empty.
```

**Example 2:**

```
Input: 
actions = ["TimeLimitedCache", "set", "set", "get", "get", "get", "count"]
values = [[], [1, 42, 50], [1, 50, 100], [1], [1], [1], []]
timeDelays = [0, 0, 40, 50, 120, 200, 250]
Output: [null, false, true, 50, 50, -1, 0]
Explanation:
At t=0, the cache is constructed.
At t=0, a key-value pair (1: 42) is added with a time limit of 50ms. The value doesn't exist so false is returned.
At t=40, a key-value pair (1: 50) is added with a time limit of 100ms. A non-expired value already existed so true is returned and the old value was overwritten.
At t=50, get(1) is called which returned 50.
At t=120, get(1) is called which returned 50.
At t=140, key=1 expires.
At t=200, get(1) is called but the cache is empty so -1 is returned.
At t=250, count() returns 0 because the cache is empty.
```

**Constraints**

- 0 <= key, value <= 109
- 0 <= duration <= 1000
- 1 <= actions.length <= 100
- actions.length === values.length
- actions.length === timeDelays.length
- 0 <= timeDelays[i] <= 1450
- actions[i] is one of "TimeLimitedCache", "set", "get" and "count"
- First action is always "TimeLimitedCache" and must be executed immediately, with a 0-millisecond delay

---

## 题目（中文翻译）

编写一个类，用于获取和设置键值对（key-value pair），但每个键都关联一个**过期时间**（time until expiration）。该类提供三个公开方法：

- **set(key, value, duration)**：接受整数 **key**、整数 **value**，以及以毫秒为单位的 **duration**（持续时间）。当 **duration** 过去后，该键应不可访问。若已经存在同一 **未过期**（un‑expired）的键，则返回 `true`，否则返回 `false`。如果键已经存在，则同时覆盖其 **value** 和 **duration**。

- **get(key)**：若存在 **未过期** 的键，则返回其对应的 **value**；否则返回 `-1`。

- **count()**：返回 **未过期** 键的数量。

---

### 示例 1

```text
actions = ["TimeLimitedCache", "set", "get", "count", "get"]
values = [[], [1, 42, 100], [1], [], [1]]
timeDelays = [0, 0, 50, 50, 150]
Output: [null, false, 42, 1, -1]
```

**解释**  
- 在 `t=0` 时，构造缓存对象。  
- 同时在 `t=0`，添加键值对 `(1: 42)`，其时限为 `100ms`。因为该键此前不存在，返回 `false`。  
- 在 `t=50`，请求键 `1`，仍在有效期内，返回 `42`。  
- 在 `t=50`，调用 `count()`，仍有一个未过期的键，返回 `1`。  
- 在 `t=150`，键 `1` 已经过期，`get(1)` 返回 `-1`。

---

### 示例 2

```text
actions = ["TimeLimitedCache", "set", "set", "get", "get", "get", "count"]
values = [[], [1, 42, 50], [1, 50, 100], [1], [1], [1], []]
timeDelays = [0, 0, 40, 50, 120, 200, 250]
Output: [null, false, true, 50, 50, -1, 0]
```

**解释**  
- 在 `t=0`，构造缓存对象。  
- 同时在 `t=0`，添加键值对 `(1: 42)`，时限 `50ms`，返回 `false`（键不存在）。  
- 在 `t=40`，再次调用 `set(1, 50, 100)`，此时键 `1` 仍未过期，返回 `true`，并覆盖原来的 **value** 为 `50`，**duration** 为 `100ms`。  
- 在 `t=50`，`get(1)` 返回 `50`（仍在有效期内）。  
- 在 `t=120`，`get(1)` 仍返回 `50`（因为上一次 `set` 将有效期延长至 `t=140`）。  
- 在 `t=200`，键已过期，`get(1)` 返回 `-1`。  
- 在 `t=250`，`count()` 返回 `0`，因为没有未过期的键。

---

### 约束条件

- `0 <= key, value <= 10^9`
- `0 <= duration <= 1000`
- `1 <= actions.length <= 100`
- `actions.length == values.length == timeDelays.length`
- `0 <= timeDelays[i] <= 1450`
- `actions[i]` 为 `"TimeLimitedCache"`、`"set"`、`"get"` 或 `"count"` 之一
- 第一个操作必定是 `"TimeLimitedCache"`，且必须立即执行（延迟为 `0` 毫秒）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把缓存的内容全部放进一个 **字典**（`dict`），键是 `key`，值是一个二元组 `(value, expire_time)`，其中  

* `value` – 真正保存的数值  
* `expire_time` – “这个键什么时候会失效”。我们把它记成 **当前时间 + duration**（毫秒），相当于给它贴了一个“有效期”标签。  

> **类比**：字典就像一本电话号码簿，`key` 是人的名字，`value` 是电话号码。这里我们给每个人再贴上一张“小纸条”，上面写着“这张纸条在 `expire_time` 以后就会被撕掉”。只要纸条还在，查询就成功；纸条被撕掉了，就当这个人不存在。

实现每个接口：

* **`set(key, value, duration)`**  
  1. 计算 `expire_time = now + duration`。  
  2. 检查 `key` 是否已经在字典里且未过期（`now < old_expire_time`），如果是返回 `True`，否则返回 `False`。  
  3. 把 `(value, expire_time)` 写进去（覆盖旧值）。  

* **`get(key)`**  
  1. 看字典里有没有 `key`。  
  2. 若有，比较 `now` 与 `expire_time`：未过期就返回 `value`，过期则删除该键并返回 `-1`。  

* **`count()`**  
  1. 需要遍历字典的所有键，逐个检查是否已过期。  
  2. 统计未过期的数量并返回。  

> 这种做法之所以 **正确**，是因为我们在每一次查询/计数时都“现场”检查了键的有效期，保证了不会误读已经失效的键。

#### 代码（Python）

```python
import time
from typing import Dict, Tuple

class TimeLimitedCache:
    """暴力实现：字典 + 过期时间"""

    def __init__(self):
        # key -> (value, expire_timestamp)
        self.store: Dict[int, Tuple[int, float]] = {}

    def _now(self) -> float:
        """返回当前时间的毫秒数（float），统一使用这个函数方便以后改成模拟时间"""
        return time.time() * 1000  # 秒 → 毫秒

    def set(self, key: int, value: int, duration: int) -> bool:
        """插入或覆盖键值，返回 True 表示已有未过期键被覆盖"""
        now = self._now()
        expire = now + duration
        existed_unexpired = False

        if key in self.store:
            _, old_expire = self.store[key]
            if now < old_expire:          # 旧键仍然有效
                existed_unexpired = True

        # 直接写入新值（覆盖旧值）
        self.store[key] = (value, expire)
        return existed_unexpired

    def get(self, key: int) -> int:
        """获取未过期的值，若不存在或已过期返回 -1"""
        now = self._now()
        if key not in self.store:
            return -1
        value, expire = self.store[key]
        if now < expire:                # 未过期
            return value
        # 已过期，立刻清理
        del self.store[key]
        return -1

    def count(self) -> int:
        """统计当前未过期的键数量"""
        now = self._now()
        # 先把已经过期的键删掉，防止下次重复遍历
        expired_keys = [k for k, (_, exp) in self.store.items() if now >= exp]
        for k in expired_keys:
            del self.store[k]

        return len(self.store)
```

> **注意**：在真实的 LeetCode 环境里会使用 `setTimeout/clearTimeout`（JavaScript）或计时器来自动删除键；这里我们用 **手动检查** 的方式模拟，思路更直观。

#### 复杂度

- **时间复杂度**  
  *`set`*：`O(1)`（字典写入/覆盖）  
  *`get`*：`O(1)`（字典查找）  
  *`count`*：`O(n)`，因为需要遍历所有键检查是否过期。  
  > 这里的 `n` 就是当前缓存里存的键的数量。想象成我们把所有钥匙都拿出来，一个一个检查是否还能打开锁，显然会花更多时间。

- **空间复杂度**  
  `O(n)`，我们需要把每个键的值和过期时间都存下来。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在 `count()`——每次都要遍历全部键。  
如果我们能够 **随时把已经失效的键删掉**，那么 `count` 只需要返回字典的大小即可，时间就降到 `O(1)`。

**优化的关键点**：

1. **提前知道哪个键最先会失效**。  
   - 把所有 `(expire_time, key)` 放进一个 **最小堆**（`heapq`），堆顶永远是最早到期的键。  
   - 这相当于把所有钥匙排好顺序，最先失效的钥匙排在最前面，想把失效钥匙清掉时，只需要查看堆顶。

2. **懒删除 + 及时清理**。  
   - 每次在 `set/get/count` 之前，先检查堆顶的 `expire_time` 是否已经 ≤ 当前时间。  
   - 若是，则弹出堆顶并在字典中同步删除对应的键。  
   - 这样可以保证字典里永远只保留 **未过期** 的键，`count` 直接返回 `len(dict)`。

3. **覆盖已有键时要把旧的超时记录从堆中移除**。  
   - 直接把旧记录留在堆里也是可以的，因为在下次“清理堆”时会发现它对应的键已经被新记录覆盖（字典里保存的是更新后的 `expire_time`），于是跳过。  
   - 为了代码更简洁，我们采用 **“标记法”**：只在堆里加入新记录，不主动删除旧记录；在弹出时再判断是否仍然有效。

> **类比**：  
> 想象我们在超市排队结账，每个人都有一个“离开时间”。如果我们把所有人排成一列，最早离开的排在最前面（最小堆），每当超市关门（查询时）就从前面一个一个检查，发现已经离开的就让他们离开。这样我们不需要每次检查全部顾客，只检查最前面的几个。

#### 代码（Python）

```python
import time
import heapq
from typing import Dict, Tuple, List

class TimeLimitedCache:
    """最优实现：字典 + 最小堆（懒删除）"""

    def __init__(self):
        # key -> (value, expire_timestamp)
        self.store: Dict[int, Tuple[int, float]] = {}
        # 最小堆，元素是 (expire_timestamp, key)
        self.heap: List[Tuple[float, int]] = []

    def _now(self) -> float:
        """统一获取当前毫秒时间"""
        return time.time() * 1000

    def _clean(self) -> None:
        """
        删除所有已经过期的键。
        只要堆顶的 expire_time <= now，就把它弹出并在 dict 中同步删除。
        这里采用“懒删除”：若弹出的键在 dict 中的记录已经被新记录覆盖（expire 更大），则不删除。
        """
        now = self._now()
        while self.heap and self.heap[0][0] <= now:
            expire, key = heapq.heappop(self.heap)
            # 若 dict 中仍然保存同样的 expire，说明它真的已经过期
            if key in self.store and self.store[key][1] == expire:
                del self.store[key]

    def set(self, key: int, value: int, duration: int) -> bool:
        """
        插入或覆盖键值，返回 True 当且仅当之前有同一个 **未过期** 的键。
        """
        self._clean()                     # 先把已经失效的键清理干净
        now = self._now()
        expire = now + duration

        existed_unexpired = False
        if key in self.store:
            _, old_expire = self.store[key]
            if now < old_expire:          # 旧键仍然有效
                existed_unexpired = True

        # 写入新记录（覆盖旧值）
        self.store[key] = (value, expire)
        heapq.heappush(self.heap, (expire, key))   # 把新超时加入堆
        return existed_unexpired

    def get(self, key: int) -> int:
        """获取未过期的值，若不存在或已过期返回 -1"""
        self._clean()
        if key not in self.store:
            return -1
        value, _ = self.store[key]
        return value

    def count(self) -> int:
        """返回当前未过期键的数量，时间 O(1)（在清理完过期键后）"""
        self._clean()
        return len(self.store)
```

#### 复杂度

- **时间复杂度**  
  *`set`*：`O(log n)`，因为要把新记录 `push` 到堆里（堆的插入是对数复杂度）。  
  *`get`*：`O(log n)` 最坏情况是需要把堆中大量已经过期的键弹出，每弹出一次 `O(log n)`，但总体上每个键只会被弹出一次，摊销后仍然是 `O(log n)`。  
  *`count`*：`O(log n)`（同 `get`，主要是调用 `_clean`），但在多数情况下几乎是 `O(1)`。  

  与暴力解相比，**不再需要遍历全部键**，所以在键很多时性能提升明显。

- **空间复杂度**  
  `O(n)`，我们额外维护了一个堆，堆里最多保存和字典同样数量的记录（每次 `set` 都会产生一个新记录），因此仍是线性空间。

---

## 心得

- **核心技巧**：**最小堆 + 懒删除**。把“什么时候会失效”这件事提前排好序，查询或计数时只检查最早的几个，而不是全部。  
- **适用的题型**  
  1. **带有超时/失效时间的缓存**（如本题、LRU/TTL 缓存）。  
  2. **需要快速获取最早/最晚事件的调度系统**（如“会议室预订”或“任务调度器”）。  
  3. **统计在时间窗口内的元素数量**（滑动窗口计数）。  
- **一句话总结解题钥匙**：把“何时会失效”提前排序，用堆把最早的失效点挑出来，保持字典只保存未失效的键。

---

## 反思

- **第一反应**：直接用字典存值和过期时间，随后在每次操作时检查是否过期。  
- **最容易踩的坑**  
  1. **忘记在 `count` 时遍历清理**，导致返回的数量包含已经失效的键。  
  2. **覆盖已有键时没有更新堆**，旧的超时记录会一直残留，导致 `_clean` 时误删新键（解决办法是使用“标记法”或在覆盖时先 `clearTimeout`/删除旧堆记录）。  
  3. **时间单位混淆**：题目要求毫秒，`time.time()` 返回秒，需要乘以 `1000`。  
- **下次遇到同类题**：第一步先思考 “**哪些键会在未来失效**”，能否把它们排成有序结构（堆、平衡树、队列），再决定是**懒删除**还是**主动删除**。这样往往能把线性遍历的瓶颈降到对数甚至常数级。