# #3483. **唯一的三位偶数** / Unique 3-Digit Even Numbers

> 难度：简单 · 标签：Array、Hash Table、Recursion、Enumeration · [LeetCode 链接](https://leetcode.com/problems/unique-3-digit-even-numbers/)

---

## 题目（英文原版）

**Description**

You are given an array of digits called digits. Your task is to determine the number of distinct three-digit even numbers that can be formed using these digits.
Note: Each copy of a digit can only be used once per number, and there may not be leading zeros.

**Examples**

**Example 1:**

```
Input: digits = [1,2,3,4]
Output: 12
Explanation: The 12 distinct 3-digit even numbers that can be formed are 124, 132, 134, 142, 214, 234, 312, 314, 324, 342, 412, and 432. Note that 222 cannot be formed because there is only 1 copy of the digit 2.
```

**Example 2:**

```
Input: digits = [0,2,2]
Output: 2
Explanation: The only 3-digit even numbers that can be formed are 202 and 220. Note that the digit 2 can be used twice because it appears twice in the array.
```

**Example 3:**

```
Input: digits = [6,6,6]
Output: 1
Explanation: Only 666 can be formed.
```

**Example 4:**

```
Input: digits = [1,3,5]
Output: 0
Explanation: No even 3-digit numbers can be formed.
```

**Constraints**

- 3 <= digits.length <= 10
- 0 <= digits[i] <= 9

---

## 题目（中文翻译）

给定一个整数数组 `digits`，求可以使用这些数字组成的、互不相同的三位偶数的数量。

- 每个数字的每个拷贝在同一个数中只能使用一次；
- 组成的数不能有前导零（leading zeros）。

**示例 1**

```text
Input: digits = [1,2,3,4]
Output: 12
Explanation: 可以组成的 12 个不同的三位偶数为 124, 132, 134, 142, 214, 234, 312, 314, 324, 342, 412, 432。注意 222 不能构成，因为数组中只有一个 2。
```

**示例 2**

```text
Input: digits = [0,2,2]
Output: 2
Explanation: 唯一可以组成的三位偶数是 202 和 220。由于数组中有两个 2，数字 2 可以使用两次。
```

**示例 3**

```text
Input: digits = [6,6,6]
Output: 1
Explanation: 只能组成 666。
```

**示例 4**

```text
Input: digits = [1,3,5]
Output: 0
Explanation: 没有偶数可以组成三位数。
```

**约束条件**

- `3 <= digits.length <= 10`
- `0 <= digits[i] <= 9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的 3 位数** 都枚举出来，逐个检查它们是否符合题目要求。  
- 我们可以把 `digits` 看成一盒子里的数字，每个数字只能取一次（类似于抽牌，抽走的牌不能再用）。  
- 用 Python 的 `itertools.permutations` 可以一次性生成“从这盒子里抽出 3 张牌，排成顺序”的所有可能。  
- 对每个排列 `(a, b, c)`，只要满足三条条件就算合法：  
  1. `a != 0`（首位不能是 0，避免出现前导零）。  
  2. `c` 为偶数（`c % 2 == 0`），因为题目要求是偶数。  
  3. 这三个数字本身已经保证了“每个数字只能用一次”，因为 `permutations` 本身不允许重复取同一个下标。  

把所有合法的三位数放进集合 `set`，最后集合的大小就是答案——集合天然去重，防止像 `[2,2,2]` 这种只能组成 **666** 但会出现多次的情况。

> **为什么这方法一定能对？**  
> 枚举的范围覆盖了 **所有** 长度为 3、顺序不重复的取法，随后只筛掉不符合条件的取法，所以剩下的必然是全部合法解。

> **时间/空间复杂度大概是啥意思？**  
> - `O(n³)`：如果 `n` 是数组长度（最多 10），枚举所有 3‑位排列大概是 `n × (n-1) × (n-2)`，相当于“立方级”增长。  
> - `O(1)`（不算返回值）：我们只用常数级别的额外空间——一个集合最多装 `10P3 = 720` 个整数，和 `n` 的大小无关。

#### 代码（Python）

```python
from itertools import permutations
from typing import List

def countEvenNumbers_bruteforce(digits: List[int]) -> int:
    # 用集合自动去重
    unique_numbers = set()

    # 生成所有长度为 3、下标不重复的排列
    for a, b, c in permutations(digits, 3):
        # 1) 首位不能为 0
        if a == 0:
            continue
        # 2) 必须是偶数，即个位是偶数
        if c % 2 != 0:
            continue
        # 3) 组成整数
        number = a * 100 + b * 10 + c
        unique_numbers.add(number)   # 集合会自动去掉重复的数字

    # 集合的大小就是不同的合法三位偶数个数
    return len(unique_numbers)
```

#### 复杂度  

- **时间复杂度：** `O(n³)`  
  - 对于每个 `n`（最多 10），我们要遍历所有 `n·(n‑1)·(n‑2)` 种排列。  
  - 立方级别的意思是：如果把 `n` 从 5 增大到 10，枚举次数会从约 60 增加到约 720，增长得相对快。  

- **空间复杂度：** `O(1)`（不计返回的集合）  
  - 只用了常数个额外变量；即使把所有结果存进集合，最多也只有 720 个整数，和 `n` 的大小无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举所有排列**，虽然数据规模小（`n ≤ 10`），但我们可以把枚举过程压缩成 **计数**，只遍历一次数组就能算出答案。

观察三位数的结构：`[hundreds][tens][units]`  

1. **个位（units）** 必须是偶数。我们先挑一个偶数作为个位。  
2. **百位（hundreds）** 不能是 0，且必须和已经选的个位不同（如果该数字只出现一次的话）。  
3. **十位（tens）** 可以是剩下的任何数字（包括 0），只要还有剩余的拷贝。

因此，只要知道每个数字在 `digits` 中出现了多少次，就可以**按数量直接计算**有多少合法组合，而不必真的把每个组合写出来。

**步骤**  

- 用长度为 10 的数组 `cnt[0..9]` 统计每个数字出现的次数（相当于“字典查词典，key 是数字，value 是出现次数”）。  
- 对每个可能的 **偶数** `e`（0、2、4、6、8），如果 `cnt[e] == 0` 则跳过。否则把 `cnt[e]` 减 1，表示这个偶数已经被占用为个位。  
- 再遍历所有 **非零** 的数字 `h`（1~9），如果 `cnt[h] == 0` 则跳过。否则把 `cnt[h]` 减 1，表示它被占为百位。  
- 此时剩下的数字（包括 0）中，只要还有至少一个拷贝，就可以放在十位。十位的选择数目等于**剩余所有拷贝的总和**。把这个数目加到答案中。  
- 最后记得把刚才减掉的 `cnt[h]`、`cnt[e]` 恢复（回溯），因为后面还要尝试别的组合。  

这其实是 **枚举两层**（个位、百位），十位直接用计数求和，时间从 `O(n³)` 降到 `O(10·10) = O(1)`——因为数字只有 0~9，遍历的次数是常数。

> **核心技巧**：先把“每个数字能用多少次”记录下来（哈希表/计数数组），然后在组合时**按需扣减**，再**恢复**，这样既保证不超用，也能快速统计。  

> **类比**：想象你有若干种颜色的积木，每种颜色的数量已知。要搭建一个三层塔，底层必须是非零颜色，顶层必须是偶数颜色。你先挑顶层的颜色，扣掉一块；再挑底层颜色，扣掉一块；最后剩下的任意颜色都可以放中间层，直接把剩余块数相加，就是所有可能的塔的数目。

#### 代码（Python）

```python
from typing import List

def countEvenNumbers_optimal(digits: List[int]) -> int:
    # 1）统计每个数字出现的次数，cnt[i] 相当于“字典里 key=i 的值”
    cnt = [0] * 10
    for d in digits:
        cnt[d] += 1

    ans = 0

    # 2）枚举个位（必须是偶数）
    for unit in (0, 2, 4, 6, 8):
        if cnt[unit] == 0:               # 没有这个偶数，跳过
            continue
        cnt[unit] -= 1                    # 占用一次

        # 3）枚举百位（不能是 0，且必须还有剩余）
        for hundred in range(1, 10):      # 1~9
            if cnt[hundred] == 0:
                continue
            cnt[hundred] -= 1             # 占用一次

            # 4）十位可以是剩下的任何数字，直接把所有剩余拷贝加起来
            tens_choices = sum(cnt)       # 剩余数字的总数
            ans += tens_choices           # 每一种十位的选法对应一个合法三位数

            cnt[hundred] += 1             # 恢复百位的计数，准备尝试下一个 hundred

        cnt[unit] += 1                    # 恢复个位的计数，准备尝试下一个 unit

    return ans
```

#### 复杂度  

- **时间复杂度：** `O(1)`（常数级）  
  - 这里的 “常数” 指的是最多遍历 5（偶数）×9（非零百位）≈45 次内部循环，和输入规模 `n`（≤10）无关。相比暴力的 `O(n³)`，这就像把“跑 10 圈”变成了“一步到位”。  

- **空间复杂度：** `O(1)`  
  - 只用了长度为 10 的计数数组和几个整数变量，所需空间不随 `n` 增长。

---

## 心得  

- **核心技巧**：**计数 + 逐位枚举**。先统计每个数字出现的次数，再按位（个位、百位）逐个尝试，剩余的位直接用计数求和。  
- **适用的题型**（类似思路）：  
  1. “不同的三位数/四位数/… 能否形成”——需要控制每个数字的使用次数。  
  2. “使用数组中的数字组成满足某种属性的数”——如“不同的回文数”“不同的可被 3 整除的数”。  
  3. “从字符数组中挑选满足特定位置要求的字符串”——比如固定首尾字符的排列计数。  
- **一句话总结解题钥匙**：**先把资源（每个数字的数量）列出来，再按位“拿走—还回”地枚举，最后用剩余资源直接计数。**

---

## 反思  

- **第一反应**：直接想到“把所有 3 位排列枚举出来”。这在脑海里最直接、最不容易出错。  
- **最容易踩的坑**：  
  - **前导零**：忘记排除百位为 0 的情况，会多算非法数。  
  - **数字重复使用**：若直接用 `set(permutations)`，会因为原数组里有重复元素导致同一个数字被算多次，需要在计数时正确扣除。  
  - **偶数判断**：只检查个位是否为偶数，别把整个数取模。  
- **下次遇到同类题**，第一步应该想到**“先统计每个元素出现多少次”，再在此基础上按位枚举/组合**，这样可以把枚举空间从指数级压到常数级。