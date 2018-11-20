# #176. 第二高的工资 / Second Highest Salary

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/second-highest-salary/)

---

## 题目（英文原版）

**Description**

Table: Employee
Write a solution to find the second highest distinct salary from the Employee table. If there is no second highest salary, return null (return None in Pandas).
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| salary      | int  |
+-------------+------+
id is the primary key (column with unique values) for this table.
Each row of this table contains information about the salary of an employee.
```

**Example 2:**

```
Input: 
Employee table:
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
Output: 
+---------------------+
| SecondHighestSalary |
+---------------------+
| 200                 |
+---------------------+
```

**Example 3:**

```
Input: 
Employee table:
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
+----+--------+
Output: 
+---------------------+
| SecondHighestSalary |
+---------------------+
| null                |
+---------------------+
```

---

## 题目（中文翻译）

编写一个查询，找出 **Employee** 表中第二高的不同工资（distinct salary）。如果不存在第二高的工资，返回 `null`（在 Pandas 中返回 `None`）。

结果格式参照下面的示例。

### 示例 1  
**表结构**  

| Column Name | Type |
|-------------|------|
| id          | int  |
| salary      | int  |

- `id` 是该表的主键（具有唯一值的列）。  
- 表中的每一行记录了员工的工资信息。

### 示例 2  
**输入**  

Employee 表：

| id | salary |
|----|--------|
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |

**输出**  

| SecondHighestSalary |
|---------------------|
| 200                 |

### 示例 3  
**输入**  

Employee 表：

| id | salary |
|----|--------|
| 1  | 100    |

**输出**  

| SecondHighestSalary |
|---------------------|
| null                |

**约束条件**  
无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**把每个人的工资都拿出来，两两比较**，找出所有工资中排第二大的那一个。  

- **用到的数据结构**：  
  - `list`：把表格里的 `salary` 列全部取出来，放进一个普通的 Python 列表。可以把列表想象成装钱的零钱罐，里面每个元素就是一张工资单。  
- **为什么正确**：  
  - 只要我们把所有工资都列出来，然后对每个工资 `x` 检查它是否恰好比 **其他** 工资多一个（即有且仅有一个工资比它大），那么 `x` 必然是第二高的工资。  
- **时间/空间复杂度**：  
  - **时间**：我们要对每个工资 `x` 再遍历一次所有工资去计数，比对次数是 `n × n`，这里的 `n` 是员工人数。用大写的 **O(n²)** 表示，意思是“随着员工数的增加，运算次数会呈二次方增长”。如果员工有 1000 人，运算次数大约是 1,000,000 次。  
  - **空间**：只需要额外保存一个长度为 `n` 的列表，空间复杂度是 **O(n)**，即“和员工数成正比”。  

#### 代码（Python）  

```python
def second_highest_brute(employee):
    """
    暴力解法：两层循环找第二高工资
    :param employee: List[Tuple[int, int]]   # (id, salary)
    :return: int or None   # 第二高工资或 None
    """
    # 1. 把所有工资取出来放进列表
    salaries = [sal for _, sal in employee]          # 只关心 salary 列

    # 2. 用集合去重（因为要求“不同的工资”）
    distinct = list(set(salaries))                   # 去重后再转回列表

    # 3. 暴力遍历每个工资，统计比它大的有多少个
    second = None
    for x in distinct:                               # 外层循环每个候选工资
        higher_cnt = 0                               # 记录比 x 大的工资个数
        for y in distinct:                           # 内层循环与所有工资比较
            if y > x:
                higher_cnt += 1
        # 如果恰好有且只有一个工资比 x 大，说明 x 是第二高
        if higher_cnt == 1:
            second = x
            break                                     # 找到后可以直接退出

    return second
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 两层循环导致比较次数随员工数的平方增长。  
- **空间复杂度**：`O(n)` —— 需要存放所有工资的列表（以及去重后的集合）。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看出，**慢的地方在于两层循环的重复比较**。我们其实不需要把每个工资都和所有工资比较，只要**一次遍历就能知道最大和第二大的两个不同工资**。  

优化思路如下：

1. **一次遍历**：用两个变量 `first`、`second` 分别记录当前看到的最高工资和次高工资。  
2. **去重**：如果出现相同的工资，只保留第一次出现的即可（因为题目要求“不同的工资”）。可以用一个 `set` 记录已经见过的工资。  
3. **更新规则**：遍历每个工资 `s`（且 `s` 未出现过）时  
   - 若 `s` 大于 `first`：`second = first`，`first = s`（最高工资被刷新，原来的最高就成了次高）。  
   - 否则若 `s` 大于 `second`：`second = s`（只更新次高）。  
4. 最后 `second` 若仍为 `None`，说明不存在第二高工资，直接返回 `None`。  

> **类比**：把所有工资想象成一条跑道上的选手，`first` 是当前跑得最快的选手，`second` 是跑第二快的选手。每当有新选手出现时，只要看他跑得是不是比第一名快，或者比第二名快，就可以即时更新名次，而不必把所有选手重新排一次。

#### 代码（Python）  

```python
def second_highest_optimal(employee):
    """
    最优解：一次遍历求第二高工资
    :param employee: List[Tuple[int, int]]   # (id, salary)
    :return: int or None   # 第二高工资或 None
    """
    seen = set()          # 用来去重，记录已经处理过的工资
    first = None          # 最高工资
    second = None         # 次高工资

    for _, sal in employee:
        if sal in seen:               # 已经见过的相同工资直接跳过
            continue
        seen.add(sal)

        if first is None or sal > first:
            # 当前工资比最高的还大，原来的最高变成次高
            second = first
            first = sal
        elif second is None or sal > second:
            # 不是最高，但比次高大，更新次高
            second = sal

    return second                     # 若 second 仍为 None，说明不存在第二高
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次员工列表，每个工资只做常数次比较。相比暴力的 `O(n²)`，速度提升明显。  
- **空间复杂度**：`O(k)` —— `k` 是不同工资的数量（最坏情况下等于 `n`），用来存放 `seen` 集合。相较于暴力的 `O(n)`，额外的集合并不会改变数量级。  

---  

## 心得  

- **核心技巧**：一次遍历维护**最大值和次大值**（或前 K 大），并配合**哈希集合去重**。  
- **适用的题型**：  
  1. “找第 K 大/小的元素”（如第 3 大的成绩）。  
  2. “求数组中不重复的最大/最小值”。  
  3. “在流中实时输出前 K 大元素”（可以使用堆结构进一步推广）。  
- **一句话总结解题钥匙**：**“只保留必要的状态（最大、次大），不必重复比较全部元素”。**  

---  

## 反思  

- **第一反应**：看到“第二高工资”，立刻想到把工资全部排序后取倒数第二个。虽然可行，但排序的时间是 `O(n log n)`，并不是最优。  
- **最容易踩的坑**：  
  - **重复工资**：如果有多个员工工资相同，直接取倒数第二会得到错误答案，需要先去重。  
  - **只有一个不同工资**：此时应该返回 `None` 而不是把最高工资当作第二高。  
  - **空表**：若员工表为空，也应返回 `None`，代码里 `first`、`second` 初始为 `None` 能自然处理。  
- **下次遇到同类题**：第一步先**思考是否可以一次遍历维护所需的前几名**，而不是先排序或双层循环。这样往往能直接得到 `O(n)` 的最优解。