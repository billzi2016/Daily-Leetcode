# #929. 唯一的电子邮件地址 / Unique Email Addresses

> 难度：简单 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/unique-email-addresses/)

---

## 题目（英文原版）

**Description**

Every valid email consists of a local name and a domain name, separated by the '@' sign. Besides lowercase letters, the email may contain one or more '.' or '+'.
If you add periods '.' between some characters in the local name part of an email address, mail sent there will be forwarded to the same address without dots in the local name. Note that this rule does not apply to domain names.
If you add a plus '+' in the local name, everything after the first plus sign will be ignored. This allows certain emails to be filtered. Note that this rule does not apply to domain names.
It is possible to use both of these rules at the same time.
Given an array of strings emails where we send one email to each emails[i], return the number of different addresses that actually receive mails.

**Examples**

**Example 1:**

```
Input: emails = ["test.email+alex@leetcode.com","test.e.mail+bob.cathy@leetcode.com","testemail+david@lee.tcode.com"]
Output: 2
Explanation: "testemail@leetcode.com" and "testemail@lee.tcode.com" actually receive mails.
```

**Example 2:**

```
Input: emails = ["a@leetcode.com","b@leetcode.com","c@leetcode.com"]
Output: 3
```

**Constraints**

- 1 <= emails.length <= 100
- 1 <= emails[i].length <= 100
- emails[i] consist of lowercase English letters, '+', '.' and '@'.
- Each emails[i] contains exactly one '@' character.
- All local and domain names are non-empty.
- Local names do not start with a '+' character.
- Domain names end with the ".com" suffix.
- Domain names must contain at least one character before ".com" suffix.

---

## 题目（中文翻译）

每个有效的电子邮件由本地名（local name）和域名（domain name）组成，两者之间用 '`@`' 符号分隔。除了小写字母外，电子邮件中还可能出现一个或多个 `.` 或 `+`。

- 如果在本地名部分的某些字符之间插入句点 `.`，发送到该地址的邮件会被转发到去掉所有句点后的同一地址。**此规则不适用于域名**。
- 如果在本地名中加入加号 `+`，则第一个加号之后的所有字符都会被忽略。此特性可用于邮件过滤。**此规则也不适用于域名**。
- 这两条规则可以同时使用。

给定一个字符串数组 `emails`，其中 `emails[i]` 表示向该地址发送一封邮件，返回实际收到邮件的不同地址的数量。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  
**示例 1:**  
```text
Input: emails = ["test.email+alex@leetcode.com","test.e.mail+bob.cathy@leetcode.com","testemail+david@lee.tcode.com"]
Output: 2
Explanation: 实际收到邮件的地址为 "testemail@leetcode.com" 和 "testemail@lee.tcode.com"。
```

**示例 2:**  
```text
Input: emails = ["a@leetcode.com","b@leetcode.com","c@leetcode.com"]
Output: 3
```

**约束条件**  
- `1 <= emails.length <= 100`
- `1 <= emails[i].length <= 100`
- `emails[i]` 只包含小写英文字母、`'+'`、`'.'` 和 `'@'`
- 每个 `emails[i]` 恰好包含一个 `'@'` 字符
- 所有本地名和域名均非空
- 本地名不以 `'+'` 开头
- 域名以 `".com"` 为后缀
- 在 `".com"` 前的域名部分至少包含一个字符

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的核心在于把每个邮箱地址 **标准化**（去掉不影响投递的字符），然后统计不同的标准化结果有多少个。  
我们可以把每个邮箱拆成两部分：

* **local name**（@ 前面的部分）  
* **domain name**（@ 后面的部分）

对 **local name** 做两件事：

1. **去掉所有的 `.`**  
   把 `.` 想象成句子里的空格，去掉它们不影响意思。  
2. **遇到第一个 `+` 就把后面的全部丢掉**  
   `+` 好比信封上的“备注”，只要出现一次，后面的文字都不再被考虑。

对 **domain name** 完全不做任何处理，因为题目说它不受规则影响。

把处理好的 `local + '@' + domain` 放进一个 **集合（hash table）**，集合天然会去重。遍历完所有邮箱后，集合的大小就是答案。

> **哈希表（集合）类比**：就像一本电话簿，里面每个名字只能出现一次，想把一个新名字加入时，如果已经存在，就不会再存一遍。

#### 代码（Python）

```python
def numUniqueEmails(emails):
    """
    统计标准化后不同邮箱的数量
    :param emails: List[str] 输入的原始邮箱列表
    :return: int 不同收件地址的数量
    """
    uniq = set()                     # 用集合自动去重
    for e in emails:                 # 逐个处理每个邮箱
        local, domain = e.split('@') # 按 '@' 分成 local 与 domain

        # 1. 只保留第一个 '+' 前面的部分（如果没有 '+'，whole string 保留）
        if '+' in local:
            local = local[:local.index('+')]

        # 2. 删除所有的 '.'（直接用 replace 替换为空字符）
        local = local.replace('.', '')

        # 3. 把处理好的两部分重新拼成标准邮箱，放进集合
        uniq.add(local + '@' + domain)

    return len(uniq)                 # 集合的长度即为不同地址的数量
```

#### 复杂度

- **时间复杂度：O(N·L)**  
  - `N` 为邮箱数量（最多 100），`L` 为单个邮箱的最大长度（最多 100）。  
  - 对每个邮箱我们只遍历一次字符（`split`、`replace`、`index` 都是线性），所以总体是 `N` 与 `L` 的乘积。  
  - 用大白话说，就是“如果有 100 封信，每封信最多 100 个字符，那最多要看 10,000 个字符”。

- **空间复杂度：O(N·L)**  
  - 最坏情况下所有邮箱都不相同，需要把它们全部放进集合。集合里每个元素仍然是完整的邮箱字符串，长度约为 `L`，所以总空间是 `N·L`。  
  - 这也是我们必须的额外空间，用来记住已经出现过的地址。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正的“慢点”并不在算法本身，而是 **我们如何组织代码**。  
- `split('@')`、`replace('.')`、`index('+')` 都已经是 **线性** 操作，已经是最简的时间复杂度了。  
- 关键在于 **一次遍历完成所有规则**，不必额外的多次遍历或创建临时列表。

下面的实现把 **去除 `.`** 与 **截断 `+`** 合并到一次遍历中，用 `for` 循环手动构造处理后的 `local`，这样可以省掉 `replace` 与 `split` 带来的额外遍历（虽然对本题规模影响不大，但展示了更“最优”的写法）。

核心数据结构仍是 **集合（哈希表）**，因为它提供 O(1) 的插入与查重。

#### 代码（Python）

```python
def numUniqueEmails(emails):
    """
    更“最优”的实现：一次遍历完成所有规则的处理
    """
    uniq = set()
    for e in emails:
        # 1. 先找到 '@' 的位置，把 domain 直接切出来
        at_idx = e.find('@')
        domain = e[at_idx:]               # 包含 '@' 本身，方便后面直接拼接

        # 2. 处理 local 部分
        local_builder = []                # 用列表收集字符，最后再 join 成字符串
        i = 0
        while i < at_idx:                 # 只遍历到 '@' 前面
            ch = e[i]
            if ch == '+':                 # 碰到第一个 '+'，后面的都忽略
                break
            if ch != '.':                 # '.' 被直接跳过
                local_builder.append(ch)
            i += 1

        local = ''.join(local_builder)    # 把列表转成字符串
        uniq.add(local + domain)          # 加入集合完成去重

    return len(uniq)
```

> **为什么这更好？**  
> - 只遍历一次字符串（从左到右），既找 `@`、又处理 `.` 与 `+`，没有额外的 `split`、`replace` 调用。  
> - 对于极端长字符串（虽然本题限制 100），这种写法的常数因子更小。

#### 复杂度

- **时间复杂度：O(N·L)**  
  - 仍然是对每个字符只看一次，只是把多个线性操作合并成一次遍历，实际运行会更快。

- **空间复杂度：O(N·L)**  
  - 需要的额外空间仍然是保存所有唯一邮箱的集合，和前面的实现相同。

---

## 心得

- **核心技巧**：**字符串标准化 + 哈希表去重**。  
- **适用的题型**：  
  1. “判断两个字符串在忽略某些字符后是否相等” （如 *Valid Palindrome* 中忽略非字母字符）。  
  2. “对一组数据进行归一化后统计不同种类” （如 *Number of Distinct Islands*）。  
- **解题钥匙**：先把 **规则抽象成“把原始数据映射到唯一的标准形式”**，再利用 **集合** 自动去重。

## 反思

- **第一反应**：把每封邮件拆分后按规则手动处理，再用集合计数。  
- **最容易踩的坑**：  
  - 忘记 **domain** 部分不受规则影响，误删了 `.`。  
  - `+` 只在 **local** 部分起作用，出现于 `domain` 时不应截断。  
  - `local` 可能根本没有 `+`，这时要保留全部字符。  
- **下次思路**：遇到类似“过滤/归一化后计数”的题目，第一步就想 **“把每个元素映射到唯一的标准形式 → 用哈希结构去重”**。这样可以快速定位解法方向。