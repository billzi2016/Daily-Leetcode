# #1887. **约简操作使数组元素相等** / Reduction Operations to Make the Array Elements Equal

> 难度：中等 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/reduction-operations-to-make-the-array-elements-equal/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, your goal is to make all elements in nums equal. To complete one operation, follow these steps:
Return the number of operations to make all elements in nums equal.

**Examples**

**Example 1:**

```
Input: nums = [5,1,3]
Output: 3
Explanation: It takes 3 operations to make all elements in nums equal:
1. largest = 5 at index 0. nextLargest = 3. Reduce nums[0] to 3. nums = [3,1,3].
2. largest = 3 at index 0. nextLargest = 1. Reduce nums[0] to 1. nums = [1,1,3].
3. largest = 3 at index 2. nextLargest = 1. Reduce nums[2] to 1. nums = [1,1,1].
```

**Example 2:**

```
Input: nums = [1,1,1]
Output: 0
Explanation: All elements in nums are already equal.
```

**Example 3:**

```
Input: nums = [1,1,2,2,3]
Output: 4
Explanation: It takes 4 operations to make all elements in nums equal:
1. largest = 3 at index 4. nextLargest = 2. Reduce nums[4] to 2. nums = [1,1,2,2,2].
2. largest = 2 at index 2. nextLargest = 1. Reduce nums[2] to 1. nums = [1,1,1,2,2].
3. largest = 2 at index 3. nextLargest = 1. Reduce nums[3] to 1. nums = [1,1,1,1,2].
4. largest = 2 at index 4. nextLargest = 1. Reduce nums[4] to 1. nums = [1,1,1,1,1].
```

**Constraints**

- 1 <= nums.length <= 5 * 104
- 1 <= nums[i] <= 5 * 104

---

## 题目（中文翻译）

给定一个整数数组 `nums`，你的目标是通过若干次操作使 `nums` 中的所有元素相等。一次操作的步骤如下：

1. 找到数组中最大的元素（largest）及其下标。  
2. 找到数组中第二大的元素（nextLargest），即严格小于 largest 的最大值。  
3. 将 **所有** 等于 largest 的元素的值减小（reduce）至 nextLargest。

返回使数组中所有元素相等所需的操作次数。

---

### 示例

#### 示例 1
**输入**  
`nums = [5,1,3]`

**输出**  
`3`

**解释**  
需要 3 次操作才能使所有元素相等：
1. `largest = 5`（下标 0），`nextLargest = 3`。将 `nums[0]` 减至 3，数组变为 `[3,1,3]`。  
2. `largest = 3`（下标 0），`nextLargest = 1`。将 `nums[0]` 减至 1，数组变为 `[1,1,3]`。  
3. `largest = 3`（下标 2），`nextLargest = 1`。将 `nums[2]` 减至 1，数组变为 `[1,1,1]`。

#### 示例 2
**输入**  
`nums = [1,1,1]`

**输出**  
`0`

**解释**  
数组中的所有元素已经相等，无需操作。

#### 示例 3
**输入**  
`nums = [1,1,2,2,3]`

**输出**  
`4`

**解释**  
需要 4 次操作才能使所有元素相等：
1. `largest = 3`（下标 4），`nextLargest = 2`。将 `nums[4]` 减至 2，数组变为 `[1,1,2,2,2]`。  
2. `largest = 2`（下标 2），`nextLargest = 1`。将 `nums[2]` 减至 1，数组变为 `[1,1,1,2,2]`。  
3. `largest = 2`（下标 3），`nextLargest = 1`。将 `nums[3]` 减至 1，数组变为 `[1,1,1,1,2]`。  
4. `largest = 2`（下标 4），`nextLargest = 1`。将 `nums[4]` 减至 1，数组变为 `[1,1,1,1,1]`。

---

### 约束条件

- `1 <= nums.length <= 5 * 10^4`
- `1 <= nums[i] <= 5 * 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **一步一步地模拟题目描述的操作** ：  

1. 在当前数组中找到最大的元素 `largest`（把它想成“最高的山”）。  
2. 再找出除 `largest` 之外的第二大元素 `nextLargest`（次高的山）。  
3. 把其中一个 `largest` 的位置直接“砍”成 `nextLargest` 的高度。  

把这三步循环执行，直到数组里所有数字都相同为止。  

> **数据结构类比**  
> - “找最大/次大”可以用一次遍历来完成，就像在一堆书里找最高的那本书。  
> - 我们只需要一个普通的 **列表**（list），不需要额外的哈希表、堆等高级结构。

**为什么正确**  
每一次操作都把最高的数降到次高的数。这样不会错过任何可能的更快方式，因为题目规定只能把 **最大** 的元素降到 **次大** 的值。只要我们一直这么做，最终所有数都会等于最小的那个值，过程必然可行。

**时间/空间复杂度（大白话）**  
- 每一次操作我们都要遍历整个数组去找最大和次大，这相当于 **看一遍所有书**。  
- 最坏情况下，数组里有 `n` 个不同的数，需要 **n‑1 次** 操作。  
- 所以总共要遍历 `n` 次，每次 `O(n)`，时间复杂度是 **O(n²)**（想象成 “平方级别”，如果数组长 1000，需要大约 1,000,000 次基本操作）。  
- 只使用了原数组和几个临时变量，空间复杂度是 **O(1)**（常数级别）。

#### 代码（Python）

```python
def reductionOperations_bruteforce(nums):
    """
    暴力模拟题目描述的操作。
    :param nums: List[int]，题目给定的数组
    :return: int，完成所有元素相等需要的操作次数
    """
    ops = 0                     # 记录已经做了多少次操作
    n = len(nums)

    while True:
        # 1. 找到当前数组的最大值和次大值
        max_val = max(nums)                     # 最大值
        # 次大值要排除所有等于 max_val 的元素
        second_max = max(x for x in nums if x != max_val) if any(x != max_val for x in nums) else max_val

        # 如果最大值已经等于次大值，说明所有元素相同，结束循环
        if max_val == second_max:
            break

        # 2. 把第一个出现的 max_val 降到 second_max
        for i in range(n):
            if nums[i] == max_val:
                nums[i] = second_max
                break

        ops += 1                # 完成一次操作

    return ops
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 每一次循环需要一次 `max`（`O(n)`）和一次遍历找要修改的下标（`O(n)`），最坏会循环 `n-1` 次。  
- **空间复杂度**：`O(1)`  
  - 只用了几个额外变量，未随输入规模增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次都要遍历整个数组去找最大/次大。  
如果我们把数组 **先排好序**，那么“最大”和“次大”就会相邻出现，**不需要再遍历去找**，只要一次线性扫描就能算出答案。

关键观察：

1. 排序后，所有相同的数会聚在一起。  
2. 当我们把所有最大的数一次性降到次大的数时，实际完成的操作次数等于 **已经出现过的（比次大大的）元素个数**。  
3. 再往左继续处理次大的数，同理，操作次数等于 **之前已经处理过的元素总数**。

于是可以这样做：

- 对 `nums` 进行升序排序。  
- 从右往左遍历（从最大值往最小值），用 `cnt` 记录已经遍历过的元素个数（即已经“变平”的元素）。  
- 每当遇到一个 **新出现的值**（与左边的值不相同），说明我们需要把这些 `cnt` 个已经平好的元素再一次“压”下来，操作次数累加 `cnt`。  
- 最后 `cnt` 会累计所有不同值之间的距离，总和即为答案。

> **数据结构类比**  
> - 排序后数组就像把一堆不同高度的砖块排成了梯子，**从最高的梯级往下走**，每跨一步需要把已经走过的所有砖块搬走一次。  
> - 只用到 **列表** 和 **整数计数器**，不需要额外的哈希表或堆。

**为什么正确**  
- 每一次“压”操作都把当前最高的整块相同数降到下一个不同的数。因为数组已经排好序，这一步只需要知道有多少块已经被压过（`cnt`），不必真的去改数组。  
- 题目规定只能把 **最大** 降到 **次大**，而我们一次性把 **所有最大** 同时降到次大，等价于把每个最大元素单独操作的次数之和，正好是 `cnt`。  
- 逐层向左压完所有不同的数后，所有元素都等于最小值，过程必然最少。

**时间/空间复杂度（大白话）**  
- 排序耗时 `O(n log n)`（想象把书按字母顺序排好，需要比“平方级”更少的比较）。  
- 排序后只需一次线性扫描 `O(n)`。  
- 总体时间复杂度 `O(n log n)`，已经是最优的（因为排序本身就需要 `log n` 级别的比较）。  
- 只用了几个计数变量，空间复杂度 `O(1)`（不计排序本身的原地改动）。

#### 代码（Python）

```python
def reductionOperations(nums):
    """
    最优解：先排序，再一次遍历统计不同值之间的“层数”。
    :param nums: List[int]
    :return: int
    """
    nums.sort()               # O(n log n) 的排序
    ops = 0                   # 累计需要的操作次数
    cnt = 0                   # 已经遍历过（已被压平）的元素个数

    # 从右往左遍历（从最大值往最小值）
    for i in range(len(nums) - 1, 0, -1):
        cnt += 1               # 当前元素已经“准备好”参与压平
        # 如果左边的元素和当前元素不同，说明出现了一个新的层级
        if nums[i] != nums[i - 1]:
            ops += cnt        # 把已经累计的 cnt 次操作加到答案

    return ops
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序是主导耗时，后面的遍历是 `O(n)`，两者相加仍是 `O(n log n)`。  
  - 与暴力解的 `O(n²)` 相比，规模为 5×10⁴ 时，最优解快数百倍。  
- **空间复杂度**：`O(1)`（如果使用原地排序）  
  - 只用了常数个整数变量。

---

## 心得  

- **核心技巧**：先排序，再利用**不同值的层数**累加已处理元素的数量。  
- 这种“层层压平”思路在 **需要把数组统一到最小/最大值** 的题目里非常常见。  
- **类似题目**  
  1. *LeetCode 1658. Minimum Operations to Reduce X to Zero*（利用前缀和/后缀和求最少操作）  
  2. *LeetCode 462. Minimum Moves to Equal Array Elements*（把所有数变成最小数的移动次数）  
  3. *LeetCode 2134. Minimum Swaps to Group All 1's Together*（把相同元素聚在一起的最少操作）  

> **一句话总结解题钥匙**：**排序 + 统计相邻不同值之间已累积的元素数**。

---

## 反思  

- **第一反应**：直接把题目描述的操作逐步模拟。  
- **最容易踩的坑**  
  - 忘记在遍历时累计 `cnt`（已经被压平的元素数），导致统计不到每层的操作次数。  
  - 边界条件：全部相同的数组直接返回 0；单元素数组同样是 0。  
  - 使用 `max` 时若全部相同会导致 `second_max` 仍等于 `max`，需要提前结束循环。  
- **下次遇到同类题**：  
  1. 先思考是否可以 **先排序**，把“最大/次大”关系变成相邻位置。  
  2. 再检查 **是否可以一次性统计** 某一类元素的贡献，而不是逐个模拟。  

祝你编码愉快，继续加油！