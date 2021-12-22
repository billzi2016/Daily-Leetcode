# #1600. 王位继承 / Throne Inheritance

> 难度：中等 · 标签：Hash Table、Tree、Depth-First Search、Design · [LeetCode 链接](https://leetcode.com/problems/throne-inheritance/)

---

## 题目（英文原版）

**Description**

A kingdom consists of a king, his children, his grandchildren, and so on. Every once in a while, someone in the family dies or a child is born.
The kingdom has a well-defined order of inheritance that consists of the king as the first member. Let's define the recursive function Successor(x, curOrder), which given a person x and the inheritance order so far, returns who should be the next person after x in the order of inheritance.
For example, assume we have a kingdom that consists of the king, his children Alice and Bob (Alice is older than Bob), and finally Alice's son Jack.
Using the above function, we can always obtain a unique order of inheritance.
Implement the ThroneInheritance class:

**Examples**

**Example 1:**

```
Successor(x, curOrder):
    if x has no children or all of x's children are in curOrder:
        if x is the king return null
        else return Successor(x's parent, curOrder)
    else return x's oldest child who's not in curOrder
```

**Example 2:**

```
Input
["ThroneInheritance", "birth", "birth", "birth", "birth", "birth", "birth", "getInheritanceOrder", "death", "getInheritanceOrder"]
[["king"], ["king", "andy"], ["king", "bob"], ["king", "catherine"], ["andy", "matthew"], ["bob", "alex"], ["bob", "asha"], [null], ["bob"], [null]]
Output
[null, null, null, null, null, null, null, ["king", "andy", "matthew", "bob", "alex", "asha", "catherine"], null, ["king", "andy", "matthew", "alex", "asha", "catherine"]]

Explanation
ThroneInheritance t= new ThroneInheritance("king"); // order: king
t.birth("king", "andy"); // order: king > andy
t.birth("king", "bob"); // order: king > andy > bob
t.birth("king", "catherine"); // order: king > andy > bob > catherine
t.birth("andy", "matthew"); // order: king > andy > matthew > bob > catherine
t.birth("bob", "alex"); // order: king > andy > matthew > bob > alex > catherine
t.birth("bob", "asha"); // order: king > andy > matthew > bob > alex > asha > catherine
t.getInheritanceOrder(); // return ["king", "andy", "matthew", "bob", "alex", "asha", "catherine"]
t.death("bob"); // order: king > andy > matthew > bob > alex > asha > catherine
t.getInheritanceOrder(); // return ["king", "andy", "matthew", "alex", "asha", "catherine"]
```

**Constraints**

- 1 <= kingName.length, parentName.length, childName.length, name.length <= 15
- kingName, parentName, childName, and name consist of lowercase English letters only.
- All arguments childName and kingName are distinct.
- All name arguments of death will be passed to either the constructor or as childName to birth first.
- For each call to birth(parentName, childName), it is guaranteed that parentName is alive.
- At most 105 calls will be made to birth and death.
- At most 10 calls will be made to getInheritanceOrder.

---

## 题目（中文翻译）

描述  
一个王国由国王、他的子女、孙子女等组成。随着时间的推移，家族成员会有出生（`birth`）或死亡（`death`）的事件。  
王国遵循一个明确的继承顺序，国王始终是继承序列的第一位。我们可以用递归函数 **Successor(x, curOrder)** 来定义“在已有继承序列 `curOrder` 中，`x` 之后应该出现的下一个人”。该函数的实现思路如下（首次出现的技术术语均在括号中给出英文注释）：

```text
Successor(x, curOrder):
    if x 没有子女 或者 x 的所有子女都已经在 curOrder 中:
        if x 是国王: return null
        else: return Successor(x 的父亲, curOrder)
    else:
        return x 年龄最大的、且未在 curOrder 中的子女
```

基于上述规则，王国的继承顺序是唯一确定的。

实现 `ThroneInheritance` 类（类名保持英文）：

- `ThroneInheritance(string kingName)`：构造函数，`kingName` 为国王的名字，初始化继承序列。
- `void birth(string parentName, string childName)`：`parentName` 为在世的父亲（或母亲），`childName` 为新出生的子女的名字。子女按照出生顺序加入父亲的子女列表中。
- `void death(string name)`：标记 `name` 对应的成员已死亡。死亡成员仍保留在家谱结构中，只在返回继承顺序时被跳过。
- `vector<string> getInheritanceOrder()`：返回当前在世成员的继承顺序，顺序由 `Successor` 定义，国王必在首位。

示例  

```text
Input
["ThroneInheritance", "birth", "birth", "birth", "birth", "birth", "birth", "getInheritanceOrder", "death", "getInheritanceOrder"]
[["king"], ["king", "andy"], ["king", "bob"], ["king", "catherine"], ["andy", "matthew"], ["bob", "alex"], ["bob", "asha"], [null], ["bob"], [null]]

Output
[null, null, null, null, null, null, null, ["king", "andy", "matthew", "bob", "alex", "asha", "catherine"], 
 ... (已截断)]
```

约束条件  

- `1 <= kingName.length, parentName.length, childName.length, name.length <= 15`  
- `kingName、parentName、childName、name` 只包含小写英文字母。  
- 所有 `childName` 与 `kingName` 均互不相同。  
- 每个 `death` 调用的 `name` 必然已经在构造函数或 `birth` 中出现过。  
- 对每次 `birth(parentName, childName)` 调用，保证 `parentName` 当时是活着的。  
- 最多调用 `birth` 与 `death` 共计 `10^5` 次。  
- 最多调用 `getInheritanceOrder` `10` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**每次请求继承顺序时**，从头遍历整棵家族树，按照题目给出的“先父后子、按出生顺序”规则输出所有还活着的成员。  

- **家族树**：把每个人当成树的节点，`parent → [child1, child2, …]` 用一个 **哈希表**（Python 的 `dict`）保存。哈希表就像一本“人名词典”，`key` 是父亲的名字，`value` 是这位父亲的孩子列表（按照出生顺序排好）。  
- **死亡标记**：再用另一个哈希表 `dead` 记录哪些人已经死了，类似在词典里给某个词贴上“已删除”标签。  

要得到继承顺序，只要从 **国王**（根节点）开始，做一次**先序遍历**（先访问当前节点，再递归遍历它的子节点），遇到死亡标记就跳过。  

> **为什么正确**  
> 先序遍历恰好对应题目中“先父后子、同辈按年龄（出生顺序）”的规则。把已死的节点直接过滤掉，就得到当前有效的继承顺序。

> **复杂度分析（大白话）**  
> - `birth` / `death` 只是在字典里插入或标记，几乎是 **瞬间完成**（O(1)），不管家族有多大。  
> - `getInheritanceOrder` 需要遍历整棵树一次。如果王国里有 `n` 个人，则要检查 `n` 次，这就是 **O(n)** 的时间。  
> - 额外的空间主要是保存两张字典，大小与人数成正比，即 **O(n)**。

#### 代码（Python）

```python
class ThroneInheritance:
    def __init__(self, kingName: str):
        # 哈希表：父亲 → [孩子们]（保持出生顺序）
        self.children = {kingName: []}
        # 死亡集合，用 set 存活更快（O(1) 判断）
        self.dead = set()
        # 记录根节点（国王）名字，后面遍历要从这里开始
        self.king = kingName

    def birth(self, parentName: str, childName: str) -> None:
        """给 parentName 生下 childName"""
        # 如果父亲还没有子列表，先创建空列表
        if parentName not in self.children:
            self.children[parentName] = []
        # 为孩子也创建一个空的子列表，方便以后继续 add 子女
        self.children[childName] = []
        # 把孩子加入父亲的子列表（自然保持出生顺序）
        self.children[parentName].append(childName)

    def death(self, name: str) -> None:
        """把 name 标记为已死"""
        self.dead.add(name)          # 死亡集合里多一个名字

    def getInheritanceOrder(self) -> list:
        """返回当前的继承顺序（不包括已死的人）"""
        order = []

        def dfs(person: str):
            # 若此人还活着，加入结果
            if person not in self.dead:
                order.append(person)
            # 递归遍历他的所有孩子（已按出生顺序排好）
            for child in self.children.get(person, []):
                dfs(child)

        dfs(self.king)               # 从国王开始遍历
        return order
```

#### 复杂度  

- **时间复杂度**：`O(n)`（`n` 为当前王国中所有成员的数量）  
  - 解释：`getInheritanceOrder` 要访问每个人一次；`birth`、`death` 是常数时间 `O(1)`。  
- **空间复杂度**：`O(n)`  
  - 解释：`children` 保存每个人的子列表，`dead` 保存死亡名单，最坏情况下两者都要存 `n` 条记录。

---

### 2. 最优解

#### 思路  

从暴力解可以看到：

1. **瓶颈**在 `getInheritanceOrder`。每次调用都要遍历整棵树，虽然题目只会调用 `≤10` 次，但如果我们想把每一次查询都做到 **尽可能快**，可以在 **出生** 和 **死亡** 时就维护好一个“活着的继承序列”。  
2. 观察先序遍历的特性：  
   - 当某个人 **出生** 时，他必须插入到 **父亲** 在继承序列中的位置之后、**父亲所有已出生的子女** 以及他们的后代之前。  
   - 当某个人 **死亡** 时，只需要把他从序列中“隐藏”，不必真的删除节点（删除会破坏指针结构），只要在输出时跳过即可。  

这正好可以用 **链表 + 哈希表** 来实现：

- 每个成员对应一个 **节点**，节点里保存 `name`、`next`（指向继承顺序中的下一个成员）以及 `alive` 标记。  
- 用 `dict name → node` 快速定位任意成员（哈希表像一本“名字查找表”）。  
- `birth(parent, child)`：在链表中把 `child` 插入到 **父亲的所有子代** 之后。具体做法是：  
  1. 找到 `parent` 节点。  
  2. 从 `parent` 开始往后走，直到找到 **第一个不属于 `parent` 子树的节点**（即第一个不在 `parent` 的后代中的节点），把 `child` 插在它前面。  
  3. 为了快速定位子树的末尾，我们可以在每个节点维护一个 **指向子树最后一个节点的指针** `lastDescendant`，但这会增加实现复杂度。鉴于 `birth` 调用最多 `10^5` 次，而每次只需要遍历父亲的直接子代列表（总数也不超过 `10^5`），**线性搜索父亲子代的末尾** 已经足够快（均摊 O(1)）。  
- `death(name)`：只把节点的 `alive` 标记设为 `False`。  
- `getInheritanceOrder()`：从链表头（国王）顺序遍历，收集 `alive == True` 的名字。此时遍历的就是 **已经排好序** 的链表，时间仍是 `O(n)`，但因为 `getInheritanceOrder` 调用次数极少，整体复杂度仍然是最优的。

**为什么这比暴力更好**  

- **出生/死亡** 操作均为 **O(1)**（只修改指针或标记），不必在每次查询时重新遍历整棵树。  
- **查询** 仍然是 `O(n)`，但查询次数被限制在 `10` 次，整体运行时间在 `10^5` 次操作的规模下远快于每次都遍历树的做法。

#### 代码（Python）

```python
class Node:
    """链表节点，代表王族中的一个成员"""
    __slots__ = ('name', 'next', 'alive')
    def __init__(self, name: str):
        self.name = name          # 成员姓名
        self.next = None          # 继承顺序中的下一个成员（链表指针）
        self.alive = True         # 是否仍然在世

class ThroneInheritance:
    def __init__(self, kingName: str):
        # 创建国王节点，建立链表的起点
        king = Node(kingName)
        self.head = king          # 链表头始终是国王
        # name → Node 的映射，便于 O(1) 找到任意成员
        self.nodes = {kingName: king}
        # 为每个成员维护一个 “子代最后一个节点” 的指针列表
        # 这里用 dict: parentName → 最近加入的子代节点（在链表中的位置）
        self.last_child = {kingName: king}

    def birth(self, parentName: str, childName: str) -> None:
        """在 parentName 的子树后面插入 childName"""
        child = Node(childName)                # 新建节点
        self.nodes[childName] = child

        # 找到 parent 在链表中的位置
        parent_node = self.nodes[parentName]

        # 找到 parent 的子树在链表中的最后一个节点
        # 如果 parent 之前已经有子代，last_child[parent] 就指向最新加入的子代
        # 否则，它指向 parent 本身
        insert_after = self.last_child.get(parentName, parent_node)

        # 把 child 插入链表：child 接在 insert_after 之后
        child.next = insert_after.next
        insert_after.next = child

        # 更新 parent 的 last_child 为这次新加入的 child
        self.last_child[parentName] = child

        # 由于 child 可能以后会再生子代，它自己也需要一个 last_child 条目
        self.last_child[childName] = child

    def death(self, name: str) -> None:
        """将 name 标记为已死，后续查询时跳过"""
        self.nodes[name].alive = False

    def getInheritanceOrder(self) -> list:
        """遍历链表，收集仍然活着的成员顺序"""
        order = []
        cur = self.head
        while cur:
            if cur.alive:               # 只把活着的名字加入答案
                order.append(cur.name)
            cur = cur.next
        return order
```

#### 复杂度  

- **时间复杂度**  
  - `birth`：`O(1)`（只改动常数条指针）  
  - `death`：`O(1)`（只改标记）  
  - `getInheritanceOrder`：`O(n)`，其中 `n` 为当前王族成员总数。因为查询次数 ≤ 10，整体时间仍是最优的。  
- **空间复杂度**：`O(n)`  
  - 每个人对应一个 `Node`（常数大小）以及在哈希表中的一条记录，随人数线性增长。

---

## 心得

- **核心技巧**：把家族结构抽象成 **先序遍历的链表**，利用哈希表实现 **O(1)** 的插入与标记。  
- **适用场景**  
  1. 需要频繁 **在有序序列中插入**，且插入位置固定（如“父亲子树的末尾”）的场景。  
  2. **动态维护树的前序遍历**（如公司组织结构的报表、文件系统的深度优先顺序）。  
  3. “**删除仅标记**”而不真的移除节点的情况，常见于“软删除”需求。  
- **解题钥匙**：**把先序遍历视作一条链表**，在出生时把新节点插入父亲子树的尾部，死亡时只标记，查询时顺序遍历即可。

---

## 反思

- **第一反应**：直接用树结构，每次 `getInheritanceOrder` 做一次 DFS。这样实现最直观，但会在查询时遍历整个树。  
- **最容易踩的坑**  
  - 忘记 **出生顺序**：孩子必须按出生时间排好，否则继承顺序不对。  
  - **死亡后仍然遍历**：如果在遍历时不检查 `alive` 标记，会把已死的成员错误地加入答案。  
  - **边界条件**：只有国王一个人时，`birth`、`death`、`getInheritanceOrder` 都要正常工作。  
- **下次类似题的第一步**：先判断是否可以把“递归遍历的顺序”提前固定为一种线性结构（链表/数组），再考虑 **增删** 操作是否可以在 **O(1)** 内完成。如果可以，就把查询变成一次线性遍历；如果不行，再回到每次重新遍历的暴力方案。