# #2881. 创建新列 / Create a New Column

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/create-a-new-column/)

---

## 题目（英文原版）

**Description**

A company plans to provide its employees with a bonus.
Write a solution to create a new column name bonus that contains the doubled values of the salary column.
The result format is in the following example.

**Examples**

**Example 1:**

```
DataFrame employees
+-------------+--------+
| Column Name | Type.  |
+-------------+--------+
| name        | object |
| salary      | int.   |
+-------------+--------+
```

**Example 2:**

```
Input:
DataFrame employees
+---------+--------+
| name    | salary |
+---------+--------+
| Piper   | 4548   |
| Grace   | 28150  |
| Georgia | 1103   |
| Willow  | 6593   |
| Finn    | 74576  |
| Thomas  | 24433  |
+---------+--------+
Output:
+---------+--------+--------+
| name    | salary | bonus  |
+---------+--------+--------+
| Piper   | 4548   | 9096   |
| Grace   | 28150  | 56300  |
| Georgia | 1103   | 2206   |
| Willow  | 6593   | 13186  |
| Finn    | 74576  | 149152 |
| Thomas  | 24433  | 48866  |
+---------+--------+--------+
Explanation: 
A new column bonus is created by doubling the value in the column salary.
```

---

## 题目（中文翻译）

描述  
一家公司计划为其员工提供奖金。  
请编写解决方案，创建一个名为 **bonus** 的新列（column），其中的值为 **salary** 列（column）数值的两倍。  
结果格式请参考下面的示例。

**示例 1**  

DataFrame `employees`  

| Column Name | Type   |
|-------------|--------|
| name        | object |
| salary      | int    |

**示例 2**  

**输入**  
DataFrame `employees`  

| name    | salary |
|---------|--------|
| Piper   | 4548   |
| Grace   | 28150  |
| Georgia | 1103   |
| Willow  | 6593   |
| Finn    | 74576  |
| Thomas  | 24433  |

**输出**  

| name    | salary | bonus |
|---------|--------|-------|
| Piper   | 4548   | 9096  |
| Grace   | 28150  | 56300 |
| Georgia | 1103   | 2206  |
| Willow  | 6593   | 13186 |
| Finn    | 74576  | 149152|
| Thomas  | 24433  | 48866 |

约束条件  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把表格（`DataFrame`）看成一本电话簿，每一行就是一个人的记录。  
我们可以 **逐行遍历**（就像一本书一页页翻），把每个人的 `salary` 取出来乘以 2，随后把算好的结果放回到表格里，形成新的列 `bonus`。

- **使用的数据结构**  
  - `DataFrame`：类似 Excel 表格，行是记录，列是属性。  
  - `iterrows()`：把 `DataFrame` 按行拆开，像一次次抽出一张卡片，卡片里有 `(index, Series)`，`Series` 就相当于一行的字典，`key` 是列名，`value` 是对应的值。  
  - `apply()`：把一个函数“套”到每一行或每一列上，类似把同一把尺子一次次量每个人的工资。

- **为什么正确**  
  对每一行我们都准确地读取了 `salary`，算出了 `salary * 2`，再把结果写进同一行的新列 `bonus`，所以最终表格里每个人的 `bonus` 都是对应 `salary` 的两倍，满足题目要求。

- **时间/空间复杂度**  
  - **时间**：我们必须看（遍历）每一行一次，行数记作 `n`，所以时间是 `O(n)`。  
    这里的 `O(n)` 可以想象成“跑一圈”，如果有 1000 条记录，就要跑 1000 步。  
  - **空间**：只额外开辟了一个存放 `bonus` 列的空间，和原表格的规模同样是 `O(n)`，但因为这是在原表格上直接添加列，额外的“临时”空间几乎是常数 `O(1)`（只用来保存当前遍历的那一行）。

#### 代码（Python）

```python
import pandas as pd

def add_bonus_bruteforce(employees: pd.DataFrame) -> pd.DataFrame:
    """
    暴力解：逐行遍历，计算 bonus = salary * 2
    """
    # 为了不修改原始 DataFrame，先拷贝一份（可选）
    df = employees.copy()

    # 1) 使用 iterrows() 逐行遍历
    for idx, row in df.iterrows():
        # row['salary'] 就是当前行的工资
        bonus = row['salary'] * 2          # 计算 bonus
        df.at[idx, 'bonus'] = bonus        # 把 bonus 写回到对应的行

    # 2) 也可以用 apply()，效果类似
    # df['bonus'] = df.apply(lambda r: r['salary'] * 2, axis=1)

    return df
```

#### 复杂度

- **时间复杂度**：`O(n)` — 需要看每一行一次，`n` 是记录数。  
- **空间复杂度**：`O(1)`（不计返回的结果）— 只用了常数级的临时变量 `bonus`，额外空间几乎不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解出发，慢的地方其实不在遍历本身（`O(n)` 已经是最低），而在 **逐行访问的开销**：每取一次 `row['salary']`、每写一次 `df.at[...]` 都会产生 Python 层面的函数调用、对象包装等，导致实际运行时间比预期要慢。

**Pandas 的强项**是 **向量化运算**——一次性对整列数据做算术操作，底层会调用高效的 C/NumPy 实现，几乎没有 Python 循环的开销。  
因此我们直接把整列 `salary` 乘以 2，结果自动对应每一行，赋值给新列 `bonus` 即可。

- **核心概念：向量化**  
  把一整列看成一个大数组（`Series`），对它做 `* 2` 相当于把尺子一次性放在所有数字上，让它们同时“长大”。这就像在厨房一次性把所有面团都揉两倍，而不是一个一个手工揉。

- **实现步骤**  
  1. 读取整列 `salary`：`employees['salary']`（返回一个 `Series`）。  
  2. 对这个 `Series` 做乘法：`employees['salary'] * 2`（返回新的 `Series`，每个元素都是原来的两倍）。  
  3. 把结果直接赋给新列名 `bonus`：`employees['bonus'] = ...`。  

- **为什么最优**  
  整个过程只用了 **一次** 对列的遍历（内部是底层 C 实现），不产生额外的 Python 循环，时间常数因子大幅降低。

#### 代码（Python）

```python
import pandas as pd

def add_bonus_vectorized(employees: pd.DataFrame) -> pd.DataFrame:
    """
    最优解：直接使用向量化运算，一行代码完成
    """
    df = employees.copy()               # 复制避免修改原始数据（可选）
    df['bonus'] = df['salary'] * 2      # 向量化乘法，自动对应每一行
    return df
```

#### 复杂度

- **时间复杂度**：`O(n)` — 仍然要处理 `n` 条记录，但底层是一次性批量操作，实际运行更快。  
- **空间复杂度**：`O(1)`（不计返回的结果）— 只在原表格上添加一列，没有额外的临时存储。

---

## 心得

- **核心技巧**：利用 Pandas 的向量化操作（列级别的算术），避免显式循环。  
- **适用的题型**  
  1. **列之间的算术关系**（如 `price * quantity` 生成 `total`）。  
  2. **批量条件赋值**（`df['flag'] = (df['score'] > 60).astype(int)`）。  
  3. **列的函数变换**（`df['log_salary'] = np.log(df['salary'])`）。  
- **一句话总结**：**“把整列当作一个大向量一次性操作，速度快且代码简洁”。**

## 反思

- **第一反应**：看到“创建新列”，自然想到逐行遍历计算后再写回。  
- **最容易踩的坑**  
  - **忘记复制 DataFrame**：直接在原始 `employees` 上修改可能影响后续使用的输入数据。  
  - **列名拼写错误**：`df['salary']` 必须与原始列名完全一致，否则会报 `KeyError`。  
  - **数据类型不匹配**：如果 `salary` 不是数值型（比如字符串），直接乘 2 会报错，需要先转换类型。  
- **下次遇到同类题**，第一步应该想到：**“这是一列对另一列的纯数值映射吗？如果是，直接用向量化表达式”。**