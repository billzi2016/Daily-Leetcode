# #3570. 查找没有可用副本的书籍 / Find Books with No Available Copies

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-books-with-no-available-copies/)

---

## 题目（英文原版）

**Description**

Table: library_books
Table: borrowing_records
Write a solution to find all books that are currently borrowed (not returned) and have zero copies available in the library.
Return the result table ordered by current borrowers in descending order, then by book title in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+------------------+---------+
| Column Name      | Type    |
+------------------+---------+
| book_id          | int     |
| title            | varchar |
| author           | varchar |
| genre            | varchar |
| publication_year | int     |
| total_copies     | int     |
+------------------+---------+
book_id is the unique identifier for this table.
Each row contains information about a book in the library, including the total number of copies owned by the library.
```

**Example 2:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| record_id     | int     |
| book_id       | int     |
| borrower_name | varchar |
| borrow_date   | date    |
| return_date   | date    |
+---------------+---------+
record_id is the unique identifier for this table.
Each row represents a borrowing transaction and return_date is NULL if the book is currently borrowed and hasn't been returned yet.
```

**Example 3:**

```
+---------+------------------------+------------------+----------+------------------+--------------+
| book_id | title                  | author           | genre    | publication_year | total_copies |
+---------+------------------------+------------------+----------+------------------+--------------+
| 1       | The Great Gatsby       | F. Scott         | Fiction  | 1925             | 3            |
| 2       | To Kill a Mockingbird  | Harper Lee       | Fiction  | 1960             | 3            |
| 3       | 1984                   | George Orwell    | Dystopian| 1949             | 1            |
| 4       | Pride and Prejudice    | Jane Austen      | Romance  | 1813             | 2            |
| 5       | The Catcher in the Rye | J.D. Salinger    | Fiction  | 1951             | 1            |
| 6       | Brave New World        | Aldous Huxley    | Dystopian| 1932             | 4            |
+---------+------------------------+------------------+----------+------------------+--------------+
```

**Example 4:**

```
+-----------+---------+---------------+-------------+-------------+
| record_id | book_id | borrower_name | borrow_date | return_date |
+-----------+---------+---------------+-------------+-------------+
| 1         | 1       | Alice Smith   | 2024-01-15  | NULL        |
| 2         | 1       | Bob Johnson   | 2024-01-20  | NULL        |
| 3         | 2       | Carol White   | 2024-01-10  | 2024-01-25  |
| 4         | 3       | David Brown   | 2024-02-01  | NULL        |
| 5         | 4       | Emma Wilson   | 2024-01-05  | NULL        |
| 6         | 5       | Frank Davis   | 2024-01-18  | 2024-02-10  |
| 7         | 1       | Grace Miller  | 2024-02-05  | NULL        |
| 8         | 6       | Henry Taylor  | 2024-01-12  | NULL        |
| 9         | 2       | Ivan Clark    | 2024-02-12  | NULL        |
| 10        | 2       | Jane Adams    | 2024-02-15  | NULL        |
+-----------+---------+---------------+-------------+-------------+
```

**Example 5:**

```
+---------+------------------+---------------+-----------+------------------+-------------------+
| book_id | title            | author        | genre     | publication_year | current_borrowers |
+---------+------------------+---------------+-----------+------------------+-------------------+
| 1       | The Great Gatsby | F. Scott      | Fiction   | 1925             | 3                 | 
| 3       | 1984             | George Orwell | Dystopian | 1949             | 1                 |
+---------+------------------+---------------+-----------+------------------+-------------------+
```

---

## 题目（中文翻译）

**描述**  
表：`library_books`  
表：`borrowing_records`  

编写一个查询，找出所有当前被借出（`return_date` 为 `NULL`）且图书馆中没有可用副本的书籍。  
返回结果表按照 **当前借阅人数**（`current_borrowers`）降序排列，若人数相同则按 **书名**（`title`）升序排列。  
结果格式参见下面的示例。

**示例**  

示例 1:  
```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| book_id      | int     |
| title        | varchar |
| author       | varchar |
| genre        | varchar |
| publication_year | int |
| total_copies | int     |
+--------------+---------+
```
`book_id` 为该表的唯一标识。每行包含一本书的基本信息。

示例 2:  
```
+-----------+---------+---------------+-------------+-------------+
| Column Name | Type    |
+-----------+---------+---------------+-------------+-------------+
| record_id   | int     |
| book_id     | int     |
| borrower_name | varchar |
| borrow_date | date    |
| return_date | date    |
+-----------+---------+---------------+-------------+-------------+
```
`record_id` 为该表的唯一标识。每行代表一次借阅交易，若 `return_date` 为 `NULL` 则表示该书仍未归还。

示例 3:  
```
+---------+-------------------+------------------+----------+-------------------+--------------+
| book_id | title             | author           | genre    | publication_year  | total_copies |
+---------+-------------------+------------------+----------+-------------------+--------------+
| 1       | The Great Gatsby  | F. Scott         | Fiction  | 1925              | 3            |
...
```

示例 4:  
```
+-----------+---------+---------------+-------------+-------------+
| record_id | book_id | borrower_name | borrow_date | return_date |
+-----------+---------+---------------+-------------+-------------+
| 1         | 1       | Alice Smith   | 2024-01-15  | NULL        |
| 2         | 1       | Bob Johnson   | 2024-01-20  | NULL        |
| 3         | 2       | Carol White   | 2024-01-10  | 2024-0
...
```

示例 5（查询结果）:  
```
+---------+-------------------+------------------+----------+-------------------+-------------------+
| book_id | title             | author           | genre    | publication_year  | current_borrowers |
+---------+-------------------+------------------+----------+-------------------+-------------------+
| 1       | The Great Gatsby  | F. Scott         | Fiction  | 1925              | 3                 |
| 3       | ...               | ...              | ...      | ...               | ...               |
...
```

**约束条件**  
暂无。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是 **对每一本书都去遍历所有借阅记录**，统计这本书当前（`return_date` 为 `NULL`）被借走的次数，随后和该书的 `total_copies` 做比较。  

- **使用的数据结构**  
  - `library_books` 表可以看成一本“图书目录”，每一行是一条记录。  
  - `borrowing_records` 表则像一本“借阅日志”，每一行记录一次借书/还书。  
  - 为了快速查找某本书对应的日志，我们可以把 **图书目录** 放进一个 `list`（就像一摞书），把 **借阅日志** 也放进另一个 `list`。  

- **为什么正确**  
  对每本书我们都把所有日志都检查一遍，能够完整地统计出当前正在借出的副本数。如果这次数 **≥** `total_copies`，说明图书馆里已经没有可借的副本了（即“available copies = 0”），于是把这本书加入答案。  

- **复杂度分析（大白话）**  
  - 假设有 `B` 本书，`R` 条借阅记录。  
  - 对每本书我们都要遍历 `R` 条记录 → **时间复杂度是 `O(B·R)`**。如果 `B=1000`、`R=5000`，相当于要跑 **5 百万次**的循环，虽然还能接受，但如果数据量翻十倍就会很慢。  
  - 我们只使用了几个临时变量和两个列表 → **空间复杂度是 `O(1)`**（不随输入规模增长）。  

#### 代码（Python）  

```python
# ------------------- 暴力解 -------------------
# 假设输入是两张表的列表形式
# library_books : List[dict]   每本书的信息
# borrowing_records : List[dict] 每条借阅记录

def find_books_bruteforce(library_books, borrowing_records):
    result = []                                 # 用来装最终符合条件的书
    for book in library_books:                  # 对每一本书
        current_borrowers = 0                   # 记录这本书当前被借出的次数
        for rec in borrowing_records:          # 遍历所有借阅日志
            # 只关心同一本书、且还没有归还的记录
            if rec["book_id"] == book["book_id"] and rec["return_date"] is None:
                current_borrowers += 1
        # 若已借出的副本数 >= 总副本数，说明图书馆里没有可借的了
        if current_borrowers >= book["total_copies"]:
            # 为了后面排序，直接把借阅人数也放进返回字段
            out = book.copy()
            out["current_borrowers"] = current_borrowers
            result.append(out)

    # 排序要求：借阅人数降序 → 书名升序
    result.sort(key=lambda x: (-x["current_borrowers"], x["title"]))
    return result
```

#### 复杂度  

- **时间复杂度**：`O(B·R)`  
  - “B 本书 × R 条记录”，相当于每本书都要把所有记录都翻一遍。  
- **空间复杂度**：`O(1)`（不计结果集）  
  - 只用了常数个计数器和临时变量，额外占用的内存几乎不随输入规模增长。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于每本书都要遍历全部借阅记录**。实际上，我们只需要 **一次遍历借阅记录**，把“当前借出的副本数”先算好，随后再一次遍历图书目录即可得到答案。  

关键点如下：  

1. **把借阅记录按 `book_id` 分组**  
   - 使用 **哈希表（字典）**，把每本书的 “当前借阅人数” 累计进去。  
   - 哈希表就像一本“字典”，`key` 是书的编号，`value` 是该书当前被借走的数量。  

2. **遍历图书目录**  
   - 对每本书直接从哈希表里取出已经借出的数量（如果没有则为 0），和 `total_copies` 比较。  

3. **排序**  
   - 同样按照 “借阅人数降序 → 书名升序” 排序。  

这样我们只需要 **两次线性遍历**（一次遍历借阅记录，一次遍历图书目录），时间从 `O(B·R)` 降到 `O(B + R)`，对大数据量友好。  

#### 代码（Python）  

```python
# ------------------- 最优解（哈希表） -------------------
def find_books_optimal(library_books, borrowing_records):
    # 1️⃣ 统计每本书当前被借出的副本数
    #   borrowed_cnt[book_id] = 当前未归还的记录数量
    borrowed_cnt = {}
    for rec in borrowing_records:
        # 只统计尚未归还的记录
        if rec["return_date"] is None:
            bid = rec["book_id"]
            borrowed_cnt[bid] = borrowed_cnt.get(bid, 0) + 1

    # 2️⃣ 根据统计结果筛选“可借副本为 0”的书
    result = []
    for book in library_books:
        cur = borrowed_cnt.get(book["book_id"], 0)   # 若字典里没有，说明没有人在借
        if cur >= book["total_copies"]:              # 已经借走的数量 ≥ 总副本数
            out = book.copy()
            out["current_borrowers"] = cur
            result.append(out)

    # 3️⃣ 排序：借阅人数降序 → 书名升序
    result.sort(key=lambda x: (-x["current_borrowers"], x["title"]))
    return result
```

#### 复杂度  

- **时间复杂度**：`O(B + R)`  
  - 第一次遍历 `borrowing_records`（`R` 条），第二次遍历 `library_books`（`B` 本），两者相加。相比暴力解的 `B·R`，速度提升非常明显。  
- **空间复杂度**：`O(K)`（`K` 为实际出现过的 `book_id` 数量）  
  - 额外用了一个字典来存储每本书的当前借阅人数。最坏情况下 `K = B`，即每本书都有借阅记录，空间仍然是线性的。  

---  

## 心得  

- **核心技巧**：**哈希表（字典）统计分组**  
  - 先把需要“聚合”的信息（这里是“当前借阅人数”）一次遍历全部原始数据并放进哈希表，再用这张“中间表”快速做后续筛选。  
- **适用的题型**  
  1. “统计每个用户的订单总额”  
  2. “找出销量最高的商品”  
  3. “查询每门课程的在读学生数”  
- **一句话总结解题钥匙**：**把“多对多”遍历转化为“先聚合再过滤”，一次遍历搞定所有计数**。  

## 反思  

- **第一反应**：看到“每本书都要检查所有借阅记录”，立刻想到 **双层循环**（暴力）会很慢。  
- **最容易踩的坑**  
  - **`return_date` 为 `NULL` 的判断**：在 Python 中用 `is None`，在实际 SQL 里要写 `IS NULL`。忘记判断会把已归还的记录也算进去。  
  - **边界情况**：某本书根本没有任何借阅记录，此时 `borrowed_cnt` 中没有对应的键，需要默认值 `0`。  
  - **等于总副本的情况**：题目要求 “available copies = 0”，所以 `>= total_copies`（而不是 `>`）才算符合。  
- **下次第一步**：先 **思考是否可以一次遍历把需要的聚合信息统计出来**，再决定是否需要哈希表或其他分组手段，而不是直接写双层循环。