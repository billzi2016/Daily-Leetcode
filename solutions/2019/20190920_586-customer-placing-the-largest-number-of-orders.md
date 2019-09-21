# #586. 下单次数最多的客户 / Customer Placing the Largest Number of Orders

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/customer-placing-the-largest-number-of-orders/)

---

## 题目（英文原版）

**Description**

Table: Orders
Write a solution to find the customer_number for the customer who has placed the largest number of orders.
The test cases are generated so that exactly one customer will have placed more orders than any other customer.
The result format is in the following example.
Follow up: What if more than one customer has the largest number of orders, can you find all the customer_number in this case?

**Examples**

**Example 1:**

```
+-----------------+----------+
| Column Name     | Type     |
+-----------------+----------+
| order_number    | int      |
| customer_number | int      |
+-----------------+----------+
order_number is the primary key (column with unique values) for this table.
This table contains information about the order ID and the customer ID.
```

**Example 2:**

```
Input: 
Orders table:
+--------------+-----------------+
| order_number | customer_number |
+--------------+-----------------+
| 1            | 1               |
| 2            | 2               |
| 3            | 3               |
| 4            | 3               |
+--------------+-----------------+
Output: 
+-----------------+
| customer_number |
+-----------------+
| 3               |
+-----------------+
Explanation: 
The customer with number 3 has two orders, which is greater than either customer 1 or 2 because each of them only has one order. 
So the result is customer_number 3.
```

---

## 题目（中文翻译）

**表：Orders**  
编写一个查询，找出下单次数（order count）最多的客户的 **客户编号（customer_number）**。  
测试数据保证恰好有一位客户的订单数量超过所有其他客户。  
结果格式请参照下方示例。

**进阶**：如果有不止一位客户拥有相同的最大订单数量，能否找出所有的 **客户编号（customer_number）**？

---

### 示例 1

```sql
+-----------------+----------+
| Column Name     | Type     |
+-----------------+----------+
| order_number    | int      |
| customer_number | int      |
+-----------------+----------+
```

`order_number` 是该表的主键（primary key），即唯一值列。  
该表记录了订单 ID 与对应的客户 ID。

### 示例 2

**输入**  
Orders 表：

| order_number | customer_number |
|--------------|-----------------|
| 1            | 1               |
| 2            | 2               |
| 3            | 3               |
| 4            | 3               |

**输出**

| customer_number |
|-----------------|
| 3               |

**解释**  
客户编号为 3 的客户拥有两条订单记录，超过客户 1 和客户 2 各自只有一条订单记录的情况。  
因此查询结果返回客户编号 3。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 **Orders** 表中的每一条记录都拿出来，统计每个 `customer_number` 出现了多少次（也就是该顾客下了多少单）。  
这一步可以用 **哈希表**（在 Python 里用 `dict`）来实现，哈希表就像一本“查字典”，我们把 `customer_number` 当作“词”，把它对应的订单数量当作“页码”。  

具体步骤：

1. 遍历整张表（每条记录一次），把 `customer_number` 作为键，计数器 `+1` 作为值，放进字典。  
2. 字典遍历完后，找到计数最大的那个键，就是下单最多的顾客。  
3. 题目保证只有一个顾客的订单数是最大的，所以直接返回即可。

这个方法一定能得到正确答案，因为我们把所有订单都算进来了，没漏也没重复。

**时间/空间复杂度**  
- 时间复杂度 `O(n)`：我们只遍历一次表，`n` 是表的行数。  
- 空间复杂度 `O(k)`：需要额外的哈希表存放每个不同顾客的计数，`k` 是顾客的种类数，最坏情况下 `k ≤ n`。

> 大白话解释：如果表里有 1000 条订单，程序大概会跑 1000 步；如果有 200 位不同的顾客，需要额外记住 200 条计数信息。

#### 代码（Python）

```python
from typing import List, Tuple

def customer_with_most_orders_brute(orders: List[Tuple[int, int]]) -> int:
    """
    暴力（最直接）解法
    :param orders: List[(order_number, customer_number)]
    :return: 下单最多的 customer_number
    """
    # 用 dict 统计每个顾客的订单数量，类似查字典
    cnt = {}                       # key: customer_number, value: order count
    for _, cust in orders:        # 遍历每一条记录，_ 表示我们不需要 order_number
        cnt[cust] = cnt.get(cust, 0) + 1   # 如果 cust 已经出现过就加一，否则初始化为 1

    # 找到计数最大的顾客
    max_customer = None
    max_cnt = -1
    for cust, c in cnt.items():
        if c > max_cnt:            # 只要比当前最大值大，就更新
            max_cnt = c
            max_customer = cust

    return max_customer
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次表，`n` 为订单数量。  
- **空间复杂度**：`O(k)` — 需要保存每个不同顾客的计数，`k` 为顾客种类数，最坏 `k = n`。

---

### 2. 最优解

#### 思路  

从暴力解看，唯一的“瓶颈”是我们用了普通的 `dict` 来计数，然后再遍历一次字典找最大值。其实这两步可以合并为一步：**在统计的同时维护当前的最大值**。  

这样做的好处是：

- **不需要再遍历字典** 找最大值，省掉一次 `O(k)` 的循环。  
- 逻辑更简洁，代码只用一次遍历即可得到答案。

核心数据结构仍然是 **哈希表**，因为我们必须要把同一个顾客的订单累计起来。这里不需要其他高级结构（如堆、前缀和等），只要在计数的同时记录最大值即可。

实现思路：

1. 初始化 `max_customer = None, max_cnt = 0`。  
2. 遍历每条记录，更新 `cnt[cust]`。  
3. 每次更新后，比较 `cnt[cust]` 与 `max_cnt`，如果更大就同步更新 `max_customer` 与 `max_cnt`。  
4. 循环结束后，`max_customer` 就是答案。

**时间/空间复杂度**  
- 时间复杂度仍然是 `O(n)`，但只进行一次遍历（不再额外遍历字典）。  
- 空间复杂度仍是 `O(k)`，因为哈希表必须保留所有顾客的计数。

> 与暴力解对比：时间上没有数量级的提升（都是线性），但实际运行时会快一点，因为省掉了遍历字典的那一步。

#### 代码（Python）

```python
from typing import List, Tuple

def customer_with_most_orders_opt(orders: List[Tuple[int, int]]) -> int:
    """
    最优解：在计数的同时维护最大值
    :param orders: List[(order_number, customer_number)]
    :return: 下单最多的 customer_number
    """
    cnt = {}
    max_customer = None
    max_cnt = 0

    for _, cust in orders:
        # 累计该顾客的订单数
        cnt[cust] = cnt.get(cust, 0) + 1

        # 同时检查是否已经成为新的最大值
        if cnt[cust] > max_cnt:
            max_cnt = cnt[cust]
            max_customer = cust

    return max_customer
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次表，且不再额外遍历字典。  
- **空间复杂度**：`O(k)` — 仍需保存每位顾客的计数。

---

## 心得

- **核心技巧**：使用哈希表累计出现次数，同时在遍历过程中维护当前最大值。  
- **适用的题型**：  
  1. “出现次数最多的元素”类问题（如 LeetCode 169. Majority Element）。  
  2. “统计每类出现频率并找出最高/最低”类（如统计单词出现次数，找出出现频率最高的单词）。  
  3. “排行榜”类（如求分数最高的学生、销售额最高的商品等）。  
- **一句话总结解题钥匙**：**在统计的同时“边走边比较”，把两步合并成一步**。

## 反思

- **第一反应**：看到“统计每个顾客的订单数”，立刻想到用字典计数。  
- **最容易踩的坑**：  
  - 忽略了 `order_number` 只是唯一标识，不参与统计。  
  - 没考虑 “多位顾客并列第一”的情况（题目原版保证唯一，进阶可返回所有最大者）。  
  - 对空表的处理：若表为空，应返回 `None` 或抛异常，防止 `max_customer` 未被赋值。  
- **下次遇到同类题**：第一步先**明确统计对象**（这里是 `customer_number`），然后**决定是否需要在统计时同步维护极值**，这样往往能一次遍历搞定。