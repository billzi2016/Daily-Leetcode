# #2625. 扁平化深层嵌套数组 / Flatten Deeply Nested Array

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/flatten-deeply-nested-array/)

---

## 题目（英文原版）

**Description**

Given a multi-dimensional array arr and a depth n, return a flattened version of that array.
A multi-dimensional array is a recursive data structure that contains integers or other multi-dimensional arrays.
A flattened array is a version of that array with some or all of the sub-arrays removed and replaced with the actual elements in that sub-array. This flattening operation should only be done if the current depth of nesting is less than n. The depth of the elements in the first array are considered to be 0.
Please solve it without the built-in Array.flat method.

**Examples**

**Example 1:**

```
Input
arr = [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
n = 0
Output
[1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]

Explanation
Passing a depth of n=0 will always result in the original array. This is because the smallest possible depth of a subarray (0) is not less than n=0. Thus, no subarray should be flattened.
```

**Example 2:**

```
Input
arr = [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
n = 1
Output
[1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11], 12, 13, 14, 15]

Explanation
The subarrays starting with 4, 7, and 13 are all flattened. This is because their depth of 0 is less than 1. However [9, 10, 11] remains unflattened because its depth is 1.
```

**Example 3:**

```
Input
arr = [[1, 2, 3], [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
n = 2
Output
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

Explanation
The maximum depth of any subarray is 1. Thus, all of them are flattened.
```

**Constraints**

- 0 <= count of numbers in arr <= 105
- 0 <= count of subarrays in arr <= 105
- maxDepth <= 1000
- -1000 <= each number <= 1000
- 0 <= n <= 1000

---

## 题目（中文翻译）

给定一个多维数组（multi-dimensional array）`arr` 和一个深度 `n`，返回该数组的扁平化（flattened）版本。  
多维数组是一种递归数据结构，元素可以是整数，也可以是其他多维数组。  
扁平化数组是指将部分或全部子数组移除，并用子数组中的实际元素替代的结果。只有当当前的嵌套深度 **小于** `n` 时才进行此操作。最外层数组的元素深度视为 `0`。  
请在实现时不要使用内置的 `Array.flat` 方法。

**示例 1**  
**示例 2**  
**示例 3**  

### 约束条件
- `0 <=` 数组中数字的个数 `<= 10^5`
- `0 <=` 子数组的个数 `<= 10^5`
- `maxDepth <= 1000`
- `-1000 <=` 每个数字 `<= 1000`
- `0 <= n <= 1000`

---

#### 示例

**示例 1**  
**输入**  
```
arr = [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
n = 0
```
**输出**  
```
[1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
```
**解释**  
深度 `n=0` 时始终返回原数组。因为子数组的最小可能深度（`0`）并不小于 `n=0`，所以不应对任何子数组进行扁平化。

**示例 2**  
**输入**  
```
arr = [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
n = 1
```
**输出**  
```
[1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11], 12, 13, 14, 15]
```
**解释**  
深度为 `0` 的子数组（起始于 `4`、`7`、`13` 的那些）全部被扁平化，因为它们的深度小于 `1`。而 `[9, 10, 11]` 的深度为 `1`，不满足 `< n` 的条件，故保持原样。

**示例 3**  
**输入**  
```
arr = [[1, 2, 3], [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
n = 2
```
**输出**  
```
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
```
**解释**  
任意子数组的最大深度为 `1`，均小于 `2`，因此全部被扁平化。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把 **所有** 子数组都展开，得到一个“一维”数组。  
可以把数组想象成一堆盒子，盒子里可能还有更小的盒子，里面装的才是真正的数字。  
我们把 **每个盒子** 都打开（递归），把里面的东西取出来放进结果列表。  

- **使用的数据结构**：  
  - `list`（Python 中的数组）用来存放原始数据和结果。  
  - **递归**：把“打开盒子”这件事交给函数自己去完成。递归就像我们请一个小朋友帮忙打开盒子，等小朋友把里面的东西递给我们后，我们再继续处理下一个盒子。  

- **为什么一定对**：  
  只要我们把每一个出现的子数组都递归展开，最终得到的就是所有数字按出现顺序排成的一维列表。  

- **复杂度大白话**：  
  - **时间**：我们会访问数组里每一个元素一次（不管它是数字还是子数组），所以时间是 **O(N)**，这里的 N 代表数组里所有数字和子数组的总个数。  
  - **空间**：需要一个新的列表把所有数字装进去，大小也是 O(N)。另外递归调用会占用栈空间，最坏情况下深度等于嵌套层数（≤1000），可以认为是 **O(depth)**。  

> 注意：这就是“暴力”解法，因为它不管题目给的深度 `n`，把所有层都拆开了。下面我们再写一个只在需要的层数才展开的更“省事”的版本。

#### 代码（Python）

```python
def flatten_bruteforce(arr):
    """
    暴力版：把 arr 里所有层的子数组全部展开，返回一维列表
    """
    res = []                     # 用来存放最终结果的列表

    def dfs(item):
        # 如果当前元素是 list（子数组），继续往里找
        if isinstance(item, list):
            for sub in item:      # 逐个处理子元素
                dfs(sub)          # 递归展开
        else:
            res.append(item)      # 不是 list，直接放进结果

    dfs(arr)                     # 从最外层开始递归
    return res

# ------------------- 示例 -------------------
if __name__ == "__main__":
    arr = [1, 2, [3, [4, 5]], 6]
    print(flatten_bruteforce(arr))   # [1, 2, 3, 4, 5, 6]
```

#### 复杂度  

- **时间复杂度**：`O(N)` — 需要遍历数组里每一个元素一次。  
- **空间复杂度**：`O(N + depth)` — 结果列表占 `O(N)`，递归栈最多占 `O(depth)`（depth ≤ 1000）。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**耗时的地方**在于我们把所有层都递归展开。  
题目要求**只在当前深度 < n 时才展开**，否则保留子数组的整体结构。  
因此我们只需要在递归时记录「已经进入了多少层」：

1. **入口**：把外层视为深度 `0`（题目约定）。  
2. **递归条件**：  
   - 如果当前元素是数字 → 直接放进结果。  
   - 如果是子数组且 **当前深度 < n** → 进入子数组继续递归（相当于把盒子打开）。  
   - 如果是子数组但 **当前深度 ≥ n** → **不再打开**，直接把整个子数组（保持原样）放进结果。  

这样我们只会展开需要展开的层数，省掉了不必要的递归调用。  

> **类比**：想象你在一层楼的建筑里，只允许在前 `n` 层使用电梯（展开），超过 `n` 层只能走楼梯（保持原样）。  

**关键点**  

- **递归深度计数**：每进入一次子数组，就把 `depth+1` 传给下一层。  
- **防止递归层数超限**：题目最大深度 ≤ 1000，Python 默认递归上限也是 1000，建议在代码开头把上限调高一点（`sys.setrecursionlimit(2000)`），以防极端情况。  
- **返回值**：我们用一个列表 `res` 累加结果，**如果遇到不需要展开的子数组**，直接把它（整个 list 对象）`append` 进去即可。  

#### 代码（Python）

```python
import sys
sys.setrecursionlimit(2000)   # 防止递归层数超过默认上限

def flatten_depth(arr, n):
    """
    在深度 < n 的层展开子数组，深度 >= n 的子数组保持原样。
    :param arr: 待处理的多维数组（list）
    :param n:   需要展开的最大深度（整数）
    :return:    按要求展开后的新列表
    """
    res = []                    # 用来收集结果

    def helper(item, depth):
        """
        :param item: 当前遍历的元素（可能是数字或 list）
        :param depth: 当前已经进入的层数（外层为 0）
        """
        if isinstance(item, list):
            # 当前是子数组，判断是否需要继续展开
            if depth < n:                       # 需要展开 → 继续递归
                for sub in item:
                    helper(sub, depth + 1)      # 进入下一层，深度+1
            else:                               # 已达到或超过 n → 保持原样
                res.append(item)                # 把整个子数组当作普通元素放进结果
        else:
            # 不是 list，直接加入结果
            res.append(item)

    helper(arr, 0)               # 从外层深度 0 开始
    return res

# ------------------- 示例 -------------------
if __name__ == "__main__":
    arr1 = [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
    print(flatten_depth(arr1, 0))
    # [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]

    print(flatten_depth(arr1, 1))
    # [1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11], 12, 13, 14, 15]

    arr2 = [[1, 2, 3], [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
    print(flatten_depth(arr2, 2))
    # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
```

#### 复杂度  

- **时间复杂度**：`O(N)` — 仍然只遍历一次所有元素，只是**在 depth ≥ n 时提前停止递归**，所以没有额外的开销。  
- **空间复杂度**：`O(N + depth)` — 结果列表占 `O(N)`，递归栈深度最多是 `min(maxDepth, n)`，不超过题目给的 1000，故为 `O(depth)`。相较于暴力解，栈空间可能更小（因为不必递归到最深的层）。  

---  

## 心得  

- **核心技巧**：**递归 + 深度控制**。在遍历嵌套结构时，记录当前层数，根据层数决定是否继续递归。  
- **适用场景**（类似题目）：  
  1. **Flatten Nested List Iterator**（LeetCode 341）——需要把任意深度的嵌套列表逐个取出。  
  2. **Maximum Depth of Binary Tree**（LeetCode 104）——递归遍历树并记录深度。  
  3. **Nested List Weight Sum**（LeetCode 339）——遍历嵌套列表并根据深度累加加权和。  
- **一句话总结解题钥匙**：**“在递归时把‘我已经在第几层’这个信息带进去，决定是否继续往里走”。**  

---  

## 反思  

- **第一反应**：看到“多维数组”和“深度 n”，立刻想到递归，因为递归天然适合处理“层层套娃”的结构。  
- **最容易踩的坑**：  
  - **递归深度超限**：Python 默认递归深度 1000，题目最大深度也 1000，实际运行时最好把上限调高一点。  
  - **忘记把子数组整体保留**：当 `depth >= n` 时，必须 `append` 整个子数组，而不是把它拆开。否则会错误地把本不该展开的层也展开。  
  - **原地修改 vs 返回新列表**：题目要求返回新的扁平化数组，直接在原数组上修改可能导致意料之外的副作用。  
- **下次类似题的第一步**：先明确**“是否需要根据层数/深度进行不同处理”**，如果是，就在递归函数的参数里加入一个 `depth`（或 `level`）变量，随后在递归入口处判断是否继续深入。这样可以一次性把思路写清楚，后面只需要实现细节。