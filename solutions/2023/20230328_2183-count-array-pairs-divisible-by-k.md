# #2183. 计数可被 K 整除的数组下标对 / Count Array Pairs Divisible by K

> 难度：困难 · 标签：Array、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/count-array-pairs-divisible-by-k/)

---

## 题目（英文原版）

**Description**

Given a 0-indexed integer array nums of length n and an integer k, return the number of pairs (i, j) such that:

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5], k = 2
Output: 7
Explanation: 
The 7 pairs of indices whose corresponding products are divisible by 2 are
(0, 1), (0, 3), (1, 2), (1, 3), (1, 4), (2, 3), and (3, 4).
Their products are 2, 4, 6, 8, 10, 12, and 20 respectively.
Other pairs such as (0, 2) and (2, 4) have products 3 and 15 respectively, which are not divisible by 2.
```

**Example 2:**

```
Input: nums = [1,2,3,4], k = 5
Output: 0
Explanation: There does not exist any pair of indices whose corresponding product is divisible by 5.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i], k <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的整数数组 `nums`（长度为 `n`）和一个整数 `k`，返回满足以下条件的下标对 `(i, j)` 的数量：

- `0 ≤ i < j < n`  
- `nums[i] * nums[j]` 能被 `k` 整除（即 `nums[i] * nums[j] % k == 0`）

---

**约束条件**  

- `1 <= nums.length <= 10^5`  
- `1 <= nums[i], k <= 10^5`

---

**示例**

**示例 1**  
```
输入: nums = [1,2,3,4,5], k = 2
输出: 7
解释: 
能够使对应乘积能被 2 整除的 7 对下标为
(0, 1), (0, 3), (1, 2), (1, 3), (1, 4), (2, 3), 和 (3, 4)。
它们的乘积分别是 2, 4, 6, 8, 10, 12, 和 20。
其他如 (0, 2) 与 (2, 4) 的乘积分别为 3 和 15，不能被 2 整除。
```

**示例 2**  
```
输入: nums = [1,2,3,4], k = 5
输出: 0
解释: 不存在任意下标对使得对应乘积能被 5 整除。
```

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「枚举所有下标对」`(i, j)`（`i < j`），把对应的两个数相乘后检查是否能被 `k` 整除。  

- **使用的数据结构**：只需要一个普通的 Python 列表 `nums`，遍历时用两个循环的索引 `i`、`j`。  
- **生活化类比**：把数组想成一排排商品，暴力解就像把每两件商品都拿出来称重，看它们的总重量（这里是乘积）能不能被某个固定的「秤砣」`k` 整除。  
- **为什么正确**：因为我们把**所有可能的**配对都检查了一遍，只要配对满足「乘积 % k == 0」就计数，所以不会漏掉任何合法的 `(i, j)`。  

#### 代码（Python）

```python
from typing import List

def countPairs_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 0
    # 外层循环固定左边的下标 i
    for i in range(n):
        # 内层循环遍历 i 右边的所有下标 j
        for j in range(i + 1, n):
            # 如果两个数的乘积能被 k 整除，就计数
            if (nums[i] * nums[j]) % k == 0:
                ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：我们用了两层循环，第一层跑 `n` 次，第二层平均跑 `n/2` 次，总共大约 `n·(n‑1)/2` 次乘法和取模。  
  - 对于 `n = 10⁵`（题目最大规模），`n²` 已经是 `10¹⁰`，在电脑上几乎不可能在合理时间内跑完。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量 `ans、i、j`，不随 `n` 增长。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都要遍历所有右侧元素**，导致二次方的时间。我们需要利用数学性质，把配对的判断转化为**只看单个元素的特征**，再用哈希表（字典）快速统计。

**关键观察**  

- 对于任意 `a = nums[i]`，要让 `a * b` 能被 `k` 整除，`b` 必须包含 `k` 中缺少的那部分因子。  
- 设 `g = gcd(a, k)`（`g` 是 `a` 与 `k` 的最大公约数），则 `a` 已经贡献了 `g` 的所有因子。  
- 为了让乘积被 `k` 整除，还需要再乘上 `k / g`（**最小的** 能补齐缺口的数）。记 `need = k // g`。  

> **类比**：想象 `k` 是一道完整的拼图，`a` 已经拼好了一块（`g`），我们还缺的那块就是 `need`。只要把缺的这块（或它的倍数）和 `a` 配对，整体就能拼成完整的图。

因此，遍历数组时：

1. 计算当前元素 `a` 的 `need = k // gcd(a, k)`。  
2. 看在**已经遍历过的元素**中，有多少个数的**余数**恰好等于 `need`（或者说，这些数的 `need` 正好是当前 `a`）。  
3. 用一个字典 `cnt` 记录 **每个已经出现的数的 `need`** 出现的次数。  

具体做法：

- 先遍历 **右侧**（从左到右），对每个 `a = nums[i]`，先把它对应的 `need` 加入字典 `cnt`，表示以后左侧的数可以和它配对。  
- 再遍历 **左侧**（从左到右），对每个 `a`，直接查询字典中 `cnt[a]`（即已有的右侧元素的 `need` 是否等于当前 `a`），把计数加到答案中，然后把当前 `a` 的 `need` 从字典里减去（因为它已经不再是“右侧”了）。  

这样每个元素只被处理了 **两次**（一次放入计数，一次查询），时间是线性的。

**核心数据结构**：Python 的 `defaultdict(int)`，相当于「查字典」：key 是数值，value 是出现次数。  

#### 代码（Python）

```python
from math import gcd
from collections import defaultdict
from typing import List

def countPairs(nums: List[int], k: int) -> int:
    """
    返回满足 nums[i] * nums[j] 能被 k 整除的下标对数量 (i < j)。
    """
    n = len(nums)
    # cnt[x] 表示「在右侧」出现过、其 need 等于 x 的元素个数
    cnt = defaultdict(int)

    # 先把所有元素的 need 加入 cnt，等价于把它们全部当作右侧元素
    for x in nums:
        need = k // gcd(x, k)          # 需要的配对数
        cnt[need] += 1

    ans = 0
    # 从左到右遍历，每次把当前元素从「右侧」移到「左侧」
    for x in nums:
        # 当前元素已经不再是右侧，先把对应的 need 数量减 1
        cur_need = k // gcd(x, k)
        cnt[cur_need] -= 1

        # 现在左侧的 x 可以和右侧那些 need == x 的元素配对
        ans += cnt[x]                  # cnt[x] 记录了满足 need == x 的右侧元素个数

    return ans
```

**代码要点解释**  

- `gcd(x, k)`：求最大公约数，帮助我们找出 `x` 已经贡献了哪些因子。  
- `need = k // gcd(x, k)`：`k` 除以已经拥有的因子，得到最小的「补齐」数。  
- `cnt[need] += 1`：把每个元素的 `need` 计数，表示它可以和 `need` 本身配对。  
- `cnt[cur_need] -= 1`：当前元素不再是右侧，防止自己和自己配对。  
- `ans += cnt[x]`：查询有多少右侧元素的 `need` 正好等于当前左侧的值 `x`，这些就是合法配对。

#### 复杂度  

- **时间复杂度**：`O(n · log max(nums[i], k))`  
  - 解释：我们遍历了 `n` 次，每次只做了常数次的 `gcd`（欧几里得算法的时间是对数级别）和字典操作，整体是线性时间。相比暴力的 `O(n²)`，快了几个数量级。  
- **空间复杂度**：`O(n)`（最坏情况）  
  - 解释：字典 `cnt` 最多会保存每个元素对应的 `need`，在极端情况下所有 `need` 都不同，需要 `n` 条记录。对于 `n ≤ 10⁵`，这在内存里是完全可以接受的。

---

## 心得  

- **核心技巧**：利用 `gcd` 把「乘积能被 k 整除」的条件转化为「两个数的 `need` 互为对方的值」的配对问题。  
- **适用的题型**：  
  1. **数对满足乘积可被某数整除**（本题）。  
  2. **数对满足和或差能被某数整除**（如 LeetCode 1542. 通过一次交换使数组平衡）。  
  3. **数对满足特定的模运算关系**（如 LeetCode 1492. 统计好子数组的数目）。  
- **一句话总结解题钥匙**：把「乘积能被 k」拆解为「每个数缺少的因子」——用 `need = k / gcd(num, k)` 把配对条件变成「左数 = 右数的 need」。

---

## 反思  

- **第一反应**：直接想到「两层循环枚举」，因为乘积的可除性看起来只能在配对时才判断。  
- **最容易踩的坑**：  
  - 忘记在遍历时把当前元素从右侧计数中减掉，导致 **自配对**（i = j）被错误计入。  
  - `k` 与 `num` 的最大公约数为 `0` 的情况不存在，但如果写成 `k // gcd` 时忘记整数除法，容易产生浮点数导致字典键不匹配。  
  - 边界值 `k = 1`：此时所有配对都合法，算法仍然正确，因为 `gcd(num,1)=1`，`need = 1`，所有数的 `need` 都是 `1`，计数逻辑仍然成立。  
- **下次遇到同类题**：第一步先**思考能否把两数之间的约束拆成每个数的“需求”**（如 `need = k / gcd`），然后用哈希表统计需求出现次数，避免暴力枚举。