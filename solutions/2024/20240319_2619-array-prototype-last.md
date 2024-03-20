# #2619. 数组原型的 last 方法 / Array Prototype Last

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/array-prototype-last/)

---

## 题目（英文原版）

**Description**

Write code that enhances all arrays such that you can call the array.last() method on any array and it will return the last element. If there are no elements in the array, it should return -1.
You may assume the array is the output of JSON.parse.

**Examples**

**Example 1:**

```
Input: nums = [null, {}, 3]
Output: 3
Explanation: Calling nums.last() should return the last element: 3.
```

**Example 2:**

```
Input: nums = []
Output: -1
Explanation: Because there are no elements, return -1.
```

**Constraints**

- arr is a valid JSON array
- 0 <= arr.length <= 1000

---

## 题目（中文翻译）

编写代码，使所有数组都拥有 `array.last()` 方法，调用该方法时返回数组的最后一个元素。如果数组中没有元素，则返回 `-1`。可以假设输入的数组是 `JSON.parse` 的返回结果。

## 示例

### 示例 1
**输入**  
`nums = [null, {}, 3]`

**输出**  
`3`

**解释**  
调用 `nums.last()` 应返回最后一个元素：`3`。

### 示例 2
**输入**  
`nums = []`

**输出**  
`-1`

**解释**  
因为数组中没有元素，返回 `-1`。

## 约束条件
- `arr` 是合法的 JSON 数组  
- `0 <= arr.length <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是：**把 `last()` 当成普通的函数，进去把数组的长度 `len` 看一下**。  
- 如果长度为 `0`，说明数组里没有元素，直接返回 `-1`。  
- 否则返回数组最后一个位置的元素，即下标 `len-1` 处的值。  

这里用到的 **数据结构** 就是 Python 内置的 `list`（相当于生活中装东西的箱子）。  
- `list[i]` 就像在箱子里数第 `i+1` 个格子取东西。  
- `len(list)` 相当于数箱子里到底有多少格子。

为什么这个方法一定对？因为 **数组的最后一个元素的下标必然是 `长度-1`**，只要我们把长度算出来，就能定位到它。

#### 代码（Python）

```python
# 为所有 list 对象添加一个 last 方法（相当于在原型上挂一个函数）
def _list_last(self):
    """
    返回当前列表的最后一个元素；若列表为空返回 -1。
    这里的 `self` 就是调用该方法的那个列表本身，类似 JS 中的 this。
    """
    if len(self) == 0:          # 列表没有元素
        return -1
    return self[-1]             # Python 支持负索引，-1 正好是最后一个

# 把函数绑定到 list 类上，所有列表实例都会拥有这个方法
list.last = _list_last
```

> **使用示例**  
> ```python
> nums = [None, {}, 3]
> print(nums.last())   # 输出 3
> empty = []
> print(empty.last())  # 输出 -1
> ```

#### 复杂度

- **时间复杂度：O(1)** — 只做了常数次操作（判断长度、取一次元素），不随列表大小增长。  
- **空间复杂度：O(1)** — 只用了极少的额外变量（`self` 本身不算），不随列表大小变化。

---

### 2. 最优解

#### 思路  

从暴力解看，唯一的**瓶颈**其实已经不存在——我们已经只用了常数时间。  
因此“最优解”与“暴力解”在实现上是相同的，只是把思考过程写得更清晰：

1. **检查空列表**：`if not self:`（Python 里空容器会被当作 `False`）  
2. **返回最后一个元素**：`self[-1]`（负索引是 Python 的语法糖，直接取倒数第 1 项）  

核心技巧是 **负索引**——它让我们不必手动算 `len(self)-1`，代码更简洁，也避免了手算时可能的下标越界。

#### 代码（Python）

```python
def _list_last(self):
    """最简写法：直接利用 Python 的负索引特性"""
    return self[-1] if self else -1   # self 为 [] 时返回 -1，否则返回最后一个

list.last = _list_last
```

> **使用示例**  
> ```python
> nums = [None, {}, 3]
> print(nums.last())   # 3
> print([].last())     # -1
> ```

#### 复杂度

- **时间复杂度：O(1)** — 仍然只做一次判断和一次取值。  
- **空间复杂度：O(1)** — 只用了极少的临时变量。

---

## 心得

- **核心技巧**：利用列表的 `len`（或直接的 `if self`）判断是否为空，使用负索引 `-1` 快速取最后一个元素。  
- **适用的题型**：  
  1. “获取数组/列表的第 k 个元素” 类问题（如 LeetCode 1791. Find Center of Star Graph）  
  2. “判断数组是否为空并返回默认值” 类问题（如返回 0、`None`、`-1` 等）  
  3. “为现有数据结构扩展方法” 的语言特性练习（如 JavaScript 的原型、Python 的类/猴子补丁）  
- **一句话总结**：**空判断 + 负索引** 是读取列表最后一个元素的最简钥匙。

---

## 反思

- **第一反应**：看到 “在所有数组上都能调用 `last()`”，立刻想到要给 `list` 类添加一个方法（在 JS 里是 `Array.prototype`）。  
- **最容易踩的坑**：  
  - 忘记处理空列表，直接返回 `self[-1]` 会抛出 `IndexError`。  
  - 在 Python 中直接改动内置类型可能影响全局，实际项目中更安全的做法是自定义子类或包装函数。  
- **下次遇到同类题**：第一步先**判断是否为空**，再**使用负索引或 `len-1` 直接定位最后元素**。如果语言不支持负索引，`len(arr)-1` 是等价的通用写法。