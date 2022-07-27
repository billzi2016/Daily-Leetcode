# #1873. 计算特殊奖金 / Calculate Special Bonus

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/calculate-special-bonus/)

---

## 题目（英文原版）

**Description**

Table: Employees
Write a solution to calculate the bonus of each employee. The bonus of an employee is 100% of their salary if the ID of the employee is an odd number and the employee's name does not start with the character 'M'. The bonus of an employee is 0 otherwise.
Return the result table ordered by employee_id.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| employee_id | int     |
| name        | varchar |
| salary      | int     |
+-------------+---------+
employee_id is the primary key (column with unique values) for this table.
Each row of this table indicates the employee ID, employee name, and salary.
```

**Example 2:**

```
Input: 
Employees table:
+-------------+---------+--------+
| employee_id | name    | salary |
+-------------+---------+--------+
| 2           | Meir    | 3000   |
| 3           | Michael | 3800   |
| 7           | Addilyn | 7400   |
| 8           | Juan    | 6100   |
| 9           | Kannon  | 7700   |
+-------------+---------+--------+
Output: 
+-------------+-------+
| employee_id | bonus |
+-------------+-------+
| 2           | 0     |
| 3           | 0     |
| 7           | 7400  |
| 8           | 0     |
| 9           | 7700  |
+-------------+-------+
Explanation: 
The employees with IDs 2 and 8 get 0 bonus because they have an even employee_id.
The employee with ID 3 gets 0 bonus because their name starts with 'M'.
The rest of the employees get a 100% bonus.
```

---

## 题目（中文翻译）

**描述**  
表（Table）`Employees`  
编写一个查询来计算每位员工的奖金。若员工的 ID 为奇数（odd number）且员工姓名的首字符不是字符 `'M'`，则该员工的奖金为其工资的 100%；否则奖金为 0。返回的结果表需按 `employee_id` 排序。结果格式参照下例。

**示例 1**  

```text
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| employee_id | int     |
| name        | varchar |
| salary      | int     |
+-------------+---------+
```

`employee_id` 是该表的主键（primary key），即唯一值（unique values）的列。表中的每一行分别表示员工 ID、员工姓名和工资。

**示例 2**  

**输入**  
`Employees` 表：

```text
+-------------+--------+--------+
| employee_id | name   | salary |
+-------------+--------+--------+
| 2           | Meir   | 3000   |
| 3           | Michael| 3800   |
| 7           | Addilyn| 7400   |
| 8           | Juan   | 6100   |
| 9           | Kannon | 7700   |
+-------------+--------+--------+
```

**输出**  

```text
+-------------+-------+
| employee_id | bonus |
+-------------+-------+
| 3           | 3800  |
| 7           | 7400  |
| 9           | 7700  |
+-------------+-------+
```

**约束条件**  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **逐行遍历** 表中的每一条记录，按照题目给出的规则判断是否可以发放 100% 的工资作为奖金。  
- **遍历**：把 `Employees` 表想象成一本员工名录，用手指从上往下点每一行。  
- **判断**：  
  - “ID 为奇数” → `employee_id % 2 == 1`（奇数除以 2 余 1）。  
  - “名字不以 `M` 开头” → `not name.startswith('M')`（字符串的 `startswith` 方法就像字典里查找某个词的开头）。  
- **计算**：如果两条都满足，`bonus = salary`；否则 `bonus = 0`。  
- **收集结果**：把 `(employee_id, bonus)` 加入结果列表，最后按 `employee_id` 排序返回。

这个方法一定能得到正确答案，因为它 **完整检查了每一条记录**，没有遗漏任何可能的情况。

#### 代码（Python）

```python
# -------------------------------------------------
# 直觉解：逐行检查每个员工
# -------------------------------------------------
from typing import List, Tuple

def calculate_bonus_brute(employees: List[Tuple[int, str, int]]) -> List[Tuple[int, int]]:
    """
    employees: List[(employee_id, name, salary)]
    返回 List[(employee_id, bonus)]，按 employee_id 升序排列
    """
    result = []                         # 用来存放 (employee_id, bonus) 的临时列表
    for emp_id, name, salary in employees:
        # 条件1：ID 为奇数
        is_odd = (emp_id % 2 == 1)
        # 条件2：名字不以 M 开头（大小写敏感，题目默认大写 M）
        not_start_M = not name.startswith('M')
        # 同时满足两条则发放全额工资，否则发 0
        bonus = salary if (is_odd and not_start_M) else 0
        result.append((emp_id, bonus)) # 把本行的结果加入列表

    # 最后按照 employee_id 排序（因为输入不一定有序）
    result.sort(key=lambda x: x[0])
    return result


# ------------------- 示例运行 --------------------
if __name__ == "__main__":
    # 模拟题目中的 Employees 表
    sample = [
        (2, "Meir",    3000),
        (3, "Michael", 3800),
        (7, "Addilyn", 7400),
        (8, "Juan",    6100),
        (9, "Kannon",  7700),
    ]
    print(calculate_bonus_brute(sample))
    # 输出: [(2, 0), (3, 0), (7, 7400), (8, 0), (9, 7700)]
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  这里的 `n` 是员工人数。我们只遍历了一遍表，每条记录做了常数次判断（取余、字符串开头检查），所以整体耗时随员工数线性增长。  
  > **大白话**：如果有 10 条记录花 1 秒，100 条记录大约花 10 秒——正比关系。

- **空间复杂度**：`O(n)`（返回结果的空间）  
  额外的临时空间只有存放结果的列表，大小正好等于记录数。若不计输出本身，则是 `O(1)`（只用了常数个变量）。

---

### 2. 最优解

#### 思路  

对这道题来说，**暴力解已经是最优**（线性时间）。  
不过我们可以从「代码可读性」和「向量化」两个角度进一步提升：

1. **瓶颈分析**  
   - 暴力解唯一的「耗时」操作是逐条判断，已是 `O(n)`，不可能再更快（必须看每条记录才能决定奖金）。  
   - 只要我们把这些判断 **批量化**，可以减少 Python 循环的解释开销，让代码更简洁、更易维护。

2. **优化思路**  
   - 使用 **列表推导式**（list comprehension）一次性完成筛选和计算，底层仍是 `O(n)`，但代码更紧凑。  
   - 若数据量非常大且已经使用 **pandas**（类似数据库的 DataFrame），可以利用 **向量化运算**一次性对整列数据进行条件过滤，性能提升明显（因为底层是 C 实现）。

下面分别给出两种「更优」的实现方式：

- **实现 A**：纯 Python 列表推导式（适合面试中直接写代码）。  
- **实现 B**：使用 `pandas` 的向量化操作（如果你已经在用 DataFrame，速度更快）。

#### 代码（Python）

```python
# -------------------------------------------------
# 实现 A：列表推导式（代码更简洁，仍是 O(n)）
# -------------------------------------------------
from typing import List, Tuple

def calculate_bonus_opt_listcomp(employees: List[Tuple[int, str, int]]) -> List[Tuple[int, int]]:
    # 先把每条记录转成 (employee_id, bonus) 再排序
    result = sorted(
        [(emp_id,
          salary if (emp_id % 2 == 1 and not name.startswith('M')) else 0)
         for emp_id, name, salary in employees],
        key=lambda x: x[0]               # 按 employee_id 升序排列
    )
    return result


# -------------------------------------------------
# 实现 B：pandas 向量化（如果数据已是 DataFrame）
# -------------------------------------------------
import pandas as pd

def calculate_bonus_opt_pandas(df: pd.DataFrame) -> pd.DataFrame:
    """
    df 必须包含三列：employee_id, name, salary
    返回的 DataFrame 只保留 employee_id 与 bonus 两列，且已排序
    """
    # 条件1：employee_id 为奇数
    cond_odd = df['employee_id'] % 2 == 1
    # 条件2：name 不以 'M' 开头
    cond_not_M = ~df['name'].str.startswith('M')
    # 计算 bonus（布尔数组直接映射为 0/1，乘以 salary 得到全额或 0）
    df['bonus'] = df['salary'].where(cond_odd & cond_not_M, other=0)
    # 只保留需要的列并排序
    result = df[['employee_id', 'bonus']].sort_values('employee_id')
    return result


# ------------------- 示例运行 --------------------
if __name__ == "__main__":
    sample = [
        (2, "Meir",    3000),
        (3, "Michael", 3800),
        (7, "Addilyn", 7400),
        (8, "Juan",    6100),
        (9, "Kannon",  7700),
    ]

    print("列表推导式实现：")
    print(calculate_bonus_opt_listcomp(sample))

    print("\npandas 实现：")
    df = pd.DataFrame(sample, columns=['employee_id', 'name', 'salary'])
    print(calculate_bonus_opt_pandas(df))
```

#### 复杂度

- **时间复杂度**：`O(n)`（与暴力解相同）  
  只要遍历一次表格，条件判断仍是常数时间。向量化实现的实际运行时间更短，因为底层用了 C 加速，但在 **算法层面** 仍是线性。

- **空间复杂度**：`O(n)`（存放结果）  
  列表推导式直接生成一个新列表；pandas 会在内存里创建额外的列 `bonus`，同样是线性空间。

> **对比**：虽然时间复杂度没有下降，但向量化实现往往在大数据集上表现更好，代码也更易读。

---

## 心得

- **核心技巧**：**逐行筛选 + 条件判断**，以及 **利用列表推导式 / 向量化** 把代码写得更简洁。
- **适用的题型**  
  1. “根据某些属性对每行数据进行打标签”——如 `Employee` 表的 `salary_grade`。  
  2. “过滤并计算衍生列”——如订单表的 `discounted_price`。  
  3. “一次遍历完成统计或转换”——如字符串数组的 `length` 列。
- **一句话总结**：**只要能一次遍历完所有记录，就已经是最优解；关键在于把判断写得简洁、可读。**

---

## 反思

- **第一反应**：拿到题目，我立刻想到 “遍历每条记录，检查两个条件”。这正是最直接的思路。
- **最容易踩的坑**  
  - 忽略了 **大小写**：题目说名字以 `'M'` 开头，默认是大写；如果写成 `name.lower().startswith('m')` 会把 `'mike'` 错误算进去。  
  - **ID 为负数**：负数的奇偶性仍然遵循 `% 2` 的规则，代码已经兼容，但要注意不要把负号当成特殊情况。  
  - **返回顺序**：忘记按 `employee_id` 排序会导致答案不符合要求。
- **下次遇到同类题**，第一步应该先 **明确过滤条件**（奇偶、前缀、范围等），然后决定 **一次遍历还是分步处理**，最后确保 **结果排序** 正确。