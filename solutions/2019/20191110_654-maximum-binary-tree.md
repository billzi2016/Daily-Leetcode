# #654. 最大二叉树 / Maximum Binary Tree

> 难度：中等 · 标签：Array、Divide and Conquer、Stack、Tree、Monotonic Stack、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/maximum-binary-tree/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums with no duplicates. A maximum binary tree can be built recursively from nums using the following algorithm:
Return the maximum binary tree built from nums.

**Examples**

**Example 1:**

```
Input: nums = [3,2,1,6,0,5]
Output: [6,3,5,null,2,0,null,null,1]
Explanation: The recursive calls are as follow:
- The largest value in [3,2,1,6,0,5] is 6. Left prefix is [3,2,1] and right suffix is [0,5].
    - The largest value in [3,2,1] is 3. Left prefix is [] and right suffix is [2,1].
        - Empty array, so no child.
        - The largest value in [2,1] is 2. Left prefix is [] and right suffix is [1].
            - Empty array, so no child.
            - Only one element, so child is a node with value 1.
    - The largest value in [0,5] is 5. Left prefix is [0] and right suffix is [].
        - Only one element, so child is a node with value 0.
        - Empty array, so no child.
```

**Example 2:**

```
Input: nums = [3,2,1]
Output: [3,null,2,null,1]
```

**Constraints**

- 1 <= nums.length <= 1000
- 0 <= nums[i] <= 1000
- All integers in nums are unique.

---

## 题目（中文翻译）

给定一个不含重复元素的整数数组 `nums`。可以使用如下递归算法从 `nums` 构建一棵最大二叉树（maximum binary tree）：

1. 在当前数组中找到最大值，将其作为根节点。  
2. 最大值左侧的子数组（subarray）递归构建左子树；右侧的子数组递归构建右子树。  
3. 对空数组返回 `null`（无子节点）。

返回由 `nums` 构建的最大二叉树的根节点。

## 示例

### 示例 1

**输入**  
``` 
nums = [3,2,1,6,0,5]
```

**输出**  
```
[6,3,5,null,2,0,null,null,1]
```

**解释**  
递归过程如下：

- 在 `[3,2,1,6,0,5]` 中最大值为 `6`，左侧前缀为 `[3,2,1]`，右侧后缀为 `[0,5]`。  
    - 在 `[3,2,1]` 中最大值为 `3`，左侧前缀为 `[]`，右侧后缀为 `[2,1]`。  
        - 空数组 → 无子节点。  
        - 在 `[2,1]` 中最大值为 `2`，左侧前缀为 `[]`，右侧后缀为 `[1]`。  
            - 空数组 → 无子节点。  
            - 只剩一个元素 `1`，因此该子节点为值为 `1` 的节点。  
    - 在 `[0,5]` 中最大值为 `5`，左侧前缀为 `[0]`，右侧后缀为 `[]`。  
        - 只剩一个元素 `0`，因此该子节点为值为 `0` 的节点。  
        - 空数组 → 无子节点。

### 示例 2

**输入**  
```
nums = [3,2,1]
```

**输出**  
```
[3,null,2,null,1]
```

## 约束

- `1 <= nums.length <= 1000`
- `0 <= nums[i] <= 1000`
- `nums` 中的所有整数均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是完全按照题目给出的递归描述来实现：

1. **找最大值**：在当前数组里找出最大的元素（相当于在一堆数里挑“最高的山峰”，这一步可以用线性扫描实现）。
2. **分左右子数组**：把最大值左边的所有元素当作左子树的数组，右边的所有元素当作右子树的数组。
3. **递归构造子树**：对左子数组、右子数组重复上面的过程，直到数组为空（相当于把山峰拆成更小的山峰）。

> **数据结构类比**  
> - **数组**就像一本顺序排好的书，左边的页码是“左子数组”，右边的页码是“右子数组”。  
> - **递归调用**相当于我们把一本书拆成左半本和右半本，再分别去找每本书里最大的章节。

只要每一步都按照上面规则去做，最终得到的二叉树一定是题目要求的 **Maximum Binary Tree**，因为我们始终把当前区间的最大值当作根节点。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点保存的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def constructMaximumBinaryTree(nums):
    """
    暴力递归实现
    :param nums: List[int] 没有重复元素的整数数组
    :return: TreeNode 树的根节点
    """
    # 递归终止条件：空数组没有节点
    if not nums:
        return None

    # 1️⃣ 找到当前数组的最大值及其索引
    max_val = max(nums)                # O(len(nums)) 的线性扫描
    max_idx = nums.index(max_val)      # 取得最大值所在的位置

    # 2️⃣ 创建根节点
    root = TreeNode(max_val)

    # 3️⃣ 递归构造左子树（左边的子数组）
    left_sub = nums[:max_idx]          # 左子数组
    root.left = constructMaximumBinaryTree(left_sub)

    # 4️⃣ 递归构造右子树（右边的子数组）
    right_sub = nums[max_idx + 1:]     # 右子数组
    root.right = constructMaximumBinaryTree(right_sub)

    return root
```

> **关键行注释**  
> - `max(nums)`：遍历一次数组找到最大值，这一步是“找最高山峰”。  
> - `nums[:max_idx]`、`nums[max_idx + 1:]`：把数组切成左、右两段，类似把书分成前后两册。  
> - 递归调用 `constructMaximumBinaryTree`：对每一本“小书”再重复同样的过程。

#### 复杂度

- **时间复杂度：** `O(n²)`  
  - 第一次找最大值需要遍历 `n` 次，第二层递归的子数组长度大约是 `n/2`，再找最大值又是 `O(n/2)`，如此往复，整体相当于 `n + (n-1) + (n-2) + … + 1 ≈ n²/2`。  
  - 大白话：如果 `n = 1000`，最坏情况下大概要做 500 000 次比较。

- **空间复杂度：** `O(n)`（递归栈）  
  - 递归深度最坏会等于数组长度（当数组是严格递增或递减时），每层调用都占用一次函数栈帧。  
  - 除了递归栈，额外的数组切片会产生 `O(n)` 的临时空间，但 Python 的切片是拷贝，实际占用也在同一个数量级。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每一次递归都要遍历一次子数组去找最大值**。如果我们能在一次遍历中直接知道每个元素的“父节点是谁”，就可以省掉所有的子数组扫描。

**关键观察**：  
- 对于任意一个元素 `x`，它的父节点一定是**左边最近且比它大的元素**或**右边最近且比它大的元素**中较小的那一个。  
- 换句话说，`x` 的父节点是“比 `x` 大的最近的山峰”，而这个最近的山峰可以用 **单调递减栈**（Monotonic Decreasing Stack）在一次遍历里找到。

**单调递减栈的工作原理**（把它想象成“装山峰的盒子”，盒子里从底到顶的山峰高度严格递减）：

1. 从左到右遍历数组。  
2. 当前元素 `num` 与栈顶元素比较：
   - 若 `num` **大于**栈顶，则栈顶元素找到了左侧最近更大的山峰（就是 `num`），于是把栈顶弹出，并把它设为 `num` 的左子树（因为弹出的元素在 `num` 左边且比它小）。  
   - 继续弹出，直到栈为空或栈顶大于等于 `num`。  
3. 弹完以后，如果栈不为空，说明栈顶是 `num` 左侧最近且更大的山峰，此时把 `num` 设为栈顶的 **右子树**（因为 `num` 位于栈顶右侧且比它小）。  
4. 最后把 `num`（对应的 `TreeNode`）压入栈中，等待后面的更大元素来处理它。

遍历结束后，栈底的节点就是整棵树的根，因为它没有左侧更大的山峰。

> **类比**：  
> 把数组想象成一排小朋友的身高，从左到右依次报数。我们用一个“只能放身高递减的队列”来记录**还没有找到更高朋友的孩子**。每当出现一个更高的孩子时，队列里比他矮的孩子都找到了“最近的更高的左边朋友”，于是出列并挂在新孩子的左侧。若队列里还有更高的孩子没出列，那新孩子就站在他们的右侧，成为他们的右孩子。

这样我们只遍历一次数组，所有的父子关系在遍历过程中即时确定，时间复杂度降到线性。

#### 代码（Python）

```python
# Definition for a binary tree node (同上)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def constructMaximumBinaryTree(nums):
    """
    单调递减栈 O(n) 解法
    :param nums: List[int] 不含重复元素的整数数组
    :return: TreeNode 树根
    """
    stack = []  # 栈中保存的是已经创建好的 TreeNode，栈顶对应最近的左侧更大元素

    for num in nums:
        cur = TreeNode(num)        # 为当前数创建节点
        # ① 处理左侧比 cur 小的节点：它们的最近更大左侧元素就是 cur
        while stack and stack[-1].val < num:
            popped = stack.pop()   # 弹出比 cur 小的节点
            # 弹出的节点一定是 cur 的左子树，因为它在 cur 左边且更小
            cur.left = popped

        # ② 处理栈顶仍然存在的情况：此时栈顶比 cur 大，是 cur 左侧最近更大的元素
        if stack:
            # cur 必须成为栈顶节点的右子树（因为 cur 在栈顶右侧且更小）
            stack[-1].right = cur

        # ③ 把当前节点压入栈中，等待以后可能出现的更大元素来处理它
        stack.append(cur)

    # 栈底的节点即为整棵树的根
    return stack[0] if stack else None
```

> **关键行注释**  
> - `while stack and stack[-1].val < num:`：只要栈顶比当前元素小，就把栈顶弹出并挂在当前节点左侧。  
> - `cur.left = popped`：弹出的节点是当前节点的左子树。  
> - `if stack: stack[-1].right = cur`：栈顶仍然比当前大，说明当前节点是栈顶的右子树。  
> - `stack.append(cur)`：把当前节点放进栈，等待更大的元素来“收养”它。

#### 复杂度

- **时间复杂度：** `O(n)`  
  - 每个元素最多进栈一次、出栈一次，所有操作的总次数不超过 `2n`。  
  - 大白话：如果数组长度是 1000，只需要大约 2000 次“进出栈”操作，远远快于 `n²` 的 500 000 次比较。

- **空间复杂度：** `O(n)`（栈的大小）  
  - 最坏情况下（数组严格递减）栈会一直增长到 `n`，相当于把所有节点都暂时保存在栈里。  
  - 除了栈本身，我们只创建了 `n` 个 `TreeNode`，这也是必须的。

---

## 心得

- **核心技巧**：**单调栈**（Monotonic Stack）——一种可以在一次遍历里找到“最近更大/更小元素”的数据结构。  
- **适用的题型**（类似思路）：  
  1. **Next Greater Element**（下一更大元素）  
  2. **Largest Rectangle in Histogram**（柱状图中最大的矩形）  
  3. **Trapping Rain Water**（接雨水）——都需要快速定位左右最近的更高柱子。  
- **一句话总结解题钥匙**：把“找左/右最近更大的元素”这件事交给单调递减栈，它能一次遍历帮你把父子关系全部搭建好。

---

## 反思

- **拿到题目第一反应**：直接照搬递归描述，先写出“找最大 → 分左右 → 递归” 的暴力实现。  
- **最容易踩的坑**：  
  - **递归深度**：对极端递增/递减数组会导致栈溢出（Python 递归层数默认 ~1000），需要手动调高递归限制或改用迭代。  
  - **空数组**：返回 `None`，否则会在后续访问属性时报错。  
  - **单调栈实现细节**：一定要先处理左侧更小的节点（`while` 循环），再处理栈顶仍在的情况，否则会把右子树挂错位置。  
- **下次遇到同类题**：第一步先思考“有没有办法一次遍历就确定左右最近更大的元素”，如果答案是 **是**，就尝试 **单调栈**；如果不是，再回到暴力递归或分治思路。