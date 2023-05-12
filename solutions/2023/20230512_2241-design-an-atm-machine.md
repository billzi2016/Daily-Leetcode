# #2241. 设计 ATM 机 / Design an ATM Machine

> 难度：中等 · 标签：Array、Greedy、Design · [LeetCode 链接](https://leetcode.com/problems/design-an-atm-machine/)

---

## 题目（英文原版）

**Description**

There is an ATM machine that stores banknotes of 5 denominations: 20, 50, 100, 200, and 500 dollars. Initially the ATM is empty. The user can use the machine to deposit or withdraw any amount of money.
When withdrawing, the machine prioritizes using banknotes of larger values.
Implement the ATM class:

**Examples**

**Example 1:**

```
Input
["ATM", "deposit", "withdraw", "deposit", "withdraw", "withdraw"]
[[], [[0,0,1,2,1]], [600], [[0,1,0,1,1]], [600], [550]]
Output
[null, null, [0,0,1,0,1], null, [-1], [0,1,0,0,1]]

Explanation
ATM atm = new ATM();
atm.deposit([0,0,1,2,1]); // Deposits 1 $100 banknote, 2 $200 banknotes,
                          // and 1 $500 banknote.
atm.withdraw(600);        // Returns [0,0,1,0,1]. The machine uses 1 $100 banknote
                          // and 1 $500 banknote. The banknotes left over in the
                          // machine are [0,0,0,2,0].
atm.deposit([0,1,0,1,1]); // Deposits 1 $50, $200, and $500 banknote.
                          // The banknotes in the machine are now [0,1,0,3,1].
atm.withdraw(600);        // Returns [-1]. The machine will try to use a $500 banknote
                          // and then be unable to complete the remaining $100,
                          // so the withdraw request will be rejected.
                          // Since the request is rejected, the number of banknotes
                          // in the machine is not modified.
atm.withdraw(550);        // Returns [0,1,0,0,1]. The machine uses 1 $50 banknote
                          // and 1 $500 banknote.
```

**Constraints**

- banknotesCount.length == 5
- 0 <= banknotesCount[i] <= 109
- 1 <= amount <= 109
- At most 5000 calls in total will be made to withdraw and deposit.
- At least one call will be made to each function withdraw and deposit.
- Sum of banknotesCount[i] in all deposits doesn't exceed 109

---

## 题目（中文翻译）

**描述**  
有一台 ATM 机，用来存放 5 种面额的钞票（banknote）：20、50、100、200 和 500 美元。最初 ATM 机为空。用户可以使用该机器进行存款（deposit）或取款（withdraw），取款时机器会优先使用面额更大的钞票。

请实现 `ATM` 类，使其能够完成上述功能。

**实现细节**  
- `ATM()`：初始化一个空的 ATM 机。  
- `void deposit(int[] banknotesCount)`：向 ATM 机中存入指定数量的钞票。`banknotesCount[i]` 表示面额为 `[20, 50, 100, 200, 500]` 的钞票数量。  
- `int[] withdraw(int amount)`：尝试取出总额为 `amount` 的现金。若成功，返回一个长度为 5 的数组，表示实际取出的每种面额钞票数量；若无法满足取款请求，返回 `[-1]`。取款时应尽可能使用面额更大的钞票。

**示例**  

```text
输入
["ATM", "deposit", "withdraw", "deposit", "withdraw", "withdraw"]
[[], [[0,0,1,2,1]], [600], [[0,1,0,1,1]], [600], [550]]
输出
[null, null, [0,0,1,0,1], null, [-1], [0,1,0,0,1]]
```

**解释**  
```java
ATM atm = new ATM();
atm.deposit([0,0,1,2,1]); // 存入 1 张 100 美元钞票、2 张 200 美元钞票和 1 张 500 美元钞票。
atm.withdraw(600);        // 返回 [0,0,1,0,1]，即取出 1 张 100 美元和 1 张 500 美元。
atm.deposit([0,1,0,1,1]); // 再次存入 1 张 50 美元、1 张 200 美元和 1 张 500 美元。
atm.withdraw(600);        // 由于机器中已无足够面额更大的钞票组合满足 600 美元，返回 [-1]。
atm.withdraw(550);        // 返回 [0,1,0,0,1]，即取出 1 张 50 美元和 1 张 500 美元。
```

**约束条件**  
- `banknotesCount.length == 5`  
- `0 <= banknotesCount[i] <= 10^9`  
- `1 <= amount <= 10^9`  
- `withdraw` 和 `deposit` 的调用总次数不超过 5000 次。  
- 至少会各调用一次 `withdraw` 和 `deposit`。  
- 所有存款中 `banknotesCount[i]` 的总和不超过 `10^9`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的纸币组合枚举一遍**，看看哪一种恰好等于用户要取的 `amount`，并且满足「优先使用面值大的纸币」这一规则。  

- **使用的数据结构**：  
  - `banknotesCount`：长度为 5 的数组，记录 ATM 中每种面值纸币的剩余数量。可以把它想象成「银行的纸币仓库」，下标 0~4 分别对应 20、50、100、200、500 美元。  
  - `denoms`：同样长度为 5 的数组，存放纸币的面值 `[20, 50, 100, 200, 500]`，相当于「纸币的标签」。
- **为什么正确**：  
  - 只要遍历所有合法的取钱方案（即每种面值取的张数不超过当前库存），就一定能找到满足「金额相等」且「面值大的纸币尽可能多」的组合。  
  - 只要遍历顺序是从大面值到小面值检查，就能自然得到「优先使用大面值」的答案。
- **复杂度分析（大白话）**：  
  - 假设每种纸币的最大张数是 `M`（这里 `M` 可能很大，最坏情况下是 `10^9`），暴力枚举需要在每一种纸币上尝试 `0~M` 次。最坏情况下的时间复杂度是 `O(M^5)`，这在实际里相当于「把宇宙中所有的纸币都试一遍」——根本不可行。  
  - 空间上我们只需要保存 `banknotesCount`、`denoms` 两个固定长度为 5 的数组，空间复杂度是 `O(1)`（常数级），相当于「只占几张纸的空间」。

#### 代码（Python）

```python
class ATM:
    def __init__(self):
        # 纸币面值，从小到大排列，方便索引
        self.denoms = [20, 50, 100, 200, 500]
        # 当前 ATM 中每种面值的张数，初始全为 0
        self.stock = [0] * 5

    # -------------------------------------------------
    # 暴力实现（仅作思路演示，实际会超时）
    # -------------------------------------------------
    def deposit(self, banknotesCount):
        """把 deposit 里每种纸币的数量加到 ATM 中"""
        for i in range(5):
            self.stock[i] += banknotesCount[i]

    def withdraw(self, amount):
        """
        暴力枚举所有可能的取法，返回满足条件的纸币张数数组。
        若找不到合法方案，返回 [-1]。
        """
        # 为了满足「大面值优先」的要求，我们从大到小尝试
        # 用一个递归/回溯的方式枚举
        ans = [-1]                     # 默认返回 [-1]
        used = [0] * 5                 # 记录当前递归路径使用了多少张纸币

        def dfs(idx, remaining):
            """尝试在 denoms[0..idx] 范围内凑出 remaining 金额"""
            nonlocal ans
            if remaining == 0:         # 成功凑出目标金额
                ans = used.copy()
                return True
            if idx < 0:                # 已经没有更小的面值可用了
                return False

            # 这一步是「大面值优先」的关键：先尽量多用当前面值
            max_take = min(self.stock[idx], remaining // self.denoms[idx])
            for k in range(max_take, -1, -1):   # 从最大可取张数往下尝试
                used[idx] = k
                if dfs(idx - 1, remaining - k * self.denoms[idx]):
                    return True
            used[idx] = 0               # 回溯，恢复现场
            return False

        dfs(4, amount)                  # 从最大面值（500）开始搜索
        if ans == [-1]:                 # 没有找到合法方案
            return [-1]

        # 把成功取出的纸币从库存中扣除
        for i in range(5):
            self.stock[i] -= ans[i]
        return ans
```

> **注意**：上述实现只用于说明「暴力思路」，在 LeetCode 上会因为时间超限而被判 `Time Limit Exceeded`。

#### 复杂度

- **时间复杂度**：`O(M^5)`（理论上）——相当于「每种纸币都尝试 0 到最大张数」的全部组合，实际会在第一批测试就超时。  
- **空间复杂度**：`O(1)`——只用了固定大小的数组和递归栈（深度最多 5），与输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有可能的取法**。其实我们根本不需要「枚举」，只要**按面值从大到小贪心取**，就一定能得到符合题目要求的答案。原因如下：

1. **面值是递增的整数**（20、50、100、200、500），且 **每种面值都是前面几种的整数倍**（虽然 20 与 50 不是倍数关系，但它们的最小公倍数是 10，足以让贪心成立）。  
2. 题目明确规定「取钱时优先使用面值大的纸币」，这正好是**贪心策略**的定义：在每一步都做出局部最优（尽可能多取大面值），最终得到全局最优。  
3. 由于每种纸币的张数上限非常大（`10^9`），**只需要一次线性扫描**（5 次）就能决定每种纸币要取多少张，根本不需要回溯。

**核心算法**：**贪心 + 前缀（剩余）计算**  

- 从面值最大的 `500` 开始，计算「当前还能取多少张」：`take = min(stock[i], amount // denoms[i])`。  
- 把 `take` 张从 ATM 中扣除，`amount` 减去 `take * denoms[i]`，继续处理下一个面值。  
- 当遍历完所有面值后，如果 `amount` 已经降到 `0`，说明成功取款；否则说明 **无法满足请求**，返回 `[-1]`，并且**不要修改 ATM 的库存**（因为取不到钱，机器不应该把钱给跑了）。

**为什么贪心一定对**（简化解释）：

- 假设我们在面值 `500` 上没有尽可能多取（比如少取了一张），那么剩下的金额只能用更小的面值来补足。因为更小的面值的总价值 **永远不可能超过** 少取的那张 `500`，所以我们最终要么取更多张小面值，要么根本取不出。因此「尽可能多取大面值」是唯一的最优选择。对每一种面值都如此递归，整体就是最优的。

#### 代码（Python）

```python
class ATM:
    def __init__(self):
        # 纸币面值，固定顺序（从小到大），后面会倒着遍历
        self.denoms = [20, 50, 100, 200, 500]
        # ATM 当前每种面值的库存，初始全为 0
        self.stock = [0] * 5

    def deposit(self, banknotesCount):
        """
        把用户存入的纸币数量加入到 ATM 的库存中。
        参数 banknotesCount 长度为 5，分别对应 20、50、100、200、500 美元。
        """
        for i in range(5):
            self.stock[i] += banknotesCount[i]

    def withdraw(self, amount):
        """
        尝试取出指定金额 amount。
        返回一个长度为 5 的数组，表示每种面值实际取出的张数；
        若无法完成取款，返回 [-1]。
        """
        # 为了不破坏原有库存，先拷贝一份用于“试取”
        temp_stock = self.stock.copy()
        # 记录本次取款实际使用的纸币张数，初始全为 0
        used = [0] * 5

        # 从面值最大的纸币（下标 4）开始贪心取
        for i in range(4, -1, -1):
            if amount <= 0:        # 已经凑齐所需金额，提前结束循环
                break
            # 这张面值的最大可取张数 = min(库存, 还能凑的张数)
            max_can_take = min(temp_stock[i], amount // self.denoms[i])
            if max_can_take > 0:
                used[i] = max_can_take
                amount -= max_can_take * self.denoms[i]
                temp_stock[i] -= max_can_take

        # 循环结束后检查是否成功凑出金额
        if amount != 0:               # 仍有剩余，说明取不到这么多钱
            return [-1]

        # 成功取款：把临时库存写回正式库存
        self.stock = temp_stock
        return used
```

> **代码要点解释**  
> - `temp_stock` 是「试探性」的库存副本，只有在最终确定可以成功取款时才会写回 `self.stock`，防止「取不到钱却把库存扣掉」的错误。  
> - `max_can_take = min(temp_stock[i], amount // self.denoms[i])`：先算出金额还能容纳多少张该面值（`amount // denoms[i]`），再受限于实际库存（`temp_stock[i]`），两者取小的就是本轮能取的最大张数。  
> - 循环顺序 `for i in range(4, -1, -1)` 正好实现「大面值优先」的需求。

#### 复杂度

- **时间复杂度**：`O(5) = O(1)` —— 只遍历 5 种面值一次，和输入规模无关。相当于「一次快速检查就能决定是否可以取款」。
- **空间复杂度**：`O(1)` —— 只用了几个长度为 5 的固定数组（`stock、temp_stock、used`），占用常数级空间。

---

## 心得

- **核心技巧**：**贪心**（始终优先使用面值最大的纸币）+ **模拟库存**。  
- **适用的题型**：  
  1. “找零”类问题（如 LeetCode 1665. Minimum Initial Energy to Finish Tasks）  
  2. “分配资源”类问题（如 LeetCode 322. Coin Change 采用贪心时需满足特定面值条件）  
  3. 其它需要**优先使用“大件”**的设计题（如电梯调度、货仓装箱）。
- **一句话总结解题钥匙**：**“大面值先抢，剩余再用小面值”**——只要面值之间满足整数倍或“足够大” 的关系，贪心必然给出最优解。

---

## 反思

- **第一反应**：看到“优先使用大面值”，立刻想到**贪心**；随后想到要模拟 ATM 的库存，于是写出暴力回溯的思路来验证。  
- **最容易踩的坑**：  
  - **取不到钱时不应修改库存**：如果直接在原数组上扣除，后面会出现“钱凭空消失”的错误。  
  - **整数溢出**：`amount` 与面值乘积可能达到 `10^9 * 500`，在 Python 中不会溢出，但在其他语言要注意使用 64 位整数。  
  - **边界情况**：`amount` 正好等于某种面值的多倍，或全部由一种纸币完成，都必须能够正确返回。  
- **下次类似题的第一步**：先确认「是否有明确的优先级」或「是否满足贪心条件」；若满足，直接用**一次线性扫描**决定每种资源的使用量；若不满足，再考虑动态规划或回溯。