# #1656. 设计有序流 / Design an Ordered Stream

> 难度：简单 · 标签：Array、Hash Table、Design、Data Stream · [LeetCode 链接](https://leetcode.com/problems/design-an-ordered-stream/)

---

## 题目（英文原版）

**Description**

There is a stream of n (idKey, value) pairs arriving in an arbitrary order, where idKey is an integer between 1 and n and value is a string. No two pairs have the same id.
Design a stream that returns the values in increasing order of their IDs by returning a chunk (list) of values after each insertion. The concatenation of all the chunks should result in a list of the sorted values.
Implement the OrderedStream class:
Example:

**Examples**

**Example 1:**

```
Input
["OrderedStream", "insert", "insert", "insert", "insert", "insert"]
[[5], [3, "ccccc"], [1, "aaaaa"], [2, "bbbbb"], [5, "eeeee"], [4, "ddddd"]]
Output
[null, [], ["aaaaa"], ["bbbbb", "ccccc"], [], ["ddddd", "eeeee"]]

Explanation
// Note that the values ordered by ID is ["aaaaa", "bbbbb", "ccccc", "ddddd", "eeeee"].
OrderedStream os = new OrderedStream(5);
os.insert(3, "ccccc"); // Inserts (3, "ccccc"), returns [].
os.insert(1, "aaaaa"); // Inserts (1, "aaaaa"), returns ["aaaaa"].
os.insert(2, "bbbbb"); // Inserts (2, "bbbbb"), returns ["bbbbb", "ccccc"].
os.insert(5, "eeeee"); // Inserts (5, "eeeee"), returns [].
os.insert(4, "ddddd"); // Inserts (4, "ddddd"), returns ["ddddd", "eeeee"].
// Concatentating all the chunks returned:
// [] + ["aaaaa"] + ["bbbbb", "ccccc"] + [] + ["ddddd", "eeeee"] = ["aaaaa", "bbbbb", "ccccc", "ddddd", "eeeee"]
// The resulting order is the same as the order above.
```

**Constraints**

- 1 <= n <= 1000
- 1 <= id <= n
- value.length == 5
- value consists only of lowercase letters.
- Each call to insert will have a unique id.
- Exactly n calls will be made to insert.

---

## 题目（中文翻译）

有一个长度为 `n` 的流，其中包含若干 `(idKey, value)` 键值对，这些键值对以任意顺序到达。`idKey` 是取值在 `[1, n]` 区间的整数，`value` 是字符串。不存在两个键值对拥有相同的 `id`。  

设计一个能够在每次插入后返回一个 **块（list）**，该块中的值按照 `id` 的递增顺序排列。所有块按顺序拼接后应得到完整的已排序值列表。

实现 `OrderedStream` 类，使其能够完成上述功能。

---

## 示例

```text
示例 1:
Input
["OrderedStream", "insert", "insert", "insert", "insert", "insert"]
[[5], [3, "ccccc"], [1, "aaaaa"], [2, "bbbbb"], [5, "eeeee"], [4, "ddddd"]]
Output
[null, [], ["aaaaa"], ["bbbbb", "ccccc"], [], ["ddddd", "eeeee"]]
```

**解释**  
// 按 `id` 排序后的值序列为 `["aaaaa", "bbbbb", "ccccc", "ddddd", "eeeee"]`。  
```java
OrderedStream os = new OrderedStream(5);
os.insert(3, "ccccc"); // 插入 (3, "ccccc")，当前没有连续的最小 id，返回空列表 []
os.insert(1, "aaaaa"); // 插入 (1, "aaaaa")，此时可以返回从 id=1 开始的连续块 ["aaaaa"]
os.insert(2, "bbbbb"); // 插入 (2, "bbbbb")，继续返回连续块 ["bbbbb", "ccccc"]
os.insert(5, "eeeee"); // 插入 (5, "eeeee")，仍未形成新的连续块，返回 []
os.insert(4, "ddddd"); // 插入 (4, "ddddd")，现在可以返回剩余的连续块 ["ddddd", "eeeee"]
```

---

## 约束条件

- `1 <= n <= 1000`
- `1 <= id <= n`
- `value.length == 5`
- `value` 仅由小写字母组成
- 每次调用 `insert` 时提供的 `id` 均唯一
- 恰好会调用 `insert` `n` 次  

---

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有已经到达的 (id, value) 放进一个字典**（可以把字典想象成“查字典”，key 是单词（这里是 id），value 是对应的页码（这里是字符串）），每次插入后：

1. 把这对 `(id, value)` 存进字典。  
2. 再遍历 **1 … n**（从最小的 id 开始），把已经出现且 **连续** 的 value 按顺序取出来组成本次返回的列表。

> 为什么这样能得到正确答案？  
> 因为题目要求「每次插入后，返回从当前最小未输出的 id 开始，所有已经出现的连续 id 对应的 value」。遍历 1 … n 正好可以检查哪些 id 已经出现，并且只要遇到第一个未出现的 id，就可以停止——这正是题目要的“连续块”。

#### 代码（Python）

```python
class OrderedStream:
    def __init__(self, n: int):
        # 用字典保存已经到达的 (id, value)
        # key = id，value = 对应的字符串
        self.n = n
        self.store = {}          # 哈希表：查询 O(1)
        self.ptr = 1             # 下一个应该输出的 id

    def insert(self, idKey: int, value: str):
        # 1. 把新来的数据放进哈希表
        self.store[idKey] = value

        # 2. 从 ptr 开始检查是否可以输出
        res = []
        # 这里用 while 而不是 for，遇到第一个缺失的 id 就停
        while self.ptr <= self.n and self.ptr in self.store:
            res.append(self.store[self.ptr])   # 把对应的字符串加入返回列表
            self.ptr += 1                      # ptr 前进一步，准备检查下一个 id
        return res
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  最坏情况下（比如每次只插入一个 id，且它恰好是当前最小未输出的 id），我们需要遍历 `1 … n` 才能确认没有更多连续的元素可以输出，所以每次 `insert` 最差是 `O(n)`。  
  用大白话说，就是“如果你每次都要把所有 1000 本书的目录都翻一遍”，时间会随书的数量线性增长。

- **空间复杂度**：`O(n)`  
  需要额外的哈希表保存最多 `n` 条 `(id, value)`，所以空间随 `n` 成正比。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于每次遍历 `1 … n`**，尤其是当已经有很多元素被存入但尚未输出时，重复检查会浪费大量时间。我们可以把“已经出现的元素”直接放在一个**固定大小的数组**里，索引就是 id，这样：

1. **数组**（下标从 1 开始）存放对应 id 的 value。数组就像一本“编号顺序的书架”，第 i 本书（`arr[i]`）要么是空的，要么已经放好了对应的字符串。  
2. 维护一个指针 `ptr`，表示**下一个应该输出的 id**。  
3. 插入时，只把 `value` 放进 `arr[id]`。随后**循环检查 `ptr`**：只要 `arr[ptr]` 已经有值，就把它加入本次返回列表并把 `ptr` 往后推一位。循环结束的那一刻，`ptr` 正好指向第一个尚未出现的 id。

这样每个 id 只会被检查 **一次**（第一次出现时可能被输出，也可能等到后面才输出），整个过程的总检查次数恰好是 `n`，所以摊销下来每次 `insert` 的时间是 **O(1)**。

#### 代码（Python）

```python
class OrderedStream:
    def __init__(self, n: int):
        # 用列表保存所有位置，列表下标就是 id（从 1 开始）
        self.arr = [None] * (n + 1)   # 0 位置不使用，方便下标对应
        self.ptr = 1                  # 下一个应该输出的 id
        self.n = n

    def insert(self, idKey: int, value: str):
        # 把 value 放进对应的位置
        self.arr[idKey] = value

        # 收集从 ptr 开始的连续已出现的值
        res = []
        while self.ptr <= self.n and self.arr[self.ptr] is not None:
            res.append(self.arr[self.ptr])   # 把该位置的字符串加入结果
            self.ptr += 1                    # ptr 前进一步
        return res
```

#### 复杂度

- **时间复杂度**：`O(1)`（摊销）  
  每次 `insert` 只做常数次操作：一次数组写入 + 若干次指针移动。指针 `ptr` 只会向右走，最多走 `n` 步，所以 **所有 `n` 次插入的总时间是 O(n)**，平均下来每次是 O(1)。  
  用通俗的话说，就是“每本书只检查一次，不会重复翻同一本书的目录”。

- **空间复杂度**：`O(n)`  
  需要一个大小为 `n+1` 的数组来存放所有可能的字符串，空间随 `n` 线性增长。  

---

## 心得

- **核心技巧**：利用**指针 + 固定下标数组**实现一次遍历完成连续块的输出，避免每次都遍历全部元素。  
- **适用场景**：  
  1. **有序输出**需求且元素的下标范围已知（如 “设计有序流”）。  
  2. **连续子序列收集**问题（如 “Find the Smallest Missing Positive”）。  
  3. **一次遍历即可完成的流式处理**（如 “Design a Log Storage System” 的简化版）。  
- **一句话总结解题钥匙**：**“把位置固定下来，只让指针向前走”。**  

---

## 反思

- **第一反应**：看到“流”和“按 id 顺序返回”，立刻想到用**哈希表**记录已到达的元素，然后每次**遍历**找连续块。  
- **最容易踩的坑**：  
  - 忘记把指针 `ptr` **持久化**在对象内部，导致每次插入都从 1 开始检查，时间会回到 O(n²)。  
  - 边界条件：`ptr` 超过 `n` 时要停止循环，否则会出现数组越界。  
  - `value` 长度固定为 5 并不影响实现，但要确保返回的列表顺序与题目要求严格一致。  
- **下次类似题的第一步**：先判断“是否可以把下标/位置直接映射到数组”，如果可以，就用**数组 + 维护一个‘下一个待输出’的指针**，这样往往能把时间复杂度从线性遍历降到常数摊销。