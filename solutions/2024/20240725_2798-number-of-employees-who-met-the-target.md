# #2798. 满足目标的员工数量 / Number of Employees Who Met the Target

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/number-of-employees-who-met-the-target/)

---

## 题目（英文原版）

**Description**

There are n employees in a company, numbered from 0 to n - 1. Each employee i has worked for hours[i] hours in the company.
The company requires each employee to work for at least target hours.
You are given a 0-indexed array of non-negative integers hours of length n and a non-negative integer target.
Return the integer denoting the number of employees who worked at least target hours.

**Examples**

**Example 1:**

```
Input: hours = [0,1,2,3,4], target = 2
Output: 3
Explanation: The company wants each employee to work for at least 2 hours.
- Employee 0 worked for 0 hours and didn't meet the target.
- Employee 1 worked for 1 hours and didn't meet the target.
- Employee 2 worked for 2 hours and met the target.
- Employee 3 worked for 3 hours and met the target.
- Employee 4 worked for 4 hours and met the target.
There are 3 employees who met the target.
```

**Example 2:**

```
Input: hours = [5,1,4,2,2], target = 6
Output: 0
Explanation: The company wants each employee to work for at least 6 hours.
There are 0 employees who met the target.
```

**Constraints**

- 1 <= n == hours.length <= 50
- 0 <= hours[i], target <= 105

---

## 题目（中文翻译）

有 `n` 名员工在公司工作，编号从 `0` 到 `n - 1`。第 `i` 名员工在公司工作了 `hours[i]` 小时。公司要求每位员工的工作时长至少为 `target` 小时。  
给定一个长度为 `n` 的非负整数数组 `hours`（工作时长）以及一个非负整数 `target`（目标时长），返回工作时长 **不少于** `target` 小时的员工数量。

**示例 1**  
**输入**: `hours = [0,1,2,3,4]`, `target = 2`  
**输出**: `3`  
**解释**: 公司要求每位员工至少工作 `2` 小时。  
- 员工 0 工作了 `0` 小时，未达标。  
- 员工 1 工作了 `1` 小时，未达标。  
- 员工 2 工作了 `2` 小时，达标。  
- 员工 3 工作了 `3` 小时，达标。  
- 员工 4 工作了 `4` 小时，达标。  

**示例 2**  
**输入**: `hours = [5,1,4,2,2]`, `target = 6`  
**输出**: `0`  
**解释**: 公司要求每位员工至少工作 `6` 小时。没有员工达标。

**约束条件**  
- `1 <= n == hours.length <= 50`  
- `0 <= hours[i], target <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有员工的工作时长一个一个看一遍，看看它们是否 **大于等于** `target`。  
- **用到的数据结构**：只有一个普通的 Python 列表 `hours`，它就像一本装有所有员工工作时长的“成绩单”。我们只需要把这本成绩单翻开，逐行检查每个成绩是否达标。  
- **为什么正确**：题目只要求统计满足条件的员工人数，而不是找出具体的员工或做更复杂的统计。只要遍历所有元素并计数，必然得到正确答案。  
- **时间/空间复杂度**：遍历一次数组，需要 **O(n)** 的时间（`n` 是员工人数），空间只用了几个计数变量，**O(1)** 的额外空间。  
  - 大白话解释：如果有 50 名员工，最多只会检查 50 次，每次检查只花一点点时间，整体花的时间和员工人数是成正比的。空间上我们只需要一个计数器和循环变量，和员工人数无关。

#### 代码（Python）

```python
def number_of_employees(hours, target):
    """
    统计工作时长不少于 target 的员工人数
    :param hours: List[int]，每个员工的工作时长
    :param target: int，目标时长
    :return: int，满足条件的员工数量
    """
    count = 0                     # 用来累计满足条件的员工数
    for h in hours:               # 逐个遍历每位员工的工作时长
        if h >= target:           # 如果该员工的时长 >= 目标时长
            count += 1            # 计数器加一
    return count
```

#### 复杂度

- **时间复杂度**：`O(n)` — 需要遍历一次长度为 `n` 的数组，遍历一次就能得到答案。
- **空间复杂度**：`O(1)` — 只用了常数个额外变量（`count`、循环变量 `h`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解来看，唯一的耗时操作是 **遍历数组**。因为题目本身只需要一次遍历就能得到答案，已经达到了时间上的下界（必须看每个元素一次），不存在进一步的加速空间。  
我们可以把实现写得更简洁、更“Pythonic”，比如使用列表推导式或 `sum` 与布尔值的特性：

- `h >= target` 的结果是 `True` 或 `False`，在数值运算中会被当作 `1` 或 `0`。  
- `sum(h >= target for h in hours)` 就等价于把所有 `True`（满足条件）累加，得到满足条件的员工数。  

这并没有改变时间复杂度，只是让代码更紧凑、更易读。

#### 代码（Python）

```python
def number_of_employees_opt(hours, target):
    """
    最简洁的实现：利用布尔值可直接参与加法的特性
    """
    # 对每个员工的时长与目标比较，True 当作 1 累加，得到满足条件的总数
    return sum(h >= target for h in hours)
```

#### 复杂度

- **时间复杂度**：`O(n)` — 仍然需要遍历一次数组，和暴力解一样快，没有额外的循环或递归。
- **空间复杂度**：`O(1)` — 只用了生成器表达式，不会创建额外的列表，额外空间保持常数级。

---

## 心得

- **核心技巧**：一次遍历统计（线性扫描）+ 利用布尔值的数值特性进行简洁计数。  
- **适用的题型**：  
  1. “统计满足某个条件的元素个数”，如 **统计数组中奇数的个数**。  
  2. “判断数组中是否全部/至少满足某个条件”，如 **判断是否所有学生成绩及格**。  
- **一句话总结解题钥匙**：**只要一次线性扫描即可得到答案，别忘了布尔值可以直接累加**。

## 反思

- **第一反应**：看到“统计”二字，就想到遍历数组并计数。  
- **最容易踩的坑**：  
  - 忘记考虑 `target` 为 `0` 的情况（此时所有员工都满足）。  
  - 忽视空数组的输入（虽然题目保证长度 ≥ 1），但写代码时仍应保证函数对空列表返回 `0`。  
- **下次遇到同类题**：第一步就想到 **“一次遍历 + 条件计数”**，如果语言支持布尔值累加，可以直接用 `sum` 把代码压缩到一行。