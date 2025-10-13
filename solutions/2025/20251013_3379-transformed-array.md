# #3379. 变换数组 / Transformed Array

> 难度：简单 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/transformed-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums that represents a circular array. Your task is to create a new array result of the same size, following these rules:
Return the new array result.
Note: Since nums is circular, moving past the last element wraps around to the beginning, and moving before the first element wraps back to the end.

**Examples**

**Example 1:**

```
Input: nums = [3,-2,1,1]
Output: [1,1,1,3]
Explanation:
```

**Example 2:**

```
Input: nums = [-1,4,-1]
Output: [-1,-1,4]
Explanation:
```

**Constraints**

- 1 <= nums.length <= 100
- -100 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个整数数组 `nums`，它表示一个循环数组（circular array）。请你创建一个大小相同的新数组 `result`，满足题目给出的规则。返回新数组 `result`。  
**注意**：由于 `nums` 是循环的，移动到最后一个元素之后会回到开头，移动到第一个元素之前会回到末尾。

## 示例

### 示例 1
**输入**  
``` 
nums = [3,-2,1,1]
```  
**输出**  
```
[1,1,1,3]
```  
**解释**：

（此处填写示例 1 的解释）

### 示例 2
**输入**  
``` 
nums = [-1,4,-1]
```  
**输出**  
```
[-1,-1,4]
```  
**解释**：

（此处填写示例 2 的解释）

## 约束条件
- `1 <= nums.length <= 100`
- `-100 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求：**对每个位置 `i`，从 `i` 出发沿数组走 `nums[i]` 步（正数向右，负数向左），环形数组超出边界时会回到另一端，最后落在的位置的值就是 `result[i]`**。

最直接的想法是**一步一步地走**，就像在玩“跳格子”游戏：

1. 先记录数组长度 `n`（相当于围成一圈的格子数）。  
2. 对每个下标 `i`：  
   - 设 `steps = nums[i]` 为要走的步数。  
   - 用一个循环 `abs(steps)` 次，每次把当前位置加 1（向右）或减 1（向左），并在越界时把指针“搬”到另一端（`-1 → n-1`，`n → 0`）。  
   - 循环结束后得到的下标就是要取的元素，下标对应的值即为 `result[i]`。  

> **类比**：把 `nums` 看成一条环形跑道，`steps` 是跑步的步数。我们把跑步的每一步都写下来，最后落在哪个位置，就把那里的风景（数组值）记下来。

这个方法一定能得到正确答案，因为我们严格按照题目描述模拟了每一次移动。

#### 代码（Python）

```python
def transformArray(nums):
    n = len(nums)                     # 环形数组的长度
    result = [0] * n                  # 用来存放答案

    for i in range(n):                # 对每个起点 i
        steps = nums[i]               # 要走的步数（可能正也可能负）
        pos = i                       # 当前所在位置，先在起点

        # 按步数一步一步走
        if steps > 0:                 # 正数 → 向右
            for _ in range(steps):
                pos += 1              # 向右走一格
                if pos == n:          # 越界到数组末尾的下一格
                    pos = 0           # 环回到开头
        else:                         # 负数 → 向左
            for _ in range(-steps):
                pos -= 1              # 向左走一格
                if pos < 0:           # 越界到数组开头的前一格
                    pos = n - 1       # 环回到末尾

        result[i] = nums[pos]         # 落点的值写入答案

    return result
```

#### 复杂度

- **时间复杂度**：`O(n * |nums[i]|)`。最坏情况下每个 `nums[i]` 的绝对值都是 100，`n ≤ 100`，所以最多约 `10⁴` 次循环，仍然能接受。这里的 `O(n²)` 可以理解为“遍历了 `n` 次，每次又可能遍历 `n` 步”。  
- **空间复杂度**：`O(1)`（不计返回的 `result` 数组）。我们只用了常数个额外变量 `n、result、pos、steps`。

---

### 2. 最优解

#### 思路  

在暴力解里，**慢的地方**是“逐步移动”。实际上我们只需要知道**最终落在哪个下标**，不必一步步走。

- 环形数组的特性恰好可以用 **取模（mod）** 来一次性算出落点下标。  
- 对于下标 `i`，向右 `steps` 步相当于把 `i` 加上 `steps`，再对长度 `n` 取模：`(i + steps) % n`。  
- Python 的 `%` 运算符对负数也会返回非负余数（`-1 % n == n-1`），所以我们不必额外处理向左走的情况。

> **类比**：想象有 `n` 把椅子围成一圈，坐在第 `i` 把椅子上，往右走 `steps` 把椅子后直接数到第几把椅子就行了，不需要每一步都站起来数。

核心公式：

```
result[i] = nums[(i + nums[i]) % n]
```

只要一次遍历数组，就能得到全部答案。

#### 代码（Python）

```python
def transformArray(nums):
    n = len(nums)                     # 环形数组的长度
    result = [0] * n

    for i in range(n):
        # 计算落点下标：起点 i + 步数 nums[i]，对 n 取模得到环形效果
        target = (i + nums[i]) % n
        result[i] = nums[target]     # 落点的值写入答案

    return result
```

#### 复杂度

- **时间复杂度**：`O(n)`。只遍历一次数组，每个位置的计算都是 `O(1)`。相比暴力的逐步模拟，速度提升了数十倍（从 “每步走” 到 “一次算完”）。  
- **空间复杂度**：`O(1)`（不计返回的 `result`），只用了常数级别的临时变量 `n、target`。

---

## 心得

- **核心技巧**：利用取模 (`%`) 直接映射环形数组的下标，省去逐步模拟的过程。  
- **适用场景**：  
  1. **环形数组/链表的跳转**（如 LeetCode 1822 `Array Queries` 的循环访问）。  
  2. **旋转数组**（把数组右移 `k` 位可用 `(i - k) % n` 找到新下标）。  
  3. **循环队列**（实现 `front`、`rear` 指针时常用模运算）。  
- **一句话总结**：环形移动 → “一步到位” 用取模。

---

## 反思

- **第一反应**：把题目文字翻译成“每个位置走 `nums[i]` 步”，于是想到逐步模拟。  
- **最容易踩的坑**：  
  - **负数取模**：在某些语言（如 C++、Java）里负数 `%` 可能得到负数，需要手动 `(i + steps % n + n) % n`；在 Python 可以直接使用 `%`。  
  - **下标越界**：忘记对 `n` 取模会导致访问不存在的下标。  
- **下次思路**：遇到“环形”“循环”这类关键词，第一步就考虑 **取模**，把“走多少步”转化为“一次算出目标下标”。