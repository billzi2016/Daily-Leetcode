# #601. 体育场人流量 / Human Traffic of Stadium

> 难度：困难 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/human-traffic-of-stadium/)

---

## 题目（英文原版）

**Description**

Table: Stadium
Write a solution to display the records with three or more rows with consecutive id's, and the number of people is greater than or equal to 100 for each.
Return the result table ordered by visit_date in ascending order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| visit_date    | date    |
| people        | int     |
+---------------+---------+
visit_date is the column with unique values for this table.
Each row of this table contains the visit date and visit id to the stadium with the number of people during the visit.
As the id increases, the date increases as well.
```

**Example 2:**

```
Input: 
Stadium table:
+------+------------+-----------+
| id   | visit_date | people    |
+------+------------+-----------+
| 1    | 2017-01-01 | 10        |
| 2    | 2017-01-02 | 109       |
| 3    | 2017-01-03 | 150       |
| 4    | 2017-01-04 | 99        |
| 5    | 2017-01-05 | 145       |
| 6    | 2017-01-06 | 1455      |
| 7    | 2017-01-07 | 199       |
| 8    | 2017-01-09 | 188       |
+------+------------+-----------+
Output: 
+------+------------+-----------+
| id   | visit_date | people    |
+------+------------+-----------+
| 5    | 2017-01-05 | 145       |
| 6    | 2017-01-06 | 1455      |
| 7    | 2017-01-07 | 199       |
| 8    | 2017-01-09 | 188       |
+------+------------+-----------+
Explanation: 
The four rows with ids 5, 6, 7, and 8 have consecutive ids and each of them has >= 100 people attended. Note that row 8 was included even though the visit_date was not the next day after row 7.
The rows with ids 2 and 3 are not included because we need at least three consecutive ids.
```

---

## 题目（中文翻译）

编写一个查询，展示 **连续的 id**（id） 行数不少于 3 且每行的 **people**（people） 大于等于 100 的记录。  
返回结果按 **visit_date**（visit_date） 升序排序。  
结果格式参照下例。

**示例 1**

示例表结构：

| Column Name | Type |
|-------------|------|
| id          | int  |
| visit_date  | date |
| people      | int  |

`visit_date` 为该表唯一的日期列。  
每条记录记录了某天（`visit_date`）进入体育场的 `id` 与当日到场人数 `people`。  
`id` 随日期递增，即 `id` 越大对应的 `visit_date` 越晚。

**示例 2**

输入：

```
Stadium 表:
+------+------------+-----------+
| id   | visit_date | people    |
+------+------------+-----------+
| 1    | 2017-01-01 | 10        |
| 2    | 2017-01-02 | 109       |
| 3    | 2017-01-03 | 150       |
| 4    | 2017-01-04 | 99        |
| 5    | 2017-01-05 | 145       |
| 6    | 2017-01-06 | 1455      |
| 7    | 2017-01-07 | 199       |
| 8    | 2017-01-09 | 188       |
+------+------------+-----------+
```

输出：

```
+------+------------+-----------+
| id   | visit_date | people    |
+------+------------+-----------+
| 5    | 2017-01-05 | 145       |
| 6    | 2017-01-06 | 1455      |
| 7    | 2017-01-07 | 199       |
| 8    | 2017-01-09 | 188       |
+------+------------+-----------+
```

**解释**  
`id` 为 5、6、7、8 的四行满足 **连续的 id** 且每行 `people` 均 ≥ 100，故被选入结果。  
注意，第 8 行虽然 `visit_date` 与第 7 行不是相邻的日期，但只要 `id` 连续即可。  
`id` 为 2、3 的两行未被选中，因为连续的 `id` 行数不足 3 条。  

**约束条件**  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的 **连续 id** 组合都枚举一遍，检查每个组合是否满足：

1. **id 连续**：`id[i+1] = id[i] + 1`（就像排队时每个人的号码正好相差 1）。
2. **人数 >= 100**：每一行的 `people` 都不小于 100。
3. **长度 ≥ 3**：组合里至少有三行。

如果一个组合满足上面三个条件，就把它里面的所有记录全部放进答案。  
这就像把所有可能的「连锁店」都检查一遍，看看哪几家店连续且客流都很大。

为什么正确？因为我们没有遗漏任何一种可能的连续段——所有长度≥3 的连续段都会在枚举过程中出现一次。

缺点是**枚举次数很多**：对每一个起点都要尝试往后延伸，最坏情况下会检查 `n + (n‑1) + … + 1 = O(n²)` 次（这里的 `n` 是表的行数），所以时间会很慢。

#### 代码（Python）

```python
from typing import List, Dict

def brute_force(stadium: List[Dict]) -> List[Dict]:
    """
    暴力枚举所有连续 id 的子数组，返回满足条件的记录。
    参数 stadium：形如 [{'id': 1, 'visit_date': '2017-01-01', 'people': 10}, ...]
    """
    n = len(stadium)
    # 为了保证按照 id 的顺序遍历，先按 id 排序
    stadium.sort(key=lambda x: x['id'])

    answer = []
    for i in range(n):                     # 选左端点
        cur_len = 0                         # 当前连续段长度
        segment = []                        # 暂存当前段的记录
        expected_id = stadium[i]['id']      # 期待的下一个 id

        for j in range(i, n):               # 向右扩展
            row = stadium[j]
            # ① id 必须连续
            if row['id'] != expected_id:
                break
            # ② people 必须 >= 100
            if row['people'] < 100:
                break

            segment.append(row)
            cur_len += 1
            expected_id += 1                 # 下一格期望的 id

            # 当长度已经达到 3 时，把整段加入答案
            if cur_len >= 3:
                # 注意：这里把 *所有* 已经收集的行都加入答案，
                # 但为了避免重复加入同一行，我们只在外层循环结束后统一去重。
                answer.extend(segment)

        # 继续下一个起点 i
    # 去重（因为同一行可能被不同起点的子数组重复加入）
    # 用 id 作为唯一标识，保持 visit_date 的升序
    seen = set()
    result = []
    for row in sorted(answer, key=lambda x: x['visit_date']):
        if row['id'] not in seen:
            seen.add(row['id'])
            result.append(row)
    return result
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  大白话：如果表里有 1000 条记录，最坏情况下要检查大约 1000 × 1000 / 2 ≈ 500 000 次，比线性遍历慢很多。  
- **空间复杂度**：`O(n)`（存放答案和临时的子数组），相当于再开一份表的大小。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复遍历相同的元素**。  
实际上，只要一次线性扫描就能把所有满足条件的连续段找出来：

1. **维护一个滑动窗口**，记录当前正在检测的连续段的起始位置 `start`、长度 `cnt`，以及是否所有 `people >= 100`。
2. 当遍历到第 `i` 行时，判断它是否可以 **接在前一行后面**  
   - `id[i] == id[i‑1] + 1`（id 连续）  
   - 且 `people[i] >= 100`（人数合格）  
   若两者都满足，就把 `cnt += 1`，窗口继续扩大。  
   否则，**窗口断裂**，需要重新从当前行开始重新计数（`start = i`，`cnt = 1`），因为新的段只能从这里起步。
3. 每当窗口长度 `cnt` 达到 **3** 时，说明已经找到了一个合法的连续段。此时把 **窗口里所有行**（从 `start` 到 `i`）全部加入答案。  
   注意：当窗口继续扩大到 4、5… 行时，这些新行也必须被加入答案，因为它们同样属于“至少 3 行连续且人数 >= 100” 的合法段。实现上，只要在 `cnt >= 3` 时把当前行 `i` 加入答案即可，之前已经加入的行不必再重复加入。
4. 最后把答案按 `visit_date` 升序返回。

核心技巧是 **一次遍历 + 计数**，类似 “找最长递增子序列的线性扫描”，不需要嵌套循环，也不需要额外的数据结构（哈希表、栈等），因此时间是 `O(n)`。

#### 代码（Python）

```python
from typing import List, Dict

def optimal(stadium: List[Dict]) -> List[Dict]:
    """
    O(n) 单次扫描找出所有满足条件的记录。
    """
    if not stadium:
        return []

    # 按 id 排序，保证 id 与 visit_date 同步递增
    stadium.sort(key=lambda x: x['id'])

    result = []               # 最终返回的记录
    start = 0                 # 当前合法段的起始下标
    cnt = 0                   # 当前段的长度（连续且 people >= 100 的行数）

    for i, row in enumerate(stadium):
        # 判断是否可以继续当前段
        if i > 0 and row['id'] == stadium[i-1]['id'] + 1 and row['people'] >= 100:
            cnt += 1                     # 段继续增长
        else:
            # 段断了，重新开始计数
            start = i
            cnt = 1 if row['people'] >= 100 else 0   # 只有本行满足才算 1，否则 0

        # 当 cnt >= 3 时，说明从 start 到 i 的所有行都是合法的
        if cnt >= 3:
            # 只把新出现的那一行加入结果即可（前面的已经在之前的步骤中加入）
            result.append(row)

    # 按 visit_date 升序返回（题目要求）
    result.sort(key=lambda x: x['visit_date'])
    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历一次表，像排队检查每个人的身份证一样，效率和人数成正比。相比暴力的 `O(n²)`，速度提升了 **n 倍**。
- **空间复杂度**：`O(k)`，其中 `k` 是答案的行数（最坏情况下可能是 `n`），额外的临时变量只有常数级别。

---

## 心得

- **核心技巧**：一次线性扫描 + 连续计数（滑动窗口思想）。  
- **适用场景**：  
  1. “连续子序列满足某个阈值” 类问题（如连续天数气温≥30℃）。  
  2. “满足条件的最长/最短连续段” 统计（如最长连续正数子数组）。  
  3. “在序列中找出满足长度≥k 的合法窗口” （如 LeetCode 2287 “Rearrange Characters to Make Target String”。）
- **一句话总结**：**只要把“是否可以继续”这件事抽象成布尔判断，整个过程就能在一次遍历中完成**。

---

## 反思

- **第一反应**：直接把所有可能的连续段枚举出来，写成三层循环——这就是暴力解的雏形。  
- **最容易踩的坑**：  
  - **边界条件**：段长度恰好为 3 时也要输出；段中出现 `people < 100` 或 `id` 不连续时必须立即终止当前段。  
  - **重复加入**：在暴力实现里，同一行可能被不同起点的子数组多次加入，需要去重。  
  - **排序**：题目要求按 `visit_date` 升序返回，若原表未按 `id` 排序，需要先排序，否则 `id` 与日期的对应关系会错乱。  
- **下次思路**：看到 “连续 id/日期 + 计数阈值” 这类描述时，第一步就想到 **线性扫描 + 计数**，把“是否连续” 和 “是否满足阈值” 两个条件合并成一个布尔表达式，避免嵌套循环。