# #3307. 在字符串游戏 II 中查找第 K 个字符 / Find the K-th Character in String Game II

> 难度：困难 · 标签：Math、Bit Manipulation、Recursion · [LeetCode 链接](https://leetcode.com/problems/find-the-k-th-character-in-string-game-ii/)

---

## 题目（英文原版）

**Description**

Alice and Bob are playing a game. Initially, Alice has a string word = "a".
You are given a positive integer k. You are also given an integer array operations, where operations[i] represents the type of the ith operation.
Now Bob will ask Alice to perform all operations in sequence:
Return the value of the kth character in word after performing all the operations.
Note that the character 'z' can be changed to 'a' in the second type of operation.

**Examples**

**Example 1:**

```
Input: k = 5, operations = [0,0,0]
Output: "a"
Explanation:
Initially, word == "a" . Alice performs the three operations as follows:
```

**Example 2:**

```
Input: k = 10, operations = [0,1,0,1]
Output: "b"
Explanation:
Initially, word == "a" . Alice performs the four operations as follows:
```

**Constraints**

- 1 <= k <= 1014
- 1 <= operations.length <= 100
- operations[i] is either 0 or 1.
- The input is generated such that word has at least k characters after all operations.

---

## 题目（中文翻译）

Alice 和 Bob 正在玩一个游戏。最初，Alice 拥有字符串 `word = "a"`。  
给定一个正整数 `k`，以及整数数组 `operations`，其中 `operations[i]` 表示第 `i` 次操作的类型。  
现在 Bob 会依次让 Alice 执行所有操作：  

返回执行完所有操作后，`word` 中第 `k` 个字符的值。  
需要注意，在第二种类型的操作中，字符 `'z'` 可以循环变为 `'a'`（即 `'z'` → `'a'`）。

### 示例 1
**输入**: `k = 5`, `operations = [0,0,0]`  
**输出**: `"a"`  
**解释**:  
最初，`word == "a"`。Alice 按顺序执行这三个操作，过程如下：

（此处省略具体操作过程，保持原题结构）

### 示例 2
**输入**: `k = 10`, `operations = [0,1,0,1]`  
**输出**: `"b"`  
**解释**:  
最初，`word == "a"`。Alice 按顺序执行这四个操作，过程如下：

（此处省略具体操作过程，保持原题结构）

### 约束条件
- `1 <= k <= 10^14`
- `1 <= operations.length <= 100`
- `operations[i]` 只能为 `0` 或 `1`
- 输入保证在所有操作执行完毕后，`word` 的长度至少为 `k` 字符

---

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**一步一步真的把字符串拼出来**，然后直接取第 `k` 个字符。  
- 初始 `word = "a"`。  
- 对于每一次操作  
  - `op = 0`：把当前字符串复制一次并接在后面 → `word = word + word`。  
  - `op = 1`：把当前字符串的每个字符都往后搬一位（`'a'→'b'`，…，`'z'→'a'`），再接在后面 → `word = word + shift(word)`。  

这里的 `shift` 可以想象成 **查字典**：把字母当成词，字典里存的是“后一个字母”。  

只要把所有操作都执行完，整个 `word` 就会很长（长度是 `2^m`，`m = len(operations)`），直接返回 `word[k‑1]` 即可。  

**为什么正确**：我们严格按照题目描述构造了最终的字符串，显然第 `k` 个字符就是答案。  

**复杂度分析（大白话）**  
- 每执行一次操作，字符串长度会 **翻倍**。如果有 `m` 次操作，最终长度是 `2^m`，而我们在最坏情况下会把整个字符串都保存下来。  
- 时间复杂度：我们要遍历所有字符一次，等价于 **O(2^m)**。  
- 空间复杂度：同样要把整条字符串放进内存，也要 **O(2^m)**。  

当 `m` 只有几次（比如 5、6）时还能接受，但题目里 `m` 最多 100，`2^100` 远远超过电脑能存的容量，暴力方法根本不可行。  

#### 代码（Python）  

```python
def shift_char(c: str) -> str:
    """把字符往后搬一位，'z' → 'a'"""
    return chr((ord(c) - ord('a') + 1) % 26 + ord('a'))

def kth_character_bruteforce(k: int, operations: list[int]) -> str:
    word = ['a']                     # 用列表方便拼接
    for op in operations:
        if op == 0:                  # word = word + word
            word = word + word
        else:                        # word = word + shift(word)
            shifted = [shift_char(ch) for ch in word]
            word = word + shifted
        # 如果已经够长，直接可以停止（仅为演示方便）
        if len(word) >= k:
            break
    return word[k - 1]               # Python 索引从 0 开始
```

> **注释**  
> - 第 2 行的 `shift_char` 把字母转成它的“后继”。这里把字母当成 **字典** 的 key，返回对应的 value。  
> - 第 7‑13 行实现了两种拼接方式。  
> - 第 15‑16 行提前判断长度是否已经 ≥ `k`，可以省掉后面的无用拼接（仅在小数据里有用）。

#### 复杂度  

- **时间复杂度**：`O(2^m)`（每次操作把长度翻倍，最终遍历所有字符）。  
- **空间复杂度**：`O(2^m)`（要把整条字符串保存下来）。  

> **含义解释**：`2^m` 代表“指数级增长”，当 `m = 100` 时，`2^100 ≈ 1.27×10³⁰`，远远大于任何计算机的内存容量，所以暴力解只能用于**教学演示**或极小的输入。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**真正需要的并不是整条字符串**，我们只关心第 `k` 个字符到底来自哪一次“复制”或“搬位”。  

**瓶颈**：暴力解把所有字符都搬进内存，导致指数级时间和空间。  
**关键观察**：每一次操作都把旧字符串 **复制两份**（不论是原样复制还是搬位复制），所以新字符串的**左半边**和**右半边**长度相等，都是旧字符串的长度。  

这意味着：  

- 如果我们想知道第 `k` 位在 **第 i 步** 的结果，只需要看它位于左半边还是右半边。  
- **左半边**直接等于第 `i‑1` 步的第 `k` 位。  
- **右半边**  
  - `op = 0` 时，同样等于第 `i‑1` 步的第 `k‑len_{i‑1}` 位。  
  - `op = 1` 时，则是第 `i‑1` 步的相同位置字符 **再搬位一次**（即字母往后 +1，`z` → `a`）。  

这里的 **`len_{i‑1}` = 2^{i‑1}`**，因为每一步长度都翻倍。  

所以我们可以**从最后一步倒着追溯**：  
1. 记录一个累计的“搬位次数” `shift_cnt`（初始为 0）。  
2. 从最后一个操作往前看：  
   - 计算当前步的 **半长** `half = 2^{i}`（因为 i 从 0 开始，i 步之后长度是 `2^{i+1}`，所以半长是 `2^{i}`）。  
   - 若 `k > half`，说明目标字符在右半边，  
     - 把 `k` 减去 `half`，映射到前一步的对应位置。  
     - 如果这一步的操作是 `1`，说明在右半边时我们额外搬位一次，于是 `shift_cnt += 1`（模 26）。  
   - 否则（`k ≤ half`）它在左半边，直接进入前一步，不改变 `shift_cnt`。  
3. 最终会把 `k` 追溯到最初的字符 `'a'`。答案就是把 `'a'` 搬位 `shift_cnt` 次得到的字符。  

**为什么只看左半边**：因为右半边的字符**全部来源于左半边**（只是在 `op=1` 时多搬位），所以只要把右半边映射回左半边，就能一直往前追溯到最初的 `'a'`。  

**核心数据结构**：只用到 **整数**（记录 `k`、`half`、`shift_cnt`），不需要任何额外的容器。  

**类比**：把整个过程想象成一棵 **满二叉树**，根节点是 `'a'`，每层对应一次操作。我们从树的叶子（第 `k` 位）往上走，遇到右子树就记一次“向右搬位”。  

#### 代码（Python）  

```python
def kth_character(k: int, operations: list[int]) -> str:
    """
    返回在完成所有 operations 之后，第 k 位字符（1-indexed）。
    思路：从后往前把 k 映射到前一步，同时累计搬位次数。
    """
    shift_cnt = 0                 # 累计向后搬位的次数（模 26）
    n = len(operations)           # 操作总数

    # 从最后一步倒着处理
    for i in range(n - 1, -1, -1):
        half = 1 << i              # 2**i，当前步的左半边长度
        if k > half:               # 落在右半边
            k -= half              # 映射到前一步的对应位置
            if operations[i] == 1:   # 右半边是 shift(word)
                shift_cnt = (shift_cnt + 1) % 26   # 记录一次搬位
        # 若 k <= half，则在左半边，直接进入前一步，不需要额外操作

    # 最终 k 必然是 1，对应最初的字符 'a'
    base = ord('a')
    ans_char = chr((base - base + shift_cnt) % 26 + base)  # 'a' 搬位 shift_cnt 次
    return ans_char
```

> **关键行解释**  
> - `half = 1 << i`：左移相当于 `2**i`，快速算出半长。  
> - `if k > half:`：判断是否在右半边。  
> - `shift_cnt = (shift_cnt + 1) % 26`：只在 `op=1` 且在右半边时才累计搬位，模 26 保证在 `'a'~'z'` 循环。  
> - 最后用 `chr` 把 `'a'` 搬位 `shift_cnt` 次得到答案。

#### 复杂度  

- **时间复杂度**：`O(m)`，其中 `m = len(operations) ≤ 100`。我们只遍历一次操作列表，**与 k 的大小无关**。  
- **空间复杂度**：`O(1)`，只用了常数个整数变量。  

> **含义解释**：相较于暴力的指数级 (`2^m`) 时间，线性 `m` 次遍历几乎可以在瞬间完成，即使 `k` 达到 `10^14` 也毫无压力。

---

## 心得  

- **核心技巧**：把“字符串复制 + 搬位”看成**二分结构**，利用**递归/迭代逆向映射**把目标位置一步步回溯到最初的字符。  
- **适用场景**（类似题）  
  1. **String Game I**（只有复制，不搬位），同样可以逆向定位字符。  
  2. **Folded String**、**Repeated Substring Queries**：通过二分或递归把查询映射到原始块。  
  3. **K-th Symbol in Grammar**（LeetCode 779），使用相同的“左半/右半”思路。  
- **一句话总结解题钥匙**：**“右半边的字符一定来源于左半边，只是多搬位一次” → 逆向追溯 + 计数搬位**。

---

## 反思  

- **第一反应**：直接把字符串拼出来，想要“看得见”答案。  
- **最容易踩的坑**  
  - 忘记把 `k` 当作 **1-indexed**（题目从第 1 位开始），导致 off‑by‑one 错误。  
  - 在右半边时忘记对 `op = 1` 累计搬位，结果少加了若干字母。  
  - 没有对搬位次数取模 26，导致字符超出 `'z'` 范围（Python 会报错）。  
- **下次遇到同类题**：第一步立刻问自己“**这一步的操作是否会把字符串对称地分成两段**”，如果是，就尝试**逆向定位**而不是正向构造。这样往往能把指数级的暴力化为线性时间。