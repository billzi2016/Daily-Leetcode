# #341. 扁平化嵌套列表迭代器 / Flatten Nested List Iterator

> 难度：中等 · 标签：Stack、Tree、Depth-First Search、Design、Queue、Iterator · [LeetCode 链接](https://leetcode.com/problems/flatten-nested-list-iterator/)

---

## 题目（英文原版）

**Description**

You are given a nested list of integers nestedList. Each element is either an integer or a list whose elements may also be integers or other lists. Implement an iterator to flatten it.
Implement the NestedIterator class:
Your code will be tested with the following pseudocode:
If res matches the expected flattened list, then your code will be judged as correct.

**Examples**

**Example 1:**

```
initialize iterator with nestedList
res = []
while iterator.hasNext()
    append iterator.next() to the end of res
return res
```

**Example 2:**

```
Input: nestedList = [[1,1],2,[1,1]]
Output: [1,1,2,1,1]
Explanation: By calling next repeatedly until hasNext returns false, the order of elements returned by next should be: [1,1,2,1,1].
```

**Example 3:**

```
Input: nestedList = [1,[4,[6]]]
Output: [1,4,6]
Explanation: By calling next repeatedly until hasNext returns false, the order of elements returned by next should be: [1,4,6].
```

**Constraints**

- 1 <= nestedList.length <= 500
- The values of the integers in the nested list is in the range [-106, 106].

---

## 题目（中文翻译）

**描述**  
给定一个整数的嵌套列表 `nestedList`。列表中的每个元素要么是一个整数，要么是一个列表，而该列表的元素也可能是整数或其他列表。请实现一个迭代器，使其能够将所有整数按顺序展平（flatten）。

**实现 `NestedIterator` 类**  
你的代码将在以下伪代码环境中进行测试：

```pseudo
iterator = NestedIterator(nestedList)
res = []
while iterator.hasNext():
    res.append(iterator.next())
```

如果 `res` 与期望的扁平化列表相同，则判定你的实现正确。

**示例 1**  
（略，示例 1 的伪代码如上所示）

**示例 2**  
输入：`nestedList = [[1,1],2,[1,1]]`  
输出：`[1,1,2,1,1]`  
解释：反复调用 `next()` 直至 `hasNext()` 返回 `false`，`next()` 返回的元素顺序应为 `[1,1,2,1,1]`。

**示例 3**  
输入：`nestedList = [1,[4,[6]]]`  
输出：`[1,4,6]`  
解释：反复调用 `next()` 直至 `hasNext()` 返回 `false`，`next()` 返回的元素顺序应为 `[1,4,6]`。

**约束条件**  
- `1 <= nestedList.length <= 500`  
- 嵌套列表中整数的取值范围为 `[-10^6, 10^6]`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一次性把所有整数全部取出来，放进一个普通的 Python 列表**，随后 `next()` 只需要顺序返回这个列表里的元素，`hasNext()` 只要判断指针是否已经到列表末尾即可。

- **用到的数据结构**  
  - `list`：就像我们平时用的 **收纳箱**，把所有数字一次性装进去，取的时候只需要按顺序搬出来。  
  - 递归：把嵌套的结构层层打开，就像 **打开套娃**，每打开一层就把里面的数字收进箱子。

- **为什么正确**  
  递归遍历能够访问到嵌套结构中的每一个元素。只要把所有整数按出现顺序压进一个线性列表，后面的迭代器只需要顺序访问这条列表，就一定能得到题目要求的扁平化顺序。

- **复杂度分析（大白话）**  
  - 时间复杂度 `O(N)`：`N` 是所有整数的总个数（包括嵌套层级里出现的每个数字）。我们必须把每个数字都看一遍才能装进箱子，所以时间跟 `N` 成正比。  
  - 空间复杂度 `O(N)`：把所有数字都放进一个列表，相当于再准备了一个大小跟原数据一样大的“背包”。如果原始嵌套列表本身已经占了 `N` 的空间，这里又额外用了 `N`，所以总共是两倍的 `N`。

#### 代码（Python）

```python
# 题目提供的接口（在 LeetCode 环境里已经实现），这里仅作说明
# class NestedInteger:
#     def isInteger(self) -> bool: ...
#     def getInteger(self) -> int: ...
#     def getList(self) -> list: ...

class NestedIterator:
    """
    暴力实现：在构造函数里一次性把所有整数取出来放进 self.flat
    """
    def __init__(self, nestedList):
        # 用一个列表收集所有整数
        self.flat = []
        self._flatten(nestedList)
        # 记录下一个要返回的下标
        self.idx = 0

    def _flatten(self, nested):
        """
        递归遍历 nested（可能是 NestedInteger 或 list）
        """
        for ni in nested:
            if ni.isInteger():
                # 如果是整数，就直接放进 flat
                self.flat.append(ni.getInteger())
            else:
                # 否则递归处理它内部的列表
                self._flatten(ni.getList())

    def next(self):
        """返回当前指向的整数，并把指针右移一位"""
        val = self.flat[self.idx]
        self.idx += 1
        return val

    def hasNext(self):
        """只要还有未访问的元素，就返回 True"""
        return self.idx < len(self.flat)
```

#### 复杂度

- **时间复杂度**：`O(N)`  
  解释：我们遍历了所有的整数一次，`N` 越大，花的时间就越多，正比关系就是 `O(N)`。

- **空间复杂度**：`O(N)`  
  解释：我们额外开辟了一个列表来存放所有整数，列表的长度恰好等于整数的个数 `N`，所以占用的额外空间也是 `N`。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于一次性把所有整数都装进列表，导致 **空间浪费**（尤其当嵌套层级很深、但只需要逐个取出时）。我们可以改进为 **按需展开**——只有在调用 `hasNext()` 时，才把最外层的下一个整数“准备好”，而不是一次性把全部装进背包。

**核心技巧：栈（Stack）+ 深度优先遍历（DFS）**  

1. **栈的作用**  
   把 **待处理的列表** 放进去，栈顶始终是我们当前正在查看的列表。  
   想象一下 **一堆待打开的盒子**，我们把最外层的盒子压在最下面，最里面的盒子压在最上面。每次只看最上面的盒子（栈顶），如果它是整数，就可以直接返回；如果它是列表，就把它拆开（把内部的元素压进栈），继续检查。

2. **为什么用栈而不是递归**  
   递归本质上也用到了系统调用栈，但我们自己显式维护一个栈可以 **更灵活地在 hasNext 与 next 之间切换**，而且可以把“把下一个整数准备好”这一步延迟到 `hasNext` 调用时完成，符合迭代器的懒加载（lazy）特性。

3. **实现细节**  
   - **栈中保存的不是 `NestedInteger` 本身，而是** `(nestedList, index)` 这种**“列表 + 当前位置”** 的组合。这样可以在遍历完一个列表后回到上层继续。  
   - `hasNext()` 的核心是 **循环把栈顶指向的元素展开**，直到栈顶是一个整数。若栈空则说明所有元素都已经遍历完。  
   - `next()` 只需要把 `hasNext()` 已经准备好的整数弹出来返回即可。

4. **类比帮助理解**  
   把栈想象成 **一本“阅读进度表”**，每打开一本书（列表）时，在表上记下当前读到第几页（下标）。当当前页是章节标题（整数）时，就可以直接读出来；当是子章节（子列表）时，就在表里再加一行记录子章节的起始页，继续向下阅读。等子章节读完，再回到上一行继续。

#### 代码（Python）

```python
# 题目已经提供的接口，同上
# class NestedInteger:
#     def isInteger(self) -> bool: ...
#     def getInteger(self) -> int: ...
#     def getList(self) -> list: ...

class NestedIterator:
    """
    最优实现：使用显式栈，实现按需展开的懒加载迭代器
    """
    def __init__(self, nestedList):
        # 栈中保存 (list, 当前遍历的下标) 的元组
        # 初始时把外层列表压进去，索引从 0 开始
        self.stack = [(nestedList, 0)]

    def _move_to_integer(self):
        """
        把栈顶调整为指向下一个整数。
        只要栈不为空且栈顶指向的不是整数，就继续展开。
        """
        while self.stack:
            cur_list, cur_idx = self.stack[-1]   # 取栈顶
            # 如果当前列表已经遍历完，弹出栈顶，回到上一层
            if cur_idx == len(cur_list):
                self.stack.pop()
                continue

            # 取出当前索引对应的 NestedInteger
            ni = cur_list[cur_idx]
            # 把当前列表的索引往后移动一位，准备下次继续
            self.stack[-1] = (cur_list, cur_idx + 1)

            if ni.isInteger():
                # 找到整数，先把它“塞回栈顶”，下次 next() 直接取
                self.stack.append(([ni], 0))   # 用单元素列表包装，使后续逻辑统一
                return
            else:
                # 是列表，进一步压入栈中继续搜索
                self.stack.append((ni.getList(), 0))

    def next(self):
        """
        直接返回栈顶的整数。调用前一定已经通过 hasNext() 把栈顶调整好。
        """
        # 确保栈顶一定是整数（由 hasNext 保证）
        cur_list, cur_idx = self.stack[-1]
        # 这里 cur_list 只会是长度为 1、只含整数的列表
        ni = cur_list[cur_idx]          # 取出 NestedInteger
        # 弹掉已经返回的整数
        self.stack.pop()
        return ni.getInteger()

    def hasNext(self):
        """
        判断是否还有下一个整数。
        通过 _move_to_integer 把栈顶提前准备好。
        """
        self._move_to_integer()
        return bool(self.stack)   # 栈非空说明还有整数
```

> **代码要点解释**  
> 1. `self.stack` 中每个元素是 `(list_obj, next_index)`，相当于“我现在正站在 list_obj 的第 next_index 位置”。  
> 2. `_move_to_integer` 循环把栈顶“推进”到一个整数所在的位置。如果当前元素是列表，就把它展开继续搜索；如果列表已经遍历完，则弹出回到上一层。  
> 3. 为了让 `next()` 的实现保持简洁，我们在找到整数时把它包装成 `[ni]` 再压回栈，这样 `next()` 只需要把栈顶的唯一元素弹出并返回即可。

#### 复杂度

- **时间复杂度**：`O(1)` 均摊（amortized）  
  - 解释：每个 `next()` 或 `hasNext()` 调用只会 **推进栈指针** 若干步。虽然一次 `hasNext()` 可能会展开多个层级的列表，但每个 `NestedInteger` 最多只会被 **检查一次、压栈一次、弹栈一次**，所以总的工作量是 `O(N)`，分摊到 `N` 次 `next()` 调用上就是均摊 `O(1)`。

- **空间复杂度**：`O(D)`  
  - 解释：栈中最多保存的是 **嵌套深度** `D`（即最深的子列表层数）。即使整体元素很多，栈只会保存当前遍历路径上的列表，不会一次性存下全部元素。相较于暴力解的 `O(N)`，这里只需要 `O(D)`，在深度远小于元素总数时可以大幅节省内存。

---

## 心得

- **核心技巧**：使用显式栈模拟递归的深度优先遍历，实现“按需展开”的懒加载迭代器。  
- **该技巧适用的题型**  
  1. **树的前序/中序/后序遍历**（如 `BinaryTreeIterator`）  
  2. **带有嵌套结构的遍历**（如 `Nested List Weight Sum`、`Flatten 2D Vector`）  
  3. **深度优先搜索的迭代版**（如 `GraphIterator`、`Word Search` 的非递归实现）  
- **一句话总结解题钥匙**：*把“下一位整数”提前准备好，只在需要时才展开嵌套结构，栈是实现这种懒展开的最佳工具。*

---

## 反思

- **拿到题目第一反应**：直接把所有数字一次性取出来，写一个简单的递归函数。  
- **最容易踩的坑**  
  - **忘记维护遍历顺序**：在递归展开时必须按原始出现顺序把整数加入列表。  
  - **栈的索引管理**：在最优解里，如果忘记在弹出已遍历完的列表时 `pop`，会导致死循环。  
  - **`hasNext` 与 `next` 的调用顺序**：`next` 必须在 `hasNext` 为 `True` 时调用，否则可能出现栈空错误。  
- **下次遇到同类题，第一步该想到**：*是否可以用栈（或队列）实现“按需展开”，而不是一次性全部展开？* 先画出遍历路径，确认最深层的递归深度，然后决定是一次性 flatten 还是懒加载。