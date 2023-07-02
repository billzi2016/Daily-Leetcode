# #2303. 计算应缴税额 / Calculate Amount Paid in Taxes

> 难度：简单 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/calculate-amount-paid-in-taxes/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer array brackets where brackets[i] = [upperi, percenti] means that the ith tax bracket has an upper bound of upperi and is taxed at a rate of percenti. The brackets are sorted by upper bound (i.e. upperi-1 < upperi for 0 < i < brackets.length).
Tax is calculated as follows:
You are given an integer income representing the amount of money you earned. Return the amount of money that you have to pay in taxes. Answers within 10-5 of the actual answer will be accepted.

**Examples**

**Example 1:**

```
Input: brackets = [[3,50],[7,10],[12,25]], income = 10
Output: 2.65000
Explanation:
Based on your income, you have 3 dollars in the 1st tax bracket, 4 dollars in the 2nd tax bracket, and 3 dollars in the 3rd tax bracket.
The tax rate for the three tax brackets is 50%, 10%, and 25%, respectively.
In total, you pay $3 * 50% + $4 * 10% + $3 * 25% = $2.65 in taxes.
```

**Example 2:**

```
Input: brackets = [[1,0],[4,25],[5,50]], income = 2
Output: 0.25000
Explanation:
Based on your income, you have 1 dollar in the 1st tax bracket and 1 dollar in the 2nd tax bracket.
The tax rate for the two tax brackets is 0% and 25%, respectively.
In total, you pay $1 * 0% + $1 * 25% = $0.25 in taxes.
```

**Example 3:**

```
Input: brackets = [[2,50]], income = 0
Output: 0.00000
Explanation:
You have no income to tax, so you have to pay a total of $0 in taxes.
```

**Constraints**

- 1 <= brackets.length <= 100
- 1 <= upperi <= 1000
- 0 <= percenti <= 100
- 0 <= income <= 1000
- upperi is sorted in ascending order.
- All the values of upperi are unique.
- The upper bound of the last tax bracket is greater than or equal to income.

---

## 题目（中文翻译）

**题目描述**  
给定一个 **0 索引** 的二维整数数组 `brackets`，其中 `brackets[i] = [upper_i, percent_i]` 表示第 `i` 个税档（tax bracket）的上限为 `upper_i`，税率为 `percent_i`（百分比）。`brackets` 按上限递增排序（即 `upper_{i-1} < upper_i`，`0 < i < brackets.length`）。

税金的计算方式如下：

- 给定一个整数 `income` 表示你的收入金额。  
- 按照税档的上限将收入分段，对每一段分别按对应的税率计税。  
- 返回需要缴纳的税金总额。答案只要在实际值的 `10⁻⁵` 以内均视为正确。

---

**示例 1**  
```text
Input: brackets = [[3,50],[7,10],[12,25]], income = 10
Output: 2.65000
Explanation:
根据你的收入，前 3 美元落在第 1 个税档，接下来的 4 美元落在第 2 个税档，剩余的 3 美元落在第 3 个税档。
三个税档的税率分别是 50%、10% 和 25%。
总计需要缴纳 $3 * 50% + $4 * 10% + $3 * 25% = $2.65 的税金。
```

**示例 2**  
```text
Input: brackets = [[1,0],[4,25],[5,50]], income = 2
Output: 0.25000
Explanation:
根据你的收入，前 1 美元落在第 1 个税档，剩余的 1 美元落在第 2 个税档。
两个税档的税率分别是 0% 和 25%。
总计需要缴纳 $1 * 0% + $1 * 25% = $0.25 的税金。
```

**示例 3**  
```text
Input: brackets = [[2,50]], income = 0
Output: 0.00000
Explanation:
没有收入可供征税，因此需要缴纳的税金总额为 $0。
```

---

**约束条件**  

- `1 <= brackets.length <= 100`
- `1 <= upper_i <= 1000`
- `0 <= percent_i <= 100`
- `0 <= income <= 1000`
- `upper_i` 按升序排列，且各值唯一
- 最后一个税档的上限大于或等于 `income`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把收入从低到高逐段切分**，每一段落在对应的税率下计算应缴税额，然后把所有段的税额加起来。  

- **数据结构**：只需要遍历一次 `brackets`（二维列表），不需要额外的数据结构。可以把 `brackets` 想象成一本《税率手册》——每一页（`[upper, percent]`）告诉我们“到达 `upper` 元时，税率是 `percent%`”。我们从第 0 页开始，逐页查看自己已经赚了多少钱，哪一页的税率应该被用到。
- **为什么正确**：税法的定义正是把收入划分成若干区间，每个区间按固定比例收税。我们按顺序遍历区间，**每次只取该区间实际能覆盖的收入**（即 `min(income, upper) - prev`），乘以对应税率，就得到这段的税额。把所有段的税额相加，就是总税额。
- **复杂度直观解释**：  
  - **时间复杂度 O(n)**：我们只遍历一次 `brackets`，`n` 是税率区间的数量。想象成排队买票，只需要走一遍队列即可。  
  - **空间复杂度 O(1)**：只用了几个普通变量（`prev`, `tax`），不随 `n` 增长而增加内存。

#### 代码（Python）

```python
def calculateTax(brackets, income):
    """
    :param brackets: List[List[int]]  税率区间，[[upper, percent], ...]
    :param income:   int              收入
    :return: float  应缴税额（保留 5 位小数即可）
    """
    tax = 0.0          # 累计税额
    prev = 0           # 前一个区间的上限，初始为 0

    for upper, percent in brackets:
        # 本区间实际能算到的收入 = min(收入, 本区上限) - 前一区上限
        # 如果收入已经小于等于 prev，则本区不再贡献税额，直接退出循环
        if income <= prev:
            break

        # 计算本区间应税的那部分钱
        taxable = min(income, upper) - prev
        # 按百分比算税（percent 为整数，需要除以 100）
        tax += taxable * percent / 100.0

        # 更新 prev，进入下一个区间
        prev = upper

    # 按题目要求返回浮点数（Python 默认会保留足够精度）
    return tax
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次税率区间列表。  
  *含义*：如果有 100 个税率区间，最多检查 100 次；如果只有 5 个，只检查 5 次，运行时间随区间数线性增长。
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量，不随输入规模增大。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**唯一的瓶颈**是必须遍历所有税率区间才能知道每段收入对应的税率。  
- **没有更快的办法**：因为题目只给了区间列表，没有任何可以直接跳过的结构（比如前缀和、二分搜索的前置条件），我们必须至少看一次每个区间才能确认该区间是否被收入覆盖。  
- **优化点**：在遍历时，一旦发现 `income` 已经被全部覆盖，就可以**提前退出**循环，避免不必要的迭代。对已经遍历完所有区间的情况（`income` 大于等于最后一个 `upper`），仍然需要遍历完整个列表，这已经是最少的工作量。

核心算法仍是 **一次线性遍历**，但加入了 **提前结束** 的小技巧，使实际运行更快（尤其当收入远小于最高税率上限时）。

下面的代码把这一点写得更清晰，同时保留了完整的中文注释，帮助初学者理解每一步。

#### 代码（Python）

```python
def calculateTax(brackets, income):
    """
    计算应缴税额（一次线性遍历 + 提前退出）。
    """
    tax = 0.0          # 累计税额
    prev = 0           # 前一个区间的上限（起始为 0）

    for upper, percent in brackets:
        # 如果收入已经不超过 prev，说明已经全部算完，直接退出
        if income <= prev:
            break

        # 本区间真正要算的收入 = min(收入, 当前上限) - 前一个上限
        taxable = min(income, upper) - prev
        tax += taxable * percent / 100.0

        # 为下一轮做准备
        prev = upper

    return tax
```

#### 复杂度

- **时间复杂度**：`O(k)`，其中 `k` 是实际遍历的区间数，`k ≤ n`。在最坏情况下（收入覆盖所有区间），`k = n`，仍然是 `O(n)`。  
  *含义*：如果收入只落在前 2 个区间，循环只跑 2 次，比完整遍历快很多。
- **空间复杂度**：`O(1)` —— 只用常数个变量。

---

## 心得

- **核心技巧**：**区间累计**（把大问题拆成若干小区间，各自独立计算后相加）。  
- **适用的题型**：  
  1. 累计分段费用（如电费、水费计费）  
  2. 分段奖励或分段扣分（游戏闯关积分、分段折扣）  
  3. 累计分段概率/期望（概率题的分段求和）  
- **一句话总结**：把收入按税率区间“切块”，每块单独算税，最后把块的税额相加。

## 反思

- **第一反应**：看到“上限”和“税率”，自然想到“把收入切成几段”，每段乘对应的百分比。  
- **最容易踩的坑**：  
  - 忘记在每段计算时用 `min(income, upper)`，导致超过收入的上限仍被计税。  
  - 忽略 `prev` 的更新，导致后面的区间重复计税。  
  - 税率是百分数，需要除以 `100`（否则会把 50 当成 5000%）。  
- **下次遇到同类题**：第一步先**确定分段规则**（上限、下限、比例），再**遍历区间并在每段取实际收入的交集**，最后累计结果。这样思路清晰，代码自然不会出错。