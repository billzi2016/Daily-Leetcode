# #690. 员工重要性 / Employee Importance

> 难度：中等 · 标签：Array、Hash Table、Tree、Depth-First Search、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/employee-importance/)

---

## 题目（英文原版）

**Description**

You have a data structure of employee information, including the employee's unique ID, importance value, and direct subordinates' IDs.
You are given an array of employees employees where:
Given an integer id that represents an employee's ID, return the total importance value of this employee and all their direct and indirect subordinates.

**Examples**

**Example 1:**

```
Input: employees = [[1,5,[2,3]],[2,3,[]],[3,3,[]]], id = 1
Output: 11
Explanation: Employee 1 has an importance value of 5 and has two direct subordinates: employee 2 and employee 3.
They both have an importance value of 3.
Thus, the total importance value of employee 1 is 5 + 3 + 3 = 11.
```

**Example 2:**

```
Input: employees = [[1,2,[5]],[5,-3,[]]], id = 5
Output: -3
Explanation: Employee 5 has an importance value of -3 and has no direct subordinates.
Thus, the total importance value of employee 5 is -3.
```

**Constraints**

- 1 <= employees.length <= 2000
- 1 <= employees[i].id <= 2000
- All employees[i].id are unique.
- -100 <= employees[i].importance <= 100
- One employee has at most one direct leader and may have several subordinates.
- The IDs in employees[i].subordinates are valid IDs.

---

## 题目（中文翻译）

**描述**  
你有一个存放员工信息（Employee information）的数据结构，其中包括员工的唯一 ID、重要性值（importance）以及直接下属（direct subordinates）的 ID 列表。  
给定一个员工数组 `employees`，以及一个整数 `id`（代表某位员工的 ID），返回该员工及其所有直接和间接下属的 **总重要性值（total importance value）**。

**示例 1**  
输入: `employees = [[1,5,[2,3]],[2,3,[]],[3,3,[]]], id = 1`  
输出: `11`  
解释: 员工 1 的重要性值为 5，且拥有两名直接下属：员工 2 和员工 3。  
它们的重要性值均为 3。  
因此，员工 1 的总重要性值为 `5 + 3 + 3 = 11`。

**示例 2**  
输入: `employees = [[1,2,[5]],[5,-3,[]]], id = 5`  
输出: `-3`  
解释: 员工 5 的重要性值为 -3，且没有直接下属。  
因此，员工 5 的总重要性值为 `-3`。

**约束条件**  
- `1 <= employees.length <= 2000`  
- `1 <= employees[i].id <= 2000`  
- 所有 `employees[i].id` 均唯一。  
- `-100 <= employees[i].importance <= 100`  
- 每位员工最多只有一个直接上级（leader），但可以有多个下属。  
- `employees[i].subordinates` 中的 ID 均为有效的员工 ID。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：  
1. 先在 `employees` 这张「名单」里找到 **id 对应的员工对象**。  
2. 把这个员工的 `importance` 加到答案里。  
3. 然后遍历他的 `subordinates`（直接下属），对每一个下属 **重复** 步骤 1‑3。  

这里使用的核心数据结构是 **列表（list）**，因为题目把所有员工都放在一个数组里。  
可以把它想象成一本「公司通讯录」，我们每次都要从头翻到对应的那一页，找到某个人的记录。  

为什么这个方法一定能得到正确答案？  
- 递归（或显式的栈）保证了「先处理自己，再处理所有直接下属的下属……」的顺序。  
- 只要每次都把当前员工的 `importance` 加上，所有直接或间接的下属都会被遍历到，最终得到的和就是题目要求的「本人 + 所有下属」的总重要度。

时间复杂度分析（大白话）：  
- 对每一次递归，我们都要在 `employees` 里 **线性查找**（遍历一次）对应的员工。  
- 最坏情况下，所有员工都会被访问一次，且每次查找都要遍历 `employees`（最多 2000 次）。  
- 所以时间是 **O(n²)**，即「如果有 1000 个人，最多要比较 1000 × 1000 = 1 000 000 次」。  

空间复杂度：  
- 递归深度最坏会等于员工总数 `n`，栈空间是 **O(n)**。  
- 另外我们没有额外的存储结构，只是用了常数级别的变量，故 **O(n)**（递归栈）即可。

#### 代码（Python）  

```python
# Definition for Employee.
class Employee:
    def __init__(self, id: int, importance: int, subordinates: list):
        self.id = id                # 员工唯一编号
        self.importance = importance  # 重要度
        self.subordinates = subordinates  # 直接下属的 id 列表


class Solution:
    def getImportance(self, employees: list[Employee], id: int) -> int:
        """
        暴力版：每次都线性搜索员工列表
        """
        # 递归函数：返回以 cur_id 为根的子树总重要度
        def dfs(cur_id: int) -> int:
            # 在整个 employees 列表里找 id == cur_id 的员工
            for emp in employees:          # O(n) 的线性查找
                if emp.id == cur_id:
                    # 找到后，先把自己的重要度加进去
                    total = emp.importance
                    # 再把每个直接下属的子树重要度累加
                    for sub_id in emp.subordinates:
                        total += dfs(sub_id)   # 递归处理下属
                    return total
            # 根据题意不会出现找不到的情况，这里仅作防御性返回 0
            return 0

        return dfs(id)
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - n 是员工总数。每访问一个员工时，都要在 `employees` 列表里遍历一次来定位。  
- **空间复杂度**：`O(n)`  
  - 递归调用栈最深可能等于员工数量。除了栈之外只用了常数级别的额外空间。  

---  

### 2. 最优解  

#### 思路  

从暴力解来看，**瓶颈** 在于每次都要遍历整个 `employees` 列表来定位员工。  
如果我们能够把「id → Employee 对象」的映射事先建立好，以后查找就可以 **O(1)**（常数时间）完成。  

这正是 **哈希表（字典）** 的用武之地：  
- 把每个员工的 `id` 当作键（key），把对应的 `Employee` 实例当作值（value）。  
- 查字典就像在一本「员工电话簿」里直接翻到对应的页码，一眼就能找到。  

有了这张「快速查找表」后，遍历员工的过程就只剩下 **DFS（深度优先搜索）** 或 **BFS（广度优先搜索）** 两种实现方式，时间复杂度会降到 **O(n)**。  

这里我们使用 **DFS（递归）**，思路如下：

1. **预处理**：遍历 `employees`，把 `id → Employee` 放进字典 `emp_map`。  
2. **深度优先遍历**：从给定的 `id` 开始，累计当前员工的 `importance`，然后递归遍历它的所有直接下属。  
3. 由于每个员工只会被访问一次，整体时间是线性的。  

如果不想用递归，也可以用 **队列** 实现 BFS，思路完全相同，只是遍历顺序不同，复杂度也一样。

#### 代码（Python）  

```python
# Definition for Employee.
class Employee:
    def __init__(self, id: int, importance: int, subordinates: list):
        self.id = id
        self.importance = importance
        self.subordinates = subordinates


class Solution:
    def getImportance(self, employees: list[Employee], id: int) -> int:
        """
        最优解：先把 id 映射到 Employee（哈希表），再用 DFS 累加重要度
        """
        # 1️⃣ 预处理：构造哈希表，key 是员工 id，value 是 Employee 对象
        emp_map: dict[int, Employee] = {emp.id: emp for emp in employees}
        # 这里的 dict 推导式相当于：“把每个员工放进字典，方便以后 O(1) 查找”

        # 2️⃣ 深度优先搜索（递归版）
        def dfs(cur_id: int) -> int:
            emp = emp_map[cur_id]          # O(1) 直接拿到员工对象
            total = emp.importance         # 先加上自己的重要度
            # 对每个直接下属继续递归求和
            for sub_id in emp.subordinates:
                total += dfs(sub_id)
            return total

        # 3️⃣ 从根节点（题目给出的 id）开始求和
        return dfs(id)
```

> **如果不想用递归**（防止递归层数太深导致栈溢出），可以改写为 BFS：

```python
from collections import deque

class Solution:
    def getImportance(self, employees: list[Employee], id: int) -> int:
        emp_map = {e.id: e for e in employees}
        total = 0
        q = deque([id])               # 队列初始化，只装根节点
        while q:
            cur = q.popleft()         # 取出当前员工 id
            emp = emp_map[cur]
            total += emp.importance   # 累加自己的重要度
            q.extend(emp.subordinates)   # 把直接下属全部加入队列
        return total
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 预处理遍历一次 `employees`（`O(n)`），随后每个员工只会被访问一次，查表是 `O(1)`，所以整体线性。  
- **空间复杂度**：`O(n)`  
  - 哈希表 `emp_map` 需要存放所有员工的信息，另外递归栈（或 BFS 队列）最坏也会保存 `n` 个节点。  

---

## 心得  

- **核心技巧**：利用哈希表把「根据 id 查找员工」的操作从线性时间降到常数时间，然后配合 DFS/BFS 完成树形（或森林）结构的遍历。  
- **适用的题型**：  
  1. **公司组织结构** 类题目（如 “Employee Importance”）。  
  2. **社交网络** 中的「朋友推荐」或「影响力传播」问题。  
  3. **文件系统** 目录大小统计（把路径映射到节点，再遍历子节点）。  
- **一句话总结**：**先把“谁是谁”记下来（哈希表），再把“谁管谁”遍历一遍（DFS/BFS）**。  

---

## 反思  

- **第一反应**：看到 `id`、`subordinates`，立刻想到要 **遍历树**，于是想用递归把每个下属的价值累加。  
- **最容易踩的坑**：  
  - **查找效率**：直接在列表里找员工会导致 `O(n²)`，在数据稍大时会超时。  
  - **负数重要度**：重要度可以为负，累加时不能假设一定是增大的。  
  - **递归深度**：极端情况下链式下属会导致递归层数接近 `n`，在 Python 中可能触发递归深度限制。  
- **下次遇到同类题**，第一步应该先问自己：「这道题是否涉及**频繁的 id → 对象** 查找？」如果答案是「是」，就立即构建哈希表，再决定用 DFS 还是 BFS 完成遍历。