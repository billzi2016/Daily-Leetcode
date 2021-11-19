# #1558. 最少函数调用次数使数组达到目标值 / Minimum Numbers of Function Calls to Make Target Array

> 难度：中等 · 标签：Array、Greedy、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/minimum-numbers-of-function-calls-to-make-target-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. You have an integer array arr of the same length with all values set to 0 initially. You also have the following modify function:
You want to use the modify function to convert arr to nums using the minimum number of calls.
Return the minimum number of function calls to make nums from arr.
The test cases are generated so that the answer fits in a 32-bit signed integer.

**Examples**

**Example 1:**

```
Input: nums = [1,5]
Output: 5
Explanation: Increment by 1 (second element): [0, 0] to get [0, 1] (1 operation).
Double all the elements: [0, 1] -> [0, 2] -> [0, 4] (2 operations).
Increment by 1 (both elements)  [0, 4] -> [1, 4] -> [1, 5] (2 operations).
Total of operations: 1 + 2 + 2 = 5.
```

**Example 2:**

```
Input: nums = [2,2]
Output: 3
Explanation: Increment by 1 (both elements) [0, 0] -> [0, 1] -> [1, 1] (2 operations).
Double all the elements: [1, 1] -> [2, 2] (1 operation).
Total of operations: 2 + 1 = 3.
```

**Example 3:**

```
Input: nums = [4,2,5]
Output: 6
Explanation: (initial)[0,0,0] -> [1,0,0] -> [1,0,1] -> [2,0,2] -> [2,1,2] -> [4,2,4] -> [4,2,5](nums).
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums`。另有一个长度相同、初始全部为 `0` 的整数数组 `arr`。你可以使用以下 **modify** 函数对 `arr` 进行操作：

1. **Increment**：将 `arr` 中任意一个元素加 `1`（一次只能作用于单个位置）。  
2. **Double**：将 `arr` 中所有元素同时乘以 `2`。

请使用上述操作将 `arr` 转换为 `nums`，并使函数调用次数最少。返回将 `arr` 变为 `nums` 所需的最小调用次数。  

题目保证答案能够放入 32 位有符号整数。

### 示例

**示例 1**  
```text
Input: nums = [1,5]
Output: 5
Explanation:  
- Increment 第 2 个元素一次： [0,0] → [0,1] （1 次操作）  
- Double 所有元素两次： [0,1] → [0,2] → [0,4] （2 次操作）  
- Increment 两个元素各一次： [0,4] → [1,4] → [1,5] （2 次操作）  
总计 1 + 2 + 2 = 5 次操作。
```

**示例 2**  
```text
Input: nums = [2,2]
Output: 3
Explanation:  
- Increment 两个元素各一次： [0,0] → [0,1] → [1,1] （2 次操作）  
- Double 所有元素一次： [1,1] → [2,2] （1 次操作）  
总计 2 + 1 = 3 次操作。
```

**示例 3**  
```text
Input: nums = [4,2,5]
Output: 6
Explanation:  
[0,0,0] → [1,0,0] → [1,0,1] → [2,0,2] → [2,1,2] → [4,2,4] → [4,2,5]（即 nums）。
```

### 约束条件

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **只使用“把选中的元素加 1”** 这一个操作，把 `arr` 从全 0 逐个递增到目标 `nums`。  
- **使用的数据结构**：只需要遍历一次数组 `nums`，不需要额外的容器。  
- **为什么能得到正确答案**：因为每一次“加 1”都把某个位置的值提升 1，反复操作足够多次后必然能把 0 变成任意非负整数。  
- **时间/空间复杂度的大白话**：  
  - 时间复杂度记作 **O(∑nums[i])**，意思是如果所有目标数加在一起是 1000，就要做 1000 次加法。对大数据来说，这个数字会非常大，甚至会超出 32 位整数的范围。  
  - 空间复杂度记作 **O(1)**，只用了常数级的额外空间（几个计数器），不随输入大小增长。

显然，这种做法在 `nums[i]` 可能高达 `10⁹` 时会非常慢，根本不可接受。

#### 代码（Python）

```python
def min_operations_bruteforce(nums):
    """
    只用“加 1”操作的暴力实现。
    统计把 0 加到每个 nums[i] 所需要的次数之和。
    """
    ops = 0                     # 记录总操作次数
    for v in nums:              # 遍历每个目标数
        ops += v                # 每个 1 需要一次加法
    return ops
```

#### 复杂度  

- **时间复杂度**：O(∑nums[i]) — 需要对每个目标数的每一个单位都做一次加法，想象成“走了 ∑nums[i] 步”。  
- **空间复杂度**：O(1) — 只用了几个整数计数器，和数组长度无关。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**只加 1** 当然能得到答案，但太慢了。  
观察例子会发现，**把所有元素一次性翻倍**（乘 2）可以一次性把每个数的二进制左移一位，这相当于一次性把所有数的“高位”一起提升。  

**关键观察**  

- 对任意正整数，它的二进制表示里每个 `1` 必须对应一次“加 1”操作（因为翻倍只能把已有的 0/1 向左移动，不能产生新的 1）。  
- 所有数的最高位出现的次数决定了需要多少次“整体翻倍”。换句话说，只要把所有数 **尽可能多地除以 2**（即向右移动二进制），每除一次就对应一次“翻倍”操作。  

**把问题倒着思考**  

从 `arr = [0,…,0]` 正向构造很难直接判断何时该翻倍。  
如果我们 **从目标 `nums` 逆向回到全 0**，每一步都很明确：

1. **如果某个数是奇数**，说明最后一次操作一定是对它执行了 “加 1”。于是我们把它减 1（对应一次加法计数）。  
2. **当所有数都是偶数**，说明上一轮一定是一次 “整体翻倍”。于是我们把所有数除以 2（对应一次翻倍计数）。  

不断循环上述两步，最终所有数都会变成 0。计数的总和就是最少的函数调用次数。

**为什么这就是最优**  

- 每次我们只能在 **所有数都是偶数** 时才进行除 2（翻倍），否则再除会产生小数，违背题意。  
- 对每个奇数我们只能选择 “减 1” 而不是 “先除再减”，因为除法只能在全部为偶数时进行。  
- 这两条规则形成了唯一的逆向路径，因而计数必然是最小的。  

**核心算法**：  
- **贪心**：每一步都做“显然必须做的事”。  
- **位运算**：判断奇偶可以用 `num & 1`，除以 2 用右移 `num >>= 1`，这在 Python 中同样适用。

**类比**：把每个数想成一串灯泡（0/1），我们只能一次性把所有灯泡向左移动（翻倍），或者单独把某盏灯点亮（加 1）。倒着思考时，就是先把点亮的灯泡关掉（减 1），然后把整串灯泡向右收拢（除 2），直至全灭。

#### 代码（Python）

```python
def min_operations(nums):
    """
    逆向贪心：从 nums 回到全 0。
    返回最少的函数调用次数。
    """
    ops = 0                     # 总操作次数
    # 只要还有任意一个数大于 0，就继续循环
    while any(num > 0 for num in nums):
        # 1）处理所有奇数：对应一次 “加 1” 操作
        for i in range(len(nums)):
            if nums[i] & 1:     # 判断奇偶，等价于 nums[i] % 2 == 1
                nums[i] -= 1
                ops += 1        # 记录一次加法

        # 2）如果此时所有数都是偶数且仍有正数，执行一次 “整体翻倍”
        if any(num > 0 for num in nums):
            # 把每个数右移一位，即除以 2
            for i in range(len(nums)):
                nums[i] >>= 1   # 等价于 nums[i] //= 2
            ops += 1            # 记录一次翻倍
    return ops
```

> **代码要点注释**  
> - `any(num > 0 for num in nums)` 用来判断是否还有未归零的元素。  
> - `num & 1` 是位运算，速度比 `% 2` 更快。  
> - `num >>= 1` 直接把二进制右移一位，相当于整除 2，省去了除法的额外开销。

#### 复杂度  

- **时间复杂度**：O(n · log M)  
  - `M = max(nums)` 是数组中最大的数。每次循环要遍历整个数组一次，循环次数等于该最大数的二进制位数（即 `log₂ M + 1`），因为每次都把所有数右移一位。  
  - 用大白话说，就是“每个元素最多被看 `log₂ 最大值` 次”。即使 `M` 达到 `10⁹`，`log₂ M` 也只有约 30 次，完全可接受。  

- **空间复杂度**：O(1)  
  - 只使用了常数个额外变量（计数器和循环索引），不随 `n` 增长。

---

## 心得  

- **核心技巧**：**倒推 + 贪心 + 位运算**。先把目标数倒着变成 0，每次只能做“必然的减 1”或“必然的除 2”。  
- **适用的题型**  
  1. “把所有数变成 0，只能减 1 或除以 2” 类似题（LeetCode 1342 – Number of Steps to Reduce a Number to Zero）。  
  2. “把数组全变成目标，只能整体翻倍或局部加 1” 的变形（如 1559 – Minimum Operations to Make Array Empty）。  
- **一句话总结**：**把加法和翻倍的顺序倒着执行，奇数先减、全部偶数再除，计数即最少操作数**。

---

## 反思  

- **第一反应**：直接想 “把每个数单独加到目标”，于是想到暴力的 `∑nums[i]` 次加法。  
- **最容易踩的坑**  
  - 忽略了 **整体翻倍** 的强大作用，以为只能对单个元素加 1，导致时间爆炸。  
  - 在倒推时忘记检查“所有数都是偶数”才可以除以 2，导致错误的除法路径。  
- **下次遇到同类题**：第一步先 **思考逆向**（从目标倒回起点），判断哪些操作是“必须”的，然后用 **贪心** 把这些必须的操作一步步执行。这样往往能直接得到最优解。