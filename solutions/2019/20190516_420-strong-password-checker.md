# #420. **强密码检查器** / Strong Password Checker

> 难度：困难 · 标签：String、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/strong-password-checker/)

---

## 题目（英文原版）

**Description**

A password is considered strong if the below conditions are all met:
Given a string password, return the minimum number of steps required to make password strong. if password is already strong, return 0.
In one step, you can:

**Examples**

**Example 1:**

```
Input: password = "a"
Output: 5
```

**Example 2:**

```
Input: password = "aA1"
Output: 3
```

**Example 3:**

```
Input: password = "1337C0d3"
Output: 0
```

**Constraints**

- 1 <= password.length <= 50
- password consists of letters, digits, dot '.' or exclamation mark '!'.

---

## 题目（中文翻译）

如果密码满足以下所有条件，则被视为强密码：  
给定一个字符串 `password`，返回使 `password` 变为强密码所需的最少步数。如果 `password` 已经是强密码，返回 `0`。  

在一次操作中，你可以：

（题目原文未给出具体的操作类型，保持原样）

**示例 1：**  
**示例 2：**  
**示例 3：**  

**约束条件**  
- `1 <= password.length <= 50`  
- `password` 仅由字母、数字、点号 `'.'` 或感叹号 `'!'` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的修改方式**，把密码一次一次改成“强密码”，然后取最少的步数。  
- **数据结构**：我们可以把密码看成一个字符数组，遍历它来检查是否满足三条规则（长度、字符种类、连续相同字符）。  
- **生活化类比**：把密码当成一串珠子，规则就像是“珠子总数要在 6~20 之间、必须有红、绿、蓝三种颜色、相邻的同色珠子不能超过两个”。暴力做法就是不停地**往珠子串里插入**、**删除**或**改颜色**，直到满足所有要求。  
- **为什么正确**：只要我们尝试了所有合法的改动组合，必然会找到最少的那一种。  

然而，这种做法的搜索空间非常大：  
- 长度最多 50，可能需要在每个位置插入/删除/替换 3 种操作。  
- 完全的递归/回溯会导致 **指数级** 的时间，根本不可行。

#### 代码（Python）

```python
def strongPasswordChecker_bruteforce(password: str) -> int:
    """
    暴力搜索（仅作概念演示，实际会超时）
    """
    from collections import Counter
    import itertools

    # 检查密码是否已经满足所有规则
    def is_strong(pw: str) -> bool:
        if not (6 <= len(pw) <= 20):
            return False
        has_lower = any('a' <= c <= 'z' for c in pw)
        has_upper = any('A' <= c <= 'Z' for c in pw)
        has_digit = any(c.isdigit() for c in pw)
        if not (has_lower and has_upper and has_digit):
            return False
        # 连续相同字符不能出现 3 次以上
        i = 2
        while i < len(pw):
            if pw[i] == pw[i - 1] == pw[i - 2]:
                return False
            i += 1
        return True

    # BFS（宽度优先搜索）逐层尝试一次、两次…的改动
    from collections import deque
    visited = {password}
    q = deque([(password, 0)])  # (当前字符串, 已经用了多少步)

    while q:
        cur, step = q.popleft()
        if is_strong(cur):
            return step
        # 生成所有一次改动的可能
        for i in range(len(cur)):
            # 删除
            nxt = cur[:i] + cur[i + 1:]
            if nxt not in visited:
                visited.add(nxt)
                q.append((nxt, step + 1))
            # 替换成 0~9、a~z、A~Z 的任意字符（这里仅示例少量字符）
            for ch in "aA0":
                if ch != cur[i]:
                    nxt = cur[:i] + ch + cur[i + 1:]
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append((nxt, step + 1))
        # 在每个位置插入字符（同样仅示例少量字符）
        for i in range(len(cur) + 1):
            for ch in "aA0":
                nxt = cur[:i] + ch + cur[i:]
                if nxt not in visited:
                    visited.add(nxt)
                    q.append((nxt, step + 1))
    return -1   # 理论上不会到这里
```

> **注意**：上述代码只用于说明“暴力思路”。在 LeetCode 上会因为搜索空间太大而 **TLE**（超时）。

#### 复杂度

- **时间复杂度**：`O(3^n)`（指数级），因为每一步我们都可能进行插入、删除、替换三种操作，搜索树的分支指数增长。  
- **空间复杂度**：`O(3^n)`，需要保存所有已经访问过的状态，同样呈指数级增长。  

> 大白话解释：如果密码长度是 10，理论上要尝试的情况多到“天文数字”，根本不可能在几秒钟内算完。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**枚举所有改动是不现实的**。我们需要利用题目本身的结构，直接算出最少的改动步数。关键在于把 **插入、删除、替换** 三类操作的影响分离出来，然后用 **贪心**（一次性把最有价值的改动做掉）来求最优。

1. **统计缺少的字符种类**  
   - 必须同时出现小写字母、大写字母、数字。  
   - 用 `missing_type = 3 - (has_lower + has_upper + has_digit)` 统计还缺几类。  
   - 这一步只需要一次遍历，时间 `O(n)`。

2. **找出所有连续重复字符序列**（长度 ≥ 3）  
   - 比如 `"aaa"`、`"bbbb"`、`"cccccc"`。  
   - 对每个序列记下它的长度 `len_seq`，以及 `len_seq // 3`（需要多少次 **替换** 才能把“3 连在一起”打散）。  
   - 这里把序列按照 `len_seq % 3`（余数）分到三类：
     - **余数 0**：每删除 1 个字符就能立刻少一次替换（因为 `3k` → `3k-1`，`//3` 减 1）。
     - **余数 1**：每删除 2 个字符才会少一次替换（`3k+1` → `3k-1`）。
     - **余数 2**：每删除 3 个字符才会少一次替换（但在长度已经合规时，我们直接用替换就可以）。
   - 这一步同样只需要一次遍历，时间 `O(n)`。

3. **根据密码长度分情况讨论**  

   - **长度 < 6**（太短）  
     - 只能**插入**字符，插入既能增加长度，又能补齐缺失的字符种类。  
     - 最少步数 = `max(missing_type, 6 - len(password))`。  
     - 解释：如果缺少两类字符但只差 1 位长度，仍然需要 2 步（先补缺的字符，再插入任意字符补齐长度）。

   - **6 ≤ 长度 ≤ 20**（长度合规）  
     - 只能通过**替换**来消除连续重复。  
     - 替换次数 = 所有 `len_seq // 3` 之和，记作 `replace_needed`。  
     - 最少步数 = `max(missing_type, replace_needed)`。  
     - 解释：如果缺少字符种类更多，就先用替换来补齐种类；否则只需要把重复序列打散。

   - **长度 > 20**（太长）  
     - 必须**删除**多余的字符，使长度不超过 20。设 `delete_needed = len(password) - 20`。  
     - 删除可以帮助减少后面需要的替换次数（因为删除了重复序列的一部分）。  
     - **贪心删除策略**：
       1. 先对余数为 0 的序列，每删除 1 个字符可以立刻少一次替换。我们尽可能多地在这些序列上删，直到 `delete_needed` 用完或这些序列处理完。
       2. 再对余数为 1 的序列，每删除 2 个字符可以少一次替换。继续用相同的方式消耗 `delete_needed`。
       3. 最后对余数为 2 的序列（以及仍然剩余的序列），每删除 3 个字符可以少一次替换。  
     - 删除完后，重新计算剩余的 **替换需求**：`replace_needed = sum( (len_seq // 3) for 剩余序列 )`。  
     - 最少步数 = `delete_needed + max(missing_type, replace_needed)`。  
     - 解释：删除是必须的（因为长度超限），而在删除的过程中我们尽量“杀掉”一些需要替换的地方，最后再用剩余的替换或补齐缺少的字符种类。

4. **整体算法**  
   - 一次遍历得到 `missing_type` 与所有重复序列的长度。  
   - 根据长度区间执行相应的公式或贪心删除。  
   - 整个过程只用了 **线性时间** `O(n)`，空间只用来存放重复序列的长度，最多 `O(n)`（实际远小于 n）。

> **类比**：把密码看成一根绳子，要求绳子长度在 6~20 之间，颜色要齐全（红、绿、蓝），且不能出现三根相同颜色的线连在一起。我们先检查缺了哪些颜色，再检查哪些地方有三根同色连在一起，最后根据绳子是太短、正好还是太长，决定是**加线**、**换颜色**还是**剪线**，并且在剪线时优先剪掉那些导致“三连”最多的地方，这样剪一次就能省掉一次换颜色的工作。

#### 代码（Python）

```python
def strongPasswordChecker(password: str) -> int:
    """
    最优解：贪心 + 分类讨论，时间 O(n)，空间 O(n)
    """
    n = len(password)

    # 1️⃣ 检查三类字符是否缺失
    has_lower = any('a' <= c <= 'z' for c in password)
    has_upper = any('A' <= c <= 'Z' for c in password)
    has_digit = any(c.isdigit() for c in password)
    missing_type = 3 - (has_lower + has_upper + has_digit)   # 需要补的种类数

    # 2️⃣ 找出所有连续相同字符序列（长度 >= 3）
    repeats = []          # 存放每段重复序列的长度
    i = 2
    while i < n:
        if password[i] == password[i-1] == password[i-2]:
            j = i - 2
            # 向后扩展，找到这段连续相同字符的结束位置
            while i < n and password[i] == password[j]:
                i += 1
            repeats.append(i - j)   # 记录该段长度
        else:
            i += 1

    # ---------- 情况一：长度 < 6 ----------
    if n < 6:
        # 需要插入的字符数
        insert_needed = 6 - n
        # 插入的同时可以补齐缺失的字符种类，取两者的最大值即可
        return max(missing_type, insert_needed)

    # ---------- 情况二：6 <= 长度 <= 20 ----------
    if n <= 20:
        # 只需要用替换来打散重复序列
        replace_needed = 0
        for length in repeats:
            replace_needed += length // 3   # 每 3 个相同字符需要一次替换
        return max(missing_type, replace_needed)

    # ---------- 情况三：长度 > 20 ----------
    delete_needed = n - 20                # 必须删除的字符数
    # 为了让删除更有价值，先把 repeats 按余数分类
    # cnt_mod[i] 记录余数为 i 的序列对应的“需要多少次替换”
    cnt_mod = [0, 0, 0]                   # 分别对应 len%3 == 0/1/2
    for length in repeats:
        cnt_mod[length % 3] += 1

    # 1) 优先删除余数为 0 的序列，每删 1 个可省掉一次替换
    #    这里用 min 防止删除超过需要的次数
    #    同时更新对应的替换需求
    #    (删除后，序列长度会变成 length-1，替换次数减 1)
    #    需要注意：cnt_mod[0] 记录的是这类序列的数量，而不是总长度
    #    因此我们直接把 delete_needed 用掉多少次就行
    #    每次删除 1 次，replace_needed 也会相应减少 1 次
    #    所以这里用 while 循环更直观
    replace_needed = 0
    # 先处理余数为 0 的序列
    for i in range(3):
        if i == 0:
            # 每删除 1 个字符，能减少 1 次 replace
            take = min(cnt_mod[0], delete_needed)
            delete_needed -= take
            cnt_mod[0] -= take
        elif i == 1:
            # 每删除 2 个字符，能减少 1 次 replace
            take = min(cnt_mod[1] * 2, delete_needed) // 2
            delete_needed -= take * 2
            cnt_mod[1] -= take
        else:   # i == 2
            # 每删除 3 个字符，能减少 1 次 replace
            take = min(cnt_mod[2] * 3, delete_needed) // 3
            delete_needed -= take * 3
            cnt_mod[2] -= take

    # 删除完上述“有价值的删除”后，仍可能剩余 delete_needed，
    # 这时只能直接在任意位置删除，不能再进一步减少 replace 次数。
    # 此时所有剩余的重复序列（不管余数是多少）都需要用替换来处理。
    # 替换次数等于每段长度除以 3（向下取整），这里把所有残余的
    # cnt_mod 汇总回去计算。
    # 实际上，cnt_mod 只记录了每种余数的“序列数量”，
    # 为了简化，我们重新遍历 repeats，计算最终的 replace_needed。
    # 这里的 delete_needed 已经被消耗完（或剩余但无效），
    # 所以直接按照剩余的 length 重新计算。
    # 为了避免再次遍历 repeats，这里直接用公式：
    #   total_replace = sum(length // 3) - 已经因删除而省掉的次数
    # 已经省掉的次数 = 原始 cnt_mod[0] + cnt_mod[1] + cnt_mod[2]（在上面删除时对应的减少量）
    # 为了代码可读，这里直接遍历一次 repeats：
    remaining_delete = n - 20  # 原始需要删除的数量（用于后面计算最终替换）
    # 重新计算 replace_needed，考虑已经完成的有价值删除
    replace_needed = 0
    for length in repeats:
        # 先把这段长度减去我们已经用来删除的字符数
        # 删除的原则是优先在余数为 0、1、2 的序列上进行
        # 为了简化，这里不再细化每段的删除情况，而是直接用
        # length // 3 计数，后面再减去已经“抵消”的次数
        replace_needed += length // 3

    # 实际上，上面已经把所有有价值的删除用掉了，
    # 只剩下纯粹的 delete_needed（可能为 0），
    # 替换次数需要再减去在删除过程中已经抵消的次数。
    # 把已经抵消的次数累计起来：
    #   - 对余数为 0 的序列，每删除 1 次抵消 1 次 replace
    #   - 对余数为 1 的序列，每删除 2 次抵消 1 次 replace
    #   - 对余数为 2 的序列，每删除 3 次抵消 1 次 replace
    # 我们在前面的循环中已经计算了这些抵消的次数，
    # 用变量 `saved` 来记录。
    saved = 0
    # 重新遍历一次，按照之前的删除策略统计抵消的次数
    # 这里用最直接的实现方式（因为 n ≤ 50，性能影响可以忽略）
    delete_left = n - 20
    # 按余数 0、1、2 的顺序尝试删除
    for mod in range(3):
        for length in repeats:
            if length < 3 or length % 3 != mod:
                continue
            # 能够通过删除来抵消的次数
            while length >= 3 and delete_left > 0:
                if mod == 0:
                    # 删除 1 次抵消 1 次 replace
                    length -= 1
                    delete_left -= 1
                    saved += 1
                elif mod == 1 and delete_left >= 2:
                    # 删除 2 次抵消 1 次 replace
                    length -= 2
                    delete_left -= 2
                    saved += 1
                elif mod == 2 and delete_left >= 3:
                    # 删除 3 次抵消 1 次 replace
                    length -= 3
                    delete_left -= 3
                    saved += 1
                else:
                    break
    # 最终的 replace 需求
    replace_needed = max(0, replace_needed - saved)

    # 最终步数 = 必须删除的次数 + 需要补齐的字符种类或替换次数（取最大）
    return (n - 20) + max(missing_type, replace_needed)
```

> **代码说明（关键行中文注释）**  
- 第 7‑12 行：统计是否包含小写、大写、数字，算出缺少的种类数 `missing_type`。  
- 第 15‑28 行：遍历字符串，找出所有连续相同字符长度 ≥ 3 的序列，存入 `repeats`。  
- 第 31‑37 行：处理长度 < 6 的情况，返回 `max(missing_type, 6 - n)`。  
- 第 40‑47 行：处理 6~20 的情况，只需要替换，返回 `max(missing_type, replace_needed)`。  
- 第 50‑94 行：长度 > 20 时的核心贪心删除。先统计不同 `len % 3` 的序列数量，然后按优先级（0 → 1 → 2）使用删除来“抵消”替换需求。  
- 第 97‑108 行：在删除完有价值的字符后，重新计算仍然需要的替换次数 `replace_needed`。  
- 第 111‑113 行：返回总步数 = 必须删除的字符数 + 其余步骤的最大值。

> **实现细节**：为了代码可读性，这里用了两遍遍历 `repeats` 来分别统计 “抵消的替换次数” 与 “最终的替换需求”。由于密码长度上限只有 50，时间开销仍然是线性级别，完全符合要求。

#### 复杂度

- **时间复杂度**：`O(n)`，只需要对密码字符串做几次线性遍历（`n = len(password)`），即使在长度 > 20 时的贪心删除也只遍历了有限次数的重复序列。  
  - 大白话：即使密码有 50 个字符，程序也只会跑几百条指令，几乎是瞬间完成。  
- **空间复杂度**：`O(n)`，主要用于保存所有重复序列的长度列表 `repeats`（最坏情况下每三个字符形成一个序列，数量不超过 `n/3`）。  

> 与暴力解相比，时间从 **指数级** 降到了 **线性级**，几乎可以在所有测试用例里毫秒通过。

---

## 心得

- **核心技巧**：**分类讨论 + 贪心删除**。先把问题拆成“长度不足”“长度合规”“长度超限”三类，再在超长情况下用“删除先削弱重复序列”来同步减少两类操作的成本。  
- **适用的题型**  
  1. “密码强度检查”系列（如 LeetCode 420）。  
  2. 需要在 **删除、插入、替换** 中平衡的字符串编辑题（如编辑距离的变形）。  
  3. 任何出现 **连续重复子串** 且有长度上下限的约束问题。  
- **一句话总结解题钥匙**：**把“删”当成“杀手”，先在最能降低“换”需求的地方删，再用最少的“换”或“插”补齐缺失的字符种类。**

---

## 反思

- **第一反应**：看到“三个要求”，我先想到要分别检查缺少的字符种类、长度是否合规、以及连续相同字符是否超过两位。于是尝试直接枚举所有改动（暴力），结果发现不可行。  
- **最容易踩的坑**  
  - 忽略 **长度 < 6** 时插入既能补长度也能补字符种类的互相抵消关系。  
  - 在 **长度 > 20** 时只考虑删除，不利用删除削减重复序列的机会，导致替换次数被高估。  
  - 边界条件：例如 `"aaaaa"`（长度 5，缺少大写和数字），既需要插入也需要替换，必须取两者的最大值。  
- **下次遇到同类题**：**第一步先分类讨论长度区间**，再分别处理“缺少种类”和“连续重复”。如果是超长情况，立刻想到“用删除先打掉重复”，这一步往往是关键的最优化点。