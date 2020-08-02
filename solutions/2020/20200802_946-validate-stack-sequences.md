# #946. 验证栈序列 / Validate Stack Sequences

> 难度：中等 · 标签：Array、Stack、Simulation · [LeetCode 链接](https://leetcode.com/problems/validate-stack-sequences/)

---

## 题目（英文原版）

**Description**

Given two integer arrays pushed and popped each with distinct values, return true if this could have been the result of a sequence of push and pop operations on an initially empty stack, or false otherwise.

**Examples**

**Example 1:**

```
Input: pushed = [1,2,3,4,5], popped = [4,5,3,2,1]
Output: true
Explanation: We might do the following sequence:
push(1), push(2), push(3), push(4),
pop() -> 4,
push(5),
pop() -> 5, pop() -> 3, pop() -> 2, pop() -> 1
```

**Example 2:**

```
Input: pushed = [1,2,3,4,5], popped = [4,3,5,1,2]
Output: false
Explanation: 1 cannot be popped before 2.
```

**Constraints**

- 1 <= pushed.length <= 1000
- 0 <= pushed[i] <= 1000
- All the elements of pushed are unique.
- popped.length == pushed.length
- popped is a permutation of pushed.

---

## 题目（中文翻译）

给定两个整数数组 `pushed` 和 `popped`（元素各不相同），如果这两个序列可能是对一个初始为空的栈（stack）进行一系列压入（push）和弹出（pop）操作后的结果，则返回 `true`，否则返回 `false`。

示例

示例 1  
输入: `pushed = [1,2,3,4,5]`, `popped = [4,5,3,2,1]`  
输出: `true`  
解释: 我们可以按以下顺序操作:  
`push(1)`, `push(2)`, `push(3)`, `push(4)`,  
`pop()` → 4,  
`push(5)`,  
`pop()` → 5, `pop()` → 3, `pop()` → 2, `pop()` → 1  

示例 2  
输入: `pushed = [1,2,3,4,5]`, `popped = [4,3,5,1,2]`  
输出: `false`  
解释: 在弹出 1 之前必须先弹出 2，无法得到该序列。

约束条件

- `1 <= pushed.length <= 1000`
- `0 <= pushed[i] <= 1000`
- `pushed` 中的所有元素互不相同。
- `popped.length == pushed.length`
- `popped` 是 `pushed` 的一个排列（permutation）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的压栈 / 弹栈顺序**，看有没有一种顺序能够得到给定的 `popped` 序列。

- **数据结构**：我们可以用 **列表**（在 Python 里当作栈）来保存当前栈的状态。  
- **枚举方式**：从 `pushed` 的第一个元素开始，**每一次**都有两种选择  
  1. **压栈**（push），把下一个还没有压入的元素放进去。  
  2. **弹栈**（pop），如果栈顶正好等于 `popped` 中下一个要弹出的元素，就弹掉它。  

这其实是一个 **回溯（深度优先搜索）** 的过程：在每一步尝试所有合法的操作，递归到底后检查是否恰好遍历完了 `popped`。如果有一次成功，就返回 `True`，否则全部尝试完返回 `False`。

> **为什么正确？**  
> 因为我们把所有合法的压/弹序列都穷举了一遍，只要存在一种能够产生 `popped`，必然会在搜索树的某个叶子节点被发现。

> **时间/空间分析（大白话）**  
> - 每个元素都有两种选择（压或弹），所以最坏情况下会出现 `2^n` 条路径（`n` 是数组长度）。实际搜索会更少一些，但仍是 **指数级**，也就是 **非常慢**，只能在 `n` 很小（比如 ≤10）时跑得动。  
> - 递归深度最多是 `n`，栈里最多放 `n` 个元素，空间开销是 **线性** 的 `O(n)`。

#### 代码（Python）

```python
def validateStackSequences_bruteforce(pushed, popped):
    n = len(pushed)

    # 用递归实现回溯
    def dfs(i, j, stack):
        """
        i: 已经处理完的 pushed 下标（[0, i) 已经压入栈）
        j: 已经匹配完的 popped 下标（[0, j) 已经弹出）
        stack: 当前栈的内容（list，stack[-1] 是栈顶）
        """
        # ① 所有元素都已经匹配完，说明找到一种合法序列
        if j == n:
            return True

        # ② 尝试弹栈（如果栈顶恰好等于下一个要弹出的元素）
        if stack and stack[-1] == popped[j]:
            # 弹掉栈顶后继续搜索
            if dfs(i, j + 1, stack[:-1]):   # 这里用切片复制，保持递归的独立性
                return True

        # ③ 尝试压栈（如果还有未压入的元素）
        if i < n:
            # 把 pushed[i] 放进栈顶
            if dfs(i + 1, j, stack + [pushed[i]]):
                return True

        # ④ 两条路都走不通，返回 False
        return False

    return dfs(0, 0, [])
```

> **关键行解释**  
> - `if stack and stack[-1] == popped[j]`：检查栈顶是否正好是下一个要弹出的数。  
> - `stack[:-1]` 与 `stack + [pushed[i]]`：分别表示弹栈后和压栈后的新栈，使用切片/拼接生成新列表，防止递归之间相互影响。

#### 复杂度

- **时间复杂度**：`O(2^n)`（指数级）——因为每个元素都有「压」或「弹」两种选择，最坏会遍历全部可能的操作序列。  
- **空间复杂度**：`O(n)`——递归栈深度最多 `n`，栈中最多存 `n` 个元素。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于**不停地回溯**，重复检查同样的状态。实际上，我们只需要**一次线性遍历**就能判断是否可能。

观察题目：

1. **压栈的顺序是固定的**——只能按 `pushed` 的顺序把元素放进去。  
2. **弹栈只能在栈顶进行**，且弹出的顺序必须严格匹配 `popped`。

于是我们可以用一个 **真实的栈**（Python 列表）**模拟**这两个过程：

- 按 `pushed` 的顺序依次把元素压入栈。  
- 每压入一个元素后，**立刻检查栈顶**是否等于 `popped` 当前要弹出的元素。如果相等，就弹掉（`pop()`），并把 `popped` 的指针往后移。  
- 只要在遍历完 `pushed` 后，`popped` 的指针已经走到数组末尾，说明所有弹出操作都成功匹配，返回 `True`；否则返回 `False`。

> **为什么只遍历一次就能判断？**  
> 因为压栈顺序固定，只有在**栈顶恰好是下一个要弹出的数**时才可以弹出。我们用 `while` 循环不断把符合条件的栈顶弹掉，确保每个元素要么一直留在栈里（等待后面更大的元素来弹），要么及时弹出。整个过程不需要回溯，时间线性。

> **核心数据结构：栈**  
> 栈可以理解为**只能从顶部进出**的盒子，和现实生活中“装盘子”很像：只能在最上面放新盘子，或者把最上面的盘子拿走。

#### 代码（Python）

```python
def validateStackSequences(pushed, popped):
    """
    使用模拟栈的线性算法。
    """
    stack = []          # 模拟真实的栈
    j = 0               # popped 的指针，指向下一个期待弹出的元素

    for x in pushed:    # 按顺序压入每个元素
        stack.append(x)            # 压栈
        # 只要栈不空且栈顶等于当前要弹出的元素，就弹掉
        while stack and stack[-1] == popped[j]:
            stack.pop()            # 弹栈
            j += 1                 # 移动 popped 指针

    # 循环结束后，若所有弹出都匹配成功，j 应该走到末尾
    return j == len(popped)
```

> **关键行解释**  
> - `stack.append(x)`：把当前的 `pushed` 元素压入栈。  
> - `while stack and stack[-1] == popped[j]`：只要栈顶正好是下一个要弹出的数，就不停地弹掉，模拟“连续弹出”。  
> - `j += 1`：记录已经成功弹出的元素数量。  
> - `return j == len(popped)`：所有元素都弹出成功则返回 `True`。

#### 复杂度

- **时间复杂度**：`O(n)`（线性）——每个元素最多被压入一次、弹出一次，整个过程只遍历两遍数组。  
- **空间复杂度**：`O(n)`（线性）——最坏情况下栈里会暂时保存全部 `n` 个元素（比如 `pushed` 全是递增，而 `popped` 全是递减的情况）。

> 与暴力解对比：时间从指数级 **秒杀** 到线性级，几乎可以在 10⁵ 规模的数据上轻松跑通。

---

## 心得

- **核心技巧**：**模拟栈 + 双指针**（一个遍历 `pushed`，一个遍历 `popped`）。  
- **适用的题型**  
  1. “Valid Parentheses” —— 用栈检查括号匹配。  
  2. “Next Greater Element” —— 单调栈帮助找左/右侧第一个更大的数。  
  3. “Sliding Window Maximum” —— 双端队列（也是一种变形的栈/队列）实现窗口最大值。  
- **一句话总结解题钥匙**：**“顺序压栈、即时弹栈”，只要栈顶等于下一个要弹的数就立即弹”。**

---

## 反思

- **第一反应**：看到两个相同长度、元素唯一的数组，就想到**栈的进出顺序一定要对应**，于是先想到用栈来模拟。  
- **最容易踩的坑**  
  1. **忘记在压栈后立即检查弹栈**，导致把所有压完再统一弹，结果会错误。  
  2. **指针越界**：在 `while` 循环里访问 `popped[j]` 前必须确认 `j < len(popped)`（本实现用 `while stack and stack[-1] == popped[j]`，因为 `j` 只会在匹配成功时才递增，安全）。  
  3. **数组中出现重复元素**（题目保证唯一，但若忽视会导致错误的匹配）。  
- **下次遇到同类题**，第一步应该想到**“用栈模拟过程”，并在每一步检查是否可以立即弹出”。这样往往可以把问题从“枚举”直接转化为 “线性扫描”。