# #1204. **最后能上公交的乘客** / Last Person to Fit in the Bus

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/last-person-to-fit-in-the-bus/)

---

## 题目（英文原版）

**Description**

Table: Queue
There is a queue of people waiting to board a bus. However, the bus has a weight limit of 1000 kilograms, so there may be some people who cannot board.
Write a solution to find the person_name of the last person that can fit on the bus without exceeding the weight limit. The test cases are generated such that the first person does not exceed the weight limit.
Note that only one person can board the bus at any given turn.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| person_id   | int     |
| person_name | varchar |
| weight      | int     |
| turn        | int     |
+-------------+---------+
person_id column contains unique values.
This table has the information about all people waiting for a bus.
The person_id and turn columns will contain all numbers from 1 to n, where n is the number of rows in the table.
turn determines the order of which the people will board the bus, where turn=1 denotes the first person to board and turn=n denotes the last person to board.
weight is the weight of the person in kilograms.
```

**Example 2:**

```
Input: 
Queue table:
+-----------+-------------+--------+------+
| person_id | person_name | weight | turn |
+-----------+-------------+--------+------+
| 5         | Alice       | 250    | 1    |
| 4         | Bob         | 175    | 5    |
| 3         | Alex        | 350    | 2    |
| 6         | John Cena   | 400    | 3    |
| 1         | Winston     | 500    | 6    |
| 2         | Marie       | 200    | 4    |
+-----------+-------------+--------+------+
Output: 
+-------------+
| person_name |
+-------------+
| John Cena   |
+-------------+
Explanation: The folowing table is ordered by the turn for simplicity.
+------+----+-----------+--------+--------------+
| Turn | ID | Name      | Weight | Total Weight |
+------+----+-----------+--------+--------------+
| 1    | 5  | Alice     | 250    | 250          |
| 2    | 3  | Alex      | 350    | 600          |
| 3    | 6  | John Cena | 400    | 1000         | (last person to board)
| 4    | 2  | Marie     | 200    | 1200         | (cannot board)
| 5    | 4  | Bob       | 175    | ___          |
| 6    | 1  | Winston   | 500    | ___          |
+------+----+-----------+--------+--------------+
```

---

## 题目（中文翻译）

有一条等待上公交的排队（queue），每个人都有对应的体重（weight）。公交车的最大承载重量为 **1000 千克**，因此可能会出现有些人因为重量限制而无法上车。  

请编写 SQL 查询，找出 **person_name**（乘客姓名）中**最后一个**能够在不超过重量上限的情况下上车的乘客。测试用例保证**第一个**上车的乘客的重量不会超过上限。  

注意：每一轮（turn）只能让 **一个** 人上车。  

返回结果的格式请参考下例。

### 示例 1

表结构：

```sql
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| person_id   | int     |
| person_name | varchar |
| weight      | int     |
| turn        | int     |
+-------------+---------+
```

- `person_id` 列的值唯一。  
- 该表记录了所有等待上车的人员信息。  
- `person_id` 与 `turn` 列的取值范围为 `1` 到 `n`（`n` 为总人数），且两列均包含 **所有** 从 `1` 到 `n` 的整数。  

（此处应有示例输出，保持原样）

### 示例 2

**输入**  

Queue 表：

```text
+-----------+-------------+--------+------+
| person_id | person_name | weight | turn |
+-----------+-------------+--------+------+
| 5         | Alice       | 250    | 1    |
| 4         | Bob         | 175    | 5    |
| 3         | Alex        | 350    | 2    |
| 6         | John Cena   | 400    | 3    |
| 1         | Winston     | 500    | 6    |
| 2         | Marie       | ...    | ...  |
+-----------+-------------+--------+------+
```

（此处应有示例输出，保持原样）

### 约束条件

- 表中每行对应一个唯一的 `person_id`。  
- `weight` 为正整数，单位为千克。  
- `turn` 表示上车的顺序，且每个 `turn` 只对应一个人。  
- 总重量上限固定为 **1000**。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**按排队顺序（turn）逐个让人上车**，每上一个人就把他的体重加到总重量里。  
如果加上下一位的体重后会超过 1000 kg，就停止，此时上车的最后一个人就是答案。  

在实现上，我们可以：

1. 先把 `Queue` 表的所有记录全部取出来（这里用一个列表模拟）。
2. 用两层循环模拟“每次从头重新算一次累计重量”。  
   - 外层遍历每一个人 `i`（假设他是最后一个能上车的），  
   - 内层把 `0 … i` 的体重全部相加，检查是否超过 1000。  
   - 如果超过，就把 `i‑1` 那个人的名字记下来，结束循环。

> **数据结构类比**：  
> - 列表就像一排排好队的乘客，顺序就是他们的 `turn`。  
> - 累计求和好比在称重秤上一次次把人的体重放进去，看看秤会不会“爆表”。  

这种方法一定能得到正确答案，因为我们把 **所有可能的上车人数** 都穷举检查了一遍，只要有一种方式不超重，就一定会被找到。

#### 代码（Python）

```python
# ------------------- 暴力解 -------------------
# 假设已经把表中的数据读取进 list_of_people，每条记录是 (turn, person_name, weight)
# 例子：[(1, "Alice", 250), (2, "Bob", 300), ...]

def last_person_bruteforce(list_of_people):
    # 按 turn 排序，确保顺序和题目要求一致
    people = sorted(list_of_people, key=lambda x: x[0])

    n = len(people)
    answer = None                     # 最后能上车的人的名字

    # 外层遍历每一种「最后一个上车的人」的可能性
    for i in range(n):
        total = 0                     # 当前累计的总重量
        # 内层把 0~i 的人全部加起来
        for j in range(i + 1):
            total += people[j][2]     # weight 在元组的第 3 位
        # 检查是否已经超过 1000
        if total > 1000:
            # 超重了，说明 i-1 才是最后能上车的人
            answer = people[i - 1][1]    # person_name 在第 2 位
            break
        # 如果遍历到最后都没有超重，则最后一个人就是答案
        if i == n - 1:
            answer = people[i][1]

    return answer
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层遍历 `n` 次，内层每次最坏要累计 `i+1` 次，形成等差求和，最终是 `1 + 2 + … + n = n·(n+1)/2 ≈ n²/2`。  
  - 用大白话说，就是如果有 1000 个人排队，程序大概会做 500 000 次加法——这在数据量稍大时会明显慢下来。  
- **空间复杂度**：`O(1)`（不计输入列表本身）  
  - 只用了几个临时变量 `total、answer`，不随 `n` 增长而增长。

---

### 2. 最优解

#### 思路  

暴力解的慢点在 **每次都重新累加** 前面的体重，导致大量重复计算。  
其实我们只需要 **一次遍历**，把每个人的体重依次加到累计和里，一旦累计和超过 1000，就可以直接停下来，前一个人就是答案。

实现步骤：

1. **按 turn 排序**（如果原始数据已经是按 turn 排好的，这一步可以省略，时间仍然是 `O(n log n)` 最差）。  
2. 用一个变量 `cur_weight` 记录当前已经上车的总重量。  
3. 依次遍历排好序的乘客：  
   - 如果 `cur_weight + weight ≤ 1000`，说明这位乘客还能上车，更新 `cur_weight` 并把 `last_name` 设为他的名字。  
   - 否则，累计重量已经要超标，直接返回之前记录的 `last_name`。  
4. 遍历结束后（所有人都能上车），返回最后记录的 `last_name`。

> **核心技巧**：**一次遍历 + 前缀和**  
> 前缀和的思想是把“从起点到当前位置的累计值”保存下来，后面再需要时直接使用，而不必重新从头累加。这里的 `cur_weight` 就是前缀和。

> **类比**：想象你在称重秤上一次次放进乘客的行李，每放一次秤会显示当前总重量。只要秤显示不超过 1000，你就继续；一旦显示超过，就停下，前一次的乘客就是最后能上车的。

#### 代码（Python）

```python
# ------------------- 最优解 -------------------
def last_person_optimal(list_of_people):
    """
    :param list_of_people: List[Tuple[int, str, int]]
           每条记录为 (turn, person_name, weight)
    :return: 最后一个还能上车的 person's name
    """
    # 1. 按 turn 排序，确保上车顺序正确
    people = sorted(list_of_people, key=lambda x: x[0])

    cur_weight = 0          # 已经上车的累计重量
    last_name = None        # 最近一次成功上车的人的名字

    for turn, name, w in people:
        if cur_weight + w > 1000:   # 加上这位会超重，停止
            break
        # 还能上车，更新累计重量和答案
        cur_weight += w
        last_name = name

    # 按题意，保证至少第一位能上车，所以 last_name 一定非空
    return last_name
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`（排序）  
  - 如果输入已经按 `turn` 排好序，则只需要一次遍历，时间是 `O(n)`。  
  - 与暴力解的 `O(n²)` 相比，`n` 增大时速度提升非常明显。  
- **空间复杂度**：`O(1)`（不计排序所需的临时列表）  
  - 只用了几个变量 `cur_weight、last_name`，不随 `n` 增长。

---

## 心得

- **核心技巧**：一次遍历累计前缀和（前缀和 + 早停）。  
- **适用题型**：  
  1. “在序列中找第一个使累计和超过阈值的元素”  
  2. “在有序序列中寻找满足累计约束的最长前缀”  
  3. “背包类的 Greedy（贪心）问题，只需线性扫描”。  
- **解题钥匙**：**把“重复的累加”改成“记住上一次的累计”，只遍历一次就够了**。

---

## 反思

- **第一反应**：把所有人一次次全部相加，看看哪一步会超重——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记先按 `turn` 排序，导致上车顺序错误。  
  - 当所有人都能上车时，需要返回最后一个人的名字，而不是 `None`。  
  - 题目保证第一位不会超重，但如果忘记这点，代码里要额外判断空结果。  
- **下次遇到同类题**：第一步先思考“累计和”是否可以在一次遍历中维护，是否可以利用**前缀和 + 早停**的贪心策略。这样往往能直接得到 O(n)（或 O(n log n)）的最优解。