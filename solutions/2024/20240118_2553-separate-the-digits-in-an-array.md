# #2553. 分离数组中的数字 / Separate the Digits in an Array

> 难度：简单 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/separate-the-digits-in-an-array/)

---

## 题目（英文原版）

**Description**

Given an array of positive integers nums, return an array answer that consists of the digits of each integer in nums after separating them in the same order they appear in nums.
To separate the digits of an integer is to get all the digits it has in the same order.

**Examples**

**Example 1:**

```
Input: nums = [13,25,83,77]
Output: [1,3,2,5,8,3,7,7]
Explanation: 
- The separation of 13 is [1,3].
- The separation of 25 is [2,5].
- The separation of 83 is [8,3].
- The separation of 77 is [7,7].
answer = [1,3,2,5,8,3,7,7]. Note that answer contains the separations in the same order.
```

**Example 2:**

```
Input: nums = [7,1,3,9]
Output: [7,1,3,9]
Explanation: The separation of each integer in nums is itself.
answer = [7,1,3,9].
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个由正整数（positive integer）构成的数组（array）`nums`，返回一个数组 `answer`，其中包含 `nums` 中每个整数的各位数字，且顺序与它们在 `nums` 中出现的顺序保持一致。

将整数的各位数字按原顺序取出，称为**分离**（separate）该整数的数字。

**示例 1**  
**输入**: `nums = [13,25,83,77]`  
**输出**: `[1,3,2,5,8,3,7,7]`  
**解释**:  
- 13 的分离结果为 `[1,3]`。  
- 25 的分离结果为 `[2,5]`。  
- 83 的分离结果为 `[8,3]`。  
- 77 的分离结果为 `[7,7]`。  
`answer = [1,3,2,5,8,3,7,7]`，注意 `answer` 按相同的顺序包含了所有分离结果。

**示例 2**  
**输入**: `nums = [7,1,3,9]`  
**输出**: `[7,1,3,9]`  
**解释**: 每个整数本身即为它的分离结果。  
`answer = [7,1,3,9]`。

**约束条件**  
- `1 <= nums.length <= 1000`  
- `1 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个整数当成“文字”，先把它变成字符串，再把字符一个一个取出来，转回整数加入答案数组。  

- **使用的数据结构**：  
  - **列表（list）**：就像装东西的盒子，`answer` 用来顺序存放所有拆出来的数字。  
  - **字符串（str）**：把数字“变成字”，每个字符对应一个数字位，就像把一本书的每一页翻出来读。  

- **为什么正确**：  
  把整数 `13` 变成字符串 `"13"`，再把字符 `'1'`、`'3'` 依次取出并转成整数 `1`、`3`，恰好就是把数字的每一位“拆开”。对数组里的每个数都这么做，按照原来的顺序把所有位拼在一起，就得到题目要求的答案。

- **复杂度分析（大白话）**：  
  - **时间**：我们要遍历所有数字的每一位。假设数组有 `n` 个数，每个数平均有 `d` 位，那么总共要看 `n·d` 次字符 → **O(n·d)**。如果把 `n·d` 看成“所有数字的总位数”，可以直接说 **O(totalDigits)**。  
  - **空间**：答案本身要保存所有位，需要 `n·d` 个整数 → **O(n·d)**。除了答案外，只用了常数级的临时变量 → **O(1)**（不计答案本身）。

#### 代码（Python）

```python
def separateDigits(nums):
    """
    把每个整数拆成单独的数字，保持出现顺序
    """
    answer = []                         # 用来装结果的列表
    for num in nums:                    # 逐个遍历原数组
        # 把整数转成字符串，例如 83 -> "83"
        for ch in str(num):             # 再逐字符遍历，顺序就是位的顺序
            answer.append(int(ch))      # 把字符再转成整数，加入答案
    return answer
```

#### 复杂度

- **时间复杂度**：`O(totalDigits)` — 实际上就是遍历所有数字的每一位一次，和输入规模线性相关。  
- **空间复杂度**：`O(totalDigits)` — 结果数组必须存放所有拆出的数字，除此之外只用了常数空间。

---

### 2. 最优解

#### 思路  

从暴力解看出瓶颈并不在时间上（已经是线性），而是在 **额外的字符串转换**。如果想省掉把整数变成字符串的开销，可以直接用数学运算把每一位取出来：

1. **先把数字倒着取**：对 `num` 使用 `% 10` 取最低位，再 `// 10` 去掉最低位，循环直到 `num` 为 `0`。这会得到 **倒序** 的位列表。  
2. **再翻转**：因为我们需要保持原来的顺序（高位在前），所以把倒序的列表反转一次。  
3. **直接放入答案**：把得到的位一次加入 `answer`。

这一步只用了整数除法和取模，完全在 **O(1)** 的额外空间内完成，每位仍然只处理一次，所以整体仍是线性时间，但省掉了字符串的创建和遍历，实际运行更快。

> **类比**：把数字看成一串珠子，`%10` 就像把最右边的珠子取下来，`//10` 把剩下的珠子往左推。取完后再把珠子按原来的顺序重新排好。

#### 代码（Python）

```python
def separateDigits(nums):
    """
    使用数学运算（取模、整除）把每个整数的各位数字拆开
    """
    answer = []                         # 最终结果列表
    for num in nums:                    # 逐个处理原数组
        if num == 0:                    # 特判 0，虽然题目保证正数，但写得更健壮
            answer.append(0)
            continue

        digits = []                     # 暂存当前数字的倒序位
        while num > 0:                  # 只要还有位就循环
            digits.append(num % 10)     # 取最低位
            num //= 10                  # 去掉最低位

        # digits 现在是倒序的，例如 83 -> [3,8]，需要翻转回正序
        answer.extend(reversed(digits))   # 直接把正序位加入答案
    return answer
```

#### 复杂度

- **时间复杂度**：`O(totalDigits)` — 每位数字只做一次取模、一次除法、一次插入，仍然是线性。相比暴力解，省掉了字符串的创建和遍历，常数因子更小。  
- **空间复杂度**：`O(totalDigits)` — 结果数组需要存放所有位；临时的 `digits` 列表最多保存当前数字的位数，最多 `log10(max(nums))`，即 **O(1)** 额外空间。

---

## 心得

- **核心技巧**：**逐位拆解**（利用字符串或数学取模），以及**保持顺序**（倒序后再翻转或直接使用字符串顺序）。  
- **适用的题型**：  
  1. “把整数的每一位单独处理”类题目，如 LeetCode 1837 *Sum of Digits in Base K*。  
  2. “数字转数组”类题目，如把电话号码拆成字符数组。  
  3. “按位比较”类题目，如判断两个数的每位是否相同。  
- **一句话总结**：**把数字视作“位的序列”，用取模/整除或字符串直接遍历即可轻松拆分**。

---

## 反思

- **第一反应**：把整数转成字符串，逐字符读取——最自然的做法。  
- **最容易踩的坑**：  
  - 忘记处理 `0`（虽然本题保证正数，但写通用代码时要考虑）。  
  - 直接把取模得到的倒序位加入答案，会导致顺序错误，需要再翻转。  
- **下次类似题的第一步**：先明确“是要正序还是倒序”。如果需要保持原顺序，最好先决定是用字符串（天然正序）还是数学方法（需要一次翻转）。这样可以避免后期顺序错误的调试。