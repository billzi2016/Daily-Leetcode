# #2649. 嵌套数组生成器 / Nested Array Generator

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/nested-array-generator/)

---

## 题目（英文原版）

**Description**

Given a multi-dimensional array of integers, return a generator object which yields integers in the same order as inorder traversal.
A multi-dimensional array is a recursive data structure that contains both integers and other multi-dimensional arrays.
inorder traversal iterates over each array from left to right, yielding any integers it encounters or applying inorder traversal to any arrays it encounters.

**Examples**

**Example 1:**

```
Input: arr = [[[6]],[1,3],[]]
Output: [6,1,3]
Explanation:
const generator = inorderTraversal(arr);
generator.next().value; // 6
generator.next().value; // 1
generator.next().value; // 3
generator.next().done; // true
```

**Example 2:**

```
Input: arr = []
Output: []
Explanation: There are no integers so the generator doesn't yield anything.
```

**Constraints**

- 0 <= arr.flat().length <= 105
- 0 <= arr.flat()[i] <= 105
- maxNestingDepth <= 105

---

## 题目（中文翻译）

描述  
给定一个 **多维数组（multi-dimensional array）**（其中的元素可以是整数，也可以是其他多维数组），返回一个 **生成器对象（generator）**，该对象按照 **中序遍历（inorder traversal）** 的顺序产生整数。  

- **多维数组** 是一种递归数据结构，既可以包含整数，又可以包含其他多维数组。  
- **中序遍历** 按照从左到右的顺序遍历每个数组：  
  - 遇到整数时直接产出（yield）该整数；  
  - 遇到子数组时递归地对该子数组执行 **中序遍历**。  

示例  

**示例 1**  
```text
Input: arr = [[[6]],[1,3],[]]
Output: [6,1,3]
Explanation:
const generator = inorderTraversal(arr);
generator.next().value; // 6
generator.next().value; // 1
generator.next().value; // 3
generator.next().done; // true
```

**示例 2**  
```text
Input: arr = []
Output: []
Explanation: 没有整数可遍历，生成器不会产出任何值。
```

约束条件  
- `0 <= arr.flat().length <= 10^5`  
- `0 <= arr.flat()[i] <= 10^5`  
- `maxNestingDepth <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是 **先把所有整数全部取出来放进一个列表**，再把列表里的元素一个一个 `yield`。  
实现步骤如下：

1. 用递归遍历整个多维数组。  
2. 每次遇到 **整数** 就把它 `append` 到一个普通的 Python 列表 `flat` 中。  
3. 每次遇到 **子数组** 就递归地继续遍历它。  
4. 递归结束后，`flat` 已经是所有整数按照 “左→右” 顺序排好的扁平列表。  
5. 在生成器函数里遍历 `flat`，`yield` 每个元素。

> **类比**：把多维数组想象成一本有目录的书，目录里还有子目录。暴力做法就是先把所有章节标题抄写到一张纸上（`flat`），再按顺序朗读纸上的内容。

这种方法 **一定能得到正确的顺序**，因为我们严格按照“先左后右”的深度优先顺序把整数收集进列表。

#### 代码（Python）

```python
def inorder_traversal_brute(arr):
    """
    暴力版：先把所有整数放进列表 flat，然后逐个 yield。
    """
    flat = []                     # 用来保存遍历得到的所有整数

    def dfs(sub):
        """深度优先遍历 sub（可能是整数或列表）"""
        if isinstance(sub, int):
            flat.append(sub)      # 遇到整数就加入 flat
        else:                     # sub 是列表
            for item in sub:      # 从左到右依次处理子元素
                dfs(item)

    dfs(arr)                      # 从根节点开始遍历

    # 生成器：把 flat 里的元素一个一个 yield
    for num in flat:
        yield num                  # 每次产生一个整数
```

> **关键行解释**  
> - `isinstance(sub, int)`: 判断当前对象是整数还是列表。  
> - `flat.append(sub)`: 把找到的整数暂存到列表里。  
> - `for num in flat: yield num`: 把列表转化为生成器输出。

#### 复杂度  

- **时间复杂度：** `O(N)`  
  - 这里的 `N` 是数组中整数的总个数（`arr.flat().length`）。我们遍历每个元素恰好一次。  
  - 大白话：如果数组里有 10 万个数字，程序会跑 10 万步，步数和数字个数成正比。

- **空间复杂度：** `O(N)`  
  - 需要额外的列表 `flat` 把所有整数保存下来，最坏情况下它会占用和原始整数一样多的内存。  
  - 大白话：如果有 10 万个数字，列表里也会占用 10 万个位置的空间。

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于需要额外的列表 `flat` 把所有整数先存起来，导致 **额外的 O(N) 空间**。  
实际上，**生成器本身就可以“一边遍历，一边产出”**，我们不必先把所有结果收集完。

优化思路：

1. 仍然使用递归遍历多维数组，但是 **在遍历的过程中直接 `yield`** 整数。  
2. 当递归遇到子数组时，**把控制权交给子数组的生成器**，这可以用 `yield from`（等价于 `yield*`）实现。  
3. 这样每找到一个整数就立刻把它交给外层调用者，**不需要额外的存储**。  
4. 递归调用本身会占用栈空间，深度最多是数组的最大嵌套层数 `maxNestingDepth`，但题目已经保证这不会导致栈溢出。

> **类比**：把多维数组想成一本书的章节目录。最优做法是 **边读边说**（每读到一个章节标题就立刻朗读），而不是先把所有标题抄到纸上再朗读。

#### 代码（Python）

```python
def inorder_traversal(arr):
    """
    最优解：使用生成器递归，直接在遍历过程中 yield 整数。
    """
    if isinstance(arr, int):
        # 基础情况：当前就是一个整数，直接产出
        yield arr
    else:
        # arr 是列表，按左到右顺序递归处理每个元素
        for item in arr:
            # 对子元素调用同一个生成器函数
            # yield from 等价于 for x in generator: yield x
            yield from inorder_traversal(item)
```

> **关键行解释**  
> - `if isinstance(arr, int): yield arr`：如果当前对象是整数，立刻把它交给外层。  
> - `for item in arr:`：遍历列表的每个子元素，从左到右保持顺序。  
> - `yield from inorder_traversal(item)`：把子元素的生成器直接嵌入当前生成器，相当于把子生成器的所有 `yield` “搬进来”。  

#### 复杂度  

- **时间复杂度：** `O(N)`  
  - 仍然需要遍历每个整数一次，时间和暴力解相同，只是省去了额外的遍历 `flat` 的步骤。  

- **空间复杂度：** `O(D)`（`D` 为最大嵌套深度）  
  - 只用递归调用栈保存当前路径上的函数帧，最坏情况下等于嵌套深度。  
  - 与暴力解的 `O(N)` 相比，**大幅降低了内存使用**，尤其当数组非常宽而不是很深时优势明显。

---

## 心得  

- **核心技巧**：使用 **生成器递归 + `yield from`**，实现“遍历即产出”。  
- **适用题型**：  
  1. 任意需要 **深度优先遍历** 并实时输出结果的树/图结构（如二叉树的前序/中序遍历）。  
  2. **嵌套列表/字典的扁平化**（Flatten Nested List Iterator、Flatten Nested Dictionary）。  
  3. **流式处理** 大数据结构，只想“一边读一边处理”，不想一次性全部加载。  
- **一句话总结**：**递归遍历 + `yield from` = “边走边说”，省空间的遍历利器。**

---

## 反思  

- **第一反应**：先把所有整数收集到列表再输出——最直观、最安全的办法。  
- **最容易踩的坑**：  
  - 忘记判断 **整数 vs. 列表**，导致在遍历时出现 `TypeError`。  
  - 空数组或全空子数组的情况，需要保证生成器在没有 `yield` 时直接结束（`next(...).done` 为 `True`）。  
  - 递归深度极端情况下（虽然题目保证安全），仍需意识到栈空间的限制。  
- **下次遇到同类题**：第一步就想到 **“能否在遍历的同时直接产出？”**，如果答案是肯定的，就尝试使用 **生成器 + `yield from`** 直接实现。