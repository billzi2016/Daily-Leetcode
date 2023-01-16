# #2094. 寻找三位偶数 / Finding 3-Digit Even Numbers

> 难度：简单 · 标签：Array、Hash Table、Sorting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/finding-3-digit-even-numbers/)

---

## 题目（英文原版）

**Description**

You are given an integer array digits, where each element is a digit. The array may contain duplicates.
You need to find all the unique integers that follow the given requirements:
For example, if the given digits were [1, 2, 3], integers 132 and 312 follow the requirements.
Return a sorted array of the unique integers.

**Examples**

**Example 1:**

```
Input: digits = [2,1,3,0]
Output: [102,120,130,132,210,230,302,310,312,320]
Explanation: All the possible integers that follow the requirements are in the output array. 
Notice that there are no odd integers or integers with leading zeros.
```

**Example 2:**

```
Input: digits = [2,2,8,8,2]
Output: [222,228,282,288,822,828,882]
Explanation: The same digit can be used as many times as it appears in digits. 
In this example, the digit 8 is used twice each time in 288, 828, and 882.
```

**Example 3:**

```
Input: digits = [3,7,5]
Output: []
Explanation: No even integers can be formed using the given digits.
```

**Constraints**

- 3 <= digits.length <= 100
- 0 <= digits[i] <= 9

---

## 题目（中文翻译）

给定一个整数数组 `digits`，其中每个元素都是一个数字（0 ≤ digit ≤ 9），数组中可能包含重复的数字。  
请找出所有满足以下要求的 **唯一整数**：

1. 由 `digits` 中的 **三个不同下标的数字** 按顺序组成一个三位数；
2. 该三位数是偶数，即个位数字是偶数（0、2、4、6、8）；
3. 该三位数不能出现前导零（最高位不能为 0）；
4. 每个数字在构成某个整数时使用的次数不能超过它在 `digits` 中出现的次数。

返回这些唯一整数的 **升序**（从小到大）数组。

示例 1  
输入: `digits = [2,1,3,0]`  
输出: `[102,120,130,132,210,230,302,310,312,320]`  
解释: 所有满足要求的整数均在输出数组中。可以看到没有奇数，也没有以零开头的整数。

示例 2  
输入: `digits = [2,2,8,8,2]`  
输出: `[222,228,282,288,822,828,882]`  
解释: 同一个数字可以使用的次数最多与它在 `digits` 中出现的次数相同。例如数字 8 在数组中出现两次，因此在 `288`、`828`、`882` 中各使用两次。

示例 3  
输入: `digits = [3,7,5]`  
输出: `[]`  
解释: 使用给定的数字无法组成任何偶数。

**约束条件**

- 3 ≤ `digits.length` ≤ 100  
- 0 ≤ `digits[i]` ≤ 9

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把所有可能的三位数都枚举出来**，然后挑出满足条件的数。

1. **选三个位置**（百位、十位、个位），每个位置都可以从 `digits` 中挑一个数字。  
2. 由于 `digits` 里可能有相同的数字，我们在挑选时要**注意每个数字的使用次数**，不能用超过它出现的次数。  
3. 组合成的三位数必须满足两个要求：  
   - **百位不能是 0**（否则会变成两位数），可以把它想成“电话号码的区号不能是 0”。  
   - **个位必须是偶数**（0、2、4、6、8），这就像挑选“偶数车牌”。  
4. 把所有满足条件的数放进集合（去重），最后把集合转成列表并排序返回。

> **类比**：  
> - `digits` 就像一本装满数字的“抽屉”，每个数字都有自己的“库存”。  
> - 选数字的过程类似“从抽屉里取出三个物品”，每取一次库存就减一。  

#### 代码（Python）

```python
from collections import Counter
from typing import List

def findEvenNumbers_bruteforce(digits: List[int]) -> List[int]:
    cnt = Counter(digits)                 # 统计每个数字出现的次数，像是抽屉里的库存表
    res = set()                           # 用集合自动去重

    # 枚举百位、十位、个位的下标（0~len(digits)-1）
    n = len(digits)
    for i in range(n):                    # 百位
        if digits[i] == 0:                # 不能是 0，避免出现前导零
            continue
        cnt[digits[i]] -= 1               # 使用一次
        for j in range(n):                # 十位
            if cnt[digits[j]] == 0:       # 该数字已经用完
                continue
            cnt[digits[j]] -= 1
            for k in range(n):            # 个位
                if cnt[digits[k]] == 0:   # 该数字已经用完
                    continue
                if digits[k] % 2 == 0:    # 必须是偶数
                    num = digits[i] * 100 + digits[j] * 10 + digits[k]
                    res.add(num)          # 加入集合，自动去重
            cnt[digits[j]] += 1           # 还原十位的使用记录
        cnt[digits[i]] += 1               # 还原百位的使用记录

    return sorted(res)                    # 返回有序列表
```

> **关键行中文注释**已在代码中标出，帮助初学者快速对照。

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 解释：我们用了三层循环，每层最多遍历 `n`（`digits` 的长度）次。  
  - 对于 `n = 100`，最坏情况约是 `100 × 100 × 100 = 1,000,000` 次，仍在可接受范围，但显然不是最优的。  
- **空间复杂度**：`O(1)`（不计返回结果）  
  - 只用了常数级别的额外空间：计数器 `Counter`、集合 `res`（最多装 900 个三位数），与输入规模无关。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈在于三层循环**——我们遍历了所有下标组合，而实际上**合法的三位偶数只有 100~998 之间的 450 个**（每隔 2 就是下一个偶数）。  

**优化思路**：

1. **枚举所有可能的答案**，而不是所有下标组合。  
   - 从 100 到 998（步长 2）遍历每个偶数 `num`。这相当于“检查每个候选三位偶数是否能用手头的数字拼成”。  
2. 对每个 `num`，把它拆成百位、十位、个位的数字 `a, b, c`。  
3. 用 `Counter` 记录 `digits` 中每个数字的库存，然后检查 `a, b, c` 是否都在库存里且库存足够。  
   - 这一步类似“把抽屉里的库存和订单逐项对比”。  
4. 如果对比成功，就把 `num` 加入答案列表。  
5. 最后返回已经排好序的答案（因为我们是从小到大枚举的，直接返回即可）。

> **为什么更快**：  
> - 循环次数从 `n³`（最多 1,000,000）降到 **只遍历 450 个数**，与 `n` 完全无关。  
> - 每次检查只做常数次的计数比较，整体时间复杂度为 `O(450) ≈ O(1)`。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def findEvenNumbers_optimal(digits: List[int]) -> List[int]:
    # 统计每个数字的出现次数，类似“库存表”
    stock = Counter(digits)
    ans = []

    # 只遍历 100~998 之间的偶数（步长 2），共 450 个候选
    for num in range(100, 1000, 2):
        a, b, c = num // 100, (num // 10) % 10, num % 10  # 拆分百、十、个

        # 先排除百位是 0 的情况（虽然这里不会出现，因为从 100 开始），保持严谨
        if a == 0:
            continue

        need = Counter([a, b, c])  # 这三个数字各需要多少个
        # 检查每种数字的需求是否不超过库存
        if all(stock[d] >= need[d] for d in need):
            ans.append(num)        # 合法，加入答案

    return ans  # 已经是从小到大排序好的列表
```

#### 复杂度  

- **时间复杂度**：`O(1)`（常数）  
  - 解释：最多检查 450 个数，每个数只做最多 3 次计数比较，和输入大小 `n` 没有关系。  
- **空间复杂度**：`O(1)`（不计返回列表）  
  - 只用了 `Counter` 保存 10 种数字的出现次数，固定大小。

---

## 心得  

- **核心技巧**：**枚举答案空间 + 计数对比**。先把“可能的答案”列出来，再用“库存表”快速验证是否可行。  
- **适用题型**：  
  1. **组合数字类**：如“从数组中拼成最大/最小数”“找出所有可以组成的回文数”。  
  2. **固定长度排列**：如“用给定字符组成所有合法的长度为 k 的字符串”。  
  3. **资源受限的背包/配对**：如“检查是否能用手头的硬币凑成指定金额”。  
- **一句话总结**：先把**搜索范围缩小到实际答案的集合**，再用**计数表**一次性验证，往往能把指数级的暴力降到常数级。

---

## 反思  

- **第一反应**：直接把三个下标套三层循环，尝试把所有排列列出来。  
- **最容易踩的坑**：  
  - **前导零**：忘记排除百位为 0 的情况，会产生两位数。  
  - **重复使用**：没有正确维护每个数字的使用次数，导致同一个数字被用了超过它在数组中的出现次数。  
  - **去重**：不同下标组合可能得到相同的数字，需要用集合或去重技巧。  
- **下次类似题的第一步**：先思考**答案的取值范围**是否可以直接枚举（比如所有 3 位偶数），再决定是**遍历答案**还是**遍历组合**。这样往往能立刻发现更高效的思路。