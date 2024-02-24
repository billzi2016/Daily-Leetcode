# #2591. 将钱分配给尽可能多的孩子 / Distribute Money to Maximum Children

> 难度：简单 · 标签：Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/distribute-money-to-maximum-children/)

---

## 题目（英文原版）

**Description**

You are given an integer money denoting the amount of money (in dollars) that you have and another integer children denoting the number of children that you must distribute the money to.
You have to distribute the money according to the following rules:
Return the maximum number of children who may receive exactly 8 dollars if you distribute the money according to the aforementioned rules. If there is no way to distribute the money, return -1.

**Examples**

**Example 1:**

```
Input: money = 20, children = 3
Output: 1
Explanation: 
The maximum number of children with 8 dollars will be 1. One of the ways to distribute the money is:
- 8 dollars to the first child.
- 9 dollars to the second child. 
- 3 dollars to the third child.
It can be proven that no distribution exists such that number of children getting 8 dollars is greater than 1.
```

**Example 2:**

```
Input: money = 16, children = 2
Output: 2
Explanation: Each child can be given 8 dollars.
```

**Constraints**

- 1 <= money <= 200
- 2 <= children <= 30

---

## 题目（中文翻译）

**描述**  
给定一个整数 `money` 表示你拥有的金钱（单位：美元），以及另一个整数 `children` 表示你必须分配金钱的孩子数量。  
你需要按照以下规则分配这些金钱：  
返回在满足上述规则的前提下，能够恰好得到 **8 美元** 的孩子的最大数量。如果不存在任何合法的分配方案，返回 **-1**。  

**示例**  

**示例 1**  
输入: `money = 20, children = 3`  
输出: `1`  
解释:  
恰好得到 8 美元的孩子最多为 1。一种可行的分配方案是：  
- 第一个孩子 8 美元。  
- 第二个孩子 9 美元。  
- 第三个孩子 3 美元。  
可以证明不存在让获得 8 美元的孩子数量大于 1 的分配方式。  

**示例 2**  
输入: `money = 16, children = 2`  
输出: `2`  
解释: 每个孩子都可以得到 8 美元。  

**约束条件**  
- $1 \leq money \leq 200$  
- $2 \leq children \leq 30$

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

把“恰好得到 8 美元的孩子数”记作 `k`。  
- 首先让 `k` 个孩子每人拿 **8 美元**。  
- 剩下的 `children‑k` 个孩子必须分到 **剩余的钱**，并且满足题目两条规则  
  1. 每个孩子至少拿 **1 美元**（相当于每个人手里至少有一张 1 美元的钞票）。  
  2. **不能出现恰好 4 美元** 的情况（这就像字典里查不到“4”，如果出现就算错误）。  

于是我们只需要判断：对于某个 `k`，**是否能把剩余的钱合法地分配给剩下的孩子**。  
如果能，就说明 `k` 是可行的；我们从大到小枚举 `k`，第一个可行的 `k` 就是答案。  

> **生活化类比**：  
> 把每个孩子想象成一本笔记本，给 8 美元相当于往笔记本里贴 8 张贴纸。  
> 其余的贴纸要均匀分配到剩下的笔记本里，每本至少要有 1 张贴纸，而且**不能恰好是 4 张**（4 张贴纸的笔记本是“禁贴本”）。  

**为什么暴力方法一定能找到答案**  
因为我们把所有可能的 `k`（从 `children` 到 `0`）都检查了一遍，只要有合法的分配方式，就一定会在某一次检查中被发现。  

**时间/空间复杂度**  
- 我们最多检查 `children + 1 ≤ 31` 次（因为 `children ≤ 30`），每次的合法性检查只用常数时间。  
- **时间复杂度**：`O(children)`，在最坏情况下大约是 `O(30)`，几乎可以忽略不计。  
- **空间复杂度**：只用了几个整数变量，`O(1)`（常数级别的内存）。  

#### 代码（Python）  

```python
def maxChildrenWithEight_bruteforce(money: int, children: int) -> int:
    # 先检查最基本的“不够钱”情况
    if money < children:          # 每个孩子至少要 1 美元
        return -1

    # 从最多的 8 美元孩子数开始往下尝试
    for k in range(children, -1, -1):          # k = children, children-1, ..., 0
        money_after_k = money - 8 * k           # 给 k 个孩子 8 美元后剩余的钱
        left_children = children - k           # 还需要分配的孩子数

        # 剩余的钱必须够每个剩余的孩子拿到至少 1 美元
        if money_after_k < left_children:
            continue                           # 钱不够，直接跳过

        # 剩余的钱如果恰好是 4 美元且只剩 1 个孩子，那只能让这个孩子拿 4，违规
        if left_children == 1 and money_after_k == 4:
            continue                           # 违规，跳过

        # 其余情况下，总可以把钱分配好（因为没有上限，只要不出现 4 即可）
        return k

    # 循环结束仍未找到合法方案，说明根本不可分配
    return -1
```

> **关键行中文注释**  
> - `if money < children:` 检查“每人至少 1 美元”这条最基本的规则。  
> - `for k in range(children, -1, -1):` 从最多的 8 美元孩子数往下枚举。  
> - `if money_after_k < left_children:` 剩余的钱不足以让每个孩子拿到 1 美元，直接不可能。  
> - `if left_children == 1 and money_after_k == 4:` 唯一的特殊情况：只剩一个孩子且只能给 4 美元，违规则。  

#### 复杂度  

- **时间复杂度**：`O(children)` → 大约 `O(30)`，即遍历一次所有可能的 `k`。  
- **空间复杂度**：`O(1)` → 只用了几个整数变量，常数级内存。  

---  

### 2. 最优解  

#### 思路  

暴力解已经可以在毫秒级跑完，但我们仍可以把思考过程抽象成 **贪心**（greedy）来得到更直接的公式。  

1. **先保证每个孩子至少 1 美元**  
   - 把 `children` 美元先平均分配（每人 1 美元），剩下的 `extra = money - children` 美元可以自由分配。  

2. **把“8 美元孩子”转化为“额外加 7 美元”**  
   - 如果某个孩子要得到 8 美元，实际上在已经拿了 1 美元的基础上**再加 7 美元**。  
   - 因此，每让一个孩子成为 “8 美元”，就要消耗 `7` 个 `extra` 美元。  

3. **最大化 8 美元孩子数**  
   - 把 `extra` 美元尽可能多地划分成若干个 `7`，得到的数量 `k = extra // 7`（整除向下取）。  
   - 但 `k` 不能超过孩子总数 `children`，所以 `k = min(children, extra // 7)`。  

4. **处理唯一的违规情况**  
   - 只要把 `k` 个孩子设为 8 美元，剩余的钱就是 `money - 8*k`，剩下的孩子数是 `children - k`。  
   - 唯一会导致**恰好只能给某个孩子 4 美元**的情况是：  
     - **只剩一个孩子**（`children - k == 1`）且  
     - **剩余的钱正好是 4 美元**（`money - 8*k == 4`）。  
   - 这时我们必须**把一个已经是 8 美元的孩子改成 7 美元**（即把 `k` 减 1），这样就可以把 4 美元拆成 3+1，避免出现 4。  

5. **返回结果**  
   - 经过上面的调整后，`k` 就是可以得到的 **最大** “恰好 8 美元的孩子数**。  

> **核心概念解释**  
> - **贪心**：每一步都做“局部最优”，这里的局部最优是“尽可能多地把 7 美元分配给一个孩子”。因为每多出一个 8 美元孩子，只会消耗固定的 7 美元，且不会影响后面孩子的分配可行性（只要不出现唯一的 4 美元冲突）。  
> - **整除 (`//`)**：把剩余的 `extra` 美元“均匀切成 7 的块”。比如 `extra = 15`，`15 // 7 = 2`，表示可以让 2 个孩子额外得到 7 美元（即 8 美元），剩下 1 美元随意分配。  

#### 代码（Python）  

```python
def maxChildrenWithEight(money: int, children: int) -> int:
    # 规则 1：每个孩子至少 1 美元
    if money < children:
        return -1

    # 先把每个孩子分到 1 美元，剩下的就是可以自由分配的额外钱
    extra = money - children               # 需要再分配的金额

    # 每让一个孩子变成 “8 美元”，就需要额外的 7 美元
    # 先算出最多能有多少个 8 美元的孩子（不考虑 “4 美元” 规则）
    k = min(children, extra // 7)          # 初步的最大 k

    # 检查唯一的违规情况：只剩一个孩子且只能给他 4 美元
    # 此时的剩余钱 = money - 8 * k
    if children - k == 1 and money - 8 * k == 4:
        # 把一个已经是 8 美元的孩子改成 7 美元（即 k 减 1），
        # 剩余的 4 美元可以拆成 3+1，避免出现 4
        k -= 1

    return k
```

> **关键行中文注释**  
> - `if money < children:` 先判断最基本的“钱不够每人 1 美元”。  
> - `extra = money - children` 把必给的 1 美元剔除，剩下的就是“自由”钱。  
> - `k = min(children, extra // 7)` 每个 8 美元孩子需要额外 7 美元，取整除得到最多的数量，同时不能超过总孩子数。  
> - `if children - k == 1 and money - 8 * k == 4:` 检测唯一的“只能给 4 美元”冲突。  
> - `k -= 1` 冲突时把一个 8 美元孩子降到 7 美元，消除冲突。  

#### 复杂度  

- **时间复杂度**：`O(1)` → 只做了几次算术运算和条件判断，时间不随输入规模增长。  
- **空间复杂度**：`O(1)` → 只用了固定数量的整数变量。  

与暴力解相比，最优解把“遍历所有可能的 k”压缩成了“一次算式”，在时间上从 `O(children)` 降到了 `O(1)`，在实际运行时更快、更简洁。  

---  

## 心得  

- **核心技巧**：把“每人至少 1 美元”先固定下来，剩余的金额就可以看成 **“额外的自由钱”**，进而把“恰好 8 美元”转化为“再加 7 美元”。这种把问题拆解为“固定基准 + 增量” 的思路是很多 **贪心** 题目的通用套路。  
- **适用的题型**（类似思路）  
  1. **分配糖果/礼物**：每人至少得到 1 件，再把剩余的礼物按固定增量分配。  
  2. **最大化特定金额的硬币**：先给每种硬币一个基准，然后把剩余金额按硬币面值的增量贪心分配。  
- **一句话总结**：**先满足最小要求，再把剩余资源按固定“增量”尽可能多地转化为目标状态，唯一的特殊冲突单独处理。**  

---  

## 反思  

- **第一反应**：把每个孩子先分 1 美元，然后思考如何把更多的 8 美元“装进去”。这一步把问题从“复杂的分配”转化为“把多余的钱划分成若干 7”。  
- **最容易踩的坑**  
  1. **忘记检查 `money < children`**，导致出现负的“额外钱”。  
  2. **漏掉唯一的冲突情况**——只剩一个孩子且只能给他 4 美元，这会直接导致答案错误。  
  3. **边界条件**：`children` 很小或 `money` 恰好等于 `children` 时，答案应为 `0`（没有孩子能得到 8 美元）。  
- **下次遇到同类题**，第一步应该先**“确定每个人的最小配额”**（比如 1 美元、1 件礼物），把剩余资源抽象出来，再思考**“每增加一个目标状态需要消耗多少额外资源”**，最后检查是否有**“唯一的不可接受剩余”**需要特别处理。