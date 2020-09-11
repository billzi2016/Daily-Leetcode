# #985. 查询后数组偶数之和 / Sum of Even Numbers After Queries

> 难度：中等 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/sum-of-even-numbers-after-queries/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an array queries where queries[i] = [vali, indexi].
For each query i, first, apply nums[indexi] = nums[indexi] + vali, then print the sum of the even values of nums.
Return an integer array answer where answer[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4], queries = [[1,0],[-3,1],[-4,0],[2,3]]
Output: [8,6,2,4]
Explanation: At the beginning, the array is [1,2,3,4].
After adding 1 to nums[0], the array is [2,2,3,4], and the sum of even values is 2 + 2 + 4 = 8.
After adding -3 to nums[1], the array is [2,-1,3,4], and the sum of even values is 2 + 4 = 6.
After adding -4 to nums[0], the array is [-2,-1,3,4], and the sum of even values is -2 + 4 = 2.
After adding 2 to nums[3], the array is [-2,-1,3,6], and the sum of even values is -2 + 6 = 4.
```

**Example 2:**

```
Input: nums = [1], queries = [[4,0]]
Output: [0]
```

**Constraints**

- 1 <= nums.length <= 104
- -104 <= nums[i] <= 104
- 1 <= queries.length <= 104
- -104 <= vali <= 104
- 0 <= indexi < nums.length

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums` 和一个查询数组（array）`queries`，其中 `queries[i] = [val_i, index_i]`。  
对于每个查询 `i`，首先执行 `nums[index_i] = nums[index_i] + val_i`，随后输出 `nums` 中所有偶数值（even values）的和。  
返回一个整数数组 `answer`，其中 `answer[i]` 为第 `i` 次查询的答案。  

### 示例

#### 示例 1
**输入**  
`nums = [1,2,3,4]`，`queries = [[1,0],[-3,1],[-4,0],[2,3]]`  

**输出**  
`[8,6,2,4]`  

**解释**  
- 初始数组为 `[1,2,3,4]`。  
- 将 `1` 加到 `nums[0]`，数组变为 `[2,2,3,4]`，偶数值之和为 `2 + 2 + 4 = 8`。  
- 将 `-3` 加到 `nums[1]`，数组变为 `[2,-1,3,4]`，偶数值之和为 `2 + 4 = 6`。  
- 将 `-4` 加到 `nums[0]`，数组变为 `[-2,-1,3,4]`，偶数值之和为 `-2 + 4 = 2`。  
- 将 `2` 加到 `nums[3]`，数组变为 `[-2,-1,3,6]`，偶数值之和为 `-2 + 6 = 4`。  

#### 示例 2
**输入**  
`nums = [1]`，`queries = [[4,0]]`  

**输出**  
`[0]`  

### 约束条件
- `1 <= nums.length <= 10^4`  
- `-10^4 <= nums[i] <= 10^4`  
- `1 <= queries.length <= 10^4`  
- `-10^4 <= val_i <= 10^4`  
- `0 <= index_i < nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：每收到一条查询 `queries[i] = [val, idx]`，先把 `nums[idx]` 加上 `val`，**随后重新遍历整个数组**，把所有偶数加起来得到本次答案。  

- **用到的数据结构**：只需要原始的 `nums` 列表和一个普通的循环。可以把数组想象成一排盒子，盒子里装着数字。我们每次都把所有盒子打开，检查里面的数字是不是偶数（就像检查每本书的页码是否是双数），如果是就把它们的“价值”累加。  
- **为什么正确**：因为我们在每一步都完整地计算了一遍“所有偶数的和”。只要遍历没有漏掉任何元素，答案必然是对的。  
- **时间/空间复杂度**：  
  - **时间**：设数组长度为 `n`，查询数量为 `m`。每次查询都要遍历 `n` 个元素，所以总共要做 `m × n` 次检查。用大 O 记号写成 `O(m·n)`。如果把 `m` 和 `n` 都看成大约是同一个数量级（比如都是 10⁴），那么 `O(m·n)` 就相当于 `O(10⁸)`，在实际运行时会比较慢。  
  - **空间**：只用了原数组和几个整数变量，额外空间是 `O(1)`（常数级），不随 `n`、`m` 增长。

#### 代码（Python）

```python
from typing import List

def sumEvenAfterQueries_bruteforce(nums: List[int], queries: List[List[int]]) -> List[int]:
    """
    暴力解：每次查询后重新遍历 nums，计算所有偶数的和。
    """
    ans = []                     # 用来保存每次查询的结果
    for val, idx in queries:     # 依次处理每条查询
        nums[idx] += val         # 第一步：把 val 加到指定位置
        cur_sum = 0              # 用来累加偶数
        for x in nums:           # 第二步：遍历整个数组
            if x % 2 == 0:       # 判断是否为偶数（% 是取余，偶数余数为 0）
                cur_sum += x
        ans.append(cur_sum)      # 把本次的偶数和加入答案列表
    return ans
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - **含义**：如果 `nums` 长度是 10⁴，`queries` 长度也是 10⁴，那么最坏情况下要执行 10⁸ 次循环，这在 Python 中可能会超时。  
- **空间复杂度**：`O(1)`（不计答案数组本身）  
  - **含义**：我们只用了常数个额外变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要遍历完整个数组**。其实我们并不需要每次都重新求和，因为 **只有一个元素会改变**，其他位置的数字保持不变。  
关键在于维护一个“当前偶数和” `even_sum`，并在每条查询时 **只对受影响的那个元素做增量更新**。

1. **先算一次初始的偶数和**  
   把 `nums` 全部遍历一遍，求出所有偶数的总和 `even_sum`（这一步是 `O(n)`）。  

2. **处理每条查询**  
   - 记住被修改前的值 `old = nums[idx]`。  
   - 如果 `old` 是偶数，则它原本已经贡献到了 `even_sum`，现在要把它的贡献 **先减掉**：`even_sum -= old`。  
   - 更新数组：`nums[idx] += val`。  
   - 再检查更新后的新值 `new = nums[idx]`。  
   - 如果 `new` 是偶数，则把它的值 **加回** 到 `even_sum`：`even_sum += new`。  
   - 此时 `even_sum` 正好是本次查询后的所有偶数之和，直接加入答案。  

这样每条查询只做了常数次（`O(1)`）的操作，整个过程的时间复杂度是 `O(n + m)`，空间仍是 `O(1)`。

**为什么这样能工作**？  
- 偶数之和的变化只能来自被修改的那个位置。  
- 通过 “如果之前是偶数就减、如果之后是偶数就加” 两步，我们恰好把 `even_sum` 调整到最新的正确值。  

**类比**：想象你在一本账本里记录所有偶数金额的合计。每次只有一笔金额会变动，你只需要把这笔金额原先的贡献（如果是偶数）删掉，然后把新的贡献（如果是偶数）加上，账本的总额立刻更新，无需重新把所有金额重新相加。

#### 代码（Python）

```python
from typing import List

def sumEvenAfterQueries(nums: List[int], queries: List[List[int]]) -> List[int]:
    """
    最优解：维护当前偶数和，只在被修改的元素上做增量更新。
    """
    # 1️⃣ 先算一次初始的偶数和
    even_sum = sum(x for x in nums if x % 2 == 0)

    ans = []                     # 用来保存每次查询的结果
    for val, idx in queries:     # 依次处理每条查询
        old = nums[idx]          # 记录修改前的值

        # 2️⃣ 如果 old 是偶数，先把它的贡献减掉
        if old % 2 == 0:
            even_sum -= old

        # 3️⃣ 执行查询的加法操作
        nums[idx] = old + val
        new = nums[idx]          # 更新后的新值

        # 4️⃣ 如果 new 是偶数，再把它的贡献加回来
        if new % 2 == 0:
            even_sum += new

        # 5️⃣ 当前 even_sum 已经是本次查询的答案
        ans.append(even_sum)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - **含义**：第一次遍历 `nums` 用 `O(n)`，随后每条查询只做常数次操作，用 `O(m)`。如果 `n = m = 10⁴`，总共只有约 2×10⁴ 次基本操作，几乎是瞬间完成。  
  - 与暴力解相比，时间从 `O(m·n)` 降到了线性级别，提升非常明显。  

- **空间复杂度**：`O(1)`（不计答案数组）  
  - **含义**：只用了几个整数变量 `even_sum、old、new`，不随输入规模增长。

---

## 心得

- **核心技巧**：**维护增量信息**（这里是偶数和），把全局计算拆解为局部的“加/减”。  
- **适用的题型**  
  1. “数组元素更新后求某类元素的统计值”——如求奇数和、求最大值、求出现次数最多的元素等。  
  2. “区间更新后查询”——如前缀和、差分数组等技巧的变形。  
  3. “滑动窗口”类问题——窗口内部只会有少量元素变化，也可以用类似的增量维护。  

- **一句话总结**：**“只在变化的地方做改动，别每次都从头算”。**  

---

## 反思

- **第一反应**：看到“每次查询后打印偶数和”，自然想到遍历数组求和——这就是暴力解。  
- **最容易踩的坑**  
  1. **忘记在旧值是偶数时先减去**，导致 `even_sum` 重复计入旧值。  
  2. **负数也可能是偶数**（如 `-2`），判断奇偶时只能靠 `% 2 == 0`，不要误以为只能是正数。  
  3. **下标越界**：一定要确保 `indexi` 在 `[0, len(nums)-1]` 范围内（题目已保证，但写代码时仍要小心）。  

- **下次遇到同类题**：第一步先思考“有没有可以预先算好的全局信息”，再判断“每次操作只会影响哪些局部”，从而决定是否可以 **增量更新**。这样往往能把时间复杂度从平方级别降到线性甚至更低。