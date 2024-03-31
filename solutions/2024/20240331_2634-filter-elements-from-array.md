# #2634. 过滤数组中的元素 / Filter Elements from Array

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/filter-elements-from-array/)

---

## 题目（英文原版）

**Description**

Given an integer array arr and a filtering function fn, return a filtered array filteredArr.
The fn function takes one or two arguments:
filteredArr should only contain the elements from the arr for which the expression fn(arr[i], i) evaluates to a truthy value. A truthy value is a value where Boolean(value) returns true.
Please solve it without the built-in Array.filter method.

**Examples**

**Example 1:**

```
Input: arr = [0,10,20,30], fn = function greaterThan10(n) { return n > 10; }
Output: [20,30]
Explanation:
const newArray = filter(arr, fn); // [20, 30]
The function filters out values that are not greater than 10
```

**Example 2:**

```
Input: arr = [1,2,3], fn = function firstIndex(n, i) { return i === 0; }
Output: [1]
Explanation:
fn can also accept the index of each element
In this case, the function removes elements not at index 0
```

**Example 3:**

```
Input: arr = [-2,-1,0,1,2], fn = function plusOne(n) { return n + 1 }
Output: [-2,0,1,2]
Explanation:
Falsey values such as 0 should be filtered out
```

**Constraints**

- 0 <= arr.length <= 1000
- -109 <= arr[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组 `arr` 和一个过滤函数 `fn`，返回一个过滤后的数组 `filteredArr`。  
`fn` 函数可以接受一个或两个参数：

- `fn(arr[i])`  
- `fn(arr[i], i)`

`filteredArr` 只应包含 `arr` 中使表达式 `fn(arr[i], i)` **求值为真值（truthy）** 的元素。**真值** 是指 `Boolean(value)` 返回 `true` 的值。

请在不使用内置的 `Array.filter` 方法的前提下实现该功能。

**示例 1**

```text
Input: arr = [0,10,20,30], fn = function greaterThan10(n) { return n > 10; }
Output: [20,30]
Explanation:
const newArray = filter(arr, fn); // [20, 30]
函数会过滤掉不大于 10 的值
```

**示例 2**

```text
Input: arr = [1,2,3], fn = function firstIndex(n, i) { return i === 0; }
Output: [1]
Explanation:
fn 也可以接受每个元素的索引 i
在本例中，函数会移除所有不在索引 0 处的元素
```

**示例 3**

```text
Input: arr = [-2,-1,0,1,2], fn = function plusOne(n) { return n + 1 }
Output: [-2,0,1,2]
Explanation:
值为 0 等假值（falsey）会被过滤掉
```

**约束条件**

- `0 <= arr.length <= 1000`
- `-10^9 <= arr[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是 **遍历原数组**，把每个元素交给给定的过滤函数 `fn`，判断它的返回值是否为 “真”。  
- **遍历** 用的是 Python 中最常见的 `for i, val in enumerate(arr)`，相当于我们在超市里一件件检查商品。  
- **过滤函数** `fn` 就像一个“检查员”，它会根据我们提供的规则（比如“大于 10”）返回 `True` 或 `False`（在 Python 中，非零、非空、非 `None` 的值都算 `True`，这叫 *truthy*）。  
- **把符合条件的元素放进新数组**，相当于把合格的商品装进购物篮。

只要遍历一次就能得到答案，这就是**暴力**（其实已经是最优）的方法。

#### 代码（Python）

```python
from typing import List, Callable
import inspect

def filter_array(arr: List[int], fn: Callable) -> List[int]:
    """
    用最直接的遍历方式实现过滤功能，不能使用 Python 内置的 filter。
    fn 可能只接受一个参数 (value) ，也可能接受两个参数 (value, index)。
    """
    result: List[int] = []                     # ① 新建一个空列表，用来装过滤后的元素
    # ② 检查 fn 需要几个参数，决定是只传值还是值+索引
    expects_index = len(inspect.signature(fn).parameters) == 2

    for idx, val in enumerate(arr):            # ③ 逐个遍历 arr，idx 是下标，val 是元素本身
        # ④ 调用 fn，得到一个“真假”值
        keep = fn(val, idx) if expects_index else fn(val)

        # ⑤ Python 中 bool(x) 会把 “truthy / falsy” 转成布尔值
        if bool(keep):                          # ⑥ 如果是 truthy，就把元素放进结果列表
            result.append(val)                  # ⑦ 关键操作：把符合条件的元素加入 result

    return result                               # ⑧ 返回过滤后的新数组
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  这里的 `n` 是数组长度。我们只遍历一次，每个元素都要调用一次 `fn`，所以时间随 `n` 成线性关系。  
  用大白话说，就是如果数组有 10 个元素，就要检查 10 次；100 个元素就要检查 100 次，检查次数和元素个数“成正比”。  

- **空间复杂度：** `O(n)`（最坏情况）  
  需要额外的列表来存放结果。最坏情况下所有元素都满足条件，结果列表和原数组等长，所以需要 `n` 个额外的存储单元。  

---

### 2. 最优解  

#### 思路  
对于这道“过滤数组”的题目，**没有比一次遍历更快的办法**，因为我们必须**看每一个元素**才能决定它是否应该留下。  
所以最优解其实就是把**暴力解写得更简洁**，常用的技巧是 **列表推导式**（list comprehension），它本质上仍然是一次遍历，只是写法更紧凑、可读性更高。  

- **核心点**：  
  1. 仍然需要遍历全部元素 → `O(n)` 已经是下界（下限），不可能再快。  
  2. 用列表推导式把“遍历 + 条件判断 + 加入结果”压在一行里，代码更易读。  

- **实现细节**：  
  与暴力解相同，我们仍然要判断 `fn` 的参数个数，以决定是否传入索引。  
  这里把判断 `bool(fn(...))` 放在列表推导式的 `if` 子句中。

#### 代码（Python）

```python
from typing import List, Callable
import inspect

def filter_array_opt(arr: List[int], fn: Callable) -> List[int]:
    """
    使用列表推导式实现同样的过滤功能，保持 O(n) 时间复杂度。
    """
    expects_index = len(inspect.signature(fn).parameters) == 2

    # 列表推导式：遍历 + 条件判断 + 自动收集满足条件的元素
    return [
        val
        for idx, val in enumerate(arr)                # 遍历每个元素和下标
        if bool(fn(val, idx) if expects_index else fn(val))   # 条件：fn 的返回值为 truthy
    ]
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  与暴力解相同，只是写法更紧凑。没有任何额外的循环或递归，仍然只检查一次每个元素。  

- **空间复杂度：** `O(n)`（最坏情况）  
  需要创建结果列表，最坏情况下和原数组等长。列表推导式本身在内部也会创建同样大小的列表，所以空间使用没有变化。  

---

## 心得  

- **核心技巧**：一次遍历 + “truthy” 判断（即 `bool()` 转换）。  
- **适用的题型**：  
  1. 任意需要根据条件挑选子集的题目，如 “删除数组中的特定元素”。  
  2. “统计满足条件的元素个数”——只需把 `append` 换成计数。  
  3. “对满足条件的元素进行映射后收集”——可以在列表推导式里加上 `map` 步骤。  
- **一句话总结**：遍历 + 条件判断是过滤的“钥匙”，只要每个元素都检查一次，就已经是最快的办法。  

## 反思  

- **第一反应**：直接想到遍历数组、调用 `fn`、把返回值为 `True` 的元素装进新列表。  
- **最容易踩的坑**：  
  - 忘记 `fn` 可能接受 **两个参数**（值和下标），导致调用错误。  
  - 对 “truthy / falsy” 理解不够，直接把返回值与 `True` 比较（`== True`），会把一些非布尔但为 truthy 的值（如 `2`、`[1]`）错误排除。  
  - 没考虑空数组的情况，应该直接返回空列表。  
- **下次第一步**：先确认过滤函数的签名（几参数），然后写一个最直接的遍历实现，确保所有元素都被检查一次。这样即使后面需要优化，也已经在正确的方向上了。