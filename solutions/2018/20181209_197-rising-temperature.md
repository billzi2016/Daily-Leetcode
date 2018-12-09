# #197. 气温上升 / Rising Temperature

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/rising-temperature/)

---

## 题目（英文原版）

**Description**

Table: Weather
Write a solution to find all dates' id with higher temperatures compared to its previous dates (yesterday).
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| recordDate    | date    |
| temperature   | int     |
+---------------+---------+
id is the column with unique values for this table.
There are no different rows with the same recordDate.
This table contains information about the temperature on a certain day.
```

**Example 2:**

```
Input: 
Weather table:
+----+------------+-------------+
| id | recordDate | temperature |
+----+------------+-------------+
| 1  | 2015-01-01 | 10          |
| 2  | 2015-01-02 | 25          |
| 3  | 2015-01-03 | 20          |
| 4  | 2015-01-04 | 30          |
+----+------------+-------------+
Output: 
+----+
| id |
+----+
| 2  |
| 4  |
+----+
Explanation: 
In 2015-01-02, the temperature was higher than the previous day (10 -> 25).
In 2015-01-04, the temperature was higher than the previous day (20 -> 30).
```

---

## 题目（中文翻译）

Table: Weather（表：Weather）

编写一个查询，找出所有温度高于前一天（昨天）的记录对应的 **id**。  
以任意顺序返回结果表。  
结果格式见下例。

**示例 1**

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| recordDate    | date    |
| temperature   | int     |
+---------------+---------+

- `id` 为本表唯一的标识列。  
- 同一 `recordDate` 不会出现多行记录。  
- 该表记录了每一天的温度信息。

**示例 2**

**Input**  
Weather 表：

+----+------------+-------------+
| id | recordDate | temperature |
+----+------------+-------------+
| 1  | 2015-01-01 | 10          |
| 2  | 2015-01-02 | 25          |
| 3  | 2015-01-03 | 20          |
| 4  | 2015-01-04 | 30          |
+----+------------+-------------+

**Output**  

+----+
| id |
+----+
| 2  |
| 4  |
+----+

**Explanation**  
- 在 2015-01-02，温度高于前一天 (10 → 25)。  
- 在 2015-01-04，温度高于前一天 (20 → 30)。

约束条件  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：对表中的每一条记录 **A**，把它的 `recordDate` 往前找一天（`昨天`），再把所有记录逐个遍历一遍，看看有没有一条记录 **B** 的 `recordDate` 正好等于 **A** 的前一天且 `temperature` 更低。  
如果找到了，就把 **A** 的 `id` 加入答案。

- **使用的数据结构**：  
  - **列表**（`list`）存放所有行，类似把所有天气记录装进一个装满卡片的抽屉。  
  - **双层循环**（`for i in range(n): for j in range(n):`）相当于把抽屉里的每张卡片都和其他每张卡片比较一次，像是让每个人都跟全班同学握手。

- **为什么正确**：  
  - 我们把每一天都和它的前一天（如果存在）比较了一遍，满足题目“温度高于昨天”的所有情况都会被捕获。

- **时间/空间复杂度**：  
  - **时间**：外层循环遍历 `n` 条记录，内层循环也遍历 `n` 条记录，总共是 `n × n`，记作 **O(n²)**。  
    - 大白话：如果有 1000 条记录，就要比较 1000 × 1000 = 1 000 000 次，数量会快速膨胀。  
  - **空间**：只用了原始列表和答案列表，额外空间与记录数无关，记作 **O(1)**（不计答案本身）。

#### 代码（Python）

```python
from datetime import datetime, timedelta
from typing import List, Dict

def rising_temperature_brute(weather: List[Dict]) -> List[int]:
    """
    暴力解：双层循环逐条比较
    :param weather: 每条记录是 {'id': int, 'recordDate': 'YYYY-MM-DD', 'temperature': int}
    :return: 满足 temperature > yesterday temperature 的 id 列表
    """
    n = len(weather)
    res = []

    # 把日期字符串转成 datetime，后面比较更方便
    for rec in weather:
        rec['date_obj'] = datetime.strptime(rec['recordDate'], "%Y-%m-%d")

    for i in range(n):
        cur = weather[i]
        # 计算昨天的日期
        yesterday = cur['date_obj'] - timedelta(days=1)

        # 在所有记录中找出昨天那天的温度
        for j in range(n):
            prev = weather[j]
            if prev['date_obj'] == yesterday:
                # 找到昨天的记录，比较温度
                if cur['temperature'] > prev['temperature']:
                    res.append(cur['id'])
                break   # 昨天只会出现一次，找到后可以提前结束内层循环

    # 清理临时字段（如果后面不再使用的话）
    for rec in weather:
        rec.pop('date_obj', None)

    return res
```

#### 复杂度

- **时间复杂度**：**O(n²)**  
  - 两层循环导致比较次数随记录数的平方增长，记录越多越慢。

- **空间复杂度**：**O(1)**（不计答案列表）  
  - 只在原数组上做了少量临时字段，额外占用常数级别空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每条记录都要遍历整个表去找昨天的记录”**，这一步是 **O(n)**，导致整体 **O(n²)**。  
我们可以把“找昨天的记录”这一步变成 **O(1)**，思路有两种：

1. **哈希表（字典）**：把所有记录先放进一个 `date → (id, temperature)` 的映射中。  
   - 类比：把所有天气卡片按日期编号，放进一本“日期-索引手册”，以后要查某天的温度，只需要翻开对应页码（O(1)）即可。  
   - 然后遍历一次表，取每条记录的 `recordDate - 1 天` 去字典里查，如果存在且温度更低，就把 `id` 加入答案。  
   - 这一步只需要 **一次遍历**，时间降到 **O(n)**，空间因为字典多了 `n` 条键值对，变成 **O(n)**。

2. **先排序 + 相邻比较**（也是 O(n log n)）  
   - 先把记录按照 `recordDate` 排序（类似把卡片按日期排好队），然后只需要比较相邻两天的温度即可。  
   - 由于题目保证同一天只有一条记录，排序后相邻的记录恰好是昨天和今天。  
   - 时间复杂度是 **O(n log n)**（排序），空间仍是 **O(1)**（原地排序或使用额外的临时列表）。

这里我们选用 **哈希表**（字典）实现，因为它既直观又达到 **O(n)** 的线性时间。

#### 代码（Python）

```python
from datetime import datetime, timedelta
from typing import List, Dict

def rising_temperature_opt(weather: List[Dict]) -> List[int]:
    """
    最优解：利用哈希表把日期映射到对应的温度，单次遍历即可判断是否升温
    :param weather: 与上面相同的输入格式
    :return: 满足 temperature > yesterday temperature 的 id 列表
    """
    # 1️⃣ 把日期（datetime 对象）映射到 (id, temperature)
    date_map = {}
    for rec in weather:
        # 把字符串日期转成 datetime，便于后面做减法
        d = datetime.strptime(rec['recordDate'], "%Y-%m-%d")
        date_map[d] = (rec['id'], rec['temperature'])

    res = []

    # 2️⃣ 再遍历一次，查找昨天的记录
    for rec in weather:
        cur_date = datetime.strptime(rec['recordDate'], "%Y-%m-%d")
        yesterday = cur_date - timedelta(days=1)

        if yesterday in date_map:                # 昨天有记录
            _, y_temp = date_map[yesterday]      # 取昨天的温度
            if rec['temperature'] > y_temp:      # 今天温度更高
                res.append(rec['id'])

    return res
```

#### 复杂度

- **时间复杂度**：**O(n)**  
  - 第一次遍历把所有记录放进字典，第二次遍历只做一次 O(1) 的查找和比较，总共线性增长。  
  - 与暴力解相比，**从 n² 降到 n**，即使记录数是几万条也能在毫秒级完成。

- **空间复杂度**：**O(n)**  
  - 需要额外的字典保存每一天的 `(id, temperature)`，所以空间随记录数线性增长。  
  - 这在大多数实际场景（几万到几百万条）都是可以接受的。

---

## 心得

- **核心技巧**：**利用哈希表实现「按键快速查找」**，把「昨天的记录」从线性搜索提升到常数时间查找。  
- **适用的题型**：  
  1. **日期/时间序列比较**（如「每日销售额是否比前一天高」）。  
  2. **基于「前一个元素」的判断**（如「数组中元素是否大于左邻右舍」）。  
  3. **需要「快速定位」某个属性对应值的查询**（如「给定员工 ID，快速找出其部门」）。
- **一句话总结解题钥匙**：**先把「查找」这一步变成 O(1)，再遍历一次即可完成所有比较**。

---

## 反思

- **第一反应**：看到“前一天”，自然想到「遍历找前一天」——这就是暴力思路。  
- **最容易踩的坑**：  
  - **日期的处理**：直接把字符串相减会出错，需要先转成 `datetime` 再做 `timedelta(days=1)`。  
  - **缺失的前一天**：有的记录是第一天，没有昨天的记录，必须先判断 `yesterday in date_map`。  
  - **重复日期**：题目说同一天不会出现多条记录，但如果出现，需要决定取哪一条（通常取最高/最低温度），这里不必考虑。  
- **下次类似题的第一步**：**先把「可以 O(1) 直接定位」的键值对放进哈希表**（或排序），再在遍历中利用它们完成比较。这样可以把时间从平方级直接降到线性级。