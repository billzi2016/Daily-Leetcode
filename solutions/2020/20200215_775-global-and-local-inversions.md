# #775. 全局与局部逆序 / Global and Local Inversions

> 难度：中等 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/global-and-local-inversions/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of length n which represents a permutation of all the integers in the range [0, n - 1].
The number of global inversions is the number of the different pairs (i, j) where:
The number of local inversions is the number of indices i where:
Return true if the number of global inversions is equal to the number of local inversions.

**Examples**

**Example 1:**

```
Input: nums = [1,0,2]
Output: true
Explanation: There is 1 global inversion and 1 local inversion.
```

**Example 2:**

```
Input: nums = [1,2,0]
Output: false
Explanation: There are 2 global inversions and 1 local inversion.
```

**Constraints**

- n == nums.length
- 1 <= n <= 105
- 0 <= nums[i] < n
- All the integers of nums are unique.
- nums is a permutation of all the numbers in the range [0, n - 1].

---

## 题目（中文翻译）

你被给定一个长度为 `n` 的整数数组 `nums`，它是区间 `[0, n - 1]` 内所有整数的一个排列（permutation）。  
全局逆序（global inversion）的数量是满足 `i < j` 且 `nums[i] > nums[j]` 的不同索引对 `(i, j)` 的个数。  
局部逆序（local inversion）的数量是满足 `i < n - 1` 且 `nums[i] > nums[i+1]` 的索引 `i` 的个数。  

返回 `true` 当且仅当全局逆序的数量等于局部逆序的数量。

**示例 1：**

``` 
Input: nums = [1,0,2]
Output: true
Explanation: 有 1 个全局逆序和 1 个局部逆序。
```

**示例 2：**

``` 
Input: nums = [1,2,0]
Output: false
Explanation: 有 2 个全局逆序和 1 个局部逆序。
```

**约束条件：**

- `n == nums.length`
- `1 <= n <= 10^5`
- `0 <= nums[i] < n`
- `nums` 中的所有整数互不相同
- `nums` 是区间 `[0, n - 1]` 内所有数字的一个排列（permutation）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的「索引对」都枚举一遍**，看看每一对 `(i, j)`（`i < j`）是否满足「全局逆序」的定义：`nums[i] > nums[j]`。  
如果满足，就把计数器 `global` 加一。  
同理，**「局部逆序」**只需要检查相邻的两个元素 `(i, i+1)` 是否满足 `nums[i] > nums[i+1]`，把计数器 `local` 加一。  

> **数据结构类比**：  
> 这里我们只用到了 **数组**，把它想象成排好队的学生。遍历所有 `(i, j)` 就像让每个学生去和排在他后面的每个人比较一次身高，看看是不是「前面比后面高」——这就是「逆序」。

只要遍历结束后 `global == local`，答案就是 `True`，否则 `False`。

#### 代码（Python）

```python
def isIdealPermutation(nums):
    n = len(nums)
    global_inv = 0          # 记录全局逆序的数量
    local_inv = 0           # 记录局部逆序的数量

    # 暴力枚举所有 (i, j) (i < j)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] > nums[j]:      # 全局逆序条件
                global_inv += 1

    # 只检查相邻的 i, i+1
    for i in range(n - 1):
        if nums[i] > nums[i + 1]:      # 局部逆序条件
            local_inv += 1

    return global_inv == local_inv
```

> **关键行解释**  
> - `if nums[i] > nums[j]`：判断「前面的数」是否比「后面的数」大，这正是逆序的定义。  
> - `for j in range(i + 1, n)`：确保只比较一次，每对只出现一次。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：外层循环 `n` 次，内层循环平均也要遍历约 `n/2` 次，所以大约要做 `n × n/2 ≈ n²/2` 次比较。对初学者来说，可以把 `O(n²)` 想成「如果有 10 000 个元素，需要大约 100 000 000 次比较」——会很慢。

- **空间复杂度**：`O(1)`  
  - 解释：只用了几个计数变量，和数组长度无关，常数级别的额外空间。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于「每两个位置都要比较一次」——这显然不必要。  
观察题目可以发现：

> **全局逆序 = 局部逆序** 当且仅当 **不存在「跨越两个以上位置的逆序」**。  
> 换句话说，如果某个数 `nums[i]` 与它原本应该在的位置 `i` 的距离超过 1（即 `|nums[i] - i| > 1`），就一定会产生一个「跨距 > 1」的全局逆序，而这个逆序在局部逆序里找不到对应的相邻对，从而导致 `global > local`。

**关键结论**：只要遍历一次数组，检查每个元素是否「离它的下标太远」即可。

- 若 `nums[i]` 在下标 `i-1, i, i+1` 之中（即 `abs(nums[i] - i) <= 1`），则它不可能产生「跨距 > 1」的逆序。  
- 若出现 `abs(nums[i] - i) > 1`，直接返回 `False`。

> **类比**：把 `nums` 看成一本编号为 `0…n-1` 的书被打乱的顺序。全局逆序是「前面的章节号比后面的章节号大」。如果一本书里每一页最多只和前后相邻的页调换位置（最多相差 1），那么所有的「章节号倒置」只能出现在相邻页之间，也就是局部逆序。只要发现有页的编号和它所在位置相差超过 1，就说明出现了「远距离」的倒置，答案必为 `False`。

实现时只需一次线性遍历即可，时间 `O(n)`，空间 `O(1)`。

#### 代码（Python）

```python
def isIdealPermutation(nums):
    """
    判断全局逆序数是否等于局部逆序数。
    只要出现任意位置 i，使得 nums[i] 与 i 的距离大于 1，
    就一定会产生跨越两格以上的逆序，返回 False。
    """
    for i, v in enumerate(nums):
        # 若元素 v 与它的下标 i 相差超过 1，直接返回 False
        if abs(v - i) > 1:
            return False
    return True
```

> **关键行解释**  
> - `enumerate(nums)`：一次性得到下标 `i` 和对应的值 `v`。  
> - `abs(v - i) > 1`：判断「元素离它应该在的位置是否超过 1」——如果是，说明出现了跨距 > 1 的逆序。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：只遍历一次数组，每个元素做一次常数时间的比较。对 10⁵ 长度的数组，只需要 10⁵ 次操作，几乎是瞬间完成的。

- **空间复杂度**：`O(1)`  
  - 解释：只使用了几个临时变量（下标、值），不随 `n` 增长。

---

## 心得

- **核心技巧**：利用「全局逆序 = 局部逆序」等价于「没有跨距大于 1 的逆序」，进而只检查每个元素与下标的距离。  
- **适用的题型**：  
  1. **Permutation + Inversion** 类题目（如 LeetCode 775 “Global and Local Inversions”）。  
  2. **相邻限制** 的排列问题（比如「每个元素最多只能向左/右移动一步」的验证）。  
  3. **局部 vs 全局属性** 的对比（如「局部最大」与「全局最大」的关系）。  
- **一句话总结**：**只要每个数字不离开它原本位置超过一步，所有全局逆序必然是局部逆序**。

---

## 反思

- **第一反应**：想到直接统计两种逆序的数量，用双层循环遍历所有 `(i, j)`。这在小数据时能工作，但一想到 `n` 可达 10⁵，立刻意识到会超时。  
- **最容易踩的坑**：  
  - **忽略排列的唯一性**：如果不利用「是一个排列」的特性，可能会尝试更复杂的结构（如 BIT、线段树），其实完全不必要。  
  - **边界条件**：`abs(nums[i] - i) > 1` 的判断必须在遍历全部元素后才决定，不能提前因为某些特殊值（如 0）误判。  
- **下次思路**：看到「全局」与「局部」的比较时，先问自己「是否存在跨越更远距离的情况」；若答案可以用「位置偏移」直接判定，就尝试 **O(n)** 的一次遍历方案。