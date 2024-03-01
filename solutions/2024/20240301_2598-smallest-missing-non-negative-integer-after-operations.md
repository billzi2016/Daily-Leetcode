# #2598. **操作后最小缺失非负整数** / Smallest Missing Non-negative Integer After Operations

> 难度：中等 · 标签：Array、Hash Table、Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/smallest-missing-non-negative-integer-after-operations/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and an integer value.
In one operation, you can add or subtract value from any element of nums.
The MEX (minimum excluded) of an array is the smallest missing non-negative integer in it.
Return the maximum MEX of nums after applying the mentioned operation any number of times.

**Examples**

**Example 1:**

```
Input: nums = [1,-10,7,13,6,8], value = 5
Output: 4
Explanation: One can achieve this result by applying the following operations:
- Add value to nums[1] twice to make nums = [1,0,7,13,6,8]
- Subtract value from nums[2] once to make nums = [1,0,2,13,6,8]
- Subtract value from nums[3] twice to make nums = [1,0,2,3,6,8]
The MEX of nums is 4. It can be shown that 4 is the maximum MEX we can achieve.
```

**Example 2:**

```
Input: nums = [1,-10,7,13,6,8], value = 7
Output: 2
Explanation: One can achieve this result by applying the following operation:
- subtract value from nums[2] once to make nums = [1,-10,0,13,6,8]
The MEX of nums is 2. It can be shown that 2 is the maximum MEX we can achieve.
```

**Constraints**

- 1 <= nums.length, value <= 105
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

你得到一个下标从 0 开始的整数数组 `nums` 和一个整数 `value`。  
在一次操作中，你可以将 `value` 加到 `nums` 的任意元素上，或者从该元素上减去 `value`。  
数组的 MEX（minimum excluded）是数组中最小的缺失非负整数。  
返回对数组进行任意次数上述操作后，能够得到的 **最大** MEX。

### 示例

#### 示例 1
```
Input: nums = [1,-10,7,13,6,8], value = 5
Output: 4
```
**解释**：可以通过以下操作得到该结果  
- 对 `nums[1]` 加 `value` 两次，使 `nums` 变为 `[1,0,7,13,6,8]`  
- 对 `nums[2]` 减 `value` 一次，使 `nums` 变为 `[1,0,2,13,6,8]`  
- 对 `nums[3]` 减 `value` 两次，使 `nums` 变为 `[1,0,2,3,6,8]`  

此时数组的 MEX 为 4。可以证明 4 是能够达到的最大 MEX。

#### 示例 2
```
Input: nums = [1,-10,7,13,6,8], value = 7
Output: 2
```
**解释**：可以通过以下操作得到该结果  
- 对 `nums[2]` 减 `value` 一次，使 `nums` 变为 `[1,-10,0,13,6,8]`  

此时数组的 MEX 为 2。可以证明 2 是能够达到的最大 MEX。

### 约束条件
- `1 <= nums.length, value <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**穷举**所有可能的操作，然后求出每种情况下数组的 MEX，取最大的那个。  
- 对每个元素 `nums[i]`，我们可以把它加上或减去 `value` 任意次。  
- 也就是说，`nums[i]` 能变成 **所有** 与 `nums[i]` 同余（mod `value`）的整数。  

如果把这件事想象成“**字典**”，  
- **键（key）**：`nums[i]` 在模 `value` 意义下的余数 `r = nums[i] % value`（就像单词的拼音）  
- **值（value）**：这把键对应的“可选数字集合”，即 `{ r, r+value, r+2·value, … }`（像字典里对应的解释页码）  

暴力做法就是：

1. 对每个元素，枚举它可以变成的所有整数（理论上是无限多）。  
2. 把这些整数放进一个大集合，计算集合的 MEX。  
3. 对所有可能的组合取最大 MEX。

**为什么这个方法正确？**  
因为我们把“所有合法的变化”都考虑进去了，必然不会漏掉最优解。

**为什么会超时？**  
- 第 1 步的枚举是无限的，实际上我们只能枚举到某个上界（比如 `[-10^9, 10^9]`），但即便如此，枚举次数仍然是 **O(n·range/value)**，天文数字。  
- 再加上每次都要重新计算 MEX（线性扫描），整体复杂度接近 **O(n·range)**，在最坏情况下会达到 `10^5 × 10^9`，根本不可接受。

**时间/空间复杂度的大白话**  
- **时间复杂度 O(n·range)**：想象你要检查 `n` 本书的每一页，而每本书有 `range`（上千上万）页，这相当于在图书馆里走来走去，根本走不完。  
- **空间复杂度 O(range)**：需要把所有可能出现的数字都存下来，等于把整个图书馆的目录都装进电脑，显然不现实。

---

#### 代码（Python）

```python
def max_mex_bruteforce(nums, value):
    # 这里仅作演示，实际运行会超时
    possible = set()
    # 为了防止无限枚举，这里随便设一个大范围（不可靠）
    BOUND = 10**5
    for x in nums:
        # 计算所有可以到达的数（仅示例）
        r = x % value
        for k in range(-BOUND, BOUND + 1):
            possible.add(r + k * value)

    # 计算 MEX
    mex = 0
    while mex in possible:
        mex += 1
    return mex
```

#### 复杂度

- **时间复杂度**：`O(n·BOUND)` —— 这里的 `BOUND` 为我们人为设定的搜索上界，实际会非常大。  
- **空间复杂度**：`O(n·BOUND)` —— 需要保存所有可能出现的数，同样不切实际。

---

### 2. 最优解

#### 思路  

从暴力解可以看到：**每个元素只能落在它对应的余数类**（`nums[i] % value`）。  
因此，**只需要关心余数的出现次数**，不必枚举所有具体的整数。

1. **统计余数频次**  
   - 把每个 `nums[i]` 的余数 `r = ((nums[i] % value) + value) % value`（保证非负）计数。  
   - 这一步相当于在“字典”里记下每个键（余数）对应的“可用次数”。  

2. **从 0 开始贪心填数**  
   - 目标是让数组尽可能包含 `0, 1, 2, …`，因为 MEX 正是第一个 **缺失** 的非负整数。  
   - 对每个候选数字 `t`，只要我们还有 **至少一个** 余数为 `t % value` 的元素，就可以把其中一个元素调成 `t`，然后把该余数的计数减 1。  
   - 当某个 `t` 对应的余数计数已经用完时，`t` 就是 **当前的 MEX**，也是我们能得到的最大 MEX（因为更大的 MEX 必然也缺少更小的数）。

3. **为什么贪心是最优的？**  
   - 每一步我们只使用**最小可能的**余数来生成当前的数字。  
   - 若在某一步放弃使用可用的余数，而改为让更大的数占用它，必然导致更小的数缺失，MEX 立刻变小。  
   - 因此**不使用就会让 MEX 下降**，使用则把 MEX 向前推进，贪心不可能错。

**核心概念解释**  

- **模（mod）**：`a % m` 表示把 `a` 按 `m` 分成若干段，余下的那段叫余数。比如 `17 % 5 = 2`，因为 `17 = 3·5 + 2`。  
- **哈希表/计数数组**：把余数当作“键”，对应的出现次数当作“值”。这就像查字典一样，键是词（余数），值是页码（还有多少个可以用）。

**算法步骤图示（文字版）**  

```
nums = [1, -10, 7, 13, 6, 8], value = 5
余数 = [1, 0, 2, 3, 1, 3]   ← 统计频次 → freq[0]=1, freq[1]=2, freq[2]=1, freq[3]=2, freq[4]=0
t = 0 → 0%5=0 → freq[0]>0 → 用掉一个 → freq[0]=0
t = 1 → 1%5=1 → freq[1]>0 → 用掉一个 → freq[1]=1
t = 2 → 2%5=2 → freq[2]>0 → 用掉一个 → freq[2]=0
t = 3 → 3%5=3 → freq[3]>0 → 用掉一个 → freq[3]=1
t = 4 → 4%5=4 → freq[4]==0 → 停止，MEX = 4
```

#### 代码（Python）

```python
def max_mex(nums, value):
    """
    返回在任意次加/减 value 后，数组能够达到的最大 MEX。
    思路：统计每个余数的出现次数，然后贪心从 0 开始尝试构造。
    """
    # 1. 统计余数出现次数（用列表模拟哈希表，速度更快）
    freq = [0] * value          # freq[r] 表示余数 r 的元素还有多少个可以使用
    for x in nums:
        # Python 的 % 可能返回负数，先把它规整到 [0, value-1]
        r = ((x % value) + value) % value
        freq[r] += 1

    # 2. 贪心尝试构造 0,1,2,...，直到某个数对应的余数用光为止
    mex = 0
    while True:
        r = mex % value          # 目标数 mex 所需的余数
        if freq[r] == 0:         # 没有可用的元素可以变成 mex
            break                # 这就是最大可能的 MEX
        freq[r] -= 1             # 使用一个余数为 r 的元素把它调成 mex
        mex += 1                 # 尝试下一个更大的数

    return mex
```

#### 复杂度

- **时间复杂度：`O(n + answer)`**  
  - 统计余数遍历一次数组，`O(n)`。  
  - 贪心循环最多尝试 `answer` 次，而 `answer`（即最终的 MEX）不可能超过数组长度 `n`（每生成一个新数至少要消耗一个元素），所以整体是线性 `O(n)`。  
  - **大白话**：我们只把每本书的目录看了一遍，然后再按顺序检查一次缺的章节，总共不超过两遍书。

- **空间复杂度：`O(value)`**  
  - 需要一个长度为 `value` 的计数数组来存余数的出现次数。  
  - 即使 `value` 最大是 `10^5`，这也只相当于几百 KB 的内存，完全可以接受。

---

## 心得

- **核心技巧**：把“加/减 value 任意次”转化为“只看余数”，利用**模运算 + 计数 + 贪心**求最大 MEX。  
- **适用场景**：  
  1. 需要把数值映射到若干“等价类”（余数、颜色、状态）再进行计数的问题。  
  2. 需要构造连续非负整数序列，且每个元素只能使用一次的场景。  
  3. 类似的题目还有 “找出数组中缺失的最小正整数”（LeetCode 41）以及 “按模分组后求最大连续段” 等。  
- **一句话总结解题钥匙**：  
  *“把所有可以到达的数划分到同余类，用计数贪心依次填满 0、1、2…，第一个填不上的就是最大 MEX。”*

---

## 反思

- **第一反应**：看到“可以任意次加/减同一个数”，立刻想到 **模运算**——相同余数的数可以互相转换。  
- **最容易踩的坑**：  
  - 负数取模在 Python 会得到负余数，需要手动转成 `[0, value-1]` 区间。  
  - 误以为 MEX 可能大于数组长度；实际上每生成一个新数都要消耗一个元素，最大不超过 `len(nums)`。  
  - 忽视 `value` 可能很大，直接用字典会稍慢，但仍在可接受范围；使用列表计数更高效。  
- **下次遇到同类题**：第一步先**把操作抽象成“等价类”**（如余数、模、颜色），再**统计每类的资源量**，最后**贪心尝试构造目标序列**。这样思路清晰，代码也自然简洁。