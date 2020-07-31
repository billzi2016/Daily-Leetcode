# #944. 删除列使其有序 / Delete Columns to Make Sorted

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/delete-columns-to-make-sorted/)

---

## 题目（英文原版）

**Description**

You are given an array of n strings strs, all of the same length.
The strings can be arranged such that there is one on each line, making a grid.
You want to delete the columns that are not sorted lexicographically. In the above example (0-indexed), columns 0 ('a', 'b', 'c') and 2 ('c', 'e', 'e') are sorted, while column 1 ('b', 'c', 'a') is not, so you would delete column 1.
Return the number of columns that you will delete.

**Examples**

**Example 1:**

```
abc
bce
cae
```

**Example 2:**

```
Input: strs = ["cba","daf","ghi"]
Output: 1
Explanation: The grid looks as follows:
  cba
  daf
  ghi
Columns 0 and 2 are sorted, but column 1 is not, so you only need to delete 1 column.
```

**Example 3:**

```
Input: strs = ["a","b"]
Output: 0
Explanation: The grid looks as follows:
  a
  b
Column 0 is the only column and is sorted, so you will not delete any columns.
```

**Example 4:**

```
Input: strs = ["zyx","wvu","tsr"]
Output: 3
Explanation: The grid looks as follows:
  zyx
  wvu
  tsr
All 3 columns are not sorted, so you will delete all 3.
```

**Constraints**

- n == strs.length
- 1 <= n <= 100
- 1 <= strs[i].length <= 1000
- strs[i] consists of lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个长度为 `n` 的字符串数组 `strs`，其中所有字符串长度相同。  
将这些字符串按顺序排列，每个字符串占一行，可形成一个字符网格（grid）。  
你需要删除那些在字典序（lexicographically）上 **不** 排序的列。  
例如（下标从 0 开始），列 0 (`'a', 'b', 'c'`) 和列 2 (`'c', 'e', 'e'`) 是排序的，而列 1 (`'b', 'c', 'a'`) 不是，因此需要删除列 1。  
返回需要删除的列数。

**示例**  

示例 1  
```
abc
bce
cae
```
（此处未给出输入/输出，仅展示网格）

示例 2  
```text
Input: strs = ["cba","daf","ghi"]
Output: 1
Explanation: 网格如下：
  cba
  daf
  ghi
列 0 和列 2 是有序的，但列 1 不是，所以只需要删除 1 列。
```

示例 3  
```text
Input: strs = ["a","b"]
Output: 0
Explanation: 网格如下：
  a
  b
唯一的列 0 是有序的，因此不需要删除任何列。
```

示例 4  
```text
Input: strs = ["zyx","wvu","tsr"]
Output: 3
Explanation: 网格如下：
  zyx
  wvu
  tsr
所有 3 列均不有序，需要删除全部 3 列。
```

**约束条件**  

- `n == strs.length`
- `1 <= n <= 100`
- `1 <= strs[i].length <= 1000`
- `strs[i]` 只包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是 **把每一列单独挑出来，检查它是不是已经从上到下递增（或相等）**。  
- **数据结构**：我们只需要遍历已有的 `list`（数组）和 `str`（字符串）。  
  - 把字符串想象成 **一本书的每一行**，每一列就是 **同一页码上的所有词**。  
  - 检查一列是否有序，就像在字典里查找每个词的页码是否递增一样。  
- **正确性**：如果某一列的任意两个相邻字符满足 `上面的字符 ≤ 下面的字符`，则整列都是有序的（传递性保证）。如果出现一次 `>`，说明这列必须被删除。只要把所有不满足的列计数，就得到答案。  
- **复杂度分析（大白话）**：  
  - 外层遍历所有列，列数记作 `m`（即字符串的长度），  
  - 内层遍历每列的所有行，行数记作 `n`（即 `strs` 的长度），  
  - 每一次比较都是 O(1) 的操作。  
  - 所以总共要做 `m × n` 次比较，用 **O(m·n)** 的时间。  
  - 只用了常数级的额外空间（几个计数器），所以 **空间 O(1)**。

#### 代码（Python）

```python
def minDeletionSize(strs):
    """
    :type strs: List[str]
    :rtype: int
    """
    if not strs:                     # 防止空列表
        return 0

    n = len(strs)                    # 行数
    m = len(strs[0])                 # 列数（所有字符串等长）
    delete_cnt = 0                   # 需要删除的列数

    # 逐列检查
    for col in range(m):             # 外层：每一列
        for row in range(1, n):      # 内层：比较相邻的两行
            # 如果上面字符大于下面字符，说明该列不满足升序
            if strs[row][col] < strs[row - 1][col]:
                delete_cnt += 1      # 计数
                break                # 这列已经确定要删，直接进入下一列
    return delete_cnt
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 这里的 `m` 是每个字符串的长度，`n` 是字符串的个数。  
  - 想象一下有 100 行、每行 1000 列，需要检查 **10 万次**字符比较，这就是 `O(m·n)` 的含义。  

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，和输入规模无关。  

---

### 2. 最优解  

#### 思路  
从暴力解出发，我们已经达到了 **遍历每个字符一次** 的下界——没有办法在不看字符的情况下判断该列是否有序。  
唯一可以改进的地方是 **代码实现的简洁度和常数因子**，比如：

1. **一次遍历同时检查所有列**：  
   - 使用 `zip(*strs)` 把矩阵转置，得到每一列对应的元组。  
   - 对每个列元组直接用 `all` 判断是否升序，省去手动的双层循环。  

2. **提前终止**：  
   - 一旦发现某列不满足，立刻计数并跳到下一列，避免无意义的比较（这已经在暴力实现中用了 `break`）。  

核心思想仍然是 **逐列检查有序性**，只是利用 Python 的语言特性写得更“优雅”。  

#### 代码（Python）

```python
def minDeletionSize(strs):
    """
    使用 zip 将列抽取出来，代码更简洁，复杂度不变。
    """
    delete_cnt = 0

    # zip(*strs) 把每一列聚合成一个 tuple，例如：
    # strs = ["abc", "bce", "cae"]  ->  zip(*strs) => ('a','b','c'), ('b','c','a'), ('c','e','e')
    for col in zip(*strs):          # 每次得到一列的所有字符
        # 判断该列是否已排序：前一个字符 <= 后一个字符，全部满足才算有序
        if any(col[i] < col[i - 1] for i in range(1, len(col))):
            delete_cnt += 1        # 不满足则计数
    return delete_cnt
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 仍然需要查看每个字符一次，只是把循环写法换成了 `zip` 与生成器表达式。  
  - 与暴力解相比，时间上没有数量级的提升，但常数更小，实际运行更快。  

- **空间复杂度**：`O(1)`（不计输出）  
  - `zip(*strs)` 生成的是迭代器，不会一次性把所有列存到内存里，只在遍历时产生当前列的元组。  

---

## 心得  

- **核心技巧**：**逐列检查有序性**（相邻字符比较）。  
- **适用的题型**：  
  1. **Delete Columns to Make Sorted II**（需要保留已经确定有序的列，稍微复杂的版本）。  
  2. **Check If All Rows Are Sorted**（行而非列的有序检查）。  
  3. **Maximum Width of a Binary Tree**（把树的每层看成列，检查宽度时也会用到列的遍历）。  
- **一句话总结解题钥匙**：**只要把二维字符矩阵转成“一列一列”，逐列比较相邻行的字符是否递增即可**。

---

## 反思  

- **第一反应**：看到“删除不排序的列”，立刻想到把每列抽出来，检查是否递增。  
- **最容易踩的坑**：  
  - **边界条件**：只有一行或一列时，所有列自然有序，返回 `0`。  
  - **字符串长度不统一**（题目保证相同，但如果忘记检查可能会 IndexError）。  
  - **忘记在发现不符合时提前 `break`**，导致不必要的比较。  
- **下次类似题的第一步**：**把二维结构（矩阵、网格）转置或逐列遍历**，先判断“局部有序”，再决定是否需要进一步处理。