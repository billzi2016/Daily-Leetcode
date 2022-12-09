# #2043. **简易银行系统** / Simple Bank System

> 难度：中等 · 标签：Array、Hash Table、Design、Simulation · [LeetCode 链接](https://leetcode.com/problems/simple-bank-system/)

---

## 题目（英文原版）

**Description**

You have been tasked with writing a program for a popular bank that will automate all its incoming transactions (transfer, deposit, and withdraw). The bank has n accounts numbered from 1 to n. The initial balance of each account is stored in a 0-indexed integer array balance, with the (i + 1)th account having an initial balance of balance[i].
Execute all the valid transactions. A transaction is valid if:
Implement the Bank class:

**Examples**

**Example 1:**

```
Input
["Bank", "withdraw", "transfer", "deposit", "transfer", "withdraw"]
[[[10, 100, 20, 50, 30]], [3, 10], [5, 1, 20], [5, 20], [3, 4, 15], [10, 50]]
Output
[null, true, true, true, false, false]

Explanation
Bank bank = new Bank([10, 100, 20, 50, 30]);
bank.withdraw(3, 10);    // return true, account 3 has a balance of $20, so it is valid to withdraw $10.
                         // Account 3 has $20 - $10 = $10.
bank.transfer(5, 1, 20); // return true, account 5 has a balance of $30, so it is valid to transfer $20.
                         // Account 5 has $30 - $20 = $10, and account 1 has $10 + $20 = $30.
bank.deposit(5, 20);     // return true, it is valid to deposit $20 to account 5.
                         // Account 5 has $10 + $20 = $30.
bank.transfer(3, 4, 15); // return false, the current balance of account 3 is $10,
                         // so it is invalid to transfer $15 from it.
bank.withdraw(10, 50);   // return false, it is invalid because account 10 does not exist.
```

**Constraints**

- n == balance.length
- 1 <= n, account, account1, account2 <= 105
- 0 <= balance[i], money <= 1012
- At most 104 calls will be made to each function transfer, deposit, withdraw.

---

## 题目（中文翻译）

你需要为一家流行的银行编写程序，以自动化其所有的入账操作（转账（transfer）、存款（deposit）和取款（withdraw））。该银行拥有 **n** 个账户，编号从 **1** 到 **n**。每个账户的初始余额（balance）存放在一个 **0** 索引的整数数组 `balance` 中，其中第 **i+1** 个账户的初始余额为 `balance[i]`。

请实现一个 `Bank` 类，执行所有**合法**的交易（transaction）。只有满足以下条件的交易才视为合法：

* **取款**：账户 `account` 的余额必须不少于取款金额 `money`。
* **存款**：始终合法（不受余额限制）。
* **转账**：账户 `account1` 必须有足够的余额（`balance[account1‑1] ≥ money`），且 `account1` 与 `account2` 必须是不同的账户。

`Bank` 类应包含以下接口：

```java
Bank(int[] balance)               // 构造函数，初始化各账户余额
boolean withdraw(int account, long money)   // 若合法则扣除金额并返回 true，否则返回 false
boolean deposit(int account, long money)    // 永远合法，增加金额并返回 true
boolean transfer(int account1, int account2, long money) // 若合法则完成转账并返回 true，否则返回 false
```

**示例 1：**

```text
Input
["Bank", "withdraw", "transfer", "deposit", "transfer", "withdraw"]
[[[10, 100, 20, 50, 30]], [3, 10], [5, 1, 20], [5, 20], [3, 4, 15], [10, 50]]

Output
[null, true, true, true, false, false]

Explanation
Bank bank = new Bank([10, 100, 20, 50, 30]);
bank.withdraw(3, 10);    // 返回 true，账户 3 的余额为 $20，取出 $10 合法。
bank.transfer(5, 1, 20); // 返回 true，账户 5 的余额为 $30，转出 $20 合法，账户 1 收到 $20。
bank.deposit(5, 20);     // 返回 true，账户 5 再存入 $20。
bank.transfer(3, 4, 15); // 返回 false，账户 3 的余额仅剩 $10，无法转出 $15。
bank.withdraw(10, 50);   // 返回 false，账户 10 超出范围（不存在）。
```

**约束条件**

- `n == balance.length`
- `1 <= n, account, account1, account2 <= 10^5`
- `0 <= balance[i], money <= 10^12`
- 每个函数 `transfer`、`deposit`、`withdraw` 最多会被调用 `10^4` 次。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是“把每个账户的余额记下来，收到一笔操作就立刻检查、改动”。  

- **数据结构**：用一个 Python 列表 `balances` 保存所有账户的余额。列表的下标 `i` 对应第 `i+1` 号账户（因为题目说账户是 **1‑indexed**，而 Python 列表是 **0‑indexed**）。  
  - 这就像我们平时查字典一样：**键** 是账户编号，**值** 是余额。  
- **为什么正确**：  
  1. **取钱** `withdraw(account, money)`：只要该账户余额 `>= money`，就可以扣除；否则交易无效。  
  2. **存钱** `deposit(account, money)`：没有任何限制，直接把 `money` 加到对应账户。  
  3. **转账** `transfer(account1, account2, money)`：先检查 `account1` 是否有足够余额（`>= money`），若是则从 `account1` 扣除并把 `money` 加到 `account2`。  
- **时间复杂度**：每一次操作只需要一次下标访问和几条算术比较，都是 **O(1)**（常数时间）。  
- **空间复杂度**：我们只额外保存一个长度为 `n` 的列表，**O(n)**（线性空间）。  

> **大白话解释**：  
> - `O(1)` 就像我们在超市直接把商品放进购物车，所花的时间和商品数量无关。  
> - `O(n)` 就像把所有商品排成一条长队，每多一个商品就多占一点空间。

#### 代码（Python）

```python
class Bank:
    """
    简单银行系统：直接用列表保存每个账户的余额。
    账户编号是 1 开始的，所以在列表中要减 1 才是对应的下标。
    """

    def __init__(self, balance):
        """
        :param balance: List[int]，第 i 位是第 i+1 号账户的初始余额
        """
        # 直接拷贝一份，防止外部修改原数组
        self.balances = balance[:]          # O(n) 的初始化

    def withdraw(self, account: int, money: int) -> bool:
        """
        从 account 号账户取出 money 元。
        只有余额足够时才成功，返回 True；否则返回 False。
        """
        idx = account - 1                    # 把 1-index 转成 0-index
        if self.balances[idx] >= money:     # 余额检查
            self.balances[idx] -= money     # 扣钱
            return True
        return False                         # 余额不足

    def deposit(self, account: int, money: int) -> bool:
        """
        向 account 号账户存入 money 元。永远成功，返回 True。
        """
        idx = account - 1
        self.balances[idx] += money
        return True

    def transfer(self, account1: int, account2: int, money: int) -> bool:
        """
        将 money 元从 account1 转到 account2。
        只有 account1 余额足够时才成功，返回 True；否则返回 False。
        """
        idx1 = account1 - 1
        idx2 = account2 - 1
        if self.balances[idx1] >= money:    # 检查转出账户是否够钱
            self.balances[idx1] -= money    # 扣钱
            self.balances[idx2] += money    # 收钱
            return True
        return False                         # 余额不足，转账失败
```

#### 复杂度  

- **时间复杂度**：`O(1)` 每次调用 `withdraw / deposit / transfer`。  
  - 意味着不管有多少账户或多少笔交易，单次操作的耗时基本不变。  
- **空间复杂度**：`O(n)`，其中 `n = len(balance)`。  
  - 只需要存储每个账户的余额，一旦创建后不再额外增长。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**每次交易只涉及常数个账户**，因此最关键的点已经是 **O(1)**。  
如果把「账户」的编号范围（最高 10⁵）和「实际使用的账户」数量相比，可能出现「很多账户从未被操作」的情况。此时我们可以用 **哈希表（字典）** 来只存储被使用过的账户，进一步节省空间。

**优化方向**  

1. **慢点在哪里？**  
   - 暴力解在初始化时把所有 `n` 个余额全部放进列表，空间是 `O(n)`。当 `n` 很大但实际只操作少量账户时，这会浪费很多内存。  
2. **怎么改进？**  
   - 用 `dict` 把「账户编号 → 余额」的映射保存下来。只在第一次出现某个账户时插入键值对。未出现的账户默认余额为 `0`（因为题目保证初始数组已经给出所有账户的余额，这里改为「只在需要时才加载」）。  
3. **核心数据结构**：**哈希表**（Python 的 `dict`）。  
   - 类比：就像查字典时，只需要翻到对应的词条页码，而不必把整本字典全部记在脑子里。  

**实现细节**  

- 在构造函数中把 `balance` 列表一次性转成字典 `self.bal = {i+1: v for i, v in enumerate(balance)}`，这一步仍是 `O(n)`，但只做一次。  
- 后续每次操作都在字典里 `O(1)` 取值、更新。  
- 若题目允许 **稀疏**（即有的账户在后续永不出现），我们也可以在 `__init__` 时不立即构建完整字典，而是 **延迟加载**：在第一次访问某个账户时，如果不在字典里，就把 `balance[idx]` 加进去。这里为了代码简洁仍采用一次性构建的方式，时间上已经是最优的。  

**为什么算最优**  

- 每笔交易的时间仍是 **O(1)**，已经达到了理论下界（因为我们必须至少检查一次余额）。  
- 空间从 `O(n)` 降到 **O(k)**，`k` 为实际使用过的账户数（最坏仍是 `O(n)`，但在稀疏场景下可显著省内存）。  

#### 代码（Python）

```python
class Bank:
    """
    使用哈希表（dict）保存账户余额，空间更“按需”。
    对于本题的规模（最多 1e5 条账户），dict 的查询/写入仍是 O(1)。
    """

    def __init__(self, balance):
        """
        :param balance: List[int]，第 i 位是第 i+1 号账户的初始余额
        """
        # 将下标转成 1-index 的键，构造字典
        self.bal = {i + 1: v for i, v in enumerate(balance)}   # O(n)

    def withdraw(self, account: int, money: int) -> bool:
        """取钱：余额足够才成功"""
        if self.bal[account] >= money:        # O(1) 查表
            self.bal[account] -= money
            return True
        return False

    def deposit(self, account: int, money: int) -> bool:
        """存钱：直接加"""
        self.bal[account] += money
        return True

    def transfer(self, account1: int, account2: int, money: int) -> bool:
        """转账：先检查转出账户是否有足够余额"""
        if self.bal[account1] >= money:
            self.bal[account1] -= money
            self.bal[account2] += money
            return True
        return False
```

#### 复杂度  

- **时间复杂度**：每次 `withdraw / deposit / transfer` 仍是 **O(1)**。  
  - 与暴力解相比没有提升，因为已经是最快的了。  
- **空间复杂度**：**O(k)**，`k` 为实际出现过的账户数。  
  - 在最坏情况下（所有账户都有交易）仍是 `O(n)`，但在很多账户从未被访问的实际业务中可以省下大量内存。

---  

## 心得  

- **核心技巧**：利用**哈希表**（或数组）实现**常数时间的随机访问**，并在每次操作前做**合法性检查**（余额是否足够）。  
- **适用题型**：  
  1. “账户/库存管理”类的模拟题（如 LeetCode 2129 `Capitalizing`、2145 `Count the Number of Homogenous Substrings` 中的计数技巧）。  
  2. 需要**快速更新、查询**的场景（如 “实现一个简易的购物车”、 “银行排队系统”等）。  
- **一句话总结**：**“把每个对象的状态存进可以 O(1) 取值的容器，操作前先检查合法性”。**  

---  

## 反思  

- **第一反应**：看到“转账、存款、取款”就想到“直接改余额”。于是立刻想到用数组或字典保存每个账户的余额。  
- **最容易踩的坑**：  
  - **下标偏移**：账户是 1‑indexed，列表是 0‑indexed，容易忘记 `-1`。  
  - **溢出**：`money` 最大可达 `10^12`，在某些语言里需要使用 64 位整数；在 Python 中整数是任意精度，天然安全。  
  - **非法账户**：虽然约束保证 `account` 在合法范围，但实现时仍要确保不越界（如使用字典可直接抛异常，列表需自行检查）。  
- **下次遇到同类题**：第一步先**确定状态容器**（数组/哈希表），然后**写出每种操作的合法性判定**，最后实现“检查 → 更新”。这样思路清晰、代码容易调通。