# #2202. K 次移动后最大化顶部元素 / Maximize the Topmost Element After K Moves

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximize-the-topmost-element-after-k-moves/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums representing the contents of a pile, where nums[0] is the topmost element of the pile.
In one move, you can perform either of the following:
You are also given an integer k, which denotes the total number of moves to be made.
Return the maximum value of the topmost element of the pile possible after exactly k moves. In case it is not possible to obtain a non-empty pile after k moves, return -1.

**Examples**

**Example 1:**

```
Input: nums = [5,2,2,4,0,6], k = 4
Output: 5
Explanation:
One of the ways we can end with 5 at the top of the pile after 4 moves is as follows:
- Step 1: Remove the topmost element = 5. The pile becomes [2,2,4,0,6].
- Step 2: Remove the topmost element = 2. The pile becomes [2,4,0,6].
- Step 3: Remove the topmost element = 2. The pile becomes [4,0,6].
- Step 4: Add 5 back onto the pile. The pile becomes [5,4,0,6].
Note that this is not the only way to end with 5 at the top of the pile. It can be shown that 5 is the largest answer possible after 4 moves.
```

**Example 2:**

```
Input: nums = [2], k = 1
Output: -1
Explanation: 
In the first move, our only option is to pop the topmost element of the pile.
Since it is not possible to obtain a non-empty pile after one move, we return -1.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i], k <= 109

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的整数数组 `nums`，它表示一叠元素的内容，其中 `nums[0]` 为堆顶元素。  
在一次移动中，你可以执行以下两种操作之一：

1. **弹出**（pop）堆顶元素，使数组的第一个元素被移除。  
2. **推入**（push）任意一个已经被弹出的元素回到堆顶（即把该元素放在数组的最前面）。

同时，你还得到一个整数 `k`，表示必须恰好进行的移动次数。

返回恰好进行 `k` 次移动后，堆顶元素可能取得的 **最大值**。如果在恰好 `k` 次移动后不可能得到非空的堆，则返回 `-1`。

---

## 示例

### 示例 1
> **输入**  
> `nums = [5,2,2,4,0,6], k = 4`  
> **输出**  
> `5`  
> **解释**  
> 以下是一种在 4 步后让堆顶为 `5` 的操作序列：  
> - 第 1 步：弹出堆顶元素 `5`，堆变为 `[2,2,4,0,6]`。  
> - 第 2 步：弹出堆顶元素 `2`，堆变为 `[2,4,0,6]`。  
> - 第 3 步：弹出堆顶元素 `2`，堆变为 `[4,0,6]`。  
> - 第 4 步：将之前弹出的元素 `5` 推回堆顶，堆变为 `[5,4,0,6]`，此时堆顶为 `5`，是可能的最大值。

### 示例 2
> **输入**  
> `nums = [2], k = 1`  
> **输出**  
> `-1`  
> **解释**  
> 第一次移动只能弹出唯一的堆顶元素 `2`。由于此后堆为空，无法得到非空堆，故返回 `-1`。

---

## 约束

- `1 <= nums.length <= 10^5`
- `0 <= nums[i], k <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题本质上是让我们在 **恰好** 做 `k` 步操作后，使栈顶元素尽可能大。  
最直接的想法是 **把所有可能的操作序列枚举出来**，然后把每一种序列执行完后得到的栈顶值记下来，取最大值。

- **数据结构**：我们把 `nums` 看成一条“堆”——`nums[0]` 是最上面的那块石头。  
  为了模拟“弹出”和“重新放回”，可以使用 **列表**（相当于栈）以及另一个 **列表** 来存放已经弹出的石头（相当于“回收站”）。  
  - 列表就像 **抽屉**：往里放（`append`）或取出来（`pop`）都很快。  
  - “回收站”相当于 **字典**（哈希表）里存的 “已经弹出的石头”，但这里我们只需要一个普通列表就行。

- **为什么正确**：如果把**所有**合法的 `k` 步操作都穷举一遍，必然能找到让栈顶最大的那一种。

- **复杂度分析**：  
  - 每一步我们有两种选择（弹出或放回），所以总的可能序列数是 `2^k`（指数级增长）。  
  - 对每条序列我们都要维护两个列表，时间和空间都随 `k` 指数级增长。  
  - 用大白话说：如果 `k = 30`，我们得检查 `1,073,741,824` 种情况，根本不可能在几秒钟内算完。  
  - 因此暴力解的 **时间复杂度** 是 `O(2^k)`，**空间复杂度** 同样是 `O(k)`（递归栈深度）。

#### 代码（Python）

```python
def max_top_bruteforce(nums, k):
    """
    暴力搜索所有可能的 k 步操作，返回能够得到的最大栈顶值。
    只用于演示思路，实际会超时。
    """
    n = len(nums)
    best = -1                     # 记录全局最大

    def dfs(step, stack, removed):
        """
        step   : 已经执行的步数
        stack  : 当前堆（列表，stack[0] 为栈顶）
        removed: 已经弹出的元素（可以随时放回）
        """
        nonlocal best
        if step == k:             # 正好走完 k 步
            if stack:             # 栈不空，更新答案
                best = max(best, stack[0])
            return

        # 1）弹出栈顶（如果还有东西）
        if stack:
            top = stack.pop(0)    # 弹出最前面的元素
            removed.append(top)  # 放进“回收站”
            dfs(step + 1, stack, removed)
            # 回溯：把弹出的元素恢复到原位
            removed.pop()
            stack.insert(0, top)

        # 2）把已经弹出的任意元素放回栈顶（如果回收站非空）
        if removed:
            for i in range(len(removed)):
                elem = removed.pop(i)          # 取出一个已弹出的元素
                stack.insert(0, elem)          # 放到栈顶
                dfs(step + 1, stack, removed)
                # 回溯
                stack.pop(0)
                removed.insert(i, elem)

    dfs(0, nums[:], [])
    return best
```

> **注意**：上述代码在 `k` 超过 20 左右就会出现 **超时**，仅用来帮助大家理清“暴力思路”。

#### 复杂度

- **时间复杂度**：`O(2^k)` —— 每一步都有两种选择，指数级增长。  
- **空间复杂度**：`O(k)` —— 递归深度最多 `k`，以及保存的临时列表。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**真正影响答案的只有前面几块石头**，因为我们最多只能弹出 `k` 次。  
下面一步步抽丝剥茧，找到最简洁的计算方式。

1. **慢在哪里？**  
   - 暴力要枚举所有操作序列，而我们只需要知道 **哪些元素** 能够在第 `k` 步出现在栈顶。  
   - 只要知道「**可以让某个元素成为栈顶**」的条件，就不必真的去模拟每一步。

2. **观察**（从题目描述推导）  
   - **弹出**：每弹出一次，就把当前栈顶移走，栈顶变成 `nums[1]、nums[2] …`。  
   - **放回**：只能把**已经弹出的**元素放回栈顶，放回一次就消耗 1 步。

   因此，有两类“合法的”结束方式：

   - **方式 A**：直接弹 `k` 次（不放回），此时栈顶是 `nums[k]`（前提是 `k < n`，否则栈会空）。  
   - **方式 B**：弹 `i` 次（`0 ≤ i ≤ k-2`），然后 **放回** 任意一个已经弹出的元素（这一步耗掉第 `i+1` 步），剩下的 `k-(i+1)` 步可以随意在已经弹出的元素之间“弹出‑放回”循环，不会再影响栈顶。  
     - 关键是：只要 **弹出的次数 ≤ k-1**，我们就能在第 `k` 步把任意一次弹出的元素放回去。  
     - 所以 **第 `k` 步的栈顶** 可以是 **弹出过的前 `k-1` 个元素中的最大值**。

3. **特殊情况**  
   - `k = 0`：不动，答案就是原来的栈顶 `nums[0]`。  
   - `len(nums) = 1`：只有一块石头。  
     - 奇数次操作必然会把它弹出而无法再放回（因为放回需要额外一步），所以返回 `-1`。  
     - 偶数次操作可以把它弹出再放回，栈顶仍是它本身。  
   - `k = 1`：只能弹一次，不能放回，答案是 `nums[1]`（如果存在），否则 `-1`。

4. **综合**  
   - 设 `n = len(nums)`。  
   - **候选答案**：
     1. `nums[k]`（如果 `k < n`）。  
     2. `max(nums[0 : k-1])`（如果 `k > 1`，因为需要至少一次弹出再放回）。  
   - 取两者的最大值即为最终答案；若两者都不存在，则返回 `-1`。

5. **算法步骤**（伪代码）  

```
if k == 0: return nums[0]
if n == 1:
    return nums[0] if k % 2 == 0 else -1

ans = -inf
if k < n:                     # 方式 A
    ans = nums[k]

if k > 1:                     # 方式 B
    ans = max(ans, max(nums[0 : k-1]))

return ans if ans != -inf else -1
```

6. **为什么线性时间就能搞定？**  
   - 我们只需要查看 **前 `k-1` 个元素的最大值**，这可以在一次遍历中完成。  
   - `k` 可能比数组长度大，但我们只遍历到 `min(k-1, n-1)`，因此时间上最多是 `O(n)`（`n ≤ 10^5`），完全满足要求。

#### 代码（Python）

```python
def maximumTop(nums, k):
    """
    只用 O(n) 时间、O(1) 额外空间求出恰好 k 步后可以得到的最大栈顶值。
    """
    n = len(nums)

    # 0 步：直接返回原来的栈顶
    if k == 0:
        return nums[0]

    # 只有一块石头的特殊情况
    if n == 1:
        # 奇数步一定会把唯一的石头弹出，无法再放回
        return -1 if k % 2 == 1 else nums[0]

    # ans 用来记录所有合法的候选答案，初始设为一个非常小的数
    ans = float('-inf')

    # 方式 A：直接弹 k 次（如果 k < n），此时栈顶是 nums[k]
    if k < n:
        ans = nums[k]          # 这里不需要额外的循环

    # 方式 B：弹 i 次 (0 ≤ i ≤ k-2) 再放回一次，等价于取前 k-1 个元素的最大值
    if k > 1:
        # 只需要遍历到 min(k-1, n) 个位置即可
        limit = min(k - 1, n)   # 防止 k-1 超出数组范围
        max_prefix = max(nums[:limit])   # 前 limit 个元素的最大值
        ans = max(ans, max_prefix)

    # 如果 ans 仍然是 -inf，说明没有合法的结束状态（例如 k == 1 且 n == 1 已在上面处理）
    return int(ans) if ans != float('-inf') else -1
```

> **代码要点解释**  
> - `float('-inf')` 相当于「负无穷」，用来表示「目前没有找到合法答案」。  
> - `limit = min(k - 1, n)` 防止 `k-1` 超出数组长度，否则 `nums[:limit]` 会把整个数组都取出来。  
> - `max(nums[:limit])` 在 Python 中一次遍历就能得到最大值，时间复杂度 `O(limit)`。  

#### 复杂度

- **时间复杂度**：`O(min(k, n))` → 最坏情况下是 `O(n)`（因为我们最多遍历整个数组一次）。  
  - 与暴力解的 `O(2^k)` 相比，指数级下降到线性级，速度快了几个数量级。  
- **空间复杂度**：`O(1)`（只用了若干个额外的整数变量），不随输入规模增长。

---

## 心得

- **核心技巧**：把问题抽象为「哪些元素**有机会**在第 `k` 步出现在栈顶」而不是「到底怎么一步步操作」。  
- **适用的题型**  
  1. **只关心前缀** 的最大/最小值（如 “Maximum Subarray Sum After K Removals”）。  
  2. **固定步数后状态** 的贪心问题（如 “Maximum Top of a Stack After K Moves”、 “Maximum Value After K Deletions”。）  
- **一句话总结解题钥匙**：**只需要关注前 `k`（或 `k-1`） 个元素的最大值和第 `k` 个元素本身**，其余的元素永远不可能在恰好 `k` 步后成为栈顶。

---

## 反思

- **第一反应**：把所有操作枚举——这在面对“恰好 K 步”这种限制时很常见，但往往会导致指数爆炸。  
- **最容易踩的坑**  
  1. **数组长度为 1** 时的奇偶步数判断容易忘记。  
  2. **k = 1** 时只能弹一次，不能放回，需要单独处理。  
  3. **k > n**：直接弹完所有元素后还有剩余步数，此时只能利用“放回”操作，必须保证不把答案算成 `nums[k]`（因为 `k` 超界）。  
- **下次类似题目**：  
  1. **先思考“能出现的状态”**，而不是“怎么一步步到达”。  
  2. **找出限制条件的边界**（如 `k` 与数组长度的关系、奇偶性），先把这些特殊情况单独处理，再写通用公式。  

祝你在算法的旅程中，**多观察、多归纳，少暴力**！ 🚀