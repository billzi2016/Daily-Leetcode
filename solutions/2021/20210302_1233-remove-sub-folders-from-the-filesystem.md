# #1233. 删除文件系统中的子文件夹 / Remove Sub-Folders from the Filesystem

> 难度：中等 · 标签：Array、String、Depth-First Search、Trie · [LeetCode 链接](https://leetcode.com/problems/remove-sub-folders-from-the-filesystem/)

---

## 题目（英文原版）

**Description**

Given a list of folders folder, return the folders after removing all sub-folders in those folders. You may return the answer in any order.
If a folder[i] is located within another folder[j], it is called a sub-folder of it. A sub-folder of folder[j] must start with folder[j], followed by a "/". For example, "/a/b" is a sub-folder of "/a", but "/b" is not a sub-folder of "/a/b/c".
The format of a path is one or more concatenated strings of the form: '/' followed by one or more lowercase English letters.

**Examples**

**Example 1:**

```
Input: folder = ["/a","/a/b","/c/d","/c/d/e","/c/f"]
Output: ["/a","/c/d","/c/f"]
Explanation: Folders "/a/b" is a subfolder of "/a" and "/c/d/e" is inside of folder "/c/d" in our filesystem.
```

**Example 2:**

```
Input: folder = ["/a","/a/b/c","/a/b/d"]
Output: ["/a"]
Explanation: Folders "/a/b/c" and "/a/b/d" will be removed because they are subfolders of "/a".
```

**Example 3:**

```
Input: folder = ["/a/b/c","/a/b/ca","/a/b/d"]
Output: ["/a/b/c","/a/b/ca","/a/b/d"]
```

**Constraints**

- 1 <= folder.length <= 4 * 104
- 2 <= folder[i].length <= 100
- folder[i] contains only lowercase letters and '/'.
- folder[i] always starts with the character '/'.
- Each folder name is unique.

---

## 题目（中文翻译）

**描述**  
给定一个文件夹路径列表 `folder`，返回删除所有子文件夹（sub-folder）后的文件夹列表。答案可以以任意顺序返回。  
如果 `folder[i]` 位于另一个文件夹 `folder[j]` 的内部，则称其为 `folder[j]` 的子文件夹（sub-folder）。子文件夹的路径必须以 `folder[j]` 开头，随后紧跟一个斜杠 `"/"`。例如，`"/a/b"` 是 `"/a"` 的子文件夹，但 `"/b"` 不是 `"/a/b/c"` 的子文件夹。  
路径（path）的格式为一个或多个由 `'/'` 加一个或多个小写英文字母组成的字符串连续拼接而成。

**示例 1**  
```text
输入: folder = ["/a","/a/b","/c/d","/c/d/e","/c/f"]
输出: ["/a","/c/d","/c/f"]
解释: 文件夹 "/a/b" 是 "/a" 的子文件夹，"/c/d/e" 位于文件夹 "/c/d" 内，因此这两个子文件夹会被删除。
```

**示例 2**  
```text
输入: folder = ["/a","/a/b/c","/a/b/d"]
输出: ["/a"]
解释: "/a/b/c" 和 "/a/b/d" 都是 "/a" 的子文件夹，需被移除。
```

**示例 3**  
```text
输入: folder = ["/a/b/c","/a/b/ca","/a/b/d"]
输出: ["/a/b/c","/a/b/ca","/a/b/d"]
解释: 这些路径之间不存在子文件夹关系，全部保留。
```

**约束条件**  
- `1 <= folder.length <= 4 * 10^4`
- `2 <= folder[i].length <= 100`
- `folder[i]` 只包含小写字母和 `'/'`。
- `folder[i]` 必定以字符 `'/'` 开头。
- 每个文件夹名称唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**两层循环**：把每个文件夹 `folder[i]` 与所有其它文件夹 `folder[j]` 作比较，判断 `folder[i]` 是否是 `folder[j]` 的子文件夹。

- **判断子文件夹**  
  如果 `folder[i]` 以 `folder[j]` 开头，并且紧跟在 `folder[j]` 后面的是字符 `'/'`，则 `folder[i]` 必然是 `folder[j]` 的子文件夹。  
  这就像在字典里查单词：键（`folder[j]`）对应的“页码”是它本身的路径，若另一个单词（`folder[i]`）的开头正好是这个键再加上一个斜杠，就说明它在这本“书”里更深的章节。

- **为什么正确**  
  只要遍历完所有的配对，就能找出每一个真正的子文件夹，然后把它们全部剔除，剩下的就是答案。

- **时间/空间复杂度**  
  - **时间**：外层循环 `n` 次，内层循环最多也要遍历 `n` 次，每次比较最多需要遍历路径的长度 `L`（最长 100）。于是时间复杂度是 **O(n²·L)**。如果把 `L` 当作常数不计，写成 **O(n²)**。这在 `n` 达到 4·10⁴ 时会非常慢（大约 1.6 × 10⁹ 次比较），几乎会超时。  
  - **空间**：只用了一个结果列表和若干临时变量，和输入规模无关，空间复杂度是 **O(1)**（不计结果列表本身）。

#### 代码（Python）

```python
from typing import List

def removeSubfolders_brute(folder: List[str]) -> List[str]:
    n = len(folder)
    # 记录每个路径是否是子文件夹，默认都不是
    is_sub = [False] * n

    # 两层循环，两两比较
    for i in range(n):
        if is_sub[i]:                     # 已经被标记为子文件夹，后面不必再比较
            continue
        for j in range(n):
            if i == j:
                continue                  # 不和自己比较
            # 若 folder[i] 以 folder[j] 为前缀，并且后面紧跟 '/'
            if folder[i].startswith(folder[j]) and \
               folder[i][len(folder[j]):len(folder[j]) + 1] == '/':
                is_sub[i] = True           # folder[i] 是子文件夹
                break                     # 找到父目录即可退出内层循环

    # 把不是子文件夹的路径挑出来返回
    return [folder[i] for i in range(n) if not is_sub[i]]

# ------------------- 示例 -------------------
if __name__ == "__main__":
    example = ["/a","/a/b","/c/d","/c/d/e","/c/f"]
    print(removeSubfolders_brute(example))  # ['/a', '/c/d', '/c/f']
```

#### 复杂度

- **时间复杂度**：**O(n²·L)**  
  “n²” 表示我们要比较每一对路径，L 是路径最长的字符数。实际运行时，n 达到 4·10⁴ 时会非常慢。

- **空间复杂度**：**O(1)**（不计返回列表）  
  只用了几个额外的布尔数组，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每一次都要遍历所有其它路径”**。如果我们能把路径排好序，使得父路径一定出现在它的子路径前面，那么只需要**一次线性扫描**就能判断是否是子文件夹。

**关键观察**  

- 按字典序（lexicographic）对所有路径进行排序。  
  例如 `["/a","/a/b","/a/b/c","/b"]` 排序后仍然是 `["/a","/a/b","/a/b/c","/b"]`。  
  因为子路径的字符串必定在父路径后面出现（父路径是它的前缀），所以在排好序的序列里，**每个父目录一定紧挨在它的所有子目录之前**。

- 只需要维护**最近加入结果列表的那个路径**（记作 `prev`）。  
  当遍历到当前路径 `cur` 时：  
  - 如果 `cur` 以 `prev` 为前缀，并且紧跟 `'/'`，说明 `cur` 是 `prev` 的子文件夹，直接 **跳过**。  
  - 否则 `cur` 不是子文件夹，加入结果并把 `prev` 更新为 `cur`。

这样我们只遍历一次（O(n)），再加上排序的 O(n log n) 就得到整体的最优复杂度。

> **为什么要检查后面的 `'/'`？**  
> 假设 `prev = "/a"`，如果 `cur = "/ab"`，它同样以 `"/a"` 开头，但实际上不是子文件夹（因为缺少斜杠分隔），所以必须再检查 `cur[len(prev)] == '/'`。

**可选的 Trie（字典树）实现**  
如果不想依赖排序，也可以把所有路径插入到一棵 Trie 中。插入时，一旦走到已经是完整路径的节点，就停止向下插入，因为它的子节点都属于子文件夹。遍历 Trie 即可得到答案。这里我们主要展示排序+线性扫描的解法，因为代码更简洁且实际运行更快。

#### 代码（Python）

```python
from typing import List

def removeSubfolders(folder: List[str]) -> List[str]:
    # 1. 按字典序排序
    folder.sort()
    res = []            # 用来保存最终结果
    prev = ""           # 上一个加入结果的路径

    for cur in folder:
        # 2. 判断 cur 是否是 prev 的子文件夹
        #    - 必须以 prev 为前缀
        #    - 并且后面紧跟 '/'（防止 "/a" 与 "/ab" 误判）
        if not prev or not (cur.startswith(prev) and 
                            len(cur) > len(prev) and 
                            cur[len(prev)] == '/'):
            res.append(cur)   # 不是子文件夹，加入结果
            prev = cur         # 更新 prev 为当前路径

    return res

# ------------------- 示例 -------------------
if __name__ == "__main__":
    cases = [
        ["/a","/a/b","/c/d","/c/d/e","/c/f"],
        ["/a","/a/b/c","/a/b/d"],
        ["/a/b/c","/a/b/ca","/a/b/d"]
    ]
    for c in cases:
        print(removeSubfolders(c))
    # ['/a', '/c/d', '/c/f']
    # ['/a']
    # ['/a/b/c', '/a/b/ca', '/a/b/d']
```

#### 复杂度

- **时间复杂度**：**O(n log n + ΣL)**  
  - 排序需要 `O(n log n)`（`n` 为路径数量）。  
  - 排序后只做一次线性遍历，每条路径最多检查一次前缀关系，整体花费与所有字符总长度 `ΣL` 成正比。  
  与暴力解的 **O(n²·L)** 相比，提升巨大，尤其在 `n` 很大时几乎是必不可少的。

- **空间复杂度**：**O(1)**（不计排序时的临时空间）  
  - Python 的原地排序 `list.sort()` 只使用了常数级的额外空间。  
  - 结果列表 `res` 需要存放最终的路径数目，和输出本身等价。

---

## 心得

- **核心技巧**：先排序，再利用“父路径一定在子路径前面” 的特性，只用一次线性扫描即可过滤子文件夹。  
- **适用场景**：  
  1. **删除子区间 / 子区间合并**（如合并重叠区间的变形）。  
  2. **字符串前缀过滤**（比如在词典里去掉被其它词覆盖的词）。  
  3. **文件系统层级筛选**（本题的直接变体）。  
- **一句话总结**：把路径按字典序排好序，逐个比较前缀即可“一遍扫除”所有子文件夹。

---

## 反思

- **第一反应**：直接两层循环逐对比较，想到“如果前缀相同且后面有斜杠，就是子文件夹”。这就是最自然的暴力思路。  
- **最容易踩的坑**：  
  - 把 `"/a"` 与 `"/ab"` 误判为父子关系，忘记检查紧跟的 `'/'`。  
  - 忽视路径本身的唯一性导致重复计数（题目保证唯一，这点可以放心）。  
  - 对排序后的遍历忘记更新 `prev`，导致所有路径都被误认为是子文件夹。  
- **下次遇到同类题**：第一步先 **思考能否把输入“排好序”**，让父子关系变成“相邻出现”，再决定是用 **双指针/线性扫描** 还是 **Trie** 来实现。这样往往能把原本的 O(n²) 降到 O(n log n) 或更低。