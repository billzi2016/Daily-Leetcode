# #2705. 紧凑对象 / Compact Object

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/compact-object/)

---

## 题目（英文原版）

**Description**

Given an object or array obj, return a compact object.
A compact object is the same as the original object, except with keys containing falsy values removed. This operation applies to the object and any nested objects. Arrays are considered objects where the indices are keys. A value is considered falsy when Boolean(value) returns false.
You may assume the obj is the output of JSON.parse. In other words, it is valid JSON.

**Examples**

**Example 1:**

```
Input: obj = [null, 0, false, 1]
Output: [1]
Explanation: All falsy values have been removed from the array.
```

**Example 2:**

```
Input: obj = {"a": null, "b": [false, 1]}
Output: {"b": [1]}
Explanation: obj["a"] and obj["b"][0] had falsy values and were removed.
```

**Example 3:**

```
Input: obj = [null, 0, 5, [0], [false, 16]]
Output: [5, [], [16]]
Explanation: obj[0], obj[1], obj[3][0], and obj[4][0] were falsy and removed.
```

**Constraints**

- obj is a valid JSON object
- 2 <= JSON.stringify(obj).length <= 106

---

## 题目（中文翻译）

给定一个对象或数组 `obj`，返回其 **紧凑对象**（compact object）。  
紧凑对象 与原始对象相同，只是把值为 **假值**（falsy）的键全部移除。该操作会递归作用于对象本身以及所有嵌套的对象。数组在这里被视为键为下标的对象。 当 `Boolean(value)` 为 `false` 时，该值被认为是 **假值**。

可以假设 `obj` 是 `JSON.parse` 的输出，即它是合法的 JSON。

**示例 1**  
**示例 2**  
**示例 3**

**约束条件**

- `obj` 是合法的 JSON 对象  
- `2 <= JSON.stringify(obj).length <= 10^6`

---

### 示例

**示例 1**  
**输入**: `obj = [null, 0, false, 1]`  
**输出**: `[1]`  
**解释**: 所有假值都已从数组中移除。

**示例 2**  
**输入**: `obj = {"a": null, "b": [false, 1]}`  
**输出**: `{"b": [1]}`  
**解释**: `obj["a"]` 与 `obj["b"][0]` 的值为假值，已被删除。

**示例 3**  
**输入**: `obj = [null, 0, 5, [0], [false, 16]]`  
**输出**: `[5, [], [16]]`  
**解释**: `obj[0]、obj[1]、obj[3][0]、obj[4][0]` 均为假值，已被移除。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把对象（或数组）全部走一遍**，把每一个键对应的值检查一遍：

1. **遍历**：如果当前是 `dict`（相当于我们生活中的字典），就遍历它的每个 `key → value`；如果是 `list`（相当于一排编号的盒子），就遍历它的每个下标 `i → value`。  
2. **判断真假**：Python 中 `bool(value)` 为 `False` 的叫 **Falsy**，包括 `None、0、0.0、""、False、[]、{}` 等。只要 `bool(value)` 为 `False`，就把这个键（或下标）删掉。  
3. **递归**：如果 `value` 本身又是 `dict` 或 `list`，说明它是“嵌套的对象”。此时需要 **递归** 继续对它进行相同的处理，直到最内部的普通值为止。  

> **类比**：把 `dict` 想成一本字典，`key` 就是单词，`value` 是解释。我们要把所有解释是“空白”（Falsy）的单词删掉。`list` 则像一排编号的盒子，盒子里装的东西如果是空的也要扔掉。  

这样做一定能得到题目要求的 **compact object**，因为我们遍历了所有键并把所有 falsy 的键删掉了。

#### 代码（Python）

```python
def compact(obj):
    """
    递归地删除 dict / list 中所有 falsy 值对应的键或下标
    返回一个全新的结构（不修改原来的 obj）
    """
    # 如果是字典，逐键检查
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            # 先递归处理子结构，得到“紧凑”后的值
            compacted_v = compact(v)
            # 只有当紧凑后的值本身为 truthy 时才保留
            if compacted_v:
                new_dict[k] = compacted_v
        return new_dict

    # 如果是列表，逐下标检查
    if isinstance(obj, list):
        new_list = []
        for item in obj:
            compacted_item = compact(item)
            if compacted_item:
                new_list.append(compacted_item)
        return new_list

    # 基本类型（数字、字符串、布尔等），直接返回
    # Python 中 bool(value) 为 False 的会在外层被过滤
    return obj
```

**关键行中文注释说明**  
- `isinstance(obj, dict) / isinstance(obj, list)`：判断当前对象的类型。  
- `compact(v)`：递归调用，把子对象也压缩。  
- `if compacted_v:`：只有子对象压缩后仍然是 **truthy**（即不为 `False、0、[]、{}` 等）才放进新容器。  

#### 复杂度  

- **时间复杂度**：`O(N)` —— 这里的 `N` 是输入 JSON 中所有键（包括数组下标）的总数。我们只需要访问每个元素一次，就像把一本书的每页都读一遍。  
- **空间复杂度**：`O(N)` —— 因为我们 **新建** 了一个与原结构大小相同的结果对象（最坏情况所有值都是 truthy），所以额外占用的空间与输入大小成正比。递归调用栈的深度最多等于 JSON 的最大嵌套层数，也算在 `O(N)` 里。

---

### 2. 最优解

#### 思路  

上面的“暴力”解法已经是 **线性时间**，几乎没有可以再快的空间了。不过它 **复制** 了整棵树（即新建了 `new_dict`、`new_list`），导致额外的 `O(N)` 空间。  
如果 **可以原地修改**（in‑place），则只需要 **常数级的额外空间**（递归栈之外），因为我们直接在原来的对象上删除 falsy 元素。

**优化点**：

1. **在原对象上删除**：当遍历到 `dict` 时，用 `del` 删除不需要的键；遍历 `list` 时，用 `list.pop(i)` 或列表推导式直接过滤。  
2. **保持递归的深度**：递归本身仍需要栈空间，最坏情况是 JSON 完全线性嵌套（如 `[[[[...]]]`），栈深度为 `O(H)`，其中 `H` 为嵌套层数。题目约束 `JSON.stringify(obj).length ≤ 10⁶`，所以递归深度一般在几千以内，Python 默认递归深度（约 1000）可能需要 `sys.setrecursionlimit` 调高。  
3. **返回原对象**：函数返回值仍是处理后的对象，便于链式调用。

> **类比**：把一本字典当成一本可以擦写的笔记本，直接把空白的词条用橡皮擦掉，而不是把整个字典抄写一遍再删。这样省下了纸张（内存）。

#### 代码（Python）

```python
import sys
sys.setrecursionlimit(10 ** 6)   # 防止极深的递归导致 RuntimeError

def compact_inplace(obj):
    """
    在原地（in‑place）删除 dict / list 中所有 falsy 值对应的键或下标。
    返回处理后的 obj 本身，方便直接使用。
    """
    # 处理字典
    if isinstance(obj, dict):
        # 先收集需要删除的键，不能边遍历边删（会导致运行时错误）
        keys_to_delete = []
        for k, v in obj.items():
            # 递归压缩子结构
            compacted_v = compact_inplace(v)
            # 如果子结构本身是 falsy，则标记删除
            if not compacted_v:
                keys_to_delete.append(k)
            else:
                # 否则把压缩后的子结构写回原位置
                obj[k] = compacted_v
        # 真正删除
        for k in keys_to_delete:
            del obj[k]
        return obj

    # 处理列表
    if isinstance(obj, list):
        i = 0
        while i < len(obj):
            compacted_item = compact_inplace(obj[i])
            if not compacted_item:
                # 删除当前下标对应的元素，列表会自动左移
                obj.pop(i)
            else:
                # 用压缩后的值覆盖原位置
                obj[i] = compacted_item
                i += 1
        return obj

    # 基本类型直接返回（在外层会判断 truthiness）
    return obj
```

**关键行中文注释说明**  
- `keys_to_delete`：先收集要删的键，避免在遍历 `dict` 时直接 `del` 抛异常。  
- `if not compacted_v:`：判断子结构是否为 falsy（`bool(compacted_v) == False`），若是则准备删除。  
- `while i < len(obj):`：遍历列表时使用 `while`，因为 `pop` 会改变列表长度。  
- `obj.pop(i)`：直接把 falsy 元素从原列表中移除。  

#### 复杂度  

- **时间复杂度**：`O(N)` —— 每个元素仍然只被访问一次，和暴力解相同。  
- **空间复杂度**：`O(H)` —— 只需要递归栈的深度 `H`（最大嵌套层数），不再额外复制整个结构。相对于暴力解的 `O(N)`，这是显著的节省。  

---

## 心得

- **核心技巧**：**递归遍历** 任意嵌套的 JSON 结构，并在遍历过程中 **原地删除** falsy 元素。  
- **适用的题型**  
  1. 删除 JSON / 树结构中满足某种条件的节点（如 LeetCode 1129. Shortest Path with Alternating Colors 中的 BFS 剪枝）。  
  2. “清理” 嵌套数据结构的题目，例如把嵌套列表中所有 `null`/`None` 移除（类似 1137. N-th Tribonacci Number 的 DP 清理思路）。  
  3. 把对象/数组压缩成只保留 “有效” 信息的题目（如 1450. Number of Students Doing Homework at a Given Time）。  
- **一句话总结解题钥匙**：**递归 + 原地过滤**，先把子结构压缩好，再决定是否保留当前键/下标。

---

## 反思

- **第一反应**：看到“对象或数组，递归删除 falsy”，立刻想到 **深度优先遍历**，因为只有遍历到最底层才能判断真假。  
- **最容易踩的坑**  
  1. **遍历时直接删除**：对 `dict` 用 `for k in obj:` 再 `del obj[k]` 会报 `RuntimeError`（字典大小变化），必须先收集要删的键。  
  2. **列表下标变化**：删除元素后后面的元素会左移，若使用 `for item in lst:` 再 `pop` 会导致跳过元素，需要使用 `while` 或倒序遍历。  
  3. **递归深度**：极深的嵌套会触发 Python 的递归限制，需要手动 `sys.setrecursionlimit`。  
- **下次遇到同类题**：第一步想到 **“先递归处理子结构，再根据子结构的真假决定是否保留当前节点”**，这一步几乎适用于所有需要“自底向上”清理的嵌套结构题目。