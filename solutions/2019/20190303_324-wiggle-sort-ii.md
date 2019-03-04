# #324. 摆动排序 II / Wiggle Sort II

> 难度：中等 · 标签：Array、Divide and Conquer、Greedy、Sorting、Quickselect · [LeetCode 链接](https://leetcode.com/problems/wiggle-sort-ii/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, reorder it such that nums[0] < nums[1] > nums[2] < nums[3]....
You may assume the input array always has a valid answer.

**Examples**

**Example 1:**

```
Input: nums = [1,5,1,1,6,4]
Output: [1,6,1,5,1,4]
Explanation: [1,4,1,5,1,6] is also accepted.
```

**Example 2:**

```
Input: nums = [1,3,2,2,3,1]
Output: [2,3,1,3,1,2]
```

**Constraints**

- 1 <= nums.length <= 5 * 104
- 0 <= nums[i] <= 5000
- It is guaranteed that there will be an answer for the given input nums.

---

## 题目（中文翻译）

给定一个整数数组 `nums`，请重新排列，使得满足 `nums[0] < nums[1] > nums[2] < nums[3] …` 的交替关系。  
你可以假设对于给定的输入数组，总能找到一个有效的答案。

### 示例

#### 示例 1
**输入**  
``` 
nums = [1,5,1,1,6,4]
```  
**输出**  
```
[1,6,1,5,1,4]
```  
**解释**  
`[1,4,1,5,1,6]` 也是一种可接受的答案。

#### 示例 2
**输入**  
``` 
nums = [1,3,2,2,3,1]
```  
**输出**  
```
[2,3,1,3,1,2]
```

### 约束条件
- `1 <= nums.length <= 5 * 10^4`
- `0 <= nums[i] <= 5000`
- 保证对于给定的 `nums` 至少存在一种满足条件的排列。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把所有排列都列举出来，检查每一种排列是否满足  

```
nums[0] < nums[1] > nums[2] < nums[3] ...
```  

如果满足，就直接返回。  

- **用到的数据结构**：  
  - `list`（Python 中的数组）保存当前排列。  
  - `itertools.permutations` 相当于“把所有可能的菜谱全写出来”，就像把所有单词的排列顺序列成一本大字典。  

- **为什么正确**：  
  暴力枚举遍历了**所有**可能的重排方式，只要有一种满足条件，就一定能在遍历过程中被找到，所以一定能得到答案。  

- **复杂度分析（大白话）**：  
  - 对长度为 `n` 的数组，所有排列的数量是 `n!`（读作 “n 的阶乘”，比如 n=5 时有 120 种）。  
  - 对每一种排列，我们要检查 `n-1` 条不等式（相邻两位的大小关系），所以总的时间是 `O(n! * n)`，这在实际中会非常慢，甚至连 10 个元素的数组都算不完。  
  - 额外的空间只用来保存一次排列，`O(n)`。  

#### 代码（Python）  

```python
import itertools

def wiggleSort_brute(nums):
    """
    暴力解：枚举所有排列，找到第一个满足摆动条件的排列返回
    """
    for perm in itertools.permutations(nums):
        ok = True
        # 检查相邻位置的大小关系
        for i in range(len(perm) - 1):
            if i % 2 == 0:               # 偶数下标后面应当更大
                if not (perm[i] < perm[i + 1]):
                    ok = False
                    break
            else:                        # 奇数下标后面应当更小
                if not (perm[i] > perm[i + 1]):
                    ok = False
                    break
        if ok:
            # 把 tuple 转回 list 并原地修改原数组
            nums[:] = list(perm)
            return
```

#### 复杂度  

- **时间复杂度**：`O(n! * n)` —— 先把所有排列都写出来（`n!`），每个排列再检查 `n` 次。  
- **空间复杂度**：`O(n)` —— 只保存当前的一个排列（`itertools.permutations` 会惰性产生，不会一次性占用 `n!` 空间），以及递归栈的临时空间。  

---

### 2. 最优解  

#### 思路  

从暴力解出发，慢的地方显而易见：**枚举所有排列** 这一层根本不可接受。  
要想快，就必须**不去穷举**，而是直接构造满足条件的序列。  

关键观察  

1. **“摆动”序列的本质**  
   把数组排成从小到大的顺序后，若把较小的一半放在奇数位置，较大的一半放在偶数位置，就能得到 `< > < > …` 的形状。  
   例子：  
   - 排序后 `[1,1,1,4,5,6]`  
   - 小半段 `[1,1,1]`（下标 0~2）  
   - 大半段 `[4,5,6]`（下标 3~5）  
   - 交叉放置得到 `[1,6,1,5,1,4]`，正好满足要求。  

2. **为什么要“交叉”**  
   - 偶数下标（0、2、4…）必须比右边的奇数下标小。  
   - 所以我们把 **最大的** 元素放到奇数下标的最左侧（`1`），把 **次大的** 放到下一个奇数下标，依次类推。  
   - 同理，**最小的** 元素放到最左侧的偶数下标。  

3. **怎样快速拿到“中位数”**  
   为了把数组分成「小」和「大」两半，我们只需要找到第 `⌊n/2⌋` 小的元素（中位数）。  
   这可以用 **快速选择（Quickselect）**，时间平均是 `O(n)`，最坏是 `O(n²)`（但实际数据几乎不会出现最坏情况）。  

4. **三路划分 + 虚拟索引**  
   - 找到中位数后，把数组划分为三类：`< median`、`= median`、`> median`。  
   - 为了让「大」的数出现在奇数位，「小」的数出现在偶数位，我们使用 **虚拟索引**：  

     ```
     new_index(i) = (1 + 2*i) % (n | 1)
     ```

     解释：  
     - `n | 1` 把 `n` 强制变成奇数（如果是偶数就加 1），这样模运算可以把下标循环遍历完整个数组。  
     - `1 + 2*i` 按 `1,3,5,…,0,2,4,…` 的顺序访问下标，先填奇数位再填偶数位。  

   - 用 **荷兰国旗**（三路划分）在虚拟索引的顺序上完成「大」「中」「小」的原地重排。  

整体步骤  

1. 用 Quickselect 找到中位数 `mid`（第 `n//2` 小的数）。  
2. 设三个指针 `left=0, i=0, right=n-1`。  
3. 当 `i <= right` 时，根据 `nums[new_index(i)]` 与 `mid` 的关系执行：  
   - 大于 `mid` → 交换到左边（`left` 位置），`left++，i++`。  
   - 小于 `mid` → 交换到右边（`right` 位置），`right--`（`i` 不动，因为换来的数还需要检查）。  
   - 等于 `mid` → 只移动 `i++`。  

遍历结束后，数组已经满足 `nums[0] < nums[1] > nums[2] …`。  

#### 代码（Python）  

```python
import random
from typing import List

def wiggleSort(nums: List[int]) -> None:
    """
    最优解：O(n) 时间、O(1) 额外空间
    思路概括：
    1) 用 Quickselect 找到中位数 mid
    2) 使用「虚拟索引」把大于 mid 的数放到奇数位，
       小于 mid 的数放到偶数位，等于 mid 的数自然填在中间
    3) 采用荷兰国旗三路划分在虚拟索引顺序上完成原地重排
    """
    n = len(nums)
    if n <= 1:
        return

    # ---------- 第一步：找中位数 ----------
    def nth_element(k: int) -> int:
        """
        返回第 k 小的元素（0-indexed），等价于 C++ 的 nth_element。
        采用随机化的快速选择，平均 O(n)。
        """
        def select(left: int, right: int) -> int:
            # 随机选一个 pivot，避免最坏情况
            pivot_idx = random.randint(left, right)
            nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
            pivot = nums[right]

            # partition，返回 pivot 最终所在的位置
            i = left
            for j in range(left, right):
                if nums[j] < pivot:
                    nums[i], nums[j] = nums[j], nums[i]
                    i += 1
            # 把 pivot 放到中间
            nums[i], nums[right] = nums[right], nums[i]

            # 根据 i 与 k 的关系递归
            if k == i:
                return nums[i]
            elif k < i:
                return select(left, i - 1)
            else:
                return select(i + 1, right)

        return select(0, n - 1)

    mid = nth_element(n // 2)      # 中位数

    # ---------- 第二步：虚拟索引 ----------
    # new_idx(i) 把 i 映射到「先奇后偶」的下标序列
    def new_idx(i: int) -> int:
        return (1 + 2 * i) % (n | 1)   # n|1 把 n 变成奇数

    # ---------- 第三步：荷兰国旗三路划分 ----------
    left, i, right = 0, 0, n - 1
    while i <= right:
        cur = nums[new_idx(i)]
        if cur > mid:                     # 大的放左边（奇数位）
            nums[new_idx(left)], nums[new_idx(i)] = cur, nums[new_idx(left)]
            left += 1
            i += 1
        elif cur < mid:                   # 小的放右边（偶数位）
            nums[new_idx(right)], nums[new_idx(i)] = cur, nums[new_idx(right)]
            right -= 1                     # i 不动，需要再次检查换来的元素
        else:                             # 等于中位数，留在中间
            i += 1
```

#### 复杂度  

- **时间复杂度**：`O(n)`（平均）  
  - 快速选择找中位数需要遍历一次数组（平均 `O(n)`）。  
  - 三路划分再遍历一次数组（`O(n)`）。  
  - 两次线性遍历相加仍是线性级别。  
  - 与暴力解的 `O(n!·n)` 相比，速度提升了 **天壤之别**，即使是最大 `5·10⁴` 的输入也能在毫秒级完成。  

- **空间复杂度**：`O(1)`（原地）  
  - 只用了常数个额外指针 `left、i、right`，以及递归栈（Quickselect 的递归深度平均为 `log n`，最坏 `n`，但我们用了随机化，实际占用几乎可以忽略）。  

---

## 心得  

- **核心技巧**：利用 **中位数 + 三路划分 + 虚拟索引** 把「大」和「小」的数分别塞进奇、偶位置，从而一次遍历完成摆动排序。  
- **适用的题型**（类似思路可复用）：  
  1. **Wiggle Sort I**（只要求 `nums[0] <= nums[1] >= nums[2] ...`，可以用一次线性扫描或排序后交叉）。  
  2. **相对排序（Relative Sort Array）**——需要把某些元素分组并保持相对顺序。  
  3. **荷兰国旗问题**（颜色分类）——三路划分的经典应用。  

- **一句话总结**：  
  “先找中位数把数组切成大小两半，再用虚拟索引把‘大’放奇数位、‘小’放偶数位，一次遍历即可完成摆动”。  

---

## 反思  

- **第一反应**：看到 “< > < > …” 的交替不等式，马上想到把数组 **排序后交叉**，但忘记了相同元素可能导致相邻相等而违背不等式。  
- **最容易踩的坑**：  
  - **重复元素**：如果直接把排好序的数组交叉，出现 `... 2,2,2 ...` 时会破坏摆动。必须用 **中位数 + 三路划分** 保证 “大于中位数” 与 “小于中位数” 的严格分布。  
  - **奇偶长度不同**：当数组长度为偶数时，左侧（小的一半）比右侧多一个元素，需要 `new_idx` 中的 `n|1` 做奇数化处理，否则会出现下标冲突。  
  - **快速选择的最坏情况**：若不随机化，特定输入会退化为 `O(n²)`。随机化 pivot 可以把概率风险降到可以接受的水平。  

- **下次遇到同类题的第一步**：  
  “先判断是否可以通过 **统计/划分** 把数组分成两类（大/小），再思考如何在原地交叉放置”。如果可以找到 **中位数**（或其他阈值），往往可以用 **三路划分 + 虚拟索引** 把答案直接构造出来。