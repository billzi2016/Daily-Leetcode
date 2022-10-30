# #1993. 树上操作 / Operations on Tree

> 难度：中等 · 标签：Array、Hash Table、Tree、Depth-First Search、Breadth-First Search、Design · [LeetCode 链接](https://leetcode.com/problems/operations-on-tree/)

---

## 题目（英文原版）

**Description**

You are given a tree with n nodes numbered from 0 to n - 1 in the form of a parent array parent where parent[i] is the parent of the ith node. The root of the tree is node 0, so parent[0] = -1 since it has no parent. You want to design a data structure that allows users to lock, unlock, and upgrade nodes in the tree.
The data structure should support the following functions:
Implement the LockingTree class:

**Examples**

**Example 1:**

```
Input
["LockingTree", "lock", "unlock", "unlock", "lock", "upgrade", "lock"]
[[[-1, 0, 0, 1, 1, 2, 2]], [2, 2], [2, 3], [2, 2], [4, 5], [0, 1], [0, 1]]
Output
[null, true, false, true, true, true, false]

Explanation
LockingTree lockingTree = new LockingTree([-1, 0, 0, 1, 1, 2, 2]);
lockingTree.lock(2, 2);    // return true because node 2 is unlocked.
                           // Node 2 will now be locked by user 2.
lockingTree.unlock(2, 3);  // return false because user 3 cannot unlock a node locked by user 2.
lockingTree.unlock(2, 2);  // return true because node 2 was previously locked by user 2.
                           // Node 2 will now be unlocked.
lockingTree.lock(4, 5);    // return true because node 4 is unlocked.
                           // Node 4 will now be locked by user 5.
lockingTree.upgrade(0, 1); // return true because node 0 is unlocked and has at least one locked descendant (node 4).
                           // Node 0 will now be locked by user 1 and node 4 will now be unlocked.
lockingTree.lock(0, 1);    // return false because node 0 is already locked.
```

**Constraints**

- n == parent.length
- 2 <= n <= 2000
- 0 <= parent[i] <= n - 1 for i != 0
- parent[0] == -1
- 0 <= num <= n - 1
- 1 <= user <= 104
- parent represents a valid tree.
- At most 2000 calls in total will be made to lock, unlock, and upgrade.

---

## 题目（中文翻译）

给定一棵有 `n` 个节点的树，节点编号为 `0` 到 `n - 1`，以父节点数组 `parent` 的形式描述，其中 `parent[i]` 表示第 `i` 个节点的父节点。根节点是 `0`，因此 `parent[0] = -1` 表示它没有父节点。请设计一个数据结构，使用户能够对树上的节点进行 **锁定（lock）**、**解锁（unlock）** 和 **升级（upgrade）** 操作。

数据结构需要实现以下三个函数：

* `bool lock(int num, int user)`  
  - 若节点 `num` 当前未被锁定，则将其锁定给 `user`，返回 `true`；否则返回 `false`。

* `bool unlock(int num, int user)`  
  - 若节点 `num` 已被 `user` 锁定，则解除锁定，返回 `true`；否则返回 `false`。

* `bool upgrade(int num, int user)`  
  - 当且仅当满足以下全部条件时，才可对节点 `num` 执行升级操作并返回 `true`，否则返回 `false`：  
    1. 节点 `num` 当前未被锁定。  
    2. 节点 `num` 的 **子树（subtree）** 中至少存在一个已锁定的节点。  
    3. 节点 `num` 的所有 **祖先节点（ancestors）** 均未被锁定。  
  - 若升级成功，需要将节点 `num` 锁定给 `user`，并 **解锁（unlock）** 其子树中所有已锁定的节点。

实现上述 `LockingTree` 类，使其能够在最多 `2000` 次的 `lock`、`unlock`、`upgrade` 调用中保持高效。

---

## 示例

**示例 1：**

```json
Input
["LockingTree", "lock", "unlock", "unlock", "lock", "upgrade", "lock"]
[[[-1, 0, 0, 1, 1, 2, 2]], [2, 2], [2, 3], [2, 2], [4, 5], [0, 1], [0, 1]]
Output
[null, true, false, true, true, true, false]
```

**解释**

```java
LockingTree lockingTree = new LockingTree([-1, 0, 0, 1, 1, 2, 2]);
lockingTree.lock(2, 2);    // 返回 true，因为节点 2 未被锁定，随后被用户 2 锁定。
lockingTree.unlock(2, 3);  // 返回 false，因为节点 2 并未被用户 3 锁定。
lockingTree.unlock(2, 2);  // 返回 true，成功解锁节点 2。
lockingTree.lock(4, 5);    // 返回 true，节点 4 被用户 5 锁定。
lockingTree.upgrade(0, 1); // 返回 true，节点 0 未被锁定且其子树中有已锁定的节点（4），且没有锁定的祖先。于是锁定节点 0 给用户 1，并解锁节点 4。
lockingTree.lock(0, 1);    // 返回 false，因为节点 0 已被锁定。
```

---

## 约束条件

- `n == parent.length`
- `2 <= n <= 2000`
- `0 <= parent[i] <= n - 1`，`i != 0`
- `parent[0] == -1`
- `0 <= num <= n - 1`
- `1 <= user <= 10^4`
- `parent` 表示一棵有效的树
- `lock`、`unlock`、`upgrade` 的调用总次数不超过 `2000` 次

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

把题目翻成生活中的情景：  
- **树** 就像公司组织结构图，`0` 是总经理，下面是各部门经理、普通员工……  
- **锁** 相当于某个人把自己的办公桌占了（`user` 表示占用者的编号）。  
- **解锁** 必须是占用者自己才能把桌子腾出来。  
- **升级（upgrade）** 要求：  
  1. 这张桌子当前没人占（未锁）。  
  2. 下面的所有下属（子树）里至少有一张桌子被人占了。  
  3. 从这张桌子往上追溯的所有上级（祖先）都 **没有** 被占。  
  4. 满足以上条件后，这张桌子被指定的 `user` 占用，同时把所有下属已经占的桌子全部腾出来（解锁）。

最直接的做法就是**每次操作都去遍历整棵树**，检查是否满足条件，再执行对应的改动。  
我们需要的几种遍历：

| 操作 | 需要遍历的方向 | 用到的数据结构 |
|------|----------------|----------------|
| `lock`、`unlock` | 只看当前节点 | 直接查数组 `locked[node]` |
| `upgrade` | ① 向上找祖先是否被锁<br>② 向下找子树中所有被锁的节点 | 用 **父指针**（`parent` 数组）向上遍历，用 **邻接表**（children 列表）做深度优先搜索（DFS）向下遍历 |

- **哈希表**（这里用 Python 的 `dict`）可以把「哪个节点被哪个用户锁住」这件事记录下来，类似查字典：键是节点编号，值是占用者编号。  
- **邻接表** 把每个节点的所有孩子放在一个列表里，遍历子树时只需要按照这个列表递归下去。

**为什么暴力法一定能对？**  
因为我们把题目里所有的约束条件全部显式检查了一遍：  
- 先检查当前节点是否已经锁住（`lock`）或是否被同一个用户锁住（`unlock`）。  
- 再检查所有祖先是否全是未锁（`upgrade` 第 3 条），以及子树里是否至少有一个锁（`upgrade` 第 2 条）。  
- 最后把符合条件的子树节点全部解锁。  
只要遍历过程不漏掉任何节点，答案必然正确。

#### 代码（Python）

```python
class LockingTree:
    def __init__(self, parent):
        """
        parent[i] 表示节点 i 的父节点，-1 表示根节点
        """
        self.parent = parent                # 父指针数组，直接用来向上遍历
        self.n = len(parent)
        # 建立 children 邻接表，方便向下遍历子树
        self.children = [[] for _ in range(self.n)]
        for i, p in enumerate(parent):
            if p != -1:                      # 根节点没有父亲
                self.children[p].append(i)

        self.locked = {}                    # {node: user} 记录哪些节点被锁，以及锁的用户

    # ---------- 辅助函数 ----------
    def _has_locked_ancestor(self, node):
        """检查 node 往上是否有被锁的祖先，若有返回 True"""
        cur = self.parent[node]
        while cur != -1:
            if cur in self.locked:          # 祖先已经被锁
                return True
            cur = self.parent[cur]
        return False

    def _collect_locked_descendants(self, node, res):
        """
        深度优先遍历 node 的子树，把所有已锁的节点加入列表 res
        同时返回是否找到至少一个锁
        """
        for child in self.children[node]:
            if child in self.locked:        # 直接是锁住的子节点
                res.append(child)
            # 递归继续向下找
            self._collect_locked_descendants(child, res)

    # ---------- 接口 ----------
    def lock(self, num, user):
        """如果节点 num 未被锁，锁上并返回 True；否则返回 False"""
        if num in self.locked:              # 已经有人占了
            return False
        self.locked[num] = user             # 锁住
        return True

    def unlock(self, num, user):
        """只有当前锁的拥有者 user 才能解锁，成功返回 True"""
        if self.locked.get(num) != user:    # 没锁或不是同一个用户
            return False
        del self.locked[num]                # 删除锁记录
        return True

    def upgrade(self, num, user):
        """
        满足三条条件时：
        1. num 本身未锁
        2. 子树中至少有一个锁
        3. 所有祖先均未锁
        然后锁住 num，解锁子树中所有已锁节点，返回 True；否则返回 False
        """
        # 条件 1：自身未锁
        if num in self.locked:
            return False
        # 条件 3：祖先未锁
        if self._has_locked_ancestor(num):
            return False
        # 条件 2：子树中必须有锁
        locked_desc = []                    # 用来收集子树中所有已锁节点
        self._collect_locked_descendants(num, locked_desc)
        if not locked_desc:                 # 没有任何锁，升级失败
            return False

        # 满足所有条件，执行升级
        for v in locked_desc:               # 逐个解锁子树节点
            del self.locked[v]
        self.locked[num] = user             # 把当前节点锁上
        return True
```

> **关键行中文注释** 已在代码里标出，直接复制运行即可。

#### 复杂度  

- **时间复杂度**  
  - `lock`、`unlock`：只看一条记录 → **O(1)**（常数时间）。  
  - `upgrade`：  
    1. 向上遍历祖先最坏会走到根节点，树高 ≤ `n` → **O(n)**。  
    2. 向下遍历整棵子树，同样最坏会访问所有节点 → **O(n)**。  
    综合起来，**最坏情况 O(n)**，这里的 `n` 代表节点总数（最多 2000），在题目限制下完全可以接受。  

- **空间复杂度**  
  - `parent`、`children`、`locked` 三个结构各占 `O(n)`，额外的递归栈深度最多 `O(n)`。  
  - 因此总空间 **O(n)**。  
  - “O(n)” 只是一种数量级的说法，实际最多 2000 条记录，几乎可以忽略不计。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈主要在 **“向下遍历子树找锁”** 这一步：每次 `upgrade` 都要把整棵子树扫一遍，即使子树很大、而且大多数节点根本没有锁。  
我们可以 **把“子树里有多少锁”** 这个信息 **提前保存**，这样在 `upgrade` 时只需要查看一个计数，就能立刻判断第 2 条条件是否成立；同时在 `lock`、`unlock`、`upgrade` 时只需要在**路径上**（从节点到根）更新这些计数，复杂度从 `O(n)` 降到 `O(height)`，在最坏情况下仍是 `O(n)`，但常数更小，且思路更清晰。

**核心技巧：**  
- 为每个节点维护 `locked_desc_cnt`：它的子树（不包括自身）里被锁的节点数量。  
- 当 **锁定** 某个节点 `x` 时，沿着 `x` 的所有祖先把 `locked_desc_cnt` +1。  
- 当 **解锁** 某个节点 `x` 时，沿着祖先把 `locked_desc_cnt` -1。  
- 当 **升级** 成功后，先把子树中所有被锁的节点全部解锁（这一步仍需要遍历子树把 `locked_desc_cnt` 归零），随后把 `x` 本身锁住并把祖先的计数 +1。  

因为 **更新只在祖先链上**，而祖先链的长度等于树的高度，**高度 ≤ n**，但在平均情况下远小于 `n`（尤其是平衡树），所以整体效率更好。

下面把每一步拆得更细，帮助零基础的同学一步步跟上思路：

1. **构建孩子列表**（和暴力解一样），方便向下遍历。  
2. **额外维护两个字典**  
   - `locked[node] = user`（同暴力解）记录哪节点被谁锁。  
   - `desc_locked_cnt[node]`（整数）记录子树里锁的数量。初始都是 `0`。  
3. **实现 `lock`**  
   - 检查 `node` 是否已经锁，若未锁则把 `locked[node]=user`。  
   - 从 `node` 往上遍历父亲，依次把 `desc_locked_cnt[parent] += 1`。  
4. **实现 `unlock`**  
   - 必须先确认 `locked[node]==user`，否则直接返回 `False`。  
   - 删除 `locked[node]`，再沿祖先链把 `desc_locked_cnt[parent] -= 1`。  
5. **实现 `upgrade`**  
   - **① 检查自身未锁**：`node not in locked`。  
   - **② 检查祖先没有锁**：沿父指针往上看，只要遇到 `locked` 即返回 `False`。  
   - **③ 检查子树里有锁**：只要 `desc_locked_cnt[node] > 0` 即可，**不需要遍历子树**。  
   - **④ 收集并解锁所有子树中的锁**：这一步仍需要一次 DFS，把所有被锁的节点删掉，并在遍历过程中把对应祖先的 `desc_locked_cnt` 减 1（因为我们要把这些锁全部清除）。  
   - **⑤ 把当前节点锁住**：同 `lock` 的过程，只是一次性完成。  

这样，**除了第 ④ 步仍需遍历子树**（因为升级必须把所有子节点的锁全部解除），其余所有检查都是 **O(height)**，而 `height` 在本题的约束下最多 2000，整体仍然是线性可接受，但相比每次 `upgrade` 都全树遍历的暴力法要更省时。

#### 代码（Python）

```python
class LockingTree:
    def __init__(self, parent):
        self.parent = parent
        self.n = len(parent)

        # 建立 children 列表，方便向下遍历
        self.children = [[] for _ in range(self.n)]
        for i, p in enumerate(parent):
            if p != -1:
                self.children[p].append(i)

        # 记录锁的信息：node -> user
        self.locked = {}

        # 记录每个节点子树里（不包括自身）锁的数量
        self.desc_locked_cnt = [0] * self.n

    # ---------- 辅助 ----------
    def _has_locked_ancestor(self, node):
        """返回 True 表示 node 的任意祖先已被锁"""
        cur = self.parent[node]
        while cur != -1:
            if cur in self.locked:
                return True
            cur = self.parent[cur]
        return False

    def _dfs_collect_locked(self, node, collected):
        """
        深度优先遍历 node 的子树，收集所有已锁节点到 collected 中。
        同时把对应的祖先计数减 1（因为稍后会统一解锁）。
        """
        for child in self.children[node]:
            if child in self.locked:
                collected.append(child)
                # 解除锁后，要把祖先的子树锁计数减 1
                anc = self.parent[child]
                while anc != -1:
                    self.desc_locked_cnt[anc] -= 1
                    anc = self.parent[anc]
                del self.locked[child]            # 真正删除锁记录
            # 继续向下搜索
            self._dfs_collect_locked(child, collected)

    # ---------- 接口 ----------
    def lock(self, num, user):
        """如果 num 未被锁，则锁住并返回 True；否则返回 False"""
        if num in self.locked:
            return False
        self.locked[num] = user

        # 把所有祖先的子树锁计数 +1
        cur = self.parent[num]
        while cur != -1:
            self.desc_locked_cnt[cur] += 1
            cur = self.parent[cur]
        return True

    def unlock(self, num, user):
        """只有锁的拥有者才能解锁，成功返回 True"""
        if self.locked.get(num) != user:
            return False
        del self.locked[num]

        # 把所有祖先的子树锁计数 -1
        cur = self.parent[num]
        while cur != -1:
            self.desc_locked_cnt[cur] -= 1
            cur = self.parent[cur]
        return True

    def upgrade(self, num, user):
        """
        若满足：
        1. num 本身未锁
        2. 祖先全部未锁
        3. 子树里至少有一个锁
        则把子树中所有锁全部解除，再把 num 锁住，返回 True
        否则返回 False
        """
        # 条件 1
        if num in self.locked:
            return False
        # 条件 2
        if self._has_locked_ancestor(num):
            return False
        # 条件 3：子树锁计数大于 0 即可
        if self.desc_locked_cnt[num] == 0:
            return False

        # 收集并解除子树中所有锁
        locked_desc = []
        self._dfs_collect_locked(num, locked_desc)   # 这里已经把计数全部减掉

        # 最后把当前节点锁住（相当于一次普通 lock）
        self.locked[num] = user
        cur = self.parent[num]
        while cur != -1:
            self.desc_locked_cnt[cur] += 1
            cur = self.parent[cur]
        return True
```

> 代码里每一段关键操作都有中文注释，帮助你一步步看清「为什么要这么写」。

#### 复杂度  

- **时间复杂度**  
  - `lock`、`unlock`：沿祖先链更新计数，最坏 O(height) ≤ **O(n)**。  
  - `upgrade`：  
    1. 检查自身、祖先、子树计数 → O(height) + O(1)。  
    2. 若满足条件，需要一次 DFS 把子树里所有已锁节点解锁，这一步仍是 **O(k)**，其中 `k` 为子树中实际被锁的节点数（**不等同于子树大小**）。  
    综合来看，**最坏仍是 O(n)**，但在大多数情况下只遍历少量被锁节点，实际运行更快。  

- **空间复杂度**  
  - 额外的 `desc_locked_cnt` 列表占 **O(n)**。  
  - 递归 DFS 使用的调用栈深度 ≤ height ≤ **O(n)**。  
  - 总体仍是 **O(n)**，和暴力解持平，只是多了一点计数数组。

> 与暴力解对比：  
> - 暴力解每次 `upgrade` 必须遍历整棵子树（即使子树里没有锁），时间上是 **必遍 O(n)**。  
> - 优化解通过计数提前判断是否需要遍历，只有真的有锁的情况下才遍历子树，**平均情况更快**。  

---

## 心得  

- **核心技巧**：为每个节点维护「子树中被锁的数量」这类**额外信息**（前缀/后缀统计、树上差分），可以把原本需要**整棵遍历**的判断，转化为**常数时间**的查询，只在局部（祖先链）做更新。  
- **适用场景**：  
  1. **树上路径/子树查询**（如「子树中最大值」「子树节点个数」），常用 **树状数组 / 线段树 / 树上差分**。  
  2. **动态维护树的状态**（如「子树是否有被标记的节点」），可以用类似的计数或布尔标记。  
  3. **树形权限系统**（本题的锁/升级），需要快速判断祖先/子孙的状态。  
- **一句话总结**：  
  > “把子树的锁信息提前累计到每个节点上，查询时只看计数，更新时只改祖先链”，这就是解锁 `upgrade` 高效实现的钥匙。

---

## 反思  

- **第一反应**：看到 “锁、解锁、升级” 这三个操作，马上想到用哈希表记录锁的状态，然后 **每次都全树遍历** 检查祖先和子孙。  
- **最容易踩的坑**：  
  1. **忘记排除自身**：升级时要求“子树中至少有一个锁”，但**自身不能算**在子树计数里，需要在计数时排除当前节点。  
  2. **祖先锁的检测**：只检查父节点是不够，需要一直往上找到根。  
  3. **解锁时计数同步**：如果只在 `lock` 时增加计数，却忘了在 `unlock` 或 `upgrade` 时相应减掉，会导致后续判断错误。  
  4. **边界条件**：根节点的父亲是 `-1`，遍历时要小心不要把 `-1` 当作合法下标。  

- **下次类似题的第一步**：  
  > “先把树的结构（父子关系）弄清楚，然后想一想哪些查询可以通过**预处理/累计信息**在 O(1) 或 O(log n) 完成”。  
  对于需要频繁判断“子树里有没有满足条件的节点”，**计数/标记**往往是最直接的优化思路。