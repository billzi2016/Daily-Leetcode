# #2511. 最大可捕获的敌方要塞数量 / Maximum Enemy Forts That Can Be Captured

> 难度：简单 · 标签：Array、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/maximum-enemy-forts-that-can-be-captured/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array forts of length n representing the positions of several forts. forts[i] can be -1, 0, or 1 where:
Now you have decided to move your army from one of your forts at position i to an empty position j such that:
While moving the army, all the enemy forts that come in the way are captured.
Return the maximum number of enemy forts that can be captured. In case it is impossible to move your army, or you do not have any fort under your command, return 0.

**Examples**

**Example 1:**

```
Input: forts = [1,0,0,-1,0,0,0,0,1]
Output: 4
Explanation:
- Moving the army from position 0 to position 3 captures 2 enemy forts, at 1 and 2.
- Moving the army from position 8 to position 3 captures 4 enemy forts.
Since 4 is the maximum number of enemy forts that can be captured, we return 4.
```

**Example 2:**

```
Input: forts = [0,0,1,-1]
Output: 0
Explanation: Since no enemy fort can be captured, 0 is returned.
```

**Constraints**

- 1 <= forts.length <= 1000
- -1 <= forts[i] <= 1

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组（array）`forts`，长度为 `n`，用于表示若干要塞的位置。`forts[i]` 的取值只能是 **-1**、**0** 或 **1**，含义如下：

- `1`：你控制的要塞（friendly fort）  
- `-1`：敌方要塞（enemy fort）  
- `0`：空位（empty position）

你可以选择将军队从你控制的某个要塞位置 `i`（`forts[i] == 1`）移动到一个空位 `j`（`forts[j] == 0`），要求满足：

- `i` 与 `j` 之间的所有位置（不包括 `i`、`j`）必须全部是敌方要塞，即 `forts[k] == -1`，其中 `min(i, j) < k < max(i, j)`。  
- 在移动过程中，途经的所有敌方要塞都会被占领（captured）。

返回在一次合法移动中能够捕获的敌方要塞的最大数量。如果不存在任何合法的移动，或你根本没有控制任何要塞，返回 **0**。

---

### 示例

#### 示例 1
> **输入**: `forts = [1,0,0,-1,0,0,0,0,1]`  
> **输出**: `4`  
> **解释**:  
> - 将军队从位置 `0` 移动到位置 `3`，可以捕获位于 `1` 与 `2` 的 **2** 个敌方要塞。  
> - 将军队从位置 `8` 移动到位置 `3`，可以捕获 **4** 个敌方要塞。  
> 由于 `4` 是能够捕获的最大敌方要塞数量，返回 `4`。

#### 示例 2
> **输入**: `forts = [0,0,1,-1]`  
> **输出**: `0`  
> **解释**: 没有任何合法的移动可以捕获敌方要塞，返回 `0`。

---

### 约束条件
- `1 <= forts.length <= 1000`  
- `-1 <= forts[i] <= 1`   (即 `forts[i]` 只能是 **-1**、**0** 或 **1**)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的出发点和目的地**，然后检查它们之间的路是否满足题目要求。

- **出发点**只能是自己阵营的要塞 `forts[i] == 1`。  
- **目的地**只能是空地 `forts[j] == 0`。  
- 两者之间（不包括 i、j）必须全是敌方要塞 `-1`，否则这条路线不可行。  

我们可以把数组想象成一条街道，`1` 是我们的大本营，`0` 是空地，`-1` 是敌人的哨所。要想搬兵，我们需要从大本营出发，走到最近的空地，途中只能经过敌人的哨所（就像只能走“敌人占领的街区”）。

遍历所有 `(i, j)` 对，满足 `i != j`，如果 `forts[i] == 1` 且 `forts[j] == 0`，再检查 `i` 与 `j` 之间是否全是 `-1`。若是，则捕获的敌方要塞数量等于两者之间 `-1` 的个数。把所有合法情况的捕获数取最大即可。

**为什么这个方法一定正确？**  
因为我们把**所有**可能的出发点和目的地都遍历了一遍，并且对每一种情况都做了完整的合法性检查，遗漏的情况不可能出现。

**时间/空间复杂度**  
- 外层遍历 `i`，内层遍历 `j`，每一次还要再遍历一次区间检查，最坏情况下相当于三层循环，时间复杂度是 **O(n³)**（这里的 `n` 是数组长度）。在实际实现时，我们可以把区间检查合并到 `j` 的遍历里，使其变成两层循环，时间复杂度 **O(n²)**。  
- 空间上只用了常数个额外变量，**O(1)**。

> **大白话**：  
> - `O(n²)` 就像你把每个人都跟每个人比一遍，次数是“人数的平方”。如果有 1000 个人，你得比较 1,000,000 次。  
> - `O(1)` 就是说你只用了几张纸记下几个数字，和输入大小无关。

#### 代码（Python）

```python
def capture_bruteforce(forts):
    n = len(forts)
    max_capture = 0                     # 记录最大捕获数

    for i in range(n):                  # 枚举出发点 i
        if forts[i] != 1:               # 只能从自己的要塞出发
            continue
        for j in range(n):              # 枚举目的地 j
            if forts[j] != 0:           # 只能到空地结束
                continue
            # 判断 i 与 j 之间是否全是 -1
            left, right = min(i, j) + 1, max(i, j)
            ok = True
            cnt = 0                     # 统计 -1 的个数
            for k in range(left, right):
                if forts[k] != -1:      # 出现 0 或 1，路不合法
                    ok = False
                    break
                cnt += 1                # 合法的敌方要塞
            if ok:                       # 合法则更新答案
                max_capture = max(max_capture, cnt)

    return max_capture
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：两层循环分别遍历 `i`、`j`，每对 `(i, j)` 只检查一次区间，总操作数随 `n` 的平方增长。

- **空间复杂度**：`O(1)`  
  解释：只用了几个计数器和指针，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**反复检查同一段区间**。如果我们从左到右一次遍历，就能把这些检查“省掉”，只需要**记录最近的起点**，并在遇到合适的终点时立即算出捕获数。

关键观察：

1. **合法的路线只能是形如**  
   - `1 , -1 , -1 , … , -1 , 0`（向右移动）  
   - `0 , -1 , -1 , … , -1 , 1`（向左移动）  
   也就是说，两个**不同**的端点（一个是 `1`，另一个是 `0`）之间必须全是 `-1`，不能出现 `0` 或 `1` 打断。

2. **当我们从左往右扫描时**，只要记住上一次出现的 `1` 或 `0`（称为“上一个非 -1 的位置”），
   - 如果当前元素是 `-1`，我们继续前进，什么也不做；
   - 如果当前元素是 `0` 或 `1`，我们就找到了一个“区间的右端”。  
   这时检查左端和右端是否互为 `1` 与 `0`（即 `forts[left] != forts[right]`），如果是，则两端之间的 `-1` 数目就是捕获数。

3. **双指针实现**  
   - `left` 保存最近的非 `-1` 位置（起点），初始化为 `-1` 表示还未出现。  
   - `right` 是遍历指针，从 `0` 到 `n-1`。  
   - 每当 `right` 指向 `0` 或 `1` 时，先判断 `left` 是否已经存在且两端不同；若符合，更新答案；随后把 `left` 移到 `right`（因为新的区间可能会以当前点为左端）。

这样只需要一次线性扫描，**每个元素最多访问两次**（一次作为 `right`，一次可能成为新的 `left`），时间复杂度降到 **O(n)**。

#### 代码（Python）

```python
def capture_optimal(forts):
    """
    使用一次遍历 + 双指针找出最大捕获数
    """
    n = len(forts)
    max_capture = 0          # 记录最大捕获数
    left = -1                # 最近的非 -1 位置，-1 表示尚未出现

    for right in range(n):
        if forts[right] == -1:
            # 仍在敌方要塞的“通道”里，继续向前
            continue

        # 此时 forts[right] 为 0 或 1，构成了一个区间的右端
        if left != -1 and forts[left] != forts[right]:
            # 左端和右端不同（必然是 1 与 0），
            # 区间之间全是 -1（因为若有 0/1，left 会提前被更新）
            capture = right - left - 1   # 两端之间的元素个数，即 -1 的数量
            max_capture = max(max_capture, capture)

        # 更新左端为当前非 -1 的位置，准备寻找下一段区间
        left = right

    return max_capture
```

**代码要点解释**：

| 行号 | 关键代码 | 中文注释 |
|------|----------|----------|
| 4    | `left = -1` | 用 `-1` 表示“还没有遇到任何 0/1”。 |
| 7-9  | `if forts[right] == -1: continue` | 遇到 `-1` 只需要跳过，因为它只能是“路上的敌人”。 |
| 12   | `if left != -1 and forts[left] != forts[right]:` | 确保左端已经出现且两端是不同的符号（1 与 0）。 |
| 13   | `capture = right - left - 1` | 两端之间的距离减一，就是被捕获的 `-1` 个数。 |
| 16   | `left = right` | 把当前的非 `-1` 位置设为新的左端。 |

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：只遍历一次数组，每个元素做 O(1) 的常数操作。相比暴力的 `O(n²)`，速度提升了好几个数量级。

- **空间复杂度**：`O(1)`  
  解释：只用了几个整数变量（`left`, `right`, `max_capture`），不随输入规模增长。

---

## 心得

- **核心技巧**：**利用“相邻非 -1 元素之间只能出现 -1” 的特性，用双指针一次遍历找出合法区间**。  
- **适用的题型**：  
  1. “只允许特定字符/数字在两端出现，中间只能是另一种字符”——例如 *“Maximum Consecutive Ones Between Zeros”*。  
  2. “两端相同/不同且中间满足某种单调或固定值”——例如 *“Find the Longest Subarray With Equal Number of 0s and 1s”*（思路类似，利用前缀和）。  
  3. “在数组中找出满足特定模式的子数组”——如 *“Number of Subarrays with Bounded Maximum”*（使用双指针滑动窗口）。  

- **一句话总结解题钥匙**：**把“只能经过 -1”的约束转化为“相邻的非 -1 元素之间必然全是 -1”，用两个指针捕捉每一段合法区间即可。**

---

## 反思

- **第一反应**：看到题目立刻想到枚举所有 `1` 与 `0` 的组合，然后检查中间是否全是 `-1`。这就是最自然的暴力思路。  
- **最容易踩的坑**：  
  - 忘记考虑 **左移** 的情况（从右侧的 `1` 移到左侧的 `0`），导致只算了一半的答案。  
  - 在判断合法区间时，没有保证区间中 **没有其他 0 或 1**，导致错误计数。  
  - 边界情况：整个数组没有 `1` 或没有 `0` 时应直接返回 `0`，否则代码可能访问未初始化的 `left`。  
- **下次遇到同类题**，第一步应该先**抽象出“合法区间的结构”**（比如两端固定，中间只能是某种值），再思考**如何只遍历一次就能捕获所有这种结构**，常用工具是**双指针/滑动窗口**。