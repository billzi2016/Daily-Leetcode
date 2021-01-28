# #1179. 重新格式化 Department 表 / Reformat Department Table

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/reformat-department-table/)

---

## 题目（英文原版）

**Description**

Table: Department
Reformat the table such that there is a department id column and a revenue column for each month.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| revenue     | int     |
| month       | varchar |
+-------------+---------+
In SQL,(id, month) is the primary key of this table.
The table has information about the revenue of each department per month.
The month has values in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].
```

**Example 2:**

```
Input: 
Department table:
+------+---------+-------+
| id   | revenue | month |
+------+---------+-------+
| 1    | 8000    | Jan   |
| 2    | 9000    | Jan   |
| 3    | 10000   | Feb   |
| 1    | 7000    | Feb   |
| 1    | 6000    | Mar   |
+------+---------+-------+
Output: 
+------+-------------+-------------+-------------+-----+-------------+
| id   | Jan_Revenue | Feb_Revenue | Mar_Revenue | ... | Dec_Revenue |
+------+-------------+-------------+-------------+-----+-------------+
| 1    | 8000        | 7000        | 6000        | ... | null        |
| 2    | 9000        | null        | null        | ... | null        |
| 3    | null        | 10000       | null        | ... | null        |
+------+-------------+-------------+-------------+-----+-------------+
Explanation: The revenue from Apr to Dec is null.
Note that the result table has 13 columns (1 for the department id + 12 for the months).
```

---

## 题目（中文翻译）

描述  
表：Department  
重新排列表，使每个月都有一个部门 **id** 列和一个收入（revenue）列。  
返回结果表，顺序不限。  
结果格式参见下面示例。

**示例 1**  

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| revenue     | int     |
| month       | varchar |
+-------------+---------+
```

在 SQL 中，`(id, month)` 是该表的主键 (primary key)。  
该表包含每个部门每个月的收入信息。  
`month` 列的取值为 `["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov", ...]`。

**示例 2**  

**输入**  

```
Department 表:
+------+---------+-------+
| id   | revenue | month |
+------+---------+-------+
| 1    | 8000    | Jan   |
| 2    | 9000    | Jan   |
| 3    | 10000   | Feb   |
| 1    | 7000    | Feb   |
| 1    | 6000    | Mar   |
+------+---------+-------+
```

**输出**  

```
+------+-------------+-------------+-------------+-----+-------------+
| id   | Jan_Revenue | Feb_Revenue | Mar_Revenue | ... |
+------+-------------+-------------+-------------+-----+-------------+
```

约束条件  
无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

我们把原始表看成 **一堆纸条**，每张纸条上写着 `(部门 id, 收入, 月份)`。  
要把它们“重新排版”，让每个部门占一行、每个月的收入占一列，就相当于：

1. **把纸条按照部门 id 分组**（把同一个部门的所有纸条放进同一个抽屉）。  
2. **把抽屉里的纸条再按照月份摆好顺序**，把收入写进对应的格子。  

在编程里，**字典**（`dict`）就像一个 **查字典**：  
- `key` 是部门 id，`value` 是「该部门所有月份的收入」这张小表。  
- 小表本身我们再用另一个字典来保存，`month -> revenue`。  

只要遍历一遍原始数据，就能把所有信息收集完。  
随后再遍历收集好的字典，把每个部门的收入按月写出来，就是我们想要的结果。

> **为什么这样一定能得到正确答案？**  
> 因为我们没有遗漏任何一张纸条，也没有对同一个 `(id, month)` 写入两次——题目说 `(id, month)` 是主键，保证唯一性。  

**时间/空间复杂度**（大白话）  
- **时间**：我们只走了一遍原始表（`O(N)`），再走了一遍部门集合（`O(D)`），`N` 是总记录数，`D` 是部门数。总体仍是线性 `O(N)`。  
- **空间**：需要保存每个部门每个月的收入，最坏情况是每条记录都不重复，空间是 `O(N)`。

#### 代码（Python）  

```python
from typing import List, Dict, Tuple

def reformat_department_bruteforce(records: List[Tuple[int, int, str]]) -> List[Dict]:
    """
    暴力实现：把 (id, revenue, month) 的列表转换为透视表。
    参数 records 示例:
        [(1, 8000, "Jan"), (2, 9000, "Jan"), (3, 10000, "Feb"), ...]
    返回值示例:
        [
            {"id": 1, "Jan_Revenue": 8000, "Feb_Revenue": 7000, "Mar_Revenue": 6000},
            {"id": 2, "Jan_Revenue": 9000},
            ...
        ]
    """
    # 1. 收集所有出现过的月份，后面要用来决定列的顺序
    months = set()
    # 2. 先把数据按部门 id 分组，每个部门内部再用 month -> revenue 保存
    dept_dict: Dict[int, Dict[str, int]] = {}

    for dept_id, revenue, month in records:
        months.add(month)                         # 记录出现过的月份
        if dept_id not in dept_dict:              # 第一次遇到这个部门，创建小表
            dept_dict[dept_id] = {}
        dept_dict[dept_id][month] = revenue       # 把收入写进对应的月份格子

    # 把月份按字典序排好，这样输出的列顺序更可预测
    sorted_months = sorted(months)

    # 3. 把收集好的信息重新组装成题目要求的列表形式
    result = []
    for dept_id, month_rev in dept_dict.items():
        row = {"id": dept_id}
        for m in sorted_months:
            # 只在该部门有该月份收入时才写入列
            if m in month_rev:
                row[f"{m}_Revenue"] = month_rev[m]
        result.append(row)

    return result


# ---------- 示例运行 ----------
if __name__ == "__main__":
    sample = [
        (1, 8000, "Jan"),
        (2, 9000, "Jan"),
        (3, 10000, "Feb"),
        (1, 7000, "Feb"),
        (1, 6000, "Mar"),
    ]
    for r in reformat_department_bruteforce(sample):
        print(r)
```

**关键注释**  
- `months.add(month)`：把出现过的月份收集起来，好像把所有可能的列先记下来。  
- `dept_dict[dept_id][month] = revenue`：把收入塞进「部门抽屉」里的「月份格子」。  
- `sorted_months = sorted(months)`：把列的顺序排好，等会儿遍历时就能按顺序写。  

#### 复杂度  

- **时间复杂度**：`O(N)`  
  - 只遍历了一遍原始记录 `N` 次，随后再遍历部门数（最多 `N`）和月份数（最多 12），整体仍是线性。  
- **空间复杂度**：`O(N)`  
  - 需要保存每条记录对应的 `(id, month) -> revenue`，最坏情况下占用和原表同样多的空间。  

---  

### 2. 最优解  

#### 思路  

暴力解已经是 **线性** 的，理论上已经很快了。  
不过我们可以把实现写得更简洁、更“Pythonic”，同时把 **月份的顺序** 固定为题目常见的自然月顺序（Jan → Dec），而不是字典序。  

**优化点**  
1. **一次遍历同时完成两件事**：  
   - 收集部门信息。  
   - 收集出现的月份（如果想保持自然月顺序，只需要固定一个月份列表即可）。  
2. **使用 `defaultdict`**：可以省去 “如果部门不存在就先创建空字典” 的判断，代码更简洁。  
3. **直接构造输出行**：在遍历完所有记录后，按固定的月份顺序一次性生成每一行，而不是再遍历一次 `sorted_months`。  

**核心工具**  
- `collections.defaultdict`：相当于“自动帮你开抽屉”的字典。  
- **列表** `MONTH_ORDER = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]`：把月份当成固定的列顺序。  

**类比**：想象我们在排班表上填写员工的工作时间，`defaultdict` 就像一张自动扩展的表格，遇到新员工会自动给他一行空白，省去我们手动创建的麻烦。

#### 代码（Python）  

```python
from collections import defaultdict
from typing import List, Tuple, Dict

MONTH_ORDER = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]

def reformat_department_optimal(records: List[Tuple[int, int, str]]) -> List[Dict]:
    """
    最优实现：一次遍历完成分组 + 按自然月顺序输出。
    """
    # dept_month_rev[dept_id][month] = revenue
    dept_month_rev: Dict[int, Dict[str, int]] = defaultdict(dict)

    for dept_id, revenue, month in records:
        dept_month_rev[dept_id][month] = revenue   # 自动创建内部字典

    # 把收集好的数据转成题目要求的列表
    result = []
    for dept_id, month_map in dept_month_rev.items():
        row = {"id": dept_id}
        for m in MONTH_ORDER:                     # 按自然月顺序遍历
            if m in month_map:                    # 只输出该部门实际拥有的月份列
                row[f"{m}_Revenue"] = month_map[m]
        result.append(row)

    return result


# ---------- 示例运行 ----------
if __name__ == "__main__":
    sample = [
        (1, 8000, "Jan"),
        (2, 9000, "Jan"),
        (3, 10000, "Feb"),
        (1, 7000, "Feb"),
        (1, 6000, "Mar"),
    ]
    for r in reformat_department_optimal(sample):
        print(r)
```

**关键注释**  
- `defaultdict(dict)`：不需要先判断 `dept_id` 是否已经存在，直接写入就行。  
- `for m in MONTH_ORDER`：固定的月份顺序，输出时自然会得到 `Jan_Revenue、Feb_Revenue …`。  

#### 复杂度  

- **时间复杂度**：`O(N)`  
  - 只遍历一次原始记录 `N` 次，随后遍历部门数 `D`（`D ≤ N`）和固定的 12 个月，仍是线性。  
- **空间复杂度**：`O(N)`  
  - 与暴力解相同，需要保存每条记录的映射关系。  

相比暴力实现，最优解在 **代码可读性** 与 **常数因子** 上更好——省去排序、额外的 `set`，直接使用固定的月份顺序。  

---  

## 心得  

- **核心技巧**：**分组 + 透视（Pivot）**。先把数据按照某个维度（这里是 `id`）聚合到一起，再把另一维度（`month`）展开成列。  
- **适用的题型**（类似技巧）  
  1. “按用户统计每个月的消费” → 需要把用户 → 月份 → 消费额透视成表格。  
  2. “将考试成绩从长表转宽表” → 学生 → 科目 → 分数。  
  3. “统计每种商品在每个仓库的库存” → 商品 → 仓库 → 库存量。  
- **一句话总结解题钥匙**：**先把相同主键的记录收集到一个字典里，再按列的顺序把字典展开成行**。  

---  

## 反思  

- **第一反应**：看到“重新排版（reformat）”，立刻想到把行转列（pivot），于是想到使用字典分组。  
- **最容易踩的坑**  
  - 忘记处理 **缺失的月份**：如果某部门在某个月没有记录，输出时不应该出现 `None`，而是直接省略该列。  
  - 月份顺序不一致：直接使用 `sorted(months)` 会得到字母顺序（`Apr, Aug, ...`），不符合自然月的阅读习惯。  
  - 主键冲突：如果数据中出现相同 `(id, month)` 两次，后写的会覆盖前面的，实际业务可能需要累加，这里题目已保证唯一性。  
- **下次类似题的第一步**：先 **列举出两层维度**（分组键 与 要展开的键），然后决定用 **字典套字典** 或 `defaultdict` 来收集，再按固定顺序输出。