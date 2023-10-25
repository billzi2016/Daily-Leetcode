# #2449. 最小操作次数使数组相似 / Minimum Number of Operations to Make Arrays Similar

> 难度：困难 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-make-arrays-similar/)

---

## 题目（英文原版）

**Description**

You are given two positive integer arrays nums and target, of the same length.
In one operation, you can choose any two distinct indices i and j where 0 <= i, j < nums.length and:
Two arrays are considered to be similar if the frequency of each element is the same.
Return the minimum number of operations required to make nums similar to target. The test cases are generated such that nums can always be similar to target.

**Examples**

**Example 1:**

```
Input: nums = [8,12,6], target = [2,14,10]
Output: 2
Explanation: It is possible to make nums similar to target in two operations:
- Choose i = 0 and j = 2, nums = [10,12,4].
- Choose i = 1 and j = 2, nums = [10,14,2].
It can be shown that 2 is the minimum number of operations needed.
```

**Example 2:**

```
Input: nums = [1,2,5], target = [4,1,3]
Output: 1
Explanation: We can make nums similar to target in one operation:
- Choose i = 1 and j = 2, nums = [1,4,3].
```

**Example 3:**

```
Input: nums = [1,1,1,1,1], target = [1,1,1,1,1]
Output: 0
Explanation: The array nums is already similiar to target.
```

**Constraints**

- n == nums.length == target.length
- 1 <= n <= 105
- 1 <= nums[i], target[i] <= 106
- It is possible to make nums similar to target.

---

## 题目（中文翻译）

给定两个长度相同的正整数数组 `nums` 和 `target`。

一次操作中，你可以选择任意两个不同的下标 `i` 和 `j`（`0 <= i, j < nums.length`），并执行以下操作：

- 将 `nums[i]` 增加 `2`，同时将 `nums[j]` 减少 `2`。

如果两个数组中每个元素出现的次数（frequency）完全相同，则称这两个数组**相似**（similar）。

返回将 `nums` 变得与 `target` 相似所需的最小操作次数。题目保证一定可以通过若干次操作使 `nums` 与 `target` 相似。

---

### 示例

#### 示例 1
**输入**  
``` 
nums = [8,12,6], target = [2,14,10]
```  
**输出**  
```
2
```  
**解释**  
可以在两次操作后使 `nums` 与 `target` 相似：
1. 选择 `i = 0`，`j = 2`，`nums` 变为 `[10,12,4]`。  
2. 选择 `i = 1`，`j = 2`，`nums` 变为 `[10,14,2]`。  

可以证明，最少需要 2 次操作。

#### 示例 2
**输入**  
``` 
nums = [1,2,5], target = [4,1,3]
```  
**输出**  
```
1
```  
**解释**  
只需一次操作即可使 `nums` 与 `target` 相似：
- 选择 `i = 1`，`j = 2`，`nums` 变为 `[1,4,3]`。

#### 示例 3
**输入**  
``` 
nums = [1,1,1,1,1], target = [1,1,1,1,1]
```  
**输出**  
```
0
```  
**解释**  
数组 `nums` 已经与 `target` 相似，无需操作。

---

### 约束条件
- `n == nums.length == target.length`
- `1 <= n <= 10^5`
- `1 <= nums[i], target[i] <= 10^6`
- 必定可以通过若干次操作使 `nums` 与 `target` 相似。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把 `nums` 中的每一个元素都和 `target` 中的每一个元素逐个比较**，如果不相等就动手“改”。  
因为一次操作只能选两个下标 `i`、`j`，我们可以把「把 `nums[i]` 调大」和「把 `nums[j]` 调小」这两件事一次性完成。  

- **数据结构**：我们只需要两个普通的 Python 列表。可以把它们想象成「两排号码牌」，我们把每个号码牌和对应的目标号码牌一一对应，看谁不匹配就去调换。
- **为什么正确**：只要把每一个不匹配的 `nums[i]` 调整到它对应的 `target[i]`，最终两列号码牌的频率（出现次数）就会完全一样。  
- **复杂度分析**：  
  - 为了找到「哪个 `nums[i]` 对应哪个 `target[j]`」我们需要两层循环：外层遍历 `i`（`n` 次），内层遍历 `j`（最坏也要 `n` 次），所以总共要做大约 `n × n` 次比较。  
  - 用大白话讲，`O(n²)` 就是「如果数组有 10 000 个数，程序要跑 100 000 000（1 亿）次」——在实际运行时会非常慢，甚至会超时。  
  - 空间上我们只用了原来的两个数组和几个临时变量，和输入规模无关，记作 `O(1)`（常数空间）。

#### 代码（Python）

```python
def min_operations_bruteforce(nums, target):
    n = len(nums)
    ops = 0                      # 记录已经做了多少次操作
    # 把 nums 按顺序和 target 按顺序两两比较
    for i in range(n):
        # 如果已经和 target[i] 相同，直接进入下一个位置
        if nums[i] == target[i]:
            continue
        # 否则在后面的下标里找一个可以「借」2 的位置 j
        for j in range(i + 1, n):
            if nums[j] == target[i]:
                # 直接把 nums[i] 与 nums[j] 交换，使两者都对上
                nums[i], nums[j] = nums[j], nums[i]
                ops += 1          # 完成一次「交换」操作
                break
            # 如果找不到完全相同的数，只好把差距缩小 2
            # （这里的实现非常笨，实际会超时，仅作示意）
            diff = nums[i] - target[i]
            if diff > 0 and nums[j] < target[j]:
                nums[i] -= 2
                nums[j] += 2
                ops += 1
                if nums[i] == target[i]:
                    break
    return ops
```

> **注意**：上述代码只是演示「暴力」的思路，真实提交会因为 `O(n²)` 的时间复杂度而超时。

#### 复杂度  

- **时间复杂度**：`O(n²)` — 需要两层循环去寻找可以配对的下标。  
- **空间复杂度**：`O(1)` — 只使用了常数个额外变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**每一次操作都是把一个数减 2、另一个数加 2**。  
这意味着：

1. **奇数永远保持奇数，偶数永远保持偶数**（因为 `+2 / -2` 不会改变奇偶性）。  
2. 只要把所有 **偶数** 和所有 **奇数** 分别对应好，整体就会相似。  

所以我们可以把问题拆成两个完全独立的小问题：

- 把 `nums` 中的所有偶数与 `target` 中的偶数配对。  
- 把 `nums` 中的所有奇数与 `target` 中的奇数配对。  

配对的原则是**从小到大贪心匹配**：

- 把两个偶数列表都排序（从小到大），然后一一对应。  
- 对每一对 `(a, b)`（`a` 来自 `nums`，`b` 来自 `target`），如果 `a > b`，说明 `a` 里「多」了 `a-b`，需要把这多余的部分转移走；如果 `a < b`，说明 `a`「少」了 `b-a`，需要把别的数转过来。  
- 由于一次操作可以把 **2** 从「多」的数转到「少」的数，所以 **每次转移 2 的次数 = (多余的总量) / 2**。  

> **关键点**：只需要统计「多余」的总量（即所有 `a > b` 时的差），不必关心「少」的总量，因为两者必然相等（题目保证可以相似）。

**算法步骤**：

1. 将 `nums` 与 `target` 按奇偶性分别放进四个列表：`even_nums, odd_nums, even_tgt, odd_tgt`。  
2. 对每个列表分别排序。  
3. 遍历已排序的偶数列表，累加 `max(0, even_nums[i] - even_tgt[i])`，得到 `excess_even`。  
4. 同理得到 `excess_odd`。  
5. 最终答案 = `(excess_even + excess_odd) // 2`（每次操作消耗 2）。  

**为什么是最优的**：

- **贪心的合理性**：把最小的 `nums` 配对最小的 `target`，可以保证「多余」的数尽可能小；如果我们把大的 `nums` 配对小的 `target`，会产生更大的差距，需要更多的转移次数。  
- **没有更好的办法**：每一次操作只能把 **2** 从一个位置搬到另一个位置，所有「多余」的 2 必须全部搬走，搬走的次数下限就是「多余总量 / 2」。我们已经达到了这个下限，所以就是最小次数。

#### 代码（Python）

```python
def min_operations(nums, target):
    """
    返回把 nums 变得和 target “相似” 所需的最少操作次数。
    思路：奇偶分离、排序后贪心配对、统计多余量 / 2。
    """
    # 1. 按奇偶性分组
    even_nums, odd_nums = [], []
    even_tgt,  odd_tgt  = [], []
    for x in nums:
        (even_nums if x % 2 == 0 else odd_nums).append(x)
    for x in target:
        (even_tgt if x % 2 == 0 else odd_tgt).append(x)

    # 2. 排序（从小到大）
    even_nums.sort()
    even_tgt.sort()
    odd_nums.sort()
    odd_tgt.sort()

    # 3. 统计“多余”部分（只算 nums > target 的差）
    excess = 0
    for a, b in zip(even_nums, even_tgt):
        if a > b:
            excess += a - b          # 这里的 a - b 必然是偶数
    for a, b in zip(odd_nums, odd_tgt):
        if a > b:
            excess += a - b

    # 4. 每次操作可以把 2 从“多余”位置搬走
    return excess // 2
```

> **代码要点注释**  
> - `x % 2 == 0` 判断奇偶，类似于“查字典”把数字放进对应的“书架”。  
> - `sort()` 相当于把书架里的书排好顺序，方便“一对一配对”。  
> - `excess // 2` 用整数除法把「多余的 2 的个数」直接转化为「操作次数」。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 分组是 `O(n)`，排序是 `O(n log n)`（主导因素），遍历统计是 `O(n)`。  
  - 用大白话说：如果有 100 000 个数，排序大约需要 100 000 × log₂100 000 ≈ 1.7 百万次比较，完全可以在一秒内跑完。  
- **空间复杂度**：`O(n)`  
  - 需要额外存放四个列表（每个最多 `n/2` 长），相当于原始数据的两倍大小，仍然是线性空间。

---

## 心得

- **核心技巧**：**奇偶分离 + 贪心配对 + 统计多余量**。  
- **适用的题型**（类似思路）  
  1. “把数组变成另一个数组，只能每次把两个数各加/减同一个偶数”。  
  2. “数组相等的最小操作次数”，要求每次操作保持奇偶不变。  
  3. “把两组数配对，使总差值最小”，常用排序后逐位比较的贪心。  
- **解题钥匙**：**“一次操作只能搬走 2，所有多余的 2 必须全部搬走 → 操作次数 = 多余总量 / 2”。**

---

## 反思

- **第一反应**：看到「两数相减 2」的操作，立刻想到「把大数往小数搬」——于是想到直接两两配对的暴力做法。  
- **最容易踩的坑**  
  1. **忘记奇偶不可变**：如果把奇数和偶数混在一起配对，会得到错误的答案。  
  2. **忽视“多余”与“缺少”必须相等**：题目保证可以相似，但如果自行构造测试用例时忘记这点，可能出现 `excess` 与 `deficit` 不匹配的错误。  
  3. **除以 2 时忘记取整**：`excess` 必然是偶数，但如果不小心用了普通除法会得到浮点数，需要使用整数除 `//`。  
- **下次遇到同类题**：**先检查是否有保持奇偶/模数不变的限制 → 把数组按该限制分组 → 对每组排序后贪心配对 → 统计多余量 / 单位搬运量**。这样可以快速定位最优解的思路。