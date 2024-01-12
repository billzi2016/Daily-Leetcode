# #2545. **按第 k 场考试成绩排序学生** / Sort the Students by Their Kth Score

> 难度：中等 · 标签：Array、Sorting、Matrix · [LeetCode 链接](https://leetcode.com/problems/sort-the-students-by-their-kth-score/)

---

## 题目（英文原版）

**Description**

There is a class with m students and n exams. You are given a 0-indexed m x n integer matrix score, where each row represents one student and score[i][j] denotes the score the ith student got in the jth exam. The matrix score contains distinct integers only.
You are also given an integer k. Sort the students (i.e., the rows of the matrix) by their scores in the kth (0-indexed) exam from the highest to the lowest.
Return the matrix after sorting it.

**Examples**

**Example 1:**

```
Input: score = [[10,6,9,1],[7,5,11,2],[4,8,3,15]], k = 2
Output: [[7,5,11,2],[10,6,9,1],[4,8,3,15]]
Explanation: In the above diagram, S denotes the student, while E denotes the exam.
- The student with index 1 scored 11 in exam 2, which is the highest score, so they got first place.
- The student with index 0 scored 9 in exam 2, which is the second highest score, so they got second place.
- The student with index 2 scored 3 in exam 2, which is the lowest score, so they got third place.
```

**Example 2:**

```
Input: score = [[3,4],[5,6]], k = 0
Output: [[5,6],[3,4]]
Explanation: In the above diagram, S denotes the student, while E denotes the exam.
- The student with index 1 scored 5 in exam 0, which is the highest score, so they got first place.
- The student with index 0 scored 3 in exam 0, which is the lowest score, so they got second place.
```

**Constraints**

- m == score.length
- n == score[i].length
- 1 <= m, n <= 250
- 1 <= score[i][j] <= 105
- score consists of distinct integers.
- 0 <= k < n

---

## 题目（中文翻译）

给定一个 $m \times n$ 的整数矩阵 `score`（0 索引），其中每一行对应一名学生，`score[i][j]` 表示第 $i$ 名学生在第 $j$ 场考试（exam）中得到的分数（score）。矩阵中的所有整数互不相同。  
同时给定一个整数 $k$，要求按照第 $k$ 场考试（0 索引）的分数从高到低对学生（即矩阵的行）进行排序，并返回排序后的矩阵。

---

**示例 1**

```text
Input: score = [[10,6,9,1],[7,5,11,2],[4,8,3,15]], k = 2
Output: [[7,5,11,2],[10,6,9,1],[4,8,3,15]]
```

**解释**：图中用 **S** 表示学生，用 **E** 表示考试。  
- 学生下标为 1 的在第 2 场考试中得分 11，最高，排名第一。  
- 学生下标为 0 的在第 2 场考试中得分 9，第二高，排名第二。  
- 学生下标为 2 的在第 2 场考试中得分 3，最低，排名第三。

---

**示例 2**

```text
Input: score = [[3,4],[5,6]], k = 0
Output: [[5,6],[3,4]]
```

**解释**：图中用 **S** 表示学生，用 **E** 表示考试。  
- 学生下标为 1 的在第 0 场考试中得分 5，最高，排名第一。  
- 学生下标为 0 的在第 0 场考试中得分 3，最低，排名第二。

---

**约束条件**

- $m == \text{score}.length$
- $n == \text{score}[i].length$
- $1 \le m, n \le 250$
- $1 \le \text{score}[i][j] \le 10^{5}$
- `score` 中的所有整数互不相同
- $0 \le k < n$

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把每个学生的第 k 门成绩记下来，然后把这些成绩从大到小排个序，按照排好的顺序把对应的整行（即整位学生的所有成绩）搬到新的位置**。  

实现上可以把“第 k 门成绩 → 学生所在行”这对信息放进**列表**中，列表里的每个元素是 `(score[i][k], i)`，就像把每位学生的成绩写进一本小册子，**成绩**是“关键词”，**学生编号**是“页码”。  
随后我们把这本小册子**按照成绩从大到小排序**（相当于在字典里查“最大页码对应的词”），最后依次把排好序的学生行取出来组成新矩阵。

因为题目保证所有分数互不相同，排序时不需要考虑相同分数的情况。  

> **为什么这个方法一定正确？**  
> 排序的定义就是把一组数按大小顺序重新排列。我们只排序第 k 门的成绩，而每个成绩唯一对应一行原始数据，所以排序后的顺序必然就是“第 k 门成绩从高到低的学生顺序”。把对应的整行搬过去，矩阵自然就完成了要求的排序。

#### 代码（Python）

```python
from typing import List

def sortStudents_bruteforce(score: List[List[int]], k: int) -> List[List[int]]:
    """
    暴力思路：先把每行第 k 列的成绩取出来，和行号一起放进列表，
    再按照成绩从大到小排序，最后按排好序的行号重新组织矩阵。
    """
    m = len(score)                     # 学生人数
    # 1) 把 (第 k 门成绩, 行号) 放进一个列表
    kth_with_idx = [(score[i][k], i) for i in range(m)]
    # 2) 按成绩降序排序，reverse=True 表示从大到小
    kth_with_idx.sort(key=lambda x: x[0], reverse=True)

    # 3) 根据排好序的行号依次取出原矩阵的行，组成新矩阵
    sorted_score = [score[idx] for _, idx in kth_with_idx]
    return sorted_score
```

#### 复杂度  

- **时间复杂度**：`O(m log m)`  
  - 取第 k 列成绩是 `O(m)`，排序是 `O(m log m)`（对 m 条记录排序的常见复杂度），其余操作都是线性。  
  - 大白话：如果有 1000 位学生，排序大概要比一次普通的遍历慢 **log₂1000 ≈ 10** 倍左右。

- **空间复杂度**：`O(m)`  
  - 需要额外存放 `kth_with_idx`（每位学生的成绩+行号）和新矩阵 `sorted_score`，这两部分都是和学生数成正比的。

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，**真正的耗时在排序这一步**，而我们已经使用了 Python 内置的 `list.sort`（或 `sorted`），它基于 **Timsort**，在最坏情况下也是 `O(m log m)`，已经是对 `m` 条记录的最优时间复杂度。  

如果一定要说“更优”，可以直接在 **一次遍历** 中把第 k 列的成绩作为 **排序键**，利用 **`sorted` 的 `key` 参数**，省去手动构造 `(score, idx)` 的中间列表。这样代码更简洁，空间占用略微降低（不需要额外存放行号列表），但时间仍是 `O(m log m)`，已经是理论下界。

> **核心技巧：自定义排序键**  
> 把每行本身当作要排序的对象，告诉排序函数“请把第 k 列的数值当作比较的依据”。这就像在图书馆里把所有书直接按照“出版年份”来排，而不必先把年份写在纸条上再排序。

#### 代码（Python）

```python
from typing import List

def sortStudents_optimal(score: List[List[int]], k: int) -> List[List[int]]:
    """
    最优思路：直接使用 Python 的 sorted，key=lambda row: row[k] 表示
    按第 k 列的数值作为比较键，reverse=True 表示从大到小。
    """
    # sorted 会返回一个新的列表，不会修改原始矩阵
    return sorted(score, key=lambda row: row[k], reverse=True)
```

#### 复杂度  

- **时间复杂度**：`O(m log m)`  
  - 与暴力解的排序步骤相同，只是省去了额外的遍历和列表构造。  
  - 对比：如果有 250 位学生，排序大约需要 `250 * log₂250 ≈ 250 * 8 = 2000` 次比较，已经是最少需要的次数。

- **空间复杂度**：`O(m)`（返回的新矩阵）  
  - 只需要存放排序后的结果，不再额外保存 `(成绩, 行号)` 的中间列表，略微节省了一点内存。

---

## 心得  

- **核心技巧**：自定义排序键（`key=lambda row: row[k]`）配合 `reverse=True` 实现“按某列降序排列”。  
- **适用的题型**：  
  1. 按二维数组（矩阵）中的某一列排序（如“按工资排序员工表”）。  
  2. 按字典列表中的某个字段排序（如“按年龄排序用户信息”）。  
  3. 按对象列表中属性排序（如“按成绩对象的分数属性排序”）。  
- **一句话总结解题钥匙**：**把要比较的列（或属性）直接交给排序函数，让它帮你完成“挑高分/挑大值”的工作**。

---

## 反思  

- **第一反应**：看到“把第 k 列从高到低排”，立刻想到把第 k 列抽出来排序，再把对应的整行搬过去。  
- **最容易踩的坑**：  
  - 忘记设置 `reverse=True`，导致得到的是升序而不是题目要求的降序。  
  - 忽视了 **“分数互不相同”** 的前提，若有相同分数时需要考虑是否保持原有相对顺序（稳定排序）。  
  - 误把 `k` 当成 1‑indexed（从 1 开始），导致索引越界。  
- **下次遇到同类题**，第一步应该想到：**“这是一道‘按某列排序’的题，用 Python 的 sorted/key 参数可以一次搞定”。**  

祝你在算法的路上越走越稳，继续加油！ 🚀