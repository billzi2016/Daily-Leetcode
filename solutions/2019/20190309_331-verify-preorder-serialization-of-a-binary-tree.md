# #331. 验证二叉树的前序序列化 / Verify Preorder Serialization of a Binary Tree

> 难度：中等 · 标签：String、Stack、Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/verify-preorder-serialization-of-a-binary-tree/)

---

## 题目（英文原版）

**Description**

One way to serialize a binary tree is to use preorder traversal. When we encounter a non-null node, we record the node's value. If it is a null node, we record using a sentinel value such as '#'.
For example, the above binary tree can be serialized to the string "9,3,4,#,#,1,#,#,2,#,6,#,#", where '#' represents a null node.
Given a string of comma-separated values preorder, return true if it is a correct preorder traversal serialization of a binary tree.
It is guaranteed that each comma-separated value in the string must be either an integer or a character '#' representing null pointer.
You may assume that the input format is always valid.
Note: You are not allowed to reconstruct the tree.

**Examples**

**Example 1:**

```
Input: preorder = "9,3,4,#,#,1,#,#,2,#,6,#,#"
Output: true
```

**Example 2:**

```
Input: preorder = "1,#"
Output: false
```

**Example 3:**

```
Input: preorder = "9,#,#,1"
Output: false
```

**Constraints**

- 1 <= preorder.length <= 104
- preorder consist of integers in the range [0, 100] and '#' separated by commas ','.

---

## 题目（中文翻译）

一种对 **二叉树**（binary tree）进行序列化的方法是使用 **前序遍历**（preorder traversal）。遍历时遇到非空节点，就记录该节点的值；遇到空节点，则使用哨兵值（sentinel value）如 `#` 进行记录。

例如，上图中的二叉树可以序列化为字符串 `"9,3,4,#,#,1,#,#,2,#,6,#,#"`，其中 `#` 代表空节点。

给定一个由逗号分隔的值组成的字符串 `preorder`，如果它是二叉树的合法前序遍历序列化结果，返回 `true`；否则返回 `false`。  
保证字符串中的每个逗号分隔值要么是整数，要么是表示空指针的字符 `#`。可以假设输入格式始终有效。  
**注意**：不能通过重建树来判断。

---

### 示例

**示例 1**  
```
Input: preorder = "9,3,4,#,#,1,#,#,2,#,6,#,#"
Output: true
```

**示例 2**  
```
Input: preorder = "1,#"
Output: false
```

**示例 3**  
```
Input: preorder = "9,#,#,1"
Output: false
```

---

### 约束条件

- `1 <= preorder.length <= 10^4`
- `preorder` 只包含范围在 `[0, 100]` 的整数和 `#`，并由逗号 `,` 分隔。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直观的想法是**把序列真的按先序遍历“重建”成一棵二叉树**，随后检查：

1. 能否完整地把所有节点都接上（即没有多余或缺失的节点）。  
2. 重建结束后，序列中不应该还有剩余的字符。

实现时可以把输入的字符串按 `,` 分割得到一个 token 列表，然后用递归模拟先序遍历：

```
读取下一个 token
如果是 '#': 这是一颗空树，直接返回
否则: 创建一个普通节点
      递归构造左子树
      递归构造右子树
```

如果在递归过程中出现“已经没有 token 但仍然需要读取”或递归结束后还有未使用的 token，则说明序列不合法。

> **类比**：想象我们有一本《树的先序遍历手册》，每读到一个词（节点值）就要在纸上画出对应的节点，并继续在左、右子树上写下后面的词。如果手册里的词写完了我们还没画完树，或者画完树后手册还有剩余词，那手册肯定写错了。

**正确性**：递归过程严格遵循先序遍历的定义：先根、再左、最后右。只要所有 token 都恰好被消耗完，且每个非空节点恰好拥有两个子位置（左、右），序列必然对应唯一的一棵二叉树。

**复杂度**：

- **时间**：每个 token 只会被访问一次，故是 **O(n)**（n 为 token 数）。  
- **空间**：递归栈深度最坏等于树的高度，最坏情况下等于 n（所有节点都是左子节点），因此 **O(n)** 的额外空间。

#### 代码（Python）

```python
def isValidSerialization_brute(preorder: str) -> bool:
    # 把字符串切成 token 列表
    tokens = preorder.split(',')
    # 用一个可变的索引模拟“指针”，在递归里移动
    index = 0

    def helper() -> bool:
        """尝试从 tokens[index] 开始构造一棵子树，成功返回 True，
           并把 index 前进到下一个未使用的 token 位置。"""
        nonlocal index
        # 若已经没有 token 可读，说明序列提前结束
        if index >= len(tokens):
            return False
        cur = tokens[index]
        index += 1                # “消费”当前 token

        if cur == '#':            # 空节点，不需要再递归
            return True
        # 非空节点，需要先构造左子树，再构造右子树
        left_ok = helper()
        if not left_ok:           # 左子树非法，直接返回
            return False
        right_ok = helper()
        return right_ok           # 右子树合法则整棵子树合法

    # 从根开始尝试构造
    ok = helper()
    # 只能在所有 token 都被消耗且构造成功时返回 True
    return ok and index == len(tokens)
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 每个 token 只访问一次。  
- **空间复杂度**：`O(n)` —— 递归调用栈最坏会达到 n（相当于一条链状的树）。

---

### 2. 最优解

#### 思路  

虽然上面的递归已经是 `O(n)` 时间，但它使用了 **递归栈**（最坏 `O(n)` 空间），而题目并不要求真的构造树，只要判断序列是否合法即可。  
我们可以把“树的构造过程”抽象成 **“槽位（slot）”** 的概念：

- 每个非空节点会 **占用** 一个槽位（因为它要挂在某个父节点的左/右位置上），但它会 **产生** 两个新的槽位（分别给左、右子树）。
- 每个 `#`（空节点）只 **占用** 一个槽位，不会产生新的槽位。

如果把所有槽位看成“可放置节点的位置”，则：

1. 初始时根节点拥有 **1** 个槽位。  
2. 依次遍历序列的每个 token：  
   - **先消耗** 一个槽位（因为当前 token 必须挂到某个位置）。如果此时没有可用槽位，说明序列已经出现了“多余的节点”，非法。  
   - 如果 token 是非空节点，则 **再增加** 两个槽位（为它的左右子树预留位置）。  
   - 如果是 `#`，则不增加槽位（因为它本身就是一个空位的结束）。

遍历结束后，**剩余的槽位必须恰好为 0**，否则说明还有未被填满的空位（比如只出现了根节点但缺少子树），同样非法。

> **类比**：想象你在排队买票，每个人买票后会得到两张新票（可以让两个人进入）。空位（`#`）只用掉一张票，不再产生新票。整个过程必须恰好把所有票用完，不能多也不能少。

**关键点**：我们只需维护一个整数 `slots`，不需要额外的数据结构，空间 **O(1)**。

#### 代码（Python）

```python
def isValidSerialization(preorder: str) -> bool:
    # 初始只有根节点的一个槽位
    slots = 1
    for token in preorder.split(','):
        # 每读到一个节点，都要先占用一个槽位
        slots -= 1
        if slots < 0:                     # 没槽位可占，说明非法
            return False
        if token != '#':                  # 非空节点会再产生两个槽位
            slots += 2
    # 最终槽位必须恰好为 0，才算完整匹配
    return slots == 0
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次序列。  
- **空间复杂度**：`O(1)` —— 只使用了一个整数变量 `slots`，不随输入规模增长。

> 与暴力递归相比，时间相同但 **空间大幅降低**（从最坏 `O(n)` 降到 `O(1)`），而且代码更简洁、没有递归深度风险。

---

## 心得

- **核心技巧**：把树的结构抽象为“槽位（可用位置）”，利用 **入度/出度平衡** 的思想快速判断序列合法性。  
- **适用题型**：  
  1. 验证二叉树的序列合法性（本题）。  
  2. 判断二叉树的后序序列是否有效（同理可改写）。  
  3. 通过入度/出度判断有向图是否形成合法的树结构（LeetCode 261）。
- **一句话总结**：**“每读一个节点先消掉一个位置，再根据节点类型补充新位置，最后槽位恰好归零则合法”。**

---

## 反思

- **第一反应**：把序列真的还原成树，然后检查是否完整。  
- **最容易踩的坑**：  
  - 忘记在读取每个 token 前先 **消耗**一个槽位，导致最终 `slots` 永远大于 0。  
  - 没有在遍历中即时检测 `slots < 0`，会在后面才发现错误，失去 **早退出** 的优势。  
  - 对空节点 `#` 的处理错误（把它当成产生新槽位的节点）。  
- **下次思路**：遇到“序列化/遍历合法性”这类题目，第一步就思考 **“每个元素对结构的贡献（增/减）”**，尝试用计数或栈来模拟结构变化，而不是直接重建。这样往往能得到 **O(1) 空间** 的最优解。