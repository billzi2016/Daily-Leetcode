# #1720. 解码异或数组 / Decode XORed Array

> 难度：简单 · 标签：Array、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/decode-xored-array/)

---

## 题目（英文原版）

**Description**

There is a hidden integer array arr that consists of n non-negative integers.
It was encoded into another integer array encoded of length n - 1, such that encoded[i] = arr[i] XOR arr[i + 1]. For example, if arr = [1,0,2,1], then encoded = [1,2,3].
You are given the encoded array. You are also given an integer first, that is the first element of arr, i.e. arr[0].
Return the original array arr. It can be proved that the answer exists and is unique.

**Examples**

**Example 1:**

```
Input: encoded = [1,2,3], first = 1
Output: [1,0,2,1]
Explanation: If arr = [1,0,2,1], then first = 1 and encoded = [1 XOR 0, 0 XOR 2, 2 XOR 1] = [1,2,3]
```

**Example 2:**

```
Input: encoded = [6,2,7,3], first = 4
Output: [4,2,0,7,4]
```

**Constraints**

- 2 <= n <= 104
- encoded.length == n - 1
- 0 <= encoded[i] <= 105
- 0 <= first <= 105

---

## 题目（中文翻译）

有一个隐藏的整数数组 **arr**，其中包含 **n** 个非负整数（non‑negative integers）。  
它被编码成另一个整数数组 **encoded**，长度为 **n - 1**，满足  

```
encoded[i] = arr[i] XOR arr[i + 1]
```  

例如，若 `arr = [1,0,2,1]`，则 `encoded = [1,2,3]`。

现在给定 **encoded** 数组，以及整数 **first**，它就是 **arr** 的第一个元素（即 `arr[0]`）。  
请返回原始数组 **arr**。可以证明答案必定存在且唯一。

**示例 1**  
**输入**: `encoded = [1,2,3]`, `first = 1`  
**输出**: `[1,0,2,1]`  
**解释**: 若 `arr = [1,0,2,1]`，则 `first = 1`，且  

```
encoded = [1 XOR 0, 0 XOR 2, 2 XOR 1] = [1,2,3]
```

**示例 2**  
**输入**: `encoded = [6,2,7,3]`, `first = 4`  
**输出**: `[4,2,0,7,4]`

**约束条件**

- `2 <= n <= 10^4`
- `encoded.length == n - 1`
- `0 <= encoded[i] <= 10^5`
- `0 <= first <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目已经把 **encoded[i] = arr[i] XOR arr[i+1]** 给出来了，只要把等式两边同时 “异或” 同一个数，就可以把未知的 `arr[i+1]` 解出来：

```
arr[i+1] = encoded[i] XOR arr[i]
```

> **类比**：把 `XOR` 想成“密码锁”。如果你知道锁的密码 `arr[i]`，以及两把钥匙 `encoded[i]`（其实是 `arr[i]` 与 `arr[i+1]` 的异或），只要再把钥匙和已知密码一起再拧一次（再 XOR），就能得到另一把钥匙 `arr[i+1]`。

因为题目已经告诉我们 `arr[0] = first`，于是我们可以从左到右一次算出所有元素，整个过程只需要一次遍历。

- **为什么正确**：  
  对任意 `i`，已知 `encoded[i] = arr[i] XOR arr[i+1]`，把等式两边同时 XOR `arr[i]`，利用 XOR 的交换律和结合律以及 `a XOR a = 0`、`a XOR 0 = a`，得到 `arr[i+1] = encoded[i] XOR arr[i]`。只要前一个元素已知，就能唯一确定后一个元素。

- **时间/空间复杂度**：  
  我们只遍历一次长度为 `n‑1` 的 `encoded`，每一步做常数次的 XOR 运算，时间复杂度是 **O(n)**（线性时间）。  
  需要额外保存结果数组 `arr`，大小为 `n`，空间复杂度是 **O(n)**（线性空间）。

#### 代码（Python）

```python
def decode(encoded, first):
    """
    :param encoded: List[int]，长度为 n-1 的编码数组
    :param first:   int，原数组的第一个元素 arr[0]
    :return:        List[int]，还原后的原数组 arr
    """
    n = len(encoded) + 1               # 原数组长度
    arr = [0] * n                       # 先开辟好空间
    arr[0] = first                      # 已知的第一个元素

    # 从左到右依次推导后面的元素
    for i in range(len(encoded)):
        # arr[i+1] = encoded[i] XOR arr[i]
        arr[i + 1] = encoded[i] ^ arr[i]   # ^ 是 Python 中的 XOR 运算符
    return arr
```

#### 复杂度

- **时间复杂度**：`O(n)` — 线性遍历一次，`n` 为原数组长度。可以把它想成“走一遍排队的队伍”，每个人只看一眼。
- **空间复杂度**：`O(n)` — 需要存放结果数组 `arr`，相当于“准备好一个同样大小的盒子装所有答案”。  

---

### 2. 最优解

#### 思路  

实际上，上面的“直觉解”已经是 **最优** 的做法，因为我们只能通过 `encoded` 与已知的前一个元素来一步步推出下一个元素，无法再进一步压缩时间或空间。下面把思路再整理得更清晰，帮助你在以后遇到类似 “相邻关系已知” 的题目时快速定位解法。

1. **找到瓶颈**：  
   - 只有 `encoded[i] = arr[i] XOR arr[i+1]` 这条信息。  
   - 只要知道 `arr[i]`，就能唯一算出 `arr[i+1]`，没有多余的搜索或枚举空间。  
   - 因此 **不需要** 暴力枚举所有可能的 `arr`（那会是指数级），只要线性遍历即可。

2. **核心技巧 – XOR 的可逆性**：  
   - XOR 有两个重要性质：  
     1. `a XOR a = 0`（相同的数异或得到 0）  
     2. `a XOR 0 = a`（和 0 异或不改变）  
   - 更关键的是 **“异或可以抵消”**：`(a XOR b) XOR a = b`。这正好把我们从 `encoded[i]` 与 `arr[i]` 推到 `arr[i+1]`。

3. **一步步实现**：  
   - 初始化 `arr[0] = first`（已知）。  
   - 对每个 `i`（从 0 到 n‑2），计算 `arr[i+1] = encoded[i] XOR arr[i]`。  
   - 把得到的 `arr[i+1]` 放进结果数组，继续向后。

> **图示文字**（帮助想象）  
> ```
> arr[i] ──XOR── encoded[i] ──XOR── arr[i] = arr[i+1]
>   ↑                               ↑
>  已知                         通过前一步得到
> ```

#### 代码（Python）

```python
def decode(encoded, first):
    n = len(encoded) + 1
    arr = [first]                     # 直接把第一个元素放进去，后面会逐个 append
    for num in encoded:               # 依次遍历 encoded 中的每个数
        # 上一步得到的 arr[-1] 就是当前的 arr[i]
        next_val = arr[-1] ^ num      # XOR 把前一个元素和当前的 encoded 结合，得到下一个元素
        arr.append(next_val)          # 把新算出的元素加入结果
    return arr
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次 `encoded`，每次做一次 XOR，和直觉解的时间一样快。  
- **空间复杂度**：`O(n)` — 结果数组 `arr` 必须返回，额外空间没有其它开销。

---

## 心得

- **核心技巧**：XOR 的可逆性（`a XOR b XOR a = b`），相当于“密码锁的钥匙可以相互抵消”。  
- **适用的题型**：  
  1. “相邻元素异或/加/减得到新数组”，如 **Decode XORed Array**（本题）。  
  2. “给出两数之和的 XOR，求原始两个数”，如 LeetCode 1720. 解码异或密码。  
  3. “翻转位运算求原始数组”，比如 **Find the Original Array of a Permutation**（涉及 XOR 与位运算的逆向推导）。  
- **一句话总结**：只要能把“已知 = 前一个 XOR 当前”拆解成 “当前 = 已知 XOR 前一个”，就能线性恢复整个序列。

## 反思

- **第一反应**：看到 `encoded[i] = arr[i] XOR arr[i+1]`，立刻想到 “XOR 可以消掉”，于是写出 `arr[i+1] = encoded[i] XOR arr[i]`。  
- **最容易踩的坑**：  
  - 忘记把 `first` 放进结果的第一个位置，导致后续下标错位。  
  - 误把 `encoded[i]` 与 `arr[i+1]` 直接相加或相减，而不是使用 XOR。  
  - 边界条件：当 `encoded` 为空（理论上不可能，因为 n≥2），要确保代码仍然能返回 `[first]`。  
- **下次类似题的第一步**：先写出关系式 `known = a XOR b`，然后两边同 XOR 一个已知量，得到 `未知 = known XOR 已知`，再用循环逐步恢复。