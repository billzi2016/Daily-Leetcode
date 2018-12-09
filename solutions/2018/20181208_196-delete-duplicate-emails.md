# #196. 删除重复邮件 / Delete Duplicate Emails

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/delete-duplicate-emails/)

---

## 题目（英文原版）

**Description**

Table: Person
Write a solution to delete all duplicate emails, keeping only one unique email with the smallest id.
For SQL users, please note that you are supposed to write a DELETE statement and not a SELECT one.
For Pandas users, please note that you are supposed to modify Person in place.
After running your script, the answer shown is the Person table. The driver will first compile and run your piece of code and then show the Person table. The final order of the Person table does not matter.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| email       | varchar |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table contains an email. The emails will not contain uppercase letters.
```

**Example 2:**

```
Input: 
Person table:
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
| 3  | john@example.com |
+----+------------------+
Output: 
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
+----+------------------+
Explanation: john@example.com is repeated two times. We keep the row with the smallest Id = 1.
```

---

## 题目（中文翻译）

**表结构**：`Person`

编写一个 SQL（或 Pandas）语句，删除所有重复的 `email`，仅保留 `id` 最小的一条记录。

- 对于 SQL 使用者，请注意需要编写 `DELETE` 语句，而不是 `SELECT` 语句。  
- 对于 Pandas 使用者，请注意需要在原地（in‑place）修改 `Person`。

运行脚本后，系统会展示 `Person` 表的最终结果。驱动程序会先编译并执行你的代码，然后返回 `Person` 表。**表的最终顺序不做要求**。结果格式参照下例。

**示例 1**

| Column Name | Type    |
|-------------|---------|
| id          | int     |
| email       | varchar |

`id` 为主键（primary key），即该列的值唯一。表中的每一行都包含一个 `email`，且所有 `email` 均不含大写字母。

**示例 2**

**输入**  
Person 表：

```
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
| 3  | john@example.com |
+----+------------------+
```

**输出**  

```
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
+----+------------------+
```

**解释**：`john@example.com` 出现了两次，保留 `id` 最小的记录，即 `id = 1` 的那一行。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把每一行都和后面的所有行逐一比较**，只要发现邮箱相同且 `id` 更大的那一行，就把它删掉。  

- **数据结构**：这里用最简单的 `list[dict]` 来模拟数据库表。每条记录是一个字典，形如 `{'id': 1, 'email': 'a@b.com'}`。  
- **类比**：把这张表想象成一本通讯录，想把重复的电话号码都擦掉，只留下最早登记的那条。我们就像一个人手里拿着一本本通讯录，逐本翻，看后面的是否有相同的号码，遇到更晚登记的就撕掉。  
- **正确性**：因为我们把每一行都和它之后的所有行比较，**一定能找到所有重复的邮箱**，并且只保留最小 `id`（即最先出现的那条）。  

#### 代码（Python）

```python
def delete_duplicates_brute(person):
    """
    暴力删除重复 email，只保留 id 最小的那一行。
    参数 person: List[Dict]，每个 dict 含 'id' 与 'email' 两个键。
    直接在原列表上原地修改（相当于 SQL 的 DELETE）。
    """
    i = 0
    # 用 while 循环方便在删除元素后不遗漏检查
    while i < len(person):
        cur = person[i]
        j = i + 1
        # 与后面的每一行比较
        while j < len(person):
            if person[j]['email'] == cur['email']:
                # 邮箱相同且 id 更大（因为 j > i），删除该行
                del person[j]          # 删除后列表会自动左移
                # 删除后不需要 j++，因为新出现的 j 位置是下一条未检查的记录
            else:
                j += 1
        i += 1
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：外层循环遍历 `n` 条记录，内层循环最坏情况下也要遍历 `n` 条（实际上是 `n‑i‑1`），所以总操作次数大约是 `n × n/2`，用大写的 `O` 表示就是 `O(n²)`。直观上可以想象为“每条记录都要和所有其他记录握手一次”。  
- **空间复杂度**：`O(1)`（**常数级**）  
  - 解释：我们只用了几个临时变量 `i、j、cur`，并没有额外的随 `n` 增长的存储空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在“每条记录都要和后面的记录比较”。我们可以把 **“已经出现过的邮箱”** 记下来，这样后面的记录只需要 **一次查询** 就能判断自己是否是重复的。

实现思路如下：

1. **遍历一次** 表格（一次 O(n)），用一个哈希表（`dict`）记录每个 `email` 第一次出现时对应的 `id`。  
   - 哈希表就像一本“邮箱 → 最小 id”的小字典，查找速度非常快（平均 O(1)），类似于我们平时查字典时，先看左边的词（key），马上就能找到对应的页码（value）。  
2. 再遍历一次表格，把 **不在哈希表中**（或者 `id` 不是该邮箱对应的最小 `id`）的记录删掉。  
   - 这里仍然是 **原地删除**，保持与 SQL `DELETE` 的行为一致。  

这样只需要 **两次线性遍历**，时间从 `O(n²)` 降到了 `O(n)`，空间用了一个额外的 `dict`（大小最多等于不同邮箱的数量），即 `O(m)`（`m` 为唯一邮箱数），在最坏情况下 `m ≤ n`，仍然是线性空间。

#### 代码（Python）

```python
def delete_duplicates_optimal(person):
    """
    使用哈希表（dict）一次遍历找出每个 email 对应的最小 id，
    再一次遍历原地删除其它重复行。
    参数 person: List[Dict]，会在原列表上直接修改。
    """
    # 第一步：记录每个 email 最小的 id
    email_to_min_id = {}          # 哈希表：email -> 最小 id
    for row in person:
        email = row['email']
        cur_id = row['id']
        # 若邮箱未出现过，或出现过但当前 id 更小，则更新
        if email not in email_to_min_id or cur_id < email_to_min_id[email]:
            email_to_min_id[email] = cur_id

    # 第二步：原地删除不是最小 id 的行
    i = 0
    while i < len(person):
        row = person[i]
        # 如果该行的 id 不是该邮箱对应的最小 id，则删除
        if row['id'] != email_to_min_id[row['email']]:
            del person[i]          # 删除后列表左移，i 不变继续检查新出现的元素
        else:
            i += 1                 # 该行保留，继续检查下一行
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：我们只做了两次线性遍历，每次对每条记录的操作都是常数时间（哈希表的插入/查询均摊为 O(1)），所以总体是 `n + n = 2n`，用大写 `O` 表示就是 `O(n)`。这比暴力的 “每条记录要和其他所有记录握手” 快很多。  
- **空间复杂度**：`O(m)`（`m` 为不同 email 的数量，最坏情况下 `m = n`）  
  - 解释：额外用了一个字典来存放每个唯一邮箱对应的最小 `id`，相当于我们准备了一本“小字典”来记住每本书的第一章节页码。除这本字典外，其他变量都是常数级。

---

## 心得

- **核心技巧**：使用哈希表（字典）记录**首次出现**或**最小值**，实现 **一次遍历** 完成去重。  
- **适用题型**：  
  1. “删除/保留重复记录，只保留最小/最大 id” 类的数据库/表格去重。  
  2. “数组/列表中出现次数超过一次的元素，只保留一次” 如 LeetCode 1839. **找出所有出现两次的元素**。  
  3. “对字符串/数组进行去重并保留出现顺序” 如 “删除重复字符只保留第一个”。  
- **一句话总结**：**“把已经见过的东西记在字典里，后面来时直接查，重复的就删”。**

---

## 反思

- **第一反应**：看到“删除重复 email，保留最小 id”，立刻想到“遍历表格，遇到相同 email 则比较 id，删掉大的”。这就是暴力思路。  
- **最容易踩的坑**：  
  - **删除时的索引问题**：在遍历列表时直接 `del` 会导致后面的元素左移，如果不小心直接 `i += 1`，会漏掉检查紧跟在被删元素后的那一行。使用 `while` 循环并在删除后不移动指针可以避免。  
  - **大小写或空格**：题目说明 email 不含大写字母，但实际面试中常会出现需要先统一大小写或去除首尾空格的情况。  
  - **原地修改 vs 返回新列表**：SQL `DELETE` 是原地修改，若写成返回新列表的函数，可能与题目要求不符。  
- **下次第一步**：先思考“是否可以用哈希表一次遍历记录出现信息”，如果答案是肯定的，就直接走最优思路；如果不能，才考虑暴力或其他高级技巧（排序、双指针等）。