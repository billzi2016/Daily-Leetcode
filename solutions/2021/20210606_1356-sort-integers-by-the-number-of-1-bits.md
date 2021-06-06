# #1356. 按二进制中 1 位数目排序整数 / Sort Integers by The Number of 1 Bits

> 难度：简单 · 标签：Array、Bit Manipulation、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/sort-integers-by-the-number-of-1-bits/)

---

## 题目（英文原版）

**Description**

You are given an integer array arr. Sort the integers in the array in ascending order by the number of 1's in their binary representation and in case of two or more integers have the same number of 1's you have to sort them in ascending order.
Return the array after sorting it.

**Examples**

**Example 1:**

```
Input: arr = [0,1,2,3,4,5,6,7,8]
Output: [0,1,2,4,8,3,5,6,7]
Explantion: [0] is the only integer with 0 bits.
[1,2,4,8] all have 1 bit.
[3,5,6] have 2 bits.
[7] has 3 bits.
The sorted array by bits is [0,1,2,4,8,3,5,6,7]
```

**Example 2:**

```
Input: arr = [1024,512,256,128,64,32,16,8,4,2,1]
Output: [1,2,4,8,16,32,64,128,256,512,1024]
Explantion: All integers have 1 bit in the binary representation, you should just sort them in ascending order.
```

**Constraints**

- 1 <= arr.length <= 500
- 0 <= arr[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组（array）`arr`。请按照每个整数在二进制表示（binary representation）中出现的 `1` 的个数（即 **1 位数目**）升序排列数组；若有两个或更多整数的 `1` 的个数相同，则按整数本身的升序排列。返回排序后的数组。

**示例 1**  
输入：`arr = [0,1,2,3,4,5,6,7,8]`  
输出：`[0,1,2,4,8,3,5,6,7]`  
解释：  
- `[0]` 是唯一一个 **0** 位的整数。  
- `[1,2,4,8]` 的二进制表示各有 **1** 位。  
- `[3,5,6]` 的二进制表示各有 **2** 位。  
- `[7]` 的二进制表示有 **3** 位。  
按位数排序后得到 `[0,1,2,4,8,3,5,6,7]`。

**示例 2**  
输入：`arr = [1024,512,256,128,64,32,16,8,4,2,1]`  
输出：`[1,2,4,8,16,32,64,128,256,512,1024]`  
解释：所有整数的二进制表示均只有 **1** 位，因此直接按整数值的升序排列。

**约束条件**  
- `1 <= arr.length <= 500`  
- `0 <= arr[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **遍历数组**，把每个整数的二进制里 `1` 的个数算出来。  
   - 这里可以把整数看成一本书，二进制的每一位是书页，`1` 就是标记了“重要”的页码。我们只要把所有“重要”页码数数就行了。  
   - 计数的方法有很多，最常见的就是把整数转成二进制字符串 `bin(x)`，再用字符串的 `count('1')` 来统计，或者自己写一个循环不断右移并检查最低位是否为 `1`（`x & 1`）。

2. **根据两个规则排序**  
   - 先按照 “1 的个数” 从小到大排列。  
   - 如果两个数的 “1 的个数” 相同，再按照数值本身的大小排列。  

Python 的 `list.sort`（或 `sorted`）可以接受 `key` 参数，只要把 **(1 的个数, 数值)** 这对元组作为排序键，就能一次完成两层排序。  
这就像在图书馆里先把书按“重要页数”排好，再把同样重要的书按书号顺序排。

**为什么一定对？**  
排序的定义就是把元素按照给定的比较规则重新排列。我们把每个元素映射成 `(popcount, value)`，并让排序函数按照元组的字典序比较——这正好对应题目要求的两层比较规则，所以结果必然满足题目。

#### 代码（Python）

```python
from typing import List

def sortByBits(arr: List[int]) -> List[int]:
    # 计算一个整数二进制中 1 的个数的函数
    def popcount(x: int) -> int:
        # 方法一：使用 Python 3.8+ 的内置 bit_count（硬件级别快）
        return x.bit_count()
        # 方法二（如果没有 bit_count）：
        # cnt = 0
        # while x:
        #     cnt += x & 1      # 检查最低位是否为 1
        #     x >>= 1           # 右移一位
        # return cnt

    # sorted 会返回一个新列表，key 使用 (popcount, value) 元组
    return sorted(arr, key=lambda v: (popcount(v), v))


# ------------------- 测试 -------------------
if __name__ == "__main__":
    print(sortByBits([0,1,2,3,4,5,6,7,8]))
    # 输出: [0, 1, 2, 4, 8, 3, 5, 6, 7]

    print(sortByBits([1024,512,256,128,64,32,16,8,4,2,1]))
    # 输出: [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
```

#### 复杂度  

- **时间复杂度：** `O(n log n)`  
  - `n` 是数组长度。排序本身需要 `n log n` 次比较。  
  - 计算每个数的 `popcount` 是 `O(1)`（硬件指令）或 `O(位数)`，但位数 ≤ 14（因为 `arr[i] ≤ 10⁴`），可以视为常数。  
  - 所以总体仍然是 `n log n`，也就是“先把所有书排好序，需要的时间随书的数量的对数增长”。

- **空间复杂度：** `O(n)`  
  - Python 的排序会创建一个额外的列表来存放排好序的结果，大小正好是 `n`。  
  - 其他临时空间（比如 `popcount` 计数器）都是常数级别的。

---

### 2. 最优解

#### 思路  

暴力解已经能够通过所有测试，但我们仍可以把时间进一步压到 **`O(n)`**（线性）：

- 观察到 **`arr[i] ≤ 10⁴`**，即二进制位数最多只有 **14 位**（因为 `2¹⁴ = 16384 > 10⁴`）。  
- “1 的个数” 的取值范围只会是 **0 ~ 14**，这意味着我们可以把元素按 **“1 的个数”** 分到 **15 个桶**（bucket）里。  
- 桶内再按照数值大小排序（因为同一桶内的元素 `popcount` 相同，只需要保证数值升序）。  
- 最后按桶的顺序（从 0 到 14）依次把桶里的元素拼接起来，即得到最终答案。

这就是**计数排序（Bucket Sort）**的思路，适合“关键字取值范围很小”的情况。我们把 “1 的个数” 当作关键字，先把所有数分组，再在每组内部做一次普通的升序排序。

**类比**：把所有书先按“重要页数”放进不同的抽屉（抽屉编号 = 重要页数），抽屉里的书再按照书号排好。最后依次打开抽屉，取出书，就完成了全部的排序。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def sortByBits_opt(arr: List[int]) -> List[int]:
    # 1. 统计每个数的 1 的个数（使用内置 bit_count，常数时间）
    def popcount(x: int) -> int:
        return x.bit_count()

    # 2. 创建 15 个桶，键为 popcount，值为该桶里的数字列表
    buckets = defaultdict(list)          # defaultdict 自动创建空列表

    for num in arr:
        cnt = popcount(num)               # 计算 1 的个数
        buckets[cnt].append(num)          # 放进对应的桶

    # 3. 对每个桶内部进行普通升序排序（因为同一桶的 cnt 相同，只剩数值比较）
    for cnt in buckets:
        buckets[cnt].sort()                # Python Timsort，时间约 O(k log k)

    # 4. 按 cnt 从小到大依次取出桶里的元素，拼接成结果
    result = []
    for cnt in range(15):                  # 0~14 共 15 个可能的 cnt
        result.extend(buckets.get(cnt, []))

    return result


# ------------------- 测试 -------------------
if __name__ == "__main__":
    print(sortByBits_opt([0,1,2,3,4,5,6,7,8]))
    # [0, 1, 2, 4, 8, 3, 5, 6, 7]

    print(sortByBits_opt([1024,512,256,128,64,32,16,8,4,2,1]))
    # [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
```

#### 复杂度  

- **时间复杂度：** `O(n + m log m)`  
  - `n` 是数组长度，用来遍历一次把数字放进桶里。  
  - `m` 是每个桶的大小，所有桶内的排序总和不超过 `n log n`，但因为每个桶的元素数量非常少（最多 500 / 15 ≈ 34），实际常数很小。  
  - 在最坏情况下仍然是 **线性** `O(n)`，因为 `log m` 的基数很小，且 `m ≤ n`。  
  - 相比直接 `n log n` 的排序，这种做法在 `n` 很大、关键字范围很小时会更快。

- **空间复杂度：** `O(n)`  
  - 需要额外的桶来存放所有元素，整体占用和原数组等量的空间。  
  - 其它辅助空间（如 `defaultdict`）也是线性级别的。

---

## 心得

- **核心技巧**：**计数排序 + 位计数（popcount）**  
  把 “1 的个数” 这类取值范围很小的属性当作关键字，用桶（bucket）把元素分组，再在每组内部排序。

- **适用的题型**  
  1. **按某个离散属性排序**（例如按数字的奇偶性、按字符出现次数等）。  
  2. **位操作相关的题目**（如“统计数组中每个数的二进制 1 的个数”）。  
  3. **范围已知且小的计数排序**（比如把 0~100 的年龄排序）。

- **一句话总结**：  
  “把数字的 1 的个数当作桶号，先分桶再在桶内排序，即可线性时间搞定。”

---

## 反思

- **第一反应**：直接想到 “遍历 + 统计 1 的个数 + 自定义排序”。这是一种最自然、最安全的思路。

- **最容易踩的坑**  
  1. **位数统计错误**：如果手写 `popcount` 时忘记右移或掩码，可能会进入死循环。  
  2. **边界条件**：`arr` 里可能出现 `0`，它的 1 的个数是 `0`，要确保桶 `0` 能正确处理。  
  3. **桶的顺序**：计数排序时必须严格按 `cnt` 从小到大遍历，否则会破坏“按 1 的个数升序”的要求。

- **下次遇到同类题**，第一步应该问自己：  
  “这个排序键的取值范围大吗？如果很小，是不是可以用桶/计数排序来把时间降到线性？”  

这样就能快速定位到最优解的方向。