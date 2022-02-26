# #1683. Invalid Tweets / Invalid Tweets

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/invalid-tweets/)

---

## 题目（英文原版）

**Description**

Table: Tweets
Write a solution to find the IDs of the invalid tweets. The tweet is invalid if the number of characters used in the content of the tweet is strictly greater than 15.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| tweet_id       | int     |
| content        | varchar |
+----------------+---------+
tweet_id is the primary key (column with unique values) for this table.
content consists of alphanumeric characters, '!', or ' ' and no other special characters.
This table contains all the tweets in a social media app.
```

**Example 2:**

```
Input: 
Tweets table:
+----------+-----------------------------------+
| tweet_id | content                           |
+----------+-----------------------------------+
| 1        | Let us Code                       |
| 2        | More than fifteen chars are here! |
+----------+-----------------------------------+
Output: 
+----------+
| tweet_id |
+----------+
| 2        |
+----------+
Explanation: 
Tweet 1 has length = 11. It is a valid tweet.
Tweet 2 has length = 33. It is an invalid tweet.
```

---

## 题目（中文翻译）

编写一个查询，找出 **无效推文**（invalid tweet）的 `tweet_id`。当推文的 `content` 中使用的字符数 **严格大于** 15 时，该推文被视为无效。返回结果表，顺序不限，格式参考下方示例。

**表结构**

```
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| tweet_id       | int     |
| content        | varchar |
+----------------+---------+
```

- `tweet_id` 为主键（primary key），值唯一。  
- `content` 只包含字母数字字符、感叹号 `!` 或空格 `' '`，不含其他特殊字符。  
- 该表记录了社交媒体应用中的所有推文。

**示例**

输入表 `Tweets`：

```
+----------+-----------------------------------+
| tweet_id | content                           |
+----------+-----------------------------------+
| 1        | Let us Code                       |
| 2        | More than fifteen chars are here!|
+----------+-----------------------------------+
```

输出：

```
+----------+
| tweet_id |
+----------+
| 2        |
+----------+
```

**解释**  
第 2 条记录的 `content` 长度为 33（大于 15），因此对应的 `tweet_id` 为无效推文。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **每一条推文** 都拿出来，数一数它的字符数（`len(content)`），如果大于 15 就把它的 `tweet_id` 加入答案。  

- **数据结构**：把整张表当成 Python 中的 **列表**（list），每条记录用 **元组** 或 **字典** 保存。  
  - 列表就像我们平时的“排队”，可以从头到尾一次遍历。  
  - 每条记录的 `content` 像一本书的正文，`len(content)` 就是数这本书有多少页（字符）。  
- **为什么正确**：题目只要求找出字符数 **严格大于 15** 的推文，遍历一次检查每条记录即可，必然不会遗漏也不会误判。  

**时间/空间复杂度**（大白话版）  
- **时间复杂度**：`O(n)`，其中 `n` 是推文的条数。我们只需要看一遍表，像排队时只走一趟。  
- **空间复杂度**：`O(k)`，`k` 是符合条件的推文数量（要把它们的 `tweet_id` 保存下来），最坏情况下 `k ≤ n`，所以额外空间最多和输入规模成正比。  

#### 代码（Python）

```python
# 假设表数据已经在 Python 中，用 list of dict 表示
tweets = [
    {"tweet_id": 1, "content": "Let us Code"},
    {"tweet_id": 2, "content": "More than fifteen chars are here!"},
    # 其他记录 ...
]

def invalid_tweets_bruteforce(tweets):
    """返回所有字符数 > 15 的 tweet_id 列表"""
    res = []                                 # 用来收集答案
    for row in tweets:                       # 逐条检查
        # len(row["content"]) 就是字符数，>15 表示不合法
        if len(row["content"]) > 15:
            res.append(row["tweet_id"])      # 记下它的 id
    return res

# 演示
print(invalid_tweets_bruteforce(tweets))   # [2]
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次表，`n` 越大，耗时线性增长。  
- **空间复杂度**：`O(k)` —— 只额外存放符合条件的 `tweet_id`，`k` 最多等于 `n`。  

---

### 2. 最优解

#### 思路  

从暴力解来看，它已经是 **线性时间**，在只能一次遍历表的前提下已经是最快的了。  
唯一可以改进的地方是 **写法更简洁、常数因子更小**，比如利用 Python 的 **列表推导式** 或 **内置 filter**，让代码更“函数式”。  
核心技巧：**一次遍历 + 条件筛选**（相当于 SQL 中的 `WHERE len(content) > 15`），不需要额外的数据结构（如哈希表、堆等），因此已经是最优。

下面给出两种更简洁的实现方式：

1. **列表推导式**：一行代码完成遍历和过滤。  
2. **filter + lambda**：使用函数式编程的风格，思路与列表推导式相同。

#### 代码（Python）

```python
# 方式 1：列表推导式
def invalid_tweets_listcomp(tweets):
    """
    用列表推导式一次遍历完成过滤，代码简洁，效率与暴力解相同。
    """
    return [row["tweet_id"] for row in tweets if len(row["content"]) > 15]

# 方式 2：filter + lambda
def invalid_tweets_filter(tweets):
    """
    filter 把不符合条件的记录过滤掉，lambda 定义筛选规则。
    """
    return list(map(lambda r: r["tweet_id"],
                    filter(lambda r: len(r["content"]) > 15, tweets)))

# 演示
print(invalid_tweets_listcomp(tweets))   # [2]
print(invalid_tweets_filter(tweets))     # [2]
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 仍然只遍历一次表。相比暴力解，**时间量级没有变化**，只是代码更简洁、常数因子略小。  
- **空间复杂度**：`O(k)` —— 只保存符合条件的 `tweet_id`，与暴力解相同。  

---

## 心得

- **核心技巧**：一次遍历配合条件过滤（相当于 `WHERE` 子句）。  
- **适用的题型**：  
  1. “找出满足某个阈值的记录”——如 `SELECT * FROM Orders WHERE amount > 1000`。  
  2. “统计符合条件的元素数量”——如统计数组中大于某值的元素个数。  
  3. “从日志中挑出错误信息”——如 `len(message) > 50`。  
- **一句话总结**：**只要能一次遍历完成筛选，就已经是最优解**。

---

## 反思

- **第一反应**：直接遍历每条推文，检查 `len(content) > 15`，把符合的 `tweet_id` 收集起来。  
- **最容易踩的坑**：  
  - 忘记“严格大于”而写成 “大于等于”。  
  - 内容里可能出现空格或感叹号，这些都算字符，**不要只数字母**。  
  - 输入可能为空表，需要返回空列表而不是报错。  
- **下次类似题的第一步**：先把 “**一次遍历 + 条件筛选**” 这把钥匙摆在手上，判断是否还能进一步压缩时间（比如是否能用哈希表提前定位），如果不行，就直接用线性遍历即可。