# #388. 最长绝对文件路径 / Longest Absolute File Path

> 难度：中等 · 标签：String、Stack、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/longest-absolute-file-path/)

---

## 题目（英文原版）

**Description**

Suppose we have a file system that stores both files and directories. An example of one system is represented in the following picture:
Here, we have dir as the only directory in the root. dir contains two subdirectories, subdir1 and subdir2. subdir1 contains a file file1.ext and subdirectory subsubdir1. subdir2 contains a subdirectory subsubdir2, which contains a file file2.ext.
In text form, it looks like this (with ⟶ representing the tab character):
If we were to write this representation in code, it will look like this: "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext". Note that the '\n' and '\t' are the new-line and tab characters.
Every file and directory has a unique absolute path in the file system, which is the order of directories that must be opened to reach the file/directory itself, all concatenated by '/'s. Using the above example, the absolute path to file2.ext is "dir/subdir2/subsubdir2/file2.ext". Each directory name consists of letters, digits, and/or spaces. Each file name is of the form name.extension, where name and extension consist of letters, digits, and/or spaces.
Given a string input representing the file system in the explained format, return the length of the longest absolute path to a file in the abstracted file system. If there is no file in the system, return 0.
Note that the testcases are generated such that the file system is valid and no file or directory name has length 0.

**Examples**

**Example 1:**

```
dir
⟶ subdir1
⟶ ⟶ file1.ext
⟶ ⟶ subsubdir1
⟶ subdir2
⟶ ⟶ subsubdir2
⟶ ⟶ ⟶ file2.ext
```

**Example 2:**

```
Input: input = "dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext"
Output: 20
Explanation: We have only one file, and the absolute path is "dir/subdir2/file.ext" of length 20.
```

**Example 3:**

```
Input: input = "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"
Output: 32
Explanation: We have two files:
"dir/subdir1/file1.ext" of length 21
"dir/subdir2/subsubdir2/file2.ext" of length 32.
We return 32 since it is the longest absolute path to a file.
```

**Example 4:**

```
Input: input = "a"
Output: 0
Explanation: We do not have any files, just a single directory named "a".
```

**Constraints**

- 1 <= input.length <= 104
- input may contain lowercase or uppercase English letters, a new line character '\n', a tab character '\t', a dot '.', a space ' ', and digits.
- All file and directory names have positive length.

---

## 题目（中文翻译）

假设我们有一个同时存储文件和目录的文件系统（file system）。下面的示意图展示了该系统的一个例子：

在该示例中，根目录下只有一个目录 `dir`。`dir` 包含两个子目录 `subdir1` 和 `subdir2`。`subdir1` 中包含一个文件 `file1.ext` 和一个子目录 `subsubdir1`。`subdir2` 中包含一个子目录 `subsubdir2`，而 `subsubdir2` 中包含一个文件 `file2.ext`。

如果把这个结构以文本形式表示（用 `⟶` 表示制表符 `\t`），则如下所示：

```
dir
⟶ subdir1
⟶ ⟶ file1.ext
⟶ ⟶ subsubdir1
⟶ subdir2
⟶ ⟶ subsubdir2
⟶ ⟶ ⟶ file2.ext
```

如果将上述表示写成代码字符串，则为：

```
"dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"
```

其中 `\n` 为换行符，`\t` 为制表符。

文件系统中的每个文件和目录都有唯一的绝对路径（absolute path），即从根目录到该文件/目录本身必须依次打开的目录顺序，目录之间使用 `/` 连接。以上例子中，文件 `file2.ext` 的绝对路径为 `"dir/subdir2/subsubdir2/file2.ext"`。目录名仅由字母、数字和/或空格组成。文件名的形式为 `name.extension`，其中 `name` 与 `extension` 也仅由字母、数字和/或空格组成。

给定一个字符串 `input`，它按照上述格式描述了文件系统，返回该文件系统中**文件**的最长绝对路径的长度。如果系统中不存在文件，返回 `0`。

> 注意：测试用例保证文件系统是合法的，且没有文件或目录的名称长度为 `0`。

## 示例

### 示例 1

```
dir
⟶ subdir1
⟶ ⟶ file1.ext
⟶ ⟶ subsubdir1
⟶ subdir2
⟶ ⟶ subsubdir2
⟶ ⟶ ⟶ file2.ext
```

### 示例 2

**输入**

```text
input = "dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext"
```

**输出**

```text
20
```

**解释**  
系统中只有一个文件，其绝对路径为 `"dir/subdir2/file.ext"`，长度为 `20`。

### 示例 3

**输入**

```text
input = "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"
```

**输出**

```text
32
```

**解释**  
系统中有两个文件：

- `"dir/subdir1/file1.ext"`，长度 `21`
- `"dir/subdir2/subsubdir2/file2.ext"`，长度 `32`

返回 `32`，因为它是最长的文件绝对路径。

### 示例 4

**输入**

```text
input = "a"
```

**输出**

```text
0
```

**解释**  
系统中没有文件，只有一个名为 `"a"` 的目录。

## 约束条件

- `1 <= input.length <= 10^4`
- `input` 可能包含小写或大写英文字母、换行符 `\n`、制表符 `\t`、点号 `.`、空格 `' '` 和数字。
- 所有文件和目录的名称长度均为正数。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

1. **把字符串拆成每一行**  
   `\n` 表示换行，换行后的一行要么是目录，要么是文件。  

2. **用 `\t`（制表符）算层级**  
   - 0 个 `\t` → 在根目录下（depth = 0）  
   - 1 个 `\t` → 是根目录的子目录或文件（depth = 1）  
   - 依此类推  

3. **把每一行的名字保存下来**  
   名字本身不含 `\t`，直接用 `lstrip('\t')` 去掉前导制表符。  

4. **对每个文件，往上回溯找到它的所有父目录**  
   - 从当前行往前找，找出深度比它小 1 的那一行 → 它的直接父目录  
   - 再往前找，深度比父目录小 1 的那一行 → 祖父目录 …  
   - 把这些名字用 `'/'` 串起来，就是该文件的绝对路径。  

5. **记录最长的路径长度**  

> **类比**：  
> 把文件系统想象成一本目录册，每一行是一本书的章节标题，标题前面的 `\t` 就是章节的层级。要得到一本书的完整标题，需要把它所在的章节、子章节一直往上找，拼在一起。  

> **为什么正确**：  
> 只要把每个文件的所有父目录都找齐，并用 `'/'` 连接，就得到它唯一的绝对路径。遍历所有文件，最长的那条路径自然就是答案。  

#### 代码（Python）  

```python
def lengthLongestPath_brute(input: str) -> int:
    # 1. 把整体字符串切成每一行
    lines = input.split('\n')
    # 记录每行的层级(depth)和名字(name)
    infos = []
    for line in lines:
        depth = line.count('\t')            # 前导 \t 的个数 = 层级
        name = line.lstrip('\t')            # 去掉前导 \t，得到真实名字
        infos.append((depth, name))

    max_len = 0

    # 2. 对每一行，如果是文件（名字里有 '.'），就向上回溯找父目录
    for i, (depth, name) in enumerate(infos):
        if '.' not in name:                  # 不是文件，跳过
            continue

        # 从当前文件往前找，收集所有父目录的名字
        path_parts = [name]                  # 先放文件名
        cur_depth = depth
        # 逆序遍历已经处理过的行
        for j in range(i - 1, -1, -1):
            d, n = infos[j]
            if d == cur_depth - 1:           # 找到直接父目录
                path_parts.append(n)         # 把父目录名字放进路径
                cur_depth = d                 # 更新当前层级，继续往上找
                if cur_depth == 0:            # 已经到根目录，结束
                    break

        # 3. 把路径用 '/' 连接，算长度
        cur_len = sum(len(p) for p in path_parts) + (len(path_parts) - 1)  # 加上 '/' 的数量
        max_len = max(max_len, cur_len)

    return max_len
```

**关键行中文注释**  
- `depth = line.count('\t')` → 统计前导制表符的个数，得到层级。  
- `if '.' not in name` → 只对文件进行后续处理。  
- `if d == cur_depth - 1` → 找到当前文件的直接父目录。  
- `cur_len = sum(len(p) for p in path_parts) + (len(path_parts) - 1)` → 名字总长度 + `'/'` 的数量（路径中每两个名字之间都有一个斜杠）。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - `n` 为行数。对每个文件，我们最坏要向前遍历所有前面的行寻找父目录，最坏情况是每行都是文件，导致二次遍历。  
  - 用大白话说，就是“如果有 1000 行，需要大约 1000×1000 次检查”。  

- **空间复杂度**：`O(n)`  
  - 需要存储每行的层级和名字（`infos` 列表），以及临时的路径片段列表 `path_parts`（最坏也不超过 `n`）。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于每次都要往前遍历寻找父目录**。如果我们在遍历文件系统的过程中，**把已经算好的“当前层级的路径长度”保存下来**，后面的行就可以直接使用，而不必再回头找。  

**核心数据结构：栈（stack）**  
- 栈顶始终保存**当前所在层级的累计路径长度**（不包括最后的 `'/'`）。  
- 类比：把栈想象成一个“层层叠起的纸条”，每一层纸条记录从根目录到该层的总字符数。  
- 当我们看到一个新的目录/文件时，先看它的层级 `depth`，  
  - **如果 `depth` 大于栈的大小**，说明它是当前目录的子目录/文件，直接在栈顶累计长度。  
  - **如果 `depth` 小于或等于栈的大小**，说明我们已经走出之前的层级，需要弹出栈顶直到栈的大小等于 `depth`，再继续。  

**步骤**  

1. 按行拆分，同暴力解。  
2. 计算每行的 `depth`（`\t` 的数量）和 `name`（去掉前导 `\t`）。  
3. **保持一个栈 `stack`，其中 `stack[i]` 表示第 `i` 层（根层为第 0 层）到该层的路径总长度**（不包括 `'/'`）。  
   - 初始时 `stack = [0]`，表示根目录之前的长度为 0。  
4. 对每行：  
   - `while len(stack) > depth + 1: stack.pop()` → 把不属于当前层级的累计长度弹出。  
   - `cur_len = stack[-1] + len(name)` → 把当前名字的长度加到父层的累计长度上。  
   - **如果是文件**（`'.' in name`），则路径实际长度还要加上 `depth`（因为每层之间会多一个 `'/'`），即 `ans = max(ans, cur_len + depth)`。  
   - **如果是目录**，把 `cur_len` 推入栈中，等待子层级使用。  
5. 遍历结束，`ans` 即为最长文件路径的长度。  

**为什么是 O(n)？**  
- 每行只会被 **一次** 推入栈，最多 **一次** 弹出栈，所有操作的总次数等于行数的常数倍。  

#### 代码（Python）  

```python
def lengthLongestPath(input: str) -> int:
    """
    用栈一次遍历求最长文件绝对路径长度。
    """
    # 1. 按行拆分
    lines = input.split('\n')
    # stack[i] 表示第 i 层（根层为 0）到该层的累计路径长度（不含斜杠）
    stack = [0]          # 虚拟根目录的长度为 0
    max_len = 0

    for line in lines:
        # 2. 统计层级 depth，去掉前导 '\t' 得到真实名字 name
        depth = line.count('\t')
        name = line.lstrip('\t')

        # 3. 栈的大小应当恰好等于 depth+1（根层算第 0 层），
        #    否则弹出多余的层级
        while len(stack) > depth + 1:
            stack.pop()

        # 4. 当前路径长度 = 父层累计长度 + 当前名字长度
        cur_len = stack[-1] + len(name)

        # 5. 判断是文件还是目录
        if '.' in name:                     # 文件
            # 真实路径还要加上每层之间的 '/'，数量等于 depth
            max_len = max(max_len, cur_len + depth)
        else:                               # 目录
            # 把当前累计长度压入栈，供子层级使用
            stack.append(cur_len)

    return max_len
```

**关键行中文注释**  
- `while len(stack) > depth + 1: stack.pop()` → 把已经不在当前层级的累计长度弹出。  
- `cur_len = stack[-1] + len(name)` → 父目录的累计长度 + 当前名字的字符数。  
- `max_len = max(max_len, cur_len + depth)` → 文件路径的实际长度 = 名字总长度 + 斜杠数（等于层级 `depth`）。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次输入的每一行，每行的栈操作（push / pop）最多各一次，整体是线性时间。  
  - 用大白话说，就是“如果有 1000 行，只需要大约 1000 次检查”。  

- **空间复杂度**：`O(d)`（`d` 为最大层级深度）  
  - 栈里最多保存当前路径的每一层累计长度，层数不会超过输入行数 `n`，最坏情况 `O(n)`，但通常远小于 `n`。  

---  

## 心得  

- **核心技巧**：利用栈（或等价的数组）在一次遍历中维护“当前路径的累计长度”。  
- **适用的题型**  
  1. **带层级结构的字符串解析**（如 LeetCode 331 `Mapping the Routes`）。  
  2. **需要实时维护前缀信息的题目**（如 “最长有效括号” 用栈保存索引）。  
  3. **树形结构的深度优先遍历**（可以用栈模拟递归）。  
- **一句话总结解题钥匙**：**把“层级 → 累计长度”映射存进栈，遇文件直接算出完整路径长度**。  

---  

## 反思  

- **第一反应**：看到 `\t` 表示层级，就想到把每行拆出来，逐层回溯找父目录——这就是暴力思路。  
- **最容易踩的坑**  
  - **层级对应关系**：`depth` 为 `\t` 的数量，而栈的大小要比 `depth` 多 1（根目录的虚拟层）。  
  - **文件路径长度的计算**：别忘了每个层级之间要加一个 `'/'`，所以最终要再加上 `depth`。  
  - **空文件系统**：如果没有任何 `'.'`，答案应返回 `0`，而不是栈的大小。  
- **下次遇到同类题**：第一步先**确定层级信息**（`\t`、空格等），然后**考虑用栈/数组保存从根到当前层的累计状态**，这样可以在一次遍历里直接得到答案。