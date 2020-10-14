# #1019. 链表中的下一个更大节点 / Next Greater Node In Linked List

> 难度：中等 · 标签：Array、Linked List、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/next-greater-node-in-linked-list/)

---

## 题目（英文原版）

**Description**

You are given the head of a linked list with n nodes.
For each node in the list, find the value of the next greater node. That is, for each node, find the value of the first node that is next to it and has a strictly larger value than it.
Return an integer array answer where answer[i] is the value of the next greater node of the ith node (1-indexed). If the ith node does not have a next greater node, set answer[i] = 0.

**Examples**

**Example 1:**

```
Input: head = [2,1,5]
Output: [5,5,0]
```

**Example 2:**

```
Input: head = [2,7,4,3,5]
Output: [7,0,5,5,0]
```

**Constraints**

- The number of nodes in the list is n.
- 1 <= n <= 104
- 1 <= Node.val <= 109

---

## 题目（中文翻译）

给定一个包含 **n** 个节点（node）的链表（linked list）的头节点 `head`。  
对于链表中的每个节点，找到 **下一个更大节点（next greater node）** 的值。即，对于每个节点，找到紧随其后的第一个节点，其值严格大于当前节点的值。  

返回一个整数数组（integer array）`answer`，其中 `answer[i]` 为第 **i** 个节点（按 1 索引）的下一个更大节点的值。如果第 **i** 个节点不存在下一个更大节点，则 `answer[i] = 0`。

**示例 1**  
**输入**: `head = [2,1,5]`  
**输出**: `[5,5,0]`

**示例 2**  
**输入**: `head = [2,7,4,3,5]`  
**输出**: `[7,0,5,5,0]`

**约束条件**  
- 链表中的节点数为 **n**。  
- `1 <= n <= 10^4`  
- `1 <= Node.val <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
把链表每个节点的值都记下来，**遍历**一次后得到一个普通的 Python 列表 `vals`（就像把一串珠子摞成一排）。  
然后对 `vals` 的每个位置 `i`，再往后看（`j = i+1 … len-1`），找到第一个比 `vals[i]` 大的数，就是答案。  

- **用到的数据结构**：  
  - **列表（array）**：把链表的值放进列表，方便随机访问。  
  - **双层循环**：外层遍历每个位置，内层向后寻找更大的值。  

> 类比：把一排学生的身高排好后，想知道每个学生后面第一个比他高的同学是谁，就得从他后面一个一个看。

- **为什么正确**：  
  对于第 `i` 个节点，内层循环检查了它后面的所有节点，必然会找到**第一个**满足“值更大”的节点（如果有的话），否则返回 `0`。这正是题目要求的“最近的更大节点”。  

- **时间/空间复杂度**：  
  - **时间**：外层遍历 `n` 次，内层最坏会遍历 `n-1, n-2, …, 1` 次，总共约 `n*(n-1)/2`，用大 O 记作 **O(n²)**。  
    - 大 O 的意义：只看数量级，忽略常数和低阶项。`n²` 表示当节点数翻倍时，运行时间会变成原来的 **四倍**。  
  - **空间**：额外用了一个长度为 `n` 的列表来存值和答案，**O(n)**。  

#### 代码（Python）  

```python
# 暴力解：双层循环
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def nextLargerNodes_bruteforce(head: ListNode):
    # 1. 把链表转成数组，方便下标访问
    vals = []
    cur = head
    while cur:
        vals.append(cur.val)      # 记录每个节点的值
        cur = cur.next

    n = len(vals)
    ans = [0] * n                 # 预先创建答案数组，默认全是 0

    # 2. 对每个位置 i，向后找第一个更大的数
    for i in range(n):
        # 从 i+1 开始向后扫描
        for j in range(i + 1, n):
            if vals[j] > vals[i]:    # 找到第一个更大的
                ans[i] = vals[j]     # 记录答案
                break                # 只要第一个就行，退出内层循环
        # 若没有更大的，ans[i] 保持为 0

    return ans
```

#### 复杂度  

- **时间复杂度**：**O(n²)** —— 两层循环导致每对节点最多比较一次。  
- **空间复杂度**：**O(n)** —— 需要额外的数组 `vals` 与答案 `ans`，每个长度为 `n`。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**“向后寻找”** 是瓶颈：每次都要遍历很多后面的节点，导致二次方时间。  
我们希望**只遍历一次**链表，就能直接得到每个节点的下一个更大值。  

**关键观察**：  
- 当我们从左到右（从链表头部向尾部）依次处理节点时，如果当前节点的值 **大于** 栈顶节点的值，那么栈顶节点的“下一个更大”一定是当前节点。因为栈顶节点之前的所有节点（在它左边）已经比它更大或已经找到了答案，**不会再受到后面更大的值影响**。  
- 因此我们可以维护一个 **单调递减栈**（栈里保存“还没有找到更大值的节点下标”），栈顶对应的值始终是**当前未解决节点中最小的**。当出现更大的值时，就把栈顶弹出并写入答案。

实现步骤如下：

1. **把链表转成数组**（这一步是为了用下标访问，便于把下标放进栈）。  
2. 创建答案数组 `ans`，全部初始化为 `0`。  
3. 初始化一个空栈 `stack`，栈中保存**数组下标**，而不是节点本身。  
4. 从左到右遍历数组 `vals`，下标记作 `i`，值记作 `v`。  
   - 当栈不为空且 `v > vals[stack[-1]]` 时，说明当前 `v` 是栈顶下标对应节点的下一个更大值。  
   - 弹出栈顶下标 `idx = stack.pop()`，把 `ans[idx] = v`。  
   - 继续检查栈顶，可能还有更小的节点也能被当前 `v` “解决”。  
   - 循环结束后，把当前下标 `i` 放进栈 `stack.append(i)`，表示它还没有找到更大的节点。  
5. 循环结束后，栈中剩余的下标对应的节点在其右侧没有更大的值，答案已经是默认的 `0`，不需要额外处理。

> **类比**：想象一排小朋友站成一列，老师手里拿着一块糖果（当前值）。如果糖果比站在队首的小朋友手里的糖果大，老师就把糖果送给他（弹出），然后继续检查下一个队首。老师只会把糖果送给**第一次**比他手里糖果大的小朋友，这正是“最近的更大”。  

**单调栈**的名字来源于：栈里保存的值始终保持**单调递减**（从栈底到栈顶）。  

#### 代码（Python）  

```python
def nextLargerNodes_optimal(head: ListNode):
    """
    使用单调递减栈，一次遍历求解下一个更大节点。
    返回一个列表 ans，ans[i] 为第 i 个节点的下一个更大节点的值（不存在则为 0）。
    """
    # 1. 链表转数组，便于下标操作
    vals = []
    cur = head
    while cur:
        vals.append(cur.val)
        cur = cur.next

    n = len(vals)
    ans = [0] * n          # 默认全部为 0
    stack = []             # 栈中只保存“未找到答案的下标”

    # 2. 单调栈遍历
    for i, v in enumerate(vals):
        # 当前值比栈顶对应的值大时，栈顶元素的答案就是当前值
        while stack and v > vals[stack[-1]]:
            idx = stack.pop()      # 弹出下标
            ans[idx] = v           # 填入答案
        # 把当前下标加入栈，等待以后可能出现的更大值
        stack.append(i)

    # 剩余在栈中的下标对应的节点右侧没有更大的值，答案已经是 0
    return ans
```

#### 复杂度  

- **时间复杂度**：**O(n)** —— 每个下标至多被压入栈一次、弹出一次，整体线性。相较于暴力的 O(n²)，提升显著。  
- **空间复杂度**：**O(n)** —— 需要存放数组 `vals`、答案 `ans`，以及最坏情况下全部 `n` 个下标的栈。  

---  

## 心得  

- **核心技巧**：**单调栈（Monotonic Stack）**——保持栈中元素单调递减，利用“当前更大值弹出栈顶”来一次遍历求解“下一个更大”。  
- **适用的题型**：  
  1. **Next Greater Element** 系列（数组版、循环版）。  
  2. **柱状图中最大的矩形面积**（利用单调栈求左右最近更小）。  
  3. **每日温度**（LeetCode 739）——找后面第一个更高温度。  
- **一句话总结**：  
  > “把还没找到答案的节点放进递减栈，遇到更大的数就一次性把它们的答案写上”。  

---  

## 反思  

- **第一反应**：直接想到把链表转成数组，再用两层循环暴力搜索。  
- **最容易踩的坑**：  
  - **下标 vs 节点**：在栈里保存下标而不是节点对象，否则比较时会混淆。  
  - **空链表或单节点**：需要保证代码能处理 `head` 为 `None`（LeetCode 保证至少 1 节点，但写通用代码时要考虑）。  
  - **整数范围**：节点值可达 `10⁹`，不影响算法，只要不要用固定大小的数组做索引。  
- **下次遇到同类题**，第一步应该想：“能否用单调栈把‘找下一个更大’的过程一次遍历完成？”  

祝你练习顺利，玩转单调栈！