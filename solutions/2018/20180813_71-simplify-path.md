# #71. 简化路径 / Simplify Path

> 难度：中等 · 标签：String、Stack · [LeetCode 链接](https://leetcode.com/problems/simplify-path/)

---

## 题目（英文原版）

**Description**

You are given an absolute path for a Unix-style file system, which always begins with a slash '/'. Your task is to transform this absolute path into its simplified canonical path.
The rules of a Unix-style file system are as follows:
The simplified canonical path should follow these rules:
Return the simplified canonical path.

**Examples**

**Example 1:**

```
Input: path = "/home/"
Output: "/home"
Explanation:
The trailing slash should be removed.
```

**Example 2:**

```
Input: path = "/home//foo/"
Output: "/home/foo"
Explanation:
Multiple consecutive slashes are replaced by a single one.
```

**Example 3:**

```
Input: path = "/home/user/Documents/../Pictures"
Output: "/home/user/Pictures"
Explanation:
A double period ".." refers to the directory up a level (the parent directory).
```

**Example 4:**

```
Input: path = "/../"
Output: "/"
Explanation:
Going one level up from the root directory is not possible.
```

**Example 5:**

```
Input: path = "/.../a/../b/c/../d/./"
Output: "/.../b/d"
Explanation:
"..." is a valid name for a directory in this problem.
```

**Constraints**

- 1 <= path.length <= 3000
- path consists of English letters, digits, period '.', slash '/' or '_'.
- path is a valid absolute Unix path.

---

## 题目（中文翻译）

给定一个 Unix 风格的**绝对路径**（absolute path），它总是以斜杠 `'/'` 开头。请将该路径转换为**简化的规范路径**（simplified canonical path）。

Unix 文件系统的规则如下：

- 连续的多个斜杠 `'/'` 被视为一个斜杠。
- `'.'` 表示当前目录， 可以忽略。
- `'..'` 表示返回到上一级目录（父目录）。如果已经在根目录 `'/'`，则无法再向上返回。
- 规范路径必须以斜杠 `'/'` 开头，且所有目录之间仅保留单个斜杠，不以结尾的斜杠结束（除非路径为根目录 `'/'`）。
- 规范路径中不应出现 `'.'` 或 `'..'`。

返回简化后的规范路径。

## 示例

### 示例 1
**输入**  
```text
path = "/home/"
```
**输出**  
```text
"/home"
```
**解释**  
尾部的斜杠应当被去除。

### 示例 2
**输入**  
```text
path = "/home//foo/"
```
**输出**  
```text
"/home/foo"
```
**解释**  
连续的多个斜杠会被替换为单个斜杠。

### 示例 3
**输入**  
```text
path = "/home/user/Documents/../Pictures"
```
**输出**  
```text
"/home/user/Pictures"
```
**解释**  
`".."` 表示返回到上一级目录（父目录）。

### 示例 4
**输入**  
```text
path = "/../"
```
**输出**  
```text
"/"
```
**解释**  
在根目录上再向上一层是不存在的。

### 示例 5
**输入**  
```text
path = "/.../a/../b/c/../d/./"
```
**输出**  
```text
"/.../b/d"
```
**解释**  
在本题中，`"..."` 被视为合法的目录名称。

## 约束条件

- `1 <= path.length <= 3000`
- `path` 仅由英文字母、数字、句点 `'.'`、斜杠 `'/'` 或下划线 `'_'` 组成。
- `path` 是一个有效的 **绝对 Unix 路径**（valid absolute Unix path）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把路径按斜杠 `/` 分割成若干段，然后**逐段**判断：

| 片段 | 含义 | 处理方式 |
|------|------|----------|
| 空字符串 `""`（出现连续斜杠时） | 没有实际目录 | 什么也不做，直接跳过 |
| `"."` | 当前目录 | 同上，跳过 |
| `".."` | 父目录 | 把已经收集好的目录弹出（如果已经在根目录，则保持根目录） |
| 其它合法名字 | 真正的子目录 | 把它加入结果列表 |

把这些步骤想象成 **“往栈里压、弹”** 的过程——栈（Stack）在这里相当于一个 **“装目录的背包”**，每读到一个合法目录名就往背包里放（`push`），遇到 `".."` 就把背包最上面的目录取出来（`pop`）。最后把背包里的目录用斜杠重新拼起来，就是简化后的路径。

这个办法之所以一定能得到正确答案，是因为：

1. **顺序不变**：我们严格按照路径出现的顺序处理，每一步只影响已经读过的部分，后面的字符不会影响前面的决定。  
2. **完整模拟**：`"."`、`".."`、连续斜杠的语义在 Unix 文件系统里就是这么解释的，完全对应我们的处理规则。

#### 代码（Python）

```python
def simplifyPath(path: str) -> str:
    # 1. 先把路径按照 '/' 切分，得到所有片段
    parts = path.split('/')          # 例如 "/a//b/../c" -> ["", "a", "", "b", "..", "c"]
    
    stack = []                       # 用列表模拟栈，保存合法的目录名
    for part in parts:
        if part == '' or part == '.':
            # 空片段或 '.' 表示当前目录，直接忽略
            continue
        elif part == '..':
            # '..' 表示回到上一级目录，弹出栈顶（如果栈非空）
            if stack:
                stack.pop()
        else:
            # 其余都是合法目录名，压入栈中
            stack.append(part)
    
    # 2. 用 '/' 把栈中的目录拼成最终路径，根目录单独处理
    simplified = '/' + '/'.join(stack)
    return simplified
```

#### 复杂度

- **时间复杂度：O(n)**  
  `n` 为路径字符串的长度。我们只遍历一次 `path.split('/')`（本身也是 O(n)），随后再遍历得到的片段列表，每个片段只做常数时间的判断和栈操作。  
  用大白话说，就是“看一遍字符，花的时间跟字符个数成正比”。

- **空间复杂度：O(n)**  
  最坏情况下（全部是合法目录且没有 `".."`），栈会存下所有目录名，整体占用的额外空间和路径长度同样是线性的。

---

### 2. 最优解

#### 思路  

虽然上面的“直觉解”已经是 **线性** 的了，但我们可以把它进一步形式化为 **标准的栈（stack）解法**，这样思路更清晰，代码也更易于迁移到其他语言。

**瓶颈定位**：  
- 暴力解的核心已经是 **一次遍历 + 栈**，不存在重复遍历或嵌套循环，所以没有明显的性能瓶颈。  
- 需要优化的点其实是 **代码可读性** 与 **对特殊情况的统一处理**（比如连续斜杠、根目录的上层访问）。

**优化思路**：

1. **一次性分割**：使用 `split('/')` 把所有片段一次性拿到，避免在遍历过程中手动寻找斜杠。  
2. **统一栈操作**：把所有合法目录名压栈，遇到 `".."` 时弹栈，其他情况直接跳过。这样只需要一个 `for` 循环。  
3. **返回结果**：栈中保存的顺序已经是从根到叶子的顺序，直接用 `'/'` 连接即可。根目录的特殊情况（空栈）只需要返回 `'/'`。

下面的代码几乎与上面的直觉解相同，但把 **“把路径切片 + 逐段处理”** 的思路明确写成 **“使用栈来模拟目录结构”**，更符合面试时的标准答案。

#### 代码（Python）

```python
def simplifyPath(path: str) -> str:
    # 把路径按 '/' 分割，得到每一段（可能出现空串）
    components = path.split('/')
    
    stack = []  # 栈，保存合法的目录名称
    for comp in components:
        if comp == '' or comp == '.':
            # 空串或 '.' 表示当前目录，直接跳过
            continue
        if comp == '..':
            # '..' 表示返回上一级目录，栈非空时弹出
            if stack:
                stack.pop()
        else:
            # 其它都是合法目录名，压入栈中
            stack.append(comp)
    
    # 用 '/' 连接栈中的目录，前面加一个根目录的 '/'。
    # 如果栈为空，直接返回根目录 '/'
    return '/' + '/'.join(stack)
```

#### 复杂度

- **时间复杂度：O(n)**  
  只遍历一次 `components`，每个元素的处理都是 O(1) 的栈操作。与直觉解的时间复杂度相同，只是代码结构更简洁。

- **空间复杂度：O(n)**  
  最坏情况下所有目录名都要保存在栈里，额外空间随路径长度线性增长。

---

## 心得

- **核心技巧**：**栈（stack）** 用来模拟目录的进出，配合字符串的 `split('/')` 完成路径的分段。  
- **适用题型**：  
  1. 处理带有 “撤销” 操作的序列（如 **有效的括号**、**逆波兰表达式求值**）。  
  2. 需要**回退**到上一步的路径或状态（如 **实现浏览器前进/后退**、**简化目录路径**）。  
- **一句话总结**：  
  “把路径看成一列进出指令，用栈记录当前所在的目录，遇到 `..` 就弹栈，最后把栈内容拼回去。”

---

## 反思

- **第一反应**：看到 `..`、`.`、`//`，立刻想到“把路径切成块，逐块决定保留还是删除”。  
- **最容易踩的坑**：  
  - 忘记处理 **连续斜杠**（会产生空字符串，需要跳过）。  
  - 在根目录下遇到 `..` 时仍然尝试弹栈，导致错误的负索引或空栈异常。  
  - 最后拼接结果时遗漏根目录的前导斜杠。  
- **下次遇到同类题**：  
  1. 先把输入 **切块**（`split`），明确每块的意义。  
  2. 决定使用 **栈** 还是 **计数器** 来模拟“进/出”操作。  
  3. 关注 **边界情况**（空块、根目录、连续特殊符号），确保代码对这些情况稳健。