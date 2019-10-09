# #609. **查找系统中的重复文件** / Find Duplicate File in System

> 难度：中等 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/find-duplicate-file-in-system/)

---

## 题目（英文原版）

**Description**

Given a list paths of directory info, including the directory path, and all the files with contents in this directory, return all the duplicate files in the file system in terms of their paths. You may return the answer in any order.
A group of duplicate files consists of at least two files that have the same content.
A single directory info string in the input list has the following format:
It means there are n files (f1.txt, f2.txt ... fn.txt) with content (f1_content, f2_content ... fn_content) respectively in the directory "root/d1/d2/.../dm". Note that n >= 1 and m >= 0. If m = 0, it means the directory is just the root directory.
The output is a list of groups of duplicate file paths. For each group, it contains all the file paths of the files that have the same content. A file path is a string that has the following format:
Follow up:

**Examples**

**Example 1:**

```
Input: paths = ["root/a 1.txt(abcd) 2.txt(efgh)","root/c 3.txt(abcd)","root/c/d 4.txt(efgh)","root 4.txt(efgh)"]
Output: [["root/a/2.txt","root/c/d/4.txt","root/4.txt"],["root/a/1.txt","root/c/3.txt"]]
```

**Example 2:**

```
Input: paths = ["root/a 1.txt(abcd) 2.txt(efgh)","root/c 3.txt(abcd)","root/c/d 4.txt(efgh)"]
Output: [["root/a/2.txt","root/c/d/4.txt"],["root/a/1.txt","root/c/3.txt"]]
```

**Constraints**

- 1 <= paths.length <= 2 * 104
- 1 <= paths[i].length <= 3000
- 1 <= sum(paths[i].length) <= 5 * 105
- paths[i] consist of English letters, digits, '/', '.', '(', ')', and ' '.
- You may assume no files or directories share the same name in the same directory.
- You may assume each given directory info represents a unique directory. A single blank space separates the directory path and file info.

---

## 题目（中文翻译）

给定一个字符串数组 `paths`，其中每个元素描述了一个目录的信息，包括目录路径以及该目录下所有文件的内容，返回文件系统中所有重复文件的路径列表。答案可以按任意顺序返回。

- **重复文件组**：至少包含两 个内容相同的文件。
- 输入列表中的单个目录信息字符串的格式如下：

```
"目录路径 文件1.txt(内容1) 文件2.txt(内容2) ... 文件n.txt(内容n)"
```

这表示在目录 `"root/d1/d2/.../dm"`（`m ≥ 0`）下有 `n` 个文件（`n ≥ 1`），文件 `fi.txt` 的内容为 `内容i`。若 `m = 0`，则表示该目录就是根目录 `root`。

- 输出是一个列表，列表中的每个子列表对应一组重复文件的完整路径。文件路径的格式为：

```
"目录路径/文件名"
```

### 示例

**示例 1：**

```
Input: paths = ["root/a 1.txt(abcd) 2.txt(efgh)","root/c 3.txt(abcd)","root/c/d 4.txt(efgh)","root 4.txt(efgh)"]
Output: [["root/a/2.txt","root/c/d/4.txt","root/4.txt"],["root/a/1.txt","root/c/3.txt"]]
```

**示例 2：**

```
Input: paths = ["root/a 1.txt(abcd) 2.txt(efgh)","root/c 3.txt(abcd)","root/c/d 4.txt(efgh)"]
Output: [["root/a/2.txt","root/c/d/4.txt"],["root/a/1.txt","root/c/3.txt"]]
```

### 约束条件

- `1 <= paths.length <= 2 * 10^4`
- `1 <= paths[i].length <= 3000`
- `1 <= sum(paths[i].length) <= 5 * 10^5`
- `paths[i]` 只包含英文字母、数字、'/', '.', '(', ')', 和空格 `' '`。
- 同一目录下不会出现同名文件或同名目录。
- 每个给出的目录信息均对应唯一的目录。目录路径与文件信息之间仅由一个空格分隔。

### 进阶

（此题目在原始描述中提供了若干进阶思考方向，可根据实际需求自行实现。）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有文件的 **路径** 和 **内容** 都取出来，放进一个列表。  
随后两两比较文件内容是否相同，如果相同就把它们的路径放进同一个组。  

- **用到的数据结构**  
  - `list`：把每个文件记成 `(path, content)` 的元组，放进列表里。  
  - 两层 `for` 循环：把列表中的每个元素都和后面的元素比较一次。  

- **为什么正确**  
  只要把每一对文件都比较一遍，就一定能找出所有内容相同的文件。只要把相同内容的文件放进同一个集合，答案自然就出来了。

- **复杂度分析（大白话版）**  
  - 假设一共有 `N` 个文件。  
  - 第一个文件要和后面的 `N‑1` 个文件比较，第二个要和 `N‑2` 个比较……于是比较次数大约是 `1 + 2 + … + (N‑1) = N·(N‑1)/2`，这就是 **O(N²)**。  
  - 空间上我们只需要保存所有文件的 `(path, content)`，这跟文件数成正比，即 **O(N)**。

#### 代码（Python）

```python
from typing import List

def findDuplicate_bruteforce(paths: List[str]) -> List[List[str]]:
    # 1. 解析每一行，得到所有文件的 (完整路径, 内容) 列表
    files = []                     # 存放 (path, content)
    for entry in paths:
        parts = entry.split()      # 第一个是目录，后面都是 "文件名(内容)"
        dir_path = parts[0]        # 目录路径，例如 "root/a"
        for file_info in parts[1:]:
            # 把 "1.txt(abcd)" 拆成文件名和内容
            name, rest = file_info.split('(')
            content = rest[:-1]     # 去掉最后的 ')'
            full_path = f"{dir_path}/{name}"
            files.append((full_path, content))

    # 2. 暴力两两比较，构建内容相同的组
    visited = set()                # 记录已经被放进某组的文件下标
    ans = []
    n = len(files)
    for i in range(n):
        if i in visited:
            continue
        cur_path, cur_content = files[i]
        group = [cur_path]         # 当前文件必定在自己的组里
        for j in range(i + 1, n):
            if j in visited:
                continue
            if files[j][1] == cur_content:   # 内容相同
                group.append(files[j][0])
                visited.add(j)               # 标记为已分组
        if len(group) > 1:          # 只有出现至少两次才算重复
            ans.append(group)

    return ans
```

#### 复杂度

- **时间复杂度：O(N²)**  
  `N` 为文件总数。我们把每两个文件都比较一次，类似 “所有同学两两握手”，所以会出现二次方的时间开销。  
- **空间复杂度：O(N)**  
  只用了一个列表保存所有文件的信息，以及几个辅助的集合，和文件数量成线性关系。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于“两两比较”。我们其实并不需要把每个文件的内容和其他所有文件去比较，只要**把相同内容的文件直接聚在一起**即可。  

**哈希表（字典）** 正好可以做到这一点：  
- 把文件内容当作 **key**，文件的完整路径当作 **value**（放进列表）。  
- 当遍历到一个文件时，直接检查哈希表里是否已经有相同的内容。如果有，就把路径追加到对应的列表；如果没有，就新建一个列表。  

这一步只需要 **一次遍历**，每次操作都是 O(1)（哈希表的查找/插入在平均情况下是常数时间），于是整体时间降到 **线性 O(N)**。

> **类比**：哈希表就像一本“词典”。我们把“文件内容”当作单词，把“出现过的文件路径”当作该单词的解释页码。查一次词典，立刻就能找到所有对应的页码。

**步骤概览**  
1. **解析**：把每行字符串拆分成目录、文件名、内容，得到 `(完整路径, 内容)`。  
2. **哈希聚类**：用 `defaultdict(list)` 把相同内容的路径收集在同一个列表里。  
3. **过滤**：只保留列表长度 ≥ 2 的组，因为只有至少两个文件才算重复。  

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def findDuplicate(paths: List[str]) -> List[List[str]]:
    # content_map: 关键字 = 文件内容，值 = 出现过的完整路径列表
    content_map = defaultdict(list)

    for entry in paths:
        parts = entry.split()
        dir_path = parts[0]                # 目录，例如 "root/a"
        for file_info in parts[1:]:
            # 把 "1.txt(abcd)" 拆成文件名和内容
            name, rest = file_info.split('(')
            content = rest[:-1]            # 去掉最后的 ')'
            full_path = f"{dir_path}/{name}"
            # 把路径加入对应内容的列表
            content_map[content].append(full_path)

    # 只保留出现次数 >= 2 的列表
    ans = [paths for paths in content_map.values() if len(paths) > 1]
    return ans
```

#### 复杂度

- **时间复杂度：O(N)**  
  `N` 为文件总数。我们只遍历一次所有文件，哈希表的查找/插入均为常数时间（平均），所以整体是线性。相比暴力的 O(N²)，快了好几个数量级。

- **空间复杂度：O(N)**  
  哈希表需要保存每个文件的路径一次，最坏情况下每个文件内容都不相同，仍然需要 O(N) 的空间。

---

## 心得

- **核心技巧**：使用哈希表（字典）把“相同属性的元素”快速聚在一起。  
- **适用题型**：  
  1. “找出所有出现两次以上的元素”——比如 **两个数组的交集**（LeetCode 349）  
  2. “根据某个字段分组”——比如 **根据员工部门统计人数**（面试常考）  
  3. “字符或子串出现频次统计”——比如 **字母异位词分组**（LeetCode 49）  
- **一句话总结**：**把相同的东西映射到同一个键上，哈希表帮你 O(1) 完成“找同伴”。**

## 反思

- **第一反应**：看到“内容相同”，自然想到把内容当作标识，然后把路径收集起来。  
- **最容易踩的坑**  
  - **字符串解析**：文件信息形如 `1.txt(abcd)`，一定要先把 `'('` 拆开，再去掉末尾的 `')`。  
  - **目录层级为空**：如果路径本身就是根目录 `"root"`，仍要在文件名前加 `/`，否则路径会错误。  
  - **过滤空组**：哈希表会为每个出现的内容都创建列表，需要在返回前剔除只出现一次的列表。  
- **下次第一步**：先**把输入逐行拆解成 “目录 + 文件(内容)”**，再决定用哈希表还是其他结构来做“相同内容分组”。这样可以避免在后期再去重新遍历或二次解析。