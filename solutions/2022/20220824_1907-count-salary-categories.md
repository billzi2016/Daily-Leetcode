# #1907. 统计工资类别 / Count Salary Categories

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/count-salary-categories/)

---

## 题目（英文原版）

**Description**

Table: Accounts
Write a solution to calculate the number of bank accounts for each salary category. The salary categories are:
The result table must contain all three categories. If there are no accounts in a category, return 0.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| account_id  | int  |
| income      | int  |
+-------------+------+
account_id is the primary key (column with unique values) for this table.
Each row contains information about the monthly income for one bank account.
```

**Example 2:**

```
Input: 
Accounts table:
+------------+--------+
| account_id | income |
+------------+--------+
| 3          | 108939 |
| 2          | 12747  |
| 8          | 87709  |
| 6          | 91796  |
+------------+--------+
Output: 
+----------------+----------------+
| category       | accounts_count |
+----------------+----------------+
| Low Salary     | 1              |
| Average Salary | 0              |
| High Salary    | 3              |
+----------------+----------------+
Explanation: 
Low Salary: Account 2.
Average Salary: No accounts.
High Salary: Accounts 3, 6, and 8.
```

---

## 题目（中文翻译）

**题目描述**  
表：`Accounts`  

请编写一个查询，统计每个工资类别（salary category）对应的银行账户数量。工资类别划分如下：

- **Low Salary**：`income < 30000`
- **Average Salary**：`30000 ≤ income ≤ 70000`
- **High Salary**：`income > 70000`

结果表必须包含上述所有三类，即使某一类别的账户数为 `0` 也要返回 `0`。  
返回的结果表可以任意排序，格式请参考下例。

**示例 1**

```sql
+-------------+------+
| Column Name | Type |
+-------------+------+
| account_id  | int  |
| income      | int  |
+-------------+------+
```

`account_id` 为该表的主键（唯一值列）。每一行记录了一个银行账户的月收入（`income`）。

**示例 2**

**输入**  
`Accounts` 表：

```
+------------+--------+
| account_id | income |
+------------+--------+
| 3          | 108939 |
| 2          | 12747  |
| 8          | 87709  |
| 6          | 91796  |
+------------+--------+
```

**输出**  

```
+----------------+----------------+
| category       | accounts_count |
+----------------+----------------+
| Low Salary     | 1              |
| Average Salary | 0              |
| High Salary    | 3              |
+----------------+----------------+
```

**约束条件**  

- 表中不存在重复的 `account_id`。  
- `income` 为非负整数。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每一种薪资区间都遍历整张表一次**，统计落在该区间的账户数。  
可以把这张表想象成一本电话簿，**“遍历整张表一次”**就像把电话簿从头到尾翻一遍，检查每个人的收入是否落在我们预先划好的三个区间里：

| 薪资区间 | 条件 |
|----------|------|
| Low Salary      | income < 30000 |
| Average Salary  | 30000 ≤ income ≤ 80000 |
| High Salary     | income > 80000 |

实现时我们会写三个独立的循环，每个循环都遍历 `Accounts` 表的所有记录并计数。  
这个办法一定能得到正确答案，因为我们把 **所有** 记录都检查了一遍，只要满足对应的条件就会被计入。

#### 代码（Python）

```python
# 假设 accounts 是一个列表，每个元素是 (account_id, income) 的元组
# 例子：accounts = [(3, 108939), (2, 12747), (8, 87709), (6, 91796)]

def count_salary_bruteforce(accounts):
    # 1️⃣ 统计 Low Salary
    low_cnt = 0
    for _, inc in accounts:                 # 遍历所有记录
        if inc < 30000:                      # 判断是否属于 Low Salary
            low_cnt += 1

    # 2️⃣ 统计 Average Salary
    avg_cnt = 0
    for _, inc in accounts:
        if 30000 <= inc <= 80000:            # 判断是否属于 Average Salary
            avg_cnt += 1

    # 3️⃣ 统计 High Salary
    high_cnt = 0
    for _, inc in accounts:
        if inc > 80000:                      # 判断是否属于 High Salary
            high_cnt += 1

    # 把结果按照题目要求的格式返回
    return [
        ("Low Salary", low_cnt),
        ("Average Salary", avg_cnt),
        ("High Salary", high_cnt)
    ]

# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    accounts = [(3, 108939), (2, 12747), (8, 87709), (6, 91796)]
    for cat, cnt in count_salary_bruteforce(accounts):
        print(f"{cat:15} | {cnt}")
```

#### 复杂度  

- **时间复杂度**：`O(n × 3) ≈ O(n)`，其中 `n` 是账户的数量。  
  这里的 `O(n²)` 并没有出现，因为我们只遍历了三遍（常数次），在大白话里可以理解为“每条记录只被看了几次”，所以整体仍然是线性增长。  
- **空间复杂度**：`O(1)`，只用了几个计数器，和 `n` 无关。

> **小结**：虽然这种写法已经是线性的，但我们仍然**重复遍历了同一份数据三次**，看起来有点“啰嗦”。下面我们来一次性完成统计，进一步简化代码。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于对表的多次遍历**。  
如果我们在一次遍历过程中就把每条记录分配到对应的类别，就不需要再额外扫描了。  

这就像在一次检查所有学生成绩时，同时记录“及格人数”和“不及格人数”，而不是先遍历一次统计及格，再遍历一次统计不及格。

实现思路：

1. 初始化三个计数器 `low_cnt、avg_cnt、high_cnt`，全部设为 0。  
2. **一次**遍历 `Accounts` 表的每条记录：
   - 如果收入 `< 30000`，`low_cnt += 1`。  
   - 否则如果收入 `≤ 80000`（已经排除了 `<30000` 的情况），`avg_cnt += 1`。  
   - 其它情况必然是 `> 80000`，`high_cnt += 1`。  
3. 遍历结束后，直接返回三个计数器的值。

这里使用 **`if‑elif‑else`** 连续判断，保证每条记录只走一次判断分支，时间上是最优的。

#### 代码（Python）

```python
def count_salary_optimal(accounts):
    """
    一次遍历统计三类薪资账户数量
    :param accounts: List[Tuple[int, int]]，每个元素是 (account_id, income)
    :return: List[Tuple[str, int]]，每个元素是 (category, accounts_count)
    """
    low_cnt = avg_cnt = high_cnt = 0      # 初始化计数器

    for _, inc in accounts:               # 只遍历一次
        if inc < 30000:                    # Low Salary
            low_cnt += 1
        elif inc <= 80000:                 # Average Salary（已经排除 low）
            avg_cnt += 1
        else:                              # High Salary
            high_cnt += 1

    # 按题目要求返回三行结果，顺序不限
    return [
        ("Low Salary", low_cnt),
        ("Average Salary", avg_cnt),
        ("High Salary", high_cnt)
    ]

# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    accounts = [(3, 108939), (2, 12747), (8, 87709), (6, 91796)]
    for cat, cnt in count_salary_optimal(accounts):
        print(f"{cat:15} | {cnt}")
```

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次表，和记录数线性相关。  
  与暴力解相比，**遍历次数从 3 次降到 1 次**，在大数据量时能省去约 2/3 的循环开销。  
- **空间复杂度**：`O(1)`，只用了常数个计数器，不随 `n` 增长。

---

## 心得

- **核心技巧**：一次遍历 + 条件分类（`if‑elif‑else`）。  
- **适用场景**：  
  1. 需要对数据进行**分桶计数**（比如年龄段、成绩等级）。  
  2. 需要**统计不同状态的数量**（如订单状态、用户活跃度）。  
  3. 任何可以用**固定阈值划分**的场景。  
- **解题钥匙**：**把所有需要的统计放进同一次遍历**，避免重复扫描。

---

## 反思

- **第一反应**：看到“统计三类”，马上想到 **SQL 的 GROUP BY**，但在纯 Python 环境下要手动实现分组。  
- **最容易踩的坑**：  
  - 忘记 **边界条件**（如 `30000` 和 `80000` 应该属于哪个区间），导致分类错误。  
  - 没有把 **所有三类都返回**，当某类计数为 0 时忘记输出，导致答案不符合“必须返回全部三类”。  
- **下次思路**：一看到“多分类计数”，立刻在脑中画出 **阈值划分图**，确认每个区间的左右闭合情况，然后 **写一个单遍历的计数框架**。这样可以快速得到最优实现。