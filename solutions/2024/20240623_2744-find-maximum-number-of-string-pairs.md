# #2744. 寻找最大字符串配对数 / Find Maximum Number of String Pairs

> 难度：简单 · 标签：Array、Hash Table、String、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-maximum-number-of-string-pairs/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array words consisting of distinct strings.
The string words[i] can be paired with the string words[j] if:
Return the maximum number of pairs that can be formed from the array words.
Note that each string can belong in at most one pair.

**Examples**

**Example 1:**

```
Input: words = ["cd","ac","dc","ca","zz"]
Output: 2
Explanation: In this example, we can form 2 pair of strings in the following way:
- We pair the 0th string with the 2nd string, as the reversed string of word[0] is "dc" and is equal to words[2].
- We pair the 1st string with the 3rd string, as the reversed string of word[1] is "ca" and is equal to words[3].
It can be proven that 2 is the maximum number of pairs that can be formed.
```

**Example 2:**

```
Input: words = ["ab","ba","cc"]
Output: 1
Explanation: In this example, we can form 1 pair of strings in the following way:
- We pair the 0th string with the 1st string, as the reversed string of words[1] is "ab" and is equal to words[0].
It can be proven that 1 is the maximum number of pairs that can be formed.
```

**Example 3:**

```
Input: words = ["aa","ab"]
Output: 0
Explanation: In this example, we are unable to form any pair of strings.
```

**Constraints**

- 1 <= words.length <= 50
- words[i].length == 2
- words consists of distinct strings.
- words[i] contains only lowercase English letters.

---

## 题目（中文翻译）

You are given a 0-indexed array `words` consisting of distinct strings.  
The string `words[i]` can be paired with the string `words[j]` **iff** the reversed string of `words[i]` is equal to `words[j]` (i.e., `reverse(words[i]) == words[j]`).  

Return the maximum number of pairs that can be formed from the array `words`.  
Note that each string can belong to **at most one** pair.

---

### 示例

**示例 1**  
Input: `words = ["cd","ac","dc","ca","zz"]`  
Output: `2`  
Explanation: 在此示例中，我们可以按如下方式形成 2 对字符串：  
- 将下标 0 的字符串与下标 2 的字符串配对，因为 `words[0]` 的反转为 `"dc"`，等于 `words[2]`。  
- 将下标 1 的字符串与下标 3 的字符串配对，因为 `words[1]` 的反转为 `"ca"`，等于 `words[3]`。  
可以证明 2 是能够形成的最大配对数。

**示例 2**  
Input: `words = ["ab","ba","cc"]`  
Output: `1`  
Explanation: 在此示例中，我们可以按如下方式形成 1 对字符串：  
- 将下标 0 的字符串与下标 1 的字符串配对，因为 `words[1]` 的反转为 `"ab"`，等于 `words[0]`。  
可以证明 1 是能够形成的最大配对数。

**示例 3**  
Input: `words = ["aa","ab"]`  
Output: `0`  
Explanation: 在此示例中，无法形成任何配对。

---

### 约束条件

- `1 <= words.length <= 50`
- `words[i].length == 2`
- `words` 中的字符串互不相同。
- `words[i]` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把数组里每两个下标 `(i, j)`（`i < j`）都拿出来检查一次，看 `words[i]` 的逆序字符串是否正好等于 `words[j]`。  
- **数据结构**：只需要最原始的列表 `words`，不需要额外的结构。可以把“逆序字符串”想象成把单词倒着读，就像我们在看镜子里的文字。  
- **正确性**：因为题目要求“只能配对一次”，只要遍历所有可能的配对并且只在配对成功后把这两个下标标记为已使用，就一定能找到所有合法的配对。  
- **时间/空间复杂度**：  
  - 我们要检查 `C(n,2) = n·(n-1)/2` 对下标，时间复杂度是 **O(n²)**。  
    用大白话说，就是如果有 10 个单词，需要检查大约 45 次；如果有 1000 个单词，就要检查近 500 000 次，显得很慢。  
  - 只用了常数级的额外空间（比如一个 `used` 布尔数组），所以 **空间复杂度是 O(n)**（实际上是 O(1) 额外空间）。

#### 代码（Python）

```python
def maximumPairs_bruteforce(words):
    n = len(words)
    used = [False] * n          # 标记每个单词是否已经配对
    pairs = 0

    for i in range(n):
        if used[i]:                 # 已经配对过的直接跳过
            continue
        for j in range(i + 1, n):
            if used[j]:
                continue
            # 检查 words[i] 的逆序是否等于 words[j]
            if words[i][::-1] == words[j]:
                pairs += 1          # 找到一对
                used[i] = used[j] = True   # 两个单词都标记为已配对
                break               # i 已配对完，去找下一个 i
    return pairs
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 需要两层循环遍历所有可能的 `(i, j)`，每一次检查逆序只花常数时间。  
- **空间复杂度**：`O(n)` —— 额外的 `used` 数组存储每个单词是否已配对。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们把每一对都枚举了一遍。实际上，只要能够 **快速判断** 某个单词的逆序是否已经出现，就不需要双重循环。

**关键观察**：

1. 所有单词长度固定为 2，且互不相同。  
2. 如果 `word = "ab"`，它唯一能配对的单词只能是 `"ba"`（即 `word[::-1]`）。  
3. 因此，只要我们在遍历数组时把已经出现的单词放进一个“字典”（在这里用 `set`），就可以在 **O(1)** 时间内判断当前单词的逆序是否已经出现过。

**步骤**：

- 初始化一个空集合 `seen`，用于存放已经遍历过的单词。  
- 逐个遍历 `words`：  
  - 计算当前单词的逆序 `rev = word[::-1]`。  
  - 如果 `rev` 已经在 `seen` 中，说明我们已经遇到过它的配对单词，**可以立刻形成一对**，计数 `pairs += 1`，并把 `rev` 从集合中移除（因为每个单词只能用一次）。  
  - 否则，把当前单词加入 `seen`，等待以后可能出现的配对。  
- 最终 `pairs` 就是最大配对数。

> **类比**：把 `seen` 想成一个“未配对的单词仓库”。每当有新单词进来，如果仓库里已经有它的“镜像兄弟”，我们立刻把这对兄弟配对走人；否则把它放进仓库继续等待。

**为什么是最优**：  
- 每个单词只被处理一次，查找和插入集合的时间都是 **O(1)**（在 Python 的哈希表实现中），所以整体时间是 **O(n)**。  
- 只用了一个集合来存放最多 `n` 个单词，空间是 **O(n)**，与暴力解的额外空间相当，但时间大幅提升。

#### 代码（Python）

```python
def maximumPairs(words):
    """
    返回可以形成的最大配对数。
    思路：遍历一次，利用哈希集合快速判断逆序是否已出现。
    """
    seen = set()      # 存放尚未配对的单词
    pairs = 0

    for w in words:
        rev = w[::-1]               # 把两字符倒序，例如 "ab" -> "ba"
        if rev in seen:             # 如果逆序已经在集合里，能配对
            pairs += 1
            seen.remove(rev)        # 配对后把对方踢出集合，防止重复使用
        else:
            seen.add(w)             # 暂时放进集合，等待以后可能的配对
    return pairs
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，每次集合的查找/插入/删除都是常数时间。相比暴力的 `O(n²)`，速度提升明显。  
- **空间复杂度**：`O(n)` —— 最坏情况下所有单词都没有配对，需要把它们全部放进集合。

---

## 心得

- **核心技巧**：利用哈希集合（相当于“查字典”）在 **常数时间** 内判断某个元素的匹配关系，从而把双层遍历降到线性遍历。  
- **适用的题型**：  
  1. “配对”或“互为补数”的问题（如两数之和、互为翻转的字符串等）。  
  2. “出现过的元素”需要快速查询的场景（如判断数组中是否存在重复、找出唯一元素）。  
- **一句话总结**：**把“能配对的对象”放进哈希表，一遍遍历即可完成配对**。

---

## 反思

- **第一反应**：看到“逆序配对”，立刻想到两层循环检查每一对——这就是暴力解。  
- **最容易踩的坑**：  
  - 忘记每个单词只能用一次，导致同一个单词被多次计入配对。  
  - 在使用集合时忘记在配对成功后把匹配的单词从集合中移除，导致重复配对。  
- **下次遇到同类题**：第一步先思考“能否用哈希结构把配对关系映射成 O(1) 的查找”，如果可以，就直接走线性解法。