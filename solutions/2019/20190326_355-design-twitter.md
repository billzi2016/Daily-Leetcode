# #355. 设计推特 / Design Twitter

> 难度：中等 · 标签：Hash Table、Linked List、Design、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/design-twitter/)

---

## 题目（英文原版）

**Description**

Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and is able to see the 10 most recent tweets in the user's news feed.
Implement the Twitter class:

**Examples**

**Example 1:**

```
Input
["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"]
[[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]]
Output
[null, null, [5], null, null, [6, 5], null, [5]]

Explanation
Twitter twitter = new Twitter();
twitter.postTweet(1, 5); // User 1 posts a new tweet (id = 5).
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 1 tweet id -> [5]. return [5]
twitter.follow(1, 2);    // User 1 follows user 2.
twitter.postTweet(2, 6); // User 2 posts a new tweet (id = 6).
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 2 tweet ids -> [6, 5]. Tweet id 6 should precede tweet id 5 because it is posted after tweet id 5.
twitter.unfollow(1, 2);  // User 1 unfollows user 2.
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 1 tweet id -> [5], since user 1 is no longer following user 2.
```

**Constraints**

- 1 <= userId, followerId, followeeId <= 500
- 0 <= tweetId <= 104
- All the tweets have unique IDs.
- At most 3 * 104 calls will be made to postTweet, getNewsFeed, follow, and unfollow.
- A user cannot follow himself.

---

## 题目（中文翻译）

设计一个简化版的 Twitter，使用户能够发布推文（tweet），关注/取关（follow/unfollow）其他用户，并能够在自己的信息流（news feed）中看到最近的 10 条推文。

实现 `Twitter` 类。

## 示例

### 示例 1

**输入**

```
["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"]
[[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]]
```

**输出**

```
[null, null, [5], null, null, [6, 5], null, [5]]
```

**解释**

```java
Twitter twitter = new Twitter();
twitter.postTweet(1, 5);   // 用户 1 发布了一条新推文（id = 5）。
twitter.getNewsFeed(1);   // 用户 1 的信息流应返回仅包含 1 条推文 id 的列表 -> [5]。
twitter.follow(1, 2);     // 用户 1 关注用户 2。
twitter.postTweet(2, 6);   // 用户 2 发布了一条新推文（id = 6）。
twitter.getNewsFeed(1);   // 用户 1 的信息流应返回包含 2 条推文 id 的列表 -> [6, 5]。因为推文 6 比推文 5 更晚发布，故排在前面。
twitter.unfollow(1, 2);   // 用户 1 取关用户 2。
twitter.getNewsFeed(1);   // 用户 1 的信息流应只返回 1 条推文 id -> [5]，因为用户 1 已不再关注用户 2。
```

## 约束条件

- `1 <= userId, followerId, followeeId <= 500`
- `0 <= tweetId <= 10^4`
- 所有推文的 ID 均唯一。
- 至多会有 `3 * 10^4` 次对 `postTweet`、`getNewsFeed`、`follow` 和 `unfollow` 的调用。
- 用户不能关注自己。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **存储用户的推文**  
   - 用一个 `defaultdict(list)` 把每个 `userId` 映射到该用户的所有推文。  
   - 每条推文可以记成 `(时间戳, tweetId)` 的二元组，时间戳只要递增的整数即可（相当于“这条推文在第几秒发的”），这样越大的时间戳代表越新。  
   - 类比：`list` 就像一本用户的“相册”，新拍的照片往后放。

2. **存储关注关系**  
   - 用 `defaultdict(set)` 把每个 `userId` 映射到他关注的所有 `followeeId`。  
   - `set` 类似于“字典里的词典”，我们只关心“是否在里面”，不需要顺序。  

3. **获取新闻推送（getNewsFeed）**  
   - 先把用户自己和他关注的所有人的推文全部取出来，放进一个大列表 `all_tweets`。  
   - 按时间戳从大到小排序（`sorted(..., reverse=True)`），取前 10 条的 `tweetId` 返回。  
   - 这一步就像把所有相册的照片全部倒出来，按拍摄时间排好序，再挑出最近的十张。

4. **为什么正确**  
   - 我们把**所有**可能出现在新闻流里的推文都收集到了，并且用时间戳保证了“最新的在前”。取前 10 条自然就是答案。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

class Twitter:
    def __init__(self):
        # 每个用户的所有推文，列表里存 (时间戳, tweetId)
        self.tweets = defaultdict(list)
        # 用户关注的集合，key 为 follower，value 为 set of followees
        self.followees = defaultdict(set)
        # 全局递增的时间戳，模拟“发帖的先后顺序”
        self.timestamp = 0

    # 用户 userId 发一条 tweetId 的推文
    def postTweet(self, userId: int, tweetId: int) -> None:
        self.timestamp += 1                      # 时间戳+1
        self.tweets[userId].append((self.timestamp, tweetId))
        # 为了统一，默认用户自己也算关注自己（后面会用到）
        self.followees[userId].add(userId)

    # 返回用户 userId 的新闻推送（最近的 10 条推文 id）
    def getNewsFeed(self, userId: int) -> List[int]:
        candidates = []                         # 用来收集所有候选推文
        # 把自己以及关注的人的推文全部拿出来
        for followee in self.followees[userId]:
            candidates.extend(self.tweets[followee])
        # 按时间戳降序排列，最近的在前
        candidates.sort(key=lambda x: x[0], reverse=True)
        # 只取前 10 条的 tweetId
        return [tweetId for _, tweetId in candidates[:10]]

    # 用户 followerId 关注 followeeId
    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId == followeeId:            # 不能关注自己
            return
        self.followees[followerId].add(followeeId)

    # 用户 followerId 取关 followeeId
    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followerId == followeeId:            # 不能取关自己
            return
        self.followees[followerId].discard(followeeId)
```

#### 复杂度  

- **时间复杂度**  
  - `postTweet`：`O(1)`，只在列表尾部追加。  
  - `follow / unfollow`：`O(1)`，集合的增删都是常数时间。  
  - `getNewsFeed`：设用户关注了 `F` 个人（包括自己），每个人最多有 `T` 条推文，则需要遍历 `F·T` 条推文并排序，时间复杂度是 `O(F·T log(F·T))`。  
    - 大白话：如果你关注的人很多、每个人发了很多推文，这一步会变慢，因为要把所有的“相册”都倒出来排队。

- **空间复杂度**  
  - `tweets` 保存所有推文：`O(totalTweets)`。  
  - `followees` 保存所有关注关系：`O(totalFollows)`。  
  - 额外的 `candidates` 列表在 `getNewsFeed` 时最多和所有相关推文等大：`O(F·T)`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **`getNewsFeed`**：我们把所有可能的推文全部拿出来再排序。实际上，只需要 **最近的 10 条**，不必完整排序。可以用 **小根堆（最小堆）** 只保留当前看到的前 10 条最新推文。

优化步骤：

1. **仍然用相同的数据结构保存推文和关注关系**（`list` + `set`），因为它们本身已经是最简洁的。

2. **每条推文仍然带时间戳**，时间戳越大越新。

3. **获取新闻推送**  
   - 对于用户自己和所有关注的人，取出他们最近的 **几条** 推文（例如每人只取最近的 10 条），放入一个最小堆 `heap`。  
   - 堆里保存 `(时间戳, tweetId)`，堆的大小始终不超过 10。  
   - 当堆的大小超过 10 时，弹出时间戳最小的（也就是最旧的）元素，保证堆里始终是当前看到的「最新的 10 条」。  
   - 最后把堆弹出并倒序（因为堆弹出的是最旧的），得到从新到旧的 10 条推文。

4. **为什么只取每个人最近的 10 条就够**  
   - 新闻流最多只返回 10 条，若某个人的第 11 条已经比堆里最旧的 10 条更旧，那么它不可能进入最终答案。  
   - 因此每个人只需要看最近的 10 条即可，大幅减少遍历量。

5. **核心工具：堆（优先队列）**  
   - Python 的 `heapq` 实现最小堆。  
   - 类比：堆就像一个「只保留最贵的 10 件商品」的展示柜，新的商品进来，如果比最便宜的还贵，就把最便宜的踢出去。

#### 代码（Python）

```python
import heapq
from collections import defaultdict
from typing import List

class Twitter:
    def __init__(self):
        # 用户 -> 推文列表，存 (时间戳, tweetId)
        self.tweets = defaultdict(list)
        # 用户 -> 关注的用户集合
        self.followees = defaultdict(set)
        # 全局时间戳，递增保证唯一且可比较
        self.time = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.time += 1
        self.tweets[userId].append((self.time, tweetId))
        # 自动关注自己，后面取新闻时会统一处理
        self.followees[userId].add(userId)

    def getNewsFeed(self, userId: int) -> List[int]:
        heap = []   # 小根堆，最多保存 10 条最新推文
        for followee in self.followees[userId]:
            # 只看该用户最近的 10 条（列表是按时间递增追加的，倒着取）
            recent = self.tweets[followee][-10:]   # 取最后 10 条
            for ts, tid in recent:
                if len(heap) < 10:
                    heapq.heappush(heap, (ts, tid))   # 直接放进堆
                else:
                    # 堆顶是当前最旧的，若新推文更新则替换
                    if ts > heap[0][0]:
                        heapq.heapreplace(heap, (ts, tid))
        # 把堆里的元素按时间倒序取出（最新的在前）
        result = [tid for _, tid in sorted(heap, key=lambda x: x[0], reverse=True)]
        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId == followeeId:
            return
        self.followees[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followerId == followeeId:
            return
        self.followees[followerId].discard(followeeId)
```

#### 复杂度  

- **时间复杂度**  
  - `postTweet`、`follow`、`unfollow` 均为 `O(1)`。  
  - `getNewsFeed`：  
    - 对每个关注的人最多遍历 **10 条** 推文，设关注人数为 `F`（包括自己），则遍历最多 `10·F` 条。  
    - 每次向堆中插入或替换的代价是 `O(log 10)`，而 `log 10` 是常数（约等于 3.3），所以整体是 `O(F)`。  
    - 大白话：不管每个人发了多少推文，我们只看每个人最近的 10 条，操作堆的成本也很小，整体随关注人数线性增长。

- **空间复杂度**  
  - 额外的堆最多保存 10 条记录，`O(1)`（常数空间）。  
  - 其余存储（`tweets`、`followees`）仍然是 `O(totalTweets + totalFollows)`，与暴力解相同。

---

## 心得

- **核心技巧**：**利用最小堆维护固定大小的“前 K 大”集合**。  
- **适用的题型**  
  1. **找出 K 条最新/最大元素**（如 “Top K Frequent Words”、 “K Closest Points to Origin”）。  
  2. **流式数据的实时排名**（如 “Sliding Window Maximum”）。  
- **一句话总结解题钥匙**：只保留“可能进入答案的候选”，用堆把候选集合压缩到固定大小。

---

## 反思

- **第一反应**：把所有相关推文全部取出来再排序——最直接但容易超时。  
- **最容易踩的坑**  
  - **忘记让用户默认关注自己**，导致 `getNewsFeed` 里没有自己的推文。  
  - **在 `unfollow` 时误删自己**（题目禁止用户关注自己），需要做判断。  
  - **堆的大小控制不当**，如果不限制在 10 条，会失去优化意义。  
- **下次遇到同类题**：  
  1. **先判断返回结果的上限**（这里是 10 条），  
  2. **思考能否只遍历“上限”范围内的元素**（每人只看最近的 10 条），  
  3. **选用合适的数据结构（堆/单调队列）保持固定大小的最佳集合**。