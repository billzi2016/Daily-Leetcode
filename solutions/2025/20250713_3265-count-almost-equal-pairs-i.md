# #3265. **Count Almost Equal Pairs I** / Count Almost Equal Pairs I

> 难度：中等 · 标签：Array、Hash Table、Sorting、Counting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/count-almost-equal-pairs-i/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of positive integers.
We call two integers x and y in this problem almost equal if both integers can become equal after performing the following operation at most once:
Return the number of indices i and j in nums where i < j such that nums[i] and nums[j] are almost equal.
Note that it is allowed for an integer to have leading zeros after performing an operation.

**Examples**

**Example 1:**

```
Input: nums = [3,12,30,17,21]
Output: 2
Explanation:
The almost equal pairs of elements are:
```

**Example 2:**

```
Input: nums = [1,1,1,1,1]
Output: 10
Explanation:
Every two elements in the array are almost equal.
```

**Example 3:**

```
Input: nums = [123,231]
Output: 0
Explanation:
We cannot swap any two digits of 123 or 231 to reach the other.
```

**Constraints**

- 2 <= nums.length <= 100
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个只包含正整数的数组 `nums`。我们称两个整数 `x` 和 `y` 在本题中**几乎相等**（almost equal），如果对其中的任意一个整数至多执行一次下列操作后，两者可以变得相等：

- 在该整数的十进制表示中**交换任意两个数字**（swap）。

在执行操作时，整数可以出现前导零（例如将 `3` 看作 `03` 再交换得到 `30`）。

返回满足 `i < j` 且 `nums[i]` 与 `nums[j]` **几乎相等** 的下标对 `(i, j)` 的数量。

---

### 示例

**示例 1**  
输入: `nums = [3,12,30,17,21]`  
输出: `2`  
解释:  
几乎相等的元素对有两个：

- `3` 与 `30`：将 `3` 看作 `03`，交换 `0` 与 `3` 得到 `30`。  
- `12` 与 `21`：直接交换 `1` 与 `2`。

**示例 2**  
输入: `nums = [1,1,1,1,1]`  
输出: `10`  
解释:  
数组中的任意两个元素都已经相等（无需任何交换），因此全部 `C(5,2)=10` 对均满足条件。

**示例 3**  
输入: `nums = [123,231]`  
输出: `0`  
解释:  
无论对 `123` 或 `231` 进行一次数字交换，都无法得到另一个数，因此不存在符合条件的下标对。

---

### 约束条件

- `2 <= nums.length <= 100`
- `1 <= nums[i] <= 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**枚举所有下标对 (i, j)**，对每一对检查 `nums[i]` 能否通过**至多一次**的“交换任意两位数字”操作变成 `nums[j]`，或者 `nums[j]` 变成 `nums[i]`，甚至两者都各换一次得到同一个数。  

- **数据结构**：只需要普通的整数和字符串。把整数转成字符数组（相当于把数字写在纸上），交换两位就像把纸上的两块拼图换位置。  
- **为什么正确**：因为我们把题目要求的“最多一次交换”全部穷举出来了：  
  1. 不交换（原数）。  
  2. 任意挑选两位交换一次。  
  对每一对 (i, j) 只要出现一种情况让两数相等，就算这是一组 **almost equal**。  
- **时间/空间复杂度**：  
  - 枚举下标对需要 `C(n,2) = n·(n‑1)/2` 次，n 最多 100，算得 **≈ O(n²)**。  
  - 对每一对，我们要把两个数的所有可能交换结果全部列出来再比较。设数字的位数为 `L`（`L ≤ 7`），一次交换有 `C(L,2)` 种可能，最多约 `21` 种，加上“不要交换”共 `≤ 22` 种。  
    - 暴力直接在每对上重新生成这 `22` 种并两两比较，最坏是 `22·22 ≈ 500` 次比较。  
    - 所以整体时间是 **O(n²·L²)**，在本题的约束下仍然可以跑完，但写起来会显得很臃肿。  
  - 只使用常数级的额外空间（几个临时字符串），**O(1)**。  

#### 代码（Python）  

```python
from itertools import combinations
from typing import List

def all_one_swap(num: int) -> List[int]:
    """返回 num 经过「至多一次」交换后可能得到的所有整数（包括原数）。"""
    s = list(str(num))                 # 把整数写成字符列表，方便交换
    res = {int(''.join(s))}            # 不交换的情况
    n = len(s)
    for i, j in combinations(range(n), 2):   # 任意两位 i<j
        s[i], s[j] = s[j], s[i]               # 交换
        res.add(int(''.join(s)))              # 加入新数，int() 会自动去掉前导零
        s[i], s[j] = s[j], s[i]               # 换回，准备下次交换
    return list(res)

def count_almost_equal_bruteforce(nums: List[int]) -> int:
    """暴力实现：直接对每一对枚举所有可能的交换结果并比较。"""
    n = len(nums)
    ans = 0
    for i in range(n):
        for j in range(i + 1, n):
            # 生成两数的所有可能（至多一次交换）
            cand_i = all_one_swap(nums[i])
            cand_j = all_one_swap(nums[j])
            # 只要有交集就算是一对
            if set(cand_i) & set(cand_j):
                ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²·L²)`  
  - `n²` 来自所有下标对，`L²`（最多 7²）来自每对内部的所有交换组合。  
  - 用大白话说，就是 **“先找所有小伙伴，再把每对的小伙伴都玩遍”**，虽然数字不大，但代码里有两层循环套两层循环。  
- **空间复杂度**：`O(1)`（不计返回值）  
  - 只用了几个临时列表和集合，和输入规模无关。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于对每一对重复生成相同的“可达数集合”**。  
同一个下标的数字在所有配对中出现很多次，却每次都重新算一遍它能变成哪些数，这是一种“重复劳动”。  

**优化思路**：  
1. **预处理**：遍历一次数组，为每个元素 **一次性** 生成它的所有 “至多一次交换” 能得到的数，保存为集合。  
   - 这一步的代价是 `O(n·L²)`，远小于 `O(n²·L²)`。  
2. **配对检查**：对每一对 (i, j) 只需要判断这两个集合是否有交集。  
   - 由于每个集合大小 ≤ 22，直接遍历较小的集合并用哈希表（Python `set`）在 O(1) 时间内查询即可。  
   - 整体配对检查的代价是 `O(n²·K)`，其中 `K ≤ 22`，可以视作常数，所以整体是 **O(n²)**。  

**核心数据结构**：**哈希集合（set）**。  
- 类比：像在字典里查词，`key` 是可能的数字，`value`（这里不需要）可以是出现的位置。只要能在字典里快速判断“这个数字我有没有见过”，就能立刻知道两数是否“almost equal”。  

**步骤图示（文字版）**：  

```
原数组 nums
   ↓ 预处理（每个数 → 可达集合）
[ {3,30}, {12,21}, {30,3}, {17}, {21,12} ]
   ↓ 配对遍历
(i=0,j=1) → {3,30} ∩ {12,21} = ∅   → 不计数
(i=0,j=2) → {3,30} ∩ {30,3} ≠ ∅   → +1
(i=1,j=4) → {12,21} ∩ {21,12} ≠ ∅ → +1
…
```

#### 代码（Python）  

```python
from itertools import combinations
from typing import List, Set

def generate_one_swap_set(num: int) -> Set[int]:
    """
    返回 num 经过至多一次交换后可能得到的所有整数集合。
    使用 set 自动去重，集合大小 ≤ 22（不交换 + 所有两位交换）。
    """
    s = list(str(num))
    n = len(s)
    reachable: Set[int] = {int(''.join(s))}   # 不交换的情况
    for i, j in combinations(range(n), 2):
        s[i], s[j] = s[j], s[i]               # 交换
        reachable.add(int(''.join(s)))       # 加入新数（int 会去掉前导零）
        s[i], s[j] = s[j], s[i]               # 恢复原状，继续下一对
    return reachable

def count_almost_equal(nums: List[int]) -> int:
    """最优实现：预处理 + 集合交集检查，时间 O(n²)，空间 O(n·L)。"""
    # 1️⃣ 预处理每个元素的可达集合
    reachable_list = [generate_one_swap_set(x) for x in nums]

    # 2️⃣ 配对检查是否有交集
    ans = 0
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            # 任选较小的集合遍历，提高常数因子
            if len(reachable_list[i]) > len(reachable_list[j]):
                small, big = reachable_list[j], reachable_list[i]
            else:
                small, big = reachable_list[i], reachable_list[j]

            # 检查是否存在公共元素
            for val in small:
                if val in big:      # O(1) 哈希查询
                    ans += 1
                    break           # 找到一个就足够，继续下一个 (i,j)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n·L² + n²·K)`，其中  
  - `L ≤ 7`（数字位数），`K ≤ 22`（每个集合的大小），均为常数。  
  - 简化后就是 **O(n²)**，即 **“先把每个人的所有可能装进背包，再两两快速比对”**。  
  - 与暴力的 `O(n²·L²)` 相比，去掉了每对内部的二次枚举，跑得更快、更省事。  
- **空间复杂度**：`O(n·K)` ≈ `O(n)`  
  - 需要保存每个数的可达集合，总共至多 `n·22` 个整数，随 n 线性增长。  

---  

## 心得  

- **核心技巧**：**预处理 + 哈希集合交集**。先把每个元素的所有“变形”一次性算好，再利用集合的 O(1) 查找特性快速判断两数是否能相等。  
- **适用场景**（类似题目）：  
  1. “Count Almost Equal Pairs II”——允许 **两次** 交换或其他限制，仍可先枚举所有可能的变形。  
  2. “Number of Pairs of Strings With Same Frequency”——把每个字符串的字符频率预处理成哈希表，再配对比较。  
  3. “Pairs of Numbers With Same Digit Multiset”——把每个数的数字集合（或排序后字符串）预处理后配对。  
- **一句话总结**：**把“每次都重新算”改成“算一次、保存下来”，用集合的快速查找把配对检查降到常数时间。**  

---  

## 反思  

- **第一反应**：看到“至多一次交换”立刻想到枚举所有下标对并对每对暴力尝试所有交换。  
- **最容易踩的坑**：  
  - **位数不统一**：如 `3` 与 `30`，交换后可能产生前导零（`03`），转回整数时要记得 `int('03') == 3`，否则会误判。  
  - **重复计数**：同一对只计一次，若两个数都能通过不同的交换得到相同结果，仍然只算一次。  
  - **集合大小**：忘记把“原数”也加入集合，会漏掉本来已经相等的情况。  
- **下次遇到同类题**：第一步想到 **“把每个元素的所有合法状态预先列出来”，再用哈希/集合快速比较”。这样既能避免重复计算，又能保持代码简洁。