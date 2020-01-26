# #747. 至少是其他数两倍的最大数 / Largest Number At Least Twice of Others

> 难度：简单 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/largest-number-at-least-twice-of-others/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums where the largest integer is unique.
Determine whether the largest element in the array is at least twice as much as every other number in the array. If it is, return the index of the largest element, or return -1 otherwise.

**Examples**

**Example 1:**

```
Input: nums = [3,6,1,0]
Output: 1
Explanation: 6 is the largest integer.
For every other number in the array x, 6 is at least twice as big as x.
The index of value 6 is 1, so we return 1.
```

**Example 2:**

```
Input: nums = [1,2,3,4]
Output: -1
Explanation: 4 is less than twice the value of 3, so we return -1.
```

**Constraints**

- 2 <= nums.length <= 50
- 0 <= nums[i] <= 100
- The largest element in nums is unique.

---

## 题目（中文翻译）

给定一个整数数组 `nums`，其中最大整数是唯一的。  
判断数组中的最大元素是否至少是数组中每个其他数字的两倍。如果是，返回最大元素的下标；否则返回 `-1`。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  

**示例 1:**  
```
Input: nums = [3,6,1,0]
Output: 1
```
**解释:** 6 是数组中的最大整数。对于数组中的每个其他数字 `x`，6 至少是 `x` 的两倍。值为 6 的下标是 1，因此返回 1。

**示例 2:**  
```
Input: nums = [1,2,3,4]
Output: -1
```
**解释:** 4 小于 3 的两倍，所以返回 -1。

**约束条件**  
- `2 <= nums.length <= 50`  
- `0 <= nums[i] <= 100`  
- `nums` 中的最大元素是唯一的。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把每个数都和其它所有数比较一遍**，看它是不是“至少是其他数的两倍”。  
- 这里用到的最基本的数据结构就是**数组（list）**，可以把它想象成一排装有商品编号的货架，`nums[i]` 就是第 `i` 格货架上的商品重量。  
- 暴力做法的步骤如下  
  1. 先遍历一次数组，找出最大值 `max_val`（因为题目保证最大值唯一），记录它的下标 `max_idx`。这一步相当于在货架上挑出最重的商品。  
  2. 再遍历一次数组，对每一个 `x`（除 `max_val` 本身外）检查 `max_val >= 2 * x` 是否成立。只要有一次不成立，就可以直接返回 `-1`。  
  3. 如果所有比较都通过，则返回 `max_idx`。  

这个思路之所以一定正确，是因为我们已经把“最大数”锁定下来，随后只需要验证它是否满足题目要求的“至少是其他每个数的两倍”。  

如果把上述两次遍历合并成 **两层循环**（每个元素都去和其它每个元素比较），时间复杂度会是 `O(n²)`，这就是最“笨”的写法，直观但不高效。下面先给出这种 `O(n²)` 的实现，帮助大家感受暴力思路的完整过程。

#### 代码（Python）  

```python
def dominantIndex_bruteforce(nums):
    n = len(nums)
    # 第一次遍历：找到最大值和它的下标
    max_val = nums[0]
    max_idx = 0
    for i in range(1, n):
        if nums[i] > max_val:
            max_val = nums[i]
            max_idx = i

    # 第二次遍历：两层循环，比较每一对数
    for i in range(n):
        if i == max_idx:          # 跳过自己
            continue
        # 如果发现 max_val < 2 * nums[i]，条件不满足
        if max_val < 2 * nums[i]:
            return -1

    # 所有比较都通过，返回最大值的下标
    return max_idx
```

> **代码要点**  
> - `max_val` 与 `max_idx` 就像“字典”里记下的**关键字**（最大数）和**页码**（下标）。  
> - `if max_val < 2 * nums[i]` 是核心判断：如果最大数不到其他数的两倍，就直接返回 `-1`。  

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  - “`n²`” 的含义可以这样想：如果有 10 个数，暴力方法要比较 10×9≈100 次；如果有 100 个数，就要比较 10,000 次，数量呈平方增长，规模稍大时就会明显变慢。  
- **空间复杂度：** `O(1)`  
  - 只用了常数级别的额外变量（`max_val`、`max_idx`、循环计数器），不随输入规模增长。

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**第二次遍历里对每个元素都做了相同的乘法比较**，其实我们只需要**找出最大的数和第二大的数**，因为：

- 如果最大的数 `max_val` 能够“至少是其他所有数的两倍”，那么它一定也要满足 `max_val >= 2 * second_max`（第二大的数是所有非最大数里最大的那个）。  
- 只要检查这唯一的条件，就可以保证它对 **所有** 其余数都成立。  

因此，只需要 **一次遍历** 同时维护两位最大的数：

1. 初始化 `max_val = -1, second_max = -1, max_idx = -1`。  
2. 逐个读取 `num`：  
   - 如果 `num > max_val`，说明出现了更大的数，原来的 `max_val` 成为 `second_max`，当前 `num` 成为新的 `max_val`，并记录下标。  
   - 否则如果 `num > second_max`，更新 `second_max`（因为它比之前的第二大更大）。  
3. 循环结束后，只需要判断 `max_val >= 2 * second_max`。若成立返回 `max_idx`，否则返回 `-1`。  

这个思路只遍历一次数组，时间线性增长，空间仍然是常数。下面给出实现。

#### 代码（Python）  

```python
def dominantIndex(nums):
    """
    返回最大数的下标，如果它至少是其他数的两倍；否则返回 -1
    """
    max_val = -1          # 当前最大的数
    second_max = -1       # 第二大的数
    max_idx = -1          # 最大数所在的下标

    for i, num in enumerate(nums):
        if num > max_val:                 # 找到更大的数
            second_max = max_val          # 旧的最大数降为第二大
            max_val = num                 # 更新最大数
            max_idx = i                   # 记录下标
        elif num > second_max:            # 只比第二大大，不影响最大数
            second_max = num

    # 检查最大数是否至少是第二大的两倍
    if max_val >= 2 * second_max:
        return max_idx
    return -1
```

> **代码要点**  
> - `enumerate(nums)` 同时给出元素值和下标，类似于在货架上“一边拿商品，一边记下它的位置”。  
> - 当出现更大的数时，**原来的最大数**自然会变成**第二大数**，这一步把“字典”里的**旧条目**搬到了**新条目**的位置。  
> - 最后只比较一次 `max_val >= 2 * second_max`，相当于只检查一次“最大商品的重量是否是第二重商品的两倍”。  

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - “`n`” 表示我们只走了一遍数组，元素个数翻倍，耗时也只翻倍。相比暴力的 `n²`，规模稍大时速度提升非常明显。  
- **空间复杂度：** `O(1)`  
  - 只用了几个整型变量，和输入规模无关。  

---  

## 心得  

- **核心技巧**：一次遍历中维护**最大值**和**次大值**，再用次大值做唯一的判断。  
- **适用场景**：  
  1. “找出数组中是否存在某个元素满足对所有其它元素的某种关系”——例如 “是否有元素大于等于所有其它元素的两倍”。  
  2. “找出数组中第二大/第二小元素”，如 LeetCode 414 *Third Maximum Number*（只需要再维护第三大）。  
  3. “判断最大值是否唯一且满足某条件”，如 “数组中最大值是否超过所有其它值的 3 倍”。  
- **一句话总结解题钥匙**：**只关注最大和次大两个数，其他的都不必逐个检查**。  

---  

## 反思  

- **第一反应**：看到“最大数”和“至少是其他数的两倍”，第一时间想到**遍历比较**，甚至会写成双层循环。  
- **最容易踩的坑**  
  - **边界情况**：数组长度只有 2 时，次大数就是唯一的另一个数，仍然需要正确处理。  
  - **最大数唯一性**：题目已保证唯一，但若忘记这点，可能会在出现相同最大值时误判。  
  - **整数乘法溢出**：在 Python 中不必担心，但在某些语言里 `2 * x` 可能超出整数范围，需要使用长整型。  
- **下次类似题的第一步**：先**定位极值（最大/最小）**，再思考**是否只需要比较次极值**，从而把“所有元素”压缩成“关键的几位”。