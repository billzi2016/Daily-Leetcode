# #1169. 无效交易 / Invalid Transactions

> 难度：中等 · 标签：Array、Hash Table、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/invalid-transactions/)

---

## 题目（英文原版）

**Description**

A transaction is possibly invalid if:
You are given an array of strings transaction where transactions[i] consists of comma-separated values representing the name, time (in minutes), amount, and city of the transaction.
Return a list of transactions that are possibly invalid. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: transactions = ["alice,20,800,mtv","alice,50,100,beijing"]
Output: ["alice,20,800,mtv","alice,50,100,beijing"]
Explanation: The first transaction is invalid because the second transaction occurs within a difference of 60 minutes, have the same name and is in a different city. Similarly the second one is invalid too.
```

**Example 2:**

```
Input: transactions = ["alice,20,800,mtv","alice,50,1200,mtv"]
Output: ["alice,50,1200,mtv"]
```

**Example 3:**

```
Input: transactions = ["alice,20,800,mtv","bob,50,1200,mtv"]
Output: ["bob,50,1200,mtv"]
```

**Constraints**

- transactions.length <= 1000
- Each transactions[i] takes the form "{name},{time},{amount},{city}"
- Each {name} and {city} consist of lowercase English letters, and have lengths between 1 and 10.
- Each {time} consist of digits, and represent an integer between 0 and 1000.
- Each {amount} consist of digits, and represent an integer between 0 and 2000.

---

## 题目（中文翻译）

**描述**  
如果满足以下任一条件，一笔交易可能是无效的：

- 交易金额（`amount`）大于 **1000**；
- 或者在 **60** 分钟之内（包括 60 分钟），出现另一笔 **相同姓名**（`name`）但 **不同城市**（`city`）的交易。

给定一个 **字符串数组**（`array of strings`）`transactions`，其中 `transactions[i]` 由用逗号分隔的四个字段组成，分别表示 **姓名**、**时间**（以分钟计）、**金额**、**城市**。  
返回所有可能无效的交易构成的 **列表**（`list`），答案可以以任意顺序返回。

**示例 1**  
```text
Input: transactions = ["alice,20,800,mtv","alice,50,100,beijing"]
Output: ["alice,20,800,mtv","alice,50,100,beijing"]
Explanation: 第一笔交易无效，因为第二笔交易在时间差 30 分钟内（≤60），姓名相同且城市不同。同理，第二笔交易也无效。
```

**示例 2**  
```text
Input: transactions = ["alice,20,800,mtv","alice,50,1200,mtv"]
Output: ["alice,50,1200,mtv"]
```

**示例 3**  
```text
Input: transactions = ["alice,20,800,mtv","bob,50,1200,mtv"]
Output: ["bob,50,1200,mtv"]
```

**约束条件**  

- `transactions.length <= 1000`
- 每个 `transactions[i]` 的形式为 `"{name},{time},{amount},{city}"`
- `{name}` 与 `{city}` 仅由小写英文字母组成，长度在 **1** 到 **10** 之间
- `{time}` 只包含数字，表示范围在 **0** 到 **1000** 之间的整数
- `{amount}` 只包含数字，表示范围在 **0** 到 **2000** 之间的整数

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把每一笔交易都拿出来，和所有其它交易比较一次，看看是否满足 **“无效交易”** 的两个条件：

1. 金额大于 1000；  
2. 与另一笔 **同名**、**不同城市** 的交易时间相差不超过 60 分钟。

这里用到的唯一数据结构是 **列表**（list）和 **字符串的 split**。  
- `split(',')` 就像把一行“名字,时间,金额,城市”切成四块，类似把一句话拆成词语。  
- 逐个比较时，我们把每笔交易的四个字段存进四个平行数组（name、time、amount、city），这样访问时下标一致，像在“同一排的不同抽屉里取东西”。

只要遍历完所有 `i, j (i != j)` 的组合，就能判断每笔交易是否无效。  
**为什么一定正确？** 因为我们把所有可能的配对都检查了一遍，若有任意一笔满足条件，就会被标记为无效。

#### 代码（Python）

```python
from typing import List

def invalidTransactions(transactions: List[str]) -> List[str]:
    # 1️⃣ 把每笔交易拆成四个字段，分别放进四个平行列表
    names, times, amounts, cities = [], [], [], []
    for tr in transactions:
        name, time, amount, city = tr.split(',')   # 用逗号分割
        names.append(name)
        times.append(int(time))    # 转成整数方便比较
        amounts.append(int(amount))
        cities.append(city)

    n = len(transactions)
    invalid = [False] * n   # 标记每笔交易是否无效

    # 2️⃣ 两层循环，比较所有 (i, j) 配对
    for i in range(n):
        # 条件 1：金额大于 1000
        if amounts[i] > 1000:
            invalid[i] = True

        # 条件 2：同名、不同城、时间差 ≤ 60
        for j in range(n):
            if i == j:
                continue          # 不和自己比较
            if names[i] != names[j]:
                continue          # 必须同名
            if cities[i] == cities[j]:
                continue          # 必须不同城
            if abs(times[i] - times[j]) <= 60:
                invalid[i] = True
                break             # 已经满足条件，后面不必继续检查

    # 3️⃣ 把所有标记为 True 的原始字符串收集返回
    return [transactions[i] for i in range(n) if invalid[i]]
```

#### 复杂度

- **时间复杂度：** `O(N²)`  
  两层循环遍历所有配对，`N` 最多 1000，`N²` 约等于 1 000 000 次比较。  
  “`O(N²)`” 可以理解为“随着交易数量的增加，工作量会像正方形一样快速增长”。

- **空间复杂度：** `O(N)`  
  需要四个长度为 `N` 的平行列表以及一个布尔标记数组，总共线性占用空间。  
  “`O(N)`” 意味着占用的内存会随交易数量等比例增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **所有配对** 的 `N²` 次比较。  
事实上，**只需要在同一个人的交易之间比较**，而且 **时间相近（≤60）** 的交易才可能构成冲突。  

优化思路分三步：

1. **按姓名分组**：把所有同名的交易放到一起。这样不同人的交易永远不需要比较。  
2. **对每组按时间排序**：时间越接近的交易才可能满足 “相差 ≤60”。排序后，只要向后检查，超过 60 分钟的就可以直接停止。  
3. **滑动窗口（双指针）**：在排序好的列表中，用两个指针 `left`、`right` 维护一个窗口，使得窗口内所有交易的时间差 ≤60。窗口里每笔交易和 `right` 指向的交易都满足条件，只要城市不同就标记为无效。随后把 `right` 向右移动，`left` 适时收缩。

核心数据结构：

- **字典（Hash Table）**：`defaultdict(list)` 把同名交易收集在同一个列表里。字典就像一本“电话簿”，名字是键，所有对应的交易是值。查找 O(1)。
- **列表 + 排序**：每个人的交易列表按照时间升序排列，排序相当于把交易排成一条时间轴，方便一次遍历找出相邻的冲突。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def invalidTransactions(transactions: List[str]) -> List[str]:
    # 1️⃣ 解析每笔交易，同时保存原始字符串供最后返回
    parsed = []                     # 每个元素 = (name, time, amount, city, original_str)
    for tr in transactions:
        name, t, amt, city = tr.split(',')
        parsed.append((name, int(t), int(amt), city, tr))

    # 2️⃣ 按姓名分组
    groups = defaultdict(list)     # name -> list of (time, amount, city, original_str, idx)
    for idx, (name, t, amt, city, orig) in enumerate(parsed):
        groups[name].append((t, amt, city, orig, idx))

    n = len(transactions)
    invalid = [False] * n

    # 3️⃣ 对每个人的交易按时间排序并使用滑动窗口检查
    for name, lst in groups.items():
        # 按时间升序排列
        lst.sort(key=lambda x: x[0])   # x[0] 是 time

        left = 0
        # right 指针遍历整个列表
        for right in range(len(lst)):
            r_time, r_amt, r_city, r_orig, r_idx = lst[right]

            # 条件 1：金额大于 1000，立即标记
            if r_amt > 1000:
                invalid[r_idx] = True

            # 收缩 left，确保窗口内时间差 ≤ 60
            while r_time - lst[left][0] > 60:
                left += 1

            # 检查窗口内（包括 left~right-1）所有交易的城市是否不同
            for k in range(left, right):
                l_time, l_amt, l_city, l_orig, l_idx = lst[k]
                if l_city != r_city:               # 城市不同即构成冲突
                    invalid[l_idx] = True
                    invalid[r_idx] = True

    # 4️⃣ 收集所有标记为 True 的原始字符串
    return [transactions[i] for i, bad in enumerate(invalid) if bad]
```

#### 复杂度

- **时间复杂度：** `O(N log N)`  
  - 分组是 `O(N)`；  
  - 对每个名字的列表排序，总时间是所有列表长度的 `log` 之和，等价于对整体 `N` 条记录排序，故为 `O(N log N)`。  
  - 滑动窗口内部的双层循环实际上是 **线性** 的，因为每个交易最多进入和离开窗口一次。  
  与暴力解的 `O(N²)` 相比，`N` 增大时速度提升明显（例如 `N=1000` 时，`N²=1e6` 次比较 vs `N log N≈1e4` 次）。

- **空间复杂度：** `O(N)`  
  需要存储解析后的信息、分组字典以及标记数组，均与交易数成线性关系。  

---

## 心得

- **核心技巧**：把同名交易聚在一起并按时间排序，然后用 **滑动窗口（双指针）** 只比较时间相近的交易。  
- **适用的题型**  
  1. “事件冲突” 类题目，如 LeetCode 2427 *Number of Common Factors*（利用哈希分组）  
  2. “区间合并/冲突检测” 如 56 *Merge Intervals*（排序 + 双指针）  
  3. “窗口内满足条件” 如 239 *Sliding Window Maximum*（单调队列）  
- **一句话总结**：**“先把同类放一起，再用时间顺序的滑动窗口，只看相邻的可能冲突”**。

---

## 反思

- **第一反应**：直接两层循环把所有配对都检查一遍，代码简单但会超时。  
- **最容易踩的坑**  
  - **时间差的绝对值**：要使用 `abs(t1 - t2) ≤ 60`，否则只比较前后顺序会漏掉前面的交易。  
  - **同一笔交易不能自比较**：记得 `i != j`。  
  - **金额阈值**：金额 > 1000 时一定无效，别忘了单独标记。  
- **下次遇到同类题**：第一步先 **分组 + 排序**，再考虑 **滑动窗口** 或 **双指针**，把比较范围压到 O(N) 或 O(N log N)。