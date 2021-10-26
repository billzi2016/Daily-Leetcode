# #1527. 患者的病症 / Patients With a Condition

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/patients-with-a-condition/)

---

## 题目（英文原版）

**Description**

Table: Patients
Write a solution to find the patient_id, patient_name, and conditions of the patients who have Type I Diabetes. Type I Diabetes always starts with DIAB1 prefix.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| patient_id   | int     |
| patient_name | varchar |
| conditions   | varchar |
+--------------+---------+
patient_id is the primary key (column with unique values) for this table.
'conditions' contains 0 or more code separated by spaces. 
This table contains information of the patients in the hospital.
```

**Example 2:**

```
Input: 
Patients table:
+------------+--------------+--------------+
| patient_id | patient_name | conditions   |
+------------+--------------+--------------+
| 1          | Daniel       | YFEV COUGH   |
| 2          | Alice        |              |
| 3          | Bob          | DIAB100 MYOP |
| 4          | George       | ACNE DIAB100 |
| 5          | Alain        | DIAB201      |
+------------+--------------+--------------+
Output: 
+------------+--------------+--------------+
| patient_id | patient_name | conditions   |
+------------+--------------+--------------+
| 3          | Bob          | DIAB100 MYOP |
| 4          | George       | ACNE DIAB100 | 
+------------+--------------+--------------+
Explanation: Bob and George both have a condition that starts with DIAB1.
```

---

## 题目（中文翻译）

**描述**  
表：`Patients`  
编写一个查询，找出 **conditions**（病症）中以 `DIAB1` 前缀开头的患者的 `patient_id`、`patient_name` 和 `conditions`。  
返回结果表，顺序不限。  

**结果格式** 参见下例。

**示例 1**  

| Column Name  | Type    |
|--------------|---------|
| patient_id   | int     |
| patient_name | varchar |
| conditions   | varchar |

`patient_id` 是该表的 **primary key**（主键），即唯一值的列。  
`conditions` 包含 0 条或多条代码（code），代码之间用空格分隔。  
该表记录了医院中患者的信息。

**示例 2**  

**输入**  

`Patients` 表：

| patient_id | patient_name | conditions   |
|------------|--------------|--------------|
| 1          | Daniel       | YFEV COUGH   |
| 2          | Alice        |              |
| 3          | Bob          | DIAB100 MYOP |
| 4          | George       | ACNE DIAB100 |
| 5          | Alain        | DIAB201      |
| ...        | ...          | ...          |

**输出**  

（此处省略，保持原样）

**约束条件**  
无。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

这道题本质上是 **在一张表里挑出满足特定条件的行**。  
每一行的 `conditions` 列是若干个疾病代码，用空格分隔，例如  
`"DIAB100 MYOP"` → `["DIAB100", "MYOP"]`。  

> **生活化类比**：把 `conditions` 看成一本书的目录，目录里每个章节都有一个编号（代码）。我们要找的患者，就是目录里出现 **以 “DIAB1” 开头的章节**（即 Type I Diabetes）的那几位。  

最直接的做法就是：

1. 逐行遍历 `Patients` 表（相当于一行行读纸质记录）。  
2. 把 `conditions` 按空格切成列表。  
3. 检查列表中是否有任意一个代码 `startswith('DIAB1')`。  
4. 若满足条件，就把 `patient_id、patient_name、conditions` 加入答案。

这种做法不需要任何高级数据结构，只用 **循环 + 字符串分割 + 前缀匹配**，所以称为“暴力”。  

- **正确性**：只要遍历到了所有记录，并且对每条记录的每个代码都检查了前缀，就一定不会漏掉符合条件的患者。  
- **时间复杂度**：设表中有 `n` 条记录，每条记录的 `conditions` 最多有 `m` 个代码（`m` 取决于实际数据），则总的比较次数是 `n × m`，记作 **O(n·m)**。  
  - 大白话：如果有 1000 条患者，每人平均有 5 个代码，最多要检查 5000 次。  
- **空间复杂度**：我们只用常数级的额外变量（循环计数器、临时列表），所以是 **O(1)**（不计答案本身的存储）。

#### 代码（Python）  

```python
# 假设 patients 是从数据库读取的列表，每条记录是字典
# 示例：
# patients = [
#     {"patient_id": 1, "patient_name": "Daniel", "conditions": "YFEV COUGH"},
#     {"patient_id": 2, "patient_name": "Alice",   "conditions": ""},
#     {"patient_id": 3, "patient_name": "Bob",     "conditions": "DIAB100 MYOP"},
#     {"patient_id": 4, "patient_name": "George",  "conditions": "ACNE DIAB100"},
#     {"patient_id": 5, "patient_name": "Alain",   "conditions": "DIAB201"},
# ]

def brute_force(patients):
    """暴力遍历，找出所有 conditions 中含有前缀 DIAB1 的患者"""
    ans = []                     # 用来保存结果
    for row in patients:        # 逐行遍历表
        # 把 conditions 按空格切成代码列表，空字符串会得到 []，不会报错
        codes = row["conditions"].split()
        # 检查是否有任意代码以 DIAB1 开头
        has_type1 = any(code.startswith("DIAB1") for code in codes)
        if has_type1:            # 满足条件 → 加入答案
            ans.append({
                "patient_id":   row["patient_id"],
                "patient_name": row["patient_name"],
                "conditions":   row["conditions"]
            })
    return ans
```

#### 复杂度  

- **时间复杂度**：O(n·m)  
  - n 为患者数量，m 为每位患者 `conditions` 中代码的平均个数。  
  - 直观来说，就是“每个人的每个代码都要检查一次”。  
- **空间复杂度**：O(1)（不计返回结果的空间）  
  - 只用了几个临时变量，和输入规模无关。

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于对每条记录都要先 `split()` 再遍历所有代码。  
如果我们能够一次性判断整条 `conditions` 字符串是否包含 **以 DIAB1 开头的完整代码**，就可以省掉 `split` 和内部循环。

**关键点**：  
- 代码之间用空格分隔，且每个代码都是完整的词。  
- “以 DIAB1 开头的代码” 等价于 **“空格或字符串开头后紧跟 DIAB1”**。  

这正好可以用 **正则表达式**（regular expression）一次性匹配：

```
(^| )DIAB1\w*
```

解释：  
- `^| ` 表示“行首或前面是空格”。  
- `DIAB1` 是我们要找的前缀。  
- `\w*` 表示后面可以跟任意字母/数字（即代码的其余部分），但必须是同一个词。

使用正则的好处是：

1. **只遍历一次字符串**（底层已经实现了高效的线性扫描）。  
2. **不需要额外的列表分割**，节省了临时对象的创建。  
3. 在 Python 中，`re.search` 已经是 C 实现，速度快于纯 Python 循环。

因此，最优解的思路是：

- 对每行记录直接在 `conditions` 字符串上跑正则搜索。  
- 若匹配成功，即可把该行加入答案。

**时间复杂度**：仍然是 O(n·L)，其中 L 为单条 `conditions` 字符串的长度。  
相比暴力解的 O(n·m)（m 为代码数量），这里的 L 与 m 成正比，但因为一次遍历即可，常数更小，实际运行更快。  

**空间复杂度**：O(1)（只保存正则对象和临时变量）。

#### 代码（Python）  

```python
import re

# 预编译正则，提高循环内部的效率
# (^| ) 表示字符串开头或前面是空格
# DIAB1 表示我们要的前缀
# \w* 表示后面可以有任意字母/数字（代码的其余部分）
PATTERN = re.compile(r'(^| )DIAB1\w*')

def optimal(patients):
    """使用正则一次匹配，找出所有患有 Type I Diabetes（DIAB1 前缀）的患者"""
    ans = []
    for row in patients:
        # re.search 在整个字符串里寻找满足模式的子串
        if PATTERN.search(row["conditions"]):
            ans.append({
                "patient_id":   row["patient_id"],
                "patient_name": row["patient_name"],
                "conditions":   row["conditions"]
            })
    return ans
```

#### 复杂度  

- **时间复杂度**：O(n·L)  
  - `n` 为患者条数，`L` 为单条 `conditions` 字符串的长度。  
  - 直观上是“每条记录只扫描一次”。  
- **空间复杂度**：O(1)（不计返回列表）  
  - 只用了一个预编译好的正则对象，大小固定。

---

## 心得  

- **核心技巧**：利用 **正则表达式** 实现“单词前缀匹配”，一次性判断整行字符串是否包含目标代码。  
- **适用场景**：  
  1. **字符串中出现特定前缀/后缀的过滤**（如搜索包含特定标签的日志行）。  
  2. **SQL/数据库查询里用 `LIKE '%DIAB1%'` 并结合空格边界**（可以写成 `REGEXP '^DIAB1| DIAB1'`）。  
  3. **文本处理任务**，需要一次性找出满足词边界条件的词汇。  
- **一句话总结**：**“把‘逐码检查’交给正则，让它一次遍历搞定前缀匹配”。**

---

## 反思  

- **第一反应**：直接把 `conditions` 用空格拆成列表，然后遍历检查 `startswith('DIAB1')`。这在脑中最容易想到，也是最直观的做法。  
- **最容易踩的坑**：  
  - `conditions` 可能为空字符串，`split()` 会得到空列表，需要防止 `IndexError`。  
  - 代码之间仅用空格分隔，若出现多余空格（如 `"DIAB100  ACNE"`），直接 `split()` 仍能正常工作，但正则要确保匹配空格或行首。  
  - 使用 `LIKE '%DIAB1%'` 时会误匹配 `XDIAB123`（前面有其他字符），所以必须加上空格或行首的边界。  
- **下次思路**：面对“在一段由分隔符分开的字符串里查找满足某种模式的子串”，第一步先考虑 **正则一次匹配**，再判断是否真的需要拆分成列表。这样往往能把时间常数降到最低。