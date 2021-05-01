# #1316. 不同的回声子串 / Distinct Echo Substrings

> 难度：困难 · 标签：String、Trie、Rolling Hash、Hash Function · [LeetCode 链接](https://leetcode.com/problems/distinct-echo-substrings/)

---

## 题目（英文原版）

**Description**

Return the number of distinct non-empty substrings of text that can be written as the concatenation of some string with itself (i.e. it can be written as a + a where a is some string).

**Examples**

**Example 1:**

```
Input: text = "abcabcabc"
Output: 3
Explanation: The 3 substrings are "abcabc", "bcabca" and "cabcab".
```

**Example 2:**

```
Input: text = "leetcodeleetcode"
Output: 2
Explanation: The 2 substrings are "ee" and "leetcodeleetcode".
```

**Constraints**

- 1 <= text.length <= 2000
- text has only lowercase English letters.

---

## 题目（中文翻译）

返回 **text** 中可以表示为某个字符串与自身连接（即可以写成 a + a，其中 a 为任意字符串）的非空子串（substring）的不同个数。

**示例 1**  
输入: `text = "abcabcabc"`  
输出: `3`  
解释: 这 3 个子串分别是 `"abcabc"`、`"bcabca"` 和 `"cabcab"`。

**示例 2**  
输入: `text = "leetcodeleetcode"`  
输出: `2`  
解释: 这 2 个子串分别是 `"ee"` 和 `"leetcodeleetcode"`。

**约束条件**  

- `1 <= text.length <= 2000`
- `text` 仅包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举所有子串**，然后判断它能否写成 `a + a`（即前后两段完全相同）。  
具体步骤如下：

1. **遍历起始位置** `i`（0 ≤ i < n），**遍历结束位置** `j`（i+1 ≤ j ≤ n），得到子串 `text[i:j]`。  
2. 若子串长度是奇数，显然不可能是 `a + a`，直接跳过。  
3. 长度为偶数时，把子串均分成两半 `left = text[i:mid]`、`right = text[mid:j]`（`mid = i + (j-i)//2`），逐字符比较 `left` 与 `right` 是否相同。  
4. 若相同，则把这个子串加入 **集合**（set），利用集合天然的去重特性，最终集合的大小就是答案。

> **数据结构类比**：集合（set）就像一本“已经出现过的词典”，每次想记下一个新词时，先去词典里查查有没有，如果没有才真正写进去，这样自然避免了重复。

> **为什么正确**：只要遍历了所有可能的子串，并且对每个子串严格检查“前半段是否等于后半段”，就不会遗漏任何合法的 “回文式” 子串；使用集合去重则保证了“不同的子串”只计一次。

#### 代码（Python）

```python
def distinctEchoSubstrings_bruteforce(text: str) -> int:
    n = len(text)
    echo_set = set()                     # 用来存放所有不同的回文式子串

    # 枚举所有子串的左端点 i
    for i in range(n):
        # 枚举右端点 j（不包括 j 本身），子串为 text[i:j]
        for j in range(i + 2, n + 1, 2):   # 只考虑长度为偶数的子串，步长设为 2
            mid = i + (j - i) // 2        # 子串的中间位置
            left = text[i:mid]            # 前半段
            right = text[mid:j]           # 后半段
            if left == right:             # 逐字符比较
                echo_set.add(text[i:j])   # 加入集合，自动去重

    return len(echo_set)
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 外层两层循环枚举所有子串，数量约为 `n²/2`。  
  - 对每个子串我们要逐字符比较两半，最坏情况下比较长度为 `O(n)`，于是总体是 `O(n³)`。  
  - 大白话：如果文本长度是 1000，粗略估算会进行约 `10⁹` 次字符比较，显然会超时。

- **空间复杂度**：`O(n²)`（最坏情况集合中保存了所有合法子串）  
  - 每个合法子串最多长度 `n`，但实际只保存子串本身的引用，最多 `n²/2` 条记录。  

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于每次比较两半时都要逐字符遍历，这会把时间推到 `O(n³)`。  
我们可以把“比较两段是否相同”这一步 **降到 O(1)**，方法是 **哈希（Rolling Hash）**：

1. **前缀哈希**  
   - 设定一个基数 `B`（常取 31、131 等）和一个大质数模 `M`（如 `10⁹+7`）。  
   - 计算 `pref[i]` 表示 `text[0:i]`（左闭右开）的哈希值：  
     `pref[i+1] = (pref[i] * B + (ord(text[i]) - ord('a') + 1)) % M`。  
   - 同时预先计算 `powB[i] = Bⁱ % M`，用于后面快速取子串哈希。

2. **子串哈希**  
   - 任意子串 `text[l:r]`（左闭右开）的哈希可以 **O(1)** 通过公式得到：  
     `hash(l, r) = (pref[r] - pref[l] * powB[r-l]) % M`（注意取模正数化）。

3. **枚举所有偶数长度子串**  
   - 与暴力法相同，只是把 “左半段是否等于右半段” 改为 **比较它们的哈希值**。  
   - 若 `hash(i, mid) == hash(mid, j)`，则子串 `text[i:j]` 合法。

4. **防止哈希冲突**  
   - 单个模数可能出现冲突（不同字符串得到相同哈希），我们使用 **双模**（两个不同的大质数）一起判断，冲突概率几乎可以忽略不计。  
   - 把 `(hash1, hash2)` 这对值作为集合的键，仍然能保证不同子串不被误判为相同。

> **核心概念——滚动哈希（Rolling Hash）**  
> 想象一本书的每一页都有一个编号（哈希值），我们只要记住从开头到任意位置的累计编号，就能 **快速算出任意区间的编号**，而不必重新遍历整段文字。就像在超市结账时，系统已经累计了每件商品的总价，想要查询任意子购物车的总价，只需要用总价减去前面的累计价即可。

#### 代码（Python）

```python
def distinctEchoSubstrings(text: str) -> int:
    n = len(text)
    MOD1, MOD2 = 1_000_000_007, 1_000_000_009   # 两个大质数
    BASE = 91138233                               # 随机的基数，避免与字符冲突

    # 预计算幂、前缀哈希（双模）
    pow1 = [1] * (n + 1)
    pow2 = [1] * (n + 1)
    pref1 = [0] * (n + 1)
    pref2 = [0] * (n + 1)

    for i, ch in enumerate(text):
        code = ord(ch) - ord('a') + 1
        pow1[i + 1] = (pow1[i] * BASE) % MOD1
        pow2[i + 1] = (pow2[i] * BASE) % MOD2
        pref1[i + 1] = (pref1[i] * BASE + code) % MOD1
        pref2[i + 1] = (pref2[i] * BASE + code) % MOD2

    # 取子串 [l, r) 的双模哈希值，返回 (h1, h2)
    def get_hash(l: int, r: int):
        h1 = (pref1[r] - pref1[l] * pow1[r - l]) % MOD1
        h2 = (pref2[r] - pref2[l] * pow2[r - l]) % MOD2
        # Python 取模可能为负数，统一转为正数
        return (h1 + MOD1) % MOD1, (h2 + MOD2) % MOD2

    echo_set = set()   # 存放所有不同合法子串的哈希对

    # 枚举所有偶数长度子串
    for i in range(n):
        # 子串长度必须是偶数，step=2 保证只看偶数长度
        for length in range(2, n - i + 1, 2):
            mid = i + length // 2
            # 比较左半段与右半段的哈希
            if get_hash(i, mid) == get_hash(mid, i + length):
                echo_set.add(get_hash(i, i + length))   # 直接把哈希对加入集合

    return len(echo_set)
```

> **代码要点注释**  
> - `BASE` 取一个比较大的随机数，能让不同字符的贡献更加分散，降低冲突概率。  
> - `pow1 / pow2` 保存 `BASE^k mod MOD`，用于 **O(1)** 取子串哈希。  
> - `get_hash` 同时返回两模哈希，确保“几乎不可能出现冲突”。  
> - 最后把 **哈希对** 加入 `set`，不需要再保存实际子串，节省内存。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 两层循环遍历所有偶数长度子串，数量约为 `n²/2`。  
  - 每次比较只需 **O(1)** 的哈希取值和相等判断，所以整体是二次方。  
  - 与暴力解相比，从 `O(n³)` 降到了 `O(n²)`，对 `n ≤ 2000` 完全足够（约 4 × 10⁶ 次操作）。

- **空间复杂度**：`O(n)`（前缀哈希数组）+ `O(k)`（集合），其中 `k` 为不同合法子串的个数，最坏不超过 `n²/2`，但实际远小于 `n²`。  
  - 与暴力解的 `O(n²)`（存完整子串）相比，仅保存 **哈希对**，内存占用更低。

---

## 心得  

- **核心技巧**：**滚动哈希 + 前缀哈希**，把“比较两段是否相同”从线性降到常数。  
- **适用的题型**：  
  1. 判断子串是否是回文或重复结构（如 *Repeated Substring Pattern*）。  
  2. 求不同子串的数量（如 *Distinct Substrings*、*Longest Duplicate Substring*）。  
  3. 字符串匹配的加速（如 *Rabin‑Karp* 搜索）。  
- **一句话总结解题钥匙**：**先把“比较”转化为“哈希相等”，再用集合去重**。

---

## 反思  

- **第一反应**：直接枚举所有子串并逐字符比较，想到集合去重。  
- **最容易踩的坑**：  
  - 忘记只枚举 **偶数长度** 的子串，导致不必要的比较。  
  - 取模后出现负数，导致哈希不一致，需要 `+ MOD` 再 `% MOD`。  
  - 单模哈希可能冲突，尤其在长度 2000 的情况下，使用 **双模** 更保险。  
- **下次类似题的第一步**：  
  1. 看能否把“相等判定”改写为“哈希相等”。  
  2. 先构造前缀哈希，保证子串哈希 O(1) 取值。  
  3. 再考虑去重方式（集合/Trie），完成整体 O(n²) 的方案。