# #2884. 修改列 / Modify Columns

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/modify-columns/)

---

## 题目（英文原版）

**Description**

A company intends to give its employees a pay rise.
Write a solution to modify the salary column by multiplying each salary by 2.
The result format is in the following example.

**Examples**

**Example 1:**

```
DataFrame employees
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| name        | object |
| salary      | int    |
+-------------+--------+
```

**Example 2:**

```
Input:
DataFrame employees
+---------+--------+
| name    | salary |
+---------+--------+
| Jack    | 19666  |
| Piper   | 74754  |
| Mia     | 62509  |
| Ulysses | 54866  |
+---------+--------+
Output:
+---------+--------+
| name    | salary |
+---------+--------+
| Jack    | 39332  |
| Piper   | 149508 |
| Mia     | 125018 |
| Ulysses | 109732 |
+---------+--------+
Explanation:
Every salary has been doubled.
```

---

## 题目（中文翻译）

公司计划给员工加薪。请编写一个解决方案，将 **salary 列** 中的每个工资乘以 2。结果格式参考下面的示例。

**示例 1**  

DataFrame **employees**  
+-------------+--------+  
| Column Name | Type   |  
+-------------+--------+  
| name        | object |  
| salary      | int    |  
+-------------+--------+

**示例 2**  

**Input:**  
DataFrame **employees**  
+---------+--------+  
| name    | salary |  
+---------+--------+  
| Jack    | 19666  |  
| Piper   | 74754  |  
| Mia     | 62509  |  
| Ulysses | 54866  |  
+---------+--------+

**Output:**  
+---------+--------+  
| name    | salary |  
+---------+--------+  
| Jack    | 39332  |  
| Piper   | 149508 |  
| Mia     | 125018 |  
| Ulysses | 109732 |  
+---------+--------+

**Explanation:**  
每个 salary 都已乘以 2。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把 **salary** 这一列的每一个数都取出来，乘以 2，再写回去。  
可以把 `DataFrame` 想象成一张 Excel 表格，`salary` 列就像是一列数字。  
我们把这列数字一个一个取出来（相当于逐行查看），做乘法后再放回原位。  

- **用到的数据结构**  
  - `pandas.DataFrame`：类似于二维数组或数据库表格，行对应记录，列对应属性。  
  - `Series`（`DataFrame` 的一列）：可以把它看成装有若干数字的 **列表**，每个元素都有一个 **索引**（就像字典的 key），所以我们可以用 `for i in range(len(df))` 按顺序访问。  

- **为什么正确**  
  - 我们没有改变行的顺序，只是把每个 `salary` 的值乘以 2，题目要求的正是“把每个工资翻倍”，所以必然得到正确答案。  

- **时间/空间复杂度**  
  - **时间复杂度**：我们需要遍历整列一次，对每个元素做一次乘法，遍历的次数正好等于员工人数 `n`，所以是 **O(n)**。  
    - 大白话：如果有 10 个人，就要算 10 次；如果有 1 000 000 个人，就要算 1 000 000 次，时间随人数线性增长。  
  - **空间复杂度**：只在原表上直接修改，没有额外申请和存放另一个同样大小的数组，只用了常数级别的临时变量（如循环计数器），所以是 **O(1)**。  

#### 代码（Python）  

```python
import pandas as pd

def increase_salary_bruteforce(employees: pd.DataFrame) -> pd.DataFrame:
    """
    暴力解：逐行遍历 salary 列，乘以 2 后写回去
    """
    # 为了不修改调用者传进来的原始 DataFrame，先拷贝一份
    df = employees.copy()

    # 逐行处理（i 是行索引）
    for i in range(len(df)):
        # 取出第 i 行的 salary，乘以 2
        original = df.loc[i, 'salary']          # 读取原始工资
        df.loc[i, 'salary'] = original * 2      # 写回翻倍后的工资

    return df
```

#### 复杂度  

- **时间复杂度**：O(n) — 随着员工数量线性增长。  
- **空间复杂度**：O(1) — 只用了常数级别的额外空间（复制的 DataFrame 不计入额外空间，因为题目本身需要返回一个新的表）。  

---  

### 2. 最优解  

#### 思路  

虽然上面的逐行循环已经是 **O(n)**，但它每次只操作单个元素，实际上 `pandas` 提供了 **向量化（vectorized）** 的操作，可以一次性把整列数据都算好再写回去。  

- **瓶颈在哪里？**  
  - 循环本身在 Python 解释器层面会有一定的开销（每次循环都要解释执行一次），即使整体仍是线性时间。  
- **优化思路**  
  - 利用 `Series` 本身支持的算术运算：`df['salary'] * 2` 会把整列看成一个向量，一次性完成所有乘法，底层由 C 实现，速度更快。  
- **核心工具：向量化运算**  
  - 类比：把每个人的工资装进一个装满数字的“盒子”，我们一次性把盒子里的所有数字都乘以 2，而不是一个一个取出来再放回。  
- **实现步骤**  
  1. 直接对 `salary` 列做乘法：`df['salary'] = df['salary'] * 2`。  
  2. 返回修改后的 DataFrame（同样可以先拷贝防止修改原始对象）。  

#### 代码（Python）  

```python
import pandas as pd

def increase_salary_optimal(employees: pd.DataFrame) -> pd.DataFrame:
    """
    最优解：利用 pandas 的向量化操作，一次性把 salary 列全部翻倍
    """
    # 为了不改动外部传进来的 DataFrame，先拷贝
    df = employees.copy()

    # 向量化乘法：一次性把整列乘以 2
    df['salary'] = df['salary'] * 2   # 这里的 * 是对整个 Series 做运算

    return df
```

#### 复杂度  

- **时间复杂度**：O(n) — 仍然需要对每个元素做一次乘法，只是底层用了更快的 C 实现，实际运行速度更快。  
  - 与暴力解相比，**常数因子更小**，所以在大数据量时明显更快。  
- **空间复杂度**：O(1) — 同样只在原表上原地修改，没有额外的线性空间开销。  

---  

## 心得  

- **核心技巧**：利用 `pandas` 的向量化（列级）运算，一次性对整列进行数学操作。  
- **适用的题型**：  
  1. 对 DataFrame 某列做统一的数值变换（如加、减、乘、除）。  
  2. 根据某列的条件批量修改另一列（使用布尔索引）。  
  3. 对多列同时做算术或函数映射（如 `df[['a','b']].apply(np.log)`）。  
- **一句话总结**：**“列是向量，直接对向量做运算”**——不必循环，用一次性算子即可完成批量修改。  

## 反思  

- **第一反应**：拿起键盘就想写 `for` 循环，一行行处理。  
- **最容易踩的坑**  
  - 忘记拷贝原始 DataFrame，导致调用者的输入被意外修改。  
  - 对空 DataFrame 或缺少 `salary` 列的情况没有提前检查，会抛出 `KeyError`。  
- **下次类似题的第一步**：先思考“这是不是可以一次性对整列做运算”，如果答案是 Yes，就直接写向量化表达式；如果有条件筛选，再考虑布尔索引或 `apply`。