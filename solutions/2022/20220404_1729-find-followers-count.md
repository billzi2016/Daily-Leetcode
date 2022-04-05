# #1729. 粉丝计数 / Find Followers Count

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-followers-count/)

---

## 题目（英文原版）

**Description**

Table: Followers
Write a solution that will, for each user, return the number of followers.
Return the result table ordered by user_id in ascending order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| user_id     | int  |
| follower_id | int  |
+-------------+------+
(user_id, follower_id) is the primary key (combination of columns with unique values) for this table.
This table contains the IDs of a user and a follower in a social media app where the follower follows the user.
```

**Example 2:**

```
Input: 
Followers table:
+---------+-------------+
| user_id | follower_id |
+---------+-------------+
| 0       | 1           |
| 1       | 0           |
| 2       | 0           |
| 2       | 1           |
+---------+-------------+
Output: 
+---------+----------------+
| user_id | followers_count|
+---------+----------------+
| 0       | 1              |
| 1       | 1              |
| 2       | 2              |
+---------+----------------+
Explanation: 
The followers of 0 are {1}
The followers of 1 are {0}
The followers of 2 are {0,1}
```

---

## 题目（中文翻译）

编写一个查询，统计每个用户的粉丝数量（followers count），并按 `user_id` 升序返回结果表。

**表结构**

```
Followers
+-------------+------+
| Column Name | Type |
+-------------+------+
| user_id     | int  |
| follower_id | int  |
+-------------+------+
```

`(user_id, follower_id)` 为主键（primary key），唯一标识表中的每一行。该表记录了社交媒体应用中用户及其粉丝的对应关系，即 `follower_id` 关注了 `user_id`。

**返回结果**

返回的结果表应包含两列：

- `user_id`：用户 ID  
- `followers_count`：该用户的粉丝数量

结果按 `user_id` 的升序排列。结果格式如下示例所示。

**示例**

输入表 `Followers`：

```
+---------+-------------+
| user_id | follower_id |
+---------+-------------+
| 0       | 1           |
| 1       | 0           |
| 2       | 0           |
| 2       | 1           |
+---------+-------------+
```

输出：

```
+---------+----------------+
| user_id | followers_count|
+---------+----------------+
| 0       | 1              |
| 1       | 1              |
| 2       | 2              |
```

（后续示例已截断）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们把 `Followers` 表想象成一本**“谁关注谁”的记录本**，每一行都是一条“**用户 A 被用户 B 关注**”的记录。  
最直接的想法是：

1. 先把所有出现过的 `user_id` 收集起来（因为要给每个用户返回关注人数）。
2. 对于每一个 `user_id`，再次遍历整张表，统计有多少行的 `user_id` 等于当前用户。  
   - 这里的遍历就像在一本电话簿里，**一次一次地去找**所有叫“张三”的条目，找多少就算多少。

这种做法不需要任何高级数据结构，只用 **列表**（存放所有记录）和 **集合**（去重得到所有用户）即可，完全符合“最笨”的直觉。

**为什么它一定能得到正确答案？**  
因为我们对每个用户都把整张表都检查了一遍，所有出现的 `(user_id, follower_id)` 都被计数了，漏掉的可能性为零。

**时间/空间复杂度大白话**  

- **时间复杂度**：外层遍历所有用户是 `U` 次，内层遍历整张表是 `N` 次，总共是 `U × N`。在最坏情况下，用户数几乎等于记录数 `N`，于是时间复杂度是 **O(N²)**。  
  用生活中的比喻：如果有 1000 本书要检查每本书里出现多少次某个词，暴力做法相当于把 1000 本书每一本都从头到尾读一遍，这会非常慢。

- **空间复杂度**：我们只用了几个额外的容器来保存用户集合和最终结果，大小与记录数线性相关，**O(N)**。  
  也就是说，额外占用的内存大概和原始数据差不多。

#### 代码（Python）

```python
# ------------------- 暴力解 -------------------
# 假设 followers 是一个列表，每个元素是 (user_id, follower_id) 的元组
# 例如：followers = [(0, 1), (1, 0), (2, 0), (2, 1)]

def followers_count_brute_force(followers):
    # 1. 收集所有出现过的 user_id
    users = {user for user, _ in followers}          # 用集合去重，类似“把所有用户名字挑出来”
    
    result = []                                        # 最终返回的列表，元素形如 (user_id, count)
    
    # 2. 对每个用户，遍历整张表计数
    for u in sorted(users):                           # 按照题目要求升序输出
        cnt = 0
        for user, _ in followers:                     # 逐行检查
            if user == u:                             # 如果这一行的 user_id 正好是当前的 u
                cnt += 1                              # 计数器加一
        result.append((u, cnt))                       # 把 (user_id, followers_count) 加入结果
    
    return result

# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    followers = [(0, 1), (1, 0), (2, 0), (2, 1)]
    print(followers_count_brute_force(followers))
    # 输出: [(0, 1), (1, 1), (2, 2)]
```

#### 复杂度

- **时间复杂度**：O(N²)  
  *解释*：如果表里有 10 万条记录，暴力解要进行 10 万 × 10 万 次比较，几乎不可接受。

- **空间复杂度**：O(N)  
  *解释*：我们额外保存了一个用户集合和结果列表，大小随记录数线性增长。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于“对每个用户都要遍历整张表”。  
如果我们在一次遍历表的过程中，就把每个 `user_id` 出现的次数记录下来，就不需要再二次扫描了。  

这正好可以用 **哈希表（Python 中的 dict）** 来实现：

- **哈希表** 可以想象成 **“查字典”**，字典的 **key** 就是 `user_id`，**value** 就是该用户已经累计的关注人数。  
- 当我们读取到一行 `(user_id, follower_id)` 时，只要把 `user_id` 对应的计数 `+1`，整个过程只需 **一次** 线性遍历。

**核心步骤**（零基础解释）  

1. **准备一个空字典** `cnt = {}`。  
2. **遍历每条记录** `(u, f)`：  
   - 如果 `u` 还没出现在字典里，先把 `cnt[u] = 0`（相当于在字典里“新建一个条目”）。  
   - 然后执行 `cnt[u] += 1`，把关注人数加一。  
3. **把字典转成结果列表**，并按 `user_id` 升序排序。  

这样只需要 **一次** 把所有记录扫完，时间就从 **O(N²)** 降到 **O(N)**，空间仍然是 **O(N)**（因为要存每个用户的计数）。

#### 代码（Python）

```python
# ------------------- 最优解（一次遍历 + 哈希表） -------------------
def followers_count_optimal(followers):
    """
    参数 followers: List[Tuple[int, int]]
        每个元组 (user_id, follower_id) 表示 follower_id 关注了 user_id
    返回值: List[Tuple[int, int]]
        每个元组 (user_id, followers_count)，按照 user_id 升序排列
    """
    # 1. 用 dict 统计每个 user_id 的关注人数
    cnt = {}                               # 空字典，相当于“空的电话簿”
    for user, _ in followers:              # 只关心被关注的 user_id，_ 代表 follower_id（这里不需要）
        if user not in cnt:                # 如果这个用户还没有条目，就先创建一个计数为 0
            cnt[user] = 0
        cnt[user] += 1                     # 计数器加一，记录一次关注

    # 2. 把统计结果转换成列表，并按照 user_id 升序排列
    result = [(user, cnt[user]) for user in sorted(cnt)]
    return result

# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    followers = [(0, 1), (1, 0), (2, 0), (2, 1)]
    print(followers_count_optimal(followers))
    # 输出: [(0, 1), (1, 1), (2, 2)]
```

#### 复杂度

- **时间复杂度**：O(N)  
  *解释*：我们只遍历一次表，N 条记录就完成全部计数。即使有 100 万条记录，也只需要 100 万次简单的“加一”操作，速度非常快。

- **空间复杂度**：O(U)（U 为不同的 user_id 数量，最坏情况下 U≈N）  
  *解释*：需要额外存储每个用户的计数，最多和记录数等量，属于线性空间。

---

## 心得

- **核心技巧**：利用哈希表（字典）在一次遍历中完成计数，避免重复扫描。  
- **适用的题型**：  
  1. “统计每个元素出现次数” 类的题目（如 LeetCode 统计数组中每个数字出现次数）。  
  2. “分组聚合” 场景（SQL 中的 `GROUP BY`，在代码里往往用字典实现）。  
  3. “求每个用户的总交易额、总点赞数”等需要对同类键进行累计的题目。  
- **一句话总结解题钥匙**：**“把所有需要的统计信息放进字典，让每条记录只来一次，统计工作一次完成”。**

---

## 反思

- **第一反应**：看到“每个用户的关注人数”，自然想到“遍历表一次，累加计数”。  
- **最容易踩的坑**：  
  - 忽略了 `follower_id` 其实在本题不参与计数，容易在代码里写成 `cnt[follower_id] += 1`（把关注者当成被关注者）。  
  - 没有对 **不存在的用户**（例如某些用户没有任何粉丝）进行初始化，导致在输出时缺失这些用户。  
  - 忘记对结果按 `user_id` **升序** 排列，导致提交不通过。  
- **下次遇到同类题**：第一步先问自己“这是不是一次“**分组计数**”的需求？”，若是，就立刻准备一个 `defaultdict(int)`（或普通 dict）在一次遍历中完成计数。