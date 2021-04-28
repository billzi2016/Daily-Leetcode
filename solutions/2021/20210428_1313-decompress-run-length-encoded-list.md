# #1313. 解压缩游程编码列表 / Decompress Run-Length Encoded List

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/decompress-run-length-encoded-list/)

---

## 题目（英文原版）

**Description**

We are given a list nums of integers representing a list compressed with run-length encoding.
Consider each adjacent pair of elements [freq, val] = [nums[2*i], nums[2*i+1]] (with i >= 0).  For each such pair, there are freq elements with value val concatenated in a sublist. Concatenate all the sublists from left to right to generate the decompressed list.
Return the decompressed list.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4]
Output: [2,4,4,4]
Explanation: The first pair [1,2] means we have freq = 1 and val = 2 so we generate the array [2].
The second pair [3,4] means we have freq = 3 and val = 4 so we generate [4,4,4].
At the end the concatenation [2] + [4,4,4] is [2,4,4,4].
```

**Example 2:**

```
Input: nums = [1,1,2,3]
Output: [1,3,3]
```

**Constraints**

- 2 <= nums.length <= 100
- nums.length % 2 == 0
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

我们得到一个整数数组 `nums`，它表示经过 **游程编码（run‑length encoding）** 压缩后的列表。  
将相邻的两个元素视为一组 `[freq, val] = [nums[2*i], nums[2*i+1]]`（其中 `i ≥ 0`）。对于每一组，生成 `freq` 个值为 `val` 的元素，形成一个子数组（subarray）。把所有子数组按照从左到右的顺序依次拼接，即得到解压后的列表。  
返回该解压后的列表。

**示例 1**  
```text
输入: nums = [1,2,3,4]
输出: [2,4,4,4]
解释: 第一个配对 [1,2] 表示 freq = 1，val = 2，生成数组 [2]。  
第二个配对 [3,4] 表示 freq = 3，val = 4，生成数组 [4,4,4]。  
最终拼接得到 [2] + [4,4,4] = [2,4,4,4]。
```

**示例 2**  
```text
输入: nums = [1,1,2,3]
输出: [1,3,3]
```

**约束条件**  

- `2 <= nums.length <= 100`
- `nums.length % 2 == 0`
- `1 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
题目把原数组 `nums` 看成若干个 **[freq, val]** 的小组，每两个相邻元素构成一组。  
直观的做法是：

1. 按顺序遍历 `nums`，每次取出一组 `[freq, val]`。  
2. 按 `freq` 的次数把 `val` 加到结果列表里。  
3. 把所有小组的结果依次拼接，得到最终的“解压”数组。

> **数据结构类比**：  
> - `list`（Python 列表）就像我们生活中的 **装东西的盒子**，可以随时往里放（`append`）或一次性放很多（`extend`）。  
> - 这里的 `freq` 相当于“要放多少个同样的东西”，`val` 就是“这个东西的具体内容”。

因为每一次我们都严格按照题目要求把 **freq 个 val** 放进去，最终得到的列表一定和题目要求的“解压后列表”相同，所以方法是 **必然正确** 的。

#### 代码（Python）

```python
def decompressRLElist(nums):
    """
    暴力解：逐组展开
    :param nums: List[int]，长度为偶数，每两个元素是 [freq, val]
    :return: List[int]，解压后的数组
    """
    result = []                         # 用来存放最终答案的盒子
    # i 步进为 2，保证每次取到一组 [freq, val]
    for i in range(0, len(nums), 2):
        freq = nums[i]                   # 要重复的次数
        val = nums[i + 1]                # 要写入的值
        # 把 val 重复 freq 次放进 result
        for _ in range(freq):
            result.append(val)           # 逐个加入，类似“一颗颗放进盒子”
    return result
```

#### 复杂度  

- **时间复杂度**：`O(N)`  
  - 这里的 `N` 指的是**解压后**数组的长度（即所有 `freq` 之和）。  
  - 直观上可以理解为：我们需要 **一次遍历每个要输出的元素**，所以时间随输出规模线性增长。  

- **空间复杂度**：`O(N)`  
  - 需要一个额外的列表来存放答案，大小正好是解压后数组的长度。  

---

### 2. 最优解

#### 思路  
在上面的暴力实现里，向结果列表中逐个 `append` 是完全可以接受的，因为 Python 的 `list.append` 均摊时间是 `O(1)`。  
不过我们可以把 “一次放入多个相同元素” 这一步写得更简洁、更高效：

- 使用列表的乘法操作 `val * freq` 可以直接得到一个 **包含 freq 个 val 的子列表**。  
- 再利用 `list.extend` 把这个子列表一次性拼接到结果列表中。  

这两个操作在底层都是 **线性复制**，总体仍然是 `O(N)`，但代码更简洁，思路更“一次性”。  

> **核心技巧**：  
> - **列表乘法** (`[val] * freq`) 相当于“复制若干份相同的东西”，就像我们把同一本书复印多份。  
> - **extend** 把一个完整的子列表一次性“倒进”大盒子，省去逐个 `append` 的循环。

#### 代码（Python）

```python
def decompressRLElist(nums):
    """
    最优解：利用列表乘法和 extend 一次性展开
    :param nums: List[int]
    :return: List[int]
    """
    result = []                         # 最终答案盒子
    for i in range(0, len(nums), 2):
        freq = nums[i]
        val = nums[i + 1]
        # 生成子列表 [val, val, ..., val]（长度为 freq）
        sub = [val] * freq
        result.extend(sub)              # 一次性把子列表倒进结果盒子
    return result
```

#### 复杂度  

- **时间复杂度**：`O(N)`  
  - 与暴力解相同，因为无论是逐个 `append` 还是一次性 `extend`，都必须把 **每个要输出的元素** 写进去。  

- **空间复杂度**：`O(N)`  
  - 仍然需要存放解压后的全部元素，只是临时子列表 `sub` 的大小最多是当前 `freq`，整体空间仍为线性。  

---

## 心得

- **核心技巧**：利用 **列表乘法** 生成重复元素的子列表，再用 **extend** 一次性拼接。  
- **适用的题型**：  
  1. “把数组按照某种规则展开/复制”的题目（如 “重复元素展开”）。  
  2. 需要把 **相同元素多次出现** 的压缩形式恢复的题目（如 “压缩字符串解码”）。  
  3. 需要**批量添加**元素到列表的场景（如 “批量插入”）。  
- **一句话总结**：把“重复”抽象成“复制子列表”，一次性倒进结果，代码简洁且不失效率。

---

## 反思

- **第一反应**：看到“频率 + 值”的配对，就想到 **循环 `freq` 次把 `val` 放进去**，这就是最直接的暴力思路。  
- **最容易踩的坑**：  
  1. **下标越界**：一定要每次 `i` 步进 2，确保 `i+1` 有效。  
  2. **频率为 0**（本题不存在，但如果出现要注意不要产生空子列表）。  
  3. **输出顺序**：必须保持左到右的顺序，否则会得到错误的结果。  
- **下次遇到同类题**，第一步应该思考 **“这是一种批量复制的模式吗？”**，如果是，就先尝试 **列表乘法 + extend**，再决定是否需要更复杂的数据结构。