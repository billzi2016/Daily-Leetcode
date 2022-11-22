# #2023. 连接等于目标的字符串对数 / Number of Pairs of Strings With Concatenation Equal to Target

> 难度：中等 · 标签：Array、Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/number-of-pairs-of-strings-with-concatenation-equal-to-target/)

---

## 题目（英文原版）

**Description**

Given an array of digit strings nums and a digit string target, return the number of pairs of indices (i, j) (where i != j) such that the concatenation of nums[i] + nums[j] equals target.

**Examples**

**Example 1:**

```
Input: nums = ["777","7","77","77"], target = "7777"
Output: 4
Explanation: Valid pairs are:
- (0, 1): "777" + "7"
- (1, 0): "7" + "777"
- (2, 3): "77" + "77"
- (3, 2): "77" + "77"
```

**Example 2:**

```
Input: nums = ["123","4","12","34"], target = "1234"
Output: 2
Explanation: Valid pairs are:
- (0, 1): "123" + "4"
- (2, 3): "12" + "34"
```

**Example 3:**

```
Input: nums = ["1","1","1"], target = "11"
Output: 6
Explanation: Valid pairs are:
- (0, 1): "1" + "1"
- (1, 0): "1" + "1"
- (0, 2): "1" + "1"
- (2, 0): "1" + "1"
- (1, 2): "1" + "1"
- (2, 1): "1" + "1"
```

**Constraints**

- 2 <= nums.length <= 100
- 1 <= nums[i].length <= 100
- 2 <= target.length <= 100
- nums[i] and target consist of digits.
- nums[i] and target do not have leading zeros.

---

## 题目（中文翻译）

**描述**  
给定一个字符串数组 `nums`（每个元素都是仅包含数字的字符串）和一个目标字符串 `target`，返回满足以下条件的下标对 `(i, j)` 的数量（其中 `i != j`）：

- 将 `nums[i]` 与 `nums[j]` 连接（concatenation）后得到的字符串等于 `target`。

**示例**  

**示例 1**  
```text
Input: nums = ["777","7","77","77"], target = "7777"
Output: 4
Explanation: 有效的下标对为：
- (0, 1): "777" + "7"
- (1, 0): "7" + "777"
- (2, 3): "77" + "77"
- (3, 2): "77" + "77"
```

**示例 2**  
```text
Input: nums = ["123","4","12","34"], target = "1234"
Output: 2
Explanation: 有效的下标对为：
- (0, 1): "123" + "4"
- (2, 3): "12" + "34"
```

**示例 3**  
```text
Input: nums = ["1","1","1"], target = "11"
Output: 6
Explanation: 有效的下标对为：
- (0, 1): "1" + "1"
- (1, 0): "1" + "1"
- (0, 2): "1" + "1"
- (2, 0): "1" + "1"
- (1, 2): "1" + "1"
- (2, 1): "1" + "1"
```

**约束条件**  
- `2 <= nums.length <= 100`
- `1 <= nums[i].length <= 100`
- `2 <= target.length <= 100`
- `nums[i]` 与 `target` 只包含数字字符。
- `nums[i]` 与 `target` 不含前导零。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把数组里每两个**不同**的下标 `i`、`j` 挑出来，直接把 `nums[i]` 与 `nums[j]` 用 `+` 拼接成一个新字符串，判断它是否恰好等于 `target`。  

- **用到的数据结构**：只需要一个普通的 Python `list`（数组），因为我们只在循环里取元素，不需要额外的映射或堆。  
- **生活化类比**：把每个字符串想象成一本书的章节标题，暴力解相当于把每两本书的章节标题依次粘在一起，看看拼好的标题是否正好是我们想要的那本“大书”。  
- **为什么一定正确**：我们遍历了 **所有** 合法的 `(i, j)`（i 与 j 必须不同），只要有一对满足 `nums[i] + nums[j] == target`，就会被计数；没有遗漏也没有多计。  

#### 代码（Python）

```python
from typing import List

def num_of_pairs_bruteforce(nums: List[str], target: str) -> int:
    n = len(nums)
    ans = 0
    # 双层循环，枚举所有 i != j 的组合
    for i in range(n):
        for j in range(n):
            if i == j:                 # 不能自己和自己配对
                continue
            # 把两个字符串拼接
            if nums[i] + nums[j] == target:
                ans += 1               # 找到一组合法配对
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n² * L)`，其中 `n = len(nums)`，`L` 是字符串拼接/比较的平均长度。  
  - “O(n²)” 可以想象成「如果有 100 本书，最多要检查 100×100 = 10,000 次配对」；  
  - 乘上的 `L` 表示每次比较要看几位数字，最坏情况是 100 位，所以整体仍然在可接受范围（`n ≤ 100`）。
- **空间复杂度**：`O(1)`，只用了常数个额外变量 `ans、i、j`，不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **两层循环**——我们把每一对都尝试一次，实际上大多数配对根本不可能等于 `target`，因为它们的前缀或后缀根本不匹配。  
我们可以把目标字符串 `target` 看成 **左半部分 + 右半部分**，然后统计每个字符串在数组中出现的次数。  

**关键观察**：

1. 若 `nums[i]` 能作为左边的部分，则它必须是 `target` 的 **前缀**（即 `target.startswith(nums[i])`）。
2. 对于这样的左边字符串 `left = nums[i]`，右边应该是 `right = target[len(left):]`（去掉左边后剩下的子串）。
3. 只要数组里有 `right`（不论是同一个下标还是别的下标），就可以形成合法配对。  
4. 计数时要注意 `i != j` 的限制：如果 `left` 与 `right` 完全相同，则配对的下标必须不同，计数方式要特殊处理。

**实现步骤**：

- 第一步，用 **哈希表**（Python `dict`）统计每个字符串出现的次数。  
  - 哈希表就像一本“字典”，键是字符串，值是它出现的次数，查找 `O(1)`，非常快。  
- 第二步，遍历字典的每个键 `left`（只遍历一次），判断它是否是 `target` 的前缀。  
- 若是前缀，计算对应的 `right`。  
- 查看 `right` 是否也在字典里：  
  - 若 `left != right`，配对数 = `cnt[left] * cnt[right]`（左边可以选任意出现的下标，右边同理）。  
  - 若 `left == right`，配对数 = `cnt[left] * (cnt[left] - 1)`，因为下标必须不同，等价于从 `cnt` 个下标中选出有序的两个（先选 i 再选 j）。  

**为什么只遍历一次就能得到所有有序对**：

因为我们把“左边”固定为 `left`，而右边自然只能是 `right = target[len(left):]`，这一步唯一确定。于是所有满足条件的 `(i, j)` 都被计入。

#### 代码（Python）

```python
from typing import List
from collections import Counter

def num_of_pairs_opt(nums: List[str], target: str) -> int:
    # 1️⃣ 统计每个字符串出现次数，等价于“字典”
    freq = Counter(nums)          # 例如 {"77":2, "7":1, "777":1}
    ans = 0

    # 2️⃣ 枚举所有可能的左边字符串（只遍历字典的键，避免重复计算）
    for left, cnt_left in freq.items():
        # left 必须是 target 的前缀
        if not target.startswith(left):
            continue               # 不是前缀直接跳过，省下很多无用比较

        # 右边应该是 target 剩余的部分
        right = target[len(left):]

        # right 可能根本不存在于 nums 中
        cnt_right = freq.get(right, 0)
        if cnt_right == 0:
            continue               # 没有对应的右边，配对数为 0

        if left == right:
            # 左右相同，下标必须不同，等价于从 cnt_left 个位置中选有序的两个
            ans += cnt_left * (cnt_left - 1)
        else:
            # 左右不同，左边可以选 cnt_left 种，右边可以选 cnt_right 种
            ans += cnt_left * cnt_right

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * L)`  
  - 统计次数 `Counter(nums)` 需要遍历一次数组，`O(n)`（每个字符串的哈希算子本身要看字符串长度 `L`）。  
  - 枚举字典的键最多也是 `n` 个，每次只做 `startswith`（最多检查 `L` 位）和一次哈希查表 `O(1)`。  
  - 与暴力的 `O(n²)` 相比，省去了大量无效配对的检查，尤其当 `n` 较大时差距明显。  
- **空间复杂度**：`O(n)`  
  - 需要额外存储哈希表 `freq`，最坏情况下每个字符串都不相同，需要 `n` 条记录。  

---

## 心得

- **核心技巧**：利用 **哈希表 + 前缀匹配** 把“枚举所有配对”转化为“枚举左边字符串”，从而把二次循环降到一次循环。  
- **适用的题型**  
  1. **两个子串拼接等于目标**（本题）。  
  2. **两数之和的字符串版**：给定字符串数组和目标字符串，找出两个不同下标的字符串拼接等于目标。  
  3. **前后缀计数**：统计数组中有多少对字符串，使得一个是另一个的前缀（或后缀）。  
- **一句话总结解题钥匙**：**把目标拆成「左」+「右」两段，只统计出现次数，用乘法计数有序配对**。

---

## 反思

- **第一反应**：直接双层循环尝试所有配对（暴力），因为最安全、最容易写。  
- **最容易踩的坑**  
  - 忘记 `i != j` 的限制，导致同一个下标配对自己，尤其在 `left == right` 时容易出错。  
  - `target` 可能比某个 `nums[i]` 长很多，需要先判断 `left` 是否是前缀，否则会产生错误的 `right`（空串或不在数组里）。  
  - 字符串没有前导零的约束不影响实现，但要注意不要在拼接时产生多余的 “0”。  
- **下次类似题的第一步**：**先把目标拆成两段，检查每段在原数组中出现的次数**，再利用计数公式求答案。这样可以快速判断是否需要进一步优化或直接用哈希表求解。