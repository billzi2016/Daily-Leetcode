# #1073. 两个负二进制数相加 / Adding Two Negabinary Numbers

> 难度：中等 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/adding-two-negabinary-numbers/)

---

## 题目（英文原版）

**Description**

Given two numbers arr1 and arr2 in base -2, return the result of adding them together.
Each number is given in array format:  as an array of 0s and 1s, from most significant bit to least significant bit.  For example, arr = [1,1,0,1] represents the number (-2)^3 + (-2)^2 + (-2)^0 = -3.  A number arr in array, format is also guaranteed to have no leading zeros: either arr == [0] or arr[0] == 1.
Return the result of adding arr1 and arr2 in the same format: as an array of 0s and 1s with no leading zeros.

**Examples**

**Example 1:**

```
Input: arr1 = [1,1,1,1,1], arr2 = [1,0,1]
Output: [1,0,0,0,0]
Explanation: arr1 represents 11, arr2 represents 5, the output represents 16.
```

**Example 2:**

```
Input: arr1 = [0], arr2 = [0]
Output: [0]
```

**Example 3:**

```
Input: arr1 = [0], arr2 = [1]
Output: [1]
```

**Constraints**

- 1 <= arr1.length, arr2.length <= 1000
- arr1[i] and arr2[i] are 0 or 1
- arr1 and arr2 have no leading zeros

---

## 题目（中文翻译）

给定两个负二进制（negabinary）数 `arr1` 和 `arr2`，返回它们相加的结果。  
每个数以 **数组形式（array format）** 给出：由 `0` 和 `1` 组成的数组，按从最高有效位到最低有效位的顺序存放。例如，`arr = [1,1,0,1]` 表示的数为  

\[
(-2)^3 + (-2)^2 + (-2)^0 = -3
\]

数组形式的数保证 **没有前导零**：要么 `arr == [0]`，要么 `arr[0] == 1`。

请返回 `arr1` 与 `arr2` 相加后的结果，仍然使用 **数组形式（array format）**，且 **不含前导零**。

## 示例

### 示例 1
**输入**  
`arr1 = [1,1,1,1,1]`, `arr2 = [1,0,1]`  

**输出**  
`[1,0,0,0,0]`  

**解释**  
`arr1` 表示十进制数 `11`，`arr2` 表示十进制数 `5`，输出数组表示十进制数 `16`。

### 示例 2
**输入**  
`arr1 = [0]`, `arr2 = [0]`  

**输出**  
`[0]`

### 示例 3
**输入**  
`arr1 = [0]`, `arr2 = [1]`  

**输出**  
`[1]`

## 约束条件

- `1 <= arr1.length, arr2.length <= 1000`
- `arr1[i]` 和 `arr2[i]` 只能是 `0` 或 `1`
- `arr1` 与 `arr2` 均不存在前导零（即要么为 `[0]`，要么首位为 `1`）

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把「负二进制」先变回我们熟悉的十进制整数，做普通的加法，再把结果重新转换成负二进制。  

- **把负二进制转成十进制**：把数组看成一串「位」，从左到右依次乘以 `(-2) 的相应幂次` 再相加。  
  - 类比查字典：字典的 `key` 是「位的位置」，`value` 是「0 或 1」的数值，`key` 对应的「页码」就是 `(-2)^位置`。  
- **十进制相加**：Python 的整数可以直接相加，没什么难度。  
- **十进制转回负二进制**：使用除 `-2` 取余的方式。  
  - 取余的结果必须是 0 或 1（因为负二进制的每位只能是 0/1），如果余数是负数，就把余数加上 2（变成正的 0/1），并把商 `+1` 来补偿。  

这样得到的答案自然没有前导零（除了唯一的 `[0]`），因为最高位一定是 1（除非答案本身是 0）。

> **为什么正确？**  
> 负二进制的定义保证了每一位的权值是 `(-2)^i`，所以把每位乘以对应的权值相加得到的整数一定等于原数组表示的数。相反，除 `-2` 取余的过程正是把整数用 `(-2)` 进制展开的逆过程。  

> **时间/空间复杂度大白话**：  
> - `O(n + m)`：把两个数组各遍历一次（`n`、`m` 是它们的长度），再把和转换一次，整体就是几次线性遍历。  
> - `O(1)` 额外空间：只用常数个变量保存中间结果（返回的数组不算在额外空间里）。

#### 代码（Python）

```python
def to_int(arr):
    """把负二进制数组转成十进制整数"""
    val = 0
    for bit in arr:                 # 从最高位到最低位遍历
        val = val * (-2) + bit      # 乘以 (-2) 再加当前位
    return val

def from_int(num):
    """把十进制整数转成负二进制数组（不含前导零）"""
    if num == 0:
        return [0]
    bits = []
    while num != 0:
        # Python 的 divmod 对负数的余数是负的，需要手动调整
        num, rem = divmod(num, -2)   # 先除 -2，得到商和余数
        if rem < 0:                  # 余数如果是 -1，就把它变成 1
            num += 1                 # 商加 1 来补偿
            rem += 2                 # 余数加 2 变成正的 0/1
        bits.append(rem)             # 余数就是当前位（0 或 1）
    return bits[::-1]                # 逆序得到从高位到低位的数组

def addNegabinary(arr1, arr2):
    """暴力解：先转十进制再相加，最后转回负二进制"""
    a = to_int(arr1)
    b = to_int(arr2)
    s = a + b
    return from_int(s)

# 示例
print(addNegabinary([1,1,1,1,1], [1,0,1]))   # -> [1,0,0,0,0]
print(addNegabinary([0], [0]))               # -> [0]
print(addNegabinary([0], [1]))               # -> [1]
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 解释：我们分别遍历 `arr1`（`n`）和 `arr2`（`m`）各一次，再把和转换为负二进制，最多需要 `O(log|sum|)` 次循环。整体仍是线性级别。  

- **空间复杂度**：`O(1)`（不计返回值）  
  - 解释：只用了几个整数变量 `val、num、rem、carry`，占用的空间不随输入规模增长。  

---  

### 2. 最优解  

#### 思路  

暴力解的「瓶颈」在于把负二进制先变成十进制，再变回来。虽然时间已经是线性的，但我们可以直接在 **负二进制位上** 完成加法，省掉「转整数」这一步，代码更简洁、也更符合「进制运算」的本质。  

**关键点**：在负二进制里，每一位的权值是 `(-2)^i`，所以「进位」的方向和普通二进制不一样。  

1. **把数组倒过来**（从低位到高位）方便顺序相加。  
2. **维护一个进位 `carry`**，它的取值可以是 `-1、0、1、2`（因为 `0/1 + 0/1 + carry` 最多是 `1+1+2 = 4`）。  
3. **当前位的总和** `total = a_i + b_i + carry`。  
4. **结果位** `res_bit = total & 1`（即 `total % 2`，只保留 0/1）。  
5. **新进位** 需要满足 `total = res_bit + (-2) * new_carry`，于是  
   `new_carry = (total - res_bit) // -2`。  
   这一步可以直接写成 `carry = -(total // 2)`，但为了易懂我们用上面的等式。  

循环结束后，如果还有非零的 `carry`，继续处理，直到 `carry` 为 0。最后把结果翻转回「高位在前」的形式，并去掉可能出现的前导零。  

> **类比**：想象普通二进制加法是「把水往左边的杯子倒」，而负二进制是「把水往右边的杯子倒」——进位的方向相反，需要「往左倒」的负数来平衡。  

> **为什么快**：我们只遍历一次最长的数组长度，所有运算都是常数时间的整数加减，完全没有额外的「转整数」步骤。  

#### 代码（Python）

```python
def addNegabinary(arr1, arr2):
    """最优解：直接在负二进制位上完成加法"""
    # 1. 先把高位在前的数组倒过来，方便从低位开始处理
    a = arr1[::-1]
    b = arr2[::-1]
    n = max(len(a), len(b))
    carry = 0                # 初始进位为 0
    res = []                 # 用来存放结果的低位到高位

    for i in range(n):
        # 取出当前位（如果已经越界则视为 0）
        ai = a[i] if i < len(a) else 0
        bi = b[i] if i < len(b) else 0

        total = ai + bi + carry          # 当前位的总和
        bit = total & 1                  # 只保留 0/1，等价于 total % 2
        res.append(bit)                  # 记录结果位（低位在前）

        # 根据等式 total = bit + (-2) * new_carry 求出新的进位
        carry = (total - bit) // -2      # 这里一定是整数除法

    # 处理完所有位后，仍可能有进位
    while carry != 0:
        total = carry
        bit = total & 1
        res.append(bit)
        carry = (total - bit) // -2

    # 结果现在是低位在前，需要翻转回高位在前
    res = res[::-1]

    # 去掉前导零（除非答案本身是 0）
    while len(res) > 1 and res[0] == 0:
        res.pop(0)

    return res

# 示例
print(addNegabinary([1,1,1,1,1], [1,0,1]))   # -> [1,0,0,0,0]
print(addNegabinary([0], [0]))               # -> [0]
print(addNegabinary([0], [1]))               # -> [1]
```

#### 复杂度  

- **时间复杂度**：`O(max(n, m))`  
  - 解释：我们只遍历最长的数组一次（`n`、`m` 分别是两数组长度），每一步做常数次整数运算。相比暴力解多了「倒序」和「进位」的常数操作，仍是线性时间。  

- **空间复杂度**：`O(max(n, m))`  
  - 解释：需要一个结果数组保存每一位，长度最多比最长输入多 2 位（极端进位），因此是线性空间。  

---

## 心得  

- **核心技巧**：在负二进制上直接模拟加法，关键是把「进位」的计算改成 `carry = (total - bit) // -2`（即向负方向进位）。  
- **适用场景**：  
  1. 所有涉及 **负进制**（如 `-2、-3` 等）的加减法题目。  
  2. 需要 **位运算** 思路的题目，例如「把二进制/三进制数加起来」的变种。  
  3. 需要 **自定义进位规则** 的进制转换题。  
- **一句话总结**：**把「进位」看成「向左除以 -2」的结果，就能像普通二进制一样逐位相加**。  

---

## 反思  

- **第一反应**：把负二进制先转成十进制再相加，思路最直观但有点「多此一举」。  
- **最容易踩的坑**：  
  - 负二进制的余数必须是 `0/1`，除 `-2` 时会出现负余数，需要手动调整。  
  - 进位可能为负数，写 `carry = total // -2` 会得到向下取整的结果，需要配合 `bit = total & 1` 再计算。  
  - 结果数组的前导零必须去掉，特别是当最高位产生了额外的 `1` 时。  
- **下次第一步**：**先把两数对齐（倒序）并思考「进位」在负基数下的计算公式**，直接在位上做加法，而不是先转成十进制。