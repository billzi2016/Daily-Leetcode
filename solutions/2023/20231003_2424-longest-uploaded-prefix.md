# #2424. 最长已上传前缀 / Longest Uploaded Prefix

> 难度：中等 · 标签：Hash Table、Binary Search、Union Find、Design、Binary Indexed Tree、Segment Tree、Heap (Priority Queue)、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/longest-uploaded-prefix/)

---

## 题目（英文原版）

**Description**

You are given a stream of n videos, each represented by a distinct number from 1 to n that you need to "upload" to a server. You need to implement a data structure that calculates the length of the longest uploaded prefix at various points in the upload process.
We consider i to be an uploaded prefix if all videos in the range 1 to i (inclusive) have been uploaded to the server. The longest uploaded prefix is the maximum value of i that satisfies this definition.

Implement the LUPrefix class:

**Examples**

**Example 1:**

```
Input
["LUPrefix", "upload", "longest", "upload", "longest", "upload", "longest"]
[[4], [3], [], [1], [], [2], []]
Output
[null, null, 0, null, 1, null, 3]

Explanation
LUPrefix server = new LUPrefix(4);   // Initialize a stream of 4 videos.
server.upload(3);                    // Upload video 3.
server.longest();                    // Since video 1 has not been uploaded yet, there is no prefix.
                                     // So, we return 0.
server.upload(1);                    // Upload video 1.
server.longest();                    // The prefix [1] is the longest uploaded prefix, so we return 1.
server.upload(2);                    // Upload video 2.
server.longest();                    // The prefix [1,2,3] is the longest uploaded prefix, so we return 3.
```

**Constraints**

- 1 <= n <= 105
- 1 <= video <= n
- All values of video are distinct.
- At most 2 * 105 calls in total will be made to upload and longest.
- At least one call will be made to longest.

---

## 题目（中文翻译）

你得到一个包含 **n** 部视频的流（stream），每部视频用 1 到 **n** 的唯一编号表示，需要将其“上传”（upload）到服务器。请实现一种数据结构，用于在上传过程的不同时间点计算**最长已上传前缀**的长度。

我们把 **i** 称为已上传前缀（uploaded prefix），如果编号范围 \[1, i\]（含 i）内的所有视频都已经上传到服务器。**最长已上传前缀**即满足该定义的最大 **i**。

实现 `LUPrefix` 类：

```text
LUPrefix(int n)          // 初始化一个包含 n 部视频的流
void upload(int video)   // 将编号为 video 的视频上传
int longest()            // 返回当前最长已上传前缀的长度
```

---

**示例 1**

```text
输入
["LUPrefix", "upload", "longest", "upload", "longest", "upload", "longest"]
[[4], [3], [], [1], [], [2], []]

输出
[null, null, 0, null, 1, null, 3]

解释
LUPrefix server = new LUPrefix(4);   // 初始化一个包含 4 部视频的流。
server.upload(3);                    // 上传视频 3。
server.longest();                    // 由于视频 1 尚未上传，当前没有前缀，返回 0。

...（已截断）
```

---

**约束条件**

- 1 ≤ n ≤ 10⁵
- 1 ≤ video ≤ n
- 所有 video 的取值互不相同。
- `upload` 与 `longest` 的调用总次数不超过 2 × 10⁵。
- 至少会调用一次 `longest`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**每次查询 `longest()` 时，从 1 开始逐个检查视频是否已经上传**，一旦遇到第一个没有上传的视频，就停下来，返回前面已经全部上传的数量。

- **用到的数据结构**：一个长度为 `n+1` 的布尔数组 `uploaded`（下标代表视频编号），`uploaded[i] = True` 表示视频 `i` 已经上传。可以把它想象成一本“是否已上架”的清单，像是一本字典的目录，里面每一项只记录“有/没有”两种状态。
- **为什么正确**：因为我们逐个检查，从最小编号开始，只要发现缺口，就说明前面的全部都是连续的上传了，这正是题目对“前缀”的定义。
- **复杂度分析**：  
  - `upload(video)` 只需要把对应位置设为 `True`，是 **O(1)**。  
  - `longest()` 需要从 1 扫描到可能的 `n`，最坏情况要检查 `n` 次，**O(n)**。  
  - 如果每次都调用 `longest()`，总时间会是 **O(n·queries)**，在最坏的 2·10⁵ 次调用下会超时。  

> **大白话解释**：  
> - `O(1)` 就像“一下子搞定”，不管数组多大，都只做一次操作。  
> - `O(n)` 就像“从头到尾数一遍”，如果 n=10000，真的要走 10000 步。

#### 代码（Python）

```python
class LUPrefix:
    def __init__(self, n: int):
        # uploaded[i] 表示视频 i 是否已上传，索引从 1 开始，0 位置不使用
        self.uploaded = [False] * (n + 1)
        self.n = n

    def upload(self, video: int) -> None:
        # 把对应位置标记为已上传
        self.uploaded[video] = True

    def longest(self) -> int:
        # 从 1 开始逐个检查，遇到未上传的立即返回前面的长度
        length = 0
        while length + 1 <= self.n and self.uploaded[length + 1]:
            length += 1
        return length
```

#### 复杂度

- **时间复杂度**  
  - `upload`：`O(1)` —— 只改动一个数组元素。  
  - `longest`：`O(n)` —— 最坏需要遍历整个数组。  
- **空间复杂度**  
  - `O(n)` —— 需要一个长度为 `n+1` 的布尔数组来记录每个视频的状态。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次 `longest()` 都要从头遍历**。  
观察到：当我们上传一个新视频时，只会让 “已上传的最长前缀” 向右移动，而移动的次数**总共不超过 n 次**（每个视频最多让指针前进一次）。  

**关键想法**：维护一个全局指针 `cur`，始终指向当前已确认的最长前缀长度。  
- 当上传视频 `x` 时，把 `uploaded[x]` 设为 `True`。  
- 然后检查 `cur + 1` 位置是否已经上传，如果是，就把 `cur` 向右移动一位。不断循环，直到 `cur + 1` 位置未上传为止。  

这样，`longest()` 只需要返回 `cur`，**不再需要遍历**。  
每个视频只会让 `cur` 前进一次，整个过程的总时间是 `O(n)`，摊销到每次操作上就是 **O(1)**。

> **类比**：把 `cur` 看成“一把尺子”，尺子左端固定在 0，右端随已上传的视频不断伸展。每次有新视频恰好在尺子右端的下一个位置出现时，尺子就向右伸长一格；否则尺子保持不动。这样我们随时都知道尺子到底伸到了哪儿——也就是最长前缀的长度。

#### 代码（Python）

```python
class LUPrefix:
    def __init__(self, n: int):
        # 记录每个视频是否已上传，索引从 1 开始
        self.uploaded = [False] * (n + 1)
        self.n = n
        # cur 表示当前已确认的最长上传前缀长度
        self.cur = 0

    def upload(self, video: int) -> None:
        # 标记该视频已上传
        self.uploaded[video] = True
        # 尝试向右推进 cur，只要下一个位置已经上传就继续
        while self.cur + 1 <= self.n and self.uploaded[self.cur + 1]:
            self.cur += 1   # 前缀长度增加 1

    def longest(self) -> int:
        # 直接返回当前的前缀长度
        return self.cur
```

#### 复杂度

- **时间复杂度**  
  - `upload`：摊销 `O(1)`。虽然内部有 `while` 循环，但每个视频只会让 `cur` 前进一次，所有循环累计最多执行 `n` 次。  
  - `longest`：`O(1)`，直接返回 `cur`。  
  - 与暴力解相比，`longest` 从 `O(n)` 降到了 `O(1)`，整体从可能的 `O(n·queries)` 降到 `O(n + queries)`，在 2·10⁵ 次调用下轻松通过。

- **空间复杂度**  
  - `O(n)`，同样需要一个布尔数组记录上传状态。  

---

## 心得

- **核心技巧**：**利用全局指针（或“前缀指针”）进行增量维护**，把原本每次查询都要重新遍历的工作，转化为在上传时少量的局部更新。  
- **适用的题型**  
  1. “最长连续子序列”类问题，如 “连续的天数”/“连续的字符”。  
  2. “动态前缀/后缀查询”类，如 “数据流中的中位数” (用两个堆维护) 的思路相似——都在插入时维护答案。  
  3. “在线判定”类，如 “检测是否所有房间都已打开” (Union Find 也可以实现)。  
- **一句话总结**：**把查询的成本前移到插入时，只让每个元素“推动”答案一次**。

## 反思

- **第一反应**：直接用数组记录上传情况，然后每次遍历找前缀——最直观但不够高效。  
- **最容易踩的坑**  
  - 忘记把数组下标从 1 开始对齐，导致 `uploaded[0]` 被错误使用。  
  - 在 `upload` 中没有循环推进 `cur`，只检查一次，会导致前缀卡在错误位置。  
  - 边界条件：`n = 1` 时仍需保证 `while` 循环不会越界。  
- **下次遇到同类题**：第一步想到 **“是否可以在插入时维护一个指针/计数，让查询只返回这个计数？”**，如果可以，就几乎可以做到 O(1) 的查询。