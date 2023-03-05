# #2154. **把找到的值不断乘以二** / Keep Multiplying Found Values by Two

> 难度：简单 · 标签：Array、Hash Table、Sorting、Simulation · [LeetCode 链接](https://leetcode.com/problems/keep-multiplying-found-values-by-two/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums. You are also given an integer original which is the first number that needs to be searched for in nums.
You then do the following steps:
Return the final value of original.

**Examples**

**Example 1:**

```
Input: nums = [5,3,6,1,12], original = 3
Output: 24
Explanation: 
- 3 is found in nums. 3 is multiplied by 2 to obtain 6.
- 6 is found in nums. 6 is multiplied by 2 to obtain 12.
- 12 is found in nums. 12 is multiplied by 2 to obtain 24.
- 24 is not found in nums. Thus, 24 is returned.
```

**Example 2:**

```
Input: nums = [2,7,9], original = 4
Output: 4
Explanation:
- 4 is not found in nums. Thus, 4 is returned.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i], original <= 1000

---

## 题目（中文翻译）

你得到一个整数数组 `nums`。另有一个整数 `original`，它是需要在 `nums` 中首先查找的数字。随后你重复以下操作：

- 若 `original` 在 `nums` 中出现，则将 `original` 乘以 2，得到新的 `original`；
- 重复上述过程，直到 `original` 不再出现在 `nums` 中。

返回最终得到的 `original`。

**示例 1**

```
Input: nums = [5,3,6,1,12], original = 3
Output: 24
```

**解释**  
- 3 在 `nums` 中出现，乘以 2 得到 6。  
- 6 在 `nums` 中出现，乘以 2 得到 12。  
- 12 在 `nums` 中出现，乘以 2 得到 24。  
- 24 不在 `nums` 中出现，结束并返回 24。

**示例 2**

```
Input: nums = [2,7,9], original = 4
Output: 4
```

**解释**  
- 4 未在 `nums` 中出现，直接返回 4。

**约束条件**

- `1 <= nums.length <= 1000`
- `1 <= nums[i], original <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一步一步模拟题目描述的过程**：

1. 先在数组 `nums` 中找有没有 `original`。  
2. 如果找到了，就把 `original` 乘以 2，得到新的值。  
3. 再次在 `nums` 中查找这个新值，重复上述步骤，直到在 `nums` 中找不到为止。  

这里唯一需要的数据结构是**数组本身**。把数组想象成一本书，**遍历查找**就像把书从头到尾翻一遍，看看某页上有没有我们想要的数字。  
只要每一步都能在数组里找到，就继续“翻书”，找不到就停下来返回当前的 `original`。

这个方法一定能得到正确答案，因为我们严格按照题目要求的“找‑乘‑再找”流程执行，没有遗漏任何一步。

**时间复杂度**  
每一次要判断 `original` 是否在 `nums` 中，都要遍历整个数组（最坏情况是遍历 `len(nums)` 次）。如果最终乘了 `k` 次才停下来，总共要做 `k` 次遍历，时间复杂度是 **O(k·n)**。在最坏情况下 `k` 可能接近 `log₂(1000)`（因为 `original` 和数组元素上限都是 1000），但这里我们把它记作 **O(n·m)**，其中 `m` 为乘法次数。对于本题的约束（`n ≤ 1000`），这仍然可以接受，但不是最优的。

**空间复杂度**  
只用了常数级别的额外变量（`original`、循环计数器等），所以是 **O(1)**。

#### 代码（Python）

```python
def findFinalValue(nums, original):
    """
    暴力版：每次都在数组里线性搜索 original 是否存在
    """
    n = len(nums)
    while True:
        found = False                     # 用来标记本轮是否找到了 original
        for i in range(n):                # 线性遍历整个数组
            if nums[i] == original:       # 找到了
                found = True
                break
        if not found:                     # 本轮遍历没有找到，直接返回
            return original
        original *= 2                     # 找到后把 original 翻倍，继续下一轮
```

#### 复杂度

- **时间复杂度：O(k·n)**  
  这里的 `k` 是乘以 2 的次数，`n` 是数组长度。可以理解为“每翻一次倍，就要把整本书从头翻一遍”。  
- **空间复杂度：O(1)**  
  只用了几个额外的整数变量，空间占用几乎为零。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈**在于每一次都要**遍历整个数组**来判断 `original` 是否存在。  
如果我们能够在 **常数时间**（O(1)）内判断一个数是否在 `nums` 中，就可以把总时间降低到只和乘法次数 `k` 成正比。

这正是 **哈希表（Python 中的 `set`）** 的强项：  
- `set` 可以看作一本“字典”，每个数字都是一个“单词”，对应的“页码”就是它是否出现。  
- 查询一个数字是否在集合里，只需要一次哈希运算，时间是 O(1)。

**步骤**：

1. 把 `nums` 转成 `set`，一次性完成 O(n) 的构造。  
2. 只要 `original` 在集合里，就把它乘以 2，继续循环。  
3. 当 `original` 不在集合里时，循环结束，返回当前值。

整个过程只涉及 **一次遍历**（把数组转成集合）和 **若干次 O(1) 的查询**，时间复杂度降到了 **O(n + k)**，而 `k` 在本题最多也只有 `log₂(1000) ≈ 10`，可以忽略不计。

#### 代码（Python）

```python
def findFinalValue(nums, original):
    """
    最优解：使用集合（哈希表）在 O(1) 时间内判断元素是否存在
    """
    values = set(nums)          # 把数组一次性放进集合，查询更快
    # 当 original 在集合中时，一直循环
    while original in values:   # O(1) 的“在不在”判断
        original *= 2           # 找到就翻倍
    return original
```

#### 复杂度

- **时间复杂度：O(n + k) ≈ O(n)**  
  先把数组转成集合需要 O(n)；随后每一次判断 `original in values` 只要 O(1)，乘法次数 `k` 最多约为 10，几乎可以忽略。  
  与暴力解相比，省掉了每次遍历数组的 `n` 次方操作，速度提升明显。

- **空间复杂度：O(n)**  
  需要额外存储一个集合，大小和原数组相同。可以把它想象成“把书的目录抄一遍”，占用的额外空间正好是原数组的大小。

---

## 心得

- **核心技巧**：利用哈希表（`set`）实现**快速存在性检查**。  
- **适用题型**：  
  1. “找不到就停止”的模拟类题目（如 *Find the Duplicate Number*、*First Missing Positive* 的变体）。  
  2. 需要**频繁判断一个元素是否出现**的题目（如 *Two Sum*、*Intersection of Two Arrays*）。  
- **一句话总结解题钥匙**：把“在数组里找”这一步改成 **O(1) 查表**，即可把暴力的 O(n·k) 降到 O(n)。

---

## 反思

- **第一反应**：直接把题目描述写成循环，逐次遍历数组查找。  
- **最容易踩的坑**：  
  - 忘记把 `original` 乘以 2 之后再继续检查，导致只检查一次。  
  - 对数组的查询使用了线性扫描，导致时间超限（虽然本题数据量不大，但养成好习惯很重要）。  
- **下次遇到同类题**，第一步应该思考**“这一步是否可以用哈希表/集合改写为 O(1”**，如果可以，就先把数据结构转换好，再进行模拟或循环。