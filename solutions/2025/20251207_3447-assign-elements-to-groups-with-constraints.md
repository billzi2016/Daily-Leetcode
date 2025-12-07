# #3447. 在约束条件下分配元素到组 / Assign Elements to Groups with Constraints

> 难度：中等 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/assign-elements-to-groups-with-constraints/)

---

## 题目（英文原版）

**Description**

You are given an integer array groups, where groups[i] represents the size of the ith group. You are also given an integer array elements.
Your task is to assign one element to each group based on the following rules:
Return an integer array assigned, where assigned[i] is the index of the element chosen for group i, or -1 if no suitable element exists.
Note: An element may be assigned to more than one group.

**Examples**

**Example 1:**

```
Input: groups = [8,4,3,2,4], elements = [4,2]
Output: [0,0,-1,1,0]
Explanation:
```

**Example 2:**

```
Input: groups = [2,3,5,7], elements = [5,3,3]
Output: [-1,1,0,-1]
Explanation:
```

**Example 3:**

```
Input: groups = [10,21,30,41], elements = [2,1]
Output: [0,1,0,1]
Explanation:
elements[0] = 2 is assigned to the groups with even values, and elements[1] = 1 is assigned to the groups with odd values.
```

**Constraints**

- 1 <= groups.length <= 105
- 1 <= elements.length <= 105
- 1 <= groups[i] <= 105
- 1 <= elements[i] <= 105

---

## 题目（中文翻译）

给定一个整数数组 **groups**，其中 `groups[i]` 表示第 *i* 个组的大小。再给定一个整数数组 **elements**。  
请按照以下规则为每个组分配一个元素：

- 选中的元素的值必须能够整除该组的大小，即 `elements[j]` 能整除 `groups[i]`。
- 同一个元素可以被分配给多个组。

返回一个整数数组 **assigned**，其中 `assigned[i]` 为分配给第 *i* 个组的元素在 **elements** 中的下标，如果不存在满足条件的元素则记为 `-1`。

> **注意**：元素可以被重复使用。

### 示例

#### 示例 1
```text
Input: groups = [8,4,3,2,4], elements = [4,2]
Output: [0,0,-1,1,0]
Explanation: 
- 8 能被 4 整除，选取 elements[0]。
- 4 能被 4 整除，选取 elements[0]。
- 3 不能被任何元素整除，记为 -1。
- 2 能被 2 整除，选取 elements[1]。
- 4 再次能被 4 整除，选取 elements[0]。
```

#### 示例 2
```text
Input: groups = [2,3,5,7], elements = [5,3,3]
Output: [-1,1,0,-1]
Explanation: 
- 2 不能被任何元素整除，记为 -1。
- 3 能被 3 整除，选取 elements[1]（或 elements[2]，任选其一，这里取下标 1）。
- 5 能被 5 整除，选取 elements[0]。
- 7 不能被任何元素整除，记为 -1。
```

#### 示例 3
```text
Input: groups = [10,21,30,41], elements = [2,1]
Output: [0,1,0,1]
Explanation: 
elements[0] = 2 被分配给所有偶数大小的组，elements[1] = 1 被分配给所有奇数大小的组。
```

### 约束条件
- `1 <= groups.length <= 10^5`
- `1 <= elements.length <= 10^5`
- `1 <= groups[i] <= 10^5`
- `1 <= elements[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐个检查**：  
- 对于每一个 `group[i]`，遍历所有 `elements[j]`，看 `elements[j]` 是否能整除 `group[i]`（`group[i] % elements[j] == 0`）。  
- 能整除的就把 `j` 记下来，取下标最小的那个；如果全部都不整除，就记 `-1`。

这里用到的唯一数据结构是 **两个普通的列表**（`groups` 与 `elements`），相当于我们在“找字典里对应的词”。  
- `group[i]` 就是要查的“词”，  
- `elements[j]` 就是字典里每一条“词‑页码”。  
我们把每条 `elements` 都拿去“比对”，找到能够“解释” `group[i]` 的最小页码（下标）。

**为什么对**：只要遍历了所有的 `elements`，必然能找到所有能够整除的情况，取最小下标自然就是答案。

**时间/空间复杂度**（大白话）  
- 外层遍历 `groups`，长度记作 `n`（最多 10⁵），  
- 内层遍历 `elements`，长度记作 `m`（最多 10⁵）。  
所以总共要做 `n × m` 次除法运算。  
如果把 `n`、`m` 都想成 10 万，那么运算次数大约是 **10⁵ × 10⁵ = 10¹⁰**，这在一秒内根本做不完。  
- 空间上只用了原数组和一个答案数组，都是 **O(n)**，几乎不占内存。

#### 代码（Python）

```python
def assign_elements_bruteforce(groups, elements):
    n = len(groups)
    ans = [-1] * n                     # 初始全部为 -1
    for i, g in enumerate(groups):     # 对每个 group
        best = -1                       # 记录当前找到的最小下标
        for j, e in enumerate(elements):   # 遍历所有 elements
            if g % e == 0:                 # 能整除才算合法
                best = j                  # 因为 j 按顺序递增，直接记下当前 j 就是最小的
                break                    # 找到最小下标后可以直接退出内层循环
        ans[i] = best
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n·m)`（比如 10⁵ × 10⁵ = 10¹⁰），即“每个 group 都要检查所有 elements”。  
- **空间复杂度**：`O(n)`，只用了一个和 `groups` 同长的答案数组。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次都要遍历全部 `elements`，这相当于在 “字典里找词” 时把每一页都翻一遍。  
如果我们能够 **预先把同一个值的 groups 放在一起**，并且 **一次性把所有能整除的 groups 填好答案**，就可以省掉大量重复检查。

**关键观察**  

- `elements[j]` 能整除的 `group` 必须是它的 **倍数**（比如 `2` 能整除 `2,4,6,8,…`）。  
- 因此我们可以把 **“遍历所有 elements”** 与 **“遍历它们的倍数”** 合并在一起——这正是 **筛法（sieve）** 常用的技巧。

**步骤拆解**  

1. **把所有 groups 按值分组**  
   用一个哈希表 `value → [group_idx1, group_idx2, …]` 保存每个数值出现的下标列表。  
   类比：把所有相同“词”放进同一本小册子，等会儿一次性找整除的词时只需要看对应的小册子。

2. **准备答案数组**，默认 `-1`，表示还没有找到合适的 element。

3. **按照元素的下标顺序遍历** `elements`  
   - 对当前元素 `v = elements[idx]`，从 `v` 开始，以步长 `v` 依次枚举 `v, 2v, 3v, …`，一直到 `max_group`（所有 groups 中的最大值）。  
   - 每枚举到一个数 `multiple`，检查哈希表中是否有 `multiple` 这个键（即是否有 group 的值等于它）。  
   - 若有，则把这些 group 的答案全部设为当前的 `idx`（因为我们是按下标从小到大遍历的，第一次赋值必然是最小下标）。随后 **把这个键删掉**，避免以后重复检查。  

   这样，每个 `group` 只会被赋值一次，且只会在它对应的最小可整除 `element` 处理时被访问。

**为什么快**  

- 对每个 `element`，我们遍历的次数是 `max_group / element_value`。  
- 所有 `element` 的遍历次数之和大约是  

  \[
  \sum_{v\in elements} \frac{max\_group}{v}
  \le max\_group \cdot \left(1 + \frac12 + \frac13 + \dots + \frac1{max\_group}\right)
  = O(max\_group \log max\_group)
  \]

  对 `max_group ≤ 10⁵` 来说，这大约是 **几百万次**，远远小于 `10¹⁰`。

- 每个 `group` 只被访问一次（因为一旦赋值就会从哈希表中删掉），所以总的时间基本就是上面的筛式遍历。

**核心算法/数据结构**  

- **哈希表（字典）**：把相同数值的 group 下标聚在一起。  
- **筛法（Sieve）**：像埃拉托斯特尼筛质数那样，用步长为 `v` 的循环遍历所有 `v` 的倍数。  
- **一次遍历**：因为 `elements` 按下标递增遍历，第一次赋值天然满足“最小下标”。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def assign_elements(groups: List[int], elements: List[int]) -> List[int]:
    """
    对每个 group[i]，返回最小下标的 element 能整除它，若不存在返回 -1。
    时间复杂度 O(max(groups) * log max(groups) + len(groups) + len(elements))
    空间复杂度 O(len(groups) + max(groups))
    """
    n = len(groups)
    ans = [-1] * n                     # 初始化答案

    # 1️⃣ 把所有 group 按值收集下标
    value_to_idxs = defaultdict(list)  # value → [group idx ...]
    max_g = 0
    for i, g in enumerate(groups):
        value_to_idxs[g].append(i)
        if g > max_g:
            max_g = g

    # 2️⃣ 按元素下标顺序遍历
    for elem_idx, val in enumerate(elements):
        # 如果 val 已经大于最大 group，后面的倍数必然都不在 groups 中，直接跳过
        if val > max_g:
            continue

        # 3️⃣ 枚举 val 的所有倍数
        multiple = val
        while multiple <= max_g:
            # 检查是否有 group 的值恰好等于这个倍数
            if multiple in value_to_idxs:
                # 把这些 group 全部指向当前的 elem_idx
                for grp_idx in value_to_idxs[multiple]:
                    if ans[grp_idx] == -1:          # 只赋值一次
                        ans[grp_idx] = elem_idx
                # 赋完后删掉，防止以后再次访问（因为后面的 element 下标更大，已经不是最小）
                del value_to_idxs[multiple]
            multiple += val                     # 下一倍数

        # 如果哈希表已经空了，说明所有 group 都已经找到答案，提早结束
        if not value_to_idxs:
            break

    return ans
```

**代码要点解释（中文注释）**

- `value_to_idxs` 把相同数值的 groups 聚在一起，类似“把同一本词典的所有词页码放在一起”。  
- `while multiple <= max_g:` 这段循环就是 **筛法**：从 `val` 开始，每次跳 `val`，遍历所有 `val` 的倍数。  
- `if multiple in value_to_idxs:` 判断当前倍数是否恰好是某些 group 的值。  
- `del value_to_idxs[multiple]` 删除已处理的键，确保每个 group 只被赋值一次，也让后面的循环更快。  

#### 复杂度

- **时间复杂度**：`O(max_group * log max_group + n + m)`  
  - `max_group ≤ 10⁵`，`log max_group ≈ 12`，所以主导项大约是几百万次，远小于暴力的 `10¹⁰`。  
  - 与暴力解相比，“每个 group 只检查一次”而不是“每个 group 检查所有 elements”。  

- **空间复杂度**：`O(n + max_group)`  
  - `ans` 用 `O(n)`，哈希表最坏情况下会存 `max_group` 条键（每个可能的数值都有），合计仍在可接受范围。

---

## 心得

- **核心技巧**：**把“能整除”转化为“是某个数的倍数”，再用筛法一次性遍历所有倍数**。  
- **适用的题型**（类似思路）  
  1. “给定数组 A，找每个数的最小因子/最小能整除它的数”。  
  2. “把若干区间标记为可用，要求对每个点找到最早出现的覆盖区间”。  
  3. “把一组数字映射到它们的约数集合，寻找最小满足条件的映射”。  
- **一句话总结解题钥匙**：*把每个元素的可行目标视作它的倍数，用一次筛遍历把所有目标一次性填好*。

---

## 反思

- **第一反应**：直接双层循环检查所有 `elements`，即暴力枚举。  
- **最容易踩的坑**  
  - 忘记 **删除已处理的 group 值**，导致后面的元素又去检查已经有答案的 group，时间会回到 `O(n·m)`。  
  - 没有提前 **记录 `max_group`**，导致循环上界写错，可能出现无限循环或遗漏大数。  
  - 对 **元素值大于所有 group** 的情况没有提前跳过，会无意义地执行大量空循环。  
- **下次类似题的第一步**：先把 “满足条件的目标” 用 **数值映射（哈希表）** 收集，然后思考 **是否可以把条件转化为“倍数/约数”**，从而使用 **筛法** 或 **前缀/后缀** 之类的一次遍历完成。