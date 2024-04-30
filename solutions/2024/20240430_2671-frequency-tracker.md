# #2671. **频率追踪器** / Frequency Tracker

> 难度：中等 · 标签：Hash Table、Design · [LeetCode 链接](https://leetcode.com/problems/frequency-tracker/)

---

## 题目（英文原版）

**Description**

Design a data structure that keeps track of the values in it and answers some queries regarding their frequencies.
Implement the FrequencyTracker class.

**Examples**

**Example 1:**

```
Input
["FrequencyTracker", "add", "add", "hasFrequency"]
[[], [3], [3], [2]]
Output
[null, null, null, true]

Explanation
FrequencyTracker frequencyTracker = new FrequencyTracker();
frequencyTracker.add(3); // The data structure now contains [3]
frequencyTracker.add(3); // The data structure now contains [3, 3]
frequencyTracker.hasFrequency(2); // Returns true, because 3 occurs twice
```

**Example 2:**

```
Input
["FrequencyTracker", "add", "deleteOne", "hasFrequency"]
[[], [1], [1], [1]]
Output
[null, null, null, false]

Explanation
FrequencyTracker frequencyTracker = new FrequencyTracker();
frequencyTracker.add(1); // The data structure now contains [1]
frequencyTracker.deleteOne(1); // The data structure becomes empty []
frequencyTracker.hasFrequency(1); // Returns false, because the data structure is empty
```

**Example 3:**

```
Input
["FrequencyTracker", "hasFrequency", "add", "hasFrequency"]
[[], [2], [3], [1]]
Output
[null, false, null, true]

Explanation
FrequencyTracker frequencyTracker = new FrequencyTracker();
frequencyTracker.hasFrequency(2); // Returns false, because the data structure is empty
frequencyTracker.add(3); // The data structure now contains [3]
frequencyTracker.hasFrequency(1); // Returns true, because 3 occurs once
```

**Constraints**

- 1 <= number <= 105
- 1 <= frequency <= 105
- At most, 2 * 105 calls will be made to add, deleteOne, and hasFrequency in total.

---

## 题目（中文翻译）

设计一个数据结构（data structure），能够记录其中出现的数值并能够就这些数值的出现次数（frequency）回答若干查询。

实现 `FrequencyTracker` 类，支持以下操作：

- `add(int number)`：向数据结构中添加一个 `number`。
- `deleteOne(int number)`：如果 `number` 在数据结构中出现至少一次，则删除其中的一个实例；否则不做任何操作。
- `hasFrequency(int frequency)`：如果数据结构中存在至少一个数，其出现次数恰好等于 `frequency`，返回 `true`，否则返回 `false`。

---

### 示例

#### 示例 1
```json
Input
["FrequencyTracker", "add", "add", "hasFrequency"]
[[], [3], [3], [2]]

Output
[null, null, null, true]
```

**解释**  
```java
FrequencyTracker frequencyTracker = new FrequencyTracker();
frequencyTracker.add(3);          // 数据结构现在包含 [3]
frequencyTracker.add(3);          // 数据结构现在包含 [3, 3]
frequencyTracker.hasFrequency(2); // 返回 true，因为数字 3 出现了两次
```

#### 示例 2
```json
Input
["FrequencyTracker", "add", "deleteOne", "hasFrequency"]
[[], [1], [1], [1]]

Output
[null, null, null, false]
```

**解释**  
```java
FrequencyTracker frequencyTracker = new FrequencyTracker();
frequencyTracker.add(1);           // 数据结构现在包含 [1]
frequencyTracker.deleteOne(1);    // 数据结构变为空 []
frequencyTracker.hasFrequency(1); // 返回 false，因为数据结构中没有出现次数为 1 的数
```

#### 示例 3
```json
Input
["FrequencyTracker", "hasFrequency", "add", "hasFrequency"]
[[], [2], [3], [1]]

Output
[null, false, null, true]
```

**解释**  
```java
FrequencyTracker frequencyTracker = new FrequencyTracker();
frequencyTracker.hasFrequency(2); // 返回 false，因为数据结构为空
frequencyTracker.add(3);          // 数据结构现在包含 [3]
frequencyTracker.hasFrequency(1); // 返回 true，因为数字 3 出现了恰好一次
```

---

### 约束条件

- `1 <= number <= 10^5`
- `1 <= frequency <= 10^5`
- 至多 `2 * 10^5` 次调用 `add`、`deleteOne` 和 `hasFrequency`（总计）



---

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把所有出现的数字全部保存在一个 **列表**（或数组）里，  
- `add(x)`：直接把 `x` 加到列表末尾。  
- `deleteOne(x)`：遍历列表找到第一个 `x` 并删掉（找不到就什么也不做）。  
- `hasFrequency(f)`：遍历整个列表，用一个临时的 **哈希表**（可以把它想象成“查字典”，单词是数字，页码是出现次数）统计每个数字出现了多少次，最后检查有没有出现次数恰好等于 `f` 的数字。

这种做法的正确性很容易理解：我们真的把所有数字都记录下来，统计时不遗漏任何一个。

#### 代码（Python）

```python
class FrequencyTracker:
    def __init__(self):
        # 用列表保存所有出现的数字
        self.nums = []                     # [] 表示空集合

    def add(self, number: int) -> None:
        # 直接把 number 加到列表末尾
        self.nums.append(number)           # O(1)

    def deleteOne(self, number: int) -> None:
        # 在列表中寻找第一个 number 并删除
        for i, val in enumerate(self.nums):
            if val == number:               # 找到第一条匹配的记录
                self.nums.pop(i)            # 删除该元素
                break                       # 只删一次，直接退出
        # 若列表里没有 number，什么也不做

    def hasFrequency(self, frequency: int) -> bool:
        # 统计每个数字出现的次数
        cnt = {}                           # 哈希表：key = 数字，value = 出现次数
        for v in self.nums:                # 遍历所有数字
            cnt[v] = cnt.get(v, 0) + 1

        # 检查是否有任意数字的出现次数恰好等于 frequency
        for times in cnt.values():
            if times == frequency:
                return True
        return False
```

#### 复杂度

- **时间复杂度**  
  - `add`：O(1)（只往列表尾部加一个元素）  
  - `deleteOne`：最坏 O(n)（需要遍历整个列表寻找要删的数）  
  - `hasFrequency`：O(n)（要遍历全部元素才能统计出现次数）  
  这里的 **n** 代表当前列表里元素的总数。  
  用大白话说，`O(n)` 就像“随人数多少线性增长”，人数翻倍，时间也大概会翻倍。

- **空间复杂度**  
  - 只用了一个列表保存所有数字，最坏需要 O(n) 的额外空间。  
  - `cnt` 哈希表在 `hasFrequency` 时临时出现，最多也只会有不超过 n 条记录，所以整体仍是 O(n)。

> 这种暴力解在 **2·10⁵** 次操作的上限下会超时，因为每次查询都要遍历全部元素，累计的工作量会达到 10¹⁰ 级别，远远超过机器能接受的范围。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 出在每次 `hasFrequency` 以及 `deleteOne` 都要遍历全部元素来重新统计频次。  
我们需要一种方式，让这三个操作都 **只用 O(1)（常数时间）** 完成。

关键点有两点：

1. **记录每个数字当前的出现次数**  
   用一个哈希表 `num2freq`（或因为数字范围 ≤ 10⁵，也可以直接用长度为 10⁵+1 的整数数组）保存 `num → 当前频次`。  
   - `add(x)`：把 `x` 的频次加 1。  
   - `deleteOne(x)`：如果 `x` 曾出现过，就把它的频次减 1（最小降到 0 即可删除记录）。

2. **记录“有多少种数字的频次是 f”**  
   再用一个哈希表 `freqCount` 保存 `freq → 具有该频次的数字种类数`。  
   - 当某个数字的频次从 `old` 变成 `new` 时，`freqCount[old]` 要减 1，`freqCount[new]` 要加 1。  
   - `hasFrequency(f)` 只需要检查 `freqCount[f]` 是否大于 0，即可在 **O(1)** 时间内得到答案。

把这两个表 **同步更新**，就能在每次操作后保持完整的频次信息。

> 类比：  
> - `num2freq` 像一本“词典”，词是数字，解释是它出现了几次。  
> - `freqCount` 像一本“目录”，目录页码是出现次数，内容是有多少个词恰好在这页。  
> 当我们在词典里改动一个词的解释时，目录也要相应地增删页码的计数，这样查目录（`hasFrequency`）就非常快。

#### 代码（Python）

```python
class FrequencyTracker:
    def __init__(self):
        # number -> 当前出现次数
        self.num2freq = {}          # 用 dict，键是数字，值是出现次数

        # frequency -> 具有该出现次数的数字种类数
        self.freqCount = {}        # 键是出现次数，值是有多少不同的数字恰好出现这么多次

    def _inc_freq(self, number: int) -> None:
        """内部帮助函数：把 number 的出现次数加 1，并同步更新 freqCount"""
        old = self.num2freq.get(number, 0)   # 之前的频次，默认 0（即不存在）
        new = old + 1                        # 新的频次

        # 更新 num2freq
        self.num2freq[number] = new

        # 老频次的计数减 1（如果 old 为 0，说明之前没有记录，不需要减）
        if old > 0:
            self.freqCount[old] -= 1
            if self.freqCount[old] == 0:
                # 为了省空间，频次为 0 时可以删掉键
                del self.freqCount[old]

        # 新频次的计数加 1
        self.freqCount[new] = self.freqCount.get(new, 0) + 1

    def _dec_freq(self, number: int) -> None:
        """内部帮助函数：把 number 的出现次数减 1（若已存在），并同步更新 freqCount"""
        if number not in self.num2freq:
            return                     # 这个数字根本不存在，直接返回

        old = self.num2freq[number]    # 之前的频次，必定 >= 1
        new = old - 1                  # 新的频次

        # 更新 num2freq：若 new 为 0，就把键删掉
        if new == 0:
            del self.num2freq[number]
        else:
            self.num2freq[number] = new

        # 老频次的计数减 1
        self.freqCount[old] -= 1
        if self.freqCount[old] == 0:
            del self.freqCount[old]

        # 新频次（>0）的计数加 1
        if new > 0:
            self.freqCount[new] = self.freqCount.get(new, 0) + 1

    def add(self, number: int) -> None:
        """把 number 加入数据结构（出现次数+1）"""
        self._inc_freq(number)   # 只需要 O(1) 的哈希表操作

    def deleteOne(self, number: int) -> None:
        """删除一个 number（出现次数-1），若不存在则不做任何事"""
        self._dec_freq(number)   # 只需要 O(1) 的哈希表操作

    def hasFrequency(self, frequency: int) -> bool:
        """检查是否存在至少一种数字，它的出现次数恰好等于 frequency"""
        # 只要 freqCount[frequency] 大于 0 即可
        return self.freqCount.get(frequency, 0) > 0
```

#### 复杂度

- **时间复杂度**  
  - `add`、`deleteOne`、`hasFrequency` 均为 **O(1)**（常数时间）。  
  - 这里的 O(1) 表示不随数据规模增长，操作只涉及几次哈希表的查找、插入或删除，类似“一次翻页”就能完成。

- **空间复杂度**  
  - 最坏情况下会记录每个不同数字的频次以及每种出现次数的计数，数量均不超过 **2·10⁵**（因为调用次数的上限），所以空间是 **O(N)**，其中 N 为不同数字的种类数。  
  - 用数组实现时（因为 `number ≤ 10⁵`），空间上限仍是线性的，但常数更小。

> 与暴力解相比，时间复杂度从每次 O(n) 降到了 O(1)，大幅提升了效率，完全可以通过所有测试。

---

## 心得

- **核心技巧**：使用 **双哈希表同步维护**——一个记录“元素 → 频次”，另一个记录“频次 → 有多少种元素”。  
- **适用场景**  
  1. 需要频繁查询“是否存在出现次数为 k 的元素”这类**频次查询**的问题（如 LeetCode 2202 `Maximize the Topmost Element After K Moves` 的计数变体）。  
  2. 需要在 **增删改** 操作后快速判断某种统计属性是否满足的题目（如“出现次数恰好为 1 的元素是否存在”）。  
  3. “出现次数统计 + 是否满足阈值” 的组合问题，例如 “统计出现次数至少为 m 的不同字符数”。  
- **一句话总结解题钥匙**：**把“元素的频次”和“频次的出现次数”分别用两个映射记录，保持同步更新，就能在 O(1) 时间内回答所有频次相关的查询。**

---

## 反思

- **拿到题目第一反应**：直接用列表或字典统计，每次查询重新遍历计数——这是一种自然但低效的实现。  
- **最容易踩的坑**  
  1. **同步更新**：忘记在 `add`/`deleteOne` 时同时更新 `freqCount`，导致 `hasFrequency` 的结果不准确。  
  2. **边界条件**：删除时频次降到 0，需要把对应键从 `num2freq`（以及 `freqCount[0]`）中删除，否则会产生“频次 0 仍被计数”的错误。  
  3. **整数范围**：虽然题目限制 `number ≤ 10⁵`，但实现时仍应使用哈希表而不是固定大小的数组，以免误用导致越界。  
- **下次遇到同类题的第一步**：先思考 **“我需要快速得到什么统计信息？”**，如果是 “某个统计值是否存在”，就立刻考虑 **额外维护一个计数映射**（即双哈希表）来把查询转化为 O(1)。