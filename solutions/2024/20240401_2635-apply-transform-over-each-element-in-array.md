# #2635. 对数组的每个元素应用转换 / Apply Transform Over Each Element in Array

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/apply-transform-over-each-element-in-array/)

---

## 题目（英文原版）

**Description**

Given an integer array arr and a mapping function fn, return a new array with a transformation applied to each element.
The returned array should be created such that returnedArray[i] = fn(arr[i], i).
Please solve it without the built-in Array.map method.

**Examples**

**Example 1:**

```
Input: arr = [1,2,3], fn = function plusone(n) { return n + 1; }
Output: [2,3,4]
Explanation:
const newArray = map(arr, plusone); // [2,3,4]
The function increases each value in the array by one.
```

**Example 2:**

```
Input: arr = [1,2,3], fn = function plusI(n, i) { return n + i; }
Output: [1,3,5]
Explanation: The function increases each value by the index it resides in.
```

**Example 3:**

```
Input: arr = [10,20,30], fn = function constant() { return 42; }
Output: [42,42,42]
Explanation: The function always returns 42.
```

**Constraints**

- 0 <= arr.length <= 1000
- -109 <= arr[i] <= 109
- fn returns an integer.

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `arr` 和一个映射函数 `fn`，返回一个新数组，使每个元素都经过一次转换。  
返回的数组应满足 `returnedArray[i] = fn(arr[i], i)`。  
请在不使用内置的 `Array.map` 方法的前提下实现。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- `0 <= arr.length <= 1000`  
- `-10^9 <= arr[i] <= 10^9`  
- `fn` 返回一个整数  

**示例**  

**示例 1**  
```text
Input: arr = [1,2,3], fn = function plusone(n) { return n + 1; }
Output: [2,3,4]
```
**解释**：  
`const newArray = map(arr, plusone); // [2,3,4]`  
该函数把数组中的每个值都增加 1。

**示例 2**  
```text
Input: arr = [1,2,3], fn = function plusI(n, i) { return n + i; }
Output: [1,3,5]
```
**解释**：该函数把每个值增加其所在的索引 `i`。

**示例 3**  
```text
Input: arr = [10,20,30], fn = function constant() { return 42; }
Output: [42,42,42]
```
**解释**：该函数始终返回 42。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **遍历** 输入数组 `arr`，把每个元素交给给定的函数 `fn` 处理后，收集到一个新的数组里返回。  

- **遍历**：相当于我们把一排排的盒子（数组元素）一个一个搬出来，交给工匠（函数 `fn`）加工。  
- **收集**：把加工好的盒子依次放进一个新的箱子（返回数组）。  
- **数据结构**：这里只需要一个普通的 Python 列表 `result` 来存放结果。列表就像我们常用的“购物车”，可以不停地往里面 **append**（添加）东西。

这种做法之所以 **正确**，是因为题目明确要求 `returnedArray[i] = fn(arr[i], i)`，我们正是按顺序把每个 `arr[i]`（以及它的下标 `i`）交给 `fn`，并把返回值放到对应位置。

**时间/空间复杂度**  
- **时间复杂度**：我们要看每个元素都要处理一次，假设数组长度为 `n`，则总共执行 `n` 次函数调用和一次 `append`，所以是 **O(n)**。这里的 `O(n)` 可以想象成“走完一条长为 `n` 步的路”，步数跟 `n` 成正比。  
- **空间复杂度**：我们新建了一个长度为 `n` 的结果数组，额外占用了 **O(n)** 的空间（不算原始输入数组的空间）。这相当于我们搬了 `n` 个新盒子来装加工后的东西。

#### 代码（Python）

```python
def map_array(arr, fn):
    """
    把 arr 中的每个元素交给 fn 处理，返回新数组。
    fn 的签名是 fn(value, index) -> int
    """
    result = []                     # 用来收集结果的空列表
    for i, value in enumerate(arr): # 同时得到下标 i 和元素 value
        transformed = fn(value, i)  # 调用 fn，得到转换后的值
        result.append(transformed)  # 把转换后的值放进 result
    return result
```

#### 复杂度

- **时间复杂度**：`O(n)` — 随着数组长度 `n` 增大，执行的步骤数线性增长，就像走路一步步走完每个元素。  
- **空间复杂度**：`O(n)` — 需要额外存放 `n` 个结果，和输入规模成正比。

---

### 2. 最优解

#### 思路  

对于本题，**遍历一次** 已经是最好的时间复杂度了（因为每个元素必须至少被查看一次），因此不存在更快的算法。  
我们可以把代码写得更“Pythonic”，即利用 **列表推导式**（list comprehension）把循环和 `append` 合二为一，使代码更简洁、可读性更高。列表推导式本质上仍然是一次遍历，复杂度保持不变。

核心概念——**列表推导式**：把 “取值 → 处理 → 收集” 用一行表达出来。可以把它想象成一条装配线，所有的工作在同一条线上一次完成。

#### 代码（Python）

```python
def map_array(arr, fn):
    """
    使用列表推导式实现同样的功能。
    效果等同于上面的暴力实现，只是写法更简洁。
    """
    # 对每个元素 value（下标 i）调用 fn，直接生成新列表返回
    return [fn(value, i) for i, value in enumerate(arr)]
```

#### 复杂度

- **时间复杂度**：`O(n)` — 仍然只遍历一次数组。相比暴力解唯一的区别是代码行数更少，实际运行时间几乎相同。  
- **空间复杂度**：`O(n)` — 仍然需要创建一个同样大小的结果列表。

---

## 心得

- **核心技巧**：遍历（for/while）+ 调用函数 + 收集结果；在 Python 中常用 **列表推导式** 来“一行实现”。
- **适用的题型**  
  1. 将数组的每个元素做一次相同的转换（如 `平方数组`、`字符串转整数`）。  
  2. 根据下标对元素进行加工（如 “每个元素加上它的索引”）。  
  3. 需要把一个列表映射成另一个列表的场景（几乎所有 `map` 类题目）。
- **解题钥匙**：**一次遍历 + 直接生成新列表**。

## 反思

- **第一反应**：看到 “对每个元素做相同的事并返回新数组”，立刻想到 “遍历 + fn 调用”。  
- **最容易踩的坑**  
  - 忘记把下标 `i` 也传给 `fn`，导致某些需要索引的实现出错。  
  - 对空数组 `[]` 没有特殊处理，直接返回空列表即可。  
- **下次遇到同类题**：第一步先判断是否只需要一次遍历，如果是，立刻考虑使用列表推导式或普通 `for` 循环实现。这样可以保证时间最优且代码简洁。