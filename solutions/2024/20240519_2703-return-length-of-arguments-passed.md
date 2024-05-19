# #2703. 返回传入参数的数量 / Return Length of Arguments Passed

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/return-length-of-arguments-passed/)

---

## 题目（英文原版）

**Description**



**Examples**

**Example 1:**

```
Input: args = [5]
Output: 1
Explanation:
argumentsLength(5); // 1

One value was passed to the function so it should return 1.
```

**Example 2:**

```
Input: args = [{}, null, "3"]
Output: 3
Explanation: 
argumentsLength({}, null, "3"); // 3

Three values were passed to the function so it should return 3.
```

**Constraints**

- args is a valid JSON array
- 0 <= args.length <= 100

---

## 题目（中文翻译）

**描述**  
给定一个 JSON 数组 `args`，它表示调用函数时传入的参数列表。请实现一个函数 `argumentsLength(...args)`，返回实际传入的参数个数，即 `args` 的长度。

**示例 1**  
输入: `args = [5]`  
输出: `1`  
**解释**:  
`argumentsLength(5); // 1`  

只有一个参数被传入函数，所以返回 `1`。

**示例 2**  
输入: `args = [{}, null, "3"]`  
输出: `3`  
**解释**:  
`argumentsLength({}, null, "3"); // 3`  

共传入了三个参数，所以返回 `3`。

**约束条件**  
- `args` 是一个有效的 JSON 数组。  
- `0 <= args.length <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是**逐个遍历**传进来的参数，把每一个都计数一次，最后把计数器的值返回。  
- 在 Python 中，函数的可变参数会被收集到一个 **元组**（`tuple`）里，类似于装有若干物品的盒子。  
- 我们可以把这个盒子想象成一本字典的书签：每翻一页（即遍历一个元素），计数器就加 1。  
- 只要把所有元素都走完，计数器的值就是参数的个数，这个方法一定是正确的，因为我们没有遗漏也没有多算。

#### 代码（Python）

```python
def argumentsLength(*args):
    """
    暴力计数版：手动遍历每一个参数并累计计数
    :param args: 可变参数，实际会被组织成一个 tuple
    :return: 参数的个数
    """
    count = 0                 # 初始化计数器
    for _ in args:            # 逐个遍历传进来的每个参数（下划线表示我们不关心具体值）
        count += 1            # 计数器加一
    return count              # 返回最终计数
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  这里的 `n` 表示传入的参数个数。我们需要遍历一次所有参数，所以时间会随参数数量线性增长。可以把 `O(n)` 想成“如果有 10 个参数，就需要大约 10 步；如果有 1000 个参数，就需要大约 1000 步”。  
- **空间复杂度**：`O(1)`  
  只用了一个整数变量 `count` 来保存计数，和参数个数无关，所占的额外内存是常数级别。

---

### 2. 最优解

#### 思路  
从暴力解可以看到，遍历每个元素只为了得到它们的数量。Python 已经帮我们实现了这个“计数器”——内置函数 `len()` 能够在 **常数时间**（对大多数实现来说）直接返回容器的长度。  

- **瓶颈**：在暴力解里我们显式遍历了一遍，虽然时间已经是线性的 `O(n)`，但仍然有额外的循环开销。  
- **优化**：直接调用 `len(args)`，让解释器自己去查表得到元素个数，代码更简洁，运行更快。  

这里涉及的核心概念只有 **内置函数 `len`**，它相当于一本字典的目录页码，直接告诉我们有多少条目，而不必逐页翻阅。

#### 代码（Python）

```python
def argumentsLength(*args):
    """
    最优解：直接使用 Python 内置的 len() 获取参数个数
    :param args: 可变参数，实际是一个 tuple
    :return: 参数的个数
    """
    return len(args)   # len() 能在 O(1) 时间返回元组的长度
```

#### 复杂度  

- **时间复杂度**：`O(1)`  
  `len()` 对元组（以及列表、字符串等）是常数时间操作，它只需要读取对象内部保存的长度字段。换句话说，不管你传进来多少参数，执行时间基本不变。  
- **空间复杂度**：`O(1)`  
  同样只使用了极少的额外空间（返回值本身），与参数个数无关。

---

## 心得

- **核心技巧**：利用语言提供的**直接查询容器大小**的函数（如 `len`），避免不必要的遍历。  
- **适用的题型**：  
  1. 求数组/列表的长度（如 LeetCode “Array Length After Removal”）  
  2. 判断字符串是否为空或获取字符数（如 “Length of Last Word”）  
  3. 统计集合/字典的元素个数（如 “Number of Good Pairs”）  
- **一句话总结**：**“有现成的 API，就别自己造轮子”。**

## 反思

- **第一反应**：看到“返回传入参数的个数”，第一时间想到遍历计数。  
- **最容易踩的坑**：  
  - 忘记使用可变参数 `*args`，导致函数只能接受固定数量的参数。  
  - 忽视空参数的情况（`args` 可能是空元组），需要确保返回 `0` 而不是抛异常。  
- **下次类似题的第一步**：先检查语言是否已经提供了“直接获取大小”的工具（`len`、`size`、`count` 等），若有则直接使用；若没有，再考虑手动遍历计数。