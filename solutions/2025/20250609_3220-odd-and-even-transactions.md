# #3220. 奇数与偶数交易 / Odd and Even Transactions

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/odd-and-even-transactions/)

---

## 题目（英文原版）

**Description**

Table: transactions
Write a solution to find the sum of amounts for odd and even transactions for each day. If there are no odd or even transactions for a specific date, display as 0.
Return the result table ordered by transaction_date in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+------------------+------+
| Column Name      | Type | 
+------------------+------+
| transaction_id   | int  |
| amount           | int  |
| transaction_date | date |
+------------------+------+
The transactions_id column uniquely identifies each row in this table.
Each row of this table contains the transaction id, amount and transaction date.
```

**Example 2:**

```
+----------------+--------+------------------+
| transaction_id | amount | transaction_date |
+----------------+--------+------------------+
| 1              | 150    | 2024-07-01       |
| 2              | 200    | 2024-07-01       |
| 3              | 75     | 2024-07-01       |
| 4              | 300    | 2024-07-02       |
| 5              | 50     | 2024-07-02       |
| 6              | 120    | 2024-07-03       |
+----------------+--------+------------------+
```

**Example 3:**

```
+------------------+---------+----------+
| transaction_date | odd_sum | even_sum |
+------------------+---------+----------+
| 2024-07-01       | 75      | 350      |
| 2024-07-02       | 0       | 350      |
| 2024-07-03       | 0       | 120      |
+------------------+---------+----------+
```

---

## 题目（中文翻译）

**表结构**：`transactions`

编写查询，统计每一天的奇数金额（odd）和偶数金额（even）之和。若某一天不存在奇数或偶数交易，结果对应列显示为 `0`。  
返回的结果表按 `transaction_date` 升序排列，列名及格式参照示例。

**说明**  
- `transaction_id` 列唯一标识表中的每一行。  
- 每行记录包含交易编号、金额 `amount` 和交易日期 `transaction_date`。  
- 统计时，金额为奇数的记入 `odd_sum`，金额为偶数的记入 `even_sum`。  

**示例**  

**示例 1：表结构**

```
+----------------+------+
| Column Name    | Type |
+----------------+------+
| transaction_id | int  |
| amount         | int  |
| transaction_date| date |
+----------------+------+
```

**示例 2：原始数据**

```
+----------------+--------+------------------+
| transaction_id | amount | transaction_date |
+----------------+--------+------------------+
| 1              | 150    | 2024-07-01       |
| 2              | 200    | 2024-07-01       |
| 3              | 75     | 2024-07-01       |
| 4              | 300    | 2024-07-02       |
| 5              | 50     | 2024-07-02       |
| 6              | 120    | 2024-07-03       |
... (已截断)
```

**示例 3：查询结果**

```
+----------------+---------+----------+
| transaction_date | odd_sum | even_sum |
+----------------+---------+----------+
| 2024-07-01       | 75      | 350      |
| 2024-07-02       | 0       | 350      |
| 2024-07-03       | 0       | 120      |
+----------------+---------+----------+
```

**约束条件**  
暂无。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有记录逐行拿出来，针对每一天再去遍历一次所有记录，分别把奇数 `transaction_id`（或 `amount` 为奇数）和偶数 `transaction_id`（或 `amount` 为偶数）的 `amount` 加起来**。  

- **数据结构**：我们把原始表格存成 `list[dict]`（每条记录是一个字典），这样就像把所有账单装进一本“账本”。  
- **哈希表类比**：如果想快速查找同一天的交易，最自然的办法是 **把日期当作键（key），把当天的所有记录放进一个列表作为值（value）**，这正是**字典（dict）**的工作方式——就像查字典时，词是 key，解释是 value。  
- **为什么正确**：我们遍历所有日期，对每个日期再遍历所有记录，检查该记录是否属于当前日期并且 `transaction_id`（或 `amount`）是奇数/偶数，符合条件就累加。所有可能的组合都被检查到了，自然能得到正确的 `odd_sum` 与 `even_sum`。  

**时间复杂度**  
- 外层遍历所有不同的日期（记为 `d`），内层遍历所有记录（记为 `n`），所以总共是 `d * n`。在最坏情况下（每条记录的日期都不相同），`d = n`，于是时间复杂度是 **O(n²)**，即“平方级”。  
- **大白话**：如果有 1000 条记录，暴力解大约要跑 1000 × 1000 = 1 000 000 次检查，随着记录数的增大，工作量会呈指数级爆炸。  

**空间复杂度**  
- 我们只用了原始数据的引用和几个临时变量，额外空间是 **O(1)**（常数级），不随 `n` 增长。  

#### 代码（Python）  

```python
# 暴力解：逐日期、逐记录累加
# 假设 transactions 是一个 list[dict]，每条记录形如
# {"transaction_id": 1, "amount": 150, "transaction_date": "2024-07-01"}

from typing import List, Dict

def odd_even_sum_bruteforce(transactions: List[Dict]) -> List[Dict]:
    # 1️⃣ 先收集所有出现过的日期
    dates = sorted({row["transaction_date"] for row in transactions})
    
    result = []                     # 最终返回的列表，每项是 {"transaction_date": ..., "odd_sum": ..., "even_sum": ...}
    for cur_date in dates:          # 对每个日期做一次完整遍历
        odd_sum, even_sum = 0, 0
        for row in transactions:   # 再遍历所有记录
            if row["transaction_date"] != cur_date:
                continue           # 不是当前日期的记录直接跳过
            # 这里我们把“奇数/偶数”定义为 transaction_id 的奇偶性
            if row["transaction_id"] % 2 == 1:   # 奇数
                odd_sum += row["amount"]
            else:                                 # 偶数
                even_sum += row["amount"]
        # 若某一天没有奇数或偶数交易，odd_sum/even_sum 已经是 0，无需额外处理
        result.append({
            "transaction_date": cur_date,
            "odd_sum": odd_sum,
            "even_sum": even_sum
        })
    return result

# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    sample = [
        {"transaction_id": 1, "amount": 150, "transaction_date": "2024-07-01"},
        {"transaction_id": 2, "amount": 200, "transaction_date": "2024-07-01"},
        {"transaction_id": 3, "amount": 75,  "transaction_date": "2024-07-01"},
        {"transaction_id": 4, "amount": 300, "transaction_date": "2024-07-02"},
        {"transaction_id": 5, "amount": 50,  "transaction_date": "2024-07-02"},
        {"transaction_id": 6, "amount": 120, "transaction_date": "2024-07-03"},
    ]
    print(odd_even_sum_bruteforce(sample))
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 每个日期都要遍历一遍所有记录，记录多了，运行时间会“平方级”增长。  
- **空间复杂度**：`O(1)` —— 只用了常数级的额外变量（结果列表除外），不随输入规模增大而显著增加。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看出，**瓶颈在于每个日期都要重新遍历整张表**。其实我们只需要 **一次遍历**，在遍历的过程中把同一天的奇数/偶数金额累加到对应的“桶”里，这样就不需要二次循环。  

- **核心技巧：哈希表（字典）一次遍历聚合**。把 **`transaction_date`** 当作键，值是一个二元组 `(odd_sum, even_sum)`，类似“每个日期对应一个小账本”。遍历到一条记录时，直接在对应的账本里加上金额，时间只花一次。  
- **类比**：想象你在超市收银，每次看到一件商品就立刻把价钱加到当天的收银机里，而不是等收完所有商品后再去找每一天的收银机再算一次。这样既省时又省力。  

**一步步推导**  
1. 初始化一个空字典 `agg = {}`。  
2. 遍历 `transactions` 中的每条记录 `row`：  
   - 取出 `date = row["transaction_date"]`。  
   - 如果 `date` 还不在 `agg`，先放进字典并初始化为 `(0, 0)`。  
   - 判断 `row["transaction_id"]` 的奇偶性：奇数则 `odd_sum += amount`，偶数则 `even_sum += amount`。  
3. 遍历结束后，`agg` 已经保存了每一天的奇偶金额总和。把它转成列表并按照日期升序返回即可。  

**时间复杂度**  
- 只遍历一次表格，**O(n)**，即“线性级”。如果有 1000 条记录，只会做 1000 次检查，随记录数线性增长，性能非常好。  

**空间复杂度**  
- 需要为每个不同的日期保存一个 `(odd_sum, even_sum)`，最坏情况下每条记录日期都不同，字典大小为 `O(d)`，其中 `d ≤ n`，所以 **O(n)** 的额外空间。  

#### 代码（Python）  

```python
# 最优解：一次遍历 + 哈希表聚合
from typing import List, Dict

def odd_even_sum_optimal(transactions: List[Dict]) -> List[Dict]:
    # 1️⃣ 用字典把同一天的奇/偶金额累计起来
    agg: Dict[str, List[int]] = {}          # key: 日期，value: [odd_sum, even_sum]

    for row in transactions:
        date = row["transaction_date"]
        amount = row["amount"]
        # 根据 transaction_id 的奇偶性决定加到哪个桶
        is_odd = row["transaction_id"] % 2 == 1

        if date not in agg:                 # 第一次遇到这一天，先创建桶
            agg[date] = [0, 0]              # [odd_sum, even_sum]

        if is_odd:
            agg[date][0] += amount          # 累加到 odd_sum
        else:
            agg[date][1] += amount          # 累加到 even_sum

    # 2️⃣ 把字典转成按日期升序的结果列表
    result = []
    for date in sorted(agg.keys()):         # sorted 让结果按日期从早到晚
        odd_sum, even_sum = agg[date]
        result.append({
            "transaction_date": date,
            "odd_sum": odd_sum,
            "even_sum": even_sum
        })
    return result

# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    sample = [
        {"transaction_id": 1, "amount": 150, "transaction_date": "2024-07-01"},
        {"transaction_id": 2, "amount": 200, "transaction_date": "2024-07-01"},
        {"transaction_id": 3, "amount": 75,  "transaction_date": "2024-07-01"},
        {"transaction_id": 4, "amount": 300, "transaction_date": "2024-07-02"},
        {"transaction_id": 5, "amount": 50,  "transaction_date": "2024-07-02"},
        {"transaction_id": 6, "amount": 120, "transaction_date": "2024-07-03"},
    ]
    print(odd_even_sum_optimal(sample))
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 只遍历一次表格，记录数翻倍，耗时也只翻倍。比暴力的 `O(n²)` 快很多。  
- **空间复杂度**：`O(d)`（`d` 为不同日期的数量），最坏 `O(n)`，因为我们需要为每一天保存两个累计值。  

---  

## 心得  

- **核心技巧**：**一次遍历 + 哈希表（字典）聚合**，即“把相同键的值直接累加”。  
- **适用的题型**  
  1. 按日期/分类统计求和、计数、求平均等（如“每日订单总额”“各城市用户数”）。  
  2. 需要把“一对多”关系压缩成“一对一”结果的聚合问题（如“每位用户的总消费”“每个部门的最高工资”）。  
- **一句话总结解题钥匙**：**“把相同属性的记录归到同一个桶里，边遍历边累计”。**  

## 反思  

- **第一反应**：看到“每一天的奇/偶交易求和”，第一时间想到“先把日期分组，再在每组内部计算”。这自然引出了分组聚合的思路。  
- **最容易踩的坑**  
  - **奇偶判断标准**：题目说“odd and even transactions”，常见理解是 `transaction_id` 的奇偶性；如果误把 `amount` 的奇偶性当作判断依据，会导致答案不符。  
  - **没有某类交易的日期**：如果当天没有奇数（或偶数）交易，必须返回 `0` 而不是 `null`，所以初始化桶为 `[0,0]` 很关键。  
  - **日期排序**：SQL 要求结果按 `transaction_date` 升序返回，Python 列表默认顺序是插入顺序，需要显式 `sorted`。  
- **下次类似题的第一步**：**先确认分组键（这里是日期），然后决定是一次遍历还是多次遍历**；如果可以在遍历时直接累计，就立刻使用哈希表实现“一遍搞定”。