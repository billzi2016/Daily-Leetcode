# #895. 最大频率栈 / Maximum Frequency Stack

> 难度：困难 · 标签：Hash Table、Stack、Design、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/maximum-frequency-stack/)

---

## 题目（英文原版）

**Description**

Design a stack-like data structure to push elements to the stack and pop the most frequent element from the stack.
Implement the FreqStack class:

**Examples**

**Example 1:**

```
Input
["FreqStack", "push", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop"]
[[], [5], [7], [5], [7], [4], [5], [], [], [], []]
Output
[null, null, null, null, null, null, null, 5, 7, 5, 4]

Explanation
FreqStack freqStack = new FreqStack();
freqStack.push(5); // The stack is [5]
freqStack.push(7); // The stack is [5,7]
freqStack.push(5); // The stack is [5,7,5]
freqStack.push(7); // The stack is [5,7,5,7]
freqStack.push(4); // The stack is [5,7,5,7,4]
freqStack.push(5); // The stack is [5,7,5,7,4,5]
freqStack.pop();   // return 5, as 5 is the most frequent. The stack becomes [5,7,5,7,4].
freqStack.pop();   // return 7, as 5 and 7 is the most frequent, but 7 is closest to the top. The stack becomes [5,7,5,4].
freqStack.pop();   // return 5, as 5 is the most frequent. The stack becomes [5,7,4].
freqStack.pop();   // return 4, as 4, 5 and 7 is the most frequent, but 4 is closest to the top. The stack becomes [5,7].
```

**Constraints**

- 0 <= val <= 109
- At most 2 * 104 calls will be made to push and pop.
- It is guaranteed that there will be at least one element in the stack before calling pop.

---

## 题目（中文翻译）

设计一种类似栈的数据结构，使得可以向栈中压入元素（push），并弹出出现频率最高的元素（pop）。

实现 `FreqStack` 类，使其支持以下操作：

- `FreqStack()`：构造函数，初始化一个空的频率栈。
- `void push(int val)`：将整数 `val` 压入栈中。
- `int pop()`：移除并返回出现频率最高的元素。如果多个元素出现频率相同，则弹出 **最近** 压入的那个（即栈顶最靠近的元素）。

---

## 示例

### 示例 1

**输入**

```json
["FreqStack", "push", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop"]
[[], [5], [7], [5], [7], [4], [5], [], [], [], []]
```

**输出**

```json
[null, null, null, null, null, null, null, 5, 7, 5, 4]
```

**解释**

```java
FreqStack freqStack = new FreqStack();
freqStack.push(5); // 栈变为 [5]
freqStack.push(7); // 栈变为 [5,7]
freqStack.push(5); // 栈变为 [5,7,5]
freqStack.push(7); // 栈变为 [5,7,5,7]
freqStack.push(4); // 栈变为 [5,7,5,7,4]
freqStack.push(5); // 栈变为 [5,7,5,7,4,5]
freqStack.pop();   // 返回 5，因为 5 的出现频率最高。栈变为 [5,7,5,7,4]。
freqStack.pop();   // 返回 7，因为 5 与 7 的出现频率相同，但 7 更靠近栈顶。栈变为 [5,7,5,4]。
freqStack.pop();   // 返回 5，因为 5 的出现频率最高。栈变为 [5,7,4]。
freqStack.pop();   // 返回 4，因为 4、5、7 的出现频率相同，但 4 更靠近栈顶。栈变为 [5,7]。
```

---

## 约束条件

- `0 <= val <= 10^9`
- 最多会有 `2 * 10^4` 次对 `push` 和 `pop` 的调用。
- 在调用 `pop` 之前，保证栈中至少有一个元素。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有元素都放进一个普通的 Python 列表 `stack`，  
- **push**：直接 `stack.append(val)`，相当于往栈顶压入一个新元素，和真实的栈没有区别。  
- **pop**：要弹出“出现次数最多且离栈顶最近的元素”。我们可以先遍历 `stack`，统计每个数出现了多少次（用 **哈希表**，它就像一本词典，单词是 `key`，对应的解释是 `value`），得到每个值的频率；再找出最高的频率 `max_freq`，最后再从 **栈顶向下** 扫一遍，找到第一个频率等于 `max_freq` 的元素并删除它。

> **为什么正确**  
> - 统计频率得到的 `max_freq` 必然是当前所有元素中出现次数最多的。  
> - 从栈顶向下第一次碰到频率等于 `max_freq` 的元素，就是“最近的”那个，符合题目要求。  

> **复杂度大白话**  
> - `O(n)` 中的 `n` 代表栈里元素的个数。这里我们每次 **pop** 都要遍历整个栈一次，最坏情况下要看 `n` 次，时间会随栈的长度线性增长。  
> - `O(1)` 表示不随输入规模增长，常数时间。

#### 代码（Python）

```python
class FreqStack:
    def __init__(self):
        # 用列表模拟普通栈，stack[-1] 是栈顶
        self.stack = []

    # 把元素压入栈顶
    def push(self, val: int) -> None:
        self.stack.append(val)          # 直接放到列表末尾

    # 弹出出现频率最高且最靠近栈顶的元素
    def pop(self) -> int:
        # 1. 统计每个值的出现次数（哈希表 = dict）
        freq = {}
        for x in self.stack:
            freq[x] = freq.get(x, 0) + 1

        # 2. 找出最大的出现次数
        max_freq = max(freq.values())

        # 3. 从栈顶往下找，第一个满足频率 = max_freq 的元素就是答案
        for i in range(len(self.stack) - 1, -1, -1):
            if freq[self.stack[i]] == max_freq:
                ans = self.stack.pop(i)   # 删除该元素并返回
                return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`（`n` 为当前栈的大小）  
  - `push` 只做一次 `append`，是 `O(1)`。  
  - `pop` 需要遍历整个栈两遍：一次统计频率，一次从栈顶找目标，所以是线性的 `O(n)`。  
- **空间复杂度**：`O(n)`  
  - 额外的哈希表 `freq` 最多会存放栈里所有不同的元素，最坏情况下和栈大小相同。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次 `pop` 都要遍历整个栈来统计频率。  
我们需要把“频率”这件事 **提前** 做好，使得 `pop` 能够 **瞬间** 找到答案。  

**关键观察**  

1. **频率只会增不减**：每次 `push` 只会让某个数的出现次数加 1，`pop` 只会把已经出现最多的那个数弹走，导致它的频率减 1。  
2. **相同频率的元素之间仍然保持栈的顺序**：如果两个数的出现次数相同，弹出的是更靠近栈顶的那个。  

**由此可以构造两层映射**  

- `cnt[x]`（哈希表）记录每个数 `x` 当前的出现次数。  
- `group[f]`（哈希表，值是 **栈**）记录所有出现次数为 `f` 的数，**按压入顺序保存**。  
  - 当我们把一个数 `x` 的频率提升到 `f` 时，就把 `x` 推入 `group[f]`。  
  - 由于我们总是把新出现的元素压到对应频率的栈顶，所以 `group[f]` 的栈顶就是“频率为 `f` 且最近压入的元素”。  

另外维护一个变量 `maxFreq`，始终保存当前出现次数的最大值。  

**操作细节**  

- **push(val)**  
  1. `cnt[val] += 1` 得到新的频率 `f`。  
  2. 把 `val` 放进 `group[f]`（如果 `group[f]` 不存在就先创建一个空列表）。  
  3. 更新 `maxFreq = max(maxFreq, f)`。  

- **pop()**  
  1. 直接从 `group[maxFreq]` 的栈顶弹出元素 `x`（`pop()`），这就是“出现次数最多且最近压入”的元素。  
  2. `cnt[x] -= 1`，因为它被弹出了。  
  3. 如果弹出后 `group[maxFreq]` 为空，说明已经没有频率为 `maxFreq` 的元素了，`maxFreq -= 1`。  

这样每一次 `push`、`pop` 都只涉及 **常数次** 哈希表查找和列表的 `append / pop`，时间都是 `O(1)`。

> **类比**：  
> - 想象每一种出现次数 `f` 对应一条专门的“传送带”（`group[f]`），只要元素的出现次数升到 `f`，它就会跳上第 `f` 条传送带。最高频率的传送带最前面的元素，就是我们要弹出的目标。  

#### 代码（Python）

```python
from collections import defaultdict

class FreqStack:
    def __init__(self):
        # cnt[x] = x 当前的出现次数
        self.cnt = defaultdict(int)          # 哈希表：键是元素，值是出现次数
        # group[f] = 所有出现次数恰好为 f 的元素，按压入顺序保存（栈结构）
        self.group = defaultdict(list)       # 哈希表：键是频率，值是列表（栈）
        # 当前最大的频率
        self.maxFreq = 0

    # 把元素压入栈顶
    def push(self, val: int) -> None:
        # 1) 更新出现次数
        self.cnt[val] += 1
        f = self.cnt[val]                     # 新的频率

        # 2) 把元素放进对应频率的栈
        self.group[f].append(val)             # 列表的末尾当作栈顶

        # 3) 更新全局最大频率
        if f > self.maxFreq:
            self.maxFreq = f

    # 弹出出现频率最高且最近压入的元素
    def pop(self) -> int:
        # 1) 从最高频率的栈顶拿元素
        val = self.group[self.maxFreq].pop()  # 直接弹出

        # 2) 该元素的出现次数减一
        self.cnt[val] -= 1

        # 3) 如果最高频率的栈空了，最大频率要向下调
        if not self.group[self.maxFreq]:
            self.maxFreq -= 1

        return val
```

#### 复杂度  

- **时间复杂度**：`O(1)`（常数时间）  
  - `push`：只做哈希表查/改和列表 `append`，都是常数操作。  
  - `pop`：直接定位到 `group[maxFreq]` 的栈顶弹出，同样是常数操作。  
  - 与暴力解相比，省掉了遍历整个栈的 `O(n)` 开销。  

- **空间复杂度**：`O(n)`  
  - `cnt`、`group` 中总共存放的元素数等于所有压入的元素数 `n`（每个元素会在某个频率的栈里出现一次），所以空间随输入规模线性增长。  

---

## 心得  

- **核心技巧**：把「出现次数」抽象成「层级」（频率），对每个层级维护一个独立的栈，从而在 `O(1)` 时间内定位最高频率且最近的元素。  
- **适用场景**：  
  1. **频率栈 / 频率队列**（如本题）。  
  2. **LFU 缓存**（Least Frequently Used），需要快速获取最少使用的元素。  
  3. **统计出现次数后快速查询最高/最低频元素** 的变体题目。  
- **一句话总结**：  
  “把相同频率的元素聚在一起，用栈保存它们的压入顺序，最高频率的栈顶就是答案。”

---

## 反思  

- **第一反应**：直接用普通栈保存元素，`pop` 时遍历统计频率。  
- **最容易踩的坑**：  
  - 忘记在 `pop` 后把对应频率的栈空了要把 `maxFreq` 减一，导致后续 `pop` 仍然访问空栈。  
  - 频率提升时忘记在 `group[f]` 不存在时先创建列表，会抛出 `KeyError`。  
  - 题目保证 `pop` 前一定有元素，但实现时仍需防止误操作导致空结构访问。  
- **下次第一步**：  
  “出现次数最多的元素” 这类需求，先想 **‘把次数映射为层级’，每层维护一个结构（栈/队列）’，而不是每次遍历全部”。这样可以迅速定位到目标，避免线性扫描。