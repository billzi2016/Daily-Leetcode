# #2197. 替换数组中的非互质数 / Replace Non-Coprime Numbers in Array

> 难度：困难 · 标签：Array、Math、Stack、Number Theory · [LeetCode 链接](https://leetcode.com/problems/replace-non-coprime-numbers-in-array/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums. Perform the following steps:
Return the final modified array. It can be shown that replacing adjacent non-coprime numbers in any arbitrary order will lead to the same result.
The test cases are generated such that the values in the final array are less than or equal to 108.
Two values x and y are non-coprime if GCD(x, y) > 1 where GCD(x, y) is the Greatest Common Divisor of x and y.

**Examples**

**Example 1:**

```
Input: nums = [6,4,3,2,7,6,2]
Output: [12,7,6]
Explanation: 
- (6, 4) are non-coprime with LCM(6, 4) = 12. Now, nums = [12,3,2,7,6,2].
- (12, 3) are non-coprime with LCM(12, 3) = 12. Now, nums = [12,2,7,6,2].
- (12, 2) are non-coprime with LCM(12, 2) = 12. Now, nums = [12,7,6,2].
- (6, 2) are non-coprime with LCM(6, 2) = 6. Now, nums = [12,7,6].
There are no more adjacent non-coprime numbers in nums.
Thus, the final modified array is [12,7,6].
Note that there are other ways to obtain the same resultant array.
```

**Example 2:**

```
Input: nums = [2,2,1,1,3,3,3]
Output: [2,1,1,3]
Explanation: 
- (3, 3) are non-coprime with LCM(3, 3) = 3. Now, nums = [2,2,1,1,3,3].
- (3, 3) are non-coprime with LCM(3, 3) = 3. Now, nums = [2,2,1,1,3].
- (2, 2) are non-coprime with LCM(2, 2) = 2. Now, nums = [2,1,1,3].
There are no more adjacent non-coprime numbers in nums.
Thus, the final modified array is [2,1,1,3].
Note that there are other ways to obtain the same resultant array.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105
- The test cases are generated such that the values in the final array are less than or equal to 108.

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组（array）`nums`。按照以下规则不断进行替换，直至无法再进行：

- 若相邻的两个数 `x` 和 `y` 为非互质数（non‑coprime），即它们的最大公约数（GCD）> 1，则用这两个数的最小公倍数（LCM）替换这两个数，并将数组长度缩减 1。

返回最终得到的数组。可以证明，无论以何种顺序替换相邻的非互质数，最终结果都是相同的。  
题目保证最终数组中的所有值均不超过 `10^8`。

**定义**  
- 两个数 `x` 和 `y` 为非互质数（non‑coprime）当且仅当 `GCD(x, y) > 1`，其中 `GCD` 为最大公约数（Greatest Common Divisor）。

---

### 示例

**示例 1**  
```
Input: nums = [6,4,3,2,7,6,2]
Output: [12,7,6]
Explanation:
- (6, 4) 为非互质数，LCM(6, 4) = 12 → nums = [12,3,2,7,6,2]
- (12, 3) 为非互质数，LCM(12, 3) = 12 → nums = [12,2,7,6,2]
- (12, 2) 为非互质数，LCM(12, 2) = 12 → nums = [12,7,6,2]
- (6, 2) 为非互质数，LCM(6, 2) = 6 → nums = [12,7,6]
此时已不存在相邻的非互质数，返回 [12,7,6]。
```

**示例 2**  
```
Input: nums = [2,2,1,1,3,3,3]
Output: [2,1,1,3]
Explanation:
- (3, 3) 为非互质数，LCM(3, 3) = 3 → nums = [2,2,1,1,3,3]
- (3, 3) 为非互质数，LCM(3, 3) = 3 → nums = [2,2,1,1,3]
- (2, 2) 为非互质数，LCM(2, 2) = 2 → nums = [2,1,1,3]
此时已不存在相邻的非互质数，返回 [2,1,1,3]。
```

---

### 约束条件
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`
- 题目保证最终数组中的所有值均 `<= 10^8`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一次遍历**数组，找到相邻的两数 `x、y`，如果它们 **不是互质**（即 `gcd(x, y) > 1`），就把这两个数合并成它们的最小公倍数 `lcm(x, y)`，随后数组长度会减 1。  
然后把新得到的数组重新从头开始检查，直到再也找不到相邻的非互质数为止。

- **用到的数据结构**：普通的 Python 列表（list）。可以把它想象成一排排的盒子，合并两盒子后把后面的盒子往左挪，空出来的位子再填上新盒子。
- **为什么正确**：题目已经说明“无论以什么顺序合并相邻的非互质数，最终结果都是唯一的”。所以只要我们一次把任意一对满足条件的相邻数合并，最终一定会收敛到同一个数组。
- **时间/空间复杂度**：  
  - 每次遍历最坏要检查 `n-1` 对相邻数。如果找到一对就立刻合并，数组长度会减 1。最坏情况下可能需要 **O(n)** 次遍历，每次遍历的工作量也是 **O(n)**，于是总时间复杂度是 **O(n²)**。  
  - 只用了原数组本身，没有额外的显著空间，空间复杂度是 **O(1)**（不计返回值本身）。

> **大白话解释**：`O(n²)` 就像你要把 1000 本书两两比较，第一遍要比较 999 次，第二遍 998 次……最后加起来差不多是 1000×1000/2 ≈ 500,000 次，比线性 `O(n)`（只走一遍）慢很多。

#### 代码（Python）

```python
import math
from typing import List

def replaceNonCoprime_bruteforce(nums: List[int]) -> List[int]:
    """
    暴力解：每次从左到右找一对相邻非互质数，合并后重新开始遍历
    """
    i = 0
    while i < len(nums) - 1:               # 只要还有相邻的两个数就继续
        a, b = nums[i], nums[i + 1]
        if math.gcd(a, b) > 1:             # gcd>1 表示不是互质
            # 计算最小公倍数：lcm = a*b // gcd(a,b)
            lcm = a // math.gcd(a, b) * b   # 先除后乘防止中间乘积溢出
            # 用 lcm 替换掉 a、b 两个位置
            nums[i] = lcm
            del nums[i + 1]                # 删除右边的那个数，数组长度-1
            # 合并后需要再次检查左边的元素是否还能合并
            i = max(i - 1, 0)               # 回退一步（或保持在 0）
        else:
            i += 1                          # 互质，继续向右检查
    return nums
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：最坏情况下每次只合并最左边的一对，需要遍历 `n-1 + n-2 + … + 1 ≈ n²/2` 次。
- **空间复杂度**：`O(1)`（不计输出列表本身）  
  解释：只在原数组上原地修改，没有额外使用与输入规模相关的容器。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每合并一次就重新从头遍历**，导致大量重复检查。我们需要一种数据结构，使得“合并后只检查左侧最近的元素”变得**常数时间**。

**核心想法**：使用 **栈**（stack）模拟左侧已经处理好的序列。  
- 栈顶永远是当前元素左边最近的、已经“确定”不会再和更左边的数合并的值。  
- 当我们把新的数字 `x` 推入栈时，只需要和栈顶 `y` 检查 `gcd(x, y)`。如果 `gcd > 1`，说明 `x` 与左侧最近的数 `y` 需要合并，弹出 `y`，把 `lcm(x, y)` 当作新的 `x` 再次和栈顶比较。  
- 这一步可能会产生“链式合并”：新的 `x` 可能继续与更左的数合并。于是我们使用 **while 循环**把这个过程一直做完，再把最终的 `x` 放进栈。

**为什么只看栈顶就够**：  
栈里保存的顺序正好是 **从左到右** 已经处理好的数组。假设栈中有 `[a, b, c]`（`c` 为栈顶），我们正要加入 `d`。若 `d` 与 `c` 互质，那么 `d` 与更左的 `b、a` 必然也互质，因为若 `d` 与 `b` 非互质，那么 `b` 与 `c` 必须已经合并过（否则 `b` 和 `c` 仍相邻且非互质），导致 `b` 已经不在栈里了。这正是题目保证“合并顺序不影响最终结果”的数学依据。

**算法步骤**：

1. 初始化空栈 `stack = []`。  
2. 依次遍历原数组 `num`：  
   - 把 `num` 赋值给变量 `cur`。  
   - `while stack` 且 `gcd(stack[-1], cur) > 1`：  
        - `prev = stack.pop()`  
        - `cur = lcm(prev, cur) = prev // gcd(prev, cur) * cur`（先除后乘防止溢出）  
   - 循环结束后，`cur` 与左侧最近的数已不再非互质，`stack.append(cur)`。  
3. 循环结束后，栈里从左到右的顺序即为最终数组，直接返回 `stack`。

**关键概念解释**：

- **最大公约数 GCD**：可以把它想象成“两个数共同拥有的最大‘因子’”。我们用欧几里得算法（`math.gcd`）快速求出。  
- **最小公倍数 LCM**：是两个数都能被整除的最小正整数，公式 `lcm(a,b) = a // gcd(a,b) * b`。先除再乘是为了避免中间乘积过大导致 Python 整数运算变慢（虽然 Python 整数是大数，但先除仍是好习惯）。  
- **栈**：想象一摞盘子，**只能在最上面放盘子或拿走最上面的盘子**。这里的盘子就是已经确定的数组元素。

#### 代码（Python）

```python
import math
from typing import List

def replaceNonCoprime(nums: List[int]) -> List[int]:
    """
    最优解：使用单调栈模拟左侧已处理序列，只与栈顶比较
    """
    stack: List[int] = []                # 用列表当栈，stack[-1] 是栈顶

    for num in nums:                     # 逐个遍历原数组
        cur = num                         # 当前要处理的数

        # 与左侧最近的数（栈顶）不断合并，直到互质为止
        while stack and math.gcd(stack[-1], cur) > 1:
            left = stack.pop()           # 弹出左侧最近的数
            # 计算 lcm，先除后乘防止中间乘积过大
            cur = left // math.gcd(left, cur) * cur

        stack.append(cur)                # 合并结束后，把结果压入栈

    return stack                         # 栈中顺序即为答案
```

#### 复杂度

- **时间复杂度**：`O(n * log C)`（近似 `O(n)`）  
  - 每个元素最多被压入栈一次、弹出一次。弹出时会计算一次 GCD，欧几里得算法的复杂度是 `O(log min(a,b))`，而 `a、b ≤ 10⁸`（题目保证），所以整体是线性 `O(n)` 加上一个很小的对数因子。  
  - 与暴力解 `O(n²)` 相比，**只遍历一次**，大幅提升效率。

- **空间复杂度**：`O(n)`  
  - 最坏情况下所有元素都互质，栈会保存全部 `n` 个数。使用的额外空间正比于输入规模。

---

## 心得

- **核心技巧**：**栈 + GCD/LCM 的贪心合并**。  
- **适用的题型**：  
  1. “相邻元素满足某种关系时合并” 类的题目（如 LeetCode 1541 *Minimum All One Subarray* 的单调栈思路）。  
  2. “需要把左侧最近的满足条件的元素合并” 的数论题（如 “合并相邻相等数” 或 “相邻数的最大公约数大于 1”）。  
- **一句话总结解题钥匙**：**只看左侧最近的元素，用栈把“递归合并”压缩成 O(1) 操作**。

---

## 反思

- **第一反应**：直接写双层循环不停合并，忽略了大量重复检查。  
- **最容易踩的坑**：  
  - **整数溢出**：`lcm = a * b // gcd` 在语言里可能会产生中间乘积过大，先除后乘是安全写法。  
  - **忘记递归合并**：合并后得到的新数可能还能和更左的数合并，需要在 `while` 循环里继续检查。  
  - **边界情况**：数组全是 1（互质）或全是相同的数，需要确保栈操作不会出错。  
- **下次遇到同类题**，第一步应想到**“用栈维护左侧已处理好的序列，只与最近的元素比较”**，从而把重复遍历的成本降到最低。