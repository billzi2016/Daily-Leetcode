# #1734. 解码异或置换 / Decode XORed Permutation

> 难度：中等 · 标签：Array、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/decode-xored-permutation/)

---

## 题目（英文原版）

**Description**

There is an integer array perm that is a permutation of the first n positive integers, where n is always odd.
It was encoded into another integer array encoded of length n - 1, such that encoded[i] = perm[i] XOR perm[i + 1]. For example, if perm = [1,3,2], then encoded = [2,1].
Given the encoded array, return the original array perm. It is guaranteed that the answer exists and is unique.

**Examples**

**Example 1:**

```
Input: encoded = [3,1]
Output: [1,2,3]
Explanation: If perm = [1,2,3], then encoded = [1 XOR 2,2 XOR 3] = [3,1]
```

**Example 2:**

```
Input: encoded = [6,5,4,6]
Output: [2,4,1,5,3]
```

**Constraints**

- 3 <= n < 105
- n is odd.
- encoded.length == n - 1

---

## 题目（中文翻译）

有一个整数数组 **perm**，它是前 **n** 个正整数的一个排列（permutation），且 **n** 总是奇数。  
它被编码成另一个长度为 **n‑1** 的整数数组 **encoded**，满足  

```
encoded[i] = perm[i] XOR perm[i + 1]
```  

例如，若 `perm = [1,3,2]`，则 `encoded = [2,1]`（因为 `1 XOR 3 = 2`，`3 XOR 2 = 1`）。

给定 **encoded** 数组，返回原始数组 **perm**。题目保证答案唯一且必定存在。

### 示例

**示例 1**  
**输入**: `encoded = [3,1]`  
**输出**: `[1,2,3]`  
**解释**: 若 `perm = [1,2,3]`，则 `encoded = [1 XOR 2, 2 XOR 3] = [3,1]`

**示例 2**  
**输入**: `encoded = [6,5,4,6]`  
**输出**: `[2,4,1,5,3]`

### 约束条件

- `3 <= n < 10^5`
- `n` 为奇数
- `encoded.length == n - 1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把 `perm[0]` 先假设为 1、2、…、n 中的某个数**，  
然后利用已知的 `encoded` 逐个恢复后面的元素：

```
perm[i] = perm[i-1] XOR encoded[i-1]      (i ≥ 1)
```

这一步就像把 **“上一格的数”** 和 **“两格之间的密码（XOR）”** 进行“异或”，就能推出 **“下一格的数”**。  

得到完整的 `perm` 之后，再检查它是不是一个合法的排列（即每个 1~n 恰好出现一次）。如果合法，就找到了答案。

> **数据结构类比**  
> - `set`（集合）好比一本“名字册”，我们可以快速判断一个数字是否已经出现过，类似于查字典时看某个词是否在词表里。  

**为什么一定能找到唯一答案**：题目保证 `perm` 是唯一的，只要我们遍历所有可能的 `perm[0]`，必定会在某一次得到合法的排列。

#### 代码（Python）

```python
from typing import List

def decode(encoded: List[int]) -> List[int]:
    n = len(encoded) + 1          # 原数组长度
    # 依次尝试 perm[0] = 1 .. n
    for first in range(1, n + 1):
        perm = [first]            # 把假设的第一个数放进结果里
        # 根据 encoded 逐个推出后面的数
        for i in range(len(encoded)):
            # perm[i+1] = perm[i] XOR encoded[i]
            perm.append(perm[i] ^ encoded[i])

        # 用集合检查是否恰好出现了 1~n（不重复也不缺失）
        if set(perm) == set(range(1, n + 1)):
            return perm          # 找到唯一合法的排列，直接返回
    # 题目保证一定有解，这行理论上不会执行
    return []
```

*关键行中文注释*  
- `for first in range(1, n + 1)`: 把 `perm[0]` 的所有可能枚举一遍。  
- `perm.append(perm[i] ^ encoded[i])`: 利用 XOR 的逆运算恢复下一个元素。  
- `if set(perm) == set(range(1, n + 1))`: 检查是否构成合法排列（集合相等即每个数出现一次）。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层循环最多 `n` 次（尝试每个可能的起点），  
  - 内层遍历 `encoded` 长度为 `n‑1`，总共约 `n·(n‑1) ≈ n²` 次操作。  
  - 用大白话说，就是“如果 n 是 10,000，最坏情况下要做 100,000,000 次运算”。  

- **空间复杂度**：`O(n)`  
  - 需要存放临时的 `perm` 列表以及集合 `set(perm)`，大小和 `n` 成正比。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **“枚举所有可能的起点”**，其实我们可以 **直接算出 `perm[0]`**，不必尝试。关键在于 XOR 的 **“全局消除”** 特性。

1. **先算出 1~n 的全部异或**  
   把 `1, 2, …, n` 全部异或一遍，记为 `total`.  
   这一步相当于把一本完整的“名字册”压成一个“总密码”。  

2. **利用 `encoded` 的奇偶位**  
   观察 `encoded`：  
   ```
   encoded[0] = perm[0] XOR perm[1]
   encoded[1] = perm[1] XOR perm[2]
   encoded[2] = perm[2] XOR perm[3]
   ...
   ```
   若把 **奇数下标**（1、3、5…）的 `encoded` 全部再异或，得到 `oddXor`：

   ```
   oddXor = encoded[1] XOR encoded[3] XOR encoded[5] ...
   ```

   这相当于把 `perm[1]、perm[2]、perm[3]…` 中 **除第一个以外的所有奇数位置** 的数全部消掉，只剩下 **`perm[1] XOR perm[3] XOR perm[5] …`**。

3. **推出 `perm[0]`**  
   因为 `n` 为奇数，**`total` 包含了所有 1~n**，而 `oddXor` 正好缺少 `perm[0]`（因为 `perm[0]` 没出现在奇数下标的异或里）。  
   所以：

   ```
   perm[0] = total XOR oddXor
   ```

   用一句话解释：把所有数字的总密码 `total` 再和“奇数位密码” `oddXor` 异或，就把 `perm[0]` “挑”出来了。

4. **其余元素顺序恢复**  
   有了 `perm[0]`，后面的元素就可以像暴力解那样逐个算：

   ```
   perm[i] = perm[i-1] XOR encoded[i-1]      (i ≥ 1)
   ```

#### 代码（Python）

```python
from typing import List

def decode(encoded: List[int]) -> List[int]:
    n = len(encoded) + 1                     # 原数组长度

    # 1. 计算 1~n 的全部异或，记作 total
    total = 0
    for i in range(1, n + 1):
        total ^= i

    # 2. 计算 encoded 中奇数下标（1、3、5…）的异或，记作 oddXor
    oddXor = 0
    # 注意：下标从 0 开始，奇数下标对应 i = 1,3,5,...
    for i in range(1, len(encoded), 2):
        oddXor ^= encoded[i]

    # 3. 推出 perm[0]
    perm0 = total ^ oddXor

    # 4. 依次恢复整个 perm
    perm = [perm0]
    for i in range(len(encoded)):
        # perm[i+1] = perm[i] XOR encoded[i]
        perm.append(perm[i] ^ encoded[i])

    return perm
```

*关键行中文注释*  
- `total ^= i`: 把 1~n 的所有数异或，得到“全局密码”。  
- `for i in range(1, len(encoded), 2)`: 只遍历奇数下标的 `encoded`，累积成 `oddXor`。  
- `perm0 = total ^ oddXor`: 把两段“密码”异或，直接得到第一个元素。  
- `perm.append(perm[i] ^ encoded[i])`: 与暴力解相同的恢复步骤。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历了三遍数组（一次算 `total`，一次算 `oddXor`，一次恢复 `perm`），每遍都是线性时间。  
  - 与暴力解相比，从 **“平方级”** 降到了 **“线性级”**，即使 n 达到 10⁵ 也能在毫秒级完成。  

- **空间复杂度**：`O(n)`  
  - 需要保存结果数组 `perm`，大小为 `n`。  
  - 其余变量都是常数级别的额外空间。  

---

## 心得  

- **核心技巧**：利用 XOR 的可逆性与**全局异或**消除多余信息。  
- **适用的题型**：  
  1. “找出缺失的数字 / 重复的数字” 系列（如 LeetCode 268、442）。  
  2. “通过相邻异或恢复原序列” 类题（如本题、LeetCode 1734 “Decode XORed Array”）。  
- **一句话总结解题钥匙**：**先把所有元素的 XOR 取出来，再用已知的局部 XOR 把目标元素“剔除”出来**。

---

## 反思  

- **第一反应**：先把 `perm[0]` 暴力枚举，然后逐个恢复。虽然能跑通，但明显不够高效。  
- **最容易踩的坑**：  
  - 忘记 `n` 必须是奇数，否则 `oddXor` 的推导不成立。  
  - 索引错误：`encoded` 的奇数下标在 Python 中是 `1,3,5,...`，要注意 `range(1, len(encoded), 2)`。  
  - 对 XOR 运算的性质不熟悉，容易误以为 `a XOR a = a`（其实是 `0`）。  
- **下次遇到同类题**：第一步先思考 **“能否通过全局 XOR 把某个位置的值单独挑出来？”**，如果可以，就直接算出该位置的值，再用线性方式恢复其余部分。