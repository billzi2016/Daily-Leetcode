# #3577. 统计计算机解锁排列的数量 / Count the Number of Computer Unlocking Permutations

> 难度：中等 · 标签：Array、Math、Brainteaser、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-computer-unlocking-permutations/)

---

## 题目（英文原版）

**Description**

You are given an array complexity of length n.
There are n locked computers in a room with labels from 0 to n - 1, each with its own unique password. The password of the computer i has a complexity complexity[i].
The password for the computer labeled 0 is already decrypted and serves as the root. All other computers must be unlocked using it or another previously unlocked computer, following this information:
Find the number of permutations of [0, 1, 2, ..., (n - 1)] that represent a valid order in which the computers can be unlocked, starting from computer 0 as the only initially unlocked one.
Since the answer may be large, return it modulo 109 + 7.
Note that the password for the computer with label 0 is decrypted, and not the computer with the first position in the permutation.

**Examples**

**Example 1:**

```
Input: complexity = [1,2,3]
Output: 2
Explanation:
The valid permutations are:
```

**Example 2:**

```
Input: complexity = [3,3,3,4,4,4]
Output: 0
Explanation:
There are no possible permutations which can unlock all computers.
```

**Constraints**

- 2 <= complexity.length <= 105
- 1 <= complexity[i] <= 109

---

## 题目（中文翻译）

你得到一个长度为 `n` 的数组 `complexity`。  
房间里有 `n` 台已锁定的电脑，编号为 `0` 到 `n - 1`，每台电脑都有唯一的密码。第 `i` 台电脑的密码复杂度为 `complexity[i]`（complexity）。  

编号为 `0` 的电脑的密码已经被解密，并作为根（root）。所有其他电脑必须使用已解密的电脑（包括根）或之前已解锁的电脑来解锁，遵循如下规则：

找出所有 **排列**（permutation）`[0, 1, 2, ..., n - 1]` 的数量，这些排列表示一种有效的解锁顺序，使得从唯一初始解锁的电脑 `0` 开始，能够依次解锁所有电脑。  

由于答案可能很大，请返回答案对 `10^9 + 7` 取模后的结果。  

> 注意：编号为 `0` 的电脑的密码已经解密，而不是排列中出现的第一个位置对应的电脑。

**示例 1**  
输入: `complexity = [1,2,3]`  
输出: `2`  
解释:  
有效的排列有：

**示例 2**  
输入: `complexity = [3,3,3,4,4,4]`  
输出: `0`  
解释:  
不存在能够解锁所有电脑的排列。

**约束条件**

- `2 <= complexity.length <= 10^5`
- `1 <= complexity[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把题目直接翻译成“把所有可能的解锁顺序都枚举一遍，看看哪些合法”。  
具体做法：

1. **枚举排列**：先把 `[0,1,2,…,n-1]` 的所有全排列列出来（Python 的 `itertools.permutations` 可以帮忙）。  
2. **检查合法性**：  
   - 第一个元素必须是 `0`，因为只有电脑 `0` 的密码已经被解密。  
   - 其余的电脑只能在已经解锁的电脑中挑一个来解锁。题目暗示，只要**根电脑的复杂度是全局唯一最小**，后面的电脑顺序随意都能被解锁。于是我们只需要判断：在当前排列里，`complexity[0]` 是否是唯一的最小值。  
   - 如果是唯一最小，则该排列合法；否则非法。

> **类比**：把 `complexity` 看成一本字典里每个词的页码，`complexity[0]` 就是最小的页码且只能出现一次。只有这样，其他词（电脑）才能在已经打开的页码后面随意翻阅。

#### 代码（Python）

```python
import itertools

MOD = 10**9 + 7

def count_bruteforce(complexity):
    n = len(complexity)
    # 1. 先检查根电脑是否唯一最小，若不是直接返回 0，省去枚举
    min_val = min(complexity)
    if complexity[0] != min_val or complexity.count(min_val) != 1:
        return 0

    cnt = 0
    # 2. 枚举所有排列（只考虑以 0 开头的）
    for perm in itertools.permutations(range(1, n)):
        # 在这里不需要进一步检查，因为根已唯一最小，任意顺序都合法
        cnt += 1
        cnt %= MOD
    return cnt
```

> **关键行中文注释**  
> - `itertools.permutations(range(1, n))`：生成除 `0` 之外的所有排列，相当于把 `0` 固定在最前面。  
> - `complexity.count(min_val) != 1`：检查最小复杂度是否唯一出现。

#### 复杂度  

- **时间复杂度**：`O(n! * n)`（枚举所有全排列，每个排列的生成本身是 `O(n)`）。这在 `n` 大于 8 时就会爆炸，只有极小规模的输入能跑得动。  
- **空间复杂度**：`O(n)`（存放当前排列的临时空间），同样不适用于大规模。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，真正的“难点”只在 **根电脑的复杂度是否唯一最小**。  
一旦满足这个条件，**后面的电脑可以随意排列**，因为每一步都有已经解锁的电脑（根电脑）可以用来解锁下一个。于是我们把问题简化为：

1. 判断 `complexity[0]` 是否是全数组的唯一最小值。  
   - 若不是，答案直接是 `0`（没有合法的解锁顺序）。  
2. 若是唯一最小，则合法排列的数量等于把剩下 `n‑1` 台电脑随意排的方式数，即 `(n‑1)!`。  
3. 由于答案要模 `10^9+7`，我们只需要在计算阶乘时不断取模。

> **为什么这一步就可以了？**  
> 想象每台电脑都有一把钥匙，钥匙的“威力”由复杂度决定。根电脑的钥匙最弱（最小），且没有其他电脑和它一样弱。于是根电脑的钥匙可以打开 **所有** 其他电脑的锁——不管它们的复杂度多大。解锁顺序只要保证根电脑先解锁，后面的顺序随意即可。

#### 代码（Python）

```python
MOD = 10**9 + 7

def count_permutations(complexity):
    n = len(complexity)

    # 1. 检查根电脑是否唯一最小
    min_val = min(complexity)
    if complexity[0] != min_val or complexity.count(min_val) != 1:
        return 0

    # 2. 计算 (n-1)! % MOD
    fact = 1
    for i in range(2, n):          # 只乘 2 … n-1
        fact = (fact * i) % MOD
    return fact
```

> **关键行中文注释**  
> - `for i in range(2, n):`：从 `2` 开始乘到 `n‑1`，因为我们要的是 `(n‑1)!`（`0! = 1`、`1! = 1`）。  
> - `fact = (fact * i) % MOD`：每一步都取模，防止整数溢出并保持答案在范围内。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组找最小值（`O(n)`），再一次线性循环计算阶乘（`O(n)`）。  
  - 与暴力的 `O(n!)` 相比，提升了指数级的速度。  
- **空间复杂度**：`O(1)`  
  - 只使用了常数个额外变量。

---

## 心得

- **核心技巧**：**先判断全局唯一最小值**，随后利用**排列计数**（阶乘）得到答案。  
- **适用的题型**：  
  1. “唯一根节点决定全局顺序”类问题（例如 “树的根节点唯一最小”）。  
  2. “只要满足某个全局条件，其余任意排列都合法” 的计数题（如 “所有数都不同且最小值固定在首位”）。  
- **一句话总结**：只要根电脑的复杂度唯一最小，合法顺序数 = `(n‑1)!`，否则为 `0`。

---

## 反思

- **第一反应**：看到“排列”二字就想直接枚举全部排列，结果很快发现这在大数据范围下根本不可行。  
- **最容易踩的坑**：  
  - 忽略 **唯一** 最小的要求，只检查 `complexity[0]` 是否是最小值，导致在有相同最小值的情况下仍返回非零答案。  
  - 阶乘计算时忘记取模，导致 Python 整数虽然不会溢出，但运行时间会明显增长。  
- **下次思路**：遇到“所有元素都可以随意排列，只要满足一个全局限制”时，第一步就检查这个全局限制是否成立，然后把计数问题转化为阶乘或组合公式，而不是直接枚举。