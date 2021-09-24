# #1487. 文件名唯一化 / Making File Names Unique

> 难度：中等 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/making-file-names-unique/)

---

## 题目（英文原版）

**Description**

Given an array of strings names of size n. You will create n folders in your file system such that, at the ith minute, you will create a folder with the name names[i].
Since two files cannot have the same name, if you enter a folder name that was previously used, the system will have a suffix addition to its name in the form of (k), where, k is the smallest positive integer such that the obtained name remains unique.
Return an array of strings of length n where ans[i] is the actual name the system will assign to the ith folder when you create it.

**Examples**

**Example 1:**

```
Input: names = ["pes","fifa","gta","pes(2019)"]
Output: ["pes","fifa","gta","pes(2019)"]
Explanation: Let's see how the file system creates folder names:
"pes" --> not assigned before, remains "pes"
"fifa" --> not assigned before, remains "fifa"
"gta" --> not assigned before, remains "gta"
"pes(2019)" --> not assigned before, remains "pes(2019)"
```

**Example 2:**

```
Input: names = ["gta","gta(1)","gta","avalon"]
Output: ["gta","gta(1)","gta(2)","avalon"]
Explanation: Let's see how the file system creates folder names:
"gta" --> not assigned before, remains "gta"
"gta(1)" --> not assigned before, remains "gta(1)"
"gta" --> the name is reserved, system adds (k), since "gta(1)" is also reserved, systems put k = 2. it becomes "gta(2)"
"avalon" --> not assigned before, remains "avalon"
```

**Example 3:**

```
Input: names = ["onepiece","onepiece(1)","onepiece(2)","onepiece(3)","onepiece"]
Output: ["onepiece","onepiece(1)","onepiece(2)","onepiece(3)","onepiece(4)"]
Explanation: When the last folder is created, the smallest positive valid k is 4, and it becomes "onepiece(4)".
```

**Constraints**

- 1 <= names.length <= 5 * 104
- 1 <= names[i].length <= 20
- names[i] consists of lowercase English letters, digits, and/or round brackets.

---

## 题目（中文翻译）

给定一个大小为 `n` 的字符串数组 `names`。你将在文件系统中创建 `n` 个文件夹，且在第 `i` 分钟时创建名称为 `names[i]` 的文件夹。  
由于两个文件夹不能拥有相同的名称，如果你尝试使用一个已经被使用过的名称，系统会在该名称后添加后缀 `(k)`，其中 `k` 是 **最小的正整数**，使得新得到的名称保持唯一。  
返回长度为 `n` 的字符串数组 `ans`，其中 `ans[i]` 为系统在创建第 `i` 个文件夹时实际分配的名称。

**示例 1**  
```text
Input: names = ["pes","fifa","gta","pes(2019)"]
Output: ["pes","fifa","gta","pes(2019)"]
Explanation: 让我们看看文件系统是如何生成文件夹名称的：
"pes"       → 之前未被使用，保持为 "pes"
"fifa"      → 之前未被使用，保持为 "fifa"
"gta"       → 之前未被使用，保持为 "gta"
"pes(2019)" → 之前未被使用，保持为 "pes(2019)"
```

**示例 2**  
```text
Input: names = ["gta","gta(1)","gta","avalon"]
Output: ["gta","gta(1)","gta(2)","avalon"]
Explanation: 让我们看看文件系统是如何生成文件夹名称的：
"gta"       → 之前未被使用，保持为 "gta"
"gta(1)"    → 之前未被使用，保持为 "gta(1)"
"gta"       → 名称已被占用，系统尝试添加后缀 (k)。由于 "gta(1)" 也已被占用，系统将 k 设为 2，得到 "gta(2)"
"avalon"    → 之前未被使用，保持为 "avalon"
```

**示例 3**  
```text
Input: names = ["onepiece","onepiece(1)","onepiece(2)","onepiece(3)","onepiece"]
Output: ["onepiece","onepiece(1)","onepiece(2)","onepiece(3)","onepiece(4)"]
Explanation: 当创建最后一个文件夹时，最小的可行正整数 k 为 4，因而得到名称 "onepiece(4)"。
```

**约束条件**  
- `1 <= names.length <= 5 * 10^4`  
- `1 <= names[i].length <= 20`  
- `names[i]` 仅由小写英文字母、数字和圆括号组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是：**每次遇到一个文件名，就检查它在已经创建的文件夹里出现过没有**。  
- 如果没有出现过，直接使用原名。  
- 如果已经出现过，就从 `k = 1` 开始尝试 `"name(k)"`，不断把 `k` 加一，直到找到一个在已使用集合中不存在的名字为止。  

这里用到的核心数据结构是 **集合（set）**，它可以看作是一本“已经用过的名字字典”。  
- `key` 就是已经创建的文件名，`value`（这里不需要）只是一种“是否在集合里”的标记。  
- 查询 `name in used_set` 的时间是 **O(1)**（像在字典里查单词的页码），但因为我们可能要循环尝试很多次 `k`，整体的时间会变得很慢。

这种做法一定能得到唯一的文件名，因为我们一直在寻找 **最小的正整数 k** 使得 `"name(k)"` 未被占用。

#### 代码（Python）

```python
def getFolderNames(names):
    used = set()               # 已经使用过的名字集合
    ans = []                   # 最终返回的答案

    for name in names:
        if name not in used:   # 直接可以使用
            ans.append(name)
            used.add(name)
        else:                  # 必须寻找最小的 k
            k = 1
            # 不断尝试 name(k) 直到找到未使用的
            while f"{name}({k})" in used:
                k += 1
            new_name = f"{name}({k})"
            ans.append(new_name)
            used.add(new_name) # 把新名字也加入集合
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n²)`（最坏情况）  
  - `n` 为文件夹数量。  
  - 当大量相同名字出现时（例如 `["a","a","a",...]`），第 `i` 个名字要尝试 `i-1` 次才能找到可用的后缀，导致总操作次数约为 `1 + 2 + … + (n‑1) = O(n²)`。  
  - 用大白话说，就是如果你每次都要从头数到第几次才能找到空位，工作量会像跑步一样越跑越慢。

- **空间复杂度：** `O(n)`  
  - 需要存放所有已经使用过的名字，最多会有 `n` 个。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次冲突都要从 1 开始线性搜索**，会重复检查已经确认不行的后缀。  
我们可以用 **哈希表（字典）** 记住每个“原始名字”对应的**下一个可以尝试的最小 k**，这样就能直接跳到可能的答案，省去无用的循环。

具体做法：

1. 用 `next_k` 字典记录：`next_k[original_name] = smallest_k_not_used`。  
   - 初始时若名字从未出现，`next_k[name] = 1`（表示下次冲突时从 1 开始尝试）。  
2. 同时仍然维护 `used` 集合记录所有已经分配的完整名字（包括带后缀的）。
3. 遍历每个 `name`  
   - **如果 `name` 未被占用**：直接使用，`used.add(name)`，并把 `next_k[name]` 初始化为 `1`（因为以后可能会冲突）。  
   - **如果 `name` 已被占用**：从 `k = next_k[name]` 开始尝试，形成 `candidate = f"{name}({k})"`。  
     - 若 `candidate` 仍在 `used` 中，说明这个 `k` 已经被别的冲突占用了，需要把 `k` 加一继续尝试。  
     - 当找到未占用的 `candidate` 时，将其加入 `used`，并把 `next_k[name] = k + 1`（下次再冲突时直接从下一个整数开始），同时把 `next_k[candidate] = 1`（因为这个新名字也可能以后被再次冲突）。  

这样，每个原始名字的 `k` 只会 **单调递增**，不会回头检查已经确认不行的数字。整个过程对每个名字的处理时间均摊为 **O(1)**，总时间为 **O(n)**。

> **类比**：想象你在图书馆登记新书名，如果某本书名已经被占用，你会在登记表上写下“下一个可用的编号是 5”。下次再遇到同名书时，你直接去看表格，直接尝试编号 5，而不是从 1 一次次往上数。

#### 代码（Python）

```python
def getFolderNames(names):
    used = set()                # 已经使用过的完整名字
    next_k = dict()             # name -> 下一个可尝试的最小 k
    ans = []

    for name in names:
        # 情况一：名字未被占用，直接使用
        if name not in used:
            ans.append(name)
            used.add(name)
            next_k[name] = 1    # 初始化，下次冲突从 1 开始尝试
        else:
            # 情况二：名字已被占用，需要找最小的 k
            k = next_k.get(name, 1)   # 若字典里没有，默认从 1 开始
            while True:
                candidate = f"{name}({k})"
                if candidate not in used:
                    break            # 找到未占用的 candidate
                k += 1               # 继续尝试更大的 k

            ans.append(candidate)
            used.add(candidate)

            # 更新两个哈希表的状态
            next_k[name] = k + 1       # 原名下次从 k+1 开始
            next_k[candidate] = 1      # 新名字首次出现，后续若冲突从 1 开始

    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 每个名字只会在哈希表中查找、写入常数次。即使在 `while` 循环中多次尝试 `k`，因为每次尝试后 `next_k[name]` 会被更新为更大的值，整体上每个 `k` 只会被检查一次，类似“摊销分析”。  
  - 用通俗的话说：虽然有时要“往前走几步”，但每一步只走一次，不会重复回头。

- **空间复杂度：** `O(n)`  
  - `used` 集合和 `next_k` 字典最多各保存 `n` 条记录，和输入规模线性相关。

---

## 心得

- **核心技巧**：使用哈希表记录“下一个可用的后缀编号”，把线性搜索转化为常数时间查找。  
- **适用场景**：  
  1. **文件/目录去重**（本题）。  
  2. **用户名唯一化**（如注册系统需要在已有用户名后加数字）。  
  3. **自增序列分配**（如给同类任务分配唯一的编号）。  
- **一句话总结**：**“冲突时记住下一个可用的编号，直接跳过去”**。

---

## 反思

- **第一反应**：看到“如果名字已经出现，就加 (k)”，本能想到循环尝试 `k = 1,2,…`，于是写出暴力版。  
- **最容易踩的坑**：  
  - 忘记把带后缀的新名字也加入哈希表，导致后续再次冲突时找不到已占用的后缀。  
  - `while` 循环里只检查 `candidate` 是否在 `used`，而没有同步更新 `next_k`，会导致同一个原名多次重复检查已失败的 `k`。  
  - 边界情况：名字本身已经包含类似 `"(1)"` 的后缀（如 `"a(1)"`），仍需视作普通字符串，不要误判为已经是 “带后缀” 的形式。  
- **下次遇到同类题**：第一步先思考 **“冲突后如何快速跳过已经占用的选项”**，看看能否用哈希表或其他数据结构记住“下一个候选”。这样可以把潜在的 `O(n²)` 降到 `O(n)`。