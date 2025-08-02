# #3289. Digitville的两个狡猾数字 / The Two Sneaky Numbers of Digitville

> 难度：简单 · 标签：Array、Hash Table、Math · [LeetCode 链接](https://leetcode.com/problems/the-two-sneaky-numbers-of-digitville/)

---

## 题目（英文原版）

**Description**

In the town of Digitville, there was a list of numbers called nums containing integers from 0 to n - 1. Each number was supposed to appear exactly once in the list, however, two mischievous numbers sneaked in an additional time, making the list longer than usual.
As the town detective, your task is to find these two sneaky numbers. Return an array of size two containing the two numbers (in any order), so peace can return to Digitville.

**Examples**

**Example 1:**

```
Input: nums = [0,1,1,0]
Output: [0,1]
Explanation:
The numbers 0 and 1 each appear twice in the array.
```

**Example 2:**

```
Input: nums = [0,3,2,1,3,2]
Output: [2,3]
Explanation:
The numbers 2 and 3 each appear twice in the array.
```

**Example 3:**

```
Input: nums = [7,1,5,4,3,4,6,0,9,5,8,2]
Output: [4,5]
Explanation:
The numbers 4 and 5 each appear twice in the array.
```

**Constraints**

- 2 <= n <= 100
- nums.length == n + 2
- 0 <= nums[i] < n
- The input is generated such that nums contains exactly two repeated elements.

---

## 题目（中文翻译）

在 Digitville 小镇上，有一个整数列表 `nums`，其中的整数取值范围是 `0` 到 `n - 1`。原本每个数字应该只出现一次，但有两个顽皮的数字各自多出现了一次，使得列表的长度比正常情况多出两个。

作为小镇的侦探，你的任务是找出这两个多余出现的数字。返回一个长度为二的数组（array），其中包含这两个数字（顺序不限），让小镇恢复平静。

**示例 1**  
**输入**: `nums = [0,1,1,0]`  
**输出**: `[0,1]`  
**解释**:  
数字 `0` 和 `1` 在数组中各出现两次。

**示例 2**  
**输入**: `nums = [0,3,2,1,3,2]`  
**输出**: `[2,3]`  
**解释**:  
数字 `2` 和 `3` 在数组中各出现两次。

**示例 3**  
**输入**: `nums = [7,1,5,4,3,4,6,0,9,5,8,2]`  
**输出**: `[4,5]`  
**解释**:  
数字 `4` 和 `5` 在数组中各出现两次。

**约束条件**  

- `2 <= n <= 100`
- `nums.length == n + 2`
- `0 <= nums[i] < n`
- 输入保证恰好有两个重复的元素。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个数字出现的次数都统计一遍，出现两次的就是我们要找的“偷偷出现的两个数字”。  
- **用到的数据结构**：哈希表（在 Python 里可以直接用 `dict`）。可以把它想象成一本字典，**key** 就是我们要查的“单词”（这里是数组里的数字），**value** 是对应的“页码”（这里是出现的次数）。  
- **为什么正确**：遍历数组一次，把每个数字的出现次数记录下来。遍历完后，检查哈希表里哪些 key 对应的 value 等于 2，正好就是那两个重复的数字。  
- **时间/空间复杂度**：  
  - 时间：我们要遍历整个数组一次，**O(n)**（n 为数组长度），再遍历哈希表一次（最多 n+2 项），仍然是 **O(n)**。  
  - 空间：需要额外存储每个不同数字的计数，最坏情况下会有 n 个不同的数字，所以需要 **O(n)** 的额外空间。  

> 大白话解释：如果把数组想象成一排排小盒子，暴力解就是先把每个盒子里的数字贴上标签（出现次数），再把所有标签翻出来找出标了“2”的两个盒子。虽然直观，但要准备一张和盒子数量一样大的贴纸表（哈希表），空间稍微大一点。

#### 代码（Python）

```python
def findTwoDuplicates_bruteforce(nums):
    # 第一步：统计每个数字出现的次数，用 dict 当作“查字典”
    count = {}                       # key: 数字，value: 出现次数
    for x in nums:                   # 遍历整个数组
        count[x] = count.get(x, 0) + 1   # 没出现过默认 0，出现一次加 1

    # 第二步：把出现两次的数字挑出来
    res = []
    for num, freq in count.items():  # 检查每个 (数字, 次数) 对
        if freq == 2:                # 正好出现两次的就是我们要的
            res.append(num)
            if len(res) == 2:        # 找到两个就可以提前结束
                break
    return res
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历了两遍数组（一次计数，一次挑选），即使说是两遍，常数因子不影响“大 O”。
- **空间复杂度**：`O(n)` — 需要一个大小和不同数字数量相同的字典，最坏会有 `n` 条记录。

---

### 2. 最优解

#### 思路  

从暴力解出发，**慢的地方**其实不在时间上（已经是线性），而是**额外的空间**——我们用了一个哈希表来记录出现次数。  
如果我们只想要 **O(1) 额外空间**，可以利用数学性质来“间接”求出那两个重复的数字。

> **核心想法**：  
> - 已知数组里本来应该出现一次的数字是 `0 … n-1`，它们的**总和**和**总平方和**都有固定公式。  
> - 现在因为两个数字 `a`、`b` 各多出现了一次，实际的总和会比理想值多 `a + b`，总平方和会多 `a² + b²`。  
> - 用这两个“差值”我们可以列出两个方程，解出 `a` 与 `b`。

**步骤**：

1. **计算理想总和 & 理想平方和**  
   - `ideal_sum = n * (n - 1) // 2`（等差数列求和公式）  
   - `ideal_sq_sum = n * (n - 1) * (2 * n - 1) // 6`（平方和公式）  

2. **遍历一次数组，得到实际的总和 & 实际平方和**  
   - `real_sum = sum(nums)`  
   - `real_sq_sum = sum(x * x for x in nums)`  

3. **求出差值**  
   - `S = real_sum - ideal_sum = a + b`  
   - `Sq = real_sq_sum - ideal_sq_sum = a² + b²`  

4. **从 S、Sq 求出 a 与 b**  
   - 先算出 `ab`（两数乘积）：  
     \[
     (a + b)^2 = a^2 + b^2 + 2ab \;\Rightarrow\; 
     ab = \frac{S^2 - Sq}{2}
     \]  
   - 现在我们有二元一次方程组  
     \[
     \begin{cases}
     a + b = S \\
     a \cdot b = P
     \end{cases}
     \]  
   - 把它们代入二次方程 `x² - Sx + P = 0`，根就是 `a`、`b`。  
   - 判别式 `D = S² - 4P` 必为完全平方数，`sqrt(D)` 用整数平方根 `int(D**0.5)` 获得。  
   - 最后  
     \[
     a = \frac{S + \sqrt{D}}{2},\quad b = S - a
     \]

**为什么一定能得到整数解？**  
因为题目保证数组只出现了两个重复的整数，它们本身就在 `0 … n-1` 范围内，所有推导都是在整数域进行的，判别式必是完全平方数。

> **类比**：想象有一堆糖果，原本每种口味都有一颗，现在有两种口味各多了一颗。我们先数出总糖果数和总糖果重量（平方和），再用“应有的”数目减去实际数目，差值正好是多出来的两颗的口味编号。

#### 代码（Python）

```python
import math

def findTwoDuplicates_optimal(nums):
    n = len(nums) - 2               # 原本应该有的数字个数
    # 1. 理想的总和、平方和
    ideal_sum = n * (n - 1) // 2
    ideal_sq_sum = n * (n - 1) * (2 * n - 1) // 6

    # 2. 实际的总和、平方和（一次遍历即可）
    real_sum = 0
    real_sq_sum = 0
    for x in nums:
        real_sum += x               # 累加当前数字
        real_sq_sum += x * x        # 累加当前数字的平方

    # 3. 差值 S = a + b,  Sq = a^2 + b^2
    S = real_sum - ideal_sum
    Sq = real_sq_sum - ideal_sq_sum

    # 4. 计算 a * b
    #    ab = (S^2 - Sq) / 2   （一定能整除，因为题目保证）
    P = (S * S - Sq) // 2

    # 5. 解二次方程 x^2 - Sx + P = 0
    #    判别式 D = S^2 - 4P 必为完全平方数
    D = S * S - 4 * P
    sqrt_D = int(math.isqrt(D))     # 整数平方根，避免浮点误差

    a = (S + sqrt_D) // 2           # 第一个重复数字
    b = S - a                       # 第二个重复数字（因为 a + b = S）

    return [a, b]
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次数组，所有其它操作都是常数时间。  
  与暴力解的时间相同，但省去了第二次遍历哈希表的开销，实际常数更小。
- **空间复杂度**：`O(1)` — 只使用了若干个整数变量，没有额外的数组或哈希表。  
  相比暴力解节省了 **n** 级别的空间，满足“无额外空间”要求。

---

## 心得

- **核心技巧**：利用**数学求和/平方和公式**把“出现次数”信息转化为**代数方程**，再通过求根得到重复元素。  
- **适用的题型**：  
  1. “找数组中唯一出现一次的数”类（利用异或或求和）  
  2. “数组中出现三次/两次的数”类（利用位运算或计数）  
  3. “数组中缺失的数”或“重复且缺失的数”类（同样可以用和、平方和或异或）  
- **一句话总结**：**把“计数”换成“求和”，用代数方程一次解出所有重复数字。**

---

## 反思

- **第一反应**：直接想到哈希表计数，因为它最直观、实现最快。  
- **最容易踩的坑**：  
  - 计算平方和时容易溢出（在 Python 中整数无限大不成问题，但在语言限制里要用 64 位）。  
  - 判别式 `D` 必须是完全平方数，若使用浮点 `sqrt` 可能出现精度误差，建议用整数平方根 `math.isqrt`。  
  - 当 `n` 较大时，`S²` 可能超过 32 位整数范围，需使用 64 位或 Python 大整数。  
- **下次遇到同类题**：第一步先思考“能否用整体的和/平方和/异或把局部计数信息整体化”，如果可以，就尝试把问题转化为求解方程或位运算，而不是直接用额外的存储结构。