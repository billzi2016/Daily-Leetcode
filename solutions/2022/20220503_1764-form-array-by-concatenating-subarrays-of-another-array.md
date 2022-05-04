# #1764. **通过拼接另一个数组的子数组形成数组** / Form Array by Concatenating Subarrays of Another Array

> 难度：中等 · 标签：Array、Two Pointers、Greedy、String Matching · [LeetCode 链接](https://leetcode.com/problems/form-array-by-concatenating-subarrays-of-another-array/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array groups of length n. You are also given an integer array nums.
You are asked if you can choose n disjoint subarrays from the array nums such that the ith subarray is equal to groups[i] (0-indexed), and if i > 0, the (i-1)th subarray appears before the ith subarray in nums (i.e. the subarrays must be in the same order as groups).
Return true if you can do this task, and false otherwise.
Note that the subarrays are disjoint if and only if there is no index k such that nums[k] belongs to more than one subarray. A subarray is a contiguous sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: groups = [[1,-1,-1],[3,-2,0]], nums = [1,-1,0,1,-1,-1,3,-2,0]
Output: true
Explanation: You can choose the 0th subarray as [1,-1,0,1,-1,-1,3,-2,0] and the 1st one as [1,-1,0,1,-1,-1,3,-2,0].
These subarrays are disjoint as they share no common nums[k] element.
```

**Example 2:**

```
Input: groups = [[10,-2],[1,2,3,4]], nums = [1,2,3,4,10,-2]
Output: false
Explanation: Note that choosing the subarrays [1,2,3,4,10,-2] and [1,2,3,4,10,-2] is incorrect because they are not in the same order as in groups.
[10,-2] must come before [1,2,3,4].
```

**Example 3:**

```
Input: groups = [[1,2,3],[3,4]], nums = [7,7,1,2,3,4,7,7]
Output: false
Explanation: Note that choosing the subarrays [7,7,1,2,3,4,7,7] and [7,7,1,2,3,4,7,7] is invalid because they are not disjoint.
They share a common elements nums[4] (0-indexed).
```

**Constraints**

- groups.length == n
- 1 <= n <= 103
- 1 <= groups[i].length, sum(groups[i].length) <= 103
- 1 <= nums.length <= 103
- -107 <= groups[i][j], nums[k] <= 107

---

## 题目（中文翻译）

你得到一个长度为 `n` 的二维整数数组 `groups`，以及一个一维整数数组 `nums`。  
请判断是否可以从 `nums` 中挑选出 `n` 个互不相交的子数组（subarray），使得第 `i` 个子数组（0 起索引）恰好等于 `groups[i]`，并且当 `i > 0` 时，第 `i‑1` 个子数组在 `nums` 中出现在第 `i` 个子数组之前（即子数组的顺序必须与 `groups` 中的顺序一致）。  

如果可以完成上述任务，返回 `true`；否则返回 `false`。  

**说明**  
- 只有当不存在下标 `k` 使得 `nums[k]` 同时属于两个子数组时，这些子数组才视为互不相交。  
- 子数组是数组中**连续的序列**（contiguous sequence）的一段。  

### 示例

#### 示例 1  
**输入**  
```json
groups = [[1,-1,-1],[3,-2,0]], 
nums = [1,-1,0,1,-1,-1,3,-2,0]
```  
**输出**  
```
true
```  
**解释**  
可以选择第 0 个子数组为 `[1,-1,0,1,-1,-1,3,-2,0]`，第 1 个子数组也为 `[1,-1,0,1,-1,-1,3,-2,0]`。这两个子数组互不相交，因为它们没有共享任何 `nums[k]` 元素。

#### 示例 2  
**输入**  
```json
groups = [[10,-2],[1,2,3,4]], 
nums = [1,2,3,4,10,-2]
```  
**输出**  
```
false
```  
**解释**  
选择子数组 `[1,2,3,4,10,-2]` 两次是错误的，因为它们在 `nums` 中的出现顺序与 `groups` 不一致。子数组 `[10,-2]` 必须出现在 `[1,2,3,4]` 之前。

#### 示例 3  
**输入**  
```json
groups = [[1,2,3],[3,4]], 
nums = [7,7,1,2,3,4,7,7]
```  
**输出**  
```
false
```  
**解释**  
选择子数组 `[7,7,1,2,3,4,7,7]` 两次是无效的，因为它们不是互不相交的——它们共享了下标为 `4`（0 起）的元素 `nums[4]`。

### 约束条件
- `groups.length == n`
- `1 <= n <= 10^3`
- `1 <= groups[i].length,  sum(groups[i].length) <= 10^3`
- `1 <= nums.length <= 10^3`
- `-10^7 <= groups[i][j], nums[k] <= 10^7`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把题目当成「在 `nums` 里找子数组」的 **全排列**：  
- 对于第 `0` 个子数组 `groups[0]`，我们可以把 `nums` 中所有可能的起始位置都尝试一次（只要对应的切片和 `groups[0]` 完全相等）。  
- 选定了一个起始位置以后，**记住** 这个子数组占用了哪些下标。  
- 接下来对 `groups[1]` 重复同样的过程，但要保证它的下标 **不能和已经占用的下标重叠**，并且它必须出现在 `groups[0]` 之后（下标更大的位置）。  
- 用递归（或显式的栈）把每一种可能的选取路径走到底：如果所有 `groups` 都找到了合法的子数组，就返回 `True`；遍历完所有可能仍未成功，则返回 `False`。

> **数据结构类比**：  
> - `nums` 就像一本长长的“文字稿”。  
> - `groups[i]` 是我们想要在稿子里找的“短句”。  
> - “把子数组占用的下标记下来”类似于在稿子上用彩笔划线，后面的短句不能再跨过已经划好的线。

这个思路一定能得到正确答案，因为它枚举了 **所有** 合法的子数组组合，只要有一种满足题目要求，就一定会被遍历到。

#### 代码（Python）

```python
def canChoose_bruteforce(groups, nums):
    n = len(groups)

    # 判断 groups[idx] 能否在 nums[pos:] 找到一个不与已占用区间冲突的子数组
    def dfs(idx, pos):
        # 所有组都匹配成功
        if idx == n:
            return True
        g = groups[idx]
        m = len(g)

        # 在 nums[pos:] 的每一个可能起点尝试匹配
        for start in range(pos, len(nums) - m + 1):
            # 检查子数组是否相等
            if nums[start:start + m] == g:
                # 若匹配成功，递归检查下一个组，起点必须在本子数组之后
                if dfs(idx + 1, start + m):
                    return True
        # 没有任何起点可以让后面的组成功匹配
        return False

    return dfs(0, 0)
```

> 关键行解释（中文注释已写在代码里）  
> - `for start in range(pos, len(nums) - m + 1)`: 从当前可用位置 `pos` 开始枚举所有可能的起点。  
> - `if nums[start:start + m] == g`: 直接用 Python 切片比较子数组是否相同。  
> - `dfs(idx + 1, start + m)`: 递归进入下一个组，**下一个组只能从本子数组的末尾之后继续寻找**，保证不重叠且顺序正确。

#### 复杂度  

- **时间复杂度**：最坏情况是每个 `group` 都可以在 `nums` 的每个位置匹配（即每次都要遍历 `O(|nums|)`），递归深度为 `n`。  
  这相当于 `O(|nums|^n)`，在本题约束（`n ≤ 1000`、`|nums| ≤ 1000`）下显然不可接受。  
  用大白话说，就是「每一步都要把所有剩余的可能都试一遍」，会导致指数级的时间。
- **空间复杂度**：递归栈深度为 `n`，最多 `O(n)`（在最坏情况下 `n = 1000`），额外存储几乎为常数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在“对每个 group 都要在剩余的 `nums` 中遍历所有起点”。  
其实我们不需要遍历所有起点，只要找到 **最左侧的**（最早出现的）匹配子数组即可，因为：

- 题目要求子数组之间必须保持顺序且不相交。  
- 若我们把第 `i` 个 group 放在更靠右的位置，只会 **压缩** 后面 group 可用的空间，绝不会带来好处。  
- 因此「**贪心**」——每次都把当前 group 放在能出现的最早位置——是最优的。

实现上，只需要一个指针 `i` 指向 `nums` 当前可搜索的起始位置，遍历 `groups`：

1. 对于当前的 `group = groups[g_idx]`，在 `nums[i:]` 中寻找第一次出现的完整子数组。  
2. 若找不到（即遍历到 `nums` 末尾仍未匹配），直接返回 `False`。  
3. 若找到了，令 `i = match_start + len(group)`，即把指针移动到本子数组的 **右侧紧邻位置**，准备匹配下一个 group。  

在寻找子数组的过程中，我们可以直接用 Python 的切片比较（`nums[pos:pos+len(group)] == group`），这相当于 **双指针**：外层指针遍历可能的起点，内层指针一次性比较整个子数组。

> **数据结构类比**：  
> - 把 `nums` 想象成一条长河，指针 `i` 是一只小船。  
> - 每次要把一段 “木板” (`group`) 放在河面上，贪心策略是把木板放在船能到达的最前面的位置，这样后面的船还能有最长的河段可以继续放木板。

#### 代码（Python）

```python
def canChoose(groups, nums):
    """
    贪心 + 双指针：每个 group 都尽可能往左放
    """
    i = 0                     # 当前在 nums 中可搜索的起始位置
    n = len(nums)

    for g in groups:
        m = len(g)            # 当前 group 的长度
        found = False

        # 在 nums[i:] 中寻找第一次完整匹配
        while i + m <= n:     # 确保子数组不会越界
            # 若从 i 开始的子数组正好等于 g
            if nums[i:i + m] == g:
                found = True
                i += m        # 把指针移动到本子数组的右侧
                break
            i += 1            # 否则把起点右移一位继续尝试

        if not found:         # 当前 group 没有任何合法匹配
            return False

    return True               # 所有 groups 都匹配成功
```

> 关键行解释  
> - `while i + m <= n:`：保证切片 `nums[i:i+m]` 不会超出 `nums` 的范围。  
> - `if nums[i:i + m] == g:`：一次性比较完整子数组，等价于内部的 `m` 次比较。  
> - `i += m`：匹配成功后，把指针直接跳到子数组右侧，确保后面的 group 与之 **不相交**。  

#### 复杂度  

- **时间复杂度**：每个元素在 `nums` 最多被检查一次（指针只向右移动），每次匹配时最多比较 `len(g)` 次元素。整体上是 `O(|nums| + Σ|groups[i]|)`，在约束下最多约 `O(2000)`，几乎瞬间完成。  
  用大白话说，就是「我们只走了一遍河，没有来回跑」。
- **空间复杂度**：只用了常数个额外变量 `i、found、m`，即 `O(1)`。

---

## 心得

- **核心技巧**：**贪心** + **双指针**（一次线性扫描）。  
- 这种「尽可能左放」的思路在很多「子序列/子数组顺序匹配」的题目中都适用，例如  
  1. **`Check If a String Contains All Binary Codes of Size K`**（子串覆盖）  
  2. **`Is Subsequence`**（判断子序列）  
  3. **`Find Substring with Concatenation of All Words`**（连续子串匹配）  
- 一句话总结解题钥匙：**「每一步都把当前需求放在最左边」**，这样后面的空间最大，永远不会因为“走得太远”而卡死。

---

## 反思

- **第一反应**：看到「不相交且顺序」就想到「递归暴力」——把所有可能都枚举。  
- **最容易踩的坑**：  
  - 忘记检查子数组是否会越界（`i + len(group) <= len(nums)`）。  
  - 把指针移动错位，只加了 `1` 而不是整段长度，导致后面的子数组出现重叠。  
  - 对负数或极大数值的比较没有特殊处理，其实切片比较本身已经能处理。  
- **下次类似题的第一步**：先问自己「是否可以一次线性扫描把每个需求放在最左侧？」如果答案是「可以」，就立刻尝试贪心 + 双指针；如果不行，再考虑更复杂的 DP 或回溯。