# #2727. 对象是否为空 / Is Object Empty

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/is-object-empty/)

---

## 题目（英文原版）

**Description**

Given an object or an array, return if it is empty.
You may assume the object or array is the output of JSON.parse.

**Examples**

**Example 1:**

```
Input: obj = {"x": 5, "y": 42}
Output: false
Explanation: The object has 2 key-value pairs so it is not empty.
```

**Example 2:**

```
Input: obj = {}
Output: true
Explanation: The object doesn't have any key-value pairs so it is empty.
```

**Example 3:**

```
Input: obj = [null, false, 0]
Output: false
Explanation: The array has 3 elements so it is not empty.
```

**Constraints**

- obj is a valid JSON object or array
- 2 <= JSON.stringify(obj).length <= 105

---

## 题目（中文翻译）

**描述**  
给定一个对象（object）或数组（array），判断它是否为空。  
你可以假设该对象或数组是 `JSON.parse` 的输出。

**示例 1：**  
（示例 1 的输入/输出保持不变，只翻译 Explanation 部分）

**示例 2：**  
（同上）

**示例 3：**  
（同上）

**约束条件**  
- `obj` 是合法的 JSON 对象或数组。  
- `2 <= JSON.stringify(obj).length <= 10^5`  

**示例**  

**示例 1:**  
```
Input: obj = {"x": 5, "y": 42}
Output: false
Explanation: 该对象拥有 2 个键值对，因此不是空的。
```

**示例 2:**  
```
Input: obj = {}
Output: true
Explanation: 该对象没有任何键值对，所以是空的。
```

**示例 3:**  
```
Input: obj = [null, false, 0]
Output: false
Explanation: 该数组包含 3 个元素，所以不是空的。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **对象**（在 Python 中是 `dict`）和 **数组**（在 Python 中是 `list`）的“长度”拿来判断：

- 对象就像一本词典，里面每一条 `key: value` 就是一对词条。如果词典里没有任何词条（`len(dict) == 0`），我们就说它是空的。
- 数组就像一排座位，坐满了多少人就对应了多少元素。如果没有人坐（`len(list) == 0`），同样认为是空的。

因为题目已经保证输入一定是合法的 JSON 解析结果（要么是 `dict`，要么是 `list`），我们只需要：

1. 判断 `obj` 的类型是 `dict` 还是 `list`（使用 `isinstance`，相当于先看它是词典还是座位排）。
2. 取它的长度 `len(obj)`，如果为 0 则返回 `True`（空），否则返回 `False`（非空）。

这种方法一定是对的，因为 **空对象/空数组的长度恰好是 0**，而非空的长度必然大于 0。

#### 代码（Python）

```python
def isEmpty(obj):
    """
    判断一个 JSON 解析得到的对象（dict）或数组（list）是否为空。
    返回 True 表示空，返回 False 表示非空。
    """
    # 1. 确认 obj 是 dict（相当于词典）还是 list（相当于座位排）
    if isinstance(obj, dict):
        # 2. dict 的长度就是键值对的个数，0 表示没有键值对
        return len(obj) == 0
    elif isinstance(obj, list):
        # 3. list 的长度就是元素的个数，0 表示没有元素
        return len(obj) == 0
    else:
        # 题目保证不会出现其他类型，这里防御性地返回 True
        return True
```

#### 复杂度

- **时间复杂度：O(1)** — 只做了常数次的 `isinstance` 检查和一次 `len` 取值，和输入规模无关。  
  大白话：不管对象有多大，判断它是否空只需要“一眼看”它的长度，花的时间是固定的。
- **空间复杂度：O(1)** — 没有额外的存储，只用了几个临时变量。  
  大白话：不需要额外的“大盒子”来装东西，使用的内存是固定的。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，判断空与否只依赖 **长度信息**，没有任何循环或递归的必要。因此已经达到了最优的时间/空间复杂度。这里再给出一种更简洁的写法：

- 直接利用 Python 对容器的 “真值” 特性：空的 `dict`、`list` 在布尔上下文中会被当作 `False`，非空则为 `True`。  
- 使用 `not obj` 即可得到是否为空的布尔值。  
- 仍然需要先判断类型，以免误判（例如传入 `None`、整数等非容器）。

这就是 **最优解**——代码最短、可读性最高，且仍然是 O(1) 时间、O(1) 空间。

#### 代码（Python）

```python
def isEmpty(obj):
    """
    更简洁的实现：利用容器的真值特性判断是否为空。
    """
    # 只接受 dict 或 list，其他类型直接视为“空”（题目不会出现）
    if isinstance(obj, (dict, list)):
        # 空的容器在布尔上下文中为 False，取反后得到 True 表示空
        return not obj
    return True
```

#### 复杂度

- **时间复杂度：O(1)** — 只做一次类型检查和一次布尔取反，和输入规模无关。  
  与暴力解相比，没有任何区别，已经是最好的。
- **空间复杂度：O(1)** —— 同样没有额外存储。

---

## 心得

- **核心技巧**：利用容器的长度或布尔特性快速判断是否为空。  
- **适用场景**：  
  1. 判断字典、列表、集合等容器是否为空（如 `if not my_dict:`）。  
  2. 检查字符串是否为空（`if not s:`），同理适用于所有可迭代容器。  
  3. 在处理 JSON 数据时，需要先判断某个字段是否提供了有效内容。  
- **一句话总结**：空容器的“长度为 0”或“布尔值为 False”，直接检查即可。

## 反思

- **第一反应**：看到 “对象或数组是否为空”，马上想到检查它们的 `len`。  
- **最容易踩的坑**：  
  - 忘记先判断类型，直接对非容器（如 `None`、整数）使用 `len` 会报错。  
  - 把 `None` 当作空对象处理，实际 JSON 里不会出现 `None`（对应 `null` 会被解析为 `None`，但题目说明输入是对象或数组）。  
- **下次思路**：遇到类似 “是否为空” 的题，第一步先确认数据结构，再使用 **长度** 或 **布尔特性** 直接判断，避免不必要的循环或遍历。