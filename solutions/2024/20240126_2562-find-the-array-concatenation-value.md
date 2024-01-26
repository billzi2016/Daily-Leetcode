# #2562. 找出数组拼接值 / Find the Array Concatenation Value

> 难度：简单 · 标签：Array、Two Pointers、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-the-array-concatenation-value/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums.
The concatenation of two numbers is the number formed by concatenating their numerals.
The concatenation value of nums is initially equal to 0. Perform this operation until nums becomes empty:
Return the concatenation value of nums.

**Examples**

**Example 1:**

```
Input: nums = [7,52,2,4]
Output: 596
Explanation: Before performing any operation, nums is [7,52,2,4] and concatenation value is 0.
 - In the first operation:
We pick the first element, 7, and the last element, 4.
Their concatenation is 74, and we add it to the concatenation value, so it becomes equal to 74.
Then we delete them from nums, so nums becomes equal to [52,2].
 - In the second operation:
We pick the first element, 52, and the last element, 2.
Their concatenation is 522, and we add it to the concatenation value, so it becomes equal to 596.
Then we delete them from the nums, so nums becomes empty.
Since the concatenation value is 596 so the answer is 596.
```

**Example 2:**

```
Input: nums = [5,14,13,8,12]
Output: 673
Explanation: Before performing any operation, nums is [5,14,13,8,12] and concatenation value is 0.
 - In the first operation:
We pick the first element, 5, and the last element, 12.
Their concatenation is 512, and we add it to the concatenation value, so it becomes equal to 512.
Then we delete them from the nums, so nums becomes equal to [14,13,8].
 - In the second operation:
We pick the first element, 14, and the last element, 8.
Their concatenation is 148, and we add it to the concatenation value, so it becomes equal to 660.
Then we delete them from the nums, so nums becomes equal to [13].
 - In the third operation:
nums has only one element, so we pick 13 and add it to the concatenation value, so it becomes equal to 673.
Then we delete it from nums, so nums become empty.
Since the concatenation value is 673 so the answer is 673.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`。  
两个数字的拼接（concatenation）是指把它们的十进制表示按顺序连接形成的新数字。  
数组的拼接值（concatenation value）最初等于 `0`。重复以下操作直到 `nums` 为空：

1. 取数组的第一个元素和最后一个元素，计算它们的拼接，将得到的数字加到拼接值上，然后将这两个元素从数组中删除。  
2. 若此时数组只剩下一个元素，则直接把该元素加到拼接值上并删除它。

返回最终的拼接值。

示例

**示例 1**

```
Input: nums = [7,52,2,4]
Output: 596
Explanation: 
在进行任何操作前，nums 为 [7,52,2,4]，拼接值为 0。
- 第一次操作：取首元素 7 和尾元素 4，拼接得到 74，拼接值加上 74 变为 74。随后删除这两个元素，nums 变为 [52,2]。
- 第二次操作：取首元素 52 和尾元素 2，拼接得到 522，拼接值加上 522 变为 596。随后删除这两个元素，nums 为空。
最终返回拼接值 596。
```

**示例 2**

```
Input: nums = [5,14,13,8,12]
Output: 673
Explanation: 
在进行任何操作前，nums 为 [5,14,13,8,12]，拼接值为 0。
- 第一次操作：取首元素 5 和尾元素 12，拼接得到 512，拼接值加上 512 变为 512。随后删除这两个元素，nums 变为 [14,13,8]。
- 第二次操作：取首元素 14 和尾元素 8，拼接得到 148，拼接值加上 148 变为 660。随后删除这两个元素，nums 变为 [13]。
- 第三次操作：只剩下一个元素 13，直接加到拼接值上，得到 673。随后删除该元素，nums 为空。
最终返回拼接值 673。
```

**约束条件**

- `1 <= nums.length <= 1000`
- `1 <= nums[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**一步步模拟**题目描述的过程：

1. 取数组的第一个元素 `left`（下标 0），取最后一个元素 `right`（下标 `len-1`）。  
2. 把这两个数的十进制表示拼在一起得到一个新数 `concat`，例如 `7` 和 `4` 拼成 `74`。  
3. 把 `concat` 加到答案 `ans` 上。  
4. 把这两个元素从数组中删除，继续对剩下的数组重复上述步骤，直到数组为空。  

> **类比**：把数组想成一条排队的队伍，左边的同学和右边的同学每次手拉手离开，离开前把两个人的编号拼在一起记下来。  

实现时最“笨”的方式是直接用 `list.pop(0)` 删除左边的元素，再用 `list.pop()` 删除右边的元素。  
`pop(0)` 会把后面的所有元素往前搬一位，时间复杂度是 **O(n)**，在循环里会被执行 `n/2` 次，所以整体是 **O(n²)**。

拼接数字我们可以把整数转成字符串再拼接，再把结果转回整数，这样代码最直观。

#### 代码（Python）

```python
def findArrayConcatenationValue(nums: list[int]) -> int:
    ans = 0                         # 最终答案
    while nums:                     # 当数组不为空时循环
        left = nums.pop(0)          # 取并删除最左边的元素（O(n)）
        if nums:                    # 可能只剩下一个元素
            right = nums.pop()      # 取并删除最右边的元素（O(1)）
        else:
            right = None            # 只剩一个时，right 设为 None

        # 把 left 与 right 拼接成一个新数
        if right is not None:
            concat = int(str(left) + str(right))   # 字符串拼接后再转成整数
        else:                                      # 只剩下 left
            concat = left

        ans += concat                # 累加到答案
    return ans
```

> **关键行解释**  
> - `nums.pop(0)`: 删除最左边的元素，相当于把队伍最前面的同学让出来。  
> - `int(str(left) + str(right))`: 把两个整数先变成文字（比如 7 → "7"），再拼在一起得到 "74"，最后转回整数 74。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每一次 `pop(0)` 都要把后面的元素整体左移，最坏情况下要移动 `n/2 + n/2‑1 + … + 1 ≈ n²/4` 次。  
  - 用大白话说，就是**随着数组变长，删除左端的代价会迅速增长**。

- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了常数个额外变量 `ans、left、right、concat`。

---

### 2. 最优解

#### 思路  

上面的暴力解的**瓶颈**在于每次 `pop(0)` 的线性时间。  
我们可以把数组视为一根绳子，两端各有一个指针：

- `l` 指向左端（最左边），初始为 `0`。  
- `r` 指向右端（最右边），初始为 `len(nums) - 1`。  

每次循环：

1. 读取 `nums[l]` 与 `nums[r]`（不删除），用它们计算拼接值。  
2. `l` 向右移动一格，`r` 向左移动一格。  
3. 当 `l > r` 时说明已经遍历完所有元素。  

这样 **每个元素只被访问一次**，不需要真正删除，时间从 `O(n²)` 降到 `O(n)`。

拼接数字有两种实现方式：

- **字符串法**：`int(str(a) + str(b))`，代码简洁。  
- **数学法**：`a * 10^{digits(b)} + b`，不依赖字符串转换。  
这里为了让思路更直观，先用字符串法；随后给出数学法的实现，展示“更省空间/更快”的技巧。

> **类比**：把数组看成一根绳子，两只手从两端往中间握手，每握一次就记下两个人的编号拼接，手不需要把已经握过的人抛掉，只是把指针往里移动。

#### 代码（Python）

```python
def findArrayConcatenationValue(nums: list[int]) -> int:
    ans = 0
    l, r = 0, len(nums) - 1          # 左右指针

    while l <= r:                    # 只要左指针未越过右指针就继续
        if l == r:                    # 只剩一个元素时，只把它本身加入答案
            ans += nums[l]
            break

        # ----- 方式一：字符串拼接（最直观） -----
        concat = int(str(nums[l]) + str(nums[r]))
        # ----- 方式二：数学拼接（不使用字符串） -----
        # digits = len(str(nums[r]))               # 先算出右边数字有几位
        # concat = nums[l] * (10 ** digits) + nums[r]

        ans += concat
        l += 1                         # 左指针右移
        r -= 1                         # 右指针左移
    return ans
```

> **关键行解释**  
> - `while l <= r:`：当左指针刚好等于右指针时，说明数组长度为奇数，只剩下中间的那一个数，需要单独处理。  
> - `int(str(nums[l]) + str(nums[r]))`：把左边的数和右边的数的文字直接拼起来，再转成整数。  
> - `l += 1`、`r -= 1`：指针向中间靠拢，等价于“把已经使用的元素从队列中‘摘掉’”。  

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个元素恰好被访问一次，像走过一次绳子，从头走到尾。  

- **空间复杂度**：`O(1)`  
  - 只用了常数个变量（`ans、l、r、concat`），不依赖额外的数组或栈。

---

## 心得

- **核心技巧**：**双指针**（Two‑Pointers）模拟“从两端取元素”。  
- **适用题型**  
  1. **数组两端配对求和**（如 LeetCode 1679 “Max Number of K‑Sum Pairs”）。  
  2. **回文判断 / 双指针遍历**（如 LeetCode 125 “Valid Palindrome”）。  
  3. **数组合并 / 交叉遍历**（如 LeetCode 977 “Squares of a Sorted Array”）。  

> **一句话总结**：把数组想成一根绳子，用左手和右手交替抓取，两手相遇即结束。

---

## 反思

- **第一反应**：直接把题目描述写成循环，用 `pop(0)` 删除左端元素——这在小数据下能跑通，却忽视了时间开销。  
- **最容易踩的坑**  
  1. **奇数长度数组**：最后只剩一个元素时，不能再做拼接，需要把它本身加到答案。  
  2. **拼接方式的溢出**：在 Python 中整数是大整数，不会溢出，但在其他语言要注意 `10^{digits}` 可能超出 32 位整数范围。  
- **下次类似题的第一步**：先判断“是否需要真正删除元素”。如果只需要“顺序遍历两端”，立刻考虑 **双指针**，避免使用 `pop(0)` 之类的线性删除操作。