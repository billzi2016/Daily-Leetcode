# #1948. 删除系统中的重复文件夹 / Delete Duplicate Folders in System

> 难度：困难 · 标签：Array、Hash Table、String、Trie、Hash Function · [LeetCode 链接](https://leetcode.com/problems/delete-duplicate-folders-in-system/)

---

## 题目（英文原版）

**Description**

Due to a bug, there are many duplicate folders in a file system. You are given a 2D array paths, where paths[i] is an array representing an absolute path to the ith folder in the file system.
Two folders (not necessarily on the same level) are identical if they contain the same non-empty set of identical subfolders and underlying subfolder structure. The folders do not need to be at the root level to be identical. If two or more folders are identical, then mark the folders as well as all their subfolders.
Once all the identical folders and their subfolders have been marked, the file system will delete all of them. The file system only runs the deletion once, so any folders that become identical after the initial deletion are not deleted.
Return the 2D array ans containing the paths of the remaining folders after deleting all the marked folders. The paths may be returned in any order.

**Examples**

**Example 1:**

```
Input: paths = [["a"],["c"],["d"],["a","b"],["c","b"],["d","a"]]
Output: [["d"],["d","a"]]
Explanation: The file structure is as shown.
Folders "/a" and "/c" (and their subfolders) are marked for deletion because they both contain an empty
folder named "b".
```

**Example 2:**

```
Input: paths = [["a"],["c"],["a","b"],["c","b"],["a","b","x"],["a","b","x","y"],["w"],["w","y"]]
Output: [["c"],["c","b"],["a"],["a","b"]]
Explanation: The file structure is as shown. 
Folders "/a/b/x" and "/w" (and their subfolders) are marked for deletion because they both contain an empty folder named "y".
Note that folders "/a" and "/c" are identical after the deletion, but they are not deleted because they were not marked beforehand.
```

**Example 3:**

```
Input: paths = [["a","b"],["c","d"],["c"],["a"]]
Output: [["c"],["c","d"],["a"],["a","b"]]
Explanation: All folders are unique in the file system.
Note that the returned array can be in a different order as the order does not matter.
```

**Constraints**

- 1 <= paths.length <= 2 * 104
- 1 <= paths[i].length <= 500
- 1 <= paths[i][j].length <= 10
- 1 <= sum(paths[i][j].length) <= 2 * 105
- path[i][j] consists of lowercase English letters.
- No two paths lead to the same folder.
- For any folder not at the root level, its parent folder will also be in the input.

---

## 题目（中文翻译）

由于系统 bug，文件系统中出现了许多重复的文件夹。给定一个二维数组 `paths`，其中 `paths[i]` 表示第 `i` 个文件夹的 **绝对路径（absolute path）**，即从根目录到该文件夹的文件夹名称序列。

两个文件夹（不必在同一层级）如果 **包含相同的非空子文件夹集合（subfolders）** 且其子文件夹的内部结构也完全相同，则认为这两个文件夹 **相同（identical）**。文件夹是否在根目录下并不影响相同的判定。

若有两个或更多文件夹相同，则把这些文件夹以及它们所有的子文件夹全部标记为待删除。  
所有相同文件夹及其子文件夹标记完成后，文件系统一次性删除所有被标记的文件夹。删除操作只执行一次，因此在首次删除后新产生的相同文件夹不会再被删除。

返回一个二维数组 `ans`，其中包含所有 **剩余文件夹的路径**。返回的路径顺序可以任意。

---

### 示例

**示例 1**

```text
Input: paths = [["a"],["c"],["d"],["a","b"],["c","b"],["d","a"]]
Output: [["d"],["d","a"]]
Explanation: 文件结构如图所示。文件夹 "/a" 与 "/c"（以及它们的子文件夹）被标记删除，因为它们都包含一个空的子文件夹 "b"。
```

**示例 2**

```text
Input: paths = [["a"],["c"],["a","b"],["c","b"],["a","b","x"],["a","b","x","y"],["w"],["w","y"]]
Output: [["c"],["c","b"],["a"],["a","b"]]
Explanation: 文件结构如图所示。文件夹 "/a/b/x" 与 "/w"（以及它们的子文件夹）被标记删除，因为它们都包含一个空的子文件夹 "y"。需要注意的是，删除后文件夹 "/a" 与 "/c" 变得相同，但它们不会再被删除，因为删除只执行一次。
```

**示例 3**

```text
Input: paths = [["a","b"],["c","d"],["c"],["a"]]
Output: [["c"],["c","d"],["a"],["a","b"]]
Explanation: 文件系统中的所有文件夹都是唯一的。返回数组的顺序可以不同，因为顺序不影响结果。
```

---

### 约束条件

- `1 <= paths.length <= 2 * 10^4`
- `1 <= paths[i].length <= 500`
- `1 <= paths[i][j].length <= 10`
- `1 <= sum(paths[i][j].length) <= 2 * 10^5`
- `paths[i][j]` 只包含小写英文字母
- 没有两条路径指向同一个文件夹
- 对于任意非根层级的文件夹，它的父文件夹必定也出现在输入中

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把所有文件夹逐个拿出来比较**，看它们的子文件夹结构是否完全一样。  
可以把每条 `paths[i]` 看成一条从根目录到某个文件夹的路径，例如 `["a","b","c"]` 就对应文件夹 **/a/b/c**。  

- **数据结构**：我们把所有路径存到一个列表里，然后对每两个文件夹 **逐层遍历**，比较它们的子文件夹集合是否相同。  
  - 把一个文件夹的子文件夹当成 **“字典”**（哈希表）来存，键是子文件夹的名字，值是该子文件夹的完整结构（递归的子字典）。  
  - 类比：字典就像一本**查字典**，你输入单词（子文件夹名字），就能快速找到对应的解释（子结构）。  

- **判断相同**：两个文件夹相同当且仅当  
  1. 它们拥有完全相同的子文件夹名字集合。  
  2. 对每一个子文件夹，递归它们的子结构也相同。  

- **为什么正确**：因为文件系统的结构就是一棵树（根目录 → 子文件夹 → …），只要每个节点的子树相同，整棵子树自然相同。  

- **时间/空间分析**：  
  - 对每一对文件夹我们都要遍历它们的子树。最坏情况（所有文件夹结构相同且层数很多）会导致 **O(N²·L)** 的比较，其中 `N` 是文件夹数量，`L` 是路径的最大深度。  
  - 为了快速找子文件夹，我们用了哈希表，查找是 **O(1)**，但仍然要遍历所有子节点。  
  - 额外的空间主要是存放每个文件夹的子字典，最坏 **O(N·L)**。  

> **大白话**：  
> - `O(N²·L)` 就像“我们要把每个人的生日派对和所有其他人的派对都比较一遍”，人数多了，工作量会指数级增长。  
> - `O(N·L)` 空间相当于“把每个人的派对名单都写下来”。  

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Dict, Tuple

# ---------- 1. 把所有路径构造成一棵树 ----------
class Node:
    """文件夹节点，children 用 dict 保存子文件夹，key 是文件夹名字"""
    def __init__(self):
        self.children: Dict[str, Node] = {}
        self.to_delete: bool = False   # 标记该节点是否需要被删除

def build_tree(paths: List[List[str]]) -> Node:
    root = Node()
    for p in paths:                     # 把每条路径插入树中
        cur = root
        for name in p:
            if name not in cur.children:
                cur.children[name] = Node()
            cur = cur.children[name]
    return root

# ---------- 2. 暴力比较两棵子树是否相同 ----------
def same_structure(a: Node, b: Node) -> bool:
    """递归判断两棵子树是否完全相同"""
    if set(a.children.keys()) != set(b.children.keys()):
        return False
    for name in a.children:            # 两棵子树的子文件夹名字一定相同
        if not same_structure(a.children[name], b.children[name]):
            return False
    return True

# ---------- 3. 暴力找出所有相同的文件夹 ----------
def mark_duplicates_bruteforce(root: Node) -> None:
    """遍历所有节点，两两比较相同的子树并标记"""
    # 把所有节点收集到列表，方便两两比较
    all_nodes: List[Tuple[Node, List[str]]] = []   # (节点, 从根到该节点的路径)

    def dfs(node: Node, path: List[str]) -> None:
        all_nodes.append((node, path[:]))
        for name, child in node.children.items():
            dfs(child, path + [name])

    dfs(root, [])

    n = len(all_nodes)
    for i in range(n):
        node_i, path_i = all_nodes[i]
        if node_i.to_delete:          # 已经被标记，无需再比较
            continue
        for j in range(i + 1, n):
            node_j, path_j = all_nodes[j]
            if node_j.to_delete:
                continue
            if same_structure(node_i, node_j):
                # 找到相同的子树，标记两棵子树以及它们的所有子节点
                def mark_subtree(node: Node) -> None:
                    node.to_delete = True
                    for child in node.children.values():
                        mark_subtree(child)
                mark_subtree(node_i)
                mark_subtree(node_j)
                break    # 同一棵子树已经被标记，跳出内部循环

# ---------- 4. 把未被标记的路径收集出来 ----------
def collect_paths(root: Node) -> List[List[str]]:
    ans: List[List[str]] = []

    def dfs(node: Node, path: List[str]) -> None:
        if not node.to_delete and path:          # 根节点本身不算路径
            ans.append(path[:])
        for name, child in node.children.items():
            dfs(child, path + [name])

    dfs(root, [])
    return ans

# ---------- 5. 主函数 ----------
def deleteDuplicateFolder_bruteforce(paths: List[List[str]]) -> List[List[str]]:
    root = build_tree(paths)
    mark_duplicates_bruteforce(root)
    return collect_paths(root)

# ==================== 示例 ====================
if __name__ == "__main__":
    example = [["a"],["c"],["d"],["a","b"],["c","b"],["d","a"]]
    print(deleteDuplicateFolder_bruteforce(example))
```

#### 复杂度  

- **时间复杂度**：`O(N²·L)`  
  - `N` 为文件夹数量，`L` 为最长路径的层数。  
  - 需要两两比较子树，最坏每次比较都要遍历完整子树。  
- **空间复杂度**：`O(N·L)`  
  - 用哈希表保存每个节点的子文件夹，另外递归栈深度最多 `L`。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“两两比较子树”**——这一步导致指数级的工作量。  
我们需要 **把子树的结构压缩成一个唯一的标识（哈希值）**，这样只要比较哈希值就能判断子树是否相同，时间就能降到线性。

**关键步骤**  

1. **构造 Trie（前缀树）**  
   - 把所有路径插入同一棵树。Trie 的每个节点代表一个文件夹，`children` 保存子文件夹。  
   - 类比：Trie 像一本**目录树**，根目录是书的封面，往下每层都是章节标题。  

2. **自底向上为每棵子树生成哈希**  
   - 对每个节点，先递归得到所有子节点的哈希值。  
   - 把子节点的 `(文件夹名字, 哈希值)` 按名字的字典序排好，然后拼成一个字符串 `name1#hash1|name2#hash2|...`。  
   - 对这个字符串再做一次哈希（这里直接用 Python 的 `hash()`，也可以用 `hashlib.sha256`），得到当前节点的 **结构哈希**。  
   - 如果两个节点的结构哈希相同，则它们的子树结构一定相同（哈希冲突极低，实际可以安全使用）。  

3. **统计每个哈希出现的次数**  
   - 用一个全局字典 `cnt[hash]` 记录出现次数。出现次数 ≥ 2 的哈希对应的子树需要被删除。  

4. **第二遍遍历标记需要删除的节点**  
   - 再次自顶向下遍历 Trie，若当前节点的哈希在 `cnt` 中出现 ≥ 2，则把该节点及其所有后代标记为删除。  

5. **收集未被删除的路径**  
   - 深度优先遍历 Trie，把所有没有被标记的节点路径加入答案。  

**为什么正确**  

- 哈希是 **自底向上** 生成的：子树的哈希只依赖于它的直接子节点的哈希以及子节点的名字。  
- 两个子树相同 ↔ 它们的子节点集合（名字+子树结构）完全相同 ↔ 哈希字符串完全相同 ↔ 哈希值相同。  
- 因此只要哈希值相同，就可以安全地认为两棵子树是“相同的”。  

**复杂度提升**  

- 只需要 **一次** 对每个节点计算哈希，**一次** 标记删除，**一次** 收集答案，整体是线性时间 `O(N·L)`。  

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Dict

# ---------- 1. Trie 节点 ----------
class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.hash_id: int = 0          # 当前子树的结构哈希（整数）
        self.to_delete: bool = False  # 是否需要被删除

# ---------- 2. 建树 ----------
def build_trie(paths: List[List[str]]) -> TrieNode:
    root = TrieNode()
    for p in paths:
        cur = root
        for name in p:
            if name not in cur.children:
                cur.children[name] = TrieNode()
            cur = cur.children[name]
    return root

# ---------- 3. 自底向上计算哈希 ----------
def compute_hash(node: TrieNode, cnt: Dict[int, int]) -> int:
    """
    返回 node 所在子树的唯一哈希，并在 cnt 中统计出现次数。
    哈希的生成方式：
        1. 对每个子节点，先递归得到它的哈希；
        2. 把 (子文件夹名字, 子哈希) 按名字排序；
        3. 拼成字符串 "name1#hash1|name2#hash2|..."；
        4. 对该字符串使用 Python 内置 hash（或自行实现）得到整数哈希。
    """
    if not node.children:               # 叶子节点（空文件夹）
        node.hash_id = hash("()")       # 固定哈希，所有空文件夹相同
        cnt[node.hash_id] += 1
        return node.hash_id

    parts = []
    for name, child in node.children.items():
        child_hash = compute_hash(child, cnt)   # 递归得到子哈希
        parts.append((name, child_hash))

    # 按名字排序，确保不同插入顺序得到相同的哈希
    parts.sort(key=lambda x: x[0])
    # 拼接成唯一字符串
    combined = "|".join(f"{name}#{h}" for name, h in parts)
    node.hash_id = hash(combined)
    cnt[node.hash_id] += 1
    return node.hash_id

# ---------- 4. 标记需要删除的子树 ----------
def mark_deletions(node: TrieNode, cnt: Dict[int, int]) -> None:
    """
    若当前节点的哈希出现次数 >= 2，则整棵子树都要删除。
    否则递归检查子节点。
    """
    if cnt[node.hash_id] >= 2:
        node.to_delete = True
        # 整棵子树直接标记，不必继续向下检查
        return
    for child in node.children.values():
        mark_deletions(child, cnt)

# ---------- 5. 收集未被删除的路径 ----------
def collect_paths(node: TrieNode, cur_path: List[str], ans: List[List[str]]) -> None:
    if node.to_delete:
        return                      # 被删除的子树直接跳过
    if cur_path:                    # 根节点本身不算路径
        ans.append(cur_path[:])
    for name, child in node.children.items():
        collect_paths(child, cur_path + [name], ans)

# ---------- 6. 主函数 ----------
def deleteDuplicateFolder(paths: List[List[str]]) -> List[List[str]]:
    # 1) 建树
    root = build_trie(paths)

    # 2) 计算哈希并统计出现次数
    cnt = defaultdict(int)          # 哈希 -> 出现次数
    compute_hash(root, cnt)

    # 3) 标记所有需要删除的子树
    mark_deletions(root, cnt)

    # 4) 收集答案
    ans: List[List[str]] = []
    collect_paths(root, [], ans)
    return ans

# ==================== 示例 ====================
if __name__ == "__main__":
    cases = [
        [["a"],["c"],["d"],["a","b"],["c","b"],["d","a"]],
        [["a"],["c"],["a","b"],["c","b"],["a","b","x"],["a","b","x","y"],["w"],["w","y"]],
        [["a","b"],["c","d"],["c"],["a"]]
    ]
    for p in cases:
        print(deleteDuplicateFolder(p))
```

#### 复杂度  

- **时间复杂度**：`O(N·L)`  
  - `N` 为文件夹数量，`L` 为最长路径层数。  
  - 每个节点只会被访问 **常数次**（一次计算哈希、一次标记、一次收集），所以整体线性。  

- **空间复杂度**：`O(N·L)`  
  - Trie 本身占用所有文件夹的结构。  
  - 递归深度最多 `L`，以及哈希计数表 `cnt` 的大小最多等于节点数。  

---

## 心得  

- **核心技巧**：**为每棵子树生成唯一哈希**（又称“子树同构哈希”），配合 **Trie** 把文件系统抽象成树结构。  
- **适用题型**（类似思路）  
  1. **找出二叉树中所有相同子树**（LeetCode 652）。  
  2. **删除重复的子文件夹**（本题的变形）。  
  3. **判断两棵树是否同构**（树同构问题）。  
- **解题钥匙**：**自底向上压缩子结构 → 用哈希快速比较**。

---

## 反思  

- **第一反应**：看到“相同的子文件夹结构”，立刻想到把文件系统建成一棵树（Trie），随后遍历比较。  
- **最容易踩的坑**  
  - **哈希冲突**：理论上可能，但实际使用 Python 的 `hash`（或更稳妥的 SHA）冲突概率极低。  
  - **子文件夹名字顺序**：若不对名字排序，同样结构但插入顺序不同会得到不同哈希。  
  - **标记删除的时机**：必须在所有哈希统计完以后再标记，否则会遗漏同层次的重复。  
  - **递归深度**：路径最深可达 500，Python 默认递归深度足够，但在极端情况下可以改为显式栈。  
- **下次类似题**：第一步先把数据抽象成**树/Trie**，第二步考虑**自底向上**把子结构压缩成**哈希**或**序列化字符串**，最后利用哈希计数找出重复。这样可以把“逐个比较”这种 O(N²) 的暴力操作，转化为 O(N) 的线性扫描。