# #2659. 清空数组 / Make Array Empty

> 难度：困难 · 标签：Array、Binary Search、Greedy、Binary Indexed Tree、Segment Tree、Sorting、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/make-array-empty/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums containing distinct numbers, and you can perform the following operations until the array is empty:
Return an integer denoting the number of operations it takes to make nums empty.

**Examples**

**Example 1:**

```
Input: nums = [3,4,-1]
Output: 5
```

**Example 2:**

```
Input: nums = [1,2,4,3]
Output: 5
```

**Example 3:**

```
Input: nums = [1,2,3]
Output: 3
```

**Constraints**

- 1 <= nums.length <= 105
- -109 <= nums[i] <= 109
- All values in nums are distinct.

---

## 题目（中文翻译）

给定一个包含互不相同整数的数组 `nums`，你可以对其执行下列操作，直到数组为空为止。  
返回一个整数，表示将 `nums` 清空所需的操作次数。

**示例 1：**  
**示例 2：**  
**示例 3：**  
**约束条件：**  

---

### 示例

#### 示例 1
**输入:** `nums = [3,4,-1]`  
**输出:** `5`

#### 示例 2
**输入:** `nums = [1,2,4,3]`  
**输出:** `5`

#### 示例 3
**输入:** `nums = [1,2,3]`  
**输出:** `3`

### 约束条件
- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `nums` 中的所有值互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

把数组想象成一条环形的传送带，指针一开始站在下标 `0` 的位置。  
每一次操作我们都要 **找出当前剩余元素中最小的那个**，然后顺时针（向右）走到它所在的下标，走过的每一个位置都算一步，走到目标下标后再把它“取走”。  
取走后，数组的长度会减 1，指针停在被取走的位置的下一个元素上（如果已经是最后一个元素，则回到最左边的下标 `0`），继续找下一个最小值，直到数组为空。

**为什么能得到正确答案**  
- 题目要求的“操作次数”正好是：*指针移动的步数 + 取走元素本身算作的一步*。  
- 按照题目描述，我们每次只能取走当前最小的数，所以只要严格按照 **从小到大** 的顺序依次处理即可。  

**实现细节（暴力）**  
1. 复制一份原数组 `arr`，用 `sorted(arr)` 得到从小到大的取走顺序。  
2. 用一个普通的 Python `list` 保存当前还在的元素，下标随时会变化。  
3. 维护一个变量 `cur` 表示指针所在的下标（相对于当前 `list`）。  
4. 对每一个要取走的数 `val`：  
   - 在当前 `list` 中找到它的下标 `idx`（`list.index(val)`，时间是 O(n)）。  
   - 计算顺时针走到 `idx` 需要的步数：如果 `cur <= idx`，步数就是 `idx - cur`；否则需要先走到列表末尾再回到开头，步数是 `len(list) - cur + idx`。  
   - 再加上取走本身的一步，总步数累计到答案。  
   - 用 `list.pop(idx)` 把该元素删掉。  
   - 把指针 `cur` 移到原来 `idx` 的位置（即删掉后列表中它后面的那个元素所在的下标），如果已经是列表最后一个位置，则把 `cur` 设为 `0`（环形回到开头）。  

#### 代码（Python）

```python
def make_array_empty_bruteforce(nums):
    # 复制一份，后面会不断删元素
    arr = list(nums)                       # 当前剩余的元素
    order = sorted(nums)                   # 取走的顺序（从小到大）
    cur = 0                                 # 指针当前所在的下标（相对于 arr）
    steps = 0

    for val in order:                      # 按最小值的顺序处理
        idx = arr.index(val)               # O(n) 查找下标
        if cur <= idx:                     # 不需要环绕
            move = idx - cur
        else:                              # 需要先走到末尾再回到开头
            move = len(arr) - cur + idx
        steps += move + 1                  # 移动的步数 + 取走本身算一步
        arr.pop(idx)                       # 删除元素，数组长度减 1
        # 删除后，指针停在原来 idx 位置的下一个元素
        if idx == len(arr):                # 刚好删的是最后一个，环回到 0
            cur = 0
        else:
            cur = idx
    return steps
```

> **关键行中文注释**  
> - `arr.index(val)`：在当前剩余数组里找出最小值的下标。  
> - `move = len(arr) - cur + idx`：如果指针在目标左侧，需要先走到数组尾部再回到开头，等价于“环形”移动。  
> - `arr.pop(idx)`：把目标元素删掉，模拟题目中的“删除”。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层循环遍历 `n` 次，每次 `list.index`、`list.pop` 都是线性扫描，最坏需要遍历剩余的全部元素，导致总体是 `1 + 2 + … + n = O(n²)`。  
  - 大白话：如果数组有 10⁵ 个元素，暴力解大约要跑 **一万亿** 次基本操作，根本跑不完。  

- **空间复杂度**：`O(n)`  
  - 需要额外保存一个可变的列表 `arr`（长度随时会变），以及排序后的 `order`。  

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在于**每次都要线性遍历剩余数组寻找目标下标**，以及**删除元素导致下标整体搬迁**。  
我们可以把“数组里还有多少个元素”抽象成 **“活着的下标集合”**，只关心这些下标是否已经被删除，而不真的搬动数组。  

**核心想法**：  
- 把原数组的下标 `0 … n-1` 视为一排座位，每个座位上最初都有一位“观众”。  
- 观众被取走后，这个座位就空了。我们每次想知道从当前位置 `cur` 到目标下标 `idx`，沿顺时针方向要经过多少个 **仍然有观众的座位**（因为空座位不算步数）。  
- 这正好是「**区间活跃元素个数**」的查询：`cnt(cur, idx)`（如果需要环绕则拆成两段）。  

**数据结构**：**树状数组（Binary Indexed Tree，简称 BIT）**  
- BIT 能在 `O(log n)` 时间内完成：  
  1. **单点更新**：把下标 `i` 的状态从 “在” (`1`) 改成 “已删” (`0`)。  
  2. **前缀和查询**：求 `1 … i` 之间还有多少个在场的元素。  
- 用前缀和可以算出任意区间 `[l, r]` 的活跃元素数：`sum(r) - sum(l-1)`。  

**步骤**  

1. **准备**  
   - 记录每个数对应的原下标 `pos[value] = index`。  
   - 把所有数从小到大排序得到处理顺序 `sorted_vals`。  
   - 初始化 BIT，所有位置的初始值都是 `1`（表示全部在场）。  
   - `cur = 0`（指针起始在下标 0），`ans = 0`（累计步数）。  

2. **遍历每个最小值**（按照 `sorted_vals`）  
   - 设目标下标为 `idx = pos[val]`。  
   - **计算步数**  
     - 如果 `cur <= idx`（不需要环绕）：  
       `steps = query(cur, idx)`  → `BIT.sum(idx) - BIT.sum(cur-1)`  
     - 否则（需要环绕）：  
       `steps = query(cur, n-1) + query(0, idx)`  
   - 把 `steps` 加到答案 `ans`。  
   - **删除目标**：`BIT.add(idx, -1)`（把该位置的 1 变成 0）。  
   - **更新指针**：`cur = idx`（指针站在被删除位置的下一个位置），如果 `cur` 已经是数组最后一个位置，则自然在下一次查询时会环绕到 `0`，不需要额外处理。  

3. 循环结束，`ans` 即为所求的最少操作次数。  

**为什么是最优**  
- 每一次只做 `O(log n)` 的查询和更新，遍历 `n` 次，总体 `O(n log n)`。  
- 不再真的删除或搬动元素，只是把“是否在场”记录在 BIT 中，查询区间活跃元素数非常快。  

#### 代码（Python）

```python
class BIT:
    """树状数组（Fenwick Tree），支持前缀和查询和单点增减"""
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)          # 1-indexed

    def add(self, idx: int, delta: int):
        """把下标 idx (0-based) 的值加 delta"""
        i = idx + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def sum(self, idx: int) -> int:
        """返回区间 [0, idx] 的前缀和，idx 为 0-based，若 idx < 0 返回 0"""
        if idx < 0:
            return 0
        i = idx + 1
        res = 0
        while i:
            res += self.tree[i]
            i -= i & -i
        return res

    def range_sum(self, l: int, r: int) -> int:
        """返回区间 [l, r]（两端都包含）的和，要求 l <= r"""
        return self.sum(r) - self.sum(l - 1)


def make_array_empty(nums):
    n = len(nums)
    # 1. 记录每个数的原始下标
    pos = {val: i for i, val in enumerate(nums)}

    # 2. 按数值升序得到处理顺序
    sorted_vals = sorted(nums)

    # 3. 初始化 BIT，所有位置都设为 1（表示“在场”）
    bit = BIT(n)
    for i in range(n):
        bit.add(i, 1)

    cur = 0          # 当前指针所在的下标（相对于原数组）
    ans = 0

    for val in sorted_vals:               # 依次取最小的数
        idx = pos[val]                     # 目标下标

        if cur <= idx:                     # 不需要环绕
            steps = bit.range_sum(cur, idx)
        else:                              # 环绕一次
            steps = bit.range_sum(cur, n - 1) + bit.range_sum(0, idx)

        ans += steps                        # 移动步数 + 取走本身已经算在 steps 里
        bit.add(idx, -1)                    # 删除该位置
        cur = idx                           # 指针停在被删除位置的“下一个”位置

    return ans
```

> **关键行中文注释**  
> - `bit.range_sum(cur, idx)`：统计从指针 `cur`（含）到目标 `idx`（含）之间还有多少个未被删除的元素，这正是本次需要走的步数。  
> - `if cur <= idx else …`：当指针在目标左侧时直接算；在右侧时必须先走到数组末尾再回到开头，等价于两段区间求和。  
> - `bit.add(idx, -1)`：把目标位置的 “在场” 标记变为 “已删”。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序 `O(n log n)`；遍历 `n` 次，每次两次区间求和和一次单点更新，均是 `O(log n)`。  
  - 与暴力的 `O(n²)` 相比，下降了一个对数量级，能够轻松处理 `10⁵` 规模的数据。  

- **空间复杂度**：`O(n)`  
  - 需要保存下标映射 `pos`、排序后的数组以及大小为 `n+1` 的 BIT。  

---

## 心得  

- **核心技巧**：把“数组里还有多少元素”抽象成 **活跃下标集合**，并用 **树状数组（或线段树）** 快速查询区间活跃元素个数。  
- **适用题型**  
  1. 需要在动态删除元素后仍然快速统计**区间内剩余元素个数**的题目（如 “删除并查询区间和”）。  
  2. **环形遍历**且每次都要找下一个满足条件的元素的题目（如 “环形游戏”“顺时针删除”）。  
- **一句话总结**：把“删除后下标搬迁”换成“下标是否活着”的布尔位，用 BIT 把 “走几步” 转化为 “活着的元素个数”。  

---

## 反思  

- **第一反应**：看到“把数组删空”，立刻想到模拟删除、一步步移动指针的暴力思路。  
- **最容易踩的坑**  
  1. **环绕计算**：指针在目标左侧时直接求区间，在右侧时必须拆成两段，否则会少算或多算步数。  
  2. **下标映射**：因为原数组下标不随删除而改变，必须提前保存每个数对应的原下标，否则在排序后会失去位置信息。  
  3. **BIT 的 0‑based / 1‑based**：实现时注意转换，容易导致查询区间错位。  
- **下次类似题的第一步**：  
  先把“每次要走的步数”抽象为 “当前指针与目标之间仍在的元素个数”，然后寻找可以在 **对数时间** 完成的**区间计数**数据结构（BIT / 线段树 / 有序集合）。  

祝你玩转算法，玩得开心！