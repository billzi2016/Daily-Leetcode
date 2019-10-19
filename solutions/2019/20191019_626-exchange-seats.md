# #626. 交换座位 / Exchange Seats

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/exchange-seats/)

---

## 题目（英文原版）

**Description**

Table: Seat
Write a solution to swap the seat id of every two consecutive students. If the number of students is odd, the id of the last student is not swapped.
Return the result table ordered by id in ascending order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| student     | varchar |
+-------------+---------+
id is the primary key (unique value) column for this table.
Each row of this table indicates the name and the ID of a student.
The ID sequence always starts from 1 and increments continuously.
```

**Example 2:**

```
Input: 
Seat table:
+----+---------+
| id | student |
+----+---------+
| 1  | Abbot   |
| 2  | Doris   |
| 3  | Emerson |
| 4  | Green   |
| 5  | Jeames  |
+----+---------+
Output: 
+----+---------+
| id | student |
+----+---------+
| 1  | Doris   |
| 2  | Abbot   |
| 3  | Green   |
| 4  | Emerson |
| 5  | Jeames  |
+----+---------+
Explanation: 
Note that if the number of students is odd, there is no need to change the last one's seat.
```

---

## 题目（中文翻译）

**表结构**: `Seat`

编写一个查询，将每两个相邻学生的座位 `id` 互换。若学生总数为奇数，则最后一位学生的座位 `id` 保持不变。  
返回的结果表需按 `id` **升序** 排列。结果格式参见下方示例。

**示例 1**

**表结构**  
```sql
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| student     | varchar |
+-------------+---------+
```
- `id` 为主键（唯一值）列。  
- 表中的每一行记录了学生的姓名和对应的 `id`。  
- `id` 序列始终从 `1` 开始，且连续递增。

**示例 2**

**输入**  
`Seat` 表：

| id | student |
|----|---------|
| 1  | Abbot   |
| 2  | Doris   |
| 3  | Emerson |
| 4  | Green   |
| 5  | Jeames  |

**输出**  

| id | student |
|----|---------|
| 1  | Doris   |
| 2  | Abbot   |
| 3  | Green   |
| 4  | Emerson |
| 5  | Jeames  |

**解释**  
每两个相邻的学生的座位 `id` 已互换；由于学生数量为奇数，最后一位学生（`id` 为 5）的座位保持不变。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有学生的记录都读进来**，然后**逐个检查**：  
- 取出第 `i` 行（`i` 从 1 开始），如果 `i` 是奇数，就把它和第 `i+1` 行互换；  
- 如果 `i` 已经是最后一行且没有配对的第 `i+1` 行（也就是学生总数为奇数），直接留下不动。

> **类比**：想象你在排队买票，老师要把相邻的两个人换位子。你可以从队首开始，一次检查两个人，决定是否换位。这个过程会遍历整条队伍 **一次**，但如果你每次都要去“重新找”下一对（比如用 `for i in range(1, n): for j in range(i+1, n):`）就会出现 **嵌套循环**，时间会变成 **平方级**。

下面给出一个**最笨的实现**：使用两层循环去寻找每一对相邻的 id，然后交换它们的 `student` 名字。虽然思路很清晰，但会导致大量重复遍历，时间复杂度是 **O(n²)**。

#### 代码（Python）

```python
def exchange_seats_brute(seats):
    """
    暴力解：两层循环逐个查找相邻的 id 并交换 student。
    参数 seats 为列表，每个元素是 (id, student) 的元组，id 从 1 连续递增。
    返回值同样是按 id 升序排列的列表。
    """
    # 先把数据复制一份，防止修改原始输入
    res = seats.copy()                     # O(n) 的额外空间

    n = len(res)
    for i in range(n):                     # 外层遍历每一行，次数 n
        for j in range(i + 1, n):          # 内层寻找 i 的下一个 id，最坏 n-1 次
            # 找到相邻的两行（id 差 1）就交换
            if res[i][0] + 1 == res[j][0]: # 这里的判断等价于 “是否相邻”
                # 交换 student 字段，id 保持不变
                res[i] = (res[i][0], res[j][1])
                res[j] = (res[j][0], res[i][1])
                break                      # 交换完后立刻结束内层循环
    # 最后按照 id 排序（虽然原表已经有序，这一步是保险的）
    res.sort(key=lambda x: x[0])
    return res
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  解释：外层循环跑 `n` 次，内层最坏情况下也要遍历 `n` 次（虽然实际会提前 `break`），所以整体是 “n 乘 n”。如果把 `n` 看成 1000，`n²` 就是 1,000,000，明显比一次遍历慢很多。  

- **空间复杂度**：`O(n)`  
  解释：我们额外创建了一个和原表等长的列表 `res` 来保存结果，这占用了与输入规模相同的额外空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈在于两层循环不停地去“寻找”相邻的行**。实际上我们已经知道：

- 表的 `id` 是 **连续递增**，从 1 开始，没有缺失。  
- 所以第 `i` 行的相邻行一定是第 `i+1` 行（如果 `i+1` 存在的话）。

因此我们只需要 **一次线性遍历**，把每一对相邻的记录直接交换即可。实现思路如下：

1. 读取所有记录到列表 `seats`（顺序已经是按 `id` 排好的）。  
2. 用 **步长为 2 的循环**（`for i in range(0, n-1, 2)`）一次处理一对相邻的学生：  
   - 把 `seats[i]` 的 `student` 与 `seats[i+1]` 的 `student` 互换。  
3. 如果学生总数是奇数，最后一个元素 `seats[-1]` 不会被遍历到，自然保持原位。  
4. 返回已经按 `id` 排好的列表。

> **类比**：这就像你手里有一串排好号的卡片，每次抓两张一起翻面，翻完所有卡片后就完成了。因为卡片已经排好，你不需要再去“找”下一张，只要一步步往后走就行。

#### 代码（Python）

```python
def exchange_seats_optimal(seats):
    """
    最优解：一次线性遍历，用步长为 2 的循环直接交换相邻两行的 student。
    参数 seats 为列表，每个元素是 (id, student) 的元组，id 连续递增。
    返回值同样是按 id 升序排列的列表。
    """
    # 复制一份防止修改原始输入（如果不在意可以直接在原列表上操作）
    res = seats.copy()                     # O(n) 的额外空间

    n = len(res)
    # range(0, n-1, 2) 确保 i+1 不会越界；如果 n 为奇数，最后一个元素不会被遍历到
    for i in range(0, n - 1, 2):
        # 交换 student 字段，id 保持不变
        id_i, stu_i = res[i]
        id_j, stu_j = res[i + 1]
        res[i] = (id_i, stu_j)             # 第 i 行换成第 i+1 行的学生
        res[i + 1] = (id_j, stu_i)         # 第 i+1 行换成第 i 行的学生

    # 已经是按 id 排好的，直接返回
    return res
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  解释：只遍历了一次数组，`n` 次循环（每次处理两条记录），所以时间随学生人数线性增长。比如有 10,000 名学生，只需要约 10,000 次操作，远快于平方级的暴力解。  

- **空间复杂度**：`O(n)`（如果在原表上就地修改，可降为 `O(1)`）  
  解释：我们仍然创建了一个同等大小的列表 `res` 来保存结果，所占空间与输入规模相同。如果面试官允许**原地修改**，只需要把 `res = seats`，这样额外空间就只有常数级别的临时变量。

---

## 心得

- **核心技巧**：利用**连续递增的下标**，一次线性遍历即可完成相邻元素的交换。  
- **适用场景**：  
  1. 两两交换相邻元素（如数组/链表的配对调换）。  
  2. 按固定步长（2）遍历并进行批量操作（如奇偶位翻转、交叉合并两列数据）。  
  3. 需要对已有顺序的数据进行“局部置换”而不是全局排序的场景。  
- **一句话总结**：**相邻元素的配对只要一步步走，一遍遍历就能完成**。

## 反思

- **第一反应**：看到 “id 连续递增”，立刻想到可以用下标直接定位相邻行，而不是去搜索。  
- **最容易踩的坑**：  
  - 忘记处理 **奇数长度** 的情况，导致最后一个学生被错误地与前一个学生再次交换。  
  - 在暴力实现里，`break` 写错位置会导致后面的配对被跳过，产生错误结果。  
- **下次类似题的第一步**：**先检查输入是否已经满足某种顺序或结构（如连续下标、已排序），再决定是要“搜索”还是直接“定位”。**这一步往往能把复杂度从 `O(n²)` 降到 `O(n)`。