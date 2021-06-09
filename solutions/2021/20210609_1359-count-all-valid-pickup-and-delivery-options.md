# #1359. 统计所有有效的取件和送达方案 / Count All Valid Pickup and Delivery Options

> 难度：困难 · 标签：Math、Dynamic Programming、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/count-all-valid-pickup-and-delivery-options/)

---

## 题目（英文原版）

**Description**

Given n orders, each order consists of a pickup and a delivery service.
Count all valid pickup/delivery possible sequences such that delivery(i) is always after of pickup(i).
Since the answer may be too large, return it modulo 10^9 + 7.

**Examples**

**Example 1:**

```
Input: n = 1
Output: 1
Explanation: Unique order (P1, D1), Delivery 1 always is after of Pickup 1.
```

**Example 2:**

```
Input: n = 2
Output: 6
Explanation: All possible orders: 
(P1,P2,D1,D2), (P1,P2,D2,D1), (P1,D1,P2,D2), (P2,P1,D1,D2), (P2,P1,D2,D1) and (P2,D2,P1,D1).
This is an invalid order (P1,D2,P2,D1) because Pickup 2 is after of Delivery 2.
```

**Example 3:**

```
Input: n = 3
Output: 90
```

**Constraints**

- 1 <= n <= 500

---

## 题目（中文翻译）

**描述**  
给定 `n` 个订单，每个订单包含一次取件（pickup）和一次送达（delivery）。  
统计所有满足以下条件的取件/送达序列的数量：对于每个 `i`，送达 `i` 必须出现在取件 `i` 之后。  
由于答案可能非常大，请返回 **10^9 + 7** 取模后的结果。

**示例**

**示例 1**  
```
Input: n = 1
Output: 1
```
**解释**：唯一的序列为 `(P1, D1)`，送达 1 必然在取件 1 之后。

**示例 2**  
```
Input: n = 2
Output: 6
```
**解释**：所有可能的序列为  
`(P1,P2,D1,D2)`, `(P1,P2,D2,D1)`, `(P1,D1,P2,D2)`, `(P2,P1,D1,D2)`, `(P2,P1,D2,D1)` 和 `(P2,D2,P1,D1)`。  
序列 `(P1,D2,P2,D1)` 为无效，因为取件 2 出现在送达 2 之后。

**示例 3**  
```
Input: n = 3
Output: 90
```

**约束条件**  
- `1 <= n <= 500`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 可能的 2n 条指令列出来，然后把不符合 “每个订单的送达一定在取货之后” 这一规则的序列剔除掉。

- **数据结构**：我们可以把每一次指令当作一个字符，比如 `"P1"` 表示取货 1，`"D1"` 表示送货 1。把所有指令放进一个列表里，用 `itertools.permutations` 生成所有排列。  
  - **类比**：把这看成把一副牌（每张牌是 `P1、D1、P2、D2…`）洗牌后一次抽完，所有抽牌顺序就是所有排列。

- **为什么正确**：因为我们枚举了**全部**可能的指令顺序，只要把不合法的过滤掉，剩下的就是答案。

- **复杂度分析**  
  - **时间**：要遍历所有排列的数量是 `(2n)!`（2n 的阶乘），每个排列检查合法性需要 O(2n) 的时间，所以总体是 **O((2n)!)**。这里的 “O((2n)!)” 可以理解为“随着 n 增大，运行时间会像 2n 的阶乘一样飞快增长”，即使 n=10，(20)! 已经是 2.4×10¹⁸，根本不可算。  
  - **空间**：生成排列时 Python 会一次保存一条排列（长度 2n），所以 **O(2n)** 的额外空间。

> **结论**：暴力法只能用来验证小 n（比如 n≤4）或在调试时使用，根本无法通过 LeetCode 的限制（n 可达 500）。

#### 代码（Python）

```python
import itertools

def countOrders_bruteforce(n: int) -> int:
    # 把所有指令写进列表
    ops = []
    for i in range(1, n + 1):
        ops.append(f'P{i}')   # Pickup i
        ops.append(f'D{i}')   # Delivery i

    ans = 0
    # 生成所有排列（只适合 n 很小的情况）
    for perm in itertools.permutations(ops):
        ok = True
        # 用字典记录每个订单的取货是否已经出现
        seen_pickup = set()
        for step in perm:
            if step[0] == 'P':                 # 取货
                seen_pickup.add(step[1:])       # 记录订单号
            else:                               # 送货
                order = step[1:]
                if order not in seen_pickup:    # 送货前没有取货 → 不合法
                    ok = False
                    break
        if ok:
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O((2n)!)` —— 随着 n 增大，计算量呈阶乘级爆炸，实际只能跑到 n=3/4 左右。  
- **空间复杂度**：`O(2n)` —— 只保存当前排列的 2n 个字符。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈**在于我们一次性把所有指令全部排好序，然后再检查合法性。实际上，合法序列具有很强的递推结构：  
> 当已经安排好 `i‑1` 对订单的所有指令时，插入第 `i` 对（`Pi`、`Di`）的方式是可以直接计数的。

**一步步推导**：

1. **已有 `i‑1` 对的合法序列** 长度是 `2(i‑1)`。  
2. **插入第 `i` 对**：  
   - 先放 `Pi`（取货），它可以插在已有序列的 **任意** `2(i‑1)+1` 个缝隙里（包括最前面和最末尾）。  
   - 放完 `Pi` 后，`Di`（送货）必须在 `Pi` 之后。此时序列长度已经是 `2(i‑1)+1`，`Di` 可以插在 `Pi` 右侧的 **任意** `2(i‑1)+2 - pos` 个位置里。把所有可能的 `pos` 加起来，得到的总方式数恰好是 `(2i‑1) * i`。  

   直观解释：  
   - `2i‑1` 表示把 **取货** 插入的所有位置数。  
   - `i` 表示在插入 **送货** 时，有多少种合法的“后面空位”。  
   - 两者相乘得到 **插入一对** 的所有可能。

3. **递推公式**  
   - 记 `dp[i]` 为前 `i` 对订单的合法序列数，则  
     \[
     dp[i] = dp[i-1] \times (2i-1) \times i
     \]
   - 初始条件 `dp[0] = 1`（空序列只有一种）。

4. **取模**  
   由于答案会非常大，需要对 `10^9+7` 取模。递推时每一步都取模即可防止溢出。

5. **等价的闭式**  
   通过展开递推可以得到  
   \[
   dp[n] = \frac{(2n)!}{2^n}
   \]
   但直接计算阶乘再除以 `2^n` 需要求模逆元，稍显繁琐。递推的方式只需要 O(n) 的乘法，代码更简洁。

**核心算法**：**动态规划 + 组合计数**（不需要额外的数组，只用一个变量滚动保存 `dp`），时间 O(n)，空间 O(1)。

#### 代码（Python）

```python
MOD = 10 ** 9 + 7

def countOrders(n: int) -> int:
    """
    统计所有合法的取货/送货序列数。
    dp[i] = dp[i-1] * (2*i - 1) * i   (mod MOD)
    """
    ans = 1            # dp[0] = 1
    for i in range(1, n + 1):
        ans = ans * (2 * i - 1) % MOD   # 插入 Pi 的位置数
        ans = ans * i % MOD             # 插入 Di 的合法位置数
    return ans
```

> **代码解释**（每行中文注释）  
> 1. `ans = 1` —— 空序列只有一种。  
> 2. 循环 `i` 从 1 到 `n`，对应加入第 `i` 对订单。  
> 3. `ans = ans * (2 * i - 1) % MOD` —— 把取货 `Pi` 插入已有序列的所有可能位置。  
> 4. `ans = ans * i % MOD` —— 把送货 `Di` 插入取货之后的合法位置。  
> 5. 循环结束后，`ans` 就是答案，直接返回。

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次 `1 … n`，每一步做常数次乘法。相较于暴力的 `(2n)!`，这几乎是瞬间完成。  
- **空间复杂度**：`O(1)` —— 只用几个整数保存中间结果，没有额外的数组或递归栈。

---

## 心得

- **核心技巧**：利用**递推计数**（插入法）把大问题拆成“小问题”，把组合数的乘法形式化为动态规划。  
- **适用题型**  
  1. **Pick-up and Delivery** 系列（LeetCode 1359）  
  2. **排列组合递推** 如 “不同路径” 中的格子插入法  
  3. **计数 Catalan 类问题的变形**（如合法括号序列的插入计数）  

- **一句话总结解题钥匙**：**把新的一对订单看成“插进已有序列的两块拼图”，直接算出插入方式数并累乘**。

---

## 反思

- **第一反应**：看到“取货必须在送货之前”，立刻想到“每对是有顺序的括号”，于是尝试枚举所有排列并检查。  
- **最容易踩的坑**  
  - **边界**：`n=1` 时公式必须返回 1，递推的初始值 `dp[0]=1` 必不可少。  
  - **取模**：乘法中间值会超出 Python 整数范围（虽然 Python 大整数不会溢出），但在语言如 C++ 中必须及时 `% MOD` 防止溢出。  
  - **误把除法写成整数除**：闭式 `(2n)! / 2^n` 需要模逆元，直接除会出错。使用递推可以规避这一步。  

- **下次遇到同类题**：第一步先思考“把第 k 件事加入已有合法序列，有几种插入方式？” 然后写出递推式，再考虑取模或其他约束。这样往往能把指数级的暴力直接压缩到线性时间。