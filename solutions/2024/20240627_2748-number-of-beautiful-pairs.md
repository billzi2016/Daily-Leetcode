# #2748. 漂亮数对的数量 / Number of Beautiful Pairs

> 难度：简单 · 标签：Array、Hash Table、Math、Counting、Number Theory · [LeetCode 链接](https://leetcode.com/problems/number-of-beautiful-pairs/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. A pair of indices i, j where 0 <= i < j < nums.length is called beautiful if the first digit of nums[i] and the last digit of nums[j] are coprime.
Return the total number of beautiful pairs in nums.
Two integers x and y are coprime if there is no integer greater than 1 that divides both of them. In other words, x and y are coprime if gcd(x, y) == 1, where gcd(x, y) is the greatest common divisor of x and y.

**Examples**

**Example 1:**

```
Input: nums = [2,5,1,4]
Output: 5
Explanation: There are 5 beautiful pairs in nums:
When i = 0 and j = 1: the first digit of nums[0] is 2, and the last digit of nums[1] is 5. We can confirm that 2 and 5 are coprime, since gcd(2,5) == 1.
When i = 0 and j = 2: the first digit of nums[0] is 2, and the last digit of nums[2] is 1. Indeed, gcd(2,1) == 1.
When i = 1 and j = 2: the first digit of nums[1] is 5, and the last digit of nums[2] is 1. Indeed, gcd(5,1) == 1.
When i = 1 and j = 3: the first digit of nums[1] is 5, and the last digit of nums[3] is 4. Indeed, gcd(5,4) == 1.
When i = 2 and j = 3: the first digit of nums[2] is 1, and the last digit of nums[3] is 4. Indeed, gcd(1,4) == 1.
Thus, we return 5.
```

**Example 2:**

```
Input: nums = [11,21,12]
Output: 2
Explanation: There are 2 beautiful pairs:
When i = 0 and j = 1: the first digit of nums[0] is 1, and the last digit of nums[1] is 1. Indeed, gcd(1,1) == 1.
When i = 0 and j = 2: the first digit of nums[0] is 1, and the last digit of nums[2] is 2. Indeed, gcd(1,2) == 1.
Thus, we return 2.
```

**Constraints**

- 2 <= nums.length <= 100
- 1 <= nums[i] <= 9999
- nums[i] % 10 != 0

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`。若下标 `i`、`j` 满足 `0 <= i < j < nums.length`，且 `nums[i]` 的**首位数字**（first digit）与 `nums[j]` 的**末位数字**（last digit）互质（coprime），则称这对下标 `(i, j)` 为**漂亮数对**（beautiful pair）。  
返回数组 `nums` 中漂亮数对的总数。

**互质**（coprime）的定义：若不存在大于 **1** 的整数同时整除两个整数 `x` 与 `y`，则称 `x` 与 `y` 互质。等价地，`x` 与 `y` 互质当且仅当 `gcd(x, y) == 1`，其中 `gcd(x, y)` 为 `x` 与 `y` 的最大公约数（greatest common divisor）。

### 示例

**示例 1**

> 输入：`nums = [2,5,1,4]`  
> 输出：`5`  
> 解释：数组中共有 5 对漂亮数对：
> - 当 `i = 0, j = 1` 时：`nums[0]` 的首位数字是 **2**，`nums[1]` 的末位数字是 **5**，`gcd(2,5) == 1`，互质。
> - 当 `i = 0, j = 2` 时：`nums[0]` 的首位数字是 **2**，`nums[2]` 的末位数字是 **1**，`gcd(2,1) == 1`，互质。
> - 当 `i = 1, j = 2` 时：`nums[1]` 的首位数字是 **5**，`nums[2]` 的末位数字是 **1**，`gcd(5,1) == 1`，互质。（后续省略）

**示例 2**

> 输入：`nums = [11,21,12]`  
> 输出：`2`  
> 解释：数组中共有 2 对漂亮数对：
> - 当 `i = 0, j = 1` 时：`nums[0]` 的首位数字是 **1**，`nums[1]` 的末位数字是 **1**，`gcd(1,1) == 1`，互质。
> - 当 `i = 0, j = 2` 时：`nums[0]` 的首位数字是 **1**，`nums[2]` 的末位数字是 **2**，`gcd(1,2) == 1`，互质。

### 约束条件

- `2 <= nums.length <= 100`
- `1 <= nums[i] <= 9999`
- `nums[i] % 10 != 0`（即每个元素的末位数字不为 0）

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把所有满足条件的下标对 `(i, j)` 都枚举一遍。  

- **枚举方式**：双层循环，外层遍历 `i`，内层遍历 `j`（`j > i`），这样可以确保 `i < j`。  
- **获取首位和末位**：把整数转成字符串，`num[0]` 就是首位，`num[-1]` 就是末位。也可以用数学方式（循环除以 10），但对初学者来说字符串更直观。  
- **判断是否互质**：用欧几里得算法求最大公约数 `gcd(a, b)`，若结果是 `1`，说明两位数互质。  

> **类比**：哈希表就像字典，`key` 是词，`value` 是页码。这里我们不需要字典，只是把每个数字的“首位”当成 `key`、 “末位” 当成 `value` 来比较。

只要把每一对都检查一遍，就一定能得到答案——因为我们没有漏掉任何可能的 `(i, j)`。

#### 代码（Python）

```python
from math import gcd  # gcd 用来判断两数是否互质

def beautifulPairs(nums):
    n = len(nums)
    ans = 0                     # 统计满足条件的对数
    for i in range(n):         # 第一个下标 i
        # 取出 nums[i] 的首位
        first_i = int(str(nums[i])[0])
        for j in range(i + 1, n):   # 第二个下标 j，必须大于 i
            # 取出 nums[j] 的末位
            last_j = int(str(nums[j])[-1])
            # 判断首位和末位是否互质
            if gcd(first_i, last_j) == 1:
                ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - “平方”其实可以想象成：如果有 100 条数据，需要检查 100 × 99 / 2 ≈ 5 000 对。随着 `n` 增大，检查的对数会像 `n` 的平方那样快速增长。  
- **空间复杂度**：`O(1)`  
  - 只用了几个额外的整数变量，和输入规模无关。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每次都要遍历所有已经出现的 `i`**，导致 `O(n²)`。  
我们注意到：

1. **首位只可能是 1~9**（因为 `nums[i] ≥ 1`，且题目保证末位不为 0）。  
2. 对于固定的 `j`，只需要知道 **在它左边出现了多少个首位为 `d` 的数**，其中 `d` 与 `last_j` 互质。  

于是可以把 “已经出现的首位” 用一个长度为 10 的计数数组 `cnt_first[d]` 记录下来：

- 先遍历数组，从左到右把当前元素当作 **右端点 `j`**。  
- 用 `last_j` 去检查所有可能的 `d`（1~9），如果 `gcd(d, last_j) == 1`，就把 `cnt_first[d]` 加到答案里。  
- 然后把当前元素的 **首位** 加入计数数组，供后面的元素使用。

这样每个元素只处理常数次（最多遍历 9 个可能的首位），整体时间降到 **线性** `O(n)`。

> **欧几里得算法（gcd）回顾**：  
> 两数 `a, b`（`a ≥ b`），用 `a % b` 取余数 `r`，再把 `(b, r)` 当成新的一对，重复直到余数为 0，最后的 `b` 就是最大公约数。若最终得到 1，说明两数互质。

#### 代码（Python）

```python
from math import gcd

def beautifulPairs(nums):
    # cnt_first[d] 记录在当前遍历位置左侧，首位恰好为 d 的数字出现了多少次
    cnt_first = [0] * 10          # 下标 0 暂时不使用，只是占位
    ans = 0

    for num in nums:              # 依次把每个数当作右端点 j
        # 取出当前数的首位和末位
        s = str(num)
        first = int(s[0])
        last = int(s[-1])

        # 统计所有左侧 i 满足首位与当前末位互质的情况
        for d in range(1, 10):    # 只需要遍历 1~9
            if gcd(d, last) == 1:    # d 与 last 互质
                ans += cnt_first[d]  # 累加左侧所有首位为 d 的数量

        # 把当前数的首位计入，供后面的元素使用
        cnt_first[first] += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * 9) = O(n)`  
  - 对每个元素最多检查 9 次（因为首位只有 1~9），所以整体随 `n` 成线性增长。相比暴力的 `O(n²)`，大幅提升。  
- **空间复杂度**：`O(1)`  
  - 只用了长度为 10 的固定数组，和输入规模无关。

---

## 心得  

- **核心技巧**：利用 **计数数组 + 互质判断**，把“遍历所有左侧元素”压缩为“遍历固定的 9 种可能”。  
- **适用场景**：  
  1. 需要统计 **左侧出现的某类属性**（如首位、奇偶、模数等）对当前元素的贡献时。  
  2. 类似 “前缀计数 + 条件匹配” 的题目，如  
     - “统计数组中前缀和满足某个取模条件的子数组数”。  
     - “求数组中满足 `a[i] % k == a[j] % k` 且 `i < j` 的对数”。  
- **一句话总结**：**把有限的属性（这里是 1~9 的首位）提前计数，随后在遍历时直接查询，省去重复遍历。**

---

## 反思  

- **第一反应**：看到 “首位”和“末位”以及 “互质”，立刻想到把每个数的这两个属性抽出来，直接两层循环检查。  
- **最容易踩的坑**：  
  1. **末位为 0 的情况**：题目已经保证 `nums[i] % 10 != 0`，但如果忘记这点，`gcd(d, 0)` 会返回 `d`，导致错误计数。  
  2. **首位和末位的获取方式**：使用字符串时要记得把字符再转成整数；用数学方式时要循环除以 10 直到 `< 10`。  
  3. **计数顺序**：在最优解里，先统计左侧贡献再把当前首位加入计数，顺序反了会把 `(i, j)` 当成 `(j, i)`，导致错误。  
- **下次类似题的第一步**：  
  **先判断属性的取值范围是否有限**（如 0~9、0~k），若是，就考虑用 **计数数组/哈希表** 记录出现次数，随后在一次遍历中完成配对统计。这样往往能把 `O(n²)` 降到 `O(n)`。