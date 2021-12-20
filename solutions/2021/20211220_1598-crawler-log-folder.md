# #1598. **爬虫日志文件夹** / Crawler Log Folder

> 难度：简单 · 标签：Array、String、Stack · [LeetCode 链接](https://leetcode.com/problems/crawler-log-folder/)

---

## 题目（英文原版）

**Description**

The Leetcode file system keeps a log each time some user performs a change folder operation.
The operations are described below:
You are given a list of strings logs where logs[i] is the operation performed by the user at the ith step.
The file system starts in the main folder, then the operations in logs are performed.
Return the minimum number of operations needed to go back to the main folder after the change folder operations.

**Examples**

**Example 1:**

```
Input: logs = ["d1/","d2/","../","d21/","./"]
Output: 2
Explanation: Use this change folder operation "../" 2 times and go back to the main folder.
```

**Example 2:**

```
Input: logs = ["d1/","d2/","./","d3/","../","d31/"]
Output: 3
```

**Example 3:**

```
Input: logs = ["d1/","../","../","../"]
Output: 0
```

**Constraints**

- 1 <= logs.length <= 103
- 2 <= logs[i].length <= 10
- logs[i] contains lowercase English letters, digits, '.', and '/'.
- logs[i] follows the format described in the statement.
- Folder names consist of lowercase English letters and digits.

---

## 题目（中文翻译）

LeetCode 的文件系统在每次用户执行更改文件夹操作（change folder operation）时都会记录一条日志。  
操作说明如下：

给定一个字符串数组 `logs`，其中 `logs[i]` 表示用户在第 `i` 步执行的操作。文件系统初始位于根文件夹（main folder），随后按照 `logs` 中的顺序执行这些操作。  
返回在完成所有更改文件夹操作后，返回根文件夹所需的最少操作次数。

---

### 示例

**示例 1**  
```
Input: logs = ["d1/","d2/","../","d21/","./"]
Output: 2
Explanation: 使用两次更改文件夹操作 “../” 即可回到根文件夹。
```

**示例 2**  
```
Input: logs = ["d1/","d2/","./","d3/","../","d31/"]
Output: 3
```

**示例 3**  
```
Input: logs = ["d1/","../","../","../"]
Output: 0
```

---

### 约束条件

- `1 <= logs.length <= 10^3`
- `2 <= logs[i].length <= 10`
- `logs[i]` 只包含小写英文字母、数字、`.` 和 `/`。
- `logs[i]` 符合题目中描述的格式。
- 文件夹名称由小写英文字母和数字组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的核心其实是“在文件夹之间来回走”。  
我们可以把 **当前所在的文件夹** 看成一只手指，指向文件系统的层级树。  

- `"../"`  表示向上返回到父文件夹，就像把手指往 **根目录** 的方向往回走一步。  
- `"./"`  表示停在当前文件夹，不需要移动，等价于“原地打个转”。  
- 其它形如 `"d1/"`、`"abc12/"`  的字符串表示进入一个子文件夹，就像把手指往 **更深的层级** 推进一步。  

如果我们把每一次进入的文件夹名字 **压进栈**，每一次返回父文件夹就 **弹出栈顶**，那么栈的大小就恰好等于我们离根目录（主文件夹）的层数。  
当所有日志处理完后，栈里还有多少元素，就需要多少次 `"../"` 才能回到根目录。

> **类比**：栈就像一本“文件夹记事本”，每进一个子文件夹就记一页，退回时把最近记的那页撕掉。

这种“直接模拟”是最直观的做法，代码实现也非常简洁。

#### 代码（Python）

```python
def minOperations(logs):
    stack = []                     # 用列表当栈，记录进入的文件夹
    for op in logs:
        if op == "../":            # 想回到父文件夹
            if stack:              # 栈非空时才能弹出，防止越过根目录
                stack.pop()
        elif op == "./":           # 当前文件夹不动，什么也不做
            continue
        else:                      # 进入一个子文件夹，例如 "d1/"
            stack.append(op)       # 把名字压进栈
    return len(stack)               # 栈的大小就是需要的 "../" 次数
```

**关键行中文注释** 已在代码中标出，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次 `logs`（`n` 为日志条数），每条日志的处理都是 `O(1)`，所以总体是线性时间。  
  > 大白话：如果日志有 100 条，程序最多检查 100 次，不会因为文件夹层数多而慢下来。

- **空间复杂度**：`O(m)`（`m` 为最终留下的子文件夹数）  
  最坏情况所有日志都是进入子文件夹，栈会保存 `n` 个元素。  
  > 大白话：如果全部都是 `"dX/"`，我们需要记住每一步的文件夹，所以占用的内存跟日志数成正比。

---

### 2. 最优解

#### 思路  

其实我们并不需要真的把文件夹名字保存下来，只要知道**当前深度**（离根目录有几层）即可。  
于是可以把栈换成一个整数计数器 `depth`：

- `"../"`  时，如果 `depth > 0`，就把 `depth` 减 1（退回上一层），否则保持不变（已经在根目录，不能再往上）。
- `"./"`  时，`depth` 不变。
- 其它进入子文件夹的操作，`depth` 加 1。

遍历结束后，`depth` 本身就是回到根目录需要的 `"../"` 次数。  
这样做省去了存放具体文件夹名字的空间，只保留一个整数，空间复杂度降到 `O(1)`。

#### 代码（Python）

```python
def minOperations(logs):
    depth = 0                       # 当前所在的层数，根目录时为 0
    for op in logs:
        if op == "../":
            if depth > 0:           # 只能在已有层数的情况下回退
                depth -= 1
        elif op == "./":
            continue                # 什么也不做
        else:                       # 进入子文件夹
            depth += 1
    return depth                    # depth 即为需要的 "../" 次数
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  与暴力解相同，只是省掉了栈的 push/pop 操作，实际常数更小。

- **空间复杂度**：`O(1)`  
  只用一个整数变量 `depth`，不随日志长度增长而增大。  
  > 与暴力解相比，省掉了最多 `n` 个字符串的存储，极大节约内存。

---

## 心得

- 这道题考察的核心技巧是 **状态压缩**（把完整的数据结构（栈）压缩成一个计数器）以及 **模拟**（一步步按照规则更新状态）。
- 类似技巧常出现在：
  1. **路径简化**（如 LeetCode 71. Simplify Path）  
  2. **括号匹配**（如 LeetCode 20. Valid Parentheses）  
  3. **移动机器人**（如 LeetCode 844. Backspace String Compare）  
- **一句话总结解题钥匙**：只要关心“层数”，不必记录每层的名字，直接用整数计数即可。

## 反思

- **第一反应**：把每一次进入的文件夹名字压栈，然后弹栈回退——这就是最自然的模拟思路。
- **最容易踩的坑**：
  - 当已经在根目录时，仍然收到 `"../"`，必须 **忽略** 而不是让深度变负。  
  - `"./"` 必须 **保持不变**，别误写成 `depth += 1`。  
  - 输入可能全部是退回操作，结果应是 `0`，不能返回负数。
- **下次遇到同类题**，第一步应该思考：“我真正需要跟踪的是什么？”  
  如果只是一种**计数**（层数、距离、剩余字符），就尝试用 **整数变量** 替代完整的数据结构。