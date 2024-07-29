# #2806. **四舍五入购买后的账户余额** / Account Balance After Rounded Purchase

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/account-balance-after-rounded-purchase/)

---

## 题目（英文原版）

**Description**

Initially, you have a bank account balance of 100 dollars.
You are given an integer purchaseAmount representing the amount you will spend on a purchase in dollars, in other words, its price.
When making the purchase, first the purchaseAmount is rounded to the nearest multiple of 10. Let us call this value roundedAmount. Then, roundedAmount dollars are removed from your bank account.
Return an integer denoting your final bank account balance after this purchase.
Notes:

**Examples**

**Example 1:**

```
Input: purchaseAmount = 9
Output: 90
Explanation:
The nearest multiple of 10 to 9 is 10. So your account balance becomes 100 - 10 = 90.
```

**Example 2:**

```
Input: purchaseAmount = 15
Output: 80
Explanation:
The nearest multiple of 10 to 15 is 20. So your account balance becomes 100 - 20 = 80.
```

**Example 3:**

```
Input: purchaseAmount = 10
Output: 90
Explanation:
10 is a multiple of 10 itself. So your account balance becomes 100 - 10 = 90.
```

**Constraints**

- 0 <= purchaseAmount <= 100

---

## 题目（中文翻译）

最初，你的银行账户余额为 100 美元。  
给定一个整数 `purchaseAmount`，表示你将要进行的购买金额（单位：美元），即商品的价格。  
在进行购买时，首先将 `purchaseAmount` 四舍五入到最近的 10 的倍数（nearest multiple of 10），记为 `roundedAmount`。随后，从你的银行账户中扣除 `roundedAmount` 美元。  
返回一个整数，表示完成此购买后的最终账户余额。

**示例 1**  
输入: `purchaseAmount = 9`  
输出: `90`  
解释:  
最近的 10 的倍数是 10。因此账户余额变为 `100 - 10 = 90`。

**示例 2**  
输入: `purchaseAmount = 15`  
输出: `80`  
解释:  
最近的 10 的倍数是 20。因此账户余额变为 `100 - 20 = 80`。

**示例 3**  
输入: `purchaseAmount = 10`  
输出: `90`  
解释:  
10 本身就是 10 的倍数。因此账户余额变为 `100 - 10 = 90`。

**约束条件**  
- `0 <= purchaseAmount <= 100`   (purchaseAmount 为整数)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的 10 的倍数**（0、10、20 … 100）都列出来，和 `purchaseAmount` 比较谁更近，最近的那个就是 `roundedAmount`。  

- **数据结构**：我们只需要一个普通的 `list`（或者直接用 `range` 生成）来存放这些倍数。可以把它想象成一本《十进制倍数手册》，每一页记着一个可能的金额。  
- **正确性**：因为题目限制 `purchaseAmount ≤ 100`，所有合法的四舍五入结果必定落在 0~100 之间，而我们检查的每一个倍数都在这个区间内，所以必能找到最近的那一个。  
- **时间/空间复杂度**：我们最多检查 11 个数（0~100 步长 10），所以时间是 **O(11) ≈ O(1)**，空间只用了常数个变量，也是 **O(1)**。这里的 “O(1)” 可以理解为“无论输入多大，耗时和占用的内存基本不变”。

#### 代码（Python）

```python
def account_balance_bruteforce(purchaseAmount: int) -> int:
    """
    暴力实现：遍历所有 10 的倍数，找到与 purchaseAmount 最近的那个。
    如果出现两个距离相同的倍数（如 5），取较大的那一个。
    """
    # 所有可能的 10 的倍数（0, 10, 20, ..., 100）
    candidates = range(0, 101, 10)

    # 用来记录当前找到的最近倍数以及它与 purchaseAmount 的距离
    best = None          # 最近的倍数
    best_diff = None     # 对应的最小距离

    for x in candidates:
        diff = abs(x - purchaseAmount)   # 计算距离

        # 第一次循环直接把当前 x 设为最优
        if best is None:
            best, best_diff = x, diff
            continue

        # 如果发现更小的距离，更新
        if diff < best_diff:
            best, best_diff = x, diff
        # 距离相等且 x 更大（题目要求取较大的），也要更新
        elif diff == best_diff and x > best:
            best = x

    # 初始账户为 100，扣掉最近的倍数即为最终余额
    return 100 - best
```

#### 复杂度

- **时间复杂度**：`O(1)`（固定检查 11 次，和输入大小无关）。  
- **空间复杂度**：`O(1)`（只用了常数个临时变量）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈其实不大，因为检查的次数固定。但我们可以用数学公式一步算出最近的 10 的倍数，省掉循环，代码更简洁、直观。

1. **观察**：把 `purchaseAmount` 加上 5 再除以 10（向下取整），得到的就是四舍五入后的“十位”。  
   - 例如 `purchaseAmount = 9` → `(9 + 5) // 10 = 1` → `1 * 10 = 10`。  
   - 再比如 `purchaseAmount = 15` → `(15 + 5) // 10 = 2` → `2 * 10 = 20`。  
2. **公式**：  

   \[
   \text{roundedAmount} = \left\lfloor\frac{\text{purchaseAmount}+5}{10}\right\rfloor \times 10
   \]

   这里的 `//` 在 Python 中就是向下取整的除法。  
3. **解释**：把 `purchaseAmount` 往右平移一位（除以 10），再往左平移回来（乘以 10），在除之前先加 5 相当于“四舍五入”。如果正好在两边中间（比如 5、15、25 …），加 5 后会向上进位，从而得到**较大的**那个倍数，正好满足题目要求。  
4. **最终余额**：`100 - roundedAmount`。

#### 代码（Python）

```python
def account_balance_optimal(purchaseAmount: int) -> int:
    """
    最优实现：使用四舍五入的数学公式直接求出最近的 10 的倍数。
    """
    # (purchaseAmount + 5) // 10 相当于四舍五入到最近的十位
    rounded = ((purchaseAmount + 5) // 10) * 10
    # 初始余额 100，扣除 rounded 即为最终余额
    return 100 - rounded
```

#### 复杂度

- **时间复杂度**：`O(1)` — 只做了几次算术运算，和输入大小完全无关。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量。

相比暴力解，最优解去掉了循环，代码更短、更易读，运行速度也更快（虽然在本题里差别几乎不可感知，但在更大规模的问题上，这种 **常数时间** 的优势会非常明显）。

---

## 心得

- **核心技巧**：利用整数除法的特性实现“四舍五入”。  
- **适用的题型**：  
  1. “把数字四舍五入到最近的 k 的倍数” （如 5、10、100 等）。  
  2. “计算最近的整十、整百、整千等” 的金融或计量问题。  
  3. “把坐标点映射到最近的格点” 的网格问题。  
- **解题钥匙**：把“最近的倍数”转化为“先除后乘”，并在除之前加上 **半个单位**（这里是 5），即可一次算出答案。

---

## 反思

- **第一反应**：看到“最近的 10 的倍数”，立刻想到遍历所有可能的倍数去比较。  
- **最容易踩的坑**：  
  - **平局取大**：如果直接用 `round()`（Python 的四舍五入）会在 `.5` 时向偶数取整，导致错误。必须手动加上 `5` 再除以 `10`，保证向上取整。  
  - **边界情况**：`purchaseAmount = 0` 或 `100` 时公式仍然适用，但要确保不会出现负数或超过 100 的扣款。  
- **下次思路**：遇到 “四舍五入到最近的某个基数” 时，先想 “加半个基数后整除”，再乘回基数，几乎可以直接写出公式，避免循环。