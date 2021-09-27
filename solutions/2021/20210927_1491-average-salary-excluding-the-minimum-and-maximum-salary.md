# #1491. 除去最低工资和最高工资的平均工资 / Average Salary Excluding the Minimum and Maximum Salary

> 难度：简单 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/average-salary-excluding-the-minimum-and-maximum-salary/)

---

## 题目（英文原版）

**Description**

You are given an array of unique integers salary where salary[i] is the salary of the ith employee.
Return the average salary of employees excluding the minimum and maximum salary. Answers within 10-5 of the actual answer will be accepted.

**Examples**

**Example 1:**

```
Input: salary = [4000,3000,1000,2000]
Output: 2500.00000
Explanation: Minimum salary and maximum salary are 1000 and 4000 respectively.
Average salary excluding minimum and maximum salary is (2000+3000) / 2 = 2500
```

**Example 2:**

```
Input: salary = [1000,2000,3000]
Output: 2000.00000
Explanation: Minimum salary and maximum salary are 1000 and 3000 respectively.
Average salary excluding minimum and maximum salary is (2000) / 1 = 2000
```

**Constraints**

- 3 <= salary.length <= 100
- 1000 <= salary[i] <= 106
- All the integers of salary are unique.

---

## 题目（中文翻译）

**题目描述**  
给定一个唯一整数数组（array）`salary`，其中 `salary[i]` 表示第 `i` 位员工的工资。返回除去最低工资和最高工资后的员工平均工资。答案在实际值的 `10^-5` 以内均视为正确。

**示例 1**  
**输入**：`salary = [4000,3000,1000,2000]`  
**输出**：`2500.00000`  
**解释**：最低工资和最高工资分别是 `1000` 与 `4000`。除去这两个工资后的平均工资为 `(2000 + 3000) / 2 = 2500`。

**示例 2**  
**输入**：`salary = [1000,2000,3000]`  
**输出**：`2000.00000`  
**解释**：最低工资和最高工资分别是 `1000` 与 `3000`。除去这两个工资后的平均工资为 `(2000) / 1 = 2000`。

**约束条件**  
- `3 <= salary.length <= 100`  
- `1000 <= salary[i] <= 10^6`  
- `salary` 中的所有整数互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是先把工资数组 `salary` **排个序**，排好序后最小的工资就在最左边，最大的工资就在最右边。把这两个数剔除掉，剩下的数求和再除以剩余人数，就得到答案。

- **用到的数据结构**：数组 + 排序。  
  排序可以类比为把一堆不同颜色的球按颜色从浅到深摆成一排，最左边的就是最浅（最小），最右边的就是最深（最大）。
- **为什么正确**：因为题目要求“除去最小和最大工资的平均”，排序后直接把两端的元素跳过即可，剩下的就是题目要求的集合。
- **复杂度分析**：  
  - 排序的时间代价是 `O(n log n)`（`n` 是员工人数），相当于把 `n` 本书按照字母顺序排好，需要 `n log n` 次比较。  
  - 其余遍历求和、除法都是线性的 `O(n)`，但整体仍被排序的 `O(n log n)` 主导。  
  - 额外使用的空间只有常数级别的变量 `O(1)`（如果使用原地排序的话），不随 `n` 增长。

#### 代码（Python）

```python
from typing import List

def average(salary: List[int]) -> float:
    # 1. 对工资数组进行升序排序
    salary.sort()                     # 排序后最小值在左端，最大值在右端

    # 2. 去掉首尾两个元素（最小和最大工资），计算剩余部分的总和
    total = sum(salary[1:-1])         # salary[1:-1] 表示去掉第0个和最后1个

    # 3. 计算平均值：总和除以剩余人数 (n - 2)
    avg = total / (len(salary) - 2)

    return avg
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  这里的 `log n` 可以理解为“把 `n` 本书排好序需要的比较次数”，因为排序是最耗时的步骤。
- **空间复杂度**：`O(1)`（若使用原地排序）  
  只用了常数个额外变量，和输入规模无关。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **排序**，排序本身已经超出了这道题的实际需求。我们只需要知道 **最小值、最大值以及所有工资的总和**，不必把整个数组排好序。

从暴力思路出发：

1. **一次遍历**：在遍历数组的过程中同步维护三个变量  
   - `total`：所有工资的累计和  
   - `mn`：当前遍历到的最小工资  
   - `mx`：当前遍历到的最大工资  
   这相当于在看一本书的同时记录下最短、最长章节的页数，而不必把整本书重新排序。
2. **剔除极值**：遍历结束后，用 `total - mn - mx` 得到除去最小、最大后的总和。
3. **求平均**：除以剩余人数 `n - 2` 即可。

核心数据结构是 **常数个变量**，不需要额外的数组或哈希表。整个过程只遍历一次数组，时间是 `O(n)`，空间是 `O(1)`。

#### 代码（Python）

```python
from typing import List

def average(salary: List[int]) -> float:
    # 初始化：把第一个元素设为当前最小、最大值，累计总和为它本身
    total = salary[0]
    mn = salary[0]      # 当前最小工资
    mx = salary[0]      # 当前最大工资

    # 从第二个元素开始遍历
    for s in salary[1:]:
        total += s               # 累加总和
        if s < mn:
            mn = s               # 更新最小工资
        elif s > mx:
            mx = s               # 更新最大工资

    # 剔除最小、最大后的总和除以剩余人数
    avg = (total - mn - mx) / (len(salary) - 2)
    return avg
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只需一次线性遍历，即使有 100 名员工，也只需要 100 次“看一眼”，没有额外的比较或排序开销。
- **空间复杂度**：`O(1)`  
  只用了三个额外的变量（`total`, `mn`, `mx`），不随员工人数增长。

---

## 心得

- **核心技巧**：一次遍历同时维护**最值**（最小/最大）和**累计和**，常用于“除去极值求平均”或“求除极值之外的统计量”。
- **适用题型**：  
  1. “除去最高分和最低分的平均分”类题目  
  2. “数组中除去某些特殊元素后的和/平均值”  
  3. “在一次遍历中求最大、最小、总和” 的常规统计题
- **一句话总结**：**只要能在一次遍历中把所需信息全部收集完，就不需要排序，时间自然从 `O(n log n)` 降到 `O(n)`。**

---

## 反思

- **第一反应**：看到“除去最小和最大”会自然想到先排序，再取中间部分。
- **最容易踩的坑**：  
  - **边界条件**：数组长度最小为 3，除去两端后仍然至少剩一个元素，除法不会出现除以 0。  
  - **整数除法**：在 Python 3 中 `/` 会返回浮点数，满足题目要求的精度；若使用 `//`（整数除）会出错。  
  - **唯一性**：题目保证所有工资唯一，若不唯一仍然可以使用同样的思路，只是最小/最大可能出现多次，仍然只剔除一次即可。
- **下次第一步**：先思考“需要哪些信息（最小、最大、总和）”，判断是否可以 **一次遍历** 完成；如果可以，直接走 O(n) 的路线，避免不必要的排序。