# #1562. 寻找大小为 M 的最新连续 1 组 / Find Latest Group of Size M

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-latest-group-of-size-m/)

---

## 题目（英文原版）

**Description**

Given an array arr that represents a permutation of numbers from 1 to n.
You have a binary string of size n that initially has all its bits set to zero. At each step i (assuming both the binary string and arr are 1-indexed) from 1 to n, the bit at position arr[i] is set to 1.
You are also given an integer m. Find the latest step at which there exists a group of ones of length m. A group of ones is a contiguous substring of 1's such that it cannot be extended in either direction.
Return the latest step at which there exists a group of ones of length exactly m. If no such group exists, return -1.

**Examples**

**Example 1:**

```
Input: arr = [3,5,1,2,4], m = 1
Output: 4
Explanation: 
Step 1: "00100", groups: ["1"]
Step 2: "00101", groups: ["1", "1"]
Step 3: "10101", groups: ["1", "1", "1"]
Step 4: "11101", groups: ["111", "1"]
Step 5: "11111", groups: ["11111"]
The latest step at which there exists a group of size 1 is step 4.
```

**Example 2:**

```
Input: arr = [3,1,5,4,2], m = 2
Output: -1
Explanation: 
Step 1: "00100", groups: ["1"]
Step 2: "10100", groups: ["1", "1"]
Step 3: "10101", groups: ["1", "1", "1"]
Step 4: "10111", groups: ["1", "111"]
Step 5: "11111", groups: ["11111"]
No group of size 2 exists during any step.
```

**Constraints**

- n == arr.length
- 1 <= m <= n <= 105
- 1 <= arr[i] <= n
- All integers in arr are distinct.

---

## 题目（中文翻译）

给定一个数组 `arr`，它是数字 `1` 到 `n` 的一个排列（permutation）。  
同时有一个长度为 `n` 的二进制字符串（binary string），最初所有位均为 `0`。  
在每一步 `i`（假设二进制字符串和 `arr` 都是 **1** 索引）从 `1` 到 `n`，将位置 `arr[i]` 的位设为 `1`。  

另给定一个整数 `m`。请找出 **最近** 的一步，使得此时存在恰好长度为 `m` 的 **连续 1 组**（group of ones）。  
连续 1 组是指一段只能由 `1` 组成的子串，且在左右两端都无法再向外延伸（即两端要么是 `0` 要么是字符串边界）。  

返回存在恰好长度为 `m` 的连续 1 组的**最新**一步的编号。如果整个过程中不存在这样的组，返回 `-1`。

## 示例

### 示例 1  
**输入**: `arr = [3,5,1,2,4]`, `m = 1`  
**输出**: `4`  
**解释**:  
- 步骤 1: `"00100"`，组: `["1"]`  
- 步骤 2: `"00101"`，组: `["1", "1"]`  
- 步骤 3: `"10101"`，组: `["1", "1", "1"]`  
- 步骤 4: `"11101"`，组: `["111", "1"]`  
- 步骤 5: `"11111"`，组: `["11111"]`  

存在长度为 `1` 的组的最新一步是第 `4` 步。

### 示例 2  
**输入**: `arr = [3,1,5,4,2]`, `m = 2`  
**输出**: `-1`  
**解释**:  
- 步骤 1: `"00100"`，组: `["1"]`  
- 步骤 2: `"10100"`，组: `["1", "1"]`  
- 步骤 3: `"10101"`，组: `["1", "1", "1"]`  
- 步骤 4: `"10111"`，组: `["1", "111"]`  
- 步骤 5: `"11111"`，组: `["11111"]`  

整个过程均不存在长度为 `2` 的组，返回 `-1`。

## 约束条件
- `n == arr.length`
- `1 <= m <= n <= 10^5`
- `1 <= arr[i] <= n`
- `arr` 中的所有整数互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把题目描述的过程 **一步步模拟**：  

1. 先准备一个长度为 `n` 的全 `0` 列表（相当于二进制字符串）。  
2. 按 `arr` 的顺序把对应位置设为 `1`。  
3. 每次设完以后，整条数组从左到右扫一遍，统计所有连续的 `1` 段的长度。只要出现长度正好等于 `m` 的段，就把当前步数记下来，继续往后走。  

> **类比**：把 `0/1` 串想象成一排灯泡，`0` 表示关灯，`1` 表示开灯。我们每次打开一个灯，然后走一遍走廊，数数有多少盏灯是连续开的。  

这套做法**一定是对的**，因为我们没有漏掉任何一步，也没有遗漏任何可能出现的 `m` 长度的连续段。  

**为什么会慢**：  
- 第 `i` 步我们都要 **完整遍历一次** 长度为 `n` 的数组来找连续段。  
- 总共有 `n` 步，所以总时间是 `n` 次遍历 * `n` 长度 = `O(n²)`。  

> **大白话解释**：如果 `n = 10⁵`，`n²` 就是 `10¹⁰`，相当于十亿级的操作，电脑根本跑不完。  

#### 代码（Python）

```python
def findLatestStep_bruteforce(arr, m):
    n = len(arr)
    # 0 表示关灯，1 表示开灯
    bits = [0] * n          # 初始全 0
    answer = -1

    for step, pos in enumerate(arr, 1):   # step 从 1 开始计数
        bits[pos - 1] = 1                 # 把第 pos 位开灯（下标要 -1）

        # ---- 扫描一遍，统计所有连续 1 的长度 ----
        cur_len = 0
        found_m = False
        for b in bits:
            if b == 1:
                cur_len += 1
            else:
                # 碰到 0，说明前面的连续段结束
                if cur_len == m:
                    found_m = True
                cur_len = 0
        # 最后一个段可能没有被 0 “终结”
        if cur_len == m:
            found_m = True

        if found_m:
            answer = step                 # 记录最新的满足步数

    return answer
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 每一步都要遍历长度为 `n` 的数组，一共 `n` 步。  
  - 用大白话说，就是“走十万步，每一步都要把全场跑一遍”。  

- **空间复杂度**：`O(n)`  
  - 需要一个长度为 `n` 的 `bits` 数组来保存当前的灯光状态。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每一步都全局扫描**。  
我们需要一种方式，在**只看局部**（即刚刚被翻开的那一位）的时候，就能知道新的连续段长度以及旧的段是怎么变化的。  

思路分三步：

1. **用两个辅助数组记录左右端点的段长**  
   - `left[i]`：以位置 `i` 为**左端点**的连续 `1` 段的长度（如果 `bits[i]==0`，值为 `0`）。  
   - `right[i]`：以位置 `i` 为**右端点**的连续 `1` 段的长度。  
   这两个数组相当于“每段的身份证”，帮助我们在 O(1) 时间合并或拆分段。

2. **维护一个哈希表 `cnt`，记录当前每种长度出现了多少段**  
   - 例如 `cnt[3]=2` 表示现在有两段长度恰好为 `3` 的连续 `1`。  
   - 只要 `cnt[m] > 0`，说明在当前步骤已经出现了满足要求的段。

3. **每次翻开第 `pos` 位**  
   - 查看左边的段长 `l = left[pos-1]`（如果左边是 `0` 则为 `0`），右边的段长 `r = right[pos+1]`。  
   - 新形成的段长度 `new_len = l + 1 + r`。  
   - 把原来左段、右段的计数在 `cnt` 中减 1（因为它们被合并了），再把新段计数加 1。  
   - 同时更新 `left`、`right`：  
     - 新段的左端点是 `pos - l`，右端点是 `pos + r`。  
     - `left[pos - l] = new_len`，`right[pos + r] = new_len`。  

   这样每一步只做常数次的数组访问和哈希表更新，**时间是 O(1)**。

4. **记录答案**  
   - 在遍历 `arr` 的过程中，如果 `cnt[m] > 0`，把当前步数 `i` 记为答案。  
   - 因为我们是顺序从第一步往后走的，最后一次更新的步数自然是**最新的**。

> **类比**：  
> 把每段连续的 `1` 看成一条绳子，`left`/`right` 记录绳子两头的长度。  
> 当我们在中间点插入一个新结点时，左边的绳子和右边的绳子会合并成一条更长的绳子，只需要更新两头的长度即可。

#### 代码（Python）

```python
def findLatestStep(arr, m):
    n = len(arr)
    if m == n:               # 特判：只有全 1 时才满足
        return n

    # left[i] : 以 i 为左端点的段长度，right[i] : 以 i 为右端点的段长度
    left = [0] * (n + 2)     # 多开两个哨兵，防止越界
    right = [0] * (n + 2)

    cnt = {}                 # 哈希表，cnt[length] = 该长度的段数
    ans = -1

    for step, pos in enumerate(arr, 1):
        l = left[pos - 1]    # 左边段的长度（若左边是 0，则为 0）
        r = right[pos + 1]   # 右边段的长度
        new_len = l + 1 + r   # 合并后新段的长度

        # ---------- 更新 cnt ----------
        # 把左段、右段的计数减 1（如果它们存在的话）
        if l:
            cnt[l] = cnt.get(l, 0) - 1
        if r:
            cnt[r] = cnt.get(r, 0) - 1
        # 新段计数加 1
        cnt[new_len] = cnt.get(new_len, 0) + 1

        # ---------- 更新 left / right ----------
        # 新段的左端点坐标
        left_boundary = pos - l
        # 新段的右端点坐标
        right_boundary = pos + r
        left[left_boundary] = new_len
        right[right_boundary] = new_len

        # ---------- 检查是否出现长度为 m 的段 ----------
        if cnt.get(m, 0) > 0:
            ans = step          # 记录最新的满足步数

    return ans
```

> **代码说明（每行中文注释已在代码中）**  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次 `arr`，每一步做的操作都是常数时间（数组访问、哈希表增删）。  
  - 与暴力解的 `O(n²)` 相比，速度提升了 **n 倍**，在 `n = 10⁵` 时也能轻松跑完。  

- **空间复杂度**：`O(n)`  
  - 需要 `left`、`right` 两个长度为 `n+2` 的数组，以及哈希表 `cnt`（最多存 `n` 种不同长度）。  
  - 用大白话说，就是“我们只需要记住每段的两头和每种长度出现了多少次”，不需要再保存整条二进制串。  

---

## 心得  

- **核心技巧**：利用**左右端点长度数组**（或等价的并查集思想）实现**局部合并**，并用**哈希表记录长度出现次数**。  
- **适用的题型**  
  1. “最大/最小 连续子数组长度”类（如 LeetCode 1568：`Maximum Length of Subarray With Positive Product` 的类似思路）。  
  2. “动态维护区间大小”类（如 LeetCode 1695：`Maximum Erasure Value` 中的滑动窗口计数）。  
  3. “倒序模拟/逆向思维”类（如 LeetCode 1903：`Largest Odd Number in String` 的逆向构造）。  
- **一句话总结**：**把每段的两端当作身份证，合并时只改两端即可**——这样就能在 O(1) 时间内维护所有段的长度分布。

---

## 反思  

- **第一反应**：直接把过程写成模拟，然后每一步全遍历检查。  
- **最容易踩的坑**  
  - 忘记在合并时把 **左段和右段的计数先减掉**，导致 `cnt[m]` 统计错误。  
  - 边界条件：`pos` 在数组最左或最右时，`left[pos-1]` 或 `right[pos+1]` 可能越界，使用哨兵或提前判断可以避免。  
  - 特判 `m == n`：只有在所有位都变成 `1` 的那一步才可能满足。  
- **下次遇到同类题**：第一步先想 **“如何在局部更新”**，找出能够在 O(1) 时间合并/拆分的结构（左/右端点、并查集、单调栈等），再把全局检查转化为局部计数的维护。这样往往能把 `O(n²)` 降到 `O(n)`。