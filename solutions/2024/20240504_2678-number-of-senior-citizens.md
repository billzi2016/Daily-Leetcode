# #2678. 老年乘客数量 / Number of Senior Citizens

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/number-of-senior-citizens/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of strings details. Each element of details provides information about a given passenger compressed into a string of length 15. The system is such that:
Return the number of passengers who are strictly more than 60 years old.

**Examples**

**Example 1:**

```
Input: details = ["7868190130M7522","5303914400F9211","9273338290F4010"]
Output: 2
Explanation: The passengers at indices 0, 1, and 2 have ages 75, 92, and 40. Thus, there are 2 people who are over 60 years old.
```

**Example 2:**

```
Input: details = ["1313579440F2036","2921522980M5644"]
Output: 0
Explanation: None of the passengers are older than 60.
```

**Constraints**

- 1 <= details.length <= 100
- details[i].length == 15
- details[i] consists of digits from '0' to '9'.
- details[i][10] is either 'M' or 'F' or 'O'.
- The phone numbers and seat numbers of the passengers are distinct.

---

## 题目（中文翻译）

你将得到一个 **0-indexed**（从 0 开始索引）的字符串数组 `details`。数组中的每个元素都是长度为 15 的压缩信息，记录了对应乘客的相关数据。  
返回年龄严格大于 60 岁的乘客数量。

**示例 1**  
**示例 2**  
**约束条件**：

- `1 <= details.length <= 100`
- `details[i].length == 15`
- `details[i]` 只包含字符 `'0'` 到 `'9'`（数字）。
- `details[i][10]` 为 `'M'`、`'F'` 或 `'O'`（性别标识）。
- 乘客的电话号码和座位号均不重复。

### 示例

**示例 1**  
**输入**: `details = ["7868190130M7522","5303914400F9211","9273338290F4010"]`  
**输出**: `2`  
**解释**: 索引为 0、1、2 的乘客年龄分别为 75、92、40。因此有 2 位乘客的年龄超过 60 岁。

**示例 2**  
**输入**: `details = ["1313579440F2036","2921522980M5644"]`  
**输出**: `0`  
**解释**: 没有乘客的年龄大于 60 岁。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是**把每个乘客的信息一条条读出来**，从中提取出年龄，然后判断是否大于 60，满足条件的就计数。  
- **数据结构**：这里我们只需要遍历原始的 `list`（数组），不需要额外的数据结构。  
- **年龄的提取**：题目说年龄是字符串第 11、12 位（下标 11、12），例如 `"7868190130M7522"`，取出字符 `'7'` 和 `'5'`，拼成 `"75"` 再转成整数 75。可以把这两位当成十位和个位，直接算 `age = int(s[11]) * 10 + int(s[12])`。  
- **正确性**：因为每条记录的格式都是固定的 15 位，且年龄一定在这两位上，逐条检查不会漏掉任何乘客，也不会误判。  

#### 代码（Python）

```python
def countSenior(details):
    """
    统计年龄严格大于 60 的乘客数量
    :param details: List[str]，每个元素长度固定为 15
    :return: int
    """
    senior_cnt = 0                     # 计数器，记录符合条件的乘客数
    for info in details:               # 逐条遍历
        # 取出第 11、12 位字符（下标 11、12），组成年龄
        # int(info[11]) 是十位，int(info[12]) 是个位
        age = int(info[11]) * 10 + int(info[12])
        if age > 60:                   # 判断是否大于 60
            senior_cnt += 1           # 符合则计数加一
    return senior_cnt
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  这里的 `n` 是 `details` 的长度（最多 100），我们只遍历一次，每次做常数时间的字符取值和整数运算。用大白话说，就是“随乘客人数线性增长”，乘客多了，时间就多线性多。
- **空间复杂度**：`O(1)`  
  只用了几个整数变量（计数器和临时的 `age`），不随输入规模增长。也就是说“几乎不占额外空间”。

---

### 2. 最优解

#### 思路  
在本题中，**暴力解已经是最优的**，因为我们必须检查每一条记录才能知道它的年龄。唯一可以改进的地方是**把代码写得更简洁**，比如使用列表推导式或 `sum` 配合布尔值直接计数。核心思想仍然是“一次遍历”。  
- **瓶颈**：遍历本身不可避免，时间已经是 `O(n)`，已经达到了下界。  
- **优化**：用 Python 的表达式把 “取年龄 → 判断 → 累计” 合并为一行，省去显式的计数器。  

#### 代码（Python）

```python
def countSenior(details):
    """
    使用简洁的写法，一行代码完成统计。
    sum 会把布尔值 True 当作 1，False 当作 0 相加，得到符合条件的数量。
    """
    return sum(
        (int(s[11]) * 10 + int(s[12]) > 60)   # 计算年龄并直接比较，返回 True/False
        for s in details                      # 生成式遍历每条记录
    )
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 与暴力解相同，只是写法更紧凑，实际执行的步骤没有减少。  
- **空间复杂度**：`O(1)` — 生成式是惰性的（lazy），不会一次性把所有结果存进列表，只在内部保持少量临时变量。

---

## 心得

- **核心技巧**：**字符串切片/索引 + 整数转换**，把固定位置的字符直接拼成数字。  
- **适用的题型**  
  1. “从固定格式的身份证/护照号码中提取出生年份、性别”等。  
  2. “根据日志行的固定列（如时间戳）进行统计”。  
  3. “从压缩的商品编码中读取数量或价格”。  
- **一句话总结解题钥匙**：**“定位 → 转换 → 判断”**，先定位到目标字符，再转成数字，最后比较计数。

## 反思

- **第一反应**：看到 “每条信息长度固定，年龄在第 11、12 位”，立刻想到遍历并直接取这两位算年龄。  
- **最容易踩的坑**  
  - 把下标弄错：有的同学会误把第 11 位写成 `details[i][10]`，导致年龄不正确。  
  - 忽略了“严格大于 60”，写成 `>= 60` 会把 60 岁算进去。  
  - 输入可能只有一条记录，确保循环能够处理最小规模。  
- **下次遇到同类题**：第一步先**确认信息的固定结构**，弄清每个字段所在的下标或切片范围，然后**直接取值并转换**，最后做所需的统计或比较。