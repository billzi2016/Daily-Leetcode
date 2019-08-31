# #556. Next Greater Element III / Next Greater Element III

> 难度：中等 · 标签：Math、Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/next-greater-element-iii/)

---

## 题目（英文原版）

**Description**

Given a positive integer n, find the smallest integer which has exactly the same digits existing in the integer n and is greater in value than n. If no such positive integer exists, return -1.
Note that the returned integer should fit in 32-bit integer, if there is a valid answer but it does not fit in 32-bit integer, return -1.

**Examples**

**Example 1:**

```
Input: n = 12
Output: 21
```

**Example 2:**

```
Input: n = 21
Output: -1
```

**Constraints**

- 1 <= n <= 231 - 1

---

## 题目（中文翻译）

给定一个正整数 `n`，找出一个最小的整数，使其恰好由 `n` 的所有数字重新排列而成，并且数值严格大于 `n`。如果不存在这样的正整数，返回 `-1`。  
需要注意，返回的整数必须能够放入 32 位有符号整数（32-bit integer）中；如果存在符合条件的答案但超出 32 位整数范围，同样返回 `-1`。

**示例 1**  
**示例 2**  
**约束条件**  

**示例：**  
示例 1:  
```
Input: n = 12
Output: 21
```

示例 2:  
```
Input: n = 21
Output: -1
```

约束条件：  
- `1 <= n <= 2^31 - 1`   (即 231 - 1)

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把数字 `n` 的每一位都拿出来，**枚举所有可能的排列**（Permutation），然后挑出：

1. **比 `n` 大** 的排列  
2. 在这些排列里取 **最小的** 那个  

这一步可以把“把数字的每一位重新排位”想象成 **把一副牌重新洗牌**，只要把所有洗出来的顺序全部列出来，就一定能找到比原来顺序更大的那一副（如果有的话）。  

- **用到的数据结构**  
  - `list`：把整数的每一位存成列表，方便后面交换、切片。  
  - `itertools.permutations`：Python 标准库里专门生成**全排列**的工具，就像字典里查每个词的所有写法。  

- **为什么一定对**  
  - 全排列把所有可能的位序都穷举了，遗漏的情况不存在。  
  - 只要在这些排列中挑出满足条件的最小值，就一定是答案（如果有答案的话）。  

- **时间/空间复杂度**  
  - 设数字 `n` 有 `k` 位（`k ≤ 10`，因为 32 位整数最多 10 位），全排列的数量是 `k!`（阶乘），每个排列我们还要把列表转成整数再比较大小。  
  - **时间复杂度** 大约是 `O(k! * k)`，因为生成每个排列本身要遍历 `k` 位。  
  - **空间复杂度** 需要保存当前排列，最坏情况是 `O(k)`（列表本身），加上 `itertools` 的迭代器内部也会占用 `O(k)`。  

> 大白话：如果数字有 5 位，`5! = 120`，也就是说最多要检查 120 种排法；如果是 9 位，`9! = 362880`，检查的次数就会爆炸，跑得很慢。

#### 代码（Python）  

```python
import itertools

def nextGreaterElement_bruteforce(n: int) -> int:
    # 把整数拆成字符列表，方便后面拼接成新整数
    digits = list(str(n))                     # ['1', '2', ...]
    k = len(digits)

    # 用 set 去重，防止相同数字产生重复排列（比如 122 会有重复）
    candidates = set()

    # itertools.permutations 会生成所有长度为 k 的排列
    for perm in itertools.permutations(digits, k):
        # 把元组 ('2','1') 重新拼成整数 21
        num = int(''.join(perm))
        if num > n:                           # 只保留比原数大的
            candidates.add(num)

    if not candidates:                        # 没有符合条件的排列
        return -1

    ans = min(candidates)                     # 取最小的那个
    # 需要确保结果仍然在 32 位有符号整数范围内
    return ans if ans < 2**31 else -1
```

#### 复杂度  

- **时间复杂度**：`O(k! * k)`  
  - `k!` 是全排列的数量，`k` 是把每个排列转成整数的代价。  
- **空间复杂度**：`O(k)`（不计入返回的 `candidates` 集合，因为最坏只会存 `k!` 个整数，但在实际使用中我们只保留满足条件的最小值）  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **枚举所有排列**，当位数稍大时就会失控。  
其实我们只需要 **找出比原数大的最近一个排列**，这正是“下一个字典序排列”(next permutation) 的概念。  

**下一个字典序排列的步骤**（把它想成把一个单词的字母重新排，使它在字典里紧挨着原单词的下一个）：

1. **从右往左找到第一个“下降点”**  
   - 即 `digits[i] < digits[i+1]` 的最右侧 `i`。  
   - 这一步相当于在单词里找出从后往后第一次出现“字母顺序变小”的位置。  

2. **在下降点右侧的子数组中，找到比 `digits[i]` 大但最小的那个**（称为 `j`）  
   - 因为右侧已经是 **非递增**（从大到小） 的，所以从右往左第一个大于 `digits[i]` 的数字就是答案。  

3. **交换 `i` 与 `j`**  
   - 把较小的数字放到左边，使整体变大。  

4. **把 `i` 右侧的所有数字 **倒序**（即变成升序）**  
   - 之前右侧是降序的，倒序后变成最小的排列，保证整体是**紧邻原数的下一个更大数**。  

把这些步骤写成代码后，只需要 **一次线性遍历**（`O(k)`） 就能得到答案。  

最后，还要检查：

- 结果是否仍在 32 位有符号整数范围内 (`< 2**31`)；如果超出，返回 `-1`。  

> 类比：如果你有一本字典，想找比当前单词稍微靠后的单词，只需要看最右侧的字母哪里可以换成更大的字母，然后把后面的字母排成最小的顺序，这样得到的单词就是下一个。  

#### 代码（Python）  

```python
def nextGreaterElement(n: int) -> int:
    # 1. 把整数拆成字符列表，方便原地修改
    digits = list(str(n))          # 例如 n=1234 -> ['1','2','3','4']
    length = len(digits)

    # 2. 从右往左找第一个下降点 i，使得 digits[i] < digits[i+1]
    i = length - 2                 # 从倒数第二位开始检查
    while i >= 0 and digits[i] >= digits[i + 1]:
        i -= 1

    # 如果遍历完都没有找到，说明整个序列是非递增的（比如 54321），
    # 已经是最大的排列，找不到更大的数
    if i < 0:
        return -1

    # 3. 在 i 右侧（即 i+1 .. end）找到第一个比 digits[i] 大的数字 j
    # 因为右侧是降序的，倒着找第一个大于 digits[i] 的就是最小的那个
    j = length - 1
    while digits[j] <= digits[i]:
        j -= 1

    # 4. 交换 i 与 j
    digits[i], digits[j] = digits[j], digits[i]

    # 5. 把 i 右侧的子数组逆序（从大到小变成从小到大）
    # 逆序等价于把列表切片后翻转
    digits[i + 1:] = reversed(digits[i + 1:])

    # 6. 把列表重新拼成整数
    result = int(''.join(digits))

    # 7. 检查是否超过 32 位有符号整数上限
    return result if result < 2 ** 31 else -1
```

#### 复杂度  

- **时间复杂度**：`O(k)`  
  - 只遍历了一遍数字的位数（最多 10 次），每一步都是常数操作。  
  - 与暴力解的 `O(k! * k)` 相比，速度提升是指数级的。  

- **空间复杂度**：`O(k)`  
  - 需要一个保存数字字符的列表，长度等于位数 `k`（≤10）。  
  - 只使用了常数级的额外变量 (`i, j, result`)。  

---

## 心得  

- **核心技巧**：**下一个字典序排列**（Next Permutation）。  
- **适用的题型**  
  1. “下一个更大的数”系列，如 *Next Permutation*（LeetCode 31）  
  2. “排列组合”中要求找最小/最大满足条件的排列，如 *Permutations II*（LeetCode 47）  
  3. “字典序”相关的字符串/数组题目，如 *Largest Number After Digit Swaps*（自定义）  

> **解题钥匙**：**只在“下降点”左侧动手，右侧全局逆序**，即可一次遍历得到紧邻的更大排列。  

---

## 反思  

- **第一反应**：直接想到把所有位的排列全部列举出来。  
- **最容易踩的坑**  
  - 忘记判断 **32 位整数上限**（`2**31 - 1`），导致返回超范围的答案。  
  - 对于全部降序的数字（如 `4321`），需要提前返回 `-1`，否则会在找 `j` 时出现越界。  
  - 在寻找 `j` 时，如果直接从左往右找，可能会选到不是最小的大于 `digits[i]` 的数，导致不是最近的更大数。  

- **下次遇到同类题**，第一步应该：**先定位右侧的“下降点”**，这一步往往是瓶颈所在，后面的交换和逆序就能保证得到最优解。