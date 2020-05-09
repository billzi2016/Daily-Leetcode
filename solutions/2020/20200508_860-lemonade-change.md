# #860. 柠檬水找零 / Lemonade Change

> 难度：简单 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/lemonade-change/)

---

## 题目（英文原版）

**Description**

At a lemonade stand, each lemonade costs $5. Customers are standing in a queue to buy from you and order one at a time (in the order specified by bills). Each customer will only buy one lemonade and pay with either a $5, $10, or $20 bill. You must provide the correct change to each customer so that the net transaction is that the customer pays $5.
Note that you do not have any change in hand at first.
Given an integer array bills where bills[i] is the bill the ith customer pays, return true if you can provide every customer with the correct change, or false otherwise.

**Examples**

**Example 1:**

```
Input: bills = [5,5,5,10,20]
Output: true
Explanation: 
From the first 3 customers, we collect three $5 bills in order.
From the fourth customer, we collect a $10 bill and give back a $5.
From the fifth customer, we give a $10 bill and a $5 bill.
Since all customers got correct change, we output true.
```

**Example 2:**

```
Input: bills = [5,5,10,10,20]
Output: false
Explanation: 
From the first two customers in order, we collect two $5 bills.
For the next two customers in order, we collect a $10 bill and give back a $5 bill.
For the last customer, we can not give the change of $15 back because we only have two $10 bills.
Since not every customer received the correct change, the answer is false.
```

**Constraints**

- 1 <= bills.length <= 105
- bills[i] is either 5, 10, or 20.

---

## 题目（中文翻译）

在一家柠檬水摊位，每杯柠檬水的售价为 **$5**。顾客按队列（queue）顺序依次购买（顺序由 `bills` 指定）。每位顾客只购买一杯柠檬水，并且只会使用 **$5、$10 或 $20** 的钞票支付。你必须为每位顾客找零，使得交易的净额为顾客实际支付 **$5**。

> 注意：开始时你手中没有任何零钱。

给定一个整数数组（integer array）`bills`，其中 `bills[i]` 表示第 `i` 位顾客支付的钞票面额。如果你能够为所有顾客提供正确的找零，返回 `true`；否则返回 `false`。

---

### 示例

#### 示例 1
**Input:** `bills = [5,5,5,10,20]`  
**Output:** `true`  
**Explanation:**  
- 前 3 位顾客各支付 **$5**，你收到了三张 **$5**。  
- 第 4 位顾客支付 **$10**，你找回 **$5**（使用一张 **$5**）。  
- 第 5 位顾客支付 **$20**，你找回 **$10** 和 **$5**（使用一张 **$10** 和一张 **$5**）。  
所有顾客都得到了正确的找零，返回 `true`。

#### 示例 2
**Input:** `bills = [5,5,10,10,20]`  
**Output:** `false`  
**Explanation:**  
- 前两位顾客各支付 **$5**，你收到了两张 **$5**。  
- 接下来的两位顾客各支付 **$10**，你分别找回 **$5**（使用一张 **$5**），此时手中剩下两张 **$10**。  
- 最后一位顾客支付 **$20**，你需要找回 **$15**，但手中只有两张 **$10**，无法凑成 **$15**。  
并非所有顾客都得到正确的找零，返回 `false`。

---

### 约束条件
- `1 <= bills.length <= 10^5`
- `bills[i]` 只能是 **5、10** 或 **20**。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把手里所有收到的钞票都记下来**，每当有顾客付钱时，就遍历这些钞票，尝试找出任意一种组合，使得找零金额恰好等于 `付的钱 - 5`。  

- **数据结构**：可以用一个列表 `cash` 来存放已经收到的每张钞票（`5、10、20`）。列表就像是我们手里的一沓零钱，想要找零时就把它们一张张翻出来尝试。  
- **正确性**：只要遍历所有可能的找零组合，就一定能判断出是否能够找零成功（如果有一种组合能凑出所需金额，就说明可以）。  
- **时间/空间复杂度**：  
  - 对于每位顾客，我们可能要检查 `cash` 中的所有钞票，最坏情况是遍历 `O(n)` 次（`n` 为顾客数）。  
  - 再加上遍历所有子集的组合（这里我们用最简单的“从大到小依次使用”模拟），整体时间复杂度会退化到 **`O(n²)`**。  
  - 空间上只需要保存已经收到的钞票，最多 `n` 张，**`O(n)`** 的额外空间。

> **大白话解释**：  
> `O(n²)` 就像是你要给 `n` 个人每个人都要检查 `n` 次——如果 `n=10,000`，检查次数就会达到一亿次，显然太慢了。

#### 代码（Python）

```python
def lemonadeChange_bruteforce(bills):
    # cash 用来记录已经收到了哪些钞票，顺序随收进来的顺序
    cash = []

    for bill in bills:
        need = bill - 5                     # 需要找零的金额

        # ---------- 暴力找零 ----------
        # 我们从大面额往小面额尝试使用，直到凑够 need 为止
        # 这里的实现仍然是贪心的，只是每次都遍历 cash，时间是 O(n²)
        while need > 0:
            # 先找 10 元（如果有的话），否则找 5 元
            if 10 in cash and need >= 10:
                cash.remove(10)             # 把一张 10 元从手里取走
                need -= 10
            elif 5 in cash and need >= 5:
                cash.remove(5)              # 把一张 5 元取走
                need -= 5
            else:                           # 没有合适的钞票可以找零
                return False

        # 找零成功后，把当前顾客付的钞票放进 cash
        cash.append(bill)

    return True
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 对每位顾客都要遍历已经收的钞票，最坏情况是 `1 + 2 + … + n ≈ n²/2` 次操作。  
- **空间复杂度**：`O(n)` —— 最多保存所有已经收的钞票。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次找零都要遍历所有已有钞票**。其实我们不需要知道每张具体的钞票，只要知道**有多少张 5 元和 10 元**就足够了，因为找零的金额最多是 15（`20 - 5`），而且 **只会用到 5 元和 10 元**（我们从不需要找零 20 元）。

于是可以使用 **计数法（greedy）**：

1. 维护两个计数器  
   - `cnt5`：手里有多少张 5 元  
   - `cnt10`：手里有多少张 10 元  

2. 按照顾客顺序处理  
   - **付 5 元**：不需要找零，只把 `cnt5 += 1`。  
   - **付 10 元**：必须找一张 5 元，若 `cnt5 == 0` 则失败；否则 `cnt5 -= 1, cnt10 += 1`。  
   - **付 20 元**：需要找 15 元，**优先使用一张 10 元 + 一张 5 元**（这样可以保留更多的 5 元，后面的顾客更容易找零），如果没有 10 元，则只能使用 **三张 5 元**。若两种组合都不可行，直接返回 `False`。  

3. 循环结束后，如果每位顾客都成功找零，返回 `True`。

> **为什么优先用 10+5 而不是 5+5+5？**  
> 因为 5 元是找零的“万能货币”，后面可能会出现付 10 元的顾客，需要用到 5 元。如果把所有 5 元都用掉，只剩 10 元，后面就可能卡住。把一张 10 元换出来后，手里还能保留更多的 5 元，安全系数更高。

#### 代码（Python）

```python
def lemonadeChange(bills):
    """
    使用计数的贪心算法，时间 O(n)，空间 O(1)
    """
    cnt5, cnt10 = 0, 0          # 记录手里有多少张 5 元和 10 元

    for bill in bills:
        if bill == 5:           # 顾客直接付 5 元
            cnt5 += 1
        elif bill == 10:        # 需要找 5 元
            if cnt5 == 0:       # 没有 5 元找零，失败
                return False
            cnt5 -= 1
            cnt10 += 1
        else:  # bill == 20，需要找 15 元
            # 优先使用 10 + 5
            if cnt10 > 0 and cnt5 > 0:
                cnt10 -= 1
                cnt5 -= 1
            # 否则只能使用 5 + 5 + 5
            elif cnt5 >= 3:
                cnt5 -= 3
            else:               # 两种方式都不行，失败
                return False

    return True
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，每位顾客的处理都是 **常数时间**（几次加减判断）。  
  - 与暴力解的 `O(n²)` 对比，速度提升了 **近乎 `n` 倍**，在 `n=10⁵` 时也能轻松跑完。  
- **空间复杂度**：`O(1)` —— 只用了两个整数计数器，和输入规模无关。

---

## 心得

- **核心技巧**：**贪心 + 计数**——只记录关键面额的数量，按“先保留小面额” 的原则给找零。  
- **适用的题型**：  
  1. “零钱兑换” 类问题（如 **`Can Place Flowers`**、**`Fruit Into Baskets`**）  
  2. “资源分配” 类的贪心题（如 **`Assign Cookies`**、**`Boats to Save People`**）  
- **解题钥匙**：**“只保留最有价值的资源”**——在找零场景下，5 元是最有价值的，尽量不要一次性把它们全部用掉。

---

## 反思

- **第一反应**：看到只会出现 `5、10、20` 三种面额，马上想到“只需要统计 5 和 10 的数量”。  
- **最容易踩的坑**：  
  - 忘记在付 20 元时优先使用 `10+5`，导致在某些测试用例（如 `[5,5,5,10,20]`）仍能通过，但在更复杂的序列上会误判。  
  - 边界条件：只有一位顾客且付 10 元或 20 元时，需要立刻返回 `False`。  
- **下次思路**：遇到“找零 / 资源分配”这类题目，第一步先**统计关键资源的数量**，再思考**如何用最少的消耗满足需求**，这往往能直接导出 O(n) 的贪心解。