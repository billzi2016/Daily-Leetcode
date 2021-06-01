# #1348. **推文计数按频率** / Tweet Counts Per Frequency

> 难度：中等 · 标签：Hash Table、Binary Search、Design、Sorting、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/tweet-counts-per-frequency/)

---

## 题目（英文原版）

**Description**

A social media company is trying to monitor activity on their site by analyzing the number of tweets that occur in select periods of time. These periods can be partitioned into smaller time chunks based on a certain frequency (every minute, hour, or day).
For example, the period [10, 10000] (in seconds) would be partitioned into the following time chunks with these frequencies:
Notice that the last chunk may be shorter than the specified frequency's chunk size and will always end with the end time of the period (10000 in the above example).
Design and implement an API to help the company with their analysis.
Implement the TweetCounts class:
Example:

**Examples**

**Example 1:**

```
Input
["TweetCounts","recordTweet","recordTweet","recordTweet","getTweetCountsPerFrequency","getTweetCountsPerFrequency","recordTweet","getTweetCountsPerFrequency"]
[[],["tweet3",0],["tweet3",60],["tweet3",10],["minute","tweet3",0,59],["minute","tweet3",0,60],["tweet3",120],["hour","tweet3",0,210]]

Output
[null,null,null,null,[2],[2,1],null,[4]]

Explanation
TweetCounts tweetCounts = new TweetCounts();
tweetCounts.recordTweet("tweet3", 0);                              // New tweet "tweet3" at time 0
tweetCounts.recordTweet("tweet3", 60);                             // New tweet "tweet3" at time 60
tweetCounts.recordTweet("tweet3", 10);                             // New tweet "tweet3" at time 10
tweetCounts.getTweetCountsPerFrequency("minute", "tweet3", 0, 59); // return [2]; chunk [0,59] had 2 tweets
tweetCounts.getTweetCountsPerFrequency("minute", "tweet3", 0, 60); // return [2,1]; chunk [0,59] had 2 tweets, chunk [60,60] had 1 tweet
tweetCounts.recordTweet("tweet3", 120);                            // New tweet "tweet3" at time 120
tweetCounts.getTweetCountsPerFrequency("hour", "tweet3", 0, 210);  // return [4]; chunk [0,210] had 4 tweets
```

**Constraints**

- 0 <= time, startTime, endTime <= 109
- 0 <= endTime - startTime <= 104
- There will be at most 104 calls in total to recordTweet and getTweetCountsPerFrequency.

---

## 题目（中文翻译）

描述  
一家社交媒体公司希望通过统计在选定时间段内出现的推文数量来监控站点活跃度。这些时间段可以按照一定的频率（每分钟、每小时或每天）进一步划分为更小的时间块。  

例如，时间段 **[10, 10000]**（单位：秒）在不同频率下的划分如下：

| 频率 | 时间块（以秒为单位） |
|------|--------------------|
| minute（每分钟） | [10, 69], [70, 129], … , [9970, 10000] |
| hour（每小时）   | [10, 3610], [3611, 7210], … , [9970, 10000] |
| day（每天）      | [10, 10000]（因为结束时间 10000 小于一个完整的“天”块） |

注意，最后一个块的长度可能小于指定频率对应的块大小，但它一定以给定时间段的结束时间为结束点（如上例中的 10000）。

请设计并实现一个 API，帮助公司完成上述分析。

实现 `TweetCounts` 类，支持以下方法：

- `recordTweet(string tweetName, int time)`  
  记录一条名称为 `tweetName`、时间点为 `time`（秒）的推文。

- `getTweetCountsPerFrequency(string freq, string tweetName, int startTime, int endTime)`  
  返回在闭区间 **[startTime, endTime]** 内，按照频率 `freq`（取值为 `"minute"`、`"hour"`、`"day"`）划分的每个时间块中 `tweetName` 出现的次数。返回值为一个整数数组，数组第 `i` 项对应第 `i` 个时间块的计数。  

示例  

```json
Input
["TweetCounts","recordTweet","recordTweet","recordTweet","getTweetCountsPerFrequency","getTweetCountsPerFrequency","recordTweet","getTweetCountsPerFrequency"]
[[],["tweet3",0],["tweet3",60],["tweet3",10],["minute","tweet3",0,59],["minute","tweet3",0,60],["tweet3",120],["hour","tweet3",0,210]]

Output
[null,null,null,null,[2],[2,1],null,[4]]
```

解释  
```java
TweetCounts tweetCounts = new TweetCounts();
tweetCounts.recordTweet("tweet3", 0);   // 在时间 0 记录一条 tweet3
tweetCounts.recordTweet("tweet3", 60);  // 在时间 60 记录一条 tweet3
tweetCounts.recordTweet("tweet3", 10);  // 在时间 10 记录一条 tweet3

// 查询频率为 minute，时间区间 [0, 59] 的计数
// 该区间被划分为一个块 [0, 59]，其中 tweet3 出现了 2 次（时间 0 和 10）
tweetCounts.getTweetCountsPerFrequency("minute", "tweet3", 0, 59); // 返回 [2]

// 查询频率为 minute，时间区间 [0, 60] 的计数
// 区间被划分为两个块 [0, 59] 和 [60, 60]，分别计数为 2 和 1
tweetCounts.getTweetCountsPerFrequency("minute", "tweet3", 0, 60); // 返回 [2, 1]

tweetCounts.recordTweet("tweet3", 120); // 在时间 120 记录一条 tweet3

// 查询频率为 hour，时间区间 [0, 210] 的计数
// 区间被划分为一个块 [0, 210]，其中 tweet3 出现了 4 次（0、10、60、120）
tweetCounts.getTweetCountsPerFrequency("hour", "tweet3", 0, 210); // 返回 [4]
```

约束条件  

- `0 <= time, startTime, endTime <= 10^9`  
- `0 <= endTime - startTime <= 10^4`  
- `recordTweet` 与 `getTweetCountsPerFrequency` 的调用总次数不超过 `10^4`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把每条推文的所有时间点全部保存下来，查询时把 **所有** 时间遍历一遍，看看它们落在了哪个时间块（minute / hour / day）里，就把对应的计数加 1。  

- **数据结构**：用一个 `dict`（哈希表）把推文的名字映射到它出现的时间列表。  
  - 哈希表可以类比成 **查字典**：键（key）是推文名称，值（value）是这条推文所有出现的时间。查一次字典的时间几乎是 **O(1)**，所以找对应的时间列表很快。  
- **为什么正确**：我们把所有时间都列出来了，遍历时只要判断 `startTime ≤ time ≤ endTime`，再看它属于哪一个块，就一定能得到每个块的真实计数。  

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

class TweetCounts:
    def __init__(self):
        # tweet_name -> 所有出现时间的列表（未排序也可以）
        self.tweets = defaultdict(list)

    # 记录一条推文
    def recordTweet(self, tweetName: str, time: int) -> None:
        self.tweets[tweetName].append(time)   # 把时间直接放进列表

    # 查询指定频率、指定时间区间的计数
    def getTweetCountsPerFrequency(self,
                                   freq: str,
                                   tweetName: str,
                                   startTime: int,
                                   endTime: int) -> List[int]:
        # 1️⃣ 把频率转换成块的长度（秒）
        interval = {"minute": 60, "hour": 3600, "day": 86400}[freq]

        # 2️⃣ 计算需要多少块
        #   例如 start=0, end=119, interval=60 → 需要 2 块 (0~59, 60~119)
        bucket_cnt = (endTime - startTime) // interval + 1
        ans = [0] * bucket_cnt               # 用来存每块的计数

        # 3️⃣ 暴力遍历所有时间，判断它属于哪一块
        for t in self.tweets[tweetName]:
            if startTime <= t <= endTime:    # 只关心区间内的时间
                idx = (t - startTime) // interval   # 计算它落在第几块
                ans[idx] += 1               # 计数加一

        return ans
```

#### 复杂度  

- **时间复杂度**：`O(N)`，其中 `N` 是该推文所有出现的次数。我们必须把所有时间都检查一遍。  
  - “O(N)” 的含义可以理解为：如果有 1000 条记录，遍历一次大约要花 1000 步；如果记录翻倍到 2000 条，步数也会翻倍。  
- **空间复杂度**：`O(N)`，用于保存每条推文的所有时间点。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **每次查询都要遍历全部时间**，即使我们只关心 `startTime` 与 `endTime` 之间的那一小段。  
我们可以把时间列表 **排序**，然后利用二分查找快速定位出区间 `[startTime, endTime]` 内的子数组，这样只遍历真正相关的时间。  

关键点：

1. **把时间列表保持有序**  
   - 插入时使用 `bisect.insort`（二分插入）或者在查询前先排序。这里选择在查询时**一次性排序**，因为总调用次数 ≤ 10⁴，排序开销仍然可接受且实现更简洁。  
2. **二分定位区间**  
   - Python 标准库 `bisect` 提供 `bisect_left` 与 `bisect_right`，可以在 **O(log N)** 时间内找到第一个 ≥ `startTime` 的位置和第一个 > `endTime` 的位置。这样我们只拿到真正需要处理的子数组。  
3. **按块计数**  
   - 对子数组中的每个时间 `t`，直接算它落在第几块：`idx = (t - startTime) // interval`，计数数组 `ans[idx]` 加一。  
   - 这一步仍然是线性遍历子数组，但子数组的长度是实际相关的记录数，通常远小于全部记录数。  

整体思路可以类比为 **在一本排好序的电话簿里查找**：先用二分快速定位到姓氏范围，再逐个统计。  

#### 代码（Python）

```python
import bisect
from collections import defaultdict
from typing import List

class TweetCounts:
    def __init__(self):
        # tweet_name -> 所有出现时间的列表（保持有序）
        self.tweets = defaultdict(list)

    # 记录推文：直接加入列表，查询前统一排序
    def recordTweet(self, tweetName: str, time: int) -> None:
        self.tweets[tweetName].append(time)

    # 查询计数
    def getTweetCountsPerFrequency(self,
                                   freq: str,
                                   tweetName: str,
                                   startTime: int,
                                   endTime: int) -> List[int]:
        # 1️⃣ 频率对应的块大小（秒）
        interval = {"minute": 60, "hour": 3600, "day": 86400}[freq]

        # 2️⃣ 需要的块数
        bucket_cnt = (endTime - startTime) // interval + 1
        ans = [0] * bucket_cnt

        # 3️⃣ 先把时间列表排好序（只排一次，以后会直接使用已排好的列表）
        times = self.tweets[tweetName]
        times.sort()                     # O(N log N) 只在第一次查询时花费

        # 4️⃣ 二分找出[startTime, endTime]所在的子区间
        left = bisect.bisect_left(times, startTime)   # 第一个 >= startTime 的位置
        right = bisect.bisect_right(times, endTime)   # 第一个 > endTime 的位置

        # 5️⃣ 只遍历区间内的时间，按块计数
        for t in times[left:right]:
            idx = (t - startTime) // interval
            ans[idx] += 1

        return ans
```

> **小技巧**：如果担心 `sort()` 每次都重复执行，可以在 `recordTweet` 时使用 `bisect.insort` 把时间直接插入到有序位置，这样列表始终保持有序，查询时就不需要再排序。实现上只需要把 `recordTweet` 改成：
> ```python
> bisect.insort(self.tweets[tweetName], time)
> ```
> 时间复杂度仍然保持在 `O(log N)` 插入。

#### 复杂度  

- **时间复杂度**  
  - 第一次查询同一条推文时，需要对全部时间做一次排序：`O(N log N)`（`N` 为该推文出现次数）。  
  - 之后的每次查询：二分定位 `O(log N)` + 只遍历区间内的 `M` 条记录，整体为 `O(log N + M)`。  
  - 与暴力解的 `O(N)` 相比，**当区间很小或查询次数很多时**，这会快很多。  
- **空间复杂度**：仍然是 `O(N)`，用于存放所有时间点。额外的 `ans` 数组大小与块数成正比，块数最多是 `(endTime-startTime)/interval + 1 ≤ 10⁴/60 ≈ 167`，可以忽略不计。

---

## 心得  

- **核心技巧**：**排序 + 二分**（先把数据排好序，再用二分快速定位查询区间）。  
- **适用的题型**  
  1. “区间计数” 类题目，如 LeetCode 307. 区间查询（Range Sum Query）  
  2. “时间戳统计” 类题目，如 LeetCode 1156. 单词频率的统计（需要快速定位区间）  
  3. “动态区间查询” 类题目，如 LeetCode 2406. 设计一个搜索系统（需要对已排序的数据进行区间统计）  
- **一句话总结**：**把数据排好序，再用二分锁定区间，只遍历真正需要的那部分**。  

---

## 反思  

- **第一反应**：直接把所有时间遍历一遍，写一个最朴素的计数循环。  
- **最容易踩的坑**  
  - **边界条件**：`endTime` 包含在区间内，需要使用 `bisect_right`（> endTime）而不是 `bisect_left`。  
  - **块数计算**：`(endTime - startTime) // interval + 1`，忘记加 1 会导致最后一个块缺失。  
  - **时间顺序**：如果不排序直接二分，会得到错误结果。  
- **下次遇到同类题**：第一步先思考 **“能否先把数据有序？”**，如果可以，就立刻引入 **二分查找** 来缩小搜索范围。