# #619. 最大单一数字 / Biggest Single Number

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/biggest-single-number/)

---

## 题目（英文原版）

**Description**

Table: MyNumbers
A single number is a number that appeared only once in the MyNumbers table.
Find the largest single number. If there is no single number, report null.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| num         | int  |
+-------------+------+
This table may contain duplicates (In other words, there is no primary key for this table in SQL).
Each row of this table contains an integer.
```

**Example 2:**

```
Input: 
MyNumbers table:
+-----+
| num |
+-----+
| 8   |
| 8   |
| 3   |
| 3   |
| 1   |
| 4   |
| 5   |
| 6   |
+-----+
Output: 
+-----+
| num |
+-----+
| 6   |
+-----+
Explanation: The single numbers are 1, 4, 5, and 6.
Since 6 is the largest single number, we return it.
```

**Example 3:**

```
Input: 
MyNumbers table:
+-----+
| num |
+-----+
| 8   |
| 8   |
| 7   |
| 7   |
| 3   |
| 3   |
| 3   |
+-----+
Output: 
+------+
| num  |
+------+
| null |
+------+
Explanation: There are no single numbers in the input table so we return null.
```

---

## 题目（中文翻译）

**描述**  
表：`MyNumbers`  
单一数字（single number）是指在 `MyNumbers` 表中仅出现一次的数字。  
请找出最大的单一数字。如果不存在单一数字，返回 `null`。  
结果的格式请参考下面的示例。

**示例 1**  

| Column Name | Type |
|-------------|------|
| num         | int  |

该表可能包含重复值（换句话说，此表在 SQL 中没有主键）。每行存储一个整数。

**示例 2**  

**输入**  
`MyNumbers` 表：

```
+-----+
| num |
+-----+
| 8   |
| 8   |
| 3   |
| 3   |
| 1   |
| 4   |
| 5   |
| 6   |
+-----+
```

**输出**  

```
+-----+
| num |
+-----+
| 6   |
+-----+
```

**解释**：单一数字为 1、4、5、6。由于 6 是最大的单一数字，返回它。

**示例 3**  

**输入**  
`MyNumbers` 表：

```
+-----+
| num |
+-----+
| 8   |
| 8   |
| 7   |
| 7   |
| 3   |
| 3   |
| 3   |
+-----+
```

**输出**  

```
+------+
| num  |
+------+
| null |
+------+
```

**解释**：输入表中不存在单一数字，故返回 `null`。

**约束条件**  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一个数字都和表里其他所有数字比较一遍，看看它是否只出现一次。  
- **使用的数据结构**：只需要一个普通的 Python 列表 `nums` 来存放表中的所有 `num`。  
- **生活化类比**：把这张表想象成一堆写在纸条上的号码，我们把每张纸条和其他所有纸条逐一比对，就能判断这张纸条上的号码是否“孤单”。  
- **为什么正确**：如果一个数字在遍历完所有其他数字后，仍然没有发现相同的值，那么它必然只出现一次。把所有满足此条件的数字挑出来，取最大值，就是答案。  

#### 代码（Python）

```python
def biggest_single_number_bruteforce(nums):
    """
    暴力解法：两层循环逐个比较，找出只出现一次的数字并返回最大值。
    如果不存在只出现一次的数字，返回 None。
    """
    single_numbers = []                     # 用来收集“单身”数字

    for i in range(len(nums)):
        is_single = True                    # 假设 nums[i] 是单身数字
        for j in range(len(nums)):
            if i != j and nums[i] == nums[j]:
                # 只要在别的位置找到了相同的数，就说明它不是单身
                is_single = False
                break                       # 可以提前结束内层循环
        if is_single:
            single_numbers.append(nums[i])  # 收集所有单身数字

    # 如果没有单身数字，返回 None（对应 SQL 的 null）
    if not single_numbers:
        return None

    # 返回单身数字中的最大值
    return max(single_numbers)


# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    # 示例 1
    data1 = [8, 8, 3, 3, 1, 4, 5, 6]
    print(biggest_single_number_bruteforce(data1))   # 输出 6

    # 示例 2
    data2 = [8, 8, 7, 7, 3, 3, 3]
    print(biggest_single_number_bruteforce(data2))   # 输出 None
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  解释：外层循环遍历 `n` 次，内层循环每次最坏也要遍历 `n` 次，所以总共大约是 `n × n` 次比较。用大白话说，就是“每个人都要和所有人握手”，随着人数的增加，工作量会成平方级增长。  
- **空间复杂度**：`O(1)`（不计输出列表）  
  解释：除了保存输入的列表外，只用了常数个额外变量 `is_single`、`i`、`j`，占用的空间几乎不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们把每个数字都要和所有其它数字比较一次，这导致了二次方的时间。  
我们可以把“看一遍就知道出现几次”这件事交给 **哈希表**（在 Python 中叫 `dict`）来完成：

1. **第一次遍历**：把每个数字的出现次数记录在哈希表 `cnt` 中。  
   - 哈希表的查找/插入都是 `O(1)`，所以遍历一次就能把所有计数算好。  
   - 类比：把所有纸条上的号码写进一本“号码簿”，每出现一次就在对应的页码上加一。这样我们只需要翻一次书，就知道每个号码出现了多少次。  

2. **第二次遍历**：从哈希表里挑出出现次数恰好为 `1` 的数字，取最大值。  
   - 只需要一次线性扫描，时间同样是 `O(n)`。  

如果没有出现一次的数字，直接返回 `None`（对应 SQL 的 `null`）。

#### 代码（Python）

```python
def biggest_single_number_optimal(nums):
    """
    最优解：利用哈希表（字典）统计出现次数，再取出现一次的最大值。
    时间 O(n)，空间 O(n)。
    """
    # 第一步：统计每个数字出现的次数
    cnt = {}                     # 哈希表，键是数字，值是出现次数
    for num in nums:
        # cnt.get(num, 0) 的意思是：如果 num 不在表里，返回 0；否则返回它当前的计数
        cnt[num] = cnt.get(num, 0) + 1

    # 第二步：遍历哈希表，找出出现一次的数字的最大值
    max_single = None            # 用来保存当前找到的最大单身数字
    for num, frequency in cnt.items():
        if frequency == 1:       # 只出现一次的才算“单身”
            if (max_single is None) or (num > max_single):
                max_single = num

    return max_single   # 如果没有单身数字，仍然是 None（相当于 SQL 的 null）


# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    data1 = [8, 8, 3, 3, 1, 4, 5, 6]
    print(biggest_single_number_optimal(data1))   # 输出 6

    data2 = [8, 8, 7, 7, 3, 3, 3]
    print(biggest_single_number_optimal(data2))   # 输出 None
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  解释：我们只遍历了两遍列表（一次统计，一次找最大），每一次的工作量和元素个数成正比。用生活化的话说，就是“只需要把所有纸条一次性收进号码簿，再一次性翻看号码簿”，不会出现“每个人都要和每个人握手”的情况。  
- **空间复杂度**：`O(n)`  
  解释：哈希表里要存放每个不同数字的计数，最坏情况下所有数字都不相同，需要 `n` 条记录。相当于我们准备了一本和纸条数量一样厚的“号码簿”。  

相比暴力解，时间从 `n²` 降到了 `n`，在数据量大时提升非常明显；空间多用了一个哈希表，代价在本题是可以接受的。

---

## 心得

- **核心技巧**：利用哈希表（字典）统计出现次数，然后筛选出满足条件的元素。  
- **适用的题型**  
  1. “出现次数唯一的数字” 类似题（如 LeetCode 136 Single Number）  
  2. “统计出现次数并找出出现最多/最少的元素” （如统计字符出现频率）  
  3. “找出只出现一次的元素并返回它们的集合” （如 LeetCode 287 Find the Duplicate Number 的逆向思路）  
- **一句话总结**：**把“出现几次”交给哈希表，一遍统计一次遍历即可得到答案。**

---

## 反思

- **第一反应**：看到“只出现一次的最大数”，马上想到要统计每个数的出现次数。  
- **最容易踩的坑**  
  - **忘记处理空结果**：如果没有单身数字，直接返回 `None`（SQL 中的 `null`），否则会出现 `max()` 报错。  
  - **误把列表本身当成哈希表**：直接使用 `list.count()` 在循环里会导致 `O(n²)`，失去优化的意义。  
  - **边界条件**：只有一条记录或全部相同的情况，都要确保代码返回正确的 `None` 或该唯一数字。  
- **下次遇到同类题**：第一步先想“我能用哈希表一次遍历把所有信息收集完吗？”如果可以，后面就只需要在哈希表里筛选满足条件的元素。