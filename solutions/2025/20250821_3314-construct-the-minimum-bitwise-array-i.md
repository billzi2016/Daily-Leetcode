# #3314. 构造最小按位或数组 I / Construct the Minimum Bitwise Array I

> 难度：简单 · 标签：Array、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/construct-the-minimum-bitwise-array-i/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of n prime integers.
You need to construct an array ans of length n, such that, for each index i, the bitwise OR of ans[i] and ans[i] + 1 is equal to nums[i], i.e. ans[i] OR (ans[i] + 1) == nums[i].
Additionally, you must minimize each value of ans[i] in the resulting array.
If it is not possible to find such a value for ans[i] that satisfies the condition, then set ans[i] = -1.

**Examples**

**Example 1:**

```
Input: nums = [2,3,5,7]
Output: [-1,1,4,3]
Explanation:
```

**Example 2:**

```
Input: nums = [11,13,31]
Output: [9,12,15]
Explanation:
```

**Constraints**

- 1 <= nums.length <= 100
- 2 <= nums[i] <= 1000
- nums[i] is a prime number.

---

## 题目（中文翻译）

给定一个长度为 `n` 的数组 `nums`，其中所有元素都是质数（prime integer）。

需要构造一个长度为 `n` 的数组 `ans`，使得对每个下标 `i`，`ans[i]` 与 `ans[i] + 1` 的按位或（bitwise OR）等于 `nums[i]`，即  

`ans[i] | (ans[i] + 1) == nums[i]`。

同时，需要使得到的每个 `ans[i]` 尽可能小（最小化）。

如果不存在满足条件的 `ans[i]`，则将 `ans[i] = -1`。

---

### 示例

#### 示例 1
**Input:** `nums = [2,3,5,7]`  
**Output:** `[-1,1,4,3]`  
**Explanation:**  

（此处略）

#### 示例 2
**Input:** `nums = [11,13,31]`  
**Output:** `[9,12,15]`  
**Explanation:**  

（此处略）

---

### 约束条件
- `1 <= nums.length <= 100`
- `2 <= nums[i] <= 1000`
- `nums[i]` 为质数（prime）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法是**把每个 `ans[i]` 当成一个待猜的数字**，从 `0` 开始逐个尝试，检查

```
ans[i] | (ans[i] + 1) == nums[i]
```

是否成立。  
如果成立，就把这个 `ans[i]` 记下来；因为我们是从小到大枚举的，第一次遇到的就是 **最小** 的答案。  

> **数据结构**：只需要一个普通的整数变量 `candidate`，相当于在“字典”里一次查找一个键值对——这里没有真正的哈希表，只是顺序遍历。

> **为什么一定对**：  
> - `ans[i]` 的取值范围是非负整数。  
> - 当我们把所有可能的取值（从 `0` 到 `nums[i]`，甚至更大）都检查一遍时，必然能找到满足等式的最小值，或者遍历完仍未找到，此时返回 `-1`。

> **复杂度大白话**：  
> - `O(n·m)`，其中 `n` 是数组长度（最多 100），`m` 是我们尝试的最大数字（`nums[i] ≤ 1000`），意思是**最多 100 × 1000 = 10⁵ 次基本操作**，在电脑眼里几乎是瞬间完成的。  
> - 空间 `O(1)`，只用几个临时变量，几乎不占内存。

#### 代码（Python）

```python
def construct_minimum_bitwise_array(nums):
    ans = []
    for num in nums:                     # 逐个处理每个 prime
        found = -1                        # 默认找不到
        # 只需要尝试到 num 本身即可，答案一定不会大于它
        for cand in range(num + 1):       
            # cand | (cand + 1) 与 num 是否相等
            if (cand | (cand + 1)) == num:
                found = cand              # 第一次遇到就是最小值
                break                     # 结束当前循环
        ans.append(found)                # 把结果放进答案数组
    return ans
```

**关键行中文注释**  
- `for cand in range(num + 1):` 遍历所有可能的 `ans[i]`（从 0 到 `num`）。  
- `if (cand | (cand + 1)) == num:` 检查位运算等式是否成立。  
- `found = cand` 找到最小的合法值后立刻保存并退出循环。

#### 复杂度

- **时间复杂度**：`O(n·m)` → 对每个元素最多检查 `num+1 ≤ 1001` 次，整体不超过 `10⁵` 步，实际运行极快。  
- **空间复杂度**：`O(1)` → 只用了常数个临时变量（`found`、`cand`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的“慢”在于**逐个枚举**。观察等式

```
ans | (ans + 1) = num
```

我们可以从二进制的角度推导出一个 **一次就能算出答案** 的公式。

1. **把 `ans` 与 `ans+1` 的二进制关系写出来**  
   - `ans` 与 `ans+1` 是相邻的整数。  
   - 在 `ans` 的最低位（从右往左）出现的第一个 `0` 位置记为 `k`。  
   - `ans` 在 `k` 以下的位全是 `1`（因为如果有 `0`，`k` 就不是最低的 `0`）。  
   - `ans+1` 会把这 `k` 以下的 `1` 全部变成 `0`，并把第 `k` 位的 `0` 变成 `1`。

   于是 `ans | (ans+1)` 的结果是：**把 `ans` 的第 `k` 位以及以下所有位都变成 `1`**，更高位保持不变。

2. **从 `num` 逆向求 `k`**  
   - `num` 必须在最低几位全部是 `1`，因为这些 `1` 正是由上面那一步产生的。  
   - 记 **从最低位开始连续的 `1` 的个数** 为 `t`（即 `num` 的 *trailing‑ones*）。  
   - 那么 `k = t`（第一个 `0` 正好在第 `t` 位）。

3. **构造最小的 `ans`**  
   - `ans` 在第 `t` 位必须是 `0`，低于它的位全部是 `0`（要让 `ans` 尽可能小）。  
   - 高于第 `t` 位的部分保持和 `num` 一致。  
   - 于是  

     ```
     ans = (num >> (t + 1)) << (t + 1)
     ```

     这一步的意义是：**把 `num` 右移 `t+1` 位抹掉低 `t+1` 位，再左移回来**，相当于把低 `t+1` 位全部清零。

4. **特殊情况**  
   - 如果 `num` 的最低位就是 `0`（即 `t = 0`），则不存在满足条件的 `ans`，返回 `-1`。  
   - 当 `num` 全部是 `1`（比如 `3 = 0b11`、`7 = 0b111`），`t` 等于它的二进制位数。此时上面的公式会得到 `0`，但真正的最小答案是 `num >> 1`（把最高的 `1` 留给 `ans+1`，其余全部变成 `1`），这正好等价于 **把低 `t-1` 位全设为 `1`**。

   综合起来的实现如下：

   ```python
   def min_ans(num: int) -> int:
       # 1. 检查最低位是否为 1
       if num & 1 == 0:          # num 的最低位是 0
           return -1

       # 2. 计算连续的 1 的个数（trailing ones）
       t = 0
       while (num >> t) & 1:     # 只要第 t 位是 1，就继续
           t += 1

       # 3. 判断是否是全 1 的数（Mersenne 质数）
       if (num >> t) == 0:       # 高位已经全被移走，说明 num 全是 1
           return num >> 1       # 例如 3 -> 1, 7 -> 3, 31 -> 15

       # 4. 普通情况：清掉低 t+1 位
       return (num >> (t + 1)) << (t + 1)
   ```

5. **整体算法**  
   对每个 `num` 调用上面的 `min_ans`，时间就是 `O(1)`（只循环几次最多 10 位），整体 `O(n)`。

#### 代码（Python）

```python
def construct_minimum_bitwise_array(nums):
    """返回满足 ans[i] | (ans[i] + 1) == nums[i] 的最小 ans 数组"""
    def min_ans(num: int) -> int:
        # 若最低位为 0，根本不可能得到 num
        if (num & 1) == 0:
            return -1

        # 统计从最低位开始连续的 1 的个数 t
        t = 0
        while (num >> t) & 1:          # 只要第 t 位是 1，就继续
            t += 1

        # 如果 num 全部都是 1（例如 3、7、31），高位已经全部被右移走
        if (num >> t) == 0:            # 说明 num = 2^t - 1
            return num >> 1            # 例如 7 -> 3, 31 -> 15

        # 普通情况：把低 t+1 位清零，得到最小的 ans
        return (num >> (t + 1)) << (t + 1)

    return [min_ans(x) for x in nums]
```

**关键行中文注释**  
- `if (num & 1) == 0:` 检查最低位是否为 `0`，若是直接返回 `-1`。  
- `while (num >> t) & 1:` 循环统计从右往左连续的 `1` 有多少个，记为 `t`。  
- `if (num >> t) == 0:` 判断 `num` 是否全是 `1`（即右移 `t` 位后全变成 `0`）。  
- `(num >> (t + 1)) << (t + 1)` 把低 `t+1` 位全部置零，得到最小合法的 `ans`。

#### 复杂度

- **时间复杂度**：`O(n)` → 每个 `num` 只循环几次（至多遍历到它的最高位，`num ≤ 1000`，二进制最多 10 位），整体线性。相比暴力的 `O(n·m)`，**快了好几个数量级**。  
- **空间复杂度**：`O(1)` → 只用常数个临时变量。

---

## 心得

- **核心技巧**：利用相邻整数的位运算特性，**把 “最低的 0 位” 与 “连续的 1”** 这两个概念转化为二进制的数学描述，从而在 O(1) 时间内直接算出答案。  
- **适用的题型**  
  1. “给定 `x`，求最小的 `y` 使得 `y | (y+1) = x`”。  
  2. “把一个数拆成两数的位或” 相关的构造题（如 “Construct the Minimum Bitwise Array II”）。  
  3. “找出满足某种位运算关系的最小/最大整数”——常用的技巧是**分析最低位的变化**。  
- **一句话总结解题钥匙**：**“把问题转化为‘最低的 0 位在哪里’，再把低位全部清零”。**

---

## 反思

- **第一反应**：看到 “`ans[i] OR (ans[i] + 1) == nums[i]`”，我先想到直接遍历所有可能的 `ans[i]`，因为约束很小。  
- **最容易踩的坑**  
  1. **忘记检查最低位**：如果 `nums[i]` 的最低位是 `0`，根本不存在合法 `ans[i]`，要直接返回 `-1`。  
  2. **全 1 的特殊情况**：`num = 2^k - 1`（全是 1）时，直接把低位全部清零会得到 `0`，但实际答案是 `num >> 1`。  
  3. **边界值**：`num = 2`（二进制 `10`）是唯一的不可构造例子，需要返回 `-1`。  
- **下次类似题的第一步**：**先在二进制层面写出“相邻数的位关系”，找出最低的 0 位或连续的 1，利用位移一次性得到答案**。这样往往能把 O(枚举) 的思路提升到 O(位运算) 的最优解。