# #1360. 两个日期之间的天数 / Number of Days Between Two Dates

> 难度：简单 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/number-of-days-between-two-dates/)

---

## 题目（英文原版）

**Description**

Write a program to count the number of days between two dates.
The two dates are given as strings, their format is YYYY-MM-DD as shown in the examples.

**Examples**

**Example 1:**

```
Input: date1 = "2019-06-29", date2 = "2019-06-30"
Output: 1
```

**Example 2:**

```
Input: date1 = "2020-01-15", date2 = "2019-12-31"
Output: 15
```

**Constraints**

- The given dates are valid dates between the years 1971 and 2100.

---

## 题目（中文翻译）

描述：  
编写一个程序，计算两个日期之间相差的天数。  
这两个日期以字符串形式给出，格式为 `YYYY-MM-DD`（年-月-日），如示例所示。

约束条件：  
- 给定的日期均为有效日期，年份范围在 1971 到 2100 之间。

示例：

示例 1:  
Input: date1 = "2019-06-29", date2 = "2019-06-30"  
Output: 1  

示例 2:  
Input: date1 = "2020-01-15", date2 = "2019-12-31"  
Output: 15

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把两个日期之间的每一天都枚举出来，计数器每走一步就加 1，最后得到的计数就是答案。  
- **数据结构**：我们只需要用 `datetime` 模块（或手动实现）来把日期表示成 “年‑月‑日”，然后用 `while` 循环把日期往后推一天。  
- **生活化类比**：这就像在日历本上从起始页翻到结束页，每翻一页就记一次，最后记了多少页就是多少天。  
- **正确性**：因为我们把 **每一天** 都走了一遍，肯定不会漏掉，也不会多算，所以答案一定正确。  

#### 代码（Python）

```python
from datetime import datetime, timedelta

def days_between_bruteforce(date1: str, date2: str) -> int:
    """
    暴力版：逐天遍历，计数
    """
    # 把字符串转成 datetime 对象，方便加一天
    d1 = datetime.strptime(date1, "%Y-%m-%d")
    d2 = datetime.strptime(date2, "%Y-%m-%d")

    # 让 start 永远是较小的那个，end 是较大的那个
    start, end = (d1, d2) if d1 <= d2 else (d2, d1)

    cnt = 0                     # 计数器
    cur = start
    while cur < end:           # 当 cur 还没到达 end 时
        cur += timedelta(days=1)   # 往后走一天
        cnt += 1               # 计数加一
    return cnt
```

#### 复杂度

- **时间复杂度**：`O(D)`，其中 `D` 是两个日期之间的天数。直观上可以理解为“我们要走多少步就花多少时间”。如果相隔 10 000 天，就要循环 10 000 次。
- **空间复杂度**：`O(1)`，只用了常数级的变量（计数器、当前日期等），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**逐天遍历**——如果日期相差很多年，循环次数会非常大。  
我们可以把每个日期先转换成“从某个固定起点（比如 1900‑01‑01）到该日期的天数”，记作 `f(date)`。  
这样答案就只需要 `|f(date1) - f(date2)|`，不需要再逐天遍历。

**如何构造 `f(date)`？**  
1. **累计完整的年份**  
   - 从基准年 1900 开始，遍历到 `year-1`（不包括当前年份）。  
   - 每一年要么 365 天，要么 366 天（闰年）。  
   - **闰年的判断**：如果 `year` 能被 4 整除且不能被 100 整除，或者能被 400 整除，则是闰年。  
   - 类比：把每一年看成一本厚厚的日历册，闰年比普通年多加一页（2 月 29 日）。

2. **累计当前年份已过去的月份**  
   - 先准备一个普通年的每月天数列表 `month_days = [31,28,31,30,31,30,31,31,30,31,30,31]`。  
   - 如果当前年份是闰年，把二月的天数改成 29。  
   - 然后把 `month-1` 个月的天数相加。

3. **累计当前月份已经过去的天数**  
   - 再把 `day-1` 加进去（因为要算到当天的前一天为止）。

把三步的和相加，就得到 `f(date)`。  
最后返回 `abs(f(date1) - f(date2))` 即可。

#### 代码（Python）

```python
def is_leap(year: int) -> bool:
    """
    判断闰年
    - 能被 4 整除且不能被 100 整除，或者能被 400 整除
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def days_from_1900(date: str) -> int:
    """
    计算从 1900-01-01 到给定日期（不包括当天）的天数
    """
    year, month, day = map(int, date.split('-'))

    # 1. 累计完整的年份
    days = 0
    for y in range(1900, year):
        days += 366 if is_leap(y) else 365

    # 2. 累计当前年份已过去的月份
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_leap(year):
        month_days[1] = 29                     # 二月改成 29 天

    for m in range(1, month):                  # 只加到 month-1
        days += month_days[m - 1]

    # 3. 累计当前月份已经过去的天数
    days += day - 1                            # 不包括当天本身

    return days

def days_between(date1: str, date2: str) -> int:
    """
    最优解：先转成天数再相减，取绝对值
    """
    return abs(days_from_1900(date1) - days_from_1900(date2))
```

#### 复杂度

- **时间复杂度**：`O(Y)`，其中 `Y` 为年份差（最多约 130 年），因为我们只遍历年份一次，再遍历月份（固定 12 次）。相较于暴力的 `O(D)`（天数），这已经是常数级的提升。可以说“无论相隔多少天，循环次数都不会超过几百次”。  
- **空间复杂度**：`O(1)`，只用了几个整数变量和一个长度为 12 的列表，空间开销与输入大小无关。

---

## 心得

- **核心技巧**：把日期转换为“距基准点的天数”，利用**闰年判定**和**月份天数表**进行累计。  
- **适用的题型**：  
  1. 两个日期相差天数的计算（本题）。  
  2. 判断某日期是否在另一个日期范围内。  
  3. 计算某日期是当年的第几天（第几周）。  
- **一句话总结解题钥匙**：**把复杂的日期比较转化为整数相减**。

---

## 反思

- **第一反应**：直接用 `while` 循环一天一天地走，代码最容易写。  
- **最容易踩的坑**：  
  - **闰年判断错误**（忘记 100 年整除但不满足 400 整除的情况）。  
  - **月份天数写错**（二月 28/29 天、30/31 天的对应关系）。  
  - **忘记取绝对值**，导致输出负数。  
- **下次类似题的第一步**：先想“能不能把日期映射成一个整数”，再在整数层面做差值运算。这样往往能把 O(天数) 的暴力遍历压到 O(年份) 或 O(1)。