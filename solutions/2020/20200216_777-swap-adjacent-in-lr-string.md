# #777. 相邻字符交换（LR 字符串） / Swap Adjacent in LR String

> 难度：中等 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/swap-adjacent-in-lr-string/)

---

## 题目（英文原版）

**Description**

In a string composed of 'L', 'R', and 'X' characters, like "RXXLRXRXL", a move consists of either replacing one occurrence of "XL" with "LX", or replacing one occurrence of "RX" with "XR". Given the starting string start and the ending string result, return True if and only if there exists a sequence of moves to transform start to result.

**Examples**

**Example 1:**

```
Input: start = "RXXLRXRXL", result = "XRLXXRRLX"
Output: true
Explanation: We can transform start to result following these steps:
RXXLRXRXL ->
XRXLRXRXL ->
XRLXRXRXL ->
XRLXXRRXL ->
XRLXXRRLX
```

**Example 2:**

```
Input: start = "X", result = "L"
Output: false
```

**Constraints**

- 1 <= start.length <= 104
- start.length == result.length
- Both start and result will only consist of characters in 'L', 'R', and 'X'.

---

## 题目（中文翻译）

在仅由字符 `'L'`、`'R'` 和 `'X'` 组成的字符串中（例如 `"RXXLRXRXL"`），**一次移动（move）**可以是以下两种操作之一：

- 用 `"LX"` 替换出现的子串 `"XL"`；
- 用 `"XR"` 替换出现的子串 `"RX"`。

给定初始字符串 `start` 与目标字符串 `result`，如果且仅如果存在一系列合法的移动，使得 `start` 能够转化为 `result`，则返回 `True`。

#### 示例

**示例 1**

```
Input: start = "RXXLRXRXL", result = "XRLXXRRLX"
Output: true
Explanation: 可以按以下步骤将 start 转换为 result：
RXXLRXRXL ->
XRXLRXRXL ->
XRLXRXRXL ->
XRLXXRRXL ->
XRLXXRRLX
```

**示例 2**

```
Input: start = "X", result = "L"
Output: false
```

#### 约束条件

- $1 \leq \text{start.length} \leq 10^4$
- $\text{start.length} = \text{result.length}$
- `start` 与 `result` 均仅由字符 `'L'`、`'R'` 和 `'X'` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**模拟每一步的合法移动**，一直尝试把 `start` 变成 `result`。  
- **数据结构**：我们只需要把字符串当成字符数组（列表）来操作，类似把一排座位上的人往左或往右挪动。  
- **合法移动**：  
  - `"XL"` → `"LX"`：把左边的空位 `X` 和右边的 `L` 交换，等价于让 `L` 向左走一步。  
  - `"RX"` → `"XR"`：把左边的 `R` 和右边的空位 `X` 交换，等价于让 `R` 向右走一步。  
- **暴力做法**：遍历整条字符串，凡是出现 `"XL"` 或 `"RX"` 就立即交换，然后把新的字符串继续遍历，直到再也找不到可以交换的地方为止。最后比较得到的字符串是否等于 `result`。

> **为什么这个方法正确？**  
> 每一次交换都严格遵守题目给出的两种合法操作。因此，只要我们能把 `start` 经过若干次合法交换变成 `result`，最终的比较一定会返回 `True`。反之，如果我们把所有可能的合法交换都做完仍然得不到 `result`，说明根本不存在这样的一系列操作。

> **时间/空间复杂度的大白话**  
> - 时间复杂度 `O(n²)`：想象有 `n` 张座位，如果每次都要从头到尾扫描一次（`O(n)`），而最坏情况下我们可能需要 `O(n)` 次扫描才能把所有字符都移动到位（比如 `R` 要向右移动 `n` 步），于是总工作量是 `n` × `n`，这就是 `O(n²)`。  
> - 空间复杂度 `O(1)`：我们只在原字符串上原地交换，不需要额外的数组或哈希表，使用的额外空间是常数级的。

#### 代码（Python）

```python
def can_transform_bruteforce(start: str, result: str) -> bool:
    # 把字符串转成列表，列表支持原地交换，效率比直接操作字符串高
    s = list(start)
    n = len(s)

    # 只要在一次遍历中还有可以交换的地方，就继续循环
    while True:
        changed = False                     # 本轮是否有任何一次交换
        i = 0
        while i < n - 1:                    # 检查相邻的两个字符
            # "XL" → "LX" 让 L 往左走
            if s[i] == 'X' and s[i + 1] == 'L':
                s[i], s[i + 1] = 'L', 'X'   # 交换
                changed = True
                i += 2                      # 已经处理了 i,i+1，跳过它们
                continue
            # "RX" → "XR" 让 R 往右走
            if s[i] == 'R' and s[i + 1] == 'X':
                s[i], s[i + 1] = 'X', 'R'   # 交换
                changed = True
                i += 2
                continue
            i += 1                          # 当前位置不匹配，继续向右

        if not changed:                     # 本轮没有任何交换，说明已经稳定
            break

    return ''.join(s) == result
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：最坏情况下每一次循环只能让一个字符前进一步，需要 `n` 次循环，每次循环遍历 `n` 个字符，总共约 `n × n` 次比较/交换。  
- **空间复杂度**：`O(1)`（不计输入字符串本身）  
  - 解释：只使用了常数个临时变量和原地交换，额外占用的内存不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每次只移动一步”**，导致大量重复遍历。  
我们可以从 **“整体视角”** 来思考：  

1. **字符种类不变**  
   - `L`、`R` 的相对顺序在任何合法移动后都保持不变（因为 `L` 只能左移、`R` 只能右移，二者不会相互穿越）。  
   - 因此，如果把所有 `X` 删除，只剩下 `L` 与 `R`，这两个压缩后的字符串必须相同。  

2. **相对位置约束**  
   - `L` 只能向左移动，意味着在 `start` 中对应的 `L` **不能出现在** `result` 中更右的位置。  
   - 同理，`R` 只能向右移动，意味着在 `start` 中对应的 `R` **不能出现在** `result` 中更左的位置。  

3. **双指针扫描**  
   - 使用两个指针 `i`、`j` 分别遍历 `start` 与 `result`，跳过所有的 `X`，只对齐真正的 `L`/`R`。  
   - 当同时指向非 `X` 时，比较字符是否相同以及位置是否满足上面的约束。若不满足，直接返回 `False`。  
   - 当遍历结束后，若两串的非 `X` 部分全部匹配且约束都满足，则一定可以通过一系列合法交换完成转化。  

> **核心数据结构**：**双指针**（Two Pointers）。  
> - 把指针想象成两个人在两条平行的跑道上跑，只有当两人都站在“人”（`L` 或 `R`）上时才需要比较，否则就继续往前跑，跳过空位（`X`）。  

#### 代码（Python）

```python
def can_transform(start: str, result: str) -> bool:
    n = len(start)
    i = j = 0                       # i 指向 start，j 指向 result

    while i < n or j < n:
        # 跳过 start 中的 'X'
        while i < n and start[i] == 'X':
            i += 1
        # 跳过 result 中的 'X'
        while j < n and result[j] == 'X':
            j += 1

        # 同时遍历结束，说明后面全是 X，合法
        if i == n and j == n:
            return True
        # 只有一方提前结束，说明字符数量不匹配
        if (i == n) != (j == n):
            return False

        # 此时 start[i] 和 result[j] 都是 'L' 或 'R'
        if start[i] != result[j]:
            return False               # 不同种类的字符根本无法对应

        # 位置约束检查
        if start[i] == 'L' and i < j:
            # L 只能左移，不能从左边跑到更右边
            return False
        if start[i] == 'R' and i > j:
            # R 只能右移，不能从右边跑到更左边
            return False

        # 对齐成功，继续向后检查
        i += 1
        j += 1

    return True
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 解释：每个指针只会向前移动最多 `n` 步，整个过程只遍历两遍字符串，和 `n` 成线性关系。相比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(1)`  
  - 解释：只用了若干整数指针和常量级的临时变量，额外空间不随输入规模增长。

---

## 心得

- **核心技巧**：**双指针配合位置约束**，通过一次线性扫描判断是否满足“只能左移的 L 与只能右移的 R”这两条不交叉的规则。  
- **适用的题型**：  
  1. **“只允许特定方向移动的字符换位”**，如 *Swap Adjacent in LR String*。  
  2. **“删除某类字符后，两串必须相同”**，例如 *Validate Stack Sequences* 的变体。  
  3. **“两串相对顺序必须保持不变”**，如 *Isomorphic Strings*（只不过那是映射关系）。  
- **一句话总结解题钥匙**：**“先把无关的 X 跳过去，只比较 L/R 本身并检查它们是否违反只能左/右移动的规则”。**

---

## 反思

- **第一反应**：直接去**模拟每一步交换**，把题目描述的操作写成循环，想要把 `start` 真的一步步变成 `result`。  
- **最容易踩的坑**：  
  - 忽视了 `L` 只能左移、`R` 只能右移的方向限制，导致写出可以让 `R` 向左或 `L` 向右的错误实现。  
  - 没有先检查两串去掉 `X` 后的字符序列是否相同，直接比较位置会产生假阳性。  
  - 边界情况：全是 `X`，或者只有一种字符（全是 `L` 或全是 `R）时的处理。  
- **下次遇到同类题**：第一步先**把所有 “无关” 的占位符（这里是 `X`）跳过，只关注真正需要比较的字符，并思考这些字符是否有**移动方向的单调性**，再决定使用双指针或前缀和等线性技巧。